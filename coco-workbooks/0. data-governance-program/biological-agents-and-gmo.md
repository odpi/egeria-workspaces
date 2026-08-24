# Coco Pharmaceuticals — Biological Agents and Contained Use of GMOs

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Governance definitions for work with biological agents and for contained use of genetically modified organisms, carrying Domain Identifier `24` — Health and Safety. Separated from `health-and-safety.md` because contained use is a distinct regulatory regime with its own classification scheme, its own regulator relationship, and a notification duty that must be discharged before work begins. Load `health-and-safety.md` and `manufacturing-governance-program.md` first.

---

## Overview

Two things in this company involve biological agents, and only one of them is obvious.

The first is research. Laboratories work with cell lines, viral vectors, and microbiological cultures, and some of that work involves agents capable of causing human disease. This is ordinary biological safety, governed as occupational health.

The second is the personalised medicine programme, and it is not obvious at all from the way the rest of the governance program describes it. Autologous cell therapy takes a patient's own cells, modifies them — frequently using a viral vector to introduce genetic material — and returns them. That is *contained use of genetically modified organisms* in the legal sense, and it brings a regulatory regime that the manufacturing, drug development, and health and safety programs between them do not currently touch. `manufacturing-governance-program.md` governs the patient identity attached to that material and the chain of identity that keeps it matched to its patient. Nothing governs the fact that the material is a genetically modified organism, that the activity has a hazard classification, or that the premises and the activity must be notified to the competent authority before work starts.

The distinction that makes this its own file is that contained use is regulated by *activity*, not by substance. A COSHH assessment describes a substance and the tasks done with it. A contained use notification describes a class of activity at a set of premises, is submitted in advance, and constrains what may be done there until it is varied. Missing a substance from the chemical register is a gap to be closed; conducting an unnotified class 2 activity is an offence committed on the first day of work.

The definitions here carry Domain Identifier `24` and join the Head of Health and Safety folio. They are not a separate domain — biological safety is occupational safety — but they are a separate body of regulation and are kept together for that reason.

---

## Part 1: Governance Drivers

---

### 1.1 Regulations

___

## Create Regulation

### Display Name
EU Directive 2000/54/EC — Biological Agents at Work

### Qualified Name
CocoPharma::Regulation::EUBiologicalAgentsDirective

### Domain Identifier
24

### Summary
The EU directive on protecting workers from risks related to exposure to biological agents at work, classifying agents into four hazard groups and setting the containment measures and health surveillance each requires.

### Description
The directive classifies biological agents into four groups by their capacity to cause human disease, the hazard they present to workers, the likelihood of spread to the community, and whether effective prophylaxis or treatment exists. Group 1 agents are unlikely to cause disease; group 4 agents cause severe disease, spread readily, and have no effective treatment. The classification determines the containment level required, and the containment level determines the physical and procedural controls the work must be conducted under. For Coco Pharmaceuticals the practical significance is in the middle of the range: much research work involves group 2 agents, and the viral vectors used in cell therapy manufacture require classification decisions that are neither obvious nor safely delegated to the people doing the work. The directive requires risk assessment before work begins, a list of workers exposed to group 3 and 4 agents, health surveillance where appropriate, and notification to the competent authority for first use of group 2 and above. National transpositions vary and in several member states go further, so the group works to the strictest applicable standard across its sites.

### Regulation Source
Council Directive 2000/54/EC on the protection of workers from risks related to exposure to biological agents at work, as transposed in each member state

### Regulators
- National labour inspectorates and health and safety authorities in EU member states
- Health and Safety Executive (HSE) — UK, under equivalent domestic provisions

### Implications
- Agents must be classified into hazard groups before work with them begins
- Containment level follows classification and is not a matter of local judgement
- A record of workers exposed to group 3 and 4 agents must be maintained and retained
- First use of group 2 and above requires notification to the competent authority
- National transpositions differ, so the group applies the strictest applicable standard

### Importance
Critical

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

___

## Create Regulation

### Display Name
Contained Use of Genetically Modified Organisms

### Qualified Name
CocoPharma::Regulation::GMOContainedUse

### Domain Identifier
24

### Summary
The regime governing contained use of genetically modified micro-organisms and organisms, requiring activities to be risk-assessed, assigned a containment class, and notified to the competent authority before they begin.

### Description
Contained use is regulated in the EU by Directive 2009/41/EC and in the UK by the Genetically Modified Organisms (Contained Use) Regulations 2014, and the two are close enough in structure to be governed as one regime while differing in notification detail. The regime attaches to the *activity* rather than to a substance: the user assesses the risk of a proposed class of work, assigns it to one of four containment classes, applies the containment and control measures that class requires, and notifies the competent authority — of the premises before first use, and of the activity itself for the higher classes, with class 3 and 4 activities requiring consent before they may proceed. Records of the assessment must be kept and made available on request. For Coco Pharmaceuticals the regime reaches further than the research laboratories where it is expected: autologous cell therapy manufacture involving viral vector modification is contained use, which places a manufacturing activity inside a framework the manufacturing program does not currently reference. Waste from contained use activities must be inactivated before disposal by a validated method, which is a separate requirement from ordinary hazardous waste routing.

### Regulation Source
Directive 2009/41/EC on the contained use of genetically modified micro-organisms, and the Genetically Modified Organisms (Contained Use) Regulations 2014 (UK)

### Regulators
- Health and Safety Executive (HSE) — UK
- National competent authorities in EU member states
- Scientific Advisory Committee on Genetic Modification (SACGM) — UK, advisory

### Implications
- The regime attaches to classes of activity, not to individual substances
- Premises require notification before first use, and higher-class activities require consent before proceeding
- Cell therapy manufacture using viral vectors is contained use, not only research work
- Waste from contained use must be inactivated by a validated method before disposal
- Risk assessment records must be retained and produced on request

### Importance
Critical

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

### 1.2 Threats

___

## Create Threat

### Display Name
Unnotified or Misclassified Contained Use Activity

### Qualified Name
CocoPharma::Threat::UnnotifiedContainedUse

### Domain Identifier
24

### Summary
Work with genetically modified organisms may begin without the notification the regime requires, or under a containment class lower than the risk assessment would support, exposing workers and constituting an offence from the first day.

### Description
This threat differs from most in the health and safety domain in that the harm to the company arrives before any harm to a person. Conducting an unnotified activity, or one notified at the wrong class, is unlawful whether or not anything is released and whether or not anyone is exposed — and it is discovered during an inspection, a grant application, or a regulatory submission that requires the notification reference to be quoted. The routes into it are ordinary rather than negligent. A research project evolves: work notified as class 1 acquires a viral vector step and becomes class 2 without anyone treating the change as a new activity. A process moves from research into manufacture, and the manufacturing site's notifications do not cover it because nobody involved in the transfer knew the regime applied. A collaboration brings in material whose classification was made under another organisation's assessment and is accepted without re-assessment. In each case the work is competently conducted and the paperwork is absent, which is exactly the failure the regime is designed to prevent.

### Implications
- Changes to an existing activity may constitute a new activity requiring fresh notification
- Transfer from research into manufacture must be assessed against the receiving site's notifications
- Classifications made by collaborators must be re-assessed, not inherited
- The offence is complete on commencement, regardless of whether anything is released

### Importance
Critical

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

## Part 2: Governance Policies

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Containment Follows Classification, Not Convenience

### Qualified Name
CocoPharma::GovernancePrinciple::ContainmentFollowsClassification

### Domain Identifier
24

### Summary
The containment level applied to biological work is determined by the assessed classification of the agent and activity, and is never reduced because the available facility is lower or the timeline is pressing.

### Description
Classification is a judgement about hazard and containment is the response to it, and the two must not be reasoned about in the opposite direction — which is the characteristic failure mode, where the facility available determines the classification recorded rather than the other way round. This principle requires the assessment to be made and recorded before any facility question is raised, and requires work that the assessment places above the available containment to be deferred, relocated, or redesigned rather than proceeding under the containment that happens to exist. Classification decisions are made by people competent to make them and are recorded with the reasoning and the evidence relied on, because the reasoning is what an inspector examines and what a subsequent reassessment builds on. The principle applies equally to material received from collaborators and to material moving from research into manufacture, both of which arrive with a classification made by somebody else under an assessment the company has not seen and cannot rely on.

### Implications
- Assessment and classification precede any consideration of which facility is available
- Work above the available containment is deferred, relocated, or redesigned, never downgraded
- Classification reasoning and supporting evidence are recorded, not only the outcome
- Externally supplied classifications are re-assessed rather than inherited

### Outcomes
- Containment matches the hazard rather than the estate
- Classification decisions withstand inspection and support later reassessment
- Pressure to proceed does not silently reduce protection

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
Notification Precedes Work

### Qualified Name
CocoPharma::GovernancePrinciple::NotificationPrecedesWork

### Domain Identifier
24

### Summary
No contained use activity begins before the premises and, where required, the activity itself have been notified to the competent authority and any necessary consent received.

### Description
The regime is one of the few in which the paperwork is the permission rather than the evidence, and the principle states that plainly because the distinction is easily lost in an organisation used to documenting what it has done. A notification is not a record of an activity — it is the thing that makes the activity lawful, and for the higher classes a consent must be received before work may proceed, not applied for in parallel with starting. The principle therefore places notification status as a gate in the project lifecycle rather than as a compliance task running alongside it, with a defined check before work commences and a named person accountable for confirming it. It extends to change: an activity that evolves beyond what was notified requires the notification to be varied first, which means the assessment has to be revisited whenever the work changes in a way that could affect its classification. Because the consequence of getting this wrong is legal rather than physical, and arrives without any incident to prompt it, the principle relies on the check being routine rather than on anyone noticing a problem.

### Implications
- Notification status is a gate before work begins, not a parallel compliance task
- Higher-class activities require consent received, not merely applied for
- Activity changes affecting classification require the notification to be varied first
- A named person confirms notification status before commencement

### Outcomes
- Work is lawful from its first day
- Evolving projects do not drift outside what was notified
- Notification references are available when submissions or grants require them

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
Biological Agents and Activities Must Be Classified Before Work Begins

### Qualified Name
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Domain Identifier
24

### Summary
Every biological agent held and every contained use activity conducted must carry a recorded classification, made by a competent person, with the assessment retained and reviewed on change.

### Description
The obligation establishes the population that everything else in this file works against, in the same way the substance register does for chemical hazards — but it must record two things rather than one, because agents are classified into hazard groups while activities are assigned containment classes, and the class of an activity is not simply the group of the agent it uses. An activity combining a group 2 vector with a laboratory procedure generating aerosols may warrant a higher class than the agent alone would suggest. Classification is made by a competent person rather than by the researcher proposing the work, and the assessment records the agent, the procedure, the containment measures relied on, and the reasoning connecting them. Review is triggered by change to the agent, the procedure, the scale, or the facility, and by new information about the agent's hazard — the last being the trigger most often missed, since it arrives from outside rather than from the project. Records are retained for the period the regime requires, which for work with the higher hazard groups extends decades beyond the end of the activity.

### Implications
- Agents carry hazard group; activities carry containment class; the two are recorded separately
- Classification is made by a competent person, not by the researcher proposing the work
- Review triggers include scale and facility change, and new external information about the agent
- Assessment records are retained well beyond the end of the activity

### Outcomes
- The population of agents and activities requiring control is known
- Containment decisions rest on recorded reasoning that can be examined and revisited
- New hazard information reaches the assessments it affects

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
Contained Use Activities Must Be Notified and Kept Within Their Notification

### Qualified Name
CocoPharma::GovernanceObligation::ContainedUseNotified

### Domain Identifier
24

### Summary
Premises and activities requiring notification must be notified before use, with consent received where required, and any change taking an activity beyond its notification must be varied before the changed work proceeds.

### Description
The obligation makes notification a tracked state rather than a filed document. Each notified activity carries its reference, its class, its scope, the premises it covers, and its current status, and that record is what a project checks against before commencing and what a regulatory submission quotes. Keeping work within scope is the harder half. Activities evolve, and the obligation requires a defined assessment whenever the work changes — a new vector, a different host, an increase in scale, a move between rooms, or a transfer between sites — to establish whether the change remains within the notified scope or requires variation. Transfer from research into manufacture is called out specifically as requiring assessment against the receiving site's notifications, because that transition crosses an organisational boundary where each side may assume the other has dealt with it. Waste from notified activities must be inactivated by a validated method before it enters the ordinary waste route, and the validation evidence is retained as part of the activity record.

### Implications
- Notification reference, class, scope, premises and status are maintained as a live record
- Project commencement checks notification status as a gate
- Changes in vector, host, scale, room or site trigger a scope assessment before proceeding
- Research-to-manufacture transfer is assessed against the receiving site's notifications
- Waste inactivation must be by a validated method, with evidence retained

### Outcomes
- Activities remain lawful as they evolve rather than only at their outset
- Notification references are available when submissions and inspections require them
- Genetically modified material does not enter the ordinary waste stream live

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
Biological Risk Assessment and Containment Assignment

### Qualified Name
CocoPharma::GovernanceApproach::BiologicalRiskAssessment

### Domain Identifier
24

### Summary
Proposed biological work is assessed by a competent committee that classifies the agent and activity, assigns containment, determines notification requirements, and records the reasoning as the basis for later review.

### Description
The approach places classification with a standing committee rather than with individual assessors, because the judgements involved are contestable, benefit from more than one perspective, and need to be made consistently across research and manufacturing where the same vector may be used in both. The committee reviews proposed work before it starts, assigns hazard group and containment class, determines whether notification or consent is required, and specifies the control measures the class demands. Its record is the reasoning as much as the outcome, since a later change is assessed against why the original decision was made rather than merely against what it was. The approach deliberately spans the research-manufacture boundary: a vector assessed for laboratory use is reassessed for manufacturing scale rather than carried across, and the committee is the body that sees both. It also owns the periodic review of existing activities, which is where evolved work is caught, and maintains the relationship with the competent authority so that notifications are handled by people who have done it before rather than by each project in turn.

### Implications
- Classification sits with a standing competent committee, not with individual assessors
- The committee spans research and manufacturing so that scale-up is reassessed rather than inherited
- Reasoning is recorded as the basis for assessing later change
- Periodic review of existing activities is the mechanism that catches evolved work
- The committee owns the competent authority relationship rather than each project

### Outcomes
- Classification is consistent across settings and defensible on inspection
- Work that has evolved beyond its notification is found by review rather than by inspection
- Notifications are made competently and on time

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls

---

### 3.1 Governance Roles

___

## Create Governance Role

### Display Name
Biological Safety Officer

### Qualified Name
CocoPharma::GovernanceRole::BiologicalSafetyOfficer

### Description
The Biological Safety Officer advises on the classification of biological agents and contained use activities, convenes and services the biological risk assessment committee, maintains the register of agents and notified activities, and is the company's point of contact with the competent authority for contained use matters. The role verifies that containment measures assigned to an activity are actually in place before work commences, conducts the periodic review through which evolved activities are identified, and is accountable for the notification status record that projects check against. It works with the Occupational Hygienist where biological and chemical hazards coincide, and with the Manufacturing Governance Lead where cell therapy manufacture brings contained use into a GMP environment.

### Scope
Biological agent and contained use classification, the assessment committee, the register of agents and notified activities, containment verification, and the competent authority relationship.

### Headcount
2

### Category
Governance Role

### Search Keywords
- biological safety
- contained use
- containment level
- GMO notification

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
Contained Use Notification Currency and Containment Verification

### Qualified Name
CocoPharma::GovernanceMetric::ContainedUseNotificationCurrency

### Domain Identifier
24

### Summary
Measures the percentage of active contained use activities operating within a current notification, and the percentage whose assigned containment measures have been verified in place within the review cycle.

### Description
Notification currency is reported as a count of exceptions rather than as a percentage, because the acceptable number is zero and a percentage invites the reading that ninety-six per cent is nearly right. Each activity found operating outside its notification is reported individually with the reason — never notified, evolved beyond scope, premises not covered, or consent not yet received — since those have different causes and different remedies. Containment verification is the second figure and asks whether the measures the classification requires are actually in place, which is a physical check rather than a documentary one: a class assigned on paper and a room operating at a lower standard is the situation the whole regime exists to prevent. Activities that moved from research into manufacture within the reporting period are examined specifically, as that transition is where scope is most often lost. The metric is reported to the Head of Health and Safety and, where cell therapy manufacture is involved, to the Manufacturing Governance Lead as well.

### Implications
- Notification exceptions are reported individually with cause, not as a percentage
- Containment verification is a physical check, not a review of the assessment
- Research-to-manufacture transitions in the period are examined specifically
- Reporting reaches manufacturing where contained use occurs in a GMP environment

### Outcomes
- Activities operating outside their notification are found before an inspection finds them
- Assigned containment is confirmed to exist rather than assumed
- Scope loss at the research-manufacture boundary is detected

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Governance Links

---

### 4.1 Governance Responses

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUBiologicalAgentsDirective

### Policy
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Rationale
The directive's four hazard groups determine containment and surveillance, so classification before work begins is the first control the regime requires.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUBiologicalAgentsDirective

### Policy
CocoPharma::GovernancePrinciple::ContainmentFollowsClassification

### Rationale
Containment measures are prescribed by hazard group. Allowing the available facility to determine the recorded classification inverts the regime.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GMOContainedUse

### Policy
CocoPharma::GovernanceObligation::ContainedUseNotified

### Rationale
Notification of premises before first use, and consent before higher-class activities proceed, is what makes contained use lawful rather than merely documented.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GMOContainedUse

### Policy
CocoPharma::GovernancePrinciple::NotificationPrecedesWork

### Rationale
In this regime the notification is the permission rather than the record, which is the distinction the principle exists to keep visible.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GMOContainedUse

### Policy
CocoPharma::GovernanceApproach::BiologicalRiskAssessment

### Rationale
The regime requires a documented risk assessment assigning the activity to a class, made competently and retained for production on request.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnnotifiedContainedUse

### Policy
CocoPharma::GovernanceObligation::ContainedUseNotified

### Rationale
Tracking notification as a live state with scope, and assessing every change against it, is what catches the evolved activity before an inspection does.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnnotifiedContainedUse

### Policy
CocoPharma::GovernanceApproach::BiologicalRiskAssessment

### Rationale
A committee spanning research and manufacturing is what prevents a vector assessed for the laboratory being carried into manufacture without reassessment.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Rationale
Autologous cell therapy using viral vectors is contained use. The transition brings a regulatory regime into manufacturing that was previously confined to research.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::WorkforceProtectedFromExposure

### Policy
CocoPharma::GovernancePrinciple::ContainmentFollowsClassification

### Rationale
Protection from biological hazard works the same way as protection from chemical hazard: the control is assigned by assessed hazard, not by what the estate happens to provide.

___

---

### 4.2 Governance Mechanisms

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ContainedUseNotified

### Mechanism
CocoPharma::GovernanceMetric::ContainedUseNotificationCurrency

### Rationale
Exceptions reported individually with cause measure the obligation as written, since the acceptable number is zero.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ContainmentFollowsClassification

### Mechanism
CocoPharma::GovernanceMetric::ContainedUseNotificationCurrency

### Rationale
Physical containment verification is what shows whether the assigned class exists in the room or only in the assessment.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::BiologicalRiskAssessment

### Mechanism
CocoPharma::GovernanceMetric::ContainedUseNotificationCurrency

### Rationale
Examining research-to-manufacture transitions in the period tells the committee whether its cross-boundary reassessment is working.

___

---

### 4.3 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Governance Policy 2
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Description
Both establish the population their regime works against, and both fail the same way when registration is treated as a periodic stocktake in a research setting. They are kept separate because agents carry a hazard group and activities carry a containment class, which the chemical register has no equivalent of.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ContainedUseNotified

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingPseudonymisation

### Description
Autologous material is simultaneously a genetically modified organism and personal data about an identified patient. The contained use notification governs the biological hazard while the pseudonymisation approach governs the identity, and both apply to the same vessel at the same time.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ContainedUseNotified

### Governance Policy 2
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Description
Chain of identity keeps the material matched to its patient; contained use keeps the activity within its notified class. A batch moving between rooms or sites engages both, and the movement must satisfy each before it proceeds.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ContainedUseNotified

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Description
A change to a cell therapy process may alter the validated state and the contained use classification at once. Change control must route to the biological assessment committee as well as to the manufacturing assessment, and neither answer alone permits the change.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Governance Policy 2
CocoPharma::GovernanceObligation::HazardousWasteConsignedAndTracked

### Description
Waste from contained use must be inactivated by a validated method before it enters the ordinary hazardous waste route, which makes the classification record a precondition of correct waste routing rather than a parallel concern.

___

---

### 4.4 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::UnnotifiedContainedUse

### Governance Driver 2
CocoPharma::Threat::OccupationalExposureToPotentCompounds

### Description
Both threats are realised through the ancillary and transitional activities that sit around well-controlled core work — scale-up, transfer between sites, maintenance, waste — and in both cases the work itself is competently done while the control that should have accompanied it was never triggered.

___

---

## Part 5: Folio and Library Membership

These definitions join the Head of Health and Safety folio created in `health-and-safety.md`, and the two regulations join the Health and Safety Regulations folder created there.

---

### 5.1 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Regulation::EUBiologicalAgentsDirective

### Membership Rationale
Worker protection from biological agents is an occupational health obligation owned by the Head of Health and Safety.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Regulation::GMOContainedUse

### Membership Rationale
Contained use notification and consent are discharged by the health and safety function through the Biological Safety Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::Threat::UnnotifiedContainedUse

### Membership Rationale
Unlawful or misclassified contained use is a health and safety exposure with legal consequence, owned in this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernancePrinciple::ContainmentFollowsClassification

### Membership Rationale
The rule that containment follows assessed hazard rather than available facility is set by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernancePrinciple::NotificationPrecedesWork

### Membership Rationale
Treating notification as permission rather than record is a health and safety principle enforced as a project gate.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Membership Rationale
Classification of agents and activities is maintained by the Biological Safety Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceObligation::ContainedUseNotified

### Membership Rationale
The notified activity record and its scope assessments are maintained by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceApproach::BiologicalRiskAssessment

### Membership Rationale
The assessment committee spanning research and manufacturing is convened by the Biological Safety Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceRole::BiologicalSafetyOfficer

### Membership Rationale
The delegated role through which biological safety and contained use are managed.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHealthAndSafety

### Element Id
CocoPharma::GovernanceMetric::ContainedUseNotificationCurrency

### Membership Rationale
Notification exceptions and containment verification are reported to the Head of Health and Safety and, where cell therapy is involved, to the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

### 5.2 Corporate Regulation Library Membership

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Health and Safety Regulations

### Element Id
CocoPharma::Regulation::EUBiologicalAgentsDirective

### Membership Rationale
Protection of workers from biological agents is occupational health and safety regulation and belongs with COSHH and the OSH Framework Directive.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Health and Safety Regulations

### Element Id
CocoPharma::Regulation::GMOContainedUse

### Membership Rationale
Contained use is regulated principally for the protection of workers and the environment, and is enforced in the UK by the same authority as the other health and safety regulations.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `health-and-safety.md` | Health and Safety domain program. Creates the folio and the regulation library folder these definitions join, and the substance register this file's classification obligation parallels |
| `manufacturing-governance-program.md` | Personalised manufacturing, chain of identity, and change control — all of which apply to the same autologous material this regime classifies |
| `drug-development-governance.md` | Clinical trial conduct for the therapies whose manufacture constitutes contained use |
| `privacy-governance-program.md` | Autologous material is simultaneously a genetically modified organism and personal data about an identified patient |
