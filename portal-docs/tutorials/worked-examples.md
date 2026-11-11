<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Worked Examples: Report Specs, Analytic Functions, Saved Queries and Dashboards

This page is a set of complete examples, each of a different kind. Every example gives the exact input,
the steps or command, and the output you should see. They use the Coco Pharmaceuticals demo data and the
sheets, Reports and specs that already exist on the quickstart.

The concepts are explained in the tutorials; this page is for trying things out:

- [Report Specs: Local and Held in Egeria](report-specs.md)
- [Add and Use Analytic Functions](analytic-functions.md)
- [Create and Use Saved Queries](saved-queries.md)
- [Building a Local Dashboard](local-dashboards.md)

> **How these were checked.** On 2026-11-10, against the quickstart (Portal at commit 81d6e636, pyegeria
> 6.2.32), without writing anything to Egeria. Each example carries one of these labels:
>
> - **Ran:** the output shown is what the Portal returned (its read APIs, or a run of a report spec, which
>   only reads from Egeria).
> - **Validated:** the Dr.Egeria document passed `dr_egeria --validate`, which makes no changes. Running it
>   with `--process` creates new Egeria elements, so the output shown is what to expect, not what was seen.
>   These examples are listed for the owner at the end of this page.
> - **Not verified:** written from the code; not run.
>
> Counts change as the demo data changes, so your numbers may differ.

**Running a report spec from the command line.** Several examples run a spec through the Portal's own
API. The request only reads from Egeria:

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute \
  -H 'Content-Type: application/json' \
  -d '{"spec_name": "<spec name>", "output_format": "DICT", "params": {<parameters>}}'
```

The same run is available in the Portal: **Egeria Explorer → Reports → Report Specs**, pick the spec, fill
in the parameters in the **Run Report** panel, and click **Run**.

**A warning you can ignore.** Every `Create Report` shown here validates with the warning
*Value '['ACTIVE']' is not a valid metadata value for 'Limit Result by Status'*. pyegeria 6.2.32 adds that
value itself, the quickstart's live Reports carry it, and they run.

---

## Report specs

### R1. A simple list spec (built-in, find)

*Ran.* A built-in spec that lists glossary terms matching a search string.

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute -H 'Content-Type: application/json' \
  -d '{"spec_name": "Help-Terms", "output_format": "TABLE", "params": {"search_string": "Patient"}}'
```

Output: 12 rows with the columns *Term Name, Description, Usage, Update Time*: Reported, Patient,
Patient Date of Birth, Patient Identifier, Patient Weight, Patient Blood Pressure, Patient Height,
and second copies of five of them (one copy of each says *Only for use in templates*). The search matches more
than the name, which is why *Reported* is there.

### R2. A parameterised spec (a required parameter that picks one element)

*Ran.* `Collection Members` lists the members of one collection, named by its GUID. Here the collection is
the Portal's report-spec folder, `ReportSpecFolder::Consumer::Portal`.

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute -H 'Content-Type: application/json' \
  -d '{"spec_name": "Collection Members", "output_format": "TABLE",
       "params": {"collection_guid": "fe5aad27-1587-4d4e-a7c0-ab806650a6e2"}}'
```

Output: 2 rows, *Resource Explorer - Curation Coverage* and *Analytic - Generic Metric Trend*, each with
*Qualified Name* `ReportSpec::…`, *Type Name* `ReportSpec` and *Created By* `erinoverview`.

To put this on a dashboard you need a Report that stores the parameter. *Validated:*

```markdown
## Create Report
### Display Name
Portal Report Specs Held in Egeria

### Description
The report specs in the Portal's consumer folder.

### Report Spec
Collection Members

### Output Format
TABLE

### Report Parameters
collection_guid : fe5aad27-1587-4d4e-a7c0-ab806650a6e2
```

### R3. An analytic spec: a count, and a trend held in Egeria

*Ran.* The built-in count spec, pointed at a type with a parameter:

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute -H 'Content-Type: application/json' \
  -d '{"spec_name": "Analytic Demo - Element Count by Type", "output_format": "DICT", "params": {"type_name": "GlossaryTerm"}}'
```

Output: `{"kind": "json", "data": 1065, …}` with `"specSource": {"source": "builtin", "sourceLabel": "pyegeria built-in", …}`.

*Ran.* The trend spec is held in Egeria. The `egeria:` prefix asks for the Egeria copy by name:

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute -H 'Content-Type: application/json' \
  -d '{"spec_name": "egeria:Analytic - Generic Metric Trend", "output_format": "DICT",
       "params": {"window": "90d", "points": 3, "metric_path": "count_elements",
                  "metric_params": {"type_name": "GlossaryTerm"}}}'
```

Output: three points, `12 Aug 2026: 200`, `26 Sep 2026: 200`, `10 Nov 2026: 1065`, and
`"spec_source": {"tier": "egeria", "version": "1.0", "guid": "7e6b0cd2-…", "synced_at": "2026-11-10T20:13:46Z"}`.
(The two earlier points both read exactly 200. That may be a limit in counting at a past time rather than
the real number; it has been reported for checking.)

### R4. A local spec in a user spec file

*Ran in a throwaway Python process in the Jupyter container (registration only).* Save this as
`~/.pyegeria/report_specs/my_specs.json` (or any folder named by `PYEGERIA_USER_REPORT_SPECS_DIR`):

```json
{
  "Demo - Terms by Name": {
    "target_type": "GlossaryTerm",
    "heading": "Terms by name",
    "description": "Glossary terms whose name contains a word.",
    "family": "Demo",
    "formats": [{"types": ["TABLE", "DICT"], "attributes": [
      {"name": "Display Name", "key": "display_name"},
      {"name": "Qualified Name", "key": "qualified_name"}]}],
    "action": {"function": "GlossaryManager.find_glossary_terms", "required_params": ["search_string"]}
  }
}
```

Then, in Python:

```python
from pyegeria.view.base_report_formats import report_spec_source
report_spec_source("Demo - Terms by Name")
```

Output: `{'tier': 'local', 'label': 'Demo - Terms by Name', 'version': None}`. If the file also defines a
spec named `Collections`, `report_spec_source("Collections")` says `local`, and
`report_spec_source("builtin:Collections")` still says `builtin`.

### R5. A list spec held in Egeria, published to the Portal

*Validated.* The same list as R4, as a `ReportSpec` element filed in the Portal's folder. The `Microflow`
was checked separately: it parses, passes pyegeria's allowlist for Egeria-held specs, and converts back to
a spec with the `search_string` parameter and three columns.

```markdown
## Create Report Spec
### Display Name
Tutorial Demo - Terms by Name

### Qualified Name
ReportSpec::Tutorial Demo - Terms by Name

### Description
Glossary terms whose name, description or other searchable text matches a search string.

### Purpose
Terms by name

### Category
Tutorial

### Content Status
ACTIVE

### Target Type Name
GlossaryTerm

### Output Types
TABLE, DICT

### Microflow
{"format":"microflow/1","params":{"search_string":{"type":"string","required":true}},"stages":[{"stage":"producer/find","type":"GlossaryTerm","function":"GlossaryManager.find_glossary_terms","params":{"search_string":"$search_string"}}],"formatters":{"TABLE":{"columns":[{"field":"display_name","label":"Term Name"},{"field":"qualified_name","label":"Qualified Name"},{"field":"description","label":"Description"}]},"DICT":{"same_as":"TABLE"}}}

### Parent ID
ReportSpecFolder::Consumer::Portal
```

Expected after `--process` and a sync (**⇣ Sync from Egeria**): the Report Specs banner says
*3 report specs held in Egeria*, and the spec shows the **held in Egeria** badge. Running it with
`search_string` `Patient` gives the same terms as R1, with these three columns.

---

## Analytic functions

### A1. A generic function, used with no code

*Ran.* The quickstart's *Term Count* Report (from
`exchange-quickstart/loading-bay/dr-egeria-inbox/Local Dashboards/LOCAL_DASHBOARDS_ANALYTICS_DEMO.dr-egeria.md`):

```markdown
## Create Report
### Display Name
Term Count

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm
```

On the `local-dashboards-next-steps` sheet this tile shows **1065**. The same spec counts 100 projects
(`type_name: Project`), 39 locations (`Location`) and 62087 assets (`Asset`).

### A2. A fixed-metric function (no parameters)

*Ran.* What it measures is built into the function, so the Report needs no `Analytic Parameters`.

| Spec | Output |
|---|---|
| `Analytic Demo - Term Definition Completeness` | `{"total": 1065, "defined": 540, "undefinedPct": 49}` |
| `Analytic Demo - Ownership Coverage` | `{"ownershipCount": 428, "ownershipCapped": false, "byOwnerType": {"UserIdentity": 6, "Unspecified": 411, "SolutionActorRole": 11}}` |

Both are tiles on the *Chief Data Officer Dashboard*.

### A3. A function that takes a list parameter (a breakdown for a chart)

*Ran.* `Analytic Demo - Assets by Type Breakdown` counts several types at once. The pie and bar tiles on
*Assets by Type and Location Demo* use:

```markdown
### Analytic Parameters
type_map: [["Data Stores", "DataStore"], ["Data Sets", "DataSet"], ["Software Components", "DeployedSoftwareComponent"], ["Infrastructure", "ITInfrastructure"], ["APIs", "DeployedAPI"], ["Processes", "Process"]]
```

Output (DICT): Data Stores 1735, Data Sets 1915, Software Components 587, Infrastructure 75, APIs 5,
Processes 58297. With `Output Format` `PIE` or `BAR` the same numbers are drawn as a chart.

### A4. A function that wraps another one (a trend)

*Ran.* `metric_trend` runs any registered function at several past times. The *Subscription Growth Trend*
tile on `digital-product-portfolio`:

```markdown
### Report Spec
Analytic - Generic Metric Trend
### Output Format
SERIES
### Analytic Parameters
window: 180d
points: 6
metric_path: count_elements
metric_params: {"type_name": "Agreement"}
```

Output: six monthly points from May to November 2026: 0, 0, 0, 0, 0, then **886** (the agreements were
loaded after the October reset), drawn as a line chart.

### A5. Your own function, registered in Python or a notebook

*Ran end to end, in a throwaway Python process in the Portal's container. That container was used because
it can sign in to Egeria; the quickstart Jupyter container has no Egeria sign-in set up. The registration
alone was also run in the Jupyter container.*

```python
# my_analytics.py
def count_my_terms(client, contains: str = "Patient") -> int:
    """Count glossary terms whose name contains a word."""
    terms = client.find_glossary_terms(contains, output_format="DICT") or []
    return len(terms) if isinstance(terms, list) else 0
```

```python
from pyegeria.view.analytic_registry import register_analytic_functions
from pyegeria.view._output_format_models import ActionParameter, Format, FormatSet, FormatSetDict
from pyegeria.view.base_report_formats import register_report_specs
from pyegeria.view.format_set_executor import exec_report_spec

register_analytic_functions({"count_my_terms": {
    "name": "count_my_terms", "function": "my_analytics.count_my_terms",
    "inputs": ["egeria_client:EgeriaTech"], "description": "Count glossary terms by name.",
    "returns": "scalar (int)",
    "params": [{"name": "contains", "type": "str", "default": "Patient", "description": "word"}]}})

register_report_specs(FormatSetDict({"Tutorial - My Term Count": FormatSet(
    heading="My term count", description="Count glossary terms by name.", family="Tutorial",
    target_type=None, formats=[Format(types=["DICT", "JSON"], attributes=[])],
    action=ActionParameter(function="", analytic_function="count_my_terms",
                           analytic_spec_params={"contains": "Patient"}))}), source="tutorial")

exec_report_spec("Tutorial - My Term Count", output_format="DICT")                              # 12
exec_report_spec("Tutorial - My Term Count", output_format="DICT", params={"contains": "Hospital"})  # 1
```

Output: `data` 12, then 1, each with `spec_source` `{'tier': 'local', …}`. Pass `view_server`,
`view_url`, `user` and `user_pass` to `exec_report_spec` if your pyegeria configuration does not set them.

### A6. The same function from a config file

*Ran, as A5.* Put the registry entry in a JSON file:

```json
{"count_my_terms_json": {"name": "count_my_terms_json", "function": "my_analytics.count_my_terms",
  "inputs": ["egeria_client:EgeriaTech"], "description": "Count glossary terms by name.", "returns": "scalar (int)"}}
```

Set `PYEGERIA_ANALYTIC_FUNCTIONS_JSON=/path/to/my_functions.json`, and **call
`refresh_analytic_functions()`** before using it (without the call the function is not registered). A spec
naming `count_my_terms_json` then returns 12, as in A5.

### A7. The same function as an installed package

*Registration ran in a throwaway virtual environment in the Jupyter container; the function was not run.*
Use the `pyproject.toml` and `manifest.py` from
[Add and Use Analytic Functions, Step 4](analytic-functions.md#step-4-register-it), then
`pip install ./my-analytics-pkg`. In a new Python process:

```python
from pyegeria.view.analytic_registry import get_analytic_registry, analytic_entry_point_errors
"count_my_terms" in get_analytic_registry(), analytic_entry_point_errors()
```

Output: `(True, {})`.

### A8. In the quickstart Portal, freshstart and Egeria Advisor

*Not verified* (each needs an image rebuild or a restart of a shared service). Install the A7 package
into the environment and restart it:

| Environment | Where the package goes | How to check it arrived |
|---|---|---|
| Quickstart Portal | `compose-configs/egeria-quickstart/PyegeriaWebHandler/requirements.txt`, then rebuild the `pyegeria-web` image | **Egeria Explorer → Reports → Analytic Functions** lists `count_my_terms` (30 functions instead of 29) |
| Freshstart | `compose-configs/egeria-freshstart/PyegeriaWebHandler/requirements.txt`, then rebuild | Run a spec naming it from Egeria Explorer's Report Specs view; freshstart has no Analytic Functions view |
| Egeria Advisor | Egeria Advisor's Python environment (a trellis dependency, then `uv sync`), then restart it | A report spec naming it runs in Egeria Advisor |

Then give that environment a report spec naming `count_my_terms` (a user spec file as in R4, or a spec
held in Egeria as in R5, in that tool's consumer folder).

---

## Saved queries

The Query tool (`/egeria-insights`) is quickstart only. Its **Run query** button calls
`POST /api/insights/search`, which only reads. These examples show the conditions to set in the Query tab
and the same search from the command line. Saving and refreshing write to Egeria, so they are not shown
running here; the full save-refresh-dashboard loop is in [Create and Use Saved Queries](saved-queries.md).

### S1. A property value

*Ran.* Query tab: **Element type** `GlossaryTerm`; **+ Add property value**: `displayName` **contains** `Patient`.

```bash
curl -sk -X POST https://localhost:8843/api/insights/search -H 'Content-Type: application/json' \
  -d '{"type_name": "GlossaryTerm", "value_conditions": [{"property": "displayName", "operator": "LIKE", "value": "Patient"}]}'
```

Output: `"total": 11`: Patient, and two copies each of Patient Blood Pressure, Date of Birth, Height,
Identifier and Weight. (R1's spec search also matched *Reported*; this one looks at the name only.)

### S2. A classification

*Ran.* Query tab: **Element type** `Asset`; **+ Add condition**: `Confidentiality`.

```bash
curl -sk -X POST https://localhost:8843/api/insights/search -H 'Content-Type: application/json' \
  -d '{"type_name": "Asset", "conditions": [{"classification": "Confidentiality"}]}'
```

Output: `"total": 11`, all `CSVFile` templates for the hospitals' weekly clinical-trial measurements,
such as *~{fileName}~ from Bowden Arrow Hospital*, each classified by steward `tanyatidie`.

### S3. A missing relationship ("which assets have no lineage?")

*Ran.* Query tab: **Element type** `Asset`; **+ Add relationship**: `DataFlow` **lacks**;
**Exclude types**: `Notification, Action`.

```bash
curl -sk -X POST https://localhost:8843/api/insights/search -H 'Content-Type: application/json' \
  -d '{"type_name": "Asset", "relationship_conditions": [{"relationship_type": "DataFlow", "presence": "lacks"}],
       "exclude_types": ["Notification", "Action"]}'
```

Output: `"total": 18, "capped": true`, with two notes: the relationship condition was applied to a capped
page of fetched assets, not to every asset, and 182 of the 200 fetched were excluded by type. Tick
**Exact count** for a complete answer. A query like this one, with only a relationship condition, cannot
use **Keep live**; refresh it by hand.

### S4. A saved query written with Dr.Egeria

*Validated.* The query from S2 as a `SavedQuery`, with a results set to hold its answer:

```markdown
## Create Saved Query
### Display Name
Confidential Assets

### Description
Assets that carry the Confidentiality classification.

### Query URL
/servers/qs-view-server/api/open-metadata/metadata-expert/metadata-elements/by-search-specification

### Query Request Body
{"class": "FindRequestBody", "metadataElementTypeName": "Asset", "limitResultsByStatus": ["ACTIVE"], "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ALL", "conditions": [{"name": "Confidentiality"}]}}

___

## Create Results Set
### Display Name
Confidential Assets Results

### Description
The answer to the Confidential Assets saved query.

___

## Link Saved Query to Results Set
### Saved Query
Confidential Assets

### Results Set
Confidential Assets Results
```

Expected after `--process`: three new elements linked by `SmartQuery`. The results set stays empty until
something fills it, and the Query tool's Saved Queries tab does not manage this query (see
[Authoring with Dr.Egeria](saved-queries.md#authoring-with-dregeria-instead-of-the-ui)).

---

## Dashboards

### D1. A sheet of analytic tiles and a text panel (live)

*Ran.* *Assets by Type and Location Demo*, from
`exchange-quickstart/loading-bay/dr-egeria-inbox/Local Dashboards/LOCAL_DASHBOARDS_ASSETS_BY_TYPE_LOCATION_DEMO.dr-egeria.md`.
Open `https://localhost:8843/local-dashboards?sheet=Assets%20by%20Type%20and%20Location%20Demo`, or read it:

```bash
curl -sk "https://localhost:8843/api/local-dashboards/Assets%20by%20Type%20and%20Location%20Demo"
```

Output: `"source": "egeria"` and five placements:

| Placement | Kind | Spec | Shows |
|---|---|---|---|
| Total Cataloged Assets | report, KPI | Element Count by Type (`Asset`) | 62087 |
| Total Locations Tracked | report, KPI | Element Count by Type (`Location`) | 39 |
| Assets by Type (Pie Chart) | report, panel | Assets by Type Breakdown, `PIE` | the six counts in A3 |
| Assets by Type (Bar Chart) | report, panel | the same, `BAR` | the same counts |
| Assets by Location Snapshot | text, full width | (none) | a caption and a mermaid pie chart written by hand |

The text panel is a snapshot: it says *37 locations are tracked*, while the live tile now says 39. Text
placements never re-query; use a Report for anything that should stay current.

### D2. A sheet that mixes text, reports and a restricted tile

*Validated.* This one document creates two Reports and a sheet with a text caption, an existing Report
(*Term Count*, from A1), a trend and a Report in the `clinical-trials` zone. Reports and the sheet are
linked within the same document, so they can be validated together.

```markdown
## Create Report
### Display Name
Glossary Growth - Last Ninety Days

### Description
How the number of glossary terms changed over the last ninety days.

### Report Spec
Analytic - Generic Metric Trend

### Output Format
SERIES

### Analytic Parameters
window: 90d
points: 3
metric_path: count_elements
metric_params: {"type_name": "GlossaryTerm"}

___

## Create Report
### Display Name
Clinical Trial Term Count

### Description
Glossary term count, visible only to people who can see the clinical-trials zone.

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm

### Zone Membership
clinical-trials

___

## Create Dashboard Sheet
### Display Name
tutorial-mixed-sheet

### Dashboard Sheet Heading
Glossary at a glance

### Dashboard Sheet Description
A text caption, a public count, a trend and a zoned count on one sheet.

### Dashboard Sheet Family
dashboard

___

## Add Text on Dashboard Sheet
### Dashboard Sheet Name
tutorial-mixed-sheet

### Placement Name
Introduction

### MD Content
#### Glossary at a glance
The first tile counts every glossary term. The second shows the trend. The last one is only visible to people who can see the *clinical-trials* zone.

### Placement Span
full

### Placement Emphasis
panel

___

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
tutorial-mixed-sheet

### Report Name
Term Count

### Placement Span
1

### Placement Emphasis
kpi

___

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
tutorial-mixed-sheet

### Report Name
Glossary Growth - Last Ninety Days

### Placement Span
2

### Placement Emphasis
panel

___

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
tutorial-mixed-sheet

### Report Name
Clinical Trial Term Count

### Placement Span
1

### Placement Emphasis
kpi
```

Expected after `--process`: a sheet with four tiles: the caption; *Term Count* (1065); the trend (as in
R3); and *Clinical Trial Term Count*. Someone who can see the `clinical-trials` zone sees 1065 there;
anyone else sees a dashed tile, 🔒 *Report not visible to you.*

What a restricted tile looks like today *(ran)*: the quickstart's `scratch-restricted-demo` sheet has
one public Report and one zoned Report.

```bash
curl -sk "https://localhost:8843/api/local-dashboards/scratch-restricted-demo"
```

Output for the Portal's service user: placement 1 `"kind": "report"` (*Project Count*); placement 2
`"kind": "restricted"`, `"restrictedElement": "Report"`, `"reason": "not visible to you"`,
`"description": "Report not visible to you."`

### D3. Perspectives and a drill-down

*Ran.* The *Chief Data Officer Dashboard* tags placements with perspectives. The page's perspective
selector (or `?perspective=` on the API) keeps the placements for that perspective, plus every placement
with no perspective:

```bash
curl -sk "https://localhost:8843/api/local-dashboards/Chief%20Data%20Officer%20Dashboard?perspective=steward"
```

Output: all 22 placements with no perspective chosen, 15 for `steward`, 11 for `engineer`. The *Governance Metrics
Defined* tile (`Placement Perspectives: governance`) has `Placement Detail Spec`
`Governance-Metric-DrE-Basic`, so the tile has a **↗** button that runs that spec in a side drawer: the list of
metrics behind the count.

### D4. A sheet only in the local file

*Validated, with `--local-only`.* Running the D2 document with `dr_egeria --local-only` writes the
sheet and its placements only to the local file (`PYEGERIA_DASHBOARD_SHEETS_STORE`). The Reports are
still Egeria elements, so `Create Report` still writes to Egeria. In the Portal the sheet would carry the
tag **local file**, and the Portal's Delete button works for it (sign-in needed). On the quickstart the
local file is empty today: all six sheets are held in Egeria.

### D5. Diagnosing a broken tile

*Ran.* The *Tasks* tile on `local-dashboards-next-steps` runs `Collection Members` with a
`collection_guid` written into its `Create Report`. Running the same thing by hand:

```bash
curl -sk -X POST https://localhost:8843/api/report-specs/execute -H 'Content-Type: application/json' \
  -d '{"spec_name": "Collection Members", "output_format": "TABLE",
       "params": {"collection_guid": "0affb580-fa81-4d00-9438-b26faf11845d"}}'
```

Output: an error, `CLIENT_ERROR_400` from `…/collection-manager/collections/0affb580-…/members`. The
collection with that GUID is no longer in Egeria (GUIDs change when the demo data is reloaded), so the
tile cannot show anything. The fix is to re-run the Report's `Create Report` with the collection's
current GUID. A Report that names its target by GUID breaks this way; one that uses a `Search String`
does not.

---

## For the owner: examples that need new Egeria elements

These were validated only. Running them with `--process` is a shared write on the quickstart Egeria:

| Example | Creates |
|---|---|
| R2 | Report *Portal Report Specs Held in Egeria* |
| R5 | ReportSpec *Tutorial Demo - Terms by Name*, filed in `ReportSpecFolder::Consumer::Portal` |
| S4 | SavedQuery *Confidential Assets*, ResultsSet *Confidential Assets Results*, and the link |
| D2 | Reports *Glossary Growth - Last Ninety Days* and *Clinical Trial Term Count* (zone `clinical-trials`), sheet `tutorial-mixed-sheet` and its four placements |
| A8 | No Egeria element, but a Portal image rebuild with a new package |

Found while writing these examples, for checking:

- D5: the *Tasks* tile on `local-dashboards-next-steps` fails, because its collection GUID is gone.
  `LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md` also gives that Report two `Output Format`
  sections (`MERMAID`, then `TABLE`); the live Report has `TABLE`.
- R3: the two earlier points of the GlossaryTerm trend read exactly 200.
- D1: the hand-written location snapshot says 37 locations; the live count is 39.
