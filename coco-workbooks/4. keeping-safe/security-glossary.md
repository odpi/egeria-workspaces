# Coco Pharmaceuticals Security Glossary

> **Author:** Simon Burr (Chief Information Security Officer), Ivor Padlock (Chief Security Officer), Sidney Seeker (Security Consultant)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-26
> **Description:** The vocabulary that security people use - the goals and principles of security, the language of the information security management system, identity and access, kinds of attack, security testing and monitoring, and incident response.

---

## Overview

When Simon Burr joined Coco Pharmaceuticals as Chief Information Security Officer, he found that the words security people use every day meant different things to different people in the company.  *Threat*, *risk* and *vulnerability* were used interchangeably; a *security event* and a *security incident* were thought to be the same thing; and a *penetration test* was assumed to be the same as a *vulnerability scan*.  These differences mattered: the risk register, the ISMS policies and the security awareness training all depend on the words being understood the same way.

Si, Ivor Padlock and Sidney Seeker wrote this glossary to give everyone a shared vocabulary.  It is used in the security awareness training delivered through the governance education program, and it is the reference for the terms used in the security governance definitions, the risk register and the threat models.

The definitions are written in Coco Pharmaceuticals' own words, following common usage in ISO/IEC 27001, the NIST Cybersecurity Framework and the OWASP guidance.  Terms specific to Martyn's Law are in the separate Martyn's Law glossary.

The terms are organized into six folders:

* **Security Foundations** - The goals of security and the principles used to design protection.
* **Security Governance and Risk** - The vocabulary of the information security management system: assets, threats, vulnerabilities, risks and controls.
* **Identity and Access** - How users and systems are identified, authenticated and authorized, and how their access is kept appropriate.
* **Threats and Attacks** - The ways that attackers - external and internal - try to compromise the organization.
* **Security Testing and Monitoring** - How weaknesses are found before attackers find them, and how attacks are detected while they happen.
* **Incident Response and Recovery** - What happens when something goes wrong, and how the organization recovers.

**Prerequisites:** `0. data-governance-program/data-security-strategy.md` must already be loaded, because this file links the glossary to the security governance principle defined there.  The `SubjectArea::Governance` collection must also exist - it is loaded from `CocoComboArchive.omarchive` when the metadata server starts up.

---

## Part 1: The Glossary

___

## Create Glossary

### Display Name
Security Glossary

### Qualified Name
Glossary::SecurityGlossary

### Description
The vocabulary used by the security team at Coco Pharmaceuticals and in its security governance program: the goals and principles of security, the language of the information security management system, identity and access, kinds of attack, security testing and monitoring, and incident response.

### Language
English

### Usage
Reference this glossary when writing security policies, risks, threat models and training material, so that security terms carry the same meaning across the company.

### Purpose
To give everyone at Coco Pharmaceuticals a shared understanding of the words that security people use.

### Search Keywords
- Security
- Cyber Security
- ISMS
- ISO 27001
- Threat Modelling

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 1.1 A member of the Governance subject area

___

## Add Member to Collection

### Element Id
Glossary::SecurityGlossary

### Membership Rationale
Security is one of the systemic governance domains, and this glossary defines the vocabulary its definitions are written in.

### Membership Status
VALIDATED

### Collection Id
SubjectArea::Governance

___

---

### 1.2 Governed by the security governance program

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::RiskBasedInformationSecurityManagement

### Referenceable
Glossary::SecurityGlossary

### Label
defines the vocabulary of

### Description
The risk-based approach to information security management is expressed in the terms defined in this glossary - asset, threat, vulnerability, risk and control.

___

---

## Part 2: The Folders

___

## Create Collection Folder

### Display Name
Security Foundations

### Qualified Name
CollectionFolder::SecurityGlossary::Foundations

### Description
The goals of security and the principles used to design protection.

### Purpose
Groups the terms that describe what security is protecting and the principles used to protect it.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Security Governance and Risk

### Qualified Name
CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Description
The vocabulary of the information security management system: assets, threats, vulnerabilities, risks and controls.

### Purpose
Groups the terms used when assessing and treating security risk.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Identity and Access

### Qualified Name
CollectionFolder::SecurityGlossary::IdentityAndAccess

### Description
How users and systems are identified, authenticated and authorized, and how their access is kept appropriate.

### Purpose
Groups the terms about accounts, credentials, secrets and access.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Threats and Attacks

### Qualified Name
CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Description
The ways that attackers - external and internal - try to compromise the organization.

### Purpose
Groups the terms that name kinds of attack and the actors behind them.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Security Testing and Monitoring

### Qualified Name
CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Description
How weaknesses are found before attackers find them, and how attacks are detected while they happen.

### Purpose
Groups the terms about scanning, testing and monitoring the estate.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Incident Response and Recovery

### Qualified Name
CollectionFolder::SecurityGlossary::Response

### Description
What happens when something goes wrong, and how the organization recovers.

### Purpose
Groups the terms about handling incidents and restoring service.

### Parent ID
Glossary::SecurityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Content Status
ACTIVE

___

---

## Part 3: The Terms

### 3.1 Security Foundations

___

## Create Glossary Term

### Display Name
CIA Triad

### Abbreviation
CIA

### Summary
The three properties that information security protects: confidentiality, integrity and availability.

### Description
The CIA triad is the usual way of describing what security is for.  Information must be seen only by those entitled to see it (confidentiality), must not be changed except by authorized means (integrity), and must be available to the people and systems that need it when they need it (availability).  Different assets weigh the three differently: research formulas are mainly a confidentiality concern, batch records an integrity concern, and manufacturing control systems an availability concern.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::CIATriad

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Usage
Use when classifying an asset or assessing the impact of a risk, to say which of the three properties would be harmed.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Confidentiality

### Summary
The property that information is available only to those who are authorized to see it.

### Description
Confidentiality is breached when information is disclosed to a person, system or organization that is not entitled to it - whether by attack, by mistake or by an insider misusing legitimate access.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Confidentiality

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Usage
Use for the security property.  The privacy team's term for personal data is related but narrower.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Integrity

### Summary
The property that information and systems are accurate and complete, and have not been changed except by authorized means.

### Description
In security, integrity means protection against unauthorized or undetected change.  It is closely related to the manufacturing team's data integrity, which adds the requirements that records are attributable, contemporaneous and original.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Integrity

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Usage
Use for the security property.  When referring to GMP records, use Data Integrity from the Data Quality Glossary.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Availability

### Summary
The property that information and systems can be used by authorized people and processes when they are needed.

### Description
Availability is lost when a system is unavailable, whether through attack (for example ransomware or denial of service), failure or error.  For manufacturing systems it is often the most important of the three properties.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Availability

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Defence in Depth

### Summary
Protecting an asset with several independent layers of controls, so that the failure of one layer does not expose it.

### Description
Defence in depth assumes that any single control can fail or be bypassed.  Layers typically include network boundaries, authentication, authorization, encryption, monitoring and backups, so that an attacker who gets past one layer is stopped or detected by another.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::DefenceInDepth

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Least Privilege

### Summary
Giving each user, process and system only the access it needs to do its job, and no more.

### Description
Least privilege limits the damage that a compromised account or a mistake can do.  It applies to people, service accounts and software components alike, and needs regular review because access tends to accumulate over time.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::LeastPrivilege

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Separation of Duties

### Summary
Dividing a sensitive task between two or more people so that no one person can complete it alone.

### Description
Separation of duties protects against both fraud and error.  For example, the person who changes a supplier's bank details should not be the person who approves the payment.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SeparationOfDuties

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Example
After the supplier fraud, a change to a supplier's banking details must be approved by someone other than the person who entered it.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Zero Trust

### Summary
An approach in which no user or system is trusted because of where it is on the network; every request is authenticated and authorized.

### Description
Zero trust replaces the idea of a trusted internal network with checks on every request, based on the identity of the caller, the state of their device and the sensitivity of what they are asking for.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ZeroTrust

### Folders
- CollectionFolder::SecurityGlossary::Foundations

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.2 Security Governance and Risk

___

## Create Glossary Term

### Display Name
Information Security Management System

### Abbreviation
ISMS

### Summary
The policies, processes, people and controls an organization uses to manage information security risk, and to improve that management over time.

### Description
An information security management system is defined by the ISO/IEC 27001 standard.  It is operated as a continuous plan-do-check-act cycle: risks are assessed, controls are chosen and implemented, their operation is checked through audit and review, and corrective actions are taken.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ISMS

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
ISO/IEC 27001

### Summary
The international standard for an information security management system, against which an organization can be certified.

### Description
ISO/IEC 27001 sets out the requirements for an ISMS.  Its Annex A provides a reference set of controls covering organizational, people, physical and technological aspects of security.  Certification is issued, and re-audited each year, by an accredited certification body.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ISO27001

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Statement of Applicability

### Abbreviation
SoA

### Summary
The record of which ISO/IEC 27001 Annex A controls apply to the organization, why, and how each is implemented.

### Description
The Statement of Applicability lists every Annex A control, whether it is applicable, the justification for including or excluding it, and its implementation status.  Each applicable control should be traceable to the risk that justifies it.  It is one of the main documents reviewed in a certification audit.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::StatementOfApplicability

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Information Asset

### Summary
Anything of value to the organization that holds or processes information - data, systems, services, devices and the knowledge of people.

### Description
Information assets are what the ISMS protects.  They must be recorded in an asset inventory and classified for their confidentiality, integrity and availability needs, so that protection can be proportionate to their value.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::InformationAsset

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Asset Inventory

### Summary
The maintained list of the information assets within the scope of the ISMS, with their owners and classifications.

### Description
At Coco Pharmaceuticals the systems inventory maintained by the IT infrastructure team and the ISMS asset inventory are the same list seen from two angles, maintained once in Egeria.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::AssetInventory

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Threat

### Summary
Something that could cause harm to the organization by exploiting a weakness.

### Description
A threat is a potential cause of an unwanted event, such as a cyber-attack, a malicious insider or a natural disaster.  On its own it is not a risk: it becomes one when it could exploit a vulnerability in an asset the organization depends on.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Threat

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Usage
In the governance model a threat is a governance driver; the risks it gives rise to are linked to it.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Vulnerability

### Summary
A weakness in a system, process or control that a threat could exploit.

### Description
Vulnerabilities include unpatched software, misconfigurations, weak passwords, missing controls and gaps in procedures.  Many software vulnerabilities are published with a CVE identifier and a CVSS severity score.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Vulnerability

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Exploit

### Summary
A technique or piece of code that takes advantage of a vulnerability.

### Description
The existence of a public exploit for a vulnerability greatly increases the likelihood that it will be used, and so the priority for fixing it.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Exploit

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Security Risk

### Summary
The possibility that a threat exploits a vulnerability and harms an asset, expressed as a combination of likelihood and impact.

### Description
A risk is the concrete, assessable consequence of a threat for this organization.  It is rated for likelihood and impact, and the rating decides how much effort goes into treating it.  Risks are recorded in the risk register and scoped to the assets they threaten.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SecurityRisk

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Example
Cyber-attack is a threat.  Ransomware encrypting the manufacturing control systems and halting production is a risk.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Likelihood

### Summary
How probable it is that a risk will materialize.

### Description
Likelihood takes into account how attractive the asset is to an attacker, how easy the vulnerability is to exploit, and how effective the existing controls are.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Likelihood

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Impact

### Summary
How much harm would be done if a risk materialized.

### Description
Impact is assessed in terms of harm to patients, people, operations, finances, reputation and regulatory standing.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Impact

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Risk Treatment

### Summary
The decision on how to respond to a risk: reduce it with controls, avoid it, transfer it or accept it.

### Description
Most risks are treated by adding or strengthening controls.  Some are avoided by not doing the risky activity, some are transferred (for example through insurance or a contract), and some are accepted because the cost of treating them outweighs the harm.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::RiskTreatment

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Residual Risk

### Summary
The risk that remains after controls have been applied.

### Description
No set of controls removes risk entirely.  Residual risk must be understood and formally accepted by the risk owner.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ResidualRisk

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Security Control

### Summary
A measure that reduces the likelihood or impact of a security risk.

### Description
Controls can be technical (encryption, firewalls, multi-factor authentication), organizational (policies, separation of duties, training) or physical (locks, guards).  They can prevent, detect or correct an incident.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SecurityControl

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Threat Model

### Summary
A structured analysis of a system that identifies how it could be attacked and how each threat is mitigated.

### Description
A threat model describes the components of a system, the actors that interact with it, and the data flows between them, then works through the ways each could be attacked.  It is kept up to date as the system changes.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ThreatModel

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
STRIDE

### Abbreviation
STRIDE

### Summary
A checklist of six threat categories used in threat modelling: spoofing, tampering, repudiation, information disclosure, denial of service and elevation of privilege.

### Description
STRIDE gives a threat modelling session a consistent set of questions to ask of every component and data flow.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::STRIDE

### Folders
- CollectionFolder::SecurityGlossary::GovernanceAndRisk

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Identity and Access

___

## Create Glossary Term

### Display Name
Authentication

### Summary
Verifying that a user or system is who or what it claims to be.

### Description
Authentication is based on something the user knows (a password), has (a device or token) or is (a biometric).  It answers the question *who are you?*

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Authentication

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Authorization

### Summary
Deciding what an authenticated user or system is allowed to do.

### Description
Authorization answers the question *what may you do?*  It is applied after authentication, using roles, groups, access control lists or policies.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Authorization

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Multi-Factor Authentication

### Abbreviation
MFA

### Summary
Authentication that requires two or more independent kinds of evidence, such as a password and a code from a device.

### Description
Multi-factor authentication means that a stolen password on its own is not enough to log on.  It is one of the most effective controls against account compromise.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::MFA

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Identity and Access Management

### Abbreviation
IAM

### Summary
The processes and technology that create, maintain and remove user identities and their access rights.

### Description
Identity and access management covers the whole life of an identity - from creation when someone joins, through changes when they move role, to removal when they leave - and the access each identity is granted along the way.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::IAM

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Joiner, Mover, Leaver

### Abbreviation
JML

### Summary
The process of granting, adjusting and removing access as people join the organization, change role and leave.

### Description
Most access problems arise at the mover and leaver stages: access granted for a previous role is never removed, or the accounts of people who have left remain active.  The process depends on human resources telling the security team about each change.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::JoinerMoverLeaver

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Example
The supplier fraud used the accounts of employees who had left the company.

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Privileged Access

### Summary
Access that allows a user or system to change configuration, manage other accounts or bypass normal controls.

### Description
Administrator and root accounts, database owner rights and access to security tools are all privileged.  They are the most valuable accounts to an attacker, so their use is tightly limited, monitored and reviewed.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::PrivilegedAccess

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Service Account

### Summary
An account used by a software process rather than a person.

### Description
Service accounts are often highly privileged and rarely reviewed.  Each one should have a named owner and a recorded purpose, and its credentials should be held in a secrets store.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ServiceAccount

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Access Review

### Summary
A periodic check by the owner of a system that each account with access still needs it.

### Description
Access reviews catch the accounts and permissions that the joiner, mover, leaver process missed.  They provide the evidence auditors look for that access is controlled.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::AccessReview

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Secret

### Summary
A piece of information that grants access and must be kept from anyone not entitled to use it, such as a password, API key, token or private key.

### Description
Secrets should be kept in a secure secrets store, retrieved by the components that need them at runtime, and never written into configuration files, code or metadata.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Secret

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Credential Rotation

### Summary
Replacing passwords, keys and other credentials on a regular schedule, or immediately when they may have been exposed.

### Description
Rotation limits how long a stolen credential remains useful.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::CredentialRotation

### Folders
- CollectionFolder::SecurityGlossary::IdentityAndAccess

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.4 Threats and Attacks

___

## Create Glossary Term

### Display Name
Social Engineering

### Summary
Manipulating people into revealing information or taking actions that help an attacker.

### Description
Social engineering exploits trust, helpfulness, urgency and fear rather than technical weaknesses.  Awareness training is the main defence.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SocialEngineering

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Phishing

### Summary
A social engineering attack in which a message that appears to come from a trusted source tricks the recipient into revealing credentials, opening malware or making a payment.

### Description
Phishing is the most common starting point for cyber-attacks.  Targeted phishing aimed at particular individuals is called spear phishing.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Phishing

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Malware

### Summary
Software designed to harm a system or its users, such as viruses, worms, trojans, spyware and ransomware.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Malware

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Ransomware

### Summary
Malware that encrypts an organization's data or systems and demands payment to restore them, often also threatening to publish stolen data.

### Description
Ransomware attacks on manufacturers can halt production.  The main defences are network segmentation, offline and tested backups, prompt patching and a rehearsed incident response plan.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Ransomware

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Insider Threat

### Summary
Harm caused by someone with legitimate access to the organization's systems or premises - deliberately or through carelessness.

### Description
Insiders include employees, contractors and partners.  Because their access is legitimate, insider threats are countered by least privilege, separation of duties, monitoring and access reviews rather than by perimeter defences.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::InsiderThreat

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Supply Chain Attack

### Summary
An attack that compromises an organization through a supplier, partner or piece of third-party software it trusts.

### Description
Examples include malicious code inserted into a software update or open source package, and attackers using a supplier's access to reach the organization's systems.  A software bill of materials and supplier security assessments help to manage the risk.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SupplyChainAttack

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Denial of Service

### Abbreviation
DoS

### Summary
An attack that makes a system or service unavailable to its legitimate users, typically by overwhelming it.

### Description
When the attack comes from many machines at once it is called a distributed denial of service (DDoS).

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::DenialOfService

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Attack Surface

### Summary
All the points where an attacker could try to enter or extract data from a system.

### Description
The attack surface includes network services, user interfaces, APIs, accounts, devices and the people who use them.  Reducing it - by removing unused services and accounts - is one of the simplest ways to improve security.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::AttackSurface

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Adversarial Tactics, Techniques, and Common Knowledge

### Abbreviation
ATT&CK

### Summary
MITRE's public knowledge base of the tactics and techniques that attackers use, based on real-world observations.

### Description
MITRE ATT&CK organizes attacker behaviour into tactics - the attacker's goal at each stage, such as initial access, privilege escalation or exfiltration - and the techniques used to achieve them.  Each technique has an identifier, for example T1190 for exploiting a public-facing application.  Coco Pharmaceuticals uses these identifiers to record how a weakness was exploited in its penetration test findings, and to check that its threat models and detection rules cover the techniques most likely to be used against it.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ATTACK

### Folders
- CollectionFolder::SecurityGlossary::ThreatsAndAttacks

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.5 Security Testing and Monitoring

___

## Create Glossary Term

### Display Name
Vulnerability Scan

### Summary
An automated check of systems for known weaknesses, such as missing patches, exposed services and insecure configuration.

### Description
Vulnerability scans are run regularly across the whole estate.  They find known problems quickly but do not show whether a weakness can actually be exploited.  Their results are catalogued as survey reports with the category Vulnerability Scan Report.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::VulnerabilityScan

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Penetration Test

### Summary
An authorized, simulated attack on a system to find out which weaknesses an attacker could actually exploit, and how far they could get.

### Description
Penetration tests may be automated or carried out by skilled testers.  They go beyond a vulnerability scan by chaining weaknesses together as a real attacker would.  Their results are catalogued as survey reports with the category Penetration Test Results.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::PenetrationTest

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Continuous Penetration Testing

### Summary
Testing the defences continuously, rather than once a year, by combining scheduled automated testing with periodic expert-led tests.

### Description
Attackers probe continuously, so a test carried out once a year only shows how secure the systems were on the day of the test.  Continuous testing is scoped by the asset inventory and prioritized by the risk register.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::ContinuousPenetrationTesting

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Red Team

### Summary
A group that plays the role of an attacker to test an organization's defences, including its people and processes, not just its technology.

### Description
The defending team is called the blue team.  Exercises where the two work together to improve detection are called purple teaming.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::RedTeam

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Common Vulnerabilities and Exposures

### Abbreviation
CVE

### Summary
The public catalog that gives each disclosed software vulnerability a unique identifier.

### Description
A CVE identifier such as CVE-2021-44228 lets scanners, suppliers and security teams refer unambiguously to the same vulnerability.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::CVE

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Common Vulnerability Scoring System

### Abbreviation
CVSS

### Summary
A standard way of scoring the severity of a vulnerability from 0 to 10.

### Description
The CVSS base score reflects how easily a vulnerability can be exploited and how much harm it could do.  It is a starting point for prioritization, which should also take account of how important the affected asset is to the organization.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::CVSS

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Security Information and Event Management

### Abbreviation
SIEM

### Summary
A platform that collects security events from across the estate, correlates them and raises alerts.

### Description
A SIEM is fed by the security logs of systems such as directories, firewalls, applications and infrastructure.  Coco Pharmaceuticals' Austin and Bucharest sites both run a SIEM.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SIEM

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Security Event

### Summary
Any observable occurrence that may be relevant to security, such as a log-on, a failed authorization or a configuration change.

### Description
Most security events are harmless.  An event, or a pattern of events, that indicates actual or attempted harm is treated as a security incident.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SecurityEvent

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Loss Prevention

### Abbreviation
DLP

### Summary
Technology that detects and blocks sensitive data leaving the organization through unauthorized routes.

### Description
Data loss prevention monitors email, file transfers, cloud storage and removable media for sensitive content such as patient data or research formulas.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::DLP

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Indicator of Compromise

### Abbreviation
IoC

### Summary
Evidence that a system may have been breached, such as a known malicious file, address or pattern of behaviour.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::IndicatorOfCompromise

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Patch Management

### Summary
The process of applying software updates, particularly security fixes, across the estate in a controlled and timely way.

### Description
Patch management depends on knowing what software is running where.  Standard operating platforms and a software bill of materials for each deployment make it possible to roll out patches systematically.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::PatchManagement

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Software Bill of Materials

### Abbreviation
SBOM

### Summary
A list of the software packages and components that make up a deployed piece of software, with their versions and dependencies.

### Description
When a vulnerability is announced in a package, the software bills of materials show where that package is running.  In open metadata an SBOM is a collection with the SoftwarePackageManifest classification.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SBOM

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Network Segmentation

### Summary
Dividing a network into separate zones so that a compromise in one zone cannot easily spread to another.

### Description
Separating manufacturing control systems from the corporate network is a key defence against ransomware.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::NetworkSegmentation

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Encryption

### Summary
Transforming data so that it can be read only by those holding the right key.

### Description
Data is encrypted at rest (in storage) and in transit (over the network).  Encryption protects confidentiality only as well as the keys are protected.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Encryption

### Folders
- CollectionFolder::SecurityGlossary::TestingAndMonitoring

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.6 Incident Response and Recovery

___

## Create Glossary Term

### Display Name
Security Incident

### Summary
An event that actually or potentially harms the confidentiality, integrity or availability of information or systems.

### Description
Every suspected security incident is reported through a single channel, logged, investigated and reviewed for lessons learned.  In open metadata it is recorded as an incident report linked to the resources it affects.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::SecurityIncident

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Incident Response

### Summary
The planned process for detecting, containing, eradicating and recovering from a security incident, and learning from it.

### Description
An incident response plan sets out who does what, how decisions are made and who must be notified.  It must be tested regularly so that people know their roles before a real incident.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::IncidentResponse

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Containment

### Summary
Stopping an incident from spreading or causing further harm, for example by isolating affected systems or disabling compromised accounts.

### Description
The time from an incident being reported to it being contained is measured by the Security Incident Mean Time to Containment metric.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::Containment

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Business Continuity

### Summary
The ability of the organization to keep delivering its critical services during and after a disruption.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::BusinessContinuity

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Recovery Time Objective

### Abbreviation
RTO

### Summary
The maximum acceptable time to restore a service after a disruption.

### Description
Recovery time objectives are set by the business that depends on the service and tested regularly.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::RTO

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Recovery Point Objective

### Abbreviation
RPO

### Summary
The maximum acceptable amount of data loss, measured as time before the disruption.

### Description
A recovery point objective of four hours means that backups or replicas must be no more than four hours old.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::RPO

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Offline Backup

### Summary
A backup copy kept disconnected from the network, so that an attacker or ransomware cannot reach it.

### Description
Offline, tested backups are the last line of defence against ransomware.  A backup that has never been restored cannot be relied on.

### Glossary Name
Glossary::SecurityGlossary

### Qualified Name
Glossary::SecurityGlossary::OfflineBackup

### Folders
- CollectionFolder::SecurityGlossary::Response

### Authors
- Simon Burr
- Ivor Padlock
- Sidney Seeker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Relationships Between the Terms

The *ISARelationship* links show which terms are kinds or parts of others, and the *RelatedTerm* links show how the concepts depend on each other - for example, that a risk is realised by a threat exploiting a vulnerability, and is reduced by controls.

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Confidentiality

### Term 2
Glossary::SecurityGlossary::CIATriad

### Expression
is part of

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Integrity

### Term 2
Glossary::SecurityGlossary::CIATriad

### Expression
is part of

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Availability

### Term 2
Glossary::SecurityGlossary::CIATriad

### Expression
is part of

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::Phishing

### Term 2
Glossary::SecurityGlossary::SocialEngineering

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::Ransomware

### Term 2
Glossary::SecurityGlossary::Malware

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::MFA

### Term 2
Glossary::SecurityGlossary::Authentication

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::PenetrationTest

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::VulnerabilityScan

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::ContinuousPenetrationTesting

### Term 2
Glossary::SecurityGlossary::PenetrationTest

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::DLP

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::Encryption

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::SecurityGlossary::NetworkSegmentation

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ISMS

### Term 2
Glossary::SecurityGlossary::ISO27001

### Expression
is defined by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::StatementOfApplicability

### Term 2
Glossary::SecurityGlossary::ISO27001

### Expression
is required by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ISMS

### Term 2
Glossary::SecurityGlossary::AssetInventory

### Expression
protects the assets in

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::AssetInventory

### Term 2
Glossary::SecurityGlossary::InformationAsset

### Expression
lists

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityRisk

### Term 2
Glossary::SecurityGlossary::Threat

### Expression
is realised by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityRisk

### Term 2
Glossary::SecurityGlossary::Vulnerability

### Expression
depends on

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityRisk

### Term 2
Glossary::SecurityGlossary::Likelihood

### Expression
is rated by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityRisk

### Term 2
Glossary::SecurityGlossary::Impact

### Expression
is rated by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::RiskTreatment

### Term 2
Glossary::SecurityGlossary::SecurityRisk

### Expression
responds to

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ResidualRisk

### Term 2
Glossary::SecurityGlossary::SecurityRisk

### Expression
remains of

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityControl

### Term 2
Glossary::SecurityGlossary::SecurityRisk

### Expression
reduces

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Exploit

### Term 2
Glossary::SecurityGlossary::Vulnerability

### Expression
takes advantage of

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ThreatModel

### Term 2
Glossary::SecurityGlossary::STRIDE

### Expression
is often structured by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ThreatModel

### Term 2
Glossary::SecurityGlossary::AttackSurface

### Expression
describes

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Authentication

### Term 2
Glossary::SecurityGlossary::Authorization

### Expression
precedes

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::IAM

### Term 2
Glossary::SecurityGlossary::JoinerMoverLeaver

### Expression
includes

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::AccessReview

### Term 2
Glossary::SecurityGlossary::LeastPrivilege

### Expression
enforces

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::PrivilegedAccess

### Term 2
Glossary::SecurityGlossary::LeastPrivilege

### Expression
is limited by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ServiceAccount

### Term 2
Glossary::SecurityGlossary::Secret

### Expression
uses

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::CredentialRotation

### Term 2
Glossary::SecurityGlossary::Secret

### Expression
renews

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::InsiderThreat

### Term 2
Glossary::SecurityGlossary::SeparationOfDuties

### Expression
is countered by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::VulnerabilityScan

### Term 2
Glossary::SecurityGlossary::PenetrationTest

### Expression
is followed by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Vulnerability

### Term 2
Glossary::SecurityGlossary::CVE

### Expression
is identified by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::CVE

### Term 2
Glossary::SecurityGlossary::CVSS

### Expression
is scored by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::PatchManagement

### Term 2
Glossary::SecurityGlossary::SBOM

### Expression
depends on

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SupplyChainAttack

### Term 2
Glossary::SecurityGlossary::SBOM

### Expression
is investigated with

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SIEM

### Term 2
Glossary::SecurityGlossary::SecurityEvent

### Expression
correlates

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityEvent

### Term 2
Glossary::SecurityGlossary::SecurityIncident

### Expression
may indicate

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::SecurityIncident

### Term 2
Glossary::SecurityGlossary::IncidentResponse

### Expression
is handled by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::IncidentResponse

### Term 2
Glossary::SecurityGlossary::Containment

### Expression
includes

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Ransomware

### Term 2
Glossary::SecurityGlossary::OfflineBackup

### Expression
is countered by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::Ransomware

### Term 2
Glossary::SecurityGlossary::NetworkSegmentation

### Expression
is countered by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::BusinessContinuity

### Term 2
Glossary::SecurityGlossary::RTO

### Expression
is measured by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::BusinessContinuity

### Term 2
Glossary::SecurityGlossary::RPO

### Expression
is measured by

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::DefenceInDepth

### Term 2
Glossary::SecurityGlossary::SecurityControl

### Expression
layers

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ZeroTrust

### Term 2
Glossary::SecurityGlossary::Authentication

### Expression
relies on

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::PenetrationTest

### Term 2
Glossary::SecurityGlossary::ATTACK

### Expression
records the techniques it used with identifiers from

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::SecurityGlossary::ThreatModel

### Term 2
Glossary::SecurityGlossary::ATTACK

### Expression
checks its coverage against

### Steward
Simon Burr

### Term Relationship Status
ACTIVE

___

---

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
