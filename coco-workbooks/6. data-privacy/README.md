<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Data Privacy

The scenarios in this directory work through the data privacy problems that are hardest for Coco Pharmaceuticals — not the ones that are hardest in general, but the ones that arise specifically from being a pharmaceutical company moving into personalised medicine while operating as a US-listed parent with subsidiaries in the UK and the EU.

The privacy governance program in [`0. data-governance-program/privacy-governance-program.md`](../0.%20data-governance-program/privacy-governance-program.md) establishes the domain: lawful bases, data subject rights, retention, breach notification, and the controllership and transfer obligations that follow from the group structure. This directory is where the situations that program has to cope with are worked through in detail.

## The scenarios

**Personalised manufacturing batch data is personal data.** For an autologous therapy the batch is made for one named patient from their own cells, and the batch record follows the product through manufacture, testing and release. Everyone who touches that record is thereby in possession of health data about an identifiable person — production operators, quality control analysts, warehouse staff, contract manufacturers and couriers, none of whom has a clinical relationship with the patient. Worse, for a targeted therapy the product itself implies the diagnosis, so knowing which product a batch is discloses the condition without any clinical field being present.

This collides with a GMP requirement that cannot bend. A batch record must be complete and attributable for its full retention period, which means the identity embedded in it cannot be erased on request. The resolution worked through in the manufacturing program is pseudonymisation — manufacturing sees a reference sufficient to prevent mix-up, never a patient, with the mapping held clinically. The residual is stated honestly rather than hidden: the mapping cannot be erased either, because a recall or safety signal years later must reach the people who received the product.

**Cross-border data transfers.** Every routine flow from the UK and EU subsidiaries to the US parent is a restricted transfer requiring a lawful mechanism, and the mechanism differs by origin — UK-origin data needs different instruments from EEA-origin data, so one document cannot cover both. Clinical trials make this concrete: sites sit across the UK and EU, the sponsor entity determines who the controller is, monitors employed by one group entity access source records held under another's jurisdiction, and the data consolidates into a US-held database. A personalised therapy consignment crossing a border carries the same question in physical form.

**Intra-group sharing that feels internal and is not.** The subsidiaries are separate legal entities and separate controllers. Common ownership confers no exemption, so an EU subsidiary sending employee records to the US parent is making a disclosure to a third party in law. This is the case most often missed, precisely because the systems are shared and the movement feels like an internal transfer.

## Files in this directory

* [data-processing-purposes.md](data-processing-purposes.md) — every data processing purpose declared across the governance program, gathered with the links that connect each to the policy it implements and the folio that owns it. It is also where the discussion of what a purpose is, and why each team declares its own rather than having the privacy team declare it for them, is set out.
* [cross-border-data-transfers.md](cross-border-data-transfers.md) — the routine flows of personal data out of the UK and the EEA to the US parent, why almost all of them are restricted transfers, and what has to be in place for each to be lawful. Adds the flow inventory that the transfer safeguard obligation had always assumed, the procedure for authority access demands, and the transfer risk assessment approach.
* [personalised-batch-data.md](personalised-batch-data.md) — the first scenario worked through in full. It traces an autologous therapy from collection to administration and on into the decades of retention that follow, showing which definitions apply at each step, and adds the three privacy-side definitions the journey surfaces that no single domain had reason to write.

## Loading

Data processing purposes link to policies created across every domain program, so load the whole of `0. data-governance-program` first.

Load `data-processing-purposes.md` first, then the two scenario files, which reference purposes defined in it.

1. From Obsidian - open each file in turn and click the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the commands:

    ```
    dr_egeria --directive process --userid faithbroker --user_pass secret data-processing-purposes.md
    ```

    ```
    dr_egeria --directive process --userid faithbroker --user_pass secret cross-border-data-transfers.md
    ```

    ```
    dr_egeria --directive process --userid faithbroker --user_pass secret personalised-batch-data.md
    ```

Both files are loaded as Faith Broker, the Chief Privacy Officer. She assures the lawful basis for every purpose in the first file — though each purpose remains owned by the domain that declared it and a member of that domain's folio — and owns the privacy-side definitions added by the two scenario files.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
