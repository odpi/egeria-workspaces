<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Tutorial: Create and Implement a New Local Dashboard

This is a step-by-step guide to authoring a **Dashboard Sheet** with
Dr.Egeria and getting it live in the **Local Dashboards** portal app
(`/local-dashboards`). It ends with a real, worked example — a dashboard
that lists the outstanding "next steps" for this very feature, tracked as
actual Egeria Work Items rather than a paragraph of prose.

> **Quickstart only.** Local Dashboards is part of the quickstart Portal. The
> freshstart Portal has no Local Dashboards page; the Dr.Egeria commands below
> still write sheets into Egeria from there, but nothing in freshstart shows them.

See also: [Worked Examples](worked-examples.md) for dashboards, specs, functions and queries of
different kinds with their outputs, [Report Specs](report-specs.md) and
[Add and Use Analytic Functions](analytic-functions.md) for the specs and
functions a Report runs, [`OVERVIEW_REPORTING_MODEL.md`](https://github.com/odpi/egeria-workspaces/blob/main/compose-configs/egeria-quickstart/PyegeriaWebHandler/OVERVIEW_REPORTING_MODEL.md) §10
for the design history,
[`report-specs-dashboards-egeria-model.md`](../Internals/report-specs-dashboards-egeria-model.md)
for how sheets are held in Egeria,
[Digital Product & Subscription Dashboard](digital-product-subscription.md)
for a business-oriented worked example focusing on Data Products and
Subscriptions,
[Create and Use Saved Queries](saved-queries.md) for building a saved
query in the Query tool and putting its results on a dashboard, and
[`BACKLOG.md`](https://github.com/odpi/egeria-workspaces/blob/main/BACKLOG.md) NEXT-10 for where this fits in the
larger Overview/Dashboard roadmap.

## Concepts, in one paragraph

A **Dashboard Sheet** is a named, ordered list of **Placements**. Each
Placement is a `ref` (a name) that resolves to either a **Report** — a real
Egeria element (type `Report`, a `DataSet`/`Asset` subtype) created with the
Dr.Egeria `Create Report` command, carrying a **Report Spec** reference
(`FormatSet`, from pyegeria's report registry — the same specs you can
browse and run one-at-a-time in Egeria Explorer's Report Spec Browser) plus
its own concrete execution parameters (`Output Format`, `Search String`,
and the rest of the same 22-attribute vocabulary `View Report` exposes
ad-hoc — plus, for an analytic-function-backed spec, `Analytic Parameters`;
see "Analytic reports" below) — another Dashboard Sheet (nesting), or
literal **markdown text** (`Add Text on Dashboard Sheet` — a caption/section
header; no Report, the text is held on the sheet itself), plus two layout hints:
`span` (`"1"` / `"2"` / `"full"`, how wide the tile is) and `emphasis`
(`"kpi"` compact vs `"panel"` larger/detailed). Since pyegeria 6.2.29 a
Dashboard Sheet is **held in Egeria** as a small chain of elements (see
"Where Dashboard Sheets live" below). The older local JSON file
(`~/.pyegeria/dashboard_sheets.json`) is now only a fallback for sheets
that have not been moved into Egeria yet. Local Dashboards is the portal
app that lists and renders Dashboard Sheets.

**Report vs. Report Spec — don't confuse them.** A Report Spec (`FormatSet`)
is a *template*: what to query and how it can be formatted, with no fixed
values — the same one can be run with any search string, any output format.
A Report is a *named, saved instance* of running one: "the `Collections`
spec, as MERMAID, scoped to this one collection." Placements always
reference a Report, never a bare Report Spec directly — that's what makes a
placement genuinely scoped/parameterized instead of always falling back to
"match everything, capped".

This is deliberately a *different* model from `egeria-overview.html`'s own
Container (`overview_containers.py`): that one is the Overview app's own
static P0 KPI layout, resolved against `overview_specs.SPECS` (Python-
computed tiles like the growth chart, not stored Report Specs). Dashboard
Sheets are the **user-authored** model — anyone can build one without
touching Python.

## Where Dashboard Sheets live

*(Updated 2026-11-10, pyegeria 6.2.29.)*

### In Egeria

A sheet is stored in Egeria as this chain of elements. Each one is named
after the sheet's `Display Name`:

| Element | Qualified name | What it holds |
|---|---|---|
| `Dashboard` (an asset) | `Dashboard::<sheet name>` | the sheet itself; its display name is the sheet's heading. It carries an `Ownership` classification naming the sheet's owner |
| `DisplayDataSchemaType` | `DashboardSchema::<sheet name>` | the sheet's layout, linked from the Dashboard by a `Schema` relationship |
| `DisplayDataContainer` | `DashboardSheet::<sheet name>` | the ordered list of placements |
| `DisplayDataField`, one per placement | `DashboardPlacement::<sheet name>::<position>::<placement name>` | the span and style of a tile, or the markdown of a text placement |

A report placement is linked to its `Report` with a `DataSetContent`
relationship from the Dashboard. Deleting a sheet removes this chain only.
It never deletes a `Report` or a Report Spec, because a sheet shows reports,
it does not own them.

### The local file, as a fallback

Before 6.2.29 every sheet lived in a JSON file
(`PYEGERIA_DASHBOARD_SHEETS_STORE`, default `~/.pyegeria/dashboard_sheets.json`).
The Portal still reads that file, but only for sheet names Egeria does not
hold:

- The Portal reads Egeria first. **If a name is in Egeria, the Egeria copy
  wins** and the local copy is ignored.
- Each sheet card, sheet heading and placement shows a small tag saying
  where it is held: **Egeria** or **local file**.
- If Egeria cannot be read, the page says so in a note ("Egeria could not
  be read, so only sheets from the local file are shown…") instead of
  showing a shorter list as if it were complete.
- If a sheet's chain in Egeria is broken (for example a `Dashboard` made with
  plain `Create Dashboard`, which has no layout), the sheet is still listed,
  with a note naming what is missing.

On the quickstart demo the five sheets that used to be in the file — Chief
Data Officer Dashboard, `local-dashboards-next-steps`, Assets by Type and
Location Demo, `digital-product-portfolio` and `my-team-dashboard` — were
moved into Egeria on 2026-11-10. They kept their names and are owned by
`erinoverview`. Their entries were then removed from the local file, so
each name now opens only the Egeria copy.

### Commands for sheets held in Egeria

pyegeria 6.2.29 has a small command-line tool. Inside the Portal's container
it already has the connection settings it needs (`EGERIA_VIEW_SERVER`,
`EGERIA_PLATFORM_URL`, `EGERIA_USER`, `EGERIA_USER_PASSWORD`); elsewhere,
set those first.

```bash
python -m pyegeria.view.dashboards list                 # every sheet held in Egeria
python -m pyegeria.view.dashboards show "my-team-dashboard"   # one sheet and its placements
python -m pyegeria.view.dashboards migrate --dry-run    # what migrate WOULD write; writes nothing
python -m pyegeria.view.dashboards migrate [--sheet NAME] [--rename NEW_NAME] [--store PATH] [--owner USER]
python -m pyegeria.view.dashboards delete --sheet NAME [--dry-run] [--local]
```

- `list` and `show` only read. `show` says so plainly if no sheet of that
  name is in Egeria.
- `migrate` copies sheets from the local file into Egeria. With no
  `--sheet` it copies every sheet in the file. `--rename` writes one
  `--sheet` under a different name (a scratch copy you can try out first).
  `--owner` sets the owner (default: the signed-in user); a sheet that
  already has an owner keeps it. Running it again changes nothing that is
  already right. It **never changes the local file**: remove the old entry
  yourself once you have checked the Egeria copy (`delete --local` does
  not help here, because it also deletes the Egeria copy).
- `delete` removes a sheet's chain from Egeria (never its Reports).
  `--local` also removes the sheet's entry from the local file.

> **`migrate` and `delete` are shared writes.** Everyone using this Egeria
> sees the result. On a shared environment, agree it with whoever looks
> after that Egeria before you run them, run them once, and use
> `--dry-run` first to see exactly what will be written.

### Who sees what: zones and the "not visible to you" tile

*(Checked 2026-11-10 on the quickstart: Portal at commit 81d6e636, pyegeria 6.2.32.)*

Every read for a sheet held in Egeria is made **as the person viewing it**,
so Egeria's governance zones decide what each person sees. One sheet can show
different tiles to different people.

The Portal reads a sheet with pyegeria's shared dashboard step
(`pyegeria.view.dashboard_resolver`; Egeria Advisor uses the same one). When
`Link Report to Dashboard Sheet` places a Report, it records that Report's GUID
on the placement (`reportGUID`). The Portal reads each Report by that GUID.
Each placement then comes back as one of four kinds:

| Kind | What the tile shows | Why |
|---|---|---|
| report | the report | the Report was read, and its spec was found |
| text | the markdown | an `Add Text on Dashboard Sheet` placement |
| restricted | 🔒 *Report not visible to you.* (dashed border) | the Report, or the Egeria-held report spec it names, is in a zone this viewer cannot see. The other tiles still show |
| missing | "Unresolved reference — no matching Report or Dashboard Sheet." | the Report was deleted, or its link was removed. The Portal then looks the Report up by name, and finds nothing |

Reading by GUID is what tells *restricted* apart from *missing*: Egeria
answers "not authorized" for an element in a hidden zone and "not found" for
one that is gone. A placement written before the GUID was recorded, whose link
is gone, can only be *missing*. Re-running its `Link Report to Dashboard
Sheet` records the GUID.

To restrict a tile, set **Zone Membership** on the `Create Report` (it is a
Basic attribute). Use pyegeria 6.2.30 or later to update a Report: in 6.2.29
and earlier, an update with **Zone Membership** left empty removed the
Report's zones.

On the quickstart the sheet `scratch-restricted-demo` shows both kinds side by
side: *Project Count* as a report, and *B4 Scratch Restricted Report* as
restricted for the Portal's service user.

### Which tools show a sheet: dashboard folders and "Used by"

*(Portal from 2026-11-11, pyegeria 6.2.34 or later.)*

Sheets held in Egeria are organised by the tool that shows them, the same
way report specs are (see [consumer folders](report-specs.md#b1-how-specs-are-organised-consumer-folders)):

```
RootCollection   "Dashboard Sheets"   RootCollection::DashboardSheets
 ├─ CollectionFolder "Portal"          DashboardFolder::Consumer::Portal
 └─ CollectionFolder "Egeria Advisor"  DashboardFolder::Consumer::EgeriaAdvisor
```

- **Putting a sheet's `Dashboard` element in a tool's folder publishes the
  sheet to that tool.** One sheet can be in several folders. Use
  `Add Member to Collection` with the folder's qualified name and
  `Dashboard::<sheet name>`. Removing the membership unpublishes it; never
  delete the `Dashboard` element to do that.
- **The Portal lists the sheets in the folders named by
  `PYEGERIA_DASHBOARD_FOLDERS`**, `DashboardFolder::Consumer::Portal` on the
  quickstart. Unset means that default; an empty value means every
  `Dashboard::` sheet, whatever its folder.
- **The list page** says which folder it read ("Egeria-held sheets are
  listed from the folder DashboardFolder::Consumer::Portal"). Each card
  shows the folder it was found in and a **Used by** row naming every tool
  whose folder holds the sheet (for example *Egeria Advisor*, *Portal*).
  Two filters narrow the list:
  - **Source:** All, Egeria folder or Local file;
  - **Used by:** Any, one tool, or *No consumer folder*.
- **Absence is said, never shown as an empty list.** No folders configured,
  a folder not found or not visible to you, or a read that failed: each gets
  a note. A sheet whose tools could not be read says *Used by: not read*,
  and is never counted as used by none. A sheet in the local file says *not
  tracked*.
- **A sheet outside the folders still opens by name**
  (`/local-dashboards?sheet=NAME`); it is just not listed.

On the quickstart the tree is built by the **Dashboard Folders** batch
(`dr-egeria-inbox/Dashboard Folders/LOCAL_DASHBOARDS_FOLDERS.dr-egeria.md`),
and the **Useful Dashboards** batch files its own sheets in both folders.
Run each once: `Add Member to Collection` does not de-duplicate.

## Prerequisites

- A running Egeria platform + view server you can reach (the quickstart
  demo's `qs-view-server` at `https://localhost:9443` works out of the box).
- The `dr_egeria` CLI (ships with pyegeria — `pip show pyegeria`; inside the
  `quickstart-pyegeria-web` container it's already on `PATH`).
- Know which Report Spec(s) you want on the dashboard. Browse them at
  `/egeria-explorer#report-specs`, or `GET /api/report-specs` — each one's
  `name` (or any of its `aliases`) is what a Placement's `ref` needs.

### Where `dr_egeria` writes, and where to run it

Since pyegeria 6.2.29, `Create Dashboard Sheet`, `Link Report to Dashboard
Sheet` and `Add Text on Dashboard Sheet` write each sheet **into Egeria**
(the chain described above) **and** into the local file
(`PYEGERIA_DASHBOARD_SHEETS_STORE`, default `~/.pyegeria/dashboard_sheets.json`)
on whatever machine or container runs `dr_egeria`. The local copy is kept so
the file stays a complete fallback while the move to Egeria is under way.
The command output has an **Egeria** line that says whether Egeria was
written.

- Every write is an update-or-create by name, so re-running a whole
  `.dr-egeria.md` file is safe and changes nothing that is already right.
- If Egeria cannot be reached, the command writes only the local file and
  says so. `dr_egeria --local-only` (or `PYEGERIA_DASHBOARD_SHEETS_LOCAL_ONLY=1`)
  does the same on purpose. A sheet written only to a local file shows up in
  the Portal only if that file is the one the Portal reads (see below).
- If you place a report on a sheet that is still only in the local file,
  the whole sheet is first written to Egeria, so the Egeria copy is never
  partial.
- Because the Portal reads Egeria first, it no longer matters much which
  machine you run `dr_egeria` on: any machine connected to the same Egeria
  updates the sheet the Portal shows.

The local file the Portal falls back to is the one **inside the
`quickstart-pyegeria-web` container** (`/root/.pyegeria/dashboard_sheets.json`),
bind-mounted to the host at
`runtime-volumes/quickstart-pyegeria-state/dashboard_sheets.json`.
`GET /api/local-dashboards` reports it as `storePath`. To run `dr_egeria`
inside that container:

```bash
docker cp my-dashboard.dr-egeria.md quickstart-pyegeria-web:/tmp/my-dashboard.md
docker exec quickstart-pyegeria-web dr_egeria --validate /tmp/my-dashboard.md
docker exec quickstart-pyegeria-web dr_egeria --process  /tmp/my-dashboard.md
```

**Do not `docker cp` a `dashboard_sheets.json` into the container.** It
replaces the file rather than merging it, so any sheet or placement only in
the container's copy is lost without a warning. Re-run the source
`.dr-egeria.md` files instead.

### No shell/Docker access? Run it from the browser instead

The Local Dashboards page itself has a **▶ Run Dr.Egeria Document** button
in the header. It opens a panel where you paste a full Dr.Egeria markdown
document (single command or many, same syntax as any `.dr-egeria.md` file)
and hit Validate or Process. This calls
`POST /api/dr-egeria/execute-document`
(`dr_egeria_commands_handler.py`), which runs in the same backend process
that serves this page — so it writes to Egeria and to the local file this
portal falls back to, with no "wrong machine" problem at all. On a successful
Process the page refreshes itself, so a newly-added placement shows up
immediately.

This is the recommended path for anyone without `docker exec` access; the
`docker cp`/`dr_egeria` CLI route above is equivalent and only worth using
for scripting or bulk/CI-style runs.

### Where to keep your `.dr-egeria.md` file

Put it in **`exchange-quickstart/loading-bay/dr-egeria-inbox/Local Dashboards/`**
— a shared, read-only folder that's already bind-mounted into
`quickstart-pyegeria-web` (it rides along on the existing `loading-bay`
volume; no new mount needed). The Run Dr.Egeria Document panel lists every
`.md` file there as a clickable chip — click one to load its content into
the editor, review it, then Validate/Process. This is the canonical shared
place for dashboard-definition documents: anyone with access to the repo
(or the file share behind it) can drop a file there and immediately browse
and run it from the portal, no pasting required.

`GET /api/local-dashboards/documents` lists what's there (and the exact
path it's reading, via `docsPath`, useful if the folder ever looks empty);
`GET /api/local-dashboards/documents/{filename}` returns one file's raw
content. Override the folder with `LOCAL_DASHBOARDS_DOCS_PATH` if you need
a different location.

## Step 1 — Pick a Report Spec, then create a Report from it

Every Dashboard Sheet is only as useful as what it places, and every
placement now needs a **Report**, not a bare Report Spec (see "Report vs.
Report Spec" above). Two things matter when picking the underlying spec:

1. **What output format renders best?** `Create Report`'s `Output Format`
   attribute is honored exactly as set — `REPORT` (markdown text), `TABLE`,
   `DICT`, `MERMAID` (renders as a real diagram via mermaid.js, loaded on
   this page — same as any other app in the portal), or whatever else the
   spec's `output_types` lists. This used to be silently ignored (fixed
   `REPORT`→`TABLE`→`DICT` preference, no per-placement override) — fixed
   as of 2026-07-29 once Reports gave placements somewhere to actually store
   a chosen format. For which type suits what, see
   [Which output type for which surface](report-specs.md#c1-which-output-type-for-which-surface).
2. **Does the spec need scoping to be useful?** Set `Search String` (and any
   other of the 22 execution-parameter attributes `View Report` supports —
   `Starts With`, `Metadata Element Type Name`, `Page Size`, etc.) on the
   `Create Report` command. A broad, generic spec like `Collections` run
   with no `Search String` returns *everything* (observed 80–150KB from one
   placement, before Reports existed to carry real scope) — always give a
   broad spec a real `Search String` unless you deliberately want the whole
   dataset. A tile still has render limits as a safety net, described in
   [How results look in a tile](#how-results-look-in-a-tile); a
   correctly scoped Report rarely reaches them.

Check `GET /api/report-specs` for a spec's `action.required_params`,
`optional_params` and `output_types` before authoring the Report. A param
outside the standard 22 (e.g. `Collection Members`'s collection) is set via
`Report Parameters` (added 2026-07-31) — a Dictionary attribute, keys
matching the param name exactly.

Name an element by its **qualifiedName**, not its GUID: a GUID changes when
the element is re-created (a platform reset or a re-run seed), and the tile
then reports that the collection no longer exists. `Collection Members`
takes `collection_qname` (or `collection_name`, or `collection_guid`) from
pyegeria 6.2.34:

```markdown
### Report Parameters
collection_qname: Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0
```

## Step 2 — Create the Dashboard Sheet

Write a Dr.Egeria markdown command:

```markdown
___

## Create Dashboard Sheet
> Create a Dashboard Sheet - a named, ordered, nestable layout of placed Report Specs used to compose dashboards.

### Display Name
my-team-dashboard

### Dashboard Sheet Heading
My Team Dashboard

### Dashboard Sheet Description
Whatever this dashboard is for.

___
```

One gotcha worth knowing up front:

- `Display Name` is the sheet's name. It names the sheet in Egeria
  (`Dashboard::<Display Name>`) and in the local file. It's
  also what every `Link Report to Dashboard Sheet`/`Add Text on Dashboard
  Sheet` placement's `Dashboard Sheet Name` attribute must match exactly
  (that attribute references an *existing* sheet by name; it's a different
  attribute, from the Link bundle, not the one you just set here — see Step
  3). (Changed 2026-07-31: `Create Dashboard Sheet` used to have its own
  separate `Dashboard Sheet Name` attribute alongside `Display Name` — now
  it's `Display Name` only.)
- Re-running `Create Dashboard Sheet` with the same name **upserts** — it
  updates the existing sheet rather than erroring, so it's safe to
  re-run this step while iterating on heading/description text.

Run it:

```bash
dr_egeria --validate my-team-dashboard.md   # catches typos/attribute issues, no changes made
dr_egeria --process  my-team-dashboard.md   # writes the sheet to Egeria (and the local file)
```

## Step 3 — Create a Report, then place it

Two commands per placement: `Create Report` (once per Report — reusable
across multiple Dashboard Sheets, or multiple placements on the same sheet
with different spans), then `Link Report to Dashboard Sheet`.

```markdown
___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
My Team Work Items

### Description
Work items for my team, shown on the team dashboard.

### Report Spec
Work-Item-List-DrE-Basic

### Output Format
DICT

___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
my-team-dashboard

### Report Name
My Team Work Items

### Placement Span
full

### Placement Emphasis
panel

___
```

- `Report Spec` (on `Create Report`) is the target Report Spec's `name` or
  alias (from Step 1); `Display Name` is what `Report Name` (on `Link
  Report to Dashboard Sheet`) then references.
- `Create Report` **upserts** — rerun it with the same `Display Name` to
  change its `Output Format`/`Search String`/etc., no need to delete first.
- The target Dashboard Sheet **must already exist** for the Link step —
  that command doesn't create one, and the Report referenced by `Report
  Name` must already exist too (run `Create Report` first in the same file,
  or earlier).
- Re-linking the same `Report Name` to the same sheet replaces that
  placement's span/emphasis rather than duplicating it (placements merge by
  `ref`), so you can safely re-run this while tuning layout.
- Order in the file is placement order in the dashboard.

### Analytic reports — charts and overridable parameters

Some Report Specs run an **analytic function** instead of querying Egeria
elements directly (a plain Python routine returning an already-aggregated
count/breakdown/series — see egeria-python's
`pyegeria/view/analytic_registry.py`/`analytic_demo_specs.py`, and the
"Analytic Demo - \*" specs in Egeria Explorer's Report Specs browser, which
also shows a **GENERIC**/**FIXED METRIC** badge for each: generic means what
it counts is itself a parameter, fixed means the metric is hardcoded). For
these, `Output Format: SERIES` renders a Vega-Lite line chart (time series),
`BAR`/`PIE` render a category-breakdown chart, and `Analytic Parameters` sets
that function's parameters — as **defaults**, not fixed pins, so a later
`Create Report` re-run (or a caller override) can still change them:

    ## Create Report
    ### Display Name
    Catalog Growth

    ### Report Spec
    Analytic Demo - Catalog Growth Trend

    ### Output Format
    SERIES

    ### Analytic Parameters
    window: 90d
    points: 12

(This example and the next are indented code blocks on purpose: Dr.Egeria
skips indented blocks, and the *Local Dashboards* data-initialization batch
processes the copy of this tutorial in the shared Dr.Egeria folder, so a
fenced block would create these Reports on every batch run. Remove the
four-space indent when you copy them.)

Link it exactly like any other Report (`Link Report to Dashboard Sheet`,
`Report Name: Catalog Growth`) — Local Dashboards renders the chart
automatically once the placement's `outputFormat` is `SERIES`/`BAR`/`PIE`, no
extra placement-level configuration needed.

**Analytic functions don't only render as charts.** A **GENERIC** function's
result can be shown as `DICT`/`JSON` too (a plain KPI number or a small
table), not just `SERIES`/`BAR`/`PIE` — `count_elements`, for instance,
returns a scalar `int` regardless of output format; the chart formats just
wrap the *same* result differently. Two Reports pointed at the same
`count_elements` function, retargeted at different types via `Analytic
Parameters: type_name`, is the clearest illustration of what "generic"
means:

    ## Create Report
    ### Display Name
    Project Count

    ### Report Spec
    Analytic Demo - Element Count by Type

    ### Output Format
    DICT

    ### Analytic Parameters
    type_name: Project

    ___

    ## Create Report
    ### Display Name
    Term Count

    ### Report Spec
    Analytic Demo - Element Count by Type

    ### Output Format
    DICT

    ### Analytic Parameters
    type_name: GlossaryTerm

Same Report Spec, same Python function, two different Reports — no code
change needed to count a different type. Contrast this with a **FIXED**
function like `term_definition_completeness`: its metric (share of
GlossaryTerms with a non-empty description) is hardcoded in the function
body, so its `Create Report` needs no `Analytic Parameters` at all — it's a
genuinely different function from `count_elements`, not just a different
parameter binding of the same one. See the worked example below for both
side by side.

**List-valued `Analytic Parameters` now work (fixed 2026-08-01).** Values
used to be stringified before storage (`md_processing/v2/report.py`), which
was transparent for scalars (`type_name: Project`, `window: 90d`) but broke
any parameter whose real type is a list or dict — e.g. `counts_by_type`'s
`type_map: [["Projects", "Project"], ["Terms", "GlossaryTerm"]]` used to come
back as a Python `str`, not a list, crashing the analytic function
(`not enough values to unpack`). Fixed in `md_processing/v2/report.py`
(egeria-python `PYEGERIA_ISSUES.md` ISSUE-20): each value is now JSON-decoded
back to its real type before the analytic function runs. The Assets by Type
& Location worked example below uses a list-valued `type_map` for its two
chart Reports as a live demonstration this works — if you hit the old
"not enough values to unpack" symptom, check the installed pyegeria predates
this fix.

### Adding explanatory text (no Report needed)

For section headers or captions — content that isn't backed by a Report Spec
at all — use `Add Text on Dashboard Sheet` instead of `Create Report`/`Link
Report to Dashboard Sheet`. No Report is involved: the text is held on the
sheet itself (in Egeria, as the placement's `markdownContent`), and nothing is
looked up when the page shows it:

```markdown
## Add Text on Dashboard Sheet
### Dashboard Sheet Name
<your-sheet-name>

### Placement Name
Intro Caption

### MD Content
**This sprint**

This dashboard tracks **team work items** for the current sprint.

### Placement Span
full

### Placement Emphasis
panel
```

Replace `<your-sheet-name>` with the sheet's `Display Name`. (The placeholder is
deliberate: the *Local Dashboards* data-initialization batch processes the copy
of this tutorial in the shared Dr.Egeria folder, and a sheet that does not
exist makes the command stop instead of writing to Egeria.)

Re-running with the same `Dashboard Sheet Name` + `Placement Name` updates
the text in place (same replace-by-name behavior as `Link Report to Dashboard
Sheet`'s `Report Name`), so it's safe to iterate on copy.

Two things that trip people up (both checked with `dr_egeria --validate` on
2026-11-10, pyegeria 6.2.32):

- **Write each attribute as a `###` heading with its value underneath.** The
  inline form `Dashboard Sheet Name: my-team-dashboard` is not read: validation
  fails with *Missing required attribute: 'Dashboard Sheet Name'*.
- **Inside `MD Content`, write a heading as bold text, never with `#`.** The
  value ends at the first line that starts with `###`, and that includes `####`
  and smaller headings; a line starting with `##` is read as the next command.
  `--validate` does not catch the `####` case: `--process` then fails with
  *MD Content is required* when the heading is the first line, or keeps only the
  text above it. (Checked 2026-11-11, pyegeria 6.2.34.)

## Step 4 — View it

Open `/local-dashboards` in the portal (or navigate straight to
`/local-dashboards?sheet=my-team-dashboard`). The list view shows every
sheet held in Egeria plus any sheet that is only in the local file, each
tagged **Egeria** or **local file**; the detail view resolves each
placement, runs the auto-runnable ones inline, and shows a pointer for the
rest.

To check from the command line that the sheet reached Egeria:

```bash
python -m pyegeria.view.dashboards show "my-team-dashboard"
```

If nothing shows up: check the `dr_egeria` output's **Egeria** line. If it
says Egeria was not written, the sheet is only in a local file — check that
`storePath` in `GET /api/local-dashboards`'s response matches where
`dr_egeria` wrote it, or re-run with a working Egeria connection.

### How results look in a tile

*(Portal from 2026-11-11, with pyegeria 6.2.37 or later.)*

- **Large tables scroll inside the tile.** A tall table stops at 420px and
  scrolls; a wide one scrolls sideways. The scroll bars are always visible
  and the header row stays in view. In the drill-down drawer a table stops
  at 70% of the window height. Small tables look as they always did.
- **Columns keep a readable width.** A table with five or more columns gives
  each column at least 120px rather than wrapping every few characters.
  Drag a column's edge to widen it; the table then scrolls further.
- **Line breaks and bullets in cells.** pyegeria 6.2.37 draws a list in a
  LIST table cell as bullets, one per line, and a property map as one
  `key: value` per line. The Portal shows these as line breaks. Nothing else
  in a cell is treated as HTML.
- **Nothing is cut silently.**
  - A DICT/JSON table shows up to 200 rows and 20 columns. Past that it says
    "+N more rows", and names the hidden columns: "+2 more columns:
    Glossary, Subject Area".
  - A markdown table (LIST, TABLE or REPORT output) is only ever cut at a
    whole row, after 1,000 rows (or about 1 MB). It then says "Showing the
    first N of M rows (this tile's render limit)".
  - Text outside tables (prose, a mermaid diagram) is cut at 20,000
    characters, at a line break; a half-written diagram is dropped rather
    than shown broken. The note names the placement's real scope ("This
    placement is scoped by search_string=…"), or says it has no query scope
    when that is true.
- **Capped queries.** When the query itself filled its page, a LIST or
  REPORT tile carries pyegeria's line "Showing the first 100: the query
  stopped at its page size of 100; more may exist." A DICT or TABLE tile
  does not show that note yet, so treat a round row count (100, 200) as
  "maybe more".

See [Report Specs, Part C](report-specs.md#part-c-how-a-specs-output-looks)
for what changed in pyegeria 6.2.37 and how a column can choose bullets,
names or a count.

### Deleting a Dashboard Sheet

**A sheet held in Egeria** (tagged **Egeria**) cannot be deleted in the
Portal: its 🗑 icon and "Delete Dashboard" button are greyed out, and
hovering them says how to delete it. Delete it with the command-line tool,
which is a shared write (see "Commands for sheets held in Egeria" above):

```bash
python -m pyegeria.view.dashboards delete --sheet "my-team-dashboard" --dry-run   # see what would go
python -m pyegeria.view.dashboards delete --sheet "my-team-dashboard" --local     # Egeria chain + local entry
```

**A sheet only in the local file** (tagged **local file**) can still be
deleted in the Portal: the list view has a 🗑 icon on each card and the
detail view a "Delete Dashboard" button, both behind a confirmation prompt
(`DELETE /api/local-dashboards/{name}`). You need to be signed in to use
them. This removes only the local entry.

Either way, deleting a sheet never deletes the Egeria `Report` elements its
placements show, since a Report is an independent, reusable object that may
be linked from other sheets too. If some other sheet nests the deleted one
as a Placement, that placement shows "Unresolved reference" on its next
load.

## Troubleshooting

| Symptom in the UI | Cause | Fix |
|---|---|---|
| "Unresolved reference — no matching Report or Dashboard Sheet" | `ref` (a `Report Name`) doesn't match any Report's exact `Display Name`, or any Dashboard Sheet name | Check the Report actually exists (`Create Report` ran, not just validated) and the name matches exactly — case and whitespace matter |
| "Needs parameters" / "Report has no Output Format set" note, links to Report Spec Browser | The Report's underlying spec still has required params the Report's stored `params` don't cover, or `Create Report` never had `Output Format` set | Rerun `Create Report` for that Report with the missing attributes filled in — upserts, safe to rerun |
| A `Report Parameters` key (e.g. `collection_guid`) shows "Missing" here even though `Create Report` set it and validated clean | Fixed 2026-07-31 (egeria-python `md_processing/v2/report.py`) — `Report Parameters` keys used to persist unconverted, but this page's `camelKey()` presence check assumes every stored param is camelCase (matching every other execution param) | Confirm the installed pyegeria includes this fix; if it does and this still happens, check `Create Report`'s persisted `additionalProperties` directly (`GET` the Report element) for the actual stored key casing |
| Tile renders "No results." | The Report's stored `Search String`/filters matched nothing | Expected if the underlying data doesn't exist yet — not a bug; double-check the `Search String` is actually scoped to something real |
| Analytic-function tile (e.g. `count_elements`) renders "No results." even though the count is real | Fixed 2026-07-31 (`local-dashboards.html`) — two bugs: (1) any analytic Report not rendered as `SERIES` was routed through the find-method code path, sending `search_string`/etc. that the function rejects outright; (2) even once routed correctly, a bare scalar result (`int`/`bool`) had no rendering path and fell through to the empty-table case | Confirm the installed `local-dashboards.html` includes both fixes (the placement JSON should carry `"isAnalytic": true`, and a scalar result renders as a large KPI number, not a table) |
| Analytic-function tile errors `Execution failed: <function>() got an unexpected keyword argument 'search_string'` | Same root cause as the row above, pre-fix — the analytic function was called with the standard find-vocabulary params instead of its own `Analytic Parameters` | Same fix as above |
| Tile shows a red box "THIS SPEC CANNOT RUN" with a sentence naming a check | pyegeria's load-time resolver refused the Report's spec (the sentence says which check and why). The tile does not call the server | Open the spec in the Report Spec Browser (the box links to it) and read its Resolution panel; fix the spec or pick another. See [what a report spec will do](../tools/egeria-explorer.md) |
| Tile shows a red box "THE SPEC REFUSED TO RUN (400)" | pyegeria raised an error when the tile ran: a role it needs is not supplied, or a parameter value it refuses (for example `*` over the root type) | Read the words in the box; they name the cause. Change the Report's `Search String` or parameters and re-run `Create Report` |
| Tile shows "SIGN-IN NEEDED (401)" | Egeria refused the user the tile ran as, or the token had expired | The words are `Not authorized for this operation — the current user does not have permission for this report`. Sign in again, or check the user has access to the elements the spec reads |
| A count reads "not measured" with a note under it | pyegeria could not measure it: the query failed or timed out, or a scan stopped before reading every page | Expected, and not zero. Fix the cause named in the note and refresh the tile |
| Sheet doesn't appear in the list at all | `--validate` was the last run instead of `--process`; or Egeria was not written (see the **Egeria** line of the `dr_egeria` output) and the sheet went to a local file the Portal doesn't read | Re-run with `--process` against a working Egeria connection; `python -m pyegeria.view.dashboards show NAME` confirms it is in Egeria |
| Edits to a sheet don't show, though `dr_egeria` reports `SUCCESS` | The sheet is held in Egeria (tag **Egeria**) and the run wrote only a local file (`--local-only`, or Egeria could not be reached). Egeria's copy wins | Re-run without `--local-only` once Egeria can be reached |
| Note: "Egeria could not be read, so only sheets from the local file are shown" | The Portal could not read Egeria; sheets held there are missing from the list | Fix the Egeria connection (sign in again, or check the platform) and reload |
| Note: "Chain broken in Egeria: …" | A part of the sheet's element chain is missing in Egeria (for example a `Dashboard` made with plain `Create Dashboard`) | Re-run the sheet's `.dr-egeria.md` file: every write is update-or-create, so missing parts are written again. `python -m pyegeria.view.dashboards show NAME` lists what is still missing |
| Tile shows 🔒 "Report not visible to you." (or "Report spec not visible to you.") | The Report, or the report spec held in Egeria that it names, is in a governance zone you cannot see | By design. Ask whoever owns the Report for access to its zone, or remove the zone from the Report if it should be public |
| Nested sheet placement | Currently shows an "Open nested sheet →" link, not inline rendering | By design for now — recursive inline rendering needs cycle detection first (see the Next Steps dashboard below) |
| Tile shows a huge, unrelated wall of text/diagram, or a note "This placement has no query scope…" | The Report's `Search String` is blank/unscoped against a broad spec | Rerun `Create Report` for that Report with a real `Search String` — this is exactly what the worked example's "Membership Diagram" Report demonstrates fixing |
| Note: "Text truncated at this tile's render limit … This placement is scoped by …" | The placement is scoped, but its text (outside tables) is still longer than 20,000 characters | Narrow the scope further, or choose an output type that is a table (LIST or TABLE), which is cut only at whole rows |
| Note: "Showing the first N of M rows (this tile's render limit)" | A markdown table has more than 1,000 rows (or about 1 MB) | Narrow the Report's scope; the full result is still available from `View Report` or `run_report` |
| "+N more columns: …" under a table | A DICT/JSON result has more than 20 columns | Expected; the hidden columns are named. Pick a spec, or output format, with fewer columns |
| A diagram tile shows a truncation note and no diagram | The diagram's source was longer than 20,000 characters; a half-written diagram is dropped rather than shown broken | Scope the Report more narrowly; the diagram was too large to draw usefully |
| A table cell shows `a<br>b` as text | pyegeria 6.2.37 or later with a Portal from before 2026-11-11 | Update the Portal |
| A DICT or TABLE tile shows exactly 100 or 200 rows | The query filled its page. pyegeria's "more may exist" note is in the result, but a DICT/TABLE tile does not show it yet | Narrow the Report's `Search String`, or raise its `Page Size` |

## Worked example: the "Next Steps" dashboard

> **These example sheets are now held in Egeria.** On the quickstart demo,
> `local-dashboards-next-steps`, Assets by Type and Location Demo,
> `digital-product-portfolio`, `my-team-dashboard` and the Chief Data
> Officer Dashboard were moved into Egeria on 2026-11-10 and are owned by
> `erinoverview`. The `.dr-egeria.md` files below still work: re-running one
> updates the Egeria copy (and writes a fresh local copy as the fallback).

Rather than a toy example, the shared folder's
[`LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`](https://github.com/odpi/egeria-workspaces/blob/main/exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md)
is a complete, runnable Dr.Egeria document that:

1. Creates a real **Work Item List** collection, `Local Dashboards - Next
   Steps`.
2. Creates a **Task** for each open item in this feature's own punch list
   (funnel chart wiring, nested-sheet inline rendering, chart drill-click
   parity, the Advisor dashboard editor, and the `find_method` gap on
   Dashboard Sheet commands) and adds each as a member of the Work Item
   List — split out into its own file,
   [`LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md`](https://github.com/odpi/egeria-workspaces/blob/main/exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md),
   so the work items can be recreated/re-linked without recreating the Work
   Item List or Dashboard Sheet.
3. Creates a Dashboard Sheet, `local-dashboards-next-steps`.
4. A third file,
   [`LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md`](https://github.com/odpi/egeria-workspaces/blob/main/exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md),
   creates two **Report** elements (`Create Report` — see below) and places
   them on the sheet: one showing the Work Item List's own attributes, one a
   Mermaid diagram of the list and its Task members, correctly *scoped* with
   a real `Search String` rather than matching the whole dataset.
5. A fourth file,
   [`LOCAL_DASHBOARDS_ANALYTICS_DEMO.dr-egeria.md`](https://github.com/odpi/egeria-workspaces/blob/main/exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_ANALYTICS_DEMO.dr-egeria.md),
   adds three more Reports demonstrating **analytic-function-backed** Report
   Specs (see "Analytic reports" above): `Project Count` and `Term Count`
   both run the same **GENERIC** `count_elements` function retargeted at two
   different types via `Analytic Parameters`, and `Term Definition
   Completeness` runs a genuinely different, **FIXED** function that's
   inherently Term-specific. Building this surfaced two real bugs, both
   fixed as part of adding it: `local-dashboards.html` was routing any
   non-`SERIES` analytic Report through the find-method code path instead of
   sending its `Analytic Parameters` (fixed via a new `isAnalytic` flag from
   the backend, not an `outputFormat === 'SERIES'` guess), and a scalar
   analytic result (a bare `int`/`bool`, e.g. `count_elements`'s count) had
   no rendering path at all and silently showed "No results." (fixed with a
   dedicated KPI-number renderer). A third issue found at the same time —
   list-valued `Analytic Parameters` — was a genuine pyegeria gap when this
   file was built; fixed since (2026-08-01, see the callout above) — the
   Assets by Type & Location example below relies on that fix for its
   `type_map`-parameterized charts.

## Worked example: "Assets by Type & Location"

A second, **standalone** worked example — it doesn't extend the "Next
Steps" dashboard above, it builds a complete dashboard from scratch in one
file,
[`LOCAL_DASHBOARDS_ASSETS_BY_TYPE_LOCATION_DEMO.dr-egeria.md`](https://github.com/odpi/egeria-workspaces/blob/main/exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_ASSETS_BY_TYPE_LOCATION_DEMO.dr-egeria.md).
Built to answer "how many assets, of which type, are cataloged, and where
are they" with a mix of techniques on one dashboard:

- Two **KPI** tiles (`Total Cataloged Assets`, `Total Locations Tracked`) —
  the same **GENERIC** `count_elements` function as the Analytics Demo
  above, retargeted at `Asset` and `Location` this time.
- Two **chart** tiles, `PIE` and `BAR`, both running `counts_by_type` with
  the *same* list-valued `type_map` `Analytic Parameters` — the live proof
  that the "list-valued Analytic Parameters" gap above is actually fixed,
  not just a doc claim.
- One **text/snapshot** panel, `Assets by Location` — the interesting case.
  There's no live analytic function or Report Spec that groups assets by
  Location today (unlike by-type, which reuses `counts_by_type`), so this
  panel is a hand-built Mermaid pie chart + markdown table, computed from
  real `/api/locations` data at authoring time via `Add Text on Dashboard
  Sheet` — a real answer, but a **snapshot**, not something that
  re-queries on every future dashboard visit like the four Report tiles
  above do. The file's own commentary on that step spells out what a live
  version would need: either a new registered analytic function (the same
  shape as `sum_type_counts`, BACKLOG.md NEXT-18, but grouping by
  `AssetLocation`-linked `Location` instead of by type), or a **Saved
  Query** (`Create Saved Query`/`Link Saved Query to Results Set` already
  exist as commands in this same Report family — worth evaluating for
  exactly this case; [Create and Use Saved Queries](saved-queries.md)
  shows how to put a saved query's results on a dashboard) — either of which
  could then also become the Pie
  Chart tile's drill-down target via `Placement Detail Spec` (see
  "Perspectives and drill-down" below) instead of sitting beside it as a
  separate panel.

This file also demonstrates `Placement Emphasis: kpi` genuinely rendering
as a compact tile (BACKLOG.md NEXT-20) — decided from each placement's
actual result shape once it resolves, not just the static attribute, so a
KPI-emphasis placement that happened to return something large would still
render in full rather than being squeezed into a tiny tile.

## Worked example: the CDO sheet's register tiles

Mandy's sheet **Chief Data Officer Dashboard** (heading *How the Data
Governance Program is Going*, from
`coco-workbooks/0. data-governance-program/chief-data-officer-dashboard.md`)
ends with three registers. Each is a `LIST` Report scoped by a
`Search String`:

| Tile | Report Spec | Search String |
|---|---|---|
| My Ninety Day Plan Progress | `Project-DrE-Basic` | `JulesKeeper::` |
| Company Risk Register | `Risk-DrE-Basic` | `CocoPharma::Risk::` |
| Governance Metric Register | `Governance-Metric-DrE-Basic` | `CocoPharma::GovernanceMetric::` |

```markdown
## Create Report

### Display Name
Governance Metric Register

### Report Spec
Governance-Metric-DrE-Basic

### Output Format
LIST

### Search String
CocoPharma::GovernanceMetric::
```

What they show with pyegeria 6.2.37 and the Portal from 2026-11-11 (checked
on the quickstart on 2026-11-11):

- **All rows.** The Governance Metric Register's LIST answer is 46 rows and
  84 KB of markdown. It used to be cut at 20,000 characters, part-way
  through a row, so the tile showed 12 of the 46, followed by a note saying
  the placement had no query scope (it has one). Now all 46 rows show, in a
  table that scrolls inside the tile, with no note.
- **Lists as bullets.** *Implications* and *Outcomes* are lists. They used
  to be one comma-joined string, so the boundary between two items and a
  comma inside a sentence looked the same. pyegeria 6.2.37 puts each item
  on its own line, and the Portal shows the breaks. Long descriptions wrap
  within their column.
- **Readable columns.** With 21 columns, the table keeps each one at least
  120px wide and scrolls sideways; *Measurement* and *Target*, the two
  columns a metric register exists for, are reached by scrolling, not
  hidden.

Screenshots of these tiles will be added once the quickstart's data has been
re-seeded.

## Perspectives and drill-down

Two more `Link Report to Dashboard Sheet` / `Add Text on Dashboard Sheet`
attributes exist beyond `Placement Span`/`Placement Emphasis`, neither used
in the worked examples above (both dashboards predate them or didn't need
them) — added BACKLOG.md NEXT-19/NEXT-21:

- **`Placement Perspectives`** — a comma-separated list of viewer-role tags
  (`governance, steward, owner, consumer, engineer, builder, privacy,
  community` — the same vocabulary `egeria-overview.html`'s own perspective
  picker uses). Available on both `Link Report to Dashboard Sheet` and `Add
  Text on Dashboard Sheet`. Leave it unset (the default) and the placement
  shows for every perspective, fail-open — it's an opt-in narrowing, not an
  opt-in visibility switch. The Local Dashboards detail page has a
  perspective picker in its header (`?perspective=` in the URL) that
  filters+keeps-order server-side against this tag.
- **`Placement Detail Spec`** — `Link Report to Dashboard Sheet` only (a
  text placement has no result to drill into). Names another Report Spec to
  run as a drill-down when the viewer clicks the placement's "↗" button —
  a slide-out drawer, same mechanics as `egeria-overview.html`'s own
  drill-down, adapted since Local Dashboards placements are arbitrary
  user-authored Reports rather than a fixed, hand-authored set of drill
  targets. The drill-down reuses whatever parameters produced the
  placement's own result (including any viewer override, see below), not
  an unscoped run of the target spec.

```markdown
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
<your-sheet-name>

### Report Name
Governance Coverage

### Placement Perspectives
governance, steward

### Placement Detail Spec
Collection Members
```

Replace `<your-sheet-name>` with your sheet's `Display Name` (the placeholder
makes the copy of this tutorial that the data-initialization batch processes
stop with "Dashboard Sheet … does not exist" instead of writing).

**Viewer-facing parameter overrides (no Dr.Egeria command needed).**
Independent of both attributes above: anyone looking at a Local Dashboard
can click the "⚙" button next to a placement's heading to open an inline
panel — an `Output Format` dropdown plus one field per parameter the
Report already carries — edit it, click Run, and that one placement
re-executes with the override for their current view (transient; resets on
reload/navigate away, never written back to the Report). This is
BACKLOG.md NEXT-14 Phase 1 — the *viewer's* way to tailor a placement
per-use, distinct from `Create Report`'s author-time defaults above. A
future Phase 2 (not built yet) would let a viewer persist their tailoring
as their own version of the dashboard.

All five files live in the shared **Local Dashboards** folder (see "Where
to keep your `.dr-egeria.md` file" above) — load any of them straight from
the Run Dr.Egeria Document panel's file chips, or run via the CLI the same
way as any Dr.Egeria document:

```bash
dr_egeria --validate LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md
dr_egeria --process  LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md
```

Then open `/local-dashboards?sheet=local-dashboards-next-steps` — the
dashboard itself **is** this feature's remaining to-do list, live from
Egeria. Add a Task and re-run `Add Member to Collection` for it, and the
dashboard picks it up on next load — no code change needed. For the
standalone Assets by Type & Location example instead, run
`LOCAL_DASHBOARDS_ASSETS_BY_TYPE_LOCATION_DEMO.dr-egeria.md` the same way
and open `/local-dashboards?sheet=Assets%20by%20Type%20and%20Location%20Demo`.

### Why a Work Item List instead of free text

This tutorial's "Adding explanatory text" section above shows `Add Text on
Dashboard Sheet` does give you a "just show this paragraph" placement kind
now — it didn't when this worked example was first built, which is why the
"Next Steps" punch list is modeled as a real Work Item List instead (kept
this way deliberately, not stale — see below for why that's still the
better choice for *this specific* content). Modeling it as a real **Work
Item List** of **Tasks** means it's not just readable on this one
dashboard: it's also a normal Egeria collection, visible in Egeria Explorer,
queryable by anything else that understands Projects/Tasks, and something a
teammate can add to with their own Dr.Egeria commands or find via search —
one write, several consumers, which is the whole point of putting it in
Egeria rather than a markdown checklist that only this file knows about. Use
`Add Text on Dashboard Sheet` for genuinely static captions/section headers
(as the Assets by Type & Location worked example below does for its Location
snapshot); reach for a real Egeria collection like this one when the content
is itself worth having as queryable, cross-referenceable metadata, not just
dashboard decoration.
