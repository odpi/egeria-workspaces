# SHARE-3 phase 1 — one copy of the low-risk Portal files (PO-64)

Branch `claude/share3-phase1`, based on `upstream/main` 21cf7057 (odpi #905).

## What changed

Freshstart's Egeria Portal (`compose-configs/egeria-freshstart/PyegeriaWebHandler`)
now uses quickstart's copy of four files:

| File | Diff lines before (qs vs fs) | Result |
|------|----:|--------|
| `static/egeria-shared-ui.js` | 1204 | shared |
| `perspectives_handler.py` | 43 | shared |
| `type_system_handler.py` | 193 | shared |
| `digital_products_handler.py` | 278 | shared |
| `collections_handler.py` | 547 | **not shared** — blocked, see below |
| `tech_catalog_handler.py` | 214 | **not shared** — blocked, see below |

(Counts are `diff | grep -c '^[<>]'` on 21cf7057; the brief's counts were on laz/next b41069bb.)

Quickstart's copy is canonical. Freshstart holds a byte-identical mirror.
`compose-configs/shared-portal-files.txt` lists the shared files;
`compose-configs/sync_shared_portal_files.py` copies quickstart → freshstart
(`--check` reports differences and exits 1); `tests/test_shared_portal_files.py`
fails CI when the two copies differ, when a shared file is dropped from the
list, when a per-environment file is listed, or when a copy is committed as a
symlink. CI (`python-tests.yml`) runs it as its own step.

**To change a shared file:** edit quickstart's copy, run
`python3 compose-configs/sync_shared_portal_files.py`, commit both.

## How the files are shared, and why this way

**Chosen: canonical copy plus a sync script and a CI drift check.**

The deciding fact: freshstart's pyegeria-web is **bind-mounted**, not only baked.
`egeria-freshstart.yaml` builds the image from `./PyegeriaWebHandler`
(`Dockerfile-fast-api`, `COPY . .`) *and* mounts `./PyegeriaWebHandler:/app`
at run time (line ~210), as quickstart does. Whatever is in that directory on
the host is what the container runs.

| Option | Verdict |
|--------|---------|
| Build context / extra `COPY` from `../egeria-quickstart` | **Rejected.** The `./PyegeriaWebHandler:/app` bind mount hides whatever the image copied in, so the extra COPY never reaches the running container. Making it work would mean per-file bind mounts in compose; single-file bind mounts go stale (they pin the inode, and `git checkout` replaces it — the bind-mount hazards already hit on laz). It would also change the Helm image's build context (below). |
| Symlinks `egeria-freshstart/…/x → ../../egeria-quickstart/…/x` | **Rejected.** A relative link out of `PyegeriaWebHandler/` dangles inside the container: only that directory is mounted at `/app`. Docker does not follow a symlink out of a build context, so the image builds (compose and Helm) would `COPY` a broken link. Windows checkouts without `core.symlinks` get a text file holding the path. |
| **Sync script + CI drift check** | **Chosen.** Freshstart keeps real files, so the image build, the bind mount, Helm and Windows all work unchanged. The cost is two copies on disk; the test makes the second a mirror that cannot drift unnoticed. This is the same model SHARE-1 used for `type-explorer.html` ("byte-identical"). SHARE-1 had no guard, and the file has drifted since — this phase adds the guard. |

### Consumers checked (moving-files-across-boundaries)

Nothing is moved or renamed: both paths still hold a regular file with the same
name. So every consumer that names only an ancestor directory still finds a real
file. Each is listed below with how it was checked, and with what goes wrong if the
file is missing (silently, in most cases).

| Consumer | Names | How checked | Result |
|----------|-------|-------------|--------|
| Compose image build, both envs | `build.context: ./PyegeriaWebHandler`, `Dockerfile-fast-api` `COPY . .` | read `egeria-{quick,fresh}start.yaml` + both Dockerfiles (identical) | real files are in the context → baked |
| `.dockerignore` | — | `ls -a` both `PyegeriaWebHandler/` | none in either env; nothing excluded |
| Compose bind mounts, both stacks | `./PyegeriaWebHandler:/app` (quickstart and freshstart) | read both compose files | the host file is what runs. **A merge is live at once on any host whose checkout is bind-mounted** (laz quickstart: no quickstart file changes here; any freshstart checkout: the four mirrors change on merge) |
| App static mount | `_static_dir = SCRIPT_DIR / "static"`, `NoCacheStaticFiles` | `pyegeria_handler.py` both envs; pinned by `test_shared_js_is_what_the_pages_load` | `/static/egeria-shared-ui.js` = the env's own mirrored file; `Cache-Control: no-cache`, so no `?v=` bump |
| Apache `/static` | freshstart `sites-available/fastapi-ssl.conf` → `freshstart-pyegeria-web:8000/static`; quickstart `proxy-locations.conf` → `quickstart-pyegeria-web:8000/static` | read both; pinned by the same test | each env's browser gets its own env's copy; Apache serves no file of its own |
| Pages loading the JS | `<script src="/static/egeria-shared-ui.js?v=…">` in 7 freshstart / 9 quickstart pages | pinned by the same test (every `src` must be that path) | no page loads a different or inline copy |
| Python import resolution | `import type_system_handler` etc. from `/app` | `test_python_module_resolves_to_the_shared_copy` (find_spec from each env dir; no second file of that name anywhere in the tree) | both trees import the mirrored file, not a stale copy |
| package-data / MANIFEST.in / pyproject | — | `PyegeriaWebHandler/` is not a package (no pyproject, setup or MANIFEST) | n/a |
| CI globs | `codeql.yml` `compose-configs/egeria-*/PyegeriaWebHandler/**.py`; `python-tests.yml` | read | still matches; one new step runs the drift test |
| Dependabot | directories | read `.github/dependabot.yml` | unaffected |
| Sync scripts | `.claude/skills/dr-egeria-command-sync` (templates only) | `git grep` for writers into either `PyegeriaWebHandler/` | none other; the new sync script is the only writer |
| **TR-112a Portal images** (cray; `dwolfson/egeria-workspaces` `tr112-helm-charts-phase1`, read at 5c07714e, branch tip now d94b23f9) | `Dockerfile-portal-image` per env, context `egeria-<env>/PyegeriaWebHandler`, `COPY . .`; `charts/tests/proof112a.sh` line 21 build loop; `README-portal-images.md` table | `git grep` on 5c07714e (read-only, branch not edited) | **needs no change.** Option (b), real files in both trees, held identical by the drift test: freshstart's context already holds the mirrored files. Option (a), widening the context to `compose-configs/` with explicit COPYs, was not needed. A symlink or a separate shared directory would have been missing from these images (docker does not follow links out of the context) |

**For TR-112a, when it lands on main:** its two `Dockerfile-portal-image` files are
byte-identical (blob b89d9ef2). Add `Dockerfile-portal-image` to
`shared-portal-files.txt` and to `SHARED_FLOOR` in the same PR, so the drift test
guards them too. It can't be listed now because the file is not on main. Nothing else
in proof112a.sh or the README needs to change.

### Proof beyond syntax

`node --check` and `py_compile` only prove the files parse. FIX-13 passed both and
still shipped ReferenceErrors and dropped props. What was checked instead:

- **Free identifiers in the shared JS** (TypeScript parser; every identifier
  referenced but declared nowhere in the file): only `React` (host global) and
  `resolveTypeNav` (behind a `typeof` check). The old freshstart copy had the same
  two, so sharing adds no new free identifiers. (The check is file-wide, not per scope:
  it finds names that are undeclared everywhere in the file.)
- **Prop plumbing:** every top-level function in both versions was compared by its
  parameter list. Only two changed, and both only gained an optional prop:
  `MermaidDiagram({code}` → `{code, label})` (label defaults to "Diagram") and
  `MermaidSection({guid}` → `{guid, data})` (data only dedupes chips). All 21
  freshstart call sites (9 `MermaidDiagram`, 12 `MermaidSection`) pass `{code}`/`{guid}` as before. No freshstart page
  changed, so no `selection`-style page prop can have been dropped.
- **Global-scope clashes:** no freshstart page redeclares a shared name with
  `const`/`let`/`class`, which would blank the page with a SyntaxError (now a test:
  `test_pages_do_not_redeclare_shared_js_names_lexically`). The `function`-vs-`function`
  overlaps (`getChain`, `getAllProps`, `getSubs`, `highlightHtml`, `MermaidDiagram`
  in lineage-explorer, …) are equivalent implementations; the page's copy wins.
- **Python:** pyflakes reports no undefined names in the three shared handlers
  in either tree. Freshstart's `pyegeria_handler` imports. Its OpenAPI includes
  `/api/types/classification-purposes` and `/api/digital-products/mesh`, with
  `/mesh` before `/{node_guid}`. Every name other freshstart modules import from the
  shared files exists (AST check), and every local name the shared files import
  exists in freshstart.
- **Quickstart's own tests for the shared files, run against freshstart's tree**
  (below): this is the behavioural proof.

## Per file: what was kept, added and gated

Every hunk was sorted into (a) a quickstart feature freshstart should get,
(b) a freshstart fix quickstart lacks, or (c) a real environment difference.
In the four shared files **every hunk was (a)**: none was (b) or (c), so
nothing needed a runtime gate, and no `DEMO_MODE`/`SERVER_MANAGED_AUTH` branch
was added or changed. Freshstart's copy is replaced wholesale by quickstart's.

### `perspectives_handler.py` — 9 hunks, all (a) — **fixes PO-65**
- **PO-65** (freshstart's Perspective/Question detail ignored `as_of_time` and
  returned 500 for a missing GUID): fixed by sharing. Before: Perspective detail
  accepted `as_of_time` but sent `{"graphQueryDepth": 1, …}` without `asOfTime`;
  the Questions list and detail had no `as_of_time`; Question detail sent depth 2;
  a stale GUID raised 500. Now both details send `_detail_body(as_of_time)`
  (depth 5, 250 nodes, `asOfTime` when set), the Questions list passes `as_of_time`,
  and `PyegeriaNotFoundException` → 404.
- Added: `as_of_time` on the Questions list/detail (As-of slider reaches Egeria);
  shared `_detail_body()` (graph depth 5, 250 mermaid nodes; was 1 and 2);
  404 instead of 500 for a missing GUID (`PyegeriaNotFoundException`);
  `relationshipType` on related-element items.
- Kept: freshstart's PO-59 fix (Perspectives list and detail routes) is already in
  quickstart's copy — same routes, same body.

### `type_system_handler.py` — all (a)
- Added: `GET /api/types/classification-purposes` and `classificationPurpose`
  fields on `/api/types` classification defs. **`egeria-shared-ui.js` calls this
  endpoint, so the two are shared together.**
- Added: `?user_id=` is no longer read on `/api/types`, `/api/types/names`,
  `/api/types/relationship-purposes`: identity comes from the X-Egeria-Token
  bearer token, else the env service account. On freshstart the token is always
  present for a signed-in user, so behaviour is unchanged; an old caller that still
  sends `user_id` is ignored (FastAPI drops unknown query parameters), not refused.

### `digital_products_handler.py` — all (a)
- Added: `GET /api/digital-products/mesh` (Data Mesh graph); `as_of_time` on catalogs
  and node detail; detail depth 5 / 250 nodes; tree caches keyed on the hashed
  credential (`result_cache.request_identity`, already identical in both envs)
  instead of a bare `user_id`, and skipped for an expired token; an auth failure
  while reading members is now a 401/403 (`raise_if_auth_error`), not an empty tree;
  related elements deduped by GUID; diagram keys via `graph_keys` (identical in
  both envs).
- Response-key rename: second-hop related elements are now `<key>RelatedElements`
  (was `<key>Appointments`). No freshstart page or script reads the old key
  (checked all `*.html` and `static/*.js`).
- Kept: every name other freshstart modules import from this file still exists
  (`collections_handler.py`'s `_get_manager`, `_serialize_node`, … and `get_node`,
  whose new `as_of_time` parameter is guarded for direct Python calls).

### `static/egeria-shared-ui.js` — 26 hunks, all (a)
- Freshstart-only lines were all earlier partial ports of quickstart code (the
  2026-08-15 bulk-action sync: `getSubs`/`getAllSubs`/`useTypeGraph`, catalog search,
  comments saying "ported from quickstart"); quickstart's copy holds the same code.
  Quickstart's top-level names are a strict superset of freshstart's.
- Added: `GraphTabs` (one chip bar for all diagrams), Activity/Root/Full-lineage
  graph labels, the As-of family (`AsOfContext`, `useAsOf`, `asOfParam`,
  `CurrentNotAsOfNote`), classification-purpose grouping (`useClassificationPurposes`
  and friends), `ClassificationModal`/`useApplicableClassifications`, shared
  `getChain`/`getAllProps`, `loadOwnedPersona`/`saveOwnedPersona` (QS-10).
- Environment check, done by hand since nothing here branches on the mode:
  - `loadOwnedPersona` is only called by pages; freshstart's one caller
    (`resource-browser.html`) reaches it only when `server_managed_auth` is false,
    i.e. never on freshstart. It previously guarded the call with `typeof` because
    the function was missing.
  - `ClassificationModal` calls `/api/classification/*`, which freshstart does not
    serve, but no freshstart page renders it (only quickstart's `type-explorer.html`
    and `tech-catalog.html` do). Unused code on freshstart until those pages are shared.
  - No `AsOfContext.Provider` in freshstart pages → `useAsOf()` is null → requests are
    byte-identical to before (no `as_of_time`).
  - `MermaidSection` reads `/api/mermaid/{guid}`'s `graphs` and falls back to
    `mermaidGraph`, so freshstart's mermaid handler still renders.
  - `AssignedElementsSection` now says "Could not look up" on a failed request instead
    of "No … elements are assigned" (absence ≠ none).
- Global-name collisions with freshstart pages (pages load after this file):
  `type-explorer.html` declares its own `getChain`/`getAllProps` (new collisions;
  `function` vs `function`, so no SyntaxError — the page's copy wins) and they are
  equivalent to the shared ones. All other collisions existed before. No page
  declares a shared name with `const`/`let`/`class`.

## Not shared in this phase (left as separate copies)

- **`collections_handler.py`** — quickstart's copy imports
  `report_specs_handler._stamp` and `egeria_auth.lineage_scope`, neither of which
  exists in freshstart. Both files are out of scope (later phases). Sharing it
  now would fail at import / first request. Also changes `/api/collections/roots`'
  default answer (summary rows of every collection, not RootCollections only),
  which freshstart's drifted `type-explorer.html` would need to be checked against.
  → Share after `egeria_auth.py` and `report_specs_handler.py`.
- **`tech_catalog_handler.py`** — quickstart's copy imports `remember_token`,
  `reusable_token`, `token_reuse_key`, `token_reuse_lock` from `egeria_auth`
  (PO-40 token reuse) and `READ_LIMIT` from `semantic_links`; freshstart's
  `egeria_auth.py` (out of scope — auth model) has none of them.
  → Share with or after `egeria_auth.py`.

**DEFERRED — PO-40 N1 (token reuse)** lives in `egeria_auth.py` (`remember_token`,
`reusable_token`, `token_reuse_key`, `token_reuse_lock`), which is out of scope (the
auth model, a later phase). It is why `tech_catalog_handler.py` is not shared, and
quickstart's `test_po40_token_reuse.py` fails at setup against freshstart's tree
(below). Freshstart keeps minting a token per request until `egeria_auth.py` is shared.

No hunk in the shared files was left unclassified.

## Noticed, not fixed (out of scope)

- `type-explorer.html`, `tech-catalog.html` and `egeria-overview.html` differ between
  the envs although ENVIRONMENT_DIVERGENCE.md calls them converged (SHARE-1 said
  byte-identical). They are the "big pages" of a later phase; the manifest and test
  here are the place to pin them once converged.

## Tests

Python 3.12 venv: the env's `requirements.txt`, `pyegeria==6.3.0` (what the live
quickstart container runs), pytest, pytest-asyncio, schemathesis. `tests/browser` is
excluded and `EGERIA_PLATFORM_URL` unset. The baseline is upstream/main 21cf7057 (a
`git archive` of the whole tree), **not** the parent commit. Failures are compared by
name. Every suite ran twice, with `DEMO_MODE=false` and `SERVER_MANAGED_AUTH=false`
(quickstart mode) and `=true` (server-managed). Note: the quickstart suite makes
read-only search calls to the local platform at `localhost:9443` (its conftest
says so).

### Both env suites

| Suite | Mode | upstream/main | this branch | New failures |
|-------|------|---------------|-------------|--------------|
| quickstart | SMA=false | 4 failed, 2015 passed, 1 skipped | same | none |
| quickstart | SMA=true  | 5 failed, 2014 passed, 1 skipped | same | none |
| freshstart | SMA=false | 150 passed | 150 passed | none |
| freshstart | SMA=true  | 150 passed | 150 passed | none |
| `tests/test_shared_portal_files.py` (new) | — | — | 21 passed | — |

The quickstart failures are the same on both trees and unrelated to this change. The
quickstart tree is byte-identical to upstream/main:
`test_golden_anchors.py::test_work_item_list_detail_matches_known_seed_data`,
`::test_work_item_list_membership_matches_known_seed_data`,
`test_openlineage_topic_owner.py::test_data_hub_batch_no_longer_runs_the_notebook`,
`::test_no_batch_runs_the_notebook`, and with SMA=true only,
`test_report_specs_sources.py::test_sync_route_reports_status_and_refuses_a_second_start`.

### Quickstart's tests for the shared files, run against freshstart's tree

Freshstart has few tests of its own for these files, so the 15 quickstart test files
that exercise a shared file were copied, with their fixtures, into scratch copies of
freshstart's `PyegeriaWebHandler` at upstream/main and at this branch, and run in both modes.
Two files can't even be collected against freshstart, and are not in the counts:
`test_md_cell_br_js.py` reads quickstart-only `local-dashboards.html`;
`test_semantic_links_capped.py` needs `semantic_links.READ_LIMIT`, which is not shared.

| freshstart tree | SMA=false | SMA=true |
|-----------------|-----------|----------|
| upstream/main | 131 failed, 29 errors, 280 passed | same |
| this branch   | 52 failed, 18 errors, 370 passed | same |

**90 fixed, 0 new.** The 70 still failing on this branch all test a file this phase
does not share:
- `test_po40_token_reuse.py` (18 errors): `egeria_auth.py`, PO-40 N1, DEFERRED.
- `test_as_of_panels.py` (20): the TimeSlider views in `type-explorer.html`,
  `tech-catalog.html` and `lineage-explorer.html` (pages), plus `mermaid_handler`,
  `glossary_handler`, `semantic_links` and `tech_catalog_handler`'s debug route.
- `test_app_bar_consistency.py` (6): `portal-docs/` pages, which freshstart doesn't have.
- `test_cache_credential_identity.py` (10): `collections_handler` (not shared),
  `solution_architect_handler._build_component_groups`, `tech_catalog_handler._build_survey_types`.
- `test_graph_keys.py` (6): `isc_handler`, `mermaid_handler`,
  `governance_definitions_handler`, `tech_catalog_handler`, `collections_handler`.
- `test_classification_purpose_js.py::test_type_explorer_wiring`,
  `test_graph_tabs_js.py::…only_mermaidGraph…`: `type-explorer.html` wiring (a page).
- `test_soa_controls_js.py` (8): the SoA view in `type-explorer.html` (a page).

The drift test was checked to fail when a freshstart copy is edited, when a
per-env file (`demo_config.py`) is listed, when a floor file is dropped from the
list, when a stray `old/type_system_handler.py` shadow copy is added, and when a
freshstart page declares `const GraphTabs`.

**Not verified:** freshstart pages in a browser with the new `egeria-shared-ui.js`
(freshstart needs a real Egeria login; it cannot be smoked headlessly). Suggested
smoke after deploy: Egeria Explorer type pages, a detail pane's Diagrams chip bar and
Classifications section, Perspectives detail with the As-of slider set, Digital
Products tree.
