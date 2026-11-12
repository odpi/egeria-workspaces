"""Report specs re-sync after an egeria-main restart (BRIEF-CDO-SHEET-TABLE-2026-11-12 sec. 5).

2026-11-12: the Portal's startup sync ran during an egeria-main restart; the specs synced but the
consumer index came back "not read", the sync counted as done, and nothing re-synced. Now:
- a sync whose consumer index is "not read" has outcome "index_not_read", which the startup run retries;
- while the index stays "not read", a Report Specs listing or a publish request starts a sync, at most
  every 2 minutes.
Offline: pyegeria's sync is a fake.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import report_spec_sync as rss  # noqa: E402


class FakeReport:
    def __init__(self, consumers):
        self.consumers = consumers

    def to_dict(self):
        return {"folders": ["ReportSpecFolder::Consumer::Portal"], "added": [], "updated": [], "unchanged": ["A"],
                "pruned": [], "skipped": [], "consumers": self.consumers}


@pytest.fixture
def sync_env(monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    state = {"consumers": {"status": "read", "reason": None, "consumers": 2, "labels": 5}, "calls": 0}

    def fake_sync(client, shared=True):
        state["calls"] += 1
        return FakeReport(state["consumers"])
    monkeypatch.setattr(esc, "sync_report_specs", fake_sync)
    monkeypatch.setattr(rss, "_service_client", lambda: None)
    monkeypatch.setattr(rss, "_reconcile_fallbacks", lambda: None)
    monkeypatch.setattr(rss, "configured_folders", lambda: ["ReportSpecFolder::Consumer::Portal"])
    monkeypatch.setattr(rss, "missing_folders", lambda rep, folders: [])
    rss._STATE.update(running=False, outcome=None, error=None)
    rss._LAZY["last"] = None
    return state


def test_a_read_index_is_synced(sync_env):
    assert rss._sync_once() == "synced" and rss._STATE["error"] is None


def test_an_unread_index_is_index_not_read_with_the_reason(sync_env):
    sync_env["consumers"] = {"status": "not read", "reason": "RootCollection::ReportSpecs not found", "consumers": 0}
    assert rss._sync_once() == "index_not_read"
    assert rss._STATE["outcome"] == "index_not_read"
    assert rss._STATE["error"] == "the consumer index was not read: RootCollection::ReportSpecs not found"


def test_no_consumer_block_is_still_synced(sync_env):
    sync_env["consumers"] = None          # older pyegeria, or no consumer root: not this check's business
    assert rss._sync_once() == "synced"


def test_the_startup_run_retries_index_not_read(monkeypatch):
    outcomes = iter(["index_not_read", "index_not_read", "synced"])
    calls = []
    monkeypatch.setattr(rss, "_sync_once", lambda: calls.append(1) or next(outcomes))
    monkeypatch.setattr(rss, "_RETRY_INTERVAL_S", 0)
    rss._STATE.update(running=True)
    rss._run("startup", 10, 0)
    assert len(calls) == 3 and rss._STATE["running"] is False


@pytest.mark.parametrize("outcome", ["synced", "folders_missing", "not_configured", "already_running"])
def test_other_outcomes_are_not_retried(monkeypatch, outcome):
    calls = []
    monkeypatch.setattr(rss, "_sync_once", lambda: calls.append(1) or outcome)
    monkeypatch.setattr(rss, "_RETRY_INTERVAL_S", 0)
    rss._run("startup", 10, 0)
    assert len(calls) == 1


# ── the lazy retry ────────────────────────────────────────────────────────────

@pytest.fixture
def starts(monkeypatch):
    out = []
    monkeypatch.setattr(rss, "start", lambda trigger="admin": out.append(trigger) or True)
    monkeypatch.setattr(rss, "configured_folders", lambda: ["ReportSpecFolder::Consumer::Portal"])
    rss._STATE.update(running=False, outcome="index_not_read")
    rss._LAZY.update(last=None, enabled=True)     # tests/conftest.py turns it off for the rest of the suite
    yield out
    rss._STATE.update(outcome=None)


def test_lazy_retry_at_most_every_2_minutes(starts):
    assert rss.LAZY_RETRY_S == 120
    assert rss.retry_if_index_not_read("not read", now=1000.0) is True
    assert rss.retry_if_index_not_read("not read", now=1060.0) is False      # within 2 minutes
    assert rss.retry_if_index_not_read("not read", now=1121.0) is True
    assert starts == ["lazy", "lazy"]


@pytest.mark.parametrize("status", ["read", "partial"])
def test_lazy_retry_only_while_not_read(starts, status):
    assert rss.retry_if_index_not_read(status, now=1000.0) is False and starts == []


def test_lazy_retry_not_while_a_sync_runs_or_without_folders(starts, monkeypatch):
    rss._STATE.update(running=True)
    assert rss.retry_if_index_not_read("not read", now=1000.0) is False
    rss._STATE.update(running=False)
    monkeypatch.setattr(rss, "configured_folders", lambda: [])
    assert rss.retry_if_index_not_read("not read", now=1000.0) is False and starts == []


def test_running_words_for_a_lazy_sync():
    assert rss.running_words({"running": True, "trigger": "lazy"}) == \
        "a sync from Egeria is running (the consumer index was not read)"


def test_the_report_specs_listing_asks_for_the_lazy_retry(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import report_spec_consumers
    import report_specs_handler as rsh
    seen = []
    monkeypatch.setattr(report_spec_consumers, "index",
                        lambda: {"status": "not read", "reason": "no sync yet", "consumers": [], "index": {}})
    monkeypatch.setattr(rss, "retry_if_index_not_read", lambda status=None, now=None: seen.append(status) or True)
    app = FastAPI()
    app.include_router(rsh.router)
    r = TestClient(app).get("/api/report-specs")
    assert r.status_code == 200 and seen == ["not read"]


def test_the_publish_control_asks_for_the_lazy_retry(monkeypatch):
    import report_spec_publish_handler as h
    seen = []
    monkeypatch.setattr(h, "_consumers", lambda: {"status": "not read", "reason": "no sync yet", "consumers": []})
    monkeypatch.setattr(rss, "retry_if_index_not_read", lambda status=None, now=None: seen.append(status) or True)
    with pytest.raises(h.Refused) as exc:
        h._folder_qn("Portal")
    assert exc.value.status == 409 and "the Portal tries again every 2 minutes" in exc.value.message
    assert seen == ["not read"]


def test_the_held_summary_says_index_not_read():
    import report_specs_handler as rsh
    import report_spec_sync
    orig = rsh._sync_status_for
    try:
        rsh._sync_status_for = lambda request: {"outcome": "index_not_read", "folders": ["F"], "running": False}
        msg = rsh._egeria_held_summary({"egeria": 0})["message"]
    finally:
        rsh._sync_status_for = orig
    assert msg.startswith("None held in Egeria yet: the last sync could not read the consumer folders")


def test_no_lazy_sync_before_any_sync_has_finished(starts):
    rss._STATE.update(outcome=None)                 # the startup sync owns the first read
    assert rss.retry_if_index_not_read("not read", now=1000.0) is False and starts == []


def test_the_suite_switch_turns_it_off(starts):
    rss._LAZY["enabled"] = False
    assert rss.retry_if_index_not_read("not read", now=1000.0) is False and starts == []


def test_public_status_carries_the_index_status_but_not_its_reason(monkeypatch):
    full = {"running": False, "outcome": "index_not_read", "finished_at": "t", "error": "secret words",
            "report": {"added": [], "updated": [], "unchanged": ["A"], "pruned": [], "skipped": [],
                       "consumers": {"status": "not read", "reason": "internal reason", "consumers": 0, "labels": 0}}}
    monkeypatch.setattr(rss, "status", lambda: full)
    pub = rss.public_status()
    assert pub["report"]["consumers"] == {"status": "not read", "consumers": 0, "labels": 0}
    assert "internal reason" not in str(pub) and "secret words" not in str(pub)
