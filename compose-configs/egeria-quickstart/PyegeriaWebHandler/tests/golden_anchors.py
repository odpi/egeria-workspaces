"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Stable, known-good entities from the Coco Pharmaceuticals seed data
(`CocoComboArchive`, one of the 11 .omarchive files loaded into
`qs-metadata-store` whenever its Postgres schema is empty — see
`compose-configs/egeria-quickstart/servers/qs-metadata-store/config/
qs-metadata-store.config`). Archive-seeded GUIDs and qualifiedNames are fixed
by the archive itself, so these anchors are safe to assert on exactly as long
as nothing has rewritten the archive content packs.

If a content-pack update ever changes one of these entities, the fix is to
re-derive the anchor from the live `/api/...` response (see each anchor's
`# verified against: <endpoint>` comment) and update this file — NOT to loosen
the assertions in the tests that consume it.
"""

# verified against: GET /api/collections/0affb580-fa81-4d00-9438-b26faf11845d
WORK_ITEM_LIST = {
    "guid": "0affb580-fa81-4d00-9438-b26faf11845d",
    "typeName": "WorkItemList",
    "displayName": "Local Dashboards - Next Steps",
    "qualifiedName": "Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0",
    "category": "Roadmap",
    "status": "ACTIVE",
    # (guid, displayName, typeName) for every collectionMember — order not
    # asserted (Egeria doesn't guarantee member ordering), membership set is.
    "members": {
        ("d8a61d15-fb63-44d2-b6ed-91557036e066", "Add drill-click parity for Vega bar/line charts", "Project"),
        ("f83d77e8-7413-436c-a4f9-4a5142ea09e7", "Unblock find_method for Dashboard Sheet commands", "Project"),
        ("c816f0e6-6789-404f-9946-b40a1ab3bf61", "Build Egeria Advisor dashboard editor (NEXT-13)", "Project"),
        ("797b1d3c-67ff-4832-ad24-06432b24d564", "Render nested Dashboard Sheets inline", "Project"),
        ("9f13b7b1-bd27-4c22-81b3-47b8e3e372c3", "Wire funnelChart into AI & Context Intelligence tile", "Project"),
    },
}

# One of WORK_ITEM_LIST's members — used by tests/browser/ to reproduce the
# 2026-07-31 Collections-vs-Digital-Products routing bug end to end: open
# this project, click "View" on its WORK_ITEM_LIST membership, and confirm
# the destination is the Collections tab (not Digital Products).
# verified against: GET /api/projects (filtered)
NEXT_13_PROJECT = {
    "guid": "c816f0e6-6789-404f-9946-b40a1ab3bf61",
    "displayName": "Build Egeria Advisor dashboard editor (NEXT-13)",
    "qualifiedName": "Build Egeria Advisor dashboard editor (NEXT-13)::1.0",
}
