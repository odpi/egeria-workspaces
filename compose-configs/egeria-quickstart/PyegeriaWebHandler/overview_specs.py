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


# Topic → ordered KPI selection — a second, independent axis from Perspective.
# Perspective is *who* (a persona/role); Topic is *what domain of concern*
# (AI-readiness, security/privacy, quality, usage/popularity). The two are
# orthogonal: a tile can belong to several perspectives AND several topics, and
# the dashboard's KPI band is the intersection of whichever one(s) the user has
# selected (see egeria-overview.html's currentKpiKeys()). Mirrors PERSP_KPIS's
# shape exactly, including the frontend/backend drift guard in
# test_overview_specs.py. "Any" (no topic selected) is not a key here — it's
# the absence of a topic filter, handled by the caller.
#
# v1 taxonomy is deliberately small (4 topics) and some tiles are left
# untagged (assets, terms, exceptions, certs, communities) — they're scale/
# baseline metrics or don't yet have a clean single-topic home; they still
# show up whenever Topic is "Any". "quality" is intentionally thin today (one
# tile) — Survey Annotation Coverage (OVERVIEW_CONTEXT_INTELLIGENCE.md Tier 2,
# not yet built) is its natural second member, not invented here to pad it out.
TOPIC_KPIS: Dict[str, List[str]] = {
    "ai-context":       ["grounding", "ownership", "governed"],
    "security-privacy": ["governed", "certs"],
    "quality":          ["exceptions"],
    "usage":            ["products", "isc", "blueprints", "people", "communities"],
}


def topics_for(kpi_key: str) -> List[str]:
    """Topics whose KPI selection includes ``kpi_key`` (TOPIC_KPIS inverted),
    in a stable topic order."""
    return [t for t, keys in TOPIC_KPIS.items() if kpi_key in keys]


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
        "summary": "Sum of active elements across 7 named asset/infrastructure types.",
        "usage": "Fixed to a hand-picked list of 7 type names (DataStore, DataSet, "
                 "DeployedSoftwareComponent, ITInfrastructure, DeployedAPI, Process, DataFeed) "
                 "-- NOT every Asset subtype in the type system, and NOT the same population "
                 "context_readiness_funnel's 'cataloged' stage uses (that one counts the broad "
                 "Asset supertype directly, a different, usually larger number). Treat this as "
                 "\"the types we've chosen to headline\", not a canonical total asset count -- "
                 "see OVERVIEW_NEXT_STEPS.md's \"Asset definition\" open decision for the "
                 "unresolved discrepancy between this and the growth-chart's own asset series.",
    },
    {
        "key": "terms", "label": "Glossary Terms", "icon": "📖", "color": "var(--c1)",
        "description": "Count of GlossaryTerm elements — the business vocabulary.",
        "target_type": "GlossaryTerm", "endpoint": "summary", "value_field": "termCount",
        "detail_spec": "grounding", "series": "terms", "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "GlossaryTerm"}),
        "questions": ["How rich is our business vocabulary?"],
        "summary": "Native count of active GlossaryTerm elements across all glossaries.",
        "usage": "Vocabulary SIZE, not vocabulary UTILIZATION -- a Term counts here whether or "
                 "not it is ever linked to an asset via SemanticAssignment (see Semantic "
                 "Grounding's own caveat for how unreliable that linkage signal currently is). "
                 "No status filter is passed to the underlying query, so a DRAFT or DEPRECATED "
                 "term counts the same as a published, in-use one.",
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
        "summary": "Count of elements carrying at least one governance classification, as a "
                   "percentage of Assets.",
        "usage": "The numerator (governance-classified elements) is NOT scoped to Asset -- ANY "
                 "element type carrying one of the 5 classifications counts, matched ANY not ALL "
                 "(one classification is enough). The denominator (percentage base) IS Asset-only. "
                 "So this can legitimately exceed a naive expectation if many non-Asset elements "
                 "(e.g. GovernanceDefinitions, Projects) are classified -- it is a coverage signal, "
                 "not literally \"the fraction of assets meeting the label\". Also capped at "
                 "DEFAULT_CAP (500) server elements per query -- governedCapped=true in the raw "
                 "payload means the true count is a floor, not exact.",
    },
    {
        "key": "certs", "label": "Active Certifications", "icon": "📜", "color": "var(--c4)",
        "description": "Count of active Certification relationships (with expiring/licenses sub-stats).",
        "target_type": None, "endpoint": "summary", "value_field": "certifications",
        "detail_spec": "certs", "series": None, "unit": None, "provenance": "live",
        "compute": ("ClassificationExplorer.get_relationships", {"relationship_type": "Certification"}),
        "questions": ["What's certified, and what's expiring?"],
        "summary": "Count of Certification relationships currently attached to any element.",
        "usage": "Despite the \"Active\" in the tile label, this is a raw count of every "
                 "Certification relationship fetched (up to a 500-relationship cap) -- there is "
                 "no filter for whether the certification's own validity window has actually "
                 "expired. The expiring-within-90-days and licenses sub-stats shown in the drill "
                 "view are computed from that same fetch, but the headline number itself is not "
                 "narrowed to \"currently valid\".",
    },
    {
        "key": "products", "label": "Data Products", "icon": "📦", "color": "var(--c3)",
        "description": "Count of DigitalProduct elements published for consumption.",
        "target_type": "DigitalProduct", "endpoint": "summary", "value_field": "dataProducts",
        "detail_spec": "products", "series": "products", "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "DigitalProduct"}),
        "questions": ["What data products are available?"],
        "summary": "Native count of DigitalProduct elements defined in the catalog.",
        "usage": "No lifecycle/status filter is applied -- a DigitalProduct still in DRAFT and "
                 "never released to consumers counts identically to one that is PUBLISHED and "
                 "actively subscribed to. This is a count of product DEFINITIONS, not a measure "
                 "of adoption or usage.",
    },
    {
        "key": "exceptions", "label": "Open Exceptions", "icon": "⚠️", "color": "var(--c5)",
        "description": "Count of open Exception governance relationships awaiting review.",
        "target_type": None, "endpoint": "summary", "value_field": "openExceptions",
        "detail_spec": "exceptions", "series": None, "unit": None, "provenance": "live",
        "compute": ("ClassificationExplorer.get_relationships", {"relationship_type": "Exception"}),
        "questions": ["What governance issues are open?"],
        "summary": "Count of Exception relationships currently attached to any element.",
        "usage": "Despite the \"Open\" in the tile label, no open/resolved status filter is "
                 "applied -- this counts every Exception relationship that exists. Also: "
                 "pyegeria's own count_relationships() docstring flags that this "
                 "get_relationships-based path can disagree materially with a native "
                 "MetadataExpert count for this exact relationship type (one comparison found "
                 "55 vs 276 -- tracked as PY-18 in egeria-python's PYEGERIA_ISSUES.md). Treat "
                 "this number as one counting method's answer, not a verified ground truth.",
    },
    {
        "key": "people", "label": "People / Contributors", "icon": "👥", "color": "var(--c2)",
        "description": "Count of Person actor profiles (registered contributors).",
        "target_type": "Person", "endpoint": "people", "value_field": "activeContributors",
        "detail_spec": "people", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "Person"}),
        "questions": ["Who contributes to the catalog?"],
        "summary": "Native count of active Person elements in the repository.",
        "usage": "Despite the tile label \"People / Contributors\", this counts every Person "
                 "element that exists, not people who have actually contributed anything -- "
                 "there is no activity/contribution filter here. A person registered in the "
                 "repository but who has never edited, rated, or commented on anything still "
                 "counts. \"Feedback Items\" (a separate signal, same People & Community section) "
                 "is the closer proxy for actual contribution activity.",
    },
    {
        "key": "communities", "label": "Active Communities", "icon": "🌐", "color": "var(--c6)",
        "description": "Count of Community elements — collaboration groups.",
        "target_type": "Community", "endpoint": "people", "value_field": "communities",
        "detail_spec": "people", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "Community"}),
        "questions": ["What communities are active?"],
        "summary": "Native count of Community elements in the repository.",
        "usage": "Same shape as People/Contributors' caveat: despite \"Active\" in the tile "
                 "label, there is no participation/activity filter -- a Community with no "
                 "members or posts counts the same as a thriving one.",
    },
    {
        "key": "isc", "label": "Supply Chains", "icon": "🔗", "color": "var(--c2)",
        "description": "Count of InformationSupplyChain elements — end-to-end data flows.",
        "target_type": "InformationSupplyChain", "endpoint": "usage-context",
        "value_field": "informationSupplyChains",
        "detail_spec": "isc", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "InformationSupplyChain"}),
        "questions": ["How does data flow through the business?"],
        "summary": "Native count of InformationSupplyChain elements in the repository.",
        "usage": "Counts chain DEFINITIONS regardless of whether they have any segments or "
                 "implementation wired up -- a supply chain that is just a name with no linked "
                 "solution components beneath it counts the same as a fully modeled one. Not a "
                 "measure of how much of the business is actually mapped end-to-end.",
    },
    {
        "key": "blueprints", "label": "Solution Blueprints", "icon": "🧱", "color": "var(--c3)",
        "description": "Count of SolutionBlueprint elements — reusable solution designs.",
        "target_type": "SolutionBlueprint", "endpoint": "usage-context", "value_field": "blueprints",
        "detail_spec": "blueprints", "series": None, "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "SolutionBlueprint"}),
        "questions": ["What solution designs exist?"],
        "summary": "Native count of SolutionBlueprint elements in the repository.",
        "usage": "Counts blueprint DEFINITIONS regardless of composition depth -- a blueprint "
                 "with no SolutionComponents actually linked beneath it counts the same as a "
                 "fully detailed one.",
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
        "summary": "Count and percentage of SemanticAssignment relationships, as a proxy for "
                   "assets grounded with business meaning for AI.",
        "usage": "CAVEAT, confirmed live 2026-08-01: SemanticAssignment is NOT Asset-scoped. In "
                 "this dataset, of 397 SemanticAssignment relationships, 348 (87.7%) connect to "
                 "GovernanceActionProcess elements (governance workflow automation, e.g. "
                 "subscription-management processes) -- not data assets. The remainder connect to "
                 "schema-level elements (DataField, TabularColumn, APIParameter, ...), which are "
                 "not Asset-typed themselves either (they'd need one more hop to their anchor "
                 "Asset). Zero of the 397 relationships connect directly to an Asset element. "
                 "Treat this percentage as an upper bound on true asset grounding, not a measured "
                 "grounded-asset rate, until NEXT-24's audit resolves the scoping (e.g. by "
                 "filtering to relationships whose non-term end is Asset-typed, or by following "
                 "schema elements up to their anchor Asset).",
    },
    {
        "key": "ownership", "label": "Ownership Coverage", "icon": "🧑‍💼", "color": "var(--c4)",
        "description": "Share of assets carrying an Ownership classification — a named "
                       "owner responsible for management/governance decisions. Distinct "
                       "from Governed Coverage (classification-based); data mesh names "
                       "'clean, owned, product-based data' as its own foundation for "
                       "trustworthy AI consumption.",
        "target_type": None, "endpoint": "ai-context", "value_field": "ownershipPct",
        "detail_spec": "ownership", "series": None, "unit": "percent", "provenance": "live",
        "compute": ("pyegeria.view.overview_metrics.ownership_coverage", {}),
        "questions": ["How much of the catalog has a named, accountable owner?"],
        "summary": "Count and percentage of elements carrying an Ownership classification, as a "
                   "percentage of Assets.",
        "usage": "Same scoping shape as Governed Coverage's caveat: the numerator (Ownership-"
                 "classified elements) is NOT Asset-scoped -- ANY element type with the "
                 "classification counts -- while the denominator (percentage base) IS Asset-only. "
                 "Not yet fully audited for exactly which element types carry Ownership in this "
                 "dataset (spot-checked live 2026-08-01: at least SolutionActorRole appears as an "
                 "owner-type value) -- a fuller by-owner-type breakdown is what `byOwnerType` in "
                 "the raw payload already returns, just not yet surfaced in this tile's UI.",
    },
]

# Stable tile order (the order tiles are declared above).
TILE_ORDER: List[str] = [t["key"] for t in _TILES]


# ── Business Value tiles (NEXT-9) ────────────────────────────────────────────
# NOT FormatSet-shaped like _TILES -- these live outside the KPI-band/
# Perspective/Topic model entirely (R-4's finding: most of a dashboard
# section's content, including this whole one, is hardcoded HTML, not tile-
# registry-driven). They still get the same summary/usage/info-bubble/
# Glossary-governance treatment as _TILES (NEXT-24's pattern), just via this
# smaller, separate list rather than a second FormatSet family — a plain
# dict shape reused as-is by gen_dashboard_glossary.py and by /api/overview/
# specs' "businessValue" key (loadTileInfo() in egeria-overview.html reads
# both that and "specs" into the same TILE_INFO map for the ⓘ bubble).
_BUSINESS_VALUE = [
    {
        "key": "bv-risk", "label": "Risk & Compliance", "provenance": "live",
        "description": "Count of Asset-typed elements carrying a Confidentiality classification.",
        "summary": "Count of Asset-typed elements classified Confidentiality, out of all "
                    "Asset-hierarchy elements checked.",
        "usage": "Proxy for regulatory exposure surface -- more classified elements need active "
                 "governance, this is not itself a measure of risk being controlled. Scoped to "
                 "the Asset type hierarchy specifically -- distinct from Governed Coverage's own "
                 "`byClassification[\"Confidentiality\"]`, which is NOT Asset-scoped (any element "
                 "type carrying the classification counts there). The two numbers can legitimately "
                 "differ a lot in the same dataset (e.g. 5 vs 1) and both are correct -- different "
                 "populations, not a discrepancy.",
    },
    {
        "key": "bv-productivity", "label": "Productivity", "provenance": "live",
        "description": "Share of Asset-hierarchy elements with a non-empty description.",
        "summary": "Percentage of Asset-hierarchy elements carrying a non-empty description, "
                    "out of all elements checked.",
        "usage": "Proxy for self-service findability -- a described asset is easier to evaluate "
                 "without a steward's help. Doesn't measure actual query/access frequency, so "
                 "treat it as a leading indicator, not a usage measure.",
    },
    {
        "key": "bv-trust", "label": "Trust & Adoption", "provenance": "live",
        "description": "Count of published DigitalProduct definitions.",
        "summary": "Count of published DigitalProduct definitions (reuses the same live count "
                    "the Data Products KPI tile shows).",
        "usage": "Counts product DEFINITIONS, not adoption -- no rating/usage signal is wired. "
                 "No `AttachedRating` relationships exist against DigitalProduct in a typical demo "
                 "dataset (confirmed live), so a rating average is honestly omitted rather than "
                 "faked; a real adoption signal would need one wired (e.g. subscription counts).",
    },
    {
        "key": "bv-cost", "label": "Cost Avoidance", "provenance": "live",
        "description": "Count of elements classified ConsolidatedDuplicate.",
        "summary": "Count of elements carrying the ConsolidatedDuplicate classification (absorbed "
                    "a detected duplicate).",
        "usage": "A candidate-for-archival signal, not a cost figure -- no dollar estimate is "
                 "attached. A real zero in a dataset with no duplicate-detection activity yet run "
                 "is an honest answer, not evidence the feature is broken.",
    },
]


def business_value_as_dicts() -> Dict[str, dict]:
    """The Business Value registry serialized the same shape as specs_as_dicts()'s per-tile
    dicts need for the frontend's TILE_INFO/loadTileInfo() and for gen_dashboard_glossary.py --
    just {key: {label, description, summary, usage, provenance}}, no FormatSet wrapping."""
    return {t["key"]: t for t in _BUSINESS_VALUE}


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
    if tile.get("summary"):
        annotations["summary"] = [tile["summary"]]
    if tile.get("usage"):
        annotations["usage"] = [tile["usage"]]
    topics = topics_for(tile["key"])
    if topics:
        annotations["topics"] = topics

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
        "topicKpis": TOPIC_KPIS,
        "specs": specs_as_dicts(),
        "businessValue": business_value_as_dicts(),
        "source": "overview_specs.py (NEXT-10 P0)",
    }
