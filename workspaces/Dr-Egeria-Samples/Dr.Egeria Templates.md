# Create Data Dictionary
>       A Data Dictionary is an organized and curated collection of data definitions that can serve as a reference for data professionals

## Display Name
>       Input Required: True
>       Description: Name of the Data Dictionary
>       Alternative Labels: Name; Data Dictionary; Data Dict; Data Dictionary Name; Dictionary Name

## Description
>       Input Required: False
>       Description: A description of the Data Dictionary.

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Data Specification
>       A Data Specification defines the data requirements for a project or initiative. This includes the data structures , data fields and data classes.

## Display Name
>       Input Required: True
>       Description: Name of the Data Specification.
>       Alternative Labels: Data Spec; Name; Display Name; Data Specification Name; Data Specification

## Description
>       Input Required: False
>       Description: A description of the Data Specification.

## Collection Type
>       Input Required: False
>       Description: A user supplied collection type.

## Qualified Name
>       Input Required: True
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Data Structure
>       A collection of data fields that for a data specification for a data source.

## Display Name
>       Input Required: True
>       Description: Name of the data structure.
>       Alternative Labels: Name; Display Name; Data Struct; Data Structure Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## In Data Specification
>       Input Required: False
>       Description: The data specifications this structure is a member of.
>       Alternative Labels: In Data Spec

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Data Field
>       A data field is a fundamental building block for a data structure.

## Display Name
>       Input Required: True
>       Description: Name of the Data Field
>       Alternative Labels: Name; Data Field Name

## Description
>       Input Required: False
>       Description: A description of the Data Field

## Data Type
>       Input Required: True
>       Description: The data type of the data field. Point to data type valid value list if exists.
>       Valid Values: string; int; long; date; boolean; char; byte; float; double; biginteger; bigdecimal; array<string>; array<int>; map<string,string>; map<string, boolean>; map<string, int>; map<string, long>; map<string,double>; map<string, date> map<string, object>; short; map<string, array<string>>; other
>       Default Value: string

## Position
>       Input Required: False
>       Description: Position of the data field in the data structure. If 0, position is irrelevant.
>       Default Value: 0

## Minimum Cardinality
>       Input Required: False
>       Description: The minimum cardinality for a data element.
>       Alternative Labels: Min Cardinality; min cardinality
>       Default Value: 1

## Maximum Cardinality
>       Input Required: False
>       Description: The maximumcardinality for a data element.
>       Alternative Labels: max cardinality; Max Cardlinality
>       Default Value: 1

## In Data Structure
>       Input Required: False
>       Description: The data structure this field is a member of. If display name is not unique, use qualified name.
>       Alternative Labels: Data Structure

## Data Class
>       Input Required: False
>       Description: The data class that values of this data field conform to.

## Glossary Term
>       Input Required: False
>       Description: Term that provides meaning to this field.
>       Alternative Labels: Term

## isNullable
>       Input Required: False
>       Description: Can the values within the dataclass be absent?
>       Alternative Labels: Nullable
>       Default Value: true

## Minimum Length
>       Input Required: False
>       Description: 
>       Alternative Labels: Min Length

## Length
>       Input Required: False
>       Description: The length of a value for a field.

## Precision
>       Input Required: False
>       Description: The precision of a numeric

## Ordered Values
>       Input Required: False
>       Description: is this field in an ordered list?

## Units
>       Input Required: False
>       Description: An optional string indicating the units of the field.
>       Alternative Labels: gradians

## Default Value
>       Input Required: False
>       Description: Specify a default value for the data class.
>       Alternative Labels: Default

## Version Identifier
>       Input Required: False
>       Description: A user supplied version identifier.

## In Data Dictionary
>       Input Required: False
>       Description: What data dictionaries is this data field in?

## Parent Data Field
>       Input Required: False
>       Description: Optional parent field if this is a nested field.
>       Alternative Labels: Parent Field

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Data Class
>       Describes the data values that may be stored in data fields. Can be used to configure quality validatiors and data field classifiers.

## Display Name
>       Input Required: True
>       Description: Name of the data structure.
>       Alternative Labels: Data Class; Display Name; Name; Data Class Name

## Description
>       Input Required: False
>       Description: A description of the data class.

## Namespace
>       Input Required: False
>       Description: Optional namespace that scopes the field.

## Match Property Names
>       Input Required: False
>       Description: Names of the properties that are set.
>       Default Value: Can be determined by Dr. Egeria?

## Match Threshold
>       Input Required: False
>       Description: Percent of values that must match the data class specification.

## IsCaseSensitive
>       Input Required: False
>       Description: Are field values case sensitive?
>       Default Value: False

## Data Type
>       Input Required: True
>       Description: Data type for the data class.
>       Valid Values: string; int; long; date; boolean; char; byte; float; double; biginteger; bigdecimal; array<string>; array<int>; map<string,string>; map<string, boolean>; map<string, int>; map<string, long>; map<string,double>; map<string, date> map<string, object>; short; map<string, array<string>>; other

## Allow Duplicate Values
>       Input Required: False
>       Description: Allow duplicate values within the data class?
>       Default Value: true

## isNullable
>       Input Required: False
>       Description: Can the values within the dataclass be absent?
>       Alternative Labels: Nullable
>       Default Value: true

## isCaseSensitive
>       Input Required: False
>       Description: Indicates if the values in a  data class are case sensitive.
>       Alternative Labels: Case Sensitive

## Default Value
>       Input Required: False
>       Description: Specify a default value for the data class.
>       Alternative Labels: Default

## Average Value
>       Input Required: False
>       Description: Average value for the data class.
>       Alternative Labels: Average

## Value List
>       Input Required: False
>       Description: 

## Value Range From
>       Input Required: False
>       Description: Beginning range of legal values.
>       Alternative Labels: Range From

## Value Range To
>       Input Required: False
>       Description: End of valid range for value.
>       Alternative Labels: Range To

## Sample Values
>       Input Required: False
>       Description: Sample values of the data class.
>       Alternative Labels: Samples

## Data Patterns
>       Input Required: False
>       Description: prescribed format of a data field - e.g. credit card numbers. Often expressed as a regular expression.

## In Data Dictionary
>       Input Required: False
>       Description: What data dictionaries is this data field in?

## Containing Data Class
>       Input Required: False
>       Description: Data classes this is part of.
>       Alternative Labels: Containing Class

## Specializes Data Class
>       Input Required: False
>       Description: Specializes a parent  data class.

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# View Data Fields
>       Return the data fields, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: LIST; FORM; REPORT; MERMAID; DICT
>       Default Value: LIST

## Starts With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the beginning of  a field.
>       Default Value: True

## Ends With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the end of  a field.
>       Default Value: False

## Ignore Case
>       Input Required: False
>       Description: If true, ignore the difference between upper and lower characters when matching the search string.
>       Default Value: False

## AsOfTime
>       Input Required: False
>       Description: An ISO-8601 string representing the time to view the state of the repository.
>       Alternative Labels: As Of Time

## Sort Order
>       Input Required: False
>       Description: How to order the results. The sort order can be selected from a list of valid value.
>       Valid Values: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING

___


# View Data Classes
>       Return the data classes, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: LIST; FORM; REPORT; MERMAID; DICT
>       Default Value: LIST

## Starts With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the beginning of  a field.
>       Default Value: True

## Ends With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the end of  a field.
>       Default Value: False

## Ignore Case
>       Input Required: False
>       Description: If true, ignore the difference between upper and lower characters when matching the search string.
>       Default Value: False

## AsOfTime
>       Input Required: False
>       Description: An ISO-8601 string representing the time to view the state of the repository.
>       Alternative Labels: As Of Time

## Sort Order
>       Input Required: False
>       Description: How to order the results. The sort order can be selected from a list of valid value.
>       Valid Values: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING

___


# View Data Structures
>       Return the data structures, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Starts With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the beginning of  a field.
>       Default Value: True

## Ends With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the end of  a field.
>       Default Value: False

## Ignore Case
>       Input Required: False
>       Description: If true, ignore the difference between upper and lower characters when matching the search string.
>       Default Value: False

## AsOfTime
>       Input Required: False
>       Description: An ISO-8601 string representing the time to view the state of the repository.
>       Alternative Labels: As Of Time

## Sort Order
>       Input Required: False
>       Description: How to order the results. The sort order can be selected from a list of valid value.
>       Valid Values: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING

___


# View Data Specifications
>       Return the data specifications, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: LIST; FORM; DICT; MD; MERMAID; REPORT
>       Default Value: LIST

## Starts With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the beginning of  a field.
>       Default Value: True

## Ends With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the end of  a field.
>       Default Value: False

## Ignore Case
>       Input Required: False
>       Description: If true, ignore the difference between upper and lower characters when matching the search string.
>       Default Value: False

## AsOfTime
>       Input Required: False
>       Description: An ISO-8601 string representing the time to view the state of the repository.
>       Alternative Labels: As Of Time

## Sort Order
>       Input Required: False
>       Description: How to order the results. The sort order can be selected from a list of valid value.
>       Valid Values: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING

___


# View Data Dictionaries
>       Return the data dictionaries, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: LIST; FORM; DICT; MD; MERMAID; REPORT
>       Default Value: LIST

## Starts With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the beginning of  a field.
>       Default Value: True

## Ends With
>       Input Required: False
>       Description: If true, look for matches with the search string starting from the end of  a field.
>       Default Value: False

## Ignore Case
>       Input Required: False
>       Description: If true, ignore the difference between upper and lower characters when matching the search string.
>       Default Value: False

## AsOfTime
>       Input Required: False
>       Description: An ISO-8601 string representing the time to view the state of the repository.
>       Alternative Labels: As Of Time

## Sort Order
>       Input Required: False
>       Description: How to order the results. The sort order can be selected from a list of valid value.
>       Valid Values: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING

___


# Create Information Supply Chain
>       The flow of a particular type of data across a digital landscape.

## Display Name
>       Input Required: True
>       Description: Name of the Information Supply Chain
>       Alternative Labels: Name; Display Name; Supply Chain; Supply Chain Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## Scope
>       Input Required: False
>       Description: Scope of the supply chain.

## Purposes
>       Input Required: False
>       Description: A list of purposes.
>       Alternative Labels: Purpose, Purposes

## Information Supply Chain Segments
>       Input Required: False
>       Description: A list of supply chain segments that make up the supply chain.
>       Alternative Labels: Supply Chain Segments; Segments

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Information Supply Chain Segment
>       A collection of data fields that for a data specification for a data source.

## Display Name
>       Input Required: True
>       Description: Name of the Information Supply Chain
>       Alternative Labels: Name; Display Name; Supply Chain Segment; Segment Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## Scope
>       Input Required: False
>       Description: Scope of the supply chain.

## Integration Style
>       Input Required: False
>       Description: Style of integration connecting this segment.

## Estimated Volumetrics
>       Input Required: False
>       Description: Estimated volumetrics for rough analysis and planning.

## Information Supply Chain
>       Input Required: False
>       Description: The owning information supply chain for this segment.
>       Alternative Labels: Owning Supply Chain; Info Supply Chain; Parent Information Supply Chain

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Solution Blueprint
>       A solution blueprint describes the architecture of a digital service in terms of solution components.

## Display Name
>       Input Required: True
>       Description: Name of the Information Supply Chain
>       Alternative Labels: Name; Display Name; Blueprint; Blueprint Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## Version Identifier
>       Input Required: False
>       Description: A user supplied version identifier.

## Solution Components
>       Input Required: False
>       Description: Solution components that make up the blueprint.
>       Alternative Labels: Components; Solution Component; Component

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Create Solution Component
>       A reusable solution component.

## Display Name
>       Input Required: True
>       Description: Name of the solution component.
>       Alternative Labels: Name; Display Name; Solution Component Name, Component Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## Solution Component Type
>       Input Required: False
>       Description: Type of solution component.
>       Alternative Labels: Soln Component Type

## Planned Deployed Implementation Type
>       Input Required: False
>       Description: The planned implementation type for deployment.
>       Alternative Labels: Planned Deployed Impl Type

## Solution SubComponents
>       Input Required: False
>       Description: Solution components that include this one.
>       Alternative Labels: SubComponents; Sub-Components

## Solution Blueprints
>       Input Required: False
>       Description: Solution Blueprints that contain this component.
>       Alternative Labels: In Solution Blueprints

## Actors
>       Input Required: False
>       Description: Actors associated with this component.

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

## Merge Update
>       Input Required: False
>       Description: If true, only those attributes specified in the update will be updated; If false, any attributes not provided during the update will be set to None.
>       Alternative Labels: Merge
>       Default Value: True

___


# Create Solution Role
>       A collection of data fields that for a data specification for a data source.

## Name
>       Input Required: True
>       Description: Name of the role.
>       Alternative Labels: Role; Solution Role; Solution Role Name; Role Name

## Description
>       Input Required: False
>       Description: A description of the data structure.

## Title
>       Input Required: False
>       Description: Title of the role.

## Scope
>       Input Required: False
>       Description: Scope of the role.

## identifier
>       Input Required: False
>       Description: role identifier

## Domain Identifier
>       Input Required: False
>       Description: Governance domain identifier
>       Default Value: 0

## Role Type
>       Input Required: False
>       Description: Type of the role.  Currently must be GovernanceRole.
>       Alternative Labels: Role Type Name
>       Default Value: GovernanceRole

## Qualified Name
>       Input Required: False
>       Description: A unique qualified name for the element. Generated using the qualified name pattern  if not user specified.

## GUID
>       Input Required: False
>       Description: A system generated unique identifier.
>       Alternative Labels: Guid; guid

___


# Attach Information Supply Chain Segments
>       

## Segment1
>       Input Required: True
>       Description: The  first segment to link.
>       Alternative Labels: Segment 1; Information Supply Chain Segment 1; Info Supply Chain Segment 1

## Segment2
>       Input Required: True
>       Description: The  second segment to link.
>       Alternative Labels: Segment 2; Information Supply Chain Segment 2; Info Supply Chain Segment 2

## Link Label
>       Input Required: False
>       Description: Labels the link between two information supply chain segments.
>       Alternative Labels: Label

## Description
>       Input Required: False
>       Description: A description of the data structure.

___


# View Information Supply Chains
>       Return information supply chains filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Detailed
>       Input Required: False
>       Description: If true a more detailed set of attributes will be teturned.
>       Default Value: True

___


# View Supply Chain Segments
>       Return the data structure details, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Detailed
>       Input Required: False
>       Description: If true a more detailed set of attributes will be teturned.
>       Default Value: True

___


# View Solution Components
>       Return the data structure details, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Detailed
>       Input Required: False
>       Description: If true a more detailed set of attributes will be teturned.
>       Default Value: True

___


# View Solution Blueprints
>       Return the data structure details, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Detailed
>       Input Required: False
>       Description: If true a more detailed set of attributes will be teturned.
>       Default Value: True

___


# View Solution Roles
>       Return the data structure details, optionally filtered by the search string.

## Search String
>       Input Required: False
>       Description: An optional search string to filter results by.
>       Alternative Labels: Filter
>       Default Value: *

## Output Format
>       Input Required: False
>       Description: Optional specification of output format for the query.
>       Alternative Labels: Format
>       Valid Values: List; Form; Report; Dict
>       Default Value: List

## Detailed
>       Input Required: False
>       Description: If true a more detailed set of attributes will be teturned.
>       Default Value: True

___