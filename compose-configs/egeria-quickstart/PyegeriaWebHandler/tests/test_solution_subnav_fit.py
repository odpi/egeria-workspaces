"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The Solution Architect sidebar's sub-tab bar (Blueprints, Components, Patterns, Roles, Boundaries) must stay readable at the default sidebar width (260px) and when the
user resizes the sidebar. It had flex:1 and padding '8px 0' with no gap, so at 260px the labels ran together ("BlueprintsComponentsPatternsRolesBoun") and the last tab was cut off.
Source test: the bar wraps, every tab has horizontal padding, does not shrink below its text, and the sidebar is still user-resizable.
"""
import re
from pathlib import Path

_HTML = (Path(__file__).resolve().parent.parent / "type-explorer.html").read_text()
LABELS = ["Blueprints", "Components", "Patterns", "Roles", "Boundaries"]


def _bar():
    a = _HTML.index('"data-test": "sa-subnav"')
    start = _HTML.rindex("React.createElement(", 0, a)
    end = _HTML.index("// Search bar (shared", a)
    return _HTML[start:end]


def _tab_styles(bar):
    out = {}
    for m in re.finditer(r'React\.createElement\("button", \{ onClick: function\(\) \{ setSubNav\(\'([a-z]+)\'\).*?style: \{(.*?)\} \}, "([A-Za-z]+)"\)', bar):
        out[m.group(3)] = m.group(2)
    return out


def test_the_bar_has_the_five_tabs_in_order():
    bar = _bar()
    assert list(_tab_styles(bar)) == LABELS


def test_the_bar_wraps_and_has_a_gap():
    head = _bar().split("\n", 1)[0]
    assert "flexWrap: 'wrap'" in head and re.search(r"gap: [1-9]", head)


def test_every_tab_has_horizontal_padding_and_never_shrinks_below_its_text():
    for label, style in _tab_styles(_bar()).items():
        m = re.search(r"padding: '(\d+)px (\d+)px'", style)
        assert m and int(m.group(2)) > 0, f"{label}: no horizontal padding"
        assert "whiteSpace: 'nowrap'" in style, f"{label}: may wrap its own text"
        assert "flex: '1 1 auto'" in style, f"{label}: must grow from its text width, not from zero"


def test_the_sidebar_is_still_user_resizable():
    assert "useResizable(260, null, null, 'SolutionArchitectView.sideW')" in _HTML
    a = _HTML.index("function SolutionArchitectView")
    assert "React.createElement(ResizeDivider, { onMouseDown: onDivDown })" in _HTML[a:a + 120000]
