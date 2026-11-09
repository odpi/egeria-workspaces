"""Resolved-sheet cache for GET /api/local-dashboards/<sheet>: key, stale-while-revalidate, no errors."""
import base64, json, os, sys, threading, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import local_dashboards_handler as ld  # noqa: E402
from result_cache import ResultCache  # noqa: E402


def _jwt(sub, exp_in=3600, salt=""):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in, 'n': salt})}.sig"


class Clock:
    def __init__(self): self.t = time.time()
    def __call__(self): return self.t
    def advance(self, s): self.t += s


@pytest.fixture
def env(monkeypatch, tmp_path):
    store = tmp_path / "sheets.json"; store.write_text("{}")
    monkeypatch.setenv("PYEGERIA_DASHBOARD_SHEETS_STORE", str(store))
    clock = Clock()
    cache = ResultCache(ttl=300, max_stale=3600, max_entries=8, clock=clock)
    monkeypatch.setattr(ld, "_SHEET_CACHE", cache)
    degraded = ResultCache(ttl=60, max_stale=60, max_entries=8, clock=clock)
    monkeypatch.setattr(ld, "_SHEET_DEGRADED", degraded)
    st = {"calls": [], "raise": None, "cacheable": True, "gate": None, "v": 1, "store": store}

    def fake_build(name, perspective, url, server, user_id, user_pwd):
        st["calls"].append((name, perspective))
        if st["gate"] is not None: st["gate"].wait(5)
        if st["raise"] is not None: raise st["raise"]
        return {"name": name, "perspective": perspective, "placements": [], "v": st["v"]}, st["cacheable"]

    monkeypatch.setattr(ld, "_build_sheet", fake_build)
    monkeypatch.setattr(ld, "_egeria_fingerprint", lambda *a, **k: "-")   # no Egeria in this file
    app = FastAPI(); app.add_middleware(egeria_auth.EgeriaTokenMiddleware); app.include_router(ld.router)
    st.update(client=TestClient(app), clock=clock, cache=cache, degraded=degraded)
    return st


def _get(env, token=None, lineage=False, name="CDO", **q):
    h = {}
    if token: h["X-Egeria-Token"] = token
    if lineage: h["X-Egeria-For-Lineage"] = "true"
    return env["client"].get(f"/api/local-dashboards/{name}", headers=h, params=q)


def _join_refresh():
    for t in threading.enumerate():
        if t.name == "sheet-refresh": t.join(5)


def test_miss_then_hit(env):
    tok = _jwt("peter"); a = _get(env, tok); b = _get(env, tok)
    assert (a.headers["X-Cache"], b.headers["X-Cache"]) == ("miss", "hit") and len(env["calls"]) == 1
    assert a.json() == b.json()


def test_forged_sub_and_wrong_password_miss(env):
    real = _jwt("peter"); _get(env, real)
    assert _get(env, _jwt("peter", salt="forged")).headers["X-Cache"] == "miss"
    _get(env, user_id="peter", user_pwd="right")
    assert _get(env, user_id="peter", user_pwd="wrong").headers["X-Cache"] == "miss"
    assert _get(env, user_id="peter", user_pwd="right").headers["X-Cache"] == "hit"


def test_sheet_perspective_lineage_are_separate(env):
    tok = _jwt("peter"); _get(env, tok)
    assert _get(env, tok, name="Other").headers["X-Cache"] == "miss"
    assert _get(env, tok, perspective="governance").headers["X-Cache"] == "miss"
    assert _get(env, tok, lineage=True).headers["X-Cache"] == "miss"


def test_store_edit_invalidates(env):
    tok = _jwt("peter"); _get(env, tok)
    env["store"].write_text('{"x": 1}'); os.utime(env["store"], ns=(1, time.time_ns() + 5_000_000_000))
    env["v"] = 2
    r = _get(env, tok)
    assert r.headers["X-Cache"] == "miss" and r.json()["v"] == 2


def test_errors_are_never_cached(env):
    env["raise"] = HTTPException(status_code=404, detail="nope")
    assert _get(env).status_code == 404 and _get(env).status_code == 404
    env["raise"] = HTTPException(status_code=500, detail="store down")
    assert _get(env).status_code == 500
    assert len(env["calls"]) == 3 and len(env["cache"]) == 0
    env["raise"] = None
    assert _get(env).headers["X-Cache"] == "miss"


def test_degraded_sheet_is_stored_briefly_in_its_own_cache(env):
    env["cacheable"] = False          # a permanently broken placement, or no Egeria connection
    a = _get(env); b = _get(env)
    assert (a.headers["X-Cache"], b.headers["X-Cache"]) == ("miss", "hit") and len(env["calls"]) == 1
    assert len(env["cache"]) == 0 and len(env["degraded"]) == 1      # never in the good cache
    env["clock"].advance(61)                                         # short TTL, and never served stale
    assert _get(env).headers["X-Cache"] == "miss" and len(env["calls"]) == 2


def test_good_answer_replaces_a_degraded_one(env):
    env["cacheable"] = False; _get(env)
    env["cacheable"] = True; _get(env, refresh="true")
    r = _get(env)
    assert r.headers["X-Cache"] == "hit" and len(env["cache"]) == 1


def test_degraded_answer_never_replaces_a_good_entry(env):
    _get(env)                                                        # good entry stored
    env["clock"].advance(301); env["cacheable"] = False; env["v"] = 2
    _get(env); _join_refresh()                                       # stale served; background refresh is degraded
    r = _get(env)
    assert r.headers["X-Cache"] == "stale" and r.json()["v"] == 1 and len(env["degraded"]) == 0
    r = _get(env, refresh="true")                                    # a forced refresh that is degraded
    assert r.json()["v"] == 2 and len(env["cache"]) == 1 and len(env["degraded"]) == 0
    assert _get(env).json()["v"] == 1                                # the good entry is still what is served


def test_stale_is_served_at_once_with_one_refresh(env):
    _get(env); env["clock"].advance(301); env["v"] = 2
    env["gate"] = threading.Event()
    rs = [_get(env) for _ in range(3)]
    assert [r.headers["X-Cache"] for r in rs] == ["stale"] * 3 and rs[0].json()["v"] == 1
    env["gate"].set(); _join_refresh()
    assert len(env["calls"]) == 2
    r = _get(env); assert r.headers["X-Cache"] == "hit" and r.json()["v"] == 2


def test_failed_refresh_keeps_the_stale_entry(env):
    _get(env); env["clock"].advance(301); env["raise"] = RuntimeError("down")
    _get(env); _join_refresh()
    r = _get(env); assert r.headers["X-Cache"] == "stale" and r.json()["v"] == 1


def test_concurrent_cold_requests_resolve_once(env):
    env["gate"] = threading.Event(); out = []
    ts = [threading.Thread(target=lambda: out.append(_get(env))) for _ in range(4)]
    [t.start() for t in ts]; time.sleep(0.3); env["gate"].set(); [t.join(10) for t in ts]
    assert len(env["calls"]) == 1 and len(out) == 4 and all(r.status_code == 200 for r in out)


def test_refresh_param_resolves_now(env):
    _get(env); env["v"] = 2
    r = _get(env, refresh="true")
    assert r.headers["X-Cache"] == "refresh" and r.json()["v"] == 2 and _get(env).json()["v"] == 2


def test_expired_token_bypasses_the_cache(env):
    _get(env, _jwt("peter"))
    r = _get(env, _jwt("peter", exp_in=-60))
    assert "X-Cache" not in r.headers and len(env["calls"]) == 2


def test_sheet_refresh_button_refreshes_every_tile():
    html = (Path(__file__).resolve().parent.parent / "local-dashboards.html").read_text()
    assert "renderPlacementBody(p, i, force)" in html                     # force reaches every tile on re-render
    assert "onclick=\"renderDetail(' + attrJson(sheet.name) + ',true)\"" in html
    assert "Refresh everything" in html                                   # and the tooltip says so
