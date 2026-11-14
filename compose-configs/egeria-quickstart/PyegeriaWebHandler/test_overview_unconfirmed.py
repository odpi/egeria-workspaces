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
