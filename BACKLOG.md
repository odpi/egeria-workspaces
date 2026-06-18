# Egeria Workspaces — Backlog

Consolidated work list. Update status when items start or finish.  
Status: `open` · `in-progress` · `done` · `deferred`
---
## Egeria Explorer — UI polish
    
    | # | Item | Status | Notes |
    |---|------|--------|-------|
    | UI-1 | Collections home-page card icon should match the others (blue outline, not emoji) | done | `_SPLASH_CAPABILITIES` Collections icon changed `'🗂'` → `'❐'` (monochrome, inherits `var(--accent)`). |
    | UI-2 | Remove duplicate sidebar titles that double the page header bar | done | Removed the hardcoded sidebar-title divs in `NoteLogView`, `LocationsView`, `CommunityView` (ISC already done). ProjectsView/ActorsView unaffected. |
  
## Mermaid Graphs copyable — ✅ done
  add a button/gesture to mermaid graphs to allow the raw mermaid text to be copied to the clipboard.
  **Done:** `MermaidDiagram` (type-explorer.html + tech-catalog.html) now shows a "⧉ Copy source" button that copies the raw mermaid text with a "✓ Copied" confirmation.

## Change Tile ordering for portal — ✅ done
    **Done:** reordered the `apps` array in both `demo-portal.html` files. Quickstart row 2 is Jupyter · Obsidian · My Egeria · Egeria Advisor; freshstart has no Obsidian tile, so its row 2 is Jupyter · My Egeria · Egeria Advisor · My Profile. Docs/Admin/API tiles follow.
    Row 1: The Catalog · Egeria Explorer · Lineage Explorer · Resource Explorer
    Row 2: Jupyter Lab · Obsidian · My Egeria · Egeria Advisor
    
    This is a reordering of the existing portal tiles in demo-portal.html (and the freshstart equivalent — keep both envs in sync, per the shared-codebase convention). The change is purely the order the tile elements appear in the markup; the grid/flex container already wraps four-per-row, so listing them in this
    sequence produces the two rows you want.
    
    A couple of things to watch when making the edit:
    - Resource Explorer and Lineage Explorer are noted as "Preview/soon" / not-yet-fully-wired in the backlog (RE-1/RE-2 credential pass-through is still open, and Lineage Explorer is net-new). They'll still render as tiles in row 1, but their launch wiring may be incomplete — that's fine for layout, just be aware
    the tiles may be placeholders.
    - Apply the same ordering to both the quickstart and freshstart portal pages so they don't diverge.
    - If the tiles are generated from an array/config rather than hardcoded markup, reorder the array entries rather than moving DOM blocks.
---

## Prioritization (workstream level)

`My Pri` = Claude's recommendation. `Your Pri` is blank — fill in `H`/`M`/`L` (or a rank) to steer.
Rationale favours **leverage** (unblocks other work) and **finishing shipped features** over net-new
exploration. Items can run concurrently when they touch different files; watch the noted dependencies.

| Workstream | Items | My Pri | Your Pri | Why / dependency |
|------------|-------|:------:|:--------:|------------------|
| Shared codebase unification | SHARE-1 ✅ done · SHARE-2 ✅ done | **H** |          | Both backend handlers and SPA `type-explorer.html` now byte-identical across quickstart/freshstart. Auth model runtime-gated via `srvManaged` + `demoMode` flags. |
| pyegeria comment-update bug | PY-4 ✅ done | **H** |    H     | Workaround already in `egeria_feedback_handler.py`. |
| **Technical Asset Catalog** | TC-0 → TC-12 | **H** |    H     | New tool; spec in `technical_data_catalog_spec.md`. TC-11 (classification ubiquity) is foundational — unblocks TC-12 (sidebar filtering) and zone display. |
| Report rendering | RR-1 → RR-5 | **H** |          | Core demo value; RR-1/RR-2 unblock RR-3/4/5. Sequential within the group. |
| Data preview polish | DP-2 ✅ · DP-3 ✅ · DP-4 ✅ done | **M** |    H     | Filter bar, column sort, search all done. |
| my-egeria additional apps | ME-8, ME-9 | **M** |    L     | TUI confirmed rendering end-to-end in demo (HTTPS). Follows proven ME-2..6 pattern. ME-7a (401 for some personas) still open. |
| ProjectExplorer integration | PORT-7, LF-1 → LF-4 | **M** |    M     | Needs the LF-AI service stood up first; port `8830` already reserved. |
| QuickStart demo polish | QS-1 ✅ · QS-3 ✅ done · QS-4 | **M** |    H     | QS-1/QS-3 already in portal; QS-4 (reset scheduler) still open. |
| Performance | PERF-1, PERF-2 | **M** |    M     | Real pain on deep catalog trees; investigate after correctness work. |
| Report specs authoring | RS-1, RS-2, RS-3 | **L** |    L     | Large, spec-still-TBD; defer until RR rendering lands. |
| User Feedback → Postgres | FB-5 → FB-9 | **M** |    H     | Per-page tool feedback to `demo.feedback`; env-specific user id; admin tab + analyst docs. Distinct from Egeria feedback. |
| Journals / feedback extras | FB-4 | **L** |    M     | Exploratory; storage model undecided. |
| Demo analytics / extras | QS-5, QS-6, QS-7 | **L** |    M     | Nice-to-have; QS-7 already deferred. |
| my-egeria V2 (multi-user) | ME-10, ME-11, ME-12 | **L** |    L     | Deferred until single-persona path is fully proven. |
| pyegeria DataDesigner/SA bugs | PY-1, PY-2, PY-3 | **L** |    H     | Have working local workarounds; fix upstream opportunistically. |
| **Modularization** | MOD-1 → MOD-3 | **M** |          | Extract shared UI components after Tech Catalog ships; unblocks future tools (Data Catalog etc). |

**Concurrency advice:** SHARE-1/2 first (or you fight merge pain on everything after). PY-4, DP-*,
and ME-8/9 are independent and safe to interleave. RR-* must go in order. Avoid starting RS-* and
FB-4 until the higher-leverage items clear.

---

## Ports & Networking  🔴 HIGH PRIORITY

**Status (2026-06-03): IMPLEMENTED and VERIFIED on a live quickstart stack** (PORT-1…PORT-6,
PORT-8, PORT-9 done). Only PORT-7 (ProjectExplorer, a not-yet-built service) remains open.
Compose files, Apache `ServerName`, `SITE_URL`, `MY_EGERIA_PUBLIC_URL`, portal links,
`gen-env.sh`, `demo_config.py`, `config_workspaces.json`, launch-script URLs, and all
READMEs/docs updated. Full table also in repo-root `README.md` (*Host port allocation*).
Verified after a full `down`/`up`: `:8800` direct, `:8885` /api/types + /egeria-explorer +
/portal + /my-egeria, `:8888` jupyter, `:8860` obsidian all healthy.

**Correction:** the earlier note "Apache proxy is container-internal, so unaffected" was WRONG
for quickstart — its vhosts proxied pyegeria-web via `host.docker.internal:8000` (the *host*
port), so moving 8000→8800 caused 503s. Fixed in PORT-9 by switching to the container name.

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
| both | **Egeria Advisor** | *(external, not in compose)* | qs **8880** / fs **7880** | was 8080 (collides w/ Airflow, Spark, new_uc); portal links via `EGERIA_ADVISOR_URL` — PORT-10 |

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
| Egeria Advisor (external) | 80 | **8880** | **7880** | 8080 (both) |

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
| PORT-8 | Repo-wide grep for hardcoded `:8000` / `:8085` / `localhost:80xx` | done | Swept compose/conf/html/py/sh/md/json; also caught `config_workspaces.json` and launch-script URLs in a second pass. |
| PORT-9 | Fix quickstart Apache proxy targets (`host.docker.internal:8000` → `quickstart-pyegeria-web:8000`) | done | Root cause of post-renumber 503s. Both `fastapi-proxy.conf` and `fastapi-ssl.conf` (44 targets). Now matches freshstart and is host-port-independent. |
| PORT-10 | Move Egeria Advisor off `8080` → qs **8880** / fs **7880** | done | Advisor is external (not in compose); `8080` collides with Airflow/Spark/new_uc. Updated `EGERIA_ADVISOR_URL` defaults (compose + `demo_config.py`) and portal `:8080` fallbacks in both envs. **Run the Advisor on the matching port**, or override `EGERIA_ADVISOR_URL` in `.env` if it's a single shared instance. |

---

## Egeria Explorer — Data Preview

| # | Item | Status | Notes |
|---|------|--------|-------|
| DP-1 | Adjustable column widths in tabular dataset preview | done | Drag-to-resize on column right-edge handles; dotted separators |
| DP-2 | Row filtering in dataset preview | done | Filter bar above table; client-side on current page |
| DP-3 | Row sorting in dataset preview | done | Click column header to sort (↑/↓/↕); numeric-aware; `e.stopPropagation` keeps resize handle separate |
| DP-4 | Search within table preview | done | Merged with DP-2 — same filter input covers full-text search across all cells |

---

## Egeria Explorer — Feedback & Comments

**Two distinct feedback systems — keep them separate:**

- **(A) Egeria Feedback** — Likes, Ratings, Comments on Egeria objects, via the Egeria/pyegeria
  feedback API. **Identical in every environment.** (FB-1..FB-3 done.)
- **(B) User Feedback** — the "Feedback" button on every tool page capturing the end user's opinion
  *of the tool/page itself*, persisted to a **Postgres table** (in the shared `demo` schema) so we
  can analyse how to improve the tools and Egeria. The **user identity attached differs by env**
  (the only intentional difference); the capture schema and UI are otherwise the same everywhere.

| # | Item | Status | Notes |
|---|------|--------|-------|
| FB-1 | Egeria comments on property sheets | done | Glossary Term + Digital Product detail panes; type dropdown; history list |
| FB-2 | Likes + ratings on remaining detail panes | done | `EgeriaFeedbackWidget` on all property detail panes. ReportSpecDetail excluded — pyegeria format specs have no Egeria GUID. |
| FB-3 | Comments (`EgeriaCommentsSection`) on remaining detail panes | done | `EgeriaCommentsSection` on all property detail panes. ReportSpecDetail excluded — same reason as FB-2. |
| FB-4 | Journals — persistent per-element notes/log separate from Egeria comments | open | Exploratory; may be local storage or a separate Egeria NoteLog. **Read-only NoteLog viewer now shipped** (Note Logs tab, see Done-recent); FB-4 remains for the *write* side. |
| FB-5 | **User Feedback → Postgres** — move per-page feedback from current `/api/demo-feedback` store to a `feedback` table in the `demo` schema (port 5442). One schema, all envs. | done | `demo_feedback_handler.py` rewrites to Postgres via `DEMO_DB_URL`; `demo` schema created on startup. Freshstart `demo_config.py` gets `DEMO_DB_*` vars. |
| FB-6 | **Env-specific user identity** on User Feedback (the one intentional per-env difference) | done | `_resolve_user_id()`: JWT `sub` (demo/freshstart) or supplied email (local). `_resolve_env()` sets `env` field. |
| FB-7 | **Capture schema** for each submission | done | Full schema: id, session_id, user_id, env, persona, page, element_guid, rating, category, message, email, wants_response, consent_to_contact, build_version, user_agent, viewport, locale, triage_status, created_at. FeedbackButton updated with category dropdown + wants_response + consent checkboxes. |
| FB-8 | **Admin review tab** in each env's admin panel | done | Feedback tab added to both admin panels: stats row (total/new/wants-response), filter by status+env, triage dropdown (new→triaged→actioned), PATCH `/api/demo-feedback/{id}`. |
| FB-9 | **Analyst docs** — how to query the raw `feedback` table | done | `feedback-analyst-guide.md` — schema reference + 12 SQL recipes (volume/day, by page, by env, category breakdown, avg rating, response queue, bugs, persona, triage). |

**FB-7 recommended capture fields** (your list + additions):
*Your list:* user id · page · environment · timestamp · email · wants-response.
*Suggested additions:* the **free-text message** + a **rating/sentiment** (the actual content) · **category**
(bug / confusing / suggestion / praise) · **element/object GUID or route detail** in view · **active persona**
(demo) · **tool/build version or git SHA** (correlate to a release) · **user-agent + viewport** (repro UI issues)
· **session/correlation id** (link multiple submissions / to analytics events QS-5) · **locale** · **explicit
consent-to-contact** flag (separate from wants-response, for privacy basis) · server-side **triage status**
(new/triaged/actioned). Optional: screenshot attachment.

---

## Egeria Explorer — Report Rendering

Spec: `report-rendering-plan.md`

**Note (2026-06-18):** the RR components were implemented earlier without updating
these rows. All verified against live report output; **two real bugs found and
fixed** — RR-4 chart detection (camelCase-only key regex) and RR-5 master-detail
(column key/name mismatch). RR-1..RR-5 all done.

| # | Phase | Item | Status | Notes |
|---|-------|------|--------|-------|
| RR-1 | 1 | GRAPH format → send DICT/JSON fallback (no unembeddable HTML) | done | Verified: selecting GRAPH sends DICT (or JSON) client-side; backend returns `kind: json`. The 3 GRAPH specs (Governance-Zones, Governance-Zone-Overview-Charts, Secrets-Collection-User-Profile-Charts) return Vega-Lite chart specs in the DICT data. |
| RR-4 | 3b | `AvailableCharts` — detect Vega-Lite chart specs in DICT results | done | **Bug fixed:** matched only camelCase `*BarGraph`/`*PieGraph` keys, but real pyegeria DICT keys are spaced ("Zone Profile All Bar Chart"). Rewrote to detect charts by *value* (any `$schema: vega-lite` dict/JSON-string) — now finds all 6 zone charts (was 0). |
| RR-3 | 3a | `VegaChart` component + vega-embed load | done | Renders dict or JSON-string specs via vegaEmbed (dark theme), with deferred-load polling; wrapped by `CollapsibleChartPanel`. |
| RR-2 | 2 | `SmartReportRenderer` — tokenize output; render Mermaid/Vega-Lite fences; master-detail anchors | done | Verified against a MERMAID spec (Org-Chart) — the ` ```mermaid ` fence tokenizes to `MermaidDiagram`. Tokenizer also handles `vega-lite`/`json` fences; `<a id>` anchors get "↑ back" links and `[text](#anchor)` becomes clickable. |
| RR-5 | 4 | `DictResultView` — spec-driven master-detail table with expand rows + auto-charts | done | **Bug fixed:** indexed `row[c.key]` (snake_case spec key) but pyegeria DICT rows are keyed by display name, so spec-driven scalar cells were empty and master-detail never expanded. Now resolves each column to whichever identifier exists in the data (`key` or `name`). Verified on Team-Members → Members detail (Team-Member-Role-Detail) now expands. |

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

`type-explorer.html` (~7500 lines) and the backend handlers existed as separate copies under
`egeria-quickstart/` and `egeria-freshstart/`. The earlier "~38 lines" estimate was wrong: actual
divergence was ~4,300 diff-lines, but it splits cleanly — the **Explorer logic was ~95% identical**;
real divergence is confined to (a) the **auth/credential seam** and (b) the by-design **auth/portal
layer** (demo SQLite auth vs Egeria-backed auth — intentionally separate, NOT unified).

**SHARE-2 is DONE.** All Explorer **backend handlers are now byte-identical** across both envs and
verified live (`/api/types` 200 in quickstart *and* freshstart). The credential seam is unified via a
`SERVER_MANAGED_AUTH` flag in `demo_config.py` (False=quickstart form/demo creds; True=freshstart
per-user Egeria token w/ service-account fallback). Remaining backend divergence is only the
by-design auth/portal layer (`demo_auth_handler`, `demo-*.html`, `demo_db`, `pyegeria_handler`
app-wiring) and the legitimately env-specific `config_workspaces.json` publishing-root port.

| # | Item | Status | Notes |
|---|------|--------|-------|
| SHARE-2 | Unify backend Explorer handlers across freshstart + quickstart | done | `type_system_handler` (via `SERVER_MANAGED_AUTH` superset), `digital_products`, `governance_definitions`, `egeria_feedback` all byte-identical; rest of Explorer handlers already were. Auth/portal layer stays per-env by design. |
| SHARE-1 | Unify `type-explorer.html` — one canonical SPA served to both envs | done | `/api/auth/me` extended with `server_managed_auth`; `srvManaged` SPA state added; 8 auth regions runtime-gated (ConnectionForm, creds defaults, load effect, "Connected as" banner, persona badge, error-retry, portal link); files byte-identical across both envs. Portal link now present in ALL modes (was regression-hidden behind `demoMode`). Needs browser verification in 3 modes (demo-qs, local-qs, freshstart). |

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

## Egeria Explorer — Hierarchy & Grouping (built; awaiting data to verify)

These left-nav hierarchy/grouping features are implemented and verified to render
correctly, but the QuickStart/Freshstart demo data doesn't currently populate the
underlying relationship, so they show flat. **Re-verify once the data is seeded.**

| # | Item | Status | Notes |
|---|------|--------|-------|
| HV-1 | **ISC segment hierarchy** in the Supply Chains left nav | built; no data | Each ISC row expands to its `segments`. All 16 ISCs have 0 segments today (structure is the `supplyTo` flow, a graph, surfaced in the detail). Verify when ISCs are given nested segments. |
| HV-2 | **Project dependency forest** (Projects → Dependencies sub-tab) | built; no data | `GET /api/projects/dependencies` builds the forest from `dependsOnProjects`/`dependentProject` (ProjectDependency). No dependencies defined in demo data → renders flat. Hierarchy sub-tab works (real data). Verify after `set_project_dependency` is used. |
| HV-3 | **Folio grouping for Blueprints** (Solution Architect → Blueprints) | built; no data | `GET /api/solution/blueprints/folios` groups blueprints under member Folios. The one Folio holds governance defs, not blueprints, so all 31 are "Not in a folio". Verify after blueprints are added to a Folio. |

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
| QS-1 | Portal — link to egeria-project.ai docs and odpi GitHub repos | done | Already in `demo-portal.html` nav bar (Documentation ↗, GitHub ↗, individual repo star links) |
| QS-2 | Portal — prompt users to star egeria / egeria-workspaces / egeria-python repos | open | Best-practice UX for this TBD |
| QS-3 | Persona picker page — link to Coco Pharmaceuticals overview | done | Already in persona picker modal and nav bar in `demo-portal.html` |
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
| PY-4 | `ServerClient.update_comment` defaults `merge_update=True` and sets `mergeUpdate: true` in body, but Egeria still rejects the request with `OPEN-METADATA-400-004` requiring `qualifiedName` | done | Workaround already in `egeria_feedback_handler.py`: fetches comment first via `get_comment_by_guid`, extracts `qualifiedName`, builds body manually |
| PY-5 | `get_notes_for_note_log` was unusable in 6.0.14.5 (default `metadata_element_type_name="Action"` → `OMAG-…-404-001` on the NoteLog guid; `="NoteLog"` returned the log not the notes; timed out on big logs) | **fixed in 6.0.14.6** | Default kwargs now return the notes, `page_size`-bounded. **Gotcha:** do *not* pass `metadata_element_type_name="NoteLog"` — now returns 0. `notelog_handler.py` uses the default. |
| PY-6 | `find_note_logs('*')` at default graph depth is O(total notes) — inlines every log's entries (~30s on qs; `page_size` bounds logs, not per-log expansion) | open | List uses `graph_query_depth=0` (≈0.3s, accepted via `**kwargs`); subjects via the depth-0 `Anchors` classification |

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
| ME-7 | End-to-end smoke test: browser → Apache WS proxy → Textual app | done | Two fixes were needed: (1) `*.tcss` missing from pyegeria `package_data` (StylesheetError crashed every session) — fixed upstream + Dockerfile bridge; (2) CSP blocked cross-origin `0.0.0.0:8020` assets — fixed by passing `public_url` to `textual_serve.Server` so it emits same-origin `/my-egeria/...` URLs. Verified: assets 200, WS 101 through proxy, no StylesheetError. **Demo deployment fixes (2026-06-04, `577fc9b2`):** (3) `my-profile` was not started by `quick-start-local` — added to build + startup; (4) `/my-egeria/` route missing from `fastapi-ssl.conf` (only existed in HTTP vhost) — caused 404 on HTTPS; (5) `MY_EGERIA_PUBLIC_URL` was `http://` — overridden to `${DEMO_SITE_URL}/my-egeria` in demo overlay to avoid browser mixed-content block on WebSocket; (6) Podman 3.x silently skips external networks at container creation — `_podman_fix_network` helper added to `quick-start-local` to connect + cycle containers onto `egeria_network` after each `up -d`. |
| ME-7a | `/my-profile` returns 401 for some personas (erinoverview, garygeeke) despite valid token | open | peterprofile loads fine and is now the quickstart default. erinoverview/garygeeke get a bearer token (`TOKEN OK`) but the `/my-profile` GET returns 401, so the TUI exits before first paint. Likely related to the known my-profile/type-query 401 (pyegeria). Investigate token scope or account state. |
| ME-8 | `serve_*` entry points for additional apps (Data Products, Tech Types, Reports, Journals) | open | Apps exist in `DemoCode/` but no `serve_*` functions or `pyproject.toml` entries yet |
| ME-9 | Additional app compose services + proxy routes + portal tiles | open | Follow ME-2/3/4/5/6 pattern; ports 8021–8024 |
| ME-10 | my-egeria integration in freshstart (Option A — app handles login) | deferred | After quickstart smoke test passes; freshstart omits `EGERIA_USER`/`EGERIA_USER_PASSWORD` so app prompts user |
| ME-11 | V2 per-persona credential routing (one container per Coco persona) | deferred | Zero app changes; Apache routes `/my-egeria/{persona}/` to right container; all passwords `secret` in quickstart |
| ME-12 | V2 per-session process spawning for freshstart multi-user | deferred | Integration doc Option B; needs process manager service + dynamic port allocation |

---

## Technical Asset Catalog

Spec: `technical_data_catalog_spec.md`

New standalone SPA (`tech-catalog.html`) + backend handler (`tech_catalog_handler.py`). Served at `/tech-catalog` via the existing Apache proxy — no new container or port needed. Uses `AssetMaker` and `ConnectionMaker` from pyegeria. Portal tile added to both quickstart and freshstart.

**Dependency order:** TC-0 (scaffolding) → TC-1 (backend) → TC-2 (shell) → TC-3/TC-4/TC-5/TC-6 (sections, parallel) → TC-7 (detail polish) → TC-8 (cross-navigation, post-MVP).
**Next priorities:** TC-11 (classification ubiquity audit) → TC-10 (zone display, free once TC-11 done) + TC-12 (sidebar filtering). TC-9 (lineage for non-Asset types) is independent.

| # | Item | Status | Notes |
|---|------|--------|-------|
| TC-0 | Scaffolding: `tech-catalog.html` skeleton, `tech_catalog_handler.py` stub, router registration, Apache proxy block, portal tile in both envs | done | Portal tile 🐱, Apache proxy, router registered in both envs; SPA loads and shows 4-tile splash |
| TC-1 | Backend: all 9 list endpoints + `/{guid}` detail — `find_infrastructure`, `find_software_capabilities`, `find_endpoints`, `find_data_assets` (×3), `find_assets` (DeployedAPI), `find_processes` (×2) | done | All pass `sequencing_order="PROPERTY_ASCENDING"`; consistent `{ items, total }` JSON shape |
| TC-2 | SPA shell: auth seam (srvManaged/demoMode), hash-based section routing, 4-tile splash screen, FeedbackButton | done | Mirrors Explorer App structure; hash nav so portal can deep-link to sections |
| TC-3 | Infrastructure section: 3 sub-tabs (IT Infrastructure / Software Capabilities / Endpoints), sidebar search + type-group filter, detail panel | done | Implemented via generic `SectionView` + `AssetTabView` with `SECTION_TABS` config |
| TC-4 | Data Assets section: 3 sub-tabs (Data Stores / Data Feeds / Data Sets), sidebar + detail | done | Same generic components |
| TC-5 | APIs section: single list + detail (DeployedAPI) | done | Single-tab section |
| TC-6 | Processes section: 2 sub-tabs (Software Components / Actions), sidebar + detail | done | `find_processes` with `metadata_element_type` filter |
| TC-7 | Detail panel polish: full property table, mermaid graphs (`AvailableMermaidDiagrams` + `MermaidSection`), classifications with properties, relationships with related element | done | `AssetTabView` fetches full detail via `get_asset_by_guid` on selection; `_extract_relationships` in backend; relationships card in `AssetDetail` (type · name · description · rel properties); summary shown immediately, detail overlaid on load |
| TC-8 | Cross-navigation links: Infrastructure ↔ Software Capabilities, Software Capability ↔ IT Asset, Endpoint → server, Data Store → Data Sets | done | Mechanism (navTarget + `TYPE_TO_NAV` + supertype fallback) built during L-6/L-9. Verified 2026-06-18 against live data: relationship `relatedElement` carries `typeName` + `superTypeNames`, so subtypes resolve via their abstract supertype (e.g. IntegrationGroup→SoftwareCapability). Working: Infra↔Capabilities, Capability↔Server, API↔Endpoint, DataStore↔Endpoint. **Limitation:** *Endpoint→server* and *DataStore→DataSets* reverse links aren't in the depth-5 graph from that element's side (only Connection internals appear). Connection/ConnectorType/VirtualConnection targets are correctly non-navigable. |
| TC-9 | Investigate which Catalog types genuinely support lineage — Endpoint and SoftwareCapability are Referenceable subtypes (not Asset) | done | `_serialize` now sets `hasLineage = "Asset" in superTypeNames` (was always True); SPA already gates `LineagePane` on `hasLineage`. Endpoint/SoftwareCapability no longer show an empty lineage pane; Assets still do. `superTypeNames` added to serializer + property-table skip list. |
| TC-10 | Zone-based sidebar filtering | done | Absorbed into TC-12 |
| TC-11 | Classification ubiquity audit and fix | done | Root cause found and fixed: pyegeria stores each classification as a named key directly on `elementHeader` with `class="ElementClassification"`, not in a `classifications` array; rewrote `_extract_classifications` in both handlers to iterate `elementHeader` items; confirmed working — `ZoneMembership` and `DataAssetEncoding` visible in Catalog property panels; `_SKIP_CLASSIFICATIONS` skips internal types (Anchors, LatestChange, Memento, etc.) |
| TC-12 | Classification-based sidebar filtering | done | Filter chips below search bar: zone chips (🌐 zoneName, green) + classification type chips (purple); multi-select AND logic; `ZoneMembership.zoneMembershipList` split per zone; classification badges on each sidebar list item (zones green, others purple, max 3); filter resets on tab change |

---

## Resource Explorer

Portal card added (Preview soon). Credential pass-through and launch wiring needed before the tool can be enabled.

The Catalog and Egeria Explorer both receive credentials at launch via query params (`url`, `server`, `user_id`) appended to the target URL by the portal. The same pattern must be applied to Resource Explorer and Egeria Advisor.

| # | Item | Status | Notes |
|---|------|--------|-------|
| RE-1 | Pass Egeria credentials to Resource Explorer at launch — append `url`, `server`, `user_id` query params the same way the portal does for The Catalog and Egeria Explorer | open | Portal `launch()` call needs to read current creds state and append params; Resource Explorer SPA reads them on load |
| RE-2 | Pass Egeria credentials to Egeria Advisor at launch — same credential pass-through pattern as RE-1 | open | Advisor is an external service (not in compose); confirm it accepts query-param credentials or needs a different mechanism |

---

## Lineage Explorer

New standalone portal application for data lineage visualization centred on a "focus asset". Spec: `Lineage Explorer.md`.

| # | Item | Status | Notes |
|---|------|--------|-------|
| LE-1 | Initial implementation — handler, SPA, portal tile, cat_calls docs | done | `lineage_handler.py` + `lineage-explorer.html`; both QS and FS |
| LE-2 | Tech Catalog → add "Open in Lineage Explorer" deep-link button to the lineage sub-pane for all asset types | done | Button added to `LineagePane` in `tech-catalog.html`; opens `/lineage?guid={guid}` |
| LE-3 | Time slider — generalise as a shared component for Egeria Explorer and Tech Catalog pages | open | Spec notes: "expected to be a common feature added to each page"; blocked on MOD-2 modularization |
| LE-4 | Audit all existing handler endpoints — remove `user_id`/`user_pwd` query params and replace with token-only pattern | open | New rule: credentials via env vars only; token via `X-Egeria-Token` header. Affects `tech_catalog_handler.py` and others |

---

## Modularization

Spec notes in `technical_data_catalog_spec.md` (Modularization strategy section).

Goal: extract the shared UI components that appear verbatim in both Explorer and Tech Catalog into a served static file (`egeria-shared-ui.js`), so changes propagate automatically. Run this workstream **after** Tech Catalog Phase 4 ships — we need both consumers to exist before we can define the stable extraction boundary.

**Short-term mitigation:** Mark shared blocks in Tech Catalog with `// SHARED — keep in sync with type-explorer.html` comments so drift is visible in code review.

| # | Item | Status | Notes |
|---|------|--------|-------|
| MOD-1 | Audit: list all components copied verbatim from Explorer into Tech Catalog; confirm boundary (what to share vs what stays per-tool) | done | See `shared-ui-audit.md`. Boundary: **Tier 1 share-now** (Mermaid family + field constants, ResizeDivider, useResizable, renderMd/_renderMdHtml, VegaChart/AvailableCharts — canonical = richer Explorer version); **Tier 2 share-after-fetch-unification** (credAppend + feedback widgets — blocked by token vs query-param auth split, sequence with LE-4); **Tier 3 per-tool** (ConnectionForm, CredContext provider, tool views). |
| MOD-2 | Extract shared components to `egeria-shared-ui.js`: `MermaidDiagram`, `DiagramPanel`, `MermaidSection`, `AvailableMermaidDiagrams`, `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, property-table renderer | open | Served as FastAPI static; imported by both SPAs via `<script>` tag |
| MOD-3 | Refactor Explorer + Tech Catalog to import from shared module; remove duplicated blocks | open | Shrinks both files ~25–30%; future tools (Data Catalog etc.) start from shared base |

---

## Done (recent)

| Item | Commit |
|------|--------|
| Note Logs tab — read-only NoteLog viewer (both envs); entries via fixed `get_notes_for_note_log` (PY-5), subjects via `Anchors` classification | `4fdf09df` |
| my-profile: wire into quick-start-local + fix Podman networking + SSL vhost + HTTPS public URL | `577fc9b2` |
| Portal layout aligned with quickstart + Workspaces docs tile added (freshstart) | `c0fd2afc` |
| Type System Explorer unified SPA + portal link fix (SHARE-1) | `5958dd03` |
| Converge trivial handler drift (SHARE-2) | `04c9be2d` |
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
