"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Duplicate Resolution Review — FastAPI router.

Endpoints:
  GET /api/duplicate-review/pending        → KnownDuplicate elements paired via PeerDuplicateLink
  GET /api/duplicate-review/consolidated   → ConsolidatedDuplicate elements with their source links

Read-only for this pass — pyegeria's ClassificationExplorer already exposes
the full write-side CRUD (set/clear *DuplicateClassification,
link/unlink *DuplicateLink) for a future confirm/reject follow-up.

Uses ClassificationExplorer.get_elements_by_classification/get_relationships
with output_format="JSON" — this is the converter-backed
OpenMetadataRootElement/ElementHeader shape (properties flat dict,
end1/end2 as ElementStub), NOT the raw MetadataExpert shape used by
insights_handler.py/action_center_handler.py. Confirmed live: ElementStub
carries no displayName of its own, only `uniqueName` (qualifiedName) — so
pair rows fall back to that for a label.

NOTE: pyegeria's link_elements_as_peer_duplicates/_async_link_elements_as_peer_duplicates
builds the wrong URL (`/elements/{guid}/peer-duplicate/{guid}/attach`) --
the real Java endpoint (ClassificationExplorerResource.java) is
`/related-elements/{guid}/peer-duplicate/{guid}/attach`. Confirmed via a 404
when seeding this feature's demo pair; worked around by calling
_async_make_request directly with the corrected path. Read path
(get_relationships) is unaffected. Worth a PYEGERIA_ISSUES.md entry
(follow-up, not blocking this read-only pane).
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token

router = APIRouter(tags=["duplicate-review"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _stub_summary(stub: dict) -> dict:
    """ElementStub (end1/end2 of a relationship, or a classified element's own
    header) → {guid, typeName, displayName, qualifiedName}. ElementStub never
    carries displayName, only uniqueName (the qualifiedName) — that's the best
    label available without a second round-trip to fetch the full element."""
    if not isinstance(stub, dict):
        return {}
    type_info = stub.get("type") or {}
    qname = stub.get("uniqueName") or ""
    return {
        "guid":          stub.get("guid", ""),
        "typeName":      type_info.get("typeName", ""),
        "displayName":   qname or stub.get("guid", ""),
        "qualifiedName": qname,
    }


def _element_summary(element: dict) -> dict:
    """Converter-shaped OpenMetadataRootElement (from get_elements_by_classification)
    → {guid, typeName, displayName, qualifiedName}."""
    if not isinstance(element, dict):
        return {}
    hdr = element.get("elementHeader") or {}
    props = element.get("properties") or {}
    type_info = hdr.get("type") or {}
    qname = props.get("qualifiedName") or ""
    return {
        "guid":          hdr.get("guid", ""),
        "typeName":      type_info.get("typeName", ""),
        "displayName":   props.get("displayName") or props.get("name") or qname or hdr.get("guid", ""),
        "qualifiedName": qname,
    }


@router.get("/api/duplicate-review/pending", summary="KnownDuplicate elements paired via PeerDuplicateLink")
def list_pending(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer for duplicate review")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        rels = mgr.get_relationships("PeerDuplicateLink", output_format="JSON")
    except Exception as exc:
        logger.exception("get_relationships(PeerDuplicateLink) failed")
        raise HTTPException(status_code=500, detail=f"Duplicate review retrieval failed: {exc}")

    pairs = []
    for rel in (rels if isinstance(rels, list) else []):
        if not isinstance(rel, dict):
            continue
        rel_props = rel.get("relationshipProperties") or {}
        rel_hdr = rel.get("relationshipHeader") or {}
        pairs.append({
            "relationshipGuid": rel_hdr.get("guid", ""),
            "statusIdentifier":  rel_props.get("statusIdentifier"),
            "steward":           rel_props.get("steward") or "",
            "source":            rel_props.get("source") or "",
            "notes":             rel_props.get("notes") or "",
            "elementA":          _stub_summary(rel.get("end1") or {}),
            "elementB":          _stub_summary(rel.get("end2") or {}),
        })

    return JSONResponse({"pairs": pairs, "total": len(pairs)})


@router.get("/api/duplicate-review/consolidated", summary="ConsolidatedDuplicate elements with their source links")
def list_consolidated(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer for duplicate review")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        survivors = mgr.get_elements_by_classification("ConsolidatedDuplicate", output_format="JSON")
    except Exception as exc:
        logger.exception("get_elements_by_classification(ConsolidatedDuplicate) failed")
        raise HTTPException(status_code=500, detail=f"Duplicate review retrieval failed: {exc}")

    try:
        source_rels = mgr.get_relationships("ConsolidatedDuplicateLink", output_format="JSON")
    except Exception as exc:
        logger.exception("get_relationships(ConsolidatedDuplicateLink) failed")
        raise HTTPException(status_code=500, detail=f"Duplicate review retrieval failed: {exc}")

    sources_by_survivor = {}
    for rel in (source_rels if isinstance(source_rels, list) else []):
        if not isinstance(rel, dict):
            continue
        survivor = _stub_summary(rel.get("end1") or {})
        source   = _stub_summary(rel.get("end2") or {})
        if survivor.get("guid"):
            sources_by_survivor.setdefault(survivor["guid"], []).append(source)

    records = []
    for el in (survivors if isinstance(survivors, list) else []):
        if not isinstance(el, dict):
            continue
        summary = _element_summary(el)
        records.append({
            "survivor": summary,
            "sources":  sources_by_survivor.get(summary.get("guid"), []),
        })

    return JSONResponse({"consolidated": records, "total": len(records)})
