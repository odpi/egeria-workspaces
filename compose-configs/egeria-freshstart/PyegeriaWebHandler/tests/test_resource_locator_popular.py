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
    never zeros.

Functions are extracted with ast and run without pyegeria or FastAPI, as in the quickstart's tests."""
import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLER = _HERE.parent / "resource_browser_handler.py"
_FIXTURE = _HERE / "fixtures" / "po27_datascope_usage_quickstart_2026_11_27.json"
_FUNCS = {"_type_names", "_display_name", "_classifications", "_data_scope", "_usage_number", "_usage"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_USAGE_COUNTS", "_USAGE_RATES", "_USAGE_TEXTS"}


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
