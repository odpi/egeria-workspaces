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
    src = inspect.getsource(oh.get_summary)
    for needle in ('count_elements(mgr, "Asset", as_of_time, strict=True)',
                   'count_elements(mgr, "GlossaryTerm", as_of_time, strict=True)',
                   'count_elements(mgr, "DigitalProduct", as_of_time, strict=True)',
                   "counts_by_type(mgr, _ASSET_TYPES, as_of_time, strict=True)"):
        assert needle in src, needle
    assert "strict=True" in inspect.getsource(oh.get_people)
    assert "strict=True" in inspect.getsource(oh.get_usage_context)


# ── funnel: a measured 0 stays 0 ─────────────────────────────────────────────

def test_pyegeria_funnel_turns_zero_into_none_which_the_handler_corrects():
    # pyegeria's `count or None`: a measured 0 is reported as None
    raw = om.context_readiness_funnel(_EmptyMgr(), _ZeroCE())
    assert raw["cataloged"] is None and raw["classified"] is None
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
    # pyegeria's own summary reports the same failure as "0 items of feedback"
    assert om.feedback_summary(_FailingCE())["total"] == 0


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
    assert failed["assetTotal"] == 0          # pyegeria: failure looks like an empty catalog
    out = oh._reconcile_business_value(failed, None, None)
    assert out["assetTotal"] is None and out["confidentialCount"] is None and out["describedCount"] is None


def test_business_value_real_empty_catalog_stays_zero():
    empty = om.business_value_signals(_EmptyMgr())
    out = oh._reconcile_business_value(empty, 0, 0)
    assert out["assetTotal"] == 0 and out["confidentialCount"] == 0 and out["duplicateCount"] == 0


def test_business_value_duplicate_count_is_the_strict_one():
    out = oh._reconcile_business_value({"assetTotal": 5, "duplicateCount": 0}, 5, None)
    assert out["duplicateCount"] is None


def test_governed_failed_find_is_not_a_zero():
    failed = om.governed_coverage(_FailingMgr())
    assert failed["governedCount"] == 0
    out = oh._reconcile_governed(failed, None)
    assert out["governedCount"] is None and out["byClassification"] is None


def test_governed_real_zero_stays_zero():
    empty = om.governed_coverage(_EmptyMgr())
    assert oh._reconcile_governed(empty, 0)["governedCount"] == 0
