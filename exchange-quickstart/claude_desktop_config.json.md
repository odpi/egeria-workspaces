```json
{
  "mcpServers" : {
    "pyegeria" : {
      "command" : "\/Users\/dwolfson\/localGit\/egeria-python\/.venv\/bin\/python",
      "args" : [
        "\/Users\/dwolfson\/localGit\/egeria-python\/pyegeria\/mcp_server.py"
      ],
      "env" : {
        "EGERIA_USER" : "erinoverview",
        "EGERIA_VIEW_SERVER" : "qs-view-server",
        "EGERIA_PASSWORD" : "secret",
        "EGERIA_VIEW_SERVER_URL" : "https:\/\/localhost:9443"
      }
    },
    "dr-egeria" : {
      "command" : "\/Users\/dwolfson\/localGit\/egeria-python\/.venv\/bin\/python",
      "args" : [
        "\/Users\/dwolfson\/localGit\/egeria-v6\/egeria-workspaces-fs\/compose-configs\/egeria-quickstart\/PyegeriaWebHandler\/mcp_server.py"
      ],
      "env" : {
        "EGERIA_USER" : "erinoverview",
        "EGERIA_USER_PASSWORD" : "secret",
        "EGERIA_VIEW_SERVER" : "qs-view-server",
        "EGERIA_VIEW_SERVER_URL" : "https:\/\/localhost:9443",
        "EGERIA_ROOT_PATH" : "\/Users\/dwolfson\/localGit\/egeria-v6\/egeria-workspaces-fs\/exchange-quickstart",
        "EGERIA_INBOX_PATH" : "loading-bay\/dr-egeria-inbox",
        "EGERIA_OUTBOX_PATH" : "distribution-hub\/dr-egeria-outbox",
        "PYEGERIA_LOG_DIRECTORY" : "\/Users\/dwolfson\/localGit\/egeria-v6\/egeria-workspaces-fs\/compose-configs\/egeria-quickstart\/PyegeriaWebHandler\/logs"
      }
    }
  }
}
```

The `mcpServers` keys (`"pyegeria"` and `"dr-egeria"`) are just client-side aliases. They only need to be unique within the JSON file.

When you run the Dr. Egeria MCP server directly from your host, `EGERIA_ROOT_PATH` should point at the exchange tree root, not `/`. The server code now auto-detects a local quickstart/freshstart workspace layout, but keeping explicit host paths in the client config is still a good idea.

