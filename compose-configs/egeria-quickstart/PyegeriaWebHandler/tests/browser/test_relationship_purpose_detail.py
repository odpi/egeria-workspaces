"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Relationship purpose on element detail pages (design-docs/relationship-purpose-plan.md,
Phase 3): GenericRelationshipsSection groups a panel's relationship groups into
purpose families, all folded by default, with fold state remembered per family
across reloads; a server that reports no purposes keeps the flat layout plus a
one-line hint.

Uses the golden NEXT_13_PROJECT, whose only generic relationship group
("Member Of Collections", CollectionMembership) belongs to the Organization
family.
"""

import json
import re

from playwright.sync_api import Page, expect

from golden_anchors import NEXT_13_PROJECT, WORK_ITEM_LIST

_NO_PURPOSE_HINT = "This Egeria server doesn't report relationship purposes"


def _open_next13(page: Page) -> None:
    page.goto("/egeria-explorer")
    projects_card = page.get_by_text("Projects", exact=True).locator("..").locator("..")
    projects_card.get_by_role("button", name="Open →").click()
    page.get_by_text(NEXT_13_PROJECT["displayName"], exact=True).click()


def test_detail_families_folded_by_default_and_remembered(page: Page):
    page.goto("/egeria-explorer")
    page.evaluate("localStorage.removeItem('egeria-rel-purpose-open')")
    _open_next13(page)

    # The family header (not the rows' own "View →" buttons inside it).
    header = page.locator('[data-purpose-family="organization"] > [role=button]')
    expect(header).to_have_attribute("aria-expanded", "false")
    expect(page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True)).to_have_count(0)

    header.click()
    expect(page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True)).to_be_visible()

    # Fold state survives a reload.
    page.reload()
    _open_next13(page)
    expect(header).to_have_attribute("aria-expanded", "true")
    expect(page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True)).to_be_visible()


def test_detail_server_without_purposes_is_flat_with_hint(page: Page):
    """Simulate an older Egeria server: no relationship carries a purpose."""
    def strip(route):
        response = route.fetch()
        body = response.json()
        for rel in body.get("relationships", {}).values():
            rel.pop("relationshipPurpose", None)
        if "purposes" in body:
            body = {"purposes": {k: None for k in body["purposes"]}, "serverReportsPurpose": False}
        route.fulfill(response=response, body=json.dumps(body))

    page.route(re.compile(r".*/api/types(/relationship-purposes)?(\?.*)?$"), strip)
    _open_next13(page)

    expect(page.get_by_text(_NO_PURPOSE_HINT).first).to_be_visible()
    expect(page.locator("[data-purpose-family]")).to_have_count(0)
    expect(page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True)).to_be_visible()
