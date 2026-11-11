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
> 3. Files the `local-dashboards-next-steps` sheet (made by `Local Dashboards/LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`)
>    in both consumer folders. It uses only a built-in spec (`Work-Item-List-DrE-Basic`).
>
> **Its batch.** "Dashboard Folders", on by default, canary the root (`RootCollection` "Dashboard Sheets"), so the
> tree heals on its own even where Local Dashboards already ran. `_folder_order.json` runs it after "Local Dashboards"
> (which makes the next-steps sheet) and before "Useful Dashboards", whose last file
> (`LOCAL_DASHBOARDS_USEFUL_SHEETS_FOLDERS.dr-egeria.md`) files its four sheets in these folders.
>
> **Why `Add Member`, never `Parent ID`.** On a command that ends as an Update, Dr.Egeria's `Parent ID`
> handling can delete an unrelated CollectionMembership of the element before linking the parent.
>
> **Run it once.** `Add Member to Collection` does not dedupe: a second run adds a second membership for each
> link. (The root and folders carry explicit Qualified Names, so they alone would be updated in place.) The
> batch's canary, the root, prevents heal re-runs: a heal runs this file only when the root is missing.
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
