
1. Define the product
2. Link documentation to it
3. Add the product to the right product folder
# Create Digital Product
>	A digital product is designed to be a resuable asset that can be reliably shared within and across organizations.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name

Raw Emissions Factors
## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.

Emissions factors are used to convert from the amount of a particular fuel to the CO2 equivalence.
## Product Name
>	**Input Required**: False

>	**Description**: The external name of the digital product.
Raw Emissions Factors Data
## Status
>	**Input Required**: False

>	**Description**: The status of the digital product. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED; APPROVED_CONCEPT; UNDER_DEVELOPMENT; DEVELOPMENT_COMPLETE; APPROVED_FOR_DEPLOYMENT; ACTIVE; DISABLED; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## User Defined Status
>	**Input Required**: False

>	**Description**: Only valid if Product Status is set to OTHER. User defined & managed status values.


## Category
>	**Input Required**: False

>	**Description**: Type of product - periodic, delta, snapshot, etc. May also be user specified.

General Reference Data
## Identifier
>	**Input Required**: False

>	**Description**: User specified product identifier.

NAICS
## Maturity
>	**Input Required**: False

>	**Description**: Product maturity - user defined.

Mature
## Service Life
>	**Input Required**: False

>	**Description**: Estimated service lifetime of the product.


## Introduction Date
>	**Input Required**: False

>	**Description**: Date of product introduction in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.

1997
## Next Version Date
>	**Input Required**: False

>	**Description**: Date of  the next version,  in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.

2027
## Withdrawal Date
>	**Input Required**: False

>	**Description**: Date of planned product withdrawal in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.


## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0

2017
## Product Manager
>	**Input Required**: False

>	**Description**: Actors responsible for managing this product. Actors may be individuals, automations, etc.


## Agreements
>	**Input Required**: False

>	**Description**: A list of agreements associated with this product.  The agreements must already exist.


## Digital Subscriptions
>	**Input Required**: False

>	**Description**: 


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid

Define NAICS Codes Product

____
Link the external description of the NAICS codes to the NAICS codes product.

____
# Link External Reference Link
>	Link an external reference to a referenceable.

## Element Name
>	**Input Required**: True

>	**Description**: A referenceable to link.

>	**Alternative Labels**: Referenceable

NAICS Codes-2017
## External Reference
>	**Input Required**: True

>	**Description**: The external reference to link to.

Official NAICS Codes Details
## Label
>	**Input Required**: False

>	**Description**: Labels the link between the referenceable and the external reference.

DocumentedBy
## Description
>	**Input Required**: False

>	**Description**: A description of the link.

Details on NAICS codes can be found at the External Reference provided.

____





Add the NAICS code product to the Industry classifications product folder.

____
# Add Member->Collection
>	Add/Remove a member to/from a collection.

## Element Id
>	**Input Required**: True

>	**Description**: The name of the element to add to the collection.

>	**Alternative Labels**: Member; Member Id

DigitalProduct::NAICS-Codes-2017::2017
## Collection Id
>	**Input Required**: True

>	**Description**: The name of the collection to link to. There are many collection types, including Digital Products, Agreements and Subscriptions.

>	**Alternative Labels**: Parent; Parent Id; Collection Id; Agreement Id; Subscription Id; Digital Product Id; Folder; Folder Id

Collection::Industry-Classifications
## Membership Rationale
>	**Input Required**: False

>	**Description**: Rationale for membership.

>	**Alternative Labels**: Rationale

Organizing Digital Product Catalog
## Expression
>	**Input Required**: False

>	**Description**: Expression that describes why the element is part of this collection.


## Confidence
>	**Input Required**: False

>	**Description**: A percent confidence in the proposed adding of the member.


## Membership Status
>	**Input Required**: False

>	**Description**: The status of adding a member to a collection.

>	

VALIDATED
## User Defined Status
>	**Input Required**: False

>	**Description**: If the Member Status is Other, the user can specify their own status values.


## Steward
>	**Input Required**: False

>	**Description**: Name of the steward reviewing the proposed membership. Initially, just a string.


## Steward Type Name
>	**Input Required**: False

>	**Description**: Type of steward.


## Steward Property Name
>	**Input Required**: False

>	**Description**: Property name to discern the type of the steward.


## Source
>	**Input Required**: False

>	**Description**: Source of the member.


## Notes
>	**Input Required**: False

>	**Description**: Notes about the membership addition.


## Effective Time
>	**Input Required**: False

>	**Description**: An ISO-8601 string representing the time to use for evaluating effectivity of the elements related to this one.


## Effective From
>	**Input Required**: False

>	**Description**: A string in ISO-8601 format that defines the when an element becomes effective (visible).


## Effective To
>	**Input Required**: False

>	**Description**: A string in ISO-8601 format that defines the when an element is no longer effective (visible).


## Additional Properties
>	**Input Required**: False

>	**Description**: Additional user defined values organized as name value pairs in a dictionary.


## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.

CSV Data File::~{fileSystemName}~:/loading-bay/Sustainability Files/raw emission factor data.csv

____
