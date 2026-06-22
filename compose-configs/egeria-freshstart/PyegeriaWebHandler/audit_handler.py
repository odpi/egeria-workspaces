# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Audit — FastAPI router.

Serves the egeria-audit SPA and the audit API. Four tabs:
  - Exceptions / Certifications / Licenses : governance relationships
    (ClassificationExplorer.get_relationships), point-in-time via asOfTime.
  - Users : platform user accounts (RuntimeManager + SecurityOfficer).

Spec: audit_plan.md (review comments inline there).

Routes:
  GET  /egeria-audit                          → serve the SPA
  GET  /api/audit/relationships?type=…        → governance relationship rows
  GET  /api/audit/element/{guid}              → full element properties (depth 0)
  GET  /api/audit/actor                       → resolve a steward/certifiedBy/… actor
  GET  /api/audit/platforms                   → OMAG Server Platforms (Users tab)
  GET  /api/audit/users?platform_guid=…       → user accounts on a platform
  POST /api/audit/users/status                → change a user's account status (admin-gated)
"""
import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from egeria_auth import apply_token

router = APIRouter(tags=["egeria-audit"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-audit.html"

_AUDIT_REL_TYPES = {"Exception", "Certification", "License"}


# ── client factory ────────────────────────────────────────────────────────────

def _classifier(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


# ── serialisation ─────────────────────────────────────────────────────────────

def _end_stub(stub: dict) -> dict:
    """Normalise an end1/end2 relationship stub to {guid, typeName, uniqueName}.

    The stub carries element header info (for type + guid) and an optional
    uniqueName (typically the element's qualifiedName). Handle both flat and
    elementHeader-nested shapes defensively.
    """
    stub = stub or {}
    hdr = stub.get("elementHeader") or stub
    typ = (hdr.get("type") or stub.get("type") or {})
    return {
        "guid":       hdr.get("guid") or stub.get("guid") or "",
        "typeName":   typ.get("typeName") or "",
        "uniqueName": stub.get("uniqueName") or "",
    }


def _serialize_relationship(rel: dict) -> dict:
    """Map one MetadataRelationshipSummary to a flat row for the audit table.

    Common columns come from the header/ends; tab-specific columns are read from
    `props` (relationshipProperties) by the frontend.
    """
    header = rel.get("relationshipHeader") or {}
    versions = header.get("versions") or {}
    props = dict(rel.get("relationshipProperties") or {})
    props.pop("class", None)
    create_time = versions.get("createTime") or ""
    return {
        "relationshipGuid": header.get("guid") or "",
        "createTime":       create_time,
        "createdBy":        versions.get("createdBy") or "",
        # updateTime may be null → fall back to createTime (per spec)
        "updateTime":       versions.get("updateTime") or create_time,
        "end1":             _end_stub(rel.get("end1") or {}),
        "end2":             _end_stub(rel.get("end2") or {}),
        "props":            props,
    }


def _rel_list(raw) -> list:
    """get_relationships returns a list of dicts OR the string 'No relationships
    found' (and similar) when empty — always normalise to a list of dicts."""
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    return []


# ── SPA ───────────────────────────────────────────────────────────────────────

@router.get("/egeria-audit", include_in_schema=False)
def serve_audit():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Audit page not found")
    return FileResponse(_HTML, media_type="text/html")


# ── Relationship tabs (Exceptions / Certifications / Licenses) ─────────────────

@router.get("/api/audit/relationships", summary="Governance relationship rows for an audit tab")
def list_relationships(
    type:       str = Query(..., description="Exception | Certification | License"),
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(500, ge=1, le=2000),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    if type not in _AUDIT_REL_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported audit relationship type {type!r}")
    try:
        mgr = _classifier(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("audit: failed to create ClassificationExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # Point-in-time: asOfTime goes in the request body (get_relationships has no
    # as_of_time param — passing it as a kwarg is a silent no-op). LE-3 mechanism.
    body = {"class": "ResultsRequestBody"}
    if as_of_time:
        body["asOfTime"] = as_of_time
    try:
        raw = mgr.get_relationships(
            relationship_type=type,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            body=body if as_of_time else None,
        )
    except Exception as exc:
        logger.exception("audit: get_relationships(%s) failed", type)
        raise HTTPException(status_code=500, detail=str(exc))

    rows = [_serialize_relationship(r) for r in _rel_list(raw)]
    return JSONResponse({"items": rows, "total": len(rows)})
