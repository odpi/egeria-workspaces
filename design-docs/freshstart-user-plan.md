# Freshstart User Plan

## Background

A freshstart environment starts empty — no pre-loaded data, no pre-created users. Unlike quickstart (which has a dual-layer auth system with a separate SQLite user store), freshstart uses **Egeria as the single user store**. The Egeria platform's SecurityOfficer API governs all accounts, roles, groups, and zones. The portal authenticates directly against Egeria — there is no separate registration flow and no SQLite database.

---

## Architecture: Single-Layer Authentication

```
User enters credentials → Portal calls Egeria bearer token endpoint
                        → Success: portal issues JWT session cookie
                        → CREDENTIALS_EXPIRED: redirect to password-change form
                        → Failure: show error
```

The portal's `demo_auth_handler.py` needs to be reworked for freshstart:

| Quickstart | Freshstart |
|---|---|
| Login validates against SQLite `users` table | Login calls `create_egeria_bearer_token` |
| Self-registration form (`/register`) | No registration — admin creates all accounts |
| Email verification flow | No email — credentials delivered out of band |
| SQLite `users` table tracks portal sessions | Egeria is the source of truth; portal issues JWT on successful Egeria auth |

The portal JWT session cookie works the same way — issued after successful Egeria auth, used to protect portal routes. The difference is what backs the credential check.

---

## Portal Structure

The portal header greeting reads **"Welcome to \<organization\> — Egeria Environment"** where the organisation name is read from `platform.organization.name` in `application.properties`. This requires a new API endpoint that reads this value from the Egeria platform at startup.

| Section | Quickstart | Freshstart |
|---|---|---|
| Header greeting | "Egeria Demo Environment" | "Welcome to \<org\> — Egeria Environment" |
| Header chip | Persona name + role | Logged-in user's display name |
| Main CTA | Choose Persona | None — users go straight to tools |
| Admin entry | Link in header right | Prominent tile in the app grid (admin only) |
| Extra page | — | My Profile (`/profile`) |
| Tool tiles | Explorer, Jupyter, Coco Web, Advisor | Explorer, Jupyter, Advisor (no Coco Web) |

---

## Bootstrap Sequence

When freshstart starts for the first time:

1. The Egeria platform initialises with a built-in `bootstrap` account (password: `secret`).
2. The portal admin logs in with `bootstrap` / `secret`.
3. If `userAccountStatus` is `CREDENTIALS_EXPIRED`, the portal redirects to the password-change form which calls `create_egeria_bearer_token` with `newPassword`.
4. Admin changes the bootstrap password, then proceeds to the **Admin → Egeria Users** tab.
5. Admin creates accounts for each user (see User Creation below).
6. Admin shares temporary credentials out of band.

---

## User Accounts

### Account statuses

| Status | Meaning |
|--------|---------|
| `CREDENTIALS_EXPIRED` | Set on all new accounts — forces password change on first login |
| `ACTIVE` | Normal working state, set automatically after first password change |
| `DISABLED` | Account blocked; user cannot log in |

### Account types (informational only — no effect on permissions)

`EMPLOYEE` · `CONTRACTOR` · `DIGITAL` · `EXTERNAL`

These appear as a dropdown in the create-user form to help admins categorise accounts. They do not affect Egeria access.

### Security roles and groups

Roles and groups are **pre-defined** in the Egeria secrets store (catalogued by the Secrets Store Cataloguer integration connector). The admin panel queries them dynamically to populate dropdowns:

```
# Find security roles
POST /servers/{viewServer}/api/open-metadata/security-officer/collections/by-search-string
{ "class": "SearchStringRequestBody", "metadataElementTypeName": "SecurityRole", "graphQueryDepth": 0 }

# Find security groups
POST /servers/{viewServer}/api/open-metadata/security-officer/collections/by-search-string
{ "class": "SearchStringRequestBody", "metadataElementTypeName": "SecurityGroup", "graphQueryDepth": 0 }
```

Zones (`defaultZones`, `publishZones`) are free-text fields in the create form.

---

## User Creation

### Phase 1 — Admin creates the Egeria account

```python
SecurityOfficer.set_user_account(
    server_name, url, user_id,
    body={
        "class": "UserAccountRequestBody",
        "userAccount": {
            "class": "OpenMetadataUserAccount",
            "userId": "jsmith",
            "userName": "Jane Smith",
            "userAccountType": "EMPLOYEE",      # dropdown
            "givenName": "Jane",
            "surname": "Smith",
            "email": "jane.smith@example.com",
            "securityRoles": ["data-analyst"],  # from role dropdown
            "securityGroups": ["research-team"],# from group dropdown
            "otherProperties": {
                "defaultZones": ["general"],
                "publishZones": ["general"]
            },
            "userAccountStatus": "CREDENTIALS_EXPIRED",
            "secrets": {
                "clearPassword": "TempPass123!"  # admin sets, shares out of band
            }
        }
    }
)
```

Admin shares `userId` + `clearPassword` with the user (out of band — email, Slack, etc.).

### Phase 2 — User changes password and creates profile

**First login** triggers a forced password-change screen. The portal calls:

```python
# Validates old credentials AND sets new password
create_egeria_bearer_token(user_id, server_name, url, body={
    "class": "PasswordRequestBody",
    "userId": "jsmith",
    "password": "TempPass123!",
    "newPassword": "MyNewSecurePass!"
})
```

On success, the portal issues a JWT session cookie and redirects to the portal hub.

**Profile creation** is self-service via the My Profile page (`/profile`):

```python
MyProfile.add_my_profile(
    server_name, url, user_id,
    body={
        "class": "NewElementRequestBody",
        "isOwnAnchor": True,
        "properties": {
            "class": "PersonProperties",
            "qualifiedName": "jsmith",
            "displayName": "Jane Smith",
            "givenNames": "Jane",
            "surname": "Smith",
            "jobTitle": "Data Analyst",
            "description": "",
            "additionalProperties": {}
        },
        "forLineage": False,
        "forDuplicateProcessing": False
    }
)
```

---

## Admin Panel

The freshstart admin panel has three tabs (no Portal Users tab — Egeria is the single user store):

| Tab | Content | Actions |
|-----|---------|---------|
| **Egeria Users** | All platform user accounts | Create, Edit roles/groups/zones, Disable, Delete |
| **Config** | Runtime config key/value pairs | Edit |

### Egeria Users — Create form fields

| Field | Type | Notes |
|-------|------|-------|
| User ID | Text | Required; Egeria userId |
| Display name | Text | Full name |
| Given name / Surname | Text | |
| Email | Text | |
| Account type | Dropdown | EMPLOYEE, CONTRACTOR, DIGITAL, EXTERNAL |
| Security roles | Multi-select | Populated from Egeria SecurityRole query |
| Security groups | Multi-select | Populated from Egeria SecurityGroup query |
| Default zones | Text (comma-separated) | |
| Publish zones | Text (comma-separated) | |
| Temporary password | Password | Shown in clear once; admin copies and shares |

### Egeria Users — Per-user actions

- **Edit** — update roles, groups, zones (re-calls `set_user_account`)
- **Disable** — sets `userAccountStatus: DISABLED`
- **Reset password** — admin sets a new temporary password, status reverts to `CREDENTIALS_EXPIRED`
- **Delete** — removes the user account from Egeria

---

## My Profile Page (`/profile`)

A self-service page available to all logged-in users. Calls `MyProfile` API to:

- View current profile (display name, job title, description)
- Edit and save profile fields
- Change password (calls `create_egeria_bearer_token` with old + new password)

---

## Files to Create / Modify

| File | Action |
|------|--------|
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo_auth_handler.py` | Rework login to authenticate against Egeria; remove register/verify/SMTP endpoints; add forced-password-change flow |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo-portal.html` | Remove persona section; add org-name greeting; admin tile in grid |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo-admin.html` | Replace Portal Users tab with Egeria Users tab; role/group dropdowns; create/edit/disable/delete actions |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo-login.html` | Update branding; add CREDENTIALS_EXPIRED redirect to password-change form |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo-profile.html` | New — My Profile self-service page |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo_db.py` | **Delete** — no SQLite at all; Egeria audit log replaces the event log |
| `compose-configs/egeria-freshstart/PyegeriaWebHandler/demo_config.py` | Remove SMTP/Resend vars; keep JWT and site URL |
| `compose-configs/egeria-freshstart/egeria-freshstart.yaml` | Add JWT env vars; SSL port + cert volume (opt-in, same pattern as quickstart) |
| `compose-configs/egeria-freshstart/.env` | `JWT_SECRET`, Egeria platform URL/server |
| `compose-configs/egeria-freshstart/BACKLOG.md` | Update / close backlog items as work completes |

---

## Decisions

| Decision | Resolution |
|----------|-----------|
| **Organisation name** | Read `application.properties` directly at startup — it's a volume-mounted static file. `RuntimeManager.get_platform_report` exists but is heavier than needed for a single config value. |
| **Event log** | Drop the Events tab — Egeria's built-in audit log already captures platform activity. No SQLite needed at all. |
| **JWT secret** | Same `.env` pattern as quickstart: `JWT_SECRET` in `.env`, substituted into the yaml via `${JWT_SECRET:-}`. |
| **SSL** | Self-signed cert for initial localhost deployment. Proper cert + domain name as a future enhancement (same `fastapi-ssl.conf` opt-in mechanism as quickstart). |

With the Events tab removed, `demo_db.py` is deleted entirely — no SQLite at all in freshstart.

---

*Last updated: 2026-05-25*
