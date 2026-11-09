"""The Collections view's pure grouping function (type-explorer.html), run under node.
Standalone: needs no app imports. Skipped when node is not installed (the container has none)."""
import json, re, shutil, subprocess
from pathlib import Path

import pytest

HTML = (Path(__file__).resolve().parent.parent / "type-explorer.html").read_text()


def _group(items, opts):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    m = re.search(r"function groupCollectionsByType\(items, opts\) \{.*?\n\}\n", HTML, re.S)
    assert m, "groupCollectionsByType not found in type-explorer.html"
    js = m.group(0) + f"console.log(JSON.stringify(groupCollectionsByType({json.dumps(items)}, {json.dumps(opts)})));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


ITEMS = [
    {"guid": "1", "typeName": "Folder", "displayName": "zeta", "hasParent": False},
    {"guid": "2", "typeName": "DigitalProduct", "displayName": "Beta", "hasParent": True},
    {"guid": "3", "typeName": "Folder", "displayName": "Alpha", "hasParent": False},
    {"guid": "4", "displayName": "NoType", "qualifiedName": "qn", "hasParent": None},
]


def test_groups_by_type_sorted_with_rows_sorted_by_name():
    g = _group(ITEMS, {})
    assert [x["typeName"] for x in g] == ["Collection", "DigitalProduct", "Folder"]    # untyped -> Collection
    assert [c["displayName"] for c in g[2]["items"]] == ["Alpha", "zeta"]


def test_type_filter_and_search():
    assert [x["typeName"] for x in _group(ITEMS, {"typeFilter": "Folder"})] == ["Folder"]
    assert [c["guid"] for x in _group(ITEMS, {"search": "ALP"}) for c in x["items"]] == ["3"]


def test_groups_start_collapsed_in_the_view():
    assert "useState(new Set());   // every group starts collapsed" in HTML
    assert "searching ? !closedInSearch.has(t) : openTypes.has(t)" in HTML    # only a search auto-opens, and a click can still close
    assert "const open = isTypeOpen(g.typeName);" in HTML                    # rows, arrow and aria-expanded share that one state
    assert "React.createElement(FoldTriangle, { open: open, size: 14 })" in HTML
