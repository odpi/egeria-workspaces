"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Relationship purpose in the Type Explorer (design-docs/relationship-purpose-plan.md,
Phase 2): the entity Relationships tab groups relationship types into purpose
families, the purpose filter narrows them, and a server that reports no
purposes gets the flat layout plus a one-line hint instead of empty families.

Uses Egeria's built-in `Asset` type, which carries relationships of every
purpose family on any current server.
"""

import json
import re

from playwright.sync_api import Page, expect

_NO_PURPOSE_HINT = "This Egeria server doesn't report relationship purposes"


def _open_asset_relationships(page: Page) -> None:
    page.goto("/egeria-explorer#type-system")
    # Wait for the type system to load (the sidebar's RELATIONSHIPS header
    # shows (0) until /api/types has returned).
    page.locator(".section-hdr", has_text=re.compile(r"RELATIONSHIPS \([1-9]\d*\)")).wait_for(timeout=60_000)
    search = page.locator(".search-input")
    search.fill("Asset")
    page.locator(".sidebar .type-name", has_text=re.compile(r"^Asset$")).click()
    search.fill("")
    page.locator(".detail button", has_text=re.compile(r"^Relationships \(\d+\)$")).click()


def test_relationships_tab_groups_by_purpose_family(page: Page):
    _open_asset_relationships(page)
    detail = page.locator(".detail").first

    # Grouped by default: Composition comes first and holds AssetConnection
    # (STRUCTURAL) with its precise purpose badge.
    expect(detail.get_by_text("Composition", exact=True)).to_be_visible()
    expect(detail.get_by_text("Governance & Description", exact=True)).to_be_visible()
    card = detail.locator(".rel-card", has=page.get_by_role("button", name="AssetConnection", exact=True))
    expect(card.get_by_text("Structural", exact=True)).to_be_visible()

    # The purpose filter narrows the list to one purpose, and so to one family.
    detail.locator("button[aria-pressed]", has_text=re.compile(r"^Structural \d+$")).click()
    expect(detail.get_by_text("Governance & Description", exact=True)).to_have_count(0)
    expect(card).to_be_visible()
    detail.get_by_role("button", name="Clear", exact=True).click()
    expect(detail.get_by_text("Governance & Description", exact=True)).to_be_visible()

    # Group: None restores the flat A–Z list.
    detail.locator("label", has_text="Group").locator("select").select_option("none")
    expect(detail.get_by_text("Composition", exact=True)).to_have_count(0)
    expect(card).to_be_visible()


def test_server_without_purposes_shows_flat_list_and_hint(page: Page):
    """Simulate an older Egeria server by stripping relationshipPurpose."""
    def strip_purposes(route):
        response = route.fetch()
        body = response.json()
        for rel in body.get("relationships", {}).values():
            rel.pop("relationshipPurpose", None)
        route.fulfill(response=response, body=json.dumps(body))

    page.route(re.compile(r".*/api/types(\?.*)?$"), strip_purposes)
    _open_asset_relationships(page)
    detail = page.locator(".detail").first

    expect(detail.get_by_text(_NO_PURPOSE_HINT)).to_be_visible()
    expect(detail.get_by_text("Composition", exact=True)).to_have_count(0)
    expect(detail.get_by_text("Unclassified", exact=True)).to_have_count(0)
    expect(detail.locator("button[aria-pressed]")).to_have_count(0)
