
In this file we will:
1. Create a Data Specification Collection to hold data structures pertaining to NAICS.
2. Create a NAICS data structure for NAICS and connet it to both the Data Specification and the Data Dictionary.
3. Define data fields  and assign them to the NAICS data structure.
_____
# Create Data Specification
>	A Data Specification defines the data requirements for a project or initiative. This includes the data structures , data fields and data classes.


## Display Name
>	**Input Required**: True

>	**Description**: Name of the Data Specification.

>	**Alternative Labels**: Data Spec; Name; Display Name; Data Specification Name; Data Specification

NAICS Data Spec
## Description
>	**Input Required**: False

>	**Description**: A description of the Data Specification.

A collection of data specifications relating to NAICS codes. NAICS codes are updated every five years so this will hold structures across years, along with cross-walks.
## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

General Reference Data
## Qualified Name
>	**Input Required**: True

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid



____
# Define a data structure for NAICS codes

# Create Data Structure
>	A collection of data fields that for a data specification for a data source.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the data structure.

>	**Alternative Labels**: Name; Display Name; Data Struct; Data Structure Name

NAICS Data Structure
## Description
>	**Input Required**: False

>	**Description**: A description of the data structure.

The basic structure of NAICS codes is very simple - just a code and a title. In NAICS files, the release year is also included in fields and structures.
## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

General Reference Data
## Status
>	**Input Required**: False

>	**Description**: The status of the data structure. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED;  ACTIVE; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## In Data Specification
>	**Input Required**: False

>	**Description**: The data specifications this structure is a member of.

>	**Alternative Labels**: In Data Spec

NAICS Data Spec
## In Data Dictionary
>	**Input Required**: False

>	**Description**: What data dictionaries is this data structure in?

Sustainability Data Dictionary, General Reference Data Dictionary

## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid

_____

# Create Data Field
>	A data field is a fundamental building block for a data structure.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the Data Field

>	**Alternative Labels**: Name; Data Field Name

NAICS Code
## Description
>	**Input Required**: False

>	**Description**: A description of the Data Field

Up to a six digit number representing the NAICS code for a given economic activity. The codes also represent a coarseness or fineness of the classification. The more digits, the more precise the description of economic activity. See the related documentation. 
## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

General Reference Data
## Status
>	**Input Required**: False

>	**Description**: The status of the data field. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED;  ACTIVE; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## Data Type
>	**Input Required**: True

>	**Description**: The data type of the data field. Point to data type valid value list if exists.

>	**Valid Values**: string; int; long; date; boolean; char; byte; float; double; biginteger; bigdecimal; array(string); array(int); map(string,string); map(string, boolean); map(string, int); map(string, long); map(string,double); map(string, date) map(string, object); short; map(string, array(string)); other

>	**Default Value**: string

String
## Position
>	**Input Required**: False

>	**Description**: Position of the data field in the data structure. If 0, position is irrelevant.

>	**Default Value**: 0

1
## Minimum Cardinality
>	**Input Required**: False

>	**Description**: The minimum cardinality for a data element.

>	**Alternative Labels**: Min Cardinality; min cardinality

>	**Default Value**: 1

1
## Maximum Cardinality
>	**Input Required**: False

>	**Description**: The maximum cardinality for a data element.

>	**Alternative Labels**: max cardinality; Max Cardinality

>	**Default Value**: 1

1
## In Data Structure
>	**Input Required**: False

>	**Description**: The data structure this field is a member of. If display name is not unique, use qualified name.

>	**Alternative Labels**: Data Structure

NAICS Data Structure
## Data Class
>	**Input Required**: False

>	**Description**: The data class that values of this data field conform to.


## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.

>	**Alternative Labels**: Term


## isNullable
>	**Input Required**: False

>	**Description**: Can the values within the dataclass be absent?

>	**Alternative Labels**: Nullable

>	**Default Value**: true

False
## Minimum Length
>	**Input Required**: False

>	**Description**: 

>	**Alternative Labels**: Min Length


## Length
>	**Input Required**: False

>	**Description**: The length of a value for a field.


## Precision
>	**Input Required**: False

>	**Description**: The precision of a numeric


## Ordered Values
>	**Input Required**: False

>	**Description**: is this field in an ordered list?


## Units
>	**Input Required**: False

>	**Description**: An optional string indicating the units of the field.

>	**Alternative Labels**: gradians


## Default Value
>	**Input Required**: False

>	**Description**: Specify a default value for the data class.

>	**Alternative Labels**: Default


## Version Identifier
>	**Input Required**: False

>	**Description**: A user supplied version identifier.

2022
## In Data Dictionary
>	**Input Required**: False

>	**Description**: What data dictionaries is this data field in?

Sustainability Data Dictionary, General Reference Data Dictionary
## Parent Data Field
>	**Input Required**: False

>	**Description**: Optional parent field if this is a nested field.

>	**Alternative Labels**: Parent Field


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid

____


# Create Data Field
>	A data field is a fundamental building block for a data structure.

## Display Name
>	**Input Required**: True

>	**Description**: Name of the Data Field

>	**Alternative Labels**: Name; Data Field Name

NAICS Title
## Description
>	**Input Required**: False

>	**Description**: A description of the Data Field

The descriptive classification name of the economic activity. The NAICS documentation provides textual descriptions of the classification approach and the classifications.
## Category
>	**Input Required**: False

>	**Description**: A user specified category name that can be used for example, to define product types or agreement types.

General Reference Data
## Status
>	**Input Required**: False

>	**Description**: The status of the data field. There is a list of valid values that this conforms to.

>	**Valid Values**: DRAFT; PREPARED; PROPOSED; APPROVED; REJECTED;  ACTIVE; DEPRECATED; OTHER

>	**Default Value**: ACTIVE


## Data Type
>	**Input Required**: True

>	**Description**: The data type of the data field. Point to data type valid value list if exists.

>	**Valid Values**: string; int; long; date; boolean; char; byte; float; double; biginteger; bigdecimal; array(string); array(int); map(string,string); map(string, boolean); map(string, int); map(string, long); map(string,double); map(string, date) map(string, object); short; map(string, array(string)); other

>	**Default Value**: string

String
## Position
>	**Input Required**: False

>	**Description**: Position of the data field in the data structure. If 0, position is irrelevant.

>	**Default Value**: 0

2
## Minimum Cardinality
>	**Input Required**: False

>	**Description**: The minimum cardinality for a data element.

>	**Alternative Labels**: Min Cardinality; min cardinality

>	**Default Value**: 1

1
## Maximum Cardinality
>	**Input Required**: False

>	**Description**: The maximum cardinality for a data element.

>	**Alternative Labels**: max cardinality; Max Cardinality

>	**Default Value**: 1

1
## In Data Structure
>	**Input Required**: False

>	**Description**: The data structure this field is a member of. If display name is not unique, use qualified name.

>	**Alternative Labels**: Data Structure

NAICS Data Structure
## Data Class
>	**Input Required**: False

>	**Description**: The data class that values of this data field conform to.


## Glossary Term
>	**Input Required**: False

>	**Description**: Term that provides meaning to this field.

>	**Alternative Labels**: Term


## isNullable
>	**Input Required**: False

>	**Description**: Can the values within the dataclass be absent?

>	**Alternative Labels**: Nullable

>	**Default Value**: true

False
## Minimum Length
>	**Input Required**: False

>	**Description**: 

>	**Alternative Labels**: Min Length


## Length
>	**Input Required**: False

>	**Description**: The length of a value for a field.


## Precision
>	**Input Required**: False

>	**Description**: The precision of a numeric


## Ordered Values
>	**Input Required**: False

>	**Description**: is this field in an ordered list?


## Units
>	**Input Required**: False

>	**Description**: An optional string indicating the units of the field.

>	**Alternative Labels**: gradians


## Default Value
>	**Input Required**: False

>	**Description**: Specify a default value for the data class.

>	**Alternative Labels**: Default


## Version Identifier
>	**Input Required**: False

>	**Description**: A user supplied version identifier.

2022
## In Data Dictionary
>	**Input Required**: False

>	**Description**: What data dictionaries is this data field in?

Sustainability Data Dictionary, General Reference Data Dictionary
## Parent Data Field
>	**Input Required**: False

>	**Description**: Optional parent field if this is a nested field.

>	**Alternative Labels**: Parent Field


## Qualified Name
>	**Input Required**: False

>	**Description**: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.


## GUID
>	**Input Required**: False

>	**Description**: A system generated unique identifier.

>	**Alternative Labels**: Guid; guid