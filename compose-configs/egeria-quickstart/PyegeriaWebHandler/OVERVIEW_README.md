<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — dashboard app

An executive / summary dashboard for the Egeria Portal. The portal's other apps
(Catalog, Explorer, Lineage, Audit, Insights, Operations) are task-oriented
drill-down tools; **none answer "how are we doing, and is it improving?"** at a
glance. Egeria Overview fills that gap: scale, governance coverage, quality,
AI-readiness, usage context, and the people/community behind the metadata — every
number tied to a business-value lens and drill-through into the owning app.

- **Route:** `/egeria-overview` · **Portal tile:** 📊 Egeria Overview (row 1)
- **Files:** `egeria-overview.html` (SPA) · `overview_handler.py` (FastAPI router,
  registered in `pyegeria_handler.py`)

## Core idea — the dashboard *is* the Perspective/Question model

A dashboard = a **Perspective's Questions**, each answered by a saved report spec,
rendered as a drill-able tile. Selecting a perspective reconfigures the whole page
(which sections show, in what order, the KPI tiles, the question set). The 8
perspectives and their scavenged question sets (DAMA-DMBOK / DCAM / FAIR / DataOps)
are materialisable as real Egeria elements — see `OVERVIEW_PERSPECTIVES.dr-egeria.md`.

## Features

- **Perspective-driven layout** — 8 personas (Governance Lead, Steward, Data Owner,
  Consumer, Engineer, App/AI Builder, Privacy Officer, Community Lead); each shows a
  curated, reordered section set + its own KPI tiles + its own questions. Persists in
  `localStorage`.
- **Business Value lens** — every metric ladders to risk / productivity / trust /
  cost / AI-enablement.
- **Time machine (`asOfTime`)** — an "as of `<date>`" picker re-queries the *entire*
  dashboard at any past date; **Compare to now** shows real now-vs-then deltas
  (retires hardcoded sample deltas). Driven by Egeria's native bitemporal queries —
  no separate time-series store.
- **Growth trends** — real monthly/…/hourly snapshots via `asOfTime`; a window
  dropdown (8h…1y) sets span + granularity. Feeds the chart and the KPI sparklines
  (real series, with a date-range tooltip; metrics without history show no sparkline).
- **Drill-down** — every KPI / bar / funnel stage opens a detail drawer with live
  values and a deep link into the owning app.
- **Usage Context** — Information Supply Chains + Solution Blueprints (assets in a
  business context, not just a list).
- **AI & Context Intelligence** — AI-ready funnel, semantic grounding, guardrails.
- **People & Community** — persons/teams/orgs/communities + crowd-sourced feedback.

## Architecture

**Backend (`overview_handler.py`)** — serves the SPA and five aggregation endpoints:
`summary`, `people`, `usage-context`, `ai-context` (all accept `as_of_time`) and
`growth?window=&points=`. Best-effort: a field that can't be computed returns `null`
with `"partial": true` rather than failing. Small TTL cache (60 s; 15 min for growth).
All counts route through a **count seam** (`_element_count` / `_rel_count`) that uses
a native server-side count method when one exists and otherwise falls back to
`len(find/get)` — ready for the count API (below) with no rework.

**Frontend (`egeria-overview.html`)** — renders a full *sample baseline* so the page
is always useful, then overlays live `/api/overview/*` values into a `LIVE` store
(and a `BASE` store for Compare). A data-source badge (● live / ◷ as-of / ⇄ compare /
○ sample) means nothing is silently faked. Vanilla JS + self-contained SVG charts.
KPI band renders per-perspective; endpoints render **progressively** so fast tiles
appear without waiting on the slow one.

## Egeria's two temporal axes

Egeria is **bitemporal**. The app leans on **`asOfTime`** (system/version time) today
— the time machine and growth series. **Effectivity time** (valid/business time,
`effectiveFrom/ToTime`) is the next axis (future-dated governance, truer
"expiring soon"). Details + per-client as-of mechanisms: `OVERVIEW_NEXT_STEPS.md`.

## The one thing to add server-side: a native count API

Every count today is `len(find_metadata_elements(...))` — materialising the full
result set just to size it, which is why as-of queries are slow (~48 s). A native
`metadata-elements/count` + `relationships/{type}/count` (honouring `asOfTime`) drops
the whole dashboard, including the time machine, to sub-second. The count seam is
already in place; add the method name to one tuple. Full spec: `OVERVIEW_NEXT_STEPS.md`.

## Live vs. sample

Most tiles are live; a few need per-asset traversal / rollups and show a clearly
labelled sample baseline (AI-funnel documented/lineage, usage % contextualised,
business-value lens numbers, leaderboard/engagement, activity feed, confidentiality
& zone bars). Per-metric definitions, sources, cost, and status: `OVERVIEW_METRICS.md`.

## Testing

`test_overview_asof.py` — reproducible as-of test cases (client + HTTP layers):
`python test_overview_asof.py --base http://localhost:8885 --as-of <iso>`. Documents
the per-client as-of mechanisms and pins the `+`→space URL-encoding regression and
the `page_size=5000`+as-of 500s (both fixed / guarded).

## Deploy notes

- The handler dir bind-mounts into the container; uvicorn auto-reloads Python, so no
  restart is usually needed.
- **Apache proxy:** each portal *page* needs its own `<Location>` in
  `sites-available/proxy-locations.conf` (only `/api/*` has a catch-all). The
  `/egeria-overview` block is included; reload Apache (`apachectl -k graceful`) if the
  page 404s through port 8885.

## Documentation set

| File | What |
|---|---|
| `OVERVIEW_README.md` | this — app overview & entry point |
| `OVERVIEW_METRICS.md` | per-metric catalog (definition, source, cost, live/sample) |
| `OVERVIEW_NEXT_STEPS.md` | roadmap, temporal axes, the count-API spec |
| `OVERVIEW_PERSPECTIVES.dr-egeria.md` | loadable Dr.Egeria Perspective/Question library (VALIDATE → PROCESS to load) |
| `gen_perspectives.py` | regenerates the above from the SPA `PERSPECTIVES` |
| `test_overview_asof.py` | reproducible as-of test cases |
