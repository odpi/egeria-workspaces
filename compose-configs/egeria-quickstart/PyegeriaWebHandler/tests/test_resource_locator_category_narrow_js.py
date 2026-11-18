# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Narrow by category (Dan, 2026-11-17: the element's category property). The choices are the
loaded rows' categories, plus "(no category)" only when some row has none; with no category on
any row there is nothing to choose. Matching is exact. Runs categoryOptions and inCategory from
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
def test_category_choices_and_matching():
    js = ("var NO_CATEGORY = '(no category)';\n" + "\n".join(_fn(n) for n in ("uniqueValues", "categoryOptions", "inCategory")) + r"""
var rows = [{ guid: 'a', category: 'Customer Domain' }, { guid: 'b', category: 'clinical trials' }, { guid: 'c', category: '' },
            { guid: 'd', category: 'Customer Domain' }];
function pick(c) { return rows.filter(function(r) { return inCategory(r, c); }).map(function(r) { return r.guid; }); }
console.log(JSON.stringify({
  options: categoryOptions(rows),
  allNamed: categoryOptions(rows.filter(function(r) { return r.category; })),
  noneNamed: categoryOptions([{ category: '' }, {}]),
  any: pick(''), customer: pick('Customer Domain'), none: pick('(no category)'), caseExact: pick('Clinical Trials'),
}));""")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["options"] == ["clinical trials", "Customer Domain", "(no category)"]
    assert d["allNamed"] == ["clinical trials", "Customer Domain"]
    assert d["noneNamed"] == []
    assert d["any"] == ["a", "b", "c", "d"] and d["customer"] == ["a", "d"] and d["none"] == ["c"] and d["caseExact"] == []


def test_category_select_is_in_search_and_browse():
    assert _PAGE.count("el(CategorySelect,") == 2
    assert "category: { label: 'Category'" in _PAGE
