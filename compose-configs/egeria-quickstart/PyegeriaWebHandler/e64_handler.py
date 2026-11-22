"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria 6.4 cards for the Egeria Explorer (odpi/egeria#9463, process variables and decisions).

Endpoints:
  GET /api/e64/status          -> whether the platform carries the 6.4 additions, with the gate's words
  GET /api/decisions           -> the Decisions list
  GET /api/decisions/{guid}    -> one Decision: header, body, dates, assessed inputs, outcomes
  GET /api/data-values         -> the Data Values list (DataValue and LiteralDataValue)
  GET /api/data-values/{guid}  -> one DataValue: format and type, the value, used by, stored in, embedded, part of

Reads use pyegeria's generic ClassificationExplorer calls (elements/by-type, elements/{guid}), which every
pyegeria the Portal runs has. So the cards don't need the unreleased 6.4 wrappers, and they work as soon as
the platform is 6.4.

The version gate (egeria_6_4_support): on an Egeria before 6.4 the answer is HTTP 200 with
`needs64: true` and the gate's sentence. It is never an error, and never an empty list that reads as
"none". Only when the platform's version can't be read is the read sent on trust, and then a bare HTTP 404
from it is read as "needs Egeria 6.4" as well. On a platform known to be 6.4 a 404 is a real error and is
reported as one.

Auth: token only (X-Egeria-Token header, stashed by EgeriaTokenMiddleware and read by async_apply_token).
No user_id/user_pwd query params; service credentials come from env vars, and only when no token is sent.
"""
from __future__ import annotations

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

import egeria_6_4_support as e64
from common_serialize import _authored_fields, _classifications, _generic_relationships, _header_summary
from egeria_auth import async_apply_token, service_password
from egeria_error_mapping import EGERIA_ERROR_RESPONSES, raise_egeria_http_error
from graph_keys import extract_graph_fields

router = APIRouter(tags=["egeria-6.4"])

_PAGE_SIZE = 100
_MAX_PAGES = 10


# ── Client factory (async only: every route here is async) ───────────────────────────────────────────────

async def _explorer_async(url: Optional[str] = None, server: Optional[str] = None):
    from pyegeria import ClassificationExplorer
    client = ClassificationExplorer(
        view_server=server or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
        platform_url=url or os.environ.get("EGERIA_PLATFORM_URL", "https://egeria-main:9443"),
        user_id=os.environ.get("EGERIA_USER", "erinoverview"),
        user_pwd=service_password(),
    )
    await async_apply_token(client)
    return client


def _raise_http(exc: Exception, log_msg: str = "") -> None:
    if isinstance(exc, HTTPException):
        raise exc
    raise_egeria_http_error(exc, log_msg)


def _needs64(what: str, purl: str, version: str = "", **extra) -> JSONResponse:
    return JSONResponse({"needs64": True, "words": e64.needs_6_4_words(what, purl, version), **extra})


async def _gate(client) -> tuple:
    """(carries, version, platform URL), never raising."""
    try:
        return await e64.async_egeria_6_4_status(client)
    except Exception:  # noqa: BLE001 -- the gate never fails a request
        return None, "", getattr(client, "platform_url", "") or ""


def _is_template(el: dict) -> bool:
    h = e64.hdr(el)
    if h.get("template"):
        return True
    return "Template" in e64.classification_names(el)


async def _list_of_type(client, type_name: str) -> tuple:
    """(elements, capped). Pages until Egeria returns no list (an empty or short page is not the end)."""
    raw, capped = [], False
    for page in range(_MAX_PAGES):
        batch = await client._async_get_elements(metadata_element_type=type_name, start_from=page * _PAGE_SIZE,
                                                 page_size=_PAGE_SIZE, output_format="JSON")
        if not isinstance(batch, list):
            break
        raw.extend(e for e in batch if isinstance(e, dict))
        if page == _MAX_PAGES - 1:
            capped = True
    seen, out = set(), []
    for el in raw:
        g = e64.hdr(el).get("guid")
        if g and g in seen:
            continue
        if g:
            seen.add(g)
        out.append(el)
    return out, capped


async def _read_element(client, guid: str, type_name: str) -> dict:
    raw = await client._async_get_element_by_guid(guid, element_type_name=type_name, graph_query_depth=1,
                                                  output_format="JSON")
    element = raw[0] if isinstance(raw, list) and raw else raw
    if not isinstance(element, dict) or not e64.hdr(element).get("guid"):
        raise HTTPException(status_code=404, detail=f"No element {guid!r} is visible to you. It may not exist, "
                                                    "or zone security may hide it.")
    return element


def _is_type(element: dict, type_name: str) -> bool:
    t = e64.hdr(element).get("type") or {}
    return t.get("typeName") == type_name or type_name in (t.get("superTypeNames") or [])


# ── Decision ─────────────────────────────────────────────────────────────────────────────────────────────

_ASSESSMENT_FIELDS = ("label", "description", "assessor", "assessorTypeName", "assessorPropertyName",
                      "assessmentTime", "expiryTime", "notes", "additionalProperties")
_OUTCOME_FIELDS = ("label", "description", "importance", "disposition")
_DECISION_KEYS = ("summary", "scope", "usage", "importance", "disposition", "implications", "notes",
                  "startTime", "lastReviewTime", "nextReviewTime", "expiryTime")
_DECISION_LISTS = ("inputsToDecision", "decisionOutcomes")
_NOT_IN_TABLE = {"class", "typeName", "extendedProperties", "additionalProperties", *_DECISION_KEYS,
                 "contentStatus", "userDefinedContentStatus", "authors", "description", "displayName"}


def serialize_decision_list_item(el: dict) -> dict:
    p = e64.props(el)
    guid = e64.hdr(el).get("guid", "")
    return {
        "guid": guid,
        "typeName": e64.type_name(el),
        "displayName": e64.display_name(p, guid),
        "qualifiedName": p.get("qualifiedName") or "",
        "disposition": p.get("disposition") or "",
        "contentStatus": p.get("contentStatus") or "",
        "nextReviewTime": p.get("nextReviewTime") or "",
        "expiryTime": p.get("expiryTime") or "",
    }


def serialize_decision(element: dict, carries: Optional[bool] = True, words: str = "",
                       requested=None) -> dict:
    """The Decision card. `requested`: the lists the read asked for (default: every list, a graph read)."""
    requested = e64.relationship_fields() if requested is None else requested
    p = e64.props(element)
    h = e64.hdr(element)
    guid = h.get("guid", "")
    implications = p.get("implications")
    if isinstance(implications, str):
        implications = [implications] if implications else []
    node = {
        # flat, top-level keys: GenericPropertiesTable reads item[key]
        **{k: v for k, v in p.items() if k not in _NOT_IN_TABLE and v not in (None, "", [], {})},
        "guid": guid,
        "typeName": e64.type_name(element),
        "superTypeNames": (h.get("type") or {}).get("superTypeNames") or [],
        "displayName": e64.display_name(p, guid),
        "description": p.get("description") or "",
        "status": h.get("status") or "",
        **{k: (p.get(k) if p.get(k) is not None else "") for k in _DECISION_KEYS if k != "implications"},
        "implications": implications or [],
        "additionalProperties": p.get("additionalProperties") or {},
        "mermaidGraph": element.get("mermaidGraph") or "",
        **{k: v for k, v in extract_graph_fields(element).items() if k != "mermaidGraph"},
        "_header": _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
        "assessments": e64.related_rows(element, "inputsToDecision", _ASSESSMENT_FIELDS),
        "outcomes": e64.related_rows(element, "decisionOutcomes", _OUTCOME_FIELDS),
        "lists": {k: e64.list_state(element, k, requested, carries, words) for k in _DECISION_LISTS},
        "relationships": _generic_relationships(element, skip=_DECISION_LISTS),
    }
    node["assessments"].sort(key=lambda r: ((r["displayName"] or "").lower(), str(r.get("assessmentTime") or "")))
    node["outcomes"].sort(key=lambda r: (r["displayName"] or "").lower())
    return node


# ── DataValue / LiteralDataValue ─────────────────────────────────────────────────────────────────────────

_POSITIONED = ("label", "description", "position")
_DATA_VALUE_LISTS = ("dataValueUses", "dataValueSources", "embeddedDataValues", "parentDataValues")
_DATA_VALUE_KEYS = ("dataFormat", "dataType", "length", "usage", "fingerprint", "fingerprintAlgorithm", "hash",
                    "hashAlgorithm")
_LITERAL_KEYS = ("dataValue", "dataValueList", "dataValueMap")
_DV_NOT_IN_TABLE = {"class", "typeName", "extendedProperties", "additionalProperties", "description", "displayName",
                    *_DATA_VALUE_KEYS, *_LITERAL_KEYS}


def position_of(row: dict):
    """A relationship's position as an int, or None when unset. Egeria's 0 means "unset" (the .http samples and
    ProcessingVariableProperties / EmbeddedDataValueProperties: Integer, 0 = no position)."""
    v = row.get("position")
    if isinstance(v, bool):
        return None
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    return n if n != 0 else None


def _by_position(rows: list) -> list:
    """Set positions ascending; rows with no position after them, by name. Each row gets `positionSet`."""
    for r in rows:
        r["position"] = position_of(r)
        r["positionSet"] = r["position"] is not None
    return sorted(rows, key=lambda r: (not r["positionSet"], r["position"] or 0, (r["displayName"] or "").lower()))


def literal_value(p: dict, is_literal: bool) -> dict:
    """{kind, dataValue, dataValueList, dataValueMap}. kind: literal | list | map | several | empty (a
    LiteralDataValue with no value recorded) | not-literal (a plain DataValue holds no value of its own)."""
    if not is_literal:
        return {"kind": "not-literal"}
    lit = p.get("dataValue")
    lst = p.get("dataValueList")
    mp = p.get("dataValueMap")
    lst = lst if isinstance(lst, list) and lst else None
    mp = mp if isinstance(mp, dict) and mp else None
    lit = lit if lit not in (None, "") else None
    present = [k for k, v in (("literal", lit), ("list", lst), ("map", mp)) if v is not None]
    kind = present[0] if len(present) == 1 else ("several" if present else "empty")
    return {"kind": kind, "dataValue": lit, "dataValueList": lst, "dataValueMap": mp}


def serialize_data_value_list_item(el: dict) -> dict:
    p = e64.props(el)
    guid = e64.hdr(el).get("guid", "")
    return {
        "guid": guid,
        "typeName": e64.type_name(el),
        "displayName": e64.display_name(p, guid),
        "qualifiedName": p.get("qualifiedName") or "",
        "dataType": p.get("dataType") or "",
        "dataFormat": p.get("dataFormat") or "",
    }


def serialize_data_value(element: dict, carries: Optional[bool] = True, words: str = "", requested=None) -> dict:
    """The DataValue card (also LiteralDataValue). `requested` as for serialize_decision."""
    requested = e64.relationship_fields() if requested is None else requested
    p = e64.props(element)
    h = e64.hdr(element)
    guid = h.get("guid", "")
    is_literal = _is_type(element, "LiteralDataValue")
    node = {
        **{k: v for k, v in p.items() if k not in _DV_NOT_IN_TABLE and v not in (None, "", [], {})},
        "guid": guid,
        "typeName": e64.type_name(element),
        "superTypeNames": (h.get("type") or {}).get("superTypeNames") or [],
        "displayName": e64.display_name(p, guid),
        "description": p.get("description") or "",
        "status": h.get("status") or "",
        "isLiteral": is_literal,
        **{k: (p.get(k) if p.get(k) is not None else "") for k in _DATA_VALUE_KEYS},
        "value": literal_value(p, is_literal),
        "additionalProperties": p.get("additionalProperties") or {},
        "mermaidGraph": element.get("mermaidGraph") or "",
        **{k: v for k, v in extract_graph_fields(element).items() if k != "mermaidGraph"},
        "_header": _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
        "usedBy": _by_position(e64.related_rows(element, "dataValueUses", _POSITIONED)),
        "storedIn": sorted(e64.related_rows(element, "dataValueSources", ("label", "description")),
                           key=lambda r: (r["displayName"] or "").lower()),
        "embedded": _by_position(e64.related_rows(element, "embeddedDataValues", _POSITIONED)),
        "partOf": _by_position(e64.related_rows(element, "parentDataValues", _POSITIONED)),
        "lists": {k: e64.list_state(element, k, requested, carries, words) for k in _DATA_VALUE_LISTS},
        "relationships": _generic_relationships(element, skip=_DATA_VALUE_LISTS),
    }
    return node


# ── Endpoints ────────────────────────────────────────────────────────────────────────────────────────────

@router.get("/api/e64/status", summary="Whether the platform carries the Egeria 6.4 additions",
            responses=EGERIA_ERROR_RESPONSES)
async def e64_status(url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    out = {"carries": carries, "version": version, "platformUrl": purl, "gateSource": e64.GATE_SOURCE}
    if carries is False:
        out["words"] = e64.needs_6_4_words("This view", purl, version)
    return JSONResponse(out)


@router.get("/api/decisions", summary="List Decisions (Egeria 6.4)", responses=EGERIA_ERROR_RESPONSES)
async def list_decisions(include_templates: bool = Query(False),
                         url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    if carries is False:
        return _needs64("The Decisions list", purl, version, items=[], total=0)
    try:
        raw, capped = await _list_of_type(client, "Decision")
    except Exception as exc:
        if carries is None and e64.is_missing_6_4_endpoint(exc):   # a 404 on a 6.4 platform is a real error
            return _needs64("The Decisions list", purl, items=[], total=0)
        _raise_http(exc, "get_elements(Decision) failed")
    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]
    items = [serialize_decision_list_item(e) for e in raw]
    items.sort(key=lambda x: (x["displayName"] or x["qualifiedName"]).lower())
    return JSONResponse({"items": items, "total": len(items), "capped": capped})


@router.get("/api/decisions/{guid}", summary="Get a Decision with its assessed inputs and outcomes (Egeria 6.4)",
            responses=EGERIA_ERROR_RESPONSES)
async def get_decision(guid: str, url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    if carries is False:
        return _needs64("The Decision card", purl, version)
    try:
        element = await _read_element(client, guid, "Decision")
    except Exception as exc:
        if carries is None and e64.is_missing_6_4_endpoint(exc):   # a 404 on a 6.4 platform is a real error
            return _needs64("The Decision card", purl)
        _raise_http(exc, "get_element_by_guid(Decision) failed")
    if not _is_type(element, "Decision"):
        raise HTTPException(status_code=404, detail=f"{guid!r} is a {e64.type_name(element) or 'element'}, "
                                                    "not a Decision.")
    return JSONResponse(serialize_decision(element, carries=True if carries is None else carries))


@router.get("/api/data-values", summary="List Data Values and Literal Data Values (Egeria 6.4)",
            responses=EGERIA_ERROR_RESPONSES)
async def list_data_values(include_templates: bool = Query(False),
                           url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    if carries is False:
        return _needs64("The Data Values list", purl, version, items=[], total=0)
    try:
        raw, capped = await _list_of_type(client, "DataValue")     # by-type includes LiteralDataValue
    except Exception as exc:
        if carries is None and e64.is_missing_6_4_endpoint(exc):   # a 404 on a 6.4 platform is a real error
            return _needs64("The Data Values list", purl, items=[], total=0)
        _raise_http(exc, "get_elements(DataValue) failed")
    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]
    items = [serialize_data_value_list_item(e) for e in raw]
    items.sort(key=lambda x: (x["displayName"] or x["qualifiedName"]).lower())
    return JSONResponse({"items": items, "total": len(items), "capped": capped})


@router.get("/api/data-values/{guid}", summary="Get a Data Value with its uses, sources and embedded values (Egeria 6.4)",
            responses=EGERIA_ERROR_RESPONSES)
async def get_data_value(guid: str, url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    if carries is False:
        return _needs64("The Data Value card", purl, version)
    try:
        element = await _read_element(client, guid, "DataValue")
    except Exception as exc:
        if carries is None and e64.is_missing_6_4_endpoint(exc):   # a 404 on a 6.4 platform is a real error
            return _needs64("The Data Value card", purl)
        _raise_http(exc, "get_element_by_guid(DataValue) failed")
    if not _is_type(element, "DataValue"):
        raise HTTPException(status_code=404, detail=f"{guid!r} is a {e64.type_name(element) or 'element'}, "
                                                    "not a Data Value.")
    return JSONResponse(serialize_data_value(element, carries=True if carries is None else carries))
