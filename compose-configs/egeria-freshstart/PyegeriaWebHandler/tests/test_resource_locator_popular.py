# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator usage readings, freshstart copy (PO-27F; parity with the quickstart's PO-27).

Egeria's open-lineage data-scope governance service keeps usage readings in the additionalProperties
of a resource's DataScope classification. The PO-27 P0 read-only check (the quickstart, 2026-11-27,
pyegeria 6.3.4) found the DataScope at elementHeader.dataScope on every element and every reading as a
string; tests/fixtures/po27_datascope_usage_quickstart_2026_11_27.json is that scrubbed fixture, copied
from the quickstart tests. No live read is made here.

Pinned here (honest-data rules, design-docs/popularity-and-usage-measures.md §5):
  - _usage reads the DataScope in either header form and parses numbers; no usage keys gives None,
    never zeros;
  - Popular ranks by readsPerDay, then readCount (else readsInWindow), then name; a resource without
    readings is not ranked; a measured 0 stays 0; "no usage on this platform" and "the read failed"
    are different answers;
  - on the fixture, freshstart's `popular` equals the quickstart's (when the quickstart copy is beside it).

Functions are extracted with ast and run without pyegeria or FastAPI, as in the quickstart's tests."""
import ast
import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLER = _HERE.parent / "resource_browser_handler.py"
_FIXTURE = _HERE / "fixtures" / "po27_datascope_usage_quickstart_2026_11_27.json"
_QUICKSTART_HANDLER = _HERE.parents[2] / "egeria-quickstart" / "PyegeriaWebHandler" / "resource_browser_handler.py"
_FUNCS = {"_type_names", "_display_name", "_classifications", "_data_scope", "_usage_number", "_usage",
          "_iso_time", "_popular"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_USAGE_COUNTS", "_USAGE_RATES", "_USAGE_TEXTS", "_POPULAR_SHOWN",
           "_POPULAR_NONE", "_POPULAR_SOURCE"}


def _extract(path: Path, funcs: set, consts: set) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in funcs)
             or (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in consts)]
    assert {n.name for n in nodes if isinstance(n, ast.FunctionDef)} == funcs
    ns = {"Optional": Optional, "re": re, "datetime": datetime, "timezone": timezone}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), ns)
    return ns


@pytest.fixture(scope="module")
def rb():
    return _extract(_HANDLER, _FUNCS, _CONSTS)


def _scope_cls(readings=None, **dims):
    props = {"class": "DataScopeProperties", "typeName": "DataScope", **dims}
    if readings is not None:
        props["additionalProperties"] = readings
    return {"class": "ElementClassification", "classificationName": "DataScope",
            "classificationOrigin": "ASSIGNED", "type": {"typeName": "DataScope"},
            "classificationProperties": props}


def _el(guid, readings=None, *, form="header", type_name="DeployedDatabaseSchema", name=None, qn=None, extra_cls=None):
    """An element as get_elements_by_classification returns it; the DataScope in the header form P0 saw
    (elementHeader.dataScope) or in the classifications list. readings=... means no DataScope at all."""
    hdr = {"class": "ElementHeader", "guid": guid, "type": {"typeName": type_name, "superTypeNames": ["Asset"]}}
    if readings is not ...:
        if form == "header":
            hdr["dataScope"] = _scope_cls(readings)
        else:
            hdr["classifications"] = [_scope_cls(readings)]
    if extra_cls:
        hdr.update(extra_cls)
    props = {"qualifiedName": qn or f"qn::{guid}"}
    if name:
        props["displayName"] = name
    return {"elementHeader": hdr, "properties": props}


def _fixture():
    return json.loads(_FIXTURE.read_text())["elements"]


def _fixture_elements():
    return [_el(e["guid"], e["usage"], type_name=e["typeName"], qn=e["qualifiedName"]) for e in _fixture()]


# ── F1: _usage ────────────────────────────────────────────────────────────────

def test_usage_reads_the_fixture_and_parses_numbers(rb):
    schema, topic = _fixture_elements()
    u = rb["_usage"](schema)
    assert u["readCount"] == 258 and isinstance(u["readCount"], int)
    assert u["readsPerDay"] == pytest.approx(86.36) and isinstance(u["readsPerDay"], float)
    assert u["readsInWindow"] == 266 and u["readersInWindow"] == 3
    assert u["lastReadAt"] == "2026-11-27T00:29:17.154Z"
    assert u["analysisWindowStart"] == "2026-10-28T01:36:26Z" and u["analysisWindowEnd"] == "2026-11-27T01:36:26Z"
    assert u["analysisService"] == "open-lineage-data-scope-governance-service"
    # The Topic carries only readCount and lastReadAt: measured, no per-day reading.
    assert rb["_usage"](topic) == {"readCount": 1, "lastReadAt": "2026-11-23T23:33:29.889Z"}


def test_usage_finds_the_data_scope_in_either_header_form(rb):
    readings = {"readsPerDay": "0.5", "readCount": "4"}
    in_header = rb["_usage"](_el("a", readings, form="header"))
    in_list = rb["_usage"](_el("b", readings, form="list"))
    assert in_header == in_list == {"readsPerDay": 0.5, "readCount": 4}


def test_usage_keeps_only_the_usage_keys(rb):
    u = rb["_usage"](_el("a", {"readsPerDay": "1", "lastReadByRunId": "run-7", "somethingElse": "x"}))
    assert u == {"readsPerDay": 1.0}


def test_a_data_scope_without_usage_keys_is_none_not_zeros(rb):
    assert rb["_usage"](_el("a", None)) is None              # a DataScope with no additionalProperties
    assert rb["_usage"](_el("a", {})) is None
    assert rb["_usage"](_el("a", {"lastReadByRunId": "run-7"})) is None
    assert rb["_usage"](_el("a", ...)) is None            # no DataScope at all
    assert rb["_usage"]({}) is None and rb["_usage"](None) is None
    assert rb["_usage"](_el("b", {}, form="list")) is None


def test_usage_numbers_accept_real_numbers_and_drop_unreadable_ones(rb):
    u = rb["_usage"](_el("a", {"readsPerDay": 0.25, "readCount": 7, "readsInWindow": "n/a", "readersInWindow": ""}))
    assert u == {"readsPerDay": 0.25, "readCount": 7}
    # An unreadable value is left out, never turned into 0.
    assert rb["_usage"](_el("a", {"readsPerDay": "lots"})) is None
    assert rb["_usage"](_el("a", {"readsPerDay": True, "readCount": "nan"})) is None


def test_a_measured_zero_is_kept(rb):
    u = rb["_usage"](_el("a", {"readsPerDay": "0", "readCount": "0"}))
    assert u == {"readsPerDay": 0.0, "readCount": 0}


def test_data_scope_already_reads_the_header_form(rb):
    """F0: freshstart's _classifications scans every header key (the same code as the quickstart's), so
    _data_scope already sees elementHeader.dataScope: no header-form fix is needed."""
    hdr = _el("a", {"readsPerDay": "2"})["elementHeader"]
    assert rb["_data_scope"](rb["_classifications"](hdr))["additionalProperties"] == {"readsPerDay": "2"}
    hdr2 = _el("b", {"readsPerDay": "2"}, form="list")["elementHeader"]
    assert rb["_data_scope"](rb["_classifications"](hdr2))["additionalProperties"] == {"readsPerDay": "2"}


# ── F2: the Popular tile ──────────────────────────────────────────────────────

def _measured(guid, per_day=None, name=None, **more):
    r = {} if per_day is None else {"readsPerDay": str(per_day)}
    r.update({k: str(v) for k, v in more.items()})
    return _el(guid, r, name=name or guid)


def test_popular_ranks_the_fixture_and_shows_the_as_of(rb):
    p = rb["_popular"](_fixture_elements())
    assert p["available"] is True and p["measure"] == "readsPerDay"
    assert [r["guid"] for r in p["ranking"]] == ["9bb418d9-0001-4557-902c-7f1141d901dc"]
    top = p["ranking"][0]
    assert top["usage"]["readsPerDay"] == pytest.approx(86.36)
    assert top["lastRead"] == "2026-11-27T00:29:17.154Z"
    assert p["asOf"] == "2026-11-27T01:36:26Z"
    assert p["window"] == {"start": "2026-10-28T01:36:26Z", "end": "2026-11-27T01:36:26Z"}
    # The Topic was measured (readCount 1) but has no reads/day: listed apart, never ranked as 0.
    assert [r["guid"] for r in p["unranked"]] == ["7d9391d0-2d92-4992-8088-fd79aa54594a"]
    assert p["unranked"][0]["usage"] == {"readCount": 1, "lastReadAt": "2026-11-23T23:33:29.889Z"}
    assert p["measured"] == 2 and p["notMeasured"] == 0
    assert "DataScope" in p["source"]


def test_popular_has_the_quickstart_json_shape(rb):
    p = rb["_popular"](_fixture_elements())
    assert {"available", "ranking", "asOf", "window", "measure", "source"} <= set(p)
    assert set(p) == {"available", "ranking", "unranked", "shown", "measured", "asOf", "window",
                      "measure", "capped", "notMeasured", "source"}
    assert set(p["ranking"][0]) == {"guid", "typeName", "displayName", "qualifiedName", "usage", "lastRead"}


def test_popular_equals_the_quickstart_handlers_on_the_fixture(rb):
    """The same fixture through both handlers' _popular gives the same JSON (skipped when the quickstart
    copy is not beside this one, e.g. a container holding only the freshstart folder)."""
    if not _QUICKSTART_HANDLER.exists():
        pytest.skip(f"{_QUICKSTART_HANDLER} not present")
    qs = _extract(_QUICKSTART_HANDLER, _FUNCS, _CONSTS)
    els = _fixture_elements()
    assert json.dumps(rb["_popular"](els), sort_keys=True) == json.dumps(qs["_popular"](els), sort_keys=True)
    none = [_el("a", None), _el("b", {})]
    assert rb["_popular"](none) == qs["_popular"](none)
    many = [_measured(f"g{i:02d}", i % 4, readCount=i) for i in range(14)]
    assert rb["_popular"](many, capped=True) == qs["_popular"](many, capped=True)


def test_popular_sort_is_reads_per_day_then_read_count_else_reads_in_window_then_name(rb):
    els = [_measured("a", 1.5, name="Zed", readCount=3),
           _measured("b", 1.5, name="Alpha", readCount=9),
           _measured("c", 1.5, name="beta", readsInWindow=9),     # no readCount: readsInWindow breaks the tie
           _measured("d", 1.5, name="Able", readsInWindow=5),
           _measured("e", 4, name="Most"),
           _measured("f", 0, name="Measured zero", readCount=0),
           _measured("g", 1.5, name="Aardvark")]                  # neither count: after the others at 1.5
    p = rb["_popular"](els)
    # 4/day first; at 1.5/day: 9 (Alpha before beta by name), 5, 3, then no count; the measured 0 last.
    assert [r["guid"] for r in p["ranking"]] == ["e", "b", "c", "d", "a", "g", "f"]


def test_a_resource_without_readings_is_not_measured_and_never_ranked(rb):
    els = [_measured("a", 2), _el("b", None), _el("c", {}), _el("d", {"lastReadByRunId": "r"})]
    p = rb["_popular"](els)
    assert [r["guid"] for r in p["ranking"]] == ["a"]
    assert p["unranked"] == [] and p["notMeasured"] == 3 and p["measured"] == 1


def test_a_measured_zero_is_ranked_as_zero_not_dropped(rb):
    p = rb["_popular"]([_measured("z", 0, readCount=0)])
    assert p["available"] is True
    assert p["ranking"][0]["usage"]["readsPerDay"] == 0.0


def test_no_usage_anywhere_says_popularity_is_not_available_yet(rb):
    p = rb["_popular"]([_el("a", None), _el("b", {})])
    assert p["available"] is False
    assert p["reason"] == "Popularity not available yet: no usage readings on this platform"
    assert p["notMeasured"] == 2 and "ranking" not in p
    assert rb["_popular"]([])["available"] is False


def test_all_are_kept_and_ten_are_shown(rb):
    p = rb["_popular"]([_measured(f"g{i:02d}", i) for i in range(14)])
    assert len(p["ranking"]) == 14 and p["shown"] == 10
    assert p["ranking"][0]["guid"] == "g13"


def test_last_read_falls_back_to_last_read_in_window(rb):
    p = rb["_popular"]([_measured("a", 1, lastReadInWindow="2026-11-20T00:00:00Z")])
    assert p["ranking"][0]["lastRead"] == "2026-11-20T00:00:00Z"
    p = rb["_popular"]([_measured("a", 1)])
    assert p["ranking"][0]["lastRead"] is None


def test_as_of_is_the_latest_analysis_window_end(rb):
    p = rb["_popular"]([_measured("a", 1, analysisWindowStart="2026-10-01T00:00:00Z", analysisWindowEnd="2026-10-31T00:00:00Z"),
                        _measured("b", 2, analysisWindowStart="2026-10-28T01:36:26Z", analysisWindowEnd="2026-11-27T01:36:26Z")])
    assert p["asOf"] == "2026-11-27T01:36:26Z"
    assert p["window"] == {"start": "2026-10-28T01:36:26Z", "end": "2026-11-27T01:36:26Z"}
    # No window recorded at all: the as-of is unknown (None), never invented.
    p = rb["_popular"]([_measured("a", 1)])
    assert p["asOf"] is None and p["window"] is None


def test_templates_and_repeats_are_left_out(rb):
    tmpl = {"template": {"class": "ElementClassification", "classificationName": "Template", "classificationProperties": {}}}
    p = rb["_popular"]([_measured("a", 1), _measured("a", 1), _el("t", {"readsPerDay": "9"}, extra_cls=tmpl)])
    assert [r["guid"] for r in p["ranking"]] == ["a"]


def test_a_capped_read_is_said(rb):
    p = rb["_popular"]([_measured("a", 1)], capped=True)
    assert p["capped"] is True
    p = rb["_popular"]([_el("a", None)], capped=True)
    assert p["available"] is False and p["capped"] is True


# ── F2: home() returns `popular`; a failed read says it failed ────────────────

class _FakeClient:
    def __init__(self, scoped=None, fail=False):
        self.scoped, self.fail, self.classification_calls = scoped or [], fail, []

    async def _async_get_elements(self, type_name, **kw):
        return "No elements found"

    async def _async_get_elements_by_classification(self, name, start_from=0, page_size=200, **kw):
        self.classification_calls.append((name, start_from, page_size))
        if self.fail:
            raise RuntimeError("platform unavailable")
        return self.scoped[start_from:start_from + page_size] or "No elements found"


async def _coro(v):
    return v


def _home(monkeypatch, client):
    import resource_browser_handler as mod
    monkeypatch.setattr(mod, "_explorer_async", lambda: _coro(client))
    mod._cache.clear()
    return json.loads(asyncio.run(mod.home()).body)


def test_home_returns_popular_from_the_data_scope_read(monkeypatch):
    client = _FakeClient(_fixture_elements())
    d = _home(monkeypatch, client)
    assert d["popular"]["available"] is True
    assert d["popular"]["ranking"][0]["guid"] == "9bb418d9-0001-4557-902c-7f1141d901dc"
    assert d["popular"]["asOf"] == "2026-11-27T01:36:26Z"
    assert client.classification_calls[0] == ("DataScope", 0, 200)
    assert "readAt" in d["popular"]
    assert d["recent"] == []                       # the recently changed part is unaffected


def test_home_popular_is_cached_with_the_existing_ttl():
    import inspect
    import resource_browser_handler as mod
    src = inspect.getsource(mod._home_popular)
    assert 'await _cached("popular", read)' in src and "_classified(client, \"DataScope\")" in src
    assert mod._CACHE_TTL == 600


def test_home_says_when_no_resource_carries_usage(monkeypatch):
    pop = _home(monkeypatch, _FakeClient([_el("a", None)]))["popular"]
    assert pop["available"] is False and not pop.get("failed")
    assert pop["reason"] == "Popularity not available yet: no usage readings on this platform"


def test_home_says_a_failed_popularity_read_failed_and_still_serves_recent(monkeypatch):
    d = _home(monkeypatch, _FakeClient(fail=True))
    pop = d["popular"]
    assert pop["available"] is False and pop["failed"] is True
    assert "could not be read" in pop["reason"]
    assert pop["reason"] != "Popularity not available yet: no usage readings on this platform"
    assert "ranking" not in pop
    assert d["recent"] == []


# ── F3: search and browse rows carry usage; the order is unchanged ────────────

def _resource(guid, name, readings=..., desc=""):
    e = _el(guid, readings, type_name="RelationalTable", name=name)
    e["elementHeader"]["type"]["superTypeNames"] = ["SchemaAttribute"]
    e["properties"]["description"] = desc
    return e


def test_rows_carry_usage_from_the_data_scope():
    import resource_browser_handler as mod
    measured = mod._row(_resource("a", "orders", {"readsPerDay": "2.5", "readCount": "10"}))
    zero = mod._row(_resource("z", "zeros", {"readsPerDay": "0"}))
    bare = mod._row(_resource("b", "orders_bare", {}))
    none = mod._row(_resource("n", "orders_none"))
    assert measured["usage"] == {"readsPerDay": 2.5, "readCount": 10}
    assert zero["usage"] == {"readsPerDay": 0.0}              # measured 0, kept
    assert bare["usage"] is None and none["usage"] is None     # not measured, never zeros
    assert "usage" in none                                     # every row carries the key


def test_the_row_gains_only_the_usage_fields():
    """F3 and F3b: freshstart's row gains `usage` and `usageRead` only (no hasScope or scopeRead added)."""
    import resource_browser_handler as mod
    r = mod._row(_resource("a", "orders", {"readsPerDay": "1"}))
    assert set(r) == {"guid", "typeName", "kind", "displayName", "qualifiedName", "description", "owner", "badges",
                      "dataScope", "usage", "usageRead", "updatedBy", "updateTime", "automated", "matched"}
    assert "scopeRead" not in r and "hasScope" not in r


def test_search_order_is_unchanged_by_usage():
    """Ordering stays text relevance (_relevance); usage is shown only. Rows with readings that would
    reverse the order if usage were used still come out in relevance order."""
    import resource_browser_handler as mod
    rows = [mod._row(_resource("1", "sales orders", {"readsPerDay": "99"}, desc="")),
            mod._row(_resource("2", "orders", {"readsPerDay": "0.1"})),
            mod._row(_resource("3", "orders archive")),
            mod._row(_resource("4", "x", {"readsPerDay": "50"}, desc="has orders in it"))]
    with_usage = sorted(rows, key=lambda r: mod._relevance(r, "orders"))
    without = sorted([{**r, "usage": None} for r in rows], key=lambda r: mod._relevance(r, "orders"))
    assert [r["guid"] for r in with_usage] == [r["guid"] for r in without] == ["2", "3", "1", "4"]
    import inspect
    assert "usage" not in inspect.getsource(mod._relevance)
    assert "items.sort(key=lambda r: _relevance(r, q))" in inspect.getsource(mod.search)


def test_order_note_says_usage_is_shown_not_used():
    import resource_browser_handler as mod
    assert mod._ORDER_NOTE == "Ordered by text relevance. Usage is shown, not used for ordering."
    assert "no usage measure" not in _HANDLER.read_text()


# ── F3b: usageRead says whether the row's classifications were read ──────────

def _unread(guid, name):
    """A resource as a source returns it without classifications: the header carries no ElementClassification."""
    e = _resource(guid, name)
    assert not any(isinstance(v, dict) and v.get("class") == "ElementClassification"
                   for v in e["elementHeader"].values())
    return e


def _anchored(guid, name, readings=..., form="header"):
    """A resource read with its classifications: Anchors (every resource has it) and, optionally, a DataScope."""
    e = _resource(guid, name, readings)
    if readings is not ... and form == "list":
        e["elementHeader"]["classifications"] = [e["elementHeader"].pop("dataScope")]
    e["elementHeader"]["anchor"] = {"class": "ElementClassification", "classificationName": "Anchors",
                                    "classificationProperties": {"anchorGUID": guid}}
    return e


def test_usage_read_is_true_when_classifications_came_with_the_element():
    import resource_browser_handler as mod
    measured = mod._row(_anchored("a", "orders", {"readsPerDay": "2"}))
    not_measured = mod._row(_anchored("b", "orders_bare"))          # read, and no DataScope: "not measured"
    in_list = mod._row(_anchored("c", "orders_list", {"readsPerDay": "1"}, form="list"))
    scope_only = mod._row(_resource("d", "orders_scope", {}))       # the DataScope itself is a classification read
    assert measured["usageRead"] is True and measured["usage"] == {"readsPerDay": 2.0}
    assert not_measured["usageRead"] is True and not_measured["usage"] is None
    assert in_list["usageRead"] is True and in_list["usage"] == {"readsPerDay": 1.0}
    assert scope_only["usageRead"] is True


def test_usage_read_is_false_when_classifications_were_not_read():
    import resource_browser_handler as mod
    r = mod._row(_unread("u", "orders_unread"))
    assert r["usageRead"] is False
    assert r["usage"] is None          # the page shows "usage not read" for this row, never "not measured"
    assert mod._row({"elementHeader": {"guid": "v", "type": {"typeName": "RelationalTable",
                                                             "superTypeNames": ["SchemaAttribute"]},
                                       "classifications": []},
                     "properties": {"displayName": "empty list"}})["usageRead"] is False


def test_usage_read_does_not_change_the_search_order():
    import resource_browser_handler as mod
    rows = [mod._row(_unread("1", "sales orders")), mod._row(_anchored("2", "orders", {"readsPerDay": "0.1"})),
            mod._row(_anchored("3", "orders archive"))]
    flipped = [{**r, "usageRead": not r["usageRead"]} for r in rows]
    assert ([r["guid"] for r in sorted(rows, key=lambda r: mod._relevance(r, "orders"))]
            == [r["guid"] for r in sorted(flipped, key=lambda r: mod._relevance(r, "orders"))] == ["2", "3", "1"])
