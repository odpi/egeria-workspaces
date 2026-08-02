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

## Metric design & research — HIGH PRIORITY, needs discussion (raised 2026-07-24)

These are not quick fixes — they need product/research discussion before building.
Captured verbatim so they don't get lost.

### R-1 — "Contextualized coverage" is an oversimplification (and not a standard term)
**Resolved 2026-08-01 — see [`OVERVIEW_CONTEXT_INTELLIGENCE.md`](OVERVIEW_CONTEXT_INTELLIGENCE.md)**
for the full research pass, design, and phased plan. Short version: replace the
single number with named Tier-1 "Capture" sub-tiles (Semantic Richness, Ownership
Coverage, Governance Classification Coverage, Data Contract Coverage, Graph
Connectivity Depth, Operational + Design/Business Lineage Coverage), shown against
maturity bands, not collapsed into one composite. No further research needed —
Phase A/B in that doc are buildable now.

### R-2 — "AI-ready assets" needs a best-practices/research effort, not a metric tweak
**Resolved 2026-08-01 — see [`OVERVIEW_CONTEXT_INTELLIGENCE.md`](OVERVIEW_CONTEXT_INTELLIGENCE.md)
§2.5.** Confirmed no universal AI-readiness (matches Gartner's own framing).
Replacement isn't a metric at all — it's a **Data Lens Conformance report spec**,
parameterized per project/purpose, living in Egeria Explorer's Report Spec browser
or a scoped Local Dashboards placement, not an Overview KPI tile. Data Scope/Grain/
Lens are now fully defined (grounded in the PDR blog series, see the design doc's
§1.2). Plan Phase C item 9.

### R-3 — Business-value metrics (Productivity, Trust & Adoption, Risk, Cost) are synthetic
Today these are narrative/sample. They can be honest with: a precise definition, a
real source, and framing as **leading indicators/proxies** not direct measures. E.g.
"Productivity 71%" = "% assets documented & findable" — a proxy for time-to-data,
but the label overclaims. For each of the four tiles: one-line definition + source +
the explicit causal claim, reword labels to what's measured, wire real data where it
exists. Medium effort; overlaps with the provenance work.

### R-4 — Per-perspective section CONTENT variants (not just visibility)

**Status: two-axis navigation shipped 2026-08-01 (Perspective × Topic); this
item is the deliberately-deferred next layer, design principle captured here
so it isn't lost.**

**What's done:** Overview now has two independent, orthogonal filter axes —
**Perspective** (*who* — a persona/role: Governance Lead, Steward, Data
Owner, Consumer, Engineer, App/AI Builder, Privacy Officer, Community Lead)
and **Topic** (*what domain of concern* — AI/Context Intelligence, Security/
Privacy, Quality, Popularity/Usage; "Any" = no filter). Both now control the
**whole dashboard**, not just the KPI band:
- KPI band: `currentKpiKeys()` — Perspective's tile list ∩ Topic's tile list,
  falling back to the Topic-only list if the intersection is empty.
- Section visibility/order: `currentSections()` — same intersection/fallback
  logic, over `PERSPECTIVES[x].show` ∩ `TOPIC_SECTIONS[topic]`.

Both axes are hand-authored dicts (`PERSP_KPIS`/`TOPIC_KPIS` for tiles,
`PERSPECTIVES[x].show`/`TOPIC_SECTIONS` for sections) — `PERSP_KPIS`/
`TOPIC_KPIS` have a Python-side mirror (`overview_specs.py`) and a
frontend/backend drift guard (`test_overview_specs.py`, 348 checks); the
section-level lists (`show`/`TOPIC_SECTIONS`) are frontend-only with no
backend mirror, since "sections" aren't a concept the tile registry models
at all today.

**What's deferred, and why it's a different shape of problem, not just more
filtering:** right now, whichever sections are *visible* show identical
content to every viewer — a shown section is complete, not itself filtered.
The design discussion (2026-08-01) surfaced a concrete example: **"Usage
Context" should plausibly look different for a Privacy Officer than a Data
Owner** — not just "shown or hidden," but genuinely different content within
it (a Privacy Officer's Usage Context view might emphasize which supply
chains touch regulated data; a Data Owner's might emphasize which blueprints
their own assets participate in).

**The key design call: solve this with per-perspective section *variants*,
not runtime filtering of one shared section.** Two different-shaped
solutions were on the table:
1. *Filter the content within one shared "Usage Context" section* by
   Perspective/Topic tags — the same mechanism `currentKpiKeys()` already
   uses, extended down a level.
2. *Author multiple section variants* — "Usage Context — Privacy Officer,"
   "Usage Context — Data Owner," etc. as distinct, independently-authored
   sections, and the Perspective/Topic resolution picks which variant to
   show instead of filtering one shared one.

(2) was the explicit call, for a real reason: most of a section's content
isn't in the tile registry at all — it's hardcoded HTML/JS blocks (Attention
Queue rows, Karma Leaderboard, Certifications table, most of "Usage
Context"'s own cards). Making (1) work means either migrating all of that
into the FormatSet/registry model first (a large refactor — this is exactly
the still-not-started "Format's own render-kind/provenance generalization"
work already flagged as P1 in this dashboard's own docstrings/
`OVERVIEW_REPORTING_MODEL.md`), or building a second, parallel tagging
system just for section-internal content (drift risk against the first).
(2) sidesteps that: authoring a new named section variant is additive (write
new content, give it a name, wire it into a per-(perspective,topic) lookup)
rather than requiring every existing hardcoded block to become
registry-aware before anything can vary. It also avoids the "why is half my
section missing" surprise a filtered-but-incomplete shared section risks.

**Not scoped yet.** Needs, at minimum: a decision on the lookup key shape
(pure per-Perspective variants, per-Topic variants, or full per-(Perspective,
Topic) — likely overkill given the sparsity a full cross product would
imply), a decision on where variant content is authored (still hand-written
HTML/JS in `egeria-overview.html`, or migrated toward the FormatSet/
Container model as part of doing this at all), and a concrete first example
(Usage Context — Privacy Officer vs. Data Owner, as raised) to prove the
mechanism before generalizing.

### R-5 — Metrics need governance: an audit, a Glossary, Collections, and an info bubble

**Status: design done 2026-08-01, see [`OVERVIEW_METRIC_GOVERNANCE.md`](OVERVIEW_METRIC_GOVERNANCE.md)
for the full design + phased plan (NEXT-24).**

Triggered by a live finding while drilling into Semantic Grounding: the
number is well-computed but measures something different from its own
label (87.7% of its underlying relationships connect to governance
workflow processes, not data assets — see the design doc §1.1 for the
full data). Rather than a one-off fix, this generalizes the check to every
`live`/`mixed`-tagged tile, and — following the exact pattern already
proven for Perspectives/Questions (`gen_perspectives.py`) — generates a
real Egeria `GlossaryTerm` per metric (carrying `summary`/`description`/
`usage`, `usage` being where caveats like this one live structurally, not
as a Python comment) grouped under a new RootCollection ("Egeria
Dashboard") with sub-collections, feeding a dashboard info-bubble UI.
`overview_specs.py` stays the single source of truth throughout — the
Glossary/Collections are generated downstream artifacts, not a second
thing to hand-maintain.

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
