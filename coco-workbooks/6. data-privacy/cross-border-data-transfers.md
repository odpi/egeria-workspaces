# Coco Pharmaceuticals — Cross-Border Data Transfers

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-24  
> **Description:** Works through the personal data that crosses borders at Coco Pharmaceuticals, why the group structure makes almost all of it a restricted transfer, and what has to be in place for each flow to be lawful. Adds the privacy-side definitions the exercise surfaces. Load the whole of `0. data-governance-program` and `data-processing-purposes.md` first.

---

## The situation

Coco Pharmaceuticals is a US-listed parent with subsidiaries in the UK and the EU. That sentence, which reads as corporate structure, is the source of a substantial and largely invisible compliance burden — because personal data moving from an EU subsidiary to the US parent is, in law, both a disclosure to a third party and a restricted international transfer, and it is neither of those things in the way anyone experiences it.

What people experience is a shared HR system, a global clinical database, a consolidated ledger, and a security operations centre that watches every site. The systems are common, the login is the same, and nothing about opening a record announces that the data has crossed a jurisdiction. The transfer happens at the point of capture, not at the point somebody deliberately sends something.

Three things make this harder than it first appears.

**The instruments differ by origin, and one document cannot cover both.** EEA-origin data and UK-origin data require different transfer mechanisms. A single agreement covering "the group's European operations" covers neither properly.

**The mechanism can be invalidated without warning.** Adequacy decisions have been struck down before and certifications lapse. A transfer basis is a live thing requiring a review date and a prepared fallback, not a signed document filed once.

**The company does not control what happens next.** Once data reaches the US parent it may be processed by the parent's own suppliers, and a safeguard that protects the data as far as the parent and no further protects very little.

---

## Part 1: The flows

These are the routine, systematic flows. Each is a restricted transfer requiring a mechanism, and each was established for good operational reasons by people who were not thinking about transfer law.

### 1. Employee and workforce data → US parent

The global HR platform holds records for every entity. Payroll consolidates. Performance and succession data is reviewed centrally. Equality monitoring data — protected characteristics, voluntarily given — sits in the same estate.

The subsidiaries are the employers and therefore the controllers; the parent receives the data as a separate controller or as a processor depending on what it does with it, and that determination changes the instrument required.

*Applies:* `DataProcessingPurpose::EmploymentRelationshipAdministration` · `DataProcessingPurpose::WorkforceEqualityMonitoring` · `GovernanceObligation::IntraGroupControllershipDefined`

### 2. Clinical trial data → US-held clinical database

Investigator sites across the UK and EU capture data that consolidates centrally. Monitors employed by one entity access identifiable source records at sites regulated under another. The sponsor entity named in the protocol determines who the controller is — and it is not always the parent.

This flow is unusual in that its retention obligation outlives every transfer mechanism it will ever use: twenty-five years of retained trial data will span several rounds of instruments being superseded.

*Applies:* `DataProcessingPurpose::ClinicalTrialConduct` · `GovernanceObligation::ClinicalTrialRecordRetention` · `Regulation::EUClinicalTrialsRegulation`

### 3. Security monitoring → central operations

Authentication logs, endpoint telemetry and network monitoring from every site flow to a central security function. This is systematic observation of identifiable EU and UK workers, processed on legitimate interests, aggregated in a jurisdiction whose government access powers are the reason the transfer regime exists in its current form.

*Applies:* `DataProcessingPurpose::SecurityMonitoringAndInvestigation` · `Threat::UnauthorisedDataDisclosure`

### 4. Financial consolidation and third-party data → US parent

SOX and FCPA obligations run to the consolidated group, so subsidiary financial data reaches the parent by regulatory necessity. It carries personal data with it: supplier and distributor contacts, screening results on directors and beneficial owners, and transfers of value to named healthcare professionals.

*Applies:* `DataProcessingPurpose::ThirdPartyDueDiligenceScreening` · `DataProcessingPurpose::TransferOfValueDisclosure` · `Regulation::SarbanesOxleySection404`

### 5. Patient material and its data, physically

Personalised therapy consignments cross borders in both directions, carrying the reference and the chain of identity record with them. The physical journey and the data transfer are the same event, which is worked through in [personalised-batch-data.md](personalised-batch-data.md).

*Applies:* `GovernanceObligation::ChainOfIdentityUnbroken` · `GovernanceApproach::JointPrivacyManufacturingReview`

### 6. Onward, from the parent

Every flow above may continue past the parent into its own cloud providers and service suppliers. The company's safeguards reach the parent; whether they reach further depends on contracts the subsidiaries did not negotiate and frequently have not seen.

---

## Part 2: What the exercise surfaces

Listing the flows exposes three gaps. The first is the same shape as the chemical register finding in health and safety — an obligation exists whose population was never established.

### 2.1 Governance Obligations

___

## Create Governance Obligation

### Display Name
Cross-Border Data Flows Must Be Inventoried Before They Begin

### Qualified Name
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Domain Identifier
PRIVACY

### Summary
Every routine flow of personal data out of the UK or the EEA must be recorded before it starts, with its origin, destination, categories of data, controllership determination, transfer mechanism, and the onward recipients at the destination.

### Description
The transfer safeguard obligation requires each restricted transfer to carry a valid mechanism, and the safeguard currency metric measures whether those mechanisms are current — but neither establishes what the flows are. Without an inventory the obligation is unenforceable and the metric is computed over whatever happened to be known, which is the comfortable subset. The inventory is therefore the foundation and is treated as such. Each entry records origin and destination jurisdiction, the categories of data and of data subject, which entity determines purpose and means at each end, the mechanism relied on and its review date, and — the field most often absent and most consequential — the onward recipients at the destination, because a safeguard that stops at the parent protects nothing beyond it. Flows are recorded before they begin, since a flow discovered afterwards has been unlawful for however long it has been running. Discovery must supplement declaration: system integrations, cloud service locations and supplier contracts are examined for transfers nobody registered, and the gap between discovered and registered is the operative measure of how far the inventory can be trusted.

### Implications
- Registration precedes the first transfer, not the first audit
- Each entry records onward recipients at the destination, not only the immediate recipient
- Controllership at each end must be determined and recorded, since it selects the instrument
- Discovery through integrations, cloud locations and supplier contracts supplements declaration
- The discovered-but-unregistered gap measures how far the inventory can be relied on

### Outcomes
- The transfer safeguard obligation has a known population to work against
- Safeguard currency is measured over the real estate rather than the known subset
- Onward transfers are visible rather than assumed to be somebody else's contract

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
Government Access Requests Must Be Assessed, Challenged Where Possible, and Recorded

### Qualified Name
CocoPharma::GovernanceObligation::GovernmentAccessRequestsHandled

### Domain Identifier
PRIVACY

### Summary
Any request from a public authority for personal data originating in the UK or the EEA must be assessed for legal validity, challenged where there are grounds, notified to the originating controller and the individual where permitted, and recorded whether or not it is complied with.

### Description
Government access to transferred data is the specific concern that reshaped the transfer regime, and it is the one aspect of it that most organisations have no procedure for at all — because the request arrives rarely, arrives at the entity that received the data rather than the one that sent it, and arrives with urgency and often with a prohibition on disclosure. The obligation requires that this be worked out in advance rather than in the days available. A request is assessed against whether the authority has jurisdiction and whether the demand is lawful and proportionate in scope, with legal advice obtained rather than assumed. Grounds to challenge — overbreadth, jurisdictional reach, conflict with the originating jurisdiction's law — are pursued rather than noted, since the commitment to challenge is part of what makes the transfer mechanism defensible in the first place. The originating controller is notified wherever the law permits, because it is their data subjects and their supervisory authority. Records are kept of every request including those refused and those where notification was prohibited, and aggregate figures are published where transparency reporting is possible, since a company that has never reported a request is indistinguishable from one that has never looked.

### Implications
- The procedure must exist before a request arrives, not be assembled in response to one
- Validity and proportionality are assessed with legal advice, not accepted at face value
- Grounds to challenge are pursued, since the commitment to do so underpins the transfer mechanism
- The originating controller is notified wherever the law permits
- Every request is recorded, including refused ones and those under a disclosure prohibition

### Outcomes
- Requests are answered lawfully rather than expediently
- The commitments made in transfer risk assessments are honoured in practice
- The originating subsidiary and its supervisory authority are not the last to know

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 2.2 Governance Approaches

___

## Create Governance Approach

### Display Name
Transfer Risk Assessment and Supplementary Measures

### Qualified Name
CocoPharma::GovernanceApproach::TransferRiskAssessment

### Domain Identifier
PRIVACY

### Summary
Where a transfer relies on contractual safeguards rather than adequacy, the destination's legal environment is assessed against the protection the safeguards promise, and supplementary technical, contractual or organisational measures are applied where it falls short.

### Description
Signing standard clauses is the beginning of the analysis rather than the end of it. The clauses promise the data a level of protection, and the assessment asks whether the law of the destination country permits that promise to be kept — principally whether public authorities can compel access in ways the clauses cannot resist, and whether the individual has any effective remedy there. Where the answer is that protection falls short, the transfer does not simply proceed on the strength of the signature: supplementary measures are applied, and the approach ranks them honestly. Technical measures that make the data unintelligible to anyone but the intended recipient are the only ones that hold against a compelled disclosure; contractual commitments to challenge and to notify are valuable but do not survive a lawful order; organisational measures such as minimising what is sent are frequently the most practical. Assessments are recorded with their reasoning and are revisited when the destination's law changes, when a new mechanism replaces the one assessed, or when a government access request demonstrates that the assumption underlying the assessment was wrong. Where no combination of measures brings the transfer within tolerance, the honest outcome is that the flow does not proceed, and the approach requires that outcome to remain genuinely available rather than being reasoned around.

### Implications
- The assessment examines destination law and effective remedy, not only the signed instrument
- Supplementary measures are ranked by whether they survive a compelled disclosure
- Assessments are revisited on legal change, mechanism change, and after any access request
- Suspending or declining a flow must remain a genuinely available outcome

### Outcomes
- Contractual safeguards are relied on where they actually hold and supplemented where they do not
- The company can show a supervisory authority the reasoning behind each transfer
- Flows that cannot be brought within tolerance are stopped rather than rationalised

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Links

---

### 3.1 Governance Responses

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Rationale
Chapter V restricts transfers out of the EEA, and an obligation to safeguard each transfer presupposes knowing which transfers occur. The inventory is that population.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKGDPR

### Policy
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Rationale
UK-origin transfers require different instruments from EEA-origin ones, so the inventory must record origin jurisdiction per flow rather than treating Europe as one.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceApproach::TransferRiskAssessment

### Rationale
Reliance on contractual safeguards requires the controller to assess whether the destination's law permits those safeguards to be kept, and to supplement them where it does not.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::GovernmentAccessRequestsHandled

### Rationale
The commitments to challenge and notify that make a contractual transfer mechanism defensible are only meaningful if a procedure exists to honour them when a request arrives.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::GovernmentAccessRequestsHandled

### Rationale
A compelled disclosure to a foreign authority is a disclosure the data subject did not expect and cannot contest, and it is the specific exposure the transfer regime exists to address.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Rationale
Onward recipients at the destination are where the company's safeguards stop and its visibility ends. Recording them is what converts an assumption into a known position.

___

---

### 3.2 Governance Mechanisms

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Mechanism
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Rationale
The metric already reports newly discovered flows as an inventory gap; this obligation creates the inventory that gap is measured against.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::TransferRiskAssessment

### Mechanism
CocoPharma::GovernanceMetric::TransferSafeguardCurrency

### Rationale
Currency includes whether the required assessment is within its review period, so the metric reports the approach's upkeep as well as the instrument's.

___

---

### 3.3 Peer Policy Links

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::InternationalTransferSafeguards

### Description
The safeguard obligation says every restricted transfer needs a current mechanism; this obligation establishes which transfers there are. Neither works alone — a safeguard obligation without an inventory is enforced over the known subset, and an inventory without the safeguard obligation is a list.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::IntraGroupControllershipDefined

### Description
The inventory records the controllership determination per flow because that determination selects the instrument: controller-to-controller, controller-to-processor and joint controllership each require a different arrangement between the same two entities.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::TransferRiskAssessment

### Governance Policy 2
CocoPharma::GovernanceApproach::GroupControllershipMapping

### Description
The mapping establishes which entity is exporting and which supervisory authority would examine the transfer; the assessment establishes whether the destination permits the safeguard to hold. Both are needed before a flow can be defended.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::GovernmentAccessRequestsHandled

### Governance Policy 2
CocoPharma::GovernanceObligation::DataBreachNotificationWithin72Hours

### Description
An unlawful compelled disclosure may also be a personal data breach, and the two procedures must reach a consistent answer rather than the access procedure quietly displacing the notification duty.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Description
The catalog records what data exists and where it is held; the flow inventory records where it goes. A flow whose source asset is uncatalogued cannot have its categories of data described accurately, which is why the two are populated from each other rather than separately.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Governance Policy 2
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Description
The data programme requires routine internal flows to be governed by a recorded agreement. Where such a flow also crosses a border it needs a transfer mechanism as well, and the two records describe the same arrangement from the operational and the jurisdictional side.

___

---

## Part 4: Folio Membership

The definitions added here are privacy-domain definitions and join the Chief Privacy Officer folio.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::CrossBorderFlowInventory

### Membership Rationale
The inventory of cross-border flows underpins every transfer safeguard and is maintained by the privacy team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceObligation::GovernmentAccessRequestsHandled

### Membership Rationale
Handling authority demands for transferred data is a privacy responsibility exercised with legal counsel.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefPrivacyOfficer

### Element Id
CocoPharma::GovernanceApproach::TransferRiskAssessment

### Membership Rationale
Transfer risk assessment and the selection of supplementary measures is owned by the Chief Privacy Officer.

### Membership Status
VALIDATED

___

---

## Appendix: Coverage map

| Question | Definition | Status |
|---|---|---|
| Which flows cross a border at all? | `CrossBorderFlowInventory` | *new* |
| Does each flow have a valid mechanism? | `InternationalTransferSafeguards` | existing |
| Which entity is exporting, to which authority? | `GroupControllershipMapping` | existing |
| Is the sending entity a controller, or a processor? | `IntraGroupControllershipDefined` | existing |
| Does the destination's law let the safeguard hold? | `TransferRiskAssessment` | *new* |
| What happens when an authority demands the data? | `GovernmentAccessRequestsHandled` | *new* |
| Are the mechanisms still current? | `TransferSafeguardCurrency` | existing |
| What governs the processors receiving it? | `DataProcessingAgreementsRequired` | existing |

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| [personalised-batch-data.md](personalised-batch-data.md) | The scenario where a physical consignment and a data transfer are the same event |
| [data-processing-purposes.md](data-processing-purposes.md) | The purposes attached to each flow described in Part 1 |
| `0. data-governance-program/privacy-governance-program.md` | The transfer safeguard, controllership and supervisory authority definitions this scenario builds on |
| `0. data-governance-program/drug-development-governance.md` | Trial data flows from UK and EU sites into a US-held database |
| `0. data-governance-program/corporate-governance-program.md` | Financial consolidation carrying third-party and healthcare professional data to the parent |
| `0. data-governance-program/data-security-strategy.md` | Security monitoring centralising employee telemetry across jurisdictions |
