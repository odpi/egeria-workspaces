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


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import GlossaryManager
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
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


# Semantic relationship keys returned by pyegeria on GlossaryTerm at graph_query_depth>=1.
_TERM_REL_KEYS = [
    ("synonyms",       "Synonyms"),
    ("antonyms",       "Antonyms"),
    ("translations",   "Translations"),
    ("preferredTerms", "Preferred Terms"),
    ("replacedTerms",  "Replaced By"),
    ("relatedTerms",   "Related Terms"),
    ("usedInContexts", "Used In Contexts"),
    ("categories",     "Categories"),
]

_TERM_REL_KEY_NAMES = {k for k, _ in _TERM_REL_KEYS}
_TERM_STRUCT_KEYS   = {"elementHeader", "properties", "mermaidGraph", "sourcedFromTemplate"}


def _camel_to_label(s: str) -> str:
    result = s[0].upper() if s else ''
    for c in s[1:]:
        result += (' ' + c) if c.isupper() else c
    return result


def _extract_extra_rels(term: dict) -> dict:
    """Scan term element keys not already in _TERM_REL_KEYS for relationship lists.
    Captures semantic assignments (DataFields etc.) whatever key name Egeria uses."""
    result = {}
    for key, val in term.items():
        if key in _TERM_REL_KEY_NAMES or key in _TERM_STRUCT_KEYS:
            continue
        if not isinstance(val, list) or not val:
            continue
        items = _related_elements(val)
        if items:
            result[_camel_to_label(key)] = items
    return result


def _related_elements(raw_list: list) -> list:
    """Extract [{guid, displayName, qualifiedName, typeName}] from a relationship list."""
    result = []
    for rel in (raw_list or []):
        re = rel.get("relatedElement") or {}
        rh = re.get("elementHeader") or {}
        rp = re.get("properties") or {}
        g  = rh.get("guid", "")
        if g:
            result.append({
                "guid":          g,
                "displayName":   rp.get("displayName") or rp.get("name") or "",
                "qualifiedName": rp.get("qualifiedName") or "",
                "typeName":      (rh.get("type") or {}).get("typeName") or "",
            })
    return result


def _serialize_glossary(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":            header.get("guid", ""),
        "displayName":     props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":   props.get("qualifiedName", "") or "",
        "description":     props.get("description", "") or "",
        "language":        props.get("language", "") or "",
        "usage":           props.get("usage", "") or "",
        "status":          header.get("status", "") or "",
        "classifications": _extract_classifications(header),
    }


def _serialize_folder(element: dict) -> dict:
    """Serialise a CollectionFolder element returned by get_collection_members."""
    props  = _props(element)
    header = _header(element)
    return {
        "guid":            header.get("guid", ""),
        "typeName":        _type_name(element),
        "displayName":     props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":   props.get("qualifiedName", "") or "",
        "description":     props.get("description", "") or "",
        "status":          header.get("status", "") or "",
        "contentStatus":   props.get("contentStatus", "") or "",
        "classifications": _extract_classifications(header),
    }


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


_SKIP_CLASSIFICATIONS = frozenset([
    "Anchors", "LatestChange", "Memento", "TemplateSubstitute", "SpineObject",
    "SpineAttribute", "ObjectIdentifier",
])

def _extract_classifications(header: dict) -> list:
    """Extract governance/business classifications from an elementHeader dict.

    In pyegeria's JSON output, each classification is a named key directly on
    elementHeader (e.g. "subjectArea", "zoneMembership"), not in a list.
    Every such value has class="ElementClassification".
    """
    result = []
    for key, val in header.items():
        if not isinstance(val, dict):
            continue
        if val.get("class") != "ElementClassification":
            continue
        cls_name = (val.get("classificationName")
                    or (val.get("type") or {}).get("typeName")
                    or (key[0].upper() + key[1:]))
        if not cls_name or cls_name in _SKIP_CLASSIFICATIONS:
            continue
        cls_props_raw = val.get("classificationProperties") or {}
        flat = {}
        if isinstance(cls_props_raw, dict):
            for k, v in cls_props_raw.items():
                if k in ("class", "typeName"):
                    continue
                if isinstance(v, list):
                    flat[k] = ", ".join(str(i) for i in v)
                elif not isinstance(v, (dict,)):
                    flat[k] = str(v)
        result.append({"typeName": cls_name, "properties": flat})
    return result


def _serialize_term(term: dict) -> dict:
    props  = _props(term)
    header = _header(term)
    # TemplateSubstitute is a classification stored as a sibling key in elementHeader,
    # not inside the classifications list.  SourcedFrom is a top-level relationship key.
    is_template_substitute  = bool(header.get("templateSubstitute"))
    is_sourced_from_template = bool(term.get("sourcedFromTemplate"))
    return {
        "guid":                   header.get("guid", ""),
        "typeName":               _type_name(term),
        "displayName":            props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":          props.get("qualifiedName", "") or "",
        "description":            props.get("description", "") or "",
        "abbreviation":           props.get("abbreviation", "") or "",
        "examples":               props.get("examples", "") or "",
        "usage":                  props.get("usage", "") or "",
        "summary":                props.get("summary", "") or "",
        "status":                 header.get("status", "") or "",
        "contentStatus":          props.get("contentStatus", "") or "",
        "activityStatus":         props.get("activityStatus", "") or "",
        "mermaidGraph":           term.get("mermaidGraph", "") or props.get("mermaidGraph", "") or "",
        "folders":                _folder_memberships(term),
        "isTemplateSubstitute":   is_template_substitute,
        "isSourcedFromTemplate":  is_sourced_from_template,
        "classifications":        _extract_classifications(header),
        "relationships":          {
                                      **{label: items for key, label in _TERM_REL_KEYS
                                         if (items := _related_elements(term.get(key)))},
                                      **_extract_extra_rels(term),
                                  },
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/glossary", summary="List all glossaries")
def get_glossaries(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return all Egeria glossaries with summary information."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
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
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
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
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return the CollectionFolder children of a glossary (organisational hierarchy)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
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
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """
    Return GlossaryTerms that are members of the given collection (glossary or folder).

    Uses get_collection_members which fetches only the members of this specific collection,
    then filters for GlossaryTerm type elements. Much faster than a full-table scan.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            body={"class": "ResultsRequestBody"},  # no metadataElementTypeName filter so GlossaryTerms are returned
        )
    except Exception as exc:
        logger.exception("get_collection_members failed")
        raise HTTPException(status_code=500, detail=f"Term retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    terms = [_serialize_term(t) for t in raw if _type_name(t) == "GlossaryTerm"]
    terms.sort(key=lambda t: (t.get("displayName") or "").lower())
    return JSONResponse({"terms": terms, "total": len(terms), "collection": collection_guid})


@router.get("/api/glossary-terms", summary="Search all glossary terms across all glossaries")
def search_all_terms(
    q:          str = Query("*",   description="Search string; use * to return all"),
    start_from: int = Query(0,     ge=0),
    page_size:  int = Query(200,   ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """
    Search for GlossaryTerms across all glossaries using a text search string.
    Terms can belong to multiple glossaries; this view is independent of glossary membership.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
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
            graph_query_depth=1,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_glossary_terms failed")
        raise HTTPException(status_code=500, detail=f"Term search failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    seen: set = set()
    unique: list = []
    for t in raw:
        g = _header(t).get("guid", "")
        if g and g not in seen:
            seen.add(g)
            unique.append(t)

    terms = [_serialize_term(t) for t in unique]
    terms.sort(key=lambda t: (t.get("displayName") or "").lower())
    return JSONResponse({"terms": terms, "total": len(terms), "query": search_string})


@router.get("/api/glossary/term/{term_guid}", summary="Get a single term by GUID")
def get_term(
    term_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a single glossary term."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create GlossaryManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_term_by_guid(term_guid, output_format="JSON", body={"class": "GetRequestBody", "graphQueryDepth": 1})
    except Exception as exc:
        logger.exception("get_term_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Term retrieval failed: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Term {term_guid!r} not found")

    return JSONResponse(_serialize_term(raw))
