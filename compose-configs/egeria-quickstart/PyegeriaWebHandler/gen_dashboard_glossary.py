#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Generate a loadable Dr.Egeria doc governing the Overview dashboard's own
metrics as real Egeria elements — one GlossaryTerm per tile, grouped under a
RootCollection with sub-collections. Single source of truth is
`overview_specs.py`'s `_TILES` (no HTML-scraping needed here, unlike
`gen_perspectives.py` — the tile registry already lives in Python).

Design: OVERVIEW_METRIC_GOVERNANCE.md (NEXT-24). Only tiles carrying a
`summary` field are included — as of Phase B all 12 tiles have one; adding a
`summary`/`usage` pair to a future new tile in `_TILES` is all a future run
needs to pick it up, no change to this script required.

Also covers `overview_specs.py`'s `_BUSINESS_VALUE` list (NEXT-9, 2026-08-02)
-- the 4 Business Value tiles, which live outside `_TILES`/the KPI-band model
entirely (see `_BUSINESS_VALUE`'s own comment) but get the same Glossary Term
+ info-bubble treatment. They join a dedicated "Business Value Signals"
app-level sub-collection (not "Overview KPIs" -- they're a different section)
and their provenance collection, but skip Topic/Perspective membership: they
show on every Perspective/Topic combination, so tagging them into any one
Topic/Perspective sub-collection would misrepresent that as an exclusive home.

Phase D added the Topic and Perspective sub-collections (§2.2's "natural,
cheap follow-ons") — purely additive `Add Member to Collection` links on top
of the same Terms, using overview_specs.py's own `topics_for()`/
`perspectives_for()` inversions (the same functions that already drive the
dashboard's Topic-strip/Perspective-strip filtering), not a second
hand-maintained mapping.

Structure produced:
  Create Glossary               "Egeria Dashboard Analytics"           (once)
  Create Root Collection        "Egeria Dashboard"                     (once)
  Create Collection             "Overview KPIs"                        (once, app grouping)
  Create Collection             "Live Metrics" / "Mixed Metrics" /
                                 "Illustrative Metrics"                 (once each, provenance grouping)
  Create Collection             one per TOPIC_KPIS key                 (Phase D, topic grouping)
  Create Collection             one per PERSP_KPIS key                 (Phase D, perspective grouping)
  Add Member to Collection      (each sub-collection -> Egeria Dashboard)
  --- per tile with a summary ---
  Create Glossary Term          (Display Name/Summary/Description/Usage from the tile)
  Add Member to Collection      (Term -> Overview KPIs)
  Add Member to Collection      (Term -> its provenance collection)
  Add Member to Collection      (Term -> each Topic collection from topics_for(key))
  Add Member to Collection      (Term -> each Perspective collection from perspectives_for(key))

Command attribute names verified against the live compact command specs
(commands_glossary_compact.json / commands_collections_compact.json)
2026-08-01 before writing this — not assumed.

Usage:
    python3 gen_dashboard_glossary.py            # (re)write OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md
    python3 gen_dashboard_glossary.py --check     # exit 1 if the file is stale (CI/test guard)
    python3 gen_dashboard_glossary.py --stdout    # print the doc, don't write
"""
import sys
from pathlib import Path

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))

import overview_specs as specs  # noqa: E402

OUT = _HERE / "OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md"

GLOSSARY_NAME = "Egeria Dashboard Analytics"
ROOT_COLLECTION_NAME = "Egeria Dashboard"
APP_COLLECTION_NAME = "Overview KPIs"
BUSINESS_VALUE_COLLECTION_NAME = "Business Value Signals"
PROVENANCE_COLLECTIONS = {
    "live": "Live Metrics",
    "mixed": "Mixed Metrics",
    "illustrative": "Illustrative Metrics",
}
# Display names mirror egeria-overview.html's TOPIC_LABELS / PERSPECTIVES[*].label
# (minus the emoji) — kept here rather than imported since those live in the
# frontend's JS data, not overview_specs.py; only the *keys* (TOPIC_KPIS/
# PERSP_KPIS) are shared source of truth, guarded by test_overview_specs.py.
TOPIC_COLLECTIONS = {
    "ai-context":       "AI / Context Intelligence Metrics",
    "security-privacy": "Security / Privacy Metrics",
    "quality":          "Quality Metrics",
    "usage":            "Popularity / Usage Metrics",
}
PERSPECTIVE_COLLECTIONS = {
    "governance": "Data Governance Lead View",
    "steward":    "Data Steward View",
    "owner":      "Data Owner View",
    "consumer":   "Data Consumer / Analyst View",
    "engineer":   "Data Engineer / Platform View",
    "builder":    "App / AI Builder View",
    "privacy":    "Privacy / Risk Officer View",
    "community":  "Community Lead View",
}


def _block(lines):
    return "\n".join(lines) + "\n"


def build_doc() -> str:
    """Return the full generated doc text, or "" if no tile carries a summary yet."""
    tiles = [t for t in specs._TILES if t.get("summary")]
    biz_tiles = [t for t in specs._BUSINESS_VALUE if t.get("summary")]
    if not tiles and not biz_tiles:
        return ""

    out = [_block([
        "<!-- SPDX-License-Identifier: CC-BY-4.0 -->",
        "<!-- Copyright Contributors to the ODPi Egeria project. -->",
        "",
        "# Egeria Dashboard Analytics — Glossary & Collections",
        "",
        "> Loadable **Dr.Egeria** document that governs the Overview dashboard's own",
        "> metrics as real Egeria elements: one **GlossaryTerm** per metric (Summary/",
        "> Description/Usage — Usage carries caveats, e.g. scoping mismatches found",
        "> during the NEXT-24 audit), grouped under a **RootCollection** with",
        "> sub-collections (by app, by provenance, by Topic, by Perspective). Generated",
        "> from `overview_specs.py`'s",
        "> `_TILES` — the single source of truth. Regenerate with",
        "> `gen_dashboard_glossary.py` after editing a tile's `summary`/`description`/",
        "> `usage` fields.",
        ">",
        "> Design: `OVERVIEW_METRIC_GOVERNANCE.md` (NEXT-24), Phases A-D.",
        "> **Run with VALIDATE first, then PROCESS.** Create commands carry user-specified",
        "> Qualified Names so later commands in this doc can cross-reference them.",
        "",
        "---",
        "",
    ])]

    # ── Glossary ──────────────────────────────────────────────────────────
    out.append(_block([
        "## Create Glossary", "",
        "### Display Name", GLOSSARY_NAME, "",
        "### Description",
        "Definitions for the Overview dashboard's own metrics/KPI tiles — what each one "
        "actually measures, including known scoping caveats. Generated from "
        "overview_specs.py; see OVERVIEW_METRIC_GOVERNANCE.md (NEXT-24).", "",
        "### Qualified Name", f"Glossary::{GLOSSARY_NAME}", "",
        "### Version Identifier", "1.0", "",
        "---", "",
    ]))

    # ── Root Collection + sub-collections ────────────────────────────────
    root_qn = f"RootCollection::{ROOT_COLLECTION_NAME}"
    out.append(_block([
        "## Create Root Collection", "",
        "### Display Name", ROOT_COLLECTION_NAME, "",
        "### Description",
        "Master collection for everything describing the Egeria Portal's own dashboards "
        "(starting with Overview) -- what each metric measures, grouped a few different "
        "ways since an element can belong to more than one collection at once.", "",
        "### Qualified Name", root_qn, "",
        "### Version Identifier", "1.0", "",
        "---", "",
    ]))

    sub_collections = [(APP_COLLECTION_NAME,
                        "Metrics belonging to the Egeria Overview dashboard app.")]
    sub_collections.append((BUSINESS_VALUE_COLLECTION_NAME,
                            "The Overview dashboard's Business Value tiles (Risk & Compliance, "
                            "Productivity, Trust & Adoption, Cost Avoidance) -- shown to every "
                            "Perspective/Topic, not filtered like the KPI-band tiles."))
    sub_collections += [(name, f"Metrics whose provenance is currently \"{prov}\".")
                         for prov, name in PROVENANCE_COLLECTIONS.items()]
    sub_collections += [(name, f"Metrics shown when the Overview dashboard's Topic "
                                f"filter is set to \"{name}\" (topics_for()'s {topic!r}).")
                         for topic, name in TOPIC_COLLECTIONS.items()]
    sub_collections += [(name, f"Metrics shown to the \"{name.replace(' View', '')}\" "
                                f"Perspective on the Overview dashboard (perspectives_for()'s "
                                f"{persp!r}).")
                         for persp, name in PERSPECTIVE_COLLECTIONS.items()]

    sub_qns = {}
    for name, desc in sub_collections:
        qn = f"Collection::{name}"
        sub_qns[name] = qn
        out.append(_block([
            "## Create Collection", "",
            "### Display Name", name, "",
            "### Description", desc, "",
            "### Qualified Name", qn, "",
            "### Version Identifier", "1.0", "",
            "---", "",
        ]))
        out.append(_block([
            "## Add Member to Collection", "",
            "### Collection Id", root_qn, "",
            "### Element Id", qn, "",
            "---", "",
        ]))

    # ── One GlossaryTerm per tile ─────────────────────────────────────────
    for tile in tiles:
        key = tile["key"]
        term_qn = f"Term::overview-kpi-{key}"
        prov = tile.get("provenance", "illustrative")
        prov_collection = sub_qns[PROVENANCE_COLLECTIONS.get(prov, "Illustrative Metrics")]

        out.append(_block([
            "## Create Glossary Term", "",
            "### Display Name", tile["label"], "",
            "### Summary", tile["summary"], "",
            "### Description", tile["description"], "",
            "### Usage", tile.get("usage", "Not yet audited — no known caveats documented."), "",
            "### Glossary Name", GLOSSARY_NAME, "",
            "### Qualified Name", term_qn, "",
            "### Version Identifier", "1.0", "",
            "---", "",
        ]))
        out.append(_block([
            "## Add Member to Collection", "",
            "### Collection Id", sub_qns[APP_COLLECTION_NAME], "",
            "### Element Id", term_qn, "",
            "---", "",
        ]))
        out.append(_block([
            "## Add Member to Collection", "",
            "### Collection Id", prov_collection, "",
            "### Element Id", term_qn, "",
            "---", "",
        ]))
        for topic in specs.topics_for(key):
            out.append(_block([
                "## Add Member to Collection", "",
                "### Collection Id", sub_qns[TOPIC_COLLECTIONS[topic]], "",
                "### Element Id", term_qn, "",
                "---", "",
            ]))
        for persp in specs.perspectives_for(key):
            out.append(_block([
                "## Add Member to Collection", "",
                "### Collection Id", sub_qns[PERSPECTIVE_COLLECTIONS[persp]], "",
                "### Element Id", term_qn, "",
                "---", "",
            ]))

    # ── One GlossaryTerm per Business Value tile (NEXT-9) ────────────────
    for tile in biz_tiles:
        key = tile["key"]
        term_qn = f"Term::overview-kpi-{key}"
        prov = tile.get("provenance", "illustrative")
        prov_collection = sub_qns[PROVENANCE_COLLECTIONS.get(prov, "Illustrative Metrics")]

        out.append(_block([
            "## Create Glossary Term", "",
            "### Display Name", tile["label"], "",
            "### Summary", tile["summary"], "",
            "### Description", tile["description"], "",
            "### Usage", tile.get("usage", "Not yet audited — no known caveats documented."), "",
            "### Glossary Name", GLOSSARY_NAME, "",
            "### Qualified Name", term_qn, "",
            "### Version Identifier", "1.0", "",
            "---", "",
        ]))
        out.append(_block([
            "## Add Member to Collection", "",
            "### Collection Id", sub_qns[BUSINESS_VALUE_COLLECTION_NAME], "",
            "### Element Id", term_qn, "",
            "---", "",
        ]))
        out.append(_block([
            "## Add Member to Collection", "",
            "### Collection Id", prov_collection, "",
            "### Element Id", term_qn, "",
            "---", "",
        ]))

    return "".join(out)


def main(argv) -> int:
    doc = build_doc()
    if not doc:
        print("No tiles carry a 'summary' field yet -- nothing to generate.")
        return 0

    if "--stdout" in argv:
        print(doc)
        return 0

    current = OUT.read_text() if OUT.exists() else None
    if "--check" in argv:
        if current != doc:
            sys.stderr.write(
                f"{OUT.name} is OUT OF DATE relative to overview_specs.py's _TILES. "
                f"Run: python3 {Path(__file__).name}\n"
            )
            return 1
        print(f"{OUT.name} is up to date.")
        return 0

    if current != doc:
        OUT.write_text(doc)
        n_tiles = (len([t for t in specs._TILES if t.get("summary")])
                   + len([t for t in specs._BUSINESS_VALUE if t.get("summary")]))
        print(f"wrote {OUT} (terms={n_tiles})")
    else:
        print(f"{OUT.name} already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
