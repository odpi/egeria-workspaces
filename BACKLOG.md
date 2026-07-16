# Egeria Workspaces — Backlog

Consolidated work list. Update status when items start or finish.  
Status: `open` · `in-progress` · `done` · `deferred`
---
## Type coverage gaps — next up (2026-07-15)

Source: `type-coverage-gap-analysis.html`. Items #2 and #7 from that doc are
already done (see their own BACKLOG sections below). Next in priority order
(smallest/niche first, per Dan's explicit ordering — not the doc's own tier
order):

| # | Item | Doc entry # | Status | Notes |
|---|------|-------------|--------|-------|
| GAP-10 | Naming-standard vocabulary | 10 | open (extension pending) | `PrimeWord`/`ClassWord`/`Modifier` classifications — "Naming Vocabulary" pane built, `naming_vocabulary_handler.py`. Demo data seeded and left in place (no live data existed). Both envs. Re-opened 2026-07-16 — Dan is writing up a scope extension; see GAP-10-EXT below. |
| GAP-9 | Policy enforcement architecture | 09 | open (extension pending) | 6 `Policy*Point` classifications — "Policy Enforcement" pane built, `policy_enforcement_handler.py`. Demo data seeded and left in place. Both envs. Re-opened 2026-07-16 — extension write-up forthcoming; see GAP-9-EXT below. |
| GAP-8 | Privacy execution detail beyond the purpose stub | 08 | done | Zero code changes needed — `governance_definitions_handler.py`'s existing generic relationship serializer + `GovDefDetail`'s generic `RelationshipSection` rendering already surface the 2 real `ApprovedPurpose`→`CSVFile` links. Both envs already identical. |
| GAP-6 | Action Center (re-scoped from "social/collaboration layer") | 06 | open (extension pending) | Notification/Meeting/ToDo/Review only — Comment/Rating/Like already covered via feedback widget; Task/Campaign are Project/Collection classifications, not separate types. `action_center_handler.py` + `ActionCenterView`/`ActionDetail` built. Notification has real data (~50-1170, fluctuates); Meeting/ToDo/Review seeded and left in place. Also fixed `EngineAction` cross-nav routing (`egeria-shared-ui.js`'s `resolveElementNav`/`crossAppNavigate`) to open Egeria Operations' Engine Actions tab instead of falling through to Tech Catalog's generic mixed Actions tab. Both envs. Re-opened 2026-07-16 — extension write-up forthcoming + cross-link completeness check; see GAP-6-EXT below. |
| GAP-5 | No duplicate-resolution review | 05 | done | `KnownDuplicate`/`ConsolidatedDuplicate`/`PeerDuplicateLink`/`ConsolidatedDuplicateLink` — new read-only "Duplicate Review" pane, `duplicate_review_handler.py`. Demo pair seeded (two `Community` entities) and left in place. Hit a pyegeria bug seeding it — see PYEGERIA_ISSUES.md PY-16. Both envs. |

### Follow-ups from review (2026-07-16)

| # | Item | Status | Notes |
|---|------|--------|-------|
| GAP-HOME | Home page splash cards for new tabs | done | Added 4 cards to `_SPLASH_CAPABILITIES` (Naming Vocabulary 𝔸, Policy Enforcement 🛡, Action Center ✓, Duplicate Review ⧉) — GAP-8 needed none (no new tab). Both envs, live-verified in quickstart. Also updated `PyegeriaWebHandler/README.md` in both envs with a subsection per new tab, and brought freshstart's README's stale top-level nav-group description up to date (it still described an old 8-tab flat layout). |
| GAP-10-EXT | Naming Vocabulary — scope extension pending | open | Dan is writing up an extension to this feature; re-opened pending that write-up. Current implementation: flat list grouped by `PrimeWord`/`ClassWord`/`Modifier` classification, seeded demo data. |
| GAP-9-EXT | Policy Enforcement — scope extension pending | open | Same as GAP-10-EXT — write-up forthcoming, re-opened pending it. Current implementation: flat list grouped by the 6 `Policy*Point` classifications, seeded demo data. |
| GAP-6-EXT | Action Center — scope extension pending | open | Write-up forthcoming; re-opened pending it. **Cross-link gap found and fixed 2026-07-16**: `get_metadata_element_by_guid` never returns relationships for these types at any `graph_query_depth` (confirmed live — depth 0-3 all identical, no relationship keys); the real cross-links (`Actions`/`ActionRequester`/`AssignmentScope`/presumably `ActionTarget`) only surface via `MetadataExpert.get_all_related_elements(guid)`. `action_center_handler.py` now calls both and merges — verified live against a real Notification with 3 real relationships (→ NotificationType, PersonRole, WatchdogActionService), all correctly cross-linkable via existing generic dispatcher fallbacks. Both envs. See PYEGERIA_ISSUES.md PY-17. |

---
## Egeria Explorer search + Tech Catalog fixes/features (2026-07-06/08) — ✅ done

| # | Item | Status | Notes |
|---|------|--------|-------|
| SEARCH-1 | Global search results always cross-linked Projects (and any type outside the backend's `_TYPE_CATEGORY` map) to the generic Catalog/data-asset screen | done | Added `"Project"` → `projects` category in `catalog_search_handler.py` (both envs). `ExplorerSearchView` (type-explorer.html) now routes linkable result types through the shared `onNavigateToElement` dispatcher instead of hardcoding a `/tech-catalog?guid=` link; added `onNavigateToProject`/`ProjectsView(navGuid)` cross-nav plumbing, matching the existing pattern for Perspectives/Communities/etc. |
| TC-REFRESH-1 | Refreshing The Catalog with a stale `?guid=` in the URL (e.g. from an old deep link) always re-navigated to that same element instead of the current section | done | `tech-catalog.html`'s deep-link resolver now calls `history.replaceState(...)` after consuming `?guid=`, replacing it with `#<resolved-section>` so a refresh lands on the section, not the one-time nav target. |
| TC-15 | Processes tab had no view for `GovernanceActionProcess` definitions — no step/flow/guard/target detail (type 0462) | done | New **Governance Processes** sub-tab in The Catalog's Processes section (`GET /api/tech-catalog/governance-processes[/{guid}]`, `GovernanceOfficer.find_governance_definitions` / `get_governance_process_graph`). Detail view shows the mermaid flow diagram, ordered steps, guarded step-links, and request/produced-guard/action-target tables (reusing `_extract_survey_spec`/`SurveySpecCard`). Also fixed `_normalize_action_target` to read `openMetadataTypeName` (previously always blank for process specs). See `technical_data_catalog_spec.md` → Processes tile → Governance Processes tab. (Note: this item was originally mislabeled `TC-9` — that ID was already in use for the lineage-support-audit item below; corrected 2026-07-08.) |
| TC-16 | Survey Reports/Annotations had no visible creation timestamp or way to filter by it or by survey name; relationship cards for Annotation-typed related elements showed only a raw GUID (Annotations have no `displayName`) | done | Backend: `_serialize()` now includes `createTime`/`updateTime` (`elementHeader.versions`); `_unwrap_rel_item()`'s relatedElement `displayName` falls back through `summary`/`qualifiedName` before `guid`, and now also returns a `properties` dict of the related element's other scalar properties (annotationType, confidence, analysisStep, etc.). Frontend: `SidebarDetail` shows each item's creation time; `AssetTabView` gained a Created date-range filter (shown for the `survey-reports` endpoint); `AnnotationsTabView` gained a survey-report-name text filter + Created date-range filter, both client-side; `AssetDetail`'s relationship cards render the new `properties` fields. See `cat_calls.md` → `_serialize` output fields. |
| TC-17 | Made `TechTable` and two hand-rolled tables (Technology Types "Catalog Instances", `SchemaPane` attributes) resizable, matching `AnnotationsTabView`. Uncovered a real, previously-undiagnosed bug in the process: `/static/*` assets (`egeria-shared-ui.js`, shared by both apps) had no `Cache-Control` header, so browsers heuristically cache it; the SPA HTML documents are versioned freshly (`no-store`) but the shared JS was not, so a browser with an old cached copy of `egeria-shared-ui.js` + fresh HTML calling a newly-added shared function throws a synchronous `ReferenceError` outside React's render cycle — reproduced deterministically in a headless Node+jsdom harness (not a browser-tooling artifact, as first suspected) — presenting as a blank page with no visible console error | done | Added `makeResizableCols`/`resizableColgroup` to `egeria-shared-ui.js` — a hook-free (ref-based, imperative DOM write) column-resize mechanism, since `TechTable` is called as a plain function inside `.map()` loops where React hooks aren't safe. Applied to `TechTable` (feeds Catalog Templates, Other Resources, Survey specs, all of `GovernanceProcessDetail`'s tables), the Catalog Instances table, and `SchemaPane`. **Root-cause fix:** `pyegeria_handler.py` now mounts `/static` via a `NoCacheStaticFiles` subclass that sets `Cache-Control: no-cache` on every response (forces ETag revalidation, so edits apply on next load without a hard-refresh) — was previously an unversioned, unheadered static mount, a latent bug independent of this specific feature that could recur on any future shared-JS edit. Also added the same `no-store, must-revalidate` header to `/egeria-explorer`'s `FileResponse` (`type_system_handler.py`), which — unlike `/tech-catalog` — had no cache header on its HTML document at all. Added a `?v=` cache-busting query string to both apps' `<script src="/static/egeria-shared-ui.js">` tags (bump on every future edit) — the `no-cache` header alone can't force browsers that cached the file *before* that header existed to revalidate; a new URL guarantees a fresh fetch regardless of prior cache state. Follow-up (same day): widened `colResizeHandle`'s hit target from 6px to a 12px invisible target around the same visible dotted line (6px was easy to miss, confirmed by mis-clicking it myself during testing), and extended resize to the three Glossary "Properties" tables (`GlossaryFolderDetail`/`GlossaryDetail`/`GlossaryTermDetail` in `egeria-shared-ui.js`, shared with Egeria Explorer) — these had no `<thead>` at all (label:value rows), so the resize handle is anchored to the first row's label cell instead of a header. Verified all edits via a headless Node+jsdom render harness before deploying, after the earlier blank-screen incident. **Second follow-up:** the actual remaining complaint was about *pane dividers*, not table columns — `TechTypesView`'s sidebar/detail split (`tech-catalog.html`) and `GlossaryView`'s middle/right split were hardcoded `width: 290`/`width: 280` with no drag handle at all (only Glossary's left/middle divider had one). Added a second `useResizable`/`ResizeDivider` pair to each, matching the pattern already used elsewhere in the same functions. |

---
## Egeria Insights (2026-07-15) — ✅ done

New portal app for cross-cutting governance search: classification + zone faceted
search over Egeria's native `find_metadata_elements` (`matchClassifications` /
`SearchClassifications` / `ClassificationCondition`, one native query rather than
client-side set intersection — see `insights_handler.py`'s module docstring for
the full design rationale). Dashboard tab (capped aggregate tallies) + Governance
Search tab (facet picker driven live from `/api/types`, compound AND/OR search
with an opt-in exhaustive `full_count` pass). Router registered in
`pyegeria_handler.py`, portal tile added to `demo-portal.html`.

| # | Item | Status | Notes |
|---|------|--------|-------|
| INS-1 | `_extract_classifications()`/`_serialize_hit()`/`get_zones()` guessed `find_metadata_elements()` returns an `elementHeader`-wrapped shape (like converter-backed calls e.g. `AssetMaker.get_asset_by_guid`) | done | Verified live against qs-view-server: it actually returns the *raw* shape — no `elementHeader` wrapper, `elementGUID` not `guid`, `classifications` as a flat list of `AttachedClassification` (`classificationName` + `classificationProperties.propertyValueMap`), `elementProperties.propertyValueMap`. Rewrote the parsing helpers in `insights_handler.py` accordingly; also fixed `GovernanceZone`'s name field (`identifier`, not `zoneName`). Verified end-to-end: single-classification search, property-filtered search (confidentialityLevel), and zones-with-usage-counts all correct against real data. |
| INS-2 | Apache's `sites-available/proxy-locations.conf` had no `<Location "/egeria-insights">` block, so the public quickstart environment 404'd the app even though the FastAPI container served it fine directly | done | Added the block (mirrors `/egeria-audit`/`/egeria-operations`). Also uncovered and fixed a **stale bind-mount**: a `git stash`/`git stash pop` (atomic rename-based rewrite) desynced the `quickstart-web-server` container's view of this file from disk — same class of issue as the "bind-mount cp hazard" memory. `docker restart quickstart-web-server` re-establishes the mount; watch for this any time a config edit under this repo "doesn't take effect." |
| INS-3 | `/egeria-insights`, `/egeria-audit`, `/egeria-operations` FileResponses had no `Cache-Control` header, and their `<script src="/static/egeria-shared-ui.js">` tags had no cache-busting `?v=` — the same class of bug as `TC-17` (stale shared-JS cache silently breaking newly-added shared functions) | done | Added `Cache-Control: no-store, must-revalidate` to all three `serve_*()` routes and a `?v=2026-07-15a` query string to all three script tags, matching the pattern already used by `tech-catalog.html`/`egeria-explorer`. |
| INS-4 | Search results table had no resizable/sortable columns or filter box, unlike other Explorer panes (Audit's `AuditRelationshipTab`) | done | Ported the shared `useColumnResize`/`colResizeHandle` pattern into `SearchResults` (egeria-insights.html) — resizable + sortable columns, plus a filter input. Bookmarks were already wired at the tab level via `FavoriteButton`. |
| INS-5 | `colResizeHandle`'s visible divider line (shared in `egeria-shared-ui.js`, used by Audit/Operations/Insights/Tech Catalog) was reported as invisible — confirmed present in the DOM with correct geometry, just too faint to notice (2px dotted line at 0.45 opacity, no hover state) | done | Bumped resting opacity to 0.6 and added a mouseenter/mouseleave brighten to 0.9 (imperative style mutation, not React state — `colResizeHandle` is a plain function called per-column inside a `.map()`, so it can't safely use hooks). Benefits every pane using the shared resize handle, not just Insights. |
| PY-15 | See "pyegeria Upstream Bugs" table below | open | Genuine Egeria server bug found while building this feature — not fixable client-side |

---
## 🔴 High Priority — Finish semantic `as_of_time` verification (PY-1/7/9/11 remainder)

**Status:** open
**Added:** 2026-07-15

Full context and the methods already confirmed live in `PYEGERIA_ISSUES.md`
(PY-7/PY-8/PY-9/PY-11). On 2026-07-15, re-verified the pyegeria `as_of_time`
fixes against the **actually deployed** container (pyegeria 6.0.16.18, not
just source) using a *real* test: compare a call with no `as_of_time` against
the same call with `as_of_time="2000-01-01T00:00:00Z"` (before any qs demo
data existed) — a genuine fix returns real data "now" and `"No elements
found"` for the year-2000 call; a fix that's merely accepted-but-ignored
returns the same non-empty result both times.

**Confirmed working (real data, real before/after difference):**
- `CollectionManager.find_note_logs("*", graph_query_depth=0)` — 4 → `"No elements found"`
- `AutomatedCuration.get_technology_type_elements(filter_string="File")` — 108 → `"No elements found"`
- `CollectionManager.get_collection_members("dbc14481-fa8d-42eb-9bce-a7dad33a6779")` — 12 → `"No elements found"`
- `DataDesigner.find_data_structures("*", graph_query_depth=0)` — 94 → `"No elements found"`

**Not yet confirmed — no test data available in this environment, needs follow-up tomorrow:**
1. `GovernanceOfficer.find_information_supply_chains` — need qs demo data with at least one ISC loaded.
2. `GovernanceOfficer.find_governance_definitions` — need at least one governance definition loaded.
3. `DataDesigner.get_data_field_by_guid` — need a real `DataField` GUID (list via `DataDesigner.find_data_fields("*", graph_query_depth=0)` first, pick a GUID from the result, then re-run the before/after test against it).
4. `ProjectManager.get_linked_projects` — tested without a `TypeError`, but the GUID used had no linked projects to show a count difference. Need a project GUID that actually has links (list via `ProjectManager.find_projects("*", graph_query_depth=0)`, or look for one referenced from Egeria Explorer's Projects tab).
5. `DataDesigner.find_data_value_specifications` (PY-1) — the crash fix is confirmed (`AttributeError` is gone), but there's no `DataValueSpecification` data loaded in this environment to confirm `as_of_time` has real effect vs. just being silently accepted. Both "now" and year-2000 calls currently return `"No elements found"` — inconclusive either way.

**How to repeat this tomorrow** (same recipe used for the confirmed methods above):
```python
# Run inside the quickstart-pyegeria-web container:
#   docker exec quickstart-pyegeria-web python3 -c "<script below>"
from pyegeria import <ClientClass>   # e.g. GovernanceOfficer, DataDesigner, ProjectManager
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

mgr = <ClientClass>(view_server="qs-view-server", platform_url="https://host.docker.internal:9443",
                     user_id="peterprofile", user_pwd="secret")
# Note: some classes (DataDesigner, ProjectManager) use `view_server_name=` instead
# of `view_server=` — check with `inspect.signature(<ClientClass>.__init__)` if the
# constructor call raises TypeError.
mgr.create_egeria_bearer_token()

r_now  = mgr.<method>(<required args>, graph_query_depth=0)   # omit graph_query_depth if not accepted
r_2000 = mgr.<method>(<required args>, graph_query_depth=0, as_of_time="2000-01-01T00:00:00Z")
print("now:", len(r_now) if isinstance(r_now, list) else r_now)
print("2000:", len(r_2000) if isinstance(r_2000, list) else r_2000)
# Real fix  -> non-empty count "now", "No elements found" (or empty list) at 2000
# Not fixed -> identical non-empty result both times
```

If any of the 5 remaining methods show identical non-empty results for both
calls (not fixed) rather than `"No elements found"` at 2000, downgrade that
method's status in `PYEGERIA_ISSUES.md` (PY-7/PY-9/PY-11 section) and
`BACKLOG.md`'s PY-9/PY-11 rows accordingly, and note the discrepancy for Dan.

**Also worth doing if time allows:** if any of the "no test data" methods
still have no data tomorrow, check whether demo data can be loaded/created for
that type (an ISC, a governance definition, a DataField, a linked project) so
this can be closed out definitively rather than left inconclusive.

---
## 🔴 High Priority — Fix SecretsStoreCataloguer catalog target (Quickstart)

**Status:** open  
**Added:** 2026-06-23  

The `SecretsStoreCataloguer` integration connector in the Quickstart metadata store has a catalog target pointing to `egeria-user-directory.omsecrets`, which is a Freshstart file. The correct file for Quickstart is `coco-user-directory.omsecrets`.

A symlink (`egeria-user-directory.omsecrets` → `coco-user-directory.omsecrets`) was added to `runtime-volumes/quickstart-platform-data/secrets/` as a temporary workaround — this suppresses the `FileNotFoundException` on every `SecretsStoreCataloguer` refresh but does not fix the underlying misconfiguration.

**Root cause:** A colleague's notebook run added `egeria-user-directory.omsecrets` as a catalog target to the Quickstart metadata store.

**Fix:** Remove or correct the catalog target via the Egeria API or a notebook — update it to reference `coco-user-directory.omsecrets`. Once corrected, remove the symlink.

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

## Platform Runtime / Infrastructure

| # | Item | Status | Notes |
|---|------|--------|-------|
| INFRA-1 | Egeria metadata-store leaks PostgreSQL connections over time | in-progress | The `qs-metadata-store` Postgres repository connector ("PostgreSQL JDBC Driver") accumulates `idle` and `idle in transaction` sessions on the shared `egeria` DB (port 5442) until the 1000-slot pool is exhausted → all metadata queries 500 with `POSTGRES-REPOSITORY-CONNECTOR-500-001 … FATAL: remaining connection slots are reserved for roles with the SUPERUSER attribute`. First hit 2026-06-23: 994/1000 used (833 idle + 161 idle-in-transaction stuck **20+ hrs** on `classification_attribute_value`). Surfaced as Operations-page 500s. **Stopgap:** `docker restart quickstart-egeria-main` (drops to 0; view servers auto-restart ~10s later). **Safety net (done 2026-06-23):** `idle_in_transaction_session_timeout=1800000` (30 min) added to `shared-infra.yaml` postgres `command:`; leaked idle-in-transaction sessions now self-reap rather than accumulating indefinitely. Takes effect on next `docker compose up` of shared-infra. **Still open:** investigate Egeria Postgres connector pool config (max pool size / session release on the connector side) to prevent accumulation in the first place. Watch `idle in transaction` count as the leading indicator (`SELECT state,count(*) FROM pg_stat_activity WHERE usename='egeria_user' GROUP BY state;`). |

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
| PERF-1 | Digital Product catalog tree load is slow — investigate query optimisation | **done (2026-06-21)** | Root cause was **not** the members fetch: `/tree` made an extra `get_collection_by_guid(catalog)` deep-graph call (~12 s) purely for catalog display metadata the frontend never reads — removed it (the frontend already has the catalog from the catalogs list). `get_collection_members(graphQueryDepth=0)` is ~0.25 s. |
| PERF-2 | Evaluate server-side lazy loading for deep catalog trees | **done (2026-06-21)** | `/tree` now returns only the catalog's top level; `_build_tree`'s recursive serial walk replaced by `_children_level` (one level, no recursion). New `GET /api/digital-products/{guid}/children` fetches a node's members on expand. Frontend `DigitalProductsView`/`DigitalTreeNode` lazy-load via a `childrenByGuid` map + `loadingGuids` (one `get_collection_members` call per expand). **Result: 28.4 s → 0.42 s** initial load (432-node catalog), ~0.5 s per expand. **Optional follow-up:** `graphQueryDepth=1` to pre-load the 2nd level (instant top-level expands, heavier payload). **Note:** the same recursive pattern still exists in collections/solution/projects/governance tree endpoints — apply the same fix if they're felt to be slow. |

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

## Egeria Explorer — Valid Values

`/api/valid-values/properties` + `/api/valid-values/lookup` backed by `valid_values_handler.py` (both envs).

| # | Item | Status | Notes |
|---|------|--------|-------|
| VV-1 | Valid Values Explorer tab in type-explorer.html | done | Left sidebar lists all property names that have registered valid values; click a name to load its values in the right pane; values sorted by ordinal; manual search box for arbitrary property names. |
| VV-2 | Fix: type-scoped valid values not returned by lookup | **done (2026-06-24)** | **Root cause:** Egeria REST `/get-valid-metadata-values/{property}?typeName=` returns 0 elements when `typeName` is empty but the values are registered against specific Egeria types (e.g. `annotationType` → `ResourceProfileAnnotation`, `QualityAnnotation`, etc.). The primary `ReferenceDataManager.get_valid_metadata_values` call (which uses that REST endpoint) therefore returned nothing for 40 of the 70 registered properties. **Fix:** added `_fallback_lookup()` in `valid_values_handler.py` — called when the primary lookup returns empty with no `type_name` specified. It calls `MetadataExpert.find_metadata_elements` with `identifier = property_name` and filters out set-header entries (those without `preferredValue`), then normalises the nested `elementProperties.propertiesAsStrings` dict into the same flat format the frontend expects. Verified live: `annotationType` now returns 39 values (was 0). Applied to both envs. |

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
| RS-3 | Filter Report Specs list by Perspective and/or Question | **done** | Perspective dropdown + name/description/question search implemented in `ReportSpecView`; perspectives derived client-side from `question_spec[].perspectives` |

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

Full repro steps (runnable code, expected vs. actual, root cause) for every row below live in **`PYEGERIA_ISSUES.md`**.

| # | Bug | Status | Workaround |
|---|-----|--------|------------|
| PY-1 | `DataDesigner.find_data_value_specifications` calls non-existent `_async_post` | **fixed** — verified 2026-07-14 live on deployed 6.0.16.18 | `_search_data_value_specs()` can likely be simplified to call the method directly now; test before removing the manual workaround |
| PY-2 | `get_data_value_specifications_by_name("*")` rejects wildcard | **not a bug — closed 2026-07-15 (Dan).** `by_name` methods are complete-match lookups (full displayName/qualifiedName), not search; `"*"` was never meant to mean "list all" here | Use `find_data_value_specifications(search_string="*")` (fixed by PY-1) for `DataGrain`/`DataClass` listing — that's what `find_*`/`_by_search_string` is for |
| PY-3 | `find_all_solution_blueprints/components` missing in 6.0.12.2 | **fixed/moot** — both exist on deployed 6.0.16.18 | Use `find_*(search_string="*")` if still on an older pin |
| PY-4 | `ServerClient.update_comment` defaults `merge_update=True` and sets `mergeUpdate: true` in body, but Egeria still rejects the request with `OPEN-METADATA-400-004` requiring `qualifiedName` | done | Workaround already in `egeria_feedback_handler.py`: fetches comment first via `get_comment_by_guid`, extracts `qualifiedName`, builds body manually |
| PY-5 | `get_notes_for_note_log` was unusable in 6.0.14.5 (default `metadata_element_type_name="Action"` → `OMAG-…-404-001` on the NoteLog guid; `="NoteLog"` returned the log not the notes; timed out on big logs) | **fixed in 6.0.14.6** | Default kwargs now return the notes, `page_size`-bounded. **Gotcha:** do *not* pass `metadata_element_type_name="NoteLog"` — now returns 0. `notelog_handler.py` uses the default. |
| PY-6 | `find_note_logs('*')` at default graph depth is O(total notes) — inlines every log's entries (~30s on qs; `page_size` bounds logs, not per-log expansion) | **not a bug** — reclassified 2026-07-14; `graph_query_depth` trading off graph richness vs. speed is intended Egeria behavior, `graph_query_depth=0` is the documented opt-out | List uses `graph_query_depth=0` (≈0.3s, accepted via `**kwargs`); subjects via the depth-0 `Anchors` classification |
| PY-7 | Add `as_of_time` to `ValidMetadataManager.get_valid_metadata_values` (no param, no `**kwargs`) | **reclassified — not a pyegeria fix.** The underlying Egeria REST endpoint (`get-valid-metadata-values/{propertyName}`) doesn't accept `asOfTime` at all; would need an Egeria API change first | Blocks LE-3 time-travel on reference-data / valid-values lists. No client-side fix possible. |
| PY-8 | Add `as_of_time` to `get_technology_type_elements` (no param, no `**kwargs`) | **fixed** — semantically verified 2026-07-15: real data returns 108 elements "now" vs. `"No elements found"` at `as_of_time="2000-01-01"` | Blocks LE-3 time-travel on Tech Type member lists — no longer blocked, ready to wire up |
| PY-11 | Add a direct `as_of_time` param to the `find_*` methods that only accept it via `**kwargs` (silent no-op): `find_information_supply_chains`, `find_governance_definitions`, `find_note_logs`, `find_collections`, `find_data_structures`. | **fixed** — semantically verified 2026-07-15 for `find_note_logs` (4→0) and `find_data_structures` (94→0) against real qs data; `find_information_supply_chains`/`find_governance_definitions` share the same code path but weren't independently data-verified (no loaded data of those types) | LE-3 time-travel on Note Logs, Data Design specs/structures confirmed unblocked; ISC/Governance definitions expected fixed |
| PY-10 | ~~Asset detail by-guid rejects `asOfTime`~~ — **NOT A BUG (closed 2026-06-21).** Root cause found by reading egeria-python + re-testing: `get_asset_graph_by_guid` and `get_asset_by_guid` **do** honour `asOfTime` (verified: `asOfTime=now` returns the element; `Z` format works). The earlier 500/404 were because the demo repo was (re)loaded **2026-06-17**, so test times of 2020 / 2026-06-01 legitimately predate the entity's repository version → Egeria correctly returns "not found at that time" (`OMAG-REPOSITORY-HANDLER-404-007`, surfaced as 404 by the by-guid retrieve and 500 by the graph endpoint). No Egeria/pyegeria change needed. | done | Asset detail pane now time-travels (LE-3); handler degrades a "not found at time" to a clean 404 → friendly "not present at the selected time" message. |
| PY-9 | **Ship the `as_of_time` method updates to the deployed pyegeria.** Local edits to `project_manager` (`get_linked_projects`), `collection_manager` (`get_collection_members`), `data_designer` (`get_data_field_by_guid`) | **resolved** — semantically verified 2026-07-15 for `get_collection_members` on deployed 6.0.16.18 (real collection: 12 members "now" vs. `"No elements found"` at `as_of_time="2000-01-01"`); `get_linked_projects` confirmed no `TypeError`; `get_data_field_by_guid` not independently data-verified | Tree-view + linked-projects + data-field time-travel can now be wired up |
| PY-12 | `ReferenceDataManager` has no specification-property / valid-metadata methods (only inherits `ServerClient`) — easy to assume it covers `SpecificationProperties`' territory since `get_valid_metadata_values` happens to work on it | open (docs/placement) | Use `pyegeria.SpecificationProperties` for `get_specification_property_*`/`find_specification_property` |
| PY-13 | `SpecificationProperties.get_specification_property_by_type` always 400s regardless of the value passed (plain name, or the enum-wrapped form from its own OpenAPI spec) | **reclassified as Egeria server bug** — not fixable in pyegeria; server-side `@RequestParam` enum binding issue | `valid_values_handler.py` uses `find_specification_property("*")` + client-side filter on `properties.identifier` instead |
| PY-14 | `find_specification_property` default `graph_query_depth=3` is O(n) per element (~50s for 1000 elements) — same root cause as PY-6, confirmed on a second method | **not a bug** — reclassified 2026-07-14, same reasoning as PY-6 | Always pass `graph_query_depth=0` on bulk `find_*`/list calls (~0.6-2s for 1000 elements, same flat data minus the graph) |
| PY-15 | Postgres repository connector's `QueryBuilder.getSearchClassificationsClause()` ignores `matchClassifications.matchCriteria` entirely once 2+ classification conditions are given — ANY/ALL/NONE all behave as an unconditional AND, so a query naming two classifications that never co-occur on the same element (e.g. `ZoneMembership` + `Confidentiality`) always returns zero elements instead of the ANY union | **open — genuine Egeria server bug**, root-caused 2026-07-15 while building Egeria Insights. Recommended Java fix (mirrors the `ANY`→`or`/`ALL`→`and` pattern already used for property conditions) is on file; needs to be applied to the Egeria checkout and PR'd upstream | Blocks `insights_handler.py`'s `get_summary()` 5-classification dashboard tally and any multi-classification compound search in Governance Search — both only correct with 0 or 1 classification condition. Regression test added: `egeria-python/tests/functional-tests/test_metadata_expert.py::test_find_metadata_elements_multi_classification_any_match_criteria` (fails now, should pass once the connector fix lands) |
| PY-16 | `ClassificationExplorer.link_elements_as_peer_duplicates`/`_async_link_elements_as_peer_duplicates` (and likely the `unlink_*` detach twin) POST to `.../classification-explorer/elements/{guid}/peer-duplicate/{guid}/attach` — the real Spring endpoint (`ClassificationExplorerResource.java`) is mapped at `.../related-elements/{guid}/peer-duplicate/{guid}/attach` (`elements` vs `related-elements`), so every call 404s | **open — pyegeria client bug**, found 2026-07-16 seeding GAP-5's Duplicate Resolution Review demo pair. Classification calls (`set_known_duplicate_classification` etc.) and the read path (`get_relationships`/`get_elements_by_classification`) are unaffected | Worked around by calling `_async_make_request` directly with the corrected URL to seed demo data; see PYEGERIA_ISSUES.md PY-16 for full repro |
| PY-17 | `MetadataExpert.get_metadata_element_by_guid` never returns relationships regardless of `graph_query_depth` (confirmed identical output at depth 0/1/2/3 against a Notification with known real relationships) | **open — likely docs/usage gap, not a bug**, found 2026-07-16 fixing Action Center cross-links. `get_all_related_elements(guid)` is the call that actually surfaces relationships ({startingElement, elementList, mermaidGraph}) | Fixed in `action_center_handler.py` (calls both, merges). Worth auditing other handlers that assumed `graph_query_depth=1` on a by-guid call would include relationships — not yet checked beyond Action Center; see PYEGERIA_ISSUES.md PY-17 |

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
| TC-13 | Preview data for file Data Assets (when accessible), ideally formatted by type | **done (2026-06-21)** | New `GET /api/tech-catalog/assets/{guid}/preview`: resolves the asset's `pathName` (the Egeria-platform `/deployments/*` path), security-allowlists it under read-only roots (realpath defeats traversal), reads a bounded page via pandas (CSV/TSV/TXT + JSON/JSONL; Parquet unsupported — no pyarrow), returns `{columns, rows, has_more}`. Compose: data dirs mounted **read-only** into pyegeria-web at matching `/deployments/*` (both envs; freshstart mirrors its `exchange-freshstart` dirs). Frontend: the Explorer's `TabularPreviewModal` was generalised to a `fetchUrl` prop and moved into `egeria-shared-ui.js` (Explorer repointed; local copy removed); the Catalog's `AssetDetail` shows a "Preview Data 📊" action for file assets (DataFile subtypes / anything with a file path). Verified live: returns real rows for week7.csv. **Note:** previews only files reachable from the web container ("when accessible"); JSON renders as a flat table (not a tree). |
| TC-14 | `annotationType` property in Annotations and Survey Reports panels | **done (2026-06-24)** | **Surveys → Annotations tab (`AnnotationsTabView`):** (1) loads `annotationType` valid values once on mount via `/api/valid-values/lookup?property_name=annotationType`; (2) derives unique `annotationType` values from the loaded annotation items; (3) renders a secondary filter chip row (indented, left-bordered) below the Egeria-type chips — "All" + one chip per value, toggling a client-side `atFilter` (no extra network request); (4) `annotationType` now appears as a small sub-label inside the Type column cell with the valid-values description as a tooltip. **Survey Report detail pane (`AnnotationsSubPane`):** same valid-values load + secondary filter chip row; chips have description tooltips. **`AnnotationCard`:** shows `annotationType` as a dim sub-line directly below the type badge; if valid values return a `displayName` different from the raw value it appends " — DisplayName"; description appears as a tooltip (`cursor: help`). The `annotationType` property was previously in `skipDisplay` (hidden). Applied to both envs. |
| TC-15 | Generic Authors/Header/Relationships display across all `AuthoredReferenceable` types (both apps) | **done (2026-07-09)** | Root cause: element attributes were being surfaced via hand-picked `fields`/`SCALAR_FIELDS` arrays per Detail component, so new/less-common properties (e.g. `authors` on `AuthoredReferenceable` subtypes) and header/version metadata (createTime/updateTime/createdBy/updatedBy/maintainedBy) were silently dropped. **Backend:** new shared module `common_serialize.py` (`_authored_fields`, `_header_summary`, `_generic_relationships`) imported by all `*_handler.py` serializers; `_generic_relationships` groups every top-level relationship-shaped key on an element into a normalized `{guid, typeName, superTypeNames, displayName, qualifiedName, description, properties}` shape, with a `skip` param per handler to avoid double-listing keys the handler already curates by hand. `project_handler.py`'s `get_project` now requests `graphQueryDepth=2` so relationship arrays are actually present to extract. **Frontend (`egeria-shared-ui.js`, shared by both apps):** `GenericPropertiesTable({item, priority, skip, extra, renderValue})` renders every scalar property generically (Title-Cased for unknown keys, with a small label-override map for common ones); `HeaderInfoButton({header})` is a popover (mirrors the existing mermaid-graph popup pattern) showing GUID/Type/Status/Version/Created/Updated/Maintained By. `GenericRelationshipsSection` (type-explorer.html only — depends on app-local `onNavigateToElement`/linkable-type registry) renders the generic relationship groups with navigable links. Replaced hand-picked field arrays in 13 Detail components across `type-explorer.html` (Project, GovDef, Location, Community, Actor, SolutionBlueprint, SolutionComponent, ISC, ReferenceData, ExternalReference, Agreement, DigitalProduct, NoteLog) and in `tech-catalog.html`'s `AssetDetail` and Glossary components. `ValidValueDetail` intentionally skipped (dead code, never invoked). Verified live via curl against `/api/projects` and `/api/projects/{guid}` — `_header`/`authors`/`relationships` all present and correctly populated. Mirrored to freshstart (freshstart lacks `ExternalReferenceDetail`/`AgreementDetail` — no `external_links_handler.py` backend there — so those two were skipped in the freshstart copy; everything else, including `DigitalProductDetail`, applied identically). Caught and fixed a real bug pre-deploy via a Node+jsdom render-test harness: `GenericPropertiesTable`'s `renderValue` callback was passing raw array values (e.g. `authors`) to callers like `renderMd`, which expects a string and crashed on `.trim()` — fixed by always joining arrays to a string before the callback runs. |

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
| LE-3 | Time slider — generalise as a shared component for Egeria Explorer and Tech Catalog pages | **in-progress** | **Done (2026-06-21):** `TimeSlider` extracted from the Lineage Explorer into `egeria-shared-ui.js` (inline styles, no CSS-class dependency; props `createTime`/`onChange(asOfTimeOrNull)`/`label`). **First page wired — Tech Catalog Data Assets:** the `data-stores`/`data-feeds`/`data-sets` handlers accept `as_of_time` and pass it to `find_data_assets`; `AssetTabView` mounts the slider atop the filter bar (gated to data-asset endpoints) and re-fetches the list on change. Verified live: 92 stores now → 0 as of 2020-01-01. **Per-page recipe for the rest:** (1) backend — add `as_of_time: Optional[str] = Query(None)` to the endpoint, pass `as_of_time=as_of_time or None` to the pyegeria find/get (most accept it — `find_data_assets` natively, `get_asset_graph_by_guid`/`get_asset_by_guid` via `**kwargs`; verify per method); (2) frontend — hold `asOfTime` state, append `&as_of_time=`, add it to the fetch effect deps, mount `TimeSlider({ onChange: setAsOfTime })`. **Done (2026-06-21) — Digital Products + Collections trees:** `_children_level` / `/tree` / `/children` in both `digital_products_handler` + `collections_handler` accept `as_of_time` and inject `asOfTime` into the `get_collection_members` request body (cache-key includes it); `DigitalProductsView` + `CollectionsView` mount the slider and thread `as_of_time` into the tree + lazy `/children` fetches (deps + reset on change). Verified: DP tree 4 children now → 0 as of 2020. **MECHANISM NOTE:** `as_of_time` must go in the request **body** as `asOfTime` — passing it as a pyegeria **kwarg is a silent no-op** in the deployed pyegeria (verified: `get_collection_members(as_of_time=…)` returned unfiltered). Direct-param `find_*` work because they build `asOfTime` into the body internally. Use body-injection for body-taking methods. **Done (2026-06-21) — Data Assets detail pane:** `get_asset_detail` + `_fetch_detail` accept `as_of_time` and inject `asOfTime` into the `get_asset_graph_by_guid` body; `AssetTabView` threads `as_of_time` into the detail fetch. A time before the element's repo-creation degrades to a clean 404 → friendly "🕐 not present at the selected time" message (PY-10 closed — not a bug, just test times predating the demo load). So the **whole Data Assets page** (list + detail) now time-travels. **Done — Tech Catalog (all):** the 9 asset lists + the asset detail pane. **Done — Egeria Explorer:** Digital Products tree, Collections tree, **Locations**, **Communities**, **Perspectives** (+ `/api/projects` flat list backend). **Done (2026-06-24) — Glossary, Projects, Actors:** `glossary_handler.py` — all 5 endpoints (`/api/glossary`, `/glossary/{guid}/folders`, `/glossary/{guid}/terms`, `/glossary-terms`, `/glossary/term/{guid}`) gain `as_of_time`; `find_glossaries`/`find_glossary_terms` use it directly; `get_collection_members` and `get_term_by_guid` receive it via body injection. `project_handler.py` — `/api/projects/tree` and `/api/projects/dependencies` gain `as_of_time`; `_project_forest` passes it to `find_projects`; `_cached_forest` keys on it; `/api/projects/{guid}` injects it into `get_project_by_guid` and `get_linked_projects` bodies. `actor_handler.py` — all 6 endpoints gain `as_of_time`; `_list_route` passes it to `find_actor_profiles`/`find_actor_roles`/`find_user_identities`; detail endpoints inject it into `get_*_by_guid` body. Frontend: `GlossaryView` mounts `TimeSlider` in the glossary-list sidebar; `fetchJson` (lazy folder expansion) also appends `as_of_time`; time change clears search results and re-fetches glossary list + scope. `ProjectsView` mounts slider; all three fetch effects (flat list, hierarchy tree, dep tree) and detail fetch re-run on time change; selection cleared. `ActorsView` mounts slider; time change resets all 3 sub-tab states to `'idle'` (forces re-fetch on next visit) and clears selection. Verified live: actors/profiles, projects/tree, glossary all return 0 items for `as_of_time=2020-01-01`. **Still blocked on pyegeria** (`find_*` `as_of_time` no-op): ISC, governance definitions, note-logs, data-design specs/structures — **PY-11**; reference-data/valid-values — **PY-7**; tech-type member lists — **PY-8**. **Follow-up:** the Lineage Explorer still has its own local `TimeSlider` (it doesn't load the shared module) — adopt the shared one when convenient. |
| LE-4 | Audit all existing handler endpoints — remove `user_id`/`user_pwd` query params and replace with token-only pattern | **in-progress (phased)** | Phased, additive-first. **Phase 1+2 done (2026-06-18):** new shared `egeria_auth.py` (contextvar + `apply_token()` + pure-ASGI `EgeriaTokenMiddleware`); registered in `pyegeria_handler.py`; all 16 query-param handlers now call `apply_token(client)` instead of `create_egeria_bearer_token()`, making them token-capable via `X-Egeria-Token` while staying fully backward-compatible. Verified live: no-token→200, token→200 across glossary/types/projects/perspectives, bogus-token→500 (token is actually applied). **Phase 3 done (2026-06-18, pending interactive spot-check):** `egeriaFetch` + `_tokenRefresher` lifted into `egeria-shared-ui.js` (canonical = the Catalog's `fetchWithToken`); Catalog now aliases `fetchWithToken = egeriaFetch`. Explorer migrated all 51 `fetch(credAppend(...))` sites to `egeriaFetch`, and acquires a token at connect via `/api/egeria-token` (`acquireToken`, gated on an explicit password so persona/blank/server-managed creds keep their existing env/JWT auth — never mints a service-account token) + registers `_tokenRefresher.refresh` for 401 retry. Passwords no longer travel in any URL. Verified live: no-creds→200, token→200; both SPAs mount clean. **Needs browser spot-check in all 3 auth modes (demo-qs persona, local-qs ConnectionForm user+pwd, freshstart JWT).** **Phase 4a done (2026-06-20):** removed the dead frontend `credAppend` helper + stale `credQS`/`credAppend` comments (`62b96ac1`). **Phase 4b (backend query-param removal) — re-scoped, NOT a quick cleanup:** an audit (2026-06-20) found `user_id`/`user_pwd` are woven through the endpoints, not just passed to an env-defaulting factory — they appear in cache keys (`f"…|{user_id or ''}"` in collections/digital_products/solution_architect/project), pagination helpers (`_list_route(…, user_id, user_pwd, …)` in actor), creds dicts (notelog), debug logs (type_system) and direct client constructors (data_design `DataDesigner(server, url, user_id, user_pwd)`, tech_catalog `_creds`, project `_cached_forest`, dr_egeria `_write_and_execute`). A naive param removal `NameError`s across ~20 files. **The security goal (no password in a URL) is already met** by Phases 1–3 (frontend never sends `user_pwd`; token governs auth), so 4b is hygiene (close the latent `?user_pwd=`/`?user_id=` accept surface), not a live fix. **Recommended approach when prioritized:** introduce a shared `Depends`-injected connection-params provider in `egeria_auth.py` (sources url/server from query, user_id/user_pwd from env/token) and replace the four per-endpoint query params + their internal references with it — a dedicated refactor, not a regex blast. tech_catalog/lineage/egeria_feedback already token-aware. |

---

## Modularization

Spec notes in `technical_data_catalog_spec.md` (Modularization strategy section).

Goal: extract the shared UI components that appear verbatim in both Explorer and Tech Catalog into a served static file (`egeria-shared-ui.js`), so changes propagate automatically. Run this workstream **after** Tech Catalog Phase 4 ships — we need both consumers to exist before we can define the stable extraction boundary.

**Short-term mitigation:** Mark shared blocks in Tech Catalog with `// SHARED — keep in sync with type-explorer.html` comments so drift is visible in code review.

| # | Item | Status | Notes |
|---|------|--------|-------|
| MOD-1 | Audit: list all components copied verbatim from Explorer into Tech Catalog; confirm boundary (what to share vs what stays per-tool) | done | See `shared-ui-audit.md`. Boundary: **Tier 1 share-now** (Mermaid family + field constants, ResizeDivider, useResizable, renderMd/_renderMdHtml, VegaChart/AvailableCharts — canonical = richer Explorer version); **Tier 2 share-after-fetch-unification** (credAppend + feedback widgets — blocked by token vs query-param auth split, sequence with LE-4); **Tier 3 per-tool** (ConnectionForm, CredContext provider, tool views). |
| MOD-2 | Extract shared components to `egeria-shared-ui.js` | **done** | **Done (Tier 1):** mermaid family (`MermaidDiagram`/`DiagramPanelFromData`/`AvailableMermaidDiagrams`/`_isMermaidKey`/`_mermaidLabel`/`_MERMAID_*`), robust `copyToClipboard` (execCommand fallback for non-secure http), `useResizable`, and the markdown renderer `renderMd`/`_renderMdHtml` (2026-06-18 — canonical Explorer version with embedded-```mermaid support; inline-code bg moved to a new `--md-code-bg` CSS var so it adapts to each SPA's light/dark theme, fixing a latent mismatch in both). **Done (Tier 2, 2026-06-19):** `EgeriaFeedbackWidget` + `EgeriaCommentsSection` extracted verbatim (byte-identical across all 4 SPA files) — they use bare `fetch()` against cookie-authed `/api/egeria-feedback/*`, so no fetch-seam injection was needed after all; hooks converted to `React.useState`/`React.useEffect` to match module convention. `ResizeDivider` shared (commit 32d906bf). **Done (2026-06-20):** `FeedbackButton` (+ `_SESSION_ID`) shared — canonical = the richer Explorer version; Catalog's stripped-down copy retired via a `pagePrefix="tech-catalog/"` prop (Catalog's demo-feedback form now gains the category dropdown + want-response/consent checkboxes). The audit's "property-table renderer" was a loose note — the two SPAs' property tables render different data and stay per-tool. `VegaChart`/`AvailableCharts` stay Explorer-only. **Tier 2 complete.** |
| MOD-3 | Refactor Explorer + Tech Catalog to import from shared module; remove duplicated blocks | **done** | Both SPAs load `/static/egeria-shared-ui.js` and consume the Tier-1 components (local dups removed). **Glossary tree shared (2026-06-18, commits c12eeb33+1a04560d):** `GlossaryTermRow`+`GlossaryTreeNode` extracted with injected `fetchJson`; Catalog Glossary rewritten from breadcrumb to the shared twistie-tree. **Feedback widgets shared (2026-06-19):** local `EgeriaFeedbackWidget`/`EgeriaCommentsSection` blocks removed from both `type-explorer.html` and `tech-catalog.html` (qs + fs); now consumed from `egeria-shared-ui.js`. **Credentials unified + mermaid shared (2026-06-20):** `CredContext` + canonical `DiagramPanel`/`MermaidSection` moved to `egeria-shared-ui.js`; the Catalog now wraps its App in `CredContext.Provider` (was prop-drilling; its mermaid had used a bare credential-less fetch — latent bug in token/ConnectionForm modes, now fixed). **Glossary detail panes shared (2026-06-20):** `GlossaryFolderDetail`/`GlossaryDetail`/`GlossaryTermDetail` + `_glsBadge` unified on the **Catalog visual design** (Properties/Classifications cards), removed from both SPAs. Folder pane gains the `MermaidSection` context graph (was Explorer-only). Term pane takes optional cross-link callbacks + an injected `isElementLinkable` predicate. **Catalog Data-Design cross-links (MOD-4, 2026-06-20):** Catalog `TYPE_TO_NAV` extended with the DataSpec/Structure/Field/Grain/Class types → deep-link the Explorer's Data Design tab (`?guid=&kind=#data-design`); `GlossaryView` now resolves term-relationship links via the existing cross-app `handleNavigate`. Explorer `DataDesignView` gained a `?guid/?kind` cold-load fallback so those deep-links actually select the target. **MOD-3 complete.** |

---

## Session Reliability & Async Fixes (2026-06-26)

Changes made to address long-running session failures (timeouts, token expiry, stale nav) surfacing in the demo site and long-lived notebooks.

### pyegeria / egeria-python — `_client.py` / `_base_platform_client.py`

| # | Item | Status | Notes |
|---|------|--------|-------|
| SR-1 | httpx connection pool settings | done | `AsyncClient` now created with `keepalive_expiry=20 s`, `connect` timeout 10 s, `max_connections=10`, `max_keepalive_connections=5`. The 20 s keepalive prevents dead-connection errors when a reverse proxy (nginx/Caddy default: 60–75 s idle timeout) closes an idle socket while pyegeria still holds it in the pool. Applied to both `pyegeria/_client.py` and `egeria-python/pyegeria/core/_base_platform_client.py`. |
| SR-2 | `__exit__` async-close bug | done | `__exit__` called `self.session.aclose()` without `await`, so the session was never closed when using the client as a sync context manager. Fixed to `loop.run_until_complete(self.session.aclose())`. Applied to both repos. |
| SR-3 | 401 auto-refresh | done | `_async_make_request` now detects 401/403 and, if `token_src == "Egeria"`, calls `_async_refresh_egeria_bearer_token()` and retries once (`_retrying=True` flag prevents loops). Externally-supplied tokens (`set_bearer_token`) are not auto-refreshed. Applied to both repos. |

### egeria-workspaces — `PyegeriaWebHandler`

| # | Item | Status | Notes |
|---|------|--------|-------|
| SR-4 | `egeria_auth.py` — `async_apply_token` | done | Added async counterpart to `apply_token`. Calls `await client._async_create_egeria_bearer_token()` directly so async FastAPI routes can build a client without triggering `RuntimeError: This event loop is already running` (which the sync `create_egeria_bearer_token()` would cause via its internal `run_until_complete`). |
| SR-5 | `operations_handler.py` — async routes | done | `list_integration_connectors` and `server_status_overview` were sync routes using `asyncio.get_event_loop().run_until_complete()` to drive async fan-out. Converted to `async def`; added `_runtime_manager_async` and `_automated_curation_async` factories using `async_apply_token`. The `_async_get_server_report` call is now directly awaited, eliminating the sub-loop pattern that fails on Python 3.10+ when the event loop is already running. This is the primary fix for the integration-connectors pane timeout on the demo site. |
| SR-6 | `audit_handler.py` — async routes | done | `list_users` and its `_user_names` fallback helper both used `asyncio.get_event_loop().run_until_complete()`. Converted both to `async def`; added `_security_officer_async` factory. The N=81 concurrent user-account fan-out now runs natively in the event loop. |
| SR-7 | `type_system_handler.py` — async client factory | done | `get_type_names` and `get_all_types` are `async def` routes but called the sync `_get_client()` → `apply_token()` → `create_egeria_bearer_token()` chain, which raises `RuntimeError` inside a running loop. Added `_get_client_async()` that uses `async_apply_token`; both routes now use it for the no-token path. The token-expired fallback path in `get_all_types` is also fixed. |
| SR-8 | `tech_catalog_handler.py` — async token creation | done | `get_egeria_bearer_token` is an `async def` route that called sync `mgr.create_egeria_bearer_token()`. Changed to `await mgr._async_create_egeria_bearer_token()`. |
| SR-9 | `egeria-operations.html` — platforms list auto-refresh | done | The platforms/servers list was fetched once on page load and never refreshed, leaving the left-nav stale when servers started, stopped, or were added. Added a 30-second `setInterval` poll in the `useEffect`. Cleanup (`clearInterval`) is returned from the effect so it fires correctly on unmount and credential change. The error handler no longer blanks the nav on a transient network hiccup. |

### Documentation

| # | Item | Status | Notes |
|---|------|--------|-------|
| SR-10 | `egeria-python/docs/user_programming.md` — Long-Running Sessions section | done | New section covering httpx connection settings, automatic token refresh scope, and the async-context rule (`_async_create_egeria_bearer_token` vs sync `create_egeria_bearer_token`). Error-handling section extended with exception-class table. |
| SR-11 | `egeria-python/AGENTS.md` — HTTP stack invariants | done | Four bullet points added under the `_base_platform_client.py` architecture entry: keepalive invariant, 401 retry, `__exit__` async rule, async context rule. Guards against accidental regression by AI coding assistants. |
| SR-12 | `egeria-workspaces-fs/CLAUDE.md` — async handler pattern | done | See CLAUDE.md: rule added that new async FastAPI routes must use `*_async` client factories and `async_apply_token`; sync factories are for sync routes only. |
| SR-13 | `egeria-workspaces-fs/AGENTS.md` — PyegeriaWebHandler async rule | done | See AGENTS.md: async invariant added to the PyegeriaWebHandler section. |

---

## Egeria Advisor — Intent Button Redesign (2026-06-26)

Redesign the seven intent buttons to match a cleaner four-mode model: Learn / Find / Author / Execute.

| # | Item | Status | Notes |
|---|------|--------|-------|
| IB-1 | Add `Create` intent + `CreateRouter` | open | Routes to PlanElicitor or ReportSpecElicitor based on query verb/domain. Remove `Plan` button. See design notes in `egeria-advisor/CLAUDE.md`. |
| IB-2 | Expand `Act` to cover report execution + Dr.Egeria commands | open | Verb-based split: SHOW/LIST/GET → ReportPipeline; CREATE/UPDATE/ASSIGN/… → DrEgeriaActionAgent. After a successful run offer "Save as Report Spec" and "Refine columns" follow-up actions. |
| IB-3 | Expand `Show me` to surface Dr.Egeria templates and report specs | open | ExamplesAgent already handles code examples. Add Dr.Egeria template search and catalog report spec listing to the same response. |
| IB-4 | Expand `Inspect` to cover all repos (egeria-workspaces, egeria-advisor, egeria-java) | open | Currently pyegeria-only. Needs multi-repo code index or targeted file-read path for workspaces config, FastAPI handlers, compose files. |
| IB-5 | Rename `Report` button → `Run Report` in UI | open | Clarifies that Report = execute existing spec, not build a new one. Small label-only change in `index.html`. |
| IB-6 | Add "Fork / Customize →" affordance per report in sidebar | open | Opens Report Spec Builder pre-populated from the clicked spec. Covers "extend a report" without cluttering the Act flow. |
| IB-7 | Ad-hoc query in Act: post-run "Save as Report Spec" button | open | After Act runs a report or ad-hoc exec, offer lightweight follow-up: [Save as Report Spec] [Refine columns] [Run again with filter]. No pre-run prompt. |

---

## Egeria Advisor — Vector Index Expansion (2026-06-26)

Expand the indexed document corpus so `Explain` can answer questions from all Egeria repos and docs.

| # | Item | Status | Notes |
|---|------|--------|-------|
| IX-1 | Index `egeria-python/docs/*.md` into `egeria_general` (or new `egeria_sdk_docs` collection) | open | Includes `output-formats-and-report-specs.md`, `user_programming.md`, `dr_egeria_manual.md`, etc. |
| IX-2 | Index `egeria-advisor/docs/**/*.md` (user-docs + design) | open | User guides, design docs, LGCI guide, report spec guide. Low volume; can go into `egeria_general`. |
| IX-3 | Index READMEs from egeria-workspaces-fs, egeria-python, egeria-advisor, egeria-java | open | Root READMEs and key sub-project READMEs. Gives Explain a "what is this repo / how do I set it up" capability. |
| IX-4 | Index `CLAUDE.md` and `AGENTS.md` files from all repos | open | Useful for Inspect queries about conventions, architecture invariants, design rules. |
| IX-5 | Add incremental indexer job for the above (so new doc edits are picked up) | open | Extend `advisor/incremental_indexer.py` collection list; add cron or watch trigger. |

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
