# Coco Pharmaceuticals - Linking Systems to their Threat Models

> **Author:** Gary Geeke (IT Infrastructure Leader), for Simon Burr (Chief Information Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-11-16
> **Description:** Links four Austin systems in the systems inventory to the STRIDE threat models that Simon Burr built for them, using the MoreInformation relationship. Load as `garygeeke`, after `batch-manufacturing-threat-models.md` and the `1. coco-data-hub/extending-the-systems-inventory` notebook.

---

## Overview

Simon Burr has built a threat model for each of four Austin systems in the Batch Manufacturing and Release information supply chain: see [batch-manufacturing-threat-models.md](batch-manufacturing-threat-models.md).  Each is a solution blueprint.

A threat model is most useful when it can be found from the system it describes.  The links below attach each threat model to its system as *more information*: the system is the *Target Element* and the threat model is the *More Information Resource*.

They are in a workbook of their own because of who can load them.  The systems are in the `business-systems` governance zone.  Simon cannot read that zone, so he cannot link to the systems; I maintain the systems inventory, so I can.

| System | Qualified name | Threat model |
|---|---|---|
| Siemens Opcenter MES (Austin) | `SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601` | `CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES` |
| Rockwell FactoryTalk SCADA (Austin) | `SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610` | `CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA` |
| LabWare Enterprise LIMS (Austin) | `SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820` | `CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS` |
| Veeva Vault EBR (Austin) | `SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301` | `CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR` |

---

## Part 1: More information for each system

___

## Link More Information

### Target Element
SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601

### More Information Resource
CocoPharma::SolutionBlueprint::ThreatModel::AustinOpcenterMES

### Label
threat-model

### Description
The STRIDE threat model for Siemens Opcenter MES (Austin), maintained by the Chief Information Security Officer.

___

---
___

## Link More Information

### Target Element
SoftwareServer::AUS-SYS-023::SN-SCA-AU-20180610

### More Information Resource
CocoPharma::SolutionBlueprint::ThreatModel::AustinFactoryTalkSCADA

### Label
threat-model

### Description
The STRIDE threat model for Rockwell FactoryTalk SCADA (Austin), maintained by the Chief Information Security Officer.

___

---
___

## Link More Information

### Target Element
SoftwareServer::AUS-SYS-024::SN-LIM-AU-20190820

### More Information Resource
CocoPharma::SolutionBlueprint::ThreatModel::AustinLabWareLIMS

### Label
threat-model

### Description
The STRIDE threat model for LabWare Enterprise LIMS (Austin), maintained by the Chief Information Security Officer.

___

---
___

## Link More Information

### Target Element
SoftwareServer::AUS-SYS-026::SN-EBR-AU-20200301

### More Information Resource
CocoPharma::SolutionBlueprint::ThreatModel::AustinVeevaVaultEBR

### Label
threat-model

### Description
The STRIDE threat model for Veeva Vault EBR (Austin), maintained by the Chief Information Security Officer.

___

---
