# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Operations — FastAPI router.

Serves the egeria-operations SPA and its API. Four tabs driven by the pyegeria
RuntimeManager (plus AutomatedCuration):

  - Servers              : config + status of servers on a platform; start/stop.
  - Integration Connectors : connectors on an Integration Daemon; start/stop/refresh.
  - Governance Engines   : engines on an Engine Host; refresh config.
  - Engine Actions       : ecosystem-wide engine-action status; cancel.

Routes
------
  GET  /egeria-operations                              → SPA shell
  GET  /api/operations/platforms                       → platforms + deployed servers
  GET  /api/operations/server-status                   → live status row per server (async fan-out)
  GET  /api/operations/server-report/{guid}            → full server report
  GET  /api/operations/integration-connectors          → connectors on an Integration Daemon
  GET  /api/operations/governance-engines              → engines on an Engine Host
  GET  /api/operations/engine-actions                  → ecosystem-wide engine actions
  POST /api/operations/server/{action}                 → activate | shutdown (admin-gated)
  POST /api/operations/connector/{action}              → start | stop | refresh (admin-gated)
  POST /api/operations/engine/refresh                  → refresh engine config (admin-gated)
  POST /api/operations/engine-action/cancel            → cancel an engine action (admin-gated)

Platform/server discovery
-------------------------
Uses _async_get_platforms_by_type (async) or get_platforms_by_type (sync) with:
  body = {class:"FilterRequestBody", filter:"OMAG Server Platform",
          graphQueryDepth:1, includeOnlyRelationships:["DeployedOn"]}
Each platform element carries hostedITAssets (DeployedOn relationships); each
relationship's relatedElement gives the server guid, displayName, and
deployedImplementationType.

Integration Connector caching (non-blocking)
--------------------------------------------
The Egeria /instance/report endpoint polls every connector for live status and
can take several minutes on a loaded daemon. The endpoint is therefore
non-blocking:

  1. Cold start  — _get_server_report_cached fires a background asyncio Task and
                   returns {"loading": true} immediately. The frontend polls every
                   8 s until loading becomes false.
  2. In-flight   — subsequent requests while the Task is running also get
                   {"loading": true}. Exactly one Task runs per cache key.
  3. Fresh cache — result returned instantly (TTL = 60 s).
  4. Stale cache — stale result returned instantly; a background refresh Task is
                   spawned; response includes {"stale": true} so the frontend
                   shows an amber banner.

Cache is invalidated by _invalidate_server_cache after any start/stop action so
the next load reflects the new connector state.

RuntimeManager timeout
----------------------
RuntimeManager is constructed with time_out=180 (seconds). The Egeria view
server is the bottleneck, not our code; 180 s gives the background task enough
headroom on slow daemons. Apache's ProxyPass timeout for /api is 300 s.

Async invariants
----------------
- Sync client factories (_runtime_manager, _automated_curation) are only called
  from sync (def) routes or background threads. Never call them from async routes.
- Async factories (_runtime_manager_async, _automated_curation_async) use
  async_apply_token, which awaits _async_create_egeria_bearer_token() directly
  instead of run_until_complete(), avoiding the "event loop already running" error.
- _platform_server_guids (sync) is used only from sync routes or executors.
  _platform_server_guids_async awaits _async_get_platforms_by_type and is used
  from async routes.
- _get_server_report_cached is intentionally sync (no await) so that the check +
  Task creation is atomic within the asyncio event loop — no concurrent cold-starts.
"""
import os
import asyncio
import time
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import apply_token, async_apply_token
from result_cache import request_identity

router = APIRouter(tags=["egeria-operations"])


# ── Server-report cache (non-blocking, stale-while-revalidate) ────────────────
# The Integration Daemon's /instance/report polls every connector for live
# status and can take several minutes.  Strategy:
#   • Cold start  → fire background task, return loading=True immediately.
#   • In-flight   → return loading=True (one task per key).
#   • Fresh cache → return data instantly.
#   • Stale cache → return data instantly, kick off background refresh.

@dataclass
class _ReportCacheEntry:
    data: Any
    ts: float
    refreshing: bool = False

_report_cache: dict[str, _ReportCacheEntry] = {}
_fetch_in_progress: dict[str, asyncio.Task] = {}
_REPORT_TTL = 60.0  # seconds before a cached entry is considered stale


def _report_cache_key(server_guid: str, url: str, server: str, identity: str) -> str:
    """identity = result_cache.request_identity(...) (a hashed credential). server_guid stays first:
    _invalidate_server_cache drops every caller's entry for a server by that prefix."""
    return f"{server_guid}|{url}|{server}|{identity}"


def _invalidate_server_cache(server_guid: str) -> None:
    """Drop cached reports for a server after a state-changing action."""
    for key in [k for k in _report_cache if k.startswith(server_guid + "|")]:
        del _report_cache[key]


async def _fetch_and_cache(rm, server_guid: str, key: str) -> None:
    """Background coroutine: fetch the server report and populate the cache."""
    try:
        raw = await rm._async_get_server_report(server_guid=server_guid, output_format="JSON")
        _report_cache[key] = _ReportCacheEntry(data=raw, ts=time.monotonic())
        logger.info("operations: server report cached for %s", server_guid)
    except Exception:
        entry = _report_cache.get(key)
        if entry:
            entry.refreshing = False
        logger.warning("operations: background fetch failed for %s", server_guid)
    finally:
        _fetch_in_progress.pop(key, None)


def _get_server_report_cached(rm, server_guid: str, key: str) -> tuple[Any, bool, bool]:
    """Return (raw_report, is_stale, is_loading).

    is_loading=True means no cached data exists yet; the caller should return
    an empty response and let the client retry in a few seconds.
    This function is sync (no await) so there is no risk of concurrent cold-starts.
    """
    now = time.monotonic()
    entry = _report_cache.get(key)
    if entry is not None:
        if now - entry.ts < _REPORT_TTL:
            return entry.data, False, False  # fresh
        if not entry.refreshing:
            entry.refreshing = True
            asyncio.get_event_loop().create_task(_fetch_and_cache(rm, server_guid, key))
        return entry.data, True, False  # stale, refreshing in background

    # No cache — ensure exactly one fetch task is running
    task = _fetch_in_progress.get(key)
    if task is None or task.done():
        _fetch_in_progress[key] = asyncio.get_event_loop().create_task(
            _fetch_and_cache(rm, server_guid, key)
        )
    return None, False, True  # loading


def _is_auth_error(exc: Exception) -> bool:
    """Return True if exc represents a 401/403 from Egeria (expired token / access denied)."""
    seen = set()
    node = exc
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        code = getattr(node, "response_code", None) or getattr(node, "http_status_code", None)
        if code in (401, 403):
            return True
        resp = getattr(node, "response", None)
        if resp is not None and getattr(resp, "status_code", None) in (401, 403):
            return True
        s = str(node).upper()
        if ("HTTP CODE: 401" in s or "HTTP CODE: 403" in s
                or "USER_NOT_AUTHORIZED" in s or "NOT_AUTHORIZED" in s
                or "AUTHORIZATION_ERROR" in s or "401 " in s
                or "CLIENT ERROR '401" in s or "CLIENT ERROR '403" in s):
            return True
        node = getattr(node, "__cause__", None) or getattr(node, "__context__", None)
    return False


def _is_timeout_error(exc: Exception) -> bool:
    """Return True if exc is a pyegeria or asyncio timeout (408 / TIMEOUT_ERROR)."""
    if isinstance(exc, asyncio.TimeoutError):
        return True
    code = getattr(exc, "response_code", None) or getattr(exc, "http_status_code", None)
    if code == 408:
        return True
    s = str(exc).upper()
    return "TIMEOUT_ERROR" in s or "TIMED OUT" in s


def _raise_http(exc: Exception, log_msg: str = "") -> None:
    """Re-raise a pyegeria exception as the correct FastAPI HTTPException."""
    if log_msg:
        logger.exception(log_msg)
    if _is_timeout_error(exc):
        raise HTTPException(status_code=504,
                            detail="Egeria did not respond in time — the server may be busy. Try again in a moment.")
    if _is_auth_error(exc):
        raise HTTPException(status_code=401,
                            detail="Session expired or token invalid — please reconnect.")
    raise HTTPException(status_code=500, detail=str(exc))

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-operations.html"


# ── client factories ──────────────────────────────────────────────────────────

def _runtime_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import RuntimeManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = RuntimeManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd, time_out=180)
    apply_token(mgr)
    return mgr


def _admin_gate(request: Request):
    """Raise 403 unless the caller is an administrator (reused demo/freshstart gate)."""
    try:
        from demo_feedback_handler import _is_admin
    except Exception:
        _is_admin = None
    if _is_admin is not None and not _is_admin(request):
        raise HTTPException(status_code=403, detail="This operation requires an administrator.")


# ── serialisation ─────────────────────────────────────────────────────────────

def _name_of(props: dict) -> str:
    props = props or {}
    return props.get("displayName") or props.get("qualifiedName") or ""


def _server_stub(rel: dict) -> dict:
    """One `hostedITAssets` DeployedOn relationship → a flat server stub.

    The server element is under `relatedElement` (elementHeader.guid +
    properties.displayName/deployedImplementationType)."""
    rel = rel or {}
    re_ = rel.get("relatedElement") or {}
    hdr = re_.get("elementHeader") or {}
    props = re_.get("properties") or {}
    return {
        "guid":        hdr.get("guid") or "",
        "displayName": _name_of(props) or hdr.get("guid") or "",
        "serverType":  props.get("deployedImplementationType") or "",
    }


# ── SPA ───────────────────────────────────────────────────────────────────────

@router.get("/egeria-operations", include_in_schema=False)
def serve_operations():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Operations page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


# ── Platform + server discovery (shared by all tabs; slowly changing) ──────────

@router.get("/api/operations/platforms", summary="OMAG Server Platforms + their deployed servers")
def list_platforms(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        body = {"class": "FilterRequestBody", "filter": "OMAG Server Platform",
                "graphQueryDepth": 1, "includeOnlyRelationships": ["DeployedOn"]}
        raw = rm.get_platforms_by_type(body=body, output_format="JSON")
    except Exception as exc:
        _raise_http(exc, "operations: get_platforms_by_type failed")
    out = []
    for e in (raw if isinstance(raw, list) else []):
        hdr = e.get("elementHeader") or {}
        props = e.get("properties") or {}
        hosted = e.get("hostedITAssets") or []
        servers = [_server_stub(r) for r in hosted if isinstance(r, dict)]
        servers = [s for s in servers if s["guid"]]
        servers.sort(key=lambda s: (s.get("displayName") or "").lower())
        out.append({
            "guid":        hdr.get("guid") or "",
            "displayName": _name_of(props) or hdr.get("guid") or "",
            "servers":     servers,
        })
    out.sort(key=lambda p: (p.get("displayName") or "").lower())
    return JSONResponse({"platforms": out})


# ── Server report (Servers tab + shared by the report-driven tabs) ─────────────

def _report_element(raw):
    """get_server_report returns a dict, a 1-item list, or a 'not found' string."""
    if isinstance(raw, list):
        return raw[0] if raw and isinstance(raw[0], dict) else None
    return raw if isinstance(raw, dict) else None


@router.get("/api/operations/server-report/{guid}", summary="Full server report (live)")
def server_report(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        raw = rm.get_server_report(server_guid=guid, output_format="JSON")
    except Exception as exc:
        _raise_http(exc, f"operations: get_server_report({guid!r}) failed")
    el = _report_element(raw)
    if not el:
        raise HTTPException(status_code=404, detail=f"Server report for {guid!r} not found")
    return JSONResponse(el)


def _platform_server_guids(rm, platform_guid: str) -> list:
    """The deployed-server stubs for one platform (DeployedOn, depth 1)."""
    body = {"class": "FilterRequestBody", "filter": "OMAG Server Platform",
            "graphQueryDepth": 1, "includeOnlyRelationships": ["DeployedOn"]}
    raw = rm.get_platforms_by_type(body=body, output_format="JSON")
    for e in (raw if isinstance(raw, list) else []):
        if (e.get("elementHeader") or {}).get("guid") == platform_guid:
            return [_server_stub(r) for r in (e.get("hostedITAssets") or []) if isinstance(r, dict)]
    return []


async def _platform_server_guids_async(rm, platform_guid: str) -> list:
    """Async version of _platform_server_guids — uses _async_get_platforms_by_type."""
    body = {"class": "FilterRequestBody", "filter": "OMAG Server Platform",
            "graphQueryDepth": 1, "includeOnlyRelationships": ["DeployedOn"]}
    raw = await rm._async_get_platforms_by_type(body=body, output_format="JSON")
    for e in (raw if isinstance(raw, list) else []):
        if (e.get("elementHeader") or {}).get("guid") == platform_guid:
            return [_server_stub(r) for r in (e.get("hostedITAssets") or []) if isinstance(r, dict)]
    return []


@router.get("/api/operations/server-status", summary="Status row per server on a platform (Servers tab)")
async def server_status_overview(
    platform_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    try:
        rm = await _runtime_manager_async(url, server, user_id, user_pwd)
        stubs = [s for s in await _platform_server_guids_async(rm, platform_guid) if s.get("guid")]
    except Exception as exc:
        _raise_http(exc, "operations: server-status discovery failed")

    sem = asyncio.Semaphore(16)

    async def _one(st):
        async with sem:
            try:
                rep = _report_element(
                    await rm._async_get_server_report(server_guid=st["guid"], output_format="JSON")
                ) or {}
            except Exception:
                rep = {}
            return {
                "guid":               st["guid"],
                "serverName":         rep.get("serverName") or st.get("displayName") or "",
                "serverType":         rep.get("serverType") or st.get("serverType") or "",
                "description":        rep.get("description") or "",
                "organizationName":   rep.get("organizationName") or "",
                "serverActiveStatus": rep.get("serverActiveStatus") or "UNKNOWN",
            }

    try:
        rows = list(await asyncio.gather(*[_one(s) for s in stubs]))
    except Exception:
        logger.exception("operations: concurrent server-report fetch failed")
        rows = [{"guid": s["guid"], "serverName": s.get("displayName") or "", "serverType": s.get("serverType") or "",
                 "description": "", "organizationName": "", "serverActiveStatus": "UNKNOWN"} for s in stubs]
    rows.sort(key=lambda r: (r.get("serverName") or "").lower())
    return JSONResponse({"servers": rows, "total": len(rows)})


# ── Integration Connectors tab ─────────────────────────────────────────────────

def _automated_curation(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import AutomatedCuration
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = AutomatedCuration(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


async def _runtime_manager_async(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import RuntimeManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = RuntimeManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd, time_out=180)
    await async_apply_token(mgr)
    return mgr


async def _automated_curation_async(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import AutomatedCuration
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = AutomatedCuration(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    await async_apply_token(mgr)
    return mgr


def _catalog_target(t: dict) -> dict:
    """One catalog-target element → flat row.

    AutomatedCuration.get_catalog_targets returns the target element directly
    (elementHeader + properties at the top level). The CatalogTarget relationship
    properties (including catalogTargetName) are in relatedBy.relationshipProperties.
    """
    t = t or {}
    hdr   = t.get("elementHeader") or {}
    props = t.get("properties") or {}
    rel_props = (t.get("relatedBy") or {}).get("relationshipProperties") or {}
    return {
        "catalogTargetName": rel_props.get("catalogTargetName") or "",
        "typeName":          (hdr.get("type") or {}).get("typeName") or "",
        "guid":              hdr.get("guid") or "",
        "elementName":       _name_of(props),
    }


def _target_list(raw) -> list:
    return [t for t in raw if isinstance(t, dict)] if isinstance(raw, list) else []


# Catalog targets per connector, read at graph depth 0 (the same rows as depth 1, measured live
# 2026-11-10: 67 targets took 25.8 s at depth 1 and 0.18 s at depth 0; two connectors timed out at
# depth 1). Paging MUST be in the body: with a body, pyegeria ignores start_from/page_size, so the old
# page_size=200 never applied. Read page by page until an empty page (the end), the cap, or the time
# budget. A read that fails before any row is an explicit "could not be read", never "no targets".
_CT_PAGE = 200
_CT_MAX = 1000
_CT_BUDGET_S = 20.0


async def _read_catalog_targets(ac, guid: str, *, page: int = _CT_PAGE, cap: int = _CT_MAX,
                                budget_s: float = _CT_BUDGET_S) -> dict:
    """{"targets": [rows] | None, "complete": bool, "error": str | None, "stoppedBy": None | "cap" |
    "time" | "error"}. targets is None only when nothing could be read (error says why)."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + budget_s
    rows: list = []
    start = 0
    while True:
        remaining = deadline - loop.time()
        try:
            if remaining <= 0:
                raise asyncio.TimeoutError()
            raw = await asyncio.wait_for(
                ac._async_get_catalog_targets(
                    integ_connector_guid=guid, output_format="JSON", report_spec=None,
                    body={"class": "FilterRequestBody", "graphQueryDepth": 0, "startFrom": start, "pageSize": page}),
                timeout=remaining)
        except Exception as exc:  # noqa: BLE001 -- timeout or Egeria error: said, never hidden as "none"
            timed_out = isinstance(exc, asyncio.TimeoutError) or _is_timeout_error(exc)
            why = (f"timed out after {budget_s:.0f} s" if timed_out
                   else f"{type(exc).__name__}: {str(exc)[:160]}")
            if not rows:
                return {"targets": None, "complete": False, "error": f"could not be read: {why}",
                        "stoppedBy": "error"}
            return {"targets": rows, "complete": False, "error": f"stopped after {len(rows)}: {why}",
                    "stoppedBy": "time" if timed_out else "error"}
        batch = [_catalog_target(t) for t in _target_list(raw)]
        if not batch:
            return {"targets": rows, "complete": True, "error": None, "stoppedBy": None}
        rows.extend(batch)
        start += len(batch)
        if len(rows) >= cap:
            return {"targets": rows[:cap], "complete": False, "error": None, "stoppedBy": "cap"}


@router.get("/api/operations/integration-connectors", summary="Connectors on an Integration Daemon (Integration Connectors tab)")
async def list_integration_connectors(
    server_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    who = request_identity(user_id, user_pwd)  # hashed credential, never a bare user_id (None under token auth)
    if who is None:
        # Expired token: never serve (or start) a cached report for it. The report itself takes minutes,
        # so refuse here rather than sending a minutes-long call to Egeria just to be refused.
        raise HTTPException(status_code=401, detail="Egeria token expired; sign in again")
    cache_key = _report_cache_key(server_guid, url or "", server or "", who)
    try:
        rm = await _runtime_manager_async(url, server, user_id, user_pwd)
        ac = await _automated_curation_async(url, server, user_id, user_pwd)
        raw, is_stale, is_loading = _get_server_report_cached(rm, server_guid, cache_key)
    except Exception as exc:
        _raise_http(exc, "operations: integration-connectors report failed")

    if is_loading:
        return JSONResponse({"connectors": [], "total": 0, "loading": True, "stale": False})

    rep = _report_element(raw) or {}

    connectors = rep.get("integrationConnectorReports") or []
    groups = {g.get("integrationGroupGUID"): g.get("integrationGroupName")
              for g in (rep.get("integrationGroups") or []) if isinstance(g, dict)}

    # Catalog targets per connector (N+1 fan-out, run concurrently), paged at depth 0; see
    # _read_catalog_targets. A connector whose targets could not be read says so.
    sem = asyncio.Semaphore(16)

    async def _one(c):
        guid = c.get("connectorGUID")
        async with sem:
            ct = await _read_catalog_targets(ac, guid) if guid else {
                "targets": None, "complete": False, "error": "could not be read: no connector GUID", "stoppedBy": "error"}
        targets = ct["targets"]
        return {
            "connectorName":            c.get("connectorName") or "",
            "connectorGUID":            guid or "",
            "connectorStatus":          c.get("connectorStatus") or "",
            "integrationGroup":         groups.get(c.get("integrationGroupGUID")) or "",
            "lastStatusChange":         c.get("lastStatusChange") or "",
            "lastRefreshTime":          c.get("lastRefreshTime") or "",
            "minMinutesBetweenRefresh": c.get("minMinutesBetweenRefresh"),
            "failingExceptionMessage":  c.get("failingExceptionMessage") or "",
            "catalogTargets":           targets if targets is not None else [],
            # None = could not be read (catalogTargetsError says why); never shown as "no targets".
            "catalogTargetCount":       (len(targets) if targets is not None and ct["complete"] else None),
            "catalogTargetsLowerBound": (len(targets) if targets is not None and not ct["complete"] else None),
            "catalogTargetsComplete":   bool(ct["complete"]),
            "catalogTargetsError":      ct["error"],
            "catalogTargetsStoppedBy":  ct["stoppedBy"],
        }

    try:
        rows = list(await asyncio.gather(*[_one(c) for c in connectors]))
    except Exception:
        logger.exception("operations: concurrent catalog-target fetch failed")
        rows = []
    rows.sort(key=lambda r: (r.get("connectorName") or "").lower())
    return JSONResponse({"connectors": rows, "total": len(rows), "loading": False, "stale": is_stale})


class _ConnectorActionBody(BaseModel):
    server_guid: str
    connector_name: str




@router.post("/api/operations/connector/{action}", summary="Start/stop/refresh a connector (admin only)")
def connector_action(action: str, request: Request, body: _ConnectorActionBody,
                     url: Optional[str] = Query(None), server: Optional[str] = Query(None),
                     user_id: Optional[str] = Query(None)):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    if action not in ("restart", "refresh"):
        raise HTTPException(status_code=400, detail=f"Unsupported connector action {action!r}")
    _admin_gate(request)
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        if action == "restart":
            rm.restart_connector(server_guid=body.server_guid, connector_name=body.connector_name)
        else:
            # Refresh can take several minutes (external actions, large surveys) — run in
            # background thread and return 202 immediately so the request never times out.
            connector_name = body.connector_name
            server_guid = body.server_guid
            def _bg_refresh():
                try:
                    asyncio.run(rm._async_refresh_integration_connector(
                        connector_name=connector_name, server_guid=server_guid
                    ))
                    logger.info("operations: connector refresh %s on %s completed", connector_name, server_guid)
                except Exception:
                    logger.exception("operations: connector refresh %s on %s failed in background", connector_name, server_guid)
            threading.Thread(target=_bg_refresh, daemon=True).start()
            return JSONResponse({"ok": True, "action": "refresh", "refreshing": True}, status_code=202)
    except Exception as exc:
        _raise_http(exc, f"operations: connector {action}({body.connector_name!r}) failed")
    _invalidate_server_cache(body.server_guid)
    logger.info("operations: connector %s %s on %s", action, body.connector_name, body.server_guid)
    return JSONResponse({"ok": True, "action": action, "connector_name": body.connector_name})


# ── Governance Engines tab ──────────────────────────────────────────────────────

@router.get("/api/operations/governance-engines", summary="Engines on an Engine Host (Governance Engines tab)")
def list_governance_engines(
    server_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        rep = _report_element(rm.get_server_report(server_guid=server_guid, output_format="JSON")) or {}
    except Exception as exc:
        _raise_http(exc, "operations: governance-engines report failed")
    rows = []
    for g in (rep.get("governanceEngineSummaries") or []):
        if not isinstance(g, dict):
            continue
        rows.append({
            "governanceEngineName":        g.get("governanceEngineName") or "",
            "governanceEngineTypeName":    g.get("governanceEngineTypeName") or "",
            "governanceEngineService":     g.get("governanceEngineService") or "",
            "governanceEngineDescription": g.get("governanceEngineDescription") or "",
            "governanceEngineStatus":      g.get("governanceEngineStatus") or "",
            "governanceRequestTypes":      g.get("governanceRequestTypes") or [],
            "lastRefreshTime":             g.get("lastRefreshTime") or "",
            "governanceEngineGUID":        g.get("governanceEngineGUID") or "",
        })
    rows.sort(key=lambda r: (r.get("governanceEngineName") or "").lower())
    return JSONResponse({"engines": rows, "total": len(rows)})


class _EngineActionBody(BaseModel):
    server_guid: str
    engine_name: str


@router.post("/api/operations/engine/refresh", summary="Refresh a governance engine's config (admin only)")
def engine_refresh(request: Request, body: _EngineActionBody,
                   url: Optional[str] = Query(None), server: Optional[str] = Query(None),
                   user_id: Optional[str] = Query(None)):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    _admin_gate(request)
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        rm.refresh_governance_engine(gov_engine_name=body.engine_name, server_guid=body.server_guid)
    except Exception as exc:
        _raise_http(exc, f"operations: refresh_governance_engine({body.engine_name!r}) failed")
    logger.info("operations: refreshed governance engine %s on %s", body.engine_name, body.server_guid)
    return JSONResponse({"ok": True, "engine_name": body.engine_name})


# ── Engine Actions tab (ecosystem-wide) ───────────────────────────────────────

_ENGINE_ACTIONS_CACHE: dict = {}
_ENGINE_ACTIONS_TTL = 60.0  # seconds — same TTL as _REPORT_TTL above; unlike that
# endpoint this one is a single call (2-3s measured live, 2026-08-26), not a
# minutes-long poll, so a plain blocking cache is enough -- no need for the
# background-task/stale-banner machinery _report_cache uses.


# Engine actions are read newest first, a page at a time, at graph depth 0 (the rows read only
# `properties`). Measured live 2026-11-10: depth 0 + PROPERTY_DESCENDING on requestedStartTime is
# honoured by Egeria (contiguous pages, no overlap), 500 rows in ~2.5 s; the old depth-3 single page of
# 500 took 90 s+ (504). Egeria held 21,908 engine actions, so one page is never "the total".
_EA_PAGE_DEFAULT = 200
_EA_PAGE_MAX = 500
_EA_ORDER = {"sequencing_order": "PROPERTY_DESCENDING", "sequencing_property": "requestedStartTime"}
_EA_COUNT_TIMEOUT = 10   # seconds; the repository-wide count is ~1 s, a viewer-scoped one times out


def _engine_action_row(item: dict) -> dict:
    hdr   = item.get("elementHeader") or {}
    props = item.get("properties") or {}
    return {
        "guid":                     hdr.get("guid") or "",
        "displayName":              props.get("displayName") or props.get("qualifiedName") or "",
        "requestType":              props.get("requestType") or "",
        "activityStatus":           props.get("activityStatus") or "",
        "executorEngineGUID":       props.get("executorEngineGUID") or "",
        "executorEngineName":       props.get("executorEngineName") or "",
        "requesterUserId":          props.get("requesterUserId") or "",
        "requestedStartTime":       props.get("requestedStartTime") or "",
        "startTime":                props.get("startTime") or "",
        "completionTime":           props.get("completionTime") or "",
        "completionGuards":         props.get("completionGuards") or [],
        "completionMessage":        props.get("completionMessage") or "",
        "governanceActionTypeName": props.get("governanceActionTypeName") or "",
    }


def _fetch_engine_actions(ac, search_string: str, start: int, page_size: int) -> list:
    raw = ac.find_engine_actions(search_string=search_string, graph_query_depth=0, start_from=start,
                                 page_size=page_size, output_format="JSON", **_EA_ORDER)
    return [r for r in raw if isinstance(r, dict)] if isinstance(raw, list) else []


def _page_summary(start: int, returned: int, next_is_empty: Optional[bool],
                  repository_count: Optional[int]) -> dict:
    """What a page says about the whole set, honestly (Egeria paging contract: a short page is NOT
    the last page; only an empty one is). `next_is_empty` is the answer to a 1-row read just past
    this page: True = this page ends the set (the total is exact), False = more exist, None = the
    check failed (unknown). `total` is set only when exact; otherwise `lowerBound` says "at least"."""
    seen = start + returned
    if returned == 0:
        # An empty page is the end. From the start it means "none"; further in, the set ends at or
        # before `start`, which is exact only when the caller paged here contiguously -- not assumed.
        more = False
        total = 0 if start == 0 else None
    else:
        more = None if next_is_empty is None else (not next_is_empty)
        total = seen if more is False else None
    return {
        "start":           start,
        "returned":        returned,
        "nextStart":       seen if (returned and more is not False) else None,   # also when unknown
        "more":            more,                  # True / False / None (unknown)
        "total":           total,
        "lowerBound":      seen + (1 if more else 0),
        "repositoryCount": repository_count,      # whole repository (all zones); None if not counted
    }


def _repository_engine_action_count(url, server, user_id, user_pwd) -> Optional[int]:
    """Every EngineAction in the repository, counted natively (push_down: repository-wide, not
    zone-scoped; ~1 s). None if the count is unavailable. Labelled as the repository's count."""
    try:
        from pyegeria import MetadataExpert
        url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
        server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
        user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
        user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
        mx = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        apply_token(mx)
        n = mx.count_metadata_elements({"class": "FindRequestBody", "metadataElementTypeName": "EngineAction"},
                                       push_down=True, timeout=_EA_COUNT_TIMEOUT)
        return n if isinstance(n, int) and n >= 0 else None
    except Exception as exc:  # noqa: BLE001 -- the count is extra; the page still serves
        logger.debug(f"operations: engine-action count unavailable: {exc}")
        return None


@router.get("/api/operations/engine-actions", summary="Ecosystem-wide engine actions, newest first, a page at a time")
def list_engine_actions(
    search_string: str = Query("*"),
    start: int = Query(0, ge=0),
    page_size: int = Query(_EA_PAGE_DEFAULT, ge=1, le=_EA_PAGE_MAX),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    who = request_identity(user_id, user_pwd)  # hashed credential; None = expired token, bypass the cache
    cache_key = f"{search_string}|{start}|{page_size}|{url or ''}|{server or ''}|{who}"
    cached = (_ENGINE_ACTIONS_CACHE.get(cache_key) if who else None)
    if cached and (time.time() - cached[0]) < _ENGINE_ACTIONS_TTL:
        return JSONResponse(cached[1])

    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        page = _fetch_engine_actions(ac, search_string, start, page_size)
    except Exception as exc:
        _raise_http(exc, "operations: find_engine_actions failed")
    # Is there anything after this page? One row past it answers that (an empty read = the end).
    try:
        next_is_empty = (not _fetch_engine_actions(ac, search_string, start + len(page), 1)) if page else True
    except Exception as exc:  # noqa: BLE001 -- unknown, said as unknown
        logger.debug(f"operations: engine-action next-page check failed: {exc}")
        next_is_empty = None
    repo_count = (_repository_engine_action_count(url, server, user_id, user_pwd)
                  if search_string in ("*", "") else None)
    rows = [_engine_action_row(item) for item in page]
    result = {"actions": rows, **_page_summary(start, len(rows), next_is_empty, repo_count)}
    if who:
        _ENGINE_ACTIONS_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


class _CancelActionBody(BaseModel):
    engine_action_guid: str


@router.post("/api/operations/engine-action/cancel", summary="Cancel an engine action (admin only)")
def cancel_engine_action_route(request: Request, body: _CancelActionBody,
                               url: Optional[str] = Query(None), server: Optional[str] = Query(None),
                               user_id: Optional[str] = Query(None)):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    _admin_gate(request)
    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        ac.cancel_engine_action(engine_action_guid=body.engine_action_guid)
    except Exception as exc:
        _raise_http(exc, f"operations: cancel_engine_action({body.engine_action_guid!r}) failed")
    logger.info("operations: cancelled engine action %s", body.engine_action_guid)
    return JSONResponse({"ok": True, "engine_action_guid": body.engine_action_guid})


# ── Server lifecycle (admin-gated writes) ──────────────────────────────────────

class _ServerActionBody(BaseModel):
    server_guid: str


@router.post("/api/operations/server/{action}", summary="Start/stop a server (admin only)")
def server_action(action: str, request: Request, body: _ServerActionBody,
                  url: Optional[str] = Query(None), server: Optional[str] = Query(None),
                  user_id: Optional[str] = Query(None)):
    user_pwd = None  # never from the URL: a password in a query string lands in access logs
    if action not in ("activate", "shutdown"):
        raise HTTPException(status_code=400, detail=f"Unsupported server action {action!r}")
    _admin_gate(request)
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        if action == "activate":
            # Slow (timeout up to 240s) — the frontend shows a spinner and suppresses refresh.
            rm.activate_server_with_stored_config(server_guid=body.server_guid)
        else:
            rm.shutdown_server(server_guid=body.server_guid)
    except Exception as exc:
        _raise_http(exc, f"operations: server {action}({body.server_guid!r}) failed")
    logger.info("operations: server %s on %s", action, body.server_guid)
    return JSONResponse({"ok": True, "action": action, "server_guid": body.server_guid})
