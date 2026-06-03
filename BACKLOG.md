# Egeria Workspaces — Backlog

Consolidated work list. Update status when items start or finish.  
Status: `open` · `in-progress` · `done` · `deferred`

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
| ME-2 | `Dockerfile-my-egeria` in quickstart | in-progress | PR from Ultraplan session |
| ME-3 | `my-profile` compose service in `egeria-quickstart.yaml` | in-progress | PR from Ultraplan session; port 8020 |
| ME-4 | `mod_proxy_wstunnel` in quickstart `httpd.conf` | in-progress | PR from Ultraplan session; required for WebSocket |
| ME-5 | WebSocket proxy route `/my-egeria/` in quickstart `fastapi-proxy.conf` | in-progress | PR from Ultraplan session; must use `ws://` scheme not `http://` |
| ME-6 | "My Egeria" portal tile in quickstart `demo-portal.html` | in-progress | PR from Ultraplan session; opens in new tab |
| ME-7 | End-to-end smoke test: browser → Apache WS proxy → Textual app | open | Verify `sys.path` / import resolution works for installed package; critical before adding more apps |
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
