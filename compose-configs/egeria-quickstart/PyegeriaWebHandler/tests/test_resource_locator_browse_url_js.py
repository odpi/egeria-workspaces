# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""A Browse list is asked for with its value in the query, never the path: free-text values
(keywords, categories, owners) may hold a "/" that a path segment cannot carry past Apache
(Architect R1, 2026-11-17; laz has the keyword "App/AI Builder"). Runs browseListUrl from
resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_browse_list_url_keeps_the_value_out_of_the_path():
    js = "var API = '/api/resource-browser';\n" + _fn("browseListUrl") + r"""
console.log(JSON.stringify({ slash: browseListUrl('keyword', 'App/AI Builder'), lens: browseListUrl('category', 'R&D / Clinical', 'L 1') }));"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["slash"] == "/api/resource-browser/browse/keyword?value=App%2FAI%20Builder"
    assert d["lens"] == "/api/resource-browser/browse/category?value=R%26D%20%2F%20Clinical&lens=L%201"


def test_the_page_builds_every_list_url_with_browse_list_url():
    assert "'/browse/' + f.id + '/' + encodeURIComponent" not in _PAGE
    assert "getJson(browseListUrl(f.id, effective, lens), creds)" in _PAGE
