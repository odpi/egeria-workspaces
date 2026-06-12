# Tech Catalog — Issues & Lessons Learned

Tracks bugs fixed, lessons learned, and outstanding work for The Catalog (`tech_catalog_handler.py` + `tech-catalog.html`). Updated as of **2026-06-11**.

---

## Lessons Learned

### L-1: pyegeria `find_*` status defaults silently hide most Coco data

Every `find_*` method has a status-list parameter that defaults to a single active state. In Coco Pharma demo data, almost nothing has an explicit status set, so everything was invisible until these were overridden to `[]`.

| pyegeria method | Status param | Default | Fix |
|---|---|---|---|
| `find_infrastructure` | `deployment_status_list` | `["ACTIVE"]` | `deployment_status_list=[]` |
| `find_data_assets` | `content_status_list` | `["ACTIVE"]` | `content_status_list=[]` |
| `find_processes` | `activity_status_list` | `["IN_PROGRESS"]` | `activity_status_list=[]` |

**Rule:** Always pass `<status_param>=[]` on any `find_*` call unless the user has explicitly requested status filtering.

**Depth rule:** List calls use `graph_query_depth=0` (performance); detail calls use `graph_query_depth=3` (full property/relationship graph for display).

---

### L-2: `Endpoint` is not an Asset — requires `ConnectionMaker`

`AssetMaker.find_assets(metadata_element_type="Endpoint")` returns nothing. `Endpoint` is not in the Asset type hierarchy. Must use `ConnectionMaker.find_endpoints()` and `ConnectionMaker.get_endpoint_by_guid()`.

`ConnectionMaker.__init__` takes `server_name` (positional), not `view_server` like `AssetMaker`.

---

### L-3: `ConnectionMaker` rejects a reused Bearer token in its constructor

`ConnectionMaker.__init__` calls `check_connection()` immediately. Passing a Bearer token obtained from `AssetMaker.get_token()` causes a 401 on that handshake — the `/api/about` check fails. The symptom was endpoint detail requests returning 404 (the exception was silently swallowed).

**Fix:** `_connection_maker_from_asset_maker()` now omits `token=` and calls `cm.create_egeria_bearer_token()` after construction. This adds one extra auth round-trip per endpoint detail request, which is acceptable.

---

### L-4: pyegeria relationship items nest the related element under `relatedElement`

`_extract_relationships()` originally stripped the outer item wrapper by doing:
```python
elem = {k: v for k, v in item.items() if k not in ("relationshipHeader", "relationshipProperties")}
```
This left an empty dict because pyegeria's `RelatedMetadataElementSummary` puts the actual element inside a nested `relatedElement` key:
```json
{
  "relationshipHeader": {...},
  "relationshipProperties": {...},
  "relatedElement": {
    "elementHeader": { "guid": "...", "type": { "typeName": "SecretsCollection", "superTypeNames": ["DataSet", ...] } },
    "properties": { "displayName": "cocoUserDirectory" }
  }
}
```
Every relationship was showing an empty `typeName`, empty `displayName`, and no GUID. This also prevented all "View →" navigation buttons from appearing.

**Fix:** `_extract_relationships()` now checks for a nested `relatedElement` with an `elementHeader` and unwraps it. It also extracts `superTypeNames` and passes them as `superTypes` in the serialized output so the frontend can resolve subtype navigation targets.

---

### L-5: Mermaid diagrams had two independent bugs

**Bug 1 — `_serialize()` stripped all mermaid fields (FIXED)**
`_serialize()` only extracted a fixed list of scalar properties and silently discarded everything else. A `_MERMAID_FIELDS` set was added; `_serialize()` now passes through any non-empty mermaid field.

**Bug 2 — `DiagramPanel` called `.text()` on a JSON response (FIXED)**
`DiagramPanel` was calling `.text()` then passing the raw JSON string to Mermaid.js, which failed to parse it. Fixed to `.json()` + extract `data.mermaidGraph`.

**Bug 3 — Mermaid field names appeared in Properties table (FIXED)**
`AssetDetail.skipKeys` didn't include mermaid field names. Fixed by concatenating `_ALL_MERMAID_FIELDS`.

---

### L-6: Cross-navigation requires threading nav state through three component levels

App → SectionView → AssetTabView → AssetDetail is a four-level prop chain. Implemented using a `navTarget` state in App: clicking "View →" calls `onNavigate({guid, section, tab, displayName})`, which sets the section, switches the sub-tab via `useEffect` in SectionView, and triggers a direct detail fetch in AssetTabView via a `useRef` deduplication guard.

Frontend `TYPE_TO_NAV` resolves Egeria types to `{ section, tab }`. A supertype fallback walk handles subtypes not explicitly listed (e.g., `SecretsCollection` → `DataSet` → `data-sets` tab).

---

### L-7: pyegeria renamed `get_asset_graph` → `get_asset_graph_by_guid`

`AssetCatalog.get_asset_graph` no longer exists in the current pyegeria version. The method was renamed to `get_asset_graph_by_guid` with a changed signature: the GUID is the first positional argument (not a keyword `asset_guid=`).

The old name caused `_fetch_detail` to throw `AttributeError` on every call. Because the call was inside a `try/except Exception: pass` block, the failure was completely silent — the backend fell through to the `get_asset_by_guid` fallback (shallower response, no mermaid), making it appear as though the richer data was simply absent.

**Rule:** After any pyegeria upgrade, verify method names directly: `python3 -c "from pyegeria import AssetCatalog; print([m for m in dir(AssetCatalog) if 'asset_graph' in m.lower()])"`.

---

### L-8: Silent exception swallowing in `_fetch_detail` masked auth errors as HTTP 404

`_fetch_detail` had `except Exception: pass` blocks around every call. When an Egeria bearer token expired, pyegeria raised an auth exception (`USER_NOT_AUTHORIZED`, response_code 401/403). The pass block swallowed it, all fallbacks also failed silently, `_fetch_detail` returned `None`, and the endpoint raised HTTP 404.

The symptom was a "brief flash then 404": the frontend immediately shows basic data from the list item, then fires the detail fetch which (after Egeria's HTTP timeout) fails and overwrites with the error banner. The 30-second delay matched the pyegeria HTTP timeout.

**Fix:** Every `except Exception` block in `_fetch_detail` now calls `_is_auth_error(exc)` first and re-raises if true. The endpoint converts auth errors to HTTP 401 (not 403 or 404) so `fetchWithToken`'s auto-refresh logic fires and retries with a fresh token.

---

### L-9: Deep-link `?guid=` routing was hardcoded to `data-assets` section

The SPA's initial-state function always set `section: 'data-assets'` when `?guid=` was present in the URL, regardless of the asset's actual type. Infrastructure assets (e.g. an `Application`) were routed to Data Stores, found nothing matching the GUID, and the detail pane showed an error.

**Fix:** Section is now initialised to `''` when `?guid=` is present. A `useEffect` on `[creds]` calls the new `GET /api/tech-catalog/element-nav?guid=<id>` endpoint, which returns `{typeName, superTypeNames, displayName}`. The frontend walks `TYPE_TO_NAV` (with supertype fallback) to resolve the correct `{section, tab}`, then sets both `section` and `navTarget`. The effect is guarded by a `useRef` so it fires exactly once.

---

### L-10: `AssetDetail` was missing an explicit `mermaidGraph` render

`TechTypeDetail` had a `DiagramPanelFromData` block that renders `item.mermaidGraph` immediately when present. `AssetDetail` did not — it relied on `AvailableMermaidDiagrams`, but `mermaidGraph` is in `_MERMAID_SECTION_FIELDS` which explicitly excludes it from that component. The result was that IT Infrastructure elements (and all Asset types) showed no context diagram even though `get_asset_graph_by_guid` returns one.

**Fix:** Added the same explicit `item.mermaidGraph && React.createElement(DiagramPanelFromData, ...)` block to `AssetDetail`, matching the `TechTypeDetail` pattern.

---

## Outstanding Issues

### O-1: List-level mermaid graph discarded
`find_*` responses may include a top-level `mermaidGraph` field for the whole result set. `_safe_list()` only extracts the `items` list and discards anything else. Unconfirmed whether Egeria actually returns this in practice.

**Status:** Needs live response inspection to confirm.

### O-2: `_safe_list` only handles `"items"` key
```python
if isinstance(raw, dict) and "items" in raw:
    return raw["items"]
```
Some pyegeria responses may use `"elements"` or `"elementList"`. Unconfirmed.

**Status:** Needs live response inspection to confirm.

### O-3: ~~Redundant mermaid fetch when embedded graph already present~~ — RESOLVED

`AssetDetail` now renders `item.mermaidGraph` immediately via `DiagramPanelFromData` (labelled "Context Diagram") when the field is present in the detail response. The `MermaidSection` on-demand button still appears below as a fetch-from-server fallback for cases where the embedded graph is absent. `mermaidGraph` remains in `_MERMAID_SECTION_FIELDS` to keep it out of `AvailableMermaidDiagrams`.

### O-8: Software Capabilities detail uses O(n) scan
The detail pane for Software Capabilities calls `find_software_capabilities(search_string="*", graph_query_depth=3)` then filters by GUID. `get_software_capability_by_guid(guid)` exists on `AssetMaker` (confirmed in 6.0.13.6) and could replace this with a direct lookup.

**Status:** Low priority — list is ~50 items, fast enough today.

### O-9: Mermaid diagram credentials not forwarded
`MermaidSection` fetches `/api/mermaid/{guid}` without passing user credentials as query params. `mermaid_handler.py` falls back to env-var defaults. Portal-authenticated users with non-default credentials get diagrams from the wrong identity.

**Status:** Known limitation, not yet fixed.

### O-10: DeployedAPI mermaid diagrams may not exist in Coco data
APIs section shows no diagrams. Likely because `get_element_by_guid` (ClassificationExplorer) returns no `mermaidGraph` for `DeployedAPI` elements in Coco. Needs live test of `/api/mermaid/{guid}` with a real API GUID to distinguish a data issue from a display issue.

**Status:** Under investigation.
