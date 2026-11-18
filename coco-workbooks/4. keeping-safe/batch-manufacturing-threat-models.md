# Coco Pharmaceuticals - Threat Models for Batch Manufacturing and Release

> **Author:** Simon Burr (Chief Information Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-11-16
> **Description:** STRIDE threat models for four of the Austin systems in the Batch Manufacturing and Release information supply chain: the solution blueprints, the actors, the risks linked to their STRIDE threats and scoped to the components they threaten, and the controls that treat them. Load after `0. data-governance-program`, `1. coco-data-hub/strategic-supply-chain-analysis.md`, `onboarding-simon-burr.md` and `statement-of-applicability.md`.

---

## Overview

One of the tasks in the second month of my [ninety-day plan](onboarding-simon-burr.md) is to *threat model the strategic information supply chains*.  I have started with **Batch Manufacturing and Release**, because it is where a failure does the most harm: it decides whether a treatment reaches a patient, and whether what reaches them is what was approved.

The supply chain is described by solution components, and the same component is implemented by different systems in each of our three estates.  A threat model has to be about a real system, with its own operating system, interfaces and suppliers, so I have built one threat model for each system.  This workbook covers four systems at Austin, chosen because between them they carry a batch from the production line to the release decision:

| System | Inventory id | Implements | Threat model |
|---|---|---|---|
| Siemens Opcenter MES (Austin) | AUS-SYS-022 | ManufacturingExecution | `CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES` |
| Rockwell FactoryTalk SCADA (Austin) | AUS-SYS-023 | ProcessHistorian | `CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA` |
| LabWare Enterprise LIMS (Austin) | AUS-SYS-024 | LaboratoryInformationManagement | `CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS` |
| Veeva Vault EBR (Austin) | AUS-SYS-026 | ElectronicBatchRecord | `CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR` |

The facts about each system - its platform, patch level and interfaces - come from the systems inventory that Gary Geeke loaded in [extending-the-systems-inventory](../1.%20coco-data-hub/extending-the-systems-inventory/README.md).

### The method

I use the STRIDE method, following Egeria's [Threat Modelling](https://egeria-project.org/egeria-solutions/threat-modelling/overview/) solution:

1. **Model the system.**  Each threat model is a *solution blueprint*.  Its members are the solution components that the system implements and exchanges data with, which already exist in the supply chain, and the *actors* - legitimate and malicious - that are considered.
2. **Elicit the threats.**  For each system I ask the six STRIDE questions of its components and data flows.  Each concrete answer is a *risk*, rated for likelihood and impact, linked to its STRIDE threat and scoped to the component it threatens.
3. **Choose the mitigations.**  Each risk is linked to the *governance controls* that treat it.  Where the control is already in the [statement of applicability](statement-of-applicability.md) the risk is linked to that Annex A control, which gives the statement its "risk treatment" justification.  Otherwise a new control is defined here.

The six STRIDE threats are in Egeria's Core Content Pack, so every model links to the same six: `Threat::STRIDE::Spoofing`, `Threat::STRIDE::Tampering`, `Threat::STRIDE::Repudiation`, `Threat::STRIDE::InformationDisclosure`, `Threat::STRIDE::DenialOfService` and `Threat::STRIDE::ElevationOfPrivilege`.

### What is in this workbook

* 7 actors (solution roles)
* 1 threat model for the supply chain as a whole and 4 for individual systems (solution blueprints)
* 15 risks, each linked to its STRIDE threat and scoped to a solution component
* 9 new governance controls, and links to 7 of the Annex A controls in the statement of applicability
* links from my task and from the information supply chain to the threat models, and from the Chief Information Security Officer's folio

The links from each *system* to its threat model are in [batch-manufacturing-threat-model-links.md](batch-manufacturing-threat-model-links.md), which is loaded by Gary Geeke.  The systems are in the infrastructure zones, which I cannot read - a finding in its own right, recorded in section 6.

### STRIDE coverage

| System | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| Siemens Opcenter MES (Austin) | Batch steps signed under a shared operator login | Production order or recipe altered between SAP and the shop floor | MES audit trail lost or forged on its way to the SIEM | - | Ransomware on the MES server halts the Austin lines | - |
| Rockwell FactoryTalk SCADA (Austin) | Spoofed telemetry reported to the MES as genuine process data | Critical setpoint changed without authorisation | - | - | Unpatched control system host taken out of service | Vendor remote support used to reach other plant systems |
| LabWare Enterprise LIMS (Austin) | - | Test result altered to pass an out-of-specification batch | - | Bulk extraction of quality control and formulation data | - | LIMS administrator grants themselves approval rights |
| Veeva Vault EBR (Austin) | Batch released under a Qualified Person's stolen identity | - | Release decision cannot be proved to be the Qualified Person's | Batch records exposed through over-broad access in the cloud service | Batch release blocked by an outage of the service or its identity provider | - |

An empty cell does not mean that the category does not apply.  It means that this first pass did not find a risk worth recording, and it is a prompt for the next review.

---

## Part 1: Actors

The people and organizations considered in every model: four with legitimate access and three kinds of attacker.

___

## Create Solution Role

### Display Name
Production Operator

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::ProductionOperator

### Description
A trained operator on the manufacturing floor who executes and signs the steps of a batch.  Starts with an individual account, access to the shop-floor terminals and physical access to the line.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
Quality Control Analyst

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::QualityControlAnalyst

### Description
A laboratory analyst who registers samples, runs tests and enters or reviews results.  Starts with an individual account in the laboratory systems.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
Qualified Person

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::QualifiedPerson

### Description
The person legally responsible for certifying that a batch may be released to a market.  Starts with the authority to sign a release decision electronically.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
System Administrator

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::SystemAdministrator

### Description
A member of the site IT or automation team who administers a manufacturing or quality system.  Starts with privileged accounts and access to configuration.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
External Attacker

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Description
A criminal group or other outsider seeking to extort the company, steal its intellectual property or disrupt supply.  Starts with no access, and gains a foothold through phishing, an exposed service or stolen credentials.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
Malicious Insider

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::MaliciousInsider

### Description
An employee or contractor who misuses the access they were legitimately given, whether for gain, under pressure to meet a target, or to hide a mistake.  Starts with a valid account and knowledge of how the process works.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Solution Role

### Display Name
Compromised Supplier

### Qualified Name
CocoPharma::SolutionRole::ThreatModel::CompromisedSupplier

### Description
An equipment vendor, software supplier or service provider whose remote access, software update or cloud tenancy is used as the route in.  Starts with trusted access that the company does not fully control.

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
## Part 2: The supply chain threat model

The blueprint for the supply chain as a whole.  It holds the system threat models as its children, so that the picture for the supply chain is the sum of the pictures for its systems.

___

## Create Solution Blueprint

### Display Name
Batch Manufacturing and Release Threat Model

### Qualified Name
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Description
The threat model for the Batch Manufacturing and Release information supply chain.  It brings together the threat models of the systems that implement the supply chain's components.  The first four cover the Austin systems that carry a batch from the production line to the release decision; the Bucharest and original Coco Pharmaceuticals systems follow.

### Purpose
Threat model of the Batch Manufacturing and Release information supply chain using the STRIDE method.

### Category
Threat Model

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Membership Rationale
Considered in every system threat model for this supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Solution Role
CocoPharma::SolutionRole::ThreatModel::MaliciousInsider

### Membership Rationale
Considered in every system threat model for this supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Solution Role
CocoPharma::SolutionRole::ThreatModel::CompromisedSupplier

### Membership Rationale
Considered in every system threat model for this supply chain.

### Membership Status
VALIDATED

___

---
## Part 3: The system threat models

### 3.1 Siemens Opcenter MES (Austin)

The manufacturing execution system at the Austin plant, which directs and records each production step.  The review covers its shop-floor terminals, its interfaces to the process control system, the electronic batch record, the quality management system and SAP, its use of Active Directory, and the forwarding of its audit trail.

What the systems inventory says about it:

* Runs on Windows Server 2022, patched in September 2024.
* Authenticates users against Active Directory over LDAPS.
* Forwards its 21 CFR Part 11 audit trail to the SIEM as syslog over UDP, which is neither authenticated nor reliable.
* Exchanges batch record events with Veeva Vault EBR, and production orders with SAP S/4HANA, in real time.

___

## Create Solution Blueprint

### Display Name
Siemens Opcenter MES (Austin) Threat Model

### Qualified Name
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Description
The manufacturing execution system at the Austin plant, which directs and records each production step.  The review covers its shop-floor terminals, its interfaces to the process control system, the electronic batch record, the quality management system and SAP, its use of Active Directory, and the forwarding of its audit trail.  System inventory identifier: AUS-SYS-022.

### Purpose
Threat model of Siemens Opcenter MES (Austin) using the STRIDE method.

### Category
Threat Model

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Blueprint Child

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Blueprint Child
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Membership Rationale
One of the systems that implements the supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Component1
CocoPharma::SolutionComponent::ManufacturingExecution

### Membership Rationale
The component that Opcenter MES implements.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Membership Rationale
Receives batch record events from the MES over a bidirectional interface.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Component1
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Membership Rationale
Receives the deviations that the MES raises on batch completion.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Component1
CocoPharma::SolutionComponent::EquipmentQualificationRegister

### Membership Rationale
The MES checks that equipment is qualified before it is used.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ProductionOperator

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Solution Role
CocoPharma::SolutionRole::ThreatModel::SystemAdministrator

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Solution Role
CocoPharma::SolutionRole::ThreatModel::MaliciousInsider

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
### 3.2 Rockwell FactoryTalk SCADA (Austin)

The supervisory control system at the Austin plant, which monitors and controls the bioreactors, filling lines and environmental systems and is the source of the process parameters in the batch record.  The review covers its operator and engineering workstations, the telemetry it sends to the MES, vendor remote support and the forwarding of its audit logs.

What the systems inventory says about it:

* Runs on Windows 10 IoT Enterprise 21H2, last patched in August 2024: the oldest patch level of the systems reviewed.
* Streams telemetry and alarms to the MES over OPC-UA.
* Forwards operator setpoint changes and controller events to the SIEM as syslog over UDP.
* The equipment vendor provides remote support.

___

## Create Solution Blueprint

### Display Name
Rockwell FactoryTalk SCADA (Austin) Threat Model

### Qualified Name
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Description
The supervisory control system at the Austin plant, which monitors and controls the bioreactors, filling lines and environmental systems and is the source of the process parameters in the batch record.  The review covers its operator and engineering workstations, the telemetry it sends to the MES, vendor remote support and the forwarding of its audit logs.  System inventory identifier: AUS-SYS-023.

### Purpose
Threat model of Rockwell FactoryTalk SCADA (Austin) using the STRIDE method.

### Category
Threat Model

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Blueprint Child

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Blueprint Child
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Membership Rationale
One of the systems that implements the supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Component1
CocoPharma::SolutionComponent::ProcessHistorian

### Membership Rationale
The process parameters captured from plant instrumentation come from this system.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Component1
CocoPharma::SolutionComponent::ManufacturingExecution

### Membership Rationale
Receives equipment status, alarms and setpoint values from the control system.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Membership Rationale
Process parameters become part of the batch record.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ProductionOperator

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Solution Role
CocoPharma::SolutionRole::ThreatModel::SystemAdministrator

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Solution Role
CocoPharma::SolutionRole::ThreatModel::CompromisedSupplier

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
### 3.3 LabWare Enterprise LIMS (Austin)

The laboratory information management system in the Austin quality control laboratory, which holds the test results that decide whether raw materials and finished product meet their specification.  The review covers result entry and approval, the instrument interface from the chromatography system, the automatic raising of deviations, and the daily extract to the data lake.

What the systems inventory says about it:

* Runs on Red Hat Enterprise Linux 8.9, patched in October 2024.
* Receives completed chromatography results from Waters Empower.
* Raises a deviation in Veeva Vault QMS automatically for each out-of-specification result.
* A service account extracts results, sample data and instrument metadata daily over JDBC for the data lake.

___

## Create Solution Blueprint

### Display Name
LabWare Enterprise LIMS (Austin) Threat Model

### Qualified Name
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Description
The laboratory information management system in the Austin quality control laboratory, which holds the test results that decide whether raw materials and finished product meet their specification.  The review covers result entry and approval, the instrument interface from the chromatography system, the automatic raising of deviations, and the daily extract to the data lake.  System inventory identifier: AUS-SYS-024.

### Purpose
Threat model of LabWare Enterprise LIMS (Austin) using the STRIDE method.

### Category
Threat Model

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Blueprint Child

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Blueprint Child
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Membership Rationale
One of the systems that implements the supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Component1
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Membership Rationale
The component that LabWare LIMS implements.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Component1
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Membership Rationale
Receives a deviation whenever the LIMS records an out-of-specification result.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Membership Rationale
Test results and certificates of analysis become part of the batch record.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Solution Role
CocoPharma::SolutionRole::ThreatModel::QualityControlAnalyst

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Solution Role
CocoPharma::SolutionRole::ThreatModel::SystemAdministrator

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Solution Role
CocoPharma::SolutionRole::ThreatModel::MaliciousInsider

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
### 3.4 Veeva Vault EBR (Austin)

The electronic batch record service used at Austin for batch review and release.  It is software as a service, with sign-on through Entra ID.  The review covers the Qualified Person's release signature, the disposition decisions arriving from the quality management system, access to batch records by people outside the company, and dependence on the service and its identity provider.

What the systems inventory says about it:

* Software as a service: the company controls configuration and access, not the platform.
* Sign-on is through Entra ID using SAML.
* Receives batch disposition decisions and Qualified Person release approvals from Veeva Vault QMS.
* Holds the complete record of each batch for the life of the retention obligation.

___

## Create Solution Blueprint

### Display Name
Veeva Vault EBR (Austin) Threat Model

### Qualified Name
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Description
The electronic batch record service used at Austin for batch review and release.  It is software as a service, with sign-on through Entra ID.  The review covers the Qualified Person's release signature, the disposition decisions arriving from the quality management system, access to batch records by people outside the company, and dependence on the service and its identity provider.  System inventory identifier: AUS-SYS-026.

### Purpose
Threat model of Veeva Vault EBR (Austin) using the STRIDE method.

### Category
Threat Model

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Blueprint Child

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Blueprint Child
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Membership Rationale
One of the systems that implements the supply chain.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Component1
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Membership Rationale
The component that Veeva Vault EBR implements.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Component1
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Membership Rationale
The Qualified Person reviews and certifies the batch in this system.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Component1
CocoPharma::SolutionComponent::ManufacturingExecution

### Membership Rationale
Supplies batch record events and operator actions.

### Membership Status
VALIDATED

___

---
___

## Link Solution Component to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Component1
CocoPharma::SolutionComponent::DeviationAndCAPAManagement

### Membership Rationale
Supplies the disposition of deviations and the release approval.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Solution Role
CocoPharma::SolutionRole::ThreatModel::QualifiedPerson

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Solution Role
CocoPharma::SolutionRole::ThreatModel::ExternalAttacker

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Solution Role
CocoPharma::SolutionRole::ThreatModel::CompromisedSupplier

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
___

## Link Actor to Blueprint

### Blueprint
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Solution Role
CocoPharma::SolutionRole::ThreatModel::MaliciousInsider

### Membership Rationale
Considered in this review.

### Membership Status
VALIDATED

___

---
## Part 4: The risks

Each risk is created, linked to the STRIDE threat that gives rise to it, and scoped to the solution component it threatens.  The likelihood and impact are in the description and the overall rating is the importance.

### 4.1 Siemens Opcenter MES (Austin)

___

## Create Risk

### Display Name
Batch steps signed under a shared operator login

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::SharedOperatorLogin

### Domain Identifier
Security

### Summary
A shared or borrowed login on a shop-floor terminal is used to execute and sign a production step, so the batch record names the wrong person.

### Description
A shared or borrowed login on a shop-floor terminal is used to execute and sign a production step, so the batch record names the wrong person.  **System:** Siemens Opcenter MES (Austin) (AUS-SYS-022).  **Likelihood:** Medium - shared terminals and shift pressure make it tempting.  **Impact:** High - a signature that cannot be trusted undermines the whole batch record.  **Overall rating:** High.

### Implications
- Every step in a batch record is attributable to one identified, qualified person
- Shared and generic accounts are not present on shop-floor terminals

### Importance
High

### Category
STRIDE - Spoofing

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Spoofing

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::SharedOperatorLogin

### Rationale
A step can be signed by somebody other than the person named.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::SharedOperatorLogin

### Scope Reference
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
threatened-component

### Description
Operators sign production steps at shared terminals on the line.

___

---
___

## Create Risk

### Display Name
Production order or recipe altered between SAP and the shop floor

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::ProductionOrderAltered

### Domain Identifier
Security

### Summary
A production order, bill of materials or recipe parameter is changed in transit or in the MES after approval, so a batch is made to something other than the approved process.

### Description
A production order, bill of materials or recipe parameter is changed in transit or in the MES after approval, so a batch is made to something other than the approved process.  **System:** Siemens Opcenter MES (Austin) (AUS-SYS-022).  **Likelihood:** Low - needs access to the interface or the MES database.  **Impact:** Critical - product made outside its specification may reach patients.  **Overall rating:** High.

### Implications
- Production orders and recipes executed on the line match what was approved
- Changes between approval and execution are detected

### Importance
High

### Category
STRIDE - Tampering

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Tampering

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::ProductionOrderAltered

### Rationale
Orders and recipes can be changed after approval without detection.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::ProductionOrderAltered

### Scope Reference
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
threatened-component

### Description
The MES receives production orders hourly from SAP and holds the recipes executed on the line.

___

---
___

## Create Risk

### Display Name
MES audit trail lost or forged on its way to the SIEM

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::AuditTrailLostInTransit

### Domain Identifier
Security

### Summary
Audit events sent as syslog over UDP are dropped, or forged events are injected, so an operator or administrator can plausibly deny an action and an investigation cannot rely on the record.

### Description
Audit events sent as syslog over UDP are dropped, or forged events are injected, so an operator or administrator can plausibly deny an action and an investigation cannot rely on the record.  **System:** Siemens Opcenter MES (Austin) (AUS-SYS-022).  **Likelihood:** High - UDP gives no delivery guarantee and no authentication.  **Impact:** Medium - the MES keeps its own trail, but the independent copy is what makes it credible.  **Overall rating:** High.

### Implications
- The independent copy of the audit trail is complete and its origin is authenticated
- A gap in the audit trail is detected within a day

### Importance
High

### Category
STRIDE - Repudiation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Repudiation

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::AuditTrailLostInTransit

### Rationale
The independent record of who did what can be incomplete or forged.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::AuditTrailLostInTransit

### Scope Reference
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
threatened-component

### Description
The MES forwards operator actions, batch record edits and e-signature events to the SIEM.

___

---
___

## Create Risk

### Display Name
Ransomware on the MES server halts the Austin lines

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Domain Identifier
Security

### Summary
Ransomware reaches the MES server from the corporate network and encrypts it.  Without the MES no production step can be authorised or recorded, so the lines stop.

### Description
Ransomware reaches the MES server from the corporate network and encrypts it.  Without the MES no production step can be authorised or recorded, so the lines stop.  **System:** Siemens Opcenter MES (Austin) (AUS-SYS-022).  **Likelihood:** Medium - the MES talks to corporate systems hourly.  **Impact:** Critical - production stops and batches in progress may be lost.  **Overall rating:** Critical.

### Implications
- The MES can be restored within its recovery objective from a backup that ransomware cannot reach
- Malware on the corporate network cannot reach the MES

### Importance
Critical

### Category
STRIDE - Denial of service

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::DenialOfService

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Rationale
It is a single point of failure for production at the site.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Scope Reference
CocoPharma::SolutionComponent::ManufacturingExecution

### Label
threatened-component

### Description
The MES is a Windows server with interfaces to corporate systems.

___

---
### 4.2 Rockwell FactoryTalk SCADA (Austin)

___

## Create Risk

### Display Name
Spoofed telemetry reported to the MES as genuine process data

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SpoofedTelemetry

### Domain Identifier
Security

### Summary
A device on the plant network impersonates the control system and sends false equipment status or process values to the MES, which records them in the batch record.

### Description
A device on the plant network impersonates the control system and sends false equipment status or process values to the MES, which records them in the batch record.  **System:** Rockwell FactoryTalk SCADA (Austin) (AUS-SYS-023).  **Likelihood:** Low - needs a presence on the plant network.  **Impact:** High - a batch record containing false process data cannot be certified.  **Overall rating:** Medium.

### Implications
- The MES accepts process data only from authenticated control systems

### Importance
Medium

### Category
STRIDE - Spoofing

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Spoofing

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SpoofedTelemetry

### Rationale
The source of the process data is not strongly authenticated.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SpoofedTelemetry

### Scope Reference
CocoPharma::SolutionComponent::ProcessHistorian

### Label
threatened-component

### Description
Process parameters flow from the control system to the MES in real time.

___

---
___

## Create Risk

### Display Name
Critical setpoint changed without authorisation

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SetpointChanged

### Domain Identifier
Security

### Summary
A temperature, pressure or fill-volume setpoint is changed from an engineering workstation, deliberately or by mistake, outside an approved change.

### Description
A temperature, pressure or fill-volume setpoint is changed from an engineering workstation, deliberately or by mistake, outside an approved change.  **System:** Rockwell FactoryTalk SCADA (Austin) (AUS-SYS-023).  **Likelihood:** Medium - engineering workstations have broad access.  **Impact:** Critical - a batch may be out of specification, or equipment and people put at risk.  **Overall rating:** Critical.

### Implications
- Setpoints and control programs change only under an approved change
- Critical setpoints cannot be moved outside validated limits

### Importance
Critical

### Category
STRIDE - Tampering

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Tampering

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SetpointChanged

### Rationale
A changed setpoint alters the product while the record continues to look normal.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SetpointChanged

### Scope Reference
CocoPharma::SolutionComponent::ProcessHistorian

### Label
threatened-component

### Description
Setpoints for bioreactors and filling lines are held in the control system.

___

---
___

## Create Risk

### Display Name
Unpatched control system host taken out of service

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::UnpatchedControlHost

### Domain Identifier
Security

### Summary
A known vulnerability in the operating system of the control system host is exploited, or the host is caught by malware spreading on the plant network, and supervisory control is lost.

### Description
A known vulnerability in the operating system of the control system host is exploited, or the host is caught by malware spreading on the plant network, and supervisory control is lost.  **System:** Rockwell FactoryTalk SCADA (Austin) (AUS-SYS-023).  **Likelihood:** Medium - the host is more than two years behind on patches.  **Impact:** Critical - the lines must stop safely and batches in progress may be lost.  **Overall rating:** Critical.

### Implications
- Control system hosts are patched, or compensating controls are in place and recorded, within the agreed time
- The plant network is isolated from networks where malware is likely to arrive

### Importance
Critical

### Category
STRIDE - Denial of service

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::DenialOfService

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::UnpatchedControlHost

### Rationale
Its patch level is the weakest of the systems reviewed.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::UnpatchedControlHost

### Scope Reference
CocoPharma::SolutionComponent::ProcessHistorian

### Label
threatened-component

### Description
The control system host runs an operating system that is patched infrequently because of validation effort.

___

---
___

## Create Risk

### Display Name
Vendor remote support used to reach other plant systems

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::VendorAccessPivot

### Domain Identifier
Security

### Summary
The remote access given to the equipment vendor for support is used, by the vendor's staff or by an attacker who has compromised the vendor, to move from the control system to the MES and beyond.

### Description
The remote access given to the equipment vendor for support is used, by the vendor's staff or by an attacker who has compromised the vendor, to move from the control system to the MES and beyond.  **System:** Rockwell FactoryTalk SCADA (Austin) (AUS-SYS-023).  **Likelihood:** Medium - supplier compromise is a common route into operational technology.  **Impact:** Critical - an attacker gains control of production systems.  **Overall rating:** Critical.

### Implications
- A supplier can reach only the named system, for an approved purpose and time
- Supplier sessions are recorded and reviewed

### Importance
Critical

### Category
STRIDE - Elevation of privilege

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::ElevationOfPrivilege

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::VendorAccessPivot

### Rationale
Vendor access is trusted access that the company does not fully control.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::VendorAccessPivot

### Scope Reference
CocoPharma::SolutionComponent::ProcessHistorian

### Label
threatened-component

### Description
The equipment vendor has remote access for support.

___

---
### 4.3 LabWare Enterprise LIMS (Austin)

___

## Create Risk

### Display Name
Test result altered to pass an out-of-specification batch

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::TestResultAltered

### Domain Identifier
Security

### Summary
A result is changed, reprocessed or re-entered so that an out-of-specification batch appears to pass, or the out-of-specification result is suppressed before a deviation is raised.

### Description
A result is changed, reprocessed or re-entered so that an out-of-specification batch appears to pass, or the out-of-specification result is suppressed before a deviation is raised.  **System:** LabWare Enterprise LIMS (Austin) (AUS-SYS-024).  **Likelihood:** Medium - the pressure to release a batch is real and the opportunity exists.  **Impact:** Critical - a failing product is certified and reaches patients.  **Overall rating:** Critical.

### Implications
- Every change to a result is recorded with who made it, when and why
- An out-of-specification result always raises a deviation

### Importance
Critical

### Category
STRIDE - Tampering

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Tampering

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::TestResultAltered

### Rationale
A changed result changes the release decision.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::TestResultAltered

### Scope Reference
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Label
threatened-component

### Description
The LIMS holds the results that decide whether a batch meets its specification.

___

---
___

## Create Risk

### Display Name
Bulk extraction of quality control and formulation data

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::BulkExtractionOfQCData

### Domain Identifier
Security

### Summary
The service account used for the daily extract, or its credentials, is used to copy test methods, specifications and results in bulk.  For personalised treatments these reveal the formulation.

### Description
The service account used for the daily extract, or its credentials, is used to copy test methods, specifications and results in bulk.  For personalised treatments these reveal the formulation.  **System:** LabWare Enterprise LIMS (Austin) (AUS-SYS-024).  **Likelihood:** Medium - the account has broad read access and its credentials are in an integration tool.  **Impact:** High - loss of intellectual property, and of patient-linked data for personalised batches.  **Overall rating:** High.

### Implications
- Service accounts can read only what their interface needs
- Unusual extraction is detected and investigated

### Importance
High

### Category
STRIDE - Information disclosure

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::InformationDisclosure

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::BulkExtractionOfQCData

### Rationale
A broad service account is a route to the laboratory's data in bulk.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::BulkExtractionOfQCData

### Scope Reference
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Label
threatened-component

### Description
A service account reads the LIMS database daily to feed the data lake.

___

---
___

## Create Risk

### Display Name
LIMS administrator grants themselves approval rights

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::AdministratorApprovesOwnResults

### Domain Identifier
Security

### Summary
An analyst who also administers the LIMS, or who obtains an administrator's access, changes their own role so that they can approve results or alter a specification.

### Description
An analyst who also administers the LIMS, or who obtains an administrator's access, changes their own role so that they can approve results or alter a specification.  **System:** LabWare Enterprise LIMS (Austin) (AUS-SYS-024).  **Likelihood:** Low - few people have administrative access.  **Impact:** High - the independence of review in the laboratory is lost.  **Overall rating:** Medium.

### Implications
- Administrative and business roles in the quality systems are held by different people
- Role changes are reviewed independently

### Importance
Medium

### Category
STRIDE - Elevation of privilege

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::ElevationOfPrivilege

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::AdministratorApprovesOwnResults

### Rationale
Control of the roles is control of the review.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::AdministratorApprovesOwnResults

### Scope Reference
CocoPharma::SolutionComponent::LaboratoryInformationManagement

### Label
threatened-component

### Description
Roles in the LIMS decide who may enter, review and approve results.

___

---
### 4.4 Veeva Vault EBR (Austin)

___

## Create Risk

### Display Name
Batch released under a Qualified Person's stolen identity

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseUnderStolenIdentity

### Domain Identifier
Security

### Summary
An attacker phishes a Qualified Person's credentials or hijacks their session and certifies a batch for release in their name.

### Description
An attacker phishes a Qualified Person's credentials or hijacks their session and certifies a batch for release in their name.  **System:** Veeva Vault EBR (Austin) (AUS-SYS-026).  **Likelihood:** Medium - Qualified Persons are named individuals and are easy to target.  **Impact:** Critical - a batch is released without the legally required certification.  **Overall rating:** Critical.

### Implications
- A release signature cannot be made with a stolen password or a hijacked session
- A release signed from an unexpected device or place is blocked

### Importance
Critical

### Category
STRIDE - Spoofing

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Spoofing

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseUnderStolenIdentity

### Rationale
The signature is only as strong as the authentication behind it.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseUnderStolenIdentity

### Scope Reference
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
threatened-component

### Description
The certification decision is an electronic signature in a cloud service.

___

---
___

## Create Risk

### Display Name
Release decision cannot be proved to be the Qualified Person's

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseDecisionDenied

### Domain Identifier
Security

### Summary
The disposition and release approval arrive from the quality management system through an interface, so the batch record shows a decision without a signature that is bound to what the Qualified Person saw.  The decision can later be disputed.

### Description
The disposition and release approval arrive from the quality management system through an interface, so the batch record shows a decision without a signature that is bound to what the Qualified Person saw.  The decision can later be disputed.  **System:** Veeva Vault EBR (Austin) (AUS-SYS-026).  **Likelihood:** Low - disputes are rare.  **Impact:** High - an unprovable certification is a regulatory finding and weakens the company's position after a recall.  **Overall rating:** Medium.

### Implications
- Each release decision is bound to the identity of the signer and to the content of the record that was signed

### Importance
Medium

### Category
STRIDE - Repudiation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::Repudiation

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseDecisionDenied

### Rationale
The link between the signer, the decision and the record crosses an interface.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseDecisionDenied

### Scope Reference
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
threatened-component

### Description
Release approvals are passed between two systems.

___

---
___

## Create Risk

### Display Name
Batch records exposed through over-broad access in the cloud service

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::BatchRecordsOverShared

### Domain Identifier
Security

### Summary
Batch records, which for personalised treatments can be linked to a patient, are visible to contract staff, partner users or the provider's support staff beyond what they need.

### Description
Batch records, which for personalised treatments can be linked to a patient, are visible to contract staff, partner users or the provider's support staff beyond what they need.  **System:** Veeva Vault EBR (Austin) (AUS-SYS-026).  **Likelihood:** Medium - sharing in cloud services tends to widen over time.  **Impact:** High - disclosure of intellectual property and patient-linked data.  **Overall rating:** High.

### Implications
- Access to batch records is limited to named roles and reviewed
- Access by the provider's staff is controlled by contract and logged

### Importance
High

### Category
STRIDE - Information disclosure

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::InformationDisclosure

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::BatchRecordsOverShared

### Rationale
It is the most complete record of how a product is made.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::BatchRecordsOverShared

### Scope Reference
CocoPharma::SolutionComponent::ElectronicBatchRecord

### Label
threatened-component

### Description
The batch record is held in a cloud service that other organizations' staff can be given access to.

___

---
___

## Create Risk

### Display Name
Batch release blocked by an outage of the service or its identity provider

### Qualified Name
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseBlockedByOutage

### Domain Identifier
Security

### Summary
The electronic batch record service or Entra ID is unavailable, so no batch can be reviewed or certified.  Personalised treatments have a short shelf life and cannot wait.

### Description
The electronic batch record service or Entra ID is unavailable, so no batch can be reviewed or certified.  Personalised treatments have a short shelf life and cannot wait.  **System:** Veeva Vault EBR (Austin) (AUS-SYS-026).  **Likelihood:** Medium - outages of cloud services happen every year.  **Impact:** High - treatments expire before they can be released.  **Overall rating:** High.

### Implications
- Batches can be certified during an outage using a validated fallback
- The provider's recovery objective matches the shelf life of the product

### Importance
High

### Category
STRIDE - Denial of service

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Link Governance Response

### Driver
Threat::STRIDE::DenialOfService

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseBlockedByOutage

### Rationale
Neither is under the company's operational control.

___

---
___

## Link Element To Scope

### Target Element
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseBlockedByOutage

### Scope Reference
CocoPharma::SolutionComponent::BatchReviewAndCertification

### Label
threatened-component

### Description
Certification depends on two cloud services being available.

___

---
## Part 5: The mitigations

### 5.1 New controls

The controls that the reviews called for and that were not already defined.

___

## Create Governance Control

### Display Name
Individual Identification on the Shop Floor

### Qualified Name
CocoPharma::GovernanceControl::IndividualShopFloorIdentity

### Domain Identifier
Security

### Summary
Every action in a manufacturing system is taken under an individual account.  Shared and generic logins are removed from shop-floor terminals, and each electronic signature needs the operator's badge and a personal PIN.

### Description
Every action in a manufacturing system is taken under an individual account.  Shared and generic logins are removed from shop-floor terminals, and each electronic signature needs the operator's badge and a personal PIN.

### Implementation Description
Owned by the site automation teams.  Individual accounts are provisioned from Active Directory; shared terminals lock when the badge is removed.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Authenticated and Integrity-Protected System Interfaces

### Qualified Name
CocoPharma::GovernanceControl::InterfaceMessageIntegrity

### Domain Identifier
Security

### Summary
The interfaces between the manufacturing and quality systems authenticate both ends and protect each message against change, so that a record cannot be injected or altered between systems.

### Description
The interfaces between the manufacturing and quality systems authenticate both ends and protect each message against change, so that a record cannot be injected or altered between systems.

### Implementation Description
Owned by the integration team.  Mutual TLS on the REST and OPC-UA interfaces, with each system holding its own certificate, and reconciliation reports between sender and receiver.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Reliable and Tamper-Evident Audit Forwarding

### Qualified Name
CocoPharma::GovernanceControl::ReliableAuditForwarding

### Domain Identifier
Security

### Summary
The audit trail of each regulated system reaches the security monitoring system complete and in order, and a gap is detected.  The source system keeps its own copy for the retention period.

### Description
The audit trail of each regulated system reaches the security monitoring system complete and in order, and a gap is detected.  The source system keeps its own copy for the retention period.

### Implementation Description
Owned by the security operations team.  Syslog over TLS with sequence numbers in place of UDP, a daily completeness check, and write-once storage for the retained copy.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Brokered and Recorded Supplier Remote Access

### Qualified Name
CocoPharma::GovernanceControl::BrokeredSupplierRemoteAccess

### Domain Identifier
Security

### Summary
A supplier reaches a system only through a broker that the company controls: access is requested for a stated purpose, approved, limited in time, restricted to the named system and recorded.

### Description
A supplier reaches a system only through a broker that the company controls: access is requested for a stated purpose, approved, limited in time, restricted to the named system and recorded.

### Implementation Description
Owned by the security team with the site automation teams.  Standing vendor accounts and vendor-managed remote access tools on the plant network are removed.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Segregation of Duties in the Quality Systems

### Qualified Name
CocoPharma::GovernanceControl::SegregationOfDutiesInQualitySystems

### Domain Identifier
Security

### Summary
Nobody can both create a quality record and approve it, and nobody who administers a quality system has a business role in it.  Changes to roles, specifications and result calculations need a second person.

### Description
Nobody can both create a quality record and approve it, and nobody who administers a quality system has a business role in it.  Changes to roles, specifications and result calculations need a second person.

### Implementation Description
Owned by quality assurance.  Role design is reviewed at each periodic access review; administrative actions are reported to quality assurance weekly.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Phishing-Resistant Authentication for Release Signatures

### Qualified Name
CocoPharma::GovernanceControl::PhishingResistantReleaseSignature

### Domain Identifier
Security

### Summary
A batch release decision is signed with authentication that cannot be replayed or relayed by an attacker who has captured a password or a session, and the signature is bound to the content that was signed.

### Description
A batch release decision is signed with authentication that cannot be replayed or relayed by an attacker who has captured a password or a session, and the signature is bound to the content that was signed.

### Implementation Description
Owned by the identity team.  Hardware security keys for Qualified Persons, re-authentication at the point of signing, and conditional access restricted to managed devices.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Least Privilege for Service Accounts

### Qualified Name
CocoPharma::GovernanceControl::LeastPrivilegeServiceAccounts

### Domain Identifier
Security

### Summary
Each service account can reach only the data its interface needs, from the host that runs the interface, and its use is monitored for unusual volume or timing.

### Description
Each service account can reach only the data its interface needs, from the host that runs the interface, and its use is monitored for unusual volume or timing.

### Implementation Description
Owned by the database and integration teams.  Read-only views in place of table access, credentials held in a secrets store and rotated, and alerts on bulk extraction.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Batch Release Continuity Procedure

### Qualified Name
CocoPharma::GovernanceControl::BatchReleaseContinuityProcedure

### Domain Identifier
Security

### Summary
A tested procedure allows batches to be reviewed and certified when the electronic batch record service or its identity provider is unavailable, without weakening the record that is kept.

### Description
A tested procedure allows batches to be reviewed and certified when the electronic batch record service or its identity provider is unavailable, without weakening the record that is kept.

### Implementation Description
Owned by quality assurance.  A validated paper fallback with later reconciliation into the electronic record, exercised annually, and a contractual recovery objective with the service provider.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
___

## Create Governance Control

### Display Name
Authorised and Verified Process Control Changes

### Qualified Name
CocoPharma::GovernanceControl::ProcessControlChangeAuthorisation

### Domain Identifier
Security

### Summary
A change to a setpoint, recipe or control program is made only under an approved change, by a named person, and is independently verified against the approved value.

### Description
A change to a setpoint, recipe or control program is made only under an approved change, by a named person, and is independently verified against the approved value.

### Implementation Description
Owned by the site automation teams with quality assurance.  Engineering workstations are restricted, critical setpoints have limits enforced in the controller, and changes are compared daily with approved change records.

### Category
Threat Model Mitigation

### Authors
- Simon Burr

### Version Identifier
1.0

### Content Status
ACTIVE

___

---
### 5.2 Linking the risks to their controls

Each risk is linked to the controls that treat it.  The controls whose names begin `ISO27001-A-` are the Annex A controls from the [statement of applicability](statement-of-applicability.md).

___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::SharedOperatorLogin

### Mechanism
CocoPharma::GovernanceControl::IndividualShopFloorIdentity

### Rationale
Removes the shared logins and ties each signature to a badge and a personal PIN.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::SharedOperatorLogin

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-5-15-AccessControl

### Rationale
The access control policy requires individual accountability.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::ProductionOrderAltered

### Mechanism
CocoPharma::GovernanceControl::InterfaceMessageIntegrity

### Rationale
Authenticates the interface and detects a message changed in transit.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::ProductionOrderAltered

### Mechanism
CocoPharma::GovernanceControl::ProcessControlChangeAuthorisation

### Rationale
Requires recipe changes to be approved and independently verified.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::AuditTrailLostInTransit

### Mechanism
CocoPharma::GovernanceControl::ReliableAuditForwarding

### Rationale
Replaces UDP with an authenticated, sequenced transport and checks for gaps.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::AuditTrailLostInTransit

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-16-MonitoringActivities

### Rationale
Monitoring depends on the audit trail being complete.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-7-ProtectionAgainstMalware

### Rationale
Malware protection on the server.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-13-InformationBackup

### Rationale
Offline backups allow the MES to be restored.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinOpcenterMES::RansomwareHaltsMES

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-20-NetworksSecurity

### Rationale
Segmentation limits the paths from the corporate network.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SpoofedTelemetry

### Mechanism
CocoPharma::GovernanceControl::InterfaceMessageIntegrity

### Rationale
OPC-UA security with certificates authenticates the control system to the MES.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SpoofedTelemetry

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-20-NetworksSecurity

### Rationale
Segmentation limits what can reach the OPC-UA endpoint.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SetpointChanged

### Mechanism
CocoPharma::GovernanceControl::ProcessControlChangeAuthorisation

### Rationale
Requires approval and independent verification, and enforces limits in the controller.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::SetpointChanged

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-16-MonitoringActivities

### Rationale
Setpoint changes are monitored and compared with approved changes.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::UnpatchedControlHost

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-8-ManagementOfTechnicalVulnerabilities

### Rationale
Vulnerability management sets the timescale for patching or compensating.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::UnpatchedControlHost

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-8-20-NetworksSecurity

### Rationale
Segmentation is the compensating control while patches wait for validation.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::VendorAccessPivot

### Mechanism
CocoPharma::GovernanceControl::BrokeredSupplierRemoteAccess

### Rationale
Removes standing vendor access and records each session.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinFactoryTalkSCADA::VendorAccessPivot

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-5-19-SupplierRelationships

### Rationale
Supplier security requirements are agreed and monitored.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::TestResultAltered

### Mechanism
CocoPharma::GovernanceControl::SegregationOfDutiesInQualitySystems

### Rationale
The person who enters a result cannot approve it, and changes need a second person.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::TestResultAltered

### Mechanism
CocoPharma::GovernanceControl::InterfaceMessageIntegrity

### Rationale
Protects results arriving from the instruments and deviations leaving for the QMS.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::BulkExtractionOfQCData

### Mechanism
CocoPharma::GovernanceControl::LeastPrivilegeServiceAccounts

### Rationale
Restricts the account to views of what the extract needs and alerts on bulk reads.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::BulkExtractionOfQCData

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-5-15-AccessControl

### Rationale
The access control policy applies to service accounts as well as people.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinLabWareLIMS::AdministratorApprovesOwnResults

### Mechanism
CocoPharma::GovernanceControl::SegregationOfDutiesInQualitySystems

### Rationale
Separates administration from laboratory roles and reports role changes to quality assurance.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseUnderStolenIdentity

### Mechanism
CocoPharma::GovernanceControl::PhishingResistantReleaseSignature

### Rationale
Hardware keys and re-authentication at signing defeat stolen passwords and sessions.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseDecisionDenied

### Mechanism
CocoPharma::GovernanceControl::PhishingResistantReleaseSignature

### Rationale
Binds the signature to the signer and to the content signed.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseDecisionDenied

### Mechanism
CocoPharma::GovernanceControl::ReliableAuditForwarding

### Rationale
Keeps an independent record of the signing event.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::BatchRecordsOverShared

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-5-15-AccessControl

### Rationale
Access is granted by role and reviewed.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::BatchRecordsOverShared

### Mechanism
CocoPharma::GovernanceControl::ISO27001-A-5-19-SupplierRelationships

### Rationale
The provider's access is governed by the supplier agreement.

___

---
___

## Link Governance Mechanism

### Policy
CocoPharma::Risk::ThreatModel::AustinVeevaVaultEBR::ReleaseBlockedByOutage

### Mechanism
CocoPharma::GovernanceControl::BatchReleaseContinuityProcedure

### Rationale
Provides a tested fallback for review and certification.

___

---
## Part 6: Connecting the threat models

### 6.1 The task and the supply chain

The supply chain threat model is the output of my task, and it is more information about the supply chain.

___

## Link Resource To Element

### Target Element
SimonBurr::Task::Next30DaysEstablishingPhase::ThreatModelSupplyChains

### Resource
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Label
threat-model

### Description
The threat model for the Batch Manufacturing and Release information supply chain, the first of the strategic supply chains to be modelled.

### Resource Use
Related Information

___

---
___

## Link More Information

### Target Element
InformationSupplyChain::Batch Manufacturing and Release Information Supply Chain

### More Information Resource
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Label
threat-model

### Description
The STRIDE threat model for this information supply chain.

___

---
### 6.2 The Chief Information Security Officer's folio

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::SolutionBlueprint::ThreatModel::BatchManufacturing

### Membership Rationale
A threat model maintained by the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---
___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Membership Rationale
A threat model maintained by the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---
___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Membership Rationale
A threat model maintained by the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---
___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Membership Rationale
A threat model maintained by the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---
___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::ChiefInformationSecurityOfficer

### Element Id
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Membership Rationale
A threat model maintained by the Chief Information Security Officer.

### Membership Status
VALIDATED

___

---
### 6.3 The systems

Each threat model should be reachable from the system it describes, so that anyone looking at the system in the inventory can find its threats.  That needs a *MoreInformation* relationship from the system to the threat model.

I cannot create it.  The Austin systems are in the `business-systems` zone, which is readable by the infrastructure, data integration and DevOps staff, and the Chief Information Security Officer is in none of those groups.  I can see the solution components but not the systems that implement them.  Gary Geeke has created the links for me, in [batch-manufacturing-threat-model-links.md](batch-manufacturing-threat-model-links.md).

This is a finding for the security program, not just an inconvenience: the security team cannot scope a penetration test, check a patch level or investigate an incident for a system it cannot read.  I have asked Gary and Ivor to agree read access to the infrastructure zones for the security team.

---

## What comes next

* The same four systems at Bucharest, where the products are the same but the suppliers and the patch levels are not.
* The quality management system and the equipment qualification register, which complete the supply chain.
* A second pass on the empty cells in the STRIDE coverage table.
* Taking the new controls into the statement of applicability as the organization's implementation of the Annex A controls they support.
