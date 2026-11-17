# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests: the Overview carries pyegeria's "unconfirmed" figures (pager step 4) to the page.

A scan that ended at Egeria's null without Egeria confirming there are no more makes its figures lower
bounds. pyegeria marks each one in result["unconfirmed"][<figure key>] = {unconfirmed, positions_read,
reason, words}. The payload must carry the mark under its own key (`unconfirmed`), must never turn a share or
a whole-set figure into a number (`notMeasured` says why it is None), and must leave confirmed figures alone.

No Egeria needed: every pyegeria routine is stubbed with a result in the exact shape the pager branch
returns. Run inside the container (pyegeria and fastapi importable):

    python -m pytest test_overview_unconfirmed.py -q
"""
import pytest

import overview_handler as oh

REASON = "Egeria didn't confirm there are no more"


def _mark(words, positions=229):
    """One figure's mark, exactly as pyegeria's overview_metrics._mark writes it."""
    return {"unconfirmed": True, "positions_read": positions, "reason": REASON, "words": words}


# ── fixtures in the pager branch's shape ─────────────────────────────────────

def _certs_unconfirmed():
    return {"active": 229, "expiring90": 3, "soon": [{"name": "SOC 2", "days": 12}], "licenses": 4,
            "exceptions": 0,
            "unconfirmed": {"active": _mark("at least 229"), "expiring90": _mark("at least 3"),
                            "soon": _mark(f"each count is at least what is shown; {REASON}"),
                            "licenses": _mark("at least 4"), "exceptions": _mark("at least 0")}}


def _certs_confirmed():
    return {"active": 229, "expiring90": 3, "soon": [{"name": "SOC 2", "days": 12}], "licenses": 4,
            "exceptions": 0}


def _gov_unconfirmed():
    return {"governedCount": 40, "governedCapped": False, "fullyGoverned": 30, "partialZoneOnly": 10,
            "byClassification": {"Confidentiality": 12}, "topZones": [{"zone": "quarantine", "count": 5}],
            "unconfirmed": {"governedCount": _mark("at least 40"), "fullyGoverned": _mark("at least 30"),
                            "partialZoneOnly": _mark("at least 10"),
                            "byClassification": _mark(f"each count is at least what is shown; {REASON}"),
                            "topZones": _mark(f"each count is at least what is shown; {REASON}")}}


def _orphans_unconfirmed():
    # pyegeria's "whole_set" figure: orphanCount is already None; referencedCount is "N found; ..."
    return {"termTotal": 80, "referencedCount": 50, "orphanCount": None,
            "unconfirmed": {"referencedCount": _mark(f"50 found; {REASON}")}}


# ── _carry_unconfirmed ───────────────────────────────────────────────────────

def test_carry_maps_to_payload_keys_with_words_and_reason():
    out = oh._carry_unconfirmed(_certs_unconfirmed(), {"active": "certifications", "licenses": "licenses"}, {})
    assert set(out) == {"certifications", "licenses"}
    assert out["certifications"] == {"unconfirmed": True, "positions_read": 229, "reason": REASON,
                                     "words": "at least 229"}


def test_carry_keeps_a_zero_lower_bound():
    # "at least 0" is not "none": the page must not say "no exceptions"
    out = oh._carry_unconfirmed(_certs_unconfirmed(), {"exceptions": "openExceptions"}, {})
    assert out["openExceptions"]["words"] == "at least 0"


def test_carry_skips_a_figure_with_no_value():
    r = {"orphanCount": None, "unconfirmed": {"orphanCount": _mark("at least 3")}}
    assert oh._carry_unconfirmed(r, {"orphanCount": "orphanTermCount"}, {}) == {}


def test_carry_of_a_confirmed_result_adds_nothing():
    assert oh._carry_unconfirmed(_certs_confirmed(), {"active": "certifications"}, {}) == {}
    assert oh._carry_unconfirmed(None, {"active": "certifications"}, {}) == {}


def test_carry_reads_a_dotted_key_and_a_per_scan_positions_map():
    r = {"byType": {"ratings": 7},
         "unconfirmed": {"byType.ratings": _mark("at least 7", positions={"AttachedRating": 100, "x": 25})}}
    out = oh._carry_unconfirmed(r, {"byType.ratings": "feedbackByType.ratings"}, {})
    assert out["feedbackByType.ratings"]["positions_read"] == {"AttachedRating": 100, "x": 25}


def test_carry_never_leaves_a_bare_marker():
    r = {"active": 5, "unconfirmed": {"active": {"unconfirmed": True, "positions_read": 5}}}
    out = oh._carry_unconfirmed(r, {"active": "certifications"}, {})
    assert out["certifications"]["words"] == "at least 5"
    assert out["certifications"]["reason"] == REASON


# ── usage-context ────────────────────────────────────────────────────────────

@pytest.fixture
def usage_stubs(monkeypatch):
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_count_scope", lambda *fns: oh.REPOSITORY)
    monkeypatch.setattr(oh, "_scoped", lambda fn, scope, **extra: fn)
    monkeypatch.setattr(oh, "usage_context_counts",
                        lambda mgr, as_of, strict=False: {"informationSupplyChains": 2, "blueprints": 3})


def test_usage_context_unconfirmed_share_is_not_measured(monkeypatch, usage_stubs):
    monkeypatch.setattr(oh, "contextualised_coverage", lambda mgr, ce, as_of: {
        "contextualisedCount": 17, "assetTotal": 300, "contextualisedPct": None,
        "unconfirmed": {"contextualisedCount": _mark(f"17 found; {REASON}")}})
    monkeypatch.setattr(oh, "solution_component_realisation", lambda mgr, ce, as_of: {
        "solutionComponentsTotal": 9, "solutionComponentsRealised": 4,
        "unconfirmed": {"solutionComponentsRealised": _mark(f"4 found; {REASON}")}})
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["contextualisedPct"] is None
    assert "separate count" in p["notMeasured"]["contextualisedPct"]
    assert p["unconfirmed"]["contextualisedCount"]["words"] == f"17 found; {REASON}"
    assert p["unconfirmed"]["solutionComponentsRealised"]["unconfirmed"] is True
    # native counts are untouched and unmarked
    assert p["informationSupplyChains"] == 2 and "informationSupplyChains" not in p["unconfirmed"]


def test_usage_context_a_stray_share_is_dropped(monkeypatch, usage_stubs):
    # an older pyegeria that still sent a share next to an unconfirmed numerator: never shown as a number
    monkeypatch.setattr(oh, "contextualised_coverage", lambda mgr, ce, as_of: {
        "contextualisedCount": 17, "assetTotal": 300, "contextualisedPct": 6,
        "unconfirmed": {"contextualisedCount": _mark(f"17 found; {REASON}")}})
    monkeypatch.setattr(oh, "solution_component_realisation", None)
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["contextualisedPct"] is None and "contextualisedPct" in p["notMeasured"]


def test_usage_context_confirmed_is_unchanged(monkeypatch, usage_stubs):
    monkeypatch.setattr(oh, "contextualised_coverage", lambda mgr, ce, as_of: {
        "contextualisedCount": 17, "assetTotal": 300, "contextualisedPct": 6})
    monkeypatch.setattr(oh, "solution_component_realisation", lambda mgr, ce, as_of: {
        "solutionComponentsTotal": 9, "solutionComponentsRealised": 4})
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["contextualisedPct"] == 6 and p["solutionComponentsRealised"] == 4
    assert p["unconfirmed"] == {} and p["notMeasured"] == {}


# ── ai-context ───────────────────────────────────────────────────────────────

@pytest.fixture
def ai_stubs(monkeypatch):
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_default_population", lambda fn: oh.VIEWER)
    monkeypatch.setattr(oh, "context_readiness_funnel", lambda mgr, ce, as_of: {
        "cataloged": 300, "documented": 120, "classified": 90, "lineage": 40, "aiReady": None})
    monkeypatch.setattr(oh, "_strict_funnel_counts", lambda readiness, mgr, as_of, scope=None: dict(readiness))
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of: {"groundingLinks": 55, "groundingPct": 18})
    monkeypatch.setattr(oh, "generate_vega_funnel_chart", None)
    # Ownership Coverage is a strict native count (owned Assets / Cataloged): never marked
    monkeypatch.setattr(oh, "_owned_asset_share", lambda mgr, as_of, population, cataloged: (60, 20.0))


def _ai_unconfirmed(monkeypatch):
    # semantic_grounding as the pager branch returns it after an unconfirmed SemanticAssignment scan:
    # groundedAssetPct already None (share_of_other) with the reason in groundedAssetNote
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of: {
        "groundedAssets": 40, "groundedAssetTotal": 300, "groundedAssetPct": None,
        "groundedAssetNote": "The share was not measured: its numerator was read without Egeria confirming "
                             "there are no more.",
        "groundingLinksScanned": 70, "groundingLinksNotOnAsset": 3, "groundingLinks": 55, "groundingPct": 18,
        "unconfirmed": {"groundedAssets": _mark(f"40 found; {REASON}"),
                        "groundingLinksScanned": _mark("at least 70"),
                        "groundingLinksNotOnAsset": _mark("at least 3")}})
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "total": 250, "capped": False,
        "unconfirmed": {"aiReadyCount": _mark("at least 12", positions={"DataFlow": 600, "Asset": 250})}})
    monkeypatch.setattr(oh, "drl_readiness_gates", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "aiReadyRecentCount": 5, "byModality": {"tabular": 3, "text_media": 1, "other": 1},
        "unconfirmed": {"aiReadyCount": _mark("at least 12"), "aiReadyRecentCount": _mark("at least 5")}})


def test_ai_context_unconfirmed_counts_marked_and_shares_not_measured(monkeypatch, ai_stubs):
    _ai_unconfirmed(monkeypatch)
    p = oh._compute_ai_context(None, None, None, None, None)
    u, nm = p["unconfirmed"], p["notMeasured"]
    assert u["groundedAssets"]["words"] == f"40 found; {REASON}" and p["groundedAssets"] == 40
    assert u["groundingLinksScanned"]["words"] == "at least 70"
    assert p["groundingMeasure"] == "linksPer100Assets" and "not measured" in p["groundedAssetNote"]
    # Ownership Coverage is a native count: confirmed and unmarked
    assert p["ownershipPct"] == 20.0 and "ownershipCount" not in u and "ownershipPct" not in nm
    assert u["aiReadyCount"]["positions_read"] == {"DataFlow": 600, "Asset": 250}
    assert u["funnel.aiReady"]["words"] == "at least 12" and p["funnel"]["aiReady"] == 12
    assert u["drlRecentCount"]["words"] == "at least 5"
    assert u["drlByModality"]["unconfirmed"] is True
    # every share over an unconfirmed figure is None with a reason -- never 0, never a bare number
    for share in ("aiReadyPct", "drlRecentPct"):
        assert p[share] is None, share
        assert nm[share], share
    # confirmed native figures in the same payload are unmarked
    assert p["groundingLinks"] == 55 and "groundingPct" not in u and "groundingLinks" not in u


def test_ai_context_confirmed_is_unchanged(monkeypatch, ai_stubs):
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of: {"aiReadyCount": 12, "total": 250,
                                                                         "capped": False})
    monkeypatch.setattr(oh, "drl_readiness_gates", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "aiReadyRecentCount": 6, "byModality": {"tabular": 3}})
    p = oh._compute_ai_context(None, None, None, None, None)
    assert p["unconfirmed"] == {} and p["notMeasured"] == {}
    assert p["ownershipPct"] == 20.0
    assert p["aiReadyPct"] == round(100 * 12 / 250, 1)
    assert p["drlRecentPct"] == 50.0


# ── summary ──────────────────────────────────────────────────────────────────

@pytest.fixture
def summary_stubs(monkeypatch):
    """Everything behind _compute_summary stubbed to a quiet, confirmed default."""
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_env", lambda *a: (None, "qs-view-server", None, None))
    monkeypatch.setattr(oh, "_count_scope", lambda *fns: oh.REPOSITORY)
    monkeypatch.setattr(oh, "_scoped", lambda fn, scope, **extra: (lambda *a, **k: 300))
    monkeypatch.setattr(oh, "_governed_asset_counts", lambda n, mgr, as_of: (40, 30))
    monkeypatch.setattr(oh, "_compute_composition", lambda *a, **k: {})
    monkeypatch.setattr(oh, "_level1_rows", lambda r: [])
    monkeypatch.setattr(oh, "business_value_signals", None)
    monkeypatch.setattr(oh, "stale_assets", None)
    monkeypatch.setattr(oh, "_survey_coverage", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("off")))
    monkeypatch.setattr(oh, "_schema_coverage", lambda *a, **k: {"assetsWithSchema": None,
                                                                 "schemaAnalysedAssets": None, "schemaTypes": None})
    monkeypatch.setattr(oh, "_engine_action_health", lambda *a, **k: None)
    monkeypatch.setattr(oh, "_confidentiality_levels", lambda *a, **k: {"levels": None, "classified": None,
                                                                        "capped": None})
    monkeypatch.setattr(oh, "_assets_by_technology", lambda *a, **k: {"technologies": None, "unrecorded": None,
                                                                      "placeholders": None, "total": None})


def test_summary_unconfirmed(monkeypatch, summary_stubs):
    monkeypatch.setattr(oh, "governed_coverage", lambda mgr, as_of: _gov_unconfirmed())
    monkeypatch.setattr(oh, "certifications_summary", lambda ce, as_of: _certs_unconfirmed())
    monkeypatch.setattr(oh, "orphan_glossary_terms", lambda mgr, ce, as_of: _orphans_unconfirmed())
    p = oh._compute_summary(None, None, None, None, None)
    u, nm = p["unconfirmed"], p["notMeasured"]
    assert u["certifications"]["words"] == "at least 229" and p["certifications"] == 229
    assert u["certExpiring90"]["words"] == "at least 3"
    assert u["openExceptions"]["words"] == "at least 0" and p["openExceptions"] == 0
    assert set(u) >= {"certSoon", "licenses", "byClassification", "topZones"}
    # Governed Coverage is replaced by strict native counts: no pyegeria mark may ride on them
    assert p["governedCount"] == 40 and not {"governedCount", "fullyGoverned", "partialZoneOnly"} & set(u)
    # orphanCount needs the whole set: not measured, with the reason, never a number
    assert p["orphanTermCount"] is None and nm["orphanTermCount"]
    assert p["orphanTermTotal"] == 80 and "orphanTermTotal" not in u


def test_summary_orphan_count_with_a_number_is_still_not_measured(monkeypatch, summary_stubs):
    # an earlier pager build returned orphanCount "at most N": any unconfirmed scan makes it not measured
    monkeypatch.setattr(oh, "governed_coverage", lambda mgr, as_of: _gov_unconfirmed())
    monkeypatch.setattr(oh, "certifications_summary", lambda ce, as_of: _certs_confirmed())
    monkeypatch.setattr(oh, "orphan_glossary_terms", lambda mgr, ce, as_of: {
        "termTotal": 80, "referencedCount": 50, "orphanCount": 30,
        "unconfirmed": {"referencedCount": _mark(f"50 found; {REASON}"), "orphanCount": _mark("at most 30")}})
    p = oh._compute_summary(None, None, None, None, None)
    assert p["orphanTermCount"] is None and "orphanTermCount" in p["notMeasured"]


def test_summary_confirmed_is_unchanged(monkeypatch, summary_stubs):
    monkeypatch.setattr(oh, "governed_coverage", lambda mgr, as_of: {
        "governedCount": 40, "governedCapped": False, "fullyGoverned": 30, "partialZoneOnly": 10,
        "byClassification": {"Confidentiality": 12}, "topZones": [{"zone": "quarantine", "count": 5}]})
    monkeypatch.setattr(oh, "certifications_summary", lambda ce, as_of: _certs_confirmed())
    monkeypatch.setattr(oh, "orphan_glossary_terms", lambda mgr, ce, as_of: {
        "termTotal": 80, "referencedCount": 50, "orphanCount": 30})
    p = oh._compute_summary(None, None, None, None, None)
    assert p["unconfirmed"] == {} and p["notMeasured"] == {}
    assert p["certifications"] == 229 and p["orphanTermCount"] == 30 and p["openExceptions"] == 0


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
    monkeypatch.setattr(oh, "_count_scope", lambda *fns: oh.VIEWER)
    # the viewer population: count_relationships reads get_relationships through the pager (the path that can
    # end unconfirmed); from pyegeria 6.2.27 an unscoped call is a repository count, so force the viewer one
    monkeypatch.setattr(oh, "count_relationships",
                        lambda ce, rel, as_of=None, expert=None, **kw: om.count_relationships(ce, rel, as_of,
                                                                                               scope="viewer"))
    monkeypatch.setattr(oh, "people_counts", lambda mgr, as_of, strict=False, scope=None: {
        "persons": 4, "teams": 1, "organizations": 1, "itProfiles": 0, "communities": 2})


def _bare_numbers(payload, keys):
    """The figures among `keys` that have a value and no mark: each would show as a confirmed total."""
    return [k for k in keys if payload.get(k) not in (None, [], {}) and k not in payload["unconfirmed"]]


@needs_pager
def test_people_figures_from_unconfirmed_scans_are_marked(pager_fakes):
    p = oh._compute_people(None, None, None, None, None)
    u = p["unconfirmed"]
    # count_relationships (feedback), karma_leaderboard and engagement_series all ended unconfirmed
    assert p["feedbackItems"] == 10 and u["feedbackItems"]["words"] == "at least 10"
    assert u["feedbackByType"]["words"].startswith("each count is at least what is shown")
    assert [e["karmaPoints"] for e in p["leaderboard"]] == [30, 20, 10]
    assert u["leaderboard"]["words"].startswith("each count is at least what is shown")
    assert u["engagementSeries"]["unconfirmed"] is True
    assert u["feedbackItems"]["reason"] == REASON
    # the charts drawn from them say so
    for chart in ("feedbackChart", "engagementChart"):
        if p[chart] is not None:
            assert p[chart]["title"]["subtitle"] == oh.CHART_UNCONFIRMED_SUBTITLE, chart
    # no bare number left: every figure from a scan is marked, and nothing slipped past the marks
    assert _bare_numbers(p, ("feedbackItems", "feedbackByType", "leaderboard", "engagementSeries")) == []
    # people_counts is stubbed (no scan): confirmed, unmarked
    assert p["activeContributors"] == 4 and "activeContributors" not in u


@needs_pager
def test_safety_net_lists_a_scan_no_figure_mark_covers():
    from pyegeria.view import overview_metrics as om

    @oh._scan_net
    def compute():
        rels = om._all_relationships(_NullAfterFirstPageCE(), "AttachedLike")
        return {"likes": len(rels), "unconfirmed": {}}

    p = compute()
    assert p["likes"] == 2
    assert [s["count"] for s in p["unconfirmedScans"]] == ["AttachedLike relationships"]
    assert p["unconfirmedScansLine"] == f"Some figures here are lower bounds: {REASON}"


@needs_pager
def test_safety_net_is_empty_when_the_figure_is_marked():
    from pyegeria.view import overview_metrics as om

    @oh._scan_net
    def compute():
        unconfirmed: dict = {}
        n0 = oh._scan_pos()
        likes = len(om._all_relationships(_NullAfterFirstPageCE(), "AttachedLike"))
        oh._mark_from_scans(n0, {"likes": ("count", likes)}, unconfirmed)
        return {"likes": likes, "unconfirmed": unconfirmed}

    p = compute()
    assert p["unconfirmed"]["likes"]["words"] == "at least 2"
    assert p["unconfirmedScans"] == [] and p["unconfirmedScansLine"] is None


@needs_pager
def test_confirmed_scan_needs_no_mark_and_no_net():
    from pyegeria.view import overview_metrics as om

    class _Done:   # rows, then an empty page and a trusted end: a confirmed read
        def get_relationships(self, relationship_type=None, output_format=None, start_from=0, page_size=0,
                              body=None):
            return [_rel(relationship_type, 0)] if (body or {}).get("startFrom", 0) == 0 else []

    @oh._scan_net
    def compute():
        unconfirmed: dict = {}
        n0 = oh._scan_pos()
        rels = om._all_relationships(_Done(), "AttachedLike")
        oh._mark_from_scans(n0, {"likes": ("count", None if rels is None else len(rels))}, unconfirmed)
        return {"likes": None if rels is None else len(rels), "unconfirmed": unconfirmed}

    p = compute()
    assert p["unconfirmed"] == {}   # never marked: confirmed, or not measured (None), never a lower bound


@needs_pager
def test_unconfirmed_viewer_asset_total_is_not_a_denominator(monkeypatch):
    from pyegeria.view import overview_metrics as om
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: None)
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: _NullAfterFirstPageExpert())
    # 7379bd83's viewer count still takes one find page (step 5 moves it onto the pager); drive the worker
    # through a paged read so the recording sees the unconfirmed end it will see then
    monkeypatch.setattr(oh, "_viewer_count", lambda mgr, as_of: len(
        om._all_elements(mgr, {"class": "FindRequestBody", "metadataElementTypeName": "Asset"})))
    monkeypatch.setattr(oh, "_env", lambda *a: ("U", "S", None, None))
    monkeypatch.setattr(oh, "request_identity", lambda *a: "viewer-1")
    key = "U|S|viewer-1|None"
    monkeypatch.setattr(oh, "_viewer_totals", {})
    monkeypatch.setattr(oh, "_viewer_unconfirmed", {})
    oh._viewer_total_worker(key, None, None, None, None, None)   # the find fallback ends unconfirmed
    assert oh._viewer_unconfirmed[key], "the worker records the unconfirmed scan"
    assert oh._viewer_totals[key][0] > time.time() + 60, "kept for the normal TTL, not retried every minute"
    out = oh._overlay_viewer_total({"countScope": oh.REPOSITORY}, None, None, None, None, None)
    assert out["assetTotalViewer"] is None and out["assetTotalViewerLoading"] is False
    assert "lower bound" in out["assetTotalViewerNote"]


# ── pager step 5 (part 1): viewer totals ("count_of") ────────────────────────
#
# termTotal, the contextualised assetTotal, solutionComponentsTotal and groundedAssetTotal are viewer counts
# that can themselves end unconfirmed. pyegeria marks them "at least N" only when their own count was
# unconfirmed. Anything the Portal derives from one (a share, a difference) is not measured.

def _step5():
    try:
        from pyegeria.view import overview_metrics as om
        return om._figure_words(("count_of", "Asset"), "k", 1, {}) == "at least 1"
    except Exception:  # noqa: BLE001
        return False


needs_step5 = pytest.mark.skipif(oh.recording_unconfirmed is None or not _step5(),
                                 reason="needs pyegeria with pager step 5 part 1 (count_of marks)")


def test_share_over_an_unconfirmed_asset_total_is_not_measured(monkeypatch, usage_stubs):
    # only the total is unconfirmed (its own count ended unconfirmed); the numerator alone would be fine
    monkeypatch.setattr(oh, "contextualised_coverage", lambda mgr, ce, as_of: {
        "contextualisedCount": 17, "assetTotal": 300, "contextualisedPct": 6,
        "unconfirmed": {"assetTotal": _mark("at least 300")}})
    monkeypatch.setattr(oh, "solution_component_realisation", lambda mgr, ce, as_of: {
        "solutionComponentsTotal": 9, "solutionComponentsRealised": 4,
        "unconfirmed": {"solutionComponentsTotal": _mark("at least 9")}})
    p = oh._compute_usage_context(None, None, None, None, None)
    assert p["contextualisedPct"] is None and "Asset total" in p["notMeasured"]["contextualisedPct"]
    assert p["unconfirmed"]["contextualisedAssetTotal"]["words"] == "at least 300"
    assert p["unconfirmed"]["solutionComponents"]["words"] == "at least 9"
    assert "solutionComponentsRealised" not in p["unconfirmed"]


def test_orphan_difference_over_an_unconfirmed_term_total_is_not_measured(monkeypatch, summary_stubs):
    monkeypatch.setattr(oh, "governed_coverage", lambda mgr, as_of: {
        "governedCount": 40, "governedCapped": False, "fullyGoverned": 30, "partialZoneOnly": 10,
        "byClassification": {}, "topZones": []})
    monkeypatch.setattr(oh, "certifications_summary", lambda ce, as_of: _certs_confirmed())
    monkeypatch.setattr(oh, "orphan_glossary_terms", lambda mgr, ce, as_of: {
        "termTotal": 80, "referencedCount": 50, "orphanCount": 30,
        "unconfirmed": {"termTotal": _mark("at least 80")}})
    p = oh._compute_summary(None, None, None, None, None)
    assert p["orphanTermCount"] is None and "orphanTermCount" in p["notMeasured"]
    assert p["unconfirmed"]["orphanTermTotal"]["words"] == "at least 80"


@needs_step5
def test_step5_viewer_totals_through_the_real_pager(pager_fakes):
    # real contextualised_coverage / solution_component_realisation on fakes whose reads end at a null:
    # the Asset count (viewer find fallback) and the ImplementedBy scan are both unconfirmed
    p = oh._compute_usage_context(None, None, None, None, None)
    u = p["unconfirmed"]
    assert p["contextualisedAssetTotal"] == 2 and u["contextualisedAssetTotal"]["words"] == "at least 2"
    assert p["contextualisedPct"] is None and p["notMeasured"]["contextualisedPct"]
    assert u["contextualisedCount"]["words"] == f"0 found; {REASON}"   # a lower bound of 0, not "none"
    assert "solutionComponentsRealised" in u
    assert p["unconfirmedScans"] == []   # every scan is accounted for by a mark


@needs_step5
def test_step5_term_total_through_the_real_pager(pager_fakes, summary_stubs, monkeypatch):
    monkeypatch.setattr(oh, "_make", lambda *a, **k: _NullAfterFirstPageCE())
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: _NullAfterFirstPageExpert())
    monkeypatch.setattr(oh, "governed_coverage", lambda mgr, as_of: {
        "governedCount": 40, "governedCapped": False, "fullyGoverned": 30, "partialZoneOnly": 10,
        "byClassification": {}, "topZones": []})
    monkeypatch.setattr(oh, "certifications_summary", lambda ce, as_of: _certs_confirmed())
    p = oh._compute_summary(None, None, None, None, None)
    assert p["orphanTermCount"] is None and p["notMeasured"]["orphanTermCount"]
    assert p["unconfirmed"]["orphanTermTotal"]["words"].startswith("at least")


# ── R4: Semantic Grounding ───────────────────────────────────────────────────
# Shape from pyegeria release/next 45add51a on laz (the browser read-back): groundedAssets "3 found; ..." and
# groundingLinksScanned "at least 715" are marked (the viewer's SemanticAssignment scan); groundingLinks (723)
# and groundingPct are native repository counts, so links per 100 Assets is confirmed and stays.

def _laz_grounding(**over):
    g = {"groundedAssets": 3, "groundedAssetTotal": None, "groundedAssetPct": None,
         "groundedAssetNote": "The share was not measured: its numerator was read without Egeria confirming "
                              "there are no more.",
         "groundingLinksScanned": 715, "groundingLinksNotOnAsset": 0, "groundingLinks": 723, "groundingPct": 5,
         "unconfirmed": {"groundedAssets": _mark(f"3 found; {REASON}"),
                         "groundingLinksScanned": _mark("at least 715")}}
    g.update(over)
    return g


def _ai_confirmed_rest(monkeypatch):
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of: {"aiReadyCount": 12, "total": 250})
    monkeypatch.setattr(oh, "drl_readiness_gates", lambda mgr, ce, as_of: {
        "aiReadyCount": 12, "aiReadyRecentCount": 6, "byModality": {"tabular": 3}})


def test_grounding_tile_carries_the_scan_marks_and_keeps_native_per_100(monkeypatch, ai_stubs):
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of: _laz_grounding())
    _ai_confirmed_rest(monkeypatch)
    p = oh._compute_ai_context(None, None, None, None, None)
    u = p["unconfirmed"]
    assert u["groundedAssets"]["words"] == f"3 found; {REASON}" and p["groundedAssets"] == 3
    assert u["groundingLinksScanned"]["words"] == "at least 715"
    # native: links per 100 Assets is confirmed and shown; the native link count is unmarked
    assert p["groundingMeasure"] == "linksPer100Assets" and p["groundingValue"] == 5
    assert "groundingLinks" not in u and "groundingLinksPer100" not in p["notMeasured"]


def test_grounding_per_100_over_an_unconfirmed_link_count_is_not_measured(monkeypatch, ai_stubs):
    marks = {**_laz_grounding()["unconfirmed"], "groundingLinks": _mark("at least 723")}
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of: _laz_grounding(unconfirmed=marks))
    _ai_confirmed_rest(monkeypatch)
    p = oh._compute_ai_context(None, None, None, None, None)
    assert p["groundingValue"] is None and p["groundingLinksPer100"] is None
    assert "separate count" in p["notMeasured"]["groundingLinksPer100"]
    assert p["unconfirmed"]["groundingLinks"]["words"] == "at least 723"
