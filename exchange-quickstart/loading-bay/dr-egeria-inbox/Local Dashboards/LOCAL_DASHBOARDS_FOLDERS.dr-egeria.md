<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Dashboard folders: the tree, and the Local Dashboards sheet (LD-2)

> Loadable **Dr.Egeria** document. It builds the tree that organises Dashboard Sheets held in Egeria by
> the tool that shows them, the same way report specs are organised (Architect brief, track (c), LD-FOLDERS,
> 2026-11-11; pyegeria's `pyegeria.view.dashboards`, LD-1):
>
> ```
> RootCollection   "Dashboard Sheets"  RootCollection::DashboardSheets          (PYEGERIA_DASHBOARD_ROOT)
>  ├─ CollectionFolder "Portal"          DashboardFolder::Consumer::Portal
>  └─ CollectionFolder "Egeria Advisor"  DashboardFolder::Consumer::EgeriaAdvisor
> ```
>
> A tool lists the sheets in the folders named by `PYEGERIA_DASHBOARD_FOLDERS` (config.json
> `"Pyegeria Dashboard Folders"`). The member is a sheet's **`Dashboard` element**, qualified name
> `Dashboard::<sheet>`; one sheet may sit in several consumer folders.
>
> **What it does, in order:**
> 1. Creates the root and the two consumer folders. No zones are set, so they are public, like the
>    report-spec tree. Each is its own anchor.
> 2. Makes each folder a member of the root.
> 3. Files the `local-dashboards-next-steps` sheet (made by `LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`, earlier
>    in this batch) in both consumer folders. It uses only a built-in spec (`Work-Item-List-DrE-Basic`).
>
> The four sheets of the "Useful Dashboards" batch are filed by that batch's own
> `LOCAL_DASHBOARDS_USEFUL_SHEETS_FOLDERS.dr-egeria.md`, which runs after the sheets exist. This document
> must have run first (it makes the folders).
>
> **Why `Add Member`, never `Parent ID`.** On a command that ends as an Update, Dr.Egeria's `Parent ID`
> handling can delete an unrelated CollectionMembership of the element before linking the parent. `Add
> Member` calls Egeria's `CollectionHandler.addToCollection`, which updates an existing membership in place,
> so re-running it is safe.
>
> **Re-running it is a no-op in effect.** Every element carries an explicit Qualified Name, so a second run
> finds it and becomes an Update with the same values; each `Add Member` updates the existing membership.
>
> **This is a shared Egeria write.** Run `--validate` first; `--process` once, under the peer check.
>
> **Undo:** remove the memberships (`Remove Member from Collection`, same Collection Id and Element Id), then
> delete the two folders and the root by GUID as the user who created them. Never delete a `Dashboard::`
> element here: removing the membership is enough to unfile a sheet.

___

## Create Root Collection
> The root of the dashboard folder tree.

### Display Name
Dashboard Sheets

### Qualified Name
RootCollection::DashboardSheets

### Description
Root of the dashboard folder tree. Each member is a consumer folder: the Dashboard Sheets a tool shows. Putting a sheet's Dashboard element in a consumer folder publishes the sheet to that tool.

### Purpose
Organise the Dashboard Sheets held in Egeria by the tools that show them.

___

## Create Collection Folder
> A consumer folder. The Egeria Portal's Local Dashboards page names it.

### Display Name
Portal

### Qualified Name
DashboardFolder::Consumer::Portal

### Description
Dashboard Sheets published to the Egeria Portal. The Portal lists the sheets in this folder (PYEGERIA_DASHBOARD_FOLDERS).

### Purpose
Consumer folder: Egeria Portal

___

## Create Collection Folder
> A consumer folder. Egeria Advisor's dashboards name it.

### Display Name
Egeria Advisor

### Qualified Name
DashboardFolder::Consumer::EgeriaAdvisor

### Description
Dashboard Sheets published to Egeria Advisor. Egeria Advisor lists the sheets in this folder (PYEGERIA_DASHBOARD_FOLDERS).

### Purpose
Consumer folder: Egeria Advisor

___

## Add Member to Collection
> Nest the Portal folder under the root.

### Collection Id
RootCollection::DashboardSheets

### Element Id
DashboardFolder::Consumer::Portal

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the dashboard folder tree.

___

## Add Member to Collection
> Nest the Egeria Advisor folder under the root.

### Collection Id
RootCollection::DashboardSheets

### Element Id
DashboardFolder::Consumer::EgeriaAdvisor

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the dashboard folder tree.

___

## Add Member to Collection
> File the Local Dashboards next-steps sheet for the Portal.

### Collection Id
DashboardFolder::Consumer::Portal

### Element Id
Dashboard::local-dashboards-next-steps

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in the Egeria Portal.

___

## Add Member to Collection
> File the Local Dashboards next-steps sheet for Egeria Advisor.

### Collection Id
DashboardFolder::Consumer::EgeriaAdvisor

### Element Id
Dashboard::local-dashboards-next-steps

### Membership Status
VALIDATED

### Membership Rationale
Seeded sheet shown in Egeria Advisor.

___
