"""PO-59: freshstart's Perspectives routes. GET /api/perspectives (the list) used to carry the detail
route's body and fail with NameError `perspective_guid` (500), and GET /api/perspectives/{guid} did not
exist. Both are exercised here with stub pyegeria clients."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import perspectives_handler as ph  # noqa: E402


def _el(guid, type_name, name, template=False):
    el = {"elementHeader": {"guid": guid, "type": {"typeName": type_name}},
          "properties": {"displayName": name, "qualifiedName": "qn::" + name}}
    if template:
        el["elementHeader"]["template"] = {"classificationName": "Template"}
    return el


class _ActorMgr:
    def __init__(self, rows):
        self.rows, self.kwargs = rows, None

    def find_actor_profiles(self, **kw):
        self.kwargs = kw
        return self.rows


class _Explorer:
    def __init__(self, element):
        self.element, self.guid = element, None

    def get_element_by_guid(self, guid, **kw):
        self.guid = guid
        return self.element


@pytest.fixture
def app():
    a = FastAPI()
    a.include_router(ph.router)
    return a


def test_list_returns_perspectives_sorted_and_not_a_500(app, monkeypatch):
    mgr = _ActorMgr([_el("p2", "Perspective", "Zeta"), _el("p1", "Perspective", "alpha"),
                     _el("x", "ActorProfile", "Not a perspective")])
    monkeypatch.setattr(ph, "_get_actor_manager", lambda *a, **k: mgr)
    r = TestClient(app).get("/api/perspectives")
    assert r.status_code == 200, r.text
    d = r.json()
    assert [p["guid"] for p in d["perspectives"]] == ["p1", "p2"]
    assert d["total"] == 2
    assert mgr.kwargs["metadata_element_type"] == "Perspective"


def test_detail_route_exists_and_returns_the_perspective(app, monkeypatch):
    ce = _Explorer(_el("p1", "Perspective", "Alpha"))
    monkeypatch.setattr(ph, "_get_classification_explorer", lambda *a, **k: ce)
    r = TestClient(app).get("/api/perspectives/p1")
    assert r.status_code == 200, r.text
    assert r.json()["guid"] == "p1" and ce.guid == "p1"


def test_detail_route_404s_on_a_non_perspective(app, monkeypatch):
    monkeypatch.setattr(ph, "_get_classification_explorer",
                        lambda *a, **k: _Explorer(_el("t1", "GlossaryTerm", "Term")))
    assert TestClient(app).get("/api/perspectives/t1").status_code == 404
