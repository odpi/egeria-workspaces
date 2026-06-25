"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Governance Definitions Explorer — FastAPI router.

Uses GovernanceOfficer to search and retrieve governance definitions.
Definitions are organised into three parent groups:
  GovernanceDriver  – strategies, business imperatives, regulations, threats
  GovernancePolicy  – approaches, principles
  GovernanceControl – technical controls, organisational controls, notification types

Endpoints:
  GET /api/governance/tree               → type hierarchy (3 root groups + subtypes)
  GET /api/governance/definitions        → search/list definitions (filter by typeName)
  GET /api/governance/definitions/{guid} → full detail for one governance definition
"""

import os
import re
import time
from egeria_auth import apply_token
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["governance"])

# ── Type hierarchy ────────────────────────────────────────────────────────────

GOV_TYPE_TREE = [
    {
        "typeName": "GovernanceDriver",
        "label": "Governance Drivers",
        "isAbstract": True,
        "children": [
            {"typeName": "BusinessImperative", "label": "Business Imperatives"},
            {"typeName": "GovernanceStrategy", "label": "Governance Strategies"},
            {
                "typeName": "Regulation",
                "label": "Regulations",
                "children": [
                    {"typeName": "RegulationArticle", "label": "Regulation Articles"},
                ],
            },
            {"typeName": "Threat", "label": "Threats"},
        ],
    },
    {
        "typeName": "GovernancePolicy",
        "label": "Governance Policies",
        "isAbstract": True,
        "children": [
            {"typeName": "GovernanceApproach",   "label": "Governance Approaches"},
            {"typeName": "GovernanceObligation", "label": "Governance Obligations"},
            {"typeName": "GovernancePrinciple",  "label": "Governance Principles"},
        ],
    },
    {
        "typeName": "GovernanceControl",
        "label": "Governance Controls",
        "isAbstract": True,
        "children": [
            {"typeName": "DataLens",              "label": "Data Lenses"},
            {"typeName": "DataProcessingPurpose", "label": "Data Processing Purposes"},
            {"typeName": "ExceptionType",         "label": "Exception Types"},
            {
                "typeName": "GovernanceActionType",
                "label": "Governance Action Types",
                "children": [
                    {"typeName": "GovernanceActionProcess", "label": "Governance Action Processes"},
                ],
            },
            {"typeName": "GovernanceMetric",      "label": "Governance Metrics"},
            {
                "typeName": "GovernanceProcedure",
                "label": "Governance Procedures",
                "children": [
                    {"typeName": "Methodology", "label": "Methodologies"},
                ],
            },
            {"typeName": "GovernanceResponsibility", "label": "Governance Responsibilities"},
            {
                "typeName": "GovernanceRule",
                "label": "Governance Rules",
                "children": [
                    {"typeName": "NamingStandardRule", "label": "Naming Standard Rules"},
                ],
            },
            {"typeName": "NotificationType",  "label": "Notification Types"},
            {"typeName": "Requirement",       "label": "Requirements"},
            {"typeName": "ResearchQuestion",  "label": "Research Questions"},
            {
                "typeName": "SecurityAccessControl",
                "label": "Security Access Controls",
                "children": [
                    {"typeName": "GovernanceZone",       "label": "Governance Zones"},
                    {"typeName": "ServiceAccessControl", "label": "Service Access Controls"},
                ],
            },
            {
                "typeName": "TermsAndConditions",
                "label": "Terms and Conditions",
                "children": [
                    {"typeName": "CertificationType",     "label": "Certification Types"},
                    {"typeName": "LicenseType",           "label": "License Types"},
                    {"typeName": "ServiceLevelObjective", "label": "Service Level Objectives"},
                ],
            },
        ],
    },
]


_TREE_CACHE: dict = {"value": None, "ts": 0.0}
_TREE_TTL = 300  # seconds


def _camel_to_label(name: str) -> str:
    """Convert CamelCase type name to a pluralised display label.

    GovernanceActionType  → "Governance Action Types"
    SecurityAccessControl → "Security Access Controls"
    """
    words = re.sub(r"([A-Z])", r" \1", name).split()
    if not words:
        return name
    last = words[-1]
    if last.endswith("y") and not last[-2:] in ("ay", "ey", "oy", "uy"):
        last = last[:-1] + "ies"
    elif last.endswith(("s", "sh", "ch", "x", "z")):
        last = last + "es"
    else:
        last = last + "s"
    words[-1] = last
    return " ".join(words)


def _build_gov_tree() -> list:
    """Build the GovernanceDefinition subtype tree from the live Egeria type system.

    Returns a list of root-level nodes (children of GovernanceDefinition) where
    each node is: {"typeName": str, "label": str, "isAbstract": bool, "children": [...]}.
    Falls back to GOV_TYPE_TREE if the type system is unavailable.
    """
    now = time.monotonic()
    if _TREE_CACHE["value"] is not None and (now - _TREE_CACHE["ts"]) < _TREE_TTL:
        return _TREE_CACHE["value"]

    try:
        from pyegeria import ValidMetadataManager
        d = _env_defaults()
        c = ValidMetadataManager(
            view_server=d["server"],
            platform_url=d["url"],
            user_id=d["user_id"],
            user_pwd=d["user_pwd"],
        )
        apply_token(c)
        raw = c.get_all_entity_defs()
    except Exception as exc:
        logger.warning(f"_build_gov_tree: could not fetch type defs ({exc}); using fallback")
        return GOV_TYPE_TREE

    if not isinstance(raw, list):
        raw = []

    type_meta: dict[str, dict] = {}
    sup_map: dict[str, str | None] = {}
    children_map: dict[str, list[str]] = {}

    for td in raw:
        if not isinstance(td, dict):
            continue
        name = td.get("name", "")
        if not name:
            continue
        sup_raw = td.get("superType")
        sup = sup_raw.get("name") if isinstance(sup_raw, dict) else (sup_raw or None)
        sup_map[name] = sup
        type_meta[name] = {
            "isAbstract": bool(td.get("isAbstract", False)),
        }

    for name, sup in sup_map.items():
        if sup:
            children_map.setdefault(sup, []).append(name)

    def _build_node(type_name: str) -> dict:
        meta = type_meta.get(type_name, {})
        children_names = sorted(children_map.get(type_name, []))
        node: dict = {
            "typeName": type_name,
            "label": _camel_to_label(type_name),
        }
        if meta.get("isAbstract"):
            node["isAbstract"] = True
        if children_names:
            node["children"] = [_build_node(c) for c in children_names]
        return node

    # GovernanceDefinition is abstract and the root; return its children as roots
    gov_children = sorted(children_map.get("GovernanceDefinition", []))
    if not gov_children:
        logger.warning("_build_gov_tree: no subtypes of GovernanceDefinition found; using fallback")
        return GOV_TYPE_TREE

    tree = [_build_node(c) for c in gov_children]
    _TREE_CACHE["value"] = tree
    _TREE_CACHE["ts"] = now
    logger.info(f"_build_gov_tree: built dynamic tree with {len(tree)} root nodes")
    return tree


def _env_defaults() -> dict:
    return dict(
        url     =os.environ.get("EGERIA_PLATFORM_URL",  "https://egeria-main:9443"),
        server  =os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id =os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd=os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import GovernanceOfficer
    d = _env_defaults()
    url      = url      or d["url"]
    server   = server   or d["server"]
    user_id  = user_id  or d["user_id"]
    user_pwd = user_pwd or d["user_pwd"]
    mgr = GovernanceOfficer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _list_to_str(v) -> str:
    """Flatten list values (implications, outcomes, results) into a newline string."""
    if isinstance(v, list):
        return "\n".join(str(i) for i in v if i)
    return str(v) if v is not None else ""


def _serialize_list_item(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    return {
        "guid":          header.get("guid", ""),
        "typeName":      _type_name(element),
        "displayName":   props.get("displayName") or props.get("name") or "",
        "qualifiedName": props.get("qualifiedName") or "",
        "description":   props.get("description") or "",
        "identifier":    props.get("identifier") or "",
        "domainIdentifier": props.get("domainIdentifier") or "",
        "summary":       props.get("summary") or "",
    }


def _serialize_detail(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)

    def sv(key):
        v = props.get(key)
        if isinstance(v, list):
            return _list_to_str(v)
        return str(v) if v not in (None, "") else ""

    node = {
        "guid":             header.get("guid", ""),
        "typeName":         _type_name(element),
        "displayName":      props.get("displayName") or props.get("name") or "",
        "qualifiedName":    sv("qualifiedName"),
        "description":      sv("description"),
        "identifier":       sv("identifier"),
        "summary":          sv("summary"),
        "scope":            sv("scope"),
        "usage":            sv("usage"),
        "domainIdentifier": sv("domainIdentifier"),
        "importance":       sv("importance"),
        "implications":     sv("implications"),
        "outcomes":         sv("outcomes"),
        "results":          sv("results"),
        "status":           (header.get("status") or ""),
        "mermaidGraph":     element.get("mermaidGraph") or "",
    }

    # Collect all relationship lists
    skip = {"class", "elementHeader", "properties", "mermaidGraph"}
    relationships = {}
    for key, val in element.items():
        if key in skip or not isinstance(val, list) or not val:
            continue
        items = []
        for entry in val:
            re = entry.get("relatedElement") or {}
            rh = re.get("elementHeader") or {}
            rp = re.get("properties") or {}
            g  = rh.get("guid") or ""
            if not g:
                # some entries expose the element directly
                rh = entry.get("elementHeader") or {}
                rp = entry.get("properties") or {}
                g  = rh.get("guid") or ""
            if g:
                rtype = rh.get("type") or {}
                items.append({
                    "guid":           g,
                    "typeName":       rtype.get("typeName") or "",
                    "superTypeNames": rtype.get("superTypeNames") or [],
                    "displayName":    rp.get("displayName") or rp.get("name") or "",
                    "qualifiedName":  rp.get("qualifiedName") or "",
                    "description":    rp.get("description") or "",
                })
        if items:
            relationships[key] = items

    node["relationships"] = relationships
    return node


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/governance/tree", summary="Governance definition type hierarchy")
def get_tree():
    return JSONResponse(_build_gov_tree())


@router.get("/api/governance/definitions", summary="Search/list governance definitions")
def find_definitions(
    type_name:     Optional[str] = Query(None),
    search_string: Optional[str] = Query(None),
    start_from:    int           = Query(0,   ge=0),
    page_size:     int           = Query(200, ge=1, le=500),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return governance definitions, optionally filtered by type and search string."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    q   = search_string or "*"
    tn  = type_name or "GovernanceDefinition"
    kwargs = {}
    if tn not in ("GovernanceDefinition", ""):
        kwargs["metadata_element_type"] = tn

    try:
        raw = mgr.find_governance_definitions(
            search_string=q,
            starts_with=True,
            ignore_case=True,
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            sequencing_order="PROPERTY_ASCENDING",
            sequencing_property="displayName",
            **kwargs,
        )
    except Exception as exc:
        logger.exception("find_governance_definitions failed")
        raise HTTPException(status_code=500, detail=str(exc))

    if not isinstance(raw, list):
        raw = []

    items = [_serialize_list_item(el) for el in raw]
    items.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"definitions": items, "total": len(items), "type_name": tn})


@router.get("/api/governance/definitions/{guid}", summary="Get a governance definition by GUID")
def get_definition(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a single governance definition, including relationships."""
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        raw = mgr.get_governance_definition_by_guid(guid, output_format="JSON")
    except Exception as exc:
        logger.exception("get_governance_definition_by_guid failed")
        raise HTTPException(status_code=500, detail=str(exc))

    if not raw:
        raise HTTPException(status_code=404, detail=f"Definition {guid!r} not found")

    # get_governance_definition_by_guid may return a list or a dict
    element = raw[0] if isinstance(raw, list) else raw
    return JSONResponse(_serialize_detail(element))
