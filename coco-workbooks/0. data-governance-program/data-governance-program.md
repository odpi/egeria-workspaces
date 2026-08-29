# Coco Pharmaceuticals — Data Governance Program

> **Author:** Jules Keeper (Chief Data Officer), Erin Overview (Information Architect), Peter Profile (Solution Architect)  
> **Version:** 2.0  
> **Status:** ACTIVE  
> **Date:** 2026-08-22  
> **Description:** Governance definitions for the DATA domain at Coco Pharmaceuticals. The DATA domain exists in service of the domains that carry business and regulatory responsibility — manufacturing, privacy, drug development, and corporate — and this file is structured to reflect that. Load `joint-governance-officer-definitions.md` first, as it defines the shared drivers, governance roles, and cross-domain policies referenced throughout. The domain programs for manufacturing, privacy, security, and drug development define the drivers that most of the policies here respond to.

---

## Overview

The DATA governance domain is different in kind from the domains around it. Manufacturing answers to GMP inspectors. Privacy answers to data protection authorities. Drug development answers to the FDA and the EMA. Each of those domains owns a business outcome, a regulator, or both, and their governance programs are built around defending them.

DATA owns neither directly. Its purpose is to make the other domains capable of meeting obligations that are theirs, not ours. When a batch record cannot be traced, the finding lands on manufacturing. When a data subject request cannot be answered within a month, the finding lands on privacy. When a submission slips because analysis datasets needed remapping, the cost lands on drug development. In each case the underlying cause is frequently a data problem — but the accountability sits with the domain that carries the outcome, and the DATA program's job is to remove the cause rather than to claim the accountability.

This has a specific consequence for how this program is shaped, and it is worth stating plainly because it makes the file look sparse in a place where other domain programs look full:

**Part 1 is deliberately short.** DATA owns only the small number of governance drivers that are genuinely systemic — problems that originate in how the organisation manages data itself, that no single domain can fix from inside its own boundary, and that surface as damage in several domains at once. Three such drivers are defined here. Everything else in this program responds to drivers owned elsewhere.

**Part 4 is deliberately long.** The service relationship is expressed structurally, as links: DATA policies responding to manufacturing, privacy, drug development, and corporate drivers. A DATA policy with no link to a driver in another domain should be treated with suspicion — it is either responding to one of our three systemic drivers, or it is governance for its own sake.

The same reasoning places SECURITY alongside DATA as a systemic domain, with one exception: cyber incidents can halt the whole business, so they reach the board and legitimately appear as drivers in their own right. IT_INFRASTRUCTURE and SOFTWARE_DEVELOPMENT are serving domains of a third kind — they provide the digital services the business runs on, and their governance programs sit downstream of this one.

The program is organised as:

1. **Governance Drivers** (Part 1) — the three systemic data drivers the DATA domain owns. All other drivers this program responds to are defined in `joint-governance-officer-definitions.md` and in the domain programs.
2. **Governance Policies** (Part 2) — the principles, obligations, and approaches through which the DATA domain serves the rest of the organisation.
3. **Governance Controls** (Part 3) — the roles and metrics that make those policies observable.
4. **Governance Links** (Part 4) — the responses, mechanisms, and peer relationships that connect this program to the domains it serves.

All definitions in this file carry Domain Identifier `Data` and are members of the Chief Data Officer Governance Folio.

---

## Part 1: Governance Drivers — DATA Domain

The DATA domain owns three governance drivers. Each meets the same test: it originates in how the organisation manages data rather than in any one business process, no single domain can resolve it from within its own boundary, and it surfaces as damage in several domains at once. Drivers that fail this test belong to the domain that carries the business or regulatory responsibility, and this program responds to them in Part 4 rather than restating them here.

---

### 1.1 Business Imperatives

___

## Create Business Imperative

### Display Name
A Trusted Data Foundation for Every Governance Domain

### Qualified Name
CocoPharma::BusinessImperative::TrustedDataFoundation

### Domain Identifier
Data

### Summary
Coco Pharmaceuticals must provide a common, trustworthy data foundation that the manufacturing, privacy, drug development, and corporate domains can each rely on to meet their own obligations.

### Description
Every governance domain in the organisation depends on data it does not itself produce. Manufacturing needs supplier and material data owned by procurement. Privacy needs to locate personal data wherever it has spread, including into research and manufacturing systems. Drug development needs reference data that is stable across the years a trial runs. Corporate reporting needs figures that reconcile across departments. Where each domain solves these needs separately, the organisation ends up with parallel definitions, duplicated reconciliation effort, and controls that stop at domain boundaries the data itself crosses freely. This imperative is the DATA domain's reason for existing: to build once, centrally, what every domain would otherwise build repeatedly and incompatibly. It is deliberately expressed as a service obligation rather than a business outcome, because the outcomes belong to the domains being served — the measure of success is that they meet their obligations more easily, not that the DATA domain accumulates governance of its own.

### Implications
- DATA-domain investment must be justified by the obligations it lets other domains discharge, not by data governance maturity in the abstract
- Common capabilities — the catalog, the business glossary, lineage, quality rules — must be usable by every domain rather than tuned to one
- Where a domain's requirement conflicts with a common definition, the conflict must be resolved explicitly rather than by allowing a private variant
- The DATA domain must be able to state, for each of its policies, which other domain's obligation it serves

### Outcomes
- Domain governance leads can meet their regulatory obligations without building private data infrastructure
- Data crossing domain boundaries retains its meaning, classification, and quality expectations
- Governance effort spent on data is incurred once rather than repeated in each domain

### Importance
High

### Category
Data Governance

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

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
Fragmented Data Definitions Across the Organisation

### Qualified Name
CocoPharma::Threat::FragmentedDataDefinitions

### Domain Identifier
Data

### Summary
The same business concept may be defined differently in each department, so that data cannot be combined across the organisation without manual reconciliation that is slow, costly, and error-prone.

### Description
"Batch", "patient", "supplier", and "revenue" each mean something slightly different in every system that records them. A batch in manufacturing execution is a production run; in quality it is a testing unit; in distribution it is a shipment lot. None of these definitions is wrong within its own department, and each was chosen for good local reasons — which is precisely why the problem is systemic and cannot be fixed by any one department deciding to change. The damage appears elsewhere: figures that will not reconcile in corporate reporting, analyses that silently combine incompatible populations, integration projects whose cost is dominated by mapping, and regulatory submissions that require manual assembly because no automated path can be trusted. The threat grows with every new system and every acquisition, and it grows fastest where departments are under time pressure and a local definition is the quickest route to a working system.

### Implications
- Definitions must be agreed across departments rather than negotiated pairwise at integration time
- A governed business glossary is required, with a defined route for proposing and approving changes
- Departments must be able to record a justified local variant rather than being forced into silent divergence
- Integration and reporting projects must be able to discover the agreed definition before building a mapping

### Importance
High

### Category
Data Governance

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Threat

### Display Name
Uncontrolled Proliferation of Data Copies

### Qualified Name
CocoPharma::Threat::UncontrolledDataProliferation

### Domain Identifier
Data

### Summary
Data copied out of governed systems into spreadsheets, extracts, and departmental databases escapes the controls applied to the original, and its existence is frequently unknown to the domain accountable for it.

### Description
Copies are made for entirely legitimate reasons — an analysis the source system cannot support, a report a regulator asked for, a dataset shared with a collaborator. The copy inherits the data but not its governance: classification labels are lost, access is granted by whoever holds the file, retention schedules do not follow, and quality rules are not applied. Over time the copy diverges from the source and may be used in preference to it, so that decisions rest on data nobody is maintaining. This threat is the common upstream cause of failures that surface as other domains' incidents: privacy cannot answer a data subject request because personal data sits in extracts nobody catalogued; security cannot assess exposure because it does not know where sensitive data lives; manufacturing and drug development discover that an analysis used a stale extract. Because the copies are made across every domain, no single domain can see the pattern, and only a data-domain control that operates across all of them can.

### Implications
- The organisation must be able to discover data copies it did not deliberately create
- Classification and retention must travel with data when it is copied, not remain attached to the source alone
- Legitimate needs that drive copying must be met by governed alternatives, or copying will continue regardless of policy
- Copies that cannot be justified must have an owned route to removal, not merely a prohibition

### Importance
High

### Category
Data Governance

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 2: Governance Policies — DATA Domain

Governance policies define how Coco Pharmaceuticals responds to the governance drivers. The definitions below apply to the DATA governance domain.

---

### 2.1 Governance Principles

___

## Create Governance Principle

### Display Name
Common Data Definitions Across the Organisation

### Qualified Name
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Domain Identifier
Data

### Summary
Coco Pharmaceuticals will maintain shared, agreed definitions for data used across multiple departments, to eliminate ambiguity and enable reliable data sharing.

### Description
One of the most significant barriers to data sharing and integrated analytics is inconsistent data definitions. When different departments define "patient", "batch", "supplier", or "revenue" differently, data cannot be combined without manual reconciliation — which is slow, error-prone, and expensive. Coco Pharmaceuticals will establish and maintain a common glossary of data definitions, agreed across departments, covering what data means, how it is formatted, what valid values it can take, and how frequently it is updated.

### Implications
- A governed business glossary must be maintained and kept current
- Changes to data definitions must go through an agreed approval process
- Systems must use common definitions wherever possible; exceptions must be documented

### Outcomes
- Data can be shared between departments without manual reconciliation
- Analytics based on data from multiple sources produce consistent results
- New staff can quickly understand what data means

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Data is a Shared Organisational Resource

### Qualified Name
CocoPharma::GovernancePrinciple::DataIsASharedOrganisationalResource

### Domain Identifier
Data

### Summary
Data collected or created by one part of the organisation is available as a shared resource for authorised use by other parts of the organisation.

### Description
In the past, Coco Pharmaceuticals' departments have operated as data silos — each collecting its own data and sharing it reluctantly. This model is incompatible with personalised medicine, which requires research, manufacturing, clinical, and financial data to flow freely between departments. The principle is that data belongs to the organisation, not to the department that collected it. Subject to appropriate privacy and security controls, data collected for one purpose should be available for other authorised purposes.

### Implications
- Data sharing agreements must be established between departments
- Access controls must enable authorised sharing while preventing unauthorised access
- Data consumers must respect the quality and governance standards set by the data owner

### Outcomes
- Research can access manufacturing and clinical data to accelerate drug development
- Finance can access data from all departments for accurate reporting and forecasting
- Duplicate data collection is reduced as authoritative shared sources are established

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Data Quality Is Defined by Fitness for Purpose

### Qualified Name
CocoPharma::GovernancePrinciple::DataQualityFitForPurpose

### Domain Identifier
Data

### Summary
Data quality is assessed against the requirements of the domains that use the data, not against an abstract standard of correctness, and those requirements are stated by the using domain.

### Description
There is no such thing as data that is simply "good quality". A supplier address accurate enough for procurement correspondence may be inadequate for customs declarations; a temperature reading rounded to the nearest degree may satisfy a dashboard and fail a GMP requirement. Treating quality as absolute produces two failures at once: effort is spent perfecting data nobody needs perfected, while data that genuinely must be exact is held to the same undifferentiated standard and quietly falls short. This principle places the definition of "good enough" with the domain that carries the obligation — manufacturing states what batch data must satisfy, privacy states what is required to answer a subject request, drug development states what a submission needs — and makes the DATA domain responsible for capturing those expectations, measuring against them, and reporting the result back. It follows that the same data element may carry several different quality expectations for different uses, and that a conflict between them is a governance question rather than a technical one.

### Implications
- Quality expectations must be recorded per data element and per use, stated by the using domain
- The same element may carry multiple expectations; conflicts are escalated, not averaged
- Quality measurement and reporting is a DATA-domain service; setting the target is not
- Data with no stated expectation is not assumed adequate — it is treated as ungoverned

### Outcomes
- Quality effort concentrates where a domain has said it matters
- Domains can evidence to their regulators that data quality is defined and measured against their stated needs
- Disputes about adequacy are resolved against a recorded expectation rather than by argument

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Data Carries Its Classification Wherever It Goes

### Qualified Name
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Domain Identifier
Data

### Summary
Sensitivity and criticality classifications are properties of the data itself and must survive copying, transformation, and movement between systems and domains.

### Description
Classification applied only at the system boundary protects data while it stays put and fails the moment it moves — which is exactly when protection matters most. Personal data extracted into an analysis dataset is still personal data; a critical manufacturing parameter copied into a spreadsheet is still critical. This principle requires classification to be attached to data rather than to its container, propagated through transformation and derivation, and preserved when data crosses into another domain's systems. It is the DATA domain's structural contribution to obligations that belong to privacy and security: those domains define what the classifications mean and what protection each demands, while the DATA domain makes classification a durable property that access controls, retention rules, and monitoring can act on wherever the data has reached. Derived data inherits the classification of its most sensitive input unless a documented assessment reduces it — aggregation and anonymisation are the usual grounds, and both require the assessment to be recorded rather than assumed.

### Implications
- Classification must be recorded as metadata that survives copying and transformation
- Derived data inherits its most sensitive input's classification unless a recorded assessment reduces it
- The meaning of each classification and the protection it demands is set by privacy and security, not by the DATA domain
- Systems receiving data from another domain must be able to read and honour the classification that arrives with it

### Outcomes
- Privacy can locate personal data wherever it has spread, including in derived datasets
- Security can assess exposure from classification rather than from system inventory alone
- Protection follows data across domain boundaries instead of stopping at them

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
Critical Data Must Be Traceable to Its Origin

### Qualified Name
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Domain Identifier
Data

### Summary
For data elements a domain has declared critical, the organisation must be able to show the path from the value in use back to the system and process that produced it.

### Description
Several domains carry obligations that are, at bottom, lineage obligations. GMP requires batch traceability. GCP requires clinical values to trace to source records. Corporate reporting must reconcile a published figure to its constituents. Each of these has historically been met by domain-specific effort — a manual reconstruction performed when an inspector asks — which is expensive, slow, and dependent on individuals who remember how a system was wired. This principle makes traceability a property of the data platform rather than an investigation: for elements declared critical, the transformations between origin and use are recorded as the data moves, so that the path can be produced on demand. It is deliberately scoped to critical elements, because capturing lineage for everything costs more than it returns and dilutes the coverage of what matters. The domains declare what is critical; the DATA domain is responsible for the lineage being there when asked.

### Implications
- Domains must declare which data elements are critical for their obligations
- Lineage must be captured as data moves, not reconstructed after the fact
- Transformation logic must be recorded alongside the movement, not only the source and target
- Lineage coverage for declared critical elements is measured and reported as a gap, not assumed complete

### Outcomes
- Inspection and audit questions about data origin are answered from the catalog rather than by investigation
- Impact of a source system change can be assessed before the change is made
- Domains can evidence traceability obligations without maintaining private lineage records

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

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
Data Quality Issues Must Be Reported and Resolved

### Qualified Name
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Domain Identifier
Data

### Summary
When data quality problems are detected, they must be reported to the responsible data owner and resolved within defined timeframes.

### Description
Data quality problems that are not detected and corrected can lead to incorrect decisions, failed processes, regulatory non-compliance, and patient harm. This obligation requires that data quality monitoring is in place, that quality failures generate notifications, that notifications reach the responsible owner, and that owners resolve issues within agreed service levels. Unresolved issues must be escalated.

### Implications
- Data quality rules must be defined for all critical data collections
- Automated monitoring must generate notifications when rules are violated
- Escalation paths must be defined for unresolved quality issues

### Outcomes
- Data quality problems are identified and fixed quickly
- Decisions are based on data that meets defined quality standards
- Regulatory requirements for data integrity are met

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Data Assets Must Be Registered in the Catalog Before Use

### Qualified Name
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Domain Identifier
Data

### Summary
Every data asset used for a governed business purpose must be registered in the Egeria catalog with its owner, classification, and the domain it serves recorded.

### Description
A data asset that is not catalogued cannot be governed by anything except the goodwill of whoever happens to maintain it. Registration is the point at which an asset acquires an accountable owner, a sensitivity classification, a statement of which domain relies on it, and a place from which its quality expectations and lineage can hang. The obligation applies to assets used for a governed purpose — supporting a regulatory obligation, a business decision of consequence, or a control another domain depends on — rather than to every file in the organisation, because an obligation that cannot be met is not a control. Registration is also the mechanism by which the proliferation threat is made tractable: discovery scanning finds assets nobody registered, and the gap between what was discovered and what was registered is itself the measure of how far governance has spread. New assets must be registered as they are created, and the obligation is not discharged by a periodic cataloguing exercise that is out of date by the time it completes.

### Implications
- Assets supporting a governed purpose must be registered before that use begins, not retrospectively
- Registration must record owner, classification, and the serving relationship to a domain
- Automated discovery must run against systems holding governed data to find unregistered assets
- The discovered-but-unregistered gap must be reported to the owning domain for resolution

### Outcomes
- Every governed data asset has a named owner who can be asked about it
- Privacy, security, and audit questions can be answered from the catalog rather than by survey
- The extent of ungoverned data is known rather than assumed

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Critical Data Elements Must Have Stated Quality Expectations

### Qualified Name
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Domain Identifier
Data

### Summary
Each data element a domain has declared critical must carry a recorded, measurable quality expectation stated by that domain, against which it is monitored.

### Description
This obligation is what makes fitness for purpose operational. A domain declaring an element critical must also state what "good enough" means for it — completeness, accuracy, timeliness, valid value ranges, and the consequence of falling short — in terms specific enough to be measured automatically. An expectation of "accurate" is not sufficient; an expectation that a batch temperature must be present for every recorded interval, within the validated instrument range, and available within fifteen minutes of measurement, is. The DATA domain provides the means to express, measure, and report; the domain that owns the obligation provides the target and receives the result. Where an element is critical to more than one domain, each domain's expectation is recorded separately, and the element is monitored against the strictest. Elements declared critical without an expectation are reported as a governance gap to the declaring domain rather than being quietly monitored against a default.

### Implications
- Expectations must be measurable automatically, not expressed as aspirations
- Elements critical to multiple domains carry multiple expectations and are monitored against the strictest
- The declaring domain sets the target and receives the measurement; the DATA domain does not set targets
- Critical elements without a stated expectation are reported as gaps, not defaulted

### Outcomes
- Quality monitoring covers what domains have said matters, at the level they specified
- Domains receive quality evidence in the terms their own regulators use
- Coverage gaps are visible to the domain accountable for closing them

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Cross-Department Data Sharing Must Be Governed by a Recorded Agreement

### Qualified Name
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Domain Identifier
Data

### Summary
Data flowing routinely between departments or to external parties must be covered by a recorded agreement stating purpose, permitted use, classification, quality expectation, and duration.

### Description
Routine data flows tend to begin as a favour between two teams and harden into dependencies nobody has examined. Years later the receiving team relies on a feed whose owner has changed twice, whose contents have drifted, and whose permitted use nobody can state. The obligation requires such flows to be recorded as agreements: what is shared, for what purpose, under what classification, to what quality expectation, and for how long. This serves several domains at once. Privacy requires a lawful basis and purpose limitation for personal data, and the agreement is where those are recorded for internal flows as well as external ones. Security needs to know what leaves a controlled boundary. Drug development and manufacturing need to know what quality they can rely on from an upstream feed before building a control on top of it. Agreements are reviewed when either party changes their systems, and a flow whose agreement has lapsed is stopped rather than allowed to continue unexamined.

### Implications
- Routine internal flows require agreements, not only external transfers
- Agreements must state purpose and permitted use, so that secondary use is a visible decision
- The quality expectation the receiver relies on must be recorded and agreed by the provider
- Lapsed or unreviewed agreements stop the flow rather than being allowed to continue

### Outcomes
- Data dependencies between departments are visible and attributable
- Privacy purpose limitation is enforceable for internal flows as well as external transfers
- Receiving teams build on a stated quality expectation rather than an assumption

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Obligation

### Display Name
Master and Reference Data Must Have a Single Authoritative Source

### Qualified Name
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Domain Identifier
Data

### Summary
For each master and reference data domain there must be exactly one authoritative source, with all other copies designated as replicas that do not originate change.

### Description
Master data — products, suppliers, materials, sites, people — and the reference data that codes it are used by every domain, which is why divergence in them is so damaging and so hard to detect. When two systems both accept changes to supplier records, they will diverge, and the divergence will surface as a reconciliation failure in a domain that had no part in creating it. This obligation requires each master and reference data domain to have one system designated as authoritative, with every other holding designated a replica that consumes changes and does not originate them. Where a business process genuinely requires local origination, the flow back into the authoritative source must be defined rather than left to periodic reconciliation. Reference data used in regulated processes carries an additional requirement: the version in force at a point in time must be recoverable, because a batch record or trial dataset coded under a superseded codelist must still be interpretable years later.

### Implications
- Each master and reference data domain must have a designated authoritative source recorded in the catalog
- Replicas must not originate change; where local origination is required, the write-back path must be defined
- Reference data versions must be retained so that historical coding remains interpretable
- Divergence between authoritative source and replica must be detected and reported, not discovered at reconciliation

### Outcomes
- Cross-department reporting reconciles without manual adjustment
- Regulated records remain interpretable under the codelists in force when they were created
- Divergence is caught as a control failure rather than as a reporting surprise

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

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
Automated Quality Monitoring

### Qualified Name
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Domain Identifier
Data

### Summary
Data quality will be monitored through automated rules that run continuously or on a schedule, generating alerts when quality thresholds are not met.

### Description
Manual data quality checking is slow, expensive, and inconsistent. Coco Pharmaceuticals will implement automated data quality monitoring — rules that check data against defined quality standards and generate alerts when problems are detected. Monitoring will run during low-load periods (e.g. nightly surveys) and continuously where real-time quality is critical. Alerts will be routed to the responsible data steward for investigation and resolution.

### Implications
- Data quality rules must be defined and documented for all critical data collections
- Automated quality scanning must be scheduled and results recorded in the metadata catalog
- Alerting and notification mechanisms must route quality failures to the right person

### Outcomes
- Data quality problems are detected quickly, often before they affect users
- Quality improvement over time can be measured and reported
- Manual quality checking effort is reduced

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Critical Data Element Identification

### Qualified Name
CocoPharma::GovernanceApproach::CriticalDataElementIdentification

### Domain Identifier
Data

### Summary
Each governance domain works with the DATA domain to identify the data elements its obligations actually depend on, and those elements receive the catalog, quality, lineage, and classification effort.

### Description
This approach is the mechanism through which the DATA domain learns what to serve. Rather than the data team deciding what matters, each domain is taken through its own obligations — a GMP requirement, a data subject right, a submission commitment, a reported financial figure — and asked which data elements the obligation would fail without. The result is a declared set of critical data elements per domain, each traceable to the obligation that makes it critical, which then drives everything downstream: these are the elements that receive quality expectations, lineage capture, classification review, and monitoring. The approach runs as a recurring engagement rather than a one-off exercise, because obligations change and new systems bring new dependencies. It also exposes disagreement usefully: where two domains declare the same element critical with incompatible expectations, the conflict surfaces at declaration time rather than at an audit. Elements that no domain declares critical are not neglected, but they receive baseline treatment rather than the full control set.

### Implications
- Criticality is declared by the domain that owns the obligation, with the obligation recorded alongside
- The declaration drives quality, lineage, and classification scope — it is not an inventory exercise
- Declarations must be revisited as obligations and systems change
- Conflicting expectations on a shared element are escalated at declaration, not at audit

### Outcomes
- DATA-domain effort is directed by the obligations of the domains it serves
- Each critical element can be traced to the regulatory or business obligation that makes it critical
- Domains understand their own data dependencies well enough to state them

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Subject Area Modelling

### Qualified Name
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Domain Identifier
Data

### Summary
Business concepts are organised into subject areas, each with an owner, agreed definitions, and a documented relationship to the systems that implement them.

### Description
Subject area modelling is the method by which the fragmented definitions threat is addressed structurally rather than by exhortation. The organisation's data is divided into subject areas — patient, product, batch, supplier, site, employee — each given an owner drawn from the domain with the strongest interest in it, and each carrying the agreed definitions of the concepts it contains, their relationships, and the systems where they are implemented. The model is deliberately business-facing: it describes what the organisation means, not how any system stores it, which is what allows several systems to be mapped to one definition and divergence to become visible. Where a department needs a variant of a shared concept, the variant is recorded in the model as a specialisation with the reason attached, rather than being allowed to exist silently as an incompatible field in a database. The subject area owner arbitrates definition changes, and the business glossary is the published face of the model.

### Implications
- Each subject area requires a named owner with authority to arbitrate definition disputes
- The model describes business meaning, kept separate from any system's implementation
- Justified departmental variants are recorded as specialisations with a stated reason
- Systems must be mapped to the model for divergence to be visible

### Outcomes
- Integration projects find an agreed definition rather than negotiating one
- Divergence between departments is visible as a modelled variant rather than hidden in schemas
- New systems can be assessed against existing definitions before they add new ones

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Approach

### Display Name
Federated Data Stewardship

### Qualified Name
CocoPharma::GovernanceApproach::FederatedDataStewardship

### Domain Identifier
Data

### Summary
Data stewardship is exercised within each business domain by people who understand the data, with the DATA domain providing method, tooling, and coordination rather than performing stewardship centrally.

### Description
Centralised stewardship fails because the central team does not know what the data means, and purely local stewardship fails because nothing reconciles the local decisions. This approach places stewards inside the domains — manufacturing, privacy, drug development, procurement — where the knowledge is, and makes the DATA domain responsible for the things that only work when done once: the method stewards follow, the tooling they record decisions in, the definitions they arbitrate against, and the forum where cross-domain conflicts are settled. It is the operational expression of the service relationship: the DATA domain does not steward other domains' data, it makes those domains able to steward it consistently. Stewards remain accountable to their own domain lead for the decisions they take, and to the DATA domain for following the common method — a split that requires the two accountabilities to be stated explicitly rather than left to emerge. This approach specialises the organisation-wide federated governance approach for data specifically.

### Implications
- Stewards sit within business domains and report to their domain lead for stewardship decisions
- The DATA domain owns the method, tooling, and the cross-domain arbitration forum
- Steward appointments must be recorded, with the subject areas and assets each covers
- Cross-domain conflicts must have a defined escalation route rather than being settled informally

### Outcomes
- Stewardship decisions are made by people who understand the data
- Decisions are recorded consistently enough to be reconciled across domains
- The DATA domain scales without needing knowledge of every business process

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Governance Controls — DATA Domain

Governance controls define how the governance policies are implemented.

---

### 3.1 Governance Roles

The Chief Data Officer (Jules Keeper) and Information Architect (Erin Overview) roles are defined in `joint-governance-officer-definitions.md`, together with their person role appointments. The roles below are the DATA-domain positions created by this program to carry federated stewardship and quality work.

Note that the Drug Development Lead, previously listed here as a DATA-domain role, belongs to the Drug Development domain (identifier 20) and is defined in `drug-development-governance.md`.

| Role | Appointed Person | Domain | Responsibility |
|------|-----------------|--------|---------------|
| Chief Data Officer | Jules Keeper | ALL | Overall governance program leadership and cross-domain coordination |
| Information Architect | Erin Overview | DATA | Data architecture, classification schemes, and subject area definitions |
| Subject Area Owner | *(per subject area)* | DATA | Definition ownership and dispute arbitration for one subject area |
| Data Quality Analyst | *(team)* | DATA | Quality expectation capture, rule implementation, and measurement reporting |

---

___

## Create Governance Role

### Display Name
Subject Area Owner

### Qualified Name
CocoPharma::GovernanceRole::SubjectAreaOwner

### Description
The Subject Area Owner holds definition authority for one subject area — patient, product, batch, supplier, site, or employee. The role agrees the definitions of the concepts in its area, arbitrates disputes when departments need incompatible variants, approves changes to definitions and reference data codelists, and confirms which system is the authoritative source for the master data in its area. Owners are drawn from the business domain with the strongest interest in the subject area rather than from the data team, and are accountable to their own domain lead for the decisions they take and to the Chief Data Officer for following the common method. One person may own more than one subject area.

### Scope
One business subject area — its concept definitions, relationships, reference data codelists, authoritative source designation, and recorded departmental variants.

### Headcount
6

### Category
Governance Role

### Search Keywords
- subject area ownership
- business glossary
- definition arbitration
- master data

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Role

### Display Name
Data Quality Analyst

### Qualified Name
CocoPharma::GovernanceRole::DataQualityAnalyst

### Description
The Data Quality Analyst works with each governance domain to turn its stated quality expectations into measurable rules, implements those rules in the monitoring platform, and reports results back to the domain that set the expectation. The role also maintains the critical data element register produced by the identification approach, tracks lineage coverage against it, and investigates the root cause of recurring quality failures — distinguishing a data entry problem from a system defect from an expectation that was never achievable as written. It does not set quality targets, which belong to the domain carrying the obligation.

### Scope
Quality rule implementation, measurement, and reporting across all domains; critical data element register maintenance; quality failure root cause analysis.

### Headcount
3

### Category
Governance Role

### Search Keywords
- data quality
- quality rules
- critical data elements
- measurement reporting

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
Percentage of Data Assets with Designated Owner

### Qualified Name
CocoPharma::GovernanceMetric::PercentageOfDataAssetsWithDesignatedOwner

### Domain Identifier
Data

### Summary
Measures the proportion of catalogued data assets that have a formally assigned and current owner.

### Description
This metric tracks progress towards the obligation that every information collection has a designated owner. It is calculated as (number of data assets with a current designated owner / total number of catalogued data assets) × 100. The target is 100%. Assets without an owner are at risk of quality degradation and governance failure.

### Implications
- Requires a complete and current inventory of data assets in the catalog
- Requires owner assignments to be kept current as staff change roles

### Outcomes
- Drives accountability for data governance across the organisation
- Identifies gaps where governance attention is needed

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Data Quality Rule Pass Rate

### Qualified Name
CocoPharma::GovernanceMetric::DataQualityRulePassRate

### Domain Identifier
Data

### Summary
Measures the percentage of automated data quality rule checks that pass within a reporting period.

### Description
This metric aggregates the results of all automated data quality rule checks run against Coco Pharmaceuticals' critical data collections. It is calculated as (number of rule checks that pass / total number of rule checks run) × 100. A declining pass rate indicates degrading data quality. A sustained high pass rate (target: ≥98%) indicates that data quality governance is effective.

### Implications
- Requires automated quality monitoring to be in place and consistently run
- Rule checks must be comprehensive enough to be meaningful

### Outcomes
- Provides an organisation-wide view of data quality health
- Enables governance team to identify domains or systems where quality is declining

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Open Data Quality Issues by Age

### Qualified Name
CocoPharma::GovernanceMetric::OpenDataQualityIssuesByAge

### Domain Identifier
Data

### Summary
Tracks the number of unresolved data quality issues and their age, to monitor whether issues are being resolved within agreed timeframes.

### Description
When a data quality rule failure generates an alert, the resulting issue must be investigated and resolved. This metric counts open (unresolved) quality issues and categorises them by age: less than 24 hours, 1–7 days, 7–30 days, and over 30 days. Issues outstanding for over 30 days are escalated to the CDO. The target is zero issues outstanding for over 7 days for critical data assets.

### Implications
- Requires a tracking mechanism for quality issue notifications and their resolution status
- Requires defined escalation paths and timeframes

### Outcomes
- Ensures that quality problems are not silently ignored
- Drives accountability for resolution
- Enables identification of systemic quality problems that require deeper intervention

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Critical Data Element Quality Expectation Coverage

### Qualified Name
CocoPharma::GovernanceMetric::CriticalDataExpectationCoverage

### Domain Identifier
Data

### Summary
Measures the percentage of declared critical data elements that carry a stated, measurable quality expectation and are actively monitored against it.

### Description
This metric reports the gap between what domains have declared critical and what is actually being measured. It is the primary indicator of whether the DATA domain is delivering the service it exists to provide, and it is deliberately expressed as coverage rather than as a quality score, because a high pass rate across a small fraction of critical elements is a worse position than a moderate pass rate across all of them and should not be allowed to look better. Reporting is broken down by the domain that declared the elements, since a low figure for one domain is a service failure to that domain specifically and is actionable in a way an organisation-wide average is not. Two failure modes are separated in the reporting: elements with no expectation stated, which is a gap the declaring domain must close, and elements with an expectation but no implemented rule, which is a gap the DATA domain must close. Target is 90% coverage with both gap types trending down.

### Implications
- Requires the critical data element register to be maintained as declarations change
- Reporting must separate "no expectation stated" from "expectation not yet implemented" so the gap is attributable
- Must be reported per declaring domain, not only in aggregate

### Outcomes
- Each domain can see how much of what it declared critical is actually monitored
- Service failures by the DATA domain are visible and distinguishable from declaration gaps
- Coverage is not obscured by a favourable pass rate on a narrow subset

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Catalog Registration Coverage

### Qualified Name
CocoPharma::GovernanceMetric::CatalogRegistrationCoverage

### Domain Identifier
Data

### Summary
Measures the percentage of data assets discovered by automated scanning that are registered in the catalog with an owner and classification recorded.

### Description
This metric measures the distance between the data estate the organisation knows about and the one it actually has. Discovery scanning across governed systems finds assets; the catalog records those that have been registered; the difference is ungoverned data. Because the metric depends on discovery, it improves in two quite different ways — by registering more assets, and by extending scanning to systems not previously covered — and the second of these will make the figure worse before it makes it better. The reporting therefore states scanned scope alongside the percentage, so that an expansion of scanning is not mistaken for a deterioration in governance. The metric is the primary indicator for the uncontrolled proliferation threat: a persistent gap in a particular system or department indicates copying that policy alone is not addressing, and the response is usually to find the legitimate need driving it. Target is 85% registration within scanned scope, with scanned scope expanding each quarter.

### Implications
- Requires automated discovery running against systems holding governed data
- Scanned scope must be reported alongside the percentage to keep the figure interpretable
- Persistent gaps by system or department must be investigated for the need driving the copying

### Outcomes
- The extent of ungoverned data is measured rather than estimated
- Expansion of governance coverage is visible and not penalised by the metric
- Proliferation hotspots are identified and their underlying cause addressed

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Lineage Coverage for Critical Data Elements

### Qualified Name
CocoPharma::GovernanceMetric::LineageCoverageForCriticalData

### Domain Identifier
Data

### Summary
Measures the percentage of declared critical data elements for which a complete lineage path from origin to point of use is available in the catalog.

### Description
This metric tests whether the traceability principle holds in practice for the elements that need it. Completeness is assessed end to end: a path that traces an element back three hops and then stops at an undocumented transformation does not count, because the question an inspector asks is about origin, not about intermediate steps. The metric is reported per declaring domain and, within that, per obligation, since the domains' traceability obligations differ in what they require — GMP batch traceability, GCP source-to-submission, and financial reconciliation each define a different origin. Manual lineage documentation is counted separately from automatically captured lineage, because manual records decay silently as systems change while automated capture does not; a high figure resting mostly on manual documentation is reported as such. Target is 95% for elements supporting a regulatory traceability obligation and 75% for other critical elements.

### Implications
- Requires lineage to be assessed end to end, with partial paths counted as gaps
- Manual and automated lineage must be counted separately, as manual records decay
- Reporting must be per domain and per obligation, since the required origin differs

### Outcomes
- Traceability obligations can be evidenced from the catalog on demand
- Decay in manually documented lineage is visible rather than discovered at inspection
- Gaps are attributable to the obligation they would cause to fail

### Authors
- Jules Keeper
- Erin Overview
- Peter Profile

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 3.3 Data Processing Purposes

The data processing purposes declared by this domain are defined in `6. data-privacy/data-processing-purposes.md`, together with those of every other domain and the links that connect them to the policies they implement. They remain owned by this domain and members of its folio; they are gathered there so that the lawful bases can be reviewed as a set.

## Part 4: Governance Links — DATA Domain

This section captures the relationships between governance definitions where at least one endpoint is a DATA-domain definition. Links between non-DATA definitions are in `joint-governance-officer-definitions.md`.

---

### 4.1 Governance Responses — Systemic DATA Drivers

These links record DATA-domain policies responding to the three systemic drivers the DATA domain owns. They are the only responses in this program where both endpoints belong to the DATA domain.

___

## Link Governance Response

### Driver
CocoPharma::Threat::FragmentedDataDefinitions

### Policy
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Rationale
The principle is the direct answer to the threat: agreed definitions maintained across departments are what prevent the same concept fragmenting into incompatible local variants.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FragmentedDataDefinitions

### Policy
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Rationale
Subject area modelling is the method by which fragmentation is addressed structurally — giving each concept an owner, an agreed definition, and a place where justified variants are recorded rather than hidden.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FragmentedDataDefinitions

### Policy
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Rationale
Fragmentation of master data is the most damaging form of this threat because every domain consumes it. Designating one authoritative source removes the mechanism by which divergence arises.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UncontrolledDataProliferation

### Policy
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Rationale
Registration combined with discovery scanning is what makes proliferation visible. A copy nobody registered and nobody discovered cannot be governed by any other control.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UncontrolledDataProliferation

### Policy
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Rationale
Copying is not going to stop, so the mitigation that matters is that a copy retains the classification of its source and remains subject to the protection that classification demands.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UncontrolledDataProliferation

### Policy
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Rationale
Recording routine flows as agreements converts undocumented copying into a governed dependency with a stated purpose, permitted use, and duration.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::TrustedDataFoundation

### Policy
CocoPharma::GovernanceApproach::CriticalDataElementIdentification

### Rationale
The imperative commits the DATA domain to serving other domains' obligations. Critical data element identification is the mechanism by which it learns what those obligations depend on.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::TrustedDataFoundation

### Policy
CocoPharma::GovernanceApproach::FederatedDataStewardship

### Rationale
A common foundation cannot be built by a central team that does not know what the data means. Federated stewardship is how the foundation is built with domain knowledge and kept consistent.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::TrustedDataFoundation

### Policy
CocoPharma::GovernancePrinciple::DataIsASharedOrganisationalResource

### Rationale
The principle states the premise the imperative acts on: data held by one department is an organisational asset that other domains have a legitimate claim on.

___

---

### 4.2 Service Responses — Drivers Owned by Other Domains

These links are the structural expression of the DATA domain's purpose. Each records a DATA-domain policy responding to a driver owned by manufacturing, privacy, drug development, security, or the corporate governance group. A DATA policy that appears nowhere in this section and nowhere in 4.1 is governance without a customer and should be reconsidered.

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Rationale
Personalised medicine requires that data about patients, treatments, and research can flow between departments without ambiguity. Common data definitions are the foundation for this.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernancePrinciple::DataIsASharedOrganisationalResource

### Rationale
On-demand, personalised treatment decisions require real-time access to data across research, manufacturing, clinical, and finance. Data must be shared — not siloed by department.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::CycleTimeReduction

### Policy
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Rationale
Reducing cycle times is only possible when data can be exchanged between departments without manual reconciliation. Common definitions eliminate that reconciliation overhead.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::CycleTimeReduction

### Policy
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Rationale
Manual quality checking adds latency to every process that depends on data. Automated monitoring detects problems quickly so that data consumers are not blocked by undetected quality issues.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::CycleTimeReduction

### Policy
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Rationale
Fast cycle times require fast resolution of data quality problems. The obligation to report and resolve issues within defined timeframes directly supports this imperative.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Policy
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Rationale
Documented, agreed data definitions in a shared catalog are the antidote to critical data knowledge being lost when key staff leave.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Policy
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Rationale
FDA regulations require that clinical trial data is accurate and that deviations are documented and investigated. The obligation to report and resolve quality issues ensures this standard is met.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Rationale
GMP requires that deviations from manufacturing standards are detected, documented, and investigated. The obligation to report and resolve data quality issues is the governance expression of this requirement.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Rationale
GMP batch traceability is a lineage obligation. Capturing lineage for manufacturing's declared critical elements is how the DATA domain lets manufacturing evidence it from the catalog rather than by reconstruction.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GoodManufacturingPractice

### Policy
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Rationale
Material, supplier, and site master data feeds every batch record. Divergence between replicas surfaces as a GMP traceability failure that manufacturing carries but did not cause.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::ManufacturingDataIntegrity

### Policy
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Rationale
Manufacturing states what its batch and equipment data must satisfy; the DATA domain captures those expectations as measurable rules and reports against them.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Rationale
Privacy cannot honour a data subject request over personal data it cannot locate. Classification surviving copying and derivation is what makes personal data findable wherever it has spread.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Rationale
Purpose limitation applies to internal flows as well as external transfers. Recording routine flows as agreements is where the purpose and permitted use of internal personal data movement is stated.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::UnauthorisedDataDisclosure

### Policy
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Rationale
Security cannot assess exposure across an estate it cannot enumerate. Catalog registration with recorded classification is what turns an inventory of systems into an assessment of what is actually at risk.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::CyberAttackOnOperationsOrData

### Policy
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Rationale
Incident response prioritises by what was exposed. Classification attached to the data rather than to the system is what allows that judgement to be made during an incident rather than after it.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::FDAClinicalTrialRegulations

### Policy
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Rationale
Tracing a submitted value back to its source record is a lineage requirement. The DATA domain provides the lineage; drug development retains the regulatory accountability for the submission.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::EUClinicalTrialsRegulation

### Policy
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Rationale
The 25-year retention obligation requires the reference data codelists in force at the time to remain recoverable, or archived trial data cannot be interpreted decades later.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::AcceleratedRegulatorySubmission

### Policy
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Rationale
The reconciliation work that delays submission is largely definitional. Agreed definitions upstream remove the mapping that drug development would otherwise perform per trial.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::FraudulentSupplierActivity

### Policy
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Rationale
Supplier fraud frequently exploits divergence between supplier records held in different systems. A single authoritative source removes the ambiguity that allows a fraudulent variant to pass as legitimate.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Threat::LossOfKeyTalentAndKnowledge

### Policy
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Rationale
Definitional knowledge held only by individuals leaves when they do. Recording it in the subject area model converts personal expertise into an organisational asset.

___

---

___

## Link Governance Response

### Driver
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Policy
CocoPharma::GovernancePrinciple::DataQualityFitForPurpose

### Rationale
Personalised medicine multiplies the number of small, fast data flows between research, manufacturing, and clinical care. Differentiated quality expectations are what keep effort proportionate across them.

___

---

### 4.3 Governance Mechanisms — DATA Policies linked to Controls

Each link below connects a DATA-domain governance policy to the metric that implements it.

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Mechanism
CocoPharma::GovernanceMetric::PercentageOfDataAssetsWithDesignatedOwner

### Rationale
This metric directly measures compliance with the obligation. A score below 100% identifies assets that lack governance accountability.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Mechanism
CocoPharma::GovernanceMetric::OpenDataQualityIssuesByAge

### Rationale
Tracking open issues by age measures whether the obligation to resolve quality problems within defined timeframes is being met. Issues ageing beyond the threshold are a direct compliance indicator.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Mechanism
CocoPharma::GovernanceMetric::DataQualityRulePassRate

### Rationale
The pass rate is the primary output metric for automated quality monitoring. A high and sustained pass rate confirms the approach is effective; a declining rate signals systemic quality problems.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Mechanism
CocoPharma::GovernanceMetric::OpenDataQualityIssuesByAge

### Rationale
Automated monitoring generates the issues tracked by this metric. Together, the approach and the metric form a detect-and-resolve feedback loop for data quality governance.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Mechanism
CocoPharma::GovernanceMetric::CriticalDataExpectationCoverage

### Rationale
The coverage metric measures the obligation directly, and separates the declaring domain's gap from the DATA domain's so that each is actionable by the party that can close it.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceApproach::CriticalDataElementIdentification

### Mechanism
CocoPharma::GovernanceMetric::CriticalDataExpectationCoverage

### Rationale
Coverage against declared critical elements is the feedback signal telling the identification approach whether declarations are being converted into working monitoring.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Mechanism
CocoPharma::GovernanceMetric::CatalogRegistrationCoverage

### Rationale
Registration coverage against discovered assets measures the obligation as written, and its gap is the observable form of the proliferation threat.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Mechanism
CocoPharma::GovernanceMetric::LineageCoverageForCriticalData

### Rationale
Lineage coverage tests whether the traceability principle holds for the elements that carry regulatory obligations, reported per obligation since each defines origin differently.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Mechanism
CocoPharma::GovernanceMetric::CatalogRegistrationCoverage

### Rationale
Registration records classification alongside ownership, so coverage is also the measure of how much of the estate carries a classification that downstream controls can act on.

___

---

___

## Link Governance Mechanism

### Policy
CocoPharma::GovernancePrinciple::DataQualityFitForPurpose

### Mechanism
CocoPharma::GovernanceMetric::DataQualityRulePassRate

### Rationale
The pass rate is only meaningful when measured against expectations the using domain has stated. Read together with expectation coverage it shows both how much is measured and how well it performs.

___

---

### 4.4 Peer Policy Links — Related DATA Policies

These links connect DATA-domain governance policies that reinforce or depend on each other.

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Governance Policy 2
CocoPharma::GovernancePrinciple::DataIsASharedOrganisationalResource

### Description
These principles are mutually dependent: data cannot be shared reliably without common definitions, and common definitions only add value when data is genuinely shared across the organisation.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::MetadataDrivenGovernance

### Governance Policy 2
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Description
Both approaches depend on the same metadata infrastructure. Automated quality monitoring is only possible when data assets, quality rules, and owners are captured as metadata in the catalog.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::DataQualityFitForPurpose

### Governance Policy 2
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Description
The principle states that quality is defined by the using domain; the obligation is the mechanism that captures what that domain actually said. Without the obligation the principle has no record to be measured against.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::CriticalDataElementIdentification

### Governance Policy 2
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Description
Identification determines which elements are critical; the obligation determines what each must satisfy. Running either without the other produces a register nobody measures or measurements against elements nobody declared important.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Governance Policy 2
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Description
The principle sets the requirement for agreed definitions; the approach is the method that produces and maintains them. The principle without the approach is an instruction with no route to compliance.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::FederatedDataStewardship

### Governance Policy 2
CocoPharma::GovernanceApproach::FederatedGovernanceWithCentralCoordination

### Description
The data stewardship approach specialises the organisation-wide federated governance approach for data, inheriting its central-coordination model and adding the subject area ownership and arbitration structures that data definitions specifically require.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Governance Policy 2
CocoPharma::GovernanceObligation::EachInformationCollectionHasDesignatedOwner

### Description
Registration is how the organisation-wide ownership obligation is discharged for data assets: the catalog entry is where the designated owner is recorded and from which ownership gaps are reported.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Description
The privacy obligation defines what the sensitivity classifications mean and what handling each demands; the data principle makes the classification durable enough to survive the copying and derivation that would otherwise strip it.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Governance Policy 2
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Description
Agreed definitions establish what a concept means; a single authoritative source establishes where its current value lives. Definitional agreement without source designation still permits two systems to hold different values for the same agreed concept.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::SecurityIncidentsLoggedReportedReviewed

### Governance Policy 2
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Description
Both obligations establish the same detect-report-resolve-within-timeframe pattern, one for security incidents and one for data quality issues, reinforcing a consistent approach to issue management across governance domains.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ThirdPartyScreeningBeforeOnboarding

### Governance Policy 2
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Description
Screening establishes that a supplier is legitimate; a single authoritative supplier record ensures the screened entity is the one that gets paid. Either without the other leaves the fraud route open.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::ReportedFiguresReconcileToSource

### Governance Policy 2
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Description
Financial reporting is the use case that most clearly demonstrates why lineage must be captured automatically: reconciliation performed by reconstruction is exactly what the reporting principle rules out.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::SerialNumberUniquenessAbsolute

### Governance Policy 2
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Description
Serial number allocation is the strictest instance of the single authoritative source obligation in the organisation: not merely that divergence is undesirable, but that a second generator produces an unrecoverable defect the moment it issues a number the first has already used.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernancePrinciple::KnowledgeOutlivesIndividual

### Governance Policy 2
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Description
Recording the meaning of data in the subject area model is one of the principal ways definitional knowledge is made to outlive the people who established it, which is why the DATA programme treats modelling as a knowledge-retention control.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::ModelsTestedForDifferentialPerformance

### Governance Policy 2
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Description
Establishing whether a model's training data represented a group requires tracing the data to its origin. Lineage is what makes the composition claim verifiable rather than asserted by the team that built the model.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceObligation::HazardousSubstanceRegisterMaintained

### Governance Policy 2
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Description
The substance register is master data in the sense the data programme means it: consumed by assessment, monitoring, waste routing, emergency response and transport classification, and damaging in exactly the way divergent master data is damaging when each of those maintains its own partial list instead.

___

---

### 4.5 Peer Driver Links — Related Systemic Drivers

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::Threat::FragmentedDataDefinitions

### Governance Driver 2
CocoPharma::Threat::UncontrolledDataProliferation

### Description
The two systemic data threats compound each other: uncontrolled copies drift away from their source definitions, and inconsistent definitions give departments a reason to make private copies rather than adopt a shared one. Addressing either in isolation leaves the other regenerating it.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::TrustedDataFoundation

### Governance Driver 2
CocoPharma::Threat::FragmentedDataDefinitions

### Description
Fragmentation is the principal obstacle the trusted foundation imperative exists to remove. The imperative states the goal in terms of what other domains gain; the threat states the same situation in terms of what the organisation loses by leaving it alone.

___

---

___

## Link Governance Drivers

### Governance Driver 1
CocoPharma::BusinessImperative::TrustedDataFoundation

### Governance Driver 2
CocoPharma::BusinessImperative::PersonalisedMedicineTransition

### Description
The personalised medicine transition is the corporate imperative that most depends on a common data foundation, since it requires research, manufacturing, and clinical data to combine at a speed that manual reconciliation cannot support.

___

---

## Part 5: External Reference Links — DATA Domain

___

## Link External Reference

### Element Name
CocoPharma::GovernanceMetric::DataQualityRulePassRate

### External Reference
CocoPharma::ExternalReference::Egeria::GovernanceDefinitionTypes

### Description
The GovernanceMetric open metadata type definition describes how this metric is represented and linked in the Egeria catalog.

___

---

---

## Part 6: Chief Data Officer Folio Members

The Chief Data Officer Governance Folio is created in `joint-governance-officer-definitions.md` and is already registered in the root collection. This file adds the DATA-domain definitions to it.

---

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::DataIsASharedOrganisationalResource

### Membership Rationale
The CDO is the sponsor of the cultural and governance shift from data silos to shared organisational data.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::CommonDataDefinitions

### Membership Rationale
Establishing and maintaining common data definitions is a core CDO responsibility.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::DataQualityIssuesMustBeReportedAndResolved

### Membership Rationale
The CDO sets the data quality standards and escalation paths that this obligation defines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::AutomatedQualityMonitoring

### Membership Rationale
The CDO owns the approach to automated data quality monitoring and is accountable for the tooling and processes that deliver it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::PercentageOfDataAssetsWithDesignatedOwner

### Membership Rationale
The CDO is responsible for reporting this metric to the board and for driving the action needed to reach 100%.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::DataQualityRulePassRate

### Membership Rationale
The CDO owns the organisation-wide data quality pass rate and uses it to assess the effectiveness of the data governance program.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::OpenDataQualityIssuesByAge

### Membership Rationale
The CDO reviews this metric to identify unresolved quality issues and trigger escalations where service levels are being missed.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::BusinessImperative::TrustedDataFoundation

### Membership Rationale
The imperative defining the DATA domain's service relationship to the rest of the organisation is owned by the Chief Data Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::Threat::FragmentedDataDefinitions

### Membership Rationale
Definitional fragmentation is a systemic data problem that no single business domain can resolve, and is owned in the DATA domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::Threat::UncontrolledDataProliferation

### Membership Rationale
Uncontrolled copying crosses every domain boundary and is visible only from the DATA domain, which therefore owns the threat.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::DataQualityFitForPurpose

### Membership Rationale
The principle placing quality definition with the using domain is a DATA-domain policy maintained by the Chief Data Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::ClassificationTravelsWithData

### Membership Rationale
Durable classification is the DATA domain's structural contribution to privacy and security obligations, and is maintained here.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernancePrinciple::CriticalDataTraceableToOrigin

### Membership Rationale
Lineage for declared critical elements is a DATA-domain service supporting traceability obligations owned by manufacturing, drug development, and corporate reporting.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::DataAssetsRegisteredInCatalog

### Membership Rationale
Catalog registration is the foundational DATA-domain obligation on which ownership, classification, and quality governance depend.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::QualityExpectationsForCriticalData

### Membership Rationale
Capturing and measuring domain-stated quality expectations is the DATA domain's core service obligation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::DataSharingGovernedByAgreement

### Membership Rationale
Governing routine data flows between departments is a DATA-domain obligation serving privacy purpose limitation and downstream quality reliance.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceObligation::SingleAuthoritativeSourceForMasterData

### Membership Rationale
Master and reference data source designation is owned in the DATA domain because every other domain consumes it.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::CriticalDataElementIdentification

### Membership Rationale
The approach by which the DATA domain learns what the other domains' obligations depend on is maintained by the Chief Data Officer.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::SubjectAreaModelling

### Membership Rationale
Subject area modelling is led by the Information Architect within the DATA domain and is the method addressing definitional fragmentation.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceApproach::FederatedDataStewardship

### Membership Rationale
The stewardship operating model is a DATA-domain approach, specialising the organisation-wide federated governance approach.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::CriticalDataExpectationCoverage

### Membership Rationale
The primary indicator of whether the DATA domain is delivering its service obligation, reported to the Chief Data Officer per declaring domain.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::CatalogRegistrationCoverage

### Membership Rationale
Registration coverage measures the extent of ungoverned data and is the observable form of the proliferation threat.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::GovernanceMetric::LineageCoverageForCriticalData

### Membership Rationale
Lineage coverage evidences the traceability obligations that other domains rely on the DATA domain to support.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefDataOfficer

### Element Id
CocoPharma::Risk::InconsistentDataDefinitionsReportingErrors

### Membership Rationale
Defined in the risk register with domain identifier DATA, this risk is the realisation of the fragmented definitions threat and belongs with the policies mitigating it.

### Membership Status
VALIDATED

___

---

## Appendix: Related Resources

| File | Contents |
|------|----------|
| `joint-governance-officer-definitions.md` | Shared drivers, cross-domain policies, governance roles, folios, and external references agreed at the joint governance leadership meeting — load this file first |
| `manufacturing-governance-program.md` | MANUFACTURING-domain program. Owns the GMP and Annex 11 drivers and the manufacturing data integrity imperative that Part 4.2 responds to |
| `privacy-governance-program.md` | PRIVACY-domain program. Owns the UK GDPR driver and the classification and purpose-limitation obligations that Part 4.2 responds to |
| `data-security-strategy.md` | SECURITY-domain program. Systemic alongside DATA, but owns board-level cyber drivers in its own right |
| `drug-development-governance.md` | Drug Development domain program (identifier 20). Owns the GCP, EU CTR, and clinical data reliability drivers that Part 4.2 responds to |
| `risk-register.md` | Threats and risks across all domains, including the inconsistent data definitions risk owned by this program |
| `data-strategy-framework.md` | Data strategy solution blueprint and the glossary terms underpinning the subject area model |
| `3. sustainability/sustainability-governance-definitions.md` | Sustainability domain governance definitions |
| `4. keeping-safe/martyns-law/` | Security scenario: Martyn's Law compliance definitions |

---

## Appendix: Domain Layering

The governance domains at Coco Pharmaceuticals are layered, and the layer determines which domain should own a given definition:

| Layer | Domains | Owns drivers? | Role |
|-------|---------|---------------|------|
| Business outcome and regulatory | MANUFACTURING, PRIVACY, Drug Development (20), CORPORATE | Yes | Carry responsibility for business results and regulatory compliance |
| Systemic | DATA, SECURITY | Sparingly | Address systemic issues across the business, in service of the outcome domains. SECURITY additionally owns board-level cyber drivers because cyber incidents can halt the whole business |
| Serving | IT_INFRASTRUCTURE, SOFTWARE_DEVELOPMENT | No | Provide the digital services the business runs on |

This program is shaped by that layering. Part 1 is short because DATA owns only genuinely systemic drivers; Part 4.2 is long because most DATA policies exist to serve obligations owned elsewhere.
