"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Collections Explorer — FastAPI router.

A type-agnostic view of the collection landscape: the left nav lists the
RootCollection elements (the genuine top-level collections, identified by the
RootCollection open metadata type), and from each root you can walk the member
hierarchy regardless of the specific collection subtype (DigitalProduct,
DigitalProductFamily, SolutionBlueprint, Folio, plain Collection, …).

Endpoints:
  GET /api/collections/roots          → list RootCollection elements (left nav)
  GET /api/collections/{guid}/tree     → recursive member hierarchy from a root
  GET /api/collections/{guid}          → detail for one collection node

Builds on the proven member-recursion in digital_products_handler; the only
behavioural difference is that *any* Collection subtype counts as a container,
so the tree is not limited to the digital-product container types.
"""

import time
import uuid
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_error_mapping import describe_bulk_item_error

from digital_products_handler import (
    _get_manager, _serialize_node, _header, _type_name, _extract_all_rels, _is_template,
)

router = APIRouter(tags=["collections"])

# Tree cache: cache_key → (timestamp, result). 5-minute TTL, like digital products.
_TREE_CACHE: dict = {}
_TREE_CACHE_TTL = 300  # seconds


def _is_collection(node: dict) -> bool:
    """A node can be navigated into iff it is a Collection (any subtype)."""
    if "Collection" in (node.get("superTypeNames") or []):
        return True
    tn = node.get("typeName") or ""
    return tn == "Collection" or tn.endswith("Collection")


def _children_level(mgr, collection_guid: str, as_of_time: Optional[str] = None) -> list:
    """Fetch ONE level of members (no recursion) for lazy tree loading (PERF-2).

    Each Collection subtype is flagged isContainer so the frontend shows an expand
    twistie; its own children are fetched on demand via /children. Replaces the old
    recursive serial walk that made deep collection trees slow to load.
    """
    try:
        body = {"class": "ResultsRequestBody", "graphQueryDepth": 0}
        if as_of_time:
            body["asOfTime"] = as_of_time  # point-in-time (LE-3); Egeria filters members
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            page_size=200,
            body=body,
        )
    except Exception as exc:
        logger.warning(f"get_collection_members failed for {collection_guid}: {exc}")
        return []

    if not isinstance(raw, list):
        return []

    nodes = []
    for element in raw:
        node = _serialize_node(element)
        node["isContainer"] = _is_collection(node)
        node["children"] = []  # lazily fetched on expand via /children
        nodes.append(node)

    nodes.sort(key=lambda n: (not n["isContainer"], (n.get("displayName") or "").lower()))
    return nodes


@router.get("/api/collections/roots", summary="List RootCollection elements")
def get_roots(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """Return the RootCollection-typed collections that anchor the hierarchy."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_collections(
            search_string="*",
            starts_with=True,
            ignore_case=True,
            output_format="JSON",
            start_from=0,
            page_size=500,
            graph_query_depth=0,
            metadata_element_type_name="RootCollection",
        )
    except Exception as exc:
        logger.exception("RootCollection discovery failed")
        raise HTTPException(status_code=500, detail=f"Root retrieval failed: {exc}")

    if not include_templates:
        raw = [c for c in raw if isinstance(c, dict) and not _is_template(c)]
    roots = [_serialize_node(c) for c in raw if isinstance(c, dict)]
    roots.sort(key=lambda c: (c.get("displayName") or c.get("qualifiedName") or "").lower())
    return JSONResponse({"roots": roots, "total": len(roots)})


@router.get("/api/collections/{root_guid}/tree", summary="Member hierarchy from a collection")
def get_tree(
    root_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """Recursive member hierarchy beneath a collection (any subtype is a container)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    cache_key = f"{root_guid}|{url or ''}|{server or ''}|{user_id or ''}|{as_of_time or ''}"
    cached = _TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _TREE_CACHE_TTL:
        return JSONResponse(cached[1])

    # The root's own metadata is already known to the client from the roots list,
    # so skip the expensive get_collection_by_guid graph query here (PERF-1).
    root = {"guid": root_guid}
    children = _children_level(mgr, root_guid, as_of_time)

    result = {"root": root, "children": children}
    _TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


@router.get("/api/collections/{node_guid}/children",
            summary="Direct members of a collection node (lazy tree loading, PERF-2)")
def get_node_children(
    node_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """One level of children for a container node, fetched when the user expands it."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    cache_key = f"children|{node_guid}|{url or ''}|{server or ''}|{user_id or ''}|{as_of_time or ''}"
    cached = _TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _TREE_CACHE_TTL:
        return JSONResponse(cached[1])

    result = {"children": _children_level(mgr, node_guid, as_of_time)}
    _TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


@router.get("/api/collections/{node_guid}", summary="Detail for one collection node")
def get_node(
    node_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Detail for a single collection node: properties, members, relationships."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    raw = None
    try:
        raw = mgr.get_collection_by_guid(node_guid, output_format="JSON")
    except Exception:
        pass
    if not raw:
        # Non-collection member (e.g. an asset) — fall back to the digital-products node lookup.
        from digital_products_handler import get_node as dp_get_node
        return dp_get_node(node_guid, url, server, user_id, user_pwd)

    node = _serialize_node(raw)
    node["relationships"] = _extract_all_rels(raw)
    try:
        raw_members = mgr.get_collection_members(
            collection_guid=node_guid,
            output_format="JSON",
            page_size=200,
            body={"class": "ResultsRequestBody", "graphQueryDepth": 0},
        )
    except Exception:
        raw_members = []
    node["children"] = [_serialize_node(m) for m in raw_members] if isinstance(raw_members, list) else []
    return JSONResponse(node)


@router.get("/api/collections/by-type", summary="Existing collections of a given subtype")
def get_collections_by_type(
    type_name: str = Query(..., description="Collection subtype, e.g. DigitalProduct, Agreement, or plain Collection"),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Feeds the Add-to-Collection picker's second step (subtype already chosen
    client-side from the /api/types graph — see egeria-shared-ui.js's
    useTypeGraph/getAllSubs). Ported from quickstart's collections_handler.py
    (bulk-action sync, 2026-08-15)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        # graph_query_depth=0 — same tradeoff documented in digital_products_handler.py:
        # this picker only needs flat collection headers, no relationship graph.
        cols = mgr.find_collections(metadata_element_type_name=type_name, output_format="JSON",
                                     page_size=200, graph_query_depth=0)
    except Exception as exc:
        logger.exception(f"Failed to find collections of type {type_name}")
        raise HTTPException(status_code=500, detail=f"Failed to find collections of type {type_name}: {exc}")
    return JSONResponse([_serialize_node(c) for c in cols] if isinstance(cols, list) else [])


class CreateCollectionBody(BaseModel):
    type_name: str
    display_name: str
    description: Optional[str] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/collections", summary="Create a new collection")
def create_collection(body: CreateCollectionBody = Body(...)):
    """Feeds the Add-to-Collection modal's "or create new" option. qualifiedName
    follows the same <Kind>::<name>::<suffix> convention used elsewhere for
    generated collections, generalized to an arbitrary subtype/display name.
    Ported from quickstart's collections_handler.py (bulk-action sync, 2026-08-15)."""
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    suffix = uuid.uuid4().hex[:8]
    try:
        guid = mgr.create_collection(body={
            "class": "NewElementRequestBody",
            "isOwnAnchor": True,
            "properties": {
                "class": "CollectionProperties",
                "typeName": body.type_name,
                "qualifiedName": f"{body.type_name}::{body.display_name}::{suffix}",
                "displayName": body.display_name,
                "description": body.description or "",
            },
        })
    except Exception as exc:
        logger.exception(f"Failed to create collection {body.display_name!r}")
        raise HTTPException(status_code=500, detail=f"Failed to create collection {body.display_name!r}: {exc}")

    try:
        raw = mgr.get_collection_by_guid(guid, output_format="JSON")
        node = _serialize_node(raw) if raw else None
    except Exception:
        node = None
    if not node:
        node = {"guid": guid, "typeName": body.type_name, "displayName": body.display_name,
                "qualifiedName": f"{body.type_name}::{body.display_name}::{suffix}"}
    return JSONResponse(node)


# ── Bulk membership (select N elements elsewhere in the portal, add/remove ──
# them here) — ported from quickstart's collections_handler.py (bulk-action
# sync, 2026-08-15). Partial-failure tolerant by design: one bad guid doesn't
# fail the whole batch, the response says exactly what happened to each one.

class BulkMembershipBody(BaseModel):
    guids: list[str]
    membership_rationale: Optional[str] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/collections/{collection_guid}/members", summary="Add elements to a collection (bulk)")
def add_members(collection_guid: str, body: BulkMembershipBody = Body(...)):
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # Re-adding an existing member is a confirmed no-op (no exception, no
    # duplicate relationship) — Egeria itself treats it as idempotent, so
    # there's no "already a member" case to detect here; a guid that doesn't
    # raise always lands in `added`.
    added, failed = [], []
    for guid in body.guids:
        try:
            mgr.add_to_collection(collection_guid, guid, body={
                "class": "NewRelationshipRequestBody",
                "properties": {
                    "class": "CollectionMembershipProperties",
                    "membershipRationale": body.membership_rationale or "Added via bulk selection",
                },
            })
            added.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, see module note above
            logger.debug(f"collections: failed to add member {guid} to {collection_guid}: {exc}")
            failed.append({"guid": guid, "error": describe_bulk_item_error(exc)})
    return JSONResponse({"added": added, "failed": failed})


@router.delete("/api/collections/{collection_guid}/members", summary="Remove elements from a collection (bulk)")
def remove_members(collection_guid: str, body: BulkMembershipBody = Body(...)):
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    removed, failed = [], []
    for guid in body.guids:
        try:
            mgr.remove_from_collection(collection_guid, guid)
            removed.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, see module note above
            logger.debug(f"collections: failed to remove member {guid} from {collection_guid}: {exc}")
            failed.append({"guid": guid, "error": describe_bulk_item_error(exc)})
    return JSONResponse({"removed": removed, "failed": failed})
