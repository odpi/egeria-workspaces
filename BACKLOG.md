# Egeria Workspaces — Backlog

Consolidated work list. Update status when items start or finish.  
Status: `open` · `in-progress` · `done` · `deferred`

---

## Egeria Explorer — Data Preview

| # | Item | Status | Notes |
|---|------|--------|-------|
| DP-1 | Adjustable column widths in tabular dataset preview | open | Drag-to-resize on column headers |
| DP-2 | Row filtering in dataset preview | open | Eventually — filter bar above table |
| DP-3 | Row sorting in dataset preview | open | Eventually — click column header to sort |

---

## Egeria Explorer — Feedback & Comments

| # | Item | Status | Notes |
|---|------|--------|-------|
| FB-1 | Egeria comments on property sheets | open | Bottom of each detail pane; dropdown for comment type; show comment history |
| FB-2 | Filter Products / Glossary / Reports by like count or rating | open | |

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
| FS-1 | Admin edit user — show all current values; roles/groups as checkboxes (not multi-select highlights) | open | Roles/groups as checkboxes makes it easier to see and toggle current state |
| FS-2 | My Profile page (`/profile`) — self-service display name, job title, description + password change | open | Calls `MyProfile` API; file exists but completeness unclear |
| FS-3 | Portal greeting reads org name from `application.properties` | open | `platform.organization.name` property |
| FS-4 | Delete `demo_db.py` — no SQLite in freshstart | open | Egeria is the sole user store; file still present |

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

## Done (recent)

| Item | Commit |
|------|--------|
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
