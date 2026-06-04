"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Information Supply Chain Explorer — FastAPI router.

Endpoints:
  GET /api/isc       → list all information supply chains
  GET /api/isc/{guid} → full detail for an ISC
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["isc"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import SolutionArchitect
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = SolutionArchitect(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _get_classifier(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _rel_list(element: dict, key: str) -> list:
    return element.get(key) or []


def _serialize_rel_entries(rel_list: list) -> list:
    result = []
    for rel in rel_list:
        re = rel.get("relatedElement") or {}
        rh = re.get("elementHeader") or {}
        rp = re.get("properties") or {}
        g = rh.get("guid", "")
        if g:
            result.append({
                "guid":          g,
                "displayName":   rp.get("displayName") or rp.get("name") or "",
                "qualifiedName": rp.get("qualifiedName") or "",
                "description":   rp.get("description") or "",
                "typeName":      (rh.get("type") or {}).get("typeName") or "",
            })
    return result


_MERMAID_FIELDS = [
    "mermaidGraph", "iscImplementationMermaidGraph", "informationSupplyChainMermaidGraph",
    "edgeMermaidGraph", "anchorMermaidGraph", "specificationMermaidGraph",
    "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "actionMermaidGraph", "localLineageGraph", "fieldLevelLineageGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph",
    "collectionMermaidMindMap", "zoneProfileMermaidPieChart",
    "zoneProfileAnchoredMermaidPieChart", "zoneProfileAllPieChart",
    "userAccountTypeProfileMermaidPieChart", "userAccountStatusMermaidPieChart",
]


def _extract_mermaid(element: dict) -> dict:
    """Return all non-empty mermaid graph fields found at the top level of an element dict."""
    lower_map = {k.lower(): v for k, v in element.items()}
    result = {}
    for f in _MERMAID_FIELDS:
        v = lower_map.get(f.lower()) or ""
        if v and isinstance(v, str) and not v.lower().startswith("no "):
            result[f] = v
    return result


def _serialize_isc(element: dict) -> dict:
    """Full serializer — used for both list and detail; includes mermaid fields and relationships."""
    props  = _props(element)
    header = _header(element)
    d = {
        "guid":              header.get("guid", ""),
        "displayName":       props.get("displayName") or props.get("name") or "",
        "qualifiedName":     props.get("qualifiedName") or "",
        "description":       props.get("description") or "",
        "scope":             props.get("scope") or "",
        "versionIdentifier": props.get("versionIdentifier") or "",
        "lifecycleStatus":   props.get("lifecycleStatus") or "",
        "status":            header.get("status") or "",
        "typeName":          _type_name(element),
        "segments":          _serialize_rel_entries(_rel_list(element, "segments")),
        "implementations":   _serialize_rel_entries(_rel_list(element, "implementations")),
    }
    d.update(_extract_mermaid(element))
    return d


@router.get("/api/isc", summary="List all information supply chains")
def list_isc(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SolutionArchitect manager for ISC list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_information_supply_chains(
            search_string="*",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            add_implementation=True,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_information_supply_chains failed")
        raise HTTPException(status_code=500, detail=f"ISC retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    iscs = [_serialize_isc(e) for e in raw if isinstance(e, dict)]
    iscs.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"supply_chains": iscs, "total": len(iscs)})


@router.get("/api/isc/{guid}", summary="Get full detail for an information supply chain")
def get_isc(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        exp = _get_classifier(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer for ISC detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        element = exp.get_element_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception(f"get_element_by_guid failed for ISC {guid}")
        raise HTTPException(status_code=500, detail=f"ISC detail retrieval failed: {exc}")

    if not isinstance(element, dict):
        raise HTTPException(status_code=404, detail=f"ISC {guid!r} not found")

    return JSONResponse(_serialize_isc(element))
