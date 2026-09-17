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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

2 products, 5 data structures, 29 data fields.  This file loads after `catalog.md`.

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
DigitalProduct::Coco::New Product Definitions

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
DigitalProduct::Coco::New Product Definitions

### Membership Rationale
Produced by the Research group's `Research` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
New Product Definitions Data Spec

### Qualified Name
DataSpec::Coco::New Product Definitions

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
DigitalProduct::Coco::New Product Definitions

### Collection Id
DataSpec::Coco::New Product Definitions

### Label
data specification

___

## Create Data Structure

### Display Name
Candidate Product Definition

### Qualified Name
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Description
One row per product candidate handed over from development.

### Namespace Path
coco_pharma.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::New Product Definitions

### Element Id
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Membership Rationale
The Candidate Product Definition structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
CandidateIdentifier

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::CandidateIdentifier

### Description
The development identifier of the candidate.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::CandidateIdentifier

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductCode

### Description
The product code assigned on handover.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductCode

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 2

___

## Create Data Field

### Display Name
ProductName

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductName

### Description
The proposed product name.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductName

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 3

___

## Create Data Field

### Display Name
FormulationIdentifier

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::FormulationIdentifier

### Description
The formulation developed.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::FormulationIdentifier

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 4

___

## Create Data Field

### Display Name
ActiveIngredientName

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::ActiveIngredientName

### Description
The active ingredient.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::ActiveIngredientName

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 5

___

## Create Data Field

### Display Name
ProductStrength

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductStrength

### Description
The strength.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::ProductStrength

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 6

___

## Create Data Field

### Display Name
ClinicalTrialIdentifier

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::ClinicalTrialIdentifier

### Description
The trial that supports the product.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::ClinicalTrialIdentifier

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 7

___

## Create Data Field

### Display Name
CandidateHandoverDate

### Qualified Name
DataField::Coco::New Product Definitions::Candidate Product Definition::CandidateHandoverDate

### Description
When development handed the definition over.

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
DataField::Coco::New Product Definitions::Candidate Product Definition::CandidateHandoverDate

### Data Structure
DataStructure::Coco::New Product Definitions::Candidate Product Definition

### Label
field 8

___

## Create Data Structure

### Display Name
Product Presentation

### Qualified Name
DataStructure::Coco::New Product Definitions::Product Presentation

### Description
One row per presentation the product will be supplied in.

### Namespace Path
coco_pharma.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::New Product Definitions

### Element Id
DataStructure::Coco::New Product Definitions::Product Presentation

### Membership Rationale
The Product Presentation structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::New Product Definitions::Product Presentation::ProductCode

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
DataField::Coco::New Product Definitions::Product Presentation::ProductCode

### Data Structure
DataStructure::Coco::New Product Definitions::Product Presentation

### Label
field 1

___

## Create Data Field

### Display Name
PackCode

### Qualified Name
DataField::Coco::New Product Definitions::Product Presentation::PackCode

### Description
The presentation's pack code.

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
DataField::Coco::New Product Definitions::Product Presentation::PackCode

### Data Structure
DataStructure::Coco::New Product Definitions::Product Presentation

### Label
field 2

___

## Create Data Field

### Display Name
PackDescription

### Qualified Name
DataField::Coco::New Product Definitions::Product Presentation::PackDescription

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

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::New Product Definitions::Product Presentation::PackDescription

### Data Structure
DataStructure::Coco::New Product Definitions::Product Presentation

### Label
field 3

___

## Create Data Field

### Display Name
PackQuantity

### Qualified Name
DataField::Coco::New Product Definitions::Product Presentation::PackQuantity

### Description
Units per pack.

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
DataField::Coco::New Product Definitions::Product Presentation::PackQuantity

### Data Structure
DataStructure::Coco::New Product Definitions::Product Presentation

### Label
field 4

___

## Create Data Structure

### Display Name
Product Specification

### Qualified Name
DataStructure::Coco::New Product Definitions::Product Specification

### Description
One row per specification limit the product must meet on release.

### Namespace Path
coco_pharma.new_product_definitions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::New Product Definitions

### Element Id
DataStructure::Coco::New Product Definitions::Product Specification

### Membership Rationale
The Product Specification structure is part of the New Product Definitions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::New Product Definitions::Product Specification::ProductCode

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
DataField::Coco::New Product Definitions::Product Specification::ProductCode

### Data Structure
DataStructure::Coco::New Product Definitions::Product Specification

### Label
field 1

___

## Create Data Field

### Display Name
TestCode

### Qualified Name
DataField::Coco::New Product Definitions::Product Specification::TestCode

### Description
The release test.

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
DataField::Coco::New Product Definitions::Product Specification::TestCode

### Data Structure
DataStructure::Coco::New Product Definitions::Product Specification

### Label
field 2

___

## Create Data Field

### Display Name
SpecificationMinimumValue

### Qualified Name
DataField::Coco::New Product Definitions::Product Specification::SpecificationMinimumValue

### Description
The lower limit.

### Data Type
string

### Position
3

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
DataField::Coco::New Product Definitions::Product Specification::SpecificationMinimumValue

### Data Structure
DataStructure::Coco::New Product Definitions::Product Specification

### Label
field 3

___

## Create Data Field

### Display Name
SpecificationMaximumValue

### Qualified Name
DataField::Coco::New Product Definitions::Product Specification::SpecificationMaximumValue

### Description
The upper limit.

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
DataField::Coco::New Product Definitions::Product Specification::SpecificationMaximumValue

### Data Structure
DataStructure::Coco::New Product Definitions::Product Specification

### Label
field 4

___

## Create Data Field

### Display Name
TestUnit

### Qualified Name
DataField::Coco::New Product Definitions::Product Specification::TestUnit

### Description
The unit.

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
DataField::Coco::New Product Definitions::Product Specification::TestUnit

### Data Structure
DataStructure::Coco::New Product Definitions::Product Specification

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
- schemaName: new_product_definitions
- schemaDescription: The definition of a new product as it leaves development: its composition, the presentations it will be supplied in and the specification it must meet. It is the source the product master is created from.

### Parent ID
DigitalProduct::Coco::New Product Definitions

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
coco_pharma.hospital_certifications

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
HospitalIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalIdentifier

### Description
The hospital.

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
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Label
field 1

___

## Create Data Field

### Display Name
ClinicalTrialIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::ClinicalTrialIdentifier

### Description
The trial.

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
DataField::Coco::Hospital Certifications::Hospital Certification::ClinicalTrialIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Label
field 2

___

## Create Data Field

### Display Name
HospitalCertificationDate

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationDate

### Description
When certified.

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
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationDate

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Label
field 3

___

## Create Data Field

### Display Name
HospitalCertificationEndDate

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationEndDate

### Description
When the certification lapses.

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
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationEndDate

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Label
field 4

___

## Create Data Field

### Display Name
HospitalCertificationStatus

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationStatus

### Description
Certified, suspended or withdrawn.

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
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertificationStatus

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

### Label
field 5

___

## Create Data Field

### Display Name
HospitalCertifierIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertifierIdentifier

### Description
Who certified the site.

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
DataField::Coco::Hospital Certifications::Hospital Certification::HospitalCertifierIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Hospital Certification

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
coco_pharma.hospital_certifications

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
HospitalIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::HospitalIdentifier

### Description
The site.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::HospitalIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Label
field 1

___

## Create Data Field

### Display Name
ClinicalTrialIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ClinicalTrialIdentifier

### Description
The trial.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ClinicalTrialIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Label
field 2

___

## Create Data Field

### Display Name
ClinicianIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ClinicianIdentifier

### Description
The staff member.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ClinicianIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Label
field 3

___

## Create Data Field

### Display Name
ProtocolIdentifier

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ProtocolIdentifier

### Description
The protocol trained on.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::ProtocolIdentifier

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Label
field 4

___

## Create Data Field

### Display Name
TrainingCompletedDate

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::TrainingCompletedDate

### Description
When training was completed.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::TrainingCompletedDate

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

### Label
field 5

___

## Create Data Field

### Display Name
TrainingExpiryDate

### Qualified Name
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::TrainingExpiryDate

### Description
When the training lapses.

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
DataField::Coco::Hospital Certifications::Site Staff Training Evidence::TrainingExpiryDate

### Data Structure
DataStructure::Coco::Hospital Certifications::Site Staff Training Evidence

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
