"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Technical Asset Catalog — FastAPI router.

Serves the tech-catalog SPA and provides backend API endpoints for all
nine asset-type sections defined in technical_data_catalog_spec.md.

Endpoints:
  GET /tech-catalog                              → serve tech-catalog.html SPA
  GET /api/tech-catalog/infrastructure           → ITInfrastructure assets
  GET /api/tech-catalog/software-capabilities    → SoftwareCapability elements
  GET /api/tech-catalog/endpoints                → Endpoint elements
  GET /api/tech-catalog/data-stores              → DataStore assets
  GET /api/tech-catalog/data-feeds               → DataFeed assets
  GET /api/tech-catalog/data-sets                → DataSet assets
  GET /api/tech-catalog/apis                     → DeployedAPI assets
  GET /api/tech-catalog/software-components      → DeployedSoftwareComponent processes
  GET /api/tech-catalog/actions                  → Action processes
  GET /api/tech-catalog/assets/{guid}            → detail for any element by GUID
  GET /api/tech-catalog/assets/{guid}/schema     → schema type + attribute tree (depth=5)
  GET /api/tech-catalog/assets/{guid}/lineage    → lineage graph via AssetCatalog

  GET /api/tech-catalog/tech-types               → list / search technology types
  GET /api/tech-catalog/tech-types/hierarchy     → hierarchy tree from root
  GET /api/tech-catalog/tech-types/{qualifiedName}          → detail by qualifiedName
  GET /api/tech-catalog/tech-types/{qualifiedName}/elements → catalog instances of this type
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


def _unwrap_rel_item(item: dict, key: str) -> Optional[dict]:
    """
    Convert one RelatedMetadataElementSummary into a normalised relationship dict,
    or return None if the item doesn't look like a relationship.
    """
    _ITEM_META = {"relationshipHeader", "relationshipProperties",
                  "relatedElement", "relatedElementAtEnd1", "class"}
    rel_hdr = item.get("relationshipHeader")
    if not isinstance(rel_hdr, dict):
        return None
    rel_type = (rel_hdr.get("type") or {}).get("typeName") or key
    rel_props_raw = item.get("relationshipProperties") or {}
    rel_props = _flat_props(rel_props_raw) if rel_props_raw else {}
    nested = item.get("relatedElement")
    if isinstance(nested, dict) and "elementHeader" in nested:
        elem = nested
    else:
        elem = {k: v for k, v in item.items() if k not in _ITEM_META}
    elem_hdr  = _header(elem)
    elem_props = _props(elem)
    type_info  = elem_hdr.get("type") or {}
    return {
        "relationshipType": rel_type,
        "relationshipProperties": rel_props,
        "relatedElement": {
            "guid":        elem_hdr.get("guid", ""),
            "typeName":    type_info.get("typeName", ""),
            "superTypes":  type_info.get("superTypeNames") or [],
            "displayName": elem_props.get("displayName") or elem_props.get("name") or elem_hdr.get("guid", ""),
            "description": elem_props.get("description") or "",
        },
    }


def _extract_relationships(el: dict) -> list:
    """
    Extract peer relationships from a graph-queried element.

    Handles both:
    - List-valued keys: each item is a RelatedMetadataElementSummary
    - Single-dict keys: e.g. 'schemaType' which is a single RelatedMetadataElementSummary
    """
    _SKIP_KEYS = {"elementHeader", "properties", "classifications", "class"}
    result = []
    for key, val in el.items():
        if key in _SKIP_KEYS:
            continue
        # Single-dict relationship (e.g. schemaType)
        if isinstance(val, dict):
            if val.get("relationshipHeader"):
                r = _unwrap_rel_item(val, key)
                if r:
                    result.append(r)
            continue
        if not isinstance(val, list):
            continue
        for item in val:
            if not isinstance(item, dict):
                continue
            r = _unwrap_rel_item(item, key)
            if r:
                result.append(r)
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
    # Signal sub-panes available in the detail view
    out["hasSchema"]  = isinstance(el.get("schemaType"), dict) and "relatedElement" in el.get("schemaType", {})
    out["hasLineage"] = True  # always offer lineage pane; empty graph shows graceful message
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


def _asset_catalog(url, server, user_id, user_pwd):
    from pyegeria import AssetCatalog
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    ac = AssetCatalog(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    ac.create_egeria_bearer_token()
    return ac


def _automated_curation(url, server, user_id, user_pwd):
    from pyegeria import AutomatedCuration
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    ac = AutomatedCuration(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    ac.create_egeria_bearer_token()
    return ac


def _serialize_schema(el: dict) -> dict:
    """Flatten the schemaType + nested attribute tree into a UI-friendly structure."""
    if not el:
        return {"schemaType": None, "attributes": []}
    st = el.get("schemaType")
    if not isinstance(st, dict):
        return {"schemaType": None, "attributes": []}
    re = st.get("relatedElement", {})
    rehdr = re.get("elementHeader", {})
    reprops = re.get("properties", {})
    type_info = rehdr.get("type") or {}
    schema_type = {
        "guid":        rehdr.get("guid", ""),
        "typeName":    type_info.get("typeName", ""),
        "displayName": reprops.get("displayName") or reprops.get("qualifiedName", ""),
        "description": reprops.get("description", ""),
    }
    attributes = []
    _SCHEMA_META = {"elementHeader", "properties", "class"}
    for key, arr in re.items():
        if key in _SCHEMA_META or not isinstance(arr, list):
            continue
        for item in arr:
            if not isinstance(item, dict):
                continue
            r = _unwrap_rel_item(item, key)
            if not r:
                continue
            ri = r["relatedElement"]
            # Also fetch inner scalar props from the relatedElement directly
            nested_elem = item.get("relatedElement", {})
            p = _props(nested_elem)
            flat = _flat_props(p)
            attributes.append({
                "guid":        ri["guid"],
                "typeName":    ri["typeName"],
                "displayName": ri["displayName"],
                "description": ri["description"],
                "dataType":    flat.get("dataType") or p.get("dataType", ""),
                "position":    flat.get("position") or p.get("position"),
                "required":    flat.get("required") or p.get("isNullable") == "false",
                "extraProps":  {k: v for k, v in flat.items()
                                if k not in ("displayName","qualifiedName","description","dataType","position","required","isNullable")},
            })
    attributes.sort(key=lambda a: (a.get("position") is None, a.get("position") or 0))
    return {"schemaType": schema_type, "attributes": attributes}


def _serialize_lineage(lin: dict) -> dict:
    """Flatten an AssetCatalog lineage graph response into a UI-friendly list."""
    if not lin:
        return {"relationships": []}
    result = []
    for key in ("lineageLinkage", "lineageRelationships"):
        for item in (lin.get(key) or []):
            if not isinstance(item, dict):
                continue
            r = _unwrap_rel_item(item, key)
            if r:
                result.append(r)
    return {"relationships": result}


def _serialize_tech_type(el: dict) -> dict:
    """Serialise a technology type list element (flat ValidMetadataValue dict)."""
    templates = el.get("catalogTemplates") or []
    return {
        "guid":          el.get("technologyTypeGUID") or el.get("guid") or "",
        "qualifiedName": el.get("qualifiedName") or "",
        "displayName":   el.get("displayName") or el.get("name") or "",
        "description":   el.get("description") or "",
        "category":      el.get("category") or "",
        "templateCount": len(templates) if isinstance(templates, list) else 0,
    }


def _normalize_placeholder(ph: dict) -> dict:
    """Normalise a placeholder property dict — handles both naming conventions."""
    return {
        "name":        ph.get("placeholderPropertyName") or ph.get("name") or "",
        "dataType":    ph.get("placeholderPropertyDataType") or ph.get("dataType") or "string",
        "required":    ph.get("required") is True or ph.get("required") == "true",
        "example":     ph.get("example") or ph.get("exampleValue") or "",
        "description": ph.get("description") or "",
    }


def _normalize_request_param(p: dict) -> dict:
    return {
        "name":        p.get("name") or p.get("parameterName") or "",
        "dataType":    p.get("dataType") or "string",
        "required":    p.get("required") is True or p.get("required") == "true",
        "description": p.get("description") or "",
        "example":     p.get("example") or "",
    }


def _serialize_tech_type_detail(el: dict) -> dict:
    """Serialise a technology type detail element for the UI."""
    base = _serialize_tech_type(el)

    # Mermaid graphs
    for field in ("mermaidGraph", "specificationMermaidGraph"):
        val = el.get(field)
        if val and isinstance(val, str) and not val.lower().startswith("no "):
            base[field] = val

    # --- Catalog Templates ---
    raw_templates = el.get("catalogTemplates") or []
    templates = []
    for t in raw_templates:
        if not isinstance(t, dict):
            continue
        rel_el = (t.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        rel_hdr   = rel_el.get("elementHeader") or {}
        spec = t.get("specification") or {}
        raw_placeholders = spec.get("placeholderProperty") or []
        placeholders = [_normalize_placeholder(p) for p in raw_placeholders if isinstance(p, dict)]
        # Sort: required first
        placeholders.sort(key=lambda p: (not p["required"], p["name"].lower()))
        templates.append({
            "displayName": t.get("displayName") or rel_props.get("displayName") or "",
            "description": t.get("description") or rel_props.get("description") or "",
            "guid":        (rel_hdr.get("guid") or rel_el.get("guid") or
                            t.get("guid") or ""),
            "resourceUse": t.get("resourceUse") or "",
            "placeholders": placeholders,
        })
    base["catalogTemplates"] = templates

    # --- Governance Processes ---
    raw_processes = el.get("governanceActionProcesses") or []
    processes = []
    for gp in raw_processes:
        if not isinstance(gp, dict):
            continue
        rel_el    = (gp.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        rel_hdr   = rel_el.get("elementHeader") or {}
        spec = gp.get("specification") or {}
        raw_params = spec.get("supportedRequestParameter") or []
        params = [_normalize_request_param(p) for p in raw_params if isinstance(p, dict)]
        params.sort(key=lambda p: (not p["required"], p["name"].lower()))
        processes.append({
            "displayName": gp.get("displayName") or rel_props.get("displayName") or "",
            "description": gp.get("description") or rel_props.get("description") or "",
            "guid":        rel_hdr.get("guid") or rel_el.get("guid") or gp.get("guid") or "",
            "resourceUse": gp.get("resourceUse") or "",
            "parameters":  params,
        })
    base["governanceProcesses"] = processes

    # --- External References ---
    raw_refs = el.get("externalReferences") or []
    ext_refs = []
    for ref in raw_refs:
        if not isinstance(ref, dict):
            continue
        rel_el    = (ref.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        ext_refs.append({
            "displayName": ref.get("displayName") or rel_props.get("displayName") or "",
            "description": ref.get("description") or rel_props.get("description") or "",
            "url":         ref.get("url") or rel_props.get("url") or "",
        })
    base["externalReferences"] = ext_refs

    return base


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


@router.get("/api/tech-catalog/assets/{guid}/schema")
def get_asset_schema(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the schema type + attribute tree for any asset with a Schema relationship."""
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd)
        raw = mgr.get_asset_by_guid(
            asset_guid=guid,
            output_format="JSON",
            body={
                "class": "GetRequestBody",
                "graphQueryDepth": 5,
                "relationshipsPageSize": 200,
                "includeOnlyRelationships": ["Schema", "AttributeForSchema"],
            },
        )
        el = raw[0] if isinstance(raw, list) else raw
        return JSONResponse(_serialize_schema(el or {}))
    except Exception as exc:
        logger.exception("get_asset_schema failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/assets/{guid}/lineage")
def get_asset_lineage(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the mermaid lineage graph string for any asset via AssetCatalog.

    Returns {"mermaidGraph": ""} when the asset has no lineage data (Egeria returns 400).
    """
    try:
        ac = _asset_catalog(url, server, user_id, user_pwd)
        mermaid_str = ac.get_asset_lineage_mermaid_graph(asset_guid=guid)
        return JSONResponse({"mermaidGraph": mermaid_str or ""})
    except Exception as exc:
        exc_str = str(exc)
        # Egeria returns 400 when no lineage data exists for the asset; treat as empty
        if "400" in exc_str or "CLIENT_ERROR_400" in exc_str:
            return JSONResponse({"mermaidGraph": ""})
        logger.exception("get_asset_lineage failed")
        raise HTTPException(status_code=500, detail=exc_str)


# ── Technology Types routes ───────────────────────────────────────────────────
# IMPORTANT: register hierarchy and elements routes BEFORE the parametric
# {qualified_name} route to avoid "hierarchy" or "{qn}/elements" being captured
# as a qualifiedName value.

@router.get("/api/tech-catalog/tech-types/hierarchy")
def get_tech_type_hierarchy(
    root: str = Query("Root Technology Type"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the technology type hierarchy tree starting from root."""
    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        raw = ac.get_tech_type_hierarchy(filter_string=root or "Root Technology Type",
                                         output_format="JSON")
        return JSONResponse({"hierarchy": raw})
    except Exception as exc:
        logger.exception("get_tech_type_hierarchy failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/tech-types")
def list_tech_types(
    q: str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """List or search technology types."""
    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        raw = ac.find_technology_types(
            search_string=q or "*",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
        )
        items = [_serialize_tech_type(e) for e in _safe_list(raw)]
        items.sort(key=lambda x: x.get("displayName", "").lower())
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_tech_types failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/tech-types/{qualified_name:path}/elements")
def get_tech_type_elements(
    qualified_name: str,
    display_name: str = Query(""),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return catalog instances of the given technology type.

    get_technology_type_elements requires the displayName (exact match, no wildcards).
    Pass it via the ?display_name= query param, populated from the already-loaded detail.
    Falls back to qualifiedName if display_name is absent.
    """
    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        filter_str = display_name or qualified_name.split(":")[-1] if ":" in qualified_name else qualified_name
        raw = ac.get_technology_type_elements(
            filter_string=filter_str,
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("get_tech_type_elements failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/tech-types/{qualified_name:path}")
def get_tech_type_detail(
    qualified_name: str,
    display_name: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a technology type.

    get_tech_type_detail (the underlying /technology-types/by-name call) matches
    by displayName only.  The frontend must pass ?display_name= alongside the
    qualifiedName path param so the lookup uses the correct display name.
    Falls back to qualified_name if display_name is not supplied.
    """
    filter_str = display_name or qualified_name
    try:
        ac = _automated_curation(url, server, user_id, user_pwd)
        raw = ac.get_tech_type_detail(filter_string=filter_str, output_format="JSON")
        el = raw[0] if isinstance(raw, list) else raw
        if not isinstance(el, dict):
            raise HTTPException(status_code=404, detail=f"Technology type {filter_str!r} not found")
        return JSONResponse(_serialize_tech_type_detail(el))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_tech_type_detail failed")
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
    Fetch a single element with full property/relationship/mermaid detail.
    Endpoints use ConnectionMaker.get_endpoint_by_guid (not an Asset subtype).
    All Asset subtypes use AssetCatalog.get_asset_graph for richer mermaid graphs,
    with fallback to get_asset_by_guid for types the graph endpoint can't serve.
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

    # All Asset types (infrastructure, software-capabilities, data assets, APIs, processes):
    # use AssetCatalog.get_asset_graph — returns the full anchored-element graph plus
    # more complete mermaid diagrams than get_asset_by_guid.
    try:
        ac = _asset_catalog_from_asset_maker(mgr)
        raw = ac.get_asset_graph(asset_guid=guid, output_format="JSON")
        el = raw[0] if isinstance(raw, list) else raw
        if el and isinstance(el, dict):
            # Inject the dedicated asset mermaid graph if not already embedded in the element.
            if not el.get("mermaidGraph") and not (el.get("properties") or {}).get("mermaidGraph"):
                try:
                    mermaid_str = ac.get_asset_mermaid_graph(guid)
                    if mermaid_str and not str(mermaid_str).lower().startswith("no "):
                        el["mermaidGraph"] = mermaid_str
                except Exception:
                    pass
            return el
    except Exception:
        pass

    # Fallback: targeted finders for non-standard Asset types
    finder = _SECTION_FINDERS.get(section or "")
    if finder:
        try:
            return _find_by_guid(finder(mgr), guid)
        except Exception:
            pass

    # Fallback: get_asset_by_guid
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

    # Last resort: SoftwareCapability finder
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


def _asset_catalog_from_asset_maker(mgr):
    """Create an AssetCatalog sharing credentials from an existing AssetMaker."""
    from pyegeria import AssetCatalog
    ac = AssetCatalog(
        view_server=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    ac.create_egeria_bearer_token()
    return ac


def _find_by_guid(raw, guid: str):
    """Filter a list result from find_* to return the single element matching guid."""
    for el in _safe_list(raw):
        if _header(el).get("guid") == guid:
            return el
    return None
