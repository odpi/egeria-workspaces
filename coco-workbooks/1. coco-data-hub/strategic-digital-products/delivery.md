# Delivery Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 7 digital products owned by the Delivery business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of inbound and outbound logistics: sample consignments, therapy delivery events, transport classifications, dangerous goods declarations, temperature readings, cold chain records and carrier events.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Patient Sample Consignments | `CocoPharma::SolutionComponent::SampleLogistics` | Transactional Record | Sample Consignment |
| Therapy Delivery Events | `CocoPharma::SolutionComponent::TreatmentDeliveryTracking` | Event Stream | Delivery Event, Administration Confirmation |
| Transport Classifications | `CocoPharma::SolutionComponent::TransportClassificationService` | Reference Data | Transport Classification |
| Dangerous Goods Consignment Records | `CocoPharma::SolutionComponent::ShippingDocumentation` | Evidence Record | Consignment Declaration, Consignment Document |
| In-Transit Temperature Readings | `CocoPharma::SolutionComponent::TemperatureMonitoringDevices` | Time Series | Temperature Reading |
| Cold Chain Transit Records | `CocoPharma::SolutionComponent::ColdChainDataCollector` | Evidence Record | Transit Temperature Record, Excursion Detection |
| Carrier Transit Events | `CocoPharma::SolutionComponent::ColdChainDataCollector` | Event Stream | Transit Event |

For every product this file:

1. creates the **digital product** and adds it to the `Delivery` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

7 products, 10 data structures, 74 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret delivery.md
```

---

# Patient Sample Consignments

*Solution component:* `CocoPharma::SolutionComponent::SampleLogistics`  
*Category:* Transactional Record

The collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site.  It is the inbound half of a round trip that has a clock running from the moment the sample is taken.

## Create Digital Product

### Display Name
Patient Sample Consignments

### Product Name
Patient Sample Consignments

### Qualified Name
DigitalProduct::Coco::Patient Sample Consignments

### Description
The collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site.  It is the inbound half of a round trip that has a clock running from the moment the sample is taken.

### Purpose
Tracks each sample from collection to arrival so that the scheduler knows what is coming and how long it has.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Patient Sample Consignments

### Membership Rationale
Produced by the Delivery group's `SampleLogistics` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Patient Sample Consignments Data Spec

### Qualified Name
DataSpec::Coco::Patient Sample Consignments

### Description
The data structures and fields that make up the Patient Sample Consignments digital product.

### Purpose
Describes the data a subscriber to Patient Sample Consignments receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Patient Sample Consignments

### Collection Id
DataSpec::Coco::Patient Sample Consignments

### Label
data specification

___

## Create Data Structure

### Display Name
Sample Consignment

### Qualified Name
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Description
One row per consignment of patient material.

### Namespace Path
coco_data_hub.patient_sample_consignments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Patient Sample Consignments

### Element Id
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Membership Rationale
The Sample Consignment structure is part of the Patient Sample Consignments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Identifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Order Identifier

### Description
The order the material is for.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Order Identifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Sample Collection Location

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Collection Location

### Description
Where collected.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Collection Location

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Sample Collection Timestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Collection Timestamp

### Description
When the sample was taken.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Collection Timestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Shipment Dispatch Timestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Dispatch Timestamp

### Description
When dispatched.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Dispatch Timestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Shipment Delivery Timestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Delivery Timestamp

### Description
When it arrived at manufacturing.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Delivery Timestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Sample Viable Duration

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Viable Duration

### Description
The remaining viable life on arrival, in hours.

### Data Type
int

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Sample Viable Duration

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Shipment Arrival Description

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Arrival Description

### Description
The condition on arrival.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Shipment Arrival Description

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Carrier Identifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::Carrier Identifier

### Description
The carrier.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::Carrier Identifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

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
- schemaName: patient_sample_consignments
- schemaDescription: The collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site. It is the inbound half of a round trip that has a clock running from the moment the sample is taken.

### Parent ID
DigitalProduct::Coco::Patient Sample Consignments

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Therapy Delivery Events

*Solution component:* `CocoPharma::SolutionComponent::TreatmentDeliveryTracking`  
*Category:* Event Stream

The finished therapy tracked from release to administration at the treating site, and the confirmation of arrival and administration reported back into the order.  It closes the loop that the ordering portal opened.

## Create Digital Product

### Display Name
Therapy Delivery Events

### Product Name
Therapy Delivery Events

### Qualified Name
DigitalProduct::Coco::Therapy Delivery Events

### Description
The finished therapy tracked from release to administration at the treating site, and the confirmation of arrival and administration reported back into the order.  It closes the loop that the ordering portal opened.

### Purpose
Gives the pseudonym register and invoicing the evidence that the therapy reached the patient it was made for.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Therapy Delivery Events

### Membership Rationale
Produced by the Delivery group's `TreatmentDeliveryTracking` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Therapy Delivery Events Data Spec

### Qualified Name
DataSpec::Coco::Therapy Delivery Events

### Description
The data structures and fields that make up the Therapy Delivery Events digital product.

### Purpose
Describes the data a subscriber to Therapy Delivery Events receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Therapy Delivery Events

### Collection Id
DataSpec::Coco::Therapy Delivery Events

### Label
data specification

___

## Create Data Structure

### Display Name
Delivery Event

### Qualified Name
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Description
One row per tracking event for a released therapy.

### Namespace Path
coco_data_hub.therapy_delivery_events

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Therapy Delivery Events

### Element Id
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Membership Rationale
The Delivery Event structure is part of the Therapy Delivery Events data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Batch Identifier

### Description
The therapy.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Batch Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Shipment Event Type

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Type

### Description
Released, dispatched, in transit, delivered, administered.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Type

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Shipment Event Timestamp

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Timestamp

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Timestamp

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Order Identifier

### Description
The order.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Order Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Shipment Event Location

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Location

### Description
Where.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Event Location

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Shipment Storage Description

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Storage Description

### Description
The storage conditions the therapy must be kept under in transit.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::Shipment Storage Description

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Administration Confirmation

### Qualified Name
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Description
One row per therapy confirmed administered.

### Namespace Path
coco_data_hub.therapy_delivery_events

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Therapy Delivery Events

### Element Id
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Membership Rationale
The Administration Confirmation structure is part of the Therapy Delivery Events data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Batch Identifier

### Description
The therapy.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Batch Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Patient Pseudonym Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Patient Pseudonym Identifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Patient Pseudonym Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Treatment Administration Timestamp

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Treatment Administration Timestamp

### Description
When administered.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Treatment Administration Timestamp

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Clinician Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Clinician Identifier

### Description
Who administered.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Clinician Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Order Identifier

### Description
The order fulfilled.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::Order Identifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

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
- schemaName: therapy_delivery_events
- schemaDescription: The finished therapy tracked from release to administration at the treating site, and the confirmation of arrival and administration reported back into the order. It closes the loop that the ordering portal opened.

### Parent ID
DigitalProduct::Coco::Therapy Delivery Events

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Transport Classifications

*Solution component:* `CocoPharma::SolutionComponent::TransportClassificationService`  
*Category:* Reference Data

The transport classification of each substance and product in each form it is shipped: UN number, packing group, labelling and the documentation set required.  It is a library rather than a process because the same rules must give the same answer to despatch, to procurement and to the person signing the declaration.

## Create Digital Product

### Display Name
Transport Classifications

### Product Name
Transport Classifications

### Qualified Name
DigitalProduct::Coco::Transport Classifications

### Description
The transport classification of each substance and product in each form it is shipped: UN number, packing group, labelling and the documentation set required.  It is a library rather than a process because the same rules must give the same answer to despatch, to procurement and to the person signing the declaration.

### Purpose
Gives shipping documentation the classification and requirements for a consignment from one rule set.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Transport Classifications

### Membership Rationale
Produced by the Delivery group's `TransportClassificationService` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Transport Classifications Data Spec

### Qualified Name
DataSpec::Coco::Transport Classifications

### Description
The data structures and fields that make up the Transport Classifications digital product.

### Purpose
Describes the data a subscriber to Transport Classifications receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Transport Classifications

### Collection Id
DataSpec::Coco::Transport Classifications

### Label
data specification

___

## Create Data Structure

### Display Name
Transport Classification

### Qualified Name
DataStructure::Coco::Transport Classifications::Transport Classification

### Description
One row per substance or product per shipped form.

### Namespace Path
coco_data_hub.transport_classifications

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Transport Classifications

### Element Id
DataStructure::Coco::Transport Classifications::Transport Classification

### Membership Rationale
The Transport Classification structure is part of the Transport Classifications data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Transport Classification Identifier

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Identifier

### Description
The unique identifier of the transport classification of a substance or product in a shipped form.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Identifier

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Substance Code

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Substance Code

### Description
The substance, for hazardous materials.

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
DataField::Coco::Transport Classifications::Transport Classification::Substance Code

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Product Code

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Product Code

### Description
The product, for finished goods.

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
DataField::Coco::Transport Classifications::Transport Classification::Product Code

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Substance Form Description

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Substance Form Description

### Description
The form shipped.

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
DataField::Coco::Transport Classifications::Transport Classification::Substance Form Description

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transport Classification Code

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Code

### Description
The UN number.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Code

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Transport Classification Packing Group Code

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Packing Group Code

### Description
The packing group.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
5

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Packing Group Code

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Transport Classification Hazard Class Code

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Hazard Class Code

### Description
The hazard class.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Hazard Class Code

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Transport Classification Labelling Description

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Labelling Description

### Description
The labelling required.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Labelling Description

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Transport Classification Documentation Description

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Documentation Description

### Description
The documentation set required.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Documentation Description

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Transport Classification Date

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Date

### Description
When derived.

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
DataField::Coco::Transport Classifications::Transport Classification::Transport Classification Date

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

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
- schemaName: transport_classifications
- schemaDescription: The transport classification of each substance and product in each form it is shipped: UN number, packing group, labelling and the documentation set required. It is a library rather than a process because the same rules must give the same answer to despatch, to procurement and to the person signing the declaration.

### Parent ID
DigitalProduct::Coco::Transport Classifications

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Dangerous Goods Consignment Records

*Solution component:* `CocoPharma::SolutionComponent::ShippingDocumentation`  
*Category:* Evidence Record

The dangerous goods declaration and accompanying documents for each consignment, signed by a certificated person, with the certificate that authorised the signature.  The shipper's liability stays with the company however the carrier behaves afterwards.

## Create Digital Product

### Display Name
Dangerous Goods Consignment Records

### Product Name
Dangerous Goods Consignment Records

### Qualified Name
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Description
The dangerous goods declaration and accompanying documents for each consignment, signed by a certificated person, with the certificate that authorised the signature.  The shipper's liability stays with the company however the carrier behaves afterwards.

### Purpose
Records what was declared, by whom and under what certificate, for every consignment handed to a carrier.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Membership Rationale
Produced by the Delivery group's `ShippingDocumentation` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Dangerous Goods Consignment Records Data Spec

### Qualified Name
DataSpec::Coco::Dangerous Goods Consignment Records

### Description
The data structures and fields that make up the Dangerous Goods Consignment Records digital product.

### Purpose
Describes the data a subscriber to Dangerous Goods Consignment Records receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Collection Id
DataSpec::Coco::Dangerous Goods Consignment Records

### Label
data specification

___

## Create Data Structure

### Display Name
Consignment Declaration

### Qualified Name
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Description
One row per dangerous goods consignment.

### Namespace Path
coco_data_hub.dangerous_goods_consignment_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Dangerous Goods Consignment Records

### Element Id
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Membership Rationale
The Consignment Declaration structure is part of the Dangerous Goods Consignment Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Shipment Dispatch Date

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Dispatch Date

### Description
When dispatched.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Dispatch Date

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Carrier Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Carrier Identifier

### Description
The carrier.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Carrier Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Shipment Ship To Address

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Ship To Address

### Description
The destination.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Ship To Address

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transport Classification Code

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Transport Classification Code

### Description
The UN number declared.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Transport Classification Code

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Shipment Quantity

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Quantity

### Description
The quantity shipped.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Quantity

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Shipment Unit

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Unit

### Description
The unit.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Shipment Unit

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Declaration Signatory Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Declaration Signatory Identifier

### Description
The certificated signatory, by pseudonym.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Declaration Signatory Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Declaration Signed Timestamp

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Declaration Signed Timestamp

### Description
When signed.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Declaration Signed Timestamp

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Certificate Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Certificate Identifier

### Description
The signatory's dangerous goods certificate.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::Certificate Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

___

## Create Data Structure

### Display Name
Consignment Document

### Qualified Name
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Description
One row per document in the consignment's documentation set.

### Namespace Path
coco_data_hub.dangerous_goods_consignment_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Dangerous Goods Consignment Records

### Element Id
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Membership Rationale
The Consignment Document structure is part of the Dangerous Goods Consignment Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Shipment Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Document Identifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Identifier

### Description
The document.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Identifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Document Type

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Type

### Description
Declaration, safety data sheet, handling instructions or other.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Type

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Document Date

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Date

### Description
Its date.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::Document Date

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

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
- schemaName: dangerous_goods_consignment_records
- schemaDescription: The dangerous goods declaration and accompanying documents for each consignment, signed by a certificated person, with the certificate that authorised the signature. The shipper's liability stays with the company however the carrier behaves afterwards.

### Parent ID
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# In-Transit Temperature Readings

*Solution component:* `CocoPharma::SolutionComponent::TemperatureMonitoringDevices`  
*Category:* Time Series

The readings from the loggers and live monitors travelling inside consignments: temperature, location and time.  The devices are themselves dangerous goods, because they contain lithium batteries.

## Create Digital Product

### Display Name
In-Transit Temperature Readings

### Product Name
In-Transit Temperature Readings

### Qualified Name
DigitalProduct::Coco::In-Transit Temperature Readings

### Description
The readings from the loggers and live monitors travelling inside consignments: temperature, location and time.  The devices are themselves dangerous goods, because they contain lithium batteries.

### Purpose
Provides the raw record from which the cold chain collector builds each consignment's temperature history.

### Category
Time Series

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::In-Transit Temperature Readings

### Membership Rationale
Produced by the Delivery group's `TemperatureMonitoringDevices` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
In-Transit Temperature Readings Data Spec

### Qualified Name
DataSpec::Coco::In-Transit Temperature Readings

### Description
The data structures and fields that make up the In-Transit Temperature Readings digital product.

### Purpose
Describes the data a subscriber to In-Transit Temperature Readings receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::In-Transit Temperature Readings

### Collection Id
DataSpec::Coco::In-Transit Temperature Readings

### Label
data specification

___

## Create Data Structure

### Display Name
Temperature Reading

### Qualified Name
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Description
One row per reading from a device.

### Namespace Path
coco_data_hub.in_transit_temperature_readings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::In-Transit Temperature Readings

### Element Id
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Membership Rationale
The Temperature Reading structure is part of the In-Transit Temperature Readings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Device Identifier

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Identifier

### Description
The device.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Identifier

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Device Reading Timestamp

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Reading Timestamp

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Reading Timestamp

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Shipment Identifier

### Description
The consignment the device travelled with.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Shipment Identifier

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Device Reading Temperature

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Reading Temperature

### Description
The temperature, in degrees Celsius.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Reading Temperature

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Device Location

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Location

### Description
The device's reported location, if it reports one.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Location

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Device Type

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Type

### Description
Logger or live monitor.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::Device Type

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

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
- schemaName: in_transit_temperature_readings
- schemaDescription: The readings from the loggers and live monitors travelling inside consignments: temperature, location and time. The devices are themselves dangerous goods, because they contain lithium batteries.

### Parent ID
DigitalProduct::Coco::In-Transit Temperature Readings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Cold Chain Transit Records

*Solution component:* `CocoPharma::SolutionComponent::ColdChainDataCollector`  
*Category:* Evidence Record

The temperature history of each consignment reconciled against the permitted range for the product shipped, and the excursions detected.  A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.

## Create Digital Product

### Display Name
Cold Chain Transit Records

### Product Name
Cold Chain Transit Records

### Qualified Name
DigitalProduct::Coco::Cold Chain Transit Records

### Description
The temperature history of each consignment reconciled against the permitted range for the product shipped, and the excursions detected.  A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.

### Purpose
Tells excursion assessment which consignments left their permitted range, for how long, and for which product and batch.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Cold Chain Transit Records

### Membership Rationale
Produced by the Delivery group's `ColdChainDataCollector` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Cold Chain Transit Records Data Spec

### Qualified Name
DataSpec::Coco::Cold Chain Transit Records

### Description
The data structures and fields that make up the Cold Chain Transit Records digital product.

### Purpose
Describes the data a subscriber to Cold Chain Transit Records receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Cold Chain Transit Records

### Collection Id
DataSpec::Coco::Cold Chain Transit Records

### Label
data specification

___

## Create Data Structure

### Display Name
Transit Temperature Record

### Qualified Name
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Description
One row per consignment, the reconciled temperature history.

### Namespace Path
coco_data_hub.cold_chain_transit_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Cold Chain Transit Records

### Element Id
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Membership Rationale
The Transit Temperature Record structure is part of the Cold Chain Transit Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Identifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Product Code

### Description
The product shipped.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Product Code

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Batch Identifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Batch Identifier

### Description
The batch.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Batch Identifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Device Identifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Device Identifier

### Description
The device the record came from.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Device Identifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Shipment Transit Start Timestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Start Timestamp

### Description
When monitoring began.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Start Timestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Shipment Transit End Timestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit End Timestamp

### Description
When monitoring ended.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit End Timestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Shipment Transit Minimum Temperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Minimum Temperature

### Description
The lowest temperature recorded.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Minimum Temperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Shipment Transit Maximum Temperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Maximum Temperature

### Description
The highest temperature recorded.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Maximum Temperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Shipment Transit Record Complete Flag

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Record Complete Flag

### Description
Whether the record has no gaps.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::Shipment Transit Record Complete Flag

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Excursion Detection

### Qualified Name
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Description
One row per excursion detected in a consignment's record.

### Namespace Path
coco_data_hub.cold_chain_transit_records

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Cold Chain Transit Records

### Element Id
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Membership Rationale
The Excursion Detection structure is part of the Cold Chain Transit Records data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Excursion Identifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Identifier

### Description
The excursion.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Identifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Shipment Identifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Excursion Start Timestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Start Timestamp

### Description
When the range was left.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Start Timestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Excursion End Timestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion End Timestamp

### Description
When it was regained.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion End Timestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Excursion Duration

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Duration

### Description
How long, in minutes.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Duration

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Excursion Maximum Temperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Maximum Temperature

### Description
The extreme temperature reached.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Maximum Temperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Excursion Type

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Type

### Description
Temperature excursion or monitoring gap.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::Excursion Type

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

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
- schemaName: cold_chain_transit_records
- schemaDescription: The temperature history of each consignment reconciled against the permitted range for the product shipped, and the excursions detected. A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.

### Parent ID
DigitalProduct::Coco::Cold Chain Transit Records

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Carrier Transit Events

*Solution component:* `CocoPharma::SolutionComponent::ColdChainDataCollector`  
*Category:* Event Stream

The handover events, delays and delivery confirmations reported by carrier systems for each consignment.  The company reads status from carriers and hands documentation to them, but has no visibility of what happens inside them.

## Create Digital Product

### Display Name
Carrier Transit Events

### Product Name
Carrier Transit Events

### Qualified Name
DigitalProduct::Coco::Carrier Transit Events

### Description
The handover events, delays and delivery confirmations reported by carrier systems for each consignment.  The company reads status from carriers and hands documentation to them, but has no visibility of what happens inside them.

### Purpose
Aligns the carriers' account of a consignment's journey with the temperature record, so that an excursion can be placed.

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
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Element Id
DigitalProduct::Coco::Carrier Transit Events

### Membership Rationale
Produced by the Delivery group's `ColdChainDataCollector` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Carrier Transit Events Data Spec

### Qualified Name
DataSpec::Coco::Carrier Transit Events

### Description
The data structures and fields that make up the Carrier Transit Events digital product.

### Purpose
Describes the data a subscriber to Carrier Transit Events receives, structure by structure and field by field, using the Data Field Naming standard.

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
DigitalProduct::Coco::Carrier Transit Events

### Collection Id
DataSpec::Coco::Carrier Transit Events

### Label
data specification

___

## Create Data Structure

### Display Name
Transit Event

### Qualified Name
DataStructure::Coco::Carrier Transit Events::Transit Event

### Description
One row per event reported by a carrier.

### Namespace Path
coco_data_hub.carrier_transit_events

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Carrier Transit Events

### Element Id
DataStructure::Coco::Carrier Transit Events::Transit Event

### Membership Rationale
The Transit Event structure is part of the Carrier Transit Events data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Shipment Identifier

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Identifier

### Description
The consignment.

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
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Identifier

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Shipment Transit Event Type

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Type

### Description
Collected, handed over, delayed, delivered or exception.

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
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Type

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Shipment Transit Event Timestamp

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Timestamp

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
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Timestamp

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Carrier Identifier

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Carrier Identifier

### Description
The carrier.

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
DataField::Coco::Carrier Transit Events::Transit Event::Carrier Identifier

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Shipment Transit Event Location

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Location

### Description
Where.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Location

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Shipment Transit Event Description

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Description

### Description
The carrier's description.

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
DataField::Coco::Carrier Transit Events::Transit Event::Shipment Transit Event Description

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

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
- schemaName: carrier_transit_events
- schemaDescription: The handover events, delays and delivery confirmations reported by carrier systems for each consignment. The company reads status from carriers and hands documentation to them, but has no visibility of what happens inside them.

### Parent ID
DigitalProduct::Coco::Carrier Transit Events

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
