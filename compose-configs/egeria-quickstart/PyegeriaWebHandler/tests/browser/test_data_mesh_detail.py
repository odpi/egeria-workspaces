"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Data Mesh detail pane: a "View full details" link opens the selected digital
product in Egeria Explorer, and the pane's header-less property table
(label | value) has a resizable label column, remembered per page by
static/egeria-resize.js.
"""

from playwright.sync_api import Page, expect

_SELECT_BUSIEST_PRODUCT = """(() => {
  const el = [...document.querySelectorAll('div')].find(d => d._cyreg);
  const cy = el._cyreg.cy;
  const n = cy.nodes().sort((a, b) => b.degree() - a.degree())[0];
  n.emit('tap');
  return n.id();
})()"""


def _open_product(page: Page) -> str:
    page.goto("/data-mesh")
    page.locator(".mesh-panel").wait_for(timeout=90_000)
    guid = page.evaluate(_SELECT_BUSIEST_PRODUCT)
    page.locator(".mesh-panel table").first.wait_for(timeout=60_000)
    return guid


def test_view_full_details_links_to_explorer(page: Page):
    guid = _open_product(page)
    link = page.locator(".mesh-panel a", has_text="View full details")
    expect(link).to_have_attribute("href", f"/egeria-explorer?guid={guid}#digital-products")
    expect(link).to_have_attribute("target", "_blank")


def test_property_table_label_column_resizes_and_is_remembered(page: Page):
    page.set_viewport_size({"width": 1600, "height": 1000})
    page.goto("/data-mesh")
    page.evaluate("EgeriaResize.reset()")
    _open_product(page)

    label = page.locator(".mesh-panel table").first.locator("tr").nth(2).locator("td").first
    box = label.bounding_box()
    # Drag the boundary on a data row: header-less tables resize from any row.
    page.mouse.move(box["x"] + box["width"] - 1, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.move(box["x"] + box["width"] + 80, box["y"] + box["height"] / 2, steps=8)
    page.mouse.up()
    first_label = page.locator(".mesh-panel table").first.locator("tr").first.locator("td").first
    widened = first_label.bounding_box()["width"]
    assert widened >= box["width"] + 60

    page.reload()
    _open_product(page)
    page.wait_for_timeout(800)
    restored = page.locator(".mesh-panel table").first.locator("tr").first.locator("td").first.bounding_box()["width"]
    assert abs(restored - widened) <= 2
