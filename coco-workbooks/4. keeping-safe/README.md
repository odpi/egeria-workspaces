# Keeping Safe

The scenarios in this directory focus on security and the IT infrastructure that underpins it.  They rest on the systems inventory that [Gary Geeke](https://egeria-project.org/practices/coco-pharmaceuticals/personas/gary-geeke/) built in [1. coco-data-hub](../1.%20coco-data-hub/README.md) — first from his own spreadsheet, to support the mapping of the strategic information supply chains to real systems, and then extended with the systems of the Austin and Bucharest acquisitions.  The security team took that inventory up to scope the ISMS.

- [it-governance-program.md](it-governance-program.md) is Gary's governance program for the `IT Infrastructure` domain, built on that inventory and structured around the ITIL practices his team already works to.  IT infrastructure is a *serving* domain: it owns no regulatory obligation of its own, and almost all of its governance is expressed as commitments to obligations belonging to security, manufacturing, privacy, drug development and corporate governance.
- [Understanding Martyn's Law](martyns-law/README.md) looks at managing a physical security situation.

## Loading the IT governance program

The definitions carry Domain Identifier `IT Infrastructure` and link to definitions across the domain programs, so load the whole of `0. data-governance-program` first, then the systems inventory notebooks in `1. coco-data-hub`, then this file.

1. From Obsidian - open the `it-governance-program.md` file and click the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process --userid garygeeke --user_pass secret it-governance-program.md
    ```

The Martyn's Law definitions load after this file.


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.