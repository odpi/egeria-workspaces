"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Actor Explorer — FastAPI router.

Covers the three Actor-domain entity kinds via pyegeria's ActorManager:
  - ActorProfile (Person, Team, Organization, ITProfile)
  - ActorRole    (PersonRole, GovernanceRole, SolutionActorRole, ...)
  - UserIdentity

Endpoints:
  GET /api/actors/profiles            → list all actor profiles
  GET /api/actors/profiles/{guid}     → full detail for an actor profile
  GET /api/actors/roles               → list all actor roles
  GET /api/actors/roles/{guid}        → full detail for an actor role
  GET /api/actors/identities          → list all user identities
  GET /api/actors/identities/{guid}   → full detail for a user identity
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["actors"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ActorManager
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ActorManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


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
            entry = {
                "guid":           g,
                "displayName":    rp.get("displayName") or rp.get("fullName") or rp.get("name") or "",
                "qualifiedName":  rp.get("qualifiedName") or "",
                "description":    rp.get("description") or "",
                "typeName":       rtype.get("typeName") or "",
                "superTypeNames": rtype.get("superTypeNames") or [],
            }
            # Surface a few useful simple properties on the related element itself —
            # e.g. ContactDetails.contactMethodValue, which is the actually useful
            # part of a "Work Email Address" relationship entry.
            for key in _EXTRA_PROPERTY_KEYS:
                val = rp.get(key)
                if val not in (None, "", []):
                    entry[key] = val
            result.append(entry)
    return result


# Simple type-specific properties worth surfacing — both on the main element's
# detail table, and on related elements within relationship sections (e.g.
# ContactDetails.contactMethodValue).
_EXTRA_PROPERTY_KEYS = (
    "jobTitle", "employeeNumber", "employeeType", "identifier", "actorRoleGroups",
    "headCount", "headCountLimitSet", "domainIdentifier", "contactType",
    "contactMethodType", "contactMethodValue", "userId", "distinguishedName",
)


def _serialize_actor_element(element: dict) -> dict:
    """Generic serializer for ActorProfile / ActorRole / UserIdentity elements.

    Relationship arrays vary by concrete type (performsRoles, contactDetails,
    assignmentScope, rolePerformers, governedBy, userIdentities, subTeams, ...),
    so rather than hard-coding each one, any top-level list whose entries look
    like RelatedMetadataElementSummary objects is treated as a relationship
    section and exposed under d["relationships"][<key>].
    """
    props  = _props(element)
    header = _header(element)
    d = {
        "guid":           header.get("guid", ""),
        "displayName":    props.get("displayName") or props.get("fullName") or props.get("name") or props.get("identifier") or "",
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "status":         header.get("status") or "",
        "typeName":       _type_name(element),
        "superTypeNames": _super_type_names(element),
    }
    for key in _EXTRA_PROPERTY_KEYS:
        val = props.get(key)
        if val not in (None, "", []):
            d[key] = val

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


def _list_route(mgr, find_fn, url, server, user_id, user_pwd, start_from, page_size, label):
    try:
        raw = find_fn(
            search_string="*",
            starts_with=False,
            output_format="JSON",
            graph_query_depth=0,
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception(f"{label} list failed")
        raise HTTPException(status_code=500, detail=f"{label} retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []
    items = [_serialize_actor_element(e) for e in raw if isinstance(e, dict)]
    items.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return items


@router.get("/api/actors/profiles", summary="List all actor profiles")
def list_actor_profiles(
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
        logger.exception("Failed to create ActorManager for profile list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    items = _list_route(mgr, mgr.find_actor_profiles, url, server, user_id, user_pwd, start_from, page_size, "Actor profile")
    return JSONResponse({"profiles": items, "total": len(items)})


@router.get("/api/actors/profiles/{guid}", summary="Get full detail for an actor profile")
def get_actor_profile(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ActorManager for profile detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        element = mgr.get_actor_profile_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_actor_profile_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Actor profile retrieval failed: {exc}")
    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Actor profile {guid!r} not found")
    return JSONResponse(_serialize_actor_element(element))


@router.get("/api/actors/roles", summary="List all actor roles")
def list_actor_roles(
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
        logger.exception("Failed to create ActorManager for role list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    items = _list_route(mgr, mgr.find_actor_roles, url, server, user_id, user_pwd, start_from, page_size, "Actor role")
    return JSONResponse({"roles": items, "total": len(items)})


@router.get("/api/actors/roles/{guid}", summary="Get full detail for an actor role")
def get_actor_role(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ActorManager for role detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        element = mgr.get_actor_role_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_actor_role_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Actor role retrieval failed: {exc}")
    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Actor role {guid!r} not found")
    return JSONResponse(_serialize_actor_element(element))


@router.get("/api/actors/identities", summary="List all user identities")
def list_user_identities(
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
        logger.exception("Failed to create ActorManager for identity list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    items = _list_route(mgr, mgr.find_user_identities, url, server, user_id, user_pwd, start_from, page_size, "User identity")
    return JSONResponse({"identities": items, "total": len(items)})


@router.get("/api/actors/identities/{guid}", summary="Get full detail for a user identity")
def get_user_identity(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ActorManager for identity detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        element = mgr.get_user_identity_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_user_identity_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"User identity retrieval failed: {exc}")
    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"User identity {guid!r} not found")
    return JSONResponse(_serialize_actor_element(element))
