<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Local Dashboards — "Next Steps" Report Migration

> Loadable **Dr.Egeria** document that migrates the `local-dashboards-next-steps`
> Dashboard Sheet (see `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`) off its
> original bare Report Spec placements onto real `Report` elements, following
> the hard cutover of `Link Report to Dashboard Sheet`'s target attribute
> from `Report Spec` to `Report Name` (a Report Spec alone can't carry fixed/
> scoped parameters — see egeria-workspaces-fs BACKLOG.md NEXT-14).
>
> Creates two `Report` assets and links both into the existing Dashboard
> Sheet:
> - **Next Steps Work Item List** — a `Work-Item-List-DrE-Basic` instance,
>   DICT format. No Search String needed; that spec only ever returns
>   WorkItemList collections, so it's inherently narrow.
> - **Next Steps Membership Diagram** — a `Collections` instance, MERMAID
>   format, **scoped with Search String** to the "Local Dashboards - Next
>   Steps" collection specifically. This is the concrete fix for the "output
>   format ignored" / "huge unscoped diagram" problems hit earlier in this
>   feature's development — without a Report carrying its own Search String,
>   this same placement returned a diagram of the *entire* dataset (observed
>   80–150KB) rather than just this one Work Item List and its Task members.
>
> **Where it writes (updated 2026-11-10).** `Create Report` and the updated
> `Link Report to Dashboard Sheet` ship in published pyegeria, so this file
> runs anywhere, including `docker exec quickstart-pyegeria-web dr_egeria` or
> the Portal's **▶ Run Dr.Egeria Document** panel. Since pyegeria 6.2.29 the
> sheet is written into Egeria (plus a local fallback copy); the
> `local-dashboards-next-steps` sheet was moved into Egeria on 2026-11-10.
> See `LOCAL_DASHBOARDS_TUTORIAL.md`, "Where Dashboard Sheets live".
>
> **Run with VALIDATE first, then PROCESS.** The two `Link Report to
> Dashboard Sheet` steps reference the Reports created earlier in this same
> file — VALIDATE will show them as "not found" (expected, mid-file
> forward-reference, same pattern as `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`);
> clears up on PROCESS since each step runs in order.
>
> This file only re-links; it doesn't remove the two old direct-Report-Spec
> placements (`Work-Item-List-DrE-Basic`, `Collections`) — those were removed
> by hand-editing the old JSON store after this ran, before the sheet moved
> into Egeria.

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Next Steps Work Item List

### Description
The Local Dashboards - Next Steps Work Item List itself (header attributes) — a Report instance of Work-Item-List-DrE-Basic, no scoping needed since that spec only ever returns WorkItemList collections.

### Report Spec
Work-Item-List-DrE-Basic

### Output Format
DICT

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Next Steps Membership Diagram

### Description
Mermaid diagram of the Local Dashboards - Next Steps Work Item List and its Task members — a Report instance of Collections, scoped with Search String so it doesn't return the entire dataset.

### Report Spec
Collections

### Output Format
MERMAID

### Search String
Local Dashboards - Next Steps

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Tasks

### Description
Tasks for the project

### Report Spec
Collection Members

### Output Format
MERMAID

### Report Parameters
collection_qname : Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0

### OUTPUT Format
TABLE

---
## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Tasks

### Placement Span
2

### Placement Emphasis
kpi
---

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Next Steps Work Item List

### Placement Span
2

### Placement Emphasis
kpi

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
local-dashboards-next-steps

### Report Name
Next Steps Membership Diagram

### Placement Span
full

### Placement Emphasis
panel

___
## Add Text on Dashboard Sheet
### Placement Name
My own mermaid
### Dashboard Sheet Name
local-dashboards-next-steps

### MD Content
 This is could be a bunch of content.
**italics?**

### Placement Span
full

### Placement Emphasis
panel
