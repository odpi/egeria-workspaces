# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests (freshstart): the Overview carries pyegeria's "unconfirmed" figures (pager step 4).

pyegeria marks a figure counted from a scan Egeria didn't confirm was complete in
result["unconfirmed"][<figure key>] = {unconfirmed, positions_read, reason, words}. The payload carries the
mark under the payload key, a share over it is None with a reason in `notMeasured`, and confirmed figures are
unchanged. Run inside a pyegeria-web container:

    python -m pytest test_overview_unconfirmed.py -q
"""
import json

import pytest

import overview_handler as oh

REASON = "Egeria didn't confirm there are no more"


def _mark(words, positions=229):
    return {"unconfirmed": True, "positions_read": positions, "reason": REASON, "words": words}


def test_carry_maps_marks_to_payload_keys():
    r = {"active": 229, "exceptions": 0, "unconfirmed": {"active": _mark("at least 229"),
                                                          "exceptions": _mark("at least 0")}}
    out = oh._carry_unconfirmed(r, {"active": "certifications", "exceptions": "openExceptions"}, {})
    assert out["certifications"]["words"] == "at least 229"
    assert out["openExceptions"]["words"] == "at least 0"   # a lower bound of 0 is not "none"
    assert oh._carry_unconfirmed({"active": 1}, {"active": "certifications"}, {}) == {}


@pytest.fixture
def ai_stubs(monkeypatch):
    monkeypatch.setattr(oh, "_cache_get", lambda key: None)
    monkeypatch.setattr(oh, "_cache_put", lambda key, value: value)
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "context_readiness_funnel", lambda mgr, ce, as_of: {
        "cataloged": 300, "documented": 120, "classified": 90, "lineage": 40, "aiReady": None})
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of: {"groundingLinks": 55, "groundingPct": 18})
    monkeypatch.setattr(oh, "generate_vega_funnel_chart", None)


def _get_ai(**kw):
    return json.loads(oh.get_ai_context(as_of_time=None, url=None, server=None, user_id=None, **kw).body)


def test_ai_context_unconfirmed(monkeypatch, ai_stubs):
    monkeypatch.setattr(oh, "ownership_coverage", lambda mgr, as_of: {
        "ownershipCount": 61, "unconfirmed": {"ownershipCount": _mark("at least 61")}})
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "total": 250, "unconfirmed": {"aiReadyCount": _mark("at least 12")}})
    monkeypatch.setattr(oh, "drl_readiness_gates", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "aiReadyRecentCount": 5, "byModality": {"tabular": 3},
        "unconfirmed": {"aiReadyRecentCount": _mark("at least 5")}})
    p = _get_ai()
    assert p["unconfirmed"]["ownershipCount"]["words"] == "at least 61"
    assert p["unconfirmed"]["funnel.aiReady"]["words"] == "at least 12"
    for share in ("ownershipPct", "aiReadyPct", "drlRecentPct"):
        assert p[share] is None and p["notMeasured"][share], share


def test_ai_context_confirmed_is_unchanged(monkeypatch, ai_stubs):
    monkeypatch.setattr(oh, "ownership_coverage", lambda mgr, as_of: {"ownershipCount": 60})
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of: {"aiReadyCount": 25, "total": 250})
    monkeypatch.setattr(oh, "drl_readiness_gates", lambda mgr, ce, as_of: {
        "aiReadyCount": 25, "aiReadyRecentCount": 5, "byModality": {"tabular": 3}})
    p = _get_ai()
    assert p["unconfirmed"] == {} and p["notMeasured"] == {}
    assert p["ownershipPct"] == 20.0 and p["aiReadyPct"] == 10.0 and p["drlRecentPct"] == 20.0
