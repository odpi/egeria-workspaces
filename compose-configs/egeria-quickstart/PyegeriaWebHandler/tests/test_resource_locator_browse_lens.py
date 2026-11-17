# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Browse: filter a list by a Data Lens, and the Data scope facet's
"recorded" / "none recorded" values (design note DESIGN-RL-BROWSE-LENS-AND-SCOPE-FILTER,
Architect read-back R1-R4, 2026-11-17).

Pinned here:
  - each row is inside / outside / cannot be compared / scope not read; "cannot be compared"
    is never counted as outside, and a row whose header carried no classifications is
    "scope not read" (R1), never "cannot be compared" or "none recorded";
  - counts say partial when the list was capped, and "none recorded" is "at least" until
    _all_elements is checked against the repository (R2);
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

    monkeypatch.setattr(rb, "_explorer_async", explorer)
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
    assert d["capped"] is True                                             # R2: at least, until cross-checked
    assert set(d["scopeListsAsOf"]) == {"recordedAsOf", "noneAsOf"}


def test_scope_facet_values_count_both_lists(client, fake):
    _scoped_state(fake)
    d = client.get("/api/resource-browser/browse/scope").json()
    vals = {v["id"]: v for v in d["values"]}
    assert (vals["recorded"]["count"], vals["none"]["count"]) == (3, 2)
    assert vals["none"]["countAtLeast"] is True and d["notRead"] == 1


def test_unknown_scope_value_is_404(client, fake):
    assert client.get("/api/resource-browser/browse/scope/everything").status_code == 404


def test_full_resource_sweeps_run_one_at_a_time(monkeypatch):
    # Architect R5: several users opening Data scope at once must not each sweep Egeria in parallel.
    import asyncio
    running, peak = {"n": 0}, {"n": 0}

    async def sweep():
        running["n"] += 1
        peak["n"] = max(peak["n"], running["n"])
        await asyncio.sleep(0.01)
        running["n"] -= 1
        return {"rows": [], "cappedTypes": []}

    async def cached(name, producer, ttl=600):          # a cache miss for every caller (different users)
        return await producer(), rb.datetime.now(rb.timezone.utc)

    async def classified(_c, _n):
        return [], False

    async def explorer():
        return None

    monkeypatch.setattr(rb, "_all_resources_sweep", sweep)
    monkeypatch.setattr(rb, "_cached", cached)
    monkeypatch.setattr(rb, "_classified", classified)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_ALL_RESOURCES_SWEEPS", None)

    async def main():
        rb._ALL_RESOURCES_SWEEPS = asyncio.Semaphore(1)  # bound to this test's loop
        await asyncio.gather(*(rb._scope_split() for _ in range(4)))
    asyncio.run(main())
    assert peak["n"] == 1
