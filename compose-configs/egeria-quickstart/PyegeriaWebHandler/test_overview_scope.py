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
    # the funnel keeps viewer scope for every stage and its ownership / AI-Ready percentages
    assert '"countScope": VIEWER' in inspect.getsource(oh._compute_ai_context)


# ── payload reports the scope actually used ──────────────────────────────────

@pytest.fixture
def stubbed_summary(monkeypatch):
    """get_summary with every Egeria call replaced by a stub; returns a callable -> payload dict."""
    import json

    def run(count_elements_fn, by_type_fn, rel_fn, prop_fn):
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
        resp = oh.get_summary(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None)
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
    people = json.loads(oh.get_people(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None).body)
    usage = json.loads(oh.get_usage_context(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None).body)
    assert people["countScope"] == usage["countScope"] == "repository"
    # and back to viewer when one helper lacks the parameter
    monkeypatch.setattr(oh, "count_relationships", lambda c, r, as_of=None, expert=None: 3)
    people = json.loads(oh.get_people(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None).body)
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
