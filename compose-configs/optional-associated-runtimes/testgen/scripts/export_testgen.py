# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
"""Export the example projects' latest TestGen profile, tests and results as one JSON document.

Runs INSIDE the TestGen engine container and writes to stdout, so the host keeps the file
(the container's user cannot write to a host bind mount on Linux):

    docker compose --env-file .env exec -T engine /dk/bin/python /examples/scripts/export_testgen.py \
        > out/testgen-export.json

The document is neutral, so compare/ needs neither TestGen nor its database: per table group,
the latest complete profile run's measures under TestGen's own `profile_results` column names
(the names Resource Explorer's value profile also uses), the suite's current test definitions,
and the result of each in the suite's latest complete test run. Every test also carries
`check_key`, built the way RE builds it, `schema.table[.column]::Test_Type`.

Absence is explicit, never an empty list that could read as "nothing found":
`profile_state` / `tests_state` are `exported`, `never_profiled`, `never_generated` or
`never_run`, and a test with no result in the latest run has `result: null`.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, date, datetime
from decimal import Decimal
from importlib.metadata import PackageNotFoundError, version
from uuid import UUID

import yaml
from sqlalchemy import text

from testgen import settings
from testgen.common.models import database_session, get_current_session
from testgen.common.models.suite_version import SuiteVersion

PROFILE_COLUMNS = (
    "schema_name", "table_name", "column_name", "general_type", "record_ct", "value_ct",
    "distinct_value_ct", "null_value_ct", "zero_length_ct", "filled_value_ct", "min_date",
    "max_date", "future_date_ct", "sample_ratio",
)
DEFINITION_COLUMNS = (
    "test_type", "schema_name", "table_name", "column_name", "severity", "test_active",
    "lock_refresh", "last_auto_gen_date", "profiling_as_of_date", "baseline_ct",
    "baseline_unique_ct", "baseline_value", "baseline_value_ct", "baseline_sum", "baseline_avg",
    "baseline_sd", "threshold_value", "lower_tolerance", "upper_tolerance", "subset_condition",
)
RESULT_COLUMNS = (
    "result_code", "result_status", "result_measure", "threshold_value", "result_message", "test_time",
)


def plain(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, UUID):
        return str(value)
    return value


def rows(sql: str, **params) -> list[dict]:
    result = get_current_session().execute(text(sql), params)
    return [{k: plain(v) for k, v in r._mapping.items()} for r in result]


def installed_version() -> str | None:
    """The image sets TESTGEN_VERSION; a pip-installed TestGen only has its package metadata."""
    try:
        return version("dataops-testgen")
    except PackageNotFoundError:
        return None


def check_key(schema: str, table: str, column: str | None, test_type: str) -> str:
    """Resource Explorer's key (surveyors/database/quality/catalogue.py::check_key)."""
    path = f"{schema}.{table}.{column}" if column else f"{schema}.{table}"
    return f"{path}::{test_type}"


def export_table_group(group: dict) -> dict:
    out = {
        "table_group": group["table_groups_name"],
        "schema": group["table_group_schema"],
        "profile_run_id": group["last_complete_profile_run_id"],
        "profiled_at": None,
        "profile_state": "never_profiled",
        "profile": [],
        "test_suite": None,
        "test_run_id": None,
        "tested_at": None,
        "tests_state": "never_generated",
        "tests": [],
    }
    if group["last_complete_profile_run_id"]:
        run = rows("SELECT profiling_starttime FROM profiling_runs WHERE id = :id",
                   id=group["last_complete_profile_run_id"])
        out["profiled_at"] = run[0]["profiling_starttime"] if run else None
        out["profile"] = rows(
            f"SELECT {', '.join(PROFILE_COLUMNS)} FROM profile_results WHERE profile_run_id = :id "
            "ORDER BY schema_name, table_name, column_name",
            id=group["last_complete_profile_run_id"],
        )
        out["profile_state"] = "exported"

    if not group["default_test_suite_id"]:
        return out
    suite = rows("SELECT id, test_suite, last_complete_test_run_id FROM test_suites WHERE id = :id",
                 id=group["default_test_suite_id"])[0]
    out["test_suite"] = suite["test_suite"]
    out["test_run_id"] = suite["last_complete_test_run_id"]
    # Only the suite's current version of each definition; a bare query on test_definitions
    # also returns superseded versions (see SuiteVersion.resolved_for_sql).
    definitions = rows(
        f"SELECT td.id, {', '.join('td.' + c for c in DEFINITION_COLUMNS)} FROM test_definitions td "
        f"WHERE td.test_suite_id = :suite AND td.version_id = {SuiteVersion.resolved_for_sql('td.test_suite_id')} "
        "ORDER BY td.schema_name, td.table_name, td.column_name, td.test_type",
        suite=suite["id"],
    )
    if not definitions:
        return out
    results: dict[str, dict] = {}
    if suite["last_complete_test_run_id"]:
        run = rows("SELECT test_starttime FROM test_runs WHERE id = :id", id=suite["last_complete_test_run_id"])
        out["tested_at"] = run[0]["test_starttime"] if run else None
        for r in rows(
            f"SELECT test_definition_id, {', '.join(RESULT_COLUMNS)} FROM test_results WHERE test_run_id = :run",
            run=suite["last_complete_test_run_id"],
        ):
            results[str(r.pop("test_definition_id"))] = r
    out["tests_state"] = "exported" if suite["last_complete_test_run_id"] else "never_run"
    for d in definitions:
        definition_id = d.pop("id")
        d["check_key"] = check_key(d["schema_name"], d["table_name"], d["column_name"], d["test_type"])
        d["result"] = results.get(definition_id)
        out["tests"].append(d)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", default="/examples/examples.yaml")
    args = parser.parse_args()
    with open(args.config) as f:
        doc = yaml.safe_load(f) or {}
    defaults = doc.get("defaults") or {}

    export = {
        "exported_at": datetime.now(UTC).isoformat(),
        "testgen_version": settings.VERSION or installed_version(),
        "projects": [],
    }
    with database_session():
        for raw in doc.get("projects") or []:
            spec = {**defaults, **raw}
            groups = rows(
                "SELECT tg.id, tg.table_groups_name, tg.table_group_schema, tg.last_complete_profile_run_id, "
                "tg.default_test_suite_id FROM table_groups tg JOIN connections c ON c.connection_id = tg.connection_id "
                "WHERE tg.project_code = :code AND c.project_db = :db ORDER BY tg.table_groups_name",
                code=spec["project_code"], db=spec["database"],
            )
            export["projects"].append({
                "project_code": spec["project_code"],
                "database": spec["database"],
                "re_slug": spec.get("re_slug") or spec["database"],
                "state": "exported" if groups else "not_seeded",
                "table_groups": [export_table_group(g) for g in groups],
            })
    json.dump(export, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
