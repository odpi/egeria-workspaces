### Obsidian Plugin Configuration Profiles

To support a vault-centric workflow with two different Obsidian vaults, please configure the following two profiles in your "Call Dr. Egeria" plugin settings.

#### Profile 1: Vault 1 (work/Obsidian)
- **Profile Name**: Vault 1 (work/Obsidian)
- **API URL**: `http://localhost:8085/dr-egeria/process`
- **Environment Key**: Quickstart Local
- **User Profile Key**: Egeria Markdown
- **Input Folder**: `/work/Obsidian`
- **Output Folder**: `dr-egeria-outbox`
- **Environment JSON**:
  ```json
  {
    "Egeria Kafka Endpoint": "host.docker.internal:9192",
    "Egeria Jupyter": true,
    "Dr.Egeria Outbox": ".",
    "Dr.Egeria Inbox": ".",
    "Egeria Integration Daemon": "qs-integration-daemon",
    "Egeria Integration Daemon URL": "https://host.docker.internal:9443",
    "Egeria View Server": "qs-view-server",
    "Egeria View Server URL": "https://host.docker.internal:9443",
    "Egeria Metadata Store": "qs-metadata-store",
    "Egeria Platform URL": "https://host.docker.internal:9443",
    "Egeria Engine Host": "qs-engine-host",
    "Egeria Engine Host URL": "https://host.docker.internal:9443",
    "Egeria Glossary Path": "/work/Obsidian/glossary",
    "Egeria Mermaid Folder": "/work/Obsidian/mermaid_graphs",
    "Pyegeria Root": "/work/Obsidian",
    "Pyegeria Config Directory": "/config",
    "Pyegeria User Format Sets Dir": "/config/format-sets",
    "Pyegeria Publishing Root": "http://localhost:8085/work/Obsidian/dr-egeria-outbox",
    "console_width": 250
  }
  ```

#### Profile 2: Vault 2 (coco-workbooks)
- **Profile Name**: Vault 2 (coco-workbooks)
- **API URL**: `http://localhost:8085/dr-egeria/process`
- **Environment Key**: Quickstart Local
- **User Profile Key**: Egeria Markdown
- **Input Folder**: `/coco-workbooks`
- **Output Folder**: `dr-egeria-outbox`
- **Environment JSON**:
  ```json
  {
    "Egeria Kafka Endpoint": "host.docker.internal:9192",
    "Egeria Jupyter": true,
    "Dr.Egeria Outbox": ".",
    "Dr.Egeria Inbox": ".",
    "Egeria Integration Daemon": "qs-integration-daemon",
    "Egeria Integration Daemon URL": "https://host.docker.internal:9443",
    "Egeria View Server": "qs-view-server",
    "Egeria View Server URL": "https://host.docker.internal:9443",
    "Egeria Metadata Store": "qs-metadata-store",
    "Egeria Platform URL": "https://host.docker.internal:9443",
    "Egeria Engine Host": "qs-engine-host",
    "Egeria Engine Host URL": "https://host.docker.internal:9443",
    "Egeria Glossary Path": "/coco-workbooks/glossary",
    "Egeria Mermaid Folder": "/coco-workbooks/mermaid_graphs",
    "Pyegeria Root": "/coco-workbooks",
    "Pyegeria Config Directory": "/config",
    "Pyegeria User Format Sets Dir": "/config/format-sets",
    "Pyegeria Publishing Root": "http://localhost:8085/coco-workbooks/dr-egeria-outbox",
    "console_width": 250
  }
  ```

### Key Changes & Interactions

- **Vault Roots**: All paths for `Egeria Root`, `Inbox`, and `Outbox` are now relative to the container's mount points (`/work/Obsidian` or `/coco-workbooks`).
- **Path Interaction**: The plugin's **Input Folder** is prepended to the active note's path before being sent to the backend. To ensure the backend correctly identifies the file, the `Dr.Egeria Inbox` in the **Environment JSON** should be set to `.` (the current directory relative to the root), which prevents redundant path stripping.
- **Output Interaction**: Similarly, setting `Dr.Egeria Outbox` to `.` in the JSON allows the plugin's **Output Folder** setting to be used as a relative path from the `Pyegeria Root`.
- **Publishing Root**: Each profile has a unique publishing root so that Apache can correctly serve the generated results.
- **Input/Output Folders**: The plugin will now correctly map your Obsidian notes to the container-side paths using these settings.

### Field Definitions

- **Environment Key**: A logical name for your server environment (e.g., "Quickstart Local"). This key is sent to the backend and returned in the results to help you identify which configuration was used.
- **User Profile Key**: A logical name for your user-specific settings (e.g., "Egeria Markdown"). Like the Environment Key, it is used for reporting and identifying the active profile in the results.
- **Environment JSON**: A JSON block containing technical settings for the Egeria environment (URLs, endpoints, paths).
- **User Profile JSON**: A JSON block containing settings specific to your Egeria user profile (Home Glossary, etc.).
