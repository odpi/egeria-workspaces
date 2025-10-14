``` mermaid
---
title: SolutionBlueprint - Initial Data Prep Blueprint for ML-OPs [02258f7f-040a-467c-b1d3-911becd6f8cb]
---
flowchart TD
%%{init: {"flowchart": {"htmlLabels": false}} }%%

1@{ shape: rounded, label: "*Solution Blueprint*
**Initial Data Prep Blueprint for ML-OPs**"}
2@{ shape: rect, label: "*Solution Component*
**Docling-Component**"}
1==>|"Collection Membership"|2
3@{ shape: rect, label: "*Solution Component*
**Data-Prep-Kit-Component**"}
3==>|"Solution Composition"|2
4@{ shape: rect, label: "*Solution Component*
**Milvus-Component**"}
1==>|"Collection Membership"|4
5@{ shape: rect, label: "*Solution Component*
**KServe-Component**"}
1==>|"Collection Membership"|5
1==>|"Collection Membership"|3
style 1 color:#000000, fill:#e0ab18, stroke:#004563
style 2 color:#000000, fill:#dda0dd, stroke:#000000
style 3 color:#000000, fill:#dda0dd, stroke:#000000
style 4 color:#000000, fill:#dda0dd, stroke:#000000
style 5 color:#000000, fill:#dda0dd, stroke:#000000

click 1 href "https://egeria-project.org" "Egeria Link"

```