# Create Digital Product
>	A Data Dictionary is an organized and curated collection of data definitions that can serve as a reference for data professionals

## Display Name
>	**Input Required**: True

>	**Description**: Name of the digital product

>	**Alternative Labels**: Name


## Description
>	**Input Required**: False

>	**Description**: Description of the contents of a product.


## Product Name
>	**Input Required**: False

>	**Description**: The external name of the digital product.


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


## Identifier
>	**Input Required**: False

>	**Description**: User specified product identifier.


## Maturity
>	**Input Required**: False

>	**Description**: Product maturity - user defined.


## Service Life
>	**Input Required**: False

>	**Description**: Estimated service lifetime of the product.


## Introduction Date
>	**Input Required**: False

>	**Description**: Date of product introduction in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.


## Next Version Date
>	**Input Required**: False

>	**Description**: Date of  the next version,  in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.


## Withdrawal Date
>	**Input Required**: False

>	**Description**: Date of planned product withdrawal in ISO 8601 format. Either all of the dates (introduction, next version, withdrawal) dates need to be supplied or none of them. Otherwise an error will occur.


## Version Identifier
>	**Input Required**: False

>	**Description**: Published product version identifier.

>	**Default Value**: 1.0


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

