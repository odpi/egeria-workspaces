"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Policy Enforcement Architecture Explorer — FastAPI router.

Endpoints:
  GET /api/policy-enforcement   → elements classified with any Policy*Point classification, grouped

The six Policy*Point types (PolicyManagementPoint, PolicyAdministrationPoint,
PolicyDecisionPoint, PolicyEnforcementPoint, PolicyInformationPoint,
PolicyRetrievalPoint) are classifications on Referenceable (a hierarchy with
PolicyManagementPoint as parent, the other five as XACML-style subclasses),
not entities — any element (commonly a GovernanceEngine/GovernanceService)
can carry one. PolicyManagementPointProperties (and the five subclasses that
inherit it) do carry label/description/pointType fields, surfaced here when
present.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token
from common_serialize import _authored_fields, _header_summary, _classifications

router = APIRouter(tags=["policy-enforcement"])

_CLASSIFICATIONS = (
    "PolicyManagementPoint",
    "PolicyAdministrationPoint",
    "PolicyDecisionPoint",
    "PolicyEnforcementPoint",
    "PolicyInformationPoint",
    "PolicyRetrievalPoint",
)


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _classification_properties(element: dict, classification: str) -> dict:
    for c in (_header(element).get("otherClassifications") or []):
        if isinstance(c, dict) and c.get("classificationName") == classification:
            props = c.get("classificationProperties") or {}
            return {k: v for k, v in props.items() if k not in ("class", "typeName")}
    return {}


def _serialize_point(element: dict, classification: str) -> dict:
    props, header = _props(element), _header(element)
    return {
        "guid":                  header.get("guid", ""),
        "typeName":              _type_name(element),
        "displayName":           props.get("displayName") or props.get("name") or props.get("qualifiedName") or "",
        "qualifiedName":         props.get("qualifiedName") or "",
        "classification":        classification,
        "classificationDetail":  _classification_properties(element, classification),
        "_header":               _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
    }


@router.get("/api/policy-enforcement", summary="Elements classified with a Policy*Point classification, grouped")
def get_policy_enforcement(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer manager for policy enforcement")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    groups: dict = {}
    for classification in _CLASSIFICATIONS:
        try:
            raw = mgr.get_elements_by_classification(classification, page_size=200, output_format="JSON", graph_query_depth=0)
        except Exception as exc:
            logger.exception(f"get_elements_by_classification failed for {classification}")
            raise HTTPException(status_code=500, detail=f"Policy enforcement retrieval failed for {classification}: {exc}")
        items = [_serialize_point(e, classification) for e in (raw if isinstance(raw, list) else []) if isinstance(e, dict)]
        items.sort(key=lambda x: (x.get("displayName") or "").lower())
        groups[classification] = items

    total = sum(len(v) for v in groups.values())
    return JSONResponse({"groups": groups, "total": total})
