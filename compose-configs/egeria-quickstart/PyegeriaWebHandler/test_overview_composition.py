# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests for /api/overview/composition (pyegeria asset_composition behind the background section cache).
The routine's result is a fake, so nothing here talks to Egeria. They pin:
  * cold -> {"loading": true}, then the rows; failures keep the "not measured" words;
  * repository counts are served to anyone; the viewer column is the hourly Asset total ONLY (total-only);
  * a not_measured cell is never turned into a 0, and nothing_found keeps its own word;
  * "not visible to you" is derived, and only where both operands are measured;
  * the summary's byType is the routine's level-1 rows.

    python -m pytest test_overview_composition.py -q
"""
import json
import time

import pytest
from fastapi import HTTPException

import overview_handler as oh


def _cell(value, state=None, reason="", pop="repository"):
    state = state or ("measured" if value else "nothing_found")
    return {"value": value, "state": state, "completeness": "complete", "as_of": "2026-11-07T00:00:00+00:00",
            "population": pop, "reason": reason, "elapsed_s": 0.2}


def _row(name, parent, level, repo, exact=False):
    return {"type_name": name, "parent": parent, "level": level, "exact_type": exact,
            "subtypes_error": None, "repository": repo}


def _result(**over):
    r = {"state": "measured", "state_reason": "", "root": "Asset", "depth": 1, "scopes": ["repository"],
         "as_of": "2026-11-07T00:00:00+00:00", "concurrency": 3, "not_measured": [],
         "provenance": {"pyegeria_version": "6.2.23"},
         "rows": [_row("Asset", None, 0, _cell(60591)),
                  _row("DataAsset", "Asset", 1, _cell(57391)),
                  _row("Process", "Asset", 1, _cell(2984)),
                  _row("Infrastructure", "Asset", 1, _cell(210)),
                  _row("RunnableSoftwareComponent", "Asset", 1, _cell(0)),
                  _row("Asset", "Asset", 1, _cell(6, "measured"), exact=True)]}
    r.update(over)
    return r


@pytest.fixture(autouse=True)
def _state(monkeypatch):
    oh._sections.clear(); oh._section_inflight.clear()
    oh._viewer_totals.clear(); oh._viewer_inflight.clear()
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (4000, False, False, time.time() - 600))
    yield
    deadline = time.time() + 5
    while oh._section_inflight and time.time() < deadline:
        time.sleep(0.01)
    oh._sections.clear()


def _get(monkeypatch, result, root="Asset", **kw):
    calls = []
    def fake(r, d, a, *rest):
        calls.append((r, d, a)); 
        if isinstance(result, Exception):
            raise result
        return result
    monkeypatch.setattr(oh, "_compute_composition", fake)
    # first call is cold; poll until the worker has measured (or failed)
    out = oh.get_composition(root=root, depth=1, as_of_time=None, url="http://x", server="s", user_id="u", user_pwd="p")
    body = json.loads(out.body)
    assert body.get("loading") is True, "a cold request must answer at once with loading"
    deadline = time.time() + 5
    while oh._section_inflight and time.time() < deadline:
        time.sleep(0.01)
    return calls


def _again(root="Asset"):
    out = oh.get_composition(root=root, depth=1, as_of_time=None, url="http://x", server="s", user_id="u", user_pwd="p")
    return json.loads(out.body)


def test_cold_then_measured_rows_repository_scope(monkeypatch):
    calls = _get(monkeypatch, _result())
    assert calls == [("Asset", 1, None)]
    b = _again()
    assert b["countScope"] == "repository" and b["viewerCounts"] == "total-only"
    assert b["refreshSeconds"] == 3600 and b["measuredAt"]
    lvl1 = {(r["type_name"], r["exact_type"]): r for r in b["rows"] if r["level"] == 1}
    assert lvl1[("DataAsset", False)]["repository"]["value"] == 57391
    assert lvl1[("RunnableSoftwareComponent", False)]["repository"]["state"] == "nothing_found"


def test_viewer_is_total_only_and_never_a_zero(monkeypatch):
    _get(monkeypatch, _result()); b = _again()
    top = [r for r in b["rows"] if r["level"] == 0][0]
    assert top["viewer"]["value"] == 4000 and top["viewer"]["state"] == "measured"
    assert top["viewer"]["population"] == "viewer"
    for r in b["rows"]:
        if r["level"] == 1:
            assert r["viewer"]["state"] == "not_measured" and r["viewer"]["value"] is None
            assert "only the total is cached" in r["viewer"]["reason"]
            assert r["not_visible"]["state"] == "not_measured" and r["not_visible"]["value"] is None


def test_not_visible_is_derived_from_both_operands(monkeypatch):
    _get(monkeypatch, _result()); b = _again()
    top = [r for r in b["rows"] if r["level"] == 0][0]
    assert top["not_visible"]["value"] == 60591 - 4000 and top["not_visible"]["population"] == "derived"


def test_viewer_total_loading_gives_not_measured_not_zero(monkeypatch):
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (None, True, False, None))
    _get(monkeypatch, _result()); b = _again()
    top = [r for r in b["rows"] if r["level"] == 0][0]
    assert b["viewerTotalLoading"] is True
    assert top["viewer"]["state"] == "not_measured" and top["viewer"]["value"] is None
    assert top["not_visible"]["state"] == "not_measured"


def test_viewer_higher_than_repository_is_not_a_negative_count(monkeypatch):
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (70000, False, False, time.time()))
    _get(monkeypatch, _result()); b = _again()
    top = [r for r in b["rows"] if r["level"] == 0][0]
    assert top["not_visible"]["state"] == "not_measured" and top["not_visible"]["value"] is None


def test_failed_repository_cell_stays_not_measured(monkeypatch):
    bad = _result(rows=[_row("Asset", None, 0, _cell(60591)),
                        _row("Process", "Asset", 1, _cell(None, "not_measured", "timed out")),
                        _row("Asset", "Asset", 1, _cell(None, "not_measured", "a child count is missing"), exact=True)],
                  not_measured=["Process/repository"], state_reason="not measured: Process/repository")
    _get(monkeypatch, bad); b = _again()
    proc = [r for r in b["rows"] if r["type_name"] == "Process"][0]
    assert proc["repository"]["value"] is None and proc["repository"]["state"] == "not_measured"
    assert proc["repository"]["reason"] == "timed out"
    assert proc["not_visible"]["value"] is None
    assert b["not_measured"] == ["Process/repository"]


def test_non_asset_root_has_no_viewer_figure(monkeypatch):
    called = []
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: called.append(1) or (1, False, False, 0))
    _get(monkeypatch, _result(root="DataAsset"), root="DataAsset"); b = _again("DataAsset")
    assert not called                     # the cached viewer total is for Asset only
    for r in b["rows"]:
        assert r["viewer"]["state"] == "not_measured"


def test_failed_run_is_503_not_zero_filled(monkeypatch):
    _get(monkeypatch, RuntimeError("boom"))
    with pytest.raises(HTTPException) as e:
        _again()
    assert e.value.status_code == 503


def test_bad_root_is_rejected():
    with pytest.raises(HTTPException) as e:
        oh.get_composition(root="Asset; drop", depth=1, as_of_time=None, url=None, server=None, user_id=None, user_pwd=None)
    assert e.value.status_code == 422


def test_level1_rows_for_summary_keep_none_for_failures():
    res = _result(rows=_result()["rows"] + [_row("Other", "Asset", 1, _cell(None, "not_measured", "x"))])
    rows = oh._level1_rows(res)
    by = {r["label"]: r for r in rows}
    assert by["DataAsset"]["count"] == 57391
    assert by["RunnableSoftwareComponent"]["count"] == 0 and by["RunnableSoftwareComponent"]["state"] == "nothing_found"
    assert by["Asset (exactly)"]["exactType"] is True
    assert by["Other"]["count"] is None
    assert all(r["type"] != "ITInfrastructure" for r in rows)


def test_old_hand_picked_types_are_gone():
    assert not hasattr(oh, "_ASSET_TYPES") and not hasattr(oh, "_exclusive_by_type")


def test_real_routine_runs_against_a_fake_client():
    """asset_composition from the installed pyegeria, with a fake vm and mgr: repository scope only."""
    class VM:
        def get_sub_types(self, name, *a, **k):
            return {"typeDefs": [{"name": "DataAsset"}, {"name": "Process"}]} if name == "Asset" else None
    class Mgr:
        platform_url, view_server = "http://x", "s"
    import pyegeria.view.overview_metrics as om
    orig = om.count_elements
    # **kw: asset_composition passes the population keyword (population= or scope=, by version)
    om.count_elements = lambda mgr, t, as_of=None, classifications=None, strict=True, **kw: {"Asset": 10, "DataAsset": 7, "Process": 0}[t]
    try:
        res = oh.asset_composition(Mgr(), VM(), root="Asset", depth=1, scopes=("repository",))
    finally:
        om.count_elements = orig
    view = oh._composition_view(res, (5, False, False, time.time()))
    cells = {(r["type_name"], r["exact_type"]): r for r in view["rows"]}
    assert cells[("Process", False)]["repository"]["state"] == "nothing_found"
    assert cells[("Asset", True)]["repository"]["value"] == 3       # 10 - 7 - 0
    assert cells[("Asset", False)]["not_visible"]["value"] == 5
