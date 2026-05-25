<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Freshstart Backlog

Items completed in quickstart that still need to be applied or adapted for freshstart.

---

## Pending

### Demo mode parity
- [ ] **SITE_URL** — update `egeria-freshstart.yaml` `SITE_URL` to the correct public URL when deploying publicly (currently `http://localhost:8086`)
- [ ] **SMTP** — configure `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` in `compose-configs/egeria-freshstart/.env` for email verification
- [ ] **Admin bootstrap** — set `ADMIN_BOOTSTRAP_EMAIL` and `ADMIN_BOOTSTRAP_PASSWORD` in `.env` before first run
- [ ] **JWT_SECRET** — set a real random value in `.env` before public deployment

### Portal / Apache config
- [ ] Freshstart uses quickstart's `httpd.conf` and `fastapi-proxy.conf` (via `context: ../egeria-quickstart`). The portal proxy rules, `/local` alias, and root redirect added to `fastapi-proxy.conf` are already shared. Verify they work on freshstart's port 8086.
- [ ] Freshstart static site volume mount needs updating to match quickstart pattern (`site:/usr/local/apache2/htdocs/local`) — currently `freshstart-apache-web` mounts at `htdocs` root. **Update `egeria-freshstart.yaml` apache volumes.**

### PostgreSQL demo schema
- [ ] Run `CREATE SCHEMA IF NOT EXISTS demo; GRANT ALL ON SCHEMA demo TO egeria_admin, egeria_user;` against the freshstart postgres if it uses a separate DB instance. Quickstart's `init_egeria.sql` already includes this for new deployments.

### SSL
- [ ] Configure Apache SSL for freshstart port 8086 once quickstart SSL is proven (same cert, different VirtualHost port).

### Data loading
- [ ] Freshstart ships empty — unlike quickstart, the Coco Pharmaceuticals demo data is NOT pre-loaded. Demo mode personas will work for auth/persona selection but Egeria Explorer will show an empty metadata store. Decide whether to:
  - Pre-load Coco data via a notebook/workbook on startup
  - Or document that freshstart is for building from scratch (not a demo environment)

---

## Completed (synced from quickstart)

- [x] Demo mode infrastructure (demo_config, demo_db, demo_auth_handler, personas.json)
- [x] Admin bootstrap from `.env` on startup
- [x] bcrypt fix (passlib → direct bcrypt)
- [x] Portal hub page (demo-portal.html)
- [x] Login/register/admin/privacy pages
- [x] Persona picker with profile links
- [x] MCP mount ordering fix (mount at "/" moved to end of pyegeria_handler.py)
- [x] type-explorer.html persona redirect to /portal
- [x] demo-login.html redirect to /portal after login
