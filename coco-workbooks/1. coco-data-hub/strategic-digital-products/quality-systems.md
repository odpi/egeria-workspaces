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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

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
coco_pharma.consolidated_safety_reports

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
SafetyReportIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportIdentifier

### Description
The report.

### Data Type
string

### Position
1

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
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 1

___

## Create Data Field

### Display Name
SafetyReportReceivedTimestamp

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportReceivedTimestamp

### Description
When first received anywhere in the company.

### Data Type
date

### Position
2

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
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportReceivedTimestamp

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 2

___

## Create Data Field

### Display Name
SafetyReportSourceType

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportSourceType

### Description
Clinician, complaint, trial site, literature or other.

### Data Type
string

### Position
3

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
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportSourceType

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 3

___

## Create Data Field

### Display Name
SafetyReportSourceIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportSourceIdentifier

### Description
The originating report or complaint.

### Data Type
string

### Position
4

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
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyReportSourceIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 4

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::PatientPseudonymIdentifier

### Description
The patient or participant, by pseudonym.

### Data Type
string

### Position
5

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
DataField::Coco::Consolidated Safety Reports::Safety Report::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 5

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::ProductCode

### Description
The product.

### Data Type
string

### Position
6

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
DataField::Coco::Consolidated Safety Reports::Safety Report::ProductCode

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 6

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::BatchIdentifier

### Description
The batch, if known.

### Data Type
string

### Position
7

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
DataField::Coco::Consolidated Safety Reports::Safety Report::BatchIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 7

___

## Create Data Field

### Display Name
ClinicalTrialIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::ClinicalTrialIdentifier

### Description
The trial, for a site report.

### Data Type
string

### Position
8

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
DataField::Coco::Consolidated Safety Reports::Safety Report::ClinicalTrialIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 8

___

## Create Data Field

### Display Name
AdverseEventDescription

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::AdverseEventDescription

### Description
The reaction as reported.

### Data Type
string

### Position
9

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
DataField::Coco::Consolidated Safety Reports::Safety Report::AdverseEventDescription

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

### Label
field 9

___

## Create Data Field

### Display Name
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyCaseIdentifier

### Description
The case opened from the report.

### Data Type
string

### Position
10

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
DataField::Coco::Consolidated Safety Reports::Safety Report::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Consolidated Safety Reports::Safety Report

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: consolidated_safety_reports
- schemaDescription: Every suspected adverse reaction registered at the single point of intake, whatever door it arrived through: a clinician's report, a complaint with safety content or a trial site's report. The statutory clock starts on first receipt anywhere in the company.

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
coco_pharma.product_complaints

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
ComplaintIdentifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ComplaintIdentifier

### Description
The complaint.

### Data Type
string

### Position
1

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
DataField::Coco::Product Complaints::Complaint::ComplaintIdentifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 1

___

## Create Data Field

### Display Name
ComplaintReceivedTimestamp

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ComplaintReceivedTimestamp

### Description
When received.

### Data Type
date

### Position
2

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
DataField::Coco::Product Complaints::Complaint::ComplaintReceivedTimestamp

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 2

___

## Create Data Field

### Display Name
ComplaintReporterType

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ComplaintReporterType

### Description
Pharmacy, distributor, patient, healthcare professional.

### Data Type
string

### Position
3

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
DataField::Coco::Product Complaints::Complaint::ComplaintReporterType

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 3

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ProductCode

### Description
The product.

### Data Type
string

### Position
4

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
DataField::Coco::Product Complaints::Complaint::ProductCode

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 4

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint::BatchIdentifier

### Description
The batch, if known.

### Data Type
string

### Position
5

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
DataField::Coco::Product Complaints::Complaint::BatchIdentifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 5

___

## Create Data Field

### Display Name
PackSerialNumber

### Qualified Name
DataField::Coco::Product Complaints::Complaint::PackSerialNumber

### Description
The pack, if known.

### Data Type
string

### Position
6

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
DataField::Coco::Product Complaints::Complaint::PackSerialNumber

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 6

___

## Create Data Field

### Display Name
ComplaintDescription

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ComplaintDescription

### Description
The complaint.

### Data Type
string

### Position
7

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
DataField::Coco::Product Complaints::Complaint::ComplaintDescription

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

### Label
field 7

___

## Create Data Field

### Display Name
ComplaintCurrentStatus

### Qualified Name
DataField::Coco::Product Complaints::Complaint::ComplaintCurrentStatus

### Description
Open, under investigation, closed.

### Data Type
string

### Position
8

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
DataField::Coco::Product Complaints::Complaint::ComplaintCurrentStatus

### Data Structure
DataStructure::Coco::Product Complaints::Complaint

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
coco_pharma.product_complaints

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
ComplaintIdentifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintIdentifier

### Description
The complaint.

### Data Type
string

### Position
1

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
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintIdentifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Label
field 1

___

## Create Data Field

### Display Name
ComplaintSafetyFlag

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintSafetyFlag

### Description
Whether it is also a suspected adverse reaction.

### Data Type
boolean

### Position
2

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
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintSafetyFlag

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Label
field 2

___

## Create Data Field

### Display Name
ComplaintAssessorIdentifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintAssessorIdentifier

### Description
Who assessed.

### Data Type
string

### Position
3

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
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintAssessorIdentifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Label
field 3

___

## Create Data Field

### Display Name
ComplaintAssessmentTimestamp

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintAssessmentTimestamp

### Description
When.

### Data Type
date

### Position
4

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
DataField::Coco::Product Complaints::Complaint Safety Assessment::ComplaintAssessmentTimestamp

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

### Label
field 4

___

## Create Data Field

### Display Name
SafetyReportIdentifier

### Qualified Name
DataField::Coco::Product Complaints::Complaint Safety Assessment::SafetyReportIdentifier

### Description
The safety report raised, if any.

### Data Type
string

### Position
5

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
DataField::Coco::Product Complaints::Complaint Safety Assessment::SafetyReportIdentifier

### Data Structure
DataStructure::Coco::Product Complaints::Complaint Safety Assessment

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: product_complaints
- schemaDescription: Complaints about product quality from pharmacies, distributors and patients, and the assessment that separates those which are also potential safety events from those which are not. The separation is deliberately generous.

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
coco_pharma.pharmacovigilance_cases

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
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseIdentifier

### Description
The case.

### Data Type
string

### Position
1

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 1

___

## Create Data Field

### Display Name
SafetyReportIdentifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyReportIdentifier

### Description
The report it was opened from.

### Data Type
string

### Position
2

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyReportIdentifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 2

___

## Create Data Field

### Display Name
SafetyCaseReceivedTimestamp

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseReceivedTimestamp

### Description
The receipt timestamp the clock runs from.

### Data Type
date

### Position
3

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseReceivedTimestamp

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 3

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::ProductCode

### Description
The product.

### Data Type
string

### Position
4

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::ProductCode

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 4

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

### Data Type
string

### Position
5

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 5

___

## Create Data Field

### Display Name
SafetyCaseSeriousnessCode

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseSeriousnessCode

### Description
Serious or non-serious, once assessed.

### Data Type
string

### Position
6

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseSeriousnessCode

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 6

___

## Create Data Field

### Display Name
SafetyCaseExpectednessCode

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseExpectednessCode

### Description
Expected or unexpected, once assessed.

### Data Type
string

### Position
7

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseExpectednessCode

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 7

___

## Create Data Field

### Display Name
SafetyCaseCausalityCode

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseCausalityCode

### Description
The causality assessment.

### Data Type
string

### Position
8

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseCausalityCode

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 8

___

## Create Data Field

### Display Name
SafetyCaseReportingDueDate

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseReportingDueDate

### Description
When the regulatory report is due.

### Data Type
date

### Position
9

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseReportingDueDate

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

### Label
field 9

___

## Create Data Field

### Display Name
SafetyCaseCurrentStatus

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseCurrentStatus

### Description
Open, awaiting assessment, follow-up, submitted, closed.

### Data Type
string

### Position
10

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
DataField::Coco::Pharmacovigilance Cases::Safety Case::SafetyCaseCurrentStatus

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Safety Case

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
coco_pharma.pharmacovigilance_cases

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
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseIdentifier

### Description
The case.

### Data Type
string

### Position
1

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
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Label
field 1

___

## Create Data Field

### Display Name
SafetyCaseNarrativeDescription

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseNarrativeDescription

### Description
The clinical narrative.

### Data Type
string

### Position
2

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
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseNarrativeDescription

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Label
field 2

___

## Create Data Field

### Display Name
PatientBirthDate

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::PatientBirthDate

### Description
The patient's date of birth, where reported.

### Data Type
date

### Position
3

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
DataField::Coco::Pharmacovigilance Cases::Case Narrative::PatientBirthDate

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Label
field 3

___

## Create Data Field

### Display Name
PatientSexCode

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::PatientSexCode

### Description
The patient's sex, where reported.

### Data Type
string

### Position
4

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
DataField::Coco::Pharmacovigilance Cases::Case Narrative::PatientSexCode

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

### Label
field 4

___

## Create Data Field

### Display Name
SafetyCaseConcomitantDescription

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseConcomitantDescription

### Description
Other treatments in use.

### Data Type
string

### Position
5

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
DataField::Coco::Pharmacovigilance Cases::Case Narrative::SafetyCaseConcomitantDescription

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Narrative

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
coco_pharma.pharmacovigilance_cases

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
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseIdentifier

### Description
The case.

### Data Type
string

### Position
1

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
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Label
field 1

___

## Create Data Field

### Display Name
SafetyCaseFollowUpNumber

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpNumber

### Description
The follow-up's sequence.

### Data Type
int

### Position
2

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
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpNumber

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Label
field 2

___

## Create Data Field

### Display Name
SafetyCaseFollowUpDate

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpDate

### Description
When.

### Data Type
date

### Position
3

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
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpDate

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

### Label
field 3

___

## Create Data Field

### Display Name
SafetyCaseFollowUpDescription

### Qualified Name
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpDescription

### Description
What was requested or received.

### Data Type
string

### Position
4

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
DataField::Coco::Pharmacovigilance Cases::Case Follow-Up::SafetyCaseFollowUpDescription

### Data Structure
DataStructure::Coco::Pharmacovigilance Cases::Case Follow-Up

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: pharmacovigilance_cases
- schemaDescription: The safety case from receipt through follow-up to closure, carrying the reporting clock that the regulators measure, with the narrative sent for assessment and the coded data that signal detection reads. Every other component in the safety chain either feeds it or reads from it.

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
coco_pharma.medical_assessments

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
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseIdentifier

### Description
The case.

### Data Type
string

### Position
1

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 1

___

## Create Data Field

### Display Name
SafetyCaseAssessorIdentifier

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessorIdentifier

### Description
The assessing physician.

### Data Type
string

### Position
2

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessorIdentifier

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 2

___

## Create Data Field

### Display Name
SafetyCaseAssessmentTimestamp

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessmentTimestamp

### Description
When.

### Data Type
date

### Position
3

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessmentTimestamp

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 3

___

## Create Data Field

### Display Name
SafetyCaseSeriousnessCode

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseSeriousnessCode

### Description
Serious or non-serious.

### Data Type
string

### Position
4

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseSeriousnessCode

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 4

___

## Create Data Field

### Display Name
SafetyCaseExpectednessCode

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseExpectednessCode

### Description
Expected or unexpected against the label.

### Data Type
string

### Position
5

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseExpectednessCode

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 5

___

## Create Data Field

### Display Name
SafetyCaseCausalityCode

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseCausalityCode

### Description
The causality assessment.

### Data Type
string

### Position
6

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseCausalityCode

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

### Label
field 6

___

## Create Data Field

### Display Name
SafetyCaseAssessmentNotes

### Qualified Name
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessmentNotes

### Description
The assessor's reasoning.

### Data Type
string

### Position
7

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
DataField::Coco::Medical Assessments::Medical Assessment::SafetyCaseAssessmentNotes

### Data Structure
DataStructure::Coco::Medical Assessments::Medical Assessment

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
coco_pharma.medical_assessments

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
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::SafetyCaseIdentifier

### Description
The case.

### Data Type
string

### Position
1

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
DataField::Coco::Medical Assessments::Coded Term::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Label
field 1

___

## Create Data Field

### Display Name
AdverseEventCode

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::AdverseEventCode

### Description
The dictionary code.

### Data Type
string

### Position
2

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
DataField::Coco::Medical Assessments::Coded Term::AdverseEventCode

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Label
field 2

___

## Create Data Field

### Display Name
AdverseEventDictionaryVersion

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::AdverseEventDictionaryVersion

### Description
The dictionary version.

### Data Type
string

### Position
3

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
DataField::Coco::Medical Assessments::Coded Term::AdverseEventDictionaryVersion

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Label
field 3

___

## Create Data Field

### Display Name
AdverseEventTermName

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::AdverseEventTermName

### Description
The term.

### Data Type
string

### Position
4

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
DataField::Coco::Medical Assessments::Coded Term::AdverseEventTermName

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

### Label
field 4

___

## Create Data Field

### Display Name
AdverseEventPrimaryFlag

### Qualified Name
DataField::Coco::Medical Assessments::Coded Term::AdverseEventPrimaryFlag

### Description
Whether this is the primary event.

### Data Type
boolean

### Position
5

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
DataField::Coco::Medical Assessments::Coded Term::AdverseEventPrimaryFlag

### Data Structure
DataStructure::Coco::Medical Assessments::Coded Term

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: medical_assessments
- schemaDescription: The qualified medical judgement of seriousness, expectedness and causality for each case, and the coding of the event to the standard dictionary. It is the step that decides whether a report is expedited or periodic.

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
coco_pharma.safety_signals

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
SignalIdentifier

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalIdentifier

### Description
The signal.

### Data Type
string

### Position
1

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
DataField::Coco::Safety Signals::Safety Signal::SignalIdentifier

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 1

___

## Create Data Field

### Display Name
SignalDetectedDate

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalDetectedDate

### Description
When detected.

### Data Type
date

### Position
2

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
DataField::Coco::Safety Signals::Safety Signal::SignalDetectedDate

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 2

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::ProductCode

### Description
The product.

### Data Type
string

### Position
3

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
DataField::Coco::Safety Signals::Safety Signal::ProductCode

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 3

___

## Create Data Field

### Display Name
AdverseEventCode

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::AdverseEventCode

### Description
The event term.

### Data Type
string

### Position
4

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
DataField::Coco::Safety Signals::Safety Signal::AdverseEventCode

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 4

___

## Create Data Field

### Display Name
SignalContributingCount

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalContributingCount

### Description
The number of cases contributing.

### Data Type
int

### Position
5

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
DataField::Coco::Safety Signals::Safety Signal::SignalContributingCount

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 5

___

## Create Data Field

### Display Name
SignalDescription

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalDescription

### Description
The pattern observed.

### Data Type
string

### Position
6

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
DataField::Coco::Safety Signals::Safety Signal::SignalDescription

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 6

___

## Create Data Field

### Display Name
SignalCurrentStatus

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalCurrentStatus

### Description
Detected, under evaluation, confirmed, refuted.

### Data Type
string

### Position
7

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
DataField::Coco::Safety Signals::Safety Signal::SignalCurrentStatus

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

### Label
field 7

___

## Create Data Field

### Display Name
SignalReferralType

### Qualified Name
DataField::Coco::Safety Signals::Safety Signal::SignalReferralType

### Description
Referred to quality, to authorisation, both or neither.

### Data Type
string

### Position
8

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
DataField::Coco::Safety Signals::Safety Signal::SignalReferralType

### Data Structure
DataStructure::Coco::Safety Signals::Safety Signal

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
coco_pharma.safety_signals

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
ProductCode

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::ProductCode

### Description
The product.

### Data Type
string

### Position
1

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
DataField::Coco::Safety Signals::Exposure Denominator::ProductCode

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Label
field 1

___

## Create Data Field

### Display Name
ExposurePeriodCode

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::ExposurePeriodCode

### Description
The period.

### Data Type
string

### Position
2

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
DataField::Coco::Safety Signals::Exposure Denominator::ExposurePeriodCode

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Label
field 2

___

## Create Data Field

### Display Name
ExposureCount

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::ExposureCount

### Description
The estimated number of patients exposed.

### Data Type
int

### Position
3

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
DataField::Coco::Safety Signals::Exposure Denominator::ExposureCount

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

### Label
field 3

___

## Create Data Field

### Display Name
ExposureSourceDescription

### Qualified Name
DataField::Coco::Safety Signals::Exposure Denominator::ExposureSourceDescription

### Description
How the estimate was derived.

### Data Type
string

### Position
4

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
DataField::Coco::Safety Signals::Exposure Denominator::ExposureSourceDescription

### Data Structure
DataStructure::Coco::Safety Signals::Exposure Denominator

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: safety_signals
- schemaDescription: The patterns found across accumulated cases that no single case shows, with the exposure denominators they were assessed against, and the referrals made to quality and to the authorisation register. A signal visible across trial and post-market data is invisible in either alone.

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
coco_pharma.regulatory_safety_submissions

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
SubmissionIdentifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionIdentifier

### Description
The submission.

### Data Type
string

### Position
1

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionIdentifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 1

___

## Create Data Field

### Display Name
SafetyCaseIdentifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SafetyCaseIdentifier

### Description
The case, for an expedited report.

### Data Type
string

### Position
2

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SafetyCaseIdentifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 2

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::ProductCode

### Description
The product.

### Data Type
string

### Position
3

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::ProductCode

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 3

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::MarketCode

### Description
The market.

### Data Type
string

### Position
4

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::MarketCode

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 4

___

## Create Data Field

### Display Name
SubmissionRegulatorCode

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionRegulatorCode

### Description
The regulator.

### Data Type
string

### Position
5

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionRegulatorCode

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 5

___

## Create Data Field

### Display Name
SubmissionType

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionType

### Description
Expedited or periodic.

### Data Type
string

### Position
6

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionType

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 6

___

## Create Data Field

### Display Name
SubmissionDueDate

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionDueDate

### Description
When due.

### Data Type
date

### Position
7

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionDueDate

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 7

___

## Create Data Field

### Display Name
SubmissionTimestamp

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionTimestamp

### Description
When transmitted.

### Data Type
date

### Position
8

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionTimestamp

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

### Label
field 8

___

## Create Data Field

### Display Name
SubmissionFormatCode

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionFormatCode

### Description
The format used.

### Data Type
string

### Position
9

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
DataField::Coco::Regulatory Safety Submissions::Safety Submission::SubmissionFormatCode

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Safety Submission

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
coco_pharma.regulatory_safety_submissions

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
SubmissionIdentifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionIdentifier

### Description
The submission.

### Data Type
string

### Position
1

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
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionIdentifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Label
field 1

___

## Create Data Field

### Display Name
SubmissionAcknowledgedTimestamp

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgedTimestamp

### Description
When acknowledged.

### Data Type
date

### Position
2

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
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgedTimestamp

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Label
field 2

___

## Create Data Field

### Display Name
SubmissionAcknowledgementIdentifier

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgementIdentifier

### Description
The regulator's reference.

### Data Type
string

### Position
3

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
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgementIdentifier

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

### Label
field 3

___

## Create Data Field

### Display Name
SubmissionAcknowledgementStatus

### Qualified Name
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgementStatus

### Description
Accepted, rejected or queried.

### Data Type
string

### Position
4

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
DataField::Coco::Regulatory Safety Submissions::Submission Acknowledgement::SubmissionAcknowledgementStatus

### Data Structure
DataStructure::Coco::Regulatory Safety Submissions::Submission Acknowledgement

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: regulatory_safety_submissions
- schemaDescription: The expedited and periodic safety reports formatted and transmitted to the regulator of each market the product is authorised in, and the acknowledgement each received. An unacknowledged submission is not a submission.

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
coco_pharma.laboratory_test_results

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
SampleIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::SampleIdentifier

### Description
The sample.

### Data Type
string

### Position
1

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
DataField::Coco::Laboratory Test Results::Sample::SampleIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Label
field 1

___

## Create Data Field

### Display Name
SampleType

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::SampleType

### Description
Raw material, in-process or finished product.

### Data Type
string

### Position
2

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
DataField::Coco::Laboratory Test Results::Sample::SampleType

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Label
field 2

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::LotIdentifier

### Description
The material lot, for raw material.

### Data Type
string

### Position
3

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
DataField::Coco::Laboratory Test Results::Sample::LotIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Label
field 3

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::BatchIdentifier

### Description
The batch, for in-process and finished product.

### Data Type
string

### Position
4

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
DataField::Coco::Laboratory Test Results::Sample::BatchIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Label
field 4

___

## Create Data Field

### Display Name
SampleCollectionTimestamp

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::SampleCollectionTimestamp

### Description
When taken.

### Data Type
date

### Position
5

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
DataField::Coco::Laboratory Test Results::Sample::SampleCollectionTimestamp

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

### Label
field 5

___

## Create Data Field

### Display Name
SampleCurrentStatus

### Qualified Name
DataField::Coco::Laboratory Test Results::Sample::SampleCurrentStatus

### Description
Received, in test, complete.

### Data Type
string

### Position
6

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
DataField::Coco::Laboratory Test Results::Sample::SampleCurrentStatus

### Data Structure
DataStructure::Coco::Laboratory Test Results::Sample

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
coco_pharma.laboratory_test_results

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
TestResultIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestResultIdentifier

### Description
The result.

### Data Type
string

### Position
1

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
DataField::Coco::Laboratory Test Results::Test Result::TestResultIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 1

___

## Create Data Field

### Display Name
SampleIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::SampleIdentifier

### Description
The sample.

### Data Type
string

### Position
2

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
DataField::Coco::Laboratory Test Results::Test Result::SampleIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 2

___

## Create Data Field

### Display Name
TestCode

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestCode

### Description
The test.

### Data Type
string

### Position
3

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
DataField::Coco::Laboratory Test Results::Test Result::TestCode

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 3

___

## Create Data Field

### Display Name
TestValue

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestValue

### Description
The result.

### Data Type
string

### Position
4

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
DataField::Coco::Laboratory Test Results::Test Result::TestValue

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 4

___

## Create Data Field

### Display Name
TestUnit

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestUnit

### Description
The unit.

### Data Type
string

### Position
5

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
DataField::Coco::Laboratory Test Results::Test Result::TestUnit

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 5

___

## Create Data Field

### Display Name
SpecificationMinimumValue

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::SpecificationMinimumValue

### Description
The lower limit.

### Data Type
string

### Position
6

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
DataField::Coco::Laboratory Test Results::Test Result::SpecificationMinimumValue

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 6

___

## Create Data Field

### Display Name
SpecificationMaximumValue

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::SpecificationMaximumValue

### Description
The upper limit.

### Data Type
string

### Position
7

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
DataField::Coco::Laboratory Test Results::Test Result::SpecificationMaximumValue

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 7

___

## Create Data Field

### Display Name
TestConformityFlag

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestConformityFlag

### Description
Whether the result is within specification.

### Data Type
boolean

### Position
8

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
DataField::Coco::Laboratory Test Results::Test Result::TestConformityFlag

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 8

___

## Create Data Field

### Display Name
TestCompletedTimestamp

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestCompletedTimestamp

### Description
When completed.

### Data Type
date

### Position
9

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
DataField::Coco::Laboratory Test Results::Test Result::TestCompletedTimestamp

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

### Label
field 9

___

## Create Data Field

### Display Name
TestAnalystIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Test Result::TestAnalystIdentifier

### Description
The analyst.

### Data Type
string

### Position
10

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
DataField::Coco::Laboratory Test Results::Test Result::TestAnalystIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Test Result

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
coco_pharma.laboratory_test_results

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
CertificateIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateIdentifier

### Description
The certificate.

### Data Type
string

### Position
1

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Label
field 1

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::BatchIdentifier

### Description
The batch, for finished product.

### Data Type
string

### Position
2

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::BatchIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Label
field 2

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::LotIdentifier

### Description
The lot, for material.

### Data Type
string

### Position
3

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::LotIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Label
field 3

___

## Create Data Field

### Display Name
CertificateDate

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateDate

### Description
When issued.

### Data Type
date

### Position
4

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateDate

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Label
field 4

___

## Create Data Field

### Display Name
CertificateConformityFlag

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateConformityFlag

### Description
Whether every test conformed.

### Data Type
boolean

### Position
5

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateConformityFlag

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

### Label
field 5

___

## Create Data Field

### Display Name
CertificateApproverIdentifier

### Qualified Name
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateApproverIdentifier

### Description
Who approved the certificate.

### Data Type
string

### Position
6

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
DataField::Coco::Laboratory Test Results::Certificate Of Analysis::CertificateApproverIdentifier

### Data Structure
DataStructure::Coco::Laboratory Test Results::Certificate Of Analysis

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: laboratory_test_results
- schemaDescription: Sampling, testing and results for raw materials, in-process checks and finished product, compared against specification, and the certificates of analysis issued for release. Results are gates rather than reports: material cannot be issued and product cannot be released until the laboratory has answered.

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
coco_pharma.deviations_and_capas

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
DeviationIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationIdentifier

### Description
The deviation.

### Data Type
string

### Position
1

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 1

___

## Create Data Field

### Display Name
DeviationRaisedTimestamp

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationRaisedTimestamp

### Description
When raised.

### Data Type
date

### Position
2

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationRaisedTimestamp

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 2

___

## Create Data Field

### Display Name
DeviationSourceType

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationSourceType

### Description
Manufacturing execution, safety signal, audit or other.

### Data Type
string

### Position
3

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationSourceType

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 3

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::BatchIdentifier

### Description
The batch affected, if any.

### Data Type
string

### Position
4

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
DataField::Coco::Deviations And CAPAs::Deviation::BatchIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 4

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::ProductCode

### Description
The product affected.

### Data Type
string

### Position
5

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
DataField::Coco::Deviations And CAPAs::Deviation::ProductCode

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 5

___

## Create Data Field

### Display Name
SignalIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::SignalIdentifier

### Description
The safety signal referred, if any.

### Data Type
string

### Position
6

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
DataField::Coco::Deviations And CAPAs::Deviation::SignalIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 6

___

## Create Data Field

### Display Name
DeviationDescription

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationDescription

### Description
The departure and its context.

### Data Type
string

### Position
7

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationDescription

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 7

___

## Create Data Field

### Display Name
DeviationSeverity

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationSeverity

### Description
Minor, major or critical.

### Data Type
string

### Position
8

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationSeverity

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

### Label
field 8

___

## Create Data Field

### Display Name
DeviationCurrentStatus

### Qualified Name
DataField::Coco::Deviations And CAPAs::Deviation::DeviationCurrentStatus

### Description
Open, under investigation, dispositioned, closed.

### Data Type
string

### Position
9

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
DataField::Coco::Deviations And CAPAs::Deviation::DeviationCurrentStatus

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Deviation

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
coco_pharma.deviations_and_capas

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
DeviationIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationIdentifier

### Description
The deviation.

### Data Type
string

### Position
1

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Label
field 1

___

## Create Data Field

### Display Name
DeviationInvestigatorIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationInvestigatorIdentifier

### Description
Who investigated.

### Data Type
string

### Position
2

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationInvestigatorIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Label
field 2

___

## Create Data Field

### Display Name
DeviationInvestigationCompletedDate

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationInvestigationCompletedDate

### Description
When.

### Data Type
date

### Position
3

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationInvestigationCompletedDate

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Label
field 3

___

## Create Data Field

### Display Name
DeviationRootCauseDescription

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationRootCauseDescription

### Description
The root cause found.

### Data Type
string

### Position
4

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationRootCauseDescription

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Label
field 4

___

## Create Data Field

### Display Name
DeviationImpactDescription

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationImpactDescription

### Description
The impact on the batch.

### Data Type
string

### Position
5

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationImpactDescription

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

### Label
field 5

___

## Create Data Field

### Display Name
DeviationDispositionStatus

### Qualified Name
DataField::Coco::Deviations And CAPAs::Investigation::DeviationDispositionStatus

### Description
No impact, rework, reject, or release with justification.

### Data Type
string

### Position
6

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
DataField::Coco::Deviations And CAPAs::Investigation::DeviationDispositionStatus

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Investigation

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
coco_pharma.deviations_and_capas

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
CorrectiveActionIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionIdentifier

### Description
The action.

### Data Type
string

### Position
1

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 1

___

## Create Data Field

### Display Name
DeviationIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::DeviationIdentifier

### Description
The deviation it addresses.

### Data Type
string

### Position
2

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
DataField::Coco::Deviations And CAPAs::Corrective Action::DeviationIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 2

___

## Create Data Field

### Display Name
CorrectiveActionType

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionType

### Description
Corrective or preventive.

### Data Type
string

### Position
3

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionType

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 3

___

## Create Data Field

### Display Name
CorrectiveActionDescription

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionDescription

### Description
The action.

### Data Type
string

### Position
4

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionDescription

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 4

___

## Create Data Field

### Display Name
CorrectiveActionOwnerIdentifier

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionOwnerIdentifier

### Description
Who owns it.

### Data Type
string

### Position
5

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionOwnerIdentifier

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 5

___

## Create Data Field

### Display Name
CorrectiveActionDueDate

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionDueDate

### Description
When due.

### Data Type
date

### Position
6

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionDueDate

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

### Label
field 6

___

## Create Data Field

### Display Name
CorrectiveActionCurrentStatus

### Qualified Name
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionCurrentStatus

### Description
Open, complete, verified.

### Data Type
string

### Position
7

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
DataField::Coco::Deviations And CAPAs::Corrective Action::CorrectiveActionCurrentStatus

### Data Structure
DataStructure::Coco::Deviations And CAPAs::Corrective Action

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: deviations_and_capas
- schemaDescription: Departures from the approved process, their investigation and the corrective and preventive actions that follow, including the signals referred from safety. An open deviation is a gate on certification, so this sits inside the release flow rather than beside it.

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
coco_pharma.batch_certification_decisions

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
BatchIdentifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchIdentifier

### Description
The batch.

### Data Type
string

### Position
1

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchIdentifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 1

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::MarketCode

### Description
The market.

### Data Type
string

### Position
2

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
DataField::Coco::Batch Certification Decisions::Certification Decision::MarketCode

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 2

___

## Create Data Field

### Display Name
BatchCertifierIdentifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertifierIdentifier

### Description
The Qualified Person.

### Data Type
string

### Position
3

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertifierIdentifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 3

___

## Create Data Field

### Display Name
BatchCertificationDate

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationDate

### Description
When decided.

### Data Type
date

### Position
4

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationDate

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 4

___

## Create Data Field

### Display Name
BatchCertificationStatus

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationStatus

### Description
Certified, rejected or held.

### Data Type
string

### Position
5

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationStatus

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 5

___

## Create Data Field

### Display Name
BatchReleasedQuantity

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchReleasedQuantity

### Description
The quantity released to the market.

### Data Type
int

### Position
6

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchReleasedQuantity

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 6

___

## Create Data Field

### Display Name
BatchRecordCompleteFlag

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchRecordCompleteFlag

### Description
Whether the record reviewed was complete.

### Data Type
boolean

### Position
7

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchRecordCompleteFlag

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 7

___

## Create Data Field

### Display Name
DeviationIdentifier

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::DeviationIdentifier

### Description
An open deviation that held the batch, if any.

### Data Type
string

### Position
8

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
DataField::Coco::Batch Certification Decisions::Certification Decision::DeviationIdentifier

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 8

___

## Create Data Field

### Display Name
BatchCertificationNotes

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationNotes

### Description
The reviewer's findings.

### Data Type
string

### Position
9

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
DataField::Coco::Batch Certification Decisions::Certification Decision::BatchCertificationNotes

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

### Label
field 9

___

## Create Data Field

### Display Name
ShipmentStorageDescription

### Qualified Name
DataField::Coco::Batch Certification Decisions::Certification Decision::ShipmentStorageDescription

### Description
The storage conditions the released therapy must be shipped under.

### Data Type
string

### Position
10

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
DataField::Coco::Batch Certification Decisions::Certification Decision::ShipmentStorageDescription

### Data Structure
DataStructure::Coco::Batch Certification Decisions::Certification Decision

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: batch_certification_decisions
- schemaDescription: The review of each assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market. It is the single human decision the whole chain exists to support, and it is market-specific.

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
coco_pharma.serialisation_alert_investigations

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
AlertIdentifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertIdentifier

### Description
The alert.

### Data Type
string

### Position
1

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertIdentifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 1

___

## Create Data Field

### Display Name
PackSerialNumber

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::PackSerialNumber

### Description
The identifier.

### Data Type
string

### Position
2

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::PackSerialNumber

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 2

___

## Create Data Field

### Display Name
AlertInvestigatorIdentifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigatorIdentifier

### Description
Who investigated.

### Data Type
string

### Position
3

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigatorIdentifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 3

___

## Create Data Field

### Display Name
AlertInvestigationStartTimestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationStartTimestamp

### Description
When opened.

### Data Type
date

### Position
4

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationStartTimestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 4

___

## Create Data Field

### Display Name
AlertInvestigationEndTimestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationEndTimestamp

### Description
When closed.

### Data Type
date

### Position
5

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationEndTimestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 5

___

## Create Data Field

### Display Name
AlertRootCauseType

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertRootCauseType

### Description
Data error, scanning error, expired product, suspected falsification, other.

### Data Type
string

### Position
6

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertRootCauseType

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 6

___

## Create Data Field

### Display Name
AlertInvestigationNotes

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationNotes

### Description
What was found.

### Data Type
string

### Position
7

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertInvestigationNotes

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

### Label
field 7

___

## Create Data Field

### Display Name
AlertCurrentStatus

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertCurrentStatus

### Description
Open, closed, escalated.

### Data Type
string

### Position
8

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
DataField::Coco::Serialisation Alert Investigations::Alert Investigation::AlertCurrentStatus

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Investigation

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
coco_pharma.serialisation_alert_investigations

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
AlertIdentifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertIdentifier

### Description
The alert.

### Data Type
string

### Position
1

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
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertIdentifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Label
field 1

___

## Create Data Field

### Display Name
AlertDispositionType

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertDispositionType

### Description
Correct repository, decommission, recall, report to authority, no action.

### Data Type
string

### Position
2

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
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertDispositionType

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Label
field 2

___

## Create Data Field

### Display Name
AlertDispositionTimestamp

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertDispositionTimestamp

### Description
When.

### Data Type
date

### Position
3

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
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertDispositionTimestamp

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Label
field 3

___

## Create Data Field

### Display Name
AlertAffectedCount

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertAffectedCount

### Description
The number of identifiers affected.

### Data Type
int

### Position
4

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
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::AlertAffectedCount

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

### Label
field 4

___

## Create Data Field

### Display Name
CorrectiveActionIdentifier

### Qualified Name
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::CorrectiveActionIdentifier

### Description
The CAPA raised, if any.

### Data Type
string

### Position
5

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
DataField::Coco::Serialisation Alert Investigations::Alert Disposition::CorrectiveActionIdentifier

### Data Structure
DataStructure::Coco::Serialisation Alert Investigations::Alert Disposition

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: serialisation_alert_investigations
- schemaDescription: The investigation of verification alerts raised by pharmacies and trading partners, separating the company's own data errors from genuine falsification signals, and the disposition returned to the serialisation repository. An alert not investigated is a falsification signal received and ignored.

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
coco_pharma.temperature_excursion_assessments

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
ExcursionIdentifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionIdentifier

### Description
The excursion.

### Data Type
string

### Position
1

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionIdentifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 1

___

## Create Data Field

### Display Name
ShipmentIdentifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ShipmentIdentifier

### Description
The consignment.

### Data Type
string

### Position
2

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 2

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ProductCode

### Description
The product.

### Data Type
string

### Position
3

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ProductCode

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 3

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::BatchIdentifier

### Description
The batch.

### Data Type
string

### Position
4

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::BatchIdentifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 4

___

## Create Data Field

### Display Name
ExcursionAssessorIdentifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessorIdentifier

### Description
Who assessed.

### Data Type
string

### Position
5

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessorIdentifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 5

___

## Create Data Field

### Display Name
ExcursionAssessmentTimestamp

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessmentTimestamp

### Description
When.

### Data Type
date

### Position
6

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessmentTimestamp

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 6

___

## Create Data Field

### Display Name
ExcursionStabilityReferenceIdentifier

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionStabilityReferenceIdentifier

### Description
The stability study the assessment relies on.

### Data Type
string

### Position
7

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionStabilityReferenceIdentifier

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 7

___

## Create Data Field

### Display Name
ExcursionDispositionStatus

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionDispositionStatus

### Description
Use, quarantine, reject.

### Data Type
string

### Position
8

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionDispositionStatus

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

### Label
field 8

___

## Create Data Field

### Display Name
ExcursionAssessmentNotes

### Qualified Name
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessmentNotes

### Description
The reasoning.

### Data Type
string

### Position
9

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
DataField::Coco::Temperature Excursion Assessments::Excursion Assessment::ExcursionAssessmentNotes

### Data Structure
DataStructure::Coco::Temperature Excursion Assessments::Excursion Assessment

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: temperature_excursion_assessments
- schemaDescription: The assessment of each temperature excursion against the product's stability data, and the disposition of the consignment. It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.

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
coco_pharma.market_authorisations

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
AuthorisationIdentifier

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationIdentifier

### Description
The authorisation.

### Data Type
string

### Position
1

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
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationIdentifier

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::ProductCode

### Description
The product.

### Data Type
string

### Position
2

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
DataField::Coco::Market Authorisations::Market Authorisation::ProductCode

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 2

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::MarketCode

### Description
The market.

### Data Type
string

### Position
3

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
DataField::Coco::Market Authorisations::Market Authorisation::MarketCode

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 3

___

## Create Data Field

### Display Name
AuthorisationRegulatorCode

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationRegulatorCode

### Description
The granting regulator.

### Data Type
string

### Position
4

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
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationRegulatorCode

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 4

___

## Create Data Field

### Display Name
AuthorisationStartDate

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationStartDate

### Description
When granted.

### Data Type
date

### Position
5

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
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationStartDate

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 5

___

## Create Data Field

### Display Name
AuthorisationEndDate

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationEndDate

### Description
When it lapses, if it does.

### Data Type
date

### Position
6

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
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationEndDate

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 6

___

## Create Data Field

### Display Name
AuthorisationCurrentStatus

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationCurrentStatus

### Description
Granted, suspended, varied, withdrawn.

### Data Type
string

### Position
7

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
DataField::Coco::Market Authorisations::Market Authorisation::AuthorisationCurrentStatus

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

### Label
field 7

___

## Create Data Field

### Display Name
SignalIdentifier

### Qualified Name
DataField::Coco::Market Authorisations::Market Authorisation::SignalIdentifier

### Description
The safety signal behind the latest variation, if any.

### Data Type
string

### Position
8

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
DataField::Coco::Market Authorisations::Market Authorisation::SignalIdentifier

### Data Structure
DataStructure::Coco::Market Authorisations::Market Authorisation

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
coco_pharma.market_authorisations

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
AuthorisationIdentifier

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationIdentifier

### Description
The authorisation.

### Data Type
string

### Position
1

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
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationIdentifier

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Label
field 1

___

## Create Data Field

### Display Name
AuthorisationRequirementNumber

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementNumber

### Description
The condition's sequence.

### Data Type
int

### Position
2

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
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementNumber

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Label
field 2

___

## Create Data Field

### Display Name
AuthorisationRequirementType

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementType

### Description
Labelling, pack size, distribution, monitoring or other.

### Data Type
string

### Position
3

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
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementType

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Label
field 3

___

## Create Data Field

### Display Name
AuthorisationRequirementDescription

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementDescription

### Description
The condition.

### Data Type
string

### Position
4

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
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementDescription

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

### Label
field 4

___

## Create Data Field

### Display Name
AuthorisationRequirementStartDate

### Qualified Name
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementStartDate

### Description
When it took effect.

### Data Type
date

### Position
5

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
DataField::Coco::Market Authorisations::Authorisation Condition::AuthorisationRequirementStartDate

### Data Structure
DataStructure::Coco::Market Authorisations::Authorisation Condition

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: market_authorisations
- schemaDescription: Which product may be placed on which market, under which authorisation and subject to which conditions, and the label and authorisation changes that safety findings drive. Batch certification and serialisation routing both read it.

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
coco_pharma.occupational_exposure_bands

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
SubstanceCode

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceCode

### Description
The substance.

### Data Type
string

### Position
1

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceCode

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Label
field 1

___

## Create Data Field

### Display Name
SubstanceName

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceName

### Description
Its name.

### Data Type
string

### Position
2

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceName

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Label
field 2

___

## Create Data Field

### Display Name
SubstanceBandingCode

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceBandingCode

### Description
The band assigned.

### Data Type
string

### Position
3

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceBandingCode

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Label
field 3

___

## Create Data Field

### Display Name
SubstanceHazardCode

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceHazardCode

### Description
The hazard classification the assignment rests on.

### Data Type
string

### Position
4

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceHazardCode

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Label
field 4

___

## Create Data Field

### Display Name
SubstanceBandingDate

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceBandingDate

### Description
When assigned or last revised.

### Data Type
date

### Position
5

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::SubstanceBandingDate

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

### Label
field 5

___

## Create Data Field

### Display Name
IncidentIdentifier

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::IncidentIdentifier

### Description
The incident that prompted the latest revision, if any.

### Data Type
string

### Position
6

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
DataField::Coco::Occupational Exposure Bands::Substance Exposure Band::IncidentIdentifier

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Substance Exposure Band

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
coco_pharma.occupational_exposure_bands

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
BandCode

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandCode

### Description
The band.

### Data Type
string

### Position
1

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
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandCode

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Label
field 1

___

## Create Data Field

### Display Name
BandMaximumValue

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandMaximumValue

### Description
The exposure limit.

### Data Type
float

### Position
2

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
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandMaximumValue

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Label
field 2

___

## Create Data Field

### Display Name
BandUnit

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandUnit

### Description
The unit of the limit.

### Data Type
string

### Position
3

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
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandUnit

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

### Label
field 3

___

## Create Data Field

### Display Name
BandContainmentDescription

### Qualified Name
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandContainmentDescription

### Description
The containment required.

### Data Type
string

### Position
4

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
DataField::Coco::Occupational Exposure Bands::Band Containment Requirement::BandContainmentDescription

### Data Structure
DataStructure::Coco::Occupational Exposure Bands::Band Containment Requirement

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: occupational_exposure_bands
- schemaDescription: Each substance assigned to an occupational exposure band and each band to a required containment level, revised as incidents reveal what the assessments missed. It is the rule set that turns a substance identity into a control requirement, and it is shared with transport classification rather than duplicated.

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
coco_pharma.exposure_monitoring_results

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
MonitoringCampaignIdentifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignIdentifier

### Description
The campaign.

### Data Type
string

### Position
1

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignIdentifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Label
field 1

___

## Create Data Field

### Display Name
SiteCode

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::SiteCode

### Description
The site.

### Data Type
string

### Position
2

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::SiteCode

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Label
field 2

___

## Create Data Field

### Display Name
MonitoringCampaignStartDate

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignStartDate

### Description
When it began.

### Data Type
date

### Position
3

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignStartDate

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Label
field 3

___

## Create Data Field

### Display Name
MonitoringCampaignEndDate

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignEndDate

### Description
When it ended.

### Data Type
date

### Position
4

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignEndDate

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Label
field 4

___

## Create Data Field

### Display Name
SubstanceCode

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::SubstanceCode

### Description
The substance monitored.

### Data Type
string

### Position
5

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::SubstanceCode

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

### Label
field 5

___

## Create Data Field

### Display Name
MonitoringCampaignDescription

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignDescription

### Description
The tasks and locations covered.

### Data Type
string

### Position
6

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
DataField::Coco::Exposure Monitoring Results::Monitoring Campaign::MonitoringCampaignDescription

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Monitoring Campaign

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
coco_pharma.exposure_monitoring_results

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
ExposureReadingIdentifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingIdentifier

### Description
The measurement.

### Data Type
string

### Position
1

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingIdentifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 1

___

## Create Data Field

### Display Name
MonitoringCampaignIdentifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::MonitoringCampaignIdentifier

### Description
The campaign.

### Data Type
string

### Position
2

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::MonitoringCampaignIdentifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 2

___

## Create Data Field

### Display Name
ExposureReadingType

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingType

### Description
Personal or static.

### Data Type
string

### Position
3

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingType

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 3

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::WorkerPseudonymIdentifier

### Description
The worker, for a personal measurement.

### Data Type
string

### Position
4

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 4

___

## Create Data Field

### Display Name
ExposureReadingLocation

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingLocation

### Description
Where, for a static measurement.

### Data Type
string

### Position
5

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingLocation

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 5

___

## Create Data Field

### Display Name
ExposureReadingTimestamp

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingTimestamp

### Description
When.

### Data Type
date

### Position
6

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingTimestamp

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 6

___

## Create Data Field

### Display Name
ExposureReadingValue

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingValue

### Description
The exposure measured.

### Data Type
float

### Position
7

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureReadingValue

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 7

___

## Create Data Field

### Display Name
BandMaximumValue

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::BandMaximumValue

### Description
The limit compared against.

### Data Type
float

### Position
8

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::BandMaximumValue

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

### Label
field 8

___

## Create Data Field

### Display Name
ExposureLimitExceededFlag

### Qualified Name
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureLimitExceededFlag

### Description
Whether the limit was exceeded.

### Data Type
boolean

### Position
9

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
DataField::Coco::Exposure Monitoring Results::Exposure Measurement::ExposureLimitExceededFlag

### Data Structure
DataStructure::Coco::Exposure Monitoring Results::Exposure Measurement

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: exposure_monitoring_results
- schemaDescription: Personal and static exposure measurements from monitoring campaigns, compared to the banded limits, against the workers and tasks monitored. An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.

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
coco_pharma.incidents_and_near_misses

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
IncidentIdentifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentIdentifier

### Description
The incident.

### Data Type
string

### Position
1

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentIdentifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 1

___

## Create Data Field

### Display Name
IncidentType

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentType

### Description
Incident or near miss.

### Data Type
string

### Position
2

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentType

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 2

___

## Create Data Field

### Display Name
IncidentTimestamp

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentTimestamp

### Description
When it occurred.

### Data Type
date

### Position
3

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentTimestamp

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 3

___

## Create Data Field

### Display Name
IncidentReportedTimestamp

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentReportedTimestamp

### Description
When reported.

### Data Type
date

### Position
4

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentReportedTimestamp

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 4

___

## Create Data Field

### Display Name
SiteCode

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::SiteCode

### Description
The site.

### Data Type
string

### Position
5

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
DataField::Coco::Incidents And Near Misses::Incident::SiteCode

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 5

___

## Create Data Field

### Display Name
IncidentLocation

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentLocation

### Description
Where.

### Data Type
string

### Position
6

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentLocation

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 6

___

## Create Data Field

### Display Name
SubstanceCode

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::SubstanceCode

### Description
The substance implicated, if any.

### Data Type
string

### Position
7

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
DataField::Coco::Incidents And Near Misses::Incident::SubstanceCode

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 7

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::WorkerPseudonymIdentifier

### Description
The worker affected, if any.

### Data Type
string

### Position
8

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
DataField::Coco::Incidents And Near Misses::Incident::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 8

___

## Create Data Field

### Display Name
IncidentDescription

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentDescription

### Description
What happened and the immediate response.

### Data Type
string

### Position
9

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentDescription

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

### Label
field 9

___

## Create Data Field

### Display Name
IncidentSeverity

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident::IncidentSeverity

### Description
The assessed seriousness.

### Data Type
string

### Position
10

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
DataField::Coco::Incidents And Near Misses::Incident::IncidentSeverity

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident

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
coco_pharma.incidents_and_near_misses

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
IncidentIdentifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentIdentifier

### Description
The incident.

### Data Type
string

### Position
1

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
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentIdentifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Label
field 1

___

## Create Data Field

### Display Name
IncidentFindingNumber

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingNumber

### Description
The finding's sequence.

### Data Type
int

### Position
2

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
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingNumber

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Label
field 2

___

## Create Data Field

### Display Name
IncidentFindingDescription

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingDescription

### Description
The finding.

### Data Type
string

### Position
3

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
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingDescription

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Label
field 3

___

## Create Data Field

### Display Name
ControlIdentifier

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::ControlIdentifier

### Description
The control implicated, if any.

### Data Type
string

### Position
4

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
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::ControlIdentifier

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

### Label
field 4

___

## Create Data Field

### Display Name
IncidentFindingActionDescription

### Qualified Name
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingActionDescription

### Description
The change to assessments or controls that follows.

### Data Type
string

### Position
5

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
DataField::Coco::Incidents And Near Misses::Incident Investigation Finding::IncidentFindingActionDescription

### Data Structure
DataStructure::Coco::Incidents And Near Misses::Incident Investigation Finding

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: incidents_and_near_misses
- schemaDescription: Incidents, near misses and their investigations, with the substance or control implicated and the findings fed back into the exposure assessments. It is what makes the health surveillance chain a loop rather than a line.

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
