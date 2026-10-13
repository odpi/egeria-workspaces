"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Browser — FastAPI router (phase 1: the Resource page).

A shop-for-data app for people who look for data rather than curate it.
Reads Egeria only, and writes back only what Egeria already models
(descriptions, informal tags, notes). Spec:
trellis/packages/resource-explorer/docs/design-notes/SPEC-RESOURCE-BROWSER-PORTAL-APP.md

Endpoints:
  GET    /resource-browser                                   → serve the SPA
  GET    /api/resource-browser/find?q=                       → interim lookup (phase 2 replaces it with search)
  GET    /api/resource-browser/resource/{guid}               → header, flavour, scope, columns, lineage, related
  GET    /api/resource-browser/resource/{guid}/statistics    → latest survey measurements (tables)
  PUT    /api/resource-browser/resource/{guid}/description   → update the description (any element, incl. a column)
  GET    /api/resource-browser/resource/{guid}/tags          → informal tags on the element
  POST   /api/resource-browser/resource/{guid}/tags          → attach a tag by name (created if new)
  DELETE /api/resource-browser/resource/{guid}/tags/{tag}    → detach a tag
  GET    /api/resource-browser/resource/{guid}/notes         → notes from the element's note logs
  POST   /api/resource-browser/resource/{guid}/notes         → add a note (creates the note log if needed)

Honesty rules (spec §2): every response carries `asOf` and `source`; "never
measured" is reported as such, not as zero; a 404 says the element may be hidden
by zone security rather than claiming it does not exist.

Authorship: writes require an X-Egeria-Token, so the signed-in user is the author.
Without one (local mode with no persona, or a deployment that runs Egeria calls
under the server's own identity) writes are refused with 401 rather than made as
a service account.
"""

import asyncio
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import async_apply_token, token_user as _token_user
from egeria_error_mapping import raise_egeria_http_error

router = APIRouter(tags=["resource-browser"])

_HERE = Path(__file__).parent
_HTML = _HERE / "resource-browser.html"

# Relationships left out of the Resource page graph query: survey annotations are
# read by the statistics endpoint (a surveyed database carries ~1000 of them,
# a 4.6 MB payload), and engine-action targets mean nothing to a data shopper.
_SKIP_RELATIONSHIPS = ["AssociatedAnnotation", "ActionTarget"]

# Relationship types shown as lineage, one level each way.
_LINEAGE_RELATIONSHIPS = {
    "DataFlow", "ControlFlow", "ProcessCall", "LineageMapping", "DataMapping",
    "UltimateSource", "UltimateDestination",
}

# Feedback the page shows in its own sections (likes, ratings, comments, tags, notes),
# so it is left out of the generic "where it fits" relationship lists.
_FEEDBACK_TYPES = {"Like", "Rating", "Comment", "InformalTag", "NoteLog"}

# Classifications that are infrastructure, never shown.
_SKIP_CLASSIFICATIONS = {"Anchors", "LatestChange", "Memento", "TemplateSubstitute"}

# The interim lookup's scope: assets, plus the schema elements people treat as
# resources (in Egeria 6.2 a RelationalTable is a SchemaAttribute, not an Asset).
_FIND_TYPES = ["Asset", "RelationalTable", "TabularSchemaType", "DigitalProduct"]

_TABLE_STATS_QN = "Annotation::Capture Database Table Measurements::"
_COLUMN_STATS_QN = "Annotation::Capture Database Column Measurements::"
_STATS_PAGE = 100
_STATS_MAX_PAGES = 10


# ── Clients ───────────────────────────────────────────────────────────────────

def _client_kwargs() -> dict:
    return dict(
        view_server=os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
        platform_url=os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
        user_id=os.environ.get("EGERIA_USER", "erinoverview"),
        user_pwd=os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


async def _explorer_async():
    from pyegeria import ClassificationExplorer
    client = ClassificationExplorer(**_client_kwargs())
    await async_apply_token(client)
    return client


async def _expert_async():
    from pyegeria.omvs.metadata_expert import MetadataExpert
    client = MetadataExpert(**_client_kwargs())
    await async_apply_token(client)
    return client


def _require_signed_in() -> str:
    user = _token_user()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Sign in (or choose a persona) to make changes: edits are recorded under your own Egeria user, never a shared account.",
        )
    return user


_NOT_VISIBLE = ("No resource with this identifier is visible to you. It may not exist, "
                "or zone security may hide it from your user.")


def _raise_not_visible_or_mapped(exc: Exception, log_msg: str) -> None:
    """Like raise_egeria_http_error, but a 404 says the element may be hidden by
    zones: Egeria answers the same way for "absent" and "not visible to you"."""
    try:
        raise_egeria_http_error(exc, log_msg)
    except HTTPException as http:
        if http.status_code == 404:
            raise HTTPException(status_code=404, detail=_NOT_VISIBLE)
        raise


# ── Pure helpers (unit-tested in tests/test_resource_browser.py) ──────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _elements(result) -> list:
    """pyegeria returns a list, a single dict, or the string "No elements found"."""
    if isinstance(result, list):
        return [e for e in result if isinstance(e, dict)]
    if isinstance(result, dict) and result.get("elementHeader"):
        return [result]
    return []


def _type_names(header: dict) -> tuple:
    t = (header or {}).get("type") or {}
    return t.get("typeName", ""), list(t.get("superTypeNames") or [])


def _display_name(props: dict, fallback: str = "") -> str:
    props = props or {}
    return (props.get("displayName") or props.get("name") or props.get("resourceName")
            or props.get("qualifiedName") or fallback)


def _related(item: dict) -> Optional[dict]:
    """One RelatedMetadataElementSummary → a flat related-element record."""
    if not isinstance(item, dict):
        return None
    elem = item.get("relatedElement")
    if not isinstance(elem, dict):
        return None
    hdr = elem.get("elementHeader") or {}
    guid = hdr.get("guid")
    if not guid:
        return None
    props = elem.get("properties") or {}
    type_name, supers = _type_names(hdr)
    return {
        "guid": guid,
        "typeName": type_name,
        "superTypeNames": supers,
        "displayName": _display_name(props, guid),
        "qualifiedName": props.get("qualifiedName", ""),
        "description": props.get("description", ""),
        "relationshipType": ((item.get("relationshipHeader") or {}).get("type") or {}).get("typeName", ""),
        "atEnd1": bool(item.get("relatedElementAtEnd1")),
        "relationshipProperties": {k: v for k, v in (item.get("relationshipProperties") or {}).items()
                                   if k not in ("class", "typeName")},
        "properties": props,
        "elementHeader": hdr,
    }


def _classifications(header: dict) -> list:
    """Classifications from an element header: each is a header key whose value
    (or list of values) has class ElementClassification."""
    out = []
    for key, val in (header or {}).items():
        vals = val if isinstance(val, list) else [val]
        for v in vals:
            if not isinstance(v, dict) or v.get("class") != "ElementClassification":
                continue
            name = v.get("classificationName") or ((v.get("type") or {}).get("typeName")) or key
            if name in _SKIP_CLASSIFICATIONS:
                continue
            props = {k: p for k, p in (v.get("classificationProperties") or {}).items()
                     if k not in ("class", "typeName") and p not in (None, "", [], {})}
            out.append({"name": name, "properties": props})
    return out


def _data_scope(classifications: list) -> Optional[dict]:
    """The DataScope classification (time and place), or None when absent."""
    for c in classifications:
        if c["name"] == "DataScope":
            return c["properties"]
    return None


def _flavour(type_name: str, super_types: list, collections: list) -> dict:
    """Which of the spec's three flavours a resource is (§3).

    (c) Hub: a member of a DataSharingHub collection.
    (b) Product: is a DigitalProduct, or a member of one.
    (a) Known: anything else Egeria knows about.
    The badge shows the highest by precedence c > b > a; `all` lists every one
    that applies so the page can mention the others. `via` names the collections
    that made it so."""
    def is_type(rec_type, rec_supers, wanted):
        return rec_type == wanted or wanted in (rec_supers or [])

    hubs = [c for c in collections if is_type(c.get("typeName"), c.get("superTypeNames"), "DataSharingHub")]
    products = [c for c in collections if is_type(c.get("typeName"), c.get("superTypeNames"), "DigitalProduct")]
    applies = []
    if hubs:
        applies.append("hub")
    if products or is_type(type_name, super_types, "DigitalProduct"):
        applies.append("product")
    applies.append("known")
    return {
        "flavour": applies[0],
        "all": applies,
        "via": {
            "hub": [{"guid": c["guid"], "displayName": c["displayName"]} for c in hubs],
            "product": [{"guid": c["guid"], "displayName": c["displayName"]} for c in products],
        },
    }


def _owner(classifications: list) -> Optional[str]:
    for c in classifications:
        if c["name"] == "Ownership":
            return c["properties"].get("owner") or None
    return None


def _column(rel: dict) -> dict:
    props = rel["properties"]
    hdr = rel["elementHeader"]
    versions = hdr.get("versions") or {}
    cls = _classifications(hdr)
    return {
        "guid": rel["guid"],
        "name": _display_name(props, rel["guid"]),
        "typeName": rel["typeName"],
        "dataType": props.get("dataType") or "",
        "description": props.get("description") or "",
        "position": rel["relationshipProperties"].get("position", props.get("position")),
        "keyMarks": [c["name"] for c in cls if c["name"] in ("PrimaryKey", "ForeignKey")],
        "dataClass": None,
        "classifications": [c for c in cls if c["name"] not in ("PrimaryKey", "ForeignKey")],
        "createTime": versions.get("createTime") or "",
        "updatedBy": versions.get("updatedBy") or "",
        "updateTime": versions.get("updateTime") or "",
    }


def _lineage(rels: list) -> dict:
    """Split lineage relationships into upstream/downstream for one level.

    For a flow relationship end1 is the source and end2 the target, so a related
    element at end1 is upstream of this one."""
    up, down = [], []
    for r in rels:
        if r["relationshipType"] not in _LINEAGE_RELATIONSHIPS:
            continue
        rec = {k: r[k] for k in ("guid", "typeName", "displayName", "relationshipType")}
        (up if r["atEnd1"] else down).append(rec)
    return {"upstream": up, "downstream": down}


def _stats_name_of(qualified_name: str, prefix: str) -> str:
    """'Annotation::Capture …::coco.schema.table.col::<uuid>' → 'coco.schema.table.col'."""
    rest = qualified_name[len(prefix):] if qualified_name.startswith(prefix) else qualified_name
    return rest.split("::", 1)[0]


def _latest_by_subject(annotations: list, prefix: str) -> dict:
    """Keep the newest annotation per measured subject name."""
    latest = {}
    for a in annotations:
        props = a.get("properties") or {}
        name = _stats_name_of(props.get("qualifiedName", ""), prefix)
        when = ((a.get("elementHeader") or {}).get("versions") or {}).get("createTime") or ""
        if name and (name not in latest or when > latest[name]["measuredAt"]):
            latest[name] = {
                "measuredAt": when,
                "annotationType": props.get("annotationType", ""),
                "values": props.get("resourceProperties") or {},
                "guid": (a.get("elementHeader") or {}).get("guid", ""),
            }
    return latest


def _jdbc_table_name(props: dict) -> Optional[str]:
    """catalog.schema.table for a JDBC-catalogued table, from its additionalProperties."""
    ap = (props or {}).get("additionalProperties") or {}
    parts = [ap.get("jdbc.catalog"), ap.get("jdbc.schema"), ap.get("jdbc.table")]
    return ".".join(parts) if all(parts) else None


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/resource-browser", include_in_schema=False)
async def serve_resource_browser():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Resource Browser page not found")
    return FileResponse(str(_HTML), media_type="text/html")


@router.get("/api/resource-browser/find", summary="Interim lookup by name (phase 2 replaces this with search)")
async def find_resources(q: str = Query(..., min_length=1), page_size: int = Query(25, ge=1, le=100)):
    try:
        client = await _explorer_async()
        raw = await client._async_find_elements_by_property_value(
            property_value=q, property_names=["displayName", "name", "qualifiedName", "description"],
            metadata_element_subtypes=_FIND_TYPES, starts_with=False, ends_with=False, ignore_case=True,
            graph_query_depth=0, output_format="JSON", page_size=page_size,
        )
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: find {q!r} failed")
    items = []
    for e in _elements(raw):
        hdr = e.get("elementHeader") or {}
        if any(c["name"] == "Template" for c in _classifications(hdr)):
            continue
        props = e.get("properties") or {}
        type_name, _ = _type_names(hdr)
        items.append({
            "guid": hdr.get("guid", ""), "typeName": type_name,
            "displayName": _display_name(props, hdr.get("guid", "")),
            "qualifiedName": props.get("qualifiedName", ""),
            "description": props.get("description", ""),
        })
    return JSONResponse({
        "items": items, "asOf": _now_iso(), "source": "ClassificationExplorer.find_elements_by_property_value",
        "mayHaveMore": len(items) == page_size,
    })


@router.get("/api/resource-browser/resource/{guid}", summary="Everything the Resource page shows, in one call")
async def get_resource(guid: str):
    try:
        client = await _explorer_async()
        el = await client._async_get_element_by_guid(
            guid, graph_query_depth=1, output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1, "skipRelationships": _SKIP_RELATIONSHIPS},
        )
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: get_element_by_guid({guid}) failed")
    if not isinstance(el, dict) or not el.get("elementHeader"):
        raise HTTPException(status_code=404, detail=_NOT_VISIBLE)

    hdr = el["elementHeader"]
    props = el.get("properties") or {}
    versions = hdr.get("versions") or {}
    type_name, supers = _type_names(hdr)
    classifications = _classifications(hdr)

    related = {}
    for key, val in el.items():
        if isinstance(val, list):
            recs = [r for r in (_related(i) for i in val) if r]
            if recs:
                related[key] = recs
    all_rels = [r for recs in related.values() for r in recs]

    collections = related.get("memberOfCollections", [])
    columns = sorted((_column(r) for r in related.get("schemaAttributes", [])),
                     key=lambda c: (c["position"] is None, c["position"] or 0, c["name"]))
    reports = sorted(
        ({"guid": r["guid"], "displayName": r["displayName"],
          "createTime": (r["elementHeader"].get("versions") or {}).get("createTime", "")}
         for r in related.get("reports", [])),
        key=lambda r: r["createTime"], reverse=True)

    anchor = (hdr.get("anchor") or {}).get("classificationProperties") or {}
    anchor_guid = anchor.get("anchorGUID")
    parent = None
    if anchor_guid and anchor_guid != guid:
        parent = {"guid": anchor_guid, "typeName": anchor.get("anchorTypeName", ""), "displayName": ""}
        try:
            anchor_el = await client._async_get_element_by_guid(anchor_guid, graph_query_depth=0, output_format="JSON")
            a_hdr = (anchor_el or {}).get("elementHeader") or {}
            parent["typeName"] = _type_names(a_hdr)[0] or parent["typeName"]
            parent["displayName"] = _display_name((anchor_el or {}).get("properties"), anchor_guid)
        except Exception as exc:  # the page still works without the parent's name
            logger.debug(f"resource-browser: anchor {anchor_guid} not readable: {exc}")

    # Everything else, minus the keys the page already shows in its own sections.
    shown = {"memberOfCollections", "schemaAttributes", "reports", "searchKeywords"}
    other = {}
    for key, recs in related.items():
        if key in shown:
            continue
        rest = [{k: r[k] for k in ("guid", "typeName", "displayName", "relationshipType", "atEnd1")}
                for r in recs if r["relationshipType"] not in _LINEAGE_RELATIONSHIPS
                and r["typeName"] not in _FEEDBACK_TYPES]
        if rest:
            other[key] = rest

    plain_props = {k: v for k, v in props.items()
                   if k not in ("class", "typeName", "displayName", "name", "description", "qualifiedName",
                                "additionalProperties", "extendedProperties")
                   and v not in (None, "", [], {}) and not isinstance(v, (dict, list))}

    return JSONResponse({
        "guid": guid,
        "typeName": type_name,
        "superTypeNames": supers,
        "displayName": _display_name(props, guid),
        "qualifiedName": props.get("qualifiedName", ""),
        "description": props.get("description") or "",
        "properties": plain_props,
        "additionalProperties": props.get("additionalProperties") or {},
        "createdBy": versions.get("createdBy") or "",
        "createTime": versions.get("createTime") or "",
        "updatedBy": versions.get("updatedBy") or "",
        "updateTime": versions.get("updateTime") or "",
        "status": hdr.get("status", ""),
        "classifications": [c for c in classifications if c["name"] not in ("DataScope", "Ownership")],
        "dataScope": _data_scope(classifications),
        "owner": _owner(classifications),
        "flavour": _flavour(type_name, supers, collections),
        "collections": [{k: c[k] for k in ("guid", "typeName", "displayName")} for c in collections],
        "parent": parent,
        # A columns section for things that have columns: any element with schema
        # attributes, or a relational table that has none recorded yet.
        "columns": columns if (columns or type_name == "RelationalTable") else None,
        "lineage": _lineage(all_rels),
        "surveyReports": reports,
        "keywords": [r["displayName"] for r in related.get("searchKeywords", [])],
        "related": other,
        "jdbcTableName": _jdbc_table_name(props),
        "me": _token_user(),
        "canWrite": _token_user() is not None,
        "asOf": _now_iso(),
        "source": "ClassificationExplorer.get_element_by_guid (graph depth 1)",
    })


async def _find_all_annotations(client, prefix: str) -> tuple:
    """All ResourceMeasureAnnotations whose qualifiedName starts with `prefix`.

    Pages until an empty page (only an empty page means the end); returns
    (annotations, capped) where capped means the page limit stopped the read."""
    found = []
    for page in range(_STATS_MAX_PAGES):
        raw = await client._async_find_assets(
            search_string=prefix, starts_with=True, ignore_case=False,
            metadata_element_type_name="ResourceMeasureAnnotation",
            graph_query_depth=0, output_format="JSON",
            start_from=page * _STATS_PAGE, page_size=_STATS_PAGE,
        )
        batch = _elements(raw)
        if not batch:
            return found, False
        found.extend(batch)
    return found, True


@router.get("/api/resource-browser/resource/{guid}/statistics",
            summary="Latest survey measurements for a JDBC-catalogued table and its columns")
async def get_statistics(guid: str):
    try:
        client = await _explorer_async()
        el = await client._async_get_element_by_guid(guid, graph_query_depth=0, output_format="JSON")
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: statistics lookup for {guid} failed")
    props = (el or {}).get("properties") or {}
    table = _jdbc_table_name(props)
    base = {"asOf": _now_iso(), "source": "ClassificationExplorer.find_assets (ResourceMeasureAnnotation by qualifiedName)"}
    if not table:
        return JSONResponse({**base, "state": "not-applicable", "table": None, "columns": {},
                             "reason": "Statistics are read for database tables catalogued with their catalog, schema and table names."})
    try:
        (table_anns, t_capped), (col_anns, c_capped) = await asyncio.gather(
            _find_all_annotations(client, f"{_TABLE_STATS_QN}{table}::"),
            _find_all_annotations(client, f"{_COLUMN_STATS_QN}{table}."),
        )
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: statistics search for {table} failed")
    table_latest = _latest_by_subject(table_anns, _TABLE_STATS_QN).get(table)
    col_latest = {name[len(table) + 1:]: v for name, v in _latest_by_subject(col_anns, _COLUMN_STATS_QN).items()
                  if name.startswith(table + ".")}
    return JSONResponse({
        **base,
        "state": "measured" if (table_latest or col_latest) else "never",
        "subject": table,
        "table": table_latest,
        "columns": col_latest,
        "capped": t_capped or c_capped,
    })


class DescriptionBody(BaseModel):
    description: str


@router.put("/api/resource-browser/resource/{guid}/description", summary="Update an element's description")
async def update_description(guid: str, body: DescriptionBody):
    _require_signed_in()
    try:
        expert = await _expert_async()
        await expert._async_update_metadata_element_properties(guid, {
            "class": "UpdatePropertiesRequestBody",
            "properties": {
                "class": "ElementProperties",
                "propertyValueMap": {
                    "description": {"class": "PrimitiveTypePropertyValue", "typeName": "string",
                                    "primitiveValue": body.description},
                },
            },
            "replaceProperties": False,
        })
        client = await _explorer_async()
        el = await client._async_get_element_by_guid(guid, graph_query_depth=0, output_format="JSON")
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: description update for {guid} failed")
    versions = ((el or {}).get("elementHeader") or {}).get("versions") or {}
    return JSONResponse({
        "guid": guid,
        "description": ((el or {}).get("properties") or {}).get("description") or "",
        "updatedBy": versions.get("updatedBy") or "",
        "updateTime": versions.get("updateTime") or "",
        "asOf": _now_iso(), "source": "MetadataExpert.update_metadata_element_properties",
    })


def _tag_record(e: dict) -> dict:
    hdr = e.get("elementHeader") or {}
    props = e.get("properties") or {}
    return {
        "guid": hdr.get("guid", ""),
        "name": props.get("displayName") or props.get("name") or "",
        "description": props.get("description") or "",
        "createdBy": (hdr.get("versions") or {}).get("createdBy") or "",
    }


@router.get("/api/resource-browser/resource/{guid}/tags", summary="Informal tags attached to an element")
async def get_tags(guid: str):
    try:
        client = await _explorer_async()
        raw = await client._async_get_attached_tags(guid, graph_query_depth=0, output_format="JSON")
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: get_attached_tags({guid}) failed")
    return JSONResponse({"tags": [_tag_record(e) for e in _elements(raw)], "me": _token_user(),
                         "asOf": _now_iso(), "source": "ClassificationExplorer.get_attached_tags"})


class TagBody(BaseModel):
    name: str


_TAG_NAME = re.compile(r"^[\w][\w .\-/]{0,62}$")


@router.post("/api/resource-browser/resource/{guid}/tags", summary="Attach an informal tag by name, creating it if new")
async def add_tag(guid: str, body: TagBody):
    _require_signed_in()
    name = body.name.strip()
    if not _TAG_NAME.match(name):
        raise HTTPException(status_code=400, detail="A tag is 1–63 letters, digits, spaces, dots, dashes or slashes.")
    try:
        client = await _explorer_async()
        existing = [_tag_record(e) for e in _elements(await client._async_find_tags(
            search_string=name, starts_with=True, ends_with=True, ignore_case=True, output_format="JSON"))]
        match = next((t for t in existing if t["name"].lower() == name.lower()), None)
        tag_guid = match["guid"] if match else await client._async_create_informal_tag(display_name=name)
        await client._async_add_tag_to_element(guid, tag_guid, is_public=True)
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: add tag {name!r} to {guid} failed")
    return await get_tags(guid)


@router.delete("/api/resource-browser/resource/{guid}/tags/{tag_guid}", summary="Detach an informal tag")
async def remove_tag(guid: str, tag_guid: str):
    _require_signed_in()
    try:
        client = await _explorer_async()
        await client._async_remove_tag_from_element(guid, tag_guid)
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: remove tag {tag_guid} from {guid} failed")
    return await get_tags(guid)


_NOTES_CAP = 100


def _note_record(e: dict) -> dict:
    hdr = e.get("elementHeader") or {}
    props = e.get("properties") or {}
    versions = hdr.get("versions") or {}
    return {
        "guid": hdr.get("guid", ""),
        "title": props.get("displayName") or "",
        "text": props.get("description") or props.get("text") or "",
        "createdBy": versions.get("createdBy") or "",
        "createTime": versions.get("createTime") or "",
    }


@router.get("/api/resource-browser/resource/{guid}/notes", summary="Notes from the element's note logs")
async def get_notes(guid: str):
    try:
        client = await _explorer_async()
        logs = _elements(await client._async_get_attached_note_logs(guid, graph_query_depth=0, output_format="JSON"))
        notes, capped = [], False
        for log in logs:
            raw = await client._async_get_notes_for_note_log(
                (log.get("elementHeader") or {}).get("guid"), output_format="JSON", page_size=_NOTES_CAP)
            batch = _elements(raw)
            capped = capped or len(batch) >= _NOTES_CAP
            notes.extend(_note_record(n) for n in batch)
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: notes for {guid} failed")
    notes.sort(key=lambda n: n["createTime"], reverse=True)
    return JSONResponse({
        "notes": notes, "noteLogs": len(logs), "capped": capped,
        "asOf": _now_iso(), "source": "ClassificationExplorer.get_attached_note_logs + get_notes_for_note_log",
    })


class NoteBody(BaseModel):
    text: str
    title: Optional[str] = None


@router.post("/api/resource-browser/resource/{guid}/notes", summary="Add a note, creating the element's note log if needed")
async def add_note(guid: str, body: NoteBody):
    user = _require_signed_in()
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="A note needs some text.")
    try:
        client = await _explorer_async()
        logs = _elements(await client._async_get_attached_note_logs(guid, graph_query_depth=0, output_format="JSON"))
        if logs:
            log_guid = logs[0]["elementHeader"]["guid"]
        else:
            log_guid = await client._async_create_note_log(
                element_guid=guid, display_name="Notes",
                description="Notes added from the Resource Browser beside the official description.")
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        await client._async_create_note(
            log_guid, display_name=(body.title or f"Note by {user}, {stamp}")[:120], description=text)
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: add note to {guid} failed")
    return await get_notes(guid)
