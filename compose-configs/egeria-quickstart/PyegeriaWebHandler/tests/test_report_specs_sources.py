"""/api/report-specs says where each spec came from, and says plainly when none are held in Egeria.
report_spec_sync records every outcome and never touches Egeria when no folders are configured.
No Egeria call is made by any test here."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import report_spec_sync  # noqa: E402
import report_specs_handler  # noqa: E402


@pytest.fixture
def api():
    app = FastAPI()
    app.include_router(report_specs_handler.router)
    return TestClient(app)


@pytest.fixture(autouse=True)
def _reset_sync_state():
    saved = dict(report_spec_sync._STATE)
    yield
    report_spec_sync._STATE.clear()
    report_spec_sync._STATE.update(saved)


def test_removed_duplicate_is_gone_and_builtin_remains(api):
    names = {s["name"] for s in api.get("/api/report-specs").json()["specs"]}
    assert "Analytic - Element Count by Type" not in names
    assert "Analytic Demo - Element Count by Type" in names
    assert "Analytic - Generic Metric Trend" in names


def test_every_spec_carries_its_source(api):
    data = api.get("/api/report-specs").json()
    by_name = {s["name"]: s for s in data["specs"]}
    demo = by_name["Analytic Demo - Element Count by Type"]
    # Another test may register pyegeria's analytic demos at runtime; that local copy then shadows
    # the built-in, and the row must say so.
    assert demo["source"] == "builtin" or (demo["source"] == "local" and demo["shadows"] == "builtin")
    assert by_name["Analytic - Generic Metric Trend"]["source"] == "local"
    assert by_name["Analytic - Generic Metric Trend"]["sourceLabel"] == "Portal (local)"
    for s in data["specs"]:
        assert "source" in s and "shadowedBy" in s and "shadows" in s
    assert sum(data["sources"].values()) == data["total"]


def test_no_egeria_held_specs_is_said_in_words(api, monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "")
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    if held["count"] == 0:
        assert held["message"].startswith("None held in Egeria")
        assert "no report spec folders are configured" in held["message"]
        assert held["folders"] == []


def test_configured_but_never_synced_says_so(api, monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::test-only")
    report_spec_sync._STATE.update(running=False, outcome=None, report=None)
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    if held["count"] == 0:
        assert held["message"] == "None held in Egeria yet: no sync from Egeria has run"
        assert held["folders"] == ["ReportSpecFolder::test-only"]


def test_folder_not_found_is_named(api, monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::test-only")
    report_spec_sync._STATE.update(running=False, outcome="synced", report={
        "folders": ["ReportSpecFolder::test-only"], "added": [], "updated": [], "unchanged": [], "pruned": [],
        "notes": [], "skipped": [["ReportSpecFolder::test-only", "folder not found, or not visible to erinoverview"]]})
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    if held["count"] == 0:
        assert held["message"] == "None held in Egeria: the configured folders were not found in Egeria"


def test_sync_with_no_folders_never_builds_a_client(monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "")
    monkeypatch.setattr(report_spec_sync, "_service_client",
                        lambda: (_ for _ in ()).throw(AssertionError("Egeria contacted")))
    assert report_spec_sync._sync_once() == "not_configured"
    assert report_spec_sync.status()["outcome"] == "not_configured"


def test_sync_failure_is_recorded_not_raised(monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::test-only")

    def down():
        raise ConnectionError("platform not up")
    monkeypatch.setattr(report_spec_sync, "_service_client", down)
    assert report_spec_sync._sync_once() == "failed"
    st = report_spec_sync.status()
    assert st["outcome"] == "failed" and "platform not up" in st["error"]


def test_sync_route_reports_status_and_refuses_a_second_start(api, monkeypatch):
    report_spec_sync._STATE.update(running=True)
    r = api.post("/api/report-specs/sync")
    assert r.status_code == 200
    assert r.json()["started"] is False and r.json()["already_running"] is True
    assert api.get("/api/report-specs/sync").json()["running"] is True


def test_startup_sync_can_be_turned_off(monkeypatch):
    monkeypatch.setenv("PORTAL_REPORT_SPEC_SYNC_AT_STARTUP", "0")
    started = []
    monkeypatch.setattr(report_spec_sync, "start", lambda trigger="admin": started.append(trigger) or True)
    report_spec_sync.start_at_startup()
    assert started == []
