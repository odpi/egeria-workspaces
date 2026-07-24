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

router = APIRouter(tags=["egeria-overview"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-overview.html"

_DEFAULT_CAP = 500            # same ceiling used elsewhere in the app
_CACHE_TTL   = 60.0          # seconds; summary is not real-time critical

# Governed-data classifications that count as "governed" (single-condition tallies
# only — PY-15 makes any 2+ classification ANY/ALL query return zero).
_GOVERNANCE_CLASSIFICATIONS = ("ZoneMembership", "Confidentiality", "Criticality", "Impact", "Retention")

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


def _json_list(raw) -> list:
    """Normalise a pyegeria output_format='JSON' result to a list of dicts.
    Empty results come back as a 'No … found' string; some calls wrap in a dict."""
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for k in ("elements", "items", "relationships", "list"):
            if isinstance(raw.get(k), list):
                return [r for r in raw[k] if isinstance(r, dict)]
    return []


# ── find helpers ─────────────────────────────────────────────────────────────

def _find(mgr, body: dict, page_size: int = _DEFAULT_CAP) -> list:
    """Run a FindRequestBody, always returning a (possibly empty) list. Never raises."""
    try:
        raw = mgr.find_metadata_elements(body, start_from=0, page_size=page_size, graph_query_depth=0)
        return [el for el in (raw if isinstance(raw, list) else []) if isinstance(el, dict)]
    except Exception as exc:  # noqa: BLE001 — best-effort tile, degrade don't fail
        logger.debug(f"overview _find failed for {body.get('metadataElementTypeName')!r}: {exc}")
        return []


# ── count seam — uses Egeria native instance counting when available ─────────
# Egeria added native counting in odpi/egeria#9168 (MetadataExpert.count_metadata_elements
# / count_relationships_between_elements → SELECT COUNT(*), no result-set
# materialization). We use it when BOTH the pyegeria client exposes the method AND
# the target server supports it; otherwise we fall back to len(find/get) — same
# result, just heavier. This makes every count here — including the as-of
# time-machine and the N-snapshot growth series — sub-second on a #9168 server, and
# still correct on older ones. The result is normalized from int or {"count": N}.
_ELEMENT_COUNT_CANDIDATES = ("count_metadata_elements", "get_metadata_element_count")
_REL_COUNT_CANDIDATES     = ("count_relationships_between_elements", "count_relationships")
_count_caps: dict[str, Optional[str]] = {}   # cache: which native method (if any) a client class exposes
_native_server_ok: dict[str, bool] = {}      # cache: does this server support native count? (False after a probe fails)


def _server_key(mgr) -> str:
    return f"{getattr(mgr, 'platform_url', '')}|{getattr(mgr, 'view_server', '')}"


def _native_disabled(mgr) -> bool:
    """True once a native count call has failed for this server — so we don't pay a
    failed round-trip on every subsequent count against an older server."""
    return _native_server_ok.get(_server_key(mgr)) is False


def _disable_native(mgr, exc) -> None:
    if not _native_disabled(mgr):
        logger.info(f"overview count seam: native count not supported by "
                    f"{_server_key(mgr)} — using len(find/get) fallback ({exc})")
    _native_server_ok[_server_key(mgr)] = False


def _native_count_method(mgr, candidates, cache_key: str) -> Optional[str]:
    if cache_key not in _count_caps:
        name = next((c for c in candidates if callable(getattr(mgr, c, None))), None)
        _count_caps[cache_key] = name
        logger.info(f"overview count seam [{cache_key}]: "
                    + (f"native via {name}" if name else "fallback to len(find/get)"))
    return _count_caps[cache_key]


def _as_count(res) -> Optional[int]:
    if isinstance(res, int):
        return res
    if isinstance(res, dict) and res.get("count") is not None:
        return int(res["count"])
    return None


def _element_count(mgr, body: dict, as_of: Optional[str] = None) -> int:
    """Count elements matching a FindRequestBody — native (count_metadata_elements)
    when the client + server support it, else len(find_metadata_elements(...))."""
    b = dict(body)
    if as_of:
        b["asOfTime"] = as_of
    name = _native_count_method(mgr, _ELEMENT_COUNT_CANDIDATES, "elem:" + type(mgr).__name__)
    if name and not _native_disabled(mgr):
        try:
            c = _as_count(getattr(mgr, name)(b))
            if c is not None:
                return c
        except Exception as exc:  # noqa: BLE001 — old server: mark unsupported, fall back
            _disable_native(mgr, exc)
    return len(_find(mgr, b))


def _count_type(mgr, type_name: Optional[str], as_of: Optional[str] = None) -> tuple[int, bool]:
    """Count of ACTIVE elements of a type, optionally as of a past time. Returns
    (count, capped) — `capped` kept for call-site compatibility."""
    body: dict = {"class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"]}
    if type_name:
        body["metadataElementTypeName"] = type_name
    n = _element_count(mgr, body, as_of)
    return n, n >= _DEFAULT_CAP


def _rel_count(ce, rel_type: str, as_of: Optional[str] = None, expert=None) -> Optional[int]:
    """Count relationships of a type, optionally as of a past time.

    Prefers Egeria's native count via MetadataExpert.count_relationships_between_elements
    (odpi/egeria#9168) with a FindRelationshipRequestBody, passed as `expert`. Falls
    back to len(ClassificationExplorer.get_relationships(...)) — the proven path —
    when there's no expert, no native support, or the native call fails. asOfTime
    goes in the request body. None on total failure."""
    if expert is not None and not _native_disabled(expert):
        name = _native_count_method(expert, _REL_COUNT_CANDIDATES, "rel:" + type(expert).__name__)
        if name:
            body = {"class": "FindRelationshipRequestBody", "relationshipTypeName": rel_type,
                    "limitResultsByStatus": ["ACTIVE"]}
            if as_of:
                body["asOfTime"] = as_of
            try:
                c = _as_count(getattr(expert, name)(body))
                if c is not None:
                    return c
            except Exception as exc:  # noqa: BLE001 — old server: mark unsupported, fall back
                _disable_native(expert, exc)
    try:
        body = {"class": "ResultsRequestBody", "asOfTime": as_of} if as_of else None
        return len(_json_list(ce.get_relationships(
            relationship_type=rel_type, output_format="JSON",
            start_from=0, page_size=5000, body=body)))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview _rel_count({rel_type}) failed: {exc}")
        return None


def _classifications_of(el: dict) -> set[str]:
    out: set[str] = set()
    for c in el.get("classifications") or []:
        if isinstance(c, dict) and c.get("classificationName"):
            out.add(c["classificationName"])
    return out


def _zone_names(el: dict) -> list:
    for c in el.get("classifications") or []:
        if isinstance(c, dict) and c.get("classificationName") == "ZoneMembership":
            pvm = (c.get("classificationProperties") or {}).get("propertyValueMap") or {}
            zv = pvm.get("zoneMembership")
            if isinstance(zv, dict) and zv.get("class") == "ArrayTypePropertyValue":
                arr = (zv.get("arrayValues") or {}).get("propertyValueMap") or {}
                return [arr[k].get("primitiveValue") for k in sorted(arr, key=lambda k: int(k) if k.isdigit() else 0)
                        if isinstance(arr.get(k), dict)]
    return []


# ── SPA ──────────────────────────────────────────────────────────────────────

@router.get("/egeria-overview", include_in_schema=False)
def serve_overview():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Overview page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


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
    gov_body = {
        "class": "FindRequestBody",
        "matchClassifications": {
            "class": "SearchClassifications",
            "matchCriteria": "ANY",
            "conditions": [{"name": n} for n in _GOVERNANCE_CLASSIFICATIONS],
        },
        "limitResultsByStatus": ["ACTIVE"],
    }
    if as_of_time:
        gov_body["asOfTime"] = as_of_time
    governed_hits = _find(mgr, gov_body)
    by_classification: dict[str, int] = {}
    zone_counts: dict[str, int] = {}
    for el in governed_hits:
        for name in _classifications_of(el):
            by_classification[name] = by_classification.get(name, 0) + 1
        for z in _zone_names(el):
            if z:
                zone_counts[z] = zone_counts.get(z, 0) + 1

    # Assets by type (best-effort; unknown types yield 0).
    by_type = []
    asset_total = 0
    for label, tname in _ASSET_TYPES:
        c, _ = _count_type(mgr, tname, as_of_time)
        by_type.append({"label": label, "type": tname, "count": c})
        asset_total += c

    term_count, term_capped = _count_type(mgr, "GlossaryTerm", as_of_time)
    top_zones = sorted(zone_counts.items(), key=lambda kv: -kv[1])[:8]

    # Data products (DigitalProduct) — live count.
    data_products, _ = _count_type(mgr, "DigitalProduct", as_of_time)

    # Certifications, licenses & open exceptions (governance relationships).
    certs = _certifications(url, server, user_id, user_pwd, as_of_time, expert=mgr)

    payload = {
        "asOfTime":         as_of_time,
        "assetTotal":       asset_total,
        "byType":           by_type,
        "termCount":        term_count,
        "governedCount":    len(governed_hits),
        "governedCapped":   len(governed_hits) >= _DEFAULT_CAP,
        "byClassification": by_classification,
        "topZones":         [{"zone": z, "count": c} for z, c in top_zones],
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

def _rel_end_date(rel: dict):
    """Best-effort expiry date for a Certification relationship: try the domain
    property, then relationship effectivity. Returns a datetime or None."""
    from datetime import datetime
    props = rel.get("relationshipProperties") or {}
    header = rel.get("relationshipHeader") or {}
    candidates = [props.get(k) for k in ("coverageEnd", "end", "endDate", "expiry", "expirationDate")]
    candidates.append((header.get("effectivityDates") or {}).get("effectiveToTime"))
    candidates.append(header.get("effectiveToTime"))
    for v in candidates:
        if not v:
            continue
        s = str(v).replace("Z", "+00:00")
        for parse in (lambda x: datetime.fromisoformat(x),):
            try:
                return parse(s)
            except Exception:  # noqa: BLE001
                pass
    return None


def _certifications(url, server, user_id, user_pwd, as_of: Optional[str] = None, expert=None) -> dict:
    """Count active certifications, those expiring within 90 days, a soonest list,
    the license count, and open governance exceptions — optionally as of a past
    time. `expert` (a MetadataExpert) enables native relationship counts.
    Degrades to zeros on any failure (demo may have none)."""
    from datetime import datetime, timezone, timedelta
    out = {"active": None, "expiring90": None, "soon": [], "licenses": None, "exceptions": None}
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview certifications: client build failed: {exc}")
        return out
    body = {"class": "ResultsRequestBody", "asOfTime": as_of} if as_of else None
    try:
        certs = _json_list(ce.get_relationships(relationship_type="Certification",
                                                output_format="JSON", start_from=0,
                                                page_size=_DEFAULT_CAP, body=body))
        # "expiring soon" is anchored to the snapshot time, not always wall-clock now.
        now = datetime.fromisoformat(as_of.replace("Z", "+00:00")) if as_of else datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        horizon = now + timedelta(days=90)
        soon = []
        expiring = 0
        for r in certs:
            end = _rel_end_date(r)
            if end is not None:
                if end.tzinfo is None:
                    end = end.replace(tzinfo=timezone.utc)
                if now <= end <= horizon:
                    expiring += 1
                    end2 = (r.get("end2") or {})
                    name = ((end2.get("properties") or end2) or {}).get("displayName") or "certification"
                    soon.append({"name": name, "days": (end - now).days})
        soon.sort(key=lambda s: s["days"])
        out["active"] = len(certs)
        out["expiring90"] = expiring
        out["soon"] = soon[:5]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview certifications: query failed: {exc}")
    out["licenses"] = _rel_count(ce, "License", as_of, expert=expert)
    out["exceptions"] = _rel_count(ce, "Exception", as_of, expert=expert)
    return out


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

    cataloged, _ = _count_type(mgr, "Asset", as_of_time)   # broad supertype
    class_body = {                                          # any governance classification
        "class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"],
        "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ANY",
                                  "conditions": [{"name": n} for n in _GOVERNANCE_CLASSIFICATIONS]},
    }
    if as_of_time:
        class_body["asOfTime"] = as_of_time
    classified = len(_find(mgr, class_body))

    # Semantic grounding: SemanticAssignment relationships (term ↔ asset) — the
    # meaning layer that grounds AI. Count of assignments as a proxy for grounded links.
    grounding_links = None
    grounding_pct = None
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        grounding_links = _rel_count(ce, "SemanticAssignment", as_of_time, expert=mgr)
        if cataloged and grounding_links is not None:
            grounding_pct = min(100, round(100 * grounding_links / cataloged))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview ai-context: grounding query failed: {exc}")

    payload = {
        "asOfTime":  as_of_time,
        "funnel": {
            "cataloged":  cataloged or None,
            "documented": None,          # needs a description-present filter — best-effort TODO
            "classified": classified or None,
            "lineage":    None,          # needs lineage-relationship presence — TODO
            "aiReady":    None,          # composite gate — TODO
        },
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
    """People counts (persons / teams / orgs / communities) are live from Actor +
    Community managers. Karma / feedback aggregates need the Collaboration OMAS and
    stay null (SPA keeps its sample baseline)."""
    as_of_time = _norm_asof(as_of_time)
    ckey = f"people|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    persons = teams = orgs = it_profiles = None
    try:
        am = _make("ActorManager", url, server, user_id, user_pwd)
        profiles = _json_list(am.find_actor_profiles(search_string="*", output_format="JSON",
                                                     start_from=0, page_size=_DEFAULT_CAP,
                                                     as_of_time=as_of_time or None))
        counts: dict[str, int] = {}
        for p in profiles:
            tn = ((p.get("elementHeader") or {}).get("type") or {}).get("typeName") or "?"
            counts[tn] = counts.get(tn, 0) + 1
        persons     = counts.get("Person", 0)
        teams       = counts.get("Team", 0)
        orgs        = counts.get("Organization", 0)
        it_profiles = counts.get("ITProfile", 0)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: actor query failed: {exc}")

    communities = None
    try:
        cm = _make("CommunityMatters", url, server, user_id, user_pwd)
        communities = len(_json_list(cm.find_communities(
            search_string="*", starts_with=False, output_format="JSON",
            graph_query_depth=0, start_from=0, page_size=_DEFAULT_CAP,
            as_of_time=as_of_time or None)))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: community query failed: {exc}")

    # Crowd-sourced feedback — Collaboration OMAS relationship counts (cheap). Often
    # sparse in demo data, but real. Leaderboard/engagement need per-person rollups
    # (deferred). karma = count of ContributionRecord elements.
    feedback_by_type = None
    feedback_items = None
    karma = None
    expert = None
    try:
        expert = _expert(url, server, user_id, user_pwd)   # for native counts (feedback + karma)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: expert build failed: {exc}")
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
        fb = {}
        for rel, key in (("AttachedRating", "ratings"), ("AttachedComment", "comments"),
                         ("AttachedLike", "likes"), ("AttachedTag", "tags"),
                         ("AttachedNoteLog", "noteLogs")):
            fb[key] = _rel_count(ce, rel, as_of_time, expert=expert) or 0
        feedback_by_type = fb
        feedback_items = sum(fb.values())
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: feedback query failed: {exc}")
    try:
        if expert is not None:
            karma, _ = _count_type(expert, "ContributionRecord", as_of_time)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: karma query failed: {exc}")

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
    blueprint". Counts are live; the "% of assets contextualised" coverage figure
    needs graph traversal and is deferred (SPA shows its sample baseline)."""
    as_of_time = _norm_asof(as_of_time)
    ckey = f"usage|{as_of_time}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    # SolutionArchitect find methods take asOfTime via `body` (no as_of_time kwarg).
    # Best-effort: if the body shape is rejected we degrade to null for that call.
    def _sa_count(fn, as_of):
        if as_of:
            try:
                # SolutionArchitect OMVS takes as-of via a SearchStringRequestBody
                # (confirmed by test_overview_asof.py — FilterRequestBody is rejected).
                return len([e for e in _json_list(fn(
                    body={"class": "SearchStringRequestBody", "searchString": "*", "asOfTime": as_of},
                    output_format="JSON", start_from=0, page_size=_DEFAULT_CAP))
                    if not _is_template_el(e)])
            except Exception as exc:  # noqa: BLE001
                logger.debug(f"overview usage-context: as-of query failed: {exc}")
                return None
        return len([e for e in _json_list(fn(
            search_string="*", output_format="JSON", start_from=0, page_size=_DEFAULT_CAP))
            if not _is_template_el(e)])

    iscs = blueprints = None
    try:
        sa = _make("SolutionArchitect", url, server, user_id, user_pwd)
        iscs = _sa_count(sa.find_information_supply_chains, as_of_time)
        blueprints = _sa_count(sa.find_solution_blueprints, as_of_time)
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


def _count_asof(mgr, type_name: Optional[str], as_of: Optional[str], classifications=None) -> int:
    body: dict = {"class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"]}
    if type_name:
        body["metadataElementTypeName"] = type_name
    if classifications:
        body["matchClassifications"] = {"class": "SearchClassifications", "matchCriteria": "ANY",
                                         "conditions": [{"name": n} for n in classifications]}
    return _element_count(mgr, body, as_of)   # native count when available, else len(find)


# Time-window → (total span seconds, default #points). asOfTime lets us snapshot
# at any granularity; granularity follows the window so we always get ~6–12 points.
_WINDOWS = {
    "8h":  (8 * 3600,       8),
    "1d":  (86400,          6),
    "3d":  (3 * 86400,      6),
    "7d":  (7 * 86400,      7),
    "30d": (30 * 86400,     6),
    "90d": (90 * 86400,     7),
    "6mo": (180 * 86400,    6),
    "1y":  (365 * 86400,    12),
}


def _growth_label(d, span_s: int) -> str:
    if span_s <= 2 * 86400:
        return d.strftime("%H:00")          # hourly / intraday
    if span_s <= 120 * 86400:
        return d.strftime("%-d %b")         # daily / weekly
    return d.strftime("%b")                 # monthly


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
    from datetime import datetime, timezone
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

    now = datetime.now(timezone.utc)
    step = span_s / (n - 1)
    date_fmt = "%d %b %Y %H:%M" if span_s <= 2 * 86400 else "%d %b %Y"
    series = []
    for i in range(n - 1, -1, -1):
        if i == 0:
            d, as_of = now, None
        else:
            d = datetime.fromtimestamp(now.timestamp() - i * step, tz=timezone.utc)
            as_of = d.isoformat()
        try:
            assets   = _count_asof(mgr, "Asset", as_of)
            terms    = _count_asof(mgr, "GlossaryTerm", as_of)
            governed = _count_asof(mgr, None, as_of, classifications=_GOVERNANCE_CLASSIFICATIONS)
            products = _count_asof(mgr, "DigitalProduct", as_of)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"overview growth: snapshot {i} failed: {exc}")
            assets = terms = governed = products = None
        series.append({"label": _growth_label(d, span_s), "date": d.strftime(date_fmt),
                       "assets": assets, "terms": terms, "governed": governed, "products": products})

    payload = {"series": series, "window": window, "points": n,
               "rangeFrom": series[0]["date"] if series else None,
               "rangeTo": series[-1]["date"] if series else None,
               "partial": False, "source": "live:growth"}
    _cache[ckey] = (time.time(), payload)
    return JSONResponse(payload)
