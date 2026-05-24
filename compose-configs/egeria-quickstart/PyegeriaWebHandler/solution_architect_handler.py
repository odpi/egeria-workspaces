"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Solution Architect Explorer — FastAPI router.

Endpoints:
  GET /api/solution/blueprints                       → list all solution blueprints
  GET /api/solution/blueprints/{guid}                → full detail for a blueprint
  GET /api/solution/components                       → list all solution components
  GET /api/solution/components/{guid}                → full detail for a component
  GET /api/solution/components/{guid}/implementations → concrete implementations
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["solution-architect"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import SolutionArchitect
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",   "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",    "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",           "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = SolutionArchitect(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    mgr.create_egeria_bearer_token()
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _rel_list(element: dict, key: str) -> list:
    """Return the raw relationship list for a given key, normalising None → []."""
    return element.get(key) or []


_SA_MERMAID_FIELDS = [
    "mermaidGraph", "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "iscImplementationMermaidGraph", "informationSupplyChainMermaidGraph",
    "edgeMermaidGraph", "anchorMermaidGraph", "specificationMermaidGraph",
    "actionMermaidGraph", "localLineageGraph", "fieldLevelLineageGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph",
    "collectionMermaidMindMap", "zoneProfileMermaidPieChart",
    "zoneProfileAnchoredMermaidPieChart", "zoneProfileAllPieChart",
    "userAccountTypeProfileMermaidPieChart", "userAccountStatusMermaidPieChart",
]


def _extract_mermaid_fields(element: dict) -> dict:
    lower_map = {k.lower(): v for k, v in element.items()}
    result = {}
    for f in _SA_MERMAID_FIELDS:
        v = lower_map.get(f.lower()) or ""
        if v and isinstance(v, str) and not v.lower().startswith("no "):
            result[f] = v
    return result


def _serialize_rel_entries(rel_list: list) -> list:
    """Convert [{relatedElement: {elementHeader, properties}}, ...] → [{guid, displayName, qualifiedName, typeName}]."""
    result = []
    for rel in rel_list:
        re = rel.get("relatedElement") or {}
        rh = re.get("elementHeader") or {}
        rp = re.get("properties") or {}
        g  = rh.get("guid", "")
        if g:
            result.append({
                "guid":          g,
                "displayName":   rp.get("displayName") or rp.get("name") or "",
                "qualifiedName": rp.get("qualifiedName") or "",
                "typeName":      (rh.get("type") or {}).get("typeName") or "",
            })
    return result


def _serialize_blueprint_summary(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":              header.get("guid", ""),
        "displayName":       props.get("displayName") or props.get("name") or "",
        "qualifiedName":     props.get("qualifiedName") or "",
        "description":       props.get("description") or "",
        "versionIdentifier": props.get("versionIdentifier") or "",
        "lifecycleStatus":   props.get("lifecycleStatus") or "",
        "userDefinedStatus": props.get("userDefinedStatus") or "",
        "status":            header.get("status") or "",
        "typeName":          _type_name(element),
    }


def _serialize_blueprint_detail(element: dict) -> dict:
    detail = _serialize_blueprint_summary(element)
    detail.update(_extract_mermaid_fields(element))
    # Components linked to this blueprint (nestedComponents or collectionMembers key varies by depth)
    components = _serialize_rel_entries(_rel_list(element, "nestedComponents"))
    if not components:
        components = _serialize_rel_entries(_rel_list(element, "solutionComponents"))
    if not components:
        # collectionMembers includes component-type entries at graph_query_depth >= 1
        components = _serialize_rel_entries(_rel_list(element, "collectionMembers"))
    detail["components"] = components
    detail["memberOf"] = _serialize_rel_entries(_rel_list(element, "memberOfCollections"))
    return detail


def _serialize_component_summary(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":              header.get("guid", ""),
        "displayName":       props.get("displayName") or props.get("name") or "",
        "qualifiedName":     props.get("qualifiedName") or "",
        "description":       props.get("description") or "",
        "componentType":     props.get("componentType") or "",
        "versionIdentifier": props.get("versionIdentifier") or "",
        "lifecycleStatus":   props.get("lifecycleStatus") or "",
        "userDefinedStatus": props.get("userDefinedStatus") or "",
        "status":            header.get("status") or "",
        "typeName":          _type_name(element),
    }


def _serialize_component_detail(element: dict) -> dict:
    detail = _serialize_component_summary(element)
    detail.update(_extract_mermaid_fields(element))

    # Parent blueprints come from memberOfCollections filtered by SolutionBlueprint typeName
    raw_collections = _rel_list(element, "memberOfCollections")
    blueprints = _serialize_rel_entries([
        m for m in raw_collections
        if (m.get("relatedElement") or {}).get("elementHeader", {}).get("type", {}).get("typeName") == "SolutionBlueprint"
    ])

    detail["parentComponents"]  = _serialize_rel_entries(_rel_list(element, "usedInSolutionComponents"))
    detail["subComponents"]     = _serialize_rel_entries(_rel_list(element, "nestedSolutionComponents"))
    detail["blueprints"]        = blueprints
    detail["actors"]            = _serialize_rel_entries(_rel_list(element, "actors"))
    detail["wiredTo"]           = _serialize_rel_entries(_rel_list(element, "wiredTo"))
    detail["wiredFrom"]         = _serialize_rel_entries(_rel_list(element, "wiredFrom"))
    return detail


def _serialize_implementation(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "displayName":   props.get("displayName") or props.get("name") or "",
        "qualifiedName": props.get("qualifiedName") or "",
        "description":   props.get("description") or "",
        "typeName":      _type_name(element),
        "status":        header.get("status") or "",
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/solution/blueprints", summary="List all solution blueprints")
def list_blueprints(
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
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_solution_blueprints(
            search_string="*",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_solution_blueprints failed")
        raise HTTPException(status_code=500, detail=f"Blueprint retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    blueprints = [_serialize_blueprint_summary(b) for b in raw]
    blueprints.sort(key=lambda b: (b.get("displayName") or "").lower())
    return JSONResponse({"blueprints": blueprints, "total": len(blueprints)})


@router.get("/api/solution/blueprints/{guid}", summary="Get a single solution blueprint by GUID")
def get_blueprint(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_solution_blueprint_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_solution_blueprint_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Blueprint retrieval failed: {exc}")

    if not raw or isinstance(raw, str):
        raise HTTPException(status_code=404, detail=f"Blueprint {guid!r} not found")

    return JSONResponse(_serialize_blueprint_detail(raw))


@router.get("/api/solution/components", summary="List all solution components")
def list_components(
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
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_solution_components(
            search_string="*",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
        )
    except Exception as exc:
        logger.exception("find_solution_components failed")
        raise HTTPException(status_code=500, detail=f"Component retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    components = [_serialize_component_summary(c) for c in raw]
    components.sort(key=lambda c: (c.get("displayName") or "").lower())
    return JSONResponse({"components": components, "total": len(components)})


@router.get("/api/solution/components/{guid}", summary="Get a single solution component by GUID")
def get_component(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_solution_component_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_solution_component_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Component retrieval failed: {exc}")

    if not raw or isinstance(raw, str):
        raise HTTPException(status_code=404, detail=f"Component {guid!r} not found")

    return JSONResponse(_serialize_component_detail(raw))


@router.get("/api/solution/components/{guid}/implementations", summary="Get implementations of a solution component")
def get_component_implementations(
    guid: str,
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
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_solution_component_implementations(
            solution_component_guid=guid,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
        )
    except Exception as exc:
        logger.exception("get_solution_component_implementations failed")
        raise HTTPException(status_code=500, detail=f"Implementations retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    implementations = [_serialize_implementation(i) for i in raw]
    return JSONResponse({"implementations": implementations, "total": len(implementations), "component": guid})
