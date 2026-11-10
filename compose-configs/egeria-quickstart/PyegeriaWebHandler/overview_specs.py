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

import re
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
# routes in overview_handler.py). "growth" (time series) and "activity" (change
# stream) feed panels rather than KPI tiles, but are listed so the registry
# names every data route.
ENDPOINTS = ("summary", "people", "usage-context", "ai-context", "growth", "activity")

# Perspective → ordered KPI selection. This is the *source of truth* for which
# tiles each perspective shows; the frontend PERSP_KPIS must match it (guarded by
# test_overview_specs.py). Each tile's question_spec.perspectives is the inverse.
PERSP_KPIS: Dict[str, List[str]] = {
    "governance":     ["assets", "terms", "governed", "certs", "products", "exceptions"],
    "steward":        ["assets", "governed", "exceptions", "certs", "terms", "grounding"],
    "owner":          ["products", "governed", "certs", "exceptions", "people", "grounding"],
    "consumer":       ["products", "terms", "grounding", "isc", "blueprints", "people"],
    "app-ai-builder": ["assets", "grounding", "isc", "blueprints", "governed", "products"],
    "privacy":        ["governed", "certs", "exceptions", "assets", "grounding", "products"],
    "community":      ["people", "communities", "products", "terms", "governed", "assets"],
    "data-expert":    ["assets", "isc", "blueprints", "grounding", "exceptions", "governed"],
    "security":       ["governed", "exceptions", "ai-ready", "certs", "assets", "grounding"],
    "architecture":   ["isc", "blueprints", "assets", "grounding", "governed", "exceptions"],
}

# The ten Trellis perspectives the Overview shows, in foundations.md order (Financial and Administration
# are left out on purpose: design note §10.8). Egeria qualifiedName is "Perspective::<display name>".
# "Owner" was "Data Owner" until 2026-11-07, when Trellis moved to the content pack's Perspective::Owner.
PERSPECTIVE_DISPLAY_NAMES: List[str] = [
    "Governance", "Steward", "Owner", "Consumer", "App/AI Builder",
    "Privacy", "Community", "Data Expert", "Security", "Architecture",
]

# Keys the page saved in localStorage before a Trellis rename -> current key. "data-owner" -> "owner"
# since 2026-11-07; the older saved "owner" is the current key again, so it needs no entry.
LEGACY_PERSPECTIVE_KEYS: Dict[str, str] = {
    "data-owner": "owner", "engineer": "data-expert", "builder": "app-ai-builder",
}


def perspective_key(display_name: str) -> str:
    """Slug of a Trellis perspective display name: lower-case, runs of non-alphanumerics -> "-".
    Mirrors perspectiveKey() in egeria-overview.html (test_overview_specs.py proves they agree)."""
    return re.sub(r"[^a-z0-9]+", "-", (display_name or "").lower()).strip("-")


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
    "ai-context":       ["grounding", "ownership", "governed", "ai-ready"],
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
        "description": "Native count of the Asset supertype — everything cataloged.",
        "target_type": "Asset", "endpoint": "summary", "value_field": "assetTotal",
        "detail_spec": "assets", "series": "assets", "unit": None, "provenance": "live",
        # OVERVIEW_NEXT_STEPS.md "Asset definition" open decision, resolved
        # 2026-08-16: this used to sum 6 curated type names (via
        # sum_type_counts/sum_counts, BACKLOG.md NEXT-18), which disagreed
        # with growth_series' own "assets" series (raw `Asset` supertype
        # count) and with context_readiness_funnel's 'cataloged' stage (same
        # supertype) -- live example: 2,668 curated-sum vs 2,523
        # Asset-supertype. Now a single native count_metadata_elements call
        # against "Asset" directly, matching both of those. The "assets by
        # type" breakdown chart (Data Stores/Data Sets/.../Processes) still
        # shows the curated 6-type composition -- it's a breakdown view now,
        # not required to sum to this headline.
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "Asset"}),
        "questions": ["How much is cataloged?", "How is the catalog growing?"],
        "summary": "Native count of active elements of the Asset supertype (and all its subtypes).",
        "usage": "Broadest possible definition of \"cataloged\" -- every Asset subtype counts, "
                 "including e.g. DigitalProduct (which also has its own \"Data Products\" tile, "
                 "so the two headline numbers overlap by design, not a double-count bug: Data "
                 "Products is a callout of one Asset subtype, Cataloged Assets is the whole "
                 "population). Same population as the growth chart's own \"assets\" series and "
                 "context_readiness_funnel's 'cataloged' stage -- all three now agree.",
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
        "description": "Share of Assets carrying at least one governance classification "
                       "(ZoneMembership/Confidentiality/Criticality/Impact/Retention).",
        "target_type": None, "endpoint": "summary", "value_field": "governedCount",
        "detail_spec": "governed", "series": "gov", "unit": "percent", "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements",
                    {"metadataElementTypeName": "Asset",
                     "matchClassifications": ["ZoneMembership", "Confidentiality",
                                              "Criticality", "Impact", "Retention"],
                     "matchCriteria": "ANY"}),
        "questions": ["Are we in control of the catalog?", "What's ungoverned?"],
        "summary": "Count of Assets carrying at least one governance classification, as a "
                   "percentage of all Assets. Counts Assets only, so it will usually be lower than "
                   "before, when elements of any type counted.",
        "usage": "Assets-only share (owner decision 2026-11-06): the numerator is the number of Asset "
                 "elements carrying at least one of the 5 governance classifications "
                 "(ZoneMembership/Confidentiality/Criticality/Impact/Retention, matched ANY not ALL), "
                 "the denominator is the number of all Assets. Both are strict native counts, so the "
                 "500-element cap no longer applies and the percentage cannot exceed 100. Elements "
                 "that are not Assets (GovernanceDefinitions, Projects, glossary terms, ...) no longer "
                 "count, so the figure is usually lower than the earlier any-type tally. A count that "
                 "could not be measured shows as not measured, never 0. The Governed vs Ungoverned "
                 "donut is Asset-scoped the same way; the zone and classification breakdowns beside "
                 "it still count elements of any type. Scope: when the installed pyegeria supports "
                 "whole-repository counts, both numerator and denominator count the whole catalog "
                 "(including Assets you cannot open), so the share can be much smaller than the "
                 "viewer-scoped figure because the denominator is every Asset in the repository; "
                 "the tile says which scope it used.",
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
        "description": "Count of DigitalProduct elements, broken down by publication (deployment) status.",
        "target_type": "DigitalProduct", "endpoint": "summary", "value_field": "dataProducts",
        "detail_spec": "products", "series": "products", "unit": None, "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements", {"type_name": "DigitalProduct"}),
        "questions": ["What data products are available?", "How many are actually published vs. still in development?"],
        "summary": "Native count of DigitalProduct elements defined in the catalog, with an active-vs-pending breakdown by deploymentStatus.",
        "usage": "The headline number is every DigitalProduct DEFINITION regardless of status -- "
                 "a count of product definitions, not a measure of adoption or usage. "
                 "\"Active\" (dataProductsActive) counts deploymentStatus == ACTIVE specifically; "
                 "\"Pending\" (dataProductsPending) folds every other value (DRAFT, "
                 "UNDER_DEVELOPMENT, unset, etc.) together rather than enumerating each one, so it "
                 "reads as \"not yet actively deployed\" rather than a specific lifecycle stage. "
                 "Ratings (dataProductsRatings) is a system-wide AttachedRating relationship count, "
                 "not scoped to products specifically -- Egeria's relationship count can't filter "
                 "by one end's type without a graph traversal -- and is omitted from the tile "
                 "entirely when zero rather than showing a fake average.",
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
        "description": "Glossary-term links (SemanticAssignment) per 100 Assets — the meaning layer "
                       "that grounds AI. A link count, not a share of Assets; it becomes the share of "
                       "Assets with at least one term once pyegeria reports distinct grounded Assets.",
        "target_type": None, "endpoint": "ai-context", "value_field": "groundingValue",
        "detail_spec": "grounding", "series": None, "unit": None, "provenance": "live",
        "compute": ("pyegeria.view.overview_metrics.semantic_grounding", {}),
        "questions": ["How well grounded is the catalog for AI?"],
        "summary": "SemanticAssignment relationships ÷ the Asset total × 100 (groundingMeasure "
                   "'linksPer100Assets'). Switches to distinct grounded Assets ÷ Assets × 100 "
                   "(groundingMeasure 'assetShare', shown with a %) when the installed pyegeria's "
                   "semantic_grounding returns groundedAssetPct (overview_handler._grounding_fields).",
        "usage": "Not a share of Assets today: one Asset with three terms counts three times, and a "
                 "link to a non-Asset element counts too (confirmed live 2026-08-01: most "
                 "SemanticAssignment links end on GovernanceActionProcess or schema elements, not "
                 "Assets). So the tile shows a plain number with the label 'term links per 100 "
                 "Assets', never a %. Verified 2026-11-10 against the seed spec 'Analytic Demo - "
                 "Semantic Grounding': same function, same value (767 links, 1 per 100 Assets).",
    },
    {
        "key": "ownership", "label": "Ownership Coverage", "icon": "🧑‍💼", "color": "var(--c4)",
        "description": "Share of Assets carrying an Ownership classification — a named "
                       "owner responsible for management/governance decisions. Distinct "
                       "from Governed Coverage (classification-based); data mesh names "
                       "'clean, owned, product-based data' as its own foundation for "
                       "trustworthy AI consumption.",
        "target_type": "Asset", "endpoint": "ai-context", "value_field": "ownershipPct",
        "detail_spec": "ownership", "series": None, "unit": "percent", "provenance": "live",
        "compute": ("MetadataExpert.count_metadata_elements",
                    {"type_name": "Asset", "classifications": ["Ownership"], "strict": True}),
        "questions": ["How much of the catalog has a named, accountable owner?"],
        "summary": "Assets carrying an Ownership classification (strict native count) ÷ all Assets "
                   "(the funnel's Cataloged), both counted in the same population. Same shape as "
                   "Governed Coverage.",
        "usage": "Asset-only on both sides since 2026-11-10 (owner decision). It used to divide a "
                 "find of Ownership-classified elements of ANY type (what the viewer can see) by a "
                 "viewer Asset total, which cannot be counted at this catalogue size (the native "
                 "viewer count times out, the find fallback stops at 500), so the tile never got a "
                 "value. The seed spec 'Analytic Demo - Ownership Coverage' still reports the "
                 "any-type count (with byOwnerType) and no percentage.",
    },
    {
        "key": "ai-ready", "label": "AI-Ready Assets", "icon": "🤖", "color": "var(--c1)",
        "description": "Count of Asset elements that are simultaneously governed, documented, "
                       "and lineage-traced -- the composite gate for \"safe to serve as AI "
                       "context\".",
        "target_type": "Asset", "endpoint": "ai-context", "value_field": "aiReadyPct",
        "detail_spec": "ai-ready", "series": None, "unit": "percent", "provenance": "live",
        "compute": ("pyegeria.view.overview_metrics.ai_ready_assets", {}),
        "questions": ["Which assets are safe to serve as AI context?",
                      "What's the single biggest thing blocking more assets from being AI-ready?"],
        "summary": "Count and percentage of Asset elements carrying >=1 governance "
                   "classification AND a non-empty description AND >=1 DataFlow relationship, "
                   "simultaneously -- a true composite (NEXT-18), not three independent counts.",
        "usage": "The AND-gate means the true bottleneck is whichever underlying signal is "
                 "weakest, and that's very often lineage, not governance or documentation -- "
                 "confirmed live 2026-08-04 on this dataset: 1,743 cataloged, 365 documented "
                 "(21%), 584 classified (governance, not Asset-scoped -- can exceed cataloged, "
                 "see Governed Coverage's own caveat), but only 8 assets carry any DataFlow "
                 "relationship at all, so AI-Ready lands at 4 (0.2%) even though documentation "
                 "and classification are both far higher individually. Read a low number here "
                 "as \"go look at the funnel stage with the steepest drop\" (usually lineage), "
                 "not as \"nothing here is AI-ready-adjacent\" -- see the Context Readiness "
                 "Funnel panel for the per-stage breakdown that explains which gate is binding.",
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
