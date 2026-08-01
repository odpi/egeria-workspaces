<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Tutorial: Create and Implement a New Local Dashboard

This is a step-by-step guide to authoring a **Dashboard Sheet** with
Dr.Egeria and getting it live in the **Local Dashboards** portal app
(`/local-dashboards`). It ends with a real, worked example — a dashboard
that lists the outstanding "next steps" for this very feature, tracked as
actual Egeria Work Items rather than a paragraph of prose.

See also: [`OVERVIEW_REPORTING_MODEL.md`](OVERVIEW_REPORTING_MODEL.md) §10
for the design history and open decisions (Dashboard Sheet → Egeria
Collection subtype migration, generic execution engine), and
[`BACKLOG.md`](../../../BACKLOG.md) NEXT-10 for where this fits in the
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
header, no Egeria element at all), plus two layout hints:
`span` (`"1"` / `"2"` / `"full"`, how wide the tile is) and `emphasis`
(`"kpi"` compact vs `"panel"` larger/detailed). Dashboard Sheets themselves
still live in a local JSON file (`~/.pyegeria/dashboard_sheets.json` by
default, override with `PYEGERIA_DASHBOARD_SHEETS_STORE`) — they are **not
yet** Egeria elements (that's planned; see the design doc) — but as of
2026-07-29 a Placement's target *is* a real element, resolved with a live
Egeria lookup, not a local-registry-only reference. Local Dashboards is the
portal app that lists and renders Dashboard Sheets.

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

## Prerequisites

- A running Egeria platform + view server you can reach (the quickstart
  demo's `qs-view-server` at `https://localhost:9443` works out of the box).
- The `dr_egeria` CLI (ships with pyegeria — `pip show pyegeria`; inside the
  `quickstart-pyegeria-web` container it's already on `PATH`).
- Know which Report Spec(s) you want on the dashboard. Browse them at
  `/egeria-explorer#report-specs`, or `GET /api/report-specs` — each one's
  `name` (or any of its `aliases`) is what a Placement's `ref` needs.

### Where `dr_egeria` has to run — this is the #1 gotcha

`Create Dashboard Sheet` and `Link Report to Dashboard Sheet` don't write to
Egeria — they write to a **local JSON file** on whatever machine/container
runs `dr_egeria` (`PYEGERIA_DASHBOARD_SHEETS_STORE`, default
`~/.pyegeria/dashboard_sheets.json`). The Local Dashboards portal app only
ever reads the copy of that file **inside the running
`quickstart-pyegeria-web` container** (`/root/.pyegeria/dashboard_sheets.json`)
— that path is *not* bind-mounted to the host.

So if you run `dr_egeria` on your own machine (your laptop's `~/.pyegeria/`),
the run succeeds, but it writes to a completely different file the portal
never sees — the dashboard looks unchanged even though `dr_egeria` reported
`SUCCESS`. There's no error to catch this; the file paths just quietly
don't match.

**Always run it inside the container** that's actually serving the portal:

```bash
docker cp my-dashboard.dr-egeria.md quickstart-pyegeria-web:/tmp/my-dashboard.md
docker exec quickstart-pyegeria-web dr_egeria --validate /tmp/my-dashboard.md
docker exec quickstart-pyegeria-web dr_egeria --process  /tmp/my-dashboard.md
```

If you edit an existing sheet's `.dr-egeria.md` file in the repo and rerun
it this way, `Create` commands upsert and placements merge by `ref`, so
it's always safe to rerun the whole file — no need to hand-pick just the
new commands. If you want to sanity-check which file the running portal is
actually reading before or after a run, `GET /api/local-dashboards`'s
`storePath` field tells you.

**Caveat as of 2026-07-29**: `Create Report` and the updated `Link Report to
Dashboard Sheet` (`Report Name`, not `Report Spec`) only exist in the
egeria-python dev checkout's own `.venv` so far, not yet in a pyegeria
release published to PyPI — so they aren't available via `docker exec
quickstart-pyegeria-web dr_egeria ...` (that container's installed pyegeria
predates them) until the next release lands. Until then, run those two
commands from `egeria-python`'s own `.venv` (`source .venv/bin/activate`,
same host/container distinction applies to *that* run too), then `docker cp`
the resulting `~/.pyegeria/dashboard_sheets.json` into the container
afterward. `Create Dashboard Sheet` and the original `Link Report to
Dashboard Sheet` (pre-cutover) both still work fine via `docker exec` as
described above — only the two Report-related commands need this extra
step for now.

### No shell/Docker access? Run it from the browser instead

The Local Dashboards page itself has a **▶ Run Dr.Egeria Document** button
in the header. It opens a panel where you paste a full Dr.Egeria markdown
document (single command or many, same syntax as any `.dr-egeria.md` file)
and hit Validate or Process. This calls
`POST /api/dr-egeria/execute-document`
(`dr_egeria_commands_handler.py`), which runs in the same backend process
that serves this page — so it always writes to the store this portal reads,
sidestepping the "wrong machine" problem above entirely. On a successful
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
   a chosen format.
2. **Does the spec need scoping to be useful?** Set `Search String` (and any
   other of the 22 execution-parameter attributes `View Report` supports —
   `Starts With`, `Metadata Element Type Name`, `Page Size`, etc.) on the
   `Create Report` command. A broad, generic spec like `Collections` run
   with no `Search String` returns *everything* (observed 80–150KB from one
   placement, before Reports existed to carry real scope) — always give a
   broad spec a real `Search String` unless you deliberately want the whole
   dataset. Rendered content is still capped at 20,000 characters as a
   defense-in-depth safety net regardless (you'll see a
   "*(truncated...)*" note if you hit it), but a correctly-scoped Report
   shouldn't come close to that.

Check `GET /api/report-specs` for a spec's `action.required_params` and
`output_types` before authoring the Report. If `required_params` lists
something outside the standard 22 (e.g. `Collection Members`'s
`collection_guid`), set it via `Report Parameters` (added 2026-07-31) —
a Dictionary attribute, keys matching the required param name exactly:

```markdown
### Report Parameters
collection_guid: 0affb580-fa81-4d00-9438-b26faf11845d
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

- `Display Name` is what the processor keys the local JSON store on — it's
  also what every `Link Report to Dashboard Sheet`/`Add Text on Dashboard
  Sheet` placement's `Dashboard Sheet Name` attribute must match exactly
  (that attribute references an *existing* sheet by name; it's a different
  attribute, from the Link bundle, not the one you just set here — see Step
  3). (Changed 2026-07-31: `Create Dashboard Sheet` used to have its own
  separate `Dashboard Sheet Name` attribute alongside `Display Name` — now
  it's `Display Name` only.)
- Re-running `Create Dashboard Sheet` with the same name **upserts** — it
  merges into the existing record rather than erroring, so it's safe to
  re-run this step while iterating on heading/description text.

Run it:

```bash
dr_egeria --validate my-team-dashboard.md   # catches typos/attribute issues, no changes made
dr_egeria --process  my-team-dashboard.md   # writes to the local JSON store
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

```markdown
## Create Report
Display Name: Catalog Growth
Report Spec: Analytic Demo - Catalog Growth Trend
Output Format: SERIES
Analytic Parameters:
  window: 90d
  points: 12
```

Link it exactly like any other Report (`Link Report to Dashboard Sheet`,
`Report Name: Catalog Growth`) — Local Dashboards renders the chart
automatically once the placement's `outputFormat` is `SERIES`/`BAR`/`PIE`, no
extra placement-level configuration needed.

### Adding explanatory text (no Report needed)

For section headers or captions — content that isn't backed by a Report Spec
at all — use `Add Text on Dashboard Sheet` instead of `Create Report`/`Link
Report to Dashboard Sheet`. It writes straight to the Placement (no Egeria
element, no live lookup when rendering):

```markdown
## Add Text on Dashboard Sheet
Dashboard Sheet Name: my-team-dashboard
Placement Name: Intro Caption
MD Content: This dashboard tracks **team work items** for the current sprint.
Placement Span: full
Placement Emphasis: panel
```

Re-running with the same `Dashboard Sheet Name` + `Placement Name` updates
the text in place (same replace-by-name behavior as `Link Report to Dashboard
Sheet`'s `Report Name`), so it's safe to iterate on copy.

## Step 4 — View it

Open `/local-dashboards` in the portal (or navigate straight to
`/local-dashboards?sheet=my-team-dashboard`). The list view shows every
sheet in the store; the detail view resolves each placement, runs the
auto-runnable ones inline, and shows a pointer for the rest.

If nothing shows up: check `storePath` in `GET /api/local-dashboards`'s
response matches where `dr_egeria` actually wrote (same
`PYEGERIA_DASHBOARD_SHEETS_STORE` env var, same container/host).

## Troubleshooting

| Symptom in the UI | Cause | Fix |
|---|---|---|
| "Unresolved reference — no matching Report or Dashboard Sheet" | `ref` (a `Report Name`) doesn't match any Report's exact `Display Name`, or any Dashboard Sheet name | Check the Report actually exists (`Create Report` ran, not just validated) and the name matches exactly — case and whitespace matter |
| "Needs parameters" / "Report has no Output Format set" note, links to Report Spec Browser | The Report's underlying spec still has required params the Report's stored `params` don't cover, or `Create Report` never had `Output Format` set | Rerun `Create Report` for that Report with the missing attributes filled in — upserts, safe to rerun |
| A `Report Parameters` key (e.g. `collection_guid`) shows "Missing" here even though `Create Report` set it and validated clean | Fixed 2026-07-31 (egeria-python `md_processing/v2/report.py`) — `Report Parameters` keys used to persist unconverted, but this page's `camelKey()` presence check assumes every stored param is camelCase (matching every other execution param) | Confirm the installed pyegeria includes this fix; if it does and this still happens, check `Create Report`'s persisted `additionalProperties` directly (`GET` the Report element) for the actual stored key casing |
| Tile renders "No results." | The Report's stored `Search String`/filters matched nothing | Expected if the underlying data doesn't exist yet — not a bug; double-check the `Search String` is actually scoped to something real |
| Sheet doesn't appear in the list at all | Wrong store path, or `--validate` was the last run instead of `--process` | Compare `storePath` from `GET /api/local-dashboards` against your `PYEGERIA_DASHBOARD_SHEETS_STORE`; re-run with `--process` |
| `dr_egeria` reports `SUCCESS` but the dashboard doesn't change at all — new/edited placement never shows up | Either ran on the wrong machine (host instead of inside `quickstart-pyegeria-web` — see "Where `dr_egeria` has to run" above), or `Create Report`/the updated `Link Report to Dashboard Sheet` aren't in the pyegeria version that machine has installed yet | Re-run via `docker exec quickstart-pyegeria-web dr_egeria --process ...` once those commands are in a published pyegeria release; until then, run from the egeria-python dev checkout's own `.venv` and `docker cp` the resulting `~/.pyegeria/dashboard_sheets.json` into the container afterward |
| Nested sheet placement | Currently shows an "Open nested sheet →" link, not inline rendering | By design for now — recursive inline rendering needs cycle detection first (see the Next Steps dashboard below) |
| Tile shows a huge, unrelated wall of text/diagram, or a "*(truncated...)*" note | The Report's `Search String` is blank/unscoped against a broad spec | Rerun `Create Report` for that Report with a real `Search String` — this is exactly what the worked example's "Membership Diagram" Report demonstrates fixing |
| Diagram doesn't render, raw ` ```mermaid ` text shows instead | Content was truncated mid-diagram by the 20,000-character cap, so the fence never closes | The diagram was too large to render at all; same underlying scoping gap as above |

## Worked example: the "Next Steps" dashboard

Rather than a toy example, the shared folder's
[`LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`](../../../exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md)
is a complete, runnable Dr.Egeria document that:

1. Creates a real **Work Item List** collection, `Local Dashboards - Next
   Steps`.
2. Creates a **Task** for each open item in this feature's own punch list
   (funnel chart wiring, nested-sheet inline rendering, chart drill-click
   parity, the Advisor dashboard editor, and the `find_method` gap on
   Dashboard Sheet commands) and adds each as a member of the Work Item
   List — split out into its own file,
   [`LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md`](../../../exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md),
   so the work items can be recreated/re-linked without recreating the Work
   Item List or Dashboard Sheet.
3. Creates a Dashboard Sheet, `local-dashboards-next-steps`.
4. A third file,
   [`LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md`](../../../exchange-quickstart/loading-bay/dr-egeria-inbox/Local%20Dashboards/LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md),
   creates two **Report** elements (`Create Report` — see below) and places
   them on the sheet: one showing the Work Item List's own attributes, one a
   Mermaid diagram of the list and its Task members, correctly *scoped* with
   a real `Search String` rather than matching the whole dataset.

All three files live in the shared **Local Dashboards** folder (see "Where
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
dashboard picks it up on next load — no code change needed.

### Why a Work Item List instead of free text

Dashboard Sheet placements can only be Reports or nested sheets — there
is no "just show this paragraph" placement kind (deliberately: the model
mirrors report tiles, not a wiki). Modeling the punch list as a real
**Work Item List** of **Tasks** means it's not just readable on this one
dashboard: it's also a normal Egeria collection, visible in Egeria Explorer,
queryable by anything else that understands Projects/Tasks, and something a
teammate can add to with their own Dr.Egeria commands or find via search —
one write, several consumers, which is the whole point of putting it in
Egeria rather than a markdown checklist that only this file knows about.
