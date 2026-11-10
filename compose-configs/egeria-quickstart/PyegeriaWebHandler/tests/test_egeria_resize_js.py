"""static/egeria-resize.js (user-resizable column/pane widths), run under node.

The module is driven through a small fake DOM (tests/egeria_resize_harness.js)
that models fixed table layout and capture/bubble event dispatch. Standalone:
needs no app imports. Skipped when node is not installed (the container has none).

Owner report 2026-11-10: "sometimes the column resizing in the Portal doesn't
work - usually not on the first screen that you try to change but subsequent".
Found live on Operations: its tables have their own resize handles (React
state + <colgroup>); this module took the mousedown first and stopped it, then
wrote <th> widths that the <col> widths overrode — so whether a drag worked
depended on which few pixels of the edge were grabbed.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent / "static" / "egeria-resize.js"
HARNESS = HERE / "egeria_resize_harness.js"


def run(scenario):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    out = subprocess.run([node, str(HARNESS), str(MODULE), scenario], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    res = json.loads(out.stdout.strip().splitlines()[-1])
    assert res.pop("ok"), res.get("error")
    return res


def test_plain_drag_widens_the_column_and_saves_it():
    r = run("plain_drag")
    assert r["widths"] == [160, 100, 100]
    assert r["marked"] and r["tableWidth"] == "360px"
    assert json.loads(r["saved"]) == [160, 100, 100]


def test_drag_survives_header_handlers_that_stop_propagation():
    # th bubble handler + React-style root capture handlers all stop the event
    r = run("stop_propagation")
    assert r["widths"] == [160, 100, 100]
    assert r["pageSawPlainClick"] == 1      # a click away from the edge still reaches the page


def test_drag_after_rerender_that_replaces_header_cells():
    r = run("rerender_new_cells")
    assert r["before"]["widths"] == [160, 100, 100]
    # the previous view's frozen widths are gone from the reused <table>
    assert r["afterRerender"] == {"widths": [100, 100, 100, 100], "marked": False, "tableWidth": ""}
    assert r["afterDrag"] == {"widths": [100, 150, 100, 100], "tableWidth": "450px"}
    # switching back restores the first view's saved widths
    assert r["back"] == {"widths": [160, 100, 100], "tableWidth": "360px"}


def test_rerender_that_reuses_header_cells_for_other_columns():
    r = run("rerender_reused_cells")
    assert r["after"] == {"widths": [100, 100, 100], "marked": False, "cellWidth0": ""}
    assert r["afterDrag"] == [100, 100, 130]


def test_sort_indicators_do_not_change_the_saved_key():
    assert run("sort_marks")["keys"] == ["egeria-resize:/test-page:table:Name|Type"]


def test_table_with_its_own_resize_handles_is_left_to_the_page():
    r = run("page_owned_handles")
    assert r["pageDowns"] == 1              # the page's handle got the mousedown
    assert r["moduleTookIt"] is False
    assert r["restored"] is False           # old saved widths are not re-applied over the page's
    assert r["marked"] is False
    assert r["widths"] == [150, 150, 150]   # only the page's own (fake, inert) resizer may change them


def test_colgroup_widths_follow_the_drag_and_reset():
    r = run("colgroup_no_handles")
    assert r["afterDrag"] == [210, 150, 150]
    assert r["resetHandled"] and r["marked"] is False
    assert r["afterReset"] == [150, 150, 150] and r["colWidths"] == ["150px"] * 3


def test_lost_mouseup_ends_the_drag():
    r = run("lost_mouseup")
    assert r["widths"] == [140, 100, 100]
    assert r["saved"]
