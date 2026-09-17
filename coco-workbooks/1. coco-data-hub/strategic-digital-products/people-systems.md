# People Systems Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 11 digital products owned by the People Systems business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of the worker record and everything derived from it: lifecycle events, access entitlements, payroll, the directory, competency requirements, training, qualifications and their currency, and the health surveillance records that outlive employment.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Worker Master Data | `CocoPharma::SolutionComponent::WorkerMasterRegister` | Master Data | Worker, Worker Assignment |
| Worker Lifecycle Events | `CocoPharma::SolutionComponent::JoinerMoverLeaverWorkflow` | Event Stream | Worker Event, Event Distribution Status |
| Access Entitlements | `CocoPharma::SolutionComponent::IdentityAndAccessProvisioning` | Reference Data | Account, Entitlement |
| Payroll Results | `CocoPharma::SolutionComponent::PayrollSystem` | Transactional Record | Payroll Run, Payroll Posting |
| Corporate Directory Entries | `CocoPharma::SolutionComponent::CorporateDirectory` | Reference Data | Directory Entry |
| Role Competency Requirements | `CocoPharma::SolutionComponent::CompetencyFrameworkRegister` | Reference Data | Role Competency Requirement |
| Training Completions | `CocoPharma::SolutionComponent::LearningManagement` | Evidence Record | Training Completion, Assessment Result, Refresher Schedule |
| Worker Qualifications | `CocoPharma::SolutionComponent::CompetencyRegister` | Master Data | Worker Qualification |
| Qualification Expiry Warnings | `CocoPharma::SolutionComponent::QualificationCurrencyChecker` | Event Stream | Qualification Expiry Warning |
| Health Surveillance Records | `CocoPharma::SolutionComponent::HealthSurveillanceRecords` | Evidence Record | Surveillance Enrolment, Surveillance Result |
| Long Term Health Archive | `CocoPharma::SolutionComponent::LongTermHealthArchive` | Evidence Record | Archived Health Record |

For every product this file:

1. creates the **digital product** and adds it to the `People Systems` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

11 products, 18 data structures, 123 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret people-systems.md
```

---

# Worker Master Data

*Solution component:* `CocoPharma::SolutionComponent::WorkerMasterRegister`  
*Category:* Master Data

The authoritative record of every worker, employees and contractors alike, and the assignment of each to a role, an entity, a cost centre and a reporting line.  It is the anchor that qualification, health surveillance, access and payroll records are all held against.

## Create Digital Product

### Display Name
Worker Master Data

### Product Name
Worker Master Data

### Qualified Name
DigitalProduct::Coco::Worker Master Data

### Description
The authoritative record of every worker, employees and contractors alike, and the assignment of each to a role, an entity, a cost centre and a reporting line.  It is the anchor that qualification, health surveillance, access and payroll records are all held against.

### Purpose
Gives every people process one record of who a worker is, what they do and who they report to.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Worker Master Data

### Membership Rationale
Produced by the People Systems group's `WorkerMasterRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Worker Master Data Data Spec

### Qualified Name
DataSpec::Coco::Worker Master Data

### Description
The data structures and fields that make up the Worker Master Data digital product.

### Purpose
Describes the data a subscriber to Worker Master Data receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Worker Master Data

### Collection Id
DataSpec::Coco::Worker Master Data

### Label
data specification

___

## Create Data Structure

### Display Name
Worker

### Qualified Name
DataStructure::Coco::Worker Master Data::Worker

### Description
One row per worker, identified by pseudonym to every consuming system.

### Namespace Path
coco_pharma.worker_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Worker Master Data

### Element Id
DataStructure::Coco::Worker Master Data::Worker

### Membership Rationale
The Worker structure is part of the Worker Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker::WorkerPseudonymIdentifier

### Description
The worker's pseudonym.

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
DataField::Coco::Worker Master Data::Worker::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 1

___

## Create Data Field

### Display Name
WorkerType

### Qualified Name
DataField::Coco::Worker Master Data::Worker::WorkerType

### Description
Employee or contractor.

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
DataField::Coco::Worker Master Data::Worker::WorkerType

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 2

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::Worker Master Data::Worker::LegalEntityCode

### Description
The employing entity.

### Data Type
string

### Position
3

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Worker Master Data::Worker::LegalEntityCode

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 3

___

## Create Data Field

### Display Name
SiteCode

### Qualified Name
DataField::Coco::Worker Master Data::Worker::SiteCode

### Description
The primary site.

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
DataField::Coco::Worker Master Data::Worker::SiteCode

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 4

___

## Create Data Field

### Display Name
WorkerHireDate

### Qualified Name
DataField::Coco::Worker Master Data::Worker::WorkerHireDate

### Description
When the worker joined.

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
DataField::Coco::Worker Master Data::Worker::WorkerHireDate

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 5

___

## Create Data Field

### Display Name
WorkerLeaveDate

### Qualified Name
DataField::Coco::Worker Master Data::Worker::WorkerLeaveDate

### Description
When they left, once they have.

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
DataField::Coco::Worker Master Data::Worker::WorkerLeaveDate

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 6

___

## Create Data Field

### Display Name
WorkerCurrentStatus

### Qualified Name
DataField::Coco::Worker Master Data::Worker::WorkerCurrentStatus

### Description
Active, on leave, left.

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
DataField::Coco::Worker Master Data::Worker::WorkerCurrentStatus

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Label
field 7

___

## Create Data Structure

### Display Name
Worker Assignment

### Qualified Name
DataStructure::Coco::Worker Master Data::Worker Assignment

### Description
One row per worker, their current role, cost centre and reporting line.

### Namespace Path
coco_pharma.worker_master_data

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Worker Master Data

### Element Id
DataStructure::Coco::Worker Master Data::Worker Assignment

### Membership Rationale
The Worker Assignment structure is part of the Worker Master Data data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Worker Master Data::Worker Assignment::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 1

___

## Create Data Field

### Display Name
RoleCode

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::RoleCode

### Description
The role.

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
DataField::Coco::Worker Master Data::Worker Assignment::RoleCode

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 2

___

## Create Data Field

### Display Name
RoleName

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::RoleName

### Description
The role's name.

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
DataField::Coco::Worker Master Data::Worker Assignment::RoleName

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 3

___

## Create Data Field

### Display Name
CostCentreCode

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::CostCentreCode

### Description
The cost centre.

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
DataField::Coco::Worker Master Data::Worker Assignment::CostCentreCode

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 4

___

## Create Data Field

### Display Name
ManagerPseudonymIdentifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::ManagerPseudonymIdentifier

### Description
The reporting manager.

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
DataField::Coco::Worker Master Data::Worker Assignment::ManagerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 5

___

## Create Data Field

### Display Name
WorkerAssignmentStartDate

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::WorkerAssignmentStartDate

### Description
When the assignment began.

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
DataField::Coco::Worker Master Data::Worker Assignment::WorkerAssignmentStartDate

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 6

___

## Create Data Field

### Display Name
WorkerSpendingMaximumAmount

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::WorkerSpendingMaximumAmount

### Description
The worker's spending authority.

### Data Type
bigdecimal

### Position
7

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
DataField::Coco::Worker Master Data::Worker Assignment::WorkerSpendingMaximumAmount

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Label
field 7

___

## Create Data Field

### Display Name
WorkerHazardProfileDescription

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::WorkerHazardProfileDescription

### Description
The substances and tasks the role exposes the worker to.

### Data Type
string

### Position
8

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
DataField::Coco::Worker Master Data::Worker Assignment::WorkerHazardProfileDescription

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

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
- schemaName: worker_master_data
- schemaDescription: The authoritative record of every worker, employees and contractors alike, and the assignment of each to a role, an entity, a cost centre and a reporting line. It is the anchor that qualification, health surveillance, access and payroll records are all held against.

### Parent ID
DigitalProduct::Coco::Worker Master Data

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Worker Lifecycle Events

*Solution component:* `CocoPharma::SolutionComponent::JoinerMoverLeaverWorkflow`  
*Category:* Event Stream

Every joining, moving or leaving event, distributed to each system that must act on it, and the record of which have.  The leaver case is the one that matters: access outlives employment by exactly this chain's delay.

## Create Digital Product

### Display Name
Worker Lifecycle Events

### Product Name
Worker Lifecycle Events

### Qualified Name
DigitalProduct::Coco::Worker Lifecycle Events

### Description
Every joining, moving or leaving event, distributed to each system that must act on it, and the record of which have.  The leaver case is the one that matters: access outlives employment by exactly this chain's delay.

### Purpose
Makes the latency between a worker event and every system acting on it measurable, system by system.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Worker Lifecycle Events

### Membership Rationale
Produced by the People Systems group's `JoinerMoverLeaverWorkflow` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Worker Lifecycle Events Data Spec

### Qualified Name
DataSpec::Coco::Worker Lifecycle Events

### Description
The data structures and fields that make up the Worker Lifecycle Events digital product.

### Purpose
Describes the data a subscriber to Worker Lifecycle Events receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Worker Lifecycle Events

### Collection Id
DataSpec::Coco::Worker Lifecycle Events

### Label
data specification

___

## Create Data Structure

### Display Name
Worker Event

### Qualified Name
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Description
One row per joiner, mover or leaver event.

### Namespace Path
coco_pharma.worker_lifecycle_events

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Worker Lifecycle Events

### Element Id
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Membership Rationale
The Worker Event structure is part of the Worker Lifecycle Events data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerEventIdentifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventIdentifier

### Description
The event.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventIdentifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 2

___

## Create Data Field

### Display Name
WorkerEventType

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventType

### Description
Joiner, mover or leaver.

### Data Type
string

### Position
3

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventType

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 3

___

## Create Data Field

### Display Name
WorkerEventStartDate

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventStartDate

### Description
The effective date.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventStartDate

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 4

___

## Create Data Field

### Display Name
WorkerEventRaisedTimestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventRaisedTimestamp

### Description
When the event was raised.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventRaisedTimestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 5

___

## Create Data Field

### Display Name
RoleCode

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::RoleCode

### Description
The new role, for a joiner or mover.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::RoleCode

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 6

___

## Create Data Field

### Display Name
WorkerEventDescription

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventDescription

### Description
The change.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::WorkerEventDescription

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Label
field 7

___

## Create Data Structure

### Display Name
Event Distribution Status

### Qualified Name
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Description
One row per event per consuming system.

### Namespace Path
coco_pharma.worker_lifecycle_events

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Worker Lifecycle Events

### Element Id
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Membership Rationale
The Event Distribution Status structure is part of the Worker Lifecycle Events data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerEventIdentifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventIdentifier

### Description
The event.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventIdentifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Label
field 1

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::SystemIdentifier

### Description
The system notified.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::SystemIdentifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Label
field 2

___

## Create Data Field

### Display Name
WorkerEventSentTimestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventSentTimestamp

### Description
When notified.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventSentTimestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Label
field 3

___

## Create Data Field

### Display Name
WorkerEventAppliedFlag

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventAppliedFlag

### Description
Whether the system has confirmed acting on it.

### Data Type
boolean

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventAppliedFlag

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Label
field 4

___

## Create Data Field

### Display Name
WorkerEventAppliedTimestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventAppliedTimestamp

### Description
When confirmed.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::WorkerEventAppliedTimestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

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
- schemaName: worker_lifecycle_events
- schemaDescription: Every joining, moving or leaving event, distributed to each system that must act on it, and the record of which have. The leaver case is the one that matters: access outlives employment by exactly this chain's delay.

### Parent ID
DigitalProduct::Coco::Worker Lifecycle Events

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Access Entitlements

*Solution component:* `CocoPharma::SolutionComponent::IdentityAndAccessProvisioning`  
*Category:* Reference Data

The accounts and entitlements created, changed and removed for each worker in response to worker events, and the data ownership assignments recorded in the open metadata catalogue.  It is driven from the worker record rather than from requests, because an access removal that depends on somebody remembering to ask does not happen.

## Create Digital Product

### Display Name
Access Entitlements

### Product Name
Access Entitlements

### Qualified Name
DigitalProduct::Coco::Access Entitlements

### Description
The accounts and entitlements created, changed and removed for each worker in response to worker events, and the data ownership assignments recorded in the open metadata catalogue.  It is driven from the worker record rather than from requests, because an access removal that depends on somebody remembering to ask does not happen.

### Purpose
Shows, for every worker, what they can access now and when it was granted or revoked.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Access Entitlements

### Membership Rationale
Produced by the People Systems group's `IdentityAndAccessProvisioning` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Access Entitlements Data Spec

### Qualified Name
DataSpec::Coco::Access Entitlements

### Description
The data structures and fields that make up the Access Entitlements digital product.

### Purpose
Describes the data a subscriber to Access Entitlements receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Access Entitlements

### Collection Id
DataSpec::Coco::Access Entitlements

### Label
data specification

___

## Create Data Structure

### Display Name
Account

### Qualified Name
DataStructure::Coco::Access Entitlements::Account

### Description
One row per account held by a worker in a system.

### Namespace Path
coco_pharma.access_entitlements

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Access Entitlements

### Element Id
DataStructure::Coco::Access Entitlements::Account

### Membership Rationale
The Account structure is part of the Access Entitlements data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
UserAccountIdentifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::UserAccountIdentifier

### Description
The account.

### Data Type
string

### Position
1

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
DataField::Coco::Access Entitlements::Account::UserAccountIdentifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Access Entitlements::Account::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 2

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::SystemIdentifier

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
DataField::Coco::Access Entitlements::Account::SystemIdentifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 3

___

## Create Data Field

### Display Name
UserAccountStartDate

### Qualified Name
DataField::Coco::Access Entitlements::Account::UserAccountStartDate

### Description
When created.

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
DataField::Coco::Access Entitlements::Account::UserAccountStartDate

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 4

___

## Create Data Field

### Display Name
UserAccountEndDate

### Qualified Name
DataField::Coco::Access Entitlements::Account::UserAccountEndDate

### Description
When removed, once removed.

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
DataField::Coco::Access Entitlements::Account::UserAccountEndDate

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 5

___

## Create Data Field

### Display Name
UserAccountCurrentStatus

### Qualified Name
DataField::Coco::Access Entitlements::Account::UserAccountCurrentStatus

### Description
Active, suspended, removed.

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
DataField::Coco::Access Entitlements::Account::UserAccountCurrentStatus

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 6

___

## Create Data Field

### Display Name
WorkerEventIdentifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::WorkerEventIdentifier

### Description
The worker event that last changed it.

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
DataField::Coco::Access Entitlements::Account::WorkerEventIdentifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Label
field 7

___

## Create Data Structure

### Display Name
Entitlement

### Qualified Name
DataStructure::Coco::Access Entitlements::Entitlement

### Description
One row per entitlement granted to an account.

### Namespace Path
coco_pharma.access_entitlements

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Access Entitlements

### Element Id
DataStructure::Coco::Access Entitlements::Entitlement

### Membership Rationale
The Entitlement structure is part of the Access Entitlements data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
UserAccountIdentifier

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::UserAccountIdentifier

### Description
The account.

### Data Type
string

### Position
1

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
DataField::Coco::Access Entitlements::Entitlement::UserAccountIdentifier

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Label
field 1

___

## Create Data Field

### Display Name
EntitlementCode

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::EntitlementCode

### Description
The entitlement.

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
DataField::Coco::Access Entitlements::Entitlement::EntitlementCode

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Label
field 2

___

## Create Data Field

### Display Name
EntitlementDescription

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::EntitlementDescription

### Description
What it permits.

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
DataField::Coco::Access Entitlements::Entitlement::EntitlementDescription

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Label
field 3

___

## Create Data Field

### Display Name
EntitlementStartDate

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::EntitlementStartDate

### Description
When granted.

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
DataField::Coco::Access Entitlements::Entitlement::EntitlementStartDate

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Label
field 4

___

## Create Data Field

### Display Name
EntitlementEndDate

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::EntitlementEndDate

### Description
When revoked, once revoked.

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
DataField::Coco::Access Entitlements::Entitlement::EntitlementEndDate

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Label
field 5

___

## Create Data Field

### Display Name
EntitlementDataOwnerFlag

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::EntitlementDataOwnerFlag

### Description
Whether the entitlement makes the worker a data owner in the catalogue.

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
DataField::Coco::Access Entitlements::Entitlement::EntitlementDataOwnerFlag

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

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
- schemaName: access_entitlements
- schemaDescription: The accounts and entitlements created, changed and removed for each worker in response to worker events, and the data ownership assignments recorded in the open metadata catalogue. It is driven from the worker record rather than from requests, because an access removal that depends on somebody remembering to ask does not happen.

### Parent ID
DigitalProduct::Coco::Access Entitlements

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Payroll Results

*Solution component:* `CocoPharma::SolutionComponent::PayrollSystem`  
*Category:* Transactional Record

The remuneration calculated and paid in each payroll run, in several countries under several sets of rules from one worker record, and the postings to the ledger by entity.  It is the pay data that statutory reporting and pay equity analysis are built from.

## Create Digital Product

### Display Name
Payroll Results

### Product Name
Payroll Results

### Qualified Name
DigitalProduct::Coco::Payroll Results

### Description
The remuneration calculated and paid in each payroll run, in several countries under several sets of rules from one worker record, and the postings to the ledger by entity.  It is the pay data that statutory reporting and pay equity analysis are built from.

### Purpose
Provides the ledger with payroll postings by entity and the analysts with pay data by worker.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Payroll Results

### Membership Rationale
Produced by the People Systems group's `PayrollSystem` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Payroll Results Data Spec

### Qualified Name
DataSpec::Coco::Payroll Results

### Description
The data structures and fields that make up the Payroll Results digital product.

### Purpose
Describes the data a subscriber to Payroll Results receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Payroll Results

### Collection Id
DataSpec::Coco::Payroll Results

### Label
data specification

___

## Create Data Structure

### Display Name
Payroll Run

### Qualified Name
DataStructure::Coco::Payroll Results::Payroll Run

### Description
One row per payroll run.

### Namespace Path
coco_pharma.payroll_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Payroll Results

### Element Id
DataStructure::Coco::Payroll Results::Payroll Run

### Membership Rationale
The Payroll Run structure is part of the Payroll Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
PayrollRunIdentifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollRunIdentifier

### Description
The run.

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
DataField::Coco::Payroll Results::Payroll Run::PayrollRunIdentifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 1

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::LegalEntityCode

### Description
The entity paid.

### Data Type
string

### Position
2

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payroll Results::Payroll Run::LegalEntityCode

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 2

___

## Create Data Field

### Display Name
PayrollPeriodCode

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollPeriodCode

### Description
The pay period.

### Data Type
string

### Position
3

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payroll Results::Payroll Run::PayrollPeriodCode

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 3

___

## Create Data Field

### Display Name
PayrollRunDate

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollRunDate

### Description
When run.

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
DataField::Coco::Payroll Results::Payroll Run::PayrollRunDate

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 4

___

## Create Data Field

### Display Name
PayrollRunCount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollRunCount

### Description
The number of workers paid.

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
DataField::Coco::Payroll Results::Payroll Run::PayrollRunCount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 5

___

## Create Data Field

### Display Name
PayrollRunTotalAmount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollRunTotalAmount

### Description
The total remuneration.

### Data Type
bigdecimal

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
DataField::Coco::Payroll Results::Payroll Run::PayrollRunTotalAmount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 6

___

## Create Data Field

### Display Name
PayrollCurrencyCode

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::PayrollCurrencyCode

### Description
The currency.

### Data Type
string

### Position
7

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
DataField::Coco::Payroll Results::Payroll Run::PayrollCurrencyCode

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Label
field 7

___

## Create Data Structure

### Display Name
Payroll Posting

### Qualified Name
DataStructure::Coco::Payroll Results::Payroll Posting

### Description
One row per worker per run, the remuneration and employer costs.

### Namespace Path
coco_pharma.payroll_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Payroll Results

### Element Id
DataStructure::Coco::Payroll Results::Payroll Posting

### Membership Rationale
The Payroll Posting structure is part of the Payroll Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
PayrollRunIdentifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::PayrollRunIdentifier

### Description
The run.

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
DataField::Coco::Payroll Results::Payroll Posting::PayrollRunIdentifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Payroll Results::Payroll Posting::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 2

___

## Create Data Field

### Display Name
PayrollGrossAmount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::PayrollGrossAmount

### Description
Gross remuneration.

### Data Type
bigdecimal

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
DataField::Coco::Payroll Results::Payroll Posting::PayrollGrossAmount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 3

___

## Create Data Field

### Display Name
PayrollEmployerAmount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::PayrollEmployerAmount

### Description
Employer costs.

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
DataField::Coco::Payroll Results::Payroll Posting::PayrollEmployerAmount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 4

___

## Create Data Field

### Display Name
PayrollNetAmount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::PayrollNetAmount

### Description
Net paid.

### Data Type
bigdecimal

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
DataField::Coco::Payroll Results::Payroll Posting::PayrollNetAmount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 5

___

## Create Data Field

### Display Name
CostCentreCode

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::CostCentreCode

### Description
The cost centre charged.

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
DataField::Coco::Payroll Results::Payroll Posting::CostCentreCode

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Label
field 6

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::LedgerAccountCode

### Description
The account posted to.

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
DataField::Coco::Payroll Results::Payroll Posting::LedgerAccountCode

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

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
- schemaName: payroll_results
- schemaDescription: The remuneration calculated and paid in each payroll run, in several countries under several sets of rules from one worker record, and the postings to the ledger by entity. It is the pay data that statutory reporting and pay equity analysis are built from.

### Parent ID
DigitalProduct::Coco::Payroll Results

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Corporate Directory Entries

*Solution component:* `CocoPharma::SolutionComponent::CorporateDirectory`  
*Category:* Reference Data

The searchable directory of people, roles, locations and reporting lines that the rest of the organisation uses.  It is downstream of the worker record and is frequently the first place a stale joiner or leaver event becomes visible to everybody.

## Create Digital Product

### Display Name
Corporate Directory Entries

### Product Name
Corporate Directory Entries

### Qualified Name
DigitalProduct::Coco::Corporate Directory Entries

### Description
The searchable directory of people, roles, locations and reporting lines that the rest of the organisation uses.  It is downstream of the worker record and is frequently the first place a stale joiner or leaver event becomes visible to everybody.

### Purpose
Gives the organisation a current view of who does what and where, derived from the worker record.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Corporate Directory Entries

### Membership Rationale
Produced by the People Systems group's `CorporateDirectory` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Corporate Directory Entries Data Spec

### Qualified Name
DataSpec::Coco::Corporate Directory Entries

### Description
The data structures and fields that make up the Corporate Directory Entries digital product.

### Purpose
Describes the data a subscriber to Corporate Directory Entries receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Corporate Directory Entries

### Collection Id
DataSpec::Coco::Corporate Directory Entries

### Label
data specification

___

## Create Data Structure

### Display Name
Directory Entry

### Qualified Name
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Description
One row per worker in the directory.

### Namespace Path
coco_pharma.corporate_directory_entries

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Corporate Directory Entries

### Element Id
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Membership Rationale
The Directory Entry structure is part of the Corporate Directory Entries data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 1

___

## Create Data Field

### Display Name
PersonFirstName

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonFirstName

### Description
Given name.

### Data Type
string

### Position
2

### Is Nullable
false

### Minimum Cardinality
1

### Length
80

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonFirstName

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 2

___

## Create Data Field

### Display Name
PersonLastName

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonLastName

### Description
Family name.

### Data Type
string

### Position
3

### Is Nullable
false

### Minimum Cardinality
1

### Length
80

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonLastName

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 3

___

## Create Data Field

### Display Name
RoleName

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::RoleName

### Description
The role.

### Data Type
string

### Position
4

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
DataField::Coco::Corporate Directory Entries::Directory Entry::RoleName

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 4

___

## Create Data Field

### Display Name
DepartmentName

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::DepartmentName

### Description
The department.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::DepartmentName

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 5

___

## Create Data Field

### Display Name
SiteCode

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::SiteCode

### Description
The location.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::SiteCode

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 6

___

## Create Data Field

### Display Name
ManagerPseudonymIdentifier

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::ManagerPseudonymIdentifier

### Description
The reporting manager.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::ManagerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 7

___

## Create Data Field

### Display Name
PersonWorkPhoneNumber

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonWorkPhoneNumber

### Description
Work telephone.

### Data Type
string

### Position
8

### Is Nullable
true

### Minimum Cardinality
0

### Length
30

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Corporate Directory Entries::Directory Entry::PersonWorkPhoneNumber

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Label
field 8

___

## Create Data Field

### Display Name
DirectoryEntryCurrentTimestamp

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::DirectoryEntryCurrentTimestamp

### Description
When the entry was last updated from the worker record.

### Data Type
date

### Position
9

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
DataField::Coco::Corporate Directory Entries::Directory Entry::DirectoryEntryCurrentTimestamp

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: corporate_directory_entries
- schemaDescription: The searchable directory of people, roles, locations and reporting lines that the rest of the organisation uses. It is downstream of the worker record and is frequently the first place a stale joiner or leaver event becomes visible to everybody.

### Parent ID
DigitalProduct::Coco::Corporate Directory Entries

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Role Competency Requirements

*Solution component:* `CocoPharma::SolutionComponent::CompetencyFrameworkRegister`  
*Category:* Reference Data

What competencies each regulated role requires and how often each must be refreshed.  It is the specification the competency chain is judged against, and it changes when a process or a regulation changes rather than when a person does.

## Create Digital Product

### Display Name
Role Competency Requirements

### Product Name
Role Competency Requirements

### Qualified Name
DigitalProduct::Coco::Role Competency Requirements

### Description
What competencies each regulated role requires and how often each must be refreshed.  It is the specification the competency chain is judged against, and it changes when a process or a regulation changes rather than when a person does.

### Purpose
Tells learning management what each role must be trained in and how often.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Role Competency Requirements

### Membership Rationale
Produced by the People Systems group's `CompetencyFrameworkRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Role Competency Requirements Data Spec

### Qualified Name
DataSpec::Coco::Role Competency Requirements

### Description
The data structures and fields that make up the Role Competency Requirements digital product.

### Purpose
Describes the data a subscriber to Role Competency Requirements receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Role Competency Requirements

### Collection Id
DataSpec::Coco::Role Competency Requirements

### Label
data specification

___

## Create Data Structure

### Display Name
Role Competency Requirement

### Qualified Name
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Description
One row per role per competency required.

### Namespace Path
coco_pharma.role_competency_requirements

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Role Competency Requirements

### Element Id
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Membership Rationale
The Role Competency Requirement structure is part of the Role Competency Requirements data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
RoleCode

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::RoleCode

### Description
The role.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::RoleCode

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 1

___

## Create Data Field

### Display Name
CompetencyCode

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyCode

### Description
The competency.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyCode

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 2

___

## Create Data Field

### Display Name
CompetencyName

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyName

### Description
Its name.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyName

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 3

___

## Create Data Field

### Display Name
CompetencyDescription

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyDescription

### Description
What the competency covers.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyDescription

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 4

___

## Create Data Field

### Display Name
CompetencyRefreshDuration

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyRefreshDuration

### Description
How often it must be refreshed, in months.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyRefreshDuration

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 5

___

## Create Data Field

### Display Name
CompetencyRegulatedFlag

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyRegulatedFlag

### Description
Whether a regulation requires it.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::CompetencyRegulatedFlag

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Label
field 6

___

## Create Data Field

### Display Name
RoleRequirementStartDate

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::RoleRequirementStartDate

### Description
When the requirement took effect.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::RoleRequirementStartDate

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

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
- schemaName: role_competency_requirements
- schemaDescription: What competencies each regulated role requires and how often each must be refreshed. It is the specification the competency chain is judged against, and it changes when a process or a regulation changes rather than when a person does.

### Parent ID
DigitalProduct::Coco::Role Competency Requirements

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Training Completions

*Solution component:* `CocoPharma::SolutionComponent::LearningManagement`  
*Category:* Evidence Record

Training delivered, completion and assessment recorded, and refreshers scheduled for lapsing qualifications.  Its output is evidence consumed by two regulated processes, which is a heavier duty than the system was originally bought for.

## Create Digital Product

### Display Name
Training Completions

### Product Name
Training Completions

### Qualified Name
DigitalProduct::Coco::Training Completions

### Description
Training delivered, completion and assessment recorded, and refreshers scheduled for lapsing qualifications.  Its output is evidence consumed by two regulated processes, which is a heavier duty than the system was originally bought for.

### Purpose
Provides the competency register with the evidence that a worker completed and passed the training a competency requires.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Training Completions

### Membership Rationale
Produced by the People Systems group's `LearningManagement` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Training Completions Data Spec

### Qualified Name
DataSpec::Coco::Training Completions

### Description
The data structures and fields that make up the Training Completions digital product.

### Purpose
Describes the data a subscriber to Training Completions receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Training Completions

### Collection Id
DataSpec::Coco::Training Completions

### Label
data specification

___

## Create Data Structure

### Display Name
Training Completion

### Qualified Name
DataStructure::Coco::Training Completions::Training Completion

### Description
One row per worker per training course completed.

### Namespace Path
coco_pharma.training_completions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Training Completions

### Element Id
DataStructure::Coco::Training Completions::Training Completion

### Membership Rationale
The Training Completion structure is part of the Training Completions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
TrainingCompletionIdentifier

### Qualified Name
DataField::Coco::Training Completions::Training Completion::TrainingCompletionIdentifier

### Description
The completion.

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
DataField::Coco::Training Completions::Training Completion::TrainingCompletionIdentifier

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Training Completions::Training Completion::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Training Completions::Training Completion::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 2

___

## Create Data Field

### Display Name
TrainingCourseCode

### Qualified Name
DataField::Coco::Training Completions::Training Completion::TrainingCourseCode

### Description
The course.

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
DataField::Coco::Training Completions::Training Completion::TrainingCourseCode

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 3

___

## Create Data Field

### Display Name
CompetencyCode

### Qualified Name
DataField::Coco::Training Completions::Training Completion::CompetencyCode

### Description
The competency the course evidences.

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
DataField::Coco::Training Completions::Training Completion::CompetencyCode

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 4

___

## Create Data Field

### Display Name
TrainingCompletedDate

### Qualified Name
DataField::Coco::Training Completions::Training Completion::TrainingCompletedDate

### Description
When completed.

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
DataField::Coco::Training Completions::Training Completion::TrainingCompletedDate

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 5

___

## Create Data Field

### Display Name
TrainingExpiryDate

### Qualified Name
DataField::Coco::Training Completions::Training Completion::TrainingExpiryDate

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
DataField::Coco::Training Completions::Training Completion::TrainingExpiryDate

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Label
field 6

___

## Create Data Structure

### Display Name
Assessment Result

### Qualified Name
DataStructure::Coco::Training Completions::Assessment Result

### Description
One row per assessment taken.

### Namespace Path
coco_pharma.training_completions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Training Completions

### Element Id
DataStructure::Coco::Training Completions::Assessment Result

### Membership Rationale
The Assessment Result structure is part of the Training Completions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
TrainingCompletionIdentifier

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::TrainingCompletionIdentifier

### Description
The completion assessed.

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
DataField::Coco::Training Completions::Assessment Result::TrainingCompletionIdentifier

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Label
field 1

___

## Create Data Field

### Display Name
TrainingAssessmentDate

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentDate

### Description
When assessed.

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
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentDate

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Label
field 2

___

## Create Data Field

### Display Name
TrainingAssessmentValue

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentValue

### Description
The score.

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
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentValue

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Label
field 3

___

## Create Data Field

### Display Name
TrainingAssessmentMinimumValue

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentMinimumValue

### Description
The pass mark.

### Data Type
float

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
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentMinimumValue

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Label
field 4

___

## Create Data Field

### Display Name
TrainingAssessmentPassedFlag

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentPassedFlag

### Description
Whether the worker passed.

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
DataField::Coco::Training Completions::Assessment Result::TrainingAssessmentPassedFlag

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Label
field 5

___

## Create Data Structure

### Display Name
Refresher Schedule

### Qualified Name
DataStructure::Coco::Training Completions::Refresher Schedule

### Description
One row per refresher scheduled for a lapsing qualification.

### Namespace Path
coco_pharma.training_completions

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Training Completions

### Element Id
DataStructure::Coco::Training Completions::Refresher Schedule

### Membership Rationale
The Refresher Schedule structure is part of the Training Completions data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Training Completions::Refresher Schedule::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Label
field 1

___

## Create Data Field

### Display Name
CompetencyCode

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::CompetencyCode

### Description
The competency lapsing.

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
DataField::Coco::Training Completions::Refresher Schedule::CompetencyCode

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Label
field 2

___

## Create Data Field

### Display Name
TrainingCourseCode

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::TrainingCourseCode

### Description
The refresher course.

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
DataField::Coco::Training Completions::Refresher Schedule::TrainingCourseCode

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Label
field 3

___

## Create Data Field

### Display Name
TrainingDueDate

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::TrainingDueDate

### Description
When it must be completed.

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
DataField::Coco::Training Completions::Refresher Schedule::TrainingDueDate

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Label
field 4

___

## Create Data Field

### Display Name
TrainingScheduledDate

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::TrainingScheduledDate

### Description
When it is scheduled.

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
DataField::Coco::Training Completions::Refresher Schedule::TrainingScheduledDate

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

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
- schemaName: training_completions
- schemaDescription: Training delivered, completion and assessment recorded, and refreshers scheduled for lapsing qualifications. Its output is evidence consumed by two regulated processes, which is a heavier duty than the system was originally bought for.

### Parent ID
DigitalProduct::Coco::Training Completions

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Worker Qualifications

*Solution component:* `CocoPharma::SolutionComponent::CompetencyRegister`  
*Category:* Master Data

The authoritative statement of what each worker is currently qualified to do, with the evidence and the expiry, read by manufacturing, shipping, drug development and the batch record as compliance evidence.  A local copy that has drifted is worse than no copy at all.

## Create Digital Product

### Display Name
Worker Qualifications

### Product Name
Worker Qualifications

### Qualified Name
DigitalProduct::Coco::Worker Qualifications

### Description
The authoritative statement of what each worker is currently qualified to do, with the evidence and the expiry, read by manufacturing, shipping, drug development and the batch record as compliance evidence.  A local copy that has drifted is worse than no copy at all.

### Purpose
Answers, at the point of use, whether a worker is qualified to perform a regulated task now.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Worker Qualifications

### Membership Rationale
Produced by the People Systems group's `CompetencyRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Worker Qualifications Data Spec

### Qualified Name
DataSpec::Coco::Worker Qualifications

### Description
The data structures and fields that make up the Worker Qualifications digital product.

### Purpose
Describes the data a subscriber to Worker Qualifications receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Worker Qualifications

### Collection Id
DataSpec::Coco::Worker Qualifications

### Label
data specification

___

## Create Data Structure

### Display Name
Worker Qualification

### Qualified Name
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Description
One row per worker per competency held.

### Namespace Path
coco_pharma.worker_qualifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Worker Qualifications

### Element Id
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Membership Rationale
The Worker Qualification structure is part of the Worker Qualifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Worker Qualifications::Worker Qualification::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 1

___

## Create Data Field

### Display Name
CompetencyCode

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::CompetencyCode

### Description
The competency.

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
DataField::Coco::Worker Qualifications::Worker Qualification::CompetencyCode

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 2

___

## Create Data Field

### Display Name
CompetencyName

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::CompetencyName

### Description
Its name.

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
DataField::Coco::Worker Qualifications::Worker Qualification::CompetencyName

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 3

___

## Create Data Field

### Display Name
QualificationStartDate

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationStartDate

### Description
When gained.

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
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationStartDate

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 4

___

## Create Data Field

### Display Name
QualificationExpiryDate

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationExpiryDate

### Description
When it lapses.

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
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationExpiryDate

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 5

___

## Create Data Field

### Display Name
QualificationCurrentStatus

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationCurrentStatus

### Description
Current, lapsing, lapsed.

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
DataField::Coco::Worker Qualifications::Worker Qualification::QualificationCurrentStatus

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 6

___

## Create Data Field

### Display Name
TrainingCompletionIdentifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::TrainingCompletionIdentifier

### Description
The training completion that evidences it.

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
DataField::Coco::Worker Qualifications::Worker Qualification::TrainingCompletionIdentifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 7

___

## Create Data Field

### Display Name
CertificateIdentifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::CertificateIdentifier

### Description
The external certificate, where one exists.

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
DataField::Coco::Worker Qualifications::Worker Qualification::CertificateIdentifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Label
field 8

___

## Create Data Field

### Display Name
RoleCode

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::RoleCode

### Description
The role the qualification was gained for.

### Data Type
string

### Position
9

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
DataField::Coco::Worker Qualifications::Worker Qualification::RoleCode

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: worker_qualifications
- schemaDescription: The authoritative statement of what each worker is currently qualified to do, with the evidence and the expiry, read by manufacturing, shipping, drug development and the batch record as compliance evidence. A local copy that has drifted is worse than no copy at all.

### Parent ID
DigitalProduct::Coco::Worker Qualifications

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Qualification Expiry Warnings

*Solution component:* `CocoPharma::SolutionComponent::QualificationCurrencyChecker`  
*Category:* Event Stream

Warnings raised for qualifications approaching or past expiry, sent to the processes that depend on them before rather than after.  Currency is the property the competency chain is actually judged on.

## Create Digital Product

### Display Name
Qualification Expiry Warnings

### Product Name
Qualification Expiry Warnings

### Qualified Name
DigitalProduct::Coco::Qualification Expiry Warnings

### Description
Warnings raised for qualifications approaching or past expiry, sent to the processes that depend on them before rather than after.  Currency is the property the competency chain is actually judged on.

### Purpose
Tells learning management, before a qualification lapses, which worker needs which refresher by when.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Qualification Expiry Warnings

### Membership Rationale
Produced by the People Systems group's `QualificationCurrencyChecker` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Qualification Expiry Warnings Data Spec

### Qualified Name
DataSpec::Coco::Qualification Expiry Warnings

### Description
The data structures and fields that make up the Qualification Expiry Warnings digital product.

### Purpose
Describes the data a subscriber to Qualification Expiry Warnings receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Qualification Expiry Warnings

### Collection Id
DataSpec::Coco::Qualification Expiry Warnings

### Label
data specification

___

## Create Data Structure

### Display Name
Qualification Expiry Warning

### Qualified Name
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Description
One row per warning raised.

### Namespace Path
coco_pharma.qualification_expiry_warnings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Qualification Expiry Warnings

### Element Id
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Membership Rationale
The Qualification Expiry Warning structure is part of the Qualification Expiry Warnings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
QualificationWarningIdentifier

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningIdentifier

### Description
The warning.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningIdentifier

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 2

___

## Create Data Field

### Display Name
CompetencyCode

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::CompetencyCode

### Description
The competency.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::CompetencyCode

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 3

___

## Create Data Field

### Display Name
QualificationExpiryDate

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationExpiryDate

### Description
When it lapses.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationExpiryDate

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 4

___

## Create Data Field

### Display Name
QualificationWarningRaisedTimestamp

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningRaisedTimestamp

### Description
When the warning was raised.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningRaisedTimestamp

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 5

___

## Create Data Field

### Display Name
QualificationWarningType

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningType

### Description
Approaching expiry or expired.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::QualificationWarningType

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Label
field 6

___

## Create Data Field

### Display Name
TrainingDueDate

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::TrainingDueDate

### Description
The deadline set for the refresher.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::TrainingDueDate

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

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
- schemaName: qualification_expiry_warnings
- schemaDescription: Warnings raised for qualifications approaching or past expiry, sent to the processes that depend on them before rather than after. Currency is the property the competency chain is actually judged on.

### Parent ID
DigitalProduct::Coco::Qualification Expiry Warnings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Health Surveillance Records

*Solution component:* `CocoPharma::SolutionComponent::HealthSurveillanceRecords`  
*Category:* Evidence Record

The enrolment of each worker in health surveillance according to their exposure profile, and the results of surveillance appointments, exposure measurements and exposure incidents held against the individual.  The record belongs to the person it describes rather than to the company.

## Create Digital Product

### Display Name
Health Surveillance Records

### Product Name
Health Surveillance Records

### Qualified Name
DigitalProduct::Coco::Health Surveillance Records

### Description
The enrolment of each worker in health surveillance according to their exposure profile, and the results of surveillance appointments, exposure measurements and exposure incidents held against the individual.  The record belongs to the person it describes rather than to the company.

### Purpose
Holds each worker's surveillance history in a form that can be released to them and archived for forty years.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Health Surveillance Records

### Membership Rationale
Produced by the People Systems group's `HealthSurveillanceRecords` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Health Surveillance Records Data Spec

### Qualified Name
DataSpec::Coco::Health Surveillance Records

### Description
The data structures and fields that make up the Health Surveillance Records digital product.

### Purpose
Describes the data a subscriber to Health Surveillance Records receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Health Surveillance Records

### Collection Id
DataSpec::Coco::Health Surveillance Records

### Label
data specification

___

## Create Data Structure

### Display Name
Surveillance Enrolment

### Qualified Name
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Description
One row per worker enrolled in surveillance.

### Namespace Path
coco_pharma.health_surveillance_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Health Surveillance Records

### Element Id
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Membership Rationale
The Surveillance Enrolment structure is part of the Health Surveillance Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 1

___

## Create Data Field

### Display Name
SurveillanceEnrollmentDate

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceEnrollmentDate

### Description
When enrolled.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceEnrollmentDate

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 2

___

## Create Data Field

### Display Name
RoleCode

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::RoleCode

### Description
The role that required enrolment.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::RoleCode

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 3

___

## Create Data Field

### Display Name
WorkerHazardProfileDescription

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::WorkerHazardProfileDescription

### Description
The exposure profile enrolment was based on.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::WorkerHazardProfileDescription

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 4

___

## Create Data Field

### Display Name
SurveillanceFrequency

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceFrequency

### Description
How often appointments are due, in months.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceFrequency

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 5

___

## Create Data Field

### Display Name
SurveillanceCurrentStatus

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceCurrentStatus

### Description
Enrolled, lapsed, ended.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::SurveillanceCurrentStatus

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Label
field 6

___

## Create Data Structure

### Display Name
Surveillance Result

### Qualified Name
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Description
One row per surveillance appointment, measurement or incident recorded against a worker.

### Namespace Path
coco_pharma.health_surveillance_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Health Surveillance Records

### Element Id
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Membership Rationale
The Surveillance Result structure is part of the Health Surveillance Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
SurveillanceResultIdentifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultIdentifier

### Description
The record.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultIdentifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 2

___

## Create Data Field

### Display Name
SurveillanceResultType

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultType

### Description
Appointment, exposure measurement or exposure incident.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultType

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 3

___

## Create Data Field

### Display Name
SurveillanceResultDate

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultDate

### Description
When.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultDate

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 4

___

## Create Data Field

### Display Name
ExposureReadingIdentifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::ExposureReadingIdentifier

### Description
The measurement, for a measurement.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::ExposureReadingIdentifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 5

___

## Create Data Field

### Display Name
IncidentIdentifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::IncidentIdentifier

### Description
The incident, for an incident.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::IncidentIdentifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 6

___

## Create Data Field

### Display Name
SurveillanceResultDescription

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultDescription

### Description
The finding.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultDescription

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Label
field 7

___

## Create Data Field

### Display Name
SurveillanceResultActionDescription

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultActionDescription

### Description
Any action required.

### Data Type
string

### Position
8

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
DataField::Coco::Health Surveillance Records::Surveillance Result::SurveillanceResultActionDescription

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

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
- schemaName: health_surveillance_records
- schemaDescription: The enrolment of each worker in health surveillance according to their exposure profile, and the results of surveillance appointments, exposure measurements and exposure incidents held against the individual. The record belongs to the person it describes rather than to the company.

### Parent ID
DigitalProduct::Coco::Health Surveillance Records

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Long Term Health Archive

*Solution component:* `CocoPharma::SolutionComponent::LongTermHealthArchive`  
*Category:* Evidence Record

Health surveillance and exposure records retained for forty years from the last entry, across every system migration in that period.  Its requirement is not storage but interpretability: a record that survives and can no longer be read is the same failure as one that was lost.

## Create Digital Product

### Display Name
Long Term Health Archive

### Product Name
Long Term Health Archive

### Qualified Name
DigitalProduct::Coco::Long Term Health Archive

### Description
Health surveillance and exposure records retained for forty years from the last entry, across every system migration in that period.  Its requirement is not storage but interpretability: a record that survives and can no longer be read is the same failure as one that was lost.

### Purpose
Keeps each worker's surveillance and exposure history readable for the whole of its retention period.

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
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Element Id
DigitalProduct::Coco::Long Term Health Archive

### Membership Rationale
Produced by the People Systems group's `LongTermHealthArchive` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Long Term Health Archive Data Spec

### Qualified Name
DataSpec::Coco::Long Term Health Archive

### Description
The data structures and fields that make up the Long Term Health Archive digital product.

### Purpose
Describes the data a subscriber to Long Term Health Archive receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Long Term Health Archive

### Collection Id
DataSpec::Coco::Long Term Health Archive

### Label
data specification

___

## Create Data Structure

### Display Name
Archived Health Record

### Qualified Name
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Description
One row per record archived.

### Namespace Path
coco_pharma.long_term_health_archive

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Long Term Health Archive

### Element Id
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Membership Rationale
The Archived Health Record structure is part of the Long Term Health Archive data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
HealthRecordIdentifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordIdentifier

### Description
The archived record.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordIdentifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::WorkerPseudonymIdentifier

### Description
The worker.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 2

___

## Create Data Field

### Display Name
SurveillanceResultIdentifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::SurveillanceResultIdentifier

### Description
The surveillance record archived.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::SurveillanceResultIdentifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 3

___

## Create Data Field

### Display Name
HealthRecordArchivedDate

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordArchivedDate

### Description
When archived.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordArchivedDate

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 4

___

## Create Data Field

### Display Name
HealthRecordFormatCode

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordFormatCode

### Description
The format the record is held in.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordFormatCode

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 5

___

## Create Data Field

### Display Name
HealthRecordArchiveEndDate

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordArchiveEndDate

### Description
When retention ends.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordArchiveEndDate

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Label
field 6

___

## Create Data Field

### Display Name
HealthRecordReadableFlag

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordReadableFlag

### Description
Whether the record was readable at the last verification.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::HealthRecordReadableFlag

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

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
- schemaName: long_term_health_archive
- schemaDescription: Health surveillance and exposure records retained for forty years from the last entry, across every system migration in that period. Its requirement is not storage but interpretability: a record that survives and can no longer be read is the same failure as one that was lost.

### Parent ID
DigitalProduct::Coco::Long Term Health Archive

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
