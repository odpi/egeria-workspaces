# Coco Pharmaceuticals — Sustainability Governance Program

> **Author:** Tom Tally (Sustainability Lead)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Connects the sustainability governance definitions created in `sustainability-governance-definitions.md` to the domain programs built since, so that the sustainability imperative sits within the wider governance framework rather than alongside it. Load after the whole of the `0. data-governance-program` directory.

---

## Overview

The sustainability definitions were created early, when the governance program consisted of the joint officer definitions and little else. They link the Sustainability Reporting imperative to the two policies available at the time — information as a company asset, and designated ownership of information collections — and that was the right connection to make then.

Since then the domain programs have been built out, and several of them contain policies that sustainability reporting depends on far more directly. This file makes those connections. It creates no new definitions: the imperative, the Sustainability Lead role, and the folio already exist, and duplicating them here would produce two of each.

The connections it adds fall into three groups. **Reporting integrity** — sustainability figures are externally reported and increasingly assured, which makes them subject to the same reconciliation discipline as financial figures rather than a softer standard. **Data foundations** — emissions, energy and waste data originates in operational systems that were never built to produce reportable figures, so the quality expectations, lineage, and catalog work in the data program is what turns operational readings into something disclosable. **Manufacturing origin** — most of the company's emissions arise in manufacturing and distribution, which means the data comes from Stew Faster's domain and inherits the integrity controls applied there.

Two things this file deliberately does not do. It does not create a sustainability domain identifier: the imperative carries `CORPORATE`, which is correct while sustainability reporting is a corporate disclosure obligation rather than a domain with its own regulator. And it does not add a sustainability regulation to the Corporate Regulation Library — the EU Corporate Sustainability Reporting Directive would be the obvious candidate, and it is noted at the end of this file as the natural next step rather than assumed.

---

## Part 1: Governance Responses — Sustainability Reporting

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Rationale
Sustainability figures are published and increasingly subject to external assurance, which places them under the same requirement as financial figures: every reported number must trace to controlled source data through documented transformations, with manual assembly steps identified and reduced.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Rationale
Emissions, energy and waste figures originate in meters, logistics records and supplier declarations that were never designed to produce reportable data. Stating the quality expectation for each critical element is what makes the gap between operational reading and disclosable figure explicit rather than absorbed in a spreadsheet.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Rationale
An assurance provider asking how a reported emissions figure was derived is asking a lineage question. Capturing lineage for the elements underlying the disclosure is what allows the answer to be produced from the catalog rather than reconstructed by the people who built the model.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Rationale
Sustainability reporting draws on data held across manufacturing, facilities, logistics and procurement, much of it in systems the sustainability team does not operate. Registration with recorded ownership is how those holdings become findable and their owners identifiable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Rationale
Emissions are reported by site, by product and by supplier, and each of those is master data. Where site or supplier records diverge between systems, the same emission is counted twice or not at all, and the discrepancy surfaces only when the totals fail to reconcile.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::SustainabilityReporting

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
Most of the company's emissions arise in manufacturing, so most sustainability data originates under the ALCOA+ regime already applied to manufacturing records. Sustainability reporting inherits that integrity standard rather than defining a weaker one for the same underlying measurements.

___

---

## Part 2: Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::SustainabilityReporting

### Governance Driver 2
CocoPharma::BusinessImperative::FinancialReportingIntegrity

### Description
Both are external reporting obligations resting on internal data whose last mile is assembled outside controlled systems, and both fail the same way — through manual consolidation nobody has brought under change control. Sustainability reporting is currently where financial reporting was before Section 404, and the controls that answered the financial problem are the ones that will answer this one.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::SustainabilityReporting

### Governance Driver 2
CocoPharma::Threat::FragmentedDataDefinitions

### Description
Sustainability reporting is unusually exposed to definitional fragmentation because it aggregates across every part of the business at once. A site boundary, a production unit, or a supplier defined differently in three systems produces a total that cannot be reconciled and cannot be explained to an assurance provider.

___

---

## Part 3: Folio Membership

The Sustainability Lead folio and its root collection membership are created in `sustainability-governance-definitions.md`. This file adds no new definitions, so it adds no new folio members.

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| [sustainability-governance-definitions.md](sustainability-governance-definitions.md) | Creates the Sustainability Reporting imperative, the Sustainability Lead role, and the folio this file connects |
| `0. data-governance-program/data-governance-program.md` | DATA-domain program supplying the quality, lineage, catalog and master data policies referenced here |
| `0. data-governance-program/corporate-governance-program.md` | CORPORATE-domain program supplying the reporting reconciliation principle and the financial reporting imperative |
| `0. data-governance-program/manufacturing-governance-program.md` | MANUFACTURING-domain program, where most emissions data originates under the ALCOA+ regime |

---

## Appendix: Not Yet Done

The **EU Corporate Sustainability Reporting Directive** is not defined as a regulation here. It would be the natural driver for this domain, converting sustainability reporting from a voluntary disclosure into a regulated one with assurance requirements and a defined reporting standard — at which point the imperative's `CORPORATE` domain identifier and the absence of any sustainability obligations or metrics would both need revisiting. Adding it would also need a library folder: it fits none of Financial, Employment, Health and Safety, Product and Service, Pharmaceutical Industry, Clinical Trial, Privacy, or Security.
