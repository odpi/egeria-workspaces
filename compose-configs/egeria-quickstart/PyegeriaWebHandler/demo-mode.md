<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Demo Mode — Setup and Operations Guide

---

## Overview

Demo mode adds user registration, authentication, and persona-based access control to the Egeria demo portal and Egeria Explorer. It is designed for public-facing deployments pre-loaded with Coco Pharmaceuticals data, where you want attendees to register, pick a named persona, and explore the metadata environment from that character's perspective.

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
RESEND_API_KEY=re_...                   # from resend.com — leave blank to skip email
RESEND_FROM=Egeria Demo <noreply@your-domain.com>
```

Then start the stack:

```bash
docker compose up --build
```

On first startup the container automatically creates the admin account from `ADMIN_BOOTSTRAP_EMAIL` / `ADMIN_BOOTSTRAP_PASSWORD`. If an admin already exists those vars are ignored, so it is safe to leave them set on subsequent restarts.

Log in at `/login` with those credentials to access the admin panel, then navigate to `/portal` to see the demo portal.

---

## Configuration reference

All settings are read from container environment variables at startup.

**Secrets belong in `.env`, not the yaml.** The compose yaml uses variable substitution (`${JWT_SECRET}`, `${SMTP_PASSWORD}`, etc.). Docker Compose automatically reads `compose-configs/egeria-quickstart/.env` (already gitignored). Set real values there.

### Core

| Variable | Default | Description |
|----------|---------|-------------|
| `DEMO_MODE` | `false` | Set `true` to activate demo auth gating |
| `SITE_URL` | `http://localhost:8085` | Base URL for email verification/reset links (no trailing slash) |
| `JWT_SECRET` | `change-me-before-going-public` | HS256 signing key — **set in `.env`, never in yaml** |
| `JWT_EXPIRY_USER_SECONDS` | `7200` | User session lifetime in seconds (2 h) |
| `JWT_EXPIRY_ADMIN_SECONDS` | `604800` | Admin session lifetime in seconds (7 d) |

### Demo auth database (PostgreSQL)

The demo auth tables (`users`, `events`, `config`) live in the **`demo_auth` schema** of the **`coco_pharma`** database on the shared PostgreSQL instance (`egeria-shared-postgres:5442`). This is the same host as the Egeria metadata store but a separate database/schema — the two are independent.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEMO_DB_HOST` | `egeria-shared-postgres` | PostgreSQL host |
| `DEMO_DB_PORT` | `5442` | PostgreSQL port |
| `DEMO_DB_NAME` | `coco_pharma` | Database name |
| `DEMO_DB_SCHEMA` | `demo_auth` | Schema for auth tables |
| `DEMO_DB_USER` | `demo_user` | DB user |
| `DEMO_DB_PASSWORD` | `demo4egeria` | DB password — **set in `.env`, never in yaml** |

Schema and tables are created automatically on first startup via SQLAlchemy (`Base.metadata.create_all`).

### Demo reset (Egeria metadata)

Admin-triggered reset: stops the Egeria container, drops the metadata store schema from PostgreSQL so Egeria re-seeds fresh Coco Pharmaceuticals data on restart.

| Variable | Default | Description |
|----------|---------|-------------|
| `EGERIA_CONTAINER_NAME` | `quickstart-egeria-main` | Docker container name for the Egeria platform |
| `EGERIA_META_DB_NAME` | `egeria` | Database holding Egeria's metadata store |
| `EGERIA_META_DB_USER` | `egeria_admin` | DB user for the metadata store |
| `EGERIA_META_DB_PASSWORD` | `admin4egeria` | DB password — **set in `.env`, never in yaml** |

The Docker socket must be mounted into the container (`/var/run/docker.sock:/var/run/docker.sock`) for reset to work.

### SMTP email

| Variable | Default | Description |
|----------|---------|-------------|
| `SMTP_HOST` | _(blank)_ | SMTP server hostname. If blank, email sending is skipped |
| `SMTP_PORT` | `587` | SMTP port (587 = STARTTLS) |
| `SMTP_SSL` | `false` | Set `true` for implicit TLS (port 465) |
| `SMTP_USER` | _(blank)_ | SMTP authentication username (falls back to `ADMIN_BOOTSTRAP_EMAIL`) |
| `SMTP_PASSWORD` | _(blank)_ | SMTP password — **set in `.env`, never in yaml** |
| `SMTP_FROM` | _(same as `SMTP_USER`)_ | Sender address for outbound emails |

### Resend email provider (alternative to SMTP)

| Variable | Default | Description |
|----------|---------|-------------|
| `RESEND_API_KEY` | _(blank)_ | Resend.com API key. If set, Resend is used instead of SMTP |
| `RESEND_FROM` | _(blank)_ | Sender address when using Resend |

### Bootstrap admin

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_BOOTSTRAP_EMAIL` | _(blank)_ | Email for the auto-created admin. Only used when no admin exists yet |
| `ADMIN_BOOTSTRAP_PASSWORD` | _(blank)_ | Password for the auto-created admin — **set in `.env`, never in yaml** |

**Development without SMTP/Resend:** Leave both blank. Registrations will not receive a verification email. Use the admin panel to manually verify accounts.

---

## Pages and routes

| Route | Behaviour |
|-------|-----------|
| `GET /portal` | Demo portal — persona picker, app launcher tiles, resource links. Requires authentication |
| `GET /login` | Login form. Auto-redirects to `/portal` if already authenticated |
| `GET /register` | Registration form |
| `GET /reset-password?token=…` | Password reset form — token arrives via email from the forgot-password flow |
| `GET /egeria-explorer` | Egeria Explorer. Auth-gated when `DEMO_MODE=true`; redirects to `/login` if no valid session |
| `GET /admin` | Admin panel. Requires `role=admin`; redirects to `/login` otherwise |
| `GET /privacy` | Privacy policy (always accessible, no auth required) |

---

## REST API reference (demo)

### Authentication

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/auth/register` | Public | Register a new account. Body: `{display_name, email, password, org?}` |
| `GET` | `/api/auth/verify/{token}` | Public | Verify email, set cookie, redirect to portal |
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

### Portal config

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/demo/portal-config` | Verified user | Returns `{obsidian_vault_url, obsidian_github_url}` for the portal tile |

### Demo reset

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/demo/reset/status` | Admin | Returns `{state, last_reset_at, reset_interval_hours}` |
| `POST` | `/api/demo/reset` | Admin | Trigger an immediate demo reset (async — returns `{status: "reset_started"}`) |

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

## Demo portal

The portal (`/portal`) is the landing page for authenticated demo users. It shows:

- **Hero banner** — welcome text, resource links (Documentation, GitHub, Coco Pharmaceuticals), and repo star prompts.
- **Persona card** — currently selected persona with display name, role, difficulty badge, and a link to their profile on egeria-project.org.
- **App launcher tiles** — one tile per integrated tool (Egeria Explorer, Jupyter, web resources, Obsidian workbooks).
- **Footer** — links to documentation, GitHub, Coco Pharmaceuticals, and Privacy Policy.

### Persona picker

Click **Switch** on the persona card to open the persona picker modal. It lists all available personas with role, difficulty, and a Starter badge for recommended entry-level personas. The description at the top links to the Coco Pharmaceuticals practice overview on egeria-project.org.

Selecting a persona:
1. Stores display info in `localStorage` (`egeria-persona`).
2. Calls `POST /api/demo/select-persona` to retrieve the matching Egeria credentials.
3. Stores those credentials in `localStorage` (`egeria-creds`) so Egeria Explorer can connect immediately without a separate login step.

### Obsidian tile

The **Coco Pharmaceuticals Workbooks** tile links to the `coco-workbooks` Obsidian vault:

- **Local access** (localhost/127.0.0.1): shows an **Open in Obsidian** button that launches the vault via the `obsidian://` protocol handler (requires Obsidian installed locally).
- **Remote access**: shows a **GitHub ↗** link pointing to the workbooks folder in the canonical repo (configurable).

Configure the tile via the admin Config panel:

| Config key | Description |
|------------|-------------|
| `obsidian_vault_url` | Vault name or `obsidian://` URI for local users. If not a full URI, it is wrapped as `obsidian://open?vault=<name>`. Leave blank to hide the local button. |
| `obsidian_github_url` | GitHub URL for remote users. Defaults to `https://github.com/odpi/egeria-workspaces/tree/main/coco-workbooks`. |

---

## Egeria Explorer

When accessed via the demo portal (demo mode active), Egeria Explorer behaves differently from standalone use:

- **Auto-credentials**: When a persona is selected in the portal, credentials are stored in `localStorage`. Explorer reads them automatically on load — no manual connection form needed.
- **Connection form hidden**: On the Home/splash screen in demo mode, the connection form is hidden. Users arriving from the portal are already connected.
- **Grouped navigation**: The top nav bar collapses the 10+ section buttons into three dropdown groups:
  - **Reference** — Type Explorer, REST APIs, Valid Values
  - **Review** — Glossary, Reference Data, Data Design, Solution Architect, Supply Chains, Perspectives
  - **Act** — Report Specs, Digital Products, Dr. Egeria
- **Type-system sub-toolbar**: When the Type Explorer is active, a secondary bar below the main nav provides the area filter and Attribute Index toggle, keeping the main nav clean.
- **Back to Portal**: A **Portal** button in the top-right header returns the user to `/portal`.
- **Persona badge**: The current persona name is shown in the header.

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

Key/value pairs from the `config` table. All values are strings. Editable in place.

| Key | Default | Description |
|-----|---------|-------------|
| `obsidian_vault_url` | _(blank)_ | Vault name or `obsidian://` URI for local Obsidian launch |
| `obsidian_github_url` | `https://github.com/odpi/egeria-workspaces/tree/main/coco-workbooks` | GitHub fallback for remote users |
| `reset_interval_hours` | `0` | Auto-reset interval; 0 = disabled. Set > 0 to enable scheduled resets |
| `directive_cap` | `validate` | Maximum Dr. Egeria directive level for demo users |
| `session_lifetime_user` | `7200` | Informational; actual lifetime is set by `JWT_EXPIRY_USER_SECONDS` |
| `session_lifetime_admin` | `604800` | Informational; actual lifetime is set by `JWT_EXPIRY_ADMIN_SECONDS` |
| `last_reset_at` | _(blank)_ | ISO timestamp of the last successful demo reset (set automatically) |
| `reset_state` | `ready` | `ready` or `resetting` — reflects current reset progress |

---

## Demo reset (Egeria metadata)

The demo reset wipes the Egeria metadata store and restarts it fresh with Coco Pharmaceuticals data. User accounts and config are unaffected.

**What it does:**
1. Stops the `quickstart-egeria-main` container.
2. Drops the `repository_qs_metadata_store` schema from the `egeria` database on `egeria-shared-postgres:5442`.
3. Restarts the container — Egeria re-seeds all Coco Pharmaceuticals data from scratch (~5 min).

**Triggering manually** (admin only):

```
POST /api/demo/reset
```

Returns immediately with `{status: "reset_started"}`. Check progress via:

```
GET /api/demo/reset/status
```

**Scheduled resets**: Set `reset_interval_hours` > 0 in the Config tab. The scheduler checks every 5 minutes and triggers a reset when the elapsed time exceeds the interval.

**Docker socket requirement**: Mount `/var/run/docker.sock` into the `quickstart-pyegeria-web` container (configured in `egeria-quickstart.yaml`).

---

## Personas reference

All personas use the Egeria password `"secret"` — the well-known Coco Pharmaceuticals demo default. This is not a security concern as the Egeria instance is pre-populated with non-sensitive fictional data.

| ID | Display Name | Title | Difficulty | Starter | Focus Areas |
|----|-------------|-------|-----------|---------|-------------|
| `erinoverview` | Erin Overview | IT Project Leader | Business | Yes | Full view; best entry point for new users |
| `peterprofile` | Peter Profile | Chief Data Officer | Business | Yes | Solution Architect, Perspectives, ISC |
| `calliequartile` | Callie Quartile | Data Scientist | Technical | Yes | Data Design, Glossary, ISC |
| `ivorpadlock` | Ivor Padlock | Information Security Officer | Business | Yes | Governance, Perspectives, Glossary |
| `garygeeke` | Gary Geeke | IT Infrastructure Director | Technical | — | Type System, Governance, Digital Products |
| `faithbroker` | Faith Broker | Head of Human Resources | Business | — | Perspectives, Governance, Glossary |
| `pollytasker` | Polly Tasker | Project Leader | Business | — | Solution Architect, ISC, Perspectives |
| `tomtally` | Tom Tally | Accounts Manager | Business | — | ISC lineage, Glossary, Data Design |
| `lemmiestage` | Lemmie Stage | Data Staging Manager | Technical | — | ISC pipeline flows, Data Design, Governance |
| `juleskeeper` | Jules Keeper | Records Manager | Business | — | Governance retention, Glossary, Perspectives |
| `stewfaster` | Stew Faster | Data Steward | Business | — | Glossary curation, Data Design, Governance |

**Starter personas** are highlighted in the persona picker with a green "Starter" badge and are recommended as first picks for demo attendees new to Egeria.

Persona credentials come from `personas.json` in the container. To add or update a persona, edit `personas.json` and restart the container (or hot-reload via uvicorn `--reload`).

---

## Database maintenance

The demo auth database is **PostgreSQL** — the `demo_auth` schema in the `coco_pharma` database on `egeria-shared-postgres:5442`. The schema is created automatically on first startup.

### Connecting directly

```bash
docker exec -it egeria-shared-postgres psql -U demo_user -d coco_pharma
```

Or from the host (if port 5442 is exposed):

```bash
psql -h localhost -p 5442 -U demo_user -d coco_pharma -n demo_auth
```

### Clearing users and events (preserving config)

```sql
DELETE FROM demo_auth.events;
DELETE FROM demo_auth.users;
```

Or via Docker:

```bash
docker exec egeria-shared-postgres psql -U demo_user -d coco_pharma \
  -c "DELETE FROM demo_auth.events; DELETE FROM demo_auth.users;"
```

After clearing, set `ADMIN_BOOTSTRAP_EMAIL` and `ADMIN_BOOTSTRAP_PASSWORD` in `.env` and restart the `quickstart-pyegeria-web` container — the bootstrap admin is re-created automatically when no admin exists.

### Full schema reset (nuclear option)

```bash
docker exec egeria-shared-postgres psql -U demo_user -d coco_pharma \
  -c "DROP SCHEMA IF EXISTS demo_auth CASCADE;"
```

The schema is recreated automatically on the next container start.

---

## SSL / HTTPS

SSL is **off by default**. The web server listens on port 8085 (HTTP) only. HTTPS is opt-in: three commented-out lines in `egeria-quickstart.yaml` are all that separate HTTP from HTTPS.

### Prerequisites

- A TLS certificate and private key for your domain.
- The certificate files accessible on the Docker host at a stable path.
- Port 443 open on any firewall between users and the host.
- DNS pointing your domain at the host's IP address.

### Enabling SSL

**Step 1 — Edit `sites-available/fastapi-ssl.conf`.**
Change the four `Define` lines at the top:

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
  - ./sites-available/fastapi-ssl.conf:/usr/local/apache2/conf/extra/fastapi-ssl.conf  # ← uncomment
  - /path/to/your/certs:/etc/ssl/egeria:ro                                             # ← uncomment, fix path
```

**Step 3 — Update `SITE_URL` in `.env`:**

```ini
SITE_URL=https://your.domain.com
```

**Step 4 — Rebuild and restart the Apache container:**

```bash
docker compose -f egeria-quickstart.yaml up --build apache-web -d
```

After first setup, cert or conf changes only need a restart (no rebuild).

### Disabling SSL

Re-comment the three SSL lines in `egeria-quickstart.yaml` and restart Apache:

```bash
docker compose -f egeria-quickstart.yaml restart apache-web
```

`httpd.conf` uses `IncludeOptional conf/extra/fastapi-ssl.conf` — when the file is not mounted, Apache silently starts HTTP-only.

### Cookie security

Cookies are set with `Secure=true` automatically when `SITE_URL` starts with `https://`. No additional configuration is required.

### Certificate renewal

Replace the files in the mounted cert directory and restart Apache — no rebuild required:

```bash
docker compose -f egeria-quickstart.yaml restart apache-web
```

---

## Security checklist

Before making a deployment public:

- [ ] `JWT_SECRET` set to a random 32+ character string in `.env` (not in the yaml)
- [ ] `SMTP_PASSWORD` (or `RESEND_API_KEY`) set in `.env` (not in the yaml)
- [ ] `SITE_URL` set to the actual public URL — required for correct verify/reset links and the `Secure` cookie flag
- [ ] HTTPS enabled for public deployments; `SITE_URL` updated to `https://`
- [ ] Port 8000 (FastAPI) NOT exposed to the internet; all traffic via Apache on port 8085
- [ ] `DEMO_DB_PASSWORD` and `EGERIA_META_DB_PASSWORD` set in `.env` (not in the yaml) if changed from defaults
- [ ] Egeria data store pre-loaded with Coco Pharmaceuticals data before announcing the demo
- [ ] `ADMIN_BOOTSTRAP_EMAIL` and `ADMIN_BOOTSTRAP_PASSWORD` set in `.env` so admin is created on first startup

---

## Troubleshooting

**"SSLCertificateFile: file '/etc/ssl/egeria/server.crt' does not exist"** — SSL lines are uncommented in the yaml but the cert directory is empty or missing. Generate self-signed certs with `./generate-certs.sh` from the repository root, or provide real certs in the mounted path.

**"Authentication required" on /egeria-explorer or /portal** — `DEMO_MODE` is true and the session cookie is missing or expired. Visit `/login` to sign in.

**Email verification link not arriving** — Neither `SMTP_HOST` nor `RESEND_API_KEY` is configured. Log into the admin panel and manually verify the account (Users tab), or promote it to admin.

**Admin panel shows "Admin access required"** — The signed-in account has `role=user`. Use the bootstrap env vars and restart the container to auto-create an admin, then log in with those credentials.

**Demo auth tables not found / schema errors** — The `demo_auth` schema has not been created yet. Restart the `quickstart-pyegeria-web` container — `get_engine()` creates the schema and tables on first call.

**Persona picker not appearing** — Either `DEMO_MODE` is false, or a persona was previously selected and stored in `localStorage`. Clear `egeria-persona` (and `egeria-creds`) from browser localStorage, or click **Switch** in the header persona badge.

**"Persona not found" error** — The persona ID sent to `/api/demo/select-persona` does not match any key in `personas.json`. Ensure the frontend is using the correct persona IDs (lowercase, no spaces: `erinoverview`, `peterprofile`, etc.).

**Egeria Explorer shows "Connect" tab with a form in demo mode** — The persona has not been selected yet, or `egeria-creds` was cleared from localStorage. Return to `/portal` and select a persona — Explorer will pick up the credentials automatically.

**Demo reset fails: "Cannot reach Docker daemon"** — `/var/run/docker.sock` is not mounted into the `quickstart-pyegeria-web` container. Check the volume mount in `egeria-quickstart.yaml`.

**Obsidian tile shows only GitHub link when I'm local** — `obsidian_vault_url` is not set in the Config tab. Set it to your vault name (e.g. `coco-workbooks`) or a full `obsidian://` URI. Local vs. remote detection is based on `window.location.hostname`; ensure you are accessing the portal via `localhost` or `127.0.0.1`.
