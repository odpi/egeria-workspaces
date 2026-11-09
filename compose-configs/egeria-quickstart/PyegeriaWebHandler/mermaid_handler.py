"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Mermaid Graph Handler — FastAPI router.

Endpoints:
  GET /api/mermaid/{guid}           → context diagram via get_metadata_element_by_guid (graph_query_depth=10, max_mermaid_node_count=250)
  GET /api/mermaid/{guid}/anchored  → full anchored element graph via get_anchored_element_graph
"""

import os
from egeria_auth import apply_token
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["mermaid"])

# pyegeria's shared find/get request helpers default graph_query_depth=3 and,
# critically, max_mermaid_node_count=5 -- the server truncates the generated
# mermaid diagram to at most 5 nodes unless told otherwise. This endpoint's
# whole purpose is rendering a complete diagram for one element, so a generous
# override is safe here (see egeria-python PYEGERIA_ISSUES.md ISSUE-23).
_MERMAID_GRAPH_QUERY_DEPTH = 10
_MERMAID_MAX_NODES = 250


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
    apply_token(mgr)
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
    apply_token(mgr)
    return mgr




from graph_keys import extract_graph_fields


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


@router.get("/api/mermaid/{guid}", summary="Get context diagram for an element (graph_query_depth=10, max_mermaid_node_count=250)")
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
        element = mgr.get_element_by_guid(
            guid, output_format="JSON",
            graph_query_depth=_MERMAID_GRAPH_QUERY_DEPTH,
            max_mermaid_node_count=_MERMAID_MAX_NODES,
        )
        # Every diagram field the element carries, found by shape (graph_keys.py): a fixed list here is what
        # hid activityMermaidGraph and every other new graph kind.
        graphs = extract_graph_fields(element) if isinstance(element, dict) else {}
    except Exception as exc:
        logger.warning(f"get_element_by_guid failed for {guid}: {exc}")
        graphs = {}

    return JSONResponse({"guid": guid, "mermaidGraph": graphs.get("mermaidGraph", ""), "graphs": graphs})
