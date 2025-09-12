# View Governance Definition Context
>	List information about a governance definition and its related elements.

## Display Name
>	**Input Required**: True

>	**Description**: The unique name of the governance definition to display information for.

>	**Alternative Labels**: Name


## Output Format
>	**Input Required**: False

>	**Description**: Optional specification of output format for the query.

>	**Alternative Labels**: Format

>	**Valid Values**: LIST; FORM; REPORT; MERMAID; DICT

>	**Default Value**: LIST


## AsOfTime
>	**Input Required**: False

>	**Description**: An ISO-8601 string representing the time to view the state of the repository.

>	**Alternative Labels**: As Of Time


## Sort Order
>	**Input Required**: False

>	**Description**: How to order the results. The sort order can be selected from a list of valid value.

>	**Valid Values**: ANY; CREATION_DATE_RECENT; CREATION_DATA_OLDEST; LAST_UPDATE_RECENT; LAST_UPDATE_OLDEST; PROPERTY_ASCENDING; PROPERTY_DESCENDING


## Order Property Name
>	**Input Required**: False

>	**Description**: The property to use for sorting if the sort_order_property is PROPERTY_ASCENDING or PROPERTY_DESCENDING


## Page Size
>	**Input Required**: False

>	**Description**: The number of elements returned per page.


## Start From
>	**Input Required**: False

>	**Description**: When paging through results, the starting point of the results to return.

