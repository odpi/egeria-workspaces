[docling-Get your documents ready for gen AI](https://github.com/docling-project/docling) - Data Ingestion

Can be used standalone or in the context of the [[Data Prep Kit]]].

1. First we'll define an external references to the web pages for Docling.
2. Define an initial component for Docling - the issue seems to be that it can be deployed in many ways.

# Create External Reference
>	Create or update External Reference Elements - or sub-types Related Media, Cited Documents, External Data Source and External Model Source.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Docling - Web Site
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Docling simplifies document processing, parsing diverse formats — including advanced PDF understanding — and providing seamless integrations with the gen AI ecosystem.

## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

ML-OPs
## Reference Title
>	**Input Required**: False

>	**Description**: Title of the external reference.

>	**Alternative Labels**: Title


## Reference Abstract
>	**Input Required**: False

>	**Description**: Abstract for the remote reference.

>	**Alternative Labels**: Abstract


## Authors
>	**Input Required**: False

>	**Description**: A list of authors.

>	**Alternative Labels**: Author


## Organization
>	**Input Required**: False

>	**Description**: Organization owning the external reference.

IBM - LF AI & Data
## URL
>	**Input Required**: False

>	**Description**: URL to access the external reference.

https://docling-project.github.io/docling/
## Sources
>	**Input Required**: False

>	**Description**: A map of source strings.

>	**Alternative Labels**: Reference Sources


## License
>	**Input Required**: False

>	**Description**: The license associated with the external reference.

MIT license
## Copyright
>	**Input Required**: False

>	**Description**: The copy right associated with the external reference.


## Attribution
>	**Input Required**: False

>	**Description**: Attribution string to describe the external reference.


## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid


## Additional Properties
>	**Input Required**: False

>	**Description**: Additional user defined values organized as name value pairs in a dictionary.

____
# Create Solution Component
>	A reusable solution component.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the solution component.

>	**Alternative Labels**: Name; Display Name; Solution Component Name; Component Name

Docling-Component
## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

ML-OPs
## Description
>	**Input Required**: False

>	**Description**: A description of the data structure.

Docling simplifies document processing, parsing diverse formats — including advanced PDF understanding — and providing seamless integrations with the gen AI ecosystem.

## Status
>	**Input Required**: False

>	**Description**: The status of the solution component. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED;  ACTIVE; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## Solution Component Type
>	**Input Required**: False

>	**Description**: Type of solution component.

>	**Alternative Labels**: Soln Component Type

Python Library
## Planned Deployed Implementation Type
>	**Input Required**: False

>	**Description**: The planned implementation type for deployment.

>	**Alternative Labels**: Planned Deployed Impl Type

DeployedSoftwareComponent
## User Defined Status
>	**Input Required**: False

>	**Description**: Supporting user managed lifecycle statuses. Only used if the Initial Status is set to OTHER.

>	**Default Value**: DRAFT


## Initial Status
>	**Input Required**: False

>	**Description**: Optional lifecycle status. If not specified, set to ACTIVE. If set to Other then the value in User Defined Status will be used.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED; ACTIVE; DISABLED; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## In Solution Components
>	**Input Required**: False

>	**Description**: Solution components that include this one.

>	**Alternative Labels**: In Solution Component; In Component

SolutionComponent::Data-Prep-Kit-Component
## In Solution Blueprints
>	**Input Required**: False

>	**Description**: Solution Blueprints that contain this component.

>	**Alternative Labels**: In Solution Blueprints

SolutionBlueprint::Initial-Data-Prep-Blueprint-for-ML-OPs::0.1
## In Information Supply Chains
>	**Input Required**: False

>	**Description**: The Information Supply Chains that this component is a member of.

>	**Alternative Labels**: In Supply Chains; In Supply Chain; In Information Supply Chain


## Actors
>	**Input Required**: False

>	**Description**: Actors associated with this component.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid


## Effective Time
>	**Input Required**: False

>	**Description**: An ISO-8601 string representing the time to use for evaluating effectivity of the elements related to this one.


## Effective From
>	**Input Required**: False

>	**Description**: A string in ISO-8601 format that defines the when an element becomes effective (visible).


## Effective To
>	**Input Required**: False

>	**Description**: A string in ISO-8601 format that defines the when an element is no longer effective (visible).


## Merge Update
>	**Input Required**: False

>	**Description**: If true, only those attributes specified in the update will be updated; If false, any attributes not provided during the update will be set to None.

>	**Alternative Labels**: Merge

>	**Default Value**: True


## Additional Properties
>	**Input Required**: False

>	**Description**: Additional user defined values organized as name value pairs in a dictionary.


## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.

