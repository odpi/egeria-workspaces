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
  GET /api/overview/specs         → the tile registry (overview_specs) as JSON (static; no Egeria call)
  GET /api/overview/container     → the Overview dashboard as a Container of placements (static; no Egeria call)
  GET /api/overview/activity      → recent changes to curated content (always "now"; no asOfTime)
  GET /api/overview/usage-context → Information Supply Chains & Solution Blueprints (usage context)

Aggregation reuses the same capped-tally philosophy as insights_handler (Egeria's
find API returns paged element lists with no total-count metadata, so counts are
capped at _DEFAULT_CAP unless full_count paging is requested). Endpoints degrade
gracefully: a field that can't be computed yet is returned as null with
`"partial": true` rather than failing the whole response, so the SPA can overlay
whatever is live over its sample baseline. The slow sections (summary, ai-context,
growth, usage-context: up to ~2 min cold) are measured by background workers and
served from an hourly cache that never blocks a request (see "Background section
cache"); people and activity are fast and keep a short in-request TTL cache.

Known constraints (see PYEGERIA_ISSUES.md):
  - No total-count in find responses → capped tallies (cap 500).
  - PY-15: Postgres connector ignores matchCriteria once 2+ classification
    conditions are present → keep every query to 0 or 1 classification.
"""
import contextvars
from datetime import datetime, timezone
import functools
import inspect
import os
import re
import threading
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from egeria_auth import apply_token, lineage_key
from result_cache import request_identity

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
    GOVERNANCE_CLASSIFICATIONS,
    count_elements,
    count_relationships,
    counts_by_type,
    governed_coverage,
    certifications_summary,
    semantic_grounding,
    context_readiness_funnel,
    people_counts,
    usage_context_counts,
    growth_series,
)

# asset_composition (pyegeria >= 6.2.23): the Asset subtype tree with repository counts. Imported plainly --
# requirements.txt floors pyegeria at the release that has it.
from pyegeria.view.overview_metrics import asset_composition

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

# solution_component_realisation is new (2026-08-27, Solution Blueprints
# drill-down panel's "components"/"realised by" secondary stats -- were
# hardcoded placeholder dashes), not yet in a published pyegeria release --
# same gap as contextualised_coverage just above. Defensive import so an
# older installed pyegeria keeps those two fields None (frontend already
# falls back to '—' when null) instead of crashing every /api/overview/*
# route.
try:
    from pyegeria.view.overview_metrics import solution_component_realisation
except ImportError:
    solution_component_realisation = None

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

# 6.2.28+: the words behind a count that is None. Optional so an older pyegeria still imports.
try:
    from pyegeria.view.overview_metrics import recording_unmeasured
except ImportError:
    recording_unmeasured = None

# ownership_coverage is new (2026-08-01), not yet in a published pyegeria release
# (same "container runs the published package, not this dev checkout" gap already
# documented for Create Report/Dashboard Sheet commands in portal-docs/tutorials/local-dashboards.md
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

# ── tiny TTL cache ───────────────────────────────────────────────────────────
_cache: dict[str, tuple[float, Any]] = {}


def _cache_get(key: Optional[str]):
    """key None = do not use the cache (see _viewer_key: an expired token)."""
    if key is None:
        return None
    hit = _cache.get(key)
    if hit and (time.time() - hit[0]) < _CACHE_TTL:
        return hit[1]
    return None


def _cache_put(key: Optional[str], value: Any):
    if key is not None:
        _cache[key] = (time.time(), value)
    return value


def _viewer_key(prefix: str, url, server, user_id, user_pwd) -> Optional[str]:
    """Cache key for viewer-scoped data: the hashed credential the caller presented
    (result_cache.request_identity), never the bare user_id -- that is None for every token-authenticated
    viewer, so they would all share one entry and see each other's zone-filtered results. None (an
    expired token) means bypass the cache so Egeria refuses the request."""
    who = request_identity(user_id, user_pwd)
    return None if who is None else f"{prefix}|{url}|{server}|{who}"


# ── client factory ───────────────────────────────────────────────────────────

def _expert(url=None, server=None, user_id=None, user_pwd=None, timeout=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    extra = {"timeout": timeout} if timeout is not None else {}
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd, **extra)
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


# ── Count scope (whole repository vs what the viewer can see) ────────────────
#
# Egeria's native count can push the count down to the repository (fast, 0.2-0.8 s at any size) or
# apply per-element visibility (slow, ~100 s for Asset). Owner decision 2026-11-06: the Overview shows
# whole-repository totals to anyone. pyegeria's count helpers take `scope="repository"|"viewer"` from
# the release after 6.2.21; on an older pyegeria the parameter does not exist and every count stays
# viewer-scoped. Support is detected from the signature at run time, never assumed from a version.
#
# One route uses ONE scope for all its native counts, and a ratio never mixes scopes: a numerator that
# comes from a find (always viewer-scoped) is only ever divided by a viewer-scoped total.

REPOSITORY = "repository"
VIEWER = "viewer"
_SCOPE_SUPPORT: dict = {}


def _accepts_scope(fn) -> bool:
    """True if `fn` takes a `scope` parameter. Cached per function object."""
    if fn not in _SCOPE_SUPPORT:
        try:
            _SCOPE_SUPPORT[fn] = "scope" in inspect.signature(fn).parameters
        except (TypeError, ValueError):
            _SCOPE_SUPPORT[fn] = False
    return _SCOPE_SUPPORT[fn]


def _count_scope(*fns) -> str:
    """The scope a route's native counts will actually use: repository only if EVERY helper the
    route calls supports it, otherwise viewer for all of them (never a mix inside one payload)."""
    return REPOSITORY if fns and all(_accepts_scope(f) for f in fns) else VIEWER


def _default_population(fn) -> str:
    """The population `fn` counts when no scope is passed, read from its signature (never a version).

    Every count call in this module passes its population explicitly; this is only for the helpers that
    cannot be told one -- context_readiness_funnel and semantic_grounding take no scope. They count in
    pyegeria's default population: since the totals change (pyegeria 6.2.27, owner decision 2026-11-08) that
    is the whole repository, the default of count_elements' scope; before it they reached the server's
    default, which counts what the viewer can see. So `_default_population(count_elements)` names theirs."""
    try:
        param = inspect.signature(fn).parameters.get("scope")
    except (TypeError, ValueError):
        return VIEWER
    return REPOSITORY if param is not None and param.default == REPOSITORY else VIEWER


def _scoped(fn, scope: str, **extra):
    """`fn` with `scope="repository"` (plus any `extra` kwargs) bound when requested and supported;
    otherwise `fn` unchanged. count_relationships needs `expert=<MetadataExpert>` for a scope to apply
    (repository scope without it returns None, i.e. not measured)."""
    if scope == REPOSITORY and _accepts_scope(fn):
        return functools.partial(fn, scope=REPOSITORY, **extra)
    return fn


# Collaboration relationship types behind the People tile's feedback tally (same set and keys as
# pyegeria's overview_metrics.feedback_summary, which folds a failed count to 0).
_FEEDBACK_RELATIONSHIPS = (
    ("AttachedRating", "ratings"), ("AttachedComment", "comments"), ("AttachedLike", "likes"),
    ("AttachedTag", "tags"), ("AttachedNoteLog", "noteLogs"),
)


def _feedback_counts(ce, as_of: Optional[str] = None, count_rel=None) -> dict:
    """Feedback tally where a count that could not be read is None, not 0.

    pyegeria's feedback_summary does `count_relationships(...) or 0`, so a failed query reads as "no
    feedback". Here each type is None when unmeasured, and `total` is None unless every type was
    measured -- a sum over a subset is a lower bound, not a total."""
    count_rel = count_rel or count_relationships
    by_type = {key: count_rel(ce, rel, as_of) for rel, key in _FEEDBACK_RELATIONSHIPS}
    unmeasured = [k for k, v in by_type.items() if v is None]
    total = None if unmeasured else sum(by_type.values())
    return {"byType": by_type, "total": total, "unmeasured": unmeasured}


_SUBSTANTIVE_GOVERNANCE = tuple(c for c in GOVERNANCE_CLASSIFICATIONS if c != "ZoneMembership")


def _governed_asset_counts(count_fn, mgr, as_of: Optional[str] = None):
    """(governed, fully governed) Asset counts, both taken through the SAME bound `count_fn` so the
    numerator and denominator of Governed Coverage always share one scope (the denominator, the Asset
    total, is taken through that same function by the caller)."""
    return (count_fn(mgr, "Asset", as_of, classifications=GOVERNANCE_CLASSIFICATIONS, strict=True),
            count_fn(mgr, "Asset", as_of, classifications=_SUBSTANTIVE_GOVERNANCE, strict=True))


def _asset_scoped_governed(gov: dict, governed: Optional[int], fully: Optional[int]) -> dict:
    """Governed Coverage is an Assets-only share (owner decision 2026-11-06).

    `governed` = Assets carrying at least one of the five governance classifications; `fully` = Assets
    carrying at least one of the four substantive ones (everything but ZoneMembership). Both are strict
    native counts, so they are exact (never a capped lower bound) or None. The zone-only share is the
    difference. `gov` (pyegeria's governed_coverage) contributes only byClassification / topZones, which
    stay element-wide (any type) and are labelled so by the page."""
    out = dict(gov)
    out["governedCount"] = governed
    out["governedCapped"] = False if governed is not None else None
    out["fullyGoverned"] = fully
    out["partialZoneOnly"] = (governed - fully) if governed is not None and fully is not None and governed >= fully else None
    return out


def _reconcile_business_value(bv: dict, asset_total: Optional[int], duplicate_count: Optional[int]) -> dict:
    """Make business_value_signals honest about a failed find.

    Its Asset find returns [] on failure, which it reports as assetTotal=0 and confidential/described=0.
    The strict Asset count (`asset_total`) is the independent check: if the find came back empty but the
    catalog is not known to be empty, the per-asset figures were not measured. The duplicate count is the
    caller's strict one, replacing pyegeria's non-strict value."""
    out = dict(bv)
    out["duplicateCount"] = duplicate_count
    if out.get("assetTotal") == 0 and asset_total != 0:
        out.update(assetTotal=None, assetCapped=None, confidentialCount=None, describedCount=None)
    return out


def _strict_funnel_counts(readiness: dict, mgr, as_of: Optional[str] = None, scope: Optional[str] = None) -> dict:
    """Re-measure the funnel's Cataloged/Classified stages strictly, in `scope` (the funnel's own
    population, see _compute_ai_context), passed explicitly whenever count_elements takes it.

    pyegeria's context_readiness_funnel returns `count or None`, turning a measured 0 into null (and a
    failed count into 0 first). A measured 0 must stay 0 and a failure must stay None."""
    n = functools.partial(count_elements, scope=scope) if scope and _accepts_scope(count_elements) else count_elements
    out = dict(readiness)
    out["cataloged"] = n(mgr, "Asset", as_of, strict=True)
    out["classified"] = n(mgr, None, as_of, classifications=GOVERNANCE_CLASSIFICATIONS, strict=True)
    return out


# ── Background viewer Asset count ────────────────────────────────────────────
#
# Under repository scope the Asset headline is whole-catalog, so the survey % and schema % (find numerators,
# viewer-scoped) need a count of the Assets THIS user can see. That count reads every Asset (~100 s), so it
# is never taken inside a request. Same non-blocking pattern as operations_handler.py's report cache:
#   cold    -> start one background worker, answer at once with value=None, loading=True
#   fresh   -> the cached value (1 hour TTL; the page shows how old it is)
#   stale   -> the cached value flagged stale, refreshed in the background
#   failed  -> None is cached for _VIEWER_TOTAL_FAIL_TTL only, then retried ("not measured" until then)
# One worker per key (url|server|user|as_of: the value is per viewer, Egeria filters by zone), and at most
# ONE worker counting across all users (_viewer_gate): each count reads every Asset and Egeria's database
# pool is 10 connections.
#
# These routes are sync `def` (they run in the threadpool), and pyegeria's count helpers are sync and call
# run_until_complete internally, so the worker is a plain thread with its OWN client, not an asyncio Task
# (an async Task or an executor on the main loop would hit "event loop already running"). The request's
# contextvars (bearer token, forLineage) are copied into the worker so it counts as the same viewer.

_VIEWER_TOTAL_TTL = 60 * 60          # seconds a measured value stays fresh (owner 2026-11-06: refresh ~hourly)
_VIEWER_TOTAL_FAIL_TTL = 60          # seconds before a failed/timed-out count is retried
_VIEWER_TOTAL_TIMEOUT = 240          # client timeout for this one count (the default is shorter than ~100 s+)
_viewer_totals: dict = {}            # key -> (expires_at, value-or-None, counted_at)
_viewer_inflight: dict = {}          # key -> Thread
_viewer_lock = threading.Lock()      # makes check-and-start atomic: at most one worker per key
_viewer_gate = threading.Semaphore(1)   # global cap: one viewer Asset count at a time, across all users


def _viewer_count(mgr, as_of: Optional[str]) -> Optional[int]:
    """Strict viewer-scoped Asset count (None if it failed or timed out)."""
    if _accepts_scope(count_elements):
        return count_elements(mgr, "Asset", as_of, strict=True, scope=VIEWER)
    return count_elements(mgr, "Asset", as_of, strict=True)


def _viewer_total_worker(key, url, server, user_id, user_pwd, as_of):
    value = None
    try:
        with _viewer_gate:
            mgr = _expert(url, server, user_id, user_pwd, timeout=_VIEWER_TOTAL_TIMEOUT)
            value = _viewer_count(mgr, as_of)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview: viewer Asset count failed: {exc}")
        value = None
    finally:
        ttl = _VIEWER_TOTAL_TTL if value is not None else _VIEWER_TOTAL_FAIL_TTL
        with _viewer_lock:
            now = time.time()
            _viewer_totals[key] = (now + ttl, value, now)
            _viewer_inflight.pop(key, None)


def _viewer_total_state(url, server, user_id, user_pwd, as_of):
    """(value, loading, stale, counted_at) for this viewer's Asset count; starts a background count if none is fresh.

    Never blocks. value is None when not (yet) measured; loading means a count is running and the
    caller should ask again; stale means value is the previous measurement, being refreshed;
    counted_at is the epoch time the value was measured (None if never measured)."""
    u, sv, uid, pwd = _env(url, server, user_id, user_pwd)
    who = request_identity(user_id, user_pwd)   # was uid: the env service user for EVERY token-authenticated viewer
    if who is None:
        return None, False, False, None         # expired token: not measured (the rest of the page shows the 401)
    key = f"{u}|{sv}|{who}|{as_of}"
    with _viewer_lock:                 # no await/IO between the check and the start
        hit = _viewer_totals.get(key)
        fresh = hit is not None and hit[0] > time.time()
        if not fresh and key not in _viewer_inflight:
            ctx = contextvars.copy_context()
            t = threading.Thread(target=ctx.run, daemon=True, name="overview-viewer-total",
                                 args=(_viewer_total_worker, key, url, server, user_id, user_pwd, as_of))
            _viewer_inflight[key] = t
            t.start()
        value = hit[1] if hit else None
    if hit is None or (value is None and not fresh):
        return None, True, False, None
    return value, False, (value is not None and not fresh), (hit[2] if value is not None else None)


def _overlay_viewer_total(payload: dict, url, server, user_id, user_pwd, as_of) -> dict:
    """Fill the viewer-scoped Asset total fields on a (possibly cached) summary payload.

    Viewer scope: assetTotal already is the viewer total, no second count. Repository scope: the viewer
    total comes from the background count; it is used only as the denominator of find-based percentages."""
    out = dict(payload)
    if out.get("countScope") == REPOSITORY:
        value, loading, stale, counted_at = _viewer_total_state(url, server, user_id, user_pwd, as_of)
        out.update(assetTotalViewer=value, assetTotalViewerLoading=loading, assetTotalViewerStale=stale,
                   assetTotalViewerAsOf=(datetime.fromtimestamp(counted_at, timezone.utc).isoformat()
                                         if counted_at is not None else None))
    else:
        out.update(assetTotalViewer=out.get("assetTotal"), assetTotalViewerLoading=False,
                   assetTotalViewerStale=False,
                   assetTotalViewerAsOf=None)
    return out


# ── Background section cache ─────────────────────────────────────────────────
#
# summary (~2 min cold), ai-context (~2 min), growth (~1 min) and usage-context (~40 s) spend their time in
# find/search calls, so a cold request used to block for minutes and a client with a 60 s timeout got
# nothing. Same non-blocking pattern as the viewer Asset count above, one entry per section key:
#   cold     -> start one background worker, answer at once with {"loading": true} and NO data fields
#   fresh    -> the cached payload (_SECTION_TTL, hourly; the page shows how old it is)
#   stale    -> the cached payload flagged "stale", refreshed in the background
#   failed   -> no new attempt for _SECTION_FAIL_TTL; a previous payload (if any) is still served as stale,
#               otherwise the route answers 503 "not measured" (never a zero-filled payload)
#   partial  -> a payload whose headline value could not be measured is served but re-measured after
#               _SECTION_PARTIAL_TTL instead of an hour
# The key is section|url|server|population|args (+ lineage_key(): forLineage changes which elements are found).
# population (see _section_key) is either "repository" -- the section's figures are whole-repository native
# counts, identical for every viewer, so no identity is in the key and there is nothing to forge -- or the
# viewer's hashed credential (result_cache.request_identity), because the section's find calls are filtered by
# zone access. Never the token's `sub`: it is read unverified, and a hit makes no Egeria call to check it.
# At most _SECTION_WORKERS sections compute at once across all users (_section_gate): a page load asks for
# four sections, and Egeria's database pool is 10 connections. Workers are plain threads with copied
# contextvars, for the same reason as _viewer_total_worker.

_SECTION_TTL = 60 * 60               # seconds a measured section stays fresh (owner 2026-11-06: hourly)
_SECTION_PARTIAL_TTL = 5 * 60        # a payload missing its headline value is re-measured sooner
_SECTION_FAIL_TTL = 60               # back-off before a failed measurement is retried
_SECTION_WORKERS = 2                 # global cap on sections computing at once
_SECTION_MAX_KEYS = 256              # bound on remembered keys (time-machine dates make many)
_sections: dict = {}                 # key -> {"payload", "measured_at", "fresh_until", "retry_at", "error"}
_section_inflight: dict = {}         # key -> Thread
_section_lock = threading.Lock()     # makes check-and-start atomic: at most one worker per key
_section_gate = threading.Semaphore(_SECTION_WORKERS)


# Which population each section's cached payload describes (checked 2026-11-09 against pyegeria 6.2.29):
#   composition    REPOSITORY -- asset_composition(scopes=(REPOSITORY,)); the viewer column is overlaid per
#                  request from the per-viewer Asset count (_viewer_total_state), never cached with the payload.
#   growth         REPOSITORY when growth_series counts the whole repository by default (6.2.27+), else viewer.
#   summary        viewer -- besides native counts it holds find-based figures (survey coverage, governed
#                  byClassification / topZones, business-value signals), and on a pyegeria without repository
#                  scope every count is viewer-scoped.
#   ai-context     viewer -- the ownership count is a find; the readiness funnel is viewer-scoped before 6.2.27.
#   usage-context  viewer -- the "% contextualised" coverage is a relationship fetch the viewer's zones filter.
def _growth_population() -> str:
    try:
        param = inspect.signature(growth_series).parameters.get("population")
    except (TypeError, ValueError):
        return VIEWER
    return REPOSITORY if param is not None and param.default == REPOSITORY else VIEWER


def _section_key(section: str, *args, population: str, url=None, server=None, user_id=None,
                 user_pwd=None) -> Optional[str]:
    """Cache key for one background section. population=REPOSITORY: no identity at all (the figures are the
    same for every viewer). Otherwise the viewer's hashed credential; None for an expired token, which the
    route turns into a 401 (see _section_key_or_401) rather than starting a minutes-long build to be refused."""
    u, sv, _, _ = _env(url, server, user_id, user_pwd)
    if population == REPOSITORY:
        who = REPOSITORY
    else:
        who = request_identity(user_id, user_pwd)
        if who is None:
            return None
    return "|".join([section, u, sv, who, *(str(a) for a in args)]) + lineage_key()


def _section_key_or_401(section: str, *args, **kw) -> str:
    key = _section_key(section, *args, **kw)
    if key is None:
        raise HTTPException(status_code=401, detail="Egeria token expired; sign in again")
    return key


def _iso(epoch: Optional[float]) -> Optional[str]:
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat() if epoch is not None else None


def _prune_sections(now: float) -> None:
    """Drop the least recently measured idle keys once there are too many (caller holds _section_lock)."""
    extra = len(_sections) - _SECTION_MAX_KEYS
    if extra <= 0:
        return
    idle = sorted((k for k in _sections if k not in _section_inflight),
                  key=lambda k: _sections[k].get("measured_at") or 0)
    for k in idle[:extra]:
        _sections.pop(k, None)


def _section_worker(key, compute, ok):
    payload, error = None, None
    try:
        with _section_gate:
            payload = compute()
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"overview: section {key.split('|', 1)[0]} failed: {exc}")
        error = str(exc) or type(exc).__name__
    finally:
        now = time.time()
        with _section_lock:
            prev = _sections.get(key) or {}
            if payload is not None:
                try:
                    whole = bool(ok(payload))
                except Exception:  # noqa: BLE001
                    whole = False
                ttl = _SECTION_TTL if whole else _SECTION_PARTIAL_TTL
                _sections[key] = {"payload": payload, "measured_at": now, "fresh_until": now + ttl,
                                  "retry_at": now + ttl, "error": None}
            else:                       # keep any previous measurement (served as stale); back off the retry
                _sections[key] = {"payload": prev.get("payload"), "measured_at": prev.get("measured_at"),
                                  "fresh_until": prev.get("fresh_until", 0), "retry_at": now + _SECTION_FAIL_TTL,
                                  "error": error or "no result"}
            _section_inflight.pop(key, None)
            _prune_sections(now)


def _section_fetch(key: str, compute, ok=lambda p: True):
    """(payload-or-None, meta) for one section key; starts a background measurement when none is fresh.

    Never blocks on Egeria. meta carries loading (nothing measured yet, a worker is running: ask again),
    stale (payload is an older measurement, past its TTL), refreshing (a worker is re-measuring it),
    measuredAt (ISO time the payload was measured), refreshSeconds (the TTL) and error (the last failure,
    while no worker is running)."""
    now = time.time()
    with _section_lock:                # no IO between the check and the start
        e = _sections.get(key)
        payload = e.get("payload") if e else None
        fresh = payload is not None and e["fresh_until"] > now
        running = key in _section_inflight
        if not fresh and not running and (e is None or e["retry_at"] <= now):
            ctx = contextvars.copy_context()
            t = threading.Thread(target=ctx.run, daemon=True, name="overview-section",
                                 args=(_section_worker, key, compute, ok))
            _section_inflight[key] = t
            t.start()
            running = True
        meta = {
            "loading":        payload is None and running,
            "stale":          payload is not None and not fresh,
            "refreshing":     payload is not None and running,
            "measuredAt":     _iso(e.get("measured_at")) if payload is not None else None,
            "refreshSeconds": _SECTION_TTL,
            "error":          (e.get("error") if e and not running else None),
        }
    return payload, meta


def _section_unready(section: str, meta: dict):
    """The answer when a section has no measurement to serve: loading (200, no data fields) or failed (503)."""
    if meta.get("loading"):
        return JSONResponse({"loading": True, "source": f"live:{section}", **meta})
    raise HTTPException(status_code=503,
                        detail=f"Not measured: {section} failed ({meta.get('error')}); retried within "
                               f"{_SECTION_FAIL_TTL} s")


# ── Asset composition ────────────────────────────────────────────────────────
#
# One routine (pyegeria asset_composition) returns the Asset subtype tree with a count per type. The Overview
# asks it for the REPOSITORY population only (owner decision, design note 9.23: the Overview shows catalog-wide
# totals to anyone, fast, ~3 s for ten counts). The viewer population is never counted here: a viewer count of
# Process takes ~120 s. The one viewer figure on offer is the Asset total, read from the hourly per-viewer
# cache above, and per-type viewer cells say so instead of showing a number. "not visible to you" is derived
# (repository - viewer) and only where both operands are measured. A failed count is never a 0.

COMPOSITION_DEPTH_MAX = 3
_VIEWER_TOTAL_ONLY = "viewer counts are refreshed hourly; only the total is cached"


def _composition_cell(value, state, reason, population, completeness="unknown", as_of=None) -> dict:
    return {"value": value, "state": state, "completeness": completeness, "as_of": as_of,
            "population": population, "reason": reason, "elapsed_s": None}


def _compute_composition(root, depth, as_of_time, url, server, user_id, user_pwd) -> dict:
    """Repository-scope asset_composition for `root`; runs in a background worker (never in the request)."""
    vm = _make("ValidMetadataManager", url, server, user_id, user_pwd)
    mgr = _expert(url, server, user_id, user_pwd)
    return asset_composition(mgr, vm, root=root, depth=depth, as_of=as_of_time, scopes=(REPOSITORY,))


def _viewer_cell_for_root(viewer: tuple) -> dict:
    value, loading, stale, counted_at = viewer
    if value is None:
        return _composition_cell(None, "not_measured",
                                 "being counted for you now (can take a couple of minutes)" if loading
                                 else "the count of assets you can see did not complete", VIEWER)
    return _composition_cell(value, "measured" if value else "nothing_found",
                             "counted earlier and refreshed hourly" + (" (refreshing)" if stale else ""),
                             VIEWER, as_of=_iso(counted_at))


def _not_visible_cell(repo: dict, viewer: dict) -> dict:
    rv, vv = repo.get("value"), viewer.get("value")
    if repo.get("state") not in ("measured", "nothing_found") or viewer.get("state") not in ("measured", "nothing_found") \
            or rv is None or vv is None:
        return _composition_cell(None, "not_measured", "needs both the repository and the viewer count", "derived")
    if vv > rv:      # the two counts were taken at different times; a negative difference is not a count
        return _composition_cell(None, "not_measured",
                                 "the viewer count is higher than the repository count (counted at different times)",
                                 "derived")
    return _composition_cell(rv - vv, "measured" if rv - vv else "nothing_found",
                             f"repository count minus the count of assets you can see "
                             f"(viewer counted {viewer.get('as_of') or 'earlier'})", "derived", completeness="unknown")


def _composition_view(result: dict, viewer: Optional[tuple]) -> dict:
    """The routine's result with the viewer column filled: the Asset total from the hourly cache, every other
    row 'not measured, only the total is cached'. Rows are otherwise the routine's own (type_name, parent,
    level, exact_type, repository, viewer, not_visible)."""
    out = dict(result)
    rows = []
    for row in result.get("rows", []):
        row = dict(row)
        if row.get("level") == 0 and viewer is not None:
            row["viewer"] = _viewer_cell_for_root(viewer)
        else:
            row["viewer"] = _composition_cell(None, "not_measured", _VIEWER_TOTAL_ONLY, VIEWER)
        row["not_visible"] = _not_visible_cell(row.get("repository") or {}, row["viewer"])
        rows.append(row)
    out["rows"] = rows
    out["scopes"] = [REPOSITORY, VIEWER]
    return out


def _level1_rows(result: dict) -> list:
    """The direct-subtype rows (plus each 'other' row) of a composition result, repository cell flattened."""
    out = []
    for r in result.get("rows", []):
        if r.get("level") != 1:
            continue
        cell = r.get("repository") or {}
        label = f"{r['type_name']} (exactly)" if r.get("exact_type") else r["type_name"]
        out.append({"label": label, "type": r["type_name"], "exactType": bool(r.get("exact_type")),
                    "count": cell.get("value"), "state": cell.get("state"), "reason": cell.get("reason")})
    return out


@router.get("/api/overview/composition",
            summary="Asset composition by subtype (repository totals; viewer total only)")
def get_composition(
    root: str = Query("Asset", description="Type whose subtypes are counted; a click on a bar re-queries with it"),
    depth: int = Query(1, ge=0, le=COMPOSITION_DEPTH_MAX),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now (time-machine)"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    """Served from the background section cache (cold -> {"loading": true}); see "Asset composition" above.

    countScope is always "repository". viewerCounts is "total-only": the Asset total of the viewer column comes
    from the hourly per-viewer cache (and only when root is Asset), every other viewer cell is not_measured."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    as_of_time = _norm_asof(as_of_time)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", root):
        raise HTTPException(status_code=422, detail="root must be an open metadata type name")
    key = _section_key_or_401("composition", root, depth, as_of_time, population=REPOSITORY,
                              url=url, server=server, user_id=user_id, user_pwd=user_pwd)
    payload, meta = _section_fetch(
        key, functools.partial(_compute_composition, root, depth, as_of_time, url, server, user_id, user_pwd),
        ok=lambda p: p.get("state") == "measured" and not p.get("not_measured"))
    if payload is None:
        return _section_unready("composition", meta)
    viewer = _viewer_total_state(url, server, user_id, user_pwd, as_of_time) if root == "Asset" else None
    view = _composition_view(payload, viewer)
    return JSONResponse({**view, "countScope": REPOSITORY, "viewerCounts": "total-only",
                         "viewerTotalLoading": bool(viewer and viewer[1]), "source": "live:composition", **meta})


# ── Summary ──────────────────────────────────────────────────────────────────

@router.get("/api/overview/summary", summary="Headline KPI counts for the Overview dashboard")
def get_summary(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now (time-machine)"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    """Served from the background section cache (see "Background section cache"); computed by _compute_summary."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    as_of_time = _norm_asof(as_of_time)
    key = _section_key_or_401("summary", as_of_time, population=VIEWER,
                              url=url, server=server, user_id=user_id, user_pwd=user_pwd)
    payload, meta = _section_fetch(
        key, functools.partial(_compute_summary, as_of_time, url, server, user_id, user_pwd),
        ok=lambda p: p.get("assetTotal") is not None)
    if payload is None:
        return _section_unready("summary", meta)
    # assetTotalViewer* are filled per request by _overlay_viewer_total (never cached with the payload, so a
    # background count that finishes is seen on the next poll without recomputing the whole summary).
    return JSONResponse({**_overlay_viewer_total(payload, url, server, user_id, user_pwd, as_of_time), **meta})


def _compute_summary(as_of_time, url, server, user_id, user_pwd) -> dict:
    """Every Egeria call behind the summary (~2 min cold, mostly find calls). Runs in a background worker."""
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.exception("overview: failed to create MetadataExpert")
        raise RuntimeError(f"Connection failed: {exc}") from exc

    # Governed tally — single ANY over governance classifications (PY-15 note: this
    # 5-classification ANY is affected by the server bug; still correct at 0/1
    # conditions and used here as a best-effort coverage proxy).
    # Every native count in this payload shares ONE scope (see "Count scope" above): the Governed share,
    # the donut, Assets by Type's "Other" remainder and Data Products' pending count are all ratios or
    # differences of these counts, so they must not mix repository- and viewer-scoped values.
    scope = _count_scope(count_elements, counts_by_type, count_relationships,
                         *([count_elements_by_property] if count_elements_by_property else []))
    n_elements = _scoped(count_elements, scope)
    n_relationships = _scoped(count_relationships, scope, expert=mgr)
    n_by_property = _scoped(count_elements_by_property, scope) if count_elements_by_property else None

    gov = governed_coverage(mgr, as_of_time)
    gov = _asset_scoped_governed(gov, *_governed_asset_counts(n_elements, mgr, as_of_time))

    # Headline total: the native `Asset` supertype count (OVERVIEW_NEXT_STEPS.md
    # "Asset definition" open decision, resolved 2026-08-16) — one native count
    # call, same population the growth chart's own "assets" series already
    # uses (pyegeria.view.overview_metrics.growth_series' type_map). Used to be
    # a sum of 6 curated type names (via sum_counts/sum_type_counts,
    # BACKLOG.md NEXT-18) which double-undercounted against Asset subtypes not
    # in that list — that mismatch (e.g. live: 2,668 curated-sum vs 2,523
    # Asset-supertype) is exactly what motivated unifying the two here, so the
    # tile's own headline number and its own sparkline finally agree.
    asset_total = n_elements(mgr, "Asset", as_of_time, strict=True)

    # Assets by type: the direct subtypes of Asset from the composition routine (repository counts, plus an
    # "(exactly)" row for plain Asset elements). A count that failed is None, never 0; the chart leaves it out
    # and the page says "not measured".
    by_type = []
    try:
        by_type = _level1_rows(_compute_composition("Asset", 1, as_of_time, url, server, user_id, user_pwd))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview summary: asset composition failed: {exc}")

    term_count = n_elements(mgr, "GlossaryTerm", as_of_time, strict=True)

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
    data_products = n_elements(mgr, "DigitalProduct", as_of_time, strict=True)
    data_products_active = None
    if n_by_property is not None:
        try:
            data_products_active = n_by_property(
                mgr, "DigitalProduct", "deploymentStatus", "ACTIVE", as_of_time, strict=True)
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
        ratings_total = n_relationships(ce, "AttachedRating", as_of_time)
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
            biz_value = _reconcile_business_value(
                _scoped(business_value_signals, scope)(mgr, as_of_time), asset_total,
                n_elements(mgr, None, as_of_time, classifications=["ConsolidatedDuplicate"], strict=True))
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
    stale_note = None   # why staleCount is None (e.g. the 500-element page cap), from pyegeria's note
    if stale_assets is not None:
        try:
            if recording_unmeasured is not None:
                with recording_unmeasured() as _notes:
                    stale = stale_assets(mgr, as_of_time)
                _why = [n.get("reason") for n in _notes if n.get("reason") and "not updated" in str(n.get("count", ""))]
                stale_note = "; ".join(_why) if _why else None
            else:
                stale = stale_assets(mgr, as_of_time)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: stale_assets failed: {exc}")

    # Survey coverage (Data Quality "Surveyed", Attention Queue "never surveyed"): one
    # ReportSubject relationship page + two counts. Needs the relationships client.
    survey: dict = {"surveyedAssets": None, "dataStoreTotal": None, "surveyedStores": None,
                    "neverSurveyedStores": None, "surveyReports": None, "surveyLinksCapped": None,
                    "qualityAnnotatedAssets": None, "annotationsByType": None,
                    "surveysCompleted": None, "surveysFailed": None, "surveysUnknown": None,
                    "assetsSurveyFailedOnly": None, "latestSurveyTime": None,
                    "surveysCompleted7d": None, "dataStoresByKind": None}
    if ce is not None:
        try:
            survey = _survey_coverage(mgr, ce, as_of_time, asset_total, scope=scope)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview summary: survey coverage failed: {exc}")
    schema = _schema_coverage(mgr, as_of_time, survey.get("schemaAnalysedGuids"))
    engine_health = _engine_action_health(url, server, user_id, user_pwd, as_of_time)
    confidentiality = _confidentiality_levels(mgr, as_of_time)
    technology = _assets_by_technology(mgr, as_of_time)

    payload = {
        "asOfTime":         as_of_time,
        "viewServer":       _env(url, server, user_id, user_pwd)[1],   # the Egeria view server queried (page header)
        "assetTotal":       asset_total,
        # Which scope every native count in this payload used: "repository" = the whole catalog (fast),
        # "viewer" = only what the signed-in user can see. The page labels the tiles with it.
        "countScope":       scope,
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
        "surveyedAssets":     survey["surveyedAssets"],
        "latestSurveyTime":   survey["latestSurveyTime"],
        "surveysCompleted7d": survey["surveysCompleted7d"],
        "dataStoresByKind":   survey["dataStoresByKind"],
        "assetsByTechnology":      technology["technologies"],
        "technologyUnrecorded":    technology["unrecorded"],
        "technologyPlaceholders":  technology["placeholders"],
        "technologyAssetTotal":    technology["total"],
        "engineActionHealth": engine_health,
        "surveysCompleted":   survey["surveysCompleted"],
        "surveysFailed":      survey["surveysFailed"],
        "surveysUnknown":     survey["surveysUnknown"],
        "assetsSurveyFailedOnly": survey["assetsSurveyFailedOnly"],
        "qualityAnnotatedAssets": survey["qualityAnnotatedAssets"],
        "annotationsByType":  survey["annotationsByType"],
        "assetsWithSchema":   schema["assetsWithSchema"],
        "schemaAnalysedAssets": schema["schemaAnalysedAssets"],
        "schemaTypes":        schema["schemaTypes"],
        "confidentialityLevels":     confidentiality["levels"],
        "confidentialityClassified": confidentiality["classified"],
        "confidentialityCapped":     confidentiality["capped"],
        "dataStoreTotal":     survey["dataStoreTotal"],
        "surveyedStores":     survey["surveyedStores"],
        "neverSurveyedStores": survey["neverSurveyedStores"],
        "surveyReports":      survey["surveyReports"],
        "surveyLinksCapped":  survey["surveyLinksCapped"],
        "staleAssetCount":    stale["staleCount"],           # no update in 180d
        "staleAssetTotal":    stale["assetTotal"],
        "staleAssetNote":     stale_note if stale["staleCount"] is None else None,  # why the count is "—"
        "partial":          True,
        "source":           "live:summary",
    }
    return payload


# ── certifications & licenses ────────────────────────────────────────────────

# Egeria's default Confidentiality levels (0-4); a deployment may define others, shown as "Level N".
_CONFIDENTIALITY_LABELS = {0: "Unclassified", 1: "Internal", 2: "Confidential", 3: "Sensitive", 4: "Restricted"}


def _classification_props(el: dict, name: str) -> Optional[dict]:
    for c in (el.get("classifications") or []):
        if c.get("classificationName") == name:
            pv = c.get("classificationProperties") or {}
            return pv.get("propertiesAsStrings") or pv
    return None


def _confidentiality_levels(mgr, as_of: Optional[str] = None) -> dict:
    """Distribution of the Confidentiality classification by level (one capped find). Every field is
    None when the query failed, so "nothing classified" (a real zero) and "could not ask" differ."""
    out = {"levels": None, "classified": None, "capped": None}
    try:
        body = {"class": "FindRequestBody", "metadataElementTypeName": "OpenMetadataRoot",
                "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0,
                "pageSize": _SURVEY_LINK_CAP,
                "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ANY",
                                         "conditions": [{"name": "Confidentiality"}]}}
        if as_of:
            body["asOfTime"] = as_of
        found = mgr.find_metadata_elements(body)
        found = [e for e in (found if isinstance(found, list) else []) if isinstance(e, dict)]
        counts: dict = {}
        for e in found:
            props = _classification_props(e, "Confidentiality")
            if props is None:
                continue
            try:
                lvl = int(props.get("confidentialityLevel"))
            except (TypeError, ValueError):
                lvl = -1
            counts[lvl] = counts.get(lvl, 0) + 1
        out["levels"] = [{"level": l, "label": _CONFIDENTIALITY_LABELS.get(l, f"Level {l}" if l >= 0 else "Unspecified"),
                          "count": c} for l, c in sorted(counts.items())]
        out["classified"] = sum(counts.values())
        out["capped"] = len(found) >= _SURVEY_LINK_CAP
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview confidentiality levels failed: {exc}")
    return out


def _assets_by_technology(mgr, as_of: Optional[str] = None) -> dict:
    """Assets grouped by the technology they record in `deployedImplementationType`. Most assets do not
    record one, so the figures are exclusive and add up to the asset total: each technology, the assets
    that record none (`unrecorded`), and template placeholders such as ``~{deployedImplementationType}~``
    (`placeholders`: template elements carry the unfilled name, which is not a technology). Read in pages
    until an empty one (Egeria's paging contract); every field is None when a page failed or
    _REL_MAX_PAGES full pages were read without reaching the end (a capped read can only under-count)."""
    out = {"technologies": None, "unrecorded": None, "placeholders": None, "total": None}
    try:
        counts: dict = {}
        unrecorded = placeholders = total = 0
        done = False
        for page in range(_REL_MAX_PAGES):
            body = {"class": "FindRequestBody", "metadataElementTypeName": "Asset",
                    "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                    "startFrom": page * _SURVEY_LINK_CAP, "pageSize": _SURVEY_LINK_CAP}
            if as_of:
                body["asOfTime"] = as_of
            chunk = mgr.find_metadata_elements(body)
            chunk = [e for e in (chunk if isinstance(chunk, list) else []) if isinstance(e, dict)]
            if not chunk:
                done = True
                break
            for e in chunk:
                total += 1
                props = e.get("elementProperties") or {}
                tech = str((props.get("propertiesAsStrings") or props).get("deployedImplementationType") or "").strip()
                if not tech:
                    unrecorded += 1
                elif tech.startswith("~{") and tech.endswith("}~"):
                    placeholders += 1
                else:
                    counts[tech] = counts.get(tech, 0) + 1
        if done:
            out.update(technologies=counts, unrecorded=unrecorded, placeholders=placeholders, total=total)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview assets by technology failed: {exc}")
    return out


def _schema_coverage(mgr, as_of: Optional[str] = None, analysed=None) -> dict:
    """How many elements have a schema: the distinct anchors of SchemaType elements (a schema's anchor is
    the asset it describes) UNION the assets a survey analysed the schema of (SchemaAnalysisAnnotation --
    surveys record a database's schema as annotations, not as SchemaType elements). Read in pages until an
    empty one (Egeria's paging contract); None when a page failed or _REL_MAX_PAGES full pages were read
    without reaching the end (a capped read can only under-count)."""
    out = {"assetsWithSchema": None, "schemaTypes": None, "schemaCapped": None, "schemaAnalysedAssets": None}
    analysed = set(analysed or [])
    try:
        found, capped = [], True
        for page in range(_REL_MAX_PAGES):
            body = {"class": "FindRequestBody", "metadataElementTypeName": "SchemaType",
                    "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                    "startFrom": page * _SURVEY_LINK_CAP, "pageSize": _SURVEY_LINK_CAP}
            if as_of:
                body["asOfTime"] = as_of
            chunk = mgr.find_metadata_elements(body)
            chunk = [e for e in (chunk if isinstance(chunk, list) else []) if isinstance(e, dict)]
            if not chunk:
                capped = False
                break
            found.extend(chunk)
        anchors = set()
        for e in found:
            props = _classification_props(e, "Anchors")
            g = (props or {}).get("anchorGUID")
            if g:
                anchors.add(g)
        out["schemaTypes"] = len(found)
        out["schemaCapped"] = capped
        out["assetsWithSchema"] = None if out["schemaCapped"] else len(anchors | analysed)
        out["schemaAnalysedAssets"] = len(analysed - anchors)   # assets whose schema is known only from a survey
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview schema coverage failed: {exc}")
    return out


# ── Recent activity (changes to curated content) ────────────────────────────
# Egeria's most-recently-updated elements are dominated by connector churn here (one catalog refresh
# rewrote ~10,000 elements in 20 minutes), so a plain "latest changes" scan says nothing about what
# people curate. Activity is therefore read per CURATED content type, and the payload names the types.
_ACTIVITY_TYPES = ["GlossaryTerm", "Collection", "GovernanceDefinition", "Project"]
_ACTIVITY_WINDOW_D = 7
_ACTIVITY_RECENT_H = 48
_ACTIVITY_PAGE = 200
_ACTIVITY_MAX_PAGES = 5      # per type: 1000 most recent; a type still inside the window after that is a lower bound
_ACTIVITY_STREAM = 12
_ACTIVITY_STEWARDS = 5


def _looks_automated(user) -> bool:
    """Heuristic: Egeria's own service accounts end in "npa" (non-person account) or are engines."""
    u = str(user or "").lower()
    return u.endswith("npa") or "engine" in u


def _element_label(e: dict) -> str:
    props = e.get("elementProperties") or {}
    props = props.get("propertiesAsStrings") or props
    return str(props.get("displayName") or props.get("name") or props.get("qualifiedName") or "(unnamed)")


def _recent_changes(mgr, now=None) -> Optional[dict]:
    """Changes to curated content in the last _ACTIVITY_WINDOW_D days, from each type's most-recently-updated
    elements (read in pages until one is older than the window). None if any query failed (a half-read
    list must not pass for the whole). `capped` is True when some type was still inside the window after
    _ACTIVITY_MAX_PAGES pages, which makes the counts a lower bound."""
    import datetime as _dt
    now = now or _dt.datetime.utcnow()
    cutoff = now - _dt.timedelta(days=_ACTIVITY_WINDOW_D)
    recent_cut = now - _dt.timedelta(hours=_ACTIVITY_RECENT_H)
    changes: dict = {}
    capped = False
    try:
        for tname in _ACTIVITY_TYPES:
            reached = False
            for page in range(_ACTIVITY_MAX_PAGES):
                chunk = mgr.find_metadata_elements({
                    "class": "FindRequestBody", "metadataElementTypeName": tname,
                    "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                    "sequencingOrder": "LAST_UPDATE_RECENT",
                    "startFrom": page * _ACTIVITY_PAGE, "pageSize": _ACTIVITY_PAGE})
                chunk = [e for e in (chunk if isinstance(chunk, list) else []) if isinstance(e, dict)]
                if not chunk:
                    reached = True
                    break
                for e in chunk:
                    v = e.get("versions") or {}
                    when = _parse_time(v.get("updateTime"))
                    if when is None:
                        continue
                    if when < cutoff:
                        reached = True
                        break
                    guid = _guid_of(e)
                    if guid and guid not in changes:
                        changes[guid] = {"time": when, "actor": v.get("updatedBy") or "", "version": v.get("version"),
                                         "type": (e.get("type") or {}).get("typeName") or tname,
                                         "name": _element_label(e), "guid": guid}
                if reached:
                    break
            if not reached:
                capped = True
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview recent activity failed: {exc}")
        return None
    rows = sorted(changes.values(), key=lambda c: c["time"], reverse=True)
    by_type: dict = {}
    stewards: dict = {}
    automated = 0
    for c in rows:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
        if _looks_automated(c["actor"]):
            automated += 1
        elif c["actor"]:
            stewards[c["actor"]] = stewards.get(c["actor"], 0) + 1
    # The stream is people's changes: automation (a subscription manager rewriting notification types every
    # few minutes) would otherwise fill it and hide everything a person did. It is counted, not listed.
    in_recent = [c for c in rows if c["time"] >= recent_cut]
    recent = [{"time": c["time"].isoformat(), "actor": c["actor"], "type": c["type"], "name": c["name"],
               "guid": c["guid"], "action": "created" if c["version"] == 1 else "updated", "automated": False}
              for c in in_recent if not _looks_automated(c["actor"])][:_ACTIVITY_STREAM]
    recent_automated = sum(1 for c in in_recent if _looks_automated(c["actor"]))
    return {"types": list(_ACTIVITY_TYPES), "windowDays": _ACTIVITY_WINDOW_D, "recentHours": _ACTIVITY_RECENT_H,
            "total": len(rows), "automated": automated, "people": len(rows) - automated, "capped": capped,
            "byType": by_type,
            "stewards": sorted(stewards.items(), key=lambda kv: (-kv[1], kv[0]))[:_ACTIVITY_STEWARDS],
            "recent": recent, "recentAutomated": recent_automated}


@router.get("/api/overview/activity", summary="Recent changes to curated content")
def get_activity(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    """Change stream, activity by type and most active stewards for curated content types (glossary terms,
    collections/products, governance definitions, projects). Always "now": Egeria's asOfTime cannot
    say who changed what. `activity` is None when a query failed -- the page then shows "Not measured"."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    ckey = _viewer_key("activity", url, server, user_id, user_pwd)
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)
    activity = None
    try:
        activity = _recent_changes(_expert(url, server, user_id, user_pwd))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview activity: client build failed: {exc}")
    return JSONResponse(_cache_put(ckey, {"activity": activity, "source": "live:activity"}))


_SURVEY_LINK_CAP = 1000   # one relationship page / one find page; a result at the cap is a lower bound, reported as such


def _type_names(end: dict) -> set:
    t = (end or {}).get("type") or {}
    return {t.get("typeName")} | set(t.get("superTypeNames") or [])


def _guid_of(el: dict) -> Optional[str]:
    return el.get("elementGUID") or (el.get("elementHeader") or {}).get("guid") or el.get("guid")


_REL_PAGE_SIZE = 1000   # one relationship page
_REL_MAX_PAGES = 10     # read at most this many pages; beyond that the result is a lower bound


def _relationship_rows(ce, relationship_type: str, as_of: Optional[str] = None):
    """Every link of one relationship type, read in pages. Returns (rows, capped), or (None, None) if
    any page failed (partial rows are discarded: a half-read list must not pass for the whole).

    Egeria's paging contract: a short page is NOT the last page, only an empty page is, so this keeps
    reading until it gets one. If _REL_MAX_PAGES full pages are read without reaching an empty page the
    rows are a lower bound and capped=True, so callers can withhold figures a lower bound would corrupt.
    This matters for ReportedAnnotation: Egeria 6.2 reuses survey annotations (one annotation can be
    reported by many reports), and every report links every annotation it reports, so the link count
    grows with each survey even when no new annotation is created.
    """
    rows: list = []
    try:
        body = {"class": "ResultsRequestBody", "asOfTime": as_of} if as_of else None
        for page in range(_REL_MAX_PAGES):
            raw = ce.get_relationships(relationship_type=relationship_type, output_format="JSON",
                                       start_from=page * _REL_PAGE_SIZE, page_size=_REL_PAGE_SIZE, body=body)
            chunk = raw if isinstance(raw, list) else ((raw or {}).get("elements") or [] if isinstance(raw, dict) else [])
            if not chunk:
                return rows, False
            rows.extend(chunk)
        return rows, True
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview {relationship_type} relationship read failed: {exc}")
        return None, None


def _survey_outcome(props: dict) -> str:
    """Classify one SurveyReport as 'completed', 'failed' or 'unknown' from its own properties.

    Two kinds of report exist on the platform and record the outcome differently:
      * engine-run surveys ("Survey Report for <asset guid>") carry a completionMessage whose id says
        what happened: OMES-SURVEY-ACTION-0019 "has completed the analysis ..." or
        OMES-SURVEY-ACTION-0018 "... threw a ... exception". A failed survey still writes a report
        (and whatever findings it got to) before it throws, so a report existing proves nothing.
      * reports created by other tools ("Survey: <name>") carry error_count in additionalProperties:
        0 is a clean run, more is a run that hit errors.
    Anything else is 'unknown': it is never counted as a success.
    """
    msg = props.get("completionMessage") or ""
    if msg:
        if msg.startswith("OMES-SURVEY-ACTION-0019") or "has completed the analysis" in msg:
            return "completed"
        if msg.startswith("OMES-SURVEY-ACTION-0018") or " threw " in msg:
            return "failed"
        return "unknown"
    m = re.search(r"error_count=(\d+)", props.get("additionalProperties") or "")
    if m:
        return "completed" if int(m.group(1)) == 0 else "failed"
    return "unknown"


def _parse_time(value):
    """A timestamp as a naive-UTC datetime, or None. Egeria hands them out as ISO strings
    ("2026-10-04T15:49:02", sometimes with a Z or fractional seconds) or as epoch milliseconds
    (propertiesAsStrings gives "1791127622579"); anything else is None, never a guess."""
    import datetime as _dt
    if value in (None, ""):
        return None
    try:
        if isinstance(value, (int, float)) or str(value).strip().lstrip("-").isdigit():
            n = float(value)
            if n > 1e11:       # epoch milliseconds
                n /= 1000.0
            elif n < 1e9:      # too small to be a modern epoch
                return None
            return _dt.datetime.utcfromtimestamp(n)
        txt = str(value).strip().replace("Z", "").replace(" ", "T")
        if "+" in txt[10:]:
            txt = txt[: 10 + txt[10:].index("+")]
        return _dt.datetime.fromisoformat(txt)
    except (ValueError, OverflowError, OSError):
        return None


_ENGINE_ACTION_PAGE = 500          # find_engine_actions page; reaching it makes the window counts a lower bound
_ENGINE_ACTION_WINDOW_H = 24


def _engine_action_health(url=None, server=None, user_id=None, user_pwd=None,
                          as_of: Optional[str] = None, client=None, now=None):
    """Outcome of the Egeria engine actions (survey runs, scheduled insight jobs, ...) requested in the
    last 24 hours, read with one find_engine_actions page.

      {"total", "completed", "failed", "inProgress", "other", "topFailing": [[requestType, n], ...],
       "capped"}

    None when the actions could not be read, and None when a past as-of time is asked for: the engine
    action list is the current state, so showing it beside as-of figures would mix time bases. "capped"
    means the page was full, so every count is a lower bound (the list is unordered, the newest actions
    may be missing). Actions whose request time cannot be parsed are left out of the window rather than
    guessed into it.
    """
    if as_of:
        return None
    import datetime as _dt
    try:
        ac = client if client is not None else _make("AutomatedCuration", url, server, user_id, user_pwd)
        raw = ac.find_engine_actions(search_string="*", page_size=_ENGINE_ACTION_PAGE, output_format="JSON")
        items = [i for i in (raw if isinstance(raw, list) else []) if isinstance(i, dict)]
        cutoff = (now or _dt.datetime.utcnow()) - _dt.timedelta(hours=_ENGINE_ACTION_WINDOW_H)
        counts = {"total": 0, "completed": 0, "failed": 0, "inProgress": 0, "other": 0}
        failing: dict = {}
        for it in items:
            props = it.get("properties") or it.get("elementProperties") or {}
            props = props.get("propertiesAsStrings") or props
            when = _parse_time(props.get("requestedStartTime")) or _parse_time(props.get("startTime"))
            if when is None or when < cutoff:
                continue
            status = str(props.get("activityStatus") or "").upper()
            counts["total"] += 1
            if status == "COMPLETED":
                counts["completed"] += 1
            elif status == "FAILED":
                counts["failed"] += 1
                rt = props.get("requestType") or props.get("governanceActionTypeName") or "(unknown)"
                failing[rt] = failing.get(rt, 0) + 1
            elif status == "IN_PROGRESS":
                counts["inProgress"] += 1
            else:
                counts["other"] += 1
        counts["topFailing"] = [[k, v] for k, v in sorted(failing.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
        counts["capped"] = len(items) >= _ENGINE_ACTION_PAGE
        return counts
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview engine action health failed: {exc}")
        return None


def _survey_outcomes(mgr, as_of: Optional[str] = None, times: Optional[dict] = None):
    """{SurveyReport guid: outcome} from one bounded find, or None if it failed (an unclassifiable
    report must not be assumed successful). If `times` is given it is filled with
    {guid: createTime string} from the same page, for survey freshness."""
    try:
        body = {"class": "FindRequestBody", "metadataElementTypeName": "SurveyReport",
                "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0,
                "pageSize": _SURVEY_LINK_CAP}
        if as_of:
            body["asOfTime"] = as_of
        found = mgr.find_metadata_elements(body)
        found = [e for e in (found if isinstance(found, list) else []) if isinstance(e, dict)]
        out = {}
        for e in found:
            g = _guid_of(e)
            if g:
                props = ((e.get("elementProperties") or {}).get("propertiesAsStrings")) or {}
                out[g] = _survey_outcome(props)
                if times is not None:
                    times[g] = (e.get("versions") or {}).get("createTime") or ""
        return out
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview survey outcomes failed: {exc}")
        return None


def _survey_coverage(mgr, ce, as_of: Optional[str] = None, asset_total: Optional[int] = None,
                     scope: str = REPOSITORY) -> dict:
    """How much of the catalog has been successfully surveyed, and how many surveys failed.

    A SurveyReport is linked to the asset it describes by a ReportSubject relationship
    (AssetSurveyReport, the older name, has none on the live platform). ReportSubject also
    links ConnectorActivityReports to their connectors, so only links whose report end is a
    SurveyReport count. Everything comes from a few bounded calls, never a per-asset fan-out:
    the SurveyReports (for their outcome), one ReportSubject page, one ReportedAnnotation page,
    and one find of the DataStore guids to intersect with.

    Coverage counts COMPLETED surveys only (see _survey_outcome): a survey that failed still wrote a
    report and partial findings, and must not make an asset look surveyed.

      surveyedAssets       distinct subjects of completed SurveyReports (any Asset type)
      surveyedStores       those that are DataStores
      neverSurveyedStores  DataStore total - surveyedStores
      surveysCompleted / surveysFailed / surveysUnknown   report counts by outcome
      assetsSurveyFailedOnly   subjects that have failed surveys and no completed one
      qualityAnnotatedAssets / annotationsByType / schemaAnalysedGuids   from completed surveys only

    Every field is None when its own step failed, never 0: a failed query must not read as
    "nothing surveyed". neverSurveyedStores is also None when a page hit its cap, since a capped
    page can only under-count what was surveyed.
    """
    out = {"assetTotal": asset_total, "surveyedAssets": None, "surveyReports": None,
           "dataStoreTotal": None, "surveyedStores": None, "neverSurveyedStores": None,
           "surveyLinksCapped": None, "qualityAnnotatedAssets": None, "annotationsByType": None,
           "schemaAnalysedGuids": None, "surveysCompleted": None, "surveysFailed": None,
           "surveysUnknown": None, "assetsSurveyFailedOnly": None, "latestSurveyTime": None,
           "surveysCompleted7d": None, "dataStoresByKind": None}
    try:
        # the summary payload's population (`scope`, its countScope), passed explicitly; a lone figure, no ratio.
        # strict: a repository count that cannot be taken is None -- non-strict, pyegeria <= 6.2.26 gives 0.
        out["surveyReports"] = _scoped(count_elements, scope)(mgr, "SurveyReport", as_of, strict=True)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview survey coverage: SurveyReport count failed: {exc}")

    times: dict = {}
    outcomes = _survey_outcomes(mgr, as_of, times)
    if outcomes is not None:
        vals = list(outcomes.values())
        out["surveysCompleted"] = vals.count("completed")
        out["surveysFailed"] = vals.count("failed")
        out["surveysUnknown"] = vals.count("unknown")
        # Freshness of the COMPLETED surveys: newest one, and how many in the 7 days before now (or
        # before the as-of time). A report whose time cannot be parsed is left out, not guessed.
        import datetime as _dt
        ref = _parse_time(as_of) if as_of else _dt.datetime.utcnow()
        stamped = [(t, g) for g, o in outcomes.items() if o == "completed"
                   for t in [_parse_time(times.get(g))] if t is not None]
        if stamped:
            out["latestSurveyTime"] = max(stamped)[0].isoformat()
        if ref is not None:
            out["surveysCompleted7d"] = sum(1 for t, _ in stamped if ref - _dt.timedelta(days=7) <= t <= ref)

    subjects = None            # subjects of COMPLETED reports
    failed_only = None
    links_capped = None
    subject_of_report: dict = {}   # SurveyReport guid -> the asset it describes
    if outcomes is not None:
        try:
            rels, rels_capped = _relationship_rows(ce, "ReportSubject", as_of)
            if rels is None:
                raise RuntimeError("ReportSubject links could not be read")
            subjects, with_failure = set(), set()
            for r in rels:
                if not isinstance(r, dict):
                    continue
                e1, e2 = r.get("end1") or {}, r.get("end2") or {}
                if "SurveyReport" in _type_names(e1):
                    subject, report_end = e2, e1
                elif "SurveyReport" in _type_names(e2):
                    subject, report_end = e1, e2
                else:
                    continue          # e.g. a ConnectorActivityReport link
                sg, rg = subject.get("guid"), report_end.get("guid")
                if not sg or not rg:
                    continue
                outcome = outcomes.get(rg, "unknown")
                if outcome == "completed":
                    subjects.add(sg)
                    subject_of_report[rg] = sg
                elif outcome == "failed":
                    with_failure.add(sg)
            failed_only = with_failure - subjects
            links_capped = rels_capped
            out["surveyedAssets"] = len(subjects)
            out["assetsSurveyFailedOnly"] = len(failed_only)
            out["surveyLinksCapped"] = links_capped
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview survey coverage: ReportSubject query failed: {exc}")
            subjects = None

    # Annotations the COMPLETED surveys produced: ReportedAnnotation links a SurveyReport to each
    # Annotation. "Has quality annotations" = survey subjects whose report carries at least one
    # QualityAnnotation.
    if subjects is not None:
        try:
            arels, a_capped = _relationship_rows(ce, "ReportedAnnotation", as_of)
            if arels is None:
                raise RuntimeError("ReportedAnnotation links could not be read")
            # Distinct annotations per type: with annotation reuse (Egeria 6.2) the same annotation is linked
            # from every report that found it, so counting links would count it once per report.
            by_type: dict = {}
            quality_reports: set = set()
            schema_reports: set = set()
            for r in arels:
                if not isinstance(r, dict):
                    continue
                e1, e2 = r.get("end1") or {}, r.get("end2") or {}
                if "SurveyReport" in _type_names(e1):
                    rep_end, ann = e1, e2
                elif "SurveyReport" in _type_names(e2):
                    rep_end, ann = e2, e1
                else:
                    continue
                if rep_end.get("guid") not in subject_of_report:
                    continue          # a failed / unknown survey's partial findings do not count
                tname = ((ann.get("type") or {}).get("typeName")) or "Annotation"
                by_type.setdefault(tname, set()).add(ann.get("guid") or id(ann))
                if "QualityAnnotation" in _type_names(ann) and rep_end.get("guid"):
                    quality_reports.add(rep_end["guid"])
                if "SchemaAnalysisAnnotation" in _type_names(ann) and rep_end.get("guid"):
                    schema_reports.add(rep_end["guid"])
            if not a_capped:
                out["annotationsByType"] = {t: len(g) for t, g in by_type.items()}
                out["qualityAnnotatedAssets"] = len({subject_of_report[g] for g in quality_reports if g in subject_of_report})
                out["schemaAnalysedGuids"] = sorted({subject_of_report[g] for g in schema_reports if g in subject_of_report})
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview survey coverage: ReportedAnnotation query failed: {exc}")

    store_guids = None
    stores_capped = None
    try:
        find_body = {"class": "FindRequestBody", "metadataElementTypeName": "DataStore",
                     "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                     "startFrom": 0, "pageSize": _SURVEY_LINK_CAP}
        if as_of:
            find_body["asOfTime"] = as_of
        found = mgr.find_metadata_elements(find_body)
        found = [e for e in (found if isinstance(found, list) else []) if isinstance(e, dict)]
        store_guids = {g for g in (_guid_of(e) for e in found) if g}
        stores_capped = len(found) >= _SURVEY_LINK_CAP
        # capped find: the native count, in the summary's population (neverSurveyedStores needs an uncapped find)
        out["dataStoreTotal"] = (_scoped(count_elements, scope)(mgr, "DataStore", as_of, strict=True) if stores_capped
                                 else len(store_guids))
        if not stores_capped:
            kinds: dict = {}
            for e in found:
                k = (e.get("type") or {}).get("typeName") or "Other"
                kinds[k] = kinds.get(k, 0) + 1
            out["dataStoresByKind"] = kinds
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview survey coverage: DataStore find failed: {exc}")

    if subjects is not None and store_guids is not None:
        out["surveyedStores"] = len(subjects & store_guids)
        total = out["dataStoreTotal"]
        if total is not None and not links_capped and not stores_capped and out["surveyedStores"] <= total:
            out["neverSurveyedStores"] = total - out["surveyedStores"]
    return out


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
    user_id: Optional[str] = Query(None),
):
    """Context-readiness funnel + grounding. Consumers/guardrails are not natively
    queryable yet — returned as null so the SPA shows its sample baseline."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    as_of_time = _norm_asof(as_of_time)
    key = _section_key_or_401("ai-context", as_of_time, population=VIEWER,
                              url=url, server=server, user_id=user_id, user_pwd=user_pwd)
    payload, meta = _section_fetch(
        key, functools.partial(_compute_ai_context, as_of_time, url, server, user_id, user_pwd),
        ok=lambda p: (p.get("funnel") or {}).get("cataloged") is not None)
    if payload is None:
        return _section_unready("ai-context", meta)
    return JSONResponse({**payload, **meta})


def _owned_asset_share(mgr, as_of, population: str, cataloged: Optional[int]):
    """(owned Assets, % of Cataloged) -- Ownership Coverage, the same shape as Governed Coverage.

    The numerator is a strict native count of Assets carrying an Ownership classification, taken in the
    SAME population as `cataloged` (the funnel's strict Asset count), so the ratio never mixes a viewer
    count with a repository one. Either count unmeasured (None) -> the % is None, never a guess."""
    n = functools.partial(count_elements, scope=population) if _accepts_scope(count_elements) else count_elements
    try:
        owned = n(mgr, "Asset", as_of, classifications=("Ownership",), strict=True)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: owned-Asset count failed: {exc}")
        owned = None
    pct = (round(100 * owned / cataloged, 1)
           if owned is not None and cataloged and owned <= cataloged else None)
    return owned, pct


def _display_round(v):
    """One decimal under 10 (1.36 -> 1.4, not 1), whole numbers from 10 up. None stays None."""
    if v is None:
        return None
    return round(v, 1) if abs(v) < 10 else round(v)


def _links_per_100(grounding: dict, cataloged: Optional[int], population: Optional[str]):
    """SemanticAssignment links ÷ Assets × 100, unrounded, or pyegeria's whole-number groundingPct.

    Recomputed from groundingLinks and the funnel's Cataloged only when the funnel counts the whole
    repository -- the population semantic_grounding counts both of its numbers in (6.2.27+) -- so the
    ratio never mixes populations. Otherwise pyegeria's own figure is used as it is."""
    links = grounding.get("groundingLinks")
    if population == REPOSITORY and links is not None and cataloged:
        return 100 * links / cataloged
    return grounding.get("groundingPct")


def _grounding_fields(grounding: Optional[dict], cataloged: Optional[int] = None,
                      population: Optional[str] = None) -> dict:
    """What the Semantic Grounding tile shows, labelled by what it measures.

    pyegeria 6.2.30's semantic_grounding returns groundingLinks (SemanticAssignment relationships) and
    groundingPct = links ÷ Asset total × 100. That is NOT a share of Assets: one Asset with three terms
    counts three times, and a link to a non-Asset element counts too. So it is reported as "links per 100
    Assets" (groundingMeasure "linksPer100Assets") and groundingPct -- the share -- stays None.

    TODO(pyegeria next release): semantic_grounding is to report distinct grounded Assets as
    `groundedAssets` (int) and `groundedAssetPct` (groundedAssets ÷ its own Asset total × 100). The
    feature check below switches the tile to that real share (groundingMeasure "assetShare") as soon as an
    installed pyegeria returns it; no Portal change is needed then.

    Values for display are rounded by _display_round: one decimal under 10 (767 links over 56,357 Assets
    is 1.4 per 100, not "1")."""
    g = grounding or {}
    per100 = _display_round(_links_per_100(g, cataloged, population))
    share = _display_round(g.get("groundedAssetPct"))
    if share is not None:
        return {"groundingMeasure": "assetShare", "groundingValue": share, "groundingPct": share,
                "groundedAssets": g.get("groundedAssets"), "groundingLinks": g.get("groundingLinks"),
                "groundingLinksPer100": per100}
    return {"groundingMeasure": "linksPer100Assets", "groundingValue": per100, "groundingPct": None,
            "groundedAssets": None, "groundingLinks": g.get("groundingLinks"),
            "groundingLinksPer100": per100}


def _compute_ai_context(as_of_time, url, server, user_id, user_pwd) -> dict:
    """Every Egeria call behind ai-context (~2 min cold). Runs in a background worker."""
    # The funnel, its strict re-count and grounding take no scope here, so they count pyegeria's default
    # population: the whole repository from 6.2.27, what the viewer can see before it.
    population = _default_population(count_elements)
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Connection failed: {exc}") from exc

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

    # Semantic grounding: SemanticAssignment relationships (term ↔ element) — the meaning layer that grounds
    # AI. See _grounding_fields: today it is links per 100 Assets, never shown as a share of Assets.
    grounding = None
    try:
        grounding = semantic_grounding(mgr, ce, as_of_time)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: grounding query failed: {exc}")

    # Ownership coverage: Context Intelligence / NEXT-7 Tier-1 "Capture" signal
    # (OVERVIEW_CONTEXT_INTELLIGENCE.md §2.2) — data-mesh literature names "clean,
    # owned, product-based data" as its own foundation for trustworthy AI
    # consumption, distinct from governance-classification coverage above.
    # Same shape as Governed Coverage (owner decision 2026-11-10): owned ASSETS, a strict native count in the
    # funnel's own population, over the funnel's Cataloged (that same count's Asset total). Always measurable
    # -- it used to divide a viewer find (any element type) by a viewer Asset total that cannot be counted at
    # this catalogue size, so the tile never got a value. Computed after the strict funnel re-count below.

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
        # a funnel stage only in a viewer funnel: ai_ready_assets is a find (what the viewer can see), so it
        # is not a stage of a whole-repository funnel; it stays in the payload as aiReadyCount (viewer)
        if population == VIEWER:
            readiness["aiReady"] = ai_ready_count
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: ai_ready_assets query failed: {exc}")

    readiness = _strict_funnel_counts(readiness, mgr, as_of_time, scope=population)
    ownership_count, ownership_pct = _owned_asset_share(mgr, as_of_time, population, readiness.get("cataloged"))
    grounding_fields = _grounding_fields(grounding, readiness.get("cataloged"), population)

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
        # The population of the funnel's counts and grounding. On a pyegeria whose totals count the whole
        # repository (6.2.27+), funnel and grounding are repository counts, and the two find-based figures
        # below (ownership, AI-Ready) are viewer-scoped: they are reported on their own, never divided by a
        # repository total and never drawn as a funnel stage. Older pyegeria: everything is viewer, as before.
        "countScope": population,
        "aiReadyCount":    ai_ready_count,
        "aiReadyScope":    VIEWER,       # ai_ready_assets is a find
        "ownershipScope":  population,   # owned Assets ÷ Cataloged: both strict counts in the funnel's population
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
        **grounding_fields,
        "ownershipCount":  ownership_count,
        "ownershipPct":    ownership_pct,
        "aiReadyPct":      ai_ready_pct,
        "drlRecentCount":  drl_recent_count,
        "drlRecentPct":    drl_recent_pct,
        "drlByModality":   drl_by_modality,
        "partial":         True,
        "source":          "live:ai-context",
    }
    return payload


# ── People & Community ───────────────────────────────────────────────────────

@router.get("/api/overview/people", summary="People / community engagement (best-effort)")
def get_people(
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    """People counts (persons / teams / orgs / communities) via native element
    counts — one `count_metadata_elements` per type (SELECT COUNT(*)), so this is
    sub-second where the old find-and-bucket approach materialized every profile.
    NB: native counts every entity of the type; the previous ActorManager
    find-and-bucket returned a curated set, so a few totals differ (that raw count
    is the authoritative repository count). Karma / feedback below."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    as_of_time = _norm_asof(as_of_time)
    ckey = _viewer_key(f"people|{as_of_time}", url, server, user_id, user_pwd)
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    persons = teams = orgs = it_profiles = communities = None
    expert = None
    scope = _count_scope(people_counts, count_elements, count_relationships)
    n_people = _scoped(people_counts, scope)
    n_elements = _scoped(count_elements, scope)
    try:
        expert = _expert(url, server, user_id, user_pwd)
        people = n_people(expert, as_of_time, strict=True)
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
    feedback_unmeasured = None
    karma = None
    ce = None
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        fb = _feedback_counts(ce, as_of_time, _scoped(count_relationships, scope, expert=expert))
        feedback_by_type = fb["byType"]
        feedback_items = fb["total"]
        feedback_unmeasured = fb["unmeasured"]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: feedback query failed: {exc}")
    try:
        if expert is not None:
            karma = n_elements(expert, "ContributionRecord", as_of_time, strict=True)
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
        "countScope":         scope,            # "repository" (whole catalog) or "viewer" (what you can see)
        "feedbackUnmeasured": feedback_unmeasured,   # relationship types whose count could not be read
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
    user_id: Optional[str] = Query(None),
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
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    as_of_time = _norm_asof(as_of_time)
    key = _section_key_or_401("usage-context", as_of_time, population=VIEWER,
                              url=url, server=server, user_id=user_id, user_pwd=user_pwd)
    payload, meta = _section_fetch(
        key, functools.partial(_compute_usage_context, as_of_time, url, server, user_id, user_pwd),
        ok=lambda p: p.get("informationSupplyChains") is not None)
    if payload is None:
        return _section_unready("usage-context", meta)
    return JSONResponse({**payload, **meta})


def _compute_usage_context(as_of_time, url, server, user_id, user_pwd) -> dict:
    """Every Egeria call behind usage-context (~40 s cold). Runs in a background worker."""
    iscs = blueprints = None
    mgr = None
    scope = _count_scope(usage_context_counts)
    try:
        mgr = _expert(url, server, user_id, user_pwd)
        usage = _scoped(usage_context_counts, scope)(mgr, as_of_time, strict=True)
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

    solution_components_total = solution_components_realised = None
    if solution_component_realisation is not None:
        try:
            ce2 = _make("ClassificationExplorer", url, server, user_id, user_pwd)
            comp = solution_component_realisation(mgr, ce2, as_of_time)
            solution_components_total    = comp["solutionComponentsTotal"]
            solution_components_realised = comp["solutionComponentsRealised"]
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview usage-context: solution_component_realisation failed: {exc}")

    payload = {
        "asOfTime":                as_of_time,
        "countScope":              scope,   # scope of the ISC / blueprint counts; the % contextualised is viewer-scoped
        "informationSupplyChains": iscs,
        "blueprints":              blueprints,
        "contextualisedCount":     contextualised_count,
        "contextualisedAssetTotal": asset_total_for_pct,
        "contextualisedPct":       contextualised_pct,
        "solutionComponents":         solution_components_total,
        "solutionComponentsRealised": solution_components_realised,
        "partial":                 True,
        "source":                  "live:usage-context",
    }
    return payload


def _is_template_el(el: dict) -> bool:
    for val in (el.get("elementHeader") or {}).values():
        if isinstance(val, dict) and (val.get("classificationName")
                                      or (val.get("type") or {}).get("typeName")) == "Template":
            return True
    return False


# ── Growth (asOfTime snapshots) ──────────────────────────────────────────────

@router.get("/api/overview/growth", summary="Catalog growth via asOfTime snapshots")
def get_growth(
    window: str = Query("6mo", description="8h|1d|3d|7d|30d|90d|6mo|1y"),
    points: Optional[int] = Query(None, ge=2, le=24, description="override #snapshots"),
    months: Optional[int] = Query(None, ge=2, le=12, description="deprecated — use window"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    """Real growth series: one count per snapshot date with asOfTime set — Egeria
    answers historical queries natively, so no separate time-series store is needed.
    The window sets the span and (by default) the granularity; points can override
    the snapshot count. Snapshots assets / terms / governed / data-products.
    Served from the background section cache (refreshed hourly; see "Background section cache")."""
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    if months:                              # back-compat: months → an N*30d window
        window = f"{months * 30}d"

    span_s, default_pts = _WINDOWS.get(window, _WINDOWS["6mo"])
    n = points or default_pts

    key = _section_key_or_401("growth", window, n, population=_growth_population(),
                              url=url, server=server, user_id=user_id, user_pwd=user_pwd)
    payload, meta = _section_fetch(
        key, functools.partial(_compute_growth, window, n, url, server, user_id, user_pwd),
        ok=lambda p: bool(p.get("series")))
    if payload is None:
        return _section_unready("growth", meta)
    return JSONResponse({**payload, **meta})


def _compute_growth(window, n, url, server, user_id, user_pwd) -> dict:
    """The N asOfTime snapshots behind the growth chart (~1 min cold). Runs in a background worker."""
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Connection failed: {exc}") from exc

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
    return payload
