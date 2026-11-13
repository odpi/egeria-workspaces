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
    # pyegeria's resolver for an Egeria-held sheet, faked like the real one on these placements: text with
    # content is text, the reader's "missing" keeps its words, any other placement is its linked Report.
    monkeypatch.setattr(ld, "_resolve_sheet", _default_resolver)
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
    assert body["egeria"]["available"] is True


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


def test_nested_sheet_placement_resolves_across_sources(env, monkeypatch, tmp_path):
    """A sheet in the local file whose placement names a sheet held in Egeria (Egeria's own chain has no
    nested-sheet placement: an unlinked one is "missing")."""
    monkeypatch.setattr(ld, "_find_report_by_name", lambda *a, **k: None)
    monkeypatch.setenv("PYEGERIA_DASHBOARD_SHEETS_STORE", str(_local_store(tmp_path, {"outer": ["inner"]})))
    env["egeria"] = {"inner": _sheet("inner", [], heading="Inner Sheet", source="egeria", breaks=[])}
    p = env["client"].get("/api/local-dashboards/outer").json()["placements"][0]
    assert p["kind"] == "sheet" and p["heading"] == "Inner Sheet"


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


def _default_resolver(client, sheet, *, perspective=None, spec_lookup=None, **kw):
    pos = {id(p): i for i, p in enumerate(sheet.placements, start=1)}
    out = []
    for p in ld._view_for_perspective(sheet.placements, perspective):
        if p.content:
            out.append(_rp(pos[id(p)], p.ref, "text", content=p.content))
        elif getattr(p, "kind", None) == "missing":
            out.append(_rp(pos[id(p)], p.ref, "missing", reason=p.note, note=p.note))
        else:
            out.append(_rp(pos[id(p)], p.ref, "report", report=_report(p.ref, guid="g")))
    return NS(placements=out)


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


def test_delete_without_a_token_user_is_refused_and_deletes_nothing(env, verify):
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


# ── P3s (2026-11-10): DELETE verifies the token with Egeria; Egeria-held sheets show Delete disabled ─────

@pytest.fixture
def verify(monkeypatch):
    """Fake MyProfile: what Egeria does with get_my_profile under the presented token."""
    st = {"raise": None, "tokens": []}

    class FakeProfile:
        def __init__(self, *a, **k): self.user_id, self.user_pwd = k.get("user_id"), k.get("user_pwd")
        def set_bearer_token(self, t): st["tokens"].append(t)
        def get_my_profile(self):
            if st["raise"]: raise st["raise"]
            return {"class": "OpenMetadataRootElement"}

    import pyegeria
    monkeypatch.setattr(pyegeria, "MyProfile", FakeProfile)
    return st


def _not_found():
    """The exception pyegeria's _base_server_client raises on an HTTP 404."""
    from pyegeria import PyegeriaNotFoundException
    resp = NS(status_code=404, url="https://egeria/my-profile", reason_phrase="Not Found",
              json=lambda: {}, text="")
    return PyegeriaNotFoundException(resp)


def test_delete_with_a_token_egeria_refuses_is_a_401_and_deletes_nothing(env, verify):
    verify["raise"] = _Refused("forged: Egeria said 401")
    c, forged = env["client"], _jwt("garygeeke", salt="hand-made")
    r = c.delete("/api/local-dashboards/json-only", headers={"X-Egeria-Token": forged})
    assert r.status_code == 401 and verify["tokens"] == [forged]           # Egeria was asked, with that token
    assert "json-only" in [s["name"] for s in c.get("/api/local-dashboards").json()["sheets"]]


def test_delete_fails_closed_when_the_token_cannot_be_checked(env, verify):
    verify["raise"] = ConnectionError("Egeria down")
    r = env["client"].delete("/api/local-dashboards/json-only", headers={"X-Egeria-Token": _jwt("alice")})
    assert r.status_code == 503
    assert "json-only" in [s["name"] for s in env["client"].get("/api/local-dashboards").json()["sheets"]]


def test_delete_with_a_verified_token_deletes_even_without_a_profile(env, verify):
    verify["raise"] = _not_found()
    r = env["client"].delete("/api/local-dashboards/json-only", headers={"X-Egeria-Token": _jwt("alice")})
    assert r.status_code == 200 and r.json() == {"deleted": "json-only"}


def test_egeria_held_sheets_show_delete_disabled_with_the_cli_hint():
    html = (Path(__file__).resolve().parent.parent / "local-dashboards.html").read_text()
    assert "python -m pyegeria.view.dashboards delete" in html and "shared Egeria write" in html
    assert html.count("s.source === 'egeria' ? egeriaDeleteDisabled(") == 1               # list card
    assert html.count("sheet.source === 'egeria' ? egeriaDeleteDisabled(") == 1           # detail view
    assert "disabled aria-disabled=\"true\"" in html


def test_not_found_is_matched_by_class_and_status_never_by_message_text(env, verify):
    c, tok = env["client"], {"X-Egeria-Token": _jwt("alice")}
    class Coded404(Exception):
        response_code = 404                                   # a 404 code on something that is not pyegeria's 404
    for exc in (ConnectionError("upstream said OMAG-404 NOT_FOUND"), Coded404("not pyegeria's not-found")):
        verify["raise"] = exc
        assert c.delete("/api/local-dashboards/json-only", headers=tok).status_code == 503, exc
    assert "json-only" in [s["name"] for s in c.get("/api/local-dashboards").json()["sheets"]]


def test_no_profile_marker_counts_as_verified(env, verify, monkeypatch):
    import pyegeria
    real = pyegeria.MyProfile
    monkeypatch.setattr(real, "get_my_profile", lambda self: "No elements found")   # pyegeria's NO_ELEMENTS_FOUND
    r = env["client"].delete("/api/local-dashboards/json-only", headers={"X-Egeria-Token": _jwt("alice")})
    assert r.status_code == 200


# ── pyegeria's shared resolver (B4 / D4, Portal-2) ───────────────────────────
# The resolver is faked here (pyegeria's own tests cover it on a fake Egeria); these check the Portal's side:
# same shape as the by-name path, the restricted kind, and the fallbacks.

def _report(name, **kw):
    r = dict(guid=f"g-{name}", name=name, description="", report_spec=None, output_format="DICT", params={},
             analytic_params={})
    r.update(kw)
    return NS(**r)


def _rp(position, ref, kind, **kw):
    base = dict(position=position, ref=ref, kind=kind, report=None, restricted=kind == "restricted",
                restricted_element=None, reason=None, note=None, content=None)
    base.update(kw)
    return NS(**base)


def _with_resolver(monkeypatch, answer, seen=None):
    def fake_resolve_sheet(client, sheet, *, perspective=None, spec_lookup=None, **kw):
        if seen is not None:
            seen.append((sheet.name, perspective, spec_lookup))
        if isinstance(answer, Exception):
            raise answer
        return NS(placements=[rp for rp in answer if perspective is None or rp.ref != "Owner Only"])
    monkeypatch.setattr(ld, "_resolve_sheet", fake_resolve_sheet)


def test_resolver_report_is_serialised_exactly_as_the_by_name_path(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Rep"), _pl("Words", content="hi")], source="egeria", breaks=[])}
    _with_resolver(monkeypatch, RuntimeError("resolver down: the by-name fallback answers"))
    by_name = env["client"].get("/api/local-dashboards/e").json()
    monkeypatch.setattr(ld, "_SHEET_CACHE", ResultCache(ttl=300, max_entries=8))
    monkeypatch.setattr(ld, "_SHEET_DEGRADED", ResultCache(ttl=60, max_stale=60, max_entries=8))
    monkeypatch.setattr(ld, "_find_report_by_name", lambda *a, **k: pytest.fail("resolved reports are not looked up by name"))
    _with_resolver(monkeypatch, [_rp(1, "Rep", "report", report=_report("Rep", guid="g")),
                                 _rp(2, "Words", "text", content="hi")])
    via_resolver = env["client"].get("/api/local-dashboards/e").json()
    assert via_resolver == by_name


def test_restricted_placement_says_not_visible_and_the_rest_resolve(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Open"), _pl("Secret"), _pl("Hidden Spec")], source="egeria", breaks=[])}
    _with_resolver(monkeypatch, [
        _rp(1, "Open", "report", report=_report("Open")),
        _rp(2, "Secret", "restricted", restricted_element="Report", reason="not visible to you"),
        _rp(3, "Hidden Spec", "restricted", restricted_element="ReportSpec", reason="not visible to you",
            report=_report("Hidden Spec"))])
    ps = env["client"].get("/api/local-dashboards/e").json()["placements"]
    assert [p["kind"] for p in ps] == ["report", "restricted", "restricted"]
    assert ps[1]["restricted"] is True and ps[1]["reason"] == "not visible to you"
    assert ps[1]["description"] == "Report not visible to you." and ps[1]["source"] == "egeria"
    assert ps[2]["restrictedElement"] == "ReportSpec" and ps[2]["description"] == "Report spec not visible to you."
    assert "reportSpec" not in ps[1] and "params" not in ps[2]     # nothing to run


def test_missing_placements_say_the_resolvers_words_and_are_never_looked_up_by_name(env, monkeypatch):
    """Portal-2: an Egeria-held placement is never searched by name. Before, a resolver "missing" fell back to a
    name search, which could only find a different, same-named Report or say "Unresolved reference"."""
    miss = _pl("Gone", kind="missing", note="report link missing in Egeria")
    env["egeria"] = {"e": _sheet("e", [miss, _pl("Raced"), _pl("Blank", content="")], source="egeria", breaks=[])}
    monkeypatch.setattr(ld, "_find_report_by_name", lambda *a, **k: pytest.fail("no by-name lookup"))
    _with_resolver(monkeypatch, [_rp(1, "Gone", "missing", reason="report link missing in Egeria"),
                                 _rp(2, "Raced", "missing", reason="the Report this placement shows is no longer in Egeria"),
                                 _rp(3, "Blank", "text", content="", note="text placement with no markdownContent in Egeria")])
    ps = env["client"].get("/api/local-dashboards/e").json()["placements"]
    assert [p["kind"] for p in ps] == ["missing", "missing", "missing"]
    assert ps[0]["description"] == "report link missing in Egeria"
    assert ps[1]["description"] == "the Report this placement shows is no longer in Egeria"
    assert ps[2]["description"] == "text placement with no markdownContent in Egeria"    # never an empty tile


def test_resolver_failure_falls_back_to_by_name(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Rep")], source="egeria", breaks=[])}
    _with_resolver(monkeypatch, RuntimeError("resolver broke"))
    d = env["client"].get("/api/local-dashboards/e").json()
    assert d["placements"][0]["kind"] == "report" and d["placements"][0]["heading"] == "Rep"


def test_resolver_token_refusal_is_a_401(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Rep")], source="egeria", breaks=[])}
    _with_resolver(monkeypatch, _Refused("Egeria said 401"))
    assert env["client"].get("/api/local-dashboards/e", headers={"X-Egeria-Token": _jwt("bob")}).status_code == 401


def test_resolver_gets_the_perspective_and_the_portals_registry(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Rep", perspectives=["Owner"]), _pl("Other", perspectives=["Steward"])],
                                 source="egeria", breaks=[])}
    seen = []
    monkeypatch.setattr(ld, "_report_registry", lambda: {"Spec-X": NS(action=None, description="d", family="F",
                                                                       formats=[])})
    _with_resolver(monkeypatch, [_rp(1, "Rep", "report", report=_report("Rep", report_spec="Spec-X"))], seen)
    ps = env["client"].get("/api/local-dashboards/e?perspective=Owner").json()["placements"]
    assert [p["ref"] for p in ps] == ["Rep"] and ps[0]["family"] == "F"
    name, perspective, lookup = seen[0]
    assert (name, perspective) == ("e", "Owner")
    assert lookup("Spec-X")[0].family == "F" and lookup("Nope") == (None, None)


def test_local_file_sheets_never_use_the_resolver(env, monkeypatch):
    _with_resolver(monkeypatch, AssertionError("not for a local-file sheet"))
    d = env["client"].get("/api/local-dashboards/json-only").json()
    assert d["source"] == "local file" and d["placements"][0]["kind"] == "report"


def test_resolver_answering_other_placements_falls_back_to_by_name(env, monkeypatch):
    env["egeria"] = {"e": _sheet("e", [_pl("Rep"), _pl("Two")], source="egeria", breaks=[])}
    for answer in ([_rp(1, "Rep", "report", report=_report("Rep"))],                         # one short
                   [_rp(1, "Rep", "report", report=_report("Rep")), _rp(2, "Other", "report", report=_report("Other"))]):
        _with_resolver(monkeypatch, answer)
        d = env["client"].get("/api/local-dashboards/e", params={"refresh": "true"}).json()
        assert [p["heading"] for p in d["placements"]] == ["Rep", "Two"]                      # by name, as the sheet says


def test_the_portal_calls_pyegeria_s_resolver_with_the_sheet_it_already_read(monkeypatch):
    from pyegeria.view import dashboard_resolver
    seen = []
    monkeypatch.setattr(dashboard_resolver, "resolve_sheet", lambda client, sheet, **kw: seen.append((client, sheet, kw)) or "r")
    assert ld._resolve_sheet("c", "s", perspective="p") == "r" and seen == [("c", "s", {"perspective": "p"})]


def test_page_shows_a_restricted_placement_and_never_runs_it():
    html = (Path(ld.__file__).parent / "local-dashboards.html").read_text()
    branch = html.index("if (p.kind === 'restricted')")
    assert branch < html.index("if (p.runnable === false)")          # before any execute path
    assert ".placement.kind-restricted" in html


# ── B5 (Egeria 8840035f): a small page can miss a Report; a miss is never cached ───────────────────────────

def test_the_report_search_asks_for_a_page_of_25_and_filters_on_the_exact_name():
    asked = []
    hit = {"elementGUID": "g1", "elementProperties": {"propertyValueMap": {
        "displayName": {"class": "PrimitiveTypePropertyValue", "primitiveValue": "Rep"}}}}
    near = {"elementGUID": "g0", "elementProperties": {"propertyValueMap": {
        "displayName": {"class": "PrimitiveTypePropertyValue", "primitiveValue": "Rep (old)"}}}}
    mgr = NS(find_metadata_elements_with_string=lambda **kw: asked.append(kw["page_size"]) or [near, hit])
    assert ld._find_report_by_name_uncached("Rep", mgr)["guid"] == "g1"
    assert asked == [25] and ld._REPORT_SEARCH_PAGE == 25


def _pv(v):
    return {"class": "PrimitiveTypePropertyValue", "primitiveValue": v}


def test_a_published_reports_authoring_stamps_are_not_report_parameters():
    """pyegeria 6.2.41 stamps a published Report's additionalProperties (D14); the by-name path (local-file
    sheets, and the fallback when the resolver fails) must not pass the stamps to the spec as parameters."""
    extra = {"reportSpec": "Risk-DrE-Basic", "outputFormat": "TABLE", "searchString": "CocoPharma::Risk::",
             "startsWith": "True", "publishedVersion": "3", "publishedAt": "2026-11-13T10:00:00+00:00",
             "publishedBy": "erinoverview", "authoringState": "PUBLISHED", "reportSpecVersion": "2"}
    stamped = {"elementGUID": "g1", "elementProperties": {"propertyValueMap": {
        "displayName": _pv("Company Risk Register"),
        # the real MapTypePropertyValue shape (laz, 2026-11-13): typed map plus pyegeria's flat strings
        "additionalProperties": {"class": "MapTypePropertyValue", "mapValues": {
            "propertyValueMap": {k: _pv(v) for k, v in extra.items()}, "propertyCount": len(extra),
            "propertyNames": list(extra), "propertiesAsStrings": dict(extra)}}}}}
    mgr = NS(find_metadata_elements_with_string=lambda **kw: [stamped])
    report = ld._find_report_by_name_uncached("Company Risk Register", mgr)
    assert report["reportSpec"] == "Risk-DrE-Basic" and report["outputFormat"] == "TABLE"
    assert report["params"] == {"searchString": "CocoPharma::Risk::", "startsWith": "True"}
    assert {"publishedVersion", "publishedAt", "publishedBy", "authoringState", "reportSpecVersion"} <= ld._AUTHORING_KEYS


def test_the_authoring_keys_include_pyegerias_own_when_it_has_them():
    try:
        from pyegeria.authoring.publication import AUTHORING_KEYS
    except ImportError:
        pytest.skip("this pyegeria has no pyegeria.authoring (the 6.2.40 floor): the literal set applies")
    assert set(AUTHORING_KEYS) <= ld._AUTHORING_KEYS


def test_a_report_miss_is_not_cached_so_a_false_miss_heals_on_the_next_build(monkeypatch):
    monkeypatch.setattr(ld, "_cache", {})
    answers = [None, {"guid": "g", "heading": "Rep"}]
    monkeypatch.setattr(ld, "_find_report_by_name_uncached", lambda name, mgr: answers.pop(0))
    assert ld._find_report_by_name("Rep", object()) is None
    assert ld._find_report_by_name("Rep", object())["guid"] == "g"           # asked again, not a pinned miss
    monkeypatch.setattr(ld, "_find_report_by_name_uncached", lambda *a: pytest.fail("a hit is cached"))
    assert ld._find_report_by_name("Rep", object())["guid"] == "g"


def test_a_spec_fetched_as_the_viewer_is_never_named_by_its_fetched_name(env, monkeypatch):
    """pyegeria's resolver can answer fetched_as="egeria:<label>@vN" for a spec no tier holds. The Portal runs a
    placement through /api/report-specs/execute by its reportSpec, which (Portal-3) refuses a fetched name: so
    the placement carries the Report's own label, never the fetched name."""
    env["egeria"] = {"e": _sheet("e", [_pl("Rep")], source="egeria", breaks=[])}
    _with_resolver(monkeypatch, [_rp(1, "Rep", "report", report=_report("Rep", report_spec="Held Elsewhere"),
                                     fetched_as="egeria:Held Elsewhere@v3", spec="Held Elsewhere")])
    r = env["client"].get("/api/local-dashboards/e")
    p = r.json()["placements"][0]
    assert p["kind"] == "report" and p["reportSpec"] == "Held Elsewhere"
    assert "egeria:" not in r.text
