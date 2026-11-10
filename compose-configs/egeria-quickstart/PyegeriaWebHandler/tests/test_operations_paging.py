"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Operations SPA: engine actions read newest first at graph depth 0, a page at a time, with an honest
total; catalog targets read at depth 0, paged in the body, and a read that fails is an explicit
unknown, never "no targets". No test reaches Egeria: the pyegeria clients are fakes.
"""
import asyncio
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import operations_handler as ops  # noqa: E402


def _ea(i):
    # newest first: a higher i is older
    return {"elementHeader": {"guid": f"ea-{i:05d}"},
            "properties": {"displayName": f"action {i}", "requestedStartTime": f"2026-11-10T{23 - i // 60 % 24:02d}:{59 - i % 60:02d}:00Z"}}


class FakeCuration:
    """find_engine_actions over N actions, recording every call's kwargs."""
    def __init__(self, n):
        self.items = [_ea(i) for i in range(n)]
        self.calls = []

    def find_engine_actions(self, **kw):
        self.calls.append(kw)
        s, size = kw.get("start_from", 0), kw.get("page_size", 100)
        return self.items[s:s + size]


@pytest.fixture
def api(monkeypatch):
    ops._ENGINE_ACTIONS_CACHE.clear()
    app = FastAPI()
    app.include_router(ops.router)
    return TestClient(app)


def _use(monkeypatch, fake, repo_count=None):
    monkeypatch.setattr(ops, "_automated_curation", lambda *a, **k: fake)
    monkeypatch.setattr(ops, "_repository_engine_action_count", lambda *a, **k: repo_count)


def test_engine_actions_ask_egeria_for_depth_0_newest_first(api, monkeypatch):
    fake = FakeCuration(10)
    _use(monkeypatch, fake)
    assert api.get("/api/operations/engine-actions").status_code == 200
    first = fake.calls[0]
    assert first["graph_query_depth"] == 0
    assert first["sequencing_order"] == "PROPERTY_DESCENDING"
    assert first["sequencing_property"] == "requestedStartTime"
    assert first["start_from"] == 0 and first["page_size"] == ops._EA_PAGE_DEFAULT


def test_a_full_page_is_never_the_total(api, monkeypatch):
    fake = FakeCuration(450)
    _use(monkeypatch, fake)
    d = api.get("/api/operations/engine-actions?start=0&page_size=200").json()
    assert len(d["actions"]) == 200
    assert d["more"] is True and d["total"] is None
    assert d["lowerBound"] == 201 and d["nextStart"] == 200
    assert "total" in d and d["total"] != 200


def test_paging_loop_reads_every_action_once_and_ends_exact(api, monkeypatch):
    fake = FakeCuration(450)
    _use(monkeypatch, fake, repo_count=450)
    seen, start, pages = [], 0, 0
    while start is not None and pages < 10:
        d = api.get(f"/api/operations/engine-actions?start={start}&page_size=200").json()
        seen += [a["guid"] for a in d["actions"]]
        start = d["nextStart"]
        pages += 1
    assert pages == 3 and len(seen) == 450 and len(set(seen)) == 450
    assert d["more"] is False and d["total"] == 450 and d["repositoryCount"] == 450


def test_a_short_page_is_checked_not_assumed_last(api, monkeypatch):
    # 50 rows, page 200: the page is short, so one row past it is read to know it is the end.
    fake = FakeCuration(50)
    _use(monkeypatch, fake)
    d = api.get("/api/operations/engine-actions").json()
    assert d["total"] == 50 and d["more"] is False
    assert fake.calls[1]["start_from"] == 50 and fake.calls[1]["page_size"] == 1


def test_failed_next_check_is_unknown_with_a_lower_bound(api, monkeypatch):
    fake = FakeCuration(450)
    calls = {"n": 0}
    real = fake.find_engine_actions

    def flaky(**kw):
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("Egeria hiccup")
        return real(**kw)
    fake.find_engine_actions = flaky
    _use(monkeypatch, fake)
    d = api.get("/api/operations/engine-actions").json()
    assert d["more"] is None and d["total"] is None and d["lowerBound"] == 200
    assert d["nextStart"] == 200          # can still try the next page


def test_cache_key_includes_paging(api, monkeypatch):
    fake = FakeCuration(450)
    _use(monkeypatch, fake)
    a = api.get("/api/operations/engine-actions?start=0&page_size=200").json()
    b = api.get("/api/operations/engine-actions?start=200&page_size=200").json()
    assert a["actions"][0]["guid"] != b["actions"][0]["guid"]


def test_page_summary_words():
    assert ops._page_summary(0, 0, None, None)["total"] == 0          # nothing at all: exactly none
    s = ops._page_summary(400, 0, True, None)
    assert s["more"] is False and s["total"] is None                    # past the end: not assumed exact
    s = ops._page_summary(0, 200, True, 21908)                          # the row after the page is empty
    assert s["total"] == 200 and s["repositoryCount"] == 21908
    s = ops._page_summary(0, 200, False, 21908)                         # more exist: no total, a bound
    assert s["total"] is None and s["lowerBound"] == 201 and s["more"] is True


# ── Catalog targets ───────────────────────────────────────────────────────────

class FakeTargets:
    def __init__(self, n=0, fail_at=None, exc=None):
        self.n, self.fail_at, self.exc, self.bodies = n, fail_at, exc, []

    async def _async_get_catalog_targets(self, integ_connector_guid, output_format="JSON", report_spec=None, body=None, **kw):
        self.bodies.append(dict(body or {}))
        if self.fail_at is not None and len(self.bodies) > self.fail_at:
            raise self.exc
        s, size = body["startFrom"], body["pageSize"]
        return [{"elementHeader": {"guid": f"t{i}", "type": {"typeName": "Asset"}}, "properties": {"displayName": f"T{i}"},
                 "relatedBy": {"relationshipProperties": {"catalogTargetName": f"n{i}"}}}
                for i in range(s, min(s + size, self.n))]


def _read(fake, **kw):
    return asyncio.run(ops._read_catalog_targets(fake, "conn-guid", **kw))


def test_catalog_targets_page_in_the_body_at_depth_0_until_empty():
    fake = FakeTargets(n=450)
    r = _read(fake)
    assert r["complete"] is True and len(r["targets"]) == 450 and r["error"] is None
    assert [b["startFrom"] for b in fake.bodies] == [0, 200, 400, 450]
    assert all(b["graphQueryDepth"] == 0 and b["pageSize"] == 200 for b in fake.bodies)


def test_catalog_target_timeout_is_an_explicit_unknown_not_none():
    fake = FakeTargets(n=10, fail_at=0, exc=asyncio.TimeoutError())
    r = _read(fake)
    assert r["targets"] is None and r["complete"] is False
    assert r["error"].startswith("could not be read: timed out")


def test_catalog_target_error_after_some_rows_is_a_lower_bound():
    fake = FakeTargets(n=1000, fail_at=1, exc=RuntimeError("boom"))
    r = _read(fake)
    assert len(r["targets"]) == 200 and r["complete"] is False and r["stoppedBy"] == "error"


def test_catalog_target_cap():
    r = _read(FakeTargets(n=5000), cap=400)
    assert len(r["targets"]) == 400 and r["complete"] is False and r["stoppedBy"] == "cap"


def test_connectors_endpoint_says_unknown_for_a_timed_out_connector(api, monkeypatch):
    report = {"integrationConnectorReports": [
        {"connectorName": "Slow", "connectorGUID": "g-slow"},
        {"connectorName": "Fine", "connectorGUID": "g-fine"}]}

    async def fake_rm(*a, **k):
        return object()

    class AC:
        async def _async_get_catalog_targets(self, integ_connector_guid, body=None, **kw):
            if integ_connector_guid == "g-slow":
                raise asyncio.TimeoutError()
            return [] if body["startFrom"] else [{"elementHeader": {"guid": "x"}, "properties": {}}]

    async def fake_ac(*a, **k):
        return AC()
    monkeypatch.setattr(ops, "_runtime_manager_async", fake_rm)
    monkeypatch.setattr(ops, "_automated_curation_async", fake_ac)
    monkeypatch.setattr(ops, "_get_server_report_cached", lambda rm, g, k: (report, False, False))
    monkeypatch.setattr(ops, "_report_element", lambda raw: raw)
    rows = {r["connectorName"]: r for r in api.get("/api/operations/integration-connectors?server_guid=s").json()["connectors"]}
    slow, fine = rows["Slow"], rows["Fine"]
    assert slow["catalogTargetCount"] is None and slow["catalogTargetsError"].startswith("could not be read")
    assert fine["catalogTargetCount"] == 1 and fine["catalogTargetsComplete"] is True and fine["catalogTargetsError"] is None
