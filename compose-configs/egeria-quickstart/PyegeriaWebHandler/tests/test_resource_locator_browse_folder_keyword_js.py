# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Browse "not shown" line: folder and keyword lists name what they read but do not list,
by type, most first; the older lists keep their sentence. Runs notShownLine from
resource-browser.html under node; skipped without node."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_not_shown_line_names_types_or_keeps_the_old_sentence():
    js = _fn("notShownLine") + r"""
console.log(JSON.stringify({
  typed: notShownLine({ notShown: 5, notShownTypes: { ConnectorType: 2, GovernanceActionType: 3 } }),
  old: notShownLine({ notShown: 1 }),
  none: notShownLine({ notShown: 0, notShownTypes: {} }),
}));"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["typed"].startswith("5 not shown: 3 GovernanceActionType, 2 ConnectorType.")
    assert "glossary terms" in d["typed"]
    assert d["old"] == "1 element is not shown because it is not a resource this app lists or is a template."
    assert d["none"] == ""


def test_folder_and_keyword_facets_are_on_the_page():
    facets = _PAGE[_PAGE.index("var FACETS = ["):_PAGE.index("];", _PAGE.index("var FACETS = ["))]
    ids = re.findall(r"id: '([a-z]+)'", facets)
    assert ids.index("folder") == ids.index("collection") + 1 and ids.index("keyword") == ids.index("folder") + 1
    assert "folder: { label: 'Folder'" in _PAGE
