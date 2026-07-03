"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Agreements Explorer — FastAPI router.

Agreements are Collection subtypes, so this reuses the generic Collection
serializer/relationship-extractor from digital_products_handler rather than
duplicating it. `find_collections(metadata_element_type_name="Agreement")`
returns every subtype together in one call (confirmed against a live server:
it returns both plain Agreement and DigitalSubscription elements).

Endpoints:
  GET /api/agreements          → list / search all agreements (all subtypes)
  GET /api/agreements/{guid}   → full detail, including agreementItems/agreementActors/contracts + mermaid graph
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from digital_products_handler import (
    _get_manager, _serialize_node, _extract_all_rels, _is_template,
)

router = APIRouter(tags=["agreements"])

# Subtypes pyegeria models for Agreement (see AGREEMENT_PROPERTIES_LIST in
# pyegeria's collection_manager.py: AgreementProperties, DigitalSubscriptionProperties).
# DataSharingAgreement has a client-side properties model but is not yet accepted
# by the server (confirmed: create fails with a 400) — kept in this list so its tab
# appears (with a zero count) the moment server support lands, with no code change.
AGREEMENT_TYPES = ["Agreement", "DataSharingAgreement", "DigitalSubscription"]


@router.get("/api/agreements", summary="List / search all agreements")
def list_agreements(
    search_string: str = Query("*", description="Filter string; '*' returns all"),
    type_name: Optional[str] = Query(None, description="Restrict to one subtype: Agreement, DataSharingAgreement, DigitalSubscription"),
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
        logger.exception("Failed to create CollectionManager for agreements list")
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
            metadata_element_type_name="Agreement",
        )
    except Exception as exc:
        logger.exception("find_collections (Agreement) failed")
        raise HTTPException(status_code=500, detail=f"Agreement retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

    agreements = [_serialize_node(e) for e in raw if isinstance(e, dict)]
    if type_name:
        agreements = [a for a in agreements if a["typeName"] == type_name]
    agreements.sort(key=lambda x: (x.get("typeName", ""), (x.get("displayName") or "").lower()))

    by_type: dict[str, int] = {}
    for a in agreements:
        by_type[a["typeName"]] = by_type.get(a["typeName"], 0) + 1

    return JSONResponse({"agreements": agreements, "total": len(agreements), "byType": by_type})


@router.get("/api/agreements/{guid}", summary="Get full detail for an agreement")
def get_agreement(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create CollectionManager for agreement detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_collection_by_guid failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Agreement detail retrieval failed: {exc}")

    if isinstance(element, list):
        element = element[0] if element else None
    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"Agreement {guid!r} not found")

    node = _serialize_node(element)
    node["relationships"] = _extract_all_rels(element)
    return JSONResponse(node)
