# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Coco Pharmaceuticals digital product feeds.

Fills the strategic digital products' tables in the Data Sharing Hub database, coco_data_hub, from the systems
that supply them, as soon as the systems' data changes.  There is one DAG per system estate, each reading that
estate's database:

    coco_feed_coco_pharma         the Coco Pharmaceuticals systems (coco_pharma)
    coco_feed_austin_systems      the acquired Austin site's systems (austin_systems)
    coco_feed_bucharest_systems   the acquired EKG Pharmaceuticals systems (bucharest_systems)

The work is defined by the extract queries in coco-system-extracts/<database>/<system schema>/
<product schema>.<product table>.sql.  Each extract reads one system's tables and returns exactly the columns of one
product table, so the extract is where the system's native data is transformed into the product's form.  Each
extract becomes one load task, in a task group named after its system.

Each DAG runs continuously:

1. wait_for_changes - a sensor that fingerprints every extract's result (an md5 of its rows) about once a minute
   and finishes as soon as any fingerprint differs from the one recorded when that extract last loaded.  It waits
   in reschedule mode, so it holds no worker slot between checks.  On the first run nothing has been recorded, so
   every extract loads.
2. choose_loads - runs the load tasks of the changed extracts only; the rest are skipped.
3. <system>.load__<product schema>__<product table> - reads the extract and its fingerprint in one consistent
   snapshot of the system's database, upserts the rows into the product table on its primary key, then records
   the fingerprint, so a failed load is retried on the next run.

Rows are upserted, never deleted: several systems can feed the same product table, and a load cannot tell
whether a row it no longer returns came from it.  Each load task declares the system tables it reads and the
product table it writes as Airflow assets, so OpenLineage reports table-level lineage and later DAGs can be
scheduled on a product table being updated.

Connections (set as AIRFLOW_CONN_* in airflow-marquez.yaml): one per system database, named after the database,
and coco_data_hub for the hub.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

from airflow.exceptions import AirflowSkipException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.standard.sensors.python import PythonSensor
from airflow.sdk import DAG, Asset, PokeReturnValue, TaskGroup, Variable

log = logging.getLogger(__name__)

EXTRACTS_DIR = Path(__file__).parent / "coco-system-extracts"
HUB_CONN_ID = "coco_data_hub"
ESTATES = {
    "coco_pharma": "Coco core",
    "austin_systems": "Austin",
    "bucharest_systems": "Bucharest",
}
# Where the databases live, as the Airflow containers see them - used only to name the assets.
POSTGRES_AUTHORITY = "host.docker.internal:5442"
POKE_INTERVAL = timedelta(seconds=60)
SENSOR_TIMEOUT = timedelta(hours=12)


def asset(database: str, schema: str, table: str) -> Asset:
    return Asset(name=f"{database}.{schema}.{table}",
                 uri=f"postgres://{POSTGRES_AUTHORITY}/{database}/{schema}/{table}")


class Extract:
    """One extract query: a system's data shaped as one product table."""

    def __init__(self, path: Path):
        self.path = path
        self.database = path.parent.parent.name
        self.system = path.parent.name
        self.product_schema, _, self.product_table = path.stem.partition(".")
        self.sql = path.read_text().strip().rstrip(";")
        header = re.search(r"^-- Source: .*\((.+)\)\s*$", self.sql, re.M)
        self.system_qualified_name = header.group(1) if header else self.system
        self.source_tables = sorted(set(re.findall(rf"\b{re.escape(self.system)}\.([a-z0-9_]+)\b", self.sql)))
        self.key = f"{self.database}.{self.system}.{self.product_schema}.{self.product_table}"
        self.task_id = f"load__{self.product_schema}__{self.product_table}"
        self.full_task_id = f"{self.system}.{self.task_id}"

    @property
    def variable(self) -> str:
        return f"coco_feed_fingerprint::{self.key}"

    def fingerprint_sql(self) -> str:
        # The newline before the closing bracket keeps a trailing comment in the extract from swallowing it.
        return f"SELECT md5(coalesce(string_agg(x::text, E'\\n' ORDER BY x::text), '')) FROM ({self.sql}\n) x"


def extracts_for(database: str) -> list[Extract]:
    return [Extract(p) for p in sorted((EXTRACTS_DIR / database).glob("*/*.sql"))]


def find_changes(database: str) -> PokeReturnValue:
    """Fingerprint every extract of the estate; done when at least one has changed since it last loaded."""
    conn = PostgresHook(postgres_conn_id=database).get_conn()
    changed = []
    try:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION READ ONLY")
            for extract in extracts_for(database):
                cur.execute(extract.fingerprint_sql())
                if cur.fetchone()[0] != Variable.get(extract.variable, default=None):
                    changed.append(extract.full_task_id)
        conn.rollback()
    finally:
        conn.close()
    if changed:
        log.info("%d extract(s) changed: %s", len(changed), ", ".join(changed))
    return PokeReturnValue(is_done=bool(changed), xcom_value=changed)


def choose_loads(ti) -> list[str]:
    return ti.xcom_pull(task_ids="wait_for_changes") or []


_table_cache: dict[str, tuple[list[str], list[str]]] = {}


def product_columns(cur, schema: str, table: str) -> tuple[list[str], list[str]]:
    """The product table's columns, in order, and its primary key columns."""
    name = f"{schema}.{table}"
    if name not in _table_cache:
        cur.execute("""
            SELECT a.attname, coalesce(a.attnum = ANY (i.indkey), false)
              FROM pg_attribute a
              LEFT JOIN pg_index i ON i.indrelid = a.attrelid AND i.indisprimary
             WHERE a.attrelid = %s::regclass AND a.attnum > 0 AND NOT a.attisdropped
             ORDER BY a.attnum""", (name,))
        rows = cur.fetchall()
        if not rows:
            raise ValueError(f"product table {name} not found in {HUB_CONN_ID}")
        _table_cache[name] = ([r[0] for r in rows], [r[0] for r in rows if r[1]])
    return _table_cache[name]


def read_extract(source, extract: Extract) -> tuple[str, list[str], list[tuple]]:
    """Run an extract on a connection to its system's database: its fingerprint, column names and rows."""
    try:
        with source.cursor() as cur:
            # One snapshot for both queries, so the fingerprint recorded is the fingerprint of the rows copied.
            cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            cur.execute(extract.fingerprint_sql())
            fingerprint = cur.fetchone()[0]
            cur.execute(extract.sql)
            names = [d[0] for d in cur.description]
            rows = cur.fetchall()
    finally:
        source.rollback()
    return fingerprint, names, rows


def upsert_rows(hub, schema: str, table: str, names: list[str], rows: list[tuple]) -> None:
    """Upsert rows into a product table on its primary key, in one transaction on a connection to coco_data_hub."""
    try:
        with hub.cursor() as cur:
            columns, key = product_columns(cur, schema, table)
            if names != columns:
                raise ValueError(f"{schema}.{table}: the extract returns {names}, but the product table has {columns}")
            target = f'"{schema}"."{table}"'
            column_list = ", ".join(f'"{c}"' for c in columns)
            updates = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in columns if c not in key)
            on_conflict = (f"ON CONFLICT ({', '.join(chr(34) + c + chr(34) for c in key)}) "
                           + (f"DO UPDATE SET {updates}" if updates else "DO NOTHING"))
            placeholders = ", ".join(["%s"] * len(columns))
            cur.executemany(f"INSERT INTO {target} ({column_list}) VALUES ({placeholders}) {on_conflict}", rows)
        hub.commit()
    except Exception:
        hub.rollback()
        raise


def load(extract_path: str) -> None:
    """Copy one extract's rows into its product table and record the fingerprint of what was copied."""
    extract = Extract(Path(extract_path))
    source = PostgresHook(postgres_conn_id=extract.database).get_conn()
    try:
        fingerprint, names, rows = read_extract(source, extract)
    finally:
        source.close()

    if fingerprint == Variable.get(extract.variable, default=None):
        raise AirflowSkipException(f"{extract.key} has not changed since it was last loaded")

    hub = PostgresHook(postgres_conn_id=HUB_CONN_ID).get_conn()
    try:
        upsert_rows(hub, extract.product_schema, extract.product_table, names, rows)
    finally:
        hub.close()

    Variable.set(extract.variable, fingerprint)
    log.info("Loaded %d row(s) from %s.%s into %s.%s", len(rows), extract.database, extract.system,
             extract.product_schema, extract.product_table)


def build_dag(database: str, estate: str) -> DAG:
    extracts = extracts_for(database)
    systems = sorted({e.system for e in extracts})
    with DAG(
        dag_id=f"coco_feed_{database}",
        description=f"Feeds the Coco Data Sharing Hub's digital products from the {estate} systems in {database}.",
        doc_md=__doc__,
        schedule="@continuous",
        max_active_runs=1,
        start_date=datetime(2026, 10, 1),
        catchup=False,
        is_paused_upon_creation=False,
        tags=["coco", "digital-product-feed", estate],
        default_args={"retries": 2, "retry_delay": timedelta(minutes=1)},
    ) as dag:
        wait = PythonSensor(
            task_id="wait_for_changes",
            python_callable=find_changes,
            op_kwargs={"database": database},
            mode="reschedule",
            poke_interval=POKE_INTERVAL.total_seconds(),
            timeout=SENSOR_TIMEOUT.total_seconds(),
            soft_fail=True,
            doc_md="Waits until the data behind at least one extract has changed since it was last loaded.",
        )
        branch = BranchPythonOperator(task_id="choose_loads", python_callable=choose_loads)
        wait >> branch
        for system in systems:
            with TaskGroup(group_id=system, tooltip=f"Loads from {system}"):
                for extract in (e for e in extracts if e.system == system):
                    branch >> PythonOperator(
                        task_id=extract.task_id,
                        python_callable=load,
                        op_kwargs={"extract_path": str(extract.path)},
                        inlets=[asset(database, system, t) for t in extract.source_tables],
                        outlets=[asset(HUB_CONN_ID, extract.product_schema, extract.product_table)],
                        doc_md=f"Copies `{system}` ({extract.system_qualified_name}) into "
                               f"`coco_data_hub.{extract.product_schema}.{extract.product_table}` "
                               f"using `{extract.path.relative_to(EXTRACTS_DIR)}`.",
                    )
    return dag


for _database, _estate in ESTATES.items():
    globals()[f"coco_feed_{_database}"] = build_dag(_database, _estate)
