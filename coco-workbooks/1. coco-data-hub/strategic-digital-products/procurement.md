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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

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
coco_pharma.supplier_master_data

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
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierIdentifier

### Description
The company's unique identifier for the supplier.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 1

___

## Create Data Field

### Display Name
SupplierName

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierName

### Description
The supplier's legal name.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierName

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 2

___

## Create Data Field

### Display Name
SupplierType

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierType

### Description
Material supplier, service provider, healthcare organisation or other.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierType

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 3

___

## Create Data Field

### Display Name
SupplierCountry

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierCountry

### Description
The country of incorporation.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierCountry

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 4

___

## Create Data Field

### Display Name
SupplierApprovedFlag

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierApprovedFlag

### Description
Whether the supplier has passed onboarding.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierApprovedFlag

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 5

___

## Create Data Field

### Display Name
SupplierApprovedDate

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierApprovedDate

### Description
When approval was granted.

### Data Type
date

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
DataField::Coco::Supplier Master Data::Supplier::SupplierApprovedDate

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

### Label
field 6

___

## Create Data Field

### Display Name
SupplierCurrentStatus

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier::SupplierCurrentStatus

### Description
Active, suspended or closed.

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
DataField::Coco::Supplier Master Data::Supplier::SupplierCurrentStatus

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier

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
coco_pharma.supplier_master_data

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
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierIdentifier

### Description
The supplier.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Label
field 1

___

## Create Data Field

### Display Name
SupplierScreenedStatus

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierScreenedStatus

### Description
Clear, match under review, or blocked.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierScreenedStatus

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Label
field 2

___

## Create Data Field

### Display Name
SupplierScreenedDate

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierScreenedDate

### Description
When the supplier was last screened.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierScreenedDate

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Label
field 3

___

## Create Data Field

### Display Name
SupplierRating

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierRating

### Description
The assessed risk rating.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::SupplierRating

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Label
field 4

___

## Create Data Field

### Display Name
ScreeningIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::ScreeningIdentifier

### Description
The screening result the status rests on.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::ScreeningIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

### Label
field 5

___

## Create Data Field

### Display Name
AnomalyIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Risk Status::AnomalyIdentifier

### Description
An open concern raised by transaction monitoring, if any.

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
DataField::Coco::Supplier Master Data::Supplier Risk Status::AnomalyIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Risk Status

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
coco_pharma.supplier_master_data

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
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::SupplierIdentifier

### Description
The supplier.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Label
field 1

___

## Create Data Field

### Display Name
BankAccountCurrentIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountCurrentIdentifier

### Description
The bank account, masked.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountCurrentIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Label
field 2

___

## Create Data Field

### Display Name
BankAccountProviderName

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountProviderName

### Description
The bank.

### Data Type
string

### Position
3

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountProviderName

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Label
field 3

___

## Create Data Field

### Display Name
BankAccountCountry

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountCountry

### Description
The country of the account.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::BankAccountCountry

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Label
field 4

___

## Create Data Field

### Display Name
PaymentDetailChangeIdentifier

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::PaymentDetailChangeIdentifier

### Description
The verified change that set these details.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::PaymentDetailChangeIdentifier

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

### Label
field 5

___

## Create Data Field

### Display Name
PaymentDetailVerifiedDate

### Qualified Name
DataField::Coco::Supplier Master Data::Supplier Payment Details::PaymentDetailVerifiedDate

### Description
When the details were last independently verified.

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
DataField::Coco::Supplier Master Data::Supplier Payment Details::PaymentDetailVerifiedDate

### Data Structure
DataStructure::Coco::Supplier Master Data::Supplier Payment Details

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
- schemaName: supplier_master_data
- schemaDescription: The authoritative record of every third party the company transacts with: its identity, its screening status and risk rating, and the payment details it is paid to. The supplier fraud was possible because this record was not authoritative; making it so is the control.

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
coco_pharma.third_party_onboarding_cases

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
OnboardingCaseIdentifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseIdentifier

### Description
The unique identifier of the case.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseIdentifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 1

___

## Create Data Field

### Display Name
ThirdPartyName

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyName

### Description
The proposed third party's legal name.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyName

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 2

___

## Create Data Field

### Display Name
ThirdPartyCountry

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyCountry

### Description
Its country of incorporation.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyCountry

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 3

___

## Create Data Field

### Display Name
ThirdPartyOwnerDescription

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyOwnerDescription

### Description
Its beneficial ownership as declared.

### Data Type
string

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::ThirdPartyOwnerDescription

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 4

___

## Create Data Field

### Display Name
OnboardingCaseRequesterIdentifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseRequesterIdentifier

### Description
Who proposed the third party.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseRequesterIdentifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 5

___

## Create Data Field

### Display Name
OnboardingCaseStartDate

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseStartDate

### Description
When the case was opened.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseStartDate

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 6

___

## Create Data Field

### Display Name
OnboardingCaseCurrentStatus

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseCurrentStatus

### Description
Screening, risk assessment, approved, rejected.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::OnboardingCaseCurrentStatus

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

### Label
field 7

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::SupplierIdentifier

### Description
The supplier record created on approval.

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
DataField::Coco::Third Party Onboarding Cases::Onboarding Case::SupplierIdentifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Onboarding Case

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
coco_pharma.third_party_onboarding_cases

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
OnboardingCaseIdentifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::OnboardingCaseIdentifier

### Description
The case.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::OnboardingCaseIdentifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Label
field 1

___

## Create Data Field

### Display Name
ScreeningIdentifier

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningIdentifier

### Description
The screening request.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningIdentifier

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Label
field 2

___

## Create Data Field

### Display Name
ScreeningRequestedTimestamp

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningRequestedTimestamp

### Description
When it was submitted.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningRequestedTimestamp

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Label
field 3

___

## Create Data Field

### Display Name
ScreeningType

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningType

### Description
Sanctions, politically exposed persons, adverse media, or all.

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::ScreeningType

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

### Label
field 4

___

## Create Data Field

### Display Name
SupplierRating

### Qualified Name
DataField::Coco::Third Party Onboarding Cases::Screening Request::SupplierRating

### Description
The risk rating assigned once the result was assessed.

### Data Type
string

### Position
5

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
DataField::Coco::Third Party Onboarding Cases::Screening Request::SupplierRating

### Data Structure
DataStructure::Coco::Third Party Onboarding Cases::Screening Request

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
- schemaName: third_party_onboarding_cases
- schemaDescription: Every proposed third party driven through screening, risk assessment and approval to the creation of a supplier record. It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.

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
coco_pharma.third_party_screening_results

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
ScreeningIdentifier

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningIdentifier

### Description
The screening request answered.

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
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningIdentifier

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Label
field 1

___

## Create Data Field

### Display Name
ThirdPartyName

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ThirdPartyName

### Description
The name screened.

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
DataField::Coco::Third Party Screening Results::Screening Result::ThirdPartyName

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Label
field 2

___

## Create Data Field

### Display Name
ScreeningDate

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningDate

### Description
When the service answered.

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
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningDate

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Label
field 3

___

## Create Data Field

### Display Name
ScreeningStatus

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningStatus

### Description
Clear, potential match, confirmed match.

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
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningStatus

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Label
field 4

___

## Create Data Field

### Display Name
ScreeningMatchCount

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningMatchCount

### Description
The number of list entries matched.

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
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningMatchCount

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

### Label
field 5

___

## Create Data Field

### Display Name
ScreeningRating

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningRating

### Description
The service's overall risk indicator.

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
DataField::Coco::Third Party Screening Results::Screening Result::ScreeningRating

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Result

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
coco_pharma.third_party_screening_results

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
ScreeningIdentifier

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningIdentifier

### Description
The screening.

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
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningIdentifier

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Label
field 1

___

## Create Data Field

### Display Name
ScreeningMatchListName

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchListName

### Description
The sanctions, PEP or media list matched.

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
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchListName

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Label
field 2

___

## Create Data Field

### Display Name
ScreeningMatchName

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchName

### Description
The list entry's name.

### Data Type
string

### Position
3

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
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchName

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Label
field 3

___

## Create Data Field

### Display Name
ScreeningMatchRating

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchRating

### Description
The strength of the match.

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
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchRating

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

### Label
field 4

___

## Create Data Field

### Display Name
ScreeningMatchDescription

### Qualified Name
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchDescription

### Description
Why the entry matched.

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
DataField::Coco::Third Party Screening Results::Screening Match::ScreeningMatchDescription

### Data Structure
DataStructure::Coco::Third Party Screening Results::Screening Match

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
- schemaName: third_party_screening_results
- schemaDescription: The answers returned by the external screening service: matches against sanctions, politically exposed person and adverse media lists, with the risk indicators and the date each was given. Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.

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
coco_pharma.supplier_material_certificates

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
CertificateIdentifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateIdentifier

### Description
The unique identifier of the certificate.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateIdentifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 1

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::SupplierIdentifier

### Description
The supplier.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 2

___

## Create Data Field

### Display Name
RawMaterialCode

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::RawMaterialCode

### Description
The material certified.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::RawMaterialCode

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 3

___

## Create Data Field

### Display Name
LotIdentifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::LotIdentifier

### Description
The supplier's lot number.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::LotIdentifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 4

___

## Create Data Field

### Display Name
CertificateType

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateType

### Description
Certificate of analysis or certificate of conformity.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateType

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 5

___

## Create Data Field

### Display Name
CertificateDate

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateDate

### Description
When the supplier issued it.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateDate

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

### Label
field 6

___

## Create Data Field

### Display Name
CertificateConformityFlag

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateConformityFlag

### Description
Whether the supplier declares the lot conforms to specification.

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
DataField::Coco::Supplier Material Certificates::Certificate Of Analysis::CertificateConformityFlag

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Of Analysis

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
coco_pharma.supplier_material_certificates

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
CertificateIdentifier

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::CertificateIdentifier

### Description
The certificate.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::CertificateIdentifier

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Label
field 1

___

## Create Data Field

### Display Name
TestCode

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestCode

### Description
The test performed.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestCode

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Label
field 2

___

## Create Data Field

### Display Name
TestValue

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestValue

### Description
The result reported.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestValue

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Label
field 3

___

## Create Data Field

### Display Name
TestUnit

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestUnit

### Description
The unit of the result.

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::TestUnit

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Label
field 4

___

## Create Data Field

### Display Name
SpecificationMinimumValue

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::SpecificationMinimumValue

### Description
The lower specification limit.

### Data Type
string

### Position
5

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::SpecificationMinimumValue

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

### Label
field 5

___

## Create Data Field

### Display Name
SpecificationMaximumValue

### Qualified Name
DataField::Coco::Supplier Material Certificates::Certificate Test Result::SpecificationMaximumValue

### Description
The upper specification limit.

### Data Type
string

### Position
6

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
DataField::Coco::Supplier Material Certificates::Certificate Test Result::SpecificationMaximumValue

### Data Structure
DataStructure::Coco::Supplier Material Certificates::Certificate Test Result

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
- schemaName: supplier_material_certificates
- schemaDescription: The certificates of analysis and conformity that accompany incoming material, held against the supplier and the lot they certify. The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.

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
coco_pharma.purchase_orders_and_receipts

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
OrderIdentifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderIdentifier

### Description
The purchase order number.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderIdentifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 1

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::SupplierIdentifier

### Description
The supplier.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::SupplierIdentifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 2

___

## Create Data Field

### Display Name
OrderDate

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderDate

### Description
When raised.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderDate

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 3

___

## Create Data Field

### Display Name
OrderTotalAmount

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderTotalAmount

### Description
The ordered value.

### Data Type
bigdecimal

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderTotalAmount

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 4

___

## Create Data Field

### Display Name
OrderCurrencyCode

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderCurrencyCode

### Description
The currency.

### Data Type
string

### Position
5

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderCurrencyCode

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 5

___

## Create Data Field

### Display Name
OrderApproverIdentifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderApproverIdentifier

### Description
Who approved the order.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderApproverIdentifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

### Label
field 6

___

## Create Data Field

### Display Name
OrderCurrentStatus

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderCurrentStatus

### Description
Open, received, closed or cancelled.

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
DataField::Coco::Purchase Orders And Receipts::Purchase Order::OrderCurrentStatus

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Purchase Order

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
coco_pharma.purchase_orders_and_receipts

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
GoodsReceiptIdentifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptIdentifier

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptIdentifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Label
field 1

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::OrderIdentifier

### Description
The order received against.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::OrderIdentifier

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Label
field 2

___

## Create Data Field

### Display Name
LineItemNumber

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::LineItemNumber

### Description
The order line.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::LineItemNumber

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Label
field 3

___

## Create Data Field

### Display Name
GoodsReceiptDate

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptDate

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptDate

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

### Label
field 4

___

## Create Data Field

### Display Name
GoodsReceiptQuantity

### Qualified Name
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptQuantity

### Description
The quantity confirmed received.

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
DataField::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation::GoodsReceiptQuantity

### Data Structure
DataStructure::Coco::Purchase Orders And Receipts::Goods Receipt Confirmation

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
- schemaName: purchase_orders_and_receipts
- schemaDescription: The purchase orders raised against approved suppliers and the confirmations that the goods or services were received, which is what a supplier invoice must match before it can be paid.

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
