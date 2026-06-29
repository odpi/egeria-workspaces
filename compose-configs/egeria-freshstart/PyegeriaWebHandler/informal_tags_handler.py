"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Informal Tags Explorer — FastAPI router.

Uses ClassificationExplorer (ClassificationManager extends Client2) because the
informal-tag methods (find_tags, get_tag_by_guid, get_elements_by_tag) live on
Client2 in the installed pyegeria and are therefore available on any Client2
subclass — including ClassificationExplorer which is already used and verified
working in this container.

Endpoints:
  GET /api/informal-tags          → list / filter all informal tags
  GET /api/informal-tags/{guid}   → full detail for a tag (includes tagged elements)
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["informal-tags"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _serialize_tagged_element(entry: dict) -> dict:
    """Serialize one item from the elementList returned by get_elements_by_tag."""
    rel_el  = entry.get("relatedElement") or {}
    el_type = rel_el.get("type") or {}
    return {
        "guid":         rel_el.get("guid", ""),
        "typeName":     el_type.get("typeName", ""),
        "superTypeNames": el_type.get("superTypeNames") or [],
        "displayName":  rel_el.get("uniqueName") or "",
    }


def _serialize_tag(element: dict, tagged_elements=None) -> dict:
    """Serialize a tag element returned by find_tags / get_tag_by_guid (output_format=JSON)."""
    props  = element.get("properties") or {}
    header = element.get("elementHeader") or {}
    h_type = header.get("type") or {}
    return {
        "guid":           header.get("guid", ""),
        "name":           props.get("displayName") or props.get("name") or "",
        "description":    props.get("description") or "",
        "isPrivateTag":   props.get("isPrivateTag", False),
        "qualifiedName":  props.get("qualifiedName") or "",
        "typeName":       h_type.get("typeName", "InformalTag"),
        "taggedElements": tagged_elements or [],
    }


@router.get("/api/informal-tags", summary="List / search all informal tags")
def list_informal_tags(
    search_string: str = Query("*", description="Filter string; '*' returns all"),
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
        logger.exception("Failed to create manager for informal tag list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # find_tags on Client2 takes search_string directly (not a body dict)
    filter_str = "" if search_string == "*" else search_string
    try:
        raw = mgr.find_tags(
            search_string=filter_str,
            starts_with=False,
            ends_with=False,
            ignore_case=True,
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
        )
    except Exception as exc:
        logger.exception("find_tags failed")
        raise HTTPException(status_code=500, detail=f"Informal tag retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    tags = [_serialize_tag(e) for e in raw if isinstance(e, dict)]
    tags.sort(key=lambda x: (x.get("name") or "").lower())
    return JSONResponse({"tags": tags, "total": len(tags)})


@router.get("/api/informal-tags/{guid}", summary="Get full detail for an informal tag")
def get_informal_tag(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create manager for informal tag detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_tag_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_tag_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Informal tag retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Informal tag {guid!r} not found")

    tagged_elements = []
    try:
        raw_els = mgr.get_elements_by_tag(tag_guid=guid)
        element_list = raw_els.get("elementList") or [] if isinstance(raw_els, dict) else []
        for entry in element_list:
            if isinstance(entry, dict) and "relatedElement" in entry:
                el = _serialize_tagged_element(entry)
                if el.get("guid"):
                    tagged_elements.append(el)
    except Exception as exc:
        logger.warning(f"get_elements_by_tag failed for {guid}: {exc}")

    return JSONResponse(_serialize_tag(element, tagged_elements))
