"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Collections Explorer — FastAPI router.

A type-agnostic view of the collection landscape: the left nav lists, by
default, every collection with no parent collection (any Collection subtype
whose guid never appears as another collection's member) — this surfaces
collections that were created standalone and never linked under a
RootCollection, not just the ones deliberately classified RootCollection.
An `only_root_type` toggle narrows the list back down to the genuine
RootCollection-typed elements. From any listed collection you can walk the
member hierarchy regardless of the specific collection subtype (DigitalProduct,
DigitalProductFamily, SolutionBlueprint, Folio, plain Collection, …).

Endpoints:
  GET /api/collections/roots          → list parentless (or RootCollection-only) elements (left nav)
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

from digital_products_handler import (
    _get_manager, _serialize_node, _header, _type_name, _extract_all_rels, _is_template,
)
from egeria_error_mapping import raise_egeria_http_error, EGERIA_ERROR_RESPONSES

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


def _rel_guid(entry) -> Optional[str]:
    """Extract the related element's guid from a single RelatedMetadataElementSummary dict."""
    if not isinstance(entry, dict):
        return None
    re = entry.get("relatedElement") or {}
    return (re.get("elementHeader") or {}).get("guid") or None


def _find_all_collections_with_members(mgr) -> list:
    """Page through every Collection (any subtype), depth=1, so each element's own
    `collectionMembers` (its children) comes back embedded in the same call — this is
    what lets us compute "has a parent" for every collection with one paginated scan
    instead of one get_collection_members call per collection.
    """
    all_elements = {}
    start_from = 0
    page_size = 200
    max_pages = 50  # safety cap: 10000 collections max
    for _ in range(max_pages):
        try:
            raw = mgr.find_collections(
                search_string="*",
                starts_with=True,
                ignore_case=True,
                output_format="JSON",
                start_from=start_from,
                page_size=page_size,
                graph_query_depth=1,
            )
        except Exception as exc:
            logger.warning(f"find_collections page {start_from} failed: {exc}")
            break
        if not isinstance(raw, list) or not raw:
            break
        for e in raw:
            g = _header(e).get("guid", "")
            if g and g not in all_elements:
                all_elements[g] = e
        start_from += page_size
    return list(all_elements.values())


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


@router.get("/api/collections/roots", summary="List parentless (or RootCollection-only) elements", responses=EGERIA_ERROR_RESPONSES)
def get_roots(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
    only_root_type: bool = Query(False, description="When True, restrict to the RootCollection open metadata type instead of any parentless collection"),
):
    """Default: every collection (any subtype) that is not itself a member of any
    other collection. When only_root_type=True: just the RootCollection-typed
    elements, as before.
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

    if only_root_type:
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
            raise_egeria_http_error(exc, "RootCollection discovery failed")

        if not include_templates:
            raw = [c for c in raw if isinstance(c, dict) and not _is_template(c)]
        roots = [_serialize_node(c) for c in raw if isinstance(c, dict)]
        roots.sort(key=lambda c: (c.get("displayName") or c.get("qualifiedName") or "").lower())
        return JSONResponse({"roots": roots, "total": len(roots)})

    try:
        all_elements = _find_all_collections_with_members(mgr)
    except Exception as exc:
        raise_egeria_http_error(exc, "Collection discovery failed")

    all_guids = {_header(e).get("guid", ""): e for e in all_elements if _header(e).get("guid")}
    has_parent = set()
    for element in all_elements:
        for entry in (element.get("collectionMembers") or []):
            child_guid = _rel_guid(entry)
            if child_guid and child_guid in all_guids:
                has_parent.add(child_guid)

    parentless = [e for g, e in all_guids.items() if g not in has_parent]
    if not include_templates:
        parentless = [e for e in parentless if not _is_template(e)]
    roots = [_serialize_node(e) for e in parentless]
    roots.sort(key=lambda c: (c.get("displayName") or c.get("qualifiedName") or "").lower())
    return JSONResponse({"roots": roots, "total": len(roots)})


@router.get("/api/collections/{root_guid}/tree", summary="Member hierarchy from a collection", responses=EGERIA_ERROR_RESPONSES)
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
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

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
            summary="Direct members of a collection node (lazy tree loading, PERF-2)",
            responses=EGERIA_ERROR_RESPONSES)
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
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

    cache_key = f"children|{node_guid}|{url or ''}|{server or ''}|{user_id or ''}|{as_of_time or ''}"
    cached = _TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _TREE_CACHE_TTL:
        return JSONResponse(cached[1])

    result = {"children": _children_level(mgr, node_guid, as_of_time)}
    _TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


# Must be registered before GET /api/collections/{node_guid} below — FastAPI/
# Starlette matches routes in declaration order, and a bare "by-type" would
# otherwise be swallowed by {node_guid} as if it were a guid (confirmed live
# 2026-08-14: swapping the order made this 404 with "Node 'by-type' not found").
@router.get("/api/collections/by-type", summary="Existing collections of a given subtype", responses=EGERIA_ERROR_RESPONSES)
def get_collections_by_type(
    type_name: str = Query(..., description="Collection subtype, e.g. DigitalProduct, Agreement, or plain Collection"),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Feeds the Add-to-Collection picker's second step (subtype already chosen
    client-side from the /api/types graph — see egeria-shared-ui.js's
    useTypeGraph/getAllSubs)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

    try:
        # graph_query_depth=0 — live-verified 2026-08-14: the default (3) walks
        # relationships deep enough to hit a stale/orphaned entity reference and
        # 500s (OMRS-REPOSITORY-404-002, "entity ... is not known to the open
        # metadata repository"), and is slow even when it doesn't fail outright
        # (same ~30s-vs-<0.5s tradeoff documented in digital_products_handler.py).
        # This picker only needs flat collection headers, no relationship graph.
        cols = mgr.find_collections(metadata_element_type_name=type_name, output_format="JSON",
                                     page_size=200, graph_query_depth=0)
    except Exception as exc:
        raise_egeria_http_error(exc, f"Failed to find collections of type {type_name}")
    return JSONResponse([_serialize_node(c) for c in cols] if isinstance(cols, list) else [])


class CreateCollectionBody(BaseModel):
    type_name: str
    display_name: str
    description: Optional[str] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/collections", summary="Create a new collection", responses=EGERIA_ERROR_RESPONSES)
def create_collection(body: CreateCollectionBody = Body(...)):
    """Feeds the Add-to-Collection modal's "or create new" option (BACKLOG.md
    Bulk Actions Phase 2). qualifiedName follows the same
    <Kind>::<name>::<suffix> convention insights_handler.py already uses for
    its own create_collection calls (ResultsSet/SavedQuery), generalized to
    an arbitrary subtype/display name instead of hardcoded ones."""
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

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
        raise_egeria_http_error(exc, f"Failed to create collection {body.display_name!r}")

    try:
        raw = mgr.get_collection_by_guid(guid, output_format="JSON")
        node = _serialize_node(raw) if raw else None
    except Exception:
        node = None
    if not node:
        node = {"guid": guid, "typeName": body.type_name, "displayName": body.display_name,
                "qualifiedName": f"{body.type_name}::{body.display_name}::{suffix}"}
    return JSONResponse(node)


@router.get("/api/collections/{node_guid}", summary="Detail for one collection node", responses=EGERIA_ERROR_RESPONSES)
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
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

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


# ── Bulk membership (select N elements elsewhere in the portal, add/remove ──
# them here) — see BACKLOG.md's Bulk Actions / Collection Membership entry
# (2026-08-14) for the design. Partial-failure tolerant by design, same
# pattern as insights_handler.py's saved-query refresh loop: one bad guid
# doesn't fail the whole batch, the response says exactly what happened to
# each one.

class BulkMembershipBody(BaseModel):
    guids: list[str]
    membership_rationale: Optional[str] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/collections/{collection_guid}/members", summary="Add elements to a collection (bulk)", responses=EGERIA_ERROR_RESPONSES)
def add_members(collection_guid: str, body: BulkMembershipBody = Body(...)):
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

    # Re-adding an existing member is a confirmed no-op (live-verified
    # 2026-08-14: no exception, no duplicate relationship) — Egeria itself
    # treats it as idempotent, so there's no "already a member" case to detect
    # here; a guid that doesn't raise always lands in `added`.
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
            failed.append({"guid": guid, "error": str(exc)})
    return JSONResponse({"added": added, "failed": failed})


@router.delete("/api/collections/{collection_guid}/members", summary="Remove elements from a collection (bulk)", responses=EGERIA_ERROR_RESPONSES)
def remove_members(collection_guid: str, body: BulkMembershipBody = Body(...)):
    try:
        mgr = _get_manager(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create CollectionManager")

    removed, failed = [], []
    for guid in body.guids:
        try:
            mgr.remove_from_collection(collection_guid, guid)
            removed.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, see module note above
            logger.debug(f"collections: failed to remove member {guid} from {collection_guid}: {exc}")
            failed.append({"guid": guid, "error": str(exc)})
    return JSONResponse({"removed": removed, "failed": failed})
