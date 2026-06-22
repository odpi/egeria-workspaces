"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Location Explorer — FastAPI router.

Endpoints:
  GET /api/locations       → list all locations
  GET /api/locations/{guid} → full detail for a location
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["locations"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import LocationArena
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = LocationArena(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _rel_list(element: dict, key: str) -> list:
    return element.get(key) or []


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
            })
    return result


def _location_kinds(element: dict) -> list:
    """Flatten elementHeader.locationKinds classifications into {kind, properties}."""
    kinds = _header(element).get("locationKinds") or []
    out = []
    for k in kinds:
        name = k.get("classificationName") or ""
        cp = k.get("classificationProperties") or {}
        props = {kk: vv for kk, vv in cp.items() if kk not in ("class", "typeName")}
        out.append({"kind": name.replace("Location", "") or name, "properties": props})
    return out


def _serialize_location(element: dict) -> dict:
    """Full serializer — used for both list and detail; includes relationships and mermaid graph."""
    props  = _props(element)
    header = _header(element)
    d = {
        "guid":              header.get("guid", ""),
        "displayName":       props.get("displayName") or props.get("name") or "",
        "qualifiedName":     props.get("qualifiedName") or "",
        "identifier":        props.get("identifier") or "",
        "description":       props.get("description") or "",
        "status":            header.get("status") or "",
        "typeName":          _type_name(element),
        "locationKinds":     _location_kinds(element),
        "parentLocations":   _serialize_rel_entries(_rel_list(element, "groupingLocations")),
        "childLocations":    _serialize_rel_entries(_rel_list(element, "nestedLocations")),
        "peerLocations":     _serialize_rel_entries(_rel_list(element, "peerLocations")),
        "localResources":    _serialize_rel_entries(_rel_list(element, "localResources")),
        "assignedActors":    _serialize_rel_entries(_rel_list(element, "assignedActors")),
        "referenceValues":   _serialize_rel_entries(_rel_list(element, "referenceValues")),
    }
    mermaid = element.get("mermaidGraph") or ""
    if mermaid and isinstance(mermaid, str) and not mermaid.lower().startswith("no "):
        d["mermaidGraph"] = mermaid
    return d


@router.get("/api/locations", summary="List all locations")
def list_locations(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create LocationArena manager for location list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_locations(
            search_string="*",
            starts_with=False,
            output_format="JSON",
            graph_query_depth=1,
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        logger.exception("find_locations failed")
        raise HTTPException(status_code=500, detail=f"Location retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    locations = [_serialize_location(e) for e in raw if isinstance(e, dict)]
    locations.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"locations": locations, "total": len(locations)})


@router.get("/api/locations/{guid}", summary="Get full detail for a location")
def get_location(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create LocationArena manager for location detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_location_by_guid(guid, output_format="JSON", graph_query_depth=1)
    except Exception as exc:
        logger.exception(f"get_location_by_guid failed for location {guid}")
        raise HTTPException(status_code=500, detail=f"Location detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Location {guid!r} not found")

    return JSONResponse(_serialize_location(element))
