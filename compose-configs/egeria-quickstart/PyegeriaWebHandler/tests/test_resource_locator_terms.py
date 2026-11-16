# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator hover help: every "?" the page shows names a term that is defined.

The definitions live in one TERMS table in resource-browser.html; the Help component,
the help: prop on cards and tiles, and the Browse facets all refer to it by id. A typo
in an id would render nothing (Help returns null) or throw (TERMS[x.term].def), so
this test reads the page and checks every reference resolves.
"""
import re
from pathlib import Path

_PAGE = Path(__file__).resolve().parent.parent / "resource-browser.html"


def _terms(src: str) -> dict:
    block = src[src.index("var TERMS = {"):src.index("};", src.index("var TERMS = {"))]
    return dict(re.findall(r"^\s*(\w+): \{ label: '([^']+)', def: '", block, re.M))


def test_terms_have_a_label_and_a_definition():
    src = _PAGE.read_text(encoding="utf-8")
    terms = _terms(src)
    assert {"flavour", "dataScope", "dataLens", "kind", "matched"} <= set(terms)
    block = src[src.index("var TERMS = {"):src.index("};", src.index("var TERMS = {"))]
    for term_id in terms:
        line = next(l for l in block.splitlines() if l.strip().startswith(term_id + ":"))
        assert len(re.search(r"def: '(.*)' \}", line).group(1)) > 20, term_id


def test_every_help_reference_is_defined():
    src = _PAGE.read_text(encoding="utf-8")
    terms = set(_terms(src))
    used = set(re.findall(r"el\(Help, \{ term: '(\w+)' \}\)", src))
    used |= set(re.findall(r"el\((?:Card|Tile), \{ help: '(\w+)'", src))
    facets = src[src.index("var FACETS = ["):src.index("];", src.index("var FACETS = ["))]
    facet_terms = set(re.findall(r"term: '(\w+)'", facets))
    assert len(facet_terms) == facets.count("{ id:"), "every Browse facet names its term"
    used |= facet_terms
    assert used, "the page shows some hover help"
    assert used - terms == set()


def test_flavour_is_explained_where_it_is_filtered_and_browsed():
    src = _PAGE.read_text(encoding="utf-8")
    assert "el(Help, { term: 'flavour' })" in src
    assert "{ id: 'flavour', label: 'Flavour', term: 'flavour'" in src
