# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""A glossary term row opens in Egeria Explorer's glossary, not on the Resource page; every
other row (and a work-list member whose type is GlossaryTerm) is decided by isTerm.
Runs isTerm, termUrl and openElement from resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    line_end = _PAGE.index("\n", start)
    if _PAGE[line_end - 1] == "}":                  # a one-line function
        return _PAGE[start:line_end + 1]
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


_HARNESS = r"""
var EXPLORER_TERM = '/egeria-explorer?guid=';
var window = { location: { href: '' } };
var opened = [];
function openResource(g) { opened.push(g); }
__FNS__
openElement({ guid: 'r 1', kind: 'table' });
openElement({ guid: 't/1', kind: 'term' });
var termHref = window.location.href;
window.location.href = '';
openElement({ guid: 'm1', typeName: 'GlossaryTerm' });
console.log(JSON.stringify({ opened: opened, termHref: termHref, memberHref: window.location.href,
  notTerm: isTerm({ kind: 'attribute' }), nothing: isTerm(null) }));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_term_rows_open_in_egeria_explorer():
    js = _HARNESS.replace("__FNS__", "\n".join(_fn(n) for n in ("isTerm", "termUrl", "openElement")))
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["opened"] == ["r 1"]
    assert d["termHref"] == "/egeria-explorer?guid=t%2F1#glossary"
    assert d["memberHref"] == "/egeria-explorer?guid=m1#glossary"
    assert d["notTerm"] is False and d["nothing"] is False


def test_glossary_terms_have_an_icon_and_a_definition():
    assert "term: '📖'" in _PAGE
    assert "term: { label: 'Glossary term'" in _PAGE
