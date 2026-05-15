"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Type System Explorer — FastAPI router.

Provides two endpoints:
  GET /egeria-explorer      → serves the single-page HTML explorer
  GET /api/types            → returns all type definitions as JSON
                              (optional ?area=N filter for entities)

Consumed by the type-explorer UI and can be called directly.
"""

import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from pyegeria import ValidMetadataManager, PyegeriaException
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
from loguru import logger

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# pyegeria bug: _async_get_all_classification_defs uses a hardcoded "typeDefList" key
# instead of _extract_typedef_list (which also checks "typeDefs" / "elements").
# Patch it to use the same robust helper as entity and relationship defs.
try:
    from pyegeria.core._globals import NO_ELEMENTS_FOUND as _NO_ELEMENTS_FOUND

    async def _patched_async_get_all_classification_defs(self, output_format="JSON", report_spec=None):
        url = (f"{self.platform_url}/servers/{self.view_server}"
               f"{self.valid_m_command_base}/open-metadata-types/classification-defs")
        resp = await self._async_make_request("GET", url)
        elements = self._extract_typedef_list(resp.json())
        if not elements:
            return _NO_ELEMENTS_FOUND
        if output_format != "JSON":
            return self._generate_entity_output(elements, None, "TypeDef", output_format, report_spec)
        return elements

    ValidMetadataManager._async_get_all_classification_defs = _patched_async_get_all_classification_defs
    logger.debug("Applied classification defs patch to ValidMetadataManager")
except Exception as _patch_err:
    logger.warning(f"Could not apply classification defs patch: {_patch_err}")

router = APIRouter(tags=["type-system"])

_HERE = Path(__file__).resolve().parent


# ── Connection ────────────────────────────────────────────────────────────────

def _env_defaults() -> dict:
    return dict(
        url     =os.environ.get("EGERIA_PLATFORM_URL",  "https://egeria-main:9443"),
        server  =os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id =os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd=os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )

def _get_client(url: str, server: str, user_id: str, user_pwd: str) -> ValidMetadataManager:
    logger.debug(f"Initializing ValidMetadataManager with url={url}, server={server}, user_id={user_id}")
    try:
        c = ValidMetadataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        c.create_egeria_bearer_token()
        return c
    except Exception as e:
        logger.error(f"Failed to initialize ValidMetadataManager: {e}")
        raise


# ── Area derivation ───────────────────────────────────────────────────────────
# The Egeria type API doesn't carry an "area" field; area is a documentation
# concept.  We derive it by walking up the supertype chain until we hit one of
# the anchor types below.  The mapping can be extended here as new areas are
# introduced without touching anything else.

AREA_ANCHORS: dict[str, int] = {
    # Area 0 — Foundation (OpenMetadataRoot, Referenceable, and base infrastructure)
    "OpenMetadataRoot": 0, "Referenceable": 0,
    "SecurityAccessControl": 0, "SecurityGroup": 0,
    # Area 1 — Collaboration (people, teams, organisations)
    "Actor": 1, "ContactDetails": 1, "PersonRole": 1, "UserIdentity": 1,
    "Team": 1, "Organization": 1,
    # Area 2 — Assets, Connectors & Infrastructure
    "Asset": 2, "Connection": 2, "ConnectorType": 2, "Endpoint": 2,
    "DeployedConnector": 2, "SoftwareCapability": 2, "ITInfrastructure": 2,
    # Area 3 — Glossary & Semantics
    "Glossary": 3, "GlossaryTerm": 3, "GlossaryCategory": 3,
    # Area 4 — Governance
    "GovernanceDefinition": 4, "GovernanceZone": 4, "SubjectAreaDefinition": 4,
    "GovernanceMetric": 4, "GovernanceDashboard": 4, "GovernanceExecutionPoint": 4,
    "GovernanceClassificationLevel": 4, "EngineAction": 4, "IncidentReport": 4,
    "ContextEvent": 4, "DataProcessingDescription": 4,
    # Area 5 — Schemas
    "SchemaType": 5, "SchemaAttribute": 5, "SchemaElement": 5,
    # Area 6 — Data Stores
    "DataStore": 6, "DataSet": 6, "DataFile": 6,
    # Area 7 — Lineage
    # Types whose supertype chain runs Referenceable→OpenMetadataRoot (area 0)
    # without passing through Process are listed here explicitly.
    "Process": 7, "Port": 7, "LineageMapping": 7,
    "InformationSupplyChain": 7, "InformationSupplyChainSegment": 7,
    "SolutionBlueprint": 7, "SolutionComponent": 7, "SolutionPort": 7,
}

AREA_NAMES: dict[int, str] = {
    0: "Foundation",
    1: "Collaboration",
    2: "Assets & Infrastructure",
    3: "Glossary",
    4: "Governance",
    5: "Schemas",
    6: "Data Stores",
    7: "Lineage",
}

def _derive_area(name: str, sup_map: dict, cache: dict) -> int:
    if name in cache:
        return cache[name]
    if name in AREA_ANCHORS:
        cache[name] = AREA_ANCHORS[name]
        return AREA_ANCHORS[name]
    sup = sup_map.get(name)
    result = _derive_area(sup, sup_map, cache) if sup else 0
    cache[name] = result
    return result


# ── TypeDef field normalisation ───────────────────────────────────────────────

def _attr_type_str(attr_type: dict) -> str:
    """Convert an Egeria attributeType dict to a readable string."""
    if not isinstance(attr_type, dict):
        return "unknown"
    cls  = attr_type.get("class", "")
    name = attr_type.get("name", "")
    if cls == "PrimitiveDef":
        return name or "string"
    if cls == "CollectionDef":
        args = attr_type.get("argumentTypes", [])
        if not isinstance(args, list):
            args = []
        kind = attr_type.get("collectionDefCategory", "")
        if "MAP" in kind and len(args) >= 2:
            arg0 = args[0] if isinstance(args[0], dict) else {}
            arg1 = args[1] if isinstance(args[1], dict) else {}
            k, v = arg0.get("name", "?"), arg1.get("name", "?")
            return f"map<{k},{v}>"
        if args:
            arg0 = args[0] if isinstance(args[0], dict) else {}
            return f"array<{arg0.get('name','?')}>"
        return name or "collection"
    if cls == "EnumDef":
        return f"enum:{name}"
    return name or cls

def _extract_props(td: dict) -> list[dict]:
    """Extract own properties; handles both attributeDefinitions and propertiesDefinition."""
    raw = td.get("attributeDefinitions") or td.get("propertiesDefinition") or []
    if not isinstance(raw, list):
        return []
    return [
        {
            "name":       p.get("attributeName", ""),
            "type":       _attr_type_str(p.get("attributeType") if isinstance(p.get("attributeType"), dict) else {}),
            "desc":       p.get("attributeDescription", ""),
            "req":        p.get("attributeCardinality") == "AT_LEAST_ONE",
            "unique":     p.get("unique", False),
            "deprecated": str(p.get("attributeStatus", "")).upper() in ("DEPRECATED_ATTRIBUTE", "DEPRECATED"),
        }
        for p in raw if isinstance(p, dict) and p.get("attributeName")
    ]

def _sup_name(td: dict) -> str | None:
    """Normalise superType which can be a plain string or a {name: ...} dict."""
    sup = td.get("superType")
    if isinstance(sup, dict):
        return sup.get("name")
    return sup or None

def _normalize_raw(raw, label: str) -> list[dict]:
    """Ensure we have a list of dictionaries, filtering out strings like 'No elements found'."""
    if not raw:
        return []
    if isinstance(raw, str):
        logger.debug(f"{label} (string): {raw}")
        return []
    if isinstance(raw, list):
        # Filter out any non-dict items (like the 'No elements found' string in a list)
        valid = [item for item in raw if isinstance(item, dict)]
        if len(valid) < len(raw):
            logger.debug(f"Filtered out {len(raw) - len(valid)} non-dict items from {label}")
        return valid
    logger.warning(f"Unexpected type for {label}: {type(raw)}")
    return []


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/egeria-explorer", include_in_schema=False)
async def egeria_explorer_ui():
    """Serve the Egeria Explorer single-page application."""
    html_path = _HERE / "type-explorer.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail=f"Egeria Explorer UI not found at {html_path}")
    return FileResponse(path=str(html_path), media_type="text/html")


@router.get("/api/types", summary="Get all open metadata type definitions")
def get_all_types(
    area: Optional[int] = Query(
        None,
        description="Filter entity types to a specific area (0–9). "
                    "Relationships and classifications are always returned in full.",
    ),
    url:      Optional[str] = Query(None, description="Egeria platform URL (overrides env)"),
    server:   Optional[str] = Query(None, description="Egeria view server name (overrides env)"),
    user_id:  Optional[str] = Query(None, description="Egeria user id (overrides env)"),
    user_pwd: Optional[str] = Query(None, description="Egeria user password (overrides env)"),
):
    """
    Return the complete Egeria open metadata type system.

    Entity types, relationship types, and classification types are returned
    as three separate dicts keyed by type name.  Entity types include an
    ``area`` field derived from the supertype chain, and a ``props`` list
    containing only the *own* properties; the UI computes inherited
    properties by walking the ``supertype`` chain client-side.
    """
    d = _env_defaults()
    url      = url      or d["url"]
    server   = server   or d["server"]
    user_id  = user_id  or d["user_id"]
    user_pwd = user_pwd or d["user_pwd"]

    try:
        c = _get_client(url, server, user_id, user_pwd)
        logger.debug("Fetching entity definitions...")
        entity_raw = _normalize_raw(c.get_all_entity_defs(), "Entity definitions")
        logger.debug(f"Fetched {len(entity_raw)} entity definitions")
        if entity_raw:
            sample = entity_raw[0]
            logger.info(f"Entity def sample keys: {list(sample.keys())}")
            logger.info(f"Entity def sample wiki: {sample.get('descriptionWiki', '<missing>')}")
        
        logger.debug("Fetching relationship definitions...")
        relationship_raw = _normalize_raw(c.get_all_relationship_defs(), "Relationship definitions")
        logger.debug(f"Fetched {len(relationship_raw)} relationship definitions")
        
        logger.debug("Fetching classification definitions...")
        classification_raw = _normalize_raw(c.get_all_classification_defs(), "Classification definitions")
        logger.debug(f"Fetched {len(classification_raw)} classification definitions")
        
        c.close_session()
    except PyegeriaException as exc:
        logger.exception(f"Pyegeria error in get_all_types: {exc}")
        raise HTTPException(status_code=502, detail=f"Egeria error: {exc}")
    except Exception as exc:
        logger.exception(f"Unexpected error in get_all_types: {exc}")
        raise HTTPException(status_code=500, detail=f"Type query failed: {exc}")

    # Build supertype map (needed for area derivation)
    sup_map: dict[str, str | None] = {
        td["name"]: _sup_name(td) for td in entity_raw if td.get("name")
    }
    area_cache: dict[str, int] = {}

    # ── Entities ──────────────────────────────────────────────────────────────
    entities: dict[str, dict] = {}
    for td in entity_raw:
        name = td.get("name")
        if not name:
            continue
        derived = _derive_area(name, sup_map, area_cache)
        if area is not None and derived != area:
            continue
        entities[name] = {
            "guid":       td.get("guid"),
            "area":       derived,
            "abstract":   td.get("isAbstract", False),
            "supertype":  sup_map.get(name),
            "desc":       td.get("description", ""),
            "wiki":       td.get("descriptionWiki", ""),
            "deprecated": str(td.get("status", "")).upper() in ("DEPRECATED_TYPEDEF", "DEPRECATED"),
            "props":      _extract_props(td),
        }

    # ── Relationships ─────────────────────────────────────────────────────────
    relationships: dict[str, dict] = {}
    for td in relationship_raw:
        name = td.get("name")
        if not name:
            continue
        e1  = td.get("endDef1")
        e2  = td.get("endDef2")
        e1 = e1 if isinstance(e1, dict) else {}
        e2 = e2 if isinstance(e2, dict) else {}
        et1 = e1.get("entityType")
        et2 = e2.get("entityType")
        et1 = et1 if isinstance(et1, dict) else {}
        et2 = et2 if isinstance(et2, dict) else {}
        relationships[name] = {
            "guid":       td.get("guid"),
            "desc":       td.get("description", ""),
            "wiki":       td.get("descriptionWiki", ""),
            "deprecated": str(td.get("status", "")).upper() in ("DEPRECATED_TYPEDEF", "DEPRECATED"),
            "end1":       et1.get("name") if isinstance(et1, dict) else et1,
            "end2":       et2.get("name") if isinstance(et2, dict) else et2,
            "role1":      e1.get("attributeName"),
            "role2":      e2.get("attributeName"),
            "props":      _extract_props(td),
        }

    # ── Classifications ───────────────────────────────────────────────────────
    classifications: dict[str, dict] = {}
    for td in classification_raw:
        name = td.get("name")
        if not name:
            continue
        valid_for = td.get("validEntityDefs") or []
        if not isinstance(valid_for, list):
            valid_for = []
        classifications[name] = {
            "guid":       td.get("guid"),
            "desc":       td.get("description", ""),
            "wiki":       td.get("descriptionWiki", ""),
            "deprecated": str(td.get("status", "")).upper() in ("DEPRECATED_TYPEDEF", "DEPRECATED"),
            "validFor":   [
                (v.get("name") if isinstance(v, dict) else v) for v in valid_for if v
            ],
            "props":      _extract_props(td),
        }

    return JSONResponse({
        "areaNames":       AREA_NAMES,
        "entities":        entities,
        "classifications": classifications,
        "relationships":   relationships,
    })