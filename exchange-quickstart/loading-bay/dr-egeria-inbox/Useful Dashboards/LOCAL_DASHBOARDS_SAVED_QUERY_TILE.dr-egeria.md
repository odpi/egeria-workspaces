<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# A saved query's last answer on a Dashboard Sheet (Route A)

> Loadable **Dr.Egeria** document. It seeds the saved query **Assets with no lineage** and its Results Set
> under fixed qualified names, an Egeria-held report spec that lists a collection named by qualified name,
> and a tile on the `catalog-health` sheet (made by `LOCAL_DASHBOARDS_USEFUL_SHEETS.dr-egeria.md`) that
> shows the query's last refreshed answer.
>
> **Depends on a Portal change that has not merged yet**
> (`~/.re-gate/BRIEF-PORTAL-SAVED-QUERY-SEEDABLE-2026-11-10.md`). Until it does, the Portal's
> `POST /api/insights/queries/{guid}/refresh` refuses this query: it wants `additionalProperties.resultsSetGuid`
> (a GUID) and a `formula`. After the change it finds the Results Set through the `SmartQuery` link and reads the
> search from `additionalProperties.searchSpec`. **So this file stays in `_batch.json`'s `exclude` list until that
> change merges**; then move it into `files`, after the sheets file.
>
> **What the query is.** The Query tool's search for assets with no `DataFlow` relationship, leaving out
> `Notification` and `Action` (worked example S3). `type_name` is declared as a parameter, so a refresh may
> override it (for example `DataSet`) and nothing else; the refresh records the value it ran with
> (`lastRefreshParams`).
>
> **Not refreshed until someone refreshes it.** Seeding leaves the Results Set empty. The first refresh is the
> Coordinator's (an Egeria write): the Query tool's Saved Queries tab, **Refresh**, or
> `POST /api/insights/queries/{guid}/refresh`. Until then the tile shows no rows. "Keep live" does not apply:
> a relationship condition cannot be run by the Smart Collections connector. Because it is not registered as
> a Smart Collection, nothing re-runs it with its stored values, so a refresh with another `type_name` keeps that
> answer until the next refresh. (A query registered as a Smart Collection is re-run about every 30 minutes with
> its stored values, which overwrites a refresh made with other values.)
>
> **"As of".** The refresh time is stamped on the SavedQuery (`lastRefreshedTime`, and after the Portal change
> `lastRefreshParams`), not on the Results Set. **TODO:** the "Saved Query Status" tile (name, refresh time,
> result count, parameter values, "never refreshed" when the time is missing). Its spec is written once a seeded,
> refreshed query exists to check which fields a find returns.
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
Saved Query Answer

### Qualified Name
ReportSpec::Saved Query Answer

### Description
The members of a collection named by its qualified name: for a saved query, the Results Set that holds its last refreshed answer.

### Purpose
Saved query answer

### Category
Saved Queries

### Content Status
ACTIVE

### Output Types
TABLE, DICT

### Microflow
{"format":"microflow/1","params":{"collection_qname":{"type":"string","required":true}},"stages":[{"stage":"producer/find","type":"Collection","function":"CollectionManager.get_collection_members","params":{"collection_qname":"$collection_qname"}}],"formatters":{"TABLE":{"columns":[{"field":"display_name","label":"Name"},{"field":"type_name","label":"Type"},{"field":"qualified_name","label":"Qualified Name"}]},"DICT":{"same_as":"TABLE"}}}

### Parent ID
ReportSpecFolder::Consumer::Portal

___

## Create Report
### Display Name
Catalog Health - Assets with No Lineage

### Description
Assets with no DataFlow relationship, as of the last refresh of the saved query "Assets with no lineage" (Query tool, Saved Queries tab). The tile does not re-run the query.

### Report Spec
Saved Query Answer

### Output Format
TABLE

### Report Parameters
collection_qname : ResultsSet::useful-sheets::Assets with no lineage

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
