"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Context Events — FastAPI router.

Backed by the pyegeria TimeKeeper View Service client.

Endpoints:
  GET /api/context-events              → list all context events
  GET /api/context-events/{guid}       → full detail for a context event
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from common_serialize import _authored_fields, _header_summary

router = APIRouter(tags=["context-events"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import TimeKeeper
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = TimeKeeper(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _is_template(element: dict) -> bool:
    for val in (element.get("elementHeader") or {}).values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _super_type_names(element: dict) -> list:
    return (_header(element).get("type") or {}).get("superTypeNames") or []


def _serialize_rel_entries(rel_list: list) -> list:
    result = []
    for rel in rel_list:
        re = rel.get("relatedElement") or {}
        rh = re.get("elementHeader") or {}
        rp = re.get("properties") or {}
        rtype = rh.get("type") or {}
        g = rh.get("guid", "")
        if g:
            result.append({
                "guid":           g,
                "displayName":    rp.get("displayName") or rp.get("name") or "",
                "qualifiedName":  rp.get("qualifiedName") or "",
                "description":    rp.get("description") or "",
                "typeName":       rtype.get("typeName") or "",
                "superTypeNames": rtype.get("superTypeNames") or [],
                "relationshipProperties": {
                    k: v for k, v in (rel.get("relationshipProperties") or {}).items()
                    if k not in ("class",) and v is not None and v != ""
                },
            })
    return result


def _serialize_classifications(header: dict) -> list:
    """Extract classifications from elementHeader into a list of {typeName, properties}."""
    result = []
    for val in header.values():
        if not isinstance(val, dict):
            continue
        cls_class = val.get("class") or ""
        if cls_class != "ElementClassification":
            continue
        type_info = val.get("type") or {}
        type_name = val.get("classificationName") or type_info.get("typeName") or ""
        if not type_name:
            continue
        raw_props = val.get("classificationProperties") or {}
        props = {k: v for k, v in raw_props.items() if k != "class" and v is not None and v != ""}
        result.append({"typeName": type_name, "properties": props})
    return result


_KNOWN_PROPS = frozenset({
    "displayName", "qualifiedName", "description", "eventEffect", "url",
    "plannedStartDate", "actualStartDate", "plannedCompletionDate", "actualCompletionDate",
    "plannedDuration", "actualDuration", "repeatInterval",
    "referenceEffectiveFrom", "referenceEffectiveTo", "class",
})


def _serialize_context_event(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    d = {
        "guid":                    header.get("guid", ""),
        "displayName":             props.get("displayName") or "",
        "qualifiedName":           props.get("qualifiedName") or "",
        "description":             props.get("description") or "",
        "eventEffect":             props.get("eventEffect") or "",
        "url":                     props.get("url") or "",
        "plannedStartDate":        props.get("plannedStartDate") or "",
        "actualStartDate":         props.get("actualStartDate") or "",
        "plannedCompletionDate":   props.get("plannedCompletionDate") or "",
        "actualCompletionDate":    props.get("actualCompletionDate") or "",
        "plannedDuration":         props.get("plannedDuration"),
        "actualDuration":          props.get("actualDuration"),
        "repeatInterval":          props.get("repeatInterval"),
        "referenceEffectiveFrom":  props.get("referenceEffectiveFrom") or "",
        "referenceEffectiveTo":    props.get("referenceEffectiveTo") or "",
        "status":                  header.get("status") or "",
        "typeName":                _type_name(element),
        "superTypeNames":          _super_type_names(element),
        "classifications":         _serialize_classifications(header),
        # Any properties not in the known set (forward-compatible with schema additions)
        "extraProperties": {
            k: v for k, v in props.items()
            if k not in _KNOWN_PROPS and v is not None and v != ""
        },
        "_header":                 _header_summary(element),
        **_authored_fields(element),
    }

    # Collect all relationship arrays generically
    relationships = {}
    for k, v in element.items():
        if k in ("class", "elementHeader", "properties"):
            continue
        if isinstance(v, list) and v and isinstance(v[0], dict) and "relatedElement" in v[0]:
            relationships[k] = _serialize_rel_entries(v)
    d["relationships"] = relationships

    mermaid = element.get("mermaidGraph") or ""
    if mermaid and isinstance(mermaid, str) and not mermaid.lower().startswith("no "):
        d["mermaidGraph"] = mermaid

    return d


@router.get("/api/context-events", summary="List all context events")
def list_context_events(
    q:          str = Query("*",   description="Search string (* = all)"),
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=1000),
    url:        Optional[str] = Query(None),
    server:     Optional[str] = Query(None),
    user_id:    Optional[str] = Query(None),
    user_pwd:   Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, Template-classified elements are excluded"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create TimeKeeper manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        kwargs = {}
        if as_of_time:
            kwargs["as_of_time"] = as_of_time
        raw = mgr.find_context_events(
            search_string=q or "*",
            starts_with=False,
            output_format="JSON",
            graph_query_depth=0,
            start_from=start_from,
            page_size=page_size,
            **kwargs,
        )
    except Exception as exc:
        logger.warning(f"find_context_events failed: {exc}")
        raw = []

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if isinstance(e, dict) and not _is_template(e)]

    events = [_serialize_context_event(e) for e in raw if isinstance(e, dict) and e.get("elementHeader")]
    return JSONResponse({"events": events})


@router.get("/api/context-events/{guid}", summary="Get a context event by GUID")
def get_context_event(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create TimeKeeper manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_context_event_by_guid(
            guid=guid,
            output_format="JSON",
            graph_query_depth=3,
        )
    except Exception as exc:
        logger.warning(f"get_context_event_by_guid({guid}) failed: {exc}")
        raise HTTPException(status_code=404, detail=f"Context event not found: {exc}")

    if not isinstance(raw, dict) or not raw.get("elementHeader"):
        raise HTTPException(status_code=404, detail="Context event not found")

    return JSONResponse(_serialize_context_event(raw))
