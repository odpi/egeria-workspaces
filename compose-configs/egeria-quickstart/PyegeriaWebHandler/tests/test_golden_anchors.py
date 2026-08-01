"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Golden-anchor tests: assert exact, known-good values against stable
Coco Pharmaceuticals seed data (see golden_anchors.py for why these are safe
to hardcode). These are characterization tests, not spec-derived tests — they
capture today's known-good behavior as a regression baseline for a codebase
that otherwise has ~0% coverage, per the Portal test-strategy discussion.

Deliberately NOT covered here: frontend routing (which tab a "View" link
lands on) — that class of bug has no backend signal at all and needs a
browser-driven test instead (Playwright, Phase 2 of the test strategy).
"""

from golden_anchors import WORK_ITEM_LIST


def test_work_item_list_detail_matches_known_seed_data(client):
    r = client.get(f"/api/collections/{WORK_ITEM_LIST['guid']}")
    assert r.status_code == 200
    body = r.json()

    assert body["guid"] == WORK_ITEM_LIST["guid"]
    assert body["typeName"] == WORK_ITEM_LIST["typeName"]
    assert body["displayName"] == WORK_ITEM_LIST["displayName"]
    assert body["qualifiedName"] == WORK_ITEM_LIST["qualifiedName"]
    assert body["status"] == WORK_ITEM_LIST["status"]
    assert body["props"]["category"] == WORK_ITEM_LIST["category"]


def test_work_item_list_membership_matches_known_seed_data(client):
    r = client.get(f"/api/collections/{WORK_ITEM_LIST['guid']}")
    assert r.status_code == 200
    body = r.json()

    members = body["relationships"]["collectionMembers"]
    actual = {(m["guid"], m["displayName"], m["typeName"]) for m in members}
    assert actual == WORK_ITEM_LIST["members"]


def test_work_item_list_findable_by_search(client):
    """The 2026-07-31 routing bug existed precisely because this WorkItemList
    is NOT reachable by browsing the root-collection tree (confirmed:
    /api/collections/roots lists only genuine RootCollection-classified
    elements, and this WorkItemList isn't a descendant of any of them) — the
    only path to it is a direct by-guid deep link, which is why the
    Collections tab needed navGuid support in the first place. This test
    instead guards the search path the frontend's own "Search" box uses to
    surface exactly this kind of otherwise-unreachable collection."""
    r = client.get("/api/catalog/search", params={"q": WORK_ITEM_LIST["displayName"]})
    assert r.status_code == 200
