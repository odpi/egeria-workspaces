"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria Overview — dashboard tile registry (NEXT-10, phase P0).

This module is the **single source of truth** for the Overview dashboard's KPI
tiles. Each tile is expressed as a pyegeria **`FormatSet`** (a.k.a. ReportSpec)
— the same model used by the Egeria Advisor's report builder and the
Perspective/Question work — proving out the reporting/dashboard model described
in `OVERVIEW_REPORTING_MODEL.md`.

Why this exists
---------------
A tile's definition used to be spread across ~6 hand-synced places
(`overview_handler.py` compute, the frontend `METRICS`/`DRILL`/`PERSP_KPIS`
maps + `apply*` field-mapping, the hardcoded provenance badges, and the
hand-written `OVERVIEW_METRICS.md`). Every drift bug we hit — wrong drill
links, stale metrics doc, provenance mismatches — came from that loose
coupling. This registry collapses "what is displayed / how it's computed / how
it's displayed / how to drill / who it's for / how trustworthy it is" into one
declarative definition per tile, served at `/api/overview/specs` and used to
generate the metrics catalog (`gen_overview_metrics.py`). `test_overview_specs.py`
guards that the frontend maps and this registry stay in sync.

How the FormatSet fields are used
---------------------------------
- ``heading``         — the tile label ("Cataloged Assets").
- ``description``     — one-line definition of the metric.
- ``target_type``     — the Open Metadata type the metric counts, when it is a
                        single type (``GlossaryTerm``, ``DigitalProduct``, …).
                        ``None`` for composite/relationship metrics.
- ``family``          — ``"overview-kpi"`` so the whole set is discoverable.
- ``action``          — ``ActionParameter`` naming the compute function + params
                        (the "how it's computed"; the P3 report-runner hook).
- ``formats[0]``      — one ``Format`` whose ``types`` carries the render kind
                        (``"kpi"``) and whose ``attributes`` name the value field
                        (``key`` = the backend payload field) and the drill
                        target (``detail_spec``).
- ``question_spec``   — ``perspectives`` (who the tile is for — the inverse of
                        ``PERSP_KPIS``) + example ``questions``.
- ``annotations``     — dashboard-specific extensions FormatSet doesn't model
                        natively yet (render kind is P1 work upstream). Stored as
                        ``Dict[str, List[str]]`` (FormatSet's annotation shape):
                        ``render_kind``, ``provenance``, ``endpoint``, ``icon``,
                        ``color``, and optionally ``series`` (sparkline field)
                        and ``unit`` (``percent``).

Nothing here mutates pyegeria's model — the render-kind / provenance
generalization of `Format` itself is deliberately deferred to P1 (see
`OVERVIEW_REPORTING_MODEL.md` §5, §10).
"""

from __future__ import annotations

from typing import Dict, List

# The FormatSet model moved to pyegeria.view in newer releases; keep a fallback
# so this module (and its test) work against both layouts.
try:  # pragma: no cover - import-path shim
    from pyegeria.view._output_format_models import (
        FormatSet, Format, Attribute, ActionParameter, QuestionSpec,
    )
except Exception:  # pragma: no cover
    from pyegeria._output_format_models import (  # type: ignore
        FormatSet, Format, Attribute, ActionParameter, QuestionSpec,
    )


FAMILY = "overview-kpi"

# Provenance vocabulary — mirrors the dashboard's in-UI badges and
# OVERVIEW_METRICS.md's status legend.
PROVENANCE = ("live", "mixed", "illustrative")

# The backend endpoints a tile's value can be sourced from (the /api/overview/*
# routes in overview_handler.py).
ENDPOINTS = ("summary", "people", "usage-context", "ai-context")

# Perspective → ordered KPI selection. This is the *source of truth* for which
# tiles each perspective shows; the frontend PERSP_KPIS must match it (guarded by
# test_overview_specs.py). Each tile's question_spec.perspectives is the inverse.
PERSP_KPIS: Dict[str, List[str]] = {
    "governance": ["assets", "terms", "governed", "certs", "products", "exceptions"],
    "steward":    ["assets", "governed", "exceptions", "certs", "terms", "grounding"],
    "owner":      ["products", "governed", "certs", "exceptions", "people", "grounding"],
    "consumer":   ["products", "terms", "grounding", "isc", "blueprints", "people"],
    "engineer":   ["assets", "isc", "blueprints", "grounding", "exceptions", "governed"],
    "builder":    ["assets", "grounding", "isc", "blueprints", "governed", "products"],
    "privacy":    ["governed", "certs", "exceptions", "assets", "grounding", "products"],
    "community":  ["people", "communities", "products", "terms", "governed", "assets"],
}


def perspectives_for(kpi_key: str) -> List[str]:
    """Perspectives whose KPI selection includes ``kpi_key`` (PERSP_KPIS inverted),
    in a stable perspective order."""
    return [p for p, keys in PERSP_KPIS.items() if kpi_key in keys]


# ── Tile definitions ─────────────────────────────────────────────────────────
# One dict per tile carrying the raw facts; _build() turns each into a FormatSet.
# Field notes:
#   key         — the dashboard's stable tile id (frontend METRICS key / drill id)
#   value_field — the field in the endpoint's JSON payload holding the value
#   detail_spec — the drill target (frontend DRILL map key)
#   series      — sparkline series field from /api/overview/growth (or None)
#   compute     — (function, spec_params) describing how it's computed
_TILES = [
    {
        "key": "assets", "label": "Cataloged Assets", "icon": "🗂️", "color": "var(--c2)",
        "description": "Sum of counts of the key asset/infrastructure types in the catalog.",
        "target_type": None, "endpoint": "summary", "value_field": "assetTotal",
        "detail_spec": "assets", "series": "assets", "unit": None, "provenance": "live",
        "compute": ("overview.sum_type_counts",
                    {"types": ["DataStore", "DataSet", "DeployedSoftwareComponent",
                               "ITInfrastructure", "DeployedAPI", "Process", "DataFeed"]}),
        "questions": ["How much is cataloged?", "How is the catalog growing?"],
    },
    {
        "key": "terms", "label": "Glossary Terms", "icon": "📖", "color": "var(--c1)",
        "description": "Count of GlossaryTerm elements — the business vocabulary.",
        "target_type": "GlossaryTerm", "endpoint": "summary", "value_field": "termCount",
        "detail_spec": "grounding", "series": "terms", "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "GlossaryTerm"}),
        "questions": ["How rich is our business vocabulary?"],
    },
    {
        "key": "governed", "label": "Governed Coverage", "icon": "🛡️", "color": "var(--c6)",
        "description": "Share of assets carrying at least one governance classification "
                       "(ZoneMembership/Confidentiality/Criticality/Impact/Retention).",
        "target_type": None, "endpoint": "summary", "value_field": "governedCount",
        "detail_spec": "governed", "series": "gov", "unit": "percent", "provenance": "live",
        "compute": ("MetadataExpert.find_metadata_elements",
                    {"matchClassifications": ["ZoneMembership", "Confidentiality",
                                              "Criticality", "Impact", "Retention"],
                     "matchCriteria": "ANY"}),
        "questions": ["Are we in control of the catalog?", "What's ungoverned?"],
    },
    {
        "key": "certs", "label": "Active Certifications", "icon": "📜", "color": "var(--c4)",
        "description": "Count of active Certification relationships (with expiring/licenses sub-stats).",
        "target_type": None, "endpoint": "summary", "value_field": "certifications",
        "detail_spec": "certs", "series": None, "unit": None, "provenance": "live",
        "compute": ("ClassificationExplorer.get_relationships", {"relationship_type": "Certification"}),
        "questions": ["What's certified, and what's expiring?"],
    },
    {
        "key": "products", "label": "Data Products", "icon": "📦", "color": "var(--c3)",
        "description": "Count of DigitalProduct elements published for consumption.",
        "target_type": "DigitalProduct", "endpoint": "summary", "value_field": "dataProducts",
        "detail_spec": "products", "series": "products", "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "DigitalProduct"}),
        "questions": ["What data products are available?"],
    },
    {
        "key": "exceptions", "label": "Open Exceptions", "icon": "⚠️", "color": "var(--c5)",
        "description": "Count of open Exception governance relationships awaiting review.",
        "target_type": None, "endpoint": "summary", "value_field": "openExceptions",
        "detail_spec": "exceptions", "series": None, "unit": None, "provenance": "live",
        "compute": ("ClassificationExplorer.get_relationships", {"relationship_type": "Exception"}),
        "questions": ["What governance issues are open?"],
    },
    {
        "key": "people", "label": "People / Contributors", "icon": "👥", "color": "var(--c2)",
        "description": "Count of Person actor profiles (registered contributors).",
        "target_type": "Person", "endpoint": "people", "value_field": "activeContributors",
        "detail_spec": "people", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "Person"}),
        "questions": ["Who contributes to the catalog?"],
    },
    {
        "key": "communities", "label": "Active Communities", "icon": "🌐", "color": "var(--c6)",
        "description": "Count of Community elements — collaboration groups.",
        "target_type": "Community", "endpoint": "people", "value_field": "communities",
        "detail_spec": "people", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "Community"}),
        "questions": ["What communities are active?"],
    },
    {
        "key": "isc", "label": "Supply Chains", "icon": "🔗", "color": "var(--c2)",
        "description": "Count of InformationSupplyChain elements — end-to-end data flows.",
        "target_type": "InformationSupplyChain", "endpoint": "usage-context",
        "value_field": "informationSupplyChains",
        "detail_spec": "isc", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "InformationSupplyChain"}),
        "questions": ["How does data flow through the business?"],
    },
    {
        "key": "blueprints", "label": "Solution Blueprints", "icon": "🧱", "color": "var(--c3)",
        "description": "Count of SolutionBlueprint elements — reusable solution designs.",
        "target_type": "SolutionBlueprint", "endpoint": "usage-context", "value_field": "blueprints",
        "detail_spec": "blueprints", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "SolutionBlueprint"}),
        "questions": ["What solution designs exist?"],
    },
    {
        "key": "grounding", "label": "Semantic Grounding", "icon": "🧠", "color": "var(--c1)",
        "description": "Share of assets linked to glossary terms via SemanticAssignment "
                       "— the meaning layer that grounds AI.",
        "target_type": None, "endpoint": "ai-context", "value_field": "groundingPct",
        "detail_spec": "grounding", "series": None, "unit": "percent", "provenance": "live",
        "compute": ("ClassificationExplorer.get_relationships",
                    {"relationship_type": "SemanticAssignment", "as": "percent_of_assets"}),
        "questions": ["How well grounded is the catalog for AI?"],
    },
]

# Stable tile order (the order tiles are declared above).
TILE_ORDER: List[str] = [t["key"] for t in _TILES]


def _build(tile: dict) -> FormatSet:
    """Turn one raw tile dict into a FormatSet."""
    func, spec_params = tile["compute"]
    annotations: Dict[str, List[str]] = {
        "render_kind": ["kpi"],
        "provenance":  [tile["provenance"]],
        "endpoint":    [tile["endpoint"]],
        "icon":        [tile["icon"]],
        "color":       [tile["color"]],
        "tile_key":    [tile["key"]],
    }
    if tile.get("series"):
        annotations["series"] = [tile["series"]]
    if tile.get("unit"):
        annotations["unit"] = [tile["unit"]]

    return FormatSet(
        target_type=tile["target_type"],
        heading=tile["label"],
        description=tile["description"],
        family=FAMILY,
        annotations=annotations,
        formats=[Format(
            types=["kpi"],
            attributes=[Attribute(
                name=tile["label"],
                key=tile["value_field"],
                detail_spec=tile["detail_spec"],
            )],
        )],
        action=ActionParameter(function=func, spec_params=spec_params),
        question_spec=[QuestionSpec(
            perspectives=perspectives_for(tile["key"]),
            questions=tile["questions"],
        )],
    )


# The registry: tile_key -> FormatSet. Built once at import.
SPECS: Dict[str, FormatSet] = {t["key"]: _build(t) for t in _TILES}


def specs_as_dicts() -> Dict[str, dict]:
    """The registry serialized as plain dicts (FormatSet.dict() per tile)."""
    return {key: fs.dict() for key, fs in SPECS.items()}


def specs_payload() -> dict:
    """Payload for GET /api/overview/specs — ordered tiles + the perspective
    selection map, everything the frontend needs to render tiles declaratively."""
    return {
        "family": FAMILY,
        "order": TILE_ORDER,
        "perspectiveKpis": PERSP_KPIS,
        "specs": specs_as_dicts(),
        "source": "overview_specs.py (NEXT-10 P0)",
    }
