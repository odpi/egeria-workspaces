<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Dr.Egeria Help Glossary (bootstrap batch)

`dr-egeria-help.dr-egeria.md` is a copy of the help document that pyegeria's generator writes
(`gen_dr_help`, `commands/tech/generate_dr_help.py`; it writes a new timestamped file,
`dr-egeria-help-<ISO8601>.md`). It creates the `dr-egeria` Glossary, one Collection Folder per
command family, and one Term per Dr.Egeria command, which the `dr_egeria_help` search tool reads.

- **Generated from:** pyegeria 6.2.39 (the quickstart Portal image), 2026-11-12, offline
  (`create_help_terms(None)`, no Egeria connection). 479 commands: 1 Create Glossary,
  20 Create Collection Folder, 458 Create Term.
- **Refresh it** whenever pyegeria's commands change: generate it again, copy the new file over
  `dr-egeria-help.dr-egeria.md`, and set the canary in `_batch.json` to the **last** Create Term's
  Display Name (the last command in pyegeria's command order). The dr-egeria-command-sync skill
  (Step 4) does both; `tests/test_bootstrap_heal_seeds.py` checks the canary.
- **Not idempotent.** Folders are linked to the glossary with `Parent ID`, and terms to folders with
  `Folders`. Re-running either on existing elements is not proven safe (`Parent ID` on an update can
  remove an unrelated membership), so the batch runs only when its canary is missing, which is the
  case after an Egeria reset. Never re-run it by hand on a populated Egeria.
- **Time:** about five minutes on the quickstart (2026-11-11), inside the 900-second heal limit.
