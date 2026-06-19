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
from egeria_auth import apply_token
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

# Tree cache: guid → (timestamp, result). Invalidated after 5 minutes.
_TREE_CACHE: dict = {}
_TREE_CACHE_TTL = 300  # seconds

router = APIRouter(tags=["digital-products"])

# Types that act as containers (recurse into them when building the tree)
_CONTAINER_TYPES = {
    "DigitalProductCatalog", "DigitalProductFamily",
    "Collection", "RootCollection", "FolderCollection",
    "DataSpecCollection", "DataDictionary",
    "DigitalProduct", "TabularDataSetCollection",
}


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import CollectionManager
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = CollectionManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


_DP_SKIP_KEYS = {"elementHeader", "properties"}

_DP_MERMAID_FIELDS = [
    "mermaidGraph", "collectionMermaidMindMap", "edgeMermaidGraph",
    "anchorMermaidGraph", "specificationMermaidGraph",
    "iscImplementationMermaidGraph", "informationSupplyChainMermaidGraph",
    "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "actionMermaidGraph", "localLineageGraph", "fieldLevelLineageGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph",
    "zoneProfileMermaidPieChart", "zoneProfileAnchoredMermaidPieChart",
    "zoneProfileAllPieChart", "userAccountTypeProfileMermaidPieChart",
    "userAccountStatusMermaidPieChart",
]


def _is_mermaid_key(key: str) -> bool:
    kl = key.lower()
    return ("mermaid" in kl or kl.endswith("graph") or kl.endswith("mindmap")
            or kl.endswith("piechart") or kl.endswith("chart"))


def _extract_mermaid_fields(element: dict) -> dict:
    """Pass through ANY non-empty mermaid-graph string field (generic — not a
    fixed allow-list), so new/rare diagram fields surface automatically."""
    result = {}
    for k, v in element.items():
        if isinstance(v, str) and v.strip() and not v.lower().startswith("no ") and _is_mermaid_key(k):
            result[k] = v
    return result


# Scalar property keys already surfaced in the node header / as named fields —
# excluded from the generic `props` pass-through to avoid duplication.
_PROP_SKIP = {"displayName", "name", "qualifiedName", "description", "class", "typeName"}


def _extract_props(props: dict) -> dict:
    """All remaining scalar properties (str/num/bool), so the detail can show the
    full property set rather than a curated product-specific subset."""
    out = {}
    for k, v in (props or {}).items():
        if k in _PROP_SKIP:
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            out[k] = v
        elif isinstance(v, str) and v.strip():
            out[k] = v
    return out


def _extract_all_rels(element: dict) -> dict:
    """Extract all relationship lists from an element → {key: [{guid, displayName, qualifiedName, typeName}]}."""
    result = {}
    for key, val in element.items():
        if key in _DP_SKIP_KEYS or not isinstance(val, list) or not val:
            continue
        items = []
        for entry in val:
            re = entry.get("relatedElement") or entry
            rh = re.get("elementHeader") or {}
            rp = re.get("properties") or {}
            g  = rh.get("guid") or re.get("guid") or ""
            if g:
                rtype = rh.get("type") or {}
                items.append({
                    "guid":           g,
                    "displayName":    rp.get("displayName") or rp.get("name") or "",
                    "qualifiedName":  rp.get("qualifiedName") or "",
                    "typeName":       rtype.get("typeName") or "",
                    "superTypeNames": rtype.get("superTypeNames") or [],
                })
        if items:
            result[key] = items
    return result


def _serialize_node(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    tn = _type_name(element)
    node = {
        "guid":             header.get("guid", ""),
        "typeName":         tn,
        "superTypeNames":   (header.get("type") or {}).get("superTypeNames") or [],
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
        "props":            _extract_props(props),
    }
    node.update(_extract_mermaid_fields(element))
    return node


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
                sequencing_order="PROPERTY_ASCENDING",
                sequencing_property="displayName",
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
        # Any Collection subtype is a container (Glossary, CollectionFolder, …),
        # not just the explicitly-listed digital-product types — otherwise those
        # nodes show no expand twistie and their members are never fetched.
        is_container = (
            tn in _CONTAINER_TYPES or "Family" in tn or "Catalog" in tn
            or "Collection" in (node.get("superTypeNames") or [])
        )
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
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return all DigitalProductCatalog collections (paginated through all available collections)."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
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
def get_catalog_tree(
    catalog_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """
    Return the full recursive hierarchy tree for a DigitalProductCatalog.

    Tree nodes: {guid, typeName, displayName, ..., isContainer: bool, children: [node...]}
    """
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    cache_key = f"{catalog_guid}|{url or ''}|{server or ''}|{user_id or ''}"
    cached = _TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _TREE_CACHE_TTL:
        logger.debug(f"Tree cache hit for {catalog_guid}")
        return JSONResponse(cached[1])

    try:
        catalog_raw = mgr.get_collection_by_guid(catalog_guid, output_format="JSON")
    except Exception as exc:
        logger.warning(f"get_collection_by_guid failed for {catalog_guid}: {exc}")
        catalog_raw = None

    catalog = _serialize_node(catalog_raw) if catalog_raw and isinstance(catalog_raw, dict) else {"guid": catalog_guid}

    visited: set = set()
    children = _build_tree(mgr, catalog_guid, visited)

    result = {"catalog": catalog, "children": children}
    _TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


@router.get("/api/digital-products/{node_guid}", summary="Get detail for any product/collection node")
def get_node(
    node_guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return detail for a single digital product, family, or asset node.

    Tries CollectionManager first (covers all Collection subtypes). If the node is
    a non-collection asset (e.g. TabularDataSet), falls back to AssetMaker.get_asset_by_guid.
    """
    url_val  = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    svr_val  = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    uid      = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    pwd      = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")

    try:
        mgr = _get_manager(url_val, svr_val, uid, pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    raw = None
    try:
        raw = mgr.get_collection_by_guid(node_guid, output_format="JSON")
    except Exception:
        pass  # not a collection — try asset fallback below

    if not raw:
        # Non-collection asset (e.g. TabularDataSet) — fetch via AssetMaker
        try:
            from pyegeria import AssetMaker
            am = AssetMaker(view_server=svr_val, platform_url=url_val, user_id=uid, user_pwd=pwd)
            apply_token(am)
            raw = am.get_asset_by_guid(node_guid, output_format="JSON")
        except Exception as exc:
            logger.exception("AssetMaker.get_asset_by_guid failed")

    if not raw:
        raise HTTPException(status_code=404, detail=f"Node {node_guid!r} not found")

    node = _serialize_node(raw)
    node["relationships"] = _extract_all_rels(raw)

    # Fetch direct members so the detail is usable when navigated directly (not via tree)
    try:
        raw_members = mgr.get_collection_members(
            collection_guid=node_guid,
            output_format="JSON",
            page_size=200,
            body={"class": "ResultsRequestBody", "graphQueryDepth": 0},
        )
    except Exception:
        raw_members = []
    if isinstance(raw_members, list):
        node["children"] = [_serialize_node(m) for m in raw_members]
    else:
        node["children"] = []

    return JSONResponse(node)


@router.get("/api/digital-products/{node_guid}/tabular", summary="Preview tabular data for a TabularDataSet")
def get_tabular_data(
    node_guid:       str,
    start_from_row:  int = Query(0,    ge=0),
    max_row_count:   int = Query(100,  ge=1, le=2000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Fetch a page of rows from a TabularDataSet via DataEngineer.get_tabular_data_set."""
    try:
        from pyegeria import DataEngineer
        url_val     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
        server_val  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
        uid         = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
        pwd         = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
        de = DataEngineer(view_server=server_val, platform_url=url_val, user_id=uid, user_pwd=pwd)
        apply_token(de)
    except Exception as exc:
        logger.exception("Failed to create DataEngineer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = de.get_tabular_data_set(
            tabular_data_set_guid=node_guid,
            start_from_row=start_from_row,
            max_row_count=max_row_count,
            output_format="JSON",
        )
    except Exception as exc:
        logger.exception("get_tabular_data_set failed")
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {exc}")

    logger.debug("get_tabular_data_set raw type={} keys={}", type(raw).__name__,
                 list(raw.keys()) if isinstance(raw, dict) else "n/a")
    logger.info("tabular preview guid={} raw_type={} raw_preview={}",
                node_guid, type(raw).__name__, str(raw)[:400])

    if not raw:
        return JSONResponse({"columns": [], "rows": [], "has_more": False,
                             "start_from_row": start_from_row, "row_count": 0})

    # Egeria returns { columnDescriptions: [{columnName, ...}], dataRecords: {"0":[...], "1":[...]} }
    # Normalise to columns (list of names) + rows (list of value-lists).
    if isinstance(raw, dict):
        col_descs = raw.get("columnDescriptions") or []
        if col_descs:
            columns = [c.get("columnName", "") for c in col_descs]
        else:
            columns = raw.get("columns") or raw.get("columnNames") or raw.get("header") or []

        data_records = raw.get("dataRecords")
        if isinstance(data_records, dict) and data_records:
            sorted_keys = sorted(data_records.keys(), key=lambda x: int(x) if x.isdigit() else 0)
            rows = [data_records[k] for k in sorted_keys]
        else:
            rows = raw.get("rows") or raw.get("data") or raw.get("rowData") or []

        has_more = len(rows) >= max_row_count
        return JSONResponse({"columns": columns, "rows": rows, "has_more": has_more,
                             "start_from_row": start_from_row, "row_count": len(rows)})

    if isinstance(raw, list):
        if not raw:
            return JSONResponse({"columns": [], "rows": [], "has_more": False,
                                 "start_from_row": start_from_row, "row_count": 0})
        columns = list(raw[0].keys()) if isinstance(raw[0], dict) else []
        rows = [[row.get(c, "") for c in columns] for row in raw if isinstance(row, dict)]
        has_more = len(rows) >= max_row_count
        return JSONResponse({"columns": columns, "rows": rows, "has_more": has_more,
                             "start_from_row": start_from_row, "row_count": len(rows)})

    return JSONResponse({"columns": [], "rows": [], "has_more": False,
                         "start_from_row": start_from_row, "row_count": 0})
