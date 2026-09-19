# Mapping the Systems

This folder follows [Erin Overview](https://egeria-project.org/practices/coco-pharmaceuticals/personas/erin-overview/) and [Peter Profile](https://egeria-project.org/practices/coco-pharmaceuticals/personas/peter-profile/) as they link the solution components of the [strategic information supply chains](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-information-supply-chains/overview/) to the systems that actually run them — and discover, in doing so, where the original Coco Pharmaceuticals operation cannot run them at all.

A solution component is a design element.  The `ImplementedBy` relationship is what connects it to a real `SoftwareServer`, and it is the link that lets activity, errors and volumetrics roll up from the systems into a supply chain somebody can be held accountable for.  There are three estates to map against: the parent company's own systems from [Gary Geeke's spreadsheet](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/) (present from startup, supplied by `CocoComboArchive.omarchive`), and the systems of the Austin and Bucharest acquisitions loaded by [extending-the-systems-inventory](../extending-the-systems-inventory/README.md).

## Contents

| File | What it is |
|---|---|
| [mapping-the-systems.ipynb](mapping-the-systems.ipynb) | Introduces the mapping, creates the `ImplementedBy` relationships with pyegeria, and produces the gap report |
| [supply-chain-lineage.ipynb](supply-chain-lineage.ipynb) | Attaches each supply chain to the `DataFlow` lineage between the systems - updating Gary's loaded interactions in place with `mergeUpdate`, cloning them where a hop carries several chains, creating new ones where nothing was loaded |
| [data/component-system-mapping.csv](data/component-system-mapping.csv) | The mapping: one row per candidate system per component, across all three estates, each with a confidence and a note |
| [data/solution-components.csv](data/solution-components.csv) | The seventy-one fine-grained components being mapped — group, type, scope, and the supply chains each belongs to |
| [data/supply-chain-lineage.csv](data/supply-chain-lineage.csv) | One row per supply chain per hop between two systems — 128 rows over 87 hops, 39 of which carry more than one chain.  Rows that correspond to a loaded interaction carry its `interaction_id` |
| [data/lineage-needs-decision.csv](data/lineage-needs-decision.csv) | The 20 wires whose two ends both map to several systems in an estate - placed only after someone who knows the factories picks the pair |
| `system-mapping-report.md`, `supply-chain-lineage-report.md` | Written by the notebooks when they run; not committed |

The mapping spreadsheet was derived from the analysis in [strategic-supply-chain-system-matches.md](../strategic-supply-chain-system-matches.md), which is where the reasoning behind each row lives.  The confidence column carries that reasoning forward:

| Confidence | Meaning | Linked by the notebook? |
|---|---|---|
| **Strong** | The system's description, or a loaded interaction between systems, names the function | Yes |
| **Probable** | The function plainly lives in this system, though nothing says so explicitly | Yes |
| **Possible** | The system could host it; the owner needs to confirm | Reported, not linked |

## What the notebook does

1. **Loads the two spreadsheets** and summarises what is in them.
2. **Resolves every qualified name to a GUID** and reports any that are missing — a missing component means `strategic-supply-chain-analysis.md` has not been loaded; a missing system means the inventory notebook has not been run.
3. **Creates the `ImplementedBy` relationships** for every Strong and Probable row, setting the relationship's `role` to the estate and its `description` to the confidence and note.  It checks what is already linked first, so it can be re-run safely after the spreadsheet changes.
4. **Produces the gap report**, which answers three questions in order: which components have no system anywhere; which are implemented only at the acquisitions and so lie outside the scope of the original Coco operation; and where the parent's coverage rests on a Possible that nobody has confirmed.  The same picture is then shown by business system group and by supply chain.

## Running it

Open [mapping-the-systems.ipynb](mapping-the-systems.ipynb) in JupyterLab and run the cells in order.  It needs, already in Egeria:

* the supply chains from `0. data-governance-program/strategic-information-supply-chains.md`
* the components from `../strategic-supply-chain-analysis.md`
* the acquisition systems from `../extending-the-systems-inventory/extending-the-systems-inventory.ipynb`

The mapping notebook runs as `peterprofile` and the lineage notebook as `garygeeke`, and the choice matters.  The parent company's systems carry zone memberships (`business-systems`, `manufacturing-systems`, `compliance-systems`, `depot-systems` - all part of the Infrastructure zone), and the access rules for those zones are defined in the user directory the platform is configured with, `compose-configs/egeria-quickstart/secrets/coco-user-directory.omsecrets`:

* The four systems zones grant `READ` to `infrastructureStaff`, `dataIntegrationStaff`, `devOpsStaff` and the automated `dataManagementProcess` and `omagServer` accounts, and every other operation (`DEFAULT`) to `infrastructureStaff` only.  The `sustainability` zone is readable by every `openMetadataMember`.
* Erin Overview and Jules Keeper are in none of those groups, so they see only the nine systems that are also in the `sustainability` zone.  Run as Erin, the mapping reports the other twenty as missing.
* Peter Profile is in `dataIntegrationStaff`, so he can read all twenty-nine, and he can create `ImplementedBy` links because those anchor on the solution component.
* A `DataFlow` anchors on the system at its end, so creating one needs `DEFAULT` access to that system's zone.  Peter is refused (`OPEN-METADATA-SECURITY-403-007`); Gary Geeke is in `infrastructureTeam` and `infrastructureLeader`, hence `infrastructureStaff`, and is allowed - which is also the right person in the story to attach the supply chains to his lineage.  The relationships it creates can be seen in [Egeria Explorer](https://egeria-project.org/user-interfaces/egeria-explorer/overview/) by opening any solution component under the **Solution Architect** card and looking at its implementations.

## The lineage notebook

With the components linked to systems, [supply-chain-lineage.ipynb](supply-chain-lineage.ipynb) attaches each supply chain to the `DataFlow` relationships between those systems.  It relies on two properties of Egeria's lineage types:

* **Merge update.**  The 120 interactions Gary loaded for Austin and Bucharest each carry a placeholder `iscQualifiedName`.  Where a strategic supply chain passes over one of them, the notebook writes the chain's qualified name onto the existing relationship with `mergeUpdate = true`, so the label, direction, integration style, protocol, frequency and data exchanged the site teams recorded are all kept.
* **Multi-links.**  Lineage relationship types allow several relationships of the same type between the same two elements.  Where a hop carries more than one supply chain, the first goes onto the existing relationship and each further chain becomes a new `DataFlow` cloned from it - every original property, plus the new `iscQualifiedName` and a label with the chain's id appended - so each chain has lineage of its own.

Where nothing was loaded for a hop, a `DataFlow` is created from the strategic wire.  The notebook is idempotent, never overwrites a supply chain name that is already set, and repairs relationships from an earlier run that are missing one.  It runs after `mapping-the-systems.ipynb`.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
