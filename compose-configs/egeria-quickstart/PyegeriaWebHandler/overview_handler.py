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
    perspective: Optional[str] = Query(None, description="Filter/reorder placements for this perspective"),
):
    """Serve a Container — an ordered, resolved placement list — optionally
    filtered/reordered for a perspective (perspective as a scoped lens over
    placements, see OVERVIEW_REPORTING_MODEL.md §6). Static definitions — no
    Egeria call, no creds required."""
    try:
        from overview_containers import CONTAINERS, container_payload
        container = CONTAINERS.get(name)
        if container is None:
            raise HTTPException(status_code=404, detail=f"Container {name!r} not found")
        return JSONResponse(container_payload(container, perspective))
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

    # Assets by type (best-effort; unknown types yield 0).
    by_type = counts_by_type(mgr, _ASSET_TYPES, as_of_time)
    asset_total = sum(r["count"] for r in by_type)

    term_count = count_elements(mgr, "GlossaryTerm", as_of_time)

    # Vega-Lite bar chart for the assets-by-type composition (real chart —
    # supersedes the hand-drawn SVG bars; see OVERVIEW_REPORTING_MODEL.md P1).
    by_type_chart = generate_vega_bar_chart(
        {r["label"]: r["count"] for r in by_type if r["count"]},
        title="Assets by Type", x_label="Assets", y_label="Type",
    )

    # Data products (DigitalProduct) — live count.
    data_products = count_elements(mgr, "DigitalProduct", as_of_time)

    # Certifications, licenses & open exceptions (governance relationships).
    certs = _certifications(url, server, user_id, user_pwd, as_of_time)

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
        "certifications":   certs["active"],
        "certExpiring90":   certs["expiring90"],
        "certSoon":         certs["soon"],
        "licenses":         certs["licenses"],
        "dataProducts":     data_products,
        "openExceptions":   certs["exceptions"],
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

    readiness = context_readiness_funnel(mgr, as_of_time)

    # Semantic grounding: SemanticAssignment relationships (term ↔ asset) — the
    # meaning layer that grounds AI. Count of assignments as a proxy for grounded links.
    grounding_links = None
    grounding_pct = None
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        grounding = semantic_grounding(mgr, ce, as_of_time)
        grounding_links = grounding["groundingLinks"]
        grounding_pct = grounding["groundingPct"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: grounding query failed: {exc}")

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
        "leaderboard":        None,              # per-person karma rollup — deferred
        "engagementSeries":   None,              # weekly feedback trend — deferred
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
    coverage figure needs graph traversal and is deferred (SPA shows sample)."""
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

    payload = {
        "asOfTime":                as_of_time,
        "informationSupplyChains": iscs,
        "blueprints":              blueprints,
        "contextualisedPct":       None,   # % assets participating in ≥1 ISC/blueprint — TODO (traversal)
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
