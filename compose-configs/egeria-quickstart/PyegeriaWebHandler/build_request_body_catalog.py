#!/usr/bin/env python3
"""
Build the Egeria request body catalog (egeria_request_body_catalog.json).

Run this script each time you upgrade the Egeria platform version so the
REST API Explorer picks up any new or changed outer request body types.

Usage:
    python3 build_request_body_catalog.py [/path/to/http-client-collections]

    If the path is omitted the script checks, in order:
      1. HTTP_COLLECTIONS_PATH environment variable
      2. The default distribution path for egeria-platform-6.x

Output is written alongside this script as egeria_request_body_catalog.json.
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Default search locations ───────────────────────────────────────────────────

_DEFAULT_ROOTS = [
    # Typical unpacked distribution location
    Path.home() / "localGit/egeria-v6/egeria/open-metadata-distribution"
      / "omag-server-platform/build/unpacked"
      / "egeria-platform-6.1-SNAPSHOT-distribution.tar.gz"
      / "assembly/opt/http-client-collections",
]

# ── Field documentation ────────────────────────────────────────────────────────

FIELD_NOTES: dict[str, str] = {
    "class":                        "Discriminator — always the body type name (set automatically).",
    "properties":                   "Layer 2 body: the type-specific properties object. Set 'class' to the <Type>Properties name.",
    "mergeUpdate":                  "true = partial update (only supplied fields change); false = replace all properties.",
    "externalSourceGUID":           "GUID of the external metadata source. Leave blank for native Egeria ownership.",
    "externalSourceName":           "Qualified name of the external metadata source. Leave blank for native Egeria ownership.",
    "anchorGUID":                   "GUID of the anchor element that owns this element's lifecycle.",
    "isOwnAnchor":                  "true if this element is its own anchor (top-level elements).",
    "parentGUID":                   "GUID of the parent element to link to on creation.",
    "parentRelationshipTypeName":   "Relationship type name used to link to the parent.",
    "parentAtEnd1":                 "Which end of the parent relationship this element occupies.",
    "parentRelationshipProperties": "Properties to set on the parent relationship.",
    "initialClassifications":       "Map of classification name → classification properties to apply at creation time.",
    "effectiveFrom":                "ISO-8601 datetime from which this element is effective.",
    "effectiveTo":                  "ISO-8601 datetime after which this element is no longer effective.",
    "effectiveTime":                "Point-in-time for the operation (defaults to now if omitted).",
    "forLineage":                   "true = include elements with the Memento classification (archived for lineage).",
    "forDuplicateProcessing":       "true = suppress duplicate-detection during this operation.",
    "cascadeDelete":                "true = also delete all elements anchored to this element.",
    "cascadedDelete":               "Alias for cascadeDelete used in some older endpoints.",
    "deleteMethod":                 "Deletion approach: SOFT or HARD.",
    "archiveDate":                  "Date the element was archived (for soft-delete audit).",
    "archiveProcess":               "Process that triggered the archive.",
    "archiveProperties":            "Additional archival metadata.",
    "searchString":                 "Regular expression or keyword to match against element properties.",
    "startsWith":                   "Anchor the search string to the start of values.",
    "endsWith":                     "Anchor the search string to the end of values.",
    "ignoreCase":                   "Case-insensitive matching when true.",
    "filter":                       "Property filter string (matched against displayName / qualifiedName).",
    "startFrom":                    "Zero-based index for pagination.",
    "pageSize":                     "Maximum number of results per page.",
    "limitResultsByStatus":         "Only return elements with these statuses (e.g. ['ACTIVE']).",
    "sequencingOrder":              "Sort order: PROPERTY_ASCENDING, PROPERTY_DESCENDING, CREATION_DATE_RECENT, etc.",
    "sequencingProperty":           "Property name to sort by (e.g. 'qualifiedName').",
    "metadataElementTypeName":      "Restrict results to elements of this open metadata type.",
    "metadataElementSubtypeNames":  "Also include elements of these subtypes.",
    "graphQueryDepth":              "How many relationship hops to traverse (0 = element only, 1 = include neighbours).",
    "skipRelationships":            "Omit relationship data from the response when true.",
    "includeOnlyRelationships":     "Relationship type names to include (all others are excluded).",
    "skipClassifiedElements":       "Classification names whose elements should be excluded.",
    "includeOnlyClassifiedElements":"Only return elements that carry at least one of these classifications.",
    "relationshipsPageSize":        "Page size for embedded relationship lists.",
    "maxMermaidNodeCount":          "Cap on Mermaid diagram nodes (0 = no limit).",
    "asOfTime":                     "Return the state of the element as it was at this ISO-8601 timestamp.",
    "oldestFirst":                  "Return history in chronological order when true.",
    "searchProperties":             "Structured property conditions (SearchProperties object).",
    "matchClassifications":         "Classification filter conditions to apply alongside property matching.",
    "relationshipTypeName":         "Filter results to relationships of this type.",
    "templateGUID":                 "GUID of the template element to copy.",
    "placeholderPropertyValues":    "Map of placeholder name → value for template substitution.",
    "replacementProperties":        "Properties to override on the copy (typed PropertyValue map).",
    "typeName":                     "Open metadata type name for generic low-level create operations.",
    "openMetadataTypeName":         "Alias for typeName used on some template endpoints.",
    "allowRetrieve":                "Return the existing element instead of failing if it already exists.",
    "anchorScopeGUIDs":             "Restrict anchor search to these scope GUIDs.",
    "makeAnchor":                   "Make the new element the anchor of the relationship.",
    "relationshipProperties":       "Alias for properties used on some relationship endpoints.",
    "replaceProperties":            "true = replace the full property set; false = merge (alias for !mergeUpdate).",
    "mergeClassifications":         "true = keep existing classifications not mentioned in the update.",
    "name":                         "Simple string name (used for lookup-by-name endpoints).",
    "namePropertyName":             "Which property to match the name against (e.g. 'qualifiedName', 'displayName').",
    "string":                       "Arbitrary string value payload.",
    "urlRoot":                      "Platform URL root (used in admin endpoints).",
    "effectiveFrom_top":            "Top-level effectiveFrom for NewExternalIdRequestBody.",
    "effectiveTo_top":              "Top-level effectiveTo for NewExternalIdRequestBody.",
    "activityStatusList":           "List of activity status values to filter or set.",
    "contentStatusList":            "List of content status values to filter.",
    "deploymentStatusList":         "List of deployment status values to filter.",
    "category":                     "Category qualifier (e.g. 'Governance').",
    "actionTargets":                "List of NewActionTarget objects (actionTargetName + actionTargetGUID).",
    "newActionTargets":             "Alias for actionTargets on ActionRequestBody.",
    "actionSponsorGUID":            "GUID of the actor sponsoring the action.",
    "assignToActorGUID":            "GUID of the actor to whom the action is assigned.",
    "originatorGUID":               "GUID of the element that initiated the action.",
    "receivedGuards":               "Guards received from predecessor governance steps.",
    "requestType":                  "Request type label sent to the governance engine.",
    "requestParameters":            "Key-value parameters for the governance engine.",
    "requestSourceGUIDs":           "GUIDs of elements that triggered this request.",
    "requestSourceName":            "Name of the requesting service.",
    "originatorEngineName":         "Name of the originating governance engine.",
    "originatorServiceName":        "Name of the originating service.",
    "processName":                  "Governance action process qualified name.",
    "startDate":                    "Scheduled start date/time for the governance action.",
    "domainIdentifier":             "Governance domain identifier (0 = all domains).",
    "governanceActionTypeQualifiedName": "Qualified name of the GovernanceActionType to initiate.",
    "connectorName":                "Name of the connector instance to reconfigure.",
    "mergeUpdate_config":           "Merge configuration properties rather than replacing.",
    "configurationProperties":      "Map of configuration property names to values.",
    "platformSecurityConnection":   "Connection object for the platform security connector.",
    "securityAccessControl":        "Security access control definition.",
    "secretsCollection":            "Secrets collection definition object.",
    "userAccount":                  "OpenMetadataUserAccount object.",
    "effectiveFrom_external":       "Effective-from date for the external ID link relationship.",
    "effectiveTo_external":         "Effective-to date for the external ID link relationship.",
}

# ── Functional groups ──────────────────────────────────────────────────────────

GROUPS: dict[str, dict] = {
    "create_entity": {
        "label":       "Create Entity",
        "description": "Create a new metadata entity. The 'properties' field holds the type-specific Layer 2 body.",
        "types":       ["NewElementRequestBody", "NewAttachmentRequestBody",
                        "NewOpenMetadataElementRequestBody", "ActionRequestBody"],
    },
    "create_from_template": {
        "label":       "Create from Template",
        "description": "Instantiate a new element by copying a template and substituting placeholder values.",
        "types":       ["TemplateRequestBody", "UpdateWithTemplateRequestBody"],
    },
    "update_entity": {
        "label":       "Update Entity",
        "description": "Update properties on an existing entity. mergeUpdate:true performs a partial update; false replaces all properties.",
        "types":       ["UpdateElementRequestBody", "UpdatePropertiesRequestBody",
                        "UpdateEffectivityDatesRequestBody", "ConnectorConfigPropertiesRequestBody"],
    },
    "delete_entity": {
        "label":       "Delete Entity",
        "description": "Delete a metadata entity. cascadeDelete removes anchored child elements.",
        "types":       ["DeleteElementRequestBody", "OpenMetadataDeleteRequestBody"],
    },
    "relationship": {
        "label":       "Relationship",
        "description": "Create, update, or delete a relationship between two elements.",
        "types":       ["NewRelationshipRequestBody", "UpdateRelationshipRequestBody",
                        "NewRelatedElementsRequestBody", "FindRelationshipRequestBody",
                        "DeleteRelationshipRequestBody"],
    },
    "classification": {
        "label":       "Classification",
        "description": "Add, update, or remove a classification on an element.",
        "types":       ["NewClassificationRequestBody", "UpdateClassificationRequestBody",
                        "DeleteClassificationRequestBody"],
    },
    "search": {
        "label":       "Search / Query",
        "description": "Find metadata elements by string, structured properties, or name. All include pagination and status-filter options.",
        "types":       ["SearchStringRequestBody", "FilterRequestBody", "FindRequestBody",
                        "GetRequestBody", "ResultsRequestBody", "HistoryRequestBody",
                        "UniqueNameRequestBody", "UniqueRequestBody",
                        "ActivityStatusFilterRequestBody", "ContentStatusFilterRequestBody",
                        "DeploymentStatusFilterRequestBody", "ActivityStatusRequestBody"],
    },
    "external_id": {
        "label":       "External Identifiers",
        "description": "Attach or manage external system identifiers on Egeria elements.",
        "types":       ["NewExternalIdRequestBody"],
    },
    "governance_action": {
        "label":       "Governance Actions",
        "description": "Initiate or manage governance engine actions and processes.",
        "types":       ["InitiateEngineActionRequestBody",
                        "InitiateGovernanceActionTypeRequestBody",
                        "InitiateGovernanceActionProcessRequestBody"],
    },
    "scalar": {
        "label":       "Simple / Scalar",
        "description": "Thin wrappers carrying a single value — used for targeted operations.",
        "types":       ["EffectiveTimeRequestBody", "MetadataSourceRequestBody",
                        "NameRequestBody", "StringRequestBody", "URLRequestBody"],
    },
    "admin": {
        "label":       "Admin / System",
        "description": "Platform administration, security configuration, and user management.",
        "types":       ["PlatformSecurityRequestBody", "SecretsCollectionRequestBody",
                        "SecurityAccessControlRequestBody", "UserAccountRequestBody"],
    },
}

_BODY_TO_GROUP: dict[str, str] = {
    bc: gk for gk, gd in GROUPS.items() for bc in gd["types"]
}


# ── Extraction ─────────────────────────────────────────────────────────────────

def _extract_json_object(text: str, match_start: int) -> dict | None:
    """Walk back from match_start to find the enclosing { and parse to end."""
    chunk_start = max(0, match_start - 400)
    pre = text[chunk_start:match_start]
    brace_pos = pre.rfind("{")
    if brace_pos < 0:
        return None
    abs_start = chunk_start + brace_pos
    snippet = text[abs_start: abs_start + 5000]
    depth = 0
    in_s = False
    esc = False
    end = 0
    for i, c in enumerate(snippet):
        if esc:
            esc = False
            continue
        if c == "\\" and in_s:
            esc = True
            continue
        if c == '"':
            in_s = not in_s
        if in_s:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if not end:
        return None
    try:
        obj = json.loads(snippet[:end])
        return obj if str(obj.get("class", "")).endswith("Body") else None
    except Exception:
        return None


def extract_from_directory(http_dir: Path) -> tuple[dict[str, set], dict[str, dict]]:
    """Return (body_fields, body_examples) from all .http files in http_dir."""
    body_fields: dict[str, set] = defaultdict(set)
    body_examples: dict[str, dict] = {}

    for f in sorted(http_dir.glob("*.http")):
        text = f.read_text(errors="replace")
        for m in re.finditer(r'"class"\s*:\s*"([A-Za-z]+Body)"', text):
            bc = m.group(1)
            obj = _extract_json_object(text, m.start())
            if obj:
                for k in obj:
                    body_fields[bc].add(k)
                if bc not in body_examples:
                    body_examples[bc] = obj

    return body_fields, body_examples


# ── Catalog assembly ───────────────────────────────────────────────────────────

def build_catalog(http_dir: Path) -> dict:
    body_fields, body_examples = extract_from_directory(http_dir)

    catalog: dict = {
        "_meta": {
            "description":  "Egeria REST API outer request body catalog.",
            "source":       str(http_dir),
            "howToRebuild": "python3 build_request_body_catalog.py [/path/to/http-client-collections]",
            "bodyCount":    len(body_fields),
        },
        "groups": {
            gk: {
                "label":       gd["label"],
                "description": gd["description"],
                "bodyTypes":   gd["types"],
            }
            for gk, gd in GROUPS.items()
        },
        "bodies": {},
    }

    for bc in sorted(body_fields):
        annotated = {
            f: FIELD_NOTES.get(f, "") for f in sorted(body_fields[bc])
        }
        catalog["bodies"][bc] = {
            "group":   _BODY_TO_GROUP.get(bc, "other"),
            "fields":  annotated,
            "example": body_examples.get(bc, {}),
        }

    return catalog


# ── Entry point ────────────────────────────────────────────────────────────────

def _resolve_http_dir(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
        if not p.is_dir():
            sys.exit(f"ERROR: path not found: {p}")
        return p

    env = os.environ.get("HTTP_COLLECTIONS_PATH")
    if env:
        p = Path(env)
        if not p.is_dir():
            sys.exit(f"ERROR: HTTP_COLLECTIONS_PATH={env} not found")
        return p

    for default in _DEFAULT_ROOTS:
        if default.is_dir():
            return default

    sys.exit(
        "ERROR: could not locate http-client-collections.\n"
        "Pass the path as an argument or set HTTP_COLLECTIONS_PATH."
    )


if __name__ == "__main__":
    http_dir = _resolve_http_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Reading from: {http_dir}", file=sys.stderr)

    catalog = build_catalog(http_dir)

    out_path = Path(__file__).resolve().parent / "egeria_request_body_catalog.json"
    out_path.write_text(json.dumps(catalog, indent=2))

    print(f"Wrote {catalog['_meta']['bodyCount']} body types → {out_path}", file=sys.stderr)
