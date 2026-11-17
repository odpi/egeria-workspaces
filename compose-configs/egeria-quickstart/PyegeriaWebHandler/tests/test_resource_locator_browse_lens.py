# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Browse: filter a list by a Data Lens, and the Data scope facet's
"recorded" / "none recorded" values (design note DESIGN-RL-BROWSE-LENS-AND-SCOPE-FILTER,
Architect read-back R1-R4, 2026-11-17).

Pinned here:
  - each row is inside / outside / cannot be compared / scope not read; "cannot be compared"
    is never counted as outside, and a row whose header carried no classifications is
    "scope not read" (R1), never "cannot be compared" or "none recorded";
  - counts say partial when the list was capped; "none recorded" is complete for what the user
    can see (R2, explained as visibility since), so it is "at least" only when a read was capped;
  - the old value id "all" answers with the old shape: value "all", title "Resources with a
    data scope" (R3).
Endpoints run through the real app with fake Egeria clients; nothing is written.
"""
import base64
import json
import time

import pytest

import data_scope_handler as ds
import resource_browser_handler as rb
import resource_locator_lens_handler as lh
from test_data_scope import _DATA_SCOPE_63

_GROUPS = ds._dimensions(_DATA_SCOPE_63)
_TABLE = ["SchemaAttribute", "SchemaElement", "Referenceable"]
_READINGS = {"analysisService": "open-lineage-data-scope-governance-service", "readCount": "7"}


def _jwt(sub="peter"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + 3600})}.sig"


def _cls(name, props=None):
    return {"class": "ElementClassification", "classificationName": name,
            "classificationProperties": {"class": name + "Properties", **(props or {})}}


def _el(guid, scope=None, read=True, type_name="RelationalTable"):
    """A resource element. read=False leaves the header without any classification entries,
    the shape of a header that was not read with its classifications."""
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": _TABLE}, "versions": {}}
    if read:
        hdr["anchor"] = _cls("Anchors", {"anchorGUID": guid})
        if scope is not None:
            hdr["dataScope"] = _cls("DataScope", scope)
    return {"elementHeader": hdr, "properties": {"displayName": guid, "qualifiedName": "qn::" + guid}}


_LENS = {"minLatitude": 49.9, "maxLatitude": 58.7}


# ── Pure helpers ─────────────────────────────────────────────────────────────

def test_a_header_without_classifications_is_not_read():
    assert rb._row(_el("a", read=True))["scopeRead"] is True
    assert rb._row(_el("b", read=False))["scopeRead"] is False


def test_lens_outcome_maps_unknown_to_cannot_be_compared_and_unread_apart():
    row = lambda el: rb._row(el)
    assert rb._lens_outcome(_LENS, row(_el("in", {"minLatitude": 51.0, "maxLatitude": 52.0})), lh._lens_match)["outcome"] == "inside"
    assert rb._lens_outcome(_LENS, row(_el("out", {"minLatitude": 40.0, "maxLatitude": 41.0})), lh._lens_match)["outcome"] == "outside"
    assert rb._lens_outcome(_LENS, row(_el("time", {"dataCoverageStartTime": "2024-01-01T00:00:00Z"})), lh._lens_match)["outcome"] == "notComparable"
    assert rb._lens_outcome(_LENS, row(_el("none")), lh._lens_match)["outcome"] == "notComparable"
    assert rb._lens_outcome(_LENS, row(_el("unread", read=False)), lh._lens_match)["outcome"] == "notRead"


# ── Endpoints, with fake Egeria ──────────────────────────────────────────────

class _Explorer:
    def __init__(self, lens_owner="peter"):
        self.lens_owner = lens_owner

    async def _async_get_element_by_guid(self, guid, **kw):
        return {"elementHeader": {"guid": guid, "type": {"typeName": "DataLens", "superTypeNames": ["GovernanceControl"]},
                                  "versions": {"createdBy": self.lens_owner}},
                "properties": {"qualifiedName": f"DataLens::portal::{self.lens_owner}::uk", "displayName": "UK", **_LENS}}


@pytest.fixture
def fake(monkeypatch):
    state = {"scoped": [], "all": {}, "capped": False, "all_capped": []}

    async def explorer():
        return _Explorer()

    async def groups(_t):
        return _GROUPS, time.time()

    async def classified(_client, name):
        assert name == "DataScope"
        return state["scoped"], state["capped"]

    async def all_elements(_client, type_name, *a, **kw):
        return state["all"].get(type_name, []), type_name in state["all_capped"]

    async def cached(name, producer, ttl=600):
        return await producer(), rb.datetime.now(rb.timezone.utc)

    async def repos():
        return []

    def sweep_done():          # the endpoint tests see a finished background sweep (its own tests are below)
        return state.get("sweep_value"), rb.datetime.now(rb.timezone.utc), state.get("sweep_loading", False), None

    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_all_resources_state", sweep_done)
    monkeypatch.setattr(rb, "_classified", classified)
    monkeypatch.setattr(rb, "_all_elements", all_elements)
    monkeypatch.setattr(rb, "_cached", cached)
    monkeypatch.setattr(rb, "_repos_value", repos)
    monkeypatch.setattr(ds, "_type_groups", groups)
    return state


def _scoped_state(state):
    state["scoped"] = [_el("london", {"minLatitude": 51.3, "maxLatitude": 51.7}),
                       _el("nyc", {"minLatitude": 40.5, "maxLatitude": 40.9}),
                       _el("collected", {"dataCollectionStartTime": "2024-01-01T00:00:00Z"}),
                       _el("usage", {"additionalProperties": _READINGS})]
    state["all"] = {"DataAsset": state["scoped"] + [_el("bare"), _el("unread", read=False)]}
    rows = {}
    for r in rb._rows(state["all"]["DataAsset"])[0]:
        rows.setdefault(r["guid"], r)
    state["sweep_value"] = {"rows": list(rows.values()), "cappedTypes": []}


def test_browse_list_with_a_lens_marks_every_row_and_counts_the_whole_list(client, fake):
    _scoped_state(fake)
    d = client.get("/api/resource-browser/browse/scope/recorded?lens=L1", headers={"X-Egeria-Token": _jwt()}).json()
    out = {r["guid"]: r["lensOutcome"]["outcome"] for r in d["items"]}
    assert out == {"london": "inside", "nyc": "outside", "collected": "notComparable"}
    assert d["lensCounts"] == {"inside": 1, "outside": 1, "notComparable": 1, "notRead": 0, "partial": False}
    assert d["lens"] == {"guid": "L1", "displayName": "UK", "dimensions": ["Latitude"]}


def test_lens_counts_are_partial_when_the_list_was_capped(client, fake):
    _scoped_state(fake)
    fake["capped"] = True
    d = client.get("/api/resource-browser/browse/scope/recorded?lens=L1", headers={"X-Egeria-Token": _jwt()}).json()
    assert d["capped"] is True and d["lensCounts"]["partial"] is True


def test_without_a_lens_the_response_is_as_before(client, fake):
    _scoped_state(fake)
    d = client.get("/api/resource-browser/browse/scope/recorded").json()
    assert "lensCounts" not in d and all("lensOutcome" not in r for r in d["items"])


def test_old_value_all_keeps_its_shape(client, fake):
    _scoped_state(fake)
    old = client.get("/api/resource-browser/browse/scope/all").json()
    assert (old["value"], old["title"]) == ("all", "Resources with a data scope")
    assert sorted(r["guid"] for r in old["items"]) == ["collected", "london", "nyc"]
    new = client.get("/api/resource-browser/browse/scope/recorded").json()
    assert [r["guid"] for r in old["items"]] == [r["guid"] for r in new["items"]]


def test_none_recorded_is_every_resource_minus_recorded_with_unread_apart(client, fake):
    _scoped_state(fake)
    d = client.get("/api/resource-browser/browse/scope/none").json()
    assert sorted(r["guid"] for r in d["items"]) == ["bare", "usage"]      # usage-only readings need a scope too
    assert "1 more could not be checked" in d["note"]                      # "unread" is neither none nor recorded
    assert d["capped"] is False and "you can see" in d["note"]            # complete for what this user sees
    assert set(d["scopeListsAsOf"]) == {"recordedAsOf", "noneAsOf"}


def test_scope_facet_values_count_both_lists(client, fake):
    _scoped_state(fake)
    d = client.get("/api/resource-browser/browse/scope").json()
    vals = {v["id"]: v for v in d["values"]}
    assert (vals["recorded"]["count"], vals["none"]["count"]) == (3, 2)
    assert vals["none"]["countAtLeast"] is False and d["notRead"] == 1
    assert "you can see" in vals["none"]["description"]


def test_unknown_scope_value_is_404(client, fake):
    assert client.get("/api/resource-browser/browse/scope/everything").status_code == 404


def test_while_counting_none_is_never_zero(client, fake):
    _scoped_state(fake)
    fake["sweep_value"], fake["sweep_loading"] = None, True
    vals = {v["id"]: v for v in client.get("/api/resource-browser/browse/scope").json()["values"]}
    assert vals["none"]["count"] is None and vals["none"]["counting"] is True
    assert vals["recorded"]["count"] == 3
    d = client.get("/api/resource-browser/browse/scope/none").json()
    assert d["loading"] is True and d["items"] == [] and "Counting every resource" in d["note"]


# ── The background sweep itself (Architect public-demo condition) ───────────

def _sweep_harness(monkeypatch, fail_first=False):
    import asyncio
    calls = {"n": 0, "running": 0, "peak": 0}
    gate = {}

    async def sweep():
        calls["n"] += 1
        calls["running"] += 1
        calls["peak"] = max(calls["peak"], calls["running"])
        try:
            await gate["release"].wait()
            if fail_first and calls["n"] == 1:
                raise RuntimeError("egeria down")
            return {"rows": [], "cappedTypes": []}
        finally:
            calls["running"] -= 1

    monkeypatch.setattr(rb, "_all_resources_sweep", sweep)
    monkeypatch.setattr(rb, "_SWEEP_STATE", {})
    monkeypatch.setattr(rb, "_sweep_key", lambda: "k|user")
    return calls, gate


def test_concurrent_requests_start_one_background_sweep_and_never_wait(monkeypatch):
    import asyncio
    calls, gate = _sweep_harness(monkeypatch)

    async def main():
        gate["release"] = asyncio.Event()
        rb._ALL_RESOURCES_SWEEPS = asyncio.Semaphore(1)
        first = [rb._all_resources_state() for _ in range(5)]          # five requests, nothing awaited
        await asyncio.sleep(0)
        assert all(v is None and loading for v, _s, loading, _e in first)
        gate["release"].set()
        for _ in range(5):
            await asyncio.sleep(0)
        return rb._all_resources_state()
    value, stamp, loading, error = asyncio.run(main())
    assert calls["n"] == 1 and calls["peak"] == 1
    assert value == {"rows": [], "cappedTypes": []} and stamp is not None and loading is False and error is None


def test_a_failed_sweep_is_reported_and_retried_only_after_a_pause(monkeypatch):
    # Architect R8: while Egeria is down, 8 s polls must not start a new 19 s sweep each time.
    import asyncio
    calls, gate = _sweep_harness(monkeypatch, fail_first=True)
    clock = {"t": 1000.0}
    monkeypatch.setattr(rb, "_sweep_clock", lambda: clock["t"])

    async def settle():
        for _ in range(5):
            await asyncio.sleep(0)

    async def main():
        gate["release"] = asyncio.Event()
        rb._ALL_RESOURCES_SWEEPS = asyncio.Semaphore(1)
        gate["release"].set()
        rb._all_resources_state()
        await settle()                                   # first sweep fails
        clock["t"] += 8
        polled = rb._all_resources_state()               # a poll 8 s later: no new sweep
        await settle()
        clock["t"] += rb._SWEEP_RETRY_S
        retry = rb._all_resources_state()                # after the pause: retried
        await settle()
        return polled, retry, rb._all_resources_state()
    polled, retry, done = asyncio.run(main())
    assert polled[0] is None and polled[2] is False and "egeria down" in polled[3]
    assert calls["n"] == 2
    assert retry[2] is True
    assert done[0] == {"rows": [], "cappedTypes": []} and done[3] is None


def test_idle_sweep_entries_are_evicted(monkeypatch):
    # Architect R7: one entry per credential, each holding thousands of rows; tokens rotate.
    import asyncio
    calls, gate = _sweep_harness(monkeypatch)
    clock = {"t": 0.0}
    monkeypatch.setattr(rb, "_sweep_clock", lambda: clock["t"])
    key = {"k": "k|old-token"}
    monkeypatch.setattr(rb, "_sweep_key", lambda: key["k"])

    async def main():
        gate["release"] = asyncio.Event()
        gate["release"].set()
        rb._ALL_RESOURCES_SWEEPS = asyncio.Semaphore(1)
        rb._all_resources_state()
        for _ in range(5):
            await asyncio.sleep(0)
        assert "k|old-token" in rb._SWEEP_STATE
        clock["t"] += rb._SWEEP_EVICT_S + 1
        key["k"] = "k|new-token"
        rb._all_resources_state()
        for _ in range(5):
            await asyncio.sleep(0)
    asyncio.run(main())
    assert "k|old-token" not in rb._SWEEP_STATE and "k|new-token" in rb._SWEEP_STATE


def test_none_recorded_is_at_least_only_when_a_type_read_was_capped(client, fake):
    _scoped_state(fake)
    fake["sweep_value"]["cappedTypes"] = ["DataAsset"]
    d = client.get("/api/resource-browser/browse/scope/none").json()
    assert d["capped"] is True
    vals = {v["id"]: v for v in client.get("/api/resource-browser/browse/scope").json()["values"]}
    assert vals["none"]["countAtLeast"] is True
