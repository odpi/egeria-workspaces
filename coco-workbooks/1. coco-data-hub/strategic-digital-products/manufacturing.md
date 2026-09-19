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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

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
coco_pharma.personalised_manufacturing_schedule

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
BatchIdentifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::BatchIdentifier

### Description
The batch opened for the order.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::BatchIdentifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 1

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::OrderIdentifier

### Description
The order.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::OrderIdentifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 2

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::PatientPseudonymIdentifier

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 3

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::ProductCode

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::ProductCode

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 4

___

## Create Data Field

### Display Name
SlotStartTimestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotStartTimestamp

### Description
When manufacturing is scheduled to start.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotStartTimestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 5

___

## Create Data Field

### Display Name
SlotEndTimestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotEndTimestamp

### Description
When it must finish.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotEndTimestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 6

___

## Create Data Field

### Display Name
PatientParameterDescription

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::PatientParameterDescription

### Description
The patient-specific parameters applied.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::PatientParameterDescription

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

### Label
field 7

___

## Create Data Field

### Display Name
SlotStatus

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotStatus

### Description
Scheduled, in progress, complete or cancelled.

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
DataField::Coco::Personalised Manufacturing Schedule::Manufacturing Slot::SlotStatus

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Manufacturing Slot

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
coco_pharma.personalised_manufacturing_schedule

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Label
field 1

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Label
field 2

___

## Create Data Field

### Display Name
ShipmentDeliveryTimestamp

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentDeliveryTimestamp

### Description
When it arrived.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentDeliveryTimestamp

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Label
field 3

___

## Create Data Field

### Display Name
ShipmentArrivalDescription

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentArrivalDescription

### Description
The condition on arrival.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::ShipmentArrivalDescription

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

### Label
field 4

___

## Create Data Field

### Display Name
SampleViableDuration

### Qualified Name
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::SampleViableDuration

### Description
The remaining viable life on arrival, in hours.

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
DataField::Coco::Personalised Manufacturing Schedule::Patient Material Receipt::SampleViableDuration

### Data Structure
DataStructure::Coco::Personalised Manufacturing Schedule::Patient Material Receipt

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
- schemaName: personalised_manufacturing_schedule
- schemaDescription: Each accepted personalised order turned into a scheduled manufacturing slot, with the arriving patient material that fixes the deadline. Unlike batch scheduling it cannot defer or re-sequence freely, because the material has a viable life measured in days.

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
coco_pharma.batch_execution_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::BatchIdentifier

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
DataField::Coco::Batch Execution Records::Execution Step::BatchIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 1

___

## Create Data Field

### Display Name
ExecutionStepNumber

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepNumber

### Description
The step's position in the process.

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepNumber

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 2

___

## Create Data Field

### Display Name
ExecutionStepCode

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepCode

### Description
The step performed.

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepCode

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 3

___

## Create Data Field

### Display Name
ExecutionStepStartTimestamp

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepStartTimestamp

### Description
When it started.

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepStartTimestamp

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 4

___

## Create Data Field

### Display Name
ExecutionStepEndTimestamp

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepEndTimestamp

### Description
When it finished.

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepEndTimestamp

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 5

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::WorkerPseudonymIdentifier

### Description
The operator.

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
DataField::Coco::Batch Execution Records::Execution Step::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 6

___

## Create Data Field

### Display Name
ExecutionStepSignature

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepSignature

### Description
The operator's electronic signature.

### Data Type
string

### Position
7

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepSignature

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

### Label
field 7

___

## Create Data Field

### Display Name
ExecutionStepStatus

### Qualified Name
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepStatus

### Description
Complete, complete with deviation, or aborted.

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
DataField::Coco::Batch Execution Records::Execution Step::ExecutionStepStatus

### Data Structure
DataStructure::Coco::Batch Execution Records::Execution Step

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
coco_pharma.batch_execution_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::BatchIdentifier

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
DataField::Coco::Batch Execution Records::Material Usage::BatchIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Label
field 1

___

## Create Data Field

### Display Name
ExecutionStepNumber

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::ExecutionStepNumber

### Description
The step.

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
DataField::Coco::Batch Execution Records::Material Usage::ExecutionStepNumber

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Label
field 2

___

## Create Data Field

### Display Name
RawMaterialCode

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialCode

### Description
The material.

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
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialCode

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Label
field 3

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::LotIdentifier

### Description
The lot consumed.

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
DataField::Coco::Batch Execution Records::Material Usage::LotIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Label
field 4

___

## Create Data Field

### Display Name
RawMaterialUsedQuantity

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialUsedQuantity

### Description
The quantity consumed.

### Data Type
float

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
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialUsedQuantity

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

### Label
field 5

___

## Create Data Field

### Display Name
RawMaterialUsedUnit

### Qualified Name
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialUsedUnit

### Description
The unit.

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
DataField::Coco::Batch Execution Records::Material Usage::RawMaterialUsedUnit

### Data Structure
DataStructure::Coco::Batch Execution Records::Material Usage

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
coco_pharma.batch_execution_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::BatchIdentifier

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
DataField::Coco::Batch Execution Records::Equipment Usage::BatchIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Label
field 1

___

## Create Data Field

### Display Name
ExecutionStepNumber

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::ExecutionStepNumber

### Description
The step.

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
DataField::Coco::Batch Execution Records::Equipment Usage::ExecutionStepNumber

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Label
field 2

___

## Create Data Field

### Display Name
EquipmentIdentifier

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentIdentifier

### Description
The equipment.

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
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentIdentifier

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Label
field 3

___

## Create Data Field

### Display Name
EquipmentQualifiedStatus

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentQualifiedStatus

### Description
The qualification status read at the moment of use.

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
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentQualifiedStatus

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

### Label
field 4

___

## Create Data Field

### Display Name
EquipmentCalibrationEndDate

### Qualified Name
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentCalibrationEndDate

### Description
When the calibration in force at use expires.

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
DataField::Coco::Batch Execution Records::Equipment Usage::EquipmentCalibrationEndDate

### Data Structure
DataStructure::Coco::Batch Execution Records::Equipment Usage

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
- schemaName: batch_execution_records
- schemaDescription: The contemporaneous record of each production step: what was done, by whom, with which materials and on which equipment, together with the deviations raised during execution. It is the source of most of what ends up in the batch record.

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
coco_pharma.process_parameter_time_series

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
BatchIdentifier

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::BatchIdentifier

### Description
The batch in progress when the reading was taken.

### Data Type
string

### Position
1

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::BatchIdentifier

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 1

___

## Create Data Field

### Display Name
EquipmentIdentifier

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::EquipmentIdentifier

### Description
The equipment instrumented.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::EquipmentIdentifier

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 2

___

## Create Data Field

### Display Name
ProcessParameterCode

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterCode

### Description
The parameter measured.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterCode

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 3

___

## Create Data Field

### Display Name
ProcessParameterTimestamp

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterTimestamp

### Description
When measured.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterTimestamp

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 4

___

## Create Data Field

### Display Name
ProcessParameterValue

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterValue

### Description
The reading.

### Data Type
float

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterValue

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 5

___

## Create Data Field

### Display Name
ProcessParameterUnit

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterUnit

### Description
The unit.

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterUnit

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 6

___

## Create Data Field

### Display Name
ProcessParameterMinimumValue

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterMinimumValue

### Description
The lower validated limit.

### Data Type
float

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterMinimumValue

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

### Label
field 7

___

## Create Data Field

### Display Name
ProcessParameterMaximumValue

### Qualified Name
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterMaximumValue

### Description
The upper validated limit.

### Data Type
float

### Position
8

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
DataField::Coco::Process Parameter Time Series::Process Parameter Reading::ProcessParameterMaximumValue

### Data Structure
DataStructure::Coco::Process Parameter Time Series::Process Parameter Reading

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
- schemaName: process_parameter_time_series
- schemaDescription: The continuous record of critical process parameters captured from plant instrumentation, at a resolution nobody reads unless something went wrong, which is exactly when it cannot be recreated.

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
coco_pharma.equipment_qualification_status

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
EquipmentIdentifier

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentIdentifier

### Description
The equipment.

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
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentIdentifier

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Label
field 1

___

## Create Data Field

### Display Name
EquipmentName

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentName

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
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentName

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Label
field 2

___

## Create Data Field

### Display Name
EquipmentType

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentType

### Description
Its type.

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
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentType

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Label
field 3

___

## Create Data Field

### Display Name
SiteCode

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::SiteCode

### Description
The site it is installed at.

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
DataField::Coco::Equipment Qualification Status::Equipment::SiteCode

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

### Label
field 4

___

## Create Data Field

### Display Name
EquipmentCurrentStatus

### Qualified Name
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentCurrentStatus

### Description
In service, out of service or retired.

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
DataField::Coco::Equipment Qualification Status::Equipment::EquipmentCurrentStatus

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Equipment

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
coco_pharma.equipment_qualification_status

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
EquipmentIdentifier

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentIdentifier

### Description
The equipment.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentIdentifier

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Label
field 1

___

## Create Data Field

### Display Name
EquipmentQualifiedStatus

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedStatus

### Description
Qualified, requalification due, or not qualified.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedStatus

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Label
field 2

___

## Create Data Field

### Display Name
EquipmentQualifiedDate

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedDate

### Description
When last qualified.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedDate

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Label
field 3

___

## Create Data Field

### Display Name
EquipmentQualifiedEndDate

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedEndDate

### Description
When qualification lapses.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentQualifiedEndDate

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Label
field 4

___

## Create Data Field

### Display Name
EquipmentCalibrationDate

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentCalibrationDate

### Description
When last calibrated.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentCalibrationDate

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

### Label
field 5

___

## Create Data Field

### Display Name
EquipmentCalibrationEndDate

### Qualified Name
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentCalibrationEndDate

### Description
When calibration lapses.

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
DataField::Coco::Equipment Qualification Status::Qualification Status::EquipmentCalibrationEndDate

### Data Structure
DataStructure::Coco::Equipment Qualification Status::Qualification Status

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
- schemaName: equipment_qualification_status
- schemaDescription: The qualification and calibration status of every piece of equipment used in production, consulted at the moment of use because a qualification that lapsed last week invalidates production that has already happened.

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
coco_pharma.electronic_batch_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchIdentifier

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::ProductCode

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
DataField::Coco::Electronic Batch Records::Batch Record::ProductCode

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 2

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::PatientPseudonymIdentifier

### Description
The patient, for a personalised batch.

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
DataField::Coco::Electronic Batch Records::Batch Record::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 3

___

## Create Data Field

### Display Name
BatchStartTimestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchStartTimestamp

### Description
When manufacturing started.

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchStartTimestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 4

___

## Create Data Field

### Display Name
BatchEndTimestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchEndTimestamp

### Description
When it finished.

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchEndTimestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 5

___

## Create Data Field

### Display Name
BatchQuantity

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchQuantity

### Description
The quantity produced.

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchQuantity

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 6

___

## Create Data Field

### Display Name
BatchRecordCompleteFlag

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchRecordCompleteFlag

### Description
Whether every contributing section has been received.

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchRecordCompleteFlag

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

### Label
field 7

___

## Create Data Field

### Display Name
BatchCertificationStatus

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record::BatchCertificationStatus

### Description
Awaiting review, certified or rejected.

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
DataField::Coco::Electronic Batch Records::Batch Record::BatchCertificationStatus

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record

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
coco_pharma.electronic_batch_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchIdentifier

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
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Label
field 1

___

## Create Data Field

### Display Name
BatchRecordSectionType

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionType

### Description
Execution, process parameters, laboratory results, deviation disposition, excursion disposition or signature authority.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionType

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Label
field 2

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::SystemIdentifier

### Description
The contributing system.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::SystemIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Label
field 3

___

## Create Data Field

### Display Name
BatchRecordSectionReceivedTimestamp

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionReceivedTimestamp

### Description
When received.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionReceivedTimestamp

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

### Label
field 4

___

## Create Data Field

### Display Name
BatchRecordSectionReferenceIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionReferenceIdentifier

### Description
The source record referenced.

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
DataField::Coco::Electronic Batch Records::Batch Record Section::BatchRecordSectionReferenceIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Batch Record Section

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
coco_pharma.electronic_batch_records

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
BatchIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchIdentifier

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
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Label
field 1

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::MarketCode

### Description
The market released to.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::MarketCode

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Label
field 2

___

## Create Data Field

### Display Name
BatchReleasedQuantity

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchReleasedQuantity

### Description
The quantity released to the market.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchReleasedQuantity

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Label
field 3

___

## Create Data Field

### Display Name
BatchCertificationDate

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchCertificationDate

### Description
When certified.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchCertificationDate

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

### Label
field 4

___

## Create Data Field

### Display Name
BatchCertifierIdentifier

### Qualified Name
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchCertifierIdentifier

### Description
The Qualified Person.

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
DataField::Coco::Electronic Batch Records::Release Authorisation::BatchCertifierIdentifier

### Data Structure
DataStructure::Coco::Electronic Batch Records::Release Authorisation

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
- schemaName: electronic_batch_records
- schemaDescription: The complete record of each batch assembled from every contributing system and held for the life of the obligation: execution, process parameters, laboratory results, deviation dispositions, excursion dispositions and signature authority, followed by the release authorisation once certified.

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
coco_pharma.serial_number_allocations

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
AllocationIdentifier

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationIdentifier

### Description
The allocation.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationIdentifier

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::ProductCode

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::ProductCode

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 2

___

## Create Data Field

### Display Name
PackCode

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::PackCode

### Description
The pack presentation.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::PackCode

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 3

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::MarketCode

### Description
The destination market.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::MarketCode

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 4

___

## Create Data Field

### Display Name
AllocationStartNumber

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationStartNumber

### Description
The first serial number in the block.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationStartNumber

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 5

___

## Create Data Field

### Display Name
AllocationEndNumber

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationEndNumber

### Description
The last serial number in the block.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationEndNumber

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 6

___

## Create Data Field

### Display Name
AllocationCount

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationCount

### Description
The number of identifiers allocated.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationCount

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 7

___

## Create Data Field

### Display Name
AllocationTimestamp

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationTimestamp

### Description
When allocated.

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::AllocationTimestamp

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

### Label
field 8

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Serial Number Allocations::Serial Number Allocation::BatchIdentifier

### Description
The batch the block is reserved for.

### Data Type
string

### Position
9

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
DataField::Coco::Serial Number Allocations::Serial Number Allocation::BatchIdentifier

### Data Structure
DataStructure::Coco::Serial Number Allocations::Serial Number Allocation

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
- schemaName: serial_number_allocations
- schemaDescription: The unique identifiers issued for saleable packs, allocated per product, pack presentation and destination market before the line starts. Uniqueness is assured at generation, because a number issued twice cannot be corrected once packs are distributed.

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
coco_pharma.commissioned_packs

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
PackSerialNumber

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::PackSerialNumber

### Description
The pack's serial number.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::PackSerialNumber

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 1

___

## Create Data Field

### Display Name
PackCode

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::PackCode

### Description
The presentation.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::PackCode

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 2

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::BatchIdentifier

### Description
The batch.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::BatchIdentifier

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 3

___

## Create Data Field

### Display Name
PackExpiryDate

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::PackExpiryDate

### Description
The expiry printed on the pack.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::PackExpiryDate

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 4

___

## Create Data Field

### Display Name
PackCommissionedTimestamp

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::PackCommissionedTimestamp

### Description
When commissioned.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::PackCommissionedTimestamp

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 5

___

## Create Data Field

### Display Name
PackVerifiedFlag

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::PackVerifiedFlag

### Description
Whether the applied identifier was read back and verified.

### Data Type
boolean

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
DataField::Coco::Commissioned Packs::Commissioned Pack::PackVerifiedFlag

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

### Label
field 6

___

## Create Data Field

### Display Name
EquipmentIdentifier

### Qualified Name
DataField::Coco::Commissioned Packs::Commissioned Pack::EquipmentIdentifier

### Description
The line.

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
DataField::Coco::Commissioned Packs::Commissioned Pack::EquipmentIdentifier

### Data Structure
DataStructure::Coco::Commissioned Packs::Commissioned Pack

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
coco_pharma.commissioned_packs

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
PackSerialNumber

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::PackSerialNumber

### Description
The pack.

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::PackSerialNumber

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Label
field 1

___

## Create Data Field

### Display Name
CaseSerialNumber

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::CaseSerialNumber

### Description
The case it was placed in.

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::CaseSerialNumber

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

### Label
field 2

___

## Create Data Field

### Display Name
PackAggregatedTimestamp

### Qualified Name
DataField::Coco::Commissioned Packs::Pack To Case Assignment::PackAggregatedTimestamp

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
DataField::Coco::Commissioned Packs::Pack To Case Assignment::PackAggregatedTimestamp

### Data Structure
DataStructure::Coco::Commissioned Packs::Pack To Case Assignment

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: commissioned_packs
- schemaDescription: Each pack that has had its identifier applied, verified and commissioned as a real, saleable object on the packaging line, and its assignment to a case. It works at line speed, which is why the identifiers had to be present before the line started.

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
coco_pharma.pack_aggregation_hierarchy

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
AggregationIdentifier

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationIdentifier

### Description
The relationship.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationIdentifier

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 1

___

## Create Data Field

### Display Name
AggregationParentSerialNumber

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationParentSerialNumber

### Description
The containing case or pallet.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationParentSerialNumber

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 2

___

## Create Data Field

### Display Name
AggregationParentType

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationParentType

### Description
Case or pallet.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationParentType

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 3

___

## Create Data Field

### Display Name
AggregationChildSerialNumber

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationChildSerialNumber

### Description
The contained pack or case.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationChildSerialNumber

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 4

___

## Create Data Field

### Display Name
AggregationChildType

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationChildType

### Description
Pack or case.

### Data Type
string

### Position
5

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationChildType

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 5

___

## Create Data Field

### Display Name
AggregationTimestamp

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationTimestamp

### Description
When recorded.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::AggregationTimestamp

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

### Label
field 6

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::BatchIdentifier

### Description
The batch.

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
DataField::Coco::Pack Aggregation Hierarchy::Aggregation Relationship::BatchIdentifier

### Data Structure
DataStructure::Coco::Pack Aggregation Hierarchy::Aggregation Relationship

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
- schemaName: pack_aggregation_hierarchy
- schemaDescription: Which packs are in which case and which cases are on which pallet. The relationships allow a shipment to be verified without opening it and make a recall a query rather than a search.

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
coco_pharma.serialised_product_identifiers

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
PackSerialNumber

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackSerialNumber

### Description
The identifier.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackSerialNumber

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::ProductCode

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::ProductCode

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 2

___

## Create Data Field

### Display Name
PackCode

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackCode

### Description
The presentation.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackCode

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 3

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::BatchIdentifier

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::BatchIdentifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 4

___

## Create Data Field

### Display Name
PackExpiryDate

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackExpiryDate

### Description
The expiry.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackExpiryDate

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 5

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::MarketCode

### Description
The destination market.

### Data Type
string

### Position
6

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::MarketCode

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 6

___

## Create Data Field

### Display Name
PackCurrentStatus

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackCurrentStatus

### Description
Allocated, commissioned, aggregated, shipped, decommissioned or destroyed.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::PackCurrentStatus

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 7

___

## Create Data Field

### Display Name
AggregationParentSerialNumber

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::AggregationParentSerialNumber

### Description
The case or pallet currently containing it.

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::AggregationParentSerialNumber

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

### Label
field 8

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::WarehouseCode

### Description
The location, while in stock.

### Data Type
string

### Position
9

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
DataField::Coco::Serialised Product Identifiers::Serialised Identifier::WarehouseCode

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Serialised Identifier

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
coco_pharma.serialised_product_identifiers

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
PackSerialNumber

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackSerialNumber

### Description
The identifier.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackSerialNumber

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Label
field 1

___

## Create Data Field

### Display Name
PackEventType

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackEventType

### Description
Commissioned, aggregated, shipped, verified, decommissioned, corrected.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackEventType

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Label
field 2

___

## Create Data Field

### Display Name
PackEventTimestamp

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackEventTimestamp

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::PackEventTimestamp

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Label
field 3

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::SystemIdentifier

### Description
The system that reported the event.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::SystemIdentifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

### Label
field 4

___

## Create Data Field

### Display Name
AlertIdentifier

### Qualified Name
DataField::Coco::Serialised Product Identifiers::Identifier Event::AlertIdentifier

### Description
The alert disposition that caused a correction, if any.

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
DataField::Coco::Serialised Product Identifiers::Identifier Event::AlertIdentifier

### Data Structure
DataStructure::Coco::Serialised Product Identifiers::Identifier Event

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
- schemaName: serialised_product_identifiers
- schemaDescription: The company's own record of every identifier issued, commissioned, aggregated, shipped and decommissioned, and the alert dispositions that corrected it. It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.

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
coco_pharma.market_identifier_submissions

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
SubmissionIdentifier

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionIdentifier

### Description
The upload.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionIdentifier

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 1

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::BatchIdentifier

### Description
The batch.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::BatchIdentifier

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 2

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::MarketCode

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::MarketCode

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 3

___

## Create Data Field

### Display Name
VerificationSchemeCode

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::VerificationSchemeCode

### Description
The national or regional scheme.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::VerificationSchemeCode

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 4

___

## Create Data Field

### Display Name
SubmissionTimestamp

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionTimestamp

### Description
When uploaded.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionTimestamp

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 5

___

## Create Data Field

### Display Name
SubmissionCount

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionCount

### Description
The number of identifiers uploaded.

### Data Type
int

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionCount

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 6

___

## Create Data Field

### Display Name
SubmissionAcknowledgedFlag

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionAcknowledgedFlag

### Description
Whether the scheme acknowledged the upload.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::SubmissionAcknowledgedFlag

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

### Label
field 7

___

## Create Data Field

### Display Name
BatchCertificationDate

### Qualified Name
DataField::Coco::Market Identifier Submissions::Identifier Submission::BatchCertificationDate

### Description
The certification the upload relied on.

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
DataField::Coco::Market Identifier Submissions::Identifier Submission::BatchCertificationDate

### Data Structure
DataStructure::Coco::Market Identifier Submissions::Identifier Submission

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
- schemaName: market_identifier_submissions
- schemaDescription: The identifier records uploaded to the national and regional verification systems of each destination market, together with the release authorisation each upload relied on. Destination determines the scheme, so the same production run may leave through several routes.

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
coco_pharma.market_verification_responses

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
VerificationEventIdentifier

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventIdentifier

### Description
The event.

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
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventIdentifier

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Label
field 1

___

## Create Data Field

### Display Name
PackSerialNumber

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::PackSerialNumber

### Description
The identifier scanned.

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
DataField::Coco::Market Verification Responses::Verification Result::PackSerialNumber

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Label
field 2

___

## Create Data Field

### Display Name
VerificationSchemeCode

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::VerificationSchemeCode

### Description
The scheme reporting.

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
DataField::Coco::Market Verification Responses::Verification Result::VerificationSchemeCode

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Label
field 3

___

## Create Data Field

### Display Name
VerificationEventType

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventType

### Description
Verified, decommissioned, or failed.

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
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventType

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Label
field 4

___

## Create Data Field

### Display Name
VerificationEventTimestamp

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventTimestamp

### Description
When.

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
DataField::Coco::Market Verification Responses::Verification Result::VerificationEventTimestamp

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

### Label
field 5

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Result::MarketCode

### Description
The market.

### Data Type
string

### Position
6

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
DataField::Coco::Market Verification Responses::Verification Result::MarketCode

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Result

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
coco_pharma.market_verification_responses

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
AlertIdentifier

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::AlertIdentifier

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
DataField::Coco::Market Verification Responses::Verification Alert::AlertIdentifier

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Label
field 1

___

## Create Data Field

### Display Name
PackSerialNumber

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::PackSerialNumber

### Description
The identifier involved.

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
DataField::Coco::Market Verification Responses::Verification Alert::PackSerialNumber

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Label
field 2

___

## Create Data Field

### Display Name
VerificationSchemeCode

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::VerificationSchemeCode

### Description
The scheme.

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
DataField::Coco::Market Verification Responses::Verification Alert::VerificationSchemeCode

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Label
field 3

___

## Create Data Field

### Display Name
AlertType

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::AlertType

### Description
Unknown identifier, already decommissioned, expiry mismatch or other.

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
DataField::Coco::Market Verification Responses::Verification Alert::AlertType

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Label
field 4

___

## Create Data Field

### Display Name
AlertRaisedTimestamp

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::AlertRaisedTimestamp

### Description
When raised.

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
DataField::Coco::Market Verification Responses::Verification Alert::AlertRaisedTimestamp

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

### Label
field 5

___

## Create Data Field

### Display Name
AlertReporterDescription

### Qualified Name
DataField::Coco::Market Verification Responses::Verification Alert::AlertReporterDescription

### Description
The pharmacy or partner that scanned.

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
DataField::Coco::Market Verification Responses::Verification Alert::AlertReporterDescription

### Data Structure
DataStructure::Coco::Market Verification Responses::Verification Alert

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
- schemaName: market_verification_responses
- schemaDescription: What the national verification systems send back: verification results, decommissioning events, and the alerts raised when a pharmacy or trading partner scans an identifier that does not verify. The data originates outside the company, in systems that are opaque to it.

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
