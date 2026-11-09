"""The As-of slider reaches the secondary panels (diagrams, assigned elements, raw JSON), and the live-only
widgets (feedback, comments) say they are current. With no time set nothing changes: the same requests, the
same pyegeria calls."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
SHARED = (HERE / "static" / "egeria-shared-ui.js").read_text()
T = "2026-11-06T00:00:00.000Z"


def _function(src: str, name: str) -> str:
    start = src.index(f"function {name}(")
    nxt = re.search(r"\n(?:async )?function [A-Za-z_]+\(", src[start + 10:])
    return src[start: start + 10 + nxt.start()] if nxt else src[start:]


# ── frontend: the shared widgets read AsOfContext ────────────────────────────

def test_context_is_defined_once_and_guarded_for_plain_dom_pages():
    assert SHARED.count("var AsOfContext =") == 1
    assert "var AsOfContext = (typeof React !== 'undefined') ? React.createContext(null) : null;" in SHARED


@pytest.mark.parametrize("widget,urls", [
    ("MermaidSection", ["'/api/mermaid/' + encodeURIComponent(guid) + asOfParam(asOf)",
                        "'/api/mermaid/' + encodeURIComponent(guid) + '/anchored' + asOfParam(asOf)"]),
    ("AssignedElementsSection", ["'/assigned-elements' + asOfParam(asOf)"]),
    ("RawJsonViewer", ["asOfParam(asOf, depth != null ? '&' : '?')"]),
])
def test_widget_sends_as_of_time_from_the_context(widget, urls):
    body = _function(SHARED, widget)
    assert "useAsOf()" in body, f"{widget} does not read AsOfContext"
    for u in urls:
        assert u in body, f"{widget} request lacks as_of_time: {u}"


@pytest.mark.parametrize("widget,deps", [
    ("MermaidSection", "[guid, asOf]"),
    ("AssignedElementsSection", "[termGuid, asOf]"),
])
def test_loaded_widgets_reset_when_the_time_moves(widget, deps):
    assert deps in _function(SHARED, widget), f"{widget} keeps showing another time's data after the slider moves"


def test_as_of_param_is_empty_for_now_so_now_requests_are_unchanged():
    helper = _function(SHARED, "asOfParam")
    assert "return asOf ? (sep || '?') + 'as_of_time=' + encodeURIComponent(asOf) : '';" in helper


def test_a_404_at_a_past_time_says_did_not_exist_not_an_empty_diagram():
    body = _function(SHARED, "MermaidSection")
    assert "r.status === 404 && asOf" in body and "did not exist at" in body
    assert "!absent && React.createElement(GraphTabs" in body


@pytest.mark.parametrize("widget", ["EgeriaFeedbackWidget", "EgeriaCommentsSection"])
def test_live_only_widgets_say_they_are_current(widget):
    assert "React.createElement(CurrentNotAsOfNote, null)" in _function(SHARED, widget)
    note = _function(SHARED, "CurrentNotAsOfNote")
    assert "if (!asOf) return null;" in note and "'current — not as of '" in note


# ── frontend: every view that renders a TimeSlider provides the context ──────

def _slider_views():
    out = []
    for page in ("type-explorer.html", "tech-catalog.html", "lineage-explorer.html", "egeria-insights.html",
                 "egeria-audit.html", "egeria-operations.html", "resource-browser.html", "data-mesh.html"):
        p = HERE / page
        if not p.exists():
            continue
        src = p.read_text()
        for m in re.finditer(r"(?:React\.createElement|el)\(TimeSlider\b", src):
            fn_start = max(x.start() for x in re.finditer(r"\nfunction [A-Za-z_]+\(", src[:m.start()]))
            name = re.match(r"\nfunction ([A-Za-z_]+)\(", src[fn_start:]).group(1)
            out.append((page, name, _function(src, name)))
    return out


SLIDER_VIEWS = _slider_views()


def test_the_slider_views_are_all_found():
    names = {n for _, n, _ in SLIDER_VIEWS}
    assert {"GlossaryTermsTab", "InformationSupplyChainView", "ProjectsView", "AssetTabView", "MainPanel"} <= names
    assert len(names) >= 13


@pytest.mark.parametrize("page,name,body", SLIDER_VIEWS, ids=[f"{p}:{n}" for p, n, _ in SLIDER_VIEWS])
def test_every_time_slider_view_provides_as_of_context(page, name, body):
    m = re.search(r"React\.createElement\(AsOfContext\.Provider, \{ value: (\w+) \}", body)
    assert m, f"{page}:{name} renders a TimeSlider but does not provide AsOfContext"
    assert re.search(rf"\b{m.group(1)}\b", body.split("AsOfContext.Provider")[0]), \
        f"{page}:{name} provides {m.group(1)}, which it does not define before its return"


# ── backend: the time reaches pyegeria; no time = the old call exactly ───────

class _Recorder:
    def __init__(self, result=None):
        self.calls, self.result = [], result

    def __getattr__(self, name):
        def call(*a, **k):
            self.calls.append((name, a, k))
            return self.result if self.result is not None else {}
        return call


def _client(module):
    app = FastAPI(); app.include_router(module.router)
    return TestClient(app)


def test_mermaid_context_diagram(monkeypatch):
    import mermaid_handler as mh
    rec = _Recorder({"mermaidGraph": "graph TD; a-->b"})
    monkeypatch.setattr(mh, "_get_classifier", lambda *a, **k: rec)
    c = _client(mh)
    c.get("/api/mermaid/g1")
    assert rec.calls[-1] == ("get_element_by_guid", ("g1",), {
        "output_format": "JSON", "graph_query_depth": mh._MERMAID_GRAPH_QUERY_DEPTH,
        "max_mermaid_node_count": mh._MERMAID_MAX_NODES})                  # unchanged without a time
    c.get("/api/mermaid/g1", params={"as_of_time": T})
    name, a, k = rec.calls[-1]
    assert k["body"] == {"class": "GetRequestBody", "asOfTime": T,     # the graph settings are repeated
                         "graphQueryDepth": mh._MERMAID_GRAPH_QUERY_DEPTH, "maxMermaidNodeCount": mh._MERMAID_MAX_NODES}


def test_mermaid_anchored(monkeypatch):
    import mermaid_handler as mh
    rec = _Recorder("graph TD; a-->b")
    monkeypatch.setattr(mh, "_get_expert", lambda *a, **k: rec)
    c = _client(mh)
    c.get("/api/mermaid/g1/anchored")
    assert rec.calls[-1] == ("get_anchored_element_graph", ("g1",), {"mermaid_only": True})
    c.get("/api/mermaid/g1/anchored", params={"as_of_time": T})
    assert rec.calls[-1] == ("get_anchored_element_graph", ("g1",), {"mermaid_only": True, "as_of_time": T})


def test_mermaid_404_only_at_a_past_time(monkeypatch):
    import mermaid_handler as mh
    from pyegeria import PyegeriaNotFoundException

    class _Missing:
        def get_element_by_guid(self, *a, **k):
            raise PyegeriaNotFoundException.__new__(PyegeriaNotFoundException)

    monkeypatch.setattr(mh, "_get_classifier", lambda *a, **k: _Missing())
    c = _client(mh)
    assert c.get("/api/mermaid/g1").status_code == 200                   # unchanged without a time
    r = c.get("/api/mermaid/g1", params={"as_of_time": T})
    assert r.status_code == 404 and "did not exist" in r.json()["detail"]


def test_assigned_elements(monkeypatch):
    import glossary_handler as gh
    import semantic_links as sl
    rel = [{"end1": {"guid": "col-1"}, "end2": {"guid": "term-1"}}]
    rec = _Recorder()

    def get_relationships(**k):
        rec.calls.append(("get_relationships", (), k))
        return rel if k["body"]["startFrom"] == 0 else []          # one page, then an empty page

    rec.get_relationships = get_relationships
    rec.get_element_by_guid = lambda **k: rec.calls.append(("get_element_by_guid", (), k)) or {
        "elementHeader": {"type": {"typeName": "Column"}}, "properties": {"displayName": "c"}}
    monkeypatch.setattr(gh, "_get_classification_explorer", lambda *a, **k: rec)
    monkeypatch.setattr(sl, "_end_guid", lambda end: end.get("guid"))
    monkeypatch.setattr(sl, "_end_is_term", lambda end: None)
    c = _client(gh)
    assert c.get("/api/glossary/term/term-1/assigned-elements").json()["total"] == 1
    rels = [k for n, _, k in rec.calls if n == "get_relationships"]
    gets = [k for n, _, k in rec.calls if n == "get_element_by_guid"]
    assert [r["body"] for r in rels] == [                          # no time: no asOfTime anywhere
        {"class": "ResultsRequestBody", "startFrom": 0, "pageSize": 1000},
        {"class": "ResultsRequestBody", "startFrom": 1000, "pageSize": 1000}]
    assert gets[-1]["body"] == {"class": "GetRequestBody", "graphQueryDepth": 0}
    rec.calls.clear()
    c.get("/api/glossary/term/term-1/assigned-elements", params={"as_of_time": T})
    rels = [k for n, _, k in rec.calls if n == "get_relationships"]
    gets = [k for n, _, k in rec.calls if n == "get_element_by_guid"]
    assert all(r["body"]["asOfTime"] == T for r in rels)
    assert gets[-1]["body"] == {"class": "GetRequestBody", "graphQueryDepth": 0, "asOfTime": T}


def test_semantic_assignments_never_ask_for_more_than_egerias_page_limit():
    import semantic_links as sl
    sizes = []

    class _CE:
        def get_relationships(self, **k):
            sizes.append(k["page_size"])
            if k["page_size"] > 1000:
                raise RuntimeError("OMAG-COMMON-400-010 pageSize > 1000")
            # a SHORT first page is not the last one: only an empty page ends the read
            return [{"end1": {"guid": f"e{k['body']['startFrom']}"}, "end2": {"guid": "t"}}] if k["body"]["startFrom"] < 2000 else []

    out = sl._fetch_semantic_assignments(_CE())
    assert max(sizes) <= 1000 and len(out) == 2 and len(sizes) == 3


def test_a_failed_assignment_read_is_an_error_not_an_empty_answer(monkeypatch):
    import glossary_handler as gh

    class _CE:
        def get_relationships(self, **k):
            raise RuntimeError("server error")

    monkeypatch.setattr(gh, "_get_classification_explorer", lambda *a, **k: _CE())
    r = _client(gh).get("/api/glossary/term/term-1/assigned-elements")
    assert r.status_code >= 500


def test_raw_json(monkeypatch):
    import pyegeria
    import tech_catalog_handler as tc
    seen = []

    class _ME:
        def __init__(self, *a, **k): pass
        def get_metadata_element_by_guid(self, guid, **k):
            seen.append(k); return {"elementHeader": {}, "properties": {}}

    monkeypatch.setattr(pyegeria, "MetadataExpert", _ME)
    monkeypatch.setattr(tc, "_apply_token", lambda *a, **k: None)
    c = _client(tc)
    c.get("/api/debug/raw/g1")
    assert seen[-1] == {"graph_query_depth": 1, "output_format": "JSON"}  # unchanged without a time
    c.get("/api/debug/raw/g1", params={"as_of_time": T})
    assert seen[-1] == {"graph_query_depth": 1, "output_format": "JSON", "as_of_time": T}
