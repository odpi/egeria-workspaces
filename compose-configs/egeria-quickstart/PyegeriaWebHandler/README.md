<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Pyegeria Web Handler
The Pyegeria Web Handler is a python module that provides a web handler for the pyegeria command line interface. It is
used to execute Dr.Egeria commands from anything that can make a REST call - and that shares the same filesystem as
the Egeria runtime.

## Maintenance Notes
The Pyegeria Web Handler now uses the **Dr. Egeria v2** core, which features a dynamic registry-based dispatcher (`V2Dispatcher`).

### Dynamic Discovery
Unlike previous versions, you no longer need to manually update `dr_egeria_md.py` with `if-elif` blocks when new commands are added to `pyegeria`. The handler now:
1.  **Auto-Registers**: Scans command specifications (JSON) in `md_processing/data/compact_commands` and automatically maps them to their respective processors.
2.  **Supports Variants**: Handles "Link", "Attach", "Add", "Detach", "Remove", etc., automatically based on the command specs.
3.  **Hot Reload**: You can trigger a refresh of the command specifications (without restarting the container) via the `/dr-egeria/refresh` POST endpoint or the "Refresh" button in the Obsidian plugin.

### Diagnostics
The v2 engine provides rich feedback tables ("Command Analysis" and "Parsed Attributes"). If the Obsidian plugin detects a long response, it will display these diagnostics in a modal window to help troubleshoot markdown formatting or missing requirements.

### Path Handling
The Dr. Egeria engine and the Obsidian plugin work together to ensure that input paths are correctly resolved, even in "Content-First" mode:
- The Obsidian plugin allows configuring a **Vault Root** (the path inside the container) and an **Input Path** (the subfolder in the vault).
- These are combined with the note name to create a logical `input_file` path sent to the backend.
- The MCP server uses this logical path for context (like naming output files) but processes the actual markdown content from a temporary file created in the container's inbox. 
- This ensures that notes can be processed even if the Obsidian vault is not mounted into the Docker container.

### Generalized MCP
The included `mcp_server.py` now supports dynamic execution. You can use the `egeria_execute_command` tool to run any Dr. Egeria command by name, and `egeria_list_commands` to see what is currently available.

## Model Context Protocol (MCP) Support

### Overview
The PyegeriaWebHandler includes a built-in MCP (Model Context Protocol) server that exposes Dr. Egeria capabilities through the MCP standard. This allows AI assistants like Claude to interact with your Egeria metadata ecosystem through a standardized protocol.

### MCP Protocol Support
The PyegeriaWebHandler uses the **Model Context Protocol (MCP)** standard via the `mcp` Python library. The implementation is highly flexible, supporting:
- **Transport Protocols**: 
  - **SSE (over HTTP)**: Used by the "Calling the Dr." Obsidian plugin (port 8000/sse).
  - **stdio**: Used by local command-line tools and Claude Desktop.
- **Server Framework**: `FastMCP` from the `mcp` library for simplified server implementation.
- **Content-First Architecture**: In SSE mode, the server returns the generated Markdown content directly to the client, which then handles the file writing. This eliminates permission issues and path-mapping complexity.
- **Tool-Based Interface**: All Dr. Egeria commands are exposed as MCP "tools" that can be discovered and called by any MCP client.

### Configuration

#### Option 1: Using the Docker Container
The MCP server runs automatically inside the `pyegeria-web` container when started. However, the primary entry point in the container is the FastAPI server (port 8000), which is the web-based handler for Dr. Egeria commands.

To access the MCP server directly from the container, you would need to:
1. Connect to the container
2. Execute the `mcp_server.py` script directly (this is useful for MCP-based clients)

#### Option 2: Local Development / Direct Access
If you want to run the MCP server locally on your machine (e.g., for Claude Desktop integration):

**Environment Variables:**
```bash
export EGERIA_USER="erinoverview"
export EGERIA_USER_PASSWORD="secret"
export EGERIA_ROOT_PATH="/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/exchange-quickstart"
export EGERIA_INBOX_PATH="loading-bay/dr-egeria-inbox"
export EGERIA_OUTBOX_PATH="distribution-hub/dr-egeria-outbox"
export PYEGERIA_LOG_DIRECTORY="/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-quickstart/PyegeriaWebHandler/logs"
```

If you launch `mcp_server.py` from within this workspace and do not set these values explicitly, the server will now auto-detect the quickstart exchange tree and use a writable local log directory.

**Running the MCP Server:**
```bash
python mcp_server.py
```

#### Option 3: Claude Desktop Integration
To integrate with Claude Desktop, configure your `claude_desktop_config.json`.
The key under `mcpServers` is a client-side alias, not a protocol-mandated server name. For the Dr. Egeria MCP server, use a distinct alias such as `dr-egeria` so it can coexist with the separate `pyegeria` MCP server in the same config:

```json
{
  "mcpServers": {
    "dr-egeria": {
      "command": "/path/to/python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "EGERIA_USER": "erinoverview",
        "EGERIA_USER_PASSWORD": "secret",
        "EGERIA_VIEW_SERVER": "qs-view-server",
        "EGERIA_VIEW_SERVER_URL": "https://localhost:9443",
        "EGERIA_ROOT_PATH": "/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/exchange-quickstart",
        "EGERIA_INBOX_PATH": "loading-bay/dr-egeria-inbox",
        "EGERIA_OUTBOX_PATH": "distribution-hub/dr-egeria-outbox",
        "PYEGERIA_LOG_DIRECTORY": "/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-quickstart/PyegeriaWebHandler/logs"
      }
    }
  }
}
```

### Available MCP Tools

The MCP server exposes the following tools:

- **`dr_egeria_run_block`** (Main Tool - Direct Dr. Egeria Commands)
   - Execute any Dr. Egeria markdown command block. 
   - **Content-First Processing**: The server saves the `markdown_block` to a temporary file in the container, allowing it to process content from remote clients (like Obsidian) without requiring local file access.
   - **Output Note**: In SSE mode, this tool returns the generated Markdown as a string.
   - Parameters:
     - `markdown_block`: Markdown content with H1 command blocks
     - `url`: Egeria platform URL (e.g., `https://host.docker.internal:9443`)
     - `server_name`: Egeria view server name (e.g., `qs-view-server`)
     - `user_id`: Egeria user ID
     - `user_pass`: Egeria user password
     - `directive`: `display`, `validate`, or `process` (default: `process`)

2. **`egeria_execute_command`** (Convenience Wrapper)
   - Execute any Dr. Egeria command by name instead of writing markdown
   - Parameters: `command_name`, `attributes`, `url`, `server_name`, `user_id`, `user_pass`, `directive`
   - This is a wrapper around `dr_egeria_run_block` that constructs the markdown for you

3. **`egeria_list_commands`** (Discovery Tool)
   - List all available Dr. Egeria commands
   - Parameters: none
   - Shows the 108+ available commands (Create, Link, View, Attach, etc.)

4. **`egeria_refresh_specs`** (Maintenance Tool)
   - Refresh command specifications from JSON files
   - Parameters: none
   - Useful when new commands are added without restarting the server

5. **`egeria_list_glossaries`** & **`egeria_list_collections`** (Convenience Shortcuts)
   - Quick access to common Egeria operations
   - Parameters: `url`, `server_name`, `user_id`, `user_pass`
   - **Important**: These ARE convenience shortcuts, NOT standalone Dr. Egeria commands. They require the same connection parameters as `dr_egeria_run_block` because they call it internally with a "View Glossaries" or "View Collections" markdown block.

#### Understanding the Tool Types

**Dr. Egeria Commands** (108+ available via `egeria_execute_command` or `dr_egeria_run_block`):
- Create Glossary, Create Glossary Term, Create Collection, Create Data Class, Create Governance Policy, etc.
- Link Term To Data Field, Link Data to Governance, etc.
- View Report, Set Glossary as Taxonomy, Attach Data Value Specification, etc.

**MCP Tool Wrappers** (provided by the server for convenience):
- `egeria_list_glossaries` — calls `dr_egeria_run_block` with "View Glossaries" command
- `egeria_list_collections` — calls `dr_egeria_run_block` with "View Collections" command
- `egeria_execute_command` — constructs markdown and calls `dr_egeria_run_block`

**Why the convenience wrappers might fail**:
- They still require connection parameters (`url`, `server_name`, `user_id`, `user_pass`)
- If Claude doesn't pass these parameters, the tool call will fail
- You need to tell Claude: "List glossaries from our Egeria instance at https://localhost:9443 with server qs-view-server"

### Does MCP Support Interfere with Pyegeria's MCP Server?

**Short Answer: No, there is no interference.**

**Detailed Explanation:**
- The `mcpServers` entry name is just a unique alias in the client config. It does not need to match the Python module name or the internal `FastMCP(...)` server name.
- The PyegeriaWebHandler's MCP server (`mcp_server.py`) is a **separate, independent process** from the FastAPI web server
- The pyegeria package may have its own MCP server implementation, but they operate in completely different contexts:
  - **PyegeriaWebHandler MCP**: Designed to expose Dr. Egeria markdown commands through MCP to external MCP clients (like Claude Desktop)
  - **Pyegeria Package MCP** (if present): Likely designed for a different use case or integration pattern
- Both can coexist and run simultaneously without conflicts
- A practical convention is to keep the pyegeria package server as `pyegeria` and name this server `dr-egeria`.
- The PyegeriaWebHandler's MCP server communicates directly with the filesystem (reading from `dr-egeria-inbox`, writing to `dr-egeria-outbox`) and the Egeria platform via REST APIs
- No shared resources or port conflicts occur if they are run in separate processes

### Use Cases

1. **AI-Assisted Metadata Management**: Use Claude Desktop with the MCP integration to manage your Egeria metadata through conversational AI
2. **Automated Governance Workflows**: Script MCP tool calls to automate metadata governance operations
3. **Integration with Other Tools**: Connect any MCP-compatible tool to your Egeria ecosystem
4. **Local Development**: Test Dr. Egeria commands locally before deploying to Docker

## Examples

### Using the Dr. Egeria MCP Server in Claude Desktop

Once you've configured the `dr-egeria` server in Claude Desktop, you can ask Claude to perform Dr. Egeria operations directly:

**Example conversation:**
```
User: "Create a glossary called 'Data Dictionary' in our Egeria instance"

Claude: I'll create a glossary for you using the Dr. Egeria MCP server.
[Claude calls dr_egeria_run_block with the command]

Output: Glossary 'Data Dictionary' created successfully with ID: glossary-12345
```

**Behind the scenes**, Claude uses the `dr_egeria_run_block` tool with:
- A markdown block containing: `# Create Glossary\n## Glossary Name\nData Dictionary`
- Your platform URL and view server
- Your credentials

### Using the Pyegeria MCP Server in Claude Desktop

The `pyegeria` server provides direct access to the Python pyegeria library:

**Example conversation:**
```
User: "List all metadata stores in our Egeria instance"

Claude: I'll query the available metadata stores using the pyegeria MCP server.
[Claude calls appropriate pyegeria tool]

Output: Available metadata stores:
- qs-metadata-store (primary)
- qs-archive-store (archive)
```

### Comparison: When to Use Each Server

| Task | Dr. Egeria MCP | Pyegeria MCP |
|------|---|---|
| Create/Update metadata via markdown commands | ✓ | - |
| View glossaries and collections | ✓ | ✓ |
| Advanced metadata queries | - | ✓ |
| Governance workflows | ✓ | ✓ |
| Integration with AI assistants | ✓ | ✓ |

### Example: Multi-Step Workflow

Using both servers together in a single Claude conversation:

```
User: "Create a new glossary called 'Financial Terms' and then show me all 
       the glossaries currently defined"

Claude: I'll do this in two steps.

Step 1: Create the glossary using Dr. Egeria commands
[calls dr_egeria_run_block]
→ Created glossary 'Financial Terms'

Step 2: List all glossaries using Dr. Egeria
[calls egeria_list_glossaries]
→ Available glossaries:
  - Data Dictionary (glossary-12345)
  - Financial Terms (glossary-12346)
  - Business Concepts (glossary-12347)
```

### Calling Convenience Tools Correctly

The convenience tools (`egeria_list_glossaries`, `egeria_list_collections`, etc.) require connection parameters. Here's the correct way to ask Claude to use them:

**Example - Listing glossaries:**
```
User: "List all the glossaries in our Egeria instance at https://localhost:9443 
       using the Dr. Egeria MCP server with server name qs-view-server"

Claude: I'll list the glossaries using the egeria_list_glossaries tool.
[Calls egeria_list_glossaries with url, server_name, user_id, user_pass]

Output: Available glossaries:
• Data Assets (id: glossary-001)
• Product Catalog (id: glossary-002)
• Business Concepts (id: glossary-003)
```

**Why this matters**: The convenience tools are wrappers around `dr_egeria_run_block`. They need your connection details to work:
- `url`: Your Egeria platform URL
- `server_name`: Your view server name (e.g., `qs-view-server`)
- `user_id`: Your Egeria username
- `user_pass`: Your Egeria password

## Egeria Explorer

The PyegeriaWebHandler includes a built-in **Egeria Explorer** — an interactive browser for the live Egeria metadata ecosystem. It presents six sections in a single-page application, all read-only, all backed by live Egeria API calls.

### Accessing the Explorer

Once the stack is running, open a browser and navigate to:

```
http://localhost:8085/egeria-explorer
```

The alias `/type-explorer` is also supported and serves the same application:

```
http://localhost:8085/type-explorer
```

Apache proxies both URLs through to the `pyegeria-web` container, which serves the single-page application and its backing API.

### Sections

The explorer opens to a **Home** splash screen on first load. Eight tabs run across the top, ordered left to right: **⌂ Home → Type Explorer → Glossary → Reference Data → Digital Products → Report Specs → Valid Values → REST APIs**. Each tab is independent; data is loaded lazily when the tab is first opened. All sections are read-only.

#### Home (Splash Screen)

The initial view shown when the application loads. It presents a one-paragraph description of the tool and a card for each of the seven capabilities. Each card shows an icon, title, and short description of what that section does. Clicking **Open →** on any card navigates directly to that section. The **⌂ Home** tab in the header returns to this screen from any section.

No Egeria connection or data fetch is required to display the splash screen.

#### Type System

Browses the Egeria open metadata type system fetched live from `ValidMetadataManager`.

Two sub-views:

**Type Explorer** — Left sidebar with three collapsible sections (Entity Types, Classifications, Relationships). A search box filters all three simultaneously. The right panel shows:
- **Properties tab** — all own and inherited properties, with `own`/`req`/`deprecated` badges and a toggle to hide inherited properties.
- **Relationships tab** — every relationship the type participates in, derived by walking the full supertype chain.
- **Graph tab** — SVG inheritance diagram showing ancestors above and direct subtypes below. Nodes are clickable to navigate.

A dropdown in the header filters entity types to a specific area (0 = Foundation through 7 = Lineage). Relationship and classification types are always shown in full regardless of the area filter.

**Attribute Index** — Searchable cross-reference of every property name to every type that declares it. Useful for answering "which types have a `description` field?" Clicking a type name navigates to it in the Type Explorer.

#### Reference Data

Browses Egeria's valid value sets and values. Displays as an expandable tree: root-level `ValidValueSet` (and `ReferenceDataSet`) nodes expand to show their member values and any nested child sets.

- Click a set to see its description, qualified name, and usage.
- Click a value to see its preferred value, category, data type, scope, and deprecation status.
- The filter box narrows visible tree nodes by display name.
- Click the **▦ Load Context Diagram** button to fetch and render a Mermaid context diagram for any selected element.

#### Digital Products

Browses the digital product catalog hierarchy: Catalogs → Families → Products. Each level is a `Collection` subtype in Egeria.

- Select a catalog from the left panel to load its full tree.
- The tree uses expand/collapse twisties. Containers are sorted above leaf products.
- The detail panel shows all `DigitalProductProperties` fields (maturity, version, dates, deployment status).
- Glossary-linked products show a **View in Glossary →** button that navigates to the Glossary tab for that element.
- Click **▦ Load Context Diagram** on any element to render its Mermaid context diagram.

#### Glossary

Browses glossaries, folders, and terms.

- Top panel: list of all glossaries.
- When a glossary is selected: its folders and a cross-glossary term search appear.
- Selecting a folder loads its terms in the right panel.
- Term detail shows all term properties (display name, summary, description, examples, usage, abbreviation, content status, activity status) plus folder memberships.
- **Template substitutes** — terms carrying the `TemplateSubstitute` classification are template placeholder entries, not real user-facing terms. They are hidden by default. A checkbox in the middle pane header ("Show template substitutes") reveals them; hidden ones are counted in a "N templates hidden" note. Template substitutes appear in the list with an amber `template` badge; when opened in the detail panel they are labelled **Template Substitute**. Terms copied from a template (but not themselves substitutes) show a lighter **From Template** badge.
- Click **▦ Load Context Diagram** on any term to render its diagram.

#### Report Specs

Browse pyegeria's client-side report format specifications. These are not stored in Egeria — they are Python objects in the pyegeria package describing how API responses can be formatted. No Egeria connection is needed to view this tab.

- Left panel: searchable list of all specs with perspective filter.
- Right panel: name, description, family, perspectives, output formats, and the full question spec.

#### Valid Values

Look up the registered valid values for a specific Egeria property name. Uses Egeria's controlled vocabulary registry (`get_valid_metadata_values`), which is separate from the Reference Data sets.

- Left panel: on tab open, a sidebar is pre-populated with all property names that have registered valid values (via `GET /api/valid-values/properties`). Click a name to look it up, or type any property name directly.
- Right panel: the ordered list of allowed values for the selected property, with display names, preferred values, and descriptions.

#### REST APIs

Browsable reference for the Egeria REST API surface, combining live OpenAPI discovery with a curated request body catalog.

The tab has three panels:

**Left — Service list.** OMAS/OMVS services derived from the OpenAPI spec tags (e.g., "Asset Manager OMAS", "Glossary Manager OMVS"). Click **Load API Endpoints** in the toolbar to fetch the spec from the live Egeria platform. Services are filterable by name.

**Middle — Endpoint list.** All endpoints for the selected service, each showing its HTTP method (color-coded badge), path, and summary. Filterable by path or summary text.

**Right — Detail / Body Catalog** (two inner tabs):

- *Endpoint Detail* — parameters table (path and query), the matched Layer 1 outer body type (click to jump to the Body Catalog), the inferred Layer 2 properties type name, a copyable example JSON payload assembled from the catalog, and a ready-to-run `curl` snippet.
- *Body Catalog* — the full request body catalog, always available without a live Egeria connection. Grouped into functional families (Create Entity, Update Entity, Delete Entity, Relationship, Classification, Search/Query, etc.), with every field annotated and a representative example for each type.

**Two-layer payload model.** Egeria REST request bodies follow a consistent two-layer pattern:

```json
{
  "class": "NewElementRequestBody",      ← Layer 1: outer wrapper (~44 types)
  "externalSourceGUID": "...",
  "parentGUID": "...",
  "properties": {
    "class": "CollectionProperties",     ← Layer 2: type-specific properties
    "qualifiedName": "...",
    "displayName": "..."
  }
}
```

Layer 1 is a small, stable set of wrapper types defined in `egeria_request_body_catalog.json`. Layer 2 is derived from the Egeria type system — for any entity or relationship type, all properties including inherited ones are valid.

**Keeping the catalog current.** After upgrading Egeria, regenerate the catalog with:

```bash
python3 build_request_body_catalog.py /path/to/egeria-platform-X.Y/assembly/opt/http-client-collections
```

Or, if `HTTP_COLLECTIONS_PATH` is set in the environment, use the in-app endpoint:

```
POST http://localhost:8085/api/request-bodies/rebuild
```

The OpenAPI endpoint data always comes from the live platform and is cached for one hour. Force a re-fetch with:

```
POST http://localhost:8085/api/rest-apis/refresh
```

#### Solution Architect

Browses Egeria's solution architecture artefacts — blueprints and solution components.

Two sub-navigations selectable from the left sidebar header:

**Blueprints** — a list of all `SolutionBlueprint` elements. Selecting one loads its detail: display name, description, lifecycle status, qualified name, and the list of components it contains (each component linkable to the Components view). A **▦ Load Context Diagram** button is available for every blueprint.

**Components** — all `SolutionComponent` elements, independently browsable. Detail panel shows component type, version, description, and a list of implementations (linked assets or deployed capabilities). Components link back to the blueprints they belong to. Context diagrams available for each component.

#### Data Design

Browses Egeria's data design artefacts: Data Specs, Data Structures, Data Fields, Data Grains, and Data Classes.

Five sub-navigations in the left sidebar:

- **Specs** — `DataSpec` (a Collection subtype) elements representing named data requirements.
- **Structures** — `DataStructure` elements, groupings of Data Fields.
- **Fields** — `DataField` elements, individual field definitions within a structure.
- **Grains** — `DataGrain` elements, the unit of data in a Data Spec.
- **Classes** — `DataClass` elements, reusable data type classifications.

Each sub-view has a search filter and shows element cards. Selecting an element opens its detail panel with all properties plus linked related elements (e.g., the parent structure for a field, or the data class assigned to a field). Context diagrams are available for all element types.

#### Perspectives

Browses Egeria's governance perspectives — structured viewpoints used to reason about the metadata from specific stakeholder angles.

Two sub-navigations:

**Perspectives** — All `ActorProfile` elements whose type is "Perspective". Each perspective has a description and is linked to a set of Questions via `ScopedBy` relationships. The detail panel shows all linked Questions.

**Questions** — All `GlossaryTerm` elements carrying the `Question` classification. Questions represent governance concerns or decision points. Detail shows the term's summary, description, and linked Perspectives. Uses `GlossaryManager.find_glossary_terms` with `include_only_classified_elements=["Question"]` and `graph_query_depth=2` to ensure classifications are included in the response.

#### Dr. Egeria Commands

Browsable reference for all Dr. Egeria markdown command templates, plus an in-browser execution panel.

**Commands tab** — Three-column layout:

- *Left* — command families grouped by level (Basic / Advanced). Click a family to see its commands in the middle column.
- *Middle* — command list for the selected family, with title, description, and a "Create / Update" or "Link / Unlink" dual-verb badge where applicable.
- *Right* — command detail: full parameter list with required/optional status, a pre-filled markdown template, and an Execute panel.

**Execute panel** — Fills in the markdown template with values entered in the parameter fields. A **Verb** row (shown when a counterpart verb exists) lets you switch between e.g. Create and Update before running. A testing disclaimer reminds users this executes real Egeria writes. Click **Run** to POST to `/api/dr-egeria/execute` and see the result markdown inline.

No Egeria connection is required to browse command templates. Executing a command does require a running Egeria instance and valid credentials in the connection context.

#### Supply Chains

Browses Egeria's Information Supply Chain (ISC) elements.

Left sidebar lists all `InformationSupplyChain` elements with a search filter. Selecting one loads the detail panel: display name, description, scope, lifecycle status, and the full relationship graph including `InformationSupplyChainLink` segments. A **▦ Load Context Diagram** and a **▦ Load Full Graph** button are available.

#### Governance Definitions

Browses Egeria's governance definition hierarchy in a three-panel layout (all panels resizable).

**Left — Definition Types.** Tree organised into three root groups, each expanded by default:

- **Governance Drivers** (`GovernanceDriver`) — the forces that motivate governance: BusinessImperative, GovernanceStrategy, Regulation (→ RegulationArticle), Threat.
- **Governance Policies** (`GovernancePolicy`) — the intent and direction of governance: GovernanceApproach, GovernanceObligation, GovernancePrinciple.
- **Governance Controls** (`GovernanceControl`) — the mechanisms that implement governance:
  - DataLens, DataProcessingPurpose, ExceptionType, GovernanceMetric
  - GovernanceProcedure (→ Methodology), GovernanceResponsibility
  - GovernanceRule (→ NamingStandardRule), NotificationType
  - Requirement, ResearchQuestion
  - SecurityAccessControl (→ GovernanceZone, ServiceAccessControl)
  - TermsAndConditions (→ CertificationType, LicenseType, ServiceLevelObjective)

Abstract types are shown in italic. Selecting any node (abstract or concrete) loads that type's definitions in the middle panel.

**Middle — Definition List.** Definitions of the selected type, sorted alphabetically by display name. A search box filters by name (debounced 400 ms). When a parent/abstract type is selected, results include all subtypes; a small badge shows each item's concrete type. Selecting a definition loads its detail in the right panel.

**Right — Detail.** Mirrors the SolutionComponent detail style:
- Display name + typeName badge
- GUID (monospace)
- Description (Markdown-rendered)
- Mermaid context diagram (if available)
- Properties table: Qualified Name, Identifier, Scope, Usage, Domain, Importance, Status, Summary, Implications, Outcomes, Results
- All relationship groups returned by the API, with **View →** buttons for related governance definitions enabling in-tab navigation.

Uses `GovernanceOfficer.find_governance_definitions` with `metadata_element_type` kwarg for type filtering, and `get_governance_definition_by_guid` for detail.

---

### Context diagrams (all sections)

Every detail panel in every section includes a **▦ Load Context Diagram** button. Clicking it calls `GET /api/mermaid/{guid}`, which uses `MetadataExpert.get_anchored_element_graph()` to fetch the element's Mermaid context graph from Egeria. The diagram is rendered client-side by the Mermaid JS library (v11+). If the diagram is unavailable for an element, a "No context diagram available" message is shown.

Once a diagram is loaded it can be toggled: a **Hide** button collapses it back to a compact "▦ Show Context Diagram" button without re-fetching. Clicking that button expands it again instantly (the diagram code is cached in component state).

Diagrams are loaded on demand, not pre-fetched, to avoid slowing down list and detail views.

---

### REST API reference

All endpoints are accessible directly in addition to being used by the SPA. Connection parameters default to environment variables (`EGERIA_PLATFORM_URL`, `EGERIA_VIEW_SERVER`, `EGERIA_USER`, `EGERIA_USER_PASSWORD`).

#### Type System

**`GET /api/types`** — All entity, relationship, and classification type definitions.

Query params: `area` (int, 0–7), `url`, `server`, `user_id`, `user_pwd`.

```
GET http://localhost:8085/api/types
GET http://localhost:8085/api/types?area=4
```

Response: `{ areaNames, entities, classifications, relationships }`. Each entity includes `guid`, `area`, `abstract`, `supertype`, `desc`, `wiki`, `deprecated`, `props` (own properties only).

#### Reference Data

**`GET /api/reference-data`** — All valid value definitions with parent set relationships.

Query params: `q` (search string), `start_from`, `page_size` (default 200, max 1000).

Response: `{ definitions, sets, values, total }`. Each definition includes `guid`, `typeName`, `isSet`, `displayName`, `qualifiedName`, `description`, `preferredValue`, `category`, `dataType`, `usage`, `scope`, `isDeprecated`, `isCaseSensitive`, `parentSets`.

**`GET /api/reference-data/{vv_guid}`** — Single valid value definition by GUID.

**`GET /api/reference-data/metadata-values`** — Valid values for a specific property name.

Query params: `property_name` (required), `type_name` (optional).

#### Glossary

**`GET /api/glossary`** — All glossaries.

**`GET /api/glossary/{guid}/folders`** — CollectionFolder children of a glossary.

**`GET /api/glossary/{guid}/terms`** — Terms whose `memberOfCollections` includes this GUID. Requires `graph_query_depth=1` internally; results are deduplicated by GUID before return.

**`GET /api/glossary-terms`** — Cross-glossary term search.

Query param: `q` (search string, default `*`).

**`GET /api/glossary/term/{guid}`** — Single term by GUID.

#### Digital Products

**`GET /api/digital-products/catalogs`** — All `DigitalProductCatalog` collections.

**`GET /api/digital-products/catalogs/{guid}/tree`** — Full recursive hierarchy for a catalog. Response: `{ catalog, children }` where each node has `guid`, `typeName`, `displayName`, `isContainer`, `children`.

**`GET /api/digital-products/{guid}`** — Single product/collection node.

#### Context Diagrams

**`GET /api/mermaid/{guid}`** — Mermaid diagram code for any element.

Response: `{ guid, mermaidGraph }`. `mermaidGraph` is an empty string if no diagram is available.

#### Valid Values

**`GET /api/valid-values/properties`** — List all property names that have at least one registered valid value.

Response: `{ properties: [string, ...], total: N }`. Used by the Valid Values tab to pre-populate the sidebar. Queries `ValidMetadataValue` entries where `preferredValue IS_NULL` (these are the header registrations). Property names are extracted from `elementProperties.propertiesAsStrings.identifier` in the raw OpenMetadata response.

**`GET /api/valid-values/lookup`** — Valid values for a property name.

Query params: `property_name` (required), `type_name` (optional).

#### REST API Explorer

**`GET /api/request-bodies`** — The full Layer 1 request body catalog as JSON.

No Egeria connection required. Loaded from `egeria_request_body_catalog.json` on first call and cached in process. Response: `{ _meta, groups, bodies }`.

**`POST /api/request-bodies/rebuild`** — Regenerate the catalog from the http-client-collections directory.

Request body: `{ "http_collections_path": "/path/to/http-client-collections" }` (optional if `HTTP_COLLECTIONS_PATH` env var is set). Re-runs the extraction, overwrites the JSON file on disk, and updates the in-process cache.

**`GET /api/rest-apis`** — OpenAPI-derived endpoint catalog, augmented with Layer 1 body type mapping.

Query params: `url` (platform URL, overrides env). Fetches `/v3/api-docs` from the Egeria platform and returns `{ services }` — a list of OMAS/OMVS services, each with its endpoints, matched outer body type, inferred properties type, and parameter definitions. Results are cached in process for one hour.

**`POST /api/rest-apis/refresh`** — Clear the OpenAPI spec cache.

Query param: `url` (clears only that platform's entry; clears all if omitted).

#### Solution Architect

**`GET /api/solution/blueprints`** — All solution blueprints.

Query params: `url`, `server`, `user_id`, `user_pwd`.

Response: `[{ guid, displayName, qualifiedName, description, lifecycleStatus, components: [{guid, displayName, qualifiedName, componentType}] }]`.

**`GET /api/solution/blueprints/{guid}`** — Full detail for a single blueprint.

**`GET /api/solution/components`** — All solution components.

Response: `[{ guid, displayName, qualifiedName, componentType, description, mermaidGraph }]`.

**`GET /api/solution/components/{guid}`** — Full detail for a single component.

**`GET /api/solution/components/{guid}/implementations`** — Implementation elements linked to a component.

#### Data Design

**`GET /api/data-design/specs`** — All DataSpec elements (Collection subtypes).

**`GET /api/data-design/structures`** — All DataStructure elements.

**`GET /api/data-design/fields`** — All DataField elements.

**`GET /api/data-design/grains`** — All DataGrain elements.

**`GET /api/data-design/classes`** — All DataClass elements.

All list endpoints accept `url`, `server`, `user_id`, `user_pwd` query params.

**`GET /api/data-design/specs/{guid}`** — Full detail for a DataSpec.

**`GET /api/data-design/structures/{guid}`** — Full detail for a DataStructure.

**`GET /api/data-design/fields/{guid}`** — Full detail for a DataField.

#### Perspectives

**`GET /api/perspectives`** — All Perspective actor profiles.

Response: `[{ guid, displayName, qualifiedName, description, typeName }]`.

**`GET /api/perspectives/{perspective_guid}`** — Full detail for a single Perspective, including linked Questions.

**`GET /api/questions`** — All GlossaryTerms with the `Question` classification.

Query params: `start_from` (default 0), `page_size` (default 100), plus standard connection params.

**`GET /api/questions/{question_guid}`** — Full detail for a single Question.

#### Dr. Egeria Commands

**`GET /api/dr-egeria/commands`** — All command templates grouped by level and family.

No Egeria connection required. Response: `{ basic: { familyName: [{ title, description, params, template }] }, advanced: {...} }`.

**`POST /api/dr-egeria/execute`** — Execute a command block.

Body: `{ title, params, directive, url, server, user_id, user_pwd }`. Builds a markdown block and calls `dr_egeria_md.process_md_file`. Returns the output markdown.

#### Information Supply Chains

**`GET /api/isc`** — All information supply chain elements.

Response: `[{ guid, displayName, qualifiedName, description, scope, lifecycleStatus, mermaidGraph, ... }]`.

**`GET /api/isc/{guid}`** — Full detail for a single information supply chain.

#### Governance Definitions

**`GET /api/governance/tree`** — The governance definition type hierarchy.

Response: `[{ typeName, label, isAbstract, children: [...] }]` with three root nodes (`GovernanceDriver`, `GovernancePolicy`, `GovernanceControl`) and their subtypes.

**`GET /api/governance/definitions`** — Search or list governance definitions.

Query params: `type_name` (default `GovernanceDefinition`), `search_string` (default `*`), `start_from`, `page_size` (default 200, max 500), plus standard connection params. When `type_name` is not the base type, it is forwarded as `metadata_element_type` to `GovernanceOfficer.find_governance_definitions`.

Response: `{ definitions: [{ guid, typeName, displayName, qualifiedName, description, identifier, domainIdentifier, summary }], total, type_name }`.

**`GET /api/governance/definitions/{guid}`** — Full detail for a single governance definition.

Response: all list fields plus `scope`, `usage`, `importance`, `implications`, `outcomes`, `results`, `status`, `mermaidGraph`, and `relationships: { relName: [{ guid, typeName, displayName, qualifiedName, description }] }`.

#### Demo mode

See [demo-mode.md](demo-mode.md) for the complete auth and admin API reference.

---

### Implementation

For internal architecture, data-fetching strategy, `graph_query_depth` behaviour, and maintenance procedures, see [type-explorer-architecture.md](type-explorer-architecture.md).

For the extension history and remaining open work, see [Extending the TypeExplorer.md](Extending%20the%20TypeExplorer.md).

| File | Purpose |
|------|---------|
| `type_system_handler.py` | `/api/types` and `/egeria-explorer`; serves the SPA HTML; derives area numbers from supertype chain |
| `reference_data_handler.py` | `/api/reference-data`; fetches with `graph_query_depth=1` to get `parentSets` for tree construction |
| `glossary_handler.py` | `/api/glossary*`; uses `graph_query_depth=1` for terms; GUID-deduplicates before returning |
| `digital_products_handler.py` | `/api/digital-products`; recursive tree via `get_collection_members` with `graph_query_depth=0` |
| `mermaid_handler.py` | `/api/mermaid/{guid}`; uses `MetadataExpert.get_anchored_element_graph` |
| `valid_values_handler.py` | `/api/valid-values/properties` (pre-populates sidebar via `MetadataExpert.find_metadata_elements`); `/api/valid-values/lookup` (values for a name via `ReferenceDataManager.get_valid_metadata_values`) |
| `report_specs_handler.py` | `/api/report-specs`; reads local pyegeria report spec objects; no Egeria connection |
| `rest_api_handler.py` | `/api/request-bodies`, `/api/rest-apis`; catalog + live OpenAPI endpoint discovery |
| `governance_definitions_handler.py` | `/api/governance/tree`, `/api/governance/definitions`, `/api/governance/definitions/{guid}`; uses `GovernanceOfficer` |
| `pyegeria_handler.py` | FastAPI app entry point; mounts all routers |
| `type-explorer.html` | Self-contained SPA (React 18 + Mermaid 11 via CDN, application JS inlined) |
| `egeria_request_body_catalog.json` | Generated catalog of Layer 1 request body types; regenerate with `build_request_body_catalog.py` |
| `build_request_body_catalog.py` | Standalone script: extracts body types from http-client-collections and writes the catalog JSON |

---

### Troubleshooting

**Explorer shows "Loading Egeria Explorer…" forever** — A JavaScript syntax error in `type-explorer.html` prevented React from mounting. Open the browser developer console; a `SyntaxError` will be visible. This typically means a stray straight-quote character (`"`) inside a string literal — use Unicode curly quotes (`"…"`) instead, or escape with `\`.

**`Service Unavailable` on `/egeria-explorer`** — The `pyegeria-web` container is not running. Check `docker logs quickstart-pyegeria-web` for startup errors.

**Types don't appear / partial results** — The Egeria platform may not be fully started. The `/api/types` endpoint returns a 502 if Egeria is unreachable; the SPA shows a retry button. Wait for `egeria-main` to report healthy.

**Mermaid diagrams show raw code instead of a rendered diagram** — Mermaid JS failed to load from CDN (network/proxy issue), or the CDN version is wrong. Egeria generates mermaid v11+ syntax; loading `mermaid@10` causes silent render failures. Check the `<script>` tag in `type-explorer.html` references `mermaid@11`. If the CDN is unreachable in your environment, a local copy of `mermaid.min.js` must be served instead.

**Reference Data tree shows no items** — `find_valid_value_definitions` returned no results, or all items had no `parentSets` and the root-set filter excluded them. Check that the Egeria instance has valid value definitions loaded. Items with no `parentSets` that are not themselves sets will not appear in the tree; they can still be retrieved individually via `/api/reference-data/{guid}`.

**REST API tab shows no services** — The OpenAPI spec could not be fetched. Check that the Egeria platform is running and the platform URL is correct (defaults to `EGERIA_PLATFORM_URL` env var). The `/v3/api-docs` endpoint must be reachable from the `pyegeria-web` container. The Body Catalog inner tab is always available regardless of Egeria status.

**Catalog body types look out of date after an Egeria upgrade** — Run `python3 build_request_body_catalog.py` pointing at the new version's `http-client-collections` directory, then restart the container (or call `POST /api/request-bodies/rebuild` if `HTTP_COLLECTIONS_PATH` is set).

**Glossary terms show duplicates** — The deduplication pass uses `_header(t).get("guid", "")`. If a term has an empty GUID in the response, it could slip through. Check the Egeria instance for corrupt or incomplete elements.

**Area derivation is wrong for a type** — Add the type (or one of its supertypes) to `AREA_ANCHORS` in `type_system_handler.py` with the correct area number. The container picks up the change immediately (uvicorn `--reload`).

### MCP Server Issues
- **MCP server won't start**: Ensure the `mcp` package (>= 1.15.0) is installed: `pip install 'mcp>=1.15.0'`
- **Connection refused**: Verify `EGERIA_USER`, `EGERIA_USER_PASSWORD`, and server URLs are correct
- **Commands not found**: Ensure your pyegeria version includes the command handlers in `pyegeria.view.md_processing_utils`

### FastAPI Issues
If FastAPI returns `No updates detected. New File not created.`:
- Verify the markdown block starts with a command H1 (`# <Command Name>`).
- Check `debug_log.log` for warnings like `not found in command_list` or `Unknown command`.
- Confirm your pyegeria version includes the command handler in `pyegeria.view.md_processing_utils`.