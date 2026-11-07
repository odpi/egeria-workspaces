# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests for the background section cache behind /api/overview/summary, ai-context, growth and
usage-context. The compute functions are controllable stubs, so nothing here talks to Egeria.

    python -m pytest test_overview_section_cache.py -q
"""
import json
import threading
import time

import pytest
from fastapi import HTTPException

import overview_handler as oh


@pytest.fixture(autouse=True)
def _fresh_state():
    oh._sections.clear()
    oh._section_inflight.clear()
    yield
    _wait_idle()
    oh._sections.clear()


def _wait_idle():
    deadline = time.time() + 5
    while oh._section_inflight and time.time() < deadline:
        time.sleep(0.01)


class _Compute:
    """A section computation; each call blocks until released, and records concurrency."""
    def __init__(self, payload=None, fail=False):
        self.payload = payload if payload is not None else {"assetTotal": 7}
        self.fail, self.calls, self.active, self.max_active = fail, 0, 0, 0
        self.release = threading.Event()
        self.started = threading.Semaphore(0)
        self.lock = threading.Lock()

    def __call__(self):
        with self.lock:
            self.calls += 1; self.active += 1; self.max_active = max(self.max_active, self.active)
        self.started.release()
        self.release.wait(5)
        with self.lock:
            self.active -= 1
        if self.fail:
            raise RuntimeError("Connection failed: boom")
        return dict(self.payload)


def _fetch(c, key="k", ok=lambda p: True):
    return oh._section_fetch(key, c, ok)


def _age(key, seconds):
    """Pretend the entry for key was measured `seconds` ago and its retry window has passed."""
    e = oh._sections[key]
    for f in ("measured_at", "fresh_until", "retry_at"):
        if e.get(f) is not None:
            e[f] -= seconds


# ── the four states ──────────────────────────────────────────────────────────

def test_cold_start_answers_loading_at_once_with_one_worker():
    c = _Compute()
    t0 = time.time()
    payload, meta = _fetch(c)
    assert time.time() - t0 < 0.5                     # the request did not wait for Egeria
    assert payload is None and meta["loading"] is True and meta["measuredAt"] is None
    assert c.started.acquire(timeout=5)
    assert len(oh._section_inflight) == 1
    c.release.set(); _wait_idle()
    assert c.calls == 1


def test_in_flight_requests_share_the_worker():
    c = _Compute()
    results = []
    ts = [threading.Thread(target=lambda: results.append(_fetch(c))) for _ in range(8)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert c.started.acquire(timeout=5)
    assert all(p is None and m["loading"] for p, m in results)
    c.release.set(); _wait_idle()
    assert c.calls == 1                               # eight requests, one computation


def test_fresh_hit_is_served_without_a_new_worker():
    c = _Compute({"assetTotal": 42}); c.release.set()
    _fetch(c); _wait_idle()
    payload, meta = _fetch(c)
    assert payload == {"assetTotal": 42}
    assert meta["loading"] is False and meta["stale"] is False and meta["refreshing"] is False
    assert meta["measuredAt"] and meta["refreshSeconds"] == oh._SECTION_TTL == 3600
    assert c.calls == 1 and not oh._section_inflight


def test_stale_hit_is_served_and_refreshed_in_the_background():
    c = _Compute({"assetTotal": 1}); c.release.set()
    _fetch(c); _wait_idle()
    _age("k", oh._SECTION_TTL + 10)
    old_measured = oh._sections["k"]["measured_at"]
    c.release.clear(); c.payload = {"assetTotal": 2}
    payload, meta = _fetch(c)
    assert payload == {"assetTotal": 1}               # the old value, at once
    assert meta["stale"] is True and meta["refreshing"] is True and meta["loading"] is False
    assert c.started.acquire(timeout=5)
    c.release.set(); _wait_idle()
    payload, meta = _fetch(c)
    assert payload == {"assetTotal": 2} and meta["stale"] is False
    assert oh._sections["k"]["measured_at"] > old_measured


# ── failure and back-off ─────────────────────────────────────────────────────

def test_cold_failure_is_not_measured_then_retried_after_the_back_off():
    c = _Compute(fail=True); c.release.set()
    _fetch(c); _wait_idle()
    payload, meta = _fetch(c)                         # inside the back-off: no new worker, no data
    assert payload is None and meta["loading"] is False and "boom" in meta["error"]
    assert c.calls == 1 and not oh._section_inflight
    _age("k", oh._SECTION_FAIL_TTL + 1)
    payload, meta = _fetch(c)                         # back-off over: one retry starts
    assert payload is None and meta["loading"] is True
    _wait_idle()
    assert c.calls == 2


def test_failed_refresh_keeps_serving_the_previous_measurement_as_stale():
    c = _Compute({"assetTotal": 5}); c.release.set()
    _fetch(c); _wait_idle()
    _age("k", oh._SECTION_TTL + 10)
    c.fail = True
    _fetch(c); _wait_idle()                           # refresh fails
    payload, meta = _fetch(c)
    assert payload == {"assetTotal": 5} and meta["stale"] is True and meta["refreshing"] is False
    assert c.calls == 2                               # and no immediate retry inside the back-off


def test_payload_missing_its_headline_value_is_re_measured_sooner():
    c = _Compute({"assetTotal": None}); c.release.set()
    _fetch(c, ok=lambda p: p["assetTotal"] is not None); _wait_idle()
    e = oh._sections["k"]
    assert e["fresh_until"] - e["measured_at"] == pytest.approx(oh._SECTION_PARTIAL_TTL, abs=1)


# ── concurrency bound ────────────────────────────────────────────────────────

def test_different_keys_are_bounded_by_the_global_semaphore():
    c = _Compute()
    for k in ("a", "b", "c", "d", "e"):
        _fetch(c, key=k)
    for _ in range(oh._SECTION_WORKERS):
        assert c.started.acquire(timeout=5)
    time.sleep(0.2)
    assert c.active == oh._SECTION_WORKERS            # the others wait on the gate, not on Egeria
    assert not c.started.acquire(timeout=0.1)
    assert len(oh._section_inflight) == 5             # but each key still has exactly one worker queued
    c.release.set(); _wait_idle()
    assert c.calls == 5 and c.max_active == oh._SECTION_WORKERS


# ── keys ─────────────────────────────────────────────────────────────────────

def test_key_separates_viewer_args_and_forlineage(monkeypatch):
    monkeypatch.setattr(oh, "_env", lambda *a: ("u", "srv", "envuser", "pw"))
    monkeypatch.setattr(oh, "token_user", lambda: None)
    monkeypatch.setattr(oh, "lineage_key", lambda: "")
    base = oh._section_key("summary", None)
    assert base == "summary|u|srv|envuser|None"
    assert oh._section_key("summary", "2026-01-01T00:00:00+00:00") != base
    monkeypatch.setattr(oh, "token_user", lambda: "peterprofile")
    assert oh._section_key("summary", None) == "summary|u|srv|peterprofile|None"
    monkeypatch.setattr(oh, "lineage_key", lambda: "|fl")
    assert oh._section_key("summary", None).endswith("|fl")


def test_old_keys_are_pruned_but_running_ones_are_kept(monkeypatch):
    monkeypatch.setattr(oh, "_SECTION_MAX_KEYS", 3)
    for i in range(5):
        oh._sections[f"k{i}"] = {"payload": {}, "measured_at": float(i), "fresh_until": 0, "retry_at": 0}
    oh._section_inflight["k0"] = object()
    oh._prune_sections(time.time())
    assert set(oh._sections) == {"k0", "k3", "k4"}
    oh._section_inflight.clear()


# ── routes: absence is never zero ────────────────────────────────────────────

ROUTES = [
    ("summary", lambda: oh.get_summary(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None),
     "_compute_summary"),
    ("ai-context", lambda: oh.get_ai_context(as_of_time=None, url=None, server=None, user_id=None, user_pwd=None),
     "_compute_ai_context"),
    ("usage-context", lambda: oh.get_usage_context(as_of_time=None, url=None, server=None, user_id=None,
                                                   user_pwd=None), "_compute_usage_context"),
    ("growth", lambda: oh.get_growth(window="6mo", points=None, months=None, url=None, server=None,
                                     user_id=None, user_pwd=None), "_compute_growth"),
]


@pytest.mark.parametrize("name,call,compute_name", ROUTES, ids=[r[0] for r in ROUTES])
def test_route_cold_answer_has_no_data_fields(monkeypatch, name, call, compute_name):
    c = _Compute()
    monkeypatch.setattr(oh, compute_name, lambda *a, **k: c())
    body = json.loads(call().body)
    assert body["loading"] is True and body["source"] == f"live:{name}"
    # nothing that could be read as a measured 0 / empty list
    assert set(body) <= {"loading", "stale", "refreshing", "measuredAt", "refreshSeconds", "error", "source"}
    c.release.set(); _wait_idle()


@pytest.mark.parametrize("name,call,compute_name", ROUTES, ids=[r[0] for r in ROUTES])
def test_route_failure_without_a_measurement_is_503(monkeypatch, name, call, compute_name):
    c = _Compute(fail=True); c.release.set()
    monkeypatch.setattr(oh, compute_name, lambda *a, **k: c())
    call(); _wait_idle()
    with pytest.raises(HTTPException) as ei:
        call()
    assert ei.value.status_code == 503 and "Not measured" in ei.value.detail


@pytest.mark.parametrize("name,call,compute_name", ROUTES, ids=[r[0] for r in ROUTES])
def test_route_serves_the_measurement_with_its_age(monkeypatch, name, call, compute_name):
    c = _Compute({"series": [{"date": "x"}], "assetTotal": 3, "countScope": "viewer",
                  "informationSupplyChains": 1, "funnel": {"cataloged": 1}}); c.release.set()
    monkeypatch.setattr(oh, compute_name, lambda *a, **k: c())
    call(); _wait_idle()
    body = json.loads(call().body)
    assert body["loading"] is False and body["stale"] is False and body["measuredAt"]
    assert body["refreshSeconds"] == 3600
    if name == "summary":                              # the viewer-total overlay still applies per request
        assert body["assetTotalViewer"] == 3


def test_worker_runs_with_the_requests_contextvars(monkeypatch):
    """The bearer token / forLineage contextvars must reach the background measurement."""
    import contextvars
    probe = contextvars.ContextVar("probe", default="unset")
    seen = []
    probe.set("request-token")
    oh._section_fetch("ctx", lambda: seen.append(probe.get()) or {"x": 1})
    _wait_idle()
    assert seen == ["request-token"]
