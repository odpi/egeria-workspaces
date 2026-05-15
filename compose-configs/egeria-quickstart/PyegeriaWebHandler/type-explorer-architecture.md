<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Type System Explorer — Architecture

This document covers how the Type System Explorer works internally, what it depends on, when data is fetched, and what needs periodic maintenance.

For feature documentation and the REST API reference, see [README.md](README.md#type-system-explorer).

---

## System architecture

```
Browser
  │  GET /type-explorer          (page load — serves the SPA HTML)
  │  GET /api/types[?area=N]     (data fetch — called once by the SPA on load)
  ▼
Apache httpd  (port 8085)
  │  ProxyPass /type-explorer  → http://pyegeria-web:8000/type-explorer
  │  ProxyPass /api/types      → http://pyegeria-web:8000/api/types
  ▼
FastAPI  (pyegeria-web container, port 8000)
  │  GET /type-explorer  → FileResponse("type-explorer.html")
  │  GET /api/types      → type_system_handler.get_all_types()
  ▼
pyegeria  ValidMetadataManager
  │  get_all_entity_defs()         → GET /servers/{server}/api/open-metadata/valid-metadata/open-metadata-types/entity-defs
  │  get_all_relationship_defs()   → GET /servers/{server}/api/open-metadata/valid-metadata/open-metadata-types/relationship-defs
  │  get_all_classification_defs() → GET /servers/{server}/api/open-metadata/valid-metadata/open-metadata-types/classification-defs
  ▼
Egeria platform  (egeria-main container, port 9443)
```

Apache and the FastAPI server run in separate containers on the same Docker network. TLS termination happens at Apache; internal container-to-container traffic is plain HTTP.

---

## Request lifecycle

### Page load (`GET /type-explorer`)

1. Browser requests `/type-explorer` from Apache.
2. Apache proxies to FastAPI, which serves `type-explorer.html` as a static file.
3. The HTML is fully self-contained: React 18, ReactDOM, and the compiled application JavaScript are all inlined. No external CDN calls are made.
4. Once the page renders, the SPA immediately fires a single `fetch('/api/types')` call.

### Data fetch (`GET /api/types`)

1. FastAPI calls `_get_client()` to construct a `ValidMetadataManager` instance using the connection parameters (from query params, falling back to env vars).
2. Three sequential synchronous calls are made to pyegeria:
   - `get_all_entity_defs()` — ~300–600 type defs depending on Egeria version
   - `get_all_relationship_defs()` — ~400–800 type defs
   - `get_all_classification_defs()` — ~50–100 type defs
3. Each pyegeria call opens a new HTTP connection to the Egeria platform, issues a `GET` to the REST endpoint, and returns the parsed JSON list.
4. The handler normalises the raw lists, derives area numbers by walking supertype chains, and returns a single JSON object.
5. The session is closed after all three calls complete.

**There is no server-side caching.** Every `/api/types` request re-queries Egeria. The SPA calls the endpoint once per page load (not once per type click). Subsequent navigation within the page — clicking types, switching tabs, changing the area filter — uses only the in-memory data already fetched.

**Typical response time** is 1–4 seconds depending on Egeria startup state and network latency inside Docker. If Egeria is still initialising, the call will fail with a 502 and the SPA displays a retry button.

---

## Data freshness

| Trigger | Data refreshed? |
|---------|----------------|
| Browser page load / hard refresh | Yes — full `/api/types` call |
| In-page navigation (click a type, change area filter) | No — uses cached in-memory data from initial load |
| SPA "Retry" button after a failed load | Yes — re-fetches `/api/types` |
| Container restart (no browser action) | No — browser still holds the previous fetch result |
| Egeria type system changes (e.g. new custom type deployed) | Only visible after the user reloads the page |

The type system of a running Egeria instance changes rarely in practice (only when new archive files are loaded or custom type definitions are deployed). A page reload is sufficient to pick up any changes.

---

## Dependencies

### Python (server-side)

| Package | Used for | Version constraint |
|---------|----------|--------------------|
| `fastapi` | HTTP routing, `APIRouter`, `FileResponse` | Any recent |
| `uvicorn` | ASGI server running FastAPI inside the container | Any recent |
| `pyegeria` | `ValidMetadataManager` — wraps Egeria REST calls | `< 6.0` (see note) |
| `httpx` / `aiohttp` | HTTP client used internally by pyegeria | Pulled in by pyegeria |

**pyegeria version note:** pyegeria 6.x introduced a circular import in `pyegeria.core._exceptions` that prevents the module from loading. Pin `pyegeria<6.0` in `requirements.txt` and remove any `RUN pip install pyegeria --upgrade` line from `Dockerfile-fast-api` until this is resolved upstream.

### Frontend (browser-side)

The SPA has no runtime dependencies fetched from the network. Everything is inlined in `type-explorer.html`:

| Library | Version inlined | Purpose |
|---------|----------------|---------|
| React | 18.x (production build) | Component rendering |
| ReactDOM | 18.x (production build) | DOM mounting |
| Application JS | compiled from JSX at build time | All UI logic |

The original JSX source lives in the `<script type="text/babel">` block of the pre-compilation artifact. If UI changes are needed, edit the JSX source and recompile — do not edit the inlined JS directly. See the Handoff.md for the build command.

### Infrastructure

| Component | Role |
|-----------|------|
| Apache httpd (`egeria-quickstart` container) | Reverse proxy; routes `/type-explorer` and `/api/types` to FastAPI |
| Docker network (`egeria-quickstart_default`) | Internal name resolution; `pyegeria-web` and `egeria-main` hostnames |
| Egeria platform (`egeria-main` container, port 9443) | Source of truth for all type definitions |

---

## Area derivation

The Egeria REST API does not include an area number in its TypeDef responses. Area is a documentation-level concept that groups related types. The handler derives it at response-build time by walking each type's supertype chain upward until hitting a known anchor in `AREA_ANCHORS`.

```
GovernanceProcedure
  → TechnicalControl
    → GovernanceControl
      → GovernanceDefinition   ← AREA_ANCHORS["GovernanceDefinition"] = 4
```

Types that bypass the normal area roots (several lineage types inherit directly from `Referenceable` rather than through `Process`) are listed explicitly in `AREA_ANCHORS`. `Referenceable` itself is pinned to area 0.

Area derivation runs once per request, not at startup. It adds negligible overhead since the type counts are small.

---

## Maintenance

### When to update `AREA_ANCHORS`

Update `AREA_ANCHORS` in `type_system_handler.py` when:
- A type appears in the wrong area in the explorer (check its supertype chain).
- You deploy custom types that do not inherit from an existing area anchor.
- Egeria introduces new root types in a future version.

The container picks up changes immediately because uvicorn runs with `--reload`.

### pyegeria compatibility patch

`type_system_handler.py` monkey-patches `ValidMetadataManager.get_all_classification_defs()` at import time. The upstream method uses a hardcoded `"typeDefList"` response key; the patch replaces it with the same `_extract_typedef_list()` helper used by the entity and relationship methods, making it resilient to API response format variations.

Check the pyegeria changelog after any pyegeria upgrade. If the upstream method is fixed, the patch block (marked with a `# pyegeria bug:` comment near the top of the file) can be removed.

### Debug logging

On every `/api/types` call, the handler logs at INFO level:
```
Entity def sample keys: ['class', 'guid', 'name', 'status', ..., 'descriptionWiki', ...]
Entity def sample wiki: https://egeria-project.org/types/0/0020-Property-Facets/
```

If `descriptionWiki` shows as `<missing>`, the Egeria endpoint for that version does not return wiki URLs and the wiki link feature will be inactive. If the keys list is empty or the call fails, check the pyegeria version and Egeria platform health.

### Freshstart config

The Type System Explorer is currently deployed only in the `egeria-quickstart` compose config. The same `type_system_handler.py`, `type-explorer.html`, `pyegeria_handler.py` patch, and `fastapi-proxy.conf` addition need to be applied to `egeria-freshstart` to make it available there as well.

---

## Security considerations

- The `/api/types` endpoint accepts Egeria credentials as query parameters. In production these should come from env vars (the defaults) rather than being passed in URLs, which may appear in server logs.
- The explorer is read-only; it calls only `GET` endpoints on the Egeria platform and makes no mutations.
- The inlined React bundle is the production (minified) build. It contains no `eval` or dynamic code execution.
