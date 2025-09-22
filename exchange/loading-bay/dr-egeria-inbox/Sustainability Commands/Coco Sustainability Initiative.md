#Coco #Sustainability 
# Create Regulation Article
>	A RegulationArticle entity is an article in a regulation. Dividing a regulation  simplifies planning and execution.

## Display Name
>	Input Required: True

>	Description: Name of the  definition.

>	Alternative Labels: Name


## Summary
>	Input Required: False

>	Description: Summary of the definition.


## Description
>	Input Required: False

>	Description: Description of the contents of the definition.


## Domain Identifier
>	Input Required: False

>	Description: Integer representing the governance domain. All domains is 0.

>	Default Value: 0


## Document Identifier
>	Input Required: False

>	Description: A user supplied identifier for the governance document.

>	Alternative Labels: Doc Id


## Version Identifier
>	Input Required: False

>	Description: Published  version identifier.


## Scope
>	Input Required: False

>	Description: Scope of the definition.


## Importance
>	Input Required: False

>	Description: Importance of the definition.


## Implications
>	Input Required: False

>	Description: List of implications.


## Outcomes
>	Input Required: False

>	Description: List of desired outcomes.


## Results
>	Input Required: False

>	Description: A list of expected results.


## Status
>	Input Required: False

>	Description: The status of the agreement. There is a list of valid values that this conforms to.

>	Alternative Labels: Definition Status

>	Valid Values: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED; ACTIVE'; DEPRECATED; OTHER

>	Default Value: DRAFT


## User Defined Status
>	Input Required: False

>	Description: Only valid if Product Status is set to OTHER. User defined & managed status values.


## Qualified Name
>	Input Required: False

>	Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	Input Required: False

>	Description: A system generated unique identifier.

>	Alternative Labels: Guid; guid

```mermaid
---
title: Governance Definition - Operate Coco Pharmaceuticals in an increasingly sustainable way [667c6480-a90a-4fd4-9022-8da646e203d2]
---
flowchart LR
%%{init: {"flowchart": {"htmlLabels": false}} }%%

1@{ shape: doc, label: "*Governance Strategy*
Operate Coco Pharmaceuticals in an increasingly sustainable way"}
2@{ shape: text, label: "*Scope*
Across Coco Pharmaceuticals"}
3@{ shape: text, label: "*Importance*
High"}
2~~~3
4@{ shape: doc, label: "*Threat*
The price of ignoring sustainability"}
4==>|"Governance Driver Link"|1
5@{ shape: doc, label: "*Regulation*
Corporate Sustainability Reporting Directive (CSRD)"}
5==>|"Governance Driver Link"|1
6@{ shape: doc, label: "*Governance Principle*
Avoid using harmful materials"}
1==>|"Governance Response"|6
7@{ shape: doc, label: "*Governance Approach*
Measure harmful emissions"}
1==>|"Governance Response"|7
8@{ shape: doc, label: "*Governance Approach*
New Sustainability Governance Domain"}
1==>|"Governance Response"|8
style 1 color:#FFFFFF, fill:#006400, stroke:#000000
style 2 color:#000000, fill:#F9F7ED, stroke:#b7c0c7
style 3 color:#000000, fill:#F9F7ED, stroke:#b7c0c7
style 4 color:#FFFFFF, fill:#006400, stroke:#000000
style 5 color:#FFFFFF, fill:#006400, stroke:#000000
style 6 color:#FFFFFF, fill:#006400, stroke:#000000
style 7 color:#FFFFFF, fill:#006400, stroke:#000000
style 8 color:#FFFFFF, fill:#006400, stroke:#000000
```


___
```mermaid  
%%{init: {"flowchart": {"htmlLabels": false}} }%%

flowchart LR

1@{ shape: doc, label: "*Governance Approach* New Sustainability Governance Domain"}

2@{ shape: text, label: "*Scope* Across Coco Pharmaceuticals"}

3@{ shape: text, label: "*Importance* High"}

2 ~~~ 3

4@{ shape: doc, label: "*Governance Strategy* Operate Coco Pharmaceuticals in an increasingly sustainable way"}

4 ==>|"Governance Response"|1

5@{ shape: doc, label: "*Governance Responsibility* Sustainability leadership"}

1 ==>|"Governance Implementation"|5

6@{ shape: doc, label: "*Governance Responsibility* Sustainability Champion"}

1 ==>|"Governance Implementation"|6

7@{ shape: doc, label: "*Governance Responsibility* Deliver Sustainability Reporting Capability"}

1 ==>|"Governance Implementation"|7

style 1 color:#FFFFFF, fill:#006400, stroke:#000000

style 2 color:#000000, fill:#F9F7ED, stroke:#b7c0c7

style 3 color:#000000, fill:#F9F7ED, stroke:#b7c0c7

style 4 color:#FFFFFF, fill:#006400, stroke:#000000

style 5 color:#FFFFFF, fill:#006400, stroke:#000000

style 6 color:#FFFFFF, fill:#006400, stroke:#000000

style 7 color:#FFFFFF, fill:#006400, stroke:#000000
```