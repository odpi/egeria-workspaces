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
from egeria_auth import apply_token
from typing import Optional

from common_serialize import _authored_fields, _header_summary

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["glossary"])


def _is_auth_error(exc: Exception) -> bool:
    seen = set()
    node = exc
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        code = getattr(node, "response_code", None) or getattr(node, "http_status_code", None)
        if code in (401, 403):
            return True
        # httpx.HTTPStatusError stores status_code on response
        resp = getattr(node, "response", None)
        if resp is not None and getattr(resp, "status_code", None) in (401, 403):
            return True
        s = str(node).upper()
        if ("HTTP CODE: 401" in s or "HTTP CODE: 403" in s
                or "USER_NOT_AUTHORIZED" in s or "NOT_AUTHORIZED" in s
                or "AUTHORIZATION_ERROR" in s or "401 " in s
                or "CLIENT ERROR '401" in s or "CLIENT ERROR '403" in s):
            return True
        node = getattr(node, "__cause__", None) or getattr(node, "__context__", None)
    return False


def _raise_http(exc: Exception, log_msg: str = "") -> None:
    if log_msg:
        logger.exception(log_msg)
    if _is_auth_error(exc):
        raise HTTPException(status_code=401,
                            detail="Session expired or token invalid — please reconnect.")
    raise HTTPException(status_code=500, detail=str(exc))


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import GlossaryManager
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = GlossaryManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _super_type_names(element: dict) -> list:
    return (_header(element).get("type") or {}).get("superTypeNames", []) or []


# NOTE: term-to-term semantic relationships (Synonym, Antonym, RelatedTerm,
# PreferredTerm, ReplacementTerm, ISARelationship) do NOT get separate top-level
# keys the way this used to assume — empirically confirmed (2026-07-15, live
# against qs-view-server) that get_term_by_guid(output_format="JSON") puts ALL
# of them into a single "relatedTerms" list, distinguishable only by each
# entry's relationshipHeader.type.typeName (and, for the asymmetric
# ISARelationship, the relatedElementAtEnd1 boolean). See _group_related_terms()
# below, which replaces the old per-key assumption. "categories" (term-to-category
# membership) is a different mechanism and does still arrive as its own key.
_TERM_REL_KEYS = [
    ("categories", "Categories"),
]

_TERM_REL_KEY_NAMES = {k for k, _ in _TERM_REL_KEYS}
_TERM_STRUCT_KEYS   = {"elementHeader", "properties", "mermaidGraph", "sourcedFromTemplate", "relatedTerms"}

_TERM_RELATIONSHIP_LABELS = {
    "Synonym":         "Synonyms",
    "Antonym":         "Antonyms",
    "RelatedTerm":     "Related Terms",
    "PreferredTerm":   "Preferred Terms",
    "ReplacementTerm": "Replaced By",
}


def _group_related_terms(raw_list: list) -> dict:
    """Group a raw 'relatedTerms' list by each entry's actual relationship type
    (relationshipHeader.type.typeName) rather than by top-level dict key — see the
    NOTE above _TERM_REL_KEYS. ISARelationship is asymmetric: relatedElementAtEnd1
    distinguishes 'Is A' (this term is the narrower/more specific one, so its
    related element is the broader concept) from 'Classifies' (this term is the
    broader one). Confirmed live: when the fetched term is end1 of the
    relationship, relatedElementAtEnd1 is False and the label is 'Is A'; when the
    fetched term is end2, relatedElementAtEnd1 is True and the label is
    'Classifies'."""
    groups: dict = {}
    for rel in (raw_list or []):
        type_name = ((rel.get("relationshipHeader") or {}).get("type") or {}).get("typeName", "")
        if type_name == "ISARelationship":
            label = "Classifies" if rel.get("relatedElementAtEnd1") else "Is A"
        else:
            label = _TERM_RELATIONSHIP_LABELS.get(type_name, type_name or "Related Terms")
        item = _related_elements([rel])
        if item:
            groups.setdefault(label, []).extend(item)
    return groups


def _is_template(element: dict) -> bool:
    for val in (element.get("elementHeader") or {}).values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


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
                "superTypeNames": (rh.get("type") or {}).get("superTypeNames") or [],
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
        "_header":         _header_summary(element),
        **_authored_fields(element),
    }


def _serialize_folder(element: dict) -> dict:
    """Serialise a CollectionFolder element returned by get_collection_members."""
    props  = _props(element)
    header = _header(element)
    return {
        "guid":            header.get("guid", ""),
        "typeName":        _type_name(element),
        "superTypeNames":  _super_type_names(element),
        "displayName":     props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":   props.get("qualifiedName", "") or "",
        "description":     props.get("description", "") or "",
        "status":          header.get("status", "") or "",
        "classifications": _extract_classifications(header),
        "_header":         _header_summary(element),
        **_authored_fields(element),
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
        "activityStatus":         props.get("activityStatus", "") or "",
        "mermaidGraph":           term.get("mermaidGraph", "") or props.get("mermaidGraph", "") or "",
        "folders":                _folder_memberships(term),
        "isTemplateSubstitute":   is_template_substitute,
        "isSourcedFromTemplate":  is_sourced_from_template,
        "classifications":        _extract_classifications(header),
        "_header":                _header_summary(term),
        **_authored_fields(term),
        "relationships":          {
                                      **{label: items for key, label in _TERM_REL_KEYS
                                         if (items := _related_elements(term.get(key)))},
                                      **_group_related_terms(term.get("relatedTerms")),
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
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """Return all Egeria glossaries with summary information."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        _raise_http(exc, "Failed to create GlossaryManager")

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
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        _raise_http(exc, "find_glossaries failed")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

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
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """Return the CollectionFolder children of a glossary (organisational hierarchy)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        _raise_http(exc, "Failed to create GlossaryManager")

    try:
        body = {"class": "ResultsRequestBody"}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            body=body,
        )
    except Exception as exc:
        _raise_http(exc, "get_collection_members failed")

    if not isinstance(raw, list):
        raw = []

    folders = [_serialize_folder(f) for f in raw if "Folder" in _type_name(f)]
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
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """
    Return GlossaryTerms that are members of the given collection (glossary or folder).

    Uses get_collection_members which fetches only the members of this specific collection,
    then filters for GlossaryTerm type elements. Much faster than a full-table scan.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        _raise_http(exc, "Failed to create GlossaryManager")

    try:
        body = {"class": "ResultsRequestBody"}  # no metadataElementTypeName filter so GlossaryTerms are returned
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            body=body,
        )
    except Exception as exc:
        _raise_http(exc, "get_collection_members failed")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

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
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """
    Search for GlossaryTerms across all glossaries using a text search string.
    Terms can belong to multiple glossaries; this view is independent of glossary membership.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        _raise_http(exc, "Failed to create GlossaryManager")

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
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        _raise_http(exc, "find_glossary_terms failed")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

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
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """Return full detail for a single glossary term."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        _raise_http(exc, "Failed to create GlossaryManager")

    try:
        body = {"class": "GetRequestBody", "graphQueryDepth": 1}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = mgr.get_term_by_guid(term_guid, output_format="JSON", body=body)
    except Exception as exc:
        _raise_http(exc, "get_term_by_guid failed")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Term {term_guid!r} not found")

    return JSONResponse(_serialize_term(raw))
