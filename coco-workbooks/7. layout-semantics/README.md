<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# 7. Layout semantics

Workbooks that show what the layout recognizer in [`layout-profiles/`](../../layout-profiles/README.md) can say about a folder tree, by names
(and a few named manifest fields) only.

- [05 Conformance and drift](05%20conformance-and-drift.ipynb): generate a synthetic BIDS-shaped tree, check it against the `bids-dataset`
  profile ("97% conformant; 12 findings"), inject deviations, survey again and report drift ("3 new since last survey"); then the real
  ds000117 file list, reported and not scored. Runs locally with Python and PyYAML only; the Resource Explorer, Portal and Egeria steps are
  marked "Phase 3 — not run".
