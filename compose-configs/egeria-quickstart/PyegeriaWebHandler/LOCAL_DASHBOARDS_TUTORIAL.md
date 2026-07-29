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
Placement is a `ref` (a name or alias) that resolves to either a **Report
Spec** — a `FormatSet` from pyegeria's report registry, the same specs you
can browse and run one-at-a-time in Egeria Explorer's Report Spec Browser —
or another Dashboard Sheet (nesting), plus two layout hints: `span`
(`"1"` / `"2"` / `"full"`, how wide the tile is) and `emphasis`
(`"kpi"` compact vs `"panel"` larger/detailed). Dashboard Sheets live in a
local JSON file (`~/.pyegeria/dashboard_sheets.json` by default, override
with `PYEGERIA_DASHBOARD_SHEETS_STORE`) — they are **not yet** Egeria
elements themselves (that's planned; see the design doc). Local Dashboards
is the portal app that lists and renders them.

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

## Step 1 — Pick your Report Specs

Every Dashboard Sheet is only as useful as what it places. Two things
matter about a candidate Report Spec:

1. **Does it need required parameters?** Local Dashboards auto-runs a
   placement only if its Report Spec has **no required parameters**, or
   exactly one and it's `search_string` (the common Dr.Egeria "find"
   convention — an empty string means "match everything, capped", not
   "match nothing"). Anything else shows a "Needs parameters" note with a
   link to the full Report Spec Browser instead of guessing values.
2. **What output format renders best?** Local Dashboards prefers `REPORT`
   (markdown text) over `TABLE` over `DICT`/whatever's first available —
   same preference order as Egeria Explorer's own report runner.

You can check both from `GET /api/report-specs`: look at `action.
required_params` and `output_types`.

## Step 2 — Create the Dashboard Sheet

Write a Dr.Egeria markdown command:

```markdown
___

## Create Dashboard Sheet
> Create a Dashboard Sheet - a named, ordered, nestable layout of placed Report Specs used to compose dashboards.

### Display Name
my-team-dashboard

### Dashboard Sheet Name
my-team-dashboard

### Dashboard Sheet Heading
My Team Dashboard

### Dashboard Sheet Description
Whatever this dashboard is for.

___
```

Two gotchas worth knowing up front:

- **Both `Display Name` and `Dashboard Sheet Name` are required**, and in
  practice you want them equal. `Display Name` satisfies validation
  (Dashboard Sheet's bundle inherits Collection Base's required-attribute
  check); `Dashboard Sheet Name` is what the processor actually keys the
  local JSON store on and what every `Link Report to Dashboard Sheet`
  placement's `Dashboard Sheet Name` must match.
- Re-running `Create Dashboard Sheet` with the same name **upserts** — it
  merges into the existing record rather than erroring, so it's safe to
  re-run this step while iterating on heading/description text.

Run it:

```bash
dr_egeria --validate my-team-dashboard.md   # catches typos/attribute issues, no changes made
dr_egeria --process  my-team-dashboard.md   # writes to the local JSON store
```

## Step 3 — Place Report Specs on it

One `Link Report to Dashboard Sheet` command per placement:

```markdown
___

## Link Report to Dashboard Sheet
> Link a Report Spec (placement) into a Dashboard Sheet.

### Dashboard Sheet Name
my-team-dashboard

### Report Spec
Work-Item-List-DrE-Basic

### Placement Span
full

### Placement Emphasis
panel

___
```

- `Report Spec` is the target Report Spec's `name` or alias (from Step 1).
- The target Dashboard Sheet **must already exist** — this command doesn't
  create one.
- Re-linking the same `Report Spec` ref to the same sheet replaces that
  placement's span/emphasis rather than duplicating it (placements merge by
  `ref`), so you can safely re-run this while tuning layout.
- Order in the file is placement order in the dashboard.

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
| "Unresolved reference — no matching Report Spec or Dashboard Sheet" | `ref` doesn't match any Report Spec name/alias or Dashboard Sheet name | Check `GET /api/report-specs` for the exact name; typos and case matter |
| "Needs parameters: X" | The spec's `action.required_params` has something other than just `search_string` | Follow the "open in Report Spec Browser" link to run it with real params, or pick a different spec for the dashboard |
| Tile renders "No results." | Auto-fill ran (`search_string=""`) but the query found nothing | Expected if the underlying data doesn't exist yet — not a bug |
| Sheet doesn't appear in the list at all | Wrong store path, or `--validate` was the last run instead of `--process` | Compare `storePath` from `GET /api/local-dashboards` against your `PYEGERIA_DASHBOARD_SHEETS_STORE`; re-run with `--process` |
| `dr_egeria` reports `SUCCESS` but the dashboard doesn't change at all — new/edited placement never shows up | Ran `dr_egeria` on the wrong machine — most likely your host instead of inside `quickstart-pyegeria-web` (see "Where `dr_egeria` has to run" above) | Re-run via `docker exec quickstart-pyegeria-web dr_egeria --process ...`; it's safe to rerun the whole file |
| Nested sheet placement | Currently shows an "Open nested sheet →" link, not inline rendering | By design for now — recursive inline rendering needs cycle detection first (see the Next Steps dashboard below) |

## Worked example: the "Next Steps" dashboard

Rather than a toy example, [`LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md`](LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md)
in this directory is a complete, runnable Dr.Egeria document that:

1. Creates a real **Work Item List** collection, `Local Dashboards - Next
   Steps`.
2. Creates a **Task** for each open item in this feature's own punch list
   (funnel chart wiring, nested-sheet inline rendering, chart drill-click
   parity, the Advisor dashboard editor, and the `find_method` gap on
   Dashboard Sheet commands) and adds each as a member of the Work Item
   List.
3. Creates a Dashboard Sheet, `local-dashboards-next-steps`, and places the
   auto-generated `Work-Item-List-DrE-Basic` report spec on it (span
   `full`, emphasis `panel`).

Run it the same way as any Dr.Egeria document:

```bash
dr_egeria --validate LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md
dr_egeria --process  LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md
```

Then open `/local-dashboards?sheet=local-dashboards-next-steps` — the
dashboard itself **is** this feature's remaining to-do list, live from
Egeria. Add a Task and re-run `Add Member to Collection` for it, and the
dashboard picks it up on next load — no code change needed.

### Why a Work Item List instead of free text

Dashboard Sheet placements can only be Report Specs or nested sheets — there
is no "just show this paragraph" placement kind (deliberately: the model
mirrors report tiles, not a wiki). Modeling the punch list as a real
**Work Item List** of **Tasks** means it's not just readable on this one
dashboard: it's also a normal Egeria collection, visible in Egeria Explorer,
queryable by anything else that understands Projects/Tasks, and something a
teammate can add to with their own Dr.Egeria commands or find via search —
one write, several consumers, which is the whole point of putting it in
Egeria rather than a markdown checklist that only this file knows about.
