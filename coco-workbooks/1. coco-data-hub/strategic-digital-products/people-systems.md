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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

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
coco_data_hub.worker_master_data

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Worker Pseudonym Identifier

### Description
The worker's pseudonym.

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
DataField::Coco::Worker Master Data::Worker::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Type

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Worker Type

### Description
Employee or contractor.

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
DataField::Coco::Worker Master Data::Worker::Worker Type

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Legal Entity Code

### Description
The employing entity.

### Data Type
string

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
DataField::Coco::Worker Master Data::Worker::Legal Entity Code

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Site Code

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Site Code

### Description
The primary site.

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
DataField::Coco::Worker Master Data::Worker::Site Code

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Worker Hire Date

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Worker Hire Date

### Description
When the worker joined.

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
DataField::Coco::Worker Master Data::Worker::Worker Hire Date

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Worker Leave Date

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Worker Leave Date

### Description
When they left, once they have.

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
DataField::Coco::Worker Master Data::Worker::Worker Leave Date

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Worker Current Status

### Qualified Name
DataField::Coco::Worker Master Data::Worker::Worker Current Status

### Description
Active, on leave, left.

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
DataField::Coco::Worker Master Data::Worker::Worker Current Status

### Data Structure
DataStructure::Coco::Worker Master Data::Worker

### Position
7

### Coverage Category
CORE_DETAIL

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
coco_data_hub.worker_master_data

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Worker Master Data::Worker Assignment::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Role Code

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Role Code

### Description
The role.

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
DataField::Coco::Worker Master Data::Worker Assignment::Role Code

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Role Name

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Role Name

### Description
The role's name.

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
DataField::Coco::Worker Master Data::Worker Assignment::Role Name

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Cost Centre Code

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Cost Centre Code

### Description
The cost centre.

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
DataField::Coco::Worker Master Data::Worker Assignment::Cost Centre Code

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Manager Pseudonym Identifier

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Manager Pseudonym Identifier

### Description
The reporting manager.

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
DataField::Coco::Worker Master Data::Worker Assignment::Manager Pseudonym Identifier

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Worker Assignment Start Date

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Worker Assignment Start Date

### Description
When the assignment began.

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
DataField::Coco::Worker Master Data::Worker Assignment::Worker Assignment Start Date

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Worker Spending Maximum Amount

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Worker Spending Maximum Amount

### Description
The worker's spending authority.

### Data Type
bigdecimal

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
DataField::Coco::Worker Master Data::Worker Assignment::Worker Spending Maximum Amount

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Worker Hazard Profile Description

### Qualified Name
DataField::Coco::Worker Master Data::Worker Assignment::Worker Hazard Profile Description

### Description
The substances and tasks the role exposes the worker to.

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
DataField::Coco::Worker Master Data::Worker Assignment::Worker Hazard Profile Description

### Data Structure
DataStructure::Coco::Worker Master Data::Worker Assignment

### Position
8

### Coverage Category
CORE_DETAIL

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
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
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
coco_data_hub.worker_lifecycle_events

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
Worker Event Identifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Identifier

### Description
The event.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Identifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Worker Event Type

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Type

### Description
Joiner, mover or leaver.

### Data Type
string

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Type

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Worker Event Start Date

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Start Date

### Description
The effective date.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Start Date

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Worker Event Raised Timestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Raised Timestamp

### Description
When the event was raised.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Raised Timestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Role Code

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Role Code

### Description
The new role, for a joiner or mover.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Role Code

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Worker Event Description

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Description

### Description
The change.

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
DataField::Coco::Worker Lifecycle Events::Worker Event::Worker Event Description

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Worker Event

### Position
7

### Coverage Category
CORE_DETAIL

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
coco_data_hub.worker_lifecycle_events

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
Worker Event Identifier

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Identifier

### Description
The event.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Identifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::System Identifier

### Description
The system notified.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::System Identifier

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Worker Event Sent Timestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Sent Timestamp

### Description
When notified.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Sent Timestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Worker Event Applied Flag

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Applied Flag

### Description
Whether the system has confirmed acting on it.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Applied Flag

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Worker Event Applied Timestamp

### Qualified Name
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Applied Timestamp

### Description
When confirmed.

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
DataField::Coco::Worker Lifecycle Events::Event Distribution Status::Worker Event Applied Timestamp

### Data Structure
DataStructure::Coco::Worker Lifecycle Events::Event Distribution Status

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
coco_data_hub.access_entitlements

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
User Account Identifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::User Account Identifier

### Description
The account.

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
DataField::Coco::Access Entitlements::Account::User Account Identifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Access Entitlements::Account::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

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
DataField::Coco::Access Entitlements::Account::System Identifier

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
DataField::Coco::Access Entitlements::Account::System Identifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
User Account Start Date

### Qualified Name
DataField::Coco::Access Entitlements::Account::User Account Start Date

### Description
When created.

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
DataField::Coco::Access Entitlements::Account::User Account Start Date

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
User Account End Date

### Qualified Name
DataField::Coco::Access Entitlements::Account::User Account End Date

### Description
When removed, once removed.

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
DataField::Coco::Access Entitlements::Account::User Account End Date

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
User Account Current Status

### Qualified Name
DataField::Coco::Access Entitlements::Account::User Account Current Status

### Description
Active, suspended, removed.

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
DataField::Coco::Access Entitlements::Account::User Account Current Status

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Worker Event Identifier

### Qualified Name
DataField::Coco::Access Entitlements::Account::Worker Event Identifier

### Description
The worker event that last changed it.

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
DataField::Coco::Access Entitlements::Account::Worker Event Identifier

### Data Structure
DataStructure::Coco::Access Entitlements::Account

### Position
7

### Coverage Category
CORE_DETAIL

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
coco_data_hub.access_entitlements

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
User Account Identifier

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::User Account Identifier

### Description
The account.

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
DataField::Coco::Access Entitlements::Entitlement::User Account Identifier

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Entitlement Code

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::Entitlement Code

### Description
The entitlement.

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
DataField::Coco::Access Entitlements::Entitlement::Entitlement Code

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Entitlement Description

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::Entitlement Description

### Description
What it permits.

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
DataField::Coco::Access Entitlements::Entitlement::Entitlement Description

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Entitlement Start Date

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::Entitlement Start Date

### Description
When granted.

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
DataField::Coco::Access Entitlements::Entitlement::Entitlement Start Date

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Entitlement End Date

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::Entitlement End Date

### Description
When revoked, once revoked.

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
DataField::Coco::Access Entitlements::Entitlement::Entitlement End Date

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Entitlement Data Owner Flag

### Qualified Name
DataField::Coco::Access Entitlements::Entitlement::Entitlement Data Owner Flag

### Description
Whether the entitlement makes the worker a data owner in the catalogue.

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
DataField::Coco::Access Entitlements::Entitlement::Entitlement Data Owner Flag

### Data Structure
DataStructure::Coco::Access Entitlements::Entitlement

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
coco_data_hub.payroll_results

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
Payroll Run Identifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Identifier

### Description
The run.

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Identifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Legal Entity Code

### Description
The entity paid.

### Data Type
string

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
DataField::Coco::Payroll Results::Payroll Run::Legal Entity Code

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Payroll Period Code

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Period Code

### Description
The pay period.

### Data Type
string

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Period Code

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Payroll Run Date

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Date

### Description
When run.

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Date

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Payroll Run Count

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Count

### Description
The number of workers paid.

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Count

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Payroll Run Total Amount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Total Amount

### Description
The total remuneration.

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Run Total Amount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Payroll Currency Code

### Qualified Name
DataField::Coco::Payroll Results::Payroll Run::Payroll Currency Code

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
DataField::Coco::Payroll Results::Payroll Run::Payroll Currency Code

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Run

### Position
7

### Coverage Category
CORE_DETAIL

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
coco_data_hub.payroll_results

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
Payroll Run Identifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Payroll Run Identifier

### Description
The run.

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
DataField::Coco::Payroll Results::Payroll Posting::Payroll Run Identifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Payroll Results::Payroll Posting::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Payroll Gross Amount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Payroll Gross Amount

### Description
Gross remuneration.

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
DataField::Coco::Payroll Results::Payroll Posting::Payroll Gross Amount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Payroll Employer Amount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Payroll Employer Amount

### Description
Employer costs.

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
DataField::Coco::Payroll Results::Payroll Posting::Payroll Employer Amount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Payroll Net Amount

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Payroll Net Amount

### Description
Net paid.

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
DataField::Coco::Payroll Results::Payroll Posting::Payroll Net Amount

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Cost Centre Code

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Cost Centre Code

### Description
The cost centre charged.

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
DataField::Coco::Payroll Results::Payroll Posting::Cost Centre Code

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Payroll Results::Payroll Posting::Ledger Account Code

### Description
The account posted to.

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
DataField::Coco::Payroll Results::Payroll Posting::Ledger Account Code

### Data Structure
DataStructure::Coco::Payroll Results::Payroll Posting

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
coco_data_hub.corporate_directory_entries

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Person First Name

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Person First Name

### Description
Given name.

### Data Type
string

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Person First Name

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Person Last Name

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Person Last Name

### Description
Family name.

### Data Type
string

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Person Last Name

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Role Name

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Role Name

### Description
The role.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Role Name

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Department Name

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Department Name

### Description
The department.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Department Name

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Site Code

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Site Code

### Description
The location.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Site Code

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Manager Pseudonym Identifier

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Manager Pseudonym Identifier

### Description
The reporting manager.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Manager Pseudonym Identifier

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Person Work Phone Number

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Person Work Phone Number

### Description
Work telephone.

### Data Type
string

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Person Work Phone Number

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Directory Entry Current Timestamp

### Qualified Name
DataField::Coco::Corporate Directory Entries::Directory Entry::Directory Entry Current Timestamp

### Description
When the entry was last updated from the worker record.

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
DataField::Coco::Corporate Directory Entries::Directory Entry::Directory Entry Current Timestamp

### Data Structure
DataStructure::Coco::Corporate Directory Entries::Directory Entry

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
coco_data_hub.role_competency_requirements

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
Role Code

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Role Code

### Description
The role.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Role Code

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Competency Code

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Code

### Description
The competency.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Code

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Competency Name

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Name

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Name

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Competency Description

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Description

### Description
What the competency covers.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Description

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Competency Refresh Duration

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Refresh Duration

### Description
How often it must be refreshed, in months.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Refresh Duration

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Competency Regulated Flag

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Regulated Flag

### Description
Whether a regulation requires it.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Competency Regulated Flag

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Role Requirement Start Date

### Qualified Name
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Role Requirement Start Date

### Description
When the requirement took effect.

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
DataField::Coco::Role Competency Requirements::Role Competency Requirement::Role Requirement Start Date

### Data Structure
DataStructure::Coco::Role Competency Requirements::Role Competency Requirement

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
coco_data_hub.training_completions

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
Training Completion Identifier

### Qualified Name
DataField::Coco::Training Completions::Training Completion::Training Completion Identifier

### Description
The completion.

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
DataField::Coco::Training Completions::Training Completion::Training Completion Identifier

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Training Completions::Training Completion::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Training Completions::Training Completion::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Training Course Code

### Qualified Name
DataField::Coco::Training Completions::Training Completion::Training Course Code

### Description
The course.

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
DataField::Coco::Training Completions::Training Completion::Training Course Code

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Competency Code

### Qualified Name
DataField::Coco::Training Completions::Training Completion::Competency Code

### Description
The competency the course evidences.

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
DataField::Coco::Training Completions::Training Completion::Competency Code

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Training Completed Date

### Qualified Name
DataField::Coco::Training Completions::Training Completion::Training Completed Date

### Description
When completed.

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
DataField::Coco::Training Completions::Training Completion::Training Completed Date

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

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
DataField::Coco::Training Completions::Training Completion::Training Expiry Date

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
DataField::Coco::Training Completions::Training Completion::Training Expiry Date

### Data Structure
DataStructure::Coco::Training Completions::Training Completion

### Position
6

### Coverage Category
CORE_DETAIL

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
coco_data_hub.training_completions

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
Training Completion Identifier

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::Training Completion Identifier

### Description
The completion assessed.

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
DataField::Coco::Training Completions::Assessment Result::Training Completion Identifier

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Training Assessment Date

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::Training Assessment Date

### Description
When assessed.

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
DataField::Coco::Training Completions::Assessment Result::Training Assessment Date

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Training Assessment Value

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::Training Assessment Value

### Description
The score.

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
DataField::Coco::Training Completions::Assessment Result::Training Assessment Value

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Training Assessment Minimum Value

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::Training Assessment Minimum Value

### Description
The pass mark.

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
DataField::Coco::Training Completions::Assessment Result::Training Assessment Minimum Value

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Training Assessment Passed Flag

### Qualified Name
DataField::Coco::Training Completions::Assessment Result::Training Assessment Passed Flag

### Description
Whether the worker passed.

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
DataField::Coco::Training Completions::Assessment Result::Training Assessment Passed Flag

### Data Structure
DataStructure::Coco::Training Completions::Assessment Result

### Position
5

### Coverage Category
CORE_DETAIL

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
coco_data_hub.training_completions

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Training Completions::Refresher Schedule::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Competency Code

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::Competency Code

### Description
The competency lapsing.

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
DataField::Coco::Training Completions::Refresher Schedule::Competency Code

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Training Due Date

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::Training Due Date

### Description
When it must be completed.

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
DataField::Coco::Training Completions::Refresher Schedule::Training Due Date

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Training Course Code

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::Training Course Code

### Description
The refresher course.

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
DataField::Coco::Training Completions::Refresher Schedule::Training Course Code

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Training Scheduled Date

### Qualified Name
DataField::Coco::Training Completions::Refresher Schedule::Training Scheduled Date

### Description
When it is scheduled.

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
DataField::Coco::Training Completions::Refresher Schedule::Training Scheduled Date

### Data Structure
DataStructure::Coco::Training Completions::Refresher Schedule

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
coco_data_hub.worker_qualifications

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Competency Code

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Competency Code

### Description
The competency.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Competency Code

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Competency Name

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Competency Name

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
DataField::Coco::Worker Qualifications::Worker Qualification::Competency Name

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Qualification Start Date

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Start Date

### Description
When gained.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Start Date

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Qualification Expiry Date

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Expiry Date

### Description
When it lapses.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Expiry Date

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Qualification Current Status

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Current Status

### Description
Current, lapsing, lapsed.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Qualification Current Status

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Training Completion Identifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Training Completion Identifier

### Description
The training completion that evidences it.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Training Completion Identifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Certificate Identifier

### Description
The external certificate, where one exists.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Certificate Identifier

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Role Code

### Qualified Name
DataField::Coco::Worker Qualifications::Worker Qualification::Role Code

### Description
The role the qualification was gained for.

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
DataField::Coco::Worker Qualifications::Worker Qualification::Role Code

### Data Structure
DataStructure::Coco::Worker Qualifications::Worker Qualification

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
coco_data_hub.qualification_expiry_warnings

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
Qualification Warning Identifier

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Identifier

### Description
The warning.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Identifier

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Competency Code

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Competency Code

### Description
The competency.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Competency Code

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Qualification Expiry Date

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Expiry Date

### Description
When it lapses.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Expiry Date

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Qualification Warning Raised Timestamp

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Raised Timestamp

### Description
When the warning was raised.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Raised Timestamp

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Qualification Warning Type

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Type

### Description
Approaching expiry or expired.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Qualification Warning Type

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Training Due Date

### Qualified Name
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Training Due Date

### Description
The deadline set for the refresher.

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
DataField::Coco::Qualification Expiry Warnings::Qualification Expiry Warning::Training Due Date

### Data Structure
DataStructure::Coco::Qualification Expiry Warnings::Qualification Expiry Warning

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
coco_data_hub.health_surveillance_records

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
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Surveillance Enrollment Date

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Enrollment Date

### Description
When enrolled.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Enrollment Date

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Role Code

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Role Code

### Description
The role that required enrolment.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Role Code

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Worker Hazard Profile Description

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Worker Hazard Profile Description

### Description
The exposure profile enrolment was based on.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Worker Hazard Profile Description

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Surveillance Frequency

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Frequency

### Description
How often appointments are due, in months.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Frequency

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Surveillance Current Status

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Current Status

### Description
Enrolled, lapsed, ended.

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
DataField::Coco::Health Surveillance Records::Surveillance Enrolment::Surveillance Current Status

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Enrolment

### Position
6

### Coverage Category
CORE_DETAIL

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
coco_data_hub.health_surveillance_records

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
Surveillance Result Identifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Identifier

### Description
The record.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Identifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Surveillance Result Type

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Type

### Description
Appointment, exposure measurement or exposure incident.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Type

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Surveillance Result Date

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Date

### Description
When.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Date

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Exposure Reading Identifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Exposure Reading Identifier

### Description
The measurement, for a measurement.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Exposure Reading Identifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Incident Identifier

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Incident Identifier

### Description
The incident, for an incident.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Incident Identifier

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Surveillance Result Description

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Description

### Description
The finding.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Description

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Surveillance Result Action Description

### Qualified Name
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Action Description

### Description
Any action required.

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
DataField::Coco::Health Surveillance Records::Surveillance Result::Surveillance Result Action Description

### Data Structure
DataStructure::Coco::Health Surveillance Records::Surveillance Result

### Position
8

### Coverage Category
CORE_DETAIL

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
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_data_hub
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
coco_data_hub.long_term_health_archive

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
Health Record Identifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Identifier

### Description
The archived record.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Identifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Worker Pseudonym Identifier

### Description
The worker.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Surveillance Result Identifier

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Surveillance Result Identifier

### Description
The surveillance record archived.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Surveillance Result Identifier

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Health Record Archived Date

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Archived Date

### Description
When archived.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Archived Date

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Health Record Format Code

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Format Code

### Description
The format the record is held in.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Format Code

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Health Record Archive End Date

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Archive End Date

### Description
When retention ends.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Archive End Date

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Health Record Readable Flag

### Qualified Name
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Readable Flag

### Description
Whether the record was readable at the last verification.

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
DataField::Coco::Long Term Health Archive::Archived Health Record::Health Record Readable Flag

### Data Structure
DataStructure::Coco::Long Term Health Archive::Archived Health Record

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
