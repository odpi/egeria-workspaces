# The Catalog — pyegeria API Call Reference

Documents the pyegeria calls made by `tech_catalog_handler.py`, `glossary_handler.py`, and the planned `tech_type_handler.py` for each section of The Catalog. Use this as the authoritative working reference for API call strategy, known quirks, and debugging guidance.

All catalog calls go through `AssetMaker` (imported from `pyegeria`) unless noted. Detail calls now go through `AssetCatalog.get_asset_graph` (see detail endpoint section). Technology Types use `AutomatedCuration`. Credential params (`url`, `server`, `user_id`, `user_pwd`) are passed from the SPA via query params; the backend falls back to env vars when absent.

**Container pyegeria version: 6.0.13.6** (installed via `pip install pyegeria --upgrade` in Dockerfile-fast-api)

---

## Key pyegeria quirks (apply everywhere)

> These were discovered by source inspection of pyegeria 6.0.13.6 in the container and confirmed against live Coco data.

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
| Tech Type detail by qualifiedName | `AutomatedCuration.get_tech_type_detail(filter_string=...)` accepts `qualifiedName` (already supported by `get_tech_type_by_name`). Use `qualifiedName` as the URL key — unique, stable, no collision risk. `technologyTypeGUID` from the list is the feedback/comment anchor. `get_tech_type_by_guid()` is planned but not yet available. |
| Tech Type elements exact-match | `get_technology_type_elements(filter_string)` requires exact type name — no wildcards. |

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

Each called when the user selects a section or sub-tab. Returns `{ items: [...], total: N }`. All use `graph_query_depth=0` for performance.

| Section | Sub-tab | Call | `metadata_element_type` | Status | Coco data |
|---|---|---|---|---|---|
| Glossary | _(whole section)_ | `GlossaryManager.get_glossaries()` | N/A | ✅ Working | ✅ Multiple glossaries |
| Infrastructure | IT Infrastructure | `find_infrastructure(search_string="*", deployment_status_list=[], graph_query_depth=0)` | `"ITInfrastructure"` | ✅ Fixed | ✅ Confirmed |
| Infrastructure | Software Capabilities | `find_software_capabilities(search_string="*", graph_query_depth=0)` | _(all)_ | ✅ Working | ✅ ~50 items |
| Infrastructure | Endpoints | `ConnectionMaker.find_endpoints(search_string="*", output_format="JSON", graph_query_depth=0)` | _(all)_ | ✅ Fixed | ✅ ~232 items |
| Data Assets | Data Stores | `find_data_assets(search_string="*", metadata_element_type="DataStore", content_status_list=[], graph_query_depth=0)` | `"DataStore"` | ✅ Fixed | ✅ ~95 items |
| Data Assets | Data Feeds | `find_data_assets(search_string="*", metadata_element_type="DataFeed", content_status_list=[], graph_query_depth=0)` | `"DataFeed"` | ✅ Fixed | ✅ Confirmed |
| Data Assets | Data Sets | `find_data_assets(search_string="*", metadata_element_type="DataSet", content_status_list=[], graph_query_depth=0)` | `"DataSet"` | ✅ Fixed | ✅ Confirmed |
| APIs | APIs | `find_assets(search_string="*", metadata_element_type="DeployedAPI", graph_query_depth=0)` | `"DeployedAPI"` | ✅ Working | ✅ 58 items |
| Processes | Software Components | `find_processes(search_string="*", metadata_element_type="DeployedSoftwareComponent", activity_status_list=[], graph_query_depth=0)` | `"DeployedSoftwareComponent"` | ✅ Fixed | ✅ Confirmed |
| Processes | Actions | `find_processes(search_string="*", metadata_element_type="Action", activity_status_list=[], graph_query_depth=0)` | `"Action"` | ✅ Fixed | ✅ 3+ items |

> **Note on Software Capabilities sorting:** `find_software_capabilities` does not support `sequencing_order` — results are sorted client-side in `AssetTabView`.

> **Note on DeployedAPI:** `find_assets` works because DeployedAPI → DeployedSoftwareComponent → Process → Asset. Switching to `find_processes(activity_status_list=[])` would allow status filtering but isn't needed currently.

---

## Detail endpoint — right-hand panel

Called when a sidebar item is clicked: `GET /api/tech-catalog/assets/{guid}?section={tab-id}`

**Primary path: `AssetCatalog.get_asset_graph(asset_guid=guid, output_format="JSON")`** — returns the full anchored-element graph including all mermaid fields, richer than `get_asset_by_guid` with a depth limit. After fetching the JSON, `get_asset_mermaid_graph(guid)` is called and the result is injected as `mermaidGraph` if not already embedded. Fallbacks are retained for types that don't work with the graph endpoint.

| Type family | `section` param | Primary call | Fallback |
|---|---|---|---|
| All Asset subtypes (DeployedAPI, DataStore, Action, ITInfrastructure, …) | any non-endpoint | `AssetCatalog.get_asset_graph(guid, output_format="JSON")` + `get_asset_mermaid_graph(guid)` | `AssetMaker.get_asset_by_guid(guid, body={graphQueryDepth:3})` |
| SoftwareCapability subtypes | `software-capabilities` | Same `get_asset_graph` primary path | `find_software_capabilities(graph_query_depth=3)` filter by GUID |
| Endpoint | `endpoints` | `ConnectionMaker.get_endpoint_by_guid(guid, body={graphQueryDepth:3})` | _(none — endpoints use a dedicated path)_ |

**Notes:**
- `AssetCatalog` is instantiated via `_asset_catalog_from_asset_maker(mgr)` which shares credentials from the already-constructed `AssetMaker` (fresh `create_egeria_bearer_token()` call required — same reason as ConnectionMaker).
- `get_asset_graph` calls `/as-graph` on the Egeria platform, returning all elements anchored to the asset. The JSON structure is the same element format as `get_asset_by_guid`.
- Schema sub-pane still uses `AssetMaker.get_asset_by_guid` with `includeOnlyRelationships: ["Schema", "AttributeForSchema"]` and depth=5 — no change needed there.
- Lineage sub-pane uses `AssetCatalog.get_asset_lineage_mermaid_graph(guid)` — unchanged.

---

## Glossary endpoints (served by `glossary_handler.py`)

The Glossary section is the first tile in The Catalog. It reuses `glossary_handler.py` which was built for Egeria Explorer.

| Endpoint | Handler call | Notes |
|---|---|---|
| `GET /api/glossary` | `GlossaryManager.get_glossaries()` | Returns `{ glossaries: [...] }` |
| `GET /api/glossary/{guid}/folders` | `GlossaryManager.get_glossary_categories()` | Returns `{ folders: [...] }` |
| `GET /api/glossary/{guid}/terms` | `GlossaryManager.get_terms_for_glossary()` | Returns `{ terms: [...] }` |
| `GET /api/glossary-terms?q=` | `GlossaryManager.find_glossary_terms()` | Cross-glossary search, returns `{ terms: [...] }` |
| `GET /api/glossary/term/{guid}` | `GlossaryManager.get_glossary_term_by_guid()` with depth=3 | Full term detail with relationships and classifications |

---

## Cross-navigation (implemented — TC-8)

Cross-navigation is fully implemented. Relationship cards in the detail pane show a **"View →"** button whenever the related element's type (or any of its `superTypeNames`) maps to a known section/tab. Clicking navigates the SPA: switches section, activates the correct sub-tab, and fetches the target element's detail directly (the list loads in the background).

### TYPE_TO_NAV mapping (frontend `tech-catalog.html`)

| Related element typeName (or supertype) | Navigates to section | Navigates to tab |
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

> **Subtype fallback:** When the exact `typeName` is not in the map (e.g., `SecretsCollection`), the frontend walks `relatedElement.superTypes` (from `elementHeader.type.superTypeNames`) to find the first matching ancestor. This means most Egeria subtypes are automatically navigable without being explicitly listed.

### Known navigable relationships in Coco data

| Viewing | Relationship type | Related element type | Tab navigated to |
|---|---|---|---|
| DataStore | `DataSetContent` | DataSet subtypes (SecretsCollection, etc.) | `data-sets` |
| DataStore | `AssetConnection` | Connection | _(not mapped — no catalog tab for Connections)_ |
| ITInfrastructure | `SupportedSoftwareCapability` | SoftwareCapability subtypes | `software-capabilities` |
| SoftwareCapability | `SoftwareCapabilityDependency` | SoftwareCapability subtypes | `software-capabilities` |
| DeployedAPI | `APIEndpoint` | Endpoint | `endpoints` |
| DataSet | `DataSetContent` | DataStore subtypes | `data-stores` |

---

## Mermaid diagrams in the detail pane

### Rendering order

> **Properties → Classifications → Diagrams → Relationships → Comments**

### Two diagram paths

| Path | Component | Data source | Trigger |
|---|---|---|---|
| Embedded | `AvailableMermaidDiagrams` | Mermaid fields in the serialised `item` (passed through by `_serialize()` via `_MERMAID_FIELDS` set) | Renders immediately when field is present |
| On-demand | `MermaidSection` → `DiagramPanel` | `GET /api/mermaid/{guid}` → `ClassificationExplorer.get_element_by_guid` | User clicks "Load Context Diagram" |
| On-demand | `MermaidSection` → `DiagramPanel` | `GET /api/mermaid/{guid}/anchored` → `MetadataExpert.get_anchored_element_graph` | User clicks "Load Anchored Graph" |

The fields `mermaidGraph` and `anchorMermaidGraph` are excluded from inline rendering (`_MERMAID_SECTION_FIELDS`) — they are served by the on-demand buttons.

### Bugs fixed

- **Bug 1 (FIXED):** `_serialize()` stripped all mermaid fields. Now iterates `_MERMAID_FIELDS` and passes through non-empty values.
- **Bug 2 (FIXED):** `DiagramPanel` called `.text()` on the JSON response and fed raw JSON to Mermaid.js. Now calls `.json()` and extracts `data.mermaidGraph`.
- **Bug 3 (FIXED):** Mermaid field names appeared in the Properties table. Fixed by adding `_ALL_MERMAID_FIELDS` to `skipKeys` in `AssetDetail`.

### Known limitation

`MermaidSection` fetch URLs don't forward user credentials — `mermaid_handler.py` falls back to env-var defaults. Portal-authenticated users with non-default credentials get diagrams from the wrong identity (O-9).

---

## Technology Types section (planned — `tech_type_handler.py`)

Technology Types are **Valid Metadata Values** — recipes for how to deploy, catalog, and govern specific technologies. They live outside the Egeria Type System. All calls use `AutomatedCuration` (takes `view_server=`, same as `AssetMaker`).

See `tech_type_plan.md` for the full design, data model, and open questions.

### List / search

| Route | Call | Notes |
|---|---|---|
| `GET /api/tech-catalog/tech-types?q=` | `AutomatedCuration.find_technology_types(search_string=q)` | Default `limit_results_by_status=["ACTIVE"]` — no override needed. Returns list of summary dicts. |
| `GET /api/tech-catalog/tech-types?q=*` | `AutomatedCuration.get_all_technology_types()` | Convenience wrapper for `find_technology_types("*")`. |
| `GET /api/tech-catalog/tech-types/hierarchy?root=...` | `AutomatedCuration.get_tech_type_hierarchy(filter_string=root)` | Passing `"*"` or omitting root defaults to `"Root Technology Type"`. Shape of the hierarchy response (flat parent-child vs. recursive tree) needs live inspection (TT-Q1). |

### Detail

| Route | Call | Notes |
|---|---|---|
| `GET /api/tech-catalog/tech-types/{qualifiedName}` | `AutomatedCuration.get_tech_type_detail(filter_string=qualifiedName)` | `get_tech_type_detail` / `get_tech_type_by_name` already accepts qualifiedName. URL-decode before calling. `qualifiedName` is unique — no collision risk. Returns single `element` dict. |
| `GET /api/tech-catalog/tech-types/{qualifiedName}/elements` | `AutomatedCuration.get_technology_type_elements(filter_string=displayName)` | Live instances. `get_technology_type_elements` needs `displayName` not qualifiedName — extract from the already-fetched detail response. Exact-match, no wildcards. |
| `GET /api/tech-catalog/tech-types/by-guid/{guid}` _(planned)_ | `AutomatedCuration.get_tech_type_by_guid(guid)` _(planned pyegeria method)_ | Future GUID-keyed route. Add backend endpoint once pyegeria method is available (TT-8). |

### Key fields in the detail response

| Field | Type | Content |
|---|---|---|
| `technologyTypeGUID` | str | Use as GUID anchor for `EgeriaFeedbackWidget` / `EgeriaCommentsSection` |
| `qualifiedName` | str | **Used as the detail lookup key** (URL-encoded in route). Unique and stable. |
| `displayName` | str | Human-readable name. Required by `get_technology_type_elements` — pass this, not qualifiedName. |
| `description` | str | Markdown-safe description |
| `url` | str | External project/documentation URL (if present) |
| `mermaidGraph` | str | Overview mermaid diagram (if present) |
| `specificationMermaidGraph` | str | Structure diagram (if present) |
| `catalogTemplates[]` | list | Parameterised blueprints; each has `placeholderProperty[]` — the key config surface |
| `governanceActionProcesses[]` | list | Survey/integrate/govern workflows applicable to this type |
| `externalReferences[]` | list | Doc links; each has `url` and `displayName` |

### Status filter

`find_technology_types` defaults to `limit_results_by_status=["ACTIVE"]` — correct behaviour, no override needed. Draft/inactive types are excluded by default.

---

## Open issues

| ID | Description | Status |
|---|---|---|
| O-1 | List-level `mermaidGraph` in `find_*` response root discarded by `_safe_list()` | Unconfirmed — needs live response inspection |
| O-2 | `_safe_list` only handles `"items"` key; may miss `"elements"` or `"elementList"` | Unconfirmed — needs live response inspection |
| O-3 | `MermaidSection` re-fetches context diagram even when embedded `mermaidGraph` already present in detail response | Low priority |
| O-8 | Software Capabilities detail: O(n) scan via `find_software_capabilities` instead of `get_software_capability_by_guid` | Low priority — fast at ~50 items |
| O-9 | `MermaidSection` fetch doesn't forward user credentials | Known limitation |
| O-10 | `DeployedAPI` elements may have no `mermaidGraph` in Coco data | Under investigation |
| TT-Q1 | Shape of `get_tech_type_hierarchy` response — flat parent-child list or recursive tree? | Needs live data inspection |
| TT-Q2 | Is `category` field reliably populated in list results? | Needs live data inspection |
| TT-Q3 | Confirm `get_technology_type_elements` is truly exact-match (no wildcards) | Needs live data test |
| TT-Q4 | Is `specificationMermaidGraph` meaningfully different from `mermaidGraph`? | Needs live examples |
| TT-Q7 | Does `technologyTypeGUID` refer to the `ValidMetadataValue` element GUID? (Safe to use as feedback anchor?) | Needs confirmation |
