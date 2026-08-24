# Coco Pharmaceuticals — Personalised Batch Data Is Personal Data

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Works through the privacy consequences of manufacturing a medicine for one identified patient, tracing the material and its data from collection to administration, showing which governance definitions apply at each step, and adding the privacy-side definitions the scenario surfaces that no single domain had reason to write. Load the whole of `0. data-governance-program` and `data-processing-purposes.md` first.

---

## The situation

Conventional pharmaceutical manufacture has no privacy dimension worth the name. A batch of ten thousand tablets is made for nobody in particular; the only personal data in the batch record belongs to the operators who signed it, held for employment and GMP reasons that are well understood.

Autologous cell therapy inverts this completely. The batch exists because a named individual needs it. Its starting material is that individual's own cells. It is made to a schedule set by their treatment plan, it cannot be given to anyone else, and if it fails there is no replacement stock — only the patient, waiting, while another collection is arranged if they are well enough.

Everything that makes this therapy work also makes the batch record a health record. And because the batch record is a GMP document, it is subject to a set of requirements written on the assumption that the identities inside it belong to employees.

**This scenario is where three governance regimes meet on one vessel**, and none of them was written with the others in mind:

- **GMP** requires the batch record to be complete, attributable and retained, and does not contemplate deleting parts of it on request.
- **Data protection** gives the patient rights over their personal data, including rights the GMP record cannot honour.
- **Contained use** applies because the material is genetically modified, bringing a notification duty and a containment classification that follow the vessel wherever it goes.

The work below traces the journey, identifies where each collision occurs, records which definitions already cover it, and adds the three that were missing.

---

## Part 1: The journey, and what applies at each step

### 1. Collection

The patient's cells are collected at a treating site. At this moment the material is unambiguously identified — it is taken from a named person by clinicians who know them.

The reference is issued **here**, at the earliest possible point, and this is the single most consequential design decision in the whole scenario. Issuing it at collection means no manufacturing system ever receives an identified record, so there is no de-identification step that can be rushed, skipped, or performed incorrectly under time pressure. Every later control depends on this one having happened.

*Applies:* `GovernanceApproach::ManufacturingPseudonymisation` · `GovernancePrinciple::PatientIdentityMinimisedInManufacturing` · `DataProcessingPurpose::PersonalisedManufacturing`

### 2. Transport to the manufacturing site

The material moves, often by air, on a clock. It is simultaneously a consignment requiring dangerous goods declaration as a biological substance, a genetically modified organism under contained use, a temperature-controlled shipment, and health data about an identified patient in the hands of a courier.

Four regimes, one box. The courier is a processor receiving pseudonymised health data and needs an Article 28 agreement saying so.

*Applies:* `GovernancePrinciple::TimeCriticalShipmentsPlanned` · `GovernancePrinciple::ShipperOwnsClassification` · `GovernanceApproach::ColdChainMonitoring` · `GovernanceObligation::ContainedUseNotified` · `GovernanceObligation::DataProcessingAgreementsRequired`

### 3. Manufacture

Production staff work on material identified only by its reference. They know this batch is for that reference and must not be confused with another — which is what patient safety actually requires — and they do not know who the patient is, which is what privacy requires. The two requirements turn out to be compatible, but only because the reference was designed to carry no information about the individual.

The residual exposure is real and cannot be designed away: for a targeted therapy, knowing which product a batch is discloses the condition. Pseudonymisation reduces the exposure; it does not eliminate it.

*Applies:* `Threat::PersonalisedBatchPatientExposure` · `GovernanceObligation::ChainOfIdentityUnbroken` · `GovernanceObligation::BiologicalAgentsClassified` · `GovernancePrinciple::ClassificationTravelsWithData`

### 4. Release and the batch record

The Qualified Person certifies the batch. The record is now a GMP document that must remain complete and attributable for its retention period — and it contains the reference, which is personal data in the hands of anyone holding the mapping.

*Applies:* `DataProcessingPurpose::BatchRecordAttribution` · `GovernanceObligation::BatchCertificationPerMarket` · `GovernanceObligation::PersonalDataRetentionSchedulesDefined`

### 5. Return transport and administration

The product returns to the treating site, and at the final step the reference is resolved back to the patient — by clinical staff, with a treating relationship, at the only point in the journey where re-identification is necessary and appropriate.

*Applies:* `GovernanceObligation::ChainOfIdentityUnbroken` · `GovernanceMetric::ChainOfIdentityIntegrity`

### 6. Afterwards, for decades

The batch record is retained. The mapping is retained, because a recall or a safety signal years later must reach the people who received the product. If the patient later asks for their data to be erased, the answer is partly no — and that answer needs to have been decided, written down, and explained to them at consent rather than improvised when the request arrives.

*Applies:* the three definitions added below.

---

## Part 2: What the scenario surfaces

Tracing the journey exposes three gaps that no single domain had reason to notice. Each sits in the privacy domain, because each concerns the patient's position rather than the manufacturing process.

### 2.1 Governance Obligations

___

## Create Governance Obligation

### Display Name
The Reference-to-Patient Mapping Must Be Held Clinically with Logged Access

### Qualified Name
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Domain Identifier
PRIVACY

### Summary
The mapping between a manufacturing reference and the patient it belongs to must be held in clinical systems under clinical access controls, with every resolution logged and attributable, and no standing access granted to manufacturing.

### Description
Pseudonymisation protects the patient only for as long as the mapping stays separate from the data it pseudonymises, and the pressure to weaken that separation is constant and reasonable-sounding. A production manager wants to answer a query about a delayed batch. A quality investigator wants to understand a deviation. A commercial team wants to know which hospital to notify. Each request is legitimate in intent and each, if satisfied by granting access to the mapping, dissolves the control. The obligation therefore places the mapping in clinical systems under clinical access controls, and requires resolution requests from outside the treating relationship to go through a defined route in which the clinical side performs the resolution and returns only what the specific enquiry needs — a hospital name rather than a patient identity, a confirmation rather than a record. Every resolution is logged with requester, reason and what was returned, because a mapping accessed without record is a mapping that cannot be shown to have been used properly. Standing access is not granted to manufacturing under any circumstance, including during an incident, when the pressure is greatest and the temptation strongest.

### Implications
- The mapping is held in clinical systems, never replicated into manufacturing systems
- Resolution requests from outside the treating relationship follow a defined route
- Resolution returns the minimum the enquiry requires, not the underlying record
- Every resolution is logged with requester, reason, and what was returned
- No standing access is granted to manufacturing, including during incidents

### Outcomes
- Pseudonymisation continues to protect the patient in practice and not only in design
- Legitimate operational enquiries are answered without dissolving the control
- The use of the mapping can be demonstrated and audited

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Limits on Erasure Must Be Documented Before They Are Relied On

### Qualified Name
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Domain Identifier
PRIVACY

### Summary
Every category of personal data the company will refuse to erase must be recorded in advance with the legal basis for the refusal, the retention period it applies for, and the wording used to explain it to the individual at the point of collection.

### Description
The company holds several categories of personal data it cannot erase on request, and they have accumulated one domain at a time without anyone assembling the list. GMP batch records cannot lose their attribution. Health surveillance and exposure records are retained for forty years by statute. Consent evidence survives the erasure of the data it authorised. Clinical trial data already used in a submission analysis stays. The reference-to-patient mapping is retained for recall and pharmacovigilance. Each position is defensible and each was reasoned about carefully by the domain that holds the data — but a data subject request does not arrive addressed to a domain. It arrives at the privacy team, with a one-month clock, and is answered well or badly depending on whether the position had been worked out beforehand. This obligation requires the positions to be registered in advance: what category, what basis, how long, and — the part most often missing — the wording used to tell the individual at the point of collection that this is how it will be. A refusal explained at consent is a term of the relationship; the same refusal explained for the first time in response to a request reads as the company inventing a reason.

### Implications
- Each refusal category records the data, the legal basis, the retention period, and the consent wording
- The register is assembled from every domain rather than maintained only by privacy
- Consent and privacy notices must carry the wording before the data is collected
- New retention obligations must add to the register when they are created, not when they are tested
- A category absent from the register is answered as erasable

### Outcomes
- Data subject requests touching retained records are answered accurately within the deadline
- Individuals learn the limits at consent rather than at refusal
- The company's refusals are consistent across domains and defensible to a supervisory authority

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.2 Governance Approaches

___

## Create Governance Approach

### Display Name
Joint Privacy and Manufacturing Review for Personalised Therapies

### Qualified Name
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Domain Identifier
PRIVACY

### Summary
Each personalised therapy is reviewed jointly by privacy, manufacturing and the biological safety function before first patient collection, assessing the whole journey rather than each domain's segment of it.

### Description
The collisions in this scenario occur at the handovers, which is precisely where a review conducted domain by domain cannot see them. Manufacturing assesses the process, privacy assesses the processing, biological safety assesses the containment, and a courier carrying a genetically modified organism containing a patient's cells across a border under a time constraint falls into the space between the three. The approach therefore reviews the journey once, with all three present, before the first collection: where identity exists and where it does not, who holds the mapping, which processors touch the material, which borders it crosses and under what mechanism, what happens when a shipment is delayed or diverted, and what the patient is told at consent. It produces a single record covering the therapy end to end rather than three assessments that each stop at a boundary. The privacy impact assessment for the therapy is conducted within it rather than alongside, since running them separately reproduces the fragmentation the approach exists to remove. Reviews are repeated when the manufacturing route changes, when a new site or courier enters the chain, or when the therapy moves into a new market.

### Implications
- The review covers the journey end to end, including the handovers between domains
- Privacy, manufacturing and biological safety participate together, not sequentially
- The privacy impact assessment is conducted within the review rather than alongside it
- Failure scenarios — delay, diversion, chain break — are assessed, not only the intended path
- Repeat triggers include route change, new site or courier, and new market

### Outcomes
- The gaps between domain boundaries are assessed by someone rather than by nobody
- One record describes the therapy's whole data journey
- What the patient is told at consent matches what actually happens to their data

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Links

---

### 3.1 Governance Responses

___

## Link Governance Response

### Driver
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Policy
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Rationale
The exposure is contained only while the mapping stays separate from the data it pseudonymises. Holding it clinically with logged, minimal resolution is what keeps that separation under operational pressure.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Policy
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Rationale
The exposure arises at the handovers between domains, which a review conducted domain by domain cannot see.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Rationale
Article 17 provides exemptions from erasure but requires the controller to identify and justify them. Registering the categories in advance is how a request is answered accurately within the month rather than researched during it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Rationale
Pseudonymisation is a recognised safeguard only where the additional information is kept separately and subject to technical and organisational measures. This obligation is those measures.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Rationale
The transition brings patient data into manufacturing for the first time, and the review is how each new therapy is assessed before the first patient is collected rather than after the first incident.

___

---

### 3.2 Governance Mechanisms

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Mechanism
CocoPharma::GovernanceMetric::PrivacyImpactAssessmentCoverage

### Rationale
The therapy review contains the privacy impact assessment, so coverage of high-risk processing is measured through it rather than through a separate assessment count.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Mechanism
CocoPharma::DataProcessingPurpose::PersonalisedManufacturing

### Rationale
The purpose declares the split between the reference processed in manufacturing and the mapping held clinically; this obligation is the control that holds the split in place.

___

---

### 3.3 Peer Policy Links

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Description
Manufacturing issues the reference and works to it; privacy governs the mapping that reference points at. Neither domain can protect the patient alone — an unbreakable reference is useless if the mapping is casually accessible, and a well-guarded mapping is useless if manufacturing holds the identity anyway.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Governance Policy 2
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Description
The batch attribution purpose states that GMP attribution cannot be erased. This obligation is where that position is registered alongside every other refusal, with the consent wording that tells the patient before their data is collected.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Governance Policy 2
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Description
The forty-year surveillance retention is another refusal category, and it concerns workers rather than patients — which is why the register is assembled across domains rather than maintained as a patient-facing list.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Description
The retention schedule says how long data is kept; the erasure register says which of those periods survive a request to delete and why. The second is not derivable from the first.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Governance Policy 2
CocoPharma::GovernanceObligation::ContainedUseNotified

### Description
A personalised therapy's review must establish that the manufacturing activity is within a current contained use notification, since the same vessel carries a biological classification and a patient identity and both follow it between sites.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
Where collection, manufacture and administration sit in different jurisdictions the therapy engages the transfer regime on every leg, and the review is where the mechanism for each is established before the first shipment.

___

---

## Part 4: Folio Membership

The definitions added here are privacy-domain definitions and join the Chief Privacy Officer folio.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::ReferenceMappingHeldClinically

### Membership Rationale
Custody of the reference-to-patient mapping and the terms on which it may be resolved is a privacy control owned by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::ErasureLimitsDocumented

### Membership Rationale
The register of erasure refusals is assembled from every domain and maintained by the privacy team, which answers the requests it governs.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::JointPrivacyManufacturingReview

### Membership Rationale
The joint therapy review is convened by the privacy function with manufacturing and biological safety.

### Membership Status
VALIDATED

___

---

## Appendix: Coverage map

Which definition answers which question, for this scenario. The definitions marked *new* are added by this file; the rest already existed and are shown so the scenario can be read as a whole.

| Question | Definition | Domain |
|---|---|---|
| Who may see the patient's identity? | `PatientIdentityMinimisedInManufacturing` | MANUFACTURING |
| Where is the reference created? | `ManufacturingPseudonymisation` | MANUFACTURING |
| Who holds the mapping, and on what terms? | `ReferenceMappingHeldClinically` *(new)* | PRIVACY |
| How is the batch kept matched to its patient? | `ChainOfIdentityUnbroken` | MANUFACTURING |
| On what basis is any of it processed? | `PersonalisedManufacturing` | MANUFACTURING |
| Why can attribution not be erased? | `BatchRecordAttribution` | MANUFACTURING |
| What else can the patient not have erased, and were they told? | `ErasureLimitsDocumented` *(new)* | PRIVACY |
| Who assesses the journey end to end? | `JointPrivacyManufacturingReview` *(new)* | PRIVACY |
| What governs the material as a GMO? | `ContainedUseNotified` | 24 |
| What governs it in transit? | `TimeCriticalShipmentsPlanned` · `ColdChainMonitoring` | 25 · MANUFACTURING |
| What governs it crossing a border? | `InternationalTransferSafeguards` · `IntraGroupControllershipDefined` | PRIVACY |
| What governs the couriers and contract manufacturers? | `DataProcessingAgreementsRequired` | PRIVACY |

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| [data-processing-purposes.md](data-processing-purposes.md) | The purposes referenced throughout, including `PersonalisedManufacturing` and `BatchRecordAttribution` |
| `0. data-governance-program/manufacturing-governance-program.md` | The manufacturing side of the scenario — pseudonymisation, chain of identity, and the batch record |
| `0. data-governance-program/privacy-governance-program.md` | Controllership, transfers, retention and the impact assessment process this scenario draws on |
| `0. data-governance-program/biological-agents-and-gmo.md` | Contained use, which applies to the same material throughout its journey |
| `0. data-governance-program/dangerous-goods-transport.md` | Transport classification for the consignments carrying patient material |
