# Coco Pharmaceuticals — Dangerous Goods Transport Governance

> **Author:** Stew Faster (Head of Manufacturing), Florence Paynter, George Pie  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Governance definitions for the transport of dangerous goods, establishing the Distribution domain, identifier `Distribution`. The file registers the domain identifier as a valid metadata value before any definition claims it. Load `health-and-safety.md`, `biological-agents-and-gmo.md`, `manufacturing-governance-program.md` and `serialisation-governance-program.md` first.

---

## Overview

Distribution is established here as a governance domain because moving product and material between sites, to hospitals, and to patients is a regulated activity in its own right, governed by authorities and rulebooks that have nothing to do with medicines law. This file covers the part of it that carries the most immediate legal exposure: dangerous goods transport.

The company moves a considerable amount of material that is dangerous goods in the transport sense, and very little of it looks dangerous to the people handling it. Solvents and reagents move between research sites. Cytotoxic product moves to hospital pharmacies. Diagnostic and clinical trial samples move from investigator sites to laboratories, and are classified as biological substances whether or not anyone involved thinks of them that way. Patient-derived material for personalised manufacture moves in both directions on a clock, and for autologous therapies is simultaneously a genetically modified organism, a person's health data, and a consignment requiring declaration. Lithium batteries in temperature monitoring devices travel with almost all of it.

Three things make this a governance problem rather than a logistics one.

**The shipper carries the liability and cannot delegate it.** Whoever offers goods for transport is responsible for their classification, packing, marking and documentation, whatever the carrier subsequently does. A courier collecting a misdeclared package has committed no offence; the company has.

**Certification expires.** Everyone who classifies, packs, or offers dangerous goods must be trained and recertified on a cycle, and an expired certificate makes every subsequent consignment non-compliant regardless of how correctly it was actually handled. This is a data problem with a hard edge — the training record is the compliance evidence.

**Time pressure falls exactly where the rules are least forgiving.** A personalised therapy with a short viable life, shipped to a waiting patient, is precisely the consignment where an expedited process is most tempting and a refusal at the airport most costly.

The domain identifier is registered here because dangerous goods is the first substantial body of distribution governance. Distribution will grow — good distribution practice, cold chain in transit, and returns and recalls all belong here — and this file is the first part of it rather than the whole of it.

---

## Part 1: Domain Registration

___

## Setup Valid Metadata Value

### Metadata Property Name
domainIdentifier

### Preferred Value
25

### Metadata Display Name
Distribution

### Metadata Description
The governance domain for distribution covers the movement of product, material and samples between the organisation's sites and onward to hospitals, laboratories and patients. It encompasses the regulated aspects of transport — the classification, packing, marking and declaration of dangerous goods, the maintenance of conditions in transit, and the records that evidence both — together with the good distribution practice obligations that attach to medicinal products in the supply chain. The domain exists because transport is governed by authorities and rulebooks distinct from those that regulate how a product is made, and because liability for a consignment rests with the party that offers it for carriage rather than with the party that carries it.

___

---

## Part 2: Governance Drivers — Distribution

---

### 2.1 Regulations

___

## Create Regulation

### Display Name
ADR — European Agreement concerning the International Carriage of Dangerous Goods by Road

### Qualified Name
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Domain Identifier
Distribution

### Summary
The agreement governing carriage of dangerous goods by road across Europe and the UK, setting classification, packaging, labelling, documentation, vehicle and training requirements, and requiring appointment of a Dangerous Goods Safety Adviser.

### Description
ADR governs almost all of the company's ground movements of hazardous material, and is given effect in national law across the contracting parties including the UK. Its structure is a set of classes — flammable liquids, toxic substances, infectious substances, miscellaneous dangerous goods including environmentally hazardous substances and lithium batteries — each with packing requirements, marking and labelling, and documentation that must accompany the consignment. Two provisions shape governance more than the rest. The first is that responsibility attaches to defined roles, with the consignor accountable for classification and declaration whatever arrangements exist with the carrier. The second is the mandatory appointment of a Dangerous Goods Safety Adviser, a qualified individual who must be named, must hold a current vocational certificate, and must produce an annual report on the undertaking's dangerous goods activities — a legal obligation on the company rather than a matter of good practice. ADR provides limited quantity and excepted quantity relaxations that reduce requirements for small amounts, which are valuable for research shipments and are also where misapplication is most common.

### Regulation Source
European Agreement concerning the International Carriage of Dangerous Goods by Road (ADR), as given effect in national legislation

### Regulators
- Department for Transport and Health and Safety Executive — UK
- National transport authorities in ADR contracting parties

### Implications
- The consignor is accountable for classification and declaration, whatever the carrier does
- A Dangerous Goods Safety Adviser must be appointed, certificated, and must report annually
- Every person classifying, packing or offering goods requires training appropriate to their function
- Limited and excepted quantity relaxations are available and are frequently misapplied
- Documentation must accompany the consignment and be retained

### Importance
Critical

### Category
Distribution

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

## Create Regulation

### Display Name
IATA Dangerous Goods Regulations

### Qualified Name
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Domain Identifier
Distribution

### Summary
The rules governing carriage of dangerous goods by air, stricter than the road regime, with mandatory recurrent training, operator variations by airline and state, and a shipper's declaration that binds the company.

### Description
Air transport is where the company's time-critical shipments go and where the rules are least forgiving. The IATA Dangerous Goods Regulations give effect to the ICAO Technical Instructions and add operator and state variations, so a package acceptable to one airline on one route may be refused by another — which means the applicable requirements depend on the routing and cannot be settled once for a lane and forgotten. Quantity limits are lower than by road, some substances acceptable by road are forbidden by air entirely, and packaging must meet specification standards with documented compliance. Training is mandatory and recurrent, and the shipper's declaration is a signed statement binding the company to the accuracy of the classification. For Coco Pharmaceuticals the demanding consignments are clinical samples and patient-derived material, which travel as biological substances under specific provisions, and the lithium batteries in the temperature monitoring devices accompanying almost every temperature-controlled shipment. A refusal at the airport for a consignment with a short viable life is not a delay to be rescheduled; it is a therapy the patient does not receive.

### Regulation Source
IATA Dangerous Goods Regulations, giving effect to the ICAO Technical Instructions for the Safe Transport of Dangerous Goods by Air

### Regulators
- Civil Aviation Authority — UK
- National civil aviation authorities
- Airline operators, through operator variations

### Implications
- Applicable requirements depend on routing, since operator and state variations differ
- Quantity limits are lower than by road and some substances are forbidden by air
- Training is mandatory and recurrent, with certification lapsing on a fixed cycle
- The shipper's declaration is a signed statement binding the company to the classification
- Refusal of a time-critical consignment can mean a patient does not receive treatment

### Importance
Critical

### Category
Distribution

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

### 2.2 Threats

___

## Create Threat

### Display Name
Misdeclared or Undeclared Dangerous Goods Consignment

### Qualified Name
CocoPharma::Threat::MisdeclaredDangerousGoods

### Domain Identifier
Distribution

### Summary
Material may be offered for carriage without declaration, or under a wrong classification, exposing transport workers and emergency responders to a hazard they have not been told about and the company to strict liability.

### Description
Undeclared dangerous goods are usually sent by people who did not know the rules applied. A researcher posts a small quantity of a reagent to a collaborator. A site returns a sample in an ordinary courier envelope. A device with a lithium battery is shipped as an ordinary spare part. In each case somebody helpful moves something quickly and the consignment enters the transport system carrying a hazard nobody downstream can see — which is exactly what the declaration regime exists to prevent, because the driver, the handler, and the firefighter attending a vehicle incident all depend on the paperwork to know what they are dealing with. Misdeclaration is the subtler form and more common in organisations that do have a process: a classification inherited from a previous shipment that is no longer accurate, a limited quantity exemption applied to a consignment that has grown past the threshold, or a road classification used for an air shipment. The consequence is asymmetric. Most misdeclared consignments arrive without incident, which means the practice persists and is reinforced, until one does not.

### Implications
- Undeclared shipments usually originate outside the logistics function, in research and at sites
- Inherited classifications become wrong as consignments and routes change
- Air shipments cannot use road classifications, and the difference is easily missed
- Most misdeclarations arrive safely, which reinforces the practice that produces them

### Importance
Critical

### Category
Distribution

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

## Part 3: Governance Policies — Distribution

---

### 3.1 Governance Principles

___

## Create Governance Principle

### Display Name
The Shipper Owns the Classification

### Qualified Name
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Domain Identifier
Distribution

### Summary
Coco Pharmaceuticals is accountable for the classification, packing and declaration of everything it offers for carriage, and that accountability is not transferred by using a carrier, a freight forwarder, or a site's own arrangements.

### Description
The principle exists because the intuition runs the other way. People assume that a professional courier who accepts a package has taken responsibility for it, and that a freight forwarder who prepares the paperwork has assumed the risk of getting it wrong. Neither is true: the consignor's duties are personal to the consignor, and a carrier that accepts a misdeclared package has been misled rather than made liable. The practical consequence is that the company must be able to stand behind every declaration made in its name, which requires the classification to have been made by someone it trained and can identify, working from information it holds, rather than by a forwarder inferring a classification from a product description. Where a third party does prepare declarations under a contract, the principle requires the company to specify the classification rather than accept one, and to audit the arrangement. The same applies to investigator sites and collaborators shipping material back: they are shipping on the company's behalf, and their arrangements are the company's exposure.

### Implications
- Carrier and forwarder involvement does not transfer consignor liability
- Classifications must be made by identified trained people working from company-held information
- Where a third party prepares declarations, the company specifies the classification and audits
- Investigator sites and collaborators shipping material back are within scope

### Outcomes
- Every declaration made in the company's name can be stood behind
- Third-party arrangements are specified and audited rather than assumed adequate
- Return shipments from sites receive the same control as outbound ones

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

## Create Governance Principle

### Display Name
Time-Critical Shipments Are Planned, Never Expedited

### Qualified Name
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Domain Identifier
Distribution

### Summary
Consignments with a short viable life have their route, classification, packaging and documentation established in advance as a validated lane, so that despatch is execution rather than improvisation.

### Description
The consignments that matter most are the ones with least time to fix a problem, and they are therefore the ones where an ad hoc process fails hardest. A personalised therapy with a viable life measured in days, a patient-derived starting material collected that morning, a clinical sample with a stability window — each is a shipment where a refusal at the airport, a wrong packaging specification, or a missing declaration means the material is lost rather than delayed. The principle requires such movements to be set up as validated lanes ahead of need: the route agreed with the operator, the classification determined, the packaging specified and tested against the conditions, the documentation templated, and the contingency established for what happens when a flight is cancelled. Despatch then executes a known configuration. The alternative — treating each urgent shipment as a special case — puts the classification decision in the hands of whoever is available at the time, under the greatest possible pressure to get it moving, which is the situation in which misdeclaration is most likely and most consequential.

### Implications
- Routes, classification, packaging and documentation are established before the need arises
- Packaging must be tested against the conditions the lane actually presents
- Contingency for cancellation and diversion is part of the lane, not improvised
- Urgency must not put classification decisions in the hands of whoever is available

### Outcomes
- Time-critical material is not lost to avoidable transport refusals
- Classification decisions are made calmly and in advance
- The people despatching under pressure execute rather than decide

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

### 3.2 Governance Obligations

___

## Create Governance Obligation

### Display Name
Consignments Must Be Classified and Declared by a Currently Certificated Person

### Qualified Name
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Domain Identifier
Distribution

### Summary
Every dangerous goods consignment must be classified, packed, marked and declared by a person holding current certification for the mode and function concerned, with the person and their certification recorded against the consignment.

### Description
The obligation ties three records together that are usually kept apart: the consignment, the person who declared it, and that person's certification at the time of the declaration. Keeping them linked is what makes the compliance position knowable — without it, discovering that a certificate lapsed in March means an unbounded question about which consignments were affected, whereas with it the answer is a query. Certification is specific to mode and function: air training does not cover road, and a packer's training does not qualify someone to classify. Recurrent training deadlines are enforced by preventing declaration rather than by reporting the lapse afterwards, on the same reasoning that applies to lapsed qualification in manufacturing — a control that blocks the action prevents the finding, while a report identifies it after the consignment has shipped. Investigator sites and collaborators shipping on the company's behalf are within scope, which in practice means either training them or providing pre-classified return packaging with the declaration already prepared.

### Implications
- Consignment, declaring person, and certification status at that date are recorded together
- Certification is specific to mode and function and does not transfer between them
- Lapsed certification must block declaration, not generate a report afterwards
- Sites and collaborators shipping on the company's behalf require training or pre-classified packaging

### Outcomes
- The compliance status of any past consignment is a query rather than an investigation
- Declarations are made by people qualified for the mode and function concerned
- Return shipments from third parties are controlled rather than hoped for

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

## Create Governance Obligation

### Display Name
Dangerous Goods Records Must Be Retained and Reconcilable

### Qualified Name
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Domain Identifier
Distribution

### Summary
Transport documents, declarations, packing certificates and training records must be retained for the required period and must reconcile against what was actually shipped.

### Description
The records are the only evidence that the regime was followed, and they are examined in three circumstances: routine inspection, investigation after an incident, and the Dangerous Goods Safety Adviser's annual report. Retention periods differ by mode and by jurisdiction, and the obligation sets the period to the longest applicable rather than maintaining several. Reconciliation is the requirement that gives the records their value: the declarations retained must correspond to the consignments actually despatched, and a shipment appearing in the logistics record with no corresponding declaration is either an undeclared dangerous goods movement or a non-dangerous shipment misfiled, and the difference matters. That reconciliation is also how undeclared shipments originating outside the logistics function are discovered, since those leave a trace in courier records and none in the declaration file. Training records are retained alongside, because a declaration is only valid if the person making it was certificated at the time, and demonstrating that years later requires the certification history rather than its current state.

### Implications
- Retention is set to the longest applicable period across modes and jurisdictions
- Declarations must reconcile against despatch records, with discrepancies investigated
- Courier records without matching declarations indicate possible undeclared movements
- Certification history is retained, not only current certification status

### Outcomes
- The company can evidence compliance for any past consignment
- Undeclared shipments originating outside logistics are detected
- The annual adviser's report rests on complete records

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

### 3.3 Governance Approaches

___

## Create Governance Approach

### Display Name
Dangerous Goods Classification and Lane Management

### Qualified Name
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Domain Identifier
Distribution

### Summary
Recurring movements are established as validated lanes carrying an agreed classification, packaging specification, documentation set and contingency, drawn from the substance and biological registers rather than determined per shipment.

### Description
The approach converts a per-shipment decision into a per-lane one wherever the movement recurs, which is most of them. A lane records what is being moved, between where, by which mode and operator, under what classification, in what packaging specification, with what documentation and what contingency — and is reviewed when any of those changes, including when an operator varies its requirements. Classification is drawn from the substance register and the biological agent register rather than being determined afresh by the person despatching, which is what connects this domain to the health and safety registers and prevents the same material carrying different classifications on different lanes. Novel and one-off shipments still require individual classification, and the approach makes that the exception requiring the Dangerous Goods Safety Adviser's involvement rather than the norm. Lanes covering time-critical material are validated against the conditions they actually encounter, including seasonal extremes and the delays that occur when a routing fails, since packaging qualified in a laboratory tells little about a diverted consignment sitting on an apron.

### Implications
- Recurring movements are established as lanes; one-off shipments are the exception requiring adviser involvement
- Classification is drawn from the substance and biological registers, not determined per despatch
- Lanes are reviewed on change of route, mode, operator, material or operator variation
- Time-critical lanes are validated against real conditions including failure scenarios

### Outcomes
- The same material carries the same classification wherever it moves
- Despatch executes a validated configuration rather than making decisions under pressure
- One-off shipments receive expert attention because they are rare

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

## Part 4: Governance Controls — Distribution

---

### 4.1 Governance Roles

___

## Create Governance Role

### Display Name
Dangerous Goods Safety Adviser

### Qualified Name
CocoPharma::GovernanceRole::DangerousGoodsSafetyAdviser

### Description
The Dangerous Goods Safety Adviser is the appointment ADR requires the company to make and hold. The role holds a current vocational certificate, monitors compliance with the dangerous goods regime across the undertaking, advises on classification for novel and one-off consignments, investigates incidents and near misses involving dangerous goods movements, and produces the annual report on the undertaking's dangerous goods activities that the regime requires. It approves new lanes and reviews existing ones, maintains the relationship with operators on variations affecting the company's routes, and owns the training and certification requirements for everyone with a dangerous goods function. It works with the Biological Safety Officer where consignments carry biological agents and with the Occupational Hygienist where they carry hazardous substances, drawing classification from the registers those roles maintain.

### Scope
Dangerous goods compliance across all modes and sites — classification advice, lane approval, training and certification requirements, incident investigation, operator relationships, and the statutory annual report.

### Headcount
1

### Category
Governance Role

### Search Keywords
- dangerous goods
- ADR safety adviser
- consignment classification
- transport compliance

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 4.2 Governance Metrics

___

## Create Governance Metric

### Display Name
Declaration Accuracy and Certification Currency

### Qualified Name
CocoPharma::GovernanceMetric::DeclarationAccuracyAndCertification

### Domain Identifier
Distribution

### Summary
Measures consignments rejected or queried by operators as a proportion of dangerous goods shipments, alongside the percentage of people with a dangerous goods function holding current certification.

### Description
Operator rejections are the closest thing to an external audit the company receives on this, since an airline refusing a package has examined the declaration against the same rules the company was supposed to apply. Rejections are reported by cause — classification, packaging, marking, documentation — and separately for time-critical lanes, where a rejection has a consequence beyond the reshipment cost. The figure is read with care in one direction: a low rejection rate combined with high volume through operators who check lightly is not evidence of accuracy, so periodic internal verification of declarations against the rules supplements it. Certification currency is the second figure and is reported as a forward view, showing who lapses within the next quarter, since the useful action is to schedule recurrent training rather than to record that someone has become unable to declare. Undeclared shipments discovered through reconciliation against courier records are reported individually rather than as a rate, because each is a potential offence and the count of them is small enough to examine.

### Implications
- Rejections are reported by cause and separately for time-critical lanes
- A low rejection rate is not evidence of accuracy where operators check lightly
- Internal verification of declarations supplements the operator signal
- Certification is reported as a forward view of upcoming lapses
- Undeclared shipments found by reconciliation are reported individually

### Outcomes
- Declaration errors are corrected at their cause rather than per consignment
- Recurrent training is scheduled before certification lapses block despatch
- Undeclared movements originating outside logistics receive individual investigation

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

## Part 5: Governance Links

---

### 5.1 Governance Responses

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Policy
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Rationale
ADR attaches duties to defined roles, and the consignor's duties are personal to the consignor whatever arrangements exist with the carrier.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Policy
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Rationale
Training appropriate to function is a requirement of the regime, and the certification is the evidence that the declaration was competently made.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Policy
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Rationale
The adviser's mandatory annual report on the undertaking's dangerous goods activities can only be produced from complete retained records.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Policy
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Rationale
Operator and state variations mean requirements depend on routing, which cannot be resolved under time pressure at the point of despatch.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Policy
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Rationale
Because the applicable rules vary by operator and route, the lane rather than the material is the unit at which air requirements can be settled.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::MisdeclaredDangerousGoods

### Policy
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Rationale
Blocking declaration on lapsed certification, and recording who declared each consignment, converts an unbounded compliance question into a query.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::MisdeclaredDangerousGoods

### Policy
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Rationale
Drawing classification from the substance and biological registers stops the same material carrying different classifications on different routes.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::MisdeclaredDangerousGoods

### Policy
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Rationale
Reconciling declarations against courier records is how undeclared shipments originating outside the logistics function are found at all.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Policy
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Rationale
On-demand personalised manufacture depends on material arriving within its viable life in both directions, which makes validated lanes a capability requirement rather than a compliance one.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::PersonalisedBatchPatientExposure

### Policy
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Rationale
Consignments of patient-derived material carry health data as well as a transport hazard, and the company remains accountable for both when a courier carries them.

___

---

### 5.2 Governance Mechanisms

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Mechanism
CocoPharma::GovernanceMetric::DeclarationAccuracyAndCertification

### Rationale
Forward-looking certification currency prevents the lapse rather than recording it, and rejection causes show whether competent people are still getting it wrong.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Mechanism
CocoPharma::GovernanceMetric::DeclarationAccuracyAndCertification

### Rationale
Rejections reported by cause and by lane tell the approach which validated configurations are wrong.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Mechanism
CocoPharma::GovernanceMetric::DeclarationAccuracyAndCertification

### Rationale
Undeclared shipments found by reconciliation are only visible because the records exist to reconcile against.

___

---

### 5.3 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Governance Policy 2
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Description
The substance register is the source of transport classification as well as of exposure assessment. A substance registered with its hazard classification supplies both, which is what keeps a material's identity consistent between the laboratory that holds it and the lane that moves it.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Governance Policy 2
CocoPharma::GovernanceObligation::BiologicalAgentsClassified

### Description
Clinical samples and patient-derived material are biological substances for transport purposes, and their transport classification follows from the hazard group assigned under the biological regime rather than being determined separately by logistics.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Governance Policy 2
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Description
A personalised consignment must satisfy both at once: the chain of identity keeps it matched to its patient while the validated lane keeps it lawful and viable in transit. A diversion breaks one and threatens the other.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Governance Policy 2
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Description
The same consignment carries a temperature obligation and a dangerous goods obligation, and the monitoring device that discharges the first is itself a lithium battery requiring declaration under the second.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Governance Policy 2
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Description
Dangerous goods certification is a competency requirement attaching to a regulated role, recorded in the HR competency framework alongside GMP and GCP qualifications and subject to the same currency enforcement.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Mechanism
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Rationale
Carriers and forwarders are third parties acting on the company's behalf, and the liability that stays with the company makes their approval and audit a transport control as much as a commercial one.

___

---

### 5.4 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::MisdeclaredDangerousGoods

### Governance Driver 2
CocoPharma::Threat::UnnotifiedContainedUse

### Description
Both are offences completed by movement or commencement rather than by harm, both usually originate with people acting helpfully outside a process they did not know applied, and both are typically discovered by an external party rather than internally.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Governance Driver 2
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Description
The two modes govern the same material to different standards, and a consignment moving by road to an airport is subject to both in sequence. Classification made for one mode does not transfer to the other, and the air limits are the stricter.

___

---

## Part 6: Folio and Library Membership

Distribution is a new domain and this file creates its folio.

---

### 6.1 Folio Definition

___

## Create Folio

### Display Name
Distribution — Governance Folio

### Qualified Name
CocoPharma::Folio::Distribution

### Description
The governance definitions for the Distribution domain, identifier 25. The folio currently covers dangerous goods transport — the ADR and IATA regimes, the misdeclaration threat, the shipper accountability and planned-lane principles, the classification, records and lane management policies, and the Dangerous Goods Safety Adviser appointment the regime requires.

### Purpose
Provides a single view of the definitions governing how material moves between the company's sites and onward to hospitals, laboratories and patients. The folio is expected to grow as good distribution practice, cold chain in transit, and returns and recalls are brought into the domain; dangerous goods is the first part of it because it carries the most immediate legal exposure.

### Category
Governance Folio

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

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::DangerousGoodsSafetyAdviser

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::Distribution

### Description
Assigns the Dangerous Goods Safety Adviser responsibility for the dangerous goods definitions in the Distribution folio. A Distribution domain lead will be appointed as the domain grows beyond dangerous goods.

___

---

### 6.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Membership Rationale
Road transport of dangerous goods is governed in this domain, with the adviser appointment the regime mandates.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Membership Rationale
Air transport carries the company's time-critical consignments and the strictest requirements.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::Threat::MisdeclaredDangerousGoods

### Membership Rationale
Misdeclared and undeclared consignments are a distribution exposure with strict liability.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Membership Rationale
Consignor accountability is the principle the whole domain rests on.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Membership Rationale
Validated lanes for short-life material are set up and maintained in this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Membership Rationale
Declaration competence and its enforcement are owned by the Dangerous Goods Safety Adviser.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Membership Rationale
Transport records supporting the statutory annual report are retained by this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernanceApproach::DangerousGoodsLaneManagement

### Membership Rationale
Lane definition and review are operated by the Dangerous Goods Safety Adviser.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernanceRole::DangerousGoodsSafetyAdviser

### Membership Rationale
The statutory appointment through which the regime is discharged.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::Distribution

### Element Id
CocoPharma::GovernanceMetric::DeclarationAccuracyAndCertification

### Membership Rationale
Rejections, certification currency and undeclared finds are reported to the adviser and to the Head of Manufacturing.

### Membership Status
VALIDATED

___

---

### 6.3 Root Collection Membership

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::Distribution

### Membership Rationale
The Distribution folio is part of the Coco Pharmaceuticals governance folios collection, making the domain discoverable alongside the others.

### Membership Status
VALIDATED

___

---

### 6.4 Corporate Regulation Library

Transport regulation belongs to none of the existing library folders.  It is closest to Health and Safety Regulations, but those govern conditions of work at the company's own premises, while ADR and the IATA regulations govern material once it has left them and bind the company as consignor rather than as employer.

___

## Create Collection Folder

### Display Name
Transport Regulations

### Qualified Name
CollectionFolder::Coco::Transport Regulations

### Purpose
Groups the regulations governing the carriage of the company's material and product by road, air and sea.

### Description
This folder holds regulation whose subject is material in transit — its classification, packaging, marking, documentation and the competence of the people who offer it for carriage.  It is distinct from Health and Safety Regulations, which govern conditions at the company's own premises, and from Pharmaceutical Industry Regulations, which govern how medicinal products are made and verified.  Requirements differ by mode and the same consignment may be subject to several in sequence, so the folder holds parallel instruments governing the same material rather than a single set.

### Category
Regulation Category

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

## Add Member to Collection

### Collection Id
RootCollection::Coco::Corporate Regulation Library

### Element Id
CollectionFolder::Coco::Transport Regulations

### Membership Rationale
Transport regulation is a category of corporate regulatory obligation in its own right, distinct from health and safety and from pharmaceutical manufacturing, and belongs in the library alongside them.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Transport Regulations

### Element Id
CocoPharma::Regulation::ADRDangerousGoodsByRoad

### Membership Rationale
ADR governs the company's road movements of dangerous goods across the UK and Europe and mandates the safety adviser appointment.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Transport Regulations

### Element Id
CocoPharma::Regulation::IATADangerousGoodsRegulations

### Membership Rationale
The IATA regulations govern the company's air consignments, including the time-critical personalised medicine and clinical sample lanes.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `health-and-safety.md` | Substance register supplying transport classification, and the hazardous waste routing that transport feeds |
| `biological-agents-and-gmo.md` | Biological agent classification from which the transport classification of samples and patient material follows |
| `manufacturing-governance-program.md` | Chain of identity and cold chain monitoring, both of which apply to the same personalised consignments |
| `serialisation-governance-program.md` | Serialisation and market destination, which govern the same finished product movements |
| `corporate-governance-program.md` | Approved third-party status covering carriers and freight forwarders |
| `human-resource-management.md` | The competency framework in which dangerous goods certification is recorded and its currency enforced |
