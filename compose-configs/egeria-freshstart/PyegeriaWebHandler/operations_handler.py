# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Operations — FastAPI router.

Serves the egeria-operations SPA and the operations API. Four tabs, all driven
by the pyegeria RuntimeManager (plus AssetMaker / AutomatedCuration):

  - Servers              : config + status of servers on a platform; start/stop.
  - Integration Connectors : connectors on an Integration Daemon; start/stop/refresh.
  - Governance Engines   : engines on an Engine Host; refresh config.
  - Engine Actions       : ecosystem-wide engine-action status; cancel.

Spec: operations_plan.md (review comments inline there).

Platform/server discovery (verified recipe — operations_plan.md):
  get_platforms_by_type(body={class:FilterRequestBody, filter:"OMAG Server Platform",
                              graphQueryDepth:1, includeOnlyRelationships:["DeployedOn"]})
  → per platform: elementHeader.guid + properties.displayName(‖qualifiedName)
  → servers under `hostedITAssets` (DeployedOn relationships); server element under
    `relatedElement`: elementHeader.guid + properties.displayName + deployedImplementationType.

Routes:
  GET  /egeria-operations                       → serve the SPA
  GET  /api/operations/platforms                → platforms + their deployed servers (cacheable)
  GET  /api/operations/server-report/{guid}     → full server report (live, per refresh)
  POST /api/operations/server/{action}          → activate | shutdown a server (admin-gated)
"""
import os
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import apply_token

router = APIRouter(tags=["egeria-operations"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-operations.html"


# ── client factories ──────────────────────────────────────────────────────────

def _runtime_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import RuntimeManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = RuntimeManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
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
    return FileResponse(_HTML, media_type="text/html")


# ── Platform + server discovery (shared by all tabs; slowly changing) ──────────

@router.get("/api/operations/platforms", summary="OMAG Server Platforms + their deployed servers")
def list_platforms(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        body = {"class": "FilterRequestBody", "filter": "OMAG Server Platform",
                "graphQueryDepth": 1, "includeOnlyRelationships": ["DeployedOn"]}
        raw = rm.get_platforms_by_type(body=body, output_format="JSON")
    except Exception as exc:
        logger.exception("operations: get_platforms_by_type failed")
        raise HTTPException(status_code=500, detail=str(exc))
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
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        raw = rm.get_server_report(server_guid=guid, output_format="JSON")
    except Exception as exc:
        logger.exception("operations: get_server_report(%s) failed", guid)
        raise HTTPException(status_code=500, detail=str(exc))
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


@router.get("/api/operations/server-status", summary="Status row per server on a platform (Servers tab)")
def server_status_overview(
    platform_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        stubs = [s for s in _platform_server_guids(rm, platform_guid) if s.get("guid")]
    except Exception as exc:
        logger.exception("operations: server-status discovery failed")
        raise HTTPException(status_code=500, detail=str(exc))

    # One report per server — fan out concurrently (bounded), as for audit users.
    async def _fetch(stub_list):
        sem = asyncio.Semaphore(16)

        async def _one(st):
            async with sem:
                try:
                    rep = await rm._async_get_server_report(server_guid=st["guid"], output_format="JSON")
                    rep = _report_element(rep) or {}
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
        return await asyncio.gather(*[_one(s) for s in stub_list])

    try:
        rows = asyncio.get_event_loop().run_until_complete(_fetch(stubs))
    except Exception:
        logger.exception("operations: concurrent server-report fetch failed")
        rows = [{"guid": s["guid"], "serverName": s.get("displayName") or "", "serverType": s.get("serverType") or "",
                 "description": "", "organizationName": "", "serverActiveStatus": "UNKNOWN"} for s in stubs]
    rows.sort(key=lambda r: (r.get("serverName") or "").lower())
    return JSONResponse({"servers": rows, "total": len(rows)})


# ── Integration Connectors tab ─────────────────────────────────────────────────

def _asset_maker(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import AssetMaker
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = AssetMaker(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _catalog_target(t: dict) -> dict:
    """One catalog-target relationship → flat row. The related element (the
    catalogued asset) is under `relatedElement`."""
    t = t or {}
    re_ = t.get("relatedElement") or {}
    hdr = re_.get("elementHeader") or {}
    props = re_.get("properties") or {}
    return {
        "catalogTargetName": t.get("catalogTargetName") or "",
        "typeName":          (hdr.get("type") or {}).get("typeName") or "",
        "guid":              hdr.get("guid") or "",
        "elementName":       _name_of(props),
    }


def _target_list(raw) -> list:
    return [t for t in raw if isinstance(t, dict)] if isinstance(raw, list) else []


@router.get("/api/operations/integration-connectors", summary="Connectors on an Integration Daemon (Integration Connectors tab)")
def list_integration_connectors(
    server_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        am = _asset_maker(url, server, user_id, user_pwd)
        rep = _report_element(rm.get_server_report(server_guid=server_guid, output_format="JSON")) or {}
    except Exception as exc:
        logger.exception("operations: integration-connectors report failed")
        raise HTTPException(status_code=500, detail=str(exc))

    connectors = rep.get("integrationConnectorReports") or []
    # integration-group lookup is by GUID (the connector carries integrationGroupGUID,
    # not the name the spec assumed).
    groups = {g.get("integrationGroupGUID"): g.get("integrationGroupName")
              for g in (rep.get("integrationGroups") or []) if isinstance(g, dict)}

    # One get_catalog_targets per connector — N+1 fan-out, run concurrently.
    async def _fetch_targets(conns):
        sem = asyncio.Semaphore(16)

        async def _one(c):
            guid = c.get("connectorGUID")
            async with sem:
                try:
                    raw = await am._async_get_catalog_targets(integration_connector_guid=guid,
                                                               graph_query_depth=1, page_size=200, output_format="JSON")
                    targets = [_catalog_target(t) for t in _target_list(raw)]
                except Exception:
                    targets = []
            return {
                "connectorName":         c.get("connectorName") or "",
                "connectorGUID":         guid or "",
                "connectorStatus":       c.get("connectorStatus") or "",
                "integrationGroup":      groups.get(c.get("integrationGroupGUID")) or "",
                "lastStatusChange":      c.get("lastStatusChange") or "",
                "lastRefreshTime":       c.get("lastRefreshTime") or "",
                "minMinutesBetweenRefresh": c.get("minMinutesBetweenRefresh"),
                "failingExceptionMessage":  c.get("failingExceptionMessage") or "",
                "catalogTargets":        targets,
            }
        return await asyncio.gather(*[_one(c) for c in conns])

    try:
        rows = asyncio.get_event_loop().run_until_complete(_fetch_targets(connectors))
    except Exception:
        logger.exception("operations: concurrent catalog-target fetch failed")
        rows = []
    rows.sort(key=lambda r: (r.get("connectorName") or "").lower())
    return JSONResponse({"connectors": rows, "total": len(rows)})


class _ConnectorActionBody(BaseModel):
    server_guid: str
    connector_name: str


@router.post("/api/operations/connector/{action}", summary="Start/stop/refresh a connector (admin only)")
def connector_action(action: str, request: Request, body: _ConnectorActionBody):
    if action not in ("start", "stop", "refresh"):
        raise HTTPException(status_code=400, detail=f"Unsupported connector action {action!r}")
    _admin_gate(request)
    try:
        rm = _runtime_manager()
        if action == "start":
            rm.start_connector(server_guid=body.server_guid, connector_name=body.connector_name)
        elif action == "stop":
            rm.stop_connector(server_guid=body.server_guid, connector_name=body.connector_name)
        else:
            # NOTE: pyegeria method is currently plural (refresh_integration_connectors);
            # Dan is renaming to singular. Prefer the singular name when it lands.
            fn = (getattr(rm, "refresh_integration_connector", None)
                  or getattr(rm, "refresh_integration_connectors"))
            fn(server_guid=body.server_guid, connector_name=body.connector_name)
    except Exception as exc:
        logger.exception("operations: connector %s(%s) failed", action, body.connector_name)
        raise HTTPException(status_code=500, detail=str(exc))
    logger.info("operations: connector %s %s on %s", action, body.connector_name, body.server_guid)
    return JSONResponse({"ok": True, "action": action, "connector_name": body.connector_name})


# ── Governance Engines tab ──────────────────────────────────────────────────────

@router.get("/api/operations/governance-engines", summary="Engines on an Engine Host (Governance Engines tab)")
def list_governance_engines(
    server_guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        rep = _report_element(rm.get_server_report(server_guid=server_guid, output_format="JSON")) or {}
    except Exception as exc:
        logger.exception("operations: governance-engines report failed")
        raise HTTPException(status_code=500, detail=str(exc))
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
def engine_refresh(request: Request, body: _EngineActionBody):
    _admin_gate(request)
    try:
        rm = _runtime_manager()
        rm.refresh_governance_engine(gov_engine_name=body.engine_name, server_guid=body.server_guid)
    except Exception as exc:
        logger.exception("operations: refresh_governance_engine(%s) failed", body.engine_name)
        raise HTTPException(status_code=500, detail=str(exc))
    logger.info("operations: refreshed governance engine %s on %s", body.engine_name, body.server_guid)
    return JSONResponse({"ok": True, "engine_name": body.engine_name})


# ── Server lifecycle (admin-gated writes) ──────────────────────────────────────

class _ServerActionBody(BaseModel):
    server_guid: str


@router.post("/api/operations/server/{action}", summary="Start/stop a server (admin only)")
def server_action(action: str, request: Request, body: _ServerActionBody):
    if action not in ("activate", "shutdown"):
        raise HTTPException(status_code=400, detail=f"Unsupported server action {action!r}")
    _admin_gate(request)
    try:
        rm = _runtime_manager()
        if action == "activate":
            # Slow (timeout up to 240s) — the frontend shows a spinner and suppresses refresh.
            rm.activate_server_with_stored_config(server_guid=body.server_guid)
        else:
            rm.shutdown_server(server_guid=body.server_guid)
    except Exception as exc:
        logger.exception("operations: server %s(%s) failed", action, body.server_guid)
        raise HTTPException(status_code=500, detail=str(exc))
    logger.info("operations: server %s on %s", action, body.server_guid)
    return JSONResponse({"ok": True, "action": action, "server_guid": body.server_guid})
