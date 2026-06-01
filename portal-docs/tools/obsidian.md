# Obsidian Vault

Obsidian is a note-taking app that doubles as the primary interface for writing and running [Dr. Egeria](dr-egeria/overview.md) commands. The **Call Dr. Egeria** plugin connects Obsidian to the Egeria backend via the Model Context Protocol (MCP).

---

## How to access Obsidian

The portal Obsidian tile offers three paths depending on your setup:

| Scenario | How it opens |
|---|---|
| `obsidian_vault_url` set in Admin → Config | Launches your local Obsidian app via `obsidian://` |
| Container available (lock free) | Opens the browser-based Obsidian at port 3000/3001 |
| Container in use | Shows "in use" status and a **Browse on GitHub** fallback |

---

## Option A — Local Obsidian (recommended for regular use)

Install [Obsidian](https://obsidian.md) on your machine. In the Admin panel → Config tab, set:

```
obsidian_vault_url = coco-workbooks
```

The portal tile will launch `obsidian://open?vault=coco-workbooks`. No session lock is involved.

---

## Option B — Containerised Obsidian (browser-based)

No install needed. The Quickstart stack automatically starts an Obsidian desktop session using **Selkies** (WebRTC-based streaming). It is always started by `quick-start-local` alongside the core services.

### Access URLs

| From | URL | Notes |
|------|-----|-------|
| On the server itself | `http://localhost:3000` | `localhost` is a secure context — WebRTC works |
| Remote, local mode | `https://<HOST_FQDN>:3001` | Self-signed cert — accept the browser warning once |
| Remote, demo mode | `https://<HOST_FQDN>:3001` | Real TLS cert (from `CERT_DIR`) — no browser warning |

The portal tile picks the right URL automatically. You never need to type the port manually.

> **Why port 3000 does not work remotely:** Selkies uses WebRTC for video streaming. Browsers only allow WebRTC in a *secure context* — either `https://` or `localhost`. Accessing `http://<hostname>:3000` from any non-localhost machine gives a black screen with a "needs a secure connection" error.

### Vault

`coco-workbooks/` is mounted as the vault root at `/config/vaults`. On the very first launch Obsidian shows a vault-selector screen — click **Open** (the path `/config/vaults` is already configured). This is a one-time step; the selection is saved to the mounted config volume and the vault opens directly on every subsequent restart.

### Session lock

Because there is only one containerised Obsidian instance, the portal manages exclusive access with a session lock:

1. The tile shows **● Available** when free. Click **Use Obsidian →** to acquire a session.
2. Your session has a configurable timer (default 20 min). Click **Extend** to add another block if no reservation is blocking.
3. Click **Release** when done so others can use it.
4. If you close the browser without releasing, the session expires automatically after the idle timeout (default 10 min hard, 5 min warning).

In demo mode the portal also writes your persona's Egeria credentials into the plugin's settings file when you acquire the lock — see [Persona auto-configuration](#persona-auto-configuration).

---

## Call Dr. Egeria plugin

### MCP Server URL

| Where Obsidian is running | URL to use |
|---|---|
| Local Obsidian, same machine as Docker | `http://localhost:8000/sse` |
| Local Obsidian, different machine on LAN | `http://<host-ip>:8000/sse` |
| Containerised Obsidian (Selkies) | `http://pyegeria-web:8000/sse` |

### Settings

Open **Settings → Call Dr. Egeria Settings (MCP)**:

- **MCP Server URL** — see table above
- **MCP Access Token** — must match `MCP_ACCESS_TOKEN` in the backend (default: `egeria-secret-mcp-token`)
- **Egeria User ID / Password** — your persona credentials; auto-populated by the portal in demo mode
- **Default Directive** — `process` / `validate` / `display`
- **Outbox Path** — where results are saved (relative to vault root, default: `dr-egeria-outbox`)
- **Vault Root** — absolute path to the vault inside the pyegeria-web container (e.g. `/coco-workbooks`)

### Running a command

1. Open a note containing a Dr. Egeria command.
2. Click the **Briefcase** icon in the left ribbon, or use **Command Palette → Run Note via MCP**.
3. Results appear in a resizable modal. If the directive is `process`, output is also saved to the outbox.

---

## Persona auto-configuration

In demo mode, when you select a persona in the portal and acquire the Obsidian lock, the portal writes your persona's Egeria credentials (`userId`, `userPass`) into the plugin's `data.json`. The plugin's file-watcher detects the change and reloads settings automatically — you'll see a notice: *"Dr. Egeria: session updated — persona is now `{userId}`"*.

This means you don't need to manually configure the plugin when switching personas.

---

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Black screen / "needs a secure connection" on port 3000 | Use `http://localhost:3000` (on the server) or `https://<HOST_FQDN>:3001` (remote) — Selkies/WebRTC requires a secure context |
| Self-signed cert warning on port 3001 | Local mode only — click Advanced → Proceed to accept once. In demo mode the real cert is used and no warning appears. |
| Vault selector appears on first open | Expected one-time step — click **Open** to confirm `/config/vaults`. The selection persists in `runtime-volumes/obsidian-config/` for all subsequent restarts. |
| 403 Forbidden in Dr. Egeria plugin | MCP Access Token mismatch — check plugin settings vs `MCP_ACCESS_TOKEN` env var |
| Connection refused in Dr. Egeria plugin | `quickstart-pyegeria-web` container not running |
| Timeout in Dr. Egeria plugin | Backend still processing — check outbox after a moment |
| Wrong persona credentials | Wait for file-watcher notice, or re-acquire the lock |
