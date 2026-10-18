# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Coco Pharmaceuticals subscription loads.

Copies the digital product data that has been delivered to each subscribing system in the subscription_staging
database into that system's own tables, as soon as it arrives.  There is one DAG per system estate, each writing to
that estate's database:

    coco_subscriptions_coco_pharma         the Coco Pharmaceuticals systems (coco_pharma)
    coco_subscriptions_austin_systems      the acquired Austin site's systems (austin_systems)
    coco_subscriptions_bucharest_systems   the acquired EKG Pharmaceuticals systems (bucharest_systems)

Delivering a product into subscription_staging - one schema per subscription, holding the product's tables plus
delivery columns - is the job of Egeria's provisioning services.  A delivered row has processing_status
'delivered'.  These DAGs take it from there.

The work is defined by the apply scripts in coco-subscription-loads/<database>/<system schema>/<product schema>.sql,
one per subscription.  An apply script runs in the destination system's database, in one transaction, with a
temporary table incoming_<product table> for each of the product's tables holding the rows waiting for this
subscriber, plus a discard_reason column.  The script first sets discard_reason on any rows that are not
appropriate to the system - another estate's data, records the system does not keep - and then writes the
remaining rows into the system's own tables, transforming them from the product's form into the system's.

Each DAG runs continuously:

1. wait_for_deliveries - a sensor that looks about once a minute for rows with processing_status 'delivered' in
   the estate's subscriptions, and finishes as soon as it finds some.  It waits in reschedule mode, so it holds no
   worker slot between checks.
2. choose_subscriptions - runs the apply tasks of the subscriptions with rows waiting; the rest are skipped.
3. <system>.apply__<product schema> - applies the waiting rows, then marks each of them in subscription_staging:
   processed, with 'applied' or the discard reason as its processing_message, or failed, with the error, if the
   apply script fails.  A failed row stays failed until its processing_status is set back to 'delivered', which is
   also how a subscriber reprocesses data.  A row that is delivered again while it is being applied keeps the new
   delivery's 'delivered' status.

Each apply task declares the subscription's staging tables and the system tables its script writes as Airflow
assets, for OpenLineage.

Connections (set as AIRFLOW_CONN_* in airflow-marquez.yaml): subscription_staging, and one per system database,
named after the database.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.standard.sensors.python import PythonSensor
from airflow.sdk import DAG, Asset, PokeReturnValue, TaskGroup

log = logging.getLogger(__name__)

LOADS_DIR = Path(__file__).parent / "coco-subscription-loads"
STAGING_CONN_ID = "subscription_staging"
ESTATES = {
    "coco_pharma": ("Coco core", "coco"),
    "austin_systems": ("Austin", "aus"),
    "bucharest_systems": ("Bucharest", "buc"),
}
DELIVERY_COLUMNS = ["delivery_identifier", "delivery_timestamp", "processing_status", "processing_timestamp",
                    "processing_message"]
# Where the databases live, as the Airflow containers see them - used only to name the assets.
POSTGRES_AUTHORITY = "host.docker.internal:5442"
POKE_INTERVAL = timedelta(seconds=60)
SENSOR_TIMEOUT = timedelta(hours=12)


def asset(database: str, schema: str, table: str) -> Asset:
    return Asset(name=f"{database}.{schema}.{table}",
                 uri=f"postgres://{POSTGRES_AUTHORITY}/{database}/{schema}/{table}")


def subscription_schema(database: str, system: str, product_schema: str) -> str:
    """The subscription's schema in subscription_staging: <estate>_<system>__<product>, without doubling 'coco'."""
    prefix = ESTATES[database][1]
    base = system if prefix == "coco" and system.startswith("coco") else f"{prefix}_{system}"
    return f"{base}__{product_schema}"


class Subscription:
    """One subscribing system taking one digital product, and the script that applies it."""

    def __init__(self, path: Path):
        self.path = path
        self.database = path.parent.parent.name
        self.system = path.parent.name
        self.product_schema = path.stem
        self.schema = subscription_schema(self.database, self.system, self.product_schema)
        self.sql = path.read_text().strip()
        self.target_tables = sorted(set(re.findall(
            rf"\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM|MERGE\s+INTO)\s+{re.escape(self.system)}\.([a-z0-9_]+)",
            self.sql, re.I)))
        self.source_tables = sorted(set(re.findall(r"\bincoming_([a-z0-9_]+)", self.sql)))
        self.task_id = f"apply__{self.product_schema}"
        self.full_task_id = f"{self.system}.{self.task_id}"


def subscriptions_for(database: str) -> list[Subscription]:
    return [Subscription(p) for p in sorted((LOADS_DIR / database).glob("*/*.sql"))]


def staging_tables(cur, schema: str) -> dict[str, tuple[list[tuple[str, str]], list[str]]]:
    """For each table of a subscription schema: its product columns with their types, and its primary key."""
    cur.execute("""
        SELECT c.relname, a.attname, format_type(a.atttypid, a.atttypmod), coalesce(a.attnum = ANY (i.indkey), false)
          FROM pg_class c
          JOIN pg_namespace n ON n.oid = c.relnamespace
          JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
          LEFT JOIN pg_index i ON i.indrelid = c.oid AND i.indisprimary
         WHERE n.nspname = %s AND c.relkind = 'r'
         ORDER BY c.relname, a.attnum""", (schema,))
    tables: dict[str, tuple[list[tuple[str, str]], list[str]]] = {}
    for table, column, data_type, is_key in cur.fetchall():
        columns, key = tables.setdefault(table, ([], []))
        if column not in DELIVERY_COLUMNS:
            columns.append((column, data_type))
            if is_key:
                key.append(column)
    return tables


def find_deliveries(database: str) -> PokeReturnValue:
    """Done when at least one of the estate's subscriptions has rows waiting to be applied."""
    conn = PostgresHook(postgres_conn_id=STAGING_CONN_ID).get_conn()
    waiting = []
    try:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION READ ONLY")
            for sub in subscriptions_for(database):
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (sub.schema,))
                tables = [r[0] for r in cur.fetchall()]
                if not tables:
                    log.warning("%s has an apply script but no schema in %s", sub.schema, STAGING_CONN_ID)
                    continue
                cur.execute(" UNION ALL ".join(
                    f'SELECT 1 FROM "{sub.schema}"."{t}" WHERE processing_status = \'delivered\'' for t in tables)
                    + " LIMIT 1")
                if cur.fetchone():
                    waiting.append(sub.full_task_id)
    finally:
        conn.rollback()
        conn.close()
    if waiting:
        log.info("%d subscription(s) have deliveries waiting: %s", len(waiting), ", ".join(waiting))
    return PokeReturnValue(is_done=bool(waiting), xcom_value=waiting)


def choose_subscriptions(ti) -> list[str]:
    return ti.xcom_pull(task_ids="wait_for_deliveries") or []


def apply_subscription(staging, destination, sub: Subscription) -> dict[str, int]:
    """
    Apply the rows waiting in one subscription to the destination system and mark them in subscription_staging.

    staging and destination are connections to subscription_staging and to the system's database.  Returns the
    number of rows applied, discarded and failed.
    """
    # 1. The rows waiting, with the delivery each came from.
    with staging.cursor() as cur:
        tables = staging_tables(cur, sub.schema)
        waiting = {}
        for table, (columns, key) in tables.items():
            names = ", ".join(f'"{c}"' for c, _ in columns)
            cur.execute(f'SELECT {names}, delivery_timestamp FROM "{sub.schema}"."{table}" '
                        "WHERE processing_status = 'delivered'")
            waiting[table] = cur.fetchall()
    staging.rollback()
    if not any(waiting.values()):
        return {"applied": 0, "discarded": 0, "failed": 0}

    # 2. Apply them in the destination system, in one transaction.
    outcome: dict[str, list[tuple]] = {}
    error = None
    try:
        with destination.cursor() as cur:
            for table, (columns, key) in tables.items():
                cur.execute(f'CREATE TEMPORARY TABLE "incoming_{table}" ('
                            + ", ".join(f'"{c}" {t}' for c, t in columns)
                            + ", discard_reason text) ON COMMIT DROP")
                rows = [r[:-1] for r in waiting[table]]
                if rows:
                    cur.executemany(f'INSERT INTO "incoming_{table}" ({", ".join(chr(34) + c + chr(34) for c, _ in columns)}) '
                                    f'VALUES ({", ".join(["%s"] * len(columns))})', rows)
            cur.execute(sub.sql)
            for table, (columns, key) in tables.items():
                cur.execute(f'SELECT {", ".join(chr(34) + c + chr(34) for c in key)}, discard_reason '
                            f'FROM "incoming_{table}"')
                outcome[table] = cur.fetchall()
        destination.commit()
    except Exception as e:
        destination.rollback()
        error = f"{type(e).__name__}: {e}".strip()[:2000]
        log.error("Applying %s to %s.%s failed: %s", sub.schema, sub.database, sub.system, error)

    # 3. Mark each row: processed (applied or discarded) or failed.  The delivery_timestamp test leaves a row
    #    that was delivered again in the meantime waiting for the next run.
    counts = {"applied": 0, "discarded": 0, "failed": 0}
    with staging.cursor() as cur:
        for table, (columns, key) in tables.items():
            index = {c: i for i, (c, _) in enumerate(columns)}
            where = " AND ".join(f'"{k}" = %s' for k in key) + " AND delivery_timestamp = %s"
            if error:
                for row in waiting[table]:
                    cur.execute(f'UPDATE "{sub.schema}"."{table}" SET processing_status = \'failed\', '
                                f'processing_timestamp = now(), processing_message = %s WHERE {where}',
                                [error] + [row[index[k]] for k in key] + [row[-1]])
                    counts["failed"] += 1
                continue
            delivered_at = {tuple(row[index[k]] for k in key): row[-1] for row in waiting[table]}
            for result in outcome[table]:
                pk, reason = tuple(result[:-1]), result[-1]
                cur.execute(f'UPDATE "{sub.schema}"."{table}" SET processing_status = \'processed\', '
                            f'processing_timestamp = now(), processing_message = %s WHERE {where}',
                            [reason or "applied"] + list(pk) + [delivered_at.pop(pk, None)])
                counts["discarded" if reason else "applied"] += 1
            # An apply script must leave every incoming row in place; any it removed are marked failed rather
            # than left waiting for ever.
            for pk, at in delivered_at.items():
                cur.execute(f'UPDATE "{sub.schema}"."{table}" SET processing_status = \'failed\', '
                            f'processing_timestamp = now(), processing_message = %s WHERE {where}',
                            ["removed from incoming_" + table + " by the apply script"] + list(pk) + [at])
                counts["failed"] += 1
    staging.commit()
    if error or counts["failed"]:
        raise RuntimeError(f"{sub.schema}: {counts['failed']} row(s) failed: "
                           + (error or "the apply script removed rows from its incoming tables"))
    return counts


def apply(script_path: str) -> None:
    sub = Subscription(Path(script_path))
    staging = PostgresHook(postgres_conn_id=STAGING_CONN_ID).get_conn()
    destination = PostgresHook(postgres_conn_id=sub.database).get_conn()
    try:
        counts = apply_subscription(staging, destination, sub)
    finally:
        staging.close()
        destination.close()
    log.info("%s: %d row(s) applied to %s.%s, %d discarded", sub.schema, counts["applied"], sub.database,
             sub.system, counts["discarded"])


def build_dag(database: str, estate: str) -> DAG:
    subscriptions = subscriptions_for(database)
    systems = sorted({s.system for s in subscriptions})
    with DAG(
        dag_id=f"coco_subscriptions_{database}",
        description=f"Applies the digital product data delivered to the {estate} systems in {database}.",
        doc_md=__doc__,
        schedule="@continuous",
        max_active_runs=1,
        start_date=datetime(2026, 10, 1),
        catchup=False,
        is_paused_upon_creation=False,
        tags=["coco", "digital-product-subscription", estate],
    ) as dag:
        wait = PythonSensor(
            task_id="wait_for_deliveries",
            python_callable=find_deliveries,
            op_kwargs={"database": database},
            mode="reschedule",
            poke_interval=POKE_INTERVAL.total_seconds(),
            timeout=SENSOR_TIMEOUT.total_seconds(),
            soft_fail=True,
            doc_md="Waits until at least one of the estate's subscriptions has delivered rows waiting.",
        )
        branch = BranchPythonOperator(task_id="choose_subscriptions", python_callable=choose_subscriptions)
        wait >> branch
        for system in systems:
            with TaskGroup(group_id=system, tooltip=f"Applies to {system}"):
                for sub in (s for s in subscriptions if s.system == system):
                    branch >> PythonOperator(
                        task_id=sub.task_id,
                        python_callable=apply,
                        op_kwargs={"script_path": str(sub.path)},
                        inlets=[asset(STAGING_CONN_ID, sub.schema, t) for t in sub.source_tables],
                        outlets=[asset(database, system, t) for t in sub.target_tables],
                        doc_md=f"Applies the subscription `{sub.schema}` to `{database}.{system}` using "
                               f"`{sub.path.relative_to(LOADS_DIR)}`.",
                    )
    return dag


for _database, (_estate, _prefix) in ESTATES.items():
    globals()[f"coco_subscriptions_{_database}"] = build_dag(_database, _estate)
