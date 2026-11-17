# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Resource Locator's documentation matches the page: every kind the search filters
on, every Browse facet, and the Data scope and Data lens sections are described, and the
in-page Help links to a document that exists.

Kinds come from the handler's _KINDS and _PART_KINDS (what /kinds serves); facets from
the page's FACETS. Skipped where the docs are not in the checkout (inside the container,
/app has no portal-docs sibling)."""
import ast
import re
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLER_DIR = _HERE.parent
_DOCS = _HERE.parents[3] / "portal-docs" if len(_HERE.parents) > 3 else _HERE / "missing"
_DOC = _DOCS / "tools" / "resource-locator.md"
_CATALOG_DOC = _DOCS / "tools" / "tech-catalog.md"


def _doc() -> str:
    if not _DOC.exists():
        pytest.skip("portal-docs not in this checkout")
    return _DOC.read_text(encoding="utf-8")


def _kind_labels() -> list:
    tree = ast.parse((_HANDLER_DIR / "resource_browser_handler.py").read_text(encoding="utf-8"))
    labels = []
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_KINDS", "_PART_KINDS"):
            labels += [t.elts[1].value for t in n.value.elts]
    return labels


def test_every_search_kind_is_documented():
    doc = _doc()
    labels = _kind_labels()
    assert "Columns and attributes" in labels and "Data fields" in labels
    for label in labels:
        assert f"**{label}" in doc or f"{label}**" in doc or label in doc, label


def test_every_browse_facet_is_documented():
    doc = _doc()
    page = (_HANDLER_DIR / "resource-browser.html").read_text(encoding="utf-8")
    facets = page[page.index("var FACETS = ["):page.index("];", page.index("var FACETS = ["))]
    for label in re.findall(r"label: '([^']+)'", facets):
        assert label in doc, label


def test_scope_lens_and_help_are_documented_and_linked():
    doc = _doc()
    for heading in ("## Data scope", "## Data lenses", "## Flavour"):
        assert heading in doc, heading
    assert "kind=table,schema" in doc and "empty page" in doc
    assert "## Data scope" in _CATALOG_DOC.read_text(encoding="utf-8")
    page = (_HANDLER_DIR / "resource-browser.html").read_text(encoding="utf-8")
    src = re.search(r"var DOCS_URL = '/docs/viewer\.html\?src=([^']+)'", page).group(1)
    assert (_DOCS / src).exists(), src
