# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests for the Overview's count scope (whole repository vs what the viewer can see).

pyegeria after 6.2.21 lets the count helpers take scope="repository"|"viewer"; 6.2.21 and older do not.
The handler must (1) pass scope only when the helper accepts it, (2) report the scope each payload
actually used, and (3) never put a repository-scoped number and a viewer-scoped one in the same ratio.

    python -m pytest test_overview_scope.py -q
"""
import inspect

import pytest

import overview_handler as oh


# ── stubs: with and without a `scope` parameter ──────────────────────────────

def _make_old():
    calls = []

    def count_elements(mgr, type_name=None, as_of=None, classifications=None, strict=False):
        calls.append({"type": type_name, "cls": classifications})
        return 1
    count_elements.calls = calls
    return count_elements


def _make_new():
    calls = []

    def count_elements(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=None):
        calls.append({"type": type_name, "cls": classifications, "scope": scope})
        return 1
    count_elements.calls = calls
    return count_elements


# ── feature detection ────────────────────────────────────────────────────────

def test_scope_passed_when_the_helper_supports_it():
    fn = _make_new()
    oh._scoped(fn, oh.REPOSITORY)(None, "Asset", strict=True)
    assert fn.calls == [{"type": "Asset", "cls": None, "scope": "repository"}]


def test_scope_omitted_when_the_helper_does_not_support_it():
    fn = _make_old()
    bound = oh._scoped(fn, oh.REPOSITORY)
    assert bound is fn                                   # nothing bound, so no unexpected kwarg
    bound(None, "Asset", strict=True)                    # would raise TypeError if scope had been passed
    assert fn.calls == [{"type": "Asset", "cls": None}]


def test_viewer_scope_never_binds_the_parameter():
    fn = _make_new()
    oh._scoped(fn, oh.VIEWER)(None, "Asset")
    assert "scope" in fn.calls[0] and fn.calls[0]["scope"] is None


def test_detection_is_cached_per_function():
    fn = _make_new()
    assert oh._accepts_scope(fn) is True
    assert fn in oh._SCOPE_SUPPORT
    assert oh._accepts_scope(_make_old()) is False


def test_route_scope_is_repository_only_if_every_helper_supports_it():
    assert oh._count_scope(_make_new(), _make_new()) == "repository"
    assert oh._count_scope(_make_new(), _make_old()) == "viewer"      # one laggard -> viewer for all
    assert oh._count_scope(_make_old()) == "viewer"
    assert oh._count_scope() == "viewer"


def test_installed_pyegeria_is_detected_honestly():
    # whatever is installed: the answer must match the real signature, not a version guess
    from pyegeria.view.overview_metrics import count_elements
    assert oh._accepts_scope(count_elements) == ("scope" in inspect.signature(count_elements).parameters)


# ── Governed Coverage: numerator and denominator share one scope ─────────────

@pytest.mark.parametrize("make", [_make_old, _make_new])
def test_governed_numerators_use_one_function_and_one_scope(make):
    fn = make()
    bound = oh._scoped(fn, oh._count_scope(fn))
    oh._governed_asset_counts(bound, None)
    bound(None, "Asset", None, strict=True)             # the denominator, taken the same way as in get_summary
    scopes = {c.get("scope") for c in fn.calls}
    assert len(scopes) == 1                              # all three calls: identical scope, never a mix
    assert len(fn.calls) == 3
    assert all(c["type"] == "Asset" for c in fn.calls)


def test_summary_takes_every_governed_count_through_the_same_bound_helper():
    src = inspect.getsource(oh._compute_summary)
    assert "_governed_asset_counts(n_elements, mgr, as_of_time)" in src
    assert 'asset_total = n_elements(mgr, "Asset", as_of_time, strict=True)' in src


def test_ratios_with_find_numerators_never_use_the_scoped_total():
    src = inspect.getsource(oh.get_summary)
    # find-based survey / schema ratios get a total only when it is viewer-scoped
    assert "_overlay_viewer_total(payload," in src            # viewer total comes only from the overlay



def _ai_context(monkeypatch, default_scope, grounding=None, owned=120):
    """get_ai_context with every Egeria call stubbed; returns (payload, scopes count_elements received).
    `default_scope` is the default of count_elements' scope parameter: "repository" from pyegeria 6.2.27
    (and so the population of context_readiness_funnel, which takes none), None before it."""
    import json
    seen = []

    def count_elements(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=default_scope):
        seen.append(scope)
        if classifications is None:
            return 1000
        return owned if tuple(classifications) == ("Ownership",) else 300
    monkeypatch.setattr(oh, "count_elements", count_elements)
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "context_readiness_funnel", lambda mgr, ce, as_of=None: {
        "cataloged": 1000, "documented": 400, "classified": 300, "lineage": 200, "aiReady": None})
    monkeypatch.setattr(oh, "semantic_grounding", lambda mgr, ce, as_of=None: grounding or {"groundingLinks": 50, "groundingPct": 5})

    def no_ownership_find(*a, **k):
        raise AssertionError("Ownership Coverage must not use the any-type find any more")
    monkeypatch.setattr(oh, "ownership_coverage", no_ownership_find)
    monkeypatch.setattr(oh, "ai_ready_assets", lambda mgr, ce, as_of=None: {"aiReadyCount": 40, "total": 500})
    monkeypatch.setattr(oh, "drl_readiness_gates", None, raising=False)
    monkeypatch.setattr(oh, "_section_fetch", lambda key, compute, ok=None: (compute(), {}))   # compute inline
    monkeypatch.setattr(oh, "_env", lambda *a, **k: ("u", "view-server", "x", "y"))

    def no_viewer_total(*a, **k):
        raise AssertionError("ai-context must not wait on the (uncountable) viewer Asset total")
    monkeypatch.setattr(oh, "_viewer_total_state", no_viewer_total)
    resp = oh.get_ai_context(as_of_time=None, url=None, server=None, user_id=None)
    return json.loads(resp.body), seen


def test_ai_context_on_a_viewer_default_pyegeria_is_unchanged(monkeypatch):
    out, seen = _ai_context(monkeypatch, None)
    assert out["countScope"] == oh.VIEWER
    assert seen == [oh.VIEWER] * 3                           # Cataloged, Classified, owned Assets: one population
    assert out["funnel"]["aiReady"] == 40 and out["aiReadyCount"] == 40
    assert out["ownershipPct"] == 12.0 and out["ownershipScope"] == oh.VIEWER   # 120 owned Assets / 1000 Assets
    assert "ownershipPctLoading" not in out


def test_ai_context_on_a_repository_default_pyegeria_never_mixes_populations(monkeypatch):
    # P1-2. pyegeria 6.2.27: the funnel and grounding count the whole repository; ownership and AI-Ready are
    # finds (what the viewer can see) and are never divided by, or drawn beside, the repository total.
    out, seen = _ai_context(monkeypatch, oh.REPOSITORY)
    assert out["countScope"] == oh.REPOSITORY                # funnel stages labelled repository
    assert seen == [oh.REPOSITORY] * 3                       # Cataloged, Classified, owned Assets
    assert out["funnel"]["cataloged"] == 1000 and out["funnel"]["classified"] == 300
    assert out["funnel"]["aiReady"] is None                   # not a stage of a repository funnel
    assert out["aiReadyCount"] == 40 and out["aiReadyScope"] == oh.VIEWER
    assert out["aiReadyPct"] == 8.0                           # 40 / 500: its own (viewer) total
    # Ownership Coverage (2026-11-10): owned ASSETS (strict native, repository) over Cataloged (same count, same
    # population) -- the shape of Governed Coverage. Always measurable; never a viewer find over a viewer total.
    assert out["ownershipScope"] == oh.REPOSITORY
    assert out["ownershipCount"] == 120 and out["ownershipPct"] == 12.0
    assert "ownershipPctLoading" not in out


def test_ai_context_ownership_unmeasured_is_none_not_a_guess(monkeypatch):
    out, _ = _ai_context(monkeypatch, oh.REPOSITORY, owned=None)
    assert out["ownershipCount"] is None and out["ownershipPct"] is None


def test_owned_asset_share_never_exceeds_100_and_needs_a_total():
    seen = []
    def n(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=None):
        seen.append((type_name, tuple(classifications or ()), strict, scope)); return 50
    orig = oh.count_elements
    try:
        oh.count_elements = n
        assert oh._owned_asset_share(None, None, oh.REPOSITORY, 40) == (50, None)     # owned > total: not a %
        assert oh._owned_asset_share(None, None, oh.REPOSITORY, None) == (50, None)   # no total: not measured
        assert oh._owned_asset_share(None, None, oh.REPOSITORY, 200) == (50, 25.0)
    finally:
        oh.count_elements = orig
    assert seen[0] == ("Asset", ("Ownership",), True, oh.REPOSITORY)


def test_grounding_is_links_per_100_assets_never_a_percent_today(monkeypatch):
    # pyegeria 6.2.30: groundingPct = links / Assets x 100. Not a share of Assets -> not shown as one.
    out, _ = _ai_context(monkeypatch, oh.REPOSITORY)
    assert out["groundingMeasure"] == "linksPer100Assets"
    assert out["groundingValue"] == 5 and out["groundingLinksPer100"] == 5 and out["groundingLinks"] == 50
    assert out["groundingPct"] is None and out["groundedAssets"] is None


def test_grounding_switches_to_the_asset_share_when_pyegeria_reports_it(monkeypatch):
    g = {"groundingLinks": 50, "groundingPct": 5, "groundedAssets": 30, "groundedAssetPct": 3.0}
    out, _ = _ai_context(monkeypatch, oh.REPOSITORY, grounding=g)
    assert out["groundingMeasure"] == "assetShare"
    assert out["groundingValue"] == 3.0 and out["groundingPct"] == 3.0 and out["groundedAssets"] == 30
    assert out["groundingLinksPer100"] == 5


def test_grounding_unmeasured_is_none():
    assert oh._grounding_fields(None)["groundingValue"] is None
    assert oh._grounding_fields({"groundingLinks": None, "groundingPct": None})["groundingMeasure"] == "linksPer100Assets"


def test_strict_funnel_counts_pass_the_scope_explicitly(monkeypatch):
    seen = []

    def with_scope(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=None):
        seen.append(scope)
        return 0
    monkeypatch.setattr(oh, "count_elements", with_scope)
    oh._strict_funnel_counts({}, None, None, scope=oh.REPOSITORY)
    oh._strict_funnel_counts({}, None, None, scope=oh.VIEWER)
    assert seen == [oh.REPOSITORY, oh.REPOSITORY, oh.VIEWER, oh.VIEWER]

    def without_scope(mgr, type_name=None, as_of=None, classifications=None, strict=False):   # pyegeria <= 6.2.21
        return 0
    monkeypatch.setattr(oh, "count_elements", without_scope)
    assert oh._strict_funnel_counts({}, None, None, scope=oh.REPOSITORY)["cataloged"] == 0


def test_summary_passes_its_scope_to_business_value_and_survey_coverage(stubbed_summary):
    seen, ce, bt, rel, prop = _stubs(with_scope=True)
    got = {}

    def bv(mgr, as_of=None, scope=None, *, population=None):
        got["business_value_signals"] = scope
        return {"assetTotal": 100, "assetCapped": False, "confidentialCount": 1, "describedCount": 2,
                "duplicateCount": 0}

    def survey(mgr, ce_, as_of=None, asset_total=None, scope=oh.REPOSITORY):
        got["_survey_coverage"] = scope
        return {k: None for k in ("surveyedAssets", "dataStoreTotal", "surveyedStores", "neverSurveyedStores",
                                  "surveyReports", "surveyLinksCapped", "qualityAnnotatedAssets", "annotationsByType",
                                  "surveysCompleted", "surveysFailed", "surveysUnknown", "assetsSurveyFailedOnly",
                                  "latestSurveyTime", "surveysCompleted7d", "dataStoresByKind", "schemaAnalysedGuids")}
    out = stubbed_summary(ce, bt, rel, prop, business_value_signals=bv, _survey_coverage=survey)
    assert out["countScope"] == oh.REPOSITORY
    assert got == {"business_value_signals": oh.REPOSITORY, "_survey_coverage": oh.REPOSITORY}


def test_survey_coverage_counts_in_the_scope_it_is_given(monkeypatch):
    seen = []

    def count_elements(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=None):
        seen.append((type_name, scope, strict))
        return 7

    class Mgr:   # every find fills its page, so the DataStore total comes from the native count
        def find_metadata_elements(self, body):
            return [{"elementHeader": {"guid": f"g{i}"}, "guid": f"g{i}"} for i in range(body.get("pageSize") or 500)]

    class CE:
        def get_relationships(self, **kw):
            return []
    monkeypatch.setattr(oh, "count_elements", count_elements)
    out = oh._survey_coverage(Mgr(), CE(), None, None, scope=oh.REPOSITORY)
    assert ("SurveyReport", oh.REPOSITORY, True) in seen and ("DataStore", oh.REPOSITORY, True) in seen   # strict
    assert out["surveyReports"] == 7 and out["dataStoreTotal"] == 7
    assert out["neverSurveyedStores"] is None                 # a capped store find never feeds the difference


# ── payload reports the scope actually used ──────────────────────────────────

@pytest.fixture
def stubbed_summary(monkeypatch):
    """get_summary with every Egeria call replaced by a stub; returns a callable -> payload dict."""
    import json

    def run(count_elements_fn, by_type_fn, rel_fn, prop_fn, **overrides):
        monkeypatch.setattr(oh, "count_elements", count_elements_fn)
        monkeypatch.setattr(oh, "counts_by_type", by_type_fn)
        monkeypatch.setattr(oh, "count_relationships", rel_fn)
        monkeypatch.setattr(oh, "count_elements_by_property", prop_fn)
        oh._CACHE.clear() if hasattr(oh, "_CACHE") else None
        monkeypatch.setattr(oh, "_cache_get", lambda k: None)
        monkeypatch.setattr(oh, "_section_fetch", lambda key, compute, ok=None: (compute(), {}))   # compute inline
        monkeypatch.setattr(oh, "_cache_put", lambda k, v: v)
        monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (None, True, False, None))   # cold: counting
        monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
        monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
        monkeypatch.setattr(oh, "_env", lambda *a, **k: ("u", "view-server", "x", "y"))
        monkeypatch.setattr(oh, "governed_coverage", lambda *a, **k: {"byClassification": {}, "topZones": []})
        monkeypatch.setattr(oh, "generate_vega_bar_chart", lambda *a, **k: None)
        monkeypatch.setattr(oh, "_certifications", lambda *a, **k: {"active": 0, "expiring90": 0, "soon": [], "licenses": 0, "exceptions": 0})
        monkeypatch.setattr(oh, "business_value_signals", None)
        monkeypatch.setattr(oh, "orphan_glossary_terms", None)
        monkeypatch.setattr(oh, "stale_assets", None)
        monkeypatch.setattr(oh, "_survey_coverage", lambda *a, **k: {
            k2: None for k2 in ("surveyedAssets", "dataStoreTotal", "surveyedStores", "neverSurveyedStores", "surveyReports",
                                "surveyLinksCapped", "qualityAnnotatedAssets", "annotationsByType", "surveysCompleted",
                                "surveysFailed", "surveysUnknown", "assetsSurveyFailedOnly", "latestSurveyTime",
                                "surveysCompleted7d", "dataStoresByKind", "schemaAnalysedGuids")})
        monkeypatch.setattr(oh, "_schema_coverage", lambda *a, **k: {"assetsWithSchema": None, "schemaAnalysedAssets": None, "schemaTypes": None})
        monkeypatch.setattr(oh, "_engine_action_health", lambda *a, **k: None)
        monkeypatch.setattr(oh, "_confidentiality_levels", lambda *a, **k: {"levels": None, "classified": None, "capped": None})
        monkeypatch.setattr(oh, "_assets_by_technology", lambda *a, **k: {"technologies": None, "unrecorded": None, "placeholders": None, "total": None})
        for name, value in overrides.items():          # a test's own stub for any of the above
            monkeypatch.setattr(oh, name, value)
        resp = oh.get_summary(as_of_time=None, url=None, server=None, user_id=None)
        return json.loads(resp.body)
    return run


def _stubs(with_scope):
    seen = []

    def ce(mgr, type_name=None, as_of=None, classifications=None, strict=False, **kw):
        seen.append(kw.get("scope"))
        return 100 if classifications is None else 40
    def bt(mgr, type_map, as_of=None, strict=False, **kw):
        seen.append(kw.get("scope"))
        return [{"type": t, "label": l, "count": 1} for t, l in type_map]
    def rel(c, r, as_of=None, expert=None, **kw):
        seen.append(kw.get("scope"))
        return 0
    def prop(mgr, t, n, v, as_of=None, strict=False, **kw):
        seen.append(kw.get("scope"))
        return 1
    if with_scope:
        # same behaviour, but with an explicit scope parameter in the signature
        def ce2(mgr, type_name=None, as_of=None, classifications=None, strict=False, scope=None):
            return ce(mgr, type_name, as_of, classifications, strict, scope=scope)
        def bt2(mgr, type_map, as_of=None, strict=False, scope=None):
            return bt(mgr, type_map, as_of, strict, scope=scope)
        def rel2(c, r, as_of=None, expert=None, scope=None):
            return rel(c, r, as_of, expert, scope=scope)
        def prop2(mgr, t, n, v, as_of=None, strict=False, scope=None):
            return prop(mgr, t, n, v, as_of, strict, scope=scope)
        return seen, ce2, bt2, rel2, prop2
    return seen, ce, bt, rel, prop


def test_summary_reports_viewer_scope_on_old_pyegeria(stubbed_summary):
    seen, ce, bt, rel, prop = _stubs(with_scope=False)
    # old pyegeria: the stubs must not receive a scope kwarg at all
    def strict_ce(mgr, type_name=None, as_of=None, classifications=None, strict=False):
        return ce(mgr, type_name, as_of, classifications, strict)
    def strict_bt(mgr, type_map, as_of=None, strict=False):
        return bt(mgr, type_map, as_of, strict)
    def strict_rel(c, r, as_of=None, expert=None):
        return rel(c, r, as_of, expert)
    def strict_prop(mgr, t, n, v, as_of=None, strict=False):
        return prop(mgr, t, n, v, as_of, strict)
    out = stubbed_summary(strict_ce, strict_bt, strict_rel, strict_prop)
    assert out["countScope"] == "viewer"
    assert out["assetTotalViewer"] == out["assetTotal"] == 100       # viewer total is usable for find ratios
    assert out["governedCount"] == 40


def test_summary_reports_repository_scope_and_withholds_the_viewer_total(stubbed_summary):
    seen, ce, bt, rel, prop = _stubs(with_scope=True)
    out = stubbed_summary(ce, bt, rel, prop)
    assert out["countScope"] == "repository"
    assert out["assetTotal"] == 100 and out["governedCount"] == 40
    assert out["assetTotalViewer"] is None and out["assetTotalViewerLoading"] is True   # find numerator must not meet this total
    assert seen and set(seen) == {"repository"}                      # every native count used the same scope


def test_one_unsupported_helper_pulls_the_whole_summary_back_to_viewer(stubbed_summary):
    seen, ce, bt, rel, prop = _stubs(with_scope=True)
    def old_prop(mgr, t, n, v, as_of=None, strict=False):            # the laggard
        return 1
    out = stubbed_summary(ce, bt, rel, old_prop)
    assert out["countScope"] == "viewer"
    assert set(seen) == {None}                                       # nothing got a repository scope
    assert out["assetTotalViewer"] == out["assetTotal"]


def test_people_and_usage_report_their_scope(monkeypatch):
    import json
    monkeypatch.setattr(oh, "_cache_get", lambda k: None)
    monkeypatch.setattr(oh, "_section_fetch", lambda key, compute, ok=None: (compute(), {}))   # compute inline
    monkeypatch.setattr(oh, "_cache_put", lambda k, v: v)
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: object())
    monkeypatch.setattr(oh, "karma_leaderboard", None)
    monkeypatch.setattr(oh, "engagement_series", None)
    monkeypatch.setattr(oh, "contextualised_coverage", None)
    monkeypatch.setattr(oh, "solution_component_realisation", None)
    keys = ("persons", "teams", "organizations", "itProfiles", "communities")
    def pc(mgr, as_of=None, strict=False, scope=None):
        return {k: 1 for k in keys}
    def ce(mgr, t=None, as_of=None, classifications=None, strict=False, scope=None):
        return 2
    def rel(c, r, as_of=None, expert=None, scope=None):
        return 3
    def uc(mgr, as_of=None, strict=False, scope=None):
        return {"informationSupplyChains": 4, "blueprints": 5}
    monkeypatch.setattr(oh, "people_counts", pc)
    monkeypatch.setattr(oh, "count_elements", ce)
    monkeypatch.setattr(oh, "count_relationships", rel)
    monkeypatch.setattr(oh, "usage_context_counts", uc)
    people = json.loads(oh.get_people(as_of_time=None, url=None, server=None, user_id=None).body)
    usage = json.loads(oh.get_usage_context(as_of_time=None, url=None, server=None, user_id=None).body)
    assert people["countScope"] == usage["countScope"] == "repository"
    # and back to viewer when one helper lacks the parameter
    monkeypatch.setattr(oh, "count_relationships", lambda c, r, as_of=None, expert=None: 3)
    people = json.loads(oh.get_people(as_of_time=None, url=None, server=None, user_id=None).body)
    assert people["countScope"] == "viewer"


def test_repository_relationship_counts_are_given_the_expert():
    """count_relationships only applies a scope through `expert`; without it repository scope is None."""
    seen = []

    def rel(c, r, as_of=None, expert=None, scope=None):
        seen.append((expert, scope))
        return 1
    marker = object()
    oh._scoped(rel, oh.REPOSITORY, expert=marker)(None, "AttachedLike", None)
    assert seen == [(marker, "repository")]
    seen.clear()
    oh._scoped(rel, oh.VIEWER, expert=marker)(None, "AttachedLike", None)   # viewer: untouched
    assert seen == [(None, None)]
    src = inspect.getsource(oh._compute_summary) + inspect.getsource(oh.get_people)
    assert src.count("expert=mgr") + src.count("expert=expert") >= 2


def test_grounding_shows_one_decimal_under_10():
    # Architect P3: 767 links over 56,357 Assets is 1.36 per 100 -> 1.4, not pyegeria's whole-number "1"
    g = {"groundingLinks": 767, "groundingPct": 1}
    f = oh._grounding_fields(g, 56357, oh.REPOSITORY)
    assert f["groundingValue"] == 1.4 and f["groundingLinksPer100"] == 1.4 and f["groundingPct"] is None
    # 10 and up: a whole number
    assert oh._grounding_fields({"groundingLinks": 1234, "groundingPct": 12}, 10000, oh.REPOSITORY)["groundingValue"] == 12
    # the asset share is rounded the same way
    s = oh._grounding_fields({"groundingLinks": 767, "groundedAssets": 700, "groundedAssetPct": 1.2421}, 56357, oh.REPOSITORY)
    assert s["groundingMeasure"] == "assetShare" and s["groundingValue"] == 1.2 and s["groundingLinksPer100"] == 1.4


def test_grounding_never_recomputes_across_populations():
    # a viewer funnel's Cataloged is not semantic_grounding's population: keep pyegeria's own figure
    g = {"groundingLinks": 767, "groundingPct": 1}
    assert oh._grounding_fields(g, 56357, oh.VIEWER)["groundingValue"] == 1
    assert oh._grounding_fields(g, None, oh.REPOSITORY)["groundingValue"] == 1     # no Asset total: pyegeria's
    assert oh._grounding_fields(g, 0, oh.REPOSITORY)["groundingValue"] == 1
    assert oh._display_round(None) is None and oh._display_round(9.96) == 10.0 and oh._display_round(0.04) == 0.0
