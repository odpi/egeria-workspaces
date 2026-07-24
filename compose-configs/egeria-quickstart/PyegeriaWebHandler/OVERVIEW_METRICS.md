<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Metrics Catalog

Reference for every number the **Egeria Overview** dashboard (`/egeria-overview`)
shows: what it means, how it is computed, its data source, cost, and caveats.

**Status legend**
- 🟢 **live** — computed from Egeria via `pyegeria`.
- 🟡 **partial** — live where cheap; some sub-fields still sample.
- ⚪ **sample** — illustrative placeholder; not yet wired (labeled in the UI).

Backend: `overview_handler.py`. All endpoints share a 60 s TTL cache
(`_CACHE_TTL`); `/api/overview/growth` uses a 15 min cache (`_GROWTH_TTL`).
Client factories build tokened `pyegeria` clients per request.

---

## How counts are computed (important)

Counts flow through a **count seam** (`_element_count` / `_rel_count` in
`overview_handler.py`). When the pyegeria client **and** the target server support
Egeria's native instance counting (odpi/egeria#9168 —
`MetadataExpert.count_metadata_elements` / `count_relationships_between_elements`,
which answer with a `SELECT COUNT(*)` and no result-set materialization), the seam
uses it — every count here, including the as-of time-machine and the N-snapshot
growth series, becomes sub-second. Otherwise it **falls back** to
`len(find_metadata_elements(...))` / `len(get_relationships(...))`, which materialize
and transfer the full result set (the historical cost driver, esp. for as-of
queries). A per-server capability cache means a single failed native probe on an
older server disables further attempts — no repeated failed round-trips. Same
result either way; native is just far cheaper.

`page_size` is set high (500–5000). In this environment `find_metadata_elements`
returns the complete list regardless of `page_size` (verified: `Asset` = 1729,
`Process` = 1325 both exceeded 500), so counts are accurate — but a repository
connector that honours `page_size` as a hard cap would undercount; revisit if so.

---

## Headline KPIs — `GET /api/overview/summary`

| Metric | Status | Definition | Egeria source | Cost |
|---|---|---|---|---|
| **Cataloged Assets** | 🟢 | Sum of counts of key asset/infrastructure types | `MetadataExpert.find_metadata_elements` per type: `DataStore`, `DataSet`, `DeployedSoftwareComponent`, `ITInfrastructure`, `DeployedAPI`, `Process` | 6 full-list queries |
| **Glossary Terms** | 🟢 | Count of `GlossaryTerm` | `find_metadata_elements(type=GlossaryTerm)` | 1 query |
| **Governed Coverage** | 🟢 | `governedCount / max(assets, governedCount)`. `governedCount` = elements carrying **≥1** of {`ZoneMembership`, `Confidentiality`, `Criticality`, `Impact`, `Retention`} | `find_metadata_elements` with `matchClassifications` `matchCriteria=ANY` | 1 query (returns the classified set) |
| **Active Certifications** | 🟢 | Count of `Certification` relationships | `ClassificationExplorer.get_relationships("Certification")` | 1 query |
| ↳ expiring ≤90d | 🟢 | Certifications whose end date is within 90 days | end date parsed from relationship props (`coverageEnd`/`end`/…) or header effectivity | (same query) |
| ↳ licenses | 🟢 | Count of `License` relationships | `get_relationships("License")` | 1 query |
| **Data Products** | 🟢 | Count of `DigitalProduct` | `find_metadata_elements(type=DigitalProduct)` | 1 query |
| **Open Exceptions** | 🟢 | Count of `Exception` relationships | `get_relationships("Exception")` | 1 query |
| Assets-by-type breakdown | 🟢 | Per-type counts (composition bars + Assets drill) | the 6 per-type queries above | — |
| Top zones | 🟢 | `ZoneMembership` values tallied over the governed set | parsed from the governed elements' classifications | — |

> **Note on "Assets":** the headline (~1,915) sums the 6 named types (includes
> infrastructure/process). The **growth** series uses the `Asset` supertype
> (~1,729), which scopes differently. They are close but not identical by design;
> unify by choosing one definition if exactness across the two is required.

---

## Growth & Trends — `GET /api/overview/growth?months=N`

| Metric | Status | Definition | Source | Cost |
|---|---|---|---|---|
| Catalog growth series | 🟢 | For each of N monthly snapshots, counts of assets (`Asset`), `GlossaryTerm`, governed (ANY governance classification), and `DigitalProduct` **as of** that date | `find_metadata_elements(..., asOfTime=<iso>)` — Egeria answers historical queries natively; **no separate time-series store** | **N × 4 full-list queries** (the expensive endpoint) |
| KPI sparklines | 🟢 | Assets/Terms/Governed%/Products draw from the series above; metrics with no series show **no** sparkline | derived client-side | — |
| KPI deltas (`▲ N / 6mo`) | 🟢 | last snapshot − first snapshot | derived | — |
| Time window (30d/90d/6mo/1y control) | ⚪ | Currently cosmetic; does not yet re-query growth. Planned: drive `window` + `interval` | — | — |

Snapshots approximate a month as 30 days; `asOfTime` omitted for "now".
Demo data was bulk-loaded in July 2026, so months before July are near-flat —
this is real, not a bug.

---

## Usage Context — `GET /api/overview/usage-context`

| Metric | Status | Definition | Source | Cost |
|---|---|---|---|---|
| **Information Supply Chains** | 🟢 | Count of non-template ISCs | `SolutionArchitect.find_information_supply_chains` | 1 query |
| **Solution Blueprints** | 🟢 | Count of non-template blueprints | `SolutionArchitect.find_solution_blueprints` | 1 query |
| **% Contextualised** | ⚪ | % of assets participating in ≥1 ISC/blueprint | needs graph traversal per asset — deferred | (would be expensive without a server API) |

---

## AI & Context Intelligence — `GET /api/overview/ai-context`

| Metric | Status | Definition | Source | Cost |
|---|---|---|---|---|
| **Semantic Grounding** | 🟢 | `SemanticAssignment` relationship count; `% = links / assets` | `ClassificationExplorer.get_relationships("SemanticAssignment")` | 1 query |
| Funnel: Cataloged | 🟢 | `Asset` supertype count | `find_metadata_elements(type=Asset)` | 1 query |
| Funnel: Classified | 🟢 | Governance-classification ANY count | `find_metadata_elements(matchClassifications ANY)` | 1 query |
| Funnel: Documented / Lineage-traced / AI-Ready | ⚪ | Needs per-asset inspection (description present; lineage relationships; composite gate) | deferred — per-asset traversal | expensive without a server API |
| Context consumers / guardrails | ⚪ | MCP/API access-log driven; not natively in metadata | out of scope for metadata queries | — |

---

## People & Community — `GET /api/overview/people`

| Metric | Status | Definition | Source | Cost |
|---|---|---|---|---|
| **People / Contributors** | 🟢 | Count of `Person` actor profiles | `ActorManager.find_actor_profiles`, bucketed by `typeName` | 1 query (all profiles) |
| **Teams / Organizations / IT Profiles** | 🟢 | Counts of `Team` / `Organization` / `ITProfile` | same single query | — |
| **Active Communities** | 🟢 | Count of communities | `CommunityMatters.find_communities` | 1 query |
| **Feedback Items** | 🟢 | Σ of AttachedRating/Comment/Like/Tag/NoteLog relationship counts | `ClassificationExplorer.get_relationships` per type | 5 queries |
| **Feedback by type** | 🟢 | the five counts above | — | — |
| **Karma records** | 🟢 | Count of `ContributionRecord` elements | `find_metadata_elements` | 1 query |
| Leaderboard / Engagement trend / Most-engaged | ⚪ | Per-person karma rollup + weekly feedback trend | needs per-person aggregation — deferred | fan-out (rollup API) |

---

## Sections that are illustrative (⚪ sample)

Business Value lens numbers (38% / 71% / 18 / 153), confidentiality & zone bars,
attention queue, DQ coverage, expiring-cert table, recent-activity feed. These
render a labeled sample baseline; wire them as their sources are added.

---

## Cost & the case for a native count API

**Today's cost per dashboard load** ≈ summary (10 queries) + people (2) +
usage (2) + ai-context (3) + growth (N×4). Each query transfers the *full*
matching set only to `len()` it. Growth dominates (hence the 15 min cache).

A **server-side count** would be the single highest-leverage addition:

1. `POST …/metadata-elements/count` taking a `FindRequestBody` → `{ "count": N }`
   (no element materialization). Replaces every `len(find_metadata_elements(...))`.
2. `…/relationships/{type}/count` → `{ "count": N }`. Replaces the certification /
   license / exception / semantic-assignment counts.
3. **Grouped counts** (bonus): count elements grouped by `typeName`, or by a
   classification's ordinal value, in one call → collapses the 6 per-type asset
   queries and powers the confidentiality/zone distributions directly.

Benefits: payload drops from ~thousands of objects to one integer per query;
finer/faster **time windows** (hourly/daily points) become cheap; the 60 s / 15 min
caches can shrink or go away; and the currently-deferred traversal metrics
(**% contextualised**, funnel documented/lineage) become tractable via count
queries with the right conditions. This also resolves the standing
`insights_handler` "no `totalCount`" limitation for the whole portal.

Until then, counts are correct but heavier than necessary, and finer time
windows are gated on cost.
