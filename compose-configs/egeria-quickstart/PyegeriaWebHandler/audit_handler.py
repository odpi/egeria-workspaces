# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Audit — FastAPI router.

Serves the egeria-audit SPA and the audit API. Four tabs:
  - Exceptions / Certifications / Licenses : governance relationships
    (ClassificationExplorer.get_relationships), point-in-time via asOfTime.
  - Users : platform user accounts (RuntimeManager + SecurityOfficer).

Governance-zone security (important — explains "missing" rows):
  Relationship visibility is filtered by the *requesting user's* governance-zone
  access. get_relationships runs as the user passed in the query (the demo
  persona / connected Egeria user), so the platform's metadata security
  connector hides relationships whose end1 element sits in a zone that user
  cannot access. This is by design — the audit view deliberately respects each
  viewer's access rights rather than elevating to a privileged reader.
    Example (Coco data): the two License relationships attach to CSVFiles in the
    'landing-area' / 'quarantine' zones, so erinoverview / peterprofile / tanyatidie
    see them but garygeeke / calliequartile see zero. Same query, different counts
    by design. The SPA's empty state and a 🔒 toolbar chip surface this to users.

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
import re
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

import asyncio
from egeria_auth import apply_token, async_apply_token

# Matches unresolved Egeria template placeholders such as ~{hospitalName}~
_TEMPLATE_PLACEHOLDER_RE = re.compile(r"^~\{[^}]+\}~$")

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
    found' (and similar) when empty — always normalise to a list of dicts.
    Some pyegeria versions wrap results in a dict with a 'relationships' key."""
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for key in ('relationships', 'items', 'elements', 'list'):
            if key in raw and isinstance(raw[key], list):
                return [r for r in raw[key] if isinstance(r, dict)]
    return []


# ── SPA ───────────────────────────────────────────────────────────────────────

@router.get("/egeria-audit", include_in_schema=False)
def serve_audit():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Audit page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


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


def _first_element(raw):
    """get_element_by_* returns a dict, a 1-item list, or a 'not found' string."""
    if isinstance(raw, list):
        return raw[0] if raw and isinstance(raw[0], dict) else None
    return raw if isinstance(raw, dict) else None


@router.get("/api/audit/element/{guid}", summary="Full element properties (depth 0) for a detail pane")
def get_audit_element(
    guid: str,
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Resolve an element (end1, end2, or a GUID-form actor) for the detail panes."""
    try:
        mgr = _classifier(url, server, user_id, user_pwd)
        body = {"class": "GetRequestBody", "graphQueryDepth": 0}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = mgr.get_element_by_guid(guid=guid, graph_query_depth=0, output_format="JSON", body=body)
    except Exception as exc:
        logger.exception("audit: get_element_by_guid(%s) failed", guid)
        raise HTTPException(status_code=500, detail=str(exc))
    el = _first_element(raw)
    if not el:
        raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")
    return JSONResponse(el)


@router.get("/api/audit/actor", summary="Resolve a steward/certifiedBy/… actor (GUID or unique-name)")
def resolve_audit_actor(
    value:        str = Query(..., description="The xxx value: a GUID, or a property value when property_name is set"),
    property_name: Optional[str] = Query(None, description="xxxPropertyName — when set, resolve by unique name"),
    type_name:    Optional[str] = Query(None, description="xxxTypeName — metadataElementTypeName for the unique-name lookup"),
    as_of_time:   Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Per the spec: if propertyName is set, resolve the actor by unique name
    (get_element_by_unique_name); otherwise `value` is the actor GUID."""
    # Unresolved template placeholders (e.g. ~{hospitalName}~) are stored as-is
    # in relationship properties when a certification/license was created from a
    # template whose substitution values were never supplied.  Egeria rejects a
    # uniqueName lookup of such a string with a 400.  Return a synthetic stub so
    # the UI can display the raw value instead of an error.
    if _TEMPLATE_PLACEHOLDER_RE.match(value.strip()):
        return JSONResponse({
            "properties": {
                "name":    value,
                "summary": "Unresolved template placeholder — the certification or license was created "
                           "from a template and this actor has not yet been assigned.",
            },
        })
    try:
        mgr = _classifier(url, server, user_id, user_pwd)
        if property_name and property_name.lower() != "guid":
            # Must use FindPropertyNameProperties format — passing a GetRequestBody
            # body overrides pyegeria's default and drops propertyValue/propertyName,
            # causing Egeria to receive null for uniqueName (OPEN-METADATA-400-004).
            body = {"class": "FindPropertyNameProperties", "propertyValue": value, "propertyName": property_name}
            if type_name:
                body["metadataElementTypeName"] = type_name
            if as_of_time:
                body["asOfTime"] = as_of_time
            raw = mgr.get_element_by_unique_name(name=value, property_name=property_name, output_format="JSON", body=body)
        else:
            body = {"class": "GetRequestBody", "graphQueryDepth": 0}
            if as_of_time:
                body["asOfTime"] = as_of_time
            raw = mgr.get_element_by_guid(guid=value, graph_query_depth=0, output_format="JSON", body=body)
    except Exception as exc:
        logger.exception("audit: resolve_actor(%s) failed", value)
        raise HTTPException(status_code=500, detail=str(exc))
    el = _first_element(raw)
    if not el:
        return JSONResponse({"properties": {"name": value, "summary": "Actor not found in metadata store — the value may reference an element that has not been loaded."}})
    return JSONResponse(el)


# ── Users tab (platforms + user accounts) ─────────────────────────────────────
# RuntimeManager lists platforms; SecurityOfficer reads/writes user accounts.
# NOTE: the status change mutates an account — it is admin-gated (_is_admin) and
# the frontend confirms. The demo security connector is currently unpopulated
# (0 users), so the mutation path needs verification against a populated platform.
from pydantic import BaseModel


def _runtime_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import RuntimeManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = RuntimeManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


async def _security_officer_async(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria.egeria_tech_client import SecurityOfficer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = SecurityOfficer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    await async_apply_token(mgr)
    return mgr


def _security_officer(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria.egeria_tech_client import SecurityOfficer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = SecurityOfficer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


@router.get("/api/audit/platforms", summary="OMAG Server Platforms (Users tab dropdown)")
def list_platforms(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        rm = _runtime_manager(url, server, user_id, user_pwd)
        raw = rm.get_platforms_by_type(filter_string="OMAG Server Platform", output_format="JSON")
    except Exception as exc:
        logger.exception("audit: get_platforms_by_type failed")
        raise HTTPException(status_code=500, detail=str(exc))
    out = []
    for e in (raw if isinstance(raw, list) else []):
        hdr = e.get("elementHeader") or {}
        props = e.get("properties") or {}
        out.append({"guid": hdr.get("guid") or "", "displayName": props.get("displayName") or props.get("qualifiedName") or hdr.get("guid") or ""})
    out.sort(key=lambda p: (p.get("displayName") or "").lower())
    return JSONResponse({"platforms": out})


async def _user_names(so, platform_name, platform_guid):
    """Return the list of user IDs registered with a platform's security connector.

    Robust against the pyegeria version where SecurityOfficer.get_user_list reads
    the wrong response key: the server returns a NameListResponse with the IDs
    under ``names``, but some versions read ``userIds`` → []. Try the library
    method first, then fall back to the raw endpoint's ``names`` key.
    """
    try:
        names = so.get_user_list(platform_name, None, None, platform_guid)
        if isinstance(names, list) and names:
            return names
    except Exception:
        logger.debug("audit: get_user_list raised; falling back to raw names")
    try:
        url = f"{so.security_officer_base_url}/platforms/{platform_guid}/user-accounts"
        r = await so._async_make_request("GET", url, params={})
        j = r.json()
        return j.get("names") or j.get("userIds") or []
    except Exception:
        logger.exception("audit: raw user-accounts fetch failed")
        return []


@router.get("/api/audit/users", summary="User accounts on a platform")
async def list_users(
    platform_guid: str = Query(...),
    platform_name: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        so = await _security_officer_async(url, server, user_id, user_pwd)
        names = await _user_names(so, platform_name, platform_guid)
    except Exception as exc:
        logger.exception("audit: get_user_list failed")
        raise HTTPException(status_code=500, detail=str(exc))
    if not isinstance(names, list):
        names = []
    # One get_user_account per user is an N+1 fan-out — serial it took ~77s for 81
    # users (browser/proxy timeout → empty tab). Fetch them concurrently (bounded).
    sem = asyncio.Semaphore(40)

    async def _one(nm):
        async with sem:
            try:
                a = await so._async_get_user_account(platform_name, nm, platform_guid)
                return a if isinstance(a, dict) else {"userId": nm}
            except Exception:
                return {"userId": nm}

    try:
        accounts = list(await asyncio.gather(*[_one(n) for n in names]))
    except Exception:
        logger.exception("audit: concurrent user-account fetch failed")
        accounts = [{"userId": n} for n in names]

    # The account carries userId (login, e.g. 'garygeeke') + userName (friendly,
    # e.g. 'Gary Geeke') — there is no displayName field — so map User Name to the
    # userId and Display Name to userName (the spec's literal field names predate
    # the actual UserAccount shape).
    rows = [{
        "userName":          acc.get("userId") or "",
        "userAccountType":   acc.get("userAccountType") or "",
        "displayName":       acc.get("userName") or "",
        "userAccountStatus": acc.get("userAccountStatus") or "",
        "account":           acc,
    } for acc in accounts]
    rows.sort(key=lambda r: (r.get("userName") or "").lower())
    return JSONResponse({"users": rows, "total": len(rows)})


class _UserStatusBody(BaseModel):
    platform_guid: str
    platform_name: Optional[str] = None
    user_id: str
    status: str


@router.post("/api/audit/users/status", summary="Change a user's account status (admin only)")
def set_user_status(request: Request, body: _UserStatusBody):
    # Privileged mutation — admin only. Reuse the demo/freshstart admin gate.
    try:
        from demo_feedback_handler import _is_admin
    except Exception:
        _is_admin = None
    if _is_admin is not None and not _is_admin(request):
        raise HTTPException(status_code=403, detail="Changing an account status requires an administrator.")
    try:
        so = _security_officer()
        # get-modify-put: fetch the account, set the new status, write it back.
        acc = so.get_user_account(body.platform_name, body.user_id, body.platform_guid)
        if not isinstance(acc, dict):
            raise HTTPException(status_code=404, detail=f"User {body.user_id!r} not found")
        acc = dict(acc)
        acc["userAccountStatus"] = body.status
        so.set_user_account(body.platform_name, acc, body.platform_guid)
    except HTTPException:
        raise
    except Exception as exc:
        http_code = getattr(exc, "response_code", None) or getattr(exc, "http_status_code", None)
        s = str(exc).upper()
        if http_code in (401, 403) or "USER_NOT_AUTHORIZED" in s or "NOT_AUTHORIZED" in s or "AUTHORIZATION_ERROR" in s:
            raise HTTPException(status_code=403, detail="Insufficient privilege — your Egeria user does not have permission to change account status.")
        logger.exception("audit: set_user_account failed")
        raise HTTPException(status_code=500, detail=str(exc))
    logger.info("audit: user %s status set to %s on platform %s", body.user_id, body.status, body.platform_guid)
    return JSONResponse({"ok": True, "userName": body.user_id, "userAccountStatus": body.status})
