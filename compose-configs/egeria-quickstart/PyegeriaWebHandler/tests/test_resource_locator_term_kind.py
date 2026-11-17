# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Glossary terms as a Resource Locator kind (Dan, 2026-11-17; design note
DESIGN-RL-BROWSE-CLASSIFICATION-TERM-CATEGORY-FOLDER-KEYWORD, Architect Q1).

Pinned here:
  - the text search asks for GlossaryTerm only when Glossary terms is picked; All leaves terms
    out and counts matching ones apart (termsNotShown), never as operational records;
  - a term row has kind "term", its summary and content status, and names no glossary (the
    header does not say which glossary holds it, so none is guessed);
  - _any_rows (Browse lists that may hold more than resources) keeps resources, terms and parts,
    and counts everything else by type name.
Endpoints run through the real app with a fake Egeria client; nothing is written."""
import pytest

import resource_browser_handler as rb


def _el(guid, type_name, supers, name, **props):
    return {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers}, "versions": {}},
            "properties": {"displayName": name, "qualifiedName": f"qn::{name}", **props}}


_TERM = _el("t1", "GlossaryTerm", ["AuthoredReferenceable", "Referenceable"], "Customer",
            summary="Someone who buys", contentStatus="ACTIVE")
_TABLE = _el("r1", "RelationalTable", ["SchemaAttribute", "DataAsset"], "customers")


class _Explorer:
    def __init__(self):
        self.asked = []

    async def _async_find_elements_by_property_value(self, property_value, property_names, metadata_element_subtypes, **kw):
        self.asked.append(list(metadata_element_subtypes))
        if kw.get("start_from"):
            return []
        out = [_TABLE, _TERM]   # Egeria answers with whatever the asked-for types match; the term only when asked
        return [e for e in out if any(t in [e["elementHeader"]["type"]["typeName"]] + e["elementHeader"]["type"]["superTypeNames"]
                                      for t in metadata_element_subtypes)] or [_TERM]


@pytest.fixture
def fake(monkeypatch):
    ex = _Explorer()

    async def explorer():
        return ex

    async def nothing(*a, **kw):
        return []

    async def no_parts(*a, **kw):
        return {"rows": [], "rollups": [], "found": 0, "lookedUp": 0}
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    for name in ("_search_tags", "_search_keywords", "_search_owners", "_search_repos"):
        monkeypatch.setattr(rb, name, nothing)
    monkeypatch.setattr(rb, "_search_parts", no_parts)
    return ex


def test_kind_types_add_terms_only_when_picked():
    assert "GlossaryTerm" not in rb._kind_types(None)
    assert rb._kind_types(["term"]) == ["GlossaryTerm"]
    assert rb._kind_types(["table", "term"]) == ["RelationalTable", "VirtualRelationalTable", "GlossaryTerm"]
    assert "GlossaryTerm" in rb._kind_types(["other", "term"]) and "GlossaryTerm" not in rb._kind_types(["other"])
    assert rb._parse_kinds("table,term") == ["table", "term"]


def test_term_row_has_kind_summary_status_and_no_glossary():
    r = rb._term_row(_TERM)
    assert r["kind"] == "term" and r["summary"] == "Someone who buys" and r["contentStatus"] == "ACTIVE"
    assert "glossary" not in r
    assert rb._term_row(_TABLE) is None
    assert rb._row(_TERM) is None          # a term is not a resource


def test_search_for_terms_returns_term_rows(client, fake):
    d = client.get("/api/resource-browser/search?q=customer&kind=term").json()
    assert fake.asked[0] == ["GlossaryTerm"]
    assert [(r["guid"], r["kind"]) for r in d["items"]] == [("t1", "term")]
    assert d["termsNotShown"] == 0


def test_all_leaves_terms_out_and_counts_them_apart(client, fake):
    d = client.get("/api/resource-browser/search?q=customer").json()
    assert "GlossaryTerm" not in fake.asked[0]
    assert all(r["kind"] != "term" for r in d["items"])


def test_all_counts_a_term_that_came_back_anyway(client, fake, monkeypatch):
    async def text(_c, _q, _types, _page):
        return [_TABLE, _TERM]
    monkeypatch.setattr(rb, "_search_text", text)
    d = client.get("/api/resource-browser/search?q=customer").json()
    assert [r["guid"] for r in d["items"]] == ["r1"]
    assert d["termsNotShown"] == 1 and d["notShown"] == 0


def test_kinds_endpoint_lists_glossary_terms_apart(client):
    d = client.get("/api/resource-browser/kinds").json()
    assert d["others"] == [{"id": "term", "label": "Glossary terms", "types": ["GlossaryTerm"]}]
    assert "term" not in [k["id"] for k in d["kinds"]]


def test_any_rows_keeps_resources_terms_and_parts_and_names_the_rest():
    col = _el("c1", "RelationalColumn", ["SchemaAttribute", "SchemaElement", "Referenceable"], "id")
    gat = _el("g1", "GovernanceActionType", ["Referenceable"], "survey")
    rows, not_shown = rb._any_rows([_TABLE, _TERM, col, gat, gat, None])
    assert [(r["guid"], r["kind"]) for r in rows] == [("r1", "table"), ("t1", "term"), ("c1", "attribute")]
    assert rows[2]["partOf"] is None and rows[2]["partOfKnown"] is False
    assert not_shown == {"GovernanceActionType": 2}
