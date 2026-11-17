"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Data Scope: read, set, change and clear the DataScope classification on an element,
and describe its dimensions so a page can draw an editor for them.

The dimensions come from Egeria's own type definition (ValidMetadataManager
get_typedef_by_name), not from a list kept here, so when Egeria adds a dimension to
DataScope (6.2 added the validity and coverage times) it appears in the editor with no
change to the Portal. The same reading serves the DataLens governance definition, which
carries the same dimensions (resource_browser_handler.py's lens endpoints use it).

Attributes are grouped by shape, not by name:
  - a pair  <x>StartTime / <x>EndTime  (dates)         → a time range "<X>"
  - a pair  min<X> / max<X>            (numbers)       → a bound on X
  - map<string,string>                                  → a list of name/value pairs
  - anything else                                       → one field of its type
Only the labels and the order of the groups are hinted here (_GROUP_HINTS); an
attribute this file has never heard of still gets a field.

Endpoints (writes need an X-Egeria-Token: the signed-in user is the author):
  GET    /api/data-scope/dimensions?type=DataScope|DataLens → the dimensions, grouped
  GET    /api/data-scope/{guid}                              → the element's DataScope, or none
  PUT    /api/data-scope/{guid}                              → set or change it
  DELETE /api/data-scope/{guid}                              → clear its time and place

additionalProperties on DataScope is also written by Egeria's OpenLineage data scope
governance service (read counts per analysis window). Every write here keeps it: a PUT
replaces the dimensions it was given and carries the stored additionalProperties
across, and a DELETE that would drop those readings leaves the classification holding
only them.
"""

import re
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import async_apply_token, token_user as _token_user
from egeria_error_mapping import raise_egeria_http_error

router = APIRouter(tags=["data-scope"])

_SCOPE_TYPES = ("DataScope", "DataLens")
_PRESERVED = "additionalProperties"     # written by the lineage governance service; never edited here
_TYPEDEF_TTL = 3600                     # seconds; type definitions change only on an Egeria upgrade
_typedef_cache: dict = {}

# Labels and order for the groups people know; anything else is labelled from its name.
_GROUP_HINTS = {
    "dataCollection": ("When the data was collected", 10),
    "dataValidity": ("When the data is valid", 20),
    "dataCoverage": ("What period the data covers", 30),
    "Latitude": ("Latitude (−90 to 90)", 40),
    "Longitude": ("Longitude (−180 to 180)", 41),
    "Height": ("Height above ground", 42),
    "scopeElements": ("Scope elements (name → Egeria element)", 60),
    "additionalProperties": ("Additional properties", 90),
}
_RANGES = {"Latitude": (-90.0, 90.0), "Longitude": (-180.0, 180.0)}


# ── Pure helpers (unit-tested in tests/test_data_scope.py) ────────────────────

def _words(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name).strip()
    return s[:1].upper() + s[1:].lower()


def _attr_kind(type_name: str) -> str:
    t = (type_name or "").lower()
    if t.startswith("map<"):
        return "map"
    if t == "date":
        return "date"
    if t in ("float", "double", "int", "long", "short", "integer"):
        return "number"
    if t == "boolean":
        return "boolean"
    return "string"


def _dimensions(attributes: list) -> list:
    """Group a type definition's attributes into editor groups (see the module docstring).

    `attributes` are typedef attributeDefinitions: {attributeName, attributeType: {name},
    attributeDescription}. Returns groups ordered by _GROUP_HINTS, then by name:
    {"id", "label", "shape": "timeRange"|"bound"|"map"|"field", "fields": [...]} where each
    field is {"name", "kind", "role": "start"|"end"|"min"|"max"|"value", "help"}."""
    by_name = {}
    for a in attributes or []:
        name = a.get("attributeName")
        if name:
            by_name[name] = {"name": name, "kind": _attr_kind((a.get("attributeType") or {}).get("name")),
                             "help": a.get("attributeDescription") or ""}
    groups, used = [], set()

    def add(gid, shape, fields):
        label, order = _GROUP_HINTS.get(gid, (_words(gid), 50))
        groups.append({"id": gid, "label": label, "shape": shape, "fields": fields, "_order": order})
        used.update(f["name"] for f in fields)

    for name, f in by_name.items():
        m = re.fullmatch(r"(\w+)StartTime", name)
        end = by_name.get(m.group(1) + "EndTime") if m else None
        if m and f["kind"] == "date" and end and end["kind"] == "date":
            add(m.group(1), "timeRange", [dict(f, role="start"), dict(end, role="end")])
    for name, f in by_name.items():
        m = re.fullmatch(r"min([A-Z]\w*)", name)
        hi = by_name.get("max" + m.group(1)) if m else None
        if m and name not in used and f["kind"] == "number" and hi and hi["kind"] == "number":
            add(m.group(1), "bound", [dict(f, role="min"), dict(hi, role="max")])
    for name, f in by_name.items():
        if name not in used:
            add(name, "map" if f["kind"] == "map" else "field", [dict(f, role="value")])
    groups.sort(key=lambda g: (g["_order"], g["id"]))
    for g in groups:
        g.pop("_order")
        if g["shape"] == "bound" and g["id"] in _RANGES:
            g["range"] = list(_RANGES[g["id"]])
        if g["id"] == _PRESERVED:
            g["readOnly"] = True
    return groups


def _field_index(groups: list) -> dict:
    return {f["name"]: (g, f) for g in groups for f in g["fields"]}


def _to_iso(value: str) -> str:
    """A date or date-time from a form → an ISO-8601 UTC timestamp Egeria accepts."""
    v = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        v += "T00:00:00"
    dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _clean_values(values: dict, groups: list) -> tuple:
    """(properties, problems): form values checked against the dimensions.

    Empty values are dropped (they clear that dimension). Unknown names and the preserved
    additionalProperties are refused; numbers, dates and maps are converted; a range whose
    start is after its end, a bound whose min is above its max, or a latitude or longitude
    out of range is a problem. Nothing is written when there is a problem."""
    idx = _field_index(groups)
    props, problems = {}, []
    for name, raw in (values or {}).items():
        if name not in idx:
            problems.append(f"{name} is not a dimension of this type")
            continue
        g, f = idx[name]
        if g.get("readOnly"):
            problems.append(f"{name} is kept as it is and cannot be set here")
            continue
        if raw is None or raw == "" or raw == {} or raw == []:
            continue
        try:
            if f["kind"] == "number":
                props[name] = float(raw)
            elif f["kind"] == "date":
                props[name] = _to_iso(str(raw))
            elif f["kind"] == "map":
                if not isinstance(raw, dict):
                    raise ValueError("expected name/value pairs")
                kept = {str(k).strip(): str(v).strip() for k, v in raw.items() if str(k).strip() and str(v).strip()}
                if kept:
                    props[name] = kept
            elif f["kind"] == "boolean":
                props[name] = bool(raw)
            else:
                props[name] = str(raw)
        except (TypeError, ValueError) as exc:
            problems.append(f"{name}: {exc}")
    for g in groups:
        a, b = (g["fields"] + [None, None])[:2]
        if g["shape"] in ("timeRange", "bound") and a["name"] in props and b["name"] in props:
            if props[a["name"]] > props[b["name"]]:
                problems.append(f"{g['label']}: the {'start' if g['shape'] == 'timeRange' else 'minimum'} "
                                f"is after the {'end' if g['shape'] == 'timeRange' else 'maximum'}")
        if g.get("range"):
            lo, hi = g["range"]
            for f in g["fields"]:
                if f["name"] in props and not lo <= props[f["name"]] <= hi:
                    problems.append(f"{f['name']} must be between {lo:g} and {hi:g}")
    return props, problems


def _has_place(props: dict) -> bool:
    """Egeria returns 0 for bounds that were never set, so all-zero bounds mean no place."""
    return any(isinstance(v, (int, float)) and v != 0
               for k, v in (props or {}).items() if re.fullmatch(r"(min|max)[A-Z]\w*", k))


def _summary(props: Optional[dict], groups: list) -> dict:
    """What a DataScope records, for display: which dimensions hold values, and whether its
    only content is the readings the lineage service keeps (which are usage, not scope)."""
    if props is None:
        return {"present": False, "dimensions": [], "usageOnly": False}
    idx = _field_index(groups)
    filled = []
    for g in groups:
        if g.get("readOnly"):
            continue
        names = [f["name"] for f in g["fields"]]
        vals = [props.get(n) for n in names]
        if g["shape"] == "bound":
            if any(isinstance(v, (int, float)) and v != 0 for v in vals):
                filled.append(g["id"])
        elif any(v not in (None, "", {}, []) for v in vals):
            filled.append(g["id"])
    unknown = [k for k in props if k not in idx and props[k] not in (None, "", {}, [])]
    return {"present": True, "dimensions": filled + unknown,
            "usageOnly": not filled and not unknown and bool(props.get(_PRESERVED))}


def _write_body(new_props: dict, stored: Optional[dict], body_class: str, props_class: str) -> dict:
    """A full-replace request body: the given dimensions plus the stored readings."""
    props = {"class": props_class, **new_props}
    if stored and stored.get(_PRESERVED):
        props[_PRESERVED] = stored[_PRESERVED]
    body = {"class": body_class, "properties": props}
    if body_class == "UpdateClassificationRequestBody":
        body["mergeUpdate"] = False
    return body


def _scope_of(element: dict) -> Optional[dict]:
    """The DataScope classification's properties from an element header, or None."""
    hdr = (element or {}).get("elementHeader") or {}
    for val in hdr.values():
        for v in (val if isinstance(val, list) else [val]):
            if isinstance(v, dict) and v.get("class") == "ElementClassification" and \
                    (v.get("classificationName") or (v.get("type") or {}).get("typeName")) == "DataScope":
                return {k: p for k, p in (v.get("classificationProperties") or {}).items()
                        if k not in ("class", "typeName")}
    return None


# ── Clients and type definitions ──────────────────────────────────────────────

def _client_kwargs() -> dict:
    from resource_browser_handler import _client_kwargs as kw
    return kw()


async def _explorer_async():
    from pyegeria import ClassificationExplorer
    client = ClassificationExplorer(**_client_kwargs())
    await async_apply_token(client)
    return client


async def _type_groups(type_name: str) -> tuple:
    """(groups, as_of) for DataScope or DataLens, from Egeria's type definition, cached."""
    hit = _typedef_cache.get(type_name)
    if hit and time.time() - hit[1] < _TYPEDEF_TTL:
        return hit[0], hit[1]
    from pyegeria.omvs.valid_metadata import ValidMetadataManager
    client = ValidMetadataManager(**_client_kwargs())
    await async_apply_token(client)
    td = await client._async_get_typedef_by_name(type_name)
    td = td.get("typeDef", td) if isinstance(td, dict) else {}
    groups = _dimensions(td.get("attributeDefinitions") or td.get("propertiesDefinition") or [])
    if not groups:
        raise HTTPException(status_code=502, detail=f"Egeria returned no attributes for the {type_name} type.")
    stamp = time.time()
    _typedef_cache[type_name] = (groups, stamp)
    return groups, stamp


def _require_signed_in() -> str:
    user = _token_user()
    if not user:
        raise HTTPException(status_code=401, detail="Sign in (or choose a persona) to change a data scope: "
                                                    "changes are recorded under your own Egeria user.")
    return user


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


async def _read_scope(client, guid: str) -> Optional[dict]:
    el = await client._async_get_element_by_guid(guid, graph_query_depth=0, output_format="JSON")
    if not isinstance(el, dict):
        raise HTTPException(status_code=404, detail="No element with this identifier is visible to you. It may "
                                                    "not exist, or zone security may hide it from your user.")
    return _scope_of(el), el


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/data-scope/dimensions", summary="The dimensions of DataScope or DataLens, from Egeria's type definition")
async def get_dimensions(type: str = Query("DataScope", description="DataScope or DataLens")):
    if type not in _SCOPE_TYPES:
        raise HTTPException(status_code=400, detail="type is DataScope or DataLens.")
    try:
        groups, stamp = await _type_groups(type)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"data-scope: type definition for {type} failed")
    return JSONResponse({"type": type, "groups": groups,
                         "asOf": datetime.fromtimestamp(stamp, timezone.utc).isoformat(timespec="seconds"),
                         "source": "ValidMetadataManager.get_typedef_by_name"})


def _scope_response(guid: str, el: dict, props: Optional[dict], groups: list, source: str, **extra) -> JSONResponse:
    versions = ((el or {}).get("elementHeader") or {}).get("versions") or {}
    return JSONResponse({"guid": guid, "scope": props, "summary": _summary(props, groups),
                         "updatedBy": versions.get("updatedBy") or versions.get("createdBy") or "",
                         "updateTime": versions.get("updateTime") or versions.get("createTime") or "",
                         "asOf": _now_iso(), "source": source, **extra})


@router.get("/api/data-scope/{guid}", summary="An element's DataScope classification, or none")
async def get_scope(guid: str):
    try:
        client = await _explorer_async()
        props, el = await _read_scope(client, guid)
        groups, _ = await _type_groups("DataScope")
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"data-scope: read for {guid} failed")
    return _scope_response(guid, el, props, groups, "ClassificationExplorer.get_element_by_guid")


class ScopeBody(BaseModel):
    values: dict


@router.put("/api/data-scope/{guid}", summary="Set or change an element's DataScope")
async def put_scope(guid: str, body: ScopeBody):
    _require_signed_in()
    try:
        groups, _ = await _type_groups("DataScope")
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, "data-scope: type definition for DataScope failed")
    props, problems = _clean_values(body.values, groups)
    if problems:
        raise HTTPException(status_code=422, detail="; ".join(problems))
    try:
        client = await _explorer_async()
        stored, _el = await _read_scope(client, guid)
        if not props:
            # Every field emptied: the person means "no data scope" (2026-11-17, the owner emptied
            # the fields and pressed Save to clear one). Clear it, keeping any lineage readings.
            if stored is None:
                raise HTTPException(status_code=422, detail="Give at least one dimension to set a data scope.")
            action = await _clear(client, guid, stored)
            after, el = await _read_scope(client, guid)
            logger.info(f"data-scope: {action} (all fields emptied) on {guid} by {_token_user()}")
            return _scope_response(guid, el, after, groups, "ClassificationExplorer.update_data_scope / clear_data_scope",
                                   action=action)
        if stored is None:
            await client._async_add_data_scope(guid, _write_body(props, None, "NewClassificationRequestBody",
                                                                 "DataScopeProperties"))
            action = "added"
        else:
            await client._async_update_data_scope(guid, _write_body(props, stored, "UpdateClassificationRequestBody",
                                                                    "DataScopeProperties"))
            action = "changed"
        after, el = await _read_scope(client, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"data-scope: write for {guid} failed")
    logger.info(f"data-scope: {action} on {guid} by {_token_user()}")
    return _scope_response(guid, el, after, groups, f"ClassificationExplorer.{'add' if action == 'added' else 'update'}_data_scope",
                           action=action)


async def _clear(client, guid: str, stored: dict) -> str:
    """Remove the dimensions of a stored DataScope. With lineage readings in
    additionalProperties the classification stays holding only them; without, it goes."""
    if stored.get(_PRESERVED):
        await client._async_update_data_scope(guid, _write_body({}, stored, "UpdateClassificationRequestBody",
                                                                "DataScopeProperties"))
        return "cleared-kept-readings"
    await client._async_clear_data_scope(guid)
    return "removed"


@router.delete("/api/data-scope/{guid}", summary="Clear an element's data scope (keeping lineage readings)")
async def delete_scope(guid: str):
    _require_signed_in()
    try:
        groups, _ = await _type_groups("DataScope")
        client = await _explorer_async()
        stored, el = await _read_scope(client, guid)
        if stored is None:
            return _scope_response(guid, el, None, groups, "nothing to clear", action="none")
        action = await _clear(client, guid, stored)
        after, el = await _read_scope(client, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"data-scope: clear for {guid} failed")
    logger.info(f"data-scope: {action} on {guid} by {_token_user()}")
    return _scope_response(guid, el, after, groups, "ClassificationExplorer.update_data_scope / clear_data_scope",
                           action=action)
