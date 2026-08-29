# Keeping Safe

The scenarios in this directory focus on security and the IT infrastructure that underpins it:

- [Creating the systems inventory](creating-system-inventory/creating-system-inventory.ipynb) builds the initial record of what runs in the business.  [Gary Geeke](https://egeria-project.org/practices/coco-pharmaceuticals/personas/gary-geeke/) built this first, ahead of his own governance program, because the security team needed it urgently to scope the ISMS.
- [Extending the systems inventory](extending-the-systems-inventory/README.md) captures the further systems information used to drive security initiatives.
- [it-governance-program.md](it-governance-program.md) is Gary's governance program for the `IT Infrastructure` domain, built on that inventory and structured around the ITIL practices his team already works to.  IT infrastructure is a *serving* domain: it owns no regulatory obligation of its own, and almost all of its governance is expressed as commitments to obligations belonging to security, manufacturing, privacy, drug development and corporate governance.
- [Understanding Martyn's Law](martyns-law/README.md) looks at managing a physical security situation.

## Loading the IT governance program

The definitions carry Domain Identifier `IT Infrastructure` and link to definitions across the domain programs, so load the whole of `0. data-governance-program` first, then the systems inventory notebooks, then this file.

1. From Obsidian - open the `it-governance-program.md` file and click the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process --userid garygeeke --user_pass secret it-governance-program.md
    ```

The Martyn's Law definitions load after this file.


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.