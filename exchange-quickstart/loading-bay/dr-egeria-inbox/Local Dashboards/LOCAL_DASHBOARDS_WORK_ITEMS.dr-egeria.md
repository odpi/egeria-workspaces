<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Local Dashboards — Next Steps: Work Items

> Loadable **Dr.Egeria** document that (re)populates the `Local Dashboards -
> Next Steps` Work Item List (created by
> `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`) with its Task members. Split out
> as its own file so the Tasks can be recreated/re-linked independently of
> the Work Item List + Dashboard Sheet setup — e.g. after a demo-environment
> reset wipes the Tasks but leaves the collection itself in place.
>
> **Run with VALIDATE first, then PROCESS.** `Add Member to Collection`
> steps reference the Tasks by Display Name, so — same as the roadmap file
> — VALIDATE will report them "not found" (they don't exist yet at
> validate-time); that clears up on PROCESS since each step runs in order.
> The target Work Item List (`Local Dashboards - Next Steps`) must already
> exist — run `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md` first if it doesn't.

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
