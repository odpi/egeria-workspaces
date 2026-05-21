"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Valid Metadata Values Explorer — FastAPI router.

Endpoints:
  GET /api/valid-values/properties  → property names that have registered valid values
  GET /api/valid-values/lookup      → valid values for a specific Egeria property name
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["valid-values"])

_FIND_BODY = {
    "class": "FindRequestBody",
    "metadataElementTypeName": "ValidMetadataValue",
    "searchProperties": {
        "class": "SearchProperties",
        "conditions": [{"property": "preferredValue", "operator": "IS_NULL"}],
        "matchCriteria": "ANY",
    },
}


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ReferenceDataManager
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ReferenceDataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _extract_name_from_element(el) -> str:
    """Extract the property name from a ValidMetadataValue element.

    Raw find_metadata_elements returns elements where the property name is stored
    under the key "identifier" (not "propertyName") in elementProperties.
    """
    if isinstance(el, str):
        return el.strip() if el.strip() else ""

    if not isinstance(el, dict):
        return ""

    # Processed pyegeria format: el["properties"]["propertyName"] or ["identifier"]
    props = el.get("properties")
    if isinstance(props, dict):
        name = props.get("propertyName") or props.get("identifier") or ""
        if name:
            return name

    # Raw OpenMetadata format — propertiesAsStrings is the fastest path
    el_props = el.get("elementProperties")
    if isinstance(el_props, dict):
        props_as_str = el_props.get("propertiesAsStrings") or {}
        name = props_as_str.get("identifier") or ""
        if name:
            return name
        # Fall back to full propertyValueMap
        prop_map = el_props.get("propertyValueMap") or {}
        prop_entry = prop_map.get("identifier") or {}
        if isinstance(prop_entry, dict):
            name = prop_entry.get("primitiveValue") or ""
            if name:
                return name

    return el.get("identifier") or el.get("propertyName") or ""


def _names_from_raw(raw) -> set:
    """Extract unique property names regardless of whether raw is a list or a response dict."""
    names: set[str] = set()

    if isinstance(raw, str):
        # NO_ELEMENTS_FOUND sentinel or unexpected string — nothing to parse
        logger.warning(f"find_metadata_elements returned string: {raw[:200]}")
        return names

    # Some pyegeria versions return the full response dict rather than just the elements list
    if isinstance(raw, dict):
        logger.info(f"find_metadata_elements returned dict with keys: {list(raw.keys())[:10]}")
        # Try "elementsAsStrings" — simple list of property name strings
        for item in (raw.get("elementsAsStrings") or []):
            n = _extract_name_from_element(item)
            if n:
                names.add(n)
        # Also try structured "elements"
        for item in (raw.get("elements") or []):
            n = _extract_name_from_element(item)
            if n:
                names.add(n)
        return names

    if not isinstance(raw, list):
        logger.warning(f"find_metadata_elements returned unexpected type {type(raw).__name__}")
        return names

    for el in raw:
        n = _extract_name_from_element(el)
        if n:
            names.add(n)
    return names


@router.get("/api/valid-values/properties", summary="List property names that have registered valid values")
def get_valid_value_properties(
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    """
    Return the sorted list of property names that have at least one registered valid value.
    Uses find_metadata_elements to query ValidMetadataValue entries where preferredValue IS_NULL
    (these are the header registrations that identify a property as having a controlled vocabulary).
    """
    try:
        mgr = _get_expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create MetadataExpert")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_metadata_elements(_FIND_BODY)
    except Exception as exc:
        logger.exception("find_metadata_elements failed")
        raise HTTPException(status_code=500, detail=f"Property list retrieval failed: {exc}")

    names = _names_from_raw(raw)
    logger.info(f"find_metadata_elements: type={type(raw).__name__} → {len(names)} unique property names: {sorted(names)}")
    return JSONResponse({"properties": sorted(names), "total": len(names)})


@router.get("/api/valid-values/lookup", summary="Look up valid values for an Egeria property name")
def lookup_valid_values(
    property_name: str           = Query(..., description="Egeria property name to look up"),
    type_name:     Optional[str] = Query(None, description="Optional: restrict to a specific Egeria type name"),
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    """
    Return valid metadata values registered for a given Egeria property name.
    Optionally restrict results to a specific open metadata type.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ReferenceDataManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_valid_metadata_values(property_name=property_name, type_name=type_name)
    except Exception as exc:
        logger.exception("get_valid_metadata_values failed")
        raise HTTPException(status_code=500, detail=f"Valid values retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    return JSONResponse({
        "property_name": property_name,
        "type_name":     type_name,
        "values":        raw,
        "total":         len(raw),
    })
