"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Locator — Data Lens.

A Data Lens (Egeria type DataLens, a governance control) says what scope of data a
piece of work needs: in time, in place, and by the elements that define the scope
(a Location, a Team, a BusinessCapability…). In Egeria's model the lens governs a
collection of the resources that meet it (GovernedBy), and resources are matched to it
by their DataScope classification. Here the collection is one of the person's work
lists, so a lens and a list together are a mini-catalog for one piece of work.

The lens's dimensions come from Egeria's DataLens type definition, read and grouped by
data_scope_handler._type_groups, so the editor follows Egeria when it adds dimensions.
Matching (_lens_match) is by the same shapes: periods overlap, bounds overlap, scope
elements share an element. A resource that records none of the lens's dimensions is not
"outside" the lens: it cannot be compared, and the page says how many there are.

The Portal's own lenses are named DataLens::portal::<user>::<slug>, and only their
creator changes them here, as with work lists.

Endpoints (writes need an X-Egeria-Token: the signed-in user is the author):
  GET    /api/resource-browser/lenses                         → the lenses the user can see
  GET    /api/resource-browser/lenses/{guid}                  → one lens, its lists, and the resources inside it
  POST   /api/resource-browser/lenses                         → create a lens (optionally governing a list)
  PUT    /api/resource-browser/lenses/{guid}                  → change a lens of yours
  POST   /api/resource-browser/lenses/{guid}/lists            → the lens governs a list of yours
  DELETE /api/resource-browser/lenses/{guid}/lists/{list}     → it stops governing it
"""

import re
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import async_apply_token
from egeria_error_mapping import raise_egeria_http_error

import data_scope_handler as ds
import resource_browser_handler as rb

router = APIRouter(tags=["resource-browser"])

_LENS_PREFIX = "DataLens::portal::"
_LENS_PAGE = 100
_LENS_MAX_PAGES = 10
_MATCH_SHOWN = 200          # resources listed as inside a lens; the count says if there are more


# ── Pure helpers (unit-tested in tests/test_resource_locator_lens.py) ─────────

def _parse_time(v) -> Optional[datetime]:
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None


def _scope_dims(props: Optional[dict]) -> dict:
    """The dimensions a scope or lens records, by shape and name.

    {"periods": {id: (start, end)}, "bounds": {id: (lo, hi)}, "elements": {name: guid}}.
    A period needs a start or an end; a bound needs a value other than 0 (Egeria
    returns 0 for bounds never set). Missing ends are None (open)."""
    props = props or {}
    periods, bounds = {}, {}
    for k in props:
        m = re.fullmatch(r"(\w+)StartTime", k)
        if m:
            s, e = _parse_time(props.get(k)), _parse_time(props.get(m.group(1) + "EndTime"))
            if s or e:
                periods[m.group(1)] = (s, e)
    for k in props:
        m = re.fullmatch(r"(\w+)EndTime", k)
        if m and m.group(1) not in periods and _parse_time(props[k]):
            periods[m.group(1)] = (None, _parse_time(props[k]))
    for k in props:
        m = re.fullmatch(r"(min|max)([A-Z]\w*)", k)
        if not m or m.group(2) in bounds:
            continue
        lo, hi = props.get("min" + m.group(2)), props.get("max" + m.group(2))
        lo = lo if isinstance(lo, (int, float)) and lo != 0 else None
        hi = hi if isinstance(hi, (int, float)) and hi != 0 else None
        if lo is not None or hi is not None:
            bounds[m.group(2)] = (lo, hi)
    elements = {k: v for k, v in (props.get("scopeElements") or {}).items() if v}
    return {"periods": periods, "bounds": bounds, "elements": elements}


def _overlaps(a: tuple, b: tuple) -> bool:
    """Two (lo, hi) intervals with open (None) ends overlap."""
    a_lo, a_hi = a
    b_lo, b_hi = b
    if a_hi is not None and b_lo is not None and b_lo > a_hi:
        return False
    if b_hi is not None and a_lo is not None and a_lo > b_hi:
        return False
    return True


def _lens_match(lens: dict, scope: Optional[dict]) -> dict:
    """How a resource's DataScope sits against a lens.

    {"outcome": "inside"|"outside"|"unknown", "compared": [...], "outside": [...]}.
    Only dimensions both record are compared. Inside: at least one is compared and
    every compared one overlaps. Outside: a compared one does not overlap. Unknown:
    nothing could be compared."""
    want, have = _scope_dims(lens), _scope_dims(scope)
    compared, outside = [], []
    for name, rng in want["periods"].items():
        if name in have["periods"]:
            compared.append(name)
            if not _overlaps(rng, have["periods"][name]):
                outside.append(name)
    for name, rng in want["bounds"].items():
        if name in have["bounds"]:
            compared.append(name)
            if not _overlaps(rng, have["bounds"][name]):
                outside.append(name)
    if want["elements"] and have["elements"]:
        compared.append("scopeElements")
        if not set(want["elements"].values()) & set(have["elements"].values()):
            outside.append("scopeElements")
    outcome = "unknown" if not compared else ("outside" if outside else "inside")
    return {"outcome": outcome, "compared": compared, "outside": outside}


def _lens_origin(qualified_name: str, me: Optional[str]) -> str:
    if me and qualified_name.startswith(f"{_LENS_PREFIX}{me}::"):
        return "mine"
    return "portal" if qualified_name.startswith(_LENS_PREFIX) else "other"


def _governed(el: dict) -> list:
    """The elements a lens governs, from any relationship list of type GovernedBy."""
    out = []
    for key, val in (el or {}).items():
        if key in ("elementHeader", "properties") or not isinstance(val, list):
            continue
        for rec in rb._related_recs(val):
            if rec["relationshipType"] == "GovernedBy":
                out.append({"guid": rec["guid"], "displayName": rec["displayName"], "typeName": rec["typeName"]})
    return list({r["guid"]: r for r in out}.values())


def _lens_record(el: dict, me: Optional[str], groups: list) -> dict:
    hdr = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    versions = hdr.get("versions") or {}
    names = {f["name"] for g in groups for f in g["fields"]}
    qn = props.get("qualifiedName", "")
    origin = _lens_origin(qn, me)
    return {
        "guid": hdr.get("guid", ""),
        "displayName": rb._display_name(props, hdr.get("guid", "")),
        "qualifiedName": qn,
        "description": props.get("description") or "",
        "scope": {k: v for k, v in props.items() if k in names and v not in (None, "", {}, [])},
        "dimensions": sorted(set(_scope_dims(props)["periods"]) | set(_scope_dims(props)["bounds"])
                             | ({"scopeElements"} if _scope_dims(props)["elements"] else set())),
        "origin": origin,
        "editable": origin == "mine",
        "governs": _governed(el),
        "createdBy": versions.get("createdBy") or "",
        "updatedBy": versions.get("updatedBy") or "",
        "updateTime": versions.get("updateTime") or versions.get("createTime") or "",
    }


def _lens_properties(name: str, description: str, dims: dict, qualified_name: str) -> dict:
    return {"class": "DataLensProperties", "typeName": "DataLens", "qualifiedName": qualified_name,
            "displayName": name, "description": description or "", **dims}


# ── Clients ───────────────────────────────────────────────────────────────────

async def _officer_async():
    from pyegeria import GovernanceOfficer
    client = GovernanceOfficer(**rb._client_kwargs())
    await async_apply_token(client)
    return client


async def _read_lens(client, guid: str) -> dict:
    el = await client._async_get_element_by_guid(
        guid, graph_query_depth=1, output_format="JSON",
        body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": ["GovernedBy"]})
    hdr = (el or {}).get("elementHeader") or {}
    if not isinstance(el, dict) or "DataLens" not in [rb._type_names(hdr)[0]] + rb._type_names(hdr)[1]:
        raise HTTPException(status_code=404, detail="No data lens with this identifier is visible to you. "
                                                    "It may not exist, or zone security may hide it from your user.")
    return el


async def _my_lens(client, guid: str, groups: list) -> tuple:
    me = rb._require_signed_in()
    el = await _read_lens(client, guid)
    rec = _lens_record(el, me, groups)
    if not rec["editable"]:
        raise HTTPException(status_code=403, detail="Only the person who made a data lens can change it.")
    return el, rec


async def _scoped_rows() -> list:
    """Every resource with a DataScope, as rows (cached per user: zone security differs)."""
    async def produce():
        client = await rb._explorer_async()
        els, capped = await rb._classified(client, "DataScope")
        return {"rows": rb._rows(els)[0], "capped": capped}
    value, stamp = await rb._cached("lens-scoped", produce)
    return value, stamp


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/resource-browser/lenses", summary="The data lenses the user can see")
async def get_lenses():
    me = rb._token_user()
    try:
        groups, _ = await ds._type_groups("DataLens")
        client = await rb._explorer_async()
        els, capped = await rb._all_elements(client, "DataLens", {"includeOnlyRelationships": ["GovernedBy"]},
                                             depth=1, page=_LENS_PAGE, max_pages=_LENS_MAX_PAGES)
    except HTTPException:
        raise
    except Exception as exc:
        if rb._is_unknown_type(exc):
            return JSONResponse({"lenses": [], "typeKnown": False, "capped": False, "asOf": rb._now_iso(), "source": ""})
        raise_egeria_http_error(exc, "resource-browser: lens list failed")
    lenses = [_lens_record(e, me, groups) for e in els]
    lenses.sort(key=lambda r: (r["origin"] != "mine", r["displayName"].lower()))
    return JSONResponse({"lenses": lenses, "typeKnown": True, "capped": capped, "asOf": rb._now_iso(),
                         "source": "ClassificationExplorer.get_elements (DataLens; GovernedBy)"})


@router.get("/api/resource-browser/lenses/{guid}", summary="One data lens, the lists it governs, and the resources inside it")
async def get_lens(guid: str):
    me = rb._token_user()
    try:
        groups, _ = await ds._type_groups("DataLens")
        client = await rb._explorer_async()
        el = await _read_lens(client, guid)
        scoped, stamp = await _scoped_rows()
    except HTTPException:
        raise
    except Exception as exc:
        rb._raise_not_visible_or_mapped(exc, f"resource-browser: lens {guid} failed")
    rec = _lens_record(el, me, groups)
    inside, outside, unknown = [], 0, 0
    for row in scoped["rows"]:
        m = _lens_match(rec["scope"], row["dataScope"])
        if m["outcome"] == "inside":
            inside.append(dict(row, matched=["inside on " + ", ".join(m["compared"])]))
        elif m["outcome"] == "outside":
            outside += 1
        else:
            unknown += 1
    inside.sort(key=lambda r: (r["kind"], r["displayName"].lower()))
    return JSONResponse({
        "lens": rec, "groups": groups,
        "inside": inside[:_MATCH_SHOWN], "insideCount": len(inside), "outsideCount": outside,
        "notComparable": unknown, "scopedCount": len(scoped["rows"]), "capped": scoped["capped"],
        "rule": "A resource is inside the lens when every dimension both record overlaps (periods and bounds "
                "overlap, scope elements share an element). A resource that records none of the lens's "
                "dimensions cannot be compared.",
        **rb._age(stamp),
        "source": "the lens (get_element_by_guid, GovernedBy) and every DataScope "
                  "(ClassificationExplorer.get_elements_by_classification), matched here",
    })


class LensBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    values: Optional[dict] = None
    listGuid: Optional[str] = None


def _checked(values: Optional[dict], groups: list) -> dict:
    dims, problems = ds._clean_values(values or {}, groups)
    if problems:
        raise HTTPException(status_code=422, detail="; ".join(problems))
    return dims


def _checked_name(name: Optional[str]) -> str:
    name = (name or "").strip()
    if not name or len(name) > 120:
        raise HTTPException(status_code=400, detail="A data lens needs a name of up to 120 characters.")
    return name


@router.post("/api/resource-browser/lenses", summary="Create a data lens, optionally governing a list of yours")
async def create_lens(body: LensBody):
    me = rb._require_signed_in()
    name = _checked_name(body.name)
    try:
        groups, _ = await ds._type_groups("DataLens")
        dims = _checked(body.values, groups)
        if body.listGuid:
            await rb._my_list(await rb._explorer_async(), body.listGuid)
        officer = await _officer_async()
        qn = f"{_LENS_PREFIX}{me}::{rb._list_slug(name, uuid.uuid4().hex[:6])}"
        guid = await officer._async_create_data_lens({
            "class": "NewElementRequestBody", "isOwnAnchor": True,
            "properties": _lens_properties(name, body.description or "", dims, qn)})
        if body.listGuid:
            await officer._async_attach_governed_by_definition(body.listGuid, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: create lens {name!r} failed")
    logger.info(f"resource-browser: lens {guid} created by {me}")
    return await get_lens(guid)


@router.put("/api/resource-browser/lenses/{guid}", summary="Change a data lens of yours")
async def edit_lens(guid: str, body: LensBody):
    try:
        groups, _ = await ds._type_groups("DataLens")
        client = await rb._explorer_async()
        el, rec = await _my_lens(client, guid, groups)
        props = el.get("properties") or {}
        name = _checked_name(body.name if body.name is not None else rec["displayName"])
        dims = _checked(body.values, groups) if body.values is not None else rec["scope"]
        description = body.description if body.description is not None else rec["description"]
        officer = await _officer_async()
        # Full replace, so a dimension emptied in the editor is removed; the lens's other
        # governance-definition properties (summary, scope, importance…) are carried across.
        names = {f["name"] for g in groups for f in g["fields"]}
        kept = {k: v for k, v in props.items() if k not in names and k not in ("displayName", "description", "class", "typeName")}
        await officer._async_update_governance_definition(guid, {
            "class": "UpdateElementRequestBody", "mergeUpdate": False,
            "properties": {**kept, **_lens_properties(name, description, dims, props.get("qualifiedName") or rec["qualifiedName"])}})
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: edit lens {guid} failed")
    return await get_lens(guid)


class LensListBody(BaseModel):
    listGuid: str


@router.post("/api/resource-browser/lenses/{guid}/lists", summary="The lens governs a list of yours")
async def govern_list(guid: str, body: LensListBody):
    try:
        groups, _ = await ds._type_groups("DataLens")
        client = await rb._explorer_async()
        _el, rec = await _my_lens(client, guid, groups)
        await rb._my_list(client, body.listGuid)
        if body.listGuid not in {g["guid"] for g in rec["governs"]}:
            officer = await _officer_async()
            await officer._async_attach_governed_by_definition(body.listGuid, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: lens {guid} govern list {body.listGuid} failed")
    return await get_lens(guid)


@router.delete("/api/resource-browser/lenses/{guid}/lists/{list_guid}", summary="The lens stops governing a list")
async def ungovern_list(guid: str, list_guid: str):
    try:
        groups, _ = await ds._type_groups("DataLens")
        client = await rb._explorer_async()
        await _my_lens(client, guid, groups)
        officer = await _officer_async()
        await officer._async_detach_governed_by_definition(list_guid, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: lens {guid} ungovern list {list_guid} failed")
    return await get_lens(guid)
