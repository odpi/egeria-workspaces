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


# ── R1: routines that return bare numbers / lists (recording_unconfirmed) ────
#
# These run pyegeria's real pager (pager step 4, 7379bd83+) on fakes that return rows on the first page and
# null after it: on get_relationships and find_metadata_elements (both NULL_NOT_END) that ends as
# null_then_empty_probes, i.e. unconfirmed. Skipped on a pyegeria without recording_unconfirmed.

import time
from datetime import datetime, timezone

needs_pager = pytest.mark.skipif(oh.recording_unconfirmed is None,
                                 reason="needs pyegeria with pager step 4 (recording_unconfirmed)")

_NOW = datetime.now(timezone.utc).isoformat()


def _rel(rel_type, i):
    return {"relationshipHeader": {"guid": f"{rel_type}-{i}", "type": {"typeName": rel_type},
                                   "versions": {"createTime": _NOW}}}


def _karma_record(i, points):
    return {"elementHeader": {"guid": f"cr-{i}"},
            "elementProperties": {"propertyValueMap": {
                "karmaPoints": {"primitiveValue": points},
                "displayName": {"primitiveValue": f"Contribution record for Person {i}"}}},
            "classifications": [{"classificationName": "Anchors", "classificationProperties": {"propertyValueMap": {
                "anchorTypeName": {"primitiveValue": "Person"}, "anchorGUID": {"primitiveValue": f"p-{i}"}}}}]}


class _NullAfterFirstPageCE:
    """get_relationships: two rows of every type on the first page, then null (no native count)."""
    def get_relationships(self, relationship_type=None, output_format=None, start_from=0, page_size=0, body=None):
        start = (body or {}).get("startFrom", start_from)
        return [_rel(relationship_type, 0), _rel(relationship_type, 1)] if start == 0 else None


class _NullAfterFirstPageExpert:
    """find_metadata_elements: three ContributionRecords on the first page, then null; Assets: two, then null."""
    def find_metadata_elements(self, body):
        if body.get("startFrom", 0) == 0 and body.get("metadataElementTypeName") == "Asset":
            return [{"elementHeader": {"guid": "a-1"}}, {"elementHeader": {"guid": "a-2"}}]
        if body.get("startFrom", 0) == 0 and body.get("metadataElementTypeName") == "ContributionRecord":
            return [_karma_record(1, 30), _karma_record(2, 20), _karma_record(3, 10)]
        return "No elements found"   # pyegeria's null for a find


@pytest.fixture
def pager_fakes(monkeypatch):
    from pyegeria.view import overview_metrics as om
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: None)   # the paged (find/get) paths
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: _NullAfterFirstPageExpert())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: _NullAfterFirstPageCE())
    # the viewer population: feedback counts read get_relationships through the pager (the path that can end
    # unconfirmed); from pyegeria 6.2.27 an unscoped call is a repository count, so force the viewer one
    monkeypatch.setattr(oh, "feedback_summary", lambda ce, as_of=None: om.feedback_summary(ce, as_of, scope="viewer"))
    monkeypatch.setattr(oh, "people_counts", lambda mgr, as_of, **kw: {
        "persons": 4, "teams": 1, "organizations": 1, "itProfiles": 0, "communities": 2})


@needs_pager
def test_people_figures_from_unconfirmed_scans_are_marked(pager_fakes):
    p = oh._compute_people(None, None, None, None, None)
    u = p["unconfirmed"]
    assert p["feedbackItems"] == 10 and u["feedbackItems"]["words"] == "at least 10"
    assert u["feedbackByType"]["words"].startswith("each count is at least what is shown")
    assert [e["karmaPoints"] for e in p["leaderboard"]] == [30, 20, 10]
    assert u["leaderboard"]["words"].startswith("each count is at least what is shown")
    assert u["engagementSeries"]["unconfirmed"] is True
    for chart in ("feedbackChart", "engagementChart"):
        if p[chart] is not None:
            assert p[chart]["title"]["subtitle"] == oh.CHART_UNCONFIRMED_SUBTITLE, chart
    for k in ("feedbackItems", "feedbackByType", "leaderboard", "engagementSeries"):
        assert p[k] in (None, [], {}) or k in u, k
    assert p["unconfirmedScans"] == [] and p["unconfirmedScansLine"] is None
    assert p["activeContributors"] == 4 and "activeContributors" not in u


@needs_pager
def test_safety_net_lists_a_scan_no_figure_mark_covers():
    from pyegeria.view import overview_metrics as om

    @oh._scan_net
    def compute():
        return {"likes": len(om._all_relationships(_NullAfterFirstPageCE(), "AttachedLike")), "unconfirmed": {}}

    p = compute()
    assert [s["count"] for s in p["unconfirmedScans"]] == ["AttachedLike relationships"]
    assert p["unconfirmedScansLine"] == f"Some figures here are lower bounds: {REASON}"


# ── pager step 5 (part 1): viewer totals ("count_of") ────────────────────────

def _step5():
    try:
        from pyegeria.view import overview_metrics as om
        return om._figure_words(("count_of", "Asset"), "k", 1, {}) == "at least 1"
    except Exception:  # noqa: BLE001
        return False


needs_step5 = pytest.mark.skipif(oh.recording_unconfirmed is None or not _step5(),
                                 reason="needs pyegeria with pager step 5 part 1 (count_of marks)")


@pytest.fixture
def usage_stubs(monkeypatch):
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "usage_context_counts", lambda mgr, as_of: {"informationSupplyChains": 2,
                                                                         "blueprints": 3})


def test_unconfirmed_solution_component_total_is_marked(monkeypatch, usage_stubs):
    monkeypatch.setattr(oh, "solution_component_realisation", lambda mgr, ce, as_of: {
        "solutionComponentsTotal": 9, "solutionComponentsRealised": 4,
        "unconfirmed": {"solutionComponentsTotal": _mark("at least 9")}})
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["unconfirmed"]["solutionComponents"]["words"] == "at least 9"
    assert "solutionComponentsRealised" not in p["unconfirmed"]


@needs_step5
def test_step5_solution_components_through_the_real_pager(pager_fakes):
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["unconfirmed"]["solutionComponentsRealised"]["words"] == f"0 found; {REASON}"
    assert p["unconfirmedScans"] == []
