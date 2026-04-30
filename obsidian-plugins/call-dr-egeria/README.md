{
  "name": "call-dr-egeria",
  "version": "0.1.0",
  "description": "Send Obsidian notes to Dr.Egeria for processing.",
  "main": "main.js",
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "tsc --noEmit --skipLibCheck && node esbuild.config.mjs production",
    "deploy": "npm run build && node deploy.mjs",
    "deploy:coco": "npm run build && node deploy.mjs ../../coco-workbooks",
    "deploy:work": "npm run build && node deploy.mjs ../../work/Work-Obsidian",
    "package": "npm run build && mkdir -p dist && cp main.js manifest.json versions.json dist/",
    "version": "node version-bump.mjs && git add manifest.json versions.json"
  },
  "keywords": [
    "obsidian",
    "plugin",
    "egeria",
    "dr-egeria"
  ],
  "license": "Apache-2.0",
  "devDependencies": {
    "@types/node": "^20.17.57",
    "builtin-modules": "^3.3.0",
    "esbuild": "^0.25.12",
    "obsidian": "latest",
    "tslib": "^2.8.1",
    "typescript": "^5.9.3"
  }
}<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Call Dr.Egeria Obsidian Plugins

This directory contains two Obsidian plugins for interacting with Dr. Egeria.

## 1. Calling the Dr. (MCP) - RECOMMENDED
The new, feature-rich plugin using the **Model Context Protocol (MCP)**. It supports dynamic command discovery, hot-reloading of specs, and detailed diagnostic feedback.

- **Source**: `obsidian-plugins/calling-the-dr/`
- **Documentation**: See [Calling the Dr. README](../calling-the-dr/README.md)

## 2. Call Dr. Egeria (Legacy)
The original plugin that uses a direct REST API. It is maintained for compatibility but lacks the advanced discovery and refresh features of the MCP version.

- **Source**: `obsidian-plugins/call-dr-egeria/`
- **Documentation**: See [Legacy Plugin Instructions](./Configuring%20and%20Using%20the%20Calling%20Dr.%20Egeria%20Obsidian%20Plug-in.md)

## Prerequisites

The plugin was built and tested with Node.js v20 or later.

From `obsidian-plugins/call-dr-egeria/`, install Node dependencies:

```bash
npm install
```

The plugin uses:

- TypeScript
- esbuild
- Obsidian plugin APIs
- npm scripts for build/deploy/package tasks

## Build

From `obsidian-plugins/call-dr-egeria/`, run:

```bash
npm run build
```

This compiles and bundles the plugin to `obsidian-plugins/call-dr-egeria/main.js`.

## Deploy

The plugin must be deployed into an Obsidian vault's plugin directory to be used.

### Deploying to coco-workbooks or Work vaults

Convenience scripts are provided for standard environments:

```bash
# Deploy to ../../coco-workbooks
npm run deploy:coco

# Deploy to ../../work/Work-Obsidian
npm run deploy:work
```

### Deploying to a custom directory

To deploy the plugin to any other Obsidian vault, use the `deploy.mjs` script:

```bash
node deploy.mjs <path-to-your-obsidian-vault>
```

For example:
```bash
node deploy.mjs ~/Documents/MyNotes
```

This will create the necessary directory structure (`.obsidian/plugins/call-dr-egeria/`) and copy the built assets.

## Configuration

Once deployed and enabled in Obsidian (Settings -> Community Plugins), you can configure the plugin in the **Dr.Egeria Settings** tab.

### Configuration File

The plugin's settings are stored in a file named `data.json` within the plugin's directory in your vault:

`<vault-path>/.obsidian/plugins/call-dr-egeria/data.json`

This file is created automatically by Obsidian the first time you modify a setting or when the plugin is loaded with default values. You generally do not need to edit this file manually, as all configuration is available through the Obsidian UI.

### Profiles

The plugin supports multiple configuration profiles, allowing you to quickly switch between different Dr.Egeria environments or configurations.

- **Active Profile**: Select the profile to use from the "Active Profile" dropdown at the top of the settings tab.
- **Switching Profiles**: When you change the Active Profile, the settings UI updates to show the configuration for that specific profile. All subsequent "Call Dr.Egeria" actions will use the selected profile.
- **Profile Fields**: Each profile defines:
  - **API URL**: The Dr.Egeria service endpoint (e.g., `http://localhost:8085/dr-egeria/process`).
  - **Environment & User Profile Keys**: Logical identifiers for the configuration.
  - **Input/Output Folders**: Default paths for processing.
    - **Input Folder**: Default path prepended to the active note's path when sending to Dr.Egeria. If the note's path already starts with this folder, it is not prepended again.
    - **Output Folder**: Passed to Dr.Egeria to specify where to write results.
  - **Environment & User Profile JSON**: Detailed configuration blocks.
    - **Pyegeria Root**: Can be an absolute path or a relative path (e.g., `work/Work-Obsidian`). Relative paths are resolved against the workspace root.

### Credentials

User ID and Password are kept separate from the profile JSON to avoid accidental exposure. These are global settings (not per-profile) and are sent with every request to the Dr.Egeria service.

### Example Configuration

### Profile Settings

- **Environment Key**: A logical name for the environment configuration (e.g., "Quickstart Local").
- **User Profile Key**: A logical name for the user profile configuration (e.g., "Egeria Markdown").
- **Input Folder**: Optional path to prepend to the note path. Useful for mapping Obsidian paths to container paths.
- **Output Folder**: Path where Dr. Egeria should place the results.

#### Environment JSON
```json
{
  "Egeria Kafka Endpoint": "host.docker.internal:9192",
  "Egeria Jupyter": true,
  "Dr.Egeria Outbox": ".",
  "Dr.Egeria Inbox": ".",
  "Egeria Platform URL": "https://host.docker.internal:9443",
  "Pyegeria Root": "/work/Work-Obsidian",
  "Pyegeria Publishing Root": "http://localhost:8085/work/Work-Obsidian/dr-egeria-outbox",
  "console_width": 250
}
```
> **Note**: Setting `Dr.Egeria Inbox` and `Dr.Egeria Outbox` to `.` in the JSON is recommended when using absolute paths in the **Input Folder** setting, to avoid redundant path stripping by the backend.

#### Multi-Vault Configuration
If you are using multiple Obsidian vaults with the Egeria quickstart environment, you should create separate profiles for each vault. Each profile should have its `Pyegeria Root`, `Dr.Egeria Inbox`, and `Pyegeria Publishing Root` aligned with the vault's mount point in the container.

Detailed configuration examples for different vaults can be found in `compose-configs/egeria-quickstart/OBSIDIAN_PROFILES.md`.

#### User Profile JSON
```json
{
  "Egeria Home Glossary Name": "Egeria-Markdown",
  "Egeria Local Qualifier": "PDR",
  "Egeria Home Collection": "MyHome"
}
```

## How to use the plugin

1. **Select a Directive**: In Settings, choose between `process`, `validate`, or `display`.
2. **Send a Note**:
   - Click the **Phone icon** ("Call Dr.Egeria") in the left ribbon.
   - Or use the Command Palette (`Ctrl/Cmd + P`) and search for `Call Dr.Egeria: Send Current Note to Dr.Egeria`.
3. **View Results**: A modal will appear showing the status, message, and any console output returned by the service.
4. **Refresh Command Specs**: If the Dr.Egeria command definitions change on the server, use the `Refresh Dr.Egeria Command Specs` command or the button in Settings to reload them.