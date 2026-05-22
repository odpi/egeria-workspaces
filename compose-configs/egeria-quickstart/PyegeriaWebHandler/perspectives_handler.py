"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Perspectives & Questions — FastAPI router.

Perspectives are actor-profile subtypes created via ActorManager.
Questions are GlossaryTerms with the IsQuestion classification, linked
to Perspectives via the ScopedBy relationship.

Endpoints:
  GET /api/perspectives              → list all Perspective elements
  GET /api/perspectives/{guid}       → full detail for a single Perspective
  GET /api/questions                 → list all GlossaryTerms with IsQuestion classification
  GET /api/questions/{guid}          → full detail for a single Question
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["perspectives"])


def _get_actor_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ActorManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ActorManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_glossary_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import GlossaryManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = GlossaryManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


_SKIP_KEYS = {"elementHeader", "properties", "mermaidGraph"}


def _extract_all_rels(element: dict) -> dict:
    """Extract all relationship lists → {key: [{guid, displayName, qualifiedName, typeName}]}."""
    result = {}
    for key, val in element.items():
        if key in _SKIP_KEYS or not isinstance(val, list) or not val:
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


def _serialize_perspective(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "typeName":      _type_name(element),
        "displayName":   props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName": props.get("qualifiedName", "") or "",
        "description":   props.get("description", "") or "",
        "category":      props.get("category", "") or "",
        "status":        header.get("status", "") or "",
        "mermaidGraph":  element.get("mermaidGraph", "") or props.get("mermaidGraph", "") or "",
        "relationships": _extract_all_rels(element),
    }


def _serialize_question(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "typeName":      _type_name(element),
        "displayName":   props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName": props.get("qualifiedName", "") or "",
        "description":   props.get("description", "") or "",
        "summary":       props.get("summary", "") or "",
        "usage":         props.get("usage", "") or "",
        "status":        header.get("status", "") or "",
        "mermaidGraph":  element.get("mermaidGraph", "") or props.get("mermaidGraph", "") or "",
        "relationships": _extract_all_rels(element),
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/perspectives", summary="List all Perspective actor profiles")
def get_perspectives(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return all Perspective elements from the metadata repository."""
    try:
        mgr = _get_actor_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ActorManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_actor_profiles(
            search_string="*",
            starts_with=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            metadata_element_type="Perspective",
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_actor_profiles (Perspective) failed")
        raise HTTPException(status_code=500, detail=f"Perspective retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    perspectives = [_serialize_perspective(p) for p in raw if _type_name(p) == "Perspective"]
    perspectives.sort(key=lambda p: (p.get("displayName") or "").lower())
    return JSONResponse({"perspectives": perspectives, "total": len(perspectives)})


@router.get("/api/perspectives/{perspective_guid}", summary="Get a single Perspective by GUID")
def get_perspective(
    perspective_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a single Perspective, including linked Questions via ScopedBy."""
    try:
        mgr = _get_actor_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ActorManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # get_actor_profile_by_guid enforces ActorProfile type server-side; Perspective is not an
    # ActorProfile subtype so that endpoint rejects it. Use find_actor_profiles with depth=1
    # (the working list endpoint) and filter by GUID client-side.
    try:
        raw_list = mgr.find_actor_profiles(
            search_string="*",
            starts_with=True,
            output_format="JSON",
            page_size=200,
            metadata_element_type="Perspective",
            graph_query_depth=1,
        )
    except Exception as exc:
        logger.exception("find_actor_profiles (detail) failed")
        raise HTTPException(status_code=500, detail=f"Perspective retrieval failed: {exc}")

    if not isinstance(raw_list, list):
        raise HTTPException(status_code=404, detail=f"Perspective {perspective_guid!r} not found")

    raw = next((p for p in raw_list if _header(p).get("guid") == perspective_guid), None)
    if not raw:
        raise HTTPException(status_code=404, detail=f"Perspective {perspective_guid!r} not found")

    return JSONResponse(_serialize_perspective(raw))


@router.get("/api/questions", summary="List all GlossaryTerms with IsQuestion classification")
def get_questions(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return all GlossaryTerms classified as Questions (IsQuestion classification)."""
    try:
        mgr = _get_glossary_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_glossary_terms(
            search_string="*",
            starts_with=True,
            ignore_case=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            include_only_classified_elements=["IsQuestion"],
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_glossary_terms (IsQuestion) failed")
        raise HTTPException(status_code=500, detail=f"Question retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    # Apply client-side filter as a correctness guarantee regardless of whether
    # the server-side include_only_classified_elements filter worked.
    seen: set = set()
    questions = []
    for t in raw:
        g = _header(t).get("guid", "")
        if g and g not in seen and _is_question(t):
            seen.add(g)
            questions.append(_serialize_question(t))
    questions.sort(key=lambda q: (q.get("displayName") or "").lower())
    logger.info(f"Questions found: {len(questions)} (from {len(raw)} raw terms)")
    return JSONResponse({"questions": questions, "total": len(questions)})


@router.get("/api/questions/{question_guid}", summary="Get a single Question by GUID")
def get_question(
    question_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a single Question (GlossaryTerm with IsQuestion classification)."""
    try:
        mgr = _get_glossary_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_term_by_guid(
            question_guid,
            output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1},
        )
    except Exception as exc:
        logger.exception("get_term_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Question retrieval failed: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Question {question_guid!r} not found")

    return JSONResponse(_serialize_question(raw))
