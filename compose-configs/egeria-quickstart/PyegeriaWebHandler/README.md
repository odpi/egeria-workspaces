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

The explorer has six tabs across the top, ordered left to right: **Type Explorer → Glossary → Reference Data → Digital Products → Report Specs → Valid Values**. Each tab is independent; data is loaded lazily when the tab is first opened. All sections are read-only.

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

- Left panel: a text input for any property name, plus quick-access buttons for standard Egeria property names (`contentStatus`, `activityStatus`, `governanceStatus`, etc.).
- Right panel: the ordered list of allowed values for the selected property, with display names, preferred values, and descriptions.

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

**`GET /api/valid-values/lookup`** — Valid values for a property name.

Query params: `property_name` (required), `type_name` (optional).

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
| `valid_values_handler.py` | `/api/valid-values/lookup`; uses `ReferenceDataManager.get_valid_metadata_values` |
| `report_specs_handler.py` | `/api/report-specs`; reads local pyegeria report spec objects; no Egeria connection |
| `pyegeria_handler.py` | FastAPI app entry point; mounts all routers |
| `type-explorer.html` | Self-contained SPA (React 18 + Mermaid 11 via CDN, application JS inlined) |

---

### Troubleshooting

**Explorer shows "Loading Egeria Explorer…" forever** — A JavaScript syntax error in `type-explorer.html` prevented React from mounting. Open the browser developer console; a `SyntaxError` will be visible. This typically means a stray straight-quote character (`"`) inside a string literal — use Unicode curly quotes (`"…"`) instead, or escape with `\`.

**`Service Unavailable` on `/egeria-explorer`** — The `pyegeria-web` container is not running. Check `docker logs quickstart-pyegeria-web` for startup errors.

**Types don't appear / partial results** — The Egeria platform may not be fully started. The `/api/types` endpoint returns a 502 if Egeria is unreachable; the SPA shows a retry button. Wait for `egeria-main` to report healthy.

**Mermaid diagrams show raw code instead of a rendered diagram** — Mermaid JS failed to load from CDN (network/proxy issue), or the CDN version is wrong. Egeria generates mermaid v11+ syntax; loading `mermaid@10` causes silent render failures. Check the `<script>` tag in `type-explorer.html` references `mermaid@11`. If the CDN is unreachable in your environment, a local copy of `mermaid.min.js` must be served instead.

**Reference Data tree shows no items** — `find_valid_value_definitions` returned no results, or all items had no `parentSets` and the root-set filter excluded them. Check that the Egeria instance has valid value definitions loaded. Items with no `parentSets` that are not themselves sets will not appear in the tree; they can still be retrieved individually via `/api/reference-data/{guid}`.

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