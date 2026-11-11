<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Report-spec consumer folders: phase 1, the tree

> Loadable **Dr.Egeria** document. It builds the tree that organises report specs held in Egeria by
> the tool that consumes them (design: BRIEF-REPORT-SPEC-CONSUMER-FOLDERS-2026-11-10, owner
> decisions D1, D2, D3, D6):
>
> ```
> RootCollection   "Report Specs"        RootCollection::ReportSpecs
>  ├─ CollectionFolder "Portal"            ReportSpecFolder::Consumer::Portal   (was ReportSpecFolder::EgeriaPortal, guid fe5aad27-…, renamed)
>  ├─ CollectionFolder "Egeria Advisor"    ReportSpecFolder::Consumer::EgeriaAdvisor
>  ├─ CollectionFolder "Resource Explorer" ReportSpecFolder::Consumer::ResourceExplorer
>  ├─ CollectionFolder "pyegeria"          ReportSpecFolder::Consumer::Pyegeria
>  ├─ CollectionFolder "My Egeria"         ReportSpecFolder::Consumer::MyEgeria
>  └─ CollectionFolder "Jupyter"           ReportSpecFolder::Consumer::Jupyter
> ```
>
> **This is a shared Egeria write. Run it once, under the shared-write peer check.** Run
> `--validate` first; it makes no changes.
>
> **What it does, in order:**
> 1. Creates the RootCollection and the five new consumer folders. No zones are set, so the
>    root and the folders are public (D6), like the existing folder. Each is its own anchor.
> 2. Renames the existing folder `ReportSpecFolder::EgeriaPortal` to
>    `ReportSpecFolder::Consumer::Portal`, with Display Name "Portal". It is the **same element**: the
>    `GUID` attribute makes Dr.Egeria update guid `fe5aad27-1587-4d4e-a7c0-ab806650a6e2` in place,
>    so its GUID and both spec memberships stay as they are. Description is left out, so the
>    merge update keeps the stored one.
> 3. Makes each of the six folders a member of the root (`Add Member to Collection`,
>    CollectionMembership with the root at end 1, status VALIDATED). Nothing is anchored to the
>    root (`Make Anchor` false), so deleting the root never deletes a folder.
>
> **Why the links are separate `Add Member` commands, not `Parent ID`.** On a command that ends as
> an Update, Dr.Egeria's `Parent ID` handling (`_sync_parent_relationship`) looks for any
> CollectionMembership on the element, at either end. If it doesn't find the root among them,
> it **deletes the last one it found** before linking the root. For the Portal folder those are
> its two spec memberships, so `Parent ID` on the rename would unpublish a spec. `Add Member`
> calls Egeria's `CollectionHandler.addToCollection`, which updates an existing membership instead
> of adding a second one, so it is safe to run again.
>
> **Re-running it is a no-op in effect.** Every element command carries an explicit Qualified Name
> (the rename also carries a `GUID`), so a second run finds each element and becomes an Update
> with the same values. Each `Add Member` finds the existing membership and updates it in place.
> No element or relationship is added. An Update may raise an element's version; that is all.
>
> **The Portal side.** The Portal syncs the folders named in `PYEGERIA_REPORT_SPEC_FOLDERS`. Its
> default is now `ReportSpecFolder::Consumer::Portal` only (`egeria-quickstart.yaml`); the old name
> `ReportSpecFolder::EgeriaPortal` is no longer read. (For one deploy the default listed both names,
> so the order of this write and that deploy did not matter.) A sync that sees the renamed folder
> keeps both specs as `unchanged`: same GUIDs and versions, with only the recorded folder name
> changed. On an Egeria where this document has not run yet, the sync reports the folder as
> "not found" and the Portal uses its local copies of its two specs.
>
> **Undo** (every step reads or writes only these seven elements):
> 1. Remove the six root memberships: `Remove Member from Collection` with the same Collection Id
>    and Element Id (or `CollectionManager.remove_from_collection(root_guid, folder_guid)` for each).
> 2. Rename the Portal folder back: the same `Create Collection Folder` block with Qualified Name
>    `ReportSpecFolder::EgeriaPortal` and Display Name `EgeriaPortal` (the GUID keeps it the same element).
> 3. Delete the root and the five new folders, which are empty. Delete by GUID; `--process` prints
>    each one, as `CollectionManager(...).delete_collection("<guid>")`, run as the user who created them.
>    Never delete fe5aad27: it holds the Portal's specs.
> 4. Set `PYEGERIA_REPORT_SPEC_FOLDERS=ReportSpecFolder::EgeriaPortal` for the Portal (the default
>    no longer names the old folder), restart it, and re-sync (`POST /api/report-specs/sync`). Both
>    specs are then found again.

___

## Create Root Collection
> The root of the report-spec tree.

### Display Name
Report Specs

### Qualified Name
RootCollection::ReportSpecs

### Description
Root of the report-spec tree. Each member is a consumer folder: the report specs a tool takes from Egeria. Putting a spec in a consumer folder publishes it to that tool.

### Purpose
Organise the report specs held in Egeria by the tools that consume them.

___

## Create Collection Folder
> A consumer folder. Egeria Advisor's report-spec sync names it.

### Display Name
Egeria Advisor

### Qualified Name
ReportSpecFolder::Consumer::EgeriaAdvisor

### Description
Report specs published to Egeria Advisor. Egeria Advisor syncs this folder.

### Purpose
Consumer folder: Egeria Advisor

___

## Create Collection Folder
> A consumer folder. Resource Explorer's report-spec sync names it.

### Display Name
Resource Explorer

### Qualified Name
ReportSpecFolder::Consumer::ResourceExplorer

### Description
Report specs published to Resource Explorer. Resource Explorer syncs this folder.

### Purpose
Consumer folder: Resource Explorer

___

## Create Collection Folder
> A consumer folder. pyegeria's CLI and library default names it.

### Display Name
pyegeria

### Qualified Name
ReportSpecFolder::Consumer::Pyegeria

### Description
Report specs published to pyegeria's CLI and library. pyegeria's default report-spec sync takes this folder.

### Purpose
Consumer folder: pyegeria

___

## Create Collection Folder
> A consumer folder. My Egeria's report-spec sync names it.

### Display Name
My Egeria

### Qualified Name
ReportSpecFolder::Consumer::MyEgeria

### Description
Report specs published to My Egeria. My Egeria syncs this folder.

### Purpose
Consumer folder: My Egeria

___

## Create Collection Folder
> A consumer folder. The Jupyter environment's report-spec sync names it.

### Display Name
Jupyter

### Qualified Name
ReportSpecFolder::Consumer::Jupyter

### Description
Report specs published to the Jupyter environment. Jupyter syncs this folder.

### Purpose
Consumer folder: Jupyter

___

## Create Collection Folder
> Renames the existing Portal folder in place. The GUID makes this the same element, so its
> two spec memberships stay. No Parent ID here: see the header.

### GUID
fe5aad27-1587-4d4e-a7c0-ab806650a6e2

### Display Name
Portal

### Qualified Name
ReportSpecFolder::Consumer::Portal

### Purpose
Consumer folder: Egeria Portal

___

## Add Member to Collection
> Nest the Portal folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::Portal

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___

## Add Member to Collection
> Nest the Egeria Advisor folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::EgeriaAdvisor

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___

## Add Member to Collection
> Nest the Resource Explorer folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::ResourceExplorer

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___

## Add Member to Collection
> Nest the pyegeria folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::Pyegeria

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___

## Add Member to Collection
> Nest the My Egeria folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::MyEgeria

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___

## Add Member to Collection
> Nest the Jupyter folder under the root.

### Collection Id
RootCollection::ReportSpecs

### Element Id
ReportSpecFolder::Consumer::Jupyter

### Membership Status
VALIDATED

### Membership Rationale
Consumer folder of the report-spec tree.

___
