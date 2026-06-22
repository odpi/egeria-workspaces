"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Projects Explorer — FastAPI router.

Endpoints:
  GET /api/projects             → list all projects (name, status, classifications)
  GET /api/projects/{guid}      → single project detail + child projects
"""

import os
from egeria_auth import apply_token
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["projects"])


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ProjectManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ProjectManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _extract_classifications(header: dict) -> list:
    result = []
    for cls in (header.get("classifications") or []):
        if not isinstance(cls, dict):
            continue
        cls_header = cls.get("classificationHeader") or cls.get("header") or cls
        type_name  = (cls_header.get("type") or {}).get("typeName") or cls_header.get("classificationName") or ""
        if not type_name or type_name == "TemplateSubstitute":
            continue
        cls_props  = cls.get("classificationProperties") or cls.get("properties") or {}
        flat_props = {}
        if isinstance(cls_props, dict):
            prop_map = cls_props.get("propertyValueMap") or {}
            for k, v in prop_map.items():
                flat_props[k] = v.get("primitiveValue", "") if isinstance(v, dict) else str(v)
            if not flat_props:
                for k, v in cls_props.items():
                    if k not in ("class", "propertyValueMap", "propertiesAsStrings"):
                        flat_props[k] = str(v)
        result.append({"typeName": type_name, "properties": flat_props})
    return result


def _serialize_project(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":           header.get("guid", ""),
        "typeName":       _type_name(element),
        "displayName":    props.get("displayName") or props.get("name") or "",
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "projectStatus":  props.get("projectStatus") or "",
        "startDate":      props.get("startDate") or "",
        "plannedEndDate": props.get("plannedEndDate") or "",
        "status":         header.get("status") or "",
        "classifications": _extract_classifications(header),
    }


@router.get("/api/projects", summary="List all projects")
def get_projects(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ProjectManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.find_projects(
            search_string="*",
            starts_with=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
            as_of_time=as_of_time or None,
        )
    except Exception as exc:
        logger.exception("find_projects failed")
        raise HTTPException(status_code=500, detail=f"Project retrieval failed: {exc}")

    if not raw or not isinstance(raw, list):
        return JSONResponse({"projects": [], "total": 0})

    projects = [_serialize_project(p) for p in raw if _type_name(p) == "Project"]
    projects.sort(key=lambda p: (p.get("displayName") or "").lower())
    return JSONResponse({"projects": projects, "total": len(projects)})


# Project hierarchy cache: cache_key → (timestamp, result).
_PROJ_TREE_CACHE: dict = {}
_PROJ_TREE_TTL = 120  # seconds


def _rel_guids(element: dict, key: str) -> list:
    """GUIDs of related elements under a relationship key (depth-1 form)."""
    out = []
    for entry in (element.get(key) or []):
        if not isinstance(entry, dict):
            continue
        re = entry.get("relatedElement") or entry
        g = (re.get("elementHeader") or {}).get("guid") or re.get("guid")
        if g:
            out.append(g)
    return out


def _project_forest(mgr, child_key: str, parent_key: str) -> dict:
    """Build a project forest from a single depth-1 find. child_key/parent_key are
    the downward/upward relationship attribute names (e.g. managedProjects /
    managingProjects for hierarchy, or dependsOnProjects / dependentProject for
    dependencies). Roots are projects with no parent edge; cycles are guarded."""
    raw = mgr.find_projects(
        search_string="*", starts_with=True, output_format="JSON",
        start_from=0, page_size=500, graph_query_depth=1,
        sequencing_order="PROPERTY_ASCENDING", sequencing_property="displayName",
    )
    if not isinstance(raw, list):
        raw = []

    summary, children, has_parent = {}, {}, set()
    for el in raw:
        if _type_name(el) != "Project":
            continue
        g = _header(el).get("guid")
        if not g:
            continue
        summary[g] = _serialize_project(el)
        kids = _rel_guids(el, child_key)
        children[g] = kids
        has_parent.update(kids)
        if _rel_guids(el, parent_key):
            has_parent.add(g)

    def build(guid: str, visited: set) -> dict:
        node = dict(summary.get(guid, {"guid": guid}))
        kids = [k for k in children.get(guid, []) if k in summary and k not in visited]
        node["children"] = [build(k, visited | {guid}) for k in kids]
        node["isContainer"] = bool(node["children"])
        return node

    roots = [build(g, set()) for g in summary if g not in has_parent]
    roots.sort(key=lambda n: (n.get("displayName") or "").lower())
    return {"roots": roots, "total": len(summary)}


def _cached_forest(kind: str, child_key: str, parent_key: str, url, server, user_id, user_pwd):
    cache_key = f"{kind}|{url or ''}|{server or ''}|{user_id or ''}"
    cached = _PROJ_TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _PROJ_TREE_TTL:
        return JSONResponse(cached[1])
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ProjectManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        result = _project_forest(mgr, child_key, parent_key)
    except Exception as exc:
        logger.exception(f"project {kind} forest failed")
        raise HTTPException(status_code=500, detail=f"Project {kind} retrieval failed: {exc}")
    _PROJ_TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


@router.get("/api/projects/tree", summary="Project management hierarchy")
def get_projects_tree(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Project hierarchy forest: roots (not managed by another) with nested
    sub-projects (managedProjects children / managingProjects parents)."""
    return _cached_forest("hierarchy", "managedProjects", "managingProjects", url, server, user_id, user_pwd)


@router.get("/api/projects/dependencies", summary="Project dependency forest")
def get_projects_dependencies(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Project dependency forest: roots (projects nothing depends on) expanding to
    the projects they depend on (dependsOnProjects children / dependentProject
    parents, per the ProjectDependency relationship)."""
    return _cached_forest("dependencies", "dependsOnProjects", "dependentProject", url, server, user_id, user_pwd)


@router.get("/api/projects/{guid}", summary="Single project detail with child projects")
def get_project(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ProjectManager")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_project_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_project_by_guid failed")
        raise HTTPException(status_code=500, detail=f"Project detail failed: {exc}")

    project = _serialize_project(raw) if isinstance(raw, dict) else {}

    children = []
    try:
        raw_children = mgr.get_linked_projects(guid, output_format="JSON")
        if isinstance(raw_children, list):
            children = [_serialize_project(c) for c in raw_children if _type_name(c) == "Project"]
            children.sort(key=lambda p: (p.get("displayName") or "").lower())
    except Exception:
        pass  # children are best-effort

    return JSONResponse({"project": project, "children": children})
