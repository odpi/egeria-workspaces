# Promised Components and Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-02
> **Description:** Classifies as a Promise every solution component of the strategic information supply chains that no system implements, and every digital product that consequently has no source of data.

---

# Overview

The [component-system mapping](../mapping-the-systems/README.md) linked each solution component of the strategic
information supply chains to the systems that implement it, across all three estates - Coco Pharmaceuticals'
own systems, Austin and Bucharest.  35 of the 81 components in the chains were left with no system at all.  This
file records them for what they are: **promises**.  A promise is a placeholder for something the organisation has
committed to but has not yet delivered.  It keeps its place in the supply chain designs and in their lineage, but it
does not pretend to be a running capability.

Each promise is classified with a deployment status of `PROPOSED` and a journal entry saying why.  Egeria returns a
promised element only to requests made for lineage, so the promises disappear from catalog searches and
reports but remain in the supply chain and product lineage graphs.  When a system is chosen, link it to the
component with `ImplementedBy`, then remove the classification with `Declassify Promise` from the component and its
products.

## Components

30 components are promises:

| Component | Supply chains |
|---|---|
| Case and Pallet Aggregation Recorder | Product Serialisation and Verification |
| Certify Hospital | Workforce Competency and Qualification |
| Controls Evidence Repository | Financial Close and External Reporting |
| Data Subject Identity Verification | Data Subject Rights |
| Disclosure and Statutory Reporting | Financial Close and External Reporting |
| Exposure Monitoring Capture | Occupational Health Surveillance |
| Group Consolidation Engine | Financial Close and External Reporting |
| Health Surveillance Records | Occupational Health Surveillance |
| Incident and Near Miss Reporting | Occupational Health Surveillance |
| Long Term Health Record Archive | Occupational Health Surveillance |
| Market Verification Gateway | Product Serialisation and Verification |
| Medical Assessment and Coding | Adverse Event and Safety Reporting |
| Patient Identity Register | Data Subject Rights, Personalized Treatment Ordering |
| Patient Sample Logistics | Cold Chain and Dangerous Goods Consignment, Personalized Treatment Ordering |
| Pharmacovigilance Case Management | Adverse Event and Safety Reporting |
| Procurement Systems | Third Party Onboarding and Payment |
| Qualification Currency Checker | Workforce Competency and Qualification |
| Record of Processing Activities Register | Data Subject Rights |
| Research Systems | New Drug Product Details |
| Retention Schedule Service | Data Subject Rights |
| Rights Fulfilment Orchestrator | Data Subject Rights |
| Rights Request Intake | Data Subject Rights |
| Safety Signal Detection | Adverse Event and Safety Reporting |
| Serial Number Generator | Product Serialisation and Verification |
| Serialisation Alert Triage | Product Serialisation and Verification |
| Serialisation Repository | Product Serialisation and Verification |
| Set Retention Period | Data Subject Rights |
| Temperature Excursion Assessment | Cold Chain and Dangerous Goods Consignment |
| Transaction Monitoring | Employee Expense Payment, Third Party Onboarding and Payment |
| Transfers of Value Register | Employee Expense Payment, Third Party Onboarding and Payment |

Five of the 35 unimplemented components are deliberately **not** promises:

* **Hospital Processes**, **Carrier Systems**, **National Verification Systems** and **Sanctions and Screening
  Service** are other organisations' systems.  Coco Pharmaceuticals will never implement them, so there is nothing for
  it to promise.
* **Egeria Open Metadata and Governance** is already running: it is the metadata platform these definitions live in,
  and [egeria-implementation.md](../mapping-the-systems/egeria-implementation.md) links it to the OMAG Server Platform.

## Digital products

A digital product built from the data entering a promised component has no system to feed its data set, so it is a
promise too.  So is *Third Party Screening Results*: its data comes from the external sanctions screening service,
and no Coco Pharmaceuticals system receives it yet.  32 products are promises:

| Product | Component |
|---|---|
| Consolidated Group Results | Group Consolidation Engine |
| Data Subject Rights Requests | Rights Request Intake |
| Exposure Monitoring Results | Exposure Monitoring Capture |
| External Financial Disclosures | Disclosure and Statutory Reporting |
| Financial Controls Evidence | Controls Evidence Repository |
| Health Surveillance Records | Health Surveillance Records |
| Hospital Certifications | Certify Hospital |
| Incidents And Near Misses | Incident and Near Miss Reporting |
| Long Term Health Archive | Long Term Health Record Archive |
| Market Identifier Submissions | Market Verification Gateway |
| Market Verification Responses | Market Verification Gateway |
| Medical Assessments | Medical Assessment and Coding |
| New Product Definitions | Research Systems |
| Pack Aggregation Hierarchy | Case and Pallet Aggregation Recorder |
| Patient Pseudonym Register | Patient Identity Register |
| Patient Sample Consignments | Patient Sample Logistics |
| Payment Anomaly Findings | Transaction Monitoring |
| Pharmacovigilance Cases | Pharmacovigilance Case Management |
| Purchase Orders And Receipts | Procurement Systems |
| Qualification Expiry Warnings | Qualification Currency Checker |
| Record Of Processing Activities | Record of Processing Activities Register |
| Requester Identity Verifications | Data Subject Identity Verification |
| Retention Obligations | Retention Schedule Service |
| Retention Period Assignments | Set Retention Period |
| Rights Fulfilment Actions | Rights Fulfilment Orchestrator |
| Safety Signals | Safety Signal Detection |
| Serial Number Allocations | Serial Number Generator |
| Serialisation Alert Investigations | Serialisation Alert Triage |
| Serialised Product Identifiers | Serialisation Repository |
| Temperature Excursion Assessments | Temperature Excursion Assessment |
| Third Party Screening Results | Sanctions and Screening Service |
| Transfers Of Value | Transfers of Value Register |

*Open Metadata Catalogue Holdings* is not a promise, because Egeria, its source, is already running.

This file loads after `product-dependencies.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret promises.md
```

---

# Promised components

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::AggregationRecorder

### Deployment Status
PROPOSED

### Journal Entry
No system implements Case and Pallet Aggregation Recorder in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Product Serialisation and Verification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
SolutionComponent::Certify Hospital::V1.0

### Deployment Status
PROPOSED

### Journal Entry
No system implements Certify Hospital in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Workforce Competency and Qualification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::ControlsEvidenceRepository

### Deployment Status
PROPOSED

### Journal Entry
No system implements Controls Evidence Repository in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Financial Close and External Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::IdentityVerification

### Deployment Status
PROPOSED

### Journal Entry
No system implements Data Subject Identity Verification in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::DisclosureReporting

### Deployment Status
PROPOSED

### Journal Entry
No system implements Disclosure and Statutory Reporting in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Financial Close and External Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::ExposureMonitoringCapture

### Deployment Status
PROPOSED

### Journal Entry
No system implements Exposure Monitoring Capture in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Occupational Health Surveillance supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::GroupConsolidation

### Deployment Status
PROPOSED

### Journal Entry
No system implements Group Consolidation Engine in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Financial Close and External Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Deployment Status
PROPOSED

### Journal Entry
No system implements Health Surveillance Records in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Occupational Health Surveillance supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::IncidentAndNearMissReporting

### Deployment Status
PROPOSED

### Journal Entry
No system implements Incident and Near Miss Reporting in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Occupational Health Surveillance supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::LongTermHealthArchive

### Deployment Status
PROPOSED

### Journal Entry
No system implements Long Term Health Record Archive in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Occupational Health Surveillance supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::MarketVerificationGateway

### Deployment Status
PROPOSED

### Journal Entry
No system implements Market Verification Gateway in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Product Serialisation and Verification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::MedicalAssessmentAndCoding

### Deployment Status
PROPOSED

### Journal Entry
No system implements Medical Assessment and Coding in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Adverse Event and Safety Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::PatientIdentityRegister

### Deployment Status
PROPOSED

### Journal Entry
No system implements Patient Identity Register in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights and Personalized Treatment Ordering supply chains, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::SampleLogistics

### Deployment Status
PROPOSED

### Journal Entry
No system implements Patient Sample Logistics in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Cold Chain and Dangerous Goods Consignment and Personalized Treatment Ordering supply chains, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Deployment Status
PROPOSED

### Journal Entry
No system implements Pharmacovigilance Case Management in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Adverse Event and Safety Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::Procurement

### Deployment Status
PROPOSED

### Journal Entry
No system implements Procurement Systems in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Third Party Onboarding and Payment supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::QualificationCurrencyChecker

### Deployment Status
PROPOSED

### Journal Entry
No system implements Qualification Currency Checker in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Workforce Competency and Qualification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::RecordOfProcessingRegister

### Deployment Status
PROPOSED

### Journal Entry
No system implements Record of Processing Activities Register in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::Research

### Deployment Status
PROPOSED

### Journal Entry
No system implements Research Systems in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the New Drug Product Details supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::RetentionScheduleService

### Deployment Status
PROPOSED

### Journal Entry
No system implements Retention Schedule Service in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Deployment Status
PROPOSED

### Journal Entry
No system implements Rights Fulfilment Orchestrator in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::RightsRequestIntake

### Deployment Status
PROPOSED

### Journal Entry
No system implements Rights Request Intake in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::SafetySignalDetection

### Deployment Status
PROPOSED

### Journal Entry
No system implements Safety Signal Detection in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Adverse Event and Safety Reporting supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::SerialNumberGenerator

### Deployment Status
PROPOSED

### Journal Entry
No system implements Serial Number Generator in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Product Serialisation and Verification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::SerialisationAlertTriage

### Deployment Status
PROPOSED

### Journal Entry
No system implements Serialisation Alert Triage in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Product Serialisation and Verification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::SerialisationRepository

### Deployment Status
PROPOSED

### Journal Entry
No system implements Serialisation Repository in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Product Serialisation and Verification supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
SolutionComponent::Set Retention Period::V1.0

### Deployment Status
PROPOSED

### Journal Entry
No system implements Set Retention Period in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Data Subject Rights supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::ExcursionAssessment

### Deployment Status
PROPOSED

### Journal Entry
No system implements Temperature Excursion Assessment in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Cold Chain and Dangerous Goods Consignment supply chain, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::TransactionMonitoring

### Deployment Status
PROPOSED

### Journal Entry
No system implements Transaction Monitoring in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Employee Expense Payment and Third Party Onboarding and Payment supply chains, and stays a promise until a system is chosen and linked to it with ImplementedBy.

___

## Classify Promise

### Target Element
CocoPharma::SolutionComponent::TransfersOfValueRegister

### Deployment Status
PROPOSED

### Journal Entry
No system implements Transfers of Value Register in any of Coco Pharmaceuticals' three estates - the component-system mapping found no Strong or Probable candidate at Coco, Austin or Bucharest. It is promised by the Employee Expense Payment and Third Party Onboarding and Payment supply chains, and stays a promise until a system is chosen and linked to it with ImplementedBy.

---

# Promised digital products

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Consolidated Group Results

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Group Consolidation Engine, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Data Subject Rights Requests

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Rights Request Intake, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Exposure Monitoring Results

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Exposure Monitoring Capture, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::External Financial Disclosures

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Disclosure and Statutory Reporting, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Financial Controls Evidence

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Controls Evidence Repository, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Health Surveillance Records

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Health Surveillance Records, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Hospital Certifications

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Certify Hospital, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Incidents And Near Misses

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Incident and Near Miss Reporting, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Long Term Health Archive

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Long Term Health Record Archive, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Market Identifier Submissions

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Market Verification Gateway, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Market Verification Responses

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Market Verification Gateway, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Medical Assessments

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Medical Assessment and Coding, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Product Definitions

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Research Systems, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Case and Pallet Aggregation Recorder, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Patient Pseudonym Register

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Patient Identity Register, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Patient Sample Consignments

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Patient Sample Logistics, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Payment Anomaly Findings

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Transaction Monitoring, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Pharmacovigilance Cases

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Pharmacovigilance Case Management, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Purchase Orders And Receipts

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Procurement Systems, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Qualification Expiry Warnings

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Qualification Currency Checker, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Record Of Processing Activities

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Record of Processing Activities Register, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Requester Identity Verifications

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Data Subject Identity Verification, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Retention Obligations

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Retention Schedule Service, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Retention Period Assignments

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Set Retention Period, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Rights Fulfilment Actions

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Rights Fulfilment Orchestrator, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Safety Signals

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Safety Signal Detection, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Serial Number Allocations

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Serial Number Generator, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Serialisation Alert Investigations

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Serialisation Alert Triage, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Serialised Product Identifiers

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Serialisation Repository, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Temperature Excursion Assessments

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Temperature Excursion Assessment, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Third Party Screening Results

### Deployment Status
PROPOSED

### Journal Entry
Its data arrives from the external Sanctions and Screening Service, and no Coco Pharmaceuticals system receives it yet. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.

___

## Classify Promise

### Target Element
DigitalProduct::Coco::Transfers Of Value

### Deployment Status
PROPOSED

### Journal Entry
No system feeds its data set in any estate, because its solution component, Transfers of Value Register, is itself a promise. The product is defined - data specification, data set and dependencies - but delivers no data until a source system is in place.
___
