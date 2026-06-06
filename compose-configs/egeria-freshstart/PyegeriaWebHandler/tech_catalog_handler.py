"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Technical Asset Catalog — FastAPI router.

Serves the tech-catalog SPA and provides backend API endpoints for all
nine asset-type sections defined in technical_data_catalog_spec.md.

Endpoints:
  GET /tech-catalog                          → serve tech-catalog.html SPA
  GET /api/tech-catalog/infrastructure       → ITInfrastructure assets
  GET /api/tech-catalog/software-capabilities → SoftwareCapability elements
  GET /api/tech-catalog/endpoints            → Endpoint elements
  GET /api/tech-catalog/data-stores          → DataStore assets
  GET /api/tech-catalog/data-feeds           → DataFeed assets
  GET /api/tech-catalog/data-sets            → DataSet assets
  GET /api/tech-catalog/apis                 → DeployedAPI assets
  GET /api/tech-catalog/software-components  → DeployedSoftwareComponent processes
  GET /api/tech-catalog/actions              → Action processes
  GET /api/tech-catalog/assets/{guid}        → detail for any element by GUID
"""

import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

router = APIRouter(tags=["tech-catalog"])

_HERE = Path(__file__).parent
_HTML = _HERE / "tech-catalog.html"

_SEQ_ORDER = "PROPERTY_ASCENDING"
_SEQ_PROP  = "displayName"


# ── Credential helpers ────────────────────────────────────────────────────────

def _creds(url, server, user_id, user_pwd):
    return (
        url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443"),
        server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id  or os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _asset_maker(url, server, user_id, user_pwd):
    from pyegeria import AssetMaker
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = AssetMaker(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _connection_maker(url, server, user_id, user_pwd):
    from pyegeria import ConnectionMaker
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = ConnectionMaker(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


# ── Serialisation ─────────────────────────────────────────────────────────────

def _header(el):
    return el.get("elementHeader") or {}

def _props(el):
    return el.get("properties") or {}

def _type_name(el):
    return (_header(el).get("type") or {}).get("typeName", "")

def _extract_classifications(header):
    result = []
    for cls in (header.get("classifications") or []):
        if not isinstance(cls, dict):
            continue
        cls_header = cls.get("classificationHeader") or cls.get("header") or cls
        type_name  = (cls_header.get("type") or {}).get("typeName") or cls_header.get("classificationName") or ""
        if not type_name or type_name == "TemplateSubstitute":
            continue
        cls_props = cls.get("classificationProperties") or cls.get("properties") or {}
        flat = {}
        if isinstance(cls_props, dict):
            prop_map = cls_props.get("propertyValueMap") or {}
            for k, v in prop_map.items():
                flat[k] = v.get("primitiveValue", "") if isinstance(v, dict) else str(v)
            if not flat:
                for k, v in cls_props.items():
                    if k not in ("class", "propertyValueMap", "propertiesAsStrings"):
                        flat[k] = str(v)
        result.append({"typeName": type_name, "properties": flat})
    return result


def _serialize(el):
    """Minimal common serialisation for any asset/element."""
    hdr   = _header(el)
    props = _props(el)
    return {
        "guid":                      hdr.get("guid", ""),
        "typeName":                  _type_name(el),
        "displayName":               props.get("displayName") or props.get("name") or "",
        "qualifiedName":             props.get("qualifiedName") or "",
        "description":               props.get("description") or "",
        "deployedImplementationType": props.get("deployedImplementationType") or "",
        "deploymentStatus":          props.get("deploymentStatus") or "",
        "activityStatus":            props.get("activityStatus") or "",
        "networkAddress":            props.get("networkAddress") or "",
        "classifications":           _extract_classifications(hdr),
    }


def _safe_list(raw):
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "items" in raw:
        return raw["items"]
    return []


# ── SPA route ─────────────────────────────────────────────────────────────────

@router.get("/tech-catalog", include_in_schema=False)
def serve_spa():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="tech-catalog.html not found")
    return FileResponse(_HTML, media_type="text/html")


# ── Common query params ───────────────────────────────────────────────────────

_CRED_PARAMS = dict(
    url      = Query(None),
    server   = Query(None),
    user_id  = Query(None),
    user_pwd = Query(None),
)


# ── List endpoints ────────────────────────────────────────────────────────────

@router.get("/api/tech-catalog/infrastructure")
def list_infrastructure(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("tech-catalog: AssetMaker connection failed")
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_infrastructure(
            search_string=q or "*",
            metadata_element_type="ITInfrastructure",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_infrastructure failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/software-capabilities")
def list_software_capabilities(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("tech-catalog: AssetMaker connection failed")
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_software_capabilities(
            search_string=q or "*",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_software_capabilities failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/endpoints")
def list_endpoints(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _connection_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("tech-catalog: ConnectionMaker connection failed")
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        from pyegeria.omvs.connection_maker import SearchStringRequestBody
        body = SearchStringRequestBody()
        body.search_string = q or "*"
        raw = mgr.find_endpoints(body=body.to_dict() if hasattr(body, 'to_dict') else {"class": "SearchStringRequestBody", "searchString": q or "*"})
        items = [_serialize(e) for e in _safe_list(raw)]
        items.sort(key=lambda x: (x.get("displayName") or "").lower())
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_endpoints failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-stores")
def list_data_stores(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataStore",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_stores failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-feeds")
def list_data_feeds(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataFeed",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_feeds failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-sets")
def list_data_sets(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataSet",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_sets failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/apis")
def list_apis(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_assets(
            search_string=q or "*",
            metadata_element_type="DeployedAPI",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_apis failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/software-components")
def list_software_components(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_processes(
            search_string=q or "*",
            metadata_element_type="DeployedSoftwareComponent",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_software_components failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/actions")
def list_actions(
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_processes(
            search_string=q or "*",
            metadata_element_type="Action",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_actions failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/assets/{guid}")
def get_asset_detail(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_assets(
            search_string="*",
            output_format="JSON",
            graph_query_depth=1,
        )
        el = next((e for e in _safe_list(raw) if _header(e).get("guid") == guid), None)
        if el is None:
            raise HTTPException(status_code=404, detail=f"Asset {guid!r} not found")
        return JSONResponse(_serialize(el))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_asset_detail failed")
        raise HTTPException(status_code=500, detail=str(exc))
