# Egeria Workspaces — Backlog

Consolidated work list. Update status when items start or finish.  
Status: `open` · `in-progress` · `done` · `deferred`

---

## Prioritization (workstream level)

`My Pri` = Claude's recommendation. `Your Pri` is blank — fill in `H`/`M`/`L` (or a rank) to steer.
Rationale favours **leverage** (unblocks other work) and **finishing shipped features** over net-new
exploration. Items can run concurrently when they touch different files; watch the noted dependencies.

| Workstream | Items | My Pri | Your Pri | Why / dependency |
|------------|-------|:------:|:--------:|------------------|
| Shared codebase unification | SHARE-1, SHARE-2 | **H** |  | Highest leverage — dual quickstart/freshstart copies tax *every* future change; divergence only grows. Do before more feature work. |
| pyegeria comment-update bug | PY-4 | **H** |  | Breaks an already-shipped feature (comment edit). Small, self-contained. |
| Report rendering | RR-1 → RR-5 | **H** |  | Core demo value; RR-1/RR-2 unblock RR-3/4/5. Sequential within the group. |
| Data preview polish | DP-2, DP-3, DP-4 | **M** |  | User-facing, independent, low risk; good "concurrent" fillers. |
| my-egeria additional apps | ME-8, ME-9 | **M** |  | TUI now renders end-to-end — momentum is here. Follows the proven ME-2..6 pattern. |
| ProjectExplorer integration | PORT-7, LF-1 → LF-4 | **M** |  | Needs the LF-AI service stood up first; port `8830` already reserved. |
| QuickStart demo polish | QS-1, QS-3, QS-4 | **M** |  | Demo-facing; QS-1/QS-3 are quick wins, QS-4 (reset) is bigger. |
| Performance | PERF-1, PERF-2 | **M** |  | Real pain on deep catalog trees; investigate after correctness work. |
| Report specs authoring | RS-1, RS-2, RS-3 | **L** |  | Large, spec-still-TBD; defer until RR rendering lands. |
| Journals / feedback extras | FB-4 | **L** |  | Exploratory; storage model undecided. |
| Demo analytics / extras | QS-5, QS-6, QS-7 | **L** |  | Nice-to-have; QS-7 already deferred. |
| my-egeria V2 (multi-user) | ME-10, ME-11, ME-12 | **L** |  | Deferred until single-persona path is fully proven. |
| pyegeria DataDesigner/SA bugs | PY-1, PY-2, PY-3 | **L** |  | Have working local workarounds; fix upstream opportunistically. |

**Concurrency advice:** SHARE-1/2 first (or you fight merge pain on everything after). PY-4, DP-*,
and ME-8/9 are independent and safe to interleave. RR-* must go in order. Avoid starting RS-* and
FB-4 until the higher-leverage items clear.

---

## Ports & Networking  🔴 HIGH PRIORITY

**Status (2026-06-03): IMPLEMENTED for all existing services** (PORT-1…PORT-6, PORT-8 done).
Only PORT-7 (ProjectExplorer, a not-yet-built service) remains open. Compose files, Apache
`ServerName`, `SITE_URL`, `MY_EGERIA_PUBLIC_URL`, portal links, `gen-env.sh`, `demo_config.py`,
and all READMEs/docs updated. The full table also lives in the repo-root `README.md`
(*Host port allocation*).

**Problem:** the quickstart `pyegeria-web` service publishes host port **8000**, which
collides with other applications commonly running on a developer's machine and is
interfering with the environment. We need to move off 8000 — and, while we're at it,
adopt a consistent, conflict-free host-port scheme across both environments.

**Adopted scheme:** **quickstart = 88xx**, **freshstart = 78xx**, with the **same last
two digits = same function** in both envs (e.g. jupyter = `88` → quickstart `8888`,
freshstart `7888`). Only the published **host** port changes; container-internal ports
stay as-is (the Apache proxy reaches services container-to-container, so it is
unaffected). Rationale for 88xx/78xx over 9xxx/8xxx: the 9xxx range collides with
Elasticsearch (9200), Prometheus (9090), MinIO/SonarQube/ClickHouse (9000),
node_exporter (9100) and our own egeria-main 9443; and an 8xxx/9xxx scheme forces
pyegeria-web onto the poisoned 8000/9000. The 88xx/78xx blocks are clean (only caveat:
8888 is Jupyter's own default) and never overlap the fixed services.

**Fixed — do NOT renumber:** egeria-main (quickstart 9443/5005, freshstart 8443/5006),
shared kafka (9192–9194), shared postgres (5442).

### Current port map (host → container) — after renumbering

| Env | Service | Container | Host:Container | Notes |
|-----|---------|-----------|----------------|-------|
| quickstart | jupyter-hub | `quickstart-jupyter-work-full` | 8888:7888, 8889:5678 | notebook + debug |
| quickstart | egeria-main | `quickstart-egeria-main` | 9443:9443, 5005:5005 | platform + debug (fixed) |
| quickstart | pyegeria-web | `quickstart-pyegeria-web` | 8800:8000 | ✅ moved off 8000 |
| quickstart | apache-web | `quickstart-web-server` | 8885:8085 | portal entry point |
| quickstart | my-profile | `quickstart-my-profile` | 8820:8020 | my-egeria TUI (textual serve) |
| quickstart | obsidian | `obsidian-quickstart` | 8860:3000, 8861:3001 | optional |
| freshstart | jupyter-hub | `freshstart-jupyter-work-full` | 7888:7888, 7889:5678 | notebook + debug |
| freshstart | egeria-main | `freshstart-egeria-main` | 8443:8443, 5006:5005 | platform + debug (fixed) |
| freshstart | pyegeria-web | `freshstart-pyegeria-web` | 7800:8000 | renumbered |
| freshstart | apache-web | `freshstart-web-server` | 7885:8085 | portal entry point |
| shared-infra | openlineage-proxy | `egeria-shared-openlineage-proxy-backend` | 6000:6000, 6001:6001 | fixed |
| shared-infra | kafka | `egeria-shared-kafka` | 9192:9192, 9193:9193, 9194:9194 | fixed |
| shared-infra | postgres | `egeria-shared-postgres` | 5442:5442 | fixed (multi-schema) |
| quickstart | **ProjectExplorer** | *(TBD)* | **8830:8830** *(planned)* | new service — PORT-7 |

### Target host-port allocation (88xx / 78xx)

Format below is `host:container` — only the host (left) side changes; container ports stay.

| Function | Code | Quickstart (88xx) | Freshstart (78xx) | From (qs / fs) |
|----------|------|-------------------|-------------------|----------------|
| jupyter notebook | 88 | **8888**:7888 | **7888**:7888 | 7888 / 7889 |
| jupyter debug (debugpy) | 89 | **8889**:5678 | **7889**:5678 | 5678 / 5679 |
| pyegeria-web | 00 | **8800**:8000 | **7800**:8000 | 8000 / 8001 |
| apache portal | 85 | **8885**:8085 | **7885**:8085 | 8085 / 8086 |
| my-profile (my-egeria) | 20 | **8820**:8020 | *7820* (reserved) | 8020 / — |
| ProjectExplorer | 30 | **8830**:8830 | *7830* (reserved) | new |
| obsidian web / https | 60 / 61 | **8860**:3000 / **8861**:3001 | — | 3000,3001 / — |

Frees up the problem port **8000** and also vacates **8086** (InfluxDB default). The only
caveat: quickstart jupyter `8888` is Jupyter's own default — collides only if another
Jupyter runs on the host.

| # | Item | Status | Notes |
|---|------|--------|-------|
| PORT-1 | Move quickstart `pyegeria-web` off host port 8000 → **8800** | done | `8000:8000` → `8800:8000` in `egeria-quickstart.yaml`. Apache proxy container-internal (`pyegeria-web:8000`) so unaffected. |
| PORT-2 | Renumber freshstart `pyegeria-web` → **7800** | done | `8001:8000` → `7800:8000` in `egeria-freshstart.yaml`; `SITE_URL`, `gen-env.sh`, docs. |
| PORT-3 | Renumber jupyter-hub host ports | done | quickstart `8888`/`8889`; freshstart `7888`/`7889`; portal `jupyterUrl` links + docs. |
| PORT-4 | Renumber apache portal host ports → qs **8885**, fs **7885** | done | Compose, Apache `ServerName`, **`MY_EGERIA_PUBLIC_URL`** → `8885`, `serve_my_egeria.py` comment, READMEs, demo-mode.md. |
| PORT-5 | Renumber my-profile host port → **8820** | done | `8020:8020` → `8820:8020`; my-egeria proxy container-internal so unaffected. `7820` reserved for freshstart (ME-10). |
| PORT-6 | Renumber obsidian host ports → **8860 / 8861** | done | Compose + portal `_obsContainerUrl()`/Open-Obsidian button + demo-mode.md. |
| PORT-7 | Allocate + wire host port for ProjectExplorer → **8830** | open | New service (LF-AI project-explorer, see LF-1..4); needs compose service, proxy `<Location>` route, and a portal tile. `7830` reserved for freshstart. |
| PORT-8 | Repo-wide grep for hardcoded `:8000` / `:8085` / `localhost:80xx` | done | Swept compose/conf/html/py/sh/md; remaining `8085`/`8000`/`8020` references confirmed container-internal (vhost `*:8085`, `Listen 8085`, ProxyPass, `EXPOSE`, uvicorn `--port`). |

---

## Egeria Explorer — Data Preview

| # | Item | Status | Notes |
|---|------|--------|-------|
| DP-1 | Adjustable column widths in tabular dataset preview | done | Drag-to-resize on column right-edge handles; dotted separators |
| DP-2 | Row filtering in dataset preview | open | Filter bar above table |
| DP-3 | Row sorting in dataset preview | open | Click column header to sort |
| DP-4 | Search within table preview | open | Global text search across visible rows |

---

## Egeria Explorer — Feedback & Comments

| # | Item | Status | Notes |
|---|------|--------|-------|
| FB-1 | Egeria comments on property sheets | done | Glossary Term + Digital Product detail panes; type dropdown; history list |
| FB-2 | Likes + ratings on remaining detail panes | done | `EgeriaFeedbackWidget` now on all property detail panes. ReportSpecDetail excluded — pyegeria format specs have no Egeria GUID. |
| FB-3 | Comments (`EgeriaCommentsSection`) on remaining detail panes | done | `EgeriaCommentsSection` now on all property detail panes. ReportSpecDetail excluded — same reason as FB-2. |
| FB-4 | Journals — persistent per-element notes/log separate from Egeria comments | open | Exploratory; may be local storage or a separate Egeria NoteLog |

---

## Egeria Explorer — Report Rendering

Spec: `report-rendering-plan.md`

| # | Phase | Item | Status |
|---|-------|------|--------|
| RR-1 | 1 | GRAPH format → send DICT/JSON fallback (no unembeddable HTML) | open |
| RR-2 | 2 | `SmartReportRenderer` — tokenize output; render Mermaid/Vega-Lite fences; fix master-detail anchor links + bi-di nav | open |
| RR-3 | 3a | `VegaChart` component + unconditional vega-embed load | open |
| RR-4 | 3b | `AvailableCharts` — scan DICT results for `*BarGraph`/`*PieGraph` keys | open |
| RR-5 | 4 | `DictResultView` — spec-driven master-detail table with expand rows + auto-charts | open |

---

## Freshstart — Admin & User Management

| # | Item | Status | Notes |
|---|------|--------|-------|
| FS-1 | Admin edit user — show all current values; roles/groups as checkboxes (not multi-select highlights) | done | Checkbox lists implemented in demo-admin.html with pre-populated values |
| FS-2 | My Profile page (`/profile`) — self-service display name, job title, description + password change | done | `demo-profile.html` exists and is wired into the handler |
| FS-3 | Portal greeting reads org name from `application.properties` | done | `get_org_name()` in auth handler; `/api/platform/org-name` endpoint; portal fetches and renders it |
| FS-4 | Delete `demo_db.py` — no SQLite in freshstart | done | File no longer present |

---

## Egeria Explorer — Shared Codebase

`type-explorer.html` (7500 lines) and all backend handlers exist as separate copies under `egeria-quickstart/` and `egeria-freshstart/`. Currently ~38 lines of divergence in the HTML (mainly the connection form: quickstart shows URL+server+user+pwd; freshstart shows user+pwd only). Every new feature added to one must be manually synced to the other — this burden grows over time.

| # | Item | Status | Notes |
|---|------|--------|-------|
| SHARE-1 | Unify `type-explorer.html` — one canonical file served to both envs | open | Gate quickstart-only features (full connection form, demo-mode UI) via `/api/env` endpoint response. Current divergence is small (~38 lines) but will grow with each new feature. |
| SHARE-2 | Unify backend handlers across freshstart + quickstart | open | `digital_products_handler.py`, `egeria_feedback_handler.py`, etc. each have separate copies. Quickstart-only features (tree cache, demo auth hooks) should be env-gated rather than forked. |

---

## Egeria Explorer — Performance

| # | Item | Status | Notes |
|---|------|--------|-------|
| PERF-1 | Digital Product catalog tree load is slow — investigate query optimisation | open | `get_collection_members` called serially per container; `include_only_relationships` explored but not yet validated |
| PERF-2 | Evaluate server-side lazy loading for deep catalog trees | open | Return top-level only; fetch children on expand click |

---

## Egeria Explorer — Home Page

| # | Item | Status | Notes |
|---|------|--------|-------|
| HOME-1 | Reorganise Explorer cards into Act / Review / Reference groups matching the menu bar | done | Three labelled sections with blurb lines; cards reordered to match nav menu membership |

---

## Egeria Explorer — Projects

| # | Item | Status | Notes |
|---|------|--------|-------|
| PROJ-1 | Projects card + tab — list projects via `ProjectManager`; show project hierarchy and other dependencies | done | `project_handler.py` backend; `ProjectsView` + `ProjectDetail` in type-explorer; sidebar list + child project cards; search filters by name, description, classification |
| PROJ-2 | Classification-based project-kind display | done | `ProjectKindBadge` component with per-kind colours (Campaign=blue, StudyProject=green, PersonalProject=amber, Task=red, GlossaryProject=indigo); shown in sidebar list, detail header, and child cards; classification properties shown in expandable detail cards |

---

## Egeria Explorer — Report Specs & Subscriptions

| # | Item | Status | Notes |
|---|------|--------|-------|
| RS-1 | Building / editing Report Specs from the UI | open | Large feature; spec TBD — form-driven composition of report specs |
| RS-2 | Subscribe to a Digital Product | open | Exploratory — notification or watch mechanism when product changes |
| RS-3 | Filter Report Specs list by Perspective and/or Question | open | Orthogonal selection axis — user picks a perspective (e.g. governance, lineage) or a question and sees only relevant report specs; complements existing name/description search |

---

## QuickStart Demo Mode

Spec: `demo_plan.md`

| # | Item | Status | Notes |
|---|------|--------|-------|
| QS-1 | Portal — link to egeria-project.ai docs and odpi GitHub repos | open | From `quickstart-demo-items.md` |
| QS-2 | Portal — prompt users to star egeria / egeria-workspaces / egeria-python repos | open | Best-practice UX for this TBD |
| QS-3 | Persona picker page — link to Coco Pharmaceuticals overview | open | `https://egeria-project.org/practices/coco-pharmaceuticals` |
| QS-4 | Reset scheduler (APScheduler) + Reset Now admin control | open | Coco archive load ≈ 5 min; pre-notify users 30 min before |
| QS-5 | Usage analytics + event logging (registrations, logins, tab views, persona selections) | open | `events` table in `demo` schema in Postgres |
| QS-6 | Obsidian integration in demo environment | open | Exploratory — Egeria already has Obsidian integration |
| QS-7 | Guided tour Level 1 (Intro.js via CDN) | deferred | After core demo is stable |

---

## pyegeria Upstream Bugs

| # | Bug | Status | Workaround |
|---|-----|--------|------------|
| PY-1 | `DataDesigner.find_data_value_specifications` calls non-existent `_async_post` | open | `_search_data_value_specs()` hits endpoint directly |
| PY-2 | `get_data_value_specifications_by_name("*")` rejects wildcard | open | Same workaround as PY-1 |
| PY-3 | `find_all_solution_blueprints/components` missing in 6.0.12.2 | open | Use `find_*(search_string="*")` |
| PY-4 | `ServerClient.update_comment` defaults `merge_update=True` and sets `mergeUpdate: true` in body, but Egeria still rejects the request with `OPEN-METADATA-400-004` requiring `qualifiedName` | open | Fetch comment first via `get_comment_by_guid`, extract `qualifiedName`, build body manually — costs an extra round-trip |

---

## LF-AI Project Explorer (separate repo)

Repo: `/Users/dwolfson/localGit/LF-AI/project-explorer`

| # | Item | Status |
|---|------|--------|
| LF-1 | End-to-end testing — compare mode, symbol table, alias banner, IntegrationAgent | open |
| LF-2 | Verify `code_symbol_extractor` is called from `pipeline.py` during `add` | open |
| LF-3 | Run test suite (`uv run pytest tests/ -v`) | open |
| LF-4 | Push to remote (only committed locally) | open |

---

## my-egeria Integration (Textual apps in portal)

Design doc: `my-egeria-integration.md` (in session). Architecture: `textual serve` turns Textual apps into browser tools; Apache proxies with WebSocket support.

**Credential model (V1):** single container per app; persona fixed at service startup via `EGERIA_USER` / `EGERIA_USER_PASSWORD` env vars from `.env`. All browser sessions to that app share one persona — fine for local single-user demo.

**Port allocation:** my_profile=8020, Data Products=8021, Tech Types=8022, Reports=8023, Journals=8024

| # | Item | Status | Notes |
|---|------|--------|-------|
| ME-1 | `serve_my_profile()` + entry point in pyegeria | done | In `my_egeria/serve.py`; registered in root `pyproject.toml` |
| ME-2 | `Dockerfile-my-egeria` in quickstart | done | Uses `textual_serve.Server` programmatically; textual==6.1.0 pinned |
| ME-3 | `my-profile` compose service in `egeria-quickstart.yaml` | done | Port 8020; `EGERIA_USER` / `EGERIA_USER_PASSWORD` from `.env` |
| ME-4 | `mod_proxy_wstunnel` in quickstart `httpd.conf` | done | Required for `upgrade=websocket`. (mod_substitute hack removed — superseded by ME-7's public_url fix.) |
| ME-5 | WebSocket proxy route `/my-egeria/` in quickstart `fastapi-proxy.conf` | done | `http://quickstart-my-profile:8020/` with `upgrade=websocket`; container name not host.docker.internal. `/my-egeria/static/...` and `/my-egeria/ws` both route through this Location. |
| ME-6 | "My Egeria" portal tile in quickstart `demo-portal.html` | done | Opens in new tab |
| ME-7 | End-to-end smoke test: browser → Apache WS proxy → Textual app | done | Two fixes were needed: (1) `*.tcss` missing from pyegeria `package_data` (StylesheetError crashed every session) — fixed upstream + Dockerfile bridge; (2) CSP blocked cross-origin `0.0.0.0:8020` assets — fixed by passing `public_url` to `textual_serve.Server` so it emits same-origin `/my-egeria/...` URLs. Verified: assets 200, WS 101 through proxy, no StylesheetError. |
| ME-7a | `/my-profile` returns 401 for some personas (erinoverview, garygeeke) despite valid token | open | peterprofile loads fine and is now the quickstart default. erinoverview/garygeeke get a bearer token (`TOKEN OK`) but the `/my-profile` GET returns 401, so the TUI exits before first paint. Likely related to the known my-profile/type-query 401 (pyegeria). Investigate token scope or account state. |
| ME-8 | `serve_*` entry points for additional apps (Data Products, Tech Types, Reports, Journals) | open | Apps exist in `DemoCode/` but no `serve_*` functions or `pyproject.toml` entries yet |
| ME-9 | Additional app compose services + proxy routes + portal tiles | open | Follow ME-2/3/4/5/6 pattern; ports 8021–8024 |
| ME-10 | my-egeria integration in freshstart (Option A — app handles login) | deferred | After quickstart smoke test passes; freshstart omits `EGERIA_USER`/`EGERIA_USER_PASSWORD` so app prompts user |
| ME-11 | V2 per-persona credential routing (one container per Coco persona) | deferred | Zero app changes; Apache routes `/my-egeria/{persona}/` to right container; all passwords `secret` in quickstart |
| ME-12 | V2 per-session process spawning for freshstart multi-user | deferred | Integration doc Option B; needs process manager service + dynamic port allocation |

---

## Done (recent)

| Item | Commit |
|------|--------|
| Type System Explorer ported to freshstart | — |
| Egeria Explorer login loop in Freshstart — token expiry + erinoverview defaults | `85341fb6` |
| Admin edit modal — givenName/surname pre-population | `85341fb6` |
| Egeria native likes + ratings on detail panes | `1344acfc` |
| Demo experience feedback button (all views) | `0731c2f0` |
| Python API docs pane | `d70b72c4` |
| Perspectives & Questions tab | — |
| Dr. Egeria Commands tab | — |
| Report Spec execution (backend + form) | — |
| ISC, Governance Definitions tabs | — |
| Solution Architect, Data Design tabs | — |
| Fix 401 on Egeria type queries in Freshstart | `e6f0c8d2` |
| Fix Egeria Explorer access + Advisor tile in Freshstart | `8f59eabd` |
