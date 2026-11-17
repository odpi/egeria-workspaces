# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Browse "Badge" is shown as "Classification" (Dan, 2026-11-17), while the id stays `badge`
so older ?browse=badge links and favourites keep working (Architect read-back R7).
The hover text names the classifications it covers, so the label does not claim every
classification. Endpoints run through the real app with a fake Egeria client."""
import re
from pathlib import Path

import pytest

import resource_browser_handler as rb

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text(encoding="utf-8")


def test_the_facet_is_labelled_classification_and_keeps_its_id():
    facets = _PAGE[_PAGE.index("var FACETS = ["):_PAGE.index("];", _PAGE.index("var FACETS = ["))]
    assert re.search(r"\{ id: 'badge', label: 'Classification', term: 'badge'", facets)
    assert "'Badge'" not in _PAGE


def test_the_definition_names_the_classifications_it_covers():
    m = re.search(r"badge: \{ label: 'Classification', def: '([^']+)'", _PAGE)
    assert m, "TERMS.badge"
    for name in rb._BADGES:
        label = "Security tags" if name == "SecurityTags" else name
        assert label in m.group(1), label


def test_search_filter_says_classification():
    assert "'any classification'" in _PAGE and "'no classifications here'" in _PAGE
    assert "any badge" not in _PAGE


class _Explorer:
    async def _async_get_elements_by_classification(self, name, start_from=0, **kw):
        if start_from or name != "Criticality":
            return []
        return [{"elementHeader": {"guid": "t1", "type": {"typeName": "RelationalTable", "superTypeNames": ["DataAsset"]},
                                   "versions": {}, "criticality": {"class": "ElementClassification", "classificationName": "Criticality"}},
                 "properties": {"displayName": "orders", "qualifiedName": "qn::orders"}}]


@pytest.fixture
def fake(monkeypatch):
    async def explorer():
        return _Explorer()

    async def cached(name, producer, ttl=600):
        return await producer(), rb.datetime.now(rb.timezone.utc)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_cached", cached)


def test_old_browse_badge_links_still_answer(client, fake):
    vals = client.get("/api/resource-browser/browse/badge").json()
    assert [v["id"] for v in vals["values"]] == rb._BADGES
    assert {v["id"]: v["count"] for v in vals["values"]}["Criticality"] == 1
    lst = client.get("/api/resource-browser/browse/badge/Criticality").json()
    assert [r["guid"] for r in lst["items"]] == ["t1"]


def test_an_unknown_classification_is_404_with_the_new_wording(client, fake):
    r = client.get("/api/resource-browser/browse/badge/Ownership")
    assert r.status_code == 404 and "not a classification this app lists" in r.json()["detail"]
