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
The overview endpoints (summary / people / usage-context / ai-context) now accept
`as_of_time` and thread it through. **How each client takes as-of differs** —
verified by `test_overview_asof.py`:

| Client method | as-of mechanism |
|---|---|
| `find_metadata_elements` | `asOfTime` in the `FindRequestBody` |
| `get_relationships` | `asOfTime` in a `ResultsRequestBody` via `body=` |
| `find_actor_profiles`, `find_communities` | `as_of_time=` kwarg |
| `SolutionArchitect.find_*` | `asOfTime` in a **`SearchStringRequestBody`** via `body=` (no kwarg) |

**Gotchas found (tests reproduce them):**
- A raw `+` in the offset URL-decodes to a space → invalid timestamp → silent
  all-null. Guarded by `_norm_asof`; clients using `URLSearchParams` are fine.
- **`page_size` 5000 + as-of intermittently 500s** the Actor/Community/Solution
  view services; 500 (the endpoints' value) is reliable. Worth a controlled repro
  / pyegeria issue.
- as-of is **expensive** (people ≈47s) — reinforces the count-API case below.

Planned uses:

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

## Native instance counting — LANDED (odpi/egeria#9168), wired here

Egeria added native counting: `POST …/metadata-elements/by-search-conditions/count`
and `POST …/relationships/by-search-conditions/count`, both taking the same
`FindRequestBody` / `FindRelationshipRequestBody` as their `find` equivalents and
returning a `CountResponse{count}` (server does a `SELECT COUNT(*)` — no
materialization). pyegeria: `MetadataExpert.count_metadata_elements` /
`count_relationships_between_elements` (+ async twins, unit-tested).

**The dashboard uses them now.** The count seam (`_element_count` / `_rel_count`)
calls the native method when the client + server support it, else falls back to
`len(find/get)` — with a per-server capability cache so an older server costs at
most one failed probe. Verified: on the current (pre-#9168) stack it falls back and
returns identical values; on a #9168 stack the whole dashboard, incl. the as-of
time-machine and the N×4 growth snapshots, drops to sub-second. To run native
end-to-end: use a #9168 Egeria server and a pyegeria that includes the count
methods.

### Still wanted (future)

1. **Grouped counts** — count elements grouped by `typeName`, or by a
   classification's ordinal value, in one call → `{ "GroupA": n, ... }`. Would
   collapse the 6 per-type asset queries and power confidentiality/zone
   distributions directly.
2. **Participation / traversal counts** — "assets reachable from ≥1 ISC or
   blueprint," "assets with lineage relationships" — as count queries. Would unlock
   the deferred funnel stages (documented/lineage/AI-ready) and usage
   **% contextualised** without client-side graph walks.

## Done since first draft

- **Time-window control** wired: `/api/overview/growth?window=8h|1d|3d|7d|30d|90d|6mo|1y` (granularity follows window); header dropdown re-queries the chart.
- **People feedback** live: feedbackItems / feedbackByType / karmaRecords from Collaboration-OMAS relationship + type counts (sparse in demo but real).
- **Perspective/Question library** materialised: `OVERVIEW_PERSPECTIVES.dr-egeria.md` (generated by `gen_perspectives.py` from the SPA `PERSPECTIVES` — 8 perspectives, 33 questions, with `Create Perspective` / `Create Question` / `Link Perspective to Question` and stable qualified names). **To load: run it through Dr.Egeria VALIDATE, then PROCESS** (creates ~74 elements — a mutating step, intentionally left for you). Regenerate after editing the SPA question sets.
- **as-of time-machine + compare mode**, **count-API seam**, **progressive rendering** — see git log.

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
