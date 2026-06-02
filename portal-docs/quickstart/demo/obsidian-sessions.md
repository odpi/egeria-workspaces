# Obsidian Session Management

The containerised Obsidian runs as a single shared desktop. The portal manages exclusive access through a session lock so multiple demo users don't collide.

---

## Session states

| State | Meaning |
|---|---|
| **FREE** | Available — anyone can acquire |
| **IN_USE** | A user holds the session |
| **ADMIN_IN_USE** | An admin holds the session |
| **STUCK** | Holder stopped sending keepalives — eligible for admin override |

---

## Regular user flow

1. The Obsidian tile shows **● Available** when free.
2. Click **Use Obsidian →** to acquire a session (your current persona is injected automatically).
3. A session timer counts down in the tile.
4. Click **Extend** to add another session block (blocked if a reservation is within the buffer window).
5. Click **Release** when done.

If you close the portal page without releasing, the session is automatically released after the idle timeout (default 10 minutes).

---

## Persona injection

When you acquire Obsidian, the portal writes your persona's Egeria credentials into the plugin's `data.json`. The Call Dr. Egeria plugin detects this change via a file-watcher and reloads settings — you'll see a notice in Obsidian: *"Dr. Egeria: session updated — persona is now `{userId}`"*.

This means you don't need to manually configure the plugin.

---

## Admin capabilities

| Action | Where | Effect |
|---|---|---|
| **Reserve a block** | Admin → Obsidian tab | Blocks regular users from acquiring during that window |
| **Evict current holder** | Admin → Obsidian tab | Shows warning to holder; releases after grace period |
| **Force unlock** | Admin → Obsidian tab | Releases immediately — use for stuck sessions |
| **View audit log** | Admin → Obsidian tab | Last 50 lock events |

### Reservations for presentations

Before a scheduled demo:
1. Go to **Admin → Obsidian tab → Reserved Blocks**
2. Enter a label (e.g. "Product demo — Acme Corp"), start time, and end time
3. Click **Reserve**

Regular users cannot acquire Obsidian within the **buffer window** (default 10 minutes) before a reservation starts. This ensures the desktop is ready when the demo begins.

### Eviction grace period

When you evict a holder, they see a warning banner in the portal counting down. The default grace period is 5 minutes — configurable per-eviction in the admin panel. After the deadline, the lock is released automatically.

---

## Local and small-team mode

In **local mode** (`DEMO_MODE=false`) the session lock is still active — useful when Quickstart is shared by a small team. The lock works identically, but there is no portal login and admin endpoints require no authentication.

**Releasing a stuck lock in local mode:**

Go to `/admin` (the **Admin** tile on the portal home page). The Local Admin page shows the lock state and provides Force Release and Evict buttons — no login required.

**Disabling the lock entirely** for a single-user install:

```
OBSIDIAN_LOCK_ENABLED=false
```

Set this in your `.env` and restart `quickstart-pyegeria-web`.

---

## Configuration

Session behaviour is tunable via the [Config tab](admin-guide.md#config-tab) or `.env`:

| Variable | Default | Purpose |
|---|---|---|
| `OBSIDIAN_SESSION_MINUTES` | `20` | Session length |
| `OBSIDIAN_IDLE_SOFT_MINUTES` | `5` | Idle warning threshold |
| `OBSIDIAN_IDLE_HARD_MINUTES` | `10` | STUCK threshold |
| `OBSIDIAN_BUFFER_MINUTES` | `10` | Buffer before reserved block |
| `OBSIDIAN_EVICT_GRACE_SECONDS` | `300` | Default eviction grace period |
| `OBSIDIAN_LOCK_ENABLED` | `true` | Set `false` to disable locking entirely |
