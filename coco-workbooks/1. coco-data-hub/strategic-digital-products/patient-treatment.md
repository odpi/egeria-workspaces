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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

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
coco_data_hub.treatment_orders

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
Order Identifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Order Identifier

### Description
The unique identifier of the order.

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
DataField::Coco::Treatment Orders::Treatment Order::Order Identifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Order Date

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Order Date

### Description
When the order was placed.

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
DataField::Coco::Treatment Orders::Treatment Order::Order Date

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Patient Identifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Patient Identifier

### Description
The patient the therapy is for, as identified by the treating site.

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
DataField::Coco::Treatment Orders::Treatment Order::Patient Identifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Clinician Identifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Clinician Identifier

### Description
The prescribing clinician.

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
DataField::Coco::Treatment Orders::Treatment Order::Clinician Identifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Hospital Identifier

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Hospital Identifier

### Description
The treating site.

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
DataField::Coco::Treatment Orders::Treatment Order::Hospital Identifier

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

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
DataField::Coco::Treatment Orders::Treatment Order::Product Code

### Description
The product ordered.

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
DataField::Coco::Treatment Orders::Treatment Order::Product Code

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Order Quantity

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Order Quantity

### Description
The number of doses ordered.

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
DataField::Coco::Treatment Orders::Treatment Order::Order Quantity

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Order Current Status

### Qualified Name
DataField::Coco::Treatment Orders::Treatment Order::Order Current Status

### Description
Where the order is in its life.

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
DataField::Coco::Treatment Orders::Treatment Order::Order Current Status

### Data Structure
DataStructure::Coco::Treatment Orders::Treatment Order

### Position
8

### Coverage Category
CORE_DETAIL

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
coco_data_hub.treatment_orders

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
Order Identifier

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::Order Identifier

### Description
The order the sample is for.

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
DataField::Coco::Treatment Orders::Sample Collection Request::Order Identifier

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Sample Collection Location

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection Location

### Description
Where the material is to be collected.

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
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection Location

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Sample Collection Start Date

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection Start Date

### Description
The earliest the material may be taken.

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
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection Start Date

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Sample Collection End Date

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection End Date

### Description
The latest the material may be taken.

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
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Collection End Date

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Sample Material Type

### Qualified Name
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Material Type

### Description
The material required from the patient.

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
DataField::Coco::Treatment Orders::Sample Collection Request::Sample Material Type

### Data Structure
DataStructure::Coco::Treatment Orders::Sample Collection Request

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
coco_data_hub.clinician_adverse_reaction_reports

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
Adverse Event Identifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Identifier

### Description
The unique identifier of the report.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Identifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Adverse Event Reported Date

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Reported Date

### Description
When the clinician reported the reaction.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Reported Date

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Clinician Identifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Clinician Identifier

### Description
The reporting clinician.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Clinician Identifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Product Code

### Description
The product suspected.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Product Code

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Batch Identifier

### Description
The batch administered, if known.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Batch Identifier

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Adverse Event Description

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Description

### Description
The clinician's description of the reaction.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Description

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Adverse Event Reported Severity

### Qualified Name
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Reported Severity

### Description
The severity as reported by the clinician.

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
DataField::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report::Adverse Event Reported Severity

### Data Structure
DataStructure::Coco::Clinician Adverse Reaction Reports::Clinician Reaction Report

### Position
8

### Coverage Category
CORE_DETAIL

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
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
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
coco_data_hub.patient_pseudonym_register

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
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Pseudonym Identifier

### Description
The pseudonym issued.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Order Identifier

### Description
The order the pseudonym was issued for.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Order Identifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Patient Pseudonym Issued Timestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Pseudonym Issued Timestamp

### Description
When the pseudonym was issued.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Pseudonym Issued Timestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Product Code

### Description
The product specified.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Product Code

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Patient Parameter Description

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Parameter Description

### Description
The patient-specific parameters manufacturing must apply.

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
DataField::Coco::Patient Pseudonym Register::Patient Pseudonym Link::Patient Parameter Description

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Patient Pseudonym Link

### Position
5

### Coverage Category
CORE_DETAIL

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
coco_data_hub.patient_pseudonym_register

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
Batch Identifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::Batch Identifier

### Description
The therapy administered.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::Batch Identifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Treatment Delivery Timestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Delivery Timestamp

### Description
When the therapy arrived at the treating site.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Delivery Timestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Treatment Administration Timestamp

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Administration Timestamp

### Description
When the therapy was administered.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Administration Timestamp

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Treatment Administration Confirmed Flag

### Qualified Name
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Administration Confirmed Flag

### Description
Whether administration has been confirmed by the site.

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
DataField::Coco::Patient Pseudonym Register::Administration Record::Treatment Administration Confirmed Flag

### Data Structure
DataStructure::Coco::Patient Pseudonym Register::Administration Record

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
