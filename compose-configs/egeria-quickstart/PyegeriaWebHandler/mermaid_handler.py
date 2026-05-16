"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Mermaid Graph Handler — FastAPI router.

Endpoint:
  GET /api/mermaid/{guid}  → mermaid diagram showing element context
"""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["mermaid"])


def _get_explorer():
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


@router.get("/api/mermaid/{guid}", summary="Get mermaid context graph for an element")
def get_mermaid_graph(guid: str):
    """
    Return a Mermaid diagram showing the element and its anchored/related elements.
    Uses MetadataExplorer OMVS get_anchored_metadata_element_graph.
    Returns {guid, mermaidGraph} — mermaidGraph is empty string if unavailable.
    """
    try:
        mgr = _get_explorer()
    except Exception as exc:
        logger.exception("Failed to create MetadataExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        graph = mgr.get_anchored_element_graph(guid, mermaid_only=True)
    except Exception as exc:
        logger.warning(f"get_anchored_metadata_element_graph failed for {guid}: {exc}")
        graph = ""

    # Normalize: pyegeria may return a "No mermaid graph found" string on miss
    if not isinstance(graph, str) or graph.lower().startswith("no "):
        graph = ""

    return JSONResponse({"guid": guid, "mermaidGraph": graph})
