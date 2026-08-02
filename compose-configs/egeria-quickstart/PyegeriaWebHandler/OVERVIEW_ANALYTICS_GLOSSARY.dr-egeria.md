<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Dashboard Analytics — Glossary & Collections

> Loadable **Dr.Egeria** document that governs the Overview dashboard's own
> metrics as real Egeria elements: one **GlossaryTerm** per metric (Summary/
> Description/Usage — Usage carries caveats, e.g. scoping mismatches found
> during the NEXT-24 audit), grouped under a **RootCollection** with
> sub-collections (by app, by provenance). Generated from `overview_specs.py`'s
> `_TILES` — the single source of truth. Regenerate with
> `gen_dashboard_glossary.py` after editing a tile's `summary`/`description`/
> `usage` fields.
>
> Design: `OVERVIEW_METRIC_GOVERNANCE.md` (NEXT-24), Phase A.
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

## Create Glossary Term

### Display Name
Cataloged Assets

### Summary
Sum of active elements across 7 named asset/infrastructure types.

### Description
Sum of counts of the key asset/infrastructure types in the catalog.

### Usage
Fixed to a hand-picked list of 7 type names (DataStore, DataSet, DeployedSoftwareComponent, ITInfrastructure, DeployedAPI, Process, DataFeed) -- NOT every Asset subtype in the type system, and NOT the same population context_readiness_funnel's 'cataloged' stage uses (that one counts the broad Asset supertype directly, a different, usually larger number). Treat this as "the types we've chosen to headline", not a canonical total asset count -- see OVERVIEW_NEXT_STEPS.md's "Asset definition" open decision for the unresolved discrepancy between this and the growth-chart's own asset series.

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

## Create Glossary Term

### Display Name
Data Products

### Summary
Native count of DigitalProduct elements defined in the catalog.

### Description
Count of DigitalProduct elements published for consumption.

### Usage
No lifecycle/status filter is applied -- a DigitalProduct still in DRAFT and never released to consumers counts identically to one that is PUBLISHED and actively subscribed to. This is a count of product DEFINITIONS, not a measure of adoption or usage.

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

