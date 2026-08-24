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

from common_serialize import _authored_fields, _header_summary, _generic_relationships, _classifications
from egeria_error_mapping import raise_egeria_http_error, EGERIA_ERROR_RESPONSES

router = APIRouter(tags=["projects"])

# ProjectManager.get_linked_projects routes through ServerClient._async_get_
# guid_request, whose dict-body branch validates against the base
# GetRequestBody Pydantic model -- and its `class` field is now a hardcoded
# Literal['GetRequestBody'] under pyegeria>=6.1.0, rejecting any real subclass
# name including RelationshipRequestBody (pyegeria's own method signature
# implies this is the expected class here). Found 2026-08-23 alongside the
# identical bug in solution_architect_handler.py (see its comment for the
# full writeup) -- filed as odpi/egeria-python#298, fixed in PR #299
# (class_ loosened from Literal to str) -- not yet released as of
# 2026-08-23 (BACKLOG.md PY-24). REVERT this workaround to a plain dict
# once that lands in a pyegeria release. Same interim workaround: build
# an already-constructed
# GetRequestBody *instance* via model_construct (skips validation entirely,
# unlike model_validate) with class_ overridden to the real subclass name.
def _relationship_request_body(as_of_time: Optional[str] = None):
    from datetime import datetime
    from pyegeria.models.models import GetRequestBody
    parsed_as_of = None
    if as_of_time:
        try:
            parsed_as_of = datetime.fromisoformat(as_of_time)
        except ValueError:
            parsed_as_of = as_of_time  # let it through as-is; a harmless serializer warning beats crashing
    return GetRequestBody.model_construct(class_="RelationshipRequestBody", as_of_time=parsed_as_of)


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ProjectManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ProjectManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
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


def _project_kinds(element: dict) -> list:
    """Project's ProjectKind classifications (Campaign/Task/PersonalProject/
    GovernanceProject/StudyProject/...) -- a real, distinct gap from
    common_serialize._classifications(), found live 2026-08-24 investigating
    "classifications aren't displayed": that helper only handles the common
    shape (one classification = one singular named key directly on
    elementHeader, e.g. elementHeader["Anchors"]). ProjectKind doesn't use
    that shape at all -- a project can carry MULTIPLE kinds simultaneously
    (confirmed live: "Clinical Trials Management" carries both Campaign and
    GovernanceProject), so Egeria groups them under one PLURAL list key,
    elementHeader["projectKinds"], instead. 23 of 30 live demo projects
    carry a real kind here -- this was a real, substantial, entirely
    invisible gap, not a missing-data non-issue like Anchors filtering was."""
    result = []
    for cls in (_header(element).get("projectKinds") or []):
        if not isinstance(cls, dict):
            continue
        cls_name = cls.get("classificationName") or (cls.get("type") or {}).get("typeName") or ""
        if not cls_name:
            continue
        cls_props_raw = cls.get("classificationProperties") or {}
        flat = {}
        if isinstance(cls_props_raw, dict):
            for k, v in cls_props_raw.items():
                if k in ("class", "typeName"):
                    continue
                if isinstance(v, list):
                    flat[k] = ", ".join(str(i) for i in v)
                elif not isinstance(v, dict):
                    flat[k] = str(v)
        result.append({"typeName": cls_name, "properties": flat})
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
        "classifications": _project_kinds(element) + _classifications(element),
        "_header":        _header_summary(element),
        **_authored_fields(element),
        "relationships":  _generic_relationships(element),
    }


@router.get("/api/projects", summary="List all projects", responses=EGERIA_ERROR_RESPONSES)
def get_projects(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create ProjectManager")

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
        raise_egeria_http_error(exc, "find_projects failed")

    if not raw or not isinstance(raw, list):
        return JSONResponse({"projects": [], "total": 0})

    if not include_templates:
        raw = [p for p in raw if not _is_template(p)]

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


def _project_forest(mgr, child_key: str, parent_key: str, as_of_time=None) -> dict:
    """Build a project forest from a single depth-1 find. child_key/parent_key are
    the downward/upward relationship attribute names (e.g. managedProjects /
    managingProjects for hierarchy, or dependsOnProjects / dependentProject for
    dependencies). Roots are projects with no parent edge; cycles are guarded."""
    raw = mgr.find_projects(
        search_string="*", starts_with=True, output_format="JSON",
        start_from=0, page_size=500, graph_query_depth=1,
        sequencing_order="PROPERTY_ASCENDING", sequencing_property="displayName",
        as_of_time=as_of_time or None,
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


def _cached_forest(kind: str, child_key: str, parent_key: str, url, server, user_id, user_pwd, as_of_time=None):
    cache_key = f"{kind}|{url or ''}|{server or ''}|{user_id or ''}|{as_of_time or ''}"
    cached = _PROJ_TREE_CACHE.get(cache_key)
    if cached and (time.time() - cached[0]) < _PROJ_TREE_TTL:
        return JSONResponse(cached[1])
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create ProjectManager")
    try:
        result = _project_forest(mgr, child_key, parent_key, as_of_time)
    except Exception as exc:
        raise_egeria_http_error(exc, f"project {kind} forest failed")
    _PROJ_TREE_CACHE[cache_key] = (time.time(), result)
    return JSONResponse(result)


@router.get("/api/projects/tree", summary="Project management hierarchy", responses=EGERIA_ERROR_RESPONSES)
def get_projects_tree(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """Project hierarchy forest: roots (not managed by another) with nested
    sub-projects (managedProjects children / managingProjects parents)."""
    return _cached_forest("hierarchy", "managedProjects", "managingProjects", url, server, user_id, user_pwd, as_of_time)


@router.get("/api/projects/dependencies", summary="Project dependency forest", responses=EGERIA_ERROR_RESPONSES)
def get_projects_dependencies(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    """Project dependency forest: roots (projects nothing depends on) expanding to
    the projects they depend on (dependsOnProjects children / dependentProject
    parents, per the ProjectDependency relationship)."""
    return _cached_forest("dependencies", "dependsOnProjects", "dependentProject", url, server, user_id, user_pwd, as_of_time)


@router.get("/api/projects/{guid}", summary="Single project detail with child projects", responses=EGERIA_ERROR_RESPONSES)
def get_project(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create ProjectManager")

    try:
        # graphQueryDepth=2 so relationship arrays (resources, dependencies, etc.)
        # are present for _generic_relationships to surface — without it the
        # response has no relationship keys to extract at all.
        body = {"class": "GetRequestBody", "graphQueryDepth": 2}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = mgr.get_project_by_guid(guid, output_format="JSON", body=body)
    except Exception as exc:
        raise_egeria_http_error(exc, "get_project_by_guid failed")

    project = _serialize_project(raw) if isinstance(raw, dict) else {}

    children = []
    try:
        child_body = _relationship_request_body(as_of_time)
        raw_children = mgr.get_linked_projects(guid, output_format="JSON", body=child_body)
        if isinstance(raw_children, list):
            children = [_serialize_project(c) for c in raw_children if _type_name(c) == "Project"]
            children.sort(key=lambda p: (p.get("displayName") or "").lower())
    except Exception:
        pass  # children are best-effort

    return JSONResponse({"project": project, "children": children})
