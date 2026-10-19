# Local Dashboards

Local Dashboards renders **Dashboard Sheets** — named, ordered pages of report output, authored entirely through Dr.Egeria markdown, no code required. Each Dashboard Sheet is a list of **Placements**, and each Placement points at either a real Egeria **Report** asset (a saved query + output format, resolved live against Egeria every time the sheet loads) or another Dashboard Sheet, so pages can nest.

Access it from the portal tile (🗂️ Local Dashboards) or directly at `/local-dashboards`.

---

## Browsing sheets

The landing page lists every Dashboard Sheet that exists. Selecting one renders its Placements in order — each Report placement runs live against Egeria and renders the result inline (table, chart, or whatever the underlying Report Spec produces); a nested Dashboard Sheet placement renders that sheet inline too.

Because Report placements resolve live, a sheet always reflects Egeria's current state — there's no separate "refresh the dashboard" step, and no stale cached snapshot to worry about.

---

## Authoring a new dashboard

Dashboard Sheets are built entirely with Dr.Egeria commands — `Create Dashboard Sheet`, `Link Report to Dashboard Sheet`, `Add Text on Dashboard Sheet` — the same markdown-document workflow used everywhere else in the Portal. There's no separate dashboard-builder UI; you write a `.md` document and process it.

For worked examples, see the tutorials in the repo's `PyegeriaWebHandler` directory:
- `LOCAL_DASHBOARDS_TUTORIAL.md` — A technical, step-by-step guide to authoring and implementing a new dashboard.
- `DIGITAL_PRODUCT_SUBSCRIPTION_TUTORIAL.md` — A business-oriented scenario showing how to track Data Product adoption and historic growth trends.

---

## Resource Explorer's Curation Coverage tile

The report spec **Resource Explorer - Curation Coverage** can be placed on a sheet like any other. For one database known to [Resource Explorer](resource-explorer.md), it shows how many of its schemas are **published** and how many are **not yet published** (undecided, chosen but not published, or left out), with the tables and reports behind them. Use the `BAR` output format for a chart, or `DICT` for the detail. Pass the resource as the `slug` parameter, for example `localhost_docker_coco_pharma`.

- The Portal does not compute these numbers. It asks Resource Explorer, which runs the Analytic Library's `curation_coverage` routine, and shows RE's answer unchanged.
- RE runs it **as you**. The sheet sends the persona you picked in this browser; the Portal signs you in to RE with it and keeps RE's session on the server. **Without a persona the tile says "choose a persona to see this"** and doesn't call RE at all.
- When RE is not running, refuses the sign-in, or answers with an error, the tile says **not established** and gives the reason. It never shows zeros it did not measure.
- The Portal finds RE at `RESOURCE_EXPLORER_API_URL`, default `http://host.docker.internal:8813`.

---

## Where the data lives

Unlike most of the Portal, a Dashboard Sheet's own structure (its name, its ordered list of Placements) is **not** an Egeria element — it's a small local JSON record the Portal itself maintains. The *Report* each Placement references, and the data the Report queries, are both real Egeria elements. This is why Dashboard Sheets need their own [Data Initialization](data-initialization.md) batch to survive an Egeria wipe: re-running their seed documents recreates both the Egeria Reports and the local sheet records that reference them.

---

## Further resources

- [Egeria Overview](egeria-overview.md) — the Portal's other, unrelated dashboard model (static P0 KPI tiles, not user-authored)
- [Data Initialization](data-initialization.md) — how Local Dashboards' seed data survives a reset
