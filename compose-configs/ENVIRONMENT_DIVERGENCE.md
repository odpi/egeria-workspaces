# Quickstart ↔ Freshstart — environment divergence guard

**Why this file exists:** several breakages have come from changes described as
"to all admin screens" / "both envs" that copied one environment's file over the
other's, silently flattening files that are *intentionally* different. This page
lists what is meant to diverge, the runtime model that lets some files be shared,
and a checklist to run before touching auth/admin/portal code.

---

## The three runtime modes

A single codebase serves three modes, selected at runtime by two flags in
`demo_config.py` (per-env defaults):

| Mode | `DEMO_MODE` | `SERVER_MANAGED_AUTH` | Auth | Used by |
|------|:----------:|:---------------------:|------|---------|
| **demo-quickstart** | `True`  | `False` | SQLite demo accounts (register/verify/email) | public demo |
| **local-quickstart** | `False` | `False` | none — Explorer ConnectionForm supplies creds | local dev |
| **freshstart** | `False` | `True`  | Egeria-backed, portal JWT cookie (`demo_token`) | server-managed |

**Rule for shared code:** any branch that gates auth/portal/admin behaviour must
consider **all three** modes — not just `DEMO_MODE`. The recurring bug is `if
DEMO_MODE:` … `else:` which lumps freshstart (server-managed, needs a login gate)
together with local-quickstart (no gate). Use `DEMO_MODE or SERVER_MANAGED_AUTH`
(see `_LOGIN_REQUIRED` in `pyegeria_handler.py`) for "login required", and a
distinct `elif SERVER_MANAGED_AUTH:` branch where the behaviour differs.

---

## Files that MUST stay per-env (do NOT converge or copy across envs)

Under `compose-configs/egeria-{quickstart,freshstart}/PyegeriaWebHandler/`:

| File | quickstart | freshstart |
|------|-----------|-----------|
| `demo_auth_handler.py` | SQLite demo auth (`/api/demo/users`, register/verify) | **Egeria-backed** server-managed auth (`/api/admin/egeria-users`, portal JWT) |
| `demo-admin.html` | demo SQLite user admin | **Egeria** user admin (Create User + first-login forced password, via `/api/admin/egeria-users`) |
| `demo-login.html` | demo account login | Egeria credential login (`POST /api/auth/login` → `demo_token` cookie) |
| `demo-portal.html` | demo portal/persona | freshstart portal (logged-in identity) |
| `demo-register.html` | demo self-registration | freshstart variant |
| `demo_config.py` | `DEMO_MODE`/`SERVER_MANAGED_AUTH` defaults | per-env defaults (SMA defaults **true**) |
| `demo_db.py` | SQLite engine | per-env (no SQLite store) |

Per-env presence (exists in only one env — never copy blindly):
- **quickstart-only:** `demo-reset-password.html`, `demo_reset_handler.py` (demo reset scheduler), `local-admin.html`
- **freshstart-only:** `demo-profile.html` (My Profile), `dr_egeria_md_bdl.py`, `dr_egeria_md_prev.py`, `user-directory.omsecrets`

Everything **else** in `PyegeriaWebHandler/` (the Explorer/Catalog handlers,
`type-explorer.html`, `tech-catalog.html`, `pyegeria_handler.py`,
`egeria_auth.py`, the mermaid/glossary handlers, …) is **converged / kept
byte-identical** and relies on the runtime flags above. Apply changes to those in
**both** envs.

**Shared by a guarded mirror (SHARE-3, 2026-11-21):** the files listed in
`compose-configs/shared-portal-files.txt` have ONE canonical copy, quickstart's.
Freshstart's copy is written by `compose-configs/sync_shared_portal_files.py`,
and `tests/test_shared_portal_files.py` fails CI on any difference. Edit
quickstart's copy, then run the script. Never edit freshstart's copy, and never
list a file from the per-env table above (the script refuses them). See
`DESIGN-SHARE-3-PHASE1.md` at the repository root.

**Now also converged (2026-08-12): `egeria-overview.html` + `overview_handler.py`
+ `overview_specs.py` + `overview_containers.py`.** Ported from quickstart-only
to freshstart (BACKLOG.md NEXT-11) using the same pattern `tech-catalog.html`
already established: `egeria-overview.html`'s `boot()` branches on
`me.server_managed_auth` internally (mirroring `tech-catalog.html`'s own boot
effect), rather than the two envs' copies diverging structurally. Apply future
changes to both.

**`demo-portal.html`'s Portal-level omni-search (2026-08-12, NEXT-12) is a
deliberate exception worth calling out explicitly**, since it's new code
inside a file this doc's own per-env list says never to copy across envs: the
search bar (CSS + HTML + the `PORTAL_EXPLORER_NAV`/`portalResolveNav`/
`portalOpenResult`/search-panel JS block, all under a "Portal-level omni-search"
comment header) was added by hand to **each** env's own copy separately — not
by copying one file over the other, following this doc's own checklist. The
routing-table portion additionally duplicates (not shares) `egeria-shared-ui.js`'s
`EGERIA_EXPLORER_NAV`/`resolveElementNav` — that file can't be loaded into this
plain-vanilla-JS landing page (it has a top-level `React.createContext()` call
that throws without React also loaded). If you add a type to one, add it to
both `egeria-shared-ui.js` copies **and** both `demo-portal.html` copies —
four places, not two.

**Solution Boundaries view (Portal Part C, 2026-11): the same feature in both environments, no intended difference.**
`solution_architect_handler.py` (three read-only async routes, the async factories, the `boundaries` field on blueprint and component detail) and
`type-explorer.html` (the Boundaries tab, the "Member of boundary" links, the in-app navigation) were changed with the same patch in each env's own copy;
neither file is in `shared-portal-files.txt`. The only differences are in the tests: freshstart's `test_solution_boundary_js.py` inlines the stub React
(freshstart has no `test_e64_cards_js.py`), and freshstart has no `test_graph_keys.py` route-count pin or `capture_boundary_fixtures.py`. Apply future
changes to both copies of both files.

---

## Known regressions this guard would have prevented (2026-06-18/19)

All three came from the convergence flattening freshstart's divergent files or
from `DEMO_MODE`-only gating:

1. **Boot failure** — `pyegeria_handler.py` converged to import `rate_limiter` /
   `obsidian_lock_handler`, but those modules were never copied to freshstart.
2. **Login loop** — `/login`, `/portal`, and the auth-router include branched on
   `DEMO_MODE` only; freshstart fell into the local-quickstart (no-auth) path →
   `/login` ↔ `/portal` loop and no `/api/auth/login`. Fixed with `_LOGIN_REQUIRED`
   + an `elif SERVER_MANAGED_AUTH:` auth-router include.
3. **Admin wiped** — `80165f1c "add user feedback table to all admin screens"`
   overwrote freshstart's Egeria user-admin with quickstart's demo SQLite admin,
   losing the Create-User + first-login-password flow. Restored from
   `80165f1c~1`.

---

## Checklist before changing auth / admin / portal / login code

- [ ] Is the file in the **per-env** list above? If so, edit each env's copy
      separately — do **not** copy one over the other.
- [ ] If it's a **converged** file, does every auth/portal/admin branch handle
      all three modes (demo / local / server-managed), not just `DEMO_MODE`?
- [ ] Commit message says "all admin screens" / "both envs"? Double-check you
      didn't flatten a per-env file — `git diff` the per-env files specifically.
- [ ] Touching `pyegeria_handler.py` imports? Confirm any newly-imported local
      module exists in **both** env dirs.
- [ ] After the change, smoke each affected mode (freshstart needs a real login;
      can't be verified headlessly).
