"""The DataValue / LiteralDataValue card's backend (e64_handler: /api/data-values, /api/data-values/{guid}).

No live server: ClassificationExplorer is replaced by a fake (tests/e64_fixtures.py). On an Egeria before
6.4 each route answers HTTP 200 with needs64 and the gate's words: never an error, never "none".
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
from e64_fixtures import (ABOUT_6_3, ABOUT_6_4, EMBEDDED, PART_OF, STORED_IN, USED_BY, FakeExplorer,  # noqa: E402
                          client_error, data_value)


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


def _card(client, el):
    return client(FakeExplorer(about=ABOUT_6_4, elements={el["elementHeader"]["guid"]: el})).get(
        "/api/data-values/" + el["elementHeader"]["guid"]).json()


# ── the version gate ─────────────────────────────────────────────────────────────────────────────────────

def test_before_6_4_list_and_card_say_needs_6_4_and_send_nothing(client):
    fake = FakeExplorer(about=ABOUT_6_3, elements={"dv-1": data_value()})
    c = client(fake)
    for path, lead in (("/api/data-values", "The Data Values list"), ("/api/data-values/dv-1", "The Data Value card")):
        r = c.get(path)
        assert r.status_code == 200 and r.json()["needs64"] is True
        assert r.json()["words"].startswith(lead + " needs Egeria 6.4")
    assert fake.calls == []


def test_unknown_version_then_bare_404_is_needs_6_4(client):
    c = client(FakeExplorer(about=RuntimeError("x"), fail=client_error(404)))
    for path in ("/api/data-values", "/api/data-values/dv-1"):
        assert c.get(path).json()["needs64"] is True


def test_a_404_on_a_6_4_platform_is_an_error_not_needs_6_4(client):
    c = client(FakeExplorer(about=ABOUT_6_4, fail=client_error(404)))
    for path in ("/api/data-values", "/api/data-values/dv-1"):
        r = c.get(path)
        assert r.status_code >= 400 and "needs64" not in r.text, path


# ── the list ─────────────────────────────────────────────────────────────────────────────────────────────

def test_list_reads_data_values_including_literals(client):
    fake = FakeExplorer(about=ABOUT_6_4, pages=[[data_value("dv-1"), data_value("dv-2", literal=False)]])
    body = client(fake).get("/api/data-values").json()
    assert fake.calls[0][1] == "DataValue"
    assert {i["typeName"] for i in body["items"]} == {"LiteralDataValue", "DataValue"}
    assert body["items"][0]["dataType"] == "string"


# ── the card ─────────────────────────────────────────────────────────────────────────────────────────────

def test_format_type_and_the_three_value_kinds(client):
    d = _card(client, data_value(value={"dataValue": "3"}))
    assert (d["dataFormat"], d["dataType"], d["length"]) == ("text/plain", "string", 3)
    assert d["value"] == {"kind": "literal", "dataValue": "3", "dataValueList": None, "dataValueMap": None}
    assert _card(client, data_value(value={"dataValueList": ["1", "2"]}))["value"]["kind"] == "list"
    m = _card(client, data_value(value={"dataValueMap": {"retries": "3", "backoff": "2s"}}))["value"]
    assert m["kind"] == "map" and m["dataValueMap"] == {"retries": "3", "backoff": "2s"}
    assert _card(client, data_value(value={"dataValue": "3", "dataValueList": ["1"]}))["value"]["kind"] == "several"


def test_a_literal_with_no_value_is_empty_and_a_plain_data_value_is_not_literal(client):
    assert _card(client, data_value())["value"]["kind"] == "empty"
    assert _card(client, data_value(literal=False))["value"] == {"kind": "not-literal"}


def test_embedded_values_ordered_by_position_with_0_unset(client):
    d = _card(client, data_value(lists={"embeddedDataValues": EMBEDDED}))
    rows = d["embedded"]
    assert [r["relationshipGuid"] for r in rows] == ["emb-1", "emb-3", "emb-n", "emb-0"]
    assert [r["position"] for r in rows] == [1, 3, None, None]
    assert [r["positionSet"] for r in rows] == [True, True, False, False]
    assert d["lists"]["embeddedDataValues"] == {"state": "read"}


def test_used_by_with_position_stored_in_and_part_of(client):
    d = _card(client, data_value(lists={"dataValueUses": USED_BY, "dataValueSources": STORED_IN,
                                        "parentDataValues": PART_OF}))
    assert [(r["displayName"], r["position"]) for r in d["usedBy"]] == [("Hourly load", 1), ("Nightly load", 2)]
    assert d["storedIn"][0]["displayName"] == "limits.csv" and d["storedIn"][0]["typeName"] == "CSVFile"
    assert d["partOf"][0]["displayName"] == "All settings" and d["partOf"][0]["position"] == 4
    for k in ("dataValueUses", "dataValueSources", "parentDataValues"):
        assert d["lists"][k] == {"state": "read"}
    assert not set(d["relationships"]) & {"dataValueUses", "dataValueSources", "embeddedDataValues", "parentDataValues"}


def test_lists_read_and_absent_are_none(client):
    d = _card(client, data_value())
    assert d["lists"] == {k: {"state": "none"} for k in
                          ("dataValueUses", "dataValueSources", "embeddedDataValues", "parentDataValues")}
    assert d["usedBy"] == d["storedIn"] == d["embedded"] == d["partOf"] == []


def test_wrong_type_is_404(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"x": {"elementHeader": {"guid": "x", "type": {"typeName": "Decision"}}}})
    r = client(fake).get("/api/data-values/x")
    assert r.status_code == 404 and "not a Data Value" in r.json()["detail"]


def test_position_of():
    assert [h.position_of({"position": v}) for v in (0, 1, "2", None, "x", True)] == [None, 1, 2, None, None, None]


def test_routes_take_no_credentials_and_are_async():
    for fn in (h.list_data_values, h.get_data_value):
        assert not {"user_id", "user_pwd"} & set(inspect.signature(fn).parameters)
        assert inspect.iscoroutinefunction(fn)
