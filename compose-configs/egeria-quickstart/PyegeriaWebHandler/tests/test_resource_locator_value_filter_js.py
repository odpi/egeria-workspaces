# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Browse values pages with many values (folders, categories, tags) get a filter box (Dan,
2026-11-17: "might need a search box"). filterValues keeps the values whose label or description
holds every word typed, ignoring case; an empty box keeps them all. Runs filterValues from
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
def test_filter_values_by_every_word_ignoring_case():
    js = _fn("filterValues") + r"""
var vals = [{ id: 1, label: 'Patterns of Information Management', description: '64 glossary terms' },
            { id: 2, label: 'Reference Data', description: '111 resources' },
            { id: 3, label: 'Schema Maker', description: 'anchored to a Glossary' }, { id: 4, label: 'Bare' }];
function ids(q) { return filterValues(vals, q).map(function(v) { return v.id; }); }
console.log(JSON.stringify({ empty: ids(''), blank: ids('   '), one: ids('REFERENCE'), two: ids('glossary patterns'),
  desc: ids('resources'), none: ids('zzz') }));"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["empty"] == [1, 2, 3, 4] and d["blank"] == [1, 2, 3, 4]
    assert d["one"] == [2] and d["two"] == [1] and d["desc"] == [2] and d["none"] == []


def test_the_box_shows_only_on_long_values_pages():
    assert "var VALUE_FILTER_MIN = 12;" in _PAGE
    assert "vals.values.length > VALUE_FILTER_MIN && el('div'" in _PAGE
