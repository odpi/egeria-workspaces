# Manufacturing Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 11 digital products owned by the Manufacturing business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of production and serialisation: schedules, execution records, process time series, equipment status, the electronic batch record, serial number allocations, commissioned packs, aggregation, the serialisation repository and the market verification traffic.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Personalised Manufacturing Schedule | `CocoPharma::SolutionComponent::PersonalisedOrderScheduler` | Transactional Record | Manufacturing Slot, Patient Material Receipt |
| Batch Execution Records | `CocoPharma::SolutionComponent::ManufacturingExecution` | Evidence Record | Execution Step, Material Usage, Equipment Usage |
| Process Parameter Time Series | `CocoPharma::SolutionComponent::ProcessHistorian` | Time Series | Process Parameter Reading |
| Equipment Qualification Status | `CocoPharma::SolutionComponent::EquipmentQualificationRegister` | Reference Data | Equipment, Qualification Status |
| Electronic Batch Records | `CocoPharma::SolutionComponent::ElectronicBatchRecord` | Evidence Record | Batch Record, Batch Record Section, Release Authorisation |
| Serial Number Allocations | `CocoPharma::SolutionComponent::SerialNumberGenerator` | Transactional Record | Serial Number Allocation |
| Commissioned Packs | `CocoPharma::SolutionComponent::PackagingLineController` | Event Stream | Commissioned Pack, Pack To Case Assignment |
| Pack Aggregation Hierarchy | `CocoPharma::SolutionComponent::AggregationRecorder` | Reference Data | Aggregation Relationship |
| Serialised Product Identifiers | `CocoPharma::SolutionComponent::SerialisationRepository` | Master Data | Serialised Identifier, Identifier Event |
| Market Identifier Submissions | `CocoPharma::SolutionComponent::MarketVerificationGateway` | Regulatory Submission | Identifier Submission |
| Market Verification Responses | `CocoPharma::SolutionComponent::MarketVerificationGateway` | Event Stream | Verification Result, Verification Alert |

For every product this file:

1. creates the **digital product** and adds it to the `Manufacturing` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

11 products, 20 data structures, 129 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret manufacturing.md
```

---

# Personalised Manufacturing Schedule

*Solution component:* `CocoPharma::SolutionComponent::PersonalisedOrderScheduler`  
*Category:* Transactional Record

Each accepted personalised order turned into a scheduled manufacturing slot, with the arriving patient material that fixes the deadline.  Unlike batch scheduling it cannot defer or re-sequence freely, because the material has a viable life measured in days.

## Create Digital Product

### Display Name
Personalised Manufacturing Schedule

### Product Name
Personalised Manufacturing Schedule

### Qualified Name
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Description
Each accepted personalised order turned into a scheduled manufacturing slot, with the arriving patient material that fixes the deadline.  Unlike batch scheduling it cannot defer or re-sequence freely, because the material has a viable life measured in days.

### Purpose
Gives manufacturing execution an instruction that is identified by pseudonym and constrained by the material's remaining viable life.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Membership Rationale
Produced by the Manufacturing group's `PersonalisedOrderScheduler` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Personalised Manufacturing Schedule Data Spec

### Qualified Name
DataSpec::Coco::Personalised Manufacturing Schedule

### Description
The data structures and fields that make up the Personalised Manufacturing Schedule digital product.

### Purpose
Describes the data a subscriber to Personalised Manufacturing Schedule receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Collection Id
DataSpec::Coco::Personalised Manufacturing Schedule

### Label
data specification

___

## Create Data Structure

### Display Name
Manufacturing Slot

### Qualified Name
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Description
One row per scheduled slot for a personalised order.

### Namespace Path
coco_data_hub.personalised_manufacturing_schedule

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Personalised Manufacturing Schedule

### Element Id
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Membership Rationale
The Manufacturing Slot structure is part of the Personalised Manufacturing Schedule data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Batch Identifier

### Description
The batch opened for the order.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Batch Identifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Order Identifier

### Description
The order.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Order Identifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Patient Pseudonym Identifier

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Product Code

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Product Code

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Slot Start Timestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot Start Timestamp

### Description
When manufacturing is scheduled to start.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot Start Timestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Slot End Timestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot End Timestamp

### Description
When it must finish.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot End Timestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Patient Parameter Description

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Patient Parameter Description

### Description
The patient-specific parameters applied.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Patient Parameter Description

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Slot Status

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot Status

### Description
Scheduled, in progress, complete or cancelled.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::Slot Status

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Patient Material Receipt

### Qualified Name
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Description
One row per consignment of patient material received at the manufacturing site.

### Namespace Path
coco_data_hub.personalised_manufacturing_schedule

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Personalised Manufacturing Schedule

### Element Id
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Membership Rationale
The Patient Material Receipt structure is part of the Personalised Manufacturing Schedule data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Identifier

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Identifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Patient Pseudonym Identifier

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Shipment Delivery Timestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Delivery Timestamp

### Description
When it arrived.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Delivery Timestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Shipment Arrival Description

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Arrival Description

### Description
The condition on arrival.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Shipment Arrival Description

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Sample Viable Duration

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Sample Viable Duration

### Description
The remaining viable life on arrival, in hours.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::Sample Viable Duration

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

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
- schemaName: personalised_manufacturing_schedule
- schemaDescription: Each accepted personalised order turned into a scheduled manufacturing slot, with the arriving patient material that fixes the deadline. Unlike batch scheduling it cannot defer or re-sequence freely, because the material has a viable life measured in days.

### Anchor ID
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Batch Execution Records

*Solution component:* `CocoPharma::SolutionComponent::ManufacturingExecution`  
*Category:* Evidence Record

The contemporaneous record of each production step: what was done, by whom, with which materials and on which equipment, together with the deviations raised during execution.  It is the source of most of what ends up in the batch record.

## Create Digital Product

### Display Name
Batch Execution Records

### Product Name
Batch Execution Records

### Qualified Name
DigitalProduct::Coco::Batch Execution Records

### Description
The contemporaneous record of each production step: what was done, by whom, with which materials and on which equipment, together with the deviations raised during execution.  It is the source of most of what ends up in the batch record.

### Purpose
Provides the batch record with an execution history that was written as it happened and cannot be reconstructed afterwards.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Batch Execution Records

### Membership Rationale
Produced by the Manufacturing group's `ManufacturingExecution` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Batch Execution Records Data Spec

### Qualified Name
DataSpec::Coco::Batch Execution Records

### Description
The data structures and fields that make up the Batch Execution Records digital product.

### Purpose
Describes the data a subscriber to Batch Execution Records receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Batch Execution Records

### Collection Id
DataSpec::Coco::Batch Execution Records

### Label
data specification

___

## Create Data Structure

### Display Name
Execution Step

### Qualified Name
DataStructure::Coco::Batch Execution Records::Execution Step

### Description
One row per production step performed for a batch.

### Namespace Path
coco_data_hub.batch_execution_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Batch Execution Records

### Element Id
DataStructure::Coco::Batch Execution Records::Execution Step

### Membership Rationale
The Execution Step structure is part of the Batch Execution Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Batch Identifier

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
DataField::Coco::Batch Execution Records::Execution Step::Batch Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Execution Step Number

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Number

### Description
The step's position in the process.

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
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Number

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Execution Step Code

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Code

### Description
The step performed.

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
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Code

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Execution Step Start Timestamp

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Start Timestamp

### Description
When it started.

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
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Start Timestamp

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Execution Step End Timestamp

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step End Timestamp

### Description
When it finished.

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
DataField::Coco::Batch Execution Records::Execution Step::Execution Step End Timestamp

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Worker Pseudonym Identifier

### Description
The operator.

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
DataField::Coco::Batch Execution Records::Execution Step::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Execution Step Signature

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Signature

### Description
The operator's electronic signature.

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
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Signature

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Execution Step Status

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Status

### Description
Complete, complete with deviation, or aborted.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
100

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Batch Execution Records::Execution Step::Execution Step Status

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Material Usage

### Qualified Name
DataStructure::Coco::Batch Execution Records::Material Usage

### Description
One row per lot of material consumed in a step.

### Namespace Path
coco_data_hub.batch_execution_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Batch Execution Records

### Element Id
DataStructure::Coco::Batch Execution Records::Material Usage

### Membership Rationale
The Material Usage structure is part of the Batch Execution Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Batch Identifier

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
DataField::Coco::Batch Execution Records::Material Usage::Batch Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Execution Step Number

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Execution Step Number

### Description
The step.

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
DataField::Coco::Batch Execution Records::Material Usage::Execution Step Number

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Lot Identifier

### Description
The lot consumed.

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
DataField::Coco::Batch Execution Records::Material Usage::Lot Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Raw Material Code

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Code

### Description
The material.

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
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Code

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Raw Material Used Quantity

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Used Quantity

### Description
The quantity consumed.

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
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Used Quantity

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Raw Material Used Unit

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Used Unit

### Description
The unit.

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
DataField::Coco::Batch Execution Records::Material Usage::Raw Material Used Unit

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Equipment Usage

### Qualified Name
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Description
One row per piece of equipment used in a step, with its qualification status at the time.

### Namespace Path
coco_data_hub.batch_execution_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Batch Execution Records

### Element Id
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Membership Rationale
The Equipment Usage structure is part of the Batch Execution Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::Batch Identifier

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
DataField::Coco::Batch Execution Records::Equipment Usage::Batch Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Execution Step Number

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::Execution Step Number

### Description
The step.

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
DataField::Coco::Batch Execution Records::Equipment Usage::Execution Step Number

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Equipment Identifier

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Identifier

### Description
The equipment.

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
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Identifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Equipment Qualified Status

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Qualified Status

### Description
The qualification status read at the moment of use.

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
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Qualified Status

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Equipment Calibration End Date

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Calibration End Date

### Description
When the calibration in force at use expires.

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
DataField::Coco::Batch Execution Records::Equipment Usage::Equipment Calibration End Date

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

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
- schemaName: batch_execution_records
- schemaDescription: The contemporaneous record of each production step: what was done, by whom, with which materials and on which equipment, together with the deviations raised during execution. It is the source of most of what ends up in the batch record.

### Anchor ID
DigitalProduct::Coco::Batch Execution Records

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Batch Execution Records

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Process Parameter Time Series

*Solution component:* `CocoPharma::SolutionComponent::ProcessHistorian`  
*Category:* Time Series

The continuous record of critical process parameters captured from plant instrumentation, at a resolution nobody reads unless something went wrong, which is exactly when it cannot be recreated.

## Create Digital Product

### Display Name
Process Parameter Time Series

### Product Name
Process Parameter Time Series

### Qualified Name
DigitalProduct::Coco::Process Parameter Time Series

### Description
The continuous record of critical process parameters captured from plant instrumentation, at a resolution nobody reads unless something went wrong, which is exactly when it cannot be recreated.

### Purpose
Holds the evidence that each batch stayed within its validated process range.

### Category
Time Series

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Process Parameter Time Series

### Membership Rationale
Produced by the Manufacturing group's `ProcessHistorian` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Process Parameter Time Series Data Spec

### Qualified Name
DataSpec::Coco::Process Parameter Time Series

### Description
The data structures and fields that make up the Process Parameter Time Series digital product.

### Purpose
Describes the data a subscriber to Process Parameter Time Series receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Process Parameter Time Series

### Collection Id
DataSpec::Coco::Process Parameter Time Series

### Label
data specification

___

## Create Data Structure

### Display Name
Process Parameter Reading

### Qualified Name
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Description
One row per instrument reading.

### Namespace Path
coco_data_hub.process_parameter_time_series

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Process Parameter Time Series

### Element Id
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Membership Rationale
The Process Parameter Reading structure is part of the Process Parameter Time Series data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Equipment Identifier

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Equipment Identifier

### Description
The equipment instrumented.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Equipment Identifier

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Process Parameter Code

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Code

### Description
The parameter measured.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Code

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Process Parameter Timestamp

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Timestamp

### Description
When measured.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Timestamp

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Batch Identifier

### Description
The batch in progress when the reading was taken.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Batch Identifier

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Process Parameter Value

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Value

### Description
The reading.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Value

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Process Parameter Unit

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Unit

### Description
The unit.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Unit

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Process Parameter Minimum Value

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Minimum Value

### Description
The lower validated limit.

### Data Type
float

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Minimum Value

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Process Parameter Maximum Value

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Maximum Value

### Description
The upper validated limit.

### Data Type
float

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::Process Parameter Maximum Value

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

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
- schemaName: process_parameter_time_series
- schemaDescription: The continuous record of critical process parameters captured from plant instrumentation, at a resolution nobody reads unless something went wrong, which is exactly when it cannot be recreated.

### Anchor ID
DigitalProduct::Coco::Process Parameter Time Series

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Process Parameter Time Series

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Equipment Qualification Status

*Solution component:* `CocoPharma::SolutionComponent::EquipmentQualificationRegister`  
*Category:* Reference Data

The qualification and calibration status of every piece of equipment used in production, consulted at the moment of use because a qualification that lapsed last week invalidates production that has already happened.

## Create Digital Product

### Display Name
Equipment Qualification Status

### Product Name
Equipment Qualification Status

### Qualified Name
DigitalProduct::Coco::Equipment Qualification Status

### Description
The qualification and calibration status of every piece of equipment used in production, consulted at the moment of use because a qualification that lapsed last week invalidates production that has already happened.

### Purpose
Tells manufacturing execution whether a piece of equipment may be used now.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Equipment Qualification Status

### Membership Rationale
Produced by the Manufacturing group's `EquipmentQualificationRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Equipment Qualification Status Data Spec

### Qualified Name
DataSpec::Coco::Equipment Qualification Status

### Description
The data structures and fields that make up the Equipment Qualification Status digital product.

### Purpose
Describes the data a subscriber to Equipment Qualification Status receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Equipment Qualification Status

### Collection Id
DataSpec::Coco::Equipment Qualification Status

### Label
data specification

___

## Create Data Structure

### Display Name
Equipment

### Qualified Name
DataStructure::Coco::Equipment Qualification Status::Equipment

### Description
One row per piece of production equipment.

### Namespace Path
coco_data_hub.equipment_qualification_status

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Equipment Qualification Status

### Element Id
DataStructure::Coco::Equipment Qualification Status::Equipment

### Membership Rationale
The Equipment structure is part of the Equipment Qualification Status data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Equipment Identifier

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Identifier

### Description
The equipment.

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
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Identifier

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Equipment Name

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Name

### Description
Its name.

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
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Name

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Equipment Type

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Type

### Description
Its type.

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
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Type

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Site Code

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::Site Code

### Description
The site it is installed at.

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
DataField::Coco::Equipment Qualification Status::Equipment::Site Code

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Equipment Current Status

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Current Status

### Description
In service, out of service or retired.

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
DataField::Coco::Equipment Qualification Status::Equipment::Equipment Current Status

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Structure

### Display Name
Qualification Status

### Qualified Name
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Description
One row per equipment, its current qualification and calibration validity.

### Namespace Path
coco_data_hub.equipment_qualification_status

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Equipment Qualification Status

### Element Id
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Membership Rationale
The Qualification Status structure is part of the Equipment Qualification Status data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Equipment Identifier

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Identifier

### Description
The equipment.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Identifier

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Equipment Qualified Status

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified Status

### Description
Qualified, requalification due, or not qualified.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified Status

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Equipment Qualified Date

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified Date

### Description
When last qualified.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified Date

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Equipment Qualified End Date

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified End Date

### Description
When qualification lapses.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Qualified End Date

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Equipment Calibration Date

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Calibration Date

### Description
When last calibrated.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Calibration Date

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Equipment Calibration End Date

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Calibration End Date

### Description
When calibration lapses.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::Equipment Calibration End Date

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

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
- schemaName: equipment_qualification_status
- schemaDescription: The qualification and calibration status of every piece of equipment used in production, consulted at the moment of use because a qualification that lapsed last week invalidates production that has already happened.

### Anchor ID
DigitalProduct::Coco::Equipment Qualification Status

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Equipment Qualification Status

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Electronic Batch Records

*Solution component:* `CocoPharma::SolutionComponent::ElectronicBatchRecord`  
*Category:* Evidence Record

The complete record of each batch assembled from every contributing system and held for the life of the obligation: execution, process parameters, laboratory results, deviation dispositions, excursion dispositions and signature authority, followed by the release authorisation once certified.

## Create Digital Product

### Display Name
Electronic Batch Records

### Product Name
Electronic Batch Records

### Qualified Name
DigitalProduct::Coco::Electronic Batch Records

### Description
The complete record of each batch assembled from every contributing system and held for the life of the obligation: execution, process parameters, laboratory results, deviation dispositions, excursion dispositions and signature authority, followed by the release authorisation once certified.

### Purpose
Provides the Qualified Person with a batch record whose completeness is a property of the chain having delivered, and provides serialisation with the release that lets packs be sold.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Electronic Batch Records

### Membership Rationale
Produced by the Manufacturing group's `ElectronicBatchRecord` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Electronic Batch Records Data Spec

### Qualified Name
DataSpec::Coco::Electronic Batch Records

### Description
The data structures and fields that make up the Electronic Batch Records digital product.

### Purpose
Describes the data a subscriber to Electronic Batch Records receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Electronic Batch Records

### Collection Id
DataSpec::Coco::Electronic Batch Records

### Label
data specification

___

## Create Data Structure

### Display Name
Batch Record

### Qualified Name
DataStructure::Coco::Electronic Batch Records::Batch Record

### Description
One row per batch.

### Namespace Path
coco_data_hub.electronic_batch_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Electronic Batch Records

### Element Id
DataStructure::Coco::Electronic Batch Records::Batch Record

### Membership Rationale
The Batch Record structure is part of the Electronic Batch Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::Batch Identifier

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

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
DataField::Coco::Electronic Batch Records::Batch Record::Product Code

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
DataField::Coco::Electronic Batch Records::Batch Record::Product Code

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

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
DataField::Coco::Electronic Batch Records::Batch Record::Patient Pseudonym Identifier

### Description
The patient, for a personalised batch.

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
DataField::Coco::Electronic Batch Records::Batch Record::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Batch Start Timestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::Batch Start Timestamp

### Description
When manufacturing started.

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Start Timestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Batch End Timestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::Batch End Timestamp

### Description
When it finished.

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch End Timestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Batch Quantity

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::Batch Quantity

### Description
The quantity produced.

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Quantity

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Record Complete Flag

### Description
Whether every contributing section has been received.

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Record Complete Flag

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Batch Certification Status

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::Batch Certification Status

### Description
Awaiting review, certified or rejected.

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
DataField::Coco::Electronic Batch Records::Batch Record::Batch Certification Status

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Batch Record Section

### Qualified Name
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Description
One row per contribution received from a source system for a batch.

### Namespace Path
coco_data_hub.electronic_batch_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Electronic Batch Records

### Element Id
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Membership Rationale
The Batch Record Section structure is part of the Electronic Batch Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Identifier

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
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Batch Record Section Reference Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Reference Identifier

### Description
The source record referenced.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Reference Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Batch Record Section Type

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Type

### Description
Execution, process parameters, laboratory results, deviation disposition, excursion disposition or signature authority.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Type

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::System Identifier

### Description
The contributing system.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::System Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Batch Record Section Received Timestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Received Timestamp

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
DataField::Coco::Electronic Batch Records::Batch Record Section::Batch Record Section Received Timestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Structure

### Display Name
Release Authorisation

### Qualified Name
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Description
One row per certified batch per market, the quantities released.

### Namespace Path
coco_data_hub.electronic_batch_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Electronic Batch Records

### Element Id
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Membership Rationale
The Release Authorisation structure is part of the Electronic Batch Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Identifier

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Market Code

### Description
The market released to.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Market Code

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Batch Released Quantity

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Released Quantity

### Description
The quantity released to the market.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Released Quantity

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Certification Date

### Description
When certified.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Certification Date

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Batch Certifier Identifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Certifier Identifier

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
DataField::Coco::Electronic Batch Records::Release Authorisation::Batch Certifier Identifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

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
- schemaName: electronic_batch_records
- schemaDescription: The complete record of each batch assembled from every contributing system and held for the life of the obligation: execution, process parameters, laboratory results, deviation dispositions, excursion dispositions and signature authority, followed by the release authorisation once certified.

### Anchor ID
DigitalProduct::Coco::Electronic Batch Records

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Electronic Batch Records

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Serial Number Allocations

*Solution component:* `CocoPharma::SolutionComponent::SerialNumberGenerator`  
*Category:* Transactional Record

The unique identifiers issued for saleable packs, allocated per product, pack presentation and destination market before the line starts.  Uniqueness is assured at generation, because a number issued twice cannot be corrected once packs are distributed.

## Create Digital Product

### Display Name
Serial Number Allocations

### Product Name
Serial Number Allocations

### Qualified Name
DigitalProduct::Coco::Serial Number Allocations

### Description
The unique identifiers issued for saleable packs, allocated per product, pack presentation and destination market before the line starts.  Uniqueness is assured at generation, because a number issued twice cannot be corrected once packs are distributed.

### Purpose
Supplies the packaging line with identifiers that are guaranteed unique and valid for the market the packs are going to.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Serial Number Allocations

### Membership Rationale
Produced by the Manufacturing group's `SerialNumberGenerator` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Serial Number Allocations Data Spec

### Qualified Name
DataSpec::Coco::Serial Number Allocations

### Description
The data structures and fields that make up the Serial Number Allocations digital product.

### Purpose
Describes the data a subscriber to Serial Number Allocations receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Serial Number Allocations

### Collection Id
DataSpec::Coco::Serial Number Allocations

### Label
data specification

___

## Create Data Structure

### Display Name
Serial Number Allocation

### Qualified Name
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Description
One row per block of serial numbers allocated.

### Namespace Path
coco_data_hub.serial_number_allocations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Serial Number Allocations

### Element Id
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Membership Rationale
The Serial Number Allocation structure is part of the Serial Number Allocations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Allocation Identifier

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Identifier

### Description
The allocation.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Identifier

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Product Code

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Product Code

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Pack Code

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Pack Code

### Description
The pack presentation.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Pack Code

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Market Code

### Description
The destination market.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Market Code

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Allocation Start Number

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Start Number

### Description
The first serial number in the block.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Start Number

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Allocation End Number

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation End Number

### Description
The last serial number in the block.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation End Number

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Allocation Count

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Count

### Description
The number of identifiers allocated.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Count

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Allocation Timestamp

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Timestamp

### Description
When allocated.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Allocation Timestamp

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Batch Identifier

### Description
The batch the block is reserved for.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::Batch Identifier

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

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
- schemaName: serial_number_allocations
- schemaDescription: The unique identifiers issued for saleable packs, allocated per product, pack presentation and destination market before the line starts. Uniqueness is assured at generation, because a number issued twice cannot be corrected once packs are distributed.

### Anchor ID
DigitalProduct::Coco::Serial Number Allocations

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Serial Number Allocations

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Commissioned Packs

*Solution component:* `CocoPharma::SolutionComponent::PackagingLineController`  
*Category:* Event Stream

Each pack that has had its identifier applied, verified and commissioned as a real, saleable object on the packaging line, and its assignment to a case.  It works at line speed, which is why the identifiers had to be present before the line started.

## Create Digital Product

### Display Name
Commissioned Packs

### Product Name
Commissioned Packs

### Qualified Name
DigitalProduct::Coco::Commissioned Packs

### Description
Each pack that has had its identifier applied, verified and commissioned as a real, saleable object on the packaging line, and its assignment to a case.  It works at line speed, which is why the identifiers had to be present before the line started.

### Purpose
Turns an allocated identifier into a commissioned pack the serialisation repository and the aggregation record can rely on.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Commissioned Packs

### Membership Rationale
Produced by the Manufacturing group's `PackagingLineController` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Commissioned Packs Data Spec

### Qualified Name
DataSpec::Coco::Commissioned Packs

### Description
The data structures and fields that make up the Commissioned Packs digital product.

### Purpose
Describes the data a subscriber to Commissioned Packs receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Commissioned Packs

### Collection Id
DataSpec::Coco::Commissioned Packs

### Label
data specification

___

## Create Data Structure

### Display Name
Commissioned Pack

### Qualified Name
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Description
One row per pack commissioned.

### Namespace Path
coco_data_hub.commissioned_packs

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Commissioned Packs

### Element Id
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Membership Rationale
The Commissioned Pack structure is part of the Commissioned Packs data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Serial Number

### Description
The pack's serial number.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Serial Number

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Pack Code

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Code

### Description
The presentation.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Code

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Batch Identifier

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Batch Identifier

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Pack Expiry Date

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Expiry Date

### Description
The expiry printed on the pack.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Expiry Date

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Pack Commissioned Timestamp

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Commissioned Timestamp

### Description
When commissioned.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Commissioned Timestamp

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Pack Verified Flag

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Verified Flag

### Description
Whether the applied identifier was read back and verified.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Pack Verified Flag

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Equipment Identifier

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::Equipment Identifier

### Description
The line.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::Equipment Identifier

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Pack To Case Assignment

### Qualified Name
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Description
One row per pack placed in a case.

### Namespace Path
coco_data_hub.commissioned_packs

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Commissioned Packs

### Element Id
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Membership Rationale
The Pack To Case Assignment structure is part of the Commissioned Packs data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Pack Serial Number

### Description
The pack.

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Pack Serial Number

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Case Serial Number

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Case Serial Number

### Description
The case it was placed in.

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Case Serial Number

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Pack Aggregated Timestamp

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Pack Aggregated Timestamp

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::Pack Aggregated Timestamp

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

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
- schemaName: commissioned_packs
- schemaDescription: Each pack that has had its identifier applied, verified and commissioned as a real, saleable object on the packaging line, and its assignment to a case. It works at line speed, which is why the identifiers had to be present before the line started.

### Anchor ID
DigitalProduct::Coco::Commissioned Packs

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Commissioned Packs

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Pack Aggregation Hierarchy

*Solution component:* `CocoPharma::SolutionComponent::AggregationRecorder`  
*Category:* Reference Data

Which packs are in which case and which cases are on which pallet.  The relationships allow a shipment to be verified without opening it and make a recall a query rather than a search.

## Create Digital Product

### Display Name
Pack Aggregation Hierarchy

### Product Name
Pack Aggregation Hierarchy

### Qualified Name
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Description
Which packs are in which case and which cases are on which pallet.  The relationships allow a shipment to be verified without opening it and make a recall a query rather than a search.

### Purpose
Gives the serialisation repository and every downstream verification the physical containment of each identifier.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Membership Rationale
Produced by the Manufacturing group's `AggregationRecorder` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Pack Aggregation Hierarchy Data Spec

### Qualified Name
DataSpec::Coco::Pack Aggregation Hierarchy

### Description
The data structures and fields that make up the Pack Aggregation Hierarchy digital product.

### Purpose
Describes the data a subscriber to Pack Aggregation Hierarchy receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Collection Id
DataSpec::Coco::Pack Aggregation Hierarchy

### Label
data specification

___

## Create Data Structure

### Display Name
Aggregation Relationship

### Qualified Name
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Description
One row per containment of one serialised unit in another.

### Namespace Path
coco_data_hub.pack_aggregation_hierarchy

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Pack Aggregation Hierarchy

### Element Id
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Membership Rationale
The Aggregation Relationship structure is part of the Pack Aggregation Hierarchy data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Aggregation Identifier

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Identifier

### Description
The relationship.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Identifier

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Aggregation Parent Serial Number

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Parent Serial Number

### Description
The containing case or pallet.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Parent Serial Number

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Aggregation Parent Type

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Parent Type

### Description
Case or pallet.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Parent Type

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Aggregation Child Serial Number

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Child Serial Number

### Description
The contained pack or case.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Child Serial Number

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Aggregation Child Type

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Child Type

### Description
Pack or case.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Child Type

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Aggregation Timestamp

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Timestamp

### Description
When recorded.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Aggregation Timestamp

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Batch Identifier

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::Batch Identifier

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

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
- schemaName: pack_aggregation_hierarchy
- schemaDescription: Which packs are in which case and which cases are on which pallet. The relationships allow a shipment to be verified without opening it and make a recall a query rather than a search.

### Anchor ID
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Pack Aggregation Hierarchy

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Serialised Product Identifiers

*Solution component:* `CocoPharma::SolutionComponent::SerialisationRepository`  
*Category:* Master Data

The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned, and the alert dispositions that corrected it.  It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.

## Create Digital Product

### Display Name
Serialised Product Identifiers

### Product Name
Serialised Product Identifiers

### Qualified Name
DigitalProduct::Coco::Serialised Product Identifiers

### Description
The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned, and the alert dispositions that corrected it.  It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.

### Purpose
Provides the authoritative status and location of every serialised unit the company has produced.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Serialised Product Identifiers

### Membership Rationale
Produced by the Manufacturing group's `SerialisationRepository` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Serialised Product Identifiers Data Spec

### Qualified Name
DataSpec::Coco::Serialised Product Identifiers

### Description
The data structures and fields that make up the Serialised Product Identifiers digital product.

### Purpose
Describes the data a subscriber to Serialised Product Identifiers receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Serialised Product Identifiers

### Collection Id
DataSpec::Coco::Serialised Product Identifiers

### Label
data specification

___

## Create Data Structure

### Display Name
Serialised Identifier

### Qualified Name
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Description
One row per identifier, its current state.

### Namespace Path
coco_data_hub.serialised_product_identifiers

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Serialised Product Identifiers

### Element Id
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Membership Rationale
The Serialised Identifier structure is part of the Serialised Product Identifiers data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Serial Number

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Serial Number

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Product Code

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Product Code

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Pack Code

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Code

### Description
The presentation.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Code

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Batch Identifier

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Batch Identifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Pack Expiry Date

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Expiry Date

### Description
The expiry.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Expiry Date

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Market Code

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Market Code

### Description
The destination market.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Market Code

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Pack Current Status

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Current Status

### Description
Allocated, commissioned, aggregated, shipped, decommissioned or destroyed.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Pack Current Status

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Aggregation Parent Serial Number

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Aggregation Parent Serial Number

### Description
The case or pallet currently containing it.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Aggregation Parent Serial Number

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Warehouse Code

### Description
The location, while in stock.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::Warehouse Code

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Identifier Event

### Qualified Name
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Description
One row per change of state of an identifier.

### Namespace Path
coco_data_hub.serialised_product_identifiers

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Serialised Product Identifiers

### Element Id
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Membership Rationale
The Identifier Event structure is part of the Serialised Product Identifiers data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Serial Number

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Serial Number

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Serial Number

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Pack Event Timestamp

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Event Timestamp

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Event Timestamp

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Pack Event Type

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Event Type

### Description
Commissioned, aggregated, shipped, verified, decommissioned, corrected.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::Pack Event Type

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::System Identifier

### Description
The system that reported the event.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::System Identifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Alert Identifier

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::Alert Identifier

### Description
The alert disposition that caused a correction, if any.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::Alert Identifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

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
- schemaName: serialised_product_identifiers
- schemaDescription: The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned, and the alert dispositions that corrected it. It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.

### Anchor ID
DigitalProduct::Coco::Serialised Product Identifiers

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Serialised Product Identifiers

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Market Identifier Submissions

*Solution component:* `CocoPharma::SolutionComponent::MarketVerificationGateway`  
*Category:* Regulatory Submission

The identifier records uploaded to the national and regional verification systems of each destination market, together with the release authorisation each upload relied on.  Destination determines the scheme, so the same production run may leave through several routes.

## Create Digital Product

### Display Name
Market Identifier Submissions

### Product Name
Market Identifier Submissions

### Qualified Name
DigitalProduct::Coco::Market Identifier Submissions

### Description
The identifier records uploaded to the national and regional verification systems of each destination market, together with the release authorisation each upload relied on.  Destination determines the scheme, so the same production run may leave through several routes.

### Purpose
Records what was uploaded to which scheme and when, so that an unacknowledged upload is visible.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Market Identifier Submissions

### Membership Rationale
Produced by the Manufacturing group's `MarketVerificationGateway` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Market Identifier Submissions Data Spec

### Qualified Name
DataSpec::Coco::Market Identifier Submissions

### Description
The data structures and fields that make up the Market Identifier Submissions digital product.

### Purpose
Describes the data a subscriber to Market Identifier Submissions receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Market Identifier Submissions

### Collection Id
DataSpec::Coco::Market Identifier Submissions

### Label
data specification

___

## Create Data Structure

### Display Name
Identifier Submission

### Qualified Name
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Description
One row per batch per market scheme uploaded to.

### Namespace Path
coco_data_hub.market_identifier_submissions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Market Identifier Submissions

### Element Id
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Membership Rationale
The Identifier Submission structure is part of the Market Identifier Submissions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Submission Identifier

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Identifier

### Description
The upload.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Identifier

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Batch Identifier

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Batch Identifier

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Market Code

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Market Code

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Verification Scheme Code

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Verification Scheme Code

### Description
The national or regional scheme.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Verification Scheme Code

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Submission Timestamp

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Timestamp

### Description
When uploaded.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Timestamp

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Submission Count

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Count

### Description
The number of identifiers uploaded.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Count

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Submission Acknowledged Flag

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Acknowledged Flag

### Description
Whether the scheme acknowledged the upload.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Submission Acknowledged Flag

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Batch Certification Date

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::Batch Certification Date

### Description
The certification the upload relied on.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::Batch Certification Date

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

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
- schemaName: market_identifier_submissions
- schemaDescription: The identifier records uploaded to the national and regional verification systems of each destination market, together with the release authorisation each upload relied on. Destination determines the scheme, so the same production run may leave through several routes.

### Anchor ID
DigitalProduct::Coco::Market Identifier Submissions

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Market Identifier Submissions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Market Verification Responses

*Solution component:* `CocoPharma::SolutionComponent::MarketVerificationGateway`  
*Category:* Event Stream

What the national verification systems send back: verification results, decommissioning events, and the alerts raised when a pharmacy or trading partner scans an identifier that does not verify.  The data originates outside the company, in systems that are opaque to it.

## Create Digital Product

### Display Name
Market Verification Responses

### Product Name
Market Verification Responses

### Qualified Name
DigitalProduct::Coco::Market Verification Responses

### Description
What the national verification systems send back: verification results, decommissioning events, and the alerts raised when a pharmacy or trading partner scans an identifier that does not verify.  The data originates outside the company, in systems that are opaque to it.

### Purpose
Brings the external verification traffic inside the company as events that reconciliation and alert triage can act on.

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
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Element Id
DigitalProduct::Coco::Market Verification Responses

### Membership Rationale
Produced by the Manufacturing group's `MarketVerificationGateway` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Market Verification Responses Data Spec

### Qualified Name
DataSpec::Coco::Market Verification Responses

### Description
The data structures and fields that make up the Market Verification Responses digital product.

### Purpose
Describes the data a subscriber to Market Verification Responses receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Market Verification Responses

### Collection Id
DataSpec::Coco::Market Verification Responses

### Label
data specification

___

## Create Data Structure

### Display Name
Verification Result

### Qualified Name
DataStructure::Coco::Market Verification Responses::Verification Result

### Description
One row per verification or decommissioning event received.

### Namespace Path
coco_data_hub.market_verification_responses

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Market Verification Responses

### Element Id
DataStructure::Coco::Market Verification Responses::Verification Result

### Membership Rationale
The Verification Result structure is part of the Market Verification Responses data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Verification Event Identifier

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Identifier

### Description
The event.

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
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Identifier

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

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
DataField::Coco::Market Verification Responses::Verification Result::Pack Serial Number

### Description
The identifier scanned.

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
DataField::Coco::Market Verification Responses::Verification Result::Pack Serial Number

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Verification Scheme Code

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::Verification Scheme Code

### Description
The scheme reporting.

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
DataField::Coco::Market Verification Responses::Verification Result::Verification Scheme Code

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Verification Event Type

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Type

### Description
Verified, decommissioned, or failed.

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
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Type

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Verification Event Timestamp

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Timestamp

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
DataField::Coco::Market Verification Responses::Verification Result::Verification Event Timestamp

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Market Code

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::Market Code

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
DataField::Coco::Market Verification Responses::Verification Result::Market Code

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Verification Alert

### Qualified Name
DataStructure::Coco::Market Verification Responses::Verification Alert

### Description
One row per alert raised by a scheme.

### Namespace Path
coco_data_hub.market_verification_responses

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Market Verification Responses

### Element Id
DataStructure::Coco::Market Verification Responses::Verification Alert

### Membership Rationale
The Verification Alert structure is part of the Market Verification Responses data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Alert Identifier

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::Alert Identifier

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
DataField::Coco::Market Verification Responses::Verification Alert::Alert Identifier

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

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
DataField::Coco::Market Verification Responses::Verification Alert::Pack Serial Number

### Description
The identifier involved.

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
DataField::Coco::Market Verification Responses::Verification Alert::Pack Serial Number

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Verification Scheme Code

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::Verification Scheme Code

### Description
The scheme.

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
DataField::Coco::Market Verification Responses::Verification Alert::Verification Scheme Code

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Alert Type

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::Alert Type

### Description
Unknown identifier, already decommissioned, expiry mismatch or other.

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
DataField::Coco::Market Verification Responses::Verification Alert::Alert Type

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Alert Raised Timestamp

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::Alert Raised Timestamp

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
DataField::Coco::Market Verification Responses::Verification Alert::Alert Raised Timestamp

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Alert Reporter Description

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::Alert Reporter Description

### Description
The pharmacy or partner that scanned.

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
DataField::Coco::Market Verification Responses::Verification Alert::Alert Reporter Description

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

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
- schemaName: market_verification_responses
- schemaDescription: What the national verification systems send back: verification results, decommissioning events, and the alerts raised when a pharmacy or trading partner scans an identifier that does not verify. The data originates outside the company, in systems that are opaque to it.

### Anchor ID
DigitalProduct::Coco::Market Verification Responses

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Market Verification Responses

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
