"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Community Explorer — FastAPI router.

Endpoints:
  GET /api/communities          → list all communities
  GET /api/communities/{guid}   → full detail for a community
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from common_serialize import _authored_fields, _header_summary, _classifications

router = APIRouter(tags=["communities"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import CommunityMatters
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = CommunityMatters(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
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
                "displayName":    rp.get("displayName") or rp.get("fullName") or rp.get("name") or "",
                "qualifiedName":  rp.get("qualifiedName") or "",
                "description":    rp.get("description") or "",
                "typeName":       rtype.get("typeName") or "",
                "superTypeNames": rtype.get("superTypeNames") or [],
            })
    return result


def _serialize_community(element: dict) -> dict:
    """Generic serializer, matching the pattern used for Actors: relationship
    arrays vary (assignedActors, assignmentScope, resourceListUsers,
    relevantToScopes, noteLogs, and — where populated — collectionMembers),
    so any top-level list of RelatedMetadataElementSummary entries is exposed
    generically under d["relationships"][<key>] rather than hard-coded.
    """
    props  = _props(element)
    header = _header(element)
    d = {
        "guid":           header.get("guid", ""),
        "displayName":    props.get("displayName") or props.get("name") or "",
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "mission":        props.get("mission") or "",
        "status":         header.get("status") or "",
        "typeName":       _type_name(element),
        "superTypeNames": _super_type_names(element),
        "_header":        _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
    }
    relationships = {}
    for k, v in element.items():
        if k in ("class", "elementHeader", "properties"):
            continue
        if isinstance(v, str):
            continue
        if isinstance(v, list) and v and isinstance(v[0], dict) and "relatedElement" in v[0]:
            relationships[k] = _serialize_rel_entries(v)
    d["relationships"] = relationships

    mermaid = element.get("mermaidGraph") or ""
    if mermaid and isinstance(mermaid, str) and not mermaid.lower().startswith("no "):
        d["mermaidGraph"] = mermaid
    return d


@router.get("/api/communities", summary="List all communities")
def list_communities(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CommunityMatters manager for community list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_communities(
            search_string="*",
            starts_with=False,
            output_format="JSON",
            graph_query_depth=0,
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        logger.exception("find_communities failed")
        raise HTTPException(status_code=500, detail=f"Community retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if isinstance(e, dict) and not _is_template(e)]

    communities = [_serialize_community(e) for e in raw if isinstance(e, dict)]
    communities.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"communities": communities, "total": len(communities)})


@router.get("/api/communities/{guid}", summary="Get full detail for a community")
def get_community(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CommunityMatters manager for community detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_community_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_community_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Community detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Community {guid!r} not found")

    return JSONResponse(_serialize_community(element))
