# Coco Pharmaceuticals — Corporate Governance Program

> **Author:** Reggie Mint (Chief Financial Officer), Tom Tally (Accounts Manager), Sally Counter (Payments Clerk)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-22  
> **Description:** Governance definitions for the CORPORATE domain at Coco Pharmaceuticals. This file extends the foundation in `joint-governance-officer-definitions.md` — which defines the fraudulent supplier activity threat, the Chief Financial Officer governance role, and the Chief Financial Officer folio — with the financial control, third-party integrity, and anti-bribery governance the corporate domain is accountable for. Coco Pharmaceuticals is a US-listed issuer with subsidiaries in the UK and the EU, so US, UK, and EU regimes apply simultaneously across the group. It adds members to the existing folio rather than recreating it.

---

## Overview

The corporate governance domain covers the obligations Coco Pharmaceuticals carries as a company rather than as a manufacturer or a sponsor of clinical trials: that its reported figures are true, that the third parties it pays are who they claim to be, and that its dealings with the healthcare professionals who prescribe its products are transparent and defensible.

The group structure shapes all three. Coco Pharmaceuticals is listed in the United States and operates through subsidiaries in the UK and the EU, which means US securities and anti-corruption law reaches the whole group while UK and EU law applies to the subsidiaries directly. The practical consequence is that controls are designed once against the strictest applicable requirement rather than separately per jurisdiction, and that consolidation across entities reporting under different conventions is itself a significant source of control risk.

Two of these have been tested recently. A payments clerk noticing that a supplier's bank details had changed shortly before a large invoice was the first indication of an attempted supplier fraud, and the investigation that followed showed how much of the company's defence depended on one person's familiarity with a ledger rather than on a control. The governance definitions here are the response: making the checks systematic, making the supplier record authoritative, and making the evidence of both available without an investigation.

The third — transfers of value to healthcare professionals — is the obligation most specific to pharmaceuticals and the one where the reputational exposure is largest. A payment that is entirely legitimate but poorly recorded is indistinguishable, at the point a regulator or journalist asks, from one that is not.

This program covers three layers:

1. **Governance Drivers** — the regulations and business imperatives that motivate corporate governance activity, including those inherited from `joint-governance-officer-definitions.md`.
2. **Governance Policies** — the principles, obligations, and approaches defining how financial and third-party data is controlled.
3. **Governance Controls** — the roles, metrics, certification, and processing purposes that operationalise them.

All definitions in this file carry Domain Identifier `CORPORATE` and become members of the Chief Financial Officer Governance Folio, which already exists, is already assigned, and is already registered in the root collection.

The corporate domain depends heavily on the DATA domain for supplier master data integrity — the single authoritative source obligation in `data-governance-program.md` is a direct response to the supplier fraud threat owned here — and on the SECURITY domain for the access controls that make segregation of duties enforceable.

---

## Part 1: Governance Drivers — Corporate Domain

The fraudulent supplier activity threat (`CocoPharma::Threat::FraudulentSupplierActivity`) is defined in `joint-governance-officer-definitions.md` and is not restated here. The drivers below cover the financial reporting and anti-bribery exposures that were not represented at the joint level.

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Financial Reporting Integrity

### Qualified Name
CocoPharma::BusinessImperative::FinancialReportingIntegrity

### Domain Identifier
CORPORATE

### Summary
Coco Pharmaceuticals must be able to demonstrate that every externally reported financial figure reconciles to controlled source data through a documented, tested path.

### Description
External reporting is the point at which the company's data becomes a statement on which investors, lenders, and regulators rely, and the point at which errors stop being internal inconveniences and become misstatements. The integrity requirement is not merely that the figures are right; it is that the company can show why they are right — that each reported number traces to source transactions through transformations that are documented, access-controlled, and independently tested. Much of the risk sits in the last mile, where figures leave controlled systems and are assembled in spreadsheets for consolidation and disclosure. That final assembly is frequently the least controlled step in the chain and the most dependent on individual knowledge. Because the group consolidates UK and EU subsidiaries into a US-listed parent, that final assembly also spans currencies, local reporting conventions, and intercompany eliminations. As the revenue model shifts towards personalised treatments billed differently from conventional products, the consolidation becomes harder and the case for controlling it systematically becomes stronger.

### Implications
- Every reported figure must have a documented path to controlled source data
- Manual consolidation steps must be identified, controlled, and reduced over time
- Reporting transformations must be access-controlled and change-managed like any other production process
- The evidence that controls operated must be retained, not merely the result they produced

### Outcomes
- External reports withstand audit and regulatory scrutiny without retrospective reconstruction
- Errors are detected in the reporting chain rather than after publication
- The cost of the annual audit falls as evidence becomes available rather than assembled

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
A Trustworthy Third-Party Network

### Qualified Name
CocoPharma::BusinessImperative::TrustworthyThirdPartyNetwork

### Domain Identifier
CORPORATE

### Summary
Coco Pharmaceuticals must know who its suppliers, distributors, and service providers actually are, and must be able to show that each was assessed before money or materials moved.

### Description
The company pays several thousand third parties, and each represents an exposure that is financial, regulatory, and — in the case of material suppliers — a matter of patient safety. A supplier that is not who it claims to be can divert payments, introduce counterfeit materials into manufacturing, or implicate the company in bribery carried out on its behalf. The controls that prevent this are unglamorous and easily eroded: verifying identity and beneficial ownership at onboarding, screening against sanctions and politically exposed person lists, confirming bank details through a channel independent of the one that requested the change, and repeating the assessment periodically rather than treating onboarding as permanent. The recent attempted supplier fraud demonstrated that the company's defence rested on an individual noticing an anomaly rather than on a control detecting it, which is not a defence that scales or that survives staff turnover.

### Implications
- Third-party identity and beneficial ownership must be verified before onboarding, not after first payment
- Bank detail changes must be confirmed through an independently sourced channel
- Assessment must be periodic and risk-rated, not a one-off at onboarding
- The assessment evidence must be retained and retrievable for the life of the relationship

### Outcomes
- Fraudulent and sanctioned parties are detected by control rather than by chance
- Counterfeit material risk is reduced at its point of entry into the supply chain
- The company can evidence its due diligence to regulators and to its insurers

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

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
Improper Payments to Healthcare Professionals

### Qualified Name
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Domain Identifier
CORPORATE

### Summary
Payments, hospitality, or other transfers of value to healthcare professionals may be made, or may appear to have been made, in order to improperly influence prescribing or procurement decisions.

### Description
Pharmaceutical companies pay healthcare professionals for legitimate reasons — advisory boards, speaking engagements, clinical investigator fees, conference attendance — and every one of those payments is capable of being characterised as an inducement. The threat has two distinct forms and both matter. The first is actual corruption: a payment made to secure a prescribing or formulary decision, which exposes the company to criminal liability under the UK Bribery Act and equivalent legislation, with no requirement that the payment succeeded or that senior management knew. The second is apparent impropriety: a payment that was entirely legitimate but recorded so poorly that the company cannot demonstrate what it was for, which produces substantially the same reputational damage and regulatory attention. Because transfers of value are disclosed publicly in most jurisdictions, poor record-keeping is not a private failure — it is published. The exposure grows as the company's personalised medicine work brings it into closer and more frequent contact with individual clinicians.

### Implications
- Every transfer of value must have a recorded business purpose and a fair market value assessment
- Payments to healthcare professionals must be approved through a route independent of the commercial team benefiting from the relationship
- Records must be complete enough to withstand publication, since disclosure is mandatory
- Liability can arise from the conduct of agents and distributors acting on the company's behalf

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Financial Misstatement Through Uncontrolled Reporting Processes

### Qualified Name
CocoPharma::Threat::FinancialMisstatementFromUncontrolledReporting

### Domain Identifier
CORPORATE

### Summary
Externally reported figures may be materially wrong because they were assembled through manual steps that are undocumented, unreviewed, and dependent on individual knowledge.

### Description
Material misstatements rarely originate in the ledger. They originate in the layer above it — the consolidation spreadsheets, the manual journals posted late in the close, the mapping tables that allocate revenue between entities, the adjustments made to reconcile subsidiaries reporting under different conventions. These artefacts are frequently maintained by one person, are not subject to change control, carry no audit trail, and are trusted because they have produced plausible numbers for years. The threat is realised when a formula is extended incorrectly, a mapping is not updated after a reorganisation, or the person who understood the model leaves. It is compounded when the same uncontrolled artefacts are used to produce the figures that management relies on internally, so that the error is not caught by the business noticing that the reported result contradicts its own experience. Detection typically comes from the external auditor or, worse, from a restatement.

### Implications
- Manual reporting artefacts must be inventoried and brought under change control
- Late and manual journals must be reviewed independently of the person posting them
- Mapping and allocation tables must have owners and a defined update process
- Key-person dependency in the reporting chain must be identified and reduced

### Importance
High

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

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
UK Bribery Act 2010

### Qualified Name
CocoPharma::Regulation::UKBriberyAct2010

### Domain Identifier
CORPORATE

### Summary
UK legislation creating criminal offences for offering, receiving, and failing to prevent bribery, including a corporate offence for which the only defence is having adequate preventive procedures in place.

### Description
The Bribery Act creates four offences, of which section 7 — failure of a commercial organisation to prevent bribery — is the one that shapes governance most directly. Under section 7 the company is criminally liable when a person associated with it bribes another party intending to obtain business or a business advantage, whether or not the company knew, and whether or not the bribery succeeded. "Associated person" extends beyond employees to agents, distributors, and joint venture partners acting on the company's behalf, which is why third-party due diligence sits at the centre of the response. The only defence is proving that adequate procedures were in place, which makes the evidence of those procedures — the due diligence performed, the training delivered, the approvals recorded, the monitoring carried out — the substance of compliance rather than its documentation. The Act has extraterritorial reach: it applies to conduct anywhere in the world by an organisation carrying on business in the UK, which the UK subsidiaries do. It applies alongside the US Foreign Corrupt Practices Act rather than instead of it, and differs in two respects that matter — it covers commercial bribery as well as bribery of officials, and it provides no exception for facilitation payments. For a pharmaceutical company the principal exposure is in dealings with healthcare professionals and with public officials in procurement and licensing.

### Regulation Source
Bribery Act 2010 (UK), with Ministry of Justice guidance on adequate procedures

### Regulators
- Serious Fraud Office (SFO) — UK
- Crown Prosecution Service — UK

### Implications
- The company is liable for bribery by agents and distributors acting on its behalf
- The adequate procedures defence requires retained evidence, not merely a policy document
- Third-party due diligence must be proportionate to the risk each relationship presents
- Hospitality and transfers of value require recorded business purpose and approval

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Regulation

### Display Name
Sarbanes-Oxley Act Section 404 — Internal Control over Financial Reporting

### Qualified Name
CocoPharma::Regulation::SarbanesOxleySection404

### Domain Identifier
CORPORATE

### Summary
US legislation requiring management to assess and report on the effectiveness of internal control over financial reporting, with independent auditor attestation.

### Description
Section 404 requires management to establish, document, and annually assess the effectiveness of internal control over financial reporting, and requires the external auditor to attest to that assessment. Its governance significance is that it converts internal control from a matter of practice into a matter of evidence: a control that operates effectively but leaves no record of having operated cannot be tested and is treated as a deficiency. The assessment covers the controls over the systems that produce financial data, including access controls and change management for those systems, which is why it reaches into territory that would otherwise be purely IT. Deficiencies are classified by severity, and a material weakness must be publicly disclosed — a disclosure that reliably affects share price and management credibility. For Coco Pharmaceuticals the demanding areas are the manual consolidation steps in the close process — where UK and EU subsidiary results are translated and combined into the group position — and the controls over spreadsheets and end-user tools that participate in producing reported figures. The assessment scope is the consolidated group, so a control failure in a subsidiary is a group deficiency.

### Regulation Source
Sarbanes-Oxley Act of 2002, Section 404, with PCAOB Auditing Standard 2201

### Regulators
- Securities and Exchange Commission (SEC) — United States
- Public Company Accounting Oversight Board (PCAOB)

### Implications
- Controls must produce retained evidence that they operated, not merely operate
- Access and change management for financial systems fall within the assessment scope
- End-user computing tools participating in reporting must be identified and controlled
- Material weaknesses must be publicly disclosed

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Regulation

### Display Name
US Foreign Corrupt Practices Act

### Qualified Name
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Domain Identifier
CORPORATE

### Summary
US legislation prohibiting corrupt payments to foreign officials and requiring issuers to keep accurate books and records and maintain a system of internal accounting controls.

### Description
The FCPA applies to Coco Pharmaceuticals as a US-listed issuer, and it reaches the conduct of the UK and EU subsidiaries and of agents and distributors acting on the group's behalf anywhere in the world. It has two limbs, and the accounting limb is the one that most often produces enforcement. The anti-bribery provisions prohibit corrupt payments to foreign officials to obtain or retain business — a category that, in most of the markets the company sells into, includes physicians and administrators employed by state-owned or state-funded healthcare systems, which is what makes ordinary commercial interactions with prescribers a live FCPA question rather than a remote one. The accounting provisions require issuers to keep books and records that accurately and fairly reflect transactions, and to devise and maintain a system of internal accounting controls sufficient to provide reasonable assurance over them. Those provisions carry no materiality threshold and no requirement to prove that any bribe occurred: mischaracterising a payment in the ledger is itself a violation. This is why the FCPA and Section 404 are addressed together — the same control population serves both — and why the description recorded against a transfer of value is a compliance artefact rather than administrative detail.

### Regulation Source
Foreign Corrupt Practices Act of 1977, 15 U.S.C. §§ 78dd-1 et seq., with the FCPA Resource Guide issued by the DOJ and SEC

### Regulators
- Securities and Exchange Commission (SEC) — United States
- Department of Justice (DOJ) — United States

### Implications
- The Act reaches conduct by the UK and EU subsidiaries and by agents acting on the group's behalf
- Healthcare professionals employed by state healthcare systems may be foreign officials for FCPA purposes
- Mischaracterising a payment in the ledger violates the accounting provisions regardless of materiality or intent
- Successor liability attaches on acquisition, making pre-acquisition due diligence a governance requirement

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — CORPORATE Domain

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Segregation of Duties in Financial Processes

### Qualified Name
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Domain Identifier
CORPORATE

### Summary
No individual may control a financial transaction from initiation through approval to payment, and the system entitlements enforcing this must be assigned by role rather than accumulated by tenure.

### Description
Segregation of duties is the oldest financial control and the one most reliably eroded in practice. It is rarely dismantled deliberately; it decays as people cover absences, absorb the duties of departed colleagues, and accumulate entitlements across a long career that nobody revokes. The result is that a control the organisation believes is operating has quietly ceased to, and the discovery usually comes after a loss. This principle requires the incompatible duty combinations to be defined explicitly — creating a supplier and approving a payment to it, posting a journal and approving it, changing bank details and releasing funds — and requires system entitlements to be reviewed against those definitions rather than against what each person currently has. Where an unavoidable conflict exists in a small team, a compensating detective control is required and documented, not simply accepted. The attempted supplier fraud made the practical case: the combination that would have permitted it was entitlement drift rather than deliberate design.

### Implications
- Incompatible duty combinations must be defined explicitly and maintained as processes change
- Entitlement reviews must test against the definitions, not confirm existing access
- Unavoidable conflicts require a documented compensating detective control
- Temporary access granted for cover must expire automatically rather than persist

### Outcomes
- A single individual cannot complete a fraudulent transaction unaided
- Entitlement drift is detected by review rather than by loss
- The company can evidence that segregation operated, as required by Section 404

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Transfers of Value Must Be Transparent and Justifiable

### Qualified Name
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Domain Identifier
CORPORATE

### Summary
Every payment, hospitality, or benefit provided to a healthcare professional or public official must have a recorded business purpose, an assessed fair market value, and an approval independent of the commercial relationship it supports.

### Description
The test this principle applies is deliberately external: could the company explain this payment, on the day it is published, to a regulator or a journalist who is not inclined to be generous? That test is stricter than legality, and it is the right one, because transfers of value are disclosed publicly and the company does not control how they are read. Meeting it requires three things recorded at the time rather than reconstructed later — what the payment was for, why the amount was appropriate, and who approved it from outside the commercial team that benefits from the relationship. Fair market value assessment matters particularly for advisory and speaking fees, where the same activity can be compensated at a defensible rate or at one that invites inference. The principle extends to agents and distributors, since the company is liable for their conduct on its behalf and cannot discharge that liability by not asking.

### Implications
- Business purpose and fair market value must be recorded at the time of approval
- Approval must come from outside the commercial team benefiting from the relationship
- Agents and distributors must be bound to equivalent standards contractually and monitored
- Records must be complete enough to withstand publication

### Outcomes
- Legitimate payments can be defended when published
- Improper payments are prevented by independent approval rather than detected afterwards
- The adequate procedures defence under the Bribery Act is supported by evidence

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Reported Figures Must Reconcile to Controlled Source Data

### Qualified Name
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Domain Identifier
CORPORATE

### Summary
Every externally reported figure must trace to controlled source data through documented transformations, with manual steps identified, controlled, and progressively eliminated.

### Description
This principle addresses the last mile of reporting, where controlled ledger data is assembled into disclosed figures through steps that are frequently outside any control framework. It requires the path from source to disclosure to be documented as a chain — which systems, which transformations, which manual interventions — and requires each manual intervention to be justified, owned, and subject to review. The direction of travel is explicit: manual steps are not merely to be controlled but to be reduced, because a controlled manual step remains dependent on the individual performing it. Spreadsheets and end-user tools that participate in producing reported figures fall within scope and are treated as financial systems, with version control, access restriction, and change records, rather than as personal working files. The principle also serves the DATA domain's traceability work in the other direction: reporting is the use case that most clearly demonstrates why lineage for critical elements has to be automatic.

### Implications
- The path from source system to disclosed figure must be documented and maintained
- Spreadsheets participating in reporting are financial systems and are controlled as such
- Manual interventions require justification, ownership, and independent review
- Key-person dependencies in the reporting chain must be identified and reduced

### Outcomes
- Reported figures can be reconciled to source without retrospective investigation
- Audit evidence is available rather than assembled at year end
- Section 404 assessment scope is known rather than discovered during testing

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

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
Third Parties Must Be Screened Before Onboarding and Periodically Thereafter

### Qualified Name
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Domain Identifier
CORPORATE

### Summary
Every supplier, distributor, agent, and service provider must be identity-verified and screened against sanctions, politically exposed person, and adverse media sources before onboarding, and rescreened on a risk-based cycle.

### Description
Screening establishes that a third party is who it claims to be and is not a party the company is prohibited or ill-advised from dealing with. Identity verification covers legal entity existence, registered address, and beneficial ownership — the last being the step most often skipped and the one that reveals whether a supplier is connected to an employee, a competitor, or a sanctioned individual behind an intermediary. Screening covers sanctions lists, politically exposed persons, and adverse media, and must be repeated rather than performed once, since sanctions designations and ownership change while relationships persist. The cycle is risk-rated: a high-risk distributor in a jurisdiction with elevated corruption exposure is rescreened far more frequently than a domestic office supplier. Bank detail changes trigger a separate control regardless of screening status, verified through a channel independently sourced rather than one supplied in the change request — the control whose absence the recent attempted fraud exposed.

### Implications
- Beneficial ownership must be established, not just legal entity identity
- Rescreening frequency must follow the risk rating and be enforced by system, not by memory
- Bank detail changes require independent channel verification regardless of screening currency
- Screening evidence must be retained for the life of the relationship and beyond

### Outcomes
- Sanctioned and fraudulent parties are prevented from onboarding
- Connections between suppliers and employees are surfaced before payments begin
- The adequate procedures defence is supported by retained, dated evidence

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Internal Controls over Financial Reporting Must Be Documented and Tested

### Qualified Name
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Domain Identifier
CORPORATE

### Summary
Controls over financial reporting must be documented with their owner, frequency, and evidence, and must be tested annually with results and remediation recorded.

### Description
Section 404 requires an assessment, and an assessment requires a population to assess. This obligation establishes that population: each control over financial reporting is documented with what it does, who performs it, how often, what evidence it produces, and which risk it addresses. Testing then examines whether the control operated as documented throughout the period, not whether it operated on the day of testing. The distinction matters because the most common finding is not a control that fails but a control that operated without leaving evidence, which is indistinguishable from one that did not operate. Deficiencies are classified by severity and tracked to remediation with a named owner and a date, and a deficiency that recurs across periods is escalated rather than re-raised. The scope extends to the general IT controls the financial systems depend on — access provisioning, change management, and backup — because a financial control operating on a system with uncontrolled access provides no assurance.

### Implications
- Each control must produce retained evidence of having operated
- Testing must cover the whole period, not a point in time
- General IT controls over financial systems are within scope
- Recurring deficiencies must escalate rather than simply be re-raised

### Outcomes
- Management can make the Section 404 assertion on evidence rather than belief
- Auditor testing proceeds against a known population rather than a discovery exercise
- Control weaknesses are remediated with ownership and dates rather than noted

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Transfers of Value to Healthcare Professionals Must Be Recorded and Disclosed

### Qualified Name
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Domain Identifier
CORPORATE

### Summary
Every transfer of value to a healthcare professional or healthcare organisation must be recorded with recipient, amount, category, business purpose, and approver, and disclosed publicly within the required timeframe.

### Description
Disclosure regimes across the jurisdictions in which Coco Pharmaceuticals operates — Open Payments under the US Physician Payments Sunshine Act, the EFPIA Disclosure Code across the EU, and Disclosure UK — require transfers of value to healthcare professionals to be published, attributed to the named recipient where consent permits and in aggregate where it does not. Meeting the obligation is primarily a data problem rather than a policy one: the payments originate in several systems — accounts payable, expenses, event management, clinical trial site payments — and must be brought together, deduplicated, attributed to a correctly identified recipient, and categorised consistently. Recipient identification is the hardest part, since the same clinician may appear with different name spellings and affiliations across systems, and a payment attributed to the wrong person is both a disclosure failure and a personal injustice. The record must be complete at the point of payment rather than reconstructed at disclosure time, and the business purpose recorded must be specific enough to be meaningful when published.

### Implications
- Payments must be captured from every originating system, not only accounts payable
- Recipient identity must be resolved to a single authoritative record before disclosure
- Business purpose must be recorded at payment and specific enough to publish
- Recipients must be able to review their attributed transfers before publication

### Outcomes
- Disclosure obligations are met accurately and on time in every jurisdiction
- Payments are correctly attributed, avoiding both under-reporting and misattribution
- The company can respond to questions about any published transfer from its own records

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Material and Manual Journal Entries Must Be Independently Reviewed

### Qualified Name
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Domain Identifier
CORPORATE

### Summary
Manual journal entries above defined thresholds, and all entries posted during the closing period, must be reviewed and approved by someone other than the preparer, with the review evidenced.

### Description
Manual journals are the mechanism through which most financial statement fraud and most material error enters the accounts, because they bypass the transactional controls that govern ordinary postings. This obligation requires independent review of the entries that matter: those above a materiality threshold, those posted late in the close when scrutiny is lowest, those affecting judgemental areas such as provisions and revenue cut-off, and those posted by individuals who also hold approval rights elsewhere in the process. Review means examining the supporting documentation and the rationale, not confirming that the entry balances. The evidence of review is part of the control — an approval recorded in the system with the reviewer's identity and the date, not a verbal confirmation. Entries that recur period after period with the same description warrant particular attention, since a recurring manual adjustment usually indicates a systematic problem being papered over rather than a genuine one-off.

### Implications
- Thresholds and high-risk categories must be defined and configured in the ledger
- Review requires examination of supporting documentation, not arithmetic confirmation
- Reviewer identity and date must be recorded by the system, not maintained separately
- Recurring manual adjustments must be investigated for the underlying cause

### Outcomes
- Fraudulent and erroneous journals are detected before period close
- Systematic problems concealed by recurring adjustments are surfaced
- Section 404 evidence for journal controls is produced automatically

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

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
Risk-Rated Third-Party Due Diligence

### Qualified Name
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Domain Identifier
CORPORATE

### Summary
Third parties are risk-rated on jurisdiction, sector, public-official exposure, and spend, and the depth of due diligence and the rescreening frequency follow the rating.

### Description
Applying identical due diligence to every third party is both unaffordable and ineffective: it consumes the capacity that should be directed at the relationships that actually carry risk, and it produces a uniform file that demonstrates process rather than judgement. This approach rates each third party on the factors that predict exposure — the corruption risk of the jurisdiction it operates in, whether its work brings it into contact with public officials or healthcare professionals, whether it acts in the company's name, the materiality of the spend, and the nature of what it supplies. The rating then determines the depth of diligence at onboarding, the frequency of rescreening, and whether enhanced measures such as site visits, audit rights, or certified beneficial ownership documentation are required. Ratings are reviewed when the relationship changes materially, and a third party whose risk rating rises moves onto the enhanced cycle rather than continuing on the one it was onboarded under. The Ministry of Justice guidance on adequate procedures explicitly contemplates this proportionate approach, which is why documenting the rating rationale matters as much as the rating.

### Implications
- Rating factors must be defined, applied consistently, and the rationale recorded
- Diligence depth and rescreening frequency must be driven by rating, enforced systematically
- Rating changes must move the relationship onto the corresponding cycle
- Enhanced measures must include contractual audit rights for the highest-rated relationships

### Outcomes
- Due diligence effort concentrates where the exposure genuinely is
- The proportionality of the approach can be demonstrated as an adequate procedure
- Rising risk in an existing relationship is acted on rather than missed

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Annual Controls Testing and Certification Cycle

### Qualified Name
CocoPharma::GovernanceApproach::ControlsTestingAndCertificationCycle

### Domain Identifier
CORPORATE

### Summary
Financial controls are tested on a planned annual cycle, with process owners certifying operation each quarter and deficiencies tracked to remediation between cycles.

### Description
The cycle distributes what would otherwise be a year-end scramble across the year. Process owners certify quarterly that the controls they own operated as documented, which surfaces problems while there is still time to remediate them and makes ownership continuous rather than annual. Independent testing is planned across the year with the timing weighted towards the controls that matter most and those that failed previously. Deficiencies are logged with severity, owner, and remediation date, and tracked between cycles rather than reset. The value of quarterly certification lies in the specific claim it forces: a process owner who has to assert that a control operated throughout the quarter finds out whether it did, which is a different exercise from being told at year end that testing found a gap. Where certification reveals a control that has not operated, the disclosure is treated as the system working rather than as a failure to be penalised, since the alternative is certification that means nothing.

### Implications
- Process owners must certify quarterly, with the certification recorded and attributable
- Testing must be planned across the year, weighted by risk and prior failure
- Deficiencies persist across cycles until remediated, with owner and date
- Self-disclosed control failures must not be penalised, or certification becomes worthless

### Outcomes
- Control problems are found early enough to remediate before the assertion is due
- Ownership of controls is continuous rather than an annual event
- The Section 404 assessment rests on evidence accumulated through the year

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Continuous Transaction Monitoring

### Qualified Name
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Domain Identifier
CORPORATE

### Summary
Payment and journal transactions are monitored automatically against patterns indicating fraud, error, or control failure, with exceptions routed for investigation rather than reported after the period closes.

### Description
Detective controls that operate quarterly detect problems quarterly. Continuous monitoring runs the same logic against transactions as they occur: payments to newly created or recently modified supplier records, bank detail changes followed quickly by payment, duplicate invoice characteristics, round-sum amounts just below approval thresholds, payments to accounts matching employee bank details, journals posted outside working hours or by unusual users. Each rule produces exceptions rather than blocks, since most matches are legitimate, and the exceptions are routed to a named investigator with a defined response time. Rule performance is reviewed and tuned, because a rule producing large volumes of false positives is worse than no rule at all — it consumes attention and trains people to dismiss alerts. The approach is the systematic form of what a long-serving payments clerk does by intuition, and its purpose is to make that detection independent of any individual's tenure and familiarity.

### Implications
- Monitoring rules must be documented with the risk each addresses and reviewed for effectiveness
- Exceptions require named investigators and defined response times, not a queue
- False positive rates must be measured and tuned, since alert fatigue destroys the control
- Employee bank account comparison requires a recorded lawful basis and restricted access

### Outcomes
- Fraudulent payments are detected before funds leave rather than at reconciliation
- Detection no longer depends on individual familiarity with the ledger
- Control failures are visible continuously rather than at the next testing cycle

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — CORPORATE Domain

---

### 3.1 Governance Roles

The Chief Financial Officer role (`CocoPharma::GovernanceRole::ChiefFinancialOfficer`, held by Reggie Mint) is defined in `joint-governance-officer-definitions.md` and carries the corporate governance domain lead accountability. The roles below are the delegated positions through which it is discharged.

___

## Create Governance Role

### Display Name
Financial Controls Manager

### Qualified Name
CocoPharma::GovernanceRole::FinancialControlsManager

### Description
The Financial Controls Manager maintains the documented population of controls over financial reporting, plans and coordinates the annual testing cycle, collects quarterly process owner certifications, and tracks deficiencies to remediation. The role owns the relationship with the external auditor on control matters, maintains the inventory of end-user computing tools participating in reporting, and assesses the control impact of changes to financial systems and processes before they are made. It reports to the Chief Financial Officer and works with the Chief Information Security Officer on the general IT controls that financial controls depend on.

### Scope
Internal control over financial reporting — control documentation, testing cycle, process owner certification, deficiency remediation, and end-user computing inventory.

### Headcount
2

### Category
Governance Role

### Search Keywords
- internal control
- Sarbanes-Oxley
- controls testing
- financial reporting

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
Third-Party Risk Manager

### Qualified Name
CocoPharma::GovernanceRole::ThirdPartyRiskManager

### Description
The Third-Party Risk Manager owns the due diligence process for suppliers, distributors, agents, and service providers: risk rating, onboarding screening, periodic rescreening, and the enhanced measures applied to high-rated relationships. The role maintains the screening evidence that supports the adequate procedures defence, investigates exceptions raised by continuous monitoring against supplier records, and approves or refuses onboarding on risk grounds. It works with the Manufacturing Governance Lead on material supplier qualification, where commercial risk assessment and GMP qualification must reach a consistent conclusion about the same supplier.

### Scope
Third-party risk rating, due diligence, screening and rescreening, and the retained evidence supporting anti-bribery compliance.

### Headcount
3

### Category
Governance Role

### Search Keywords
- third-party risk
- due diligence
- sanctions screening
- supplier onboarding

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
Third-Party Screening Currency Rate

### Qualified Name
CocoPharma::GovernanceMetric::ThirdPartyScreeningCurrencyRate

### Domain Identifier
CORPORATE

### Summary
Measures the percentage of active third-party relationships whose screening is current against the frequency required by their risk rating.

### Description
Currency rather than coverage is the useful measure here. Nearly every active supplier will have been screened at some point, so a coverage figure approaches 100% and conceals the real exposure, which is screening that has lapsed on relationships that continue to receive payments. This metric compares each third party's last screening date against the interval its risk rating requires, so a high-risk distributor screened fourteen months ago counts as a failure while a low-risk supplier screened at the same time does not. Reporting is broken down by risk band, since a lapse in the high-risk band matters disproportionately and would be invisible in an aggregate. Relationships that are dormant but not closed are reported separately, because they represent a route by which a payment could be made to a party whose status has not been checked for years. Target is 100% currency in the high-risk band and 95% overall.

### Implications
- Requires risk rating and rescreening interval to be recorded per third party
- Must be measured against required interval, not as a coverage percentage
- Dormant-but-open relationships must be reported separately
- High-risk band must be reported distinctly, not absorbed into an average

### Outcomes
- Lapsed screening on active relationships is visible before a payment is made
- Effort concentrates on the risk band where a lapse actually matters
- The adequate procedures defence rests on current rather than historical evidence

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Internal Control Test Pass Rate

### Qualified Name
CocoPharma::GovernanceMetric::InternalControlTestPassRate

### Domain Identifier
CORPORATE

### Summary
Measures the percentage of tested financial controls that passed on first testing, with failures categorised by whether the control did not operate or operated without evidence.

### Description
The categorisation is what makes this metric useful. A control that did not operate is a process failure requiring the process to change; a control that operated but left no retained evidence is a design failure requiring the evidence to be captured. The two demand entirely different remediation and would be conflated in a single pass rate. Reporting therefore separates them and additionally identifies controls failing for the second or subsequent consecutive cycle, since a repeat failure indicates that the previous remediation was cosmetic. First-pass rate is used rather than post-remediation rate, because remediation before the assertion date is expected and a post-remediation figure would be near 100% and say nothing. General IT controls are reported as their own group, since a failure there potentially invalidates every financial control depending on the affected system. Target is 90% first-pass with zero repeat failures.

### Implications
- Failures must be categorised as non-operation versus absence of evidence
- Repeat failures across cycles must be identified and escalated
- General IT control results must be reported as a distinct group
- Measurement is first-pass, before remediation

### Outcomes
- Remediation addresses the actual cause rather than the symptom
- Cosmetic remediation is exposed by repeat failure tracking
- Control failures with system-wide consequence are visible immediately

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Transfer of Value Record Completeness

### Qualified Name
CocoPharma::GovernanceMetric::TransferOfValueRecordCompleteness

### Domain Identifier
CORPORATE

### Summary
Measures the percentage of transfers of value to healthcare professionals that carry a resolved recipient identity, a recorded business purpose, and an independent approval at the point of payment.

### Description
This metric is measured at payment rather than at disclosure, which is the point of the control. A gap found at disclosure time can only be closed by reconstruction — asking people months later what a payment was for — and reconstruction is exactly what the transparency principle exists to avoid. The three components are reported separately because they fail for different reasons: recipient resolution fails where a clinician appears differently across source systems, business purpose fails where a payment was processed as an ordinary invoice without the transfer-of-value workflow, and independent approval fails where the commercial team approved its own relationship. Reporting is broken down by originating system, since payments arriving from event management or clinical trial site payments typically show weaker completeness than those from accounts payable, and the remediation is system-specific. Target is 98% on all three components.

### Implications
- Measurement must occur at payment, not at disclosure preparation
- The three components must be reported separately, as their causes differ
- Reporting by originating system is required to locate the weakness
- Recipient resolution depends on an authoritative healthcare professional record

### Outcomes
- Disclosure is assembled from complete records rather than reconstructed
- Weak originating systems are identified and corrected
- Misattribution to the wrong clinician is prevented before publication

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Certification Type

___

## Create Certification Type

### Display Name
Approved Third-Party Status

### Qualified Name
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Domain Identifier
CORPORATE

### Summary
The status a supplier, distributor, agent, or service provider must hold before Coco Pharmaceuticals may transact with it, confirming that identity verification, screening, and risk-appropriate due diligence have been completed.

### Description
Approved status is the gate between due diligence and commercial activity. It is granted when identity and beneficial ownership have been verified, screening against sanctions, politically exposed person, and adverse media sources has returned an acceptable result, the risk rating has been assigned, and any enhanced measures required by that rating have been completed. The status carries an expiry aligned to the rescreening interval for the risk band, so that it lapses rather than persisting indefinitely, and a lapsed status blocks new purchase orders while leaving existing commitments to be managed deliberately rather than severed. Status may be suspended immediately where screening returns an adverse result, where a bank detail change fails independent verification, or where monitoring raises an exception pending investigation. For material suppliers the status is held jointly with GMP qualification, and neither the commercial nor the manufacturing assessment alone is sufficient to transact — a supplier may be commercially sound and not GMP-qualified, or qualified and commercially unacceptable.

### Scope
All third parties with which Coco Pharmaceuticals transacts — suppliers of materials and services, distributors, agents acting in the company's name, and contract research and manufacturing organisations.

### Implications
- No purchase order may be raised against a third party without current approved status
- Status expires on the rescreening interval rather than persisting indefinitely
- Status may be suspended immediately pending investigation of an exception
- Material suppliers require both commercial approval and GMP qualification

### Importance
Critical

### Category
Corporate Governance

### Authors
- Reggie Mint
- Tom Tally
- Sally Counter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.4 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to CORPORATE Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKBriberyAct2010

### Policy
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Rationale
The adequate procedures defence requires that payments capable of being read as inducements are justified and independently approved at the time. The principle states that requirement in operational terms.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKBriberyAct2010

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Rationale
Section 7 liability extends to bribery by associated persons. Screening third parties before they act in the company's name is the primary preventive procedure.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKBriberyAct2010

### Policy
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Rationale
Ministry of Justice guidance contemplates proportionate, risk-based due diligence. The rating approach is how proportionality is applied and evidenced.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::SarbanesOxleySection404

### Policy
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Rationale
Section 404 requires management to assess control effectiveness annually. The obligation establishes the documented population and the testing that makes an assessment possible.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::SarbanesOxleySection404

### Policy
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Rationale
Segregation of duties is a foundational control within the Section 404 scope, and one whose erosion is a common source of deficiency findings.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::SarbanesOxleySection404

### Policy
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Rationale
The assessment covers the whole path to the reported figure, including the end-user computing tools that produce it. The principle brings that last mile into scope explicitly.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::SarbanesOxleySection404

### Policy
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Rationale
Journal entry controls are examined directly in every Section 404 assessment because manual journals bypass transactional controls.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Policy
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Rationale
Both forms of the threat — actual impropriety and apparent impropriety through poor records — are addressed by recording purpose and approval at the point of payment.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Policy
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Rationale
Independent approval from outside the benefiting commercial team is the control that prevents the payment rather than documenting it afterwards.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FinancialMisstatementFromUncontrolledReporting

### Policy
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Rationale
The threat originates in uncontrolled manual assembly above the ledger. The principle brings that layer under documentation and change control.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FinancialMisstatementFromUncontrolledReporting

### Policy
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Rationale
Manual journals are the mechanism through which most material misstatement enters the accounts; independent review is the control that intercepts it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FraudulentSupplierActivity

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Rationale
Screening and beneficial ownership verification prevent a fraudulent party from being onboarded, and independent bank detail verification prevents diversion once it is.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FraudulentSupplierActivity

### Policy
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Rationale
Monitoring makes detection systematic rather than dependent on an individual noticing an anomaly, which is what the recent attempted fraud showed the company was relying on.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FraudulentSupplierActivity

### Policy
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Rationale
Supplier fraud requires the ability to create or amend a supplier record and to cause payment against it. Segregation removes that combination.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::FinancialReportingIntegrity

### Policy
CocoPharma::GovernanceApproach::ControlsTestingAndCertificationCycle

### Rationale
The imperative requires demonstrable integrity. The testing and certification cycle is how the demonstration is accumulated through the year rather than assembled at its end.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::TrustworthyThirdPartyNetwork

### Policy
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Rationale
Knowing who the company's third parties are, proportionate to the risk each presents, is the imperative expressed as an operating method.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::TrustworthyThirdPartyNetwork

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Rationale
The obligation is the enforceable form of the imperative: verification and screening before money or materials move.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Rationale
Physicians in state-funded healthcare systems may be foreign officials for FCPA purposes, which makes recorded business purpose and independent approval of every transfer of value an anti-bribery control rather than a disclosure formality.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Rationale
FCPA liability attaches to payments made through agents and distributors. Screening and beneficial ownership verification before onboarding is the preventive control, and it must extend to the UK and EU subsidiaries' own third parties.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Rationale
The accounting provisions require a system of internal accounting controls sufficient to provide reasonable assurance over transactions. The documented and tested control population is that system.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Rationale
The books and records provisions carry no materiality threshold, so a mischaracterised journal is a violation in itself. Independent review of manual entries is the control that catches mischaracterisation.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Rationale
An accurately described payment in the ledger is what distinguishes a legitimate advisory fee from a books and records violation. Recording purpose at payment is the FCPA accounting control as much as the disclosure one.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Policy
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Rationale
Risk rating that weights jurisdiction corruption exposure and public-official contact is how FCPA diligence is directed at the relationships that actually carry the exposure across the group.

___

---

### 4.2 Governance Mechanisms — CORPORATE Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Mechanism
CocoPharma::GovernanceMetric::ThirdPartyScreeningCurrencyRate

### Rationale
Currency against the required interval measures the obligation as written, where a simple coverage figure would conceal lapsed screening on active relationships.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Mechanism
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Rationale
Approved status is the gate that enforces the obligation: without current status no purchase order may be raised.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Mechanism
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Rationale
The risk rating determines the depth of diligence required before status is granted and the interval at which it expires.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Mechanism
CocoPharma::GovernanceMetric::InternalControlTestPassRate

### Rationale
The pass rate measures the testing the obligation requires, and its categorisation distinguishes controls that did not operate from those that left no evidence.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::ControlsTestingAndCertificationCycle

### Mechanism
CocoPharma::GovernanceMetric::InternalControlTestPassRate

### Rationale
First-pass results, with repeat failures identified, are the feedback signal telling the cycle whether previous remediation was substantive.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Mechanism
CocoPharma::GovernanceMetric::TransferOfValueRecordCompleteness

### Rationale
Measured at payment rather than at disclosure, the metric tests whether the obligation is met at the point where a gap can still be closed without reconstruction.

___

---

### 4.3 Peer Driver Links — Related CORPORATE Drivers

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::TrustworthyThirdPartyNetwork

### Governance Driver 2
CocoPharma::Threat::FraudulentSupplierActivity

### Description
The threat is the failure mode the imperative exists to prevent. Holding them as peers keeps the positive objective and the specific attack visible together.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::FinancialReportingIntegrity

### Governance Driver 2
CocoPharma::Threat::FinancialMisstatementFromUncontrolledReporting

### Description
The imperative describes the assurance required; the threat describes precisely where it breaks down — in the manual layer above the ledger rather than in the ledger itself.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::UKBriberyAct2010

### Governance Driver 2
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Description
The Act creates the liability; the threat describes the conduct that triggers it in a pharmaceutical context, where routine legitimate payments to prescribers are unavoidable.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Governance Driver 2
CocoPharma::Regulation::UKBriberyAct2010

### Description
The two anti-bribery regimes apply simultaneously to the group: the FCPA through the US listing, the Bribery Act through the UK subsidiaries and UK business. They differ in detail — the Bribery Act covers commercial as well as official bribery and has no facilitation payment exception — so controls are designed against the stricter of the two on each point rather than against either alone.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Governance Driver 2
CocoPharma::Regulation::SarbanesOxleySection404

### Description
The FCPA accounting provisions and Section 404 address the same control population from different directions: Section 404 asks whether controls over financial reporting are effective, the FCPA asks whether books and records accurately reflect transactions. A single control programme serves both, and a deficiency in one is usually a deficiency in the other.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Governance Driver 2
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Description
Where prescribers are employed by state healthcare systems, an improper payment is both a bribery offence and an FCPA foreign official violation. The threat is the conduct; the Act is one of the two regimes that penalises it.

___

---

### 4.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Governance Policy 2
CocoPharma::GovernanceObligation::AllUsersMustBeAuthenticatedAndAccountable

### Description
Segregation is enforced through system entitlements, which depend entirely on individual authentication. Shared accounts dissolve segregation without any entitlement appearing to change.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Description
The consolidated transfer of value record is a financial profile of a named individual and must be classified and protected internally, notwithstanding that parts of it are published.

___

---


## Part 5: External Reference Links — CORPORATE Domain

___

## Create External Reference

### Display Name
Ministry of Justice — Bribery Act 2010 Guidance

### Qualified Name
CocoPharma::ExternalReference::MOJ::BriberyActGuidance

### Description
The UK Ministry of Justice guidance on procedures that commercial organisations can put in place to prevent bribery, issued under section 9 of the Bribery Act 2010. It sets out the six principles — proportionate procedures, top-level commitment, risk assessment, due diligence, communication, and monitoring and review — against which the adequate procedures defence is assessed.

### URL
https://www.gov.uk/government/publications/bribery-act-2010-guidance

### Reference Title
Bribery Act 2010: guidance to help commercial organisations prevent bribery

### Category
Regulatory Guidance

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create External Reference

### Display Name
US Securities and Exchange Commission

### Qualified Name
CocoPharma::ExternalReference::SEC::HomePage

### Description
The US Securities and Exchange Commission is the regulator responsible for enforcing federal securities law, including the internal control over financial reporting requirements of the Sarbanes-Oxley Act and the disclosure obligations that apply to Coco Pharmaceuticals' US-listed activities.

### URL
https://www.sec.gov/

### Reference Title
U.S. Securities and Exchange Commission

### Category
Regulator

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::UKBriberyAct2010

### External Reference
CocoPharma::ExternalReference::MOJ::BriberyActGuidance

### Description
The Ministry of Justice guidance defines the six principles against which the adequate procedures defence is judged, and is the primary source for the proportionality of the due diligence approach adopted here.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::SarbanesOxleySection404

### External Reference
CocoPharma::ExternalReference::SEC::HomePage

### Description
The SEC enforces the Section 404 internal control reporting requirement and publishes the interpretive guidance management relies on in making its annual assessment.

___

---

___

## Link External Reference

### Element Name
CocoPharma::Regulation::ForeignCorruptPracticesAct

### External Reference
CocoPharma::ExternalReference::SEC::HomePage

### Description
The SEC co-enforces the FCPA with the Department of Justice and, with the DOJ, publishes the FCPA Resource Guide that sets out enforcement expectations for issuers.

___

---

## Part 6: Chief Financial Officer Folio Membership

The Chief Financial Officer Governance Folio is created in `joint-governance-officer-definitions.md`, is already assigned to Reggie Mint, and is already registered in the root collection. This file adds the corporate-domain definitions to it. The fraudulent supplier activity threat is already a member and is not re-added.

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::BusinessImperative::FinancialReportingIntegrity

### Membership Rationale
The CFO is accountable for the integrity of externally reported figures and for the Section 404 assertion that rests on it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::BusinessImperative::TrustworthyThirdPartyNetwork

### Membership Rationale
Third-party integrity spans procurement, finance, and manufacturing, and is coordinated by the CFO as corporate governance domain lead.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Threat::ImproperPaymentsToHealthcareProfessionals

### Membership Rationale
Anti-bribery exposure arising from payments to prescribers is a corporate liability owned by the CFO.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Threat::FinancialMisstatementFromUncontrolledReporting

### Membership Rationale
Misstatement risk originating in the manual reporting layer is owned by the CFO and drives the controls programme.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Regulation::UKBriberyAct2010

### Membership Rationale
The Bribery Act creates corporate criminal liability for which the CFO coordinates the adequate procedures response.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Regulation::SarbanesOxleySection404

### Membership Rationale
The Section 404 assessment is made by management under the CFO's leadership.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Membership Rationale
Segregation of duties across financial processes is defined and enforced under the CFO's authority.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernancePrinciple::TransfersOfValueTransparentAndJustifiable

### Membership Rationale
The standard applied to payments to healthcare professionals is set by the CFO independently of the commercial teams.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Membership Rationale
Traceability from source data to disclosed figure is a finance responsibility supported by the DATA domain's lineage work.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Membership Rationale
Screening before onboarding is the corporate domain's principal preventive control against fraud and bribery.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceObligation::InternalControlsDocumentedAndTested

### Membership Rationale
The documented control population and its testing are maintained under the CFO's authority.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceObligation::TransfersOfValueRecordedAndDisclosed

### Membership Rationale
Disclosure obligations across jurisdictions are discharged by the finance team on behalf of the company.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceObligation::MaterialJournalEntriesReviewed

### Membership Rationale
Journal review thresholds and the independence of review are set by the CFO.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceApproach::ThirdPartyDueDiligenceAndRiskRating

### Membership Rationale
The risk-rating method is the documented basis for the proportionality of the company's anti-bribery procedures.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceApproach::ControlsTestingAndCertificationCycle

### Membership Rationale
The annual testing and quarterly certification cycle is operated by the finance controls team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceApproach::ContinuousTransactionMonitoring

### Membership Rationale
Transaction monitoring is operated by finance with exceptions investigated by the third-party risk team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceMetric::ThirdPartyScreeningCurrencyRate

### Membership Rationale
Screening currency by risk band is reported to the CFO and to the audit committee.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceMetric::InternalControlTestPassRate

### Membership Rationale
Control test results underpin the Section 404 assertion and are reported to the CFO and audit committee.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::GovernanceMetric::TransferOfValueRecordCompleteness

### Membership Rationale
Record completeness at payment determines whether disclosure can be assembled without reconstruction.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::CertificationType::ApprovedThirdPartyStatus

### Membership Rationale
Approved status is granted, suspended, and withdrawn under the CFO's authority through the third-party risk team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Risk::FraudulentSupplierOnboarding

### Membership Rationale
Defined in the risk register with domain identifier CORPORATE, this risk is owned by the CFO and mitigated by the screening obligation and monitoring approach.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Risk::CounterfeitMaterialsInManufacturing

### Membership Rationale
Defined in the risk register with domain identifier CORPORATE, this risk is jointly managed with manufacturing, with third-party approval as the corporate-side control.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefFinancialOfficer

### Element Id
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Membership Rationale
The FCPA applies to the group through the US listing and reaches the UK and EU subsidiaries. The CFO coordinates the compliance response across both its anti-bribery and accounting provisions.

### Membership Status
VALIDATED

___

---

## Part 7: Corporate Regulation Library Membership

The regulations defined in this file are placed in the Corporate Regulation Library so that they are discoverable alongside every other regulation the company is subject to, independently of the governance domain that owns them. The library folders are defined outside this workbook.

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Financial Regulations

### Element Id
CocoPharma::Regulation::UKBriberyAct2010

### Membership Rationale
The Bribery Act is a financial and commercial conduct regulation carrying corporate criminal liability, and sits with the other regulations the finance function is accountable for.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Financial Regulations

### Element Id
CocoPharma::Regulation::SarbanesOxleySection404

### Membership Rationale
Section 404 governs internal control over financial reporting and belongs with the financial regulations applying to the US-listed parent.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Financial Regulations

### Element Id
CocoPharma::Regulation::ForeignCorruptPracticesAct

### Membership Rationale
The FCPA's accounting provisions make it a financial regulation as much as an anti-corruption one, and it is enforced by the same regulator as Section 404.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `joint-governance-officer-definitions.md` | Foundation definitions — the fraudulent supplier activity threat, the Chief Financial Officer role and folio, and the authentication obligation referenced in Part 4.4 |
| `risk-register.md` | The two CORPORATE-domain risks added to the folio in Part 6, and the manufacturing risks that counterfeit materials feed into |
| `data-governance-program.md` | DATA-domain program. Its single authoritative source obligation is the counterpart control to third-party screening, and its lineage principle supports financial reconciliation |
| `manufacturing-governance-program.md` | MANUFACTURING-domain program. Material supplier qualification is the GMP-side assessment that pairs with commercial approved third-party status |
| `privacy-governance-program.md` | PRIVACY-domain program. Assures the lawful basis for the two processing purposes declared here |
| `data-security-strategy.md` | SECURITY-domain program. Provides the access controls and entitlement reviews on which segregation of duties depends |
