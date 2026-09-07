# Strategic Supply Chain Analysis

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-30  
> **Description:** The solution components that implement Coco Pharmaceuticals' strategic information supply chains, their membership of those chains, and the solution linking wires that carry data between them.

---

## Overview

The [strategic information supply chain register](../0.%20data-governance-program/strategic-information-supply-chains.md) named sixteen flows the company governs and monitors, and said plainly what it was leaving out:

> None of these chains is yet linked to the solution components that execute it, which is what makes activity, error and volumetric roll-up possible.  That linkage is what turns the register from a list into a monitor.

This file is that linkage.  For each supply chain it identifies the components that implement it — creating the ones that did not exist, and locating the ones that did — makes them members of the chain, and draws the wires that carry data between them.  Every wire records which supply chains it implements, so that Egeria can assemble each chain's implementation graph from the wires rather than from a hand-drawn picture.

Two of the sixteen chains are not modelled here, because they are already complete.  **Clinical Trials** and **Sustainability Reporting** arrive fully implemented in `CocoComboArchive.omarchive`, with components, roles, wires and membership.  This file adds handover members to the clinical trials chain where another chain now meets it, and otherwise leaves both alone.

---

## What was already there, and what was not

The archive turned out to have laid foundations that nobody had built on.  Seven solution blueprints exist; two of them — Clinical Trial Management and Sustainability Reporting — are complete, and the other five are stubs:

| Archive blueprint | Components before | Components added here |
|---|---|---|
| `Personalized Medicine Order Fulfillment` | 1 (Accounting ledgers) | 6 |
| `Automated Manufacturing Control` | 0 | 14 |
| `Inventory Management` | 1 (Goods Inventory) | 3 |
| `Employee Management` | 1 (Employee Expense Tool) | 10 |
| `Hazardous Material Management` | 1 (HazMat Inventory) | 11 |

Filling in a stub the archive left is better than inventing a parallel blueprint beside it, so that is what this file does.  The remaining components — safety reporting, product master, financial control, third party management and privacy operations — have no archive blueprint to join, and are registered against their information supply chains only.

Eight existing components are reused rather than recreated: the accounting ledgers, the goods inventory, the HazMat inventory, the employee expense tool, Egeria itself, the hospital processes, hospital certification, and the retention period step.  Several of them turn out to belong to more supply chains than the archive had them in — the HazMat inventory alone serves occupational health, dangerous goods transport and inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.

---

## Relationship to `solution-design.md`

`solution-design.md` describes the Data Hub and the eight business functions that exchange data through it.  Those eight components are the landscape every one of these supply chains runs over, so they are needed here — and this file loads first.  The eight `Create Solution Component` commands have therefore **moved** from `solution-design.md` into Part 1 below, and `solution-design.md` now links them to its blueprint instead of creating them.  Its blueprint, its wires and its narrative are unchanged.

The move also let the eight pick up a `Solution Component Type`, which they did not have, so they now render with the right shape in Egeria's graphs.

---

## Load order

This file loads **after** `0. data-governance-program/strategic-information-supply-chains.md`, which creates nine of the sixteen supply chains, and **before** `solution-design.md`, which now depends on it.

```
dr_egeria --directive process --userid erinoverview --user_pass secret strategic-supply-chain-analysis.md
```

---

## Part 1: Business System Groups

The eight groups moved from `solution-design.md`, and three more the strategic chains needed: quality and regulatory, people, and privacy operations.  They are containers rather than systems — each one holds the components that do the actual work, so that a supply chain can be read at either level.

___

## Create Solution Component

### Display Name
Data Hub

### Qualified Name
CocoPharma::SolutionComponent::DataHub

### Description
The central integration point of the architecture. Receives orders, status and inventory updates from every connected business function and distributes requirements and insight back out to them.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Data Hub

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Patient Treatment (Sales/Direct) Systems

### Qualified Name
CocoPharma::SolutionComponent::PatientTreatment

### Description
The sales and direct-to-patient treatment channel. Originates new business into the Data Hub.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Finance Systems

### Qualified Name
CocoPharma::SolutionComponent::Finance

### Description
Manages invoices, payments and expenses, and raises new orders on behalf of the business.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Procurement Systems

### Qualified Name
CocoPharma::SolutionComponent::Procurement

### Description
Sources materials and services against requirements published by the Data Hub, and raises new orders back into it.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Research Systems

### Qualified Name
CocoPharma::SolutionComponent::Research

### Description
Develops new treatments, consuming patient insight from the Data Hub and publishing new recipes back into it.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### In Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Warehouse Systems

### Qualified Name
CocoPharma::SolutionComponent::Warehouse

### Description
Holds materials and finished goods, reporting inventory levels to the Data Hub and fulfilling materials requests from Manufacturing.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Manufacturing Systems

### Qualified Name
CocoPharma::SolutionComponent::Manufacturing

### Description
Produces treatments, reporting manufacturing status to the Data Hub, requesting materials from the Warehouse, and passing finished shipments to Delivery.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Delivery Systems

### Qualified Name
CocoPharma::SolutionComponent::Delivery

### Description
Delivers shipments received from Manufacturing to their destination, reporting delivery status back to the Data Hub.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Quality and Regulatory Systems

### Qualified Name
CocoPharma::SolutionComponent::QualitySystems

### Description
The systems through which quality and regulatory affairs operate: laboratory results, deviations and corrective actions, batch certification, market authorisations, safety case handling and the assessments that gate a release. They sit alongside manufacturing rather than inside it, because the point of the quality function is that it can say no.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
People Systems

### Qualified Name
CocoPharma::SolutionComponent::PeopleSystems

### Description
The systems holding the worker record and everything derived from it: the joiner, mover and leaver process, payroll, the corporate directory, learning and qualification records, and the long-lived health records that outlive employment. Several regulated processes read from here as compliance evidence rather than as human resources data.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Privacy Operations Systems

### Qualified Name
CocoPharma::SolutionComponent::PrivacyOperations

### Description
The systems through which the privacy function operates across every other system: the record of processing activities, data subject request handling, personal data discovery, and the retention schedules that decide what may and may not be erased.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Business Systems Group

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: The Component Catalogue

Seventy-one components, grouped by the business system group that holds them.  Each declares the supply chains it is a member of at the point it is created, so that the chains below are complete without a further membership command for anything defined in this file.

A component that appears in several chains is created once.  The qualification register belongs to four of them, and that is the finding rather than an accident of modelling: a record human resources maintains for employment reasons is read as compliance evidence by manufacturing, by clinical trials and by dangerous goods transport.

### 2.1 Data Hub

Master data that no single business function owns.

___

## Create Solution Component

### Display Name
Product Master Register

### Qualified Name
CocoPharma::SolutionComponent::ProductMasterRegister

### Description
The authoritative definition of every product: its identity, presentations, pack configurations, composition and handling requirements. It is read by manufacturing, serialisation, distribution, sales and finance, none of which own it, which is the definition of master data and the reason an inconsistency here surfaces somewhere else.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Master Data Management

### In Solution Components
- CocoPharma::SolutionComponent::DataHub

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Product Data Distribution

### Qualified Name
CocoPharma::SolutionComponent::ProductDataDistribution

### Description
Publishes changes to the product master to every system that holds a copy, and records which of them have applied it. Knowing who has not yet applied a change is the part that matters: an inconsistent estate is only dangerous while nobody knows which systems are stale.

### Solution Component Type
Data Distribution

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::DataHub

### In Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.2 Patient Treatment (Sales/Direct) Systems

Where a treatment decision taken outside the company becomes an instruction inside it.

___

## Create Solution Component

### Display Name
Treatment Ordering Portal

### Qualified Name
CocoPharma::SolutionComponent::TreatmentOrderingPortal

### Description
The channel through which a treating clinician orders a personalised therapy for a named patient. It is the point at which a treatment decision made outside Coco Pharmaceuticals becomes an instruction inside it, and the point at which the patient identity that the rest of the chain protects first enters the estate.

### Solution Component Type
User Interface

### Planned Deployed Implementation Type
Web Application

### In Solution Components
- CocoPharma::SolutionComponent::PatientTreatment

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Patient Identity Register

### Qualified Name
CocoPharma::SolutionComponent::PatientIdentityRegister

### Description
Holds the link between the patient, the material taken from them, and the therapy manufactured from it. Every other system in the chain works from the pseudonym this register issues, so that manufacturing can be certain it has the right material without holding the patient's identity.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
PostgreSQL Database

### In Solution Components
- CocoPharma::SolutionComponent::PatientTreatment

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.3 Finance Systems

The ledger's feeds, the close, and the payment flows the supplier fraud travelled.

___

## Create Solution Component

### Display Name
Order to Invoice Processing

### Qualified Name
CocoPharma::SolutionComponent::OrderToInvoice

### Description
Converts a fulfilled treatment order into an invoice and a revenue posting. It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Subledger Feeds

### Qualified Name
CocoPharma::SolutionComponent::SubledgerFeeds

### Description
The scheduled and event-driven flows that carry transactions from the operational systems into the ledger. Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.

### Solution Component Type
Data Distribution

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Journal Entry Review

### Qualified Name
CocoPharma::SolutionComponent::JournalEntryReview

### Description
The review and approval of manual journal entries above a materiality threshold. Manual adjustment is the segment of the flow least covered by system controls and most able to change a reported figure, which is why it is the segment with a person in it.

### Solution Component Type
Manual Process

### Planned Deployed Implementation Type
Manual Process

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Group Consolidation Engine

### Qualified Name
CocoPharma::SolutionComponent::GroupConsolidation

### Description
Consolidates the ledgers of the US parent and the UK and EU subsidiaries, eliminating intercompany balances and translating currency. It is where several sets of books become one set of figures, and where the group structure stops being an organisational fact and becomes an accounting one.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Disclosure and Statutory Reporting

### Qualified Name
CocoPharma::SolutionComponent::DisclosureReporting

### Description
Produces the statements filed with regulators and published to the market. Every figure it emits must be resolvable back through the consolidation and the ledger to the transactions it was built from, on demand.

### Solution Component Type
Publishing

### Planned Deployed Implementation Type
Reporting Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Controls Evidence Repository

### Qualified Name
CocoPharma::SolutionComponent::ControlsEvidenceRepository

### Description
Holds the documentation and test evidence for the internal controls over financial reporting. The controls it evidences are controls over this chain, so the repository is part of the chain rather than an audit of it.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Content Manager

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Payment Detail Change Control

### Qualified Name
CocoPharma::SolutionComponent::PaymentDetailChangeControl

### Description
Governs changes to a supplier's bank details as a controlled event with independent verification, rather than as routine maintenance. This is where the flow has historically been attacked, and it is the one step that is cheap to add and expensive to omit.

### Solution Component Type
Automated Action

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Supplier Payment Processing

### Qualified Name
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Description
Matches invoices to orders and receipts, authorises payment, and instructs the bank. It reads the screening status and the payment details at the moment of authorisation, which is the only moment at which either of them protects anything.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Transaction Monitoring

### Qualified Name
CocoPharma::SolutionComponent::TransactionMonitoring

### Description
Looks across payments for the patterns that reveal fraud, duplicate payment and unusual supplier behaviour. It exists because the pattern that revealed the original fraud was visible across the whole flow and in no single transaction within it.

### Solution Component Type
Insight Model

### Planned Deployed Implementation Type
Analytics Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Transfers of Value Register

### Qualified Name
CocoPharma::SolutionComponent::TransfersOfValueRegister

### Description
Identifies and records payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, so that they can be disclosed. Reconstructing this afterwards from a general ledger is the failure mode it exists to prevent.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
PostgreSQL Database

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Expense Approval Workflow

### Qualified Name
CocoPharma::SolutionComponent::ExpenseApprovalWorkflow

### Description
Routes an expense claim for approval and carries the approval forward to payment. The approval is only worth anything if it is still attached to the claim when the payment is made, which is a property of this flow rather than of either system it connects.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::Finance

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.4 Procurement Systems

Third party onboarding and the supplier record everything else reads.

___

## Create Solution Component

### Display Name
Supplier Material Certificates

### Qualified Name
CocoPharma::SolutionComponent::SupplierMaterialCertificates

### Description
Holds the certificates of analysis and conformity supplied with incoming material. The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Content Manager

### In Solution Components
- CocoPharma::SolutionComponent::Procurement

### In Solution Blueprints
- SolutionBlueprint::Inventory Management::Inventory Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Third Party Onboarding Workflow

### Qualified Name
CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow

### Description
Drives a proposed third party through screening, risk assessment and approval to the creation of a supplier record. It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::Procurement

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Supplier Master Register

### Qualified Name
CocoPharma::SolutionComponent::SupplierMasterRegister

### Description
The authoritative record of every third party the company transacts with, including its screening status, risk rating and payment details. The supplier fraud was possible because this record was not authoritative; making it so is the control.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Master Data Management

### In Solution Components
- CocoPharma::SolutionComponent::Procurement

### In Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.5 Warehouse Systems

Receipt, quarantine and release of physical material.

___

## Create Solution Component

### Display Name
Goods Receipt and Inspection

### Qualified Name
CocoPharma::SolutionComponent::GoodsReceiptAndInspection

### Description
Receives physical material, checks it against the order and the accompanying documentation, and records what actually arrived. It is the point at which a supplier's claim becomes the company's record.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Warehouse

### In Solution Blueprints
- SolutionBlueprint::Inventory Management::Inventory Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Material Quarantine and Release Control

### Qualified Name
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Description
Holds received material in quarantine until testing and documentation review are complete, and releases it for use only then. It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.

### Solution Component Type
Automated Action

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Warehouse

### In Solution Blueprints
- SolutionBlueprint::Inventory Management::Inventory Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.6 Manufacturing Systems

Production and packaging, including everything serialisation needs to run at line speed.

___

## Create Solution Component

### Display Name
Personalised Order Scheduler

### Qualified Name
CocoPharma::SolutionComponent::PersonalisedOrderScheduler

### Description
Turns an accepted order and its arriving patient material into a scheduled manufacturing slot. Unlike batch scheduling it cannot defer or re-sequence freely, because the material it is scheduling has a viable life measured in days.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Scheduling Application

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Manufacturing Execution System

### Qualified Name
CocoPharma::SolutionComponent::ManufacturingExecution

### Description
Directs and records the execution of each production step: what was done, by whom, with which materials and on which equipment. It is the source of most of what ends up in the batch record, and it records contemporaneously because reconstruction afterwards is precisely what the data integrity obligations forbid.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Process Historian

### Qualified Name
CocoPharma::SolutionComponent::ProcessHistorian

### Description
Continuously captures process parameters from plant instrumentation. It holds the evidence that the process stayed within its validated range, at a resolution nobody reads unless something went wrong — which is exactly when it cannot be recreated.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
Time Series Database

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Equipment Qualification Register

### Qualified Name
CocoPharma::SolutionComponent::EquipmentQualificationRegister

### Description
Records the qualification and calibration status of every piece of equipment used in production. It is consulted at the moment of use, because a qualification that lapsed last week invalidates production that has already happened.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Electronic Batch Record System

### Qualified Name
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Description
Assembles the complete record of a batch from every contributing system and holds it for the life of the obligation. Completeness is a property of the chain having delivered, not of this system having stored what it was given, which is why it is modelled here as the convergence point of several supply chains rather than as one more manufacturing application.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Serial Number Generator

### Qualified Name
CocoPharma::SolutionComponent::SerialNumberGenerator

### Description
Issues the unique identifiers applied to saleable packs. Uniqueness is assured here, at the point of generation, because a number issued twice cannot be corrected once packs are distributed — detection in reconciliation is already too late.

### Solution Component Type
Software Service

### Planned Deployed Implementation Type
Serialisation Service

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Packaging Line Controller

### Qualified Name
CocoPharma::SolutionComponent::PackagingLineController

### Description
Applies and verifies identifiers on the packaging line, and commissions each pack as a real, saleable object. It works at line speed, which is why the identifiers have to be present and valid before the line starts rather than requested as it runs.

### Solution Component Type
Automated Action

### Planned Deployed Implementation Type
Line Control System

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Case and Pallet Aggregation Recorder

### Qualified Name
CocoPharma::SolutionComponent::AggregationRecorder

### Description
Records which packs are in which case and which cases are on which pallet. The relationships it captures are what allow a shipment to be verified without opening it, and what make a recall a query rather than a search.

### Solution Component Type
Automated Action

### Planned Deployed Implementation Type
Line Control System

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Serialisation Repository

### Qualified Name
CocoPharma::SolutionComponent::SerialisationRepository

### Description
The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned. It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Serialisation Platform

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Market Verification Gateway

### Qualified Name
CocoPharma::SolutionComponent::MarketVerificationGateway

### Description
Routes identifier data to the national and regional verification system required by each destination market, and receives verification, decommissioning and alert traffic back. Destination determines the scheme, so the same production run may leave through several different routes.

### Solution Component Type
Data Distribution

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::Manufacturing

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.7 Delivery Systems

Consignments in both directions, and the classification and monitoring that travel with them.

___

## Create Solution Component

### Display Name
Patient Sample Logistics

### Qualified Name
CocoPharma::SolutionComponent::SampleLogistics

### Description
Arranges collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site. It is the inbound half of a round trip that has a clock running from the moment the sample is taken.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Logistics Application

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Treatment Delivery Tracking

### Qualified Name
CocoPharma::SolutionComponent::TreatmentDeliveryTracking

### Description
Tracks the finished therapy from release to administration at the treating site, and reports arrival back into the order. It closes the loop that the ordering portal opened.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
Tracking Service

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Personalized Medicine Order Fulfillment::Personalized Medicine Order Fulfillment Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Transport Classification Service

### Qualified Name
CocoPharma::SolutionComponent::TransportClassificationService

### Description
Derives the transport classification of a consignment from the substance and biological agent registers and the form the material is being shipped in. It is a library rather than a process because the same rules have to give the same answer to despatch, to procurement and to the person signing the declaration.

### Solution Component Type
Software Library

### Planned Deployed Implementation Type
Rules Service

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Shipping Documentation Preparation

### Qualified Name
CocoPharma::SolutionComponent::ShippingDocumentation

### Description
The preparation and signature of the dangerous goods declaration and accompanying documents by a certificated person. The signature is the act that transfers nothing: the shipper's liability stays with the company however the carrier behaves afterwards.

### Solution Component Type
Manual Process

### Planned Deployed Implementation Type
Manual Process

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Temperature Monitoring Devices

### Qualified Name
CocoPharma::SolutionComponent::TemperatureMonitoringDevices

### Description
The loggers and live monitors travelling inside consignments. They are themselves dangerous goods, because they contain lithium batteries, which is the small irony at the centre of this chain.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
IoT Device

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Cold Chain Data Collector

### Qualified Name
CocoPharma::SolutionComponent::ColdChainDataCollector

### Description
Collects the temperature record from devices and carrier systems on arrival, and reconciles it against the permitted range for the product being shipped. A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::Delivery

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.8 Quality and Regulatory Systems

The components that can say no: laboratory results, deviations, certification, safety cases and the assessments that gate a release.

___

## Create Solution Component

### Display Name
Safety Intake Gateway

### Qualified Name
CocoPharma::SolutionComponent::SafetyIntakeGateway

### Description
The single point at which a suspected adverse reaction is registered, whatever door it arrived through. It exists because the statutory reporting clock starts on first receipt anywhere in the company, and a clock that starts in five different places cannot be measured.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Product Complaint Intake

### Qualified Name
CocoPharma::SolutionComponent::ProductComplaintIntake

### Description
Receives complaints about product quality from pharmacies, distributors and patients, and separates those that are also potential safety events from those that are not. The separation is deliberately generous: a complaint wrongly treated as a safety event costs an assessment, the reverse costs a missed report.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Pharmacovigilance Case Management

### Qualified Name
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Description
Holds the safety case from receipt through follow-up to closure, and carries the reporting clock that the regulators measure. Every other component in this chain either feeds it or reads from it.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Medical Assessment and Coding

### Qualified Name
CocoPharma::SolutionComponent::MedicalAssessmentAndCoding

### Description
The qualified medical judgement of seriousness, expectedness and causality, and the coding of the event to a standard dictionary. It is the step that decides whether a report is expedited or periodic, which makes it the step the clock is most sensitive to.

### Solution Component Type
Manual Process

### Planned Deployed Implementation Type
Manual Process

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Safety Signal Detection

### Qualified Name
CocoPharma::SolutionComponent::SafetySignalDetection

### Description
Looks across accumulated cases for patterns that no single case shows. It is the reason the chain has to consolidate every source rather than report each one separately: a signal visible across trial and post-market data is invisible in either alone.

### Solution Component Type
Insight Model

### Planned Deployed Implementation Type
Analytics Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Regulatory Safety Submission

### Qualified Name
CocoPharma::SolutionComponent::RegulatorySafetySubmission

### Description
Formats and transmits expedited and periodic safety reports to the regulator of each market the product is authorised in. Each market has its own format, timetable and acknowledgement, and an unacknowledged submission is not a submission.

### Solution Component Type
Publishing

### Planned Deployed Implementation Type
Regulatory Gateway

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Laboratory Information Management System

### Qualified Name
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Description
Manages sampling, testing and results for raw materials, in-process checks and finished product. Its results are gates rather than reports: material cannot be issued and product cannot be released until it has answered.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Deviation and CAPA Management

### Qualified Name
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Description
Records departures from the approved process, drives their investigation, and tracks the corrective and preventive actions that follow. An open deviation is a gate on certification, so this component sits inside the release flow rather than beside it.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Batch Review and QP Certification

### Qualified Name
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Description
The review of the assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market. It is the single human decision the whole chain exists to support, and it is market-specific.

### Solution Component Type
Manual Process

### Planned Deployed Implementation Type
Manual Process

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Serialisation Alert Triage

### Qualified Name
CocoPharma::SolutionComponent::SerialisationAlertTriage

### Description
Investigates verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals. An alert that is not investigated is a falsification signal that was received and ignored.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Automated Manufacturing Control::Automated Manufacturing Control Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Temperature Excursion Assessment

### Qualified Name
CocoPharma::SolutionComponent::ExcursionAssessment

### Description
Assesses a temperature excursion against the product's stability data and dispositions the consignment. It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Market Authorisation Register

### Qualified Name
CocoPharma::SolutionComponent::MarketAuthorisationRegister

### Description
Records which product may be placed on which market, under which authorisation and subject to which conditions. Batch certification and serialisation routing both read from it, so a market added here changes what two other chains do.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Content Manager

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Exposure Banding Register

### Qualified Name
CocoPharma::SolutionComponent::ExposureBandingRegister

### Description
Assigns each substance to an occupational exposure band and each band to a required containment level. It is the rule set that turns a substance identity into a control requirement, and it is shared with the transport classification service rather than duplicated.

### Solution Component Type
Software Library

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Exposure Monitoring Capture

### Qualified Name
CocoPharma::SolutionComponent::ExposureMonitoringCapture

### Description
Captures personal and static exposure measurements from monitoring campaigns and compares them to the banded limits. An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Laboratory Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Incident and Near Miss Reporting

### Qualified Name
CocoPharma::SolutionComponent::IncidentAndNearMissReporting

### Description
Records incidents, near misses and their investigations, and feeds what they reveal back into the assessments. It is what makes this chain a loop rather than a line, and it only works if reporting is blameless enough that people use it.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::QualitySystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.9 People Systems

The worker record and everything anchored on it, including records that outlive the employment.

___

## Create Solution Component

### Display Name
Worker Master Register

### Qualified Name
CocoPharma::SolutionComponent::WorkerMasterRegister

### Description
The authoritative record of every worker — employees and contractors alike — and the anchor that qualification, health surveillance, access and payroll records are all held against. Almost everything the people systems do is a read of this record.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Master Data Management

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Joiner Mover Leaver Workflow

### Qualified Name
CocoPharma::SolutionComponent::JoinerMoverLeaverWorkflow

### Description
Distributes a joining, moving or leaving event to every system that must act on it, and records which of them have. Its latency is what the timeliness obligation measures, and the leaver case is the one that matters: access outlives employment by exactly this chain's delay.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Identity and Access Provisioning

### Qualified Name
CocoPharma::SolutionComponent::IdentityAndAccessProvisioning

### Description
Creates, changes and removes accounts and entitlements in response to worker events. It is driven from the worker record rather than from requests, because an access removal that depends on somebody remembering to ask does not happen.

### Solution Component Type
Automated Action

### Planned Deployed Implementation Type
Identity Management

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Payroll System

### Qualified Name
CocoPharma::SolutionComponent::PayrollSystem

### Description
Calculates and pays remuneration, and produces the pay data that statutory reporting and pay equity analysis are built from. It runs in several countries under several sets of rules from one worker record.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Corporate Directory

### Qualified Name
CocoPharma::SolutionComponent::CorporateDirectory

### Description
The searchable directory of people, roles and reporting lines that the rest of the organisation uses. It is downstream of the worker record and is frequently the first place a stale joiner or leaver event becomes visible to everybody.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Directory Service

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Competency Framework Register

### Qualified Name
CocoPharma::SolutionComponent::CompetencyFrameworkRegister

### Description
Defines what competencies each regulated role requires. It is the specification this chain is judged against, and it changes when a process or a regulation changes rather than when a person does.

### Solution Component Type
Software Library

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Learning Management System

### Qualified Name
CocoPharma::SolutionComponent::LearningManagement

### Description
Delivers training, records completion and assessment, and schedules refreshers. Its output is evidence consumed by two regulated processes, which is a heavier duty than the system was originally bought for.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
COTS Application

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Qualification and Competency Register

### Qualified Name
CocoPharma::SolutionComponent::CompetencyRegister

### Description
The authoritative statement of what each worker is currently qualified to do. Manufacturing and drug development read it as compliance evidence, so a local copy that has drifted is worse than no copy at all.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
PostgreSQL Database

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Qualification Currency Checker

### Qualified Name
CocoPharma::SolutionComponent::QualificationCurrencyChecker

### Description
Watches for qualifications approaching or past expiry and warns the processes that depend on them before rather than after. Currency is the property this chain is actually judged on: a record that is correct but stale is indistinguishable from a wrong one at the point of use.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
Integration Service

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Employee Management::Employee Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Health Surveillance Records

### Qualified Name
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Description
Holds the results of health surveillance appointments against the individual worker. The record belongs to the person it describes rather than to the company, which constrains who this chain may deliver it to and in what form.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Clinical Records System

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Long Term Health Record Archive

### Qualified Name
CocoPharma::SolutionComponent::LongTermHealthArchive

### Description
Retains health surveillance and exposure records for forty years from the last entry, across every system migration in that period. Its requirement is not storage but interpretability: a record that survives and can no longer be read is the same failure as one that was lost.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Archive Service

### In Solution Components
- CocoPharma::SolutionComponent::PeopleSystems

### In Solution Blueprints
- SolutionBlueprint::Hazardous Material Management::Hazardous Material Management Solution Blueprint

### In Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.10 Privacy Operations Systems

The components that reach across every other chain on behalf of a data subject.

___

## Create Solution Component

### Display Name
Rights Request Intake

### Qualified Name
CocoPharma::SolutionComponent::RightsRequestIntake

### Description
Receives requests from data subjects through every channel the company offers, and starts the statutory clock. The clock runs from receipt by any part of the company, so an email to a site address counts exactly as much as a submission through this component.

### Solution Component Type
User Interface

### Planned Deployed Implementation Type
Web Application

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Data Subject Identity Verification

### Qualified Name
CocoPharma::SolutionComponent::IdentityVerification

### Description
Establishes that the requester is who they claim to be, proportionately to what they are asking for. It is the step that stops the rights process from becoming an attack on the data it is meant to protect.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Record of Processing Activities Register

### Qualified Name
CocoPharma::SolutionComponent::RecordOfProcessingRegister

### Description
Records what personal data the company processes, for what purpose, under what lawful basis, and where it is held. It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.

### Solution Component Type
Data Storage

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Personal Data Discovery

### Qualified Name
CocoPharma::SolutionComponent::PersonalDataDiscovery

### Description
Surveys systems and stores for personal data and reconciles what it finds against the record of processing. It exists because the register describes what the company believes it processes and this describes what it actually holds.

### Solution Component Type
Long Running Daemon

### Planned Deployed Implementation Type
Discovery Service

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Rights Fulfilment Orchestrator

### Qualified Name
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Description
Fans a verified request out to every system and processor holding the person's data, collects what comes back, and drives erasure, rectification and objection decisions onward to the systems that must act on them. It is the component that turns a register into an answer.

### Solution Component Type
Multi-Step Process

### Planned Deployed Implementation Type
Cloud Application

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Retention Schedule Service

### Qualified Name
CocoPharma::SolutionComponent::RetentionScheduleService

### Description
Holds the retention obligation attaching to each category of personal data, so that an erasure decision can be checked against the obligations that override it. Clinical trial records, employment decisions and health surveillance all outrank a request to be forgotten, and the chain has to know that per holding rather than in general.

### Solution Component Type
Software Library

### Planned Deployed Implementation Type
Rules Service

### In Solution Components
- CocoPharma::SolutionComponent::PrivacyOperations

### In Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.11 External Systems

Systems operated outside Coco Pharmaceuticals that the chains hand data to or receive it from.  They are modelled so that the boundary is visible, not because the company can see inside them.

___

## Create Solution Component

### Display Name
National Verification Systems

### Qualified Name
CocoPharma::SolutionComponent::NationalVerificationSystems

### Description
The repositories operated outside Coco Pharmaceuticals that pharmacies check before dispensing. They are opaque to the company and they are also where its product data becomes publicly visible in real time, which is why defects in this chain are frequently reported inward rather than detected internally.

### Solution Component Type
Third Party Process

### Planned Deployed Implementation Type
External Organization Processes

### In Information Supply Chain
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Carrier Systems

### Qualified Name
CocoPharma::SolutionComponent::CarrierSystems

### Description
The tracking and handling systems of the couriers and freight forwarders that physically move the goods. The company reads status from them and hands documentation to them, but has no visibility of what happens inside them.

### Solution Component Type
Third Party Process

### Planned Deployed Implementation Type
External Organization Processes

### In Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Sanctions and Screening Service

### Qualified Name
CocoPharma::SolutionComponent::SanctionsAndScreeningService

### Description
The external service that screens third parties against sanctions, politically exposed person and adverse media lists. Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

### Solution Component Type
Third Party Process

### Planned Deployed Implementation Type
External Service

### In Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Authors
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: The Supply Chains

Each chain below lists its members, adds the ones that already existed outside this file, and then draws its wires.  Every wire names the supply chains it implements in its `ISC Qualified Names`, which is how a wire that carries a handover between two chains ends up counted in both.

### 3.1 Personalised Treatment Ordering

The chain begins outside the company, with a treating clinician, and ends outside it again, with the same clinician administering the therapy.  Everything in between is a round trip carrying one patient's identity, and the components are shaped by that: an identity register that issues the pseudonym the rest of the chain works from, a scheduler that cannot re-sequence freely because its input has a viable life, and a delivery tracker whose job is to close the loop the order opened.

The archive's **Personalized Medicine Order Fulfillment** blueprint already existed with a single component in it — the accounting ledgers.  The components below fill it in.

| Component | Role in this chain |
|---|---|
| **Treatment Ordering Portal** | The channel through which a treating clinician orders a personalised therapy for a named patient. |
| **Patient Identity Register** | Holds the link between the patient, the material taken from them, and the therapy manufactured from it. |
| **Patient Sample Logistics** | Arranges collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site. |
| **Personalised Order Scheduler** | Turns an accepted order and its arriving patient material into a scheduled manufacturing slot. |
| **Treatment Delivery Tracking** | Tracks the finished therapy from release to administration at the treating site, and reports arrival back into the order. |
| **Order to Invoice Processing** | Converts a fulfilled treatment order into an invoice and a revenue posting. |
| **Accounting ledgers** | Revenue from a fulfilled treatment order posts here, which is where the clinical event becomes a financial one. |
| **Data Hub** | New business originating in the treatment channel is published to the hub for the rest of the business to see. |
| Electronic Batch Record System *(handover)* | A personalised therapy is manufactured under a batch record like any other product, and the chain of identity attaches to it. |
| Batch Review and QP Certification *(handover)* | The same certification decision releases a personalised therapy, and is what starts delivery to the treating site. |
| Cold Chain Data Collector *(handover)* | Patient material arrives under the same transit monitoring as product leaves, on a much shorter clock. |
| Safety Intake Gateway *(handover)* | A reaction reported by a treating clinician leaves this chain through the ordering portal and enters the safety chain. |
| Subledger Feeds *(handover)* | Invoiced treatment revenue reaches the ledger through the subledger feeds. |
| Rights Fulfilment Orchestrator *(handover)* | Patient data held against the identity register is reachable by a rights request, which is what concentrating it was for. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### ISC Child
SolutionComponent::Accounting ledgers::V1.0

### Membership Rationale
Revenue from a fulfilled treatment order posts here, which is where the clinical event becomes a financial one.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TreatmentOrderingPortal

### Component2
CocoPharma::SolutionComponent::PatientIdentityRegister

### Label
register order

### Description
The order is registered against the patient and a pseudonym is issued for everything downstream to work from.

### Data Exchanged
patient identity, prescribing clinician, product ordered

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TreatmentOrderingPortal

### Component2
CocoPharma::SolutionComponent::SampleLogistics

### Label
request sample collection

### Description
Collection is requested at the treating site as soon as the order is accepted, because the clock starts when the sample is taken rather than when it arrives.

### Data Exchanged
collection site, time window, material required

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SampleLogistics

### Component2
CocoPharma::SolutionComponent::PersonalisedOrderScheduler

### Label
patient material received

### Description
Arrival of the material is what releases the manufacturing slot. Condition on arrival determines whether there is still a slot worth releasing.

### Data Exchanged
consignment identity, arrival condition, remaining viable life

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PatientIdentityRegister

### Component2
CocoPharma::SolutionComponent::PersonalisedOrderScheduler

### Label
identified manufacturing instruction

### Description
Manufacturing receives enough identity to be certain it has the right material, and no more than that.

### Data Exchanged
pseudonym, product specification, patient-specific parameters

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PersonalisedOrderScheduler

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
open batch

### Description
The scheduled slot opens a batch record. This is where the ordering chain hands over to the manufacturing chain, and where the chain of identity obligation attaches to the batch.

### Data Exchanged
batch identity, pseudonym, product specification

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Component2
CocoPharma::SolutionComponent::TreatmentDeliveryTracking

### Label
therapy released

### Description
Certification releases the therapy for despatch to the treating site.

### Data Exchanged
batch identity, pseudonym, certification, storage conditions

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TreatmentDeliveryTracking

### Component2
CocoPharma::SolutionComponent::PatientIdentityRegister

### Label
administration confirmed

### Description
Confirmation closes the loop against the original order, and is the point at which the chain of identity is shown to have held end to end.

### Data Exchanged
pseudonym, delivery and administration timestamps

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TreatmentDeliveryTracking

### Component2
CocoPharma::SolutionComponent::OrderToInvoice

### Label
fulfilment confirmed

### Description
Fulfilment is what makes the order invoiceable, so the financial record is derived from the delivery record rather than agreed with it later.

### Data Exchanged
order identity, delivery evidence

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::OrderToInvoice

### Component2
SolutionComponent::Accounting ledgers::V1.0

### Label
revenue posting

### Description
Invoiced revenue posts to the ledger and is consolidated into the published figures.

### Data Exchanged
invoice, revenue recognition data

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::OrderToInvoice

### Component2
CocoPharma::SolutionComponent::DataHub

### Label
new-business

### Description
The completed order is published to the hub so that research, manufacturing and finance see the same view of new business.

### Data Exchanged
order, fulfilment and revenue summary

### ISC Qualified Names
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

### 3.2 Adverse Event and Safety Reporting

The defining feature of this chain is its shape: many doors, one clock.  The intake gateway exists precisely because a reporting clock that starts in five different places cannot be measured, and every source — trial site, treating clinician, patient, product complaint — is routed through it before anything else happens.

Nothing in the archive covered this area, so all seven components are new.  Two of the doors are components that already exist for other reasons: the hospital processes that feed the clinical trials chain, and the ordering portal through which clinicians reach the company.

| Component | Role in this chain |
|---|---|
| **Safety Intake Gateway** | The single point at which a suspected adverse reaction is registered, whatever door it arrived through. |
| **Product Complaint Intake** | Receives complaints about product quality from pharmacies, distributors and patients, and separates those that are also potential safety events from those that are not. |
| **Pharmacovigilance Case Management** | Holds the safety case from receipt through follow-up to closure, and carries the reporting clock that the regulators measure. |
| **Medical Assessment and Coding** | The qualified medical judgement of seriousness, expectedness and causality, and the coding of the event to a standard dictionary. |
| **Safety Signal Detection** | Looks across accumulated cases for patterns that no single case shows. |
| **Regulatory Safety Submission** | Formats and transmits expedited and periodic safety reports to the regulator of each market the product is authorised in. |
| **Hospital Processes** | Trial sites report suspected adverse reactions observed in participants, which is one of the doors the intake gateway exists to consolidate. |
| **Treatment Ordering Portal** | Treating clinicians report reactions through the same channel they order through, which is the door most likely to be used and least likely to be designed for. |
| Deviation and CAPA Management *(handover)* | A safety signal traced to a product or process fault becomes a corrective action, so the quality system is where this chain ends when the cause is manufacturing. |
| Market Authorisation Register *(handover)* | A confirmed signal can change what may be sold and how it must be labelled, which is a safety outcome expressed as a product master change. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### ISC Child
SolutionComponent::Hospital Processes::V1.0

### Membership Rationale
Trial sites report suspected adverse reactions observed in participants, which is one of the doors the intake gateway exists to consolidate.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
SolutionComponent::Hospital Processes::V1.0

### Component2
CocoPharma::SolutionComponent::SafetyIntakeGateway

### Label
site safety report

### Description
Suspected adverse reactions observed at a trial site enter the safety chain here, and the clock starts at this handover.

### Data Exchanged
suspected reaction, participant pseudonym, trial identity

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TreatmentOrderingPortal

### Component2
CocoPharma::SolutionComponent::SafetyIntakeGateway

### Label
clinician report

### Description
A reaction reported by a treating clinician after administration enters through a different door under the same clock.

### Data Exchanged
suspected reaction, patient pseudonym, product and batch

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductComplaintIntake

### Component2
CocoPharma::SolutionComponent::SafetyIntakeGateway

### Label
complaint with safety content

### Description
Complaints that may also be safety events are routed on deliberately generously: a false positive costs an assessment, a false negative costs a missed report.

### Data Exchanged
complaint, product, batch, reported harm

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SafetyIntakeGateway

### Component2
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Label
open case

### Description
The case is opened with the receipt timestamp from the original door rather than from the gateway, which is what makes the clock measurable end to end.

### Data Exchanged
consolidated report, receipt timestamp, source

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Component2
CocoPharma::SolutionComponent::MedicalAssessmentAndCoding

### Label
assess and code

### Description
Qualified medical judgement of seriousness, expectedness and causality, and coding to a standard dictionary.

### Data Exchanged
case narrative, product, patient context

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MedicalAssessmentAndCoding

### Component2
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Label
assessment recorded

### Description
The assessment decides whether the report is expedited or periodic, which is the step the clock is most sensitive to.

### Data Exchanged
seriousness, expectedness, causality, coded terms

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Component2
CocoPharma::SolutionComponent::SafetySignalDetection

### Label
case data for analysis

### Description
Signals are visible across accumulated cases and in no single one, which is why the chain consolidates every source rather than reporting each separately.

### Data Exchanged
coded cases, exposure denominators

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement

### Component2
CocoPharma::SolutionComponent::RegulatorySafetySubmission

### Label
submit report

### Description
Each market has its own format, timetable and acknowledgement, and an unacknowledged submission is not a submission.

### Data Exchanged
expedited and periodic reports, per market

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SafetySignalDetection

### Component2
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Label
signal referred to quality

### Description
A signal traced to a product or process fault becomes a corrective action, which is where the safety chain hands over to the quality system.

### Data Exchanged
signal, implicated product or process

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SafetySignalDetection

### Component2
CocoPharma::SolutionComponent::MarketAuthorisationRegister

### Label
label or authorisation change

### Description
A confirmed signal can change what may be sold and how it must be labelled, which reaches back into the product master chain.

### Data Exchanged
safety finding, affected authorisations

### ISC Qualified Names
- InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

### 3.3 Batch Manufacturing and Release

This section models the convergence the strategic register described: a batch cannot be certified unless the raw material data was verified, the equipment qualification was current and the operator was qualified, and those three facts arrive from three different chains with three different owners.  The wires below make each of those preconditions explicit rather than assumed.

The archive's **Automated Manufacturing Control** blueprint was empty.  These seven components and the seven in the next section fill it.

| Component | Role in this chain |
|---|---|
| **Manufacturing Execution System** | Directs and records the execution of each production step: what was done, by whom, with which materials and on which equipment. |
| **Process Historian** | Continuously captures process parameters from plant instrumentation. |
| **Laboratory Information Management System** | Manages sampling, testing and results for raw materials, in-process checks and finished product. |
| **Equipment Qualification Register** | Records the qualification and calibration status of every piece of equipment used in production. |
| **Electronic Batch Record System** | Assembles the complete record of a batch from every contributing system and holds it for the life of the obligation. |
| **Deviation and CAPA Management** | Records departures from the approved process, drives their investigation, and tracks the corrective and preventive actions that follow. |
| **Batch Review and QP Certification** | The review of the assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market. |
| **Goods Inventory** | Material issued to a batch is drawn from inventory, and the identity and status of what was issued becomes part of the batch record. |
| **Qualification and Competency Register** | Signature authority in the batch record is checked against the qualification register at the moment of signing. |
| **Product Master Register** | The product specification the batch is made to, and the markets it may be certified for, are read from the product master. |
| **Data Hub** | Manufacturing status is published to the hub for the rest of the business. |
| Personalised Order Scheduler *(handover)* | A personalised order opens a batch record, which is where the ordering chain becomes a manufacturing one. |
| Material Quarantine and Release Control *(handover)* | Material cannot enter a batch until quarantine has released it, so the gate is part of the release flow as well as the inventory flow. |
| Market Verification Gateway *(handover)* | Certification releases identifiers for upload, so the serialisation gateway is what the manufacturing chain hands over to. |
| Temperature Excursion Assessment *(handover)* | A transit excursion changes what may be done with product that has already been certified, so the assessment writes back into the batch record. |
| Safety Signal Detection *(handover)* | A safety signal referred to the quality system enters the manufacturing chain as a corrective action. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### ISC Child
SolutionComponent::Goods Inventory::V1.0

### Membership Rationale
Material issued to a batch is drawn from inventory, and the identity and status of what was issued becomes part of the batch record.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
SolutionComponent::Goods Inventory::V1.0

### Component2
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
issue material

### Description
Material can only be issued once quarantine has been released, so the inventory chain is a precondition of this one.

### Data Exchanged
material identity, lot, quantity, quarantine status

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Component2
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
in-process results

### Description
In-process results are gates rather than reports: the next step does not start until the laboratory has answered.

### Data Exchanged
sample results, specification comparison

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::EquipmentQualificationRegister

### Component2
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
qualification status

### Description
Status is read at the moment of use, because a qualification that lapsed last week invalidates production that has already happened.

### Data Exchanged
equipment identity, qualification and calibration validity

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
operator qualification

### Description
The evidence that the person performing and the person checking were qualified to do so arrives from the people chain and must be current at the moment of signature.

### Data Exchanged
worker pseudonym, qualifications, currency

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ManufacturingExecution

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
execution record

### Description
The record is assembled contemporaneously, because reconstruction afterwards is precisely what the data integrity obligations forbid.

### Data Exchanged
steps performed, materials used, equipment, signatures

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProcessHistorian

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
process parameters

### Description
The evidence that the process stayed within its validated range, at a resolution nobody reads unless something went wrong.

### Data Exchanged
time series of critical process parameters

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
finished product results

### Description
Release testing results complete the record and are the last input the certification decision waits on.

### Data Exchanged
release testing results, certificate of analysis

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ManufacturingExecution

### Component2
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Label
raise deviation

### Description
A deviation raised in production is a gate on certification, which is why it sits inside the release flow rather than beside it.

### Data Exchanged
departure from approved process, context

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
deviation disposition

### Description
The batch record carries the deviation and its closure, because an open deviation blocks the certification decision.

### Data Exchanged
investigation outcome, impact on batch

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductMasterRegister

### Component2
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
product and market requirements

### Description
Certification is market-specific, so the destination has to be known before the record is closed.

### Data Exchanged
specification, pack configuration, authorised markets

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Component2
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
batch record for review

### Description
The single human decision the whole chain exists to support.

### Data Exchanged
complete assembled batch record

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Component2
CocoPharma::SolutionComponent::DataHub

### Label
manufacturing-status

### Description
Release status is published to the hub so that warehouse, delivery and finance work from the same view.

### Data Exchanged
batch identity, certification decision, quantities

### ISC Qualified Names
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

### 3.4 Product Serialisation and Verification

Two properties shape these components.  Uniqueness is assured at generation rather than detected in reconciliation, because a number issued twice cannot be corrected once packs are distributed.  And the chain runs partly outside the company: the national verification systems are opaque, and they are also where the company's product data becomes publicly visible in real time, which is why the return flow carries alerts inward rather than merely confirmations.

| Component | Role in this chain |
|---|---|
| **Serial Number Generator** | Issues the unique identifiers applied to saleable packs. |
| **Packaging Line Controller** | Applies and verifies identifiers on the packaging line, and commissions each pack as a real, saleable object. |
| **Case and Pallet Aggregation Recorder** | Records which packs are in which case and which cases are on which pallet. |
| **Serialisation Repository** | The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned. |
| **Market Verification Gateway** | Routes identifier data to the national and regional verification system required by each destination market, and receives verification, decommissioning and alert traffic back. |
| **National Verification Systems** | The repositories operated outside Coco Pharmaceuticals that pharmacies check before dispensing. |
| **Serialisation Alert Triage** | Investigates verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals. |
| **Electronic Batch Record System** | Identifiers may only be uploaded once the batch is certified, so the batch record is the gate this chain waits on. |
| **Product Master Register** | Pack configuration and destination market are read from the product master and determine which scheme applies. |
| **Market Authorisation Register** | Which market a pack may be placed on determines which external system its identifiers must reach. |
| Goods Inventory *(handover)* | Serialised stock becomes physical inventory, and the two chains share a key from commissioning onwards. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### ISC Child
SolutionComponent::Goods Inventory::V1.0

### Membership Rationale
Serialised stock becomes physical inventory, and the two chains share a key from commissioning onwards.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductMasterRegister

### Component2
CocoPharma::SolutionComponent::SerialNumberGenerator

### Label
pack configuration

### Description
Destination determines the numbering scheme, so it has to be known before the identifiers exist.

### Data Exchanged
product code, pack presentation, destination market

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SerialNumberGenerator

### Component2
CocoPharma::SolutionComponent::PackagingLineController

### Label
issue identifiers

### Description
Identifiers are present and valid before the line starts, because the line runs faster than a request-response would allow.

### Data Exchanged
allocated serial numbers

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PackagingLineController

### Component2
CocoPharma::SolutionComponent::SerialisationRepository

### Label
commission packs

### Description
Commissioning turns a number into a real saleable object, and is recorded in the company's own record before anything external sees it.

### Data Exchanged
commissioned identifiers, batch and expiry

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PackagingLineController

### Component2
CocoPharma::SolutionComponent::AggregationRecorder

### Label
pack to case

### Description
The relationships recorded here are what allow a shipment to be verified without opening it.

### Data Exchanged
pack identifiers, case identity

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::AggregationRecorder

### Component2
CocoPharma::SolutionComponent::SerialisationRepository

### Label
aggregation hierarchy

### Description
Aggregation makes a recall a query rather than a search.

### Data Exchanged
pack, case and pallet relationships

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Component2
CocoPharma::SolutionComponent::MarketVerificationGateway

### Label
release authorisation

### Description
Upload is gated on certification, which is the handover point between the manufacturing chain and this one.

### Data Exchanged
batch certification, released quantities and markets

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SerialisationRepository

### Component2
CocoPharma::SolutionComponent::MarketVerificationGateway

### Label
identifiers for upload

### Description
The gateway routes to the scheme required by each destination, so one production run may leave through several routes.

### Data Exchanged
commissioned identifiers, aggregation, destination

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MarketVerificationGateway

### Component2
CocoPharma::SolutionComponent::NationalVerificationSystems

### Label
upload identifiers

### Description
Stock that has not reached the verification system cannot lawfully be sold, so an outage here halts distribution.

### Data Exchanged
identifier records per national scheme

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::NationalVerificationSystems

### Component2
CocoPharma::SolutionComponent::MarketVerificationGateway

### Label
verification and alerts

### Description
The return flow is how the company learns of a defect — frequently from a pharmacist rather than from its own monitoring.

### Data Exchanged
verification results, decommissioning events, alerts

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MarketVerificationGateway

### Component2
CocoPharma::SolutionComponent::SerialisationAlertTriage

### Label
raise alert

### Description
Alerts are separated into the company's own data errors and genuine falsification signals; one that is not investigated is a signal received and ignored.

### Data Exchanged
alert, identifier, reporting party

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SerialisationAlertTriage

### Component2
CocoPharma::SolutionComponent::SerialisationRepository

### Label
alert disposition

### Description
Disposition is written back so that repeat alerts on the same cause are visible as a pattern rather than as separate incidents.

### Data Exchanged
root cause, corrective action, affected identifiers

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SerialisationRepository

### Component2
SolutionComponent::Goods Inventory::V1.0

### Label
serialised stock

### Description
Once commissioned and aggregated, packs are tracked as physical inventory by their identifiers, so the two chains share a key from here on.

### Data Exchanged
identifiers, aggregation, location

### ISC Qualified Names
- InformationSupplyChain::Product Serialisation and Verification Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

### 3.5 Cold Chain and Dangerous Goods Consignment

The two obligations meet in the same consignment, so the components are shared: one classification service answers both the transport question and, through the exposure banding register, the occupational one.  The monitoring devices are themselves dangerous goods because they contain lithium batteries, which is the small irony at the centre of this chain and the reason the classification service is consulted about the packaging as well as the contents.

These components complete the archive's **Hazardous Material Management** blueprint, which previously held only the HazMat inventory.

| Component | Role in this chain |
|---|---|
| **Transport Classification Service** | Derives the transport classification of a consignment from the substance and biological agent registers and the form the material is being shipped in. |
| **Shipping Documentation Preparation** | The preparation and signature of the dangerous goods declaration and accompanying documents by a certificated person. |
| **Temperature Monitoring Devices** | The loggers and live monitors travelling inside consignments. |
| **Cold Chain Data Collector** | Collects the temperature record from devices and carrier systems on arrival, and reconciles it against the permitted range for the product being shipped. |
| **Temperature Excursion Assessment** | Assesses a temperature excursion against the product's stability data and dispositions the consignment. |
| **Carrier Systems** | The tracking and handling systems of the couriers and freight forwarders that physically move the goods. |
| **Hazardous Materials (HazMat) Inventory** | Transport classification is derived from the substance register, so a substance reclassified for safety reasons changes how it may be shipped. |
| **Patient Sample Logistics** | Inbound patient material is a consignment under the same rules as outbound product, moving under tighter time pressure. |
| **Qualification and Competency Register** | The declaration must be signed by a certificated person, and an expired certificate makes every subsequent consignment non-compliant. |
| Product Master Register *(handover)* | Storage range, packaging and hazard properties are read from the product master before a consignment is built. |
| Electronic Batch Record System *(handover)* | An excursion disposition belongs with the batch record, because it changes what may be done with certified product. |
| Exposure Banding Register *(handover)* | One substance classification answers both the occupational and the transport question. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### ISC Child
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Membership Rationale
Transport classification is derived from the substance register, so a substance reclassified for safety reasons changes how it may be shipped.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Component2
CocoPharma::SolutionComponent::TransportClassificationService

### Label
substance identity

### Description
Classification is derived rather than declared, so that despatch, procurement and the signatory all get the same answer.

### Data Exchanged
substance, hazard classification, form and quantity

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductMasterRegister

### Component2
CocoPharma::SolutionComponent::TransportClassificationService

### Label
product handling requirements

### Description
The product master supplies what the product needs; the classification service decides what the transport rules require.

### Data Exchanged
storage range, packaging, hazard properties

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TransportClassificationService

### Component2
CocoPharma::SolutionComponent::ShippingDocumentation

### Label
classification and requirements

### Description
The classification is what the certificated person signs against, which is why it is produced before the consignment is built rather than at the airport.

### Data Exchanged
UN number, packing group, labelling, documentation set

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
CocoPharma::SolutionComponent::ShippingDocumentation

### Label
certificated signatory

### Description
Certification expires, and the expiry is checked at signature rather than at audit.

### Data Exchanged
worker pseudonym, certificate and expiry

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ShippingDocumentation

### Component2
CocoPharma::SolutionComponent::CarrierSystems

### Label
consign

### Description
The shipper's liability stays with the company however the carrier behaves afterwards, so the correctness of what is handed over is the company's exposure.

### Data Exchanged
declaration, documentation, handling instructions

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TemperatureMonitoringDevices

### Component2
CocoPharma::SolutionComponent::ColdChainDataCollector

### Label
transit temperature record

### Description
A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.

### Data Exchanged
time series of in-transit temperature and location

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CarrierSystems

### Component2
CocoPharma::SolutionComponent::ColdChainDataCollector

### Label
transit status

### Description
Status is read from the carrier, which is the only visibility the company has of what happened between despatch and receipt.

### Data Exchanged
handover events, delays, delivery confirmation

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ColdChainDataCollector

### Component2
CocoPharma::SolutionComponent::ExcursionAssessment

### Label
excursion detected

### Description
Assessment runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

### Data Exchanged
excursion profile, duration, product and batch

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ExcursionAssessment

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
disposition recorded

### Description
The disposition belongs with the batch record, because it changes what may be done with product that has already been certified.

### Data Exchanged
excursion assessment, disposition decision

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SampleLogistics

### Component2
CocoPharma::SolutionComponent::ColdChainDataCollector

### Label
inbound material record

### Description
Patient material arrives under the same monitoring as product leaves, on a much shorter clock.

### Data Exchanged
consignment identity, in-transit condition

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ShippingDocumentation

### Component2
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Label
consignment record

### Description
Consignment records are retained and retrievable long after the shipment has been delivered.

### Data Exchanged
declaration, classification, quantities shipped

### ISC Qualified Names
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

### 3.6 Physical Inventory Tracking

The archive's **Inventory Management** blueprint held only the goods inventory itself.  The three components added here are the ones that make the inventory record trustworthy rather than merely current: the certificates that arrive with the material, the receipt that turns a supplier's claim into the company's record, and the quarantine gate that keeps unverified material out of a batch.

The quarantine control is deliberately a system-enforced gate rather than a procedure, because the failure it prevents is discovered in a finished batch.

| Component | Role in this chain |
|---|---|
| **Supplier Material Certificates** | Holds the certificates of analysis and conformity supplied with incoming material. |
| **Goods Receipt and Inspection** | Receives physical material, checks it against the order and the accompanying documentation, and records what actually arrived. |
| **Material Quarantine and Release Control** | Holds received material in quarantine until testing and documentation review are complete, and releases it for use only then. |
| **Goods Inventory** | The inventory record itself, tracking material from receipt through storage to issue. |
| **Hazardous Materials (HazMat) Inventory** | Hazardous material identity carried by the inventory is what transport classification and emergency response are both derived from. |
| **Supplier Master Register** | Material may only be received from a supplier that has been screened and approved, so the supplier record is a precondition of receipt. |
| **Laboratory Information Management System** | Incoming material testing is what releases it from quarantine. |
| **Data Hub** | Inventory levels are published to the hub so that procurement and manufacturing plan from the same numbers. |
| Manufacturing Execution System *(handover)* | Material issued to a batch leaves the inventory chain at the point of issue. |
| Serialisation Repository *(handover)* | Once commissioned and aggregated, packs are tracked as inventory by their identifiers. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### ISC Child
SolutionComponent::Goods Inventory::V1.0

### Membership Rationale
The inventory record itself, tracking material from receipt through storage to issue.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### ISC Child
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Membership Rationale
Hazardous material identity carried by the inventory is what transport classification and emergency response are both derived from.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierMasterRegister

### Component2
CocoPharma::SolutionComponent::GoodsReceiptAndInspection

### Label
approved supplier

### Description
Receipt from an unapproved supplier is refused here rather than discovered later, which is what makes the onboarding chain worth having.

### Data Exchanged
supplier identity, approval and risk status

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierMaterialCertificates

### Component2
CocoPharma::SolutionComponent::GoodsReceiptAndInspection

### Label
certificate of analysis

### Description
The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

### Data Exchanged
supplier test results, conformity declaration

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::GoodsReceiptAndInspection

### Component2
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Label
place in quarantine

### Description
Material is held rather than made available, so the default state of anything new is unusable.

### Data Exchanged
received lot, quantity, storage location

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Component2
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Label
request incoming testing

### Description
Testing is requested by the quarantine gate, which means it cannot be skipped by whoever wants the material.

### Data Exchanged
lot identity, required tests

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Component2
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Label
test results

### Description
Results release or reject the lot; there is no third state that allows use while waiting.

### Data Exchanged
results, specification comparison, disposition

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MaterialQuarantineControl

### Component2
SolutionComponent::Goods Inventory::V1.0

### Label
release for use

### Description
Only released material appears as available inventory, so the verification travels with the material rather than being looked up later.

### Data Exchanged
released lot, quantity, expiry

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Goods Inventory::V1.0

### Component2
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Label
hazardous holdings

### Description
What is held, where and in what quantity is drawn from the inventory record, and the hazardous substance register is fiction if the flow does not reflect physical reality.

### Data Exchanged
substance, quantity, location

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Goods Inventory::V1.0

### Component2
CocoPharma::SolutionComponent::DataHub

### Label
inventory

### Description
Inventory levels are published to the hub for procurement and manufacturing planning.

### Data Exchanged
stock levels, locations, movements

### ISC Qualified Names
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

### 3.7 New Drug Product Details

This is a master data chain rather than a transactional one, and its components reflect that.  The product master is authoritative, the market authorisation register says where each product may go, and the distribution component publishes changes and — the part that matters — records which systems have applied them.

Knowing who has *not* yet applied a change is the useful half.  An inconsistent estate is only dangerous while nobody knows which systems are stale.

| Component | Role in this chain |
|---|---|
| **Product Master Register** | The authoritative definition of every product: its identity, presentations, pack configurations, composition and handling requirements. |
| **Market Authorisation Register** | Records which product may be placed on which market, under which authorisation and subject to which conditions. |
| **Product Data Distribution** | Publishes changes to the product master to every system that holds a copy, and records which of them have applied it. |
| **Research Systems** | New product definitions originate in research, from the evidence the clinical trials chain assembled. |
| **Data Hub** | The hub is how the product definition reaches the systems that hold copies of it. |
| **Egeria Open Metadata and Governance** | The catalogue records which systems receive the product definition, because a system nobody knows receives it is a system nobody updates. |
| Batch Review and QP Certification *(handover)* | Certification reads the authorised markets from the product master, which is what makes it market-specific. |
| Serial Number Generator *(handover)* | Pack configuration and destination market determine the numbering scheme, so serialisation reads the product master before identifiers exist. |
| Transport Classification Service *(handover)* | Product handling requirements are read from the product master and combined with substance data to classify a consignment. |
| Safety Signal Detection *(handover)* | A confirmed safety signal changes labelling or authorisation, which reaches back into the product master. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::New Drug Product Details Information Supply Chain

### ISC Child
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Membership Rationale
The catalogue records which systems receive the product definition, because a system nobody knows receives it is a system nobody updates.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::Research

### Component2
CocoPharma::SolutionComponent::ProductMasterRegister

### Label
new product definition

### Description
The evidence assembled by the trials chain becomes the authorisation the product definition is built on.

### Data Exchanged
composition, presentations, specification

### ISC Qualified Names
- InformationSupplyChain::New Drug Product Details Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MarketAuthorisationRegister

### Component2
CocoPharma::SolutionComponent::ProductMasterRegister

### Label
authorised markets

### Description
Which markets a product may enter is part of its definition, because two other chains read it as an instruction.

### Data Exchanged
authorisation, conditions, labelling requirements

### ISC Qualified Names
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductMasterRegister

### Component2
CocoPharma::SolutionComponent::ProductDataDistribution

### Label
publish change

### Description
Changes are published rather than made available, so that the estate converges on a known date.

### Data Exchanged
changed product attributes, effective date

### ISC Qualified Names
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductDataDistribution

### Component2
CocoPharma::SolutionComponent::DataHub

### Label
product master feed

### Description
The hub is the route to systems that hold copies.

### Data Exchanged
current product definitions

### ISC Qualified Names
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ProductDataDistribution

### Component2
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Label
record distribution

### Description
Which systems have not yet applied a change is the half of the answer that matters.

### Data Exchanged
recipients, applied and outstanding changes

### ISC Qualified Names
- InformationSupplyChain::New Drug Product Details Information Supply Chain

___

---

### 3.8 Financial Close and External Reporting

The chain has to be traversable in both directions.  Forwards it consolidates transactions into published figures; backwards, any published figure must resolve to the transactions it was built from, on demand and without an investigation.  That second requirement is what puts the subledger feeds in as a component in their own right rather than as plumbing — each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period.

There is no archive blueprint covering financial control, so these components are registered against their information supply chains only.

| Component | Role in this chain |
|---|---|
| **Subledger Feeds** | The scheduled and event-driven flows that carry transactions from the operational systems into the ledger. |
| **Journal Entry Review** | The review and approval of manual journal entries above a materiality threshold. |
| **Group Consolidation Engine** | Consolidates the ledgers of the US parent and the UK and EU subsidiaries, eliminating intercompany balances and translating currency. |
| **Disclosure and Statutory Reporting** | Produces the statements filed with regulators and published to the market. |
| **Controls Evidence Repository** | Holds the documentation and test evidence for the internal controls over financial reporting. |
| **Accounting ledgers** | The general ledger of each group entity, and the point every subledger feed arrives at. |
| **Employee Expense Tool** | Approved expenses post to the ledger through the same feed mechanism as every other subledger. |
| **Supplier Payment Processing** | Payments to third parties post to the ledger, so a fraudulent payment is also a misstatement. |
| **Order to Invoice Processing** | Invoiced treatment revenue is the operating income the published figures are mostly made of. |
| Payroll System *(handover)* | Payroll is one of the larger subledger feeds and one of the few running under several national rule sets at once. |
| Transfers of Value Register *(handover)* | Disclosure is produced from the register rather than reconstructed from the ledger, so the register is part of the reporting chain. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### ISC Child
SolutionComponent::Accounting ledgers::V1.0

### Membership Rationale
The general ledger of each group entity, and the point every subledger feed arrives at.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### ISC Child
SolutionComponent::Employee Expense Tool::V1.0

### Membership Rationale
Approved expenses post to the ledger through the same feed mechanism as every other subledger.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SubledgerFeeds

### Component2
SolutionComponent::Accounting ledgers::V1.0

### Label
post transactions

### Description
Completeness is asserted per feed rather than in aggregate, because a dropped feed is invisible in a total.

### Data Exchanged
transaction batches per source and period

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Employee Expense Tool::V1.0

### Component2
CocoPharma::SolutionComponent::SubledgerFeeds

### Label
expense postings

### Description
Approved expenses enter the ledger through the same mechanism as every other subledger.

### Data Exchanged
approved expense claims, cost coding

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Component2
CocoPharma::SolutionComponent::SubledgerFeeds

### Label
payment postings

### Description
Third party payments post to the ledger and are consolidated into the published figures.

### Data Exchanged
authorised payments, supplier, cost coding

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::OrderToInvoice

### Component2
CocoPharma::SolutionComponent::SubledgerFeeds

### Label
revenue postings

### Description
Treatment revenue enters the ledger from the fulfilment record rather than being agreed with it afterwards.

### Data Exchanged
invoices, revenue recognition data

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PayrollSystem

### Component2
CocoPharma::SolutionComponent::SubledgerFeeds

### Label
payroll postings

### Description
Payroll is one of the larger subledger feeds and one of the few that runs under several national rule sets at once.

### Data Exchanged
remuneration, employer costs, by entity

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Accounting ledgers::V1.0

### Component2
CocoPharma::SolutionComponent::JournalEntryReview

### Label
material entries for review

### Description
Manual adjustment is the segment least covered by system controls and most able to change a reported figure.

### Data Exchanged
manual journal entries above threshold

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::JournalEntryReview

### Component2
SolutionComponent::Accounting ledgers::V1.0

### Label
approved adjustments

### Description
The review is recorded against the entry, so that the evidence and the adjustment cannot become separated.

### Data Exchanged
reviewed and approved journal entries

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Accounting ledgers::V1.0

### Component2
CocoPharma::SolutionComponent::GroupConsolidation

### Label
entity ledgers

### Description
Several sets of books become one set of figures here, and the group structure becomes an accounting fact.

### Data Exchanged
trial balances by entity and currency

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::GroupConsolidation

### Component2
CocoPharma::SolutionComponent::DisclosureReporting

### Label
consolidated results

### Description
The published figures, each of which must resolve back through this component to its source transactions.

### Data Exchanged
consolidated statements, segment analysis

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::GroupConsolidation

### Component2
CocoPharma::SolutionComponent::ControlsEvidenceRepository

### Label
close evidence

### Description
The controls the company certifies as effective are controls over this flow, so testing them means testing the flow.

### Data Exchanged
reconciliations, approvals, close checklist

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TransfersOfValueRegister

### Component2
CocoPharma::SolutionComponent::DisclosureReporting

### Label
transfers of value

### Description
Disclosure is produced from a register populated as payments are made, not reconstructed from a general ledger afterwards.

### Data Exchanged
payments and benefits to healthcare professionals

### ISC Qualified Names
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

### 3.9 Third Party Onboarding and Payment

This is the flow the supplier fraud travelled, and the components are laid out to make the two failures it exploited impossible to repeat.  The onboarding workflow is deliberately the only route to a supplier record, so a supplier created outside it does not exist.  And payment detail changes are modelled as a controlled event with independent verification rather than as routine maintenance, because that is where the flow was actually attacked.

Screening answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

| Component | Role in this chain |
|---|---|
| **Third Party Onboarding Workflow** | Drives a proposed third party through screening, risk assessment and approval to the creation of a supplier record. |
| **Sanctions and Screening Service** | The external service that screens third parties against sanctions, politically exposed person and adverse media lists. |
| **Supplier Master Register** | The authoritative record of every third party the company transacts with, including its screening status, risk rating and payment details. |
| **Payment Detail Change Control** | Governs changes to a supplier's bank details as a controlled event with independent verification, rather than as routine maintenance. |
| **Supplier Payment Processing** | Matches invoices to orders and receipts, authorises payment, and instructs the bank. |
| **Transaction Monitoring** | Looks across payments for the patterns that reveal fraud, duplicate payment and unusual supplier behaviour. |
| **Transfers of Value Register** | Identifies and records payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, so that they can be disclosed. |
| **Accounting ledgers** | Authorised payments post to the ledger, which is where a fraudulent payment also becomes a misstatement. |
| **Procurement Systems** | Requirements and orders originate in procurement and are matched against invoices before payment. |
| **Supplier Material Certificates** | Material documentation is held against the supplier record, so quality and commercial views of a supplier agree. |
| Goods Receipt and Inspection *(handover)* | Receipt refuses material from an unapproved supplier, which is where the onboarding chain is actually enforced. |
| Subledger Feeds *(handover)* | Authorised payments reach the ledger through the subledger feeds. |
| Disclosure and Statutory Reporting *(handover)* | Transfers of value recorded in this chain are published through statutory disclosure. |
| Employee Expense Tool *(handover)* | Hospitality and travel provided to healthcare professionals frequently arrives as an employee expense rather than a supplier invoice. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### ISC Child
SolutionComponent::Accounting ledgers::V1.0

### Membership Rationale
Authorised payments post to the ledger, which is where a fraudulent payment also becomes a misstatement.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### ISC Child
SolutionComponent::Employee Expense Tool::V1.0

### Membership Rationale
Hospitality and travel provided to healthcare professionals frequently arrives as an employee expense rather than a supplier invoice.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow

### Component2
CocoPharma::SolutionComponent::SanctionsAndScreeningService

### Label
screen third party

### Description
Screening is performed against external lists whose answers age, so the result is dated rather than final.

### Data Exchanged
legal entity, ownership, jurisdictions

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SanctionsAndScreeningService

### Component2
CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow

### Label
screening result

### Description
The result and its date travel onward together, because a screening result without a date protects nothing.

### Data Exchanged
matches, risk indicators, screening date

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow

### Component2
CocoPharma::SolutionComponent::SupplierMasterRegister

### Label
create supplier record

### Description
This is deliberately the only route to a supplier record: one created outside this flow is one nothing has checked.

### Data Exchanged
approved supplier, risk rating, screening evidence

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PaymentDetailChangeControl

### Component2
CocoPharma::SolutionComponent::SupplierMasterRegister

### Label
verified bank details

### Description
Payment detail changes are a controlled event rather than maintenance, because this is where the flow has historically been attacked.

### Data Exchanged
changed payment details, independent verification evidence

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierMasterRegister

### Component2
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Label
supplier and payment details

### Description
The screening status is read at the moment of authorisation, which is the only moment at which it protects anything.

### Data Exchanged
screening status, risk rating, bank details

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::Procurement

### Component2
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Label
order and receipt

### Description
Invoices are matched to orders and receipts, so a payment with no corresponding delivery is visible before it is made.

### Data Exchanged
purchase order, goods receipt confirmation

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Component2
SolutionComponent::Accounting ledgers::V1.0

### Label
payment instruction

### Description
Payment posts to the ledger, and a payment made in error is rarely recovered.

### Data Exchanged
authorised payment, supplier, amount, coding

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain
- InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Component2
CocoPharma::SolutionComponent::TransactionMonitoring

### Label
payment stream

### Description
The pattern that revealed the original fraud was visible across the whole flow and in no single transaction within it.

### Data Exchanged
payments, suppliers, timing and amounts

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::TransactionMonitoring

### Component2
CocoPharma::SolutionComponent::SupplierMasterRegister

### Label
raise supplier concern

### Description
A concern raised by monitoring is attached to the supplier record, so the next payment authorisation sees it.

### Data Exchanged
anomaly, supplier, evidence

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierPaymentProcessing

### Component2
CocoPharma::SolutionComponent::TransfersOfValueRegister

### Label
identify disclosable payment

### Description
Payments to healthcare professionals are identified as such within the payment flow, so the disclosure is populated rather than reconstructed.

### Data Exchanged
payee, benefit, purpose, value

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::SupplierMasterRegister

### Component2
CocoPharma::SolutionComponent::SupplierMaterialCertificates

### Label
supplier documentation

### Description
Quality and commercial views of a supplier are held against the same record.

### Data Exchanged
approved supplier, quality documentation

### ISC Qualified Names
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain
- InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

___

---

### 3.10 Employee Expense Payment

The archive already had the expense tool itself, sitting in both the **Employee Management** and **Sustainability Reporting** blueprints — travel expenses being one of the better proxies for corporate emissions.  What was missing was the approval step, which is the whole point of the chain: approval and payment sit in different systems, and the approval is only worth anything if it is still attached to the claim when the payment is made.

That is the same structural weakness the supplier fraud exploited, on a smaller scale, which is why this chain shares its monitoring and its transfers of value register with the third party chain.

| Component | Role in this chain |
|---|---|
| **Expense Approval Workflow** | Routes an expense claim for approval and carries the approval forward to payment. |
| **Employee Expense Tool** | Recording and categorisation of employee expenses, and the request for repayment. |
| **Accounting ledgers** | Approved expenses post to the ledger and are consolidated into the published figures. |
| **Transaction Monitoring** | The same monitoring applied to supplier payments applies here, for the same structural reason. |
| **Transfers of Value Register** | Hospitality and travel provided to healthcare professionals frequently arrives as an employee expense. |
| **Worker Master Register** | Claims are held against the worker record, and a leaver with an open claim is a case the chain has to handle. |
| Subledger Feeds *(handover)* | Approved expenses reach the ledger through the same feed mechanism as every other subledger. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### ISC Child
SolutionComponent::Employee Expense Tool::V1.0

### Membership Rationale
Recording and categorisation of employee expenses, and the request for repayment.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### ISC Child
SolutionComponent::Accounting ledgers::V1.0

### Membership Rationale
Approved expenses post to the ledger and are consolidated into the published figures.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
SolutionComponent::Employee Expense Tool::V1.0

### Component2
CocoPharma::SolutionComponent::ExpenseApprovalWorkflow

### Label
submit for approval

### Description
The claim leaves the recording system to be approved elsewhere, which is the gap the chain has to close.

### Data Exchanged
claim, cost coding, supporting evidence

### ISC Qualified Names
- InformationSupplyChain::Employee Expense Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::ExpenseApprovalWorkflow

### Label
approver and cost centre

### Description
Who may approve is derived from the worker record rather than configured separately, so it changes when the person moves.

### Data Exchanged
worker, reporting line, spending authority

### ISC Qualified Names
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ExpenseApprovalWorkflow

### Component2
SolutionComponent::Employee Expense Tool::V1.0

### Label
approval decision

### Description
The approval is written back onto the claim, so the two travel together to payment.

### Data Exchanged
approval, approver identity, timestamp

### ISC Qualified Names
- InformationSupplyChain::Employee Expense Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Employee Expense Tool::V1.0

### Component2
CocoPharma::SolutionComponent::TransfersOfValueRegister

### Label
identify disclosable expense

### Description
Hospitality provided to a healthcare professional is identified where it is claimed, not where it is paid.

### Data Exchanged
payee, benefit, purpose, value

### ISC Qualified Names
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Employee Expense Tool::V1.0

### Component2
CocoPharma::SolutionComponent::TransactionMonitoring

### Label
expense stream

### Description
Patterns in expense claims are examined on the same basis as patterns in supplier payments.

### Data Exchanged
claims, claimants, categories and amounts

### ISC Qualified Names
- InformationSupplyChain::Employee Expense Payment Information Supply Chain
- InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

___

---

### 3.11 New Employee Onboarding

The archive's **Employee Management** blueprint contained one component, the expense tool, which is a fair description of how much of the employee lifecycle had been modelled.  The five components here and the four in the next section complete it.

The chain is modelled around the leaver case rather than the joiner case.  Joining is forgiving — a missing account is reported within the hour by the person who does not have it.  Leaving is not: access outlives employment by exactly this chain's delay, and nobody is inconvenienced by the delay except the company.

| Component | Role in this chain |
|---|---|
| **Worker Master Register** | The authoritative record of every worker — employees and contractors alike — and the anchor that qualification, health surveillance, access and payroll records are all held against. |
| **Joiner Mover Leaver Workflow** | Distributes a joining, moving or leaving event to every system that must act on it, and records which of them have. |
| **Identity and Access Provisioning** | Creates, changes and removes accounts and entitlements in response to worker events. |
| **Payroll System** | Calculates and pays remuneration, and produces the pay data that statutory reporting and pay equity analysis are built from. |
| **Corporate Directory** | The searchable directory of people, roles and reporting lines that the rest of the organisation uses. |
| **Employee Expense Tool** | A new worker needs expense access, and a leaver needs it removed with any open claim resolved. |
| **Qualification and Competency Register** | Qualification records are held against the worker record created here. |
| **Egeria Open Metadata and Governance** | Access decisions and data ownership are recorded in the catalogue, which is how a departed owner becomes visible as a gap. |
| Learning Management System *(handover)* | Training requirements follow from the role a person is appointed to, so a joiner or mover event generates them. |
| Expense Approval Workflow *(handover)* | Spending authority is derived from the worker record, so it changes when the person moves. |
| Health Surveillance Records *(handover)* | Enrolment in health surveillance follows from the role, and the record outlives the employment. |
| Exposure Monitoring Capture *(handover)* | Who needs exposure monitoring follows from what a person does, so the monitoring population changes with the worker record. |
| Record of Processing Activities Register *(handover)* | Onboarding is where employee personal data enters the estate, and the register is what records where it went. |
| Rights Fulfilment Orchestrator *(handover)* | Employee data is one of the two largest holdings a rights request has to reach, anchored on the worker record. |
| Subledger Feeds *(handover)* | Payroll postings reach the ledger through the subledger feeds. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### ISC Child
SolutionComponent::Employee Expense Tool::V1.0

### Membership Rationale
A new worker needs expense access, and a leaver needs it removed with any open claim resolved.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### ISC Child
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Membership Rationale
Access decisions and data ownership are recorded in the catalogue, which is how a departed owner becomes visible as a gap.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::JoinerMoverLeaverWorkflow

### Component2
CocoPharma::SolutionComponent::WorkerMasterRegister

### Label
worker event

### Description
The worker record is the anchor everything else is held against, so the event lands here first.

### Data Exchanged
joiner, mover or leaver event, effective date

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::IdentityAndAccessProvisioning

### Label
provision or revoke

### Description
Provisioning is driven from the worker record rather than from requests, because an access removal that depends on somebody asking does not happen.

### Data Exchanged
worker identity, role, effective date

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::PayrollSystem

### Label
payroll record

### Description
Payroll runs in several countries under several rule sets from one worker record.

### Data Exchanged
worker, entity, contract terms

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::CorporateDirectory

### Label
directory entry

### Description
The directory is downstream of the worker record and is frequently where a stale joiner or leaver event first becomes visible to everybody.

### Data Exchanged
name, role, location, reporting line

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
SolutionComponent::Employee Expense Tool::V1.0

### Label
expense access

### Description
Expense access is granted and removed on the same event as everything else.

### Data Exchanged
worker, cost centre, spending authority

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Employee Expense Payment Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::CompetencyRegister

### Label
new worker record

### Description
Qualification and training records are held against the record created here, so a delay in onboarding delays every qualification that follows it.

### Data Exchanged
worker identity, role, start date

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Label
surveillance enrolment

### Description
Enrolment in health surveillance follows from the role a person is appointed to.

### Data Exchanged
worker, role, exposure profile

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::IdentityAndAccessProvisioning

### Component2
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Label
access and ownership

### Description
Recording ownership in the catalogue is what makes a departed owner visible as a gap rather than as silence.

### Data Exchanged
accounts, entitlements, data ownership assignments

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::JoinerMoverLeaverWorkflow

### Component2
CocoPharma::SolutionComponent::RecordOfProcessingRegister

### Label
employee personal data

### Description
Onboarding distributes employee personal data to every system and directory, and the rights chain has to be able to follow it to each of them.

### Data Exchanged
processing purposes, systems holding worker data

### ISC Qualified Names
- InformationSupplyChain::New Employee Onboarding Information Supply Chain
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

### 3.12 Workforce Competency and Qualification

Currency is the property this chain is judged on, which is why it has a daemon in it.  A qualification record that is correct but stale is indistinguishable from a wrong one at the point where a batch is signed or a trial is inspected, and both of those points are consumers that human resources did not originally build these systems for.

The framework register is separated from the records themselves because it changes for a different reason: it moves when a process or a regulation changes, not when a person does.

| Component | Role in this chain |
|---|---|
| **Competency Framework Register** | Defines what competencies each regulated role requires. |
| **Learning Management System** | Delivers training, records completion and assessment, and schedules refreshers. |
| **Qualification and Competency Register** | The authoritative statement of what each worker is currently qualified to do. |
| **Qualification Currency Checker** | Watches for qualifications approaching or past expiry and warns the processes that depend on them before rather than after. |
| **Worker Master Register** | Qualification records are held against the worker record. |
| **Electronic Batch Record System** | Signature authority in the batch record is checked against the qualification register at the moment of signing. |
| **Certify Hospital** | Certifying a hospital for a clinical trial includes evidence that its staff were trained on the protocol before they worked to it. |
| **Shipping Documentation Preparation** | Dangerous goods declarations must be signed by a person whose certificate has not expired. |
| Manufacturing Execution System *(handover)* | Signature authority in production is checked against the qualification register at the moment of use. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### ISC Child
SolutionComponent::Certify Hospital::V1.0

### Membership Rationale
Certifying a hospital for a clinical trial includes evidence that its staff were trained on the protocol before they worked to it.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyFrameworkRegister

### Component2
CocoPharma::SolutionComponent::LearningManagement

### Label
required competencies

### Description
The framework is the specification the chain is judged against, and it moves when a process or regulation changes.

### Data Exchanged
role, required competencies, refresh interval

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::LearningManagement

### Label
worker and role

### Description
Training requirements follow from the role, so a mover generates a new set without anybody requesting one.

### Data Exchanged
worker identity, role, start date

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::LearningManagement

### Component2
CocoPharma::SolutionComponent::CompetencyRegister

### Label
completion and assessment

### Description
The record of what a person is currently qualified to do, assembled from what they have actually completed.

### Data Exchanged
training completed, assessment results, dates

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
CocoPharma::SolutionComponent::QualificationCurrencyChecker

### Label
qualification status

### Description
Expiry is watched rather than discovered, because the consumers of this data act on it at a moment they cannot defer.

### Data Exchanged
qualifications, expiry dates

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::QualificationCurrencyChecker

### Component2
CocoPharma::SolutionComponent::LearningManagement

### Label
refresher required

### Description
A lapse is prevented by scheduling rather than reported after it has invalidated something.

### Data Exchanged
worker, lapsing qualification, deadline

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
signature authority

### Description
The batch record's signatures are only meaningful with this evidence behind them, and it must be current at the moment of signing.

### Data Exchanged
worker pseudonym, qualifications, currency at time of signature

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
SolutionComponent::Certify Hospital::V1.0

### Label
site staff training evidence

### Description
Trial master file completeness depends on evidence that site staff were trained on the protocol before they worked to it.

### Data Exchanged
site staff, protocol training, dates

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::CompetencyRegister

### Component2
CocoPharma::SolutionComponent::ShippingDocumentation

### Label
certificated signatory

### Description
An expired certificate makes every subsequent consignment non-compliant however correctly it was handled.

### Data Exchanged
certificate, scope, expiry

### ISC Qualified Names
- InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

### 3.13 Occupational Health Surveillance

Every other control in the plant protects the product from the people; this chain protects the people from the product, and the record it produces belongs to the worker rather than to the company.  That inverts the usual access question, and it is why the health records are held separately from everything else the people systems hold.

The archive component reused here is the HazMat inventory, and reusing it is the point: the same substance register drives exposure banding, transport classification and emergency response.  Three chains reading one register is a great deal safer than three registers agreeing most of the time.

| Component | Role in this chain |
|---|---|
| **Exposure Banding Register** | Assigns each substance to an occupational exposure band and each band to a required containment level. |
| **Exposure Monitoring Capture** | Captures personal and static exposure measurements from monitoring campaigns and compares them to the banded limits. |
| **Health Surveillance Records** | Holds the results of health surveillance appointments against the individual worker. |
| **Incident and Near Miss Reporting** | Records incidents, near misses and their investigations, and feeds what they reveal back into the assessments. |
| **Long Term Health Record Archive** | Retains health surveillance and exposure records for forty years from the last entry, across every system migration in that period. |
| **Hazardous Materials (HazMat) Inventory** | The substance register that exposure banding, transport classification and emergency response are all derived from. |
| **Worker Master Register** | Surveillance and exposure records are held against the worker record, and outlive the employment it describes. |
| **Transport Classification Service** | The same substance identity that drives exposure banding drives transport classification. |
| Goods Inventory *(handover)* | What hazardous material is held, where and in what quantity is drawn from the inventory record. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### ISC Child
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Membership Rationale
The substance register that exposure banding, transport classification and emergency response are all derived from.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### ISC Child
SolutionComponent::Goods Inventory::V1.0

### Membership Rationale
What hazardous material is held, where and in what quantity is drawn from the inventory record.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0

### Component2
CocoPharma::SolutionComponent::ExposureBandingRegister

### Label
substance holdings

### Description
Banding is derived from what is actually held, which is why the register being fiction would make the banding fiction too.

### Data Exchanged
substance, hazard data, quantities and locations

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ExposureBandingRegister

### Component2
CocoPharma::SolutionComponent::ExposureMonitoringCapture

### Label
banded limits

### Description
The limits are what measurements are judged against, and they change when a substance is reclassified rather than when monitoring is next scheduled.

### Data Exchanged
band, exposure limit, required containment

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::WorkerMasterRegister

### Component2
CocoPharma::SolutionComponent::ExposureMonitoringCapture

### Label
worker and task exposure

### Description
Who needs monitoring follows from what they do, so a mover changes the monitoring population without anybody requesting it.

### Data Exchanged
worker, role, tasks and locations

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ExposureMonitoringCapture

### Component2
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Label
exposure results

### Description
An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

### Data Exchanged
personal and static measurements, comparison to limits

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::IncidentAndNearMissReporting

### Component2
CocoPharma::SolutionComponent::ExposureBandingRegister

### Label
assessment feedback

### Description
Incidents and near misses feed back into the assessments, which is what makes the chain a loop rather than a line.

### Data Exchanged
incident, implicated substance or control, findings

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::IncidentAndNearMissReporting

### Component2
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Label
exposure incident

### Description
An acute exposure enters the individual record as well as the assessment.

### Data Exchanged
affected worker, exposure event, immediate response

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::HealthSurveillanceRecords

### Component2
CocoPharma::SolutionComponent::LongTermHealthArchive

### Label
archive record

### Description
Forty years from the last entry, across every system migration in between. The requirement is interpretability, not storage.

### Data Exchanged
surveillance results, exposure history, worker identity

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ExposureBandingRegister

### Component2
CocoPharma::SolutionComponent::TransportClassificationService

### Label
shared substance classification

### Description
One classification answers both the occupational and the transport question, rather than two registers agreeing most of the time.

### Data Exchanged
substance, hazard classification

### ISC Qualified Names
- InformationSupplyChain::Occupational Health Surveillance Information Supply Chain
- InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

___

---

### 3.14 Data Subject Rights

This chain is the practical test of every other entry in the register.  A subject access request is hard exactly to the extent that the company cannot say where personal data travels, so the components here mostly read from things the other chains produced: the record of processing, the catalogue, the worker record, the patient identity register.

Two of them exist because a register describes what the company *believes* it processes.  Personal data discovery describes what it actually holds, and the difference between the two is the thing worth measuring.

| Component | Role in this chain |
|---|---|
| **Rights Request Intake** | Receives requests from data subjects through every channel the company offers, and starts the statutory clock. |
| **Data Subject Identity Verification** | Establishes that the requester is who they claim to be, proportionately to what they are asking for. |
| **Record of Processing Activities Register** | Records what personal data the company processes, for what purpose, under what lawful basis, and where it is held. |
| **Personal Data Discovery** | Surveys systems and stores for personal data and reconciles what it finds against the record of processing. |
| **Rights Fulfilment Orchestrator** | Fans a verified request out to every system and processor holding the person's data, collects what comes back, and drives erasure, rectification and objection decisions onward to the systems that must act on them. |
| **Retention Schedule Service** | Holds the retention obligation attaching to each category of personal data, so that an erasure decision can be checked against the obligations that override it. |
| **Egeria Open Metadata and Governance** | The catalogue is where personal data holdings are recorded, and is what discovery reconciles the register against. |
| **Worker Master Register** | Employee personal data is anchored on the worker record, which is one of the two largest holdings the chain has to reach. |
| **Patient Identity Register** | Patient identity is deliberately concentrated here, which makes it findable — the same property that protects it. |
| **Set Retention Period** | Retention periods set during data onboarding are the obligations an erasure decision has to be checked against. |
| Joiner Mover Leaver Workflow *(handover)* | Onboarding is what distributes employee personal data across the estate, so it is what the record of processing has to describe. |

The components below already exist — they come from `CocoComboArchive.omarchive` — so they are located and added to the chain rather than created.

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Data Subject Rights Information Supply Chain

### ISC Child
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Membership Rationale
The catalogue is where personal data holdings are recorded, and is what discovery reconciles the register against.

### Membership Status
VALIDATED

___

---

___

## Link Information Supply Chain Child

### ISC Parent
InformationSupplyChain::Data Subject Rights Information Supply Chain

### ISC Child
SolutionComponent::Set Retention Period::V1.0

### Membership Rationale
Retention periods set during data onboarding are the obligations an erasure decision has to be checked against.

### Membership Status
VALIDATED

___

---

**Wires**

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RightsRequestIntake

### Component2
CocoPharma::SolutionComponent::IdentityVerification

### Label
verify requester

### Description
Verification is proportionate to what is being asked for, and it is what stops the rights process becoming an attack on the data it protects.

### Data Exchanged
request, claimed identity, evidence offered

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::IdentityVerification

### Component2
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Label
verified request

### Description
The clock carried forward is the one that started at receipt by any part of the company, not at verification.

### Data Exchanged
verified subject, request type, receipt timestamp

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RecordOfProcessingRegister

### Component2
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Label
where to look

### Description
The register is what tells the chain where to look, so its accuracy is tested every time a request is answered.

### Data Exchanged
processing activities, systems, processors, purposes

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::PersonalDataDiscovery

### Component2
CocoPharma::SolutionComponent::RecordOfProcessingRegister

### Label
reconcile holdings

### Description
The register describes what the company believes it processes; discovery describes what it actually holds. The gap is the finding.

### Data Exchanged
discovered personal data, systems, discrepancies against register

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Component2
CocoPharma::SolutionComponent::PersonalDataDiscovery

### Label
catalogued holdings

### Description
Discovery works from the catalogue rather than scanning blind, which is what makes it tractable at estate scale.

### Data Exchanged
assets, classifications, personal data indicators

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Component2
CocoPharma::SolutionComponent::WorkerMasterRegister

### Label
locate employee data

### Description
Employee data is one of the two largest holdings the chain has to reach, and the worker record is its anchor.

### Data Exchanged
subject identity, request type

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::New Employee Onboarding Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Component2
CocoPharma::SolutionComponent::PatientIdentityRegister

### Label
locate patient data

### Description
Patient identity is concentrated in one register, which makes it findable — the same property that protects it.

### Data Exchanged
subject identity, request type

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RetentionScheduleService

### Component2
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Label
retention constraints

### Description
Clinical trial records, employment decisions and health surveillance all outrank a request to be forgotten, and the chain has to know that per holding rather than in general.

### Data Exchanged
category, retention obligation, overriding basis

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

___

## Link Solution Components

### Component1
SolutionComponent::Set Retention Period::V1.0

### Component2
CocoPharma::SolutionComponent::RetentionScheduleService

### Label
retention periods set

### Description
Retention set at onboarding is what an erasure decision is checked against years later.

### Data Exchanged
asset, retention basis, archive and delete dates

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain
- InformationSupplyChain::Clinical Trials Information Supply Chain

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator

### Component2
CocoPharma::SolutionComponent::RightsRequestIntake

### Label
response

### Description
The response has to be complete within the statutory period, and the period cannot be extended by the company not knowing where its data is.

### Data Exchanged
assembled response, actions taken, decisions and reasons

### ISC Qualified Names
- InformationSupplyChain::Data Subject Rights Information Supply Chain

___

---

## Appendix: What the Wires Revealed

Drawing the wires produced four findings that the register could not have produced on its own.

**Components belong to more chains than anyone expected.** The qualification register is read by manufacturing, by clinical trials and by dangerous goods transport, and none of those consumers is a human resources use case. The HazMat inventory serves occupational health, transport classification and inventory tracking from one substance identity. The subledger feeds carry four different chains into the same ledger. Each of these is a component whose owner is answering questions they were not asked when it was bought.

**The handovers are where the work is.** Of the 130 wires, forty-four implement more than one supply chain — they are the points at which a fault in one chain becomes a failure in the next. Those are the wires worth instrumenting first, and none of them belongs unambiguously to one team.

**Some chains are gates, not flows.** Batch release, material quarantine and identifier upload are not conveyances; they are refusals that occasionally let something through. Modelling them as wires makes the gate visible as a dependency, which is what a downstream team needs in order to understand why their input sometimes does not arrive.

**The archive's stubs were a plan.** Five blueprints existed with almost nothing in them, and every one of them turned out to sit exactly where a strategic supply chain needed components. Filling them in was easier than deciding where to put a new blueprint would have been.

---

## Appendix: What This File Deliberately Leaves Out

**Implementation links.** No component here is yet linked to the systems that implement it through `ImplementedBy`. The archive does this for nine of its own components, and the systems inventory built in `4. keeping-safe/` is what the rest would be linked to. That linkage is what turns a designed component into a monitored one.

**Ports and delegation.** Solution ports and port delegation are not modelled. They matter when a component's interface is contested between teams; none of these are yet.

**Roles.** The archive attaches solution actor roles to its two complete blueprints. The components here have owners in the governance program but no `SolutionActorRole`, so a chain cannot yet answer who to call at three in the morning.

**Segments.** The strategic register said segmenting each chain is best done by the team that owns it. That remains true, and this file makes it easier rather than doing it: the wires now show where the natural segment boundaries fall.

---

## Appendix: Related Resources

| Resource | Relevance |
|---|---|
| [`0. data-governance-program/strategic-information-supply-chains.md`](../0.%20data-governance-program/strategic-information-supply-chains.md) | Creates the supply chains this file implements, and links them to governance |
| [solution-design.md](solution-design.md) | The Data Hub blueprint; loads after this file and links the eight business system groups to it |
| [Information supply chains](https://egeria-project.org/concepts/information-supply-chain/) | The concept, and how implementation links to lineage |
| [Solution blueprints](https://egeria-project.org/concepts/solution-blueprint/) | The blueprints the archive supplies and this file fills in |
| `CocoComboArchive.omarchive` | Supplies the eight reused components and the five stub blueprints |

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
