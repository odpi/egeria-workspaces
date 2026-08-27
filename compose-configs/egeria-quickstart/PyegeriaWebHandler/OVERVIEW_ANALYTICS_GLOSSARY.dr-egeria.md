<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Dashboard Analytics — Glossary & Collections

> Loadable **Dr.Egeria** document that governs the Overview dashboard's own
> metrics as real Egeria elements: one **GlossaryTerm** per metric (Summary/
> Description/Usage — Usage carries caveats, e.g. scoping mismatches found
> during the NEXT-24 audit), grouped under a **RootCollection** with
> sub-collections (by app, by provenance, by Topic, by Perspective). Generated
> from `overview_specs.py`'s
> `_TILES` — the single source of truth. Regenerate with
> `gen_dashboard_glossary.py` after editing a tile's `summary`/`description`/
> `usage` fields.
>
> Design: `OVERVIEW_METRIC_GOVERNANCE.md` (NEXT-24), Phases A-D.
> **Run with VALIDATE first, then PROCESS.** Create commands carry user-specified
> Qualified Names so later commands in this doc can cross-reference them.

---

## Create Glossary

### Display Name
Egeria Dashboard Analytics

### Description
Definitions for the Overview dashboard's own metrics/KPI tiles — what each one actually measures, including known scoping caveats. Generated from overview_specs.py; see OVERVIEW_METRIC_GOVERNANCE.md (NEXT-24).

### Qualified Name
Glossary::Egeria Dashboard Analytics

### Version Identifier
1.0

---

## Create Root Collection

### Display Name
Egeria Dashboard

### Description
Master collection for everything describing the Egeria Portal's own dashboards (starting with Overview) -- what each metric measures, grouped a few different ways since an element can belong to more than one collection at once.

### Qualified Name
RootCollection::Egeria Dashboard

### Version Identifier
1.0

---

## Create Collection

### Display Name
Overview KPIs

### Description
Metrics belonging to the Egeria Overview dashboard app.

### Qualified Name
Collection::Overview KPIs

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Overview KPIs

---

## Create Collection

### Display Name
Business Value Signals

### Description
The Overview dashboard's Business Value tiles (Risk & Compliance, Productivity, Trust & Adoption, Cost Avoidance) -- shown to every Perspective/Topic, not filtered like the KPI-band tiles.

### Qualified Name
Collection::Business Value Signals

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Business Value Signals

---

## Create Collection

### Display Name
Live Metrics

### Description
Metrics whose provenance is currently "live".

### Qualified Name
Collection::Live Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Live Metrics

---

## Create Collection

### Display Name
Mixed Metrics

### Description
Metrics whose provenance is currently "mixed".

### Qualified Name
Collection::Mixed Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Mixed Metrics

---

## Create Collection

### Display Name
Illustrative Metrics

### Description
Metrics whose provenance is currently "illustrative".

### Qualified Name
Collection::Illustrative Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Illustrative Metrics

---

## Create Collection

### Display Name
AI / Context Intelligence Metrics

### Description
Metrics shown when the Overview dashboard's Topic filter is set to "AI / Context Intelligence Metrics" (topics_for()'s 'ai-context').

### Qualified Name
Collection::AI / Context Intelligence Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::AI / Context Intelligence Metrics

---

## Create Collection

### Display Name
Security / Privacy Metrics

### Description
Metrics shown when the Overview dashboard's Topic filter is set to "Security / Privacy Metrics" (topics_for()'s 'security-privacy').

### Qualified Name
Collection::Security / Privacy Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Security / Privacy Metrics

---

## Create Collection

### Display Name
Quality Metrics

### Description
Metrics shown when the Overview dashboard's Topic filter is set to "Quality Metrics" (topics_for()'s 'quality').

### Qualified Name
Collection::Quality Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Quality Metrics

---

## Create Collection

### Display Name
Popularity / Usage Metrics

### Description
Metrics shown when the Overview dashboard's Topic filter is set to "Popularity / Usage Metrics" (topics_for()'s 'usage').

### Qualified Name
Collection::Popularity / Usage Metrics

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Popularity / Usage Metrics

---

## Create Collection

### Display Name
Governance View

### Description
Metrics shown to the "Governance" Perspective on the Overview dashboard (perspectives_for()'s 'governance').

### Qualified Name
Collection::Governance View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Governance View

---

## Create Collection

### Display Name
Steward View

### Description
Metrics shown to the "Steward" Perspective on the Overview dashboard (perspectives_for()'s 'steward').

### Qualified Name
Collection::Steward View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Steward View

---

## Create Collection

### Display Name
Data Owner View

### Description
Metrics shown to the "Data Owner" Perspective on the Overview dashboard (perspectives_for()'s 'owner').

### Qualified Name
Collection::Data Owner View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Data Owner View

---

## Create Collection

### Display Name
Consumer View

### Description
Metrics shown to the "Consumer" Perspective on the Overview dashboard (perspectives_for()'s 'consumer').

### Qualified Name
Collection::Consumer View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Consumer View

---

## Create Collection

### Display Name
Engineering View

### Description
Metrics shown to the "Engineering" Perspective on the Overview dashboard (perspectives_for()'s 'engineer').

### Qualified Name
Collection::Engineering View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Engineering View

---

## Create Collection

### Display Name
Architecture View

### Description
Metrics shown to the "Architecture" Perspective on the Overview dashboard (perspectives_for()'s 'architecture').

### Qualified Name
Collection::Architecture View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Architecture View

---

## Create Collection

### Display Name
Security View

### Description
Metrics shown to the "Security" Perspective on the Overview dashboard (perspectives_for()'s 'security').

### Qualified Name
Collection::Security View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Security View

---

## Create Collection

### Display Name
App/AI Builder View

### Description
Metrics shown to the "App/AI Builder" Perspective on the Overview dashboard (perspectives_for()'s 'builder').

### Qualified Name
Collection::App/AI Builder View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::App/AI Builder View

---

## Create Collection

### Display Name
Privacy View

### Description
Metrics shown to the "Privacy" Perspective on the Overview dashboard (perspectives_for()'s 'privacy').

### Qualified Name
Collection::Privacy View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Privacy View

---

## Create Collection

### Display Name
Community View

### Description
Metrics shown to the "Community" Perspective on the Overview dashboard (perspectives_for()'s 'community').

### Qualified Name
Collection::Community View

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
RootCollection::Egeria Dashboard

### Element Id
Collection::Community View

---

## Create Glossary Term

### Display Name
Cataloged Assets

### Summary
Native count of active elements of the Asset supertype (and all its subtypes).

### Description
Native count of the Asset supertype — everything cataloged.

### Usage
Broadest possible definition of "cataloged" -- every Asset subtype counts, including e.g. DigitalProduct (which also has its own "Data Products" tile, so the two headline numbers overlap by design, not a double-count bug: Data Products is a callout of one Asset subtype, Cataloged Assets is the whole population). Same population as the growth chart's own "assets" series and context_readiness_funnel's 'cataloged' stage -- all three now agree.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-assets

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-assets

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-assets

---

## Create Glossary Term

### Display Name
Glossary Terms

### Summary
Native count of active GlossaryTerm elements across all glossaries.

### Description
Count of GlossaryTerm elements — the business vocabulary.

### Usage
Vocabulary SIZE, not vocabulary UTILIZATION -- a Term counts here whether or not it is ever linked to an asset via SemanticAssignment (see Semantic Grounding's own caveat for how unreliable that linkage signal currently is). No status filter is passed to the underlying query, so a DRAFT or DEPRECATED term counts the same as a published, in-use one.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-terms

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-terms

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-terms

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-terms

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-terms

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-terms

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-terms

---

## Create Glossary Term

### Display Name
Governed Coverage

### Summary
Count of elements carrying at least one governance classification, as a percentage of Assets.

### Description
Share of assets carrying at least one governance classification (ZoneMembership/Confidentiality/Criticality/Impact/Retention).

### Usage
The numerator (governance-classified elements) is NOT scoped to Asset -- ANY element type carrying one of the 5 classifications counts, matched ANY not ALL (one classification is enough). The denominator (percentage base) IS Asset-only. So this can legitimately exceed a naive expectation if many non-Asset elements (e.g. GovernanceDefinitions, Projects) are classified -- it is a coverage signal, not literally "the fraction of assets meeting the label". Also capped at DEFAULT_CAP (500) server elements per query -- governedCapped=true in the raw payload means the true count is a floor, not exact.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-governed

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::AI / Context Intelligence Metrics

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Security / Privacy Metrics

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-governed

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-governed

---

## Create Glossary Term

### Display Name
Active Certifications

### Summary
Count of Certification relationships currently attached to any element.

### Description
Count of active Certification relationships (with expiring/licenses sub-stats).

### Usage
Despite the "Active" in the tile label, this is a raw count of every Certification relationship fetched (up to a 500-relationship cap) -- there is no filter for whether the certification's own validity window has actually expired. The expiring-within-90-days and licenses sub-stats shown in the drill view are computed from that same fetch, but the headline number itself is not narrowed to "currently valid".

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-certs

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Security / Privacy Metrics

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-certs

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-certs

---

## Create Glossary Term

### Display Name
Data Products

### Summary
Native count of DigitalProduct elements defined in the catalog, with an active-vs-pending breakdown by deploymentStatus.

### Description
Count of DigitalProduct elements, broken down by publication (deployment) status.

### Usage
The headline number is every DigitalProduct DEFINITION regardless of status -- a count of product definitions, not a measure of adoption or usage. "Active" (dataProductsActive) counts deploymentStatus == ACTIVE specifically; "Pending" (dataProductsPending) folds every other value (DRAFT, UNDER_DEVELOPMENT, unset, etc.) together rather than enumerating each one, so it reads as "not yet actively deployed" rather than a specific lifecycle stage. Ratings (dataProductsRatings) is a system-wide AttachedRating relationship count, not scoped to products specifically -- Egeria's relationship count can't filter by one end's type without a graph traversal -- and is omitted from the tile entirely when zero rather than showing a fake average.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-products

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Popularity / Usage Metrics

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-products

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-products

---

## Create Glossary Term

### Display Name
Open Exceptions

### Summary
Count of Exception relationships currently attached to any element.

### Description
Count of open Exception governance relationships awaiting review.

### Usage
Despite the "Open" in the tile label, no open/resolved status filter is applied -- this counts every Exception relationship that exists. Also: pyegeria's own count_relationships() docstring flags that this get_relationships-based path can disagree materially with a native MetadataExpert count for this exact relationship type (one comparison found 55 vs 276 -- tracked as PY-18 in egeria-python's PYEGERIA_ISSUES.md). Treat this number as one counting method's answer, not a verified ground truth.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-exceptions

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Quality Metrics

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Governance View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-exceptions

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-exceptions

---

## Create Glossary Term

### Display Name
People / Contributors

### Summary
Native count of active Person elements in the repository.

### Description
Count of Person actor profiles (registered contributors).

### Usage
Despite the tile label "People / Contributors", this counts every Person element that exists, not people who have actually contributed anything -- there is no activity/contribution filter here. A person registered in the repository but who has never edited, rated, or commented on anything still counts. "Feedback Items" (a separate signal, same People & Community section) is the closer proxy for actual contribution activity.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-people

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-people

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-people

---

## Add Member to Collection

### Collection Id
Collection::Popularity / Usage Metrics

### Element Id
Term::overview-kpi-people

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-people

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-people

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-people

---

## Create Glossary Term

### Display Name
Active Communities

### Summary
Native count of Community elements in the repository.

### Description
Count of Community elements — collaboration groups.

### Usage
Same shape as People/Contributors' caveat: despite "Active" in the tile label, there is no participation/activity filter -- a Community with no members or posts counts the same as a thriving one.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-communities

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-communities

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-communities

---

## Add Member to Collection

### Collection Id
Collection::Popularity / Usage Metrics

### Element Id
Term::overview-kpi-communities

---

## Add Member to Collection

### Collection Id
Collection::Community View

### Element Id
Term::overview-kpi-communities

---

## Create Glossary Term

### Display Name
Supply Chains

### Summary
Native count of InformationSupplyChain elements in the repository.

### Description
Count of InformationSupplyChain elements — end-to-end data flows.

### Usage
Counts chain DEFINITIONS regardless of whether they have any segments or implementation wired up -- a supply chain that is just a name with no linked solution components beneath it counts the same as a fully modeled one. Not a measure of how much of the business is actually mapped end-to-end.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-isc

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::Popularity / Usage Metrics

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-isc

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-isc

---

## Create Glossary Term

### Display Name
Solution Blueprints

### Summary
Native count of SolutionBlueprint elements in the repository.

### Description
Count of SolutionBlueprint elements — reusable solution designs.

### Usage
Counts blueprint DEFINITIONS regardless of composition depth -- a blueprint with no SolutionComponents actually linked beneath it counts the same as a fully detailed one.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-blueprints

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::Popularity / Usage Metrics

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-blueprints

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-blueprints

---

## Create Glossary Term

### Display Name
Semantic Grounding

### Summary
Count and percentage of SemanticAssignment relationships, as a proxy for assets grounded with business meaning for AI.

### Description
Share of assets linked to glossary terms via SemanticAssignment — the meaning layer that grounds AI.

### Usage
CAVEAT, confirmed live 2026-08-01: SemanticAssignment is NOT Asset-scoped. In this dataset, of 397 SemanticAssignment relationships, 348 (87.7%) connect to GovernanceActionProcess elements (governance workflow automation, e.g. subscription-management processes) -- not data assets. The remainder connect to schema-level elements (DataField, TabularColumn, APIParameter, ...), which are not Asset-typed themselves either (they'd need one more hop to their anchor Asset). Zero of the 397 relationships connect directly to an Asset element. Treat this percentage as an upper bound on true asset grounding, not a measured grounded-asset rate, until NEXT-24's audit resolves the scoping (e.g. by filtering to relationships whose non-term end is Asset-typed, or by following schema elements up to their anchor Asset).

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-grounding

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::AI / Context Intelligence Metrics

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Steward View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Data Owner View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Consumer View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Engineering View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Architecture View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::App/AI Builder View

### Element Id
Term::overview-kpi-grounding

---

## Add Member to Collection

### Collection Id
Collection::Privacy View

### Element Id
Term::overview-kpi-grounding

---

## Create Glossary Term

### Display Name
Ownership Coverage

### Summary
Count and percentage of elements carrying an Ownership classification, as a percentage of Assets.

### Description
Share of assets carrying an Ownership classification — a named owner responsible for management/governance decisions. Distinct from Governed Coverage (classification-based); data mesh names 'clean, owned, product-based data' as its own foundation for trustworthy AI consumption.

### Usage
Same scoping shape as Governed Coverage's caveat: the numerator (Ownership-classified elements) is NOT Asset-scoped -- ANY element type with the classification counts -- while the denominator (percentage base) IS Asset-only. Not yet fully audited for exactly which element types carry Ownership in this dataset (spot-checked live 2026-08-01: at least SolutionActorRole appears as an owner-type value) -- a fuller by-owner-type breakdown is what `byOwnerType` in the raw payload already returns, just not yet surfaced in this tile's UI.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-ownership

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-ownership

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-ownership

---

## Add Member to Collection

### Collection Id
Collection::AI / Context Intelligence Metrics

### Element Id
Term::overview-kpi-ownership

---

## Create Glossary Term

### Display Name
AI-Ready Assets

### Summary
Count and percentage of Asset elements carrying >=1 governance classification AND a non-empty description AND >=1 DataFlow relationship, simultaneously -- a true composite (NEXT-18), not three independent counts.

### Description
Count of Asset elements that are simultaneously governed, documented, and lineage-traced -- the composite gate for "safe to serve as AI context".

### Usage
The AND-gate means the true bottleneck is whichever underlying signal is weakest, and that's very often lineage, not governance or documentation -- confirmed live 2026-08-04 on this dataset: 1,743 cataloged, 365 documented (21%), 584 classified (governance, not Asset-scoped -- can exceed cataloged, see Governed Coverage's own caveat), but only 8 assets carry any DataFlow relationship at all, so AI-Ready lands at 4 (0.2%) even though documentation and classification are both far higher individually. Read a low number here as "go look at the funnel stage with the steepest drop" (usually lineage), not as "nothing here is AI-ready-adjacent" -- see the Context Readiness Funnel panel for the per-stage breakdown that explains which gate is binding.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-ai-ready

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Overview KPIs

### Element Id
Term::overview-kpi-ai-ready

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-ai-ready

---

## Add Member to Collection

### Collection Id
Collection::AI / Context Intelligence Metrics

### Element Id
Term::overview-kpi-ai-ready

---

## Add Member to Collection

### Collection Id
Collection::Security View

### Element Id
Term::overview-kpi-ai-ready

---

## Create Glossary Term

### Display Name
Risk & Compliance

### Summary
Count of Asset-typed elements classified Confidentiality, out of all Asset-hierarchy elements checked.

### Description
Count of Asset-typed elements carrying a Confidentiality classification.

### Usage
Proxy for regulatory exposure surface -- more classified elements need active governance, this is not itself a measure of risk being controlled. Scoped to the Asset type hierarchy specifically -- distinct from Governed Coverage's own `byClassification["Confidentiality"]`, which is NOT Asset-scoped (any element type carrying the classification counts there). The two numbers can legitimately differ a lot in the same dataset (e.g. 5 vs 1) and both are correct -- different populations, not a discrepancy.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-bv-risk

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Business Value Signals

### Element Id
Term::overview-kpi-bv-risk

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-bv-risk

---

## Create Glossary Term

### Display Name
Productivity

### Summary
Percentage of Asset-hierarchy elements carrying a non-empty description, out of all elements checked.

### Description
Share of Asset-hierarchy elements with a non-empty description.

### Usage
Proxy for self-service findability -- a described asset is easier to evaluate without a steward's help. Doesn't measure actual query/access frequency, so treat it as a leading indicator, not a usage measure.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-bv-productivity

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Business Value Signals

### Element Id
Term::overview-kpi-bv-productivity

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-bv-productivity

---

## Create Glossary Term

### Display Name
Trust & Adoption

### Summary
Count of published DigitalProduct definitions (reuses the same live count the Data Products KPI tile shows).

### Description
Count of published DigitalProduct definitions.

### Usage
Counts product DEFINITIONS, not adoption -- no rating/usage signal is wired. No `AttachedRating` relationships exist against DigitalProduct in a typical demo dataset (confirmed live), so a rating average is honestly omitted rather than faked; a real adoption signal would need one wired (e.g. subscription counts).

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-bv-trust

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Business Value Signals

### Element Id
Term::overview-kpi-bv-trust

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-bv-trust

---

## Create Glossary Term

### Display Name
Cost Avoidance

### Summary
Count of elements carrying the ConsolidatedDuplicate classification (absorbed a detected duplicate).

### Description
Count of elements classified ConsolidatedDuplicate.

### Usage
A candidate-for-archival signal, not a cost figure -- no dollar estimate is attached. A real zero in a dataset with no duplicate-detection activity yet run is an honest answer, not evidence the feature is broken.

### Glossary Name
Egeria Dashboard Analytics

### Qualified Name
Term::overview-kpi-bv-cost

### Version Identifier
1.0

---

## Add Member to Collection

### Collection Id
Collection::Business Value Signals

### Element Id
Term::overview-kpi-bv-cost

---

## Add Member to Collection

### Collection Id
Collection::Live Metrics

### Element Id
Term::overview-kpi-bv-cost

---

