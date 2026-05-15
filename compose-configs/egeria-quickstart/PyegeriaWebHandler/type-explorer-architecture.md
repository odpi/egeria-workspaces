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
  │  GET /api/mermaid/{guid}           (context diagram for any element)
  │  GET /api/valid-values/lookup      (valid values for a property name)
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
4. On load the SPA fetches `/api/types` immediately. All other section data is fetched lazily when the user first opens that tab.

### Tab data fetching

| Tab | Endpoint | Fetched when |
|-----|----------|-------------|
| Type System | `GET /api/types` | Page load |
| Reference Data | `GET /api/reference-data?page_size=500` | First time tab is opened |
| Glossary | `GET /api/glossary` | First time tab is opened |
| Glossary terms | `GET /api/glossary/{guid}/terms` | Glossary or folder selected |
| Digital Products | `GET /api/digital-products/catalogs` | First time tab is opened |
| Digital Products tree | `GET /api/digital-products/catalogs/{guid}/tree` | Catalog selected |
| Context diagram | `GET /api/mermaid/{guid}` | User clicks "Load Context Diagram" button |
| Valid Values | `GET /api/valid-values/lookup?property_name=…` | User selects or enters a property name |

**There is no server-side caching.** Data is re-fetched on tab re-open (after a page reload) but held in React state for the session while the page is open.

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

1. User clicks **▦ Load Context Diagram** on any element detail panel.
2. `MermaidSection` component sets `open = true`, triggering a `useEffect` that calls `GET /api/mermaid/{guid}`.
3. `mermaid_handler.py` constructs a `MetadataExpert` client and calls `get_anchored_element_graph(guid, mermaid_only=True)`.
4. The mermaid diagram code string is returned to the browser and stored in the component's `code` state.
5. `MermaidDiagram` component calls `window.mermaid.render(id, code)` which returns a Promise resolving to `{ svg }`.
6. The SVG string is injected into the DOM via `innerHTML`.

Once rendered, the user can toggle visibility with a **Hide** / **▦ Show Context Diagram** button. The `code` state is preserved so no re-fetch is needed on show. The `open` state gates the fetch; the `visible` state gates the render.

If the CDN is unreachable (mermaid not loaded), the component polls for up to 6 seconds then shows the raw mermaid code with a "library not loaded" warning. If `render()` rejects, the error message is shown above the raw code.

### Backend class name

The pyegeria class for element graph queries is `MetadataExpert` (not `MetadataExplorer`). The method is `get_anchored_element_graph(guid, mermaid_only=True)`.

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
| `GlossaryManager` | `glossary_handler.py` | `find_glossaries`, `find_glossary_terms`, `get_term_by_guid`, `get_collection_members` |
| `CollectionManager` | `digital_products_handler.py` | `find_collections`, `get_collection_members`, `get_collection_by_guid` |
| `MetadataExpert` | `mermaid_handler.py` | `get_anchored_element_graph` |

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
| `pyegeria_handler.py` | — | FastAPI app; mounts all routers |
| `type-explorer.html` | — | Self-contained SPA served by type_system_handler |

---

## Known pyegeria quirks

### Classification defs response key

`ValidMetadataManager.get_all_classification_defs()` uses a hardcoded `"typeDefList"` response key instead of the `_extract_typedef_list()` helper used by the entity and relationship equivalents. `type_system_handler.py` monkey-patches this at import time. The patch can be removed once the fix is merged upstream in pyegeria.

### MetadataExpert vs MetadataExplorer

The class for element graph queries is `MetadataExpert`. There is no `MetadataExplorer` class in pyegeria; using that name produces an `ImportError`.

### mermaidGraph field location

Egeria places the `mermaidGraph` string at the **response container level** (e.g., `element["mermaidGraph"]`), not inside `element["properties"]`. Per-element serialisers that look in `properties` will always find an empty string. The dedicated `/api/mermaid/{guid}` endpoint using `MetadataExpert.get_anchored_element_graph` is the correct way to retrieve per-element diagrams.

---

## Maintenance

### Adding a new Explorer section

1. Create `<section>_handler.py` with a `router = APIRouter(tags=["<section>"])`.
2. Add endpoints; follow the `_get_manager()` / `_props()` / `_header()` pattern from existing handlers.
3. Register in `pyegeria_handler.py`: `from <section>_handler import router as <section>_router` then `app.include_router(<section>_router)`.
4. Add the frontend component(s) to `type-explorer.html` and a tab button in the `App` component's tab bar.
5. Update this document and README.md.

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
