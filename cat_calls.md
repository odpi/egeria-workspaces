# The Catalog — pyegeria API Call Reference

Documents the pyegeria calls made by `tech_catalog_handler.py` and `glossary_handler.py` for each section of The Catalog. Use this as the authoritative working reference for API call strategy, known quirks, and debugging guidance.

All catalog calls go through `AssetMaker` (imported from `pyegeria`) unless noted. Detail calls go through `AssetCatalog.get_asset_graph` (see detail endpoint section). Technology Types use `AutomatedCuration`. Credential params (`url`, `server`, `user_id`, `user_pwd`) are passed from the SPA via query params; the backend falls back to env vars when absent.

**Container pyegeria version: manually updated — see container pip list** (installed via `pip install pyegeria --upgrade` in Dockerfile-fast-api; recently updated in-container to pick up `get_asset_graph` body parameter support)

---

## Key pyegeria quirks (apply everywhere)

| Quirk | Detail |
|---|---|
| `find_*` status defaults | Every find method silently applies a status filter. Must pass `[]` to see all elements in Coco (which sets no explicit status). See table below. |
| `AssetMaker` constructor | Takes `view_server=` (not `server_name=`) |
| `AssetCatalog` constructor | Takes `view_server=`. Used for `get_asset_graph` (detail) and `get_asset_lineage_mermaid_graph`. |
| `AutomatedCuration` constructor | Takes `view_server=`. Used for Technology Types. |
| `ConnectionMaker` constructor | Takes `server_name=` (not `view_server=`). Also calls `check_connection()` immediately — do NOT pass a Bearer token; it causes a 401 on the check. Call `create_egeria_bearer_token()` after construction instead. |
| `Endpoint` is not an Asset | `AssetMaker.find_assets(metadata_element_type="Endpoint")` returns nothing. Must use `ConnectionMaker.find_endpoints()` and `ConnectionMaker.get_endpoint_by_guid()`. |
| `find_endpoints` kwargs | Signature: `(search_string, output_format, report_spec, body, **kwargs)`. Pass `graph_query_depth`, `start_from`, `page_size` via `**kwargs`. |
| Relationship data structure | pyegeria wraps related elements in `RelatedMetadataElementSummary` — the related element's header/properties are inside a nested `relatedElement` key, not at the top level of the relationship item. The `elementHeader.type.superTypeNames` list enables subtype nav resolution. |
| `get_asset_graph` body parameter | Updated in recent pyegeria: now accepts `body: Optional[dict \| ResultsRequestBody] = None`. Pass `{"class": "ResultsRequestBody", "graphQueryDepth": N}` to control traversal depth. Default (no body) uses Egeria server default depth. |
| `get_tech_type_detail` lookup | The underlying `/technology-types/by-name` call matches by **`deployedImplementationType`**. The frontend passes `?deployed_implementation_type=` alongside the qualifiedName path param. Falls back to `display_name` then `qualified_name` if absent. |
| Tech Type elements exact-match | `get_technology_type_elements(filter_string)` requires exact displayName — no wildcards. |
| `_safe_list` only handles `"items"` | `_safe_list(raw)` checks `isinstance(raw, list)` then `raw.get("items")`. Does NOT handle `"elements"` or `"elementList"` keys — may silently return empty list for some responses (O-2). |
| Sequencing | List endpoints use `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"`. `find_software_capabilities` does not support sequencing — sorted client-side. |
| Classification structure | pyegeria stores each classification as a **named key directly on `elementHeader`** (e.g. `header["zoneMembership"]`, `header["dataAssetEncoding"]`), not in a `classifications` list. Each value is a dict with `"class": "ElementClassification"`, optional `classificationName`, `type.typeName`, and `classificationProperties`. `_extract_classifications` iterates `header.items()` and filters by `class == "ElementClassification"`. Internal types are removed by `_SKIP_CLASSIFICATIONS` = `{Anchors, LatestChange, Memento, TemplateSubstitute, SpineObject, SpineAttribute, ObjectIdentifier}`. |
| Bearer token API (container pyegeria) | `create_egeria_bearer_token()` — creates a token AND returns the raw token string (store the return value). `set_bearer_token(token)` — injects an existing token string into the client's `Authorization` header. `get_token()` — returns `"Bearer <token>"` from `text_headers`. There is **no** `egeria_bearer_token` attribute. |

### Status filter defaults

| pyegeria method | Status param | Default (wrong for Coco) | Fix |
|---|---|---|---|
| `find_infrastructure` | `deployment_status_list` | `["ACTIVE"]` | `deployment_status_list=[]` |
| `find_data_assets` | `content_status_list` | `["ACTIVE"]` | `content_status_list=[]` |
| `find_processes` | `activity_status_list` | `["IN_PROGRESS"]` | `activity_status_list=[]` |
| `find_software_capabilities` | _(none)_ | N/A | No change needed |
| `find_endpoints` | _(none confirmed)_ | Unknown | Monitor; may need `body={"contentStatusList":[]}` |

---

## List endpoints — left-hand navigation

Called when the user selects a section or sub-tab. Returns `{ items: [...], total: N }`. All use `graph_query_depth=0` for performance.

### Infrastructure

| Sub-tab | pyegeria call | Class | Key params |
|---|---|---|---|
| IT Infrastructure | `AssetMaker.find_infrastructure` | `AssetMaker` | `search_string=q\|"*"`, `metadata_element_type="ITInfrastructure"`, `deployment_status_list=[]`, `start_from`, `page_size`, `output_format="JSON"`, `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"`, `graph_query_depth=0` |
| Software Capabilities | `AssetMaker.find_software_capabilities` | `AssetMaker` | `search_string=q\|"*"`, `start_from`, `page_size`, `output_format="JSON"`, `graph_query_depth=0` _(no sequencing support)_ |
| Endpoints | `ConnectionMaker.find_endpoints` | `ConnectionMaker` | `search_string=q\|"*"`, `output_format="JSON"`, `start_from`, `page_size`, `graph_query_depth=0` _(via **kwargs)_ |

### Data Assets

| Sub-tab | pyegeria call | Key params |
|---|---|---|
| Data Stores | `AssetMaker.find_data_assets` | `search_string=q\|"*"`, `metadata_element_type="DataStore"`, `content_status_list=[]`, `start_from`, `page_size`, `output_format="JSON"`, `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"`, `graph_query_depth=0` |
| Data Feeds | `AssetMaker.find_data_assets` | same as above with `metadata_element_type="DataFeed"` |
| Data Sets | `AssetMaker.find_data_assets` | same as above with `metadata_element_type="DataSet"` |

### APIs

| Sub-tab | pyegeria call | Key params |
|---|---|---|
| APIs | `AssetMaker.find_assets` | `search_string=q\|"*"`, `metadata_element_type="DeployedAPI"`, `start_from`, `page_size`, `output_format="JSON"`, `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"`, `graph_query_depth=0` |

> `find_assets` is used (not `find_processes`) because DeployedAPI → DeployedSoftwareComponent → Process → Asset hierarchy makes it reachable. `find_processes(activity_status_list=[])` would also work if status filtering becomes needed.

### Processes

| Sub-tab | pyegeria call | Key params |
|---|---|---|
| Software Components | `AssetMaker.find_processes` | `search_string=q\|"*"`, `metadata_element_type="DeployedSoftwareComponent"`, `activity_status_list=[]`, `start_from`, `page_size`, `output_format="JSON"`, `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"`, `graph_query_depth=0` |
| Actions | `AssetMaker.find_processes` | same as above with `metadata_element_type="Action"` |

### Technology Types

| Sub-tab | pyegeria call | Key params |
|---|---|---|
| Technology Types (flat list) | `AutomatedCuration.find_technology_types` | `search_string=q\|"*"`, `start_from`, `page_size`, `output_format="JSON"` _(status defaults to `["ACTIVE"]` — correct)_ |
| Technology Types (hierarchy) | `AutomatedCuration.get_tech_type_hierarchy` | `filter_string=root\|"Root Technology Type"`, `output_format="JSON"` |

> List results are deduplicated by `qualifiedName` client-side in the backend — when duplicates exist (same type registered by multiple content packs), the entry with more `catalogTemplates` is kept.

---

## Detail endpoint — `GET /api/tech-catalog/assets/{guid}?section={tab-id}`

All detail calls use `graphQueryDepth=5`. Called when a sidebar item is clicked. Returns the full serialised element with relationships, classifications, and mermaid fields.

### `_fetch_detail` call sequence

The backend tries each path in order, returning on first success:

#### 1. Endpoints (section = `"endpoints"`) — dedicated path

| Call | Class | Params |
|---|---|---|
| `ConnectionMaker.get_endpoint_by_guid` | `ConnectionMaker` | `guid=guid`, `output_format="JSON"`, `graph_query_depth=5` |

Returns `None` (404) if this fails — no further fallback for endpoints. Note: parameter is `guid=` (not `endpoint_guid=`); `graph_query_depth` is a direct kwarg, not passed via `body`.

#### 2 & 3. All Asset types — graph with depth 5

All sections now use the same path. No `get_asset_mermaid_graph` injection — mermaid fields come from the `get_asset_graph` response directly.

| Call | Class | Params |
|---|---|---|
| `AssetCatalog.get_asset_graph` | `AssetCatalog` | `asset_guid=guid`, `output_format="JSON"`, `body={"class": "ResultsRequestBody", "graphQueryDepth": 5}` |

Falls through to step 4 on exception.

#### 4. Fallback — targeted section finders (software-capabilities, infrastructure only)

Defined in `_SECTION_FINDERS`:

| section | Call | Params |
|---|---|---|
| `"software-capabilities"` | `AssetMaker.find_software_capabilities` | `search_string="*"`, `output_format="JSON"`, `graph_query_depth=5` |
| `"infrastructure"` | `AssetMaker.find_infrastructure` | `search_string="*"`, `output_format="JSON"`, `graph_query_depth=5`, `deployment_status_list=[]`, `sequencing_order="PROPERTY_ASCENDING"`, `sequencing_property="displayName"` |

Result filtered by GUID via `_find_by_guid`. Falls through to step 5 on exception.

#### 5. Fallback — `get_asset_by_guid`

| Call | Class | Params |
|---|---|---|
| `AssetMaker.get_asset_by_guid` | `AssetMaker` | `asset_guid=guid`, `output_format="JSON"`, `body={"class": "GetRequestBody", "graphQueryDepth": 5, "relationshipsPageSize": 50}` |

Falls through to step 6 on exception.

#### 6. Last resort — SoftwareCapability scan

| Call | Class | Params |
|---|---|---|
| `AssetMaker.find_software_capabilities` | `AssetMaker` | `search_string="*"`, `output_format="JSON"`, `graph_query_depth=5` |

Result filtered by GUID. Returns `None` if all paths fail → 404.

---

## Schema sub-pane — `GET /api/tech-catalog/assets/{guid}/schema`

| Call | Class | Params |
|---|---|---|
| `AssetMaker.get_asset_by_guid` | `AssetMaker` | `asset_guid=guid`, `output_format="JSON"`, `body={"class": "GetRequestBody", "graphQueryDepth": 5, "relationshipsPageSize": 200, "includeOnlyRelationships": ["Schema", "AttributeForSchema"]}` |

Result passed through `_serialize_schema` which extracts `schemaType` + nested attribute list. Attributes sorted by `position` ascending.

---

## Lineage sub-pane — `GET /api/tech-catalog/assets/{guid}/lineage`

| Call | Class | Params |
|---|---|---|
| `AssetCatalog.get_asset_lineage_graph` | `AssetCatalog` | `asset_guid=guid`, `output_format="MERMAID"` |

Returns `{"mermaidGraph": ""}` when Egeria returns 400 (asset has no lineage data). Other errors propagate as 500.

---

## Technology Types detail — `GET /api/tech-catalog/tech-types/{qualifiedName}`

| Call | Class | Params |
|---|---|---|
| `AutomatedCuration.get_tech_type_detail` | `AutomatedCuration` | `filter_string=deployed_implementation_type\|display_name\|qualified_name`, `output_format="JSON"` |

> **Critical:** `get_tech_type_detail` calls `/technology-types/by-name` which matches on **`deployedImplementationType`**. The frontend passes `?deployed_implementation_type=` query param; backend falls back to `display_name` then `qualified_name`. The `deployedImplementationType` value is now included in `_serialize_tech_type` output and passed by the frontend.

## Technology Types instances — `GET /api/tech-catalog/tech-types/{qualifiedName}/elements`

| Call | Class | Params |
|---|---|---|
| `AutomatedCuration.get_technology_type_elements` | `AutomatedCuration` | `filter_string=display_name\|last segment of qualifiedName`, `start_from`, `page_size`, `output_format="JSON"` |

> Exact displayName match required — no wildcards. `filter_string` prefers `?display_name=` query param; falls back to splitting `qualifiedName` on `:` and taking the last segment.

---

## Glossary endpoints (served by `glossary_handler.py`)

| Route | Call | Notes |
|---|---|---|
| `GET /api/glossary` | `GlossaryManager.find_glossaries(search_string="*", graph_query_depth=0)` | Returns `{ glossaries: [...] }` |
| `GET /api/glossary/{guid}/folders` | `GlossaryManager.get_collection_members(collection_guid)` | Returns `{ folders: [...] }`; filters by `CollectionFolder` type |
| `GET /api/glossary/{guid}/terms` | `GlossaryManager.get_collection_members(collection_guid)` | Returns `{ terms: [...] }`; filters by `GlossaryTerm` type |
| `GET /api/glossary-terms?q=` | `GlossaryManager.find_glossary_terms(graph_query_depth=1)` | Cross-glossary search, returns `{ terms: [...] }` |
| `GET /api/glossary/term/{guid}` | `GlossaryManager.get_term_by_guid(graphQueryDepth=1)` | Full term detail with relationships and classifications |

---

## Cross-navigation (TC-8 — implemented)

Relationship cards in the detail pane show a **"View →"** button whenever the related element's type (or any of its `superTypeNames`) maps to a known section/tab.

### TYPE_TO_NAV mapping (frontend `tech-catalog.html`)

| Related element typeName (or supertype) | Section | Tab |
|---|---|---|
| `ITInfrastructure` and subtypes (SoftwareServer, Host, …) | `infrastructure` | `infrastructure` |
| `SoftwareCapability` and subtypes (APIManager, DatabaseManager, …) | `infrastructure` | `software-capabilities` |
| `Endpoint` | `infrastructure` | `endpoints` |
| `DataStore` and subtypes (Database, CSVFile, DataFile, …) | `data-assets` | `data-stores` |
| `DataFeed` and subtypes (Topic, KafkaTopic, …) | `data-assets` | `data-feeds` |
| `DataSet` and subtypes (SecretsCollection, VirtualRelationalTable, …) | `data-assets` | `data-sets` |
| `DeployedAPI` | `apis` | `apis` |
| `DeployedSoftwareComponent` and subtypes | `processes` | `software-components` |
| `GlossaryTerm`, `Glossary`, `GlossaryCategory` | `glossary` | `glossary` |

> Subtype fallback: when exact `typeName` is not in the map, the frontend walks `relatedElement.superTypes` (from `elementHeader.type.superTypeNames`) to find the first matching ancestor.

---

## Mermaid diagrams in the detail pane

### Two rendering paths

| Path | Component | Data source | Trigger |
|---|---|---|---|
| Embedded | `AvailableMermaidDiagrams` | Mermaid fields in serialised `item` (passed through by `_serialize()` via `_MERMAID_FIELDS` set) | Renders immediately when field is present |
| On-demand (context) | `MermaidSection` → `DiagramPanel` | `GET /api/mermaid/{guid}` → `ClassificationExplorer.get_element_by_guid` | User clicks "Load Context Diagram" |
| On-demand (anchored) | `MermaidSection` → `DiagramPanel` | `GET /api/mermaid/{guid}/anchored` → `MetadataExpert.get_anchored_element_graph` | User clicks "Load Anchored Graph" |

### `_MERMAID_FIELDS` (passed through by `_serialize`)

```
mermaidGraph, anchorMermaidGraph, edgeMermaidGraph,
localLineageGraph, fieldLevelLineageGraph,
informationSupplyChainMermaidGraph, iscImplementationMermaidGraph,
actionMermaidGraph, specificationMermaidGraph,
solutionBlueprintMermaidGraph, solutionSubcomponentMermaidGraph,
governanceActionProcessMermaidGraph, organizationTreeMermaidGraph,
collectionMermaidMindMap
```

`mermaidGraph` and `anchorMermaidGraph` are excluded from inline `AvailableMermaidDiagrams` rendering (`_MERMAID_SECTION_FIELDS`) — they are served by on-demand buttons only.

### Known limitation

`MermaidSection` fetch URLs don't forward user credentials — `mermaid_handler.py` falls back to env-var defaults. Portal-authenticated users with non-default credentials get diagrams from the wrong identity (O-9).

---

## `_serialize` output fields

Every list item and detail response is normalised through `_serialize(el, include_relationships=False)`:

| Field | Source |
|---|---|
| `guid` | `elementHeader.guid` |
| `typeName` | `elementHeader.type.typeName` |
| `displayName` | `properties.displayName` \| `properties.name` |
| `qualifiedName` | `properties.qualifiedName` |
| `description` | `properties.description` |
| `deployedImplementationType` | `properties.deployedImplementationType` |
| `deploymentStatus` | `properties.deploymentStatus` |
| `activityStatus` | `properties.activityStatus` |
| `networkAddress` | `properties.networkAddress` |
| `classifications` | named `ElementClassification` keys on `elementHeader`, iterated by `_extract_classifications`; internal types removed by `_SKIP_CLASSIFICATIONS` |
| `relationships` | extracted via `_extract_relationships` (detail only, `include_relationships=True`) |
| `hasSchema` | `True` if `schemaType` key is present and contains a `relatedElement` |
| `hasLineage` | Currently always `True` — see TC-9 in backlog to determine which types genuinely support lineage. The lineage endpoint handles non-Asset GUIDs gracefully (returns empty graph). |
| `mermaidGraph` et al. | any `_MERMAID_FIELDS` present in element or `properties` with non-empty, non-"no " value |

---

## Authentication endpoints

| Route | Method | Purpose |
|---|---|---|
| `/api/egeria-token` | `POST` | Mint a new Egeria Bearer token. Body: `{ user_id, url, server }`. Returns `{ token, user_id }`. Frontend calls this on 401 to refresh an expired token before retrying the original request. |
| `/api/debug/raw/{guid}` | `GET` | Diagnostic endpoint — returns raw pyegeria response for a GUID, including `raw_classifications`, `extracted` (output of `_extract_classifications`), `header_keys`, `element_type`, and `fetch_method`. Tries `get_asset_by_guid(depth=1)`, then `find_infrastructure`, then `get_term_by_guid`. |

### Frontend token refresh flow

`fetchWithToken` wraps every backend call. On HTTP 401 (token expired):
1. Calls `_tokenRefresher.refresh(creds)` — POST to `/api/egeria-token`
2. Updates `creds.token` state with new token
3. Retries the original request once with `_isRetry=true` flag to prevent loops

HTTP 403 (Egeria-level `USER_NOT_AUTHORIZED`) is not retried — the detail pane shows a lock icon instead. `_is_auth_error(exc)` in the backend detects both `response_code in (401, 403)` and string patterns `USER_NOT_AUTHORIZED`, `NOT_AUTHORIZED`, `AUTHORIZATION_ERROR`.

---

## Open issues

| ID | Description | Status |
|---|---|---|
| O-1 | List-level `mermaidGraph` in `find_*` response root discarded by `_safe_list()` | Unconfirmed — needs live response inspection |
| O-2 | `_safe_list` only handles `"items"` key; may silently return empty list for responses using `"elements"` or `"elementList"` | Unconfirmed — monitor for unexpected empty panels |
| O-3 | `MermaidSection` re-fetches context diagram even when embedded `mermaidGraph` already present in detail response | Low priority |
| O-8 | Software Capabilities detail: O(n) scan via `find_software_capabilities` fallback instead of direct GUID lookup | Low priority — fast at ~50 items; primary `get_asset_graph` path should handle most cases |
| O-9 | `MermaidSection` on-demand fetch doesn't forward user credentials — uses env-var defaults | Known limitation |
| O-10 | `DeployedAPI` elements may have no `mermaidGraph` in Coco data | Under investigation |
| O-11 | `get_asset_graph` with default depth may return sparse detail for non-data-asset types | **Resolved** — all detail calls now use `graphQueryDepth=5` |
| O-12 | `get_tech_type_detail` lookup used wrong field | **Resolved** — backend now accepts `?deployed_implementation_type=`; frontend passes it; `_serialize_tech_type` includes the field |
| TT-Q1 | Shape of `get_tech_type_hierarchy` response — flat parent-child list or recursive tree? | Needs live data inspection |
| TT-Q2 | Is `category` field reliably populated in list results? | Needs live data inspection |
| TT-Q3 | Confirm `get_technology_type_elements` is truly exact-match (no wildcards) | Needs live data test |
| TT-Q4 | Is `specificationMermaidGraph` meaningfully different from `mermaidGraph`? | Needs live examples |

---

## Lineage Explorer endpoints (`lineage_handler.py`)

### pyegeria methods used

| Method | Class | Purpose |
|---|---|---|
| `find_assets(search_string, graph_query_depth=0, output_format="JSON")` | `AssetMaker` | Asset search — returns list elements with `elementHeader` + `properties` |
| `get_asset_graph(asset_guid, as_of_time, output_format="JSON")` | `AssetCatalog` | Full asset graph including lineage + ISC membership |
| `get_asset_lineage_graph(asset_guid, as_of_time, limit_to_isc_q_name, hilight_isc_q_name, all_anchors, output_format="JSON")` | `AssetCatalog` | End-to-end lineage graph(s) + linked assets table |

**Auth pattern**: Token only — no `user_id`/`user_pwd` query params. Bearer token via `X-Egeria-Token` header. Credentials for pyegeria client init come from env vars (`EGERIA_PLATFORM_URL`, `EGERIA_VIEW_SERVER`, `EGERIA_USER`, `EGERIA_USER_PASSWORD`).

### `GET /api/lineage/search`

**Query params**: `q` (search string, default `*`), `url`, `server`

**Response**: `{"items": [{guid, typeName, displayName, qualifiedName, description}]}`

Calls `AssetMaker.find_assets(search_string=q, graph_query_depth=0)`. Returns empty list on 400/404 (no results), raises 500 on other errors.

### `GET /api/lineage/asset/{guid}/graph`

**Query params**: `as_of_time` (ISO 8601 or absent = now), `url`, `server`

**Response**: Raw JSON dict from `AssetCatalog.get_asset_graph`. Frontend extracts:

| Key | Type | Description |
|---|---|---|
| `elementHeader` | dict | `guid`, `createTime`, `updateTime`, `type.typeName`, `type.superTypeNames` |
| `properties` | dict | `displayName`, `qualifiedName`, `description`, and other asset properties |
| `localLineageGraph` | string | Mermaid — direct lineage relationships (may be absent/null) |
| `fieldLevelLineageGraph` | string | Mermaid — field-to-field mappings (may be absent/null) |
| `lineageLinkage` | list | Lineage relationship objects; each has `guid`, `label`, `description`, `relatedElement.elementHeader`, `relatedElement.properties` |
| `partOfInformationSupplyChains` | list | ISC membership; each has `relatedElement.elementHeader.guid` and `relatedElement.properties.{qualifiedName,displayName,description}` |

Returns `{"error": "not_found"}` (404) when the asset is not found or Egeria returns 400/404.

**Time travel**: Pass `as_of_time=<ISO 8601>` to query historical lineage state. The frontend derives the slider range from `elementHeader.createTime` (fallback: 30 days ago) to `Date.now()`. Slider fires on `mouseup`/`touchend` only to avoid flooding the API.

### `GET /api/lineage/asset/{guid}/lineage-graph`

**Query params**: `as_of_time`, `limit_to_isc` (qualifiedName), `highlight_isc` (qualifiedName), `all_anchors` (`"true"` or absent), `url`, `server`

**Response**: Raw JSON dict from `AssetCatalog.get_asset_lineage_graph`. Frontend extracts:

| Key | Type | Description |
|---|---|---|
| `mermaidGraph` / `fullLineageMermaidGraph` | string | Mermaid — end-to-end data and control flow |
| `edgeMermaidGraph` | string | Mermaid — extreme source/destination nodes only |
| `linkedAssets` | list | All nodes in the full lineage graph; each has `elementHeader` (guid, createTime, updateTime) and `properties` (displayName, qualifiedName, description) |

Returns `{"mermaidGraph":"","edgeMermaidGraph":"","linkedAssets":[]}` on 400/404 (no lineage).

**ISC filter options** (mutually exclusive):
- `limit_to_isc=<qualifiedName>` → restrict graph to single ISC (`limitToISCQualifiedName`)
- `highlight_isc=<qualifiedName>` → show full graph but highlight this ISC (`highlightISCQualifiedName`)

**`all_anchors=true`** → pass `all_anchors=True` to pyegeria — includes field-level detail in graphs.

This endpoint is only called when `localLineageGraph` from the `/graph` response is non-null.
