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
name, so every consumer that names an ancestor keeps working.

- **Dockerfiles** — both envs' `Dockerfile-fast-api` are identical and `COPY . .` from
  `PyegeriaWebHandler/`. No `.dockerignore` in either env.
- **Compose** — `./PyegeriaWebHandler:/app` in both envs. Freshstart already builds
  Jupyter and Apache from `../egeria-quickstart`; pyegeria-web is unchanged.
- **Static cache** — `/static` is served `Cache-Control: no-cache`
  (`NoCacheStaticFiles` in `pyegeria_handler.py`), so freshstart browsers revalidate
  the new `egeria-shared-ui.js` without a `?v=` bump. Pages were not touched.
- **CI** — `codeql.yml` globs `compose-configs/egeria-*/PyegeriaWebHandler/**.py`
  (still matches). `python-tests.yml` gains one step. Dependabot watches
  directories, not these files.
- **Sync scripts** — `.claude/skills/dr-egeria-command-sync` syncs templates, not
  these files. No other script in the repo writes into either `PyegeriaWebHandler/`.
- **TR-112 Helm (`dwolfson/egeria-workspaces` branch `tr112-helm-charts-phase1`)** —
  **not affected.** Its `Dockerfile-portal-image` (one per env) uses build context
  `PyegeriaWebHandler/` and `COPY . .`, the same as compose. Real files arrive in
  the image; symlinks would have dangled, which is one more reason they were
  rejected. If TR-112 later bakes a single image for both envs, the manifest tells
  it which files are common.

## Per file: what was kept, added and gated

Every hunk was sorted into (a) a quickstart feature freshstart should get,
(b) a freshstart fix quickstart lacks, or (c) a real environment difference.
In the four shared files **every hunk was (a)**: none was (b) or (c), so
nothing needed a runtime gate, and no `DEMO_MODE`/`SERVER_MANAGED_AUTH` branch
was added or changed. Freshstart's copy is replaced wholesale by quickstart's.

### `perspectives_handler.py` — 9 hunks, all (a)
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

No hunk in the shared files was left unclassified.

## Noticed, not fixed (out of scope)

- `type-explorer.html`, `tech-catalog.html` and `egeria-overview.html` differ between
  the envs although ENVIRONMENT_DIVERGENCE.md calls them converged (SHARE-1 said
  byte-identical). They are the "big pages" of a later phase; the manifest and test
  here are the place to pin them once converged.

## Tests

Python 3.12 venv with the env's `requirements.txt`, `pyegeria==6.3.0` (what the live
quickstart container runs), pytest, pytest-asyncio and schemathesis; `tests/browser`
excluded; `EGERIA_PLATFORM_URL` unset. Failures compared by name.

| Suite | upstream/main 21cf7057 | this branch | New failures |
|-------|------------------------|-------------|--------------|
| quickstart `PyegeriaWebHandler/tests` | 4 failed, 2015 passed, 1 skipped | 4 failed, 2015 passed, 1 skipped | none |
| freshstart `PyegeriaWebHandler/tests` | 150 passed | 150 passed | none |
| `tests/test_shared_portal_files.py` (new) | — | 11 passed | — |

The 4 quickstart failures are the same on both (pre-existing, unrelated):
`test_golden_anchors.py::test_work_item_list_detail_matches_known_seed_data`,
`test_golden_anchors.py::test_work_item_list_membership_matches_known_seed_data`,
`test_openlineage_topic_owner.py::test_data_hub_batch_no_longer_runs_the_notebook`,
`test_openlineage_topic_owner.py::test_no_batch_runs_the_notebook`.

The drift test was checked to fail when a freshstart copy is edited, when a
per-env file (`demo_config.py`) is listed, and when a floor file is dropped from
the list.

Also checked: freshstart's `pyegeria_handler` imports with the shared files, and its
OpenAPI lists `/api/types/classification-purposes` and `/api/digital-products/mesh`
(`/mesh` is registered before `/{node_guid}`); `node --check` passes on the shared JS.

**Not verified:** freshstart pages in a browser with the new `egeria-shared-ui.js`
(freshstart needs a real Egeria login; it cannot be smoked headlessly). Suggested
smoke after deploy: Egeria Explorer type pages, a detail pane's Diagrams chip bar and
Classifications section, Perspectives detail, Digital Products tree.
