<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Coco Pharmaceuticals — Chief Data Officer Dashboard

> **Author:** Jules Keeper (Chief Data Officer)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-11-06  
> **Description:** A local dashboard that shows Jules Keeper how well the data governance program is going. Every tile is a live query against Egeria, so the dashboard changes as the domain teams, the data hub team and the data governance team add to the catalog.

---

## Overview

The final phase of Jules' ninety day plan — the Impact Phase — set three goals.  The first was to *build a metrics system to demonstrate the value the team and the data governance efforts are bringing to the business*.  This file is that metrics system, in its first form.

It is organised around the questions Jules has to answer when the board, or a fellow governance leader, asks how things are going:

| | Question | Where the answer comes from |
|---|---|---|
| 1 | Has the governance program actually been built? | Counts of the drivers, policies, roles, metrics and risks every domain team has defined, plus the strategic information supply chains |
| 2 | Are the DATA domain's own metrics moving? | The six governance metrics defined in `data-governance-program.md`, each mapped to the nearest live measure — or called out honestly as not yet measured |
| 3 | Is the common vocabulary being used? | Glossary definition completeness, and whether terms are actually attached to anything |
| 4 | Is the data hub delivering? | Digital products, catalog growth, and the strategic information supply chain register |
| 5 | Where am I against my plan, and what could go wrong? | The ninety day plan, the risk register and the full governance metric register |

The DATA domain is a *systemic* domain: it exists so that the manufacturing, privacy, drug development and corporate domains can meet obligations that are theirs (see the README's *How the governance domains fit together*).  So most of the tiles measure the shared foundation the other domains depend on, rather than anything the DATA domain owns outright.

### What this file creates

| | |
|---|---|
| 1 Dashboard Sheet | `Chief Data Officer Dashboard` — held in Egeria as a `Dashboard` asset and its layout elements (pyegeria 6.2.29+) |
| 15 Reports | Egeria `Report` assets, each a Report Spec plus the parameters that scope it |
| 15 placements | `Link Report to Dashboard Sheet`, in display order |
| 7 text placements | Section headings and captions explaining what each group of tiles means |

### Loading the dashboard

Since pyegeria 6.2.29 the Dashboard Sheet commands write the sheet into Egeria, and also keep a copy in a local file (`~/.pyegeria/dashboard_sheets.json`) on whatever machine runs `dr_egeria`.  The Portal's **Local Dashboards** app reads Egeria first and uses the local file inside the `quickstart-pyegeria-web` container only for sheets Egeria does not hold.  On the quickstart this sheet was moved into Egeria on 2026-11-10 and is owned by `erinoverview`; re-running this file updates that Egeria copy.  Either of these works:

1. From the Portal — open **Local Dashboards**, click **▶ Run Dr.Egeria Document**, paste this file, then **Validate** and **Process**.
2. From the command line:

    ```
    docker exec -w "/coco-workbooks/0. data-governance-program" quickstart-pyegeria-web \
        dr_egeria --directive process --userid juleskeeper --user_pass secret chief-data-officer-dashboard.md
    ```

Then open `/local-dashboards?sheet=Chief%20Data%20Officer%20Dashboard`.

Load it after the rest of this directory.  It reads better still after `1. coco-data-hub/`, because the digital product and supply chain tiles count what the data hub team builds.  Running **Validate** first will report each `Link Report to Dashboard Sheet` as "not found" — that is expected, because the Reports are created earlier in the same file; they resolve on **Process**.

Every command upserts, so the file is safe to re-run after changing a tile.

---

## The Dashboard Sheet

___

## Create Dashboard Sheet

### Display Name
Chief Data Officer Dashboard

### Dashboard Sheet Heading
How the Data Governance Program is Going

### Dashboard Sheet Description
Jules Keeper's view of the data governance program at Coco Pharmaceuticals: whether the program has been built, whether the DATA domain's own metrics are moving, whether the common vocabulary is in use, whether the data hub is delivering, and where things stand against the ninety day plan and the risk register.

### Dashboard Sheet Family
dashboard

___

---

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Introduction

### MD Content
**How is the data governance program going?**  Every tile below is a live query against Egeria, so this page changes as the domain teams, the data hub team and the data governance team add to the catalog.  The DATA domain exists in service of the domains that carry business and regulatory responsibility, so most tiles measure the shared foundation those domains depend on.  Where a governance metric has no live measure yet, the dashboard says so rather than leaving it out.

### Placement Span
full

### Placement Emphasis
panel

___

---

## 1. Has the governance program been built?

Jules' first act in the Initiation Phase was to convene the governance leaders and get each domain team to define its drivers, policies, roles and metrics.  These tiles count what exists, across every domain.  A count is not a quality measure, but a domain whose bar is missing has not started.

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Section 1 - Program Built

### MD Content
**1. Has the governance program been built?**  The governance definitions defined by all the governance leaders and their teams, the metrics that make them observable, and the information supply chains and blueprints that put the data in a business context.

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Create Report

### Display Name
Governance Definitions by Type

### Qualified Name
CocoPharma::Report::CDODashboard::GovernanceDefinitionsByType

### Description
The number of governance definitions of each kind across all the governance domains, from the drivers (business imperatives, regulations and threats), through the policies (principles, obligations and approaches), to the controls (roles and metrics) and the risk register.

### Report Spec
Analytic Demo - Assets by Type Breakdown

### Output Format
BAR

### Analytic Parameters
  type_map: [["Business Imperatives", "BusinessImperative"], ["Regulations", "Regulation"], ["Threats", "Threat"], ["Principles", "GovernancePrinciple"], ["Obligations", "GovernanceObligation"], ["Approaches", "GovernanceApproach"], ["Roles", "GovernanceRole"], ["Metrics", "GovernanceMetric"], ["Risks", "Risk"]]

___

---

___

## Create Report

### Display Name
Governance Metrics Defined

### Qualified Name
CocoPharma::Report::CDODashboard::GovernanceMetricsDefined

### Description
The number of governance metrics defined across all the domains.  The metrics are what make the program observable, so this is the size of the metrics system the Impact Phase set out to build.

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
  type_name: GovernanceMetric

___

---

___

## Create Report

### Display Name
Supply Chains and Blueprints

### Qualified Name
CocoPharma::Report::CDODashboard::SupplyChainsAndBlueprints

### Description
The number of information supply chains and solution blueprints in the catalog — the two structures that put data in a business context.  Identifying the key information supply chains was one of the tasks in the Initiation Phase of the ninety day plan.

### Report Spec
Analytic Demo - Usage Context: Supply Chains & Blueprints

### Output Format
DICT

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Governance Definitions by Type

### Placement Span
2

### Placement Emphasis
panel

### Placement Perspectives
governance

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Governance Metrics Defined

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance

### Placement Detail Spec
Governance-Metric-DrE-Basic

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Supply Chains and Blueprints

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance

___

---

## 2. Are the DATA domain's own metrics moving?

`data-governance-program.md` defines six governance metrics for the DATA domain.  Three have a reasonable live measure today; three depend on automated data quality monitoring that the catalog does not yet record.  The mapping is stated on the dashboard itself, so nobody mistakes a proxy for the metric it stands in for.

| Governance metric | Tile | How close |
|---|---|---|
| Percentage of Data Assets with Designated Owner | Data Asset Ownership | Direct — assets carrying an `Ownership` classification |
| Catalog Registration Coverage | Governance Classification Coverage and Catalog Freshness | Partial — measures what is registered and governed, but there is no discovery scan to compare against yet |
| Lineage Coverage for Critical Data Elements | Solution Design Context | Proxy — assets implemented by a solution component; the first hop of lineage, not end to end |
| Critical Data Element Quality Expectation Coverage | — | Not yet measured |
| Data Quality Rule Pass Rate | — | Not yet measured |
| Open Data Quality Issues by Age | — | Not yet measured |

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Section 2 - DATA Metrics

### MD Content
**2. Are the DATA domain's own metrics moving?**  The data governance program defines six metrics.  Three have a live measure below: *Percentage of Data Assets with Designated Owner* (Data Asset Ownership, a direct measure), *Catalog Registration Coverage* (Governance Classification Coverage and Catalog Freshness, a partial measure until discovery scanning runs) and *Lineage Coverage for Critical Data Elements* (Solution Design Context, a proxy: the first hop from an asset to the design it implements, not an end-to-end lineage path).

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Create Report

### Display Name
Data Asset Ownership

### Qualified Name
CocoPharma::Report::CDODashboard::DataAssetOwnership

### Description
How many catalogued assets carry an Ownership classification naming who is responsible for them, broken down by the kind of owner.  This is the live measure of the governance metric Percentage of Data Assets with Designated Owner, whose target is 100%.

### Report Spec
Analytic Demo - Ownership Coverage

### Output Format
DICT

___

---

___

## Create Report

### Display Name
Governance Classification Coverage

### Qualified Name
CocoPharma::Report::CDODashboard::GovernanceClassificationCoverage

### Description
How many catalogued assets carry at least one governance classification, with a breakdown by classification and by governance zone.  Together with Catalog Freshness, this is the partial measure of the governance metric Catalog Registration Coverage.

### Report Spec
Analytic Demo - Governance Coverage

### Output Format
DICT

___

---

___

## Create Report

### Display Name
Catalog Freshness

### Qualified Name
CocoPharma::Report::CDODashboard::CatalogFreshness

### Description
How many catalogued assets have not been updated for six months.  A catalog entry that nobody maintains decays into a record of how things used to be, so stale assets are candidates for review by their owners.

### Report Spec
Analytic Demo - Stale Assets

### Output Format
DICT

### Analytic Parameters
  days: 180

___

---

___

## Create Report

### Display Name
Solution Design Context

### Qualified Name
CocoPharma::Report::CDODashboard::SolutionDesignContext

### Description
The percentage of catalogued assets linked to the solution component they implement.  This is a proxy for the governance metric Lineage Coverage for Critical Data Elements: it shows that an asset has been placed in its designed information supply chain, which is the first step towards end-to-end lineage, but not that the full path from origin to point of use is recorded.

### Report Spec
Analytic Demo - Contextualised Coverage

### Output Format
DICT

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Data Asset Ownership

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, owner

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Governance Classification Coverage

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, steward

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Catalog Freshness

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, steward

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Solution Design Context

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, engineer

___

---

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Data Quality Not Yet Measured

### MD Content
**Not yet measured: data quality.**  Three of the DATA domain's metrics — *Critical Data Element Quality Expectation Coverage*, *Data Quality Rule Pass Rate* (target 98% or above) and *Open Data Quality Issues by Age* (target: nothing older than seven days on critical data) — need automated quality rule results and a record of the issues they raise.  The clinical trials pipeline in `2. clinical-trials` runs quality checks, but their results are not yet recorded in the catalog in a form these tiles can count.  Until they are, the honest answer to *how good is our data?* is *we cannot yet say*, and closing this gap is the next priority for Erin Overview and Peter Profile.

### Placement Span
full

### Placement Emphasis
panel

### Placement Perspectives
governance, steward

___

---

## 3. Is the common vocabulary being used?

The *common data definitions* principle only pays off if the terms are defined and then used.  Jules had planned to write a data quality definition, then adopted the manufacturing team's ALCOA++ vocabulary instead, and asked Erin to build it out into the data quality glossary.  Erin and Faith built the employee glossary the same way.  These two tiles show whether that effort is taking hold across the whole catalog.

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Section 3 - Vocabulary

### MD Content
**3. Is the common vocabulary being used?**  A glossary term is only useful once it is defined, and only does its job once it is attached to the data it describes.  The first tile shows how many terms have a definition; the second shows how many terms are actually assigned to something in the catalog.

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Create Report

### Display Name
Glossary Definition Completeness

### Qualified Name
CocoPharma::Report::CDODashboard::GlossaryDefinitionCompleteness

### Description
How many glossary terms carry a definition.  A term with a name and no definition invites every team to read its own meaning into it — the problem the data quality glossary was created to solve.

### Report Spec
Analytic Demo - Term Definition Completeness

### Output Format
DICT

___

---

___

## Create Report

### Display Name
Glossary Terms in Use

### Qualified Name
CocoPharma::Report::CDODashboard::GlossaryTermsInUse

### Description
How many glossary terms are assigned to at least one element in the catalog, and how many have been defined but never used to describe any data.

### Report Spec
Analytic Demo - Orphan Glossary Terms

### Output Format
DICT

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Glossary Definition Completeness

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, steward

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Glossary Terms in Use

### Placement Span
1

### Placement Emphasis
kpi

### Placement Perspectives
governance, steward

___

---

## 4. Is the data hub delivering?

The data strategy commits Coco Pharmaceuticals to sharing data safely between the business units, through a data hub and a mesh of digital products built along the strategic information supply chains.  These tiles show whether that is happening.

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Section 4 - Data Hub

### MD Content
**4. Is the data hub delivering?**  The digital products that deliver critical data between systems, how the catalog has grown over the last ninety days, and the register of strategic information supply chains the company governs and monitors at company level.

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Create Report

### Display Name
Digital Products Published

### Qualified Name
CocoPharma::Report::CDODashboard::DigitalProductsPublished

### Description
The number of digital products in the catalog.  Each digital product delivers critical data between systems along a strategic information supply chain, so this is the most direct measure of the data hub's output.

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
  type_name: DigitalProduct

___

---

___

## Create Report

### Display Name
Catalog Growth - Last Ninety Days

### Qualified Name
CocoPharma::Report::CDODashboard::CatalogGrowthLastNinetyDays

### Description
Catalogued assets, glossary terms, governed assets and digital products over the last ninety days, as six snapshots.  A flat line is a program that has stalled.

### Report Spec
Analytic Demo - Catalog Growth Trend

### Output Format
SERIES

### Analytic Parameters
  window: 90d
  points: 6

___

---

___

## Create Report

### Display Name
Strategic Information Supply Chain Register

### Qualified Name
CocoPharma::Report::CDODashboard::StrategicInformationSupplyChainRegister

### Description
The register of information supply chains that Coco Pharmaceuticals governs and monitors at company level, from strategic-information-supply-chains.md.

### Report Spec
Collections

### Output Format
MERMAID

### Search String
Strategic Information Supply Chains

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Digital Products Published

### Placement Span
1

### Placement Emphasis
kpi

### Placement Detail Spec
Digital-Products

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Catalog Growth - Last Ninety Days

### Placement Span
2

### Placement Emphasis
panel

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Strategic Information Supply Chain Register

### Placement Span
full

### Placement Emphasis
panel

### Placement Detail Spec
Information-Supply-Chain-DrE-Basic

___

---

## 5. The plan, the risks and the metrics

The last group is the working detail behind the numbers: where Jules stands against the ninety day plan, what the risk register says could go wrong, and the full list of governance metrics every domain has committed to.

___

## Add Text on Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Placement Name
Section 5 - Plan Risks Metrics

### MD Content
**5. The plan, the risks and the metrics.**  The ninety day plan with the status of each phase and task, the company risk register built by all the governance leaders, and the full governance metric register — the metrics system the Impact Phase set out to build, of which the tiles above are the first live measures.

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Create Report

### Display Name
My Ninety Day Plan Progress

### Qualified Name
CocoPharma::Report::CDODashboard::MyNinetyDayPlanProgress

### Description
The campaign, phases and tasks of Jules Keeper's ninety day plan, from jules-90-day-plan.md, with their current status.

### Report Spec
Project-DrE-Basic

### Output Format
LIST

### Search String
JulesKeeper::

___

---

___

## Create Report

### Display Name
Company Risk Register

### Qualified Name
CocoPharma::Report::CDODashboard::CompanyRiskRegister

### Description
The risks in the company risk register, from risk-register.md, built and owned jointly by the governance leaders.

### Report Spec
Risk-DrE-Basic

### Output Format
LIST

### Search String
CocoPharma::Risk::

___

---

___

## Create Report

### Display Name
Governance Metric Register

### Qualified Name
CocoPharma::Report::CDODashboard::GovernanceMetricRegister

### Description
Every governance metric defined by the governance domains — what the program has committed to measure.

### Report Spec
Governance-Metric-DrE-Basic

### Output Format
LIST

### Search String
CocoPharma::GovernanceMetric::

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
My Ninety Day Plan Progress

### Placement Span
full

### Placement Emphasis
panel

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Company Risk Register

### Placement Span
full

### Placement Emphasis
panel

### Placement Perspectives
governance

___

---

___

## Link Report to Dashboard Sheet

### Dashboard Sheet Name
Chief Data Officer Dashboard

### Report Name
Governance Metric Register

### Placement Span
full

### Placement Emphasis
panel

### Placement Perspectives
governance

___

---

## Where next

This is a first version of the metrics system, and its gaps are part of its message:

* **Data quality** — the three quality metrics need quality rule results recorded in the catalog.  When they are, replace the *Data Quality Not Yet Measured* text placement with Reports.
* **Lineage** — *Solution Design Context* measures only the first hop.  A live end-to-end lineage measure for critical data elements needs the critical data element register that `data-governance-program.md` calls for.
* **Per-domain reporting** — several of the DATA metrics must be reported per declaring domain.  The counts above are company-wide, because `domainIdentifier` is not yet a dimension the analytic functions group by.
* **Trends** — the growth chart shows the catalog as a whole.  The same technique (`Analytic Demo - Metric Trend`) can trend any single tile, such as ownership coverage, once there is enough history to make it meaningful.
