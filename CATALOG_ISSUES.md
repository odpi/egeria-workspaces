# Tech Catalog — Issues & Lessons Learned

Tracks outstanding work, known bugs, and pyegeria API lessons discovered while building The Catalog (`tech_catalog_handler.py` + `tech-catalog.html`).

---

## Lessons Learned — pyegeria API defaults

Every `find_*` method in pyegeria has a status-list parameter that **defaults to a single active state**, silently filtering out any element that hasn't had that status explicitly set. In the Coco Pharma demo data, almost nothing has an explicit status, so everything was invisible until these were overridden to `[]`.

| pyegeria method | Status param | Default | Fix applied |
|---|---|---|---|
| `find_infrastructure` | `deployment_status_list` | `["ACTIVE"]` | `deployment_status_list=[]` |
| `find_data_assets` | `content_status_list` | `["ACTIVE"]` | `content_status_list=[]` |
| `find_processes` | `activity_status_list` | `["IN_PROGRESS"]` | `activity_status_list=[]` |

**Rule:** Always pass `<status_param>=[]` on any `find_*` call unless the user has explicitly requested status filtering.

**Also:** All list calls now use `graph_query_depth=0` (performance); all detail calls use `graph_query_depth=3` (full property/relationship data for display).

---

## Lessons Learned — Endpoints

`Endpoint` is NOT an Asset subtype — `AssetMaker.find_assets(metadata_element_type="Endpoint")` returns nothing. Must use `ConnectionMaker.find_endpoints()` and `ConnectionMaker.get_endpoint_by_guid()`.

`ConnectionMaker.__init__` takes `server_name` (positional), not `view_server` like `AssetMaker`.

---

## Lessons Learned — Mermaid diagrams

Two separate diagram paths exist in the detail pane:

1. **`AvailableMermaidDiagrams`** — renders mermaid fields embedded in the element response (`edgeMermaidGraph`, `localLineageGraph`, etc.). These require `graph_query_depth > 0`. Now passed through by `_serialize()` via `_MERMAID_FIELDS` set. `mermaidGraph` and `anchorMermaidGraph` are intentionally excluded from this path (handled by buttons below).

2. **`MermaidSection` buttons** — "Load Context Diagram" / "Load Anchored Graph" fetch from `mermaid_handler.py` via `ClassificationExplorer.get_element_by_guid` and `MetadataExpert.get_anchored_element_graph`. These are on-demand, separate from the detail fetch.

**Bug fixed:** `DiagramPanel` was calling `.text()` on the JSON response and passing the raw JSON string to Mermaid.js. Fixed to `.json()` + extract `data.mermaidGraph`.

**Bug fixed:** Mermaid fields were stripped by `_serialize()`. Now passed through for all `_MERMAID_FIELDS`.

**Bug fixed:** Mermaid field names were appearing in the Properties table. Fixed by adding `_ALL_MERMAID_FIELDS` to `skipKeys` in `AssetDetail`.

**Credentials note:** `MermaidSection` fetch URLs don't include credentials — the mermaid handler uses env var defaults. If a user authenticates with non-default credentials, diagram fetches use the wrong identity. This is a known limitation.

---

## Outstanding Issues

### O-1: List-level mermaid graph discarded
`find_*` calls may return a result-set-level `mermaidGraph` at the response root alongside the elements. `_safe_list()` only extracts the elements list and discards any top-level fields. If Egeria generates a diagram of all found elements, it never reaches the frontend.

**Status:** Not yet fixed. Needs a live test to confirm whether the response root actually contains a mermaid graph.

### O-2: `_safe_list` only handles `"items"` key
```python
if isinstance(raw, dict) and "items" in raw:
    return raw["items"]
```
pyegeria may use `"elements"` or `"elementList"` as the list key in some response formats. If so, the handler silently returns `[]`. Needs a live response inspection to confirm.

**Status:** Not yet fixed. Confirm response key with a live test.

### O-3: `AvailableMermaidDiagrams` skips `mermaidGraph`
`mermaidGraph` is in `_MERMAID_SECTION_FIELDS` and excluded from inline rendering — it's expected from the `MermaidSection` on-demand button. But `MermaidSection` re-fetches via a separate API call even when `_serialize()` already passed the embedded `mermaidGraph` through. Wasted fetch.

**Fix options:**
- (a) Pre-populate the "Context Diagram" button state from the embedded `mermaidGraph` (avoids second fetch)
- (b) Remove `mermaidGraph` from `_MERMAID_SECTION_FIELDS` so it renders inline immediately

**Status:** Not yet fixed.

### O-4: `DeployedSoftwareComponent` results — needs live retest
Added `activity_status_list=[]` — previously returned 0. Now should return connectors catalogued in the Egeria runtime.

**Status:** Fixed in code, needs live test confirmation.

### O-5: Data assets (DataStore / DataFeed / DataSet) — needs live retest
Added `content_status_list=[]` — previously returned 0.

**Status:** Fixed in code, needs live test confirmation.

### O-6: ITInfrastructure — needs live retest
Added `deployment_status_list=[]` — previously returned 0.

**Status:** Fixed in code, needs live test confirmation.

### O-7: Endpoints — needs live retest
Switched from `AssetMaker.find_assets(metadata_element_type="Endpoint")` to `ConnectionMaker.find_endpoints()`. Previously returned wrong/empty results.

**Status:** Fixed in code, needs live test confirmation.

### O-8: `get_software_capability_by_guid` optimisation
The detail pane for Software Capabilities does an O(n) scan (`find_software_capabilities(search_string="*")` then filter by GUID). `get_software_capability_by_guid(guid)` exists on `AssetMaker` in 6.0.13.6 and could replace this with a direct lookup.

**Status:** Not yet implemented. Low priority (50 items is fast).

### O-9: Mermaid diagram credentials not forwarded
`MermaidSection` fetches `/api/mermaid/{guid}` without passing the user's credentials as query params. `mermaid_handler.py` falls back to env var defaults. Portal-authenticated users with non-default credentials get diagrams from the wrong identity.

**Status:** Not yet fixed.

### O-10: DeployedAPI mermaid diagrams
APIs section shows no diagrams. Likely because `get_element_by_guid` (ClassificationExplorer) returns no `mermaidGraph` for `DeployedAPI` elements in Coco data. Needs live test of `/api/mermaid/{guid}` with a real API GUID to confirm data vs display issue.

**Status:** Under investigation.
