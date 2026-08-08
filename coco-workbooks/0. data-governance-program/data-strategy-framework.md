# Coco Pharmaceuticals Data Strategy Framework

> **Author:** Jules Keeper (Chief Data Officer)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-07-31  
> **Description:** This document defines the solution architecture for Coco Pharmaceuticals' Data Strategy Framework, as described in the [Defining the Data Strategy](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-the-data-strategy/overview/) scenario.

---

## Overview

The Data Strategy Framework sets out the seven building blocks Coco Pharmaceuticals needs in place to become a data-driven organisation. A Multi-faceted Governance Model sits over the other six components, providing the coordinated oversight that lets them work together consistently. The remaining six components form a chain running from how employees make decisions through to how the underlying data itself is defined.

The architecture is captured as a solution blueprint containing seven solution components — one for each part of the framework — linked together with solution linking wires that show how governance oversees each component, and how the operational chain flows from decision-making back down to common data definitions.

A companion **Data Sharing Glossary** defines the shared vocabulary used across the framework, so that everyone discussing it — governance leaders, architects and employees alike — means the same thing by terms such as *Authoritative Source*, *Information Supply Chain* and *Data Hub*.

---

## Part 1: Solution Blueprint

___

## Create Solution Blueprint

### Display Name
Data Strategy Framework

### Qualified Name
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Description
The overall solution architecture for Coco Pharmaceuticals' data strategy, showing the seven components identified by Jules Keeper's Data Strategy Framework and how they relate to one another.

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Add Member to Collection

### Element Id
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Collection Id
RootCollection::Coco::Strategic Solutions

___

---

## Part 2: Solution Components

___

## Create Solution Component

### Display Name
Multi-faceted Governance Model

### Qualified Name
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Description
An integrated governance program covering data, infrastructure, privacy, security and corporate operations, coordinated across the organisation's governance leaders so the other six components of the framework work together consistently.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Data-enabled Employees

### Qualified Name
CocoPharma::SolutionComponent::DataEnabledEmployees

### Description
Provides the workforce with access to current, trustworthy information so that employees across the organisation can make data-informed decisions and continuously improve how the business operates.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Continuous Analytics and AI

### Qualified Name
CocoPharma::SolutionComponent::ContinuousAnalyticsAndAI

### Description
Analytics and AI capabilities that support discovery, validation and automated monitoring of business operations, turning data into the insight that employees use to make decisions.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Authoritative Sources

### Qualified Name
CocoPharma::SolutionComponent::AuthoritativeSources

### Description
Trusted sources of key information, typically used by multiple parts of the business, that ensure consistency in the data consumed by analytics and AI.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Optimized Information Supply Chains

### Qualified Name
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### Description
The flow of data between systems, understood, optimized and managed so that any failure is quickly detected, located and resolved without affecting the service offered, keeping the authoritative sources maintained and current.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Data-driven Systems Architecture

### Qualified Name
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### Description
The IT systems architecture that evolves to support new data and process requirements, enabling the real-time integration that the information supply chains are designed around.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Solution Component

### Display Name
Common Data Definitions

### Qualified Name
CocoPharma::SolutionComponent::CommonDataDefinitions

### Description
Shared agreements on what data is required, what it means, how it is formatted, the expected quality, granularity, update frequency and valid values, and how it can be used — the foundation that the systems architecture is built to understand.

### In Solution Blueprints
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 3: Solution Linking Wires

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::DataEnabledEmployees

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::ContinuousAnalyticsAndAI

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::AuthoritativeSources

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### Component2
CocoPharma::SolutionComponent::CommonDataDefinitions

### Label
governs

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::DataEnabledEmployees

### Component2
CocoPharma::SolutionComponent::ContinuousAnalyticsAndAI

### Label
makes decisions with

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::ContinuousAnalyticsAndAI

### Component2
CocoPharma::SolutionComponent::AuthoritativeSources

### Label
uses

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::AuthoritativeSources

### Component2
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### Label
maintained by

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### Component2
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### Label
designed by

___

---

___

## Link Solution Components

### Component1
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### Component2
CocoPharma::SolutionComponent::CommonDataDefinitions

### Label
understood through

___

---

## Part 4: Glossary

___

## Create Glossary

### Display Name
Data Sharing Glossary

### Qualified Name
Glossary::DataSharingGlossary

### Description
The shared vocabulary of terms used when discussing the Data Strategy Framework and the sharing of data across Coco Pharmaceuticals.

### Language
English

### Usage
Reference this glossary when writing or reviewing material that discusses the Data Strategy Framework, so that terms such as Authoritative Source, Information Supply Chain and Data Hub are used consistently.

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Attach Collection to Resource

### Element Id
CocoPharma::SolutionBlueprint::DataStrategyFramework

### Label
Data Sharing Glossary

### Description
Links the Data Strategy Framework solution blueprint to the glossary of shared terms used to discuss it.

### Resource Use
Related Information

### Collection Id
Glossary::DataSharingGlossary

___

---

___

## Create Glossary Term

### Display Name
Authoritative Source

### Summary
The trusted, best source of a particular type of information.

### Description
The "best" source of a particular type of information — a system formally designated and overseen by the organisation (or a trusted external party) as the trusted origin of that information.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::AuthoritativeSource

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/identifying-authoritative-sources/overview/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Information Supply Chain

### Abbreviation
ISC

### Summary
A high-level view of how data and control move through a digital environment.

### Description
A high-level depiction of how data and control move through a digital environment. It presents data flow at a level meaningful to business users and regulators, and connects to the underlying lineage-producing components that actually execute the flow so that activity, errors and volumetrics can be rolled up and audited.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::InformationSupplyChain

### URL
https://egeria-project.org/concepts/information-supply-chain/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Artificial Intelligence

### Abbreviation
AI

### Summary
Techniques that let systems perform tasks normally requiring human intelligence.

### Description
Computer systems and techniques, such as machine learning, that perform tasks which typically require human intelligence — including discovery, prediction, analysis and decision-making — over the data made available through Continuous Analytics and AI.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::ArtificialIntelligence

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Subject Area

### Summary
A topic or domain of knowledge important to the organisation.

### Description
A topic or domain of knowledge that is important to the organisation. Subject areas typically cover data that is widely shared across the business, where keeping values consistent across multiple copies has real business value.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::SubjectArea

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-subject-areas/overview/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Glossary

### Summary
A collection of semantic definitions for the meaning of data.

### Description
A collection of semantic definitions, typically focused on defining the meaning of data. A glossary's content — glossary terms, categories, term relationships and classifications — should have a clearly identified owner responsible for its quality.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::Glossary

### URL
https://egeria-project.org/practices/common-data-definitions/anatomy-of-a-glossary/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Multi-faceted Governance

### Summary
Coordinated governance spanning data, infrastructure, privacy, security and operations.

### Description
An integrated governance program covering data, infrastructure, privacy, security and corporate operations, coordinated across multiple governance leaders rather than being handed to a single team.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::MultiFacetedGovernance

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-the-data-strategy/overview/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Hub

### Summary
A collector of authoritative data stores suitable for sharing.

### Description
A collector of data stores that contain authoritative data that is suitable for sharing.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::DataHub

### URL
https://egeria-project.org/concepts/data-hub/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Dictionary

### Summary
A curated reference collection of data definitions.

### Description
An organized and curated collection of data definitions that can serve as a reference for data professionals — describing the data fields found in a particular data store, or the typical data fields within a subject area.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::DataDictionary

### URL
https://egeria-project.org/concepts/data-dictionary/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Glossary Term

### Summary
A defined meaning for a word or phrase.

### Description
Describes the meaning of a word or phrase. The definition includes examples, abbreviations and a detailed description, and the same term may have several distinct meanings, each recorded as its own glossary term.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::GlossaryTerm

### URL
https://egeria-project.org/concepts/glossary-term/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Solution Blueprint

### Summary
A collection of components that together deliver a business solution.

### Description
A collection that assembles the solution components that together deliver a business solution, visualized at a level of abstraction suited to team discussion and stakeholder agreement rather than technical specification.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::SolutionBlueprint

### URL
https://egeria-project.org/concepts/solution-blueprint/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Governance

### Summary
Directing, monitoring and controlling an organisation's use of its data.

### Description
The people, processes and technology used to direct, monitor and control an organisation's use of its data and information assets, so that they are managed consistently, securely and ethically.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::Governance

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Schema

### Summary
Describes the structure of the data held by an asset.

### Description
Describes the structure of the data associated with an asset. Schemas are represented as linked subgraphs of schema elements, starting with a root schema type and made up of schema attributes that describe individual data fields.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::Schema

### URL
https://egeria-project.org/concepts/schema/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Lineage

### Summary
Shows how data flows and is processed from origin to destination.

### Description
Shows how data flows from its origins to its various destinations, including details of the processing along the way. Lineage supports traceability, impact analysis when changes occur, and validation that operational processes are executing correctly.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::Lineage

### URL
https://egeria-project.org/features/lineage-management/overview/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Sharing Agreement

### Summary
An agreement covering the sharing of data between parties.

### Description
An agreement that indicates its subject relates to the sharing of data. The related data specifications can be attached as members of the agreement, and the responsibilities of each party are identified through agreement actor relationships.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::DataSharingAgreement

### URL
https://egeria-project.org/types/7/0711-Agreements/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Literate Governance

### Summary
Documenting governance decisions in plain language alongside the commands that implement them.

### Description
A concept, borrowed from Donald Knuth's Literate Programming, that emphasises documentation and communication in the governance process. Rather than disconnected code or rigid forms, governance officers, data stewards and engineers author integrated documents that explain _why_ a structure exists in plain natural language, right alongside the precise commands that _create_ it — so that governance decisions are made in a transparent and consistent manner.

### Glossary Name
Glossary::DataSharingGlossary

### Qualified Name
Glossary::DataSharingGlossary::LiterateGovernance

### URL
https://egeria-project.org/concepts/literate-governance/

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 5: Worked Example — Data Sharing Agreement

Authoritative Sources are only useful once the terms on which they may be consumed are made explicit. This worked
example uses the new `Create Data Sharing Agreement` command to instantiate a real agreement, and attaches it to
the Authoritative Sources solution component as a resource.

___

## Create Data Sharing Agreement

### Display Name
Authoritative Sources Data Sharing Agreement

### Agreement Type
Data Sharing Agreement

### Description
Defines the terms under which the systems designated as Authoritative Sources make their data available for consumption by Continuous Analytics and AI, and for propagation through the Optimized Information Supply Chains.

### Qualified Name
CocoPharma::Agreement::AuthoritativeSourcesDataSharingAgreement

### Authors
- Jules Keeper

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Attach Collection to Resource

### Element Id
CocoPharma::SolutionComponent::AuthoritativeSources

### Label
Data Sharing Agreement

### Description
Links the Authoritative Sources solution component to the agreement that governs how its data may be shared.

### Resource Use
Related Information

### Collection Id
CocoPharma::Agreement::AuthoritativeSourcesDataSharingAgreement

___

---

## Part 6: More Information — Solution Components to Glossary Terms

Each solution component is linked, via `Link More Information`, to the glossary term(s) in the Data Sharing
Glossary that best explain it.

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### More Information Resource
Glossary::DataSharingGlossary::Governance

### Label
Governance

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::MultiFacetedGovernanceModel

### More Information Resource
Glossary::DataSharingGlossary::MultiFacetedGovernance

### Label
Multi-faceted Governance

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::DataEnabledEmployees

### More Information Resource
Glossary::DataSharingGlossary::Glossary

### Label
Glossary

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::DataEnabledEmployees

### More Information Resource
Glossary::DataSharingGlossary::DataDictionary

### Label
Data Dictionary

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::ContinuousAnalyticsAndAI

### More Information Resource
Glossary::DataSharingGlossary::ArtificialIntelligence

### Label
Artificial Intelligence

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::AuthoritativeSources

### More Information Resource
Glossary::DataSharingGlossary::AuthoritativeSource

### Label
Authoritative Source

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::AuthoritativeSources

### More Information Resource
Glossary::DataSharingGlossary::DataSharingAgreement

### Label
Data Sharing Agreement

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### More Information Resource
Glossary::DataSharingGlossary::InformationSupplyChain

### Label
Information Supply Chain

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::OptimizedInformationSupplyChains

### More Information Resource
Glossary::DataSharingGlossary::Lineage

### Label
Lineage

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### More Information Resource
Glossary::DataSharingGlossary::DataHub

### Label
Data Hub

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::DataDrivenSystemsArchitecture

### More Information Resource
Glossary::DataSharingGlossary::Schema

### Label
Schema

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::CommonDataDefinitions

### More Information Resource
Glossary::DataSharingGlossary::GlossaryTerm

### Label
Glossary Term

___

---

___

## Link More Information

### Target Element
CocoPharma::SolutionComponent::CommonDataDefinitions

### More Information Resource
Glossary::DataSharingGlossary::SubjectArea

### Label
Subject Area

___
