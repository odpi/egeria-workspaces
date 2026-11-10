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
    full = [[_el(f"g{i}", "Collection", f"n{i}")] for i in range(10)]
    d = client(full, RELS).get("/api/collections/roots", params={"all_collections": "true"}).json()
    assert d["capped"] is True and d["total"] == 10


def test_pages_of_1000_and_only_an_empty_page_ends_the_read(client, monkeypatch):
    sizes = []
    class Mgr:
        def find_collections(self, **kw):
            sizes.append((kw["start_from"], kw["page_size"]))
            n = kw["start_from"] // 1000
            return [_el(f"g{n}-{i}", "Collection", f"n{n}-{i}") for i in range(300)] if n < 2 else []   # short pages, not last
    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: Mgr())
    monkeypatch.setattr(ch, "_get_expert", lambda *a, **k: _Expert([]))
    ch._ROOTS_CACHE.clear()
    app = FastAPI(); app.include_router(ch.router)
    d = TestClient(app).get("/api/collections/roots").json()
    assert sizes == [(0, 1000), (1000, 1000), (2000, 1000)] and d["total"] == 600 and d["capped"] is False


def _seen_keys(client_, **headers):
    """The cache key(s) a real request creates, by making it."""
    ch._ROOTS_CACHE.clear()
    assert client_.get("/api/collections/roots", headers=headers).status_code == 200
    return set(ch._ROOTS_CACHE)


def test_warm_up_warms_exactly_the_keys_page_requests_use_lineage_on_and_off(client, monkeypatch):
    import egeria_auth
    app = FastAPI(); app.add_middleware(egeria_auth.EgeriaTokenMiddleware); app.include_router(ch.router)
    client(PAGES)
    c = TestClient(app)
    key_on = _seen_keys(c, **{"X-Egeria-For-Lineage": "true"})       # what a default browser visitor sends
    key_off = _seen_keys(c)
    assert len(key_on) == len(key_off) == 1 and key_on != key_off and next(iter(key_on)).endswith("|fl")
    ch._ROOTS_CACHE.clear()
    ch.warm_roots_cache()
    assert set(ch._ROOTS_CACHE) == key_on | key_off                  # both passes, same keys as real requests
    # and the toggle is restored afterwards, so the warm-up leaks nothing into later work
    assert egeria_auth._for_lineage.get() is False
    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: (_ for _ in ()).throw(AssertionError("not cached")))
    assert c.get("/api/collections/roots", headers={"X-Egeria-For-Lineage": "true"}).json()["total"] == 3
    assert c.get("/api/collections/roots").json()["total"] == 3


def test_warm_up_runs_lineage_on_first_then_off_and_restores_state(client, monkeypatch):
    import egeria_auth
    client(PAGES); seen = []
    real = ch._roots_payload
    def spy(*a, **k):
        seen.append(egeria_auth.for_lineage_requested()); return real(*a, **k)
    monkeypatch.setattr(ch, "_roots_payload", spy)
    ch._ROOTS_CACHE.clear(); ch.warm_roots_cache()
    assert seen == [True, False] and egeria_auth.for_lineage_requested() is False


def test_one_failing_pass_does_not_stop_the_other(client, monkeypatch):
    import egeria_auth
    client(PAGES); real = ch._roots_payload
    def flaky(*a, **k):
        if egeria_auth.for_lineage_requested(): raise RuntimeError("on-pass failed")
        return real(*a, **k)
    monkeypatch.setattr(ch, "_roots_payload", flaky)
    ch._ROOTS_CACHE.clear(); ch.warm_roots_cache()
    assert len(ch._ROOTS_CACHE) == 1 and not next(iter(ch._ROOTS_CACHE)).endswith("|fl")


def test_roots_cache_ignores_a_password_in_the_query_string(client):
    # user_pwd is no longer a query param (BRIEF-PORTAL-PLATFORM-URL-ALLOWLIST): a password in a URL lands in
    # access logs. One sent anyway is ignored -- it neither changes the cache key nor reaches it.
    c = client(PAGES)
    ch._ROOTS_CACHE.clear()
    c.get("/api/collections/roots", params={"user_id": "peter", "user_pwd": "right"})
    assert len(ch._ROOTS_CACHE) == 1
    c.get("/api/collections/roots", params={"user_id": "peter", "user_pwd": "wrong"})     # same user id, other password
    assert len(ch._ROOTS_CACHE) == 1                                                      # the query password is ignored
    assert all("right" not in k and "wrong" not in k for k in ch._ROOTS_CACHE)


def test_warm_up_failure_is_logged_not_cached_and_never_raises(client, monkeypatch):
    client(PAGES)
    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("egeria not up yet")))
    ch._ROOTS_CACHE.clear()
    ch.warm_roots_cache()                      # must not raise
    assert ch._ROOTS_CACHE == {}


def test_warm_up_partial_answer_is_not_cached(client):
    client([PAGES[0]], fail_at=1)
    ch._ROOTS_CACHE.clear()
    ch.warm_roots_cache()
    assert ch._ROOTS_CACHE == {}


def test_startup_hook_is_non_blocking_and_switchable():
    src = (Path(__file__).resolve().parent.parent / "pyegeria_handler.py").read_text()
    assert 'PORTAL_WARM_COLLECTIONS", "1") != "0"' in src and 'threading.Thread(target=warm_roots_cache, daemon=True' in src


EXPECTED_ROUTES = {
    ("GET", "/api/collections/roots"),
    ("GET", "/api/collections/{root_guid}/tree"),
    ("GET", "/api/collections/{node_guid}/children"),
    ("GET", "/api/collections/by-type"),
    ("POST", "/api/collections"),
    ("GET", "/api/collections/{node_guid}"),
    ("POST", "/api/collections/{collection_guid}/members"),
    ("DELETE", "/api/collections/{collection_guid}/members"),
}


def test_the_router_still_has_all_eight_collections_routes():
    """A truncated edit once dropped seven of these (hierarchy, detail, create, membership) and every test
    passed. The Collections view needs all of them, so list them: losing one must fail here."""
    have = {(m, r.path) for r in ch.router.routes for m in (getattr(r, "methods", None) or ())}
    assert EXPECTED_ROUTES <= have, f"missing routes: {sorted(EXPECTED_ROUTES - have)}"
    assert len([r for r in ch.router.routes if getattr(r, "path", "")]) == 8


def test_roots_sends_x_cache_hit_and_miss_headers(client):
    c = client(PAGES)
    ch._ROOTS_CACHE.clear()
    a = c.get("/api/collections/roots"); b = c.get("/api/collections/roots")
    assert (a.headers["X-Cache"], b.headers["X-Cache"]) == ("miss", "hit")
    assert "X-Cache-At" in b.headers and "X-Cache-Age" in b.headers
