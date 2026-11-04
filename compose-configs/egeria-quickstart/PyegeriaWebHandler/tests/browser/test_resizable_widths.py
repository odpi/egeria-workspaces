"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

User-resizable widths (owner rule: every column / pane width is user-changeable).
Covers the three mechanisms: the shared useResizable hook (sidebar, remembered,
no fixed 900px cap), static/egeria-resize.js table columns (drag a header
edge, remembered), and egeria-resize.js layout grids (draggable split that
still collapses at the page's responsive breakpoint).
"""

import re

from playwright.sync_api import Page

_RELS_LOADED = re.compile(r"RELATIONSHIPS \([1-9]\d*\)")


def _drag(page: Page, x: float, y: float, dx: float) -> None:
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + dx / 2, y, steps=5)
    page.mouse.move(x + dx, y, steps=5)
    page.mouse.up()
    page.wait_for_timeout(300)


def _open_type_explorer(page: Page) -> None:
    page.goto("/egeria-explorer#type-system")
    page.locator(".section-hdr", has_text=_RELS_LOADED).wait_for(timeout=60_000)


def test_sidebar_resizes_past_old_cap_and_is_remembered(page: Page):
    page.set_viewport_size({"width": 1700, "height": 1000})
    _open_type_explorer(page)
    page.evaluate("Object.keys(localStorage).filter(k => k.startsWith('egeria-pane-width:'))"
                  ".forEach(k => localStorage.removeItem(k))")
    page.reload()
    page.locator(".section-hdr", has_text=_RELS_LOADED).wait_for(timeout=60_000)

    divider = page.locator(".col-divider").first.bounding_box()
    _drag(page, divider["x"] + 2, divider["y"] + 300, 1000)
    dragged = page.locator(".sidebar").first.bounding_box()["width"]
    assert dragged > 900, f"sidebar stopped at {dragged}px (old fixed cap was 900px)"

    page.reload()
    page.locator(".section-hdr", has_text=_RELS_LOADED).wait_for(timeout=60_000)
    assert abs(page.locator(".sidebar").first.bounding_box()["width"] - dragged) <= 2


def test_table_column_drag_is_remembered(page: Page):
    page.set_viewport_size({"width": 1500, "height": 1000})
    _open_type_explorer(page)
    page.evaluate("EgeriaResize.reset()")
    page.reload()
    th = page.locator(".detail table th").first
    th.wait_for(timeout=60_000)

    box = th.bounding_box()
    _drag(page, box["x"] + box["width"] - 2, box["y"] + box["height"] / 2, 120)
    widened = page.locator(".detail table th").first.bounding_box()["width"]
    assert widened >= box["width"] + 100

    page.reload()
    page.locator(".detail table th").first.wait_for(timeout=60_000)
    page.wait_for_timeout(800)
    assert abs(page.locator(".detail table th").first.bounding_box()["width"] - widened) <= 2


def test_overview_grid_split_drags_and_still_collapses(page: Page):
    page.set_viewport_size({"width": 1500, "height": 1000})
    page.goto("/egeria-overview")
    page.evaluate("EgeriaResize.reset()")
    page.reload()
    page.locator(".g-2").first.wait_for(timeout=60_000)
    page.wait_for_timeout(1500)

    cols = "getComputedStyle(document.querySelector('.g-2')).gridTemplateColumns.split(' ').map(parseFloat)"
    before = page.evaluate(cols)
    left_right, right_left, y = page.evaluate(
        "(() => { const k = document.querySelector('.g-2').children;"
        " const a = k[0].getBoundingClientRect(), b = k[1].getBoundingClientRect();"
        " return [a.right, b.left, a.top + 40]; })()")
    _drag(page, (left_right + right_left) / 2, y, 200)
    after = page.evaluate(cols)
    assert after[0] > before[0] + 150

    # Below the page's 1100px breakpoint the grid still collapses to one column.
    page.set_viewport_size({"width": 1000, "height": 1000})
    page.wait_for_timeout(600)
    assert len(page.evaluate(cols)) == 1
