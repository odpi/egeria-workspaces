# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
"""Create the example TestGen projects in examples.yaml, then profile, generate and test them.

Runs INSIDE the TestGen engine container, with TestGen's own interpreter, so projects and
connections go through TestGen's models: the connection password is encrypted with the
container's TG_DECRYPT_* secrets, exactly as the UI would store it. The open-source UI cannot
create a project and shows only a project's first connection, so this is the only supported way
to get several databases into one TestGen instance short of hand-written SQL.

    docker compose --env-file .env exec engine python /examples/scripts/seed_examples.py
        [--config /examples/examples.yaml] [--project CODE ...] [--setup-only] [--skip-tests]

Re-runnable: an existing project, connection, membership, table group or suite is reused and left
unchanged, so a second run only adds what is new (for example a schema created since) and then
re-profiles and re-tests. The run steps use TestGen's CLI, which queues each job for the
scheduler in this container and waits for it.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

import psycopg2
import yaml

from testgen import settings
from testgen.common.database.table_group_service import apply_table_group_flavor_rules
from testgen.common.models import database_session
from testgen.common.models.connection import Connection
from testgen.common.models.project import Project
from testgen.common.models.project_membership import ProjectMembership
from testgen.common.models.table_group import TableGroup, table_group_defaults
from testgen.common.models.test_suite import TestSuite
from testgen.common.models.user import User

# TESTGEN_BIN overrides the `testgen` found on PATH, for an unusual install.
TESTGEN = os.environ.get("TESTGEN_BIN") or shutil.which("testgen") or "/dk/bin/testgen"
SYSTEM_SCHEMAS = {"information_schema", "pg_catalog", "pg_toast"}
# TestGen 5.134.0 stores schema names in VARCHAR(50) columns (profiling_runs, test_results and
# others), so a table group on a longer schema name is created but every profiling run of it fails.
# Such schemas are reported and skipped instead.
TESTGEN_SCHEMA_NAME_MAX = 50


def load_config(path: str) -> tuple[dict, list[dict]]:
    with open(path) as f:
        doc = yaml.safe_load(f) or {}
    return doc.get("defaults") or {}, doc.get("projects") or []


def target_credentials() -> tuple[str, str]:
    user = os.environ.get("TESTGEN_TARGET_DB_USER", "surveyor")
    password = os.environ.get("TESTGEN_TARGET_DB_PASSWORD")
    if not password:
        sys.exit("TESTGEN_TARGET_DB_PASSWORD is not set in the container's environment (.env).")
    return user, password


def discover_schemas(spec: dict, user: str, password: str) -> list[str]:
    """Schemas the connection account can see in the target database, filtered by the spec."""
    with psycopg2.connect(
        host=spec["host"], port=spec["port"], dbname=spec["database"], user=user, password=password,
        connect_timeout=15,
    ) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT nspname FROM pg_namespace WHERE has_schema_privilege(nspname, 'USAGE') ORDER BY nspname"
        )
        found = [row[0] for row in cur.fetchall()]
    found = [s for s in found if s not in SYSTEM_SCHEMAS and not s.startswith("pg_")]
    if spec.get("schemas"):
        allowed = set(spec["schemas"])
        missing = sorted(allowed - set(found))
        if missing:
            print(f"  ! listed but not visible to {user}: {', '.join(missing)}")
        found = [s for s in found if s in allowed]
    excluded = set(spec.get("exclude_schemas") or [])
    return [s for s in found if s not in excluded]


def ensure_project(spec: dict) -> None:
    code = spec["project_code"]
    if Project.get(code) is None:
        Project(project_code=code, project_name=spec.get("name") or code).save()
        print(f"  + project {code}")
    # Membership is what puts a project in a user's project switcher, the global admin's included.
    user = User.get(settings.USERNAME)
    if user is None:
        print(f"  ! UI user {settings.USERNAME!r} not found; the project will not show in the UI")
        return
    if not any(m.project_code == code for m in ProjectMembership.get_memberships_for_user(user.id)):
        ProjectMembership(user_id=user.id, project_code=code, role="admin").save()
        print(f"  + membership {settings.USERNAME} -> {code} (admin)")


def ensure_connection(spec: dict, user: str, password: str) -> Connection:
    code = spec["project_code"]
    existing = list(Connection.select_where(Connection.project_code == code))
    if len(existing) > 1:
        print(f"  ! {code} has {len(existing)} connections; the UI shows only the first")
    for conn in existing:
        if conn.project_db == spec["database"] and conn.project_host == spec["host"]:
            return conn
    conn = Connection(
        project_code=code,
        sql_flavor="postgresql",
        sql_flavor_code="postgresql",
        project_host=spec["host"],
        project_port=str(spec["port"]),
        project_user=user,
        project_db=spec["database"],
        connection_name=spec["database"],
        project_pw_encrypted=password,
        max_threads=4,
        max_query_chars=settings.PROJECT_CONNECTION_MAX_QUERY_CHAR,
    )
    conn.save()
    print(f"  + connection {spec['database']}@{spec['host']}:{spec['port']} as {user}")
    return conn


def ensure_table_group(spec: dict, conn: Connection, schema: str) -> tuple[str, str]:
    """(table_group_id, test_suite_id) for one schema, creating either as needed."""
    code = spec["project_code"]
    name = f"{spec['database']}.{schema}"
    group = next(iter(TableGroup.select_where(
        TableGroup.project_code == code, TableGroup.table_groups_name == name,
    )), None)
    if group is None:
        # Built the way TestGen's REST API creates one (api/table_groups.py).
        group = TableGroup(
            project_code=code,
            connection_id=conn.connection_id,
            table_groups_name=name,
            table_group_schema=schema,
            **table_group_defaults(),
        )
        apply_table_group_flavor_rules(group, conn)
        group.save(add_scorecard_definition=True)
        print(f"  + table group {name}")
    suite = TestSuite.get(group.default_test_suite_id) if group.default_test_suite_id else None
    if suite is None:
        # The same fields the UI's table-group wizard sets for a new Standard suite.
        suite = TestSuite(
            project_code=code,
            test_suite=f"{name} standard"[:200],
            connection_id=conn.connection_id,
            table_groups_id=group.id,
            export_to_observability=False,
            dq_score_exclude=False,
            monitor_lookback=0,
            predict_min_lookback=0,
        )
        suite.save()
        group.default_test_suite_id = suite.id
        group.save()
        print(f"  + test suite {suite.test_suite}")
    return str(group.id), str(suite.id)


def run(step: list[str]) -> bool:
    print(f"  $ testgen {' '.join(step)}", flush=True)
    result = subprocess.run([TESTGEN, *step], check=False)
    if result.returncode != 0:
        print(f"  ! exited {result.returncode}", flush=True)
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", default="/examples/examples.yaml")
    parser.add_argument("--project", action="append", help="Only this project code (repeatable).")
    parser.add_argument("--setup-only", action="store_true", help="Create the objects; run nothing.")
    parser.add_argument("--skip-tests", action="store_true", help="Profile and generate, but do not run tests.")
    args = parser.parse_args()

    defaults, projects = load_config(args.config)
    if args.project:
        wanted = set(args.project)
        projects = [p for p in projects if p["project_code"] in wanted]
    user, password = target_credentials()

    failures = 0
    for raw in projects:
        spec = {**defaults, **raw}
        print(f"\n== {spec['project_code']} ({spec['database']})")
        try:
            schemas = discover_schemas(spec, user, password)
        except psycopg2.Error as error:
            # Not "no schemas": the database was not reached, and the project is not seeded.
            print(f"  ! cannot read {spec['database']} as {user}: {str(error).strip()}")
            failures += 1
            continue
        too_long = [s for s in schemas if len(s) > TESTGEN_SCHEMA_NAME_MAX]
        for schema in too_long:
            print(f"  ! skipped {schema}: {len(schema)} characters, over TestGen's {TESTGEN_SCHEMA_NAME_MAX}")
        schemas = [s for s in schemas if len(s) <= TESTGEN_SCHEMA_NAME_MAX]
        if not schemas:
            print("  ! no schemas to profile after filtering; nothing seeded for this project")
            continue
        with database_session():
            ensure_project(spec)
            conn = ensure_connection(spec, user, password)
            pairs = [ensure_table_group(spec, conn, schema) for schema in schemas]
        if args.setup_only:
            continue
        for group_id, suite_id in pairs:
            if not run(["run-profile", "-tg", group_id]):
                failures += 1
                continue
            if not run(["run-test-generation", "-t", suite_id]):
                failures += 1
                continue
            if not args.skip_tests and not run(["run-tests", "-t", suite_id]):
                failures += 1

    print(f"\nDone, {failures} failed step(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
