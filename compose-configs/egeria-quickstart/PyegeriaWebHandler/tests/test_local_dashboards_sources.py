"""Dashboard Sheets from two sources (RS-DASH PR-3): Egeria first, the JSON store for names Egeria does not hold.

Covers both sources, the merge order (Egeria wins by name), the fallback when Egeria fails (said, never an
empty list passed off as "none"), the source labels on sheets and placements, and the credential/lineage
cache key. Egeria is faked: nothing here touches a platform or writes anything.
"""
import base64, json, sys, time, types
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import local_dashboards_handler as ld  # noqa: E402
from result_cache import ResultCache  # noqa: E402


def _jwt(sub, salt=""):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + 3600, 'n': salt})}.sig"


def _pl(ref, **kw):
    base = dict(ref=ref, span="1", emphasis="kpi", content=None, perspectives=[], detail_spec=None)
    base.update(kw)
    return NS(**base)


def _sheet(name, placements, heading=None, **kw):
    return NS(name=name, heading=heading or name.title(), description=f"{name} sheet", family="Test",
              aliases=[], placements=placements, **kw)


def _local_store(tmp_path, sheets):
    from pyegeria.view._output_dashboard_sheet_models import (
        DashboardSheet, Placement, save_dashboard_sheets_to_json, DashboardSheetDict)
    d = DashboardSheetDict()
    for name, refs in sheets.items():
        d[name] = DashboardSheet(name=name, heading=name.title(), description=f"{name} sheet", family="Test",
                                 placements=[Placement(ref=r, span="1", emphasis="kpi") for r in refs])
    path = tmp_path / "sheets.json"
    save_dashboard_sheets_to_json(d, str(path))
    return path


@pytest.fixture
def env(monkeypatch, tmp_path):
    store = _local_store(tmp_path, {"json-only": ["Rep A"], "twin": ["Rep Local"]})
    monkeypatch.setenv("PYEGERIA_DASHBOARD_SHEETS_STORE", str(store))
    monkeypatch.setattr(ld, "_cache", {})
    monkeypatch.setattr(ld, "_sheets_cache", {})
    clock = time.time
    monkeypatch.setattr(ld, "_SHEET_CACHE", ResultCache(ttl=300, max_entries=8, clock=clock))
    monkeypatch.setattr(ld, "_SHEET_DEGRADED", ResultCache(ttl=60, max_stale=60, max_entries=8, clock=clock))
    monkeypatch.setattr(ld, "_report_registry", lambda: {})
    monkeypatch.setattr(ld.spec_resolution, "resolve_all", lambda: {})
    monkeypatch.setattr(ld, "_expert", lambda *a, **k: object())
    monkeypatch.setattr(ld, "_find_report_by_name",
                        lambda name, *a, **k: {"guid": "g", "heading": name, "description": "", "reportSpec": None,
                                               "outputFormat": "DICT", "params": {}, "analyticParams": {}})
    st = {"egeria": {}, "fail": None, "calls": 0}

    def fake_client(*a, **k):
        return object()

    def fake_list(client):
        st["calls"] += 1
        if st["fail"]:
            raise st["fail"]
        return list(st["egeria"].values())

    def fake_load(name, client):
        st["loads"] += 1
        if st["fail"]:
            raise st["fail"]
        return st["egeria"].get(name)

    st["loads"] = 0
    mod = types.ModuleType("pyegeria.view.dashboards")
    mod.list_dashboard_sheets = fake_list
    mod.load_dashboard_sheet = fake_load
    monkeypatch.setitem(sys.modules, "pyegeria.view.dashboards", mod)
    monkeypatch.setattr(ld, "_egeria_client", fake_client)
    app = FastAPI(); app.add_middleware(egeria_auth.EgeriaTokenMiddleware); app.include_router(ld.router)
    st["client"] = TestClient(app)
    return st


def test_list_has_both_sources_and_egeria_wins_by_name(env):
    env["egeria"] = {"twin": _sheet("twin", [_pl("Rep Egeria")], source="egeria", breaks=[]),
                     "only-egeria": _sheet("only-egeria", [], source="egeria", breaks=[])}
    body = env["client"].get("/api/local-dashboards").json()
    by = {s["name"]: s for s in body["sheets"]}
    assert set(by) == {"twin", "only-egeria", "json-only"} and body["total"] == 3     # no duplicate "twin"
    assert [s["name"] for s in body["sheets"]][:2] == ["twin", "only-egeria"]          # Egeria first
    assert by["twin"]["source"] == "egeria" and by["only-egeria"]["source"] == "egeria"
    assert by["json-only"]["source"] == "local file"
    assert by["twin"]["placementCount"] == 1                                           # the Egeria copy, not the file's
    assert body["egeria"] == {"available": True}


def test_detail_from_egeria_labels_sheet_and_placements(env):
    env["egeria"] = {"twin": _sheet("twin", [_pl("Rep Egeria"), _pl("Words", content="hello")],
                                    source="egeria", breaks=[])}
    d = env["client"].get("/api/local-dashboards/twin").json()
    assert d["source"] == "egeria" and d["breaks"] == []
    assert [p["ref"] for p in d["placements"]] == ["Rep Egeria", "Words"]
    assert {p["source"] for p in d["placements"]} == {"egeria"}
    assert d["placements"][0]["kind"] == "report" and d["placements"][1]["kind"] == "text"


def test_detail_from_json_for_a_name_egeria_does_not_hold(env):
    d = env["client"].get("/api/local-dashboards/json-only").json()
    assert d["source"] == "local file" and d["egeria"] == {"available": True}
    assert [p["source"] for p in d["placements"]] == ["local file"]
    assert d["placements"][0]["ref"] == "Rep A"


def test_egeria_report_link_missing_keeps_the_readers_words(env):
    miss = _pl("Gone", kind="missing", note="report link missing in Egeria")
    env["egeria"] = {"e": _sheet("e", [miss], source="egeria", breaks=[])}
    p = env["client"].get("/api/local-dashboards/e").json()["placements"][0]
    assert p["kind"] == "missing" and p["description"] == "report link missing in Egeria" and p["source"] == "egeria"


def test_broken_chain_is_listed_with_its_break(env):
    env["egeria"] = {"b": _sheet("b", [], source="egeria", breaks=["no DashboardSheet link"])}
    s = [x for x in env["client"].get("/api/local-dashboards").json()["sheets"] if x["name"] == "b"][0]
    assert s["breaks"] == ["no DashboardSheet link"]


def test_egeria_failure_falls_back_and_says_so(env):
    env["fail"] = ConnectionError("platform down")
    body = env["client"].get("/api/local-dashboards").json()
    assert {s["name"] for s in body["sheets"]} == {"json-only", "twin"} and body["total"] == 2   # JSON still listed
    assert body["egeria"]["available"] is False and "platform down" in body["egeria"]["error"]
    assert {s["source"] for s in body["sheets"]} == {"local file"}
    d = env["client"].get("/api/local-dashboards/twin").json()
    assert d["source"] == "local file" and d["egeria"]["available"] is False


def test_egeria_failure_unknown_name_is_503_not_404(env):
    env["fail"] = ConnectionError("platform down")
    r = env["client"].get("/api/local-dashboards/only-in-egeria")
    assert r.status_code == 503 and "may be held there" in r.json()["detail"]
    env["fail"] = None
    assert env["client"].get("/api/local-dashboards/only-in-egeria").status_code == 404


def test_failures_are_not_cached_and_degraded_sheet_is_not_pinned(env):
    env["fail"] = ConnectionError("down")
    a = env["client"].get("/api/local-dashboards/json-only")
    assert a.json()["egeria"]["available"] is False
    env["fail"] = None
    env["egeria"] = {"json-only": _sheet("json-only", [_pl("Rep E")], source="egeria", breaks=[])}
    ld._SHEET_DEGRADED.clear() if hasattr(ld._SHEET_DEGRADED, "clear") else None
    ld._cache.clear()
    d = env["client"].get("/api/local-dashboards/json-only", params={"refresh": "true"}).json()
    assert d["source"] == "egeria" and d["placements"][0]["ref"] == "Rep E"


def test_egeria_read_is_cached_per_credential_and_lineage(env):
    env["egeria"] = {}
    c = env["client"]
    alice, bob = _jwt("alice"), _jwt("bob")
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": alice})
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": alice})
    assert env["calls"] == 1                                                    # same credential: one Egeria read
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": bob})
    assert env["calls"] == 2                                                    # another user never shares it
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": alice, "X-Egeria-For-Lineage": "true"})
    assert env["calls"] == 3                                                    # Promise/Memento toggle is in the key
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": _jwt("alice", salt="forged")})
    assert env["calls"] == 4                                                    # same sub, different token: miss


def test_nested_sheet_placement_resolves_across_sources(env, monkeypatch):
    monkeypatch.setattr(ld, "_find_report_by_name", lambda *a, **k: None)
    env["egeria"] = {"outer": _sheet("outer", [_pl("json-only")], source="egeria", breaks=[])}
    p = env["client"].get("/api/local-dashboards/outer").json()["placements"][0]
    assert p["kind"] == "sheet" and p["heading"] == "Json-Only"


def test_report_lookup_cache_key_is_per_credential_and_lineage(env):
    c = env["client"]; seen = []
    app = c.app
    @app.get("/_probe")
    def probe():
        seen.append(ld._report_ckey("R", "u", "s", None, None)); return {}
    for headers in ({"X-Egeria-Token": _jwt("alice")}, {"X-Egeria-Token": _jwt("bob")},
                    {"X-Egeria-Token": _jwt("alice"), "X-Egeria-For-Lineage": "true"}):
        c.get("/_probe", headers=headers)
    assert len(set(seen)) == 3 and all("alice" not in k and "bob" not in k for k in seen)   # hashed, distinct


def test_report_lookups_run_concurrently_and_fill_the_cache(env, monkeypatch):
    calls = []
    def slow(name, mgr, *a, **k):
        calls.append(name); time.sleep(0.3)
        ld._cache_put(ld._report_ckey(name, *a[:2], a[2], a[3] if len(a) > 3 else None), {"heading": name})
    monkeypatch.setattr(ld, "_find_report_by_name", slow)
    pls = [_pl(f"R{i}") for i in range(4)] + [_pl("Words", content="x"), _pl("R0")]
    t = time.time()
    ld._prime_report_lookups(pls, None, None, None, None)
    assert sorted(calls) == ["R0", "R1", "R2", "R3"]          # text skipped, duplicates once
    assert time.time() - t < 0.9                              # 4 x 0.3 s serial would be 1.2 s


def test_detail_reads_one_chain_not_the_whole_list(env):
    env["egeria"] = {"e1": _sheet("e1", [], source="egeria", breaks=[]), "e2": _sheet("e2", [], source="egeria", breaks=[])}
    c = env["client"]
    assert c.get("/api/local-dashboards/e1").json()["source"] == "egeria"
    assert c.get("/api/local-dashboards/json-only").json()["source"] == "local file"      # Egeria does not hold it
    assert env["calls"] == 0 and env["loads"] == 2                                         # list never read
    c.get("/api/local-dashboards/json-only", params={"refresh": "true"})
    assert env["loads"] == 2                                                               # "not held" is cached too


def test_expired_token_neither_reads_nor_fills_the_egeria_caches(env):
    env["egeria"] = {"e1": _sheet("e1", [], source="egeria", breaks=[])}
    exp = _jwt("alice"); enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    expired = f"{enc({'alg': 'none'})}.{enc({'sub': 'alice', 'exp': int(time.time()) - 60})}.sig"
    c = env["client"]
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": exp})              # a good user fills the cache
    n = env["calls"]
    for path in ("/api/local-dashboards", "/api/local-dashboards/e1"):
        r = c.get(path, headers={"X-Egeria-Token": expired})
        assert r.status_code == 401                                              # refused before any read
    assert env["calls"] == n and env["loads"] == 0                               # no cache hit, no Egeria call
    assert not any("expired" in k for k in ld._cache)
    assert ld._report_ckey("R", None, None, None, None) is not None              # (no token here: service user)


def test_local_sheet_named_like_an_egeria_alias_is_listed_and_opens_as_itself(env):
    e = _sheet("real", [_pl("Rep Egeria")], source="egeria", breaks=[]); e.aliases = ["json-only"]
    env["egeria"] = {"real": e}
    names = [s["name"] for s in env["client"].get("/api/local-dashboards").json()["sheets"]]
    assert "json-only" in names and "real" in names                                   # the local sheet is still listed
    d = env["client"].get("/api/local-dashboards/json-only").json()
    assert d["source"] == "local file" and d["placements"][0]["ref"] == "Rep A"       # ...and opens as itself: they agree


def test_report_lookup_workers_close_their_clients(env, monkeypatch):
    closed = []
    class C:
        def close_session(self): closed.append(1)
    monkeypatch.setattr(ld, "_expert", lambda *a, **k: C())
    def boom(name, mgr, *a, **k):
        if name == "R2": raise RuntimeError("lookup failed")
    monkeypatch.setattr(ld, "_find_report_by_name", boom)
    ld._prime_report_lookups([_pl("R1"), _pl("R2"), _pl("R3")], None, None, None, None)
    assert len(closed) == 3                                                          # even when a lookup failed


def test_egeria_edit_changes_the_built_sheet_key(env, monkeypatch):
    built = []
    monkeypatch.undo() if False else None
    real_build = ld._build_sheet
    def counting(name, *a):
        built.append(name); return real_build(name, *a)
    monkeypatch.setattr(ld, "_build_sheet", counting)
    env["egeria"] = {"e1": _sheet("e1", [_pl("Rep A")], source="egeria", breaks=[])}
    class M(NS):
        def model_dump_json(self): return json.dumps({"p": [x.ref for x in self.placements]})
    env["egeria"]["e1"] = M(**env["egeria"]["e1"].__dict__)
    c = env["client"]
    assert c.get("/api/local-dashboards/e1").headers["X-Cache"] == "miss"
    assert c.get("/api/local-dashboards/e1").headers["X-Cache"] == "hit"
    env["egeria"]["e1"] = M(**{**env["egeria"]["e1"].__dict__, "placements": [_pl("Rep B")]})   # edited in Egeria
    ld._cache.clear()                                                                  # the 60 s Egeria read has expired
    r = c.get("/api/local-dashboards/e1")
    assert r.headers["X-Cache"] == "miss" and r.json()["placements"][0]["ref"] == "Rep B"


# ── Token-header auth only (P3 2026-11-09: passwords in access logs) ─────────────────────────────────────

def test_no_route_accepts_user_id_or_user_pwd():
    for route in ld.router.routes:
        names = {p.name for p in route.dependant.query_params} | {p.alias for p in route.dependant.query_params}
        assert not names & {"user_id", "user_pwd", "password"}, route.path


def test_credentials_in_the_url_are_ignored_never_signed_in_as(env, monkeypatch):
    seen = []
    monkeypatch.setattr(ld, "_egeria_client", lambda url=None, server=None, user_id=None, user_pwd=None:
                        seen.append((user_id, user_pwd)) or object())
    monkeypatch.setattr(ld, "_expert", lambda url=None, server=None, user_id=None, user_pwd=None:
                        seen.append((user_id, user_pwd)) or object())
    env["egeria"] = {"e1": _sheet("e1", [_pl("Rep E")], source="egeria", breaks=[])}
    q = {"user_id": "garygeeke", "user_pwd": "secret"}
    c = env["client"]
    assert c.get("/api/local-dashboards", params=q).status_code == 200
    assert c.get("/api/local-dashboards/e1", params=q).status_code == 200
    assert seen and all(s == (None, None) for s in seen)          # the env service user, never garygeeke
    assert not any("garygeeke" in k for k in ld._cache)


def test_no_token_never_gets_a_signed_in_users_cached_data(env):
    env["egeria"] = {}
    c = env["client"]
    c.get("/api/local-dashboards", headers={"X-Egeria-Token": _jwt("alice")})
    n = env["calls"]
    c.get("/api/local-dashboards")                                   # no token: its own (service) entry
    assert env["calls"] == n + 1
    c.get("/api/local-dashboards", params={"user_id": "alice"})       # a claimed user_id does not reach alice's entry
    assert env["calls"] == n + 1                                      # shares the service entry, not alice's


def test_page_never_puts_credentials_in_a_local_dashboards_url():
    import re
    html = (Path(__file__).resolve().parent.parent / "local-dashboards.html").read_text()
    for m in re.finditer(r"/api/local-dashboards[^\n]*", html):
        assert not re.search(r"user_pwd|user_id|password", m.group(0)), m.group(0)


class _Refused(Exception):
    response_code = 401


def test_a_refused_token_is_a_401_not_a_quiet_fallback_to_the_local_file(env):
    env["fail"] = _Refused("Egeria said 401")
    c, tok = env["client"], {"X-Egeria-Token": _jwt("alice")}
    assert c.get("/api/local-dashboards", headers=tok).status_code == 401
    assert c.get("/api/local-dashboards/json-only", headers=tok).status_code == 401
    # the service user's own failure (no token) still degrades to the local file, and says so
    body = c.get("/api/local-dashboards").json()
    assert body["egeria"]["available"] is False and [s["name"] for s in body["sheets"]]


def _expired(sub="alice"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) - 60})}.sig"


def test_delete_without_a_token_user_is_refused_and_deletes_nothing(env):
    c = env["client"]
    for headers in ({}, {"X-Egeria-Token": _expired()}, {"X-Egeria-Token": "not-a-jwt"}):
        r = c.delete("/api/local-dashboards/json-only", headers=headers)
        assert r.status_code == 401, headers
    assert "json-only" in [s["name"] for s in c.get("/api/local-dashboards").json()["sheets"]]
    r = c.delete("/api/local-dashboards/json-only", headers={"X-Egeria-Token": _jwt("alice")})
    assert r.status_code == 200 and r.json() == {"deleted": "json-only"}
    ld._cache.clear()
    assert "json-only" not in [s["name"] for s in c.get("/api/local-dashboards").json()["sheets"]]


def test_page_sends_the_token_header_on_delete():
    html = (Path(__file__).resolve().parent.parent / "local-dashboards.html").read_text()
    i = html.index("function deleteSheet(")
    body = html[i:html.index("\n}\n", i)]
    assert "viewerToken()" in body and "'X-Egeria-Token': token" in body
