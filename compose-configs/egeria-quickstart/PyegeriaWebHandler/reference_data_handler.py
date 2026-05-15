"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Reference Data Explorer — FastAPI router.

Endpoints:
  GET /api/reference-data               → list all valid value definitions (with optional search)
  GET /api/reference-data/{guid}        → full detail for a single valid value definition
  GET /api/reference-data/metadata-values → valid values for a specific property/type name
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["reference-data"])


def _get_manager():
    from pyegeria import ReferenceDataManager
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = ReferenceDataManager(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


# Built-in and known custom Egeria set types
_SET_TYPES = {"ValidValueSet", "ReferenceDataSet"}


def _serialize_vv_def(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    type_info = header.get("type") or {}
    type_name = type_info.get("typeName", "") or ""
    super_types = type_info.get("superTypeNames") or []
    # An element is a "set" if its most-specific type IS ValidValueSet or inherits from it
    is_set = type_name in _SET_TYPES or bool(_SET_TYPES.intersection(set(super_types)))
    return {
        "guid":           header.get("guid", ""),
        "typeName":       type_name,
        "superTypeNames": super_types,
        "isSet":          is_set,
        "displayName":    props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":  props.get("qualifiedName", "") or "",
        "description":    props.get("description", "") or "",
        "preferredValue": props.get("preferredValue", "") or "",
        "category":       props.get("category", "") or "",
        "dataType":       props.get("dataType", "") or "",
        "usage":          props.get("usage", "") or "",
        "scope":          props.get("scope", "") or "",
        "status":         header.get("status", "") or "",
        "isDeprecated":   props.get("isDeprecated", False),
        "isCaseSensitive":props.get("isCaseSensitive", False),
    }


@router.get("/api/reference-data", summary="Search valid value definitions")
def get_valid_value_definitions(
    q:          Optional[str] = Query(None, description="Search string (substring match, case-insensitive). Defaults to all."),
    start_from: int           = Query(0,   ge=0),
    page_size:  int           = Query(200, ge=1, le=1000),
):
    """
    Return valid value definitions from Egeria.

    Searches by display name / description using `find_valid_value_definitions`.
    Returns a flat list suitable for client-side grouping by typeName (ValidValueSet vs ValidValueDefinition).
    """
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create ReferenceDataManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    search_string = q.strip() if q and q.strip() else "*"
    try:
        raw = mgr.find_valid_value_definitions(
            search_string=search_string,
            starts_with=False,
            ignore_case=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_valid_value_definitions failed")
        raise HTTPException(status_code=500, detail=f"Valid value retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    definitions = [_serialize_vv_def(e) for e in raw]
    definitions.sort(key=lambda d: (d.get("typeName", ""), d.get("displayName", "").lower()))

    sets   = [d for d in definitions if d["isSet"]]
    values = [d for d in definitions if not d["isSet"]]

    return JSONResponse({
        "definitions": definitions,
        "sets":        sets,
        "values":      values,
        "total":       len(definitions),
        "start_from":  start_from,
        "page_size":   page_size,
    })


@router.get("/api/reference-data/metadata-values", summary="Valid values for a property/type")
def get_metadata_values(
    property_name: str           = Query(..., description="Property name to look up valid values for"),
    type_name:     Optional[str] = Query(None, description="Optional: restrict to a specific open metadata type"),
):
    """
    Return the valid metadata values registered for a given property name.
    Optionally restricted to a specific open metadata type.
    Does not require Egeria connection (uses local ValidMetadataManager registry).
    """
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create ReferenceDataManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_valid_metadata_values(property_name=property_name, type_name=type_name)
    except Exception as exc:
        logger.exception("get_valid_metadata_values failed")
        raise HTTPException(status_code=500, detail=f"Metadata values retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    return JSONResponse({
        "property_name": property_name,
        "type_name":     type_name,
        "values":        raw,
        "total":         len(raw),
    })


@router.get("/api/reference-data/{vv_guid}", summary="Get a valid value definition by GUID")
def get_valid_value_definition(vv_guid: str):
    """Return full detail for a single valid value definition."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create ReferenceDataManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_valid_value_definition_by_guid(vv_guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_valid_value_definition_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Valid value retrieval failed: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Valid value definition {vv_guid!r} not found")

    return JSONResponse(_serialize_vv_def(raw))
