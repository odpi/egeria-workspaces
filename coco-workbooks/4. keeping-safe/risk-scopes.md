# Coco Pharmaceuticals - Scoping the Risks

> **Author:** Ivor Padlock (Chief Security Officer), Simon Burr (Chief Information Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-26
> **Description:** Links the risks in the [Risk Register](../0.%20data-governance-program/risk-register.md) to the solution components of the strategic information supply chains that they threaten, using the ScopedBy relationship. Load after `0. data-governance-program` and `1. coco-data-hub/strategic-supply-chain-analysis.md`.

---

## Overview

The risk register rates each risk for likelihood and impact and links it to the threat it realises, but on its own it says nothing about *where* in the business the risk applies.  When Simon Burr began threat modelling, he worked from the solution components that Erin Overview and Peter Profile laid out for the strategic information supply chains.  Those components are linked to the systems that implement them in all three estates - Coco Pharmaceuticals, Austin and Bucharest - so scoping a risk to a component scopes it to every system that implements it.

Each entry below uses the ScopedBy relationship: the risk is the *Target Element* and the solution component that it threatens is the *Scope Reference*.  The *Description* records why the component is in scope.

With these links in place:

* the risks scoped to a component show what needs to be looked at again when the component, or a system that implements it, changes;
* a critical component with no risks scoped to it has probably never been reviewed;
* the implications recorded on each risk can be checked against the systems that actually implement the components.

### What is not yet scoped

Some risks are scoped elsewhere, or have nothing in open metadata to scope them to yet - which is itself a finding:

* **Loss of Clinical Trial Data Integrity** - none of the strategic supply chain components cover clinical trial data.  It is scoped once the clinical trial systems are described.
* **Terrorism-Related Incident at the Annual Conference** and **Failure to Discharge Martyn's Law Responsible Person Duties** - these are scoped to the annual conference project in [martyns-law/annual-conference.md](martyns-law/annual-conference.md), alongside the Responsible Person role.
* **Loss of Undocumented Governance Knowledge on Staff Departure** and **Inconsistent Data Definitions Undermining Cross-Department Reporting** - these are organisational risks that apply across the business rather than to particular components.

---

## Part 1: Risk Scopes

### 1.1 Cyber Security Risks

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::Manufacturing

### Label
threatened-component

### Description
The manufacturing systems as a whole are the target: an encrypted control or scheduling system anywhere in the group halts production.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::PersonalisedOrderScheduler

### Label
threatened-component

### Description
Scheduling of on-demand personalised treatments stops if the scheduler is encrypted, delaying treatment for identified patients.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
threatened-component

### Description
The manufacturing execution system controls production on the shop floor; losing it halts the lines.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::ProcessHistorian

### Label
threatened-component

### Description
Process history is needed to release batches; losing it prevents release even if production resumes.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
threatened-component

### Description
Batch records cannot be completed or reviewed while the electronic batch record system is unavailable.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Scope Reference
CocoPharma::SolutionComponent::PackagingLineController

### Label
threatened-component

### Description
Packaging lines stop if their controllers are encrypted, so finished product cannot be shipped.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::TheftOfPersonalisedTreatmentIP

### Scope Reference
CocoPharma::SolutionComponent::Research

### Label
threatened-component

### Description
The research systems hold the personalised treatment formulas and genomic-targeting methods that this risk is about.

___

---

### 1.2 Privacy and Data Protection Risks

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::AccidentalPatientDataDisclosure

### Scope Reference
CocoPharma::SolutionComponent::PatientIdentityRegister

### Label
threatened-component

### Description
Holds patient identities; a misconfigured access control here exposes patient data directly.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::AccidentalPatientDataDisclosure

### Scope Reference
CocoPharma::SolutionComponent::TreatmentOrderingPortal

### Label
threatened-component

### Description
The portal is used by hospitals to order treatments for named patients, so its access configuration determines who can see their details.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::AccidentalPatientDataDisclosure

### Scope Reference
CocoPharma::SolutionComponent::SampleLogistics

### Label
threatened-component

### Description
Patient samples travel with identifying information, which must only be visible to the people handling them.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::InsiderMisuseOfPatientData

### Scope Reference
CocoPharma::SolutionComponent::PatientIdentityRegister

### Label
threatened-component

### Description
Staff with legitimate access to the patient identity register could use it for an unapproved purpose.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::InsiderMisuseOfPatientData

### Scope Reference
CocoPharma::SolutionComponent::Research

### Label
threatened-component

### Description
Research consumes patient insight from the Data Sharing Hub, so its use must stay within the approved processing purposes.

___

---

### 1.3 Supply Chain and Corporate Risks

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::FraudulentSupplierOnboarding

### Scope Reference
CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow

### Label
threatened-component

### Description
Identity verification of a new supplier happens in the onboarding workflow.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::FraudulentSupplierOnboarding

### Scope Reference
CocoPharma::SolutionComponent::SupplierMasterRegister

### Label
threatened-component

### Description
A fraudulent supplier becomes real once it is in the supplier master register - as happened in the earlier fraud.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::FraudulentSupplierOnboarding

### Scope Reference
CocoPharma::SolutionComponent::PaymentDetailChangeControl

### Label
threatened-component

### Description
Changes to supplier banking details are the usual route for diverting payments.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::FraudulentSupplierOnboarding

### Scope Reference
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Label
threatened-component

### Description
Payments to a fraudulent supplier are made here.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::CounterfeitMaterialsInManufacturing

### Scope Reference
CocoPharma::SolutionComponent::SupplierMaterialCertificates

### Label
threatened-component

### Description
Certificates from a compromised supplier may be forged.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::CounterfeitMaterialsInManufacturing

### Scope Reference
CocoPharma::SolutionComponent::GoodsReceiptAndInspection

### Label
threatened-component

### Description
Incoming materials must be checked before they are accepted.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::CounterfeitMaterialsInManufacturing

### Scope Reference
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Label
threatened-component

### Description
Material must stay in quarantine until it has passed its quality checks.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::CounterfeitMaterialsInManufacturing

### Scope Reference
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Label
threatened-component

### Description
Quality testing of incoming material is recorded in the laboratory information management system.

___

---

### 1.4 Regulatory and Clinical Compliance Risks

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::GMPBatchRecordNonCompliance

### Scope Reference
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
threatened-component

### Description
The batch record must capture every data point needed for GMP traceability.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::GMPBatchRecordNonCompliance

### Scope Reference
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
threatened-component

### Description
Batch records are reviewed and signed off here before product release.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::GMPBatchRecordNonCompliance

### Scope Reference
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Label
threatened-component

### Description
Deviations found during batch review are investigated and documented here.

___

---

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
