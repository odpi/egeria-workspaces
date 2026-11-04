"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Type Explorer: relationship and classification types show their inheritance
chain (navigable) and inherited properties with a Show inherited toggle, like
entity types. Uses Egeria's built-in DataFlow (DataLineageRelationship ->
LineageRelationship -> LabeledRelationship) and EditingCollection
(CollectionKind) types.
"""

import re

from playwright.sync_api import Page, expect

_RELS_LOADED = re.compile(r"RELATIONSHIPS \([1-9]\d*\)")


def _open(page: Page, name: str) -> None:
    search = page.locator(".search-input")
    search.fill(name)
    page.locator(".sidebar .type-name", has_text=re.compile(f"^{name}$")).first.click()
    search.fill("")


def test_relationship_inheritance_chain_and_inherited_properties(page: Page):
    page.goto("/egeria-explorer#type-system")
    page.locator(".section-hdr", has_text=_RELS_LOADED).wait_for(timeout=60_000)
    _open(page, "DataFlow")
    detail = page.locator(".detail").first

    expect(detail.locator(".chain")).to_contain_text("LabeledRelationship")
    expect(detail.locator(".chain")).to_contain_text("DataLineageRelationship")
    rows = detail.locator("table tbody tr")
    all_count = rows.count()
    # Inherited properties are listed with the type that defines them.
    expect(detail.locator("table tbody")).to_contain_text("LineageRelationship")

    detail.locator("input[type=checkbox]").first.uncheck()
    assert rows.count() < all_count

    # The chain navigates to the supertype, which lists DataFlow's parent as a subtype.
    detail.locator(".chain button", has_text=re.compile("^LineageRelationship$")).click()
    expect(page.locator(".detail .detail-name").first).to_have_text("LineageRelationship")
    expect(page.locator(".detail .subs")).to_contain_text("DataLineageRelationship")


def test_classification_inheritance_chain(page: Page):
    page.goto("/egeria-explorer#type-system")
    page.locator(".section-hdr", has_text=_RELS_LOADED).wait_for(timeout=60_000)
    _open(page, "EditingCollection")
    detail = page.locator(".detail").first

    expect(detail.locator(".chain")).to_contain_text("CollectionKind")
    detail.locator(".chain button", has_text="CollectionKind").click()
    expect(page.locator(".detail .detail-name").first).to_have_text("CollectionKind")
    expect(page.locator(".detail .subs")).to_contain_text("EditingCollection")
