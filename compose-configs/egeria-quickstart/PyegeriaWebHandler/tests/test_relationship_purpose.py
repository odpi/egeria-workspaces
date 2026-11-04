"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Relationship purpose (design-docs/relationship-purpose-plan.md, Phase 1):
_norm_purpose and GET /api/types/relationship-purposes. Egeria is mocked here,
so these run anywhere the handler imports (no live platform needed).
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import type_system_handler as h


# ── _norm_purpose ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("value, expected", [
    ("STRUCTURAL", "STRUCTURAL"),
    ("DESIGN_LINEAGE", "DESIGN_LINEAGE"),       # constant name (the observed wire format)
    ("DesignLineage", "DESIGN_LINEAGE"),        # display name
    ("Design Lineage", "DESIGN_LINEAGE"),
    ("assignment", "ASSIGNMENT"),
    ({"name": "PEER"}, "PEER"),                 # object shapes
    ({"displayName": "Activity"}, "ACTIVITY"),
    ({"ordinal": 5, "name": "Peer"}, "PEER"),
])
def test_norm_purpose_recognised(value, expected):
    assert h._norm_purpose(value) == expected


@pytest.mark.parametrize("value", [None, "", "   ", {}, {"name": None}, "NOT_A_PURPOSE", 42, ["PEER"]])
def test_norm_purpose_unknown_is_none(value):
    assert h._norm_purpose(value) is None


def test_norm_purpose_never_defaults_to_association():
    assert h._norm_purpose(None) != "ASSOCIATION"
    assert h._norm_purpose("garbage") != "ASSOCIATION"


def test_norm_purpose_warns_once_per_value(monkeypatch):
    warnings = []
    monkeypatch.setattr(h.logger, "warning", lambda msg, *a, **k: warnings.append(msg))
    monkeypatch.setattr(h, "_WARNED_PURPOSES", set())
    h._norm_purpose("BOGUS_ONE")
    h._norm_purpose("BOGUS_ONE")
    h._norm_purpose("BOGUS_TWO")
    assert len(warnings) == 2


def test_purpose_map_keeps_unpurposed_types_as_null():
    m = h._purpose_map([
        {"name": "SemanticAssignment", "relationshipPurpose": "ASSIGNMENT"},
        {"name": "BiopsySupportingEvidence"},
        {"relationshipPurpose": "PEER"},        # no name -> skipped
    ])
    assert m == {
        "purposes": {"SemanticAssignment": "ASSIGNMENT", "BiopsySupportingEvidence": None},
        "serverReportsPurpose": True,
    }


# ── GET /api/types/relationship-purposes ──────────────────────────────────────

class _FakeClient:
    def __init__(self, defs, calls):
        self._defs = defs
        self._calls = calls
        self.closed = False

    async def _async_get_all_relationship_defs(self):
        self._calls.append(1)
        return self._defs

    async def _async_close_session(self):
        self.closed = True


@pytest.fixture
def purposes_client(monkeypatch):
    """Returns (TestClient, set_defs, calls) with Egeria mocked out."""
    state = {"defs": []}
    calls: list[int] = []

    async def fake_get_client_async(url, server, user_id, user_pwd):
        return _FakeClient(state["defs"], calls)

    monkeypatch.setattr(h, "_get_client_async", fake_get_client_async)
    monkeypatch.setattr(h, "_egeria_token_from_request", lambda request: None)
    monkeypatch.setattr(h, "_PURPOSE_CACHE", {})

    app = FastAPI()
    app.include_router(h.router)

    def set_defs(defs):
        state["defs"] = defs

    return TestClient(app), set_defs, calls


_URL = "/api/types/relationship-purposes?url=https://p:9443&server=vs"


def test_endpoint_returns_purposes(purposes_client):
    client, set_defs, _ = purposes_client
    set_defs([
        {"name": "AssetSchemaType", "relationshipPurpose": "STRUCTURAL"},
        {"name": "DataFlow", "relationshipPurpose": "DESIGN_LINEAGE"},
        {"name": "BiopsySupportingEvidence"},
    ])
    r = client.get(_URL)
    assert r.status_code == 200
    assert r.json() == {
        "purposes": {
            "AssetSchemaType": "STRUCTURAL",
            "DataFlow": "DESIGN_LINEAGE",
            "BiopsySupportingEvidence": None,
        },
        "serverReportsPurpose": True,
    }


def test_endpoint_cache_hit_skips_egeria(purposes_client):
    client, set_defs, calls = purposes_client
    set_defs([{"name": "MoreInformation", "relationshipPurpose": "ASSIGNMENT"}])
    first = client.get(_URL).json()
    set_defs([{"name": "Changed", "relationshipPurpose": "PEER"}])
    second = client.get(_URL).json()
    assert len(calls) == 1
    assert second == first


def test_endpoint_cache_is_per_server(purposes_client):
    client, set_defs, calls = purposes_client
    set_defs([{"name": "MoreInformation", "relationshipPurpose": "ASSIGNMENT"}])
    client.get(_URL)
    client.get("/api/types/relationship-purposes?url=https://p:9443&server=other")
    assert len(calls) == 2


def test_endpoint_cache_expires(purposes_client, monkeypatch):
    client, set_defs, calls = purposes_client
    set_defs([{"name": "MoreInformation", "relationshipPurpose": "ASSIGNMENT"}])
    client.get(_URL)
    now = h.time.monotonic()
    monkeypatch.setattr(h.time, "monotonic", lambda: now + h._PURPOSE_TTL + 1)
    client.get(_URL)
    assert len(calls) == 2


def test_endpoint_server_without_purposes(purposes_client):
    """An older server omits relationshipPurpose entirely."""
    client, set_defs, _ = purposes_client
    set_defs([{"name": "MoreInformation"}, {"name": "SemanticAssignment"}])
    body = client.get(_URL).json()
    assert body["serverReportsPurpose"] is False
    assert body["purposes"] == {"MoreInformation": None, "SemanticAssignment": None}


def test_endpoint_no_defs(purposes_client):
    """pyegeria returns a 'No elements found' string when the list is empty."""
    client, set_defs, _ = purposes_client
    set_defs("No elements found")
    assert client.get(_URL).json() == {"purposes": {}, "serverReportsPurpose": False}


def test_endpoint_error_is_not_cached(purposes_client, monkeypatch):
    client, set_defs, calls = purposes_client

    async def boom(url, server, user_id, user_pwd):
        raise RuntimeError("platform down")

    monkeypatch.setattr(h, "_get_client_async", boom)
    assert client.get(_URL).status_code == 500
    assert h._PURPOSE_CACHE == {}
