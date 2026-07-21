"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Technical Asset Catalog — FastAPI router.

Serves the tech-catalog SPA and provides backend API endpoints for all
nine asset-type sections defined in technical_data_catalog_spec.md.

Endpoints:
  GET /tech-catalog                              → serve tech-catalog.html SPA
  GET /api/tech-catalog/infrastructure           → ITInfrastructure assets
  GET /api/tech-catalog/software-capabilities    → SoftwareCapability elements
  GET /api/tech-catalog/endpoints                → Endpoint elements
  GET /api/tech-catalog/data-stores              → DataStore assets
  GET /api/tech-catalog/data-feeds               → DataFeed assets
  GET /api/tech-catalog/data-sets                → DataSet assets
  GET /api/tech-catalog/apis                     → DeployedAPI assets
  GET /api/tech-catalog/software-components      → DeployedSoftwareComponent processes
  GET /api/tech-catalog/actions                  → Action processes
  GET /api/tech-catalog/assets/{guid}            → detail for any element by GUID
  GET /api/tech-catalog/assets/{guid}/schema     → schema type + attribute tree (depth=5)
  GET /api/tech-catalog/assets/{guid}/lineage    → lineage graph via AssetCatalog

  GET /api/tech-catalog/tech-types               → list / search technology types
  GET /api/tech-catalog/tech-types/hierarchy     → hierarchy tree from root
  GET /api/tech-catalog/tech-types/{qualifiedName}          → detail by qualifiedName
  GET /api/tech-catalog/tech-types/{qualifiedName}/elements → catalog instances of this type

  GET /api/tech-catalog/survey-reports                        → SurveyReport assets
  GET /api/tech-catalog/survey-reports/{guid}/annotations     → Annotations for a report
  GET /api/tech-catalog/annotations                           → All/searched Annotations
  GET /api/tech-catalog/survey-types                          → Survey type definitions (aggregated from TechnologyTypes)
"""

import os
import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from common_serialize import _authored_fields, _header_summary

router = APIRouter(tags=["tech-catalog"])

_HERE = Path(__file__).parent
_HTML = _HERE / "tech-catalog.html"

_SEQ_ORDER = "PROPERTY_ASCENDING"
_SEQ_PROP  = "displayName"

# Mermaid graph fields Egeria may embed in an element response.
# Must stay in sync with _ALL_MERMAID_FIELDS in tech-catalog.html and mermaid_handler.py.
_MERMAID_FIELDS = {
    "mermaidGraph", "anchorMermaidGraph", "edgeMermaidGraph",
    "localLineageGraph", "fieldLevelLineageGraph",
    "informationSupplyChainMermaidGraph", "iscImplementationMermaidGraph",
    "actionMermaidGraph", "specificationMermaidGraph",
    "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph",
    "collectionMermaidMindMap",
}


# ── Credential helpers ────────────────────────────────────────────────────────

def _creds(url, server, user_id, user_pwd):
    return (
        url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443"),
        server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id  or os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _token_from_request(request: Request) -> Optional[str]:
    """Extract pre-obtained Egeria bearer token from X-Egeria-Token header."""
    return request.headers.get("X-Egeria-Token") or None


def _apply_token(client, token: Optional[str]):
    """Set a pre-obtained bearer token on a pyegeria client, or obtain a fresh one."""
    if token:
        client.set_bearer_token(token)
    else:
        client.create_egeria_bearer_token()


def _is_auth_error(exc: Exception) -> bool:
    """Return True if exc represents a 401/403 from Egeria (token expired or access denied)."""
    http_code = getattr(exc, "response_code", None) or getattr(exc, "http_status_code", None)
    if http_code in (401, 403):
        return True
    s = str(exc).upper()
    return "USER_NOT_AUTHORIZED" in s or "NOT_AUTHORIZED" in s or "AUTHORIZATION_ERROR" in s


def _asset_maker(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import AssetMaker
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = AssetMaker(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(mgr, token)
    return mgr


def _connection_maker(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import ConnectionMaker
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = ConnectionMaker(server_name=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(mgr, token)
    return mgr


def _governance_officer(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import GovernanceOfficer
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    mgr = GovernanceOfficer(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(mgr, token)
    return mgr


# ── Serialisation ─────────────────────────────────────────────────────────────

def _header(el):
    return el.get("elementHeader") or {}

def _props(el):
    return el.get("properties") or {}

def _type_name(el):
    return (_header(el).get("type") or {}).get("typeName", "")

def _is_mermaid_key(key: str) -> bool:
    kl = key.lower()
    return ("mermaid" in kl or kl.endswith("graph") or kl.endswith("mindmap")
            or kl.endswith("piechart") or kl.endswith("chart"))

# Classifications that are internal infrastructure — never shown in the UI.
_SKIP_CLASSIFICATIONS = frozenset([
    "Anchors", "LatestChange", "Memento", "TemplateSubstitute", "SpineObject",
    "SpineAttribute", "ObjectIdentifier",
])

def _extract_classifications(header: dict) -> list:
    """Extract governance/business classifications from an elementHeader dict.

    In pyegeria's JSON output, each classification is a named key directly on
    elementHeader (e.g. "dataAssetEncoding", "zoneMembership"), not in a
    "classifications" list.  Every such value has class="ElementClassification"
    and carries classificationName + classificationProperties.
    """
    result = []
    for key, val in header.items():
        if not isinstance(val, dict):
            continue
        if val.get("class") != "ElementClassification":
            continue
        cls_name = (val.get("classificationName")
                    or (val.get("type") or {}).get("typeName")
                    or (key[0].upper() + key[1:]))
        if not cls_name or cls_name in _SKIP_CLASSIFICATIONS:
            continue
        cls_props_raw = val.get("classificationProperties") or {}
        flat = {}
        if isinstance(cls_props_raw, dict):
            for k, v in cls_props_raw.items():
                if k in ("class", "typeName"):
                    continue
                if isinstance(v, list):
                    flat[k] = ", ".join(str(i) for i in v)
                elif not isinstance(v, (dict,)):
                    flat[k] = str(v)
        result.append({"typeName": cls_name, "properties": flat})
    return result


def _is_template(element: dict) -> bool:
    """Return True if the element carries the Egeria 'Template' classification."""
    for val in (element.get("elementHeader") or {}).values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


def _flat_props(props_dict: dict) -> dict:
    """Flatten a properties dict that may use propertyValueMap encoding."""
    flat = {}
    prop_map = props_dict.get("propertyValueMap") or {}
    if prop_map:
        for k, v in prop_map.items():
            pv = v.get("primitiveValue", "") if isinstance(v, dict) else v
            # primitiveValue can itself be a nested object — always stringify
            flat[k] = str(pv) if not isinstance(pv, (dict, list)) else ", ".join(str(i) for i in pv) if isinstance(pv, list) else ""
    else:
        for k, v in props_dict.items():
            if k not in ("class", "propertyValueMap", "propertiesAsStrings"):
                flat[k] = str(v) if not isinstance(v, (dict, list)) else ""
    return {k: v for k, v in flat.items() if v}


def _unwrap_rel_item(item: dict, key: str) -> Optional[dict]:
    """
    Convert one RelatedMetadataElementSummary into a normalised relationship dict,
    or return None if the item doesn't look like a relationship.
    """
    _ITEM_META = {"relationshipHeader", "relationshipProperties",
                  "relatedElement", "relatedElementAtEnd1", "class"}
    rel_hdr = item.get("relationshipHeader")
    if not isinstance(rel_hdr, dict):
        return None
    rel_type = (rel_hdr.get("type") or {}).get("typeName") or key
    rel_props_raw = item.get("relationshipProperties") or {}
    rel_props = _flat_props(rel_props_raw) if rel_props_raw else {}
    nested = item.get("relatedElement")
    if isinstance(nested, dict) and "elementHeader" in nested:
        elem = nested
    else:
        elem = {k: v for k, v in item.items() if k not in _ITEM_META}
    elem_hdr  = _header(elem)
    elem_props = _props(elem)
    type_info  = elem_hdr.get("type") or {}
    # Some related types (e.g. Annotation) have no displayName/name of their own —
    # fall back through summary/qualifiedName before finally falling back to guid,
    # so relationship cards don't just show a raw GUID.
    display_name = (
        elem_props.get("displayName")
        or elem_props.get("name")
        or elem_props.get("summary")
        or elem_props.get("qualifiedName")
        or elem_hdr.get("guid", "")
    )
    # Pass through the related element's remaining scalar properties so relationship
    # cards can show useful detail (e.g. an Annotation's annotationType/confidence)
    # beyond just displayName/description — especially valuable for types like
    # Annotation that have no displayName of their own.
    _skip_extra = {"class", "displayName", "name", "description", "qualifiedName"}
    extra_props = {}
    for k, v in elem_props.items():
        if k in _skip_extra:
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            extra_props[k] = v
        elif isinstance(v, str) and v.strip():
            extra_props[k] = v
    return {
        "relationshipType": rel_type,
        "relationshipProperties": rel_props,
        "relatedElement": {
            "guid":        elem_hdr.get("guid", ""),
            "typeName":    type_info.get("typeName", ""),
            "superTypes":  type_info.get("superTypeNames") or [],
            "displayName": display_name,
            "description": elem_props.get("description") or "",
            "properties":  extra_props,
        },
    }


def _extract_relationships(el: dict) -> list:
    """
    Extract peer relationships from a graph-queried element.

    Handles both:
    - List-valued keys: each item is a RelatedMetadataElementSummary
    - Single-dict keys: e.g. 'schemaType' which is a single RelatedMetadataElementSummary
    """
    _SKIP_KEYS = {"elementHeader", "properties", "classifications", "class"}
    result = []
    for key, val in el.items():
        if key in _SKIP_KEYS:
            continue
        # Single-dict relationship (e.g. schemaType)
        if isinstance(val, dict):
            if val.get("relationshipHeader"):
                r = _unwrap_rel_item(val, key)
                if r:
                    result.append(r)
            continue
        if not isinstance(val, list):
            continue
        for item in val:
            if not isinstance(item, dict):
                continue
            r = _unwrap_rel_item(item, key)
            if r:
                result.append(r)
    return result


def _serialize(el, include_relationships: bool = False):
    """Common serialisation for any asset/element."""
    hdr   = _header(el)
    props = _props(el)
    # Fallback: some element shapes return guid/properties at the top level
    guid = hdr.get("guid") or el.get("guid", "")
    if not props:
        props = el  # treat top-level keys as properties when no nested 'properties' dict
    super_types = (hdr.get("type") or {}).get("superTypeNames") or []
    out = {
        "guid":                       guid,
        "typeName":                   _type_name(el),
        "superTypeNames":             super_types,
        "displayName":                props.get("displayName") or props.get("name") or "",
        "qualifiedName":              props.get("qualifiedName") or "",
        "description":                props.get("description") or "",
        "deployedImplementationType": props.get("deployedImplementationType") or "",
        "deploymentStatus":           props.get("deploymentStatus") or "",
        "activityStatus":             props.get("activityStatus") or "",
        "networkAddress":             props.get("networkAddress") or "",
        "classifications":            _extract_classifications(hdr),
        "_header":                    _header_summary(el),
        **_authored_fields(el),
    }
    if include_relationships:
        out["relationships"] = _extract_relationships(el)
    # Signal sub-panes available in the detail view
    out["hasSchema"]  = isinstance(el.get("schemaType"), dict) and "relatedElement" in el.get("schemaType", {})
    # TC-9: lineage only applies to Asset subtypes. Endpoint and SoftwareCapability
    # are Referenceable (not Asset) and have no lineage graph, so suppress the pane.
    out["hasLineage"] = "Asset" in super_types
    # SurveyReports have annotations reachable via the survey-reports/{guid}/annotations endpoint.
    out["hasAnnotations"] = (out["typeName"] == "SurveyReport" or "SurveyReport" in super_types)
    # Pass through ANY non-empty mermaid graph field (generic — from the element or
    # its properties), so all available diagrams surface, consistent with Explorer.
    for src in (el, props):
        for k, v in src.items():
            if k not in out and isinstance(v, str) and v.strip() \
                    and not v.lower().startswith("no ") and _is_mermaid_key(k):
                out[k] = v
    # Pass through every remaining scalar property so the detail shows the full
    # property set, not a fixed subset. Skip header/mermaid keys already handled.
    for k, v in props.items():
        if k in out or k in {"displayName", "name", "qualifiedName", "description", "class"} or _is_mermaid_key(k):
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            out[k] = v
        elif isinstance(v, str) and v.strip():
            out[k] = v
    return out


def _safe_list(raw):
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "items" in raw:
        return raw["items"]
    return []


def _serialize_annotation(ann: dict) -> dict:
    """Serialise a single Annotation element (any subtype) into a UI-friendly dict."""
    hdr = _header(ann)
    props = _props(ann)
    guid = hdr.get("guid") or ann.get("guid", "")
    type_info = hdr.get("type") or {}
    type_name = type_info.get("typeName", "")
    super_types = type_info.get("superTypeNames") or []
    versions = hdr.get("versions") or {}
    out = {
        "guid":           guid,
        "typeName":       type_name,
        "superTypeNames": super_types,
        "qualifiedName":  props.get("qualifiedName") or "",
        "annotationType": props.get("annotationType") or type_name,
        "summary":        props.get("summary") or "",
        "analysisStep":   props.get("analysisStep") or "",
        "confidence":     props.get("confidence"),
        "explanation":    props.get("explanation") or "",
        "expression":     props.get("expression") or "",
        "createTime":     versions.get("createTime") or "",
    }
    # Pass through remaining scalar properties
    skip = set(out.keys()) | {"class", "typeName"}
    for k, v in props.items():
        if k in skip or _is_mermaid_key(k):
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            out[k] = v
        elif isinstance(v, str) and v.strip():
            out[k] = v
        elif isinstance(v, dict) and v:
            # Flatten simple nested dicts (e.g. resourceProperties)
            for nk, nv in v.items():
                if isinstance(nv, str) and nv.strip():
                    out[f"{k}.{nk}"] = nv
    # Extract link to parent SurveyReport (present when graph_query_depth >= 1)
    from_report = ann.get("fromSurveyReport")
    if isinstance(from_report, dict):
        rel_elem = from_report.get("relatedElement") or {}
        rel_hdr = rel_elem.get("elementHeader") or {}
        rel_props = rel_elem.get("properties") or {}
        survey_guid = rel_hdr.get("guid", "")
        if survey_guid:
            out["surveyReportGuid"] = survey_guid
            out["surveyReportDisplayName"] = rel_props.get("displayName") or ""
    return out


def _asset_catalog(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import AssetCatalog
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    ac = AssetCatalog(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(ac, token)
    return ac


def _automated_curation(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import AutomatedCuration
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    ac = AutomatedCuration(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(ac, token)
    return ac


def _discovery_client(url, server, user_id, user_pwd, token: Optional[str] = None):
    from pyegeria import DataDiscovery
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    dd = DataDiscovery(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    _apply_token(dd, token)
    return dd


# ── Token exchange endpoint ───────────────────────────────────────────────────

@router.post("/api/egeria-token", summary="Exchange Egeria credentials for a bearer token")
async def get_egeria_bearer_token(request: Request):
    """Called once at login. Returns a short-lived Egeria bearer token so that
    subsequent catalog API calls can pass X-Egeria-Token instead of user_pwd."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    user_id  = body.get("user_id")  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = body.get("password") or os.environ.get("EGERIA_USER_PASSWORD",  "secret")
    url      = body.get("url")      or os.environ.get("EGERIA_PLATFORM_URL",   "https://localhost:9443")
    server   = body.get("server")   or os.environ.get("EGERIA_VIEW_SERVER",    "qs-view-server")
    try:
        from pyegeria import AssetMaker
        mgr = AssetMaker(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        token = await mgr._async_create_egeria_bearer_token()
        return JSONResponse({"token": token, "user_id": user_id})
    except Exception as exc:
        logger.exception("get_egeria_bearer_token failed")
        raise HTTPException(status_code=500, detail=str(exc))


# Relationship types that represent schema *containment* (parent contains
# child schema element) — walked recursively to build the attribute tree.
# Deliberately does NOT include "Schema" (asset -> schemaType; that direction
# is already resolved via el["schemaType"] itself, not walked from here).
_SCHEMA_CONTAINMENT_RELS = {
    "RelationalDBSchema", "AttributeForSchema", "NestedSchemaAttribute",
    "SchemaAttributeType", "MapFromElementType", "MapToElementType",
}


def _to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _node_from_related_element(re_: dict) -> dict:
    hdr = re_.get("elementHeader") or {}
    flat = _flat_props(re_.get("properties") or {})
    return {
        "guid":        hdr.get("guid", ""),
        "typeName":    (hdr.get("type") or {}).get("typeName", ""),
        "displayName": flat.get("displayName") or flat.get("qualifiedName", ""),
        "description": flat.get("description", ""),
        "dataType":    flat.get("dataType", ""),
        "required":    flat.get("isNullable") in ("False", False),
        "extraProps":  {k: v for k, v in flat.items()
                        if k not in ("displayName", "qualifiedName", "description", "dataType", "isNullable")},
        "children":    [],
    }


def _node_from_metadata_expert_element(el: dict) -> dict:
    """Same shape as _node_from_related_element, but for the raw MetadataExpert
    shape (elementGUID/elementProperties.propertyValueMap) returned by the
    supplementary per-guid lookup — a different shape from AssetCatalog's."""
    flat = _flat_props(el.get("elementProperties") or {})
    type_info = (el.get("type") or {})
    return {
        "guid":        el.get("elementGUID", ""),
        "typeName":    type_info.get("typeName", ""),
        "displayName": flat.get("displayName") or flat.get("qualifiedName", ""),
        "description": flat.get("description", ""),
        "dataType":    flat.get("dataType", ""),
        "required":    flat.get("isNullable") in ("False", False),
        "extraProps":  {k: v for k, v in flat.items()
                        if k not in ("displayName", "qualifiedName", "description", "dataType", "isNullable")},
        "children":    [],
    }


def _serialize_schema(el: dict, mgr=None) -> dict:
    """Build the nested schemaType -> attribute -> nested-attribute tree.

    AssetCatalog.get_asset_graph_by_guid's response flattens the ENTIRE
    reachable subgraph into one top-level `relationships` list with no
    indication of which element each relationship attaches from, or which
    end is the container vs the member — both pieces the generic
    relationship extraction used for the "Relationships" section
    (_extract_relationships/_unwrap_rel_item) discards, and both required to
    reassemble a real tree:

    - `startingElementGUID` says which element pyegeria's traversal was
      visiting when it recorded the relationship (NOT reliably "the parent" —
      confirmed live it can be either end).
    - `relatedElementAtEnd1` resolves it: confirmed empirically against
      RETAILSCHEMA's real 3-level hierarchy (DeployedDatabaseSchema
      -[Schema]-> RelationalDBSchemaTypeList -[RelationalDBSchema]->
      RelationalDBSchemaType -[AttributeForSchema]-> RelationalTable
      -[NestedSchemaAttribute]-> RelationalColumn) that the parent is
      `relatedElement` when atEnd1 is True, and `startingElementGUID` when
      atEnd1 is False.

    A further gap: some nodes (e.g. the intermediate RelationalDBSchemaType,
    and columns reached via the atEnd1=True direction) only ever appear as a
    bare `startingElementGUID` in this response — never as a fully-described
    `relatedElement` anywhere in it, so their own displayName/typeName is
    simply not present. Confirmed live these are real schema elements, not
    noise, via a supplementary MetadataExpert.get_metadata_element_by_guid
    lookup (depth 0, cheap) for each one — done here when `mgr` is supplied.
    """
    if not el:
        return {"schemaType": None, "attributes": []}
    st = el.get("schemaType")
    if not isinstance(st, dict):
        return {"schemaType": None, "attributes": []}
    st_elem = st.get("relatedElement") or {}
    st_hdr = st_elem.get("elementHeader") or {}
    st_props = _flat_props(st_elem.get("properties") or {})
    schema_type_guid = st_hdr.get("guid", "")
    schema_type = {
        "guid":        schema_type_guid,
        "typeName":    (st_hdr.get("type") or {}).get("typeName", ""),
        "displayName": st_props.get("displayName") or st_props.get("qualifiedName", ""),
        "description": st_props.get("description", ""),
    }
    if not schema_type_guid:
        return {"schemaType": schema_type, "attributes": []}

    # parent_guid -> list of (child_guid, node-if-known-or-None, position)
    edges: dict = {}
    known_nodes: dict = {}  # guid -> node dict, for children we DO have full data for

    for r in (el.get("relationships") or []):
        if not isinstance(r, dict):
            continue
        rtype = ((r.get("relationshipHeader") or {}).get("type") or {}).get("typeName")
        if rtype not in _SCHEMA_CONTAINMENT_RELS:
            continue
        start = r.get("startingElementGUID")
        re_ = r.get("relatedElement") or {}
        related_guid = (re_.get("elementHeader") or {}).get("guid", "")
        if not start or not related_guid:
            continue
        at_end1 = r.get("relatedElementAtEnd1")
        rel_props = _flat_props(r.get("relationshipProperties") or {})
        position = _to_int(rel_props.get("position"))
        if at_end1:
            parent_guid, child_guid = related_guid, start
        else:
            parent_guid, child_guid = start, related_guid
        edges.setdefault(parent_guid, []).append((child_guid, position))
        # We only have full node data for `related_guid` (the relatedElement
        # side) — if that's the child, keep it; if it's the parent, we
        # already have that from schemaType or an earlier level's own
        # known_nodes entry.
        if child_guid == related_guid:
            known_nodes[child_guid] = _node_from_related_element(re_)

    # Resolve any child guid we don't have full data for via a supplementary
    # by-guid lookup (cheap, depth 0) — see docstring above.
    if mgr is not None:
        missing = set()
        for children in edges.values():
            for child_guid, _pos in children:
                if child_guid not in known_nodes:
                    missing.add(child_guid)
        if missing:
            try:
                me = _metadata_expert_from_asset_maker(mgr)
                for guid in missing:
                    try:
                        raw_el = me.get_metadata_element_by_guid(guid, graph_query_depth=0, output_format="JSON")
                        if isinstance(raw_el, dict):
                            known_nodes[guid] = _node_from_metadata_expert_element(raw_el)
                    except Exception:
                        logger.debug("schema tree: could not resolve node %s", guid)
            except Exception:
                logger.debug("schema tree: could not create MetadataExpert for supplementary lookups")

    def _children_of(guid: str, visited: set) -> list:
        nodes = []
        for child_guid, position in edges.get(guid, []):
            if not child_guid or child_guid in visited:
                continue
            node = known_nodes.get(child_guid)
            if not node:
                continue  # genuinely unresolvable (lookup failed) — skip rather than show a blank row
            node = dict(node)
            node["position"] = position
            visited.add(child_guid)
            node["children"] = _children_of(child_guid, visited)
            nodes.append(node)
        nodes.sort(key=lambda n: (n.get("position") is None, n.get("position") or 0))
        return nodes

    attributes = _children_of(schema_type_guid, {schema_type_guid})
    return {"schemaType": schema_type, "attributes": attributes}


def _serialize_lineage(lin: dict) -> dict:
    """Flatten an AssetCatalog lineage graph response into a UI-friendly list."""
    if not lin:
        return {"relationships": []}
    result = []
    for key in ("lineageLinkage", "lineageRelationships"):
        for item in (lin.get(key) or []):
            if not isinstance(item, dict):
                continue
            r = _unwrap_rel_item(item, key)
            if r:
                result.append(r)
    return {"relationships": result}


def _serialize_tech_type(el: dict) -> dict:
    """Serialise a technology type list element (flat ValidMetadataValue dict)."""
    templates = el.get("catalogTemplates") or []
    return {
        "guid":                        el.get("technologyTypeGUID") or el.get("guid") or "",
        "qualifiedName":               el.get("qualifiedName") or "",
        "displayName":                 el.get("displayName") or el.get("name") or "",
        "deployedImplementationType":  el.get("deployedImplementationType") or el.get("displayName") or el.get("name") or "",
        "description":                 el.get("description") or "",
        "category":                    el.get("category") or "",
        "templateCount":               len(templates) if isinstance(templates, list) else 0,
        "classifications":             _extract_classifications(_header(el)),
    }


def _normalize_placeholder(ph: dict) -> dict:
    """Normalise a placeholder property dict — handles both naming conventions."""
    return {
        "name":        ph.get("placeholderPropertyName") or ph.get("name") or "",
        "dataType":    ph.get("placeholderPropertyDataType") or ph.get("dataType") or "string",
        "required":    ph.get("required") is True or ph.get("required") == "true",
        "example":     ph.get("example") or ph.get("exampleValue") or "",
        "description": ph.get("description") or "",
    }


def _normalize_request_param(p: dict) -> dict:
    return {
        "name":        p.get("name") or p.get("parameterName") or "",
        "dataType":    p.get("dataType") or "string",
        "required":    p.get("required") is True or p.get("required") == "true",
        "description": p.get("description") or "",
        "example":     p.get("example") or "",
    }


def _normalize_produced_annotation(a: dict) -> dict:
    other = {}
    raw_other = a.get("otherPropertyValues") or {}
    if isinstance(raw_other, dict):
        other = {k: v for k, v in raw_other.items() if v not in (None, "", [], {})}
    return {
        "name":               a.get("name") or "",
        "description":        a.get("description") or "",
        "analysisStepName":   a.get("analysisStepName") or "",
        "openMetadataTypeName": a.get("openMetadataTypeName") or "",
        "explanation":        a.get("explanation") or "",
        "otherPropertyValues": other,
    }


def _normalize_analysis_step(s: dict) -> dict:
    return {
        "name":        s.get("name") or "",
        "description": s.get("description") or "",
    }


def _normalize_action_target(t: dict) -> dict:
    return {
        "name":        t.get("name") or "",
        "description": t.get("description") or "",
        "required":    t.get("required") is True or t.get("required") == "true",
        "typeName":    t.get("technicalName") or t.get("openMetadataTypeName") or t.get("typeName") or "",
    }


def _normalize_guard(g: dict) -> dict:
    return {
        "guard":           g.get("guard") or "",
        "description":     g.get("description") or "",
        "completionStatus": g.get("completionStatus") or "",
    }


def _extract_survey_spec(spec: dict) -> dict:
    """Extract the survey specification fields from a governanceActionProcesses or resourceList entry."""
    raw_params     = spec.get("supportedRequestParameter") or []
    raw_steps      = spec.get("supportedAnalysisStep") or []
    raw_produced   = spec.get("producedAnnotationType") or []
    raw_guards     = spec.get("producedGuard") or []
    raw_sup_tgts   = spec.get("supportedActionTarget") or []
    raw_prod_tgts  = spec.get("producedActionTarget") or []
    params   = sorted(
        [_normalize_request_param(p) for p in raw_params if isinstance(p, dict)],
        key=lambda p: (not p["required"], p["name"].lower()),
    )
    return {
        "parameters":            params,
        "analysisSteps":         [_normalize_analysis_step(s) for s in raw_steps if isinstance(s, dict)],
        "producedAnnotationTypes": [_normalize_produced_annotation(a) for a in raw_produced if isinstance(a, dict)],
        "producedGuards":        [_normalize_guard(g) for g in raw_guards if isinstance(g, dict)],
        "supportedActionTargets": [_normalize_action_target(t) for t in raw_sup_tgts if isinstance(t, dict)],
        "producedActionTargets": [_normalize_action_target(t) for t in raw_prod_tgts if isinstance(t, dict)],
    }


def _serialize_governance_process_list_item(el: dict) -> dict:
    hdr, props = _header(el), _props(el)
    return {
        "guid":          hdr.get("guid", ""),
        "typeName":      _type_name(el),
        "displayName":   props.get("displayName") or props.get("name") or "",
        "qualifiedName": props.get("qualifiedName") or "",
        "description":   props.get("description") or "",
    }


def _serialize_governance_process_detail(raw: dict) -> dict:
    """Serialise a GovernanceOfficer.get_governance_process_graph() response.

    That call returns {governanceActionProcess, firstProcessStep, nextProcessSteps,
    processStepLinks, governanceActionProcessMermaidGraph} — a shape specific to
    process/step structure (0462 Governance Action Processes), not a plain Asset
    element, so it needs its own serializer rather than the generic _serialize().
    """
    gap   = raw.get("governanceActionProcess") or {}
    hdr   = _header(gap)
    props = _props(gap)
    spec  = gap.get("specification") or {}

    steps_by_guid: dict = {}

    def _add_step(step_el: dict, is_first: bool = False):
        s_hdr = _header(step_el)
        s_guid = s_hdr.get("guid", "")
        if not s_guid or s_guid in steps_by_guid:
            return
        s_props = step_el.get("processStepProperties") or _props(step_el)
        steps_by_guid[s_guid] = {
            "guid":          s_guid,
            "typeName":      (s_hdr.get("type") or {}).get("typeName", ""),
            "displayName":   s_props.get("displayName") or s_props.get("name") or "",
            "qualifiedName": s_props.get("qualifiedName") or "",
            "description":   s_props.get("description") or "",
            "isFirst":       is_first,
        }

    first_element = (raw.get("firstProcessStep") or {}).get("element") or {}
    if first_element:
        _add_step(first_element, is_first=True)
    for step_el in _safe_list(raw.get("nextProcessSteps")):
        _add_step(step_el)

    step_links = []
    for link in _safe_list(raw.get("processStepLinks")):
        prev_stub = link.get("previousProcessStep") or {}
        next_stub = link.get("nextProcessStep") or {}
        prev_guid = prev_stub.get("guid", "")
        next_guid = next_stub.get("guid", "")
        step_links.append({
            "fromGuid": prev_guid,
            "fromName": steps_by_guid.get(prev_guid, {}).get("displayName") or prev_stub.get("uniqueName") or "",
            "toGuid":   next_guid,
            "toName":   steps_by_guid.get(next_guid, {}).get("displayName") or next_stub.get("uniqueName") or "",
            "guard":    link.get("guard") or "",
            "mandatoryGuard": bool(link.get("mandatoryGuard")),
        })

    return {
        "guid":          hdr.get("guid", ""),
        "typeName":      (hdr.get("type") or {}).get("typeName", ""),
        "displayName":   props.get("displayName") or props.get("name") or "",
        "qualifiedName": props.get("qualifiedName") or "",
        "description":   props.get("description") or "",
        "governanceActionProcessMermaidGraph": raw.get("governanceActionProcessMermaidGraph") or "",
        "steps":          list(steps_by_guid.values()),
        "stepLinks":      step_links,
        "specification":  _extract_survey_spec(spec) if spec else None,
    }


def _serialize_tech_type_detail(el: dict) -> dict:
    """Serialise a technology type detail element for the UI."""
    base = _serialize_tech_type(el)

    # Mermaid graphs
    for field in ("mermaidGraph", "specificationMermaidGraph"):
        val = el.get(field)
        if val and isinstance(val, str) and not val.lower().startswith("no "):
            base[field] = val

    # --- Catalog Templates ---
    raw_templates = el.get("catalogTemplates") or []
    templates = []
    for t in raw_templates:
        if not isinstance(t, dict):
            continue
        rel_el = (t.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        rel_hdr   = rel_el.get("elementHeader") or {}
        spec = t.get("specification") or {}
        raw_placeholders = spec.get("placeholderProperty") or []
        placeholders = [_normalize_placeholder(p) for p in raw_placeholders if isinstance(p, dict)]
        # Sort: required first
        placeholders.sort(key=lambda p: (not p["required"], p["name"].lower()))
        templates.append({
            "displayName": t.get("displayName") or rel_props.get("displayName") or "",
            "description": t.get("description") or rel_props.get("description") or "",
            "guid":        (rel_hdr.get("guid") or rel_el.get("guid") or
                            t.get("guid") or ""),
            "resourceUse": t.get("resourceUse") or "",
            "placeholders": placeholders,
        })
    base["catalogTemplates"] = templates

    # --- Governance Processes ---
    raw_processes = el.get("governanceActionProcesses") or []
    processes = []
    for gp in raw_processes:
        if not isinstance(gp, dict):
            continue
        rel_el    = (gp.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        rel_hdr   = rel_el.get("elementHeader") or {}
        spec = gp.get("specification") or {}
        survey_spec = _extract_survey_spec(spec)
        entry = {
            # rel_props.displayName is the actual process name; gp.displayName is the resourceUse label
            "displayName": rel_props.get("displayName") or gp.get("displayName") or "",
            "description": gp.get("description") or rel_props.get("description") or "",
            "guid":        rel_hdr.get("guid") or rel_el.get("guid") or gp.get("guid") or "",
            "resourceUse": gp.get("resourceUse") or "",
            "typeName":    (rel_hdr.get("type") or {}).get("typeName") or "",
        }
        entry.update(survey_spec)
        processes.append(entry)
    base["governanceActionProcesses"] = processes

    # --- Resource List (GovernanceActionTypes) ---
    raw_resources = el.get("resourceList") or []
    resource_list = []
    for r in raw_resources:
        if not isinstance(r, dict):
            continue
        rel_el    = (r.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        rel_hdr   = rel_el.get("elementHeader") or {}
        spec = r.get("specification") or {}
        survey_spec = _extract_survey_spec(spec)
        entry = {
            "displayName": rel_props.get("displayName") or r.get("displayName") or "",
            "qualifiedName": rel_props.get("qualifiedName") or "",
            "description": r.get("description") or rel_props.get("description") or "",
            "guid":        rel_hdr.get("guid") or rel_el.get("guid") or "",
            "resourceUse": r.get("resourceUse") or "",
            "typeName":    (rel_hdr.get("type") or {}).get("typeName") or "",
        }
        entry.update(survey_spec)
        resource_list.append(entry)
    base["resourceList"] = resource_list

    # --- External References ---
    raw_refs = el.get("externalReferences") or []
    ext_refs = []
    for ref in raw_refs:
        if not isinstance(ref, dict):
            continue
        rel_el    = (ref.get("relatedElement") or {})
        rel_props = rel_el.get("properties") or {}
        ext_refs.append({
            "displayName": ref.get("displayName") or rel_props.get("displayName") or "",
            "description": ref.get("description") or rel_props.get("description") or "",
            "url":         ref.get("url") or rel_props.get("url") or "",
        })
    base["externalReferences"] = ext_refs

    return base


# ── Debug / diagnostic endpoints ─────────────────────────────────────────────

@router.get("/api/debug/raw/{guid}")
def debug_raw_element(
    request: Request,
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return raw pyegeria element response for a GUID — for classification structure diagnosis.

    Shows:
    - raw: the full element dict as returned by pyegeria
    - header_keys: top-level keys in elementHeader
    - raw_classifications: the raw classifications array from elementHeader
    - extracted: what _extract_classifications() produced
    """
    import json as _json
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    el = None
    fetch_method = "unknown"
    # Try asset-graph fetch first
    try:
        raw = mgr.get_asset_by_guid(
            guid=guid,
            output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 1},
        )
        el = raw[0] if isinstance(raw, list) else raw
        fetch_method = "get_asset_by_guid(depth=1)"
    except Exception:
        pass

    # Fallback: find in broader search
    if not el:
        try:
            raw = mgr.find_infrastructure(search_string="*", output_format="JSON", graph_query_depth=1)
            el = _find_by_guid(raw, guid)
            fetch_method = "find_infrastructure"
        except Exception:
            pass

    if not el:
        # Try GlossaryManager as fallback
        try:
            from pyegeria import GlossaryManager
            u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
            gm = GlossaryManager(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
            _apply_token(gm, _token_from_request(request))
            raw = gm.get_term_by_guid(guid, output_format="JSON", body={"class": "GetRequestBody", "graphQueryDepth": 1})
            el = raw
            fetch_method = "get_term_by_guid(depth=1)"
        except Exception:
            pass

    if not el:
        raise HTTPException(status_code=404, detail=f"Could not fetch element {guid!r} via any method")

    hdr = _header(el)
    raw_classifs = hdr.get("classifications") or []
    extracted = _extract_classifications(hdr)

    return JSONResponse({
        "fetch_method":        fetch_method,
        "header_keys":         list(hdr.keys()),
        "raw_classifications": raw_classifs,
        "extracted":           extracted,
        "classification_count": len(raw_classifs),
        "element_type":        _type_name(el),
        "element_keys":        list(el.keys()),
    })


# ── SPA route ─────────────────────────────────────────────────────────────────

@router.get("/tech-catalog", include_in_schema=False)
def serve_spa():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="tech-catalog.html not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


# ── Common query params ───────────────────────────────────────────────────────

_CRED_PARAMS = dict(
    url      = Query(None),
    server   = Query(None),
    user_id  = Query(None),
    user_pwd = Query(None),
)


# ── List endpoints ────────────────────────────────────────────────────────────

@router.get("/api/tech-catalog/infrastructure")
def list_infrastructure(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        logger.exception("tech-catalog: AssetMaker connection failed")
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_infrastructure(
            search_string=q or "*",
            metadata_element_type="ITInfrastructure",
            deployment_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_infrastructure failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/software-capabilities")
def list_software_capabilities(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        logger.exception("tech-catalog: AssetMaker connection failed")
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_software_capabilities(
            search_string=q or "*",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_software_capabilities failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/endpoints")
def list_endpoints(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _connection_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_endpoints(
            search_string=q or "*",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
        )
        if not include_templates:
            raw = [e for e in _safe_list(raw) if not _is_template(e)]
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_endpoints failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-stores")
def list_data_stores(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataStore",
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_stores failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-feeds")
def list_data_feeds(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataFeed",
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_feeds failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/data-sets")
def list_data_sets(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="DataSet",
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_data_sets failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/apis")
def list_apis(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_assets(
            search_string=q or "*",
            metadata_element_type="DeployedAPI",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_apis failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/software-components")
def list_software_components(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_processes(
            search_string=q or "*",
            metadata_element_type="DeployedSoftwareComponent",
            activity_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_software_components failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/actions")
def list_actions(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_processes(
            search_string=q or "*",
            metadata_element_type="Action",
            activity_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            graph_query_depth=0,
            as_of_time=as_of_time or None,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_actions failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/governance-processes")
def list_governance_processes(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(200, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """List GovernanceActionProcess definitions (0462 Governance Action Processes)."""
    try:
        mgr = _governance_officer(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_governance_definitions(
            search_string=q or "*",
            metadata_element_type="GovernanceActionProcess",
            output_format="JSON",
            start_from=start_from,
            page_size=page_size,
            graph_query_depth=0,
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            skip_classified_elements=[] if include_templates else ["Template"],
        )
        raw = _safe_list(raw)
        items = [_serialize_governance_process_list_item(e) for e in raw]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("list_governance_processes failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/governance-processes/{guid}")
def get_governance_process_detail(
    request: Request,
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Full step/flow/target detail for one GovernanceActionProcess, via
    GovernanceOfficer.get_governance_process_graph — the 0462 structural API,
    not the generic Asset graph (which has no concept of process steps)."""
    try:
        mgr = _governance_officer(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.get_governance_process_graph(guid, output_format="JSON")
        if not raw or not isinstance(raw, dict) or not raw.get("governanceActionProcess"):
            raise HTTPException(status_code=404, detail=f"Governance action process {guid!r} not found")
        return JSONResponse(_serialize_governance_process_detail(raw))
    except HTTPException:
        raise
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("get_governance_process_detail failed for %s", guid)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/element-nav")
def get_element_nav(
    request: Request,
    guid: str = Query(...),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return typeName and superTypeNames for a GUID so the frontend can route to the correct section."""
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        el = _fetch_detail(mgr, guid, None)
        if not el:
            raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")
        hdr = _header(el)
        type_info = hdr.get("type") or {}
        type_name = type_info.get("typeName") or _type_name(el)
        super_types = type_info.get("superTypeNames") or []
        props = _props(el) or {}
        display_name = props.get("displayName") or props.get("name") or guid
        return JSONResponse({
            "guid": guid,
            "typeName": type_name,
            "superTypeNames": super_types,
            "displayName": display_name,
        })
    except HTTPException:
        raise
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("get_element_nav failed for %s", guid)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/assets/{guid}")
def get_asset_detail(
    request: Request,
    guid: str,
    # section tells us which find_* to use for non-Asset types
    section: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None, description="ISO 8601; null/absent = now"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        el = _fetch_detail(mgr, guid, section, as_of_time)
        if not el:
            raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")
        return JSONResponse(_serialize(el, include_relationships=True))
    except HTTPException:
        raise
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail=f"Token expired or user not authorized for element {guid!r}")
        logger.exception("get_asset_detail failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/assets/{guid}/schema")
def get_asset_schema(
    request: Request,
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the schema type + nested attribute tree for any asset with a Schema relationship.

    Uses AssetCatalog.get_asset_graph_by_guid (same call _fetch_detail() uses
    for the main asset detail view), NOT AssetMaker.get_asset_by_guid --
    confirmed live that the latter never nests attribute relationships under
    el["schemaType"]["relatedElement"] at any graph depth, which is why this
    section always came back empty. get_asset_graph_by_guid's response
    carries a separate top-level `relationships` list covering the whole
    reachable subgraph, where each entry's `startingElementGUID` says which
    element it actually attaches from -- the piece _serialize_schema() needs
    to walk it into a real tree instead of the schema data being buried
    (unlabeled) in the generic flattened "Relationships" section.
    """
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
        ac = _asset_catalog_from_asset_maker(mgr)
        raw = ac.get_asset_graph_by_guid(
            guid,
            output_format="JSON",
            body={"class": "ResultsRequestBody", "graphQueryDepth": 5},
        )
        el = raw[0] if isinstance(raw, list) else raw
        return JSONResponse(_serialize_schema(el or {}, mgr=mgr))
    except Exception as exc:
        logger.exception("get_asset_schema failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/assets/{guid}/lineage")
def get_asset_lineage(
    request: Request,
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the mermaid lineage graph string for any asset via AssetCatalog.

    Returns {"mermaidGraph": ""} when the asset has no lineage data (Egeria returns 400).
    """
    try:
        ac = _asset_catalog(url, server, user_id, user_pwd, token=_token_from_request(request))
        mermaid_str = ac.get_asset_lineage_graph_by_guid(guid, output_format="MERMAID")
        if isinstance(mermaid_str, str):
            return JSONResponse({"mermaidGraph": mermaid_str or ""})
        # Some pyegeria versions return a dict; extract mermaidGraph field if present
        if isinstance(mermaid_str, dict):
            return JSONResponse({"mermaidGraph": mermaid_str.get("mermaidGraph") or ""})
        return JSONResponse({"mermaidGraph": ""})
    except Exception as exc:
        exc_str = str(exc)
        # 400 = no lineage data; 404 = element not an Asset (e.g. Endpoint); treat both as empty
        if any(code in exc_str for code in ("400", "404", "CLIENT_ERROR_400", "CLIENT_ERROR_404")):
            return JSONResponse({"mermaidGraph": ""})
        logger.exception("get_asset_lineage failed for %s", guid)
        raise HTTPException(status_code=500, detail=exc_str)


# ── TC-13: file Data Asset preview ────────────────────────────────────────────
# Backing files live under /deployments/* (mounted read-only into this container
# to mirror the Egeria platform's view), so an asset's pathName resolves directly.
# Only paths under these roots are previewable — realpath() defeats traversal.
_PREVIEW_ROOTS = (
    "/deployments/loading-bay",
    "/deployments/landing-area",
    "/deployments/coco-data-lake",
    "/deployments/distribution-hub",
    "/deployments/treasury-dts-history",
    "/deployments/work",
)
_PREVIEW_MAX_BYTES = 50 * 1024 * 1024  # skip files larger than 50 MB


def _resolve_preview_path(raw_path: str) -> Optional[str]:
    """Return a safe absolute path under an allowed root, or None if disallowed."""
    if not raw_path:
        return None
    p = raw_path
    if p.startswith("file://"):
        p = p[len("file://"):]
        # strip a leading host component (file://host/abs/path)
        if p and not p.startswith("/") and "/" in p:
            p = "/" + p.split("/", 1)[1]
    try:
        real = os.path.realpath(p)
    except Exception:
        return None
    for root in _PREVIEW_ROOTS:
        root_real = os.path.realpath(root)
        if real == root_real or real.startswith(root_real + os.sep):
            return real
    return None


@router.get("/api/tech-catalog/assets/{guid}/preview",
            summary="Preview a bounded page of rows from a file Data Asset (CSV/TSV/JSON)")
def get_asset_preview(
    request: Request,
    guid: str,
    start_from_row: int = Query(0,   ge=0),
    max_row_count:  int = Query(100, ge=1, le=2000),
    section: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Read a bounded page of rows from a file asset's backing store, normalised to
    {columns, rows, has_more} for the tabular preview modal. The file must be under
    an allowed /deployments root and reachable from this container ('when accessible')."""
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
        el = _fetch_detail(mgr, guid, section)
        if not el:
            raise HTTPException(status_code=404, detail=f"Element {guid!r} not found")
        d = _serialize(el)
    except HTTPException:
        raise
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or not authorized")
        logger.exception("get_asset_preview: detail fetch failed")
        raise HTTPException(status_code=500, detail=str(exc))

    raw_path = d.get("pathName") or d.get("resourceName") or d.get("networkAddress") or ""
    ext = (d.get("fileExtension") or os.path.splitext(raw_path)[1].lstrip(".")).lower()
    path = _resolve_preview_path(raw_path)

    if not path:
        raise HTTPException(status_code=422,
            detail=f"This asset's file isn't previewable from here (path: {raw_path or 'unknown'}).")
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="The backing file isn't accessible from the server.")
    try:
        if os.path.getsize(path) > _PREVIEW_MAX_BYTES:
            raise HTTPException(status_code=413, detail="File is too large to preview.")
    except OSError:
        pass

    try:
        import pandas as pd
        if ext in ("csv", "tsv", "txt"):
            sep = "\t" if ext == "tsv" else ","
            df = pd.read_csv(path, sep=sep,
                             skiprows=range(1, start_from_row + 1) if start_from_row else None,
                             nrows=max_row_count + 1)
        elif ext in ("json", "jsonl", "ndjson"):
            df = pd.read_json(path, lines=ext in ("jsonl", "ndjson"))
            df = df.iloc[start_from_row:start_from_row + max_row_count + 1]
        else:
            raise HTTPException(status_code=415, detail=f"Preview not supported for .{ext or '?'} files.")
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_asset_preview: read failed for %s", path)
        raise HTTPException(status_code=500, detail=f"Could not read file: {exc}")

    has_more = len(df) > max_row_count
    df = df.iloc[:max_row_count]
    columns = [str(c) for c in df.columns]
    safe = df.astype(object).where(pd.notnull(df), None)
    rows = safe.values.tolist()
    return JSONResponse({"columns": columns, "rows": rows, "has_more": bool(has_more),
                         "start_from_row": start_from_row, "row_count": len(rows),
                         "fileName": d.get("fileName") or os.path.basename(path)})


# ── Survey Reports & Annotations routes ──────────────────────────────────────

@router.get("/api/tech-catalog/survey-reports")
def list_survey_reports(
    request: Request,
    q:          str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    as_of_time: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """List SurveyReport elements. SurveyReports are DataAsset subtypes but use an
    empty content_status_list because they are not given ACTIVE status by Egeria."""
    try:
        mgr = _asset_maker(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        raw = mgr.find_data_assets(
            search_string=q or "*",
            metadata_element_type="SurveyReport",
            content_status_list=[],
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            graph_query_depth=0,
            sequencing_order=_SEQ_ORDER,
            sequencing_property=_SEQ_PROP,
            as_of_time=as_of_time or None,
        )
        if not include_templates:
            raw = [e for e in _safe_list(raw) if not _is_template(e)]
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("list_survey_reports failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/survey-reports/{guid}/annotations")
def get_survey_annotations(
    request: Request,
    guid: str,
    annotation_type: Optional[str] = Query(None, description="Filter by annotation subtype name"),
    page_size: int = Query(500, ge=1, le=1000),
    as_of_time: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return all Annotation elements for a specific SurveyReport GUID.

    Fetches annotations with graph_query_depth=1 (to get fromSurveyReport link)
    then filters to those belonging to the requested report.
    """
    try:
        dd = _discovery_client(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        kwargs = {}
        if annotation_type:
            kwargs["metadata_element_type"] = annotation_type
        if as_of_time:
            kwargs["as_of_time"] = as_of_time
        raw = dd.find_annotations(
            search_string="*",
            page_size=page_size,
            output_format="JSON",
            graph_query_depth=1,
            **kwargs,
        )
        items = []
        for ann in _safe_list(raw):
            from_report = ann.get("fromSurveyReport") or {}
            rel_elem = from_report.get("relatedElement") or {}
            rel_hdr = rel_elem.get("elementHeader") or {}
            if rel_hdr.get("guid") == guid:
                items.append(_serialize_annotation(ann))
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("get_survey_annotations failed for %s", guid)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/annotations")
def list_annotations(
    request: Request,
    q:               str = Query("*"),
    annotation_type: Optional[str] = Query(None, description="Filter by annotation subtype name"),
    start_from:      int = Query(0, ge=0),
    page_size:       int = Query(100, ge=1, le=500),
    as_of_time:      Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """List or search Annotation elements across all survey reports."""
    try:
        dd = _discovery_client(url, server, user_id, user_pwd, token=_token_from_request(request))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    try:
        kwargs = {}
        if annotation_type:
            kwargs["metadata_element_type"] = annotation_type
        if as_of_time:
            kwargs["as_of_time"] = as_of_time
        raw = dd.find_annotations(
            search_string=q or "*",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
            graph_query_depth=1,
            **kwargs,
        )
        items = [_serialize_annotation(ann) for ann in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Token expired or unauthorized")
        logger.exception("list_annotations failed")
        raise HTTPException(status_code=500, detail=str(exc))


# ── Technology Types routes ───────────────────────────────────────────────────
# IMPORTANT: register hierarchy and elements routes BEFORE the parametric
# {qualified_name} route to avoid "hierarchy" or "{qn}/elements" being captured
# as a qualifiedName value.

@router.get("/api/tech-catalog/tech-types/hierarchy")
def get_tech_type_hierarchy(
    request: Request,
    root: str = Query("Root Technology Type"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return the technology type hierarchy tree starting from root."""
    try:
        ac = _automated_curation(url, server, user_id, user_pwd, token=_token_from_request(request))
        raw = ac.get_tech_type_hierarchy(filter_string=root or "Root Technology Type",
                                         output_format="JSON")
        return JSONResponse({"hierarchy": raw})
    except Exception as exc:
        logger.exception("get_tech_type_hierarchy failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/tech-types")
def list_tech_types(
    request: Request,
    q: str = Query("*"),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    """List or search technology types."""
    try:
        ac = _automated_curation(url, server, user_id, user_pwd, token=_token_from_request(request))
        raw = ac.find_technology_types(
            search_string=q or "*",
            start_from=start_from,
            page_size=page_size,
            output_format="JSON",
        )
        # Deduplicate by qualifiedName (some content packs register the same type twice).
        # Keep the entry with more catalogTemplates when there's a conflict.
        if not include_templates:
            raw = [e for e in _safe_list(raw) if not _is_template(e)]
        seen: dict = {}
        for e in _safe_list(raw):
            item = _serialize_tech_type(e)
            qn = item.get("qualifiedName", "")
            if qn not in seen or item.get("templateCount", 0) > seen[qn].get("templateCount", 0):
                seen[qn] = item
        items = sorted(seen.values(), key=lambda x: x.get("displayName", "").lower())
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        logger.exception("list_tech_types failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/tech-catalog/tech-types/{qualified_name:path}/elements")
def get_tech_type_elements(
    request: Request,
    qualified_name: str,
    display_name: str = Query(""),
    start_from: int = Query(0, ge=0),
    page_size:  int = Query(100, ge=1, le=500),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return catalog instances of the given technology type.

    get_technology_type_elements requires the displayName (exact match, no wildcards).
    Pass it via the ?display_name= query param, populated from the already-loaded detail.
    Falls back to qualifiedName if display_name is absent.
    """
    try:
        ac = _automated_curation(url, server, user_id, user_pwd, token=_token_from_request(request))
        filter_str = display_name or (qualified_name.split(":")[-1] if ":" in qualified_name else qualified_name)
        raw = ac.get_technology_type_elements(
            filter_string=filter_str,
            start_from=start_from,
            page_size=page_size,
            get_templates=True,
            output_format="JSON",
        )
        items = [_serialize(e) for e in _safe_list(raw)]
        return JSONResponse({"items": items, "total": len(items)})
    except Exception as exc:
        exc_str = str(exc)
        # Egeria returns 400/404 when no elements match — treat as empty list
        if any(code in exc_str for code in ("400", "404", "CLIENT_ERROR_400", "CLIENT_ERROR_404", "No elements")):
            return JSONResponse({"items": [], "total": 0})
        logger.exception("get_tech_type_elements failed")
        raise HTTPException(status_code=500, detail=exc_str)


@router.get("/api/tech-catalog/tech-types/{qualified_name:path}")
def get_tech_type_detail(
    request: Request,
    qualified_name: str,
    deployed_implementation_type: Optional[str] = Query(None),
    display_name: Optional[str] = Query(None),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return full detail for a technology type.

    get_tech_type_detail matches by deployedImplementationType (the preferred lookup
    field).  Falls back to display_name or qualified_name if not supplied.
    """
    filter_str = deployed_implementation_type or display_name or qualified_name
    try:
        ac = _automated_curation(url, server, user_id, user_pwd, token=_token_from_request(request))
        raw = ac.get_tech_type_detail(filter_string=filter_str, output_format="JSON")
        el = raw[0] if isinstance(raw, list) else raw
        if not isinstance(el, dict):
            raise HTTPException(status_code=404, detail=f"Technology type {filter_str!r} not found")
        return JSONResponse(_serialize_tech_type_detail(el))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_tech_type_detail failed")
        raise HTTPException(status_code=500, detail=str(exc))


# ── Survey Types aggregation ──────────────────────────────────────────────────

_SURVEY_TYPES_CACHE: dict = {}   # key → {"ts": float, "data": list}
_SURVEY_TYPES_TTL = 300          # 5 minutes


@router.get("/api/tech-catalog/survey-types")
def list_survey_types(
    request: Request,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Return survey type definitions extracted from all TechnologyTypes.

    Each entry represents a GovernanceActionType or GovernanceActionProcess with
    resourceUse == 'Survey Resource', with the full survey specification and the
    list of TechnologyTypes that reference it.
    """
    cache_key = f"{url}|{server}|{user_id}"
    cached = _SURVEY_TYPES_CACHE.get(cache_key)
    if cached and (time.time() - cached["ts"]) < _SURVEY_TYPES_TTL:
        return JSONResponse({"items": cached["data"]})

    token = _token_from_request(request)
    try:
        ac = _automated_curation(url, server, user_id, user_pwd, token=token)
        raw_list = ac.find_technology_types(search_string="*", page_size=500, output_format="JSON")
    except Exception as exc:
        logger.exception("list_survey_types: find_technology_types failed")
        raise HTTPException(status_code=500, detail=str(exc))

    # guid → survey type entry (aggregated across TechTypes)
    by_guid: dict = {}

    for tech_raw in _safe_list(raw_list):
        tech_base = _serialize_tech_type(tech_raw)
        tech_display = tech_base.get("displayName") or tech_base.get("qualifiedName") or ""
        tech_qn = tech_base.get("qualifiedName") or ""

        try:
            detail_raw = ac.get_tech_type_detail(
                filter_string=tech_base.get("deployedImplementationType") or tech_base.get("displayName") or tech_qn,
                output_format="JSON",
            )
            el = detail_raw[0] if isinstance(detail_raw, list) else detail_raw
            if not isinstance(el, dict):
                continue
        except Exception:
            logger.warning("list_survey_types: could not fetch detail for %s", tech_qn)
            continue

        def _process_survey_entry(entry: dict, source: str):
            if not isinstance(entry, dict):
                return
            resource_use = entry.get("resourceUse") or ""
            if "survey" not in resource_use.lower():
                return
            rel_el    = (entry.get("relatedElement") or {})
            rel_props = rel_el.get("properties") or {}
            rel_hdr   = rel_el.get("elementHeader") or {}
            guid = rel_hdr.get("guid") or rel_el.get("guid") or ""
            if not guid:
                return
            spec = entry.get("specification") or {}
            survey_spec = _extract_survey_spec(spec)
            if guid not in by_guid:
                by_guid[guid] = {
                    "guid":          guid,
                    "displayName":   rel_props.get("displayName") or entry.get("displayName") or "",
                    "qualifiedName": rel_props.get("qualifiedName") or "",
                    "description":   entry.get("description") or rel_props.get("description") or "",
                    "typeName":      (rel_hdr.get("type") or {}).get("typeName") or "",
                    "resourceUse":   resource_use,
                    "usedByTechTypes": [],
                    **survey_spec,
                }
            ref = {"displayName": tech_display, "qualifiedName": tech_qn}
            if ref not in by_guid[guid]["usedByTechTypes"]:
                by_guid[guid]["usedByTechTypes"].append(ref)

        for gp in _safe_list(el.get("governanceActionProcesses")):
            _process_survey_entry(gp, "governanceActionProcesses")
        for r in _safe_list(el.get("resourceList")):
            _process_survey_entry(r, "resourceList")

    items = sorted(by_guid.values(), key=lambda x: x.get("displayName", "").lower())
    _SURVEY_TYPES_CACHE[cache_key] = {"ts": time.time(), "data": items}
    return JSONResponse({"items": items})


# Map from section id → targeted find_* with graph_query_depth=5
_SECTION_FINDERS = {
    "software-capabilities": lambda m: m.find_software_capabilities(
        search_string="*", output_format="JSON", graph_query_depth=5),
    "infrastructure": lambda m: m.find_infrastructure(
        search_string="*", output_format="JSON", graph_query_depth=5,
        deployment_status_list=[],
        sequencing_order=_SEQ_ORDER, sequencing_property=_SEQ_PROP),
}


def _fetch_detail(mgr, guid: str, section: Optional[str], as_of_time: Optional[str] = None):
    """
    Fetch a single element with full property/relationship/mermaid detail.
    Endpoints use ConnectionMaker.get_endpoint_by_guid (not an Asset subtype).
    All Asset subtypes use AssetCatalog.get_asset_graph_by_guid for richer mermaid graphs,
    with fallback to get_asset_by_guid for types the graph endpoint can't serve.

    as_of_time (ISO 8601) selects a point-in-time version (LE-3); injected as
    ``asOfTime`` in the request body. If the element did not yet exist at that
    time, Egeria reports "not found" and the caller surfaces a clean 404.
    """
    # Endpoints are Referenceable subtypes, not Assets — use ConnectionMaker directly.
    if section == "endpoints":
        try:
            cm = _connection_maker_from_asset_maker(mgr)
            raw = cm.get_endpoint_by_guid(guid=guid, output_format="JSON", graph_query_depth=5)
            el = raw[0] if isinstance(raw, list) else raw
            if el:
                return el
        except Exception as exc:
            if _is_auth_error(exc):
                raise
            logger.exception("get_endpoint_by_guid failed for %s", guid)
        return None

    # All Asset types: use get_asset_graph_by_guid with graphQueryDepth=5.
    try:
        ac = _asset_catalog_from_asset_maker(mgr)
        graph_body = {"class": "ResultsRequestBody", "graphQueryDepth": 5}
        if as_of_time:
            graph_body["asOfTime"] = as_of_time
        raw = ac.get_asset_graph_by_guid(guid, output_format="JSON", body=graph_body)
        el = raw[0] if isinstance(raw, list) else raw
        if el and isinstance(el, dict):
            return el
    except Exception as exc:
        if _is_auth_error(exc):
            raise
        logger.debug("get_asset_graph_by_guid failed for %s, trying fallbacks: %s", guid, exc)

    # Fallback: targeted finders for non-standard Asset types
    finder = _SECTION_FINDERS.get(section or "")
    if finder:
        try:
            return _find_by_guid(finder(mgr), guid)
        except Exception as exc:
            if _is_auth_error(exc):
                raise

    # Fallback: get_asset_by_guid
    try:
        raw = mgr.get_asset_by_guid(
            guid=guid,
            output_format="JSON",
            body={"class": "GetRequestBody", "graphQueryDepth": 5, "relationshipsPageSize": 50},
        )
        el = raw[0] if isinstance(raw, list) else raw
        if el:
            return el
    except Exception as exc:
        if _is_auth_error(exc):
            raise

    # Last resort: SoftwareCapability finder
    try:
        result = _find_by_guid(
            mgr.find_software_capabilities(search_string="*", output_format="JSON", graph_query_depth=3),
            guid)
        if result:
            return result
    except Exception:
        pass

    # Final fallback: ClassificationExplorer.get_element_by_guid works for any
    # metadata element type, including non-Assets (Referenceable subtypes, etc.)
    try:
        ce = _classification_explorer_from_asset_maker(mgr)
        body = {"class": "GetRequestBody", "graphQueryDepth": 3}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = ce.get_element_by_guid(guid=guid, graph_query_depth=3, output_format="JSON", body=body)
        el = raw[0] if isinstance(raw, list) and raw else (raw if isinstance(raw, dict) else None)
        if el and isinstance(el, dict):
            return el
    except Exception as exc:
        if _is_auth_error(exc):
            raise
        logger.debug("ClassificationExplorer.get_element_by_guid failed for %s: %s", guid, exc)

    return None


def _connection_maker_from_asset_maker(mgr):
    """Create a ConnectionMaker sharing credentials from an existing AssetMaker.

    NOTE: ConnectionMaker.__init__ calls check_connection() immediately, so we
    must call create_egeria_bearer_token() (not set the token directly) to avoid
    a 401 on that handshake.
    """
    from pyegeria import ConnectionMaker
    cm = ConnectionMaker(
        server_name=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    cm.create_egeria_bearer_token()
    return cm


def _asset_catalog_from_asset_maker(mgr):
    """Create an AssetCatalog sharing credentials/token from an existing AssetMaker."""
    from pyegeria import AssetCatalog
    ac = AssetCatalog(
        view_server=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    auth = (getattr(mgr, "headers", None) or {}).get("Authorization", "")
    token = auth[len("Bearer "):] if auth.startswith("Bearer ") else None
    _apply_token(ac, token)
    return ac


def _metadata_expert_from_asset_maker(mgr):
    """Create a MetadataExpert sharing credentials/token from an existing AssetMaker.

    Used by _serialize_schema()'s supplementary per-guid lookups: some schema
    tree nodes (RelationalDBSchemaType, some columns) only ever appear as a
    bare `startingElementGUID` in AssetCatalog.get_asset_graph_by_guid's
    response, never as a fully-described `relatedElement` anywhere in it —
    confirmed live, not a bug in our own parsing, a real gap in that response
    shape. get_metadata_element_by_guid(graph_query_depth=0) is cheap and
    works for any element type.
    """
    from pyegeria import MetadataExpert
    me = MetadataExpert(
        view_server=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    auth = (getattr(mgr, "headers", None) or {}).get("Authorization", "")
    token = auth[len("Bearer "):] if auth.startswith("Bearer ") else None
    _apply_token(me, token)
    return me


def _classification_explorer_from_asset_maker(mgr):
    """Create a ClassificationExplorer sharing credentials/token from an existing AssetMaker.

    ClassificationExplorer.get_element_by_guid works for ANY metadata element type,
    not just Assets — used as the final fallback in _fetch_detail.
    """
    from pyegeria import ClassificationExplorer
    ce = ClassificationExplorer(
        view_server=mgr.server_name,
        platform_url=mgr.platform_url,
        user_id=mgr.user_id,
        user_pwd=mgr.user_pwd,
    )
    auth = (getattr(mgr, "headers", None) or {}).get("Authorization", "")
    token = auth[len("Bearer "):] if auth.startswith("Bearer ") else None
    _apply_token(ce, token)
    return ce


def _find_by_guid(raw, guid: str):
    """Filter a list result from find_* to return the single element matching guid."""
    for el in _safe_list(raw):
        if _header(el).get("guid") == guid:
            return el
    return None
