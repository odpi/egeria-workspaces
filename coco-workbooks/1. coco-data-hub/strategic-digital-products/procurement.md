# Procurement Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 5 digital products owned by the Procurement business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of the sourcing function: supplier master data, onboarding cases, third party screening results, supplier certificates, and the purchase orders and receipts that payment is matched against.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Supplier Master Data | `CocoPharma::SolutionComponent::SupplierMasterRegister` | Master Data | Supplier, Supplier Risk Status, Supplier Payment Details |
| Third Party Onboarding Cases | `CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow` | Transactional Record | Onboarding Case, Screening Request |
| Third Party Screening Results | `CocoPharma::SolutionComponent::SanctionsAndScreeningService` | Reference Data | Screening Result, Screening Match |
| Supplier Material Certificates | `CocoPharma::SolutionComponent::SupplierMaterialCertificates` | Evidence Record | Certificate Of Analysis, Certificate Test Result |
| Purchase Orders And Receipts | `CocoPharma::SolutionComponent::Procurement` | Transactional Record | Purchase Order, Goods Receipt Confirmation |

For every product this file:

1. creates the **digital product** and adds it to the `Procurement` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

5 products, 11 data structures, 68 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret procurement.md
```

---

# Supplier Master Data

*Solution component:* `CocoPharma::SolutionComponent::SupplierMasterRegister`  
*Category:* Master Data

The authoritative record of every third party the company transacts with: its identity, its screening status and risk rating, and the payment details it is paid to.  The supplier fraud was possible because this record was not authoritative; making it so is the control.

## Create Digital Product

### Display Name
Supplier Master Data

### Product Name
Supplier Master Data

### Qualified Name
DigitalProduct::Coco::Supplier Master Data

### Description
The authoritative record of every third party the company transacts with: its identity, its screening status and risk rating, and the payment details it is paid to.  The supplier fraud was possible because this record was not authoritative; making it so is the control.

### Purpose
Gives payment processing, goods receipt and disclosure one trusted record of who a supplier is, whether it has been screened and where it is paid.

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
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Element Id
DigitalProduct::Coco::Supplier Master Data

### Membership Rationale
Produced by the Procurement group's `SupplierMasterRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Supplier Master Data Data Spec

### Qualified Name
DataSpec::Coco::Supplier Master Data

### Description
The data structures and fields that make up the Supplier Master Data digital product.

### Purpose
Describes the data a subscriber to Supplier Master Data receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Supplier Master Data

### Collection Id
DataSpec::Coco::Supplier Master Data

### Label
data specification

___

## Create Data Structure

### Display Name
Supplier

### Qualified Name
DataStructure::Coco::Supplier Master Data::Supplier

### Description
One row per approved third party.

### Namespace Path
coco_data_hub.supplier_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Master Data

### Element Id
DataStructure::Coco::Supplier Master Data::Supplier

### Membership Rationale
The Supplier structure is part of the Supplier Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Identifier

### Description
The company's unique identifier for the supplier.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Name

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Name

### Description
The supplier's legal name.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Name

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Supplier Type

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Type

### Description
Material supplier, service provider, healthcare organisation or other.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Type

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Supplier Country

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Country

### Description
The country of incorporation.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Country

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Supplier Approved Flag

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Approved Flag

### Description
Whether the supplier has passed onboarding.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Approved Flag

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Supplier Approved Date

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Approved Date

### Description
When approval was granted.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Approved Date

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Supplier Current Status

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::Supplier Current Status

### Description
Active, suspended or closed.

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
DataField::Coco::Supplier Master Data::Supplier::Supplier Current Status

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Supplier Risk Status

### Qualified Name
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Description
One row per supplier, its current screening and risk position.

### Namespace Path
coco_data_hub.supplier_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Master Data

### Element Id
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Membership Rationale
The Supplier Risk Status structure is part of the Supplier Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Identifier

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Screened Status

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Screened Status

### Description
Clear, match under review, or blocked.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Screened Status

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Supplier Screened Date

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Screened Date

### Description
When the supplier was last screened.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Screened Date

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Supplier Rating

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Rating

### Description
The assessed risk rating.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Supplier Rating

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Screening Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Screening Identifier

### Description
The screening result the status rests on.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Screening Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Anomaly Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::Anomaly Identifier

### Description
An open concern raised by transaction monitoring, if any.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::Anomaly Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Supplier Payment Details

### Qualified Name
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Description
One row per supplier, the verified bank details it is paid to.

### Namespace Path
coco_data_hub.supplier_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Master Data

### Element Id
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Membership Rationale
The Supplier Payment Details structure is part of the Supplier Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Supplier Identifier

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Bank Account Current Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Current Identifier

### Description
The bank account, masked.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Current Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Bank Account Provider Name

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Provider Name

### Description
The bank.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Provider Name

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Bank Account Country

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Country

### Description
The country of the account.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Bank Account Country

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Payment Detail Change Identifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Payment Detail Change Identifier

### Description
The verified change that set these details.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Payment Detail Change Identifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Payment Detail Verified Date

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::Payment Detail Verified Date

### Description
When the details were last independently verified.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::Payment Detail Verified Date

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

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
- schemaName: supplier_master_data
- schemaDescription: The authoritative record of every third party the company transacts with: its identity, its screening status and risk rating, and the payment details it is paid to. The supplier fraud was possible because this record was not authoritative; making it so is the control.

### Anchor ID
DigitalProduct::Coco::Supplier Master Data

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Supplier Master Data

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Third Party Onboarding Cases

*Solution component:* `CocoPharma::SolutionComponent::ThirdPartyOnboardingWorkflow`  
*Category:* Transactional Record

Every proposed third party driven through screening, risk assessment and approval to the creation of a supplier record.  It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.

## Create Digital Product

### Display Name
Third Party Onboarding Cases

### Product Name
Third Party Onboarding Cases

### Qualified Name
DigitalProduct::Coco::Third Party Onboarding Cases

### Description
Every proposed third party driven through screening, risk assessment and approval to the creation of a supplier record.  It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.

### Purpose
Evidences that each supplier was screened and risk-assessed before it could be paid.

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
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Element Id
DigitalProduct::Coco::Third Party Onboarding Cases

### Membership Rationale
Produced by the Procurement group's `ThirdPartyOnboardingWorkflow` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Third Party Onboarding Cases Data Spec

### Qualified Name
DataSpec::Coco::Third Party Onboarding Cases

### Description
The data structures and fields that make up the Third Party Onboarding Cases digital product.

### Purpose
Describes the data a subscriber to Third Party Onboarding Cases receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Third Party Onboarding Cases

### Collection Id
DataSpec::Coco::Third Party Onboarding Cases

### Label
data specification

___

## Create Data Structure

### Display Name
Onboarding Case

### Qualified Name
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Description
One row per third party proposed for onboarding.

### Namespace Path
coco_data_hub.third_party_onboarding_cases

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Third Party Onboarding Cases

### Element Id
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Membership Rationale
The Onboarding Case structure is part of the Third Party Onboarding Cases data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Onboarding Case Identifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Identifier

### Description
The unique identifier of the case.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Identifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Third Party Name

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Name

### Description
The proposed third party's legal name.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Name

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Third Party Country

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Country

### Description
Its country of incorporation.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Country

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Third Party Owner Description

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Owner Description

### Description
Its beneficial ownership as declared.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Third Party Owner Description

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Onboarding Case Requester Identifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Requester Identifier

### Description
Who proposed the third party.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Requester Identifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Onboarding Case Start Date

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Start Date

### Description
When the case was opened.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Start Date

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Onboarding Case Current Status

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Current Status

### Description
Screening, risk assessment, approved, rejected.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Onboarding Case Current Status

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Supplier Identifier

### Description
The supplier record created on approval.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::Supplier Identifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Screening Request

### Qualified Name
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Description
One row per screening submitted to the external service for a case.

### Namespace Path
coco_data_hub.third_party_onboarding_cases

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Third Party Onboarding Cases

### Element Id
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Membership Rationale
The Screening Request structure is part of the Third Party Onboarding Cases data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Screening Identifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Identifier

### Description
The screening request.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Identifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Onboarding Case Identifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::Onboarding Case Identifier

### Description
The case.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::Onboarding Case Identifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Screening Requested Timestamp

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Requested Timestamp

### Description
When it was submitted.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Requested Timestamp

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Screening Type

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Type

### Description
Sanctions, politically exposed persons, adverse media, or all.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::Screening Type

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Supplier Rating

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::Supplier Rating

### Description
The risk rating assigned once the result was assessed.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::Supplier Rating

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

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
- schemaName: third_party_onboarding_cases
- schemaDescription: Every proposed third party driven through screening, risk assessment and approval to the creation of a supplier record. It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.

### Anchor ID
DigitalProduct::Coco::Third Party Onboarding Cases

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Third Party Onboarding Cases

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Third Party Screening Results

*Solution component:* `CocoPharma::SolutionComponent::SanctionsAndScreeningService`  
*Category:* Reference Data

The answers returned by the external screening service: matches against sanctions, politically exposed person and adverse media lists, with the risk indicators and the date each was given.  Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

## Create Digital Product

### Display Name
Third Party Screening Results

### Product Name
Third Party Screening Results

### Qualified Name
DigitalProduct::Coco::Third Party Screening Results

### Description
The answers returned by the external screening service: matches against sanctions, politically exposed person and adverse media lists, with the risk indicators and the date each was given.  Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

### Purpose
Makes the external screening evidence part of the company's own record, dated, so that a stale result is visible.

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
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Element Id
DigitalProduct::Coco::Third Party Screening Results

### Membership Rationale
Produced by the Procurement group's `SanctionsAndScreeningService` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Third Party Screening Results Data Spec

### Qualified Name
DataSpec::Coco::Third Party Screening Results

### Description
The data structures and fields that make up the Third Party Screening Results digital product.

### Purpose
Describes the data a subscriber to Third Party Screening Results receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Third Party Screening Results

### Collection Id
DataSpec::Coco::Third Party Screening Results

### Label
data specification

___

## Create Data Structure

### Display Name
Screening Result

### Qualified Name
DataStructure::Coco::Third Party Screening Results::Screening Result

### Description
One row per screening returned by the service.

### Namespace Path
coco_data_hub.third_party_screening_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Third Party Screening Results

### Element Id
DataStructure::Coco::Third Party Screening Results::Screening Result

### Membership Rationale
The Screening Result structure is part of the Third Party Screening Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Screening Identifier

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Screening Identifier

### Description
The screening request answered.

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
DataField::Coco::Third Party Screening Results::Screening Result::Screening Identifier

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Third Party Name

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Third Party Name

### Description
The name screened.

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
DataField::Coco::Third Party Screening Results::Screening Result::Third Party Name

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Screening Date

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Screening Date

### Description
When the service answered.

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
DataField::Coco::Third Party Screening Results::Screening Result::Screening Date

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Screening Status

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Screening Status

### Description
Clear, potential match, confirmed match.

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
DataField::Coco::Third Party Screening Results::Screening Result::Screening Status

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Screening Match Count

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Screening Match Count

### Description
The number of list entries matched.

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
DataField::Coco::Third Party Screening Results::Screening Result::Screening Match Count

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Screening Rating

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::Screening Rating

### Description
The service's overall risk indicator.

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
DataField::Coco::Third Party Screening Results::Screening Result::Screening Rating

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Screening Match

### Qualified Name
DataStructure::Coco::Third Party Screening Results::Screening Match

### Description
One row per list entry matched by a screening.

### Namespace Path
coco_data_hub.third_party_screening_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Third Party Screening Results

### Element Id
DataStructure::Coco::Third Party Screening Results::Screening Match

### Membership Rationale
The Screening Match structure is part of the Third Party Screening Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Screening Identifier

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::Screening Identifier

### Description
The screening.

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
DataField::Coco::Third Party Screening Results::Screening Match::Screening Identifier

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Screening Match List Name

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match List Name

### Description
The sanctions, PEP or media list matched.

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
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match List Name

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Screening Match Name

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Name

### Description
The list entry's name.

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
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Name

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Screening Match Rating

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Rating

### Description
The strength of the match.

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
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Rating

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Screening Match Description

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Description

### Description
Why the entry matched.

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
DataField::Coco::Third Party Screening Results::Screening Match::Screening Match Description

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

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
- schemaName: third_party_screening_results
- schemaDescription: The answers returned by the external screening service: matches against sanctions, politically exposed person and adverse media lists, with the risk indicators and the date each was given. Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

### Anchor ID
DigitalProduct::Coco::Third Party Screening Results

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Third Party Screening Results

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Supplier Material Certificates

*Solution component:* `CocoPharma::SolutionComponent::SupplierMaterialCertificates`  
*Category:* Evidence Record

The certificates of analysis and conformity that accompany incoming material, held against the supplier and the lot they certify.  The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

## Create Digital Product

### Display Name
Supplier Material Certificates

### Product Name
Supplier Material Certificates

### Qualified Name
DigitalProduct::Coco::Supplier Material Certificates

### Description
The certificates of analysis and conformity that accompany incoming material, held against the supplier and the lot they certify.  The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

### Purpose
Gives goods receipt and quarantine control the supplier's own test claims to check the material against.

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
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Element Id
DigitalProduct::Coco::Supplier Material Certificates

### Membership Rationale
Produced by the Procurement group's `SupplierMaterialCertificates` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Supplier Material Certificates Data Spec

### Qualified Name
DataSpec::Coco::Supplier Material Certificates

### Description
The data structures and fields that make up the Supplier Material Certificates digital product.

### Purpose
Describes the data a subscriber to Supplier Material Certificates receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Supplier Material Certificates

### Collection Id
DataSpec::Coco::Supplier Material Certificates

### Label
data specification

___

## Create Data Structure

### Display Name
Certificate Of Analysis

### Qualified Name
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Description
One row per certificate received with a lot of material.

### Namespace Path
coco_data_hub.supplier_material_certificates

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Material Certificates

### Element Id
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Membership Rationale
The Certificate Of Analysis structure is part of the Supplier Material Certificates data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Identifier

### Description
The unique identifier of the certificate.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Identifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Supplier Identifier

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Raw Material Code

### Description
The material certified.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Raw Material Code

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Lot Identifier

### Description
The supplier's lot number.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Lot Identifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Certificate Type

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Type

### Description
Certificate of analysis or certificate of conformity.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Type

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Certificate Date

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Date

### Description
When the supplier issued it.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Date

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Certificate Conformity Flag

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Conformity Flag

### Description
Whether the supplier declares the lot conforms to specification.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::Certificate Conformity Flag

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Certificate Test Result

### Qualified Name
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Description
One row per test reported on a certificate.

### Namespace Path
coco_data_hub.supplier_material_certificates

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Material Certificates

### Element Id
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Membership Rationale
The Certificate Test Result structure is part of the Supplier Material Certificates data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Certificate Identifier

### Description
The certificate.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Certificate Identifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Code

### Description
The test performed.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Code

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Test Value

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Value

### Description
The result reported.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Value

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Test Unit

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Unit

### Description
The unit of the result.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Test Unit

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Specification Minimum Value

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Specification Minimum Value

### Description
The lower specification limit.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Specification Minimum Value

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Specification Maximum Value

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Specification Maximum Value

### Description
The upper specification limit.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::Specification Maximum Value

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

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
- schemaName: supplier_material_certificates
- schemaDescription: The certificates of analysis and conformity that accompany incoming material, held against the supplier and the lot they certify. The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

### Anchor ID
DigitalProduct::Coco::Supplier Material Certificates

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Supplier Material Certificates

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Purchase Orders And Receipts

*Solution component:* `CocoPharma::SolutionComponent::Procurement`  
*Category:* Transactional Record

The purchase orders raised against approved suppliers and the confirmations that the goods or services were received, which is what a supplier invoice must match before it can be paid.

## Create Digital Product

### Display Name
Purchase Orders And Receipts

### Product Name
Purchase Orders And Receipts

### Qualified Name
DigitalProduct::Coco::Purchase Orders And Receipts

### Description
The purchase orders raised against approved suppliers and the confirmations that the goods or services were received, which is what a supplier invoice must match before it can be paid.

### Purpose
Provides the order and receipt halves of the three-way match.

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
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Element Id
DigitalProduct::Coco::Purchase Orders And Receipts

### Membership Rationale
Produced by the Procurement group's `Procurement` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Purchase Orders And Receipts Data Spec

### Qualified Name
DataSpec::Coco::Purchase Orders And Receipts

### Description
The data structures and fields that make up the Purchase Orders And Receipts digital product.

### Purpose
Describes the data a subscriber to Purchase Orders And Receipts receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Purchase Orders And Receipts

### Collection Id
DataSpec::Coco::Purchase Orders And Receipts

### Label
data specification

___

## Create Data Structure

### Display Name
Purchase Order

### Qualified Name
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Description
One row per purchase order.

### Namespace Path
coco_data_hub.purchase_orders_and_receipts

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Purchase Orders And Receipts

### Element Id
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Membership Rationale
The Purchase Order structure is part of the Purchase Orders And Receipts data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Identifier

### Description
The purchase order number.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Identifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Supplier Identifier

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Supplier Identifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Order Date

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Date

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Date

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Order Total Amount

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Total Amount

### Description
The ordered value.

### Data Type
bigdecimal

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Total Amount

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Order Currency Code

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Currency Code

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Order Approver Identifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Approver Identifier

### Description
Who approved the order.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Approver Identifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Order Current Status

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Current Status

### Description
Open, received, closed or cancelled.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::Order Current Status

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Goods Receipt Confirmation

### Qualified Name
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Description
One row per confirmation that an order line has been received.

### Namespace Path
coco_data_hub.purchase_orders_and_receipts

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Purchase Orders And Receipts

### Element Id
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Membership Rationale
The Goods Receipt Confirmation structure is part of the Purchase Orders And Receipts data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Goods Receipt Identifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Identifier

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Identifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Order Identifier

### Description
The order received against.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Order Identifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Line Item Number

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Line Item Number

### Description
The order line.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Line Item Number

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Goods Receipt Date

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Date

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Date

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Goods Receipt Quantity

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Quantity

### Description
The quantity confirmed received.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::Goods Receipt Quantity

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

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
- schemaName: purchase_orders_and_receipts
- schemaDescription: The purchase orders raised against approved suppliers and the confirmations that the goods or services were received, which is what a supplier invoice must match before it can be paid.

### Anchor ID
DigitalProduct::Coco::Purchase Orders And Receipts

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Purchase Orders And Receipts

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
