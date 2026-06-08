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

# Mermaid graph fields Egeria may embed in an element response.
# Must stay in sync with _ALL_MERMAID_FIELDS in tech-catalog.html and mermaid_handler.py.
_MERMAID_FIELDS = {
    "mermaidGraph", "anchorMermaidGraph", "edgeMermaidGraph",
    "localLineageGraph", "fieldLevelLineageGraph",
    "informationSupplyChainMermaidGraph", "iscImplementationMermaidGraph",
    "actionMermaidGraph", "specificationMermaidGraph",
    "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph",
    "collectionMermaidMindMap",
}


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

    pyegeria wraps the related element in a nested 'relatedElement' sub-dict
    (class RelatedMetadataElementSummary). The top-level item only contains
    'relationshipHeader', 'relationshipProperties', 'relatedElement', and
    optionally 'relatedElementAtEnd1'. We must unwrap 'relatedElement' to
    reach the actual elementHeader / properties.
    """
    _SKIP_KEYS = {"elementHeader", "properties", "classifications", "class"}
    _ITEM_META  = {"relationshipHeader", "relationshipProperties",
                   "relatedElement", "relatedElementAtEnd1", "class"}
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
            rel_props_raw = item.get("relationshipProperties") or {}
            rel_props = _flat_props(rel_props_raw) if rel_props_raw else {}

            # Prefer the nested 'relatedElement' wrapper (standard pyegeria format).
            nested = item.get("relatedElement")
            if isinstance(nested, dict) and "elementHeader" in nested:
                elem = nested
            else:
                # Fallback for older / flat formats
                elem = {k: v for k, v in item.items() if k not in _ITEM_META}

            elem_hdr   = _header(elem)
            elem_props = _props(elem)
            type_info  = elem_hdr.get("type") or {}
            type_name  = type_info.get("typeName", "")
            # superTypeNames lets the frontend find a nav target for subtypes
            super_types = type_info.get("superTypeNames") or []

            result.append({
                "relationshipType": rel_type,
                "relationshipProperties": rel_props,
                "relatedElement": {
                    "guid":        elem_hdr.get("guid", ""),
                    "typeName":    type_name,
                    "superTypes":  super_types,
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
    # Pass through any mermaid graph fields present in the element or its properties.
    # These are only populated when graph_query_depth > 0 and Egeria has diagram data.
    for field in _MERMAID_FIELDS:
        val = el.get(field) or props.get(field)
        if val and isinstance(val, str) and not val.lower().startswith("no "):
            out[field] = val
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
            deployment_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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
            graph_query_depth=0,
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
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_endpoints(
            search_string=q or "*",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
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
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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
            graph_query_depth=0,
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
            activity_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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
            activity_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
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


# Map from section id → targeted find_* with graph_query_depth=3 for full property/relationship detail
_SECTION_FINDERS = {
    "software-capabilities": lambda m: m.find_software_capabilities(
        search_string="*", output_format="JSON", graph_query_depth=3),
    "infrastructure": lambda m: m.find_infrastructure(
        search_string="*", output_format="JSON", graph_query_depth=3,
        deployment_status_list=[],
        sequencing_order=_SEQ_ORDER, sequencing_property=_SEQ_PROP),
}


def _fetch_detail(mgr, guid: str, section: Optional[str]):
    """
    Fetch a single element with graph_query_depth=3 to expose full property/relationship detail.
    Endpoints use ConnectionMaker.get_endpoint_by_guid (not an Asset subtype).
    Other non-Asset sections use the targeted finder.
    Asset subtypes fall through to get_asset_by_guid.
    """
    # Endpoints: direct GUID lookup via ConnectionMaker
    if section == "endpoints":
        try:
            cm = _connection_maker_from_asset_maker(mgr)
            raw = cm.get_endpoint_by_guid(
                endpoint_guid=guid,
                output_format="JSON",
                body={"class": "GetRequestBody", "graphQueryDepth": 3},
            )
            el = raw[0] if isinstance(raw, list) else raw
            if el:
                return el
        except Exception:
            pass
        return None

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
            body={"class": "GetRequestBody", "graphQueryDepth": 3, "relationshipsPageSize": 50},
        )
        el = raw[0] if isinstance(raw, list) else raw
        if el:
            return el
    except Exception:
        pass

    # Fallback: SoftwareCapability subtypes (catches any missed non-Asset type)
    try:
        return _find_by_guid(
            mgr.find_software_capabilities(search_string="*", output_format="JSON", graph_query_depth=3),
            guid)
    except Exception:
        pass

    return None


def _connection_maker_from_asset_maker(mgr):
    """Create a ConnectionMaker sharing credentials from an existing AssetMaker.

    NOTE: Do NOT pass token= here. ConnectionMaker.__init__ calls check_connection()
    immediately, and the Bearer token format from AssetMaker causes a 401 on that
    handshake. A fresh create_egeria_bearer_token() call is required instead.
    """
    from pyegeria import ConnectionMaker
    cm = ConnectionMaker(
        server_name=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    cm.create_egeria_bearer_token()
    return cm


def _find_by_guid(raw, guid: str):
    """Filter a list result from find_* to return the single element matching guid."""
    for el in _safe_list(raw):
        if _header(el).get("guid") == guid:
            return el
    return None
