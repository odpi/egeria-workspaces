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
    from pyegeria.omvs.connection_maker import ConnectionMaker
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = ConnectionMaker(server_name=s, platform_url=u, user_id=uid, user_pwd=pwd)
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


def _flat_props(props_dict: dict) -> dict:
    """Flatten a properties dict that may use propertyValueMap encoding."""
    flat = {}
    prop_map = props_dict.get("propertyValueMap") or {}
    if prop_map:
        for k, v in prop_map.items():
            flat[k] = v.get("primitiveValue", "") if isinstance(v, dict) else str(v)
    else:
        for k, v in props_dict.items():
            if k not in ("class", "propertyValueMap", "propertiesAsStrings"):
                flat[k] = str(v) if not isinstance(v, (dict, list)) else ""
    return {k: v for k, v in flat.items() if v}


def _extract_relationships(el: dict) -> list:
    """
    Extract peer relationships from a graph-queried element.
    Egeria embeds related elements as list-valued keys where each item
    carries a 'relationshipHeader' dict describing the link type.
    """
    _SKIP_KEYS = {"elementHeader", "properties", "classifications", "class"}
    result = []
    for key, val in el.items():
        if key in _SKIP_KEYS or not isinstance(val, list):
            continue
        for item in val:
            if not isinstance(item, dict):
                continue
            rel_hdr = item.get("relationshipHeader")
            if not isinstance(rel_hdr, dict):
                continue
            rel_type = (rel_hdr.get("type") or {}).get("typeName") or key
            rel_props_raw = item.get("relationshipProperties") or item.get("properties") or {}
            rel_props = _flat_props(rel_props_raw) if rel_props_raw else {}
            # Related element is the remainder of the item dict
            elem = {k: v for k, v in item.items()
                    if k not in ("relationshipHeader", "relationshipProperties")}
            elem_hdr   = _header(elem)
            elem_props = _props(elem)
            result.append({
                "relationshipType": rel_type,
                "relationshipProperties": rel_props,
                "relatedElement": {
                    "guid":        elem_hdr.get("guid", ""),
                    "typeName":    _type_name(elem),
                    "displayName": elem_props.get("displayName") or elem_props.get("name") or elem_hdr.get("guid", ""),
                    "description": elem_props.get("description") or "",
                },
            })
    return result


def _serialize(el, include_relationships: bool = False):
    """Common serialisation for any asset/element."""
    hdr   = _header(el)
    props = _props(el)
    out = {
        "guid":                       hdr.get("guid", ""),
        "typeName":                   _type_name(el),
        "displayName":                props.get("displayName") or props.get("name") or "",
        "qualifiedName":              props.get("qualifiedName") or "",
        "description":                props.get("description") or "",
        "deployedImplementationType": props.get("deployedImplementationType") or "",
        "deploymentStatus":           props.get("deploymentStatus") or "",
        "activityStatus":             props.get("activityStatus") or "",
        "networkAddress":             props.get("networkAddress") or "",
        "classifications":            _extract_classifications(hdr),
    }
    if include_relationships:
        out["relationships"] = _extract_relationships(el)
    return out


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
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_assets(
            search_string=q or "*",
            metadata_element_type="Endpoint",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
        )
        items = [_serialize(e) for e in _safe_list(raw)]
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
    # section tells us which find_* to use for non-Asset types
    section: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        el = _fetch_detail(mgr, guid, section)
        if not el:
            raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")
        return JSONResponse(_serialize(el, include_relationships=True))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_asset_detail failed")
        raise HTTPException(status_code=500, detail=str(exc))


# Map from section id → targeted find_* with graph_query_depth=1
_SECTION_FINDERS = {
    "software-capabilities": lambda m: m.find_software_capabilities(
        search_string="*", output_format="JSON", graph_query_depth=1),
    "endpoints": lambda m: m.find_assets(
        search_string="*", metadata_element_type="Endpoint",
        output_format="JSON", graph_query_depth=1,
        sequencing_order=_SEQ_ORDER, sequencing_property=_SEQ_PROP),
    "infrastructure": lambda m: m.find_infrastructure(
        search_string="*", output_format="JSON", graph_query_depth=1,
        sequencing_order=_SEQ_ORDER, sequencing_property=_SEQ_PROP),
}


def _fetch_detail(mgr, guid: str, section: Optional[str]):
    """
    Fetch a single element with graph_query_depth=1.
    If section is known we use the targeted finder directly.
    Otherwise tries get_asset_by_guid first, then find_software_capabilities.
    """
    # Known non-Asset section — use targeted find and filter by GUID
    finder = _SECTION_FINDERS.get(section or "")
    if finder:
        try:
            return _find_by_guid(finder(mgr), guid)
        except Exception:
            pass

    # Asset subtypes — direct GUID lookup (fast)
    try:
        raw = mgr.get_asset_by_guid(
            asset_guid=guid,
            output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1, "relationshipsPageSize": 50},
        )
        el = raw[0] if isinstance(raw, list) else raw
        if el:
            return el
    except Exception:
        pass

    # Fallback: SoftwareCapability subtypes (catches any missed non-Asset type)
    try:
        return _find_by_guid(
            mgr.find_software_capabilities(search_string="*", output_format="JSON", graph_query_depth=1),
            guid)
    except Exception:
        pass

    return None


def _find_by_guid(raw, guid: str):
    """Filter a list result from find_* to return the single element matching guid."""
    for el in _safe_list(raw):
        if _header(el).get("guid") == guid:
            return el
    return None
