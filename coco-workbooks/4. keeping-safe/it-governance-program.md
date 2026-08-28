# Coco Pharmaceuticals — IT Infrastructure Governance Program

> **Author:** Gary Geeke (IT Infrastructure Director)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Governance definitions for the `IT Infrastructure` domain at Coco Pharmaceuticals, built on the systems inventory created in this directory and structured around the ITIL service management practices Gary Geeke's team already works to. Load the data governance program directory first, then the systems inventory notebooks, then this file.

---

## Overview

The IT infrastructure domain is a serving domain. It owns no regulatory obligation of its own and no business outcome — what it owns is the digital services every other domain runs on, and the consequence is that its governance is almost entirely expressed as commitments to other people's obligations. Manufacturing cannot maintain a validated state on a platform that changes without notice. Privacy cannot enforce a retention schedule on systems nobody has enumerated. Drug development's twenty-five year retention and health and safety's forty-year retention are, in practice, promises about system succession that only this domain can keep.

The program follows the ITIL practices the team already uses, which is deliberate: a governance framework that mirrors how the work is actually organised gets applied, and one that introduces a parallel vocabulary does not. Configuration management, change enablement, service level management and service continuity each carry a governance definition here, expressed in terms of the data they produce rather than the process they describe.

Everything rests on the systems inventory. That inventory was built first — before this program existed — because the security team needed it urgently to scope the ISMS, and it turned out to be the precondition for almost everything else as well. A system that is not in the inventory has no owner, no recovery objective, no change path, and no place in anyone's compliance scope. The inventory is where this domain's contribution to the wider governance program begins, and the notebooks that create and extend it sit alongside this file:

* [creating-system-inventory](creating-system-inventory/creating-system-inventory.ipynb)
* [extending-the-systems-inventory](extending-the-systems-inventory/README.md)

The domain's relationship with two others is close enough to state explicitly. With **SECURITY**, the systems inventory and the ISMS asset inventory are the same enumeration seen from two angles, and they are maintained once. With **DATA**, the systems inventory records where data lives while the catalog records what the data is, and neither is complete without the other.

---

## Part 1: Governance Drivers — IT Infrastructure

As a serving domain, IT infrastructure owns few drivers of its own. One business imperative and one threat are defined here; everything else in this program responds to drivers owned by the domains it serves.

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Digital Services the Business Can Depend On

### Qualified Name
CocoPharma::BusinessImperative::DependableDigitalServices

### Domain Identifier
IT Infrastructure

### Summary
Coco Pharmaceuticals must run digital services whose availability, change behaviour, and recovery characteristics are known and agreed, so that the domains depending on them can make commitments of their own.

### Description
Every regulatory commitment the company makes is, somewhere underneath, a commitment about a system. A batch cannot be released if the electronic batch record system is unavailable; a data subject request cannot be answered in a month if the systems holding the data cannot be searched; expedited safety reporting cannot meet a seven-day deadline through a manual workaround. What the business needs from this domain is not maximal availability everywhere, which is unaffordable, but *known* characteristics — an agreed service level, an understood recovery time, and a change process that does not surprise the people who depend on the service. This imperative is deliberately expressed as dependability rather than uptime, because a service that is reliably available four days a week is more useful to plan around than one that is usually available and occasionally not. The measure of success is that other domains can state their own commitments with confidence, not that this domain reports high availability figures.

### Implications
- Service characteristics must be agreed with the depending domain, not set by IT alone
- Recovery objectives must reflect what the business actually needs, which differs sharply by service
- Change behaviour must be predictable, since unpredictability is itself an availability problem
- Investment must be justified by the obligations it lets other domains discharge

### Outcomes
- Domains can make regulatory and business commitments knowing what they rest on
- Service investment is directed by consequence rather than by uniform standards
- Unplanned change ceases to be a source of compliance failure in other domains

### Importance
High

### Category
IT Infrastructure

### Authors
Gary Geeke

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
Unmanaged and Unrecorded Systems

### Qualified Name
CocoPharma::Threat::UnmanagedSystems

### Domain Identifier
IT Infrastructure

### Summary
Systems may run in the business without appearing in any inventory, leaving them unpatched, unbacked-up, unowned, and outside every compliance scope that depends on knowing what exists.

### Description
Systems arrive outside the managed estate for ordinary reasons: a departmental team buys a cloud service on a card, a laboratory instrument arrives with an embedded controller, a proof of concept becomes load-bearing without ever being handed over, a supplier operates a system on the company's behalf. None of this involves anyone circumventing a control, and each system is doing useful work — which is exactly why the situation persists. The harm is that every downstream governance activity silently under-scopes. Security patches what it knows about. Privacy searches the systems it can enumerate. Data governance catalogues the assets it has been told exist. Recovery planning covers the services on the list. A system absent from the inventory is therefore absent from all of them simultaneously, and its absence is discovered during an incident, a data subject request, or an inspection — the three moments when discovery is most expensive. The threat grows with every acquisition and with every shift towards services procured directly by business teams.

### Implications
- Discovery must be active, since systems arriving outside the process will not announce themselves
- Business-procured cloud services and embedded instrument controllers are in scope, not exceptions
- Supplier-operated systems handling company data belong in the inventory
- Absence from the inventory removes a system from every compliance scope at once

### Importance
High

### Category
IT Infrastructure

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — IT Infrastructure

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Every System Has a Named Owner and a Recorded Purpose

### Qualified Name
CocoPharma::GovernancePrinciple::SystemsHaveOwnerAndPurpose

### Domain Identifier
IT Infrastructure

### Summary
No system runs in the business without a named owner accountable for it and a recorded statement of what it is for, what data it holds, and which domains depend on it.

### Description
Ownership is what makes every other control addressable. Without it there is nobody to ask whether a system can be patched, nobody to approve a change, nobody to consult before decommissioning, and nobody accountable when it fails — and the practical consequence is that the question goes to the infrastructure team, who can answer how the system runs but not whether the business still needs it. The principle requires ownership to sit with the business function relying on the service rather than with the team operating it, and requires the record to state purpose, data holdings, and dependent domains so that the consequences of any decision about the system can be traced before it is taken. Systems inherited through acquisition, operated by suppliers, or embedded in laboratory and production equipment are explicitly in scope; these are the categories most often treated as somebody else's problem, and they are disproportionately represented in incidents. Where an owner cannot be identified, that is a finding requiring resolution rather than a gap to be recorded and tolerated.

### Implications
- Ownership sits with the depending business function, not the operating team
- The record must state purpose, data holdings, and dependent domains
- Supplier-operated, acquired, and embedded systems are in scope
- An unidentifiable owner is a finding to resolve, not a gap to record

### Outcomes
- Every system has someone who can answer for it
- Decisions about a system can be assessed for consequence before being taken
- Decommissioning proceeds without discovering dependencies afterwards

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Change Reaches Production by One Path

### Qualified Name
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Domain Identifier
IT Infrastructure

### Summary
All change to production systems follows one recorded path, whatever its size or urgency, so that what is running can always be explained by what was approved.

### Description
Parallel change routes are how validated states are lost and how incidents become unexplainable. When emergency fixes, vendor patches, configuration tweaks and formal releases each reach production differently, the running configuration diverges from any record of it, and the divergence is discovered when a change fails to behave as tested or when an inspector asks why the system differs from its validated specification. This principle requires one path with variations in depth rather than variations in route — an emergency change is assessed and approved faster and with fewer people, but it is assessed, approved, and recorded, and it is reviewed afterwards. The requirement bears hardest on the systems where it matters most: those supporting GMP and GCP activities, where an unrecorded change can invalidate the validated state and, with it, the records the system produced since. Vendor-initiated changes to cloud services are the hardest case, since the company does not control their timing, and the principle requires those to be tracked and assessed rather than accepted as weather.

### Implications
- Emergency changes vary in depth and speed, never in route, and are reviewed afterwards
- Vendor-initiated cloud changes must be tracked and assessed, not treated as unavoidable
- Changes to GMP and GCP systems must route to validated-state assessment
- The running configuration must be reconcilable to the approved record

### Outcomes
- What is running in production can be explained from records
- Validated states survive routine operational change
- Incident investigation starts from a known configuration

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Services Are Built for the Recovery the Business Actually Needs

### Qualified Name
CocoPharma::GovernancePrinciple::DesignedForRequiredRecovery

### Domain Identifier
IT Infrastructure

### Summary
Recovery time and recovery point objectives are set by the domain depending on the service, tested against those objectives, and reflected in how the service is built rather than asserted in a plan.

### Description
Recovery objectives set by the infrastructure team are guesses about business consequence; set by the depending domain they are statements of requirement, and the difference shows up during an incident. This principle places the objective with the domain that bears the loss — manufacturing states what an electronic batch record system outage costs in hours, privacy states how long a subject request system can be down before deadlines are missed — and makes the infrastructure team accountable for building to that objective and demonstrating it. Demonstration is the part most often skipped: a documented four-hour recovery time that has never been exercised is an aspiration, and the failure modes that matter tend to appear only in a real restore. The principle therefore requires periodic testing against the stated objective, with the result reported to the depending domain rather than held within IT, so that a domain relying on a four-hour recovery learns promptly if the tested time is eleven. Where the tested capability falls short and cannot economically be improved, the objective is renegotiated openly rather than left standing as fiction.

### Implications
- Recovery objectives are set by the depending domain, not by the infrastructure team
- Objectives must be tested by exercise, not asserted in a continuity document
- Test results are reported to the depending domain, not retained within IT
- An unachievable objective is renegotiated openly rather than left in place

### Outcomes
- Business continuity planning rests on demonstrated rather than documented capability
- Domains know what their obligations actually rest on
- Investment in resilience is directed by stated business consequence

### Authors
Gary Geeke

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
Systems Must Be Recorded in the Systems Inventory Before Reaching Production

### Qualified Name
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Domain Identifier
IT Infrastructure

### Summary
Every system holding company data or supporting a business process must be recorded in the systems inventory with its owner, purpose, data holdings, service level, and recovery objective before it enters production use.

### Description
The inventory is the join point between this domain and every other, which is why registration is required before production use rather than as a subsequent tidying exercise. The record carries what other domains need in order to include the system in their own scope: the owner for accountability, the data holdings for privacy and security classification, the dependent domains for change impact, and the service and recovery objectives for continuity planning. Registration alone is insufficient, because systems arrive outside the process by construction, so the obligation pairs it with active discovery — network and cloud account scanning, procurement feeds, and reconciliation against supplier contracts — and treats the gap between discovered and registered as the operative measure. Decommissioning is equally in scope and more often neglected: a system removed from service but left in the inventory distorts every scope built from it, while one removed from the inventory without its data being dealt with destroys records other domains are obliged to retain.

### Implications
- Registration precedes production use, not follows it
- The record must carry owner, purpose, data holdings, dependent domains, service level, and recovery objective
- Active discovery must run alongside registration, since some systems will never be registered voluntarily
- Decommissioning must update the inventory and resolve retained data before removal

### Outcomes
- Security, privacy, and data governance scopes are built on a complete enumeration
- The extent of the unmanaged estate is measured rather than assumed
- Decommissioning does not destroy records other domains must retain

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Changes Must Be Assessed for Impact and Recorded Before Deployment

### Qualified Name
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Domain Identifier
IT Infrastructure

### Summary
Every change to a production system must be assessed for its impact on dependent domains, approved at a level proportionate to that impact, and recorded so that the running configuration can be reconciled to what was approved.

### Description
Impact assessment is what turns a change record from an audit artefact into a control. The assessment asks which domains depend on the system, whether the change affects a validated state, whether it alters what data is held or where it flows, and whether it changes the service or recovery characteristics anyone is relying on — and it routes the change to those domains where the answer is yes. This is the mechanism by which a manufacturing validated state, a privacy transfer safeguard, or a drug development retention arrangement is protected from an infrastructure change made in good faith by someone unaware of the dependency. Approval depth follows assessed impact rather than change size, since a one-line configuration change to an authentication service can be far more consequential than a large release to a reporting system. Records must be sufficient to reconstruct the configuration at any past point, because incident investigation and inspection both ask what was running at a specific time rather than what is running now.

### Implications
- Assessment must identify dependent domains and route the change to them
- Approval depth follows assessed impact, not the size of the change
- Changes affecting validated systems must route to validated-state assessment
- Records must support reconstruction of past configuration, not only current state

### Outcomes
- Dependent domains learn of changes that affect their obligations before deployment
- Validated states and compliance arrangements survive routine infrastructure work
- Incident and inspection questions about past configuration are answerable

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Service Levels and Recovery Objectives Must Be Agreed and Tested

### Qualified Name
CocoPharma::GovernanceObligation::ServiceLevelsAgreedAndTested

### Domain Identifier
IT Infrastructure

### Summary
Each service must carry a service level and recovery objectives agreed with the domains depending on it, tested on a defined cycle, with results reported back to those domains.

### Description
The obligation makes the agreement bilateral and the demonstration mandatory. Agreement means the depending domain states what it needs and why — usually by reference to an obligation of its own, such as a regulatory deadline or a batch release window — and the infrastructure team states what it can deliver, with any gap resolved explicitly rather than left to be discovered. Testing is required on a cycle proportionate to consequence, and a test means an exercise producing a measured result, not a review of a document. Reporting results back to the depending domain is what keeps the arrangement honest: a domain planning around a four-hour recovery is entitled to know that the last exercise took eleven, and to decide what to do about it. Objectives must be revisited when the service changes materially or when the depending domain's obligations change, since a recovery objective set against a superseded regulatory deadline protects nothing.

### Implications
- Objectives are agreed bilaterally, with any gap resolved explicitly at the point of agreement
- Testing means a measured exercise, not a document review
- Results are reported to the depending domain whether favourable or not
- Objectives are revisited on material service change and on change to the depending obligation

### Outcomes
- Business commitments rest on demonstrated infrastructure capability
- Shortfalls are known by the people who would be affected by them
- Resilience investment is justified by specific obligations rather than by general prudence

### Authors
Gary Geeke

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
ITIL Service Management Adoption

### Qualified Name
CocoPharma::GovernanceApproach::ITILServiceManagementAdoption

### Domain Identifier
IT Infrastructure

### Summary
IT governance is expressed through the ITIL practices the team already operates — configuration management, change enablement, service level management, incident and problem management, and service continuity — rather than through a parallel governance vocabulary.

### Description
The approach is a deliberate choice to govern through the operating model rather than alongside it. Each ITIL practice already produces records, and those records are what the governance definitions in this program depend on: configuration management produces the inventory, change enablement produces the change record, service level management produces the agreed objectives, and incident and problem management produce the evidence that they are being met. Introducing a separate governance process would mean maintaining a second set of records that diverges from the first, and the divergence would be discovered at audit. What the governance program adds to ITIL is direction: ITIL describes how to run the practices well but is silent on whose requirements should set the objectives, and this program answers that by placing service levels, recovery objectives, and change impact judgements with the domains that bear the consequences. The approach is adopted pragmatically rather than to the letter — practices are implemented where they earn their cost, and the decision not to implement one is recorded with its reasoning.

### Implications
- Governance records are the operational records, not a parallel set
- Objectives and impact judgements come from depending domains, which ITIL does not specify
- Practices are adopted where they earn their cost, with omissions recorded and reasoned
- Practice records must be retained to the standard the depending domains require

### Outcomes
- Governance evidence is produced by doing the work rather than by documenting it separately
- The framework is applied because it matches how the team already operates
- Depending domains have a defined route into IT decisions that affect them

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Systems Inventory and Configuration Management

### Qualified Name
CocoPharma::GovernanceApproach::SystemsInventoryManagement

### Domain Identifier
IT Infrastructure

### Summary
The systems inventory is maintained as a single authoritative record of what runs in the business, populated from procurement, deployment, and active discovery, and consumed by the security, privacy, and data governance programs rather than duplicated by them.

### Description
The inventory was built first because the security team needed it to scope the ISMS, and the approach preserves that as its operating principle: the inventory exists to be consumed by other domains, so its structure is driven by what they need from it rather than by what is convenient to record. Population comes from three routes, because no single one is sufficient — procurement catches what is bought, deployment catches what is built, and active discovery catches what arrived through neither. Reconciliation between the three is where unmanaged systems surface. The inventory records the system and its characteristics; it deliberately does not record what the data inside it *means*, which is the data catalog's role, and the two are linked rather than merged so that neither team is maintaining the other's content. The same discipline applies to the ISMS asset register: it is a view over the inventory with security-specific attributes, not a separate enumeration, which is what prevents the two diverging and the divergence being discovered during a certification audit.

### Implications
- Structure is driven by what consuming domains need, not by operational convenience
- Population runs from procurement, deployment, and active discovery, with reconciliation between them
- The inventory records systems; the data catalog records meaning; the two are linked, not merged
- The ISMS asset register is a view over the inventory rather than a separate enumeration

### Outcomes
- Security, privacy, and data governance work from one enumeration of the estate
- Unmanaged systems surface through reconciliation rather than through incidents
- Two teams stop maintaining overlapping inventories that drift apart

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — IT Infrastructure

---

### 3.1 Governance Roles

The IT Infrastructure Lead role (`CocoPharma::GovernanceRole::ITInfrastructureLead`, held by Gary Geeke) is defined in `joint-governance-officer-definitions.md`. The role below is the delegated position through which service accountability reaches individual systems.

___

## Create Governance Role

### Display Name
Service Owner

### Qualified Name
CocoPharma::GovernanceRole::ServiceOwner

### Description
The Service Owner is accountable for a named service through its life: agreeing its service level and recovery objectives with the domains depending on it, approving changes that affect it, maintaining its systems inventory record, and deciding when it is retired. The role sits with the business function relying on the service rather than with the team operating it, which is what makes the accountability meaningful — a Service Owner can say whether the business still needs a capability, and the operating team cannot. Service Owners are the counterparties for change impact assessment and receive the recovery test results for their services. One person may own several services.

### Scope
One named service — its inventory record, agreed service level and recovery objectives, change approval, and retirement decision.

### Headcount
24

### Category
Governance Role

### Search Keywords
- service ownership
- service level
- change approval
- systems inventory

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
Systems Inventory Completeness

### Qualified Name
CocoPharma::GovernanceMetric::SystemsInventoryCompleteness

### Domain Identifier
IT Infrastructure

### Summary
Measures the percentage of discovered systems that are registered in the inventory with an owner, purpose, data holdings, and recovery objective recorded.

### Description
Registration alone is a weak measure, so completeness is assessed against the fields other domains actually consume: a system registered with no owner and no data holdings appears in the inventory while contributing nothing to security scoping, privacy search, or continuity planning. The metric therefore reports registration and field completeness separately. Discovered-but-unregistered systems are reported as their own figure and broken down by how they were found — procurement reconciliation, network discovery, cloud account scanning, supplier contract review — because each route points at a different gap in the process that let the system arrive unrecorded. As with catalog coverage in the data programme, the figure worsens when discovery is extended to a new area before it improves, so the scanned scope is reported alongside and an expansion is not read as deterioration. Systems supporting GMP, GCP, or personal data processing are reported separately, since an unregistered system in those categories carries regulatory consequence rather than operational untidiness.

### Implications
- Registration and field completeness are reported separately
- Unregistered discoveries are broken down by discovery route to locate the process gap
- Scanned scope must be reported alongside, so expansion is not mistaken for decline
- Regulated-system categories are reported distinctly from the general estate

### Outcomes
- Security, privacy, and data governance can see how complete their scope actually is
- The process gaps letting systems arrive unrecorded are identified and closed
- Unregistered regulated systems surface as the compliance exposure they are

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Change Success and Emergency Change Rate

### Qualified Name
CocoPharma::GovernanceMetric::ChangeSuccessRate

### Domain Identifier
IT Infrastructure

### Summary
Measures the percentage of changes completing without rollback or incident, reported alongside the proportion of changes made under emergency provisions.

### Description
The two figures must be read together, since either alone can be improved by making the other worse. A high success rate achieved by routing difficult changes through the emergency path — where assessment is lighter and scrutiny lower — is not an improvement, and a low emergency rate achieved by declaring genuine emergencies as routine simply moves the risk out of view. Reporting them as a pair makes that trade visible. Emergency changes are additionally tracked for post-implementation review completion, because the emergency path is only acceptable if the assessment that was compressed is subsequently done. Changes affecting validated GMP or GCP systems are reported separately and held to a higher standard, since a failed change there can invalidate records rather than merely requiring a rollback. Failed changes are analysed by cause, and a recurring cause is treated as a problem in the change process rather than as a series of unrelated incidents.

### Implications
- Success rate and emergency rate must be reported as a pair, never separately
- Emergency changes require post-implementation review, tracked to completion
- Changes to validated systems are reported separately and held to a higher standard
- Recurring failure causes indicate a process problem, not a run of bad luck

### Outcomes
- The trade between change speed and change safety is visible rather than hidden
- The emergency path is used for emergencies rather than for convenience
- Systematic weaknesses in change practice are identified and corrected

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Recovery Objective Test Coverage and Achievement

### Qualified Name
CocoPharma::GovernanceMetric::RecoveryTestCoverage

### Domain Identifier
IT Infrastructure

### Summary
Measures the percentage of services with a recovery objective that have been exercised within their test cycle, and the proportion of those exercises that met the agreed objective.

### Description
Coverage and achievement are separate questions and both matter. Coverage asks whether the exercise happened; achievement asks whether the tested recovery met what the depending domain was promised. A service with high coverage and poor achievement is honestly reported and correctable; one with poor coverage is a service whose stated objective is unverified, and unverified objectives are the ones that fail during an actual incident. Reporting is per service and goes to the Service Owner and the depending domain rather than only to the infrastructure team, which is the arrangement that makes a shortfall actionable by the people it affects. Services supporting regulatory deadlines — batch release, safety reporting, data subject requests — are reported separately because a recovery shortfall there converts directly into a missed statutory obligation. Where achievement falls persistently short and the gap cannot be closed economically, the metric is the evidence for renegotiating the objective rather than continuing to report failure against a target nobody can meet.

### Implications
- Coverage and achievement are distinct measures and both are required
- Results go to the Service Owner and the depending domain, not only to IT
- Services supporting regulatory deadlines are reported separately
- Persistent shortfall is evidence for renegotiating the objective, not for repeated failure reporting

### Outcomes
- Stated recovery objectives are verified rather than assumed
- Depending domains learn of shortfalls before an incident reveals them
- Objectives converge on what can actually be delivered

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: Governance Links

---

### 4.1 Governance Responses — Systemic IT Drivers

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnmanagedSystems

### Policy
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Rationale
Registration before production use plus active discovery is the only control that reaches systems arriving outside the process, which is how this threat materialises.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnmanagedSystems

### Policy
CocoPharma::GovernancePrinciple::SystemsHaveOwnerAndPurpose

### Rationale
An unowned system is an unmanaged one. Requiring a named owner in the depending business function is what makes every subsequent control addressable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::DependableDigitalServices

### Policy
CocoPharma::GovernanceObligation::ServiceLevelsAgreedAndTested

### Rationale
Dependability means known and demonstrated characteristics, which is what bilateral agreement and measured exercise produce.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::DependableDigitalServices

### Policy
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Rationale
Unpredictable change is an availability problem in its own right, so a single recorded change path is part of what dependability means.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::DependableDigitalServices

### Policy
CocoPharma::GovernanceApproach::ITILServiceManagementAdoption

### Rationale
Governing through the practices the team already operates is what makes the commitments deliverable rather than aspirational.

___

---

### 4.2 Service Responses — Drivers Owned by Other Domains

These links are the substance of a serving domain's programme. Each records an IT policy answering a driver owned by security, manufacturing, privacy, drug development, or corporate governance.

___

## Link Governance Response

### Driver
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Policy
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Rationale
Security cannot patch, monitor, or scope an estate it cannot enumerate. The inventory is the precondition for every technical security control, which is why it was built before this programme existed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Policy
CocoPharma::GovernancePrinciple::DesignedForRequiredRecovery

### Rationale
Ransomware recovery is a restore exercise under pressure. Tested recovery objectives are what determine whether the business recovers in hours or weeks.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Rationale
An unrecorded infrastructure change to a GMP system can invalidate its validated state and the records it has produced since. A single assessed path is what protects it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUGMPAnnex11

### Policy
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Rationale
Annex 11 requires computerised systems to be validated and changes controlled. Impact assessment routing to validated-state review is how infrastructure work stays within that requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Rationale
Answering a data subject request within a month requires knowing which systems could hold the person's data. Systems absent from the inventory are absent from the search.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernancePrinciple::SystemsHaveOwnerAndPurpose

### Rationale
Recording data holdings against each system is what lets privacy establish where personal data lives and who is accountable for it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Policy
CocoPharma::GovernancePrinciple::DesignedForRequiredRecovery

### Rationale
Twenty-five year retention is a promise about system succession. Recovery and migration capability is what makes archived trial data retrievable decades after the originating system is gone.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::SarbanesOxleySection404

### Policy
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Rationale
Section 404 scope extends to the general IT controls that financial systems depend on — access provisioning, change management, and backup — which are governed here rather than by the finance function.

___

---

### 4.3 Governance Mechanisms — IT Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Mechanism
CocoPharma::GovernanceMetric::SystemsInventoryCompleteness

### Rationale
Registration and field completeness against discovery measures the obligation as written, and the discovery-route breakdown locates the process gap.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::SystemsInventoryManagement

### Mechanism
CocoPharma::GovernanceMetric::SystemsInventoryCompleteness

### Rationale
The reconciliation between procurement, deployment, and discovery is what the unregistered figure exposes.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Mechanism
CocoPharma::GovernanceMetric::ChangeSuccessRate

### Rationale
Success and emergency rates read as a pair test whether assessment is being done or bypassed.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Mechanism
CocoPharma::GovernanceMetric::ChangeSuccessRate

### Rationale
A rising emergency rate is the principle failing in practice, whatever the change policy says.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ServiceLevelsAgreedAndTested

### Mechanism
CocoPharma::GovernanceMetric::RecoveryTestCoverage

### Rationale
Coverage and achievement together measure whether objectives are exercised and whether they hold.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DesignedForRequiredRecovery

### Mechanism
CocoPharma::GovernanceMetric::RecoveryTestCoverage

### Rationale
Achievement against the agreed objective is the evidence that the service was built for the recovery the business asked for.

___

---

### 4.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::InformationAssetsInventoriedAndClassifiedForISMS

### Description
These are one enumeration seen from two angles. The ISMS asset register is maintained as a view over the systems inventory with security-specific attributes, rather than as a second inventory that would drift from the first and be found to have drifted during a certification audit.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Description
The systems inventory records where data lives; the data catalog records what it means. Neither is complete alone, and they are linked rather than merged so that neither team maintains the other's content.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Governance Policy 2
CocoPharma::GovernanceApproach::ManufacturingChangeControl

### Description
Manufacturing change control and IT change enablement govern the same change when it touches a GMP system. The two must reach one decision, and the impact assessment is where an infrastructure change is routed into manufacturing's process.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::SystemsHaveOwnerAndPurpose

### Governance Policy 2
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Description
The organisation-wide ownership obligation is discharged for infrastructure through the inventory record, which is where the system's owner is named and from which ownership gaps are reported.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ServiceLevelsAgreedAndTested

### Governance Policy 2
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Description
A forty-year retention obligation is a succession commitment about systems that will be replaced several times within the period. Migration and retrieval capability is what makes the retention real rather than nominal.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Governance Policy 2
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Description
General IT controls fall within the Section 404 assessment population, so the change records produced here are tested as part of the corporate controls cycle rather than separately.

___

---

### 4.5 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::UnmanagedSystems

### Governance Driver 2
CocoPharma::Threat::UncontrolledDataProliferation

### Description
The two threats are the same phenomenon observed from different domains: a system nobody registered almost always holds data nobody catalogued. Discovery scanning for one finds the other, which is why the systems inventory and the data catalog share their discovery reconciliation rather than running it twice.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::UnmanagedSystems

### Governance Driver 2
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Description
An unmanaged system is unpatched and unmonitored by construction, so it is the most likely entry point for the cyber threat the board is concerned with. This is why the security team needed the inventory before the IT governance programme itself existed.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::DependableDigitalServices

### Governance Driver 2
CocoPharma::BusinessImperative::TrustedDataFoundation

### Description
Both are serving-domain imperatives expressed as obligations to other domains rather than as outcomes of their own, and both are measured by whether the domains they serve can meet commitments more easily.

___

---


## Part 5: IT Infrastructure Governance Folio

The IT Infrastructure Lead had no folio in the joint governance officer definitions, so this file creates one and registers it in the root collection alongside the others.

---

### 5.1 Folio Definition

___

## Create Folio

### Display Name
IT Infrastructure Lead — Governance Folio

### Qualified Name
CocoPharma::Folio::ITInfrastructureLead

### Description
The governance definitions owned by the IT Infrastructure Lead (Gary Geeke) in the `IT Infrastructure` domain. The folio covers the dependable services imperative, the unmanaged systems threat, the ownership, change path and recovery principles, the inventory, change assessment and service level obligations, the ITIL and inventory management approaches, and the controls that measure them.

### Purpose
Provides Gary Geeke with a single view of the definitions through which the infrastructure domain serves the rest of the governance programme. Most of the folio's content exists to let another domain meet an obligation that is theirs, and the folio is where that service relationship is made visible as a set rather than scattered across other people's programmes.

### Category
Governance Folio

### Authors
Gary Geeke

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::ITInfrastructureLead

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::ITInfrastructureLead

### Description
Assigns the IT Infrastructure Lead role responsibility for the governance definitions collected in this folio.

___

---

### 5.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::BusinessImperative::DependableDigitalServices

### Membership Rationale
Dependable service characteristics are what the rest of the organisation relies on this domain to provide.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::Threat::UnmanagedSystems

### Membership Rationale
Systems running outside the managed estate are an infrastructure exposure that removes them from every other domain's scope simultaneously.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernancePrinciple::SystemsHaveOwnerAndPurpose

### Membership Rationale
Ownership and purpose recording is the foundation on which every other infrastructure control depends.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernancePrinciple::SingleChangePathToProduction

### Membership Rationale
The single change path is owned by the IT Infrastructure Lead and protects validated states in other domains.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernancePrinciple::DesignedForRequiredRecovery

### Membership Rationale
Building services to the recovery objectives depending domains state is an infrastructure commitment.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceObligation::SystemsRecordedInInventory

### Membership Rationale
The systems inventory is the domain's principal contribution to the wider governance programme.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceObligation::ChangesAssessedAndRecorded

### Membership Rationale
Change impact assessment and recording is operated by the infrastructure team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceObligation::ServiceLevelsAgreedAndTested

### Membership Rationale
Service level and recovery objective agreement and testing is an infrastructure obligation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceApproach::ITILServiceManagementAdoption

### Membership Rationale
The ITIL operating model through which this programme is delivered is owned here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceApproach::SystemsInventoryManagement

### Membership Rationale
Inventory population, reconciliation, and its relationship to the ISMS register and data catalog are managed by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceRole::ServiceOwner

### Membership Rationale
The delegated role through which service accountability reaches individual systems.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceMetric::SystemsInventoryCompleteness

### Membership Rationale
Inventory completeness is reported to the IT Infrastructure Lead, the CISO, and the CDO.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceMetric::ChangeSuccessRate

### Membership Rationale
Change success and emergency rates are reported to the IT Infrastructure Lead and to Service Owners.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ITInfrastructureLead

### Element Id
CocoPharma::GovernanceMetric::RecoveryTestCoverage

### Membership Rationale
Recovery coverage and achievement are reported to Service Owners and the domains depending on each service.

### Membership Status
VALIDATED

___

---

### 5.3 Root Collection Membership

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::ITInfrastructureLead

### Membership Rationale
The IT Infrastructure Lead folio is part of the Coco Pharmaceuticals governance folios collection, making the infrastructure domain discoverable alongside the others.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| [creating-system-inventory](creating-system-inventory/creating-system-inventory.ipynb) | Builds the initial systems inventory this programme rests on |
| [extending-the-systems-inventory](extending-the-systems-inventory/README.md) | Extends the inventory with the detail the security and data teams need |
| [martyns-law](martyns-law/README.md) | Physical security scenario in this directory, loaded after this file |
| `0. data-governance-program/data-security-strategy.md` | SECURITY-domain program. The ISMS asset register is maintained as a view over the systems inventory |
| `0. data-governance-program/data-governance-program.md` | DATA-domain program. The catalog records what data means; the inventory records where it lives |
| `0. data-governance-program/manufacturing-governance-program.md` | Manufacturing change control, which IT change assessment must route into for GMP systems |
| `0. data-governance-program/joint-governance-officer-definitions.md` | Defines the IT Infrastructure Lead role this folio is assigned to |
