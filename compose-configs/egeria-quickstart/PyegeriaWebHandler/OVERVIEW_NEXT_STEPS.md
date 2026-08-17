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
- Still ⚪ sample (labeled): confidentiality distribution, confidential-assets-
  in-open-zones, data-stores-never-surveyed / has-schema-captured / surveyed /
  has-quality-annotations, most-engaged assets, activity feed.

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
   the deferred funnel stages (documented/lineage/AI-ready). Usage
   **% contextualised** turned out not to need this — see below, resolved
   2026-08-17 via a relationship-based proxy instead of the literal traversal.

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

**2026-08-02 update:** a second, independent Gartner/NIST AI RMF/IEEE P2807
research pass (§1.8) converged with this design rather than overturning it, and
**§1.9 now resolves direction** on the three items it left open: Modality tag is
derived automatically from existing Open Metadata type (no new classification);
DRL bands (Raw → Analytics-Ready → RAG-Ready → AI-Ready/Contextualized) are
cumulative gate checklists, not score cutoffs, with AI-Ready composing the
already-shipped `ai_ready_assets` intersection; and band membership is
represented via a `Classification` (cheap, always-current, queryable like
`Confidentiality`) for live state, with a periodically-materialized
`Certification` (provenance/expiry) reserved for Analytics-Ready and AI-Ready
specifically — RAG-Ready stays computed-only. Exact thresholds, per-modality
Structural-Readiness sub-checks, and Certification mechanics (certifying-actor
identity, re-evaluation cadence) remain as implementation-detail open items,
listed in the design doc's "Open decisions" section.

### R-3 — Business-value metrics (Productivity, Trust & Adoption, Risk, Cost) are synthetic — ✅ done (2026-08-02)

Wired to real data via a new `business_value_signals(mgr, as_of)` (egeria-python
`overview_metrics.py`, NEXT-9) — same defensive-import pattern as
`ownership_coverage`/`ai_ready_assets`. One Asset-hierarchy fetch answers two
of the four fields (per-element checks, same shape `context_readiness_funnel`
uses); duplicate detection is a separate classification count; Trust & Adoption
reuses the already-live `dataProducts` count rather than duplicating it.

| Tile | Old (synthetic) | New (real) | Causal-claim caveat |
|---|---|---|---|
| Risk & Compliance | "↓38% ungoverned confidential assets, YoY" | Count of **Asset-typed** elements carrying `Confidentiality` — verified live 2026-08-02: 1 of 1,737 in a real dataset | Proxy for regulatory exposure surface, not itself a risk-control measure. **Distinct from `governed_coverage`'s own `byClassification["Confidentiality"]`, which is NOT Asset-scoped** — the two numbers can legitimately differ a lot (5 vs 1 in the same dataset) and both are correct, just different populations |
| Productivity | "71% assets documented & findable" | `describedCount / assetTotal` — non-empty-description share of the Asset hierarchy (23% live) | Proxy for self-service findability; doesn't measure actual query/access frequency |
| Trust & Adoption | "18 products · ★4.3 avg" | Live `dataProducts` count (121); rating avg dropped entirely | No `AttachedRating` relationships exist against `DigitalProduct` in a typical demo dataset (confirmed live) — honestly omitted rather than faked |
| Cost Avoidance | "153 stale/duplicate assets flagged" | Count of `ConsolidatedDuplicate`-classified elements (0 in the demo dataset) | A real zero is an honest answer here, not a placeholder — this dataset has no detected duplicates |

**A real investigation dead-end worth recording:** while building the
Confidentiality check, an early test used `matchClassifications`'s older
flat `classificationNames` body shape and got 925 hits — looked like a
serious undercount bug in the newer `SearchClassifications`/`conditions`
shape `governed_coverage`/`ownership_coverage` already use. Cross-checked
against `ClassificationExplorer.get_elements_by_classification('Confidentiality')`
(purpose-built, most reliable ground truth): only 5 such elements exist
total, 4 of them typed `Referenceable` not `Asset`. The 925-hit flat-shape
query was the actual bug (silently ignored/near-unfiltered), not the
newer shape — no fix needed anywhere, existing code was already correct.
Logged here rather than in PYEGERIA_ISSUES.md since it resolved to
"working as intended," not an open gap.

### R-4 — Per-perspective section CONTENT variants (not just visibility) — ✅ mechanism proven, 2026-08-02

**Resolved the 3 open design decisions this item was waiting on:**
1. **Lookup key shape: per-Perspective only**, not per-Topic and not a full
   (Perspective, Topic) cross product — matches this doc's own lean toward
   avoiding a mostly-empty cross product.
2. **Authored as hand-written HTML template strings** in `egeria-overview.html`
   (a new `SECTION_VARIANTS` object), not migrated into the FormatSet/
   Container model — that migration is real, separate, much larger work.
3. **First concrete example built: "Usage Context"**, exactly as raised in
   the design discussion — `privacy` and `owner` variants, reframing the
   same 3 cards (Information Supply Chains / Solution Blueprints /
   Contextualised Coverage) with audience-specific labels and caveats.
   Deliberately does **not** invent new cross-referenced numbers ("chains
   carrying confidential data," "my own assets") the backend doesn't
   compute — each variant's caveat says so explicitly rather than faking a
   scoped figure. `uc-isc`/`uc-bp`/`uc-cov` ids and `data-drill` attributes
   are identical across every variant, so `applyUsage()`'s live-value
   wiring and drill-click both keep working regardless of which variant is
   in the DOM. A perspective with no authored variant (6 of 8 today) keeps
   the section's original "default" markup — `applySectionVariants()`
   caches it on first swap and restores it, verified live switching
   Governance Lead → Privacy Officer → Data Owner → back to Governance Lead.

Mechanism is proven and additive: authoring a variant for another section
or another perspective is just adding an entry to `SECTION_VARIANTS`, no
further plumbing needed.

**Status before this fix: two-axis navigation shipped 2026-08-01 (Perspective × Topic); this
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

- **Data products — ✅ done 2026-08-17.** Active-vs-pending breakdown via a new
  `count_elements_by_property(mgr, type_name, property_name, property_value,
  as_of)` helper (pyegeria `overview_metrics.py`) counting `deploymentStatus ==
  ACTIVE` vs everything else (2 cheap native COUNT calls, same cost class as the
  flat count it replaces). Ratings reuses the existing `count_relationships(ce,
  "AttachedRating", as_of)` call the People tile already makes independently —
  system-wide, not scoped to products (Egeria's relationship count can't filter
  by one end's type without a graph traversal), shown only when non-zero.
  Verified live: `dataProducts=6, dataProductsActive=2, dataProductsPending=4,
  dataProductsRatings=0`.
- **AI funnel — ✅ already done, dated 2026-08-01 (this bullet was stale).**
  `context_readiness_funnel`/`ai_ready_assets` (pyegeria `overview_metrics.py`)
  already compute all five stages (cataloged → documented → classified →
  lineage-traced → AI-ready) and the frontend funnel bar chart + Vega-Lite
  chart were already wired end-to-end — this bullet and the "Still ⚪ sample"
  line above both just predated that work. While re-verifying this live
  2026-08-17 (after a quickstart Egeria redeploy) found and fixed a real
  regression instead: `ClassificationExplorer.get_relationships`'s hardcoded
  `page_size=5000` now exceeds Egeria's new 1000-record max
  (`OMAG-COMMON-400-010`), so `lineage`/`aiReady`/every relationship-count-based
  metric (including Data Products' ratings above) was silently returning
  None/0-that-looked-intentional instead of erroring. Fixed to use the
  existing `DEFAULT_CAP` (500) at all three call sites; `insights_handler.py`
  and pyegeria's own `test_overview_asof.py` had the same literal, also
  fixed. Then made genuinely systemic: `max_paging_size` (pyegeria's
  underlying default) was itself a bare hardcoded constant disconnected from
  the `.env`/config.json settings system — now env-configurable
  (`EGERIA_MAX_PAGE_SIZE`), so a future server-side limit change is a config
  edit, not another repo-wide grep.
- **Usage % contextualised — ✅ done 2026-08-17.** Looked traversal-blocked
  (no native "assets reachable from an ISC/blueprint" count exists), but a
  single relationship type gets there cheaply instead: `ImplementedBy`
  (model 0737, Solution Implementation) links a SolutionComponent to its
  concrete implementation. One bounded fetch of all `ImplementedBy`
  relationships, filtered to Asset-subtype ends, distinct-GUID count = the
  numerator (`contextualised_coverage()` in pyegeria's
  `overview_metrics.py`). Confirmed live: 31 of 384 Assets = 8.1%. This is a
  **proxy**, not the literal metric — confirms an asset was given *some*
  solution-design context via ImplementedBy, not that its specific
  SolutionComponent is itself wired into an ISC/blueprint (that would need a
  second composition-relationship hop) — same single-hop tradeoff every
  other proxy metric in this file already makes (e.g. `lineage` counting
  DataFlow relationships, not confirming each sits on a path Egeria would
  call "lineage" in the strict sense). Documented as such in the function's
  own docstring and the frontend's tile caption.
- **People karma leaderboard + engagement over time — ✅ done 2026-08-17.**
  Leaderboard: `karma_leaderboard()` (pyegeria `overview_metrics.py`) — one
  bounded find over `ContributionRecord` elements (karma is a scalar
  `karmaPoints` property, not something derived from counting related
  things), filtered to `Person`-anchored records via the standard `Anchors`
  classification already carried on each element (no relationship traversal,
  no per-person loop), sorted desc, top 10. Engagement: `engagement_series()`
  reuses the same 5 feedback-relationship-type queries `feedback_summary()`
  already makes, keeping each relationship's `relationshipHeader.versions.
  createTime` instead of just the count, bucketed into ISO weeks (zero-filled
  across the trailing 12wk window, not omitted). Rendered via
  `generate_vega_line_chart`, same pattern as the Growth chart. Verified
  live: leaderboard = [Erin Overview 1260 pts, Peter Profile 210 pts];
  engagement series correctly zero-filled 11 weeks with the real 7 noteLog
  events landing in the current week (2026-W34). "Most-engaged assets" (a
  separate, per-asset rollup) remains unwired.
- **Governed vs Ungoverned 3-bucket split + Elements by Governance Zone — ✅
  done 2026-08-17.** `governed_coverage()` already fetched the full `hits`
  list for `byClassification`/`topZones`; extended it to also bucket each
  hit by which classifications it carries, at no extra query cost:
  "Fully governed" = carries ≥1 substantive governance classification
  (Confidentiality/Criticality/Impact/Retention); "Partial (zone only)" =
  carries `ZoneMembership` and nothing else from the governance set.
  Ungoverned is derived on the frontend the same way the donut % badge
  already was (`assetTotal - fully - partial`), not a separate query. Also
  found and fixed a real bug while here: "Elements by Governance Zone" was
  marked `status: 'live'` in the registry, but `topZones` was never actually
  read by any frontend code — the `byZone` bar chart was still the static
  sample array from page load. Wired it for real. Removed a fabricated
  "24 ungoverned assets are also flagged Confidential" line from the donut
  panel — no query computes that intersection, it was never anything but a
  sample number. Verified live: fullyGoverned=2, partialZoneOnly=48,
  assetTotal=388 (ungoverned=338); topZones led by digital-products (34).
  **Confidentiality Distribution** (the `byConf` panel, still illustrative)
  investigated but not wired: the per-level property is real
  (`confidentialityLevel`, an int ordinal on the `Confidentiality`
  classification — confirmed live), but only 2 elements in the whole
  dataset carry the classification at all (one of those two has no
  properties set), too sparse to be a meaningful distribution chart today;
  revisit once more governance-classified demo data exists.
- **Business Value lens — ✅ already done, dated 2026-08-02 (this bullet was
  stale).** Risk & Compliance / Productivity / Trust & Adoption / Cost
  Avoidance are all `status: 'live'` in the registry already, backed by
  `business_value_signals()` + the existing `dataProducts` count — same
  "bullet predated the work" pattern as the AI funnel finding above.
- **Attention Queue + Data Quality Coverage — ✅ 3 of 5 / 2 of 5 rows done
  2026-08-17.** Investigated all remaining panels in one pass (see chat/
  session log for the full per-row feasibility table) and wired the cheap
  wins: `orphan_glossary_terms()` (new pyegeria function — one bounded
  `SemanticAssignment` relationship fetch, distinct GlossaryTerm-end GUIDs
  = referenced, orphan = total - referenced) and `stale_assets()` (new
  pyegeria function — one bounded `Asset` element fetch, each element's own
  `_update_time()` vs a 180d cutoff, no traversal). "Certifications expiring
  ≤90d" and "Has assigned owner"/"Has description" needed **no new pyegeria
  code at all** — `certifications_summary`/`ownership_coverage`/
  `business_value_signals` already computed them for other panels, just
  weren't also wired into this one. Verified live: orphanTermCount=398 of
  407 terms (97.8% of the glossary has never been semantically assigned to
  anything), staleAssetCount=25 of 400 assets, certExpiring90=0,
  ownershipPct=1.8%, descriptions on 245/332 assets. Status registry split
  from 3 panel-level entries into 11 per-row entries (`quality` section) —
  the panels are genuinely mixed now, not uniformly live or sample.
  Remaining ⚪: "Confidential assets in open zones" (too sparse, see
  Confidentiality Distribution finding above), "Data stores never surveyed"
  and "Has schema captured"/"Surveyed"/"Has quality annotations" (need a
  2-hop DataStore→SurveyReport→Annotation traversal or a SchemaType
  traversal — not investigated in depth, real annotation data exists but is
  sparse: only 3 `ReportedAnnotation` relationships live today).
- **Perspective Question library**: persist the `PERSPECTIVES[*].questions` JS
  drafts as real `Question` (GlossaryTerm + `IsQuestion`) Dr.Egeria terms per
  perspective, each mapped to a report spec + tile.

## Design question raised 2026-08-17: how should Egeria itself describe these metrics?

Dan's own framing, worth capturing verbatim rather than losing it in chat:
this dashboard now has ~25 live metric functions in `overview_metrics.py`,
each with its own docstring explaining what it *really* measures (proxy vs.
literal, population scope, caveats) — but that knowledge lives only in
Python comments and frontend HTML captions. As the metric count keeps
growing, two related questions need a real design pass rather than being
answered ad hoc per-metric the way R-5 below started to:

1. **How does Egeria itself describe a calculation like this?** Not just
   the GlossaryTerm-per-metric governance layer R-5 already designs (name/
   summary/usage as structured metadata instead of a Python docstring) —
   whether the *computation itself* (which relationship type, which
   classification property, which population, ANY vs ALL, single-hop-proxy
   caveats) should be expressible as first-class Egeria metadata at all, or
   whether a docstring + GlossaryTerm pairing is the right permanent shape.
2. **Should these calculations be exposed as Governance Actions** (or a
   similar first-class Egeria construct) rather than living purely as
   Python functions a FastAPI route calls? That would make a metric
   independently triggerable/schedulable/auditable through Egeria's own
   governance-action framework instead of only ever running inline inside
   an HTTP request — potentially relevant for anything that currently has to
   stay a cheap single-bounded-fetch proxy (like `orphan_glossary_terms`
   above) specifically *because* it runs synchronously in a request/response
   cycle; a governance-action-triggered batch computation wouldn't have that
   constraint and could afford a real traversal.

**Design landed 2026-08-17, pilot run live** — see Dan's own two-part
response and the resulting investigation:

1. **`GovernanceMetric` (model 0450) is a strong fit for the definition
   side, largely without new schema.** It extends `GovernanceControl` →
   `GovernanceDefinition`, which already carries `summary`/`scope`/`usage`/
   `domainIdentifier`/`implementationDescription` plus its own `measurement`/
   `target`. `usage` is literally the slot R-5 below already planned to use
   for caveats — good confirmation R-5 picked the right field before this
   design pass existed. `GovernanceExpectations`/`GovernanceMeasurements`
   classifications were considered and set aside for now — both are
   per-resource constructs (a value classified onto one Asset), not a fit
   for catalog-wide aggregates like these.
2. **`report_specs` (not Governance Actions) is the implementation
   mechanism** — Dan's call, with a heads-up that FormatSet/report_specs are
   themselves being migrated toward standard Egeria types over time, which
   is part of why he's separately exploring letting Egeria define the
   Python functions callable inline (a further-out concern than this pilot).
   `GovernanceResults` (Metric → DataSet, "used to gather measurements from
   the landscape") already exists in the model, and `Report`
   (`Report → DataSet → Asset → Referenceable`) is already a DataSet
   subtype — so `GovernanceMetric --[GovernanceResults]--> Report` needs
   **no new relationship type**. Governance Actions remain a good fit later
   specifically as a second *execution mode* for the metrics too expensive
   to run synchronously in a request (the survey/schema-traversal DQ rows
   left illustrative above) — not a replacement for report_specs as the
   definition mechanism.

**Pilot run live, 2026-08-17, on `orphan_glossary_terms`:**
- Registered all 6 of this session's new `overview_metrics.py` functions
  (`count_elements_by_property`, `contextualised_coverage`,
  `karma_leaderboard`, `engagement_series`, `orphan_glossary_terms`,
  `stale_assets`) into `analytic_registry.py`'s `_BUILTINS` + one demo
  `FormatSet` each in `analytic_demo_specs.py` — the registry's own
  docstring claimed to cover "every analytic function that already exists,"
  which was stale; 23/23 parity restored between the two registries.
  Verified live via `/api/analytics` (23 functions) and `/api/report-specs`
  (348 specs, all 6 new demo specs present).
- Created a real `Report` element (`Create Report`, Report Spec: `Analytic
  Demo - Orphan Glossary Terms`, Output Format: DICT) and a real
  `GovernanceMetric` element (`Create Governance Metric`, `Summary`/
  `Scope`/`Usage`/`Implementation Description`/`Measurement`/`Target` all
  populated with the real prose from `orphan_glossary_terms`'s own
  docstring) via Dr.Egeria — both commands already existed, no new command
  needed for element creation.
- Linked them via `GovernanceResults`, using
  `GovernanceOfficer._async_link_governance_results` directly (raw pyegeria
  call, not a Dr.Egeria command — see the gap below).
- **Verified the full chain resolves purely from Egeria metadata**:
  `mgr.get_all_related_elements(<GovernanceMetric guid>)` returns the
  `GovernanceResults` relationship pointing at "Orphan Glossary Terms
  Metric Report"; that Report's `additionalProperties.reportSpec` names
  the FormatSet; executing the FormatSet via
  `POST /api/report-specs/execute` returns the real live numbers:
  `{"termTotal": 407, "referencedCount": 9, "orphanCount": 398}`.

**Real gap found, logged as `egeria-python` `PYEGERIA_ISSUES.md` ISSUE-61**:
no Dr.Egeria command exists for the `GovernanceResults` link — but it's not
an SDK gap, `link_governance_results`/`_async_link_governance_results` (and
the unlink twin) already exist in `governance_officer.py`, just never wired
to a compact-spec command. Per Dan: trivial for him to add once given an
issue number — logged, not yet added.

**Not yet done**: rolling this pattern out to the other ~24 metrics (this
was a one-metric pilot to validate the design, not a mass rollout), and the
`Link Governance Metric to Report` command itself.

## Open decisions

- **Asset definition — ✅ resolved 2026-08-16.** Headline "Cataloged Assets" used
  to sum 6 named types (curated-sum, e.g. live 2,668) while the growth chart's own
  "assets" series counted the raw `Asset` supertype (e.g. live 2,523) — genuinely
  confusing, not an intentional distinction. Unified on the `Asset` supertype: the
  headline tile now calls `MetadataExpert.count_metadata_elements(type_name="Asset")`
  directly (one native count, replacing the 6-query `sum_type_counts`/`sum_counts`
  path, BACKLOG.md NEXT-18's `sum_counts` import is now unused/removed from
  `overview_handler.py`), matching both `growth_series`' "assets" series and
  `context_readiness_funnel`'s 'cataloged' stage — all three now agree (verified
  live: `assetTotal` 2,598 == growth chart's own latest point). The "Assets by
  Type" breakdown chart still shows the curated 6-type composition — it's a
  breakdown view now, not required to sum to the headline. `overview_specs.py`'s
  `assets` tile `compute`/`summary`/`usage` updated to match;
  `OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md` regenerated (`gen_dashboard_glossary.py`,
  `--check` passes) and **re-processed against the live server 2026-08-16** via
  `POST /api/dr-egeria/execute-document` (VALIDATE then PROCESS, 147/147 commands
  succeeded each pass, 0 errors/warnings) — the live "Cataloged Assets" GlossaryTerm's
  `usage` now reads "Native count of the Asset supertype — everything cataloged...
  Same population as the growth chart's own 'assets' series and
  context_readiness_funnel's 'cataloged' stage — all three now agree" (verified
  live against guid `4f3cbc58-ab24-4b3b-bc61-c1c6b6dafc72`). Fully closed.
- Where the global as-of / compare controls live vs. the per-chart window control.
- Whether the time-window control also re-times the KPI deltas (recommended: yes).
