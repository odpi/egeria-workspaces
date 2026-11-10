<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# The Egeria Portal's own report specs, held in Egeria

> Loadable **Dr.Egeria** document. It creates the Portal's two code-defined report specs as
> `ReportSpec` elements in Egeria and makes each a member of the CollectionFolder
> `ReportSpecFolder::EgeriaPortal` (guid `fe5aad27-1587-4d4e-a7c0-ab806650a6e2`). That is the
> folder the Portal syncs at startup (`PYEGERIA_REPORT_SPEC_FOLDERS`).
>
> **This is a shared Egeria write. Run it once, under the shared-write peer check.** Run
> `--validate` first; it makes no changes.
>
> The two specs copy the Portal's local definitions exactly:
>
> | Label | Local definition | Analytic |
> |---|---|---|
> | Analytic - Generic Metric Trend | `local_spec_fallback.metric_trend_specs()` (was `report_specs_handler.register_local_specs`; freshstart's copy is `report_specs_handler._local_specs`) | `metric_trend` (built in to pyegeria) |
> | Resource Explorer - Curation Coverage | `re_analytics.report_specs()` | `re_curation_coverage_tile` (registered by the Portal) |
>
> How the fields map (pyegeria `egeria_spec_cache._build`):
> - `Display Name` is the label. `Qualified Name` is `ReportSpec::<label>`: the sync takes the
>   label from the text after `ReportSpec::` and skips the spec if `Display Name` differs.
> - `Purpose` is the heading. `Category` is the family. `Content Status` must be ACTIVE, or a
>   plain sync skips the spec.
> - `Microflow` is the text `pyegeria.view.microflow.format_set_to_microflow` writes for the local
>   FormatSet. Read back by the sync, it gives the same action, formats and target type. The
>   one difference is that the action's `function` is `None` instead of `""`; both mean "no find
>   stage".
> - There is no target type. Both local specs have `target_type=None`, so the attribute is left out.
> - Admission (resource types, test-only) is not stored on a spec. It comes from the analytic's
>   own declaration when the spec is resolved, so it is the same for both copies.
> - `Parent ID` makes the spec a member of the folder (CollectionMembership, the folder at end 1).
>
> The Portal registers a local copy of each spec only while the synced EGERIA tier does not
> hold that label (`local_spec_fallback.py`). After this runs and the Portal syncs, the Egeria
> copies are the source, and the local copies are the fallback.
>
> **Undo.** Delete both specs. Deleting a ReportSpec also removes its folder membership; the
> folder itself stays. Then re-sync the Portal (admin "Sync from Egeria", or
> `POST /api/report-specs/sync`). The sync prunes the two labels, and the Portal registers its
> local copies again. Deleting needs both specs' GUIDs, which `--process` prints. Example:
> `docker exec -i quickstart-pyegeria-web python -` running
> `CollectionManager(...).delete_collection("<guid>")` for each one, as the same user that
> created them.

___

## Create Report Spec
> Creates or updates a report specification held in Egeria.

### Display Name
Analytic - Generic Metric Trend

### Qualified Name
ReportSpec::Analytic - Generic Metric Trend

### Description
Trend any analytic function over time. metric_path is the target function; metric_params are its keyword arguments. Default trends count_elements(type_name=Asset).

### Purpose
Generic Metric Trend

### Category
Analytic

### Content Status
ACTIVE

### Version Identifier
1.0

### Output Types
DICT, JSON, SERIES

### Microflow
{"format": "microflow/1", "params": {}, "stages": [{"stage": "producer/analytic", "function": "metric_trend", "params": {"metric_path": "count_elements", "metric_params": {"type_name": "Asset"}, "window": "6mo"}}], "formatters": {"DICT": {"columns": []}, "JSON": {"same_as": "DICT"}, "SERIES": {"same_as": "DICT"}}}

### Parent ID
ReportSpecFolder::EgeriaPortal

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
True

___

## Create Report Spec
> Creates or updates a report specification held in Egeria.

### Display Name
Resource Explorer - Curation Coverage

### Qualified Name
ReportSpec::Resource Explorer - Curation Coverage

### Description
Published against not yet published, from Resource Explorer's curation record (trellis-analytics curation_coverage, run by RE as the viewer). The subtitle is the result's state; counts carry the ids they count.

### Purpose
Curation Coverage

### Category
Curation

### Content Status
ACTIVE

### Version Identifier
1.0

### Output Types
DICT, JSON, BAR

### Microflow
{"format": "microflow/1", "params": {}, "stages": [{"stage": "producer/analytic", "function": "re_curation_coverage_tile", "params": {"resource_type": "database"}}], "formatters": {"DICT": {"columns": []}, "JSON": {"same_as": "DICT"}, "BAR": {"same_as": "DICT"}}}

### Parent ID
ReportSpecFolder::EgeriaPortal

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
True

___
