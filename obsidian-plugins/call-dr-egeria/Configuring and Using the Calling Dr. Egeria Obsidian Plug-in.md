# Configuring and Using the Calling Dr. Egeria Obsidian Plug-in

This document provides complete instructions for configuring and using the "Call Dr. Egeria" Obsidian plugin with the Egeria Workspaces environment.

## 1. Prerequisites

*   **Egeria Workspaces** running (quickstart or freshstart).
*   **Obsidian** installed.
*   **Call Dr. Egeria Plugin** installed and enabled in your vault(s).

## 2. Plugin Deployment

The plugin must be built and deployed to your vault's plugin directory. From the `obsidian-plugins/call-dr-egeria/` directory:

```bash
# Install dependencies
npm install

# Deploy to coco-workbooks
npm run deploy:coco

# Deploy to Work-Obsidian
npm run deploy:work
```

After deployment, **Reload** the plugin in Obsidian (Settings > Community Plugins).

## 3. Configuration Profiles

The plugin uses profiles to switch between different vaults or environments. Each profile requires an **Environment JSON** block.

### Profile 1: Vault 1 (Work-Obsidian)
*   **Profile Name**: Work
*   **API URL**: `http://localhost:8085/dr-egeria/process`
*   **Environment Key**: Work
*   **Input Folder**: `<blank>` (optional, handled by Pyegeria Root)
*   **Output Folder**: `<blank>` (optional, handled by Pyegeria Root)
*   **Environment JSON**:
```json
{
  "Dr.Egeria Inbox": ".",
  "Dr.Egeria Outbox": ".",
  "Pyegeria Root": "/work/Work-Obsidian",
  "Pyegeria Publishing Root": "http://localhost:8085/work/Work-Obsidian/dr-egeria-outbox"
}
```

### Profile 2: Vault 2 (coco-workbooks)
*   **Profile Name**: coco-workbooks
*   **API URL**: `http://localhost:8085/dr-egeria/process`
*   **Environment Key**: coco-workbooks
*   **Input Folder**: `<blank>`
*   **Output Folder**: `<blank>`
*   **Environment JSON**:
```json
{
  "Dr.Egeria Inbox": ".",
  "Dr.Egeria Outbox": ".",
  "Pyegeria Root": "/coco-workbooks",
  "Pyegeria Publishing Root": "http://localhost:8085/coco-workbooks/dr-egeria-outbox"
}
```

## 4. Usage

1.  Open a Markdown file containing Dr. Egeria commands (e.g., `# View Glossaries`).
2.  Click the **Phone Icon** in the ribbon or use the command "Send Current Note to Dr.Egeria".
3.  A results modal will appear showing the status and console output. 
4.  **Note**: The results modal is resizable—drag the bottom-right corner to expand it.
5.  Check the `dr-egeria-outbox` folder in your vault for generated output files.

## 5. Troubleshooting

*   **File Not Found**: Ensure the `Pyegeria Root` in your Environment JSON matches the mount point in the `egeria-quickstart.yaml` file.
*   **500 Internal Server Error**: Check the Docker logs for the `quickstart-pyegeria-web` container.
*   **No Result Popup**: Ensure the plugin is reloaded in Obsidian after any updates.
