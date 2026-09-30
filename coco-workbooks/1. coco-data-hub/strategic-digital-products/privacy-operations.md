# Privacy Operations Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 7 digital products owned by the Privacy Operations business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of the privacy function: rights requests, identity verifications, the record of processing, personal data discovery findings, fulfilment actions, retention obligations and the retention periods set on catalogued assets.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Data Subject Rights Requests | `CocoPharma::SolutionComponent::RightsRequestIntake` | Transactional Record | Rights Request, Request Response |
| Requester Identity Verifications | `CocoPharma::SolutionComponent::IdentityVerification` | Evidence Record | Identity Verification |
| Record Of Processing Activities | `CocoPharma::SolutionComponent::RecordOfProcessingRegister` | Master Data | Processing Activity, Processing System |
| Personal Data Discovery Findings | `CocoPharma::SolutionComponent::PersonalDataDiscovery` | Insight | Discovered Holding, Register Discrepancy |
| Rights Fulfilment Actions | `CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator` | Transactional Record | Fulfilment Request, System Action |
| Retention Obligations | `CocoPharma::SolutionComponent::RetentionScheduleService` | Reference Data | Retention Obligation |
| Retention Period Assignments | `SolutionComponent::Set Retention Period::V1.0` | Reference Data | Retention Period Assignment |

For every product this file:

1. creates the **digital product** and adds it to the `Privacy Operations` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

7 products, 11 data structures, 78 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret privacy-operations.md
```

---

# Data Subject Rights Requests

*Solution component:* `CocoPharma::SolutionComponent::RightsRequestIntake`  
*Category:* Transactional Record

Requests from data subjects received through every channel the company offers, with the statutory clock that starts on receipt, and the response assembled for each.  An email to a site address counts exactly as much as a submission through the portal.

## Create Digital Product

### Display Name
Data Subject Rights Requests

### Product Name
Data Subject Rights Requests

### Qualified Name
DigitalProduct::Coco::Data Subject Rights Requests

### Description
Requests from data subjects received through every channel the company offers, with the statutory clock that starts on receipt, and the response assembled for each.  An email to a site address counts exactly as much as a submission through the portal.

### Purpose
Records every request from the moment of receipt to the response sent, with its deadline.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Data Subject Rights Requests

### Membership Rationale
Produced by the Privacy Operations group's `RightsRequestIntake` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Data Subject Rights Requests Data Spec

### Qualified Name
DataSpec::Coco::Data Subject Rights Requests

### Description
The data structures and fields that make up the Data Subject Rights Requests digital product.

### Purpose
Describes the data a subscriber to Data Subject Rights Requests receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Data Subject Rights Requests

### Collection Id
DataSpec::Coco::Data Subject Rights Requests

### Label
data specification

___

## Create Data Structure

### Display Name
Rights Request

### Qualified Name
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Description
One row per request received.

### Namespace Path
coco_data_hub.data_subject_rights_requests

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Data Subject Rights Requests

### Element Id
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Membership Rationale
The Rights Request structure is part of the Data Subject Rights Requests data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Rights Request Identifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Identifier

### Description
The request.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Identifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Rights Request Received Timestamp

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Received Timestamp

### Description
When first received anywhere in the company.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Received Timestamp

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Rights Request Channel Type

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Channel Type

### Description
Portal, email, letter, telephone or other.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Channel Type

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Rights Request Type

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Type

### Description
Access, rectification, erasure, objection, portability or restriction.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Type

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Data Subject Type

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Data Subject Type

### Description
Patient, worker, healthcare professional, other.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Data Subject Type

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Data Subject Claimed Name

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Data Subject Claimed Name

### Description
The name the requester gave.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Data Subject Claimed Name

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Rights Request Description

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Description

### Description
What was asked for.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Description

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Rights Request Due Date

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Due Date

### Description
The statutory deadline.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Due Date

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Rights Request Current Status

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Current Status

### Description
Received, verifying, in progress, responded, closed.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::Rights Request Current Status

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Request Response

### Qualified Name
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Description
One row per response sent to a requester.

### Namespace Path
coco_data_hub.data_subject_rights_requests

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Data Subject Rights Requests

### Element Id
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Membership Rationale
The Request Response structure is part of the Data Subject Rights Requests data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Rights Request Identifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Identifier

### Description
The request.

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
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Identifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Rights Request Response Timestamp

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Response Timestamp

### Description
When the response was sent.

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
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Response Timestamp

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Rights Request Response Description

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Response Description

### Description
The response, the actions taken and the reasons.

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
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Response Description

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Rights Request Responder Identifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Responder Identifier

### Description
Who sent it.

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
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Responder Identifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Rights Request Refused Flag

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Refused Flag

### Description
Whether any part of the request was refused.

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
DataField::Coco::Data Subject Rights Requests::Request Response::Rights Request Refused Flag

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

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
- schemaName: data_subject_rights_requests
- schemaDescription: Requests from data subjects received through every channel the company offers, with the statutory clock that starts on receipt, and the response assembled for each. An email to a site address counts exactly as much as a submission through the portal.

### Anchor ID
DigitalProduct::Coco::Data Subject Rights Requests

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Data Subject Rights Requests

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Requester Identity Verifications

*Solution component:* `CocoPharma::SolutionComponent::IdentityVerification`  
*Category:* Evidence Record

The verification that a requester is who they claim to be, proportionate to what they are asking for.  It is the step that stops the rights process from becoming an attack on the data it is meant to protect.

## Create Digital Product

### Display Name
Requester Identity Verifications

### Product Name
Requester Identity Verifications

### Qualified Name
DigitalProduct::Coco::Requester Identity Verifications

### Description
The verification that a requester is who they claim to be, proportionate to what they are asking for.  It is the step that stops the rights process from becoming an attack on the data it is meant to protect.

### Purpose
Evidences, for each request, how the requester's identity was established before any data was released.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Requester Identity Verifications

### Membership Rationale
Produced by the Privacy Operations group's `IdentityVerification` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Requester Identity Verifications Data Spec

### Qualified Name
DataSpec::Coco::Requester Identity Verifications

### Description
The data structures and fields that make up the Requester Identity Verifications digital product.

### Purpose
Describes the data a subscriber to Requester Identity Verifications receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Requester Identity Verifications

### Collection Id
DataSpec::Coco::Requester Identity Verifications

### Label
data specification

___

## Create Data Structure

### Display Name
Identity Verification

### Qualified Name
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Description
One row per verification performed.

### Namespace Path
coco_data_hub.requester_identity_verifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Requester Identity Verifications

### Element Id
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Membership Rationale
The Identity Verification structure is part of the Requester Identity Verifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Rights Request Identifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Identifier

### Description
The request.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Identifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Rights Request Verified Timestamp

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Timestamp

### Description
When verified.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Timestamp

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Rights Request Verified Method Code

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Method Code

### Description
The method used.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Method Code

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Rights Request Verified Evidence Description

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Evidence Description

### Description
The evidence offered and accepted.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Evidence Description

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Rights Request Verified Status

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Status

### Description
Verified, failed, insufficient.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verified Status

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Rights Request Verifier Identifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verifier Identifier

### Description
Who verified.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Rights Request Verifier Identifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Data Subject Identifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::Data Subject Identifier

### Description
The verified subject's identifier in the relevant register.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::Data Subject Identifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

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
- schemaName: requester_identity_verifications
- schemaDescription: The verification that a requester is who they claim to be, proportionate to what they are asking for. It is the step that stops the rights process from becoming an attack on the data it is meant to protect.

### Anchor ID
DigitalProduct::Coco::Requester Identity Verifications

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Requester Identity Verifications

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Record Of Processing Activities

*Solution component:* `CocoPharma::SolutionComponent::RecordOfProcessingRegister`  
*Category:* Master Data

What personal data the company processes, for what purpose, under what lawful basis, and in which systems and processors it is held.  It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.

## Create Digital Product

### Display Name
Record Of Processing Activities

### Product Name
Record Of Processing Activities

### Qualified Name
DigitalProduct::Coco::Record Of Processing Activities

### Description
What personal data the company processes, for what purpose, under what lawful basis, and in which systems and processors it is held.  It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.

### Purpose
Gives fulfilment the list of systems and processors to ask for each category of data subject.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Record Of Processing Activities

### Membership Rationale
Produced by the Privacy Operations group's `RecordOfProcessingRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Record Of Processing Activities Data Spec

### Qualified Name
DataSpec::Coco::Record Of Processing Activities

### Description
The data structures and fields that make up the Record Of Processing Activities digital product.

### Purpose
Describes the data a subscriber to Record Of Processing Activities receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Record Of Processing Activities

### Collection Id
DataSpec::Coco::Record Of Processing Activities

### Label
data specification

___

## Create Data Structure

### Display Name
Processing Activity

### Qualified Name
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Description
One row per processing activity.

### Namespace Path
coco_data_hub.record_of_processing_activities

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Record Of Processing Activities

### Element Id
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Membership Rationale
The Processing Activity structure is part of the Record Of Processing Activities data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Processing Activity Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Identifier

### Description
The activity.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Processing Activity Name

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Name

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Name

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Processing Activity Purpose Description

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Purpose Description

### Description
The purpose.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Purpose Description

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Processing Activity Basis Code

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Basis Code

### Description
The lawful basis.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Basis Code

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Data Subject Type

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Data Subject Type

### Description
The category of data subject.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Data Subject Type

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Processing Activity Data Description

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Data Description

### Description
The categories of personal data.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Data Description

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Processing Activity Owner Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Owner Identifier

### Description
The accountable owner.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Owner Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Processing Activity Current Timestamp

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Current Timestamp

### Description
When last reviewed.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::Processing Activity Current Timestamp

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Processing System

### Qualified Name
DataStructure::Coco::Record Of Processing Activities::Processing System

### Description
One row per system or processor holding data for an activity.

### Namespace Path
coco_data_hub.record_of_processing_activities

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Record Of Processing Activities

### Element Id
DataStructure::Coco::Record Of Processing Activities::Processing System

### Membership Rationale
The Processing System structure is part of the Record Of Processing Activities data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Processing Activity System Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::Processing Activity System Identifier

### Description
The unique identifier of the entry for one system or processor holding data for a processing activity.

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
DataField::Coco::Record Of Processing Activities::Processing System::Processing Activity System Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Processing Activity Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::Processing Activity Identifier

### Description
The activity.

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
DataField::Coco::Record Of Processing Activities::Processing System::Processing Activity Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::System Identifier

### Description
The system, for internal holdings.

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
DataField::Coco::Record Of Processing Activities::Processing System::System Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::Supplier Identifier

### Description
The processor, for external holdings.

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
DataField::Coco::Record Of Processing Activities::Processing System::Supplier Identifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Retention Category Code

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::Retention Category Code

### Description
The retention category of the data held.

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
DataField::Coco::Record Of Processing Activities::Processing System::Retention Category Code

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
System Reconciled Flag

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::System Reconciled Flag

### Description
Whether discovery found a discrepancy against this entry.

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
DataField::Coco::Record Of Processing Activities::Processing System::System Reconciled Flag

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

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
- schemaName: record_of_processing_activities
- schemaDescription: What personal data the company processes, for what purpose, under what lawful basis, and in which systems and processors it is held. It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.

### Anchor ID
DigitalProduct::Coco::Record Of Processing Activities

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Record Of Processing Activities

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Personal Data Discovery Findings

*Solution component:* `CocoPharma::SolutionComponent::PersonalDataDiscovery`  
*Category:* Insight

What the survey of systems and stores actually found: personal data holdings by system, and the discrepancies between them and the record of processing.  The register describes what the company believes it processes; this describes what it actually holds.

## Create Digital Product

### Display Name
Personal Data Discovery Findings

### Product Name
Personal Data Discovery Findings

### Qualified Name
DigitalProduct::Coco::Personal Data Discovery Findings

### Description
What the survey of systems and stores actually found: personal data holdings by system, and the discrepancies between them and the record of processing.  The register describes what the company believes it processes; this describes what it actually holds.

### Purpose
Keeps the record of processing honest by reconciling it against the catalogued estate.

### Category
Insight

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Personal Data Discovery Findings

### Membership Rationale
Produced by the Privacy Operations group's `PersonalDataDiscovery` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Personal Data Discovery Findings Data Spec

### Qualified Name
DataSpec::Coco::Personal Data Discovery Findings

### Description
The data structures and fields that make up the Personal Data Discovery Findings digital product.

### Purpose
Describes the data a subscriber to Personal Data Discovery Findings receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Personal Data Discovery Findings

### Collection Id
DataSpec::Coco::Personal Data Discovery Findings

### Label
data specification

___

## Create Data Structure

### Display Name
Discovered Holding

### Qualified Name
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Description
One row per personal data holding found.

### Namespace Path
coco_data_hub.personal_data_discovery_findings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Personal Data Discovery Findings

### Element Id
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Membership Rationale
The Discovered Holding structure is part of the Personal Data Discovery Findings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Holding Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Identifier

### Description
The holding.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Asset Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Asset Identifier

### Description
The catalogued asset.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Asset Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::System Identifier

### Description
The system.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::System Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Data Subject Type

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Data Subject Type

### Description
The category of data subject the data concerns.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Data Subject Type

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Holding Data Description

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Data Description

### Description
The personal data found.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Data Description

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Holding Discovered Timestamp

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Discovered Timestamp

### Description
When found.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Holding Discovered Timestamp

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Processing Activity Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Processing Activity Identifier

### Description
The activity it reconciles to, if any.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::Processing Activity Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Register Discrepancy

### Qualified Name
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Description
One row per difference between what was found and what the register says.

### Namespace Path
coco_data_hub.personal_data_discovery_findings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Personal Data Discovery Findings

### Element Id
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Membership Rationale
The Register Discrepancy structure is part of the Personal Data Discovery Findings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Discrepancy Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Identifier

### Description
The discrepancy.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Holding Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Holding Identifier

### Description
The holding, for data found but not registered.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Holding Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Processing Activity Identifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Processing Activity Identifier

### Description
The activity, for data registered but not found.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Processing Activity Identifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Discrepancy Type

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Type

### Description
Unregistered holding, missing holding, category mismatch.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Type

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Discrepancy Description

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Description

### Description
The difference.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Description

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Discrepancy Current Status

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Current Status

### Description
Open, register corrected, holding removed, accepted.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::Discrepancy Current Status

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

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
- schemaName: personal_data_discovery_findings
- schemaDescription: What the survey of systems and stores actually found: personal data holdings by system, and the discrepancies between them and the record of processing. The register describes what the company believes it processes; this describes what it actually holds.

### Anchor ID
DigitalProduct::Coco::Personal Data Discovery Findings

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Personal Data Discovery Findings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Rights Fulfilment Actions

*Solution component:* `CocoPharma::SolutionComponent::RightsFulfilmentOrchestrator`  
*Category:* Transactional Record

Each verified request fanned out to every system and processor holding the person's data, what came back, and the erasure, rectification and objection decisions driven onward to the systems that must act on them.  It is the component that turns a register into an answer.

## Create Digital Product

### Display Name
Rights Fulfilment Actions

### Product Name
Rights Fulfilment Actions

### Qualified Name
DigitalProduct::Coco::Rights Fulfilment Actions

### Description
Each verified request fanned out to every system and processor holding the person's data, what came back, and the erasure, rectification and objection decisions driven onward to the systems that must act on them.  It is the component that turns a register into an answer.

### Purpose
Shows, per request, every system asked, every answer received and every action taken.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Rights Fulfilment Actions

### Membership Rationale
Produced by the Privacy Operations group's `RightsFulfilmentOrchestrator` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Rights Fulfilment Actions Data Spec

### Qualified Name
DataSpec::Coco::Rights Fulfilment Actions

### Description
The data structures and fields that make up the Rights Fulfilment Actions digital product.

### Purpose
Describes the data a subscriber to Rights Fulfilment Actions receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Rights Fulfilment Actions

### Collection Id
DataSpec::Coco::Rights Fulfilment Actions

### Label
data specification

___

## Create Data Structure

### Display Name
Fulfilment Request

### Qualified Name
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Description
One row per verified request taken into fulfilment.

### Namespace Path
coco_data_hub.rights_fulfilment_actions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Rights Fulfilment Actions

### Element Id
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Membership Rationale
The Fulfilment Request structure is part of the Rights Fulfilment Actions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Rights Request Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Identifier

### Description
The request.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Data Subject Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Data Subject Identifier

### Description
The verified subject.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Data Subject Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Data Subject Type

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Data Subject Type

### Description
The category of subject.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Data Subject Type

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Rights Request Type

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Type

### Description
The right exercised.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Type

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Rights Request Fulfilment Start Timestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Start Timestamp

### Description
When fulfilment began.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Start Timestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Rights Request Fulfilment Count

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Count

### Description
The number of systems and processors asked.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Count

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Rights Request Fulfilment Status

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Status

### Description
In progress, awaiting responses, decided, complete.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::Rights Request Fulfilment Status

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
System Action

### Qualified Name
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Description
One row per system or processor per request.

### Namespace Path
coco_data_hub.rights_fulfilment_actions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Rights Fulfilment Actions

### Element Id
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Membership Rationale
The System Action structure is part of the Rights Fulfilment Actions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
System Action Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Identifier

### Description
The unique identifier of the action requested of one system or processor for a request.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Rights Request Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::Rights Request Identifier

### Description
The request.

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
DataField::Coco::Rights Fulfilment Actions::System Action::Rights Request Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Identifier

### Description
The system, for internal holdings.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::Supplier Identifier

### Description
The processor, for external holdings.

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
DataField::Coco::Rights Fulfilment Actions::System Action::Supplier Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
System Action Type

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Type

### Description
Locate, disclose, rectify, erase, restrict.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Type

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
System Action Requested Timestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Requested Timestamp

### Description
When asked.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Requested Timestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
System Action Completed Timestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Completed Timestamp

### Description
When answered.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Completed Timestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
System Action Status

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Status

### Description
Requested, completed, refused, no data held.

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
DataField::Coco::Rights Fulfilment Actions::System Action::System Action Status

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Retention Obligation Identifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::Retention Obligation Identifier

### Description
The retention obligation that overrode an erasure, if any.

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
DataField::Coco::Rights Fulfilment Actions::System Action::Retention Obligation Identifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

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
- schemaName: rights_fulfilment_actions
- schemaDescription: Each verified request fanned out to every system and processor holding the person's data, what came back, and the erasure, rectification and objection decisions driven onward to the systems that must act on them. It is the component that turns a register into an answer.

### Anchor ID
DigitalProduct::Coco::Rights Fulfilment Actions

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Rights Fulfilment Actions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Retention Obligations

*Solution component:* `CocoPharma::SolutionComponent::RetentionScheduleService`  
*Category:* Reference Data

The retention obligation attaching to each category of personal data, and the basis that lets it override a request to be forgotten.  Clinical trial records, employment decisions and health surveillance all outrank erasure, and the chain has to know that per holding rather than in general.

## Create Digital Product

### Display Name
Retention Obligations

### Product Name
Retention Obligations

### Qualified Name
DigitalProduct::Coco::Retention Obligations

### Description
The retention obligation attaching to each category of personal data, and the basis that lets it override a request to be forgotten.  Clinical trial records, employment decisions and health surveillance all outrank erasure, and the chain has to know that per holding rather than in general.

### Purpose
Lets an erasure decision be checked against the obligations that override it before anything is deleted.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Retention Obligations

### Membership Rationale
Produced by the Privacy Operations group's `RetentionScheduleService` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Retention Obligations Data Spec

### Qualified Name
DataSpec::Coco::Retention Obligations

### Description
The data structures and fields that make up the Retention Obligations digital product.

### Purpose
Describes the data a subscriber to Retention Obligations receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Retention Obligations

### Collection Id
DataSpec::Coco::Retention Obligations

### Label
data specification

___

## Create Data Structure

### Display Name
Retention Obligation

### Qualified Name
DataStructure::Coco::Retention Obligations::Retention Obligation

### Description
One row per retention category.

### Namespace Path
coco_data_hub.retention_obligations

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Retention Obligations

### Element Id
DataStructure::Coco::Retention Obligations::Retention Obligation

### Membership Rationale
The Retention Obligation structure is part of the Retention Obligations data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Retention Obligation Identifier

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Obligation Identifier

### Description
The obligation.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Obligation Identifier

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Retention Category Code

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Category Code

### Description
The category of data.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Category Code

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Retention Category Description

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Category Description

### Description
What the category covers.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Category Description

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Retention Duration

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Duration

### Description
How long the data must be kept, in months.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Duration

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Retention Basis Description

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Basis Description

### Description
The regulation or contract that requires it.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Basis Description

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Retention Overrides Erasure Flag

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Overrides Erasure Flag

### Description
Whether the obligation overrides a request for erasure.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Overrides Erasure Flag

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Retention Obligation Start Date

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::Retention Obligation Start Date

### Description
When the obligation took effect.

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
DataField::Coco::Retention Obligations::Retention Obligation::Retention Obligation Start Date

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

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
- schemaName: retention_obligations
- schemaDescription: The retention obligation attaching to each category of personal data, and the basis that lets it override a request to be forgotten. Clinical trial records, employment decisions and health surveillance all outrank erasure, and the chain has to know that per holding rather than in general.

### Anchor ID
DigitalProduct::Coco::Retention Obligations

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Retention Obligations

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Retention Period Assignments

*Solution component:* `SolutionComponent::Set Retention Period::V1.0`  
*Category:* Reference Data

The retention period set on each catalogued asset: the basis it was set under and the dates on which the asset is to be archived and deleted.  It is the point at which a retention obligation becomes an instruction attached to a specific holding.

## Create Digital Product

### Display Name
Retention Period Assignments

### Product Name
Retention Period Assignments

### Qualified Name
DigitalProduct::Coco::Retention Period Assignments

### Description
The retention period set on each catalogued asset: the basis it was set under and the dates on which the asset is to be archived and deleted.  It is the point at which a retention obligation becomes an instruction attached to a specific holding.

### Purpose
Tells the retention schedule and the rights chain what has already been decided for each asset.

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
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Element Id
DigitalProduct::Coco::Retention Period Assignments

### Membership Rationale
Produced by the Privacy Operations group's `Set Retention Period` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Retention Period Assignments Data Spec

### Qualified Name
DataSpec::Coco::Retention Period Assignments

### Description
The data structures and fields that make up the Retention Period Assignments digital product.

### Purpose
Describes the data a subscriber to Retention Period Assignments receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Retention Period Assignments

### Collection Id
DataSpec::Coco::Retention Period Assignments

### Label
data specification

___

## Create Data Structure

### Display Name
Retention Period Assignment

### Qualified Name
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Description
One row per asset with a retention period set.

### Namespace Path
coco_data_hub.retention_period_assignments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Retention Period Assignments

### Element Id
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Membership Rationale
The Retention Period Assignment structure is part of the Retention Period Assignments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Asset Identifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Asset Identifier

### Description
The catalogued asset.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Asset Identifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Retention Obligation Identifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Obligation Identifier

### Description
The obligation applied.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Obligation Identifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Retention Basis Description

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Basis Description

### Description
The basis recorded on the asset.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Basis Description

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Retention Archive Date

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Archive Date

### Description
When the asset is to be archived.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Archive Date

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Retention Delete Date

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Delete Date

### Description
When it is to be deleted.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Delete Date

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Retention Assigned Timestamp

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Assigned Timestamp

### Description
When the period was set.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Assigned Timestamp

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Retention Assigner Identifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Assigner Identifier

### Description
Who set it.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::Retention Assigner Identifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

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
- schemaName: retention_period_assignments
- schemaDescription: The retention period set on each catalogued asset: the basis it was set under and the dates on which the asset is to be archived and deleted. It is the point at which a retention obligation becomes an instruction attached to a specific holding.

### Anchor ID
DigitalProduct::Coco::Retention Period Assignments

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Retention Period Assignments

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
