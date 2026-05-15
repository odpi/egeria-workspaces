"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Glossary Explorer — FastAPI router.

Endpoints:
  GET /api/glossary                           → list all glossaries
  GET /api/glossary/{guid}/folders            → CollectionFolder children of a glossary
  GET /api/glossary/{guid}/terms              → terms in a glossary or folder (by collection membership)
  GET /api/glossary-terms                     → cross-glossary term search
  GET /api/glossary/term/{guid}               → full detail for a single term
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["glossary"])


def _get_manager():
    from pyegeria import GlossaryManager
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = GlossaryManager(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _serialize_glossary(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "displayName":   props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName": props.get("qualifiedName", "") or "",
        "description":   props.get("description", "") or "",
        "language":      props.get("language", "") or "",
        "usage":         props.get("usage", "") or "",
        "status":        header.get("status", "") or "",
    }


def _serialize_folder(element: dict) -> dict:
    """Serialise a CollectionFolder element returned by get_collection_members."""
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "typeName":      _type_name(element),
        "displayName":   props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName": props.get("qualifiedName", "") or "",
        "description":   props.get("description", "") or "",
        "status":        header.get("status", "") or "",
        "contentStatus": props.get("contentStatus", "") or "",
    }


def _collection_guids(term: dict) -> set:
    """Return the set of GUIDs for all collections this term is a member of."""
    guids = set()
    for col in (term.get("memberOfCollections") or []):
        re = col.get("relatedElement") or {}
        g = (re.get("elementHeader") or {}).get("guid", "")
        if g:
            guids.add(g)
    return guids


def _folder_memberships(term: dict) -> list:
    """Return [{guid, displayName}] for CollectionFolder memberships of this term."""
    folders = []
    for col in (term.get("memberOfCollections") or []):
        re    = col.get("relatedElement") or {}
        rh    = re.get("elementHeader") or {}
        rp    = re.get("properties") or {}
        tn    = (rh.get("type") or {}).get("typeName", "")
        if "Folder" in tn or "Collection" in tn:
            g = rh.get("guid", "")
            n = rp.get("displayName") or rp.get("name") or ""
            if g and "Glossary" not in tn:  # Exclude the Glossary itself
                folders.append({"guid": g, "displayName": n})
    return folders


def _serialize_term(term: dict) -> dict:
    props  = _props(term)
    header = _header(term)
    return {
        "guid":            header.get("guid", ""),
        "typeName":        _type_name(term),
        "displayName":     props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":   props.get("qualifiedName", "") or "",
        "description":     props.get("description", "") or "",
        "abbreviation":    props.get("abbreviation", "") or "",
        "examples":        props.get("examples", "") or "",
        "usage":           props.get("usage", "") or "",
        "summary":         props.get("summary", "") or "",
        "status":          header.get("status", "") or "",
        "contentStatus":   props.get("contentStatus", "") or "",
        "activityStatus":  props.get("activityStatus", "") or "",
        "folders":         _folder_memberships(term),
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/glossary", summary="List all glossaries")
def get_glossaries(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(100, ge=1, le=500),
):
    """Return all Egeria glossaries with summary information."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_glossaries(
            search_string="*",
            starts_with=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_glossaries failed")
        raise HTTPException(status_code=500, detail=f"Glossary retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    glossaries = [_serialize_glossary(g) for g in raw
                  if _type_name(g) == "Glossary"]
    glossaries.sort(key=lambda g: (g.get("displayName") or "").lower())
    return JSONResponse({"glossaries": glossaries, "total": len(glossaries)})


@router.get("/api/glossary/{collection_guid}/folders", summary="List CollectionFolder children of a glossary")
def get_glossary_folders(
    collection_guid: str,
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=1000),
):
    """Return the CollectionFolder children of a glossary (organisational hierarchy)."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
        )
    except Exception as exc:
        logger.exception("get_collection_members failed")
        raise HTTPException(status_code=500, detail=f"Folder retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    folders = [_serialize_folder(f) for f in raw]
    folders.sort(key=lambda f: (f.get("displayName") or "").lower())
    return JSONResponse({"folders": folders, "total": len(folders), "collection": collection_guid})


@router.get("/api/glossary/{collection_guid}/terms", summary="Terms in a glossary or folder")
def get_terms_in_collection(
    collection_guid: str,
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(500, ge=1, le=2000),
):
    """
    Return GlossaryTerms that are members of the given collection (glossary or folder).

    Terms are detected by inspecting each term's memberOfCollections list for a matching GUID.
    This is the correct approach since GlossaryTerms link to their parent glossary/folder
    via CollectionMembership relationships, not via get_collection_members.
    """
    try:
        mgr = _get_manager()
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
            graph_query_depth=1,  # depth=1 needed to get memberOfCollections for filtering
        )
    except Exception as exc:
        logger.exception("find_glossary_terms failed")
        raise HTTPException(status_code=500, detail=f"Term retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    # Filter: term is in this collection if the collection GUID appears in memberOfCollections
    terms = [_serialize_term(t) for t in raw
             if collection_guid in _collection_guids(t)]
    terms.sort(key=lambda t: (t.get("displayName") or "").lower())
    return JSONResponse({"terms": terms, "total": len(terms), "collection": collection_guid})


@router.get("/api/glossary-terms", summary="Search all glossary terms across all glossaries")
def search_all_terms(
    q:          str = Query("*",   description="Search string; use * to return all"),
    start_from: int = Query(0,     ge=0),
    page_size:  int = Query(200,   ge=1, le=1000),
):
    """
    Search for GlossaryTerms across all glossaries using a text search string.
    Terms can belong to multiple glossaries; this view is independent of glossary membership.
    """
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    search_string = q.strip() if q and q.strip() else "*"
    try:
        raw = mgr.find_glossary_terms(
            search_string=search_string,
            starts_with=True,
            ignore_case=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
        )
    except Exception as exc:
        logger.exception("find_glossary_terms failed")
        raise HTTPException(status_code=500, detail=f"Term search failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    terms = [_serialize_term(t) for t in raw]
    terms.sort(key=lambda t: (t.get("displayName") or "").lower())
    return JSONResponse({"terms": terms, "total": len(terms), "query": search_string})


@router.get("/api/glossary/term/{term_guid}", summary="Get a single term by GUID")
def get_term(term_guid: str):
    """Return full detail for a single glossary term."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_term_by_guid(term_guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_term_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Term retrieval failed: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Term {term_guid!r} not found")

    return JSONResponse(_serialize_term(raw))
