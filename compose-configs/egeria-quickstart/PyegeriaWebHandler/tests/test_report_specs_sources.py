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
    # The Portal's own spec is a fallback for its Egeria-held copy (local_spec_fallback.py): local
    # only while the synced EGERIA tier does not hold the label.
    from pyegeria.view.egeria_spec_cache import egeria_tier
    if "Analytic - Generic Metric Trend" in egeria_tier().keys():
        assert by_name["Analytic - Generic Metric Trend"]["source"] == "egeria"
    else:
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
    report_spec_sync._STATE.update(running=False, outcome="folders_missing",
                                   missing_folders=["ReportSpecFolder::test-only"], report={
        "folders": ["ReportSpecFolder::test-only"], "added": [], "updated": [], "unchanged": [], "pruned": [],
        "notes": [], "skipped": [["ReportSpecFolder::test-only", "folder not found, or not visible to erinoverview"]]})
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    if held["count"] == 0:
        assert held["message"] == "None held in Egeria: the configured folders were not found in Egeria (or are not visible to the Portal's user)"


class _FakeReport:
    def __init__(self, skipped):
        self.skipped = skipped

    def to_dict(self):
        return {"folders": [], "added": [], "updated": [], "unchanged": [], "pruned": [], "notes": [],
                "skipped": [list(x) for x in self.skipped]}


def _fake_sync(monkeypatch, skipped):
    import pyegeria.view.egeria_spec_cache as esc

    class _C:
        def close_session(self):
            pass
    monkeypatch.setattr(report_spec_sync, "_service_client", lambda: _C())
    monkeypatch.setattr(esc, "sync_report_specs", lambda client, **kw: _FakeReport(skipped))


def test_every_folder_missing_is_its_own_outcome(monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::a,ReportSpecFolder::b")
    _fake_sync(monkeypatch, [("ReportSpecFolder::a", "folder not found, or not visible to x"),
                             ("ReportSpecFolder::b", "folder not found, or not visible to x")])
    assert report_spec_sync._sync_once() == "folders_missing"
    st = report_spec_sync.status()
    assert st["outcome"] == "folders_missing"
    assert st["missing_folders"] == ["ReportSpecFolder::a", "ReportSpecFolder::b"]


def test_some_folders_missing_is_synced_and_names_them(monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::a,ReportSpecFolder::b")
    _fake_sync(monkeypatch, [("ReportSpecFolder::b", "folder not found, or not visible to x")])
    assert report_spec_sync._sync_once() == "synced"
    assert report_spec_sync.status()["missing_folders"] == ["ReportSpecFolder::b"]


def test_unreadable_folder_is_not_called_missing(monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::a")
    _fake_sync(monkeypatch, [("ReportSpecFolder::a", "the folder could not be read, so its specs are kept")])
    assert report_spec_sync._sync_once() == "synced"
    assert report_spec_sync.status()["missing_folders"] == []


def test_admin_gate_fails_closed_when_the_check_cannot_load(api, monkeypatch):
    monkeypatch.setitem(sys.modules, "demo_feedback_handler", None)   # import now raises ImportError
    started = []
    monkeypatch.setattr(report_spec_sync, "start", lambda trigger="admin": started.append(trigger) or True)
    r = api.post("/api/report-specs/sync")
    assert r.status_code == 403
    assert started == []


def test_anonymous_status_withholds_error_detail(api, monkeypatch):
    monkeypatch.setattr(report_specs_handler, "_is_admin_closed", lambda request: False)
    report_spec_sync._STATE.update(running=False, outcome="failed", error="ConnectError: secret-host:9443 refused",
                                   report=None)
    st = api.get("/api/report-specs/sync").json()
    assert st["outcome"] == "failed" and st["detail"] is False
    assert "secret-host" not in str(st)
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    assert "secret-host" not in str(held)


def test_admin_status_shows_error_detail(api, monkeypatch):
    monkeypatch.setattr(report_specs_handler, "_is_admin_closed", lambda request: True)
    report_spec_sync._STATE.update(running=False, outcome="failed", error="ConnectError: secret-host:9443 refused")
    st = api.get("/api/report-specs/sync").json()
    assert st["detail"] is True and "secret-host" in st["error"]


def test_startup_retries_are_worded_as_retrying(api, monkeypatch):
    monkeypatch.setenv("PYEGERIA_REPORT_SPEC_FOLDERS", "ReportSpecFolder::test-only")
    report_spec_sync._STATE.update(running=True, trigger="startup", phase="syncing", attempt=3, attempts=10,
                                   outcome="failed", error="x")
    st = api.get("/api/report-specs/sync").json()
    assert "retrying (attempt 3 of 10" in st["running_words"]
    assert "already" not in st["running_words"]
    held = api.get("/api/report-specs").json()["egeriaHeld"]
    if held["count"] == 0:
        assert held["message"].startswith("None held in Egeria yet: the startup sync from Egeria is retrying")
    report_spec_sync._STATE.update(phase="waiting", attempt=0)
    assert report_spec_sync.running_words(report_spec_sync.status()) == "the startup sync from Egeria is starting"


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
    report_spec_sync._STATE.update(running=True, trigger="startup", phase="retry_wait", attempt=2, attempts=10)
    r = api.post("/api/report-specs/sync")
    assert r.status_code == 200
    assert r.json()["started"] is False and r.json()["already_running"] is True
    assert "retrying (attempt 2 of 10" in r.json()["running_words"]
    assert api.get("/api/report-specs/sync").json()["running"] is True


def test_startup_sync_can_be_turned_off(monkeypatch):
    monkeypatch.setenv("PORTAL_REPORT_SPEC_SYNC_AT_STARTUP", "0")
    started = []
    monkeypatch.setattr(report_spec_sync, "start", lambda trigger="admin": started.append(trigger) or True)
    report_spec_sync.start_at_startup()
    assert started == []
