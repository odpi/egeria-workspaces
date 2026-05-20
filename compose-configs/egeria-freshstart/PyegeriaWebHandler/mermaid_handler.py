"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Mermaid Graph Handler — FastAPI router.

Endpoints:
  GET /api/mermaid/{guid}           → context diagram via get_metadata_element_by_guid (graph_query_depth=5)
  GET /api/mermaid/{guid}/anchored  → full anchored element graph via get_anchored_element_graph
"""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["mermaid"])


def _get_classifier():
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_expert():
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",   "view-server")
    user   = os.environ.get("EGERIA_USER",          "erinoverview")
    pwd    = os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _normalise(graph) -> str:
    if not isinstance(graph, str) or graph.lower().startswith("no "):
        return ""
    return graph


@router.get("/api/mermaid/{guid}/anchored", summary="Get full anchored element graph")
def get_anchored_graph(guid: str):
    """
    Return a Mermaid diagram showing the element and all its anchored elements.
    Uses MetadataExpert.get_anchored_element_graph — a broader, more expensive traversal.
    Returns {guid, mermaidGraph}.
    """
    try:
        mgr = _get_expert()
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
def get_mermaid_graph(guid: str):
    """
    Return a Mermaid context diagram using ClassificationExplorer.get_element_by_guid.
    Extracts the top-level mermaidGraph field from the response.
    Returns {guid, mermaidGraph}.
    """
    try:
        mgr = _get_classifier()
    except Exception as exc:
        logger.exception("Failed to create ClassificationManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = mgr.get_element_by_guid(guid, output_format="JSON")
        graph = _normalise(element.get("mermaidGraph", "") if isinstance(element, dict) else "")
    except Exception as exc:
        logger.warning(f"get_element_by_guid failed for {guid}: {exc}")
        graph = ""

    return JSONResponse({"guid": guid, "mermaidGraph": graph})
