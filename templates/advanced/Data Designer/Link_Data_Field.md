___

## Link Data Field
> Link two data fields with a LinkedDataField relationship -- a relationship (or one end of a relationship) between the fields in the data's schema, such as a foreign key. Label is stored as the relationship's display name.

### Linked Data Field 1
>	**Input Required**: True

>	**Attribute Type**: Reference Name

>	**Description**: The first data field in a LinkedDataField peer relationship.


### Linked Data Field 2
>	**Input Required**: True

>	**Attribute Type**: Reference Name

>	**Description**: The second data field in a LinkedDataField peer relationship.


### Label
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: A label used to identify or categorise a relationship link.

>	**Alternative Labels**: Wire Label


### Link Relationship Type Name
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: The open metadata type name of the relationship used in a LinkedDataField connection.


### Minimum Cardinality
>	**Input Required**: False

>	**Attribute Type**: Simple Int

>	**Description**: The minimum number of times this field must appear in the containing data structure.

>	**Default Value**: 1


### Maximum Cardinality
>	**Input Required**: False

>	**Attribute Type**: Simple Int

>	**Description**: The maximum number of times this field may appear in the containing data structure (-1 means unbounded).

>	**Default Value**: 1


### Journal Entry
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: A text entry into a journal.


### Description
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: A description.


### Relationship End
>	**Input Required**: False

>	**Attribute Type**: Simple Int

>	**Description**: Which end of the relationship named by Link Relationship Type Name this link represents: 0 = the whole relationship (e.g. a relational foreign key), 1 or 2 = one end of it (e.g. in a graph schema).

>	**Default Value**: 0


### Effective From
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: The beginning of when an element is viewable.


### Effective Time
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: The time at which an element must be effective in order to be returned by the request.


### Effective To
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: The ending time at which an element is visible.


### External Source GUID
>	**Input Required**: False

>	**Attribute Type**: GUID

>	**Description**: The unique identifier of an external source.


### External Source Name
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: The name of an external source


### For Duplicate Processing
>	**Input Required**: False

>	**Attribute Type**: Bool

>	**Description**: Flag indicating if the request is to support duplicate processing.


### For Lineage
>	**Input Required**: False

>	**Attribute Type**: Bool

>	**Description**: Flag indicating if the request is to support lineage.


### Request ID
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: A user provided or system generated request id for a conversation.


### Anchor Scope IDs
>	**Input Required**: False

>	**Attribute Type**: Reference Name List

>	**Description**: A list of IDs that are anchor scopes for this element.


### Make Anchor
>	**Input Required**: False

>	**Attribute Type**: Bool

>	**Description**: Is the element at end2 an anchor to end1?

>	**Default Value**: false


___
