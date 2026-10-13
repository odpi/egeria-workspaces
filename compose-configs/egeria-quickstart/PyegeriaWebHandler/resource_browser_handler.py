"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Browser — FastAPI router (phase 1: the Resource page; phase 2: search, Home, Browse).

A shop-for-data app for people who look for data rather than curate it.
Reads Egeria only, and writes back only what Egeria already models
(descriptions, informal tags, notes). Spec:
trellis/packages/resource-explorer/docs/design-notes/SPEC-RESOURCE-BROWSER-PORTAL-APP.md

Endpoints:
  GET    /resource-browser                                   → serve the SPA
  GET    /api/resource-browser/resource/{guid}               → header, flavour, scope, columns, lineage, related
  GET    /api/resource-browser/resource/{guid}/statistics    → latest survey measurements (tables)
  PUT    /api/resource-browser/resource/{guid}/description   → update the description (any element, incl. a column)
  GET    /api/resource-browser/resource/{guid}/tags          → informal tags on the element
  POST   /api/resource-browser/resource/{guid}/tags          → attach a tag by name (created if new)
  DELETE /api/resource-browser/resource/{guid}/tags/{tag}    → detach a tag
  GET    /api/resource-browser/resource/{guid}/notes         → notes from the element's note logs
  POST   /api/resource-browser/resource/{guid}/notes         → add a note (creates the note log if needed)
  GET    /api/resource-browser/search?q=&kind=&page=         → L0 search: text, columns, tags, keywords, owners
  GET    /api/resource-browser/flavours                      → which resources are product or hub members (cached)
  GET    /api/resource-browser/row-extras?guids=             → tags, likes and rating summary for visible rows
  GET    /api/resource-browser/home                          → recently changed resources; popularity status
  GET    /api/resource-browser/lists                         → work lists the user can see (read-only until phase 3)
  GET    /api/resource-browser/browse/{facet}                → the values of one browse facet
  GET    /api/resource-browser/browse/{facet}/{value}        → the resources under one facet value

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

from egeria_auth import async_apply_token, lineage_key as _lineage_key, token_user as _token_user
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


# ══ Phase 2: search, Home, Browse ════════════════════════════════════════════
#
# L0 search (spec §6): Egeria's own find, ordered by text relevance, with the
# source and as-of on every response so a later layer can replace it unseen.
# Egeria cannot sort by use or count facets, so neither is attempted here.

# Search and browse scope: data resources. "Asset" alone would bring in ~8,600
# Notifications and ~700 EngineActions, which mean nothing to a data shopper.
_RESOURCE_TYPES = ["DataAsset", "RelationalTable", "DigitalProduct", "DeployedAPI"]

# DataAsset subtypes that are operational records rather than data to shop for.
_NOT_RESOURCES = {"SurveyReport", "ConnectorActivityReport", "SecretsCollection", "MetadataCollection",
                  "KeyStoreFile"}

# Resource kinds, in matching order (the first whose types the element has wins).
_KINDS = [
    ("table", "Tables", ["RelationalTable", "VirtualRelationalTable"]),
    ("schema", "Schemas", ["DeployedDatabaseSchema"]),
    ("database", "Databases", ["Database"]),
    ("report", "Reports", ["Report"]),
    ("dataset", "Data sets", ["TabularDataSet", "TabularDataSetCollection", "DataSet"]),
    ("file", "Files and folders", ["DataFile", "DataFolder", "FileFolder", "DataFileCollection"]),
    ("topic", "Topics and feeds", ["Topic", "DataFeed"]),
    ("product", "Products", ["DigitalProduct"]),
    ("api", "APIs", ["DeployedAPI"]),
]
_KIND_IDS = [k[0] for k in _KINDS] + ["other"]

# Governance classifications shown as badges.
_BADGES = ["Confidentiality", "Confidence", "Criticality", "Impact", "Retention", "SecurityTags"]

_SEARCH_PROPS = ["displayName", "name", "qualifiedName", "description"]
_SEARCH_PAGE = 50
_COLUMN_ROLLUP_CAP = 25      # columns per page whose table is looked up
_TAG_MATCH_CAP = 5           # tags (and keywords) per query whose elements are read
_LOOKUP_CONCURRENCY = 4      # parallel per-element calls; Egeria's JDBC pool is 10 connections
_ROW_EXTRAS_CAP = 25
_RECENT_PAGE = 50
_RECENT_SHOWN = 25
_CACHE_TTL = 600             # seconds; the page shows the age

_ORDER_NOTE = ("Ordered by text relevance: name matches first, then qualified name, description, "
               "tag, keyword, owner and column matches. Egeria holds no usage measure yet, "
               "so nothing is ranked by use.")


def _kind_of(type_name: str, super_types: list) -> str:
    names = [type_name] + list(super_types or [])
    for kind, _label, types in _KINDS:
        if any(t in names for t in types):
            return kind
    return "other"


def _is_resource(type_name: str, super_types: list) -> bool:
    if type_name in _NOT_RESOURCES:
        return False
    names = [type_name] + list(super_types or [])
    return any(t in names for t in _RESOURCE_TYPES)


def _looks_automated(user) -> bool:
    """Egeria's own service accounts end in "npa" (non-person account) or are engines."""
    u = str(user or "").lower()
    return u.endswith("npa") or "engine" in u


def _row(el: dict) -> Optional[dict]:
    """One result row, from an element (or a related element) at graph depth 0.

    None for anything that is not a data resource, and for templates."""
    if not isinstance(el, dict):
        return None
    hdr = el.get("elementHeader") or {}
    guid = hdr.get("guid")
    type_name, supers = _type_names(hdr)
    if not guid or not _is_resource(type_name, supers):
        return None
    cls = _classifications(hdr)
    if any(c["name"] == "Template" for c in cls):
        return None
    props = el.get("properties") or {}
    versions = hdr.get("versions") or {}
    desc = props.get("description") or ""
    return {
        "guid": guid,
        "typeName": type_name,
        "kind": _kind_of(type_name, supers),
        "displayName": _display_name(props, guid),
        "qualifiedName": props.get("qualifiedName", ""),
        "description": desc if len(desc) <= 400 else desc[:397] + "…",
        "owner": _owner(cls),
        "badges": [c["name"] for c in cls if c["name"] in _BADGES],
        "dataScope": _data_scope(cls),
        "updatedBy": versions.get("updatedBy") or versions.get("createdBy") or "",
        "updateTime": versions.get("updateTime") or versions.get("createTime") or "",
        "automated": _looks_automated(versions.get("updatedBy") or versions.get("createdBy")),
        "matched": [],
    }


def _rows(elements: list) -> tuple:
    """(rows, not_shown): rows for the data resources, and how many elements were not."""
    rows, skipped = [], 0
    for e in elements:
        r = _row(e)
        if r:
            rows.append(r)
        else:
            skipped += 1
    return rows, skipped


def _relevance(row: dict, q: str) -> tuple:
    """Sort key: how directly the row's own text matches the query, then its name."""
    ql = q.lower()
    name = row["displayName"].lower()
    if name == ql:
        rank = 0
    elif name.startswith(ql):
        rank = 1
    elif ql in name:
        rank = 2
    elif ql in row["qualifiedName"].lower():
        rank = 3
    elif ql in row["description"].lower():
        rank = 4
    else:
        rank = 5
    return rank, name


def _text_reason(row: dict, q: str) -> str:
    """Which of the row's own fields the text search matched, for the "matched:" line."""
    ql = q.lower()
    if ql in row["displayName"].lower():
        return "name"
    if ql in row["qualifiedName"].lower():
        return "qualified name"
    if ql in row["description"].lower():
        return "description"
    return "name or description"


def _merge(into: dict, rows: list, reason: str) -> None:
    """Add rows to a guid-keyed result map, recording why each matched."""
    for r in rows:
        have = into.get(r["guid"])
        if have is None:
            r = dict(r, matched=[reason])
            into[r["guid"]] = r
        elif reason not in have["matched"]:
            have["matched"].append(reason)


def _flavour_index(products: list, hubs: Optional[list]) -> dict:
    """Map member guid → the products and hubs that hold it, from collections read
    with their CollectionMembership relationships. Collections are themselves listed:
    a DigitalProduct is a product."""
    def index(collections):
        members = {}
        for c in collections or []:
            hdr = c.get("elementHeader") or {}
            ref = {"guid": hdr.get("guid", ""), "displayName": _display_name(c.get("properties"), hdr.get("guid", ""))}
            for item in c.get("collectionMembers") or []:
                rel = _related(item)
                if rel:
                    members.setdefault(rel["guid"], []).append(ref)
        return members
    return {
        "product": index(products),
        "productGuids": sorted({(c.get("elementHeader") or {}).get("guid") for c in products
                                if (c.get("elementHeader") or {}).get("guid")}),
        "hub": index(hubs),
        "hubTypeKnown": hubs is not None,
        "productCount": len(products),
        "hubCount": len(hubs or []),
    }


def _feedback_summary(el: dict) -> dict:
    """Tags, likes and rating summary from an element read with its feedback relationships."""
    from egeria_feedback_handler import _star_int
    tags, likes, stars, ratings = [], 0, [], 0
    for key, val in (el or {}).items():
        if not isinstance(val, list):
            continue
        for item in val:
            rel = _related(item)
            if not rel:
                continue
            if rel["relationshipType"] == "AttachedTag":
                tags.append(rel["displayName"])
            elif rel["relationshipType"] == "AttachedLike":
                likes += 1
            elif rel["relationshipType"] == "AttachedRating":
                ratings += 1
                s = _star_int({"properties": rel["properties"]})
                if s:
                    stars.append(s)
    return {"tags": sorted(set(tags)), "likes": likes, "ratings": ratings,
            "rating": round(sum(stars) / len(stars), 1) if stars else None}


# ── Per-process cache (spec §6: in memory, with a visible age) ───────────────

_cache: dict = {}
_cache_locks: dict = {}


async def _cached(name: str, producer, ttl: int = _CACHE_TTL):
    """(value, as_of) for `name`, per signed-in user and lineage mode: zone security
    can show two users different elements, and forLineage changes the results."""
    key = f"{name}|{_token_user() or '-'}{_lineage_key()}"
    now = datetime.now(timezone.utc)
    hit = _cache.get(key)
    if hit and (now - hit[1]).total_seconds() < ttl:
        return hit[0], hit[1]
    lock = _cache_locks.setdefault(key, asyncio.Lock())
    async with lock:
        hit = _cache.get(key)
        if hit and (now - hit[1]).total_seconds() < ttl:
            return hit[0], hit[1]
        value = await producer()
        stamp = datetime.now(timezone.utc)
        _cache[key] = (value, stamp)
        return value, stamp


def _age(stamp: datetime) -> dict:
    return {"asOf": stamp.isoformat(timespec="seconds"),
            "ageSeconds": int((datetime.now(timezone.utc) - stamp).total_seconds())}


def _is_unknown_type(exc: Exception) -> bool:
    s = str(exc)
    return "OMAG-COMMON-400-018" in s or "is not recognized" in s


async def _all_elements(client, type_name: str, body_extra: Optional[dict] = None, depth: int = 0,
                        page: int = 200, max_pages: int = 25) -> tuple:
    """Every element of a type, paged until an empty page. (elements, capped)."""
    out = []
    for p in range(max_pages):
        body = {"class": "ResultsRequestBody", "metadataElementTypeName": type_name, "graphQueryDepth": depth,
                "startFrom": p * page, "pageSize": page, **(body_extra or {})}
        batch = _elements(await client._async_get_elements(
            type_name, start_from=p * page, page_size=page, output_format="JSON", graph_query_depth=depth, body=body))
        if not batch:
            return out, False
        out.extend(batch)
    return out, True


async def _flavours_value():
    client = await _explorer_async()
    only_members = {"includeOnlyRelationships": ["CollectionMembership"]}
    products, p_capped = await _all_elements(client, "DigitalProduct", only_members, depth=1, page=100)
    try:
        hubs, h_capped = await _all_elements(client, "DataSharingHub", only_members, depth=1, page=100)
    except Exception as exc:
        if not _is_unknown_type(exc):
            raise
        hubs, h_capped = None, False
    return {**_flavour_index(products, hubs), "capped": p_capped or h_capped}


@router.get("/api/resource-browser/flavours", summary="Which resources are members of a product or a data sharing hub")
async def get_flavours():
    try:
        value, stamp = await _cached("flavours", _flavours_value)
    except Exception as exc:
        raise_egeria_http_error(exc, "resource-browser: flavour index failed")
    return JSONResponse({**value, **_age(stamp),
                         "source": "ClassificationExplorer.get_elements (DigitalProduct, DataSharingHub; CollectionMembership only)"})


# ── Search ────────────────────────────────────────────────────────────────────

def _kind_types(kind: Optional[str]) -> list:
    for k, _label, types in _KINDS:
        if k == kind:
            return types
    return _RESOURCE_TYPES


async def _search_text(client, q, kind, page):
    raw = await client._async_find_elements_by_property_value(
        property_value=q, property_names=_SEARCH_PROPS, metadata_element_subtypes=_kind_types(kind),
        starts_with=False, ends_with=False, ignore_case=True, graph_query_depth=0, output_format="JSON",
        start_from=page * _SEARCH_PAGE, page_size=_SEARCH_PAGE)
    return _elements(raw)


async def _parent_table(client, sem, column_guid):
    async with sem:
        el = await client._async_get_element_by_guid(
            column_guid, graph_query_depth=1, output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": ["NestedSchemaAttribute"]})
    for item in (el or {}).get("parentSchemaElements") or []:
        if item.get("relatedElementAtEnd1"):
            return item.get("relatedElement")
    return None


async def _search_columns(client, q, page):
    """Column-name matches, rolled up to their tables (spec: children roll up)."""
    raw = await client._async_find_elements_by_property_value(
        property_value=q, property_names=["displayName", "name"], metadata_element_subtypes=["RelationalColumn"],
        starts_with=False, ends_with=False, ignore_case=True, graph_query_depth=0, output_format="JSON",
        start_from=page * _SEARCH_PAGE, page_size=_SEARCH_PAGE)
    cols = _elements(raw)
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)
    looked = cols[:_COLUMN_ROLLUP_CAP]
    parents = await asyncio.gather(*(_parent_table(client, sem, (c.get("elementHeader") or {}).get("guid"))
                                     for c in looked), return_exceptions=True)
    tables = {}
    for col, parent in zip(looked, parents):
        if isinstance(parent, Exception) or not parent:
            continue
        row = _row(parent)
        if not row:
            continue
        t = tables.setdefault(row["guid"], (row, []))
        t[1].append(_display_name(col.get("properties"), ""))
    return {"tables": list(tables.values()), "found": len(cols), "rolledUp": len(looked)}


async def _search_tags(client, q):
    tags = [t for t in _elements(await client._async_find_tags(
        search_string=q, starts_with=False, ends_with=False, ignore_case=True, output_format="JSON"))][:_TAG_MATCH_CAP]
    out = []
    for t in tags:
        tag_guid = (t.get("elementHeader") or {}).get("guid")
        name = _display_name(t.get("properties"), "")
        els = _elements(await client._async_get_elements_by_tag(tag_guid, graph_query_depth=0, output_format="JSON",
                                                                page_size=_SEARCH_PAGE))
        out.append((name, els))
    return out


async def _search_keywords(client, q):
    """Exact keyword matches (a SearchKeyword is one element per attachment)."""
    kws = _elements(await client._async_get_search_keyword_by_keyword(
        q, graph_query_depth=1, output_format="JSON", page_size=_SEARCH_PAGE))
    out = []
    for k in kws:
        for item in k.get("keywordElements") or []:
            if isinstance(item, dict) and item.get("relatedElement"):
                out.append(item["relatedElement"])
    return out


async def _search_owners(client, q):
    return _elements(await client._async_get_elements_by_classification_with_property_value(
        "Ownership", q, ["owner"], starts_with=False, ends_with=False, ignore_case=True,
        graph_query_depth=0, output_format="JSON", page_size=_SEARCH_PAGE))


@router.get("/api/resource-browser/search", summary="L0 search over Egeria's own find")
async def search(q: str = Query(..., min_length=1), kind: Optional[str] = Query(None),
                 page: int = Query(0, ge=0, le=40)):
    q = q.strip()
    if q in ("", "*"):
        raise HTTPException(status_code=400, detail="Type a word to search for.")
    if kind and kind not in _KIND_IDS:
        raise HTTPException(status_code=400, detail=f"Unknown kind {kind!r}.")
    try:
        client = await _explorer_async()
    except Exception as exc:
        raise_egeria_http_error(exc, "resource-browser: search client failed")

    jobs = {"text": _search_text(client, q, kind, page)}
    if kind in (None, "table"):
        jobs["columns"] = _search_columns(client, q, page)
    if page == 0:  # tag, keyword and owner matches are bounded and come on the first page only
        jobs.update(tags=_search_tags(client, q), keywords=_search_keywords(client, q), owners=_search_owners(client, q))
    results = dict(zip(jobs, await asyncio.gather(*jobs.values(), return_exceptions=True)))

    failed = {}
    for name, res in results.items():
        if isinstance(res, Exception):
            failed[name] = str(res)[:200]
            logger.warning(f"resource-browser: search source {name} failed for {q!r}: {res}")
    if "text" in failed and len(failed) == len(results):
        raise_egeria_http_error(results["text"], f"resource-browser: search {q!r} failed")

    found: dict = {}
    not_shown = 0
    if "text" not in failed:
        rows, skipped = _rows(results["text"])
        not_shown += skipped
        for r in rows:
            _merge(found, [r], _text_reason(r, q))
    if "tags" in results and "tags" not in failed:
        for name, els in results["tags"]:
            rows, skipped = _rows(els)
            not_shown += skipped
            _merge(found, rows, f"tag: {name}")
    if "keywords" in results and "keywords" not in failed:
        rows, skipped = _rows(results["keywords"])
        not_shown += skipped
        _merge(found, rows, f"keyword: {q}")
    if "owners" in results and "owners" not in failed:
        rows, skipped = _rows(results["owners"])
        not_shown += skipped
        for r in rows:
            _merge(found, [r], f"owner: {r['owner']}")
    columns = None
    if "columns" in results and "columns" not in failed:
        columns = {k: v for k, v in results["columns"].items() if k != "tables"}
        for row, names in results["columns"]["tables"]:
            _merge(found, [row], "column: " + ", ".join(sorted(set(names))))

    items = [r for r in found.values() if not kind or r["kind"] == kind]
    items.sort(key=lambda r: _relevance(r, q))
    may_have_more = ("text" not in failed and len(results["text"]) == _SEARCH_PAGE) or \
                    (columns is not None and columns["found"] == _SEARCH_PAGE)
    # Sources read once (first page only) whose single read came back full: more may exist there.
    capped = [name for name in ("keywords", "owners") if name in results and name not in failed
              and len(results[name]) == _SEARCH_PAGE]
    capped += [f"tag: {name}" for name, els in (results.get("tags") if "tags" not in failed and "tags" in results else [])
               if len(els) == _SEARCH_PAGE]
    return JSONResponse({
        "query": q, "kind": kind, "page": page, "items": items,
        "mayHaveMore": may_have_more,
        "cappedSources": capped,
        "notShown": not_shown,
        "columns": columns,
        "failedSources": failed,
        "order": _ORDER_NOTE,
        "layer": "L0",
        "asOf": _now_iso(),
        "source": "ClassificationExplorer: find_elements_by_property_value, find_tags + get_elements_by_tag, "
                  "get_search_keyword_by_keyword, get_elements_by_classification_with_property_value (Ownership)",
    })


@router.get("/api/resource-browser/kinds", summary="The resource kinds search and browse filter on")
async def get_kinds():
    return JSONResponse({"kinds": [{"id": k, "label": label, "types": types} for k, label, types in _KINDS]
                         + [{"id": "other", "label": "Other", "types": []}]})


@router.get("/api/resource-browser/row-extras", summary="Tags, likes and rating summary for the rows on screen")
async def row_extras(guids: str = Query(..., description="Comma-separated GUIDs, at most 25")):
    wanted = [g for g in dict.fromkeys(x.strip() for x in guids.split(",")) if g][:_ROW_EXTRAS_CAP]
    try:
        client = await _explorer_async()
    except Exception as exc:
        raise_egeria_http_error(exc, "resource-browser: row extras client failed")
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def one(g):
        async with sem:
            return await client._async_get_element_by_guid(
                g, graph_query_depth=1, output_format="JSON",
                body={"class": "GetRequestBody", "graphQueryDepth": 1,
                      "includeOnlyRelationships": ["AttachedTag", "AttachedLike", "AttachedRating"]})
    got = await asyncio.gather(*(one(g) for g in wanted), return_exceptions=True)
    out = {}
    for g, el in zip(wanted, got):
        out[g] = None if isinstance(el, Exception) or not isinstance(el, dict) else _feedback_summary(el)
    return JSONResponse({"extras": out, "asOf": _now_iso(),
                         "source": "ClassificationExplorer.get_element_by_guid (AttachedTag, AttachedLike, AttachedRating)"})


# ── Home ──────────────────────────────────────────────────────────────────────

async def _recent(client, type_name):
    raw = await client._async_get_elements(
        type_name, start_from=0, page_size=_RECENT_PAGE, output_format="JSON", graph_query_depth=0,
        body={"class": "ResultsRequestBody", "metadataElementTypeName": type_name, "graphQueryDepth": 0,
              "sequencingOrder": "LAST_UPDATE_RECENT", "limitResultsByStatus": ["ACTIVE"],
              "startFrom": 0, "pageSize": _RECENT_PAGE})
    return _elements(raw)


def _recent_rows(batches: list) -> list:
    """Merge per-type newest-first pages into one newest-first list of resources."""
    seen = {}
    for batch in batches:
        for r in _rows(batch)[0]:
            seen.setdefault(r["guid"], r)
    return sorted(seen.values(), key=lambda r: r["updateTime"], reverse=True)


@router.get("/api/resource-browser/home", summary="Recently changed resources, and whether popularity is available")
async def home():
    try:
        client = await _explorer_async()
        batches = await asyncio.gather(*(_recent(client, t) for t in _RESOURCE_TYPES))
    except Exception as exc:
        raise_egeria_http_error(exc, "resource-browser: recently changed failed")
    rows = _recent_rows(batches)
    return JSONResponse({
        "recent": rows[:_RECENT_SHOWN],
        "recentPeople": [r for r in rows if not r["automated"]][:_RECENT_SHOWN],
        "recentWindow": {"perType": _RECENT_PAGE, "types": _RESOURCE_TYPES},
        "popular": {"available": False,
                    "reason": "Popularity is not available yet: Egeria holds no usage measure for these resources."},
        "me": _token_user(),
        "asOf": _now_iso(),
        "source": "ClassificationExplorer.get_elements (sequencingOrder LAST_UPDATE_RECENT)",
    })


_RE_LIST_PREFIX = "WorkingSet::resource-explorer::"
_PORTAL_LIST_PREFIX = "WorkingSet::portal::"


@router.get("/api/resource-browser/lists", summary="Work lists the user can see (read-only until phase 3)")
async def get_lists():
    try:
        client = await _explorer_async()
        sets, capped = await _all_elements(client, "WorkingSet", page=100, max_pages=10)
    except Exception as exc:
        if _is_unknown_type(exc):
            sets, capped = [], False
        else:
            raise_egeria_http_error(exc, "resource-browser: work lists failed")
    me = _token_user()
    from_re, mine = [], []
    for s in sets:
        hdr = s.get("elementHeader") or {}
        props = s.get("properties") or {}
        qn = props.get("qualifiedName", "")
        rec = {"guid": hdr.get("guid", ""), "displayName": _display_name(props, hdr.get("guid", "")),
               "qualifiedName": qn, "description": props.get("description") or "",
               "updateTime": (hdr.get("versions") or {}).get("updateTime") or ""}
        if qn.startswith(_RE_LIST_PREFIX):
            from_re.append(rec)
        elif me and qn.startswith(f"{_PORTAL_LIST_PREFIX}{me}::"):
            mine.append(rec)
    return JSONResponse({"mine": mine, "fromResourceExplorer": from_re, "capped": capped,
                         "editable": False, "note": "Creating and editing lists comes with work lists (phase 3).",
                         "asOf": _now_iso(), "source": "ClassificationExplorer.get_elements (WorkingSet)"})


# ── Browse ────────────────────────────────────────────────────────────────────

_FACETS = ["tag", "badge", "owner", "source", "collection", "flavour", "scope"]
_SOURCE_TYPES = ["Database", "DataFolder", "FileFolder"]
_COLLECTION_TYPES = ["DataSharingHub", "DigitalProductFamily", "WorkingSet"]


async def _classified(client, name: str) -> tuple:
    out = []
    for p in range(25):
        batch = _elements(await client._async_get_elements_by_classification(
            name, start_from=p * 200, page_size=200, output_format="JSON", graph_query_depth=0))
        if not batch:
            return out, False
        out.extend(batch)
    return out, True


async def _anchored(client, guid: str, type_name: str) -> list:
    return _elements(await client._async_get_elements_by_classification_with_property_value(
        "Anchors", guid, ["anchorGUID"], metadata_element_type_name=type_name, starts_with=True, ends_with=True,
        graph_query_depth=0, output_format="JSON", page_size=500))


async def _facet_values(facet: str) -> dict:
    client = await _explorer_async()
    if facet == "tag":
        tags = _elements(await client._async_find_tags(search_string="*", output_format="JSON", page_size=500))
        return {"values": sorted(({"id": (t.get("elementHeader") or {}).get("guid", ""),
                                   "label": _display_name(t.get("properties"), ""),
                                   "description": (t.get("properties") or {}).get("description") or ""}
                                  for t in tags), key=lambda v: v["label"].lower())}
    if facet == "badge":
        sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

        async def count(name):
            async with sem:
                return len(_rows((await _classified(client, name))[0])[0])
        counts = await asyncio.gather(*(count(b) for b in _BADGES))
        return {"values": [{"id": b, "label": b, "count": n} for b, n in zip(_BADGES, counts)],
                "countsAre": "resources with this classification, read in full"}
    if facet == "owner":
        els, capped = await _classified(client, "Ownership")
        owners = {}
        for r in _rows(els)[0]:
            owners[r["owner"] or "(owner not named)"] = owners.get(r["owner"] or "(owner not named)", 0) + 1
        return {"values": [{"id": o, "label": o, "count": n} for o, n in sorted(owners.items(), key=lambda kv: kv[0].lower())],
                "countsAre": "resources with this owner, read in full", "capped": capped}
    if facet == "source":
        out = []
        for t in _SOURCE_TYPES:
            for r in _rows((await _all_elements(client, t))[0])[0]:
                out.append({"id": r["guid"], "label": r["displayName"], "description": r["typeName"]})
        uniq = {v["id"]: v for v in out}
        return {"values": sorted(uniq.values(), key=lambda v: v["label"].lower())}
    if facet == "collection":
        out = []
        for t in _COLLECTION_TYPES:
            try:
                els, _ = await _all_elements(client, t)
            except Exception as exc:
                if _is_unknown_type(exc):
                    continue
                raise
            for e in els:
                hdr = e.get("elementHeader") or {}
                out.append({"id": hdr.get("guid", ""), "label": _display_name(e.get("properties"), hdr.get("guid", "")),
                            "description": _type_names(hdr)[0]})
        return {"values": sorted(out, key=lambda v: (v["description"], v["label"].lower()))}
    if facet == "flavour":
        return {"values": [{"id": "hub", "label": "Hub"}, {"id": "product", "label": "Product"},
                           {"id": "known", "label": "Known"}]}
    if facet == "scope":
        return {"values": [{"id": "all", "label": "Resources with a data scope (time or place)"}]}
    raise HTTPException(status_code=404, detail=f"Unknown browse facet {facet!r}.")


@router.get("/api/resource-browser/browse/{facet}", summary="The values of one browse facet")
async def browse_values(facet: str):
    if facet not in _FACETS:
        raise HTTPException(status_code=404, detail=f"Unknown browse facet {facet!r}.")
    try:
        value, stamp = await _cached(f"browse:{facet}", lambda: _facet_values(facet))
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: browse values for {facet} failed")
    return JSONResponse({"facet": facet, **value, **_age(stamp), "source": "Egeria (see the facet's list page)"})


async def _members(client, collection_guid: str) -> tuple:
    el = await client._async_get_element_by_guid(
        collection_guid, graph_query_depth=1, output_format="JSON",
        body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": ["CollectionMembership"]})
    hdr = (el or {}).get("elementHeader") or {}
    title = _display_name((el or {}).get("properties"), collection_guid)
    members = [i.get("relatedElement") for i in (el or {}).get("collectionMembers") or [] if isinstance(i, dict)]
    return title, _type_names(hdr)[0], members


@router.get("/api/resource-browser/browse/{facet}/{value}", summary="The resources under one browse facet value")
async def browse_list(facet: str, value: str):
    if facet not in _FACETS:
        raise HTTPException(status_code=404, detail=f"Unknown browse facet {facet!r}.")
    title, note, source, capped = value, None, "", False
    try:
        client = await _explorer_async()
        if facet == "tag":
            tag = await client._async_get_tag_by_guid(value, graph_query_depth=0, output_format="JSON")
            title = _display_name((tag or {}).get("properties"), value)
            els = _elements(await client._async_get_elements_by_tag(value, graph_query_depth=0, output_format="JSON",
                                                                    page_size=500))
            source = "ClassificationExplorer.get_elements_by_tag"
        elif facet == "badge":
            if value not in _BADGES:
                raise HTTPException(status_code=404, detail=f"{value!r} is not a badge this app shows.")
            els, capped = await _classified(client, value)
            source = "ClassificationExplorer.get_elements_by_classification"
        elif facet == "owner":
            els, capped = await _classified(client, "Ownership")
            want = None if value == "(owner not named)" else value
            els = [e for e in els if (_row(e) or {}).get("owner") == want]
            source = "ClassificationExplorer.get_elements_by_classification (Ownership)"
        elif facet == "source":
            src = await client._async_get_element_by_guid(value, graph_query_depth=0, output_format="JSON")
            title = _display_name((src or {}).get("properties"), value)
            els = [src] if src else []
            for t in ("DataSet", "DataStore"):
                els += await _anchored(client, value, t)
            schemas = [e for e in els if _type_names(e.get("elementHeader") or {})[0] == "DeployedDatabaseSchema"]
            sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

            async def tables(s):
                async with sem:
                    return await _anchored(client, (s.get("elementHeader") or {}).get("guid"), "RelationalTable")
            for batch in await asyncio.gather(*(tables(s) for s in schemas)):
                els += batch
            note = "The source itself, what it anchors, and the tables of its schemas."
            source = "ClassificationExplorer.get_elements_by_classification_with_property_value (Anchors.anchorGUID)"
        elif facet == "collection":
            title, ctype, els = await _members(client, value)
            title = f"{title} ({ctype})" if ctype else title
            source = "ClassificationExplorer.get_element_by_guid (CollectionMembership)"
        elif facet == "flavour":
            if value not in ("hub", "product", "known"):
                raise HTTPException(status_code=404, detail="Flavours are hub, product and known.")
            idx, _ = await _cached("flavours", _flavours_value)
            title = {"hub": "Hub resources", "product": "Product resources", "known": "Known resources"}[value]
            if value == "known":
                return JSONResponse({"facet": facet, "value": value, "title": title, "items": [], "notShown": 0,
                                     "note": "Every resource that is neither a product nor in a hub is Known. "
                                             "That is most of Egeria, so use Search and filter by flavour instead.",
                                     "asOf": _now_iso(), "source": ""})
            guids = list(idx["hub"]) if value == "hub" else list(dict.fromkeys(idx["productGuids"] + list(idx["product"])))
            if value == "hub" and not idx["hubTypeKnown"]:
                note = "This Egeria does not know the DataSharingHub type, so no resource can be a hub resource."
            elif value == "hub" and not idx["hubCount"]:
                note = "No data sharing hub exists in this Egeria yet."
            sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

            async def get(g):
                async with sem:
                    return await client._async_get_element_by_guid(g, graph_query_depth=0, output_format="JSON")
            got = await asyncio.gather(*(get(g) for g in guids), return_exceptions=True)
            els = [e for e in got if isinstance(e, dict)]
            capped = idx.get("capped", False)
            source = "the flavour index, then ClassificationExplorer.get_element_by_guid per resource"
        elif facet == "scope":
            els, capped = await _classified(client, "DataScope")
            title = "Resources with a data scope"
            source = "ClassificationExplorer.get_elements_by_classification (DataScope)"
    except HTTPException:
        raise
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: browse {facet}/{value} failed")
    rows, not_shown = _rows(els)
    uniq = list({r["guid"]: r for r in rows}.values())
    uniq.sort(key=lambda r: (r["kind"], r["displayName"].lower()))
    return JSONResponse({"facet": facet, "value": value, "title": title, "items": uniq, "notShown": not_shown,
                         "note": note, "capped": capped, "order": "By kind, then name.",
                         "asOf": _now_iso(), "source": source})
