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

___


## Update Work Item List

### Work Item List Name 

Local Dashboards - Next Steps

### Category
Roadmap

### Description
Punch list of remaining work for the Local Dashboards / Egeria Overview feature (NEXT-10). Tracked as real Egeria Tasks so it can be browsed like any other dashboard content.

### Display Name
Local Dashboards - Next Steps

### GUID
0affb580-fa81-4d00-9438-b26faf11845d

### Legal
None

### Qualified Name
Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Purpose
None


___


## Update Task

### Task Name 

Wire funnelChart into AI & Context Intelligence tile

### Category
None

### Description
Only 2 of 5 context-readiness funnel stages (Cataloged, Classified) are computed today; Documented/Lineage-traced/AI-Ready need graph-traversal queries (R-2) before the real Vega funnel chart can replace the illustrative 5-stage UI without a UX regression.

### Display Name
Wire funnelChart into AI & Context Intelligence tile

### GUID
9f13b7b1-bd27-4c22-81b3-47b8e3e372c3

### Legal
None

### Qualified Name
Wire funnelChart into AI & Context Intelligence tile::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Actual Completion Date
None

### Actual Start Date
None

### Mission
None

### Planned Completion Date
None

### Planned Start Date
None

### Priority
2

### Project Approach
None

### Project Health
None

### Project Identifier
None

### Project Management Style
None

### Project Phase
None

### Project Results Usage
None

### Project Scope
None

### Project Status
Not started

### Project Type
None

### Purposes
None

### Sub-Projects
None

### Success Criteria
None


___


## Update Task

### Task Name 

Render nested Dashboard Sheets inline

### Category
None

### Description
local-dashboards.html currently just links out to a nested Dashboard Sheet placement ("Open nested sheet ->") instead of rendering it inline in the parent grid. Needs cycle detection before recursive inline rendering is safe.

### Display Name
Render nested Dashboard Sheets inline

### GUID
797b1d3c-67ff-4832-ad24-06432b24d564

### Legal
None

### Qualified Name
Render nested Dashboard Sheets inline::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Actual Completion Date
None

### Actual Start Date
None

### Mission
None

### Planned Completion Date
None

### Planned Start Date
None

### Priority
3

### Project Approach
None

### Project Health
None

### Project Identifier
None

### Project Management Style
None

### Project Phase
None

### Project Results Usage
None

### Project Scope
None

### Project Status
Not started

### Project Type
None

### Purposes
None

### Sub-Projects
None

### Success Criteria
None


___


## Update Task

### Task Name 

Add drill-click parity for Vega bar/line charts

### Category
None

### Description
The hand-drawn SVG tiles it replaced were clickable (drill into the owning app); the new Vega-Lite bar/line/funnel charts in overview_handler.py are not yet wired for click-through navigation.

### Display Name
Add drill-click parity for Vega bar/line charts

### GUID
d8a61d15-fb63-44d2-b6ed-91557036e066

### Legal
None

### Qualified Name
Add drill-click parity for Vega bar/line charts::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Actual Completion Date
None

### Actual Start Date
None

### Mission
None

### Planned Completion Date
None

### Planned Start Date
None

### Priority
3

### Project Approach
None

### Project Health
None

### Project Identifier
None

### Project Management Style
None

### Project Phase
None

### Project Results Usage
None

### Project Scope
None

### Project Status
Not started

### Project Type
None

### Purposes
None

### Sub-Projects
None

### Success Criteria
None


___


## Update Task

### Task Name 

Build Egeria Advisor dashboard editor (NEXT-13)

### Category
None

### Description
Backlog item only, not yet scoped: a UI in Egeria Advisor for authoring Dashboard Sheets/placements interactively instead of via Dr.Egeria markdown commands.

### Display Name
Build Egeria Advisor dashboard editor (NEXT-13)

### GUID
c816f0e6-6789-404f-9946-b40a1ab3bf61

### Legal
None

### Qualified Name
Build Egeria Advisor dashboard editor (NEXT-13)::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Actual Completion Date
None

### Actual Start Date
None

### Mission
None

### Planned Completion Date
None

### Planned Start Date
None

### Priority
4

### Project Approach
None

### Project Health
None

### Project Identifier
None

### Project Management Style
None

### Project Phase
None

### Project Results Usage
None

### Project Scope
None

### Project Status
Not started

### Project Type
None

### Purposes
None

### Sub-Projects
None

### Success Criteria
None


___


## Update Task

### Task Name 

Unblock find_method for Dashboard Sheet commands

### Category
None

### Description
compact_spec_validator._load_omvs_classes() only scans pyegeria.omvs.*, so find_method can''t be set on Create Dashboard Sheet / Link Report to Dashboard Sheet (their processors live in md_processing.v2 / pyegeria.view). Needs either a validator scope extension or moving processor entry points into pyegeria.omvs.

### Display Name
Unblock find_method for Dashboard Sheet commands

### GUID
f83d77e8-7413-436c-a4f9-4a5142ea09e7

### Legal
None

### Qualified Name
Unblock find_method for Dashboard Sheet commands::1.0

### Url
None

### Version Identifier
1.0

### Authors
None

### Content Status
ACTIVE

### Actual Completion Date
None

### Actual Start Date
None

### Mission
None

### Planned Completion Date
None

### Planned Start Date
None

### Priority
4

### Project Approach
None

### Project Health
None

### Project Identifier
None

### Project Management Style
None

### Project Phase
None

### Project Results Usage
None

### Project Scope
None

### Project Status
Not started

### Project Type
None

### Purposes
None

### Sub-Projects
None

### Success Criteria
None


___



## Add Member to Collection

Operation completed.

### Associated Elements
- **Collection Id**: `Local Dashboards - Next Steps`
- **Element Id**: `Wire funnelChart into AI & Context Intelligence tile`

### Link Properties
- **Membership Rationale**: Open NEXT-10 P1 item
- **Membership Status**: PROPOSED

___



## Add Member to Collection

Operation completed.

### Associated Elements
- **Collection Id**: `Local Dashboards - Next Steps`
- **Element Id**: `Render nested Dashboard Sheets inline`

### Link Properties
- **Membership Rationale**: Open NEXT-10 P2 item
- **Membership Status**: PROPOSED

___



## Add Member to Collection

Operation completed.

### Associated Elements
- **Collection Id**: `Local Dashboards - Next Steps`
- **Element Id**: `Add drill-click parity for Vega bar/line charts`

### Link Properties
- **Membership Rationale**: Open NEXT-10 P1 item
- **Membership Status**: PROPOSED

___



## Add Member to Collection

Operation completed.

### Associated Elements
- **Collection Id**: `Local Dashboards - Next Steps`
- **Element Id**: `Build Egeria Advisor dashboard editor (NEXT-13)`

### Link Properties
- **Membership Rationale**: Backlog item
- **Membership Status**: PROPOSED

___



## Add Member to Collection

Operation completed.

### Associated Elements
- **Collection Id**: `Local Dashboards - Next Steps`
- **Element Id**: `Unblock find_method for Dashboard Sheet commands`

### Link Properties
- **Membership Rationale**: Backlog item
- **Membership Status**: PROPOSED

___



## Create Dashboard Sheet

Created Dashboard Sheet **local-dashboards-next-steps**

- **Heading**: Local Dashboards — Next Steps
- **Description**: The open punch list for the Local Dashboards / Egeria Overview feature, tracked as a real Egeria Work Item List and browsable right here as a Dashboard Sheet.
- **Family**: _(none)_

___



## Link Report to Dashboard Sheet

Placed **Work-Item-List-DrE-Basic** in Dashboard Sheet **local-dashboards-next-steps** (span=full, emphasis=panel)

___




## Link Report to Dashboard Sheet

Placed **Collections** in Dashboard Sheet **local-dashboards-next-steps** (span=full, emphasis=panel)




## Provenance:
 
- Derived from processing file LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md on 2026-07-29 10:04
