<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Explorer — Architecture

This document covers how the Egeria Explorer works internally: its request flow, data-fetching strategy, known Egeria API behaviours, frontend dependencies, and maintenance notes.

For feature documentation and the REST API reference, see [README.md](README.md#egeria-explorer).

---

## System architecture

```
Browser
  │  GET /egeria-explorer              (page load — serves the SPA HTML)
  │  GET /api/types                    (type system data)
  │  GET /api/reference-data           (reference data sets + values)
  │  GET /api/glossary                 (glossary list)
  │  GET /api/glossary/{guid}/terms    (terms in a glossary or folder)
  │  GET /api/glossary-terms           (cross-glossary term search)
  │  GET /api/digital-products/catalogs          (catalog list)
  │  GET /api/digital-products/catalogs/{guid}/tree  (full catalog tree)
  │  GET /api/digital-products/{guid}            (node detail)
  │  GET /api/mermaid/{guid}           (context diagram — graph_query_depth=5)
  │  GET /api/mermaid/{guid}/anchored  (full anchored element graph)
  │  GET /api/valid-values/properties  (property names that have registered valid values)
  │  GET /api/valid-values/lookup      (valid values for a property name)
  │  GET /api/request-bodies           (Layer 1 request body catalog — no Egeria needed)
  │  GET /api/rest-apis                (OpenAPI endpoint catalog)
  │  POST /api/request-bodies/rebuild  (regenerate catalog from http-client-collections)
  │  POST /api/rest-apis/refresh       (clear OpenAPI cache)
  │  GET /api/solution/blueprints      (solution blueprints list)
  │  GET /api/solution/blueprints/{guid} (blueprint detail)
  │  GET /api/solution/components      (solution components list)
  │  GET /api/data-design/specs        (data specs list)
  │  GET /api/data-design/structures   (data structures)
  │  GET /api/data-design/fields       (data fields)
  │  GET /api/data-design/grains       (data grains)
  │  GET /api/data-design/classes      (data classes)
  │  GET /api/perspectives             (perspectives list)
  │  GET /api/questions                (questions list — GlossaryTerms with Question classification)
  │  GET /api/isc                      (information supply chains)
  │  GET /api/dr-egeria/commands       (Dr. Egeria command templates)
  │  POST /api/dr-egeria/execute       (execute a Dr. Egeria command)
  │  GET /login, /register, /admin, /privacy  (demo mode pages — only active when DEMO_MODE=true)
  │  GET /api/auth/me, POST /api/auth/login, etc.  (demo auth — only active when DEMO_MODE=true)
  ▼
Apache httpd  (port 8085)
  │  ProxyPass /egeria-explorer → http://pyegeria-web:8000/egeria-explorer
  │  ProxyPass /api/*           → http://pyegeria-web:8000/api/*
  ▼
FastAPI  (pyegeria-web container, port 8000)
  │  type_system_handler.py       → ValidMetadataManager
  │  reference_data_handler.py    → ReferenceDataManager
  │  glossary_handler.py          → GlossaryManager
  │  digital_products_handler.py  → CollectionManager
  │  mermaid_handler.py           → MetadataExpert
  │  valid_values_handler.py      → ReferenceDataManager
  │  rest_api_handler.py          → egeria_request_body_catalog.json (static)
  │                                 + Egeria /v3/api-docs (live, cached 1h)
  │  solution_architect_handler.py → SolutionArchitectManager
  │  data_design_handler.py        → DataDesignerManager + CollectionManager
  │  perspectives_handler.py       → ActorProfileManager + GlossaryManager
  │  dr_egeria_commands_handler.py → local markdown templates + dr_egeria_md processor
  │  isc_handler.py                → InformationSupplyChainManager
  │  demo_auth_handler.py          → SQLite (demo only, DEMO_MODE=true)
  ▼
pyegeria (various managers)
  ▼
Egeria platform  (egeria-main container, port 9443)
```

Apache and the FastAPI server run in separate containers on the same Docker network. TLS termination happens at Apache; internal container-to-container traffic is plain HTTP.

---

## Request lifecycle

### Page load (`GET /egeria-explorer` or `GET /type-explorer`)

1. Browser requests `/egeria-explorer` (or the alias `/type-explorer`) from Apache.
2. Apache proxies to FastAPI. `type_system_handler.py` has two `@router.get` decorators on the same handler function so both URLs serve the same `type-explorer.html` via `FileResponse`.
3. The HTML is a self-contained React 18 SPA. React and ReactDOM are loaded from CDN (`unpkg.com`). Mermaid diagram rendering is loaded from CDN (`cdn.jsdelivr.net/npm/mermaid@11`). Application JavaScript is inlined in the HTML.
4. On load the SPA fetches `/api/types` immediately and renders the **Home (Splash Screen)** as the initial visible section. All other section data is fetched lazily when the user first opens that tab.

### Tab data fetching

| Tab | Endpoint | Fetched when |
|-----|----------|-------------|
| Home (Splash Screen) | — | Shown immediately on page load; no data fetch |
| Type System | `GET /api/types` | Page load |
| Reference Data | `GET /api/reference-data?page_size=500` | First time tab is opened |
| Glossary | `GET /api/glossary` | First time tab is opened |
| Glossary terms | `GET /api/glossary/{guid}/terms` | Glossary or folder selected |
| Digital Products | `GET /api/digital-products/catalogs` | First time tab is opened |
| Digital Products tree | `GET /api/digital-products/catalogs/{guid}/tree` | Catalog selected |
| Context diagram | `GET /api/mermaid/{guid}` — `get_metadata_element_by_guid` at depth=5 | User clicks "▦ Load Context Diagram" |
| Full anchored graph | `GET /api/mermaid/{guid}/anchored` — `get_anchored_element_graph` | User clicks "▦ Load Full Graph" |
| Valid Values — property list | `GET /api/valid-values/properties` | First time tab is opened (pre-populates sidebar) |
| Valid Values — lookup | `GET /api/valid-values/lookup?property_name=…` | User selects or enters a property name |
| REST APIs — body catalog | `GET /api/request-bodies` | REST APIs tab is opened (no Egeria needed) |
| REST APIs — endpoints | `GET /api/rest-apis` | User clicks "Load API Endpoints" in the toolbar |
| Solution Architect | `GET /api/solution/blueprints`, `GET /api/solution/components` | First time tab is opened (lazy) |
| Data Design | `GET /api/data-design/specs`, `GET /api/data-design/structures`, etc. | First time sub-tab is opened |
| Perspectives | `GET /api/perspectives`, `GET /api/questions` | First time tab is opened |
| Dr. Egeria Commands | `GET /api/dr-egeria/commands` | First time tab is opened (static — no Egeria needed) |
| Supply Chains | `GET /api/isc` | First time tab is opened |

**Server-side caching:** Most handlers have no caching — data is re-fetched on tab re-open. The REST API handler is the exception: the OpenAPI spec fetched from Egeria (`/v3/api-docs`) is cached in process for one hour. The request body catalog is loaded from disk once and held for the process lifetime. All other data is held in React state for the current page session.

---

## Egeria graph_query_depth — behaviour and tradeoffs

Most API calls specify a `graph_query_depth` parameter that controls how far Egeria traverses relationship edges when building the response:

- **`graph_query_depth=0`** — returns the element's own properties only. No relationship data in the response. Fast; each matching element appears exactly once.
- **`graph_query_depth=1`** — returns the element's properties plus all directly related elements (one hop out). Slower; **can return duplicates** (see below).

### Why graph_query_depth=1 causes duplicates

With depth=1, Egeria traverses outward from every primary hit. If a neighbor element also matches the search, it appears in results twice:
1. As a primary search hit.
2. As a neighbor of each other primary hit that is linked to it.

**Example — glossary terms in a folder:** If a folder contains terms A, B, and C, and the search returns all three as primary hits, then A also appears as a neighbor of B and C (via `CollectionMembership`), B appears as a neighbor of A and C, and so on. A folder of 20 terms can yield up to 400 rows for 20 unique terms.

**Mitigation:** The glossary handler deduplicates by GUID immediately after the API response, before any filtering:

```python
seen: set = set()
unique: list = []
for t in raw:
    g = _header(t).get("guid", "")
    if g and g not in seen:
        seen.add(g)
        unique.append(t)
```

### When depth=1 is necessary

`memberOfCollections` (on glossary terms) and `memberOfValidValueSets` (on reference data values) are only populated when `graph_query_depth=1`. These fields are essential for:
- Filtering terms by their containing glossary/folder.
- Building the parent-child tree in the Reference Data view.

The deduplication cost is worth paying to get this relationship data.

### Endpoints using depth=0 (fast path)

`find_collections` (digital products catalog listing) and the top-level glossary list use `graph_query_depth=0` deliberately. These endpoints only need root-level element properties; they do not need relationship traversal. Switching to depth=0 cut per-page response time from ~30s to <0.5s on typical Egeria demo data.

---

## Mermaid diagram rendering

Context diagrams are rendered client-side using the Mermaid JS library loaded from CDN.

### Version requirement

Egeria generates mermaid diagram code using **mermaid v11+ syntax** — specifically the `@{ shape: … }` node shape notation introduced in v11.0. Loading mermaid v10 (or earlier) results in silent render failures: `mermaid.render()` resolves successfully but returns an empty SVG. Always load `mermaid@11` or later.

Current CDN reference in `type-explorer.html`:
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
```

### Rendering flow

Each element detail panel exposes two lazy-loading diagram buttons, each backed by a `DiagramPanel` component:

**▦ Load Context Diagram** (`GET /api/mermaid/{guid}`)
1. `DiagramPanel` sets `open = true`, triggering a fetch to `GET /api/mermaid/{guid}`.
2. `mermaid_handler.py` calls `MetadataExpert.get_metadata_element_by_guid(guid, graph_query_depth=5, output_format="JSON")`.
3. The top-level `mermaidGraph` field is extracted from the response (depth=5 scope).
4. The diagram code is stored in `code` state and rendered via `MermaidDiagram`.

**▦ Load Full Graph** (`GET /api/mermaid/{guid}/anchored`)
1. `DiagramPanel` sets `open = true`, triggering a fetch to `GET /api/mermaid/{guid}/anchored`.
2. `mermaid_handler.py` calls `MetadataExpert.get_anchored_element_graph(guid, mermaid_only=True)`.
3. The returned mermaid string (broader, slower traversal) is stored and rendered.

Both panels support **Hide** / **▦ Show** toggling. `code` state is preserved per panel so no re-fetch occurs on show. The `/anchored` route is registered before `/{guid}` in FastAPI so the literal path segment is not consumed as a GUID.

If the CDN is unreachable (mermaid not loaded), the component polls for up to 6 seconds then shows the raw mermaid code with a "library not loaded" warning. If `render()` rejects, the error message is shown above the raw code.

### Backend class name

The pyegeria class for element graph queries is `MetadataExpert` (not `MetadataExplorer`). The method is `get_anchored_element_graph(guid, mermaid_only=True, graph_query_depth=5)`.

---

## Reference Data tree construction

The Reference Data view displays a hierarchy: root-level ValidValueSets as tree roots, with their member values and child sets nested underneath. This tree is built client-side from a flat list returned by the backend.

**Backend:** `GET /api/reference-data` fetches all valid value definitions using `graph_query_depth=1`. The serialiser reads `element["memberOfValidValueSets"]` to extract each element's parent set GUIDs and names, adding them as a `parentSets` field.

**Frontend:** The `RefDataTreeNode` component filters `byGuid` (a `guid → item` map) to find children of a given set. Root nodes are sets with an empty `parentSets` list. The tree expands/collapses on click. Sets can be nested arbitrarily deep.

---

## Data freshness

| Trigger | Data refreshed? |
|---------|----------------|
| Browser page load / hard refresh | Yes — all tab data is re-fetched when tabs are opened |
| In-section navigation (click an item) | No — uses in-memory React state |
| SPA retry button after failed load | Yes — re-fetches that section's data |
| Container restart (no browser action) | No — browser still holds previous data |
| Egeria data changes | Only visible after page reload and tab re-open |

---

## Dependencies

### Python (server-side)

| Package | Used for |
|---------|----------|
| `fastapi` | HTTP routing, `APIRouter`, `FileResponse` |
| `uvicorn` | ASGI server with `--reload` for hot code pickup |
| `pyegeria` | All manager classes; always latest release |
| `loguru` | Structured logging in all handlers |

**pyegeria managers used:**

| Manager | Handler | Key methods |
|---------|---------|-------------|
| `ValidMetadataManager` | `type_system_handler.py` | `get_all_entity_defs`, `get_all_relationship_defs`, `get_all_classification_defs` |
| `ReferenceDataManager` | `reference_data_handler.py`, `valid_values_handler.py` | `find_valid_value_definitions`, `get_valid_metadata_values` |
| `MetadataExpert` | `valid_values_handler.py` | `find_metadata_elements` (properties list — raw OpenMetadata format) |
| `GlossaryManager` | `glossary_handler.py` | `find_glossaries`, `find_glossary_terms`, `get_term_by_guid`, `get_collection_members` |
| `CollectionManager` | `digital_products_handler.py` | `find_collections`, `get_collection_members`, `get_collection_by_guid` |
| `MetadataExpert` | `mermaid_handler.py` | `get_metadata_element_by_guid` (depth=5), `get_anchored_element_graph` |
| `SolutionArchitectManager` | `solution_architect_handler.py` | `find_solution_blueprints`, `get_solution_blueprint_by_guid`, `find_solution_components`, `get_solution_component_by_guid` |
| `DataDesignerManager` | `data_design_handler.py` | `find_data_structures`, `find_data_fields`, `find_data_grains`, `find_data_classes`; falls back to search-string endpoint for data value specs (pyegeria ≤6.0.12.3 missing `find_data_value_specifications`) |
| `ActorProfileManager` | `perspectives_handler.py` | `find_actors`, `get_actor_profile_by_guid` |
| `InformationSupplyChainManager` | `isc_handler.py` | `find_information_supply_chains`, `get_information_supply_chain_by_guid` |
| `CollectionManager` | `data_design_handler.py` | Used alongside DataDesignerManager to fetch collection memberships |

### Frontend (browser-side)

| Library | Source | Purpose |
|---------|--------|---------|
| React 18 | CDN (`unpkg.com`) | Component rendering |
| ReactDOM 18 | CDN (`unpkg.com`) | DOM mounting |
| Mermaid 11+ | CDN (`cdn.jsdelivr.net`) | Context diagram rendering |
| Application JS | Inlined in `type-explorer.html` | All UI logic |

The application JavaScript is written inline in the HTML using `React.createElement()` calls (no JSX transpilation required). All React hooks are destructured from `React` at the top of the script block.

### Infrastructure

| Component | Role |
|-----------|------|
| Apache httpd (`egeria-quickstart` container) | Reverse proxy; routes `/egeria-explorer` and `/api/*` to FastAPI |
| Docker network | Internal name resolution; `pyegeria-web` and `egeria-main` hostnames |
| Egeria platform (`egeria-main`, port 9443) | Source of truth for all instance and type data |

---

## Handler file map

| File | Router prefix | Purpose |
|------|--------------|---------|
| `type_system_handler.py` | `/api/types`, `/egeria-explorer`, `/type-explorer` | Type definitions; serves the SPA HTML via two URL aliases |
| `reference_data_handler.py` | `/api/reference-data` | Valid value set/value tree |
| `glossary_handler.py` | `/api/glossary`, `/api/glossary-terms` | Glossaries, folders, terms |
| `digital_products_handler.py` | `/api/digital-products` | Catalog→family→product hierarchy |
| `mermaid_handler.py` | `/api/mermaid` | Element context diagrams |
| `valid_values_handler.py` | `/api/valid-values` | Property-name valid value lookups |
| `report_specs_handler.py` | `/api/report-specs` | pyegeria report format specs |
| `rest_api_handler.py` | `/api/request-bodies`, `/api/rest-apis` | Layer 1 body catalog (static) + OpenAPI endpoint catalog (live, cached) |
| `solution_architect_handler.py` | `/api/solution` | Solution blueprints and components via SolutionArchitectManager |
| `data_design_handler.py` | `/api/data-design` | Data specs, structures, fields, grains, classes via DataDesignerManager |
| `perspectives_handler.py` | `/api/perspectives`, `/api/questions` | Egeria Perspectives (actor profiles) and Questions (GlossaryTerms with Question classification) |
| `dr_egeria_commands_handler.py` | `/api/dr-egeria` | Command template catalog (static) and command execution (live) |
| `isc_handler.py` | `/api/isc` | Information supply chains via InformationSupplyChainManager |
| `demo_auth_handler.py` | `/api/auth`, `/api/demo` | Demo mode auth, persona selection, admin endpoints; active only when `DEMO_MODE=true` |
| `demo_config.py` | — | DEMO_MODE flag and all JWT/SMTP/DB settings read from env vars |
| `demo_db.py` | — | SQLite models (User, Event, Config) via SQLAlchemy; `demo.db` at DEMO_DB_PATH |
| `personas.json` | — | 10 Coco Pharmaceuticals persona definitions with credentials and UI metadata |
| `demo-login.html`, `demo-register.html`, `demo-admin.html`, `demo-privacy.html` | — | Self-contained demo mode HTML pages served by pyegeria_handler.py |
| `pyegeria_handler.py` | — | FastAPI app; mounts all routers |
| `type-explorer.html` | — | Self-contained SPA served by type_system_handler |
| `egeria_request_body_catalog.json` | — | Generated catalog of Layer 1 request body types; loaded once at startup |
| `build_request_body_catalog.py` | — | Standalone rebuild script; run after each Egeria upgrade |

---

## Data sources at a glance

This table answers the question "where does the data actually come from?" for each Explorer section, and whether the section works when Egeria is not reachable.

| Section | Data source | Egeria required? | Caching |
|---------|-------------|-----------------|---------|
| Home (Splash Screen) | Static — rendered from hardcoded capability list | **No** | N/A |
| Type System | `ValidMetadataManager` → Egeria REST API | Yes | None (re-fetched per page load) |
| Glossary | `GlossaryManager` → Egeria REST API | Yes | None |
| Reference Data | `ReferenceDataManager` → Egeria REST API | Yes | None |
| Digital Products | `CollectionManager` → Egeria REST API | Yes | None |
| Valid Values | `ReferenceDataManager` → Egeria REST API | Yes | None |
| Context Diagram | `MetadataExpert.get_metadata_element_by_guid` at depth=5 | Yes | None |
| Full Anchored Graph | `MetadataExpert.get_anchored_element_graph` | Yes | None |
| Report Specs | pyegeria module introspection (format specs) | **No** | None |
| REST APIs — body catalog | `egeria_request_body_catalog.json` (static file in container) | **No** | Process lifetime |
| REST APIs — endpoints | Egeria `/v3/api-docs` OpenAPI spec | Yes | 1 hour in-process |
| Solution Architect | `SolutionArchitectManager` → Egeria REST API | Yes | None |
| Data Design | `DataDesignerManager` + `CollectionManager` → Egeria REST API | Yes | None |
| Perspectives | `ActorProfileManager` + `GlossaryManager` → Egeria REST API | Yes | None |
| Dr. Egeria Commands | Markdown template files in container (`md_processing/data/compact_commands`) | **No** | Process lifetime |
| Supply Chains | `InformationSupplyChainManager` → Egeria REST API | Yes | None |

**Report Specs**, the **REST API body catalog**, and **Dr. Egeria Commands** work without an Egeria connection. All other sections require the Egeria platform to be running and reachable from the `pyegeria-web` container at the URL configured by `EGERIA_PLATFORM_URL`.

---

## Demo mode architecture

Demo mode is an optional layer that adds user registration, authentication, and persona-based access control to Egeria Explorer. It is activated by setting `DEMO_MODE=true` in the container environment.

### Component overview

```
Browser
  │  GET /login, /register          → demo-login.html, demo-register.html (served by FastAPI)
  │  POST /api/auth/register        → email + bcrypt hash stored in SQLite
  │  GET /api/auth/verify/{token}   → marks user verified; sets demo_token cookie; redirects to /egeria-explorer
  │  POST /api/auth/login           → verifies bcrypt hash; sets demo_token cookie (2h expiry)
  │  GET /egeria-explorer           → auth gate checks demo_token; 302 → /login if absent/invalid
  │  POST /api/demo/select-persona  → returns Coco Pharmaceuticals Egeria credentials
  │  GET /admin                     → admin panel (admin role required)
  ▼
FastAPI (pyegeria-web:8000)
  │  demo_auth_handler.py           → JWT decode/encode, bcrypt, email via SMTP
  │  demo_db.py (SQLite)            → User, Event, Config tables at DEMO_DB_PATH
  ▼
pyegeria_handler.py
  │  DEMO_MODE=true → includes demo_auth_handler router
  │  /login, /register, /admin, /privacy routes always present; redirect to /egeria-explorer if DEMO_MODE=false
```

### Authentication flow

1. User registers with name, email, password → POST `/api/auth/register` → bcrypt-hashed password stored in SQLite; verify token emailed.
2. Email link hits `GET /api/auth/verify/{token}` → `verified=True` set in DB; `demo_token` JWT cookie set; browser redirected to `/egeria-explorer`.
3. Subsequent requests to `/egeria-explorer` pass through the auth gate in `type_system_handler.py`, which decodes the JWT from the cookie using `python-jose` / HS256. Invalid or expired tokens redirect to `/login`.
4. After reaching the Explorer, the persona picker (`PersonaPickerModal`) fires on first load. It calls `GET /api/demo/personas` (public, no auth) then `POST /api/demo/select-persona` (auth required). The server returns the persona's Egeria username and well-known password (`"secret"`). The browser stores these in `localStorage` as `egeria-creds` and in `egeria-persona` for the badge display.

### JWT session

- **Algorithm**: HS256, secret from `JWT_SECRET` env var.
- **User expiry**: `JWT_EXPIRY_USER_SEC` (default 7200 = 2 hours).
- **Admin expiry**: `JWT_EXPIRY_ADMIN_SEC` (default 604800 = 7 days).
- The cookie name is `demo_token`, HTTPOnly, SameSite=lax.
- If SMTP is not configured, email verification is skipped (the user is still created but remains `verified=False` until an admin enables them, or the env allows auto-verify for development).

### SQLite schema

Three tables in the database at `DEMO_DB_PATH` (default `/app/demo-data/demo.db`):

**`users`** — `id` (UUID PK), `display_name`, `org`, `email` (unique), `password_hash`, `role` (user|admin), `verified`, `verify_token`, `reset_token`, `reset_expires`, `created_at`, `last_login`.

**`events`** — `id` (UUID PK), `user_id` (FK → users), `event_type` (register|verify|login|persona_select), `detail` (JSON text), `created_at`.

**`config`** — `key` (PK), `value` (text). Seeded with defaults: `reset_interval_hours`, `directive_cap`, `session_lifetime_user`, `session_lifetime_admin`, `reset_notify_minutes`, `last_reset_at`, `reset_state`.

### Persona selection flow

The `POST /api/demo/select-persona` endpoint:
1. Verifies the user is authenticated and verified (JWT cookie required).
2. Looks up the persona in `personas.json` by the `persona` field in the request body.
3. Returns `{ persona, display_name, coco_title, egeria_user, egeria_password }`.
4. The browser's `applyPersona()` function in `App` takes these credentials, calls `saveCreds()` to update `CredContext` (the React context that all data-fetching handlers read), and stores `egeria-persona` in localStorage for the badge display and "Switch Persona" functionality.

The returned password is always `"secret"` — the well-known Coco Pharmaceuticals demo default. This is not a security concern as the Egeria instance is pre-populated with non-sensitive fictional data.

### When DEMO_MODE is false

All auth routes are still registered in FastAPI (the page routes `/login`, `/register`, `/admin`, `/privacy` always exist) but:
- `GET /login` redirects to `/egeria-explorer` immediately.
- `GET /egeria-explorer` serves the HTML without any cookie check.
- `demo_auth_handler` router is NOT mounted (no `/api/auth/*` or `/api/demo/*` routes).
- The `PersonaPickerModal` in the SPA does not appear (it only activates when `/api/auth/me` returns `authenticated: true`).

### Security considerations for public deployment

- Change `JWT_SECRET` from the default before public exposure.
- Set `SMTP_HOST` to enable email verification; without it, newly registered users cannot verify themselves.
- Mount `demo-data/` on a persistent volume (see `runtime-volumes/quickstart-demo-data`).
- The `directive_cap` config key limits what demo users can execute via the Dr. Egeria Commands tab (planned: `validate` level prevents writes; `process` allows writes).
- Do not expose port 8000 (FastAPI) directly; all public traffic should pass through Apache on host port 8885.

---

## Known pyegeria quirks

### Classification defs response key

Fixed upstream in pyegeria (the method now uses `_extract_typedef_list()` and accepts `get_inherited_attributes` / `get_relationship_attributes` parameters). The monkey-patch that previously existed in `type_system_handler.py` has been removed.

This incident is a worked example of the pyegeria upgrade process — see [Upgrading pyegeria](#upgrading-pyegeria) below.

### find_metadata_elements returns raw OpenMetadata format

`MetadataExpert.find_metadata_elements(body)` returns elements in raw OpenMetadata format — **not** the processed pyegeria format returned by manager methods like `find_valid_value_definitions`. There is no `elementHeader` / `properties` split; instead each element has:

```
el["elementGUID"]                                                      # top-level GUID
el["elementProperties"]["propertiesAsStrings"]["identifier"]          # fastest path — string value
el["elementProperties"]["propertyValueMap"]["identifier"]["primitiveValue"]  # full structure
```

The property name field is `"identifier"`, not `"propertyName"`. Code that looks for `"propertyName"` in `propertyValueMap` will silently find nothing.

The `propertiesAsStrings` shortcut is preferred for extraction — it contains the same string values without the type wrapper objects.

### MetadataExpert vs MetadataExplorer

The class for element graph queries is `MetadataExpert`. There is no `MetadataExplorer` class in pyegeria; using that name produces an `ImportError`.

### mermaidGraph field location

Egeria places the `mermaidGraph` string at the **top level of the element dict** (e.g., `element["mermaidGraph"]`), not inside `element["properties"]`. The field is **generated at execution time** and is scoped to the same depth and relationship constraints as the enclosing find/get call — it reflects exactly what that query returned, no more.

Per-element serialisers read it with a two-level fallback to guard against format variation:
```python
element.get("mermaidGraph", "") or props.get("mermaidGraph", "") or ""
```

The `mermaidGraph` field is present in responses from any find or get method when `output_format="JSON"` is passed. The `/api/mermaid/{guid}` endpoint uses `MetadataExpert.get_anchored_element_graph` with `graph_query_depth=5` to fetch a depth=5 diagram for the context diagram button, since list and tree queries use depth 0–1 and their embedded `mermaidGraph` values would be too shallow.

### DataDesignerManager — find_data_value_specifications missing in early 6.x

In pyegeria ≤6.0.12.3, `DataDesignerManager.find_data_value_specifications()` is absent (the async method `_async_post` it relied on was not yet available). `data_design_handler.py` works around this by calling the underlying Egeria REST endpoint directly via `mgr.make_request()` with the search-string URL. If a future pyegeria version restores the method, the direct call in `_search_data_value_specs()` should be replaced with the manager method.

---

## Maintenance

### Adding a new Explorer section

1. Create `<section>_handler.py` with a `router = APIRouter(tags=["<section>"])`.
2. Add endpoints; follow the `_get_manager()` / `_props()` / `_header()` pattern from existing handlers.
3. Register in `pyegeria_handler.py`: `from <section>_handler import router as <section>_router` then `app.include_router(<section>_router)`.
4. Add the frontend component(s) to `type-explorer.html` and a tab button in the `App` component's tab bar.
5. Update this document, `README.md`, and `Extending the TypeExplorer.md`.

### Upgrading pyegeria

`requirements.txt` pins pyegeria at `>=5.4.8.10` with no upper bound, so Docker image builds always install the latest published version. pyegeria is actively developed and its method signatures and response formats can change without a major-version bump.

**When a pyegeria update causes a startup error:**

1. Read the traceback in `docker logs quickstart-pyegeria-web`.
2. Identify whether the failure is:
   - A **signature mismatch** — the error will be `TypeError: <method>() got an unexpected keyword argument` or similar.  
     Likely cause: the new pyegeria added a parameter that a handler (or a now-deleted monkey-patch) does not accept.
   - A **changed response format** — the data is fetched successfully but serialisation fails with a `KeyError`, `AttributeError`, or unexpected type.  
     Likely cause: the new pyegeria changed a field name or response structure.
   - An **import error** — a class or function was renamed or removed.

3. **Monkey-patches**: If the error is in a patched method:
   - First check whether the upstream pyegeria has fixed the bug the patch was working around. If yes, remove the patch entirely (preferred — keeps the code clean).
   - If not, update the patch signature to match the new pyegeria signature, and add `**kwargs` for forward-compatibility.

4. **Response format changes**: Update the field extraction in the affected handler's `_props()` or `_header()` helper. Log the new response keys at `DEBUG` level to inspect the live structure:
   ```python
   logger.debug(f"Sample keys: {list(sample.keys())}")
   ```

5. After fixing, rebuild and restart the container:
   ```bash
   docker compose build pyegeria-web && docker compose up -d pyegeria-web
   ```

**Worked example — classification defs (fixed in pyegeria ~5.4.9):**

`type_system_handler.py` previously monkey-patched `ValidMetadataManager._async_get_all_classification_defs` to fix a bug where the method read `"typeDefList"` from the response instead of the correct key. A later pyegeria release fixed the method natively and also added `get_inherited_attributes` / `get_relationship_attributes` parameters. The patch started failing with:

```
TypeError: _patched_async_get_all_classification_defs() got an unexpected keyword argument 'get_inherited_attributes'
```

Resolution: confirmed the upstream fix was correct, removed the entire monkey-patch block.

### Upgrading Egeria — keeping the REST API catalog current

The Layer 1 request body catalog (`egeria_request_body_catalog.json`) is derived from the `http-client-collections` directory shipped with the Egeria platform distribution. After each Egeria upgrade:

```bash
python3 build_request_body_catalog.py /path/to/egeria-platform-X.Y/assembly/opt/http-client-collections
```

The script re-extracts all `*Body` class occurrences, rebuilds the field union and representative examples, and overwrites the JSON file. Commit the updated JSON alongside the new release notes.

If `HTTP_COLLECTIONS_PATH` is set in the container environment pointing at a mounted copy of `http-client-collections`, the rebuild can also be triggered at runtime without file-system access:

```
POST /api/request-bodies/rebuild
Content-Type: application/json

{}
```

The OpenAPI endpoint data (`/api/rest-apis`) always comes from the live Egeria platform and needs no manual update step — the 1-hour in-process cache is cleared automatically on container restart, or on demand via `POST /api/rest-apis/refresh`.

### REST API handler design notes

**Two-layer payload model.** Egeria REST payloads follow a consistent two-layer pattern: an outer wrapper body (`NewElementRequestBody`, `UpdateElementRequestBody`, etc.) that handles governance metadata, provenance, and linkage; and an inner type-specific properties body (`GlossaryTermProperties`, `CollectionProperties`, etc.) that carries the element's own fields.

There are ~44 distinct outer body types across the Egeria platform — a small, stable set. The inner properties bodies are unbounded (one per entity/relationship/classification type) but fully derivable from the type system.

**Catalog extraction.** `build_request_body_catalog.py` parses every `.http` file in `http-client-collections`, locates JSON objects whose `"class"` field ends in `Body`, and accumulates the union of all top-level field names seen across all occurrences. Each body type's catalog entry records: functional group, annotated field list, and one representative example object.

**OpenAPI mapping.** `rest_api_handler.py` fetches `/v3/api-docs` from the Egeria platform and walks every path/operation. For each operation it:
1. Resolves the `requestBody.content['application/json'].schema.$ref` to get the outer body class name and matches it against the catalog.
2. Attempts to resolve the body schema's `properties.properties.$ref` to an inner properties type name; falls back to summary-string parsing and URL-path heuristics if the schema is too generic (e.g., `ElementProperties`).
3. Extracts path and query parameters.

Results are grouped by OpenAPI tag (= OMAS/OMVS service name) and returned as a structured JSON list. The spec is cached in `_openapi_cache` keyed by platform URL with a 1-hour TTL.

### Upgrading mermaid

If the CDN version is bumped, verify that Egeria's generated diagram syntax is still valid for the new version. The `%%{init: {"flowchart": {"htmlLabels": false}} }%%` directive and `@{ shape: … }` node syntax have been stable since mermaid v11.0.

### Debug logging

All handlers log at `ERROR`/`WARNING` level via `loguru`. On a failed API call:
```
ERROR | mermaid_handler:43 - Failed to create MetadataExpert
```
Check `docker logs quickstart-pyegeria-web` for the full traceback. The most common causes are bearer token expiry (re-create by restarting the connection) and network issues between the pyegeria-web and egeria-main containers.

### graph_query_depth tuning

If a new section requires relationship data, use `graph_query_depth=1` and add GUID deduplication. If a section only needs element properties, use `graph_query_depth=0` for maximum speed. Never pass depth values greater than 1 for list/search endpoints — the combinatorial explosion of graph traversal makes responses extremely slow.
