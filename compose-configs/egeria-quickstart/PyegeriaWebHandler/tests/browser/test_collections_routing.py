"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Golden-path regression test for the 2026-07-31 Collections-vs-Digital-Products
routing bug: in Egeria Explorer, selecting a Project and clicking "View" on a
Collection it's a member of used to land on the Digital Products tab (showing
the right content under the wrong tab) instead of Collections. Fixed by
adding navGuid/deep-link support to CollectionsView (see type-explorer.html)
— this test reproduces the exact manual repro used to verify that fix.

This is Tier C of the Portal test strategy (browser-driven, golden-path
regression) — not a smoke test. It exists because this bug class has NO
backend signal at all (tests/test_golden_anchors.py already covers that the
API layer returns the right data; this covers that the FRONTEND routes to
the right tab), so only a real browser test can catch it.
"""

from golden_anchors import NEXT_13_PROJECT, WORK_ITEM_LIST


def test_project_collection_membership_view_lands_on_collections_tab(page):
    page.goto("/egeria-explorer")

    # Reach the Projects section the same way a user would from the home
    # page (direct #projects deep-linking isn't supported by this section —
    # confirmed manually during the original bug investigation). Scope to
    # the "Projects" card specifically (two ancestors up from its title span
    # is the card div with exactly one "Open ->" button; going further up
    # picks up every other card's button too).
    projects_card = page.get_by_text("Projects", exact=True).locator("..").locator("..")
    projects_card.get_by_role("button", name="Open →").click()

    page.get_by_text(NEXT_13_PROJECT["displayName"], exact=True).click()

    page.get_by_text("MEMBER OF COLLECTIONS").wait_for()
    page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True).wait_for()

    # Click "View ->" on the WORK_ITEM_LIST membership row specifically —
    # two ancestors up from its display name is the row with exactly one
    # "View ->" button (going further up picks up unrelated page buttons
    # like Header/Copy JSON/Post).
    membership_row = page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True).locator("..").locator("..")
    membership_row.get_by_role("button", name="View →").click()

    # The bug: this used to navigate to section=digital-products. Assert the
    # header/nav shows Collections, not Digital Products.
    page.get_by_text("Collections", exact=True).first.wait_for()
    assert page.get_by_text("Digital Products", exact=True).count() == 0, (
        "Regression: navigated to Digital Products instead of Collections"
    )

    # And the correct node's detail is what actually rendered (not just the
    # right tab with the wrong/blank content).
    page.get_by_text(WORK_ITEM_LIST["displayName"], exact=True).wait_for()
    page.get_by_text(WORK_ITEM_LIST["qualifiedName"]).wait_for()
