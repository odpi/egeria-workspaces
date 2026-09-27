# Research Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 2 digital products owned by the Research business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of drug development that other chains consume: new product definitions and the certification of hospitals as trial sites.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| New Product Definitions | `CocoPharma::SolutionComponent::Research` | Master Data | Candidate Product Definition, Product Presentation, Product Specification |
| Hospital Certifications | `SolutionComponent::Certify Hospital::V1.0` | Evidence Record | Hospital Certification, Site Staff Training Evidence |

For every product this file:

1. creates the **digital product** and adds it to the `Research` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

2 products, 5 data structures, 27 data fields.  Product Code is one data field shared by all three New Product Definitions structures: it identifies a row of Candidate Product Definition and Product Specification, and refers to the product in Product Presentation.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret research.md
```

---

# New Product Definitions

*Solution component:* `CocoPharma::SolutionComponent::Research`  
*Category:* Master Data

The definition of a new product as it leaves development: its composition, the presentations it will be supplied in and the specification it must meet.  It is the source the product master is created from.

## Create Digital Product

### Display Name
New Product Definitions

### Product Name
New Product Definitions

### Qualified Name
DigitalProduct::Coco::Product Definitions

### Description
The definition of a new product as it leaves development: its composition, the presentations it will be supplied in and the specification it must meet.  It is the source the product master is created from.

### Purpose
Hands a completed development over to the product master as data rather than as a document.

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
CollectionFolder::Coco::Strategic Digital Products::Research

### Element Id
DigitalProduct::Coco::Product Definitions

### Membership Rationale
Produced by the Research group's `Research` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
New Product Definitions Data Spec

### Qualified Name
DataSpec::Coco::Product Definitions

### Description
The data structures and fields that make up the New Product Definitions digital product.

### Purpose
Describes the data a subscriber to New Product Definitions receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Product Definitions

### Collection Id
DataSpec::Coco::Product Definitions

### Label
data specification

___

## Create Data Structure

### Display Name
Candidate Product Definition

### Qualified Name
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Description
One row per product candidate handed over from development.

### Namespace Path
coco_data_hub.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Definitions

### Element Id
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Membership Rationale
The Candidate Product Definition structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Product Definitions::Product Code

### Description
The product code assigned on handover.

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
DataField::Coco::Product Definitions::Product Code

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Candidate Identifier

### Qualified Name
DataField::Coco::Product Definitions::Candidate Identifier

### Description
The development identifier of the candidate.

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
DataField::Coco::Product Definitions::Candidate Identifier

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Name

### Qualified Name
DataField::Coco::Product Definitions::Product Name

### Description
The proposed product name.

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
DataField::Coco::Product Definitions::Product Name

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Formulation Identifier

### Qualified Name
DataField::Coco::Product Definitions::Formulation Identifier

### Description
The formulation developed.

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
DataField::Coco::Product Definitions::Formulation Identifier

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

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
DataField::Coco::Product Definitions::Active Ingredient Name

### Description
The active ingredient.

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
DataField::Coco::Product Definitions::Active Ingredient Name

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

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
DataField::Coco::Product Definitions::Product Strength

### Description
The strength.

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
DataField::Coco::Product Definitions::Product Strength

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Clinical Trial Identifier

### Qualified Name
DataField::Coco::Product Definitions::Clinical Trial Identifier

### Description
The trial that supports the product.

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
DataField::Coco::Product Definitions::Clinical Trial Identifier

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Candidate Handover Date

### Qualified Name
DataField::Coco::Product Definitions::Candidate Handover Date

### Description
When development handed the definition over.

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
DataField::Coco::Product Definitions::Candidate Handover Date

### Data Structure
DataStructure::Coco::Product Definitions::Candidate Product Definition

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Product Presentation

### Qualified Name
DataStructure::Coco::Product Definitions::Product Presentation

### Description
One row per presentation the product will be supplied in.

### Namespace Path
coco_data_hub.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Definitions

### Element Id
DataStructure::Coco::Product Definitions::Product Presentation

### Membership Rationale
The Product Presentation structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Pack Code

### Qualified Name
DataField::Coco::Product Definitions::Pack Code

### Description
The presentation's pack code.

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
DataField::Coco::Product Definitions::Pack Code

### Data Structure
DataStructure::Coco::Product Definitions::Product Presentation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Definitions::Product Code

### Data Structure
DataStructure::Coco::Product Definitions::Product Presentation

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
DataField::Coco::Product Definitions::Pack Description

### Description
The presentation.

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
DataField::Coco::Product Definitions::Pack Description

### Data Structure
DataStructure::Coco::Product Definitions::Product Presentation

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
DataField::Coco::Product Definitions::Pack Quantity

### Description
Units per pack.

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
DataField::Coco::Product Definitions::Pack Quantity

### Data Structure
DataStructure::Coco::Product Definitions::Product Presentation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Structure

### Display Name
Product Specification

### Qualified Name
DataStructure::Coco::Product Definitions::Product Specification

### Description
One row per specification limit the product must meet on release.

### Namespace Path
coco_data_hub.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Product Definitions

### Element Id
DataStructure::Coco::Product Definitions::Product Specification

### Membership Rationale
The Product Specification structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Product Definitions::Product Code

### Data Structure
DataStructure::Coco::Product Definitions::Product Specification

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Test Code

### Qualified Name
DataField::Coco::Product Definitions::Test Code

### Description
The release test.

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
DataField::Coco::Product Definitions::Test Code

### Data Structure
DataStructure::Coco::Product Definitions::Product Specification

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Specification Minimum Value

### Qualified Name
DataField::Coco::Product Definitions::Specification Minimum Value

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
DataField::Coco::Product Definitions::Specification Minimum Value

### Data Structure
DataStructure::Coco::Product Definitions::Product Specification

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Specification Maximum Value

### Qualified Name
DataField::Coco::Product Definitions::Specification Maximum Value

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
DataField::Coco::Product Definitions::Specification Maximum Value

### Data Structure
DataStructure::Coco::Product Definitions::Product Specification

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
DataField::Coco::Product Definitions::Test Unit

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
DataField::Coco::Product Definitions::Test Unit

### Data Structure
DataStructure::Coco::Product Definitions::Product Specification

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
- schemaName: new_product_definitions
- schemaDescription: The definition of a new product as it leaves development: its composition, the presentations it will be supplied in and the specification it must meet. It is the source the product master is created from.

### Parent ID
DigitalProduct::Coco::Product Definitions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Hospital Certifications

*Solution component:* `SolutionComponent::Certify Hospital::V1.0`  
*Category:* Evidence Record

The certification of hospitals as clinical trial sites, including the evidence that site staff were trained on the protocol before they worked to it.  Competency data is read here as compliance evidence.

## Create Digital Product

### Display Name
Hospital Certifications

### Product Name
Hospital Certifications

### Qualified Name
DigitalProduct::Coco::Hospital Certifications

### Description
The certification of hospitals as clinical trial sites, including the evidence that site staff were trained on the protocol before they worked to it.  Competency data is read here as compliance evidence.

### Purpose
Records which sites may treat trial participants, and on what training evidence.

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
CollectionFolder::Coco::Strategic Digital Products::Research

### Element Id
DigitalProduct::Coco::Hospital Certifications

### Membership Rationale
Produced by the Research group's `Certify Hospital` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Hospital Certifications Data Spec

### Qualified Name
DataSpec::Coco::Hospital Certifications

### Description
The data structures and fields that make up the Hospital Certifications digital product.

### Purpose
Describes the data a subscriber to Hospital Certifications receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Hospital Certifications

### Collection Id
DataSpec::Coco::Hospital Certifications

### Label
data specification

___

## Create Data Structure

### Display Name
Hospital Certification

### Qualified Name
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Description
One row per hospital certified for a trial.

### Namespace Path
coco_data_hub.hospital_certifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Hospital Certifications

### Element Id
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Membership Rationale
The Hospital Certification structure is part of the Hospital Certifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Hospital Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Identifier

### Description
The hospital.

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
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Clinical Trial Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Clinical Trial Identifier

### Description
The trial.

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
DataField::Coco::Hospital Certifications::Hospital Certification::Clinical Trial Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Hospital Certification Date

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification Date

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
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification Date

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Hospital Certification End Date

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification End Date

### Description
When the certification lapses.

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
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification End Date

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Hospital Certification Status

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification Status

### Description
Certified, suspended or withdrawn.

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
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certification Status

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Hospital Certifier Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certifier Identifier

### Description
Who certified the site.

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
DataField::Coco::Hospital Certifications::Hospital Certification::Hospital Certifier Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Site Staff Training Evidence

### Qualified Name
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Description
One row per site staff member per protocol training completed.

### Namespace Path
coco_data_hub.hospital_certifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Hospital Certifications

### Element Id
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Membership Rationale
The Site Staff Training Evidence structure is part of the Hospital Certifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Hospital Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Hospital Identifier

### Description
The site.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Hospital Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Clinical Trial Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Clinical Trial Identifier

### Description
The trial.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Clinical Trial Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Clinician Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Clinician Identifier

### Description
The staff member.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Clinician Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Protocol Identifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Protocol Identifier

### Description
The protocol trained on.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Protocol Identifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Position
4

### Coverage Category
IDENTIFIER

### Label
field 4

___

## Create Data Field

### Display Name
Training Completed Date

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Training Completed Date

### Description
When training was completed.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Training Completed Date

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Training Expiry Date

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Training Expiry Date

### Description
When the training lapses.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::Training Expiry Date

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

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
- schemaName: hospital_certifications
- schemaDescription: The certification of hospitals as clinical trial sites, including the evidence that site staff were trained on the protocol before they worked to it. Competency data is read here as compliance evidence.

### Parent ID
DigitalProduct::Coco::Hospital Certifications

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
