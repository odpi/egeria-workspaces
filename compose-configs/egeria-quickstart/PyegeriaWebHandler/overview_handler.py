# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Overview — FastAPI router.

An executive / summary dashboard for the Egeria Portal. Where the other portal
apps (Catalog, Explorer, Lineage, Audit, Insights, Operations) are task-oriented
drill-down tools, this one answers "how are we doing, and is it improving?" at a
glance — scale, governance coverage, quality, AI-readiness, and the people /
community engagement behind the metadata — with every number tied to a business
value lens and drill-through into the owning app.

Design note — the dashboard *is* the Perspective/Question model: a perspective's
questions, each answered by a saved report spec, rendered as a drill-able tile.

Routes:
  GET /egeria-overview            → serve the SPA
  GET /api/overview/summary       → headline KPI counts (capped tally)
  GET /api/overview/ai-context    → AI & context-intelligence readiness (best-effort)
  GET /api/overview/people        → people / community engagement (best-effort)
  GET /api/overview/growth        → catalog growth via asOfTime snapshots (best-effort)

Aggregation reuses the same capped-tally philosophy as insights_handler (Egeria's
find API returns paged element lists with no total-count metadata, so counts are
capped at _DEFAULT_CAP unless full_count paging is requested). Endpoints degrade
gracefully: a field that can't be computed yet is returned as null with
`"partial": true` rather than failing the whole response, so the SPA can overlay
whatever is live over its sample baseline. Results are held in a small in-process
TTL cache (mirroring the operations_handler non-blocking pattern, but simpler —
these queries are seconds, not minutes).

Known constraints (see PYEGERIA_ISSUES.md):
  - No total-count in find responses → capped tallies (cap 500).
  - PY-15: Postgres connector ignores matchCriteria once 2+ classification
    conditions are present → keep every query to 0 or 1 classification.
"""
import os
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from egeria_auth import apply_token

# generate_vega_bar_chart/generate_vega_pie_chart ship with pyegeria (the
# requirements.txt-pinned version has them). generate_vega_line_chart and
# generate_vega_funnel_chart are newer additions not yet on the pinned PyPI
# release — imported defensively so an older pyegeria degrades those two
# chart fields to None instead of crashing the whole app at import time.
# Drop this try/except once requirements.txt's pin includes them.
from pyegeria.view.vega_utilities import generate_vega_bar_chart
try:
    from pyegeria.view.vega_utilities import generate_vega_line_chart, generate_vega_funnel_chart
except ImportError:
    generate_vega_line_chart = None
    generate_vega_funnel_chart = None

# Reusable metric/KPI palette (pyegeria >= 6.0.17.4) — this handler now delegates
# every count/tally computation here and keeps only client construction, caching,
# route wiring and Vega chart assembly local (see overview_metrics.py's module
# docstring for the design boundary).
from pyegeria.view.overview_metrics import (
    WINDOWS as _WINDOWS,
    count_elements,
    count_relationships,
    counts_by_type,
    governed_coverage,
    certifications_summary,
    semantic_grounding,
    context_readiness_funnel,
    people_counts,
    feedback_summary,
    usage_context_counts,
    growth_series,
)

# count_elements_by_property is new (2026-08-17, Data Products deploymentStatus
# breakdown), not yet in a published pyegeria release -- same
# "container runs the published package, not this dev checkout" gap as
# ownership_coverage just below. Defensive import so an older installed
# pyegeria degrades to the old flat count instead of crashing every
# /api/overview/* route.
try:
    from pyegeria.view.overview_metrics import count_elements_by_property
except ImportError:
    count_elements_by_property = None

# contextualised_coverage is new (2026-08-17, "Usage % contextualised"), not
# yet in a published pyegeria release -- same gap as count_elements_by_property
# just above. Defensive import so an older installed pyegeria keeps
# contextualisedPct as the old None/TODO instead of crashing every
# /api/overview/* route.
try:
    from pyegeria.view.overview_metrics import contextualised_coverage
except ImportError:
    contextualised_coverage = None

# karma_leaderboard / engagement_series are new (2026-08-17, People panel's
# leaderboard + engagementSeries -- previously left None as "deferred").
# Same defensive-import gap as above.
try:
    from pyegeria.view.overview_metrics import karma_leaderboard, engagement_series
except ImportError:
    karma_leaderboard = None
    engagement_series = None

# orphan_glossary_terms / stale_assets are new (2026-08-17, Attention Queue's
# "Orphan glossary terms" + "Stale assets" rows). Same defensive-import gap.
try:
    from pyegeria.view.overview_metrics import orphan_glossary_terms, stale_assets
except ImportError:
    orphan_glossary_terms = None
    stale_assets = None

# ownership_coverage is new (2026-08-01), not yet in a published pyegeria release
# (same "container runs the published package, not this dev checkout" gap already
# documented for Create Report/Dashboard Sheet commands in LOCAL_DASHBOARDS_TUTORIAL.md
# — this import crashed the whole app on an installed pyegeria that predates it,
# taking down every /api/overview/* route, not just ai-context). Defensive import,
# matching the vega_utilities pattern just above this block.
try:
    from pyegeria.view.overview_metrics import ownership_coverage
except ImportError:
    ownership_coverage = None


# ai_ready_assets is new (2026-08-01) -- same defensive-import reasoning as
# ownership_coverage above. This is the true composite (governed AND
# documented AND lineage-traced simultaneously) that context_readiness_
# funnel's own aiReady field deliberately still leaves None -- see NEXT-18.
try:
    from pyegeria.view.overview_metrics import ai_ready_assets
except ImportError:
    ai_ready_assets = None

# business_value_signals is new (2026-08-02, NEXT-9) -- same defensive-import
# reasoning as ownership_coverage/ai_ready_assets above.
try:
    from pyegeria.view.overview_metrics import business_value_signals
except ImportError:
    business_value_signals = None

# drl_readiness_gates is new (2026-08-02/03, NEXT-8 §1.9) -- same defensive-
# import reasoning as the three above. Not a full DRL band distribution (see
# its own docstring): a recency-narrowed view of ai_ready_assets plus a
# modality breakdown, until Survey Annotation coverage and a Structural
# Readiness sub-check exist to certify the Analytics-Ready/RAG-Ready rungs.
try:
    from pyegeria.view.overview_metrics import drl_readiness_gates
except ImportError:
    drl_readiness_gates = None

router = APIRouter(tags=["egeria-overview"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-overview.html"

_CACHE_TTL   = 60.0          # seconds; summary is not real-time critical

# Base open-metadata type names for the headline "assets by type" tally. Kept as a
# small, override-safe list — a wrong/unknown type just yields 0 for that row
# rather than failing the response.
_ASSET_TYPES = [
    ("Data Stores",         "DataStore"),
    ("Data Sets",           "DataSet"),
    ("Software Components", "DeployedSoftwareComponent"),
    ("Infrastructure",      "ITInfrastructure"),
    ("APIs",                "DeployedAPI"),
    ("Processes",           "Process"),
]

# ── tiny TTL cache ───────────────────────────────────────────────────────────
_cache: dict[str, tuple[float, Any]] = {}


def _cache_get(key: str):
    hit = _cache.get(key)
    if hit and (time.time() - hit[0]) < _CACHE_TTL:
        return hit[1]
    return None


def _cache_put(key: str, value: Any):
    _cache[key] = (time.time(), value)
    return value


# ── client factory ───────────────────────────────────────────────────────────

def _expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _env(url, server, user_id, user_pwd):
    return (
        url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443"),
        server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id  or os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _make(cls_name, url=None, server=None, user_id=None, user_pwd=None):
    """Build + token any pyegeria client by class name (imported lazily like the
    other handlers). Used for the certification / people / usage-context tallies."""
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    cls = getattr(pyegeria, cls_name)
    url, server, user_id, user_pwd = _env(url, server, user_id, user_pwd)
    mgr = cls(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _norm_asof(s: Optional[str]) -> Optional[str]:
    """Repair an ISO-8601 `asOfTime` whose `+HH:MM` offset arrived as ` HH:MM`
    because a raw `+` in a query string URL-decodes to a space. Clients that use
    URLSearchParams encode it correctly; this guards curl / hand-built URLs so a
    malformed offset doesn't silently degrade every query to null."""
    if not s:
        return s
    import re
    return re.sub(r" (\d{2}:\d{2})$", r"+\1", s.strip())


# ── SPA ──────────────────────────────────────────────────────────────────────

@router.get("/egeria-overview", include_in_schema=False)
def serve_overview():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Overview page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


# ── Tile registry (NEXT-10 P0) ───────────────────────────────────────────────

@router.get("/api/overview/specs",
            summary="Dashboard tile definitions (FormatSet-shaped registry, NEXT-10 P0)")
def get_specs():
    """Serve the single source-of-truth registry of dashboard KPI tiles as
    FormatSet-shaped definitions (see overview_specs.py / OVERVIEW_REPORTING_MODEL.md).
    Static definitions — no Egeria call, no creds required."""
    try:
        from overview_specs import specs_payload
        return JSONResponse(specs_payload())
    except Exception as exc:  # noqa: BLE001
        logger.exception("overview: failed to build tile specs")
        raise HTTPException(status_code=500, detail=f"Spec registry failed: {exc}")


@router.get("/api/overview/container",
            summary="Overview dashboard as a Container of placements (NEXT-10 P2)")
def get_container(
    name: str = Query("overview-dashboard", description="Container name"),
    perspective: Optional[str] = Query(None, description="Filter/reorder placements for this perspective (who — a persona/role)"),
    topic: Optional[str] = Query(None, description="Filter/reorder placements for this topic (what domain of concern — independent of perspective)"),
):
    """Serve a Container — an ordered, resolved placement list — optionally
    filtered/reordered by Perspective and/or Topic, two independent axes
    (Perspective = who, Topic = what domain of concern; see
    overview_specs.py's TOPIC_KPIS docstring and OVERVIEW_REPORTING_MODEL.md
    §6). Static definitions — no Egeria call, no creds required."""
    try:
        from overview_containers import CONTAINERS, container_payload
        container = CONTAINERS.get(name)
        if container is None:
            raise HTTPException(status_code=404, detail=f"Container {name!r} not found")
        return JSONResponse(container_payload(container, perspective, topic))
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("overview: failed to build container payload")
        raise HTTPException(status_code=500, detail=f"Container resolution failed: {exc}")


# ── Summary ──────────────────────────────────────────────────────────────────

@router.get("/api/overview/summary", summary="Headline KPI counts for the Overview dashboard")
def get_summary(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now (time-machine)"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    as_of_time = _norm_asof(as_of_time)
    ckey = f"summary|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.exception("overview: failed to create MetadataExpert")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # Governed tally — single ANY over governance classifications (PY-15 note: this
    # 5-classification ANY is affected by the server bug; still correct at 0/1
    # conditions and used here as a best-effort coverage proxy).
    gov = governed_coverage(mgr, as_of_time)

    # Assets by type (best-effort; unknown types yield 0) — kept purely as the
    # composition breakdown behind the "Assets by Type" chart below; it is
    # NOT summed for the headline total anymore (see asset_total below).
    by_type = counts_by_type(mgr, _ASSET_TYPES, as_of_time)

    # Headline total: the native `Asset` supertype count (OVERVIEW_NEXT_STEPS.md
    # "Asset definition" open decision, resolved 2026-08-16) — one native count
    # call, same population the growth chart's own "assets" series already
    # uses (pyegeria.view.overview_metrics.growth_series' type_map). Used to be
    # a sum of 6 curated type names (via sum_counts/sum_type_counts,
    # BACKLOG.md NEXT-18) which double-undercounted against Asset subtypes not
    # in that list — that mismatch (e.g. live: 2,668 curated-sum vs 2,523
    # Asset-supertype) is exactly what motivated unifying the two here, so the
    # tile's own headline number and its own sparkline finally agree.
    asset_total = count_elements(mgr, "Asset", as_of_time)

    term_count = count_elements(mgr, "GlossaryTerm", as_of_time)

    # Vega-Lite bar chart for the assets-by-type composition (real chart —
    # supersedes the hand-drawn SVG bars; see OVERVIEW_REPORTING_MODEL.md P1).
    by_type_chart = generate_vega_bar_chart(
        {r["label"]: r["count"] for r in by_type if r["count"]},
        title="Assets by Type", x_label="Assets", y_label="Type",
    )

    # Data products (DigitalProduct) — live count, plus a deploymentStatus
    # breakdown (OVERVIEW_NEXT_STEPS.md "Data products publication status +
    # ratings"). deploymentStatus is the property describing whether a
    # product's implementation is deployed/active vs still under development
    # (distinct from contentStatus, the DRAFT->APPROVED lifecycle of the
    # product *description* — see digital_products_handler.py). Folding
    # every other value (DRAFT/UNDER_DEVELOPMENT/unset/etc.) into "not yet
    # active" rather than enumerating every possible deploymentStatus value
    # keeps this to 2 cheap native COUNT calls total, same cost class as the
    # single count this replaces, and stays correct regardless of which
    # status values actually appear in a given dataset.
    data_products = count_elements(mgr, "DigitalProduct", as_of_time)
    data_products_active = None
    if count_elements_by_property is not None:
        try:
            data_products_active = count_elements_by_property(
                mgr, "DigitalProduct", "deploymentStatus", "ACTIVE", as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: data products deploymentStatus breakdown failed: {exc}")
    data_products_pending = (
        max(data_products - data_products_active, 0)
        if data_products is not None and data_products_active is not None else None
    )

    # Ratings — system-wide AttachedRating relationship count (Egeria's
    # relationship count can't be scoped to one end's type without a graph
    # traversal, so this is repo-wide, not products-only; reuses the exact
    # same count_relationships call the People tile already makes
    # independently for its own feedback rollup). Honestly omitted from the
    # tile when zero rather than faked — confirmed live 2026-08-17 that no
    # AttachedRating relationships exist against DigitalProduct in this
    # dataset today.
    ratings_total = None
    ce = None
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        ratings_total = count_relationships(ce, "AttachedRating", as_of_time)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview summary: ratings count failed: {exc}")

    # Certifications, licenses & open exceptions (governance relationships).
    certs = _certifications(url, server, user_id, user_pwd, as_of_time)

    # Business Value tiles (NEXT-9) -- defensive: business_value_signals is
    # new, not yet in a published pyegeria release (see the import above).
    biz_value: dict = {"assetTotal": None, "assetCapped": None, "confidentialCount": None,
                        "describedCount": None, "duplicateCount": None}
    if business_value_signals is not None:
        try:
            biz_value = business_value_signals(mgr, as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: business_value_signals failed: {exc}")

    # Attention Queue rows (NEXT-25): orphan glossary terms + stale assets.
    # Both defensive -- new pyegeria, not yet in a published release.
    orphan_terms: dict = {"termTotal": None, "referencedCount": None, "orphanCount": None}
    if orphan_glossary_terms is not None and ce is not None:
        try:
            orphan_terms = orphan_glossary_terms(mgr, ce, as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: orphan_glossary_terms failed: {exc}")
    stale: dict = {"staleCount": None, "assetTotal": None}
    if stale_assets is not None:
        try:
            stale = stale_assets(mgr, as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: stale_assets failed: {exc}")

    payload = {
        "asOfTime":         as_of_time,
        "assetTotal":       asset_total,
        "byType":           by_type,
        "byTypeChart":      by_type_chart,
        "termCount":        term_count,
        "governedCount":    gov["governedCount"],
        "governedCapped":   gov["governedCapped"],
        "byClassification": gov["byClassification"],
        "topZones":         gov["topZones"],
        "fullyGoverned":    gov["fullyGoverned"],       # ≥1 substantive classification (Confidentiality/Criticality/Impact/Retention)
        "partialZoneOnly":  gov["partialZoneOnly"],     # ZoneMembership only, no substantive classification
        "certifications":   certs["active"],
        "certExpiring90":   certs["expiring90"],
        "certSoon":         certs["soon"],
        "licenses":         certs["licenses"],
        "dataProducts":         data_products,
        "dataProductsActive":   data_products_active,
        "dataProductsPending":  data_products_pending,
        "dataProductsRatings":  ratings_total,
        "openExceptions":   certs["exceptions"],
        "bvAssetTotal":       biz_value["assetTotal"],
        "bvAssetCapped":      biz_value["assetCapped"],
        "bvConfidentialCount": biz_value["confidentialCount"],
        "bvDescribedCount":   biz_value["describedCount"],
        "bvDuplicateCount":   biz_value["duplicateCount"],
        "orphanTermCount":    orphan_terms["orphanCount"],   # SemanticAssignment-unreferenced GlossaryTerms
        "orphanTermTotal":    orphan_terms["termTotal"],
        "staleAssetCount":    stale["staleCount"],           # no update in 180d
        "staleAssetTotal":    stale["assetTotal"],
        "partial":          True,
        "source":           "live:summary",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── certifications & licenses ────────────────────────────────────────────────

def _certifications(url, server, user_id, user_pwd, as_of: Optional[str] = None) -> dict:
    """Build a ClassificationExplorer and delegate to overview_metrics.certifications_summary.
    Degrades to zeros/None on client-build failure (demo may have none)."""
    out = {"active": None, "expiring90": None, "soon": [], "licenses": None, "exceptions": None}
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview certifications: client build failed: {exc}")
        return out
    return certifications_summary(ce, as_of)


# ── AI & Context Intelligence ────────────────────────────────────────────────

@router.get("/api/overview/ai-context", summary="AI / context-intelligence readiness (best-effort)")
def get_ai_context(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Context-readiness funnel + grounding. Consumers/guardrails are not natively
    queryable yet — returned as null so the SPA shows its sample baseline."""
    as_of_time = _norm_asof(as_of_time)
    ckey = f"ai|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: ClassificationExplorer construction failed: {exc}")
        ce = None

    # documented/lineage now computed live (2026-08-01) -- see
    # context_readiness_funnel's own docstring for exactly what each stage
    # means; aiReady is still None (needs a true cross-criteria intersection,
    # tracked under NEXT-18). This is a SIGNATURE change to an existing
    # function (mgr, as_of) -> (mgr, ce, as_of), not a new one -- an older
    # installed pyegeria still has the 2-arg form, so try the new signature
    # first and fall back to the old one on TypeError, rather than letting
    # cataloged/classified (which worked fine before this change) go dark
    # too just because documented/lineage aren't available yet.
    try:
        readiness = context_readiness_funnel(mgr, ce, as_of_time)
    except TypeError:
        try:
            readiness = context_readiness_funnel(mgr, as_of_time)  # pre-2026-08-01 pyegeria
            readiness.setdefault("documented", None)
            readiness.setdefault("lineage", None)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview ai-context: readiness funnel query failed (old signature): {exc}")
            readiness = {"cataloged": None, "documented": None, "classified": None,
                         "lineage": None, "aiReady": None}
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: readiness funnel query failed: {exc}")
        readiness = {"cataloged": None, "documented": None, "classified": None,
                     "lineage": None, "aiReady": None}

    # Semantic grounding: SemanticAssignment relationships (term ↔ asset) — the
    # meaning layer that grounds AI. Count of assignments as a proxy for grounded links.
    grounding_links = None
    grounding_pct = None
    try:
        grounding = semantic_grounding(mgr, ce, as_of_time)
        grounding_links = grounding["groundingLinks"]
        grounding_pct = grounding["groundingPct"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: grounding query failed: {exc}")

    # Ownership coverage: Context Intelligence / NEXT-7 Tier-1 "Capture" signal
    # (OVERVIEW_CONTEXT_INTELLIGENCE.md §2.2) — data-mesh literature names "clean,
    # owned, product-based data" as its own foundation for trustworthy AI
    # consumption, distinct from governance-classification coverage above.
    ownership_count = None
    ownership_pct = None
    try:
        ownership = ownership_coverage(mgr, as_of_time)
        ownership_count = ownership["ownershipCount"]
        total = readiness.get("cataloged")
        if total:
            ownership_pct = round(100 * ownership_count / total, 1)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: ownership query failed: {exc}")

    # True AI-Ready composite (governed AND documented AND lineage-traced
    # simultaneously) — the actual claim the "AI-Ready Assets" tile already
    # makes in its own copy ("governed + documented + lineage"), not three
    # independent counts. First real use of the composite/derived analytic
    # metric pattern (NEXT-18). Feeds both the funnel's aiReady stage and the
    # standalone AI-Ready Assets KPI tile.
    ai_ready_count = None
    ai_ready_pct = None
    try:
        ready = ai_ready_assets(mgr, ce, as_of_time)
        ai_ready_count = ready["aiReadyCount"]
        if ready["total"]:
            ai_ready_pct = round(100 * ai_ready_count / ready["total"], 1)
        readiness["aiReady"] = ai_ready_count
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: ai_ready_assets query failed: {exc}")

    funnel = {
        "Cataloged":       readiness["cataloged"],
        "Documented":      readiness["documented"],
        "Classified":      readiness["classified"],
        "Lineage-traced":  readiness["lineage"],
        "AI-Ready":        readiness["aiReady"],
    }
    # Vega-Lite funnel chart (ordered horizontal bars — Vega-Lite has no native
    # funnel mark). Renders whichever stages are non-null today; gains the
    # deferred stages automatically once they're wired. None on an older
    # pyegeria (see the defensive import at module top).
    funnel_chart = generate_vega_funnel_chart(funnel, title="Context Readiness Funnel") \
        if generate_vega_funnel_chart else None

    # DRL (Data Readiness Level) recency + modality (NEXT-8 §1.9) -- not a full
    # band distribution, see drl_readiness_gates' own docstring for exactly
    # what this is/isn't. None on an older pyegeria (see defensive import above).
    drl_recent_count = None
    drl_recent_pct = None
    drl_by_modality = None
    if drl_readiness_gates is not None:
        try:
            drl = drl_readiness_gates(mgr, ce, as_of_time)
            drl_recent_count = drl["aiReadyRecentCount"]
            if drl["aiReadyCount"]:
                drl_recent_pct = round(100 * drl_recent_count / drl["aiReadyCount"], 1)
            drl_by_modality = drl["byModality"]
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview ai-context: drl_readiness_gates query failed: {exc}")

    payload = {
        "asOfTime":  as_of_time,
        "funnel": {
            "cataloged":  funnel["Cataloged"],
            "documented": funnel["Documented"],
            "classified": funnel["Classified"],
            "lineage":    funnel["Lineage-traced"],
            "aiReady":    funnel["AI-Ready"],
        },
        "funnelChart":     funnel_chart,
        "consumers":       None,         # not natively tracked (MCP/API access logs)
        "guardrails":      None,
        "groundingLinks":  grounding_links,
        "groundingPct":    grounding_pct,
        "ownershipCount":  ownership_count,
        "ownershipPct":    ownership_pct,
        "aiReadyPct":      ai_ready_pct,
        "drlRecentCount":  drl_recent_count,
        "drlRecentPct":    drl_recent_pct,
        "drlByModality":   drl_by_modality,
        "partial":         True,
        "source":          "live:ai-context",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── People & Community ───────────────────────────────────────────────────────

@router.get("/api/overview/people", summary="People / community engagement (best-effort)")
def get_people(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """People counts (persons / teams / orgs / communities) via native element
    counts — one `count_metadata_elements` per type (SELECT COUNT(*)), so this is
    sub-second where the old find-and-bucket approach materialized every profile.
    NB: native counts every entity of the type; the previous ActorManager
    find-and-bucket returned a curated set, so a few totals differ (that raw count
    is the authoritative repository count). Karma / feedback below."""
    as_of_time = _norm_asof(as_of_time)
    ckey = f"people|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    persons = teams = orgs = it_profiles = communities = None
    expert = None
    try:
        expert = _expert(url, server, user_id, user_pwd)
        people = people_counts(expert, as_of_time)
        persons     = people["persons"]
        teams       = people["teams"]
        orgs        = people["organizations"]
        it_profiles = people["itProfiles"]
        communities = people["communities"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: identity counts failed: {exc}")

    # Crowd-sourced feedback — Collaboration OMAS relationship counts (cheap). Often
    # sparse in demo data, but real. Leaderboard/engagement need per-person rollups
    # (deferred). karma = count of ContributionRecord elements.
    feedback_by_type = None
    feedback_items = None
    karma = None
    ce = None
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        fb = feedback_summary(ce, as_of_time)
        feedback_by_type = fb["byType"]
        feedback_items = fb["total"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: feedback query failed: {exc}")
    try:
        if expert is not None:
            karma = count_elements(expert, "ContributionRecord", as_of_time)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: karma query failed: {exc}")

    feedback_chart = generate_vega_bar_chart(
        {k: v for k, v in (feedback_by_type or {}).items() if v},
        title="Feedback by Type", x_label="Items", y_label="Type",
    ) if feedback_by_type else None

    # Leaderboard — per-person karma rollup. Cheap: one bounded find over
    # ContributionRecord elements (already anchored to their owning Person via
    # the standard Anchors classification), no per-person loop.
    leaderboard = None
    if karma_leaderboard is not None and expert is not None:
        try:
            leaderboard = karma_leaderboard(expert, as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview people: karma_leaderboard failed: {exc}")

    # Engagement over time — weekly feedback-event trend. Reuses the same
    # relationship types feedback_summary() already queries, just keeps the
    # createTime instead of only the count.
    engagement_series_data = None
    engagement_chart = None
    if engagement_series is not None and ce is not None:
        try:
            engagement_series_data = engagement_series(ce, as_of_time)
            if generate_vega_line_chart and engagement_series_data:
                engagement_chart = generate_vega_line_chart(
                    engagement_series_data, x_field="week",
                    y_fields=["comments", "ratings", "likes", "tags", "noteLogs"],
                    title="Engagement Over Time", x_label="Week", y_label="Events",
                )
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview people: engagement_series failed: {exc}")

    payload = {
        "asOfTime":           as_of_time,
        "activeContributors": persons,
        "teams":              teams,
        "organizations":      orgs,
        "itProfiles":         it_profiles,
        "communities":        communities,
        "karmaRecords":       karma,             # count of ContributionRecord elements
        "feedbackItems":      feedback_items,    # Σ ratings+comments+likes+tags+noteLogs
        "feedbackByType":     feedback_by_type,
        "feedbackChart":      feedback_chart,
        "leaderboard":        leaderboard,       # per-person karma rollup, top 10
        "engagementSeries":   engagement_series_data,  # weekly feedback trend, 12wk
        "engagementChart":    engagement_chart,
        "partial":            True,
        "source":             "live:people",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── Usage Context — ISC & Blueprints ─────────────────────────────────────────

@router.get("/api/overview/usage-context",
            summary="Information Supply Chains & Solution Blueprints that give assets a usage context")
def get_usage_context(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """ISCs and Blueprints are what put assets in a *usage context* — "this store
    feeds the Clinical Trial supply chain", "this component realises the Sales
    blueprint". Counted natively (count_metadata_elements) — sub-second, vs the old
    find-and-filter that materialized every element. The "% of assets contextualised"
    coverage figure is computed via contextualised_coverage — a single bounded
    ImplementedBy relationship fetch (SolutionComponent -> its concrete
    implementation), not a per-asset graph walk; see that function's own
    docstring for the honest "this is a proxy" caveat (confirms an asset was
    given *some* solution-design context, not that its specific
    SolutionComponent is itself wired into an ISC/blueprint)."""
    as_of_time = _norm_asof(as_of_time)
    ckey = f"usage|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    iscs = blueprints = None
    try:
        mgr = _expert(url, server, user_id, user_pwd)
        usage = usage_context_counts(mgr, as_of_time)
        iscs       = usage["informationSupplyChains"]
        blueprints = usage["blueprints"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview usage-context: query failed: {exc}")

    contextualised_count = asset_total_for_pct = contextualised_pct = None
    if contextualised_coverage is not None:
        try:
            ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
            cov = contextualised_coverage(mgr, ce, as_of_time)
            contextualised_count = cov["contextualisedCount"]
            asset_total_for_pct  = cov["assetTotal"]
            contextualised_pct   = cov["contextualisedPct"]
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview usage-context: contextualised_coverage failed: {exc}")

    payload = {
        "asOfTime":                as_of_time,
        "informationSupplyChains": iscs,
        "blueprints":              blueprints,
        "contextualisedCount":     contextualised_count,
        "contextualisedAssetTotal": asset_total_for_pct,
        "contextualisedPct":       contextualised_pct,
        "partial":                 True,
        "source":                  "live:usage-context",
    }
    return JSONResponse(_cache_put(ckey, payload))


def _is_template_el(el: dict) -> bool:
    for val in (el.get("elementHeader") or {}).values():
        if isinstance(val, dict) and (val.get("classificationName")
                                      or (val.get("type") or {}).get("typeName")) == "Template":
            return True
    return False


# ── Growth (asOfTime snapshots) ──────────────────────────────────────────────

_GROWTH_TTL = 900.0   # 15 min — growth is expensive (N snapshots) and slow-moving


@router.get("/api/overview/growth", summary="Catalog growth via asOfTime snapshots")
def get_growth(
    window: str = Query("6mo", description="8h|1d|3d|7d|30d|90d|6mo|1y"),
    points: Optional[int] = Query(None, ge=2, le=24, description="override #snapshots"),
    months: Optional[int] = Query(None, ge=2, le=12, description="deprecated — use window"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Real growth series: one count per snapshot date with asOfTime set — Egeria
    answers historical queries natively, so no separate time-series store is needed.
    The window sets the span and (by default) the granularity; points can override
    the snapshot count. Snapshots assets / terms / governed / data-products.
    Cached 15 min (this is the expensive endpoint until the count API lands)."""
    if months:                              # back-compat: months → an N*30d window
        window = f"{months * 30}d"

    span_s, default_pts = _WINDOWS.get(window, _WINDOWS["6mo"])
    n = points or default_pts

    ckey = f"growth|{window}|{n}|{url}|{server}|{user_id}"
    hit = _cache.get(ckey)
    if hit and (time.time() - hit[0]) < _GROWTH_TTL:
        return JSONResponse(hit[1])

    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    series = growth_series(mgr, window=window, points=n)

    # Vega-Lite multi-series line chart — supersedes the hand-drawn SVG growth
    # chart once available (needs a newer pyegeria than requirements.txt pins
    # today; see the defensive import at module top). None on an older pyegeria.
    growth_chart = None
    if generate_vega_line_chart and len(series) >= 2:
        growth_chart = generate_vega_line_chart(
            series, x_field="label", y_fields=["assets", "terms", "governed", "products"],
            title="Catalog Growth", x_label="Snapshot", y_label="Count",
        )

    payload = {"series": series, "window": window, "points": n,
               "rangeFrom": series[0]["date"] if series else None,
               "rangeTo": series[-1]["date"] if series else None,
               "growthChart": growth_chart,
               "partial": False, "source": "live:growth"}
    _cache[ckey] = (time.time(), payload)
    return JSONResponse(payload)
