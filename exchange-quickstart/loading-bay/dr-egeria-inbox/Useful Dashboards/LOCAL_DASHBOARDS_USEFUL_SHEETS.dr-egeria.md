<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Useful Dashboard Sheets: seeds

> Loadable **Dr.Egeria** document (a seed, not a tutorial). It creates four public Dashboard Sheets for the
> quickstart, each built from pyegeria's built-in analytic report specs:
>
> | Sheet | Family | Tiles |
> |---|---|---|
> | `catalog-health` | Overview | AI context readiness, ownership, stale assets, asset composition |
> | `glossary-and-meaning` | Glossary | term total, definition completeness, terms in use, active and draft terms, semantic grounding |
> | `governance-and-compliance` | Governance | governance coverage, certifications and exceptions, usage context, solution design context |
> | `community-and-feedback` | Community | feedback, engagement over twelve weeks, active contributors, karma leaderboard, people |
>
> Rules this file keeps (brief BRIEF-USEFUL-SHEETS-AND-SAVED-QUERY-REPORTS-2026-11-10):
> - **No GUIDs** in any parameter, **no zones** on any element, **no trend over past counts** (`metric_trend`,
>   `growth_series`) until pyegeria 6.2.34. `engagement_series` is kept: it buckets each feedback
>   relationship by its create time and reads every page, so it is not a past-count trend.
> - Every Report name starts with its sheet's heading, so this file never updates a Report another sheet uses.
> - Every value seen when the tiles were checked is recorded in the PR, not here (the data changes).
>
> **This is a shared Egeria write.** Run `--validate` first; run `--process` once, under the shared-write peer
> check. It is also the *Useful Dashboards* data-initialization batch (`_batch.json` in this folder), whose
> canary is the Catalog Health sheet's Dashboard element.
>
> **Undo:** for each sheet, `python -m pyegeria.view.dashboards delete --sheet <name> --dry-run`, then without
> `--dry-run` (removes the sheet's chain only). The Reports stay; delete them only if asked.

___
# Catalog Health

## Create Report
### Display Name
Catalog Health - AI Context Readiness

### Description
Assets at each step from cataloged to AI-ready.

### Report Spec
Analytic Demo - AI Context Readiness

### Output Format
DICT

___
## Create Report
### Display Name
Catalog Health - Asset Ownership

### Description
Assets with an owner, by the kind of owner.

### Report Spec
Analytic Demo - Ownership Coverage

### Output Format
BAR

___
## Create Report
### Display Name
Catalog Health - Stale Assets

### Description
Assets that have not changed in 180 days, out of all assets.

### Report Spec
Analytic Demo - Stale Assets

### Output Format
DICT

### Analytic Parameters
days: 180

___
## Create Report
### Display Name
Catalog Health - Asset Composition

### Description
How many assets of each main kind the catalog holds.

### Report Spec
Analytic Demo - Assets by Type Breakdown

### Output Format
PIE

### Analytic Parameters
type_map: [["Data Stores", "DataStore"], ["Data Sets", "DataSet"], ["Software Components", "DeployedSoftwareComponent"], ["Infrastructure", "ITInfrastructure"], ["APIs", "DeployedAPI"], ["Processes", "Process"]]

___
## Create Dashboard Sheet
### Display Name
catalog-health

### Dashboard Sheet Heading
Catalog Health

### Dashboard Sheet Description
How complete and how current the catalog is: readiness for AI use, ownership, staleness and what the assets are.

### Dashboard Sheet Family
Overview

___
## Add Text on Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Placement Name
What these tiles measure

### MD Content
#### What these tiles measure
The readiness funnel counts assets at each step from cataloged to AI-ready. Ownership counts assets with an owner, by the kind of owner. Stale assets have not changed in 180 days. The composition chart shows the asset types the catalog holds.

### Placement Span
full

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Report Name
Catalog Health - AI Context Readiness

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Report Name
Catalog Health - Asset Ownership

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Report Name
Catalog Health - Stale Assets

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Report Name
Catalog Health - Asset Composition

### Placement Span
2

### Placement Emphasis
panel

___
# Glossary & Meaning

## Create Report
### Display Name
Glossary & Meaning - Term Total

### Description
All glossary terms.

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm

___
## Create Report
### Display Name
Glossary & Meaning - Definition Completeness

### Description
Terms with a description, out of all terms.

### Report Spec
Analytic Demo - Term Definition Completeness

### Output Format
DICT

___
## Create Report
### Display Name
Glossary & Meaning - Terms in Use

### Description
Terms that something refers to, and the orphans.

### Report Spec
Analytic Demo - Orphan Glossary Terms

### Output Format
DICT

___
## Create Report
### Display Name
Glossary & Meaning - Active Terms

### Description
Terms whose content status is ACTIVE.

### Report Spec
Analytic Demo - Count by Property

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm
property_name: contentStatus
property_value: ACTIVE

___
## Create Report
### Display Name
Glossary & Meaning - Draft Terms

### Description
Terms whose content status is DRAFT.

### Report Spec
Analytic Demo - Count by Property

### Output Format
DICT

### Analytic Parameters
type_name: GlossaryTerm
property_name: contentStatus
property_value: DRAFT

___
## Create Report
### Display Name
Glossary & Meaning - Semantic Grounding

### Description
Assets linked to a glossary term.

### Report Spec
Analytic Demo - Semantic Grounding

### Output Format
DICT

___
## Create Dashboard Sheet
### Display Name
glossary-and-meaning

### Dashboard Sheet Heading
Glossary & Meaning

### Dashboard Sheet Description
How well the glossary is defined and used.

### Dashboard Sheet Family
Glossary

___
## Add Text on Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Placement Name
What these tiles measure

### MD Content
#### What these tiles measure
Definition completeness is the share of terms with a description. Terms in use counts terms that something refers to; the rest are orphans. Active and draft count terms by content status. Semantic grounding counts assets linked to a term.

### Placement Span
full

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Term Total

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Definition Completeness

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Terms in Use

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Active Terms

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Draft Terms

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Report Name
Glossary & Meaning - Semantic Grounding

### Placement Span
2

### Placement Emphasis
kpi

___
# Governance & Compliance

## Create Report
### Display Name
Governance & Compliance - Governance Coverage

### Description
Elements with a governance classification or zone, by classification.

### Report Spec
Analytic Demo - Governance Coverage

### Output Format
BAR

___
## Create Report
### Display Name
Governance & Compliance - Certifications and Exceptions

### Description
Active and expiring certifications, licenses and exceptions.

### Report Spec
Analytic Demo - Certifications and Exceptions

### Output Format
BAR

___
## Create Report
### Display Name
Governance & Compliance - Usage Context

### Description
Information supply chains and solution blueprints.

### Report Spec
Analytic Demo - Usage Context: Supply Chains & Blueprints

### Output Format
DICT

___
## Create Report
### Display Name
Governance & Compliance - Solution Design Context

### Description
Assets placed in a solution design.

### Report Spec
Analytic Demo - Contextualised Coverage

### Output Format
DICT

___
## Create Dashboard Sheet
### Display Name
governance-and-compliance

### Dashboard Sheet Heading
Governance & Compliance

### Dashboard Sheet Description
How much of the catalog is under governance, and what is certified or excepted.

### Dashboard Sheet Family
Governance

___
## Add Text on Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Placement Name
What these tiles measure

### MD Content
#### What these tiles measure
Governance coverage counts elements that carry a governance classification or zone. Certifications counts active and expiring certifications, licenses and exceptions. Usage context counts information supply chains and blueprints; solution design context counts assets placed in a solution design.

### Placement Span
full

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Report Name
Governance & Compliance - Governance Coverage

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Report Name
Governance & Compliance - Certifications and Exceptions

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Report Name
Governance & Compliance - Usage Context

### Placement Span
1

### Placement Emphasis
kpi

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Report Name
Governance & Compliance - Solution Design Context

### Placement Span
1

### Placement Emphasis
kpi

___
# Community & Feedback

## Create Report
### Display Name
Community & Feedback - Feedback Summary

### Description
Comments, ratings, likes, tags and note logs.

### Report Spec
Analytic Demo - Feedback Summary

### Output Format
BAR

___
## Create Report
### Display Name
Community & Feedback - Engagement

### Description
Feedback events by the week they were made, last twelve weeks.

### Report Spec
Analytic Demo - Engagement Over Time

### Output Format
SERIES

### Analytic Parameters
weeks: 12

___
## Create Report
### Display Name
Community & Feedback - Active Contributors

### Description
People who have contributed, by contribution type.

### Report Spec
Analytic Demo - Active Contributors

### Output Format
BAR

___
## Create Report
### Display Name
Community & Feedback - Karma Leaderboard

### Description
The ten people with the most karma points.

### Report Spec
Analytic Demo - Karma Leaderboard

### Output Format
DICT

### Analytic Parameters
top_n: 10

___
## Create Report
### Display Name
Community & Feedback - People

### Description
People, teams, organizations, IT profiles and communities.

### Report Spec
Analytic Demo - People and Community

### Output Format
DICT

___
## Create Dashboard Sheet
### Display Name
community-and-feedback

### Dashboard Sheet Heading
Community & Feedback

### Dashboard Sheet Description
Who is contributing, and how people are reacting to the catalog.

### Dashboard Sheet Family
Community

___
## Add Text on Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Placement Name
What these tiles measure

### MD Content
#### What these tiles measure
Feedback counts comments, ratings, likes, tags and note logs. Engagement shows the same events by the week they were made, over the last twelve weeks. Contributors and the karma leaderboard show who is adding to the catalog.

### Placement Span
full

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Report Name
Community & Feedback - Feedback Summary

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Report Name
Community & Feedback - Engagement

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Report Name
Community & Feedback - Active Contributors

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Report Name
Community & Feedback - Karma Leaderboard

### Placement Span
2

### Placement Emphasis
panel

___
## Link Report to Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Report Name
Community & Feedback - People

### Placement Span
2

### Placement Emphasis
kpi

___
