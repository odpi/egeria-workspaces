"""pyegeria's result notes reach the browser through /api/report-specs/execute.

pyegeria 6.2.37+ puts words beside a result in `notes` (F8: "Showing the first 100: the query stopped
at its page size of 100; more may exist."). The Portal used to drop them in the browser; this checks the
server side never strips them, live or from the result cache, so the page has something to show.

The results are real: pyegeria (upstream main 70da8d51) replaying its own Egeria captures from laz,
see fixtures/result_notes_pyegeria_replay_2026_11_11.json. Offline: exec_report_spec is a fake that
returns them.
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import report_specs_handler as rh  # noqa: E402
from result_cache import ResultCache  # noqa: E402

FX = json.loads((Path(__file__).resolve().parent / "fixtures" / "result_notes_pyegeria_replay_2026_11_11.json").read_text())
CAPPED = FX["digital_products_dict"]
PLAIN = FX["risk_register_dict"]
F8 = "Showing the first 100: the query stopped at its page size of 100; more may exist."


def test_fixture_is_the_real_shape():
    assert CAPPED["kind"] == "json" and len(CAPPED["data"]) == 100 and CAPPED["notes"] == [F8]
    assert "notes" not in PLAIN and len(PLAIN["data"]) == 12


@pytest.fixture
def client(monkeypatch):
    import pyegeria.view.format_set_executor as fse
    state = {"result": CAPPED, "calls": 0}

    def fake_exec(name, **kwargs):
        state["calls"] += 1
        return copy.deepcopy(state["result"])

    monkeypatch.setattr(fse, "exec_report_spec", fake_exec)
    monkeypatch.setattr(rh, "_RESULT_CACHE", ResultCache(ttl=300, max_stale=3600, max_entries=10, refresh_backoff=30))
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(rh.router)
    return TestClient(app), state


def _post(c, cache):
    return c.post("/api/report-specs/execute",
                  json={"spec_name": "Digital-Products", "output_format": "DICT",
                        "params": {"search_string": "*"}, "cache": cache})


def test_live_run_passes_notes_through(client):
    c, _ = client
    body = _post(c, cache=False).json()
    assert body["notes"] == [F8] and len(body["data"]) == 100


def test_cached_run_keeps_notes(client):
    c, state = client
    first, second = _post(c, cache=True), _post(c, cache=True)
    assert (first.headers["X-Cache"], second.headers["X-Cache"]) == ("miss", "hit")
    assert first.json()["notes"] == second.json()["notes"] == [F8]
    assert state["calls"] == 1


def test_result_without_notes_gains_none(client):
    c, state = client
    state["result"] = PLAIN
    assert "notes" not in _post(c, cache=False).json()
