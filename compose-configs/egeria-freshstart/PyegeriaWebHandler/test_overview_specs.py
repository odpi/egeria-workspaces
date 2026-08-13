#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Drift guard for the Overview dashboard tile registry (NEXT-10 P0).

`overview_specs.py` is the single source of truth for the KPI tiles. This test
proves the registry is internally consistent AND that the frontend
(`egeria-overview.html` — the `METRICS` / `PERSP_KPIS` / `DRILL` maps) and the
generated metrics doc (`OVERVIEW_METRICS.md`) still agree with it. Any future
edit that changes one place without the others fails here — which is the whole
point of collapsing the six hand-synced places into one.

Run where pyegeria is importable (e.g. inside the container):
    docker exec freshstart-pyegeria-web sh -c "cd /app && python3 test_overview_specs.py"

Exit code is non-zero if any check FAILS.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import overview_specs as specs

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-overview.html"

_failures: list[str] = []
_checks = 0


def check(cond: bool, msg: str) -> None:
    global _checks
    _checks += 1
    if not cond:
        _failures.append(msg)


def _slice_object(text: str, start_marker: str) -> str:
    """Return the text from `start_marker` up to the first line that is just `};`."""
    i = text.index(start_marker)
    rest = text[i:]
    end = re.search(r"\n\};", rest)
    return rest[: end.end()] if end else rest


def parse_metrics(html: str) -> dict:
    """Parse the frontend METRICS map → {key: {label, ico, color, drill, hist}}."""
    block = _slice_object(html, "const METRICS = {")
    out = {}
    pat = re.compile(
        r"^\s*'?([\w-]+)'?:\s*\{\s*label:'([^']*)',\s*ico:'([^']*)',\s*color:'([^']*)',"
        r"\s*drill:'([^']*)'(?:,\s*hist:'([^']*)')?",
        re.MULTILINE,
    )
    for m in pat.finditer(block):
        key, label, ico, color, drill, hist = m.groups()
        out[key] = {"label": label, "ico": ico, "color": color, "drill": drill, "hist": hist}
    return out


def parse_persp_kpis(html: str) -> dict:
    """Parse the frontend PERSP_KPIS map → {perspective: [kpi, ...]}."""
    block = _slice_object(html, "const PERSP_KPIS = {")
    out = {}
    for m in re.finditer(r"^\s*(\w+):\s*\[([^\]]*)\]", block, re.MULTILINE):
        persp, arr = m.groups()
        out[persp] = [x.strip().strip("'\"") for x in arr.split(",") if x.strip()]
    return out


def parse_topic_kpis(html: str) -> dict:
    """Parse the frontend TOPIC_KPIS map → {topic: [kpi, ...]}."""
    block = _slice_object(html, "const TOPIC_KPIS = {")
    out = {}
    for m in re.finditer(r"^\s*'?([\w-]+)'?:\s*\[([^\]]*)\]", block, re.MULTILINE):
        topic, arr = m.groups()
        out[topic] = [x.strip().strip("'\"") for x in arr.split(",") if x.strip()]
    return out


def parse_drill_keys(html: str) -> set:
    """Top-level keys of the frontend DRILL map (drill targets that exist)."""
    block = _slice_object(html, "const DRILL = {")
    return set(re.findall(r"^\s*'?([\w-]+)'?:\s*\{\s*eb:", block, re.MULTILINE))


def primary_attr(fs):
    fmt = fs.formats[0]
    a = fmt.attributes[0]
    return a.name, a.key, a.detail_spec


def main() -> int:
    html = _HTML.read_text()
    metrics = parse_metrics(html)
    persp_kpis = parse_persp_kpis(html)
    topic_kpis = parse_topic_kpis(html)
    drill_keys = parse_drill_keys(html)

    reg_keys = set(specs.SPECS.keys())

    # 1. Frontend METRICS keys == registry keys.
    check(set(metrics) == reg_keys,
          f"METRICS keys {set(metrics)} != registry keys {reg_keys}")

    # 2. Per-tile: registry internals + agreement with frontend METRICS.
    for key, fs in specs.SPECS.items():
        name, value_key, detail = primary_attr(fs)
        ann = fs.annotations or {}
        prov = (ann.get("provenance") or [None])[0]
        endpoint = (ann.get("endpoint") or [None])[0]
        render = (ann.get("render_kind") or [None])[0]
        icon = (ann.get("icon") or [None])[0]
        color = (ann.get("color") or [None])[0]
        series = (ann.get("series") or [None])[0]

        check(render == "kpi", f"[{key}] render_kind={render!r} (expected 'kpi')")
        check(prov in specs.PROVENANCE, f"[{key}] provenance={prov!r} not in {specs.PROVENANCE}")
        check(endpoint in specs.ENDPOINTS, f"[{key}] endpoint={endpoint!r} not in {specs.ENDPOINTS}")
        check(bool(value_key), f"[{key}] empty value field key")
        check(bool(detail), f"[{key}] empty detail_spec (drill target)")
        check(fs.family == specs.FAMILY, f"[{key}] family={fs.family!r} (expected {specs.FAMILY!r})")
        check(bool(fs.action and fs.action.function), f"[{key}] missing action.function")
        check(detail in drill_keys, f"[{key}] detail_spec {detail!r} not a DRILL target {sorted(drill_keys)}")

        if key in metrics:
            fm = metrics[key]
            check(fm["label"] == name, f"[{key}] label: frontend {fm['label']!r} != spec {name!r}")
            check(fm["drill"] == detail, f"[{key}] drill: frontend {fm['drill']!r} != spec {detail!r}")
            check(fm["ico"] == icon, f"[{key}] icon: frontend {fm['ico']!r} != spec {icon!r}")
            check(fm["color"] == color, f"[{key}] color: frontend {fm['color']!r} != spec {color!r}")
            check((fm["hist"] or None) == (series or None),
                  f"[{key}] series: frontend {fm['hist']!r} != spec {series!r}")

    # 3. PERSP_KPIS: frontend == registry (exact, order included).
    check(persp_kpis == specs.PERSP_KPIS,
          f"PERSP_KPIS mismatch:\n  frontend={persp_kpis}\n  registry={specs.PERSP_KPIS}")

    # 4. perspectives_for() inverts PERSP_KPIS correctly.
    for persp, keys in specs.PERSP_KPIS.items():
        for k in keys:
            check(persp in specs.perspectives_for(k),
                  f"perspectives_for({k!r}) missing {persp!r}")
    for k in reg_keys:
        for persp in specs.perspectives_for(k):
            check(k in specs.PERSP_KPIS.get(persp, []),
                  f"perspectives_for({k!r}) claims {persp!r} but PERSP_KPIS disagrees")

    # 4b. TOPIC_KPIS: frontend == registry (exact, order included) — same drift
    # guard as PERSP_KPIS, for the independent Topic axis.
    check(topic_kpis == specs.TOPIC_KPIS,
          f"TOPIC_KPIS mismatch:\n  frontend={topic_kpis}\n  registry={specs.TOPIC_KPIS}")

    for topic, keys in specs.TOPIC_KPIS.items():
        for k in keys:
            check(topic in specs.topics_for(k),
                  f"topics_for({k!r}) missing {topic!r}")
    for k in reg_keys:
        for topic in specs.topics_for(k):
            check(k in specs.TOPIC_KPIS.get(topic, []),
                  f"topics_for({k!r}) claims {topic!r} but TOPIC_KPIS disagrees")

    # 5. The generated metrics-doc block is up to date.
    res = subprocess.run(
        [sys.executable, str(_HERE / "gen_overview_metrics.py"), "--check"],
        capture_output=True, text=True,
    )
    check(res.returncode == 0,
          f"OVERVIEW_METRICS.md generated block is stale (run gen_overview_metrics.py): "
          f"{res.stdout.strip()} {res.stderr.strip()}")

    # 5b. The generated metric-governance glossary doc (NEXT-24) is up to date
    # relative to _TILES' summary/usage fields.
    res = subprocess.run(
        [sys.executable, str(_HERE / "gen_dashboard_glossary.py"), "--check"],
        capture_output=True, text=True,
    )
    check(res.returncode == 0,
          f"OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md is stale (run gen_dashboard_glossary.py): "
          f"{res.stdout.strip()} {res.stderr.strip()}")

    # 6. Container (NEXT-10 P2): the Overview dashboard container's declared
    # placement order matches overview_specs.TILE_ORDER, every ref resolves,
    # and each perspective's filtered view matches PERSP_KPIS exactly (order
    # included) — the same drift class this whole registry exists to prevent,
    # now checked one layer up.
    import overview_containers as containers

    refs = [p.ref for p in containers.OVERVIEW_CONTAINER.placements]
    check(refs == specs.TILE_ORDER,
          f"Container placement order != TILE_ORDER:\n  container={refs}\n  registry={specs.TILE_ORDER}")

    resolved = containers.resolve(containers.OVERVIEW_CONTAINER)
    check(len(resolved) == len(specs.TILE_ORDER), "Container did not resolve one placement per tile")
    for rp in resolved:
        check(rp.kind == "tile", f"[{rp.ref}] resolved kind={rp.kind!r} (expected 'tile')")
        fs = specs.SPECS[rp.ref]
        check(rp.heading == fs.heading, f"[{rp.ref}] resolved heading != FormatSet heading")

    for persp, expected in specs.PERSP_KPIS.items():
        view = [rp.ref for rp in containers.view_for_perspective(containers.OVERVIEW_CONTAINER, persp)]
        check(view == expected,
              f"[{persp}] container perspective view != PERSP_KPIS:\n  view={view}\n  expected={expected}")

    # 6b. Same check for the Topic axis, and for the combined view_for()
    # intersection (Perspective ∩ Topic, falling back to Topic-only when the
    # intersection is empty).
    for topic, expected in specs.TOPIC_KPIS.items():
        view = [rp.ref for rp in containers.view_for_topic(containers.OVERVIEW_CONTAINER, topic)]
        check(view == expected,
              f"[{topic}] container topic view != TOPIC_KPIS:\n  view={view}\n  expected={expected}")

    for persp, persp_keys in specs.PERSP_KPIS.items():
        for topic, topic_keys in specs.TOPIC_KPIS.items():
            expected_intersection = [k for k in persp_keys if k in topic_keys]
            expected = expected_intersection if expected_intersection else topic_keys
            view = [rp.ref for rp in containers.view_for(containers.OVERVIEW_CONTAINER, persp, topic)]
            check(view == expected,
                  f"[{persp}+{topic}] view_for() != expected intersection/fallback:\n  view={view}\n  expected={expected}")

    # 7. NEXT-24 metric-governance guard: every tile must carry non-empty
    # summary/usage fields (§2.6) -- a new tile can't ship undocumented.
    for tile in specs._TILES:
        check(bool(tile.get("summary")),
              f"[{tile['key']}] missing a non-empty 'summary' field (required by NEXT-24)")
        check(bool(tile.get("usage")),
              f"[{tile['key']}] missing a non-empty 'usage' field (required by NEXT-24)")

    # Report.
    print(f"ran {_checks} checks over {len(reg_keys)} tiles / {len(specs.PERSP_KPIS)} perspectives / "
          f"{len(specs.TOPIC_KPIS)} topics")
    if _failures:
        print(f"\nFAILED ({len(_failures)}):")
        for f in _failures:
            print(f"  ✗ {f}")
        return 1
    print("PASS — registry, frontend maps, and metrics doc are in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
