"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Statements of Applicability — FastAPI router for Egeria Explorer's
"Statements of Applicability" section.

A StatementOfApplicability (Egeria 6.3, Security Officer OMVS) is an
AuthoredReferenceable that records, for one scope (an ISMS, a programme),
which governance controls apply and how far each one is implemented. Each
assessed control is linked by a ControlApplicability relationship whose
properties carry the assessment (label, isApplicable, justification,
inclusionReasons, implementationStatus, implementationDescription,
reviewDate, description).

Endpoints:
  GET /api/statements-of-applicability          → list (find_statements_of_applicability)
  GET /api/statements-of-applicability/{guid}   → detail + controls table + status summary

Auth: token only (X-Egeria-Token header, stashed by EgeriaTokenMiddleware and
read by async_apply_token). No user_id/user_pwd query params; service
credentials come from env vars only and are used only when no token is sent.

Absence is never reported as a value: a failed read is an HTTP error, a
missing SoA is a 404, and "no controls linked" is an empty `controls` list
with `controlsRead: true`.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from common_serialize import _authored_fields, _classifications, _generic_relationships, _header_summary
from egeria_auth import async_apply_token
from egeria_error_mapping import EGERIA_ERROR_RESPONSES, raise_egeria_http_error
from graph_keys import extract_graph_fields

router = APIRouter(tags=["statements-of-applicability"])

_CA_TYPE = "ControlApplicability"

# Page through the list; stop at the first page that is not a full list of elements
# (pyegeria returns the "No elements found" string for an empty page). Capped so a
# runaway estate can't hold the request open; `capped` says the list may be partial.
_PAGE_SIZE = 100
_MAX_PAGES = 10

# Egeria's ControlImplementationStatus values, in order. Read from pyegeria when it
# has the enum so a new value appears without a code change here.
_FALLBACK_STATUSES = ("NOT_STARTED", "PLANNED", "PARTIALLY_IMPLEMENTED", "IMPLEMENTED", "OTHER")


def _implementation_statuses() -> tuple:
    try:
        from pyegeria.models import ControlImplementationStatus
        return tuple(s.value for s in ControlImplementationStatus)
    except ImportError:
        return _FALLBACK_STATUSES


# ── Client factory (async only — every route here is async) ──────────────────

async def _security_officer_async(url: Optional[str] = None, server: Optional[str] = None):
    from pyegeria.omvs.security_officer import SecurityOfficer
    mgr = SecurityOfficer(
        view_server=server or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
        platform_url=url or os.environ.get("EGERIA_PLATFORM_URL", "https://egeria-main:9443"),
        user_id=os.environ.get("EGERIA_USER", "erinoverview"),
        user_pwd=os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )
    await async_apply_token(mgr)
    return mgr


def _raise_http(exc: Exception, log_msg: str = "") -> None:
    """HTTPException (incl. PlatformRefused) passes through; pyegeria errors map by type."""
    if isinstance(exc, HTTPException):
        raise exc
    raise_egeria_http_error(exc, log_msg)


# ── Serialization ────────────────────────────────────────────────────────────

def _hdr(el: dict) -> dict:
    return el.get("elementHeader") or {}


def _props(el: dict) -> dict:
    return el.get("properties") or {}


def _type_name(el: dict) -> str:
    return (_hdr(el).get("type") or {}).get("typeName") or ""


def _is_template(el: dict) -> bool:
    hdr = _hdr(el)
    if hdr.get("template"):
        return True
    for val in hdr.values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


def _rel_type(entry: dict) -> str:
    return ((entry.get("relationshipHeader") or {}).get("type") or {}).get("typeName") or ""


def _serialize_list_item(el: dict) -> dict:
    p = _props(el)
    return {
        "guid":              _hdr(el).get("guid", ""),
        "typeName":          _type_name(el),
        "displayName":       p.get("displayName") or "",
        "qualifiedName":     p.get("qualifiedName") or "",
        "scope":             p.get("scope") or "",
        "versionIdentifier": p.get("versionIdentifier") or "",
        "contentStatus":     p.get("contentStatus") or "",
        "reviewDate":        p.get("reviewDate") or "",
    }


def _control_rows(element: dict) -> list:
    """One row per ControlApplicability link: the control, plus the assessment.

    Kept separate from the control's own properties (`control`) so a relationship
    `description` never hides the control's description. `isApplicable` is the
    stored value or None — the UI says "applicable (default)" for None, since
    Egeria treats an unset flag as applicable.
    """
    rows = []
    seen = set()
    for key in ("otherRelatedElements", "relationships"):
        for entry in element.get(key) or []:
            if not isinstance(entry, dict) or _rel_type(entry) != _CA_TYPE:
                continue
            rel_guid = (entry.get("relationshipHeader") or {}).get("guid")
            if rel_guid and rel_guid in seen:
                continue
            if rel_guid:
                seen.add(rel_guid)
            control = entry.get("relatedElement") or {}
            cp = _props(control)
            rp = {k: v for k, v in (entry.get("relationshipProperties") or {}).items()
                  if k not in ("class", "typeName")}
            ch = _hdr(control)
            rows.append({
                "guid":                      ch.get("guid", ""),
                "typeName":                  _type_name(control),
                "displayName":               cp.get("displayName") or cp.get("name") or cp.get("qualifiedName") or "",
                "qualifiedName":             cp.get("qualifiedName") or "",
                "identifier":                cp.get("identifier") or "",
                "controlDescription":        cp.get("description") or "",
                "label":                     rp.get("label") or "",
                "isApplicable":              rp.get("isApplicable"),
                "justification":             rp.get("justification") or "",
                "inclusionReasons":          rp.get("inclusionReasons") or [],
                "implementationStatus":      rp.get("implementationStatus") or "",
                "implementationDescription": rp.get("implementationDescription") or "",
                "reviewDate":                rp.get("reviewDate") or "",
                "notes":                     rp.get("description") or "",
                "relationshipGuid":          rel_guid or "",
            })
    rows.sort(key=lambda r: (_label_sort_key(r["label"]), r["displayName"].lower()))
    return rows


def _label_sort_key(label: str):
    """'5.1' < '8.20' < '8.25' (numeric parts compare as numbers); unlabelled rows last."""
    if not label:
        return (1, ())
    parts = []
    for piece in str(label).replace("-", ".").split("."):
        parts.append((0, int(piece), "") if piece.isdigit() else (1, 0, piece.lower()))
    return (0, tuple(parts))


def _summary(rows: list) -> dict:
    """Applicable controls counted by implementation status; every status present,
    so a 0 is a real count. A control with no status is counted under `unset`, not
    folded into NOT_STARTED — that it was never recorded is itself worth showing."""
    by_status = {s: 0 for s in _implementation_statuses()}
    unset = not_applicable = 0
    for r in rows:
        if r["isApplicable"] is False:
            not_applicable += 1
            continue
        s = r["implementationStatus"]
        if not s:
            unset += 1
        else:
            by_status[s] = by_status.get(s, 0) + 1
    return {
        "total":         len(rows),
        "applicable":    len(rows) - not_applicable,
        "notApplicable": not_applicable,
        "byStatus":      by_status,
        "statusUnset":   unset,
    }


def _without_control_links(element: dict) -> dict:
    """A copy of the element with ControlApplicability entries removed, so the
    generic relationship cards don't repeat what the controls table shows."""
    out = dict(element)
    for key in ("otherRelatedElements", "relationships"):
        if isinstance(out.get(key), list):
            out[key] = [e for e in out[key] if not (isinstance(e, dict) and _rel_type(e) == _CA_TYPE)]
    return out


# Properties shown in the header/summary or elsewhere, not repeated in the generic table.
_NOT_IN_TABLE = {"class", "typeName", "extendedProperties", "additionalProperties"}


def _serialize_detail(element: dict) -> dict:
    p = _props(element)
    rows = _control_rows(element)
    node = {
        # flat, top-level keys: GenericPropertiesTable reads item[key]
        **{k: v for k, v in p.items() if k not in _NOT_IN_TABLE and v not in (None, "", [], {})},
        "guid":           _hdr(element).get("guid", ""),
        "typeName":       _type_name(element),
        "superTypeNames": (_hdr(element).get("type") or {}).get("superTypeNames") or [],
        "status":         _hdr(element).get("status") or "",
        "additionalProperties": p.get("additionalProperties") or {},
        "mermaidGraph":   element.get("mermaidGraph") or "",
        **{k: v for k, v in extract_graph_fields(element).items() if k != "mermaidGraph"},
        "_header":        _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
        "controls":       rows,
        "controlsRead":   True,
        "summary":        _summary(rows),
        "relationships":  _generic_relationships(_without_control_links(element)),
    }
    return node


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/api/statements-of-applicability", summary="List statements of applicability",
            responses=EGERIA_ERROR_RESPONSES)
async def list_statements_of_applicability(
    search_string:     Optional[str] = Query(None),
    include_templates: bool          = Query(False),
    url:    Optional[str] = Query(None),
    server: Optional[str] = Query(None),
):
    try:
        mgr = await _security_officer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "SecurityOfficer client failed")

    raw: list = []
    capped = False
    try:
        for page in range(_MAX_PAGES):
            batch = await mgr._async_find_statements_of_applicability(
                search_string=search_string or "*",
                starts_with=True,
                ignore_case=True,
                graph_query_depth=0,   # the list reads flat properties only
                start_from=page * _PAGE_SIZE,
                page_size=_PAGE_SIZE,
                output_format="JSON",
            )
            if not isinstance(batch, list) or not batch:
                break
            raw.extend(batch)
            if page == _MAX_PAGES - 1:
                capped = True
    except Exception as exc:
        _raise_http(exc, "find_statements_of_applicability failed")

    raw = [e for e in raw if isinstance(e, dict)]
    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]
    items = [_serialize_list_item(e) for e in raw]
    items.sort(key=lambda x: (x["displayName"] or x["qualifiedName"]).lower())
    return JSONResponse({"items": items, "total": len(items), "capped": capped})


@router.get("/api/statements-of-applicability/{guid}", summary="Get a statement of applicability with its controls",
            responses=EGERIA_ERROR_RESPONSES)
async def get_statement_of_applicability(
    guid:   str,
    url:    Optional[str] = Query(None),
    server: Optional[str] = Query(None),
):
    try:
        mgr = await _security_officer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "SecurityOfficer client failed")
    try:
        # max_mermaid_node_count defaults to 5 in pyegeria's get-by-guid helper (ISSUE-23)
        raw = await mgr._async_get_statement_of_applicability_by_guid(
            guid, graph_query_depth=3, output_format="JSON", max_mermaid_node_count=250)
    except Exception as exc:
        _raise_http(exc, "get_statement_of_applicability_by_guid failed")

    element = raw[0] if isinstance(raw, list) and raw else raw
    if not isinstance(element, dict) or not _hdr(element).get("guid"):
        raise HTTPException(status_code=404, detail=f"Statement of applicability {guid!r} not found")
    return JSONResponse(_serialize_detail(element))
