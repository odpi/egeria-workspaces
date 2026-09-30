# Quality Systems Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 15 digital products owned by the Quality Systems business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of quality, regulatory affairs and safety: safety reports and cases, assessments, signals and submissions; laboratory results, deviations and CAPAs, batch certification, serialisation alert investigations, excursion assessments, market authorisations; exposure bands, monitoring results and incidents.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Consolidated Safety Reports | `CocoPharma::SolutionComponent::SafetyIntakeGateway` | Event Stream | Safety Report |
| Product Complaints | `CocoPharma::SolutionComponent::ProductComplaintIntake` | Transactional Record | Complaint, Complaint Safety Assessment |
| Pharmacovigilance Cases | `CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement` | Transactional Record | Safety Case, Case Narrative, Case Follow-Up |
| Medical Assessments | `CocoPharma::SolutionComponent::MedicalAssessmentAndCoding` | Evidence Record | Medical Assessment, Coded Term |
| Safety Signals | `CocoPharma::SolutionComponent::SafetySignalDetection` | Insight | Safety Signal, Exposure Denominator |
| Regulatory Safety Submissions | `CocoPharma::SolutionComponent::RegulatorySafetySubmission` | Regulatory Submission | Safety Submission, Submission Acknowledgement |
| Laboratory Test Results | `CocoPharma::SolutionComponent::LaboratoryInformationManagement` | Evidence Record | Sample, Test Result, Certificate Of Analysis |
| Deviations And CAPAs | `CocoPharma::SolutionComponent::DeviationAndCAPAManagement` | Transactional Record | Deviation, Investigation, Corrective Action |
| Batch Certification Decisions | `CocoPharma::SolutionComponent::BatchReviewAndCertification` | Evidence Record | Certification Decision |
| Serialisation Alert Investigations | `CocoPharma::SolutionComponent::SerialisationAlertTriage` | Transactional Record | Alert Investigation, Alert Disposition |
| Temperature Excursion Assessments | `CocoPharma::SolutionComponent::ExcursionAssessment` | Evidence Record | Excursion Assessment |
| Market Authorisations | `CocoPharma::SolutionComponent::MarketAuthorisationRegister` | Master Data | Market Authorisation, Authorisation Condition |
| Occupational Exposure Bands | `CocoPharma::SolutionComponent::ExposureBandingRegister` | Reference Data | Substance Exposure Band, Band Containment Requirement |
| Exposure Monitoring Results | `CocoPharma::SolutionComponent::ExposureMonitoringCapture` | Evidence Record | Monitoring Campaign, Exposure Measurement |
| Incidents And Near Misses | `CocoPharma::SolutionComponent::IncidentAndNearMissReporting` | Transactional Record | Incident, Incident Investigation Finding |

For every product this file:

1. creates the **digital product** and adds it to the `Quality Systems` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

15 products, 30 data structures, 208 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret quality-systems.md
```

---

# Consolidated Safety Reports

*Solution component:* `CocoPharma::SolutionComponent::SafetyIntakeGateway`  
*Category:* Event Stream

Every suspected adverse reaction registered at the single point of intake, whatever door it arrived through: a clinician's report, a complaint with safety content or a trial site's report.  The statutory clock starts on first receipt anywhere in the company.

## Create Digital Product

### Display Name
Consolidated Safety Reports

### Product Name
Consolidated Safety Reports

### Qualified Name
DigitalProduct::Coco::Consolidated Safety Reports

### Description
Every suspected adverse reaction registered at the single point of intake, whatever door it arrived through: a clinician's report, a complaint with safety content or a trial site's report.  The statutory clock starts on first receipt anywhere in the company.

### Purpose
Gives case management one stream of reports with the receipt timestamp the regulators measure from.

### Category
Event Stream

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Consolidated Safety Reports

### Membership Rationale
Produced by the Quality Systems group's `SafetyIntakeGateway` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Consolidated Safety Reports Data Spec

### Qualified Name
DataSpec::Coco::Consolidated Safety Reports

### Description
The data structures and fields that make up the Consolidated Safety Reports digital product.

### Purpose
Describes the data a subscriber to Consolidated Safety Reports receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Consolidated Safety Reports

### Collection Id
DataSpec::Coco::Consolidated Safety Reports

### Label
data specification

___

## Create Data Structure

### Display Name
Safety Report

### Qualified Name
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Description
One row per suspected reaction registered.

### Namespace Path
coco_data_hub.consolidated_safety_reports

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Consolidated Safety Reports

### Element Id
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Membership Rationale
The Safety Report structure is part of the Consolidated Safety Reports data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Report Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Identifier

### Description
The report.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Report Received Timestamp

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Received Timestamp

### Description
When first received anywhere in the company.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Received Timestamp

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Safety Report Source Type

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Source Type

### Description
Clinician, complaint, trial site, literature or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Source Type

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Safety Report Source Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Source Identifier

### Description
The originating report or complaint.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Report Source Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Patient Pseudonym Identifier

### Description
The patient or participant, by pseudonym.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Product Code

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Batch Identifier

### Description
The batch, if known.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Batch Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Clinical Trial Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Clinical Trial Identifier

### Description
The trial, for a site report.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Clinical Trial Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Adverse Event Description

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Adverse Event Description

### Description
The reaction as reported.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Adverse Event Description

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Case Identifier

### Description
The case opened from the report.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Safety Reports::Safety Report::Safety Case Identifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: consolidated_safety_reports
- schemaDescription: Every suspected adverse reaction registered at the single point of intake, whatever door it arrived through: a clinician's report, a complaint with safety content or a trial site's report. The statutory clock starts on first receipt anywhere in the company.

### Anchor ID
DigitalProduct::Coco::Consolidated Safety Reports

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Consolidated Safety Reports

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Product Complaints

*Solution component:* `CocoPharma::SolutionComponent::ProductComplaintIntake`  
*Category:* Transactional Record

Complaints about product quality from pharmacies, distributors and patients, and the assessment that separates those which are also potential safety events from those which are not.  The separation is deliberately generous.

## Create Digital Product

### Display Name
Product Complaints

### Product Name
Product Complaints

### Qualified Name
DigitalProduct::Coco::Product Complaints

### Description
Complaints about product quality from pharmacies, distributors and patients, and the assessment that separates those which are also potential safety events from those which are not.  The separation is deliberately generous.

### Purpose
Records every complaint and routes those with safety content to intake on the day they arrive.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Product Complaints

### Membership Rationale
Produced by the Quality Systems group's `ProductComplaintIntake` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Product Complaints Data Spec

### Qualified Name
DataSpec::Coco::Product Complaints

### Description
The data structures and fields that make up the Product Complaints digital product.

### Purpose
Describes the data a subscriber to Product Complaints receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Product Complaints

### Collection Id
DataSpec::Coco::Product Complaints

### Label
data specification

___

## Create Data Structure

### Display Name
Complaint

### Qualified Name
DataStructure::Coco::Product Complaints::Complaint

### Description
One row per complaint received.

### Namespace Path
coco_data_hub.product_complaints

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Complaints

### Element Id
DataStructure::Coco::Product Complaints::Complaint

### Membership Rationale
The Complaint structure is part of the Product Complaints data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Complaint Identifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Complaint Identifier

### Description
The complaint.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Complaint Identifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Complaint Received Timestamp

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Complaint Received Timestamp

### Description
When received.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Complaint Received Timestamp

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Complaint Reporter Type

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Complaint Reporter Type

### Description
Pharmacy, distributor, patient, healthcare professional.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Complaint Reporter Type

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Product Code

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Batch Identifier

### Description
The batch, if known.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Batch Identifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Pack Serial Number

### Description
The pack, if known.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Pack Serial Number

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Complaint Description

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Complaint Description

### Description
The complaint.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Complaint Description

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Complaint Current Status

### Qualified Name
DataField::Coco::Product Complaints::Complaint::Complaint Current Status

### Description
Open, under investigation, closed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint::Complaint Current Status

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Complaint Safety Assessment

### Qualified Name
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Description
One row per complaint, whether it carries a potential safety event.

### Namespace Path
coco_data_hub.product_complaints

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Complaints

### Element Id
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Membership Rationale
The Complaint Safety Assessment structure is part of the Product Complaints data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Complaint Identifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Identifier

### Description
The complaint.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Identifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Complaint Safety Flag

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Safety Flag

### Description
Whether it is also a suspected adverse reaction.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Safety Flag

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Complaint Assessor Identifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Assessor Identifier

### Description
Who assessed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Assessor Identifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Complaint Assessment Timestamp

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Assessment Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint Safety Assessment::Complaint Assessment Timestamp

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Safety Report Identifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::Safety Report Identifier

### Description
The safety report raised, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Complaints::Complaint Safety Assessment::Safety Report Identifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: product_complaints
- schemaDescription: Complaints about product quality from pharmacies, distributors and patients, and the assessment that separates those which are also potential safety events from those which are not. The separation is deliberately generous.

### Anchor ID
DigitalProduct::Coco::Product Complaints

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Product Complaints

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Pharmacovigilance Cases

*Solution component:* `CocoPharma::SolutionComponent::PharmacovigilanceCaseManagement`  
*Category:* Transactional Record

The safety case from receipt through follow-up to closure, carrying the reporting clock that the regulators measure, with the narrative sent for assessment and the coded data that signal detection reads.  Every other component in the safety chain either feeds it or reads from it.

## Create Digital Product

### Display Name
Pharmacovigilance Cases

### Product Name
Pharmacovigilance Cases

### Qualified Name
DigitalProduct::Coco::Pharmacovigilance Cases

### Description
The safety case from receipt through follow-up to closure, carrying the reporting clock that the regulators measure, with the narrative sent for assessment and the coded data that signal detection reads.  Every other component in the safety chain either feeds it or reads from it.

### Purpose
Holds the case, its clock and its coded outcome in one place, so that reporting deadlines and signal detection work from the same record.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Pharmacovigilance Cases

### Membership Rationale
Produced by the Quality Systems group's `PharmacovigilanceCaseManagement` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Pharmacovigilance Cases Data Spec

### Qualified Name
DataSpec::Coco::Pharmacovigilance Cases

### Description
The data structures and fields that make up the Pharmacovigilance Cases digital product.

### Purpose
Describes the data a subscriber to Pharmacovigilance Cases receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Pharmacovigilance Cases

### Collection Id
DataSpec::Coco::Pharmacovigilance Cases

### Label
data specification

___

## Create Data Structure

### Display Name
Safety Case

### Qualified Name
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Description
One row per case.

### Namespace Path
coco_data_hub.pharmacovigilance_cases

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Pharmacovigilance Cases

### Element Id
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Membership Rationale
The Safety Case structure is part of the Pharmacovigilance Cases data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Identifier

### Description
The case.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Identifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Report Identifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Report Identifier

### Description
The report it was opened from.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Report Identifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Safety Case Received Timestamp

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Received Timestamp

### Description
The receipt timestamp the clock runs from.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Received Timestamp

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Product Code

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Safety Case Seriousness Code

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Seriousness Code

### Description
Serious or non-serious, once assessed.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Seriousness Code

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Safety Case Expectedness Code

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Expectedness Code

### Description
Expected or unexpected, once assessed.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Expectedness Code

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Safety Case Causality Code

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Causality Code

### Description
The causality assessment.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Causality Code

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Safety Case Reporting Due Date

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Reporting Due Date

### Description
When the regulatory report is due.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Reporting Due Date

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Safety Case Current Status

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Current Status

### Description
Open, awaiting assessment, follow-up, submitted, closed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Safety Case::Safety Case Current Status

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Data Structure

### Display Name
Case Narrative

### Qualified Name
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Description
One row per case, the narrative and patient context sent for medical assessment.

### Namespace Path
coco_data_hub.pharmacovigilance_cases

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Pharmacovigilance Cases

### Element Id
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Membership Rationale
The Case Narrative structure is part of the Pharmacovigilance Cases data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Identifier

### Description
The case.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Identifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Case Narrative Description

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Narrative Description

### Description
The clinical narrative.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Narrative Description

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Patient Birth Date

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Patient Birth Date

### Description
The patient's date of birth, where reported.

### Data Type
date

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Patient Birth Date

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Patient Sex Code

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Patient Sex Code

### Description
The patient's sex, where reported.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Patient Sex Code

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Safety Case Concomitant Description

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Concomitant Description

### Description
Other treatments in use.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Narrative::Safety Case Concomitant Description

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Structure

### Display Name
Case Follow-Up

### Qualified Name
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Description
One row per follow-up action on a case.

### Namespace Path
coco_data_hub.pharmacovigilance_cases

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Pharmacovigilance Cases

### Element Id
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Membership Rationale
The Case Follow-Up structure is part of the Pharmacovigilance Cases data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Identifier

### Description
The case.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Identifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Case Follow Up Number

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Number

### Description
The follow-up's sequence.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Number

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Safety Case Follow Up Date

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Date

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Date

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Safety Case Follow Up Description

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Description

### Description
What was requested or received.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::Safety Case Follow Up Description

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: pharmacovigilance_cases
- schemaDescription: The safety case from receipt through follow-up to closure, carrying the reporting clock that the regulators measure, with the narrative sent for assessment and the coded data that signal detection reads. Every other component in the safety chain either feeds it or reads from it.

### Anchor ID
DigitalProduct::Coco::Pharmacovigilance Cases

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Pharmacovigilance Cases

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Medical Assessments

*Solution component:* `CocoPharma::SolutionComponent::MedicalAssessmentAndCoding`  
*Category:* Evidence Record

The qualified medical judgement of seriousness, expectedness and causality for each case, and the coding of the event to the standard dictionary.  It is the step that decides whether a report is expedited or periodic.

## Create Digital Product

### Display Name
Medical Assessments

### Product Name
Medical Assessments

### Qualified Name
DigitalProduct::Coco::Medical Assessments

### Description
The qualified medical judgement of seriousness, expectedness and causality for each case, and the coding of the event to the standard dictionary.  It is the step that decides whether a report is expedited or periodic.

### Purpose
Returns to case management the assessment that sets the reporting route and the coded terms that signal detection depends on.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Medical Assessments

### Membership Rationale
Produced by the Quality Systems group's `MedicalAssessmentAndCoding` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Medical Assessments Data Spec

### Qualified Name
DataSpec::Coco::Medical Assessments

### Description
The data structures and fields that make up the Medical Assessments digital product.

### Purpose
Describes the data a subscriber to Medical Assessments receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Medical Assessments

### Collection Id
DataSpec::Coco::Medical Assessments

### Label
data specification

___

## Create Data Structure

### Display Name
Medical Assessment

### Qualified Name
DataStructure::Coco::Medical Assessments::Medical Assessment

### Description
One row per assessment of a case.

### Namespace Path
coco_data_hub.medical_assessments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Medical Assessments

### Element Id
DataStructure::Coco::Medical Assessments::Medical Assessment

### Membership Rationale
The Medical Assessment structure is part of the Medical Assessments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Identifier

### Description
The case.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Identifier

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Case Assessment Timestamp

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessment Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessment Timestamp

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Safety Case Assessor Identifier

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessor Identifier

### Description
The assessing physician.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessor Identifier

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Safety Case Seriousness Code

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Seriousness Code

### Description
Serious or non-serious.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Seriousness Code

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Safety Case Expectedness Code

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Expectedness Code

### Description
Expected or unexpected against the label.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Expectedness Code

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Safety Case Causality Code

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Causality Code

### Description
The causality assessment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Causality Code

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Safety Case Assessment Notes

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessment Notes

### Description
The assessor's reasoning.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Medical Assessment::Safety Case Assessment Notes

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Coded Term

### Qualified Name
DataStructure::Coco::Medical Assessments::Coded Term

### Description
One row per dictionary term coded against a case.

### Namespace Path
coco_data_hub.medical_assessments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Medical Assessments

### Element Id
DataStructure::Coco::Medical Assessments::Coded Term

### Membership Rationale
The Coded Term structure is part of the Medical Assessments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::Safety Case Identifier

### Description
The case.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Coded Term::Safety Case Identifier

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Adverse Event Code

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Code

### Description
The dictionary code.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Code

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Adverse Event Dictionary Version

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Dictionary Version

### Description
The dictionary version.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Dictionary Version

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Adverse Event Term Name

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Term Name

### Description
The term.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Term Name

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Adverse Event Primary Flag

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Primary Flag

### Description
Whether this is the primary event.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Medical Assessments::Coded Term::Adverse Event Primary Flag

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: medical_assessments
- schemaDescription: The qualified medical judgement of seriousness, expectedness and causality for each case, and the coding of the event to the standard dictionary. It is the step that decides whether a report is expedited or periodic.

### Anchor ID
DigitalProduct::Coco::Medical Assessments

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Medical Assessments

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Safety Signals

*Solution component:* `CocoPharma::SolutionComponent::SafetySignalDetection`  
*Category:* Insight

The patterns found across accumulated cases that no single case shows, with the exposure denominators they were assessed against, and the referrals made to quality and to the authorisation register.  A signal visible across trial and post-market data is invisible in either alone.

## Create Digital Product

### Display Name
Safety Signals

### Product Name
Safety Signals

### Qualified Name
DigitalProduct::Coco::Safety Signals

### Description
The patterns found across accumulated cases that no single case shows, with the exposure denominators they were assessed against, and the referrals made to quality and to the authorisation register.  A signal visible across trial and post-market data is invisible in either alone.

### Purpose
Turns the accumulated cases into signals that quality investigation and label changes can act on.

### Category
Insight

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Safety Signals

### Membership Rationale
Produced by the Quality Systems group's `SafetySignalDetection` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Safety Signals Data Spec

### Qualified Name
DataSpec::Coco::Safety Signals

### Description
The data structures and fields that make up the Safety Signals digital product.

### Purpose
Describes the data a subscriber to Safety Signals receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Safety Signals

### Collection Id
DataSpec::Coco::Safety Signals

### Label
data specification

___

## Create Data Structure

### Display Name
Safety Signal

### Qualified Name
DataStructure::Coco::Safety Signals::Safety Signal

### Description
One row per signal detected.

### Namespace Path
coco_data_hub.safety_signals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Safety Signals

### Element Id
DataStructure::Coco::Safety Signals::Safety Signal

### Membership Rationale
The Safety Signal structure is part of the Safety Signals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Signal Identifier

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Identifier

### Description
The signal.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Identifier

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Signal Detected Date

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Detected Date

### Description
When detected.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Detected Date

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Product Code

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Adverse Event Code

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Adverse Event Code

### Description
The event term.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Adverse Event Code

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Signal Contributing Count

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Contributing Count

### Description
The number of cases contributing.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Contributing Count

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Signal Description

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Description

### Description
The pattern observed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Description

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Signal Current Status

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Current Status

### Description
Detected, under evaluation, confirmed, refuted.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Current Status

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Signal Referral Type

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::Signal Referral Type

### Description
Referred to quality, to authorisation, both or neither.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Safety Signal::Signal Referral Type

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Exposure Denominator

### Qualified Name
DataStructure::Coco::Safety Signals::Exposure Denominator

### Description
One row per product per period, the exposure the signal rate was measured against.

### Namespace Path
coco_data_hub.safety_signals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Safety Signals

### Element Id
DataStructure::Coco::Safety Signals::Exposure Denominator

### Membership Rationale
The Exposure Denominator structure is part of the Safety Signals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Exposure Denominator::Product Code

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Exposure Period Code

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Period Code

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Exposure Count

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Count

### Description
The estimated number of patients exposed.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Count

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Exposure Source Description

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Source Description

### Description
How the estimate was derived.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Safety Signals::Exposure Denominator::Exposure Source Description

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: safety_signals
- schemaDescription: The patterns found across accumulated cases that no single case shows, with the exposure denominators they were assessed against, and the referrals made to quality and to the authorisation register. A signal visible across trial and post-market data is invisible in either alone.

### Anchor ID
DigitalProduct::Coco::Safety Signals

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Safety Signals

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Regulatory Safety Submissions

*Solution component:* `CocoPharma::SolutionComponent::RegulatorySafetySubmission`  
*Category:* Regulatory Submission

The expedited and periodic safety reports formatted and transmitted to the regulator of each market the product is authorised in, and the acknowledgement each received.  An unacknowledged submission is not a submission.

## Create Digital Product

### Display Name
Regulatory Safety Submissions

### Product Name
Regulatory Safety Submissions

### Qualified Name
DigitalProduct::Coco::Regulatory Safety Submissions

### Description
The expedited and periodic safety reports formatted and transmitted to the regulator of each market the product is authorised in, and the acknowledgement each received.  An unacknowledged submission is not a submission.

### Purpose
Proves, per market, that each report went out on time and was received.

### Category
Regulatory Submission

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Regulatory Safety Submissions

### Membership Rationale
Produced by the Quality Systems group's `RegulatorySafetySubmission` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Regulatory Safety Submissions Data Spec

### Qualified Name
DataSpec::Coco::Regulatory Safety Submissions

### Description
The data structures and fields that make up the Regulatory Safety Submissions digital product.

### Purpose
Describes the data a subscriber to Regulatory Safety Submissions receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Regulatory Safety Submissions

### Collection Id
DataSpec::Coco::Regulatory Safety Submissions

### Label
data specification

___

## Create Data Structure

### Display Name
Safety Submission

### Qualified Name
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Description
One row per report submitted to a regulator.

### Namespace Path
coco_data_hub.regulatory_safety_submissions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Regulatory Safety Submissions

### Element Id
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Membership Rationale
The Safety Submission structure is part of the Regulatory Safety Submissions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Submission Identifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Identifier

### Description
The submission.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Identifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Safety Case Identifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Safety Case Identifier

### Description
The case, for an expedited report.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Safety Case Identifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Product Code

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Market Code

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Market Code

### Description
The market.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
8

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Market Code

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Submission Regulator Code

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Regulator Code

### Description
The regulator.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Regulator Code

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Submission Type

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Type

### Description
Expedited or periodic.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Type

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Submission Due Date

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Due Date

### Description
When due.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Due Date

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Submission Timestamp

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Timestamp

### Description
When transmitted.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Timestamp

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Submission Format Code

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Format Code

### Description
The format used.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Safety Submission::Submission Format Code

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Submission Acknowledgement

### Qualified Name
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Description
One row per acknowledgement received.

### Namespace Path
coco_data_hub.regulatory_safety_submissions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Regulatory Safety Submissions

### Element Id
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Membership Rationale
The Submission Acknowledgement structure is part of the Regulatory Safety Submissions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Submission Acknowledgement Identifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledgement Identifier

### Description
The regulator's reference.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledgement Identifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Submission Identifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Identifier

### Description
The submission.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Identifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Submission Acknowledged Timestamp

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledged Timestamp

### Description
When acknowledged.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledged Timestamp

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Submission Acknowledgement Status

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledgement Status

### Description
Accepted, rejected or queried.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::Submission Acknowledgement Status

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: regulatory_safety_submissions
- schemaDescription: The expedited and periodic safety reports formatted and transmitted to the regulator of each market the product is authorised in, and the acknowledgement each received. An unacknowledged submission is not a submission.

### Anchor ID
DigitalProduct::Coco::Regulatory Safety Submissions

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Regulatory Safety Submissions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Laboratory Test Results

*Solution component:* `CocoPharma::SolutionComponent::LaboratoryInformationManagement`  
*Category:* Evidence Record

Sampling, testing and results for raw materials, in-process checks and finished product, compared against specification, and the certificates of analysis issued for release.  Results are gates rather than reports: material cannot be issued and product cannot be released until the laboratory has answered.

## Create Digital Product

### Display Name
Laboratory Test Results

### Product Name
Laboratory Test Results

### Qualified Name
DigitalProduct::Coco::Laboratory Test Results

### Description
Sampling, testing and results for raw materials, in-process checks and finished product, compared against specification, and the certificates of analysis issued for release.  Results are gates rather than reports: material cannot be issued and product cannot be released until the laboratory has answered.

### Purpose
Answers, for each sample, whether the material or product meets its specification.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Laboratory Test Results

### Membership Rationale
Produced by the Quality Systems group's `LaboratoryInformationManagement` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Laboratory Test Results Data Spec

### Qualified Name
DataSpec::Coco::Laboratory Test Results

### Description
The data structures and fields that make up the Laboratory Test Results digital product.

### Purpose
Describes the data a subscriber to Laboratory Test Results receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Laboratory Test Results

### Collection Id
DataSpec::Coco::Laboratory Test Results

### Label
data specification

___

## Create Data Structure

### Display Name
Sample

### Qualified Name
DataStructure::Coco::Laboratory Test Results::Sample

### Description
One row per sample taken for testing.

### Namespace Path
coco_data_hub.laboratory_test_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Laboratory Test Results

### Element Id
DataStructure::Coco::Laboratory Test Results::Sample

### Membership Rationale
The Sample structure is part of the Laboratory Test Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Sample Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Sample Identifier

### Description
The sample.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Sample Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Sample Type

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Sample Type

### Description
Raw material, in-process or finished product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Sample Type

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Lot Identifier

### Description
The material lot, for raw material.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Lot Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Batch Identifier

### Description
The batch, for in-process and finished product.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Batch Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Sample Collection Timestamp

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Sample Collection Timestamp

### Description
When taken.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Sample Collection Timestamp

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Sample Current Status

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::Sample Current Status

### Description
Received, in test, complete.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Sample::Sample Current Status

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Test Result

### Qualified Name
DataStructure::Coco::Laboratory Test Results::Test Result

### Description
One row per test on a sample.

### Namespace Path
coco_data_hub.laboratory_test_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Laboratory Test Results

### Element Id
DataStructure::Coco::Laboratory Test Results::Test Result

### Membership Rationale
The Test Result structure is part of the Laboratory Test Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Test Result Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Result Identifier

### Description
The result.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Result Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Sample Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Sample Identifier

### Description
The sample.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Sample Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Test Code

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Code

### Description
The test.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Code

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Test Value

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Value

### Description
The result.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Value

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Test Unit

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Unit

### Description
The unit.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Unit

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Specification Minimum Value

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Specification Minimum Value

### Description
The lower limit.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Specification Minimum Value

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Specification Maximum Value

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Specification Maximum Value

### Description
The upper limit.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Specification Maximum Value

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Test Conformity Flag

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Conformity Flag

### Description
Whether the result is within specification.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Conformity Flag

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Test Completed Timestamp

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Completed Timestamp

### Description
When completed.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Completed Timestamp

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Test Analyst Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::Test Analyst Identifier

### Description
The analyst.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Test Result::Test Analyst Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Data Structure

### Display Name
Certificate Of Analysis

### Qualified Name
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Description
One row per certificate issued for a batch or lot.

### Namespace Path
coco_data_hub.laboratory_test_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Laboratory Test Results

### Element Id
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Membership Rationale
The Certificate Of Analysis structure is part of the Laboratory Test Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Identifier

### Description
The certificate.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Batch Identifier

### Description
The batch, for finished product.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Batch Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Lot Identifier

### Description
The lot, for material.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Lot Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Certificate Date

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Date

### Description
When issued.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Date

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Certificate Conformity Flag

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Conformity Flag

### Description
Whether every test conformed.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Conformity Flag

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Certificate Approver Identifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Approver Identifier

### Description
Who approved the certificate.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::Certificate Approver Identifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: laboratory_test_results
- schemaDescription: Sampling, testing and results for raw materials, in-process checks and finished product, compared against specification, and the certificates of analysis issued for release. Results are gates rather than reports: material cannot be issued and product cannot be released until the laboratory has answered.

### Anchor ID
DigitalProduct::Coco::Laboratory Test Results

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Laboratory Test Results

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Deviations And CAPAs

*Solution component:* `CocoPharma::SolutionComponent::DeviationAndCAPAManagement`  
*Category:* Transactional Record

Departures from the approved process, their investigation and the corrective and preventive actions that follow, including the signals referred from safety.  An open deviation is a gate on certification, so this sits inside the release flow rather than beside it.

## Create Digital Product

### Display Name
Deviations And CAPAs

### Product Name
Deviations And CAPAs

### Qualified Name
DigitalProduct::Coco::Deviations And CAPAs

### Description
Departures from the approved process, their investigation and the corrective and preventive actions that follow, including the signals referred from safety.  An open deviation is a gate on certification, so this sits inside the release flow rather than beside it.

### Purpose
Gives the batch record and the certifying Qualified Person the disposition of every deviation that touched a batch.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Deviations And CAPAs

### Membership Rationale
Produced by the Quality Systems group's `DeviationAndCAPAManagement` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Deviations And CAPAs Data Spec

### Qualified Name
DataSpec::Coco::Deviations And CAPAs

### Description
The data structures and fields that make up the Deviations And CAPAs digital product.

### Purpose
Describes the data a subscriber to Deviations And CAPAs receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Deviations And CAPAs

### Collection Id
DataSpec::Coco::Deviations And CAPAs

### Label
data specification

___

## Create Data Structure

### Display Name
Deviation

### Qualified Name
DataStructure::Coco::Deviations And CAPAs::Deviation

### Description
One row per deviation raised.

### Namespace Path
coco_data_hub.deviations_and_capas

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Deviations And CAPAs

### Element Id
DataStructure::Coco::Deviations And CAPAs::Deviation

### Membership Rationale
The Deviation structure is part of the Deviations And CAPAs data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Deviation Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Identifier

### Description
The deviation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Deviation Raised Timestamp

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Raised Timestamp

### Description
When raised.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Raised Timestamp

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Deviation Source Type

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Source Type

### Description
Manufacturing execution, safety signal, audit or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Source Type

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Batch Identifier

### Description
The batch affected, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Batch Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Product Code

### Description
The product affected.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Product Code

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Signal Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Signal Identifier

### Description
The safety signal referred, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Signal Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Deviation Description

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Description

### Description
The departure and its context.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Description

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Deviation Severity

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Severity

### Description
Minor, major or critical.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Severity

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Deviation Current Status

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Current Status

### Description
Open, under investigation, dispositioned, closed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Deviation::Deviation Current Status

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Investigation

### Qualified Name
DataStructure::Coco::Deviations And CAPAs::Investigation

### Description
One row per deviation, the investigation outcome and impact on the batch.

### Namespace Path
coco_data_hub.deviations_and_capas

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Deviations And CAPAs

### Element Id
DataStructure::Coco::Deviations And CAPAs::Investigation

### Membership Rationale
The Investigation structure is part of the Deviations And CAPAs data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Deviation Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Identifier

### Description
The deviation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Deviation Investigator Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Investigator Identifier

### Description
Who investigated.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Investigator Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Deviation Investigation Completed Date

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Investigation Completed Date

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Investigation Completed Date

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Deviation Root Cause Description

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Root Cause Description

### Description
The root cause found.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Root Cause Description

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Deviation Impact Description

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Impact Description

### Description
The impact on the batch.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Impact Description

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Deviation Disposition Status

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Disposition Status

### Description
No impact, rework, reject, or release with justification.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Investigation::Deviation Disposition Status

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Corrective Action

### Qualified Name
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Description
One row per corrective or preventive action.

### Namespace Path
coco_data_hub.deviations_and_capas

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Deviations And CAPAs

### Element Id
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Membership Rationale
The Corrective Action structure is part of the Deviations And CAPAs data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Corrective Action Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Identifier

### Description
The action.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Deviation Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Deviation Identifier

### Description
The deviation it addresses.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Deviation Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Corrective Action Type

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Type

### Description
Corrective or preventive.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Type

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Corrective Action Description

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Description

### Description
The action.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Description

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Corrective Action Owner Identifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Owner Identifier

### Description
Who owns it.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Owner Identifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Corrective Action Due Date

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Due Date

### Description
When due.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Due Date

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Corrective Action Current Status

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Current Status

### Description
Open, complete, verified.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Deviations And CAPAs::Corrective Action::Corrective Action Current Status

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: deviations_and_capas
- schemaDescription: Departures from the approved process, their investigation and the corrective and preventive actions that follow, including the signals referred from safety. An open deviation is a gate on certification, so this sits inside the release flow rather than beside it.

### Anchor ID
DigitalProduct::Coco::Deviations And CAPAs

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Deviations And CAPAs

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Batch Certification Decisions

*Solution component:* `CocoPharma::SolutionComponent::BatchReviewAndCertification`  
*Category:* Evidence Record

The review of each assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market.  It is the single human decision the whole chain exists to support, and it is market-specific.

## Create Digital Product

### Display Name
Batch Certification Decisions

### Product Name
Batch Certification Decisions

### Qualified Name
DigitalProduct::Coco::Batch Certification Decisions

### Description
The review of each assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market.  It is the single human decision the whole chain exists to support, and it is market-specific.

### Purpose
Records who certified which batch for which market, on what record, and what they found.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Batch Certification Decisions

### Membership Rationale
Produced by the Quality Systems group's `BatchReviewAndCertification` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Batch Certification Decisions Data Spec

### Qualified Name
DataSpec::Coco::Batch Certification Decisions

### Description
The data structures and fields that make up the Batch Certification Decisions digital product.

### Purpose
Describes the data a subscriber to Batch Certification Decisions receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Batch Certification Decisions

### Collection Id
DataSpec::Coco::Batch Certification Decisions

### Label
data specification

___

## Create Data Structure

### Display Name
Certification Decision

### Qualified Name
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Description
One row per batch per market reviewed.

### Namespace Path
coco_data_hub.batch_certification_decisions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Batch Certification Decisions

### Element Id
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Membership Rationale
The Certification Decision structure is part of the Batch Certification Decisions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Identifier

### Description
The batch.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Identifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Market Code

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Market Code

### Description
The market.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
8

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Market Code

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Batch Certifier Identifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certifier Identifier

### Description
The Qualified Person.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certifier Identifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Batch Certification Date

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Date

### Description
When decided.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Date

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Batch Certification Status

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Status

### Description
Certified, rejected or held.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Status

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Batch Released Quantity

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Released Quantity

### Description
The quantity released to the market.

### Data Type
int

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Released Quantity

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Batch Record Complete Flag

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Record Complete Flag

### Description
Whether the record reviewed was complete.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Record Complete Flag

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Deviation Identifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Deviation Identifier

### Description
An open deviation that held the batch, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Deviation Identifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Batch Certification Notes

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Notes

### Description
The reviewer's findings.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Batch Certification Notes

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Shipment Storage Description

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::Shipment Storage Description

### Description
The storage conditions the released therapy must be shipped under.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Certification Decisions::Certification Decision::Shipment Storage Description

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: batch_certification_decisions
- schemaDescription: The review of each assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market. It is the single human decision the whole chain exists to support, and it is market-specific.

### Anchor ID
DigitalProduct::Coco::Batch Certification Decisions

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Batch Certification Decisions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Serialisation Alert Investigations

*Solution component:* `CocoPharma::SolutionComponent::SerialisationAlertTriage`  
*Category:* Transactional Record

The investigation of verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals, and the disposition returned to the serialisation repository.  An alert not investigated is a falsification signal received and ignored.

## Create Digital Product

### Display Name
Serialisation Alert Investigations

### Product Name
Serialisation Alert Investigations

### Qualified Name
DigitalProduct::Coco::Serialisation Alert Investigations

### Description
The investigation of verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals, and the disposition returned to the serialisation repository.  An alert not investigated is a falsification signal received and ignored.

### Purpose
Closes every alert with a cause and, where the cause was the company's own data, a correction.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Serialisation Alert Investigations

### Membership Rationale
Produced by the Quality Systems group's `SerialisationAlertTriage` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Serialisation Alert Investigations Data Spec

### Qualified Name
DataSpec::Coco::Serialisation Alert Investigations

### Description
The data structures and fields that make up the Serialisation Alert Investigations digital product.

### Purpose
Describes the data a subscriber to Serialisation Alert Investigations receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Serialisation Alert Investigations

### Collection Id
DataSpec::Coco::Serialisation Alert Investigations

### Label
data specification

___

## Create Data Structure

### Display Name
Alert Investigation

### Qualified Name
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Description
One row per alert investigated.

### Namespace Path
coco_data_hub.serialisation_alert_investigations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Serialisation Alert Investigations

### Element Id
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Membership Rationale
The Alert Investigation structure is part of the Serialisation Alert Investigations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Alert Identifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Identifier

### Description
The alert.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Identifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Pack Serial Number

### Description
The identifier.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Pack Serial Number

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Alert Investigator Identifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigator Identifier

### Description
Who investigated.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigator Identifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Alert Investigation Start Timestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation Start Timestamp

### Description
When opened.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation Start Timestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Alert Investigation End Timestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation End Timestamp

### Description
When closed.

### Data Type
date

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation End Timestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Alert Root Cause Type

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Root Cause Type

### Description
Data error, scanning error, expired product, suspected falsification, other.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Root Cause Type

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Alert Investigation Notes

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation Notes

### Description
What was found.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Investigation Notes

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Alert Current Status

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Current Status

### Description
Open, closed, escalated.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::Alert Current Status

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Alert Disposition

### Qualified Name
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Description
One row per disposition returned for an alert.

### Namespace Path
coco_data_hub.serialisation_alert_investigations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Serialisation Alert Investigations

### Element Id
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Membership Rationale
The Alert Disposition structure is part of the Serialisation Alert Investigations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Alert Identifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Identifier

### Description
The alert.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Identifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Alert Disposition Timestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Disposition Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Disposition Timestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Alert Disposition Type

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Disposition Type

### Description
Correct repository, decommission, recall, report to authority, no action.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Disposition Type

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Alert Affected Count

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Affected Count

### Description
The number of identifiers affected.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Alert Affected Count

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Corrective Action Identifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Corrective Action Identifier

### Description
The CAPA raised, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::Corrective Action Identifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: serialisation_alert_investigations
- schemaDescription: The investigation of verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals, and the disposition returned to the serialisation repository. An alert not investigated is a falsification signal received and ignored.

### Anchor ID
DigitalProduct::Coco::Serialisation Alert Investigations

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Serialisation Alert Investigations

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Temperature Excursion Assessments

*Solution component:* `CocoPharma::SolutionComponent::ExcursionAssessment`  
*Category:* Evidence Record

The assessment of each temperature excursion against the product's stability data, and the disposition of the consignment.  It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

## Create Digital Product

### Display Name
Temperature Excursion Assessments

### Product Name
Temperature Excursion Assessments

### Qualified Name
DigitalProduct::Coco::Temperature Excursion Assessments

### Description
The assessment of each temperature excursion against the product's stability data, and the disposition of the consignment.  It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

### Purpose
Decides, with evidence, whether a consignment that left its range may still be used.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Temperature Excursion Assessments

### Membership Rationale
Produced by the Quality Systems group's `ExcursionAssessment` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Temperature Excursion Assessments Data Spec

### Qualified Name
DataSpec::Coco::Temperature Excursion Assessments

### Description
The data structures and fields that make up the Temperature Excursion Assessments digital product.

### Purpose
Describes the data a subscriber to Temperature Excursion Assessments receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Temperature Excursion Assessments

### Collection Id
DataSpec::Coco::Temperature Excursion Assessments

### Label
data specification

___

## Create Data Structure

### Display Name
Excursion Assessment

### Qualified Name
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Description
One row per excursion assessed.

### Namespace Path
coco_data_hub.temperature_excursion_assessments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Temperature Excursion Assessments

### Element Id
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Membership Rationale
The Excursion Assessment structure is part of the Temperature Excursion Assessments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Excursion Identifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Identifier

### Description
The excursion.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Identifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Shipment Identifier

### Description
The consignment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Shipment Identifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Product Code

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Batch Identifier

### Description
The batch.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Batch Identifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Excursion Assessor Identifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessor Identifier

### Description
Who assessed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessor Identifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Excursion Assessment Timestamp

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessment Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessment Timestamp

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Excursion Stability Reference Identifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Stability Reference Identifier

### Description
The stability study the assessment relies on.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Stability Reference Identifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Excursion Disposition Status

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Disposition Status

### Description
Use, quarantine, reject.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Disposition Status

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Excursion Assessment Notes

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessment Notes

### Description
The reasoning.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::Excursion Assessment Notes

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: temperature_excursion_assessments
- schemaDescription: The assessment of each temperature excursion against the product's stability data, and the disposition of the consignment. It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

### Anchor ID
DigitalProduct::Coco::Temperature Excursion Assessments

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Temperature Excursion Assessments

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Market Authorisations

*Solution component:* `CocoPharma::SolutionComponent::MarketAuthorisationRegister`  
*Category:* Master Data

Which product may be placed on which market, under which authorisation and subject to which conditions, and the label and authorisation changes that safety findings drive.  Batch certification and serialisation routing both read it.

## Create Digital Product

### Display Name
Market Authorisations

### Product Name
Market Authorisations

### Qualified Name
DigitalProduct::Coco::Market Authorisations

### Description
Which product may be placed on which market, under which authorisation and subject to which conditions, and the label and authorisation changes that safety findings drive.  Batch certification and serialisation routing both read it.

### Purpose
Provides the authoritative statement of where each product may be sold and under what conditions.

### Category
Master Data

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Market Authorisations

### Membership Rationale
Produced by the Quality Systems group's `MarketAuthorisationRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Market Authorisations Data Spec

### Qualified Name
DataSpec::Coco::Market Authorisations

### Description
The data structures and fields that make up the Market Authorisations digital product.

### Purpose
Describes the data a subscriber to Market Authorisations receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Market Authorisations

### Collection Id
DataSpec::Coco::Market Authorisations

### Label
data specification

___

## Create Data Structure

### Display Name
Market Authorisation

### Qualified Name
DataStructure::Coco::Market Authorisations::Market Authorisation

### Description
One row per authorisation held.

### Namespace Path
coco_data_hub.market_authorisations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Market Authorisations

### Element Id
DataStructure::Coco::Market Authorisations::Market Authorisation

### Membership Rationale
The Market Authorisation structure is part of the Market Authorisations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Authorisation Identifier

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Identifier

### Description
The authorisation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Identifier

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Product Code

### Description
The product.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Product Code

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Market Code

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Market Code

### Description
The market.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
8

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Market Code

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Authorisation Regulator Code

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Regulator Code

### Description
The granting regulator.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Regulator Code

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Authorisation Start Date

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Start Date

### Description
When granted.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Start Date

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Authorisation End Date

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation End Date

### Description
When it lapses, if it does.

### Data Type
date

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation End Date

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Authorisation Current Status

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Current Status

### Description
Granted, suspended, varied, withdrawn.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Authorisation Current Status

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Signal Identifier

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::Signal Identifier

### Description
The safety signal behind the latest variation, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Market Authorisation::Signal Identifier

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Authorisation Condition

### Qualified Name
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Description
One row per condition or labelling requirement attached to an authorisation.

### Namespace Path
coco_data_hub.market_authorisations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Market Authorisations

### Element Id
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Membership Rationale
The Authorisation Condition structure is part of the Market Authorisations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Authorisation Identifier

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Identifier

### Description
The authorisation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Identifier

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Authorisation Requirement Number

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Number

### Description
The condition's sequence.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Number

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Authorisation Requirement Type

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Type

### Description
Labelling, pack size, distribution, monitoring or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Type

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Authorisation Requirement Description

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Description

### Description
The condition.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Description

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Authorisation Requirement Start Date

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Start Date

### Description
When it took effect.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Market Authorisations::Authorisation Condition::Authorisation Requirement Start Date

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: market_authorisations
- schemaDescription: Which product may be placed on which market, under which authorisation and subject to which conditions, and the label and authorisation changes that safety findings drive. Batch certification and serialisation routing both read it.

### Anchor ID
DigitalProduct::Coco::Market Authorisations

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Market Authorisations

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Occupational Exposure Bands

*Solution component:* `CocoPharma::SolutionComponent::ExposureBandingRegister`  
*Category:* Reference Data

Each substance assigned to an occupational exposure band and each band to a required containment level, revised as incidents reveal what the assessments missed.  It is the rule set that turns a substance identity into a control requirement, and it is shared with transport classification rather than duplicated.

## Create Digital Product

### Display Name
Occupational Exposure Bands

### Product Name
Occupational Exposure Bands

### Qualified Name
DigitalProduct::Coco::Occupational Exposure Bands

### Description
Each substance assigned to an occupational exposure band and each band to a required containment level, revised as incidents reveal what the assessments missed.  It is the rule set that turns a substance identity into a control requirement, and it is shared with transport classification rather than duplicated.

### Purpose
Gives exposure monitoring its limits and transport classification its hazard data from one register.

### Category
Reference Data

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Occupational Exposure Bands

### Membership Rationale
Produced by the Quality Systems group's `ExposureBandingRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Occupational Exposure Bands Data Spec

### Qualified Name
DataSpec::Coco::Occupational Exposure Bands

### Description
The data structures and fields that make up the Occupational Exposure Bands digital product.

### Purpose
Describes the data a subscriber to Occupational Exposure Bands receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Occupational Exposure Bands

### Collection Id
DataSpec::Coco::Occupational Exposure Bands

### Label
data specification

___

## Create Data Structure

### Display Name
Substance Exposure Band

### Qualified Name
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Description
One row per substance, its band.

### Namespace Path
coco_data_hub.occupational_exposure_bands

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Occupational Exposure Bands

### Element Id
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Membership Rationale
The Substance Exposure Band structure is part of the Occupational Exposure Bands data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Code

### Description
The substance.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Code

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Substance Name

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Name

### Description
Its name.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
200

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Name

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Substance Banding Code

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Banding Code

### Description
The band assigned.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Banding Code

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Substance Hazard Code

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Hazard Code

### Description
The hazard classification the assignment rests on.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Hazard Code

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Substance Banding Date

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Banding Date

### Description
When assigned or last revised.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Substance Banding Date

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Incident Identifier

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Incident Identifier

### Description
The incident that prompted the latest revision, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::Incident Identifier

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Band Containment Requirement

### Qualified Name
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Description
One row per band, the limit and containment required.

### Namespace Path
coco_data_hub.occupational_exposure_bands

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Occupational Exposure Bands

### Element Id
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Membership Rationale
The Band Containment Requirement structure is part of the Occupational Exposure Bands data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Band Code

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Code

### Description
The band.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Code

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Band Maximum Value

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Maximum Value

### Description
The exposure limit.

### Data Type
float

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Maximum Value

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Band Unit

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Unit

### Description
The unit of the limit.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Unit

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Band Containment Description

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Containment Description

### Description
The containment required.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::Band Containment Description

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: occupational_exposure_bands
- schemaDescription: Each substance assigned to an occupational exposure band and each band to a required containment level, revised as incidents reveal what the assessments missed. It is the rule set that turns a substance identity into a control requirement, and it is shared with transport classification rather than duplicated.

### Anchor ID
DigitalProduct::Coco::Occupational Exposure Bands

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Occupational Exposure Bands

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Exposure Monitoring Results

*Solution component:* `CocoPharma::SolutionComponent::ExposureMonitoringCapture`  
*Category:* Evidence Record

Personal and static exposure measurements from monitoring campaigns, compared to the banded limits, against the workers and tasks monitored.  An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

## Create Digital Product

### Display Name
Exposure Monitoring Results

### Product Name
Exposure Monitoring Results

### Qualified Name
DigitalProduct::Coco::Exposure Monitoring Results

### Description
Personal and static exposure measurements from monitoring campaigns, compared to the banded limits, against the workers and tasks monitored.  An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

### Purpose
Delivers each worker's measured exposure, and its comparison to the limit, to their health surveillance record.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Exposure Monitoring Results

### Membership Rationale
Produced by the Quality Systems group's `ExposureMonitoringCapture` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Exposure Monitoring Results Data Spec

### Qualified Name
DataSpec::Coco::Exposure Monitoring Results

### Description
The data structures and fields that make up the Exposure Monitoring Results digital product.

### Purpose
Describes the data a subscriber to Exposure Monitoring Results receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Exposure Monitoring Results

### Collection Id
DataSpec::Coco::Exposure Monitoring Results

### Label
data specification

___

## Create Data Structure

### Display Name
Monitoring Campaign

### Qualified Name
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Description
One row per monitoring campaign.

### Namespace Path
coco_data_hub.exposure_monitoring_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Exposure Monitoring Results

### Element Id
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Membership Rationale
The Monitoring Campaign structure is part of the Exposure Monitoring Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Monitoring Campaign Identifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Identifier

### Description
The campaign.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Identifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Site Code

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Site Code

### Description
The site.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Site Code

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Monitoring Campaign Start Date

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Start Date

### Description
When it began.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Start Date

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Monitoring Campaign End Date

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign End Date

### Description
When it ended.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign End Date

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Substance Code

### Description
The substance monitored.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Substance Code

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Monitoring Campaign Description

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Description

### Description
The tasks and locations covered.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::Monitoring Campaign Description

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Exposure Measurement

### Qualified Name
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Description
One row per measurement.

### Namespace Path
coco_data_hub.exposure_monitoring_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Exposure Monitoring Results

### Element Id
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Membership Rationale
The Exposure Measurement structure is part of the Exposure Monitoring Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Exposure Reading Identifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Identifier

### Description
The measurement.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Identifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Monitoring Campaign Identifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Monitoring Campaign Identifier

### Description
The campaign.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Monitoring Campaign Identifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Exposure Reading Type

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Type

### Description
Personal or static.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Type

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Worker Pseudonym Identifier

### Description
The worker, for a personal measurement.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Exposure Reading Location

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Location

### Description
Where, for a static measurement.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Location

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Exposure Reading Timestamp

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Timestamp

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Exposure Reading Value

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Value

### Description
The exposure measured.

### Data Type
float

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Reading Value

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Band Maximum Value

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Band Maximum Value

### Description
The limit compared against.

### Data Type
float

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Band Maximum Value

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Exposure Limit Exceeded Flag

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Limit Exceeded Flag

### Description
Whether the limit was exceeded.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::Exposure Limit Exceeded Flag

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: exposure_monitoring_results
- schemaDescription: Personal and static exposure measurements from monitoring campaigns, compared to the banded limits, against the workers and tasks monitored. An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

### Anchor ID
DigitalProduct::Coco::Exposure Monitoring Results

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Exposure Monitoring Results

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Incidents And Near Misses

*Solution component:* `CocoPharma::SolutionComponent::IncidentAndNearMissReporting`  
*Category:* Transactional Record

Incidents, near misses and their investigations, with the substance or control implicated and the findings fed back into the exposure assessments.  It is what makes the health surveillance chain a loop rather than a line.

## Create Digital Product

### Display Name
Incidents And Near Misses

### Product Name
Incidents And Near Misses

### Qualified Name
DigitalProduct::Coco::Incidents And Near Misses

### Description
Incidents, near misses and their investigations, with the substance or control implicated and the findings fed back into the exposure assessments.  It is what makes the health surveillance chain a loop rather than a line.

### Purpose
Feeds what incidents reveal back into the banding register and into the affected worker's surveillance record.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Element Id
DigitalProduct::Coco::Incidents And Near Misses

### Membership Rationale
Produced by the Quality Systems group's `IncidentAndNearMissReporting` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Incidents And Near Misses Data Spec

### Qualified Name
DataSpec::Coco::Incidents And Near Misses

### Description
The data structures and fields that make up the Incidents And Near Misses digital product.

### Purpose
Describes the data a subscriber to Incidents And Near Misses receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Incidents And Near Misses

### Collection Id
DataSpec::Coco::Incidents And Near Misses

### Label
data specification

___

## Create Data Structure

### Display Name
Incident

### Qualified Name
DataStructure::Coco::Incidents And Near Misses::Incident

### Description
One row per incident or near miss reported.

### Namespace Path
coco_data_hub.incidents_and_near_misses

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Incidents And Near Misses

### Element Id
DataStructure::Coco::Incidents And Near Misses::Incident

### Membership Rationale
The Incident structure is part of the Incidents And Near Misses data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Incident Identifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Identifier

### Description
The incident.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Identifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Incident Type

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Type

### Description
Incident or near miss.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Type

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Incident Timestamp

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Timestamp

### Description
When it occurred.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Timestamp

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Incident Reported Timestamp

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Reported Timestamp

### Description
When reported.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Reported Timestamp

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Site Code

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Site Code

### Description
The site.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Site Code

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Incident Location

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Location

### Description
Where.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Location

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Substance Code

### Description
The substance implicated, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Substance Code

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Worker Pseudonym Identifier

### Description
The worker affected, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Incident Description

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Description

### Description
What happened and the immediate response.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Description

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Incident Severity

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::Incident Severity

### Description
The assessed seriousness.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident::Incident Severity

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Data Structure

### Display Name
Incident Investigation Finding

### Qualified Name
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Description
One row per finding from an incident's investigation.

### Namespace Path
coco_data_hub.incidents_and_near_misses

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Incidents And Near Misses

### Element Id
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Membership Rationale
The Incident Investigation Finding structure is part of the Incidents And Near Misses data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Incident Identifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Identifier

### Description
The incident.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Identifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Incident Finding Number

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Number

### Description
The finding's sequence.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Number

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Incident Finding Description

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Description

### Description
The finding.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Description

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Control Identifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Control Identifier

### Description
The control implicated, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Control Identifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Incident Finding Action Description

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Action Description

### Description
The change to assessments or controls that follows.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::Incident Finding Action Description

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Element

### Element Type Name
TabularDataSetCollection

### Template GUID
3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values
- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
- schemaName: incidents_and_near_misses
- schemaDescription: Incidents, near misses and their investigations, with the substance or control implicated and the findings fed back into the exposure assessments. It is what makes the health surveillance chain a loop rather than a line.

### Anchor ID
DigitalProduct::Coco::Incidents And Near Misses

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Incidents And Near Misses

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
