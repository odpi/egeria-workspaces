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
from egeria_auth import lineage_key as _lineage_key
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from digital_products_handler import (
    _get_manager, _serialize_node, _header, _type_name, _extract_all_rels, _is_template,
    _extract_mermaid_fields,
)
from egeria_error_mapping import raise_egeria_http_error, describe_bulk_item_error, EGERIA_ERROR_RESPONSES
from egeria_auth import apply_token
from result_cache import credential_identity
import os

router = APIRouter(tags=["collections"])


def _get_solution_architect(url=None, server=None, user_id=None, user_pwd=None):
    """SolutionArchitect client — needed only for _enrich_isc_implementation_graph
    below. CollectionManager's generic get_collection_by_guid hits a plain
    /collections/{guid}/retrieve REST endpoint that never runs the ISC-specific
    server-side mermaid-graph generation, no matter what depth/params are
    passed to it -- that logic only fires behind SolutionArchitect's dedicated
    get_info_supply_chain_by_guid(add_implementation=True) call (see
    isc_handler.py's get_isc, which is where this same graph IS shown today)."""
    from pyegeria import SolutionArchitect
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = SolutionArchitect(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


# Same generous caps isc_handler.py uses for its (structurally identical)
# detail view -- this is a "show me everything about one chain" fetch.
_ISC_ENRICH_GRAPH_QUERY_DEPTH = 10
_ISC_ENRICH_MAX_MERMAID_NODES = 250


def _enrich_isc_implementation_graph(node: dict, node_guid: str, url, server, user_id, user_pwd) -> None:
    """When a collection reached through this type-agnostic view turns out to
    be an InformationSupplyChain, fetch its implementation graph the way
    isc_handler.py's own detail view does and merge the mermaid fields in --
    otherwise Collections shows every diagram EXCEPT this one for an ISC,
    while Solution Architect's own ISC view (isc_handler.py) shows it fine.
    Best-effort: any failure here just leaves the collection's other detail
    (properties, members, relationships) intact, unenriched."""
    if node.get("typeName") != "InformationSupplyChain":
        return
    try:
        mgr = _get_solution_architect(url, server, user_id, user_pwd)
        raw = mgr.get_info_supply_chain_by_guid(
            node_guid,
            output_format="JSON",
            add_implementation=True,
            graph_query_depth=_ISC_ENRICH_GRAPH_QUERY_DEPTH,
            max_mermaid_node_count=_ISC_ENRICH_MAX_MERMAID_NODES,
        )
    except Exception:
        logger.exception("ISC implementation-graph enrichment failed for %s", node_guid)
        return
    if isinstance(raw, dict):
        extracted = _extract_mermaid_fields(raw)
        # get_info_supply_chain_by_guid returns this key in a different case
        # than find_information_supply_chains does (isc_handler.py's list/detail
        # calls) -- "iscimplementationMermaidGraph" vs "iscImplementationMermaidGraph".
        # Harmless either way (AvailableMermaidDiagrams matches case-insensitively),
        # but the frontend's auto-generated label falls back to an ugly
        # "Iscimplementation Graph" without the canonical casing, since it can't
        # find an exact match in its nice-label lookup table. Canonicalize so the
        # label matches what isc_handler.py's own detail view already shows.
        for k in list(extracted.keys()):
            if k.lower() == "iscimplementationmermaidgraph" and k != "iscImplementationMermaidGraph":
                extracted["iscImplementationMermaidGraph"] = extracted.pop(k)
        node.update(extracted)


def _get_expert(url=None, server=None, user_id=None, user_pwd=None):
    """MetadataExpert client — used alongside _get_manager's CollectionManager
    for the one thing CollectionManager can't do: a flat relationship-type
    search (find_relationships_between_elements), needed by
    _find_all_collections_with_members's PERF-3 rewrite below."""
    from pyegeria import MetadataExpert
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    expert = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(expert)
    return expert


# Tree cache: cache_key → (timestamp, result). 5-minute TTL, like digital products.
_TREE_CACHE: dict = {}
_TREE_CACHE_TTL = 300  # seconds

# Roots cache: same TTL/shape as _TREE_CACHE. See _find_all_collections_with_
# members's PERF-3 docstring below for why the default (non only_root_type)
# path used to be expensive (~46s confirmed live 2026-09-02) and how it was
# fixed. Only Egeria Explorer's Collections tab calls this endpoint, but it
# re-fetches on every tab visit, so the cache still matters even post-fix.
_ROOTS_CACHE: dict = {}
_ROOTS_CACHE_TTL = 300  # seconds


def _is_collection(node: dict) -> bool:
    """A node can be navigated into iff it is a Collection (any subtype)."""
    if "Collection" in (node.get("superTypeNames") or []):
        return True
    tn = node.get("typeName") or ""
    return tn == "Collection" or tn.endswith("Collection")


def _find_all_collections_with_members(mgr, url=None, server=None, user_id=None, user_pwd=None,
                                       with_parents: bool = True) -> tuple:
    """Return (all Collection elements, set of guids that have a parent, status).

    `status` says how far to trust the first two, so the UI never shows a partial list as the whole
    one: {"capped": the page loop hit max_pages (more collections exist), "incomplete": a page failed
    (the list stops early), "parentsKnown": the CollectionMembership read succeeded and was not cut off
    (when False, "has a parent" is unknown, and every collection looks parentless)}. With
    with_parents=False the relationship read is skipped (parentsKnown is then False by definition).

    PERF-3: was a single depth=1 scan over every Collection, each fetch
    embedding that element's own `collectionMembers` — confirmed live
    2026-09-02 at 46.6s cold with ~470 collections in the store (worse than
    the ~8.5s measured 2026-08-26, as the collection count grew since).
    Replaced with two independent flat calls, live-measured combined at
    ~13s: every Collection at graph_query_depth=0 via the same
    find_collections already used by the RootCollection-only path above (no
    nested member embedding — 472 elements in ~3s), plus every
    CollectionMembership relationship via MetadataExpert
    (relationshipTypeName filter, not a per-collection walk — 970
    relationships in ~9-10s), from which "has a parent" is just membership
    in the set of member-end guids.

    Why "has a parent" is only a best effort (checked live 2026-11-09): CollectionMembership holds
    thousands of relationships, because collections contain assets, terms and everything else, not only
    collections, and a page comes back SHORT (984 of 1000) with far more after it. Egeria also now refuses
    pageSize > 1000 (OMAG-COMMON-400-010), which made the old page_size=2000 read fail so every collection
    looked parentless. Reading all of them is ~10 s per 1000 (minutes in total), so this reads ONE page of
    1000 and says parentsKnown=False: the parent set is partial. The type-grouped list does not need it
    and passes with_parents=False.
    """
    all_elements = {}
    start_from = 0
    # Egeria's maximum page is 1000 (OMAG-COMMON-400-010 above it). Measured live 2026-11-09 at depth 0:
    # 200 rows 1.5 s, 500 rows 3.7 s, 1000 rows 3.8 s, so a 1000-row page costs about what a 500-row one does.
    # Still only an EMPTY page ends the read (a short page is not the last one).
    page_size = 1000
    max_pages = 10  # safety cap: 10000 collections max
    status = {"capped": False, "incomplete": False, "parentsKnown": True}
    for page_no in range(max_pages):
        try:
            raw = mgr.find_collections(
                search_string="*",
                starts_with=True,
                ignore_case=True,
                output_format="JSON",
                start_from=start_from,
                page_size=page_size,
                graph_query_depth=0,
            )
        except Exception as exc:
            logger.warning(f"find_collections page {start_from} failed: {exc}")
            status["incomplete"] = True
            break
        if not isinstance(raw, list) or not raw:
            break
        for e in raw:
            g = _header(e).get("guid", "")
            if g and g not in all_elements:
                all_elements[g] = e
        start_from += page_size
        if page_no == max_pages - 1:
            status["capped"] = True      # every page was non-empty: there may be more

    has_parent = set()
    status["parentsKnown"] = False         # see the docstring: one page cannot establish "no parent"
    if with_parents:
        try:
            expert = _get_expert(url, server, user_id, user_pwd)
            body = {"class": "FindRelationshipRequestBody", "relationshipTypeName": "CollectionMembership"}
            res = expert.find_relationships_between_elements(body, start_from=0, page_size=1000)
            rels = res.get("relationships", []) if isinstance(res, dict) else res
            if isinstance(rels, list):
                for r in rels:
                    # end2 = the member (role2 "collectionMembers"); a flat guid field on the relationship
                    member_guid = r.get("elementGUIDAtEnd2")
                    if member_guid:
                        has_parent.add(member_guid)
        except Exception as exc:
            logger.warning(f"CollectionMembership relationship fetch failed: {exc}")

    return list(all_elements.values()), has_parent, status


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


_SUMMARY_DESCRIPTION_CHARS = 200


def _summarize_node(node: dict) -> dict:
    """The few fields the type-grouped list and the tree's top node read. The full node (properties,
    classifications, mermaid graphs...) averaged 1.9 KB and reached 19 KB; 1,840 of them were 3.2 MB.
    The detail pane fetches the full element by guid when a collection is selected."""
    desc = node.get("description") or ""
    if len(desc) > _SUMMARY_DESCRIPTION_CHARS:
        desc = desc[:_SUMMARY_DESCRIPTION_CHARS].rstrip() + "…"
    return {
        "guid":           node.get("guid", ""),
        "typeName":       node.get("typeName", ""),
        "superTypeNames": node.get("superTypeNames") or [],
        "displayName":    node.get("displayName", ""),
        "qualifiedName":  node.get("qualifiedName", ""),
        "description":    desc,
    }


@router.get("/api/collections/roots", summary="List parentless (or RootCollection-only) elements", responses=EGERIA_ERROR_RESPONSES)
def get_roots(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
    only_root_type: bool = Query(False, description="When True, restrict to the RootCollection open metadata type instead of any parentless collection"),
    all_collections: bool = Query(False, description="When True, return EVERY collection (any subtype) as summary rows (guid, typeName, names, a short description) without working out parents (fast), for the type-grouped list"),
    parentless: bool = Query(False, description="Opt in to the OLD 'collections without a parent' answer. It costs ~10 s and is only a best effort (parentsKnown=false): CollectionMembership is too big to read in full. Without this flag, and without only_root_type, the answer is all_collections."),
):
    """Default: every collection (any subtype) that is not itself a member of any
    other collection. When only_root_type=True: just the RootCollection-typed
    elements, as before. When all_collections=True, or when no mode is given: every collection as
    summary rows, no parent test (fast). parentless=True opts in to the slow, partial parent test.

    Besides roots/total the answer says whether the list is the whole story: `capped` (more exist
    than were read), `complete` (false if a page failed), `parentsKnown` (false: parentless is a best effort).
    """
    if not only_root_type and not parentless:
        all_collections = True          # the default: the cheap, complete answer
    return JSONResponse(_roots_payload(url, server, user_id, user_pwd, include_templates, only_root_type, all_collections))


def _roots_cache_key(url, server, user_id, user_pwd, include_templates, only_root_type, all_collections) -> str:
    """Who asked (the credential PRESENTED, hashed, never a bare user_id: see result_cache.credential_identity),
    what they asked for, and the forLineage toggle. The warm-up builds its keys with this too."""
    from egeria_auth import get_request_token
    identity = credential_identity(get_request_token(), user_id, user_pwd, os.environ.get("EGERIA_USER", "erinoverview"))
    return f"{url or ''}|{server or ''}|{identity}|{include_templates}|{only_root_type}|{all_collections}{_lineage_key()}"


def _roots_payload(url, server, user_id, user_pwd, include_templates, only_root_type, all_collections) -> dict:
    """The roots answer, from the cache when fresh. Raises HTTPException on a failure; a partial answer is
    returned but never cached. Shared by the route and the startup warm-up."""
    from egeria_auth import _token_expired, get_request_token
    token = get_request_token()
    use_cache = not (token and _token_expired(token))    # an expired token must reach Egeria and be refused
    cache_key = _roots_cache_key(url, server, user_id, user_pwd, include_templates, only_root_type, all_collections)
    cached = _ROOTS_CACHE.get(cache_key) if use_cache else None
    if cached and (time.time() - cached[0]) < _ROOTS_CACHE_TTL:
        return cached[1]

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
                metadata_element_type="RootCollection",
            )
        except Exception as exc:
            raise_egeria_http_error(exc, "RootCollection discovery failed")

        if not include_templates:
            raw = [c for c in raw if isinstance(c, dict) and not _is_template(c)]
        roots = [_serialize_node(c) for c in raw if isinstance(c, dict)]
        roots.sort(key=lambda c: (c.get("displayName") or c.get("qualifiedName") or "").lower())
        result = {"roots": roots, "total": len(roots), "capped": len(raw) >= 500, "complete": True,
                  "parentsKnown": True}
        if use_cache: _ROOTS_CACHE[cache_key] = (time.time(), result)
        return result

    try:
        all_elements, has_parent, status = _find_all_collections_with_members(
            mgr, url, server, user_id, user_pwd, with_parents=not all_collections)
    except Exception as exc:
        raise_egeria_http_error(exc, "Collection discovery failed")

    all_guids = {_header(e).get("guid", ""): e for e in all_elements if _header(e).get("guid")}
    chosen = list(all_guids.items()) if all_collections else [(g, e) for g, e in all_guids.items() if g not in has_parent]
    if not include_templates:
        chosen = [(g, e) for g, e in chosen if not _is_template(e)]
    roots = [_summarize_node(_serialize_node(e)) if all_collections else _serialize_node(e) for g, e in chosen]
    roots.sort(key=lambda c: (c.get("displayName") or c.get("qualifiedName") or "").lower())
    result = {"roots": roots, "total": len(roots), "capped": status["capped"],
              "complete": not status["incomplete"], "parentsKnown": status["parentsKnown"]}
    if result["complete"]:      # a partial answer is served, not remembered
        if use_cache: _ROOTS_CACHE[cache_key] = (time.time(), result)
    return result


def warm_roots_cache() -> None:
    """Fill the all-collections list cache for the Portal's own service user, for BOTH forLineage settings,
    so the first visitor after a restart rarely waits ~8-11 s. The Promise/Memento toggle defaults ON in
    the browser (egeriaFetch then sends X-Egeria-For-Lineage: true, a different cache key and a different,
    larger list), so that key is warmed first, then the OFF key, one after the other. Each pass runs inside
    egeria_auth.lineage_scope, i.e. the same state the middleware sets per request.

    Runs in a daemon thread (sync pyegeria is only safe off the event loop), never blocks startup, and logs
    one line per pass. A failure, or a partial answer, is logged and NOT cached (_roots_payload stores only
    complete answers), so a warm-up while Egeria is still coming up leaves the cache empty, not wrong."""
    from egeria_auth import lineage_scope
    for lineage in (True, False):
        started = time.time()
        try:
            with lineage_scope(lineage):
                result = _roots_payload(None, None, None, None, False, False, True)
            took = time.time() - started
            logger.info(f"collections: warmed the type-grouped list (forLineage={'on' if lineage else 'off'}): "
                        f"{result['total']} collections in {took:.1f}s ({'cached' if result['complete'] else 'partial, not cached'})")
        except Exception as exc:  # noqa: BLE001 -- warm-up is best effort
            logger.warning(f"collections: list warm-up (forLineage={'on' if lineage else 'off'}) failed after "
                           f"{time.time() - started:.1f}s (nothing cached): {exc}")
