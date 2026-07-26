#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Generate the "KPI tile registry" block of OVERVIEW_METRICS.md from the single
source of truth, overview_specs.py (NEXT-10, phase P0).

This kills the drift-bug class: the KPI catalog + provenance in the metrics doc
is derived from the same registry the backend serves at /api/overview/specs and
the frontend renders from, rather than being hand-synced.

Usage (run where pyegeria is importable — e.g. inside the quickstart-pyegeria-web
container: ``docker exec quickstart-pyegeria-web sh -c "cd /app && python3 gen_overview_metrics.py"``):

    python3 gen_overview_metrics.py            # rewrite the generated block in OVERVIEW_METRICS.md
    python3 gen_overview_metrics.py --check    # exit 1 if the block is out of date (CI/test guard)
    python3 gen_overview_metrics.py --stdout    # print the block, don't write

The block lives between the markers:
    <!-- BEGIN GENERATED: overview-kpi-catalog -->
    <!-- END GENERATED: overview-kpi-catalog -->
"""

from __future__ import annotations

import sys
from pathlib import Path

import overview_specs as specs

_HERE = Path(__file__).parent
_DOC = _HERE / "OVERVIEW_METRICS.md"
_BEGIN = "<!-- BEGIN GENERATED: overview-kpi-catalog -->"
_END = "<!-- END GENERATED: overview-kpi-catalog -->"

_PROV_LABEL = {"live": "🟢 live", "mixed": "🟡 mixed", "illustrative": "⚪ illustrative"}


def _ann(fs, key: str, default: str = "") -> str:
    vals = (fs.annotations or {}).get(key) or []
    return vals[0] if vals else default


def _primary_attr(fs):
    fmt = fs.formats[0]
    attrs = fmt.attributes if not isinstance(fmt, dict) else fmt.get("attributes", [])
    a = attrs[0]
    return (a.name, a.key, a.detail_spec) if not isinstance(a, dict) else (
        a.get("name"), a.get("key"), a.get("detail_spec"))


def build_block() -> str:
    lines = [_BEGIN]
    lines.append("")
    lines.append(
        "The Overview dashboard's KPI tiles are defined once in `overview_specs.py` as "
        "FormatSet-shaped specs (NEXT-10 P0) and served at `/api/overview/specs`. This "
        "table — provenance, drill targets, and the per-perspective selection — is "
        "generated from that registry, the single source of truth."
    )
    lines.append("")
    lines.append("| Tile | Metric | Prov. | Type | Source (endpoint → field) | Render | Drill → | Perspectives |")
    lines.append("|---|---|---|---|---|---|---|---|")

    prov_tally = {"live": 0, "mixed": 0, "illustrative": 0}
    compute_lines = []

    for key in specs.TILE_ORDER:
        fs = specs.SPECS[key]
        name, value_key, detail = _primary_attr(fs)
        prov = _ann(fs, "provenance", "live")
        prov_tally[prov] = prov_tally.get(prov, 0) + 1
        render = _ann(fs, "render_kind", "kpi")
        endpoint = _ann(fs, "endpoint")
        target = fs.target_type or "—"
        perspectives = ", ".join(specs.perspectives_for(key))
        lines.append(
            f"| `{key}` | {name} | {_PROV_LABEL.get(prov, prov)} | {target} | "
            f"{endpoint} → `{value_key}` | {render} | `{detail}` | {perspectives} |"
        )
        # Compute line from the spec's action.
        act = fs.action
        func = act.function if act is not None and not isinstance(act, dict) else (act or {}).get("function", "")
        sp = act.spec_params if act is not None and not isinstance(act, dict) else (act or {}).get("spec_params", {})
        sp_str = ", ".join(f"{k}={v}" for k, v in (sp or {}).items())
        compute_lines.append(f"- `{key}` — `{func}({sp_str})`")

    lines.append("")
    lines.append("**Compute** (each spec's `action` — the how-it's-computed / P3 report-runner hook):")
    lines.append("")
    lines.extend(compute_lines)
    lines.append("")
    lines.append(
        f"**Provenance tally:** {prov_tally.get('live', 0)} live · "
        f"{prov_tally.get('mixed', 0)} mixed · {prov_tally.get('illustrative', 0)} illustrative."
    )
    lines.append("")
    lines.append(_END)
    return "\n".join(lines)


def _splice(doc_text: str, block: str) -> str:
    if _BEGIN not in doc_text or _END not in doc_text:
        raise SystemExit(
            f"Markers not found in {_DOC.name}; add:\n{_BEGIN}\n{_END}\nwhere the block should go."
        )
    pre = doc_text.split(_BEGIN)[0]
    post = doc_text.split(_END, 1)[1]
    return pre + block + post


def main(argv) -> int:
    block = build_block()
    if "--stdout" in argv:
        print(block)
        return 0
    current = _DOC.read_text()
    updated = _splice(current, block)
    if "--check" in argv:
        if current != updated:
            sys.stderr.write(
                f"{_DOC.name} KPI registry block is OUT OF DATE. "
                f"Run: python3 {Path(__file__).name}\n"
            )
            return 1
        print(f"{_DOC.name} KPI registry block is up to date.")
        return 0
    if current != updated:
        _DOC.write_text(updated)
        print(f"Updated {_DOC.name} KPI registry block ({len(specs.SPECS)} tiles).")
    else:
        print(f"{_DOC.name} already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
