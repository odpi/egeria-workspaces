# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
"""Compare TestGen's profile, generated tests and results with Resource Explorer's, per column.

Inputs:
  * the JSON from scripts/export_testgen.py (TestGen's side), and
  * Resource Explorer's registry (RE's side), by SQLAlchemy URL: the latest batch per database of
    database_value_profiles, database_quality_proposals and database_quality_results. Those tables
    are RE's quality slice 1 (trellis branch re/value-profile-quality-checks, not yet merged), so
    their names can still move.

    uv run --no-project --with sqlalchemy --with "psycopg[binary]" compare/compare_re_testgen.py \
        --export out/testgen-export.json \
        --re-registry "postgresql+psycopg://egeria_advisor:...@localhost:5442/egeria_advisor?options=-csearch_path%3Dresource_explorer" \
        --out out/compare

Writes <out>/report.md, profile.csv, checks.csv and results.csv. Read-only on both sides.

Absence stays distinct from agreement: a column one side did not profile, a check one side never
proposed, and a check that has no result are reported as such, never as a match or a zero.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter

from sqlalchemy import create_engine, inspect, text

# RE quality slice 1's test types (Recency moved to slice 2). TestGen generates many more; only
# these are comparable until RE's catalogue grows.
SLICE1_TYPES = ("Missing_Pct", "Required", "Required_No_Placeholder", "Unique", "Future_Date", "Min_Date", "Row_Ct_Pct")
MEASURES = ("general_type", "record_ct", "value_ct", "distinct_value_ct", "null_value_ct", "zero_length_ct",
            "filled_value_ct", "min_date", "max_date", "future_date_ct")
# TestGen's result_status words, folded onto RE's result vocabulary for the agreement column.
TG_STATUS = {"Passed": "pass", "Failed": "fail", "Warning": "warning", "Error": "error", "Log": "logged"}


def latest_batch(conn, table: str, slug: str) -> list[dict]:
    """Rows of the newest surveyed_at batch for one database; [] when RE has none."""
    newest = conn.execute(
        text(f"SELECT MAX(surveyed_at) FROM {table} WHERE database_slug = :slug"), {"slug": slug}
    ).scalar()
    if newest is None:
        return []
    result = conn.execute(
        text(f"SELECT * FROM {table} WHERE database_slug = :slug AND surveyed_at = :at"),
        {"slug": slug, "at": newest},
    )
    return [dict(r._mapping) for r in result]


def same(a, b) -> bool:
    if a is None or b is None:
        return False
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return float(a) == float(b)
    # Dates arrive as ISO text from both sides, with or without a time part.
    return str(a).replace("T", " ")[:19] == str(b).replace("T", " ")[:19]


def compare_profile(slug: str, tg_profile: list[dict], re_profile: list[dict]) -> list[dict]:
    key = lambda r: (r["schema_name"], r["table_name"], r["column_name"])  # noqa: E731
    tg = {key(r): r for r in tg_profile}
    re_ = {key(r): r for r in re_profile}
    out = []
    for k in sorted(set(tg) | set(re_)):
        t, r = tg.get(k), re_.get(k)
        row = {"database": slug, "schema": k[0], "table": k[1], "column": k[2]}
        if t is None:
            row["coverage"] = "re_only"
        elif r is None:
            row["coverage"] = "testgen_only"
        elif r.get("state") not in (None, "measured"):
            row["coverage"] = f"re_{r['state']}"
        else:
            row["coverage"] = "both"
        differing = []
        for m in MEASURES:
            tv, rv = (t or {}).get(m), (r or {}).get(m)
            row[f"tg_{m}"], row[f"re_{m}"] = tv, rv
            if row["coverage"] == "both" and (tv is not None or rv is not None) and not same(tv, rv):
                differing.append(m)
        row["differs"] = ",".join(differing)
        out.append(row)
    return out


def compare_checks(slug: str, tg_tests: list[dict], re_proposals: list[dict], types: tuple[str, ...]) -> list[dict]:
    tg = {t["check_key"]: t for t in tg_tests if t["test_type"] in types}
    re_ = {p["check_key"]: p for p in re_proposals if p["test_type"] in types}
    out = []
    for k in sorted(set(tg) | set(re_)):
        t, p = tg.get(k), re_.get(k)
        params = {}
        if p and p.get("params_json"):
            try:
                params = json.loads(p["params_json"]) if isinstance(p["params_json"], str) else dict(p["params_json"])
            except ValueError:
                params = {"unparsed": p["params_json"]}
        out.append({
            "database": slug,
            "check_key": k,
            "test_type": (t or p)["test_type"],
            "coverage": "both" if t and p else ("testgen_only" if t else "re_only"),
            "re_state": p.get("state") if p else None,
            "re_reason": p.get("reason") if p else None,
            "tg_active": t.get("test_active") if t else None,
            "tg_severity": t.get("severity") if t else None,
            "tg_threshold_value": t.get("threshold_value") if t else None,
            "tg_baseline_value": t.get("baseline_value") if t else None,
            "tg_baseline_ct": t.get("baseline_ct") if t else None,
            "re_params": json.dumps(params, sort_keys=True) if p else None,
        })
    return out


def compare_results(slug: str, tg_tests: list[dict], re_results: list[dict], types: tuple[str, ...]) -> list[dict]:
    tg = {t["check_key"]: t for t in tg_tests if t["test_type"] in types}
    re_ = {r["check_key"]: r for r in re_results if r["test_type"] in types}
    out = []
    for k in sorted(set(tg) | set(re_)):
        t, r = tg.get(k), re_.get(k)
        tg_result = (t or {}).get("result")
        tg_status = TG_STATUS.get(tg_result["result_status"], tg_result["result_status"]) if tg_result else None
        re_status = r.get("status") if r else None
        if tg_status is None or re_status is None:
            agreement = "not_comparable"
        else:
            agreement = "agree" if tg_status == re_status else "disagree"
        out.append({
            "database": slug,
            "check_key": k,
            "test_type": (t or r)["test_type"],
            "tg_status": tg_status if t else "no_test",
            "tg_measure": tg_result.get("result_measure") if tg_result else None,
            "tg_threshold": tg_result.get("threshold_value") if tg_result else None,
            "re_status": re_status if r else "no_result",
            "re_measure": r.get("measure") if r else None,
            "re_threshold": r.get("threshold_values_json") if r else None,
            "re_reason": r.get("reason") if r else None,
            "agreement": agreement,
        })
    return out


def write_csv(path: str, rows: list[dict]) -> None:
    with open(path, "w", newline="") as f:
        if not rows:
            f.write("")
            return
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarise(title: str, rows: list[dict], field: str) -> list[str]:
    counts = Counter(r[field] for r in rows)
    lines = [f"### {title}", ""]
    if not rows:
        return lines + ["Nothing to compare.", ""]
    lines += [f"| {field} | rows |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    return lines + [""]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--export", required=True, help="JSON from scripts/export_testgen.py")
    parser.add_argument("--re-registry", required=True, help="SQLAlchemy URL of RE's registry")
    parser.add_argument("--out", default="out/compare")
    parser.add_argument("--types", nargs="*", default=list(SLICE1_TYPES), help="Test types to compare")
    args = parser.parse_args()
    types = tuple(args.types)

    with open(args.export) as f:
        export = json.load(f)
    engine = create_engine(args.re_registry)
    os.makedirs(args.out, exist_ok=True)

    profile_rows, check_rows, result_rows = [], [], []
    report = [
        "# Resource Explorer vs TestGen",
        "",
        f"TestGen export: {export.get('exported_at')} (TestGen {export.get('testgen_version')}). "
        f"Test types compared: {', '.join(types)}.",
        "",
    ]
    with engine.connect() as conn:
        present = set(inspect(conn).get_table_names())
        needed = {"database_value_profiles", "database_quality_proposals", "database_quality_results"}
        if missing := sorted(needed - present):
            report += [f"**RE registry has no {', '.join(missing)}**: RE quality slice 1 is not deployed "
                       "there, so RE's side of those comparisons reads as absent, not empty.", ""]
        for project in export["projects"]:
            slug = project["re_slug"]
            tg_profile = [c for g in project["table_groups"] for c in g["profile"]]
            tg_tests = [t for g in project["table_groups"] for t in g["tests"]]
            states = Counter(g["profile_state"] for g in project["table_groups"])
            report.append(f"## {project['project_code']} → RE `{slug}`")
            report.append("")
            report.append(f"TestGen: {project['state']}; table groups {dict(states) or 'none'}; "
                          f"{len(tg_profile)} profiled columns, {len(tg_tests)} tests.")
            re_profile = latest_batch(conn, "database_value_profiles", slug) if "database_value_profiles" in present else []
            re_props = latest_batch(conn, "database_quality_proposals", slug) if "database_quality_proposals" in present else []
            re_results = latest_batch(conn, "database_quality_results", slug) if "database_quality_results" in present else []
            report.append(f"RE: {len(re_profile)} value-profile rows, {len(re_props)} proposals, "
                          f"{len(re_results)} results in the latest batches.")
            report.append("")
            p = compare_profile(slug, tg_profile, re_profile)
            c = compare_checks(slug, tg_tests, re_props, types)
            r = compare_results(slug, tg_tests, re_results, types)
            differing = sum(1 for row in p if row["differs"])
            report += summarise("Profile coverage", p, "coverage")
            report += [f"Columns profiled by both whose measures differ: {differing}.", ""]
            report += summarise("Proposed (RE) vs generated (TestGen)", c, "coverage")
            report += summarise("Results", r, "agreement")
            profile_rows += p
            check_rows += c
            result_rows += r

    write_csv(os.path.join(args.out, "profile.csv"), profile_rows)
    write_csv(os.path.join(args.out, "checks.csv"), check_rows)
    write_csv(os.path.join(args.out, "results.csv"), result_rows)
    with open(os.path.join(args.out, "report.md"), "w") as f:
        f.write("\n".join(report) + "\n")
    print(f"Wrote {args.out}/report.md, profile.csv, checks.csv, results.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
