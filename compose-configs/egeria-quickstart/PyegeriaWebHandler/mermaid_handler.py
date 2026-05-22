"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Mermaid Graph Handler — FastAPI router.

Endpoints:
  GET /api/mermaid/{guid}           → context diagram via get_metadata_element_by_guid (graph_query_depth=5)
  GET /api/mermaid/{guid}/anchored  → full anchored element graph via get_anchored_element_graph
"""

import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["mermaid"])


def _get_classifier(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url     = url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server  = server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


_ALL_MERMAID_FIELDS = [
    "mermaidGraph",
    "anchorMermaidGraph",
    "informationSupplyChainMermaidGraph",
    "fieldLevelLineageGraph",
    "actionMermaidGraph",
    "localLineageGraph",
    "edgeMermaidGraph",
    "iscImplementationMermaidGraph",
    "specificationMermaidGraph",
    "solutionBlueprintMermaidGraph",
    "solutionSubcomponentMermaidGraph",
    "governanceActionProcessMermaidGraph",
    # newer pyegeria fields (may not be present in older installations)
    "organizationTreeMermaidGraph",
    "collectionMermaidMindMap",
    "zoneProfileMermaidPieChart",
    "zoneProfileAnchoredMermaidPieChart",
    "zoneProfileAllPieChart",
    "userAccountTypeProfileMermaidPieChart",
    "userAccountStatusMermaidPieChart",
]


def _normalise(graph) -> str:
    if not isinstance(graph, str) or graph.lower().startswith("no "):
        return ""
    return graph


@router.get("/api/mermaid/{guid}/anchored", summary="Get full anchored element graph")
def get_anchored_graph(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """
    Return a Mermaid diagram showing the element and all its anchored elements.
    Uses MetadataExpert.get_anchored_element_graph — a broader, more expensive traversal.
    Returns {guid, mermaidGraph}.
    """
    try:
        mgr = _get_expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create MetadataExpert")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        graph = _normalise(mgr.get_anchored_element_graph(guid, mermaid_only=True))
    except Exception as exc:
        logger.warning(f"get_anchored_element_graph failed for {guid}: {exc}")
        graph = ""

    return JSONResponse({"guid": guid, "mermaidGraph": graph})


@router.get("/api/mermaid/{guid}", summary="Get context diagram for an element (graph_query_depth=5)")
def get_mermaid_graph(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """
    Return a Mermaid context diagram using ClassificationExplorer.get_element_by_guid.
    Extracts the top-level mermaidGraph field from the response.
    Returns {guid, mermaidGraph}.
    """
    try:
        mgr = _get_classifier(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_element_by_guid(guid, output_format="JSON")
        graphs = {}
        if isinstance(element, dict):
            lower_map = {k.lower(): v for k, v in element.items()}
            for field in _ALL_MERMAID_FIELDS:
                val = _normalise(lower_map.get(field.lower(), ""))
                if val:
                    graphs[field] = val
    except Exception as exc:
        logger.warning(f"get_element_by_guid failed for {guid}: {exc}")
        graphs = {}

    return JSONResponse({"guid": guid, "mermaidGraph": graphs.get("mermaidGraph", ""), "graphs": graphs})
