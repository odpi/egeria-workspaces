<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Local Dashboards — Worked Example: "Next Steps" Roadmap

> Loadable **Dr.Egeria** document that is the worked example in
> `LOCAL_DASHBOARDS_TUTORIAL.md`. Creates a real Egeria Work Item List of the
> open NEXT-10 punch-list items as Tasks, then a Dashboard Sheet that places
> the `Work-Item-List-DrE-Basic` report spec so the list is browsable at
> `/local-dashboards?sheet=local-dashboards-next-steps`.
>
> **Run with VALIDATE first, then PROCESS.** `Add Member to Collection` steps
> reference the Tasks/List by Display Name — they only resolve once those
> elements actually exist, so VALIDATE will show them as "not found"; that's
> expected mid-file and clears up on PROCESS (each step runs in order and
> earlier Creates have already landed in Egeria by the time each Add Member
> step runs).
>
> **The two `Link Report to Dashboard Sheet` steps below are EXPECTED to
> fail** with "Missing required attribute: 'Report Name'" — they still use
> the original `Report Spec` attribute, which predates the hard cutover to
> `Report Name` (a bare Report Spec can't carry fixed/scoped parameters; see
> `LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md` and BACKLOG.md NEXT-14).
> They're left as-is deliberately, as the worked example of the *original*
> placement approach — run `LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md`
> immediately afterward to create the two Reports and re-link them correctly;
> that's what actually populates the Dashboard Sheet's placements.

___

## Create Work Item List
> Create a WorkItemList collection - a collection organizing work items such as ToDos or Tasks.

### Display Name
Local Dashboards - Next Steps

### Description
Punch list of remaining work for the Local Dashboards / Egeria Overview feature (NEXT-10). Tracked as real Egeria Tasks so it can be browsed like any other dashboard content.

### Category
Roadmap

___

## Create Task
> Creates or updates a task — a small piece of work typically assigned to a single person. Sets the Task classification on the Project entity.

### Display Name
Wire funnelChart into AI & Context Intelligence tile

### Description
Only 2 of 5 context-readiness funnel stages (Cataloged, Classified) are computed today; Documented/Lineage-traced/AI-Ready need graph-traversal queries (R-2) before the real Vega funnel chart can replace the illustrative 5-stage UI without a UX regression.

### Priority
2

### Project Status
Not started

___

## Create Task
> Creates or updates a task — a small piece of work typically assigned to a single person. Sets the Task classification on the Project entity.

### Display Name
Render nested Dashboard Sheets inline

### Description
local-dashboards.html currently just links out to a nested Dashboard Sheet placement ("Open nested sheet ->") instead of rendering it inline in the parent grid. Needs cycle detection before recursive inline rendering is safe.

### Priority
3

### Project Status
Not started

___

## Create Task
> Creates or updates a task — a small piece of work typically assigned to a single person. Sets the Task classification on the Project entity.

### Display Name
Add drill-click parity for Vega bar/line charts

### Description
The hand-drawn SVG tiles it replaced were clickable (drill into the owning app); the new Vega-Lite bar/line/funnel charts in overview_handler.py are not yet wired for click-through navigation.

### Priority
3

### Project Status
Not started

___

## Create Task
> Creates or updates a task — a small piece of work typically assigned to a single person. Sets the Task classification on the Project entity.

### Display Name
Build Egeria Advisor dashboard editor (NEXT-13)

### Description
Backlog item only, not yet scoped: a UI in Egeria Advisor for authoring Dashboard Sheets/placements interactively instead of via Dr.Egeria markdown commands.

### Priority
4

### Project Status
Not started

___

## Create Task
> Creates or updates a task — a small piece of work typically assigned to a single person. Sets the Task classification on the Project entity.

### Display Name
Unblock find_method for Dashboard Sheet commands

### Description
compact_spec_validator._load_omvs_classes() only scans pyegeria.omvs.*, so find_method can't be set on Create Dashboard Sheet / Link Report to Dashboard Sheet (their processors live in md_processing.v2 / pyegeria.view). Needs either a validator scope extension or moving processor entry points into pyegeria.omvs.

### Priority
4

### Project Status
Not started

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Element Id
Wire funnelChart into AI & Context Intelligence tile

### Collection Id
Local Dashboards - Next Steps

### Membership Rationale
Open NEXT-10 P1 item

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Element Id
Render nested Dashboard Sheets inline

### Collection Id
Local Dashboards - Next Steps

### Membership Rationale
Open NEXT-10 P2 item

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Element Id
Add drill-click parity for Vega bar/line charts

### Collection Id
Local Dashboards - Next Steps

### Membership Rationale
Open NEXT-10 P1 item

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Element Id
Build Egeria Advisor dashboard editor (NEXT-13)

### Collection Id
Local Dashboards - Next Steps

### Membership Rationale
Backlog item

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Element Id
Unblock find_method for Dashboard Sheet commands

### Collection Id
Local Dashboards - Next Steps

### Membership Rationale
Backlog item

___

## Create Dashboard Sheet
> Create a Dashboard Sheet - a named, ordered, nestable layout of placed Report Specs used to compose dashboards.

### Display Name
local-dashboards-next-steps

### Dashboard Sheet Heading
Local Dashboards — Next Steps

### Dashboard Sheet Description
The open punch list for the Local Dashboards / Egeria Overview feature, tracked as a real Egeria Work Item List and browsable right here as a Dashboard Sheet.

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Spec
Work-Item-List-DrE-Basic

### Placement Span
full

### Placement Emphasis
panel

___


## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Spec
Collections

### Metadata Element Type
WorkItemList

### Placement Span
full

### Placement Emphasis
panel

### Output Format
REPORT
