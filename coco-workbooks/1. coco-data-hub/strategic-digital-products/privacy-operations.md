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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

7 products, 11 data structures, 76 data fields.  This file loads after `catalog.md`.

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
coco_pharma.data_subject_rights_requests

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
RightsRequestIdentifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestIdentifier

### Description
The request.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestIdentifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 1

___

## Create Data Field

### Display Name
RightsRequestReceivedTimestamp

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestReceivedTimestamp

### Description
When first received anywhere in the company.

### Data Type
date

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestReceivedTimestamp

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 2

___

## Create Data Field

### Display Name
RightsRequestChannelType

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestChannelType

### Description
Portal, email, letter, telephone or other.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestChannelType

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 3

___

## Create Data Field

### Display Name
RightsRequestType

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestType

### Description
Access, rectification, erasure, objection, portability or restriction.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestType

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 4

___

## Create Data Field

### Display Name
DataSubjectType

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::DataSubjectType

### Description
Patient, worker, healthcare professional, other.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::DataSubjectType

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 5

___

## Create Data Field

### Display Name
DataSubjectClaimedName

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::DataSubjectClaimedName

### Description
The name the requester gave.

### Data Type
string

### Position
6

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
DataField::Coco::Data Subject Rights Requests::Rights Request::DataSubjectClaimedName

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 6

___

## Create Data Field

### Display Name
RightsRequestDescription

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestDescription

### Description
What was asked for.

### Data Type
string

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestDescription

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 7

___

## Create Data Field

### Display Name
RightsRequestDueDate

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestDueDate

### Description
The statutory deadline.

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestDueDate

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

### Label
field 8

___

## Create Data Field

### Display Name
RightsRequestCurrentStatus

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestCurrentStatus

### Description
Received, verifying, in progress, responded, closed.

### Data Type
string

### Position
9

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
DataField::Coco::Data Subject Rights Requests::Rights Request::RightsRequestCurrentStatus

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Rights Request

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
coco_pharma.data_subject_rights_requests

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
RightsRequestIdentifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestIdentifier

### Description
The request.

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
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestIdentifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Label
field 1

___

## Create Data Field

### Display Name
RightsRequestResponseTimestamp

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponseTimestamp

### Description
When the response was sent.

### Data Type
date

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
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponseTimestamp

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Label
field 2

___

## Create Data Field

### Display Name
RightsRequestResponseDescription

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponseDescription

### Description
The response, the actions taken and the reasons.

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
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponseDescription

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Label
field 3

___

## Create Data Field

### Display Name
RightsRequestResponderIdentifier

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponderIdentifier

### Description
Who sent it.

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
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestResponderIdentifier

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

### Label
field 4

___

## Create Data Field

### Display Name
RightsRequestRefusedFlag

### Qualified Name
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestRefusedFlag

### Description
Whether any part of the request was refused.

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
DataField::Coco::Data Subject Rights Requests::Request Response::RightsRequestRefusedFlag

### Data Structure
DataStructure::Coco::Data Subject Rights Requests::Request Response

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
- schemaName: data_subject_rights_requests
- schemaDescription: Requests from data subjects received through every channel the company offers, with the statutory clock that starts on receipt, and the response assembled for each. An email to a site address counts exactly as much as a submission through the portal.

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
coco_pharma.requester_identity_verifications

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
RightsRequestIdentifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestIdentifier

### Description
The request.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestIdentifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 1

___

## Create Data Field

### Display Name
RightsRequestVerifiedTimestamp

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedTimestamp

### Description
When verified.

### Data Type
date

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedTimestamp

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 2

___

## Create Data Field

### Display Name
RightsRequestVerifiedMethodCode

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedMethodCode

### Description
The method used.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedMethodCode

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 3

___

## Create Data Field

### Display Name
RightsRequestVerifiedEvidenceDescription

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedEvidenceDescription

### Description
The evidence offered and accepted.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedEvidenceDescription

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 4

___

## Create Data Field

### Display Name
RightsRequestVerifiedStatus

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedStatus

### Description
Verified, failed, insufficient.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifiedStatus

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 5

___

## Create Data Field

### Display Name
RightsRequestVerifierIdentifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifierIdentifier

### Description
Who verified.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::RightsRequestVerifierIdentifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

### Label
field 6

___

## Create Data Field

### Display Name
DataSubjectIdentifier

### Qualified Name
DataField::Coco::Requester Identity Verifications::Identity Verification::DataSubjectIdentifier

### Description
The verified subject's identifier in the relevant register.

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
DataField::Coco::Requester Identity Verifications::Identity Verification::DataSubjectIdentifier

### Data Structure
DataStructure::Coco::Requester Identity Verifications::Identity Verification

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
- schemaName: requester_identity_verifications
- schemaDescription: The verification that a requester is who they claim to be, proportionate to what they are asking for. It is the step that stops the rights process from becoming an attack on the data it is meant to protect.

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
coco_pharma.record_of_processing_activities

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
ProcessingActivityIdentifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityIdentifier

### Description
The activity.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityIdentifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 1

___

## Create Data Field

### Display Name
ProcessingActivityName

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityName

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityName

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 2

___

## Create Data Field

### Display Name
ProcessingActivityPurposeDescription

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityPurposeDescription

### Description
The purpose.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityPurposeDescription

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 3

___

## Create Data Field

### Display Name
ProcessingActivityBasisCode

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityBasisCode

### Description
The lawful basis.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityBasisCode

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 4

___

## Create Data Field

### Display Name
DataSubjectType

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::DataSubjectType

### Description
The category of data subject.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::DataSubjectType

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 5

___

## Create Data Field

### Display Name
ProcessingActivityDataDescription

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityDataDescription

### Description
The categories of personal data.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityDataDescription

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 6

___

## Create Data Field

### Display Name
ProcessingActivityOwnerIdentifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityOwnerIdentifier

### Description
The accountable owner.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityOwnerIdentifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

### Label
field 7

___

## Create Data Field

### Display Name
ProcessingActivityCurrentTimestamp

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityCurrentTimestamp

### Description
When last reviewed.

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
DataField::Coco::Record Of Processing Activities::Processing Activity::ProcessingActivityCurrentTimestamp

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing Activity

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
coco_pharma.record_of_processing_activities

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
ProcessingActivityIdentifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::ProcessingActivityIdentifier

### Description
The activity.

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
DataField::Coco::Record Of Processing Activities::Processing System::ProcessingActivityIdentifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Label
field 1

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::SystemIdentifier

### Description
The system, for internal holdings.

### Data Type
string

### Position
2

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
DataField::Coco::Record Of Processing Activities::Processing System::SystemIdentifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Label
field 2

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::SupplierIdentifier

### Description
The processor, for external holdings.

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
DataField::Coco::Record Of Processing Activities::Processing System::SupplierIdentifier

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Label
field 3

___

## Create Data Field

### Display Name
RetentionCategoryCode

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::RetentionCategoryCode

### Description
The retention category of the data held.

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
DataField::Coco::Record Of Processing Activities::Processing System::RetentionCategoryCode

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

### Label
field 4

___

## Create Data Field

### Display Name
SystemReconciledFlag

### Qualified Name
DataField::Coco::Record Of Processing Activities::Processing System::SystemReconciledFlag

### Description
Whether discovery found a discrepancy against this entry.

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
DataField::Coco::Record Of Processing Activities::Processing System::SystemReconciledFlag

### Data Structure
DataStructure::Coco::Record Of Processing Activities::Processing System

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
- schemaName: record_of_processing_activities
- schemaDescription: What personal data the company processes, for what purpose, under what lawful basis, and in which systems and processors it is held. It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.

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
coco_pharma.personal_data_discovery_findings

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
HoldingIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingIdentifier

### Description
The holding.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 1

___

## Create Data Field

### Display Name
AssetIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::AssetIdentifier

### Description
The catalogued asset.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::AssetIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 2

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::SystemIdentifier

### Description
The system.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::SystemIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 3

___

## Create Data Field

### Display Name
DataSubjectType

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::DataSubjectType

### Description
The category of data subject the data concerns.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::DataSubjectType

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 4

___

## Create Data Field

### Display Name
HoldingDataDescription

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingDataDescription

### Description
The personal data found.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingDataDescription

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 5

___

## Create Data Field

### Display Name
HoldingDiscoveredTimestamp

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingDiscoveredTimestamp

### Description
When found.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::HoldingDiscoveredTimestamp

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

### Label
field 6

___

## Create Data Field

### Display Name
ProcessingActivityIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::ProcessingActivityIdentifier

### Description
The activity it reconciles to, if any.

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
DataField::Coco::Personal Data Discovery Findings::Discovered Holding::ProcessingActivityIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Discovered Holding

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
coco_pharma.personal_data_discovery_findings

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
DiscrepancyIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyIdentifier

### Description
The discrepancy.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Label
field 1

___

## Create Data Field

### Display Name
HoldingIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::HoldingIdentifier

### Description
The holding, for data found but not registered.

### Data Type
string

### Position
2

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::HoldingIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Label
field 2

___

## Create Data Field

### Display Name
ProcessingActivityIdentifier

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::ProcessingActivityIdentifier

### Description
The activity, for data registered but not found.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::ProcessingActivityIdentifier

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Label
field 3

___

## Create Data Field

### Display Name
DiscrepancyType

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyType

### Description
Unregistered holding, missing holding, category mismatch.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyType

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Label
field 4

___

## Create Data Field

### Display Name
DiscrepancyDescription

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyDescription

### Description
The difference.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyDescription

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

### Label
field 5

___

## Create Data Field

### Display Name
DiscrepancyCurrentStatus

### Qualified Name
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyCurrentStatus

### Description
Open, register corrected, holding removed, accepted.

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
DataField::Coco::Personal Data Discovery Findings::Register Discrepancy::DiscrepancyCurrentStatus

### Data Structure
DataStructure::Coco::Personal Data Discovery Findings::Register Discrepancy

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
- schemaName: personal_data_discovery_findings
- schemaDescription: What the survey of systems and stores actually found: personal data holdings by system, and the discrepancies between them and the record of processing. The register describes what the company believes it processes; this describes what it actually holds.

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
coco_pharma.rights_fulfilment_actions

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
RightsRequestIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestIdentifier

### Description
The request.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 1

___

## Create Data Field

### Display Name
DataSubjectIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::DataSubjectIdentifier

### Description
The verified subject.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::DataSubjectIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 2

___

## Create Data Field

### Display Name
DataSubjectType

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::DataSubjectType

### Description
The category of subject.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::DataSubjectType

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 3

___

## Create Data Field

### Display Name
RightsRequestType

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestType

### Description
The right exercised.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestType

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 4

___

## Create Data Field

### Display Name
RightsRequestFulfilmentStartTimestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentStartTimestamp

### Description
When fulfilment began.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentStartTimestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 5

___

## Create Data Field

### Display Name
RightsRequestFulfilmentCount

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentCount

### Description
The number of systems and processors asked.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentCount

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

### Label
field 6

___

## Create Data Field

### Display Name
RightsRequestFulfilmentStatus

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentStatus

### Description
In progress, awaiting responses, decided, complete.

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
DataField::Coco::Rights Fulfilment Actions::Fulfilment Request::RightsRequestFulfilmentStatus

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::Fulfilment Request

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
coco_pharma.rights_fulfilment_actions

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
RightsRequestIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::RightsRequestIdentifier

### Description
The request.

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
DataField::Coco::Rights Fulfilment Actions::System Action::RightsRequestIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 1

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SystemIdentifier

### Description
The system, for internal holdings.

### Data Type
string

### Position
2

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
DataField::Coco::Rights Fulfilment Actions::System Action::SystemIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 2

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SupplierIdentifier

### Description
The processor, for external holdings.

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
DataField::Coco::Rights Fulfilment Actions::System Action::SupplierIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 3

___

## Create Data Field

### Display Name
SystemActionType

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionType

### Description
Locate, disclose, rectify, erase, restrict.

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
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionType

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 4

___

## Create Data Field

### Display Name
SystemActionRequestedTimestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionRequestedTimestamp

### Description
When asked.

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
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionRequestedTimestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 5

___

## Create Data Field

### Display Name
SystemActionCompletedTimestamp

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionCompletedTimestamp

### Description
When answered.

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
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionCompletedTimestamp

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 6

___

## Create Data Field

### Display Name
SystemActionStatus

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionStatus

### Description
Requested, completed, refused, no data held.

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
DataField::Coco::Rights Fulfilment Actions::System Action::SystemActionStatus

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

### Label
field 7

___

## Create Data Field

### Display Name
RetentionObligationIdentifier

### Qualified Name
DataField::Coco::Rights Fulfilment Actions::System Action::RetentionObligationIdentifier

### Description
The retention obligation that overrode an erasure, if any.

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
DataField::Coco::Rights Fulfilment Actions::System Action::RetentionObligationIdentifier

### Data Structure
DataStructure::Coco::Rights Fulfilment Actions::System Action

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
- schemaName: rights_fulfilment_actions
- schemaDescription: Each verified request fanned out to every system and processor holding the person's data, what came back, and the erasure, rectification and objection decisions driven onward to the systems that must act on them. It is the component that turns a register into an answer.

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
coco_pharma.retention_obligations

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
RetentionObligationIdentifier

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionObligationIdentifier

### Description
The obligation.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionObligationIdentifier

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 1

___

## Create Data Field

### Display Name
RetentionCategoryCode

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionCategoryCode

### Description
The category of data.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionCategoryCode

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 2

___

## Create Data Field

### Display Name
RetentionCategoryDescription

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionCategoryDescription

### Description
What the category covers.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionCategoryDescription

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 3

___

## Create Data Field

### Display Name
RetentionDuration

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionDuration

### Description
How long the data must be kept, in months.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionDuration

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 4

___

## Create Data Field

### Display Name
RetentionBasisDescription

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionBasisDescription

### Description
The regulation or contract that requires it.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionBasisDescription

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 5

___

## Create Data Field

### Display Name
RetentionOverridesErasureFlag

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionOverridesErasureFlag

### Description
Whether the obligation overrides a request for erasure.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionOverridesErasureFlag

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

### Label
field 6

___

## Create Data Field

### Display Name
RetentionObligationStartDate

### Qualified Name
DataField::Coco::Retention Obligations::Retention Obligation::RetentionObligationStartDate

### Description
When the obligation took effect.

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
DataField::Coco::Retention Obligations::Retention Obligation::RetentionObligationStartDate

### Data Structure
DataStructure::Coco::Retention Obligations::Retention Obligation

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
- schemaName: retention_obligations
- schemaDescription: The retention obligation attaching to each category of personal data, and the basis that lets it override a request to be forgotten. Clinical trial records, employment decisions and health surveillance all outrank erasure, and the chain has to know that per holding rather than in general.

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
coco_pharma.retention_period_assignments

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
AssetIdentifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::AssetIdentifier

### Description
The catalogued asset.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::AssetIdentifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 1

___

## Create Data Field

### Display Name
RetentionObligationIdentifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionObligationIdentifier

### Description
The obligation applied.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionObligationIdentifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 2

___

## Create Data Field

### Display Name
RetentionBasisDescription

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionBasisDescription

### Description
The basis recorded on the asset.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionBasisDescription

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 3

___

## Create Data Field

### Display Name
RetentionArchiveDate

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionArchiveDate

### Description
When the asset is to be archived.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionArchiveDate

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 4

___

## Create Data Field

### Display Name
RetentionDeleteDate

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionDeleteDate

### Description
When it is to be deleted.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionDeleteDate

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 5

___

## Create Data Field

### Display Name
RetentionAssignedTimestamp

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionAssignedTimestamp

### Description
When the period was set.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionAssignedTimestamp

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

### Label
field 6

___

## Create Data Field

### Display Name
RetentionAssignerIdentifier

### Qualified Name
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionAssignerIdentifier

### Description
Who set it.

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
DataField::Coco::Retention Period Assignments::Retention Period Assignment::RetentionAssignerIdentifier

### Data Structure
DataStructure::Coco::Retention Period Assignments::Retention Period Assignment

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
- schemaName: retention_period_assignments
- schemaDescription: The retention period set on each catalogued asset: the basis it was set under and the dates on which the asset is to be archived and deleted. It is the point at which a retention obligation becomes an instruction attached to a specific holding.

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
