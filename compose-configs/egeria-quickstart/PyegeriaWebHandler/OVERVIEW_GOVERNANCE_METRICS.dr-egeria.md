<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Governance Metrics

> Loadable **Dr.Egeria** document that materialises the Overview dashboard's
> fixed (non-generic) `pyegeria.view.overview_metrics` functions as real
> `GovernanceMetric` elements, each linked via `GovernanceResults` to a real
> `Report` (report-spec-backed, runnable via `/api/report-specs/execute`), plus
> a per-metric `InformationSupplyChain` documenting the conceptual data flow
> (data source → analytic function → Report → GovernanceMetric) — a real
> Collection membership for the two real artifacts today, text-only for the
> two stages that aren't Egeria elements yet. Generated from
> `pyegeria.view.analytic_registry` + `analytic_demo_specs` — the single
> source of truth. Regenerate with `gen_governance_metrics.py`. Upsert-safe —
> re-running this file (e.g. after a repository reset) is always correct.
> **Run with VALIDATE first, then PROCESS.**

---

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Active Contributors Metric Report

### Description
Live computation backing the Active Contributors governance metric.

### Report Spec
Analytic Demo - Active Contributors

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Active Contributors

### Summary
Distinct usernames behind at least one feedback relationship (ratings/comments/likes/tags/noteLogs) -- an engagement signal feedback_summary's raw relationship counts don't give you (one prolific commenter vs. many occasional ones).

### Scope
Fixed to Collaboration OMAS's feedback relationship types -- not a parameter.

### Usage
Distinct usernames behind at least one feedback relationship (ratings/comments/likes/tags/noteLogs) -- pick BAR below for a by-type breakdown. A real engagement signal Feedback Summary's raw relationship counts don't give you: ten comments from one person and ten comments from ten people both show up as '10' there, but differently here. FIXED metric -- Fixed to Collaboration OMAS's feedback relationship types -- not a parameter. This spec always returns that one metric. Result shape: dict (contributors, byType).

### Implementation Description
pyegeria.view.overview_metrics.active_contributors() -- exposed as Report Spec "Analytic Demo - Active Contributors" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (contributors, byType).

### Measurement
dict (contributors, byType). Fixed to Collaboration OMAS's feedback relationship types -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Active Contributors

### Data Asset
Active Contributors Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Active Contributors Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Active Contributors" governance metric: a data source (the Egeria relationship/classification/property active_contributors() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.active_contributors(), exposed as Report Spec "Analytic Demo - Active Contributors", instantiated as the Report "Active Contributors Metric Report", measured by the GovernanceMetric "Active Contributors". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Active Contributors Data Flow

### Element Id
Active Contributors Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Active Contributors Data Flow

### Element Id
Active Contributors

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
AI-Ready Assets (Composite) Metric Report

### Description
Live computation backing the AI-Ready Assets (Composite) governance metric.

### Report Spec
Analytic Demo - AI-Ready Assets

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
AI-Ready Assets (Composite)

### Summary
The true 'AI-Ready' composite: Asset elements that are governed AND documented AND lineage-traced simultaneously, not three independent counts intersected after the fact. First real implementation of the composite/derived analytic metric pattern -- see NEXT-18 (egeria-workspaces BACKLOG.md) for why this pattern didn't exist here before. Takes two leading clients (mgr, ce), same convention as semantic_grounding/context_readiness_funnel.

### Scope
Fixed to governed+documented+lineage-traced over Asset elements -- not a parameter.

### Usage
The actual per-asset intersection context_readiness_funnel's 'aiReady' field can't give you: Asset elements that are governed AND documented AND lineage-traced, all three, checked per element from a single capped Asset fetch plus one DataFlow relationship query (not three separate counts intersected client-side after the fact -- see the function's own docstring for the exact field-name gotchas this hit while being built, e.g. find_metadata_elements results key their GUID as 'elementGUID' but a relationship end's GUID is plain 'guid'). 'total' is the (possibly capped) Asset population actually checked -- divide aiReadyCount by total for a percentage, don't assume it's the full catalog. First worked example of the composite/derived analytic metric pattern NEXT-18 (egeria-workspaces BACKLOG.md) flagged as missing. FIXED metric -- Fixed to governed+documented+lineage-traced over Asset elements -- not a parameter. This spec always returns that one metric. Result shape: dict (aiReadyCount, total, capped).

### Implementation Description
pyegeria.view.overview_metrics.ai_ready_assets() -- exposed as Report Spec "Analytic Demo - AI-Ready Assets" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (aiReadyCount, total, capped).

### Measurement
dict (aiReadyCount, total, capped). Fixed to governed+documented+lineage-traced over Asset elements -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
AI-Ready Assets (Composite)

### Data Asset
AI-Ready Assets (Composite) Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
AI-Ready Assets (Composite) Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "AI-Ready Assets (Composite)" governance metric: a data source (the Egeria relationship/classification/property ai_ready_assets() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.ai_ready_assets(), exposed as Report Spec "Analytic Demo - AI-Ready Assets", instantiated as the Report "AI-Ready Assets (Composite) Metric Report", measured by the GovernanceMetric "AI-Ready Assets (Composite)". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
AI-Ready Assets (Composite) Data Flow

### Element Id
AI-Ready Assets (Composite) Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
AI-Ready Assets (Composite) Data Flow

### Element Id
AI-Ready Assets (Composite)

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Business Value Signals Metric Report

### Description
Live computation backing the Business Value Signals governance metric.

### Report Spec
Analytic Demo - Business Value Signals

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Business Value Signals

### Summary
Real signals behind the four Overview dashboard Business Value tiles (Risk & Compliance, Productivity, Trust & Adoption, Cost Avoidance): Confidentiality-classified asset count, described-asset count, ConsolidatedDuplicate-flagged element count -- all proxies with a documented causal-claim caveat, not direct measures (NEXT-9).

### Scope
Fixed to the Asset type hierarchy and Confidentiality/ConsolidatedDuplicate classifications -- not a parameter.

### Usage
Real signals behind the Overview dashboard's four Business Value tiles (NEXT-9): confidentialCount and describedCount come from a single Asset-hierarchy fetch (assetTotal is that fetch's size, assetCapped=true if it hit DEFAULT_CAP); duplicateCount is a separate ConsolidatedDuplicate classification count. Each is a documented proxy, not a direct measure -- see business_value_signals()'s docstring for the causal-claim caveat that belongs with each field before treating it as more than that. FIXED metric -- Fixed to the Asset type hierarchy and Confidentiality/ConsolidatedDuplicate classifications -- not a parameter. This spec always returns that one metric. Result shape: dict (assetTotal, assetCapped, confidentialCount, describedCount, duplicateCount).

### Implementation Description
pyegeria.view.overview_metrics.business_value_signals() -- exposed as Report Spec "Analytic Demo - Business Value Signals" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (assetTotal, assetCapped, confidentialCount, describedCount, duplicateCount).

### Measurement
dict (assetTotal, assetCapped, confidentialCount, describedCount, duplicateCount). Fixed to the Asset type hierarchy and Confidentiality/ConsolidatedDuplicate classifications -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Business Value Signals

### Data Asset
Business Value Signals Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Business Value Signals Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Business Value Signals" governance metric: a data source (the Egeria relationship/classification/property business_value_signals() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.business_value_signals(), exposed as Report Spec "Analytic Demo - Business Value Signals", instantiated as the Report "Business Value Signals Metric Report", measured by the GovernanceMetric "Business Value Signals". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Business Value Signals Data Flow

### Element Id
Business Value Signals Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Business Value Signals Data Flow

### Element Id
Business Value Signals

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Certifications & Exceptions Summary Metric Report

### Description
Live computation backing the Certifications & Exceptions Summary governance metric.

### Report Spec
Analytic Demo - Certifications and Exceptions

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Certifications & Exceptions Summary

### Summary
Active/expiring Certification relationships, licenses, and open Exception counts.

### Scope
Fixed to the Certification and Exception relationship types -- not a parameter.

### Usage
Active/expiring Certification relationships and License counts. 'exceptions' is a GENERAL open-governance-Exception count (any Exception relationship in the repository) -- it is NOT scoped to certifications/licenses specifically, despite sitting in this same summary; treat it as a separate metric riding along here. FIXED metric -- Fixed to the Certification and Exception relationship types -- not a parameter. This spec always returns that one metric. Result shape: dict (active, expiring90, soon, licenses, exceptions).

### Implementation Description
pyegeria.view.overview_metrics.certifications_summary() -- exposed as Report Spec "Analytic Demo - Certifications and Exceptions" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (active, expiring90, soon, licenses, exceptions).

### Measurement
dict (active, expiring90, soon, licenses, exceptions). Fixed to the Certification and Exception relationship types -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Certifications & Exceptions Summary

### Data Asset
Certifications & Exceptions Summary Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Certifications & Exceptions Summary Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Certifications & Exceptions Summary" governance metric: a data source (the Egeria relationship/classification/property certifications_summary() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.certifications_summary(), exposed as Report Spec "Analytic Demo - Certifications and Exceptions", instantiated as the Report "Certifications & Exceptions Summary Metric Report", measured by the GovernanceMetric "Certifications & Exceptions Summary". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Certifications & Exceptions Summary Data Flow

### Element Id
Certifications & Exceptions Summary Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Certifications & Exceptions Summary Data Flow

### Element Id
Certifications & Exceptions Summary

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
AI Context Readiness Funnel Metric Report

### Description
Live computation backing the AI Context Readiness Funnel governance metric.

### Report Spec
Analytic Demo - AI Context Readiness

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
AI Context Readiness Funnel

### Summary
Cataloged -> Documented -> Classified -> Lineage-traced -> AI-Ready funnel counts. Takes two leading clients (mgr, ce) -- the executor supplies the same EgeriaTech instance for both, matching semantic_grounding's convention. This function's own aiReady stays None always by design -- it's four independent counts, and aiReady needs a true cross-criteria intersection instead. Pair with ai_ready_assets (below) for that -- overview_handler.py calls both and merges the result.

### Scope
Fixed 5-stage readiness definition baked into the function body -- not a parameter.

### Usage
'cataloged' (Asset supertype count), 'documented' (Assets with a non-empty description, capped at DEFAULT_CAP -- a floor, not exact, on a large catalog), 'classified' (elements matching ANY of the same governance classifications governed_coverage uses), and 'lineage' (count of DataFlow relationships -- design/ business lineage, distinct from OpenLineage's operational lineage) are all computed as of 2026-08-01. 'aiReady' stays None from this function ALWAYS, by design -- these four are independent counts, not a per-asset check, so they can't answer 'how many assets are ALL of these at once'. See 'Analytic Demo - AI-Ready Assets' (below) for that -- a genuinely different function, not a missing field on this one. FIXED metric -- Fixed 5-stage readiness definition baked into the function body -- not a parameter. This spec always returns that one metric. Result shape: dict (cataloged, documented, classified, lineage, aiReady).

### Implementation Description
pyegeria.view.overview_metrics.context_readiness_funnel() -- exposed as Report Spec "Analytic Demo - AI Context Readiness" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (cataloged, documented, classified, lineage, aiReady).

### Measurement
dict (cataloged, documented, classified, lineage, aiReady). Fixed 5-stage readiness definition baked into the function body -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
AI Context Readiness Funnel

### Data Asset
AI Context Readiness Funnel Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
AI Context Readiness Funnel Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "AI Context Readiness Funnel" governance metric: a data source (the Egeria relationship/classification/property context_readiness_funnel() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.context_readiness_funnel(), exposed as Report Spec "Analytic Demo - AI Context Readiness", instantiated as the Report "AI Context Readiness Funnel Metric Report", measured by the GovernanceMetric "AI Context Readiness Funnel". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
AI Context Readiness Funnel Data Flow

### Element Id
AI Context Readiness Funnel Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
AI Context Readiness Funnel Data Flow

### Element Id
AI Context Readiness Funnel

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Usage Context Coverage Metric Report

### Description
Live computation backing the Usage Context Coverage governance metric.

### Report Spec
Analytic Demo - Contextualised Coverage

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Usage Context Coverage

### Summary
Percent of Assets given business/solution-design context via an ImplementedBy relationship to a SolutionComponent. A proxy, not the literal 'participates in an ISC/blueprint' metric -- confirms some solution-design context exists, not that the specific SolutionComponent is itself wired into an ISC/blueprint (a second hop this function doesn't take). Takes two leading clients (mgr, ce), same convention as semantic_grounding.

### Scope
Fixed to the ImplementedBy relationship, filtered to Asset-subtype ends -- not a parameter.

### Usage
Percent of Assets connected to a SolutionComponent via ImplementedBy -- a proxy for 'has some solution-design context', not the literal 'participates in an ISC/blueprint'. FIXED metric -- Fixed to the ImplementedBy relationship, filtered to Asset-subtype ends -- not a parameter. This spec always returns that one metric. Result shape: dict (contextualisedCount, assetTotal, contextualisedPct).

### Implementation Description
pyegeria.view.overview_metrics.contextualised_coverage() -- exposed as Report Spec "Analytic Demo - Contextualised Coverage" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (contextualisedCount, assetTotal, contextualisedPct).

### Measurement
dict (contextualisedCount, assetTotal, contextualisedPct). Fixed to the ImplementedBy relationship, filtered to Asset-subtype ends -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Usage Context Coverage

### Data Asset
Usage Context Coverage Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Usage Context Coverage Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Usage Context Coverage" governance metric: a data source (the Egeria relationship/classification/property contextualised_coverage() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.contextualised_coverage(), exposed as Report Spec "Analytic Demo - Contextualised Coverage", instantiated as the Report "Usage Context Coverage Metric Report", measured by the GovernanceMetric "Usage Context Coverage". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Usage Context Coverage Data Flow

### Element Id
Usage Context Coverage Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Usage Context Coverage Data Flow

### Element Id
Usage Context Coverage

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Engagement Over Time Metric Report

### Description
Live computation backing the Engagement Over Time governance metric.

### Report Spec
Analytic Demo - Engagement Over Time

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Engagement Over Time

### Summary
Weekly-bucketed feedback-event trend (comments/ratings/likes/tags/noteLogs), zero-filled across the trailing window -- reuses the same 5 relationship-type queries feedback_summary() already makes, keeping createTime instead of only the count. Takes ce as its leading client.

### Scope
Fixed to Collaboration OMAS's 5 feedback relationship types -- weeks tunes the window, not what's measured.

### Usage
Weekly-bucketed feedback-event trend (comments/ratings/likes/tags/noteLogs), zero-filled across the trailing window. Run with output_format SERIES for a chart. FIXED metric -- Fixed to Collaboration OMAS's 5 feedback relationship types -- weeks tunes the window, not what's measured. This spec always returns that one metric. Result shape: list[dict] (time series: {week, comments, ratings, likes, tags, noteLogs, total}). Default params (edit/override at run time): {'weeks': 12}.

### Implementation Description
pyegeria.view.overview_metrics.engagement_series() -- exposed as Report Spec "Analytic Demo - Engagement Over Time" via pyegeria's analytic function registry (analytic_registry.py). Returns: list[dict] (week, comments, ratings, likes, tags, noteLogs, total), oldest week first.

### Measurement
list[dict] (week, comments, ratings, likes, tags, noteLogs, total), oldest week first. Fixed to Collaboration OMAS's 5 feedback relationship types -- weeks tunes the window, not what's measured.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Engagement Over Time

### Data Asset
Engagement Over Time Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Engagement Over Time Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Engagement Over Time" governance metric: a data source (the Egeria relationship/classification/property engagement_series() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.engagement_series(), exposed as Report Spec "Analytic Demo - Engagement Over Time", instantiated as the Report "Engagement Over Time Metric Report", measured by the GovernanceMetric "Engagement Over Time". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Engagement Over Time Data Flow

### Element Id
Engagement Over Time Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Engagement Over Time Data Flow

### Element Id
Engagement Over Time

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Crowd-sourced Feedback Summary Metric Report

### Description
Live computation backing the Crowd-sourced Feedback Summary governance metric.

### Report Spec
Analytic Demo - Feedback Summary

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Crowd-sourced Feedback Summary

### Summary
Crowd-sourced feedback counts (ratings/comments/likes/tags/noteLogs) by type, via Collaboration OMAS relationships.

### Scope
Fixed to Collaboration OMAS's feedback relationship types -- not a parameter.

### Usage
Ratings/comments/likes/tags/noteLogs counts by type -- pick BAR below for a by-type breakdown chart. A trend over time isn't available from this metric yet (feedback_summary is a point-in-time snapshot, not a series) -- a real gap for later. FIXED metric -- Fixed to Collaboration OMAS's feedback relationship types -- not a parameter. This spec always returns that one metric. Result shape: dict (byType, total).

### Implementation Description
pyegeria.view.overview_metrics.feedback_summary() -- exposed as Report Spec "Analytic Demo - Feedback Summary" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (byType, total).

### Measurement
dict (byType, total). Fixed to Collaboration OMAS's feedback relationship types -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Crowd-sourced Feedback Summary

### Data Asset
Crowd-sourced Feedback Summary Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Crowd-sourced Feedback Summary Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Crowd-sourced Feedback Summary" governance metric: a data source (the Egeria relationship/classification/property feedback_summary() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.feedback_summary(), exposed as Report Spec "Analytic Demo - Feedback Summary", instantiated as the Report "Crowd-sourced Feedback Summary Metric Report", measured by the GovernanceMetric "Crowd-sourced Feedback Summary". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Crowd-sourced Feedback Summary Data Flow

### Element Id
Crowd-sourced Feedback Summary Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Crowd-sourced Feedback Summary Data Flow

### Element Id
Crowd-sourced Feedback Summary

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Governance Classification Coverage Metric Report

### Description
Live computation backing the Governance Classification Coverage governance metric.

### Report Spec
Analytic Demo - Governance Coverage

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Governance Classification Coverage

### Summary
Share of assets carrying at least one governance classification, plus a by-classification / top-zones breakdown.

### Scope
Fixed to GOVERNANCE_CLASSIFICATIONS: ZoneMembership, Confidentiality, Criticality, Impact, Retention -- not a parameter.

### Usage
Count of elements carrying at least one governance classification (ZoneMembership/Confidentiality/Criticality/Impact/Retention) -- NOT a percentage despite 'coverage' in the name (there's no cheap total-elements denominator to divide by yet). governedCapped=true means the query hit its result-page cap (DEFAULT_CAP), so governedCount is a floor, not exact, when true. byClassification and topZones are nested breakdowns of the same governedCount elements -- pick BAR below for a chart of byClassification. FIXED metric -- Fixed to GOVERNANCE_CLASSIFICATIONS: ZoneMembership, Confidentiality, Criticality, Impact, Retention -- not a parameter. This spec always returns that one metric. Result shape: dict (governedCount, governedCapped, byClassification, topZones).

### Implementation Description
pyegeria.view.overview_metrics.governed_coverage() -- exposed as Report Spec "Analytic Demo - Governance Coverage" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (governedCount, governedCapped, byClassification, topZones).

### Measurement
dict (governedCount, governedCapped, byClassification, topZones). Fixed to GOVERNANCE_CLASSIFICATIONS: ZoneMembership, Confidentiality, Criticality, Impact, Retention -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Governance Classification Coverage

### Data Asset
Governance Classification Coverage Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Governance Classification Coverage Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Governance Classification Coverage" governance metric: a data source (the Egeria relationship/classification/property governed_coverage() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.governed_coverage(), exposed as Report Spec "Analytic Demo - Governance Coverage", instantiated as the Report "Governance Classification Coverage Metric Report", measured by the GovernanceMetric "Governance Classification Coverage". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Governance Classification Coverage Data Flow

### Element Id
Governance Classification Coverage Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Governance Classification Coverage Data Flow

### Element Id
Governance Classification Coverage

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Karma Leaderboard Metric Report

### Description
Live computation backing the Karma Leaderboard governance metric.

### Report Spec
Analytic Demo - Karma Leaderboard

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Karma Leaderboard

### Summary
Top-N people by karma -- one bounded ContributionRecord fetch, karmaPoints is a scalar property on the record itself (not derived from counting related things), filtered to the given anchor type(s) via each record's own Anchors classification.

### Scope
Fixed to ContributionRecord.karmaPoints -- top_n and anchor_types tune the result but don't change what's being measured.

### Usage
Top-N people by karma (ContributionRecord.karmaPoints, anchored via Anchors classification). FIXED metric -- Fixed to ContributionRecord.karmaPoints -- top_n and anchor_types tune the result but don't change what's being measured. This spec always returns that one metric. Result shape: list[dict] (name, karmaPoints, anchorGuid, anchorType). Default params (edit/override at run time): {'top_n': 10}.

### Implementation Description
pyegeria.view.overview_metrics.karma_leaderboard() -- exposed as Report Spec "Analytic Demo - Karma Leaderboard" via pyegeria's analytic function registry (analytic_registry.py). Returns: list[dict] (name, karmaPoints, anchorGuid, anchorType), longest-karma first.

### Measurement
list[dict] (name, karmaPoints, anchorGuid, anchorType), longest-karma first. Fixed to ContributionRecord.karmaPoints -- top_n and anchor_types tune the result but don't change what's being measured.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Karma Leaderboard

### Data Asset
Karma Leaderboard Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Karma Leaderboard Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Karma Leaderboard" governance metric: a data source (the Egeria relationship/classification/property karma_leaderboard() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.karma_leaderboard(), exposed as Report Spec "Analytic Demo - Karma Leaderboard", instantiated as the Report "Karma Leaderboard Metric Report", measured by the GovernanceMetric "Karma Leaderboard". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Karma Leaderboard Data Flow

### Element Id
Karma Leaderboard Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Karma Leaderboard Data Flow

### Element Id
Karma Leaderboard

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Orphan Glossary Terms Metric Report

### Description
Live computation backing the Orphan Glossary Terms governance metric.

### Report Spec
Analytic Demo - Orphan Glossary Terms

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Orphan Glossary Terms

### Summary
Approved-but-unassigned glossary terms -- a term with no SemanticAssignment relationship to anything was authored but never put to use grounding the catalog. One bounded SemanticAssignment fetch, distinct GlossaryTerm-end GUID count is the 'referenced' set; orphan = term total - referenced. Takes two leading clients (mgr, ce), same convention as semantic_grounding.

### Scope
Fixed to the SemanticAssignment relationship type and GlossaryTerm elements -- not a parameter.

### Usage
Approved-but-unassigned glossary terms -- terms with no SemanticAssignment relationship to anything. orphanCount = termTotal - referencedCount. FIXED metric -- Fixed to the SemanticAssignment relationship type and GlossaryTerm elements -- not a parameter. This spec always returns that one metric. Result shape: dict (termTotal, referencedCount, orphanCount).

### Implementation Description
pyegeria.view.overview_metrics.orphan_glossary_terms() -- exposed as Report Spec "Analytic Demo - Orphan Glossary Terms" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (termTotal, referencedCount, orphanCount).

### Measurement
dict (termTotal, referencedCount, orphanCount). Fixed to the SemanticAssignment relationship type and GlossaryTerm elements -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Orphan Glossary Terms

### Data Asset
Orphan Glossary Terms Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Orphan Glossary Terms Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Orphan Glossary Terms" governance metric: a data source (the Egeria relationship/classification/property orphan_glossary_terms() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.orphan_glossary_terms(), exposed as Report Spec "Analytic Demo - Orphan Glossary Terms", instantiated as the Report "Orphan Glossary Terms Metric Report", measured by the GovernanceMetric "Orphan Glossary Terms". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Orphan Glossary Terms Data Flow

### Element Id
Orphan Glossary Terms Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Orphan Glossary Terms Data Flow

### Element Id
Orphan Glossary Terms

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Ownership Coverage Metric Report

### Description
Live computation backing the Ownership Coverage governance metric.

### Report Spec
Analytic Demo - Ownership Coverage

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Ownership Coverage

### Summary
Share of assets carrying an Ownership classification (a named owner responsible for management/governance decisions), plus a by-owner-type breakdown. Distinct from governed_coverage -- data mesh literature names 'clean, owned, product-based data' as its own foundation for trustworthy AI consumption, not a synonym for governance-classification coverage.

### Scope
Fixed to the Ownership classification -- not a parameter.

### Usage
Count of elements carrying an Ownership classification -- NOT a percentage, same caveat as Governance Coverage (no cheap total-elements denominator yet). ownershipCapped=true means the query hit its result-page cap (DEFAULT_CAP), so ownershipCount is a floor, not exact, when true. byOwnerType is a nested breakdown of the same ownershipCount elements by the owner's type (Person, Team, SolutionActorRole, ...) -- pick BAR below for a chart of byOwnerType. FIXED metric -- Fixed to the Ownership classification -- not a parameter. This spec always returns that one metric. Result shape: dict (ownershipCount, ownershipCapped, byOwnerType).

### Implementation Description
pyegeria.view.overview_metrics.ownership_coverage() -- exposed as Report Spec "Analytic Demo - Ownership Coverage" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (ownershipCount, ownershipCapped, byOwnerType).

### Measurement
dict (ownershipCount, ownershipCapped, byOwnerType). Fixed to the Ownership classification -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Ownership Coverage

### Data Asset
Ownership Coverage Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Ownership Coverage Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Ownership Coverage" governance metric: a data source (the Egeria relationship/classification/property ownership_coverage() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.ownership_coverage(), exposed as Report Spec "Analytic Demo - Ownership Coverage", instantiated as the Report "Ownership Coverage Metric Report", measured by the GovernanceMetric "Ownership Coverage". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Ownership Coverage Data Flow

### Element Id
Ownership Coverage Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Ownership Coverage Data Flow

### Element Id
Ownership Coverage

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
People & Community Counts Metric Report

### Description
Live computation backing the People & Community Counts governance metric.

### Report Spec
Analytic Demo - People and Community

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
People & Community Counts

### Summary
Counts of Person / Team / Organization / ITProfile / Community actor profiles.

### Scope
Fixed to Person/Team/Organization/ITProfile/Community -- not a parameter.

### Usage
Counts of Person/Team/Organization/ITProfile/Community actor profiles. FIXED metric -- Fixed to Person/Team/Organization/ITProfile/Community -- not a parameter. This spec always returns that one metric. Result shape: dict (persons, teams, organizations, itProfiles, communities).

### Implementation Description
pyegeria.view.overview_metrics.people_counts() -- exposed as Report Spec "Analytic Demo - People and Community" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (persons, teams, organizations, itProfiles, communities).

### Measurement
dict (persons, teams, organizations, itProfiles, communities). Fixed to Person/Team/Organization/ITProfile/Community -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
People & Community Counts

### Data Asset
People & Community Counts Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
People & Community Counts Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "People & Community Counts" governance metric: a data source (the Egeria relationship/classification/property people_counts() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.people_counts(), exposed as Report Spec "Analytic Demo - People and Community", instantiated as the Report "People & Community Counts Metric Report", measured by the GovernanceMetric "People & Community Counts". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
People & Community Counts Data Flow

### Element Id
People & Community Counts Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
People & Community Counts Data Flow

### Element Id
People & Community Counts

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Semantic Grounding Coverage Metric Report

### Description
Live computation backing the Semantic Grounding Coverage governance metric.

### Report Spec
Analytic Demo - Semantic Grounding

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Semantic Grounding Coverage

### Summary
SemanticAssignment relationship count and coverage percent -- the meaning layer that grounds AI. Takes two leading clients (mgr, ce) -- the executor supplies the same EgeriaTech instance for both.

### Scope
Fixed to the SemanticAssignment relationship type -- not a parameter.

### Usage
groundingLinks = count of SemanticAssignment relationships (term<->asset). groundingPct = that count as a percent of the broad Asset supertype count (i.e. 'percent of Assets' as the denominator, capped at 100 -- an asset with multiple assignments can push the raw ratio over 100%, which is why it's capped, not because grounding coverage is literally bounded there). A per-asset detail breakdown (which assets are/aren't grounded) isn't available from this metric --  a real gap for later. FIXED metric -- Fixed to the SemanticAssignment relationship type -- not a parameter. This spec always returns that one metric. Result shape: dict (groundingLinks, groundingPct).

### Implementation Description
pyegeria.view.overview_metrics.semantic_grounding() -- exposed as Report Spec "Analytic Demo - Semantic Grounding" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (groundingLinks, groundingPct).

### Measurement
dict (groundingLinks, groundingPct). Fixed to the SemanticAssignment relationship type -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Semantic Grounding Coverage

### Data Asset
Semantic Grounding Coverage Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Semantic Grounding Coverage Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Semantic Grounding Coverage" governance metric: a data source (the Egeria relationship/classification/property semantic_grounding() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.semantic_grounding(), exposed as Report Spec "Analytic Demo - Semantic Grounding", instantiated as the Report "Semantic Grounding Coverage Metric Report", measured by the GovernanceMetric "Semantic Grounding Coverage". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Semantic Grounding Coverage Data Flow

### Element Id
Semantic Grounding Coverage Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Semantic Grounding Coverage Data Flow

### Element Id
Semantic Grounding Coverage

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Stale Assets (No Update in 180 Days) Metric Report

### Description
Live computation backing the Stale Assets (No Update in 180 Days) governance metric.

### Report Spec
Analytic Demo - Stale Assets

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Stale Assets (No Update in 180 Days)

### Summary
Assets with no update in the last N days (default 180) -- candidates for archival review. One bounded Asset element fetch, each element's own version metadata compared against the cutoff, no relationship traversal.

### Scope
Fixed to the Asset type -- population isn't a parameter, but the staleness threshold (days) is.

### Usage
Assets with no update in the last N days (default 180) -- candidates for archival review. FIXED metric -- Fixed to the Asset type -- population isn't a parameter, but the staleness threshold (days) is. This spec always returns that one metric. Result shape: dict (staleCount, assetTotal). Default params (edit/override at run time): {'days': 180}.

### Implementation Description
pyegeria.view.overview_metrics.stale_assets() -- exposed as Report Spec "Analytic Demo - Stale Assets" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (staleCount, assetTotal).

### Measurement
dict (staleCount, assetTotal). Fixed to the Asset type -- population isn't a parameter, but the staleness threshold (days) is.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Stale Assets (No Update in 180 Days)

### Data Asset
Stale Assets (No Update in 180 Days) Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Stale Assets (No Update in 180 Days) Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Stale Assets (No Update in 180 Days)" governance metric: a data source (the Egeria relationship/classification/property stale_assets() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.stale_assets(), exposed as Report Spec "Analytic Demo - Stale Assets", instantiated as the Report "Stale Assets (No Update in 180 Days) Metric Report", measured by the GovernanceMetric "Stale Assets (No Update in 180 Days)". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Stale Assets (No Update in 180 Days) Data Flow

### Element Id
Stale Assets (No Update in 180 Days) Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Stale Assets (No Update in 180 Days) Data Flow

### Element Id
Stale Assets (No Update in 180 Days)

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Term Definition Completeness Metric Report

### Description
Live computation backing the Term Definition Completeness governance metric.

### Report Spec
Analytic Demo - Term Definition Completeness

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Term Definition Completeness

### Summary
Share of GlossaryTerms carrying a non-empty description -- a definitions-coverage metric, distinct from semantic_grounding (term<->asset linkage, not whether the term itself is actually defined).

### Scope
Fixed to GlossaryTerm's description property -- not a parameter.

### Usage
Share of GlossaryTerms carrying a non-empty description. undefinedPct is the gap (not the coverage) -- a near-100%-defined glossary is the uninteresting case, and the gap is what's actionable. FIXED metric -- Fixed to GlossaryTerm's description property -- not a parameter. This spec always returns that one metric. Result shape: dict (total, defined, undefinedPct).

### Implementation Description
pyegeria.view.overview_metrics.term_definition_completeness() -- exposed as Report Spec "Analytic Demo - Term Definition Completeness" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (total, defined, undefinedPct).

### Measurement
dict (total, defined, undefinedPct). Fixed to GlossaryTerm's description property -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Term Definition Completeness

### Data Asset
Term Definition Completeness Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Term Definition Completeness Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Term Definition Completeness" governance metric: a data source (the Egeria relationship/classification/property term_definition_completeness() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.term_definition_completeness(), exposed as Report Spec "Analytic Demo - Term Definition Completeness", instantiated as the Report "Term Definition Completeness Metric Report", measured by the GovernanceMetric "Term Definition Completeness". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Term Definition Completeness Data Flow

### Element Id
Term Definition Completeness Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Term Definition Completeness Data Flow

### Element Id
Term Definition Completeness

___

## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
Usage Context: Supply Chains & Blueprints Metric Report

### Description
Live computation backing the Usage Context: Supply Chains & Blueprints governance metric.

### Report Spec
Analytic Demo - Usage Context: Supply Chains & Blueprints

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
Usage Context: Supply Chains & Blueprints

### Summary
InformationSupplyChain and SolutionBlueprint counts -- the two structures that put assets in a business usage context (supply chain membership, blueprint realization).

### Scope
Fixed to InformationSupplyChain and SolutionBlueprint -- not a parameter.

### Usage
InformationSupplyChain and SolutionBlueprint counts -- the two structures that put assets in a business usage context (supply chain membership, blueprint realization). FIXED metric -- Fixed to InformationSupplyChain and SolutionBlueprint -- not a parameter. This spec always returns that one metric. Result shape: dict (informationSupplyChains, blueprints).

### Implementation Description
pyegeria.view.overview_metrics.usage_context_counts() -- exposed as Report Spec "Analytic Demo - Usage Context: Supply Chains & Blueprints" via pyegeria's analytic function registry (analytic_registry.py). Returns: dict (informationSupplyChains, blueprints).

### Measurement
dict (informationSupplyChains, blueprints). Fixed to InformationSupplyChain and SolutionBlueprint -- not a parameter.

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
Usage Context: Supply Chains & Blueprints

### Data Asset
Usage Context: Supply Chains & Blueprints Metric Report

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
Usage Context: Supply Chains & Blueprints Data Flow

### Purposes
Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual chain behind the "Usage Context: Supply Chains & Blueprints" governance metric: a data source (the Egeria relationship/classification/property usage_context_counts() actually reads -- see its own Implementation Description) feeds the analytic function pyegeria.view.overview_metrics.usage_context_counts(), exposed as Report Spec "Analytic Demo - Usage Context: Supply Chains & Blueprints", instantiated as the Report "Usage Context: Supply Chains & Blueprints Metric Report", measured by the GovernanceMetric "Usage Context: Supply Chains & Blueprints". Real Collection membership below covers the Report and GovernanceMetric (both real elements today); the data-source and analytic-function stages are text-only until FormatSet/the analytic function itself become real Egeria types.

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Usage Context: Supply Chains & Blueprints Data Flow

### Element Id
Usage Context: Supply Chains & Blueprints Metric Report

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
Usage Context: Supply Chains & Blueprints Data Flow

### Element Id
Usage Context: Supply Chains & Blueprints

___
