"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

RS-W2-4: the Portal shows each report spec's declarations and resolution, and refusals in the
resolver's own words. No Egeria connection: every test runs on pyegeria's registries alone (the
execute test refuses before any Egeria call).
"""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

pytest.importorskip("pyegeria.view.spec_resolver")

import analytics_registry_handler  # noqa: E402
import local_dashboards_handler  # noqa: E402
import report_specs_handler  # noqa: E402
import spec_resolution  # noqa: E402


@pytest.fixture(scope="module")
def specs():
    app = FastAPI()
    app.include_router(report_specs_handler.router)
    r = TestClient(app).get("/api/report-specs")
    assert r.status_code == 200, r.text
    return r.json()


def _by_name(specs):
    return {s["name"]: s for s in specs["specs"]}


# ── /api/report-specs ────────────────────────────────────────────────────────

def test_every_spec_has_a_resolution_and_names_are_unchanged(specs):
    from pyegeria.view.base_report_formats import get_report_registry
    assert {s["name"] for s in specs["specs"]} == set(get_report_registry().keys())
    assert all(s["resolution"] is not None for s in specs["specs"])


def test_counts_are_three_states_matching_the_resolver(specs):
    from pyegeria.view.spec_resolver import resolve_all
    res = resolve_all()
    c = specs["counts"]
    assert c["unresolved"] == 0
    assert c["runnable"] == sum(1 for r in res.values() if r.runnable)
    assert c["formatOnly"] == sum(1 for r in res.values() if not r.runnable and r.kind == "format_only")
    assert c["unrunnable"] == sum(1 for r in res.values() if not r.runnable and r.kind != "format_only")
    assert c["runnable"] + c["unrunnable"] + c["formatOnly"] == specs["total"]


def test_unrunnable_spec_carries_the_resolvers_words(specs):
    from pyegeria.view.spec_resolver import resolve_all
    spec = _by_name(specs).get("Data-Classes")
    if spec is None or resolve_all()["Data-Classes"].runnable:
        pytest.skip("Data-Classes is runnable on this pyegeria")
    r = spec["resolution"]
    assert r["status"] == "unrunnable" and r["runnable"] is False
    assert r["words"] == resolve_all()["Data-Classes"].words
    assert r["checks"] == [1]
    assert [p["name"] for p in r["params"]] == ["search_string"]  # what it needs, even unrunnable


def test_format_only_spec_is_not_unrunnable(specs):
    fo = [s for s in specs["specs"] if s["action"] is None]
    assert fo, "expected at least one format-only spec"
    r = fo[0]["resolution"]
    assert r["status"] == "format_only" and r["kind"] == "format_only"
    assert r["checks"] is None  # not counted or styled as a failure
    assert "has no action" in r["words"][0]


def test_runnable_find_spec(specs):
    s = next(s for s in specs["specs"] if s["resolution"]["kind"] == "find" and s["resolution"]["runnable"])
    r = s["resolution"]
    assert r["words"] is None and r["checks"] is None
    assert r["stages"][0]["name"] == s["action"]["function"]
    assert {p["name"] for p in r["params"] if p["required"]} == set(s["action"]["required_params"])


def test_analytic_spec_shows_inputs_param_categories_and_out(specs):
    s = next(s for s in specs["specs"]
             if s["resolution"]["kind"] == "analytic" and s["resolution"]["roleInputs"] and s["resolution"]["outFields"])
    r = s["resolution"]
    assert all(i.split(":")[0] in ("egeria_client", "reader", "viewer", "subject") for i in r["roleInputs"])
    assert r["stages"][0]["binding"].startswith("python ")
    assert {"name", "label", "type"} <= set(r["outFields"][0])
    routine_params = [p for p in r["params"] if p["stage"] == s["action"]["analytic_function"]]
    assert all(p["category"] in ("content", "shape", "performance") for p in routine_params)


def test_portal_supply_note_is_stated(specs):
    assert "viewer" in specs["portalSupply"] and "reader" in specs["portalSupply"]


# ── /api/analytics ───────────────────────────────────────────────────────────

def test_analytics_adds_declaration_keys_and_keeps_old_ones():
    app = FastAPI()
    app.include_router(analytics_registry_handler.router)
    data = TestClient(app).get("/api/analytics").json()
    f = data["functions"][0]
    for key in ("name", "function", "description", "returns", "generic", "bindingNote", "demoReportSpec", "params"):
        assert key in f
    for key in ("kind", "binding", "inputs", "outFields", "outShape"):
        assert key in f
    assert f["binding"] == f["function"]
    assert all("category" in p for fn in data["functions"] for p in fn["params"])


def test_library_shape_name_reads_as_a_shape_not_as_no_output():
    entry = SimpleNamespace(declaration=SimpleNamespace(out="CoverageResult", out_fields=lambda: []),
                            routine=lambda: SimpleNamespace(out_fields=lambda: []))
    out = spec_resolution.routine_out(entry)
    assert out["outFields"] == [] and out["outShape"] == "CoverageResult" and out["outDeclared"] is True


# ── analytic_binders marker (O1-a) ───────────────────────────────────────────

def test_binders_tag_keys_on_the_stable_prefix():
    prefix = spec_resolution.binders_prefix()
    assert prefix.startswith("deprecated: analytic_binders ignored")
    assert spec_resolution.has_binders_warning([prefix + " (binders for: mgr); declare these ..."])
    assert not spec_resolution.has_binders_warning(["check 2: optional parameter x is not accepted"])
    assert not spec_resolution.has_binders_warning(None)


# ── /api/local-dashboards/{name}: a placement on an unrunnable spec ──────────

def _placement(ref):
    return SimpleNamespace(ref=ref, span=1, emphasis="kpi", perspectives=[], content=None)


def _report(spec):
    return {"guid": "g", "heading": "H", "description": "", "reportSpec": spec, "outputFormat": "DICT",
            "analyticParams": {}, "params": {}}


def test_placement_on_unrunnable_spec_carries_refusal(monkeypatch):
    fake = {"Broken": spec_resolution_unrunnable("Broken"),
            "Fine": SimpleNamespace(runnable=True, kind="find", words=[], warnings=[])}
    monkeypatch.setattr(local_dashboards_handler, "_find_report_by_name",
                        lambda ref, *a, **k: _report({"tile-broken": "Broken", "tile-fine": "Fine",
                                                      "tile-unknown": "Nope"}[ref]))
    registry = {"Broken": SimpleNamespace(action=None, formats=[], description="", family=None),
                "Fine": SimpleNamespace(action=None, formats=[], description="", family=None)}
    ser = lambda ref: local_dashboards_handler._serialize_placement(_placement(ref), {}, registry, object(),
                                                                    resolutions=fake)
    broken = ser("tile-broken")
    assert broken["kind"] == "report" and broken["runnable"] is False
    assert broken["refusal"] == "Spec 'Broken' cannot run (check 1): its find method does not exist."
    fine = ser("tile-fine")
    assert fine["runnable"] is True and fine["refusal"] is None
    unknown = ser("tile-unknown")  # not resolved: unknown, never "runnable"
    assert unknown["runnable"] is None and unknown["refusal"] is None


def spec_resolution_unrunnable(name):
    return SimpleNamespace(runnable=False, kind="find", checks=[1], warnings=[],
                           words=[f"Spec '{name}' cannot run (check 1): its find method does not exist."])


# ── /api/report-specs/execute: 400 with the words ────────────────────────────

def test_execute_refusal_is_400_with_the_words(monkeypatch):
    import pyegeria.view.format_set_executor as fse
    words = "Routine 'x' cannot run: the Portal supplies no reader:ods."
    monkeypatch.setattr(fse, "exec_report_spec", lambda *a, **k: (_ for _ in ()).throw(ValueError(words)))
    app = FastAPI()
    app.include_router(report_specs_handler.router)
    r = TestClient(app).post("/api/report-specs/execute",
                             json={"spec_name": "Anything", "output_format": "DICT"})
    assert r.status_code == 400, r.text
    assert r.json()["detail"] == words
