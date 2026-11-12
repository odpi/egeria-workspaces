<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Fix-up: switch the "Assets with No Lineage" tile to Route B (one run, 2026-11-11)

> Loadable **Dr.Egeria** document, **for one run on a platform seeded with the Route A tile** (laz,
> 2026-11-11). It creates the report spec **Saved Query Result** (pyegeria's `saved_query`, cached, count), files it
> in `ReportSpecFolder::Consumer::Portal` with `Add Member to Collection`, and **updates the existing Report**
> "Catalog Health - Assets with No Lineage" in place to run that spec with Analytic Parameters `name`, `mode`,
> `output` and Output Format DICT. The Report is named by its own qualified name, so this is an Update of that
> element; there is no `Parent ID` anywhere. Updating the Report re-links its `ReportTypeInstance` to the new spec
> and detaches the old one ("Saved Query Answer").
>
> **Not touched:** the placement on `catalog-health` (same Report, same span and emphasis), the sheet, the
> SavedQuery, the Results Set and their link, and the Route A spec "Saved Query Answer" (left in place; nothing
> seeded uses it now). The Report's old flat `collectionQname` key may stay in its additionalProperties: an
> analytic tile is run with its `analyticParams` only, so it is not read.
>
> **After it runs:** the Portal must load the new spec from its folder (`POST /api/report-specs/sync`, or its
> periodic sync), then the tile says "not read: never refreshed" until the first refresh of the saved query.
>
> **Not in any batch** (`_batch.json` lists it under `exclude`). Shared Egeria write: `--validate` first, then
> `--process` **ONCE** under the peer check. Do not re-run it: the spec and the Report would be updated in place,
> but `Add Member to Collection` does not dedupe, so a second run adds a second folder membership.

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

### Qualified Name
Coco Pharmaceuticals::DeployedReport::Catalog-Health---Assets-with-No-Lineage::1.0

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
