# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator usage readings and the Home "Popular" tile (PO-27; Dan, 2026-11-27).

Egeria's open-lineage data-scope governance service keeps usage readings in the additionalProperties
of a resource's DataScope classification. The P0 read-only check (Rocky quickstart, 2026-11-27,
erinoverview, pyegeria 6.3.4) found the DataScope at elementHeader.dataScope on all 126 elements and
every reading as a string; tests/fixtures/po27_datascope_usage_rocky_2026_11_27.json holds the two
elements that carried usage, scrubbed to the usage keys.

Pinned here (honest-data rules, design-docs/popularity-and-usage-measures.md §5):
  - _usage reads the DataScope in either header form and parses numbers; no usage keys gives None,
    never zeros;
  - Popular ranks by readsPerDay, then readCount (else readsInWindow), then name; a resource without
    readings is not ranked; a measured 0 stays 0; "no usage on this platform" and "the read failed"
    are different answers.

Quickstart only: the freshstart copy is stale (BACKLOG "Mirror egeria-freshstart"). Functions are
extracted with ast and run without pyegeria or FastAPI, as in test_resource_browser.py."""
import ast
import json
import re
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLER = _HERE.parent / "resource_browser_handler.py"
_FIXTURE = _HERE / "fixtures" / "po27_datascope_usage_rocky_2026_11_27.json"
_FUNCS = {"_type_names", "_display_name", "_classifications", "_data_scope", "_has_scope", "_usage_number", "_usage"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_USAGE_COUNTS", "_USAGE_RATES", "_USAGE_TEXTS"}


@pytest.fixture(scope="module")
def rb():
    tree = ast.parse(_HANDLER.read_text(encoding="utf-8"))
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in _FUNCS)
             or (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _CONSTS)]
    assert {n.name for n in nodes if isinstance(n, ast.FunctionDef)} == _FUNCS
    from datetime import datetime
    ns = {"Optional": Optional, "re": re, "datetime": datetime}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(_HANDLER), "exec"), ns)
    return ns


def _scope_cls(readings=None, **dims):
    props = {"class": "DataScopeProperties", "typeName": "DataScope", **dims}
    if readings is not None:
        props["additionalProperties"] = readings
    return {"class": "ElementClassification", "classificationName": "DataScope",
            "classificationOrigin": "ASSIGNED", "type": {"typeName": "DataScope"},
            "classificationProperties": props}


def _el(guid, readings=None, *, form="header", type_name="DeployedDatabaseSchema", name=None, qn=None, extra_cls=None):
    """An element as get_elements_by_classification returns it; the DataScope in the header form P0 saw
    (elementHeader.dataScope) or in the classifications list."""
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


# ── P1: _usage ────────────────────────────────────────────────────────────────

def test_usage_reads_the_p0_fixture_and_parses_numbers(rb):
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


def test_usage_numbers_accept_real_numbers_and_drop_unreadable_ones(rb):
    u = rb["_usage"](_el("a", {"readsPerDay": 0.25, "readCount": 7, "readsInWindow": "n/a", "readersInWindow": ""}))
    assert u == {"readsPerDay": 0.25, "readCount": 7}
    # An unreadable value is left out, never turned into 0.
    assert rb["_usage"](_el("a", {"readsPerDay": "lots"})) is None


def test_a_measured_zero_is_kept(rb):
    u = rb["_usage"](_el("a", {"readsPerDay": "0", "readCount": "0"}))
    assert u == {"readsPerDay": 0.0, "readCount": 0}


def test_data_scope_still_reads_the_header_form_and_has_scope_is_unchanged(rb):
    """P0: _classifications scans every header key, so _data_scope already sees elementHeader.dataScope.
    _has_scope still treats a scope holding only usage readings as no dimension."""
    hdr = _el("a", {"readsPerDay": "2"})["elementHeader"]
    scope = rb["_data_scope"](rb["_classifications"](hdr))
    assert scope["additionalProperties"] == {"readsPerDay": "2"}
    assert rb["_has_scope"](scope) is False
    hdr2 = _el("b", {"readsPerDay": "2"})["elementHeader"]
    hdr2["dataScope"]["classificationProperties"]["dataCollectionStartTime"] = "2026-01-01T00:00:00Z"
    assert rb["_has_scope"](rb["_data_scope"](rb["_classifications"](hdr2))) is True
