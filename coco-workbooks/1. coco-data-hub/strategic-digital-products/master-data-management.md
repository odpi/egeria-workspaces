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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

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
coco_pharma.product_master_data

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
ProductCode

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductCode

### Description
The company's unique code for the product.

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
DataField::Coco::Product Master Data::Product Definition::ProductCode

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 1

___

## Create Data Field

### Display Name
ProductName

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductName

### Description
The product's name as it appears on the label.

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
DataField::Coco::Product Master Data::Product Definition::ProductName

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 2

___

## Create Data Field

### Display Name
ProductDescription

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductDescription

### Description
What the product is and what it treats.

### Data Type
string

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
DataField::Coco::Product Master Data::Product Definition::ProductDescription

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 3

___

## Create Data Field

### Display Name
ProductType

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductType

### Description
Whether the product is a standard, personalised or investigational treatment.

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
DataField::Coco::Product Master Data::Product Definition::ProductType

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 4

___

## Create Data Field

### Display Name
ActiveIngredientName

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ActiveIngredientName

### Description
The active ingredient responsible for the therapeutic effect.

### Data Type
string

### Position
5

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
DataField::Coco::Product Master Data::Product Definition::ActiveIngredientName

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 5

___

## Create Data Field

### Display Name
ProductStrength

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductStrength

### Description
The concentration or potency of the active ingredient.

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
DataField::Coco::Product Master Data::Product Definition::ProductStrength

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 6

___

## Create Data Field

### Display Name
ProductCurrentStatus

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductCurrentStatus

### Description
Whether the product is in development, marketed, suspended or withdrawn.

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
DataField::Coco::Product Master Data::Product Definition::ProductCurrentStatus

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

### Label
field 7

___

## Create Data Field

### Display Name
ProductCurrentVersion

### Qualified Name
DataField::Coco::Product Master Data::Product Definition::ProductCurrentVersion

### Description
The version of the product definition consuming systems should hold.

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
DataField::Coco::Product Master Data::Product Definition::ProductCurrentVersion

### Data Structure
DataStructure::Coco::Product Master Data::Product Definition

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
coco_pharma.product_master_data

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
PackCode

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::PackCode

### Description
The GTIN or company code of the pack presentation.

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
DataField::Coco::Product Master Data::Pack Configuration::PackCode

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::ProductCode

### Description
The product the pack contains.

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
DataField::Coco::Product Master Data::Pack Configuration::ProductCode

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Label
field 2

___

## Create Data Field

### Display Name
PackDescription

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::PackDescription

### Description
The presentation, for example thirty tablets in a blister pack.

### Data Type
string

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
DataField::Coco::Product Master Data::Pack Configuration::PackDescription

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Label
field 3

___

## Create Data Field

### Display Name
PackQuantity

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::PackQuantity

### Description
The number of units of the product in the pack.

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
DataField::Coco::Product Master Data::Pack Configuration::PackQuantity

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Label
field 4

___

## Create Data Field

### Display Name
PackDestinationCode

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::PackDestinationCode

### Description
The destination market the pack presentation is configured for.

### Data Type
string

### Position
5

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
DataField::Coco::Product Master Data::Pack Configuration::PackDestinationCode

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

### Label
field 5

___

## Create Data Field

### Display Name
PackSerialisedFlag

### Qualified Name
DataField::Coco::Product Master Data::Pack Configuration::PackSerialisedFlag

### Description
Whether packs of this presentation must carry a serial number.

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
DataField::Coco::Product Master Data::Pack Configuration::PackSerialisedFlag

### Data Structure
DataStructure::Coco::Product Master Data::Pack Configuration

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
coco_pharma.product_master_data

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
ProductCode

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductCode

### Description
The product the requirement applies to.

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
DataField::Coco::Product Master Data::Handling Requirement::ProductCode

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Label
field 1

___

## Create Data Field

### Display Name
ProductStorageMinimumTemperature

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductStorageMinimumTemperature

### Description
The lowest temperature the product may be stored at, in degrees Celsius.

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
DataField::Coco::Product Master Data::Handling Requirement::ProductStorageMinimumTemperature

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Label
field 2

___

## Create Data Field

### Display Name
ProductStorageMaximumTemperature

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductStorageMaximumTemperature

### Description
The highest temperature the product may be stored at, in degrees Celsius.

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
DataField::Coco::Product Master Data::Handling Requirement::ProductStorageMaximumTemperature

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Label
field 3

___

## Create Data Field

### Display Name
ProductHazardCode

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductHazardCode

### Description
The hazard classification of the product for transport, if any.

### Data Type
string

### Position
4

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
DataField::Coco::Product Master Data::Handling Requirement::ProductHazardCode

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Label
field 4

___

## Create Data Field

### Display Name
ProductPackagingDescription

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductPackagingDescription

### Description
The packaging required for transport.

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
DataField::Coco::Product Master Data::Handling Requirement::ProductPackagingDescription

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

### Label
field 5

___

## Create Data Field

### Display Name
ProductExpiryDuration

### Qualified Name
DataField::Coco::Product Master Data::Handling Requirement::ProductExpiryDuration

### Description
The shelf life of the product from manufacture, in days.

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
DataField::Coco::Product Master Data::Handling Requirement::ProductExpiryDuration

### Data Structure
DataStructure::Coco::Product Master Data::Handling Requirement

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
coco_pharma.product_master_data

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
ProductCode

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::ProductCode

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
DataField::Coco::Product Master Data::Authorised Market Assignment::ProductCode

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Label
field 1

___

## Create Data Field

### Display Name
MarketCode

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::MarketCode

### Description
The market the product is authorised for.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::MarketCode

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Label
field 2

___

## Create Data Field

### Display Name
AuthorisationIdentifier

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationIdentifier

### Description
The market authorisation the assignment relies on.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationIdentifier

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Label
field 3

___

## Create Data Field

### Display Name
AuthorisationStartDate

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationStartDate

### Description
When the product may first be placed on the market.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationStartDate

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

### Label
field 4

___

## Create Data Field

### Display Name
AuthorisationEndDate

### Qualified Name
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationEndDate

### Description
When the authorisation lapses, if it does.

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
DataField::Coco::Product Master Data::Authorised Market Assignment::AuthorisationEndDate

### Data Structure
DataStructure::Coco::Product Master Data::Authorised Market Assignment

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
coco_pharma.product_change_notifications

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
ProductChangeIdentifier

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::ProductChangeIdentifier

### Description
The unique identifier of the change.

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
DataField::Coco::Product Change Notifications::Product Change::ProductChangeIdentifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::ProductCode

### Description
The product changed.

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
DataField::Coco::Product Change Notifications::Product Change::ProductCode

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Label
field 2

___

## Create Data Field

### Display Name
ProductChangeDescription

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::ProductChangeDescription

### Description
Which attributes changed and to what.

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
DataField::Coco::Product Change Notifications::Product Change::ProductChangeDescription

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Label
field 3

___

## Create Data Field

### Display Name
ProductChangeStartDate

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::ProductChangeStartDate

### Description
When the change takes effect.

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
DataField::Coco::Product Change Notifications::Product Change::ProductChangeStartDate

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

### Label
field 4

___

## Create Data Field

### Display Name
ProductChangePublishedTimestamp

### Qualified Name
DataField::Coco::Product Change Notifications::Product Change::ProductChangePublishedTimestamp

### Description
When the change was published to consumers.

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
DataField::Coco::Product Change Notifications::Product Change::ProductChangePublishedTimestamp

### Data Structure
DataStructure::Coco::Product Change Notifications::Product Change

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
coco_pharma.product_change_notifications

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
ProductChangeIdentifier

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeIdentifier

### Description
The change distributed.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeIdentifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Label
field 1

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::SystemIdentifier

### Description
The consuming system the change was sent to.

### Data Type
string

### Position
2

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
DataField::Coco::Product Change Notifications::Distribution Receipt::SystemIdentifier

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Label
field 2

___

## Create Data Field

### Display Name
ProductChangeAppliedFlag

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeAppliedFlag

### Description
Whether the system has confirmed the change is applied.

### Data Type
boolean

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
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeAppliedFlag

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

### Label
field 3

___

## Create Data Field

### Display Name
ProductChangeAppliedTimestamp

### Qualified Name
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeAppliedTimestamp

### Description
When the system confirmed it.

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
DataField::Coco::Product Change Notifications::Distribution Receipt::ProductChangeAppliedTimestamp

### Data Structure
DataStructure::Coco::Product Change Notifications::Distribution Receipt

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
coco_pharma.open_metadata_catalogue_holdings

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
AssetIdentifier

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetIdentifier

### Description
The catalogue's unique identifier for the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetIdentifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 1

___

## Create Data Field

### Display Name
AssetName

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetName

### Description
The asset's display name.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetName

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 2

___

## Create Data Field

### Display Name
AssetType

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetType

### Description
The open metadata type of the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetType

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 3

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::SystemIdentifier

### Description
The system that hosts the asset.

### Data Type
string

### Position
4

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::SystemIdentifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 4

___

## Create Data Field

### Display Name
AssetOwnerIdentifier

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetOwnerIdentifier

### Description
The person or team accountable for the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetOwnerIdentifier

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 5

___

## Create Data Field

### Display Name
AssetPersonalDataFlag

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetPersonalDataFlag

### Description
Whether the asset is classified as holding personal data.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetPersonalDataFlag

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

### Label
field 6

___

## Create Data Field

### Display Name
AssetConfidentialityLevel

### Qualified Name
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetConfidentialityLevel

### Description
The confidentiality classification of the asset.

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
DataField::Coco::Open Metadata Catalogue Holdings::Catalogued Asset::AssetConfidentialityLevel

### Data Structure
DataStructure::Coco::Open Metadata Catalogue Holdings::Catalogued Asset

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
