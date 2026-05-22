"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Data Design Explorer — FastAPI router.

Type hierarchy (https://egeria-project.org/types/5/):
  DataSpec        → subtype of Collection (use CollectionManager.find_collections / get_collection)
  DataStructure   → use DataDesigner.find_data_structures / get_data_structure_by_guid
  DataField       → use DataDesigner.find_data_fields / get_data_field_by_guid; sub-fields nest inside
  DataGrain       → subtype of DataValueSpecification (use _search_data_value_specs + typeName filter)
  DataClass       → subtype of DataValueSpecification (same endpoint as DataGrain, different typeName)

Note: DataValueSpecification defines *values*, not structure.  DataSpec/Structure/Field define structure.
DataDesigner.find_data_value_specifications is broken (calls self._async_post, absent ≤6.0.12.3);
  _search_data_value_specs() calls /by-search-string directly as a workaround.

Endpoints:
  GET /api/data-design/specs              → list all Data Specs (Collection subtype)
  GET /api/data-design/specs/{guid}       → detail for a Data Spec
  GET /api/data-design/structures         → list all Data Structures
  GET /api/data-design/structures/{guid}  → detail for a Data Structure
  GET /api/data-design/fields             → list all Data Fields
  GET /api/data-design/fields/{guid}      → detail for a Data Field
  GET /api/data-design/grains             → list all Data Grains (subtype of DataValueSpecification)
  GET /api/data-design/grains/{guid}      → detail for a Data Grain
"""

import asyncio
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["data-design"])


def _get_designer(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import DataDesigner
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = DataDesigner(server, url, user_id, user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_collection_mgr(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import CollectionManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = CollectionManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr



def _props(el: dict) -> dict:
    return el.get("properties") or {}


def _header(el: dict) -> dict:
    return el.get("elementHeader") or {}


def _type_name(el: dict) -> str:
    return (_header(el).get("type") or {}).get("typeName", "") or ""


def _base(el: dict) -> dict:
    p = _props(el)
    return {
        "guid":          _header(el).get("guid", ""),
        "typeName":      _type_name(el),
        "displayName":   p.get("displayName", "") or p.get("name", "") or "",
        "qualifiedName": p.get("qualifiedName", "") or "",
        "description":   p.get("description", "") or "",
    }


def _zip_refs(guids: list, names: list, qnames: list = None) -> list:
    """Zip parallel guid/name/qname arrays into [{guid, displayName, qualifiedName}]."""
    qnames = qnames or []
    return [
        {
            "guid":          guids[i],
            "displayName":   names[i] if i < len(names) else "",
            "qualifiedName": qnames[i] if i < len(qnames) else "",
        }
        for i in range(len(guids or []))
    ]


def _safe_list(raw) -> list:
    return raw if isinstance(raw, list) else []


def _search_data_value_specs(mgr) -> list:
    """Call /by-search-string directly — find_data_value_specifications uses _async_post (absent ≤6.0.12.3)."""
    endpoint = (
        f"{mgr.platform_url}/servers/{mgr.view_server}"
        f"/api/open-metadata/data-designer/data-value-specifications/by-search-string"
    )
    body = {"class": "SearchStringRequestBody", "searchString": "", "startFrom": 0, "pageSize": 500}
    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(mgr._async_make_request("POST", endpoint, body))
    if hasattr(resp, "json"):
        return resp.json().get("elements", []) or []
    if isinstance(resp, dict):
        return resp.get("elements", []) or []
    return []


def _first(raw) -> dict | None:
    if isinstance(raw, list):
        return raw[0] if raw else None
    if isinstance(raw, dict):
        return raw
    return None


def _rels(mgr, element: dict) -> dict:
    try:
        return mgr.get_data_rel_elements_dict(element) or {}
    except Exception:
        return {}


def _extract_all_rels(element: dict) -> dict:
    """
    Scan every list key in an element response and extract related-element entries.
    Returns {fieldKey: [{guid, displayName, qualifiedName, typeName}, ...]} for
    every non-empty relationship list found, regardless of relationship type.
    Skips structural keys (elementHeader, properties, mermaidGraph).
    """
    SKIP = {"elementHeader", "properties", "mermaidGraph"}
    result = {}
    for key, val in element.items():
        if key in SKIP or not isinstance(val, list) or not val:
            continue
        items = []
        for entry in val:
            re = entry.get("relatedElement") or entry
            rh = re.get("elementHeader") or {}
            rp = re.get("properties") or {}
            g  = rh.get("guid") or re.get("guid") or ""
            if g:
                items.append({
                    "guid":          g,
                    "displayName":   rp.get("displayName") or rp.get("name") or "",
                    "qualifiedName": rp.get("qualifiedName") or "",
                    "typeName":      (rh.get("type") or {}).get("typeName") or "",
                })
        if items:
            result[key] = items
    return result


def _serialize_spec(el: dict) -> dict:
    p = _props(el)
    n = _base(el)
    n.update({
        "versionIdentifier": p.get("versionIdentifier", "") or "",
        "namespace":         p.get("namespace", "") or p.get("namespacePath", "") or "",
        "mermaidGraph":      el.get("mermaidGraph", "") or p.get("mermaidGraph", "") or "",
    })
    return n


def _serialize_structure(el: dict) -> dict:
    p = _props(el)
    n = _base(el)
    n.update({
        "versionIdentifier": p.get("versionIdentifier", "") or "",
        "namespace":         p.get("namespace", "") or p.get("namespacePath", "") or "",
        "mermaidGraph":      el.get("mermaidGraph", "") or p.get("mermaidGraph", "") or "",
    })
    return n


def _serialize_field(el: dict) -> dict:
    p = _props(el)
    n = _base(el)
    n.update({
        "dataType":      p.get("dataType", "") or "",
        "isNullable":    bool(p.get("isNullable", False)),
        "defaultValue":  p.get("defaultValue", "") or "",
        "minimumLength": p.get("minimumLength", 0) or 0,
        "length":        p.get("length", 0) or 0,
        "mermaidGraph":  el.get("mermaidGraph", "") or p.get("mermaidGraph", "") or "",
    })
    return n


def _serialize_grain(el: dict) -> dict:
    p = _props(el)
    n = _base(el)
    n.update({
        "dataType":    p.get("dataType", "") or "",
        "mermaidGraph": el.get("mermaidGraph", "") or p.get("mermaidGraph", "") or "",
    })
    return n


# ── List endpoints ─────────────────────────────────────────────────────────────

@router.get("/api/data-design/specs", summary="List all Data Specs (Collection subtype)")
def list_specs(
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_collection_mgr(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.find_collections(search_string="*", metadata_element_type="DataSpec",
                                    graph_query_depth=0, output_format="JSON")
        items = sorted(
            [_serialize_spec(e) for e in _safe_list(raw)],
            key=lambda x: (x.get("displayName") or "").lower(),
        )
        return JSONResponse({"specs": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_specs failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/structures", summary="List all Data Structures")
def list_structures(
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.find_data_structures(search_string="*", graph_query_depth=0, output_format="JSON")
        items = sorted([_serialize_structure(e) for e in _safe_list(raw)],
                       key=lambda x: (x.get("displayName") or "").lower())
        return JSONResponse({"structures": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_structures failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/fields", summary="List all Data Fields")
def list_fields(
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.find_data_fields(search_string="*", graph_query_depth=0, output_format="JSON")
        items = sorted([_serialize_field(e) for e in _safe_list(raw)],
                       key=lambda x: (x.get("displayName") or "").lower())
        return JSONResponse({"fields": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_fields failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/grains", summary="List all Data Grains")
def list_grains(
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = _search_data_value_specs(mgr)
        items = sorted(
            [_serialize_grain(e) for e in _safe_list(raw) if _type_name(e) == "DataGrain"],
            key=lambda x: (x.get("displayName") or "").lower(),
        )
        return JSONResponse({"grains": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_grains failed")
        raise HTTPException(status_code=500, detail=str(exc))


# ── Detail endpoints ───────────────────────────────────────────────────────────

@router.get("/api/data-design/specs/{guid}", summary="Detail for a Data Spec")
def get_spec(
    guid: str,
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_collection_mgr(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.get_collection_by_guid(guid, output_format="JSON")
        element = _first(raw)
        if not element:
            raise HTTPException(status_code=404, detail=f"Spec {guid!r} not found")
        node = _serialize_spec(element)
        # Fetch members separately — get_collection_by_guid doesn't traverse relationships
        members = []
        try:
            members_raw = mgr.get_collection_members(
                collection_guid=guid,
                output_format="JSON",
                page_size=200,
                body={"class": "ResultsRequestBody", "graphQueryDepth": 0},
            )
            for m in _safe_list(members_raw):
                rh = (m.get("elementHeader") or {})
                rp = (m.get("properties") or {})
                g  = rh.get("guid", "")
                if g:
                    members.append({
                        "guid":          g,
                        "displayName":   rp.get("displayName") or rp.get("name") or "",
                        "qualifiedName": rp.get("qualifiedName") or "",
                        "typeName":      (rh.get("type") or {}).get("typeName") or "",
                    })
        except Exception:
            logger.warning(f"get_collection_members failed for DataSpec {guid}")
        rels = _extract_all_rels(element)
        # Inject the reliably-fetched collection members (get_collection_by_guid
        # doesn't traverse depth, so collectionMembers won't be in the element)
        if members:
            rels["collectionMembers"] = members
        node["relationships"] = rels
        return JSONResponse(node)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_spec failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/structures/{guid}", summary="Detail for a Data Structure")
def get_structure(
    guid: str,
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.get_data_structure_by_guid(guid, output_format="JSON")
        element = _first(raw)
        if not element:
            raise HTTPException(status_code=404, detail=f"Structure {guid!r} not found")
        node = _serialize_structure(element)
        node["relationships"] = _extract_all_rels(element)
        return JSONResponse(node)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_structure failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/fields/{guid}", summary="Detail for a Data Field")
def get_field(
    guid: str,
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.get_data_field_by_guid(guid, output_format="JSON")
        element = _first(raw)
        if not element:
            raise HTTPException(status_code=404, detail=f"Field {guid!r} not found")
        node = _serialize_field(element)
        node["relationships"] = _extract_all_rels(element)
        return JSONResponse(node)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_field failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/data-design/grains/{guid}", summary="Detail for a Data Grain")
def get_grain(
    guid: str,
    url:     Optional[str] = Query(None),
    server:  Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd:Optional[str] = Query(None),
):
    try:
        mgr = _get_designer(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        raw = mgr.get_data_grain_by_guid(guid, output_format="JSON")
        element = _first(raw)
        if not element:
            raise HTTPException(status_code=404, detail=f"Grain {guid!r} not found")
        node = _serialize_grain(element)
        node["relationships"] = _extract_all_rels(element)
        return JSONResponse(node)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_grain failed")
        raise HTTPException(status_code=500, detail=str(exc))
