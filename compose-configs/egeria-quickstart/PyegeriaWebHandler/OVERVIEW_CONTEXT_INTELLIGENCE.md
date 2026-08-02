<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Context Intelligence: Current Thinking, Design, and Plan

Written 2026-08-01, resolving **NEXT-7/8/9** in `BACKLOG.md` and superseding the
placeholder R-1/R-2/R-3 entries in `OVERVIEW_NEXT_STEPS.md` (kept there as
short pointers to this document, not duplicated). Updated 2026-08-02 (§1.8)
with a second, independently-sourced research pass (Gartner/NIST AI RMF/
IEEE P2807) that cross-checks the design below — it converges with the
existing conclusions rather than overturning them, and resolves the
Analytics-Ready vs. AI-Ready question as an explicit open item.

This document has three parts:

1. **Current thinking** — a synthesis of Pragmatic Data Research's Context
   Intelligence blog series against current (2026) industry practice and
   research, with sources.
2. **Design** — a revised definition for the Overview dashboard's coverage/
   readiness metrics, plus how Egeria's actual capabilities (Survey
   Framework, OpenLineage, Bitol interoperability, Digital Products) map
   onto it.
3. **Plan** — a phased roadmap, sequenced against effort and what's already
   buildable versus what needs research.

---

## Part 1 — Current Thinking

### 1.1 The core claim, and where it sits relative to the industry

Pragmatic Data Research's **Context Intelligence** thesis: AI systems
(LLMs, RAG, agents, MCP tools) don't fail from lack of data — they fail
from lack of *context* about that data (semantic, operational, governance,
usage). "Context Engineering" (the 2026 industry term for structuring what
goes into a prompt/agent turn) optimizes *within* a single query; it has no
visibility into which systems are authoritative, which data is current, or
how organizational boundaries should shape behavior. Context Intelligence
is the layer that supplies that — grounded in an open, cross-tool metadata
federation (Egeria), not a per-application bolt-on.
[Introducing Context Intelligence](https://pdr-associates.com/context-intelligence);
[Putting Context into Context Engineering](https://pdr-associates.com/putting-context-into-context-engineering)

**Is this ahead of the industry, or converged with it?** Both, in different
places:

- **Converged and current, not speculative.** "Context engineering" is
  independently confirmed as *the* defining 2026 enterprise AI trend —
  "the ability to provide rich, relevant context supersedes prompt
  engineering as the primary skill for maximizing AI effectiveness"
  ([arXiv:2603.09619](https://arxiv.org/abs/2603.09619);
  [OvalEdge](https://www.ovaledge.com/blog/context-engineering-tools)).
  Gartner's own AI-readiness framework — three pillars, metadata
  management / data quality / data observability — is the same claim from
  the data-management side: readiness isn't one number, and it isn't
  achievable by prompt tricks alone
  ([Gartner](https://www.gartner.com/en/articles/ai-ready-data);
  [DataGalaxy](https://www.datagalaxy.com/en/blog/3-key-pillars-for-ai-readiness/)).
  Search results for "context-graph and ontology-driven RAG" describe an
  *emerging* 2026 pattern — "extends GraphRAG by layering operational
  metadata, lineage, quality metrics, temporal context, and governance
  policies onto the knowledge graph" — that is, close to word-for-word,
  PDR's own framing, independently arrived at.
  ([Synvestable, Enterprise RAG Guide 2026](https://www.synvestable.com/enterprise-rag.html))
- **Ahead on execution specificity, not on direction.** Where the blog
  series goes further than general industry content is naming concrete,
  implementable patterns rather than staying at "layer metadata onto the
  graph": **Scoped-Resource Lists**, **Query Routing**, and **RAG
  Contextualization** (with three named, tradeoff-explicit implementation
  options), each with a stated Egeria-native mechanism (Digital Products,
  a Router Cache, Data Lens/Scope classifications). Most published material
  in this space stops at the concept.

### 1.2 The vocabulary: Data Lens, Data Scope, Data Grain

Three distinct, blog-defined concepts (often conflated in casual use):

- **Data Lens** — the *specification*: the scoped dimensions a project's
  data must match (temporal, geospatial, organizational, subject area,
  quality, legal/licensing).
  [Building the Data Lens for AI](https://pdr-associates.com/building-the-data-lens-for-ai)
- **Data Scope** — the *classification*: metadata attached to an asset
  recording which dimensional values it actually has (e.g. "North
  America," "Current Fiscal Year," "Sales Operations"). A Data Lens is
  matched by finding assets whose Data Scope conforms to it.
  [AI Application Development](https://pdr-associates.com/ai-application-development-building-with-context-intelligence)
- **Data Grain** — the level of aggregation/granularity (row-level vs.
  daily vs. weekly vs. monthly). Concretely demonstrated in the sales-
  forecasting case study: live/row-level data was *intentionally*
  restricted to weekly/monthly summaries to fit the stability needs of
  the use case, not because finer data wasn't available.
  [Data Preparation in the AI Journey (Part 2)](https://pdr-associates.com/data-preparation-in-the-ai-journey-part-2)

Most business systems don't capture this metadata natively — it lives in
application code, naming conventions, and tribal knowledge, not the schema.
Matching a Data Lens to real sources is therefore itself a real, nontrivial
capture problem — the same "coverage" question NEXT-7 is asking, one layer
down.
[Matching the AI Data Lens to the Data Sources](https://pdr-associates.com/matching-the-ai-data-lens-to-the-data-sources)

### 1.3 The three RAG-pipeline patterns

From [AI Application Development – Building with Context Intelligence](https://pdr-associates.com/ai-application-development-building-with-context-intelligence):

| Pattern | Question it answers | Egeria-native mechanism |
|---|---|---|
| **Scoped-Resource Lists** | What data should this AI application ingest? | Data Lens (spec) matched against Data Scope classifications; packaged and shipped as a **Digital Product** so the application doesn't query Egeria live at runtime |
| **Query Routing** | Which RAG partition / model / MCP tool for this query, given who's asking and why? | A **Router Cache** — Egeria maintains the authoritative mapping (business context → resource), the application consumes it as a fast local lookup |
| **RAG Contextualization** | How should retrieval respect business context (region, role, governance)? | Three explicit options: **metadata filtering** (hard boundaries, pre-retrieval), **context-aware re-ranking** (softer, post-retrieval), **context-augmented embeddings** (context baked into the vector itself, for disambiguation-critical collections) |

This maps cleanly onto current RAG engineering practice: metadata-driven
pre-retrieval filtering and post-retrieval re-ranking are both named
current best practices, with semantic + metadata chunking showing
87–92% recall versus 50–65% for fixed-size baselines
([Unstructured.io](https://unstructured.io/insights/how-to-use-metadata-in-rag-for-better-contextual-results);
[Atlan, Chunking Strategies for RAG 2026](https://atlan.com/know/chunking-strategies-rag/)).
The novelty isn't the RAG technique — it's that Egeria is positioned as the
*single authoritative source* generating that metadata for every
downstream RAG/agent/MCP consumer, instead of each application inventing
and maintaining its own.

### 1.4 Data quality and observability — corrected framing

Earlier framing in this discussion incorrectly treated "Egeria has no data
quality or observability mechanism" as a flat gap. It doesn't compute
quality itself, but it doesn't need to — the **Survey Framework**
(`SurveyReport`/`Annotation` elements — live examples already exist in this
environment, e.g. "Survey report produced by survey-postgres-database")
plus the **Governance Action Framework** (invoke external
quality/profiling/analytics engines on a trigger, store results, act on
predefined kinds of change) is the orchestration/storage/action layer for
exactly this. This is architecturally the right answer to Gartner's "data
observability" pillar: Egeria doesn't compete with Monte Carlo/Bigeye-style
tools, it's the place their results land, get linked to business context,
and drive governance action. The in-development **Resource Explorer** is
the natural UI surface for this. This also directly matches the "ingesting
observability data from AI systems... integrating that into the broader
understanding of business processes" idea already named in
[Putting Context into Context Engineering](https://pdr-associates.com/putting-context-into-context-engineering) —
except it generalizes beyond AI-system feedback to *any* external
quality/profiling engine.

### 1.5 Lineage — OpenLineage changes the framing

Egeria and OpenLineage are sister LF AI & Data projects, not unrelated
tools Egeria happens to read. Egeria has a dedicated **OpenLineage
Cataloguer Integration Connector**; OpenLineage events can be augmented
with Egeria governance facets and republished, and governance processes
can use OpenLineage events to validate that source pipelines are running
as expected.
([OpenLineage blog: OpenLineage Support in Egeria](https://openlineage.io/blog/openlineage-egeria/);
[egeria-project.org lineage management overview](https://egeria-project.org/features/lineage-management/overview/))

This means "lineage coverage" should not be one generic tile. There are
(at least) two distinct kinds, with different maturity expectations:

- **Operational lineage** (OpenLineage-sourced) — job/run-level,
  near-real-time, "did this pipeline actually run and produce what we
  expect."
- **Design/business lineage** (Egeria-native, declarative) — the
  intended data flow, asset-to-asset, often authored rather than observed.

Industry lineage-tooling benchmarks (useful as maturity bands, not targets
to hit blindly): mature organizations target 90%+ coverage on critical
assets including column-level lineage; 75%+ documented lineage correlates
with 40–50% higher AI-project success rates in the cited data.
([Murdio, Data lineage metrics in 2026](https://murdio.com/insights/data-lineage-metrics/);
[Promethium, Data Lineage Tools Compared 2026](https://promethium.ai/guides/data-lineage-tools-compared-2026-buyers-guide/))

### 1.6 Data Contracts and Data Products — a real standards path, not a hypothetical

**Bitol** (Open Data Contract Standard / ODCS + Open Data Product Standard
/ ODPS) is an LF AI & Data incubation project — the same foundation as
Egeria. ODCS v3.1.0 adds relationships between properties, stricter
validation, and executable SLAs; ODPS is explicitly positioned alongside
ODCS as the common foundation for interoperable, governed data products.
([Bitol](https://bitol.io/);
[ODCS v3.1.0 announcement](https://bitol.io/bitol-announces-odcs-v3-1-0-stronger-smarter-and-stricter/);
[ODPS v1.0.0 announcement](https://bitol.io/announcing-odps-v1-0-0-building-the-language-of-data-products/))
2026 industry data confirms this is a live, forming trend, not a niche
concern: an estimated 40% of large enterprises are projected to adopt a
formal data contract framework by 2026, with "contract-first" data
engineering treating schema + SLOs as versioned, CI/CD-managed artifacts.
([Kliente 360, Data management trends 2026](https://kliente360.com/blog/en/tendencias-data-management-2026.html);
[TechTarget, Data domain ownership, data mesh chart path to AI-ready data](https://www.techtarget.com/searchdatamanagement/feature/Data-domain-ownership-data-mesh-chart-path-to-AI-ready-data))
Egeria already models the ingredients of a data contract natively
(Governance Definitions, SLOs, Certification Types — see the Project
Definition blog); the stated direction of interoperability with ODCS/ODPS
means "Data Contract Coverage" can eventually be defined in terms an
external tool would also recognize, not an Egeria-only vocabulary.

### 1.7 What this rules in and out for a dashboard metric

The FAIR Data Maturity Model literature is a useful cautionary precedent
for *how not* to build this: composite/blended FAIR scores are
consistently criticized because they hide exactly the disagreement between
sub-dimensions that matters — a dataset can score high on Findability and
weak on Accessibility/Interoperability/Reusability, and a single number
erases that. The RDA working group itself couldn't settle on one scoring
method.
([RDA FAIR Data Maturity Model](https://www.rd-alliance.org/group_output/fair-data-maturity-model-specification-and-guidelines-draft/);
[Data Science Journal](https://datascience.codata.org/articles/10.5334/dsj-2020-041))
**Conclusion carried into the design below: show named sub-scores, not one
blended "context richness" number** — this was already the instinct in the
prior draft, and it now has a documented failure mode as its justification
rather than just taste.

RAG evaluation research (RAGAS, groundedness/faithfulness scoring,
precision@k/recall@k) also confirms a boundary that matters for scoping:
these metrics require the AI/RAG system's own retrieval and generation
events, not just catalog metadata — they live *outside* what Egeria can
compute from its own graph.
([N-iX, RAG evaluation explained](https://www.n-ix.com/rag-evaluation/);
[Patronus AI, RAG Evaluation Metrics](https://www.patronus.ai/llm-testing/rag-evaluation-metrics))
But there's a middle tier worth adding that the earlier draft collapsed
into "needs full feedback loop": **is a retrieved chunk traceable back to
a cataloged, classified, owned source at all** is answerable from Egeria's
side alone, given just a log of what got retrieved — no AI-system
cooperation on grading its own output required.

### 1.8 A second research pass (2026-08-02): Gartner/NIST/IEEE cross-check

A second, independently-sourced research pass (Gartner, NIST AI RMF, IEEE
P2807, and enterprise architecture material from Databricks/IBM/Alteryx)
was brought in specifically to stress-test the four-tier design above
before building against it. Net result: **it converges with §1.7's
conclusions rather than contradicting them**, and it sharpens two things
the design left implicit.

**What it confirms, independently.** The same five-dimension shape this
pass proposed — semantic/grounding, lineage/provenance, governance/
entitlement, operational/recency, structural/interpretability — maps
almost one-to-one onto the Tier 1–3 sub-tiles already designed in §2.2–2.4
(Semantic Richness, Design/Business + Operational Lineage Coverage,
Governance Classification Coverage, Survey Annotation Coverage, Graph
Connectivity Depth). Nothing in the cross-check required inventing a new
Egeria concept — a second, unrelated research pass landing on essentially
the same decomposition is a reasonable signal the tiering is the right
shape, not an artifact of how the first pass happened to frame it.

**Where it was tempting but wrong, and why the existing design already
avoids it.** The proposed `AI Readiness Score = w1·Semantic + w2·Lineage +
w3·Governance + w4·Quality + w5·Structure` composite is the exact
blended-score failure mode §1.7 already ruled out via the FAIR Data
Maturity Model precedent — a weighted sum lets a strong score in one
dimension paper over a zero in another (e.g. rich lineage and semantic
grounding compensating for *zero* governance classification, which is
backwards for what NIST AI RMF and the EU AI Act actually care about:
governance failures should gate access, not get averaged away). This
project already has a concrete, shipped precedent for gates-over-weights:
`ai_ready_assets` (NEXT-18, shipped 2026-08-01) is a true intersection —
governed AND documented AND lineage-traced *simultaneously* — precisely
because a blended version would have let a well-documented, well-traced,
ungoverned asset still read as "mostly AI-ready." **Design principle,
now with two independent lines of evidence: named sub-scores/gates, never
one blended headline number** (§1.7's FAIR precedent + this session's own
`ai_ready_assets` precedent).

**Where it genuinely extends the design: per-purpose gates aren't a new
concept here, they're what §2.5's Data Lens Conformance report spec
already *is*.** The cross-check's own "different AI applications need
different weight profiles" observation (a RAG chatbot cares about
Semantic/Recency more than a batch training job does; an autonomous agent
with write access needs Governance/Entitlement to matter far more than a
read-only retriever) doesn't need a new mechanism — a **Data Lens** (§1.2)
already is a named, parameterized spec of which dimensions matter and by
how much for one project's purpose, and **Data Lens Conformance** (§2.5,
already planned as a report spec, not a KPI) is already the "evaluate
against this purpose's profile" mechanism the cross-check was reaching
for. Recorded here so this connection isn't lost: *when Data Lens
Conformance gets built, its scoring should itself use gates per matched
dimension, not a weighted blend* — the per-purpose parameterization was
already right, the internal scoring shape needs the same discipline as
Tier 1's sub-tiles.

**A genuinely new axis: Analytics-Ready vs. AI-Ready, and the textual/
numerical split.** Raised directly in discussion, not in either research
pass verbatim: does "AI-ready" skew toward textual/media data (chunking,
embeddings) while "analytics-ready" skews numerical/tabular, and should
Egeria treat them as different constructs? Resolution — validated in
part, relocated in part:
- The *perception* is real but the cause isn't inherent to the data — it's
  that the dominant first AI use case (RAG chat over documents) is
  text/media-heavy, so tooling and mental models calcified around that.
  There's an equally real AI-readiness question for structured/numerical
  data — feature stores for predictive models, text-to-SQL agents,
  forecasting agents — where readiness looks like *analytics-readiness
  plus a semantic layer for grounding* (business term → column mapping),
  not chunking and embeddings.
- The cross-check's own **DRL (Data Readiness Level) ladder** — Raw →
  Analytics-Ready → RAG-Ready → AI-Ready/Contextualized — gives the right
  resolution: **Analytics-Ready and AI-Ready are ordered points on one
  maturity ladder, not two parallel scoring systems.** They share almost
  all the same underlying machinery (governance, lineage, quality); the
  difference is which additional gates get required as you climb, not a
  different metric stack. This also answers "should we link them" from
  the original question directly: yes, as adjacent rungs, not as a
  cross-reference between two separate systems.
- What *does* need to vary by modality is what "Structural Readiness"
  (§2.2's Graph Connectivity Depth is one facet of this) concretely means:
  schema/type conformance and referential integrity for tabular data,
  versus chunking/embedding correctness and vector-index mapping for text/
  media. Rather than a second readiness axis, this is a **Modality tag**
  on the asset (Egeria already has the structural distinction —
  `DataField`/`TabularColumn`/`RelationalColumn` vs. `Document`/`Media`/
  unstructured `Asset` subtypes) that changes which Structural-Readiness
  sub-check applies, not a fork of the framework. Design consequence
  for §2.2, captured as an open decision in §"Open decisions" below —
  not yet built.

### 1.9 Resolved (2026-08-02): modality tagging, DRL bands, and how bands are represented in Egeria

Direction agreed on the three items §1.8 left open. Implementation detail
still needs its own pass (see "Open decisions" below), but the *shape* of
each is settled:

1. **Modality tag** — derive automatically from the asset's existing Open
   Metadata type (`DataField`/`TabularColumn`/`RelationalColumn` →
   tabular; `Document`/`Media`/unstructured `Asset` subtypes → text/media).
   No new classification for this. An explicit override is deferred until
   a real misclassified asset surfaces — same restraint already applied
   to `find_method` earlier in this project (don't build override
   machinery ahead of a concrete case).

2. **DRL bands = cumulative gate checklists, not score cutoffs** — extends
   the gates-not-weights principle (§1.7, §1.8) down into the band
   boundaries themselves, each band being the previous band's gates plus
   one or two new named gates:
   - **Raw** — cataloged only.
   - **Analytics-Ready** — Governance Classification Coverage AND
     Ownership Coverage AND Survey Annotation present — the existing
     Tier 1 baseline gates (§2.2).
   - **RAG-Ready** — Analytics-Ready gates + Semantic Richness above a
     floor + the modality-appropriate Structural Readiness sub-check.
   - **AI-Ready/Contextualized** — RAG-Ready gates + the already-shipped
     `ai_ready_assets` intersection (governed AND documented AND
     lineage-traced) + an operational/recency check.
   The top band composes existing shipped gates rather than needing new
   scoring machinery. Exact numeric floors (e.g. the Semantic Richness
   threshold) still need a banding pass — same shape as the existing
   lineage-coverage bands in §2.2, not new research.

3. **Band representation in Egeria — `Classification` and `Certification`
   are complementary, not either/or.** A `Classification` gives cheap,
   always-current band membership, queryable the same way as
   `Confidentiality`/other governance classifications Tier 1 already uses
   (`ClassificationExplorer`-shaped, no certifier-actor identity needed).
   A `Certification` adds the provenance/expiry story — who attested a
   band, when, next revalidation — reserved for the two bands worth a
   governance-grade badge: **Analytics-Ready** and **AI-Ready**.
   **RAG-Ready stays computed-only** in both representations — too
   high-churn to classify or certify. Likely shape: `Classification` for
   live band membership everywhere, a periodically-materialized
   `Certification` as the auditable snapshot for the top two bands only.
   `overview_metrics.py`'s gate computation stays the single source of
   truth for both. Sub-certifications (purpose/domain-scoped variants)
   remain explicitly backlogged, not designed.

---

## Part 2 — Design

### 2.1 Structural fix: split into four tiers, not one metric or two

| Tier | Question | Computable from Egeria's own graph today? |
|---|---|---|
| **1. Capture** | Is context being captured about our assets at all? | Mostly yes |
| **2. Quality / Observability** | Is captured context (and the underlying data) actually trustworthy? | Partially — via Survey Annotation coverage; full DQ scoring needs an external engine feeding Survey results in |
| **3. Traceability** | When AI retrieves something, can we prove where it came from and what governs it? | Yes, cheaply — needs a retrieval-event log, not AI-system cooperation |
| **4. Effectiveness** | Did the AI actually produce a good, faithful answer? | No — needs closed-loop feedback from the AI/RAG system itself |

Tiers 1–3 are Overview-dashboard-appropriate (Egeria-computable, near-term).
Tier 4 is out of scope for this round — it's real work (R-8-adjacent,
instrumentation/feedback-loop design) and shouldn't be faked with a proxy
that overclaims, the same lesson R-3 already drew for the business-value
tiles.

### 2.2 Tier 1 — Capture (replaces "Contextualized coverage")

Named sub-tiles, shown together (per §1.7 — no single blended score as the
headline number; an optional weighted composite can exist *underneath*,
clearly labeled as a blend):

| Tile | Definition | Backing |
|---|---|---|
| Semantic Richness | % assets linked to a glossary term / business capability | `semantic_grounding` — **exists** |
| Ownership Coverage | % assets with an assigned steward / data product owner | New — Egeria Actor/steward relationships already model this |
| Governance Classification Coverage | % assets carrying ≥1 governance classification (zone/confidentiality/criticality/retention) | `governed_coverage` — **exists** (this is what was previously mislabeled as a "quality" signal — it's a tagging metric, kept here where it belongs) |
| Data Contract Coverage | % assets with an attached, current SLA/certification (Governance Definition) | New — models exist, needs a count function; naming chosen to align with the ODCS/ODPS trend (§1.6) rather than an Egeria-only term |
| **Graph Connectivity Depth** *(new, not in either prior draft)* | e.g. % assets reachable via ≥2-hop typed relationship path, or average relationship fan-out | New — this measures the thing GraphRAG research says actually drives its accuracy gains (up to 35% precision uplift, 3.4x accuracy on multi-entity queries per [Atlan](https://atlan.com/know/knowledge-graphs-vs-rag-for-ai/) / [arXiv:2408.08921](https://arxiv.org/html/2408.08921v1)), and only a graph-native catalog can credibly claim it |
| Operational Lineage Coverage | % assets with OpenLineage-sourced run-level lineage | New — via the OpenLineage Cataloguer connector |
| Design/Business Lineage Coverage | % assets with declared, declarative lineage | `context_readiness_funnel`'s lineage stage — **currently stubbed `None`, real gap** |

Each shown against a maturity band (early / developing / mature), not a
bare percentage — per the industry lineage-tooling benchmarks in §1.5. A
raw "62%" is not actionable on its own; "62%, mature-org band is 90%+" is.

### 2.3 Tier 2 — Quality / Observability

- **Survey Annotation Coverage** — % assets with a recent (within N days)
  `SurveyReport`/`Annotation` attached. This is the corrected replacement
  for the flagged "no DQ mechanism" gap — it measures whether the
  orchestration layer is actually being used, which is the honest
  question Egeria can answer today.
- **External DQ Score Coverage** *(future, depends on which profiling
  engines get connected via Survey Framework)* — once a specific
  profiling/DQ engine is wired in (Great Expectations-style, or a
  Monte-Carlo-shaped connector), the fraction of assets with a live DQ
  score becomes measurable. Not blocked on building DQ scoring in Egeria
  — blocked on which external engine to integrate first, a Resource
  Explorer-adjacent decision.

### 2.4 Tier 3 — Traceability

- **Retrieval Provenance Rate** — % of logged AI/RAG retrieval events
  whose source chunk traces back to a cataloged, owned, classified Egeria
  asset. Requires: (a) RAG/agent side logs *which* asset/document a
  retrieved chunk came from (a metadata tag already recommended in
  §1.3's Contextualization pattern), (b) Egeria correlates that tag back
  to a real element. This is the cheap, high-value "traceability" signal
  called out in §1.7 as distinct from full effectiveness grading.

### 2.5 What's explicitly deferred (Tier 4, and AI-readiness-per-purpose / R-2)

Per-purpose AI-readiness (RAG-ready / training-ready / agent-tool-ready)
is not a single metric — it's **Data Lens conformance for a specific
project's Lens**, computed on demand, not a standing dashboard tile. The
Overview dashboard can show *capability* ("Egeria can answer Data Lens
conformance queries") without trying to show one global "AI-readiness %"
that Gartner's own research says doesn't exist as a universal thing.
Concretely: a **"Data Lens Conformance" report spec**, parameterized by a
named Data Lens, is a better fit than a KPI tile — this belongs in Egeria
Explorer's Report Spec browser or a Local Dashboards placement scoped to
one project, not the enterprise-wide Overview dashboard. **Per §1.8's
cross-check: when this gets built, its internal scoring must itself use
gates per matched Data Lens dimension, not a weighted blend** — the
per-purpose parameterization (this section) already solves "different AI
applications need different priorities" correctly; the risk is only in
*how* conformance against a matched Lens gets scored once the mechanism
exists, and that should inherit the same gates-not-weights discipline as
Tier 1, for the same reason (§1.7, §1.8).

Tier 4 (Effectiveness: groundedness, precision@k, hallucination rate)
requires closed-loop AI-system instrumentation feeding back into Egeria —
real, valuable, and explicitly out of scope for this pass.

---

## Part 3 — Plan

Phased by what's buildable now (existing functions/connectors) versus what
needs new work versus what needs research/design before any code.

### Phase A — Near-term, mostly wiring (targets NEXT-7)

1. Replace the Overview "Contextualized coverage" tile with the Tier 1
   sub-tile set (§2.2), shown as named scores + maturity band, not one
   composite headline number.
2. Wire the three sub-tiles with existing functions: Semantic Richness
   (`semantic_grounding`), Governance Classification Coverage
   (`governed_coverage`).
3. Build `ownership_coverage` and `data_contract_coverage` analytic
   functions (same shape as existing ones in `overview_metrics.py` /
   `analytic_registry.py` — this session's Local Dashboards analytics
   demo is a template for how to wire and verify one of these end-to-end).
4. Build **Graph Connectivity Depth** — new, no existing analogue; needs a
   short design pass on exactly what "typed relationship path" should
   count (avoid double-counting trivial relationships like classifications
   themselves).

### Phase B — Near-term, needs one new integration (targets NEXT-7)

5. Wire **Operational Lineage Coverage** via the OpenLineage Cataloguer
   connector (confirm it's deployed/configured in the quickstart/
   freshstart environments — needs an environment check first, may
   already exist).
6. Build **Design/Business Lineage Coverage** to fill
   `context_readiness_funnel`'s currently-stubbed lineage stage — this
   was already a known gap (OVERVIEW_NEXT_STEPS.md, pre-existing), now
   has a concrete definition to build against.

### Phase C — Medium-term, needs a scoping decision (targets NEXT-7/R-2)

7. **Survey Annotation Coverage** (Tier 2) — straightforward count, but
   needs a decision on which existing survey connectors count and what
   "recent" means (staleness window).
8. **Retrieval Provenance Rate** (Tier 3) — needs an actual RAG/agent
   deployment logging retrieval events with source tags before this is
   measurable at all; sequence after at least one real Context
   Intelligence pattern (§1.3) is deployed somewhere, not before.
9. **Data Lens Conformance report spec** — replaces the old "AI-ready
   assets" gate (R-2). Needs: a Data Lens authoring mechanism (Dr.Egeria
   commands or Resource Explorer UI — scoping question, not yet decided),
   then a report spec parameterized by a chosen Lens.

### Phase D — Research/design required before building (targets R-2/R-8, longer-horizon)

10. External DQ engine selection for Survey Framework integration (which
    profiling tool to connect first — a Resource Explorer-adjacent
    decision, not an Overview-dashboard one).
11. Tier 4 (Effectiveness) instrumentation design — what a RAG/agent
    deployment needs to report back to Egeria to make groundedness/
    precision/hallucination-rate metrics real, and how that data re-enters
    the graph (mirrors the "Organizing Protection" phase named in the
    blog series).
12. Bitol (ODCS/ODPS) interoperability — track as its own item; once
    Egeria's contract-interoperability work lands, revisit Data Contract
    Coverage's definition to align with the external standard's schema
    rather than an Egeria-only shape.

### Sequencing notes

- Phase A/B items are independent of each other and safe to build
  concurrently.
- Phase C item 9 (Data Lens Conformance) is the most consequential —
  it's the actual replacement for R-2's "AI-ready assets," not a nice-to-
  have, and should be prioritized once Phase A/B free up capacity.
- Nothing here is blocked on Phase D — Phases A–C deliver real, honest
  dashboard value without needing the harder research items resolved
  first.

---

## Open decisions (need a call, not further research)

- Exact "typed relationship path" definition for Graph Connectivity Depth
  (which relationship types count; how to avoid inflating the score with
  trivial links).
- Staleness window for "recent" Survey Annotation.
- Whether Data Lens authoring is a Dr.Egeria command surface or a Resource
  Explorer UI feature first.
- Which external DQ/profiling engine to integrate first via Survey
  Framework (Phase D-10) — depends on what the Resource Explorer work
  already has in flight.
- **(§1.8/§1.9) Modality tagging, DRL bands, and Classification vs.
  Certification — direction RESOLVED 2026-08-02, see §1.9.** Remaining
  before build (implementation detail, not open direction):
  - Which Structural-Readiness sub-checks apply per modality (schema/type
    conformance + referential integrity for tabular; chunking/embedding
    correctness + vector-index mapping for text/media) — needed before
    Graph Connectivity Depth / Structural Readiness (§2.2) can be
    modality-aware.
  - Exact numeric floors for each DRL band gate (e.g. the Semantic
    Richness threshold for RAG-Ready) — a banding exercise, not research.
  - Certification mechanics: certifying-actor identity (a
    `SoftwareServerCapability` standing in for the dashboard's metric
    engine, not a human), re-evaluation cadence, and how a live gate
    regression is reflected in the `Classification` before the next
    `Certification` re-evaluation run catches up.
  - Whether Classification, Certification, or both ship first for
    Analytics-Ready/AI-Ready — sub-certifications (purpose/domain-scoped
    variants) stay backlogged regardless.
