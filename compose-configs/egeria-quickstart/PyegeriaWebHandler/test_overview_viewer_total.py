# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests for the background viewer Asset count (denominator of the find-based survey / schema %
under repository scope). Fake clients; the count is a controllable stub, so nothing here talks to Egeria.

    python -m pytest test_overview_viewer_total.py -q
"""
import threading
import time

import pytest

import overview_handler as oh


@pytest.fixture(autouse=True)
def _fresh_state(monkeypatch):
    oh._viewer_totals.clear()
    oh._viewer_inflight.clear()
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: ("mgr", k.get("timeout")))
    yield
    deadline = time.time() + 5                       # let any worker finish before the next test
    while oh._viewer_inflight and time.time() < deadline:
        time.sleep(0.01)


class _Counter:
    """Replaces oh._viewer_count; each call blocks until released, and records concurrency."""
    def __init__(self, value=123):
        self.value, self.calls, self.active, self.max_active = value, [], 0, 0
        self.release = threading.Event()
        self.started = threading.Semaphore(0)
        self.lock = threading.Lock()

    def __call__(self, mgr, as_of):
        with self.lock:
            self.calls.append((mgr, as_of)); self.active += 1; self.max_active = max(self.max_active, self.active)
        self.started.release()
        self.release.wait(5)
        with self.lock:
            self.active -= 1
        return self.value


def _wait_idle():
    deadline = time.time() + 5
    while oh._viewer_inflight and time.time() < deadline:
        time.sleep(0.01)


def _state(user="u", as_of=None):
    return oh._viewer_total_state("http://x", "srv", user, "pw", as_of)


def test_cold_start_returns_loading_and_starts_exactly_one_worker(monkeypatch):
    c = _Counter(); monkeypatch.setattr(oh, "_viewer_count", c)
    assert _state() == (None, True, False)
    assert c.started.acquire(timeout=5)
    assert len(oh._viewer_inflight) == 1
    c.release.set(); _wait_idle()
    assert len(c.calls) == 1


def test_concurrent_requests_for_one_key_share_the_worker(monkeypatch):
    c = _Counter(); monkeypatch.setattr(oh, "_viewer_count", c)
    results = []
    ts = [threading.Thread(target=lambda: results.append(_state())) for _ in range(8)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert c.started.acquire(timeout=5)
    assert results == [(None, True, False)] * 8
    c.release.set(); _wait_idle()
    assert len(c.calls) == 1                         # eight requests, one count


def test_different_keys_queue_on_the_global_cap_of_one(monkeypatch):
    c = _Counter(); monkeypatch.setattr(oh, "_viewer_count", c)
    for u in ("a", "b", "c"):
        _state(user=u)
    assert c.started.acquire(timeout=5)
    time.sleep(0.2)                                  # give the others the chance to (wrongly) start
    assert c.max_active == 1 and len(c.calls) == 1
    c.release.set(); _wait_idle()
    assert len(c.calls) == 3 and c.max_active == 1   # all ran, strictly one at a time


def test_fresh_hit_returns_the_value_without_a_new_count(monkeypatch):
    c = _Counter(value=4242); c.release.set(); monkeypatch.setattr(oh, "_viewer_count", c)
    _state(); _wait_idle()
    assert _state() == (4242, False, False)
    assert len(c.calls) == 1


def test_stale_hit_returns_value_flagged_stale_and_refreshes_in_background(monkeypatch):
    c = _Counter(value=7); c.release.set(); monkeypatch.setattr(oh, "_viewer_count", c)
    _state(); _wait_idle()
    key = next(iter(oh._viewer_totals))
    oh._viewer_totals[key] = (time.time() - 1, 7)    # expire it
    c.value = 8; c.release.clear()
    assert _state() == (7, False, True)              # old value served at once, marked stale
    assert c.started.acquire(timeout=5) and len(c.calls) == 2   # refresh started
    c.release.set(); _wait_idle()
    assert _state() == (8, False, False)


def test_timeout_gives_none_not_loading_then_retries_after_the_short_ttl(monkeypatch):
    c = _Counter(value=None); c.release.set(); monkeypatch.setattr(oh, "_viewer_count", c)
    _state(); _wait_idle()
    assert _state() == (None, False, False)          # settled: "not measured", not "counting"
    assert len(c.calls) == 1
    key = next(iter(oh._viewer_totals))
    oh._viewer_totals[key] = (time.time() - 1, None) # short fail TTL elapsed
    c.value = 55
    assert _state() == (None, True, False)           # retrying
    _wait_idle()
    assert _state() == (55, False, False) and len(c.calls) == 2


def test_worker_exception_is_not_measured_and_clears_inflight(monkeypatch):
    def boom(mgr, as_of):
        raise RuntimeError("timeout")
    monkeypatch.setattr(oh, "_viewer_count", boom)
    _state(); _wait_idle()
    assert oh._viewer_inflight == {}
    assert _state() == (None, False, False)


def test_count_uses_the_long_client_timeout(monkeypatch):
    c = _Counter(); c.release.set(); monkeypatch.setattr(oh, "_viewer_count", c)
    _state(); _wait_idle()
    assert c.calls[0][0] == ("mgr", oh._VIEWER_TOTAL_TIMEOUT) and oh._VIEWER_TOTAL_TIMEOUT >= 240


def test_viewer_count_asks_for_viewer_scope_only_when_supported(monkeypatch):
    seen = {}
    def new(mgr, t, as_of=None, classifications=None, strict=False, scope=None):
        seen["new"] = (t, strict, scope); return 1
    def old(mgr, t, as_of=None, classifications=None, strict=False):
        seen["old"] = (t, strict); return 2
    monkeypatch.setattr(oh, "count_elements", new)
    assert oh._viewer_count(None, None) == 1 and seen["new"] == ("Asset", True, "viewer")
    monkeypatch.setattr(oh, "count_elements", old)
    assert oh._viewer_count(None, None) == 2 and seen["old"] == ("Asset", True)


# ── the scope rule ───────────────────────────────────────────────────────────

def test_viewer_scope_needs_no_second_count(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("must not start a count on viewer scope")
    monkeypatch.setattr(oh, "_viewer_total_state", boom)
    out = oh._overlay_viewer_total({"countScope": "viewer", "assetTotal": 99}, None, None, None, None, None)
    assert out["assetTotalViewer"] == 99 and out["assetTotalViewerLoading"] is False


def test_repository_scope_overlay_never_reuses_the_repository_total(monkeypatch):
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (None, True, False))
    out = oh._overlay_viewer_total({"countScope": "repository", "assetTotal": 60680}, None, None, None, None, None)
    assert out["assetTotalViewer"] is None and out["assetTotal"] == 60680 and out["assetTotalViewerLoading"] is True
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (43, False, True))
    out = oh._overlay_viewer_total({"countScope": "repository", "assetTotal": 60680}, None, None, None, None, None)
    assert out["assetTotalViewer"] == 43 and out["assetTotal"] == 60680 and out["assetTotalViewerStale"] is True


def test_overlay_does_not_mutate_the_cached_payload(monkeypatch):
    monkeypatch.setattr(oh, "_viewer_total_state", lambda *a, **k: (5, False, False))
    cached = {"countScope": "repository", "assetTotal": 10}
    oh._overlay_viewer_total(cached, None, None, None, None, None)
    assert "assetTotalViewer" not in cached
