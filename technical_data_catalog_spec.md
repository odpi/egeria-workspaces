# Technical Asset Catalog — Specification

The **Technical Catalog** is a new tile on the portals for quickstart and freshstart. It is aimed at technical users that are used to working with assets.

When you launch the **Technical Catalog**, there are 4 tiles:

- Infrastructure Assets — For working with servers, storage and networks.
- Data Assets — For working with your data stores, data feeds and data sets.
- APIs — For working with your APIs
- Processes — For working with your software processes and actions

---

## General features for each tile/tab

When a tile is selected, it opens up a page with two panels. A left-hand panel for a tree-view of elements and a right-hand detail panel.

The left-hand tree view under each tile should include a search box to restrict the elements listed. The elements displayed are of a specific type (detailed in the description of each tile). They are organized alphabetically unless the description of the tile specifies otherwise.

When an element in the left-hand pane is selected, the details pane is populated.
On the detail pane, the properties of the element are displayed with a link to display each mermaid graph, along with any classifications and relationships (like egeria explorer).

For each classification displayed, it should be possible to see the properties of the classification.

For each relationship displayed, it should be possible to see the properties of the relationship and the related element.

---

## Under the Infrastructure Assets tile

In the left-hand tree-view, there are 3 tabs:

1. Infrastructure Assets
2. Software Capabilities
3. Endpoints

### Infrastructure Assets tab

The infrastructure assets are accessed using the Asset Maker API. They inherit from ITInfrastructure (metadataElementTypeName="ITInfrastructure").
They should be organized by type. It should be possible to filter by deployedImplementationType and deploymentStatus attributes.

When an asset is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the asset and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related software capabilities (getCapabilities) from the software capabilities tab would be good.

### Software Capabilities tab

The software capabilities are accessed using the Asset Maker API. They inherit from SoftwareCapability and have their own methods.
They should be organized by type. It should be possible to filter by the deployedImplementationType and deploymentStatus attributes.

When a software capability is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the software capability and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related infrastructure asset (getHostedByDeployedITInfrastructure) from the infrastructure assets tab would be good.

### Endpoints tab

The endpoints are accessed using the Connection Maker API. They inherit from Endpoint and there are specialized methods for working with endpoints.
They should be organized by display name.

When an endpoint is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the endpoint and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related infrastructure asset (getServers) from the infrastructure assets tab would be good.

---

## Under the Data Assets tile

In the left-hand tree-view, there are 3 tabs:

1. Data Stores
2. Data Feeds
3. Data Sets

### Data Stores tab

The data stores are accessed using the Asset Maker API. They inherit from DataStore (metadataElementTypeName="DataStore").
They should be organized by type. It should be possible to filter by the deployedImplementationType attribute.

When a data store is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the data store and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related data sets (getSupportedDataSets) from the data sets tab would be good.

### Data Feeds tab

The data feeds are accessed using the Asset Maker API. They inherit from DataFeed (metadataElementTypeName="DataFeed").
They should be organized by type. It should be possible to filter by the deployedImplementationType attribute.

When a data feed is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the data feed and its mermaid graphs, along with any classifications and relationships (like egeria explorer).

### Data Sets tab

The data sets are accessed using the Asset Maker API. They inherit from DataSet (metadataElementTypeName="DataSet").
They should be organized by type. It should be possible to filter by the deployedImplementationType attribute.

When a data set is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the data set and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related data stores (getDataContent) from the data stores tab would be good.

---

## Under the APIs tile

The APIs are accessed using the Asset Maker API. They inherit from DeployedAPI (metadataElementTypeName="DeployedAPI").
They should be organized by type. It should be possible to filter by the deployedImplementationType attribute.

When an API is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the API and its mermaid graphs, along with any classifications and relationships (like egeria explorer). If possible, linking to the related endpoints (getEndpoints) from the endpoints tab would be good.

---

## Under the Processes tile

In the left-hand tree-view, there are 2 tabs:

1. Software Components
2. Actions

### Software Components tab

The software components are accessed using the Asset Maker API. They inherit from DeployedSoftwareComponent (metadataElementTypeName="DeployedSoftwareComponent").
They should be organized by type. It should be possible to filter by the deployedImplementationType and activityStatus attributes.

When a software component is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the software component and its mermaid graphs, along with any classifications and relationships (like egeria explorer).

### Actions tab

The actions are accessed using the Asset Maker API. They inherit from Action (metadataElementTypeName="Action").
They should be organized by type. It should be possible to filter by the deployedImplementationType and activityStatus attributes.

When an action is selected, the detail panel is displayed.
In this initial implementation it is sufficient to display the properties of the action and its mermaid graphs, along with any classifications and relationships (like egeria explorer).

---

## Design Notes and Implementation Plan

*Added 2026-06-06.*

### Key design decisions

**1. Standalone SPA, not an extension of Egeria Explorer.**

`type-explorer.html` is already ~7,600 lines. Adding 9 more asset-type panels there would make it unmaintainable and slow to load. A separate `tech-catalog.html` (~2,500–3,000 lines estimated) keeps concerns clean and makes modularization tractable later. The two tools share the same visual language (dark theme, CSS variables, sidebar+detail layout) but are independently deployable.

**2. Same URL-routing model as Explorer.**

The tool lives at `/tech-catalog` (served by the existing Apache proxy → FastAPI). Deep-linking via `window.location.hash` is supported from launch, so portal cards and bookmarks can land directly on a section (e.g., `/tech-catalog#data-stores`). This follows the hash-navigation pattern already in place for Explorer.

**3. Single backend handler file: `tech_catalog_handler.py`.**

All nine asset-type endpoints live in one file. The handler uses `AssetMaker` (from pyegeria) for infrastructure, data assets, APIs, software components, and actions; and `ConnectionMaker` for endpoints. All calls pass `sequencing_order="PROPERTY_ASCENDING"` and `sequencing_property="displayName"` — the established pattern across all existing handlers.

**4. `deployedImplementationType` filtering is client-side in Phase 1.**

The pyegeria `find_*` calls do not expose `deployedImplementationType` as a direct server-side filter parameter — it is a property on the returned element. In Phase 1 the sidebar will show a type-grouping dropdown that filters the already-loaded list client-side. Phase 2 can add a `property_names` body parameter if Egeria adds support.

**5. Status filters use the pyegeria-native params.**

- `find_infrastructure` → `deployment_status_list` (default `["ACTIVE"]`)
- `find_data_assets` → `content_status_list` (default `["ACTIVE"]`)
- `find_processes` → `activity_status_list`
- `find_software_capabilities` → no status filter; client-side grouping by type

**6. Detail panel reuses the same component patterns as Explorer.**

`AvailableMermaidDiagrams`, `MermaidSection`, `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, and the property-table layout are copy-initialised from Explorer. When the Modularization workstream (MOD-1→3) runs, these will be extracted to a shared static include so changes propagate automatically. Building the catalog first gives us concrete evidence of which components are truly shared.

**7. Port allocation.**

The Technical Catalog is served by the existing `quickstart-pyegeria-web` FastAPI container via a new Apache `<Location /tech-catalog>` proxy block — same pattern as `/egeria-explorer`. No new container or host port is required.

---

### pyegeria API mapping

| Section / Tab | pyegeria class | Method | `metadata_element_type` |
|---|---|---|---|
| Infrastructure Assets | `AssetMaker` | `find_infrastructure` | `"ITInfrastructure"` |
| Software Capabilities | `AssetMaker` | `find_software_capabilities` | *(all, filter client-side)* |
| Endpoints | `ConnectionMaker` | `find_endpoints` | *(body-based search)* |
| Data Stores | `AssetMaker` | `find_data_assets` | `"DataStore"` |
| Data Feeds | `AssetMaker` | `find_data_assets` | `"DataFeed"` |
| Data Sets | `AssetMaker` | `find_data_assets` | `"DataSet"` |
| APIs | `AssetMaker` | `find_assets` | `"DeployedAPI"` |
| Software Components | `AssetMaker` | `find_processes` | `"DeployedSoftwareComponent"` |
| Actions | `AssetMaker` | `find_processes` | `"Action"` |

Detail panel (any type): `AssetMaker.get_asset_by_guid()` or `find_assets` with GUID filter. Mermaid: existing `/api/mermaid/{guid}` endpoint already works for any Egeria element.

---

### Backend API endpoints (`tech_catalog_handler.py`)

```
GET /api/tech-catalog/infrastructure          find_infrastructure(type=ITInfrastructure)
GET /api/tech-catalog/software-capabilities   find_software_capabilities()
GET /api/tech-catalog/endpoints               find_endpoints() via ConnectionMaker
GET /api/tech-catalog/data-stores             find_data_assets(type=DataStore)
GET /api/tech-catalog/data-feeds              find_data_assets(type=DataFeed)
GET /api/tech-catalog/data-sets               find_data_assets(type=DataSet)
GET /api/tech-catalog/apis                    find_assets(type=DeployedAPI)
GET /api/tech-catalog/software-components     find_processes(type=DeployedSoftwareComponent)
GET /api/tech-catalog/actions                 find_processes(type=Action)
GET /api/tech-catalog/assets/{guid}           get detail for any element by GUID
```

All list endpoints accept `q` (search string), `start_from`, `page_size`, and credential query params (`url`, `server`, `user_id`, `user_pwd`) — same FastAPI query-param pattern as all other handlers.

---

### Phased implementation plan

#### Phase 0 — Scaffolding (TC-0) — *start here*

- Create `tech-catalog.html` skeleton (HTML boilerplate, React/CDN imports, empty `App` component)
- Create `tech_catalog_handler.py` with one stub endpoint (`/api/tech-catalog/ping`)
- Register handler in `pyegeria_handler.py` (both quickstart + freshstart)
- Add Apache `<Location /tech-catalog>` proxy block to `fastapi-proxy.conf` (both envs)
- Add portal tile "Technical Catalog" to `demo-portal.html` (both portals)
- Confirm the tile renders and the page loads

#### Phase 1 — Full backend (TC-1)

- Implement all 9 list endpoints + the `/{guid}` detail endpoint
- Wire in `sequencing_order` / `sequencing_property` on every call
- Return consistent JSON shape: `{ items: [...], total: N }` with serialized element objects (guid, displayName, qualifiedName, typeName, deployedImplementationType, description, classifications, properties)
- Manual smoke-test each endpoint against live Egeria

#### Phase 2 — SPA shell + Infrastructure section (TC-2, TC-3)

- App shell: auth seam (reads `/api/auth/me`, gates connection form on `srvManaged`), hash-based section routing, top-level 4-tile splash screen
- Infrastructure section: 3 sub-tabs (Assets / Capabilities / Endpoints), sidebar with search + type-group filter, detail panel with property table + mermaid buttons + feedback widgets

#### Phase 3 — Data Assets section (TC-4)

- 3 sub-tabs: Data Stores / Data Feeds / Data Sets
- Same sidebar + detail pattern as Phase 2; add `deployedImplementationType` filter dropdown

#### Phase 4 — APIs and Processes sections (TC-5, TC-6)

- APIs: single list + detail (no sub-tabs needed)
- Processes: 2 sub-tabs (Software Components / Actions)

#### Phase 5 — Cross-navigation links (TC-8)

- Infrastructure Asset detail → "View Software Capabilities" link that switches sub-tab and pre-selects
- Software Capability detail → linked Infrastructure Asset
- Endpoint detail → linked server/asset
- Data Store detail → linked Data Sets

#### Phase 6 (post-MVP) — Modularization (MOD-1→3)

After both Explorer and Tech Catalog are stable, extract the genuinely shared components:
- `MermaidDiagram`, `DiagramPanel`, `MermaidSection`, `AvailableMermaidDiagrams`
- `EgeriaFeedbackWidget`, `EgeriaCommentsSection`
- Property table renderer
- Auth seam helpers

Target: a `egeria-shared-ui.js` static file served by FastAPI, imported by both SPAs via `<script>` tag. Both files become ~30% shorter and changes to shared components propagate automatically.

---

### Modularization strategy (item #1)

The immediate risk of copy-paste duplication is real — the Mermaid + feedback components are ~350 lines of the Explorer, and the auth seam is ~80 lines. If we change them in one tool and forget the other, they drift.

**Short-term mitigation (now):** When building Tech Catalog, copy the components verbatim from Explorer. Add a `// SHARED — keep in sync with type-explorer.html` comment on each block so drift is visible in code review.

**Medium-term fix (MOD phase):** Once both tools exist and usage patterns are clear, extract to a shared module. The extraction boundary will be obvious from the `// SHARED` markers.

**What NOT to share:** Auth portal HTML, connection forms, persona picker, section routing — these differ enough between tools that sharing would create coupling without benefit.

The Glossary panel is the first candidate for reuse across tools (Explorer → future Data Catalog). Its backend is already a standalone handler (`glossary_handler.py`). The frontend `GlossaryView` component in Explorer (~400 lines) can be extracted to `egeria-shared-ui.js` and embedded in other tools with minimal adaptation — the only coupling is the `onNavigate*` callback props, which the host tool provides.
