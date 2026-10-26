# Coco Pharmaceuticals - The Annual Conference

> **Author:** Ivor Padlock (Chief Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-26
> **Description:** Describes Coco Pharmaceuticals' annual conference in London as a project, defines the Responsible Person role that Martyn's Law requires for it, and scopes the role and the two event security risks in the [Risk Register](../../0.%20data-governance-program/risk-register.md) to the conference.  Load after the other Martyn's Law files and after `0. data-governance-program`.

---

## Overview

Martyn's Law places its duties on the person who has control of the premises in connection with their use for a qualifying event.  For Coco Pharmaceuticals, that event is the annual conference in London.  Until now the conference has not been described in open metadata, so the role the Act requires and the risks Ivor identified had nothing to be scoped to.

This file:

1. creates a project for the annual conference,
2. defines the *Responsible Person* governance role,
3. links the role and the two event security risks to the conference with the `ScopedBy` relationship, and
4. adds the project and the role to the Martyn's Law collection folder.

The role is defined but not yet appointed.  Formally designating the Responsible Person well ahead of the 2027 enforcement date is one of the implications of the *Failure to Discharge Martyn's Law Responsible Person Duties* risk.

---

## Part 1: The Annual Conference

___

## Create Project

### Display Name
Coco Pharmaceuticals Annual Conference (London)

### Qualified Name
CocoPharma::Project::AnnualConferenceLondon

### Description
Coco Pharmaceuticals' annual conference in London, bringing together employees, partners and customers.  Attendance has grown steadily and is now around 700 people, which places the conference in the standard tier of the Terrorism (Protection of Premises) Act 2025 (Martyn's Law).  If attendance reaches 800 the conference becomes a qualifying event in the enhanced tier, with additional duties for the Responsible Person.

### Mission
Deliver a safe, well-run annual conference that meets the duties of Martyn's Law for every attendee, member of staff and venue partner.

### Project Scope
The planning and running of the annual conference, including the choice of venue, the public protection procedures agreed with the venue, the briefing of staff working at the event, and communications with attendees.

### Success Criteria
- Public protection procedures (evacuation, invacuation, lockdown and communication) are documented and rehearsed before each conference
- The venue security assessment is refreshed for each conference
- Staff working at the event are briefed on their role in the public protection procedures
- Attendance is monitored against the 800-attendee enhanced tier threshold

### Category
In-person Meetings and Events

### Search Keywords
- annual conference
- Martyn's Law
- event security

### Authors
- Ivor Padlock

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: The Responsible Person

___

## Create Governance Role

### Display Name
Martyn's Law Responsible Person - Annual Conference

### Qualified Name
CocoPharma::GovernanceRole::MartynsLawResponsiblePerson

### Description
The person responsible for discharging Coco Pharmaceuticals' duties under the Terrorism (Protection of Premises) Act 2025 (Martyn's Law) for the annual conference.  The Responsible Person ensures that public protection procedures are in place and rehearsed, that the venue's security arrangements are assessed for each conference, and that staff working at the event know their role.  If attendance reaches the enhanced tier threshold of 800, the Responsible Person must also notify the Security Industry Authority (SIA) of the event, and must be a senior individual with authority to ensure compliance.

### Scope
The annual conference in London, from venue selection through to the end of the event.

### Headcount
1

### Category
Governance Role

### Search Keywords
- Martyn's Law
- responsible person
- event security

### Version Identifier
1.0

___

---

## Part 3: Scoping the role and the risks to the conference

___

## Link Element To Scope

### Target Element
CocoPharma::GovernanceRole::MartynsLawResponsiblePerson

### Scope Reference
CocoPharma::Project::AnnualConferenceLondon

### Label
responsible-for-event

### Description
The duties of the Responsible Person apply to the annual conference as a qualifying event, rather than to Coco Pharmaceuticals as a whole.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::TerrorismIncidentAtAnnualConference

### Scope Reference
CocoPharma::Project::AnnualConferenceLondon

### Label
threatened-event

### Description
The annual conference, with around 700 attendees, is the event that could be the scene of, or affected by, a terrorism-related incident.

___

---

___

## Link Element To Scope

### Target Element
CocoPharma::Risk::MartynsLawResponsiblePersonNonCompliance

### Scope Reference
CocoPharma::Project::AnnualConferenceLondon

### Label
threatened-event

### Description
The Responsible Person duties that could fail to be discharged are those for the annual conference.

___

---

## Part 4: Adding the conference to the Martyn's Law folder

___

## Add Member to Collection

### Collection Id
CollectionFolder::MartynsLawUK

### Element Id
CocoPharma::Project::AnnualConferenceLondon

### Membership Rationale
The annual conference is the event that Martyn's Law applies to at Coco Pharmaceuticals.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::MartynsLawUK

### Element Id
CocoPharma::GovernanceRole::MartynsLawResponsiblePerson

### Membership Rationale
The Responsible Person is the role the Act requires for the annual conference.

### Membership Status
VALIDATED

___

---

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
