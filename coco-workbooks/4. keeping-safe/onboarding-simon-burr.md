# Onboarding Simon Burr

> **Author:** Simon Burr (Chief Information Security Officer), Ivor Padlock (Chief Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-26
> **Description:** Onboards Simon Burr as Coco Pharmaceuticals' first Chief Information Security Officer: his person profile, the CISO governance role and his appointment to it, his governance folio, and his plan for his first ninety days.

---

## Overview

When the scenarios begin, Ivor Padlock is Coco Pharmaceuticals' only security officer, responsible for both physical and IT security.  He has a lot of experience of physical security but no real IT background, so when the fraud around the supplier database was detected he engaged Sidney Seeker as a security consultant.  On the IT side he had relied on Gary Geeke, who joined the company from college and learnt IT systems management, and the security that goes with it, on the job.  Gary has been a great help, but he is no security expert either.

Sidney's review of the situation recommended that the company employ more security staff.  In typical Coco Pharmaceuticals style, they employed one new person: Simon Burr, known as Si, joins as Chief Information Security Officer (CISO).  Si reports to Ivor, who becomes the Chief Security Officer and remains head of the security governance domain.

This file records Si's arrival in open metadata:

1. **Si's profile** - his person profile, the new CISO governance role, and his appointment to it.
2. **Si's governance folio** - the definitions from the data security strategy and the risk register that he operates day to day.  Ivor remains accountable for them, so they stay in the Chief Security Officer's folio too.
3. **Si's first ninety days** - a campaign of three thirty-day projects, following the pattern Jules Keeper used when she joined.  Part of his remit is to set up continuous penetration testing across the company, and he plans to build on the security monitoring and testing experience of the two acquisitions in Austin and Bucharest.

Si's user account (`simonburr`) is in the quickstart user directory.  His user identity is created, and linked to this profile, the first time he logs on through My Egeria.  Until then, Egeria Audit reports his account as a *Missing User Identity* - a useful first exercise for Si himself.

**Prerequisites:** load `0. data-governance-program` (which defines the Chief Security Officer role and folio, the data security strategy and the risk register) first.  This file is loaded as Simon Burr:

```
dr_egeria --directive process --userid simonburr --user_pass secret onboarding-simon-burr.md
```

---

## Part 1: Si's profile and role

___

## Create Person

### Display Name
Simon Burr

### Qualified Name
Person::USA::512047

### Full Name
Mr Simon Burr

### Courtesy Title
Mr

### Given Names
Simon

### Surname
Burr

### Initials
S

### Pronouns
He/him/his

### Job Title
Chief Information Security Officer

### Employee Number
512047

### Employee Type
Permanent

### Resident Country
USA

### Preferred Language
English

### Description
Si is Coco Pharmaceuticals' first Chief Information Security Officer.  He is a cyber-security and penetration testing specialist, responsible for monitoring, testing and validating the security of the company's IT systems and services.  He reports to Ivor Padlock, the Chief Security Officer, and spends much of his time working with Polly Tasker on the active IT projects and with Gary Geeke on the security of the IT infrastructure.

### Search Keywords
- CISO
- cyber security
- penetration testing

___

---

___

## Create Governance Role

### Display Name
Chief Information Security Officer

### Qualified Name
CocoPharma::GovernanceRole::ChiefInformationSecurityOfficer

### Description
The Chief Information Security Officer (CISO) is responsible for the security of Coco Pharmaceuticals' information and IT systems.  The CISO operates the information security management system (ISMS) - including risk assessment, the ISO/IEC 27001 controls, management reviews and certification audits - leads the technical response to security incidents, and sets up and runs continuous security testing and monitoring across the company.  The CISO reports to the Chief Security Officer, who remains head of the security governance domain.

### Scope
Information and IT system security across Coco Pharmaceuticals, including the sites acquired in Austin and Bucharest.

### Headcount
1

### Category
Governance Role

### Search Keywords
- CISO
- information security
- ISMS
- cyber security

### Version Identifier
1.0

___

---

___

## Link Person Role Appointment

### Person
Person::USA::512047

### Person Role
CocoPharma::GovernanceRole::ChiefInformationSecurityOfficer

___

---

## Part 2: Si's governance folio

___

## Create Folio

### Display Name
Chief Information Security Officer - Governance Folio

### Qualified Name
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Description
The governance definitions operated day to day by the Chief Information Security Officer (Simon Burr): the ISMS operating cycle, ISO/IEC 27001 certification and the metrics that track it, the obligations for the asset inventory, incident handling and user accountability, and the critical cyber security risks.  The Chief Security Officer remains accountable for them, so they are also members of the Chief Security Officer's folio.

### Purpose
Provides Simon Burr with a single view of the security governance definitions he operates.

### Category
Governance Folio

### Authors
- Simon Burr

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
Assigns the Chief Information Security Officer role responsibility for operating the governance definitions collected in the Chief Information Security Officer Governance Folio.

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
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceApproach::ISMSPlanDoCheckActCycle

### Membership Rationale
The CISO runs the ISMS plan-do-check-act cycle, including internal audits and management reviews.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::CertificationType::ISO27001

### Membership Rationale
The CISO prepares for and supports the ISO/IEC 27001 certification and surveillance audits.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceMetric::ISO27001ControlImplementationRate

### Membership Rationale
The CISO maintains the Statement of Applicability and the evidence behind this metric.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceMetric::SecurityIncidentMeanTimeToContainment

### Membership Rationale
The CISO leads the technical response to security incidents, which this metric measures.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceObligation::SecurityIncidentsLoggedReportedReviewed

### Membership Rationale
The CISO operates the incident logging, investigation and review process.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::GovernanceObligation::InformationAssetsInventoriedAndClassifiedForISMS

### Membership Rationale
The asset inventory defines the scope of the CISO's monitoring and continuous penetration testing.

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
The CISO runs the routine audit of user accounts, including Egeria's own users.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::Risk::RansomwareDisruptionToManufacturing

### Membership Rationale
One of the two Critical cyber security risks that set the CISO's priorities.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::Risk::TheftOfPersonalisedTreatmentIP

### Membership Rationale
One of the two Critical cyber security risks that set the CISO's priorities.

### Membership Status
VALIDATED

___

---

## Part 3: Si's first ninety days

___

## Create Campaign

### Display Name
My First Ninety Days as CISO

### Qualified Name
SimonBurr::Campaign::FirstNinetyDays

### Project Type
Campaign

### Mission
To make a fast, well-informed start as Coco Pharmaceuticals' first Chief Information Security Officer - learning the security landscape, establishing the threat models, vocabulary and plans the security program needs, and getting continuous security testing and monitoring running.

### Description
A ninety-day plan covering my first three months as CISO, divided into three thirty-day projects: a Learning Phase, an Establishing Phase and an Operating Phase.

### Sub-Projects
- SimonBurr::Project::First30DaysLearningPhase
- SimonBurr::Project::Next30DaysEstablishingPhase
- SimonBurr::Project::Final30DaysOperatingPhase

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Project

### Display Name
First 30 Days (Learning Phase)

### Qualified Name
SimonBurr::Project::First30DaysLearningPhase

### Project Phase
Learning

### Mission
To understand Coco Pharmaceuticals' security position - its people, its systems, its strategy and its risks - before changing anything.

### Description
My first job is to listen.  I need to get to know Ivor, Sidney, Gary and Lemmie, read the data security strategy and the risk register, and understand what is actually running.  The systems inventory in Egeria is my starting point.  The two acquisitions run security monitoring and testing that the original Coco Pharmaceuticals estate does not have, so I want to learn from the people who run it there.

### Success Criteria
- Met the security team and the IT colleagues they rely on
- Reviewed the data security strategy, the risk register and the systems inventory
- Learnt how security is monitored and tested at Austin and Bucharest
- Audited the users of Egeria itself

### Sub-Projects
- SimonBurr::Task::First30DaysLearningPhase::MeetTheTeam
- SimonBurr::Task::First30DaysLearningPhase::ReviewStrategyAndRisks
- SimonBurr::Task::First30DaysLearningPhase::ReviewSystemsInventory
- SimonBurr::Task::First30DaysLearningPhase::LearnFromAcquisitions
- SimonBurr::Task::First30DaysLearningPhase::AuditEgeriaUsers

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Meet Ivor, Sidney, Gary and Lemmie

### Qualified Name
SimonBurr::Task::First30DaysLearningPhase::MeetTheTeam

### Mission
To understand how security has been run so far, and where my colleagues think the gaps are.

### Description
Meet Ivor Padlock, Sidney Seeker, Gary Geeke and Lemmie Stage to learn how security has been handled, what the fraud investigation found, and how the IT systems are built, deployed and run.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Review the security strategy and risk register

### Qualified Name
SimonBurr::Task::First30DaysLearningPhase::ReviewStrategyAndRisks

### Mission
To understand what the company has committed to and which risks matter most.

### Description
Read the data security strategy and the risk register, and the governance definitions in the Chief Security Officer's folio, paying particular attention to the two Critical cyber security risks.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Review the systems inventory

### Qualified Name
SimonBurr::Task::First30DaysLearningPhase::ReviewSystemsInventory

### Mission
To know what I am protecting.

### Description
Work through the systems inventory in Egeria with Gary Geeke, including the systems of the Austin and Bucharest acquisitions, to understand what runs where and who owns it.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Learn from the Austin and Bucharest security teams

### Qualified Name
SimonBurr::Task::First30DaysLearningPhase::LearnFromAcquisitions

### Mission
To build on the security monitoring and testing that the acquisitions already run.

### Description
Meet the people who run the SIEM, threat detection, data loss prevention and penetration testing at Austin and Bucharest, and learn what they monitor, what they test, how often, and what they have learned.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Audit Egeria's own users

### Qualified Name
SimonBurr::Task::First30DaysLearningPhase::AuditEgeriaUsers

### Mission
To make sure that open metadata - which now describes our systems and their weaknesses - is itself kept safe.

### Description
Use Egeria Audit to review the user accounts, clear-text passwords, missing user identities and unsecured governance zones in Egeria, starting with my own account.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Project

### Display Name
Next 30 Days (Establishing Phase)

### Qualified Name
SimonBurr::Project::Next30DaysEstablishingPhase

### Project Phase
Establishing

### Mission
To put in place the models, vocabulary and plans the security program needs.

### Description
With the landscape understood, I need to model the threats, agree a shared vocabulary, and plan the testing and monitoring that will tell us whether our defences work.

### Success Criteria
- Threat models built for the strategic information supply chains, with risks scoped to the components they threaten
- A security glossary agreed with Ivor and Sidney
- A plan for continuous penetration testing, scoped by the inventory and prioritized by the risk register
- A design for extending security monitoring to the original Coco Pharmaceuticals systems

### Sub-Projects
- SimonBurr::Task::Next30DaysEstablishingPhase::ThreatModelSupplyChains
- SimonBurr::Task::Next30DaysEstablishingPhase::WriteSecurityGlossary
- SimonBurr::Task::Next30DaysEstablishingPhase::PlanContinuousPenetrationTesting
- SimonBurr::Task::Next30DaysEstablishingPhase::DesignMonitoringExtension

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Threat model the strategic information supply chains

### Qualified Name
SimonBurr::Task::Next30DaysEstablishingPhase::ThreatModelSupplyChains

### Mission
To identify how the systems the business depends on could be attacked.

### Description
Use the STRIDE method on the solution components of the strategic information supply chains, and scope each risk to the components it threatens.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Write the security glossary

### Qualified Name
SimonBurr::Task::Next30DaysEstablishingPhase::WriteSecurityGlossary

### Mission
To give everyone a shared understanding of the words security people use.

### Description
Write the security glossary with Ivor Padlock and Sidney Seeker, for use in the security awareness training.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Plan continuous penetration testing

### Qualified Name
SimonBurr::Task::Next30DaysEstablishingPhase::PlanContinuousPenetrationTesting

### Mission
To test our defences continuously rather than once a year.

### Description
Design the layers of testing - scheduled vulnerability scanning, automated penetration testing and periodic expert-led tests - scoped by the systems inventory and prioritized by the risks scoped to each component.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Design the extension of security monitoring

### Qualified Name
SimonBurr::Task::Next30DaysEstablishingPhase::DesignMonitoringExtension

### Mission
To make sure attacks on the original Coco Pharmaceuticals systems are detected.

### Description
Using the security event flows of the acquisitions' SIEMs as a template, identify where each original Coco Pharmaceuticals system's security events should go, and what is not monitored today.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Project

### Display Name
Final 30 Days (Operating Phase)

### Qualified Name
SimonBurr::Project::Final30DaysOperatingPhase

### Project Phase
Operating

### Mission
To have security testing and monitoring running, and to show the governance leaders that it is working.

### Description
By the end of my first ninety days, the testing should be running and its results flowing into Egeria, so that I can report progress with evidence rather than opinion.

### Success Criteria
- Vulnerability scanning and automated penetration testing running against the highest-priority systems
- Test results catalogued in Egeria as survey reports
- The first ISMS management review held
- Progress reported to Ivor and the governance leaders

### Sub-Projects
- SimonBurr::Task::Final30DaysOperatingPhase::StartContinuousTesting
- SimonBurr::Task::Final30DaysOperatingPhase::FirstManagementReview
- SimonBurr::Task::Final30DaysOperatingPhase::ReportProgress

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Start continuous testing

### Qualified Name
SimonBurr::Task::Final30DaysOperatingPhase::StartContinuousTesting

### Mission
To find weaknesses before attackers do.

### Description
Start scheduled vulnerability scanning and automated penetration testing on the systems that implement the components with the highest-rated risks, and catalogue the results through the Data Discovery API.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Hold the first ISMS management review

### Qualified Name
SimonBurr::Task::Final30DaysOperatingPhase::FirstManagementReview

### Mission
To start the plan-do-check-act cycle.

### Description
Hold the first ISMS management review, using the control implementation rate and the first test results to decide what to act on next.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Task

### Display Name
Report progress to the governance leaders

### Qualified Name
SimonBurr::Task::Final30DaysOperatingPhase::ReportProgress

### Mission
To show the value of the investment in IT security.

### Description
Report to Ivor Padlock and the governance leaders on what has been found, what has been fixed, and what is planned next.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### Dependencies between the tasks

___

## Link Project Dependency

### Dependent Project
SimonBurr::Task::Next30DaysEstablishingPhase::ThreatModelSupplyChains

### Depends on Project
SimonBurr::Task::First30DaysLearningPhase::ReviewSystemsInventory

___

---

___

## Link Project Dependency

### Dependent Project
SimonBurr::Task::Next30DaysEstablishingPhase::PlanContinuousPenetrationTesting

### Depends on Project
SimonBurr::Task::First30DaysLearningPhase::LearnFromAcquisitions

___

---

___

## Link Project Dependency

### Dependent Project
SimonBurr::Task::Next30DaysEstablishingPhase::PlanContinuousPenetrationTesting

### Depends on Project
SimonBurr::Task::Next30DaysEstablishingPhase::ThreatModelSupplyChains

___

---

___

## Link Project Dependency

### Dependent Project
SimonBurr::Task::Next30DaysEstablishingPhase::DesignMonitoringExtension

### Depends on Project
SimonBurr::Task::First30DaysLearningPhase::LearnFromAcquisitions

___

---

___

## Link Project Dependency

### Dependent Project
SimonBurr::Task::Final30DaysOperatingPhase::StartContinuousTesting

### Depends on Project
SimonBurr::Task::Next30DaysEstablishingPhase::PlanContinuousPenetrationTesting

___

---

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
