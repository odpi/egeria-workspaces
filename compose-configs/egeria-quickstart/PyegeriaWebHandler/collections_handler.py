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
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

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
