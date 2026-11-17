# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Data Scope: dimensions read from Egeria's type definition, and the set/change/clear
endpoints The Catalog uses.

The attribute list below is the DataScope type definition as Egeria 6.3 returns it
(ValidMetadataManager.get_typedef_by_name, captured 2026-11-16 on laz). The endpoints run
through the real FastAPI app with a fake ClassificationExplorer, so nothing is written to
Egeria. They pin three rules:
  - a dimension Egeria adds is grouped by its shape with no change here;
  - every write keeps additionalProperties, which Egeria's lineage service fills with
    read counts;
  - writes need a signed-in token.
"""
import base64
import json
import time

import pytest

import data_scope_handler as ds


def _attr(name, type_name, desc=""):
    return {"attributeName": name, "attributeType": {"name": type_name}, "attributeDescription": desc}


_DATA_SCOPE_63 = [
    _attr("dataCollectionEndTime", "date"), _attr("dataValidityStartTime", "date"),
    _attr("dataValidityEndTime", "date"), _attr("dataCollectionStartTime", "date"),
    _attr("dataCoverageEndTime", "date"), _attr("dataCoverageStartTime", "date"),
    _attr("minHeight", "float"), _attr("maxLongitude", "float"), _attr("minLatitude", "float"),
    _attr("maxHeight", "float"), _attr("additionalProperties", "map<string,string>"),
    _attr("minLongitude", "float"), _attr("maxLatitude", "float"),
    _attr("scopeElements", "map<string,string>", "Map from name to guid"),
]
_READINGS = {"analysisService": "open-lineage-data-scope-governance-service", "readCount": "7"}


def _jwt(sub="peter"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + 3600})}.sig"


# ── Dimensions ───────────────────────────────────────────────────────────────

def test_dimensions_group_by_shape_in_a_stable_order():
    groups = ds._dimensions(_DATA_SCOPE_63)
    assert [(g["id"], g["shape"]) for g in groups] == [
        ("dataCollection", "timeRange"), ("dataValidity", "timeRange"), ("dataCoverage", "timeRange"),
        ("Latitude", "bound"), ("Longitude", "bound"), ("Height", "bound"),
        ("scopeElements", "map"), ("additionalProperties", "map")]
    coll = groups[0]
    assert [(f["name"], f["role"]) for f in coll["fields"]] == [
        ("dataCollectionStartTime", "start"), ("dataCollectionEndTime", "end")]
    assert groups[3]["range"] == [-90.0, 90.0] and "range" not in groups[5]
    assert groups[-1]["readOnly"] is True and not groups[-2].get("readOnly")


def test_a_dimension_egeria_adds_later_appears_without_a_change_here():
    groups = ds._dimensions(_DATA_SCOPE_63 + [
        _attr("dataRetentionStartTime", "date"), _attr("dataRetentionEndTime", "date"),
        _attr("minDepth", "float"), _attr("maxDepth", "float"), _attr("subjectArea", "string")])
    by = {g["id"]: g for g in groups}
    assert by["dataRetention"]["shape"] == "timeRange" and by["dataRetention"]["label"] == "Data retention"
    assert by["Depth"]["shape"] == "bound"
    assert by["subjectArea"]["shape"] == "field" and by["subjectArea"]["fields"][0]["kind"] == "string"


def test_an_unpaired_start_time_is_a_field_of_its_own():
    groups = ds._dimensions([_attr("dataLoadStartTime", "date"), _attr("minWidth", "float")])
    assert [(g["id"], g["shape"]) for g in groups] == [("dataLoadStartTime", "field"), ("minWidth", "field")]


# ── Values ───────────────────────────────────────────────────────────────────

def test_values_are_converted_and_empties_dropped():
    groups = ds._dimensions(_DATA_SCOPE_63)
    props, problems = ds._clean_values({
        "dataCollectionStartTime": "2024-01-01", "dataCollectionEndTime": "2024-06-30T12:30",
        "minLatitude": "51.2", "maxLatitude": 52, "minHeight": "", "scopeElements": {"Location": "g-1", "": "x"},
    }, groups)
    assert problems == []
    assert props == {"dataCollectionStartTime": "2024-01-01T00:00:00Z", "dataCollectionEndTime": "2024-06-30T12:30:00Z",
                     "minLatitude": 51.2, "maxLatitude": 52.0, "scopeElements": {"Location": "g-1"}}


@pytest.mark.parametrize("values, needle", [
    ({"dataCoverageStartTime": "2025-01-01", "dataCoverageEndTime": "2024-01-01"}, "start is after the end"),
    ({"minLongitude": 10, "maxLongitude": -10}, "minimum is after the maximum"),
    ({"maxLatitude": 91}, "between -90 and 90"),
    ({"additionalProperties": {"readCount": "0"}}, "kept as it is"),
    ({"colour": "blue"}, "not a dimension"),
    ({"minHeight": "high"}, "minHeight"),
])
def test_bad_values_are_problems_and_nothing_is_written(values, needle):
    _props, problems = ds._clean_values(values, ds._dimensions(_DATA_SCOPE_63))
    assert any(needle in p for p in problems), problems


def test_summary_tells_usage_readings_from_a_scope():
    groups = ds._dimensions(_DATA_SCOPE_63)
    assert ds._summary(None, groups) == {"present": False, "dimensions": [], "usageOnly": False}
    usage = ds._summary({"additionalProperties": _READINGS, "minLatitude": 0, "maxLatitude": 0}, groups)
    assert usage["usageOnly"] is True and usage["dimensions"] == []
    real = ds._summary({"dataCollectionStartTime": "2024-01-01T00:00:00Z", "additionalProperties": _READINGS}, groups)
    assert real["usageOnly"] is False and real["dimensions"] == ["dataCollection"]


def test_write_body_replaces_the_dimensions_and_keeps_the_readings():
    body = ds._write_body({"minLatitude": 1.0}, {"maxLatitude": 5.0, "additionalProperties": _READINGS},
                          "UpdateClassificationRequestBody", "DataScopeProperties")
    assert body == {"class": "UpdateClassificationRequestBody", "mergeUpdate": False,
                    "properties": {"class": "DataScopeProperties", "minLatitude": 1.0, "additionalProperties": _READINGS}}


# ── Endpoints, with a fake Egeria ────────────────────────────────────────────

class _FakeExplorer:
    def __init__(self, scope):
        self.scope, self.calls = scope, []

    async def _async_get_element_by_guid(self, guid, **kw):
        hdr = {"guid": guid, "type": {"typeName": "RelationalTable"},
               "versions": {"updatedBy": "peter", "updateTime": "2026-11-16T22:00:00Z"}}
        if self.scope is not None:
            hdr["dataScope"] = {"class": "ElementClassification", "classificationName": "DataScope",
                                "classificationProperties": {"class": "DataScopeProperties", **self.scope}}
        return {"elementHeader": hdr, "properties": {"displayName": "t"}}

    async def _async_add_data_scope(self, guid, body):
        self.calls.append(("add", body))
        self.scope = {k: v for k, v in body["properties"].items() if k != "class"}

    async def _async_update_data_scope(self, guid, body):
        self.calls.append(("update", body))
        self.scope = {k: v for k, v in body["properties"].items() if k != "class"}

    async def _async_clear_data_scope(self, guid, *a, **kw):
        self.calls.append(("clear", None))
        self.scope = None


@pytest.fixture
def fake(monkeypatch):
    box = {}

    def install(scope):
        box["client"] = _FakeExplorer(scope)

        async def explorer():
            return box["client"]

        async def groups(_type):
            return ds._dimensions(_DATA_SCOPE_63), time.time()
        monkeypatch.setattr(ds, "_explorer_async", explorer)
        monkeypatch.setattr(ds, "_type_groups", groups)
        return box["client"]
    return install


def test_dimensions_endpoint_rejects_other_types(client):
    assert client.get("/api/data-scope/dimensions?type=Asset").status_code == 400


def test_writes_need_a_signed_in_token(client, fake):
    c = fake(None)
    assert client.put("/api/data-scope/g1", json={"values": {"minLatitude": 1}}).status_code == 401
    assert client.delete("/api/data-scope/g1").status_code == 401
    assert c.calls == []


def test_put_adds_a_scope_where_there_is_none(client, fake):
    c = fake(None)
    r = client.put("/api/data-scope/g1", json={"values": {"minLatitude": "10", "maxLatitude": "20"}},
                   headers={"X-Egeria-Token": _jwt()})
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["action"] == "added" and c.calls[0][0] == "add"
    assert c.calls[0][1]["class"] == "NewClassificationRequestBody"
    assert d["scope"]["minLatitude"] == 10.0 and d["summary"]["dimensions"] == ["Latitude"]


def test_put_changes_a_scope_and_keeps_the_lineage_readings(client, fake):
    c = fake({"dataCollectionStartTime": "2020-01-01T00:00:00Z", "additionalProperties": _READINGS})
    r = client.put("/api/data-scope/g1", json={"values": {"dataCoverageStartTime": "2024-01-01", "dataCollectionStartTime": ""}},
                   headers={"X-Egeria-Token": _jwt()})
    assert r.status_code == 200, r.text
    kind, body = c.calls[0]
    assert kind == "update" and body["mergeUpdate"] is False
    # The emptied collection start is gone; the readings are carried across untouched.
    assert body["properties"] == {"class": "DataScopeProperties", "dataCoverageStartTime": "2024-01-01T00:00:00Z",
                                  "additionalProperties": _READINGS}


def test_put_with_a_problem_writes_nothing(client, fake):
    c = fake(None)
    r = client.put("/api/data-scope/g1", json={"values": {"maxLatitude": 120}}, headers={"X-Egeria-Token": _jwt()})
    assert r.status_code == 422 and "between -90 and 90" in r.json()["detail"]
    assert c.calls == []


def test_clear_keeps_the_readings_or_removes_the_classification(client, fake):
    c = fake({"minLatitude": 1.0, "maxLatitude": 2.0, "additionalProperties": _READINGS})
    d = client.delete("/api/data-scope/g1", headers={"X-Egeria-Token": _jwt()}).json()
    assert d["action"] == "cleared-kept-readings" and c.scope == {"additionalProperties": _READINGS}
    assert d["summary"]["usageOnly"] is True
    c = fake({"minLatitude": 1.0, "maxLatitude": 2.0})
    d = client.delete("/api/data-scope/g1", headers={"X-Egeria-Token": _jwt()}).json()
    assert d["action"] == "removed" and c.scope is None and c.calls == [("clear", None)]


# ── The Locator counts a scope only when it records a dimension ──────────────

def test_locator_has_scope_ignores_usage_readings_and_unset_bounds():
    import resource_browser_handler as rb
    assert rb._has_scope(None) is False
    assert rb._has_scope({"additionalProperties": _READINGS}) is False
    assert rb._has_scope({"minLatitude": 0, "maxLatitude": 0, "additionalProperties": _READINGS}) is False
    assert rb._has_scope({"dataCoverageStartTime": "2024-01-01T00:00:00Z"}) is True
    assert rb._has_scope({"minLatitude": 0, "maxLatitude": 51.5}) is True
    # A dimension Egeria adds later counts too.
    assert rb._has_scope({"subjectArea": "sales"}) is True
