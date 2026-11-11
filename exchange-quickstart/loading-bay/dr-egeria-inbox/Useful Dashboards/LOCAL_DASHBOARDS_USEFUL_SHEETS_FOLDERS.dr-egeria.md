<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# File the four useful sheets in the dashboard folders (LD-2)

> Loadable **Dr.Egeria** document. It files the four sheets made by `LOCAL_DASHBOARDS_USEFUL_SHEETS.dr-egeria.md`
> (`catalog-health`, `glossary-and-meaning`, `governance-and-compliance`, `community-and-feedback`) in both
> consumer folders of the dashboard folder tree: `DashboardFolder::Consumer::Portal` and
> `DashboardFolder::Consumer::EgeriaAdvisor`. The member is each sheet's `Dashboard` element (`Dashboard::<sheet>`).
>
> **Needs, already run:** the sheets file of this batch, and `Local Dashboards/LOCAL_DASHBOARDS_FOLDERS.dr-egeria.md`
> (it makes the root and the folders). The "Local Dashboards" batch runs before this one.
>
> Every tile uses a built-in pyegeria spec except `catalog-health`'s "Assets with No Lineage" tile (from
> `LOCAL_DASHBOARDS_SAVED_QUERY_TILE.dr-egeria.md`), whose spec "Saved Query Answer" is filed only in
> `ReportSpecFolder::Consumer::Portal`. A tool that doesn't take that report-spec folder shows that one tile as
> a missing spec; the rest of the sheet works.
>
> `Add Member`, never `Parent ID` (see `LOCAL_DASHBOARDS_FOLDERS.dr-egeria.md`). Re-running it updates the same
> memberships. **This is a shared Egeria write:** `--validate` first, `--process` once under the peer check.
> **Undo:** `Remove Member from Collection` with the same Collection Id and Element Id.

___

## Add Member to Collection
> File the catalog-health sheet for the Portal.

### Collection Id
DashboardFolder::Consumer::Portal

### Element Id
Dashboard::catalog-health

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in the Egeria Portal.

___

## Add Member to Collection
> File the catalog-health sheet for Egeria Advisor.

### Collection Id
DashboardFolder::Consumer::EgeriaAdvisor

### Element Id
Dashboard::catalog-health

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in Egeria Advisor.

___

## Add Member to Collection
> File the glossary-and-meaning sheet for the Portal.

### Collection Id
DashboardFolder::Consumer::Portal

### Element Id
Dashboard::glossary-and-meaning

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in the Egeria Portal.

___

## Add Member to Collection
> File the glossary-and-meaning sheet for Egeria Advisor.

### Collection Id
DashboardFolder::Consumer::EgeriaAdvisor

### Element Id
Dashboard::glossary-and-meaning

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in Egeria Advisor.

___

## Add Member to Collection
> File the governance-and-compliance sheet for the Portal.

### Collection Id
DashboardFolder::Consumer::Portal

### Element Id
Dashboard::governance-and-compliance

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in the Egeria Portal.

___

## Add Member to Collection
> File the governance-and-compliance sheet for Egeria Advisor.

### Collection Id
DashboardFolder::Consumer::EgeriaAdvisor

### Element Id
Dashboard::governance-and-compliance

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in Egeria Advisor.

___

## Add Member to Collection
> File the community-and-feedback sheet for the Portal.

### Collection Id
DashboardFolder::Consumer::Portal

### Element Id
Dashboard::community-and-feedback

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in the Egeria Portal.

___

## Add Member to Collection
> File the community-and-feedback sheet for Egeria Advisor.

### Collection Id
DashboardFolder::Consumer::EgeriaAdvisor

### Element Id
Dashboard::community-and-feedback

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in Egeria Advisor.

___
