# Strategic Digital Product Dependencies

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The dependencies between the strategic digital products, one for each solution linking wire in the supply chain analysis whose two ends both have a product.

---

## Overview

A solution linking wire in the [strategic supply chain analysis](../strategic-supply-chain-analysis.md) says that data flows from one component to another.  In product terms, the product built from the data *entering* the second component depends on the product the first component *publishes*.  This file draws that dependency for every wire: the consuming product is `Digital Product 1`, the product it depends on is `Digital Product 2`, the label is the wire's label, and the description records what data is exchanged and which supply chains the exchange implements.

Wires with one end outside Coco Pharmaceuticals produce no dependency where the data is *sent out* (to national verification systems, to carriers, to the screening service) and where the hospital's own processes are the source.  Where an external party sends data *in*, that data is a product in its own right, owned by the group that receives it, and the dependencies run from it.

Because `DigitalProductDependency` is a multi-link relationship, two products that exchange several kinds of data along several wires have one dependency per wire, each carrying its own label.

125 dependencies.  This file loads last.

```
dr_egeria --directive process --userid erinoverview --user_pass secret product-dependencies.md
```

### Dependencies per supply chain

| Supply chain | Dependencies |
|---|---|
| Batch Manufacturing and Release | 19 |
| Third Party Onboarding and Payment | 15 |
| Personalized Treatment Ordering | 14 |
| New Employee Onboarding | 14 |
| Financial Close and External Reporting | 13 |
| Physical Inventory Tracking | 11 |
| Data Subject Rights | 11 |
| Workforce Competency and Qualification | 10 |
| Product Serialisation and Verification | 10 |
| Cold Chain and Dangerous Goods Consignment | 10 |
| Occupational Health Surveillance | 10 |
| Adverse Event and Safety Reporting | 9 |
| New Drug Product Details | 9 |
| Employee Expense Payment | 7 |
| Clinical Trials | 3 |

---

# Data Hub

Dependencies of the Data Hub group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Data Hub Business Summary

### Digital Product 2
DigitalProduct::Coco::Treatment Invoices

### Label
new-business

### Description
Order, fulfilment and revenue summary.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Data Hub Business Summary

### Digital Product 2
DigitalProduct::Coco::Batch Certification Decisions

### Label
manufacturing-status

### Description
Batch identity, certification decision, quantities.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Data Hub Business Summary

### Digital Product 2
DigitalProduct::Coco::Goods Inventory Stock

### Label
inventory

### Description
Stock levels, locations, movements.  Implements: Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Product Master Data

### Digital Product 2
DigitalProduct::Coco::New Product Definitions

### Label
new product definition

### Description
Composition, presentations, specification.  Implements: New Drug Product Details; Clinical Trials.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Product Master Data

### Digital Product 2
DigitalProduct::Coco::Market Authorisations

### Label
authorised markets

### Description
Authorisation, conditions, labelling requirements.  Implements: New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Product Change Notifications

### Digital Product 2
DigitalProduct::Coco::Product Master Data

### Label
publish change

### Description
Changed product attributes, effective date.  Implements: New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Data Hub Business Summary

### Digital Product 2
DigitalProduct::Coco::Product Change Notifications

### Label
product master feed

### Description
Current product definitions.  Implements: New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Digital Product 2
DigitalProduct::Coco::Product Change Notifications

### Label
record distribution

### Description
Recipients, applied and outstanding changes.  Implements: New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Digital Product 2
DigitalProduct::Coco::Access Entitlements

### Label
access and ownership

### Description
Accounts, entitlements, data ownership assignments.  Implements: New Employee Onboarding.

___

# Patient Treatment

Dependencies of the Patient Treatment group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Patient Pseudonym Register

### Digital Product 2
DigitalProduct::Coco::Treatment Orders

### Label
register order

### Description
Patient identity, prescribing clinician, product ordered.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Patient Pseudonym Register

### Digital Product 2
DigitalProduct::Coco::Therapy Delivery Events

### Label
administration confirmed

### Description
Pseudonym, delivery and administration timestamps.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Patient Pseudonym Register

### Digital Product 2
DigitalProduct::Coco::Rights Fulfilment Actions

### Label
locate patient data

### Description
Subject identity, request type.  Implements: Data Subject Rights; Personalized Treatment Ordering.

___

# Finance

Dependencies of the Finance group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Treatment Invoices

### Digital Product 2
DigitalProduct::Coco::Therapy Delivery Events

### Label
fulfilment confirmed

### Description
Order identity, delivery evidence.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::General Ledger Balances

### Digital Product 2
DigitalProduct::Coco::Treatment Invoices

### Label
revenue posting

### Description
Invoice, revenue recognition data.  Implements: Personalized Treatment Ordering; Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::General Ledger Balances

### Digital Product 2
DigitalProduct::Coco::Subledger Postings

### Label
post transactions

### Description
Transaction batches per source and period.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Subledger Postings

### Digital Product 2
DigitalProduct::Coco::Employee Expense Claims

### Label
expense postings

### Description
Approved expense claims, cost coding.  Implements: Financial Close and External Reporting; Employee Expense Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Subledger Postings

### Digital Product 2
DigitalProduct::Coco::Supplier Payments

### Label
payment postings

### Description
Authorised payments, supplier, cost coding.  Implements: Financial Close and External Reporting; Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Subledger Postings

### Digital Product 2
DigitalProduct::Coco::Treatment Invoices

### Label
revenue postings

### Description
Invoices, revenue recognition data.  Implements: Financial Close and External Reporting; Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Subledger Postings

### Digital Product 2
DigitalProduct::Coco::Payroll Results

### Label
payroll postings

### Description
Remuneration, employer costs, by entity.  Implements: Financial Close and External Reporting; New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Manual Journal Approvals

### Digital Product 2
DigitalProduct::Coco::General Ledger Balances

### Label
material entries for review

### Description
Manual journal entries above threshold.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::General Ledger Balances

### Digital Product 2
DigitalProduct::Coco::Manual Journal Approvals

### Label
approved adjustments

### Description
Reviewed and approved journal entries.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Consolidated Group Results

### Digital Product 2
DigitalProduct::Coco::General Ledger Balances

### Label
entity ledgers

### Description
Trial balances by entity and currency.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::External Financial Disclosures

### Digital Product 2
DigitalProduct::Coco::Consolidated Group Results

### Label
consolidated results

### Description
Consolidated statements, segment analysis.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Financial Controls Evidence

### Digital Product 2
DigitalProduct::Coco::Consolidated Group Results

### Label
close evidence

### Description
Reconciliations, approvals, close checklist.  Implements: Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::External Financial Disclosures

### Digital Product 2
DigitalProduct::Coco::Transfers Of Value

### Label
transfers of value

### Description
Payments and benefits to healthcare professionals.  Implements: Financial Close and External Reporting; Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Payments

### Digital Product 2
DigitalProduct::Coco::Supplier Master Data

### Label
supplier and payment details

### Description
Screening status, risk rating, bank details.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Payments

### Digital Product 2
DigitalProduct::Coco::Purchase Orders And Receipts

### Label
order and receipt

### Description
Purchase order, goods receipt confirmation.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::General Ledger Balances

### Digital Product 2
DigitalProduct::Coco::Supplier Payments

### Label
payment instruction

### Description
Authorised payment, supplier, amount, coding.  Implements: Third Party Onboarding and Payment; Financial Close and External Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Payment Anomaly Findings

### Digital Product 2
DigitalProduct::Coco::Supplier Payments

### Label
payment stream

### Description
Payments, suppliers, timing and amounts.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Transfers Of Value

### Digital Product 2
DigitalProduct::Coco::Supplier Payments

### Label
identify disclosable payment

### Description
Payee, benefit, purpose, value.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Expense Approvals

### Digital Product 2
DigitalProduct::Coco::Employee Expense Claims

### Label
submit for approval

### Description
Claim, cost coding, supporting evidence.  Implements: Employee Expense Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Expense Approvals

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
approver and cost centre

### Description
Worker, reporting line, spending authority.  Implements: Employee Expense Payment; New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Employee Expense Claims

### Digital Product 2
DigitalProduct::Coco::Expense Approvals

### Label
approval decision

### Description
Approval, approver identity, timestamp.  Implements: Employee Expense Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Transfers Of Value

### Digital Product 2
DigitalProduct::Coco::Employee Expense Claims

### Label
identify disclosable expense

### Description
Payee, benefit, purpose, value.  Implements: Employee Expense Payment; Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Payment Anomaly Findings

### Digital Product 2
DigitalProduct::Coco::Employee Expense Claims

### Label
expense stream

### Description
Claims, claimants, categories and amounts.  Implements: Employee Expense Payment; Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Employee Expense Claims

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
expense access

### Description
Worker, cost centre, spending authority.  Implements: New Employee Onboarding; Employee Expense Payment.

___

# Procurement

Dependencies of the Procurement group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Master Data

### Digital Product 2
DigitalProduct::Coco::Third Party Onboarding Cases

### Label
create supplier record

### Description
Approved supplier, risk rating, screening evidence.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Master Data

### Digital Product 2
DigitalProduct::Coco::Supplier Payment Detail Changes

### Label
verified bank details

### Description
Changed payment details, independent verification evidence.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Master Data

### Digital Product 2
DigitalProduct::Coco::Payment Anomaly Findings

### Label
raise supplier concern

### Description
Anomaly, supplier, evidence.  Implements: Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Supplier Material Certificates

### Digital Product 2
DigitalProduct::Coco::Supplier Master Data

### Label
supplier documentation

### Description
Approved supplier, quality documentation.  Implements: Third Party Onboarding and Payment; Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Third Party Onboarding Cases

### Digital Product 2
DigitalProduct::Coco::Third Party Screening Results

### Label
screening result

### Description
Matches, risk indicators, screening date.  Implements: Third Party Onboarding and Payment.

___

# Research

Dependencies of the Research group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Hospital Certifications

### Digital Product 2
DigitalProduct::Coco::Worker Qualifications

### Label
site staff training evidence

### Description
Site staff, protocol training, dates.  Implements: Workforce Competency and Qualification; Clinical Trials.

___

# Warehouse

Dependencies of the Warehouse group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Goods Inventory Stock

### Digital Product 2
DigitalProduct::Coco::Serialised Product Identifiers

### Label
serialised stock

### Description
Identifiers, aggregation, location.  Implements: Product Serialisation and Verification; Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Hazardous Material Holdings

### Digital Product 2
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Label
consignment record

### Description
Declaration, classification, quantities shipped.  Implements: Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Goods Receipts

### Digital Product 2
DigitalProduct::Coco::Supplier Master Data

### Label
approved supplier

### Description
Supplier identity, approval and risk status.  Implements: Physical Inventory Tracking; Third Party Onboarding and Payment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Goods Receipts

### Digital Product 2
DigitalProduct::Coco::Supplier Material Certificates

### Label
certificate of analysis

### Description
Supplier test results, conformity declaration.  Implements: Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Material Quarantine Dispositions

### Digital Product 2
DigitalProduct::Coco::Goods Receipts

### Label
place in quarantine

### Description
Received lot, quantity, storage location.  Implements: Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Material Quarantine Dispositions

### Digital Product 2
DigitalProduct::Coco::Laboratory Test Results

### Label
test results

### Description
Results, specification comparison, disposition.  Implements: Physical Inventory Tracking; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Goods Inventory Stock

### Digital Product 2
DigitalProduct::Coco::Material Quarantine Dispositions

### Label
release for use

### Description
Released lot, quantity, expiry.  Implements: Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Hazardous Material Holdings

### Digital Product 2
DigitalProduct::Coco::Goods Inventory Stock

### Label
hazardous holdings

### Description
Substance, quantity, location.  Implements: Physical Inventory Tracking; Occupational Health Surveillance.

___

# Manufacturing

Dependencies of the Manufacturing group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Digital Product 2
DigitalProduct::Coco::Patient Sample Consignments

### Label
patient material received

### Description
Consignment identity, arrival condition, remaining viable life.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Digital Product 2
DigitalProduct::Coco::Patient Pseudonym Register

### Label
identified manufacturing instruction

### Description
Pseudonym, product specification, patient-specific parameters.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Label
open batch

### Description
Batch identity, pseudonym, product specification.  Implements: Personalized Treatment Ordering; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Execution Records

### Digital Product 2
DigitalProduct::Coco::Goods Inventory Stock

### Label
issue material

### Description
Material identity, lot, quantity, quarantine status.  Implements: Batch Manufacturing and Release; Physical Inventory Tracking.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Execution Records

### Digital Product 2
DigitalProduct::Coco::Laboratory Test Results

### Label
in-process results

### Description
Sample results, specification comparison.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Execution Records

### Digital Product 2
DigitalProduct::Coco::Equipment Qualification Status

### Label
qualification status

### Description
Equipment identity, qualification and calibration validity.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Execution Records

### Digital Product 2
DigitalProduct::Coco::Worker Qualifications

### Label
operator qualification

### Description
Worker pseudonym, qualifications, currency.  Implements: Batch Manufacturing and Release; Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Batch Execution Records

### Label
execution record

### Description
Steps performed, materials used, equipment, signatures.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Process Parameter Time Series

### Label
process parameters

### Description
Time series of critical process parameters.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Laboratory Test Results

### Label
finished product results

### Description
Release testing results, certificate of analysis.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Deviations And CAPAs

### Label
deviation disposition

### Description
Investigation outcome, impact on batch.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serial Number Allocations

### Digital Product 2
DigitalProduct::Coco::Product Master Data

### Label
pack configuration

### Description
Product code, pack presentation, destination market.  Implements: Product Serialisation and Verification; New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Commissioned Packs

### Digital Product 2
DigitalProduct::Coco::Serial Number Allocations

### Label
issue identifiers

### Description
Allocated serial numbers.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serialised Product Identifiers

### Digital Product 2
DigitalProduct::Coco::Commissioned Packs

### Label
commission packs

### Description
Commissioned identifiers, batch and expiry.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Digital Product 2
DigitalProduct::Coco::Commissioned Packs

### Label
pack to case

### Description
Pack identifiers, case identity.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serialised Product Identifiers

### Digital Product 2
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Label
aggregation hierarchy

### Description
Pack, case and pallet relationships.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Market Identifier Submissions

### Digital Product 2
DigitalProduct::Coco::Electronic Batch Records

### Label
release authorisation

### Description
Batch certification, released quantities and markets.  Implements: Product Serialisation and Verification; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Market Identifier Submissions

### Digital Product 2
DigitalProduct::Coco::Serialised Product Identifiers

### Label
identifiers for upload

### Description
Commissioned identifiers, aggregation, destination.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serialised Product Identifiers

### Digital Product 2
DigitalProduct::Coco::Serialisation Alert Investigations

### Label
alert disposition

### Description
Root cause, corrective action, affected identifiers.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Temperature Excursion Assessments

### Label
disposition recorded

### Description
Excursion assessment, disposition decision.  Implements: Cold Chain and Dangerous Goods Consignment; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Electronic Batch Records

### Digital Product 2
DigitalProduct::Coco::Worker Qualifications

### Label
signature authority

### Description
Worker pseudonym, qualifications, currency at time of signature.  Implements: Workforce Competency and Qualification; Batch Manufacturing and Release.

___

# Delivery

Dependencies of the Delivery group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Patient Sample Consignments

### Digital Product 2
DigitalProduct::Coco::Treatment Orders

### Label
request sample collection

### Description
Collection site, time window, material required.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Therapy Delivery Events

### Digital Product 2
DigitalProduct::Coco::Batch Certification Decisions

### Label
therapy released

### Description
Batch identity, pseudonym, certification, storage conditions.  Implements: Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Transport Classifications

### Digital Product 2
DigitalProduct::Coco::Hazardous Material Holdings

### Label
substance identity

### Description
Substance, hazard classification, form and quantity.  Implements: Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Transport Classifications

### Digital Product 2
DigitalProduct::Coco::Product Master Data

### Label
product handling requirements

### Description
Storage range, packaging, hazard properties.  Implements: Cold Chain and Dangerous Goods Consignment; New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Digital Product 2
DigitalProduct::Coco::Transport Classifications

### Label
classification and requirements

### Description
UN number, packing group, labelling, documentation set.  Implements: Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Digital Product 2
DigitalProduct::Coco::Worker Qualifications

### Label
certificated signatory

### Description
Worker pseudonym, certificate and expiry.  Implements: Cold Chain and Dangerous Goods Consignment; Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Cold Chain Transit Records

### Digital Product 2
DigitalProduct::Coco::In-Transit Temperature Readings

### Label
transit temperature record

### Description
Time series of in-transit temperature and location.  Implements: Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Cold Chain Transit Records

### Digital Product 2
DigitalProduct::Coco::Patient Sample Consignments

### Label
inbound material record

### Description
Consignment identity, in-transit condition.  Implements: Cold Chain and Dangerous Goods Consignment; Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Transport Classifications

### Digital Product 2
DigitalProduct::Coco::Occupational Exposure Bands

### Label
shared substance classification

### Description
Substance, hazard classification.  Implements: Occupational Health Surveillance; Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Cold Chain Transit Records

### Digital Product 2
DigitalProduct::Coco::Carrier Transit Events

### Label
read directly

### Description
Data read directly from the upstream product.  Implements: read directly.

___

# Quality Systems

Dependencies of the Quality Systems group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Consolidated Safety Reports

### Digital Product 2
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Label
clinician report

### Description
Suspected reaction, patient pseudonym, product and batch.  Implements: Adverse Event and Safety Reporting; Personalized Treatment Ordering.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Consolidated Safety Reports

### Digital Product 2
DigitalProduct::Coco::Product Complaints

### Label
complaint with safety content

### Description
Complaint, product, batch, reported harm.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Pharmacovigilance Cases

### Digital Product 2
DigitalProduct::Coco::Consolidated Safety Reports

### Label
open case

### Description
Consolidated report, receipt timestamp, source.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Medical Assessments

### Digital Product 2
DigitalProduct::Coco::Pharmacovigilance Cases

### Label
assess and code

### Description
Case narrative, product, patient context.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Pharmacovigilance Cases

### Digital Product 2
DigitalProduct::Coco::Medical Assessments

### Label
assessment recorded

### Description
Seriousness, expectedness, causality, coded terms.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Safety Signals

### Digital Product 2
DigitalProduct::Coco::Pharmacovigilance Cases

### Label
case data for analysis

### Description
Coded cases, exposure denominators.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Regulatory Safety Submissions

### Digital Product 2
DigitalProduct::Coco::Pharmacovigilance Cases

### Label
submit report

### Description
Expedited and periodic reports, per market.  Implements: Adverse Event and Safety Reporting.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Deviations And CAPAs

### Digital Product 2
DigitalProduct::Coco::Safety Signals

### Label
signal referred to quality

### Description
Signal, implicated product or process.  Implements: Adverse Event and Safety Reporting; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Market Authorisations

### Digital Product 2
DigitalProduct::Coco::Safety Signals

### Label
label or authorisation change

### Description
Safety finding, affected authorisations.  Implements: Adverse Event and Safety Reporting; New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Deviations And CAPAs

### Digital Product 2
DigitalProduct::Coco::Batch Execution Records

### Label
raise deviation

### Description
Departure from approved process, context.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Certification Decisions

### Digital Product 2
DigitalProduct::Coco::Product Master Data

### Label
product and market requirements

### Description
Specification, pack configuration, authorised markets.  Implements: Batch Manufacturing and Release; New Drug Product Details.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Batch Certification Decisions

### Digital Product 2
DigitalProduct::Coco::Electronic Batch Records

### Label
batch record for review

### Description
Complete assembled batch record.  Implements: Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serialisation Alert Investigations

### Digital Product 2
DigitalProduct::Coco::Market Verification Responses

### Label
raise alert

### Description
Alert, identifier, reporting party.  Implements: Product Serialisation and Verification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Temperature Excursion Assessments

### Digital Product 2
DigitalProduct::Coco::Cold Chain Transit Records

### Label
excursion detected

### Description
Excursion profile, duration, product and batch.  Implements: Cold Chain and Dangerous Goods Consignment.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Laboratory Test Results

### Digital Product 2
DigitalProduct::Coco::Material Quarantine Dispositions

### Label
request incoming testing

### Description
Lot identity, required tests.  Implements: Physical Inventory Tracking; Batch Manufacturing and Release.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Occupational Exposure Bands

### Digital Product 2
DigitalProduct::Coco::Hazardous Material Holdings

### Label
substance holdings

### Description
Substance, hazard data, quantities and locations.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Exposure Monitoring Results

### Digital Product 2
DigitalProduct::Coco::Occupational Exposure Bands

### Label
banded limits

### Description
Band, exposure limit, required containment.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Exposure Monitoring Results

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
worker and task exposure

### Description
Worker, role, tasks and locations.  Implements: Occupational Health Surveillance; New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Occupational Exposure Bands

### Digital Product 2
DigitalProduct::Coco::Incidents And Near Misses

### Label
assessment feedback

### Description
Incident, implicated substance or control, findings.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Serialisation Alert Investigations

### Digital Product 2
DigitalProduct::Coco::Market Verification Responses

### Label
read directly

### Description
Data read directly from the upstream product.  Implements: read directly.

___

# People Systems

Dependencies of the People Systems group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Worker Master Data

### Digital Product 2
DigitalProduct::Coco::Worker Lifecycle Events

### Label
worker event

### Description
Joiner, mover or leaver event, effective date.  Implements: New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Access Entitlements

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
provision or revoke

### Description
Worker identity, role, effective date.  Implements: New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Payroll Results

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
payroll record

### Description
Worker, entity, contract terms.  Implements: New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Corporate Directory Entries

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
directory entry

### Description
Name, role, location, reporting line.  Implements: New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Worker Qualifications

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
new worker record

### Description
Worker identity, role, start date.  Implements: New Employee Onboarding; Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Health Surveillance Records

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
surveillance enrolment

### Description
Worker, role, exposure profile.  Implements: New Employee Onboarding; Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Training Completions

### Digital Product 2
DigitalProduct::Coco::Role Competency Requirements

### Label
required competencies

### Description
Role, required competencies, refresh interval.  Implements: Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Training Completions

### Digital Product 2
DigitalProduct::Coco::Worker Master Data

### Label
worker and role

### Description
Worker identity, role, start date.  Implements: Workforce Competency and Qualification; New Employee Onboarding.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Worker Qualifications

### Digital Product 2
DigitalProduct::Coco::Training Completions

### Label
completion and assessment

### Description
Training completed, assessment results, dates.  Implements: Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Qualification Expiry Warnings

### Digital Product 2
DigitalProduct::Coco::Worker Qualifications

### Label
qualification status

### Description
Qualifications, expiry dates.  Implements: Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Training Completions

### Digital Product 2
DigitalProduct::Coco::Qualification Expiry Warnings

### Label
refresher required

### Description
Worker, lapsing qualification, deadline.  Implements: Workforce Competency and Qualification.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Health Surveillance Records

### Digital Product 2
DigitalProduct::Coco::Exposure Monitoring Results

### Label
exposure results

### Description
Personal and static measurements, comparison to limits.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Health Surveillance Records

### Digital Product 2
DigitalProduct::Coco::Incidents And Near Misses

### Label
exposure incident

### Description
Affected worker, exposure event, immediate response.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Long Term Health Archive

### Digital Product 2
DigitalProduct::Coco::Health Surveillance Records

### Label
archive record

### Description
Surveillance results, exposure history, worker identity.  Implements: Occupational Health Surveillance.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Worker Master Data

### Digital Product 2
DigitalProduct::Coco::Rights Fulfilment Actions

### Label
locate employee data

### Description
Subject identity, request type.  Implements: Data Subject Rights; New Employee Onboarding.

___

# Privacy Operations

Dependencies of the Privacy Operations group's products.

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Record Of Processing Activities

### Digital Product 2
DigitalProduct::Coco::Worker Lifecycle Events

### Label
employee personal data

### Description
Processing purposes, systems holding worker data.  Implements: New Employee Onboarding; Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Requester Identity Verifications

### Digital Product 2
DigitalProduct::Coco::Data Subject Rights Requests

### Label
verify requester

### Description
Request, claimed identity, evidence offered.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Rights Fulfilment Actions

### Digital Product 2
DigitalProduct::Coco::Requester Identity Verifications

### Label
verified request

### Description
Verified subject, request type, receipt timestamp.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Rights Fulfilment Actions

### Digital Product 2
DigitalProduct::Coco::Record Of Processing Activities

### Label
where to look

### Description
Processing activities, systems, processors, purposes.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Record Of Processing Activities

### Digital Product 2
DigitalProduct::Coco::Personal Data Discovery Findings

### Label
reconcile holdings

### Description
Discovered personal data, systems, discrepancies against register.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Personal Data Discovery Findings

### Digital Product 2
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Label
catalogued holdings

### Description
Assets, classifications, personal data indicators.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Rights Fulfilment Actions

### Digital Product 2
DigitalProduct::Coco::Retention Obligations

### Label
retention constraints

### Description
Category, retention obligation, overriding basis.  Implements: Data Subject Rights.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Retention Obligations

### Digital Product 2
DigitalProduct::Coco::Retention Period Assignments

### Label
retention periods set

### Description
Asset, retention basis, archive and delete dates.  Implements: Data Subject Rights; Clinical Trials.

___

## Link Product Dependency

### Digital Product 1
DigitalProduct::Coco::Data Subject Rights Requests

### Digital Product 2
DigitalProduct::Coco::Rights Fulfilment Actions

### Label
response

### Description
Assembled response, actions taken, decisions and reasons.  Implements: Data Subject Rights.

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
