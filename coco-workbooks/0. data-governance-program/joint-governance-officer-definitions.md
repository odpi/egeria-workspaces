# Coco Pharmaceuticals — Joint Governance Officer Definitions

> **Author:** Jules Keeper (Chief Data Officer)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-07-01  
> **Description:** Governance definitions shared across all governance domains at Coco Pharmaceuticals. This file must be loaded first. It defines governance drivers (business imperatives, threats, regulations), cross-domain and domain-specific policies for non-DATA domains, all governance roles, external references, and governance folios. The DATA-domain policies, controls, and links are in `data-governance-program.md`.

---

## Overview

This document contains the governance definitions that are shared across multiple governance domains, or that belong to a specific non-DATA domain. It covers:

- **Part 1: Governance Drivers** — business imperatives, threats, and regulations that motivate the governance program.
- **Part 2: Governance Policies** — principles, obligations, and approaches for ALL, SECURITY, PRIVACY, and CORPORATE domains.
- **Part 3: Governance Controls** — all governance roles (with person role appointments) and the PRIVACY-domain metric.
- **Part 4: Governance Links** — links between drivers and non-DATA policies, and peer links.
- **Part 5: External References** — web resources linked to governance definitions.
- **Part 6: Governance Folios** — role-owned collections of governance definitions.

---

## Part 1: Governance Drivers

Governance drivers are the reasons why Coco Pharmaceuticals needs a governance program. They are divided into three types: *business imperatives*, *threats*, and *regulations*.

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Personalized Medicine Transition

### Qualified Name
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Domain Identifier
All Domains

### Summary
Coco Pharmaceuticals is shifting from batch manufacturing of generic drugs to personalised, genomic-targeted treatments delivered on-demand.

### Description
The organisation's core strategic direction is to provide personalised medicine to its customers. This requires a fundamental change in how data is collected, shared, and acted upon across research, manufacturing, clinical operations, and finance. Real-time data exchange between departments becomes essential; patient characteristics must drive treatment decisions; and manufacturing must operate a hybrid model supporting both existing batch processes and agile on-demand production for new drugs.

### Implications
- Data must be available in real-time across all departments
- Information about patients must be handled with appropriate privacy controls
- Manufacturing systems must integrate with active treatment plans
- Finance needs cash flow visibility across patients, suppliers, and predictions

### Outcomes
- Physicians have interactive decision support based on individual patient characteristics
- Hospital partners can order drugs on-demand rather than in batches
- Research cycles are accelerated through data-driven insights

### Importance
Critical — this is the primary strategic direction of the organisation.

### Category
Strategic Transformation

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
Cycle Time Reduction

### Qualified Name
CocoPharma::BusinessImperative::CycleTimeReduction

### Domain Identifier
All Domains

### Summary
Coco Pharmaceuticals must reduce cycle times across all business operations to remain competitive.

### Description
The move to personalised medicine and on-demand manufacturing demands that the organisation operates much faster. Hospitals require agile ordering and validation processes. Research teams need to accelerate drug development timelines. Finance and operations must have real-time visibility to support dynamic planning. Reducing cycle times is only possible with well-governed, high-quality, consistently defined data flowing between all departments without friction.

### Implications
- Data must be consistently defined so that it can be shared without manual reconciliation
- Information supply chains must be optimised and monitored for failures
- Authoritative data sources must be identified so staff are not delayed by uncertainty about data quality

### Outcomes
- Faster drug development from research to manufacturing
- Reduced time from patient referral to treatment
- Faster financial reporting and planning cycles

### Importance
High

### Category
Operational Efficiency

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
Cyber Resilience

### Qualified Name
CocoPharma::BusinessImperative::CyberResilience

### Domain Identifier
Security

### Summary
Coco Pharmaceuticals must protect its intellectual property, patient data, and operational systems against cyber threats to sustain its business.

### Description
As Coco Pharmaceuticals relies increasingly on digital systems and data sharing — including sharing patient data with hospitals, research partners, and regulators — it becomes a more attractive target for cyber-attacks. Intellectual property related to novel personalised treatments is particularly valuable. Cyber resilience requires governance over who can access what data, under what conditions, and with what audit trail.

### Implications
- All systems containing sensitive data must have access controls
- Audit logs must capture who accessed or modified data and when
- Security incidents must be detected and responded to promptly

### Outcomes
- Intellectual property is protected from theft or exposure
- Patient data is not compromised
- Business operations continue without disruption from cyber incidents

### Importance
Critical

### Category
Security & Resilience

### Authors
Ivor Padlock

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
Cyber-Attack on Operations or Data

### Qualified Name
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Domain Identifier
Security

### Summary
Malicious actors may attempt to disrupt Coco Pharmaceuticals' operations or steal sensitive data through cyber-attacks.

### Description
Coco Pharmaceuticals holds high-value intellectual property related to novel drug formulas and personalised treatment protocols. It also holds sensitive patient health data. Both categories make it an attractive target for cyber-attacks — whether ransomware disrupting manufacturing, data theft from research systems, or manipulation of clinical trial data. The threat is heightened as the organisation increases its use of digital systems and data sharing with external partners.

### Implications
- Access to sensitive systems must be tightly controlled and audited
- Data shared with external partners must be governed by agreements and monitored
- Incident response procedures must exist and be tested regularly

### Importance
Critical

### Category
Cyber Security

### Authors
Ivor Padlock

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Unauthorised Data Disclosure

### Qualified Name
CocoPharma::Threat::UnauthorisedDataDisclosure

### Domain Identifier
Privacy

### Summary
Patient data or commercially sensitive information may be disclosed to unauthorised parties — accidentally or through insider misuse.

### Description
Coco Pharmaceuticals handles sensitive patient health data as part of clinical trials and personalised treatment programmes. There is a real risk that this data could be inadvertently disclosed — through misconfigured access controls, human error, or deliberate insider misuse. Such disclosure could harm patients, expose the organisation to regulatory fines, and damage its reputation with hospital partners and patients. The risk increases as more data is shared digitally across organisational boundaries.

### Implications
- Personal data must be classified and handled under defined privacy controls
- Data sharing with hospitals and research partners must be governed by formal agreements
- Staff must understand their responsibilities for protecting patient data

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

___

## Create Threat

### Display Name
Fraudulent Supplier Activity

### Qualified Name
CocoPharma::Threat::FraudulentSupplierActivity

### Domain Identifier
Corporate

### Summary
The organisation may be exposed to fraud through bogus or compromised suppliers entering the supply chain.

### Description
A previous incident at Coco Pharmaceuticals involved a fraudulent supplier entering the procurement process. Without adequate governance over supplier data and procurement workflows, the organisation is vulnerable to financial loss, reputational damage, and — in the context of pharmaceutical manufacturing — potentially serious harm from substandard or counterfeit inputs. Strong data governance over supplier identity and procurement data reduces this risk.

### Implications
- Supplier master data must have a designated authoritative source
- Changes to supplier records must require approval and audit
- Procurement data must be accurate and traceable

### Importance
High

### Category
Supply Chain Risk

### Authors
Reggie Mint

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Loss of Key Talent and Knowledge

### Qualified Name
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Domain Identifier
All Domains

### Summary
Departure of key personnel could result in loss of critical knowledge about data definitions, processes, and governance practices.

### Description
Coco Pharmaceuticals has historically relied on informal knowledge sharing — a pattern common in startup cultures. As the organisation grows and formalises, there is a risk that institutional knowledge held by individuals is not captured in documented form. If key staff leave, this knowledge may be lost, leaving the organisation unable to operate processes or make decisions that depend on undocumented understanding. The governance program must capture knowledge as documented governance definitions and data specifications.

### Implications
- Governance definitions, data definitions, and process documentation must be maintained in a shared metadata catalog
- Authoritative sources and data stewards must be formally assigned — not left to informal convention
- Onboarding new staff must rely on documented knowledge rather than tribal knowledge

### Importance
Medium

### Category
Knowledge Management

### Authors
Jules Keeper

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
General Data Protection Regulation (GDPR)

### Qualified Name
CocoPharma::Regulation::GDPR

### Domain Identifier
Privacy

### Summary
EU regulation governing the collection, processing, storage, and sharing of personal data, including patient health data.

### Description
GDPR applies to all personal data processed by Coco Pharmaceuticals, including patient data collected during clinical trials, treatment programmes, and any data sharing activities with hospitals. It requires organisations to have a lawful basis for processing personal data, to protect data subjects' rights, to implement appropriate security measures, and to notify authorities and individuals in the event of a data breach. Non-compliance can result in fines of up to 4% of global annual turnover.

### Regulation Source
European Union — Regulation (EU) 2016/679

### Regulators
- Information Commissioner's Office (ICO) — UK
- National data protection authorities in EU member states

### Implications
- Personal data must be identified, classified, and handled under defined privacy controls
- Data processing must have a documented lawful basis
- Data subjects must be able to exercise their rights (access, erasure, portability)
- Data breach notification procedures must exist

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

___

## Create Regulation

### Display Name
FDA Clinical Trial Regulations

### Qualified Name
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Domain Identifier
All Domains

### Summary
US Food and Drug Administration regulations governing the conduct, recording, and reporting of clinical trials.

### Description
Coco Pharmaceuticals conducts clinical trials as part of its drug development activities. FDA regulations — including 21 CFR Parts 11, 50, 56, and 312 — impose strict requirements on how clinical trial data is collected, managed, validated, and reported. Electronic records must be trustworthy, reliable, and equivalent to paper records. Data integrity is critical; falsification or loss of clinical trial data can result in regulatory action, withdrawal of drug approvals, and criminal liability.

### Regulation Source
US Food and Drug Administration (FDA)

### Regulators
- US Food and Drug Administration (FDA)

### Implications
- Clinical trial data must have a clear audit trail from source to report
- Systems holding clinical trial data must have validated access controls
- Data quality rules must be enforced and documented
- Data retention periods must be respected

### Importance
Critical

### Category
Drug Development & Clinical Trials

### Authors
Tessa Tube

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Regulation

### Display Name
Good Manufacturing Practice (GMP)

### Qualified Name
CocoPharma::Regulation::GoodManufacturingPractice

### Domain Identifier
All Domains

### Summary
Regulations governing pharmaceutical manufacturing to ensure products are consistently produced and controlled according to quality standards.

### Description
GMP regulations (EU GMP Directive 2003/94/EC and US 21 CFR Parts 210–211) require pharmaceutical manufacturers to document all manufacturing processes, control quality at every stage, and maintain complete records. For Coco Pharmaceuticals, this means manufacturing data — including batch records, equipment logs, and quality control results — must be governed to ensure completeness, accuracy, and traceability. As the organisation moves towards personalised on-demand manufacturing, these requirements become even more complex.

### Regulation Source
EU European Medicines Agency (EMA) and US Food and Drug Administration (FDA)

### Regulators
- European Medicines Agency (EMA)
- Medicines and Healthcare products Regulatory Agency (MHRA) — UK
- US Food and Drug Administration (FDA)

### Implications
- Manufacturing data must be complete, accurate, and tamper-evident
- Batch records must be traceable to raw material sourcing
- Quality control data must be retained for defined periods
- Deviations from process must be documented and investigated

### Importance
Critical

### Category
Pharmaceutical Manufacturing

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — Non-DATA Domains

Governance policies define how Coco Pharmaceuticals responds to the governance drivers above. The definitions below apply to ALL, SECURITY, PRIVACY, and CORPORATE governance domains.

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Information is a Company Asset

### Qualified Name
CocoPharma::GovernancePrinciple::InformationIsACompanyAsset

### Domain Identifier
All Domains

### Summary
All information created or used by Coco Pharmaceuticals is recognised as a company asset and will be managed accordingly.

### Description
Information — like physical equipment or financial capital — is a valuable asset that belongs to the organisation. It must be identified, catalogued, protected, and made available to authorised users who need it to do their work. Information that is not governed is information that is at risk of being lost, misused, or degraded in quality. Treating information as an asset means assigning ownership, defining quality standards, and maintaining a current inventory.

### Implications
- All significant data collections must be catalogued with a designated owner
- Information assets must be protected from unauthorised access, loss, or corruption
- The value of information assets must be considered in investment and risk decisions

### Outcomes
- A complete catalogue of Coco Pharmaceuticals' information assets exists and is kept current
- Every information asset has an accountable owner
- Information assets are protected proportionally to their value and sensitivity

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Privacy by Design

### Qualified Name
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Domain Identifier
Privacy

### Summary
Privacy controls will be built into systems and processes from the start, not added as an afterthought.

### Description
Coco Pharmaceuticals handles patient health data — some of the most sensitive personal data that exists. The principle of privacy by design means that when new systems or processes are designed, privacy protections are considered and built in from the beginning. This is more effective and less costly than retrofitting privacy controls after systems are deployed. It also supports compliance with GDPR, which explicitly requires privacy by design and by default.

### Implications
- All new systems handling personal data must include a privacy impact assessment during design
- Default settings must protect privacy — personal data must not be shared by default
- Data minimisation must be applied — only the personal data that is actually needed should be collected

### Outcomes
- Personal data is protected from unnecessary exposure
- GDPR compliance is built into systems rather than bolted on
- Trust with patients and hospital partners is maintained


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
Information Use Limited to Approved, Ethical Purposes

### Qualified Name
CocoPharma::GovernancePrinciple::InformationUseLimitedToApprovedEthicalPurposes

### Domain Identifier
All Domains

### Summary
Data and information held by Coco Pharmaceuticals will only be used for purposes that have been formally approved and that are consistent with ethical standards.

### Description
Data — particularly patient health data — can be misused in ways that harm individuals or undermine trust. Coco Pharmaceuticals commits to using its information only for purposes that have been reviewed, approved, and documented, and that are consistent with ethical norms and legal requirements. Requests to use data for new purposes must go through an approval process. Staff must understand and respect the boundaries of approved use.

### Implications
- Data processing purposes must be documented and approved before use
- Staff must be trained on approved uses of different data types
- Requests to use data for new purposes must be formally assessed

### Outcomes
- Patient trust is maintained
- The organisation is protected from ethical and legal exposure
- Regulatory requirements around purpose limitation are met

### Authors
Jules Keeper

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
All Users Must Be Authenticated and Accountable

### Qualified Name
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Domain Identifier
Security

### Summary
Every user who accesses Coco Pharmaceuticals' systems must be uniquely identified and authenticated, and their actions must be recorded.

### Description
Accountability for data access and modification depends on knowing who did what and when. This obligation requires that every person accessing any system holding company data must authenticate with a unique identity. Shared accounts and generic logins are prohibited for systems holding sensitive data. Access must be logged and logs must be retained for a defined period to support audit and incident investigation.

### Implications
- All systems must enforce unique user authentication
- Shared accounts must be eliminated from systems holding company or patient data
- Access logs must be retained according to defined retention schedules

### Outcomes
- All data access can be traced to an individual
- Security incidents can be investigated with complete audit trails
- Regulatory audit requirements can be satisfied

### Authors
Ivor Padlock

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Personal Data Must Be Classified and Handled According to Sensitivity

### Qualified Name
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Domain Identifier
Privacy

### Summary
Personal data must be identified, classified by sensitivity, and handled under controls appropriate to its classification.

### Description
Not all personal data carries the same risk. Patient health data is among the most sensitive; employee contact information is less so. This obligation requires that personal data held by Coco Pharmaceuticals is classified according to its sensitivity level, and that each classification has defined handling requirements — covering access controls, retention periods, sharing permissions, and disposal methods. Classification must be documented in the metadata catalog.

### Implications
- A personal data classification scheme must be defined and published
- Systems holding personal data must document what classifications of data they hold
- Staff handling personal data must understand the requirements for each classification

### Outcomes
- Personal data is protected proportionally to its sensitivity
- GDPR obligations around appropriate technical and organisational measures are satisfied
- Data subjects' rights can be exercised because data is identifiable and traceable

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
Each Information Collection Must Have a Designated Owner

### Qualified Name
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Domain Identifier
All Domains

### Summary
Every significant collection of data held by Coco Pharmaceuticals must have a formally assigned owner who is accountable for its quality and appropriate use.

### Description
Without clear ownership, data quality degrades, access controls become inconsistent, and nobody takes responsibility for problems. This obligation requires that every significant data collection — database, file store, data feed, report — has a designated owner who is accountable for its fitness for purpose. The owner is responsible for setting quality standards, approving access requests, monitoring quality, and escalating issues.

### Implications
- A register of information assets and their owners must be maintained
- Ownership must be formally assigned — not assumed by convention
- Owners must have the authority and capacity to discharge their responsibilities

### Outcomes
- Every data quality issue has a clear escalation path
- Access requests can be approved or denied promptly
- Information assets are maintained to a consistent standard

### Authors
Jules Keeper

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
Metadata-Driven Governance

### Qualified Name
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Domain Identifier
All Domains

### Summary
Governance definitions, data definitions, and governance controls will be maintained as metadata in Egeria's open metadata catalog, making them discoverable, linked, and actionable.

### Description
Traditional governance programs produce documents that become stale and disconnected from the systems they govern. Coco Pharmaceuticals will use a metadata-driven approach: governance drivers, policies, and controls are recorded as structured metadata in the Egeria open metadata ecosystem. This means they are linked to the actual data assets, systems, and processes they govern. Changes to the governance program are reflected immediately in the catalog. Automated governance actions can be triggered by metadata.

### Implications
- All governance definitions must be created and maintained in the Egeria metadata catalog using tools such as Dr.Egeria, pyegeria, Egeria Advisor, Resource Explorer and the Egeria Portal.
- Governance definitions must be linked to the data assets and processes they govern
- The metadata catalog must be the authoritative source for governance program information

### Outcomes
- Governance definitions are always current and linked to live systems
- Automated governance actions can be triggered based on metadata
- Staff can discover what governance applies to any data asset

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Federated Governance with Central Coordination

### Qualified Name
CocoPharma::GovernanceApproach::FederatedGovernanceWithCentralCoordination

### Domain Identifier
All Domains

### Summary
Each governance domain is managed by a specialist domain lead, with central coordination by the Chief Data Officer to ensure consistency and avoid gaps or conflicts.

### Description
Governance across data, security, privacy, IT infrastructure, software development, corporate compliance, and sustainability requires deep specialist expertise in each domain. Coco Pharmaceuticals will therefore federate governance responsibility to domain leads — each empowered to define and enforce governance in their domain. However, the domains are interconnected: a data governance decision affects security; a privacy decision affects data architecture. The Chief Data Officer coordinates across domains, identifies conflicts, and ensures that the overall governance program is consistent and complete.

### Implications
- Domain leads must be formally appointed with clear responsibilities
- A cross-domain governance forum must meet regularly to identify and resolve conflicts
- The CDO has authority to resolve cross-domain conflicts where domain leads cannot agree

### Outcomes
- Governance in each domain benefits from specialist expertise
- Cross-domain issues are identified and resolved promptly
- The overall governance program is coherent and complete

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls

Governance controls define how the governance policies are implemented. They include roles and metrics.

---

### 3.1 Governance Roles

The following governance roles are assigned as part of the Coco Pharmaceuticals governance program. Each role carries accountability for a specific aspect of governance.

| Role | Appointed Person | Domain | Responsibility |
|------|-----------------|--------|---------------|
| Chief Data Officer | Jules Keeper | ALL | Overall governance program leadership and cross-domain coordination |
| Chief Information Security Officer | Ivor Padlock | SECURITY | Security governance — access controls, incident response, cyber resilience |
| Chief Privacy Officer | Faith Broker | PRIVACY | Privacy governance — personal data handling, GDPR compliance |
| Chief Financial Officer (Governance) | Reggie Mint | CORPORATE | Corporate governance — financial reporting, supplier management |
| IT Infrastructure Lead | Gary Geeke | IT_INFRASTRUCTURE | Infrastructure governance — systems, platforms, and networks |
| Senior Software Manager | Polly Tasker | SOFTWARE_DEVELOPMENT | Software development governance — development standards and DevOps |
| Information Architect | Erin Overview | DATA | Data architecture, classification schemes, and subject area definitions |
| Drug Development Lead | Tessa Tube | Drug Development | Clinical trial data governance and FDA compliance |

---

___

## Create Governance Role

### Display Name
Chief Data Officer

### Qualified Name
CocoPharma::GovernanceRole::ChiefDataOfficer

### Description
The Chief Data Officer (CDO) is responsible for the overall data governance program at Coco Pharmaceuticals. The CDO defines the data strategy, establishes governance policies and standards, coordinates across all governance domains, chairs the cross-domain governance forum, and is accountable to the board for the quality, availability, and appropriate use of the organisation's information assets.

### Scope
Organisation-wide across all governance domains.

### Headcount
1

### Category
Governance Role

### Search Keywords
- CDO
- data governance
- data strategy
- governance program

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::UK::296776

### Person Role
CocoPharma::GovernanceRole::ChiefDataOfficer

___

---

___

## Create Governance Role

### Display Name
Chief Information Security Officer

### Qualified Name
CocoPharma::GovernanceRole::ChiefInformationSecurityOfficer

### Description
The Chief Information Security Officer (CISO) is responsible for Coco Pharmaceuticals' information security governance domain. The CISO defines security policies and standards, oversees access controls and authentication requirements, leads incident response, and manages cyber resilience.

### Scope
Security governance domain — all systems, data, and physical events operated by Coco Pharmaceuticals.

### Headcount
1

### Category
Governance Role

### Search Keywords
- CISO
- security governance
- cyber resilience
- information security

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::USA::499888

### Person Role
CocoPharma::GovernanceRole::ChiefInformationSecurityOfficer

___

---

___

## Create Governance Role

### Display Name
Chief Privacy Officer

### Qualified Name
CocoPharma::GovernanceRole::ChiefPrivacyOfficer

### Description
The Chief Privacy Officer (CPO) is responsible for Coco Pharmaceuticals' privacy governance domain. The CPO defines privacy policies, oversees the classification and handling of personal data, ensures compliance with GDPR and other data protection regulations, manages data breach notification, and maintains the organisation's data processing register. The CPO works closely with the CDO and CISO to ensure privacy controls are embedded in data and security governance.

### Scope
Privacy governance domain — all personal data processed by Coco Pharmaceuticals, including patient health data, employee data, and clinical trial participant data.

### Headcount
1

### Category
Governance Role

### Search Keywords
- CPO
- privacy governance
- GDPR
- data protection
- personal data

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::NL::139870

### Person Role
CocoPharma::GovernanceRole::ChiefPrivacyOfficer

___

---

___

## Create Governance Role

### Display Name
Chief Financial Officer (Corporate Governance Lead)

### Qualified Name
CocoPharma::GovernanceRole::ChiefFinancialOfficer

### Description
The Chief Financial Officer (CFO) holds the corporate governance domain lead role in addition to their primary financial responsibilities. In this governance capacity, the CFO is accountable for supplier master data integrity, procurement governance, financial reporting data quality, and other corporate compliance obligations. The CFO coordinates with the CDO to ensure financial and corporate data assets are appropriately governed.

### Scope
Corporate governance domain — financial data, supplier data, procurement processes, and corporate compliance reporting.

### Headcount
1

### Category
Governance Role

### Search Keywords
- CFO
- corporate governance
- financial governance
- supplier management

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::UK::188888

### Person Role
CocoPharma::GovernanceRole::ChiefFinancialOfficer

___

---

___

## Create Governance Role

### Display Name
IT Infrastructure Lead

### Qualified Name
CocoPharma::GovernanceRole::ITInfrastructureLead

### Description
The IT Infrastructure Lead is responsible for the IT infrastructure governance domain. This role defines standards for platforms, networks, and systems; governs the deployment and decommissioning of infrastructure assets; ensures infrastructure changes are managed with appropriate audit trails; and coordinates with the CISO on infrastructure security controls and with the CDO on metadata cataloguing of infrastructure components.

### Scope
IT infrastructure governance domain — all computing platforms, networks, storage systems, and cloud services operated by or on behalf of Coco Pharmaceuticals.

### Headcount
1

### Category
Governance Role

### Search Keywords
- IT governance
- infrastructure governance
- platform management

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::NL::199995

### Person Role
CocoPharma::GovernanceRole::ITInfrastructureLead

___

---

___

## Create Governance Role

### Display Name
Senior Software Manager (Software Development Governance Lead)

### Qualified Name
CocoPharma::GovernanceRole::SeniorSoftwareManager

### Description
The Senior Software Manager holds the software development governance domain lead role. This role defines coding standards, DevOps practices, software quality gates, and release governance for Coco Pharmaceuticals' internally developed and maintained software. The role ensures that governance requirements — including audit logging, access controls, and data handling — are embedded in software development practices from the design stage.

### Scope
Software development governance domain — all software developed, maintained, or deployed by Coco Pharmaceuticals' engineering teams.

### Headcount
1

### Category
Governance Role

### Search Keywords
- software governance
- DevOps governance
- development standards

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::NL::338575

### Person Role
CocoPharma::GovernanceRole::SeniorSoftwareManager

___

---

___

## Create Governance Role

### Display Name
Information Architect

### Qualified Name
CocoPharma::GovernanceRole::InformationArchitect

### Description
The Information Architect is responsible for defining and maintaining the organisation's data architecture within the data governance domain. This role designs subject area structures, classification schemes, and data zone definitions; works with domain leads to identify authoritative data sources; and oversees the structure of the business glossary and metadata catalog. The Information Architect reports to the CDO and works closely with the Data Designer and Data Steward roles.

### Scope
Data governance domain — data architecture, subject area definitions, classification schemes, metadata catalog structure, and authoritative source identification across the organisation.

### Headcount
1

### Category
Governance Role

### Search Keywords
- information architect
- data architecture
- subject areas
- metadata catalog

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::UK::324713

### Person Role
CocoPharma::GovernanceRole::InformationArchitect

___

---

___

## Create Governance Role

### Display Name
Drug Development Lead (Data Governance)

### Qualified Name
CocoPharma::GovernanceRole::DrugDevelopmentLead

### Description
The Drug Development Lead holds governance responsibility for the drug development and clinical trials data domain. This role defines data governance requirements specific to clinical trial conduct, ensures compliance with FDA regulations (including 21 CFR Part 11), oversees the integrity and retention of clinical trial data, and coordinates with the CDO on data quality standards for drug development data. The role works closely with clinical operations, research, and regulatory affairs teams.

### Scope
Drug development governance domain — clinical trial data, research data, drug development records, and regulatory submission data.

### Headcount
1

### Category
Governance Role

### Search Keywords
- drug development governance
- clinical trial governance
- FDA compliance
- clinical data

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::USA::302145

### Person Role
CocoPharma::GovernanceRole::DrugDevelopmentLead

___

---

### 3.2 Governance Metrics

___

## Create Governance Metric

### Display Name
Personal Data Breaches Reported

### Qualified Name
CocoPharma::GovernanceMetric::PersonalDataBreachesReported

### Domain Identifier
Privacy

### Summary
Counts the number of personal data breaches identified and reported in a period, including near-misses.

### Description
Under GDPR, Coco Pharmaceuticals must report personal data breaches to the relevant supervisory authority within 72 hours of becoming aware of them, where the breach is likely to result in risk to individuals. This metric counts breaches (and near-misses) detected in each period. The existence of this metric does not mean breaches are acceptable — the aim is zero breaches. However, a metric of zero may also indicate inadequate detection capability. Near-misses must also be reported to enable proactive risk reduction.

### Implications
- Requires breach detection and reporting mechanisms
- Requires clear definition of what constitutes a breach versus a near-miss
- Requires a process for 72-hour GDPR notification

### Outcomes
- GDPR reporting obligations are met
- Near-misses are captured and used to prevent future breaches
- The organisation's privacy risk profile is tracked over time

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Governance Links

This section captures the relationships between governance definitions where neither endpoint is a DATA-domain definition. Links involving DATA-domain definitions are in `data-governance-program.md`.

---

### 4.1 Governance Responses — Drivers linked to Policies

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Rationale
The scale and pace of the personalised medicine transformation requires governance that is embedded in live systems via metadata, not maintained separately in documents that quickly become stale.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::CyberResilience

### Policy
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Rationale
Cyber resilience requires knowing who is accessing what. Unique authentication and access logging are the foundation of the audit trail needed for incident investigation and deterrence.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Policy
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Rationale
Cyber-attacks frequently exploit weak or shared credentials. Mandatory unique authentication and access logging reduce both the attack surface and the time to detect a breach.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Rationale
Building privacy controls into systems from the start — rather than adding them later — is the most effective way to prevent inadvertent disclosure of patient and sensitive data.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Rationale
Disclosure risk varies by data sensitivity. Classifying personal data enables proportionate controls — the highest-risk data receives the strongest protection.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernancePrinciple::InformationUseLimitedToApprovedEthicalPurposes

### Rationale
Insider misuse of data — a key disclosure vector — is deterred when staff understand that data use is limited to formally approved purposes and that breaches carry consequences.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FraudulentSupplierActivity

### Policy
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Rationale
Supplier fraud is enabled when supplier master data has no clear owner and changes can be made without scrutiny. Designated ownership ensures that supplier data changes require authorisation.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Policy
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Rationale
When governance knowledge is captured as structured metadata in the catalog — rather than held informally in people's heads — it survives staff departures and is accessible to successors.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Rationale
GDPR Article 25 explicitly requires data protection by design and by default. The Privacy by Design principle directly implements this legal requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Rationale
GDPR requires appropriate technical and organisational measures proportionate to the risk. Classification by sensitivity is the mechanism for determining what measures are appropriate.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::InformationUseLimitedToApprovedEthicalPurposes

### Rationale
GDPR's purpose limitation principle (Article 5(1)(b)) requires that personal data is only processed for the specific purposes for which it was collected. This principle gives effect to that requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Policy
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Rationale
21 CFR Part 11 requires that electronic records have a reliable audit trail tied to individual users. Mandatory unique authentication is the control that delivers this.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Rationale
GMP traceability requirements depend on knowing who is accountable for each category of manufacturing data. Designated ownership provides that accountability.

___

---

### 4.2 Governance Mechanisms — Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Mechanism
CocoPharma::GovernanceMetric::PersonalDataBreachesReported

### Rationale
Proper classification and proportionate controls are the primary means of preventing breaches. This metric measures the outcome — breach occurrence — as an indicator of whether classification controls are effective.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Mechanism
CocoPharma::GovernanceMetric::PersonalDataBreachesReported

### Rationale
Privacy by Design aims to eliminate breach risk through proactive system design. Reported breaches (and near-misses) are the key outcome measure for this principle.

___

---

### 4.3 Peer Driver Links — Related Governance Drivers

These links connect governance drivers that are closely related, helping readers understand how threats, imperatives, and regulations reinforce each other.

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Governance Driver 2
CocoPharma::BusinessImperative::CycleTimeReduction

### Description
Both imperatives arise from the same strategic transformation. Personalised medicine requires faster cycles; cycle time reduction is a prerequisite for personalised medicine to be operationally viable.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::CyberResilience

### Governance Driver 2
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Description
The Cyber Resilience imperative is a direct organisational response to the Cyber-Attack threat. They represent the same risk viewed from the positive (what we must achieve) and negative (what we must prevent) perspectives.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::GDPR

### Governance Driver 2
CocoPharma::Threat::UnauthorisedDataDisclosure

### Description
GDPR and the unauthorised disclosure threat are closely linked: the regulation exists precisely because unauthorised disclosure of personal data causes harm. Compliance with GDPR is a key mitigant of the threat.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Governance Driver 2
CocoPharma::Regulation::GoodManufacturingPractice

### Description
Both regulations apply to Coco Pharmaceuticals' drug development and manufacturing activities. They share common themes of data integrity, audit trails, and traceability, and are often assessed together.

___

---

### 4.4 Peer Policy Links — Related Governance Policies

These links connect governance policies that reinforce or depend on each other.

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::InformationIsACompanyAsset

### Governance Policy 2
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Description
Ownership is the operational expression of the asset principle. Recognising information as an asset (principle) demands that someone is accountable for it (obligation).

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Description
Privacy by Design specifies the approach; data classification provides the mechanism for applying proportionate controls. Together they form the core of Coco Pharmaceuticals' privacy governance.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::FederatedGovernanceWithCentralCoordination

### Governance Policy 2
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Description
Federated governance requires a shared view of governance definitions across domains. The metadata catalog — delivered by the Metadata-Driven Governance approach — is the coordination layer that makes federation practical.

___

---

## Part 5: External References

This section defines external web resources — regulation texts, regulatory body home pages, and Egeria documentation — and links them to the governance definitions they relate to.

---

### 5.1 External Reference Definitions

___

## Create External Reference

### Display Name
GDPR — Full Regulation Text (EUR-Lex)

### Qualified Name
CocoPharma::ExternalReference::GDPR::EURLex

### Reference Title
Regulation (EU) 2016/679 of the European Parliament and of the Council

### Organization
Publications Office of the European Union

### Reference Abstract
The full text of the General Data Protection Regulation (GDPR), Regulation (EU) 2016/679, as published in the Official Journal of the European Union. This is the authoritative legal source for all GDPR obligations referenced in this governance program.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679 |

### Category
Regulation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
ICO — Information Commissioner's Office

### Qualified Name
CocoPharma::ExternalReference::ICO::HomePage

### Reference Title
ICO — The UK's independent authority set up to uphold information rights

### Organization
Information Commissioner's Office (ICO)

### Reference Abstract
The UK supervisory authority for data protection. The ICO provides guidance on GDPR compliance, handles complaints, and can investigate and fine organisations for data protection breaches. The ICO website includes practical guidance on implementing GDPR requirements.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://ico.org.uk/ |
| GDPR Guidance | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/ |

### Category
Regulatory Body

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
FDA — Clinical Trials and Human Subject Protection

### Qualified Name
CocoPharma::ExternalReference::FDA::ClinicalTrials

### Reference Title
FDA Clinical Trials and Human Subject Protection

### Organization
US Food and Drug Administration (FDA)

### Reference Abstract
The FDA's main resource page for clinical trial regulations, guidance documents, and information on human subject protection. Covers the regulatory framework that applies to Coco Pharmaceuticals' drug development activities.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection |

### Category
Regulatory Guidance

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
FDA 21 CFR Part 11 — Electronic Records and Signatures

### Qualified Name
CocoPharma::ExternalReference::FDA::21CFRPart11

### Reference Title
21 CFR Part 11 — Electronic Records; Electronic Signatures

### Organization
US Food and Drug Administration (FDA)

### Reference Abstract
The specific FDA regulation governing electronic records and electronic signatures. Part 11 sets out the requirements for audit trails, access controls, and system validation that Coco Pharmaceuticals must meet for systems holding clinical trial data. Referenced directly by the FDA Clinical Trial Regulations governance driver.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 |

### Category
Regulation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
EudraLex Volume 4 — EU Guidelines for Good Manufacturing Practice

### Qualified Name
CocoPharma::ExternalReference::EMA::GMPGuidelines

### Reference Title
EudraLex — The Rules Governing Medicinal Products in the European Union, Volume 4

### Organization
European Commission — Directorate-General for Health and Food Safety

### Reference Abstract
Volume 4 of EudraLex contains the EU Guidelines for Good Manufacturing Practice for Medicinal Products for Human and Veterinary Use. This is the primary reference for GMP obligations applicable to Coco Pharmaceuticals' EU manufacturing operations.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en |

### Category
Regulatory Guidance

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
EMA — European Medicines Agency

### Qualified Name
CocoPharma::ExternalReference::EMA::HomePage

### Reference Title
European Medicines Agency

### Organization
European Medicines Agency (EMA)

### Reference Abstract
The EMA is the European Union agency responsible for the scientific evaluation, supervision, and safety monitoring of medicines. It publishes GMP inspection findings, guidance documents, and regulatory decisions relevant to Coco Pharmaceuticals' EU drug development and manufacturing activities.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://www.ema.europa.eu/ |
| GMP Inspections | https://www.ema.europa.eu/en/human-regulatory-overview/research-and-development/compliance-and-inspection/good-manufacturing-practice |

### Category
Regulatory Body

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
MHRA — Medicines and Healthcare products Regulatory Agency

### Qualified Name
CocoPharma::ExternalReference::MHRA::HomePage

### Reference Title
Medicines and Healthcare products Regulatory Agency

### Organization
Medicines and Healthcare products Regulatory Agency (MHRA)

### Reference Abstract
The MHRA is the UK government agency responsible for regulating medicines, medical devices, and blood components. It is the relevant GMP regulatory authority for Coco Pharmaceuticals' UK manufacturing operations following Brexit.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency |
| GMP Guidance | https://www.gov.uk/guidance/good-manufacturing-practice-and-good-distribution-practice |

### Category
Regulatory Body

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
Egeria — Governance Program Planning Guide

### Qualified Name
CocoPharma::ExternalReference::Egeria::GovernanceProgramGuide

### Reference Title
Planning a Governance Program with Egeria

### Organization
ODPi / LF AI & Data — Egeria Project

### Reference Abstract
The Egeria documentation page describing how to plan and implement a governance program using Egeria's open metadata capabilities. Covers governance domains, governance definitions, and the relationship between drivers, policies, and controls — the framework used to structure this document.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://egeria-project.org/guides/planning/governance-program/overview/ |

### Category
Egeria Documentation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
Egeria — Governance Officer View Service

### Qualified Name
CocoPharma::ExternalReference::Egeria::GovernanceOfficerAPI

### Reference Title
Governance Officer OMVS — API Reference

### Organization
ODPi / LF AI & Data — Egeria Project

### Reference Abstract
Documentation for the Egeria Governance Officer Open Metadata View Service (OMVS), the API used to create, update, and query governance definitions (drivers, policies, controls, and their relationships) in the Egeria metadata catalog. The Dr.Egeria templates in this document map to this API.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://egeria-project.org/services/omvs/governance-officer/overview/ |

### Category
Egeria Documentation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
Egeria — Open Metadata Types for Governance Definitions

### Qualified Name
CocoPharma::ExternalReference::Egeria::GovernanceDefinitionTypes

### Reference Title
Open Metadata Type — Governance Definitions (Area 4)

### Organization
ODPi / LF AI & Data — Egeria Project

### Reference Abstract
The Egeria documentation page describing the open metadata types that underpin governance definitions, including GovernanceDriver, BusinessImperative, Threat, Regulation, GovernancePrinciple, GovernanceObligation, GovernanceApproach, and GovernanceMetric. Understanding these types helps relate the definitions in this document to the underlying metadata model.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| Governance Definitions | https://egeria-project.org/types/4/0401-Governance-Definitions/ |
| Governance Drivers | https://egeria-project.org/types/4/0405-Governance-Drivers/ |
| Governance Responses | https://egeria-project.org/types/4/0415-Governance-Responses/ |
| Governance Controls | https://egeria-project.org/types/4/0420-Governance-Controls/ |
| Governance Metrics | https://egeria-project.org/types/4/0450-Governance-Rollout/ |

### Category
Egeria Documentation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
Egeria — Dr.Egeria User Interface

### Qualified Name
CocoPharma::ExternalReference::Egeria::DrEgeria

### Reference Title
Dr.Egeria — Markdown-Driven Metadata Authoring Interface

### Organization
ODPi / LF AI & Data — Egeria Project

### Reference Abstract
Documentation for Dr.Egeria, the Egeria user interface that interprets Markdown files (like this one) using Dr.Egeria templates to create and update metadata in the Egeria catalog. The templates in the Governance Officer subdirectory are used to load the governance definitions in this document into the live metadata catalog.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| URL | https://egeria-project.org/user-interfaces/dr-egeria/overview/ |

### Category
Egeria Documentation

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
Egeria — Coco Pharmaceuticals Data Strategy Scenario

### Qualified Name
CocoPharma::ExternalReference::Egeria::CocoDataStrategy

### Reference Title
Coco Pharmaceuticals — Defining the Data Strategy

### Organization
ODPi / LF AI & Data — Egeria Project

### Reference Abstract
The Egeria project's worked example of defining a data strategy for the fictional Coco Pharmaceuticals organisation. This scenario is the primary source material for the governance definitions in this document and provides narrative context for why each driver, policy, and control exists.

### Sources
| Parameter Name | Parameter Value |
|---|---|
| Data Strategy Overview | https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-the-data-strategy/overview/ |
| Governance Program | https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/creating-data-governance-program/overview/ |
| Building the Team | https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/building-the-governance-team/overview/ |
| Multi-Faceted Governance | https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-multi-faceted-governance/overview/ |

### Category
Egeria Documentation

### Content Status
ACTIVE

___

---

### 5.2 External Reference Links

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GDPR

### External Reference
CocoPharma::ExternalReference::GDPR::EURLex

### Description
Full text of the regulation that this governance driver is based on.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GDPR

### External Reference
CocoPharma::ExternalReference::ICO::HomePage

### Description
The UK supervisory authority for GDPR. The ICO's guidance and enforcement decisions are directly relevant to Coco Pharmaceuticals' GDPR compliance obligations.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernancePrinciple::PrivacyByDesign

### External Reference
CocoPharma::ExternalReference::ICO::HomePage

### Description
The ICO publishes practical guidance on implementing privacy by design that informs how this principle is applied at Coco Pharmaceuticals.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### External Reference
CocoPharma::ExternalReference::ICO::HomePage

### Description
The ICO provides guidance on classifying and handling personal data that informs the implementation of this obligation.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::FDAClinicalTrialRegulations

### External Reference
CocoPharma::ExternalReference::FDA::ClinicalTrials

### Description
The FDA's primary resource page for the clinical trial regulatory framework that this governance driver is based on.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::FDAClinicalTrialRegulations

### External Reference
CocoPharma::ExternalReference::FDA::21CFRPart11

### Description
21 CFR Part 11 is the specific regulation governing electronic records and audit trails for clinical trial data — a core requirement referenced by this governance driver.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GoodManufacturingPractice

### External Reference
CocoPharma::ExternalReference::EMA::GMPGuidelines

### Description
EudraLex Volume 4 is the primary EU source for the Good Manufacturing Practice requirements that this governance driver is based on.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GoodManufacturingPractice

### External Reference
CocoPharma::ExternalReference::EMA::HomePage

### Description
The EMA is the EU regulatory authority for GMP compliance and publishes inspection findings and updated guidance.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::GoodManufacturingPractice

### External Reference
CocoPharma::ExternalReference::MHRA::HomePage

### Description
The MHRA is the UK regulatory authority for GMP compliance, relevant to Coco Pharmaceuticals' UK manufacturing operations.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### External Reference
CocoPharma::ExternalReference::Egeria::GovernanceOfficerAPI

### Description
The Governance Officer API is the Egeria service through which this approach is implemented — all governance definitions are created and maintained via this API.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### External Reference
CocoPharma::ExternalReference::Egeria::DrEgeria

### Description
Dr.Egeria is the authoring interface used to load governance definitions from Markdown documents (like this one) into the Egeria catalog, directly implementing this approach.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### External Reference
CocoPharma::ExternalReference::Egeria::GovernanceProgramGuide

### Description
The Egeria governance program planning guide describes the framework and best practices that underpin this approach.

___

---

___

## Link External Reference

### Element Name
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### External Reference
CocoPharma::ExternalReference::Egeria::CocoDataStrategy

### Description
The Coco Pharmaceuticals data strategy scenario on the Egeria website provides the narrative context and background for this business imperative.

___

---

___

## Link External Reference

### Element Name
CocoPharma::GovernanceApproach::FederatedGovernanceWithCentralCoordination

### External Reference
CocoPharma::ExternalReference::Egeria::GovernanceProgramGuide

### Description
Egeria's governance program guide describes the federated, multi-domain governance model that this approach implements.

___

---

## Part 6: Governance Folios

A folio is a collection of governance definitions that a specific role is responsible for. Each folio groups the definitions owned or authored by a domain lead, making it easy to find all the governance work associated with a given role.

---

### 6.1 Folio Definitions

___

## Create Folio

### Display Name
Chief Data Officer — Governance Folio

### Qualified Name
CocoPharma::Folio::ChiefDataOfficer

### Description
The governance definitions owned by the Chief Data Officer (Jules Keeper). This folio covers the cross-cutting data governance program: the strategic business imperatives driving the transformation, the foundational data governance principles and obligations, the approaches that define how governance is practised, and the metrics used to measure effectiveness.

### Purpose
Provides Jules Keeper with a single view of all governance definitions he is responsible for authoring, maintaining, and enforcing across the organisation.

### Category
Governance Folio

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ChiefDataOfficer

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ChiefDataOfficer

### Description
Assigns the Chief Data Officer role responsibility for all governance definitions collected in the Chief Data Officer Governance Folio.

___

---

___

## Create Folio

### Display Name
Chief Information Security Officer — Governance Folio

### Qualified Name
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Description
The governance definitions owned by the Chief Information Security Officer (Ivor Padlock). This folio covers the security domain: the business imperative for cyber resilience, the cyber-attack threat, and the obligation for universal user authentication and accountability.

### Purpose
Provides Ivor Padlock with a single view of all security governance definitions he is responsible for authoring, maintaining, and enforcing.

### Category
Governance Folio

### Authors
Ivor Padlock

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ChiefInformationSecurityOfficer

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Description
Assigns the Chief Information Security Officer role responsibility for all governance definitions collected in the Chief Information Security Officer Governance Folio.

___

---

___

## Create Folio

### Display Name
Chief Privacy Officer — Governance Folio

### Qualified Name
CocoPharma::Folio::ChiefPrivacyOfficer

### Description
The governance definitions owned by the Chief Privacy Officer (Faith Broker). This folio covers the privacy domain: the unauthorised data disclosure threat, the GDPR regulation, the Privacy by Design principle, the obligation to classify personal data by sensitivity, and the metric tracking personal data breaches.

### Purpose
Provides Faith Broker with a single view of all privacy governance definitions she is responsible for authoring, maintaining, and enforcing.

### Category
Governance Folio

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ChiefPrivacyOfficer

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ChiefPrivacyOfficer

### Description
Assigns the Chief Privacy Officer role responsibility for all governance definitions collected in the Chief Privacy Officer Governance Folio.

___

---

___

## Create Folio

### Display Name
Chief Financial Officer — Governance Folio

### Qualified Name
CocoPharma::Folio::ChiefFinancialOfficer

### Description
The governance definitions owned by the Chief Financial Officer (Reggie Mint) in his capacity as the corporate governance domain lead. This folio currently covers the fraudulent supplier activity threat and will expand as corporate governance controls are defined.

### Purpose
Provides Reggie Mint with a single view of all corporate governance definitions he is responsible for authoring, maintaining, and enforcing.

### Category
Governance Folio

### Authors
Reggie Mint

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ChiefFinancialOfficer

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ChiefFinancialOfficer

### Description
Assigns the Chief Financial Officer role responsibility for all governance definitions collected in the Chief Financial Officer Governance Folio.

___

---

___

## Create Folio

### Display Name
Drug Development Lead — Governance Folio

### Qualified Name
CocoPharma::Folio::DrugDevelopmentLead

### Description
The governance definitions owned by the Drug Development Lead (Tessa Tube). This folio covers the FDA clinical trial regulatory requirements and will expand to include clinical data governance controls, certification types, and data processing purposes as the governance program matures.

### Purpose
Provides Tessa Tube with a single view of all drug development governance definitions she is responsible for authoring, maintaining, and enforcing.

### Category
Governance Folio

### Authors
Tessa Tube

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::DrugDevelopmentLead

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::DrugDevelopmentLead

### Description
Assigns the Drug Development Lead role responsibility for all governance definitions collected in the Drug Development Lead Governance Folio.

___

---

### 6.2 Folio Members

---

#### Chief Data Officer Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Membership Rationale
The CDO is accountable for ensuring data governance supports Coco Pharmaceuticals' strategic shift to personalised medicine.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::BusinessImperative::CycleTimeReduction

### Membership Rationale
Reducing cycle times depends on well-governed, high-quality data flowing between departments — a core CDO responsibility.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Membership Rationale
The CDO owns the response to this threat: ensuring governance knowledge is captured as documented metadata rather than held informally by individuals.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::Regulation::GoodManufacturingPractice

### Membership Rationale
GMP data integrity and traceability requirements sit within the CDO's data governance remit, in coordination with the Drug Development Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::InformationIsACompanyAsset

### Membership Rationale
This foundational principle is authored and championed by the CDO as the basis for the entire data governance program.

### Membership Status
VALIDATED

___



---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::InformationUseLimitedToApprovedEthicalPurposes

### Membership Rationale
Ensuring data is only used for approved, ethical purposes is a cross-cutting CDO responsibility spanning all domains.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Membership Rationale
The CDO is accountable for the register of information assets and their owners across the organisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Membership Rationale
The CDO is the sponsor and accountable owner of the Egeria-based metadata-driven governance approach.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::FederatedGovernanceWithCentralCoordination

### Membership Rationale
The CDO chairs the cross-domain governance forum and is the central coordinator of the federated governance model.

### Membership Status
VALIDATED

___

---
---

#### Chief Information Security Officer Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::BusinessImperative::CyberResilience

### Membership Rationale
The CISO is the accountable executive for the cyber resilience imperative and owns the security governance program that delivers it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Membership Rationale
The CISO is responsible for threat assessment and for the controls that mitigate the risk of cyber-attack.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Membership Rationale
User authentication and access logging are core security controls authored and owned by the CISO.

### Membership Status
VALIDATED

___

---

#### Chief Privacy Officer Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::Threat::UnauthorisedDataDisclosure

### Membership Rationale
Preventing unauthorised disclosure of personal data is a primary CPO responsibility.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::Regulation::GDPR

### Membership Rationale
The CPO is the accountable executive for GDPR compliance across the organisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Membership Rationale
Privacy by Design is the foundational privacy principle authored and championed by the CPO.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Membership Rationale
The CPO defines the personal data classification scheme and is accountable for its implementation across the organisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceMetric::PersonalDataBreachesReported

### Membership Rationale
The CPO is accountable for monitoring and reporting personal data breaches and for the 72-hour GDPR notification process.

### Membership Status
VALIDATED

___

---

#### Chief Financial Officer Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Threat::FraudulentSupplierActivity

### Membership Rationale
Supplier fraud is a financial and procurement risk. The CFO is accountable for the controls over supplier master data and procurement governance.

### Membership Status
VALIDATED

___

---

#### Drug Development Lead Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::DrugDevelopmentLead

### Element Id
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Membership Rationale
Tessa Tube is the domain lead for drug development and is accountable for ensuring clinical trial data governance meets FDA requirements.

### Membership Status
VALIDATED

___

---

### 6.3 Root Collection Membership

The governance folios are registered as members of the organisation's root governance folios collection, making them discoverable as a group in Egeria.

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ChiefDataOfficer

### Membership Rationale
The CDO folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Membership Rationale
The CISO folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Membership Rationale
The CPO folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ChiefFinancialOfficer

### Membership Rationale
The CFO folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::DrugDevelopmentLead

### Membership Rationale
The Drug Development Lead folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___

---

### 6.4 Collection Folder Memberships

___

## Create Collection Folder

### Display Name
Pharmaceutical Manufacturing Regulations

### Qualified Name
CollectionFolder::Coco::Pharmaceutical Manufacturing Regulations

### Purpose
Groups the regulations governing how Coco Pharmaceuticals manufactures medicinal products, as a branch of pharmaceutical industry regulation.

### Description
Pharmaceutical industry regulation covers everything from trial conduct through manufacture to supply, and the manufacturing part of it is large enough and specific enough to be found on its own. This folder holds the Good Manufacturing Practice regimes and the computerised systems requirements that attach to them, across every jurisdiction the company manufactures in or supplies. It sits inside the Pharmaceutical Industry Regulations folder rather than directly in the Corporate Regulation Library, because manufacturing regulation is a branch of pharmaceutical regulation rather than a category alongside it.

### Category
Regulation Category

### Authors
Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Pharmaceutical Industry Regulations

### Element Id
CollectionFolder::Coco::Pharmaceutical Manufacturing Regulations

### Membership Rationale
Manufacturing regulation is a branch of pharmaceutical industry regulation, so the manufacturing folder sits inside the pharmaceutical industry folder rather than alongside it in the library.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Pharmaceutical Manufacturing Regulations

### Element Id
CocoPharma::Regulation::GoodManufacturingPractice

### Membership Rationale
Good Manufacturing Practice is a pharmaceutical industry regulation applicable to Coco Pharmaceuticals' drug manufacturing operations.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Clinical Trial Regulations

### Element Id
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Membership Rationale
The FDA Clinical Trial Regulations govern the conduct, recording, and reporting of clinical trials undertaken by Coco Pharmaceuticals.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Privacy Regulations

### Element Id
CocoPharma::Regulation::GDPR

### Membership Rationale
GDPR is the primary privacy regulation applicable to Coco Pharmaceuticals' processing of personal data, including patient health data.

### Membership Status
VALIDATED

___

---

## Appendix: Governance Domain Leads

| Domain | Identifier | Lead | Description |
|--------|-----------|------|-------------|
| Data | DATA | Jules Keeper | Governance of data assets, definitions, quality, and use |
| Privacy | PRIVACY | Faith Broker | Governance of personal data handling and privacy compliance |
| Security | SECURITY | Ivor Padlock | Governance of access controls, cyber resilience, and incident response |
| IT Infrastructure | IT_INFRASTRUCTURE | Gary Geeke | Governance of systems, platforms, networks, and infrastructure |
| Software Development | SOFTWARE_DEVELOPMENT | Polly Tasker | Governance of software development practices and DevOps |
| Corporate | CORPORATE | Reggie Mint | Governance of financial reporting, supplier management, and corporate compliance |
