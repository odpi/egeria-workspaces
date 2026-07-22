"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Business Capability Explorer — FastAPI router.

Endpoints:
  GET /api/business-capabilities          → list all business capabilities
  GET /api/business-capabilities/{guid}   → full detail for a business capability

Modeled on community_handler.py (flat list + detail, no sub-nav — Business
Capability has no hierarchy comparable to Solution Architect's
blueprints→components). Relationships are extracted via
common_serialize._generic_relationships rather than a hand-picked key list:
today's qs demo data has 9 real BusinessCapability entities (Coco
Pharmaceuticals content pack) with memberOfCollections/collectionMembers/
assignedActors relationships, but zero BusinessCapabilityDependency links.
Confirmed live (seeded test data, then cleaned up) that
_generic_relationships picks up BusinessCapabilityDependency automatically
under its real raw key, "dependsOnBusinessCapabilities" — see
egeria-python/tests/functional-tests/test_digital_business_omvs.py::test_business_capability_dependency_relationship_key.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token
from common_serialize import _authored_fields, _header_summary, _generic_relationships, _classifications

router = APIRouter(tags=["business-capabilities"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import DigitalBusiness
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = DigitalBusiness(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
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


def _serialize_business_capability_summary(element: dict) -> dict:
    props, header = _props(element), _header(element)
    return {
        "guid":                       header.get("guid", ""),
        "typeName":                   _type_name(element),
        "superTypeNames":             _super_type_names(element),
        "displayName":                props.get("displayName") or props.get("name") or "",
        "qualifiedName":              props.get("qualifiedName") or "",
        "description":                props.get("description") or "",
        "businessCapabilityType":     props.get("businessCapabilityType") or "",
        "businessImplementationType": props.get("businessImplementationType") or "",
        "status":                     header.get("status") or "",
        "_header":                    _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
    }


def _serialize_business_capability_detail(element: dict) -> dict:
    detail = _serialize_business_capability_summary(element)
    # No curated relationship keys to skip — memberOfCollections/collectionMembers/
    # assignedActors (and, once seeded, any BusinessCapabilityDependency-shaped key)
    # all surface generically.
    detail["relationships"] = _generic_relationships(element)
    return detail


@router.get("/api/business-capabilities", summary="List all business capabilities")
def list_business_capabilities(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=500),
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
        logger.exception("Failed to create DigitalBusiness manager for business capability list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_business_capabilities(
            search_string="*",
            starts_with=False,
            output_format="JSON",
            graph_query_depth=0,  # PY-6/PY-14 perf lesson — bulk listing stays cheap
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        logger.exception("find_business_capabilities failed")
        raise HTTPException(status_code=500, detail=f"Business capability retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if isinstance(e, dict) and not _is_template(e)]

    capabilities = [_serialize_business_capability_summary(e) for e in raw if isinstance(e, dict)]
    capabilities.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"businessCapabilities": capabilities, "total": len(capabilities)})


@router.get("/api/business-capabilities/{guid}", summary="Get full detail for a business capability")
def get_business_capability(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create DigitalBusiness manager for business capability detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_business_capability_by_guid(guid, output_format="JSON", graph_query_depth=2)
    except Exception as exc:
        logger.exception(f"get_business_capability_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Business capability detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Business capability {guid!r} not found")

    return JSONResponse(_serialize_business_capability_detail(element))
