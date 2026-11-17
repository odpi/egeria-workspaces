# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Data Lens: matching a resource's DataScope to a lens, and the
create / change / govern-a-list endpoints.

Matching rules pinned here: only dimensions both record are compared; a period or bound
overlaps when the intervals meet (an open end is unbounded); scope elements match when
they share an element; and a resource that records none of the lens's dimensions is
"unknown", never "outside". The endpoints run through the real app with fake Egeria
clients, so nothing is written to Egeria.
"""
import base64
import json
import time

import pytest

import data_scope_handler as ds
import resource_browser_handler as rb
import resource_locator_lens_handler as lens
from test_data_scope import _DATA_SCOPE_63


def _jwt(sub="peter"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + 3600})}.sig"


_GROUPS = ds._dimensions(_DATA_SCOPE_63)   # DataLens carries the same dimensions as DataScope in 6.3
_LENS_2024_UK = {"dataCoverageStartTime": "2024-01-01T00:00:00Z", "dataCoverageEndTime": "2024-12-31T00:00:00Z",
                 "minLatitude": 49.9, "maxLatitude": 58.7, "minLongitude": -8.2, "maxLongitude": 1.8}


# ── Matching ─────────────────────────────────────────────────────────────────

def test_scope_dims_reads_periods_bounds_and_elements_by_shape():
    d = lens._scope_dims({"dataCollectionStartTime": "2024-01-01T00:00:00Z", "dataValidityEndTime": "2025-01-01T00:00:00Z",
                          "minLatitude": 0, "maxLatitude": 0, "minDepth": 10.0, "scopeElements": {"Location": "loc-1"},
                          "additionalProperties": {"readCount": "7"}})
    assert set(d["periods"]) == {"dataCollection", "dataValidity"}
    assert d["periods"]["dataValidity"][0] is None
    assert d["bounds"] == {"Depth": (10.0, None)}          # all-zero latitude is "never set"
    assert d["elements"] == {"Location": "loc-1"}


@pytest.mark.parametrize("scope, outcome", [
    ({"dataCoverageStartTime": "2024-06-01T00:00:00Z", "dataCoverageEndTime": "2025-06-01T00:00:00Z"}, "inside"),
    ({"dataCoverageStartTime": "2023-01-01T00:00:00Z", "dataCoverageEndTime": "2023-12-01T00:00:00Z"}, "outside"),
    ({"dataCoverageEndTime": "2024-02-01T00:00:00Z"}, "inside"),                           # open start
    ({"minLatitude": 51.3, "maxLatitude": 51.7, "minLongitude": -0.5, "maxLongitude": 0.3}, "inside"),  # London
    ({"minLatitude": 40.5, "maxLatitude": 40.9, "minLongitude": -74.3, "maxLongitude": -73.7}, "outside"),  # New York
    ({"dataCoverageStartTime": "2024-06-01T00:00:00Z", "minLatitude": 40.5, "maxLatitude": 40.9}, "outside"),
    ({"dataCollectionStartTime": "2024-06-01T00:00:00Z"}, "unknown"),     # a dimension the lens does not use
    ({"additionalProperties": {"readCount": "7"}}, "unknown"),           # usage readings only
    (None, "unknown"),
])
def test_lens_match(scope, outcome):
    assert lens._lens_match(_LENS_2024_UK, scope)["outcome"] == outcome


def test_scope_elements_match_when_they_share_an_element():
    l = {"scopeElements": {"Location": "uk", "Team": "sales"}}
    assert lens._lens_match(l, {"scopeElements": {"Region": "uk"}})["outcome"] == "inside"
    assert lens._lens_match(l, {"scopeElements": {"Region": "fr"}})["outcome"] == "outside"


def test_lens_record_is_editable_only_by_its_creator_and_lists_what_it_governs():
    el = {"elementHeader": {"guid": "L", "type": {"typeName": "DataLens", "superTypeNames": ["GovernanceControl"]},
                            "versions": {"createdBy": "peter"}},
          "properties": {"qualifiedName": "DataLens::portal::peter::uk-2024-abc123", "displayName": "UK 2024",
                         "summary": "s", **_LENS_2024_UK},
          "governedElements": [{"relatedElement": {"elementHeader": {"guid": "W", "type": {"typeName": "WorkingSet"}},
                                                   "properties": {"displayName": "My list"}},
                                "relationshipHeader": {"type": {"typeName": "GovernedBy"}}}]}
    mine = lens._lens_record(el, "peter", _GROUPS)
    assert mine["editable"] and mine["governs"] == [{"guid": "W", "displayName": "My list", "typeName": "WorkingSet"}]
    assert mine["scope"] == _LENS_2024_UK and "summary" not in mine["scope"]
    assert mine["dimensions"] == ["Latitude", "Longitude", "dataCoverage"]
    assert lens._lens_record(el, "erin", _GROUPS)["editable"] is False


# ── Endpoints, with fake Egeria ──────────────────────────────────────────────

class _FakeOfficer:
    def __init__(self):
        self.calls = []

    async def _async_create_data_lens(self, body):
        self.calls.append(("create", body))
        return "L-new"

    async def _async_update_governance_definition(self, guid, body):
        self.calls.append(("update", guid, body))

    async def _async_attach_governed_by_definition(self, element_guid, definition_guid, body=None):
        self.calls.append(("govern", element_guid, definition_guid))

    async def _async_detach_governed_by_definition(self, element_guid, definition_guid, body=None):
        self.calls.append(("ungovern", element_guid, definition_guid))


class _FakeExplorer:
    def __init__(self, owner="peter"):
        self.owner = owner

    async def _async_get_element_by_guid(self, guid, **kw):
        return {"elementHeader": {"guid": guid, "type": {"typeName": "DataLens", "superTypeNames": ["GovernanceControl"]},
                                  "versions": {"createdBy": self.owner}},
                "properties": {"qualifiedName": f"DataLens::portal::{self.owner}::x-1", "displayName": "UK 2024",
                               "importance": "high", **_LENS_2024_UK}}


@pytest.fixture
def fake(monkeypatch):
    officer = _FakeOfficer()
    state = {"explorer": _FakeExplorer(), "lists": []}

    async def groups(_t):
        return _GROUPS, time.time()

    async def explorer():
        return state["explorer"]

    async def off():
        return officer

    async def my_list(_client, guid):
        state["lists"].append(guid)
        if guid == "not-mine":
            raise rb.HTTPException(status_code=403, detail="Only the person who made a list can change it.")
        return {}, {"guid": guid}

    def row(guid, scope):
        return {"guid": guid, "kind": "table", "displayName": guid, "dataScope": scope, "matched": []}

    async def scoped():
        return {"rows": [row("london", {"minLatitude": 51.3, "maxLatitude": 51.7}),
                         row("nyc", {"minLatitude": 40.5, "maxLatitude": 40.9}),
                         row("usage", {"additionalProperties": {"readCount": "3"}})], "capped": False}, \
            rb.datetime.now(rb.timezone.utc)

    monkeypatch.setattr(ds, "_type_groups", groups)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_my_list", my_list)
    monkeypatch.setattr(lens, "_officer_async", off)
    monkeypatch.setattr(lens, "_scoped_rows", scoped)
    return officer, state


def test_lens_page_lists_what_is_inside_and_counts_the_rest(client, fake):
    d = client.get("/api/resource-browser/lenses/L1").json()
    assert [r["guid"] for r in d["inside"]] == ["london"]
    assert (d["insideCount"], d["outsideCount"], d["notComparable"]) == (1, 1, 1)
    assert d["inside"][0]["matched"] == ["inside on Latitude"]


def test_create_needs_a_signed_in_token(client, fake):
    officer, _ = fake
    assert client.post("/api/resource-browser/lenses", json={"name": "UK"}).status_code == 401
    assert officer.calls == []


def test_create_names_it_for_its_creator_and_governs_the_list(client, fake):
    officer, state = fake
    r = client.post("/api/resource-browser/lenses", headers={"X-Egeria-Token": _jwt()},
                    json={"name": "UK 2024", "description": "sales", "listGuid": "W1",
                          "values": {"dataCoverageStartTime": "2024-01-01", "minLatitude": "49.9", "maxLatitude": "58.7"}})
    assert r.status_code == 200, r.text
    kind, body = officer.calls[0]
    props = body["properties"]
    assert kind == "create" and props["class"] == "DataLensProperties"
    assert props["qualifiedName"].startswith("DataLens::portal::peter::uk-2024-")
    assert props["dataCoverageStartTime"] == "2024-01-01T00:00:00Z" and props["minLatitude"] == 49.9
    assert officer.calls[1] == ("govern", "W1", "L-new") and state["lists"] == ["W1"]


def test_create_refuses_bad_values_and_lists_that_are_not_yours(client, fake):
    officer, _ = fake
    h = {"X-Egeria-Token": _jwt()}
    r = client.post("/api/resource-browser/lenses", headers=h, json={"name": "x", "values": {"maxLatitude": 99}})
    assert r.status_code == 422
    r = client.post("/api/resource-browser/lenses", headers=h, json={"name": "x", "listGuid": "not-mine"})
    assert r.status_code == 403
    assert client.post("/api/resource-browser/lenses", headers=h, json={"name": "  "}).status_code == 400
    assert officer.calls == []


def test_edit_replaces_the_dimensions_and_keeps_other_properties(client, fake):
    officer, _ = fake
    r = client.put("/api/resource-browser/lenses/L1", headers={"X-Egeria-Token": _jwt()},
                   json={"values": {"minLatitude": "50", "maxLatitude": "55"}})
    assert r.status_code == 200, r.text
    kind, guid, body = officer.calls[0]
    props = body["properties"]
    assert (kind, guid, body["mergeUpdate"]) == ("update", "L1", False)
    assert props["minLatitude"] == 50.0 and "dataCoverageStartTime" not in props and "minLongitude" not in props
    assert props["importance"] == "high" and props["displayName"] == "UK 2024"


def test_only_the_creator_changes_a_lens(client, fake):
    officer, state = fake
    state["explorer"] = _FakeExplorer(owner="erin")
    h = {"X-Egeria-Token": _jwt("peter")}
    assert client.put("/api/resource-browser/lenses/L1", headers=h, json={"name": "mine now"}).status_code == 403
    assert client.post("/api/resource-browser/lenses/L1/lists", headers=h, json={"listGuid": "W1"}).status_code == 403
    assert client.delete("/api/resource-browser/lenses/L1/lists/W1", headers=h).status_code == 403
    assert officer.calls == []


def test_govern_and_ungovern_a_list(client, fake):
    officer, _ = fake
    h = {"X-Egeria-Token": _jwt()}
    assert client.post("/api/resource-browser/lenses/L1/lists", headers=h, json={"listGuid": "W2"}).status_code == 200
    assert client.delete("/api/resource-browser/lenses/L1/lists/W2", headers=h).status_code == 200
    assert officer.calls == [("govern", "W2", "L1"), ("ungovern", "W2", "L1")]
