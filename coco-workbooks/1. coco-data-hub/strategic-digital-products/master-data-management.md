# Master Data Management Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 3 digital products owned by the Master Data Management business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

The master data no single business function owns: the product master, the change notifications that keep every copy of it honest, and the open metadata catalogue that describes the estate the copies live in.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Product Master Data | `CocoPharma::SolutionComponent::ProductMasterRegister` | Master Data | Product Definition, Pack Configuration, Handling Requirement, Authorised Market Assignment |
| Product Change Notifications | `CocoPharma::SolutionComponent::ProductDataDistribution` | Event Stream | Product Change, Distribution Receipt |
| Open Metadata Catalogue Holdings | `SolutionComponent::Egeria Open Metadata and Governance::V1.0` | Reference Data | Catalogued Asset |

For every product this file:

1. creates the **digital product** and adds it to the `Master Data Management` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

3 products, 7 data structures, 41 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret master-data-management.md
```

---

# Product Master Data

*Solution component:* `CocoPharma::SolutionComponent::ProductMasterRegister`  
*Category:* Master Data

The authoritative definition of every Coco Pharmaceuticals product: its identity, composition, presentations and pack configurations, the conditions it must be stored and shipped under, and the markets it is authorised for.  Manufacturing, serialisation, distribution, sales and finance all read it and none of them own it.

## Create Digital Product

### Display Name
Product Master Data

### Product Name
Product Master Data

### Qualified Name
DigitalProduct::Coco::Product Master Data

### Description
The authoritative definition of every Coco Pharmaceuticals product: its identity, composition, presentations and pack configurations, the conditions it must be stored and shipped under, and the markets it is authorised for.  Manufacturing, serialisation, distribution, sales and finance all read it and none of them own it.

### Purpose
Gives every consuming system one definition of a product to work from, so that an inconsistency is corrected here rather than discovered somewhere else.

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
CollectionFolder::Coco::Strategic Digital Products::Master Data Management

### Element Id
DigitalProduct::Coco::Product Master Data

### Membership Rationale
Produced by the Master Data Management group's `ProductMasterRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Product Master Data Data Spec

### Qualified Name
DataSpec::Coco::Product Master Data

### Description
The data structures and fields that make up the Product Master Data digital product.

### Purpose
Describes the data a subscriber to Product Master Data receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Product Master Data

### Collection Id
DataSpec::Coco::Product Master Data

### Label
data specification

___

## Create Data Structure

### Display Name
Product Definition

### Qualified Name
DataStructure::Coco::Product Master Data::Product Definition

### Description
One row per product, the attributes that identify it and describe what it is.

### Namespace Path
coco_data_hub.product_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Master Data

### Element Id
DataStructure::Coco::Product Master Data::Product Definition

### Membership Rationale
The Product Definition structure is part of the Product Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Code

### Description
The company's unique code for the product.

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
DataField::Coco::Product Master Data::Product Definition::Product Code

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Product Name

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Name

### Description
The product's name as it appears on the label.

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
DataField::Coco::Product Master Data::Product Definition::Product Name

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Description

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Description

### Description
What the product is and what it treats.

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
DataField::Coco::Product Master Data::Product Definition::Product Description

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Type

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Type

### Description
Whether the product is a standard, personalised or investigational treatment.

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
DataField::Coco::Product Master Data::Product Definition::Product Type

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Active Ingredient Name

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Active Ingredient Name

### Description
The active ingredient responsible for the therapeutic effect.

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
DataField::Coco::Product Master Data::Product Definition::Active Ingredient Name

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Product Strength

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Strength

### Description
The concentration or potency of the active ingredient.

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
DataField::Coco::Product Master Data::Product Definition::Product Strength

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Product Current Status

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Current Status

### Description
Whether the product is in development, marketed, suspended or withdrawn.

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
DataField::Coco::Product Master Data::Product Definition::Product Current Status

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Product Current Version

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::Product Current Version

### Description
The version of the product definition consuming systems should hold.

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
DataField::Coco::Product Master Data::Product Definition::Product Current Version

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Pack Configuration

### Qualified Name
DataStructure::Coco::Product Master Data::Pack Configuration

### Description
One row per saleable presentation of a product, the unit that carries a serial number.

### Namespace Path
coco_data_hub.product_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Master Data

### Element Id
DataStructure::Coco::Product Master Data::Pack Configuration

### Membership Rationale
The Pack Configuration structure is part of the Product Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Code

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::Pack Code

### Description
The GTIN or company code of the pack presentation.

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
DataField::Coco::Product Master Data::Pack Configuration::Pack Code

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

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
DataField::Coco::Product Master Data::Pack Configuration::Product Code

### Description
The product the pack contains.

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
DataField::Coco::Product Master Data::Pack Configuration::Product Code

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Pack Description

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::Pack Description

### Description
The presentation, for example thirty tablets in a blister pack.

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
DataField::Coco::Product Master Data::Pack Configuration::Pack Description

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Pack Quantity

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::Pack Quantity

### Description
The number of units of the product in the pack.

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
DataField::Coco::Product Master Data::Pack Configuration::Pack Quantity

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Pack Destination Code

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::Pack Destination Code

### Description
The destination market the pack presentation is configured for.

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
DataField::Coco::Product Master Data::Pack Configuration::Pack Destination Code

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Pack Serialised Flag

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::Pack Serialised Flag

### Description
Whether packs of this presentation must carry a serial number.

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
DataField::Coco::Product Master Data::Pack Configuration::Pack Serialised Flag

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Handling Requirement

### Qualified Name
DataStructure::Coco::Product Master Data::Handling Requirement

### Description
One row per product, the storage and transport conditions it must be kept within.

### Namespace Path
coco_data_hub.product_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Master Data

### Element Id
DataStructure::Coco::Product Master Data::Handling Requirement

### Membership Rationale
The Handling Requirement structure is part of the Product Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Code

### Description
The product the requirement applies to.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Code

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Product Storage Minimum Temperature

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Storage Minimum Temperature

### Description
The lowest temperature the product may be stored at, in degrees Celsius.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Storage Minimum Temperature

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Storage Maximum Temperature

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Storage Maximum Temperature

### Description
The highest temperature the product may be stored at, in degrees Celsius.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Storage Maximum Temperature

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Hazard Code

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Hazard Code

### Description
The hazard classification of the product for transport, if any.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Hazard Code

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Product Packaging Description

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Packaging Description

### Description
The packaging required for transport.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Packaging Description

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Product Expiry Duration

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::Product Expiry Duration

### Description
The shelf life of the product from manufacture, in days.

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
DataField::Coco::Product Master Data::Handling Requirement::Product Expiry Duration

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Authorised Market Assignment

### Qualified Name
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Description
One row per product per market it may be placed on.

### Namespace Path
coco_data_hub.product_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Master Data

### Element Id
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Membership Rationale
The Authorised Market Assignment structure is part of the Product Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::Product Code

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Product Code

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Market Code

### Description
The market the product is authorised for.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Market Code

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Authorisation Identifier

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation Identifier

### Description
The market authorisation the assignment relies on.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation Identifier

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Authorisation Start Date

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation Start Date

### Description
When the product may first be placed on the market.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation Start Date

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Authorisation End Date

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation End Date

### Description
When the authorisation lapses, if it does.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::Authorisation End Date

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

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
- schemaName: product_master_data
- schemaDescription: The authoritative definition of every Coco Pharmaceuticals product: its identity, composition, presentations and pack configurations, the conditions it must be stored and shipped under, and the markets it is authorised for. Manufacturing, serialisation, distribution, sales and finance all read it and none of them own it.

### Parent ID
DigitalProduct::Coco::Product Master Data

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Product Change Notifications

*Solution component:* `CocoPharma::SolutionComponent::ProductDataDistribution`  
*Category:* Event Stream

Every change published from the product master, and the record of which consuming system has applied it and which has not.  An inconsistent estate is only dangerous while nobody knows which copies are stale.

## Create Digital Product

### Display Name
Product Change Notifications

### Product Name
Product Change Notifications

### Qualified Name
DigitalProduct::Coco::Product Change Notifications

### Description
Every change published from the product master, and the record of which consuming system has applied it and which has not.  An inconsistent estate is only dangerous while nobody knows which copies are stale.

### Purpose
Lets any system holding a copy of the product master prove it is current, and lets the data hub see which are not.

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
CollectionFolder::Coco::Strategic Digital Products::Master Data Management

### Element Id
DigitalProduct::Coco::Product Change Notifications

### Membership Rationale
Produced by the Master Data Management group's `ProductDataDistribution` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Product Change Notifications Data Spec

### Qualified Name
DataSpec::Coco::Product Change Notifications

### Description
The data structures and fields that make up the Product Change Notifications digital product.

### Purpose
Describes the data a subscriber to Product Change Notifications receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Product Change Notifications

### Collection Id
DataSpec::Coco::Product Change Notifications

### Label
data specification

___

## Create Data Structure

### Display Name
Product Change

### Qualified Name
DataStructure::Coco::Product Change Notifications::Product Change

### Description
One row per published change to a product attribute.

### Namespace Path
coco_data_hub.product_change_notifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Change Notifications

### Element Id
DataStructure::Coco::Product Change Notifications::Product Change

### Membership Rationale
The Product Change structure is part of the Product Change Notifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Change Identifier

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::Product Change Identifier

### Description
The unique identifier of the change.

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
DataField::Coco::Product Change Notifications::Product Change::Product Change Identifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

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
DataField::Coco::Product Change Notifications::Product Change::Product Code

### Description
The product changed.

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
DataField::Coco::Product Change Notifications::Product Change::Product Code

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Change Description

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::Product Change Description

### Description
Which attributes changed and to what.

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
DataField::Coco::Product Change Notifications::Product Change::Product Change Description

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Change Start Date

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::Product Change Start Date

### Description
When the change takes effect.

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
DataField::Coco::Product Change Notifications::Product Change::Product Change Start Date

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Product Change Published Timestamp

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::Product Change Published Timestamp

### Description
When the change was published to consumers.

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
DataField::Coco::Product Change Notifications::Product Change::Product Change Published Timestamp

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Structure

### Display Name
Distribution Receipt

### Qualified Name
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Description
One row per change per consuming system, recording whether it has been applied.

### Namespace Path
coco_data_hub.product_change_notifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Change Notifications

### Element Id
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Membership Rationale
The Distribution Receipt structure is part of the Product Change Notifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Change Identifier

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Identifier

### Description
The change distributed.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Identifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::System Identifier

### Description
The consuming system the change was sent to.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::System Identifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Product Change Applied Flag

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Applied Flag

### Description
Whether the system has confirmed the change is applied.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Applied Flag

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Product Change Applied Timestamp

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Applied Timestamp

### Description
When the system confirmed it.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::Product Change Applied Timestamp

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

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
- schemaName: product_change_notifications
- schemaDescription: Every change published from the product master, and the record of which consuming system has applied it and which has not. An inconsistent estate is only dangerous while nobody knows which copies are stale.

### Parent ID
DigitalProduct::Coco::Product Change Notifications

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Open Metadata Catalogue Holdings

*Solution component:* `SolutionComponent::Egeria Open Metadata and Governance::V1.0`  
*Category:* Reference Data

What the open metadata catalogue knows about the estate: the assets it has catalogued, their classifications and owners, and the indicators that an asset holds personal data.  It is the starting point for personal data discovery and for setting retention periods, because it describes what the company actually holds rather than what it believes it holds.

## Create Digital Product

### Display Name
Open Metadata Catalogue Holdings

### Product Name
Open Metadata Catalogue Holdings

### Qualified Name
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Description
What the open metadata catalogue knows about the estate: the assets it has catalogued, their classifications and owners, and the indicators that an asset holds personal data.  It is the starting point for personal data discovery and for setting retention periods, because it describes what the company actually holds rather than what it believes it holds.

### Purpose
Gives the privacy and retention processes an inventory of assets to work from that is maintained by the systems themselves.

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
CollectionFolder::Coco::Strategic Digital Products::Master Data Management

### Element Id
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Membership Rationale
Produced by the Master Data Management group's `Egeria Open Metadata and Governance` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Open Metadata Catalogue Holdings Data Spec

### Qualified Name
DataSpec::Coco::Open Metadata Catalogue Holdings

### Description
The data structures and fields that make up the Open Metadata Catalogue Holdings digital product.

### Purpose
Describes the data a subscriber to Open Metadata Catalogue Holdings receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Collection Id
DataSpec::Coco::Open Metadata Catalogue Holdings

### Label
data specification

___

## Create Data Structure

### Display Name
Catalogued Asset

### Qualified Name
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Description
One row per asset in the catalogue.

### Namespace Path
coco_data_hub.open_metadata_catalogue_holdings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Open Metadata Catalogue Holdings

### Element Id
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Membership Rationale
The Catalogued Asset structure is part of the Open Metadata Catalogue Holdings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Asset Identifier

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Identifier

### Description
The catalogue's unique identifier for the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Identifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Asset Name

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Name

### Description
The asset's display name.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Name

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Asset Type

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Type

### Description
The open metadata type of the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Type

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::System Identifier

### Description
The system that hosts the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::System Identifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Asset Owner Identifier

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Owner Identifier

### Description
The person or team accountable for the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Owner Identifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Asset Personal Data Flag

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Personal Data Flag

### Description
Whether the asset is classified as holding personal data.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Personal Data Flag

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Asset Confidentiality Level

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Confidentiality Level

### Description
The confidentiality classification of the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::Asset Confidentiality Level

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

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
- schemaName: open_metadata_catalogue_holdings
- schemaDescription: What the open metadata catalogue knows about the estate: the assets it has catalogued, their classifications and owners, and the indicators that an asset holds personal data. It is the starting point for personal data discovery and for setting retention periods, because it describes what the company actually holds rather than what it believes it holds.

### Parent ID
DigitalProduct::Coco::Open Metadata Catalogue Holdings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
