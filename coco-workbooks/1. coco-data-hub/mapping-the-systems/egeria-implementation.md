# Implementing Egeria Open Metadata and Governance

> **Author:** Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-02
> **Description:** Links the Egeria Open Metadata and Governance solution component to the OMAG Server Platform that runs it.

---

# Overview

*Egeria Open Metadata and Governance* is a member of three strategic information supply chains, but the
[component-system mapping](data/component-system-mapping.csv) gives it no system, because Gary Geeke's inventory and
the acquired estates' inventories list business systems, not the metadata platform itself.  Egeria is nevertheless
running: these definitions live in it.  This file draws the missing `ImplementedBy` relationship, from the component
to the **Quickstart OMAG Server Platform**, which hosts the metadata access store, view server, integration daemons
and engine host that make up Egeria at Coco Pharmaceuticals.  Like the notebook's links, the relationship's role is
the estate and its description records the confidence.

The platform is catalogued by Egeria's own platform cataloguer, so it appears once the platform has started.  The
cataloguer records it under each URL it is reached by, and this file links the `https://localhost:9443` entry.

Run it as Peter Profile, after `mapping-the-systems.ipynb`:

```
dr_egeria --directive process --userid peterprofile --user_pass secret egeria-implementation.md
```

___

## Link Implemented By

### Design Element
SolutionComponent::Egeria Open Metadata and Governance::V1.0

### Implementation Element
OMAG Server Platform::https://localhost:9443

### Implementation Role
Coco core

### Description
Strong: Egeria is the metadata platform these definitions are held in; the Quickstart OMAG Server Platform hosts its metadata access store, view server, integration daemons and engine host.

___
