<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# A saved query's last answer on a Dashboard Sheet (Route A)

> Loadable **Dr.Egeria** document. It shows the last answer of the Portal-saved query **Assets with no
> lineage** on the `catalog-health` sheet (made by `LOCAL_DASHBOARDS_USEFUL_SHEETS.dr-egeria.md`).
>
> **Not in the heal batch.** The Portal names a saved query's Results Set
> `ResultsSet::insights-query::<query name>::<8 random hex>`, so its qualified name is known only after the
> query is saved, and it changes if the query is saved again (for example after a platform reset). This file
> therefore stays out of `_batch.json`: after each save, put the Results Set's qualified name below, then
> validate and run it once.
>
> **Before running it:**
> 1. In the Portal's Query tool, build the query: **Element type** `Asset`; **+ Add relationship** `DataFlow`
>    **lacks**; **Exclude types** `Notification, Action`. Save it as `Assets with no lineage` (leave
>    **Keep live** off: a relationship-only query cannot be kept live), then click **Refresh**.
> 2. Read its Results Set's qualified name: `GET /api/insights/queries` gives each query's
>    `resultsSetGuid`; the Results Set element's `qualifiedName` is what goes below. Replace
>    `<ResultsSet qualifiedName>`.
>
> **Why a spec of its own.** pyegeria's built-in `Collection Members` spec requires `collection_guid` and
> forwards no other way to name the collection, and a Report must never pin a GUID. `Saved Query Answer`
> is the same call (`CollectionManager.get_collection_members`) with the collection named by qualified name.
> It is held in Egeria, in the Portal's consumer folder, so the Portal picks it up at its next sync.
>
> **"As of".** The refresh time is stamped on the SavedQuery (`additionalProperties.lastRefreshedTime`),
> not on the Results Set, so this tile shows the members only; its description says it is the last
> refreshed answer. **TODO (live check):** a second tile that shows the SavedQuery's `lastRefreshedTime`.
>
> **This is a shared Egeria write.** Run `--validate` first, `--process` once under the peer check.
> **Undo:** remove the placement (re-run the sheet file without it, or `python -m pyegeria.view.dashboards`);
> the Report and spec can be deleted by GUID if asked.

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
collection_qname : <ResultsSet qualifiedName>

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
