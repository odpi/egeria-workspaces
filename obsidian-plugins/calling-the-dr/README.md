# Calling the Dr. (MCP) Obsidian Plugin

**Calling the Dr.** is the next-generation Obsidian plugin for interacting with Dr. Egeria. It uses the **Model Context Protocol (MCP)** to communicate with the backend, providing a robust, secure, and extensible interface.

For full setup, configuration, and usage details, please see the primary guide in the repository root:
👉 **[Configuring and Using the Calling Dr. Egeria Obsidian Plug-in](../../Configuring%20and%20Using%20the%20Calling%20Dr.%20Egeria%20Obsidian%20Plug-in.md)**

## Key Features

- **Content-First Design**: The plugin receives raw Markdown from the backend and writes it directly to the vault using the Obsidian API, avoiding Docker permission issues.
- **MCP-Based Communication**: Uses the Model Context Protocol over SSE (Server-Sent Events) for bidirectional communication.
- **Dynamic Command Discovery**: Automatically discovers available Dr. Egeria commands from the backend.
- **Flexible Directives**: Supports `process`, `validate`, and `display` modes.
- **Hot-Reload**: Built-in "Refresh Now" functionality to reload command definitions without restarting the backend container.
- **Rich Diagnostics**: Enhanced results modal with status icons (✅, ❌, ⚠️) and detailed console output.
- **Vault Portability**: Works with any Obsidian vault, even if not mounted in Docker.

## Prerequisites

- **Egeria Workspaces**: Running `quickstart` or `freshstart` environment.
- **Node.js**: v20 or later (for building).
- **Obsidian**: Installed and running.

## Installation & Deployment

The plugin source is located at `obsidian-plugins/calling-the-dr/`.

### 1. Build the Plugin
From the `obsidian-plugins/calling-the-dr/` directory:
```bash
npm install
npm run build
```

### 2. Deploy to Your Vault
Use the convenience scripts to deploy to standard Egeria Workspace vaults:
```bash
# Deploy to coco-workbooks
npm run deploy:coco

# Deploy to Work-Obsidian
npm run deploy:work
```

After deployment, **Reload** the plugin in Obsidian (Settings > Community Plugins).

## Configuration

Open Obsidian **Settings** and navigate to the **Calling the Dr. Settings (MCP)** tab.

### MCP Settings
- **MCP Server URL**: The SSE endpoint of your Dr. Egeria MCP server. Default: `http://localhost:8000/sse`.
- **MCP Access Token**: Security token for MCP access. Default: `egeria-secret-mcp-token`.

### Egeria Settings
- **Egeria User ID**: Your Egeria username (e.g., `erinoverview`).
- **Egeria User Password**: Your Egeria password (e.g., `secret`).
- **Egeria Platform URL**: The URL of the Egeria platform. Default: `https://host.docker.internal:9443`.
- **Egeria View Server**: The name of the View Server. Default: `qs-view-server`.
- **Default Directive**: Choose between `process` (execute), `validate` (check syntax), or `display` (view metadata).
- **Outbox Path**: The location relative to your vault root where Dr. Egeria should save output files (e.g., `dr-egeria-outbox`).
- **Vault Root**: The absolute path to your vault inside the Docker container (e.g., `/work/Work-Obsidian`). Used to provide logical context to the backend.
- **Input Path**: The subfolder path within your vault where the current note is located.

## Usage

1.  **Open a Note**: Open a Markdown file containing Dr. Egeria commands.
2.  **Call the Dr.**: Click the **Briefcase Icon** in the ribbon or use the command "Run Note via MCP".
3.  **View Results**: A rich modal will appear showing:
    - **Status**: Visual indicator of success or failure.
    - **Console Output**: Detailed logs from the processing engine.
    - **Output Info**: Path to the generated result file.
4.  **Check the Outbox**: Processed files are saved to your configured Outbox with the naming convention: `<original-name>-processed-<timestamp>.md`.

## Maintenance

### Refreshing Specs
If you update Dr. Egeria command definitions or fix dispatcher logic in the backend, you can click the **Refresh Now** button in the plugin settings. This forces the backend to reload its internal registry and command specifications immediately.

## Troubleshooting

- **403 Forbidden**: Ensure your **MCP Access Token** matches the token configured in the backend (usually defined in `pyegeria_handler.py`).
- **CORS Errors**: The backend automatically handles CORS for `app://obsidian.md`. If you see CORS errors, check that your `MCP Server URL` is correct and accessible.
- **Vault Root Configuration**: If you receive errors about file paths, ensure your **Vault Root** in settings matches the expected path on the backend (e.g. `/work/Work-Obsidian`). Note that the backend no longer requires direct file access to process your notes.
- **Permission Denied**: This is resolved in V3 by having the plugin write files directly. If you still see this, check your local OS permissions for the Obsidian vault folder.
- **Timeout**: Some searches take a long time. The plugin will notify you of the timeout, but the processing often completes in the background. Check your outbox after a few moments.
