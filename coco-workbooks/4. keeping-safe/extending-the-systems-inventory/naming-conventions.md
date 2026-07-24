# Coco Pharmaceuticals Naming Conventions

> **Author:** Gary Geeke (Infrastructure Lead)
> **Version:** 0.1
> **Status:** ACTIVE
> **Date:** 2026-07-23
> **Description:** Naming conventions used across Coco Pharmaceuticals and its subsidiary sites (Austin, Bucharest). This file creates the root collection that will hold all naming standard rules, and defines the first rule covering IT system identifiers.

---

___

## Create Root Collection

### Display Name
Naming Conventions

### Description
Master collection of naming standard rules used across Coco Pharmaceuticals, including its recently acquired subsidiaries Coco Pharmaceuticals Austin (manufacturing plant, Texas, USA) and EKG Pharmaceuticals (Bucharest, Romania). These rules promote consistency in how systems, data assets, people and processes are identified and described across the enterprise.

### Purpose
Provide a single authoritative reference for all naming conventions so that metadata loaded into the Egeria open metadata ecosystem uses consistent, predictable identifiers and display names.

### Content Status
ACTIVE

### Version Identifier
0.1

### Authors
Gary Geeke

### Qualified Name
Collection::CocoPharma::NamingConventions

___

## Create Naming Standard Rule

### Display Name
IT System Identifier — Coco Pharmaceuticals Austin

### Domain Identifier
IT_INFRASTRUCTURE

### Summary
System identifiers for IT assets at the Austin manufacturing plant follow the pattern AUS-SYS-{NNN}, where NNN is a zero-padded three-digit sequence number.

### Description
Each IT system at the Coco Pharmaceuticals Austin (Texas, USA) manufacturing plant is assigned a unique system identifier at the time it is recorded in the asset inventory.  The identifier is composed of three parts separated by hyphens:

1. **Site prefix** — the fixed string `AUS` identifying the Austin site.
2. **Asset-type segment** — the fixed string `SYS` indicating this is a system-level asset (as opposed to a subsystem, component, or individual device).
3. **Sequence number** — a three-digit integer, zero-padded to three places, assigned sequentially as each system is added to the inventory (e.g. `001`, `002`, … `045`).

Example identifiers: `AUS-SYS-001`, `AUS-SYS-002`, `AUS-SYS-045`.

Subsystems that group related systems together use a parallel scheme: `SS-AUS-{NNN}` (e.g. `SS-AUS-001`).

The same structural convention is used at the EKG Pharmaceuticals Bucharest site, substituting `EKG` as the site prefix and omitting the `AUS` segment — system identifiers there follow `SYS-{NNN}` (e.g. `SYS-001`) and subsystem identifiers follow `SS-EKG-{NNN}` (e.g. `SS-EKG-001`). A separate naming standard rule covers the EKG scheme.

### Scope
Coco Pharmaceuticals Austin manufacturing plant (Texas, USA).

### Name Patterns
- AUS-SYS-{NNN}
- SS-AUS-{NNN}

### Implementation Description
When adding a new system to the Austin asset inventory, find the highest existing sequence number in use for the relevant prefix (AUS-SYS-* or SS-AUS-*) and increment by one, zero-padding to three digits.  Record the identifier in the `system_id` (for systems) or `subsystem_id` (for subsystems) column of the inventory CSV or the corresponding Egeria asset record.

### Importance
Mandatory — all Austin plant systems must carry an identifier conforming to this rule before the asset record is published to the active governance zone.

### Outcomes
- Every Austin IT system can be unambiguously referenced by a short, human-readable identifier.
- Identifiers sort naturally in alphanumeric order, reflecting the order in which systems were added to the inventory.
- The site prefix `AUS` instantly distinguishes Austin assets from those at other Coco Pharmaceuticals sites.

### Version Identifier
0.1

### Authors
Gary Geeke

### Content Status
ACTIVE

### Qualified Name
NamingStandardRule::CocoPharma::Austin::SystemIdentifier

___

## Add Member to Collection

### Collection Id
Collection::CocoPharma::NamingConventions

### Element Id
NamingStandardRule::CocoPharma::Austin::SystemIdentifier

___

## Create Naming Standard Rule

### Display Name
IT System Identifier — EKG Pharmaceuticals Bucharest

### Domain Identifier
IT_INFRASTRUCTURE

### Summary
System identifiers for IT assets at EKG Pharmaceuticals (Bucharest, Romania) follow the pattern SYS-{NNN} for systems and SS-EKG-{NNN} for subsystems, where NNN is a zero-padded three-digit sequence number.

### Description
Each IT system at EKG Pharmaceuticals in Bucharest, Romania is assigned a unique system identifier at the time it is recorded in the asset inventory.  The identifier is composed of two parts separated by a hyphen:

1. **Asset-type prefix** — the fixed string `SYS` indicating this is a system-level asset.
2. **Sequence number** — a three-digit integer, zero-padded to three places, assigned sequentially as each system is added to the inventory (e.g. `001`, `002`, … `030`).

Example identifiers: `SYS-001`, `SYS-002`, `SYS-030`.

Subsystems that group related systems together use a slightly different scheme that incorporates the site abbreviation to distinguish EKG subsystems from those at other sites: `SS-EKG-{NNN}` (e.g. `SS-EKG-001`).

This convention pre-dates the acquisition of EKG by Coco Pharmaceuticals and was established by the EKG IT team.  It is retained as-is for continuity.  The equivalent convention at the Austin manufacturing plant uses a site-prefixed form `AUS-SYS-{NNN}` — see the Austin System Identifier naming standard rule.

### Scope
EKG Pharmaceuticals, Bucharest, Romania (wholly owned subsidiary of Coco Pharmaceuticals).

### Name Patterns
- SYS-{NNN}
- SS-EKG-{NNN}

### Implementation Description
When adding a new system to the EKG asset inventory, find the highest existing sequence number in use under the `SYS-` prefix and increment by one, zero-padding to three digits.  For a new subsystem, do the same under `SS-EKG-`.  Record the identifier in the `system_identifier` (for systems) or `subsystem_id` (for subsystems) column of the inventory CSV or the corresponding Egeria asset record.

### Importance
Mandatory — all EKG Bucharest systems must carry an identifier conforming to this rule before the asset record is published to the active governance zone.

### Outcomes
- Every EKG IT system can be unambiguously referenced by a short, human-readable identifier.
- Identifiers sort naturally in alphanumeric order, reflecting the order in which systems were added to the inventory.
- The `SS-EKG-` subsystem prefix distinguishes EKG subsystems from those at other Coco Pharmaceuticals sites.

### Version Identifier
0.1

### Authors
Gary Geeke

### Content Status
ACTIVE

### Qualified Name
NamingStandardRule::CocoPharma::EKG::SystemIdentifier

___

## Add Member to Collection

### Collection Id
Collection::CocoPharma::NamingConventions

### Element Id
NamingStandardRule::CocoPharma::EKG::SystemIdentifier

___
