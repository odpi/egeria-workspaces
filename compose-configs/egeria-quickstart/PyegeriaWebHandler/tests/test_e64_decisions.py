"""The Decision card's backend (e64_handler: /api/decisions, /api/decisions/{guid}).

No live server: ClassificationExplorer is replaced by a fake (tests/e64_fixtures.py), whose /api/about
answer drives the version gate. On an Egeria before 6.4 each route answers HTTP 200 with needs64 and the
gate's words: never an error, and never an empty list that would read as "none".
"""
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import e64_handler as h  # noqa: E402
import egeria_6_4_support as e64  # noqa: E402
from e64_fixtures import (ABOUT_6_3, ABOUT_6_4, OUTCOMES, TWO_ASSESSMENTS_ONE_ELEMENT, FakeExplorer,  # noqa: E402
                          client_error, decision)


@pytest.fixture
def client(monkeypatch):
    app = FastAPI()
    app.include_router(h.router)
    e64.clear_cache()

    def setup(fake):
        async def factory(url=None, server=None):
            return fake
        monkeypatch.setattr(h, "_explorer_async", factory)
        return TestClient(app)
    yield setup
    e64.clear_cache()


# ── the version gate ─────────────────────────────────────────────────────────────────────────────────────

def test_list_before_6_4_says_needs_6_4_and_sends_nothing(client):
    fake = FakeExplorer(about=ABOUT_6_3)
    r = client(fake).get("/api/decisions")
    assert r.status_code == 200
    body = r.json()
    assert body["needs64"] is True
    assert "needs Egeria 6.4" in body["words"] and "runs Egeria 6.3" in body["words"]
    assert fake.calls == []                       # nothing was sent to Egeria


def test_detail_before_6_4_says_needs_6_4(client):
    fake = FakeExplorer(about=ABOUT_6_3, elements={"dec-1": decision()})
    r = client(fake).get("/api/decisions/dec-1")
    assert r.status_code == 200 and r.json()["needs64"] is True
    assert r.json()["words"].startswith("The Decision card needs Egeria 6.4")
    assert fake.calls == []


def test_unknown_version_then_bare_404_is_needs_6_4_not_an_error(client):
    fake = FakeExplorer(about=RuntimeError("about unreadable"), fail=client_error(404))
    c = client(fake)
    for path in ("/api/decisions", "/api/decisions/dec-1"):
        r = c.get(path)
        assert r.status_code == 200, path
        assert r.json()["needs64"] is True
        assert "does not serve this request (HTTP 404)" in r.json()["words"]


def test_a_404_on_a_6_4_platform_is_an_error_not_needs_6_4(client):
    # read-back W1: laz is on 6.4, so a 404 there is a real failure and must not hide behind the gate's words
    c = client(FakeExplorer(about=ABOUT_6_4, fail=client_error(404)))
    for path in ("/api/decisions", "/api/decisions/dec-1"):
        r = c.get(path)
        assert r.status_code >= 400, path
        assert "needs64" not in r.text and "needs Egeria 6.4" not in r.text


def test_other_errors_stay_errors(client):
    r = client(FakeExplorer(about=ABOUT_6_4, fail=client_error(400))).get("/api/decisions")
    assert r.status_code >= 400 and "needs64" not in r.text


def test_status_route(client):
    r = client(FakeExplorer(about=ABOUT_6_3)).get("/api/e64/status")
    assert r.json()["carries"] is False and "needs Egeria 6.4" in r.json()["words"]
    assert r.json()["gateSource"] in ("pyegeria", "vendored")


# ── the list ─────────────────────────────────────────────────────────────────────────────────────────────

def test_list_on_6_4_pages_and_sorts(client):
    page1 = [decision("d-%03d" % i, props={"displayName": "Decision %03d" % (199 - i)}) for i in range(100)]
    page2 = [decision("d-%03d" % i, props={"displayName": "Decision %03d" % (199 - i)}) for i in range(100, 105)]
    fake = FakeExplorer(about=ABOUT_6_4, pages=[page1, page2])
    body = client(fake).get("/api/decisions").json()
    assert body["total"] == 105 and not body.get("needs64")
    assert body["items"][0]["displayName"] == "Decision 095"
    assert body["items"][0]["disposition"] == "Approved"
    assert [c[0] for c in fake.calls] == ["by-type"] * 3       # a short page is not taken as the end


def test_empty_list_on_6_4_is_empty_not_needs_6_4(client):
    body = client(FakeExplorer(about=ABOUT_6_4, pages=[])).get("/api/decisions").json()
    assert body == {"items": [], "total": 0, "capped": False}


# ── the card ─────────────────────────────────────────────────────────────────────────────────────────────

def test_card_header_body_and_dates(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"dec-1": decision(assessments=[], outcomes=OUTCOMES)})
    d = client(fake).get("/api/decisions/dec-1").json()
    assert (d["disposition"], d["importance"], d["contentStatus"]) == ("Approved", "High", "ACTIVE")
    assert d["summary"].startswith("Use OpenLineage") and d["scope"] == "Data platform"
    assert d["usage"] == "Pipeline design reviews" and d["notes"].startswith("Agreed")
    assert d["implications"] == ["Every pipeline needs an OpenLineage emitter", "Old pipelines migrate by Q3"]
    assert d["nextReviewTime"].startswith("2026-09-01") and d["expiryTime"].startswith("2027-01-01")
    assert ("by-guid", "dec-1", "Decision", 1) in fake.calls      # a graph read: every list is asked for


def test_two_assessments_of_one_element_are_two_rows_keyed_by_relationship_guid(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"dec-1": decision(assessments=TWO_ASSESSMENTS_ONE_ELEMENT)})
    d = client(fake).get("/api/decisions/dec-1").json()
    rows = d["assessments"]
    assert [r["relationshipGuid"] for r in rows] == ["as-1", "as-2", "as-3"]
    assert [r["guid"] for r in rows] == ["term-1", "term-1", "term-2"]
    assert rows[0]["label"] == "Initial review" and rows[1]["label"] == "Re-review"
    assert rows[1]["assessorTypeName"] == "SoftwareCapability" and rows[1]["assessorPropertyName"] == "score"
    assert d["lists"]["inputsToDecision"] == {"state": "read"}


def test_lists_none_when_read_and_absent(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"dec-1": decision()})
    d = client(fake).get("/api/decisions/dec-1").json()
    assert d["assessments"] == [] and d["outcomes"] == []
    assert d["lists"] == {"inputsToDecision": {"state": "none"}, "decisionOutcomes": {"state": "none"}}


def test_assessment_and_outcome_lists_are_not_repeated_in_generic_relationships(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"dec-1": decision(assessments=TWO_ASSESSMENTS_ONE_ELEMENT,
                                                                       outcomes=OUTCOMES)})
    d = client(fake).get("/api/decisions/dec-1").json()
    assert "inputsToDecision" not in d["relationships"] and "decisionOutcomes" not in d["relationships"]
    assert d["outcomes"][0]["label"] == "Rollout" and d["outcomes"][0]["disposition"] == "Started"


def test_unknown_version_but_a_decision_came_back_means_6_4(client):
    fake = FakeExplorer(about=RuntimeError("about unreadable"), elements={"dec-1": decision()})
    d = client(fake).get("/api/decisions/dec-1").json()
    assert d["lists"]["inputsToDecision"] == {"state": "none"}


def test_missing_and_wrong_type_are_404(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"x": {"elementHeader": {"guid": "x", "type": {"typeName": "Project"}}}})
    c = client(fake)
    assert c.get("/api/decisions/nope").status_code == 404
    r = c.get("/api/decisions/x")
    assert r.status_code == 404 and "not a Decision" in r.json()["detail"]


def test_routes_take_no_credentials_in_the_query():
    for fn in (h.list_decisions, h.get_decision, h.e64_status):
        assert not {"user_id", "user_pwd"} & set(inspect.signature(fn).parameters)


def test_routes_are_async_and_use_the_async_factory():
    src = inspect.getsource(h)
    assert "create_egeria_bearer_token()" not in src and "run_until_complete" not in src
    for fn in (h.list_decisions, h.get_decision, h.e64_status):
        assert inspect.iscoroutinefunction(fn)
