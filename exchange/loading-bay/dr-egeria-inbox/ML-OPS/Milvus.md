[Milvus | High-Performance Vector Database Built for Scale](https://milvus.io/)- Vector Indexing & Storage & RAG

____
# Create External Reference
>	Create or update External Reference Elements - or sub-types Related Media, Cited Documents, External Data Source and External Model Source.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Milvus - Web Site

## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Milvus is an open-source vector database built for GenAI applications. Install with pip, perform high-speed searches, and scale to tens of billions of vectors with minimal performance loss.

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

Milvus is an **open-source**, **cloud-native** vector database designed for high-performance similarity search on massive vector datasets. Built on top of popular vector search libraries including Faiss, HNSW, DiskANN, and SCANN, it empowers AI applications and unstructured data retrieval scenarios.
## Authors
>	**Input Required**: False

>	**Description**: A list of authors.

>	**Alternative Labels**: Author


## Organization
>	**Input Required**: False

>	**Description**: Organization owning the external reference.


## URL
>	**Input Required**: False

>	**Description**: URL to access the external reference.


## Sources
>	**Input Required**: False

>	**Description**: A map of source strings.

>	**Alternative Labels**: Reference Sources


## License
>	**Input Required**: False

>	**Description**: The license associated with the external reference.

Apache License 2.0

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

Milvus-Component

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

🐦 [Milvus](https://milvus.io/) is a high-performance vector database built for scale. It powers AI applications by efficiently organizing and searching vast amounts of unstructured data, such as text, images, and multi-modal information.

🧑‍💻 Written in Go and C++, Milvus implements hardware acceleration for CPU/GPU to achieve best-in-class vector search performance. Thanks to its [fully-distributed and K8s-native architecture](https://milvus.io/docs/overview.md#What-Makes-Milvus-so-Scalable), Milvus can scale horizontally, handle tens of thousands of search queries on billions of vectors, and keep data fresh with real-time streaming updates. Milvus also supports [Standalone mode](https://milvus.io/docs/install_standalone-docker.md) for single machine deployment. [Milvus Lite](https://milvus.io/docs/milvus_lite.md) is a lightweight version good for quickstart in python with `pip install`.
## Status
>	**Input Required**: False

>	**Description**: The status of the solution component. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED;  ACTIVE; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## Solution Component Type
>	**Input Required**: False

>	**Description**: Type of solution component.

>	**Alternative Labels**: Soln Component Type

SoftwareServer
## Planned Deployed Implementation Type
>	**Input Required**: False

>	**Description**: The planned implementation type for deployment.

>	**Alternative Labels**: Planned Deployed Impl Type

DataStore
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

____

# Link External Reference
>	Link an external reference to a referenceable.

## Element Name
>	**Input Required**: True

>	**Description**: A referenceable to link.

>	**Alternative Labels**: Referenceable

Milvus-Component

## External Reference
>	**Input Required**: True

>	**Description**: The external reference to link to.

Milvus - Web Site
## Label
>	**Input Required**: False

>	**Description**: Labels the link between the referenceable and the external reference.

Documents
## Description
>	**Input Required**: False

>	**Description**: A description of the link.

This web site documents Milvus.