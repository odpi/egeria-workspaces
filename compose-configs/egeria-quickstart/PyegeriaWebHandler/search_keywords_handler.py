"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Search Keywords Explorer — FastAPI router.

Endpoints:
  GET /api/search-keywords          → list / filter all search keywords
  GET /api/search-keywords/{guid}   → full detail for a keyword (includes tagged elements)
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["search-keywords"])


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


def _serialize_keyword_element(entry: dict) -> dict:
    re = entry.get("relatedElement") or {}
    rh = re.get("elementHeader") or {}
    rp = re.get("properties") or {}
    rtype = rh.get("type") or {}
    return {
        "guid":         rh.get("guid", ""),
        "typeName":     rtype.get("typeName", ""),
        "superTypeNames": rtype.get("superTypeNames") or [],
        "displayName":  rp.get("displayName") or rp.get("name") or "",
        "description":  rp.get("description") or "",
        "category":     rp.get("category") or "",
        "qualifiedName": rp.get("qualifiedName") or "",
    }


def _serialize_keyword(element: dict) -> dict:
    props  = element.get("properties") or {}
    header = element.get("elementHeader") or {}
    keyword_elements_raw = element.get("keywordElements") or []
    keyword_elements = []
    for entry in keyword_elements_raw:
        if isinstance(entry, dict) and "relatedElement" in entry:
            el = _serialize_keyword_element(entry)
            if el.get("guid"):
                keyword_elements.append(el)
    return {
        "guid":            header.get("guid", ""),
        "keyword":         props.get("keyword", ""),
        "description":     props.get("description") or "",
        "status":          header.get("status") or "",
        "keywordElements": keyword_elements,
    }


@router.get("/api/search-keywords", summary="List / search all search keywords")
def list_search_keywords(
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
        logger.exception("Failed to create ClassificationExplorer manager for keyword list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_search_keywords(
            search_string=search_string,
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
        )
    except Exception as exc:
        logger.exception("find_search_keywords failed")
        raise HTTPException(status_code=500, detail=f"Search keyword retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    keywords = [_serialize_keyword(e) for e in raw if isinstance(e, dict)]
    keywords.sort(key=lambda x: (x.get("keyword") or "").lower())
    return JSONResponse({"keywords": keywords, "total": len(keywords)})


@router.get("/api/search-keywords/{guid}", summary="Get full detail for a search keyword")
def get_search_keyword(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer manager for keyword detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_search_keyword_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_search_keyword_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Search keyword detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Search keyword {guid!r} not found")

    return JSONResponse(_serialize_keyword(element))
