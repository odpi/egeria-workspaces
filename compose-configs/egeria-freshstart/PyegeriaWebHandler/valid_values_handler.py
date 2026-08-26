"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Valid Metadata Values Explorer — FastAPI router.

Endpoints:
  GET /api/valid-values/properties          → property names that have registered valid values
  GET /api/valid-values/lookup              → valid values for a specific Egeria property name
  GET /api/valid-values/spec-property-types → specification property type names
  GET /api/valid-values/spec-property-lookup → specification property values for a given type
"""

import os
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from digital_products_handler import _serialize_node, _extract_all_rels

router = APIRouter(tags=["valid-values"])

_FIND_BODY = {
    "class": "FindRequestBody",
    "metadataElementTypeName": "ValidMetadataValue",
    "searchProperties": {
        "class": "SearchProperties",
        "conditions": [{"property": "preferredValue", "operator": "IS_NULL"}],
        "matchCriteria": "ANY",
    },
    # PY-6/PY-14 perf lesson — _names_from_raw only reads flat property names,
    # never relationships; same fix already applied to find_specification_property
    # below via graph_query_depth=0.
    "graphQueryDepth": 0,
}


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ReferenceDataManager
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ReferenceDataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _get_spec_props(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import SpecificationProperties
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = SpecificationProperties(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
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
    apply_token(mgr)
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


def _fallback_lookup(property_name: str, url=None, server=None, user_id=None, user_pwd=None) -> list:
    """
    Fall back to find_metadata_elements when the primary REST lookup returns nothing.
    This handles properties whose valid values are registered against specific Egeria
    types (e.g. annotationType → ResourceProfileAnnotation) rather than globally.
    Returns a list of flat dicts matching the format the REST API normally produces.
    """
    expert = _get_expert(url, server, user_id, user_pwd)
    find_body = {
        "class": "FindRequestBody",
        "metadataElementTypeName": "ValidMetadataValue",
        "searchProperties": {
            "class": "SearchProperties",
            "conditions": [
                {
                    "property": "identifier",
                    "operator": "EQ",
                    "value": {
                        "class": "PrimitiveTypePropertyValue",
                        "typeName": "string",
                        "primitiveValue": property_name,
                    },
                }
            ],
            "matchCriteria": "ALL",
        },
        # PY-6/PY-14 perf lesson — the loop below only reads flat propertiesAsStrings fields.
        "graphQueryDepth": 0,
    }
    try:
        raw = expert.find_metadata_elements(find_body)
    except Exception as exc:
        logger.warning(f"fallback find_metadata_elements failed for {property_name}: {exc}")
        return []

    if not isinstance(raw, list):
        return []

    results = []
    for el in raw:
        props = (el.get("elementProperties") or {}).get("propertiesAsStrings") or {}
        preferred = props.get("preferredValue", "")
        if not preferred:
            # Skip set-header entries (preferredValue absent = the containing set record)
            continue
        try:
            ordinal = int(props.get("ordinal", 9999))
        except (TypeError, ValueError):
            ordinal = 9999
        is_case = props.get("isCaseSensitive", "false").lower() == "true"
        results.append({
            "displayName":     props.get("displayName") or preferred,
            "preferredValue":  preferred,
            "description":     props.get("description", ""),
            "category":        props.get("category", ""),
            "dataType":        props.get("dataType", ""),
            "usage":           props.get("usage", ""),
            "scope":           props.get("scope", ""),
            "qualifiedName":   props.get("qualifiedName", ""),
            "isCaseSensitive": is_case,
            "ordinal":         ordinal,
            "propertyName":    property_name,
            "guid":            el.get("elementGUID", ""),
        })
    logger.info(f"fallback lookup for {property_name!r}: {len(results)} values via find_metadata_elements")
    return results


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
    When the primary REST lookup returns nothing and no type_name was specified,
    falls back to find_metadata_elements to catch type-scoped valid value sets.
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

    # No type was scoped — merge in find_metadata_elements results to pick up values
    # registered against specific Egeria types (e.g. annotationType), in addition to
    # whatever the primary REST lookup already found globally. Egeria's primary
    # get-valid-metadata-values REST endpoint never returns a guid/qualifiedName/scope/
    # usage — those only come back via find_metadata_elements — so beyond picking up
    # subtype-only values, this merge also backfills those fields onto matching primary
    # entries (matched by preferredValue) so the 3rd-column detail pane (which fetches
    # by guid) has something to select for every value, not just fallback-only ones.
    if not type_name:
        fallback = _fallback_lookup(property_name, url, server, user_id, user_pwd)
        fallback_by_value = {v.get("preferredValue"): v for v in fallback}
        for v in raw:
            match = fallback_by_value.get(v.get("preferredValue"))
            if match:
                for key in ("guid", "qualifiedName", "scope", "usage"):
                    if not v.get(key) and match.get(key):
                        v[key] = match[key]
        seen = {v.get("preferredValue") for v in raw}
        raw = raw + [v for v in fallback if v.get("preferredValue") not in seen]

    return JSONResponse({
        "property_name": property_name,
        "type_name":     type_name,
        "values":        raw,
        "total":         len(raw),
    })


@router.get("/api/valid-values/spec-property-types", summary="List specification property type names")
def get_specification_property_types(
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    """
    Return the sorted list of specification property type names (e.g. TemplateSubstitute,
    ReplacementProperty) that can be used to look up specification property values.
    """
    try:
        mgr = _get_spec_props(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SpecificationProperties client")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_specification_property_types()
    except Exception as exc:
        logger.exception("get_specification_property_types failed")
        raise HTTPException(status_code=500, detail=f"Specification property type retrieval failed: {exc}")

    names = sorted(raw.keys()) if isinstance(raw, dict) else []
    return JSONResponse({"types": names, "total": len(names)})


def _flatten_spec_property_element(el: dict) -> dict:
    """Flatten a raw OpenMetadataRootElement into the flat shape ValidValueEntry expects."""
    props = el.get("properties") or {}
    return {
        "displayName":     props.get("displayName") or props.get("preferredValue") or "",
        "preferredValue":  props.get("preferredValue", ""),
        "description":     props.get("description", ""),
        "category":        props.get("category", ""),
        "dataType":        props.get("dataType", ""),
        "usage":           props.get("usage", ""),
        "qualifiedName":   props.get("qualifiedName", ""),
        "isCaseSensitive": bool(props.get("isCaseSensitive", False)),
        "ordinal":         props.get("ordinal", 9999),
        "specPropertyType": props.get("identifier", ""),
        "guid":            (el.get("elementHeader") or {}).get("guid", ""),
    }


@router.get("/api/valid-values/spec-property-lookup", summary="Look up specification property values for a type")
def lookup_specification_property_values(
    spec_property_type: str           = Query(..., description="Specification property type to look up (PascalCase, e.g. PlaceholderProperty)"),
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    """
    Return specification property values registered for a given specification property type.

    NOTE: the dedicated "by-type" REST operation (get_specification_property_by_type)
    rejects every value tried for its specificationPropertyType enum parameter with a
    generic 400 from the view server (looks like an upstream Egeria/pyegeria mismatch).
    As a workaround, fetch the full specification property catalog via the working
    by-search-string operation (find_specification_property) and filter client-side on
    the "identifier" property, which holds the camelCase form of the type name
    (e.g. "PlaceholderProperty" -> "placeholderProperty").

    graph_query_depth=0 is required: the default (3) makes the view server compute a
    relationship graph/mermaid diagram per element, which takes ~50s for 1000 elements
    vs <1s with depth=0 (same O(n) cost pattern as the Note Logs graph_query_depth issue).
    """
    try:
        mgr = _get_spec_props(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SpecificationProperties client")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        elements = mgr.find_specification_property("*", page_size=1000, graph_query_depth=0)
    except Exception as exc:
        logger.exception("find_specification_property failed")
        raise HTTPException(status_code=500, detail=f"Specification property retrieval failed: {exc}")

    if not isinstance(elements, list):
        elements = []

    identifier = spec_property_type[:1].lower() + spec_property_type[1:] if spec_property_type else ""
    raw = [
        _flatten_spec_property_element(el)
        for el in elements
        if isinstance(el, dict) and (el.get("properties") or {}).get("identifier") == identifier
    ]

    return JSONResponse({
        "spec_property_type": spec_property_type,
        "values":             raw,
        "total":              len(raw),
    })


# Lightweight display-name lookup for an arbitrary element guid — used by the
# frontend to label folded spec-property/valid-value groups (e.g. the same
# "versionIdentifier" or "Capture File Counts" spec property registered once per
# owning GovernanceActionProcess/Type, distinguished only by an embedded owner
# guid in qualifiedName). graph_query_depth=0 keeps this cheap even though the
# UI may fire several of these in parallel when a group is expanded — unlike
# get_valid_value_detail below, callers here don't need relationships, just a
# name, so there's no reason to pay the depth=2 cost. Two path segments (vs.
# {guid}'s one) means this can't collide with the catch-all route regardless
# of declaration order, but it's still placed first for readability.
@router.get("/api/valid-values/resolve-name/{guid}", summary="Cheap display-name lookup for an arbitrary element guid (group-label resolution)")
def resolve_element_name(
    guid: str,
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    from pyegeria import ClassificationExplorer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    try:
        ce = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        apply_token(ce)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = ce.get_element_by_guid(
            guid=guid, output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 0},
        )
    except Exception as exc:
        logger.info("resolve_element_name: %s not found/resolvable: %s", guid, exc)
        raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")

    node = _serialize_node(raw)
    return JSONResponse({
        "guid": guid,
        "displayName": node.get("displayName") or node.get("qualifiedName"),
        "typeName": node.get("typeName"),
    })


# Must be registered after the literal routes above (properties, lookup,
# spec-property-types, spec-property-lookup) — FastAPI/Starlette matches
# routes in declaration order, and a bare {guid} declared first would swallow
# them as if they were a guid (same class of bug already hit and fixed in
# collections_handler.py's by-type route — see its comment there).
@router.get("/api/valid-values/{guid}", summary="Full detail for one valid value or specification property value (relationships, classifications)")
def get_valid_value_detail(
    guid: str,
    url:     Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:  Optional[str] = Query(None, description="View server name (overrides env)"),
    user_id: Optional[str] = Query(None, description="User ID (overrides env)"),
    user_pwd:Optional[str] = Query(None, description="Password (overrides env)"),
):
    """The list endpoints above (lookup / spec-property-lookup) intentionally return flat
    summaries only, no relationships or classifications — fetching those per-item across a
    whole list would be the same O(n) graph_query_depth cost this codebase has already hit
    and fixed twice (Note Logs, digital products). This is the per-item detail fetch for
    the master-detail 3rd column instead: ClassificationExplorer.get_element_by_guid is the
    general-purpose "any element type" fetch already used the same way as a fallback in
    digital_products_handler.py's get_node — ValidMetadataValue/SpecificationPropertyValue
    elements aren't Collections or Assets, so that's the right tool here directly, not a
    fallback. graph_query_depth=2 (not 0) is intentional: this is a single-element detail
    fetch, not a list — the cost that matters elsewhere doesn't apply to one guid."""
    from pyegeria import ClassificationExplorer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    try:
        ce = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        apply_token(ce)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        # NOTE (see digital_products_handler.py's get_node for the same gotcha): when body
        # is an explicit dict, pyegeria validates it as-is and ignores graph_query_depth/
        # max_mermaid_node_count kwargs entirely — they must be set directly in the body.
        raw = ce.get_element_by_guid(
            guid=guid, output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 2, "maxMermaidNodeCount": 250},
        )
    except Exception as exc:
        logger.exception("ClassificationExplorer.get_element_by_guid failed for %s", guid)
        raise HTTPException(status_code=404, detail=f"Value {guid!r} not found: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Value {guid!r} not found")

    node = _serialize_node(raw)
    node["relationships"] = _extract_all_rels(raw)
    return JSONResponse(node)
