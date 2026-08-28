# Coco Pharmaceuticals — Data Processing Purposes

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** The data processing purposes declared across every governance domain at Coco Pharmaceuticals, gathered into one file together with the links that connect each purpose to the policy it serves and the folio that owns it. Load the whole of `0. data-governance-program` first.

---

## What a data processing purpose is, and why each team declares its own

A data processing purpose records **why** personal data is processed, **on what legal basis**, and **what that basis permits and forbids**. It is a governance control in Egeria terms, which places it alongside certification types and governance rules rather than among the policies it implements — a purpose does not say what good practice looks like, it says what this organisation is actually allowed to do with a particular body of personal data and what follows from that.

The concept came into the governance program through GDPR, and the instinct when it arrives is to hand the whole subject to the privacy team. That instinct produces purposes that are accurate about the law and wrong about the work. **The privacy team cannot declare a purpose on another team's behalf, because it does not know what that team does with the data.** Only manufacturing knows that GMP requires an operator's identity to stay in a batch record for the life of the record; only drug development knows that a trial's consent describes the analyses the protocol pre-specified; only the security team knows what its monitoring actually collects. So every domain declares its own purposes, and the privacy domain assures the lawful basis rather than authoring it.

That division shows in the pattern each purpose follows:

| Field | Who owns it |
|---|---|
| Display Name, Summary, Description, Scope, Usage | The domain that carries out the processing |
| `Legal` — the lawful basis and the special category condition | Written by the domain, assured by the Chief Privacy Officer |
| `Implications` — what the basis permits and forbids | Jointly, and this is where most of the value sits |

## Why the purposes are worth reading together

Gathered in one file rather than scattered across nine, three things become visible that are hard to see from inside any single domain.

**Several purposes exist to record a refusal.** The manufacturing batch attribution purpose exists largely to state that operator identity in a GMP record cannot be erased. The health and safety surveillance purpose states that forty-year exposure records cannot be erased either. The privacy consent records purpose states the inverse — that consent evidence survives the erasure of the data it authorised. Each is a conclusion someone would otherwise have to reach under time pressure when a data subject request arrives, and having them written down in advance is most of their value.

**Two purposes collect exactly the data that must not drive decisions.** Workforce equality monitoring and representativeness monitoring both process protected characteristics for the sole purpose of detecting inequity, and both are constrained so the data is structurally unavailable at the point of any individual decision. Their `Implications` are almost entirely prohibitions.

**The personalised medicine batch is where several purposes meet on one vessel.** For an autologous therapy the batch record is manufacturing data, health data about an identified patient, and — because the material is genetically modified — a biological hazard record. The `Personalised Product Manufacture` purpose is where the collision between GMP record completeness and the right to erasure is resolved, and it resolves it by pseudonymisation rather than by choosing a winner. That scenario is the subject of this directory's wider work.

## How to read the rest of this file

Part 1 holds the purposes themselves, grouped by the domain that declared them. Part 2 holds the `Link Governance Mechanism` commands connecting each purpose to the policy it implements — reading these tells you *why* each purpose exists. Part 3 holds the peer links to related policies. Part 4 places each purpose in its domain's folio, which is unchanged by gathering them here: a purpose declared by manufacturing still belongs to the Manufacturing Governance Lead.

---

## Part 1: The Purposes

### Privacy — declared by Faith Broker

___

## Create Data Processing Purpose

### Display Name
Consent and Lawful Basis Records Management

### Qualified Name
CocoPharma::DataProcessingPurpose::ConsentRecordsManagement

### Domain Identifier
Privacy

### Summary
Processing of personal data for the purpose of recording, maintaining, and evidencing the consent or other lawful basis under which each individual's data is held.

### Description
The obligation to demonstrate a lawful basis is itself a processing activity, and one that necessarily outlives the processing it authorises. A consent record must identify the individual, the consent given, when and how it was obtained, the version of the notice presented, and any subsequent withdrawal — and it must survive the deletion of the data it authorised, because the company may later need to show that it held the data lawfully. This produces the counter-intuitive position that erasing an individual's data does not erase the record that they once consented and then withdrew. Declaring this as a distinct purpose makes that position explicit rather than leaving it as an apparent contradiction of the erasure obligation. Consent records are also the source from which the record of processing activities is compiled, and from which purpose limitation is enforced when another team proposes a secondary use.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Article 7(1), which requires the controller to be able to demonstrate that consent was given, and Article 5(2) accountability. Consent records are retained after erasure of the underlying data to the extent needed to evidence lawful processing.

### Scope
Consent and lawful basis records for every individual whose personal data is processed by Coco Pharmaceuticals, including withdrawal records and the notice versions presented at the time.

### Implications
- Consent records survive erasure of the data they authorised, and this must be stated in privacy notices
- The notice version presented must be retained, not only the fact of consent
- Withdrawal must be recorded against the original consent rather than replacing it
- Consent records are the authoritative source for purpose limitation decisions on secondary use

### Usage
Applied to consent and lawful basis registers, to distinguish the retention of evidence from the retention of the personal data whose processing it authorises.

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

___

## Create Data Processing Purpose

### Display Name
Data Subject Request Fulfilment

### Qualified Name
CocoPharma::DataProcessingPurpose::DataSubjectRequestFulfilment

### Domain Identifier
Privacy

### Summary
Processing of a requester's personal data in order to verify their identity, locate the personal data held about them, and respond to an access, rectification, erasure, restriction, portability, or objection request.

### Description
Answering a data subject request requires processing the requester's personal data twice over: once to establish that they are who they claim to be, and again to search every system that might hold data about them. The search itself is intrusive — it touches records across research, manufacturing, clinical, and corporate systems — and it produces a compiled view of an individual that did not previously exist in one place. That compilation is retained only as long as needed to answer the request and to evidence that it was answered within the statutory period. Identity verification data is collected for that sole purpose and is not added to the individual's ongoing record. Where a request is refused in whole or in part, the reasoning is retained as evidence, since the requester may complain to the supervisory authority and the company must be able to show the basis on which it acted.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Articles 15 to 22, which require the controller to respond to data subject requests within one month. Identity verification data is processed on the same basis, limited to establishing entitlement to the request.

### Scope
Requester identity verification data, the compiled view of personal data assembled to answer a request, and the record of the response and its reasoning.

### Implications
- Compiled request responses are retained only for the period needed to evidence compliance, then deleted
- Identity verification data is not merged into the individual's ongoing records
- Refusal reasoning must be retained for the period in which a complaint may be brought
- The search itself must be logged, since it accesses personal data across every domain

### Usage
Applied to the data subject request case records and to the temporary compiled datasets assembled to answer requests, to distinguish this processing from the original purposes under which the data was collected.

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

___

## Create Data Processing Purpose

### Display Name
Personal Data Breach Investigation and Notification

### Qualified Name
CocoPharma::DataProcessingPurpose::PersonalDataBreachResponse

### Domain Identifier
Privacy

### Summary
Processing of personal data belonging to affected individuals in order to assess the scope and severity of a personal data breach, notify the supervisory authority, and where required inform the individuals concerned.

### Description
Investigating a breach requires establishing precisely whose data was affected and what categories were exposed, which means processing the very data whose confidentiality has already been compromised. This is unavoidable — a notification that cannot state the categories of data and the approximate number of individuals affected does not meet the Article 33 requirement — but it warrants explicit purpose declaration because the processing is intrusive, is carried out at speed under a 72-hour deadline, and frequently involves staff who would not ordinarily have access to the data in question. Access granted for investigation is time-limited and logged. The investigation record, including the assessment of risk to individuals and the decision on whether to notify them, is retained as evidence of the controller's reasoning, since supervisory authorities examine that reasoning rather than the outcome alone.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Articles 33 and 34, which require notification to the supervisory authority within 72 hours of becoming aware and communication to data subjects where the breach is likely to result in high risk to their rights and freedoms.

### Scope
Personal data of individuals affected by a suspected or confirmed breach, processed for the duration of the investigation and notification, together with the retained investigation and decision record.

### Implications
- Investigation access is time-limited, granted by named individual, and logged
- The assessment of risk to individuals must be recorded even where notification is not required
- Investigation records are retained separately from the affected individuals' ongoing records
- Staff granted investigation access may see data outside their normal authorisation and must be briefed accordingly

### Usage
Applied to breach investigation case records and the working datasets assembled during an investigation, to record the basis for processing that is otherwise outside the original collection purpose.

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

### Human Resource Management (22) — declared by Faith Broker

___

## Create Data Processing Purpose

### Display Name
Employment Relationship Administration

### Qualified Name
CocoPharma::DataProcessingPurpose::EmploymentRelationshipAdministration

### Domain Identifier
Human Resource Management

### Summary
Processing of employee and worker personal data for the purpose of administering the employment relationship — pay, benefits, absence, performance, competency, and the employment decisions taken during it.

### Description
This is the primary purpose under which workforce data is held, covering the whole relationship from offer through to the records retained after it ends. Two features distinguish it from an ordinary contractual purpose. First, a substantial part of the processing is not necessary for the contract at all but for compliance with employment, tax, health and safety, and medicines legislation, and the two bases have different consequences for whether the individual can object — which is why they are separated rather than described collectively as employment administration. Second, the imbalance of power in the employment relationship means consent is rarely a valid basis for anything the employer needs, so processing is grounded in contract, legal obligation, or legitimate interests with an assessment recorded, and consent is reserved for genuinely optional matters such as voluntary benefits. Competency and qualification records processed under this purpose are also relied upon by manufacturing and drug development for regulatory evidence, and their retention follows the regulated activity rather than the employment relationship, extending well beyond the individual's departure.

### Legal
Processing necessary for the performance of the employment contract under UK GDPR and EU GDPR Article 6(1)(b), and for compliance with legal obligations under Article 6(1)(c) arising from employment, tax, health and safety, and medicines legislation. Health data processed for absence management and occupational health relies on Article 9(2)(b) — obligations in the field of employment law. Consent is not relied upon for processing the employer requires, given the imbalance of power in the employment relationship.

### Scope
Personal data of employees, workers, and contractors, from offer through employment and into the retained records that follow it, including pay, benefits, absence, performance, competency, and employment decision records.

### Implications
- Contract and legal obligation bases must be distinguished, as they differ in objection rights
- Consent is reserved for genuinely optional processing, not used for required processing
- Competency records follow regulated activity retention, extending beyond employment
- Occupational health data requires separate handling and restricted access within HR
- Employment decision records are retained for the limitation period, not the employment period

### Usage
Applied to core HR, payroll, competency, and case management records, to record the basis on which workforce data is processed and the differing retention drivers that apply within it.

### Category
Human Resource Management

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Data Processing Purpose

### Display Name
Workforce Equality Monitoring and Pay Gap Reporting

### Qualified Name
CocoPharma::DataProcessingPurpose::WorkforceEqualityMonitoring

### Domain Identifier
Human Resource Management

### Summary
Processing of workforce diversity and pay data for the purpose of monitoring equality of opportunity, producing statutory pay gap reports, and answering individual comparative pay requests.

### Description
Equality monitoring requires the company to process exactly the characteristics it is prohibited from making decisions on, which is why this purpose is declared separately from employment administration and why its constraints are strict. Data on ethnicity, disability, sexual orientation, and religion is provided voluntarily, may be declined without consequence, and is held so that it cannot inform any individual employment decision — separated from the records managers see, and available for analysis only in aggregate. Analytical outputs are subject to minimum group sizes, because a breakdown of a small category can identify individuals as effectively as naming them. The purpose also covers the comparative pay information provided to individuals under transparency obligations, which is a disclosure of aggregated pay data about colleagues to a third party and requires the same minimum group protection: where a category is too small for the average to be meaningfully anonymous, the response explains that rather than disclosing it. Where analysis is conducted under legal privilege, the privileged material is held separately from the operational monitoring data.

### Legal
Processing for identifying or reviewing the existence or absence of equality of opportunity between groups, relying on the substantial public interest condition under UK GDPR Article 9(2)(g) and Schedule 1 of the Data Protection Act 2018, and equivalent member state provisions for the EU subsidiaries. Statutory pay gap reporting is processed under Article 6(1)(c) as a legal obligation. Diversity data is provided voluntarily and may be withheld or withdrawn without any effect on the employment relationship.

### Scope
Voluntarily provided diversity characteristics, pay and reward data, and equal-value categorisation, processed for aggregate analysis, statutory reporting, and individual comparative pay responses.

### Implications
- Diversity data must be held separately from records used in employment decisions
- Analytical outputs require minimum group sizes to prevent identification
- Comparative pay responses disclose colleagues' aggregated data and need the same protection
- Withholding diversity data must have no effect on the individual
- Privileged analysis is held separately from operational monitoring data

### Usage
Applied to diversity monitoring records, pay analysis datasets, and statutory reporting outputs, to record the basis for processing protected characteristics and the constraints that keep them out of employment decisions.

### Category
Human Resource Management

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Health and Safety (24) — declared by Faith Broker

___

## Create Data Processing Purpose

### Display Name
Occupational Health Surveillance and Exposure Records

### Qualified Name
CocoPharma::DataProcessingPurpose::OccupationalHealthSurveillance

### Domain Identifier
Health and Safety

### Summary
Processing of workers' health and exposure data for the purpose of detecting early indications of harm from occupational exposure, verifying that control measures are effective, and discharging statutory retention obligations.

### Description
This purpose covers the most sensitive personal data the company processes about its own workforce, and its constraints follow from the principle that surveillance serves the worker. Clinical findings are held by occupational health and are not accessible to management, which receives fitness conclusions and required adjustments only; the separation is enforced by system access rather than by undertaking. Exposure records are held against the individual because the retention obligation requires it and because reconstructing an individual's exposure history decades later is the purpose those records exist for. Erasure is not available for either category — health surveillance records must be retained for forty years from the last entry, and the exposure history that explains them must be retained with them — and this must be explained to individuals when surveillance begins rather than discovered by them when they request erasure after leaving. The retention long outlives the employment relationship, so the purpose also covers processing of data about former workers with whom the company has no current relationship, which is unusual and warrants the explicit statement. Contractors and agency workers are within scope on the same basis as employees.

### Legal
Processing necessary for compliance with legal obligations under UK GDPR and EU GDPR Article 6(1)(c) arising from the Control of Substances Hazardous to Health Regulations 2002 and member state transpositions of Directive 89/391/EEC. Health data is processed under Article 9(2)(b) — obligations in the field of employment and social protection law — and Article 9(2)(h) for occupational medicine and assessment of working capacity, under the responsibility of a health professional subject to an obligation of professional secrecy. Erasure is unavailable for the statutory retention period and this is stated to individuals at the point surveillance begins.

### Scope
Health surveillance records, exposure monitoring results attributed to individuals, and the linked exposure history, for employees, contractors, and agency workers, retained for forty years from the last entry.

### Implications
- Clinical findings are held by occupational health; management receives fitness conclusions only
- Erasure is unavailable for the statutory period and must be explained at the outset
- Processing continues for decades after the working relationship ends
- Contractors and agency workers are in scope on the same basis as employees
- Surveillance results are also control-effectiveness data and feed workplace investigation

### Usage
Applied to occupational health records, individual exposure histories, and the surveillance population register, to record the basis for processing health data about current and former workers and the separation from employment decision-making that bounds it.

### Category
Health and Safety

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Drug Development (20) — declared by Tessa Tube

___

## Create Data Processing Purpose

### Display Name
Clinical Trial Conduct and Analysis

### Qualified Name
CocoPharma::DataProcessingPurpose::ClinicalTrialConduct

### Domain Identifier
Drug Development

### Summary
Processing of trial participant data for the purpose of conducting the trial, analysing its results, and supporting the resulting regulatory submissions.

### Description
This purpose covers the processing that the trial itself requires: recording eligibility and consent, capturing visits, assessments, and outcomes, monitoring participant safety, analysing results against the protocol's endpoints, and submitting the resulting datasets to regulators. It is the primary purpose for which participants give their data and is described to them in the informed consent. Processing under this purpose is confined to the trial for which the data was collected — reuse in a different trial, or for a research question outside the protocol, falls under the secondary research purpose and requires its own basis. Special category health data and, for many Coco Pharmaceuticals trials, genetic data are both processed under this purpose, which sets the protection standard accordingly.

### Legal
Processing of special category health and genetic data for scientific research purposes, supported by the participant's explicit informed consent to trial participation and by the company's legal obligation to conduct and report trials under applicable clinical trial regulations. Withdrawal of consent stops further collection but does not require deletion of data already used in analyses supporting a submission, as required by clinical trial regulation; this is stated in the consent given to participants.

### Scope
Trial participant data collected under an approved protocol, from screening through to the final clinical study report and any resulting regulatory submission.

### Implications
- Processing must remain within the protocol under which the data was collected
- Consent withdrawal must stop further collection and be recorded against the participant
- The consent must state that data already used in submission analyses is retained
- Genetic data processed under this purpose requires controlled access throughout

### Usage
Applied to clinical trial datasets, case report form data, and safety data to record the basis on which participant data is processed and the boundary beyond which a further purpose is required.

### Category
Drug Development & Clinical Trials

### Authors
- Tessa Tube
- Tanya Tidie
- Callie Quartile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Data Processing Purpose

### Display Name
Secondary Research Use of Clinical Trial Data

### Qualified Name
CocoPharma::DataProcessingPurpose::SecondaryClinicalResearch

### Domain Identifier
Drug Development

### Summary
Processing of clinical trial data for research questions beyond the protocol under which it was collected, including pooled analyses, method development, and external collaboration.

### Description
Trial data has value beyond the trial that produced it. Pooling across studies supports safety analyses no single trial can power, and historical trial data underpins the modelling on which the personalised medicine programme depends. This purpose covers that reuse, and exists as a separate purpose precisely because reuse is not covered by the consent given for trial conduct. Processing under it requires either specific consent for future research, obtained at enrolment, or anonymisation sufficient that the data is no longer personal data — which for genomic data is not achievable, so genomic reuse always requires the consent route with controlled access. Where data is shared externally under this purpose, the anonymisation and controlled sharing approach governs the transformation and the recipient's obligations. Reuse under this purpose must be recorded against the source trial so that the company can establish what its data has been used for.

### Legal
Processing for scientific research purposes, supported either by the participant's specific consent to future research use given at enrolment, or by anonymisation to the point that the data no longer constitutes personal data. Genomic data cannot be anonymised to that standard and therefore requires the consent route with controlled access in all cases.

### Scope
Completed trial datasets reused for research questions outside their originating protocol, including internal pooled analyses, methodological development, and data shared with external research collaborators.

### Implications
- Reuse requires either future-research consent recorded at enrolment or verified anonymisation
- Genomic data reuse always requires consent and controlled access, never anonymisation alone
- Each reuse must be recorded against the source trial and its consent basis
- External sharing under this purpose is governed by the anonymisation and controlled sharing approach

### Usage
Applied to trial datasets entering pooled analyses, research collaborations, or model development, to record the basis for reuse and the consent constraints inherited from the source trial.

### Category
Drug Development & Clinical Trials

### Authors
- Tessa Tube
- Tanya Tidie
- Callie Quartile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Manufacturing — declared by Stew Faster

___

## Create Data Processing Purpose

### Display Name
Batch Record Attribution and Electronic Signature

### Qualified Name
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Domain Identifier
Manufacturing

### Summary
Processing of operator and reviewer identity within batch records and electronic signatures for the purpose of attributing every GMP-relevant action to the individual who performed it.

### Description
Attributability is the first requirement of ALCOA+ and the reason batch records carry names at all. Every weighing, addition, in-process check, deviation entry, and review is signed, and the signature identifies a person. This embeds personal data permanently in the regulatory record: it cannot be pseudonymised without destroying the attribution that makes the record compliant, and it cannot be erased on request, because the batch record must remain complete for its full retention period. Declaring this as a distinct processing purpose makes that constraint explicit and gives the privacy team a documented position to work from when a data subject request touches manufacturing records. Electronic signature records additionally capture the meaning of the signature — performed, checked, approved — since a signature without a stated meaning does not satisfy the electronic records requirements.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Article 6(1)(c), arising from EU GMP Annex 11, EU GMP Chapter 4, and FDA 21 CFR Part 11, which require GMP-relevant actions to be attributable to an identified individual and records to be retained complete. Erasure of attribution data is not available, as it would render the regulatory record non-compliant.

### Scope
Operator, reviewer, and approver identity recorded within batch records, electronic batch record systems, and electronic signature manifestations.

### Implications
- Attribution data cannot be erased or pseudonymised without breaching GMP record completeness
- Data subject erasure requests touching batch records must be refused on the legal obligation basis, with the reasoning recorded
- Electronic signatures must record the meaning of the signature alongside the identity
- Retention follows the batch record retention period, not employment or ordinary record schedules

### Usage
Applied to batch records and electronic signature stores, to record why attribution data is retained and why it is out of scope for erasure.

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

## Create Data Processing Purpose

### Display Name
Operator Qualification and Training Records

### Qualified Name
CocoPharma::DataProcessingPurpose::OperatorQualificationRecords

### Domain Identifier
Manufacturing

### Summary
Processing of production and quality staff personal data for the purpose of recording the training and qualification that authorises each individual to perform GMP-regulated activities.

### Description
GMP requires that personnel performing regulated activities are qualified to do so, and that the qualification is evidenced. The resulting records — training completion, competency assessment, authorisation to perform specific operations, and requalification history — are personal data about an identifiable employee, held for a regulatory purpose rather than an employment one. That distinction matters in practice: the records must be retained for the life of the batches the individual worked on, which substantially exceeds their employment and exceeds ordinary HR retention. An inspector examining a batch produced eight years ago will ask whether the operator who signed it was qualified at the time, and the answer must be available whether or not that person still works for the company. The records are used to establish regulatory authorisation and are not used for performance management, which follows a separate HR process on a separate basis.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Article 6(1)(c), arising from EU GMP Chapter 2 and equivalent FDA requirements that personnel performing GMP activities be qualified and that qualification be documented. Retention extends beyond employment for the period required to support the batch records the individual signed.

### Scope
Training, competency, authorisation, and requalification records for production, quality control, and quality assurance staff performing GMP-regulated activities.

### Implications
- Records are retained for the life of the batch records they support, beyond the end of employment
- Qualification records are used for regulatory authorisation, not for performance management
- Leavers' qualification records must remain retrievable and attributable
- Employees must be informed that qualification records outlive their employment and why

### Usage
Applied to the training and qualification record systems, to distinguish GMP-driven retention from ordinary HR record retention.

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

## Create Data Processing Purpose

### Display Name
Personalised Product Manufacture for an Identified Patient

### Qualified Name
CocoPharma::DataProcessingPurpose::PersonalisedManufacturing

### Domain Identifier
Manufacturing

### Summary
Processing of a patient's health data, and of material derived from them, for the purpose of manufacturing, testing, releasing, and delivering a medicinal product intended for that patient alone.

### Description
This purpose covers the processing that personalised manufacture requires and states the boundary that the identity minimisation principle enforces: manufacturing processes a pseudonymous reference and the technical data attached to it, while the mapping to the patient is processed clinically. Declaring it explicitly resolves a collision that would otherwise sit unaddressed between two obligations the company already holds. The batch record attribution purpose states that attribution data cannot be erased, because a GMP record must remain complete for its retention period. For a conventional batch that is uncontroversial, since the identities involved are those of operators acting in their employment. For a personalised batch it would appear to mean that a patient's identity is embedded permanently in a manufacturing record and is beyond the reach of an erasure request. Pseudonymisation is what dissolves the apparent conflict: the manufacturing record contains a reference, which stays complete and unerasable as GMP requires, while the identifying mapping is held clinically under clinical retention rules and is not part of the batch record. The conflict is reduced rather than eliminated, and honestly stated: the mapping cannot be erased on request either, because a recall or a safety signal years later must be traceable to the people who received the product, and that retention is justified under the same public-interest basis as pharmacovigilance rather than under manufacturing necessity.

### Legal
Processing necessary for compliance with legal obligations under UK GDPR and EU GDPR Article 6(1)(c) arising from GMP and medicinal product safety legislation, with special category health data processed under Article 9(2)(i) — public interest in the area of public health, ensuring high standards of quality and safety of medicinal products. Processing of the patient's own starting material additionally relies on the explicit consent given for the treatment. Erasure is not available for the batch record or for the reference-to-patient mapping, as both are required for recall and pharmacovigilance traceability; this is stated to the patient at consent.

### Scope
The pseudonymous batch reference and associated technical data processed in manufacturing systems, the patient-derived starting material, and the reference-to-patient mapping held in clinical systems for the retention period required for recall and safety follow-up.

### Implications
- Manufacturing systems process the reference only; identity fields are absent by design
- Erasure is unavailable for both the batch record and the mapping, and this must be stated at consent
- Contract manufacturers and logistics providers are processors receiving the reference, and require Article 28 agreements
- Product type may disclose the condition, so the reference alone is not full de-identification
- Cross-border movement of personalised batches engages the international transfer obligations

### Usage
Applied to personalised manufacturing records, chain of identity records, and the clinical reference mapping, to record the basis for processing patient health data in a manufacturing context and the limits placed on it.

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

### Diversity, Equity and Inclusion (23) — declared by Faith Broker

___

## Create Data Processing Purpose

### Display Name
Representativeness and Equity Monitoring

### Qualified Name
CocoPharma::DataProcessingPurpose::RepresentativenessAndEquityMonitoring

### Domain Identifier
Diversity, Equity and Inclusion

### Summary
Processing of demographic data about trial participants, patients, investigators, and suppliers for the purpose of measuring representativeness and detecting differential outcomes between groups.

### Description
This purpose covers processing that exists solely to find inequity, and its constraints follow from that narrow aim. Demographic data processed under it is used for aggregate analysis and for the enrolment monitoring that trial targets require; it is not available at the point of any individual decision about enrolment, treatment, engagement, or contract award, and the separation is enforced by system design rather than by policy. Trial participant demographic data is collected under the trial's own consent and is processed here for monitoring and for the subgroup analyses the protocol pre-specifies, which is within the originating purpose rather than a secondary use. Aggregate outputs carry minimum group sizes, and the constraint bites harder here than in workforce reporting because trial subgroups are small by construction — a breakdown of eleven participants by two characteristics identifies people. Where demographic data is used to test a model for differential performance, it is used to evaluate the model and is never supplied to it as an input feature. The workforce half of representation monitoring is processed under the HR purpose and is consumed here in aggregate rather than re-collected.

### Legal
Processing for scientific research purposes and for identifying or reviewing the existence or absence of equality of opportunity, relying on Article 9(2)(j) for trial demographic data processed as part of research, and on the substantial public interest conditions under UK GDPR Article 9(2)(g) and Schedule 1 of the Data Protection Act 2018 and equivalent member state provisions for equality monitoring. Trial participant demographic data is additionally covered by the explicit consent given for trial participation, which describes the monitoring and subgroup analysis purposes.

### Scope
Demographic data of clinical trial participants, patients using company services, clinical investigators, and supplier personnel, processed in aggregate for representativeness measurement and differential outcome detection.

### Implications
- Demographic data is unavailable at the point of individual decisions, enforced by design
- Minimum group sizes apply and bite harder for trial subgroups than for workforce reporting
- Demographic data evaluates models and is never supplied to them as an input feature
- Workforce representation is consumed in aggregate from HR, not separately collected
- Trial monitoring is within the originating consent, not a secondary research use

### Usage
Applied to enrolment monitoring datasets, equity analysis outputs, and model evaluation datasets, to record the basis for processing demographic data and the separation from decision-making that bounds it.

### Category
Diversity, Equity and Inclusion

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Security — declared by Ivor Padlock

___

## Create Data Processing Purpose

### Display Name
Identity and Access Administration

### Qualified Name
CocoPharma::DataProcessingPurpose::IdentityAndAccessAdministration

### Domain Identifier
Security

### Summary
Processing of employee, contractor, and partner personal data for the purpose of establishing identity, provisioning access, maintaining entitlements, and revoking access when it is no longer required.

### Description
Every access control in the organisation rests on an identity record, and every identity record is personal data. The purpose covers the identity lifecycle: establishing who an individual is at onboarding, provisioning the entitlements their role requires, recording each subsequent change, and removing access when they leave or move. Entitlement records are the evidence base for access reviews and for the authentication and accountability obligation, which means they must be retained after an individual departs — a leaver's historical entitlements are needed to interpret the audit trails they generated while employed. Identity data is deliberately minimal: enough to distinguish individuals reliably and to route approvals, and no more. Where identity is federated from a partner organisation, the same minimisation applies and the partner's data is not enriched with information the company does not need.

### Legal
Processing necessary for the performance of a contract of employment or engagement under UK GDPR and EU GDPR Article 6(1)(b), and for compliance with the controller's legal and regulatory obligations to control access to regulated systems under Article 6(1)(c). Historical entitlement records are retained on the legitimate interests basis for the period required to interpret retained audit trails.

### Scope
Identity records, role and entitlement assignments, access approval records, and access revocation records for employees, contractors, and federated partner users.

### Implications
- Identity records are limited to what is required to distinguish individuals and route approvals
- Historical entitlements are retained after departure for as long as the audit trails they explain
- Federated partner identities are subject to the same minimisation as internal records
- Entitlement change records must identify the approver, not only the change

### Usage
Applied to identity stores, entitlement registers, and access approval records, to record the basis on which staff personal data underpins access control.

### Category
Security & Resilience

### Authors
- Ivor Padlock
- Sidney Seeker
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Data Processing Purpose

### Display Name
Security Monitoring and Incident Investigation

### Qualified Name
CocoPharma::DataProcessingPurpose::SecurityMonitoringAndInvestigation

### Domain Identifier
Security

### Summary
Processing of employee and third-party personal data contained in system logs, access records, and endpoint telemetry for the purpose of detecting, investigating, and responding to security incidents.

### Description
Security monitoring is, in data protection terms, systematic observation of identifiable individuals at work. Authentication logs record who accessed what and when; endpoint telemetry records process execution and file access; network monitoring records destinations visited. Each is collected to protect the organisation rather than to assess the individual, and that distinction is what keeps the processing proportionate — monitoring data is used to investigate security events, not to evaluate performance or conduct unrelated to security. Where an investigation does reveal misconduct, escalation to HR follows a defined route rather than the security team acting on it directly, and the individual retains the rights that any disciplinary process affords. Access to monitoring data is restricted to the security operations team, is logged, and is itself subject to review. Retention is set to the period over which incidents are realistically detected and investigated, not to the maximum the systems can hold.

### Legal
Processing necessary for the purposes of the legitimate interests pursued by the controller under UK GDPR and EU GDPR Article 6(1)(f) — namely network and information security — as recognised in Recital 49. A legitimate interests assessment is recorded, and employees are informed that monitoring takes place, what is collected, and for what purpose.

### Scope
System, application, authentication, network, and endpoint logs across Coco Pharmaceuticals systems, and the investigation records derived from them.

### Implications
- A legitimate interests assessment must be recorded and reviewed when monitoring scope changes
- Employees must be informed that monitoring occurs and what it covers
- Monitoring data must not be used to assess performance or conduct unrelated to security
- Findings indicating misconduct follow a defined escalation route rather than direct action by the security team
- Access to monitoring data is restricted, logged, and periodically reviewed

### Usage
Applied to log and telemetry stores and to security investigation case records, to distinguish security processing from the operational purposes of the systems generating the data.

### Category
Security & Resilience

### Authors
- Ivor Padlock
- Sidney Seeker
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Corporate — declared by Reggie Mint

___

## Create Data Processing Purpose

### Display Name
Third-Party Due Diligence and Screening

### Qualified Name
CocoPharma::DataProcessingPurpose::ThirdPartyDueDiligenceScreening

### Domain Identifier
Corporate

### Summary
Processing of personal data belonging to directors, beneficial owners, and key personnel of third parties for the purpose of verifying identity, screening against sanctions and politically exposed person lists, and assessing bribery and fraud risk.

### Description
Due diligence necessarily processes personal data about people who are not employees, customers, or trial participants, and who have no direct relationship with Coco Pharmaceuticals — the beneficial owner of a supplier three ownership layers up has not chosen to deal with the company at all. The processing includes screening against sanctions designations, politically exposed person status, and adverse media, all of which may produce findings that are unfavourable, contested, or simply wrong: adverse media screening in particular returns allegations rather than findings, and name-matching produces false positives against individuals who share a name with a sanctioned party. The purpose therefore constrains the processing tightly. Screening results are treated as an input to a human assessment rather than as a decision, no third party is refused solely on an automated match, and a match that is discounted is recorded as discounted with the reasoning, so that the same false positive is not re-raised at every rescreening. Screening data is retained as evidence supporting the adequate procedures defence, which means it outlives the relationship it assessed.

### Legal
Processing necessary for compliance with legal obligations under UK GDPR and EU GDPR Article 6(1)(c) — sanctions compliance and the Bribery Act duty to prevent bribery — and for the legitimate interests of the controller under Article 6(1)(f) in preventing fraud, as recognised in Recital 47. Criminal offence data arising from adverse media screening is processed under the substantial public interest condition for preventing unlawful acts. A legitimate interests assessment and an appropriate policy document are maintained.

### Scope
Personal data of directors, beneficial owners, and key personnel of third parties, processed at onboarding and at each rescreening, together with the retained screening results and assessment reasoning.

### Implications
- No third party may be refused solely on an automated screening match; human assessment is required
- Discounted matches must be recorded with reasoning so they are not re-raised at each rescreening
- Adverse media findings are allegations and must be recorded and treated as such
- Screening evidence is retained beyond the end of the relationship to support the adequate procedures defence
- Individuals screened have rights under data protection law despite having no direct relationship with the company

### Usage
Applied to third-party due diligence case records and screening result stores, to record the basis for processing personal data of individuals who are not counterparties to any agreement with the company.

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Data Processing Purpose

### Display Name
Transfer of Value Recording and Public Disclosure

### Qualified Name
CocoPharma::DataProcessingPurpose::TransferOfValueDisclosure

### Domain Identifier
Corporate

### Summary
Processing of healthcare professionals' personal data for the purpose of recording transfers of value made to them and publishing those transfers as required by transparency regimes.

### Description
This purpose is unusual in that its end point is deliberate publication of personal data. A named clinician's fees, hospitality, and expenses are placed in the public domain, attributed to them, because transparency regimes require it and because the alternative — undisclosed payments between manufacturers and prescribers — is what those regimes exist to prevent. The processing therefore has to be handled with more care than its regulatory mandate alone might suggest. Recipient identity must be resolved to a single authoritative record before publication, since attributing a payment to the wrong clinician is a serious injustice that is difficult to correct once published and indexed. Recipients are given the opportunity to review their attributed transfers before publication and to challenge errors. Where a jurisdiction requires consent for individual attribution and consent is withheld, the transfer is disclosed in aggregate instead, and the withholding must not affect the commercial relationship. The purpose covers the internal recording as well as the publication, because the record assembled for disclosure combines payments from several systems into a profile of an individual's financial relationship with the company that exists nowhere else.

### Legal
Processing necessary for compliance with a legal obligation under UK GDPR and EU GDPR Article 6(1)(c) where disclosure is mandated by law, and on the basis of the recipient's consent under Article 6(1)(a) in jurisdictions where individual attribution requires it. Withdrawal of consent results in aggregate rather than individual disclosure and must not affect the commercial relationship.

### Scope
Healthcare professional and healthcare organisation identity and payment data, from capture in the originating systems through consolidation to public disclosure and the retained disclosure record.

### Implications
- Recipient identity must be resolved authoritatively before publication to prevent misattribution
- Recipients must be able to review and challenge their attributed transfers before publication
- Consent withdrawal results in aggregate disclosure and must not affect the commercial relationship
- The consolidated record constitutes a profile that must be access-controlled internally
- Published records must be correctable after publication, with a defined correction route

### Usage
Applied to transfer of value records, the consolidated disclosure dataset, and published disclosure files, to record the basis for assembling and publishing personal data about individuals outside the company.

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Data — declared by Jules Keeper

___

## Create Data Processing Purpose

### Display Name
Data Quality Profiling and Catalog Metadata Generation

### Qualified Name
CocoPharma::DataProcessingPurpose::DataQualityProfilingAndCataloguing

### Domain Identifier
Data

### Summary
Processing of personal data held in governed systems for the purpose of profiling its quality, generating catalog metadata, and detecting its presence in systems where it has not been declared.

### Description
Measuring quality means reading the data. A completeness check counts populated fields, a validity check compares values against an expected pattern, and a discovery scan looks at content in order to recognise that a column contains national insurance numbers or dates of birth. Where the underlying data is personal, all of this is processing, carried out by the data team rather than by the domain that collected it, and for a purpose the individual was never told about. That warrants an explicit declaration. The processing is deliberately constrained: profiling reads data to compute aggregate statistics and metadata, and does not retain the values it read; discovery scanning records that a system holds a category of personal data, not the personal data itself. Where a profiling result would itself be identifying — an outlier report naming individuals, a sample of failing records — it is treated as personal data in its own right, retained under the classification of its source, and access is restricted to the steward resolving the issue. This purpose does not authorise analysis of individuals; it authorises analysis of data about how well data is being managed.

### Legal
Processing necessary for the purposes of the legitimate interests pursued by the controller under UK GDPR and EU GDPR Article 6(1)(f) — namely ensuring the accuracy of personal data as required by Article 5(1)(d), and identifying where personal data is held so that data subject rights can be honoured. A legitimate interests assessment is recorded. Special category data is profiled only where the assessment establishes that quality or discovery cannot be achieved by other means.

### Scope
Personal data held in systems within the scope of quality monitoring and automated discovery, processed to produce aggregate quality measurements, catalog metadata, and classification findings.

### Implications
- Profiling retains aggregate results and metadata, not the values read
- Discovery scanning records the presence and category of personal data, not its content
- Identifying profiling outputs, such as failing-record samples, inherit the classification of their source and have restricted access
- A legitimate interests assessment must be recorded and reviewed when profiling scope extends to special category data
- This purpose does not authorise analysis of individuals, only of data management quality

### Usage
Applied to quality profiling jobs, discovery scans, and the catalog metadata they produce, to record the basis on which the data team processes personal data belonging to other domains' collections.

### Category
Data Governance

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Mechanisms — the policy each purpose implements

Each link below records a governance policy whose implementation depends on the purpose named. Read together, they answer the question a purpose alone does not: what obligation made this declaration necessary.

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Mechanism
CocoPharma::DataProcessingPurpose::TransferOfValueDisclosure

### Rationale
Publication of a named clinician's payments is processing that requires its own declared basis; the purpose records it and constrains how attribution is resolved.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Mechanism
CocoPharma::DataProcessingPurpose::ThirdPartyDueDiligenceScreening

### Rationale
Screening processes personal data of people with no relationship to the company. The purpose is the control that bounds it and forbids automated refusal.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Mechanism
CocoPharma::DataProcessingPurpose::ThirdPartyDueDiligenceScreening

### Rationale
Monitoring rules that compare payment accounts against employee bank details process employee personal data, which requires a recorded basis and restricted access.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Mechanism
CocoPharma::DataProcessingPurpose::DataQualityProfilingAndCataloguing

### Rationale
Discovery scanning finds unregistered assets by examining their contents. The purpose is the control that makes that examination lawful where the contents are personal data.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Mechanism
CocoPharma::DataProcessingPurpose::DataQualityProfilingAndCataloguing

### Rationale
Automated monitoring reads personal data to compute quality measurements. The purpose bounds what may be retained from that reading and what may not.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Mechanism
CocoPharma::DataProcessingPurpose::DataQualityProfilingAndCataloguing

### Rationale
Profiling outputs that identify individuals inherit their source classification under this purpose, which is the principle applied to the data team's own derived data.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::SecurityIncidentsLoggedReportedReviewed

### Mechanism
CocoPharma::DataProcessingPurpose::SecurityMonitoringAndInvestigation

### Rationale
The obligation requires incidents to be logged and investigated; the purpose is the control that makes the underlying processing of employee data lawful and bounded.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::RiskBasedInformationSecurityManagement

### Mechanism
CocoPharma::DataProcessingPurpose::SecurityMonitoringAndInvestigation

### Rationale
Risk-based management determines how much monitoring is proportionate. The purpose records the assessment that justifies the monitoring actually carried out.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Mechanism
CocoPharma::DataProcessingPurpose::IdentityAndAccessAdministration

### Rationale
Authentication and accountability rest on identity records that are themselves personal data. The purpose governs their collection, minimisation, and retention.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::SupplierSecurityRiskAssessment

### Mechanism
CocoPharma::DataProcessingPurpose::IdentityAndAccessAdministration

### Rationale
Third-party access is provisioned through the same identity lifecycle, so supplier personnel data falls under this purpose and its minimisation requirements.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::EquityImpactAssessment

### Mechanism
CocoPharma::DataProcessingPurpose::RepresentativenessAndEquityMonitoring

### Rationale
Assessing differential effect requires processing the characteristics the assessment is about; the purpose records the basis and the separation from decision-making.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DemographicDataForEquityNotAccess

### Mechanism
CocoPharma::DataProcessingPurpose::RepresentativenessAndEquityMonitoring

### Rationale
The purpose is where the principle's separation between measurement and decision is recorded as an enforceable constraint rather than an intention.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Mechanism
CocoPharma::DataProcessingPurpose::ClinicalTrialConduct

### Rationale
The principle requires protection to be designed into how participant data is handled. The processing purpose is the control that records what the data may be used for, making the boundary of permitted processing explicit rather than implicit in the protocol.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Mechanism
CocoPharma::DataProcessingPurpose::SecondaryClinicalResearch

### Rationale
Reuse beyond the originating protocol is permitted only under this purpose, and the purpose states which route applies — future-research consent or verified anonymisation. The approach governs the transformation; the purpose governs whether the reuse is allowed at all.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Mechanism
CocoPharma::DataProcessingPurpose::ClinicalTrialConduct

### Rationale
The purpose records that data already used in submission analyses is retained despite consent withdrawal, which is what reconciles the 25-year retention obligation with participants' right to withdraw.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Mechanism
CocoPharma::DataProcessingPurpose::OccupationalHealthSurveillance

### Rationale
The purpose records the separation between clinical findings and management information as an enforceable constraint, and states the erasure position the retention creates.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Mechanism
CocoPharma::DataProcessingPurpose::EmploymentRelationshipAdministration

### Rationale
The purpose records the basis on which decision records are held and the retention that the limitation period requires.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Mechanism
CocoPharma::DataProcessingPurpose::WorkforceEqualityMonitoring

### Rationale
Analysing outcomes by protected characteristic requires processing exactly the data that must not inform decisions; the purpose is the control that keeps the two apart.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Mechanism
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Rationale
Attributability is the first ALCOA+ attribute and is achieved by embedding identity in the record. The purpose records why that personal data is held and why it cannot be removed.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Mechanism
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Rationale
Record completeness and attribution retention are the same obligation viewed from the data protection side; the purpose is the control that reconciles them with erasure rights.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Mechanism
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Rationale
Annex 11 and Part 11 require electronic signatures to identify the signer and state the meaning of the signature. The purpose governs that identity data.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Mechanism
CocoPharma::DataProcessingPurpose::OperatorQualificationRecords

### Rationale
Equipment qualification is meaningless without qualified operators; the personnel qualification records that evidence this are governed by this purpose.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Mechanism
CocoPharma::DataProcessingPurpose::PersonalisedManufacturing

### Rationale
The purpose is the control that records the legal basis and states the boundary the principle enforces, including the erasure position it produces.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Mechanism
CocoPharma::DataProcessingPurpose::DataSubjectRequestFulfilment

### Rationale
The approach defines how requests are handled; the purpose records the basis on which the request itself may be processed and how long the compiled response is kept.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Mechanism
CocoPharma::DataProcessingPurpose::PersonalDataBreachResponse

### Rationale
Meeting the 72-hour deadline requires processing affected individuals' data at speed and outside normal authorisation. The purpose is the control that makes that processing lawful and bounded.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ConsentAndLawfulBasisManagement

### Mechanism
CocoPharma::DataProcessingPurpose::ConsentRecordsManagement

### Rationale
The approach manages consent operationally; the purpose records why consent evidence is retained after the data it authorised has been erased.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::LawfulBasisDocumented

### Mechanism
CocoPharma::DataProcessingPurpose::ConsentRecordsManagement

### Rationale
The principle requires a documented basis for all processing. The consent records purpose is where that documentation is itself held and governed.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::PurposeLimitation

### Mechanism
CocoPharma::DataProcessingPurpose::DataSubjectRequestFulfilment

### Rationale
Request fulfilment processes data outside the purpose for which it was collected. Declaring it as a distinct purpose is how purpose limitation is honoured rather than quietly breached.

___

---

## Part 3: Peer Policy Links

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DemographicDataForEquityNotAccess

### Mechanism
CocoPharma::DataProcessingPurpose::WorkforceEqualityMonitoring

### Rationale
The HR purpose applies this principle to employment data and this domain applies it to clinical and patient data. The constraint is identical — collect to measure, structurally prevent from deciding — and stating it once in each domain keeps ownership clear without duplicating the control.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Mechanism
CocoPharma::DataProcessingPurpose::OccupationalHealthSurveillance

### Rationale
Fitness conclusions from surveillance can restrict what an individual may do, which makes them an input to the authorisation HR records. The clinical finding stays with occupational health; only the restriction reaches the competency record.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::QualificationRecordsAuthoritative

### Mechanism
CocoPharma::DataProcessingPurpose::OperatorQualificationRecords

### Rationale
Manufacturing declares the GMP purpose for which operator qualification records are held and retained beyond employment; HR holds the record itself and is accountable for its currency. The two describe one dataset from either side of the domain boundary.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Mechanism
CocoPharma::DataProcessingPurpose::IdentityAndAccessAdministration

### Rationale
The identity lifecycle is driven entirely by HR events, so security's ability to provision and revoke correctly is bounded by the timeliness of the feed it receives.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DataMinimisation

### Mechanism
CocoPharma::DataProcessingPurpose::WorkforceEqualityMonitoring

### Rationale
Equality monitoring is a deliberate exception to minimisation, justified by the substantial public interest in identifying inequality of opportunity and bounded by voluntary provision, separation from decision records, and minimum group sizes.

___

---

## Part 4: Folio Membership

Gathering the purposes into one file does not move their ownership. Each remains a member of the folio of the domain that declared it.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::DataProcessingPurpose::ThirdPartyDueDiligenceScreening

### Membership Rationale
The basis for processing third-party personal data during screening is declared by the finance team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::DataProcessingPurpose::TransferOfValueDisclosure

### Membership Rationale
The basis for recording and publishing healthcare professionals' payment data is declared by the finance team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::DataProcessingPurpose::DataQualityProfilingAndCataloguing

### Membership Rationale
The Chief Data Officer owns the legitimate interests basis on which the data team profiles and scans personal data belonging to other domains' collections.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::DataProcessingPurpose::SecurityMonitoringAndInvestigation

### Membership Rationale
The CISO owns the legitimate interests basis for security monitoring and the proportionality assessment supporting it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfDiversityEquityInclusion

### Element Id
CocoPharma::DataProcessingPurpose::RepresentativenessAndEquityMonitoring

### Membership Rationale
The basis for processing demographic data to detect inequity is declared by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::DataProcessingPurpose::ClinicalTrialConduct

### Membership Rationale
The primary processing purpose for trial participant data is defined in this domain, with the lawful basis assured by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::DataProcessingPurpose::SecondaryClinicalResearch

### Membership Rationale
Reuse of trial data beyond its originating protocol is authorised in this domain and constrained by the consent recorded at enrolment.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::DataProcessingPurpose::OccupationalHealthSurveillance

### Membership Rationale
The basis for processing worker health and exposure data is declared by this domain, with lawful basis assured by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::DataProcessingPurpose::EmploymentRelationshipAdministration

### Membership Rationale
The primary employment processing purpose is declared by HR, with lawful basis assured by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::DataProcessingPurpose::WorkforceEqualityMonitoring

### Membership Rationale
Equality monitoring processing is declared by HR and its constraints enforced within the HR function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::DataProcessingPurpose::OperatorQualificationRecords

### Membership Rationale
The Manufacturing Governance Lead owns the GMP basis on which staff qualification records are retained beyond employment.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::DataProcessingPurpose::BatchRecordAttribution

### Membership Rationale
Attribution data embedded in batch records is a manufacturing responsibility and is the documented basis for refusing erasure of GMP records.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::DataProcessingPurpose::PersonalisedManufacturing

### Membership Rationale
The basis for processing patient health data in manufacturing is declared by the manufacturing team, with lawful basis assured by privacy.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::DataProcessingPurpose::DataSubjectRequestFulfilment

### Membership Rationale
The Chief Privacy Officer owns the purpose under which data subject requests are processed, including the retention of compiled responses.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::DataProcessingPurpose::PersonalDataBreachResponse

### Membership Rationale
Breach investigation processing is carried out under the Chief Privacy Officer's authority and within the statutory notification deadline.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::DataProcessingPurpose::ConsentRecordsManagement

### Membership Rationale
Consent and lawful basis evidence is maintained by the privacy team and is the source for accountability reporting.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::DataProcessingPurpose::IdentityAndAccessAdministration

### Membership Rationale
Identity and entitlement data underpins every access control in the ISMS and is governed by the CISO.

### Membership Status
VALIDATED

___

---

## Appendix: Where each purpose came from

| Purpose | Domain | Declared in |
|---|---|---|
| Consent and Lawful Basis Records Management | `Privacy` | `privacy-governance-program.md` |
| Data Subject Request Fulfilment | `Privacy` | `privacy-governance-program.md` |
| Personal Data Breach Investigation and Notification | `Privacy` | `privacy-governance-program.md` |
| Employment Relationship Administration | `Human Resource Management` | `human-resource-management.md` |
| Workforce Equality Monitoring and Pay Gap Reporting | `Human Resource Management` | `human-resource-management.md` |
| Occupational Health Surveillance and Exposure Records | `Health and Safety` | `health-and-safety.md` |
| Clinical Trial Conduct and Analysis | `Drug Development` | `drug-development-governance.md` |
| Secondary Research Use of Clinical Trial Data | `Drug Development` | `drug-development-governance.md` |
| Batch Record Attribution and Electronic Signature | `Manufacturing` | `manufacturing-governance-program.md` |
| Operator Qualification and Training Records | `Manufacturing` | `manufacturing-governance-program.md` |
| Personalised Product Manufacture for an Identified Patient | `Manufacturing` | `manufacturing-governance-program.md` |
| Representativeness and Equity Monitoring | `Diversity, Equity and Inclusion` | `diversity-equity-inclusion.md` |
| Identity and Access Administration | `Security` | `data-security-strategy.md` |
| Security Monitoring and Incident Investigation | `Security` | `data-security-strategy.md` |
| Third-Party Due Diligence and Screening | `Corporate` | `corporate-governance-program.md` |
| Transfer of Value Recording and Public Disclosure | `Corporate` | `corporate-governance-program.md` |
| Data Quality Profiling and Catalog Metadata Generation | `Data` | `data-governance-program.md` |

Each of those files retains a pointer to this one in place of the section its purposes used to occupy.
