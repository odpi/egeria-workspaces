<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Next Steps & Roadmap

Handoff / pick-up-later notes for the `/egeria-overview` dashboard. Companion to
[`OVERVIEW_METRICS.md`](OVERVIEW_METRICS.md) (per-metric catalog + costs).

## Where it stands (branch `feature/egeria-overview-dashboard`)

- App is live and verified through the Apache proxy (`localhost:8885/egeria-overview`).
- Live: summary KPIs (assets, terms, governed, certs/licenses, data products,
  exceptions), People (persons/teams/orgs/communities), Usage Context (ISC,
  blueprints), AI grounding, and the **Growth series via `asOfTime`**.
- KPI **sparklines are real** for metrics with history (assets/terms/governed/
  products) with a time reference; others show no sparkline (honest).
- Still ⚪ sample (labeled): Business Value lens numbers, confidentiality/zone
  bars, attention queue, DQ coverage, karma/feedback/leaderboard/engagement,
  activity feed, AI funnel documented/lineage/aiReady, usage % contextualised.

## The big opportunity: Egeria's two temporal axes

Egeria is **bitemporal**. The dashboard currently uses only a sliver of one axis.
Leaning into both is the most distinctive thing this app can do — no separate
time-series store, no data warehouse, the metadata *is* the history.

### Axis 1 — `asOfTime` (system / version time) — **use this heavily next**

"What did the repository know at time T." Already used for the growth series.
Underexploited. Planned uses:

1. **Global time-machine** — a single "as of `<date>`" picker in the header that
   re-runs **every** `/api/overview/*` endpoint with `asOfTime=<date>`. The whole
   dashboard (every KPI, every section) then shows the metadata landscape *as it
   was* on that date. Backend already threads `as_of_time` in several places
   (insights/audit do too); generalize it across the overview endpoints.
2. **Compare mode** — "now vs as-of `<date>`": show each KPI with a delta and an
   arrow. This is the honest, general version of the hardcoded sample deltas.
   Every metric gets a real historical value *for free* from `asOfTime` — no
   sample needed.
3. **Time-window control** (the 30d/90d/6mo/1y selector, currently cosmetic) —
   drive the growth window + granularity off `asOfTime`. Generalize the growth
   endpoint: `GET /api/overview/growth?window=7d&points=7` (or `interval=1d`),
   granularity following window: 8h→hourly, 1d→2–4h, 7d→daily, 30d→daily,
   90d→weekly, 1y→monthly. UI: compact dropdown (favorites as chips + "⋯" for the
   rest) rather than more buttons. NB: demo data is bulk-loaded in July, so
   sub-month windows are flat here — this feature is for production continuous
   ingest.

### Axis 2 — effectivity time (valid / business time) — later, subtler

`effectiveFromTime` / `effectiveToTime` on elements and relationships: "when is
this *meant* to be in effect," independent of when it was recorded. Distinct from
`asOfTime`. Deferred, but powerful once the above lands:

- **"Effective as of `<date>`"** — governance/classifications/certifications that
  are (or will be) in force on a chosen business date, incl. **future-dated**
  changes. E.g. "our governance posture effective start of next quarter."
- **Expiring effectivity** surfacing — certifications/classifications whose
  `effectiveToTime` is approaching (a truer "expiring soon" than the ad-hoc end-date
  parse in `_certifications`).
- Combined bitemporal view ("as recorded at T1, effective at T2") is the full
  power but almost certainly more than the dashboard needs near-term.

## Egeria API enhancements we want (for the enhancements session)

Root problem (see `OVERVIEW_METRICS.md` → *Cost & the case for a count API*):
**no server-side count.** Every metric is `len(find_metadata_elements(...))`,
which materializes and transfers the whole result set. Growth pays this N×4.

Requested, in priority order:

1. **Element count** — `POST …/metadata-elements/count` taking a `FindRequestBody`
   (same shape as the search) → `{ "count": N }`. Must honour `asOfTime` and
   classification/type/status conditions. Replaces ~all `find_metadata_elements`
   `len()` calls.
2. **Relationship count** — `…/relationships/{type}/count` (+ `asOfTime`) →
   `{ "count": N }`. Replaces certification/license/exception/semantic-assignment
   counts.
3. **Grouped counts** — count elements grouped by `typeName`, or by a
   classification's ordinal value, in one call → `{ "GroupA": n, ... }`. Collapses
   the 6 per-type asset queries and powers confidentiality/zone distributions
   directly.
4. **(stretch) Participation / traversal counts** — "assets reachable from ≥1 ISC
   or blueprint," "assets with lineage relationships," "assets with a
   `SemanticAssignment`" — as count queries. Unlocks the deferred funnel stages
   (documented/lineage/AI-ready) and usage **% contextualised** without
   client-side graph walks.

Payoff: payloads shrink from thousands of objects to one integer; fine time
windows become cheap; the 60 s / 15 min caches can shrink or go away; and the
standing `insights_handler` "no `totalCount`" limitation is resolved portal-wide.

**Client prep (do first, no server change needed):** add a `_count(body)` helper
in `overview_handler.py` that calls the count API when available and falls back to
`len(find_metadata_elements(body))`. Route all counters through it, so the whole
dashboard speeds up the moment the server API ships.

## Remaining app wiring (independent of the API work)

- **Data products** publication status + ratings (currently just a count).
- **AI funnel** documented / lineage-traced / AI-Ready stages (needs traversal or
  the count API above).
- **Usage % contextualised** (traversal / count API).
- **People**: karma (ContributionRecord) + feedback rollups (comments/ratings/
  likes/tags) via Collaboration OMAS — the leaderboard/engagement/most-engaged
  widgets. Karma is often sparse in demo data → also compute an engagement score
  from feedback volume as a fallback.
- **Business Value lens** numbers, confidentiality/zone bars, attention queue, DQ
  coverage, activity feed → wire from their sources.
- **Perspective Question library**: persist the `PERSPECTIVES[*].questions` JS
  drafts as real `Question` (GlossaryTerm + `IsQuestion`) Dr.Egeria terms per
  perspective, each mapped to a report spec + tile.

## Open decisions

- **Asset definition**: headline "Cataloged Assets" sums 6 named types (~1,915);
  growth uses the `Asset` supertype (~1,729). Unify to one definition if exactness
  across headline and trend matters.
- Where the global as-of / compare controls live vs. the per-chart window control.
- Whether the time-window control also re-times the KPI deltas (recommended: yes).
