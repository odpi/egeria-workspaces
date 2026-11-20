"""PO-60: freshstart's GET /api/collections/by-type (the Add-to-Collection picker's second step) was
declared after GET /api/collections/{node_guid}, so "by-type" was taken as a guid; and that detail
route's non-collection fallback called digital_products_handler.get_node with 5 positional args
where it takes 4, so the request ended in a TypeError (500)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import collections_handler as ch  # noqa: E402
import digital_products_handler as dph  # noqa: E402


def _el(guid, type_name, name):
    return {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": ["Collection"]}},
            "properties": {"displayName": name, "qualifiedName": "qn::" + name}}


class _Mgr:
    def __init__(self, cols=None):
        self.cols, self.find_kwargs = cols or [], None

    def find_collections(self, **kw):
        self.find_kwargs = kw
        return self.cols

    def get_collection_by_guid(self, guid, **kw):
        return None                     # not a collection -> the digital-products fallback


@pytest.fixture
def app():
    a = FastAPI()
    a.include_router(ch.router)
    return a


def test_by_type_is_not_swallowed_by_the_node_route(app, monkeypatch):
    mgr = _Mgr([_el("f1", "Folder", "Alpha"), _el("f2", "Folder", "Beta")])
    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: mgr)
    r = TestClient(app).get("/api/collections/by-type", params={"type_name": "Folder"})
    assert r.status_code == 200, r.text
    assert [c["guid"] for c in r.json()] == ["f1", "f2"]
    assert mgr.find_kwargs["metadata_element_type_name"] == "Folder"


def test_node_fallback_calls_digital_products_get_node_with_its_signature(app, monkeypatch):
    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: _Mgr())
    seen = {}

    def fake_dp_get_node(node_guid, url=None, server=None, user_id=None):  # dph.get_node's signature
        seen["guid"] = node_guid
        return JSONResponse({"guid": node_guid, "typeName": "TabularDataSet"})

    monkeypatch.setattr(dph, "get_node", fake_dp_get_node)
    r = TestClient(app).get("/api/collections/asset-1")
    assert r.status_code == 200, r.text
    assert seen["guid"] == "asset-1"
