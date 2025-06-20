<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Rules
* If this is a create, and qualfied name is provided, it will be used.
* If this is an update, and qualified name is provided, it is an error if it doesn't match.
* If this is an update and no qualified name provided, will try to use the display name
* If this is an update and qualified name and guid provided, then the qualified name can be changed
=> This needs work when the upsert methods are done

# foo Update Solution Component

## Display Name

Lab Processes

## Description
Test to create component that doesn't exist

## Solution Component Type
dan-test
## Planned Deployed Implementation Type
Something
## In Solution Blueprints

## Sub-Components

___

# foo Update Solution Blueprint

## Display Name
dr egerias blueprint

## Description
A quick description3

## Solution Component Type
dan-test
## Solution Components
Lab Processes
___

# foo Update Solution Component

## Display Name

Hospital Processes

## Description
Test to Update a component that exists
## Version Identifier
2
## Solution Component Type
Should succeed
## Planned Deployed Implementation Type
somehow
## Solution Blueprints

## Merge Update
False

## Solution SubComponents
SolutionComponent::Lab Processes

___


# foo Update Information Supply Chain
## Display Name
my supply chain

## Scope
universal

## Purposes
hegemony, betterment of mankind, pranks

## Description
My own personal supply chain
___

# foo Create Information Supply Chain Segment
## Display Name
first segment
## Description
A first segment description2
## Scope
Infinite
## Integration Style
Wishful Thinking
## Information Supply Chain
my supply chain

___

# foo Create Information Supply Chain Segment
## Display Name
second segment
## Description
A second segment description
## Scope
Infinite
## Integration Style
Wishful
## Information Supply Chain
my supply chain

# foo Link Segments
## Segment1

first segment

## Segment2
second segment

## Label
A link

___


# Solution Blueprints with filter: `*`

# Solution Blueprint Report - created at 2025-06-15 14:24
	Solution Blueprint  found from the search string:  `All`

# Solution Blueprint Name: dr egerias blueprint

## Qualified Name
SolutionBlueprint::dr egerias blueprint

## Description
A quick description3

## Solution Components
{ Lab Processes:	 Test to create component that doesn't exist },

## Mermaid
---
title: Components and Roles for Solution Blueprint - dr egerias blueprint [423d0074-6b8a-40f5-8116-8540220bd1c2]
---
flowchart TD
%%{init: {"flowchart": {"htmlLabels": false}} }%%

subgraph 1 [Components and Actors]
2@{ shape: text, label: "*Description*
**A quick description3**"}
3@{ shape: rect, label: "*Solution Component*
**Lab Processes**"}
end
style 1 color:#FFFFFF, fill:#3079ab, stroke:#000000
style 2 color:#000000, fill:#F9F7ED, stroke:#b7c0c7
style 3 color:#000000, fill:#dda0dd, stroke:#000000

## Guid
423d0074-6b8a-40f5-8116-8540220bd1c2


# Provenance

* Results from processing file solution-components.md on 2025-06-15 14:24
