"""A SemanticAssignment read that stops at its cap is a lower bound, and the people reading it are told so:
the term panel says "at least N", and the schema tree says its term badges may be incomplete. The schema
tree follows the As-of slider (tree, node lookups and badges at one time)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import semantic_links as sl  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
T = "2026-11-06T00:00:00.000Z"


class _CE:
    """Serves `n_rels` SemanticAssignments for term `t` in pages, honouring startFrom/pageSize."""
    def __init__(self, n_rels, term="t"):
        self.rels = [{"end1": {"guid": f"e{i}"}, "end2": {"guid": term}} for i in range(n_rels)]
        self.bodies = []

    def get_relationships(self, **k):
        b = k["body"]; self.bodies.append(b)
        return self.rels[b["startFrom"]: b["startFrom"] + b["pageSize"]]

    def get_element_by_guid(self, **k):
        self.bodies.append(k["body"])
        return {"elementHeader": {"type": {"typeName": "Column"}}, "properties": {"displayName": k["guid"]}}


@pytest.fixture(autouse=True)
def _ends(monkeypatch):
    monkeypatch.setattr(sl, "_end_guid", lambda end: end.get("guid"))
    monkeypatch.setattr(sl, "_end_is_term", lambda end: None)
    sl._ASSIGN_CACHE.clear()          # every test starts with no cached read
    yield
    sl._ASSIGN_CACHE.clear()


def test_a_read_that_ends_on_an_empty_page_is_complete():
    links, capped = sl._fetch_semantic_assignments(_CE(1500))
    assert len(links) == 1500 and capped is False


def test_a_read_that_fills_every_page_is_capped():
    links, capped = sl._fetch_semantic_assignments(_CE(sl.READ_LIMIT + 1))
    assert len(links) == sl.READ_LIMIT and capped is True


def test_exactly_the_limit_is_still_reported_capped_because_the_next_page_was_never_read():
    assert sl._fetch_semantic_assignments(_CE(sl.READ_LIMIT))[1] is True


def test_both_public_helpers_carry_the_flag_and_the_time():
    ce = _CE(sl.READ_LIMIT + 10)
    els, capped = sl.elements_for_term_guid(ce, "t", T)
    assert capped is True and all(b.get("asOfTime") == T for b in ce.bodies)
    terms, capped = sl.terms_for_element_guids(_CE(3), {"e0", "e1"}, None)
    assert capped is False and set(terms) == {"e0", "e1"}


def test_assigned_elements_route_reports_capped_and_the_limit(monkeypatch):
    import glossary_handler as gh
    monkeypatch.setattr(gh, "_get_classification_explorer", lambda *a, **k: _CE(sl.READ_LIMIT + 1))
    app = FastAPI(); app.include_router(gh.router)
    d = TestClient(app).get("/api/glossary/term/t/assigned-elements").json()
    assert d["capped"] is True and d["readLimit"] == sl.READ_LIMIT and d["total"] == sl.READ_LIMIT
    sl._ASSIGN_CACHE.clear()          # same caller: the capped read above would otherwise be served from cache
    monkeypatch.setattr(gh, "_get_classification_explorer", lambda *a, **k: _CE(2))
    d = TestClient(app).get("/api/glossary/term/t/assigned-elements").json()
    assert d["capped"] is False and d["total"] == 2


# ── schema tree ──────────────────────────────────────────────────────────────

def _schema(monkeypatch, ce, raise_terms=False):
    import tech_catalog_handler as tc
    calls = {"graph": [], "lookups": []}

    class _AC:
        def get_asset_graph_by_guid(self, guid, **k):
            calls["graph"].append(k["body"])
            return {"elementHeader": {"guid": guid}, "schemaType": {"relatedElement": {"elementHeader": {"guid": "st"}}}}

    monkeypatch.setattr(tc, "_asset_maker", lambda *a, **k: object())
    monkeypatch.setattr(tc, "_asset_catalog_from_asset_maker", lambda m: _AC())

    def fake_serialize(el, mgr=None, as_of_time=None, **kw):
        calls["serialize_as_of"] = as_of_time
        return {"attributes": [{"guid": "e0"}], "termsStatus": None}
    return tc, calls, fake_serialize


def test_schema_route_passes_the_slider_time_to_the_tree_read(monkeypatch):
    tc, calls, fake = _schema(monkeypatch, None)
    monkeypatch.setattr(tc, "_serialize_schema", fake)
    app = FastAPI(); app.include_router(tc.router)
    c = TestClient(app)
    c.get("/api/tech-catalog/assets/a1/schema")
    assert calls["graph"][-1] == {"class": "ResultsRequestBody", "graphQueryDepth": 5} and calls["serialize_as_of"] is None
    c.get("/api/tech-catalog/assets/a1/schema", params={"as_of_time": T})
    assert calls["graph"][-1]["asOfTime"] == T and calls["serialize_as_of"] == T


@pytest.mark.parametrize("n_rels,expected", [(2, "complete"), (sl.READ_LIMIT + 1, "capped"), (None, "failed")])
def test_schema_terms_status(monkeypatch, n_rels, expected):
    import tech_catalog_handler as tc

    class _Failing:
        def get_relationships(self, **k):
            raise RuntimeError("server error")

    ce = _Failing() if n_rels is None else _CE(n_rels)
    monkeypatch.setattr(tc, "_classification_explorer_from_asset_maker", lambda mgr: ce)
    monkeypatch.setattr(tc, "_metadata_expert_from_asset_maker", lambda mgr: (_ for _ in ()).throw(RuntimeError("no lookups")))
    rel_type = next(iter(tc._SCHEMA_CONTAINMENT_RELS))
    el = {"schemaType": {"relatedElement": {"elementHeader": {"guid": "st"}, "properties": {"displayName": "S"}}},
          "relationships": [{"startingElementGUID": "st", "relatedElementAtEnd1": False,
                             "relatedElement": {"elementHeader": {"guid": "e0"}, "properties": {"displayName": "col"}},
                             "relationshipHeader": {"type": {"typeName": rel_type}}}]}
    out = tc._serialize_schema(el, mgr=object(), as_of_time=None)
    assert out["attributes"], "fixture did not produce a tree"
    assert out["termsStatus"] == expected and out["termsReadLimit"] == sl.READ_LIMIT


def test_the_ui_says_so_when_the_read_was_cut_short_or_failed():
    ui = (HERE / "static" / "egeria-shared-ui.js").read_text()
    assert "'At least ' + data.total + ' — the assignment read stopped at '" in ui
    assert "data.total === 0 && !data.capped" in ui                      # capped-and-empty is not "none assigned"
    tcat = (HERE / "tech-catalog.html").read_text()
    assert "data.termsStatus === 'capped'" in tcat and "data.termsStatus === 'failed'" in tcat
    pane = tcat[tcat.index("function SchemaPane("): tcat.index("// LineagePane")]
    assert "useAsOf()" in pane and "'/schema' + asOfParam(asOf)" in pane and "key: asOf || 'now'" in pane


# ── the short shared cache of the assignment read ────────────────────────────

class _CountingCE(_CE):
    platform_url, view_server = "https://p", "vs"

    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.reads = 0

    def get_relationships(self, **k):
        if k["body"]["startFrom"] == 0:
            self.reads += 1
        return super().get_relationships(**k)


@pytest.fixture
def ce(monkeypatch):
    sl._ASSIGN_CACHE.clear()
    import egeria_auth
    monkeypatch.setattr(egeria_auth, "lineage_key", lambda: "")
    return _CountingCE(3)


def test_same_identity_and_time_hits(ce):
    sl.elements_for_term_guid(ce, "t", None, identity="t:aaa")
    sl.terms_for_element_guids(ce, {"e0"}, None, identity="t:aaa")       # the schema badges reuse the read
    assert ce.reads == 1


def test_other_identity_or_time_misses(ce):
    sl.elements_for_term_guid(ce, "t", None, identity="t:aaa")
    sl.elements_for_term_guid(ce, "t", None, identity="t:bbb")
    sl.elements_for_term_guid(ce, "t", T, identity="t:aaa")
    assert ce.reads == 3


def test_no_identity_means_no_cache(ce):
    sl.elements_for_term_guid(ce, "t", None, identity=None)
    sl.elements_for_term_guid(ce, "t", None, identity=None)
    assert ce.reads == 2 and sl._ASSIGN_CACHE == {}


def test_a_failed_read_is_never_cached(ce):
    class _Boom(_CountingCE):
        def get_relationships(self, **k):
            raise RuntimeError("server error")
    with pytest.raises(RuntimeError):
        sl.elements_for_term_guid(_Boom(0), "t", None, identity="t:aaa")
    assert sl._ASSIGN_CACHE == {}


def test_lineage_toggle_is_in_the_key(ce, monkeypatch):
    import egeria_auth
    sl.elements_for_term_guid(ce, "t", None, identity="t:aaa")
    monkeypatch.setattr(egeria_auth, "lineage_key", lambda: "|fl")
    sl.elements_for_term_guid(ce, "t", None, identity="t:aaa")
    assert ce.reads == 2
