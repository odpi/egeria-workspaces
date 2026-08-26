# Coco Pharmaceuticals — Human Resource Management Governance

> **Author:** Faith Broker (Chief Privacy Officer / Head of Human Resources)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-23  
> **Description:** Governance definitions for the Human Resource Management domain at Coco Pharmaceuticals, domain identifier `22`. The file registers the domain identifier itself as a valid metadata value before any definition claims it, then defines the drivers, policies, and controls for the domain. Load `joint-governance-officer-definitions.md` first.

---

## Overview

Human Resource Management is established here as a governance domain in its own right. It sits alongside the domains that carry business and regulatory responsibility rather than among those that serve them: HR decisions create obligations to individuals and to regulators, and the consequences of getting them wrong fall on the organisation directly.

The domain has an unusual dual character. Outward, it answers to employment law that differs across the US parent and the UK and EU subsidiaries, and to pay transparency obligations that are among the most data-intensive reporting duties the company carries. Inward, it supplies data that several other domains depend on absolutely: manufacturing cannot certify a batch without evidence that the operator was qualified, drug development cannot show GCP compliance without site staff training records, and security cannot revoke access to someone it has not been told has left. Those dependencies are what make HR a governance domain rather than an administrative function.

The boundary with the privacy domain is deliberate and worth stating. Privacy owns the lawful basis, the data subject rights, and the retention framework for all personal data including employees'. HR owns the employment purposes that data is processed for and the decisions taken on it. Where this file declares processing purposes, it declares HR's own — as every domain does — with privacy assuring the basis rather than declaring it on HR's behalf.

The first act is to register the domain identifier. Egeria resolves `domainIdentifier` through a valid value set that deployments extend without rebuilding, so a value used before it is registered will not resolve to a name. Registering `22` first means every subsequent definition in this file — and in any other file adopting the domain — displays as Human Resource Management rather than as a bare number.

---

## Part 1: Domain Registration

The command below extends the `domainIdentifier` valid value set with the Human Resource Management domain.

**Type Name is deliberately omitted.** The template applies a valid value to all open metadata types when Type Name is left unset, which is what is wanted here: `domainIdentifier` is a property of governance definitions, governance roles, governance zones, and several other types, and the domain means the same thing in each. Setting a type name would restrict the value to one of them.

___

## Setup Valid Metadata Value

### Metadata Property Name
domainIdentifier

### Preferred Value
22

### Metadata Display Name
Human Resource Management

### Metadata Description
The governance domain for human resources encompasses the policies, practices, and structures that guide and oversee the management of an organization's human resources. It ensures that HR decisions, such as hiring, compensation, and terminations, are made within a clear and consistent system, not left to personal discretion. This framework is essential for maintaining institutional trust, supporting ethical practice, and ensuring compliance with corporate governance, risk management, and regulatory obligations.

___

---

## Part 1: Governance Drivers — Human Resource Management

The organisation-wide threat of losing key talent and knowledge (`CocoPharma::Threat::LossOfKeyTalentAndKnowledge`) is defined in `joint-governance-officer-definitions.md`. The drivers below cover the employment-specific exposures that were not represented at the joint level.

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
Workforce Capability for the Personalised Medicine Transition

### Qualified Name
CocoPharma::BusinessImperative::WorkforceCapabilityTransition

### Domain Identifier
22

### Summary
Coco Pharmaceuticals must know what capabilities its workforce holds, what the personalised medicine transition requires, and how to close the difference — before the shortfall constrains the programme.

### Description
The move to personalised, on-demand manufacturing changes what the company needs people to be able to do. Cell and gene handling, real-time release methods, decentralised trial conduct, and manufacturing at batch-of-one scale all require competencies the current workforce holds unevenly and in some cases not at all. The constraint is rarely headcount; it is the specific qualification that permits a named individual to perform a regulated step, and which cannot be conjured at short notice because it requires training, supervised practice, and assessment. This imperative treats workforce capability as something to be measured against a defined requirement rather than assumed from job titles and long service. It requires the company to hold an accurate picture of what capabilities exist, where they are concentrated, and where a single individual is the only person qualified to do something the business depends on — because that last case is a business continuity exposure wearing an HR label.

### Implications
- Capability requirements must be defined for the roles the transition depends on, not inferred from job titles
- The organisation must be able to identify activities where only one person is qualified
- Capability gaps must be visible early enough for training and assessment to close them
- Workforce planning must treat qualification lead time as a real constraint on programme timelines

### Outcomes
- Programme plans reflect when qualified people will actually be available
- Single points of qualification are identified and addressed before they cause disruption
- Training investment is directed at the capabilities the strategy requires

### Importance
High

### Category
Human Resource Management

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Business Imperative

### Display Name
Employment Decisions the Company Can Explain

### Qualified Name
CocoPharma::BusinessImperative::ExplicableEmploymentDecisions

### Domain Identifier
22

### Summary
Coco Pharmaceuticals must be able to explain any hiring, promotion, pay, or termination decision by reference to recorded, job-related criteria applied consistently.

### Description
Employment decisions are challenged — by individuals at tribunal, by regulators conducting equality audits, and increasingly by employees exercising the right to ask how their pay compares with colleagues doing equivalent work. The company's position in each case rests on what was recorded at the time, and a decision that was entirely fair but poorly documented is very difficult to defend years later against a contemporaneous account from the individual. The imperative is therefore about the record as much as the decision: criteria defined before the decision rather than justified after it, applied consistently across comparable cases, and retained in a form that can be produced. It also has a systemic dimension that individual case records cannot address. Decisions that are each defensible in isolation can produce a pattern that is not, and only aggregate analysis reveals it. Getting this right is a matter of institutional trust as much as legal exposure: a workforce that believes decisions are made on merit behaves differently from one that does not.

### Implications
- Decision criteria must be defined before the decision, not reconstructed to justify it
- Comparable cases must be identifiable so that consistency can be tested
- Records must survive long enough to answer challenges brought years afterwards
- Aggregate patterns must be analysed, since individually defensible decisions can aggregate badly

### Outcomes
- Challenges are answered from records rather than from recollection
- Inconsistency is detected internally before it is raised externally
- Employees can be given a substantive answer when they ask why a decision was made

### Importance
Critical

### Category
Human Resource Management

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
Unqualified Personnel Performing Regulated Activities

### Qualified Name
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Domain Identifier
22

### Summary
An individual may perform a GMP or GCP regulated activity for which their qualification has lapsed, was never recorded, or does not cover the specific task, invalidating the work and the records it produced.

### Description
Regulated activities may only be performed by people qualified to perform them, and the evidence of that qualification is an HR record. When the record is wrong the consequence lands on another domain: a batch certified on the signature of an operator whose qualification had expired is a GMP finding against manufacturing, and a trial procedure performed by untrained site staff is a GCP finding against drug development. Neither domain can detect the problem, because both reasonably rely on HR's record being current. The threat materialises through ordinary administrative drift rather than misconduct — a requalification date missed during a busy period, a transfer to a new area where the previous authorisation does not apply, a temporary cover arrangement that outlives its intended duration, training completed but recorded weeks later so that the record shows a gap that did not exist. It is aggravated by the fact that the work is usually done correctly: the product is fine, the trial data is sound, and what fails is the ability to demonstrate that the person was permitted to produce it.

### Implications
- Qualification currency must be enforced by system rather than tracked by memory
- Role and area changes must trigger reassessment of what the individual is authorised to do
- Temporary cover arrangements require an expiry, not an intention to review
- Delayed recording of completed training creates apparent gaps that are indistinguishable from real ones

### Importance
Critical

### Category
Human Resource Management

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Inconsistent or Discriminatory Employment Decisions

### Qualified Name
CocoPharma::Threat::InconsistentEmploymentDecisions

### Domain Identifier
22

### Summary
Employment decisions may be taken inconsistently across comparable cases, producing outcomes that disadvantage particular groups and that the company cannot defend when challenged.

### Description
Discrimination in a company of this size is rarely a decision anyone recognises as discriminatory. It emerges from many individually reasonable decisions taken by different managers against criteria they each interpreted slightly differently, and it becomes visible only in aggregate — a promotion rate that differs by group, a starting salary distribution that diverges at the point of hire and never converges, a pattern in who is selected for development opportunities. Because no single decision looks wrong, the problem is invisible to case-by-case review and is usually first identified by someone outside the company: a claimant's solicitor, a regulator, or a journalist working from published pay gap data. The exposure is rising as pay transparency obligations require more to be published and give individuals the right to ask how their pay compares with colleagues doing equal work, which converts an internal analytical question into an external one the company must be prepared to answer accurately.

### Implications
- Aggregate analysis is required, since case-by-case review cannot detect the pattern
- Criteria interpreted differently by different managers produce divergence without intent
- Starting salary decisions have persistent effects and warrant particular scrutiny
- Individuals will increasingly ask comparative pay questions the company must answer accurately

### Importance
Critical

### Category
Human Resource Management

### Authors
Faith Broker

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
UK Equality Act 2010

### Qualified Name
CocoPharma::Regulation::UKEqualityAct2010

### Domain Identifier
22

### Summary
UK legislation prohibiting discrimination on protected characteristics in employment, requiring equal pay for equal work, and imposing annual gender pay gap reporting on larger employers.

### Description
The Equality Act consolidates UK discrimination law and applies to every stage of the employment relationship at the UK subsidiaries — recruitment, terms, promotion, training access, dismissal, and matters arising after employment ends. Two features drive data governance requirements specifically. The equal pay provisions imply a right to compare, which means the company must be able to identify work of equal value across different job titles and departments and to explain any pay difference by reference to a material factor that is not a protected characteristic; that explanation must rest on recorded reasoning rather than on reconstruction. Separately, gender pay gap reporting requires publication of defined statutory measures each year, calculated on a prescribed basis from a snapshot date, which makes payroll data quality a public matter. Indirect discrimination is the provision most often engaged in practice: a criterion applied uniformly may still be unlawful if it disadvantages a protected group and cannot be objectively justified, and identifying that requires analysing outcomes rather than intentions.

### Regulation Source
Equality Act 2010 (UK), with the Equality Act 2010 (Gender Pay Gap Information) Regulations 2017

### Regulators
- Equality and Human Rights Commission (EHRC) — UK
- Employment Tribunals — UK

### Implications
- Work of equal value must be identifiable across differing job titles and departments
- Pay differences must be explicable by recorded material factors unrelated to protected characteristics
- Statutory pay gap measures must be calculated on the prescribed basis and published annually
- Indirect discrimination requires outcome analysis, since uniform application is not a defence

### Importance
Critical

### Category
Human Resource Management

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
EU Pay Transparency Directive (EU) 2023/970

### Qualified Name
CocoPharma::Regulation::EUPayTransparencyDirective

### Domain Identifier
22

### Summary
EU directive requiring pay transparency before and during employment, individual rights to comparative pay information, gender pay gap reporting, and joint pay assessment where an unjustified gap persists.

### Description
Directive (EU) 2023/970 goes considerably further than reporting. It requires pay ranges to be disclosed to applicants before interview and prohibits asking candidates about pay history, which removes a mechanism by which existing pay differences propagate into new appointments. It gives employees the right to request information on their individual pay level and on average pay levels broken down by sex for categories of workers doing the same work or work of equal value, and requires that request to be answered within two months. Employers must report gender pay gap data, and where reporting shows a gap of at least five per cent in any category of workers that cannot be justified by objective gender-neutral criteria and is not remedied within six months, a joint pay assessment must be conducted with worker representatives. For Coco Pharmaceuticals the demanding requirement is categorisation: the company must be able to group workers by same or equal-value work using objective criteria including skills, effort, responsibility and working conditions, consistently across the EU subsidiaries. That grouping is a data modelling exercise, and it determines every figure that follows.

### Regulation Source
Directive (EU) 2023/970 on pay transparency and enforcement mechanisms, as transposed in each member state

### Regulators
- National equality bodies in EU member states
- National labour inspectorates and courts

### Implications
- Pay ranges must be available to applicants and pay history questions are prohibited
- Individual comparative pay requests must be answered within two months
- Workers must be categorised by equal-value work on objective, documented criteria
- An unjustified gap of five per cent or more triggers a joint pay assessment if not remedied
- The burden of proof shifts to the employer where pay transparency obligations have not been met

### Importance
Critical

### Category
Human Resource Management

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — Human Resource Management

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Employment Decisions Rest on Recorded, Job-Related Criteria

### Qualified Name
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Domain Identifier
22

### Summary
The criteria for any employment decision are defined before the decision is taken, applied consistently across comparable cases, and recorded with the reasoning at the time.

### Description
Defining criteria in advance is what separates a judgement from a rationalisation, and the sequence matters more than the content: criteria written after a decision will always fit it. This principle requires the criteria for hiring, promotion, pay setting, development selection, and termination to exist before the decision, to be job-related rather than personal, and to be recorded alongside the reasoning that applied them to the individual case. Recording the reasoning is the part most often omitted and the part that matters most on challenge, because the criteria alone do not show how they were weighed. The principle also requires comparable cases to be identifiable, since consistency cannot be demonstrated without knowing what to compare against — which in practice means decisions must be recorded in a structured form rather than in free text scattered across correspondence. Where a decision departs from the criteria for a legitimate reason, the departure is recorded as such rather than being accommodated by reinterpreting the criteria.

### Implications
- Criteria must exist before the decision, in a form that cannot be retrospectively adjusted
- The reasoning applying criteria to the individual case must be recorded, not only the outcome
- Decisions must be recorded in structured form so comparable cases can be identified
- Justified departures from criteria are recorded as departures, not as reinterpretation

### Outcomes
- The company can explain any individual decision from contemporaneous records
- Consistency across managers and departments is testable rather than assumed
- Employees receive substantive reasons rather than conclusions

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
Qualification Records Are Authoritative and Current

### Qualified Name
CocoPharma::GovernancePrinciple::QualificationRecordsAuthoritative

### Domain Identifier
22

### Summary
The HR qualification record is the single authoritative statement of what an individual is permitted to do, and other domains rely on it rather than maintaining their own.

### Description
Manufacturing, drug development, and security each need to know what an individual is authorised to do, and each would maintain its own list if HR's record were not trustworthy — which is how organisations end up with four partially-correct answers to the same question. This principle establishes the HR record as authoritative and accepts the obligations that come with that status: it must be current rather than periodically reconciled, it must reflect authorisation at a point in time and not only today, and it must be queryable by the systems that depend on it rather than available on request. Point-in-time capability is the requirement most often missed and the one inspections turn on, because the question asked is never whether an operator is qualified now but whether they were qualified on the date they signed. The principle also means that when the record and reality diverge, the record is corrected through a controlled process rather than worked around locally, since a local workaround leaves every dependent domain relying on something known to be wrong.

### Implications
- Other domains consume the HR record rather than maintaining parallel lists
- The record must support point-in-time queries, not only current state
- Currency is maintained continuously, not restored by periodic reconciliation
- Divergence between record and reality is corrected in the record, not worked around

### Outcomes
- Manufacturing and drug development can evidence personnel qualification from one source
- Inspection questions about historical authorisation are answerable
- The organisation holds one answer to what an individual may do, not several

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
Pay Structures Must Be Explicable

### Qualified Name
CocoPharma::GovernancePrinciple::PayStructuresExplicable

### Domain Identifier
22

### Summary
Every element of an individual's pay must be attributable to a defined structural factor, so that any difference between comparable employees can be explained without reference to who they are.

### Description
Pay transparency obligations invert the traditional position: the company must now be able to explain differences rather than decline to discuss them, and where it cannot, the burden of proof may shift against it. Meeting that requires pay to be built from identifiable components — grade, market supplement, location allowance, performance element, retained terms from a previous arrangement — each attributable to a defined factor recorded when it was applied. Legacy anomalies are the practical difficulty, since a difference originating in a starting salary negotiated years ago is real but is not a material factor that justifies present inequality, and the honest response is remediation rather than a better explanation. The principle requires such anomalies to be identified and addressed rather than documented and retained. It applies equally to the grouping of roles into equal-value categories, which must rest on objective criteria — skills, effort, responsibility, working conditions — since a categorisation that conveniently separates comparators will not survive scrutiny and would be evidence of the problem rather than a defence.

### Implications
- Every pay element must trace to a defined factor recorded when applied
- Equal-value categories must rest on objective criteria, not on organisational convenience
- Legacy anomalies require remediation, not documentation
- Explanations must hold for an external audience, since individuals may request comparisons

### Outcomes
- Individual pay comparison requests can be answered accurately and within the required period
- Unjustified differences are found and corrected internally rather than externally
- Statutory pay gap figures can be explained rather than merely published

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
Critical Knowledge Must Outlive the Individual Who Holds It

### Qualified Name
CocoPharma::GovernancePrinciple::KnowledgeOutlivesIndividual

### Domain Identifier
22

### Summary
Where an activity the organisation depends on can only be performed or explained by one person, that concentration is treated as a risk to be reduced rather than a strength to be relied upon.

### Description
Organisations reward and then depend upon the person who knows how something works, and the dependency is invisible until they leave. This principle requires such concentrations to be identified deliberately — activities with a single qualified person, systems with one person who understands the configuration, governance definitions whose rationale exists only in someone's memory — and treated as exposures with owners and reduction plans. Reduction is usually a combination of documentation and a second qualified person, and documentation alone is rarely sufficient, since tacit knowledge about why decisions were made resists being written down and is best transferred by working alongside someone. The principle deliberately applies to governance knowledge as well as technical skill, because the reasoning behind a control is what allows it to be adapted correctly when circumstances change, and a control maintained by people who no longer know why it exists decays into ritual. Departure is the point of maximum loss and minimum attention, which is why knowledge transfer is required before exit rather than attempted afterwards.

### Implications
- Single points of knowledge must be identified deliberately, not discovered on departure
- Reduction requires a second qualified person, not documentation alone
- Governance rationale is in scope, not only technical and operational skill
- Transfer happens before exit, while the individual is still available

### Outcomes
- Departures do not remove capabilities the organisation depends on
- Controls continue to be applied by people who understand their purpose
- Succession exposure is visible to management as a risk rather than a surprise

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
Regulated Roles Must Have Defined Competency Requirements

### Qualified Name
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Domain Identifier
22

### Summary
Every role performing a GMP, GCP, or otherwise regulated activity must have its competency requirements defined, recorded against the role rather than the individual, and kept current as the activity changes.

### Description
Competency requirements attach to the work, not to the person doing it, and recording them against the role is what makes it possible to ask whether an individual meets them. The obligation requires each regulated role to carry a defined set of requirements — the training that must be completed, the supervised practice that must be evidenced, the assessment that must be passed, and the interval at which each must be renewed — agreed with the domain that owns the regulated activity rather than determined by HR alone. Manufacturing states what a batch record signatory must be able to do; HR records it, tracks it, and reports currency. Requirements must be maintained as the activity changes: a process change that alters what an operator must do creates a competency gap in everyone previously qualified, and treating requalification as a change control consequence rather than an annual routine is what prevents a validated process being run by people trained on its predecessor. Where a role spans jurisdictions, the requirement is set to the strictest applicable.

### Implications
- Requirements attach to roles and are agreed with the domain owning the regulated activity
- Process and protocol changes must trigger competency reassessment for everyone affected
- Requirements must specify renewal intervals, not only initial attainment
- Roles spanning jurisdictions take the strictest applicable requirement

### Outcomes
- Whether an individual is qualified is a determinable question rather than a judgement
- Process changes do not silently invalidate the qualification of the people running them
- Manufacturing and drug development can evidence personnel competency to inspectors

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
Joiner, Mover, and Leaver Changes Must Be Actioned Within Defined Timeframes

### Qualified Name
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Domain Identifier
22

### Summary
Changes to an individual's employment status or role must be recorded and communicated to dependent systems within defined timeframes, with leaver notification treated as time-critical.

### Description
HR is the source of the event that every access control, delegation record, and authorisation list depends on, and the value of that data decays quickly. A leaver whose departure is recorded three days late retains system access for three days, retains authority to sign records they should no longer sign, and remains on distribution lists carrying confidential information — none of which is a security failure in the sense of a control being breached, because every control operated correctly on the information it had. Movers are the harder case and the more common failure: an individual changing role usually gains the new access promptly, because they need it to work, and retains the old access indefinitely, because nobody is inconvenienced by its persistence. This accumulation is precisely the entitlement drift that dissolves segregation of duties. The obligation therefore sets timeframes by event type, with leaver notification the shortest and involuntary departures immediate, and requires notification to dependent systems to be automatic rather than dependent on an HR administrator remembering which systems care.

### Implications
- Leaver notification is time-critical, with involuntary departures actioned immediately
- Mover changes must remove old entitlements as well as granting new ones
- Notification to dependent systems must be automatic, not manually initiated
- Timeframes must be defined per event type and monitored against actual performance

### Outcomes
- Access and authority end when employment or the role does
- Entitlement accumulation across a career is prevented rather than periodically corrected
- Dependent domains receive employment events without needing to ask

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
Employment Decision Records Must Be Retained and Reviewable

### Qualified Name
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Domain Identifier
22

### Summary
Records of hiring, promotion, pay, disciplinary, and termination decisions must capture the criteria, the reasoning, and the decision maker, and be retained for the period in which a claim may be brought.

### Description
The record must contain enough to reconstruct the decision, which means the criteria applied, the reasoning that connected them to this individual, the alternatives considered where the decision was comparative, and the identity of the decision maker. A record showing only the outcome is worth little on challenge. Retention runs to the limitation period for the claims that could arise, which differs across the US parent and the UK and EU subsidiaries and must be set to the longest applicable where an individual's employment spans more than one; discrimination claims in particular can be brought long after the decision and may reference decisions taken years earlier as evidence of a pattern. This retention requirement sits in tension with data minimisation and with erasure requests from former employees, and the tension is resolved by the privacy domain's retention framework rather than by HR deciding unilaterally — the obligation here is to state the employment-law requirement accurately so that the retention schedule reflects a real need rather than an assumed one.

### Implications
- Records must capture criteria, reasoning, alternatives considered, and decision maker
- Retention runs to the longest applicable limitation period across relevant jurisdictions
- Unsuccessful candidate records are in scope, since claims may arise from non-appointment
- The retention requirement is stated to privacy for incorporation into the retention schedule

### Outcomes
- Challenges brought years later are answered from contemporaneous records
- Pattern evidence can be examined internally before it is assembled externally
- Retention rests on a stated legal requirement rather than on caution

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
Pay Data Must Support Statutory Reporting and Individual Comparison Requests

### Qualified Name
CocoPharma::GovernanceObligation::PayDataSupportsStatutoryReporting

### Domain Identifier
22

### Summary
Payroll and reward data must be structured so that statutory pay gap measures can be produced on the prescribed basis, and individual comparative pay requests answered within the required period.

### Description
Both obligations draw on the same data and fail for the same reason: pay elements that cannot be classified consistently. Statutory reporting prescribes exactly what counts as ordinary pay and as bonus, calculated from a snapshot date, and a payroll structure where allowances and supplements are recorded inconsistently across subsidiaries cannot produce the figures without manual adjustment — which is both unreliable and unauditable. Individual comparison requests are harder still, because answering one requires the equal-value categorisation to already exist: within two months the company must identify the category of workers doing the same or equal-value work as the requester, compute average pay by sex within it, and provide the result. That cannot be assembled on demand. The obligation therefore requires the categorisation, the pay element classification, and the calculation logic to be maintained as standing capabilities, tested against the prescribed basis, and consistent across the UK and EU subsidiaries even where local reporting formats differ.

### Implications
- Pay elements must be classified consistently across all subsidiaries
- Equal-value worker categorisation must exist in advance of any request
- Calculation logic must be maintained, versioned, and tested against the prescribed basis
- Two-month response capability requires standing data, not on-demand assembly

### Outcomes
- Statutory figures are produced from data rather than from manual adjustment
- Individual comparison requests are answered accurately within the required period
- The company's published figures can be reconciled and defended

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
Critical Knowledge Must Be Transferred Before Departure

### Qualified Name
CocoPharma::GovernanceObligation::KnowledgeTransferBeforeExit

### Domain Identifier
22

### Summary
Where a departing individual holds critical knowledge or sole qualification, transfer must be planned and evidenced before their last working day, with the exposure escalated if it cannot be completed.

### Description
Notice periods are the only window in which knowledge can be transferred, and they are routinely consumed by handover of active work rather than by transfer of what only the individual knows. The obligation requires the exposure to be assessed at the point notice is given: what activities does this person perform that nobody else is qualified for, what systems do they alone understand, and what governance definitions do they own whose rationale is not written down. Where the assessment identifies a critical concentration, transfer is planned with a named recipient and evidenced by the recipient demonstrating the capability rather than by the departer confirming they explained it. Where transfer cannot be completed within the notice period the exposure is escalated to the domain that depends on the activity, so that the receiving domain can decide whether to secure a consultancy arrangement, suspend the activity, or accept the risk — a decision that belongs to them and not to HR. The obligation applies equally to involuntary departures, where the window may be nil and the escalation is therefore immediate.

### Implications
- Exposure assessment happens when notice is given, not during the final week
- Transfer is evidenced by the recipient demonstrating capability, not by the departer's assurance
- Incomplete transfer is escalated to the dependent domain, which owns the resulting decision
- Involuntary departures require immediate escalation, since the transfer window may not exist

### Outcomes
- Sole-qualification activities do not lapse silently on departure
- Dependent domains learn of the exposure while they can still act on it
- Governance definitions retain someone who understands why they exist

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
Competency Framework Management

### Qualified Name
CocoPharma::GovernanceApproach::CompetencyFrameworkManagement

### Domain Identifier
22

### Summary
Competencies are defined once as reusable units, assembled into role requirements with the owning domain, and tracked per individual with currency enforced by the systems that grant authorisation.

### Description
Defining competencies as reusable units rather than as role-specific training lists is what makes the framework maintainable: aseptic technique is one competency whether it appears in a sterile filling role or a quality control role, and when its requirements change it changes once. Role requirements are then assembled from those units in consultation with the domain owning the regulated activity, which keeps the technical judgement where the knowledge is while keeping the record in one system. Currency is enforced at the point of authorisation rather than reported afterwards — a system that will not accept a signature from someone whose qualification has lapsed prevents the finding, whereas a monthly report identifies it after the batch has been signed. The framework also carries the gap analysis the workforce capability imperative depends on, comparing competencies held against those the strategy requires, and it is the mechanism through which change control reaches people: a process change identifies the affected competency, which identifies everyone requiring requalification.

### Implications
- Competencies are defined as reusable units, not as role-specific training lists
- Role requirements are agreed with the domain owning the regulated activity
- Currency is enforced at the point of authorisation, not reported after the fact
- Change control must resolve to affected competencies and thence to affected individuals

### Outcomes
- Competency definitions are maintained once and applied consistently
- Lapsed qualification prevents the action rather than being discovered afterwards
- Capability gaps against strategic requirements are measurable

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Pay Equity Analysis and Remediation

### Qualified Name
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Domain Identifier
22

### Summary
Pay is analysed at least annually across equal-value categories to identify differences that recorded material factors do not explain, with unexplained differences remediated rather than documented.

### Description
The analysis proceeds in a deliberate order. Workers are grouped into equal-value categories on objective criteria; pay differences within each category are computed; the recorded material factors are applied to see how much of the difference they account for; and what remains is the unexplained gap. That residual is the number that matters, and it is a far more useful management measure than the headline gender pay gap, which is driven largely by the distribution of men and women across grades and can move for reasons unconnected to pay decisions. Where the residual is material the response is remediation on a defined timetable, because the alternative — continuing to search for an explanation — is what the regulations characterise as an unjustified gap. The analysis is conducted under legal privilege where the jurisdiction permits, so that the company can examine its position honestly before deciding what to do, and its results feed the joint pay assessment process where the directive's threshold is crossed. Starting salaries receive separate attention, since differences introduced at hire persist through percentage-based increases indefinitely.

### Implications
- Categorisation must precede analysis and rest on objective, documented criteria
- The unexplained residual is the operative measure, not the headline gap
- Material residual differences require remediation on a timetable, not further investigation
- Starting salary distributions require separate analysis given their persistence

### Outcomes
- Unjustified pay differences are found and corrected before they are challenged
- The company can explain its published figures rather than only publish them
- Joint pay assessment, where triggered, begins from work already done

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Succession and Knowledge Continuity Planning

### Qualified Name
CocoPharma::GovernanceApproach::SuccessionAndKnowledgeContinuity

### Domain Identifier
22

### Summary
Critical activities are mapped to the individuals qualified to perform them, single points of dependency are reported as exposures with owners, and reduction plans are tracked alongside other risks.

### Description
The approach starts from activities rather than from people, which is what distinguishes it from conventional succession planning focused on senior roles. Each domain identifies the activities it depends on; the competency framework identifies who is qualified to perform each; and any activity with one qualified person is an exposure regardless of that person's seniority. In practice the most acute concentrations are rarely at the top — they are the one analyst who can run a legacy method, the one engineer who understands a control system, the one person who remembers why a governance definition was written as it was. Exposures are owned by the domain depending on the activity rather than by HR, since only that domain can weigh the cost of reduction against the consequence of loss. Reduction plans pair documentation with a second qualified person, and the plan is considered complete when the second person has demonstrated the capability independently. Concentrations are reviewed on a defined cycle and reassessed whenever an individual gives notice.

### Implications
- Mapping starts from critical activities, not from senior roles
- Exposures are owned by the depending domain, which weighs reduction cost against loss
- Reduction requires demonstrated capability in a second person, not documentation alone
- Notice from any individual triggers reassessment of the activities they cover

### Outcomes
- Dependency concentrations are visible before they become disruptions
- Reduction effort is directed by the domains that would bear the consequence
- Departures are absorbed rather than causing capability loss

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — Human Resource Management

---

### 3.1 Governance Roles

___

## Create Governance Role

### Display Name
Head of Human Resources (Governance Domain Lead)

### Qualified Name
CocoPharma::GovernanceRole::HeadOfHumanResources

### Description
The Head of Human Resources holds the Human Resource Management governance domain lead role, accountable for employment practice, workforce data, competency records, and pay equity across the group. The role sets the framework within which employment decisions are made and evidenced, owns the qualification record that manufacturing, drug development, and security depend on, and is accountable for statutory pay reporting and for answering individual pay comparison requests. It is held by Faith Broker, who also holds the Chief Privacy Officer role; the two are kept distinct in governance terms, with privacy assuring the lawful basis for employee data processing that HR declares, and any conflict between the two positions escalated to the Chief Data Officer rather than resolved within the combined role.

### Scope
Human Resource Management governance domain — employment decision framework, workforce and competency data, qualification records relied on by other domains, pay structures and equity analysis, and knowledge continuity.

### Headcount
1

### Category
Governance Role

### Search Keywords
- human resources governance
- competency management
- pay equity
- employment practice

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
HR Data Steward

### Qualified Name
CocoPharma::GovernanceRole::HRDataSteward

### Description
The HR Data Steward maintains the workforce data that other domains consume: the competency framework and its role requirements, individual qualification records and their currency, the joiner-mover-leaver event feed to dependent systems, and the equal-value worker categorisation underpinning pay analysis. The role monitors the timeliness of employment event notification, investigates cases where a dependent system acted on stale HR data, and maintains the point-in-time query capability that inspections rely on. It works with the Manufacturing Governance Lead and the Drug Development Lead on competency requirements for regulated roles, and with the Chief Information Security Officer on the leaver notification path.

### Scope
Competency framework and qualification records, employment event notification to dependent systems, equal-value categorisation data, and point-in-time workforce reporting.

### Headcount
2

### Category
Governance Role

### Search Keywords
- workforce data
- competency records
- joiner mover leaver
- HR data stewardship

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
Regulated Role Competency Currency

### Qualified Name
CocoPharma::GovernanceMetric::RegulatedRoleCompetencyCurrency

### Domain Identifier
22

### Summary
Measures the percentage of individuals authorised to perform regulated activities whose competency record is complete and within its renewal interval.

### Description
The metric measures the condition that manufacturing and drug development rely on when they certify that qualified people performed the work. It is computed per regulated activity rather than per person, since an individual may be current for one authorisation and lapsed for another, and reported to the domain owning the activity rather than only within HR — the Manufacturing Governance Lead needs to know that four batch record signatories are approaching requalification, and that is not information HR should hold alone. Two failure types are separated: lapsed, where the renewal interval has passed, and incomplete, where a requirement was never evidenced, because the second usually indicates a process gap at onboarding or transfer rather than a scheduling failure. Individuals requalifying within thirty days are reported as a forward view, since the useful action is to schedule the assessment rather than to record the lapse. Target is 100%, as a lapse is a compliance exposure rather than a performance shortfall.

### Implications
- Computed per authorisation, not per person, since currency varies by activity
- Reported to the domain owning the regulated activity, not only within HR
- Lapsed and never-evidenced failures must be separated, as their causes differ
- A forward view of upcoming renewals is required for the metric to drive action

### Outcomes
- Regulated work is performed by demonstrably qualified people
- Approaching lapses are scheduled rather than discovered
- Onboarding and transfer process gaps are distinguishable from scheduling failures

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Leaver Notification and Access Revocation Timeliness

### Qualified Name
CocoPharma::GovernanceMetric::LeaverNotificationTimeliness

### Domain Identifier
22

### Summary
Measures elapsed time from employment end to HR record update and onward to access revocation in dependent systems, reported separately for voluntary and involuntary departures.

### Description
The measurement is split deliberately into two intervals because they have different owners. The first runs from the employment end date to the HR record being updated, and is HR's own performance; the second runs from that update to entitlements actually being revoked in dependent systems, and belongs to the systems consuming the feed. Reporting them separately prevents the common outcome in which each party believes the delay was elsewhere. Involuntary departures are reported apart from voluntary ones because the risk profile differs sharply and the target is immediate rather than same-day; an aggregate figure dominated by planned retirements would conceal poor performance on exactly the cases that matter. Movers are reported alongside leavers, measured on removal of superseded entitlements rather than on grant of new ones, since the grant happens promptly by necessity and the removal is what decays. Target is same working day for voluntary leavers and immediate for involuntary, with mover entitlement removal within five working days.

### Implications
- Two intervals must be measured separately so delay is attributable
- Involuntary departures must be reported apart from voluntary ones
- Mover measurement must be on entitlement removal, not on entitlement grant
- Requires employment end date and revocation timestamps to be captured comparably

### Outcomes
- Access ends when employment does, and delay is attributable when it does not
- The high-risk involuntary cases are visible rather than averaged away
- Entitlement accumulation through role changes is measurably reduced

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Unexplained Pay Difference by Equal-Value Category

### Qualified Name
CocoPharma::GovernanceMetric::UnexplainedPayDifference

### Domain Identifier
22

### Summary
Measures the pay difference remaining within each equal-value worker category after recorded material factors are applied, reported against the regulatory threshold.

### Description
This is the residual the pay equity analysis produces, and it is reported rather than the headline pay gap because it is the figure the company can actually act on. The headline gap largely reflects how men and women are distributed across grades and can improve or worsen through recruitment patterns that have nothing to do with pay decisions; the residual within a category, by contrast, is a difference between people doing equal-value work that the company's own recorded factors do not explain, which is precisely what regulators and claimants examine. Reporting is per category and against the five per cent threshold that triggers joint pay assessment under the EU directive, with categories over threshold identified individually rather than absorbed into an average. Coverage is reported alongside: the proportion of the workforce that falls into a defined equal-value category at all, since a low residual across categories covering half the workforce says little. The metric is produced from the annual analysis and reviewed by the Head of Human Resources with the Chief Financial Officer, given the remediation cost implications.

### Implications
- Reports the residual after material factors, not the headline pay gap
- Categories exceeding the regulatory threshold must be identified individually
- Categorisation coverage must be reported alongside, or the residual is unrepresentative
- Requires material factors to be recorded at the point they are applied to pay

### Outcomes
- Management sees a figure it can act on rather than one driven by workforce composition
- Categories at regulatory risk are identified before an assessment is triggered
- Remediation cost can be estimated and planned rather than incurred reactively

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links

---

### 4.1 Governance Responses — Drivers linked to HR Policies

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKEqualityAct2010

### Policy
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Rationale
Indirect discrimination turns on whether a criterion can be objectively justified, which requires the criterion to have been defined and recorded before it was applied.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKEqualityAct2010

### Policy
CocoPharma::GovernancePrinciple::PayStructuresExplicable

### Rationale
Equal pay claims are answered by showing that a difference arises from a material factor unrelated to a protected characteristic. Pay built from recorded factors makes that answer available.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::UKEqualityAct2010

### Policy
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Rationale
Discrimination claims may be brought long after the decision and may cite earlier decisions as pattern evidence, so retention must run to the limitation period rather than to operational need.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUPayTransparencyDirective

### Policy
CocoPharma::GovernanceObligation::PayDataSupportsStatutoryReporting

### Rationale
The two-month deadline for individual comparison requests cannot be met by assembling the categorisation on demand; the capability must stand ready.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUPayTransparencyDirective

### Policy
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Rationale
An unjustified gap of five per cent or more triggers joint pay assessment. Annual analysis of the unexplained residual is how the company finds that before the threshold is crossed.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUPayTransparencyDirective

### Policy
CocoPharma::GovernancePrinciple::PayStructuresExplicable

### Rationale
The directive shifts the burden of proof where transparency obligations are unmet, making the ability to explain every pay element a defensive necessity rather than good practice.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Policy
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Rationale
The threat exists because what an individual is permitted to do is often undefined. Recording requirements against the role makes qualification a determinable question.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Policy
CocoPharma::GovernanceApproach::CompetencyFrameworkManagement

### Rationale
Enforcing currency at the point of authorisation prevents the unqualified action, where reporting afterwards only documents it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Policy
CocoPharma::GovernancePrinciple::QualificationRecordsAuthoritative

### Rationale
Manufacturing and drug development rely on the HR record being right. Making it authoritative accepts that reliance and the obligations that follow from it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::InconsistentEmploymentDecisions

### Policy
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Rationale
The pattern is invisible case by case and appears only in aggregate, which is what the analysis is designed to surface before an external party does.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::InconsistentEmploymentDecisions

### Policy
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Rationale
Divergence arises from managers interpreting criteria differently. Defining criteria in advance and recording their application is what makes consistency testable.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Policy
CocoPharma::GovernancePrinciple::KnowledgeOutlivesIndividual

### Rationale
The organisation-wide talent threat is answered in this domain by treating single points of knowledge as exposures to be reduced rather than as dependable strengths.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Policy
CocoPharma::GovernanceObligation::KnowledgeTransferBeforeExit

### Rationale
The notice period is the only window in which transfer is possible, so the obligation places the assessment at the point notice is given.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::WorkforceCapabilityTransition

### Policy
CocoPharma::GovernanceApproach::CompetencyFrameworkManagement

### Rationale
Measuring capability against what the strategy requires depends on competencies being defined as comparable units rather than as role-specific training lists.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::WorkforceCapabilityTransition

### Policy
CocoPharma::GovernanceApproach::SuccessionAndKnowledgeContinuity

### Rationale
Single points of qualification constrain programme delivery as directly as absent skills, and the mapping identifies them before they bite.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ExplicableEmploymentDecisions

### Policy
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Rationale
The company's ability to explain a decision years later rests entirely on what was recorded at the time and retained since.

___

---

### 4.2 Governance Mechanisms — HR Policies linked to Controls

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Mechanism
CocoPharma::GovernanceMetric::RegulatedRoleCompetencyCurrency

### Rationale
Currency per authorisation measures the obligation where it matters, and reporting to the owning domain puts the information where action can be taken.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::CompetencyFrameworkManagement

### Mechanism
CocoPharma::GovernanceMetric::RegulatedRoleCompetencyCurrency

### Rationale
The split between lapsed and never-evidenced tells the framework whether its failures are scheduling or onboarding, which need different fixes.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Mechanism
CocoPharma::GovernanceMetric::LeaverNotificationTimeliness

### Rationale
Measuring the two intervals separately makes delay attributable to HR or to the consuming system rather than disputed between them.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Mechanism
CocoPharma::GovernanceMetric::UnexplainedPayDifference

### Rationale
The residual after material factors is the analysis output and the figure that regulators and claimants examine.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::PayStructuresExplicable

### Mechanism
CocoPharma::GovernanceMetric::UnexplainedPayDifference

### Rationale
A rising residual indicates that pay elements are being applied without a recorded factor, which is the principle failing in practice.

___

---

### 4.3 Peer Driver Links

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Governance Driver 2
CocoPharma::Threat::BatchQualityFailureFromDataErrors

### Description
An expired qualification and a wrong batch record entry produce the same finding: a record that cannot demonstrate the product was made correctly. The HR threat is a cause of the manufacturing one, and neither domain can see it alone.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::WorkforceCapabilityTransition

### Governance Driver 2
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Description
The corporate transition depends on capabilities the workforce does not yet hold uniformly, and qualification lead time is a hard constraint on how fast the transition can proceed.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::InconsistentEmploymentDecisions

### Governance Driver 2
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Description
Perceived unfairness in employment decisions is among the most reliable causes of voluntary departure by exactly the people the organisation can least afford to lose, so the two threats reinforce each other.

___

---

### 4.4 Peer Policy Links — Related Policies Across Domains

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Mechanism
CocoPharma::CertificationType::GCPSiteQualification

### Rationale
Site qualification confirms that investigator site staff are trained for the protocol; the competency obligation is the internal equivalent for company personnel. Both answer the same regulatory question about who is permitted to perform the work.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Governance Policy 2
CocoPharma::GovernancePrinciple::SegregationOfDutiesInFinancialProcesses

### Description
Entitlement drift through unremoved mover access is the principal mechanism by which segregation of duties decays, which makes the mover half of this obligation a financial control as much as an HR one.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataRetentionSchedulesDefined

### Description
HR states the employment-law retention requirement; privacy incorporates it into the schedule and resolves it against minimisation and erasure rights. Neither domain sets the period alone.

___

---


## Part 5: Human Resource Management Governance Folio

Unlike the other domain programs, this file creates its folio rather than adding to an existing one, since the Human Resource Management domain is established here for the first time.

---

### 5.1 Folio Definition

___

## Create Folio

### Display Name
Head of Human Resources — Governance Folio

### Qualified Name
CocoPharma::Folio::HeadOfHumanResources

### Description
The governance definitions owned by the Head of Human Resources (Faith Broker) in the Human Resource Management domain, identifier 22. The folio covers the workforce capability and employment practice imperatives, the unqualified personnel and inconsistent decision threats, the UK Equality Act and EU Pay Transparency Directive, the employment decision, qualification, pay and knowledge continuity policies, and the controls and processing purposes that operationalise them.

### Purpose
Provides Faith Broker with a single view of the HR governance definitions distinct from the Chief Privacy Officer folio also held. Keeping the two separate is deliberate: the same person holds both roles, and the folios are what make the boundary between employment purposes and data protection assurance visible rather than implicit.

### Category
Governance Folio

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::HeadOfHumanResources

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::HeadOfHumanResources

### Description
Assigns the Head of Human Resources role responsibility for the governance definitions collected in the Human Resource Management folio.

___

---

### 5.2 Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::BusinessImperative::WorkforceCapabilityTransition

### Membership Rationale
Workforce capability against the personalised medicine transition is owned by the Head of Human Resources with the depending domains.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::BusinessImperative::ExplicableEmploymentDecisions

### Membership Rationale
The framework within which employment decisions are made and evidenced is set by the Head of Human Resources.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::Threat::UnqualifiedPersonnelInRegulatedRoles

### Membership Rationale
The qualification record other domains rely on is an HR record, so the exposure arising from its inaccuracy is owned here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::Threat::InconsistentEmploymentDecisions

### Membership Rationale
Aggregate inconsistency in employment outcomes is detectable and correctable only from within the HR domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::Regulation::UKEqualityAct2010

### Membership Rationale
UK discrimination and equal pay obligations fall to the Head of Human Resources across the UK subsidiaries.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::Regulation::EUPayTransparencyDirective

### Membership Rationale
Pay transparency obligations across the EU subsidiaries are discharged by the HR function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernancePrinciple::EmploymentDecisionsOnRecordedCriteria

### Membership Rationale
The standard applied to employment decision making and recording is set within this domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernancePrinciple::QualificationRecordsAuthoritative

### Membership Rationale
Establishing the HR record as authoritative, and accepting the obligations that follow, is an HR commitment to the domains that consume it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernancePrinciple::PayStructuresExplicable

### Membership Rationale
Pay structure design and the recording of material factors is owned by the HR function with the Chief Financial Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernancePrinciple::KnowledgeOutlivesIndividual

### Membership Rationale
Treating knowledge concentration as a reducible exposure is an HR-owned principle applied across every domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceObligation::CompetencyRequirementsDefinedForRegulatedRoles

### Membership Rationale
Competency requirements are recorded and maintained by HR in consultation with the domains owning the regulated activities.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceObligation::JoinerMoverLeaverTimeliness

### Membership Rationale
Employment event timeliness is an HR obligation on which security, manufacturing, and drug development all depend.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceObligation::EmploymentDecisionRecordsRetained

### Membership Rationale
The employment-law retention requirement is stated by HR for incorporation into the privacy retention schedule.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceObligation::PayDataSupportsStatutoryReporting

### Membership Rationale
Statutory pay reporting and individual comparison responses are produced by the HR function.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceObligation::KnowledgeTransferBeforeExit

### Membership Rationale
Exit-time knowledge transfer is initiated and evidenced by HR, with escalation to the depending domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceApproach::CompetencyFrameworkManagement

### Membership Rationale
The competency framework is designed and maintained by the HR Data Steward.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceApproach::PayEquityAnalysis

### Membership Rationale
Annual pay equity analysis is conducted by HR and reviewed with the Chief Financial Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceApproach::SuccessionAndKnowledgeContinuity

### Membership Rationale
Activity-based succession mapping is operated by HR with exposures owned by the depending domains.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceMetric::RegulatedRoleCompetencyCurrency

### Membership Rationale
Competency currency is reported by HR to each domain owning regulated activities.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceMetric::LeaverNotificationTimeliness

### Membership Rationale
Notification and revocation timeliness is reported to the Head of Human Resources and the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::HeadOfHumanResources

### Element Id
CocoPharma::GovernanceMetric::UnexplainedPayDifference

### Membership Rationale
The unexplained pay residual is reported to the Head of Human Resources and the Chief Financial Officer.

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
CocoPharma::Folio::HeadOfHumanResources

### Membership Rationale
The Head of Human Resources folio is part of the Coco Pharmaceuticals governance folios collection, making the Human Resource Management domain discoverable alongside the other domain folios.

### Membership Status
VALIDATED

___

---

## Part 6: Corporate Regulation Library

Employment regulation had no home in the Corporate Regulation Library, whose folders covered financial, clinical trial, pharmaceutical industry, privacy, and security regulation. This part creates the Employment Regulations folder, registers it in the library, and places the two regulations defined in this file.

---

### 6.1 Folder Definition

___

## Create Collection Folder

### Display Name
Employment Regulations

### Qualified Name
CollectionFolder::Coco::Employment Regulations

### Purpose
Groups the employment, equality, and pay transparency regulations that Coco Pharmaceuticals is subject to across the US parent and the UK and EU subsidiaries.

### Description
Employment regulation governs the relationship between the company and the people who work for it: discrimination and equal treatment, equal pay and pay transparency, working time, and the procedural obligations attaching to hiring and dismissal. It is distinct from the other library folders in that its subject is the workforce rather than the product, the money, or the data, and it applies to every part of the group regardless of what that part makes or sells. Regulations here differ materially by jurisdiction — the UK and EU regimes diverge on pay transparency in particular, and the US position differs again — so the folder holds parallel instruments addressing the same subject rather than a single set applying group-wide.

### Category
Regulation Category

### Authors
Faith Broker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 6.2 Library Registration

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Corporate Regulation Library

### Element Id
CollectionFolder::Coco::Employment Regulations

### Membership Rationale
Employment regulation is a category of corporate regulatory obligation in its own right and belongs in the library alongside the financial, pharmaceutical industry, privacy, and security folders, so that the full set of regulations the company is subject to is discoverable from one place.

### Membership Status
VALIDATED

___

---

### 6.3 Folder Members

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Employment Regulations

### Element Id
CocoPharma::Regulation::UKEqualityAct2010

### Membership Rationale
The Equality Act is the principal UK employment regulation governing discrimination and equal pay, and applies across the UK subsidiaries.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Employment Regulations

### Element Id
CocoPharma::Regulation::EUPayTransparencyDirective

### Membership Rationale
The Pay Transparency Directive governs pay disclosure, comparison rights, and gap reporting across the EU subsidiaries, and is the EU counterpart to the equal pay provisions of the Equality Act.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| Resource | Description |
|----------|-------------|
| `joint-governance-officer-definitions.md` | Foundation definitions — the loss of key talent threat this domain responds to, and the governance roles and folios framework |
| `privacy-governance-program.md` | PRIVACY-domain program. Owns the lawful basis, retention framework, and data subject rights for employee personal data; this file declares HR's own processing purposes within that framework |
| `manufacturing-governance-program.md` | MANUFACTURING-domain program. Consumes the qualification record and declares its own GMP purpose for operator training data |
| `drug-development-governance.md` | Drug Development domain program. Depends on site and company personnel training records for GCP compliance |
| `data-security-strategy.md` | SECURITY-domain program. The identity lifecycle is driven by the employment events this domain produces |
| `corporate-governance-program.md` | CORPORATE-domain program. Segregation of duties depends on mover entitlement removal, and pay remediation cost is reviewed with the CFO |
| `employee-glossary.md` | Glossary of employee and organisational terms used across the workforce data model |
