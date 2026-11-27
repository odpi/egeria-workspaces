<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# 7. Layout semantics

Workbooks that show what the layout recognizer in [`layout-profiles/`](../../layout-profiles/README.md) can say about a folder tree, by names
(and a few named manifest fields) only.

- [05 Conformance and drift](05%20conformance-and-drift.ipynb): generate a synthetic BIDS-shaped tree, check it against the `bids-dataset`
  profile ("97% conformant; 12 findings"), inject deviations, survey again and report drift ("3 new since last survey"); then the real
  ds000117 file list, reported and not scored. Runs locally with Python and PyYAML only; the Resource Explorer, Portal and Egeria steps are
  marked "Phase 3 — not run".
- [04a Simulation-case layout](04a%20simulation-case-layout.ipynb): generate a synthetic CalculiX-shaped parametric FEA sweep, recognize it with
  `generic-relevance` alone ("497 assets") and with the `fea-sweep` profile ("1 sweep, 60 cases, 61% hidden output"), build a parameter table from
  the case names, check conformance against a declared grid, inject deviations, and report drift after cases are added. Runs locally with Python
  and PyYAML only; the Resource Explorer, Portal, Egeria and lineage steps are marked "Phase 3/4 — not run".
