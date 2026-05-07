## Report
> Runs a named pyegeria report spec (FormatSet) via hey_egeria run_report. Returns formatted output from the Egeria repository — not an element creation command.

### Report Spec
>	**Input Required**: True

>	**Attribute Type**: Simple

>	**Description**: The name of the report spec (FormatSet) to run, e.g. 'Digital-Products', 'Collections', 'My-User-MD'. This is the primary identifier for the report — equivalent to --report in the CLI.

>	**Default Value**: Referenceable
Org-Chart

### #Search String
>	**Input Required**: False

>	**Attribute Type**: Simple

>	**Description**: An optional search string to filter results by.

>	**Default Value**: *

team-hr
### Output Format
>	**Input Required**: False

>	**Attribute Type**: Valid Value

>	**Description**: Optional specification of output format for the query.

>	**Valid Values**: LIST,FORM,REPORT,MERMAID,DICT,MD,TABLE,JSON

>	**Default Value**: JSON

MERMAID
