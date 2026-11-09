"""Result cache for local-dashboard placement runs (/api/report-specs/execute with cache=true).

Offline: the report run (_run_spec) is a fake and the clock is a fake, so no Egeria is needed.
"""
import base64, json, sys, threading, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import report_specs_handler as rh  # noqa: E402
from result_cache import ResultCache  # noqa: E402


def _jwt(sub, exp_in=3600, salt=""):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in, 'n': salt})}.sig"


class Clock:
    def __init__(self): self.t = time.time()
    def __call__(self): return self.t
    def advance(self, s): self.t += s


@pytest.fixture
def env(monkeypatch):
    clock = Clock()
    cache = ResultCache(ttl=300, max_stale=3600, max_entries=3, refresh_backoff=30, clock=clock)
    monkeypatch.setattr(rh, "_RESULT_CACHE", cache)
    state = {"calls": [], "result": {"n": 1}, "raise": None, "gate": None}

    def fake_run(req, request, token, url, server, user_id, user_pwd):
        state["calls"].append((req.spec_name, token))
        if state["gate"] is not None:
            state["gate"].wait(5)
        if state["raise"] is not None:
            raise state["raise"]
        return state["result"]

    monkeypatch.setattr(rh, "_run_spec", fake_run)
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(rh.router)
    state.update(client=TestClient(app), clock=clock, cache=cache)
    return state


def _post(env, token=None, lineage=False, **body):
    h = {}
    if token: h["X-Egeria-Token"] = token
    if lineage: h["X-Egeria-For-Lineage"] = "true"
    payload = {"spec_name": "S", "output_format": "DICT", "params": {"a": 1}, "cache": True}
    payload.update(body)
    return env["client"].post("/api/report-specs/execute", headers=h, json=payload)


def _wait_refresh(env):
    for t in threading.enumerate():
        if t.name == "report-spec-refresh":
            t.join(5)


def test_miss_then_hit_runs_once(env):
    a = _post(env, _jwt("peter")); b = _post(env, _jwt("peter", salt="renewed"))
    assert (a.headers["X-Cache"], b.headers["X-Cache"]) == ("miss", "hit")   # a renewed token is the same viewer
    assert a.json() == b.json() == {"n": 1}
    assert len(env["calls"]) == 1
    assert "X-Cache-At" in b.headers


def test_uncached_requests_always_run_live(env):
    _post(env, cache=False); r = _post(env, cache=False)
    assert len(env["calls"]) == 2 and "X-Cache" not in r.headers


def test_viewers_are_separate(env):
    _post(env, _jwt("peter")); _post(env, _jwt("paul"))
    assert len(env["calls"]) == 2


def test_lineage_toggle_is_separate(env):
    _post(env, _jwt("peter")); r = _post(env, _jwt("peter"), lineage=True)
    assert r.headers["X-Cache"] == "miss" and len(env["calls"]) == 2


def test_params_and_format_are_part_of_the_key(env):
    _post(env, _jwt("peter")); _post(env, _jwt("peter"), params={"a": 2}); _post(env, _jwt("peter"), output_format="JSON")
    assert len(env["calls"]) == 3


def test_errors_and_refusals_are_never_cached(env):
    env["raise"] = HTTPException(status_code=400, detail="refused")
    assert _post(env).status_code == 400 and _post(env).status_code == 400
    env["raise"] = HTTPException(status_code=401, detail="token")
    assert _post(env).status_code == 401
    assert len(env["calls"]) == 3 and len(env["cache"]) == 0
    env["raise"] = None
    assert _post(env).headers["X-Cache"] == "miss"


def test_not_measured_result_is_cached_verbatim(env):
    env["result"] = {"kind": "absent", "content": "Not measured: the count timed out."}
    _post(env); r = _post(env)
    assert r.headers["X-Cache"] == "hit" and r.json() == env["result"]


def test_stale_is_served_at_once_with_exactly_one_refresh(env):
    _post(env)
    env["clock"].advance(301)
    env["result"] = {"n": 2}
    env["gate"] = threading.Event()                      # hold the refresh in flight
    s1 = _post(env); s2 = _post(env); s3 = _post(env)
    assert [s.headers["X-Cache"] for s in (s1, s2, s3)] == ["stale"] * 3
    assert s1.json() == {"n": 1}                          # the old value, at once
    env["gate"].set(); _wait_refresh(env)
    assert len(env["calls"]) == 2                         # the initial run + ONE refresh
    fresh = _post(env)
    assert fresh.headers["X-Cache"] == "hit" and fresh.json() == {"n": 2}


def test_failed_refresh_keeps_stale_and_backs_off(env):
    _post(env); env["clock"].advance(301)
    env["raise"] = RuntimeError("down")
    s = _post(env); _wait_refresh(env)
    assert s.headers["X-Cache"] == "stale"
    s = _post(env); _wait_refresh(env)                    # inside the back-off: no second attempt
    assert s.headers["X-Cache"] == "stale" and len(env["calls"]) == 2 and s.json() == {"n": 1}
    env["clock"].advance(31); env["raise"] = None; env["result"] = {"n": 3}
    _post(env); _wait_refresh(env)
    assert _post(env).json() == {"n": 3}


def test_too_old_is_a_miss(env):
    _post(env); env["clock"].advance(3601)
    assert _post(env).headers["X-Cache"] == "miss" and len(env["calls"]) == 2


def test_refresh_flag_runs_now_and_stores(env):
    _post(env); env["result"] = {"n": 2}
    r = _post(env, refresh=True)
    assert r.headers["X-Cache"] == "refresh" and r.json() == {"n": 2}
    assert _post(env).json() == {"n": 2} and len(env["calls"]) == 2


def test_expired_token_bypasses_the_cache(env):
    _post(env, _jwt("peter"))
    r = _post(env, _jwt("peter", exp_in=-60))
    assert "X-Cache" not in r.headers and len(env["calls"]) == 2   # reached _run_spec, which refuses it


def test_cache_is_bounded_lru(env):
    for i in range(5):
        _post(env, params={"i": i})
    assert len(env["cache"]) == 3
    assert _post(env, params={"i": 4}).headers["X-Cache"] == "hit"
    assert _post(env, params={"i": 0}).headers["X-Cache"] == "miss"


def test_claim_refresh_is_atomic_across_threads():
    c = ResultCache(); won = []
    barrier = threading.Barrier(8)
    def go():
        barrier.wait(); won.append(c.claim_refresh("k"))
    ts = [threading.Thread(target=go) for _ in range(8)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert won.count(True) == 1
