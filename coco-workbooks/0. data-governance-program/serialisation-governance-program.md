# Coco Pharmaceuticals — Serialisation and Product Traceability Governance Program

> **Author:** Stew Faster (Head of Manufacturing), Florence Paynter, George Pie  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-23  
> **Description:** Governance definitions for product serialisation and supply chain traceability at Coco Pharmaceuticals, carrying Domain Identifier `MANUFACTURING`. Separated from `manufacturing-governance-program.md` because serialisation is a distinct data domain with its own regulations, its own external interfaces, and a data volume larger than the whole of the rest of manufacturing combined. Load `joint-governance-officer-definitions.md` and `manufacturing-governance-program.md` first.

---

## Overview

Serialisation gives every saleable pack of medicine a unique identity and requires that identity to be reported to national systems that pharmacies check before dispensing. It exists to keep falsified medicines out of the legitimate supply chain, and it converts what was a physical distribution problem into a data problem operating at a scale nothing else in the company approaches: tens of millions of unique identifiers a year, each generated once, printed once, verified at several points, and decommissioned exactly once.

The regulatory position is fragmented in a way that follows the group structure. EU packs fall under the Falsified Medicines Directive and its Delegated Regulation, reporting into the European Hub and onward to national repositories. The UK left that system on withdrawal from the EU and operates its own arrangements, so a pack destined for Belfast and one destined for Dublin are governed differently despite leaving the same production line. US packs fall under the Drug Supply Chain Security Act, which took a different technical path — no central repository, but interoperable electronic tracing between trading partners, with the obligation resting on exchanging and retaining transaction information rather than on uploading to a hub.

Three characteristics make this a governance problem rather than a systems integration problem:

**Uniqueness is absolute and unrecoverable.** A serial number issued twice is a defect that cannot be corrected once packs are in distribution, because both packs are legitimate and the system cannot say which. Number generation therefore needs governance ordinarily reserved for financial controls.

**The data is externally visible in real time.** When a pharmacist scans a pack and the system says it is already decommissioned, the company learns about a data problem from a patient standing at a counter. There is no internal reconciliation step that catches errors first.

**Decommissioning is irreversible and time-boxed.** A pack marked as dispensed cannot be reinstated after a short window, so an erroneous decommissioning destroys saleable stock.

This program covers the drivers, policies, and controls specific to serialisation. It relies on the batch traceability and data integrity policies in `manufacturing-governance-program.md` rather than restating them, and its definitions join the Manufacturing Governance Lead folio.

---

## Part 1: Governance Drivers — Serialisation

---

### 1.1 Regulations

___

## Create Regulation

### Display Name
EU Falsified Medicines Directive and Delegated Regulation 2016/161

### Qualified Name
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Domain Identifier
MANUFACTURING

### Summary
EU legislation requiring prescription medicines to carry a unique identifier and an anti-tampering device, with identifiers uploaded to a central repository and verified and decommissioned at the point of dispensing.

### Description
Directive 2011/62/EU and Delegated Regulation (EU) 2016/161 together establish the European Medicines Verification System. Every pack of a prescription medicine carries a unique identifier in a two-dimensional barcode encoding the product code, a randomised serial number, the batch number, and the expiry date. Manufacturers upload identifiers to the European Hub, which distributes them to the national repository of each market the pack may reach. Wholesalers verify at defined points, and the pharmacy verifies and decommissions at dispensing. The serial number must be randomised with a guessing probability below one in ten thousand, which rules out sequential allocation. The system is designed so that a falsified pack either carries an identifier that does not exist, or one that has already been decommissioned — and either produces an alert investigated by the national organisation and the manufacturer. Alerts are consequential: a pattern of unexplained alerts against Coco Pharmaceuticals product triggers regulatory attention regardless of whether falsification is eventually found, and most alerts in practice arise from data quality rather than crime.

### Regulation Source
Directive 2011/62/EU and Commission Delegated Regulation (EU) 2016/161

### Regulators
- European Medicines Agency (EMA)
- National competent authorities in EU member states
- European Medicines Verification Organisation (EMVO) and national verification organisations

### Implications
- Serial numbers must be randomised to the specified guessing probability, not sequential
- Identifiers must be uploaded to the European Hub before packs are released to market
- Every market a pack may reach must have the identifier in its national repository
- Alerts must be investigated and responded to within defined timeframes
- Data quality problems surface as suspected falsification alerts at the point of dispensing

### Importance
Critical

### Category
Serialisation & Traceability

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
UK Medicines Verification Arrangements

### Qualified Name
CocoPharma::Regulation::UKMedicinesVerification

### Domain Identifier
MANUFACTURING

### Summary
The UK arrangements for medicines verification following withdrawal from the European Medicines Verification System, under which Great Britain operates outside the EU repository network while Northern Ireland's position is governed by the Windsor Framework.

### Description
On leaving the EU the United Kingdom ceased to participate in the European Medicines Verification System, and packs supplied to Great Britain are no longer verified through the EU repositories. Northern Ireland's position is determined by the Windsor Framework rather than by Great Britain's, which means product moving within the United Kingdom can face different requirements depending on destination. The practical governance consequence for Coco Pharmaceuticals is that market destination must be known and controlled at the point of packaging and release rather than being resolved later in distribution, because the applicable regime — and therefore whether an identifier must be uploaded to the EU Hub, and to which national repositories — is determined by where the pack is going. Product diverted between markets after release creates a compliance exposure that is difficult to correct: a pack whose identifier was never uploaded to a market's repository will fail verification at the pharmacy in that market. The UK regime remains subject to change, so the governance emphasis is on retaining the flexibility to serialise for either destination and on keeping market allocation data accurate.

### Regulation Source
UK Human Medicines Regulations 2012 as amended, and the Windsor Framework arrangements for Northern Ireland

### Regulators
- Medicines and Healthcare products Regulatory Agency (MHRA) — UK
- Department of Health (Northern Ireland)

### Implications
- Market destination must be determined and controlled at packaging, not in distribution
- Great Britain and Northern Ireland destinations may require different treatment for the same product
- Diversion between markets after release creates verification failures that cannot be corrected remotely
- The regime is subject to change, so serialisation capability must remain flexible for either destination

### Importance
Critical

### Category
Serialisation & Traceability

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
US Drug Supply Chain Security Act

### Qualified Name
CocoPharma::Regulation::DrugSupplyChainSecurityAct

### Domain Identifier
MANUFACTURING

### Summary
US legislation requiring interoperable, electronic, package-level tracing of prescription drugs through the supply chain, with transaction information exchanged between trading partners and retained for six years.

### Description
The DSCSA takes a different architectural approach from the EU system. Rather than a central repository that pharmacies query, it requires trading partners to exchange transaction information, transaction history, and transaction statements electronically at each change of ownership, and to be able to respond to verification and tracing requests at package level. The obligation is therefore distributed: the company must send accurate data to each customer, receive and retain data from each supplier, respond to tracing requests within the required timeframe, and verify saleable returns before redistributing them. Trading partners must be authorised, meaning the company must confirm each customer and supplier holds a valid licence or registration before transacting — a check that connects directly to the corporate third-party approval process. Records are retained for six years. Because the data lives with trading partners rather than in a hub, data quality problems propagate outward and are discovered by customers, and a customer unable to reconcile received product against received data may reject a shipment.

### Regulation Source
Drug Supply Chain Security Act, Title II of the Drug Quality and Security Act of 2013

### Regulators
- Food and Drug Administration (FDA) — United States

### Implications
- Transaction data must be exchanged electronically and accurately at each change of ownership
- Trading partners must be verified as authorised before transacting
- Tracing and verification requests must be answered within regulated timeframes
- Transaction records must be retained for six years and remain retrievable
- Saleable returns must be verified before redistribution

### Importance
Critical

### Category
Serialisation & Traceability

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

### 1.2 Threats

___

## Create Threat

### Display Name
Falsified Product Entering the Legitimate Supply Chain

### Qualified Name
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Domain Identifier
MANUFACTURING

### Summary
Counterfeit or otherwise falsified product bearing Coco Pharmaceuticals branding may reach patients through the legitimate distribution network, causing harm and destroying confidence in genuine product.

### Description
Falsified medicines enter the legitimate chain at its weaker joints — through diverted stock re-entering distribution, through wholesalers dealing outside authorised channels, and through returns processes that accept product back without adequate verification. The harm is direct: a falsified medicine may contain no active ingredient, the wrong ingredient, or a toxic one, and the patient taking it believes they are being treated. The harm to the company is severe and asymmetric, because patients and prescribers cannot distinguish a falsification from a manufacturing failure, and a falsification incident damages confidence in every pack of that product regardless of provenance. Serialisation is the principal control, but it only works if the underlying data is right: a verification system that generates frequent false alerts trains pharmacists to dismiss them, at which point a genuine falsification alert is dismissed alongside the noise. The company's data quality is therefore part of the collective defence, not merely its own compliance position.

### Implications
- Returns and diverted stock are the highest-risk routes and require verification before redistribution
- Serialisation only defends against falsification if alert quality is high enough to be trusted
- Poor data quality actively degrades the defence for the whole market, not only for this company
- Wholesaler and distributor authorisation must be verified, not assumed

### Importance
Critical

### Category
Serialisation & Traceability

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

## Create Threat

### Display Name
Serialisation Data Failure Blocking Legitimate Supply

### Qualified Name
CocoPharma::Threat::SerialisationDataFailure

### Domain Identifier
MANUFACTURING

### Summary
Errors in serialisation data may prevent genuine product from being dispensed, creating supply interruption for patients and a false appearance of falsification.

### Description
This threat is the mirror image of falsification and, on current experience across the industry, materialises far more often. A pack whose identifier was never uploaded, was uploaded to the wrong market's repository, was decommissioned in error during warehouse handling, or carries a barcode that will not scan reliably, cannot be dispensed. From the pharmacy's perspective it is indistinguishable from a falsified pack, so the failure is recorded as a suspected falsification alert, investigated as one, and counted in the statistics regulators use to assess whether the company's product is being targeted. Meanwhile a patient does not receive their medicine. The scale of the exposure is what makes it a governance matter rather than an operational one: a systematic error in an upload affects an entire batch simultaneously across every pharmacy holding it, and because the data is externally visible the company usually learns of it from the market rather than from its own monitoring. Aggregation errors compound this — where a case is scanned rather than each pack, a wrong parent-child relationship silently misattributes hundreds of packs.

### Implications
- Upload completeness must be verified before release, since errors affect whole batches at once
- Erroneous decommissioning destroys saleable stock within a short reversal window
- Aggregation errors misattribute many packs from a single mistake and are hard to detect downstream
- Alert investigation capacity must be sized for data-quality alerts, which dominate the volume

### Importance
High

### Category
Serialisation & Traceability

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

## Part 2: Governance Policies — Serialisation

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Every Serial Number Is Issued Once and Never Reissued

### Qualified Name
CocoPharma::GovernancePrinciple::SerialNumberUniquenessAbsolute

### Domain Identifier
MANUFACTURING

### Summary
Serial number uniqueness is treated as an absolute constraint enforced at generation, because a duplicate cannot be detected reliably in the field and cannot be corrected once packs are distributed.

### Description
Most data quality problems are recoverable: a wrong value is corrected and the corrected value propagates. A duplicated serial number is not. Once two packs bearing the same identifier are in distribution, both are genuine, neither can be identified as the duplicate, and the verification system will report the second decommissioning as a suspected falsification of a real product — which is precisely the alert the whole system exists to make meaningful. This principle therefore treats number generation with the rigour normally applied to financial controls: a single authoritative generator per product code, allocation recorded before printing rather than after, randomisation meeting the regulatory guessing probability, and no manual creation or reuse of numbers under any circumstance, including rework and reprinting. Numbers allocated but not applied to a saleable pack are recorded as consumed rather than returned to the pool, because the cost of retiring an unused number is nothing and the cost of reissuing one is unrecoverable. Ranges are never shared between sites or between contract manufacturers.

### Implications
- One authoritative generator per product code, with no manual number creation
- Allocation is recorded before printing, so a printing failure cannot silently reuse a number
- Numbers allocated but unused are retired, never returned to the available pool
- Ranges are never shared between sites or contract manufacturers
- Rework and reprint consume new numbers rather than reusing the original

### Outcomes
- Duplicate identifiers do not reach distribution
- Decommissioning alerts retain their meaning as genuine falsification indicators
- Number allocation can be reconciled and audited end to end

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
Market Destination Governs Serialisation Treatment

### Qualified Name
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Domain Identifier
MANUFACTURING

### Summary
The regulatory treatment of a pack follows its intended market, which must be determined and controlled at packaging rather than resolved later in distribution.

### Description
A pack leaving the line is not regime-neutral. An EU destination requires upload to the European Hub and onward distribution to the national repositories of every market the pack might reach; a Great Britain destination does not; Northern Ireland follows the Windsor Framework; a US destination requires transaction data exchange with the receiving trading partner instead. These are not variations on a process but different processes, and the choice between them is made when the pack is coded. This principle requires market allocation to be a controlled attribute set at packaging and carried with the pack thereafter, and requires diversion between markets after release to be treated as a change requiring assessment rather than a commercial decision taken in distribution. Where product is packed for a market and later needs to serve another, the serialisation consequences are established before the stock moves — in some cases the product cannot lawfully be redirected at all, and knowing that before the stock is committed is the point of the control.

### Implications
- Market allocation is a controlled attribute set at packaging and carried with the pack
- Post-release diversion between markets requires assessment, not a commercial decision alone
- Repository upload scope must cover every market a pack could legitimately reach
- Great Britain and Northern Ireland must be distinguishable in allocation data

### Outcomes
- Packs verify successfully in the market where they are dispensed
- Diversion exposures are identified before stock is committed rather than at the pharmacy counter
- Upload scope errors are prevented rather than detected through alerts

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

### 2.2 Governance Obligations

___

## Create Governance Obligation

### Display Name
Identifiers Must Be Uploaded and Confirmed Before Batch Release

### Qualified Name
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Domain Identifier
MANUFACTURING

### Summary
For every batch destined for a repository market, all pack identifiers must be uploaded and upload confirmation received and reconciled against the batch record before the Qualified Person releases the batch.

### Description
Upload before release is the control that prevents an entire batch failing verification simultaneously in the market. The obligation requires more than transmission: it requires positive confirmation from the repository, reconciled against the count of packs actually produced and coded in the batch record, so that a partial upload is detected while the stock is still in the company's control. Reconciliation is the substance of the obligation, because a transmission that reports success while silently rejecting a subset is the failure mode that produces field alerts weeks later. Discrepancies must be resolved before release rather than noted for follow-up, since once the batch has shipped the affected packs cannot be identified without recalling stock. The obligation is placed in the release decision deliberately, making it the Qualified Person's check alongside the existing GMP release criteria, rather than a separate supply chain step that runs in parallel and can be overtaken by shipping pressure.

### Implications
- Positive upload confirmation must be received, not merely transmission success
- Confirmed counts must be reconciled against packs produced and coded in the batch record
- Discrepancies must be resolved before release, not tracked afterwards
- The check sits within the QP release decision, not alongside it
- Upload scope must cover every market the batch may reach, per the destination principle

### Outcomes
- Batches do not reach market with missing or partial repository data
- Upload failures are found while the stock is still controllable
- Verification failures attributable to the company's own data become rare enough that alerts stay meaningful

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
Aggregation Relationships Must Be Verified at Each Packing Level

### Qualified Name
CocoPharma::GovernanceObligation::AggregationRelationshipsVerified

### Domain Identifier
MANUFACTURING

### Summary
Parent-child relationships between packs, cases, and pallets must be established by verified scanning at each packing level and must be corrected only through a controlled process that preserves the audit trail.

### Description
Aggregation lets a warehouse scan one case label instead of every pack inside it, which is what makes serialised distribution economically viable — and it means that one wrong relationship silently misattributes every pack it claims to contain. A case recorded as holding packs it does not hold will decommission the wrong identifiers when handled, generating alerts against product that is elsewhere and leaving the actual packs in an inconsistent state. This obligation requires relationships to be established by verified scanning rather than inferred from production sequence or expected counts, and requires any subsequent change — a case opened for a partial shipment, a pack removed for sampling or damage — to be recorded through a controlled disaggregation process rather than by editing the relationship. Where aggregation data is known to be unreliable for a consignment, the correct response is to ship it disaggregated and accept the handling cost, rather than to ship data the receiving partner will act on incorrectly.

### Implications
- Relationships must come from verified scanning, never from expected counts or production sequence
- Partial shipments and pack removals require controlled disaggregation, not relationship editing
- Every relationship change must retain an audit trail
- Unreliable aggregation data must result in disaggregated shipment rather than transmitted uncertainty

### Outcomes
- Downstream decommissioning acts on correct identifiers
- Aggregation errors are contained at the point they occur rather than propagating to trading partners
- Warehouse efficiency gains from aggregation are not paid for in field alerts

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
Verification Alerts Must Be Investigated and Closed Within Regulated Timeframes

### Qualified Name
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Domain Identifier
MANUFACTURING

### Summary
Every alert raised against Coco Pharmaceuticals product must be investigated, classified as data quality or suspected falsification, and closed within the timeframe the applicable regime allows.

### Description
An alert is a pharmacy reporting that a pack of the company's product did not verify, and the company's response determines both whether a falsification is caught and whether a patient gets their medicine. Investigation must establish which of the two it is, and the classification matters beyond the individual case: falsification suspicions are escalated to the competent authority and to the relevant verification organisation, while data quality alerts are corrected and, more importantly, trended to find the systematic cause. Most alerts in practice are data quality, and treating them individually without addressing the pattern guarantees they recur. The obligation requires root cause analysis at the level of the cause rather than the pack — a batch whose upload was partial produces many alerts from one defect — and requires alert rates to be reported by cause category so that recurring causes are visible. Where an alert cannot be resolved as data quality, it is treated as suspected falsification until demonstrated otherwise rather than the reverse.

### Implications
- Alerts must be classified as data quality or suspected falsification, with reasoning recorded
- Unresolved alerts default to suspected falsification, not to assumed data error
- Root cause analysis operates at the level of the defect, not the individual pack
- Alert rates must be trended by cause category to surface systematic problems
- Escalation routes to competent authorities must be defined and exercised

### Outcomes
- Genuine falsification is escalated promptly rather than absorbed into data-quality noise
- Systematic data defects are corrected at source instead of recurring
- Patients affected by a verification failure are supplied without avoidable delay

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
Trading Partner Transaction Data Must Be Exchanged, Verified, and Retained

### Qualified Name
CocoPharma::GovernanceObligation::TradingPartnerDataExchange

### Domain Identifier
MANUFACTURING

### Summary
Transaction information must be exchanged electronically with authorised trading partners at each change of ownership, verified on receipt, and retained for six years in a retrievable form.

### Description
Under the DSCSA the company's compliance depends partly on data it receives from others, which makes verification on receipt as important as accuracy on transmission. Incoming transaction data must be checked for completeness and internal consistency and reconciled against physical receipt, with discrepancies raised with the sending partner rather than absorbed, since accepting inconsistent data propagates it onward to the company's own customers. Outbound data must be accurate and must reach the customer in the agreed format and timeframe; a customer unable to reconcile a shipment against its data may reject it outright. Trading partner authorisation must be confirmed before transacting — a check that overlaps directly with the corporate approved third-party process and should reach a consistent answer, since a partner acceptable commercially but not licensed to handle prescription medicines must not be supplied. Six-year retention must survive system replacement, and tracing requests must be answerable within regulated timeframes throughout that period.

### Implications
- Incoming data must be verified and reconciled against physical receipt, not accepted on trust
- Discrepancies must be raised with the sending partner rather than corrected silently
- Trading partner authorisation must be confirmed before transacting and kept current
- Retention must survive system replacement, with tracing answerable throughout
- Authorisation checks must reconcile with the corporate approved third-party determination

### Outcomes
- The company neither receives nor propagates inconsistent transaction data
- Tracing and verification requests are answered within regulated timeframes
- Unlicensed parties are not supplied with prescription medicines

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

### 2.3 Governance Approaches

___

## Create Governance Approach

### Display Name
Centralised Serialisation Data Management

### Qualified Name
CocoPharma::GovernanceApproach::CentralisedSerialisationDataManagement

### Domain Identifier
MANUFACTURING

### Summary
Serial number generation, repository connections, and market allocation are managed from a single central system serving all sites and contract manufacturers, rather than site by site.

### Description
Serialisation is one of the few areas where centralisation is not a preference but a requirement of the data model: uniqueness cannot be guaranteed across independently operating generators, and the repository connections are per-company rather than per-site. The approach places number generation, market allocation, repository interfaces, and alert handling in one system, with production sites and contract manufacturers drawing allocated ranges from it and reporting commissioning events back. Contract manufacturers are the harder case and the one most often got wrong, because they operate their own line systems and may serve several clients: the interface must deliver ranges without exposing the company's wider allocation, and must receive commissioning confirmation in a form that can be reconciled. The central system is treated as a validated GMP system under the manufacturing computerised systems obligation, since batch release now depends on it. Its availability requirement is unusually high because a repository connection failure stops release, and the approach therefore specifies buffering behaviour and a defined maximum period for which production may continue before release is blocked.

### Implications
- One central system owns generation, allocation, repository interfaces, and alert handling
- Contract manufacturer interfaces must deliver ranges without exposing wider allocation data
- The system is a validated GMP system, since batch release depends on it
- Buffering behaviour and a maximum period of degraded operation must be specified
- Site systems report commissioning events back rather than generating numbers locally

### Outcomes
- Uniqueness is enforceable because generation has a single authority
- Contract manufacturers participate without weakening the control
- Connection failures degrade predictably instead of stopping production without warning

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

## Create Governance Approach

### Display Name
Alert Triage and Root Cause Reduction

### Qualified Name
CocoPharma::GovernanceApproach::AlertTriageAndRootCauseReduction

### Domain Identifier
MANUFACTURING

### Summary
Alerts are triaged on a defined path that separates suspected falsification from data quality within hours, with data quality alerts driving root cause elimination rather than case-by-case correction.

### Description
The approach exists because alert volume is dominated by the company's own data defects, and handling those case by case consumes the capacity needed to investigate the rare genuine falsification properly. Triage runs on a defined path: identify the pack, establish its production and upload history, determine whether the identifier exists in the expected repository and what state it holds, and classify. Cases that resolve to a known data defect are grouped to that defect rather than investigated individually, so that a partial upload affecting six hundred packs is one investigation and one corrective action rather than six hundred. Cases that do not resolve are escalated as suspected falsification within the regulated timeframe. Root cause reduction then targets the defect classes producing the most alerts, which are usually a small number of recurring mechanisms — upload scope errors, aggregation mistakes in one warehouse, marginal print quality on one line. Alert rate per million packs is tracked as the measure of whether reduction is working, because absolute alert counts move with volume and conceal the trend.

### Implications
- Triage must classify within hours, since falsification escalation is time-bound
- Alerts arising from one defect are grouped into one investigation and one corrective action
- Root cause work must target defect classes by alert volume, not individual cases
- Alert rate must be normalised per million packs to be interpretable across volume changes
- Unresolved cases escalate as suspected falsification within the regulated timeframe

### Outcomes
- Genuine falsification receives full investigative attention
- Recurring data defects are eliminated rather than repeatedly corrected
- Alert rates fall to a level where each remaining alert is worth taking seriously

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

## Part 3: Governance Controls — Serialisation

---

### 3.1 Governance Roles

___

## Create Governance Role

### Display Name
Serialisation Data Manager

### Qualified Name
CocoPharma::GovernanceRole::SerialisationDataManager

### Description
The Serialisation Data Manager owns the central serialisation system and the data flowing through it: number allocation to sites and contract manufacturers, market allocation configuration, repository and trading partner connections, upload reconciliation, and the alert triage process. The role approves the serialisation configuration for a new product or market before first production, maintains the interface arrangements with contract manufacturers, and reports alert rates and root cause reduction progress to the Manufacturing Governance Lead. It is the escalation point when a repository connection failure threatens to block batch release, and works with the Qualified Person on the upload confirmation element of the release decision.

### Scope
The central serialisation system, number allocation, market allocation, repository and trading partner interfaces, upload reconciliation, and alert triage across all sites and contract manufacturers.

### Headcount
2

### Category
Governance Role

### Search Keywords
- serialisation
- unique identifiers
- medicines verification
- track and trace

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
Verification Alert Rate per Million Packs

### Qualified Name
CocoPharma::GovernanceMetric::VerificationAlertRate

### Domain Identifier
MANUFACTURING

### Summary
Measures alerts raised against Coco Pharmaceuticals product per million packs supplied, reported by cause category and separating data quality from suspected falsification.

### Description
Normalisation per million packs is what makes the figure interpretable, since absolute counts rise with volume and would show deterioration during growth and improvement during a supply shortage. The metric separates data quality alerts from suspected falsification, and within data quality reports by cause category — upload scope, aggregation, print quality, erroneous decommissioning — because the categories have different owners and different remedies, and an aggregate rate tells nobody what to fix. Reporting is also broken down by market, since a rate concentrated in one country usually indicates a repository configuration problem rather than a production one. The suspected falsification count is reported as an absolute number alongside the rate and is never normalised, for the same reason chain of identity breaks are not: each is a potential patient safety event warranting individual attention. Target is fewer than fifty data quality alerts per million packs, trending downward, with every falsification suspicion escalated within the regulated timeframe.

### Implications
- Rate must be normalised per million packs to be interpretable across volume changes
- Data quality alerts must be broken down by cause category and by market
- Suspected falsification is reported as an absolute count, never normalised
- The metric depends on alerts being classified accurately during triage

### Outcomes
- Root cause reduction progress is visible and attributable to specific defect classes
- Market-specific configuration problems are distinguished from production problems
- Falsification suspicions retain individual visibility rather than being averaged away

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

## Create Governance Metric

### Display Name
Upload Reconciliation Success Rate at Release

### Qualified Name
CocoPharma::GovernanceMetric::UploadReconciliationSuccessRate

### Domain Identifier
MANUFACTURING

### Summary
Measures the percentage of batches whose identifier upload was confirmed and reconciled against the batch record without discrepancy at the first attempt before release.

### Description
This metric tests the control that prevents whole-batch field failures, and it is measured at first attempt because a discrepancy resolved before release is still a defect that consumed time in the release window and would have reached the market had it gone unnoticed. Discrepancies are categorised — packs produced but not uploaded, packs uploaded but not produced, market scope incomplete, repository rejection — since each points at a different part of the chain between line and hub. Batches produced by contract manufacturers are reported separately, because the reconciliation depends on data returned across an external interface and typically shows a lower first-attempt rate. The metric is deliberately paired with the alert rate: a high reconciliation success rate alongside a rising upload-scope alert rate indicates that reconciliation is checking the wrong thing, most often confirming counts against one repository while the pack could reach several. Target is 98% first-attempt success with no batch released on an unresolved discrepancy.

### Implications
- Measurement is at first attempt, since a caught discrepancy still indicates a defect
- Discrepancies must be categorised to locate the failing part of the chain
- Contract manufacturer batches must be reported separately
- The metric must be read alongside alert rate to detect reconciliation checking the wrong scope

### Outcomes
- Whole-batch verification failures in the field become rare
- The weakest links between line and repository are identified by category
- Contract manufacturer interface quality is visible rather than assumed

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

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to Serialisation Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Policy
CocoPharma::GovernancePrinciple::SerialNumberUniquenessAbsolute

### Rationale
The Delegated Regulation requires randomised identifiers with a specified guessing probability, and the verification model collapses if an identifier is issued twice. Uniqueness enforced at generation is the only point where this can be guaranteed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Policy
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Rationale
Packs must be present in the national repository of every market they may reach before they arrive there. Confirming upload as part of release is what makes that reliable rather than probable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Policy
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Rationale
The Regulation places an investigation and response duty on the manufacturer for alerts raised against its product, within defined timeframes.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKMedicinesVerification

### Policy
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Rationale
Great Britain sits outside the EU repository network while Northern Ireland follows the Windsor Framework, so destination determines the applicable process and must be fixed at packaging.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::DrugSupplyChainSecurityAct

### Policy
CocoPharma::GovernanceObligation::TradingPartnerDataExchange

### Rationale
The DSCSA distributes the obligation across trading partners rather than centralising it, so accurate exchange, verification on receipt, and six-year retention are the substance of compliance.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::DrugSupplyChainSecurityAct

### Policy
CocoPharma::GovernanceObligation::AggregationRelationshipsVerified

### Rationale
Package-level tracing depends on parent-child relationships being correct, since trading partners act on aggregation data they cannot independently verify without opening cases.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Policy
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Rationale
Alerts are the mechanism by which falsification is detected. Their value depends entirely on investigation quality and on the classification decision being made correctly.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Policy
CocoPharma::GovernanceApproach::AlertTriageAndRootCauseReduction

### Rationale
Reducing data quality alerts is a falsification control in itself: an alert stream dominated by noise trains pharmacists to dismiss the alert that matters.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::SerialisationDataFailure

### Policy
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Rationale
The most damaging form of this threat is a whole batch failing verification simultaneously, which upload reconciliation before release is specifically designed to prevent.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::SerialisationDataFailure

### Policy
CocoPharma::GovernanceObligation::AggregationRelationshipsVerified

### Rationale
Aggregation errors misattribute many packs from a single mistake and are undetectable downstream without opening cases, making verified scanning the only effective control point.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::SerialisationDataFailure

### Policy
CocoPharma::GovernanceApproach::CentralisedSerialisationDataManagement

### Rationale
Distributed generation and configuration multiply the opportunities for scope and allocation error. Centralisation reduces the surface on which this threat operates.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKMedicinesVerification

### Policy
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Rationale
Great Britain sits outside the EU release framework while Northern Ireland follows it, so a single production run may require separate certification and a Responsible Person (Import) for the Great Britain portion.

___

---

### 4.2 Governance Mechanisms — Serialisation Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Mechanism
CocoPharma::GovernanceMetric::VerificationAlertRate

### Rationale
Normalised alert rate by cause category measures whether investigation is producing elimination or merely correction, which is the difference the obligation turns on.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::AlertTriageAndRootCauseReduction

### Mechanism
CocoPharma::GovernanceMetric::VerificationAlertRate

### Rationale
The rate is the approach's own success measure, and its cause breakdown directs where the next root cause effort should go.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Mechanism
CocoPharma::GovernanceMetric::UploadReconciliationSuccessRate

### Rationale
First-attempt reconciliation success measures the obligation directly, and its discrepancy categories locate the failing link between line and repository.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::CentralisedSerialisationDataManagement

### Mechanism
CocoPharma::GovernanceMetric::UploadReconciliationSuccessRate

### Rationale
Reported separately for contract manufacturers, the rate exposes the quality of the external interfaces the centralised model depends on.

___

---

### 4.3 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Governance Driver 2
CocoPharma::Threat::SerialisationDataFailure

### Description
The two threats are in tension rather than merely adjacent. The control that defends against falsification generates the alerts that data failure corrupts, so effort spent reducing data failure directly increases the falsification defence — and a company that tolerates a high alert rate is degrading the protection for every other manufacturer in the same market.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Governance Driver 2
CocoPharma::Threat::ManufacturingQualityDeviation

### Description
Patients and prescribers cannot distinguish a falsified pack from a genuine one that failed in manufacture, so the two threats produce the same loss of confidence in the product and are managed together in recall and communication planning.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Governance Driver 2
CocoPharma::Regulation::UKMedicinesVerification

### Description
The UK arrangements are defined by departure from the EU system, so the two must be read together: what applies in Northern Ireland derives from the EU regime through the Windsor Framework, while Great Britain sits outside it, and the same production line serves both.

___

---

### 4.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Governance Policy 2
CocoPharma::GovernanceObligation::BatchRecordsCompleteAccurateRetained

### Description
Upload reconciliation compares repository confirmation against the pack count in the batch record, so the serialisation control depends on batch record completeness. An inaccurate produced-pack count makes the reconciliation meaningless while appearing to succeed.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::CentralisedSerialisationDataManagement

### Governance Policy 2
CocoPharma::GovernanceObligation::ComputerisedSystemsComplyWithElectronicRecordsRequirements

### Description
Batch release now depends on the serialisation system, which brings it within the validated GMP systems population and subjects it to the same validation, access control, and audit trail requirements as the batch record system itself.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::TradingPartnerDataExchange

### Governance Policy 2
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Description
DSCSA requires trading partners to be authorised to handle prescription medicines; the corporate obligation screens them for legitimacy and sanctions exposure. Both must clear before supply, and a partner may satisfy one and fail the other.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Governance Policy 2
CocoPharma::GovernancePrinciple::FullBatchTraceability

### Description
Traceability establishes where product went; market destination establishes where it was permitted to go and under which regime it was coded. Diversion is visible as a divergence between the two.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::BatchCertificationPerMarket

### Governance Policy 2
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Description
Certification and serialisation coding must agree on the market. A batch coded for one destination and certified for another cannot lawfully be supplied to either until the divergence is resolved, so the two records are reconciled before release.

___

---

## Part 5: Folio Membership

The definitions in this file join the Manufacturing Governance Lead Governance Folio, which is created in `manufacturing-governance-program.md` and already registered in the root collection.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Membership Rationale
EU medicines verification obligations are discharged by the manufacturing organisation under the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::UKMedicinesVerification

### Membership Rationale
UK verification arrangements, including the Northern Ireland position, are managed within manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Regulation::DrugSupplyChainSecurityAct

### Membership Rationale
DSCSA trading partner obligations are operated by manufacturing with commercial input on partner authorisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Threat::FalsifiedProductInSupplyChain

### Membership Rationale
Falsification of company product is a manufacturing and supply chain exposure owned by the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::Threat::SerialisationDataFailure

### Membership Rationale
Serialisation data defects blocking legitimate supply are owned by manufacturing as the originator of the data.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::SerialNumberUniquenessAbsolute

### Membership Rationale
Uniqueness enforcement at generation is a manufacturing control with no equivalent elsewhere in the organisation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernancePrinciple::MarketDestinationGovernsSerialisation

### Membership Rationale
Market allocation at packaging is set and controlled within manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::IdentifiersUploadedBeforeRelease

### Membership Rationale
Upload confirmation sits within the Qualified Person's release decision and is therefore a manufacturing obligation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::AggregationRelationshipsVerified

### Membership Rationale
Aggregation is performed in packing and warehousing and is owned by manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::VerificationAlertsInvestigated

### Membership Rationale
Alert investigation and escalation to competent authorities is performed by the serialisation team within manufacturing.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceObligation::TradingPartnerDataExchange

### Membership Rationale
Transaction data exchange is operated by manufacturing and distribution, with partner authorisation reconciled against corporate approval.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::CentralisedSerialisationDataManagement

### Membership Rationale
The central serialisation system is owned by manufacturing and validated as a GMP system.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceApproach::AlertTriageAndRootCauseReduction

### Membership Rationale
Triage and root cause reduction are operated by the Serialisation Data Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::VerificationAlertRate

### Membership Rationale
Alert rate by cause and market is reported to the Manufacturing Governance Lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ManufacturingGovernanceLead

### Element Id
CocoPharma::GovernanceMetric::UploadReconciliationSuccessRate

### Membership Rationale
Reconciliation success at release is reported to the Manufacturing Governance Lead and the Qualified Person.

### Membership Status
VALIDATED

___

---

## Part 6: Corporate Regulation Library Membership

The regulations defined in this file are placed in the Corporate Regulation Library so that they are discoverable alongside every other regulation the company is subject to, independently of the governance domain that owns them. The library folders are defined outside this workbook.

___

## Create Collection Folder

### Display Name
Medicines Verification Regulations

### Qualified Name
CollectionFolder::Coco::Medicines Verification Regulations

### Purpose
Groups the regulations governing unique identifiers, verification and supply chain traceability for medicinal products.

### Description
These regulations govern the medicine after it has been made — how each pack is identified, how that identity is reported and checked, and how the chain of custody through distribution is evidenced. They are pharmaceutical industry regulation but they are not manufacturing practice, which is why they sit in their own folder alongside Pharmaceutical Manufacturing Regulations rather than within it. The regimes differ sharply by market: the EU operates a central repository model, Great Britain sits outside it while Northern Ireland follows it, and the US requires interoperable exchange between trading partners instead — so the folder holds parallel instruments governing the same packs.

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
CollectionFolder::Coco::Pharmaceutical Industry Regulations

### Element Id
CollectionFolder::Coco::Medicines Verification Regulations

### Membership Rationale
Medicines verification is a branch of pharmaceutical industry regulation, so the folder sits inside the pharmaceutical industry folder alongside the manufacturing regulations rather than alongside it in the library.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Medicines Verification Regulations

### Element Id
CocoPharma::Regulation::EUFalsifiedMedicinesDirective

### Membership Rationale
The Falsified Medicines Directive and its Delegated Regulation govern medicines verification across the EU and are pharmaceutical industry regulations.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Medicines Verification Regulations

### Element Id
CocoPharma::Regulation::UKMedicinesVerification

### Membership Rationale
The UK medicines verification arrangements govern the same subject matter for Great Britain and Northern Ireland.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Medicines Verification Regulations

### Element Id
CocoPharma::Regulation::DrugSupplyChainSecurityAct

### Membership Rationale
The DSCSA governs US supply chain traceability for prescription medicines and belongs with the pharmaceutical industry regulations.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `manufacturing-governance-program.md` | MANUFACTURING-domain program — batch traceability, data integrity, computerised systems, and the folio these definitions join |
| `corporate-governance-program.md` | Approved third-party status, which must reconcile with DSCSA trading partner authorisation |
| `data-governance-program.md` | The single authoritative source obligation, of which serial number allocation is the strictest instance |
| `risk-register.md` | Counterfeit or substandard materials risk, which this program's controls mitigate on the outbound side |
| `joint-governance-officer-definitions.md` | Foundation definitions including the GMP regulation and the manufacturing governance role |
