# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Browse by category (Dan, 2026-11-17: the element's category property; design
note DESIGN-RL-BROWSE-CLASSIFICATION-TERM-CATEGORY-FOLDER-KEYWORD, Architect read-back R1, R2, R6).

Pinned here:
  - values come from the background sweep (no Egeria call lists distinct categories), counted as
    resources plus glossary terms, with "(no category)" last; "counting" while the sweep runs, never 0;
  - a list is the same sweep rows, so it always agrees with its count;
  - R1: a glossary term is never in the Data scope lists (recorded / none / not read);
  - R2: a failed GlossaryTerm read keeps the resource rows and says terms were not read;
  - R6: counts are "at least" when a resource type, or the term read, was capped.
Endpoints run through the real app with fake Egeria clients; nothing is written."""
import asyncio
from datetime import datetime, timezone

import pytest

import resource_browser_handler as rb


def _el(guid, type_name, supers, name, category=None, scope=None):
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers}, "versions": {},
           "anchor": {"class": "ElementClassification", "classificationName": "Anchors", "classificationProperties": {}}}
    if scope:
        hdr["dataScope"] = {"class": "ElementClassification", "classificationName": "DataScope",
                            "classificationProperties": scope}
    props = {"displayName": name, "qualifiedName": f"qn::{name}"}
    if category is not None:
        props["category"] = category
    return {"elementHeader": hdr, "properties": props}


_ASSET = ["DataSet", "DataAsset", "Asset", "Referenceable"]
_DB = _el("db", "RelationalDatabase", _ASSET, "customers db", category="Customer Domain")
_CSV = _el("csv", "CSVFile", _ASSET, "trial.csv", category="Clinical Trials")
_BARE = _el("bare", "DataSet", _ASSET, "bare set")
_TERM = _el("t1", "GlossaryTerm", ["Referenceable"], "Customer", category="Customer Domain")
_TERM2 = _el("t2", "GlossaryTerm", ["Referenceable"], "Visit")


def _sweep(rows, terms=(), capped_types=(), terms_capped=False, terms_error=None):
    return {"rows": rb._rows(rows)[0], "cappedTypes": list(capped_types),
            "terms": [rb._term_row(t) for t in terms], "termsCapped": terms_capped, "termsError": terms_error}


@pytest.fixture
def state(monkeypatch):
    st = {"value": None, "loading": False, "error": None}

    def fake_state():
        return st["value"], datetime.now(timezone.utc), st["loading"], st["error"]

    async def explorer():           # the facet reads nothing else from Egeria
        return object()
    monkeypatch.setattr(rb, "_all_resources_state", fake_state)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    return st


def test_values_count_resources_and_terms_with_no_category_last(client, state):
    state["value"] = _sweep([_DB, _CSV, _BARE], [_TERM, _TERM2])
    d = client.get("/api/resource-browser/browse/category").json()
    assert [(v["id"], v["count"], v["description"]) for v in d["values"]] == [
        ("Clinical Trials", 1, "1 resource"), ("Customer Domain", 2, "1 resource, 1 glossary term"),
        ("(no category)", 2, "1 resource, 1 glossary term")]
    assert all(v["countAtLeast"] is False for v in d["values"]) and d["countsAre"] is None
    assert "you can see" in d["note"]


def test_while_counting_there_is_no_value_and_no_zero(client, state):
    state["loading"] = True
    d = client.get("/api/resource-browser/browse/category").json()
    assert d["values"] == [] and d["loading"] is True and "background" in d["note"]
    lst = client.get("/api/resource-browser/browse/category/Customer%20Domain").json()
    assert lst["items"] == [] and lst["loading"] is True


def test_the_list_agrees_with_its_count(client, state):
    state["value"] = _sweep([_DB, _CSV, _BARE], [_TERM, _TERM2])
    vals = {v["id"]: v["count"] for v in client.get("/api/resource-browser/browse/category").json()["values"]}
    for cat, n in vals.items():
        lst = client.get(f"/api/resource-browser/browse/category/{cat}").json()
        assert len(lst["items"]) == n, cat
    lst = client.get("/api/resource-browser/browse/category/Customer%20Domain").json()
    assert sorted(r["guid"] for r in lst["items"]) == ["db", "t1"]
    assert {r["guid"]: r["kind"] for r in lst["items"]}["t1"] == "term"


def test_a_category_nobody_has_says_so(client, state):
    state["value"] = _sweep([_DB])
    lst = client.get("/api/resource-browser/browse/category/Nope").json()
    assert lst["items"] == [] and "No resource or glossary term you can see" in lst["note"]


def test_r6_counts_are_at_least_when_a_read_was_capped(client, state):
    state["value"] = _sweep([_DB], [_TERM], terms_capped=True)
    d = client.get("/api/resource-browser/browse/category").json()
    assert all(v["countAtLeast"] for v in d["values"]) and "at least" in d["countsAre"]
    state["value"] = _sweep([_DB], [_TERM], capped_types=["DataAsset"])
    assert all(v["countAtLeast"] for v in client.get("/api/resource-browser/browse/category").json()["values"])


def test_r2_terms_not_read_are_named(client, state):
    state["value"] = _sweep([_DB], [], terms_error="timeout")
    d = client.get("/api/resource-browser/browse/category").json()
    assert [v["id"] for v in d["values"]] == ["Customer Domain"] and "could not be read" in d["note"]


def test_r1_a_term_is_in_no_data_scope_list():
    rec = {"rows": [], "usageOnly": 0, "capped": False}
    allr = _sweep([_BARE], [_TERM2])
    allr["rows"] = allr["rows"] + allr["terms"]          # even if a term reached the rows, it is not a resource
    recorded, none = rb._split_from(rec, datetime.now(timezone.utc), allr, datetime.now(timezone.utc))
    assert [r["guid"] for r in none["rows"]] == ["bare"]
    assert none["notRead"] == [] and recorded["rows"] == []


class _Explorer:
    async def _async_get_elements(self, type_name, start_from=0, **kw):
        if type_name == "GlossaryTerm":
            raise RuntimeError("term read timed out")
        return [] if start_from else ([_DB] if type_name == "DataAsset" else [])


def test_r2_a_failed_term_read_keeps_the_resource_rows(monkeypatch):
    async def explorer():
        return _Explorer()

    async def cached(name, producer, ttl=600):
        return [], datetime.now(timezone.utc)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_cached", cached)
    out = asyncio.run(rb._all_resources_sweep())
    assert [r["guid"] for r in out["rows"]] == ["db"]
    assert out["terms"] == [] and "timed out" in out["termsError"]
