"""Collections view: the type-grouped list. Server flags (all_collections, hasParent, capped...) and the
pure JS grouping function (run under node when available; skipped otherwise)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import collections_handler as ch  # noqa: E402


def _el(guid, type_name, name):
    return {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": ["Collection"]}},
            "properties": {"displayName": name, "qualifiedName": "qn::" + name}}


class _Mgr:
    def __init__(self, pages, fail_at=None):
        self.pages, self.fail_at, self.calls = pages, fail_at, 0

    def find_collections(self, **kw):
        i = kw["start_from"] // kw["page_size"]
        if self.fail_at is not None and i == self.fail_at:
            raise RuntimeError("page failed")
        return self.pages[i] if i < len(self.pages) else []


class _Expert:
    """Serves `rels` honouring start_from/page_size, and refuses page_size > 1000 as Egeria now does."""
    def __init__(self, rels=None, fail=False, ignore_paging=False):
        self.rels, self.fail, self.ignore_paging, self.sizes = rels or [], fail, ignore_paging, []
    def find_relationships_between_elements(self, body, start_from=0, page_size=2000):
        self.sizes.append(page_size)
        if self.fail or page_size > 1000: raise RuntimeError("OMAG-COMMON-400-010 pageSize > 1000")
        if self.ignore_paging: return {"relationships": self.rels}
        return {"relationships": self.rels[start_from:start_from + page_size]}


@pytest.fixture
def client(monkeypatch):
    ch._ROOTS_CACHE.clear()
    app = FastAPI(); app.include_router(ch.router)
    def setup(pages, rels=None, fail_rels=False, fail_at=None):
        monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: _Mgr(pages, fail_at))
        monkeypatch.setattr(ch, "_get_expert", lambda *a, **k: _Expert(rels, fail_rels))
        return TestClient(app)
    return setup


PAGES = [[_el("a", "Folder", "Alpha"), _el("b", "DigitalProduct", "Beta"), _el("c", "Folder", "Gamma")]]
RELS = [{"elementGUIDAtEnd2": "c"}]


def test_all_collections_returns_every_type_and_skips_the_parent_read(client, monkeypatch):
    ex = _Expert(RELS)
    c = client(PAGES, RELS)
    monkeypatch.setattr(ch, "_get_expert", lambda *a, **k: ex)
    d = c.get("/api/collections/roots", params={"all_collections": "true"}).json()
    assert {r["guid"] for r in d["roots"]} == {"a", "b", "c"}                  # c is a member of something, still listed
    assert {r["typeName"] for r in d["roots"]} == {"Folder", "DigitalProduct"}
    assert ex.sizes == [] and "hasParent" not in d["roots"][0]                 # no relationship read at all
    assert (d["capped"], d["complete"]) == (False, True)


def test_parentless_opt_in_uses_a_valid_page_size_and_says_it_is_partial(client, monkeypatch):
    ex = _Expert(RELS)
    c = client(PAGES, RELS)
    monkeypatch.setattr(ch, "_get_expert", lambda *a, **k: ex)
    d = c.get("/api/collections/roots", params={"parentless": "true"}).json()
    assert ex.sizes == [1000]                                                  # Egeria refuses pageSize > 1000
    assert {r["guid"] for r in d["roots"]} == {"a", "b"} and d["parentsKnown"] is False


def test_default_call_is_the_cheap_all_collections_answer(client, monkeypatch):
    ex = _Expert(RELS)
    c = client(PAGES, RELS)
    monkeypatch.setattr(ch, "_get_expert", lambda *a, **k: ex)
    d = c.get("/api/collections/roots").json()
    assert ex.sizes == [] and {r["guid"] for r in d["roots"]} == {"a", "b", "c"}     # no ~10 s parent read, nobody waits for it


def test_all_collections_rows_are_summaries_with_a_short_description(client):
    long = "x" * 5000
    pages = [[dict(_el("a", "Folder", "Alpha"), properties={"displayName": "Alpha", "qualifiedName": "qn::Alpha",
                                                            "description": long, "mermaidGraph": "y" * 9000})]]
    row = client(pages).get("/api/collections/roots", params={"all_collections": "true"}).json()["roots"][0]
    assert set(row) == {"guid", "typeName", "superTypeNames", "displayName", "qualifiedName", "description"}
    assert len(row["description"]) <= 201 and row["description"].endswith("…")


def test_a_failed_page_marks_the_list_incomplete(client):
    d = client([PAGES[0]], RELS, fail_at=1).get("/api/collections/roots", params={"all_collections": "true"}).json()
    assert d["complete"] is False and d["total"] == 3
    assert ch._ROOTS_CACHE == {}


def test_hitting_the_page_cap_says_capped(client, monkeypatch):
    # every page non-empty for all max_pages pages: more may exist
    full = [[_el(f"g{i}", "Collection", f"n{i}")] for i in range(50)]
    d = client(full, RELS).get("/api/collections/roots", params={"all_collections": "true"}).json()
    assert d["capped"] is True and d["total"] == 50
