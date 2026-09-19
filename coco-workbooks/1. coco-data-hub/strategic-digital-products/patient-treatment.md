# Patient Treatment Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 3 digital products owned by the Patient Treatment business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products originating in the direct-to-patient channel: treatment orders, the pseudonym register that protects patient identity through the rest of the chain, and the adverse reactions clinicians report.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Treatment Orders | `CocoPharma::SolutionComponent::TreatmentOrderingPortal` | Transactional Record | Treatment Order, Sample Collection Request |
| Clinician Adverse Reaction Reports | `CocoPharma::SolutionComponent::TreatmentOrderingPortal` | Event Stream | Clinician Reaction Report |
| Patient Pseudonym Register | `CocoPharma::SolutionComponent::PatientIdentityRegister` | Master Data | Patient Pseudonym Link, Administration Record |

For every product this file:

1. creates the **digital product** and adds it to the `Patient Treatment` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

3 products, 5 data structures, 31 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret patient-treatment.md
```

---

# Treatment Orders

*Solution component:* `CocoPharma::SolutionComponent::TreatmentOrderingPortal`  
*Category:* Transactional Record

The orders placed by treating clinicians for personalised therapies: the patient, the prescribing clinician, the product ordered and the sample collection it requires.  It is the point at which a treatment decision made outside the company becomes an instruction inside it.

## Create Digital Product

### Display Name
Treatment Orders

### Product Name
Treatment Orders

### Qualified Name
DigitalProduct::Coco::Treatment Orders

### Description
The orders placed by treating clinicians for personalised therapies: the patient, the prescribing clinician, the product ordered and the sample collection it requires.  It is the point at which a treatment decision made outside the company becomes an instruction inside it.

### Purpose
Starts the personalised treatment chain with a complete, identified order that the pseudonym register and the sample logistics can act on.

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
CollectionFolder::Coco::Strategic Digital Products::Patient Treatment

### Element Id
DigitalProduct::Coco::Treatment Orders

### Membership Rationale
Produced by the Patient Treatment group's `TreatmentOrderingPortal` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Treatment Orders Data Spec

### Qualified Name
DataSpec::Coco::Treatment Orders

### Description
The data structures and fields that make up the Treatment Orders digital product.

### Purpose
Describes the data a subscriber to Treatment Orders receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Treatment Orders

### Collection Id
DataSpec::Coco::Treatment Orders

### Label
data specification

___

## Create Data Structure

### Display Name
Treatment Order

### Qualified Name
DataStructure::Coco::Treatment Orders::Treatment Order

### Description
One row per order placed through the portal.

### Namespace Path
coco_pharma.treatment_orders

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Treatment Orders

### Element Id
DataStructure::Coco::Treatment Orders::Treatment Order

### Membership Rationale
The Treatment Order structure is part of the Treatment Orders data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::OrderIdentifier

### Description
The unique identifier of the order.

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
DataField::Coco::Treatment Orders::Treatment Order::OrderIdentifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 1

___

## Create Data Field

### Display Name
OrderDate

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::OrderDate

### Description
When the order was placed.

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
DataField::Coco::Treatment Orders::Treatment Order::OrderDate

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 2

___

## Create Data Field

### Display Name
PatientIdentifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::PatientIdentifier

### Description
The patient the therapy is for, as identified by the treating site.

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
DataField::Coco::Treatment Orders::Treatment Order::PatientIdentifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 3

___

## Create Data Field

### Display Name
ClinicianIdentifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::ClinicianIdentifier

### Description
The prescribing clinician.

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
DataField::Coco::Treatment Orders::Treatment Order::ClinicianIdentifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 4

___

## Create Data Field

### Display Name
HospitalIdentifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::HospitalIdentifier

### Description
The treating site.

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
DataField::Coco::Treatment Orders::Treatment Order::HospitalIdentifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 5

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::ProductCode

### Description
The product ordered.

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
DataField::Coco::Treatment Orders::Treatment Order::ProductCode

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 6

___

## Create Data Field

### Display Name
OrderQuantity

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::OrderQuantity

### Description
The number of doses ordered.

### Data Type
int

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
DataField::Coco::Treatment Orders::Treatment Order::OrderQuantity

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 7

___

## Create Data Field

### Display Name
OrderCurrentStatus

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::OrderCurrentStatus

### Description
Where the order is in its life.

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
DataField::Coco::Treatment Orders::Treatment Order::OrderCurrentStatus

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Label
field 8

___

## Create Data Structure

### Display Name
Sample Collection Request

### Qualified Name
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Description
One row per request for patient material to be collected for an order.

### Namespace Path
coco_pharma.treatment_orders

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Treatment Orders

### Element Id
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Membership Rationale
The Sample Collection Request structure is part of the Treatment Orders data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::OrderIdentifier

### Description
The order the sample is for.

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
DataField::Coco::Treatment Orders::Sample Collection Request::OrderIdentifier

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Label
field 1

___

## Create Data Field

### Display Name
SampleCollectionLocation

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionLocation

### Description
Where the material is to be collected.

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
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionLocation

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Label
field 2

___

## Create Data Field

### Display Name
SampleCollectionStartDate

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionStartDate

### Description
The earliest the material may be taken.

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
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionStartDate

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Label
field 3

___

## Create Data Field

### Display Name
SampleCollectionEndDate

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionEndDate

### Description
The latest the material may be taken.

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
DataField::Coco::Treatment Orders::Sample Collection Request::SampleCollectionEndDate

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Label
field 4

___

## Create Data Field

### Display Name
SampleMaterialType

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::SampleMaterialType

### Description
The material required from the patient.

### Data Type
string

### Position
5

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
DataField::Coco::Treatment Orders::Sample Collection Request::SampleMaterialType

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

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
- schemaName: treatment_orders
- schemaDescription: The orders placed by treating clinicians for personalised therapies: the patient, the prescribing clinician, the product ordered and the sample collection it requires. It is the point at which a treatment decision made outside the company becomes an instruction inside it.

### Parent ID
DigitalProduct::Coco::Treatment Orders

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Clinician Adverse Reaction Reports

*Solution component:* `CocoPharma::SolutionComponent::TreatmentOrderingPortal`  
*Category:* Event Stream

Suspected adverse reactions reported by treating clinicians through the ordering portal, identifying the patient by pseudonym and the product and batch involved.  The data arrives through the same channel as orders but is of a different kind, and starts a different clock.

## Create Digital Product

### Display Name
Clinician Adverse Reaction Reports

### Product Name
Clinician Adverse Reaction Reports

### Qualified Name
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Description
Suspected adverse reactions reported by treating clinicians through the ordering portal, identifying the patient by pseudonym and the product and batch involved.  The data arrives through the same channel as orders but is of a different kind, and starts a different clock.

### Purpose
Gets a clinician's suspected reaction to the safety intake gateway on the day it is reported, with the product and batch attached.

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
CollectionFolder::Coco::Strategic Digital Products::Patient Treatment

### Element Id
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Membership Rationale
Produced by the Patient Treatment group's `TreatmentOrderingPortal` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Clinician Adverse Reaction Reports Data Spec

### Qualified Name
DataSpec::Coco::Clinician Adverse Reaction Reports

### Description
The data structures and fields that make up the Clinician Adverse Reaction Reports digital product.

### Purpose
Describes the data a subscriber to Clinician Adverse Reaction Reports receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Collection Id
DataSpec::Coco::Clinician Adverse Reaction Reports

### Label
data specification

___

## Create Data Structure

### Display Name
Clinician Reaction Report

### Qualified Name
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Description
One row per suspected reaction reported by a clinician.

### Namespace Path
coco_pharma.clinician_adverse_reaction_reports

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Clinician Adverse Reaction Reports

### Element Id
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Membership Rationale
The Clinician Reaction Report structure is part of the Clinician Adverse Reaction Reports data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
AdverseEventIdentifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventIdentifier

### Description
The unique identifier of the report.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventIdentifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 1

___

## Create Data Field

### Display Name
AdverseEventReportedDate

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventReportedDate

### Description
When the clinician reported the reaction.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventReportedDate

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 2

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 3

___

## Create Data Field

### Display Name
ClinicianIdentifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::ClinicianIdentifier

### Description
The reporting clinician.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::ClinicianIdentifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 4

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::ProductCode

### Description
The product suspected.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::ProductCode

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 5

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::BatchIdentifier

### Description
The batch administered, if known.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::BatchIdentifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 6

___

## Create Data Field

### Display Name
AdverseEventDescription

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventDescription

### Description
The clinician's description of the reaction.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventDescription

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 7

___

## Create Data Field

### Display Name
AdverseEventReportedSeverity

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventReportedSeverity

### Description
The severity as reported by the clinician.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::AdverseEventReportedSeverity

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Label
field 8

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
- schemaName: clinician_adverse_reaction_reports
- schemaDescription: Suspected adverse reactions reported by treating clinicians through the ordering portal, identifying the patient by pseudonym and the product and batch involved. The data arrives through the same channel as orders but is of a different kind, and starts a different clock.

### Parent ID
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Patient Pseudonym Register

*Solution component:* `CocoPharma::SolutionComponent::PatientIdentityRegister`  
*Category:* Master Data

The link between a patient, the material taken from them and the therapy manufactured from it, issued as a pseudonym that every other system in the chain works from.  Manufacturing can be certain it has the right material without ever holding the patient's identity.

## Create Digital Product

### Display Name
Patient Pseudonym Register

### Product Name
Patient Pseudonym Register

### Qualified Name
DigitalProduct::Coco::Patient Pseudonym Register

### Description
The link between a patient, the material taken from them and the therapy manufactured from it, issued as a pseudonym that every other system in the chain works from.  Manufacturing can be certain it has the right material without ever holding the patient's identity.

### Purpose
Protects patient identity through the manufacturing chain while guaranteeing that each therapy returns to the patient it was made for.

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
CollectionFolder::Coco::Strategic Digital Products::Patient Treatment

### Element Id
DigitalProduct::Coco::Patient Pseudonym Register

### Membership Rationale
Produced by the Patient Treatment group's `PatientIdentityRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Patient Pseudonym Register Data Spec

### Qualified Name
DataSpec::Coco::Patient Pseudonym Register

### Description
The data structures and fields that make up the Patient Pseudonym Register digital product.

### Purpose
Describes the data a subscriber to Patient Pseudonym Register receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Patient Pseudonym Register

### Collection Id
DataSpec::Coco::Patient Pseudonym Register

### Label
data specification

___

## Create Data Structure

### Display Name
Patient Pseudonym Link

### Qualified Name
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Description
One row per patient pseudonym issued for an order.

### Namespace Path
coco_pharma.patient_pseudonym_register

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Patient Pseudonym Register

### Element Id
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Membership Rationale
The Patient Pseudonym Link structure is part of the Patient Pseudonym Register data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientPseudonymIdentifier

### Description
The pseudonym issued.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Label
field 1

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::OrderIdentifier

### Description
The order the pseudonym was issued for.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::OrderIdentifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Label
field 2

___

## Create Data Field

### Display Name
PatientPseudonymIssuedTimestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientPseudonymIssuedTimestamp

### Description
When the pseudonym was issued.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientPseudonymIssuedTimestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Label
field 3

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::ProductCode

### Description
The product specified.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::ProductCode

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Label
field 4

___

## Create Data Field

### Display Name
PatientParameterDescription

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientParameterDescription

### Description
The patient-specific parameters manufacturing must apply.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::PatientParameterDescription

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Label
field 5

___

## Create Data Structure

### Display Name
Administration Record

### Qualified Name
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Description
One row per therapy delivered and administered, closing the loop the order opened.

### Namespace Path
coco_pharma.patient_pseudonym_register

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Patient Pseudonym Register

### Element Id
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Membership Rationale
The Administration Record structure is part of the Patient Pseudonym Register data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Label
field 1

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::BatchIdentifier

### Description
The therapy administered.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::BatchIdentifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Label
field 2

___

## Create Data Field

### Display Name
TreatmentDeliveryTimestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentDeliveryTimestamp

### Description
When the therapy arrived at the treating site.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentDeliveryTimestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Label
field 3

___

## Create Data Field

### Display Name
TreatmentAdministrationTimestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentAdministrationTimestamp

### Description
When the therapy was administered.

### Data Type
date

### Position
4

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
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentAdministrationTimestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Label
field 4

___

## Create Data Field

### Display Name
TreatmentAdministrationConfirmedFlag

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentAdministrationConfirmedFlag

### Description
Whether administration has been confirmed by the site.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::TreatmentAdministrationConfirmedFlag

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

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
- schemaName: patient_pseudonym_register
- schemaDescription: The link between a patient, the material taken from them and the therapy manufactured from it, issued as a pseudonym that every other system in the chain works from. Manufacturing can be certain it has the right material without ever holding the patient's identity.

### Parent ID
DigitalProduct::Coco::Patient Pseudonym Register

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
