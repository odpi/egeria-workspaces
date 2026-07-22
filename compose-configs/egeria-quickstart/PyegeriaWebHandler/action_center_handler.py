"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Action Center — FastAPI router.

Endpoints:
  GET /api/action-center            → list Notification/Meeting/ToDo/Review elements, paginated
  GET /api/action-center/{guid}      → full detail for one action, including any related elements

Notification, Meeting, ToDo, and Review are real first-class entities in
Egeria's model 0135 ("Actions For People") — siblings under the abstract
Action supertype (model 0013), same supertype EngineAction extends.
EngineAction already has dedicated coverage in egeria-operations.html;
Comment/Rating/Like are attachment-only feedback types already covered
per-element via egeria_feedback_handler.py; Task/Campaign are classifications
on Project/Collection, not separate entities — none of those five belong here.

Uses MetadataExpert.find_metadata_elements/get_metadata_element_by_guid (the
raw, non-converter-backed path — same shape insights_handler.py already
solved: elementGUID, flat classifications list, elementProperties.propertyValueMap,
NOT the elementHeader-wrapped shape). AssetMaker.find_processes was considered
(the mechanism tech_catalog_handler.py's generic mixed "Actions" tab uses) but
its default activity_status_list=['IN_PROGRESS'] filter gave wrong/inconsistent
counts for Notification (0, vs the real ~44 confirmed live) — Notification
doesn't have a meaningful "in progress" activity status the way ToDo does, so
the plain type-scoped find_metadata_elements call is simpler and correct here.

get_metadata_element_by_guid does NOT return relationships regardless of
graph_query_depth (confirmed live against real Notification data with known
Actions/ActionRequester/AssignmentScope relationships — all absent from every
depth 0-3). MetadataExpert.get_all_related_elements(guid) is the call that
actually surfaces them ({startingElement, elementList, mermaidGraph} —
elementList entries carry the relationship's own type.typeName plus a nested
`element` for the other end), so detail fetches both and merges them.

Governance-zone/visibility filtering is automatic (server-side, based on the
calling user's token) — no app-level filtering code needed, same as everywhere
else in this codebase.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token
from common_serialize import _classifications_from_metadata_expert

router = APIRouter(tags=["action-center"])

_ACTION_TYPES = ("Notification", "Meeting", "ToDo", "Review")


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _prop_scalar(pv):
    """Unwrap one PropertyValue payload into a plain Python value. Arrays arrive as
    ArrayTypePropertyValue with a nested propertyValueMap keyed "0", "1", ... rather
    than a plain list — reassemble those in order. (Copied from insights_handler.py —
    same raw MetadataExpert shape, small enough to duplicate rather than cross-import,
    matching this codebase's per-handler-private-helper convention.)"""
    if not isinstance(pv, dict):
        return pv
    if pv.get("class") == "ArrayTypePropertyValue":
        arr = (pv.get("arrayValues") or {}).get("propertyValueMap") or {}
        return [_prop_scalar(arr[k]) for k in sorted(arr, key=lambda k: int(k)) if k.isdigit()]
    if "primitiveValue" in pv:
        return pv.get("primitiveValue")
    return pv.get("symbolicName", pv)


def _element_props(element: dict) -> dict:
    pvm = (element.get("elementProperties") or {}).get("propertyValueMap") or {}
    return {k: _prop_scalar(v) for k, v in pvm.items()}


def _relationships_from_related_elements(related: dict) -> dict:
    """mgr.get_all_related_elements(guid) returns {startingElement, elementList,
    mermaidGraph} — elementList is a flat list of relationship-header dicts,
    each with its own `type.typeName` (the relationship type, e.g. ActionTarget/
    ActionRequester/AssignmentScope/Actions) and a nested `element` (the OTHER
    end, same raw elementGUID/elementProperties shape as the action itself).
    get_metadata_element_by_guid never returns these regardless of
    graph_query_depth (confirmed live against real Notification data with known
    relationships) — this is the only call that surfaces them, so it's the
    real source of truth for cross-linking, not the element dict's own keys."""
    out = {}
    for item in (related.get("elementList") or []):
        if not isinstance(item, dict):
            continue
        rel_type = (item.get("type") or {}).get("typeName") or "Related"
        el = item.get("element") or {}
        rp = _element_props(el)
        g = el.get("elementGUID", "")
        if not g:
            continue
        etype = el.get("type") or {}
        out.setdefault(rel_type, []).append({
            "guid":           g,
            "typeName":       etype.get("typeName", ""),
            "superTypeNames": etype.get("superTypeNames") or [],
            "displayName":    rp.get("displayName") or rp.get("name") or rp.get("qualifiedName") or g,
            "qualifiedName":  rp.get("qualifiedName") or "",
        })
    return out


def _serialize_summary(element: dict) -> dict:
    props = _element_props(element)
    return {
        "guid":          element.get("elementGUID", ""),
        "typeName":      (element.get("type") or {}).get("typeName", ""),
        "displayName":   props.get("displayName") or props.get("name") or props.get("qualifiedName") or "",
        "qualifiedName": props.get("qualifiedName") or "",
        "situation":     props.get("situation") or "",
        "status":        element.get("status", ""),
        "createTime":    (element.get("versions") or {}).get("createTime", ""),
    }


def _serialize_detail(element: dict, related: dict) -> dict:
    props = _element_props(element)
    detail = _serialize_summary(element)
    detail["properties"] = props
    detail["relationships"] = _relationships_from_related_elements(related)
    detail["classifications"] = _classifications_from_metadata_expert(element)
    return detail


@router.get("/api/action-center", summary="List Notification/Meeting/ToDo/Review actions, paginated")
def list_actions(
    action_type: Optional[str] = Query(None, description="Notification | Meeting | ToDo | Review; omit for all four"),
    start_from:  int = Query(0,  ge=0),
    page_size:   int = Query(50, ge=1, le=200),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create MetadataExpert manager for action center")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    types = (action_type,) if action_type in _ACTION_TYPES else _ACTION_TYPES

    # This codebase's usual "load-all held in state" pattern doesn't scale here
    # (Notification volume has been observed as high as ~1170 in this same demo
    # environment, though it fluctuates as a background watchdog engine creates
    # them) — real server-side start_from/page_size paging per type instead.
    results = []
    for t in types:
        try:
            body = {"class": "FindRequestBody", "metadataElementTypeName": t, "limitResultsByStatus": ["ACTIVE"]}
            raw = mgr.find_metadata_elements(body, start_from=start_from, page_size=page_size, graph_query_depth=0)
        except Exception as exc:
            logger.exception(f"find_metadata_elements failed for {t}")
            raise HTTPException(status_code=500, detail=f"Action center retrieval failed for {t}: {exc}")
        for el in (raw if isinstance(raw, list) else []):
            if isinstance(el, dict):
                item = _serialize_summary(el)
                item["actionType"] = t
                results.append(item)

    results.sort(key=lambda x: x.get("createTime") or "", reverse=True)
    return JSONResponse({"actions": results, "total": len(results), "startFrom": start_from, "pageSize": page_size})


@router.get("/api/action-center/{guid}", summary="Get full detail for a single action")
def get_action(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create MetadataExpert manager for action detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_metadata_element_by_guid(guid, graph_query_depth=1, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_metadata_element_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Action detail retrieval failed: {exc}")

    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Action {guid!r} not found")

    # get_metadata_element_by_guid never returns relationships regardless of
    # graph_query_depth (confirmed live) — get_all_related_elements is the only
    # call that surfaces them, so it's fetched separately for cross-linking.
    try:
        related = mgr.get_all_related_elements(guid, output_format="JSON")
        if not isinstance(related, dict):
            related = {}
    except Exception:
        logger.exception(f"get_all_related_elements failed for {guid}")
        related = {}

    return JSONResponse(_serialize_detail(element, related))
