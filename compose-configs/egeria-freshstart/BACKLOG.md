<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Freshstart Backlog

Items completed in quickstart that still need to be applied or adapted for freshstart.

---

## Pending

### Security / deployment readiness
- [ ] **JWT_SECRET** — set a real random value in `compose-configs/egeria-freshstart/.env` before any public deployment (never in the yaml)
- [ ] **SITE_URL** — update `SITE_URL` in `egeria-freshstart.yaml` to the correct public URL when deploying beyond localhost (currently `http://localhost:7885`)
- [ ] **EGERIA_ADMIN_USERS** — add your own Egeria user ID to the `EGERIA_ADMIN_USERS` list in `egeria-freshstart.yaml` after first login so the `bootstrap` account can be retired

### Portal / Apache config
- [ ] Freshstart shares quickstart's `httpd.conf` and `fastapi-proxy.conf` (via `context: ../egeria-quickstart`). Verify the proxy rules work correctly on freshstart's port 7885.

### SSL
- [ ] Configure Apache SSL for freshstart port 7885 once quickstart SSL is proven. See the SSL section in [`PyegeriaWebHandler/demo-mode.md`](PyegeriaWebHandler/demo-mode.md#ssl--https) for the procedure (substitute port 7885 and `egeria-freshstart.yaml`).

### PostgreSQL demo schema
- [ ] Run `CREATE SCHEMA IF NOT EXISTS demo; GRANT ALL ON SCHEMA demo TO egeria_admin, egeria_user;` against the freshstart postgres if it uses a separate DB instance.

### User management API upgrade
- [ ] **Switch user listing to new SecurityOfficer list API** — The current implementation reads the `egeria-user-directory.omsecrets` YAML file directly for the admin user list because (a) SecurityOfficer has no list-all endpoint and (b) OMRS sync from SecurityOfficer to the actor registry runs hourly. When Egeria adds a SecurityOfficer list endpoint, replace the YAML-reading path in `list_egeria_users()` in `demo_auth_handler.py` with the new API call. The mutation paths (create/update/delete/disable/reset-password) already use SecurityOfficer correctly — only listing needs updating.
- [x] **Fix security roles and groups in admin edit modal** — Replaced multi-select with checkbox lists; pre-population on edit now works correctly. See BACKLOG.md FS-1.
- [ ] **Fix roles column in user list table** — The Roles column in the admin panel user table is still always empty (separate from modal pre-population). Requires reverse-mapping `namedLists` in the YAML reading path or a new SecurityOfficer list API. See BACKLOG.md FS-1 notes.

### Data loading
- [ ] Freshstart ships empty — unlike quickstart, Coco Pharmaceuticals demo data is NOT pre-loaded. Decide whether to:
  - Pre-load Coco data via a notebook/workbook on startup
  - Or document that freshstart is for building from scratch (not a demo environment)

---

## Completed

- [x] Egeria-backed authentication (no SQLite, no email, no self-registration)
  - Portal authenticates directly against Egeria `POST /api/token`
  - `CREDENTIALS_EXPIRED` response triggers forced password-change form inline on login page
  - JWT session cookie includes Egeria bearer token for admin API calls
  - Admin role controlled by `EGERIA_ADMIN_USERS` env var
- [x] Login page (`demo-login.html`) — user ID + password, inline CREDENTIALS_EXPIRED flow
- [x] Portal hub (`demo-portal.html`) — no persona picker; org name from API; admin tile gated by role
- [x] Admin panel (`demo-admin.html`) — Egeria Users tab (create/edit/disable/reset/delete) + Config tab
- [x] Profile page (`demo-profile.html`) — view/edit Egeria profile, change password
- [x] `demo_auth_handler.py` — full rewrite for Egeria-backed auth; SecurityOfficer admin routes; my-profile proxy; runtime config JSON
- [x] `demo_config.py` — stripped of DB/email config; added `EGERIA_PLATFORM_URL`, `EGERIA_VIEW_SERVER`, `EGERIA_ADMIN_USERS`, `SITE_URL`
- [x] `egeria-freshstart.yaml` — removed SMTP/bootstrap env vars; added `EGERIA_ADMIN_USERS`, `EGERIA_ORG_NAME`; fixed `::` YAML quoting bug in uvicorn command
- [x] `pyegeria_handler.py` — removed `/register` route; auth router always included (not gated on DEMO_MODE); added `/profile` route; removed all `demo_db` lazy imports
- [x] `type_system_handler.py` — auth guard uses `get_current_user(request)` (no DB dependency)
- [x] `demo-mode.md` — complete rewrite for Egeria-backed auth architecture
- [x] `README.md` — added Portal and Authentication section
- [x] Organisation name resolution (application.properties → EGERIA_ORG_NAME env var → "Egeria")
- [x] MCP mount ordering fix (mount at "/" moved to end of pyegeria_handler.py)
- [x] type-explorer.html auth guard redirects to /login
