"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Lineage Explorer — FastAPI router.

Serves the lineage-explorer SPA and provides backend API endpoints for
data lineage traversal centred on a "focus asset".

Endpoints:
  GET /lineage                              → serve lineage-explorer.html SPA
  GET /api/lineage/search?q=               → search for assets (AssetMaker.find_assets)
  GET /api/lineage/asset/{guid}/graph      → get_asset_graph (local lineage + ISC data)
  GET /api/lineage/asset/{guid}/lineage-graph → get_asset_lineage_graph (full lineage)

Auth: token only (X-Egeria-Token header). No user_id/user_pwd query params.
Credentials for pyegeria client construction come from env vars only.
"""

import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

router = APIRouter(tags=["lineage"])

_HERE = Path(__file__).parent
_HTML = _HERE / "lineage-explorer.html"


# ── Credential helpers ─────────────────────────────────────────────────────────

def _creds(url, server):
    """Resolve platform URL and server name from params or environment."""
    return (
        url    or os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
        server or os.environ.get("EGERIA_VIEW_SERVER",  "qs-view-server"),
        os.environ.get("EGERIA_USER",          "erinoverview"),
        os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _token_from_request(request: Request) -> Optional[str]:
    """Extract pre-obtained Egeria bearer token from X-Egeria-Token header."""
    return request.headers.get("X-Egeria-Token") or None


def _apply_token(client, token: Optional[str]):
    """Set a pre-obtained bearer token on a pyegeria client, or obtain a fresh one."""
    if token:
        client.set_bearer_token(token)
    else:
        client.create_egeria_bearer_token()


def _is_no_data_error(exc: Exception) -> bool:
    """Return True if the exception represents an empty-result response (400/404)."""
    exc_str = str(exc)
    return any(code in exc_str for code in (
        "400", "404", "CLIENT_ERROR_400", "CLIENT_ERROR_404", "No elements",
    ))


def _asset_catalog(url, server, token=None):
    from pyegeria import AssetCatalog
    u, s, uid, pwd = _creds(url, server)
    ac = AssetCatalog(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(ac, token)
    return ac


def _asset_maker(url, server, token=None):
    from pyegeria import AssetMaker
    u, s, uid, pwd = _creds(url, server)
    mgr = AssetMaker(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(mgr, token)
    return mgr


# ── Serialisation helpers ─────────────────────────────────────────────────────

def _safe_list(raw) -> list:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        return [raw]
    return []


def _serialize_search_item(el: dict) -> dict:
    """Flatten a find_assets result element into a simple search result."""
    hdr   = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    typ   = (hdr.get("type") or {}).get("typeName", "")
    return {
        "guid":          hdr.get("guid", ""),
        "typeName":      typ,
        "displayName":   props.get("displayName") or props.get("name") or props.get("qualifiedName", ""),
        "qualifiedName": props.get("qualifiedName", ""),
        "description":   props.get("description", ""),
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/lineage")
def serve_lineage_explorer():
    """Serve the Lineage Explorer SPA."""
    return FileResponse(_HTML)


@router.get("/api/lineage/search")
def search_assets(
    request: Request,
    q: str = Query("*"),
    url: Optional[str] = Query(None),
    server: Optional[str] = Query(None),
):
    """Search for assets to use as a lineage focus asset.

    Uses AssetMaker.find_assets with graph_query_depth=0 (list-only, no graph data).
    Returns: {"items": [{guid, typeName, displayName, qualifiedName, description}]}
    """
    try:
        mgr = _asset_maker(url, server, _token_from_request(request))
        raw = mgr.find_assets(
            search_string=q or "*",
            graph_query_depth=0,
            output_format="JSON",
        )
        items = [_serialize_search_item(e) for e in _safe_list(raw) if isinstance(e, dict)]
        return JSONResponse({"items": items})
    except Exception as exc:
        if _is_no_data_error(exc):
            return JSONResponse({"items": []})
        logger.exception("lineage search failed for q=%r", q)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/lineage/asset/{guid}/graph")
def get_asset_graph(
    request: Request,
    guid: str,
    as_of_time: Optional[str] = Query(None),
    url: Optional[str] = Query(None),
    server: Optional[str] = Query(None),
):
    """Return the full asset graph for a lineage focus asset.

    Calls AssetCatalog.get_asset_graph with output_format="JSON".
    The response is returned as-is; the frontend extracts:
      - elementHeader (guid, createTime, updateTime, type)
      - properties (displayName, qualifiedName, description, …)
      - localLineageGraph (Mermaid string — direct lineage)
      - fieldLevelLineageGraph (Mermaid string — field mappings)
      - lineageLinkage (list — related elements via lineage relationships)
      - partOfInformationSupplyChains (list — ISC membership)

    as_of_time: ISO 8601 string for historical query; null/absent = "now".
    """
    try:
        ac = _asset_catalog(url, server, _token_from_request(request))
        raw = ac.get_asset_graph_by_guid(
            guid,
            output_format="JSON",
        )
        el = raw[0] if isinstance(raw, list) else raw
        if not isinstance(el, dict):
            return JSONResponse({"error": "not_found"}, status_code=404)
        return JSONResponse(el)
    except Exception as exc:
        if _is_no_data_error(exc):
            return JSONResponse({"error": "not_found"}, status_code=404)
        logger.exception("get_asset_graph failed for guid=%s", guid)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/lineage/asset/{guid}/lineage-graph")
def get_asset_lineage_graph(
    request: Request,
    guid: str,
    as_of_time: Optional[str] = Query(None),
    limit_to_isc: Optional[str] = Query(None),
    highlight_isc: Optional[str] = Query(None),
    all_anchors: Optional[str] = Query(None),
    url: Optional[str] = Query(None),
    server: Optional[str] = Query(None),
):
    """Return the full and edge lineage graphs plus linked assets table.

    Only called when the focus asset has a non-null localLineageGraph.
    Calls AssetCatalog.get_asset_lineage_graph with output_format="JSON".
    The response is returned as-is; the frontend extracts:
      - mermaidGraph / fullLineageMermaidGraph (end-to-end Mermaid lineage)
      - edgeMermaidGraph (extreme source/destination nodes)
      - linkedAssets (list — all nodes in the full graph)

    ISC filtering options (mutually exclusive):
      limit_to_isc: qualifiedName — restrict to this supply chain only
      highlight_isc: qualifiedName — highlight this supply chain in the graph

    all_anchors: "true" to include field-level detail in the graphs.
    as_of_time: ISO 8601 string; null/absent = "now".
    """
    _empty = {"mermaidGraph": "", "edgeMermaidGraph": "", "linkedAssets": []}
    try:
        ac = _asset_catalog(url, server, _token_from_request(request))
        raw = ac.get_asset_lineage_graph_by_guid(
            guid,
            as_of_time=as_of_time or None,
            limit_to_isc_q_name=limit_to_isc or None,
            hilight_isc_q_name=highlight_isc or None,
            all_anchors=(all_anchors == "true"),
            output_format="JSON",
        )
        el = raw[0] if isinstance(raw, list) else raw
        if not isinstance(el, dict):
            return JSONResponse(_empty)
        return JSONResponse(el)
    except Exception as exc:
        if _is_no_data_error(exc):
            return JSONResponse(_empty)
        logger.exception("get_asset_lineage_graph failed for guid=%s", guid)
        raise HTTPException(status_code=500, detail=str(exc))
