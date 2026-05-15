"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Digital Products Explorer — FastAPI router.

Uses CollectionManager (not ProductManager) which has collection_command_root
and therefore supports get_collection_members correctly.

Endpoints:
  GET /api/digital-products/catalogs              → list DigitalProductCatalog elements
  GET /api/digital-products/catalogs/{guid}/tree  → full hierarchy tree for a catalog
  GET /api/digital-products/{guid}                → detail for any collection/product node
"""

import os

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["digital-products"])

# Types that act as containers (recurse into them when building the tree)
_CONTAINER_TYPES = {
    "DigitalProductCatalog", "DigitalProductFamily",
    "Collection", "RootCollection", "FolderCollection",
    "DataSpecCollection", "DataDictionary",
}


def _get_manager():
    from pyegeria import CollectionManager
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = CollectionManager(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _serialize_node(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    tn = _type_name(element)
    return {
        "guid":             header.get("guid", ""),
        "typeName":         tn,
        "displayName":      props.get("displayName", "") or props.get("name", "") or "",
        "qualifiedName":    props.get("qualifiedName", "") or "",
        "description":      props.get("description", "") or "",
        "productName":      props.get("productName", "") or "",
        "productType":      props.get("productType", "") or "",
        "maturity":         props.get("maturity", "") or "",
        "serviceLife":      props.get("serviceLife", "") or "",
        "introductionDate": props.get("introductionDate", "") or "",
        "nextVersionDate":  props.get("nextVersionDate", "") or "",
        "withdrawalDate":   props.get("withdrawalDate", "") or "",
        "currentVersion":   props.get("currentVersion", "") or "",
        "deploymentStatus": props.get("deploymentStatus", "") or "",
        "status":           header.get("status", "") or "",
    }


def _find_all_catalogs(mgr) -> list:
    """
    Paginate through all collections and return those with typeName == DigitalProductCatalog.
    graph_query_depth=0 avoids deep relationship traversal, cutting per-page time from ~30s to <0.5s.
    Egeria may return fewer items than page_size even on non-last pages, so we only stop
    when we receive an empty page (not when len < page_size).
    """
    catalogs = {}
    start_from = 0
    page_size  = 100
    max_pages  = 50  # safety cap: 5000 collections max
    for _ in range(max_pages):
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
            break
        if not isinstance(raw, list) or not raw:
            break  # empty page → done
        for c in raw:
            if _type_name(c) == "DigitalProductCatalog":
                g = _header(c).get("guid", "")
                if g and g not in catalogs:
                    catalogs[g] = c
        start_from += page_size

    return list(catalogs.values())


def _build_tree(mgr, collection_guid: str, visited: set, depth: int = 0) -> list:
    """Recursively fetch collection members, building a node tree. Max depth 5."""
    if depth > 5 or collection_guid in visited:
        return []
    visited.add(collection_guid)

    try:
        raw = mgr.get_collection_members(
            collection_guid=collection_guid,
            output_format="JSON",
            page_size=200,
            body={"class": "ResultsRequestBody", "graphQueryDepth": 0},
        )
    except Exception as exc:
        logger.warning(f"get_collection_members failed for {collection_guid}: {exc}")
        return []

    if not isinstance(raw, list):
        return []

    nodes = []
    for element in raw:
        node = _serialize_node(element)
        tn = node["typeName"]
        is_container = tn in _CONTAINER_TYPES or "Family" in tn or "Catalog" in tn
        if is_container:
            node["children"] = _build_tree(mgr, node["guid"], visited, depth + 1)
            node["isContainer"] = True
        else:
            node["children"] = []
            node["isContainer"] = False
        nodes.append(node)

    nodes.sort(key=lambda n: (not n["isContainer"], (n.get("displayName") or "").lower()))
    return nodes


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/digital-products/catalogs", summary="List DigitalProductCatalog elements")
def get_catalogs(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(100, ge=1, le=500),
):
    """Return all DigitalProductCatalog collections (paginated through all available collections)."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw_catalogs = _find_all_catalogs(mgr)
    except Exception as exc:
        logger.exception("Catalog discovery failed")
        raise HTTPException(status_code=500, detail=f"Catalog retrieval failed: {exc}")

    catalogs = [_serialize_node(c) for c in raw_catalogs]
    catalogs.sort(key=lambda c: (c.get("displayName") or "").lower())
    return JSONResponse({"catalogs": catalogs, "total": len(catalogs)})


@router.get("/api/digital-products/catalogs/{catalog_guid}/tree",
            summary="Full hierarchy tree for a catalog")
def get_catalog_tree(catalog_guid: str):
    """
    Return the full recursive hierarchy tree for a DigitalProductCatalog.

    Tree nodes: {guid, typeName, displayName, ..., isContainer: bool, children: [node...]}
    """
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        catalog_raw = mgr.get_collection_by_guid(catalog_guid, output_format="JSON")
    except Exception as exc:
        logger.warning(f"get_collection_by_guid failed for {catalog_guid}: {exc}")
        catalog_raw = None

    catalog = _serialize_node(catalog_raw) if catalog_raw and isinstance(catalog_raw, dict) else {"guid": catalog_guid}

    visited: set = set()
    children = _build_tree(mgr, catalog_guid, visited)

    return JSONResponse({"catalog": catalog, "children": children})


@router.get("/api/digital-products/{node_guid}", summary="Get detail for any product/collection node")
def get_node(node_guid: str):
    """Return detail for a single digital product or family node."""
    try:
        mgr = _get_manager()
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_collection_by_guid(node_guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_collection_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Node retrieval failed: {exc}")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Node {node_guid!r} not found")

    return JSONResponse(_serialize_node(raw))
