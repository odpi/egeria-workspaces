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
from egeria_auth import apply_token
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from common_serialize import _authored_fields, _header_summary, _generic_relationships

router = APIRouter(tags=["solution-architect"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import SolutionArchitect
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",   "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",    "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",           "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    mgr = SolutionArchitect(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _is_template(element: dict) -> bool:
    """Return True if the element carries the Egeria 'Template' classification."""
    for val in (element.get("elementHeader") or {}).values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


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
        rtype = rh.get("type") or {}
        g  = rh.get("guid", "")
        if g:
            result.append({
                "guid":           g,
                "displayName":    rp.get("displayName") or rp.get("name") or "",
                "qualifiedName":  rp.get("qualifiedName") or "",
                "typeName":       rtype.get("typeName") or "",
                "superTypeNames": rtype.get("superTypeNames") or [],
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
        "_header":           _header_summary(element),
        **_authored_fields(element),
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
    # Generic catch-all so any relationship key not curated above (e.g. resourceList,
    # governanceDefinitions) still surfaces instead of being silently dropped.
    detail["relationships"] = _generic_relationships(element, skip=(
        "nestedComponents", "solutionComponents", "collectionMembers", "memberOfCollections",
    ))
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
        "_header":           _header_summary(element),
        **_authored_fields(element),
    }


def _serialize_component_detail(element: dict) -> dict:
    detail = _serialize_component_summary(element)
    detail.update(_extract_mermaid_fields(element))

    # memberOfCollections mixes SolutionBlueprint and InformationSupplyChain related
    # elements — split by typeName so both memberships surface on the detail page.
    raw_collections = _rel_list(element, "memberOfCollections")
    blueprints = _serialize_rel_entries([
        m for m in raw_collections
        if (m.get("relatedElement") or {}).get("elementHeader", {}).get("type", {}).get("typeName") == "SolutionBlueprint"
    ])
    supply_chains = _serialize_rel_entries([
        m for m in raw_collections
        if (m.get("relatedElement") or {}).get("elementHeader", {}).get("type", {}).get("typeName") == "InformationSupplyChain"
    ])

    detail["parentComponents"]        = _serialize_rel_entries(_rel_list(element, "usedInSolutionComponents"))
    detail["subComponents"]           = _serialize_rel_entries(_rel_list(element, "nestedSolutionComponents"))
    detail["blueprints"]              = blueprints
    detail["informationSupplyChains"] = supply_chains
    detail["actors"]                  = _serialize_rel_entries(_rel_list(element, "actors"))
    detail["wiredTo"]                 = _serialize_rel_entries(_rel_list(element, "wiredTo"))
    detail["wiredFrom"]               = _serialize_rel_entries(_rel_list(element, "wiredFrom"))
    # Generic catch-all so any relationship key not curated above still surfaces.
    detail["relationships"]     = _generic_relationships(element, skip=(
        "memberOfCollections", "usedInSolutionComponents", "nestedSolutionComponents",
        "actors", "wiredTo", "wiredFrom",
    ))
    return detail


def _serialize_implementation(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":           header.get("guid", ""),
        "displayName":    props.get("displayName") or props.get("name") or "",
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "typeName":       _type_name(element),
        "superTypeNames": (header.get("type") or {}).get("superTypeNames") or [],
        "status":         header.get("status") or "",
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
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
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
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_solution_blueprints failed")
        raise HTTPException(status_code=500, detail=f"Blueprint retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [b for b in raw if not _is_template(b)]

    blueprints = [_serialize_blueprint_summary(b) for b in raw]
    blueprints.sort(key=lambda b: (b.get("displayName") or "").lower())
    return JSONResponse({"blueprints": blueprints, "total": len(blueprints)})


_BP_FOLIO_CACHE: dict = {}
_BP_FOLIO_TTL = 30  # seconds


@router.get("/api/solution/blueprints/folios", summary="Blueprints grouped by their Folios")
def list_blueprints_by_folio(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    refresh:  bool = Query(False, description="Bypass the cache and re-query the metadata store"),
):
    """Group solution blueprints under the Folios that curate them. A blueprint's
    folios are its memberOfCollections entries whose type is Folio; blueprints in
    no folio are returned under `ungrouped`. Built from one depth-1 find."""
    cache_key = f"{url or ''}|{server or ''}|{user_id or ''}"
    cached = _BP_FOLIO_CACHE.get(cache_key)
    if not refresh and cached and (time.time() - cached[0]) < _BP_FOLIO_TTL:
        return JSONResponse(cached[1])

    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_solution_blueprints(
            search_string="*", output_format="JSON", start_from=0, page_size=500,
            graph_query_depth=1, sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_solution_blueprints (folios) failed")
        raise HTTPException(status_code=500, detail=f"Blueprint retrieval failed: {exc}")
    if not isinstance(raw, list):
        raw = []

    folios: dict = {}   # folio guid → {folio fields, blueprints: [...]}
    ungrouped: list = []
    for bp in raw:
        summary = _serialize_blueprint_summary(bp)
        parent_folios = [
            (m.get("relatedElement") or {})
            for m in _rel_list(bp, "memberOfCollections")
            if (m.get("relatedElement") or {}).get("elementHeader", {}).get("type", {}).get("typeName") == "Folio"
        ]
        if not parent_folios:
            ungrouped.append(summary)
            continue
        for f in parent_folios:
            fg = (f.get("elementHeader") or {}).get("guid")
            if not fg:
                continue
            if fg not in folios:
                fp = f.get("properties") or {}
                folios[fg] = {
                    "guid": fg,
                    "displayName": fp.get("displayName") or fp.get("name") or fp.get("qualifiedName") or "",
                    "qualifiedName": fp.get("qualifiedName") or "",
                    "typeName": "Folio",
                    "blueprints": [],
                }
            folios[fg]["blueprints"].append(summary)

    folio_list = sorted(folios.values(), key=lambda f: (f.get("displayName") or "").lower())
    for f in folio_list:
        f["blueprints"].sort(key=lambda b: (b.get("displayName") or "").lower())
    ungrouped.sort(key=lambda b: (b.get("displayName") or "").lower())

    result = {"folios": folio_list, "ungrouped": ungrouped, "total": len(raw)}
    _BP_FOLIO_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


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
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
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
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_solution_components failed")
        raise HTTPException(status_code=500, detail=f"Component retrieval failed: {exc}")

    if not isinstance(raw, list):
        raw = []

    if not include_templates:
        raw = [c for c in raw if not _is_template(c)]

    components = [_serialize_component_summary(c) for c in raw]
    components.sort(key=lambda c: (c.get("displayName") or "").lower())
    return JSONResponse({"components": components, "total": len(components)})


# Component tree cache: cache_key → (timestamp, result). The depth-1 find is ~5s.
_COMP_TREE_CACHE: dict = {}
_COMP_TREE_TTL = 30  # seconds


def _rel_guids(element: dict, key: str) -> list:
    """GUIDs of the related elements under a relationship key."""
    out = []
    for entry in _rel_list(element, key):
        re = entry.get("relatedElement") or entry
        g = (re.get("elementHeader") or {}).get("guid") or re.get("guid")
        if g:
            out.append(g)
    return out


@router.get("/api/solution/components/tree", summary="Solution component composition hierarchy")
def list_components_tree(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    refresh:  bool = Query(False, description="Bypass the cache and re-query the metadata store"),
):
    """Return the solution-component composition forest: roots (components not nested
    in any other) with recursively nested children. Built from a single depth-1 find
    that inlines nestedSolutionComponents (children) and usedInSolutionComponents
    (parents)."""
    cache_key = f"{url or ''}|{server or ''}|{user_id or ''}"
    cached = _COMP_TREE_CACHE.get(cache_key)
    if not refresh and cached and (time.time() - cached[0]) < _COMP_TREE_TTL:
        return JSONResponse(cached[1])

    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create SolutionArchitect manager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_solution_components(
            search_string="*", output_format="JSON",
            start_from=0, page_size=500, graph_query_depth=1,
            sequencing_order="PROPERTY_ASCENDING", sequencing_property="displayName",
        )
    except Exception as exc:
        logger.exception("find_solution_components (tree) failed")
        raise HTTPException(status_code=500, detail=f"Component tree retrieval failed: {exc}")
    if not isinstance(raw, list):
        raw = []

    summary = {}      # guid → node
    children = {}     # guid → [child guid]
    has_parent = set()
    for el in raw:
        g = (el.get("elementHeader") or {}).get("guid")
        if not g:
            continue
        summary[g] = _serialize_component_summary(el)
        kids = _rel_guids(el, "nestedSolutionComponents")
        children[g] = kids
        has_parent.update(kids)                       # nested children have a parent
        if _rel_guids(el, "usedInSolutionComponents"):
            has_parent.add(g)                          # this component is used by another

    def build(guid: str, visited: set) -> dict:
        node = dict(summary.get(guid, {"guid": guid}))
        kids = [k for k in children.get(guid, []) if k in summary and k not in visited]
        node["children"] = [build(k, visited | {guid}) for k in kids]
        node["isContainer"] = bool(node["children"])
        return node

    roots = [build(g, set()) for g in summary if g not in has_parent]
    roots.sort(key=lambda n: (n.get("displayName") or "").lower())
    result = {"roots": roots, "total": len(summary)}
    _COMP_TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


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
