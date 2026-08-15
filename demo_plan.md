# Egeria Explorer — Demo Mode Planning Document

**Status**: Active design iteration — decisions being locked  
**Scope**: QuickStart compose config; FreshStart unchanged  
**Authors**: Dan Wolfson + Claude  
**Last updated**: 2026-05-24

---

## 1. Goals

Turn the QuickStart deployment of Egeria Explorer into a compelling, self-service demo environment while keeping the same codebase usable as a plain metadata-management interface for anyone running their own local copy.

Core objectives:
- Let visitors experience Egeria through the lens of a real business story (Coco Pharmaceuticals) without needing prior Egeria knowledge.
- Make the demo safe to expose publicly — authenticated, rate-limited, and self-resetting.
- Keep the QuickStart image usable as a non-demo local tool by toggling demo mode off via config.
- Leave FreshStart completely untouched.

---

## 2. The Four-Interface Landscape

| Interface | Public port | Internal | Current role | Demo-mode role |
|-----------|-------------|----------|-------------|----------------|
| Apache (static site) | :8085 | :8085 | Docs, Dr. Egeria docs, rendered reports | **Entry point** — landing page, registration, navigation hub |
| Egeria Explorer (FastAPI) | :8085/egeria-explorer | :8000 | Metadata exploration SPA | **Post-login** — persona picker + Explorer tabs + persona badge |
| Jupyter | :7888 | :7888 | Sample notebooks, local workbooks | Demo: curated story notebooks; local: full working environment |
| Egeria Advisor | (not in compose yet) | :8001 (planned) | Separate FastAPI app (in development) | Keep separate; future: `/advisor` tab in Explorer |

### The existing proxy architecture (already in place)

Apache on :8085 is already a reverse proxy for the FastAPI app on :8000. The `fastapi-proxy.conf` already routes:

```
:8085/                    →  Apache htdocs (static content)
:8085/egeria-explorer     →  pyegeria-web:8000/egeria-explorer
:8085/api/*               →  pyegeria-web:8000/api/*
:8085/dr-egeria/process   →  pyegeria-web:8000/dr-egeria/process
```

**This solves the session continuity problem.** The browser only ever sees one origin (`:8085`). Cookies set by FastAPI are on that origin. Registration forms POST to `/api/auth/*` on the same origin. No CORS issues, no cross-origin token passing.

New routes to add for demo mode:
```
:8085/admin               →  pyegeria-web:8000/admin
:8085/login               →  pyegeria-web:8000/login
:8085/register            →  pyegeria-web:8000/register  (or serve as static from Apache)
```

### Public deployment: TLS

For the public instance, TLS is required. Two options:

**Option A — Apache mod_ssl + Let's Encrypt certbot**  
Add `mod_ssl` to the Apache Docker image. Mount the cert from a certbot container or pre-generated cert. Straightforward but requires the Apache image to change.

**Option B — nginx container for TLS termination (recommended)**  
Add a thin nginx container that handles TLS and forwards to Apache on :8085. Apache is unchanged. Cert managed by a certbot sidecar. Standard pattern, cleanest separation.

> **Q18 (Dan):** Preference for TLS approach — mod_ssl in Apache or nginx sidecar? For V1 development (localhost), TLS is not needed. This only matters for the public deployment.

### EgeriaAdvisor port

Currently the FastAPI Explorer app (`pyegeria-web`) runs on :8000. EgeriaAdvisor is also FastAPI and currently on :8000 in its own deployment. When EgeriaAdvisor is added to the QuickStart compose, it will need a different port — :8001 is the natural choice — with an Apache proxy rule at `/advisor`.

---

## 3. Deployment Modes

Controlled by `DEMO_MODE` in `docker-compose.yml`.

### 3a — Public Demo Instance (`DEMO_MODE=true`)

- Hosted publicly (e.g., `demo.pdr-associates.com`) on port 443 (TLS)
- Pre-populated with Coco Pharmaceuticals environment
- Registration + email verification required before accessing Explorer
- Persona picker after login
- Data resets on admin-configurable schedule
- Dr. Egeria Execute cap: configurable (default `validate` for users, `process` for admins)
- Landing page at `/` also visible without login (public-facing marketing/story page)

### 3b — Local / Personal Instance (`DEMO_MODE=false` or unset)

- Anyone running QuickStart locally from the repo
- Landing page at `/` remains (informational, no auth required — can be a useful local homepage)
- Explorer opens directly at `/egeria-explorer` — no login required
- No persona picker, no reset schedule
- Full Dr. Egeria Execute (`process`) for all
- FreshStart always behaves this way regardless of DEMO_MODE

### 3c — FreshStart

Unchanged. No demo layer. DEMO_MODE is irrelevant.

---

## 4. Decisions Locked

| # | Decision |
|---|----------|
| D1 | **Auth V1**: email + password only. No OAuth. Can add in V2. |
| D2 | **Session lifetime**: 2 hours for regular users; 7 days for admins. |
| D3 | **Roles**: two roles only — `user` (default) and `admin`. Admins manually assigned. |
| D4 | **Admin panel**: separate page at `/admin`, served by FastAPI, protected by role check. |
| D5 | **Dr. Egeria cap**: admin-configurable per deployment. Default `validate` public; default `process` local. |
| D6 | **User account storage**: `demo` schema in the existing Egeria Postgres instance. |
| D7 | **Reset mechanism**: stop Egeria container → drop schema → restart → archive auto-loads. |
| D8 | **Guided tour Level 2** (narrative scenarios): V2. Sourced from Jupyter notebooks + Coco docs. |
| D9 | **Personas**: full Coco cast from egeria-project.org/practices/coco-pharmaceuticals/personas/. All shown in picker; starter set highlighted. |
| D10 | **Coco data**: all personas have meaningful data in QuickStart. Content pack: egeria-project.org/content-packs/coco-content-pack/overview |
| D11 | **Event logging**: `events` table in `demo` schema. Log registration, login, persona select, tab views. |
| D12 | **Privacy policy**: simple one-page static policy, linked from registration form. |
| D13 | **Session continuity**: already solved by existing Apache proxy. Browser sees one origin (:8085). |
| D14 | **Landing page in local mode**: stays, shown at `/`, informational (no auth wall). |
| D15 | **Ports**: Explorer FastAPI on :8000 internally, exposed via Apache on :8085. EgeriaAdvisor will use :8001 when added. |

---

## 5. Authentication & User Management

### Database schema (`demo` schema in existing Postgres)

```sql
CREATE TABLE demo.users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name  TEXT NOT NULL,
    org           TEXT,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,          -- bcrypt
    role          TEXT DEFAULT 'user',    -- 'user' | 'admin'
    verified      BOOLEAN DEFAULT false,
    verify_token  TEXT,
    reset_token   TEXT,
    reset_expires TIMESTAMPTZ,
    created_at    TIMESTAMPTZ DEFAULT now(),
    last_login    TIMESTAMPTZ
);

CREATE TABLE demo.events (
    id         BIGSERIAL PRIMARY KEY,
    user_id    UUID REFERENCES demo.users(id),
    event_type TEXT NOT NULL,    -- 'register' | 'verify' | 'login' | 'persona_select' | 'tab_view' | 'reset'
    detail     JSONB,            -- e.g. {"persona": "erinoverview", "tab": "glossary"}
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE demo.config (
    key   TEXT PRIMARY KEY,
    value TEXT
);
-- Seed rows: reset_interval_hours=24, directive_cap=validate,
--            session_lifetime_user=7200, session_lifetime_admin=604800
```

### FastAPI auth routes (`/api/auth/*`)

| Route | Method | Description |
|-------|--------|-------------|
| `/api/auth/register` | POST | Create account; send verification email |
| `/api/auth/verify/{token}` | GET | Activate account via email link |
| `/api/auth/login` | POST | Return JWT |
| `/api/auth/logout` | POST | Invalidate token |
| `/api/auth/forgot-password` | POST | Send password-reset email |
| `/api/auth/reset-password/{token}` | POST | Set new password |
| `/api/auth/me` | GET | Current user info (requires JWT) |

### SMTP config (env vars)

```
SMTP_HOST=mail.pdr-associates.com
SMTP_PORT=587
SMTP_USER=demo@pdr-associates.com
SMTP_PASSWORD=...
SMTP_FROM=demo@pdr-associates.com
```

### Rate limiting (`slowapi`)

- `/api/auth/register`: 5 / hour / IP
- `/api/auth/login`: 10 / hour / IP
- `/api/auth/forgot-password`: 3 / hour / IP

---

## 6. Request Flow in DEMO_MODE

```
Browser → Apache :8085
  │
  ├── GET /                    → Apache serves landing.html (static)
  ├── GET /register            → Apache serves register.html (static form)
  ├── POST /api/auth/register  → Apache proxies → FastAPI → sends verification email
  ├── GET /api/auth/verify/:t  → Apache proxies → FastAPI → activates account
  ├── POST /api/auth/login     → Apache proxies → FastAPI → returns JWT in cookie
  │
  ├── GET /egeria-explorer     → Apache proxies → FastAPI
  │     FastAPI checks JWT cookie
  │     ├── No JWT / expired   → redirect to /login
  │     └── Valid JWT          → serve Explorer SPA
  │           └── First visit  → show persona picker modal
  │
  └── GET /admin               → Apache proxies → FastAPI
        FastAPI checks JWT + role == 'admin'
        ├── Not admin          → 403
        └── Admin              → serve admin panel
```

---

## 7. Persona System

### How persona login works (security model)

When a user selects a persona, the FastAPI backend generates an Egeria bearer token for that persona's Egeria user ID. **The Egeria password never leaves the server.**

Flow:
1. Browser: `POST /api/auth/select-persona` with `{"persona": "erinoverview"}`
2. FastAPI: looks up persona credentials from server-side config file (`personas.json`)
3. FastAPI: calls `mgr.create_egeria_bearer_token(user_id, password)` for that persona
4. FastAPI: stores bearer token in user's JWT claims (or server-side session)
5. All subsequent Egeria API calls on the backend use this persona's bearer token

`personas.json` (mounted as a volume, not baked into the image):
```json
{
  "erinoverview":  {"password": "secret", "display_name": "Erin Overview",  "role": "Data Steward"},
  "peterprofile":  {"password": "secret", "display_name": "Peter Profile",  "role": "CDO"},
  "calliequartile":{"password": "secret", "display_name": "Callie Quartile","role": "Data Scientist"},
  "garygeeke":     {"password": "secret", "display_name": "Gary Geeke",     "role": "IT Infrastructure"},
  "ivorpadlock":   {"password": "secret", "display_name": "Ivor Padlock",   "role": "Security Officer"}
}
```

> **Q15 (Dan):** Are all Coco persona passwords `"secret"`, or do they vary? This goes into `personas.json` server-side.

### Persona card content

Each card in the picker shows:
- Name + Coco title
- 2-sentence backstory (sourced from egeria-project.org persona profiles)
- "What you'll see" — 3 bullets of Explorer highlights
- Badge: Starter / Business / Technical
- Link: "Full profile →" (to egeria-project.org)
- [Enter as {Name}] button

Starter set highlighted (coloured border); remaining Coco personas shown below in a collapsible "More personas" section.

> **Q14 (Dan):** Should non-highlighted personas be in a "More personas" collapsible, or shown equally alongside the highlighted ones?

### Persona badge in Explorer header (DEMO_MODE=true only)

```
[Egeria Explorer]     👤 Erin Overview — Data Steward     [Switch Persona]  [Log Out]
```

---

## 8. Data Reset Mechanism

### What reset means

Stop Egeria container → drop Egeria schema in Postgres → restart container → Coco archive auto-loads on startup.

The Egeria platform is **offline during reset**. Duration depends on archive load time.

> **Q17 (Dan):** How long does the Coco archive take to load on a clean Egeria restart? This determines whether a pre-notification warning is essential (it is if > ~2 minutes).

### Reset implementation options

The FastAPI app needs to trigger a container restart. Two approaches:

**Option A — Docker socket mount (standard pattern)**
```yaml
# in docker-compose.yml
pyegeria-web:
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```
FastAPI calls `docker.from_env().containers.get("egeria-main").restart()` via the Python Docker SDK. Clean, no subprocess.

**Option B — Reset script via subprocess**
FastAPI calls a shell script (`/app/scripts/reset-egeria.sh`) that does `docker compose restart egeria-main`. The script is mounted as a volume. Avoids Docker socket but requires careful path management.

> **Q16 (Dan):** Is mounting the Docker socket into the FastAPI container acceptable for your deployment? It's a standard pattern but does give that container broad Docker control — worth being deliberate about.

### Admin reset controls

Stored in `demo.config`, changeable at runtime:

| Config key | Values | Default |
|-----------|--------|---------|
| `reset_interval_hours` | `0` (never), `6`, `12`, `24`, `168` | `24` |
| `reset_notify_minutes` | minutes of advance warning shown to users | `30` |
| `last_reset_at` | ISO timestamp | set on each reset |

Admin panel controls:
- Interval dropdown (Never / 6h / 12h / Daily / Weekly)
- **Reset Now** button + confirmation modal ("This will take the Egeria platform offline for ~N minutes")
- Last reset + next reset timestamps
- Pre-reset banner shown to all active users at `reset_notify_minutes` before scheduled reset

---

## 9. Admin Panel (`/admin`)

Separate page at `/admin`, served by FastAPI. JWT required + `role == 'admin'`.

Sections:

**Reset Management** — interval, last/next timestamps, Reset Now, notify config

**User Management** — paginated table (name, org, email, role, created, last login, verified); promote/demote; disable/delete; pending verifications

**Usage Analytics**
- Registrations over time
- Daily logins
- Most-selected personas
- Most-viewed Explorer tabs
- Dr. Egeria Execute usage by directive

**System Config** — directive cap for `user` role; session lifetimes; rate limits; SMTP test

**Environment Status** — Egeria platform health (live poll); active session count; reset state

---

## 10. Landing Page

Lives at `/` — Apache serves a static `index.html` from htdocs. When `DEMO_MODE=false`, this page is an informational homepage (no auth wall, links to Explorer and Jupyter directly). When `DEMO_MODE=true`, it adds Register/Login CTAs.

A single `index.html` handles both modes cleanly: embed a `<script>` that checks a `DEMO_MODE` meta tag (injected at build time or read from a config endpoint) and shows/hides the auth elements accordingly.

### Content outline

**Hero** — Headline + 2-sentence Egeria intro + [Register Free] / [Log In] CTAs

**Coco Pharmaceuticals story** — Brief narrative + link to egeria-project.org/practices/coco-pharmaceuticals/

**What's inside** — "Explore a pre-loaded environment with N glossary terms, M data assets, K solution blueprints, J personas" + Explorer screenshot

**The four surfaces** — Cards linking to Explorer (`/egeria-explorer`), Jupyter (`:7888`), Apache docs (`/docs`), and Egeria Advisor (when available)

**Footer** — Privacy Policy link, GitHub repo link, contact

---

## 11. Implementation Phases

| Phase | Description | Effort | Depends on |
|-------|-------------|--------|------------|
| 0 | `DEMO_MODE` env flag — FastAPI reads it, gates auth middleware | XS | — |
| 1 | `demo` schema + SQLAlchemy models in Postgres | S | 0 |
| 2 | FastAPI auth routes (register, verify, login, logout, JWT) | M | 1 |
| 3 | Rate limiting (`slowapi`) + SMTP email verification | S | 2 |
| 4 | Apache proxy rules for `/admin`, `/login`, `/register` | XS | — |
| 5 | Landing page (`index.html`) — static, DEMO_MODE-aware | M | 0 |
| 6 | Persona picker page + `POST /api/auth/select-persona` | M | 2, Q15 |
| 7 | Persona badge + Switch Persona in Explorer header | S | 6 |
| 8 | Privacy policy page | XS | — |
| 9 | Reset scheduler (APScheduler) + reset task | M | Q16, Q17 |
| 10 | Admin panel — reset controls + user management | M | 2, 9 |
| 11 | Admin panel — usage analytics + event logging | M | 10 |
| 12 | Guided tour Level 1 (Intro.js via CDN) | S | 6 |
| V2 | Guided tour Level 2 — narrative scenario player | L | Jupyter notebooks |
| Deploy | TLS setup (Apache mod_ssl or nginx sidecar) | S | Q18, Q10, Q11 |

**Phases 0–8**: working public demo.  
**Phases 9–11**: operationally safe (reset + admin).  
**Phase 12**: polish.

---

## 12. Open Questions

| # | Question | Blocks |
|---|----------|--------|
| Q14 | Non-highlighted personas in picker: collapsible "More personas" section, or all equal? | Phase 6 |
| Q15 | Are all Coco persona Egeria passwords `"secret"`, or do they vary? | Phase 6 |
| Q16 | Is mounting the Docker socket into the FastAPI container acceptable? | Phase 9 |
| Q17 | How long does the Coco archive load take on a clean Egeria restart? | Phase 9 |
| Q18 | TLS preference: Apache mod_ssl or nginx sidecar? | Deploy phase |
| Q10 | Hosting target for the public instance? Cloud provider? | Deploy phase |
| Q11 | Domain name for the public demo? | Deploy phase |
Q14: Collapsible
Q15: all secret---
Q16: Docker socket is acceptable
Q17: Coco archive load time is ~5 minutes
Q18: nginx sidecar preferred for TLS termination
Q10: My own local server for now; open to cloud hosting in the future if needed
Q11: `demo.pdr-associates.com` (or similar)


## 13. Iteration Notes

**2026-05-24 — Round 1**  
Q1–Q9 answered. Key outcomes: two roles (user/admin), separate `/admin` page, reset via container restart, 2h/7d sessions, Level 2 tour to V2, all Coco personas in picker, `demo` schema in existing Postgres.

**2026-05-24 — Round 2**  
Discovered existing architecture: Apache on :8085 already reverse-proxies FastAPI on :8000. Session continuity already solved — browser sees one origin. Landing page stays in local mode (informational). EgeriaAdvisor will move to :8001 when added to compose. New questions: Q14–Q18 (persona picker layout, Coco passwords, Docker socket, reset duration, TLS approach).
