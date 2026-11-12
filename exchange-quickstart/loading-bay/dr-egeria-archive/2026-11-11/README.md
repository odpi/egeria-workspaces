<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Archived Dr.Egeria documents, 2026-11-11

**Never run these on a clean Egeria.**

- `FIXUP_2026_11_11_USEFUL_SHEETS_TEXT.dr-egeria.md`
- `FIXUP_2026_11_11_SAVED_QUERY_TILE_ROUTE_B.dr-egeria.md`

They patched data made by older versions of the Useful Dashboards seeds, on the quickstart Egeria
as it was on 2026-11-11. The current seeds in `dr-egeria-inbox/Useful Dashboards/` already contain
these corrections, so on a clean Egeria (after a reset) the batch alone gives the right result.
Running a FIXUP there would duplicate: `Add Text on Dashboard Sheet` adds the text again, and
`Add Member to Collection` does not de-duplicate.

They are kept here, outside `dr-egeria-inbox`, only as a record. Nothing discovers or runs this
folder: the bootstrap batches read `dr-egeria-inbox` (and the Portal's own extra roots) only.
