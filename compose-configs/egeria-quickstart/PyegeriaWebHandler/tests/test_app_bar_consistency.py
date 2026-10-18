# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Every portal page uses the one shared app bar (static/app-bar.js).

The "⌂ Portal" link used to be hand-rolled per page -- top-left on some, top-right on
others, hidden until a persona was chosen on a few, missing entirely on the rest. The
bar now lives in one place; these checks stop a page drifting back to its own copy.
Static only (no browser): reads the HTML that FastAPI / Apache serve.
"""
import re
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent            # .../egeria-quickstart/PyegeriaWebHandler
REPO = HERE.parent.parent.parent
HANDLER_DIRS = [HERE, REPO / "compose-configs" / "egeria-freshstart" / "PyegeriaWebHandler"]
DOCS_PAGES = [REPO / "portal-docs" / "index.html", REPO / "portal-docs" / "viewer.html"]

# Pre-login pages and generated reports: no app chrome by design.
EXEMPT = {
    "demo-login.html", "demo-register.html", "demo-reset-password.html", "demo-privacy.html",
    "type-coverage-gap-analysis.html",
}
# The Portal keeps its own header (it IS the portal) but must carry the shared theme toggle.
PORTAL = "demo-portal.html"

# Labels the old per-page portal links used (bare "Portal" is also React's own
# internal component name in the inlined bundle, so it can't be matched here).
OLD_PORTAL_LINKS = re.compile(r"(?:← Portal|Portal ↗|['\">]⌂ Portal['\"<])")


def _pages():
    for d in HANDLER_DIRS:
        for p in sorted(d.glob("*.html")):
            if p.name not in EXEMPT:
                yield p
    yield from DOCS_PAGES


PAGES = list(_pages())


def _id(p):
    return f"{p.parent.parent.name}/{p.name}" if p.parent.name == "PyegeriaWebHandler" else f"portal-docs/{p.name}"


@pytest.mark.parametrize("page", PAGES, ids=_id)
def test_loads_app_bar_in_head(page):
    html = page.read_text(encoding="utf-8")
    head = html.split("</head>", 1)[0]
    assert "/static/app-bar.js" in head, "load static/app-bar.js in <head> (it applies the saved theme before first paint)"


@pytest.mark.parametrize("page", PAGES, ids=_id)
def test_uses_shared_bar(page):
    html = page.read_text(encoding="utf-8")
    if page.name == PORTAL:
        assert 'class="eg-theme-btn"' in html, "the Portal needs the shared theme toggle"
        return
    assert 'class="eg-appbar' in html or "AppHeader," in html, "render the header with AppHeader / <header class=\"eg-appbar\">"


@pytest.mark.parametrize("page", PAGES, ids=_id)
def test_no_hand_rolled_portal_link(page):
    html = page.read_text(encoding="utf-8")
    hits = [m.group(0) for m in OLD_PORTAL_LINKS.finditer(html)]
    assert not hits, f"page draws its own Portal link {hits!r}; the app bar already provides it"


def test_app_bar_identical_in_both_environments():
    a, b = (d / "static" / "app-bar.js" for d in HANDLER_DIRS)
    assert a.read_text(encoding="utf-8") == b.read_text(encoding="utf-8")


def test_app_header_identical_in_both_shared_ui_copies():
    def block(d):
        src = (d / "static" / "egeria-shared-ui.js").read_text(encoding="utf-8")
        start = src.index("function appBarIdentity(")
        return src[start:src.index("\n}\n", src.index("function AppHeader(")) ]
    q, f = (block(d) for d in HANDLER_DIRS)
    assert q == f
