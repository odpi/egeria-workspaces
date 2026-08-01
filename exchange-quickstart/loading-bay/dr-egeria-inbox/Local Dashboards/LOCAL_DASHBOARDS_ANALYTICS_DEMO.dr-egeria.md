<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Local Dashboards — Analytic Function Demo (Projects & Terms)

> Loadable **Dr.Egeria** document that extends the `local-dashboards-next-steps`
> Dashboard Sheet (see `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md` and
> `LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md`) with three placements
> that show **analytic-function-backed** Reports in action — Report Specs
> whose action runs a plain Python routine returning an already-aggregated
> result, rather than querying Egeria elements directly (see
> `pyegeria/view/analytic_registry.py` / `analytic_demo_specs.py`, and
> `LOCAL_DASHBOARDS_TUTORIAL.md`'s "Analytic reports" section for the
> concepts).
>
> Creates three `Report` assets and links all three into the existing
> Dashboard Sheet:
> - **Project Count** and **Term Count** — both instances of the *same*
>   **GENERIC** analytic function, `count_elements`
>   (`Analytic Demo - Element Count by Type` report spec), retargeted at two
>   different types via `Analytic Parameters: type_name`. This is the point
>   of a GENERIC analytic function: one Python routine, reusable at any
>   type, no code change needed to count something else.
> - **Term Definition Completeness** — a genuinely *different*, **FIXED**
>   analytic function (`term_definition_completeness`). Unlike
>   `count_elements`, this one's vocabulary (GlossaryTerm's `description`
>   property) is hardcoded in the function body — it's inherently
>   Term-specific, not retargetable via a parameter. Included to show both
>   ends of the GENERIC/FIXED spectrum side by side.
>
> **A known gap surfaced while building this**: a *third* kind of variety —
> one generic function (`counts_by_type`) comparing Projects and Terms
> **in a single chart** — was attempted first and hit a real pyegeria bug:
> `Analytic Parameters`/`Report Parameters` stringify every value before
> storing them, which silently breaks any parameter whose real type is a
> list (`counts_by_type`'s `type_map`). See egeria-python's
> `PYEGERIA_ISSUES.md` ISSUE-20 (also logged in this repo's
> `PYEGERIA_GAPS.md` #6) for the full repro and candidate fix — **not
> fixed here**, per the standing rule to track pyegeria-repo issues for
> approval before touching code. Until it's fixed, only scalar-valued
> `Analytic Parameters` (`type_name`, `window`, `points`, …) work reliably;
> avoid list/dict-valued ones (`type_map`, `metric_params`).
>
> **Requires the `Create Report` / `Link Report to Dashboard Sheet`
> commands** — see `LOCAL_DASHBOARDS_TUTORIAL.md`'s "Where `dr_egeria` has
> to run" section for the same venv/container caveats that applied to the
> Next Steps Reports file.
>
> **Run with VALIDATE first, then PROCESS.** The three `Link Report to
> Dashboard Sheet` steps reference the Reports created earlier in this same
> file — VALIDATE will show them as "not found" (expected, mid-file
> forward-reference); clears up on PROCESS since each step runs in order.

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Project Count

### Description
Count of active Project elements — the GENERIC `count_elements` analytic function, retargeted at Project via Analytic Parameters (the same function backs Term Count below, pointed at a different type).

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: Project

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Term Count

### Description
Count of active GlossaryTerm elements — the same GENERIC `count_elements` analytic function as Project Count above, retargeted at GlossaryTerm.

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Term Definition Completeness

### Description
Share of GlossaryTerms carrying a non-empty description — a genuinely different, FIXED analytic function (term_definition_completeness) from Project/Term Count's GENERIC count_elements. Its vocabulary (GlossaryTerm's description property) is hardcoded, not a parameter, so it needs no Analytic Parameters at all.

### Report Spec
Analytic Demo - Term Definition Completeness

### Output Format
DICT

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Project Count

### Placement Span
1

### Placement Emphasis
kpi

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Term Count

### Placement Span
1

### Placement Emphasis
kpi

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Term Definition Completeness

### Placement Span
2

### Placement Emphasis
kpi

___
