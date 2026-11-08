# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests: the Overview copes with odpi/egeria-python #555, where a count whose find
fallback stops at its page cap is None ("not measured"), never the cap.

Before #555 a capped fallback returned 500 and the Overview showed it as a total. After it,
count_elements (strict or not) and count_relationships return None for a capped page, and
growth_series' points are strict. These tests drive the handler's own code paths with a
client whose every page comes back full, and check that the Overview's payload carries None
-- never 500, never 0 -- and still builds (no TypeError on a None in arithmetic).

Skipped on a pyegeria without #555 (no `recording_unmeasured`), where a capped count is
still the cap. Run where pyegeria and fastapi are importable:

    python -m pytest test_overview_capped_counts.py -q
"""
import json

import pytest

import overview_handler as oh
from pyegeria.view import overview_metrics as om

pytestmark = pytest.mark.skipif(not hasattr(om, "recording_unmeasured"),
                                reason="installed pyegeria predates #555 (capped count is still the cap)")

CAP = om.DEFAULT_CAP


def _full_page(prefix, size):
    return [{"elementHeader": {"guid": f"{prefix}-{i}", "type": {"typeName": "CSVFile"}}, "guid": f"{prefix}-{i}"}
            for i in range(size)]


class _CappedMgr:
    """A catalog bigger than any page: every find fills the page it asked for."""
    platform_url, view_server = "http://x", "s"

    def find_metadata_elements(self, body):
        return _full_page(body.get("metadataElementTypeName") or "el", body.get("pageSize") or CAP)


class _CappedCE:
    def get_relationships(self, relationship_type=None, **kw):
        return [{"relationshipHeader": {"guid": f"r-{i}"}} for i in range(CAP)]


@pytest.fixture(autouse=True)
def _no_native_counts(monkeypatch):
    # no native count method: the find fallback (and its cap) decides the outcome
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: None)


# The cap belongs to the viewer find fallback; from 6.2.27 an unscoped count is the repository's, which
# has no fallback at all (see the last test). So the cap is exercised with population="viewer".
VIEWER = {"population": "viewer"}


def test_capped_counts_are_none_not_the_cap():
    assert om.count_elements(_CappedMgr(), "SurveyReport", **VIEWER) is None   # non-strict
    assert om.count_elements(_CappedMgr(), "Asset", strict=True, **VIEWER) is None
    assert om.count_relationships(_CappedCE(), "AttachedRating", **VIEWER) is None
    # the default population (repository from 6.2.27) is never the cap either
    assert om.count_elements(_CappedMgr(), "SurveyReport") is None
    assert om.count_relationships(_CappedCE(), "AttachedRating") is None


def test_capped_count_records_its_lower_bound():
    with om.recording_unmeasured() as notes:
        om.count_elements(_CappedMgr(), "Asset", strict=True, **VIEWER)
    assert notes and notes[0]["at_least"] == CAP


def test_unscoped_count_without_native_is_noted_not_guessed():
    with om.recording_unmeasured() as notes:
        value = om.count_elements(_CappedMgr(), "Asset", strict=True)
    assert value is None and notes            # a note says why, whichever population is the default


def test_feedback_tally_with_capped_relationship_pages():
    fb = oh._feedback_counts(_CappedCE())
    assert set(fb["byType"].values()) == {None}
    assert fb["total"] is None and len(fb["unmeasured"]) == 5


def test_survey_coverage_never_reports_the_cap():
    out = oh._survey_coverage(_CappedMgr(), _CappedCE(), None, None)
    assert out["surveyReports"] is None                      # was 500 before #555
    assert out["dataStoreTotal"] is None                     # capped store page -> count_elements -> None
    json.dumps(out, default=str)


def test_growth_with_capped_counts_keeps_gaps(monkeypatch):
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: _CappedMgr())
    payload = oh._compute_growth("30d", 3, "http://x", "s", "u", "p")
    series = payload["series"]
    assert series and all(p["assets"] is None for p in series)    # strict in #555: a gap, never 500
    assert all(p[k] != CAP for p in series for k in ("assets", "terms", "governed", "products"))
    json.dumps(payload, default=str)                                # the route can serialise it
