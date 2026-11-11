<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# A saved query's last answer on a Dashboard Sheet (Route B)

> Loadable **Dr.Egeria** document. It seeds the saved query **Assets with no lineage** and its Results Set
> under fixed qualified names, the Egeria-held report spec **Saved Query Result**, and a tile on the
> `catalog-health` sheet (made by `LOCAL_DASHBOARDS_USEFUL_SHEETS.dr-egeria.md`) that shows how many assets the
> query found at its last refresh.
>
> **Route B (owner, 2026-11-11).** The tile runs pyegeria's registered analytic function `saved_query`
> (pyegeria 6.2.34 or later) with `name` = the SavedQuery's qualified name, `mode: cached`, `output: count`. It reads
> the Results Set the last refresh filled and says "as of" that refresh. **Until the first refresh it says the
> answer was not read (never refreshed), not "0".** Route A (listing the Results Set's members with a
> `get_collection_members` spec) showed an unrefreshed query as an empty answer, which read as "no assets
> without lineage".
>
> **Count, not list.** `output: list` also works in pyegeria, but the Portal's tile shows an analytic result as a
> one-row table of its first eight keys, and the elements are not among them. A list tile needs a Portal change.
>
> **Needs the Portal refresh change of odpi/egeria-workspaces#823** (merged 2026-11-11): the refresh finds the
> Results Set through the `SmartQuery` link, reads the search from `additionalProperties.searchSpec`, and stamps
> `resultsSetGuid`, `lastRefreshedTime` and `lastRefreshParams` on the SavedQuery, which `saved_query` reads.
> This file runs after the sheets file in the "Useful Dashboards" batch.
>
> **What the query is.** The Query tool's search for assets with no `DataFlow` relationship, leaving out
> `Notification` and `Action` (worked example S3). `type_name` is declared as a parameter (default `Asset`);
> a cached answer stands only for the values its refresh recorded, so the tile (which gives no `params`) shows
> the answer of a refresh made with the default.
>
> **The first refresh is a shared Egeria write:** the Query tool's Saved Queries tab, **Refresh**, or
> `POST /api/insights/queries/{guid}/refresh`. "Keep live" does not apply: a relationship condition cannot be run
> by the Smart Collections connector, so nothing re-runs it; the tile shows the last refresh until the next one.
>
> **The spec is filed with `Add Member to Collection`**, not `Parent ID` (the Update hazard), in
> `ReportSpecFolder::Consumer::Portal`, which the Portal syncs. Egeria Advisor takes specs from
> `ReportSpecFolder::Consumer::EgeriaAdvisor`, where this one is not filed.
>
> **This is a shared Egeria write.** Run `--validate` first, `--process` once under the peer check.
> **Undo:** delete the placement, the Report, the spec, the Results Set and the SavedQuery, by GUID, as the
> seeding user.

___

## Create Saved Query
### Display Name
Assets with no lineage

### Qualified Name
SavedQuery::useful-sheets::Assets with no lineage

### Description
Assets with no DataFlow relationship, leaving out notifications and actions. The Query tool's search; refresh it to update the answer.

### Additional Properties
pyegeriaInsightsQuery: true
searchSpec: {"type_name": "Asset", "relationship_conditions": [{"relationship_type": "DataFlow", "presence": "lacks"}], "exclude_types": ["Notification", "Action"]}
parameters: [{"name": "type_name", "type": "string", "default": "Asset"}]

___

## Create Results Set
### Display Name
Assets with no lineage (results)

### Qualified Name
ResultsSet::useful-sheets::Assets with no lineage

### Description
The last refreshed answer of the saved query "Assets with no lineage".

___

## Link Saved Query to Results Set
### Saved Query
SavedQuery::useful-sheets::Assets with no lineage

### Results Set
ResultsSet::useful-sheets::Assets with no lineage

___

## Create Report Spec
### Display Name
Saved Query Result

### Qualified Name
ReportSpec::Saved Query Result

### Description
The answer of a saved query named by its qualified name, through pyegeria's analytic function saved_query: a count as of its last refresh (mode cached), or never refreshed. Params: name (required), mode (cached or live), output (count or list), params (values for its declared parameters).

### Purpose
Saved query answer, as of its last refresh

### Category
Saved Queries

### Content Status
ACTIVE

### Output Types
DICT, JSON

### Microflow
{"format":"microflow/1","params":{"name":{"type":"string","required":true},"mode":{"type":"string"},"output":{"type":"string"},"params":{"type":"object"}},"stages":[{"stage":"producer/analytic","function":"saved_query","params":{"mode":"cached","output":"count"}}],"formatters":{"DICT":{"columns":["display"]},"JSON":{"same_as":"DICT"}}}

___

## Add Member to Collection
> File the spec in the Portal's report-spec folder (no Parent ID: see the header).

### Collection Id
ReportSpecFolder::Consumer::Portal

### Element Id
ReportSpec::Saved Query Result

### Membership Status
VALIDATED

### Membership Rationale
Report spec used by a seeded Portal tile.

___

## Create Report
### Display Name
Catalog Health - Assets with No Lineage

### Description
How many assets have no DataFlow relationship, as of the last refresh of the saved query "Assets with no lineage" (Query tool, Saved Queries tab). The tile does not re-run the query; before the first refresh it says the answer was not read.

### Report Spec
Saved Query Result

### Output Format
DICT

### Analytic Parameters
name : SavedQuery::useful-sheets::Assets with no lineage
mode : cached
output : count

___

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Report Name
Catalog Health - Assets with No Lineage

### Placement Span
full

### Placement Emphasis
panel

___
