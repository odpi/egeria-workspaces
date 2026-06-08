# The Catalog — pyegeria API Call Reference

Documents the pyegeria calls made by `tech_catalog_handler.py` and `glossary_handler.py` for each section of The Catalog. Use this as the authoritative working reference for API call strategy, known quirks, and debugging guidance.

All catalog calls go through `AssetMaker` (imported from `pyegeria`) unless noted. Credential params (`url`, `server`, `user_id`, `user_pwd`) are passed from the SPA via query params; the backend falls back to env vars when absent.

**Container pyegeria version: 6.0.13.6** (installed via `pip install pyegeria --upgrade` in Dockerfile-fast-api)

---

## Key pyegeria quirks (apply everywhere)

> These were discovered by source inspection of pyegeria 6.0.13.6 in the container and confirmed against live Coco data.

| Quirk | Detail |
|---|---|
| `find_*` status defaults | Every find method silently applies a status filter. Must pass `[]` to see all elements in Coco (which sets no explicit status). See table below. |
| `AssetMaker` constructor | Takes `view_server=` (not `server_name=`) |
| `ConnectionMaker` constructor | Takes `server_name=` (not `view_server=`). Also calls `check_connection()` immediately — do NOT pass a Bearer token; it causes a 401 on the check. Call `create_egeria_bearer_token()` after construction instead. |
| `Endpoint` is not an Asset | `AssetMaker.find_assets(metadata_element_type="Endpoint")` returns nothing. Must use `ConnectionMaker.find_endpoints()` and `ConnectionMaker.get_endpoint_by_guid()`. |
| `find_endpoints` kwargs | Signature: `(search_string, output_format, report_spec, body, **kwargs)`. Pass `graph_query_depth`, `start_from`, `page_size` via `**kwargs`. |
| Relationship data structure | pyegeria wraps related elements in `RelatedMetadataElementSummary` — the related element's header/properties are inside a nested `relatedElement` key, not at the top level of the relationship item. The `elementHeader.type.superTypeNames` list enables subtype nav resolution. |

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

**`graph_query_depth=3` is used for all detail fetches** to return the full relationship/property graph needed to populate the detail pane. This depth exposes nested schema links, lineage anchors, and multi-hop relationships that depth=1 misses.

| Type family | `section` param | Call | Notes |
|---|---|---|---|
| Asset subtypes (DeployedAPI, Action, DataStore, …) | `apis`, `actions`, `data-*` | `AssetMaker.get_asset_by_guid(guid, body={graphQueryDepth:3, relationshipsPageSize:50})` | Direct GUID lookup. |
| SoftwareCapability subtypes | `software-capabilities` | `find_software_capabilities(search_string="*", graph_query_depth=3)` then filter by GUID | O(n) scan — acceptable for ~50 items. `get_software_capability_by_guid(guid)` exists on `AssetMaker` and could replace this (O-8). |
| Endpoint | `endpoints` | `ConnectionMaker.get_endpoint_by_guid(guid, body={graphQueryDepth:3})` via `_connection_maker_from_asset_maker()` | Direct GUID lookup. ConnectionMaker is re-authenticated (fresh `create_egeria_bearer_token()`) — passing the token from AssetMaker causes a 401. |
| ITInfrastructure | `infrastructure` | `find_infrastructure(search_string="*", deployment_status_list=[], graph_query_depth=3)` then filter by GUID | O(n) scan — acceptable given small infrastructure list. |

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

## Open issues

| ID | Description | Status |
|---|---|---|
| O-1 | List-level `mermaidGraph` in `find_*` response root discarded by `_safe_list()` | Unconfirmed — needs live response inspection |
| O-2 | `_safe_list` only handles `"items"` key; may miss `"elements"` or `"elementList"` | Unconfirmed — needs live response inspection |
| O-3 | `MermaidSection` re-fetches context diagram even when embedded `mermaidGraph` already present in detail response | Low priority |
| O-8 | Software Capabilities detail: O(n) scan via `find_software_capabilities` instead of `get_software_capability_by_guid` | Low priority — fast at ~50 items |
| O-9 | `MermaidSection` fetch doesn't forward user credentials | Known limitation |
| O-10 | `DeployedAPI` elements may have no `mermaidGraph` in Coco data | Under investigation |
