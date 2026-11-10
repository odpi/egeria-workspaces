<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Overview — Governance Metrics

> Loadable **Dr.Egeria** document that materialises the Overview dashboard's
> fixed (non-generic) `pyegeria.view.overview_metrics` functions as real
> `GovernanceMetric` elements, each linked via `GovernanceResults` to a real
> `Report` (report-spec-backed, runnable via `/api/report-specs/execute`).
> (Until 2026-11-09 it also wrote a per-metric "<metric> Data Flow"
> `InformationSupplyChain`; the owner judged them noise and they were removed.)
> Generated from
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
Distinct usernames behind at least one feedback relationship (ratings/comments/likes/tags/noteLogs) -- an engagement signal feedback_summary's raw relationship counts don't give you (one prolific commenter vs. many occasional ones). Cost: five relationship scans, paged until Egeria returns an empty page, seconds.

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
The true 'AI-Ready' composite: Asset elements that are governed AND documented AND lineage-traced simultaneously, not three independent counts intersected after the fact. First real implementation of the composite/derived analytic metric pattern -- see NEXT-18 (egeria-workspaces BACKLOG.md) for why this pattern didn't exist here before. Takes two leading clients (mgr, ce), same convention as semantic_grounding/context_readiness_funnel. Cost: one Asset find page (a full page is a sample, so not measured) plus every DataFlow relationship page, seconds.

### Scope
Fixed to governed+documented+lineage-traced over Asset elements -- not a parameter.

### Usage
The actual per-asset intersection context_readiness_funnel's 'aiReady' field can't give you: Asset elements that are governed AND documented AND lineage-traced, all three, checked per element from one Asset find page plus every DataFlow relationship (not three separate counts intersected client-side after the fact -- see the function's own docstring for the exact field-name gotchas this hit while being built, e.g. find_metadata_elements results key their GUID as 'elementGUID' but a relationship end's GUID is plain 'guid'). 'total' is the Asset population checked. A full Asset page is a sample, not the catalog, so then nothing is measured (capped=true, with a note); otherwise divide aiReadyCount by total for a percentage. First worked example of the composite/derived analytic metric pattern NEXT-18 (egeria-workspaces BACKLOG.md) flagged as missing. FIXED metric -- Fixed to governed+documented+lineage-traced over Asset elements -- not a parameter. This spec always returns that one metric. Result shape: dict (aiReadyCount, total, capped).

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
Real signals behind the four Overview dashboard Business Value tiles (Risk & Compliance, Productivity, Trust & Adoption, Cost Avoidance): Confidentiality-classified asset count, described-asset count, ConsolidatedDuplicate-flagged element count -- all proxies with a documented causal-claim caveat, not direct measures (NEXT-9). Cost: four native counts, sub-second each in the repository population. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed to the Asset type hierarchy and Confidentiality/ConsolidatedDuplicate classifications -- not a parameter.

### Usage
Real signals behind the Overview dashboard's four Business Value tiles (NEXT-9): assetTotal, confidentialCount (Assets classified Confidentiality), describedCount (Assets whose description is set and not empty) and duplicateCount (ConsolidatedDuplicate elements) are native counts over the whole repository, including elements the viewer may not be able to see. Each is a documented proxy, not a direct measure -- see business_value_signals()'s docstring for the causal-claim caveat that belongs with each field before treating it as more than that. FIXED metric -- Fixed to the Asset type hierarchy and Confidentiality/ConsolidatedDuplicate classifications -- not a parameter. This spec always returns that one metric. Result shape: dict (assetTotal, assetCapped, confidentialCount, describedCount, duplicateCount).

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
Active/expiring Certification relationships, licenses, and open Exception counts. Cost: one relationship scan, paged until Egeria returns an empty page, plus two counts, seconds.

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
Cataloged -> Documented -> Classified -> Lineage-traced -> AI-Ready funnel counts. Takes two leading clients (mgr, ce) -- the executor supplies the same EgeriaTech instance for both, matching semantic_grounding's convention. This function's own aiReady stays None always by design -- it's four independent counts, and aiReady needs a true cross-criteria intersection instead. Pair with ai_ready_assets (below) for that -- overview_handler.py calls both and merges the result. Every stage is a native count in the repository population. Cost: four native counts, sub-second each. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed 5-stage readiness definition baked into the function body -- not a parameter.

### Usage
'cataloged' (Asset supertype count), 'documented' (Assets whose description is set and not empty), 'classified' (elements matching ANY of the same governance classifications governed_coverage uses), and 'lineage' (count of DataFlow relationships -- design/ business lineage, distinct from OpenLineage's operational lineage) are all native counts over the whole repository (including elements the viewer may not be able to see), computed as of 2026-08-01. 'aiReady' stays None from this function ALWAYS, by design -- these four are independent counts, not a per-asset check, so they can't answer 'how many assets are ALL of these at once'. See 'Analytic Demo - AI-Ready Assets' (below) for that -- a genuinely different function, not a missing field on this one. FIXED metric -- Fixed 5-stage readiness definition baked into the function body -- not a parameter. This spec always returns that one metric. Result shape: dict (cataloged, documented, classified, lineage, aiReady).

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
Percent of Assets given business/solution-design context via an ImplementedBy relationship to a SolutionComponent. A proxy, not the literal 'participates in an ISC/blueprint' metric -- confirms some solution-design context exists, not that the specific SolutionComponent is itself wired into an ISC/blueprint (a second hop this function doesn't take). Takes two leading clients (mgr, ce), same convention as semantic_grounding. Cost: one relationship scan, paged until Egeria returns an empty page, plus one count, seconds.

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
Weekly-bucketed feedback-event trend (comments/ratings/likes/tags/noteLogs), zero-filled across the trailing window -- reuses the same 5 relationship-type queries feedback_summary() already makes, keeping createTime instead of only the count. Takes ce as its leading client. Cost: five relationship scans, paged until Egeria returns an empty page, seconds.

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
Crowd-sourced feedback counts (ratings/comments/likes/tags/noteLogs) by type, via Collaboration OMAS relationships. Takes an EgeriaTech: the repository count is MetadataExpert's native relationship count, and the viewer path is ClassificationExplorer's get_relationships. Cost: five native counts, sub-second each in the repository population; population=viewer reads five relationship scans instead, paged until Egeria returns an empty page. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

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
Share of assets carrying at least one governance classification, plus a by-classification / top-zones breakdown. Cost: one find, paged until Egeria returns an empty page (an incomplete scan is not measured), seconds.

### Scope
Fixed to GOVERNANCE_CLASSIFICATIONS: ZoneMembership, Confidentiality, Criticality, Impact, Retention -- not a parameter.

### Usage
Count of elements carrying at least one governance classification (ZoneMembership/Confidentiality/Criticality/Impact/Retention) -- NOT a percentage despite 'coverage' in the name (there's no cheap total-elements denominator to divide by yet). The find is paged until Egeria returns an empty page, so governedCount is every governed element (governedCapped is false when measured). byClassification and topZones are nested breakdowns of the same governedCount elements -- pick BAR below for a chart of byClassification. FIXED metric -- Fixed to GOVERNANCE_CLASSIFICATIONS: ZoneMembership, Confidentiality, Criticality, Impact, Retention -- not a parameter. This spec always returns that one metric. Result shape: dict (governedCount, governedCapped, byClassification, topZones).

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
Top-N people by karma -- every ContributionRecord, karmaPoints is a scalar property on the record itself (not derived from counting related things), filtered to the given anchor type(s) via each record's own Anchors classification. Cost: one find, paged until Egeria returns an empty page, seconds.

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
Approved-but-unassigned glossary terms -- a term with no SemanticAssignment relationship to anything was authored but never put to use grounding the catalog. Every SemanticAssignment relationship, paged until Egeria returns an empty page; the distinct GlossaryTerm-end GUID count is the 'referenced' set (Egeria cannot count distinct relationship ends natively); orphan = term total - referenced. Takes two leading clients (mgr, ce), same convention as semantic_grounding. Cost: one viewer count, run at the same time as one relationship scan, seconds.

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
Share of assets carrying an Ownership classification (a named owner responsible for management/governance decisions), plus a by-owner-type breakdown. Distinct from governed_coverage -- data mesh literature names 'clean, owned, product-based data' as its own foundation for trustworthy AI consumption, not a synonym for governance-classification coverage. Cost: one find, paged until Egeria returns an empty page (an incomplete scan is not measured), seconds.

### Scope
Fixed to the Ownership classification -- not a parameter.

### Usage
Count of elements carrying an Ownership classification -- NOT a percentage, same caveat as Governance Coverage (no cheap total-elements denominator yet). The find is paged until Egeria returns an empty page, so ownershipCount is every owned element (ownershipCapped is false when measured; an incomplete scan is not measured). byOwnerType is a nested breakdown of the same ownershipCount elements by the owner's type (Person, Team, SolutionActorRole, ...) -- pick BAR below for a chart of byOwnerType. FIXED metric -- Fixed to the Ownership classification -- not a parameter. This spec always returns that one metric. Result shape: dict (ownershipCount, ownershipCapped, byOwnerType).

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
Counts of Person / Team / Organization / ITProfile / Community actor profiles. Cost: five native counts, sub-second each in the repository population. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed to Person/Team/Organization/ITProfile/Community -- not a parameter.

### Usage
Counts of Person/Team/Organization/ITProfile/Community actor profiles. FIXED metric -- Fixed to Person/Team/Organization/ITProfile/Community -- not a parameter. This spec always returns that one metric. Result shape: dict (persons, teams, organizations, itProfiles, communities). Default params (edit/override at run time): {'strict': True}.

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
SemanticAssignment relationship count and coverage percent -- the meaning layer that grounds AI. Takes two leading clients (mgr, ce) -- the executor supplies the same EgeriaTech instance for both. Both counts are native, in the repository population, so the percentage never divides one population by the other. Cost: two native counts, sub-second each. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed to the SemanticAssignment relationship type -- not a parameter.

### Usage
groundingLinks = count of SemanticAssignment relationships (term<->asset). groundingPct = that count as a percent of the broad Asset supertype count; both are native counts over the whole repository, including elements the viewer may not see (i.e. 'percent of Assets' as the denominator, capped at 100 -- an asset with multiple assignments can push the raw ratio over 100%, which is why it's capped, not because grounding coverage is literally bounded there). A per-asset detail breakdown (which assets are/aren't grounded) isn't available from this metric --  a real gap for later. FIXED metric -- Fixed to the SemanticAssignment relationship type -- not a parameter. This spec always returns that one metric. Result shape: dict (groundingLinks, groundingPct).

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
Assets with no update in the last N days (default 180) -- candidates for archival review. Egeria cannot count by update time, but it sorts by it, so the stale count is a bisection over the Assets' offsets in update-time order, using one-row reads, never a page of Assets. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists). Cost: one native count plus about log2(Assets / 25) one-row reads and one 25-row read (12 for 37,000 Assets), seconds.

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
Share of GlossaryTerms whose description is set and not empty -- a definitions-coverage metric, distinct from semantic_grounding (term<->asset linkage, not whether the term itself is actually defined). Both numbers are native counts in the repository population, so the share never mixes populations; a whitespace-only description counts as defined. Cost: two native counts, sub-second each. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed to GlossaryTerm's description property -- not a parameter.

### Usage
Share of GlossaryTerms whose description is set and not empty; total and defined are native counts over the whole repository (including terms the viewer may not be able to see). undefinedPct is the gap (not the coverage) -- a near-100%-defined glossary is the uninteresting case, and the gap is what's actionable. FIXED metric -- Fixed to GlossaryTerm's description property -- not a parameter. This spec always returns that one metric. Result shape: dict (total, defined, undefinedPct).

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
InformationSupplyChain and SolutionBlueprint counts -- the two structures that put assets in a business usage context (supply chain membership, blueprint realization). Cost: two native counts, sub-second each in the repository population. Its totals count the whole repository (population=repository), including elements you may not be able to see (a deliberate interim choice until zone-aware push-down exists).

### Scope
Fixed to InformationSupplyChain and SolutionBlueprint -- not a parameter.

### Usage
InformationSupplyChain and SolutionBlueprint counts -- the two structures that put assets in a business usage context (supply chain membership, blueprint realization). FIXED metric -- Fixed to InformationSupplyChain and SolutionBlueprint -- not a parameter. This spec always returns that one metric. Result shape: dict (informationSupplyChains, blueprints). Default params (edit/override at run time): {'strict': True}.

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

