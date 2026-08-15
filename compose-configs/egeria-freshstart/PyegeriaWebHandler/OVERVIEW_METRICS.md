<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Metrics Catalog

Reference for every number the **Egeria Overview** dashboard (`/egeria-overview`)
shows: what it means, how it is computed, its data source, cost, and caveats.

**Status legend** (mirrors the dashboard's in-UI provenance badges: the header
carries a legend and every section-label shows ● live / ◐ mixed / ○ illustrative)
- 🟢 **live** — computed from Egeria via `pyegeria` (section badge: ● live).
- 🟡 **partial / mixed** — live where cheap; some sub-fields still sample (◐ mixed).
- ⚪ **sample** — illustrative placeholder; not yet wired (○ illustrative).

Section provenance in the UI: KPI band = live; Business Value, Quality & Attention,
Recent Activity = illustrative; Growth & Trends, Composition, Usage Context, AI &
Context Intelligence, People & Community = mixed.

Backend: `overview_handler.py`. All endpoints share a 60 s TTL cache
(`_CACHE_TTL`); `/api/overview/growth` uses a 15 min cache (`_GROWTH_TTL`).
Client factories build tokened `pyegeria` clients per request.

**Per-tile caveats (NEXT-24):** every tile below also carries a `summary` +
`usage` text — the same content behind the dashboard's click-to-open "ⓘ"
info bubble (fetched from `/api/overview/specs`) and behind a generated
Egeria Glossary ("Egeria Dashboard Analytics", one GlossaryTerm per tile,
under the "Egeria Dashboard" RootCollection — browsable in Egeria
Explorer's Collections view). Several tiles have real scoping caveats
(e.g. "Governed Coverage"'s numerator is not Asset-scoped while its
denominator is; "Semantic Grounding" is dominated by
`GovernanceActionProcess` elements, not `Asset`s). See
`OVERVIEW_METRIC_GOVERNANCE.md` for the design and
`OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md` for the generated doc — this
table itself doesn't repeat the full `usage` text, use the ⓘ bubble or the
Glossary Term for that.

---

## KPI tile registry (generated)

<!-- BEGIN GENERATED: overview-kpi-catalog -->

The Overview dashboard's KPI tiles are defined once in `overview_specs.py` as FormatSet-shaped specs (NEXT-10 P0) and served at `/api/overview/specs`. This table — provenance, drill targets, and the per-perspective selection — is generated from that registry, the single source of truth.

| Tile | Metric | Prov. | Type | Source (endpoint → field) | Render | Drill → | Perspectives |
|---|---|---|---|---|---|---|---|
| `assets` | Cataloged Assets | 🟢 live | — | summary → `assetTotal` | kpi | `assets` | governance, steward, engineer, builder, privacy, community |
| `terms` | Glossary Terms | 🟢 live | GlossaryTerm | summary → `termCount` | kpi | `grounding` | governance, steward, consumer, community |
| `governed` | Governed Coverage | 🟢 live | — | summary → `governedCount` | kpi | `governed` | governance, steward, owner, engineer, builder, privacy, community |
| `certs` | Active Certifications | 🟢 live | — | summary → `certifications` | kpi | `certs` | governance, steward, owner, privacy |
| `products` | Data Products | 🟢 live | DigitalProduct | summary → `dataProducts` | kpi | `products` | governance, owner, consumer, builder, privacy, community |
| `exceptions` | Open Exceptions | 🟢 live | — | summary → `openExceptions` | kpi | `exceptions` | governance, steward, owner, engineer, privacy |
| `people` | People / Contributors | 🟢 live | Person | people → `activeContributors` | kpi | `people` | owner, consumer, community |
| `communities` | Active Communities | 🟢 live | Community | people → `communities` | kpi | `people` | community |
| `isc` | Supply Chains | 🟢 live | InformationSupplyChain | usage-context → `informationSupplyChains` | kpi | `isc` | consumer, engineer, builder |
| `blueprints` | Solution Blueprints | 🟢 live | SolutionBlueprint | usage-context → `blueprints` | kpi | `blueprints` | consumer, engineer, builder |
| `grounding` | Semantic Grounding | 🟢 live | — | ai-context → `groundingPct` | kpi | `grounding` | steward, owner, consumer, engineer, builder, privacy |
| `ownership` | Ownership Coverage | 🟢 live | — | ai-context → `ownershipPct` | kpi | `ownership` |  |
| `ai-ready` | AI-Ready Assets | 🟢 live | Asset | ai-context → `aiReadyPct` | kpi | `ai-ready` |  |

**Compute** (each spec's `action` — the how-it's-computed / P3 report-runner hook):

- `assets` — `pyegeria.view.overview_metrics.sum_type_counts(type_map=[('Data Stores', 'DataStore'), ('Data Sets', 'DataSet'), ('Software Components', 'DeployedSoftwareComponent'), ('Infrastructure', 'ITInfrastructure'), ('APIs', 'DeployedAPI'), ('Processes', 'Process')])`
- `terms` — `MetadataExpert.count_metadata_elements(type_name=GlossaryTerm)`
- `governed` — `MetadataExpert.find_metadata_elements(matchClassifications=['ZoneMembership', 'Confidentiality', 'Criticality', 'Impact', 'Retention'], matchCriteria=ANY)`
- `certs` — `ClassificationExplorer.get_relationships(relationship_type=Certification)`
- `products` — `MetadataExpert.count_metadata_elements(type_name=DigitalProduct)`
- `exceptions` — `ClassificationExplorer.get_relationships(relationship_type=Exception)`
- `people` — `MetadataExpert.count_metadata_elements(type_name=Person)`
- `communities` — `MetadataExpert.count_metadata_elements(type_name=Community)`
- `isc` — `MetadataExpert.count_metadata_elements(type_name=InformationSupplyChain)`
- `blueprints` — `MetadataExpert.count_metadata_elements(type_name=SolutionBlueprint)`
- `grounding` — `ClassificationExplorer.get_relationships(relationship_type=SemanticAssignment, as=percent_of_assets)`
- `ownership` — `pyegeria.view.overview_metrics.ownership_coverage()`
- `ai-ready` — `pyegeria.view.overview_metrics.ai_ready_assets()`

**Provenance tally:** 13 live · 0 mixed · 0 illustrative.

<!-- END GENERATED: overview-kpi-catalog -->

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

**Native vs find — a semantics note.** A native `count_metadata_elements` returns
the raw repository count of matching entities; the older find-and-materialize
approach returns a *curated* graph view, so totals differ slightly (e.g. summed
asset types ≈ +6%, `Team` 45→66, `ITProfile` 32→62 — the native count is the
authoritative one). **Relationship** counts are the exception: the metadata-expert
`count_relationships_between_elements` and the classification-explorer
`get_relationships` disagree for some types (`Exception` 276 vs 55), so the
dashboard keeps relationship counts on `get_relationships` to stay consistent with
the Audit app. Element counts use native; relationship counts do not.

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
| **Information Supply Chains** | 🟢 | Count of `InformationSupplyChain` | native `count_metadata_elements` | 1 count |
| **Solution Blueprints** | 🟢 | Count of `SolutionBlueprint` | native `count_metadata_elements` | 1 count |
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
| **People / Contributors** | 🟢 | Count of `Person` | native `count_metadata_elements` | 1 count |
| **Teams / Organizations / IT Profiles** | 🟢 | Counts of `Team` / `Organization` / `ITProfile` | same single query | — |
| **Active Communities** | 🟢 | Count of `Community` | native `count_metadata_elements` | 1 count |
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
