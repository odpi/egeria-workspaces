# Admin Guide

There are two admin panels depending on how Quickstart is running:

| Mode | URL | Access |
|------|-----|--------|
| **Demo mode** (`DEMO_MODE=true`) | `/admin` | Requires login with the admin role |
| **Local mode** (`DEMO_MODE=false`) | `/admin` | No login — open to anyone on the network |

This page documents the **demo mode** admin panel. For local mode, see [Local Admin](#local-admin) below.

---

## Demo admin panel

The demo admin panel is at `/admin`. It is only accessible to users with the admin role.

---

## Users tab

View all registered users. Actions per user:

| Action | When to use |
|---|---|
| **Promote / Demote** | Grant or remove admin role |
| **Verify** | Manually verify a user who didn't receive the email |
| **Resend Email** | Re-send the verification link (also shows the raw link for manual sharing) |
| **Disable** | Block a user from logging in |
| **Delete** | Permanently remove a user and their event history |

Stats at the top show total users, verified count, and admin count.

---

## Events tab

Shows the last 200 events across all users — registrations, logins, persona selections, and admin actions. Useful for auditing who did what and when.

---

## Feedback tab

Every in-app feedback submission (the 👍/👎/comment widget available on most pages), across **all three environments** — quickstart-demo, quickstart-local, and freshstart — filterable by environment and by triage status (New / Triaged / Actioned). Stats at the top show total submissions, new count, how many want a response, and the average star rating.

Set a submission's triage status inline from its row's **Actions** column as you work through the queue.

---

## Config tab

Runtime configuration key-value store. Changes take effect immediately without a restart.

Key config values:

| Key | Purpose |
|---|---|
| `reset_interval_hours` | Auto-reset interval (0 = disabled) |
| `obsidian_session_minutes` | Default Obsidian session length |
| `obsidian_idle_soft_minutes` | Minutes before idle warning shows |
| `obsidian_idle_hard_minutes` | Minutes before session marked STUCK |
| `obsidian_buffer_minutes` | Buffer before a reserved block |
| `obsidian_evict_grace_secs` | Default grace period for eviction |

---

## Reset tab

Controls the Egeria metadata store reset — stops the platform, drops the metadata schema, and restarts from scratch. User accounts are not affected.

- **Auto-reset schedule** — configure an interval (6h, 12h, 24h, etc.) to reset automatically
- **Force Reset Now** — trigger an immediate reset; Egeria takes ~5 minutes to reinitialise

---

## Obsidian tab

Manages the shared Obsidian session lock.

### Status cards

Show the current lock state, who holds it, their persona, and time remaining.

### Override actions

| Action | Effect |
|---|---|
| **Evict** | Starts a grace-period countdown — holder sees a warning in the portal |
| **Force unlock** | Releases the lock immediately — use for stuck sessions |

The grace period defaults to 5 minutes and is configurable per-eviction.

### Reservations

Create future reserved blocks (label, start time, end time) to block regular users from acquiring Obsidian during a scheduled presentation. Conflict detection prevents overlapping reservations.

### Audit log

Shows the last 50 lock events — acquisitions, releases, evictions, and auto-releases.

See also: [Obsidian session management](obsidian-sessions.md)

---

## Data Initialization tab

Controls which folders of Dr.Egeria documents get (re)run to seed the Portal's reference data after Egeria's metadata store is wiped — a redeploy, a manual DB drop, or a Reset tab action. See [Portal Startup and Data Initialization](../../tools/data-initialization.md) for the full mechanics; this section covers just what you see on this tab.

Every folder under `dr-egeria-inbox` shows up here automatically as a **batch**, with a checkbox for the folder itself and one per file inside it. A batch with an **auto-heal** badge is re-run automatically if Egeria detects its data went missing; a batch marked **manual only** never runs on its own — only when you click **Run Now** here, or **Run All Enabled** to run every checked batch in order.

A batch badged **⚠ not safe to re-run** contains a command known to duplicate data if run against a target that's already seeded — clicking Run Now (or Run All Enabled, if that batch is enabled) prompts for confirmation before proceeding rather than running silently. If you're not sure whether the batch's data already exists, check first (e.g. via Egeria Explorer) rather than confirming blind.

Selections are saved automatically as you check/uncheck — there's no separate Save button.

---

## Local Admin

In local mode the same `/admin` URL serves a lightweight page — no authentication required. It provides:

- **Obsidian lock** — status, force release, evict with grace period, reservations, audit log
- **User Feedback** — the same feedback queue as the demo admin panel's Feedback tab, scoped to this environment
- **Data Initialization** — same panel and behavior as [above](#data-initialization-tab)
- **Platform info** — Obsidian URL, Advisor status, Egeria connection settings

The local admin panel is useful when running Quickstart in a **shared small-team** context. It is linked from the portal home page as an **Admin** tile (visible in local mode only).

---

## Freshstart admin panel

Freshstart's `/admin` (Egeria-backed login required) has its own tab set, different from quickstart's demo admin panel above — it manages real Egeria user accounts rather than a separate demo account store, since freshstart has no self-registration:

- **Egeria Users** — create/manage Egeria user accounts (roles, security groups, default/publish zones)
- **Feedback** — same feedback queue as quickstart's
- **Config** — freshstart's own runtime config store
- **Data Initialization** — same panel and behavior as [above](#data-initialization-tab)

Freshstart has no Obsidian or Reset tab — it has no Obsidian integration, and its Egeria reset is handled outside the Portal.
