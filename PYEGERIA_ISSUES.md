# pyegeria / Egeria Upstream Issues

Detailed bug reports for issues hit while building Egeria Explorer, with exact
repro steps so they can be verified and fixed upstream. Compact status tracking
lives in `BACKLOG.md` under "pyegeria Upstream Bugs" (same `PY-#` numbering) —
this document is the expanded version with code you can run directly.

Unless noted otherwise, repro commands assume:
- A running Egeria view server reachable at `https://localhost:9443` (or
  `https://host.docker.internal:9443` from inside a container), view server
  name `qs-view-server`, user `peterprofile` / `secret` (adjust to your env).
- `pip install pyegeria` matching the version noted per issue.

---

## PY-1: `DataDesigner.find_data_value_specifications` calls non-existent `_async_post`

**Status:** fixed — verified 2026-07-14. `_async_post` no longer exists anywhere in
the codebase; `find_data_value_specifications` now routes through the shared
`_async_find_request` helper.

**How to trigger:**
```python
from pyegeria import DataDesigner
mgr = DataDesigner(view_server="qs-view-server", platform_url="https://localhost:9443",
                    user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.find_data_value_specifications(search_string="*")
```

**Expected:** a list of `DataValueSpecification` elements matching the search string.

**Actual:** `AttributeError: 'DataDesigner' object has no attribute '_async_post'`

**Root cause:** the method body calls `self._async_post(...)`, which has never
existed in pyegeria. The correct internal method is `_async_make_request`.

**Workaround:** call `mgr._async_make_request("POST", url, body)` directly against
the `/data-value-specifications/by-search-string` endpoint (see
`_search_data_value_specs()` in `data_design_handler.py`).

---

## PY-2: `get_data_value_specifications_by_name("*")` rejects wildcard

**Status:** not a bug — closed 2026-07-15, confirmed by design (Dan). `by_name`
methods are a complete-match lookup: they match a full `displayName` or
`qualifiedName`, not a filter/search pattern, so a bare `"*"` sentinel was
never meant to mean "list all" here. Wildcard/substring listing is what the
`find_*` (`_by_search_string`) methods are for — `find_data_value_specifications`
(fixed by PY-1) is the correct call for listing `DataGrain`/`DataClass`. The
`_async_get_name_request` helper's `"*"` → `None` mapping (still present,
still correct) exists so a caller who passes `"*"` gets a clean "name
required" error instead of a silently-mangled `.*` literal match — it is not,
and was never intended to be, a listing affordance.

**How to trigger (expected behavior, not a defect):**
```python
from pyegeria import DataDesigner
mgr = DataDesigner(view_server_name="qs-view-server", platform_url="https://localhost:9443",
                    user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.get_data_value_specifications_by_name("*")
```
(Note: the constructor parameter is `view_server_name`, not `view_server`, on
the currently deployed version — differs from the constructor of some other
OMVS clients, e.g. `ReferenceDataManager`.)

**Expected:** all `DataValueSpecification` elements (wildcard listing), matching
the convention used by most other `get_*_by_name` methods in pyegeria.

**Actual:** server error `OPEN-METADATA-400-004: The name passed on the name
parameter of getDataValueSpecificationsByName is null` — the `"*"` sentinel is
no longer mangled into an invalid literal, but the endpoint still rejects a
missing/null name outright.

**Workaround (still required):** use `find_data_value_specifications(search_string="*")`
(hits `/by-search-string`, fixed by PY-1) for listing `DataGrain`/`DataClass`
instead of `get_data_value_specifications_by_name`. `_search_data_value_specs()`
in `data_design_handler.py` can likely be simplified to call
`find_data_value_specifications` directly now that PY-1's crash is fixed —
recommend testing that swap before removing the manual `_async_make_request`
call it currently uses.

---

## PY-3: `find_all_solution_blueprints` / `find_all_solution_components` missing in 6.0.12.2

**Status:** fixed/moot — verified 2026-07-14. Both methods exist in the current
codebase (pyegeria 6.0.16.18), well past the 6.0.12.4 floor where they were
added. Was a version-pinning issue, not a code defect.

**How to trigger:**
```python
from pyegeria import SolutionArchitect
mgr = SolutionArchitect(view_server="qs-view-server", platform_url="https://localhost:9443",
                         user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.find_all_solution_blueprints()
```

**Expected:** all solution blueprints returned.

**Actual (on pyegeria 6.0.12.2):** `AttributeError` — the method was added in
6.0.12.4 but the container was pinned to 6.0.12.2 at the time.

**Workaround:** use `find_solution_blueprints(search_string="*")` /
`find_solution_components(search_string="*")`, which exist in both versions.

**Note:** verify current pinned version before re-testing — this may already be
fixed by a floor bump.

---

## PY-4: `ServerClient.update_comment` sends `mergeUpdate: true` but server still demands `qualifiedName`

**Status:** done (workaround shipped, not an upstream fix)

**How to trigger:**
```python
from pyegeria import CommentManager  # or whichever OMVS client exposes update_comment
mgr = CommentManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                      user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.update_comment(comment_guid="<guid>", body={"commentText": "edited text"})
```

**Expected:** partial update succeeds since `merge_update` defaults to `True`
(only the supplied fields should be required).

**Actual:** `OPEN-METADATA-400-004` demanding `qualifiedName`, even though the
request body already sets `"mergeUpdate": true`.

**Workaround:** `egeria_feedback_handler.py` fetches the comment first via
`get_comment_by_guid`, extracts `qualifiedName`, and builds the update body
manually so it's always present regardless of `mergeUpdate`.

---

## PY-5: `get_notes_for_note_log` broken pre-6.0.14.6, version-sensitive

**Status:** fixed in 6.0.14.6/.7 — **regression risk on any `pip install --upgrade` that lands on 6.0.14.4/.5**

**How to trigger the broken behavior (pyegeria 6.0.14.4 or .5):**
```python
from pyegeria import NoteLogManager  # or whichever OMVS client has the mixin
mgr = NoteLogManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                      user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.get_notes_for_note_log(note_log_guid="<guid-of-a-note-log>")
```

**Expected:** the list of notes contained in the note log.

**Actual (6.0.14.4/.5):**
- Default `metadata_element_type_name="Action"` → server error
  `OMAG-REPOSITORY-HANDLER-404-001` ("guid is of type NoteLog rather than Action").
- Passing `metadata_element_type_name="NoteLog"` returns the **log itself**, not
  its notes.
- Large logs (hundreds of entries) time out.

**Fixed in 6.0.14.6+:** default kwargs (no `metadata_element_type_name`
override) now return the notes list, or the sentinel string `"No elements
found"` for a genuinely empty log. **Gotcha:** do NOT pass
`metadata_element_type_name="NoteLog"` anymore — it now returns 0 notes.

**Regression seen 2026-06-17:** a plain `pip install pyegeria --upgrade` inside
the Docker build pulled 6.0.14.4 from PyPI (a point release had been yanked/
reordered), silently emptying the Egeria Explorer Note Logs tab in production.

**Mitigation shipped:** floor-pinned `pyegeria>=6.0.17.5` in both
`Dockerfile-fast-api` and `requirements.txt` (freshstart + quickstart). Note
that `uvicorn --reload` only watches `.py` files — a package upgrade needs an
explicit container/worker restart to take effect, which is why the regression
went unnoticed for a while.

---

## PY-6: `find_note_logs('*')` is O(total notes across every log) at default depth

**Status:** not a pyegeria bug — reclassified 2026-07-14. This is Egeria view
server behavior: `graph_query_depth` controls how much relationship graph the
server computes per element, and defaulting to depth 3 is a deliberate
trade-off (rich results by default), not a defect. pyegeria already exposes
`graph_query_depth=0` for callers who want the cheap listing. No client-side
fix needed; left here for reference/discoverability only.

**How to trigger:**
```python
import time
from pyegeria import NoteLogManager
mgr = NoteLogManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                      user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()

t0 = time.time()
mgr.find_note_logs("*")
print(time.time() - t0)   # ~30-70s on the qs demo data
```

**Expected:** a fast "list of note logs" call, since callers usually just want
names/GUIDs to populate a list UI.

**Actual:** at the default graph query depth, the call inlines **every note
log's full `noteLogEntries` array**. On the qs demo data two system logs hold
~1000 / ~500 entries each, making a supposedly cheap listing call take
30-70 seconds — unusable directly in a request/response HTTP handler.

**Workaround:** `graph_query_depth=0` **is silently accepted via `**kwargs`
even though it's not in the method signature**, and brings this down to ~0.3s
(returns names/qualifiedNames only, no `noteLogSubjects`/`noteLogEntries`).
```python
mgr.find_note_logs("*", graph_query_depth=0)   # ~0.3s
```
`notelog_handler.py`'s list view uses this; detail view does a second,
separately-bounded call (`get_notes_for_note_log(guid, page_size=100)`) for the
actual entries.

**Suggested upstream fix:** either (a) make `graph_query_depth=0` the default
for `find_note_logs`, or (b) document that the entries expansion is
depth-gated and add it explicitly to the method signature instead of leaving
it as an undocumented passthrough kwarg.

---

## PY-7 / PY-8 / PY-11: `as_of_time` missing or silently dropped on several methods

**Status:** fixed, semantically re-verified 2026-07-15 (not just "no
`TypeError`" — actual behavior change confirmed against qs demo data on the
deployed 6.0.16.18). Below each method has a real before/after count where
`as_of_time` set to a date before the data existed returns **zero** results
vs. the real count for "now" — proof `as_of_time` is genuinely threaded to
the Egeria query, not just silently accepted:

| Method | Class used | "now" result | `as_of_time="2000-01-01T00:00:00Z"` result |
|---|---|---|---|
| `find_note_logs` | `CollectionManager` | `4` note logs | `"No elements found"` |
| `get_technology_type_elements` | `AutomatedCuration` | `108` elements (filter `"File"`) | `"No elements found"` |
| `get_collection_members` | `CollectionManager` | `12` members (real collection GUID) | `"No elements found"` |
| `find_data_structures` | `DataDesigner` | `94` structures | `"No elements found"` |

Repro for the first row:
```python
from pyegeria import CollectionManager
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
mgr = CollectionManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                         user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
r_now  = mgr.find_note_logs("*", graph_query_depth=0)
r_2000 = mgr.find_note_logs("*", graph_query_depth=0, as_of_time="2000-01-01T00:00:00Z")
print(len(r_now), r_2000)   # 4 "No elements found"
```
**Independently re-verified 2026-07-31** (real demo data now loaded for both
types) — same before/after recipe, against the deployed container:

| Method | Class used | "now" result | `as_of_time="2000-01-01T00:00:00Z"` result |
|---|---|---|---|
| `find_information_supply_chains` | `SolutionArchitect` (moved off `GovernanceOfficer` since this issue was first filed — no `find_information_supply_chains` method exists on `GovernanceOfficer` anymore) | `18` ISCs | `"No elements found"` |
| `find_governance_definitions` | `GovernanceOfficer` | `100` definitions | `"No elements found"` |

Both confirmed genuinely time-scoped, not silently-accepted.

**`get_valid_metadata_values` reclassified, not a pyegeria fix:** checked the
ground-truth `.http` files — `get-valid-metadata-values/{propertyName}` is a
plain GET endpoint taking only `typeName`/`startFrom`/`pageSize` query params;
`asOfTime` never appears there, only on POST-body search/filter endpoints
elsewhere. The Egeria server doesn't expose historical-query capability on
this endpoint at all, so adding an `as_of_time` param client-side would be
dead code (silently ignored server-side) — the same "looks accepted, has no
effect" failure mode this issue originally complained about, just moved one
layer down. No pyegeria change needed; this would need an Egeria REST API
change to add `asOfTime` support to that endpoint first.

**Expected:** consistent with `find_communities`/`find_projects`/etc., which
already accept and honor `as_of_time` directly — these now do too.

**Impact:** time-travel (viewing metadata as of a past date) is unblocked in
Egeria Explorer for: Tech Type member lists, Note Logs, Data Design
specs/structures, and Collections (confirmed); Information Supply Chains and
Governance definitions (expected fixed, not independently data-verified).
Reference Data / Valid Values lists remain blocked — Egeria server
limitation, not pyegeria (see above).

---

## PY-9: Local `as_of_time` fixes not shipped to the deployed pyegeria package

**Status:** likely resolved — verified 2026-07-14. `get_linked_projects`,
`get_collection_members`, and `get_data_field_by_guid` all have `**kwargs` in
current source, and the deployed container is at 6.0.16.18 (past the 6.0.15.5
mentioned in the original report).

**Live-server smoke test done 2026-07-15 — confirmed with real semantic
effect, not just absence of `TypeError`:**
```python
from pyegeria import CollectionManager
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
mgr = CollectionManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                         user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
guid = "dbc14481-fa8d-42eb-9bce-a7dad33a6779"   # a real qs collection with 12 members
r_now  = mgr.get_collection_members(guid)
r_2000 = mgr.get_collection_members(guid, as_of_time="2000-01-01T00:00:00Z")
print(len(r_now), r_2000)   # 12 "No elements found"
```
**`get_data_field_by_guid` — confirmed 2026-07-31** with a real `DataField`
GUID (`DataDesigner.find_data_fields("*", graph_query_depth=0)`, picked
`52c5868b-b8d9-4315-8965-8dd92256d6c7`): "now" returns the real element;
`as_of_time="2000-01-01T00:00:00Z"` raises `PyegeriaAPIException` /
`OMAG-REPOSITORY-HANDLER-404-007` ("not found") — the correct by-guid-getter
equivalent of a find method's `"No elements found"` (same 404-for-not-yet-
existing-at-that-time semantics already documented for PY-10's
`get_asset_by_guid`). Genuinely time-scoped, confirmed.

**`get_linked_projects` — real, separate correctness bug found 2026-07-31,
independent of `as_of_time`.** Checked all 29 qs demo projects
(`ProjectManager.find_projects("*", graph_query_depth=0)`) —
`get_linked_projects(guid)` returns `"No elements found"` for every single
one, including `"Sustainability Campaign"`
(`5d0057f6-7bb5-4693-961c-48cec3ea5307`), which demonstrably **does** have a
real `ProjectHierarchy` relationship: `ProjectManager.get_project_by_guid(guid)`
returns it directly in its own `managedProjects` field
(`RelatedMetadataHierarchySummary`, `typeName: "ProjectHierarchy"`). So
`get_linked_projects` itself doesn't surface real relationship data at all
today, "now" or otherwise — this can't be attributed to a lack of test data
(the earlier note above, "the guid used didn't have linked projects," was an
incomplete test — a guid *with* real links does exist and still shows
nothing via this method). Substituted `get_project_by_guid`'s
`managedProjects` field for the `as_of_time` check instead, since that's the
field that actually carries the relationship: "now" call succeeds with real
`managedProjects` data; `as_of_time="2000-01-01T00:00:00Z"` raises the same
404 `PyegeriaAPIException` as `get_data_field_by_guid` above — so
`as_of_time` itself is confirmed working on `get_project_by_guid`, but
`get_linked_projects`'s own relationship-resolution logic needs its own,
separate investigation — filed as PY-22 below.

`find_data_value_specifications` (PY-1) still has no `DataValueSpecification`
demo data loaded as of 2026-07-31 (same as 2026-07-15) — both "now" and
year-2000 calls return `"No elements found"`, still genuinely inconclusive
either way. Loading real `DataValueSpecification` test data would close this
out definitively; not done here (writes to the shared demo environment,
deliberately not done without being asked).

**Fix needed:** none for `as_of_time` itself — that part is resolved on the
currently deployed package for every method checked. `get_linked_projects`'s
relationship-resolution bug is unrelated to `as_of_time` and needs its own
fix/investigation.

---

## PY-10: (closed, not a bug) Asset detail by-guid "rejecting" `asOfTime`

**Status:** closed — investigated 2026-06-21, confirmed not a defect.

`get_asset_graph_by_guid` / `get_asset_by_guid` **do** honor `asOfTime`
correctly. The original 404/500 reports were caused by test timestamps (2020,
2026-06-01) that predate the entity's repository version after the demo data
was reloaded on 2026-06-17 — Egeria correctly reports "not found at that time"
(`OMAG-REPOSITORY-HANDLER-404-007`), surfaced as 404 by the by-guid retrieve
and 500 by the graph endpoint (the graph endpoint's 500-vs-404 mapping is a
minor rough edge but not the reported bug). No pyegeria/Egeria change needed;
Egeria Explorer's asset detail handler now degrades this to a clean 404 with a
friendly "not present at the selected time" message.

---

## PY-12: `pyegeria.ReferenceDataManager` does not have specification-property or valid-metadata-value methods

**Status:** open — not necessarily a bug, but a sharp edge worth documenting/fixing in method placement or docs.

**Environment:** pyegeria 6.0.16.16.

**How to trigger:**
```python
from pyegeria import ReferenceDataManager
mgr = ReferenceDataManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                            user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()
mgr.get_specification_property_types()
```

**Expected (reasonable assumption):** since `ReferenceDataManager` is the
class already used successfully for `get_valid_metadata_values`/
`lookup_valid_values` elsewhere in this codebase, it's natural to assume all
"valid metadata"-flavored methods (including specification properties) live on
it too.

**Actual:** `AttributeError: 'ReferenceDataManager' object has no attribute
'get_specification_property_types'`

**Root cause:** `ReferenceDataManager` inherits only from `ServerClient`
(it's for *business* reference data — country codes, currency codes, etc.),
**not** from `ValidMetadataManager`. `get_valid_metadata_values` happens to
work on it because that particular method lives on the shared `ServerClient`/
`BaseServerClient` base class, not on `ValidMetadataManager` — which makes the
class boundary easy to misjudge. The specification-property methods
(`get_specification_property_types`, `get_specification_property_by_type`,
`get_specification_property_by_name`, `get_specification_property_by_guid`,
`find_specification_property`) only exist on **`pyegeria.SpecificationProperties`**
(also `ValidMetadataManager` subclasses: `ValidMetadataLists`, `ValidTypeLists`).

**Fix:** use `pyegeria.SpecificationProperties(...)` for these calls instead.

**Suggested upstream improvement:** either (a) add a class-level docstring
note on `ReferenceDataManager` clarifying it does not cover specification
properties/valid metadata values despite the similar naming, or (b) expose a
single unified client (or a documented decision tree) for "which OMVS client
class do I need" across `ReferenceDataManager` / `SpecificationProperties` /
`ValidMetadataLists` / `ValidTypeLists` / `MetadataExpert`, since several of
these overlap in purpose and are easy to reach for interchangeably.

---

## PY-13: `SpecificationProperties.get_specification_property_by_type` always returns 400 regardless of the value passed

**Status:** open, reclassified as Egeria server bug 2026-07-14 — not
actionable in pyegeria. Root cause is server-side (Spring `@RequestParam` enum
binding drifted from the OpenAPI-declared enum, per the original analysis
below). No pyegeria code change will fix a 400 the server returns for every
input; keep the `find_specification_property("*", ...)` workaround in place
and track this against the Egeria server issue tracker. Re-verify once the
in-flight Egeria server fixes land.

**Environment:** pyegeria 6.0.16.16, Egeria view server 6.1-SNAPSHOT.

**How to trigger:**
```python
from pyegeria import SpecificationProperties
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

mgr = SpecificationProperties(view_server="qs-view-server", platform_url="https://localhost:9443",
                               user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()

# get_specification_property_types() works and returns e.g. "PlaceholderProperty"
# as one of the keys (PascalCase type names).
types = mgr.get_specification_property_types()
print(list(types.keys())[:5])

# Passing that type name straight through fails:
mgr.get_specification_property_by_type("PlaceholderProperty")
```

**Expected:** the list of specification properties whose type matches
`PlaceholderProperty`.

**Actual:** `pyegeria.core._exceptions.PyegeriaClientException` wrapping an
HTTP 400 from the view server, body:
```json
{"timestamp":"...","status":400,"error":"Bad Request","path":"/servers/qs-view-server/api/open-metadata/valid-metadata/specification-properties/by-type"}
```
with no further detail. This 400 is returned for **every** value tried:
- the plain type name (`"PlaceholderProperty"`)
- the enum-wrapped form shown in the endpoint's own OpenAPI spec, e.g.
  `"SpecificationPropertyType{placeholderProperty}"`
- the same enum-wrapped form, percent-encoded for the `{`/`}` characters

**Extra detail for whoever picks this up:** the OpenAPI schema for
`POST /servers/{serverName}/api/open-metadata/{urlMarker}/specification-properties/by-type`
declares `specificationPropertyType` as a **required query param** with an
`enum` of literal strings that look like Java `toString()` output, e.g.:
```
"SpecificationPropertyType{placeholderProperty}"
"SpecificationPropertyType{replacementAttribute}"
"SpecificationPropertyType{supportedTemplate}"
...
```
Fetch this yourself to confirm against your running server:
```python
import httpx
r = httpx.get("https://localhost:9443/v3/api-docs", headers=mgr.headers, verify=False)
spec = r.json()
print(spec["paths"]["/servers/{serverName}/api/open-metadata/{urlMarker}/specification-properties/by-type"])
```
Every one of these enum literal values, tried verbatim as the query param,
still 400s — suggesting the Spring `@RequestParam` enum converter registered
for this parameter does not actually accept the same string form that
springdoc used to generate the schema's enum listing (i.e., the OpenAPI spec
and the real converter have drifted apart), or there's a related failure with
how `pyegeria` posts the required `ResultsRequestBody` alongside a query
param on the same request. Needs someone with server-side access to add
logging/debug the `@RequestParam` binding for `getSpecificationPropertyByType`.

**Workaround (shipped in `valid_values_handler.py`, both freshstart/quickstart
copies of Egeria Explorer):** use the working
`find_specification_property("*", ...)` (by-search-string) endpoint instead,
and filter client-side on `element["properties"]["identifier"]`, which holds
the camelCase form of the type name (`"PlaceholderProperty"` ->
`"placeholderProperty"`). See PY-14 for a critical performance caveat on that
workaround.

**Confirmed 2026-07-17 (Dan):** `find_specification_property` is defined on
`ValidMetadataManager`, not `SpecificationProperties` itself —
`SpecificationProperties` just inherits it (see PY-12). Calling it via
`ValidMetadataManager.find_specification_property` directly (or any class
that inherits from it) is the correct, supported path; no need to instantiate
`SpecificationProperties` specifically just for this one call.

---

## PY-14: `find_specification_property` (and likely other `find_*` methods) is O(n) per element unless `graph_query_depth=0` — same root cause as PY-6

**Status:** not a pyegeria bug — reclassified 2026-07-14, same as PY-6. This
is Egeria view server behavior (graph computation cost scales with
`graph_query_depth`), not a defect; `graph_query_depth=0` is already the
documented, working opt-out for bulk listing calls. No client-side fix
needed.

**Environment:** pyegeria 6.0.16.16.

**How to trigger:**
```python
import time
from pyegeria import SpecificationProperties
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

mgr = SpecificationProperties(view_server="qs-view-server", platform_url="https://localhost:9443",
                               user_id="peterprofile", user_pwd="secret")
mgr.create_egeria_bearer_token()

t0 = time.time()
r = mgr.find_specification_property("*", page_size=1000)   # default graph_query_depth=3
print("default depth:", time.time() - t0, "elements:", len(r))

t0 = time.time()
r = mgr.find_specification_property("*", page_size=1000, graph_query_depth=0)
print("depth=0:       ", time.time() - t0, "elements:", len(r))
```

**Expected:** a bulk search/listing call should be roughly linear in the
number of results and fast enough for interactive use (sub-second to a couple
seconds for 1000 elements).

**Actual (measured on qs demo data, 1000-element result set):**
- Default `graph_query_depth=3`: **~50 seconds**
- `graph_query_depth=0`: **~0.6-2 seconds**

Both calls return identical flat `properties` data per element (displayName,
description, preferredValue, identifier, dataType, etc.) — the only
difference at depth 0 is the omission of `mermaidGraph` and any expanded
relationship graph, which most bulk-listing callers don't need anyway.

**Root cause:** same as PY-6 (`find_note_logs`) — the default graph query
depth makes the view server compute a full relationship graph / mermaid
diagram per returned element, turning an O(n) listing into effectively O(n ×
graph-computation-cost). This is at minimum the second unrelated `find_*`
method with this exact performance cliff; there are likely more.

**Confirmed 2026-07-17 (Dan):** the cost is incurred by the *attempt* to
compute the graph, not by how much actually comes back — an element with no
relationships to traverse still costs the same as one with many, because
Egeria has to do the traversal work to discover that there's nothing there.
So this scales with `graph_query_depth` and result-set size, not with how
much metadata actually exists to return. Confirms this is inherent cost, not
a bug — nothing to fix, `graph_query_depth=0` remains the correct opt-out.

**Workaround:** always pass `graph_query_depth=0` explicitly on any `find_*`
or `get_*` bulk-listing call unless the caller actually needs the
graph/mermaid output. Used in `valid_values_handler.py`'s Specification
Property Values lookup (`find_specification_property("*", page_size=1000,
graph_query_depth=0)`) and `notelog_handler.py`'s note log listing.

**Suggested upstream fix:** either (a) default `graph_query_depth` to `0`
across `find_*`/list-style methods (opt-in to the expensive graph, not
opt-out), or (b) split "list" and "graph" into genuinely separate REST
operations so the expensive computation isn't hidden behind a depth parameter
that's easy to leave at its default.

---

## PY-15: Postgres repository connector ignores `matchCriteria` on `SearchClassifications` — multi-classification search always returns 0

**Status: FIXED and CLOSED — verified 2026-07-17.** Originally confirmed as a
server-side bug 2026-07-15, while building Egeria Insights
(`insights_handler.py`) — not a pyegeria client bug, the client sent the body
faithfully; the Postgres repository connector's SQL generation dropped
`matchCriteria` on the classification-matching path only. Fixed server-side
and re-verified live against `qs-view-server` once the fixed server was
deployed to this environment:

```
ZoneMembership ANY:      150   (unchanged — single-condition baseline)
Confidentiality ANY:       1   (unchanged — single-condition baseline)
Both ANY:                150   (was 0 — now a real, differentiated union)
Both ALL:                  0   ("No elements found" — correct, empty intersection)
Both NONE:               1000  (was 0 — now a real, differentiated count)
```

`ANY`/`ALL`/`NONE` now produce distinct, semantically correct results instead
of all being an unconditional AND that always returned zero. The pytest
regression test below now passes.

**How to trigger:**
```python
import pyegeria, os
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
from pyegeria import MetadataExpert
mgr = MetadataExpert(view_server="qs-view-server", platform_url="https://localhost:9443",
                      user_id="erinoverview", user_pwd="secret")
mgr.create_egeria_bearer_token()

def find(names, match_criteria):
    body = {
        "class": "FindRequestBody",
        "matchClassifications": {
            "class": "SearchClassifications",
            "matchCriteria": match_criteria,
            "conditions": [{"name": n} for n in names],
        },
        "limitResultsByStatus": ["ACTIVE"],
    }
    return mgr.find_metadata_elements(body, start_from=0, page_size=500, graph_query_depth=0)

print(len(find(["ZoneMembership"], "ANY")))                    # 150 on qs demo data
print(len(find(["Confidentiality"], "ANY")))                    # 1
print(find(["ZoneMembership", "Confidentiality"], "ANY"))       # "No elements found"
print(find(["ZoneMembership", "Confidentiality"], "ALL"))       # "No elements found" — same as ANY
print(find(["ZoneMembership", "Confidentiality"], "NONE"))      # "No elements found" — same again
```

**Expected:** `matchCriteria: "ANY"` across two classification names should
return the union — every element carrying *either* classification (151 on qs
demo data, since none carry both). `"ALL"` should return the (here, empty)
intersection. `"NONE"` should return elements carrying neither.

**Actual:** any query naming 2+ classifications in `matchClassifications`
returns zero elements, and the result is identical no matter which
`matchCriteria` value is sent — `ANY`/`ALL`/`NONE` are indistinguishable.
Single-condition queries work correctly and are unaffected.

**Root cause:** `QueryBuilder.getSearchClassificationsClause()` in
`open-metadata-implementation/adapters/open-connectors/repository-services-connectors/open-metadata-collection-store-connectors/postgres-repository-connector/src/main/java/org/odpi/openmetadata/adapters/repositoryservices/postgres/repositoryconnector/database/QueryBuilder.java`
(lines 1036–1078) unconditionally `AND`s an `AND (type_name LIKE '%:<Name>:%' ...)`
clause per classification condition and never reads
`matchClassifications.getMatchCriteria()` at all — confirmed by grepping the
whole file: `MatchCriteria` is read in the *property*-matching path
(`getPropertyComparisonFromPropertyConditions()`, ~line 896: `if
(searchProperties.getMatchCriteria() == MatchCriteria.ANY) { matchOperand =
" or "; }`) but never in the classification-matching path. So the generated
SQL always requires every named classification to appear on the same
classification-table join simultaneously, regardless of what `matchCriteria`
the caller asked for. With two mutually exclusive classification names, no
row can satisfy the `AND`-chain, so the query returns nothing.

**No client-side workaround applied** — `insights_handler.py`'s
`get_summary()` (5-classification `ANY` tally for the Dashboard card) and any
multi-classification compound search in the Governance Search tab are
affected; both currently return correct results only when 0 or 1
classification condition is supplied. Fixing this requires a server-side
change; a full replacement for `getSearchClassificationsClause()` (mirroring
the `ANY`→`or`/`ALL`→`and`/`NONE`→`not(...)` pattern already used for
property conditions) is on file at
`scratchpad/QueryBuilder-classifications-fix.patch` in the session that found
this, pending a proper PR against `postgres-repository-connector`.

**Regression coverage:**
- `egeria-python/tests/functional-tests/test_metadata_expert.py::test_find_metadata_elements_multi_classification_any_match_criteria`
  (pytest, asserts ANY's count >= max of the two single-condition counts) —
  **passes** as of 2026-07-17 (1 passed, run via the `egeria-python` repo's own
  `.venv`).
- `egeria-python/pyegeria/http clients/Egeria-PY15-matchClassifications-bug.http`
  (PyCharm/IntelliJ HTTP Client collection, same assertions via raw REST calls —
  run "Token" then top-to-bottom, or `ijhttp --insecure Egeria-PY15-matchClassifications-bug.http`
  from the CLI) — not re-run this pass (`ijhttp` unavailable outside PyCharm in
  this shell), but the underlying server behavior it asserts on is now proven
  correct via the pytest test above.

---

## PY-16: `ClassificationExplorer.link_elements_as_peer_duplicates` (and its `_async_*` twin) POST to the wrong URL path — always 404s

**Status: FIXED — confirmed 2026-07-17 on pyegeria 6.0.16.20.**
`_async_link_elements_as_peer_duplicates` now builds the URL from
`f"{self.classification_command_root}/related-elements/{element_guid}/peer-duplicate/{peer_duplicate_guid}/attach"`
— verified directly against the running `quickstart-pyegeria-web` container's
installed pyegeria source. Originally confirmed as a client-side bug
2026-07-16, while seeding demo data for the Duplicate Resolution Review pane
(`duplicate_review_handler.py`), whose seed script used a direct
`_async_make_request` workaround (see below) rather than the plain client
call — safe to switch back to the plain `link_elements_as_peer_duplicates`
call now if that seed script is ever re-run.

**How to trigger:**
```python
import pyegeria, os
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
from pyegeria import ClassificationExplorer
ce = ClassificationExplorer(view_server="qs-view-server", platform_url="https://localhost:9443",
                             user_id="erinoverview", user_pwd="secret")
ce.create_egeria_bearer_token()

body = {
    "class": "NewRelationshipRequestBody",
    "properties": {"class": "PeerDuplicateLinkProperties", "statusIdentifier": 0,
                    "steward": "erinoverview", "source": "test", "notes": "test"},
}
ce.link_elements_as_peer_duplicates("<guid-a>", "<guid-b>", body)  # any two valid, same-typed GUIDs
```

**Expected:** creates a `PeerDuplicateLink` relationship, returns its GUID.

**Actual:** `httpx.HTTPStatusError: Client error '404'` — the client posts to
```
.../classification-explorer/elements/{elementGUID}/peer-duplicate/{peerDuplicateGUID}/attach
```
but the real Spring endpoint
(`open-metadata-implementation/view-server-generic-services/classification-explorer/classification-explorer-spring/.../ClassificationExplorerResource.java`,
`linkElementsAsPeerDuplicates`) is mapped at
```
.../classification-explorer/related-elements/{elementGUID}/peer-duplicate/{peerDuplicateGUID}/attach
```
— `elements` vs `related-elements`. Same root cause likely affects
`unlink_elements_as_peer_duplicates` (detach, same path shape). Classification
calls (`set_known_duplicate_classification`/`set_consolidated_duplicate_classification`)
and the read path (`get_relationships`/`get_elements_by_classification`) are
unaffected — confirmed working.

**Workaround used:** called `ce._async_make_request("POST", corrected_url, body)`
directly with the `related-elements` path, bypassing the buggy helper, to seed
the Duplicate Resolution Review pane's demo pair (two `Community` entities,
GAP-5 in `BACKLOG.md`'s type-coverage-gaps section).

**Fix:** in `pyegeria/omvs/classification_explorer.py`,
`_async_link_elements_as_peer_duplicates` (and its detach twin) should build
the URL from `f"{self.classification_command_root}/related-elements/{element_guid}/peer-duplicate/{peer_duplicate_guid}/attach"`.

---

## PY-17: `MetadataExpert.get_metadata_element_by_guid` never returns relationships, at any `graph_query_depth` — use `get_all_related_elements` instead

**Status: not a bug — working as designed (confirmed 2026-07-17, Dan).**
`get_metadata_element_by_guid` is deliberately scoped to the element itself;
`get_all_related_elements` is the correct, separate call for relationships —
this is a two-call design, not a gap in the by-guid method. Originally
flagged 2026-07-16 while fixing the Action Center pane's cross-links
(`action_center_handler.py`, GAP-6 in `BACKLOG.md`) because the accepted
`graph_query_depth` parameter on `get_metadata_element_by_guid` suggested it
should affect relationship inclusion; it doesn't, and that's correct
behavior. No pyegeria change needed — kept below as a usage note (which call
to use for what) rather than a bug report.

**How to trigger:**
```python
import pyegeria, os
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
from pyegeria import MetadataExpert
mgr = MetadataExpert(view_server="qs-view-server", platform_url="https://localhost:9443",
                      user_id="erinoverview", user_pwd="secret")
mgr.create_egeria_bearer_token()

guid = "<a Notification guid known to have Actions/ActionRequester/AssignmentScope relationships>"
for depth in (0, 1, 2, 3):
    el = mgr.get_metadata_element_by_guid(guid, graph_query_depth=depth, output_format="JSON")
    print(depth, sorted(el.keys()))
# every depth prints the same 8 keys — no relationship key ever appears:
# ['classifications', 'elementGUID', 'elementProperties', 'headerVersion',
#  'origin', 'status', 'type', 'versions']
```

**Expected:** at `graph_query_depth >= 1`, the element dict should include its
relationships (as other raw-shape handlers in this codebase assume —
`insights_handler.py`, `glossary_handler.py`, the original `action_center_handler.py`
all built relationship-extraction helpers assuming top-level list-valued keys
would appear on the element itself once `graph_query_depth=1` was passed).

**Actual:** the element dict is byte-identical across `graph_query_depth`
0 through 3 — relationships never appear on it via this call, regardless of
depth.

**Working alternative:** `MetadataExpert.get_all_related_elements(guid, output_format="JSON")`
returns `{"startingElement": <the element>, "elementList": [...], "mermaidGraph": ...}`.
Each `elementList` entry is a relationship-header dict with its own
`type.typeName` (the *relationship* type — `Actions`, `ActionRequester`,
`AssignmentScope`, presumably `ActionTarget` when present) and a nested
`element` key holding the *other* end, in the same raw `elementGUID`/
`elementProperties.propertyValueMap` shape as everything else in this
codebase's raw-shape handlers. This is the actual source of cross-link data —
confirmed live against a real Notification with 3 genuine relationships, all
three showed up correctly via this call and none via `get_metadata_element_by_guid`
at any depth.

**Fix applied**: `action_center_handler.py`'s `get_action()` now calls both —
`get_metadata_element_by_guid` for the element's own properties,
`get_all_related_elements` for relationships — and merges them via
`_relationships_from_related_elements()`. Both envs.

**Audited 2026-07-26 (BACKLOG.md NEXT-6):** checked every other handler for
this same trap. None found — every other by-guid detail call in the codebase
uses a proper OMVS-specific method (`ActorManager.get_actor_role_by_guid`,
`CommunityManager.get_community_by_guid`, etc.), not `MetadataExpert.
get_metadata_element_by_guid`, so this specific trap is contained to the two
places already known: `action_center_handler.py` (fixed above) and the raw
debug-JSON viewer (`/api/debug/raw/{guid}`, expected/by-design — it exists to
show MetadataExpert's raw shape). One near-miss found: the original NEXT-5
investigation used the debug viewer to conclude an Actor Role had no
community relationship, which was a false negative caused by exactly this
trap — the real app endpoint (`get_actor_role_by_guid`) returns it fine. See
BACKLOG.md's "NEXT-5 / NEXT-6" section for the full writeup.

---

## PY-18: `count_relationships_between_elements("Exception")` (276) disagrees with `ClassificationExplorer.get_relationships("Exception")` (55)

**Status:** open — needs Egeria-side investigation. Found 2026-07-24 while wiring
the Egeria Overview dashboard to the new native counting from odpi/egeria#9168.
pyegeria with the `count_metadata_elements` / `count_relationships_between_elements`
methods; a #9168-capable view server.

**Summary:** the OMF metadata-expert **native relationship count** and the
classification-explorer **`get_relationships`** return materially different totals
for the `Exception` relationship type — and *only* that type, among those tested.

**How to trigger:**
```python
from pyegeria import MetadataExpert, ClassificationExplorer
me = MetadataExpert(view_server="qs-view-server", platform_url="https://localhost:9443",
                    user_id="erinoverview", user_pwd="secret"); me.create_egeria_bearer_token()
ce = ClassificationExplorer(view_server="qs-view-server", platform_url="https://localhost:9443",
                    user_id="erinoverview", user_pwd="secret"); ce.create_egeria_bearer_token()

me.count_relationships_between_elements({"class":"FindRelationshipRequestBody","relationshipTypeName":"Exception"})
# -> 276
len(ce.get_relationships(relationship_type="Exception", output_format="JSON", start_from=0, page_size=5000))
# -> 55  (all 55 have exact typeName "Exception"; no effectivity dates)
```

**What it is NOT:**
- Not the type filter — `count(relationshipTypeName="ZZBogus")` errors, and
  `count("SemanticAssignment")` = 397 = `get_relationships` = 397; `License` 2 = 2;
  `Certification` 0 = 0; `AttachedRating` 0 = 0. **Every other tested type matches**;
  only `Exception` diverges (276 vs 55).
- Not status/effectivity — `count("Exception")` is 276 with `limitResultsByStatus=[ACTIVE]`,
  with `effectiveTime=<now>`, and with neither; the 55 `get_relationships` results
  carry no `effectiveFromTime`/`effectiveToTime`.
- `count(no relationshipTypeName)` = 31857 (all relationships), so 276 is a genuine
  type-scoped subset, not "count ignores the filter".

**Open question for Egeria:** what does the metadata-expert count include for
`Exception` that the classification-explorer traversal excludes (subtypes counted
under the supertype? relationships to non-visible / anchored / dangling ends?
access/zone filtering that differs between the two OMVS)? Whichever is "true", the
two APIs should agree for a given type — or the difference should be documented.

**Impact / workaround:** the Overview dashboard keeps **relationship** counts on
`ClassificationExplorer.get_relationships` (so "Open Exceptions" stays consistent
with the Audit app at 55) and uses native counting only for **element** counts.
See `overview_handler.py` `_rel_count` and `OVERVIEW_METRICS.md`.

---

## PY-19: `MetadataExpert.find_relationships_between_elements(relationshipTypeName=…)` returns "No elements found" even when the matching count is non-zero

**Status:** open — found 2026-07-24 alongside PY-18. Same env.

**How to trigger:**
```python
me.count_relationships_between_elements({"class":"FindRelationshipRequestBody","relationshipTypeName":"SemanticAssignment"})
# -> 397
me.find_relationships_between_elements({"class":"FindRelationshipRequestBody","relationshipTypeName":"SemanticAssignment"},
                                       start_from=0, page_size=5000)
# -> "No elements found"   (same for "Exception", which counts 276)
```

**Expected:** a plain type-scoped `find_relationships_between_elements` should return
the relationships the sibling `count_relationships_between_elements` counts (or the
two methods should document why they differ).

**Actual:** the find returns the empty-result string for a bare `relationshipTypeName`
query even though the count is non-zero — suggesting the find needs anchor element
GUIDs (or has a bug), while the count does not.

**Impact / workaround:** none in the dashboard — element counts use
`count_metadata_elements`; relationship counts/lists use
`ClassificationExplorer.get_relationships`, which works. Flagged because the
count/find asymmetry within the same OMVS is confusing and blocks using the
metadata-expert find as a fallback for the native relationship count.

---

## PY-20: Paging / sequencing strategy for "load-all" list endpoints — DESIGN DISCUSSION (high priority)

**Status:** open — **design discussion, not a confirmed bug.** High-priority
follow-up. Raised 2026-07-24 from the glossary-term aliases fix: aliased terms were
missing from the default listing because of how the portal loads and sorts lists.

**Observations (repro, `find_glossary_terms`, qs-view-server, 388 terms):**
```python
# start_from paging works — each page is a different, non-overlapping slice:
m.find_glossary_terms(search_string="*", start_from=0,  page_size=10, output_format="JSON")   # 10 terms
m.find_glossary_terms(search_string="*", start_from=10, page_size=10, output_format="JSON")   # next 10, no overlap

# BUT sequencing is not reflected in the result order:
m.find_glossary_terms(search_string="*", page_size=10, output_format="JSON",
                      sequencing_order="PROPERTY_ASCENDING", sequencing_property="displayName")
# -> ['Rolling base year','Carbon Intensity','Megawatt Hour','Inventory','Shall', ...]  (server-internal order, not A→Z)
```

So the portal's **"load-all up to a page-size ceiling, then sort/filter in JS"**
pattern (glossary, insights, catalog, …) silently returns an *arbitrary* subset
when a collection exceeds the ceiling: e.g. default `page_size=200` on 388 terms
returns some 200, the endpoint re-sorts *those 200* by `displayName`, and terms
outside that slice (incl. alphabetically-early ones) simply never appear.

**Open questions to decide (not asserting any of these is a defect):**
1. Is `sequencing_order`/`sequencing_property` expected to order the result here,
   or is that behaviour config/connector-dependent? (Determines whether true
   server-side paged UIs are even feasible, or whether fetch-all-then-sort-in-JS
   remains the only reliable sort.)
2. Preferred model: **bounded server-side fetch-all** (loop `start_from` until the
   native `count_metadata_elements` total is reached or a ceiling is hit, return a
   `truncated`/`total` flag) vs a true paged UI. Fetch-all keeps the existing
   instant client-side search; paged UI needs #1 resolved first.
3. **Page-size ceiling is bounded by the view server's configured `maxPageSize`**
   (OMAG server config) — likely well below 5000. Any fetch-all loop must chunk at
   ≤ that limit; the overall load ceiling is a separate product decision. **TBD —
   to be chosen in discussion.**
4. Apply the chosen strategy consistently via a shared helper across all
   "load-all" endpoints, rather than per-handler.

**Current mitigation:** none beyond raising `page_size`, which only lowers the odds
(a single page is still unsorted, so it sorts an arbitrary slice). Tracked for a
deliberate fix once the strategy + `maxPageSize` are agreed.

---

## PY-21: `find_glossary_terms(sequencing_order=..., include_only_classified_elements=...)` returns ZERO results when combined — each filter alone works fine

**Status:** confirmed bug — found 2026-07-28 debugging Egeria Explorer's Perspectives
page showing Perspectives but no Questions. Related to PY-20 (same broken parameter,
different — and more severe — failure mode: not just wrong order, but zero rows).

**How to trigger** (`GlossaryManager.find_glossary_terms`, qs-view-server, 33
`GlossaryTerm`s classified `Question`):
```python
# classification filter alone: 33 hits
mgr.find_glossary_terms(search_string="*", starts_with=True, output_format="JSON",
                        page_size=200, graph_query_depth=0,
                        include_only_classified_elements=["Question"])

# sequencing_order alone (no classification filter): 200 hits (unrelated terms, page_size ceiling)
mgr.find_glossary_terms(search_string="*", starts_with=True, output_format="JSON",
                        page_size=200, graph_query_depth=0,
                        sequencing_order="PROPERTY_ASCENDING")

# BOTH together: 0 hits
mgr.find_glossary_terms(search_string="*", starts_with=True, output_format="JSON",
                        page_size=200, graph_query_depth=0,
                        sequencing_order="PROPERTY_ASCENDING",
                        include_only_classified_elements=["Question"])
# -> []  (or a "No elements found" string, depending on call shape)
```
Isolated further: `sequencing_order="PROPERTY_ASCENDING"` is the trigger —
`sequencing_property` alone (no `sequencing_order`) does **not** break it (still 33
hits). It's specifically `sequencing_order` + a classification filter.

**Expected:** the classification filter's 33 matches, sorted by the given
sequencing property (or, per PY-20, at least returned in server-internal order —
but not silently emptied).

**Actual:** zero rows, with no error — the query silently looks like "nothing
matches" rather than failing loudly, which is what made this hard to spot (the
egeria-workspaces `/api/questions` endpoint returned `{"total": 0}` with a 200
status; only comparing against a live count of Question-classified terms in Egeria
surfaced that this was wrong, not just an empty demo).

**Impact / workaround:** `perspectives_handler.py`'s `get_questions()` used exactly
this broken combination. Fixed by dropping `sequencing_order`/`sequencing_property`
from the call — the endpoint already sorts client-side (`questions.sort(...)` by
`displayName`), so the server-side sequencing was redundant even before this bug was
found. No other known callers currently combine `sequencing_order` with a
classification filter, but worth checking `include_only_classified_elements`/
`matchClassifications` callers generally if new zero-result reports show up
elsewhere.

---

## PY-22: `ProjectManager.get_linked_projects()` doesn't surface real `ProjectHierarchy` relationships

**Status:** open — found 2026-07-31 while finishing the PY-7/8/9/11 `as_of_time`
verification remainder (this method was one of the "not yet confirmed" ones,
originally attributed to "the guid used didn't have linked projects").

**Environment:** deployed `quickstart-pyegeria-web` container, live server.

**How to trigger:**
```python
from pyegeria import ProjectManager
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True
pm = ProjectManager(view_server="qs-view-server", platform_url="https://localhost:9443",
                     user_id="peterprofile", user_pwd="secret")
pm.create_egeria_bearer_token()

guid = "5d0057f6-7bb5-4693-961c-48cec3ea5307"  # "Sustainability Campaign"

# Returns "No elements found" -- wrong, this project has real child projects.
print(pm.get_linked_projects(guid))

# The same relationship IS there, in get_project_by_guid's own response:
p = pm.get_project_by_guid(guid)
print(p["managedProjects"])  # RelatedMetadataHierarchySummary, typeName "ProjectHierarchy" -- real data
```

**Confirmed not a data-availability problem:** checked all 29 qs demo
projects (`find_projects("*", graph_query_depth=0)`) — `get_linked_projects`
returns `"No elements found"` for every single one, including several with
an obvious parent/child naming pattern ("Sustainability Campaign" →
"Design/Define/Implement/Run the sustainability..."). `get_project_by_guid`'s
`managedProjects` field confirms the real relationship exists for at least
"Sustainability Campaign". So `get_linked_projects` itself isn't resolving
`ProjectHierarchy` (or whatever relationship type it's meant to cover) at
all today, independent of any `as_of_time` question.

**Impact:** any caller relying on `get_linked_projects` for project hierarchy
(e.g. Egeria Explorer's Projects tab, if it uses this method for the
parent/child tree) is silently missing real relationship data.

**Not yet investigated:** whether this is a wrong relationship-type filter
inside `get_linked_projects`'s implementation, a wrong request-body shape, or
an Egeria-server-side gap specific to that endpoint (cf. PY-18's "two OMVS
layers can disagree" pattern, and PY-19's structurally similar "count > 0 but
find returns nothing" symptom for a different method) — needs a source read
of `ProjectManager._async_get_linked_projects` next.

---

## PY-23: `MetadataExpert.find_metadata_elements` — pyegeria's own dropped-parameter bug is FIXED (6.0.17.15), but Egeria's server still ignores `startFrom`/`pageSize` on this endpoint

**Status: pyegeria side FIXED, Egeria server side still open.** Found
2026-08-04/05 while building Egeria Insights' relationship search
(`insights_handler.py`) — the `full_count` pagination loop kept re-appending
the same ~1,700 elements on every page until hitting its hard cap, because
`_async_find_metadata_elements` silently dropped `start_from`/`page_size`/
`graph_query_depth` entirely (same "dead parameter" bug shape as ISSUE-25).
Fixed client-side in pyegeria 6.0.17.15 (`startFrom`/`pageSize` now sent as
URL query params, `graphQueryDepth` merged into the body, per the `.http`
ground truth) — see egeria-python `ISSUE-25`/commit `df053ec`.

**But the fix alone doesn't restore real pagination.** Re-verified live
2026-08-05 against `qs-view-server` on the upgraded client (6.0.17.15,
confirmed via a request-spy that the correct URL — `?startFrom=0&pageSize=5`
— actually reaches the wire):

```python
p1 = mgr.find_metadata_elements(body, start_from=0, page_size=5, graph_query_depth=0)
p2 = mgr.find_metadata_elements(body, start_from=5, page_size=5, graph_query_depth=0)
# len(p1) == len(p2) == 1837 (the FULL Asset population, both times)
# set(guids in p1) == set(guids in p2) -- 100% overlap, not two distinct pages
```

The client now sends the spec-correct request; the server returns the same
full, unpaginated result set regardless of what `startFrom`/`pageSize` it was
given. This is an Egeria-server-side gap in the
`metadata-expert/metadata-elements/by-search-conditions` endpoint's handling
of those two query parameters specifically — not yet root-caused on the Java
side (no source read done yet, unlike PY-15's `QueryBuilder` deep-dive).

**Workaround still required and still in place**:
`insights_handler.py`'s `search_elements()` full_count loop dedupes by GUID
while accumulating pages and stops once a page contributes zero new GUIDs —
correct regardless of whether the server ever starts respecting real
pagination (if it does, the loop naturally terminates after the first real
empty/short page instead of after a same-content detection). Do **not**
remove this workaround on the assumption that 6.0.17.15 alone fixes it — it
doesn't.

**Not yet investigated:** whether this affects other `find_*` methods that
share the same `metadata-expert` OMVS service, or is specific to
`by-search-conditions`; whether other repository connectors (this
environment runs Postgres — cf. PY-15's connector-specific root cause) behave
the same way.

---

## Quick reference: which OMVS client class for which purpose

| Need | Class | Notes |
|---|---|---|
| Business reference data (country/currency codes) | `ReferenceDataManager` | Does **not** cover specification properties (PY-12, docs-only) |
| Valid metadata values for a property name | `ReferenceDataManager` or `MetadataExpert` | `get_valid_metadata_values` lives on shared `ServerClient` base; no `as_of_time` support — Egeria endpoint doesn't expose it |
| Specification properties (placeholders, guards, action targets, etc.) | `ValidMetadataManager.find_specification_property` (inherited by `SpecificationProperties`) | Avoid `get_specification_property_by_type` (PY-13, open Egeria server bug); use `find_specification_property` with `graph_query_depth=0` (PY-14, expected Egeria behavior, not a bug — cost is incurred by the traversal attempt itself, not by how much comes back) |
| `DataGrain` / `DataClass` listing | `find_data_value_specifications(search_string="*")` | Fixed (PY-1) — safe to call directly now. Do **not** use `get_data_value_specifications_by_name("*")` for listing — by design a complete-match lookup, not search (PY-2, not a bug) |
| `DataSpec` (Collection subtype) | `CollectionManager.find_collections(metadata_element_type="DataSpec")` | |
| `DataStructure` / `DataField` | `DataDesigner.find_data_structures` / `find_data_fields` | |
| Solution blueprints/components (any pyegeria version) | `SolutionArchitect.find_solution_blueprints/components(search_string="*")` | Avoid `find_all_*` variants (PY-3) |
| Note logs (list) | `find_note_logs("*", graph_query_depth=0)` | PY-6 |
| Multi-classification search (`matchClassifications`, 2+ conditions) | `MetadataExpert.find_metadata_elements` | Fixed in Egeria (PY-15) — re-verify once the fixed server is deployed here |
| Paging a large `find_metadata_elements` result (`start_from`/`page_size`) | Don't rely on it | Egeria server ignores both regardless of pyegeria version (PY-23, open) — dedupe by GUID client-side while accumulating pages instead |
| Peer-duplicate linking | `ClassificationExplorer.link_elements_as_peer_duplicates` | Fixed in pyegeria 6.0.16.20 (PY-16) — safe to call directly now |
| Relationships for a single element by guid | `MetadataExpert.get_all_related_elements(guid)` | **Not** `get_metadata_element_by_guid` — that call never returns relationships, by design (PY-17, not a bug) |
| Note logs (entries) | `get_notes_for_note_log(guid, page_size=100)` | PY-5 — never pass `metadata_element_type_name="NoteLog"` |
