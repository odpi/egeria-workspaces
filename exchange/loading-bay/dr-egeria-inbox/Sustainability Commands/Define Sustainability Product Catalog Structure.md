Define Sustainability Product Catalog Structure

# Update Digital Product Catalog
>	Create or update a Digital Product Catalog. 


## Display Name
>	**Input Required**: True

>	**Description**: Name of a catalog of digital products.

>	**Alternative Labels**: Name; Catalog Name; Marketplace

Sustainability Product Catalog
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product catalog.

Catalog of Sustainability Assets that includes reference data used in carbon accounting, interim and localized results, aggregated results and finalized sustainability reports.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainability
## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0

2025
## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

True
## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)


## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 


## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.


## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.


## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True


## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.

____
# Update Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Emissions Factors Reference Data

## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Emissions factors datasets from a variety of sources, covering different kinds of emissions factors for different regions and industries.

## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainabiliity

## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False

## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog

## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog
## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership

## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog

## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True

## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.

____
# Now lets define the folder structures within the catalog

#  Don't Create Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Industry Classifications

## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Industry classifications such as NAICS codes are used in some Emissions factors reference data as well as in some of the GHG Scope 3 reference data sets.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

General Reference Data

## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False

## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog

## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog

## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership

## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog

## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True

## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.


____

#  Don't Create Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Scope 3 Related Data
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

The Greenhouse Gas Protocol defines Scope 3 as indirect upstream and downstream carbon emissions to be included in the overall carbon accounting.  This folder contains various reference data and external references to useful datasets and information useful in Scope 3 emissions calculations.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainability
## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False
## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog
## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog
## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership
## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog
## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True
## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.


____

#  Don't Create Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Interim Carbon Accounting Data
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

A location for different disciplines and locations to share their interim carbon accounting analyses.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainability
## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False
## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog
## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog
## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership
## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog
## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True
## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.


____

#  Don't Create Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Audited Carbon Accounting Data
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Homogenized and aggregated carbon accounting data that has been reviewed and audited in preparation for publishing to both internal and external stakeholders.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainability
## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False
## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog
## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog
## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership
## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog
## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True
## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.

____

#  Don't Create Folder
>	Create or update a generic collection. While it can be used to create specific kinds of collections, you cannot set the collection-specific properties - so use the appropriate Dr.Egeria command to set all of the properties.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name; Folder Name; Collection Name; Collection

Sustainability Reports
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Published Sustainability Reports over time.
## Classifications
>	**Input Required**: False

>	**Description**: Optionally specify the initial classifications for a collection. Multiple classifications can be specified. 

>	**Alternative Labels**: classification


## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

>	**Alternative Labels**: Category Name

Sustainability
## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


## Is Own Anchor
>	**Input Required**: False

>	**Description**: Generally true. 

>	**Alternative Labels**: Own Anchor

>	**Default Value**: True

False
## Anchor ID
>	**Input Required**: False

>	**Description**: Anchor identity for the collection. Typically a qualified name but if display name is unique then it could be used (not recommended)

Sustainability Product Catalog
## Parent ID
>	**Input Required**: False

>	**Description**: Unique name of the parent element.

>	**Alternative Labels**: Parent; 

Sustainability Product Catalog
## Parent Relationship Type Name
>	**Input Required**: False

>	**Description**: The kind of the relationship to the parent element.

CollectionMembership
## Anchor Scope Name
>	**Input Required**: False

>	**Description**: Optional qualified name of an anchor scope.

Sustainability Product Catalog
## Parent at End1
>	**Input Required**: False

>	**Description**: Is the parent at end1 of the relationship?

>	**Default Value**: True

True
## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


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


## External Source GUID
>	**Input Required**: False

>	**Description**: Identifier of an external source that is associated with this element.


## External Source Name
>	**Input Required**: False

>	**Description**: Name of an external element that is associated with this element.

___

# Add Member->Collection  
>   Add/Remove a member to/from a collection.  
  
## Element Id  
>   **Input Required**: True  
  
>   **Description**: The name of the element to add to the collection.  
  
>   **Alternative Labels**: Member; Member Id  
  
Industry Classifications  
  
## Collection Id  
>   **Input Required**: True  
  
>   **Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.  
  
>   **Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id  
  
Sustainability Product Catalog  
## Membership Rationale  
>   **Input Required**: False  
  
>   **Description**: Rationale for membership.  
  
>   **Alternative Labels**: Rationale  
  
Organizing Digital Product Catalog  
## Expression  
>   **Input Required**: False  
  
>   **Description**: Expression that describes why the element is part of this collection.

____
# Add Member->Collection  
>   Add/Remove a member to/from a collection.  
  
## Element Id  
>   **Input Required**: True  
  
>   **Description**: The name of the element to add to the collection.  
  
>   **Alternative Labels**: Member; Member Id  
  
Sustainability Data Dictionary  
  
## Collection Id  
>   **Input Required**: True  
  
>   **Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.  
  
>   **Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id  
  
Sustainability Product Catalog  
## Membership Rationale  
>   **Input Required**: False  
  
>   **Description**: Rationale for membership.  
  
>   **Alternative Labels**: Rationale  
  
Organizing Digital Product Catalog

____
# Add Member->Collection  
>   Add/Remove a member to/from a collection.  
  
## Element Id  
>   **Input Required**: True  
  
>   **Description**: The name of the element to add to the collection.  
  
>   **Alternative Labels**: Member; Member Id  
  
Glossary::Sustainability-Glossary  
  
## Collection Id  
>   **Input Required**: True  
  
>   **Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.  
  
>   **Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id  
  
Sustainability Product Catalog  
## Membership Rationale  
>   **Input Required**: False  
  
>   **Description**: Rationale for membership.  
  
>   **Alternative Labels**: Rationale  
  
Organizing Digital Product Catalog

____

# Add Member->Collection  
>   Add/Remove a member to/from a collection.  
  
## Element Id  
>   **Input Required**: True  
  
>   **Description**: The name of the element to add to the collection.  
  
>   **Alternative Labels**: Member; Member Id  
  
DataStruct::NAICS-Data-Structure  
  
## Collection Id  
>   **Input Required**: True  
  
>   **Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.  
  
>   **Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id  
  
DigitalProduct::NAICS-Codes::2022  
  
## Membership Rationale  
>   **Input Required**: False  
  
>   **Description**: Rationale for membership.  
  
>   **Alternative Labels**: Rationale  
  
Organizing Digital Product Catalog

____
   
____  
# Add Member->Collection  
>   Add/Remove a member to/from a collection.  
  
##Element Id  
>   **Input Required**: True  
  
>   **Description**: The name of the element to add to the collection.  
  
>   **Alternative Labels**: Member; Member Id  
  
DataDict::Sustainability-Data-Dictionary  
  
## Collection Id  
>   **Input Required**: True  
  
>   **Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.  
  
>   **Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id  
  
Sustainability Product Catalog  
  
## Membership Rationale  
>   **Input Required**: False  
  
>   **Description**: Rationale for membership.  
  
>   **Alternative Labels**: Rationale  
  
Organizing Digital Product Catalog

____
