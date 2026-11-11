"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Classification purpose: _norm_cls_purpose, GET /api/types/classification-purposes
and the classificationPurpose field on /api/types classifications. The twin of
test_relationship_purpose.py.

Egeria is mocked, but the defs are real: fixtures/classification_defs_laz_2026_11_11.json
was captured read-only from the laz quickstart platform (see its _captured note).
"""

import json
from collections import Counter
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import type_system_handler as h

_FIXTURE = json.loads(
    (Path(__file__).resolve().parent / "fixtures" / "classification_defs_laz_2026_11_11.json").read_text()
)
# The verbatim defs, as pyegeria's _extract_typedef_list hands them back.
LAZ_DEFS = _FIXTURE["response"]["typeDefList"]["typeDefs"]
# Every classification def on laz: name -> classificationPurpose (None = absent).
LAZ_ALL = _FIXTURE["allPurposes"]


# ── What laz reports ──────────────────────────────────────────────────────────

def test_laz_reports_six_purposes_all_known():
    """Classifications have their own six purposes, not the eleven relationship
    ones, and every value laz sends is one the handler recognises."""
    seen = {v for v in LAZ_ALL.values() if v is not None}
    assert seen == set(h.CLS_PURPOSES)
    assert not seen & set(h.REL_PURPOSES)


def test_laz_counts():
    assert len(LAZ_ALL) == 94
    assert Counter(LAZ_ALL.values()) == {
        "CATEGORY": 46, "GOVERNANCE": 15, "GOVERNANCE_IMPLEMENTATION": 10,
        "MANAGEMENT": 10, "ANALYTICAL": 6, "DESCRIPTIVE": 6, None: 1,
    }
    assert [n for n, p in LAZ_ALL.items() if p is None] == ["ReviewedByClinicalTrials"]


def test_fixture_defs_are_real_shape():
    by_name = {d["name"]: d for d in LAZ_DEFS}
    assert by_name["Confidentiality"]["class"] == "OpenMetadataClassificationDef"
    assert by_name["Confidentiality"]["classificationPurpose"] == "GOVERNANCE"
    # The one unpurposed def omits the key entirely (not null).
    assert "classificationPurpose" not in by_name["ReviewedByClinicalTrials"]
    # Subtypes carry their own resolved value.
    assert by_name["PolicyEnforcementPoint"]["superType"]["name"] == "PolicyManagementPoint"
    assert by_name["PolicyEnforcementPoint"]["classificationPurpose"] == "GOVERNANCE_IMPLEMENTATION"


# ── _norm_cls_purpose ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("value, expected", [
    ("GOVERNANCE", "GOVERNANCE"),
    ("GOVERNANCE_IMPLEMENTATION", "GOVERNANCE_IMPLEMENTATION"),   # the wire format
    ("GovernanceImplementation", "GOVERNANCE_IMPLEMENTATION"),    # Egeria's display name
    ("Governance Implementation", "GOVERNANCE_IMPLEMENTATION"),
    ("category", "CATEGORY"),
    ({"name": "MANAGEMENT"}, "MANAGEMENT"),
    ({"displayName": "Analytical"}, "ANALYTICAL"),
    ({"ordinal": 5, "name": "Descriptive"}, "DESCRIPTIVE"),
])
def test_norm_cls_purpose_recognised(value, expected):
    assert h._norm_cls_purpose(value) == expected


@pytest.mark.parametrize("value", [
    None, "", "   ", {}, {"name": None}, "NOT_A_PURPOSE", 42, ["GOVERNANCE"],
    "STRUCTURAL", "ASSIGNMENT",     # relationship purposes are not classification purposes
])
def test_norm_cls_purpose_unknown_is_none(value):
    assert h._norm_cls_purpose(value) is None


def test_norm_cls_purpose_never_defaults_to_category():
    """CATEGORY is Egeria's enum default; absence must not become it."""
    assert h._norm_cls_purpose(None) is None
    assert h._norm_cls_purpose("garbage") is None


def test_rel_normaliser_does_not_accept_classification_purposes():
    assert h._norm_purpose("GOVERNANCE") is None


def test_norm_cls_purpose_warns_once_per_value(monkeypatch):
    warnings = []
    monkeypatch.setattr(h.logger, "warning", lambda msg, *a, **k: warnings.append(msg))
    monkeypatch.setattr(h, "_WARNED_CLS_PURPOSES", set())
    h._norm_cls_purpose("BOGUS_ONE")
    h._norm_cls_purpose("BOGUS_ONE")
    h._norm_cls_purpose("BOGUS_TWO")
    assert len(warnings) == 2


def test_cls_purpose_map_on_laz_defs():
    m = h._cls_purpose_map(LAZ_DEFS)
    assert m["serverReportsPurpose"] is True
    assert m["purposes"] == {
        "Anchors": "MANAGEMENT", "Confidentiality": "GOVERNANCE", "Memento": "MANAGEMENT",
        "PolicyEnforcementPoint": "GOVERNANCE_IMPLEMENTATION", "PrimaryKey": "DESCRIPTIVE",
        "ReviewedByClinicalTrials": None, "Taxonomy": "CATEGORY", "UsageActivity": "ANALYTICAL",
    }


def test_cls_purpose_map_older_server():
    """A server from before classification purposes: no def carries the key."""
    older = [{k: v for k, v in d.items() if k != "classificationPurpose"} for d in LAZ_DEFS]
    m = h._cls_purpose_map(older)
    assert m["serverReportsPurpose"] is False
    assert set(m["purposes"].values()) == {None}


# ── GET /api/types/classification-purposes ────────────────────────────────────

class _FakeClient:
    def __init__(self, state, calls):
        self._state = state
        self._calls = calls

    async def _async_get_all_classification_defs(self):
        self._calls.append("classification")
        return self._state["classification"]

    async def _async_get_all_relationship_defs(self):
        self._calls.append("relationship")
        return self._state["relationship"]

    async def _async_close_session(self):
        pass


@pytest.fixture
def purposes_client(monkeypatch):
    """(TestClient, state, calls) with Egeria mocked out."""
    state = {"classification": LAZ_DEFS, "relationship": []}
    calls: list[str] = []

    async def fake_get_client_async(url, server, user_id, user_pwd):
        return _FakeClient(state, calls)

    monkeypatch.setattr(h, "_get_client_async", fake_get_client_async)
    monkeypatch.setattr(h, "_egeria_token_from_request", lambda request: None)
    monkeypatch.setattr(h, "_PURPOSE_CACHE", {})
    monkeypatch.setattr(h, "_CLS_PURPOSE_CACHE", {})

    app = FastAPI()
    app.include_router(h.router)
    return TestClient(app), state, calls


_URL = "/api/types/classification-purposes?url=https://p:9443&server=vs"


def test_endpoint_returns_laz_purposes(purposes_client):
    client, _, calls = purposes_client
    r = client.get(_URL)
    assert r.status_code == 200
    body = r.json()
    assert body["serverReportsPurpose"] is True
    assert body["purposes"]["Confidentiality"] == "GOVERNANCE"
    assert body["purposes"]["ReviewedByClinicalTrials"] is None
    assert calls == ["classification"]          # never fetches relationship defs


def test_endpoint_cache_hit_and_expiry(purposes_client, monkeypatch):
    client, state, calls = purposes_client
    first = client.get(_URL).json()
    state["classification"] = [{"name": "Changed", "classificationPurpose": "CATEGORY"}]
    assert client.get(_URL).json() == first
    assert len(calls) == 1
    now = h.time.monotonic()
    monkeypatch.setattr(h.time, "monotonic", lambda: now + h._PURPOSE_TTL + 1)
    assert client.get(_URL).json()["purposes"] == {"Changed": "CATEGORY"}
    assert len(calls) == 2


def test_endpoint_cache_is_per_server_and_separate_from_relationships(purposes_client):
    client, state, calls = purposes_client
    state["relationship"] = [{"name": "DataFlow", "relationshipPurpose": "DESIGN_LINEAGE"}]
    client.get(_URL)
    client.get("/api/types/classification-purposes?url=https://p:9443&server=other")
    rel = client.get("/api/types/relationship-purposes?url=https://p:9443&server=vs").json()
    assert calls == ["classification", "classification", "relationship"]
    assert rel["purposes"] == {"DataFlow": "DESIGN_LINEAGE"}


def test_endpoint_server_without_purposes(purposes_client):
    client, state, _ = purposes_client
    state["classification"] = [{"name": "Confidentiality"}, {"name": "Anchors"}]
    assert client.get(_URL).json() == {
        "purposes": {"Confidentiality": None, "Anchors": None},
        "serverReportsPurpose": False,
    }


def test_endpoint_no_defs(purposes_client):
    """pyegeria returns a 'No elements found' string when the list is empty."""
    client, state, _ = purposes_client
    state["classification"] = "No elements found"
    assert client.get(_URL).json() == {"purposes": {}, "serverReportsPurpose": False}


def test_endpoint_error_is_not_cached(purposes_client, monkeypatch):
    client, _, _ = purposes_client

    async def boom(url, server, user_id, user_pwd):
        raise RuntimeError("platform down")

    monkeypatch.setattr(h, "_get_client_async", boom)
    assert client.get(_URL).status_code == 500
    assert h._CLS_PURPOSE_CACHE == {}


# ── /api/types carries classificationPurpose ─────────────────────────────────

class _FullClient:
    def get_all_entity_defs(self):
        return [{"name": "Referenceable"}]

    def get_all_relationship_defs(self):
        return [{"name": "DataFlow", "relationshipPurpose": "DESIGN_LINEAGE"}]

    def get_all_classification_defs(self):
        return LAZ_DEFS

    def close_session(self):
        pass


def test_api_types_classifications_carry_purpose(monkeypatch):
    async def fake_get_client_async(url, server, user_id, user_pwd):
        return _FullClient()

    monkeypatch.setattr(h, "_get_client_async", fake_get_client_async)
    monkeypatch.setattr(h, "_egeria_token_from_request", lambda request: None)
    monkeypatch.setattr(h, "_PURPOSE_CACHE", {})
    monkeypatch.setattr(h, "_CLS_PURPOSE_CACHE", {})
    app = FastAPI()
    app.include_router(h.router)
    body = TestClient(app).get("/api/types?url=https://p:9443&server=vs").json()
    cls = body["classifications"]
    assert cls["Confidentiality"]["classificationPurpose"] == "GOVERNANCE"
    assert cls["Taxonomy"]["classificationPurpose"] == "CATEGORY"
    assert cls["ReviewedByClinicalTrials"]["classificationPurpose"] is None
    assert body["relationships"]["DataFlow"]["relationshipPurpose"] == "DESIGN_LINEAGE"
    # /api/types primes the map cache, so the lighter endpoint needs no second fetch.
    assert h._CLS_PURPOSE_CACHE["https://p:9443|vs"][1]["purposes"]["Anchors"] == "MANAGEMENT"
