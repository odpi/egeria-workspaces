# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Locator's home page is "Resource Locator Home", not "Home" (Dan, 2026-11-17, PO-39: the
Portal has many homes). Covers the Locator's own nav tab and crumbs; the Portal app bar is not
the Locator's, so it is not touched here."""
import re
from pathlib import Path

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text(encoding="utf-8")


def test_the_label_is_defined_once_and_used_for_the_tab_and_crumbs():
    assert "var HOME_LABEL = 'Resource Locator Home';" in _PAGE
    assert "tab('home', HOME_LABEL, {})" in _PAGE
    assert _PAGE.count("navigate({}); } }, '← ' + HOME_LABEL)") == 1
    assert _PAGE.count("navigate({}); } }, HOME_LABEL), '›'") == 1


def test_no_bare_home_label_is_left_in_the_locator():
    app = _PAGE[_PAGE.index("var HOME_LABEL"):]
    assert not re.search(r"""[(,]\s*'(← )?Home'\s*[),]""", app)
