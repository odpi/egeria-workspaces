"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Namespaces Explorer — FastAPI router.

Namespace is a Collection subtype (OpenMetadataType NAMESPACE_COLLECTION,
guid 1a0849e0-c97b-4d99-adda-e22cdbb99ff9) used to group elements under a
particular namespace — in this deployment, Unity Catalog Catalogs. Reuses the
generic Collection serializer/relationship-extractor from
digital_products_handler rather than duplicating it, same pattern as
agreements_handler.py (the closest existing template: a single-subtype
Collection list + detail, no hierarchy assembly needed).

Endpoints:
  GET /api/namespaces          → list / search all namespaces
  GET /api/namespaces/{guid}   → full detail, including members + mermaid graph
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from digital_products_handler import (
    _get_manager, _serialize_node, _extract_all_rels, _is_template,
)

router = APIRouter(tags=["namespaces"])


@router.get("/api/namespaces", summary="List / search all namespaces")
def list_namespaces(
    search_string: str = Query("*", description="Filter string; '*' returns all"),
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(500, ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager for namespaces list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_collections(
            search_string=search_string,
            starts_with=False,
            ignore_case=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
            metadata_element_type_name="Namespace",
        )
    except Exception as exc:
        logger.exception("find_collections (Namespace) failed")
        raise HTTPException(status_code=500, detail=f"Namespace retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

    namespaces = [_serialize_node(e) for e in raw if isinstance(e, dict)]
    namespaces.sort(key=lambda x: (x.get("displayName") or "").lower())

    return JSONResponse({"namespaces": namespaces, "total": len(namespaces)})


@router.get("/api/namespaces/{guid}", summary="Get full detail for a namespace")
def get_namespace(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager for namespace detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_collection_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Namespace detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Namespace {guid!r} not found")

    node = _serialize_node(element)
    node["relationships"] = _extract_all_rels(element)
    try:
        raw_members = mgr.get_collection_members(
            collection_guid=guid,
            output_format="JSON",
            page_size=200,
            body={"class": "ResultsRequestBody", "graphQueryDepth": 0},
        )
    except Exception:
        raw_members = []
    node["children"] = [_serialize_node(m) for m in raw_members] if isinstance(raw_members, list) else []
    return JSONResponse(node)
