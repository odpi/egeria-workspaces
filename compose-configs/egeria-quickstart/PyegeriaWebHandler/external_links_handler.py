"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

External References Explorer — FastAPI router.

External references cover five subtypes, all returned together by
`find_external_references` / `get_external_reference_by_guid`:
  ExternalReference, RelatedMedia, CitedDocument, ExternalDataSource, ExternalModelSource

Endpoints:
  GET /api/external-references          → list / search all external references (all subtypes)
  GET /api/external-references/{guid}   → full detail, including referencing elements + mermaid graph
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["external-references"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ExternalReferences
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ExternalReferences(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


# Properties surfaced as dedicated fields; everything else in `properties` is
# passed through as `props` for generic per-subtype rendering on the frontend.
_COMMON_PROP_KEYS = {"class", "typeName", "qualifiedName", "displayName", "name", "description", "url"}


def _serialize_related(entry: dict) -> Optional[dict]:
    """Serialize one entry from the `referencingElements` list (RelatedMetadataElementSummary) —
    the elements this external reference is attached to."""
    rel_el = entry.get("relatedElement") or {}
    rh = rel_el.get("elementHeader") or {}
    rp = rel_el.get("properties") or {}
    rtype = rh.get("type") or {}
    guid = rh.get("guid", "")
    if not guid:
        return None
    rel_props = entry.get("relationshipProperties") or {}
    return {
        "guid":           guid,
        "typeName":       rtype.get("typeName", ""),
        "superTypeNames": rtype.get("superTypeNames") or [],
        "displayName":    rp.get("displayName") or rp.get("name") or "",
        "qualifiedName":  rp.get("qualifiedName") or "",
        "label":          rel_props.get("label") or "",
        "linkDescription": rel_props.get("description") or "",
    }


def _serialize_ext_ref(element: dict, include_relationships: bool = False) -> dict:
    props  = _props(element)
    header = _header(element)
    type_info   = header.get("type") or {}
    type_name   = type_info.get("typeName", "") or "ExternalReference"
    super_types = type_info.get("superTypeNames") or []

    result = {
        "guid":           header.get("guid", ""),
        "typeName":       type_name,
        "superTypeNames": super_types,
        "displayName":    props.get("displayName") or props.get("name") or "",
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "url":            props.get("url") or "",
        "status":         header.get("status") or "",
        "props":          {k: v for k, v in props.items() if k not in _COMMON_PROP_KEYS},
    }

    if include_relationships:
        referencing = []
        for entry in (element.get("referencingElements") or []):
            if isinstance(entry, dict):
                item = _serialize_related(entry)
                if item:
                    referencing.append(item)
        result["relationships"] = {"referencingElements": referencing} if referencing else {}
        result["mermaidGraph"] = element.get("mermaidGraph", "") or ""

    return result


@router.get("/api/external-references", summary="List / search all external references")
def list_external_references(
    search_string: str = Query("*", description="Filter string; '*' returns all"),
    type_name: Optional[str] = Query(None, description="Restrict to one subtype: ExternalReference, RelatedMedia, CitedDocument, ExternalDataSource, ExternalModelSource"),
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(500, ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ExternalReferences manager for list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_external_references(
            search_string=search_string,
            starts_with=False,
            ignore_case=True,
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
            output_format="JSON",
        )
    except Exception as exc:
        logger.exception("find_external_references failed")
        raise HTTPException(status_code=500, detail=f"External reference retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    references = [_serialize_ext_ref(e) for e in raw if isinstance(e, dict)]
    if type_name:
        references = [r for r in references if r["typeName"] == type_name]
    references.sort(key=lambda x: (x.get("typeName", ""), (x.get("displayName") or "").lower()))

    by_type: dict[str, int] = {}
    for r in references:
        by_type[r["typeName"]] = by_type.get(r["typeName"], 0) + 1

    return JSONResponse({"references": references, "total": len(references), "byType": by_type})


@router.get("/api/external-references/{guid}", summary="Get full detail for an external reference")
def get_external_reference(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ExternalReferences manager for detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_external_reference_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_external_reference_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"External reference detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"External reference {guid!r} not found")

    return JSONResponse(_serialize_ext_ref(element, include_relationships=True))
