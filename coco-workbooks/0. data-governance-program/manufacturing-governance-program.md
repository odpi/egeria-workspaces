# Coco Pharmaceuticals — Manufacturing Governance Program

> **Author:** Stew Faster (Head of Manufacturing), Florence Paynter, George Pie  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-15  
> **Description:** Governance definitions for the MANUFACTURING domain at Coco Pharmaceuticals. This file extends the foundation in `joint-governance-officer-definitions.md` (which defines the Good Manufacturing Practice regulation, the EachInformationCollectionHasDesignatedOwner obligation, and the MetadataDrivenGovernance approach) with the detailed manufacturing data governance policies, controls, and metrics needed to operationalise GMP compliance. It also creates the Manufacturing Governance Lead folio and registers it in the root collection.

---

## Overview

Coco Pharmaceuticals manufactures pharmaceutical products under regulatory frameworks that impose strict data governance requirements on every stage of production — from raw material receipt through batch manufacture, quality control, and release. As the organisation transitions towards personalised, on-demand manufacturing, the complexity and volume of manufacturing data governance increases significantly.

As Head of Manufacturing, Stew Faster is accountable for ensuring that all manufacturing data is trustworthy, traceable, and managed in a manner that satisfies regulatory requirements. This governance program covers three layers:

1. **Governance Drivers** — the manufacturing-specific regulations and business imperatives that motivate governance activity in this domain.
2. **Governance Policies** — the principles, obligations, and approaches that define how manufacturing data is managed, protected, and verified.
3. **Governance Controls** — the roles and metrics that operationalise the manufacturing governance policies day-to-day.

All definitions in this file have Domain Identifier `MANUFACTURING` and are members of the Manufacturing Governance Lead Governance Folio defined in Part 6.

---

## Part 1: Governance Drivers — Manufacturing Domain

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Manufacturing Data Integrity

### Qualified Name
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Domain Identifier
MANUFACTURING

### Summary
All data generated during pharmaceutical manufacturing must be accurate, complete, and traceable to support batch release, regulatory inspection, and patient safety.

### Description
Pharmaceutical manufacturing is one of the most data-intensive regulated environments. Every step in the manufacturing process — from raw material testing to in-process monitoring, equipment log entries, environmental controls, and final batch release — generates data that forms part of the regulatory record. If that data is inaccurate, incomplete, or untraceable, the batch cannot be released. In the event of a product quality issue or recall, the data must support a complete investigation. As Coco Pharmaceuticals moves towards on-demand personalised manufacturing, the volume, variety, and velocity of manufacturing data will increase substantially, making systematic data governance a business-critical capability rather than a compliance overhead.

### Implications
- Manufacturing data systems must capture data contemporaneously, not retrospectively
- Data must be attributable to the individual or system that generated it
- Original data must be preserved — overwriting without audit trail is prohibited
- The move to on-demand manufacturing requires real-time data quality assurance

### Outcomes
- Batches are released on the basis of complete, accurate, and reviewed records
- Regulatory inspections can be supported with full data traceability
- Product quality issues can be investigated quickly with complete data lineage

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
On-Demand Manufacturing Capability

### Qualified Name
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Domain Identifier
MANUFACTURING

### Summary
Coco Pharmaceuticals must develop the data infrastructure to support agile, patient-specific on-demand manufacturing alongside existing batch production.

### Description
Personalised medicine requires manufacturing to respond to individual patient needs rather than producing standardised batches for stock. This demands a fundamental shift in manufacturing data architecture: patient treatment parameters must flow into manufacturing systems; batch records must be patient-linked; quality systems must support much smaller batch sizes with greater variety; and data must flow in real time between clinical, manufacturing, and logistics systems. None of this is achievable without well-governed, high-quality manufacturing data and integration between previously siloed systems. The governance framework for manufacturing data must be designed to support both the existing batch model and the emerging on-demand model simultaneously.

### Implications
- Manufacturing data models must be extended to support patient-specific parameters
- Integration between clinical, manufacturing, and supply chain data must be governed
- Quality systems must support smaller-scale, higher-variety batch records
- Data quality monitoring must operate in near-real-time rather than end-of-batch

### Outcomes
- Hospital partners can receive patient-specific medicines on a clinically appropriate timeline
- Manufacturing can scale up on-demand production without compromising data governance
- Regulatory submissions for on-demand manufacturing are supported by complete data records

### Importance
High

### Category
Strategic Transformation

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 1.2 Threats

___

## Create Threat

### Display Name
Batch Quality Failure from Data Errors

### Qualified Name
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Domain Identifier
MANUFACTURING

### Summary
Inaccurate, incomplete, or untraceable manufacturing data may result in batch quality failures, product recalls, or the release of substandard products to patients.

### Description
Manufacturing data errors are a leading cause of batch failures and product recalls in the pharmaceutical industry. An incorrect quantity entry, a missed environmental monitoring result, an equipment log that cannot be attributed to a specific operator, or a deviation that was not recorded and investigated can each result in a batch being rejected — or, in a worst case, released when it should not have been. The risk is compounded for Coco Pharmaceuticals by the move to on-demand manufacturing, where smaller batch sizes and greater product variety reduce the opportunity for errors to be caught through statistical sampling. Every data error in a patient-specific batch directly affects that patient.

### Implications
- All manufacturing data entry points must have controls to prevent and detect errors
- Data must be reviewed by a qualified second person before batch release decisions are made
- Automated data capture must be preferred over manual entry wherever technically feasible
- Data entry errors must be investigated to root cause, not simply corrected

### Importance
Critical

### Category
Product Quality & Patient Safety

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Patient Identity Exposure Through Personalised Batch Records

### Qualified Name
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Domain Identifier
MANUFACTURING

### Summary
In personalised manufacturing the batch record is linked to an identified patient, exposing their identity and, by inference, their diagnosis to manufacturing staff and suppliers who have no clinical relationship with them.

### Description
Conventional batch records identify operators but not patients: a batch of ten thousand tablets is for nobody in particular. A personalised product inverts this. The batch exists because a named individual needs it, their starting material may be their own cells or a sample derived from them, and the record follows the product through manufacture, testing, and release. Everyone who touches that record — production operators, quality control analysts, warehouse staff, and any contract manufacturer or courier in the chain — is placed in possession of health data about an identifiable person. The exposure is worse than it first appears, because for a targeted therapy the product itself implies the condition: knowing which product a batch is discloses the diagnosis without any clinical field being present. The people concerned have no clinical relationship with the patient, work in an environment designed around product quality rather than patient confidentiality, and in many cases have no reason to know who the patient is at all — only that this batch is for that patient and must not be confused with another.

### Implications
- Manufacturing personnel require batch distinguishability, not patient identity
- The product type can disclose the diagnosis even where no clinical data is present in the record
- Contract manufacturers and logistics providers enter the chain of custody as recipients of health data
- Batch records circulate more widely than clinical records and under different controls

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 1.3 Regulations

___

## Create Regulation

### Display Name
EU GMP Annex 11 — Computerised Systems

### Qualified Name
CocoPharma::Regulation::EUGMPAnnex11

### Domain Identifier
MANUFACTURING

### Summary
EU GMP Annex 11 sets specific requirements for computerised systems used in pharmaceutical manufacturing, covering validation, data integrity, audit trails, and access controls.

### Description
EU GMP Annex 11 applies to all computerised systems used in GMP-regulated activities at Coco Pharmaceuticals — including Manufacturing Execution Systems (MES), Laboratory Information Management Systems (LIMS), building management systems controlling environmental conditions, and any electronic batch record systems. Key requirements include: system validation before use and after changes; access controls ensuring only authorised individuals can access, enter, or modify data; audit trails capturing who changed what and when; data backup and recovery; and requirements for electronic signatures where signatures are required by GMP. Annex 11 must be read alongside EU GMP Part I (Basic Requirements for Medicinal Products) and Part II (Basic Requirements for Active Substances). The US equivalent framework is FDA 21 CFR Part 11, which applies in parallel to Coco Pharmaceuticals' FDA-regulated activities.

### Regulation Source
EU GMP Annex 11 — Computerised Systems (EudraLex Volume 4)

### Regulators
- European Medicines Agency (EMA)
- Medicines and Healthcare products Regulatory Agency (MHRA) — UK
- National competent authorities in EU member states

### Implications
- All computerised manufacturing systems must be validated before use in production
- Audit trails must be enabled and must capture all GMP-relevant data changes
- Access to manufacturing systems must be controlled and logged by individual user identity
- Electronic data must be backed up and recoverable; backup integrity must be tested regularly

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Regulation

### Display Name
FDA Current Good Manufacturing Practice — 21 CFR Parts 210 and 211

### Qualified Name
CocoPharma::Regulation::FDAcGMP

### Domain Identifier
MANUFACTURING

### Summary
The US regulations setting minimum current good manufacturing practice for the manufacture, processing, packing, and holding of finished pharmaceuticals, enforced by FDA inspection of any site supplying the US market.

### Description
Parts 210 and 211 apply to every site supplying finished pharmaceuticals to the United States, wherever that site is located — which for Coco Pharmaceuticals means the UK and EU sites are subject to FDA inspection alongside their EU and MHRA obligations, not instead of them. The regulations overlap substantially with EU GMP but diverge in ways that matter operationally. Part 211 requires an independent quality control unit with defined authority to approve or reject, mandates specific record retention of one year past expiry, and requires investigation of any unexplained discrepancy or batch failure whether or not the batch was distributed, with the investigation extending to other batches that may have been associated. It also carries the annual product review requirement in §211.180(e). The most consequential divergence for data governance is the treatment of out-of-specification results, where FDA expectations shaped by the Barr Laboratories judgment require that an initial result is not invalidated without a documented laboratory investigation establishing an assignable cause — a requirement about how data may be treated rather than about how product is made. FDA also enforces through inspection observations and warning letters, and data integrity findings have been among the most common citations against pharmaceutical manufacturers.

### Regulation Source
21 CFR Part 210 and 21 CFR Part 211, with FDA guidance on data integrity and cGMP compliance

### Regulators
- Food and Drug Administration (FDA) — United States

### Implications
- UK and EU sites supplying the US market are subject to FDA inspection in addition to their local regimes
- An independent quality control unit with defined reject authority is required
- Out-of-specification results may not be invalidated without a documented assignable cause
- Unexplained discrepancies require investigation extending to potentially associated batches
- Records must be retained for at least one year past expiry, alongside the longer EU periods

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — MANUFACTURING Domain

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
ALCOA+ Data Integrity

### Qualified Name
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Domain Identifier
MANUFACTURING

### Summary
All manufacturing data must satisfy the ALCOA+ principles: Attributable, Legible, Contemporaneous, Original, and Accurate; plus Complete, Consistent, Enduring, and Available.

### Description
ALCOA+ is the pharmaceutical industry's recognised framework for manufacturing data integrity, adopted by regulators including the EMA, FDA, MHRA, and WHO. Each element has a specific meaning: **Attributable** — it must be clear who collected the data and when; **Legible** — data must be readable and permanent; **Contemporaneous** — data must be recorded at the time of the activity, not reconstructed afterwards; **Original** — the first recorded data or a certified copy must be retained; **Accurate** — data must be correct, truthful, and reflect what was actually observed. The additional ALCOA+ elements are: **Complete** — the record must include all relevant data including any repeat tests; **Consistent** — data must be internally consistent with other records from the same activity; **Enduring** — data must be maintained for the required retention period without degradation; **Available** — data must be accessible for review and inspection throughout the retention period. At Coco Pharmaceuticals, ALCOA+ applies to all data generated in GMP-regulated manufacturing activities, whether captured on paper, in electronic systems, or by automated instruments.

### Implications
- Manual data entry must be contemporaneous — pre-recording or post-recording from memory is prohibited
- Electronic systems must generate audit trails that capture original values and who changed them
- Instrument data must be captured directly from the instrument, not transcribed manually where avoidable
- Data must be retained in a readable, accessible format for the full regulatory retention period

### Outcomes
- Manufacturing records satisfy the data integrity expectations of EMA, FDA, and MHRA inspectors
- Batch release decisions are made on the basis of complete and accurate data
- Data integrity failures are detected and investigated before they affect product quality or patient safety

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Full Batch Traceability

### Qualified Name
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Domain Identifier
MANUFACTURING

### Summary
Every batch of manufactured product must be traceable forward from its raw material sources and backward from any distributed unit to the complete manufacturing record and source materials.

### Description
GMP regulations require that every batch can be fully traced in both directions: forward from raw materials through every manufacturing step to the finished product and its distribution; and backward from any unit of product in the market to its manufacturing record, in-process data, equipment, operators, and raw material lots. For Coco Pharmaceuticals, traceability is essential both for regulatory compliance — particularly for product recall management — and for the personalised medicine model, where individual patient batches must be linkable to the clinical treatment record that initiated the manufacturing order. Traceability must survive system changes, archiving, and staff turnover; it cannot depend on institutional knowledge held in people's heads.

### Implications
- Batch records must capture unique identifiers for every input: raw material lot numbers, equipment IDs, operator IDs, and environmental monitoring records
- System integrations between manufacturing, clinical, and supply chain systems must maintain traceable linkages
- Archiving must preserve traceability links — archived records must be as accessible as active ones for the purposes of investigation
- Product distribution records must link to batch records

### Outcomes
- Product recall decisions can be made quickly and with confidence based on traceable records
- Patient-specific manufacturing records can be linked to clinical outcomes for post-market surveillance
- GMP traceability requirements are satisfied for all regulatory jurisdictions in which Coco Pharmaceuticals operates

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Validated State Must Be Maintained

### Qualified Name
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Domain Identifier
MANUFACTURING

### Summary
All manufacturing processes, equipment, and computerised systems must be validated before use in production and must remain in a documented, qualified state throughout their operational life.

### Description
GMP regulations and EU GMP Annex 11 require that manufacturing processes are validated to demonstrate they consistently deliver a product meeting its specification; that equipment is qualified (Installation Qualification, Operational Qualification, Performance Qualification — IQ/OQ/PQ) before use; and that computerised systems are validated to demonstrate they perform as intended. Validation is not a one-time activity — processes, equipment, and systems must remain in a validated state throughout their operational life. Changes — whether planned improvements or emergency fixes — must go through change control to assess the impact on validated status and trigger revalidation where needed. At Coco Pharmaceuticals, the move to on-demand manufacturing introduces new process variants that each require validation before they can be used in patient-specific production.

### Implications
- No manufacturing process, piece of equipment, or computerised system may be used in production without documented validation or qualification evidence
- Changes to validated processes, equipment, and systems must go through the change control process
- Periodic review must confirm that validated states remain current and that equipment performance has not drifted
- Validation documentation must be retained for the life of the process or system plus the regulatory retention period

### Outcomes
- Products are manufactured using processes that have been demonstrated to be fit for purpose
- Regulatory inspections can verify the validated state of all manufacturing activities
- Changes are introduced safely without inadvertently compromising product quality

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Manufacturing Sees a Reference, Not a Patient

### Qualified Name
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Domain Identifier
MANUFACTURING

### Summary
Personalised manufacturing operates on a pseudonymous batch reference sufficient to prevent mix-up, with re-identification to the patient occurring only at the clinical boundary and only by clinical staff.

### Description
Manufacturing has a genuine and safety-critical need to distinguish one patient's product from another's — administering the wrong personalised product is potentially fatal and is the failure mode the whole chain is designed to prevent. That need is satisfied by a unique reference, not by a name. This principle separates the two: the manufacturing record carries a reference that is unique, verifiable, and unambiguous throughout production, while the mapping from reference to patient is held on the clinical side under clinical access controls and is resolved only at the point of administration, by staff who have a clinical relationship with the patient. The reference must be designed so that it does not itself leak identity — not derived from initials, date of birth, or hospital number — and so that it survives every system in the chain without truncation or reformatting, since a reference that gets reshaped between systems reintroduces exactly the ambiguity it exists to remove. Where a contract manufacturer or courier participates, they receive the reference only, and their contract binds them accordingly.

### Implications
- The batch reference must be unique, verifiable, and not derived from any patient identifier
- The reference-to-patient mapping is held clinically, not in manufacturing systems
- Re-identification occurs at administration, by clinical staff with a treating relationship
- The reference must pass through every system unchanged, including third-party systems
- Product type may still disclose condition, so the reference alone does not remove all exposure

### Outcomes
- Manufacturing achieves the distinguishability patient safety requires without holding identity
- Health data exposure is confined to those with a clinical relationship to the patient
- Contract manufacturers and logistics providers handle references rather than patient data

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.2 Governance Obligations

___

## Create Governance Obligation

### Display Name
Batch Records Must Be Complete, Accurate, and Retained

### Qualified Name
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Domain Identifier
MANUFACTURING

### Summary
A complete batch manufacturing record must be created for every batch produced, reviewed by a qualified second person, and retained for the regulatory retention period.

### Description
GMP regulations (EU GMP Chapter 4 and US 21 CFR Part 211.188) require that a Batch Manufacturing Record (BMR) or Master Batch Record is created for every batch. The record must document every step of the manufacturing process: starting materials and quantities, equipment used and its cleaning status, in-process checks and results, any deviations, environmental conditions where relevant, operator identities and signatures, yield reconciliation, and any additional steps required for on-demand patient-specific batches. The record must be reviewed — and any discrepancies resolved — before the batch is released. Electronic batch records must meet the additional requirements of EU GMP Annex 11 and FDA 21 CFR Part 11. Retention periods for batch records are typically 1 year after the product expiry date or 5 years after batch certification, whichever is longer — and for patient-specific batches may be linked to the patient record retention requirements.

### Implications
- A Master Batch Record must exist for every product and process variant before production begins
- Every GMP data entry in the batch record must be attributable, contemporaneous, and legible
- Batch records must be reviewed for completeness before being presented for Qualified Person certification
- Retention and archiving systems must maintain batch record integrity and accessibility for the full retention period

### Outcomes
- Every batch has a complete and reviewable record supporting the release decision
- Regulatory inspections can verify that batch records meet GMP requirements
- Product investigations and recalls are supported by complete batch data

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Manufacturing Deviations Must Be Documented, Investigated, and Closed

### Qualified Name
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Domain Identifier
MANUFACTURING

### Summary
Any deviation from an approved manufacturing process, specification, or procedure must be documented at the time of occurrence, investigated to root cause, and formally closed with documented corrective and preventive actions.

### Description
GMP regulations require that deviations from approved manufacturing procedures are documented, investigated, and acted upon. A deviation is any departure from an approved process, specification, or procedure — whether or not it results in a product quality impact. Deviations must be classified by impact (critical, major, minor), investigated to identify root cause, assessed for impact on the batch and on future batches, and closed with documented Corrective and Preventive Actions (CAPAs). Critical deviations may result in batch rejection. All open deviations must be resolved before the batch record can be closed and the batch presented for Qualified Person certification. Trend analysis of deviations is a GMP expectation and is used to identify systemic quality issues before they affect products.

### Implications
- Operators must be trained and empowered to raise deviations at the time they occur, without fear of blame
- Deviation forms must capture the event, its classification, immediate containment actions, and the investigation outcome
- CAPA actions must be assigned, tracked, and verified to closure within defined timeframes
- Deviation trends must be reviewed regularly as part of the product quality review process

### Outcomes
- Deviations are captured and investigated rather than concealed, supporting a culture of quality
- Root causes are identified and addressed, reducing recurrence
- Batch release decisions incorporate all relevant deviation data

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Equipment and Facilities Must Have Current Qualification Records

### Qualified Name
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Domain Identifier
MANUFACTURING

### Summary
All equipment and facilities used in pharmaceutical manufacturing must have documented qualification evidence (IQ/OQ/PQ) that is current and maintained through periodic review and change control.

### Description
GMP regulations require that manufacturing equipment and facilities are qualified before use and maintained in a qualified state. Installation Qualification (IQ) documents that equipment has been installed correctly; Operational Qualification (OQ) demonstrates that it operates within defined parameters; Performance Qualification (PQ) confirms consistent performance under production conditions. Qualification must be repeated or extended whenever equipment is moved, significantly repaired, or modified. A qualification register must be maintained, showing the qualification status, last review date, and next scheduled review for every critical piece of equipment. Equipment whose qualification has lapsed must be taken out of service until re-qualified. Calibration of measuring instruments is a related obligation that must also be maintained and documented.

### Implications
- A qualification register must be maintained and kept current for all GMP-critical equipment
- Change control must assess the qualification impact of every equipment modification or repair
- Calibration schedules must be defined and followed for all measuring instruments used in GMP activities
- Equipment with lapsed qualification or overdue calibration must be quarantined from production use

### Outcomes
- Products are manufactured using equipment that has been demonstrated to operate correctly
- Equipment-related batch failures are prevented through proactive qualification management
- GMP inspection findings related to equipment qualification are avoided

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Raw Material and Component Data Must Be Verified Before Use

### Qualified Name
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Domain Identifier
MANUFACTURING

### Summary
Every raw material and component used in manufacturing must be received, tested, and approved in accordance with GMP requirements, with data verified against approved specifications before release for use in production.

### Description
GMP regulations require that starting materials — active pharmaceutical ingredients (APIs), excipients, and packaging components — are only used in production after they have been tested and approved to meet their specifications. Receipt data (supplier, lot number, quantity, condition on receipt), identity testing results, full specification test results, and approval status must all be captured before a material is released for production use. For on-demand personalised manufacturing, where patient-specific materials may have been specifically sourced or prepared, this verification is critical to patient safety. The source of each material must be traced back to an approved supplier, and any material from an unapproved or unqualified source must be quarantined and rejected. Material data must link to the batch record for every batch in which the material is used.

### Implications
- A quarantine and release process must govern all incoming materials before they enter production
- Identity testing must be conducted on every container of incoming API, not just on a sample
- Material data must be entered into inventory systems contemporaneously on receipt
- Approved supplier lists must be maintained and used to verify that materials come from qualified sources

### Outcomes
- No out-of-specification or unqualified material enters the manufacturing process
- Every batch record can trace its materials to tested, approved, and supplier-qualified lots
- Patient safety risk from contaminated or counterfeit starting materials is minimised

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Computerised Manufacturing Systems Must Comply with Electronic Records Requirements

### Qualified Name
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Domain Identifier
MANUFACTURING

### Summary
All computerised systems used in GMP-regulated manufacturing must be validated, have audit trails enabled, control access by individual user identity, and meet the requirements of EU GMP Annex 11 and FDA 21 CFR Part 11.

### Description
Computerised systems — including Manufacturing Execution Systems (MES), LIMS, building management systems, and electronic batch record systems — are now central to pharmaceutical manufacturing at Coco Pharmaceuticals. EU GMP Annex 11 and FDA 21 CFR Part 11 impose specific requirements on these systems: they must be validated before use in production; audit trails must record who created, modified, or deleted GMP data and when; access must be controlled by unique user identifiers with role-appropriate permissions; electronic signatures must be attributable to the individual signing and must not be transferable; data must be backed up regularly with backup integrity verified; and systems must be protected from unauthorised access. These requirements apply equally to systems operated in-house and to cloud-based or third-party systems holding GMP data on behalf of Coco Pharmaceuticals.

### Implications
- All computerised systems used in GMP activities must have a Validation Master Plan and individual system validation documentation
- Audit trail configuration must be reviewed as part of system validation and must not be disabled in production
- User access reviews must be conducted regularly; access for leavers must be removed promptly
- Cloud and third-party GMP systems must be covered by a Technical Agreement and the vendor's quality management system must be assessed

### Outcomes
- Electronic manufacturing records satisfy the requirements of EU GMP Annex 11 and FDA 21 CFR Part 11
- Data integrity of electronic records can be demonstrated to regulatory inspectors
- Audit trails provide a complete history of GMP data for investigation purposes

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Chain of Identity Must Be Unbroken from Sample to Administration

### Qualified Name
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Domain Identifier
MANUFACTURING

### Summary
For every personalised product, the link from the patient's starting material through manufacture and testing to administration must be verifiable at each handover, with any break stopping the batch.

### Description
Chain of identity is the personalised-manufacturing counterpart of batch traceability, and it carries a consequence traceability does not: a break is not a documentation problem to be investigated later but an immediate patient safety event, because a product that cannot be confidently matched to its patient cannot be administered to anyone. The obligation requires verification at every handover — collection to logistics, logistics to manufacturing, through each production step, release to distribution, and delivery to the treating site — with each verification recorded against the reference and attributed to the person performing it. Automated verification is preferred at every point where it is possible, since the failure mode is a human confirming a match that does not hold. A break, or an inability to demonstrate the link, quarantines the batch pending investigation, and where the link cannot be re-established the product is destroyed rather than administered. This obligation coexists with the identity minimisation principle without conflict: the chain is verified on the reference throughout, and only the final step at the treating site resolves the reference to the patient.

### Implications
- Every handover requires a recorded, attributed verification against the reference
- Verification should be automated wherever technically possible
- A break quarantines the batch immediately rather than raising a deviation for later review
- Where the link cannot be re-established the product is destroyed, not administered
- The chain is verified on the reference; only the treating site resolves it to the patient

### Outcomes
- No patient receives a product manufactured for someone else
- Chain integrity is demonstrable to inspectors as a continuous record rather than reconstruction
- Breaks are contained at the point they occur rather than discovered at administration

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Corrective and Preventive Actions Must Be Verified as Effective

### Qualified Name
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Domain Identifier
MANUFACTURING

### Summary
Every CAPA must define in advance how its effectiveness will be measured, and must remain open until that measurement demonstrates the problem has not recurred.

### Description
Closing a deviation records that an incident was investigated; a CAPA is the separate commitment that it will not happen again, and inspectors examine the two as distinct systems. The failure mode this obligation addresses is the CAPA closed on completion of the action rather than on evidence of its effect — retraining delivered, procedure revised, box ticked — which is why the same deviation recurs and why repeat findings are among the most common inspection observations. The obligation therefore requires the effectiveness check to be defined when the CAPA is raised, not chosen afterwards when the available evidence is known, and requires it to be measurable against data rather than assessed by opinion. A CAPA stays open until the check period has elapsed and the measurement has been made. Where the check shows the action did not work, the CAPA is reopened and escalated rather than closed with a note, because a failed CAPA on a recurring problem is itself a quality system finding. Actions that amount only to retraining or to reminding operators are treated as weak by default and require justification, since they address the person rather than the system that permitted the error.

### Implications
- The effectiveness check and its measurement period must be defined at CAPA initiation
- CAPAs remain open until the check has been performed, not until the action is complete
- Effectiveness must be measured against data, not assessed by opinion
- Retraining-only actions are presumed weak and require documented justification
- A failed effectiveness check reopens and escalates rather than closing the CAPA

### Outcomes
- Recurrence of the same problem falls rather than persisting through repeated investigations
- Weak actions are identified before they are relied upon
- The quality system can demonstrate that its corrective mechanism actually corrects

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Batch Certification and Import Responsibility Must Match the Market Supplied

### Qualified Name
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Domain Identifier
MANUFACTURING

### Summary
Each batch must be certified by a Qualified Person operating under a manufacturing authorisation valid for the market it will supply, with import responsibility discharged separately where product crosses into Great Britain.

### Description
Before the UK left the EU a single Qualified Person certification covered release across the whole territory. It no longer does, and the consequence is structural rather than procedural: certification is now an act performed under a specific national authorisation for a specific market, and a batch certified under an EU manufacturing authorisation is not thereby released to the Great Britain market. Northern Ireland follows the EU regime through the Windsor Framework, so a single production run may need to be released twice under different authorisations depending on where each portion goes. Product entering Great Britain from an EU site additionally requires import responsibility to be discharged by a Responsible Person (Import) confirming that appropriate checks were carried out, which is a distinct role from the Qualified Person and cannot be assumed by them by default. The governance requirement is that market destination, the authorisation under which certification occurred, and the identity of the certifying QP or RPi are all recorded against the batch — so that the release position for any portion of any batch can be established without reconstructing it from correspondence. Certification data must reconcile with the serialisation market allocation, since a batch coded for one market and certified for another cannot lawfully be supplied to either without correction.

### Implications
- Certification is performed per market under the authorisation valid for that market
- A single production run may require multiple certifications for different destinations
- Great Britain import from an EU site requires a Responsible Person (Import), distinct from the QP
- Market, authorisation, and certifying person must be recorded against each batch portion
- Certification data must reconcile with serialisation market allocation

### Outcomes
- Product is supplied only to markets for which it was lawfully certified
- The release position of any batch portion is establishable from records
- Divergence between coding and certification is caught before supply

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Temperature Excursions Must Be Recorded and Assessed Before Product Disposition

### Qualified Name
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Domain Identifier
MANUFACTURING

### Summary
Continuous temperature data must be captured for every temperature-sensitive consignment, and any excursion must be assessed against the product's stability data by the quality organisation before the product is released, forwarded, or administered.

### Description
For temperature-sensitive product the storage and transport record is part of the evidence that the product is fit to use, and a gap in that record is equivalent to a gap in the batch record — the product cannot be shown to be within its validated conditions, and absence of evidence is treated as an excursion rather than as compliance. The obligation requires continuous monitoring rather than spot checks at handover, since a two-hour excursion between readings taken twelve hours apart is invisible to sampling. Excursions are assessed against the product's stability data, which means the assessment requires the cumulative excursion history for that batch and not only the current event: a product may tolerate one brief excursion and not three, and each leg of a journey assessed in isolation will approve a consignment the cumulative record would reject. Disposition is a quality decision, never an operational one taken by whoever received the consignment, and the assessment and its reasoning are recorded against the batch. The exposure grows with the portfolio: personalised and biological products have narrower tolerances and shorter usable lives, and for an autologous product there is no replacement stock.

### Implications
- Monitoring must be continuous; missing data is treated as an excursion, not as compliance
- Assessment must use cumulative excursion history for the batch, not the current event alone
- Disposition is a quality decision, not an operational one taken at the receiving site
- Assessment reasoning must be recorded against the batch and retained with it
- Personalised and biological products require tighter tolerances and have no replacement stock

### Outcomes
- Product administered to patients has a complete, assessed temperature history
- Cumulative excursion effects are caught rather than approved leg by leg
- Monitoring gaps in the logistics chain become visible and correctable

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.3 Governance Approaches

___

## Create Governance Approach

### Display Name
ALCOA+ Data Integrity Framework

### Qualified Name
CocoPharma::GovernanceApproach::ALCOAPlusFramework

### Domain Identifier
MANUFACTURING

### Summary
Coco Pharmaceuticals applies the ALCOA+ framework as the operational method for assessing, designing, and auditing manufacturing data governance controls across all GMP-regulated activities.

### Description
The ALCOA+ framework is used in three ways at Coco Pharmaceuticals. First, as a design tool: when new manufacturing data collection processes or systems are designed, each ALCOA+ element is considered explicitly — can the data be attributed? Is it being captured contemporaneously? Is the original value preserved? Second, as an audit tool: periodic data integrity self-inspections use ALCOA+ as a checklist to identify where controls are missing or insufficient. Third, as an investigation framework: when a data integrity concern is raised — whether through deviation, audit, or regulatory inspection — the investigation maps the concern against ALCOA+ elements to identify the root cause and appropriate corrective action. The approach is applied to both paper-based and electronic data capture processes, recognising that many manufacturing environments operate hybrid systems.

### Implications
- All manufacturing data system designs must be reviewed against ALCOA+ before implementation
- Data integrity self-inspections must be conducted on a defined frequency across all production areas
- Staff at all levels who generate or review manufacturing data must be trained on ALCOA+ principles
- Data integrity risk assessments must be documented for all GMP-critical data processes

### Outcomes
- Data integrity controls are consistently designed and applied across all manufacturing data processes
- Data integrity issues are detected internally before they are identified by regulators
- Manufacturing data meets the expectations of EMA, FDA, and MHRA data integrity guidance

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Electronic Batch Record Management

### Qualified Name
CocoPharma::GovernanceApproach::ElectronicBatchRecordManagement

### Domain Identifier
MANUFACTURING

### Summary
Manufacturing batch records are captured, reviewed, and archived electronically, using validated systems with audit trails, electronic signatures, and integration to the Egeria metadata catalog for governance linkage.

### Description
Coco Pharmaceuticals is transitioning from paper-based batch records to fully electronic batch records (EBRs) managed in a validated Manufacturing Execution System. The EBR approach enables: real-time data entry by operators with immediate validation against specifications; automatic capture of instrument data, reducing transcription errors; electronic review and approval workflow with attributable electronic signatures; integration with laboratory systems to pull in analytical results; and automatic flagging of out-of-specification values for immediate deviation initiation. The EBR system is integrated with the Egeria metadata catalog to enable batch records to be linked to the governance framework — each batch record is associated with the product's governance definitions, the applicable manufacturing process version, and the quality standards that apply. This supports both GMP compliance and the data-driven quality governance approach.

### Implications
- The EBR system must be validated to EU GMP Annex 11 and 21 CFR Part 11 requirements before it replaces paper records
- Integration interfaces to LIMS and other data sources must be validated and their data transfers verified
- A hybrid paper and electronic approach must be managed during the transition period
- Users must be trained on electronic data integrity requirements — the prohibitions on backdating and data manipulation apply equally to electronic systems

### Outcomes
- Batch records are captured with higher accuracy and completeness than paper-based systems allow
- Review and release timelines are shortened through electronic workflow
- Data integrity is strengthened by removing manual transcription steps and enabling real-time checks

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Manufacturing Change Control

### Qualified Name
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Domain Identifier
MANUFACTURING

### Summary
All changes to validated manufacturing processes, equipment, computerised systems, and supporting documentation must be assessed, approved, implemented, and verified through a formal change control process before the changed state is used in production.

### Description
GMP regulations require that changes to manufacturing processes, equipment, systems, and associated documentation are controlled. An uncontrolled change — however well-intentioned — can inadvertently compromise the validated state of a process or system, introduce data integrity vulnerabilities, or affect product quality in ways that are not immediately apparent. The manufacturing change control process at Coco Pharmaceuticals covers: proposal and impact assessment (including validation impact, regulatory impact, and data integrity impact); cross-functional review and approval; implementation planning; verification that the change has been correctly implemented; and update of all affected documentation, training records, and validation files. Emergency changes must go through an expedited process that still requires approval and is followed by a full retrospective review. Changes with regulatory implications must be submitted to authorities before implementation where required.

### Implications
- No change to a validated process, system, or procedure may be implemented without an approved change control record
- Change impact assessments must consider validation status, data integrity controls, and the need for regulatory notification
- CAPA actions from deviations and audits must be implemented through the change control process when they affect validated systems or procedures
- Change control records must link to the affected validation documentation, updated SOPs, and training records

### Outcomes
- The validated state of manufacturing processes and systems is protected from uncontrolled changes
- Regulatory compliance is maintained through appropriate notification of significant changes
- Data integrity controls are assessed and updated whenever processes or systems change

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Manufacturing Pseudonymisation for Personalised Products

### Qualified Name
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Domain Identifier
MANUFACTURING

### Summary
A reference is issued at the point the patient's starting material is collected and used as the sole patient identifier throughout manufacturing, with the mapping held clinically and access to it logged.

### Description
The approach defines where the reference is created, who holds the mapping, and how the boundary is enforced. The reference is issued at collection — the earliest possible point, so that no manufacturing system ever receives an identified record and there is no de-identification step that could be skipped. It is generated so as to carry no information about the patient, and it is registered in the clinical system alongside the patient record, which is where the mapping lives and where access to it is restricted to the treating team and logged. Manufacturing systems, including those operated by contract manufacturers, are configured so that patient identity fields are absent rather than blank, since a blank field invites completion. Requests to resolve a reference from the manufacturing side — which arise legitimately in recall, complaint investigation, and pharmacovigilance — go through a defined route in which the clinical side performs the resolution and returns only what the specific enquiry requires. The approach is reviewed with the privacy team, which assures the pseudonymisation is effective and that the residual disclosure through product type is assessed rather than overlooked.

### Implications
- The reference is issued at collection, so no manufacturing system holds an identified record
- Patient identity fields must be absent from manufacturing systems, not present and empty
- The mapping is held clinically with restricted, logged access
- Recall and pharmacovigilance resolution goes through a defined route, returning the minimum needed
- Privacy assures effectiveness, including the residual disclosure implied by product type

### Outcomes
- Manufacturing operates without ever receiving identified patient data
- Legitimate resolution needs are met without granting standing access
- The pseudonymisation can be evidenced as effective rather than asserted

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Corrective and Preventive Action Management

### Qualified Name
CocoPharma::GovernanceApproach::CAPAManagement

### Domain Identifier
MANUFACTURING

### Summary
CAPAs are raised from defined triggers, graded by risk, subjected to structured root cause analysis, and tracked to an effectiveness check, with the whole population trended to identify systemic weakness.

### Description
The approach defines when a CAPA is raised and what happens to it. Triggers are explicit rather than discretionary — recurring deviations, any critical deviation, adverse trends crossing defined limits, inspection observations, complaint patterns, failed effectiveness checks — because leaving the decision to judgement produces a system whose scope varies with workload. Each CAPA is graded, and the grade determines the depth of root cause analysis required, the seniority of approval, and the effectiveness check interval; not everything warrants a full structured investigation and treating everything as though it does is how backlogs form. Root cause analysis distinguishes the immediate cause from the systemic one, and the test applied is whether the proposed action would prevent recurrence in a comparable but non-identical situation — an action that would not is addressing the symptom. The CAPA population is trended as a whole, by originating system, area, and root cause category, since the pattern across CAPAs frequently identifies a weakness that no individual investigation would surface. Backlog and ageing are reported, because an overdue CAPA population is itself an inspection finding regardless of the merits of any individual item.

### Implications
- Trigger criteria must be explicit, not left to case-by-case judgement
- Risk grading determines analysis depth, approval level, and check interval
- Root cause must reach the systemic cause, tested against a comparable non-identical scenario
- The CAPA population must be trended by area and cause, not only managed case by case
- Backlog and ageing must be reported, since an overdue population is itself a finding

### Outcomes
- CAPA scope is consistent regardless of workload or individual judgement
- Effort is proportionate, so genuinely serious issues receive genuine analysis
- Systemic weaknesses visible only across cases are identified and addressed

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Continuous Cold Chain Monitoring and Excursion Management

### Qualified Name
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Domain Identifier
MANUFACTURING

### Summary
Temperature-sensitive consignments carry continuous monitoring from despatch to receipt, with data recovered into the batch record and excursions routed automatically to quality assessment rather than reported by the receiving site.

### Description
The approach addresses the two ways cold chain data is usually lost: monitors whose data is never recovered because the consignment arrived apparently fine, and excursions noticed by a receiving site that decides locally that the product looks acceptable. It requires monitoring data to be recovered and attached to the batch record as a condition of receipt rather than as an option exercised when something appears wrong, so that the cumulative history exists for every consignment. Excursion detection is automated against the product's defined limits and routed directly to the quality organisation, removing the local judgement that would otherwise stand between an excursion and its assessment. Monitor selection and placement are specified per product and route, since a device recording ambient air in a vehicle says little about the temperature inside a pallet, and validation of shipping configurations covers the routes and seasons actually used rather than a single qualification run. For personalised products the approach additionally requires real-time rather than retrospective monitoring, because there is no replacement stock and an intervention during transit may be the only way to save a product a patient is waiting for.

### Implications
- Monitoring data recovery is a condition of receipt, not an exception-driven activity
- Excursion detection is automated and routed to quality, bypassing local judgement
- Monitor selection and placement are specified per product and route
- Shipping configuration validation must cover actual routes and seasonal conditions
- Personalised products require real-time monitoring to permit intervention in transit

### Outcomes
- Every temperature-sensitive consignment has a recovered, complete monitoring record
- Excursions reach quality assessment regardless of how the product appears on arrival
- Transit problems affecting irreplaceable personalised product can be acted on in time

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — MANUFACTURING Domain

---

### 3.1 Governance Roles

___

## Create Governance Role

### Display Name
Manufacturing Governance Lead

### Qualified Name
CocoPharma::GovernanceRole::ManufacturingGovernanceLead

### Description
The Manufacturing Governance Lead is the domain lead responsible for the governance of manufacturing data and manufacturing data systems at Coco Pharmaceuticals. This role is accountable for defining and maintaining the manufacturing data governance framework, ensuring GMP compliance of manufacturing data practices, overseeing data integrity self-inspection programmes, and coordinating with the CDO on the integration of manufacturing data into the broader data governance program. The Manufacturing Governance Lead chairs the Manufacturing Data Governance Forum, which brings together Quality Assurance, Manufacturing Operations, and IT to maintain the governance framework as manufacturing processes evolve. In the current governance structure, the Head of Manufacturing holds this role.

### Scope
Manufacturing governance domain — all data generated, processed, or stored in GMP-regulated manufacturing activities, including batch records, deviation records, equipment qualification records, raw material records, and computerised manufacturing systems.

### Headcount
1

### Category
Governance Role

### Search Keywords
- manufacturing governance
- GMP data governance
- batch record governance
- data integrity

### Version Identifier
1.0

___

---

___

## Create Governance Role

### Display Name
Qualified Person

### Qualified Name
CocoPharma::GovernanceRole::QualifiedPerson

### Description
The Qualified Person (QP) is a mandatory role under EU GMP (Directive 2001/83/EC Article 48 and Annex 16) responsible for certifying that each batch of medicinal product has been manufactured and tested in accordance with the applicable regulations, the Marketing Authorisation, and GMP. At Coco Pharmaceuticals, the QP is the final human governance control before a batch of medicine is released for sale or supply. The QP must be personally satisfied that the batch record is complete and accurate, all deviations have been closed or assessed, in-process and finished product results are within specification, and all regulatory requirements have been met. The QP is a named individual who must hold the qualifications specified by EU GMP and be registered with the relevant national competent authority. The QP cannot be pressured to release a batch — their independence in the release decision is a regulatory requirement.

### Scope
Batch certification and release for all EU-regulated medicinal products manufactured by or on behalf of Coco Pharmaceuticals. The QP must have direct access to all manufacturing and quality data relevant to the certification decision.

### Headcount
2

### Category
Governance Role

### Search Keywords
- Qualified Person
- QP
- batch release
- GMP certification
- EU GMP

### Version Identifier
1.0

___

---

___

## Create Governance Role

### Display Name
Manufacturing Data Steward

### Qualified Name
CocoPharma::GovernanceRole::ManufacturingDataSteward

### Description
A Manufacturing Data Steward is a production area representative responsible for the day-to-day application of manufacturing data governance within their assigned manufacturing suite or production area. Each significant production area — including API processing, formulation, packaging, and quality control laboratories — has a designated Manufacturing Data Steward. This role monitors data integrity within the area, identifies data entry risks and errors before they reach the batch record review stage, supports the data integrity self-inspection programme, ensures operators are trained on current data integrity requirements, and acts as the first escalation point for data-related deviations and concerns. The Manufacturing Data Steward reports to the Manufacturing Governance Lead and works closely with the Quality Assurance team.

### Scope
Production-area level — each Manufacturing Data Steward is accountable for data governance in their assigned manufacturing area.

### Headcount
5

### Category
Governance Role

### Search Keywords
- manufacturing data steward
- data integrity
- production area governance
- GMP data

### Version Identifier
1.0

___

---

___

## Create Governance Role

### Display Name
Responsible Person (Import)

### Qualified Name
CocoPharma::GovernanceRole::ResponsiblePersonImport

### Description
The Responsible Person (Import) discharges the import responsibility for medicinal product entering Great Britain from an EU or other approved-country site, confirming that appropriate checks have been carried out on the batch and that it was certified by a Qualified Person under an authorisation recognised for that route. The role maintains the evidence supporting each import confirmation, verifies that the supplying site's authorisation remains current, and works with the Serialisation Data Manager to confirm that market allocation and certification are consistent for the consignment. It is a distinct role from the Qualified Person and is named on the relevant manufacturing and import authorisation; one person may hold both roles only where the authorisation permits it and the segregation of duties assessment supports it.

### Scope
Import of medicinal product into Great Britain from EU and other approved-country manufacturing sites — batch check confirmation, supplying site authorisation verification, and the evidence supporting each import.

### Headcount
2

### Category
Governance Role

### Search Keywords
- responsible person import
- batch certification
- Great Britain import
- manufacturing authorisation

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.2 Governance Metrics

___

## Create Governance Metric

### Display Name
Batch Record Completeness Rate

### Qualified Name
CocoPharma::GovernanceMetric::BatchRecordCompletenessRate

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of batch records that are submitted for Qualified Person review without any missing or incomplete GMP data entries.

### Description
This metric tracks the proportion of batch records that are submitted for QP review complete — meaning all mandatory data fields have been entered, all in-process results recorded, all deviations documented, and no blank, uncrossed, or unsigned entries remain. A batch record with missing data cannot be reviewed or released until the discrepancy is resolved; incomplete records cause delays and may indicate underlying data integrity weaknesses. The metric is calculated per batch and reported at the production area level and overall. Targets are set at 95% or above for initial implementation, rising to 98% as electronic batch record systems mature. Root causes of incomplete submissions are tracked by type to drive targeted improvement.

### Implications
- Requires a defined checklist of mandatory data fields for each batch record type
- Requires review of batch records at the point of area sign-off, before submission to QA review
- Incomplete records must be categorised by type of omission to enable trend analysis

### Outcomes
- QP review is not delayed by missing data
- Data completeness trends across production areas are visible and actionable
- The organisation can demonstrate a systematic approach to batch record data quality

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Deviation Closure Rate

### Qualified Name
CocoPharma::GovernanceMetric::DeviationClosureRate

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of manufacturing deviations that are closed — with documented investigation, root cause, and CAPA — within the defined timeframe for their classification.

### Description
Manufacturing deviations are classified as critical (must be closed within 5 working days), major (within 15 working days), or minor (within 30 working days). This metric tracks the proportion of deviations in each classification that are closed within the applicable timeframe. A deviation closure rate below target indicates resourcing, investigation quality, or CAPA implementation issues. All deviations must be closed before a batch manufactured during the deviation period can be presented for QP certification. Open deviations beyond their timeframe are escalated to the Manufacturing Governance Lead and Quality Director. Trend data — number, classification, production area, root cause category — is reviewed monthly and used in the annual Product Quality Review.

### Implications
- Requires a formal deviation tracking system with classification, owner, and due date fields
- Requires CAPA implementation and verification to be documented before a deviation can be closed
- Deviations affecting a batch must be linked to the batch record in the tracking system

### Outcomes
- Deviations are resolved promptly rather than accumulating as an unmanaged backlog
- Batch release is not delayed by overdue deviation investigations
- Root cause trend data drives systemic quality improvements

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Equipment Qualification Currency Rate

### Qualified Name
CocoPharma::GovernanceMetric::EquipmentQualificationCurrencyRate

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of GMP-critical manufacturing equipment and instruments that have current, valid qualification or calibration records and are within their scheduled review period.

### Description
This metric tracks what proportion of GMP-critical equipment is in a current, qualified state. Equipment is classified as: In-date (qualification and calibration current — counts toward the metric), Due for review within 30 days (flagged for action but still compliant), Overdue (must be taken out of service — counts against the metric), or Out of service for requalification (excluded from the calculation). The target is 100% of GMP-critical equipment either In-date or Flagged. Any Overdue equipment triggers an immediate notification to the Manufacturing Data Steward and Manufacturing Governance Lead. The metric is produced from the equipment qualification register, which must be kept current as a condition of GMP compliance. The register is reviewed monthly; approaching-overdue items are flagged 60 days in advance.

### Implications
- Requires a maintained qualification register covering all GMP-critical equipment
- Requires a defined review schedule for each equipment category
- Overdue equipment must have a documented decision: quarantine from production or emergency requalification

### Outcomes
- Manufacturing equipment is consistently maintained in a qualified state
- Regulatory inspection findings related to out-of-date qualification are avoided
- The organisation can demonstrate proactive qualification management

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
CAPA Effectiveness Verification Rate

### Qualified Name
CocoPharma::GovernanceMetric::CAPAEffectivenessRate

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of CAPAs whose effectiveness check passed at first verification, reported alongside recurrence of the problem the CAPA was raised to address.

### Description
The pass rate alone would be a poor measure, since it can be raised simply by choosing undemanding effectiveness checks. It is therefore reported against recurrence: the proportion of closed CAPAs where the originating problem has recurred within a defined window afterwards. A high pass rate combined with meaningful recurrence indicates that the checks are not testing what matters, which is a more useful finding than either figure alone. Reporting separates CAPAs by grade, since a weak effectiveness regime for critical CAPAs is a serious matter and would be concealed in an aggregate dominated by minor ones, and by action type, which reliably shows that retraining-only actions have the poorest effectiveness — evidence that supports treating them as weak by default rather than arguing the point case by case. CAPA ageing and backlog are reported alongside, because effectiveness statistics from a system with a large overdue population describe only the items that happened to be completed. Target is 90% first-check pass with recurrence below 5%.

### Implications
- Pass rate must be reported against recurrence, or undemanding checks will inflate it
- Reporting must separate CAPAs by grade and by action type
- Ageing and backlog must be reported alongside, as they condition the other figures
- Recurrence measurement requires the originating problem to be classified consistently

### Outcomes
- Ineffective corrective actions are identified from evidence rather than by argument
- The weakness of retraining-only actions is demonstrable
- Effectiveness figures cannot be improved by lowering the standard of the check

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Cold Chain Monitoring Data Completeness

### Qualified Name
CocoPharma::GovernanceMetric::ColdChainDataCompleteness

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of temperature-sensitive consignments arriving with a complete, recovered monitoring record covering the whole journey, with gaps and excursions reported separately.

### Description
Completeness is measured against the whole journey rather than against the existence of a monitoring file, because a record that starts an hour after despatch or ends at a distribution centre before the final leg does not establish that the product stayed within conditions. Gaps are reported by where in the chain they occur — origin site, primary transport, distribution centre handling, final leg — since each has a different owner and remedy, and final-leg gaps are the most common and the most consequential for personalised product going directly to a treating site. Excursions are reported separately from gaps and are not treated as a failure of this metric: an excursion detected, assessed, and dispositioned is the system working correctly, whereas a gap means no assessment was possible at all. Consignments handled by third-party logistics providers are reported distinctly, as the recovery depends on their processes. Target is 98% complete journey coverage, with 100% for personalised and other irreplaceable product.

### Implications
- Completeness is assessed across the whole journey, not by the presence of a file
- Gaps must be attributed to a chain segment to be actionable
- Excursions are reported separately and do not count as completeness failures
- Third-party logistics consignments must be reported distinctly
- Irreplaceable product requires full coverage, not a percentage target

### Outcomes
- Product cannot be dispositioned on an incomplete temperature history without that being visible
- Chain segments losing monitoring data are identified and their processes corrected
- Personalised product is not administered on an unverifiable storage record

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Chain of Identity Verification Integrity

### Qualified Name
CocoPharma::GovernanceMetric::ChainOfIdentityIntegrity

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of personalised batch handovers verified automatically against the reference without a manual override, and reports every chain break separately.

### Description
Two figures are reported and they answer different questions. The first is the proportion of handovers verified automatically without manual override, which measures how far the control depends on a person confirming a match rather than a system establishing one — overrides are where breaks originate, and a rising override rate is a leading indicator regardless of whether any break has yet occurred. Overrides are reported with their reason, since a recurring reason usually identifies a step where the automated verification does not fit how the work is actually done and will keep being overridden until the step is redesigned. The second figure is the count of chain breaks, reported individually rather than as a rate. A break is a patient safety event and averaging it into a percentage would be a category error: the target is zero, each occurrence is investigated in full, and a batch destroyed because its link could not be re-established is reported to the Manufacturing Governance Lead and the Qualified Person directly. Handovers involving contract manufacturers and logistics providers are reported separately, since those are the points where the chain leaves systems the company controls.

### Implications
- Manual overrides must be recorded with a reason and trended, as they precede breaks
- Chain breaks are reported as individual events, never as a rate
- Third-party handovers must be reported separately from internal ones
- A recurring override reason indicates a verification step that needs redesign, not more training

### Outcomes
- Dependence on human confirmation is visible and reducible
- Verification steps that do not fit the work are identified before they cause a break
- Every break receives individual investigation rather than being absorbed into a statistic

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Certification Type

___

## Create Certification Type

### Display Name
GMP Material Supplier Qualification

### Qualified Name
CocoPharma::CertificationType::GMPSupplierQualification

### Domain Identifier
MANUFACTURING

### Summary
The qualification a supplier of active ingredients, excipients, or primary packaging must hold before its material may be used in GMP manufacturing, confirming that it can consistently supply material meeting the agreed specification.

### Description
Qualification is the manufacturing-side assessment of a supplier, and it answers a different question from the commercial assessment: not whether the supplier is legitimate and solvent, but whether it can reliably produce material to specification under a quality system Coco Pharmaceuticals has examined. It is granted on the basis of a technical assessment covering the supplier's quality management system, its manufacturing and testing capability, its own supply chain for the material, and — for active ingredients — an audit of the manufacturing site, on site rather than on paper. A quality agreement recording specifications, testing responsibilities, change notification duties, and audit rights is a condition of qualification, since a supplier that changes its process without telling the company can invalidate the validated state of every product using the material. Qualification is material-specific and site-specific: a supplier qualified for one excipient from one plant is not thereby qualified for another. Status is reviewed periodically, on quality events, and on notified change, and may be suspended, which stops use of material not yet released while leaving material already incorporated to be assessed on its own evidence.

### Scope
Suppliers of active pharmaceutical ingredients, excipients, primary packaging, and contract manufacturing and testing services, assessed per material and per manufacturing site.

### Implications
- No material may be released for manufacturing use from an unqualified supplier or site
- Qualification is specific to material and site; it does not extend to other materials or plants
- A quality agreement with change notification duties is a precondition of qualification
- Active ingredient suppliers require an on-site audit, not a paper assessment
- Suspension stops future use and triggers assessment of material already incorporated

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.4 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to MANUFACTURING Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
GMP regulations across all jurisdictions require manufacturing data to be accurate, attributable, and traceable. The ALCOA+ framework is the industry's recognised operationalisation of those requirements.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Rationale
GMP traceability requirements — from raw material to finished product and forward into distribution — are a core GMP obligation. Full batch traceability is the governance principle that gives effect to this requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Rationale
GMP regulations require that manufacturing processes, equipment, and computerised systems are validated. Maintaining validated state throughout the operational life of processes and systems is the governance principle that ensures this obligation is continuously met.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Rationale
GMP Chapter 4 and US 21 CFR Part 211.188 directly require complete and accurate batch records. This obligation translates those regulatory requirements into a governance control.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Rationale
GMP regulations require that deviations from approved procedures are documented and investigated. This obligation operationalises that requirement with defined classification, investigation, and closure expectations.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Rationale
GMP requires equipment to be qualified before use and maintained in a qualified state. This obligation defines the governance controls — the qualification register, change control, and periodic review — that ensure continuous compliance.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Rationale
GMP Chapter 5 requires that starting materials are tested and approved before use in production. This obligation defines the governance controls — quarantine, testing, and approved supplier verification — that give effect to this requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUGMPAnnex11

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
EU GMP Annex 11 sets specific data integrity requirements for computerised systems. The ALCOA+ principle applies those requirements to both electronic and paper-based data capture in manufacturing.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUGMPAnnex11

### Policy
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Rationale
EU GMP Annex 11 requires computerised systems to be validated before use in GMP activities. The Validated State Maintained principle extends this requirement to cover the operational life of the system, not just initial validation.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUGMPAnnex11

### Policy
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Rationale
EU GMP Annex 11 is the primary source of the computerised systems obligation. This obligation translates Annex 11 requirements — validation, audit trails, access control, backup — into enforceable governance controls at Coco Pharmaceuticals.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
The business imperative for manufacturing data integrity is operationalised through the ALCOA+ principle, which sets the standard that all manufacturing data must meet.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Policy
CocoPharma::GovernanceApproach::ALCOAPlusFramework

### Rationale
The ALCOA+ framework is the primary approach through which the manufacturing data integrity imperative is applied in practice — as a design tool, audit tool, and investigation framework.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Policy
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Rationale
Patient-specific on-demand manufacturing requires each batch to be traceable to the individual patient's treatment record. Full batch traceability is foundational to the on-demand manufacturing model.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Policy
CocoPharma::GovernanceApproach::ElectronicBatchRecordManagement

### Rationale
On-demand manufacturing with smaller, more varied batches is only operationally viable with electronic batch records that capture data in real time and integrate with clinical and supply chain systems.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
Data errors are a primary cause of batch quality failures. The ALCOA+ principle defines the standard that manufacturing data must meet to prevent such failures.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Policy
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Rationale
Complete and accurate batch records are the primary safeguard against batch quality failures caused by data errors — errors in the record are identified and resolved before the release decision is made.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Policy
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Rationale
Systematically investigating deviations to root cause — including data-related deviations — prevents recurrence of the data errors that cause batch quality failures.

___

---

### 4.2 Governance Mechanisms — MANUFACTURING Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Mechanism
CocoPharma::GovernanceMetric::BatchRecordCompletenessRate

### Rationale
The batch record completeness rate directly measures whether this obligation is being met. A rate below target identifies production areas where data completeness controls need strengthening.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ElectronicBatchRecordManagement

### Mechanism
CocoPharma::GovernanceMetric::BatchRecordCompletenessRate

### Rationale
Electronic batch record management should improve completeness rates through real-time validation. The metric tracks whether the approach is delivering that improvement.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Mechanism
CocoPharma::GovernanceMetric::DeviationClosureRate

### Rationale
The deviation closure rate measures whether the investigation and closure obligation is being met within defined timeframes. Low closure rates signal resourcing or process issues in the deviation management system.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Mechanism
CocoPharma::GovernanceMetric::EquipmentQualificationCurrencyRate

### Rationale
The equipment qualification currency rate directly measures whether the qualification obligation is being met — whether all GMP-critical equipment has current, valid qualification and calibration records.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Mechanism
CocoPharma::CertificationType::GMPSupplierQualification

### Rationale
Verification before use presupposes that the source was assessed. Qualification is the control that establishes the supplier can meet specification consistently, rather than confirming one delivery did.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Mechanism
CocoPharma::CertificationType::GMPSupplierQualification

### Rationale
A supplier changing its process without notification can invalidate the validated state of every product using the material. The change notification duty in the quality agreement is a qualification condition for that reason.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Policy
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Rationale
The exposure arises because manufacturing holds identity it does not need. Replacing identity with a reference removes the exposure at source rather than restricting access to it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Policy
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Rationale
Issuing the reference at collection means no manufacturing system ever receives an identified record, so there is no de-identification step that can be omitted under time pressure.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Policy
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Rationale
On-demand personalised manufacture is only safe if every product can be matched with certainty to the patient it was made for. Chain of identity is the control that makes the capability deliverable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Rationale
The corporate transition to personalised medicine brings patient data into manufacturing for the first time. Identity minimisation is how that is absorbed without extending health data exposure across the plant.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Rationale
GMP requires that product can be traced and that mix-up is prevented. For personalised products those two requirements converge into a single chain that must never break.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Mechanism
CocoPharma::GovernanceMetric::ChainOfIdentityIntegrity

### Rationale
Automated verification rate and individual break reporting together measure the obligation, separating the leading indicator from the safety event.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Mechanism
CocoPharma::GovernanceMetric::ChainOfIdentityIntegrity

### Rationale
Verification operates on the reference the approach issues, so override trends reveal where the pseudonymised chain does not fit the physical process.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAcGMP

### Policy
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Rationale
Part 211 requires unexplained discrepancies and batch failures to be investigated, and FDA treats recurrence of a previously corrected problem as evidence that the quality system does not work. Effectiveness verification is what distinguishes correction from closure.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAcGMP

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Rationale
Data integrity findings are among the most frequent FDA citations against pharmaceutical manufacturers, and the out-of-specification expectations constrain how results may be treated rather than how product is made.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAcGMP

### Policy
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Rationale
Part 211 sets its own retention requirement of one year past expiry, which runs alongside the longer EU periods; the batch record obligation is met against the longest applicable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Rationale
GMP requires a functioning corrective and preventive action system as part of the pharmaceutical quality system, assessed as a system in its own right rather than through individual deviations.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Rationale
Qualified Person certification under a valid manufacturing authorisation is the act that permits release, and post-Brexit that authorisation is market-specific.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Policy
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Rationale
For temperature-sensitive product an incomplete storage record is a data error with the same consequence as a wrong batch record entry: the product cannot be shown fit for use.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Rationale
Personalised products have narrow tolerances, short usable lives, and no replacement stock, so real-time monitoring that permits intervention during transit becomes a patient supply control rather than a documentation one.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Policy
CocoPharma::GovernanceApproach::CAPAManagement

### Rationale
The imperative depends on problems being genuinely fixed rather than repeatedly investigated. Structured root cause work and population trending are how systemic data integrity weaknesses are found.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Mechanism
CocoPharma::GovernanceMetric::CAPAEffectivenessRate

### Rationale
First-check pass rate read against recurrence measures the obligation as written and prevents the standard being met by choosing undemanding checks.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::CAPAManagement

### Mechanism
CocoPharma::GovernanceMetric::CAPAEffectivenessRate

### Rationale
Grade and action-type breakdowns tell the approach whether its risk grading is calibrated and which action types are worth discouraging.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Mechanism
CocoPharma::GovernanceMetric::ColdChainDataCompleteness

### Rationale
Assessment is impossible without a complete record, so completeness by chain segment is the precondition the metric measures rather than the excursion rate itself.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Mechanism
CocoPharma::GovernanceMetric::ColdChainDataCompleteness

### Rationale
Recovery as a condition of receipt is what the metric tests; gaps by segment show where the condition is not being enforced.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Mechanism
CocoPharma::CertificationType::GMPSupplierQualification

### Rationale
Certification for a market presupposes that the materials used came from suppliers qualified for that product, since an unqualified source invalidates the basis on which the QP certifies.

___

---

### 4.3 Peer Driver Links — Related MANUFACTURING Drivers

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Governance Driver 2
CocoPharma::Regulation::GoodManufacturingPractice

### Description
GMP is the regulatory expression of the same need that the Manufacturing Data Integrity imperative captures as a business goal. Both demand trustworthy, traceable manufacturing data — one from a regulatory obligation perspective, the other from a business performance and patient safety perspective.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Governance Driver 2
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Description
On-demand manufacturing capability is the manufacturing expression of the broader personalised medicine transition. The personalised medicine imperative (defined in `joint-governance-officer-definitions.md`) creates the demand; on-demand manufacturing capability is how manufacturing responds.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::EUGMPAnnex11

### Governance Driver 2
CocoPharma::Regulation::GoodManufacturingPractice

### Description
EU GMP Annex 11 is a supplement to the main GMP regulations, applying specific requirements to computerised systems. The two regulations must be read and applied together for any manufacturing site using computerised systems.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Governance Driver 2
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Description
The batch quality failure threat is the negative expression of the manufacturing data integrity imperative. Achieving the imperative mitigates the threat; failing to achieve it materialises the threat.

___

---

### 4.4 Peer Policy Links — Related MANUFACTURING Policies

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Governance Policy 2
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Description
Deviation closure records that an incident was investigated; CAPA effectiveness records that it will not recur. Inspectors assess them as separate systems, and a well-run deviation process with a weak CAPA process produces exactly the pattern of recurring findings that attracts attention.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Governance Policy 2
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Description
For personalised product both controls guard the same consignment and both can render it unusable — one because it cannot be matched to its patient, the other because it cannot be shown to have stayed in condition. Neither has replacement stock to fall back on.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::CAPAManagement

### Governance Policy 2
CocoPharma::GovernanceApproach::ControlsTestingAndCertificationCycle

### Description
Both are systems for finding and closing weaknesses on a cycle, and both fail the same way — closure on completion of the action rather than on evidence of effect. The corporate controls cycle and the manufacturing CAPA system share that lesson without sharing a population.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::FDAcGMP

### Governance Driver 2
CocoPharma::Regulation::GoodManufacturingPractice

### Description
The US and EU cGMP regimes overlap substantially and both apply to the same sites, since UK and EU plants supplying the US market are subject to FDA inspection alongside their local regulators. Controls are designed once against the stricter requirement on each point rather than maintained as two parallel systems.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::FDAcGMP

### Governance Driver 2
CocoPharma::Regulation::EUGMPAnnex11

### Description
Annex 11 and FDA 21 CFR Part 11 address computerised systems from the same premise and differ in detail. A single validation and audit trail approach satisfies both where it is designed against the stricter of the two.

___

---



___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Governance Policy 2
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Description
Both apply the same reasoning in adjacent domains: the people handling the data need a reference rather than an identity, and protection is designed into collection rather than applied at disclosure. Personalised manufacture extends the trial principle into the plant.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Governance Policy 2
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Description
Traceability answers what went into a batch and where it went; chain of identity answers whose batch it is. For personalised products the second is the stricter requirement, because a break makes the product unusable rather than merely undocumented.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Governance Policy 2
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Description
The reference-to-patient mapping sits clinically while manufacturing may be performed by another group entity or a contract manufacturer, so the controllership determination establishes who holds what and on whose instruction.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
A personalised batch crossing a border carries a reference rather than an identity, which reduces but does not remove the transfer question — the chain of identity records themselves relate to an identifiable person and move with the product.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Governance Driver 2
CocoPharma::Threat::UnauthorisedDataDisclosure

### Description
Personalised batch exposure is a specialised form of unauthorised disclosure in which no control is breached: the data is disclosed to manufacturing staff by the ordinary operation of the process, which is why the mitigation is to remove the data rather than to restrict access to it.

___

---


___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Governance Policy 2
CocoPharma::GovernanceApproach::ALCOAPlusFramework

### Description
The principle defines the standard all manufacturing data must meet; the framework defines the process by which that standard is applied — in system design, self-inspection, and investigation. The principle without the framework is aspiration; the framework without the principle has no target.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Description
Maintaining validated state requires that changes are controlled. The change control approach is the primary operational mechanism through which the validated state principle is protected.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Governance Policy 2
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Description
Full batch traceability depends on complete and accurate batch records. If batch records are incomplete, traceability is broken. The two policies are mutually reinforcing — traceability sets the standard; the batch record obligation defines the control.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Description
CAPA actions arising from deviation investigations are implemented through the change control process. Deviations identify what needs to change; change control governs how those changes are made safely.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Governance Policy 2
CocoPharma::GovernanceApproach::ElectronicBatchRecordManagement

### Description
The electronic batch record approach relies on computerised systems meeting the EU GMP Annex 11 and 21 CFR Part 11 requirements set out in the computerised systems obligation. The approach cannot be implemented without the underlying compliance controls.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Mechanism
CocoPharma::CertificationType::GMPSupplierQualification

### Rationale
GMP qualification and commercial approved third-party status are two assessments of one supplier answering different questions — technical capability against specification, and legitimacy against fraud and bribery exposure. Both are required before transacting, and a supplier may hold one and fail the other.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Mechanism
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Rationale
For material suppliers the commercial approval and the GMP verification are two assessments of one relationship. Neither alone permits transacting, and a supplier may pass one and fail the other.

___

---

## Part 5: External Reference Links — MANUFACTURING Domain

___

## Link External Reference

### Element Name
CocoPharma::Regulation::EUGMPAnnex11

### External Reference
CocoPharma::ExternalReference::EMA::GMPGuidelines

### Description
EudraLex Volume 4 contains EU GMP Annex 11 — Computerised Systems. This is the primary regulatory source for the computerised systems requirements referenced by this governance driver.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GoodManufacturingPractice

### External Reference
CocoPharma::ExternalReference::Egeria::GovernanceProgramGuide

### Description
Egeria's governance program planning guide describes the framework used to structure manufacturing governance definitions and link them to the metadata catalog.

___

---

## Part 6: Manufacturing Governance Folio

A folio is a collection of governance definitions that a specific role is responsible for. The Manufacturing Governance Lead folio collects all manufacturing-domain governance definitions owned by Stew Faster.

---

### 6.1 Folio Definition

___

## Create Folio

### Display Name
Manufacturing Governance Lead — Governance Folio

### Qualified Name
CocoPharma::Folio::ManufacturingGovernanceLead

### Description
The governance definitions owned by the Manufacturing Governance Lead (Stew Faster). This folio covers the manufacturing governance domain: the manufacturing data integrity imperative, on-demand manufacturing capability, batch quality failure threat, EU GMP Annex 11 regulation, manufacturing principles (ALCOA+, batch traceability, validated state), obligations (batch records, deviations, equipment qualification, raw materials, computerised systems), approaches (ALCOA+ framework, electronic batch records, change control), governance roles, and metrics.

### Purpose
Provides Stew Faster with a single view of all manufacturing governance definitions he is responsible for authoring, maintaining, and enforcing. The folio supports GMP inspection readiness by making the manufacturing governance framework visible and linked in the Egeria metadata catalog.

### Category
Governance Folio

### Authors
- Stew Faster
- Florence Paynter
- George Pie

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ManufacturingGovernanceLead

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ManufacturingGovernanceLead

### Description
Assigns the Manufacturing Governance Lead role responsibility for all governance definitions collected in the Manufacturing Governance Lead Governance Folio.

___

---

### 6.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Membership Rationale
Stew Faster is accountable for ensuring all manufacturing data meets the accuracy, completeness, and traceability standards required by GMP regulations and by the business.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Membership Rationale
Stew Faster is accountable for developing the data and governance infrastructure that will enable Coco Pharmaceuticals to deliver patient-specific on-demand manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Membership Rationale
As head of manufacturing, Stew Faster is accountable for the controls that prevent batch quality failures arising from data errors.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::EUGMPAnnex11

### Membership Rationale
Stew Faster is accountable for compliance with EU GMP Annex 11 across all computerised systems used in manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::GoodManufacturingPractice

### Membership Rationale
GMP compliance is the primary regulatory obligation of the manufacturing function. Stew Faster is the domain lead accountable for GMP data governance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Membership Rationale
Stew Faster authored and champions the ALCOA+ data integrity principle as the standard for all manufacturing data quality at Coco Pharmaceuticals.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Membership Rationale
Full batch traceability is a core GMP requirement and a manufacturing governance principle for which Stew Faster is accountable.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::ValidatedStateMaintained

### Membership Rationale
Maintaining the validated state of manufacturing processes, equipment, and systems is a core accountability of the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Membership Rationale
Stew Faster is accountable for ensuring that complete and accurate batch records are produced for every batch manufactured.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Membership Rationale
The head of manufacturing is accountable for the deviation management programme and for ensuring deviations are investigated and closed within defined timeframes.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Membership Rationale
Stew Faster is accountable for ensuring all GMP-critical manufacturing equipment is qualified and calibrated to a current standard.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Membership Rationale
Ensuring that raw materials are tested and approved before use in production is a core manufacturing data governance obligation for which Stew Faster is accountable.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Membership Rationale
Stew Faster is accountable for ensuring all computerised systems used in manufacturing meet EU GMP Annex 11 and 21 CFR Part 11 requirements.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::ALCOAPlusFramework

### Membership Rationale
Stew Faster owns the ALCOA+ data integrity framework as the operational approach for assessing, designing, and auditing manufacturing data governance controls.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::ElectronicBatchRecordManagement

### Membership Rationale
The head of manufacturing is accountable for the transition to electronic batch records and for ensuring the approach meets GMP data integrity requirements.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Membership Rationale
Stew Faster owns the manufacturing change control process, which protects the validated state of processes, equipment, and systems from uncontrolled changes.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::BatchRecordCompletenessRate

### Membership Rationale
Stew Faster uses this metric to monitor data completeness across production areas and to drive improvement in batch record quality.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::DeviationClosureRate

### Membership Rationale
As head of manufacturing, Stew Faster is accountable for the timely investigation and closure of all manufacturing deviations within the defined classification timeframes.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::EquipmentQualificationCurrencyRate

### Membership Rationale
Stew Faster reports this metric to demonstrate that all GMP-critical equipment is maintained in a current, qualified state and that no production is being carried out on unqualified equipment.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::CertificationType::GMPSupplierQualification

### Membership Rationale
Supplier qualification is granted, suspended, and withdrawn by the Manufacturing Governance Lead through the quality organisation, and pairs with the corporate approved third-party status.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Membership Rationale
Patient data entering manufacturing through personalised production is a manufacturing exposure owned by the Manufacturing Governance Lead, assessed jointly with the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Membership Rationale
The boundary between reference and identity is set and enforced within manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Membership Rationale
Chain of identity is a manufacturing patient-safety control owned by the Manufacturing Governance Lead and the Qualified Person.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Membership Rationale
The pseudonymisation model is operated by manufacturing with effectiveness assured by the privacy team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::ChainOfIdentityIntegrity

### Membership Rationale
Override trends and chain breaks are reported to the Manufacturing Governance Lead and the Qualified Person.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::FDAcGMP

### Membership Rationale
US cGMP applies to every site supplying the US market, including the UK and EU plants, and is owned by the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::CAPAEffectivenessVerified

### Membership Rationale
CAPA effectiveness is a manufacturing quality system obligation assessed directly at inspection.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Membership Rationale
Certification per market and import responsibility are discharged by the Qualified Person and Responsible Person (Import) within manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Membership Rationale
Excursion assessment is a quality disposition decision owned by the manufacturing quality organisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::CAPAManagement

### Membership Rationale
The CAPA system is operated by manufacturing quality assurance under the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Membership Rationale
Cold chain monitoring is specified and operated by manufacturing, including for third-party logistics legs.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::CAPAEffectivenessRate

### Membership Rationale
CAPA effectiveness and recurrence are reported to the Manufacturing Governance Lead and reviewed in the product quality review.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::ColdChainDataCompleteness

### Membership Rationale
Monitoring completeness by chain segment is reported to the Manufacturing Governance Lead and the Qualified Person.

### Membership Status
VALIDATED

___

---

### 6.3 Root Collection Membership

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Membership Rationale
The Manufacturing Governance Lead folio is part of the Coco Pharmaceuticals governance folios collection, making it discoverable alongside the other domain governance folios.

### Membership Status
VALIDATED

___

---

## Part 7: Corporate Regulation Library Membership

The regulations defined in this file are placed in the Corporate Regulation Library so that they are discoverable alongside every other regulation the company is subject to, independently of the governance domain that owns them. The library folders are defined outside this workbook.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Pharmaceutical Manufacturing Regulations

### Element Id
CocoPharma::Regulation::EUGMPAnnex11

### Membership Rationale
Annex 11 is part of the EU GMP framework and sits with the other pharmaceutical industry regulations; the parent GMP regulation is already a member.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Pharmaceutical Manufacturing Regulations

### Element Id
CocoPharma::Regulation::FDAcGMP

### Membership Rationale
US cGMP applies to every site supplying the US market and belongs with the pharmaceutical manufacturing regulations.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `joint-governance-officer-definitions.md` | Foundation governance definitions — GMP regulation (CocoPharma::Regulation::GoodManufacturingPractice), EachInformationCollectionHasDesignatedOwner obligation, and MetadataDrivenGovernance approach |
| `data-governance-program.md` | DATA-domain governance definitions including data quality obligations and metrics |
| `privacy-governance-program.md` | PRIVACY-domain governance definitions — relevant for handling patient data in personalised manufacturing |
| `3. sustainability/sustainability-governance-definitions.md` | Sustainability domain definitions — relevant to manufacturing energy and emissions data |
