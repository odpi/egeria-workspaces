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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

7 products, 10 data structures, 73 data fields.  This file loads after `catalog.md`.

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
coco_pharma.patient_sample_consignments

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 1

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::OrderIdentifier

### Description
The order the material is for.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::OrderIdentifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 2

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 3

___

## Create Data Field

### Display Name
SampleCollectionLocation

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleCollectionLocation

### Description
Where collected.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleCollectionLocation

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 4

___

## Create Data Field

### Display Name
SampleCollectionTimestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleCollectionTimestamp

### Description
When the sample was taken.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleCollectionTimestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 5

___

## Create Data Field

### Display Name
ShipmentDispatchTimestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentDispatchTimestamp

### Description
When dispatched.

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentDispatchTimestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 6

___

## Create Data Field

### Display Name
ShipmentDeliveryTimestamp

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentDeliveryTimestamp

### Description
When it arrived at manufacturing.

### Data Type
date

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentDeliveryTimestamp

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 7

___

## Create Data Field

### Display Name
SampleViableDuration

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleViableDuration

### Description
The remaining viable life on arrival, in hours.

### Data Type
int

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::SampleViableDuration

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 8

___

## Create Data Field

### Display Name
ShipmentArrivalDescription

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentArrivalDescription

### Description
The condition on arrival.

### Data Type
string

### Position
9

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::ShipmentArrivalDescription

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

### Label
field 9

___

## Create Data Field

### Display Name
CarrierIdentifier

### Qualified Name
DataField::Coco::Patient Sample Consignments::Sample Consignment::CarrierIdentifier

### Description
The carrier.

### Data Type
string

### Position
10

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
DataField::Coco::Patient Sample Consignments::Sample Consignment::CarrierIdentifier

### Data Structure
DataStructure::Coco::Patient Sample Consignments::Sample Consignment

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
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
coco_pharma.therapy_delivery_events

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
BatchIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::BatchIdentifier

### Description
The therapy.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::BatchIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 1

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 2

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::OrderIdentifier

### Description
The order.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::OrderIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 3

___

## Create Data Field

### Display Name
ShipmentEventType

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventType

### Description
Released, dispatched, in transit, delivered, administered.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventType

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 4

___

## Create Data Field

### Display Name
ShipmentEventTimestamp

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventTimestamp

### Description
When.

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
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventTimestamp

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 5

___

## Create Data Field

### Display Name
ShipmentEventLocation

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventLocation

### Description
Where.

### Data Type
string

### Position
6

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
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentEventLocation

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

### Label
field 6

___

## Create Data Field

### Display Name
ShipmentStorageDescription

### Qualified Name
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentStorageDescription

### Description
The storage conditions the therapy must be kept under in transit.

### Data Type
string

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
DataField::Coco::Therapy Delivery Events::Delivery Event::ShipmentStorageDescription

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Delivery Event

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
coco_pharma.therapy_delivery_events

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
BatchIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::BatchIdentifier

### Description
The therapy.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::BatchIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Label
field 1

___

## Create Data Field

### Display Name
PatientPseudonymIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::PatientPseudonymIdentifier

### Description
The patient, by pseudonym.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::PatientPseudonymIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Label
field 2

___

## Create Data Field

### Display Name
TreatmentAdministrationTimestamp

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::TreatmentAdministrationTimestamp

### Description
When administered.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::TreatmentAdministrationTimestamp

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Label
field 3

___

## Create Data Field

### Display Name
ClinicianIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::ClinicianIdentifier

### Description
Who administered.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::ClinicianIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

### Label
field 4

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Therapy Delivery Events::Administration Confirmation::OrderIdentifier

### Description
The order fulfilled.

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
DataField::Coco::Therapy Delivery Events::Administration Confirmation::OrderIdentifier

### Data Structure
DataStructure::Coco::Therapy Delivery Events::Administration Confirmation

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
coco_pharma.transport_classifications

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
SubstanceCode

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::SubstanceCode

### Description
The substance, for hazardous materials.

### Data Type
string

### Position
1

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
DataField::Coco::Transport Classifications::Transport Classification::SubstanceCode

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::ProductCode

### Description
The product, for finished goods.

### Data Type
string

### Position
2

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
DataField::Coco::Transport Classifications::Transport Classification::ProductCode

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 2

___

## Create Data Field

### Display Name
SubstanceFormDescription

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::SubstanceFormDescription

### Description
The form shipped.

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
DataField::Coco::Transport Classifications::Transport Classification::SubstanceFormDescription

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 3

___

## Create Data Field

### Display Name
TransportClassificationCode

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationCode

### Description
The UN number.

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationCode

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 4

___

## Create Data Field

### Display Name
TransportClassificationPackingGroupCode

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationPackingGroupCode

### Description
The packing group.

### Data Type
string

### Position
5

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationPackingGroupCode

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 5

___

## Create Data Field

### Display Name
TransportClassificationHazardClassCode

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationHazardClassCode

### Description
The hazard class.

### Data Type
string

### Position
6

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationHazardClassCode

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 6

___

## Create Data Field

### Display Name
TransportClassificationLabellingDescription

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationLabellingDescription

### Description
The labelling required.

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationLabellingDescription

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 7

___

## Create Data Field

### Display Name
TransportClassificationDocumentationDescription

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationDocumentationDescription

### Description
The documentation set required.

### Data Type
string

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationDocumentationDescription

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

### Label
field 8

___

## Create Data Field

### Display Name
TransportClassificationDate

### Qualified Name
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationDate

### Description
When derived.

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
DataField::Coco::Transport Classifications::Transport Classification::TransportClassificationDate

### Data Structure
DataStructure::Coco::Transport Classifications::Transport Classification

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
coco_pharma.dangerous_goods_consignment_records

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 1

___

## Create Data Field

### Display Name
ShipmentDispatchDate

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentDispatchDate

### Description
When dispatched.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentDispatchDate

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 2

___

## Create Data Field

### Display Name
CarrierIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::CarrierIdentifier

### Description
The carrier.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::CarrierIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 3

___

## Create Data Field

### Display Name
ShipmentShipToAddress

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentShipToAddress

### Description
The destination.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentShipToAddress

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 4

___

## Create Data Field

### Display Name
TransportClassificationCode

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::TransportClassificationCode

### Description
The UN number declared.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::TransportClassificationCode

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 5

___

## Create Data Field

### Display Name
ShipmentQuantity

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentQuantity

### Description
The quantity shipped.

### Data Type
float

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentQuantity

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 6

___

## Create Data Field

### Display Name
ShipmentUnit

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentUnit

### Description
The unit.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::ShipmentUnit

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 7

___

## Create Data Field

### Display Name
DeclarationSignatoryIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::DeclarationSignatoryIdentifier

### Description
The certificated signatory, by pseudonym.

### Data Type
string

### Position
8

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::DeclarationSignatoryIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 8

___

## Create Data Field

### Display Name
DeclarationSignedTimestamp

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::DeclarationSignedTimestamp

### Description
When signed.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::DeclarationSignedTimestamp

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

### Label
field 9

___

## Create Data Field

### Display Name
CertificateIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::CertificateIdentifier

### Description
The signatory's dangerous goods certificate.

### Data Type
string

### Position
10

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Declaration::CertificateIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Declaration

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
coco_pharma.dangerous_goods_consignment_records

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Label
field 1

___

## Create Data Field

### Display Name
DocumentType

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentType

### Description
Declaration, safety data sheet, handling instructions or other.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentType

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Label
field 2

___

## Create Data Field

### Display Name
DocumentIdentifier

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentIdentifier

### Description
The document.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentIdentifier

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

### Label
field 3

___

## Create Data Field

### Display Name
DocumentDate

### Qualified Name
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentDate

### Description
Its date.

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
DataField::Coco::Dangerous Goods Consignment Records::Consignment Document::DocumentDate

### Data Structure
DataStructure::Coco::Dangerous Goods Consignment Records::Consignment Document

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
coco_pharma.in_transit_temperature_readings

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
DeviceIdentifier

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceIdentifier

### Description
The device.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceIdentifier

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Label
field 1

___

## Create Data Field

### Display Name
ShipmentIdentifier

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::ShipmentIdentifier

### Description
The consignment the device travelled with.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::ShipmentIdentifier

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Label
field 2

___

## Create Data Field

### Display Name
DeviceReadingTimestamp

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceReadingTimestamp

### Description
When.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceReadingTimestamp

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Label
field 3

___

## Create Data Field

### Display Name
DeviceReadingTemperature

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceReadingTemperature

### Description
The temperature, in degrees Celsius.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceReadingTemperature

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Label
field 4

___

## Create Data Field

### Display Name
DeviceLocation

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceLocation

### Description
The device's reported location, if it reports one.

### Data Type
string

### Position
5

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceLocation

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

### Label
field 5

___

## Create Data Field

### Display Name
DeviceType

### Qualified Name
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceType

### Description
Logger or live monitor.

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
DataField::Coco::In-Transit Temperature Readings::Temperature Reading::DeviceType

### Data Structure
DataStructure::Coco::In-Transit Temperature Readings::Temperature Reading

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
coco_pharma.cold_chain_transit_records

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 1

___

## Create Data Field

### Display Name
ProductCode

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ProductCode

### Description
The product shipped.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ProductCode

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 2

___

## Create Data Field

### Display Name
BatchIdentifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::BatchIdentifier

### Description
The batch.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::BatchIdentifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 3

___

## Create Data Field

### Display Name
DeviceIdentifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::DeviceIdentifier

### Description
The device the record came from.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::DeviceIdentifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 4

___

## Create Data Field

### Display Name
ShipmentTransitStartTimestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitStartTimestamp

### Description
When monitoring began.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitStartTimestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 5

___

## Create Data Field

### Display Name
ShipmentTransitEndTimestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitEndTimestamp

### Description
When monitoring ended.

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitEndTimestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 6

___

## Create Data Field

### Display Name
ShipmentTransitMinimumTemperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitMinimumTemperature

### Description
The lowest temperature recorded.

### Data Type
float

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitMinimumTemperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 7

___

## Create Data Field

### Display Name
ShipmentTransitMaximumTemperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitMaximumTemperature

### Description
The highest temperature recorded.

### Data Type
float

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitMaximumTemperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

### Label
field 8

___

## Create Data Field

### Display Name
ShipmentTransitRecordCompleteFlag

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitRecordCompleteFlag

### Description
Whether the record has no gaps.

### Data Type
boolean

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
DataField::Coco::Cold Chain Transit Records::Transit Temperature Record::ShipmentTransitRecordCompleteFlag

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Transit Temperature Record

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
coco_pharma.cold_chain_transit_records

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
ExcursionIdentifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionIdentifier

### Description
The excursion.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionIdentifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 1

___

## Create Data Field

### Display Name
ShipmentIdentifier

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 2

___

## Create Data Field

### Display Name
ExcursionStartTimestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionStartTimestamp

### Description
When the range was left.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionStartTimestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 3

___

## Create Data Field

### Display Name
ExcursionEndTimestamp

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionEndTimestamp

### Description
When it was regained.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionEndTimestamp

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 4

___

## Create Data Field

### Display Name
ExcursionDuration

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionDuration

### Description
How long, in minutes.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionDuration

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 5

___

## Create Data Field

### Display Name
ExcursionMaximumTemperature

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionMaximumTemperature

### Description
The extreme temperature reached.

### Data Type
float

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionMaximumTemperature

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

### Label
field 6

___

## Create Data Field

### Display Name
ExcursionType

### Qualified Name
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionType

### Description
Temperature excursion or monitoring gap.

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
DataField::Coco::Cold Chain Transit Records::Excursion Detection::ExcursionType

### Data Structure
DataStructure::Coco::Cold Chain Transit Records::Excursion Detection

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
coco_pharma.carrier_transit_events

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
ShipmentIdentifier

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentIdentifier

### Description
The consignment.

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
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentIdentifier

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Label
field 1

___

## Create Data Field

### Display Name
CarrierIdentifier

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::CarrierIdentifier

### Description
The carrier.

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
DataField::Coco::Carrier Transit Events::Transit Event::CarrierIdentifier

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Label
field 2

___

## Create Data Field

### Display Name
ShipmentTransitEventType

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventType

### Description
Collected, handed over, delayed, delivered or exception.

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
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventType

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Label
field 3

___

## Create Data Field

### Display Name
ShipmentTransitEventTimestamp

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventTimestamp

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
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventTimestamp

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Label
field 4

___

## Create Data Field

### Display Name
ShipmentTransitEventLocation

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventLocation

### Description
Where.

### Data Type
string

### Position
5

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
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventLocation

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

### Label
field 5

___

## Create Data Field

### Display Name
ShipmentTransitEventDescription

### Qualified Name
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventDescription

### Description
The carrier's description.

### Data Type
string

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
DataField::Coco::Carrier Transit Events::Transit Event::ShipmentTransitEventDescription

### Data Structure
DataStructure::Coco::Carrier Transit Events::Transit Event

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
