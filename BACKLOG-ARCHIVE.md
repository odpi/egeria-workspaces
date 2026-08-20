# Egeria Workspaces — Backlog Archive

Fully closed work items, split out of `BACKLOG.md` ahead of the 6.1 release
so the live backlog stays focused on what's actually open. Content moved
here verbatim, unedited — history, not a place to add new notes. See
`BACKLOG.md` for anything still open or in progress.

---

## Fix: REST APIs view — blank screen (2026-08-18) — ✅ done (quickstart only)

Dan reported the REST APIs view (Egeria Explorer → Reference → REST APIs) loaded to a blank
screen. Two independent bugs, both fixed:

1. **Backend (`rest_api_handler.py`)**: `_fetch_openapi()` fetches the Egeria platform's OpenAPI
   spec via a plain unauthenticated `requests.get`. That used to be enough; it no longer is —
   confirmed live: `/v2/api-docs` and `/api-docs` now 401 anonymous (moving to 404, i.e. genuinely
   not found, once a valid bearer token is supplied); `/v3/api-docs` — the real, working path —
   times out anonymous but returns 200 in ~21s with a token. Fixed by minting a bearer token
   (reusing the per-request `X-Egeria-Token` via `egeria_auth.get_request_token()` if present,
   else a fresh one from env-var credentials) and sending it as `Authorization: Bearer`. Also
   bumped the fetch timeout 30s → 60s — the real ~21s fetch was already close to the old timeout
   even once auth stopped being the blocker, a genuine flakiness risk on its own. Verified live:
   cold fetch (explicit `/api/rest-apis/refresh` first) → 200, 56 services, correct shape.
2. **Frontend (`type-explorer.html`'s `RestApiView`)**: `loadOpenApi()` called `r.json()`
   unconditionally without checking `r.ok` — a non-2xx error response (e.g. the 502 the backend
   bug above was producing, `{"detail": "..."}`) parses as valid JSON with no `services` key,
   gets stored via `setOpenapi(d)` anyway, and the `services` `useMemo`'s
   `openapi.services.filter(...)` then throws `TypeError: Cannot read properties of undefined` on
   the next render — an uncaught render error, which is what actually produced the blank screen
   (not the 502 itself; a handled error would have shown `apiError` text instead). Fixed by
   checking `r.ok` and throwing with the server's `detail` message on failure so it lands in
   `.catch()` properly, plus a defensive `Array.isArray(openapi.services)` guard in the `useMemo`
   itself so a future response-shape surprise degrades to an empty list instead of a blank screen
   again. General lesson: any `egeriaFetch(...).then(r => r.json())` pattern that doesn't check
   `r.ok` first has this exact failure mode waiting — worth a grep across the other views if this
   class of bug shows up again.

---

---
## Fixes (2026-07-26) — ✅ done

| # | Item | Status | Notes |
|---|------|--------|-------|
| FIX-1 | The Catalog — Technology Type detail showed `[object Object]` instead of the description text | done | Root cause: `TechTypeDetail` (`tech-catalog.html`, both envs) wrapped `renderMd(item.description)` in `dangerouslySetInnerHTML: { __html: ... }` — but `renderMd()` (shared `egeria-shared-ui.js`) returns a **React element**, not an HTML string (it already applies its own `dangerouslySetInnerHTML` internally). Setting `__html` to a React element object coerces it to the string `"[object Object]"` when the browser sets `innerHTML`. Every other call site (e.g. `GlossaryTermDetail`) already uses the correct pattern — `renderMd(...)` rendered directly as a child. Fixed by rendering it as a child instead of re-wrapping. Verified live against `CSV Data File`'s Technology Type detail. |
| FIX-2 | Egeria Overview dashboard — "Back to Portal" link was broken (pointed to `/`, the FastAPI health-check JSON endpoint, not `/portal`); dashboard also had no "Share your feedback" affordance, unlike every other portal app | done | `egeria-overview.html`: fixed the header link to `/portal` (was silently landing on `{"status":"ok",...}`). Added a vanilla-JS "💬 Feedback" floating button + panel (this app has no React runtime, unlike the other SPAs) posting to the same `/api/demo-feedback` endpoint with the same field shape as the shared React `FeedbackButton` component, so entries land in the same `feedback` table/admin-review flow (FB-5..FB-9). Verified live: opens, submits, shows the thank-you state, `POST /api/demo-feedback` → 200. |
| FIX-3 | Search (The Catalog + Egeria Explorer) — clicking a search result for a type The Catalog doesn't own (Valid Values, Actors, etc.) silently wrapped the correct detail content in **The Catalog's "Data Assets" chrome**, mislabeling every such result as Catalog content | done | Root cause: `tech-catalog.html`'s `?guid=` deep-link resolver (`App`'s element-nav effect) defaulted `sec = (nav && nav.section) \|\| 'data-assets'` whenever the resolved type wasn't in `TYPE_TO_NAV` — so any non-Catalog type landed in the Data Assets section instead of an honest "not found" state. Both search paths fed this: The Catalog's own `SearchResultCard` reload-to-`/tech-catalog?guid=` fallback for `categoryId==='other'` results, and Egeria Explorer's `ExplorerSearchView` → `↗ Catalog` fallback for types outside its own (more complete but not exhaustive) `_elementIsLinkable` allowlist. **Fix:** removed the `data-assets` default; unresolved types now show a new `UnresolvedElement` panel ("This is a ‹Type› — it isn't part of The Catalog", guid shown, "Open in Egeria Explorer ↗" + "⌂ Catalog home") instead of any Catalog section chrome. Both the guid-resolver and `SearchResultCard`'s fallback now hand off to Egeria Explorer's search tab pre-filled with the query (`/egeria-explorer?q=…#search` — added `?q=` seeding to `type-explorer.html`'s top-level `searchQuery` init, mirroring its existing `glossaryNavGuid`/`digitalProductNavGuid` deep-link pattern). Verified live end-to-end: a `ValidMetadataValue` search result now hands off correctly from both apps (Explorer search re-runs pre-filled, 46 results); a direct `?guid=` link to the same element shows the new panel; a legitimate `GlossaryTerm`/Catalog-owned guid still resolves in-app with no regression. Broader "should Search live at the Portal level instead of per-app" question captured separately as **NEXT-12** (low priority, needs discussion). |

---

---
## NEXT-5 / NEXT-6 — Actor community relationships + systematic audit (2026-07-22 → 2026-07-26) — ✅ done

**Original report:** community relationships weren't showing up on Actor
detail; Dan asked for the same class of gap (relationships/classifications
silently missing because of which pyegeria call/depth a screen happens to
use) to be audited across other tools too, not just fixed one-off.

**NEXT-5 resolution — false alarm, root-caused 2026-07-26.** The original
investigation concluded PersonRole `ac694a80-c063-44cd-bd65-abc87cab646e`
("Community Member of Data Science special interest group") had *no*
relationship key pointing back to its community, "even in the raw payload."
That check used `/api/debug/raw/{guid}`, which defaults to
`MetadataExpert.get_metadata_element_by_guid` — and per **PY-17** (confirmed
"working as designed," not a bug), that specific method never returns
relationships at *any* `graph_query_depth`. The investigation was
inadvertently testing the wrong pyegeria method, not the one the app
actually uses.

The real app code path — `ActorManager.get_actor_role_by_guid(guid,
graph_query_depth=1)`, called from `actor_handler.py`'s own
`GET /api/actors/roles/{guid}` — **already returns the community correctly**,
via the role's `assignmentScope` relationship. Confirmed live two ways:
- API: `relationships.assignmentScope[0]` = `{typeName: "Community",
  displayName: "Data Science special interest group", ...}`.
- UI: the Role detail page's mermaid diagram shows a `Contributor
  [Assignment Scope]` edge straight to the Community node, and the page
  needs no code change — `_serialize_actor_element`'s generic
  relationship-section logic already surfaces it.

No fix was needed. (Separately, `actor_handler.py` already has a real,
deliberate enrichment — `_enrich_person_communities` — for the *Person's own*
detail page, which needs a second hop since `assignmentScope` sits on the
Role, not directly on the Person; that one **was** a genuine gap and was
already fixed earlier this session.)

**NEXT-6 audit — systematic pass across all handlers, 2026-07-26.** Result:
**this bug class was already systematically closed**, earlier in the
project, via a shared `common_serialize.py` module:
- `_generic_relationships(element, skip=...)` — groups every top-level
  relationship-shaped key (list-of-dicts or single dict, `RelatedMetadataElementSummary`-shaped)
  into relationship sections, replacing hand-picked key lists that silently
  drop anything not explicitly named. (`business_capability_handler.py`'s own
  docstring cites this exact problem and a regression test:
  `test_business_capability_dependency_relationship_key`.)
- `_classifications(element)` / `_classifications_from_metadata_expert(element)`
  — the same dual-shape classification extraction as
  `tech_catalog_handler.py`'s original fix, centralized so every handler gets
  it free.
- Adopted by 21 of ~30 metadata-detail handlers directly; `actor_handler.py`,
  `community_handler.py`, `context_events_handler.py`,
  `digital_products_handler.py` (+ `agreements_handler.py`/
  `collections_handler.py`, which reuse its `_extract_all_rels`),
  `perspectives_handler.py`, and `glossary_handler.py` each carry a local,
  structurally-equivalent generic extractor (glossary's also has a dedicated
  `_group_related_terms` for term-to-term semantics, plus a generic
  `_extract_extra_rels` catch-all for anything else).
- Checked every collection/project/solution-architect/digital-product **tree**
  endpoint (the other bug shape — classifications missing on *traversed*
  nodes, per the original Tech Catalog schema fix): all delegate to
  serializers that already call `_classifications`/`_extract_classifications`,
  so tree nodes aren't missing them either. `lineage_handler.py` also calls
  `AssetCatalog.get_asset_graph_by_guid` (the method with the known
  classification gap) but never attempts to surface node classifications at
  all, so there's nothing to silently drop there.
- No other genuine instance of this bug class found.

**Conclusion:** no further code changes required for either item. Worth
remembering for *future* handlers: use `common_serialize._generic_relationships`/
`_classifications` from the start rather than hand-picking keys, and don't
trust `/api/debug/raw/{guid}` (or any `MetadataExpert.get_metadata_element_by_guid`
call) as evidence that a relationship doesn't exist — see PY-17.

---

---
## Egeria Explorer — UI polish
    
    | # | Item | Status | Notes |
    |---|------|--------|-------|
    | UI-1 | Collections home-page card icon should match the others (blue outline, not emoji) | done | `_SPLASH_CAPABILITIES` Collections icon changed `'🗂'` → `'❐'` (monochrome, inherits `var(--accent)`). |
    | UI-2 | Remove duplicate sidebar titles that double the page header bar | done | Removed the hardcoded sidebar-title divs in `NoteLogView`, `LocationsView`, `CommunityView` (ISC already done). ProjectsView/ActorsView unaffected. |
  

---
## Mermaid Graphs copyable — ✅ done
  add a button/gesture to mermaid graphs to allow the raw mermaid text to be copied to the clipboard.
  **Done:** `MermaidDiagram` (type-explorer.html + tech-catalog.html) now shows a "⧉ Copy source" button that copies the raw mermaid text with a "✓ Copied" confirmation.


---
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

---
## Fix: Tech Catalog / Egeria Explorer classifications missing on schema elements (2026-07-22) — ✅ done

Dan reported classification info seemed to have been lost in recent updates.
Investigation found the top-level asset classifications badge and the
type-system CLASSIFICATIONS browser were both fine — the real gap was that
schema-tree nodes (`RelationalTable`/`RelationalColumn`, etc., from the
Schema section rebuilt earlier this week) never carried classification data
at all:

- `AssetCatalog.get_asset_graph_by_guid`'s `relatedElement.elementHeader`
  never populates `classifications` for graph-traversal results — confirmed
  live: `None` for every node in RETAILSCHEMA's tree, even though the SAME
  guid's top-level asset fetch (`get_asset_by_guid`) DOES return real
  classification data. Not something recent edits broke; `_serialize_schema`
  simply never had a `classifications` field to populate.
- Fix (`tech_catalog_handler.py`, both envs): added
  `_extract_classifications_from_metadata_expert()` — a second extractor
  alongside the existing `_extract_classifications()`, because
  `MetadataExpert.get_metadata_element_by_guid`'s raw shape is different (a
  real top-level `classifications` list with `propertyValueMap`-wrapped
  properties, vs. AssetCatalog's classifications-as-named-keys-on-header).
  `_serialize_schema`'s existing per-guid supplementary `MetadataExpert`
  lookup (previously only used to resolve nodes AssetCatalog left as a bare
  `startingElementGUID`) now runs for every node in the tree, attaching real
  classification data.
- Frontend (`tech-catalog.html`, both envs): extracted each schema-tree row
  into its own `SchemaRow` component (needed local `useState` for a
  per-row expand toggle) — rows with classifications get a `FoldTriangle` +
  count badge; toggling reveals a sub-row with the same classification-card
  rendering used for top-level asset classifications (typeName + full
  properties dict, not just a badge — Dan specifically flagged that some
  classifications carry detailed property dictionaries worth showing in
  full). Also wrapped the existing top-level asset "Classifications" block in
  `Collapsible`, matching the "foldable everywhere" rule from NEXT-4.
- Verified live end-to-end against RETAILSCHEMA's `CUSTID`/`CUSTNAME`/etc.
  columns (now show a real `TypeEmbeddedAttribute` classification with
  `dataType`/`schemaTypeName` properties).

---

---
## Fix: Foldable section indicator — large turning triangle (2026-07-21) — ✅ done

Dan asked for it to be visually obvious that sections like Schema and
Relationships are foldable, and wanted a large "turning" triangle applied as
a general design rule, not a one-off for those two sections.

- Added one canonical component, `FoldTriangle`, to `static/egeria-shared-ui.js`
  (both envs, kept byte-identical as usual) — a single `▶` glyph rotated via
  CSS `transform: rotate()` + `transition`, 16px (up from the old 10-11px
  chevrons), so it visibly turns 0°→90° on toggle instead of instantly
  swapping characters (▾/▸ or ▲/▼).
- Rewired the shared `Collapsible` component to use it — this automatically
  upgrades `RelationshipSection` in `type-explorer.html` (the ~30 call sites
  behind every Detail panel's relationship groups) with zero further changes,
  since it already delegated to `Collapsible`.
- Applied directly to `tech-catalog.html`'s `SubPane` (both the "prominent"
  and normal header variants — this backs Schema, Lineage, and the
  Relationships block) and `AnnotationsSubPane`, in both envs.
- Scope: this covers every **foldable section header** (Collapsible/SubPane/
  Annotations) — the pattern semantically matching Schema/Relationships.
  Deliberately left untouched: the small tree-navigation expand/collapse
  chevrons in `type-explorer.html`/`tech-catalog.html`/`egeria-shared-ui.js`
  (dozens of instances) — a different UX pattern (hierarchical tree
  drill-down, not section show/hide). Flagged for Dan in case he wants those
  addressed too as a follow-up.
- Checked egeria-audit.html/egeria-operations.html/egeria-insights.html for
  the same generic section-fold pattern — none found (their relationship UIs
  are already specialized/tabbed, not this generic collapsible-section
  pattern), so no changes needed there.

**Follow-up (same day):** Dan liked the look and asked to standardize it
across *every* collapsible/expandable affordance, explicitly including the
hierarchical tree drill-downs that were deliberately left out above.
Extended `FoldTriangle` (`egeria-shared-ui.js`, both envs) to take optional
`onClick`/`size`/`style` so it can slot into tree-node rows (which often
need the arrow itself clickable, independent of row selection, and a
smaller footprint at deep nesting) while keeping the same glyph/rotation
everywhere. Converted every remaining `▲/▼`/`▸/▾`/`▶` fold-toggle glyph in
`type-explorer.html` and `tech-catalog.html` (both envs) — tree nodes
(entity/classification/relationship side-nav, glossary tree, ref-data tree,
location tree, solution-components tree, pyegeria-docs class tree, note-log
rows), collapsible parameter groups (Optional Parameters, Advanced), and a
multi-select dropdown's open/closed indicator. Left untouched: two `▶ Run`
execute-button icons and one `▶ ` "first pipeline step" marker in Tech
Catalog's process view — neither is a fold/expand affordance.

---

---
## Fix: Tech Catalog Schema section always empty (2026-07-21) — ✅ done

Dan reported: for a data asset like RetailSchema, the Schema section is
always empty because the schema elements were flattened into the generic
"Relationships" section above instead. Root-caused and fixed in
`tech_catalog_handler.py` (both envs):

- `get_asset_schema` was calling `AssetMaker.get_asset_by_guid`, which never
  nests attribute relationships under `el["schemaType"]["relatedElement"]` at
  any graph depth — confirmed live. Switched to `AssetCatalog.get_asset_graph_by_guid`
  (the same call the main asset detail view already successfully uses via
  `_fetch_detail`), whose response carries a separate top-level `relationships`
  list covering the whole reachable subgraph.
- That list has no explicit parent/child marking — each entry only carries
  `startingElementGUID` (confirmed NOT reliably "the parent"; it can be
  either end) and `relatedElementAtEnd1`. Empirically confirmed against
  RetailSchema's real hierarchy (`DeployedDatabaseSchema -[Schema]->
  RelationalDBSchemaTypeList -[RelationalDBSchema]-> RelationalDBSchemaType
  -[AttributeForSchema]-> RelationalTable -[NestedSchemaAttribute]->
  RelationalColumn`) that the parent is `relatedElement` when `atEnd1` is
  True, `startingElementGUID` otherwise. Rewrote `_serialize_schema` to walk
  the flat list into a real tree using that rule, anchored at the asset's own
  `schemaType` so unrelated schema instances the same broad traversal picks
  up elsewhere (e.g. a shared physical table catalogued under a different
  schema) are naturally excluded.
- A further gap: some tree nodes (the intermediate `RelationalDBSchemaType`,
  and several columns) only ever appear as a bare `startingElementGUID` in
  this response, never as a fully-described `relatedElement` — their own
  displayName/typeName simply isn't present anywhere in it. Added a
  supplementary `MetadataExpert.get_metadata_element_by_guid` lookup (depth
  0, cheap) per unresolved node, confirmed live these are real schema
  elements (e.g. a `CUSTSTATUS` column), not noise.
- Updated `SchemaPane` in `tech-catalog.html` to render the resulting tree
  with indentation (previously a flat table, which is why even a partially-
  correct fix wouldn't have shown the real nesting). Verified live: RetailSchema
  now shows its full 4-level structure — schema type → RETAILSCHEMA schema
  detail → CUSTOMER table → 4 columns (CUSTID, CUSTNAME, CUSTSTATUS, CUSTCARD),
  correctly ordered by position.

---

---
## Fix: Lineage Explorer blank screen on asset selection (2026-07-21) — ✅ done

Dan reported: search for an asset works fine, but selecting one to view its
lineage shows a blank screen with no visible console error. Two real bugs
found and fixed, plus a systemic robustness gap:

1. **`tech_catalog_handler.py` — genuine backend TypeError** (both envs, 3
   call sites: the classification-diagnosis endpoint, `get_asset_schema`, and
   a fallback in the generic asset-detail lookup). All three called
   `mgr.get_asset_by_guid(asset_guid=guid, ...)`, but pyegeria's real
   parameter name is `guid`, not `asset_guid`. Because the method also
   accepts `**kwargs`, the wrong keyword name was silently absorbed instead
   of raising "unexpected keyword argument" — so it failed with `TypeError:
   get_asset_by_guid() missing 1 required positional argument: 'guid'`,
   a 500 on `/api/tech-catalog/assets/{guid}/schema` any time this fallback
   path was hit. Confirmed via `inspect.signature` against the installed
   pyegeria and fixed by renaming the keyword; verified live (both a
   genuinely-missing guid and a real one now behave correctly instead of
   crashing).
2. **`lineage-explorer.html`'s `MermaidDiagram`** (both envs) had an
   asymmetric try/catch: `window.mermaid.initialize(...)` was wrapped in
   `try/catch(_){}`, but the very next line, `window.mermaid.render(...)`,
   was not. `window.mermaid` loads from a blocking external CDN `<script
   src>` — if that request is slow, blocked (ad-blocker, restrictive
   network), or fails, `window.mermaid` stays undefined and the unguarded
   `.render()` call throws synchronously inside a `useEffect`. Wrapped the
   whole effect body and added an explicit "Mermaid library failed to load"
   inline message instead of an uncaught throw.
3. **No Error Boundary existed anywhere in this ~1200-line app.** React's
   default behavior for an uncaught render/effect error with no boundary is
   to unmount the *entire* tree — turning any single bug (like #2 above, or
   any future one) into exactly the reported symptom: a totally blank page,
   with the actual error easy to miss in the console. Added a class-based
   `ErrorBoundary` wrapping `<App>`, so any future uncaught error shows a
   readable message + reload button instead of silently blanking the page.

**The actual original root cause, found once the Error Boundary above made
the crash visible instead of silent:** `lineage-explorer.html` (quickstart
only — freshstart's copy never had this feature) referenced `FavoriteButton`
in the Focus Asset Card header, but never loaded `/static/egeria-shared-ui.js`
(where `FavoriteButton` is actually defined) — the file only pulled in the
mermaid CDN script. `ReferenceError: Can't find variable: FavoriteButton`
fired on every render of the Focus Asset Card whenever a persona was active
(`favPersonaId &&` short-circuits past it otherwise, which is why this
depends on being logged in as a persona to reproduce). Fixed by adding the
shared script include, positioned so this page's own local
`MermaidDiagram`/`TimeSlider`/`ResizeDivider`/`useResizable` (all
independently defined in this file, all still active) safely take
precedence over the shared file's same-named versions via normal
last-declaration-wins `function` redeclaration semantics.

Note: browser-based live reproduction was attempted but the Chrome
automation tool gave unreliable results this session (reported a 200 success
for a POST that the container's own server logs show as a 404) — root-caused
via direct backend calls (curl with a real egeria-token, replicating
`fetchWithToken`'s exact request shape) and static analysis instead once that
became clear.

---

---
## Fix: relationships disappear after collection toggle-close/reopen (2026-07-20) — ✅ done

Dan reported: open a Collection, select a member, relationships show fine;
toggle the collection closed and reopen it, select a member — relationships
no longer appear. Traced to `CollectionsView`'s (and identically-patterned
`DigitalProductsView`'s) `handleSelect`/detail-fetch-`useEffect` pair in
`type-explorer.html`:

1. `handleSelect` unconditionally called `setNodeDetail(null)` on every
   click, but the fetch effect only reruns when the selected guid actually
   *changes*. A tree container's `onClick` fires `onSelect` on itself every
   time it's toggled open/closed — so toggling a collection closed then
   reopening it reselects the collection each time, and if that leaves
   `selectedNode` unchanged, the wipe fires with nothing to trigger a
   refetch, leaving the pane blank until a genuinely different node is
   picked. Fixed by moving the clear inside the effect (only runs on real
   guid changes).
2. Neither fetch effect guarded against out-of-order async responses — a
   slow fetch for a previous selection could resolve after a faster one for
   the current selection and clobber it. Added the standard `cancelled`-flag
   cleanup guard.

Also found and fixed the same missing-guard-#2 in Solution Architect's
blueprint/component detail fetch (same `DigitalTreeNode` pattern; didn't have
bug #1 since its `onSelect` doesn't eagerly clear). No other `DigitalTreeNode`
call sites in the file. Both envs.

---

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
| PY-15 | See "pyegeria Upstream Bugs" table below | **fixed** — server bug fixed and verified live 2026-07-17, see the PY-15 row in that table | Genuine Egeria server bug found while building this feature — not fixable client-side |

---

---
## 🔴 High Priority — Finish semantic `as_of_time` verification (PY-1/7/9/11 remainder)

**Status:** closed 2026-07-31 — 4 of 5 remaining methods confirmed genuinely
time-scoped; the 5th remains inconclusive for lack of test data (not a
pyegeria defect, just no `DataValueSpecification` demo data in this
environment); a real, separate (non-`as_of_time`) bug found and filed as
PY-22 along the way. Full detail in `PYEGERIA_ISSUES.md`'s PY-7/PY-9
sections and the new PY-22 section.

**2026-07-31 results:**
1. `SolutionArchitect.find_information_supply_chains` (moved off
   `GovernanceOfficer` since this was filed — no such method exists there
   anymore) — **confirmed**: 18 → `"No elements found"`.
2. `GovernanceOfficer.find_governance_definitions` — **confirmed**: 100 →
   `"No elements found"`.
3. `DataDesigner.get_data_field_by_guid` — **confirmed**: real data "now" →
   `PyegeriaAPIException` / `OMAG-REPOSITORY-HANDLER-404-007` ("not found")
   at year-2000 — the correct by-guid-getter equivalent of a find method's
   empty result.
4. `ProjectManager.get_linked_projects` — **still not confirmed, but now for
   a real reason**: checked all 29 qs demo projects, every one returns `"No
   elements found"` from this method, including "Sustainability Campaign"
   which demonstrably has a real `ProjectHierarchy` relationship (visible in
   `get_project_by_guid`'s own `managedProjects` field). This isn't a
   test-data gap — `get_linked_projects` itself doesn't surface real
   relationship data at all. Filed as **PY-22**. Substituted
   `get_project_by_guid`'s `managedProjects` field for the `as_of_time`
   check instead (that field does carry real data): confirmed genuinely
   time-scoped (404 at year-2000) — so `as_of_time` itself works fine on
   `get_project_by_guid`, `get_linked_projects` has an unrelated bug.
5. `DataDesigner.find_data_value_specifications` (PY-1) — still no
   `DataValueSpecification` demo data loaded (same as 2026-07-15), still
   genuinely inconclusive. Loading real test data would close this out;
   deliberately not done without being asked (writes to the shared demo
   environment).

**Added (historical, 2026-07-15):**

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

---
## Egeria Explorer — Data Preview

| # | Item | Status | Notes |
|---|------|--------|-------|
| DP-1 | Adjustable column widths in tabular dataset preview | done | Drag-to-resize on column right-edge handles; dotted separators |
| DP-2 | Row filtering in dataset preview | done | Filter bar above table; client-side on current page |
| DP-3 | Row sorting in dataset preview | done | Click column header to sort (↑/↓/↕); numeric-aware; `e.stopPropagation` keeps resize handle separate |
| DP-4 | Search within table preview | done | Merged with DP-2 — same filter input covers full-text search across all cells |

---


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


---
## Freshstart — Admin & User Management

| # | Item | Status | Notes |
|---|------|--------|-------|
| FS-1 | Admin edit user — show all current values; roles/groups as checkboxes (not multi-select highlights) | done | Checkbox lists implemented in demo-admin.html with pre-populated values |
| FS-2 | My Profile page (`/profile`) — self-service display name, job title, description + password change | done | `demo-profile.html` exists and is wired into the handler |
| FS-3 | Portal greeting reads org name from `application.properties` | done | `get_org_name()` in auth handler; `/api/platform/org-name` endpoint; portal fetches and renders it |
| FS-4 | Delete `demo_db.py` — no SQLite in freshstart | done | File no longer present |

---


---
## Egeria Explorer — Performance

| # | Item | Status | Notes |
|---|------|--------|-------|
| PERF-1 | Digital Product catalog tree load is slow — investigate query optimisation | **done (2026-06-21)** | Root cause was **not** the members fetch: `/tree` made an extra `get_collection_by_guid(catalog)` deep-graph call (~12 s) purely for catalog display metadata the frontend never reads — removed it (the frontend already has the catalog from the catalogs list). `get_collection_members(graphQueryDepth=0)` is ~0.25 s. |
| PERF-2 | Evaluate server-side lazy loading for deep catalog trees | **done (2026-06-21)** | `/tree` now returns only the catalog's top level; `_build_tree`'s recursive serial walk replaced by `_children_level` (one level, no recursion). New `GET /api/digital-products/{guid}/children` fetches a node's members on expand. Frontend `DigitalProductsView`/`DigitalTreeNode` lazy-load via a `childrenByGuid` map + `loadingGuids` (one `get_collection_members` call per expand). **Result: 28.4 s → 0.42 s** initial load (432-node catalog), ~0.5 s per expand. **Optional follow-up:** `graphQueryDepth=1` to pre-load the 2nd level (instant top-level expands, heavier payload). **Note:** the same recursive pattern still exists in collections/solution/projects/governance tree endpoints — apply the same fix if they're felt to be slow. |

---


---
## Egeria Explorer — Home Page

| # | Item | Status | Notes |
|---|------|--------|-------|
| HOME-1 | Reorganise Explorer cards into Act / Review / Reference groups matching the menu bar | done | Three labelled sections with blurb lines; cards reordered to match nav menu membership |

---


---
## Egeria Explorer — Projects

| # | Item | Status | Notes |
|---|------|--------|-------|
| PROJ-1 | Projects card + tab — list projects via `ProjectManager`; show project hierarchy and other dependencies | done | `project_handler.py` backend; `ProjectsView` + `ProjectDetail` in type-explorer; sidebar list + child project cards; search filters by name, description, classification |
| PROJ-2 | Classification-based project-kind display | done | `ProjectKindBadge` component with per-kind colours (Campaign=blue, StudyProject=green, PersonalProject=amber, Task=red, GlossaryProject=indigo); shown in sidebar list, detail header, and child cards; classification properties shown in expandable detail cards |

---


---
## Egeria Explorer — Valid Values

`/api/valid-values/properties` + `/api/valid-values/lookup` backed by `valid_values_handler.py` (both envs).

| # | Item | Status | Notes |
|---|------|--------|-------|
| VV-1 | Valid Values Explorer tab in type-explorer.html | done | Left sidebar lists all property names that have registered valid values; click a name to load its values in the right pane; values sorted by ordinal; manual search box for arbitrary property names. |
| VV-2 | Fix: type-scoped valid values not returned by lookup | **done (2026-06-24)** | **Root cause:** Egeria REST `/get-valid-metadata-values/{property}?typeName=` returns 0 elements when `typeName` is empty but the values are registered against specific Egeria types (e.g. `annotationType` → `ResourceProfileAnnotation`, `QualityAnnotation`, etc.). The primary `ReferenceDataManager.get_valid_metadata_values` call (which uses that REST endpoint) therefore returned nothing for 40 of the 70 registered properties. **Fix:** added `_fallback_lookup()` in `valid_values_handler.py` — called when the primary lookup returns empty with no `type_name` specified. It calls `MetadataExpert.find_metadata_elements` with `identifier = property_name` and filters out set-header entries (those without `preferredValue`), then normalises the nested `elementProperties.propertiesAsStrings` dict into the same flat format the frontend expects. Verified live: `annotationType` now returns 39 values (was 0). Applied to both envs. |

---


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

---
## Egeria Explorer — Feedback & Comments (FB-1/2/3/5/6/7/8/9)

**Two distinct feedback systems:**

- **(A) Egeria Feedback** — Likes, Ratings, Comments on Egeria objects, via the Egeria/pyegeria
  feedback API. **Identical in every environment.**
- **(B) User Feedback** — the "Feedback" button on every tool page capturing the end user's opinion
  *of the tool/page itself*, persisted to a **Postgres table** (in the shared `demo` schema) so we
  can analyse how to improve the tools and Egeria. The **user identity attached differs by env**
  (the only intentional difference); the capture schema and UI are otherwise the same everywhere.

| # | Item | Status | Notes |
|---|------|--------|-------|
| FB-1 | Egeria comments on property sheets | done | Glossary Term + Digital Product detail panes; type dropdown; history list |
| FB-2 | Likes + ratings on remaining detail panes | done | `EgeriaFeedbackWidget` on all property detail panes. ReportSpecDetail excluded — pyegeria format specs have no Egeria GUID. |
| FB-3 | Comments (`EgeriaCommentsSection`) on remaining detail panes | done | `EgeriaCommentsSection` on all property detail panes. ReportSpecDetail excluded — same reason as FB-2. |
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
## Self-hosted Kroki, remove pyegeria's public kroki.io dependency (2026-07-20) — ✅ done

Dan reported intermittent "Kroki error 400 ... Failed to launch the browser
process ... crashpad" failures rendering Mermaid diagrams in Jupyter
notebooks, plus inconsistent diagram colors between runs. Root cause:
`pyegeria.view.mermaid_utilities.render_mermaid()` called the **public**
`https://kroki.io` service directly and unconditionally — Jupyter notebook
users had no visibility into that dependency, and the failures were kroki.io's
own infrastructure (a shared, multi-tenant headless-Chromium renderer)
crashing under its own load, plus its bundled Mermaid version drifting over
time. Not fixable by tuning local container resources, since the Jupyter
container was never doing the rendering.

**Fix — pyegeria (`egeria-python` repo):**
- `pyegeria/core/config.py`: new `egeria_kroki_url` setting (`EGERIA_KROKI_URL`
  env var), empty by default — no default guess at any specific container.
- `pyegeria/view/mermaid_utilities.py`: `render_mermaid()` rewritten as a
  two-tier fallback, no more silent external network call:
  1. **Local Kroki** — only attempted if `EGERIA_KROKI_URL` is explicitly set;
     short (5s) timeout so a dead local service falls through fast.
  2. **Client-side rendering** — if tier 1 isn't configured or fails, the
     diagram renders entirely in the notebook's own browser via mermaid.js,
     inside a sandboxed `<iframe srcdoc="...">` (JupyterLab 4.x strips
     top-level `<script>` tags from HTML outputs; an iframe is its own
     document so its scripts still execute). Reuses the existing
     `construct_mermaid_web` HTML (refactored into a shared
     `_build_mermaid_client_html` helper) rather than duplicating it.
  - The public kroki.io is no longer called anywhere in this path.

**Fix — egeria-workspaces-fs (this repo):**
- `compose-configs/shared-infra/shared-infra.yaml`: new `kroki` +
  `kroki-mermaid` services (`yuzutech/kroki` + `yuzutech/kroki-mermaid`
  companion, internal-network only, no host port). `kroki-mermaid` sets
  `shm_size: 1gb` — the standard fix for the exact "Failed to launch the
  browser process" Chromium/Docker crash Dan reported, same pattern already
  used for Postgres in this file.
- `compose-configs/shared-infra/ensure-shared-infra.sh`: added `kroki
  kroki-mermaid` to the build/up service lists and a `wait_for_container_state`
  check.
- `compose-configs/shared-infra/README.md`: documented the new service.
- Both `egeria-quickstart.yaml`/`egeria-freshstart.yaml`'s Jupyter service:
  `EGERIA_KROKI_URL: "http://egeria-shared-kroki:8000"`.

**Update (2026-08-14):** kroki's host port was later published (`egeria-shared-kroki's port to the host`,
b9bcee9a) as `8000:8000`, then moved to `6002:8000` — `8000` collided with `mkdocs serve`'s default port on a dev
machine. Container-internal port is still `8000` (unaffected); see the port table below and `shared-infra.yaml`.

**Verified live:**
- `/health` on the new `egeria-shared-kroki` container: healthy, Mermaid 11.15.0.
- 8 consecutive `/mermaid/svg` renders: byte-identical output every time (no
  crashes, no theme drift) — the exact two problems reported.
- Cross-container reachability confirmed from `quickstart-pyegeria-web` over
  `egeria_network`.
- Copied the modified pyegeria source into `quickstart-jupyter-work-full`
  (not yet a published pyegeria release) and confirmed both fallback tiers
  live: local-Kroki-configured-and-up → SVG via local container;
  local-Kroki-configured-but-unreachable → falls through to the client-side
  iframe path. Container restored to its pinned pyegeria release afterward.

**Follow-up resolved:** the `render_mermaid()` fix (`egeria-python` commit
`d389a79`) is confirmed **shipped in pyegeria 6.1.0 on PyPI** and deployed
live — `quickstart-pyegeria-web`'s `pip show pyegeria` reports 6.1.0.
`render_mermaid()` no longer has any code path that reaches kroki.io.

---
