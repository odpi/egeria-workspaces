# Technical Asset Catalog — Specification

**The Catalog** is a tile on the quickstart (and freshstart) portal. It is aimed at technical users who work directly with assets: infrastructure engineers, data engineers, API developers, and architects browsing the governed vocabulary.

When you launch The Catalog, there are **five tiles** (Glossary is first):

| Tile | Description |
|---|---|
| **Glossary** | Browse glossaries, categories, and terms; cross-link to data assets |
| **Infrastructure Assets** | Servers, storage, networks, software capabilities, and endpoints |
| **Data Assets** | Data stores, data feeds, and data sets |
| **APIs** | Deployed APIs and their endpoints |
| **Processes** | Software components, actions, and governance action process definitions |

---

## General features

When a tile is selected, it opens a page with a left-hand navigation panel and a right-hand detail panel. The Glossary tile has a three-column layout (glossary list → categories/terms → term detail); all other tiles have a two-panel layout (item list → item detail).

**Left-hand panel (all asset tiles):**
- Search box to filter the displayed elements
- Type filter dropdown when multiple `deployedImplementationType` values are present
- Items are sorted alphabetically by display name (client-side)
- Sub-tabs within a tile (e.g., Data Stores / Data Feeds / Data Sets) are shown as a tab bar above the list

**Right-hand detail panel (all asset tiles):**
- Header: element display name, type badge, Egeria feedback widget
- Qualified name and description
- Properties table (all scalar properties not in the header)
- Classifications with their properties
- Mermaid diagrams: embedded graphs (rendered immediately) + on-demand "Load Context Diagram" / "Load Anchored Graph" buttons
- Relationships: each relationship card shows the relationship type, related element name and type, relationship properties, and a **"View →"** button when the related element's type maps to a known catalog tab
- Egeria comments section

**Cross-navigation (implemented):** The "View →" button in any relationship card navigates the SPA to the appropriate section and tab, auto-fetching the related element's detail. Navigation resolves subtypes via the `superTypeNames` hierarchy (e.g., `SecretsCollection` navigates to the Data Sets tab because it inherits from `DataSet`).

---

## Glossary tile

The Glossary tile uses a three-column layout:

1. **Left column** — glossary list, plus an "All Terms (search)" entry for cross-glossary search
2. **Middle column** — folder tree and terms for the selected glossary; or search results in global search mode
3. **Right column** — term detail, folder detail, or glossary detail

### Glossary detail
Shows the glossary display name, description, language, usage, and a mermaid context diagram button.

### Folder (GlossaryCategory) detail
Shows folder name, type, status, description, and property table.

### Term detail
Shows term display name, abbreviation, summary, examples, usage, status, content status, description (rendered as markdown), classifications (with badges), folder assignments, mermaid diagram, full property table, all relationship types with their related elements, and an Egeria comments section.

**Term cross-navigation:** Related elements in a term's relationship list (e.g., other terms linked via `SynonymRelationship`) show a "View →" button that navigates within the Glossary section. Non-glossary related elements (e.g., `DataAsset` linked via semantic assignment) show "View →" buttons that navigate to the appropriate asset tab.

**Template substitutes:** Template terms are hidden by default. A "Show template substitutes" checkbox is available in the filter bar.

### Backend
All glossary calls are served by `glossary_handler.py` (shared with Egeria Explorer):
- `GET /api/glossary` → list of glossaries
- `GET /api/glossary/{guid}/folders` → categories for a glossary or category
- `GET /api/glossary/{guid}/terms` → terms for a glossary or category
- `GET /api/glossary-terms?q=` → cross-glossary term search
- `GET /api/glossary/term/{guid}` → full term detail (`graph_query_depth=3`)

---

## Infrastructure Assets tile

Three sub-tabs:

### IT Infrastructure tab
- **API:** `AssetMaker.find_infrastructure(search_string, deployment_status_list=[], graph_query_depth=0)`
- **Type:** `ITInfrastructure` and all subtypes (SoftwareServer, Host, VirtualMachine, HostCluster, etc.)
- **Filter:** `deployedImplementationType` (client-side dropdown)
- **Cross-nav:** `SupportedSoftwareCapability` relationships navigate to the Software Capabilities tab

### Software Capabilities tab
- **API:** `AssetMaker.find_software_capabilities(search_string, graph_query_depth=0)`
- **Type:** `SoftwareCapability` and all subtypes (APIManager, DatabaseManager, EventBroker, etc.)
- **Filter:** `deployedImplementationType` (client-side dropdown)
- **Cross-nav:** `SoftwareCapabilityDependency` relationships navigate within this tab; hosting infrastructure relationships navigate to the IT Infrastructure tab

### Endpoints tab
- **API:** `ConnectionMaker.find_endpoints(search_string, output_format="JSON", graph_query_depth=0)`
- **Type:** `Endpoint` (not an Asset subtype — requires `ConnectionMaker`)
- **Detail:** `ConnectionMaker.get_endpoint_by_guid(guid, body={graphQueryDepth:3})` — a fresh `create_egeria_bearer_token()` call is required (passing a reused token causes a 401 in the constructor)
- **Cross-nav:** Connected server/asset relationships navigate to the IT Infrastructure tab

---

## Data Assets tile

Three sub-tabs:

### Data Stores tab
- **API:** `AssetMaker.find_data_assets(search_string, metadata_element_type="DataStore", content_status_list=[], graph_query_depth=0)`
- **Type:** `DataStore` and all subtypes (Database, CSVFile, DataFile, RelationalDatabase, FileFolder, etc.)
- **Filter:** `deployedImplementationType` (client-side)
- **Cross-nav:** `DataSetContent` relationships (key: `supportedDataSets`) navigate to the Data Sets tab

### Data Feeds tab
- **API:** `AssetMaker.find_data_assets(search_string, metadata_element_type="DataFeed", content_status_list=[], graph_query_depth=0)`
- **Type:** `DataFeed` and all subtypes (Topic, KafkaTopic, etc.)
- **Note:** Coco data feeds are primarily Kafka topics

### Data Sets tab
- **API:** `AssetMaker.find_data_assets(search_string, metadata_element_type="DataSet", content_status_list=[], graph_query_depth=0)`
- **Type:** `DataSet` and all subtypes (SecretsCollection, VirtualRelationalTable, etc.)
- **Cross-nav:** `DataSetContent` relationships navigate to the Data Stores tab

---

## APIs tile

Single list (no sub-tabs):

- **API:** `AssetMaker.find_assets(search_string, metadata_element_type="DeployedAPI", graph_query_depth=0)`
- **Type:** `DeployedAPI` (inherits from DeployedSoftwareComponent → Process → Asset)
- **Filter:** `deployedImplementationType` (client-side)
- **Cross-nav:** `APIEndpoint` relationships navigate to the Endpoints tab

---

## Processes tile

Three sub-tabs:

### Software Components tab
- **API:** `AssetMaker.find_processes(search_string, metadata_element_type="DeployedSoftwareComponent", activity_status_list=[], graph_query_depth=0)`
- **Type:** `DeployedSoftwareComponent` and subtypes
- **Note:** `activity_status_list` defaults to `["IN_PROGRESS"]` — must pass `[]` to see all connectors in Coco

### Actions tab
- **API:** `AssetMaker.find_processes(search_string, metadata_element_type="Action", activity_status_list=[], graph_query_depth=0)`
- **Type:** `Action` and subtypes

### Governance Processes tab
Reusable `GovernanceActionProcess` *definitions* (type 0462), not the same thing as the Actions tab's runtime `Action`/`EngineAction` instances. This tab is a `custom: true` entry in `SECTION_TABS.processes` (own `GovernanceProcessesView`/`GovernanceProcessDetail` components), not a generic `AssetTabView`, because process structure (steps, guarded flow links, request/action targets) isn't representable in the generic Asset graph model.

- **List API:** `GovernanceOfficer.find_governance_definitions(search_string, metadata_element_type="GovernanceActionProcess", graph_query_depth=0)`
- **Detail API:** `GovernanceOfficer.get_governance_process_graph(guid)` — returns `{governanceActionProcess, firstProcessStep, nextProcessSteps, processStepLinks, governanceActionProcessMermaidGraph}`. `_serialize_governance_process_detail()` flattens this into `{steps[], stepLinks[], specification, governanceActionProcessMermaidGraph}`, reusing `_extract_survey_spec()` (previously TechnologyType-only) for the `producedGuards`/`supportedActionTargets`/`producedActionTargets`/`parameters` tables.
- **Type:** `GovernanceActionProcess` (not a subtype of `Asset` — hence its own detail path instead of `AssetCatalog.get_asset_graph_by_guid`)
- **Cross-nav:** `TYPE_TO_NAV['GovernanceActionProcess']` routes here (not to Egeria Explorer's Governance tab, despite `GovernanceActionProcess` inheriting from `GovernanceDefinition`) — the exact-typeName entry takes priority over the `GovernanceDefinition` supertype fallback.

---

## Backend API surface (`tech_catalog_handler.py`)

```
GET /api/tech-catalog/infrastructure          find_infrastructure (ITInfrastructure)
GET /api/tech-catalog/software-capabilities   find_software_capabilities
GET /api/tech-catalog/endpoints               ConnectionMaker.find_endpoints
GET /api/tech-catalog/data-stores             find_data_assets (DataStore)
GET /api/tech-catalog/data-feeds              find_data_assets (DataFeed)
GET /api/tech-catalog/data-sets               find_data_assets (DataSet)
GET /api/tech-catalog/apis                    find_assets (DeployedAPI)
GET /api/tech-catalog/software-components     find_processes (DeployedSoftwareComponent)
GET /api/tech-catalog/actions                 find_processes (Action)
GET /api/tech-catalog/governance-processes    GovernanceOfficer.find_governance_definitions (GovernanceActionProcess)
GET /api/tech-catalog/governance-processes/{guid}  GovernanceOfficer.get_governance_process_graph
GET /api/tech-catalog/assets/{guid}           detail for any element by GUID + section hint
```

All list endpoints accept: `q` (search string), `start_from`, `page_size`, `url`, `server`, `user_id`, `user_pwd`.

Glossary endpoints are served by `glossary_handler.py` (shared with Egeria Explorer).

---

## Design Notes

*Initial design: 2026-06-06. Updated to reflect implementation: 2026-06-08.*

### Key design decisions

**1. Standalone SPA, not an extension of Egeria Explorer.**
`type-explorer.html` is already ~7,600 lines. A separate `tech-catalog.html` keeps concerns clean. The two tools share the same visual language (dark theme, CSS variables, sidebar+detail layout) but are independently deployable.

**2. Glossary is shared with Egeria Explorer.**
`glossary_handler.py` is used by both SPAs without modification. The `GlossaryView` component was ported from `type-explorer.html` with inline styles replacing CSS class dependencies and `creds` prop replacing `CredContext`. When MOD-1 extracts shared components, GlossaryView is the top candidate.

**3. Hash-based section routing.**
`window.location.hash` enables deep-linking from portal cards and bookmarks (e.g., `/tech-catalog#glossary`). Valid section IDs: `glossary`, `infrastructure`, `data-assets`, `apis`, `processes`.

**4. `deployedImplementationType` filtering is client-side.**
pyegeria `find_*` calls don't expose `deployedImplementationType` as a server-side filter. The sidebar shows a type-grouping dropdown that filters the already-loaded list.

**5. Status filters must always be overridden to `[]`.**
Every find method defaults to a status that filters out most Coco demo data. The rule: always pass `<status_param>=[]` unless the user explicitly requests filtering. See `cat_calls.md` for the per-method defaults.

**6. Detail panel uses `graph_query_depth=3`.**
List calls use `graph_query_depth=0` for performance. Detail calls use `graph_query_depth=3` to expose nested schema links, lineage anchors, multi-hop relationships, and embedded mermaid diagram fields.

**7. Relationship data is nested in `relatedElement`.**
pyegeria wraps related elements in `RelatedMetadataElementSummary`. The actual `elementHeader` and `properties` are inside a `relatedElement` sub-dict, not at the item top level. `_extract_relationships()` unwraps this and also extracts `superTypeNames` for subtype-aware navigation.

**8. Cross-navigation uses a `navTarget` state threaded from App to leaf components.**
`App` holds `{ navTarget, handleNavigate }`. `SectionView` switches sub-tabs via `useEffect` on `navTarget`. `AssetTabView` detects a new nav target via `useRef` deduplication and calls `handleSelect` directly. This avoids a global store while keeping the component tree clean.

---

## Implementation status (as of 2026-06-08)

| Phase | Items | Status |
|---|---|---|
| TC-0 | Scaffolding (SPA shell, handler stub, Apache proxy, portal tile) | ✅ Complete |
| TC-1 | All list + detail backend endpoints | ✅ Complete |
| TC-2 | SPA shell + auth seam + splash screen | ✅ Complete |
| TC-3 | Infrastructure section (3 sub-tabs) | ✅ Complete |
| TC-4 | Data Assets section (3 sub-tabs) | ✅ Complete |
| TC-5 | APIs section | ✅ Complete |
| TC-6 | Processes section (3 sub-tabs incl. Governance Processes, added 2026-07-07) | ✅ Complete |
| TC-7 | Glossary tile (3-column browser, full term detail) | ✅ Complete |
| TC-8 | Cross-navigation links via "View →" in relationship cards | ✅ Complete |
| MOD-1→3 | Extract shared components to `egeria-shared-ui.js` | 🔲 Post-MVP |

### Outstanding work

See `CATALOG_ISSUES.md` for detailed tracking. Remaining open issues:
- **O-1/O-2:** Confirm list response key format and whether result-set mermaid graphs are returned
- **O-3:** Pre-populate "Load Context Diagram" from embedded `mermaidGraph` to avoid redundant fetch
- **O-8:** Replace O(n) scan for SoftwareCapability detail with `get_software_capability_by_guid`
- **O-9:** Forward user credentials to mermaid diagram fetch URLs
- **O-10:** Confirm whether `DeployedAPI` elements in Coco have mermaid graph data

### Modularization strategy

Both Explorer and The Catalog share: `MermaidDiagram`, `DiagramPanel`, `MermaidSection`, `AvailableMermaidDiagrams`, `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, the auth seam, and `GlossaryView`. The target for MOD-1 is an `egeria-shared-ui.js` static file served by FastAPI and imported by both SPAs. The Glossary backend (`glossary_handler.py`) is already shared at the API level.
