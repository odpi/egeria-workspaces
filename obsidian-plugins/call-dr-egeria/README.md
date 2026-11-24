# Call Dr. Egeria — Obsidian Plugin

**Call Dr. Egeria** is the Obsidian plugin for interacting with Dr. Egeria via the **Model Context Protocol (MCP)** over SSE. It sends the active note to the backend for processing, validation, or display, and writes the result directly back into your vault.

For full setup and configuration details see the primary guide:
👉 **[Configuring and Using the Call Dr. Egeria Obsidian Plugin](../../Configuring%20and%20Using%20the%20Call%20Dr.%20Egeria%20Obsidian%20Plugin.md)**

## Key Features

- **MCP over SSE**: Robust, token-secured communication with the Dr. Egeria backend.
- **Content-First**: Plugin writes results directly to the vault — no Docker volume permissions required.
- **Auto-Config**: When deployed via `npm run deploy:coco`, the container MCP URL (`http://pyegeria-web:8000/sse`) is written as the default so no manual setup is needed inside the containerized Obsidian.
- **Live Persona Reload**: When the portal updates the session persona, the plugin detects the change in `data.json` and reloads settings automatically (shows a notice).
- **Flexible Directives**: `process`, `validate`, and `display` modes.
- **Rich Results Modal**: Status icons (✅ ❌ ⚠️), resizable window, optional verbose toggle.

## Prerequisites

- Node.js v20+ (for building)
- Obsidian desktop (native) **or** the containerized Obsidian via the quickstart stack

## Build

```bash
cd obsidian-plugins/call-dr-egeria
npm install
npm run build
```

## Deploy

| Command | Target | MCP URL default |
|---|---|---|
| `npm run deploy:coco` | `coco-workbooks` vault (container use) | `http://pyegeria-web:8000/sse` |
| `npm run deploy:coco:local` | `coco-workbooks` vault (local/native use) | `http://localhost:8000/sse` |
| `npm run deploy:work` | `work/Work-Obsidian` vault | `http://localhost:8000/sse` |

`deploy:coco` writes `data.json` defaults only on a **fresh install** — existing user config is never overwritten.

After deploying, reload the plugin in Obsidian: **Settings → Community Plugins → Call Dr. Egeria → Reload**.

## MCP Server URL quick reference

| Where Obsidian is running | MCP Server URL |
|---|---|
| Native, same machine as Docker | `http://localhost:8000/sse` |
| Native, different machine on LAN | `http://<host-ip>:8000/sse` |
| Containerized (KasmVNC / quickstart) | `http://pyegeria-web:8000/sse` |

## Configuration

Open **Settings → Call Dr. Egeria Settings (MCP)**:

- **MCP Server URL** — SSE endpoint (see table above)
- **MCP Access Token** — must match `MCP_ACCESS_TOKEN` in the backend container. There is no default: `quick-start-local` (or `fresh-start-local`) generates one into the stack's `.env` (`compose-configs/egeria-quickstart/.env`) on the first run; copy it from there. In demo mode the portal fills it in when you take the Obsidian lock. The value the stack used to publish is refused. `node deploy.mjs <vault> --container` takes it from the `MCP_ACCESS_TOKEN` environment variable if set.
- **Egeria User ID / Password** — persona credentials; auto-populated by the portal in demo mode
- **Default Directive** — `process` / `validate` / `display`
- **Outbox Path** — where results are saved (relative to vault root)
- **Vault Root** — absolute path to vault inside the pyegeria-web container (e.g. `/coco-workbooks`)
- **Verbose Output** — toggle to hide internal log lines from the results modal

## Troubleshooting

| Symptom | Check |
|---|---|
| 403 Forbidden | MCP Access Token mismatch |
| Blank/timeout | Backend still processing — check outbox after a moment |
| Wrong persona | Portal may not have written `data.json` yet; check Obsidian lock status in the portal |
| CORS error | Verify MCP Server URL is correct and the backend container is running |
