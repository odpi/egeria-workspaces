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

## Type System Explorer

The PyegeriaWebHandler includes a built-in **Type System Explorer** — an interactive browser for the Egeria open metadata type system. It queries the live Egeria instance via `ValidMetadataManager` and presents all entity types, relationship types, and classification types in a navigable web UI.

### Accessing the Explorer

Once the stack is running, open a browser and navigate to:

```
http://localhost:8085/type-explorer
```

Apache proxies this request through to the `pyegeria-web` container, which serves the single-page application and its backing API.

### Features

The explorer has two top-level views, switchable via tabs in the header: **Type Explorer** and **Attribute Index**.

#### Type Explorer view

**Area selector** — A dropdown in the header filters the view to a specific Egeria type system area, or shows all areas together:

| Area | Name |
|------|------|
| 0 | Foundation (OpenMetadataRoot, Referenceable, security base types) |
| 1 | Collaboration (people, teams, organisations) |
| 2 | Assets & Infrastructure |
| 3 | Glossary |
| 4 | Governance |
| 5 | Schemas |
| 6 | Data Stores |
| 7 | Lineage |

**Sidebar** — Shows three collapsible sections, each with a count in parentheses. All three start collapsed; click any section header to expand or collapse it:
- **Entity Types** — a full inheritance tree from `OpenMetadataRoot` down, with model area badges. Expand or collapse any branch; click any node to select it. When an area filter is active, only the types in that area and their ancestor path are visible in the tree.
- **Classifications** — flat alphabetical list of all classification types.
- **Relationships** — flat alphabetical list of all relationship types.
- A **search box** at the top switches all three sections into a flat filtered list simultaneously.

**Properties tab** — For any selected entity type, shows a table of all properties including inherited ones. Each row indicates which supertype originally defined the property (`own` badge for properties defined directly on the selected type, `req` for required). A toggle shows or hides inherited properties.

**Relationships tab** — Lists every relationship that the selected type participates in, derived by walking the full supertype chain. Shows the direction, the other endpoint type (clickable), and any properties on the relationship itself.

**Graph tab** — An SVG inheritance diagram showing the complete ancestor chain above the selected type and all direct subtypes below. Nodes are clickable to navigate. Pan by dragging; zoom with the scroll wheel or the −/+/1:1 toolbar buttons.

#### Attribute Index view

Shows every property name that appears anywhere in the type system — entities, relationships, and classifications — and for each property lists all the types that define it, grouped by kind. Use this view to answer questions such as "which types have a `description` property?" or to find naming inconsistencies across the type model.

- **Sidebar** — searchable alphabetical list of all property names with a count of how many types use each.
- **Detail panel** — three tables (Entities, Relationships, Classifications) showing every type that declares the selected property, its data type, and whether it is required. Clicking a type name navigates to it in the Type Explorer view.

#### Theme toggle

A **☀/☾** button in the top-right of the header switches between dark mode (default) and light mode. The preference is not persisted across page loads.

### REST API

The explorer is backed by a REST endpoint that can also be called directly:

#### `GET /api/types`

Returns all entity, relationship, and classification type definitions from the live Egeria instance.

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `area` | integer | Optional. Filter entity types to a single area (0–7). Relationships and classifications are always returned in full. |
| `url` | string | Egeria platform URL. Defaults to `EGERIA_PLATFORM_URL` env var. |
| `server` | string | Egeria view server name. Defaults to `EGERIA_VIEW_SERVER` env var. |
| `user_id` | string | Egeria user id. Defaults to `EGERIA_USER` env var. |
| `user_pwd` | string | Egeria user password. Defaults to `EGERIA_USER_PASSWORD` env var. |

**Example — all types:**
```
GET http://localhost:8085/api/types
```

**Example — governance types only:**
```
GET http://localhost:8085/api/types?area=4
```

**Response structure:**
```json
{
  "areaNames": { "0": "Foundation", "4": "Governance", ... },
  "entities": {
    "GovernanceDefinition": {
      "guid": "...",
      "area": 4,
      "abstract": true,
      "supertype": "Referenceable",
      "desc": "An aspect of the governance program.",
      "props": [
        { "name": "documentIdentifier", "type": "string", "desc": "...", "req": false }
      ]
    }
  },
  "classifications": {
    "Confidentiality": {
      "guid": "...",
      "desc": "Confidentiality level of data.",
      "validFor": ["Referenceable"],
      "props": [ ... ]
    }
  },
  "relationships": {
    "GovernanceDefinitionScope": {
      "guid": "...",
      "desc": "Links a governance definition to its scope.",
      "end1": "GovernanceDefinition",
      "end2": "Referenceable",
      "role1": "governanceDefinition",
      "role2": "scope",
      "props": []
    }
  }
}
```

The `props` list on each entity type contains only the **own properties** for that type. The UI computes the full inherited property list client-side by walking the `supertype` chain. Calling `/api/types` directly gives you the same raw data.

### Implementation

| File | Purpose |
|------|---------|
| `type_system_handler.py` | FastAPI `APIRouter` with the `/api/types` and `/type-explorer` routes. Calls `ValidMetadataManager.get_all_entity_defs()`, `get_all_relationship_defs()`, and `get_all_classification_defs()`. Derives area numbers by walking the supertype chain against `AREA_ANCHORS` — types that bypass the usual area-specific roots (e.g. `InformationSupplyChain`, `SolutionComponent`) are listed explicitly. Includes an import-time patch for a pyegeria bug in classification loading. |
| `type-explorer.html` | Self-contained single-page application (React via CDN, no build step). Fetches from `/api/types` on load. Place this file directly in `PyegeriaWebHandler/` alongside `type_system_handler.py`. |
| `sites-available/fastapi-proxy.conf` | Apache proxy rules routing `/type-explorer` and `/api/types` to `pyegeria-web:8000`. |
| `pyegeria_handler.py` | Two lines added before the MCP mount: imports the router and calls `app.include_router()`. |

**Area derivation** — The Egeria REST API does not include an area field in its TypeDef responses; area is a documentation concept. The handler derives it by walking up the supertype chain until it reaches a known anchor type. The mapping is defined in the `AREA_ANCHORS` dict in `type_system_handler.py`.

Not all types inherit from an area-specific root. Several Egeria types (notably `InformationSupplyChain`, `SolutionComponent`, `SolutionBlueprint`, `SolutionPort`, and `Port`) inherit directly from `Referenceable`, which would otherwise resolve to area 0 (Foundation). These are listed explicitly in `AREA_ANCHORS`:

```python
# Area 7 — Lineage (explicit entries for types that bypass Process in their supertype chain)
"Process": 7, "Port": 7, "LineageMapping": 7,
"InformationSupplyChain": 7, "InformationSupplyChainSegment": 7,
"SolutionBlueprint": 7, "SolutionComponent": 7, "SolutionPort": 7,
```

`Referenceable` itself is explicitly mapped to area 0 so it appears correctly in the Foundation area rather than being derived through the chain.

Add further entries to `AREA_ANCHORS` if you add custom types or discover that a standard type is assigned to the wrong area.

**Pyegeria compatibility note** — `ValidMetadataManager.get_all_classification_defs()` in current pyegeria versions uses a hardcoded `"typeDefList"` response key instead of the more robust `_extract_typedef_list()` helper used by the entity and relationship equivalents. `type_system_handler.py` monkey-patches this at import time to use the same helper, making classification loading resilient to future API response changes. The patch can be removed once the fix is merged upstream in pyegeria.

### Troubleshooting

**`Service Unavailable` on `/type-explorer`** — The `pyegeria-web` container is not running. Check `docker logs quickstart-pyegeria-web` for startup errors.

**Types don't appear / partial results** — The Egeria platform may not be fully started yet. The `/api/types` endpoint will return a 502 with a descriptive message if the platform is unreachable. Wait for `egeria-main` to report healthy, then reload the explorer.

**Area derivation is wrong for a type** — Add the type (or one of its supertypes) to `AREA_ANCHORS` in `type_system_handler.py` with the correct area number. The container picks up the change immediately (uvicorn runs with `--reload`).

**Entity tree is empty when area filter is applied** — The tree always roots at `OpenMetadataRoot`. When an area filter is active the full entity graph is still used for navigation; `visibleInTree` (computed in the UI) controls which nodes are rendered so that only the ancestors of matching types are shown. If no types match the selected area, the tree will show nothing — this is correct behaviour.

### MCP Server Issues
- **MCP server won't start**: Ensure the `mcp` package (>= 1.15.0) is installed: `pip install 'mcp>=1.15.0'`
- **Connection refused**: Verify `EGERIA_USER`, `EGERIA_USER_PASSWORD`, and server URLs are correct
- **Commands not found**: Ensure your pyegeria version includes the command handlers in `pyegeria.view.md_processing_utils`

### FastAPI Issues
If FastAPI returns `No updates detected. New File not created.`:
- Verify the markdown block starts with a command H1 (`# <Command Name>`).
- Check `debug_log.log` for warnings like `not found in command_list` or `Unknown command`.
- Confirm your pyegeria version includes the command handler in `pyegeria.view.md_processing_utils`.