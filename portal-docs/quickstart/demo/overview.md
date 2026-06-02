# Quickstart — Demo Environment

Demo mode enables public access to the Quickstart stack with user registration, persona selection, and a managed Obsidian session. It is designed for running structured demonstrations to external audiences.

---

## Enabling demo mode

From the repository root:

```bash
./quick-start-local --demo
```

On first run the script prompts for:
- **TLS certificate directory** — a host path containing `server.crt`, `server.key`, `server-ca.crt`
- **Admin bootstrap email and password** — the initial admin account
- **Resend API key** (optional) — for email verification; leave blank to verify accounts manually via `/admin`

Answers are saved to `compose-configs/egeria-quickstart/.env.demo` (mode 600, gitignored) and reused on subsequent runs. A JWT secret is auto-generated if not already set.

> **Do not manually edit `.env`** — it is regenerated on every startup. Demo credentials belong in `.env.demo`.

> **Rootless Podman note:** port 443 is privileged. Either run `sudo sysctl -w net.ipv4.ip_unprivileged_port_start=443` once, or set `HTTPS_PORT=8443` in `.env.demo` to use a non-privileged port.

---

## What starts

| Service | URL |
|---------|-----|
| Portal (HTTP) | `http://<HOST_FQDN>:8085` |
| Portal (HTTPS) | `https://<HOST_FQDN>` (port 443, or `HTTPS_PORT`) |
| Login | `https://<HOST_FQDN>/login` |
| Jupyter | `http://<HOST_FQDN>:7888` (password: `egeria`) |
| Egeria platform | `https://<HOST_FQDN>:9443` |
| Obsidian (local) | `http://localhost:3000` |
| Obsidian (remote) | `https://<HOST_FQDN>:3001` (self-signed cert — accept once) |

---

## User flow

1. Visitor arrives at the portal → redirected to `/login`
2. They register with email + password → receive a verification email (or admin verifies manually)
3. After verifying → they reach the portal and choose a persona
4. If they click Egeria Explorer without choosing a persona first, they are returned to the portal with the persona picker opened automatically

---

## Personas

Each persona represents a [Coco Pharmaceuticals](../coco/overview.md) employee with a different role and focus. Choosing a persona sets:
- The Egeria user ID and password used for all API calls
- The Dr. Egeria plugin credentials (auto-populated when acquiring Obsidian)
- The highlighted tools shown in the bio card

See [Coco Pharmaceuticals personas](../coco/personas.md) for the full list.

---

## Obsidian in demo mode

The containerised Obsidian instance is shared among all demo users. The portal manages access with a session lock:

- Users acquire a timed session (default 20 min) before Obsidian opens
- Credentials are injected automatically from the selected persona
- Admins can reserve blocks, evict current holders, and view the audit log

See [Obsidian session management](obsidian-sessions.md) for full details.

For Obsidian access from remote browsers, use `https://<HOST_FQDN>:3001` (self-signed cert). See [Obsidian](../../tools/obsidian.md) for why port 3000 does not work remotely.

---

## Updating to the latest version

To pull the latest egeria-workspaces and restart the demo environment:

```bash
./refresh-local --no-pull   # if you just want to rebuild without pulling
./refresh-local             # pull latest, rebuild all images, restart
```

Re-run with `--demo` after the refresh to restore HTTPS and auth:

```bash
./quick-start-local --demo
```

`refresh-local` preserves `.env.demo` (your certs, admin credentials, and JWT secret are not touched).

---

## Admin responsibilities

- Monitor and manage registered users in the [Admin panel](admin-guide.md)
- Set the Egeria reset schedule if you want the metadata store refreshed periodically
- Create Obsidian reservations before scheduled presentations
