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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

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
coco_pharma.goods_receipts

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
GoodsReceiptIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptIdentifier

### Description
The receipt.

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
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 1

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::OrderIdentifier

### Description
The purchase order.

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
DataField::Coco::Goods Receipts::Goods Receipt::OrderIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 2

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::SupplierIdentifier

### Description
The supplier.

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
DataField::Coco::Goods Receipts::Goods Receipt::SupplierIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 3

___

## Create Data Field

### Display Name
RawMaterialCode

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::RawMaterialCode

### Description
The material.

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
DataField::Coco::Goods Receipts::Goods Receipt::RawMaterialCode

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 4

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::LotIdentifier

### Description
The supplier's lot.

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
DataField::Coco::Goods Receipts::Goods Receipt::LotIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 5

___

## Create Data Field

### Display Name
GoodsReceiptDate

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptDate

### Description
When received.

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
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptDate

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 6

___

## Create Data Field

### Display Name
GoodsReceiptQuantity

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptQuantity

### Description
The quantity received.

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
DataField::Coco::Goods Receipts::Goods Receipt::GoodsReceiptQuantity

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 7

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::WarehouseCode

### Description
The receiving location.

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
DataField::Coco::Goods Receipts::Goods Receipt::WarehouseCode

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

### Label
field 8

___

## Create Data Field

### Display Name
CertificateIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Goods Receipt::CertificateIdentifier

### Description
The certificate that accompanied the lot.

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
DataField::Coco::Goods Receipts::Goods Receipt::CertificateIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Goods Receipt

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
coco_pharma.goods_receipts

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
GoodsReceiptIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptIdentifier

### Description
The receipt inspected.

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
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Label
field 1

___

## Create Data Field

### Display Name
GoodsReceiptInspectorIdentifier

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectorIdentifier

### Description
Who inspected.

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
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectorIdentifier

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Label
field 2

___

## Create Data Field

### Display Name
GoodsReceiptInspectionDate

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionDate

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
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionDate

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Label
field 3

___

## Create Data Field

### Display Name
GoodsReceiptInspectionStatus

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionStatus

### Description
Accepted, rejected or held.

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
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionStatus

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

### Label
field 4

___

## Create Data Field

### Display Name
GoodsReceiptInspectionNotes

### Qualified Name
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionNotes

### Description
What was found.

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
DataField::Coco::Goods Receipts::Receipt Inspection::GoodsReceiptInspectionNotes

### Data Structure
DataStructure::Coco::Goods Receipts::Receipt Inspection

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
- schemaName: goods_receipts
- schemaDescription: What physically arrived: each lot of material received, checked against the order and the supplier's documentation, and what the inspection found. It is the point at which a supplier's claim becomes the company's record.

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
coco_pharma.material_quarantine_dispositions

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
LotIdentifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotIdentifier

### Description
The lot.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotIdentifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 1

___

## Create Data Field

### Display Name
RawMaterialCode

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::RawMaterialCode

### Description
The material.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::RawMaterialCode

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 2

___

## Create Data Field

### Display Name
GoodsReceiptIdentifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::GoodsReceiptIdentifier

### Description
The receipt that placed it.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::GoodsReceiptIdentifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 3

___

## Create Data Field

### Display Name
LotQuarantineStartTimestamp

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuarantineStartTimestamp

### Description
When quarantine began.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuarantineStartTimestamp

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 4

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::WarehouseCode

### Description
The quarantine location.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::WarehouseCode

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 5

___

## Create Data Field

### Display Name
LotQuantity

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuantity

### Description
The quantity held.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuantity

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 6

___

## Create Data Field

### Display Name
SampleIdentifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::SampleIdentifier

### Description
The sample sent for incoming testing.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::SampleIdentifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

### Label
field 7

___

## Create Data Field

### Display Name
LotQuarantineStatus

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuarantineStatus

### Description
Held, released or rejected.

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
DataField::Coco::Material Quarantine Dispositions::Quarantine Record::LotQuarantineStatus

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Quarantine Record

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
coco_pharma.material_quarantine_dispositions

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
LotIdentifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotIdentifier

### Description
The lot.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotIdentifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Label
field 1

___

## Create Data Field

### Display Name
LotDispositionStatus

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotDispositionStatus

### Description
Released for use or rejected.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotDispositionStatus

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Label
field 2

___

## Create Data Field

### Display Name
LotDispositionTimestamp

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotDispositionTimestamp

### Description
When decided.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotDispositionTimestamp

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Label
field 3

___

## Create Data Field

### Display Name
TestResultIdentifier

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::TestResultIdentifier

### Description
The laboratory result the decision rests on.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::TestResultIdentifier

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Label
field 4

___

## Create Data Field

### Display Name
LotExpiryDate

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotExpiryDate

### Description
The expiry assigned to the released lot.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotExpiryDate

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

### Label
field 5

___

## Create Data Field

### Display Name
LotReleasedQuantity

### Qualified Name
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotReleasedQuantity

### Description
The quantity released.

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
DataField::Coco::Material Quarantine Dispositions::Release Disposition::LotReleasedQuantity

### Data Structure
DataStructure::Coco::Material Quarantine Dispositions::Release Disposition

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
- schemaName: material_quarantine_dispositions
- schemaDescription: Each lot held in quarantine, the tests requested for it, and the disposition that released it for use or rejected it. It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.

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
coco_pharma.goods_inventory_stock

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
ProductCode

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::ProductCode

### Description
The material or product.

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
DataField::Coco::Goods Inventory Stock::Stock Position::ProductCode

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 1

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::WarehouseCode

### Description
The location.

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
DataField::Coco::Goods Inventory Stock::Stock Position::WarehouseCode

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 2

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::LotIdentifier

### Description
The lot, where stock is lot-tracked.

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
DataField::Coco::Goods Inventory Stock::Stock Position::LotIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 3

___

## Create Data Field

### Display Name
StockLevel

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::StockLevel

### Description
Quantity on hand.

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
DataField::Coco::Goods Inventory Stock::Stock Position::StockLevel

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 4

___

## Create Data Field

### Display Name
StockMinimumLevel

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::StockMinimumLevel

### Description
The reorder level.

### Data Type
int

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
DataField::Coco::Goods Inventory Stock::Stock Position::StockMinimumLevel

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 5

___

## Create Data Field

### Display Name
StockMaximumLevel

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::StockMaximumLevel

### Description
The maximum holding.

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
DataField::Coco::Goods Inventory Stock::Stock Position::StockMaximumLevel

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

### Label
field 6

___

## Create Data Field

### Display Name
StockCurrentTimestamp

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Position::StockCurrentTimestamp

### Description
When the position was last updated.

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
DataField::Coco::Goods Inventory Stock::Stock Position::StockCurrentTimestamp

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Position

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
coco_pharma.goods_inventory_stock

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
StockMovementIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementIdentifier

### Description
The movement.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::ProductCode

### Description
The material or product.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::ProductCode

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 2

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::LotIdentifier

### Description
The lot.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::LotIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 3

___

## Create Data Field

### Display Name
StockMovementType

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementType

### Description
Receipt, issue, transfer, adjustment or shipment.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementType

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 4

___

## Create Data Field

### Display Name
StockMovementQuantity

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementQuantity

### Description
The quantity moved.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementQuantity

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 5

___

## Create Data Field

### Display Name
StockMovementTimestamp

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementTimestamp

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
DataField::Coco::Goods Inventory Stock::Stock Movement::StockMovementTimestamp

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

### Label
field 6

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Goods Inventory Stock::Stock Movement::WarehouseCode

### Description
The location affected.

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
DataField::Coco::Goods Inventory Stock::Stock Movement::WarehouseCode

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Stock Movement

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
coco_pharma.goods_inventory_stock

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
StockMovementIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::StockMovementIdentifier

### Description
The issue movement.

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
DataField::Coco::Goods Inventory Stock::Material Issue::StockMovementIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Label
field 1

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::BatchIdentifier

### Description
The batch the material was issued to.

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
DataField::Coco::Goods Inventory Stock::Material Issue::BatchIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Label
field 2

___

## Create Data Field

### Display Name
RawMaterialCode

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::RawMaterialCode

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
DataField::Coco::Goods Inventory Stock::Material Issue::RawMaterialCode

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Label
field 3

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::LotIdentifier

### Description
The lot issued.

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
DataField::Coco::Goods Inventory Stock::Material Issue::LotIdentifier

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Label
field 4

___

## Create Data Field

### Display Name
RawMaterialIssuedQuantity

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::RawMaterialIssuedQuantity

### Description
The quantity issued.

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
DataField::Coco::Goods Inventory Stock::Material Issue::RawMaterialIssuedQuantity

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

### Label
field 5

___

## Create Data Field

### Display Name
LotQuarantineStatus

### Qualified Name
DataField::Coco::Goods Inventory Stock::Material Issue::LotQuarantineStatus

### Description
The lot's quarantine status at issue.

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
DataField::Coco::Goods Inventory Stock::Material Issue::LotQuarantineStatus

### Data Structure
DataStructure::Coco::Goods Inventory Stock::Material Issue

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
- schemaName: goods_inventory_stock
- schemaDescription: The stock of materials and finished goods at every location: the current position, the movements that produced it, and the issues of material to manufacturing with their quarantine status. It also carries serialised finished goods once they are commissioned.

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
coco_pharma.hazardous_material_holdings

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
SubstanceCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceCode

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Label
field 1

___

## Create Data Field

### Display Name
WarehouseCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::WarehouseCode

### Description
The location.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::WarehouseCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Label
field 2

___

## Create Data Field

### Display Name
SubstanceQuantity

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceQuantity

### Description
The quantity held.

### Data Type
float

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceQuantity

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Label
field 3

___

## Create Data Field

### Display Name
SubstanceUnit

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceUnit

### Description
The unit of the quantity.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceUnit

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Label
field 4

___

## Create Data Field

### Display Name
SubstanceFormDescription

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceFormDescription

### Description
The physical form held, for example powder or solution.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceFormDescription

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

### Label
field 5

___

## Create Data Field

### Display Name
SubstanceCurrentTimestamp

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceCurrentTimestamp

### Description
When the holding was last updated.

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
DataField::Coco::Hazardous Material Holdings::Substance Holding::SubstanceCurrentTimestamp

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Holding

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
coco_pharma.hazardous_material_holdings

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
SubstanceCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceCode

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Label
field 1

___

## Create Data Field

### Display Name
SubstanceName

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceName

### Description
The substance's name.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceName

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Label
field 2

___

## Create Data Field

### Display Name
SubstanceHazardCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceHazardCode

### Description
The hazard classification.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceHazardCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Label
field 3

___

## Create Data Field

### Display Name
SubstanceHazardDescription

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceHazardDescription

### Description
The hazards the substance presents.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceHazardDescription

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Label
field 4

___

## Create Data Field

### Display Name
SubstanceBandingCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceBandingCode

### Description
The occupational exposure band assigned, once assigned.

### Data Type
string

### Position
5

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceBandingCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

### Label
field 5

___

## Create Data Field

### Display Name
SubstanceTransportCode

### Qualified Name
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceTransportCode

### Description
The transport classification, once derived.

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
DataField::Coco::Hazardous Material Holdings::Substance Hazard Data::SubstanceTransportCode

### Data Structure
DataStructure::Coco::Hazardous Material Holdings::Substance Hazard Data

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
- schemaName: hazardous_material_holdings
- schemaDescription: The hazardous substances the company holds, where and in what quantity, with the hazard data for each. It serves occupational health, dangerous goods transport and physical inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.

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
