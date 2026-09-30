# Warehouse Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 4 digital products owned by the Warehouse business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of physical stock handling: goods receipts, quarantine dispositions, the goods inventory and the hazardous material holdings.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Goods Receipts | `CocoPharma::SolutionComponent::GoodsReceiptAndInspection` | Transactional Record | Goods Receipt, Receipt Inspection |
| Material Quarantine Dispositions | `CocoPharma::SolutionComponent::MaterialQuarantineControl` | Transactional Record | Quarantine Record, Release Disposition |
| Goods Inventory Stock | `SolutionComponent::Goods Inventory::V1.0` | Transactional Record | Stock Position, Stock Movement, Material Issue |
| Hazardous Material Holdings | `SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0` | Reference Data | Substance Holding, Substance Hazard Data |

For every product this file:

1. creates the **digital product** and adds it to the `Warehouse` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

4 products, 9 data structures, 60 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret warehouse.md
```

---

# Goods Receipts

*Solution component:* `CocoPharma::SolutionComponent::GoodsReceiptAndInspection`  
*Category:* Transactional Record

What physically arrived: each lot of material received, checked against the order and the supplier's documentation, and what the inspection found.  It is the point at which a supplier's claim becomes the company's record.

## Create Digital Product

### Display Name
Goods Receipts

### Product Name
Goods Receipts

### Qualified Name
DigitalProduct::Coco::Goods Receipts

### Description
What physically arrived: each lot of material received, checked against the order and the supplier's documentation, and what the inspection found.  It is the point at which a supplier's claim becomes the company's record.

### Purpose
Records receipt and inspection so that quarantine, payment matching and stock all start from the same fact.

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
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Element Id
DigitalProduct::Coco::Goods Receipts

### Membership Rationale
Produced by the Warehouse group's `GoodsReceiptAndInspection` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Goods Receipts Data Spec

### Qualified Name
DataSpec::Coco::Goods Receipts

### Description
The data structures and fields that make up the Goods Receipts digital product.

### Purpose
Describes the data a subscriber to Goods Receipts receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Goods Receipts

### Collection Id
DataSpec::Coco::Goods Receipts

### Label
data specification

___

## Create Data Structure

### Display Name
Goods Receipt

### Qualified Name
DataStructure::Coco::Goods Receipts::Goods Receipt

### Description
One row per lot received.

### Namespace Path
coco_data_hub.goods_receipts

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Goods Receipts

### Element Id
DataStructure::Coco::Goods Receipts::Goods Receipt

### Membership Rationale
The Goods Receipt structure is part of the Goods Receipts data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Goods Receipt Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Identifier

### Description
The receipt.

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
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

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
DataField::Coco::Goods Receipts::Goods Receipt::Order Identifier

### Description
The purchase order.

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
DataField::Coco::Goods Receipts::Goods Receipt::Order Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Supplier Identifier

### Description
The supplier.

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
DataField::Coco::Goods Receipts::Goods Receipt::Supplier Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Raw Material Code

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Raw Material Code

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
DataField::Coco::Goods Receipts::Goods Receipt::Raw Material Code

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Lot Identifier

### Description
The supplier's lot.

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
DataField::Coco::Goods Receipts::Goods Receipt::Lot Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Goods Receipt Date

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Date

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
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Date

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Goods Receipt Quantity

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Quantity

### Description
The quantity received.

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
DataField::Coco::Goods Receipts::Goods Receipt::Goods Receipt Quantity

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Warehouse Code

### Description
The receiving location.

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
DataField::Coco::Goods Receipts::Goods Receipt::Warehouse Code

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::Certificate Identifier

### Description
The certificate that accompanied the lot.

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
DataField::Coco::Goods Receipts::Goods Receipt::Certificate Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Receipt Inspection

### Qualified Name
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Description
One row per inspection of a received lot.

### Namespace Path
coco_data_hub.goods_receipts

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Goods Receipts

### Element Id
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Membership Rationale
The Receipt Inspection structure is part of the Goods Receipts data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Goods Receipt Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Identifier

### Description
The receipt inspected.

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
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Goods Receipt Inspection Date

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Date

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
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Date

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Goods Receipt Inspector Identifier

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspector Identifier

### Description
Who inspected.

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
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspector Identifier

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Goods Receipt Inspection Status

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Status

### Description
Accepted, rejected or held.

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
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Status

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Goods Receipt Inspection Notes

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Notes

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
DataField::Coco::Goods Receipts::Receipt Inspection::Goods Receipt Inspection Notes

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

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
- schemaName: goods_receipts
- schemaDescription: What physically arrived: each lot of material received, checked against the order and the supplier's documentation, and what the inspection found. It is the point at which a supplier's claim becomes the company's record.

### Anchor ID
DigitalProduct::Coco::Goods Receipts

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Goods Receipts

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Material Quarantine Dispositions

*Solution component:* `CocoPharma::SolutionComponent::MaterialQuarantineControl`  
*Category:* Transactional Record

Each lot held in quarantine, the tests requested for it, and the disposition that released it for use or rejected it.  It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.

## Create Digital Product

### Display Name
Material Quarantine Dispositions

### Product Name
Material Quarantine Dispositions

### Qualified Name
DigitalProduct::Coco::Material Quarantine Dispositions

### Description
Each lot held in quarantine, the tests requested for it, and the disposition that released it for use or rejected it.  It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.

### Purpose
Guarantees that no material is issued to manufacturing until its testing and documentation review are complete.

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
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Element Id
DigitalProduct::Coco::Material Quarantine Dispositions

### Membership Rationale
Produced by the Warehouse group's `MaterialQuarantineControl` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Material Quarantine Dispositions Data Spec

### Qualified Name
DataSpec::Coco::Material Quarantine Dispositions

### Description
The data structures and fields that make up the Material Quarantine Dispositions digital product.

### Purpose
Describes the data a subscriber to Material Quarantine Dispositions receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Material Quarantine Dispositions

### Collection Id
DataSpec::Coco::Material Quarantine Dispositions

### Label
data specification

___

## Create Data Structure

### Display Name
Quarantine Record

### Qualified Name
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Description
One row per lot placed in quarantine.

### Namespace Path
coco_data_hub.material_quarantine_dispositions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Material Quarantine Dispositions

### Element Id
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Membership Rationale
The Quarantine Record structure is part of the Material Quarantine Dispositions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Identifier

### Description
The lot.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Identifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Raw Material Code

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Raw Material Code

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Raw Material Code

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Goods Receipt Identifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Goods Receipt Identifier

### Description
The receipt that placed it.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Goods Receipt Identifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Lot Quarantine Start Timestamp

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quarantine Start Timestamp

### Description
When quarantine began.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quarantine Start Timestamp

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Warehouse Code

### Description
The quarantine location.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Warehouse Code

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Lot Quantity

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quantity

### Description
The quantity held.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quantity

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Sample Identifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Sample Identifier

### Description
The sample sent for incoming testing.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Sample Identifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Lot Quarantine Status

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quarantine Status

### Description
Held, released or rejected.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::Lot Quarantine Status

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Release Disposition

### Qualified Name
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Description
One row per disposition decision on a quarantined lot.

### Namespace Path
coco_data_hub.material_quarantine_dispositions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Material Quarantine Dispositions

### Element Id
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Membership Rationale
The Release Disposition structure is part of the Material Quarantine Dispositions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Identifier

### Description
The lot.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Identifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Lot Disposition Timestamp

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Disposition Timestamp

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Disposition Timestamp

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Lot Disposition Status

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Disposition Status

### Description
Released for use or rejected.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Disposition Status

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Test Result Identifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Test Result Identifier

### Description
The laboratory result the decision rests on.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Test Result Identifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Lot Expiry Date

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Expiry Date

### Description
The expiry assigned to the released lot.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Expiry Date

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Lot Released Quantity

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Released Quantity

### Description
The quantity released.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::Lot Released Quantity

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

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
- schemaName: material_quarantine_dispositions
- schemaDescription: Each lot held in quarantine, the tests requested for it, and the disposition that released it for use or rejected it. It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.

### Anchor ID
DigitalProduct::Coco::Material Quarantine Dispositions

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Material Quarantine Dispositions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Goods Inventory Stock

*Solution component:* `SolutionComponent::Goods Inventory::V1.0`  
*Category:* Transactional Record

The stock of materials and finished goods at every location: the current position, the movements that produced it, and the issues of material to manufacturing with their quarantine status.  It also carries serialised finished goods once they are commissioned.

## Create Digital Product

### Display Name
Goods Inventory Stock

### Product Name
Goods Inventory Stock

### Qualified Name
DigitalProduct::Coco::Goods Inventory Stock

### Description
The stock of materials and finished goods at every location: the current position, the movements that produced it, and the issues of material to manufacturing with their quarantine status.  It also carries serialised finished goods once they are commissioned.

### Purpose
Gives manufacturing, the data hub and the hazardous materials register a single view of what is held where.

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
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Element Id
DigitalProduct::Coco::Goods Inventory Stock

### Membership Rationale
Produced by the Warehouse group's `Goods Inventory` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Goods Inventory Stock Data Spec

### Qualified Name
DataSpec::Coco::Goods Inventory Stock

### Description
The data structures and fields that make up the Goods Inventory Stock digital product.

### Purpose
Describes the data a subscriber to Goods Inventory Stock receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Goods Inventory Stock

### Collection Id
DataSpec::Coco::Goods Inventory Stock

### Label
data specification

___

## Create Data Structure

### Display Name
Stock Position

### Qualified Name
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Description
One row per material or product per location.

### Namespace Path
coco_data_hub.goods_inventory_stock

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Goods Inventory Stock

### Element Id
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Membership Rationale
The Stock Position structure is part of the Goods Inventory Stock data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Product Code

### Description
The material or product.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Product Code

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Warehouse Code

### Description
The location.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Warehouse Code

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

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
DataField::Coco::Goods Inventory Stock::Stock Position::Lot Identifier

### Description
The lot, where stock is lot-tracked.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Lot Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Stock Level

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Level

### Description
Quantity on hand.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Level

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Stock Minimum Level

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Minimum Level

### Description
The reorder level.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Minimum Level

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Stock Maximum Level

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Maximum Level

### Description
The maximum holding.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Maximum Level

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Stock Current Timestamp

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Current Timestamp

### Description
When the position was last updated.

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
DataField::Coco::Goods Inventory Stock::Stock Position::Stock Current Timestamp

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Stock Movement

### Qualified Name
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Description
One row per movement of stock into, out of or between locations.

### Namespace Path
coco_data_hub.goods_inventory_stock

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Goods Inventory Stock

### Element Id
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Membership Rationale
The Stock Movement structure is part of the Goods Inventory Stock data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Stock Movement Identifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Identifier

### Description
The movement.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Product Code

### Description
The material or product.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Product Code

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Lot Identifier

### Description
The lot.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Lot Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Stock Movement Type

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Type

### Description
Receipt, issue, transfer, adjustment or shipment.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Type

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Stock Movement Quantity

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Quantity

### Description
The quantity moved.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Quantity

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Stock Movement Timestamp

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Timestamp

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Stock Movement Timestamp

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::Warehouse Code

### Description
The location affected.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::Warehouse Code

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Material Issue

### Qualified Name
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Description
One row per issue of material to a manufacturing batch.

### Namespace Path
coco_data_hub.goods_inventory_stock

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Goods Inventory Stock

### Element Id
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Membership Rationale
The Material Issue structure is part of the Goods Inventory Stock data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Stock Movement Identifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::Stock Movement Identifier

### Description
The issue movement.

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
DataField::Coco::Goods Inventory Stock::Material Issue::Stock Movement Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

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
DataField::Coco::Goods Inventory Stock::Material Issue::Batch Identifier

### Description
The batch the material was issued to.

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
DataField::Coco::Goods Inventory Stock::Material Issue::Batch Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Raw Material Code

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::Raw Material Code

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
DataField::Coco::Goods Inventory Stock::Material Issue::Raw Material Code

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Lot Identifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::Lot Identifier

### Description
The lot issued.

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
DataField::Coco::Goods Inventory Stock::Material Issue::Lot Identifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Raw Material Issued Quantity

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::Raw Material Issued Quantity

### Description
The quantity issued.

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
DataField::Coco::Goods Inventory Stock::Material Issue::Raw Material Issued Quantity

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Lot Quarantine Status

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::Lot Quarantine Status

### Description
The lot's quarantine status at issue.

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
DataField::Coco::Goods Inventory Stock::Material Issue::Lot Quarantine Status

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

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
- schemaName: goods_inventory_stock
- schemaDescription: The stock of materials and finished goods at every location: the current position, the movements that produced it, and the issues of material to manufacturing with their quarantine status. It also carries serialised finished goods once they are commissioned.

### Anchor ID
DigitalProduct::Coco::Goods Inventory Stock

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Goods Inventory Stock

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Hazardous Material Holdings

*Solution component:* `SolutionComponent::Hazardous Materials (HazMat) Inventory::V1.0`  
*Category:* Reference Data

The hazardous substances the company holds, where and in what quantity, with the hazard data for each.  It serves occupational health, dangerous goods transport and physical inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.

## Create Digital Product

### Display Name
Hazardous Material Holdings

### Product Name
Hazardous Material Holdings

### Qualified Name
DigitalProduct::Coco::Hazardous Material Holdings

### Description
The hazardous substances the company holds, where and in what quantity, with the hazard data for each.  It serves occupational health, dangerous goods transport and physical inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.

### Purpose
Provides the substance identities and holdings that exposure banding and transport classification both start from.

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
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Element Id
DigitalProduct::Coco::Hazardous Material Holdings

### Membership Rationale
Produced by the Warehouse group's `Hazardous Materials (HazMat) Inventory` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Hazardous Material Holdings Data Spec

### Qualified Name
DataSpec::Coco::Hazardous Material Holdings

### Description
The data structures and fields that make up the Hazardous Material Holdings digital product.

### Purpose
Describes the data a subscriber to Hazardous Material Holdings receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Hazardous Material Holdings

### Collection Id
DataSpec::Coco::Hazardous Material Holdings

### Label
data specification

___

## Create Data Structure

### Display Name
Substance Holding

### Qualified Name
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Description
One row per substance per location.

### Namespace Path
coco_data_hub.hazardous_material_holdings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Hazardous Material Holdings

### Element Id
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Membership Rationale
The Substance Holding structure is part of the Hazardous Material Holdings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Code

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Warehouse Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Warehouse Code

### Description
The location.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Warehouse Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Substance Quantity

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Quantity

### Description
The quantity held.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Quantity

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Substance Unit

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Unit

### Description
The unit of the quantity.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Unit

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Substance Form Description

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Form Description

### Description
The physical form held, for example powder or solution.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Form Description

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Substance Current Timestamp

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Current Timestamp

### Description
When the holding was last updated.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::Substance Current Timestamp

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Substance Hazard Data

### Qualified Name
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Description
One row per substance, its hazard classification.

### Namespace Path
coco_data_hub.hazardous_material_holdings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Hazardous Material Holdings

### Element Id
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Membership Rationale
The Substance Hazard Data structure is part of the Hazardous Material Holdings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Code

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Name

### Description
The substance's name.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Name

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Substance Hazard Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Hazard Code

### Description
The hazard classification.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Hazard Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Substance Hazard Description

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Hazard Description

### Description
The hazards the substance presents.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Hazard Description

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Substance Banding Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Banding Code

### Description
The occupational exposure band assigned, once assigned.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Banding Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Substance Transport Code

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Transport Code

### Description
The transport classification, once derived.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::Substance Transport Code

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

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
- schemaName: hazardous_material_holdings
- schemaDescription: The hazardous substances the company holds, where and in what quantity, with the hazard data for each. It serves occupational health, dangerous goods transport and physical inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.

### Anchor ID
DigitalProduct::Coco::Hazardous Material Holdings

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Hazardous Material Holdings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
