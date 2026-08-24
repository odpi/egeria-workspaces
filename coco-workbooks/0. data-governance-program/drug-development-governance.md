# Coco Pharmaceuticals — Drug Development Governance Program

> **Author:** Tessa Tube (Drug Development Lead), Tanya Tidie (Clinical Record Clerk), Callie Quartile (Data Scientist)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-22  
> **Description:** Governance definitions for the Drug Development domain (domain identifier `20`) at Coco Pharmaceuticals. This file extends the foundation in `joint-governance-officer-definitions.md` — which defines the FDA Clinical Trial Regulations driver, the Drug Development Lead role, and the Drug Development Lead governance folio — with the clinical trial and research data governance policies, controls, and metrics needed to operationalise Good Clinical Practice. All definitions created here are added to the existing Drug Development Lead folio.

---

## Overview

Coco Pharmaceuticals runs clinical trials as the evidential backbone of its drug development pipeline. Every regulatory submission the company makes rests on trial data being attributable, complete, and reconstructable years after the fact — and, increasingly, on that data being reusable across the personalised medicine programme without compromising the participants who provided it.

The `joint-governance-officer-definitions.md` foundation captured the FDA clinical trial regulations as a governance driver and appointed Tessa Tube as Drug Development Lead, but left the domain otherwise unpopulated: a single folio member and no policies, controls, or metrics. This file fills that gap. It covers three layers:

1. **Governance Drivers** — the clinical trial regulations and business imperatives that motivate governance activity in this domain.
2. **Governance Policies** — the principles, obligations, and approaches defining how clinical and research data is captured, protected, and retained.
3. **Governance Controls** — the roles, metrics, certification, and processing purposes that operationalise those policies day-to-day.

All definitions in this file carry Domain Identifier `20` (Drug Development) and become members of the Drug Development Lead Governance Folio, which already exists and is already registered in the root collection — this file adds members to it rather than recreating it.

Two definitions relevant to this domain live in `risk-register.md` and are retagged to domain `20`: the `ClinicalTrialDataIntegrityFailure` threat and the `ClinicalTrialDataIntegrityLoss` risk. They are added to the folio in Part 6.

Trials also make the group's structure operationally relevant: sites sit in the UK and the EU, the sponsor entity determines controllership, and data consolidates into a US-held database. The controllership and transfer obligations governing this are owned by the privacy domain; Part 4.5 records how the policies here depend on them.

---

## Part 1: Governance Drivers — Drug Development Domain

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Clinical Trial Data Reliability

### Qualified Name
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Domain Identifier
20

### Summary
Coco Pharmaceuticals must be able to stand behind every figure in a regulatory submission, tracing it back to the participant, the visit, and the instrument that produced it.

### Description
A drug approval is only as sound as the trial data supporting it. When a regulator questions an efficacy figure, the company must be able to reconstruct how that figure was derived — from the source record at the investigator site, through the case report form, into the statistical analysis dataset, and out into the submission. Any break in that chain puts the submission, and potentially an existing approval, at risk. Reliability here is not merely an absence of fraud: it means data that is captured once, captured correctly, and never silently altered. As trial designs grow more complex and more data arrives from wearables, home monitoring, and decentralised sites, maintaining that chain requires deliberate governance rather than the diligence of individual study teams.

### Implications
- Every clinical data point must have an identifiable source and an audit trail from source to submission
- Investigator sites must be qualified and monitored against a defined data quality standard
- Changes to analysis datasets after database lock require documented justification and approval
- Data flowing from third-party vendors and devices must meet the same standards as directly captured data

### Outcomes
- Regulatory submissions withstand inspection without data-related findings
- Efficacy and safety conclusions can be independently reconstructed from retained records
- Trial results can be reused with confidence in later submissions and post-marketing commitments

### Importance
Critical

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

## Create Business Imperative

### Display Name
Accelerated Time to Regulatory Submission

### Qualified Name
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Domain Identifier
20

### Summary
Coco Pharmaceuticals must shorten the interval between last patient visit and regulatory submission without weakening the data controls that make the submission defensible.

### Description
The gap between a trial completing and a submission being filed is dominated by data work: query resolution, reconciliation between systems, coding of adverse events and medications, and the assembly of standardised analysis datasets. Much of that work is repeated from trial to trial because data arrives in inconsistent shapes and must be reshaped by hand each time. Standardising clinical data structures at the point of capture, rather than remediating them at the end, converts weeks of reconciliation into an automated step. This imperative matters commercially — earlier submission means earlier patient access and a longer effective patent life — and it matters for the personalised medicine transition, where trial cycles are shorter and more numerous, so per-trial overheads compound.

### Implications
- Clinical data must be captured against agreed standard structures rather than trial-specific formats
- Query management and source data verification must run continuously through the trial, not only at database lock
- Metadata describing datasets, variables, and derivations must be maintained as trial assets in their own right

### Outcomes
- Database lock to submission-ready datasets is measured in days rather than weeks
- Submission assembly is repeatable across trials and less dependent on individual expertise
- Trial data is reusable for pooled analyses and post-marketing commitments without re-mapping

### Importance
High

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

### 1.2 Threats

The `risk-register.md` file already defines the Clinical Trial Data Integrity Failure threat (`CocoPharma::Threat::ClinicalTrialDataIntegrityFailure`), now carrying domain identifier `20`. The threats below cover the two remaining drug development exposures that were not represented as drivers.

___

## Create Threat

### Display Name
Re-identification of Clinical Trial Participants

### Qualified Name
CocoPharma::Threat::ClinicalTrialParticipantReidentification

### Domain Identifier
20

### Summary
Individuals who took part in a clinical trial may be re-identified from data that was believed to be anonymised, particularly where genomic or rare-condition data is shared or published.

### Description
Clinical trial datasets are shared widely — with regulators, with academic collaborators, with journals as a condition of publication, and increasingly through data-sharing platforms mandated by funders. Pseudonymisation by subject identifier is not sufficient protection for these uses. A trial cohort is small by construction, and the combination of site, age band, visit dates, and condition can single out an individual even without direct identifiers. Genomic data, central to Coco Pharmaceuticals' personalised medicine work, is inherently identifying and cannot be anonymised by removing fields. The exposure is greatest at the boundary between the drug development domain and the outside world, where data leaves the controls that protected it during the trial. Realisation of this threat harms participants directly, breaches the consent under which the data was given, and would materially damage the company's ability to recruit for future trials.

### Implications
- Anonymisation for external sharing must be assessed against re-identification risk, not judged by field removal alone
- Genomic and rare-condition data require controlled-access sharing rather than open publication
- Consent language must accurately describe the sharing that will actually occur
- Re-identification risk must be reassessed when a dataset is combined with another

### Importance
Critical

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

## Create Threat

### Display Name
Irreproducible Research Results

### Qualified Name
CocoPharma::Threat::ResearchDataIrreproducibility

### Domain Identifier
20

### Summary
Research findings that cannot be reproduced from retained data and methods may cause the company to advance an ineffective candidate or abandon a viable one.

### Description
Decisions to progress a compound into expensive later-phase trials rest on earlier research results. Where the data, code, parameters, and environment behind a result were not captured well enough to rerun it, the company cannot distinguish a real effect from an artefact. The cost of this threat is asymmetric and largely invisible: a false positive is eventually caught by a failed Phase III at very high expense, while a false negative — a viable candidate discarded because a result could not be confirmed — is never detected at all. The risk rises as analysis moves into notebooks and machine learning pipelines whose outputs depend on library versions, random seeds, and preprocessing choices that are rarely recorded alongside the result. Staff departure compounds it, since undocumented method knowledge leaves with the researcher.

### Implications
- Analytical results must be traceable to the exact dataset version, code, and parameters that produced them
- Research environments and dependencies must be recorded as part of the result, not left implicit
- Method documentation must be sufficient for a competent colleague to rerun the work without the original author

### Importance
High

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

### 1.3 Regulations

The FDA clinical trial regulations (`CocoPharma::Regulation::FDAClinicalTrialRegulations`) are defined in `joint-governance-officer-definitions.md`. The regulations below cover the international and EU frameworks that apply in parallel.

___

## Create Regulation

### Display Name
ICH E6(R3) Good Clinical Practice

### Qualified Name
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Domain Identifier
20

### Summary
The international ethical and scientific quality standard for designing, conducting, recording, and reporting clinical trials involving human participants.

### Description
ICH E6 Good Clinical Practice is the standard against which regulators in the US, EU, UK, Japan, and most other jurisdictions assess trial conduct. The R3 revision restructures the guideline around quality by design and proportionate, risk-based approaches, and modernises its treatment of electronic data — recognising decentralised trials, data captured directly from participants, and computerised systems that did not exist when earlier revisions were written. For Coco Pharmaceuticals the governance-relevant requirements are: identifying the data and processes critical to participant safety and result reliability, and focusing controls there; maintaining source records that are attributable, legible, contemporaneous, original, and accurate; ensuring the sponsor retains oversight of activities delegated to vendors and sites; and keeping a trial master file that allows the conduct of the trial to be reconstructed. GCP applies alongside, not instead of, the FDA regulations and the EU Clinical Trials Regulation.

### Regulation Source
ICH Harmonised Guideline E6(R3) — Good Clinical Practice

### Regulators
- Food and Drug Administration (FDA) — United States
- European Medicines Agency (EMA)
- Medicines and Healthcare products Regulatory Agency (MHRA) — UK
- Pharmaceuticals and Medical Devices Agency (PMDA) — Japan

### Implications
- Trials must identify their critical data and processes and apply controls proportionate to risk
- Source records must meet ALCOA expectations and remain available for inspection
- Sponsor oversight of delegated activities must be documented, not assumed
- The trial master file must be contemporaneous and complete enough to reconstruct trial conduct

### Importance
Critical

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

## Create Regulation

### Display Name
EU Clinical Trials Regulation (EU) No 536/2014

### Qualified Name
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Domain Identifier
20

### Summary
The EU regulation governing authorisation, conduct, and transparency of clinical trials, including mandatory public disclosure of trial information and results through the Clinical Trials Information System.

### Description
Regulation (EU) No 536/2014 replaced the earlier Clinical Trials Directive and applies directly across all EU member states through the Clinical Trials Information System (CTIS), a single portal for trial authorisation and reporting. Its governance significance for Coco Pharmaceuticals is chiefly transparency: trial protocols, summaries of results, and — for many trials — full clinical study reports become publicly available on defined timelines, whether or not the trial produced a favourable outcome. Content published through CTIS must be prepared so that commercially confidential information and participant personal data are protected before disclosure, which makes anonymisation a submission-path activity rather than a post-hoc one. The Regulation also imposes safety reporting timelines that run in parallel with FDA requirements, and requires that trial records be retained and remain accessible for at least 25 years.

### Regulation Source
Regulation (EU) No 536/2014 on clinical trials on medicinal products for human use

### Regulators
- European Medicines Agency (EMA)
- National competent authorities in EU member states
- European Commission

### Implications
- Trial results must be posted to CTIS within the deadlines set by the Regulation, including for terminated trials
- Documents published through CTIS must be anonymised and reviewed for commercially confidential information before release
- Safety reporting timelines must be met in parallel with FDA obligations
- Trial records must be retained and remain readable for at least 25 years

### Importance
Critical

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

## Part 2: Governance Policies — Drug Development Domain

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Clinical Data Must Be Attributable to a Source

### Qualified Name
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Domain Identifier
20

### Summary
Every clinical data point must be traceable to the person, system, or device that produced it, and to the original record it came from.

### Description
Attribution is the foundation on which every other clinical data control rests. A value in an analysis dataset must be traceable back through the case report form to a source record — a clinic note, an instrument output, a participant diary entry — and that source record must identify who recorded it and when. Where data is captured directly from a device or entered by the participant, the source is the electronic record itself and no prior paper record exists; this must be declared in advance rather than discovered at inspection. Attribution also governs change: an amended value must retain the original, the new value, the identity of the person who changed it, and the reason. Shared logins, unattributed corrections, and transcription without a retained source all break this principle, and each is a common inspection finding.

### Implications
- Every clinical system must authenticate individual users; shared accounts are not permitted
- The source of each data element must be declared in a data source agreement before the trial opens
- Audit trails must capture the original value, new value, author, timestamp, and reason for change
- Transcription from paper must retain the paper record for the full retention period

### Outcomes
- Any submitted value can be traced to its origin during inspection
- Data changes are visible and explicable rather than silent
- Investigator sites and vendors are held to a single, stated standard of attribution

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

## Create Governance Principle

### Display Name
Trial Participants Are Protected by Design

### Qualified Name
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Domain Identifier
20

### Summary
Protection of trial participants is designed into how clinical data is collected, stored, and shared, rather than applied as a control at the point of disclosure.

### Description
Participants give data under a specific consent, for a specific purpose, on the understanding that their identity will not be exposed. Honouring that requires decisions taken at trial design: what identifiers are collected at all, how the pseudonymisation key is held and by whom, which staff can see identified data, and what form the data will take when it is eventually shared or published. Retrofitting protection at the point of disclosure is where re-identification risk concentrates, because by then the dataset has been shaped for analysis rather than for release. This principle is the drug development expression of the organisation-wide Privacy by Design principle, and defers to it on personal data handling generally; what it adds is the trial-specific reality that the cohort is small, the data is often genomic, and the sharing obligations are externally imposed by regulators and journals.

### Implications
- Identifier collection must be justified at protocol design and limited to what the trial requires
- Pseudonymisation keys must be held separately from the trial data with controlled, logged access
- The intended sharing and publication path must be described in the consent given to participants
- Re-identification risk assessment is a design activity, performed before data is prepared for release

### Outcomes
- Participants receive the protection they were promised at consent
- External sharing obligations can be met without ad hoc anonymisation decisions
- Genomic and rare-condition data is handled under controls matched to its sensitivity

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

## Create Governance Principle

### Display Name
Research Results Must Be Reproducible

### Qualified Name
CocoPharma::GovernancePrinciple::ResearchDataReproducibility

### Domain Identifier
20

### Summary
Any analytical result used to make a development decision must be reproducible from retained data, code, and parameters by someone other than its author.

### Description
A result that cannot be reproduced cannot be relied upon, and the company routinely commits substantial expenditure on the strength of research results. Reproducibility requires that the inputs to a result be versioned and retained, that the code and parameters producing it be captured alongside it, and that the computational environment be recorded well enough to be reconstituted. The test applied is deliberately independent of the author: a competent colleague, without access to the original researcher, must be able to rerun the analysis and obtain the same answer. This principle covers exploratory research as well as formal statistical analysis, because progression decisions are frequently made on exploratory work, and it applies equally to machine learning pipelines, whose outputs depend on seeds, library versions, and preprocessing choices that are easily left unrecorded.

### Implications
- Analysis inputs must be versioned datasets, not mutable extracts
- Code, parameters, and random seeds must be retained with the result
- Computational environments must be recorded in a form that can be reconstituted
- Results supporting progression decisions must be independently rerun before the decision is taken

### Outcomes
- Development decisions rest on results that have been confirmed rather than assumed
- Analyses survive the departure of the researcher who produced them
- Regulatory questions about derived results can be answered by rerunning the derivation

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

## Create Governance Principle

### Display Name
Blinding and Randomisation Integrity Must Be Preserved

### Qualified Name
CocoPharma::GovernancePrinciple::BlindingIntegrityPreserved

### Domain Identifier
20

### Summary
Access to treatment allocation is restricted to those who require it, and every unblinding event is controlled, justified, and recorded.

### Description
Blinding is a data access control that happens to be a scientific requirement. Once treatment allocation becomes visible to investigators, participants, or those assessing outcomes, the trial's ability to demonstrate an effect is compromised and no subsequent analysis can restore it. The governance obligation is therefore to treat the randomisation schedule as one of the most tightly held datasets in the organisation: segregated storage, access limited to named unblinded roles such as the trial statistician and drug supply, and no route by which allocation can be inferred from adjacent data — supply records, dosing quantities, or laboratory values that vary by arm. Emergency unblinding for participant safety must always be possible, must be performed through a controlled mechanism, and must be recorded with the reason, the individual unblinded, and the time. Unrecorded or casual unblinding is a reportable protocol deviation.

### Implications
- Randomisation schedules must be stored separately with access limited to named unblinded roles
- Systems must prevent allocation being inferred from supply, dosing, or laboratory data
- Emergency unblinding must be available at all times through a controlled, logged mechanism
- Every unblinding event must be recorded with reason, individual, and timestamp, and assessed as a deviation

### Outcomes
- Trial conclusions are not undermined by avoidable loss of blinding
- Participant safety is never delayed by blinding controls
- The integrity of the blind can be evidenced to regulators at inspection

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

### 2.2 Governance Obligations

___

## Create Governance Obligation

### Display Name
Trial Master File Must Be Complete and Inspection-Ready at All Times

### Qualified Name
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Domain Identifier
20

### Summary
The trial master file must be maintained contemporaneously throughout the trial, not assembled before an inspection, and must allow trial conduct to be reconstructed.

### Description
The trial master file is the evidential record of how a trial was conducted: protocol and amendments, ethics and regulatory approvals, site qualification and delegation records, monitoring reports, safety reports, and the agreements governing every delegated activity. GCP requires it to be contemporaneous — filed as events occur — because a file assembled retrospectively cannot demonstrate that oversight actually happened at the time. Inspectors routinely test this by comparing filing dates against event dates. The obligation applies equally to the sponsor file and the investigator site file, and to trials where document management is delegated to a contract research organisation, since sponsor oversight is not delegable. Completeness is assessed against an agreed index rather than judged informally, and gaps are tracked as findings with owners and due dates.

### Implications
- The trial master file index must be defined at trial start and used as the completeness standard
- Documents must be filed as events occur; retrospective filing must be visible as such
- Contract research organisation-held documents must be accessible to the sponsor throughout the trial
- Completeness must be assessed periodically during the trial, not only at close-out

### Outcomes
- Inspections proceed without findings related to missing or retrospectively assembled documentation
- Trial conduct can be reconstructed years after completion
- Oversight of delegated activities is evidenced rather than asserted

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

## Create Governance Obligation

### Display Name
Source Data Must Be Verified Against Case Report Forms

### Qualified Name
CocoPharma::GovernanceObligation::SourceDataVerification

### Domain Identifier
20

### Summary
Clinical data submitted on case report forms must be verified against the underlying source records, with verification effort targeted by risk.

### Description
Source data verification confirms that what was reported matches what was recorded at the site. Verifying every field of every form is neither affordable nor useful; ICH E6(R3) explicitly favours a risk-based approach in which critical data — primary endpoints, eligibility criteria, safety data, consent — is verified thoroughly while lower-impact fields are covered by sampling and by central statistical monitoring that detects anomalous patterns across sites. What the obligation requires is that the targeting be deliberate and documented in the monitoring plan before the trial opens, rather than emerging from monitor availability. Discrepancies must be raised as queries, resolved at the site with the correction attributed and reasoned, and analysed for pattern: a site producing systematic discrepancies needs retraining or closure, not simply more queries.

### Implications
- A risk-based monitoring plan must define verification coverage before the first participant is enrolled
- Critical data elements must be identified per protocol and verified at the agreed level
- Discrepancies must be raised, resolved, and attributed through the query management process
- Discrepancy patterns by site must be analysed and escalated, not merely corrected

### Outcomes
- Monitoring effort is concentrated where errors would affect participant safety or trial conclusions
- Systematic site data quality problems are detected while the trial can still respond
- Submitted data can be evidenced as matching site source records

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

## Create Governance Obligation

### Display Name
Protocol Deviations Must Be Recorded, Assessed, and Reported

### Qualified Name
CocoPharma::GovernanceObligation::ProtocolDeviationsRecorded

### Domain Identifier
20

### Summary
Every departure from the approved protocol must be recorded when identified, assessed for impact on participant safety and data integrity, and reported where required.

### Description
Trials deviate from protocol — visits fall outside windows, assessments are missed, ineligible participants are occasionally enrolled. What distinguishes a well-governed trial is not the absence of deviations but that each one is captured when it occurs, categorised consistently, and assessed for whether it affects participant safety or the interpretability of the data. Important deviations must be reported to ethics committees and regulators within defined timeframes and disclosed in the clinical study report, where they inform how the results are read. Deviations must also be analysed in aggregate: a cluster at one site suggests a training or comprehension problem, while the same deviation recurring across all sites usually indicates a protocol that is impractical as written and should be amended rather than repeatedly breached.

### Implications
- Deviation categories and importance criteria must be defined before the trial opens
- Deviations must be recorded when identified, with date of occurrence distinct from date of identification
- Important deviations must be reported to ethics committees and regulators within required timeframes
- Aggregate deviation patterns must be reviewed periodically and drive protocol amendment or site action

### Outcomes
- The effect of deviations on trial conclusions can be assessed and disclosed honestly
- Impractical protocol requirements are amended rather than tolerated as recurring breaches
- Sites needing intervention are identified from evidence rather than impression

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

## Create Governance Obligation

### Display Name
Adverse Events Must Be Captured and Reported Within Regulatory Timeframes

### Qualified Name
CocoPharma::GovernanceObligation::AdverseEventReporting

### Domain Identifier
20

### Summary
Adverse events must be recorded when they become known and expedited to regulators within the statutory timeframes, which run from the moment any company representative becomes aware.

### Description
Safety reporting carries the shortest and least forgiving deadlines in drug development: suspected unexpected serious adverse reactions that are fatal or life-threatening must be reported within seven calendar days, and other such reactions within fifteen. The clock starts at the point any employee, vendor, or partner first becomes aware — not when the safety database is updated — which makes the handoff between site, monitor, vendor, and pharmacovigilance the controlling factor. Reports must also reach multiple destinations with differing formats and expectations, and the same event must be reconciled between the clinical database and the safety database so that the two do not tell different stories at submission. Because the awareness date is what regulators test, the obligation is as much about the reliability of the intake path as about the reporting itself.

### Implications
- Awareness dates must be recorded at first contact anywhere in the organisation or its vendors
- Vendor and partner contracts must impose onward notification timelines that preserve the sponsor's ability to meet the deadline
- Clinical and safety databases must be reconciled on a defined cycle, with discrepancies resolved before database lock
- Reporting performance must be measured against the awareness date, not the database entry date

### Outcomes
- Regulators receive safety information within statutory timeframes
- Emerging safety signals reach the people who can act on them without avoidable delay
- Clinical and safety datasets agree at the point of submission

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

## Create Governance Obligation

### Display Name
Clinical Trial Records Must Be Retained and Remain Readable

### Qualified Name
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Domain Identifier
20

### Summary
Clinical trial records must be retained for at least 25 years and must remain readable and reconstructable for the whole of that period, including after systems are retired.

### Description
The EU Clinical Trials Regulation requires trial master file retention for at least 25 years, and other jurisdictions impose their own periods that must be satisfied in parallel — the effective obligation is the longest applicable. Twenty-five years exceeds the life of any clinical system the company will run, which makes technology succession the substance of this obligation rather than storage capacity. A retained record must remain readable in a format that will still open, and it must remain interpretable: audit trails, the metadata describing what fields meant, and the codelists in force at the time are all part of the record, and a dataset retained without them cannot be reconstructed. Records must survive decommissioning of the originating system, and migrations must be verified to show that content and audit trails transferred intact. Retention is a floor, not a ceiling: records must not be destroyed while any trial-related litigation or regulatory question remains open.

### Implications
- Retention periods must be set to the longest applicable jurisdiction, recorded per trial
- Archived data must retain its audit trails, metadata, and codelists, not only its values
- System decommissioning must include a verified migration of records into the archive
- Destruction must be suspended where litigation or regulatory questions are open

### Outcomes
- Trial records remain readable and interpretable for the full retention period
- Regulatory questions arising decades after a trial can still be answered
- System retirement does not silently destroy evidential records

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

### 2.3 Governance Approaches

___

## Create Governance Approach

### Display Name
Risk-Based Quality Management for Clinical Trials

### Qualified Name
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Domain Identifier
20

### Summary
Each trial identifies the data and processes critical to participant safety and result reliability at design time, and concentrates monitoring and control effort on those.

### Description
ICH E6(R3) is built around the proposition that quality is designed into a trial rather than inspected into it afterwards. The approach implements this as a defined activity in trial start-up: the study team identifies the critical data and processes for that specific protocol, assesses what could go wrong with each, decides which risks are worth controlling, and records the resulting decisions in a monitoring plan and a risk assessment that are living documents rather than start-up artefacts. Central statistical monitoring supports this by detecting anomalous patterns across sites — implausibly uniform data, digit preference, visit timing that clusters unnaturally — which on-site verification of individual records rarely surfaces. Quality tolerance limits are set for the parameters that matter most, and an excursion beyond a limit triggers assessment rather than an automatic response. The approach requires accepting that not every error will be prevented; effort goes where errors would change conclusions or harm participants.

### Implications
- Critical data and processes must be identified per protocol before enrolment opens
- Quality tolerance limits must be set, monitored, and excursions assessed and documented
- Central statistical monitoring must run alongside site monitoring throughout the trial
- Risk assessments must be revisited as the trial progresses, not filed at start-up

### Outcomes
- Monitoring cost is proportionate to risk rather than uniform across all data
- Systematic data problems are detected centrally before they affect trial conclusions
- Inspection findings concentrate on genuine issues rather than clerical noise

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

## Create Governance Approach

### Display Name
CDISC Standards Adoption for Clinical Data

### Qualified Name
CocoPharma::GovernanceApproach::CDISCStandardsAdoption

### Domain Identifier
20

### Summary
Clinical data is captured, tabulated, and analysed against CDISC standard structures from protocol design onward, rather than mapped into them before submission.

### Description
CDISC standards define how clinical trial data should be structured at each stage: CDASH for collection, SDTM for tabulation, ADaM for analysis, and controlled terminology binding the values these structures may take. FDA and PMDA require SDTM and ADaM for submission, so the question is never whether to conform but when. Conforming late means a mapping exercise at the end of each trial, repeated per study, performed under submission time pressure, and productive of exactly the reconciliation work that delays filing. Adopting the standards at design time means the case report form is built from CDASH elements, the tabulation structure is known before data arrives, and define-xml metadata is generated from the same definitions rather than written afterwards. The approach also delivers the reuse the personalised medicine programme depends on: trials that conform to the same structures can be pooled without re-mapping. Where a protocol genuinely requires a non-standard element, the deviation is documented in the define-xml rather than being resolved by quietly bending a standard domain.

### Implications
- Case report forms must be built from CDASH elements at design time
- Controlled terminology versions must be pinned per trial and recorded
- Define-xml metadata must be generated from the same definitions used to build the datasets
- Genuine non-standard elements must be documented as sponsor extensions, not forced into standard domains

### Outcomes
- Submission datasets are produced without a per-trial mapping exercise
- Data from separate trials can be pooled for integrated analyses without re-mapping
- Regulatory reviewers receive data in the structure they expect, reducing review queries

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

## Create Governance Approach

### Display Name
Anonymisation and Controlled Sharing of Clinical Data

### Qualified Name
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Domain Identifier
20

### Summary
Clinical data leaving the organisation passes through a defined anonymisation and access-control process, with the method chosen from an assessment of re-identification risk for that dataset and recipient.

### Description
Coco Pharmaceuticals must share trial data — with regulators, with journals, through CTIS transparency obligations, and with academic collaborators. The approach treats each release as a decision with two variables: how much the data is transformed, and how tightly the recipient is controlled. A dataset published openly requires aggressive transformation, with dates offset, small cells suppressed, rare values generalised, and free text removed or reviewed. The same dataset shared with a named collaborator under a data use agreement that forbids re-identification attempts can retain far more utility. Genomic data sits at one extreme: it cannot be anonymised by transformation, so it is shared only through controlled access with the recipient bound by agreement. Every release is preceded by a documented re-identification risk assessment that accounts for what the recipient could combine the data with, and the assessment is redone when a dataset is reused for a different release rather than inherited from the first. Anonymised outputs are retained so that what was released is known years later.

### Implications
- A re-identification risk assessment must precede every external release and be retained with it
- The transformation method must be matched to the recipient's controls, not applied uniformly
- Genomic and rare-condition data must be shared through controlled access only
- Released outputs must be retained so that past disclosures can be reconstructed

### Outcomes
- Transparency and data-sharing obligations are met without exposing participants
- Sharing decisions are consistent and evidenced rather than case-by-case judgements
- Retained release records allow the company to answer questions about past disclosures

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

## Part 3: Governance Controls — Drug Development Domain

---

### 3.1 Governance Roles

The Drug Development Lead role (`CocoPharma::GovernanceRole::DrugDevelopmentLead`, held by Tessa Tube) is defined in `joint-governance-officer-definitions.md`. The roles below are the delegated positions through which that accountability is discharged.

___

## Create Governance Role

### Display Name
Clinical Data Manager

### Qualified Name
CocoPharma::GovernanceRole::ClinicalDataManager

### Description
The Clinical Data Manager is accountable for the quality and standards conformance of clinical data for the trials assigned to them. The role owns the data management plan, the case report form design and its conformance to CDASH, the edit check specification, the query management process, and the database lock decision. It is the operational counterpart to the Drug Development Lead's domain accountability, and works with the trial statistician on analysis dataset specifications and with pharmacovigilance on clinical-safety reconciliation.

### Scope
Clinical trial data for assigned trials — case report form design, data management planning, query management, standards conformance, and database lock.

### Headcount
4

### Category
Governance Role

### Search Keywords
- clinical data management
- CDISC standards
- query management
- database lock

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
Clinical Trial Data Steward

### Qualified Name
CocoPharma::GovernanceRole::ClinicalTrialDataSteward

### Description
The Clinical Trial Data Steward maintains the metadata that makes clinical trial data findable and interpretable after the trial closes: dataset and variable definitions, controlled terminology versions in force, derivation documentation, and the catalog entries linking trial datasets to the protocol and the governance definitions that apply to them. The role also curates the anonymised outputs retained under the anonymisation and controlled sharing approach, so that the company can establish what was released, to whom, and in what form. It reports to the Drug Development Lead and works with the Information Architect on alignment to the wider data catalog.

### Scope
Clinical trial metadata, standards terminology, derivation documentation, catalog curation, and the retained record of external data releases.

### Headcount
2

### Category
Governance Role

### Search Keywords
- clinical metadata
- data stewardship
- controlled terminology
- trial data catalog

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
Critical Data Source Verification Pass Rate

### Qualified Name
CocoPharma::GovernanceMetric::CriticalDataVerificationPassRate

### Domain Identifier
20

### Summary
Measures the percentage of verified critical data elements that match their source records on first verification, without a query being required.

### Description
This metric reports how often critical data — primary endpoints, eligibility criteria, safety data, and consent — matches its source record the first time a monitor or central check compares them. It is deliberately restricted to critical elements, since those are the fields the risk-based monitoring plan commits to verifying thoroughly, and a rate computed across all fields would be dominated by low-impact data and would move for uninteresting reasons. The metric is reported per site and per trial, with the site-level view being the actionable one: a single site falling below target usually indicates a training or process problem that can be corrected, whereas a trial-wide decline more often points to an ambiguous case report form or protocol. The target is 98% or above for critical elements. First-pass rate is used rather than post-query accuracy because every query costs site and monitor time and delays lock, so the objective is data that is right when recorded rather than data that becomes right eventually.

### Implications
- Requires the critical data elements to be identified per protocol before enrolment
- Requires verification outcomes to be captured as pass or query at the element level
- Site-level reporting must be available while the trial is running, not only at close-out

### Outcomes
- Sites needing intervention are identified while the trial can still respond
- Ambiguous case report form design is detected from trial-wide patterns
- Query volume and its effect on lock timelines fall over successive trials

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

## Create Governance Metric

### Display Name
Trial Master File Completeness Rate

### Qualified Name
CocoPharma::GovernanceMetric::TrialMasterFileCompletenessRate

### Domain Identifier
20

### Summary
Measures the percentage of expected trial master file documents that are present and filed within the expected interval of the event they record.

### Description
This metric assesses the trial master file against its agreed index at defined points during the trial rather than at close-out, on the basis that a gap found while the trial is running can usually be filled and a gap found afterwards frequently cannot. It has two components, and both matter: presence, meaning the expected document exists; and timeliness, meaning it was filed within the defined interval of the event it records. Timeliness is the component inspectors probe, because a file that is complete but entirely filed in the month before an inspection demonstrates preparation rather than contemporaneous oversight. The metric is reported per trial and separately for documents held by contract research organisations, where sponsor visibility is typically weakest. Target is 95% presence with 90% filed within the defined interval, assessed quarterly and at each major trial milestone.

### Implications
- Requires an agreed trial master file index defined at trial start-up
- Requires filing dates and event dates to be recorded separately and compared
- Contract research organisation-held sections must be assessed on the same basis as sponsor-held sections

### Outcomes
- Documentation gaps are found while they can still be remediated
- Contemporaneous filing can be evidenced to inspectors rather than asserted
- Contract research organisation oversight weaknesses become visible during the trial

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

## Create Governance Metric

### Display Name
Expedited Safety Report Timeliness

### Qualified Name
CocoPharma::GovernanceMetric::ExpeditedSafetyReportTimeliness

### Domain Identifier
20

### Summary
Measures the percentage of expedited safety reports submitted to regulators within the statutory timeframe, calculated from the date of first company awareness.

### Description
This metric tracks compliance with the seven-day and fifteen-day expedited reporting deadlines, measured from the awareness date — the point at which any company employee, vendor, or partner first learned of the event — rather than from safety database entry. Measuring from the database date would report near-perfect performance while concealing exactly the failure mode that matters, which is delay in the intake path between site, monitor, vendor, and pharmacovigilance. The metric is reported by deadline category and by intake route, since a low rate concentrated in one vendor's route indicates a contractual or process problem at that vendor rather than a pharmacovigilance capacity issue. Target is 100%: unlike most metrics in this program a shortfall is a regulatory breach rather than a performance gap, so every miss is investigated individually and the aggregate rate serves to reveal trends in the intake path.

### Implications
- Awareness dates must be captured at first contact anywhere in the organisation or its vendors
- Reporting must be measured by intake route to locate delay, not only in aggregate
- Every individual miss requires investigation regardless of the aggregate rate

### Outcomes
- Delays in the safety intake path are located and corrected at their source
- Vendor notification performance is visible and contractually enforceable
- Regulatory reporting compliance can be evidenced at inspection

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

## Create Governance Metric

### Display Name
Database Lock to Submission-Ready Dataset Interval

### Qualified Name
CocoPharma::GovernanceMetric::LockToSubmissionReadyInterval

### Domain Identifier
20

### Summary
Measures the elapsed days between clinical database lock and the availability of validated, conformant analysis datasets ready for submission.

### Description
This metric measures the interval that the accelerated submission imperative exists to compress, and it is the clearest available indicator of whether standards adoption is delivering. Where CDISC structures are adopted at design time, the interval reflects validation and quality control only; where conformance is retrofitted, it absorbs a mapping exercise as well, and the difference between trials that did and did not adopt standards early is directly visible. The measurement runs from lock to the point at which datasets pass conformance validation with no unresolved findings and define-xml is complete — not to first draft, since drafts that fail validation have not shortened anything. Reported per trial with the trial's standards adoption approach recorded alongside, so the comparison is available. Target is 15 working days for trials that adopted standards at design time.

### Implications
- Requires database lock and dataset readiness to be recorded as dated events per trial
- Readiness must be defined as passing conformance validation, not as first draft delivery
- Standards adoption approach must be recorded per trial for the comparison to be meaningful

### Outcomes
- The benefit of early standards adoption is measurable rather than asserted
- Submission timeline planning rests on observed intervals rather than estimates
- Trials that retrofit conformance are identifiable and their cost quantified

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

### 3.3 Certification Type

___

## Create Certification Type

### Display Name
GCP Investigator Site Qualification

### Qualified Name
CocoPharma::CertificationType::GCPSiteQualification

### Domain Identifier
20

### Summary
The qualification a clinical investigator site must hold before it may enrol participants into a Coco Pharmaceuticals trial, confirming its capability to conduct the trial to Good Clinical Practice standards.

### Description
Before a site is activated, Coco Pharmaceuticals assesses whether it can actually run the trial as designed: whether the principal investigator has the relevant experience and sufficient time, whether the site has access to the participant population the protocol requires, whether facilities and equipment are adequate and calibrated, whether staff are trained in GCP and in the protocol, and whether records and investigational product can be handled and stored correctly. The qualification records that assessment and is the basis on which the site is authorised to enrol. It is not permanent: it is reassessed when the principal investigator changes, when the protocol is substantially amended, and periodically for sites running long trials. Qualification may be withdrawn where monitoring reveals data quality or conduct problems that the site cannot correct, in which case enrolment stops. The qualification record forms part of the trial master file.

### Scope
Clinical investigator sites, including academic centres, hospital departments, and private research sites, participating in Coco Pharmaceuticals sponsored trials in any jurisdiction.

### Implications
- Sites must not enrol participants before qualification is granted and recorded
- Qualification must be reassessed on principal investigator change and substantial protocol amendment
- Delegation of trial duties at the site must be recorded and kept current as staff change
- Withdrawal of qualification must halt enrolment and trigger assessment of data already collected

### Importance
Critical

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

### 3.4 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to Drug Development Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Policy
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Rationale
21 CFR Part 11 requires electronic records to identify the individual responsible for each entry and to retain audit trails of changes. Attribution to source is the principle that gives effect to that requirement across all clinical systems.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Policy
CocoPharma::GovernanceObligation::SourceDataVerification

### Rationale
FDA inspections test whether submitted data matches site source records. Verifying critical data against source during the trial is how the sponsor discharges that expectation before inspection rather than at it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Policy
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Rationale
E6(R3) is structured around quality by design and proportionate, risk-based control. This approach is the direct operationalisation of that structure in Coco Pharmaceuticals trials.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Policy
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Rationale
GCP requires a trial master file that allows trial conduct to be reconstructed, filed contemporaneously. The obligation states that requirement as an enforceable internal standard with a defined completeness index.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Policy
CocoPharma::GovernanceObligation::ProtocolDeviationsRecorded

### Rationale
GCP requires deviations from the approved protocol to be documented and important deviations reported. The obligation defines how they are categorised, assessed, and escalated.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Policy
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Rationale
Regulation (EU) No 536/2014 requires trial master file retention for at least 25 years. The obligation extends that from a storage duration into a requirement that records remain readable and interpretable for the whole period.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Policy
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Rationale
CTIS transparency obligations require trial documents and results to be published on defined timelines. The anonymisation approach is how those disclosures are made without exposing participants or commercially confidential information.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Policy
CocoPharma::GovernanceObligation::AdverseEventReporting

### Rationale
The Regulation sets expedited safety reporting timelines that run in parallel with FDA requirements. The obligation defines a single intake and reporting path that satisfies both.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ClinicalTrialParticipantReidentification

### Policy
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Rationale
Re-identification risk concentrates where protection is retrofitted at the point of disclosure. Designing protection into collection and storage is the primary mitigation for this threat.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ClinicalTrialParticipantReidentification

### Policy
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Rationale
Where trial data must leave the organisation, the anonymisation and controlled sharing approach is the operational control that keeps re-identification risk within tolerance for each release.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ResearchDataIrreproducibility

### Policy
CocoPharma::GovernancePrinciple::ResearchDataReproducibility

### Rationale
The threat is the direct consequence of results whose inputs, code, and environment were not retained. The reproducibility principle states the standard that prevents it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ClinicalTrialDataIntegrityFailure

### Policy
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Rationale
Falsified or unattributable clinical data is the realisation of this threat. Requiring every data point to trace to an identified source and author is the control that makes falsification detectable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ClinicalTrialDataIntegrityFailure

### Policy
CocoPharma::GovernanceObligation::SourceDataVerification

### Rationale
Verification against source records, combined with central statistical monitoring, is how integrity failures are detected while the trial is running rather than at submission.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Policy
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Rationale
The imperative requires that any submitted figure can be traced back to its origin. Attribution to source is the principle that makes that traceability a property of the data rather than an investigation.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Policy
CocoPharma::GovernancePrinciple::BlindingIntegrityPreserved

### Rationale
Reliable trial conclusions depend on the blind holding. Controlling access to treatment allocation protects the interpretability of the results the imperative is concerned with.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Policy
CocoPharma::GovernanceApproach::CDISCStandardsAdoption

### Rationale
The interval between lock and submission is dominated by reshaping data into submission structures. Adopting those structures at design time removes the exercise rather than accelerating it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Policy
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Rationale
Continuous risk-based monitoring resolves data issues throughout the trial, so that database lock is not preceded by a backlog of queries that delays submission.

___

---

### 4.2 Governance Mechanisms — Drug Development Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::SourceDataVerification

### Mechanism
CocoPharma::GovernanceMetric::CriticalDataVerificationPassRate

### Rationale
The pass rate measures directly whether critical data matches source on first verification, which is the outcome this obligation exists to produce.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Mechanism
CocoPharma::GovernanceMetric::CriticalDataVerificationPassRate

### Rationale
Reported per site and per trial, the pass rate is the feedback signal that tells the risk-based approach whether its targeting decisions were correct.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Mechanism
CocoPharma::GovernanceMetric::TrialMasterFileCompletenessRate

### Rationale
The completeness rate measures both presence and filing timeliness, which are the two components of the obligation. A file that scores well on presence but poorly on timeliness has not met it.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::AdverseEventReporting

### Mechanism
CocoPharma::GovernanceMetric::ExpeditedSafetyReportTimeliness

### Rationale
Measured from the awareness date rather than database entry, this metric tests the obligation as written and locates delay in the intake path.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::CDISCStandardsAdoption

### Mechanism
CocoPharma::GovernanceMetric::LockToSubmissionReadyInterval

### Rationale
The interval quantifies the benefit of adopting standards at design time versus retrofitting conformance, making the case for the approach measurable per trial.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Mechanism
CocoPharma::CertificationType::GCPSiteQualification

### Rationale
Attribution depends on site practice — individual accounts, contemporaneous recording, retained source documents. Site qualification is the control that confirms a site can meet those requirements before it enrols anyone.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ProtocolDeviationsRecorded

### Mechanism
CocoPharma::CertificationType::GCPSiteQualification

### Rationale
Persistent deviation patterns at a site are grounds for reassessing or withdrawing its qualification, which is the enforcement route when recording and escalation alone do not correct conduct.

___

---

### 4.3 Peer Driver Links — Related Drug Development Drivers

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Governance Driver 2
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Description
The FDA regulations impose as a legal requirement what the imperative expresses as a business need. Both demand that submitted data be traceable to its source; one is enforced by inspection, the other by the commercial consequences of a submission that cannot be defended.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Governance Driver 2
CocoPharma::Threat::ClinicalTrialDataIntegrityFailure

### Description
The threat is the failure mode the imperative exists to prevent. Treating them as peers keeps the positive goal and the negative scenario visible together, so that controls can be justified from either direction.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Governance Driver 2
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Description
GCP and the FDA regulations are assessed together at inspection and overlap substantially on source records, sponsor oversight, and electronic records. Controls should be designed once against the stricter of the two rather than separately against each.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Governance Driver 2
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Description
The EU Regulation requires trials to be conducted in accordance with GCP and adds transparency and retention obligations on top. GCP defines how the trial is run; the Regulation defines what must be disclosed and for how long records must survive.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Governance Driver 2
CocoPharma::BusinessImperative::CycleTimeReduction

### Description
Accelerating regulatory submission is the drug development expression of the organisation-wide cycle time imperative. The corporate goal identifies the need; this imperative locates it in the specific interval between database lock and filing.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::ClinicalTrialParticipantReidentification

### Governance Driver 2
CocoPharma::Threat::UnauthorisedDataDisclosure

### Description
Re-identification is a specialised form of unauthorised disclosure in which no access control is breached — the data was released deliberately, but transformed insufficiently. The distinction matters because access controls do not mitigate it.

___

---

### 4.4 Peer Policy Links — Related Drug Development Policies

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Governance Policy 2
CocoPharma::GovernanceObligation::SourceDataVerification

### Description
The principle states that data must be traceable to a source; the obligation is the activity that confirms the trace actually holds. Without verification the principle is an assertion about systems rather than a statement about data.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Governance Policy 2
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Description
The drug development principle is a specialisation of the organisation-wide privacy principle for the clinical trial context, where cohorts are small, genomic data is common, and external sharing is imposed by regulators and journals rather than chosen.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Governance Policy 2
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Description
The principle sets the standard participants are entitled to; the approach is the process applied at each release to meet it. The principle without the approach leaves each disclosure to individual judgement.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Governance Policy 2
CocoPharma::GovernanceApproach::CDISCStandardsAdoption

### Description
Records retained for 25 years must remain interpretable, not merely readable. Standard structures and versioned controlled terminology are what allow a dataset archived decades earlier to still be understood.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Governance Policy 2
CocoPharma::GovernanceObligation::ProtocolDeviationsRecorded

### Description
Deviation data is a primary input to risk-based quality management: aggregate patterns identify which processes are actually failing, which in turn redirects monitoring effort. The obligation supplies the evidence the approach depends on.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Governance Policy 2
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Description
Attribution in clinical systems rests on the organisation-wide authentication obligation. The shared logins that obligation prohibits are the single most common cause of unattributable clinical data at inspection.

___

---

### 4.5 Cross-Border and Controllership Links — Trial Data

Clinical trials make the group's subsidiary structure concrete in a way most processing does not. Investigator sites sit in the UK and across the EU; the sponsor entity for a given trial may be the US parent or a subsidiary, and that choice determines who the controller is; monitors employed by one entity access source data held at sites regulated under another; and the data then flows to a US-held clinical database. Each of these is a controllership question and, usually, a restricted international transfer.

The privacy obligations that govern this are owned by the privacy domain and defined in `privacy-governance-program.md`. The links below record how the drug development policies depend on them. The determination itself is made per trial at protocol design, not per data flow after the fact.

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Governance Policy 2
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Description
The sponsor entity named in the protocol determines which group company is controller for that trial's data, and therefore which regime, which supervisory authority, and which participant-facing information apply. Designing protection into the trial requires that determination to be made at protocol design rather than inferred later from where the database happens to sit.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
Trial data captured at UK and EU sites and consolidated into a US-held clinical database is a restricted transfer at the point of capture, not at the point of analysis. The safeguard has to be in place before the first participant is enrolled, and the instrument differs for UK-origin and EEA-origin sites within the same trial.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SourceDataVerification

### Governance Policy 2
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Description
A monitor employed by one group entity accessing identifiable source records at a site regulated under another is both a disclosure between controllers and, where the entities sit in different jurisdictions, a transfer. Remote source data verification makes this routine rather than occasional, so the basis must be established for the monitoring model the trial actually uses.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
Anonymisation sufficient that the data is no longer personal data removes a transfer from the scope of Chapter V entirely, which is the cleanest route for publication and academic sharing. Pseudonymised trial data does not qualify, and genomic data cannot be anonymised to that standard — so the anonymisation assessment determines whether a transfer mechanism is required at all, and must be made deliberately rather than assumed.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
A transfer mechanism supports a flow for as long as it remains valid; the retention obligation runs for at least 25 years. Mechanisms will be superseded or invalidated several times within that period, so archived trial data held across borders must be re-papered as instruments change rather than resting on the mechanism in force when the trial closed.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::AdverseEventReporting

### Governance Policy 2
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Description
Safety data moves between the entity running the trial, the group pharmacovigilance function, and regulators in several jurisdictions, all within statutory deadlines. The controllership determination establishes the basis for those movements in advance, since a 7-day expedited report cannot wait on a controllership question being resolved.

___

---

## Part 5: External Reference Links — Drug Development Domain

___

## Link External Reference

### Element Name
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### External Reference
CocoPharma::ExternalReference::FDA::ClinicalTrials

### Description
The FDA clinical trials resource page carries the agency's adoption of ICH E6 as guidance and the associated inspection expectations, and is the primary source for how GCP is assessed in FDA-regulated trials.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### External Reference
CocoPharma::ExternalReference::FDA::21CFRPart11

### Description
21 CFR Part 11 sets the electronic records and signatures requirements — individual authentication, audit trails, and record retention — that this principle applies to clinical systems.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::EUClinicalTrialsRegulation

### External Reference
CocoPharma::ExternalReference::EMA::HomePage

### Description
The EMA operates the Clinical Trials Information System through which authorisation, reporting, and transparency obligations under Regulation (EU) No 536/2014 are discharged.

___

---

## Part 6: Drug Development Governance Folio Membership

The Drug Development Lead Governance Folio (`CocoPharma::Folio::DrugDevelopmentLead`) is already created in `joint-governance-officer-definitions.md`, already assigned to Tessa Tube through a Link Assignment Scope command, and already registered in the `RootCollection::Coco::Governance Folios` root collection. This file therefore adds members to the existing folio rather than recreating it.

The FDA Clinical Trial Regulations driver is already a folio member and is not re-added here.

---

### 6.1 Driver Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::BusinessImperative::ClinicalTrialDataReliability

### Membership Rationale
Tessa Tube is accountable for ensuring clinical trial data can be traced from submission back to source, which is the substance of this imperative.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Membership Rationale
Compressing the interval between database lock and filing is a drug development domain objective owned by the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Threat::ClinicalTrialParticipantReidentification

### Membership Rationale
Protection of trial participants in shared and published data is a drug development responsibility, exercised in coordination with the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Threat::ResearchDataIrreproducibility

### Membership Rationale
Reproducibility of research results underpins the development decisions the Drug Development Lead is accountable for supporting with reliable data.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Threat::ClinicalTrialDataIntegrityFailure

### Membership Rationale
Defined in the risk register and carrying domain identifier 20, this threat is a drug development driver and belongs in the folio alongside the policies that respond to it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Membership Rationale
GCP is the international standard against which Coco Pharmaceuticals trial conduct is assessed, and is owned in this domain by the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Membership Rationale
The EU Clinical Trials Regulation governs authorisation, transparency, and retention for the company's EU trials, and its obligations fall to the Drug Development Lead.

### Membership Status
VALIDATED

___

---

### 6.2 Policy Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Membership Rationale
Attribution to source is the foundational clinical data principle in this domain and is authored and maintained by the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Membership Rationale
The trial-specific specialisation of privacy by design is owned in this domain, with the Chief Privacy Officer retaining ownership of the organisation-wide principle it derives from.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernancePrinciple::ResearchDataReproducibility

### Membership Rationale
Reproducibility of analytical results is a drug development governance standard maintained by the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernancePrinciple::BlindingIntegrityPreserved

### Membership Rationale
Blinding and randomisation integrity is specific to clinical trial conduct and has no equivalent in other governance domains.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Membership Rationale
Trial master file completeness is inspected directly by regulators and is the Drug Development Lead's responsibility to maintain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceObligation::SourceDataVerification

### Membership Rationale
Verification of critical data against source records is the core clinical data quality obligation in this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceObligation::ProtocolDeviationsRecorded

### Membership Rationale
Protocol deviation recording and escalation is a GCP requirement discharged within the drug development domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceObligation::AdverseEventReporting

### Membership Rationale
Expedited safety reporting timelines are a drug development obligation, discharged jointly with pharmacovigilance but owned in this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Membership Rationale
The 25-year retention obligation for clinical trial records is specific to this domain and outlives the systems that hold the records.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceApproach::RiskBasedClinicalQualityManagement

### Membership Rationale
Risk-based quality management is the method by which GCP is operationalised in Coco Pharmaceuticals trials, owned by the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceApproach::CDISCStandardsAdoption

### Membership Rationale
Clinical data standards adoption is maintained in this domain in coordination with the Information Architect on alignment to the wider data catalog.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceApproach::ClinicalDataAnonymisation

### Membership Rationale
Anonymisation and controlled sharing of clinical data is exercised in this domain, with method assurance provided by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

### 6.3 Control Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceMetric::CriticalDataVerificationPassRate

### Membership Rationale
This metric measures the source data verification obligation and is reported to the Drug Development Lead per site and per trial.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceMetric::TrialMasterFileCompletenessRate

### Membership Rationale
Trial master file completeness is assessed quarterly and at trial milestones, and reported to the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceMetric::ExpeditedSafetyReportTimeliness

### Membership Rationale
Safety reporting timeliness is a regulatory compliance measure owned in this domain and reviewed jointly with pharmacovigilance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::GovernanceMetric::LockToSubmissionReadyInterval

### Membership Rationale
This metric measures progress against the accelerated regulatory submission imperative and quantifies the benefit of standards adoption.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::CertificationType::GCPSiteQualification

### Membership Rationale
Site qualification is granted, reassessed, and withdrawn under the Drug Development Lead's authority, and is the control gating site activation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Risk::ClinicalTrialDataIntegrityLoss

### Membership Rationale
Defined in the risk register and carrying domain identifier 20, this risk is owned by the Drug Development Lead and belongs in the folio with the controls that mitigate it.

### Membership Status
VALIDATED

___

---

## Part 7: Corporate Regulation Library Membership

The regulations defined in this file are placed in the Corporate Regulation Library so that they are discoverable alongside every other regulation the company is subject to, independently of the governance domain that owns them. The library folders are defined outside this workbook.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Clinical Trial Regulations

### Element Id
CocoPharma::Regulation::ICHE6GoodClinicalPractice

### Membership Rationale
GCP is the international standard governing clinical trial conduct and belongs in the clinical trial regulations folder alongside the FDA regulations already placed there.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Clinical Trial Regulations

### Element Id
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Membership Rationale
Regulation (EU) No 536/2014 governs clinical trial authorisation, conduct, and transparency across the EU subsidiaries.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `joint-governance-officer-definitions.md` | Foundation definitions — FDA Clinical Trial Regulations (`CocoPharma::Regulation::FDAClinicalTrialRegulations`), the Drug Development Lead role, the Drug Development Lead folio and its assignment scope, the Privacy by Design principle, and the authentication obligation referenced in Part 4 |
| `risk-register.md` | Clinical Trial Data Integrity Failure threat and Loss of Clinical Trial Data Integrity risk, both carrying domain identifier 20 and added to the folio in Part 6 |
| `privacy-governance-program.md` | PRIVACY-domain definitions — the data minimisation, purpose limitation, and lawful basis principles that the trial participant protection principle specialises for clinical trials |
| `manufacturing-governance-program.md` | MANUFACTURING-domain definitions — ALCOA+ data integrity and electronic records controls, which share their regulatory basis with the clinical data integrity requirements here |
| `data-governance-program.md` | DATA-domain definitions — common data definitions and data quality obligations that clinical standards adoption aligns to |
