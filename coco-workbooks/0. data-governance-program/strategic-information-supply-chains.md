# Coco Pharmaceuticals Strategic Information Supply Chains

> **Author:** Jules Keeper (Chief Data Officer) with Erin Overview (Information Architect)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-30  
> **Description:** The register of information supply chains that Coco Pharmaceuticals considers strategic — the flows of data whose failure would stop the business, breach a regulation, or harm a patient — together with the governance definitions that govern each of them.

---

## Overview

The Data Strategy Framework names **Optimized Information Supply Chains** as one of its seven building blocks: the flow of data between systems, understood, optimized and managed so that any failure is quickly detected, located and resolved without affecting the service offered.  That component describes an ambition.  This file makes it concrete by naming the flows.

An [information supply chain](https://egeria-project.org/concepts/information-supply-chain/) is a high-level depiction of how data and control move through the digital landscape.  It sits above lineage rather than replacing it: the chain is described at a level a business owner or a regulator can follow, and is then connected to the components that actually execute the flow, so that activity, errors and volumetrics roll up from the real systems into a view somebody can be held accountable for.

Coco Pharmaceuticals runs many hundreds of data flows.  Only a small number of them are worth governing at this level, and the point of the register is to say which.

---

## What makes a supply chain strategic

Erin Overview proposed four tests, and a flow qualifies if it meets any one of them.  Each of the entries below records which tests it met in its `Purposes`.

| Test | The question it answers |
|---|---|
| **Business continuity** | If this flow stopped for a day, would the company stop making, selling or shipping something? |
| **Regulatory exposure** | Does a regulator have a statutory expectation of this data arriving somewhere, correct and on time? |
| **Patient safety** | Could a fault in this flow reach a patient? |
| **Irreversibility** | Once wrong data has travelled this flow, can the damage be undone? |

The fourth test is the one Jules argued hardest for.  Most data quality problems are recoverable — a report is reissued, a figure restated.  A serial number issued twice, a decommissioned pack, or a patient-derived material that has lost its identity are not.  Flows with that property need monitoring *before* the fault propagates, not reporting afterwards, and that is a different engineering problem.

---

## Adopted and new supply chains

Seven of the sixteen entries in the register already exist in Egeria.  They arrive with `CocoComboArchive.omarchive`, which is loaded when the metadata server starts, and are already wired to the solution components that produce their lineage.  This file **adopts** those seven rather than recreating them: it adds them to the register and links them to the governance definitions that govern them, leaving their descriptions and their component wiring untouched.

The other nine are created here.  They are flows the governance programs described in this directory clearly depend on, but which nothing had yet named as a supply chain.

Both kinds follow the archive's naming convention, `InformationSupplyChain::<display name>`, so that the register reads as one set.

---

## Load order

This file links to governance definitions owned by every domain in the directory, so it loads **after** all of them — that is, after `data-governance-program.md`.  It has no forward references: the sustainability program links its own definitions to the Sustainability Reporting supply chain when `3. sustainability/sustainability-governance-program.md` loads later.

```
dr_egeria --directive process --userid juleskeeper --user_pass secret strategic-information-supply-chains.md
```

---

## Part 1: The Register

The register is a folder in the Strategic Solutions collection, alongside the Data Strategy Framework blueprint that called for it.

___

## Create Collection Folder

### Display Name
Strategic Information Supply Chains

### Qualified Name
CollectionFolder::Coco::Strategic Information Supply Chains

### Purpose
Holds the information supply chains that Coco Pharmaceuticals governs and monitors at company level, so that the set can be reviewed as a whole rather than discovered one flow at a time.

### Description
The flows of data that matter enough to the business to be named, owned and watched.  Membership is deliberately restrictive: a flow enters the register only if stopping it would halt part of the business, a regulator expects its output, a fault in it could reach a patient, or its errors cannot be undone.  Everything else is governed through the systems that carry it rather than as a supply chain in its own right.  The register mixes supply chains defined here with those already established in the metadata archive, because the question it answers — what must we watch? — does not care where the definition came from.

### Category
Solution Category

### Authors
Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Strategic Solutions

### Element Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Membership Rationale
The register is a strategic solution artifact in its own right: it is the list the Data Strategy Framework's Optimized Information Supply Chains component is measured against, and belongs beside the blueprint that called for it.

### Membership Status
VALIDATED

___

---

## Part 2: Treating the Patient

Three supply chains carry data that can reach a patient.  They are listed first because the fourth test — irreversibility — applies to all of them, and because they are the flows the transition to personalised medicine depends on.

### 2.1 Personalised Treatment Ordering

*Adopted from the metadata archive.*

The order-to-treatment flow: a clinician orders a personalised therapy, the patient's material is collected and shipped in, the therapy is manufactured against that specific identity, released, returned to the treating site, and invoiced.  It is the supply chain the personalised medicine business is made of, and the only one in the register with a clock attached to the material itself — the therapy has a short viable life, and a delay anywhere in the flow is not recoverable by retrying.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Membership Rationale
Fails all four tests at once: it is how the personalised medicine business earns revenue, it carries an identity link the manufacturing regulations require to be unbroken, a fault in it reaches a named patient, and the material it tracks cannot be remade if the identity is lost.

### Membership Status
VALIDATED

___

---

### 2.2 Clinical Trials

*Adopted from the metadata archive.*

Measurements arrive from partner hospitals into a landing area, are validated and onboarded into the data lake, provisioned into the sandboxes where the research team analyses them, assessed, and reported to the regulators.  Each stage is a segment with a different team accountable for it, which is why the archive already models the chain and its per-trial variants rather than a single flow.

The chain crosses an organisational boundary at its very first hop, and the data is personally sensitive at that point.  Whether the hospital delivered what it agreed to deliver is a question the supply chain has to be able to answer, because nobody at Coco Pharmaceuticals can see inside the hospital's own processes.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Clinical Trials Information Supply Chain

### Membership Rationale
The evidence a regulatory submission is built from travels this flow.  A gap in it is discovered at inspection, years after the point where it could have been corrected, and the twenty-five year retention obligation means the flow's output outlives every system that carries it.

### Membership Status
VALIDATED

___

---

### 2.3 Adverse Event and Safety Reporting

Safety signals do not arrive through one door.  They come from trial sites, from treating clinicians, from patients directly, from product complaints raised through distribution, and from published literature — and once received, the statutory clock starts and does not care which door was used.  Nothing in the governance program had named the flow, with the result that each source was managed by whoever owned that source.

This is the register's clearest case of a chain that exists whether or not anyone models it.  Naming it makes the clock measurable end to end rather than per-source.

___

## Create Information Supply Chain

### Display Name
Adverse Event and Safety Reporting Information Supply Chain

### Qualified Name
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Identifier
Adverse-Event-Reporting

### Description
The collection of suspected adverse reactions and safety signals from every source — clinical trial sites, treating clinicians, patients, product complaints and published literature — through triage, medical assessment and coding, to expedited and periodic reporting to the regulators of each market the product is authorised in.  The chain is measured against the statutory reporting clock, which starts on first receipt by any part of the company and runs regardless of which source the report arrived through.

### Scope
The world

### Purposes
- Patient safety
- Regulatory exposure
- Irreversibility

### Integration Style
Event-driven intake with case management and scheduled regulatory submission

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Tessa Tube

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Membership Rationale
The statutory reporting clock starts on first receipt anywhere in the company, so the flow can only be governed end to end.  A report that reaches the regulator late cannot be made timely afterwards.

### Membership Status
VALIDATED

___

---

## Part 3: Making and Moving the Product

Five supply chains carry the product from raw material to the point where a pharmacist scans a pack.  Two of them already existed; three are added here because the manufacturing, serialisation and distribution programs each depend on a flow that nothing had named.

### 3.1 Batch Manufacturing and Release

The electronic batch record is assembled during production from equipment, operators, materials and in-process results, reviewed, and used by a Qualified Person to certify the batch for a specific market.  The whole of Good Manufacturing Practice rests on that record being complete, contemporaneous and attributable, and the ALCOA+ obligations in the manufacturing program are obligations about this flow specifically.

The flow has an unusual property: it is the point where several other supply chains have to have already delivered.  A batch cannot be certified unless the raw material data was verified, the equipment qualification was current, and the operator was qualified — three facts that arrive from three different chains and three different owners.

___

## Create Information Supply Chain

### Display Name
Batch Manufacturing and Release Information Supply Chain

### Qualified Name
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Identifier
Batch-Manufacturing-Release

### Description
The assembly of the electronic batch record from process, equipment, material and operator data during production, through in-process and finished product testing, deviation handling and batch record review, to certification by a Qualified Person against the requirements of each destination market.  The chain gathers evidence from the material, equipment, competency and quality flows and produces the single decision — released or not — that everything downstream depends on.

### Scope
Within organization

### Purposes
- Business continuity
- Regulatory exposure
- Patient safety
- Irreversibility

### Integration Style
Continuous capture from plant systems with staged review and electronic signature

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Membership Rationale
The batch record is the evidence the company's licence to manufacture rests on, and it is assembled once, during production, from data that cannot be reconstructed afterwards.  It is also the convergence point for the material, equipment and competency flows.

### Membership Status
VALIDATED

___

---

### 3.2 Product Serialisation and Verification

Every saleable pack carries a unique identifier that is uploaded to a national or regional repository before the pack may be released, and checked there by the pharmacy before the medicine is dispensed.  The serialisation program separates this from the rest of manufacturing for three reasons, and all three are reasons to govern it as a supply chain: the data volume exceeds the whole of the rest of manufacturing combined, the data is externally visible in real time so defects are reported back by a pharmacist rather than found internally, and both duplicate issuance and erroneous decommissioning are irreversible.

A pack destined for Belfast and one destined for Dublin leave the same line and are governed by different systems, so market destination is a property the flow itself has to carry.

___

## Create Information Supply Chain

### Display Name
Product Serialisation and Verification Information Supply Chain

### Qualified Name
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Identifier
Product-Serialisation-Verification

### Description
The generation and allocation of unique pack identifiers, their commissioning on the packaging line, the recording of aggregation into cases and pallets, upload to the national and regional verification systems required by the destination market, and the return flow of verification, decommissioning and alert data from pharmacies and trading partners.  Market destination determines which regulatory scheme applies, so the same production run may feed several external systems under different rules.

### Scope
The world

### Purposes
- Business continuity
- Regulatory exposure
- Patient safety
- Irreversibility

### Integration Style
High-volume event streaming to external verification systems with bidirectional alert flow

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Membership Rationale
Stock cannot be released until identifiers are uploaded, so an outage in this flow halts distribution.  A serial number issued twice cannot be corrected once packs are in the market, and a mistaken decommissioning destroys saleable stock within a window too short to notice by reporting.

### Membership Status
VALIDATED

___

---

### 3.3 Cold Chain and Dangerous Goods Consignment

Temperature data and transport classification travel with the goods, and the two obligations meet in the same consignment: the shipment must have been kept within its permitted range, and it must have been correctly classified and documented by a certificated person before it was handed to a carrier.  Both are the shipper's liability and neither can be delegated to the courier.

The distribution program makes the point that time pressure falls exactly where the rules are least forgiving — a personalised therapy with a short viable life, shipped to a waiting patient, is where an expedited process is most tempting and a refusal at the airport most costly.  That is an argument for the classification data being ready before the shipment is, which is a supply chain requirement rather than a logistics one.

___

## Create Information Supply Chain

### Display Name
Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Qualified Name
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Identifier
Cold-Chain-Dangerous-Goods

### Description
The data accompanying a physical consignment from despatch to receipt: transport classification derived from the substance and biological agent registers, the shipping documentation prepared by a certificated person, the continuous temperature record produced by monitoring devices in transit, and the excursion assessment and disposition decision made on arrival.  It covers outbound finished product and inbound patient-derived material alike, both of which move under time pressure and under transport regulation.

### Scope
The world

### Purposes
- Regulatory exposure
- Patient safety
- Irreversibility

### Integration Style
Device telemetry with document exchange to carriers and receiving sites

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Membership Rationale
The shipper carries a liability it cannot delegate, an expired certificate makes every subsequent consignment non-compliant however well it was handled, and product outside its permitted temperature range cannot be brought back into specification.

### Membership Status
VALIDATED

___

---

### 3.4 Physical Inventory Tracking

*Adopted from the metadata archive.*

Material tracked from supplier through depot to the point of manufacture.  It is the flow that answers whether the raw material about to enter a batch is what it claims to be and is still within its own specification — a question the batch release decision depends on absolutely, and one whose answer originates outside the company.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Membership Rationale
Manufacturing stops without it, and the raw material data it delivers is a precondition of batch release.  It also carries the hazardous substance identity that transport classification and emergency response are derived from.

### Membership Status
VALIDATED

___

---

### 3.5 New Drug Product Details

*Adopted from the metadata archive.*

The distribution of information about a new product to every system that needs to know about it.  This is a master data flow rather than a transactional one, and it is in the register because of what depends on it: manufacturing, serialisation, distribution, pricing and sales all work from a product definition none of them own, and a product defined inconsistently across them is discovered downstream as a batch certified for the wrong market or a pack serialised under the wrong scheme.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Membership Rationale
Every product-facing flow in the register reads from this one.  An inconsistency here is not visible where it is created; it surfaces as a fault in manufacturing, serialisation or distribution, which is the signature of a master data flow that needs governing as a supply chain.

### Membership Status
VALIDATED

___

---

## Part 4: Running the Company

Three supply chains carry money and the records of it.  The supplier fraud that Sally Counter detected runs underneath all three, and the lesson the corporate program drew from it — that the company's defence rested on one person's familiarity with a ledger rather than on a control — is a supply chain observation.  A flow nobody had described end to end was being monitored by somebody who happened to know what normal looked like.

### 4.1 Financial Close and External Reporting

Transactions from every operating system consolidate into the ledger, are adjusted and eliminated across the group, and become figures published to the market and to the regulators.  As a US-listed parent with UK and EU subsidiaries, the company reports under several regimes from one set of underlying records, and the obligation that reported figures reconcile to source is an obligation about traceability through this flow.

___

## Create Information Supply Chain

### Display Name
Financial Close and External Reporting Information Supply Chain

### Qualified Name
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Identifier
Financial-Close-External-Reporting

### Description
The consolidation of transactional data from the sales, procurement, manufacturing, payroll and expense systems into the general ledger, through period-end adjustment, intercompany elimination and group consolidation, to the statements filed with regulators and published to the market.  The chain has to be traceable in the opposite direction as well: any published figure must be resolvable back to the transactions it was built from, on demand and without an investigation.

### Scope
The world

### Purposes
- Regulatory exposure
- Business continuity

### Integration Style
Scheduled batch consolidation with controlled manual adjustment

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Reggie Mint

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Membership Rationale
The controls the company certifies as effective are controls over this flow, and the reconciliation from a published figure back to its source transactions is a lineage question that only an end-to-end description of the chain can answer.

### Membership Status
VALIDATED

___

---

### 4.2 Third Party Onboarding and Payment

A supplier is proposed, screened, approved, given bank details, and paid.  Sally Counter's investigation found a fraud living in the gap between the screening and the payment, and the corporate program's response was to make the checks systematic and the supplier record authoritative.  Both of those are properties of a supply chain rather than of a system: the screening result has to still be attached to the supplier record at the moment the payment is authorised, which means the flow between them is the control.

___

## Create Information Supply Chain

### Display Name
Third Party Onboarding and Payment Information Supply Chain

### Qualified Name
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Identifier
Third-Party-Onboarding-Payment

### Description
The lifecycle of a third party relationship as data: the request to onboard, sanctions and anti-bribery screening, security and quality risk assessment, approval and creation of the authoritative supplier record, the maintenance of bank and remittance details, and the invoice-to-payment flow that draws on all of it.  Changes to payment details are treated as part of the chain rather than as maintenance, because that is where the flow has historically been attacked.

### Scope
The world

### Purposes
- Regulatory exposure
- Business continuity
- Irreversibility

### Integration Style
Workflow-driven with external screening services and continuous transaction monitoring

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Reggie Mint

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Membership Rationale
This is the flow the supplier fraud travelled.  A payment made to a fraudulent account is rarely recovered, and the screening evidence that would have prevented it is only useful if it is still attached to the supplier record when the payment is authorised.

### Membership Status
VALIDATED

___

---

### 4.3 Employee Expense Payment

*Adopted from the metadata archive.*

Expense data collected, approved, and authorised for payment.  It is a smaller flow than the other two but shares their weakness: approval and payment sit in different systems, and the value of the approval depends entirely on it still being attached to the claim when the payment is made.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Membership Rationale
It is a payment flow with an approval step in a different system, which is the same structural weakness the supplier fraud exploited, and it feeds transfers of value that may be disclosable.

### Membership Status
VALIDATED

___

---

## Part 5: The Workforce

The human resource management program makes an argument that belongs in this register: the domain supplies data other domains depend on absolutely.  Manufacturing cannot certify a batch without evidence the operator was qualified, drug development cannot show good clinical practice compliance without site training records, and security cannot revoke access to someone it has not been told has left.  Those are three supply chains, and until now they were three assumptions.

### 5.1 New Employee Onboarding

*Adopted from the metadata archive.*

A new person's details distributed to every system and directory that needs them.  The archive models it as an organisation-wide flow, and the register adopts it because of the leaver case rather than the joiner case: the same chain run in reverse is how access is removed, and the interval between a person leaving and their access ending is a security exposure measured in this flow's latency.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Membership Rationale
Joiner, mover and leaver timeliness is measured on this chain, and it is the flow that determines how long a departed employee's access survives them.  It is also the point at which employee personal data enters the estate.

### Membership Status
VALIDATED

___

---

### 5.2 Workforce Competency and Qualification

Training and qualification records are held by human resources, and are relied on as evidence by manufacturing and by drug development at the moment a batch is certified or a trial is inspected.  The evidence has to be current at the moment of the act, not at the moment of the audit, which makes the freshness of the flow the thing being governed.

This is the register's clearest example of a chain crossing a domain boundary in a direction nobody planned.  Human resources maintains the records for employment reasons; two regulated processes consume them as compliance evidence.

___

## Create Information Supply Chain

### Display Name
Workforce Competency and Qualification Information Supply Chain

### Qualified Name
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Identifier
Workforce-Competency-Qualification

### Description
The flow of competency requirements, training completion, assessment results and qualification status from the learning and human resource systems to the regulated processes that depend on them — batch record signature authority in manufacturing, site staff qualification in clinical trials, certificated status for dangerous goods classification, and role-based access decisions in security.  The chain is judged on currency: a qualification record that is correct but stale is indistinguishable from an incorrect one at the point where it is relied upon.

### Scope
Within organization

### Purposes
- Regulatory exposure
- Patient safety

### Integration Style
Master data distribution with currency checks at the point of use

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Membership Rationale
Two regulated processes consume this data as compliance evidence at the moment they act.  A batch certified by an operator whose qualification had lapsed, or a trial site staffed by untrained personnel, are both discovered at inspection and neither can be remedied retrospectively.

### Membership Status
VALIDATED

___

---

### 5.3 Occupational Health Surveillance

Exposure measurements and health surveillance results, held against the individual worker, for forty years from the last entry.  The health and safety program is explicit that the records must remain interpretable across every system migration in that period, which is an unusual requirement to place on a data flow and the reason it is in the register.

The flow also inverts the usual direction of protection.  Every other control in the plant protects the product from the people; this one protects the people from the product, and the record it produces belongs to the worker rather than to the company.

___

## Create Information Supply Chain

### Display Name
Occupational Health Surveillance Information Supply Chain

### Qualified Name
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Identifier
Occupational-Health-Surveillance

### Description
The flow from the hazardous substance and biological agent registers through exposure banding and task assessment to personal and static exposure monitoring, health surveillance appointments and their results, and the long-term record held against the individual worker.  Incidents and near misses feed back into the assessments.  The chain's defining constraint is duration: the records must be retained for forty years from the last entry and must remain interpretable by whoever holds them at the end of that period, across every system migration in between.

### Scope
Within organization

### Purposes
- Regulatory exposure
- Irreversibility

### Integration Style
Periodic monitoring feeds with long-horizon archival

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Membership Rationale
It carries the longest retention obligation in the whole programme, and an exposure that was not measured at the time cannot be measured later.  A record that survives forty years but can no longer be read is the same failure as one that was lost.

### Membership Status
VALIDATED

___

---

## Part 6: Obligations That Cut Across

Two supply chains belong to no single business process.  They exist because an obligation reaches into every other flow and asks it a question.

### 6.1 Data Subject Rights

A person asks what data the company holds about them, or asks for it to be corrected or erased, and the answer has to be assembled within a month from wherever that data ended up.  The request is one flow; finding the data is the work of every other flow in the register having been described.

This is the only entry whose difficulty is a direct consequence of the others.  A subject access request is hard exactly to the extent that the company cannot say where personal data travels, which makes the register itself part of the answer.

___

## Create Information Supply Chain

### Display Name
Data Subject Rights Information Supply Chain

### Qualified Name
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Identifier
Data-Subject-Rights

### Description
The receipt and verification of a request from a data subject, its distribution to every system and processor holding data about that person, the collection and review of what comes back, and the response within the statutory period — together with the onward flow of erasure, rectification and objection decisions to the systems that must act on them.  The chain reads from the record of processing activities and depends on the personal data holdings of the other supply chains being known rather than discovered per request.

### Scope
The world

### Purposes
- Regulatory exposure

### Integration Style
Case management fanning out to system and processor holdings

### Category
Strategic Information Supply Chain

### Authors
- Jules Keeper
- Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Membership Rationale
The statutory response period runs from receipt and cannot be extended by the company not knowing where its data is.  The chain is the practical test of whether the personal data holdings described elsewhere in the register are accurate.

### Membership Status
VALIDATED

___

---

### 6.2 Sustainability Reporting

*Adopted from the metadata archive.*

Energy, emissions, materials and travel data delivered to the sustainability reporting tools.  It enters the register because its output is now externally reported rather than internally advisory, and because it draws on operational data that was never collected with reporting in mind — which is a data quality and traceability problem before it is a sustainability one.

The sustainability program links its own governance definitions to this chain when it loads from `3. sustainability/`.  The links made here are the ones the data governance program is responsible for.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Information Supply Chains

### Element Id
InformationSupplyChain::Sustainability Reporting Information Supply Chain

### Membership Rationale
Its output is externally reported, and it is assembled from operational data collected for other purposes, so the traceability of a reported figure back to its source is the flow's principal risk.

### Membership Status
VALIDATED

___

---

## Part 7: Handoffs Between Supply Chains

Where one chain ends another begins, and the handover is where accountability changes hands.  These are the points at which a fault in one supply chain becomes a failure in the next, and they are the places worth instrumenting first.

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Element2 Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
product definition

### Description
Manufacturing works from a product definition it does not own. The market authorisations carried in that definition determine which certification the Qualified Person is able to give, so an error here becomes a batch certified for a market it may not enter.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Element2 Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
verified raw material

### Description
The batch cannot start until the material data has been verified, and the verification travels with the material rather than being looked up later.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Element2 Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
operator qualification

### Description
The batch record records who performed and who checked each step. The evidence that those people were qualified to do so arrives from the competency chain and must be current at the moment of signature.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Element2 Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
manufacturing instruction

### Description
A personalised order releases a manufacturing instruction tied to one identified patient, which is the point at which the chain of identity obligation attaches to the batch.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Element2 Id
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
released packs

### Description
Identifiers may only be uploaded to the verification systems once the batch is certified, so release is the handover point between the two chains.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Element2 Id
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
released stock

### Description
Released stock is handed to distribution together with the storage conditions it must be kept within, which become the limits the transit monitoring is judged against.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Element2 Id
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Label
serialised stock

### Description
Once commissioned and aggregated, packs are tracked as physical inventory by their identifiers, so the two chains share a key from this point on.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Element2 Id
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Label
qualified supplier

### Description
Material may only be received from a supplier that has been screened, risk assessed and approved, so the supplier record is a precondition of the inventory flow.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Element2 Id
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
substance classification

### Description
Transport classification is derived from the same substance and biological agent registers that drive exposure assessment, so a substance reclassified for safety reasons changes how it may be shipped.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Clinical Trials Information Supply Chain

### Element2 Id
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
trial safety events

### Description
Suspected adverse reactions observed at a trial site enter the safety chain, and the statutory clock starts at that handover rather than when the trial data is next analysed.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Element2 Id
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
treatment outcomes

### Description
Reactions reported by a treating clinician after a personalised therapy has been administered enter the safety chain through a different door from trial events, under the same clock.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Clinical Trials Information Supply Chain

### Element2 Id
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Label
approved product definition

### Description
The evidence assembled by the trials chain becomes the authorisation the product definition is built on, which is the point where research output becomes operational master data.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Element2 Id
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
site staff training

### Description
Trial master file completeness depends on evidence that site staff were trained on the protocol before they worked to it.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Element2 Id
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
new joiner record

### Description
The person record created at onboarding is what competency and qualification records are held against, so a delay in onboarding delays every qualification that follows it.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Element2 Id
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
worker record

### Description
Enrolment in health surveillance follows from the role a person is appointed to, so the surveillance chain reads the same joiner record.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Element2 Id
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
invoiced revenue

### Description
Fulfilment of a personalised order raises the invoice that becomes reported revenue, which is where a fulfilment record and a financial record must agree.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Element2 Id
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
supplier postings

### Description
Payments made to third parties post to the ledger and are consolidated into the published figures, so a fraudulent payment is also a misstatement.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Element2 Id
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
expense postings

### Description
Approved expenses post to the ledger, and those representing transfers of value to healthcare professionals must also be identifiable for disclosure.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Element2 Id
InformationSupplyChain::Sustainability Reporting Information Supply Chain

### Label
material consumption

### Description
Materials consumed and goods moved are the operational basis of the reported emissions and materials figures, which is why their traceability matters beyond operations.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::Clinical Trials Information Supply Chain

### Element2 Id
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
trial participant data

### Description
Trial participant data is personal data held across landing areas, the data lake and analysis sandboxes, so the rights chain has to be able to reach into every segment of the trials chain.

___

---

___

## Link Information Supply Chain Peers

### Element Id
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Element2 Id
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
employee personal data

### Description
Onboarding distributes employee personal data to every system and directory, and the rights chain has to be able to follow it to each of them.

___

---


## Part 8: Governance

Each supply chain is linked to the governance definitions that govern it, using the `GovernedBy` relationship.  The definitions themselves are owned by the domains that wrote them; what this part adds is the statement of which flow each one actually lands on.

Reading the links in the other direction is the more useful exercise.  An obligation with no supply chain attached is either operating on data that does not move, or is an obligation nobody has yet worked out how to observe.

### 8.1 Personalized Treatment Ordering

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::ChainOfIdentityUnbroken

### Referenceable
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Label
chain of identity

### Description
The link between the patient, their material and the resulting therapy is carried by this flow from order to administration, and the obligation is that it is never broken at any handover.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::PatientIdentityMinimisedInManufacturing

### Referenceable
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Label
identity minimisation

### Description
The chain must carry enough identity to be certain the right therapy reaches the right patient, and no more than that into the manufacturing environment.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::BusinessImperative::OnDemandManufacturingCapability

### Referenceable
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Label
business imperative

### Description
The imperative is realised by this flow. Its latency is the company's lead time from order to treatment.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::TimeCriticalShipmentsPlanned

### Referenceable
InformationSupplyChain::Personalized Treatment Ordering Information Supply Chain

### Label
time criticality

### Description
The therapy has a short viable life, so the transport arrangements have to be planned from the order rather than assembled at despatch.

___

---

### 8.2 Clinical Trials

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::ClinicalDataAttributableToSource

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
attribution

### Description
Every measurement travelling this chain must remain attributable to the site and the person that produced it, through every transformation between the hospital and the submission.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::SourceDataVerification

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
source data verification

### Description
Verification against source is performed on data that has already travelled several segments of this chain, so the chain must preserve what was received as distinct from what was derived.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
inspection readiness

### Description
The file an inspector reads is assembled from the outputs of this chain, and must be complete at any moment rather than at the end of the trial.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::ClinicalTrialRecordRetention

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
retention

### Description
The records this chain delivers must survive twenty-five years and every system migration in that period.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
data sharing agreement

### Description
The first hop crosses an organisational boundary, and the agreement with each hospital is what makes that hop lawful for both parties.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::BlindingIntegrityPreserved

### Referenceable
InformationSupplyChain::Clinical Trials Information Supply Chain

### Label
blinding

### Description
Provisioning data into analysis sandboxes is the segment where blinding is most easily lost, so the chain has to be able to show what each recipient could see.

___

---

### 8.3 Adverse Event and Safety Reporting

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::AdverseEventReporting

### Referenceable
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
statutory reporting clock

### Description
The obligation runs from first receipt anywhere in the company, which makes it an obligation on the whole chain rather than on the pharmacovigilance system alone.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::TrialParticipantProtectionByDesign

### Referenceable
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
participant protection

### Description
Safety information arising from a trial has to reach the people who can act on it before it reaches the people who will analyse it.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Referenceable
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
sensitivity

### Description
Adverse event reports carry health data about identifiable people from sources with very different expectations of confidentiality, so the classification has to travel with the report.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::CAPAManagement

### Referenceable
InformationSupplyChain::Adverse Event and Safety Reporting Information Supply Chain

### Label
corrective action

### Description
Events traced to a product or process fault feed the corrective and preventive action process, which is where the safety chain hands over to the quality system.

___

---

### 8.4 Batch Manufacturing and Release

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
data integrity

### Description
The record is assembled once, during production, from data that cannot be reconstructed afterwards. Every ALCOA+ attribute is a property of how this chain captures and carries it.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
batch record completeness

### Description
Completeness is a property of the chain having delivered every contributing input, not of the batch record system having stored what it was given.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
market certification

### Description
Certification is the decision this chain exists to support, and it differs by destination market, so the market has to be known before the record is closed.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
raw material verification

### Description
The verification arrives from the inventory chain and must be present before the material enters the batch, which makes it a precondition on this flow.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::EquipmentQualificationCurrentAndRecorded

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
equipment qualification

### Description
Equipment qualification status is consumed by this chain at the moment of use, so a lapsed qualification invalidates production that has already happened.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
traceability

### Description
Tracing a finished pack back to its materials and forward to its destinations is a query against this chain and the ones it hands over to.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::DeviationsDocumentedInvestigatedClosed

### Referenceable
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### Label
deviations

### Description
A deviation is raised inside this flow and must be closed before the batch can be certified, so it is a gate on the chain rather than a parallel process.

___

---

### 8.5 Product Serialisation and Verification

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::SerialNumberUniquenessAbsolute

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
uniqueness

### Description
A serial number issued twice cannot be corrected once packs are distributed, so uniqueness has to be assured at generation rather than detected in reconciliation.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
upload before release

### Description
The upload is a gate on distribution: stock that has not reached the verification system cannot lawfully be sold, so an outage in this chain halts shipping.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::AggregationRelationshipsVerified

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
aggregation

### Description
Pack, case and pallet relationships recorded by this chain are what allow a shipment to be verified without opening it.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
alert handling

### Description
The return flow from pharmacies is how the company learns of a defect, and an alert that is not investigated is a falsification signal that was received and ignored.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
market destination

### Description
Destination determines which external system the identifiers go to and under which rules, so the chain must carry destination from the packaging line onwards.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TradingPartnerDataExchange

### Referenceable
InformationSupplyChain::Product Serialisation and Verification Information Supply Chain

### Label
trading partners

### Description
Part of this chain runs outside the company entirely, exchanged with distributors and dispensers under obligations neither party can discharge alone.

___

---

### 8.6 Cold Chain and Dangerous Goods Consignment

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::ColdChainMonitoring

### Referenceable
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
cold chain monitoring

### Description
The monitoring approach defines what is measured in transit and how often, which is what this chain carries.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TemperatureExcursionAssessment

### Referenceable
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
excursion assessment

### Description
An excursion has to be assessed against the product's stability data before the consignment is dispositioned, so the assessment is part of the flow rather than a follow-up.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::ConsignmentsClassifiedByCertificatedPerson

### Referenceable
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
classification

### Description
Classification is a documented act by a named certificated person, and the evidence of it travels with the consignment.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::ShipperOwnsClassification

### Referenceable
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
shipper liability

### Description
The liability cannot be delegated to the carrier, so the correctness of the data this chain produces is the company's exposure and nobody else's.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::DangerousGoodsRecordsRetained

### Referenceable
InformationSupplyChain::Cold Chain and Dangerous Goods Consignment Information Supply Chain

### Label
retention

### Description
The consignment records this chain produces must be retained and retrievable long after the shipment has been delivered.

___

---

### 8.7 Physical Inventory Tracking

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::RawMaterialDataVerifiedBeforeUse

### Referenceable
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Label
raw material verification

### Description
This is the chain the verification travels on, from the supplier's certificate of analysis to the point where the material is issued to a batch.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Referenceable
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Label
authoritative source

### Description
Material and location master data is read by manufacturing, distribution and finance, so it has to have one authoritative source rather than one per consumer.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Referenceable
InformationSupplyChain::Physical Inventory Tracking Information Supply Chain

### Label
hazardous substance register

### Description
What is held, where and in what quantity is drawn from this chain, and the register is fiction if the flow does not reflect physical reality.

___

---

### 8.8 New Drug Product Details

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Referenceable
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Label
common definitions

### Description
The product definition is read by systems that model a product differently, which is exactly the case common data definitions exist to address.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Referenceable
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Label
authoritative source

### Description
Every consumer of the product definition must read from the same source, or the inconsistency surfaces downstream as a manufacturing or distribution fault.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Referenceable
InformationSupplyChain::New Drug Product Details Information Supply Chain

### Label
catalogued

### Description
The systems that receive the product definition need to be discoverable, because a system nobody knows receives it is a system nobody updates.

___

---

### 8.9 Financial Close and External Reporting

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Referenceable
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
reconciliation

### Description
The principle is a statement about this chain being traversable in reverse, from a published figure back to the transactions that produced it.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Referenceable
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
journal review

### Description
Manual adjustment is the segment of the chain least covered by system controls and most able to change a reported figure.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Referenceable
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
internal controls

### Description
The controls the company certifies as effective are controls over this flow, and testing them means testing the flow.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Referenceable
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
segregation of duties

### Description
Segregation only holds if the separation is preserved across the systems the chain passes through, not only within each of them.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Referenceable
InformationSupplyChain::Financial Close and External Reporting Information Supply Chain

### Label
traceability

### Description
Reported figures are critical data, and their origin is several systems and one consolidation away from where they are published.

___

---

### 8.10 Third Party Onboarding and Payment

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
screening

### Description
The screening result only protects the company if it is still attached to the supplier record when a payment is authorised, which is a property of the chain rather than of the screening step.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
authoritative supplier record

### Description
The fraud found in the supplier ledger was possible because the supplier record was not authoritative, and making it so is a requirement on this flow.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
transaction monitoring

### Description
Monitoring is applied to this chain because the pattern that reveals a fraudulent payment is only visible across the whole flow, not within any one step.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
due diligence

### Description
The risk rating produced during onboarding determines how the rest of the chain treats that third party.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::SupplierSecurityRiskAssessment

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
supplier security

### Description
Suppliers connected to company systems are assessed as part of onboarding, and the assessment travels with the supplier record.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Referenceable
InformationSupplyChain::Third Party Onboarding and Payment Information Supply Chain

### Label
transfers of value

### Description
Payments to healthcare professionals and organisations must be identifiable as such within the payment flow, or the disclosure has to be reconstructed afterwards.

___

---

### 8.11 Employee Expense Payment

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Referenceable
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Label
segregation of duties

### Description
Approval and payment sit in different systems, and the value of the approval depends on it still being attached to the claim when payment is made.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Referenceable
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Label
transfers of value

### Description
Hospitality and travel provided to healthcare professionals frequently arrives as an employee expense, so the disclosure obligation reaches into this flow.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Referenceable
InformationSupplyChain::Employee Expense Payment Information Supply Chain

### Label
transaction monitoring

### Description
The same monitoring applied to supplier payments applies here, for the same structural reason.

___

---

### 8.12 New Employee Onboarding

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Referenceable
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Label
timeliness

### Description
The obligation is expressed as a latency, and the latency is this chain's.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Referenceable
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Label
accountability

### Description
Accounts are created and removed by this flow, so the accountability of every user in the estate depends on it having run correctly.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Referenceable
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Label
personal data

### Description
This is the point at which employee personal data enters the estate, and the classification applied here is the one every downstream system inherits.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Referenceable
InformationSupplyChain::New Employee Onboarding Information Supply Chain

### Label
retention

### Description
The records created and distributed by this chain are the ones that must be retained to explain an employment decision later.

___

---

### 8.13 Workforce Competency and Qualification

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Referenceable
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
competency requirements

### Description
The requirements define what this chain has to be able to evidence, role by role.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::QualificationRecordsAuthoritative

### Referenceable
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
authoritative records

### Description
Manufacturing and drug development rely on these records as compliance evidence, so a local copy that has drifted is worse than no copy at all.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Referenceable
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
batch record evidence

### Description
The batch record's signatures are only meaningful with the qualification evidence this chain supplies behind them.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::TrialMasterFileInspectionReady

### Referenceable
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
trial file evidence

### Description
Site staff training records are part of what makes the trial master file inspection ready, and they arrive from this chain.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::AnnualSecurityAwarenessTraining

### Referenceable
InformationSupplyChain::Workforce Competency and Qualification Information Supply Chain

### Label
security training

### Description
Security awareness completion is tracked on the same flow as regulated competency, and evidences a different obligation from the same records.

___

---

### 8.14 Occupational Health Surveillance

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::ExposureMonitoredAgainstBandedLimits

### Referenceable
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
exposure monitoring

### Description
The banded limits are what the measurements travelling this chain are judged against, and an exposure not measured at the time cannot be measured later.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::HealthSurveillanceRecordsRetained

### Referenceable
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
forty year retention

### Description
Forty years from the last entry, across every system migration in between, is a constraint on the chain's archival segment rather than on any current system.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::HealthSurveillanceServesWorker

### Referenceable
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
serves the worker

### Description
The record belongs to the person it describes, which determines who this chain may deliver it to and in what form.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::HazardousSubstanceAssessmentsCurrent

### Referenceable
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
assessment currency

### Description
The assessments this chain works from must be current, or the exposure banding applied to a task describes work nobody does any more.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::IncidentsRecordedAndReported

### Referenceable
InformationSupplyChain::Occupational Health Surveillance Information Supply Chain

### Label
incidents

### Description
Incidents and near misses feed back into the assessments, which makes the chain a loop rather than a line.

___

---

### 8.15 Data Subject Rights

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::DataSubjectRightsHonoured

### Referenceable
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
rights honoured

### Description
The principle is discharged by this chain, and by nothing else.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::DataSubjectRequestManagement

### Referenceable
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
request management

### Description
The approach describes how a request is received, verified and tracked; the chain is how it reaches the data.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::RecordOfProcessingActivitiesMaintained

### Referenceable
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
record of processing

### Description
The record of processing activities is what tells this chain where to look, so its accuracy is tested every time a request is answered.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Referenceable
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
retention schedules

### Description
Erasure decisions travelling this chain have to respect the retention obligations that override them, which means the schedule has to be known per holding.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::PurposeLimitation

### Referenceable
InformationSupplyChain::Data Subject Rights Information Supply Chain

### Label
purpose limitation

### Description
Answering a request requires knowing not just where personal data is but what it is there for, which is the same information purpose limitation depends on.

___

---

### 8.16 Sustainability Reporting

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Referenceable
InformationSupplyChain::Sustainability Reporting Information Supply Chain

### Label
traceability

### Description
Externally reported sustainability figures are critical data assembled from operational systems that were not built to report them, so traceability to origin is the flow's principal control.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Referenceable
InformationSupplyChain::Sustainability Reporting Information Supply Chain

### Label
quality expectations

### Description
The quality expected of a figure that will be published differs from the quality expected of the operational data it is derived from, and the difference has to be stated.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Referenceable
InformationSupplyChain::Sustainability Reporting Information Supply Chain

### Label
catalogued sources

### Description
A reported figure whose source system is not catalogued cannot be defended, and the sustainability sources are spread across sites and business units.

___

---


## Appendix: The Register at a Glance

| # | Information supply chain | Source | Tests met |
|---|---|---|---|
| 1 | Personalised Treatment Ordering | archive | continuity, regulatory, patient safety, irreversible |
| 2 | Clinical Trials | archive | regulatory, patient safety, irreversible |
| 3 | Adverse Event and Safety Reporting | this file | patient safety, regulatory, irreversible |
| 4 | Batch Manufacturing and Release | this file | continuity, regulatory, patient safety, irreversible |
| 5 | Product Serialisation and Verification | this file | continuity, regulatory, patient safety, irreversible |
| 6 | Cold Chain and Dangerous Goods Consignment | this file | regulatory, patient safety, irreversible |
| 7 | Physical Inventory Tracking | archive | continuity, regulatory |
| 8 | New Drug Product Details | archive | continuity, regulatory |
| 9 | Financial Close and External Reporting | this file | regulatory, continuity |
| 10 | Third Party Onboarding and Payment | this file | regulatory, continuity, irreversible |
| 11 | Employee Expense Payment | archive | regulatory |
| 12 | New Employee Onboarding | archive | continuity, regulatory |
| 13 | Workforce Competency and Qualification | this file | regulatory, patient safety |
| 14 | Occupational Health Surveillance | this file | regulatory, irreversible |
| 15 | Data Subject Rights | this file | regulatory |
| 16 | Sustainability Reporting | archive | regulatory |

---

## Appendix: What This File Deliberately Leaves Out

Three things are missing, and their absence is a decision rather than an oversight.

**Segments.** Most of these chains divide into segments with different owners — the clinical trials chain already does, in the metadata archive.  Segmenting the rest is the next piece of work, and it is best done by the team that owns each chain rather than centrally.  A segment boundary drawn from the outside tends to follow the system boundary rather than the accountability boundary, and the accountability boundary is the useful one.

**Implementation.** None of these chains is linked here to the solution components that execute it, which is what makes activity, error and volumetric roll-up possible.  That work is done in [`1. coco-data-hub/strategic-supply-chain-analysis.md`](../1.%20coco-data-hub/strategic-supply-chain-analysis.md), which identifies the components implementing each chain, makes them members of it, and draws the wires between them.  What remains after that is the link from each component to the system that runs it, which depends on the systems inventory that `4. keeping-safe/it-governance-program.md` builds out.

**Metrics.** Each chain has an obvious thing to measure — the reporting clock, the release gate, the joiner-to-access interval, the response period — and none of them is defined here.  Metrics attach to the governance definitions the chains are linked to in Part 8, so they are written by the domain that owns the definition, not by the register.

---

## Appendix: Related Resources

| Resource | Relevance |
|---|---|
| [Information supply chains](https://egeria-project.org/concepts/information-supply-chain/) | The concept and its representation in open metadata |
| [Defining information supply chains](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-information-supply-chains/overview/) | The Coco Pharmaceuticals scenario this file belongs to |
| `data-strategy-framework.md` | Defines the Optimized Information Supply Chains component this register makes concrete |
| [`1. coco-data-hub/strategic-supply-chain-analysis.md`](../1.%20coco-data-hub/strategic-supply-chain-analysis.md) | The solution components implementing each chain, their membership, and the wires between them |
| `1. coco-data-hub/solution-design.md` | The data-driven systems architecture the flows in this register run over |
| `2. clinical-trials/receive-data-from-hospitals.ipynb` | The clinical trials chain and its per-trial variants, in operation |
| `CocoComboArchive.omarchive` | Supplies the seven adopted supply chains and their component wiring |

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
