# Coco Pharmaceuticals Software Development Governance Program

> **Author:** Polly Tasker (Lead)  
> **Contributors:** Peter Profile, Callie Quartile, Lemmie Stage, Bob Nitter  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-07-14  
> **Description:** Governance definitions for the IT development team's use of AI-assisted software delivery. The team is a small group delivering a large integration project around the Coco Data Hub, and wants AI to help them move faster without losing observability, reliability, evolvability or integrity. This workbook records the governance principles sketched out in their planning meeting.

---

## Overview

The IT development team recognises that using AI to help build and evolve the Coco Data Hub integration will change many of their existing ways of working. Before adopting AI-assisted delivery at scale, the team met to agree a small set of governance principles that will apply to all software they build, whether written by a person or generated with AI assistance.

This file is the result of the team's work.

---

## Governance Principles

___

## Create Governance Principle

### Display Name
The AI did it wrong is no excuse!

### Qualified Name
CocoPharma::GovernancePrinciple::AIDidItWrongIsNoExcuse

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Description
The IT project team retains ownership of the resulting software, and responsibility for its quality, evolvability and security.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
All software should be built with observability in mind.

### Qualified Name
CocoPharma::GovernancePrinciple::ObservabilityByDesign

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Description
This observability supports verification of progress and throughput; alerting when errors occur or something fails to happen (much harder!) and diagnosis of the cause of any issues. It includes multiple perspectives - an engineer level view, a system level view and a business level view, and a business owner view.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
All software should be built with verification in mind.

### Qualified Name
CocoPharma::GovernancePrinciple::VerificationByDesign

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Description
This includes testability during development and first-failure data capture in operation.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Principle

### Display Name
All software should be built with resilience in mind.

### Qualified Name
CocoPharma::GovernancePrinciple::ResilienceByDesign

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Description
Resilience ensures these business-critical processes do not fail - or in extreme circumstances, degrade gracefully alerting the relevant people.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Governance Obligations

___

## Create Governance Obligation

### Display Name
Use AI wisely.

### Qualified Name
CocoPharma::GovernanceObligation::UseAIWisely

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Description
AI uses a lot of resources (energy, water) and so should not be used for routine, repeatable tasks, but instead to generate artifacts such as programs, data models, and documentation that will efficiently support the business.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Meeting Notes: Mapping the AI-Assisted Development Process

Having agreed the governance principles and the "use AI wisely" obligation, Polly suggested the team walk through how a simple data pipeline and data model are created today, and how AI should change that process. The aim was to determine their general approach and map out an initial development process flow, covering:

1. Extracting the specification of the source system's data feed — including its schema, valid values, and volumetrics (frequency, trigger, expected volumes, peak times, etc).
2. Extracting the schema of existing data stores (primarily Operational Data Stores, ODSs) that will be included in the data hub.
3. Designing any new data stores for the data hub.
4. Extracting the specification of the target system's API and data store — including its schema, valid values, and volumetrics (frequency, trigger, expected volumes, peak times, etc).
5. Modelling mappings between source systems, data hub stores and target systems.
6. Designing the data pipelines to move the data from the source systems to the data hub.
7. Designing the data pipelines to move the data from the data hub to the target systems.

The team saw uses for AI in every stage. The biggest *aha* realization was in the role of Egeria. They all understood that Egeria would be where all the data stores and pipelines are eventually catalogued, linked to the business context in the form of [solution blueprints](/concepts/solution-blueprint) and [information supply chains](/concepts/information-supply-chain), so that operational data could be organized and aggregated for business users. What they began to appreciate was that by involving Egeria in all phases of the engineering work, the mapping of business context to implementation evolves naturally — allowing the resulting observability to be tested and reviewed at each stage. AI could be used in the development of this business context, making open metadata a key part of the development process itself.

With this in mind, the team evolved their approach to AI-based data integration. On review, the team settled on a single high-level governance approach describing how they will develop software with AI, implemented concretely by one governance action process made up of ordered process steps.

---

## Governance Approach

___

## Create Governance Approach

### Display Name
AI-Assisted Data Integration Development

### Qualified Name
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
The Coco Data Hub integration team builds each data integration use case as an agile increment, using AI tools where they help, with Egeria capturing the business context first so that the whole engineering lifecycle — from source and destination analysis through pipeline delivery — stays linked to that context, observable, verifiable and resilient.

### Description
The team delivers Coco Data Hub integration one use case at a time. Within each use case, they use AI tools wherever appropriate to accelerate the creation of artifacts — programs, data models and documentation — while retaining full ownership of, and responsibility for, the resulting software. Business context is modelled in Egeria before implementation begins, using solution blueprints, solution roles, solution components and information supply chains, and this context anchors both business-level observability and the detailed engineering work that follows: surveying and classifying source and destination systems, mapping data into and out of the data hub, building and testing the resulting pipelines, and instrumenting them with open lineage. The detailed, ordered activities that implement this approach are defined in the "AI-Assisted Data Integration Development Process" governance action process.

### Implications
- Every use case follows the same high-level approach, even though the AI tools and techniques used at each stage may vary.
- Business-context models must be established in Egeria before, and remain linked to, all subsequent technical artifacts and pipelines.
- The governance principles and obligations agreed for software development apply throughout every stage of this approach.

### Outcomes
- Coco Data Hub integration use cases are delivered faster with AI assistance, without losing observability, verifiability, resilience or integrity.
- Business and technical views of the data hub remain continuously aligned as new use cases are added.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Governance Action Process

___

## Create Governance Action Process

### Display Name
AI-Assisted Data Integration Development Process

### Qualified Name
CocoPharma::GovernanceActionProcess::AIAssistedDataIntegrationDevelopmentProcess

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
The ordered sequence of steps used to deliver a Coco Data Hub integration use case, from establishing the agile approach through business modelling, source/destination analysis, data mapping, pipeline delivery and lineage instrumentation.

### Description
This governance action process implements the "AI-Assisted Data Integration Development" governance approach as a concrete, ordered sequence of steps. It begins when a new use case starts, and chains through the analysis, mapping, and pipeline-delivery steps in the order in which they are needed to deliver an observable, verified and resilient integration into and out of the Coco Data Hub.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Governance Mechanism

### Mechanism
CocoPharma::GovernanceActionProcess::AIAssistedDataIntegrationDevelopmentProcess

### Policy
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Label
Implements Approach

### Rationale
The governance action process is the concrete mechanism that carries out the high-level AI-assisted data integration development approach.

___

---

## Governance Action Process Steps

___

## Create Governance Action Process Step

### Display Name
Business View First, Modelled as Solution Architecture

### Qualified Name
CocoPharma::GovernanceActionProcessStep::BusinessViewFirstSolutionArchitecture

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Each use case starts with a business-level model — solution blueprints, solution roles, solution components and information supply chains — before any implementation work begins.

### Description
The first stage of each iteration is to build the business view of the use case, expressed using solution blueprints, solution roles, solution components and information supply chains. These models are pitched at a level suitable for showing to business stakeholders. They also become the anchor for business-user observability: operational statistics from the running pipelines are rolled up and attached to these concepts, so business users can see how the use case is performing in terms they understand.

### Implications
- Solution blueprints, roles, components and information supply chains must exist for a use case before implementation starts.
- Operational metrics must be designed so they can be rolled up and attached to these business-level models.

### Outcomes
- Business stakeholders can review and validate the intended design before implementation begins.
- Business users have an observability view of the use case expressed in business, not just technical, terms.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Survey and Classify Source and Destination Systems

### Qualified Name
CocoPharma::GovernanceActionProcessStep::SurveyAndClassifySourceAndDestinationSystems

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Existing systems and data stores that will act as sources or destinations are represented as assets with schema-level descriptions, surveyed, and classified with DataScope so the team understands the data they hold.

### Description
The next stage is to build or enhance the representation of any existing systems or data stores that will act as sources or destinations for the use case, where this does not already exist. These definitions include asset and schema level descriptions of the systems and data stores. Surveys are run against these assets and attached to them, so there is an understanding of the data inside. The aim is to gather enough information to add DataScope classifications to the assets.

For large sources or destinations, the team may choose to focus only on the part of the system's behaviour or data that is relevant to the use case, rather than surveying it in full. For systems or data stores that are significant — because they are involved in multiple use cases, or are business-critical — the team may also create a data dictionary and glossary describing the data they find. For source systems, the aim is a data lens describing the data needed from that source; for destination systems, the aim is a data lens describing the data being delivered to that destination. The team checks that the data lenses of the destinations can be supplied by the data lenses of the sources.

### Implications
- Every source or destination system used by a use case must be represented as an asset with schema-level detail, if it is not already.
- Surveys must be run and attached to assets to support DataScope classification.
- Large systems may be scoped down to just the data relevant to the use case; significant or multi-use-case systems warrant a data dictionary, glossary and data lens.

### Outcomes
- The team has a documented, classified understanding of the data held by every source and destination system involved.
- Data lens comparisons confirm, before pipelines are built, that destinations' data needs can be met by the sources' data.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Map Source Data to the Data Hub

### Qualified Name
CocoPharma::GovernanceActionProcessStep::MapSourceDataToDataHub

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Source data is mapped onto the data hub's stores, extending hub schemas where needed, with the Egeria Data Hub Manager keeping the hub's data dictionary current as schemas are catalogued.

### Description
The next stage is to map the data from the source systems and data stores onto the stores within the data hub. This may require the schemas of the data hub stores to be enhanced to support new types of data. As these schemas are catalogued, the Data Hub Manager in Egeria enhances the data dictionary of the data hub; the team may also wish to add to these enhancements directly.

### Implications
- Data hub schemas may need to be extended to accommodate data introduced by a new use case.
- Schema cataloguing must happen in Egeria so the Data Hub Manager can keep the data hub's data dictionary current.

### Outcomes
- The data hub's data dictionary accurately reflects the data it holds, with minimal manual maintenance.
- Source-to-hub mappings are documented and available for pipeline design and future reuse.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Build and Test Source-to-Hub Pipelines

### Qualified Name
CocoPharma::GovernanceActionProcessStep::BuildAndTestSourceToHubPipelines

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
The source-to-hub mapping is used to build and test the pipelines that extract data from the source systems and populate the data hub.

### Description
This mapping is used to build and test the data pipelines that extract data from the source systems to populate the data hub.

### Implications
- Pipeline development does not start until the corresponding source-to-hub mapping exists.

### Outcomes
- The data hub is populated with correctly mapped data from its source systems, ready to support the use case.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Map Data Hub Data to Destinations

### Qualified Name
CocoPharma::GovernanceActionProcessStep::MapDataHubDataToDestinations

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Data hub data is mapped onto each destination's API and data store, extending destination schemas where needed, ready for the hub-to-destination pipelines to be built.

### Description
Before the hub-to-destination pipelines can be built, the data held in the data hub must be mapped onto the specification of each target system's API and data store — matching the data hub's schemas to what the destination expects. This may require the destination's schema to be enhanced, or reveal that the data hub's data lens needs adjustment, to satisfy the destination's data lens. As with the earlier source-to-hub mapping, this mapping is catalogued in Egeria so it is available for pipeline design and review.

### Implications
- Every destination used by a use case must have its data-hub-to-destination mapping catalogued before pipeline development starts.
- Gaps between the data hub's schema and a destination's expected schema or data lens must be resolved as part of this mapping, not discovered during pipeline testing.

### Outcomes
- The mapping between data hub stores and each destination is documented and available before pipeline work begins.
- The hub-to-destination pipelines are built against an agreed, reviewed mapping rather than being reverse-engineered from destination errors.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Build and Test Hub-to-Destination Pipelines

### Qualified Name
CocoPharma::GovernanceActionProcessStep::BuildAndTestHubToDestinationPipelines

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
With data in place in the data hub, the team builds and tests the pipelines that deliver that data to the destination systems.

### Description
With the data in place, the team can build and test the pipelines that take data from the data hub and populate the destination systems.

### Implications
- Hub-to-destination pipeline development follows on from, and depends on, the data hub being populated by the source-to-hub pipelines.

### Outcomes
- Destination systems receive the data they need, sourced reliably from the data hub.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Instrument Pipelines with Open Lineage

### Qualified Name
CocoPharma::GovernanceActionProcessStep::InstrumentPipelinesWithOpenLineage

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
All pipelines must produce open lineage — automatically from the pipeline platform or coded directly — which Egeria aggregates and links to the relevant assets and business-context models; where the built-in aggregation isn't enough, it is augmented with additional Egeria governance actions.

### Description
All pipeline implementation should use open lineage. This is either produced automatically by the pipeline platform (such as Apache Airflow) or coded directly into the pipeline. This lineage is sent to Egeria, which aggregates it and links it to the relevant assets, solution components, solution roles, solution blueprints and information supply chains. If the built-in aggregation of operational information is not sufficient, it should be augmented with additional governance actions in Egeria.

### Implications
- Every pipeline, regardless of platform, must emit open lineage.
- Lineage must be routed to Egeria and linked to both the technical assets and the business-context models established in the first stage.
- Gaps in built-in lineage aggregation should be closed with additional Egeria governance actions, not left unaddressed.

### Outcomes
- End-to-end lineage is available from source system to destination system, linked to both technical and business views.
- Business-level observability stays current as pipelines run, without manual reconciliation.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Action Process Step

### Display Name
Review the Iteration and Feed Learnings Back

### Qualified Name
CocoPharma::GovernanceActionProcessStep::ReviewIterationAndFeedLearningsBack

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
At the end of each use case, the team reviews how the iteration went — including how well AI assistance worked at each stage — and feeds any lessons back into the approach, the process and the governance definitions themselves.

### Description
Once the use case's pipelines are built, tested and instrumented with lineage, the team holds a short retrospective before starting the next use case. This looks at where AI tools helped and where they didn't, whether the resulting business and technical models remained linked and observable as intended, and whether the governance principles, obligation and process steps still fit. Any changes are proposed as updates to this governance approach, its process, or its metrics, rather than being left as informal team knowledge.

### Implications
- A retrospective must be held at the end of every use case, before starting the next.
- Findings that suggest a change to the approach, process steps or metrics must be raised as an update to this governance definition, not just discussed informally.

### Outcomes
- The approach improves iteration by iteration, based on real experience of using AI across the pipeline lifecycle.
- Governance definitions stay current with how the team actually works, rather than drifting out of date.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Linking the Process Steps

___

## Link First Process Step

### Governance Action Process
CocoPharma::GovernanceActionProcess::AIAssistedDataIntegrationDevelopmentProcess

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BusinessViewFirstSolutionArchitecture

### Guard
start-project

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BusinessViewFirstSolutionArchitecture

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::SurveyAndClassifySourceAndDestinationSystems

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::SurveyAndClassifySourceAndDestinationSystems

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::MapSourceDataToDataHub

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::MapSourceDataToDataHub

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BuildAndTestSourceToHubPipelines

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BuildAndTestSourceToHubPipelines

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::MapDataHubDataToDestinations

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::MapDataHubDataToDestinations

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BuildAndTestHubToDestinationPipelines

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::BuildAndTestHubToDestinationPipelines

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::InstrumentPipelinesWithOpenLineage

### Guard
supplies-artifacts-to

___

---

___

## Link Next Process Step

### Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::InstrumentPipelinesWithOpenLineage

### Next Governance Action Process Step
CocoPharma::GovernanceActionProcessStep::ReviewIterationAndFeedLearningsBack

### Guard
iteration-complete

___

---

## Governance Metrics

___

## Create Governance Metric

### Display Name
AI-Generated Artifact Review Rate

### Qualified Name
CocoPharma::GovernanceMetric::AIGeneratedArtifactReviewRate

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Measures the proportion of AI-generated artifacts — code, data models, pipeline definitions, documentation — that are reviewed and approved by a team member before being merged or deployed.

### Description
This metric tracks adherence to the "AI did it wrong is no excuse!" principle, under which the IT project team retains ownership of, and responsibility for, everything it delivers, regardless of how it was produced. It is calculated as (number of AI-generated artifacts reviewed and approved by a team member / total number of AI-generated artifacts merged or deployed) × 100. The target is 100%.

### Implications
- Requires AI-generated artifacts to be identifiable as such, so they can be tracked separately from human-authored ones.
- Requires a recorded review and approval step before an AI-generated artifact is merged or deployed.

### Outcomes
- Gives the team visibility into whether AI-assisted delivery is being combined with proper human oversight.
- Surfaces any drift towards merging AI output without review before it becomes a quality or security problem.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Pipeline Lineage Coverage

### Qualified Name
CocoPharma::GovernanceMetric::PipelineLineageCoverage

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Measures the proportion of production data pipelines that emit open lineage successfully captured by Egeria and linked to their assets, solution components, solution roles, solution blueprints and information supply chains.

### Description
This metric tracks adherence to the "built with observability in mind" principle and the "Instrument Pipelines with Open Lineage" process step. It is calculated as (number of production pipelines with lineage captured and linked in Egeria / total number of production pipelines) × 100. The target is 100%. Gaps indicate pipelines whose behaviour cannot be verified through Egeria and may need additional governance actions to close the aggregation gap.

### Implications
- Requires every production pipeline to be catalogued in Egeria as an asset.
- Requires lineage capture to be checked as part of moving a pipeline into production, not added as an afterthought.

### Outcomes
- Gives business and engineering stakeholders confidence that the observability promised by the approach is actually in place.
- Identifies pipelines needing additional governance actions to close lineage aggregation gaps.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Governance Metric

### Display Name
Routine-Task AI Usage Rate

### Qualified Name
CocoPharma::GovernanceMetric::RoutineTaskAIUsageRate

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Measures the proportion of AI tool usage on the project that was spent on routine, repeatable tasks rather than on generating artifacts such as programs, data models and documentation.

### Description
This metric tracks adherence to the "use AI wisely" obligation, which discourages using AI for routine, repeatable tasks because of the resources (energy, water) AI consumes, and instead directs its use towards artifact generation that efficiently supports the business. It is calculated as (AI usage classified as routine or repeatable / total recorded AI usage) × 100, based on the team's own periodic self-classification of their AI usage. The target is a low and, ideally, declining percentage.

### Implications
- Requires the team to periodically classify their own AI usage as either "artifact generation" or "routine/repeatable", since this cannot easily be measured automatically.
- Requires this classification to be reviewed, for example during the iteration retrospective, rather than left unexamined.

### Outcomes
- Keeps the resource cost of AI use visible and discussable, rather than invisible.
- Gives the team a concrete, trackable signal for whether they are following the "use AI wisely" obligation in practice, not just in principle.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Governance Role and Responsibility

___

## Create Governance Role

### Display Name
AI-Assisted Delivery Reviewer

### Headcount
1

### Description
Reviews and approves AI-generated artifacts — code, data models, pipeline definitions, documentation — before they are merged or deployed as part of the Coco Data Hub integration project, and confirms that DataScope and privacy classifications have been correctly applied where source or destination data is personal or sensitive.

### Qualified Name
CocoPharma::GovernanceRole::AIAssistedDeliveryReviewer

### Scope
Coco Data Hub integration project

### Version Identifier
1.0

___

---

___

## Create Governance Responsibility

### Display Name
Review and Approve AI-Generated Artifacts

### Qualified Name
CocoPharma::GovernanceResponsibility::ReviewAndApproveAIGeneratedArtifacts

### Domain Identifier
SOFTWARE_DEVELOPMENT

### Scope
Coco Data Hub integration project

### Summary
Before any AI-generated artifact is merged or deployed, a team member holding the AI-Assisted Delivery Reviewer role reviews and approves it, and checks that any personal or sensitive data it touches has the correct DataScope and privacy classifications.

### Description
This responsibility puts the "AI did it wrong is no excuse!" principle into practice: it names who is accountable for reviewing AI-generated work before it goes live, rather than leaving ownership as a collective, unassigned expectation. Where an artifact relates to a source or destination system surveyed and classified in the "Survey and Classify Source and Destination Systems" process step, the reviewer also confirms that DataScope and privacy classifications correctly reflect the data involved.

### Implications
- Every AI-generated artifact must be reviewed and approved by the holder of this responsibility before merge or deployment.
- Where an artifact touches personal or sensitive data, the reviewer confirms DataScope and privacy classifications are correct, in line with Coco Pharmaceuticals' privacy obligations.

### Outcomes
- The team retains real, evidenced ownership of AI-generated work, not just a stated principle.
- The "AI-Generated Artifact Review Rate" metric has a clear, accountable source of truth.

### Authors
- Polly Tasker (Lead)
- Peter Profile
- Callie Quartile
- Lemmie Stage
- Bob Nitter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::AIAssistedDeliveryReviewer

### Assignment Type
Governance Responsibility

### Scope Element
CocoPharma::GovernanceResponsibility::ReviewAndApproveAIGeneratedArtifacts

### Description
Assigns the AI-Assisted Delivery Reviewer role responsibility for reviewing and approving AI-generated artifacts on the Coco Data Hub integration project.

___

---

## Linking to the Data Governance Program

This software development governance program does not stand alone: the Coco Data Hub integration pipelines built under it will handle personal and sensitive data already governed by the Coco Pharmaceuticals data governance program. The links below connect the two.

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Governance Policy 2
CocoPharma::GovernancePrinciple::PrivacyByDesign

### Label
Privacy alignment

### Description
Pipelines built under the AI-assisted data integration approach must honour privacy-by-design, established in the Coco Pharmaceuticals data governance program, wherever they carry personal data between source systems, the data hub, and destination systems.

___

---

___

## Link Governance Policies

### Governance Policy 1
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Governance Policy 2
CocoPharma::GovernanceObligation::PersonalDataClassifiedBySensitivity

### Label
Classification alignment

### Description
The DataScope classification work done in the "Survey and Classify Source and Destination Systems" process step is how this approach fulfils the data governance program's obligation that personal data be classified by sensitivity.

___

---

___

## Link Governance Response

### Driver
CocoPharma::Regulation::GDPR

### Policy
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Rationale
Source and destination systems integrated through the Coco Data Hub may hold personal data in scope of GDPR, so this development approach is also a governance response to that regulation, alongside the data governance program's existing policies.

___

---

## Governance Folio

A folio is a collection of governance definitions that a specific role is responsible for. This folio groups the definitions in this workbook under the Senior Software Manager, the software development governance domain lead (`CocoPharma::GovernanceRole::SeniorSoftwareManager`, Polly Tasker), following the pattern established for the other domain leads in the Coco Pharmaceuticals data governance program.

___

## Create Folio

### Display Name
Senior Software Manager — Governance Folio

### Qualified Name
CocoPharma::Folio::SeniorSoftwareManager

### Description
The governance definitions owned by the Senior Software Manager (Polly Tasker), the software development governance domain lead. This folio covers the software development governance program: the principles and obligation governing AI-assisted delivery, the approach and action process — with its steps — for AI-assisted data integration development, the metrics used to measure effectiveness, and the responsibility for reviewing AI-generated artifacts.

### Purpose
Provides Polly Tasker with a single view of all software development governance definitions she is responsible for authoring, maintaining, and enforcing.

### Category
Governance Folio

### Authors
Polly Tasker

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Link Assignment Scope

### Assigned Actor
CocoPharma::GovernanceRole::SeniorSoftwareManager

### Assignment Type
Governance Folio

### Scope Element
CocoPharma::Folio::SeniorSoftwareManager

### Description
Assigns the Senior Software Manager role responsibility for all governance definitions collected in the Software Development Governance Folio.

___

---

### Folio Members

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernancePrinciple::AIDidItWrongIsNoExcuse

### Membership Rationale
The Senior Software Manager is accountable for ensuring the engineering team retains ownership of software quality regardless of how much of it is AI-generated.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernancePrinciple::ObservabilityByDesign

### Membership Rationale
Observability is a core software development standard the Senior Software Manager is responsible for embedding in every engineering team's practice.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernancePrinciple::VerificationByDesign

### Membership Rationale
Verification practices, including testability and first-failure data capture, are software development standards owned by the Senior Software Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernancePrinciple::ResilienceByDesign

### Membership Rationale
Resilience of business-critical software is a software development governance standard set by the Senior Software Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceObligation::UseAIWisely

### Membership Rationale
Responsible, resource-conscious use of AI tooling in engineering is set and monitored by the Senior Software Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceApproach::AIAssistedDataIntegrationDevelopment

### Membership Rationale
This is the Senior Software Manager's definition of how the software development team uses AI to deliver the Coco Data Hub integration.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcess::AIAssistedDataIntegrationDevelopmentProcess

### Membership Rationale
The Senior Software Manager owns the concrete process that implements the AI-assisted development approach.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::BusinessViewFirstSolutionArchitecture

### Membership Rationale
Ensures every use case starts with a business-level model, a standard the Senior Software Manager sets for the engineering team.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::SurveyAndClassifySourceAndDestinationSystems

### Membership Rationale
Governs how the engineering team surveys and classifies source and destination systems before building pipelines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::MapSourceDataToDataHub

### Membership Rationale
Governs how source data is mapped into the data hub, a standard owned by the Senior Software Manager.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::BuildAndTestSourceToHubPipelines

### Membership Rationale
Defines the standard for building and testing source-to-hub pipelines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::MapDataHubDataToDestinations

### Membership Rationale
Governs how data hub data is mapped to destination systems ahead of pipeline delivery.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::BuildAndTestHubToDestinationPipelines

### Membership Rationale
Defines the standard for building and testing hub-to-destination pipelines.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::InstrumentPipelinesWithOpenLineage

### Membership Rationale
Sets the lineage instrumentation standard the Senior Software Manager requires of every pipeline.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceActionProcessStep::ReviewIterationAndFeedLearningsBack

### Membership Rationale
Ensures the engineering team's retrospective learnings are fed back into governance, under the Senior Software Manager's oversight.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceMetric::AIGeneratedArtifactReviewRate

### Membership Rationale
Tracks whether AI-generated work is reviewed before release, a key measure the Senior Software Manager uses to monitor engineering quality.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceMetric::PipelineLineageCoverage

### Membership Rationale
Tracks whether pipelines meet the observability standard the Senior Software Manager has set.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceMetric::RoutineTaskAIUsageRate

### Membership Rationale
Tracks compliance with the "use AI wisely" obligation the Senior Software Manager is accountable for.

### Membership Status
VALIDATED

___

---

___

## Add Member to Collection

### Collection Id
CocoPharma::Folio::SeniorSoftwareManager

### Element Id
CocoPharma::GovernanceResponsibility::ReviewAndApproveAIGeneratedArtifacts

### Membership Rationale
Defines the accountability the Senior Software Manager delegates to the AI-Assisted Delivery Reviewer role.

### Membership Status
VALIDATED

___

---

### Root Collection Membership

The Senior Software Manager folio is registered as a member of the organisation's root governance folios collection, alongside the other domain leads' folios, making it discoverable as part of the same group in Egeria.

___

## Add Member to Collection

### Collection Id
RootCollection::Coco::Governance Folios

### Element Id
CocoPharma::Folio::SeniorSoftwareManager

### Membership Rationale
The Senior Software Manager folio is part of the Coco Pharmaceuticals governance folios collection.

### Membership Status
VALIDATED

___
