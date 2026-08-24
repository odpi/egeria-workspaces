# Coco Pharmaceuticals — Privacy Governance Program

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-15  
> **Description:** Governance definitions for the PRIVACY domain at Coco Pharmaceuticals. This file extends the foundation in `joint-governance-officer-definitions.md` (which defines GDPR, the Privacy by Design principle, the data classification obligation, the Chief Privacy Officer role and folio, and the personal data breaches metric) with the full set of privacy governance principles, obligations, approaches, roles, and metrics needed to operationalise GDPR compliance. Coco Pharmaceuticals is a US-listed parent with subsidiaries in the UK and the EU, which makes controllership, international transfers, and supervisory authority relationships live governance questions rather than structural detail.

---

## Overview

Coco Pharmaceuticals processes significant volumes of personal data — patient health data collected during clinical trials and personalised treatment programmes, employee data held by Human Resources, and commercial data about hospital contacts and clinical staff. As Chief Privacy Officer and Head of Human Resources, Faith Broker holds responsibility for both the regulatory compliance and the organisational culture dimensions of privacy governance.

The group structure complicates every one of those flows. Coco Pharmaceuticals is a US-listed parent operating through subsidiaries in the UK and the EU, and those subsidiaries are separate legal entities and separate controllers — common ownership confers no exemption. Personal data moving from an EU subsidiary to the US parent is a disclosure to a third party and a restricted international transfer, requiring both a controllership basis and a transfer mechanism, even though the systems are shared and the movement feels internal. Post-Brexit the UK operates its own regime with its own regulator and its own transfer instruments, so UK-origin and EEA-origin data cannot be governed by a single document. Parts 2 and 3 address these directly.

This document builds out the PRIVACY governance domain across three layers:

1. **Governance Drivers** — the UK GDPR regulation (separate from EU GDPR post-Brexit) that extends the obligations in `joint-governance-officer-definitions.md`.
2. **Governance Policies** — the detailed privacy principles, obligations, and approaches that implement GDPR requirements in practice.
3. **Governance Controls** — the privacy-specific governance roles and metrics that operationalise the policies, including the measurement of transfer safeguard currency across the group.

All definitions in this file have Domain Identifier `PRIVACY` and are members of the Chief Privacy Officer Governance Folio.

---

## Part 1: Governance Drivers — Additional Privacy Regulations

___

## Create Regulation

### Display Name
UK General Data Protection Regulation (UK GDPR)

### Qualified Name
CocoPharma::Regulation::UKGDPR

### Domain Identifier
PRIVACY

### Summary
The UK's post-Brexit data protection regulation, which retains the substance of EU GDPR and applies to Coco Pharmaceuticals' processing of personal data in the United Kingdom.

### Description
Following the UK's departure from the European Union, the EU GDPR was incorporated into UK law as the UK GDPR, supplemented by the Data Protection Act 2018. The UK GDPR applies to all personal data processed by Coco Pharmaceuticals in relation to UK data subjects — including patients at UK hospital partners, UK-based employees, and UK clinical trial participants. The requirements closely mirror those of EU GDPR: lawful basis, data subject rights, data breach notification within 72 hours, and privacy by design. The UK Information Commissioner's Office (ICO) is the supervisory authority. Transfers of personal data from the UK to other countries — including the EU — must meet adequacy or safeguard requirements.

### Regulation Source
UK Data Protection Act 2018 incorporating the UK General Data Protection Regulation

### Regulators
- Information Commissioner's Office (ICO) — UK

### Implications
- UK data subjects have the same rights as EU data subjects under GDPR
- Transfers of personal data from the UK to non-adequate countries require appropriate safeguards
- UK GDPR and EU GDPR must both be satisfied for cross-border processing activities
- The ICO must be notified of breaches affecting UK data subjects within 72 hours

### Importance
Critical

### Category
Privacy & Data Protection

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — PRIVACY Domain

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Data Minimisation

### Qualified Name
CocoPharma::GovernancePrinciple::DataMinimisation

### Domain Identifier
PRIVACY

### Summary
Coco Pharmaceuticals will only collect, process, and retain personal data that is adequate, relevant, and limited to what is necessary for the specified purpose.

### Description
GDPR Article 5(1)(c) requires that personal data is collected only to the extent needed for the stated purpose. For Coco Pharmaceuticals, this means that clinical trial data collection protocols must specify exactly what personal data is required and why; patient treatment programmes must not capture data beyond what is clinically necessary; HR systems must not retain employee data beyond its purpose; and any new data collection must be reviewed to confirm it is genuinely required. Collecting excess personal data increases privacy risk, increases the scope of any potential breach, and creates unnecessary regulatory exposure.

### Implications
- All new data collection must be assessed against a stated purpose before implementation
- Data collection protocols must specify what personal data fields are required and why
- Existing data collections must be reviewed to identify and remove excess personal data
- Privacy impact assessments must include a data minimisation assessment

### Outcomes
- The volume of personal data held by Coco Pharmaceuticals is limited to what is genuinely needed
- Privacy risk and potential breach scope are reduced
- GDPR data minimisation requirements (Article 5(1)(c)) are satisfied

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Purpose Limitation

### Qualified Name
CocoPharma::GovernancePrinciple::PurposeLimitation

### Domain Identifier
PRIVACY

### Summary
Personal data collected for one purpose will not be used for a different, incompatible purpose without a fresh lawful basis and, where required, the data subject's consent.

### Description
GDPR Article 5(1)(b) requires that personal data is collected for specified, explicit, and legitimate purposes and not further processed in a manner incompatible with those purposes. At Coco Pharmaceuticals, patient data collected for a specific clinical trial cannot be repurposed for commercial analytics without assessment and, typically, renewed consent. Research data cannot be used for HR decisions. Employee data cannot be used for drug development purposes. Each new use of existing personal data must be assessed for compatibility with the original collection purpose, and a new lawful basis identified if needed. This principle works alongside the cross-domain principle of Information Use Limited to Approved, Ethical Purposes.

### Implications
- The purpose of each personal data collection must be documented at the point of collection
- New uses of existing personal data must be assessed for GDPR compatibility before implementation
- Where a new use is incompatible with the original purpose, a fresh lawful basis must be identified
- Data subjects must be informed of any material change in how their data is used

### Outcomes
- Personal data is used only in ways that data subjects would reasonably expect
- GDPR purpose limitation requirements (Article 5(1)(b)) are satisfied
- Trust with patients, clinical trial participants, and employees is maintained

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Data Subject Rights Must Be Honoured Promptly

### Qualified Name
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Domain Identifier
PRIVACY

### Summary
Individuals whose personal data is held by Coco Pharmaceuticals have legal rights over that data, and the organisation must have processes to exercise those rights within GDPR deadlines.

### Description
GDPR grants data subjects a set of rights: the right to access their personal data (Subject Access Request, SAR), the right to rectification of inaccurate data, the right to erasure ("right to be forgotten") in defined circumstances, the right to restrict processing, the right to data portability, and the right to object. For Coco Pharmaceuticals, this applies to patients, clinical trial participants, employees, and any other individual whose personal data the organisation holds. Most rights must be fulfilled within one calendar month of the request. The organisation must have clear processes, trained staff, and sufficient technical capability to locate, retrieve, correct, or delete personal data in response to a valid request.

### Implications
- A formal process must exist to receive, triage, verify, and respond to data subject requests
- All systems holding personal data must be capable of locating an individual's data by identity
- Staff who receive data subject requests must know how to handle and escalate them
- Records of requests and responses must be maintained

### Outcomes
- Data subjects can exercise their GDPR rights within legal deadlines
- The organisation avoids regulatory sanction for failing to respond to rights requests
- Trust with patients, employees, and clinical trial participants is maintained

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Lawful Basis for Processing Must Be Documented

### Qualified Name
CocoPharma::GovernancePrinciple::LawfulBasisDocumented

### Domain Identifier
PRIVACY

### Summary
Every activity in which Coco Pharmaceuticals processes personal data must have a documented lawful basis under GDPR before processing begins.

### Description
GDPR Article 6 requires that personal data is only processed when there is a valid lawful basis. The six lawful bases are: consent, contract, legal obligation, vital interests, public task, and legitimate interests. For a pharmaceutical company, the most common bases are: consent (for optional data collection from patients), contract (for employee data), legal obligation (for regulatory submissions and clinical trial reporting), and legitimate interests (for some analytics and security monitoring). Special category data (such as health data) requires both a standard lawful basis and an additional condition under Article 9. The lawful basis must be determined before processing begins, documented in the Record of Processing Activities, and communicated to data subjects in privacy notices.

### Implications
- A lawful basis must be identified and documented for every data processing activity before it begins
- Health data (special category) requires both Article 6 and Article 9 conditions to be identified
- Privacy notices must accurately state the lawful basis for each processing activity
- If the lawful basis changes, data subjects must be informed and processing must pause until the new basis is established

### Outcomes
- All personal data processing has a clear legal foundation
- GDPR Article 6 and Article 9 requirements are satisfied
- Enforcement risk from unlawful processing is eliminated

### Authors
Faith Broker

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
Privacy Impact Assessments Required for High-Risk Processing

### Qualified Name
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Domain Identifier
PRIVACY

### Summary
Any new or significantly changed processing activity that is likely to result in a high risk to individuals' rights and freedoms must have a completed Privacy Impact Assessment (Data Protection Impact Assessment) before processing begins.

### Description
GDPR Article 35 requires a Data Protection Impact Assessment (DPIA) — referred to here as a Privacy Impact Assessment (PIA) — for processing that is likely to result in high risk. At Coco Pharmaceuticals, high-risk processing includes: processing special category data at scale (patient health data), systematic surveillance or monitoring, new uses of existing personal data collections, automated decision-making with significant effects, and large-scale data sharing with research partners. The PIA must identify risks, assess their likelihood and severity, and define mitigation measures. Where residual risks remain high, the ICO must be consulted before processing begins. PIAs must be reviewed when processing activities change materially.

### Implications
- A PIA screening must be completed for all new data processing initiatives
- Full PIAs must be conducted for any initiative meeting the high-risk criteria
- PIAs must be reviewed and updated when processing activities change materially
- The Data Protection Officer must review and approve PIAs before high-risk processing begins

### Outcomes
- High-risk processing activities are identified before they begin, not after a breach
- GDPR Article 35 obligations are met
- Privacy risks are mitigated by design rather than retrospectively

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
Personal Data Retention Schedules Must Be Defined and Enforced

### Qualified Name
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Domain Identifier
PRIVACY

### Summary
Every collection of personal data held by Coco Pharmaceuticals must have a defined retention period; data must be deleted or anonymised when that period expires.

### Description
GDPR Article 5(1)(e) requires that personal data is kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which it is processed. For Coco Pharmaceuticals, different categories of personal data have different retention requirements: clinical trial data has regulatory retention requirements (typically 15–25 years under ICH E6 GCP and FDA regulations); employee data has statutory and contractual retention requirements; patient data held by hospital partners has different obligations from data held by Coco Pharmaceuticals directly. Each data collection must have a defined retention schedule that reflects both the minimum retention needed for the business or regulatory purpose and the maximum allowed by privacy law. Automated or process-enforced deletion must be implemented where technically feasible.

### Implications
- A retention schedule must be defined for every significant personal data collection
- Retention periods must be reviewed when regulatory requirements change
- Systems must have mechanisms to delete or anonymise data when retention periods expire
- Retention periods and the basis for them must be documented in the Record of Processing Activities

### Outcomes
- Personal data is not held for longer than necessary, reducing privacy risk and storage costs
- GDPR storage limitation requirements (Article 5(1)(e)) are satisfied
- Regulatory retention obligations (FDA, ICH GCP) are met within a privacy-compliant framework

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
Personal Data Breaches Must Be Notified Within 72 Hours

### Qualified Name
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Domain Identifier
PRIVACY

### Summary
Any personal data breach that is likely to result in a risk to individuals must be reported to the relevant supervisory authority within 72 hours of becoming aware of it; affected individuals must be informed where the risk is high.

### Description
GDPR Article 33 requires that personal data breaches are reported to the supervisory authority (ICO for UK; the relevant national authority in EU member states) within 72 hours of becoming aware, where the breach is likely to result in risk to individuals. GDPR Article 34 requires notification to affected individuals without undue delay where the breach is likely to result in high risk. At Coco Pharmaceuticals, any incident involving loss, unauthorised access, or disclosure of personal data — including patient health data, clinical trial participant data, or employee data — must be assessed immediately and escalated to the CPO within hours of detection. The 72-hour clock starts when the organisation becomes aware that a breach has occurred. Near-misses must also be recorded. Internal procedures, contact details for supervisory authorities, and template notification letters must be prepared in advance.

### Implications
- A breach response procedure must exist and be rehearsed before a breach occurs
- All staff must know how to recognise and report a suspected data breach immediately
- The CPO must have a contact list for supervisory authorities ready to use
- Internal breach records must be maintained even where notification to the authority is not required

### Outcomes
- GDPR breach notification obligations (Articles 33 and 34) are met within legal deadlines
- Affected individuals receive timely information to take protective action
- The organisation demonstrates compliance by having a documented and rehearsed response process

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
Record of Processing Activities Must Be Maintained

### Qualified Name
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Domain Identifier
PRIVACY

### Summary
Coco Pharmaceuticals must maintain a documented Record of Processing Activities (ROPA) covering all personal data processing, as required by GDPR Article 30.

### Description
GDPR Article 30 requires that organisations with more than 250 employees — or organisations processing special category data (which Coco Pharmaceuticals does) — maintain a written record of all processing activities. The ROPA must document: the name and contact details of the data controller, the purpose of each processing activity, a description of the categories of data subjects and personal data, the recipients of the data, details of any international transfers, retention periods, and a description of the technical and organisational security measures in place. The ROPA is a living document: it must be updated whenever new processing activities begin, existing activities change, or processing ceases. It must be made available to supervisory authorities on request. The ROPA forms the backbone of Coco Pharmaceuticals' privacy accountability documentation.

### Implications
- A ROPA must be created and maintained covering all personal data processing activities
- New processing activities must be added to the ROPA before processing begins
- Changes to existing processing must be reflected in the ROPA promptly
- The CPO is accountable for the ROPA; each data owner is responsible for supplying information about their processing activities

### Outcomes
- GDPR Article 30 obligations are met
- The organisation has a complete and current map of its personal data processing
- The ROPA supports PIAs, breach assessments, and supervisory authority enquiries

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
Data Processing Agreements Required for Third-Party Processors

### Qualified Name
CocoPharma::GovernanceObligation::DataProcessingAgreementsRequired

### Domain Identifier
PRIVACY

### Summary
Any third party that processes personal data on behalf of Coco Pharmaceuticals must have a written Data Processing Agreement in place before processing begins.

### Description
GDPR Article 28 requires that when a controller engages a processor — any third party that processes personal data on behalf of the controller — the arrangement must be governed by a written contract (a Data Processing Agreement, DPA). For Coco Pharmaceuticals, processors include: clinical research organisations (CROs) that manage trial data on the company's behalf, cloud service providers hosting systems that contain personal data, HR software providers, and laboratory service providers handling patient samples linked to personal data. The DPA must impose GDPR-compliant obligations on the processor: processing only on documented instructions, implementing appropriate security measures, assisting with data subject rights requests and breach notification, and allowing audit. Processors may not sub-contract without the controller's authorisation. Existing supplier agreements must be reviewed to identify gaps. The requirement is not limited to external suppliers: where one group entity processes personal data on the instruction of another, an Article 28 agreement is required between them in the same form, and the intra-group controllership obligation governs how that determination is made.

### Implications
- All third-party processors must be identified and mapped (this feeds into the ROPA)
- No personal data may be shared with a processor that does not have a signed DPA in place
- DPAs must be reviewed and updated when the processing relationship changes materially
- Supplier onboarding must include a privacy review to determine whether a DPA is required

### Outcomes
- GDPR Article 28 obligations are met
- Third-party processing risk is contractually controlled
- The organisation can demonstrate accountability across its supply chain

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
Intra-Group Personal Data Sharing Must Have a Defined Controllership Basis

### Qualified Name
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Domain Identifier
PRIVACY

### Summary
Personal data shared between the US parent and the UK and EU subsidiaries must have a recorded controllership determination and an intra-group agreement giving effect to it, before sharing begins.

### Description
Group companies are separate legal entities and separate controllers under data protection law, notwithstanding common ownership and shared systems. There is no group exemption: a transfer of employee records from the EU subsidiary to the US parent is a disclosure to a third party in law, and requires the same basis and the same documentation as a disclosure to an unconnected company. In practice this is frequently missed precisely because the systems are shared and the sharing feels internal. This obligation requires each category of intra-group sharing to be assessed and recorded: which entity determines the purpose and means, and therefore is controller; whether entities are joint controllers with an Article 26 arrangement setting out who discharges which obligation; or whether one entity processes on another's instruction, requiring an intra-group Article 28 agreement in the same form as one with an external processor. Shared platforms need particular attention, since a single HR or trial management system holding data for all entities has to be resolved into per-entity controllership rather than treated as a group asset. Where the determination is joint controllership, the essence of the arrangement must be made available to data subjects, and they may exercise their rights against any of the joint controllers regardless of what the arrangement says between them.

### Implications
- Each category of intra-group sharing requires a recorded controllership determination
- Joint controllership requires an Article 26 arrangement and disclosure of its essence to data subjects
- Intra-group processor relationships require Article 28 agreements in the same form as external ones
- Shared platforms must be resolved into per-entity controllership, not treated as group assets
- Data subjects may exercise rights against any joint controller, whatever the internal allocation

### Outcomes
- Group sharing rests on a documented basis rather than on common ownership
- Responsibility for responding to a data subject or a regulator is clear before the request arrives
- Shared systems can be operated without obscuring which entity is accountable for the data in them

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
International Personal Data Transfers Must Have a Documented Safeguard

### Qualified Name
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Domain Identifier
PRIVACY

### Summary
Personal data leaving the UK or the EEA — including transfers to the US parent — must be covered by an adequacy decision or an appropriate safeguard, supported by a transfer risk assessment where a safeguard is relied on.

### Description
Every routine flow from the UK and EU subsidiaries to the US parent is a restricted international transfer requiring a lawful transfer mechanism, and the mechanism differs by origin. For EEA-origin data the routes are the EU-US Data Privacy Framework where the US parent is certified for the relevant data categories, or the EU Standard Contractual Clauses. For UK-origin data neither of those applies unchanged: the UK requires the International Data Transfer Agreement, or the UK Addendum to the EU clauses, or reliance on the UK extension to the Data Privacy Framework. Relying on contractual safeguards rather than adequacy triggers a transfer risk assessment examining whether the law of the destination country undermines the protection the clauses promise, with supplementary measures applied where it does. Transfer mechanisms are not permanent: adequacy decisions have been invalidated before and Data Privacy Framework certifications lapse, so each mechanism carries a review date and a documented fallback that can be activated without interrupting the flow. Onward transfers by the US parent to its own processors are within scope, since a safeguard that ends at the parent protects nothing.

### Implications
- Every routine cross-border flow must be inventoried with its origin, destination, and mechanism
- UK-origin and EEA-origin transfers require different instruments and cannot share one document
- Reliance on contractual safeguards requires a transfer risk assessment and any necessary supplementary measures
- Each mechanism carries a review date and a documented fallback that can be activated at short notice
- Onward transfers by the receiving entity are within scope and must be covered contractually

### Outcomes
- Transfers to the US parent rest on a valid, current mechanism rather than assumed group latitude
- Invalidation of a mechanism triggers a prepared fallback rather than an interruption
- The company can evidence its transfer basis to the ICO and to EU authorities on request

### Authors
Faith Broker

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
Data Subject Request Management

### Qualified Name
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Domain Identifier
PRIVACY

### Summary
A defined, end-to-end process for receiving, verifying, routing, fulfilling, and recording responses to data subject rights requests within GDPR deadlines.

### Description
Data subject rights requests — including Subject Access Requests (SARs), rectification requests, erasure requests, and objections — must be handled within one calendar month (extendable by two further months for complex requests, with notice). At Coco Pharmaceuticals, requests may arrive through multiple channels: the company website, HR, clinical trial teams, or hospital partner contacts. The approach defines: a single intake point for all requests; identity verification before personal data is disclosed; a triage process to determine which right is being exercised and which systems hold the relevant data; a co-ordination process involving the relevant data owners; a quality check by the CPO team before response; and a record of requests, decisions, and responses maintained in the ROPA. Staff in patient-facing, HR, and clinical roles must be trained to recognise and escalate requests.

### Implications
- A single intake channel must be established and communicated to data subjects
- All systems holding personal data must respond to data owner search requests within a defined timeframe
- Staff training must cover recognition and escalation of data subject requests
- The DSRM process must be tested at least annually

### Outcomes
- Data subjects receive timely, complete, and accurate responses to their rights requests
- GDPR deadlines are consistently met
- The organisation can demonstrate a systematic, accountable approach to rights fulfilment

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Consent and Lawful Basis Management

### Qualified Name
CocoPharma::GovernanceApproach::ConsentAndLawfulBasisManagement

### Domain Identifier
PRIVACY

### Summary
A structured approach to identifying, documenting, obtaining, and maintaining the lawful basis for each personal data processing activity, including managing consent where it is the chosen basis.

### Description
Before any personal data processing begins, a lawful basis must be identified and documented. Where consent is the lawful basis — for example, for optional data collection from clinical trial participants beyond the minimum required for the trial — that consent must be freely given, specific, informed, and unambiguous. Consent records must capture what was consented to, when, through which mechanism, and the version of the privacy notice in force at the time. Data subjects must be able to withdraw consent as easily as they gave it, and withdrawal must be acted upon promptly. For processing that relies on legitimate interests, a Legitimate Interests Assessment (LIA) must be conducted and documented. The approach also governs the maintenance of privacy notices — they must be written in plain language, kept accurate, and updated when processing activities change.

### Implications
- Consent must be captured in a structured, auditable way — not through pre-ticked boxes or implied acceptance
- Consent withdrawal must trigger a documented process to cease processing and record the withdrawal
- Legitimate interests assessments must be documented before processing begins on that basis
- Privacy notices must be reviewed and updated whenever processing activities change materially

### Outcomes
- All personal data processing has a documented, defensible lawful basis
- Consent is managed in a manner that satisfies GDPR Article 7 requirements
- Privacy notices accurately reflect processing activities and give data subjects the information they need

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Privacy Impact Assessment Process

### Qualified Name
CocoPharma::GovernanceApproach::PrivacyImpactAssessmentProcess

### Domain Identifier
PRIVACY

### Summary
A defined process for screening new and changed data processing activities, conducting full Privacy Impact Assessments for high-risk activities, and embedding privacy risk management into project delivery.

### Description
The PIA process operates at two levels. First, a lightweight screening is applied to every new or materially changed data processing activity to determine whether a full PIA is required. Second, for activities meeting the high-risk threshold, a full PIA is conducted covering: a systematic description of the processing, an assessment of the necessity and proportionality of the processing, an assessment of risks to data subjects, and the measures taken to address those risks. At Coco Pharmaceuticals, the PIA process is embedded into the project delivery lifecycle — no new system or process involving personal data may proceed to implementation without a PIA screening outcome on record, and no high-risk processing may begin without a completed and approved PIA. The Data Protection Officer reviews and approves PIAs for high-risk processing. The CPO maintains a register of completed PIAs.

### Implications
- Project teams must engage the privacy team at the design stage, not at the point of go-live
- A PIA screening form must be available to all project leads
- The DPO must have capacity to review high-risk PIAs within the project timeline
- A register of PIA outcomes must be maintained and linked to the ROPA

### Outcomes
- Privacy risks are identified and addressed before systems are built or changed
- GDPR DPIA obligations (Article 35) are met
- The organisation embeds privacy by design into its delivery processes

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Group Controllership and Supervisory Authority Mapping

### Qualified Name
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Domain Identifier
PRIVACY

### Summary
The group maintains a map of which entity controls which processing, which supervisory authority leads for each, and where a representative must be appointed, reviewed whenever the corporate or system landscape changes.

### Description
With a US parent and subsidiaries in the UK and the EU, the question of who regulates a given processing activity has no single answer, and answering it during an incident is too late. This approach maintains the map in advance. For EU processing it establishes whether the group has a main establishment in the EU — the place where decisions about purposes and means are actually taken, which is a question of fact rather than of corporate structure — and therefore whether it can rely on the one-stop-shop and deal with a single lead supervisory authority under Article 56, or whether it faces each national authority separately. Post-Brexit the UK ICO is a separate regulator regardless of the EU position, so the group deals with at least two authorities and possibly more. Where an entity offers goods or services into the EU or UK without an establishment there, an Article 27 representative must be appointed and published. The map records, for each processing activity: the controlling entity, the applicable regime, the competent authority, the transfer mechanism where data crosses a border, and the accountable privacy steward. It is reviewed on any corporate change, on any material change to where decisions are taken, and at least annually.

### Implications
- Main establishment must be determined on where decisions are actually taken, not on corporate convenience
- The UK ICO is a separate authority from EU authorities and must be handled as such
- Article 27 representatives must be appointed and published where an entity has no local establishment
- The map must be reviewed on corporate change, not only on the annual cycle
- Each processing activity must resolve to a named entity, regime, authority, and steward

### Outcomes
- The competent authority for any processing is known before an incident requires it
- One-stop-shop eligibility is established deliberately rather than assumed
- Regulatory correspondence reaches the entity accountable for the processing in question

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — PRIVACY Domain

---

### 3.1 Governance Roles

___

## Create Governance Role

### Display Name
Data Protection Officer

### Qualified Name
CocoPharma::GovernanceRole::DataProtectionOfficer

### Description
The Data Protection Officer (DPO) is the independent privacy expert required by GDPR Article 37 for organisations that process special category data at scale. At Coco Pharmaceuticals, the DPO is mandatory given the volume of patient health data processed during clinical trials and personalised treatment programmes. The DPO's responsibilities are set by GDPR and cannot be restricted by the organisation: informing and advising the organisation on GDPR obligations, monitoring compliance, advising on PIAs, cooperating with supervisory authorities, and acting as the contact point for data subjects and regulators. The DPO must have expert knowledge of data protection law, must be resourced adequately to perform their tasks, and must report to the highest level of management. The DPO may be an employee or an external service provider, and must be able to act independently.

### Scope
Organisation-wide independence — the DPO monitors compliance across all personal data processing activities regardless of domain, and cannot be given instructions that compromise their independence.

### Headcount
1

### Category
Governance Role

### Search Keywords
- DPO
- Data Protection Officer
- GDPR compliance
- privacy regulation

### Version Identifier
1.0

___

---

___

## Create Governance Role

### Display Name
Privacy Steward

### Qualified Name
CocoPharma::GovernanceRole::PrivacySteward

### Description
A Privacy Steward is a departmental representative responsible for applying privacy governance within their business area. Each significant department that processes personal data — including Clinical Trials, Research, Manufacturing, Human Resources, Finance, and IT — appoints a Privacy Steward. The Privacy Steward acts as the first point of contact for privacy queries within their department, assists with PIA screenings and full PIAs, maintains awareness of what personal data their department collects and processes, escalates potential breaches to the CPO, and supports data subject rights fulfilment by locating personal data held in their departmental systems. Privacy Stewards are appointed by the CPO in consultation with the relevant department head, and receive specialist privacy training.

### Scope
Departmental — each Privacy Steward is accountable for the privacy governance of the personal data processed within their assigned department or business area.

### Headcount
6

### Category
Governance Role

### Search Keywords
- Privacy Steward
- departmental privacy
- privacy representative
- GDPR compliance

### Version Identifier
1.0

___

---

### 3.2 Governance Metrics

___

## Create Governance Metric

### Display Name
Data Subject Request Completion Rate

### Qualified Name
CocoPharma::GovernanceMetric::DataSubjectRequestCompletionRate

### Domain Identifier
PRIVACY

### Summary
Measures the percentage of data subject rights requests that are completed within the GDPR deadline of one calendar month.

### Description
Under GDPR, data subject rights requests must be responded to within one calendar month (with a possible two-month extension for complex or numerous requests, provided the data subject is informed within the first month). This metric tracks the proportion of requests that are completed — with a substantive response to the data subject — within the one-month deadline without requiring an extension. A rate below 100% indicates process gaps or resourcing constraints that must be addressed. The metric is reported by the CPO monthly and reviewed quarterly with the CDO and DPO.

### Implications
- Requires a formal log of all data subject requests with submission and completion dates
- Requires all departments to respond to data owner search requests within internal sub-deadlines
- Extensions must be recorded separately — an extension granted is not a failure, but an unnotified overrun is

### Outcomes
- GDPR data subject rights obligations are met within legal deadlines
- Data subjects receive a satisfactory level of service
- The organisation's exposure to ICO complaints and enforcement action is minimised

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Privacy Impact Assessment Coverage Rate

### Qualified Name
CocoPharma::GovernanceMetric::PrivacyImpactAssessmentCoverage

### Domain Identifier
PRIVACY

### Summary
Measures the percentage of new or materially changed data processing activities that have a completed PIA screening on record before implementation.

### Description
All new or materially changed data processing activities should be screened for PIA requirements before they begin. This metric tracks the proportion of initiatives identified as involving personal data that have a completed PIA screening — or a completed full PIA where required — on record at the point of go-live. A rate below 100% indicates that projects are bypassing the privacy gateway, which creates both regulatory risk and operational risk. The metric is produced by comparing the project registry (maintained by IT/PMO) against the PIA register (maintained by the CPO). Gaps are investigated and remediated.

### Implications
- Requires a mechanism to identify all active projects and determine which involve personal data
- Requires the PIA screening to be a formal gate in the project delivery process
- Requires the CPO team to have sufficient capacity to conduct screenings within project timelines

### Outcomes
- Privacy risks are assessed before processing begins rather than after a breach
- GDPR DPIA obligations are systematically met
- The organisation can demonstrate a privacy-by-design culture to supervisory authorities

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Personal Data Retention Schedule Compliance Rate

### Qualified Name
CocoPharma::GovernanceMetric::PersonalDataRetentionComplianceRate

### Domain Identifier
PRIVACY

### Summary
Measures the percentage of personal data collections that have a defined, approved retention schedule, and the percentage where expired data is deleted or anonymised within the scheduled timeframe.

### Description
This metric has two components. First, the coverage component: the proportion of personal data collections documented in the ROPA that have a defined and approved retention schedule. This should be 100%. Second, the compliance component: where automated or process deletion is in place, the proportion of deletion actions that are completed within 30 days of the retention expiry date. The metric highlights both gaps in schedule definition (the coverage component) and failures in deletion execution (the compliance component). It is reported quarterly by the CPO and reviewed alongside the ROPA update cycle.

### Implications
- Requires a current ROPA with retention schedules defined for all personal data collections
- Requires a mechanism to track when retention periods expire and whether deletion/anonymisation has been performed
- Requires data owners to confirm deletion completion where manual action is required

### Outcomes
- Personal data is not held beyond its retention period, reducing privacy risk
- GDPR storage limitation obligations (Article 5(1)(e)) are satisfied
- The organisation can demonstrate accountability for its retention practices

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
International Transfer Safeguard Currency

### Qualified Name
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Domain Identifier
PRIVACY

### Summary
Measures the percentage of inventoried cross-border personal data flows covered by a current, valid transfer mechanism with an in-date transfer risk assessment where one is required.

### Description
Currency is the measure rather than coverage, for the same reason it is in third-party screening: almost every known flow will have had a mechanism put in place at some point, and the exposure lies in mechanisms that have lapsed, that were signed against a superseded version of the clauses, or that rest on a certification which has since expired. The metric therefore tests each inventoried flow against three conditions — a mechanism exists, it is the current instrument for that origin, and any required transfer risk assessment is within its review period. Reporting separates UK-origin from EEA-origin flows, since they require different instruments and a single figure would conceal a systematic gap in one of them. Flows discovered during review but not previously inventoried are reported separately as an inventory gap rather than being absorbed into the denominator, because an unknown flow is a different and worse problem than a lapsed one. Target is 100%, since unlike most metrics a shortfall here is an unlawful transfer rather than a performance gap.

### Implications
- Requires a maintained inventory of cross-border flows, which is itself the harder part
- UK-origin and EEA-origin flows must be reported separately
- Newly discovered flows are reported as inventory gaps, not folded into the rate
- Mechanism version currency must be tested, not merely existence

### Outcomes
- Lapsed and superseded transfer mechanisms are found before a regulator finds them
- Systematic gaps in one origin regime are visible rather than averaged away
- The scale of undocumented transfer activity is measured rather than assumed

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to PRIVACY Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::DataMinimisation

### Rationale
GDPR Article 5(1)(c) directly requires data minimisation. This principle translates that legal requirement into a governance commitment across all Coco Pharmaceuticals' data processing activities.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::PurposeLimitation

### Rationale
GDPR Article 5(1)(b) directly requires purpose limitation. This principle gives effect to that requirement, preventing personal data from being repurposed without a fresh assessment and lawful basis.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Rationale
GDPR Chapter III (Articles 12–23) establishes the full set of data subject rights. This principle commits Coco Pharmaceuticals to honouring those rights within the legal deadlines.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::LawfulBasisDocumented

### Rationale
GDPR Article 6 requires a lawful basis for all personal data processing. Documenting that basis before processing begins is the foundational accountability requirement for GDPR compliance.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Rationale
GDPR Article 35 requires a Data Protection Impact Assessment for high-risk processing. This obligation implements that requirement as a mandatory governance gate in the project delivery process.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Rationale
GDPR Article 5(1)(e) requires that personal data is kept no longer than necessary. Defining and enforcing retention schedules is the operational mechanism for meeting this requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Rationale
GDPR Articles 33 and 34 require breach notification to supervisory authorities within 72 hours and to affected individuals without undue delay where risk is high. This obligation operationalises those requirements.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Rationale
GDPR Article 30 requires a written Record of Processing Activities. This obligation makes maintaining an accurate and current ROPA a mandatory governance control.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::DataProcessingAgreementsRequired

### Rationale
GDPR Article 28 requires written contracts with all third-party processors. This obligation ensures no personal data is shared with a processor without a compliant agreement in place.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernancePrinciple::DataMinimisation

### Rationale
UK GDPR mirrors EU GDPR's data minimisation requirement. The same principle applies to personal data processing activities involving UK data subjects.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Rationale
UK GDPR grants UK data subjects the same rights as EU GDPR. This principle ensures those rights are honoured for UK patients, employees, and clinical trial participants.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Rationale
UK GDPR requires breach notification to the ICO within 72 hours. This obligation covers both EU GDPR and UK GDPR breach notification requirements for the respective supervisory authorities.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernancePrinciple::DataMinimisation

### Rationale
Minimising the volume of personal data collected directly reduces the potential impact of any unauthorised disclosure — there is less data to be exposed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Rationale
When an unauthorised disclosure does occur, the 72-hour notification obligation ensures that the impact on data subjects is limited by prompt regulatory and individual notification.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::DataProcessingAgreementsRequired

### Rationale
A significant disclosure risk comes from third-party processors who handle personal data on the organisation's behalf. Data Processing Agreements contractually bind processors to appropriate security and breach notification obligations.

___

---

### 4.2 Governance Mechanisms — PRIVACY Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Mechanism
CocoPharma::GovernanceMetric::DataSubjectRequestCompletionRate

### Rationale
The completion rate directly measures whether the organisation is honouring data subject rights within legal deadlines. A rate below 100% is a direct indicator of non-compliance with this principle.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Mechanism
CocoPharma::GovernanceMetric::DataSubjectRequestCompletionRate

### Rationale
The completion rate is the primary outcome measure for the data subject request management process. A high rate confirms the process is working; a low rate triggers process review.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Mechanism
CocoPharma::GovernanceMetric::PrivacyImpactAssessmentCoverage

### Rationale
The PIA coverage rate measures whether the PIA obligation is being met. A rate below 100% means projects are beginning without the required privacy risk assessment.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::PrivacyImpactAssessmentProcess

### Mechanism
CocoPharma::GovernanceMetric::PrivacyImpactAssessmentCoverage

### Rationale
The coverage rate is the primary outcome measure for the PIA process. It confirms whether the process is being applied consistently across all relevant projects.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Mechanism
CocoPharma::GovernanceMetric::PersonalDataRetentionComplianceRate

### Rationale
The retention compliance rate measures whether retention schedules are both defined (coverage component) and enforced (compliance component), directly tracking adherence to this obligation.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Rationale
UK GDPR restricts transfers out of the UK, including to the EU and to the US parent, and requires the UK-specific instruments. The obligation states which instrument applies to which origin.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Rationale
Chapter V restricts transfers out of the EEA. Every routine flow from the EU subsidiaries to the US parent falls within it and requires a current mechanism.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Rationale
There is no group exemption in the Regulation. Sharing between separate legal entities requires a controllership determination and an Article 26 or Article 28 instrument as appropriate.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Rationale
Articles 56 and 60 make the identification of a main establishment and lead supervisory authority a precondition for the one-stop-shop, which has to be established before it is needed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Rationale
Post-Brexit the ICO is a separate supervisory authority from the EU authorities, so the group must map UK and EU regulatory relationships independently of each other.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Rationale
Sharing between group entities that feels internal but is a disclosure in law is a common route by which personal data leaves its lawful basis without anyone identifying it as a disclosure.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Mechanism
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Rationale
Currency against the current instrument for each origin measures the obligation as written, where a coverage figure would conceal lapsed and superseded mechanisms.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Mechanism
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Rationale
The map supplies the inventory of flows the metric measures; newly discovered flows are reported back as inventory gaps in the map.

___

---

### 4.3 Peer Policy Links — Related PRIVACY Policies

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::DataMinimisation

### Governance Policy 2
CocoPharma::GovernancePrinciple::PurposeLimitation

### Description
Data minimisation and purpose limitation are complementary: minimisation limits how much data is collected, and purpose limitation constrains how it is used. Together they define the boundaries of legitimate personal data processing.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::LawfulBasisDocumented

### Governance Policy 2
CocoPharma::GovernanceApproach::ConsentAndLawfulBasisManagement

### Description
The principle establishes the requirement; the approach defines how the requirement is met in practice — identifying, recording, and maintaining the lawful basis for every processing activity.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Governance Policy 2
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Description
The principle commits the organisation to honouring data subject rights; the approach defines the end-to-end process that makes that commitment operationally deliverable within GDPR deadlines.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Governance Policy 2
CocoPharma::GovernanceApproach::PrivacyImpactAssessmentProcess

### Description
The obligation defines when a PIA is required; the approach defines how PIAs are conducted, reviewed, and recorded. Both are needed for the DPIA requirement to be practically met.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Description
The ROPA must include retention schedules for each processing activity. These two obligations are therefore interdependent: a complete ROPA requires retention periods to be defined, and retention compliance depends on the ROPA being accurate.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Governance Policy 2
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Description
Privacy by Design (defined in `joint-governance-officer-definitions.md`) requires privacy to be embedded from the start. The PIA obligation is the primary mechanism by which this principle is applied in practice — PIAs ensure privacy risks are assessed before systems are built.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Description
The sensitivity classification (defined in `joint-governance-officer-definitions.md`) determines the stringency of the retention schedule — higher-sensitivity data may have stricter deletion requirements or, conversely, longer regulated retention periods that must be carefully managed.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Governance Policy 2
CocoPharma::GovernanceObligation::DataProcessingAgreementsRequired

### Description
The Article 28 obligation applies within the group exactly as it does to external processors. Where one group entity processes on another's instruction, the same form of agreement is required — common ownership is not a substitute for a contract.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Governance Policy 2
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Description
The ROPA already requires international transfers to be recorded. The transfer obligation makes that record the operative inventory against which safeguard currency is measured, rather than a descriptive field.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Governance Policy 2
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Description
The 72-hour clock cannot be met if the entity has to determine which authority to notify after the breach is discovered. The map answers that question in advance, for each processing activity.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Governance Policy 2
CocoPharma::GovernancePrinciple::PurposeLimitation

### Description
A transfer to a group entity for a purpose other than the one for which the data was collected is a secondary use, whatever the internal reporting lines suggest. Controllership determination is where that is caught.

___

---

## Part 5: Chief Privacy Officer Folio — Additional Members

The following Add Member to Collection commands extend the Chief Privacy Officer Governance Folio (defined in `joint-governance-officer-definitions.md`) to include the new definitions in this file.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::Regulation::UKGDPR

### Membership Rationale
The CPO is accountable for UK GDPR compliance across all Coco Pharmaceuticals' UK processing activities, in parallel with EU GDPR compliance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernancePrinciple::DataMinimisation

### Membership Rationale
Faith Broker authored and champions this principle as a core GDPR accountability requirement for all personal data processing at Coco Pharmaceuticals.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernancePrinciple::PurposeLimitation

### Membership Rationale
Faith Broker is accountable for ensuring personal data is not repurposed without a fresh assessment and lawful basis — a direct GDPR obligation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Membership Rationale
As CPO, Faith Broker is accountable for the organisation's capacity to honour data subject rights within legal deadlines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernancePrinciple::LawfulBasisDocumented

### Membership Rationale
Ensuring every processing activity has a documented lawful basis is a foundational CPO accountability, forming the basis for all other GDPR compliance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::PrivacyImpactAssessmentRequired

### Membership Rationale
Faith Broker is accountable for the PIA programme and for ensuring high-risk processing is not initiated without a completed DPIA.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Membership Rationale
The CPO is accountable for ensuring retention schedules are defined for all personal data collections and that expired data is deleted or anonymised.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Membership Rationale
As CPO, Faith Broker is personally responsible for breach notifications to supervisory authorities and for the breach response procedure.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Membership Rationale
The CPO is the accountable owner of the ROPA and is responsible for keeping it accurate, current, and available to supervisory authorities.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::DataProcessingAgreementsRequired

### Membership Rationale
Faith Broker is accountable for ensuring all third-party processors have compliant DPAs in place before personal data is shared with them.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Membership Rationale
The CPO owns the data subject request management process and is accountable for its effectiveness and timeliness.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::ConsentAndLawfulBasisManagement

### Membership Rationale
Faith Broker is accountable for the organisation's approach to consent and lawful basis documentation, including the maintenance of compliant privacy notices.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::PrivacyImpactAssessmentProcess

### Membership Rationale
The CPO owns the PIA process and is accountable for its consistent application across all projects involving personal data.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceMetric::DataSubjectRequestCompletionRate

### Membership Rationale
Faith Broker reports this metric to demonstrate the organisation's capacity to honour data subject rights within GDPR deadlines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceMetric::PrivacyImpactAssessmentCoverage

### Membership Rationale
The CPO uses this metric to confirm that the PIA programme is operating effectively and that no high-risk processing is bypassing the privacy gateway.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceMetric::PersonalDataRetentionComplianceRate

### Membership Rationale
Faith Broker is accountable for demonstrating that personal data is not held beyond its retention period — a core GDPR accountability obligation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Membership Rationale
Controllership across the US parent and the UK and EU subsidiaries is determined under the Chief Privacy Officer's authority.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Membership Rationale
Transfer mechanisms for flows to the US parent are selected, maintained, and reviewed by the privacy team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Membership Rationale
The controllership and supervisory authority map is maintained by the Data Protection Officer on the Chief Privacy Officer's behalf.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Membership Rationale
Transfer safeguard currency is reported to the Chief Privacy Officer separately for UK-origin and EEA-origin flows.

### Membership Status
VALIDATED

___

---

## Part 6: Corporate Regulation Library Membership

The regulations defined in this file are placed in the Corporate Regulation Library so that they are discoverable alongside every other regulation the company is subject to, independently of the governance domain that owns them. The library folders are defined outside this workbook.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Privacy Regulations

### Element Id
CocoPharma::Regulation::UKGDPR

### Membership Rationale
UK GDPR operates as a separate regime from EU GDPR following withdrawal, and both belong in the privacy regulations folder.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `joint-governance-officer-definitions.md` | Foundation governance definitions — GDPR regulation, Privacy by Design, Personal Data Classification, Chief Privacy Officer role and folio, Personal Data Breaches metric |
| `data-governance-program.md` | DATA-domain governance definitions |
| `3. sustainability/sustainability-governance-definitions.md` | Sustainability domain definitions |
| `4. keeping-safe/martyns-law/` | Security scenario: Martyn's Law compliance definitions |
