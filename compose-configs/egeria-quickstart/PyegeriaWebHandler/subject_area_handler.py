"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Subject Area Explorer — FastAPI router.

SubjectArea is a Collection subtype, nested via the SubjectAreaHierarchy
relationship — each element carries a single `broaderSubjectArea` (parent)
and a `nestedSubjectAreas` list (children), confirmed live against
qs-view-server. Detail and CollectionMembers browsing for a selected subject
area deliberately reuse the generic Collection endpoints already exposed by
digital_products_handler/collections_handler (GET /api/collections/{guid} and
its /children) rather than duplicating them here — a SubjectArea is just
another Collection subtype, so get_collection_by_guid and
get_collection_members already work for it unmodified, cross-links and all.

Endpoints:
  GET /api/subject-areas   → full nesting hierarchy (small taxonomy; one fetch)
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from digital_products_handler import _get_manager, _serialize_node, _is_template

router = APIRouter(tags=["subject-areas"])


def _rel_guid(entry) -> Optional[str]:
    """Extract the related element's guid from a single RelatedMetadataElementSummary dict."""
    if not isinstance(entry, dict):
        return None
    re = entry.get("relatedElement") or {}
    return (re.get("elementHeader") or {}).get("guid") or None


@router.get("/api/subject-areas", summary="Full SubjectArea nesting hierarchy")
def get_subject_area_hierarchy(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """
    Return every SubjectArea, nested per the SubjectAreaHierarchy relationship
    (broaderSubjectArea / nestedSubjectAreas properties on each element). The
    taxonomy is small (governance classification, not a data catalog), so the
    whole tree is assembled in one fetch rather than lazily per-node.
    """
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
            page_size=1000,
            graph_query_depth=1,
            metadata_element_type_name="SubjectArea",
        )
    except Exception as exc:
        logger.exception("SubjectArea discovery failed")
        raise HTTPException(status_code=500, detail=f"Subject area retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []
    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]

    nodes: dict = {}
    child_guids: dict = {}
    parent_guid: dict = {}
    for element in raw:
        node = _serialize_node(element)
        g = node.get("guid") or ""
        if not g:
            continue
        nodes[g] = node
        kids = []
        for entry in (element.get("nestedSubjectAreas") or []):
            cg = _rel_guid(entry)
            if cg:
                kids.append(cg)
        child_guids[g] = kids
        parent_guid[g] = _rel_guid(element.get("broaderSubjectArea"))

    def build(guid: str, seen: frozenset) -> dict:
        node = dict(nodes[guid])
        node["isContainer"] = bool(child_guids.get(guid))
        if guid in seen:
            node["children"] = []  # cycle guard — shouldn't happen, but don't hang
            return node
        seen = seen | {guid}
        node["children"] = [build(cg, seen) for cg in child_guids.get(guid, []) if cg in nodes]
        return node

    roots = [build(g, frozenset()) for g in nodes
             if not parent_guid.get(g) or parent_guid.get(g) not in nodes]
    roots.sort(key=lambda n: (n.get("displayName") or "").lower())
    return JSONResponse({"roots": roots, "total": len(nodes)})
