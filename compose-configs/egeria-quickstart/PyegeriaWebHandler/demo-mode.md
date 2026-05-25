<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Demo Mode — Setup and Operations Guide

---

## Overview

Demo mode adds user registration, authentication, and persona-based access control to Egeria Explorer. It is designed for public-facing deployments pre-loaded with Coco Pharmaceuticals data, where you want attendees to register and select a named persona before exploring the metadata.

When `DEMO_MODE=false` (the default), all demo machinery is dormant. The Explorer behaves as a local development tool: no login required, no persona picker, no auth gate on `/egeria-explorer`. All demo page routes (`/login`, `/register`, `/admin`, `/privacy`) still exist but redirect immediately to `/egeria-explorer`.

---

## Quick start

Edit `.env` (in the same directory as the yaml, already gitignored) and set these values:

```ini
DEMO_MODE=true                          # activates auth gating
JWT_SECRET=your-random-32-plus-char-string
SITE_URL=https://egeria-demo.example.com
ADMIN_BOOTSTRAP_EMAIL=you@example.com   # first admin account
ADMIN_BOOTSTRAP_PASSWORD=changeme       # change this
SMTP_PASSWORD=your-smtp-password        # leave blank to skip email
```

Then start the stack:

```bash
docker compose up --build
```

On first startup the container automatically creates the admin account from `ADMIN_BOOTSTRAP_EMAIL` / `ADMIN_BOOTSTRAP_PASSWORD`. If an admin already exists those vars are ignored, so it is safe to leave them set on subsequent restarts.

Log in at `/login` with those credentials to access the admin panel.

---

## Configuration reference

All settings are read from container environment variables at startup.

**Secrets belong in `.env`, not the yaml.** The compose yaml uses `${JWT_SECRET}` and `${SMTP_PASSWORD}` variable substitution. Docker Compose automatically reads `compose-configs/egeria-quickstart/.env` (already gitignored). Set real values there:

```ini
JWT_SECRET=your-random-32-plus-char-string
SMTP_PASSWORD=your-smtp-password
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DEMO_MODE` | `false` | Set `true` to activate demo auth gating |
| `DEMO_DB_PATH` | `/app/demo-data/demo.db` | Path to the SQLite database file inside the container |
| `JWT_SECRET` | `change-me-before-going-public` | HS256 signing key for session JWTs — **set in `.env`, never in yaml** |
| `JWT_EXPIRY_USER_SECONDS` | `7200` | User session lifetime in seconds (2 hours) |
| `JWT_EXPIRY_ADMIN_SECONDS` | `604800` | Admin session lifetime in seconds (7 days) |
| `SITE_URL` | `http://localhost:8085` | Base URL for email verification links (no trailing slash) |
| `SMTP_HOST` | _(blank)_ | SMTP server hostname. If blank, email sending is skipped |
| `SMTP_PORT` | `587` | SMTP port (587 = STARTTLS) |
| `SMTP_USER` | _(blank)_ | SMTP authentication username |
| `SMTP_PASSWORD` | _(blank)_ | SMTP authentication password — **set in `.env`, never in yaml** |
| `SMTP_FROM` | _(same as SMTP_USER)_ | Sender address for outbound emails |
| `ADMIN_BOOTSTRAP_EMAIL` | _(blank)_ | Email for the auto-created admin account. Only used when no admin exists yet |
| `ADMIN_BOOTSTRAP_PASSWORD` | _(blank)_ | Password for the auto-created admin account — **set in `.env`, never in yaml** |

**Development without SMTP:** Leave `SMTP_HOST` blank. New registrations will not receive a verification email. Use the admin panel to manually verify accounts, or promote an account to admin so it can manage others.

---

## Pages and routes

| Route | Behaviour |
|-------|-----------|
| `GET /login` | Serves login form. Auto-redirects to `/egeria-explorer` if already authenticated |
| `GET /register` | Serves registration form |
| `GET /egeria-explorer` | Auth-gated when `DEMO_MODE=true`. Redirects to `/login` if no valid session |
| `GET /admin` | Serves admin panel. Requires `role=admin`; redirects to `/login` otherwise |
| `GET /privacy` | Serves privacy policy (always accessible, no auth required) |

---

## REST API reference (demo)

### Authentication

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/auth/register` | Public | Register a new account. Body: `{display_name, email, password, org?}` |
| `GET` | `/api/auth/verify/{token}` | Public | Verify email, set cookie, redirect to Explorer |
| `POST` | `/api/auth/login` | Public | Log in. Body: `{email, password}`. Sets `demo_token` cookie |
| `POST` | `/api/auth/logout` | Public | Clear session cookie |
| `GET` | `/api/auth/me` | Optional | Returns `{authenticated, id, display_name, email, role}` or `{authenticated: false}` |
| `POST` | `/api/auth/forgot-password` | Public | Send reset link. Body: `{email}` |
| `POST` | `/api/auth/reset-password` | Public | Reset password. Body: `{token, password}` |

### Personas

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/demo/personas` | Public | List all personas (passwords excluded) |
| `POST` | `/api/demo/select-persona` | Verified user | Select a persona. Body: `{persona}`. Returns Egeria credentials |

### Admin

All admin endpoints require `role=admin`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/demo/users` | List all registered users |
| `POST` | `/api/demo/users/{id}/role` | Set role. Body: `{role: "user"\|"admin"}` |
| `POST` | `/api/demo/users/{id}/disable` | Disable account (sets `verified=false`) |
| `GET` | `/api/demo/events?limit=200` | Recent event log |
| `GET` | `/api/demo/config` | Current runtime config |
| `POST` | `/api/demo/config` | Update config. Body: `{key, value}` |

---

## Admin panel guide

Navigate to `/admin` while logged in as an account with `role=admin`.

### Users tab

Shows all registered users with role badge, verification status, and last login time. Available actions:

- **Promote** — elevate a `user` to `admin`.
- **Demote** — reduce an `admin` to `user`.
- **Disable** — blocks login by setting `verified=false`. The user record is retained for audit purposes.

### Events tab

Shows the 200 most recent events (register, verify, login, persona_select) with timestamps and detail JSON. Use this to diagnose registration problems or confirm that email verification completed.

### Config tab

Key/value pairs from the `config` table. All values are strings. Editable in place:

- `reset_interval_hours` — planned: how often the Egeria data store is reset (not yet implemented).
- `directive_cap` — planned: maximum Dr. Egeria directive level available to demo users (`validate` prevents writes; `process` allows writes).
- `session_lifetime_user` / `session_lifetime_admin` — informational; actual session lifetime is governed by the `JWT_EXPIRY_*` env vars set at container startup.

---

## Personas reference

All personas use the Egeria password `"secret"` — the well-known Coco Pharmaceuticals demo default. This is not a security concern as the Egeria instance is pre-populated with non-sensitive fictional data.

| ID | Display Name | Title | Difficulty | Starter | Focus Areas |
|----|-------------|-------|-----------|---------|-------------|
| `erinoverview` | Erin Overview | IT Project Leader | Starter | Yes | Full view; best entry point for new users |
| `peterprofile` | Peter Profile | Chief Data Officer | Business | Yes | Solution Architect, Perspectives, ISC |
| `calliequartile` | Callie Quartile | Data Scientist | Technical | Yes | Data Design, Glossary, ISC |
| `ivorpadlock` | Ivor Padlock | Information Security Officer | Business | Yes | Governance, Perspectives, Glossary |
| `garygeeke` | Gary Geeke | IT Infrastructure Director | Technical | — | Type System, Governance, Digital Products |
| `faithbroker` | Faith Broker | Head of Human Resources | Business | — | Perspectives, Governance, Glossary |
| `pollytasker` | Polly Tasker | Project Leader | Business | — | Solution Architect, ISC, Perspectives |
| `zachnow` | Zach Now | IT Systems Programmer | Technical | — | Type System, REST APIs, Dr. Egeria |
| `sallycounter` | Sally Counter | Finance Controller | Business | — | ISC, Glossary, Data Design |
| `nickstructure` | Nick Structure | Information Architect | Technical | — | Data Design, Type System, Glossary |

**Starter personas** are highlighted in the persona picker with a green "Starter" badge and are recommended as first picks for demo attendees new to Egeria.

Persona credentials come from `personas.json` in the container. To add or update a persona, edit `personas.json` and restart the container (the file is read on each request, so a hot reload via uvicorn `--reload` works without a full container restart).

---

## Database maintenance

The SQLite database persists at `DEMO_DB_PATH` on the `demo-data` volume. The schema is created automatically on first startup by SQLAlchemy (`Base.metadata.create_all`). No migration step is required for a fresh deployment.

**Backup:**

```bash
docker cp quickstart-pyegeria-web:/app/demo-data/demo.db ./demo-backup-$(date +%Y%m%d).db
```

**Reset (wipe all users and events, preserving config):**

```bash
docker exec quickstart-pyegeria-web python -c "
from demo_db import get_engine
from sqlalchemy import text
with get_engine().begin() as conn:
    conn.execute(text('DELETE FROM events'))
    conn.execute(text('DELETE FROM users'))
print('Users and events cleared')
"
```

After a reset, set `ADMIN_BOOTSTRAP_EMAIL` and `ADMIN_BOOTSTRAP_PASSWORD` in `.env` and restart the container — the bootstrap runs automatically on startup when no admin exists.

---

## SSL / HTTPS

SSL is **off by default**. The web server listens on port 8085 (HTTP) only. HTTPS is opt-in: three commented-out lines in `egeria-quickstart.yaml` are all that separate HTTP from HTTPS.

### Prerequisites

- A TLS certificate and private key for your domain (Let's Encrypt, self-signed, or commercial CA).
- The certificate files accessible on the Docker host at a stable path (not `~/Downloads`).
- Port 443 open on any firewall between users and the host.
- DNS pointing your domain at the host's IP address.

### Enabling SSL

**Step 1 — Edit `sites-available/fastapi-ssl.conf`.**
Change the four `Define` lines at the top to match your deployment:

```apache
Define SSL_SERVER_NAME your.domain.com
Define SSL_CERT_FILE   /etc/ssl/egeria/server.crt
Define SSL_KEY_FILE    /etc/ssl/egeria/server.key
Define SSL_CHAIN_FILE  /etc/ssl/egeria/server-ca.crt
```

**Step 2 — Uncomment the three SSL lines in `egeria-quickstart.yaml`** under `apache-web`:

```yaml
ports:
  - "8085:8085"
  - "443:443"          # ← uncomment

volumes:
  # ... existing volumes ...
  - ./sites-available/fastapi-ssl.conf:/usr/local/apache2/conf/extra/fastapi-ssl.conf  # ← uncomment
  - /path/to/your/certs:/etc/ssl/egeria:ro                                             # ← uncomment, fix path
```

Replace `/path/to/your/certs` with the directory on the host that contains the cert files named in Step 1.

**Step 3 — Update `SITE_URL` in `.env`** to use `https://`:

```ini
SITE_URL=https://your.domain.com
```

**Step 4 — Rebuild and restart the Apache container:**

```bash
docker compose -f egeria-quickstart.yaml up --build apache-web -d
```

The `--build` is required because `httpd.conf` changed. After this, subsequent cert or conf edits (volume-mounted) only need a restart:

```bash
docker compose -f egeria-quickstart.yaml restart apache-web
```

HTTP on port 8085 continues to work. If you want to redirect all HTTP traffic to HTTPS, add a `Redirect permanent / https://your.domain.com` inside the `<VirtualHost *:8085>` block in `fastapi-proxy.conf`.

### Disabling SSL

**Step 1 — Re-comment the three SSL lines** in `egeria-quickstart.yaml` (add `#` back):

```yaml
# - "443:443"
# - ./sites-available/fastapi-ssl.conf:/usr/local/apache2/conf/extra/fastapi-ssl.conf
# - /path/to/your/certs:/etc/ssl/egeria:ro
```

**Step 2 — Restart the Apache container:**

```bash
docker compose -f egeria-quickstart.yaml restart apache-web
```

No rebuild needed. `httpd.conf` contains `IncludeOptional conf/extra/fastapi-ssl.conf` — when the file is not mounted, Apache silently skips it and starts HTTP-only.

### How it works

`httpd.conf` contains a single line:

```apache
IncludeOptional conf/extra/fastapi-ssl.conf
```

When `fastapi-ssl.conf` is **not mounted**, Apache ignores it — no SSL modules are loaded, port 443 is not opened, and the container starts normally on 8085.

When the file **is mounted**, Apache loads it, which in turn loads `mod_ssl`, opens port 443, and activates the `<VirtualHost *:443>` block. All proxy locations are mirrored from the HTTP VirtualHost so the full application is available over both protocols.

### Certificate renewal

When your certificate expires, replace the files in the mounted host directory and restart the Apache container — no rebuild required:

```bash
docker compose -f egeria-quickstart.yaml restart apache-web
```

For Let's Encrypt with Certbot, the renewed files land in the same path automatically. Point the cert volume mount at the live directory (`/etc/letsencrypt/live/your.domain.com/`) and the container picks up renewals on its next restart.

---

## Security checklist

Before making a deployment public:

- [ ] `JWT_SECRET` set to a random 32+ character string in `.env` (not in the yaml)
- [ ] `SMTP_PASSWORD` set in `.env` (not in the yaml)
- [ ] `SMTP_HOST` set (or documented that email verification requires admin activation)
- [ ] `SITE_URL` set to the actual public URL (required for correct verify/reset links)
- [ ] HTTPS enabled for public deployments (see [SSL / HTTPS](#ssl--https) above); `SITE_URL` updated to `https://`
- [ ] Port 8000 (FastAPI) NOT exposed to the internet; all traffic via Apache on port 8085
- [ ] `demo-data/` volume mounted on persistent storage (not ephemeral container layer)
- [ ] Egeria data store pre-loaded with Coco Pharmaceuticals data before announcing the demo
- [ ] `ADMIN_BOOTSTRAP_EMAIL` and `ADMIN_BOOTSTRAP_PASSWORD` set in `.env` (not in the yaml) so admin is created on first startup

---

## Troubleshooting

**"Authentication required" on /egeria-explorer** — `DEMO_MODE` is true and the session cookie is missing or expired. Visit `/login` to sign in.

**Email verification link not arriving** — SMTP is not configured (`SMTP_HOST` blank). Log into the admin panel and enable the user's account manually: use the Users tab, find the user, and check their status. Alternatively, promote the account to admin (which also sets `verified=true`).

**Admin panel shows "Admin access required"** — The signed-in account has `role=user`. Bootstrap an admin account using the `docker exec` command in the [Quick start](#quick-start) section, then log in with those credentials.

**demo.db not persisting across container restarts** — The `demo-data` volume is not mounted. Check `egeria-quickstart.yaml` for the `../../runtime-volumes/quickstart-demo-data:/app/demo-data` volume mount. Create the directory if it does not exist:

```bash
mkdir -p runtime-volumes/quickstart-demo-data
```

**Persona picker not appearing** — Either `DEMO_MODE` is false (the persona picker only activates when `/api/auth/me` returns `authenticated: true`), or a persona was previously selected and stored in `localStorage`. Clear `egeria-persona` from browser localStorage or click "Switch" in the header badge.

**"Persona not found" error** — The persona ID sent to `/api/demo/select-persona` does not match any key in `personas.json`. Ensure the frontend is using the correct persona IDs (lowercase, no spaces: `erinoverview`, `peterprofile`, etc.).
