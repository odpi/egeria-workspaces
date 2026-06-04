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

## Local Admin

In local mode the same `/admin` URL serves a lightweight page — no authentication required. It provides:

- **Obsidian lock** — status, force release, evict with grace period, reservations, audit log
- **Platform info** — Obsidian URL, Advisor status, Egeria connection settings

The local admin panel is useful when running Quickstart in a **shared small-team** context. It is linked from the portal home page as an **Admin** tile (visible in local mode only).
