"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Valid Metadata Values Explorer — FastAPI router.

Endpoints:
  GET /api/valid-values/lookup   → valid values registered for a specific Egeria property name
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["valid-values"])


def _get_manager():
    from pyegeria import ReferenceDataManager
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = ReferenceDataManager(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


@router.get("/api/valid-values/lookup", summary="Look up valid values for an Egeria property name")
def lookup_valid_values(
    property_name: str           = Query(..., description="Egeria property name to look up"),
    type_name:     Optional[str] = Query(None, description="Optional: restrict to a specific Egeria type name"),
):
    """
    Return valid metadata values registered for a given Egeria property name.
    Optionally restrict results to a specific open metadata type.
    These represent the allowed values for properties like contentStatus, operationalStatus, etc.
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
        raise HTTPException(status_code=500, detail=f"Valid values retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    return JSONResponse({
        "property_name": property_name,
        "type_name":     type_name,
        "values":        raw,
        "total":         len(raw),
    })
