<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Pyegeria Web Handler
The Pyegeria Web Handler is a python module that provides a web handler for the pyegeria command line interface. It is
used to execute Dr.Egeria commands from anything that can make a REST call - and that shares the same filesystem as
the Egeria runtime.

## Maintenance Notes
A version of dr_egeria_md.py has been copied to the root of the pyegeria-web-handler directory rather than 
just calling it from the md_processing module of pyegeria. This facilitated building. However, what this does mean is that after
significant change (generally additions) to the Dr.Egeria md_processing module, we need to copy the new version
of dr_egeria_md.py into the root of the pyegeria-web-handler directory and make a few checks and changes.

Check that the imports are correct. The name of the main routine is process_markdown_file. So if this changes in the
future, you will need to change either pyegeria_handler or dr_egeria_md.py to match. Other than that is should be a drop
in replacement.

## Command Catalog Notes
`md_processing/__init__.py` now re-exports command handlers and command lists from
`pyegeria.view.md_processing_utils` when available, and only falls back to local stubs when unavailable.
This prevents valid commands from being silently skipped because local constants were empty.

`dr_egeria_md.py` also attempts handler dispatch even when a command is missing from `command_list` and logs a warning.

### Path Handling
The Dr. Egeria engine and the Obsidian plugin work together to ensure that input paths are correctly resolved, even in "Content-First" mode:
- The Obsidian plugin allows configuring a **Vault Root** (the path inside the container) and an **Input Path** (the subfolder in the vault).
- These are combined with the note name to create a logical `input_file` path sent to the backend.
- The MCP server uses this logical path for context (like naming output files) but processes the actual markdown content from a temporary file created in the container's inbox. 
- This ensures that notes can be processed even if the Obsidian vault is not mounted into the Docker container.

## Model Context Protocol (MCP) Support

### Overview
The PyegeriaWebHandler includes a built-in MCP (Model Context Protocol) server that exposes Dr. Egeria capabilities through the MCP standard. This allows AI assistants like Claude to interact with your Egeria metadata ecosystem through a standardized protocol.

### MCP Protocol Support
The PyegeriaWebHandler uses the **Model Context Protocol (MCP)** standard via the `mcp` Python library (version >= 1.15.0). The implementation uses:
- **Transport Protocol**: stdio (standard input/output) for local execution
- **Server Framework**: `FastMCP` from the `mcp` library for simplified server implementation
- **Protocol Version**: MCP 1.0 compatible
- **Tool-Based Interface**: All Egeria commands are exposed as MCP "tools" that can be called by MCP clients

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
export EGERIA_ROOT_PATH="/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/exchange-freshstart"
export EGERIA_INBOX_PATH="loading-bay/dr-egeria-inbox"
export EGERIA_OUTBOX_PATH="distribution-hub/dr-egeria-outbox"
export PYEGERIA_LOG_DIRECTORY="/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-freshstart/PyegeriaWebHandler/logs"
```

If you launch `mcp_server.py` from within this workspace and do not set these values explicitly, the server will now auto-detect the freshstart exchange tree and use a writable local log directory.

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
        "EGERIA_VIEW_SERVER": "fs-view-server",
        "EGERIA_VIEW_SERVER_URL": "https://localhost:8443",
        "EGERIA_ROOT_PATH": "/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/exchange-freshstart",
        "EGERIA_INBOX_PATH": "loading-bay/dr-egeria-inbox",
        "EGERIA_OUTBOX_PATH": "distribution-hub/dr-egeria-outbox",
        "PYEGERIA_LOG_DIRECTORY": "/Users/<you>/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-freshstart/PyegeriaWebHandler/logs"
      }
    }
  }
}
```

### Available MCP Tools

The MCP server exposes the following tools:

1. **`dr_egeria_run_block`** (Main Tool - Direct Dr. Egeria Commands)
   - Execute any Dr. Egeria markdown command block
   - **Content-First Processing**: The server saves the `markdown_block` to a temporary file in the container, allowing it to process content from remote clients (like Obsidian) without requiring local file access.
   - **Output Note**: In SSE mode, this tool returns the generated Markdown as a string.
   - Parameters:
     - `markdown_block`: Markdown content with H1 command blocks
     - `url`: Egeria platform URL (e.g., `https://host.docker.internal:9443`)
     - `server_name`: Egeria view server name (e.g., `qs-view-server`)
     - `user_id`: Egeria user ID
     - `user_pass`: Egeria user password
     - `directive`: `display`, `validate`, or `process` (default: `process`)
     - `output_folder`: Optional output subfolder under outbox

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
- You need to tell Claude: "List glossaries from our Egeria instance at https://localhost:8443 with server fs-view-server"

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
- fs-metadata-store (primary)
- fs-archive-store (archive)
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
User: "List all the glossaries in our Egeria instance at https://localhost:8443 
       using the Dr. Egeria MCP server with server name fs-view-server"

Claude: I'll list the glossaries using the egeria_list_glossaries tool.
[Calls egeria_list_glossaries with url, server_name, user_id, user_pass]

Output: Available glossaries:
• Data Assets (id: glossary-001)
• Product Catalog (id: glossary-002)
• Business Concepts (id: glossary-003)
```

**Why this matters**: The convenience tools are wrappers around `dr_egeria_run_block`. They need your connection details to work:
- `url`: Your Egeria platform URL
- `server_name`: Your view server name (e.g., `fs-view-server`)
- `user_id`: Your Egeria username
- `user_pass`: Your Egeria password

## Troubleshooting

### MCP Server Issues
- **MCP server won't start**: Ensure the `mcp` package (>= 1.15.0) is installed: `pip install 'mcp>=1.15.0'`
- **Connection refused**: Verify `EGERIA_USER`, `EGERIA_USER_PASSWORD`, and server URLs are correct
- **Commands not found**: Ensure your pyegeria version includes the command handlers in `pyegeria.view.md_processing_utils`

### FastAPI Issues
If FastAPI returns `No updates detected. New File not created.`:
- Verify the markdown block starts with a command H1 (`# <Command Name>`).
- Check `debug_log.log` for warnings like `not found in command_list` or `Unknown command`.
- Confirm your pyegeria version includes the command handler in `pyegeria.view.md_processing_utils`.

