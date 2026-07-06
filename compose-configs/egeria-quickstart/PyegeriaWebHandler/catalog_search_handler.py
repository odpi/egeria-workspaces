"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Global catalog search — FastAPI router.

Endpoints:
  GET /api/catalog/search?q=...  → cross-type keyword search via ClassificationExplorer
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token
from pyegeria.omvs.classification_explorer import ClassificationExplorer

router = APIRouter(tags=["catalog-search"])

# Properties searched across all element types
_SEARCH_PROPS = ["displayName", "qualifiedName", "description", "name"]

# Maximum results returned per search (keep snappy; caller can increase via page_size)
_DEFAULT_PAGE_SIZE = 100

# Map from Egeria typeName → UI category bucket.
# Keys are exact typeNames; values are {id, label} matching the tech-catalog SECTIONS/TABS.
# Types not listed fall into "other".
_TYPE_CATEGORY: dict[str, dict] = {
    # Glossary
    "Glossary":          {"id": "glossary",    "label": "Glossary"},
    "GlossaryCategory":  {"id": "glossary",    "label": "Glossary"},
    "GlossaryTerm":      {"id": "glossary",    "label": "Glossary"},
    # Technology types
    "TechnologyType":           {"id": "tech-types", "label": "Technology Types"},
    "DeployedImplementationType": {"id": "tech-types", "label": "Technology Types"},
    # Infrastructure
    "ITInfrastructure":         {"id": "infrastructure", "label": "Infrastructure"},
    "Host":                     {"id": "infrastructure", "label": "Infrastructure"},
    "BareMetalComputer":        {"id": "infrastructure", "label": "Infrastructure"},
    "VirtualMachine":           {"id": "infrastructure", "label": "Infrastructure"},
    "VirtualContainer":         {"id": "infrastructure", "label": "Infrastructure"},
    "HostCluster":              {"id": "infrastructure", "label": "Infrastructure"},
    "StorageVolume":            {"id": "infrastructure", "label": "Infrastructure"},
    "Server":                   {"id": "infrastructure", "label": "Infrastructure"},
    "SoftwareCapability":       {"id": "infrastructure", "label": "Infrastructure"},
    "DataEngine":               {"id": "infrastructure", "label": "Infrastructure"},
    "DatabaseManager":          {"id": "infrastructure", "label": "Infrastructure"},
    "FileSystem":               {"id": "infrastructure", "label": "Infrastructure"},
    "EventBroker":              {"id": "infrastructure", "label": "Infrastructure"},
    "Endpoint":                 {"id": "infrastructure", "label": "Infrastructure"},
    "Connection":               {"id": "infrastructure", "label": "Infrastructure"},
    "VirtualConnection":        {"id": "infrastructure", "label": "Infrastructure"},
    "ConnectorType":            {"id": "infrastructure", "label": "Infrastructure"},
    # Data assets
    "DataStore":                {"id": "data-assets", "label": "Data Assets"},
    "Database":                 {"id": "data-assets", "label": "Data Assets"},
    "RelationalDatabase":       {"id": "data-assets", "label": "Data Assets"},
    "DataFile":                 {"id": "data-assets", "label": "Data Assets"},
    "CSVFile":                  {"id": "data-assets", "label": "Data Assets"},
    "SpreadsheetFile":          {"id": "data-assets", "label": "Data Assets"},
    "DataFileCollection":       {"id": "data-assets", "label": "Data Assets"},
    "DataFolder":               {"id": "data-assets", "label": "Data Assets"},
    "DataSet":                  {"id": "data-assets", "label": "Data Assets"},
    "RelationalTable":          {"id": "data-assets", "label": "Data Assets"},
    "RelationalColumn":         {"id": "data-assets", "label": "Data Assets"},
    "DataFeed":                 {"id": "data-assets", "label": "Data Assets"},
    "Topic":                    {"id": "data-assets", "label": "Data Assets"},
    "KafkaTopic":               {"id": "data-assets", "label": "Data Assets"},
    "SchemaType":               {"id": "data-assets", "label": "Data Assets"},
    "TabularSchemaType":        {"id": "data-assets", "label": "Data Assets"},
    "RelationalDBSchemaType":   {"id": "data-assets", "label": "Data Assets"},
    # APIs
    "DeployedAPI":              {"id": "apis", "label": "APIs"},
    "APISchemaType":            {"id": "apis", "label": "APIs"},
    "APIOperation":             {"id": "apis", "label": "APIs"},
    # Processes
    "DeployedSoftwareComponent": {"id": "processes", "label": "Processes"},
    "Application":              {"id": "processes", "label": "Processes"},
    "DataMovementEngine":       {"id": "processes", "label": "Processes"},
    "GovernanceActionProcess":  {"id": "processes", "label": "Processes"},
    "GovernanceActionType":     {"id": "processes", "label": "Processes"},
    "EngineAction":             {"id": "processes", "label": "Processes"},
    "GovernanceActionProcessInstance": {"id": "processes", "label": "Processes"},
    # Projects (Campaign/StudyProject/PersonalProject/Task/GlossaryProject are
    # classifications on a Project entity, not distinct typeNames — so "Project"
    # alone covers all of them here).
    "Project":                  {"id": "projects", "label": "Projects"},
    # Surveys
    "SurveyReport":             {"id": "surveys", "label": "Surveys", "tab": "survey-reports"},
    "Annotation":               {"id": "surveys", "label": "Surveys", "tab": "annotations"},
    "SchemaAnalysisAnnotation": {"id": "surveys", "label": "Surveys", "tab": "annotations"},
    "ResourceMeasureAnnotation": {"id": "surveys", "label": "Surveys", "tab": "annotations"},
    "DataFieldAnnotation":      {"id": "surveys", "label": "Surveys", "tab": "annotations"},
    "ClassificationAnnotation": {"id": "surveys", "label": "Surveys", "tab": "annotations"},
    "QualityAnnotation":        {"id": "surveys", "label": "Surveys", "tab": "annotations"},
}

_CATEGORY_ORDER = [
    "glossary", "tech-types", "data-assets", "infrastructure", "apis", "processes", "projects", "surveys", "other",
]

_CATEGORY_LABELS = {
    "glossary":     "Glossary",
    "tech-types":   "Technology Types",
    "data-assets":  "Data Assets",
    "infrastructure": "Infrastructure",
    "apis":         "APIs",
    "processes":    "Processes",
    "projects":     "Projects",
    "surveys":      "Surveys",
    "other":        "Other",
}


def _creds(url, server, user_id, user_pwd):
    return (
        url      or os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
        server   or os.environ.get("EGERIA_VIEW_SERVER",  "qs-view-server"),
        user_id  or os.environ.get("EGERIA_USER",         "erinoverview"),
        user_pwd or os.environ.get("EGERIA_USER_PASSWORD","secret"),
    )


def _classification_explorer(url, server, user_id, user_pwd):
    resolved_url, resolved_server, resolved_uid, resolved_pwd = _creds(url, server, user_id, user_pwd)
    ce = ClassificationExplorer(
        view_server=resolved_server,
        platform_url=resolved_url,
        user_id=resolved_uid,
        user_pwd=resolved_pwd,
    )
    apply_token(ce)
    return ce


def _serialize_search_result(el: dict) -> Optional[dict]:
    """Serialize a ClassificationExplorer element to a lightweight search result."""
    if not isinstance(el, dict):
        return None
    hdr   = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    type_info = hdr.get("type") or {}
    type_name = type_info.get("typeName") or props.get("typeName") or ""
    guid = hdr.get("guid") or ""
    display_name = (
        props.get("displayName") or
        props.get("name") or
        props.get("qualifiedName") or
        guid
    )
    qualified_name = props.get("qualifiedName") or ""
    description = props.get("description") or ""

    cat_info = _TYPE_CATEGORY.get(type_name, {"id": "other", "label": "Other"})
    result = {
        "guid":          guid,
        "typeName":      type_name,
        "superTypeNames": type_info.get("superTypeNames") or [],
        "displayName":   display_name,
        "qualifiedName": qualified_name,
        "description":   description,
        "categoryId":    cat_info["id"],
        "categoryLabel": cat_info["label"],
    }
    if "tab" in cat_info:
        result["tab"] = cat_info["tab"]
    return result


@router.get("/api/catalog/search")
def catalog_search(
    q: str = Query(..., min_length=1, description="Search query"),
    page_size: int = Query(_DEFAULT_PAGE_SIZE, ge=1, le=500),
    url: Optional[str] = Query(None),
    server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Search across all element types using ClassificationExplorer.

    Returns results grouped by category (glossary, data-assets, infrastructure, etc.).
    Each item includes guid, typeName, displayName, qualifiedName, description, and
    categoryId/categoryLabel for routing to the correct section in the UI.
    """
    # Egeria treats '*' as None in the request body → 400 error.
    if q.strip() in ("*", ""):
        raise HTTPException(status_code=400, detail="Wildcard '*' search is not supported. Enter a specific search term.")
    try:
        ce = _classification_explorer(url, server, user_id, user_pwd)
        raw = ce.find_elements_by_property_value(
            property_value=q,
            property_names=_SEARCH_PROPS,
            starts_with=False,
            ends_with=False,
            ignore_case=True,
            page_size=page_size,
            output_format="JSON",
        )
    except Exception as exc:
        logger.exception("catalog_search failed for q=%r", q)
        raise HTTPException(status_code=500, detail=str(exc))

    items = []
    for el in (raw if isinstance(raw, list) else []):
        r = _serialize_search_result(el)
        if r:
            items.append(r)

    # Deduplicate by GUID (search may return duplicates across property matches)
    seen: set[str] = set()
    unique: list[dict] = []
    for item in items:
        key = item["guid"] or item["qualifiedName"]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Group by category in defined order
    by_cat: dict[str, list] = {cid: [] for cid in _CATEGORY_ORDER}
    for item in unique:
        cat = item["categoryId"] if item["categoryId"] in by_cat else "other"
        by_cat[cat].append(item)

    groups = [
        {
            "categoryId":    cid,
            "categoryLabel": _CATEGORY_LABELS[cid],
            "items":         by_cat[cid],
            "count":         len(by_cat[cid]),
        }
        for cid in _CATEGORY_ORDER
        if by_cat[cid]
    ]

    return JSONResponse({
        "query":  q,
        "total":  len(unique),
        "groups": groups,
    })
