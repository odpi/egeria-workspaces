<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Freshstart Portal — Authentication and User Management Guide

---

## Overview

Freshstart uses **Egeria as the single user store**. There is no SQLite database, no self-registration form, and no email verification. The portal authenticates directly against Egeria's token endpoint, issues a short-lived JWT session cookie, and delegates all account management to the Egeria SecurityOfficer API.

```
User → Portal login → POST /api/token (Egeria) → JWT session cookie → Portal hub
                                    ↓ CREDENTIALS_EXPIRED
                              Forced password-change form → new token → Portal hub
```

---

## Quick start

**First run — bootstrap sequence:**

1. Start the stack: `./fresh-start-local` (from the repository root)
2. Open `http://localhost:8086/login`
3. Sign in with `bootstrap` / `secret`
4. If redirected to the password-change form, set a new password and continue
5. You are now in the portal as an admin — go to **Admin → Egeria Users** to create accounts for your team

**Required `.env` settings** (`compose-configs/egeria-freshstart/.env`, gitignored):

```ini
JWT_SECRET=your-random-32-plus-char-string
```

Optional:

```ini
EGERIA_ORG_NAME=My Organisation          # shown in portal header and login page
```

---

## Architecture

### Single-layer authentication

| Quickstart | Freshstart |
|---|---|
| Login validates against SQLite `users` table | Login calls Egeria `POST /api/token` |
| Self-registration at `/register` | No registration — admin creates all accounts |
| Email verification flow | No email — credentials shared out of band |
| SQLite stores portal sessions and events | Egeria is the source of truth; portal issues JWT on successful auth |
| Persona picker (Coco Pharmaceuticals) | Direct tool access — no persona |

### User account storage and listing

Egeria manages user accounts through two parallel mechanisms:

- **In-memory cache** — SecurityOfficer OMVS holds the authoritative state for authentication. Mutations (create, update, delete, disable, reset-password) take effect immediately via the SecurityOfficer REST API.
- **YAML file** (`egeria-user-directory.omsecrets`) — Egeria's persistent backing store. Egeria lazily flushes its in-memory cache to this file (approximately hourly). The portal mounts this file directly at `/secrets/user-directory.omsecrets` and reads it for the admin user list so that newly created accounts are visible immediately without waiting for the hourly flush.

**Write path** (immediate auth effect + immediate listing):

```
Admin creates user → SecurityOfficer REST (auth takes effect)
                   → YAML mirror write (listing takes effect)
```

**Read path** (admin user list):

```
GET /api/admin/egeria-users → reads /secrets/user-directory.omsecrets directly
```

This hybrid approach will be replaced by the SecurityOfficer list API once Egeria adds one. See [`BACKLOG.md`](../BACKLOG.md) for the tracking item.

### User account types

Egeria tracks accounts by `userAccountType`. Only human account types are shown in the admin panel:

| Type | Shown in admin? | Notes |
|------|-----------------|-------|
| `EMPLOYEE` | Yes | Default for new accounts |
| `EXTERNAL` | Yes | Contractors, guests |
| `CONTRACTOR` | Yes | External contractors |
| `DIGITAL` | No | Egeria internal service NPAs (e.g. `generalnpa`, engine, integration connector identities) |

**Email is not part of a user account** — it belongs in the user's Egeria profile and is managed on the `/profile` page, not in the admin user creation form.

### JWT session cookie

After successful Egeria authentication the portal issues a signed JWT (`demo_token` cookie) containing:

- `sub` — Egeria user ID
- `role` — `admin` or `user` (see [Admin role](#admin-role) below)
- `display_name` — user ID (updated once a profile is saved via `/profile`)
- `egeria_token` — the Egeria bearer token, used for SecurityOfficer admin API calls
- `exp` — expiry (2 hours for regular users, 7 days for admins)

The Egeria token stored in the JWT is used directly for SecurityOfficer calls — admin operations run with the logged-in admin's own Egeria credentials, naturally respecting Egeria's RBAC.

### Admin role

Portal admin role is determined at login by the `EGERIA_ADMIN_USERS` environment variable — a comma-separated list of Egeria user IDs that receive `role=admin` in the portal JWT. Default is `bootstrap`.

```yaml
# egeria-freshstart.yaml
EGERIA_ADMIN_USERS: "bootstrap,yourusername"
```

Egeria's own RBAC (security roles, groups, zones) is independent of the portal admin flag.

---

## Configuration reference

All settings are read from container environment variables at startup.

**Secrets belong in `.env`, not the yaml.** Docker Compose automatically reads `compose-configs/egeria-freshstart/.env` (gitignored).

```ini
JWT_SECRET=your-random-32-plus-char-string
```

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET` | `change-me-before-going-public` | HS256 signing key — **set in `.env`, never in yaml** |
| `JWT_EXPIRY_USER_SECONDS` | `7200` | User session lifetime (2 hours) |
| `JWT_EXPIRY_ADMIN_SECONDS` | `604800` | Admin session lifetime (7 days) |
| `EGERIA_PLATFORM_URL` | `https://freshstart-egeria-main:8443` | Egeria platform URL (already set in yaml) |
| `EGERIA_VIEW_SERVER` | `fs-view-server` | View server for SecurityOfficer API calls |
| `EGERIA_ADMIN_USERS` | `bootstrap` | Comma-separated user IDs that get portal admin role |
| `EGERIA_ORG_NAME` | `Egeria` | Organisation name in portal header and login page |
| `SITE_URL` | `http://localhost:8086` | Public base URL |
| `EGERIA_USER_SECRETS_PATH` | `/secrets/user-directory.omsecrets` | Path to the mounted omsecrets YAML file used for user listing |

---

## Pages and routes

| Route | Description |
|-------|-------------|
| `GET /login` | Sign-in form (user ID + password). Handles CREDENTIALS_EXPIRED inline |
| `GET /portal` | Hub with tool tiles. Requires authentication |
| `GET /admin` | Admin panel. Requires `role=admin` |
| `GET /profile` | My Profile — view/edit Egeria profile and change password |
| `GET /egeria-explorer` | Egeria Explorer. Requires authentication |
| `GET /privacy` | Privacy policy |

---

## REST API reference

### Authentication

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/auth/login` | Public | Body: `{user_id, password}`. Returns JWT cookie or `{credentials_expired: true}` |
| `POST` | `/api/auth/change-password` | Public | Body: `{user_id, password, new_password}`. Returns JWT cookie |
| `POST` | `/api/auth/logout` | Public | Clears session cookie |
| `GET` | `/api/auth/me` | Optional | Returns `{authenticated, user_id, display_name, role}` |

### Profile

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/my-profile` | User | Get current user's Egeria profile |
| `POST` | `/api/my-profile` | User | Create or update Egeria profile |

### Platform

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/platform/org-name` | Public | Organisation name from `application.properties` or `EGERIA_ORG_NAME` |

### Admin — Egeria users

All endpoints require `role=admin`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/admin/roles` | List Egeria SecurityRole elements |
| `GET` | `/api/admin/groups` | List Egeria SecurityGroup elements |
| `GET` | `/api/admin/egeria-users` | List all Egeria user accounts |
| `POST` | `/api/admin/egeria-users` | Create a new user account |
| `PUT` | `/api/admin/egeria-users/{id}` | Update user (name, roles, groups, zones) |
| `POST` | `/api/admin/egeria-users/{id}/disable` | Set account status to `DISABLED` |
| `POST` | `/api/admin/egeria-users/{id}/reset-password` | Set new temp password; status → `CREDENTIALS_EXPIRED` |
| `DELETE` | `/api/admin/egeria-users/{id}` | Delete user account from Egeria |

### Admin — config

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/demo/config` | Get runtime config key/value store |
| `POST` | `/api/demo/config` | Update a config value. Body: `{key, value}` |

---

## User account lifecycle

### Account statuses

| Status | Meaning |
|--------|---------|
| `CREDENTIALS_EXPIRED` | Set on all new accounts — forces password change on first login |
| `ACTIVE` | Normal working state, set automatically after first password change |
| `DISABLED` | Account blocked; user cannot log in |

### Creating a user (admin steps)

1. Go to **Admin → Egeria Users → Create User**
2. Fill in User ID, display name, account type, and a temporary password. Security roles, groups, and zones are optional.
3. After clicking **Create User**, a prompt shows the credentials — copy and share with the user out of band (Slack, Teams, etc.)
4. The user logs in with the temporary password → the portal shows the forced password-change form → on success they enter the portal hub

**Note:** Email address is not part of the user account. It belongs in the user's Egeria profile and is set from the `/profile` page after first login.

### First login (user steps)

1. Open `http://localhost:8086/login` (or the configured SITE_URL)
2. Enter the User ID and temporary password
3. The portal detects `CREDENTIALS_EXPIRED` and shows the password-change form inline
4. Set a new password — the portal issues a session and redirects to the hub

### Resetting a password (admin)

In the **Egeria Users** tab, click **Reset Pw** next to the user. Enter a new temporary password. The user's status reverts to `CREDENTIALS_EXPIRED` and they must change it again on next login.

### Disabling an account

Click **Disable** next to the user. Sets `userAccountStatus: DISABLED`. The user cannot log in. Re-create the account or call the SecurityOfficer API directly to re-enable.

---

## Admin panel guide

Navigate to `/admin` while signed in as a portal admin.

### Egeria Users tab

Lists all human Egeria user accounts (types EMPLOYEE, EXTERNAL, CONTRACTOR) with user ID, display name, account type, status badge, and security roles. Egeria service accounts (type DIGITAL) are filtered out. Actions per user:

- **Edit** — opens a modal to update display name, security roles, security groups, default zones, and publish zones
- **Disable** — sets `userAccountStatus: DISABLED`
- **Reset Pw** — prompts for a new temporary password, sets status back to `CREDENTIALS_EXPIRED`
- **Delete** — permanently removes the account from Egeria (confirmation required; cannot be undone)

The **Create User** button opens the same modal pre-cleared. The **Security Roles** and **Security Groups** multi-selects are populated from the Egeria SecurityOfficer API (requires SecurityRole/SecurityGroup elements in the metadata store).

**Current limitation:** The Roles column always shows empty in the user list. Role and group memberships are stored in the `namedLists` section of the omsecrets YAML (not in the per-user record), so they cannot be reverse-mapped without additional work. This will be fixed once the SecurityOfficer list API is available. See [BACKLOG.md](../BACKLOG.md).

### Config tab

Key/value pairs persisted in `/app/demo-data/config.json` on the `demo-data` volume. Editable in place. Use for any runtime tuning flags specific to your deployment.

---

## Organisation name

The portal header shows **"Welcome — \<org name\>"**. Resolved in this order:

1. `platform.organization.name` from `application.properties`, if mounted into pyegeria-web at `/app/application.properties`
2. The `EGERIA_ORG_NAME` environment variable (simplest option)
3. Falls back to `"Egeria"`

To mount the properties file, add this volume to `freshstart-pyegeria-web` in `egeria-freshstart.yaml`:

```yaml
- ../../runtime-volumes/freshstart-platform-data/freshstart.application.properties:/app/application.properties:ro
```

Or simply set in `egeria-freshstart.yaml`:

```yaml
EGERIA_ORG_NAME: "My Organisation"
```

---

## SSL / HTTPS

SSL is off by default. The same opt-in mechanism as quickstart applies. See
[`../../egeria-quickstart/PyegeriaWebHandler/demo-mode.md`](../../egeria-quickstart/PyegeriaWebHandler/demo-mode.md#ssl--https)
for the full procedure. Substitute:

- yaml file: `egeria-freshstart.yaml` (apache-web service)
- Port: 8086 instead of 8085
- `SSL_SERVER_NAME`: your freshstart domain

---

## Security checklist

Before making a freshstart deployment accessible beyond localhost:

- [ ] `JWT_SECRET` set to a random 32+ character string in `.env` (not in yaml)
- [ ] `bootstrap` password changed on first login
- [ ] `EGERIA_ADMIN_USERS` updated to include your own user ID (so bootstrap can be retired)
- [ ] `SITE_URL` set to the actual public URL
- [ ] HTTPS enabled for public deployments (see [SSL / HTTPS](#ssl--https))
- [ ] Port 8001 (FastAPI) **not** exposed directly to the internet; all traffic via Apache on 8086
- [ ] `runtime-volumes/freshstart-platform-data/secrets/egeria-user-directory.omsecrets` exists (seeded from template by startup script; copy manually if starting compose directly)

---

## Troubleshooting

**Login redirects back to `/login` with no error** — Egeria platform may not be healthy yet. Check `docker compose logs freshstart-egeria-main` and wait for all servers to finish starting.

**"Invalid user ID or password"** — Confirm the user ID and password are correct in Egeria's secrets store. User IDs are case-sensitive.

**Password-change form appears every time** — The Egeria `POST /api/token` endpoint returned `CREDENTIALS_EXPIRED` even after the password change. Check `docker compose logs freshstart-pyegeria-web` — a HTTP 200 response from `/api/token` with a non-JSON body confirms the change succeeded. If the body is a JSON error, the `newPassword` field may not be accepted by this Egeria version.

**Admin panel shows empty Egeria Users list** — The omsecrets YAML file at `EGERIA_USER_SECRETS_PATH` may not exist or may not contain any human user entries. Check that `runtime-volumes/freshstart-platform-data/secrets/egeria-user-directory.omsecrets` exists on the host and is mounted correctly (the compose file mounts it to `/secrets/user-directory.omsecrets`). Run `docker compose logs freshstart-pyegeria-web` for YAML parse errors. If the file only contains `DIGITAL` accounts (Egeria service NPAs), the list will be empty — this is correct behaviour; human accounts must be created via the admin panel.

**omsecrets file missing on startup** — If `runtime-volumes/freshstart-platform-data/secrets/egeria-user-directory.omsecrets` doesn't exist, the startup script copies the template from `compose-configs/egeria-freshstart/secrets/egeria-user-directory.omsecrets`. If you bypassed the startup script and started compose manually, copy the template manually before starting: `cp compose-configs/egeria-freshstart/secrets/egeria-user-directory.omsecrets runtime-volumes/freshstart-platform-data/secrets/`.

**Roles/Groups dropdowns are empty in Create User form** — Expected if SecurityRole/SecurityGroup metadata has not been loaded into the metadata store via the Secrets Store Cataloguer integration connector. The create form still works — roles and groups fields will be empty multi-selects.

**"Admin access required" on `/admin`** — The signed-in user ID is not in `EGERIA_ADMIN_USERS`. Add it to `egeria-freshstart.yaml` and restart `freshstart-pyegeria-web`:

```bash
docker compose -f egeria-freshstart.yaml restart freshstart-pyegeria-web
```
