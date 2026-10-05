# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""_recent_changes() reads changes to curated content types, and must stay honest about its window.

Egeria's most-recently-updated elements are dominated by connector churn, so activity is read per curated
type. The function pages each type (newest first) until an element is older than the window, splits people
from automation, and returns None -- never a half-read list -- if any query failed. A type still inside the
window after the page limit makes the counts a lower bound (`capped`).

The functions are extracted from each handler file (quickstart and freshstart carry identical copies) and
run against a fake manager, without importing pyegeria or FastAPI.
"""
import ast
import datetime as dt
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLERS = {
    "quickstart": _HERE.parent / "overview_handler.py",
    "freshstart": _HERE.parents[2] / "egeria-freshstart" / "PyegeriaWebHandler" / "overview_handler.py",
}
_NOW = dt.datetime(2026, 10, 5, 12, 0, 0)
_NEEDED = {"_parse_time", "_guid_of", "_looks_automated", "_element_label", "_recent_changes"}


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in _NEEDED]
    assert {n.name for n in body} == _NEEDED
    consts = [n for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id.startswith("_ACTIVITY_")]
    ns = {"Optional": Optional, "logger": type("L", (), {"debug": staticmethod(lambda *a, **k: None)})()}
    exec(compile(ast.Module(body=consts + body, type_ignores=[]), str(path), "exec"), ns)
    return ns


@pytest.fixture(params=sorted(_HANDLERS))
def ns(request):
    return _load(_HANDLERS[request.param])


def _el(guid, typ, hours_ago, actor="steward1", version=2, name="n"):
    t = (_NOW - dt.timedelta(hours=hours_ago)).strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
    return {"elementGUID": guid, "type": {"typeName": typ},
            "versions": {"updateTime": t, "updatedBy": actor, "version": version},
            "elementProperties": {"propertiesAsStrings": {"displayName": name}}}


class _Mgr:
    """Serves each type's elements newest-first, honouring startFrom/pageSize."""
    def __init__(self, by_type, fail_type=None):
        self.by_type, self.fail_type, self.calls = by_type, fail_type, []

    def find_metadata_elements(self, body):
        t = body["metadataElementTypeName"]
        self.calls.append((t, body["startFrom"], body.get("sequencingOrder")))
        if t == self.fail_type:
            raise RuntimeError("boom")
        lo = body["startFrom"]
        return self.by_type.get(t, [])[lo:lo + body["pageSize"]]


def test_splits_people_from_automation_and_counts_by_type(ns):
    m = _Mgr({"GlossaryTerm": [_el("a", "GlossaryTerm", 1, "erinoverview"), _el("b", "GlossaryTerm", 5, "apicatnpa"),
                               _el("c", "GlossaryTerm", 30, "erinoverview", version=1)],
              "Collection": [_el("d", "DigitalProduct", 2, "peterprofile")]})
    out = ns["_recent_changes"](m, _NOW)
    assert out["total"] == 4 and out["automated"] == 1 and out["people"] == 3 and out["capped"] is False
    assert out["byType"] == {"GlossaryTerm": 3, "DigitalProduct": 1}
    assert out["stewards"] == [("erinoverview", 2), ("peterprofile", 1)]
    assert all(c[2] == "LAST_UPDATE_RECENT" for c in m.calls)


def test_the_stream_is_the_last_48_hours_newest_first_with_created_vs_updated(ns):
    m = _Mgr({"GlossaryTerm": [_el("a", "GlossaryTerm", 1, version=1), _el("b", "GlossaryTerm", 47),
                               _el("c", "GlossaryTerm", 49), _el("d", "GlossaryTerm", 100)]})
    out = ns["_recent_changes"](m, _NOW)
    assert [r["guid"] for r in out["recent"]] == ["a", "b"]
    assert [r["action"] for r in out["recent"]] == ["created", "updated"]
    assert out["total"] == 4                                 # 7-day window still counts the older two


def test_the_stream_lists_people_only_and_counts_automation_separately(ns):
    m = _Mgr({"GlossaryTerm": [_el("a", "GlossaryTerm", 1, "baudotnpa"), _el("b", "GlossaryTerm", 2, "baudotnpa"),
                               _el("c", "GlossaryTerm", 3, "erinoverview"), _el("d", "GlossaryTerm", 60, "baudotnpa")]})
    out = ns["_recent_changes"](m, _NOW)
    assert [r["guid"] for r in out["recent"]] == ["c"] and out["recentAutomated"] == 2   # "d" is older than 48 h
    assert all(r["automated"] is False for r in out["recent"])


def test_nothing_older_than_the_window_is_counted_and_paging_stops_there(ns):
    m = _Mgr({"GlossaryTerm": [_el("a", "GlossaryTerm", 1)] + [_el(f"o{i}", "GlossaryTerm", 24 * 8 + i) for i in range(500)]})
    out = ns["_recent_changes"](m, _NOW)
    assert out["total"] == 1 and out["capped"] is False
    assert [c for c in m.calls if c[0] == "GlossaryTerm"] == [("GlossaryTerm", 0, "LAST_UPDATE_RECENT")]   # one page


def test_a_type_still_inside_the_window_after_the_page_limit_is_a_lower_bound(ns):
    busy = [_el(f"g{i}", "GlossaryTerm", 1) for i in range(1200)]       # 6 pages of 200, all inside the window
    out = ns["_recent_changes"](_Mgr({"GlossaryTerm": busy}), _NOW)
    assert out["capped"] is True and out["total"] == 1000


def test_an_element_in_two_queried_types_is_counted_once(ns):
    m = _Mgr({"GlossaryTerm": [_el("x", "GlossaryTerm", 1)], "Collection": [_el("x", "GlossaryTerm", 1)]})
    assert ns["_recent_changes"](m, _NOW)["total"] == 1


def test_no_changes_is_a_real_zero(ns):
    out = ns["_recent_changes"](_Mgr({}), _NOW)
    assert out["total"] == 0 and out["people"] == 0 and out["recent"] == [] and out["stewards"] == [] and out["byType"] == {}


def test_a_failed_query_returns_none_not_a_partial_result(ns):
    m = _Mgr({"GlossaryTerm": [_el("a", "GlossaryTerm", 1)]}, fail_type="Project")
    assert ns["_recent_changes"](m, _NOW) is None


def test_automation_heuristic(ns):
    f = ns["_looks_automated"]
    assert f("apicatnpa") and f("EgeriaGovernanceEngine") and not f("erinoverview") and not f("") and not f(None)
