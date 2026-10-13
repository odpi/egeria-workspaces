"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Browser — FastAPI router (phase 1: the Resource page; phase 2: search, Home, Browse;
phase 3: work lists).

A shop-for-resources app for people who look for resources (data, code, APIs, products)
rather than curate them.
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
  GET    /api/resource-browser/lists                         → work lists the user can see, and which hold what
  GET    /api/resource-browser/lists/{guid}                  → one list, every member with its rationale
  POST   /api/resource-browser/lists                         → create a list of your own
  PUT    /api/resource-browser/lists/{guid}                  → rename it or change its description
  POST   /api/resource-browser/lists/{guid}/members          → add resources (with a reason)
  DELETE /api/resource-browser/lists/{guid}/members/{m}      → remove one
  POST   /api/resource-browser/lists/{guid}/copy             → copy chosen members into a list of your own
  GET    /api/resource-browser/groups                        → the Teams and Communities you belong to
  POST   /api/resource-browser/lists/{guid}/share            → share a list of yours with one of them
  DELETE /api/resource-browser/lists/{guid}/share/{group}    → stop sharing it
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
import json
import os
import re
import uuid
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
# a 4.6 MB payload), and engine-action targets mean nothing to someone looking for resources.
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
    """catalog.schema.table for a JDBC-catalogued table, from its additionalProperties.

    A column carries the same three plus jdbc.column; it is not a table, and its
    figures are shown in its table's columns card."""
    ap = (props or {}).get("additionalProperties") or {}
    if ap.get("jdbc.column"):
        return None
    parts = [ap.get("jdbc.catalog"), ap.get("jdbc.schema"), ap.get("jdbc.table")]
    return ".".join(parts) if all(parts) else None


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/resource-browser", include_in_schema=False)
async def serve_resource_browser():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Resource Browser page not found")
    return FileResponse(str(_HTML), media_type="text/html")


# ── Reading a resource ────────────────────────────────────────────────────────
#
# A surveyed database carries about a thousand measurement annotations. At graph
# depth 1 Egeria reads every one of them, even when skipRelationships names them
# (15 s for coco_pharma), and a long includeOnlyRelationships list is not honoured
# either. A short list is. So an element with many annotations is read as several
# short lists of the relationships this page shows, in parallel (~0.5 s), and the
# page says that only those were read. Everything else is read in one call.

_ANNOTATION_HEAVY = 50       # annotations at which the curated read is used
_INCLUDE_CHUNK = 10          # relationship types per curated call
_PAGE_RELATIONSHIPS = [
    # sections of the page
    "CollectionMembership", "NestedSchemaAttribute", "ReportSubject", "SearchKeywordLink", "SemanticAssignment",
    "DataFlow", "ControlFlow", "ProcessCall", "LineageMapping", "DataMapping", "UltimateSource", "UltimateDestination",
    # structure
    "DataSetContent", "NestedFile", "FolderHierarchy", "AttributeForSchema", "Schema",
    # where it fits
    "ResourceConnection", "CatalogTarget", "ImplementedBy", "GovernedBy", "ScopedBy", "AssignmentScope",
    "ResourceList", "DataDescription", "ExternalIdLink", "MonitoredResource", "DeployedOn", "SourcedFrom",
    "CatalogTemplate", "RelatedTerm", "MoreInformation", "ExternalReferenceLink", "Certification", "License",
    "APIEndpoint", "SchemaTypeDefinition", "CapabilityAssetUse", "TargetForGovernanceAction",
]


async def _annotation_heavy(client, guid: str) -> bool:
    """Whether the element has at least _ANNOTATION_HEAVY annotations (one short page, ~0.1 s)."""
    try:
        raw = await client._async_get_related_elements(
            guid, relationship_type="AssociatedAnnotation", output_format="JSON", page_size=_ANNOTATION_HEAVY,
            body={"class": "ResultsRequestBody", "startFrom": 0, "pageSize": _ANNOTATION_HEAVY, "graphQueryDepth": 0})
    except Exception as exc:
        logger.debug(f"resource-browser: annotation count for {guid} failed: {exc}")
        return False
    return isinstance(raw, list) and len(raw) >= _ANNOTATION_HEAVY


def _merge_reads(reads: list) -> dict:
    """Several depth-1 reads of one element → one, each relationship once."""
    out = {k: reads[0][k] for k in ("elementHeader", "properties") if k in reads[0]}
    seen = set()
    for el in reads:
        for key, val in el.items():
            if key in ("elementHeader", "properties") or not isinstance(val, (list, dict)):
                out.setdefault(key, val)
                continue
            for item in (val if isinstance(val, list) else [val]):
                rel_guid = ((item.get("relationshipHeader") or {}).get("guid") if isinstance(item, dict) else None) or id(item)
                if rel_guid in seen:
                    continue
                seen.add(rel_guid)
                if isinstance(val, list):
                    out.setdefault(key, []).append(item)
                else:
                    out.setdefault(key, item)
    return out


async def _read_resource(client, guid: str) -> tuple:
    """(element at graph depth 1, whether only the page's relationships were read)."""
    if not await _annotation_heavy(client, guid):
        el = await client._async_get_element_by_guid(
            guid, graph_query_depth=1, output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1, "skipRelationships": _SKIP_RELATIONSHIPS})
        return el, False
    chunks = [_PAGE_RELATIONSHIPS[i:i + _INCLUDE_CHUNK] for i in range(0, len(_PAGE_RELATIONSHIPS), _INCLUDE_CHUNK)]
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def one(types):
        async with sem:
            return await client._async_get_element_by_guid(
                guid, graph_query_depth=1, output_format="JSON",
                body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": types})
    reads = [r for r in await asyncio.gather(*(one(c) for c in chunks)) if isinstance(r, dict) and r.get("elementHeader")]
    return (_merge_reads(reads) if reads else None), True


@router.get("/api/resource-browser/resource/{guid}", summary="Everything the Resource page shows, in one call")
async def get_resource(guid: str):
    try:
        client = await _explorer_async()
        el, curated = await _read_resource(client, guid)
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
    shown = {"memberOfCollections", "schemaAttributes", "reports", "searchKeywords"} | _STRUCTURE_SHOWN_KEYS
    other = {}
    for key, recs in related.items():
        if key in shown:
            continue
        rest = [{k: r[k] for k in ("guid", "typeName", "displayName", "relationshipType", "atEnd1")}
                for r in recs if r["relationshipType"] not in _LINEAGE_RELATIONSHIPS
                and r["relationshipType"] not in _STRUCTURE_RELATIONSHIPS
                and r["relationshipType"] != "SemanticAssignment"
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
        "relationshipsLimited": curated,
        "source": "ClassificationExplorer.get_element_by_guid (graph depth 1"
                  + (", the page's relationships only)" if curated else ")"),
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
            log_name = _display_name(log.get("properties"), "")
            notes.extend(dict(_note_record(n), log=log_name) for n in batch)
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


# ── Structure: what a resource is part of, and what it contains ──────────────
#
# Egeria names each related element by the role it plays at its end of the
# relationship (DataSetContent: end1 supportedDataSets, end2 dataSetContent), so
# the key alone says which side of the containment the related element is on.

_CONTAINS_KEYS = [                       # (key, relationship): the parts it holds
    ("supportedDataSets", "DataSetContent"),
    ("nestedFolders", "FolderHierarchy"),
    ("nestedFiles", "NestedFile"),
    ("collectionMembers", "CollectionMembership"),
]
_PART_OF_KEYS = ["dataSetContent", "parentFolder", "homeFolder"]   # its container

# Relationships the structure section shows, left out of "where it fits".
_STRUCTURE_RELATIONSHIPS = {"DataSetContent", "FolderHierarchy", "NestedFile", "AttributeForSchema",
                            "NestedSchemaAttribute", "APIOperations", "SchemaTypeOption"}
_STRUCTURE_SHOWN_KEYS = {k for k, _ in _CONTAINS_KEYS} | set(_PART_OF_KEYS)

_PATH_HOPS = 5          # containers walked up from a resource
_PARTS_CAP = 200        # parts listed per group
_PART_COUNT_CAP = 50    # parts whose own contents are counted


def _related_recs(val) -> list:
    """A relationship key's value (a list, or one related element) → flat records."""
    items = val if isinstance(val, list) else [val]
    return [r for r in (_related(i) for i in items) if r]


def _is_schema_attribute(type_name: str, supers: list) -> bool:
    return "SchemaAttribute" in [type_name] + list(supers or [])


def _is_schema_element(type_name: str, supers: list) -> bool:
    return "SchemaElement" in [type_name] + list(supers or [])


# Asking for only these is what keeps the walk fast: a surveyed database carries
# about a thousand measurement annotations, and skipping them still costs ~13 s a
# read where naming the wanted relationships takes ~0.2 s.
_STRUCTURE_INCLUDE = ["DataSetContent", "FolderHierarchy", "NestedFile", "CollectionMembership",
                      "Schema", "AttributeForSchema", "NestedSchemaAttribute", "APIOperations", "SchemaTypeOption"]

# What a schema type holds, by key: a schema's tables and a data set's fields
# (schemaAttributes), an API's operations, a topic's event types (schema options).
_SCHEMA_PART_KEYS = ["schemaAttributes", "containsOperations", "schemaOptions"]

# Labels for parts that have no resource kind of their own.
_PART_LABELS = {"APIOperation": "Operations", "EventType": "Event types", "GlossaryTerm": "Glossary terms",
                "CollectionFolder": "Folders", "Collection": "Collections"}

# Kinds whose parts are worth counting (a schema's tables, a table's columns, …).
_COUNTED_KINDS = {"database", "schema", "table", "file", "topic", "product", "dataset"}
_COUNTED_TYPES = {"EventType"}
_RELATED_LIMIT = 1000   # Egeria returns at most this many relationships per key at depth 1


async def _get_depth1(client, guid: str) -> dict:
    """The element with only its containment relationships, one level each way."""
    return await client._async_get_element_by_guid(
        guid, graph_query_depth=1, output_format="JSON",
        body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": _STRUCTURE_INCLUDE})


def _container_of(el: dict) -> Optional[dict]:
    """The element one level up from this one, or None at the top.

    A data set sits in its content (a schema in its database); a file or folder in
    its folder. A table or column is a schema attribute: a column's container is
    its table; a top-level table hangs off a schema type, so its container is the
    asset the schema type describes, which is the table's anchor. Other schema
    elements (an API operation, a topic's event type) belong to their anchor too."""
    for key in _PART_OF_KEYS:
        recs = _related_recs(el.get(key))
        if recs:
            return recs[0]
    hdr = el.get("elementHeader") or {}
    type_name, supers = _type_names(hdr)
    if _is_schema_element(type_name, supers):
        for p in _related_recs(el.get("parentSchemaElements")):
            if _is_schema_attribute(p["typeName"], p["superTypeNames"]) or p["typeName"] in _COUNTED_TYPES:
                return p
        anchor = (hdr.get("anchor") or {}).get("classificationProperties") or {}
        if anchor.get("anchorGUID") and anchor["anchorGUID"] != hdr.get("guid"):
            return {"guid": anchor["anchorGUID"], "typeName": anchor.get("anchorTypeName", ""),
                    "superTypeNames": [], "displayName": ""}
    return None


def _part_record(rec: dict) -> dict:
    hdr = rec.get("elementHeader") or {}
    anchor = (hdr.get("anchor") or {}).get("classificationProperties") or {}
    return {
        "guid": rec["guid"],
        "typeName": rec["typeName"],
        "superTypeNames": rec["superTypeNames"],
        "displayName": rec["displayName"],
        "qualifiedName": rec.get("qualifiedName", ""),
        "kind": _kind_of(rec["typeName"], rec["superTypeNames"]),
        # Tables and columns have no page of their own in The Catalog; their anchor does.
        "anchorGUID": anchor.get("anchorGUID") if anchor.get("anchorGUID") != rec["guid"] else None,
        "count": None,
    }


async def _schema_parts(client, el: dict) -> list:
    """What the element's schema type holds: a schema's tables, a data set's fields,
    an API's operations, a topic's event types."""
    st = _related_recs(el.get("schemaType"))
    if not st:
        return []
    st_el = await _get_depth1(client, st[0]["guid"]) or {}
    return [r for key in _SCHEMA_PART_KEYS for r in _related_recs(st_el.get(key))]


def _attribute_noun(parts: list) -> str:
    if {_kind_of(p["typeName"], p["superTypeNames"]) for p in parts} == {"table"}:
        return "tables"
    if all(p["typeName"] == "RelationalColumn" for p in parts):
        return "columns"
    return "fields"


async def _count_parts(client, guid: str) -> Optional[dict]:
    """How many parts one contained element holds, by the same rules, or None."""
    el = await _get_depth1(client, guid)
    if not isinstance(el, dict):
        return None
    cols = _related_recs(el.get("schemaAttributes"))
    if cols:
        return {"n": len(cols), "of": _attribute_noun(cols)}
    parts = await _schema_parts(client, el)
    if parts:
        return {"n": len(parts), "of": _attribute_noun(parts)}
    n = sum(len(_related_recs(el.get(k))) for k, _ in _CONTAINS_KEYS)
    return {"n": n, "of": "parts"} if n else None


def _group_label(part: dict) -> str:
    if part["typeName"] in _PART_LABELS:
        return _PART_LABELS[part["typeName"]]
    if part["kind"] != "other":
        return next(label for k, label, _types in _KINDS if k == part["kind"])
    if _is_schema_attribute(part["typeName"], part["superTypeNames"]):
        return "Fields"
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", part["typeName"])


async def _part_sources(client, el: dict) -> list:
    """[(relationship, related records)] for each way the element holds parts."""
    sources = [(rel, recs) for key, rel in _CONTAINS_KEYS for recs in [_related_recs(el.get(key))] if recs]
    try:
        schema_parts = await _schema_parts(client, el)
    except Exception as exc:
        logger.debug(f"resource-browser: schema parts not readable: {exc}")
        schema_parts = []
    if schema_parts:
        sources.append(("AttributeForSchema", schema_parts))
    return sources


@router.get("/api/resource-browser/resource/{guid}/structure",
            summary="What a resource is part of, and the parts it contains")
async def get_structure(guid: str):
    try:
        client = await _explorer_async()
        el = await _get_depth1(client, guid)
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: structure of {guid} failed")
    if not isinstance(el, dict) or not el.get("elementHeader"):
        raise HTTPException(status_code=404, detail=_NOT_VISIBLE)
    type_name, supers = _type_names(el["elementHeader"])

    # Part of: walk up, one container at a time.
    path, seen, cur, path_cut = [], {guid}, el, False
    try:
        for _ in range(_PATH_HOPS):
            up = _container_of(cur)
            if not up or up["guid"] in seen:
                break
            seen.add(up["guid"])
            cur = await _get_depth1(client, up["guid"])
            if not isinstance(cur, dict) or not cur.get("elementHeader"):
                path_cut = True
                break
            hdr = cur["elementHeader"]
            t, s = _type_names(hdr)
            path.append({"guid": up["guid"], "typeName": t, "superTypeNames": s,
                         "displayName": _display_name(cur.get("properties"), up["guid"]),
                         "kind": _kind_of(t, s)})
        else:
            path_cut = _container_of(cur) is not None
    except Exception as exc:  # what was found so far still helps
        logger.debug(f"resource-browser: container walk for {guid} stopped: {exc}")
        path_cut = True
    path.reverse()

    # Contains: the parts, grouped by kind. A table's columns have their own card.
    groups = {}
    for rel, recs in await _part_sources(client, el):
        for rec in recs:
            part = _part_record(rec)
            g = groups.setdefault((rel, _group_label(part)),
                                  {"label": _group_label(part), "relationship": rel, "parts": [], "total": 0})
            g["total"] += 1
            if len(g["parts"]) < _PARTS_CAP:
                g["parts"].append(part)
    contains = sorted(groups.values(), key=lambda g: g["label"])
    for g in contains:
        g["parts"].sort(key=lambda p: p["displayName"].lower())

    for g in contains:
        g["atLeast"] = g["total"] >= _RELATED_LIMIT

    # Count each part's own parts (a schema's tables, a table's columns), bounded.
    to_count = [p for g in contains for p in g["parts"]
                if p["kind"] in _COUNTED_KINDS or p["typeName"] in _COUNTED_TYPES][:_PART_COUNT_CAP]
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def count(part):
        async with sem:
            try:
                part["count"] = await _count_parts(client, part["guid"])
            except Exception as exc:
                logger.debug(f"resource-browser: count parts of {part['guid']} failed: {exc}")
    await asyncio.gather(*(count(p) for p in to_count))

    n_parts = sum(len(g["parts"]) for g in contains)
    return JSONResponse({
        "guid": guid,
        "typeName": type_name,
        "partOf": path,
        "partOfIncomplete": path_cut,
        "contains": contains,
        "countsCapped": len(to_count) >= _PART_COUNT_CAP and n_parts > _PART_COUNT_CAP,
        "asOf": _now_iso(),
        "source": "ClassificationExplorer.get_element_by_guid (graph depth 1), one call per level",
    })


# ── Meaning: glossary terms assigned to a resource and its columns ───────────
#
# A SemanticAssignment links an element (end 1) to the glossary term that says
# what it means (end 2). One a user adds here is PROPOSED: a steward validates it
# in Egeria Explorer. Only the user who proposed one may remove it here.

_MEANING_COLUMN_CAP = 200
_TERM_SEARCH_PAGE = 20


def _is_term(type_name: str, supers: list) -> bool:
    return "GlossaryTerm" in [type_name] + list(supers or [])


def _meanings_of(el: dict) -> list:
    """The terms assigned to an element, with how and by whom."""
    out = {}
    for key, val in (el or {}).items():
        if key in ("elementHeader", "properties") or not isinstance(val, (list, dict)):
            continue
        for item in (val if isinstance(val, list) else [val]):
            rec = _related(item)
            if not rec or rec["relationshipType"] != "SemanticAssignment" or not _is_term(rec["typeName"], rec["superTypeNames"]):
                continue
            rel_versions = ((item.get("relationshipHeader") or {}).get("versions") or {})
            rp = rec["relationshipProperties"]
            out[rec["guid"]] = {
                "guid": rec["guid"],
                "displayName": rec["displayName"],
                "qualifiedName": rec["qualifiedName"],
                "summary": rec["properties"].get("summary") or rec["description"] or "",
                "status": rp.get("termAssignmentStatus") or rp.get("status") or "",
                "confidence": rp.get("confidence") or None,
                "description": rp.get("description") or "",
                "assignedBy": rel_versions.get("createdBy") or rp.get("createdBy") or "",
                "assignedAt": rel_versions.get("createTime") or "",
            }
    return sorted(out.values(), key=lambda t: t["displayName"].lower())


async def _read_meanings(client, guid: str, with_columns: bool = True) -> dict:
    el = await client._async_get_element_by_guid(
        guid, graph_query_depth=1, output_format="JSON",
        body={"class": "GetRequestBody", "graphQueryDepth": 1,
              "includeOnlyRelationships": ["SemanticAssignment", "NestedSchemaAttribute"]})
    if not isinstance(el, dict) or not el.get("elementHeader"):
        raise HTTPException(status_code=404, detail=_NOT_VISIBLE)
    columns = {}
    col_recs = _related_recs(el.get("schemaAttributes")) if with_columns else []
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def one(col):
        async with sem:
            try:
                c_el = await client._async_get_element_by_guid(
                    col["guid"], graph_query_depth=1, output_format="JSON",
                    body={"class": "GetRequestBody", "graphQueryDepth": 1, "includeOnlyRelationships": ["SemanticAssignment"]})
                terms = _meanings_of(c_el)
                if terms:
                    columns[col["guid"]] = terms
            except Exception as exc:
                logger.debug(f"resource-browser: meanings of column {col['guid']} failed: {exc}")
    await asyncio.gather(*(one(c) for c in col_recs[:_MEANING_COLUMN_CAP]))
    return {"guid": guid, "meanings": _meanings_of(el), "columns": columns,
            "columnsCapped": len(col_recs) > _MEANING_COLUMN_CAP, "me": _token_user(),
            "asOf": _now_iso(), "source": "ClassificationExplorer.get_element_by_guid (SemanticAssignment)"}


@router.get("/api/resource-browser/resource/{guid}/meanings",
            summary="Glossary terms that say what a resource, and each of its columns, means")
async def get_meanings(guid: str):
    try:
        client = await _explorer_async()
        return JSONResponse(await _read_meanings(client, guid))
    except HTTPException:
        raise
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: meanings of {guid} failed")


class MeaningBody(BaseModel):
    termGuid: str
    description: Optional[str] = None


@router.post("/api/resource-browser/resource/{guid}/meanings",
             summary="Propose a glossary term as the meaning of a resource or column")
async def add_meaning(guid: str, body: MeaningBody):
    user = _require_signed_in()
    try:
        client = await _explorer_async()
        # termAssignmentStatus, not "status" as pyegeria's docstring sample has it: Egeria
        # silently drops a property it does not know.
        props = {"class": "SemanticAssignmentProperties", "termAssignmentStatus": "PROPOSED", "createdBy": user}
        if body.description and body.description.strip():
            props["description"] = body.description.strip()
        await client._async_setup_semantic_assignment(
            body.termGuid, guid, {"class": "NewRelationshipRequestBody", "properties": props})
        return JSONResponse(await _read_meanings(client, guid, with_columns=False))
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: assign term {body.termGuid} to {guid} failed")


@router.delete("/api/resource-browser/resource/{guid}/meanings/{term_guid}",
               summary="Withdraw a meaning you proposed")
async def remove_meaning(guid: str, term_guid: str):
    user = _require_signed_in()
    try:
        client = await _explorer_async()
        current = await _read_meanings(client, guid, with_columns=False)
        mine = next((t for t in current["meanings"] if t["guid"] == term_guid), None)
        if not mine:
            raise HTTPException(status_code=404, detail="That term is not assigned to this resource.")
        if mine["assignedBy"] != user:
            raise HTTPException(status_code=403, detail=(
                f"Only {mine['assignedBy'] or 'whoever assigned it'} can withdraw this here; "
                "a steward can change it in Egeria Explorer."))
        await client._async_clear_semantic_assignment_classification(term_guid, guid)
        return JSONResponse(await _read_meanings(client, guid, with_columns=False))
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: withdraw term {term_guid} from {guid} failed")


@router.get("/api/resource-browser/terms", summary="Glossary terms matching some text, to choose a meaning from")
async def search_terms(q: str = Query(..., min_length=2)):
    try:
        client = await _explorer_async()
        raw = await client._async_find_elements_by_property_value(
            property_value=q, property_names=["displayName", "qualifiedName", "summary"],
            metadata_element_subtypes=["GlossaryTerm"], starts_with=False, ends_with=False, ignore_case=True,
            graph_query_depth=0, output_format="JSON", page_size=_TERM_SEARCH_PAGE)
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: term search {q!r} failed")
    terms = []
    for e in _elements(raw):
        hdr = e.get("elementHeader") or {}
        props = e.get("properties") or {}
        terms.append({"guid": hdr.get("guid", ""), "displayName": _display_name(props, hdr.get("guid", "")),
                      "qualifiedName": props.get("qualifiedName", ""),
                      "summary": props.get("summary") or props.get("description") or ""})
    terms.sort(key=lambda t: (not t["displayName"].lower().startswith(q.lower()), t["displayName"].lower()))
    return JSONResponse({"terms": terms, "asOf": _now_iso(),
                         "source": "ClassificationExplorer.find_elements_by_property_value (GlossaryTerm)"})


# ── Notes on its parts ───────────────────────────────────────────────────────

_PART_NOTES_CAP = 100   # parts whose note logs are read


async def _notes_on(client, guid: str) -> list:
    logs = _elements(await client._async_get_attached_note_logs(guid, graph_query_depth=0, output_format="JSON"))
    notes = []
    for log in logs:
        raw = await client._async_get_notes_for_note_log(
            (log.get("elementHeader") or {}).get("guid"), output_format="JSON", page_size=_NOTES_CAP)
        notes.extend(_note_record(n) for n in _elements(raw))
    return notes


@router.get("/api/resource-browser/resource/{guid}/part-notes",
            summary="Notes and journal entries left on a resource's parts, one level down")
async def get_part_notes(guid: str):
    try:
        client = await _explorer_async()
        el = await _get_depth1(client, guid)
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: part notes of {guid} failed")
    if not isinstance(el, dict) or not el.get("elementHeader"):
        raise HTTPException(status_code=404, detail=_NOT_VISIBLE)
    parts = [r for _rel, recs in await _part_sources(client, el) for r in recs]
    parts += _related_recs(el.get("schemaAttributes"))           # a table's columns
    checked = parts[:_PART_NOTES_CAP]
    found = []
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def one(rec):
        async with sem:
            try:
                notes = await _notes_on(client, rec["guid"])
            except Exception as exc:
                logger.debug(f"resource-browser: notes on part {rec['guid']} failed: {exc}")
                return
        if notes:
            notes.sort(key=lambda n: n["createTime"], reverse=True)
            found.append({"part": {k: rec[k] for k in ("guid", "typeName", "displayName")}, "notes": notes})
    await asyncio.gather(*(one(r) for r in checked))
    found.sort(key=lambda f: f["notes"][0]["createTime"], reverse=True)
    return JSONResponse({"guid": guid, "parts": found, "partsChecked": len(checked),
                         "capped": len(parts) > _PART_NOTES_CAP, "asOf": _now_iso(),
                         "source": "get_attached_note_logs + get_notes_for_note_log on each part"})


# ══ Phase 2: search, Home, Browse ════════════════════════════════════════════
#
# L0 search (spec §6): Egeria's own find, ordered by text relevance, with the
# source and as-of on every response so a later layer can replace it unseen.
# Egeria cannot sort by use or count facets, so neither is attempted here.

# Search and browse scope: resources people look for (data, code, APIs, products).
# "Asset" alone would bring in ~8,600 Notifications and ~700 EngineActions, which
# are operational records, not resources.
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
    ("repo", "Code repositories", []),   # recognised by _REPO_QN_PREFIX, see _is_repo
]

# Resource Explorer publishes a GitHub repository as a plain Asset named
# GitHubRepository::<url> (no subtype yet), so a repo is told by its name.
_REPO_QN_PREFIX = "GitHubRepository::"
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


def _is_repo(type_name: str, qualified_name: str) -> bool:
    return type_name == "Asset" and (qualified_name or "").startswith(_REPO_QN_PREFIX)


def _row(el: dict, any_type: bool = False) -> Optional[dict]:
    """One result row, from an element (or a related element) at graph depth 0.

    None for templates, and (unless any_type) for anything that is not a resource this app lists."""
    if not isinstance(el, dict):
        return None
    hdr = el.get("elementHeader") or {}
    guid = hdr.get("guid")
    type_name, supers = _type_names(hdr)
    props = el.get("properties") or {}
    repo = _is_repo(type_name, props.get("qualifiedName", ""))
    if not guid or (not any_type and not repo and not _is_resource(type_name, supers)):
        return None
    cls = _classifications(hdr)
    if any(c["name"] == "Template" for c in cls):
        return None
    versions = hdr.get("versions") or {}
    desc = props.get("description") or ""
    return {
        "guid": guid,
        "typeName": type_name,
        "kind": "repo" if repo else _kind_of(type_name, supers),
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
    """(rows, not_shown): rows for the resources, and how many elements were not."""
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


async def _repos_value():
    """Every published code repository (a plain Asset named GitHubRepository::<url>), as rows."""
    client = await _explorer_async()
    out = []
    for p in range(10):
        batch = _elements(await client._async_find_elements_by_property_value(
            property_value=_REPO_QN_PREFIX, property_names=["qualifiedName"], metadata_element_subtypes=["Asset"],
            starts_with=True, ends_with=False, ignore_case=False, graph_query_depth=0, output_format="JSON",
            start_from=p * 200, page_size=200))
        if not batch:
            break
        out.extend(r for r in (_row(e) for e in batch) if r and r["kind"] == "repo")
    return out


async def _search_repos(q):
    rows, _stamp = await _cached("repos", _repos_value)
    ql = q.lower()
    return [r for r in rows if ql in r["displayName"].lower() or ql in r["qualifiedName"].lower()
            or ql in r["description"].lower()]


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

    jobs = {} if kind == "repo" else {"text": _search_text(client, q, kind, page)}
    if kind in (None, "repo") and page == 0:
        jobs["repos"] = _search_repos(q)
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
    if failed and len(failed) == len(results):
        raise_egeria_http_error(next(r for r in results.values() if isinstance(r, Exception)),
                                f"resource-browser: search {q!r} failed")

    found: dict = {}
    not_shown = 0
    if "repos" in results and "repos" not in failed:
        for r in results["repos"]:
            _merge(found, [r], _text_reason(r, q))
    if "text" in results and "text" not in failed:
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
    may_have_more = ("text" in results and "text" not in failed and len(results["text"]) == _SEARCH_PAGE) or \
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


# ── Work lists (phase 3, spec §5 option (a)) ─────────────────────────────────
#
# A work list is an Egeria WorkingSet. The Portal's own lists are named
# WorkingSet::portal::<user>::<slug> and only their creator changes them here.
# Resource Explorer's published lists (WorkingSet::resource-explorer::<slug>) are
# read-only: a person copies the members they want into a list of their own, and
# nothing is ever written back to RE. A copy is a snapshot that records its source
# in additionalProperties.

_LIST_CAP = 200            # members read per list; Egeria membership pages are bounded
_ADD_CAP = 100             # members added in one request
_COPY_KEYS = ("copiedFromGUID", "copiedFromQualifiedName", "copiedFromName", "copiedAt")


async def _collections_async():
    from pyegeria import CollectionManager
    client = CollectionManager(**_client_kwargs())
    await async_apply_token(client)
    return client


def _list_slug(name: str, suffix: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "list"
    return f"{base}-{suffix}"


def _list_origin(qualified_name: str, me: Optional[str]) -> str:
    """mine | resource-explorer | portal (another person's) | other."""
    if me and qualified_name.startswith(f"{_PORTAL_LIST_PREFIX}{me}::"):
        return "mine"
    if qualified_name.startswith(_RE_LIST_PREFIX):
        return "resource-explorer"
    if qualified_name.startswith(_PORTAL_LIST_PREFIX):
        return "portal"
    return "other"


def _list_record(el: dict, me: Optional[str]) -> dict:
    hdr = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    versions = hdr.get("versions") or {}
    qn = props.get("qualifiedName", "")
    origin = _list_origin(qn, me)
    ap = props.get("additionalProperties") or {}
    copied = {k: ap[k] for k in _COPY_KEYS if ap.get(k)}
    return {
        "guid": hdr.get("guid", ""),
        "displayName": _display_name(props, hdr.get("guid", "")),
        "qualifiedName": qn,
        "description": props.get("description") or "",
        "origin": origin,
        "editable": origin == "mine",
        "creator": qn.split("::")[2] if origin in ("mine", "portal") and qn.count("::") >= 3 else None,
        "copiedFrom": copied or None,
        "sharedWith": _shared_with(el),
        "createdBy": versions.get("createdBy") or "",
        "updatedBy": versions.get("updatedBy") or "",
        "updateTime": versions.get("updateTime") or versions.get("createTime") or "",
    }


def _list_members(el: dict) -> list:
    """Members of a list read with its CollectionMembership relationships: every
    member, a listed resource kind or not, with the reason it is on the list."""
    out = []
    for item in (el or {}).get("collectionMembers") or []:
        if not isinstance(item, dict):
            continue
        row = _row(item.get("relatedElement"), any_type=True)
        if not row:
            continue
        rel = {k: v for k, v in (item.get("relationshipProperties") or {}).items() if k not in ("class", "typeName")}
        # Egeria 6.2 stores `confidence` (an int defaulting to 0); `expectedConfidence`
        # is silently dropped on write. 0 cannot be told from "never set", so it reads as None.
        out.append(dict(row, rationale=rel.get("membershipRationale") or "",
                        confidence=rel.get("confidence") or None,
                        isResource=_row(item.get("relatedElement")) is not None))
    return out


def _membership_body(rationale: Optional[str], confidence=None) -> Optional[dict]:
    props = {}
    if rationale:
        props["membershipRationale"] = rationale
    if confidence:
        props["confidence"] = confidence
    if not props:
        return None
    return {"class": "NewRelationshipRequestBody", "properties": dict(props, **{"class": "CollectionMembershipProperties"})}


async def _read_list(client, guid: str) -> dict:
    el = await client._async_get_element_by_guid(
        guid, graph_query_depth=1, output_format="JSON",
        body={"class": "GetRequestBody", "graphQueryDepth": 1,
              "includeOnlyRelationships": ["CollectionMembership", "ResourceList"]})
    if not isinstance(el, dict) or _type_names(el.get("elementHeader") or {})[0] != "WorkingSet":
        raise HTTPException(status_code=404, detail="That is not a work list visible to you.")
    return el


async def _my_list(client, guid: str) -> tuple:
    """(element, record) for a list the signed-in user may change, else 403."""
    me = _require_signed_in()
    el = await _read_list(client, guid)
    rec = _list_record(el, me)
    if not rec["editable"]:
        why = ("Resource Explorer lists are read-only here: copy the members you want into a list of your own."
               if rec["origin"] == "resource-explorer" else "Only the person who made a list can change it.")
        raise HTTPException(status_code=403, detail=why)
    return el, rec


@router.get("/api/resource-browser/lists", summary="Work lists the user can see")
async def get_lists():
    try:
        client = await _explorer_async()
        sets, capped = await _all_elements(client, "WorkingSet",
                                           {"includeOnlyRelationships": ["CollectionMembership", "ResourceList"]},
                                           depth=1, page=100, max_pages=10)
    except Exception as exc:
        if _is_unknown_type(exc):
            sets, capped = [], False
        else:
            raise_egeria_http_error(exc, "resource-browser: work lists failed")
    me = _token_user()
    my_groups, groups_note = set(), None
    if me:
        try:
            g, _ = await _cached("groups", _groups_value)
            my_groups = {x["guid"] for x in g["groups"]}
            groups_note = None if my_groups else f"No teams found: {g['how']}."
        except Exception as exc:  # the lists still show; only "shared with you" is unknown
            groups_note = "Your teams could not be read, so lists shared with them are not shown."
            logger.warning(f"resource-browser: groups for lists failed: {exc}")
    mine, from_re, shared, member_of = [], [], [], {}
    for s in sets:
        rec = _list_record(s, me)
        members = [((i.get("relatedElement") or {}).get("elementHeader") or {}).get("guid")
                   for i in s.get("collectionMembers") or [] if isinstance(i, dict)]
        rec["memberCount"] = len([m for m in members if m])
        if rec["origin"] == "mine":
            mine.append(rec)
            for m in members:
                if m:
                    member_of.setdefault(m, []).append(rec["guid"])
        elif rec["origin"] == "resource-explorer":
            from_re.append(rec)
        if rec["origin"] != "mine" and my_groups & {g["guid"] for g in rec["sharedWith"]}:
            shared.append(rec)
    shared.sort(key=lambda r: r["displayName"].lower())
    mine.sort(key=lambda r: r["displayName"].lower())
    from_re.sort(key=lambda r: r["displayName"].lower())
    return JSONResponse({"mine": mine, "fromResourceExplorer": from_re, "sharedWithMe": shared,
                         "groupsNote": groups_note, "memberOf": member_of, "capped": capped,
                         "canWrite": me is not None, "me": me,
                         "asOf": _now_iso(), "source": "ClassificationExplorer.get_elements (WorkingSet, CollectionMembership)"})


@router.get("/api/resource-browser/lists/{guid}", summary="One work list with its members and why each is on it")
async def get_list(guid: str):
    try:
        client = await _explorer_async()
        el = await _read_list(client, guid)
    except HTTPException:
        raise
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: work list {guid} failed")
    members = _list_members(el)
    members.sort(key=lambda r: (r["kind"], r["displayName"].lower()))
    return JSONResponse({**_list_record(el, _token_user()), "members": members,
                         "capped": len(members) >= _LIST_CAP, "canWrite": _token_user() is not None,
                         "asOf": _now_iso(), "source": "ClassificationExplorer.get_element_by_guid (CollectionMembership)"})


class NewListBody(BaseModel):
    name: str
    description: Optional[str] = None


async def _create_list(client, me: str, name: str, description: str, extra: Optional[dict] = None) -> str:
    name = name.strip()
    if not name or len(name) > 120:
        raise HTTPException(status_code=400, detail="A list needs a name of up to 120 characters.")
    props = {"class": "CollectionProperties", "typeName": "WorkingSet",
             "qualifiedName": f"{_PORTAL_LIST_PREFIX}{me}::{_list_slug(name, uuid.uuid4().hex[:6])}",
             "displayName": name, "description": description or ""}
    if extra:
        props["additionalProperties"] = extra
    return await client._async_create_collection(body={"class": "NewElementRequestBody", "properties": props})


@router.post("/api/resource-browser/lists", summary="Create a work list of your own")
async def create_list(body: NewListBody):
    me = _require_signed_in()
    try:
        cm = await _collections_async()
        guid = await _create_list(cm, me, body.name, body.description or "")
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: create list {body.name!r} failed")
    return await get_list(guid)


class EditListBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


@router.put("/api/resource-browser/lists/{guid}", summary="Rename a list of yours or change its description")
async def edit_list(guid: str, body: EditListBody):
    props = {"class": "CollectionProperties"}
    if body.name is not None:
        if not body.name.strip() or len(body.name) > 120:
            raise HTTPException(status_code=400, detail="A list needs a name of up to 120 characters.")
        props["displayName"] = body.name.strip()
    if body.description is not None:
        props["description"] = body.description
    try:
        client = await _explorer_async()
        await _my_list(client, guid)
        cm = await _collections_async()
        await cm._async_update_collection(guid, {"class": "UpdateElementRequestBody", "mergeUpdate": True,
                                                 "properties": props})
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: edit list {guid} failed")
    return await get_list(guid)


class MembersBody(BaseModel):
    guids: list
    rationale: Optional[str] = None


@router.post("/api/resource-browser/lists/{guid}/members", summary="Add resources to a list of yours")
async def add_members(guid: str, body: MembersBody):
    wanted = [g for g in dict.fromkeys(str(x).strip() for x in body.guids) if g]
    if not wanted or len(wanted) > _ADD_CAP:
        raise HTTPException(status_code=400, detail=f"Add between 1 and {_ADD_CAP} resources at a time.")
    try:
        client = await _explorer_async()
        await _my_list(client, guid)
        cm = await _collections_async()
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: add to list {guid} failed")
    failed = {}
    for g in wanted:  # one at a time: CollectionMembership is uni-link, so a repeat leaves one member
        try:
            await cm._async_add_to_collection(guid, g, body=_membership_body((body.rationale or "").strip() or None))
        except Exception as exc:
            failed[g] = str(exc)[:200]
            logger.warning(f"resource-browser: add {g} to list {guid} failed: {exc}")
    out = await get_list(guid)
    if failed:
        data = json.loads(out.body)
        data["failed"] = failed
        return JSONResponse(data, status_code=207)
    return out


@router.delete("/api/resource-browser/lists/{guid}/members/{member_guid}", summary="Remove a resource from a list of yours")
async def remove_member(guid: str, member_guid: str):
    try:
        client = await _explorer_async()
        await _my_list(client, guid)
        cm = await _collections_async()
        await cm._async_remove_from_collection(guid, member_guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: remove {member_guid} from list {guid} failed")
    return await get_list(guid)


class CopyBody(BaseModel):
    members: Optional[list] = None      # the member guids to copy; None copies them all
    name: Optional[str] = None          # a new list's name (when into is not given)
    into: Optional[str] = None          # or the guid of an existing list of yours


@router.post("/api/resource-browser/lists/{guid}/copy",
             summary="Copy members of a list (e.g. from Resource Explorer) into a list of your own")
async def copy_list(guid: str, body: CopyBody):
    me = _require_signed_in()
    try:
        client = await _explorer_async()
        source = await _read_list(client, guid)
    except HTTPException:
        raise
    except Exception as exc:
        _raise_not_visible_or_mapped(exc, f"resource-browser: copy from list {guid} failed")
    src = _list_record(source, me)
    members = {m["guid"]: m for m in _list_members(source)}
    chosen = list(members) if body.members is None else [g for g in dict.fromkeys(body.members) if g in members]
    unknown = [] if body.members is None else [g for g in body.members if g not in members]
    if not chosen:
        raise HTTPException(status_code=400, detail="Choose at least one member of this list to copy.")
    try:
        cm = await _collections_async()
        if body.into:
            await _my_list(client, body.into)
            target = body.into
        else:
            target = await _create_list(
                cm, me, body.name or f"{src['displayName']} (copy)",
                src["description"],
                {"copiedFromGUID": guid, "copiedFromQualifiedName": src["qualifiedName"],
                 "copiedFromName": src["displayName"], "copiedAt": _now_iso()})
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: copy target for list {guid} failed")
    failed = {}
    for g in chosen:
        m = members[g]
        try:
            await cm._async_add_to_collection(target, g, body=_membership_body(m["rationale"] or None, m["confidence"]))
        except Exception as exc:
            failed[g] = str(exc)[:200]
            logger.warning(f"resource-browser: copy {g} into list {target} failed: {exc}")
    out = await get_list(target)
    data = json.loads(out.body)
    data.update(copied=len(chosen) - len(failed), failed=failed, notInSource=unknown)
    return JSONResponse(data, status_code=207 if failed else 200)


# ── Team sharing (spec §5: a list is shared with a Team or Community by a
# ResourceList from that actor profile to the WorkingSet, as RE's investigations do)

_GROUP_TYPES = ("Team", "Community")
_PERSONAS_JSON = _HERE / "personas.json"


def _is_group(type_name: str, super_types: list) -> bool:
    return type_name in _GROUP_TYPES or any(t in (super_types or []) for t in _GROUP_TYPES)


def _shared_with(el: dict) -> list:
    """The Teams and Communities a list is shared with: ResourceList relationships
    whose other end is a group."""
    out = {}
    for val in (el or {}).values():
        if not isinstance(val, list):
            continue
        for item in val:
            rel = _related(item)
            if rel and rel["relationshipType"] == "ResourceList" and _is_group(rel["typeName"], rel["superTypeNames"]):
                out[rel["guid"]] = {"guid": rel["guid"], "displayName": rel["displayName"], "typeName": rel["typeName"]}
    return sorted(out.values(), key=lambda g: g["displayName"].lower())


def _groups_of(person: dict, roles: list) -> list:
    """Groups a person belongs to: those whose AssignmentScope reaches one of the
    person's roles (PersonRoleAppointment), or the person directly."""
    out = {}

    def take(el, via):
        for item in (el or {}).get("assignmentScope") or []:
            rel = _related(item)
            if rel and _is_group(rel["typeName"], rel["superTypeNames"]):
                out.setdefault(rel["guid"], {"guid": rel["guid"], "displayName": rel["displayName"],
                                             "typeName": rel["typeName"], "via": via})
    take(person, "you directly")
    for role in roles:
        take(role, _display_name(role.get("properties"), "a role"))
    return sorted(out.values(), key=lambda g: (g["typeName"], g["displayName"].lower()))


def _persona_display_name(user: str) -> Optional[str]:
    try:
        return (json.loads(_PERSONAS_JSON.read_text()).get(user) or {}).get("display_name")
    except Exception:
        return None


async def _person_of(client, user: str) -> tuple:
    """(person element guid, how it was found) for an Egeria user id, or (None, why not).

    First the identity graph: the UserIdentity with this userId and the profile its
    ProfileIdentity names. Some demo users have no such link, so then an exact
    display-name match against the Portal's persona list, labelled as a match by name."""
    uids = _elements(await client._async_find_elements_by_property_value(
        property_value=user, property_names=["userId"], metadata_element_subtypes=["UserIdentity"],
        starts_with=True, ends_with=True, ignore_case=False, graph_query_depth=0, output_format="JSON"))
    if uids:
        expert = await _expert_async()
        for u in uids:
            res = await expert._async_get_related_metadata_elements(
                u["elementHeader"]["guid"], "ProfileIdentity", {"class": "ResultsRequestBody"}, starting_at_end=0)
            for item in (res or {}).get("elementList") or [] if isinstance(res, dict) else []:
                e = item.get("element") or {}
                if "ActorProfile" in ((e.get("type") or {}).get("superTypeNames") or []):
                    return e.get("elementGUID"), "your user identity's profile"
    name = _persona_display_name(user)
    if name:
        people = [p for p in _elements(await client._async_find_elements_by_property_value(
            property_value=name, property_names=["displayName"], metadata_element_subtypes=["Person"],
            starts_with=True, ends_with=True, ignore_case=False, graph_query_depth=0, output_format="JSON"))]
        if len(people) == 1:
            return people[0]["elementHeader"]["guid"], f"the profile named “{name}” (matched by name: your user identity is not linked to a profile)"
        if len(people) > 1:
            return None, f"{len(people)} profiles are named “{name}”, so yours cannot be told apart"
    return None, "your Egeria user is not linked to a person profile"


async def _groups_value():
    me = _token_user()
    if not me:
        return {"groups": [], "person": None, "how": "not signed in"}
    client = await _explorer_async()
    person_guid, how = await _person_of(client, me)
    if not person_guid:
        return {"groups": [], "person": None, "how": how}
    person = await client._async_get_element_by_guid(person_guid, graph_query_depth=1, output_format="JSON")
    role_guids = [r["guid"] for r in (_related(i) for i in person.get("performsRoles") or []) if r]
    sem = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async def role(g):
        async with sem:
            return await client._async_get_element_by_guid(g, graph_query_depth=1, output_format="JSON")
    roles = [r for r in await asyncio.gather(*(role(g) for g in role_guids), return_exceptions=True) if isinstance(r, dict)]
    return {"groups": _groups_of(person, roles), "how": how, "rolesRead": len(roles), "rolesFound": len(role_guids),
            "person": {"guid": person_guid, "displayName": _display_name(person.get("properties"), person_guid)}}


@router.get("/api/resource-browser/groups", summary="The Teams and Communities you belong to")
async def get_groups():
    try:
        value, stamp = await _cached("groups", _groups_value)
    except Exception as exc:
        raise_egeria_http_error(exc, "resource-browser: group lookup failed")
    return JSONResponse({**value, **_age(stamp),
                         "source": "UserIdentity → ProfileIdentity → Person → PersonRoleAppointment → AssignmentScope"})


class ShareBody(BaseModel):
    group: str


@router.post("/api/resource-browser/lists/{guid}/share", summary="Share a list of yours with a Team or Community you belong to")
async def share_list(guid: str, body: ShareBody):
    try:
        client = await _explorer_async()
        await _my_list(client, guid)
        groups, _ = await _cached("groups", _groups_value)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: share list {guid} failed")
    if body.group not in {g["guid"] for g in groups["groups"]}:
        raise HTTPException(status_code=403, detail="You can share only with a Team or Community you belong to.")
    try:
        cm = await _collections_async()
        await cm._async_attach_collection(body.group, guid)  # ResourceList; uni-link, so a repeat leaves one
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: share list {guid} with {body.group} failed")
    return await get_list(guid)


@router.delete("/api/resource-browser/lists/{guid}/share/{group}", summary="Stop sharing a list of yours with a group")
async def unshare_list(guid: str, group: str):
    try:
        client = await _explorer_async()
        await _my_list(client, guid)
        cm = await _collections_async()
        await cm._async_detach_collection(group, guid)
    except HTTPException:
        raise
    except Exception as exc:
        raise_egeria_http_error(exc, f"resource-browser: unshare list {guid} from {group} failed")
    return await get_list(guid)


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
