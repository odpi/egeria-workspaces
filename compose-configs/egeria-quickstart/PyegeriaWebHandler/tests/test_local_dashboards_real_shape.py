"""Portal-2 (the resolver refactor): the live sheets are the oracle.

fixtures/local_dashboards_real_shape_2026_11_12.json was captured read-only from laz's Egeria: every sheet the
Portal serves as pyegeria's reader returns it (all nine are held in Egeria, the Chief Data Officer sheet too; the
five in the Portal's consumer folder are the same five Egeria Advisor's holds), the Report elements their
placements link to, the Chief Data Officer sheet from the Portal's local store with the raw by-name Report
searches its placements make, the registry/resolution facts of every spec named, and what GET
/api/local-dashboards/{name} returned for each (byte-identical before and after the refactor). Here those inputs
are replayed through the handler and the REAL pyegeria resolver, and the answer must equal what the Portal served.
"""
import json, sys, time
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import local_dashboards_handler as ld  # noqa: E402
from result_cache import ResultCache  # noqa: E402

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "local_dashboards_real_shape_2026_11_12.json").read_text())
EGERIA = sorted(FIXTURE["egeria_sheets"])
CDO = "Chief Data Officer Dashboard"


def _registry():
    reg = {}
    for label, f in FIXTURE["specs"].items():
        a = f["action"]
        reg[label] = NS(description=f["description"], family=f["family"],
                        formats=[NS(types=t) for t in f["formats"]],
                        action=None if a is None else NS(required_params=a["required_params"],
                                                         analytic_function=a["analytic_function"]))
    return reg


def _resolutions():
    return {label: NS(runnable=f["resolution"]["runnable"], words=f["resolution"]["words"],
                      warnings=f["resolution"]["warnings"])
            for label, f in FIXTURE["specs"].items() if f["resolution"] is not None}


@pytest.fixture
def live(monkeypatch, tmp_path):
    from pyegeria.view import dashboards as dash_mod, dashboard_resolver
    from pyegeria.view._output_dashboard_sheet_models import (
        DashboardSheet, DashboardSheetDict, save_dashboard_sheets_to_json)
    store = DashboardSheetDict()
    for name, body in FIXTURE["local_sheets"].items():
        store[name] = DashboardSheet.model_validate(body)
    path = tmp_path / "sheets.json"
    save_dashboard_sheets_to_json(store, str(path))
    monkeypatch.setenv("PYEGERIA_DASHBOARD_SHEETS_STORE", str(path))
    monkeypatch.setattr(ld, "_cache", {})
    monkeypatch.setattr(ld, "_sheets_cache", {})
    monkeypatch.setattr(ld, "_SHEET_CACHE", ResultCache(ttl=300, max_entries=8, clock=time.time))
    monkeypatch.setattr(ld, "_SHEET_DEGRADED", ResultCache(ttl=60, max_stale=60, max_entries=8, clock=time.time))

    registry, resolutions = _registry(), _resolutions()
    monkeypatch.setattr(ld, "_report_registry", lambda: registry)
    monkeypatch.setattr(ld.spec_resolution, "resolve_all", lambda: resolutions)
    monkeypatch.setattr(dashboard_resolver, "_all_resolutions", lambda: resolutions)

    sheets = {}
    for n, b in FIXTURE["egeria_sheets"].items():      # placements are declared as the base Placement: rebuild them
        sheets[n] = dash_mod.EgeriaDashboardSheet.model_validate({**b, "placements": []})
        sheets[n].placements = [dash_mod.EgeriaPlacement.model_validate(p) for p in b["placements"]]
    seen = {"guids": [], "searches": []}
    held = {"by_egeria": True}
    monkeypatch.setattr(dash_mod, "load_dashboard_sheet",
                        lambda name, client: sheets.get(name) if held["by_egeria"] else None)

    async def by_guid(guid):
        seen["guids"].append(guid)
        el = FIXTURE["elements"].get(guid)
        return el if el is not None else {"elementHeader": {"guid": guid}, "properties": {}}   # a spec's own GUID

    client = NS(user_id="erinoverview", classification_manager=NS(_async_get_element_by_guid_=by_guid))
    monkeypatch.setattr(ld, "_egeria_client", lambda *a, **k: client)

    class Expert:
        def find_metadata_elements_with_string(self, *, search_string, page_size, **kw):
            seen["searches"].append((search_string, page_size))
            return FIXTURE["searches"].get(search_string, [])
        def close_session(self): pass
    monkeypatch.setattr(ld, "_expert", lambda *a, **k: Expert())

    app = FastAPI(); app.add_middleware(egeria_auth.EgeriaTokenMiddleware); app.include_router(ld.router)
    return NS(client=TestClient(app), seen=seen, held=held)


@pytest.mark.parametrize("key", sorted(FIXTURE["expected"]))
def test_every_live_sheet_resolves_exactly_as_the_live_portal_served_it(live, key):
    name, perspective = key.split("|")
    params = {} if perspective == "None" else {"perspective": perspective}
    got = live.client.get(f"/api/local-dashboards/{name}", params=params)
    assert got.status_code == 200
    assert got.json() == FIXTURE["expected"][key]


@pytest.mark.parametrize("name", EGERIA)
def test_egeria_held_sheets_are_resolved_by_guid_never_by_name(live, name):
    live.client.get(f"/api/local-dashboards/{name}")
    assert live.seen["searches"] == []                                  # no by-name search at all
    linked = {p["report_guid"] for p in FIXTURE["egeria_sheets"][name]["placements"] if p.get("report_guid")}
    assert linked and linked <= set(live.seen["guids"])                 # every linked Report read by its GUID


def test_the_local_cdo_sheet_resolves_by_name_as_before_with_a_page_of_25(live):
    """The CDO sheet's local-store copy, when Egeria does not hold it: the by-name path, on real searches."""
    live.held["by_egeria"] = False
    got = live.client.get(f"/api/local-dashboards/{CDO}").json()
    assert got == FIXTURE["expected_by_name"][f"{CDO}|None"]
    assert live.seen["searches"] and {size for _, size in live.seen["searches"]} == {25}
    assert live.seen["guids"] == []                                     # a local sheet has no GUIDs to read by


def test_a_search_hit_with_another_name_is_never_taken_for_the_report():
    """Real shape: a search for one Report also returns others whose names contain it; only the exact name counts."""
    noisy = {n: r for n, r in FIXTURE["searches"].items() if len(r) > 1}
    assert noisy, "the fixture should hold a search with more than one hit"
    for name, results in noisy.items():
        mgr = NS(find_metadata_elements_with_string=lambda **kw: results)
        got = ld._find_report_by_name_uncached(name, mgr)
        assert got is not None and got["heading"] == name
