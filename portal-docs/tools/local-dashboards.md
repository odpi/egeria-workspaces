# Local Dashboards

Local Dashboards renders **Dashboard Sheets** — named, ordered pages of report output, authored entirely through Dr.Egeria markdown, no code required. Each Dashboard Sheet is a list of **Placements**, and each Placement points at either a real Egeria **Report** asset (a saved query + output format, resolved live against Egeria every time the sheet loads) or another Dashboard Sheet, so pages can nest.

Access it from the portal tile (🗂️ Local Dashboards) or directly at `/local-dashboards`.

Local Dashboards is part of the quickstart Portal; freshstart does not have it.

**Who sees what.** Each report on a sheet is read as the person viewing it. A Report (or the Egeria-held report spec it names) in a governance zone you cannot see shows as a dashed tile reading 🔒 *Report not visible to you.*; the rest of the sheet still shows. See [Who sees what](../tutorials/local-dashboards.md#who-sees-what-zones-and-the-not-visible-to-you-tile).

---

## Browsing sheets

The landing page lists the Dashboard Sheets held in Egeria **in the Portal's dashboard folder** (`DashboardFolder::Consumer::Portal`, set by `PYEGERIA_DASHBOARD_FOLDERS`), plus any sheet still only in the Portal's local file. Each card carries a small tag saying where the sheet is held, **Egeria** or **local file**, and a **Used by** row naming every tool whose folder holds the sheet (for example *Egeria Advisor*, *Portal*). The **Source** and **Used by** filters narrow the list. A sheet whose tools could not be read says *not read*, never *none*; a sheet outside the folder still opens by name (`/local-dashboards?sheet=NAME`). See [dashboard folders](../tutorials/local-dashboards.md#which-tools-show-a-sheet-dashboard-folders-and-used-by).

Selecting a sheet renders its Placements in order — each Report placement runs live against Egeria and renders the result inline (table, chart, or whatever the underlying Report Spec produces); a nested Dashboard Sheet placement renders that sheet inline too.

Because Report placements resolve live, a sheet always reflects Egeria's current state — there's no separate "refresh the dashboard" step, and no stale cached snapshot to worry about.

---

## How results are drawn

- **Tables scroll inside their tile** (420px high; 70% of the window in the drill-down drawer), with always-visible scroll bars and a header row that stays in view. Wide tables keep each column at least 120px and scroll sideways; column edges can be dragged.
- **Cells can hold several lines.** pyegeria 6.2.37 puts each list item, and each `key: value` pair, on its own line in a LIST table cell (`<br>`). The Portal shows these as line breaks; nothing else in a cell is treated as HTML.
- **Caps are always stated, never silent.**
  - A DICT/JSON table shows up to 200 rows and 20 columns, then "+N more rows" and "+N more columns: *names*".
  - A markdown table is cut only at a whole row, after 1,000 rows: "Showing the first N of M rows (this tile's render limit)".
  - Text outside tables is cut at 20,000 characters, and the note names the placement's actual scope (or says it has none).
- **A query that filled its page** says "more may exist" in LIST and REPORT tiles. DICT and TABLE tiles do not show that note yet.

Details and the worked example (the CDO sheet's registers): [How results look in a tile](../tutorials/local-dashboards.md#how-results-look-in-a-tile). For choosing an output type: [Report Specs, Part C](../tutorials/report-specs.md#part-c-how-a-specs-output-looks).

---

## Authoring a new dashboard

Dashboard Sheets are built entirely with Dr.Egeria commands — `Create Dashboard Sheet`, `Link Report to Dashboard Sheet`, `Add Text on Dashboard Sheet` — the same markdown-document workflow used everywhere else in the Portal. There's no separate dashboard-builder UI; you write a `.md` document and process it.

For worked examples, see the [Tutorials](../tutorials/overview.md):
- [Building a Local Dashboard](../tutorials/local-dashboards.md) — A technical, step-by-step guide to authoring and implementing a new dashboard.
- [Digital Product & Subscription Dashboard](../tutorials/digital-product-subscription.md) — A business-oriented scenario showing how to track Data Product adoption and historic growth trends.
- [Create and Use Saved Queries](../tutorials/saved-queries.md) — How to save a query in the [Query tool](egeria-insights.md), refresh it, and show its results on a dashboard.

---

## Resource Explorer's Curation Coverage tile

The report spec **Resource Explorer - Curation Coverage** can be placed on a sheet like any other. For one database known to [Resource Explorer](resource-explorer.md), it shows how many of its schemas are **published** and how many are **not yet published** (undecided, chosen but not published, or left out), with the tables and reports behind them. Use the `BAR` output format for a chart, or `DICT` for the detail. Pass the resource as the `slug` parameter, for example `localhost_docker_coco_pharma`.

- The Portal does not compute these numbers. It asks Resource Explorer, which runs the Analytic Library's `curation_coverage` routine, and shows RE's answer unchanged.
- RE runs it **as you**. The sheet sends the persona you picked in this browser; the Portal signs you in to RE with it and keeps RE's session on the server. **Without a persona the tile says "choose a persona to see this"** and doesn't call RE at all.
- When RE is not running, refuses the sign-in, or answers with an error, the tile says **not established** and gives the reason. It never shows zeros it did not measure.
- The Portal finds RE at `RESOURCE_EXPLORER_API_URL`, default `http://host.docker.internal:8813`.

---

## When a placement cannot run, or refuses

A Report placement is checked against pyegeria's load-time resolution before it runs:

- **The spec cannot run** (the resolver refused it at load). The tile does not call the server. It shows a box labelled **THIS SPEC CANNOT RUN** with the resolver's own words and a link, *open in Report Spec Browser →*, to the spec's Resolution panel in the [Egeria Explorer](egeria-explorer.md). It would only fail, once per refresh.
- **The spec is not resolved** (pyegeria did not report on it). The tile runs as before.
- **The run is refused.** A non-2xx answer shows the server's words verbatim in a box labelled by the status: *THE SPEC REFUSED TO RUN (400)*, *SIGN-IN NEEDED (401)*, *TIMED OUT (504)* or *SERVER ERROR (500)*. A tile is never left blank.
- **A figure was not measured.** The tile says **not measured** and lists the note; it does not show `0`.
- **BINDERS IGNORED.** A placement whose spec still carries the removed `analytic_binders` key is tagged. Declare those arguments as the routine's inputs instead.

On the quickstart on 2026-11-09 all 20 Report placements across the five sheets resolved as runnable, so none showed a refusal.

**Who runs it.** Each run sends the persona chosen in this browser (so a routine that declares the `viewer` role knows who is looking). The clients use the server's service user: the browser does not yet send an Egeria token. See [what the Portal supplies](egeria-explorer.md) (section *Reports: what a report spec will do*).

---

## Where the data lives

*(Updated 2026-11-10, pyegeria 6.2.29.)*

**Dashboard Sheets are held in Egeria.** A sheet is a `Dashboard` asset (qualified name `Dashboard::<sheet name>`, with an `Ownership` classification naming its owner), linked to a `DisplayDataSchemaType` (the layout), a `DisplayDataContainer` (the sheet) and one `DisplayDataField` per placement. The *Reports* each placement shows, and the data they query, are Egeria elements too. Deleting a sheet never deletes its Reports.

**Which tool shows a sheet** is decided by dashboard folders: a sheet's `Dashboard` element is a member of `DashboardFolder::Consumer::<tool>` under `RootCollection::DashboardSheets`. On the quickstart the **Dashboard Folders** batch builds the tree.

**The local file is a fallback.** Before 6.2.29 sheets lived in a JSON file the Portal kept (`~/.pyegeria/dashboard_sheets.json` in the Portal's container). The Portal reads Egeria first and uses the file only for sheet names Egeria does not hold. **If a name is in both, Egeria wins.** If Egeria cannot be read, the page says so ("Egeria could not be read, so only sheets from the local file are shown…") rather than showing a shorter list as if it were complete.

On the quickstart, the five sheets that were in the file (Chief Data Officer Dashboard, `local-dashboards-next-steps`, Assets by Type and Location Demo, `digital-product-portfolio`, `my-team-dashboard`) were moved into Egeria on 2026-11-10, keep their names, and are owned by `erinoverview`. Their entries were removed from the file, so each name opens only the Egeria copy.

**Managing sheets held in Egeria.** The Dr.Egeria sheet commands write to Egeria (and keep a local copy as the fallback). pyegeria also has a command-line tool:

```bash
python -m pyegeria.view.dashboards list                # sheets held in Egeria
python -m pyegeria.view.dashboards show NAME           # one sheet and its placements
python -m pyegeria.view.dashboards migrate --dry-run   # copy sheets from the local file into Egeria (dry run first)
python -m pyegeria.view.dashboards delete --sheet NAME [--local]
```

`migrate` and `delete` are **shared writes**: everyone using that Egeria sees the result, so agree them with whoever looks after it, use `--dry-run` first, and run them once. `migrate` never edits the local file; remove a migrated sheet's old entry from it yourself. The Portal's Delete button (which needs you to be signed in) removes only a sheet that is held in the local file; for a sheet held in Egeria the button is greyed out, and hovering it says how to delete the sheet. Delete a sheet held in Egeria with `python -m pyegeria.view.dashboards delete --sheet NAME`, which is a shared write. Details: [Building a Local Dashboard](../tutorials/local-dashboards.md#where-dashboard-sheets-live).

After an Egeria wipe, the [Data Initialization](data-initialization.md) batch **Local Dashboards** (`dr-egeria-inbox/Local Dashboards/_batch.json`) re-runs the documents that create four of the quickstart sheets and their Reports: `local-dashboards-next-steps`, Assets by Type and Location Demo, `digital-product-portfolio` and `my-team-dashboard`. The Chief Data Officer Dashboard is not in that batch: load `coco-workbooks/0. data-governance-program/chief-data-officer-dashboard.md` again to recreate it.

---

## Further resources

- [Egeria Overview](egeria-overview.md) — the Portal's other, unrelated dashboard model (static P0 KPI tiles, not user-authored)
- [Data Initialization](data-initialization.md) — how Local Dashboards' seed data survives a reset
