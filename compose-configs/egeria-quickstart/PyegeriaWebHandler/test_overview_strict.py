# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests for the Overview's "a failure is not a zero" handling.

No Egeria needed -- the clients are fakes. Run with pytest from this directory, in an
environment where pyegeria and fastapi are importable (e.g. inside the container):

    python -m pytest test_overview_strict.py -q
"""
import pytest

import overview_handler as oh
from pyegeria.view import overview_metrics as om


class _FailingMgr:
    """A client whose every query fails: no native count, find raises."""
    def find_metadata_elements(self, body):
        raise RuntimeError("view server down")


class _EmptyMgr:
    """A client whose queries succeed and match nothing (pyegeria's miss sentinel)."""
    def find_metadata_elements(self, body):
        return "No elements found"


class _FailingCE:
    def get_relationships(self, **kw):
        raise RuntimeError("down")


class _ZeroCE:
    def get_relationships(self, **kw):
        return []


@pytest.fixture(autouse=True)
def _no_native_counts(monkeypatch):
    # force the find-based fallback so the fakes above decide the outcome
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: None)


# ── strict counts: failure -> None, never 0 ──────────────────────────────────

def test_strict_count_of_failed_query_is_none():
    assert om.count_elements(_FailingMgr(), "Asset", strict=True) is None


def test_nonstrict_count_of_failed_query_is_the_zero_we_are_avoiding():
    # documents why the handler passes strict=True
    assert om.count_elements(_FailingMgr(), "Asset") == 0


def test_strict_count_of_real_empty_result_is_zero():
    assert om.count_elements(_EmptyMgr(), "Asset", strict=True) == 0


def test_strict_people_and_usage_counts_are_none_on_failure():
    assert set(om.people_counts(_FailingMgr(), strict=True).values()) == {None}
    assert set(om.usage_context_counts(_FailingMgr(), strict=True).values()) == {None}


def test_handler_passes_strict_for_headline_counts():
    # the summary tile counts must come from strict calls; check the source rather than a live route
    import inspect
    src = inspect.getsource(oh._compute_summary)
    for needle in ('n_elements(mgr, "Asset", as_of_time, strict=True)',
                   'n_elements(mgr, "GlossaryTerm", as_of_time, strict=True)',
                   'n_elements(mgr, "DigitalProduct", as_of_time, strict=True)',
                   "n_by_type(mgr, _ASSET_TYPES, as_of_time, strict=True)"):
        assert needle in src, needle
    assert "strict=True" in inspect.getsource(oh.get_people)
    assert "strict=True" in inspect.getsource(oh._compute_usage_context)


# ── funnel: a measured 0 stays 0 ─────────────────────────────────────────────

def test_pyegeria_funnel_turns_zero_into_none_which_the_handler_corrects():
    # pyegeria 6.2.21 reports a measured 0 as None (`count or None`); later versions may report 0.
    # Either way the handler must end up with a real 0.
    raw = om.context_readiness_funnel(_EmptyMgr(), _ZeroCE())
    assert raw["cataloged"] in (None, 0) and raw["classified"] in (None, 0)
    fixed = oh._strict_funnel_counts(raw, _EmptyMgr())
    assert fixed["cataloged"] == 0 and fixed["classified"] == 0
    # other stages are untouched
    assert fixed["lineage"] == raw["lineage"] and fixed["aiReady"] is None


def test_funnel_failure_stays_none():
    fixed = oh._strict_funnel_counts({"cataloged": 0, "classified": 0}, _FailingMgr())
    assert fixed["cataloged"] is None and fixed["classified"] is None


# ── other best-effort blocks that folded failure to 0 ────────────────────────

def test_feedback_failure_is_none_not_zero():
    fb = oh._feedback_counts(_FailingCE())
    assert set(fb["byType"].values()) == {None}
    assert fb["total"] is None and len(fb["unmeasured"]) == 5
    # pyegeria 6.2.21's own summary reports the same failure as "0 items of feedback"; later versions
    # report None. The handler does not depend on which.
    assert om.feedback_summary(_FailingCE())["total"] in (0, None)


def test_feedback_real_zero_is_zero():
    fb = oh._feedback_counts(_ZeroCE())
    assert fb["total"] == 0 and fb["unmeasured"] == []


def test_feedback_partial_failure_has_no_total():
    class _Mixed:
        def get_relationships(self, relationship_type=None, **kw):
            if relationship_type == "AttachedTag":
                raise RuntimeError("down")
            return []
    fb = oh._feedback_counts(_Mixed())
    assert fb["byType"]["tags"] is None and fb["byType"]["ratings"] == 0
    assert fb["total"] is None and fb["unmeasured"] == ["tags"]


def test_business_value_failed_find_is_not_a_zero():
    failed = om.business_value_signals(_FailingMgr())
    assert failed["assetTotal"] in (0, None)  # 6.2.21: failure looks like an empty catalog; later: None
    out = oh._reconcile_business_value(failed, None, None)
    assert out["assetTotal"] is None and out["confidentialCount"] is None and out["describedCount"] is None


def test_business_value_real_empty_catalog_stays_zero():
    empty = om.business_value_signals(_EmptyMgr())
    out = oh._reconcile_business_value(empty, 0, 0)
    assert out["assetTotal"] == 0 and out["confidentialCount"] == 0 and out["duplicateCount"] == 0


def test_business_value_duplicate_count_is_the_strict_one():
    out = oh._reconcile_business_value({"assetTotal": 5, "duplicateCount": 0}, 5, None)
    assert out["duplicateCount"] is None


# ── Governed Coverage is an Assets-only share ────────────────────────────────

class _CountingMgr:
    """Records the body of every native count call and answers from a table keyed on
    (type, sorted classification names)."""
    def __init__(self, table):
        self.table, self.bodies = table, []

    def count_metadata_elements(self, body):
        self.bodies.append(body)
        names = tuple(sorted(c["name"] for c in (body.get("matchClassifications") or {}).get("conditions", [])))
        return self.table[(body.get("metadataElementTypeName"), names)]


def test_governed_counts_are_asset_scoped_and_strict(monkeypatch):
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: "count_metadata_elements")
    G = tuple(sorted(om.GOVERNANCE_CLASSIFICATIONS))
    S = tuple(sorted(oh._SUBSTANTIVE_GOVERNANCE))
    # any-type tally (232) differs from the Asset-scoped one (43): the numerator must be the latter
    mgr = _CountingMgr({("Asset", G): 43, ("Asset", S): 30, (None, G): 232})
    governed = om.count_elements(mgr, "Asset", None, classifications=om.GOVERNANCE_CLASSIFICATIONS, strict=True)
    fully = om.count_elements(mgr, "Asset", None, classifications=oh._SUBSTANTIVE_GOVERNANCE, strict=True)
    assert (governed, fully) == (43, 30)
    assert all(b["metadataElementTypeName"] == "Asset" for b in mgr.bodies)
    out = oh._asset_scoped_governed({"byClassification": {"Confidentiality": 5}, "topZones": []}, governed, fully)
    assert out["governedCount"] == 43 and out["governedCapped"] is False
    assert out["fullyGoverned"] == 30 and out["partialZoneOnly"] == 13
    assert out["byClassification"] == {"Confidentiality": 5}      # element-wide breakdown is passed through


def test_governed_summary_route_uses_asset_scoped_counts():
    import inspect
    src = inspect.getsource(oh._compute_summary)
    assert '_governed_asset_counts(n_elements, mgr, as_of_time)' in src
    gsrc = inspect.getsource(oh._governed_asset_counts)
    assert 'classifications=GOVERNANCE_CLASSIFICATIONS, strict=True' in gsrc
    assert 'classifications=_SUBSTANTIVE_GOVERNANCE, strict=True' in gsrc


def test_governed_unmeasured_is_none_not_zero():
    out = oh._asset_scoped_governed({}, None, None)
    assert out["governedCount"] is None and out["governedCapped"] is None
    assert out["fullyGoverned"] is None and out["partialZoneOnly"] is None
    # fully known but governed not: zone-only cannot be derived
    assert oh._asset_scoped_governed({}, None, 3)["partialZoneOnly"] is None


def test_governed_real_zero_stays_zero():
    out = oh._asset_scoped_governed({}, 0, 0)
    assert out["governedCount"] == 0 and out["fullyGoverned"] == 0 and out["partialZoneOnly"] == 0
    assert out["governedCapped"] is False


def test_governed_failed_strict_count_is_none():
    assert om.count_elements(_FailingMgr(), "Asset", classifications=om.GOVERNANCE_CLASSIFICATIONS, strict=True) is None
