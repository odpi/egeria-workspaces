"""GET /api/report-specs/sync names no spec and no zone to a caller who is not an administrator (F1).

The sync reads Egeria as the Portal's service account, so its skip list can name a zoned spec, and
its zones, that the viewer cannot read (read-back 2026-11-15: peter saw an erin-only spec's name and
zones). A non-admin gets the counts and the skip categories; an administrator keeps the full detail.
Through the real route, EgeriaTokenMiddleware and the real admin check (a signed demo JWT).
"""
import base64
import json
import re
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import report_spec_sync as rss  # noqa: E402

HIDDEN = "ZZ-RB-20261115 erin restricted"
ZONE = "erinoverview"
FOLDER = "ReportSpecFolder::Consumer::Portal"
REPORT = {
    "added": [], "updated": [], "unchanged": ["Shared One", "Shared Two"], "pruned": [],
    "skipped": [[HIDDEN, f"zoned: not synced into a shared cache (until B6's public-only read); zones {ZONE}"],
                ["ZZ other zoned", "zoned: not synced into a shared cache; zones financeteam"],
                ["Draft Thing", "contentStatus DRAFT is not synced"]],
}


def _unsigned(sub):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + 3600})}.sig"


def _app(monkeypatch, demo_mode):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from jose import jwt
    import demo_feedback_handler as dfh
    import report_specs_handler as rsh
    from egeria_auth import EgeriaTokenMiddleware

    monkeypatch.setattr(dfh, "DEMO_MODE", demo_mode)     # on: _is_admin really checks; off: laz
    monkeypatch.setattr(dfh, "SERVER_MANAGED_AUTH", False)
    monkeypatch.setattr(rss, "start", lambda trigger: False)   # POST never starts a real sync here
    monkeypatch.delenv("PORTAL_SYNC_DETAIL_USERS", raising=False)
    monkeypatch.setattr(rss, "configured_folders", lambda: [FOLDER])
    monkeypatch.setitem(rss._STATE, "outcome", "synced")
    monkeypatch.setitem(rss._STATE, "running", False)
    monkeypatch.setitem(rss._STATE, "finished_at", "2026-11-15T16:30:59+00:00")
    monkeypatch.setitem(rss._STATE, "report", json.loads(json.dumps(REPORT)))
    monkeypatch.setitem(rss._STATE, "error", None)

    app = FastAPI()
    app.include_router(rsh.router)
    app.add_middleware(EgeriaTokenMiddleware)
    client = TestClient(app)

    def demo(sub, role="user"):
        return jwt.encode({"sub": sub, "role": role, "exp": int(time.time()) + 3600}, dfh._JWT_SECRET, algorithm="HS256")

    def _get(who):
        headers, cookies = {}, {}
        if who == "peter":            # a signed-in viewer: an Egeria token and a non-admin demo session
            headers["X-Egeria-Token"] = _unsigned("peterprofile")
            cookies["demo_token"] = demo("peterprofile")
        elif who == "admin":
            headers["X-Egeria-Token"] = _unsigned("garygeeke")
            cookies["demo_token"] = demo("garygeeke", role="admin")
        r = client.get("/api/report-specs/sync", headers=headers, cookies=cookies)
        assert r.status_code == 200, r.text
        return r.json()
    return _get, client, demo


@pytest.fixture
def get(monkeypatch):
    return _app(monkeypatch, demo_mode=True)[0]


@pytest.mark.parametrize("who", ["peter", "anonymous"])
def test_a_non_admin_sees_no_skipped_name_or_zone(get, who):
    st = get(who)
    text = json.dumps(st)
    for secret in (HIDDEN, "ZZ other zoned", "Draft Thing", ZONE, "financeteam"):
        assert secret not in text, f"{secret!r} reached a non-admin ({who})"
    rep = st["report"]
    assert st["detail"] is False and "skipped" not in rep
    assert rep["skipped_count"] == 3                                   # still honest: three were skipped
    assert rep["skipped_categories"] == [["zoned", 2], ["not active", 1]]
    assert rep["unchanged"] == ["Shared One", "Shared Two"]            # shared specs stay named


def test_an_admin_keeps_the_full_detail(get):
    st = get("admin")
    assert st["detail"] is True
    names = [who for who, _why in st["report"]["skipped"]]
    assert HIDDEN in names and ZONE in json.dumps(st["report"]["skipped"])


def test_a_signed_in_non_admin_no_longer_gets_the_error_text(get, monkeypatch):
    monkeypatch.setitem(rss._STATE, "outcome", "failed")
    monkeypatch.setitem(rss._STATE, "error", f"RuntimeError: {HIDDEN} in zone {ZONE}")
    assert HIDDEN not in json.dumps(get("peter"))
    assert HIDDEN in get("admin")["error"]


def test_no_skips_reads_zero_not_absent(get, monkeypatch):
    rep = dict(REPORT, skipped=[])
    monkeypatch.setitem(rss._STATE, "report", rep)
    got = get("peter")["report"]
    assert got["skipped_count"] == 0 and got["skipped_categories"] == []


def test_an_unknown_reason_is_other_never_its_words():
    assert rss.skip_summary([["X", f"something new about {HIDDEN}"]]) == [["other", 1]]
    assert rss.skip_category(None) == "other"


def test_the_explorer_counts_and_shows_the_categories():
    html = (ROOT / "type-explorer.html").read_text(encoding="utf-8")
    assert "r.skipped_count != null ? r.skipped_count" in html          # "N skipped" uses the count
    assert "skipped_categories" in html and "shown to administrators only" in html
    assert "Whether a restricted report spec can run is not checked here" in html   # A1


# ── F1b: a Portal without auth (laz: DEMO_MODE and SERVER_MANAGED_AUTH off) ──────────────────────
# There _is_admin says everyone is an administrator, so the sync detail has its own rule: no
# X-Egeria-Token (the local owner) gets it; a persona token only if its user is listed.

SECRETS = (HIDDEN, "ZZ other zoned", "Draft Thing", ZONE, "financeteam")


@pytest.fixture
def noauth(monkeypatch):
    _get, client, demo = _app(monkeypatch, demo_mode=False)

    def call(token=None, method="get"):
        headers = {"X-Egeria-Token": token} if token else {}
        r = (client.post if method == "post" else client.get)("/api/report-specs/sync", headers=headers)
        assert r.status_code == 200, r.text
        return r.json()
    call.persona = lambda sub, exp=3600: demo(sub) if exp > 0 else _expired(demo, sub)
    return call


def _expired(demo, sub):
    from jose import jwt
    import demo_feedback_handler as dfh
    return jwt.encode({"sub": sub, "role": "user", "exp": int(time.time()) - 60}, dfh._JWT_SECRET, algorithm="HS256")


def _redacted(st):
    text = json.dumps(st)
    for secret in SECRETS:
        assert secret not in text, f"{secret!r} reached a persona"
    assert st["detail"] is False and "skipped" not in st["report"]
    assert st["report"]["skipped_count"] == 3
    assert st["report"]["skipped_categories"] == [["zoned", 2], ["not active", 1]]


@pytest.mark.parametrize("method", ["get", "post"])
def test_noauth_without_a_token_the_local_owner_gets_the_detail(noauth, method):
    st = noauth(method=method)
    assert st["detail"] is True and HIDDEN in [who for who, _ in st["report"]["skipped"]]


@pytest.mark.parametrize("method", ["get", "post"])
def test_noauth_a_persona_token_gets_counts_and_categories_only(noauth, method):
    _redacted(noauth(noauth.persona("peterprofile"), method=method))


def test_noauth_an_expired_persona_token_gets_no_names(noauth):
    _redacted(noauth(noauth.persona("peterprofile", exp=0)))


@pytest.mark.parametrize("method", ["get", "post"])
def test_noauth_a_listed_persona_gets_the_detail(noauth, monkeypatch, method):
    monkeypatch.setenv("PORTAL_SYNC_DETAIL_USERS", " garygeeke , someoneelse")
    assert noauth(noauth.persona("garygeeke"), method=method)["detail"] is True
    _redacted(noauth(noauth.persona("peterprofile"), method=method))       # the list is exact


def test_noauth_egeria_admin_users_from_demo_config_count(noauth, monkeypatch):
    import demo_config
    monkeypatch.setattr(demo_config, "EGERIA_ADMIN_USERS", {"garygeeke"}, raising=False)
    assert noauth(noauth.persona("garygeeke"))["detail"] is True


@pytest.mark.parametrize("token", ["not-a-jwt", "a.b.c", "x.eyJzdWIiOiAxfQ.y"])   # no readable string sub
def test_noauth_an_unreadable_token_gets_the_public_status(noauth, monkeypatch, token):
    monkeypatch.setenv("PORTAL_SYNC_DETAIL_USERS", "garygeeke")
    _redacted(noauth(token))


def test_noauth_any_error_withholds_the_detail(noauth, monkeypatch):
    import egeria_auth
    def boom(token):
        raise RuntimeError("cannot read")
    monkeypatch.setattr(egeria_auth, "_token_sub", boom)
    _redacted(noauth(noauth.persona("garygeeke")))


# ── F1b R1: the Explorer sends the persona's token with the calls that carry the sync detail ──────
# Without auth a request with no token is the local owner and gets the names, so a bare fetch from a
# signed-in persona's page (peter on laz) would still show them.


# A bare fetch of a report-specs URL that is allowed, and why. Nothing here carries the sync detail.
_BARE_FETCH_ALLOWED = {
    "/api/report-specs/execute": "the non-restricted run: its answer holds no sync status (restricted runs use egeriaFetch)",
}


def _explorer():
    return (ROOT / "type-explorer.html").read_text(encoding="utf-8")


def test_no_bare_fetch_of_a_report_specs_url_is_left():
    bare = re.findall(r"(?<![\w.])fetch\(\s*['\"`](/api/report-specs[^'\"`?]*)", _explorer())
    left = [u for u in bare if u not in _BARE_FETCH_ALLOWED]
    assert not left, f"bare fetch of {left}: use rsSpecFetch(url, creds, ...) so a persona's token goes with it"


def test_the_list_the_sync_and_its_poll_go_through_rs_spec_fetch():
    html = _explorer()
    assert "rsSpecFetch('/api/report-specs', creds)" in html
    assert "rsSpecFetch('/api/report-specs/sync', creds, { method: 'POST' })" in html
    assert "rsSpecFetch('/api/report-specs/sync', creds).then" in html


def test_rs_spec_fetch_sends_the_token_when_signed_in_and_plain_fetch_otherwise():
    body = re.search(r"function rsSpecFetch\(url, creds, opts\) \{(.*?)\n\}", _explorer(), re.S)
    assert body, "rsSpecFetch is missing"
    assert body.group(1).strip() == (
        "if (!rsCredsReady(creds)) return Promise.reject(new Error('signing in to Egeria has not finished'));\n"
        "  return creds && creds.token ? egeriaFetch(url, creds, opts) : fetch(url, opts);")


def test_the_sync_callback_sees_the_current_creds():
    html = _explorer()
    start = html.index("const startSync = useCallback(")
    deps = re.compile(r"\n  \}, \[([^\]]*)\]\);").search(html, start)       # the callback's own close
    assert deps and deps.group(1) == "creds", "startSync must re-bind when the token changes"


def _js_function(source, name):
    m = re.search(r"\nfunction " + name + r"\(.*?\n\}\n", source, re.S)
    assert m, f"{name} not found"
    return m.group(0)


def test_rs_spec_fetch_puts_the_token_on_the_wire_under_node(tmp_path):
    """Runs the page's rsSpecFetch and the shared egeriaFetch with a stub fetch: what a request carries."""
    import shutil
    import subprocess
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed (the Portal container has none)")
    shared = (ROOT / "static" / "egeria-shared-ui.js").read_text(encoding="utf-8")
    script = "\n".join([
        "var sent = [];",
        "function fetch(url, opts) { sent.push({ url: url, token: ((opts || {}).headers || {})['X-Egeria-Token'] || null });",
        "  return Promise.resolve({ status: 200 }); }",
        "function egeriaForLineageOn() { return false; }",
        "var _tokenRefresher = {};",
        _js_function(shared, "egeriaFetch"),
        _js_function(_explorer(), "rsSpecFetch"),
        _js_function(_explorer(), "rsCredsReady"),
        "Promise.all([",
        "  rsSpecFetch('/api/report-specs', { token: 'PETER-TOKEN', userId: 'peterprofile' }),",
        "  rsSpecFetch('/api/report-specs/sync', { token: 'PETER-TOKEN' }, { method: 'POST' }),",
        "  rsSpecFetch('/api/report-specs', {}),",
        "  rsSpecFetch('/api/report-specs/sync', null),",
        "]).then(function() { console.log(JSON.stringify(sent)); });",
    ])
    js = tmp_path / "rs_spec_fetch.js"
    js.write_text(script, encoding="utf-8")
    out = subprocess.run([node, str(js)], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    sent = json.loads(out.stdout)
    assert [s["token"] for s in sent] == ["PETER-TOKEN", "PETER-TOKEN", None, None]
    assert sent[2]["url"] == "/api/report-specs" and sent[3]["url"] == "/api/report-specs/sync"   # plain fetch


# ── F1b R2: a persona whose token is still being minted is not ready, not anonymous ─────────────

def _run_node(tmp_path, body):
    import shutil
    import subprocess
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed (the Portal container has none)")
    shared = (ROOT / "static" / "egeria-shared-ui.js").read_text(encoding="utf-8")
    script = "\n".join([
        "var sent = [];",
        "function fetch(url, opts) { sent.push({ url: url, token: ((opts || {}).headers || {})['X-Egeria-Token'] || null });",
        "  return Promise.resolve({ status: 200 }); }",
        "function egeriaForLineageOn() { return false; }",
        "var _tokenRefresher = {};",
        _js_function(shared, "egeriaFetch"),
        _js_function(_explorer(), "rsSpecFetch"),
        _js_function(_explorer(), "rsCredsReady"),
        body,
    ])
    js = tmp_path / "rs_ready.js"
    js.write_text(script, encoding="utf-8")
    out = subprocess.run([node, str(js)], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_a_persona_without_its_token_sends_no_request_until_the_token_lands(tmp_path):
    got = _run_node(tmp_path, """
var loading = { url: '', server: '', userId: 'peterprofile', password: 'pw' };   // as localStorage gives it
var out = { ready: rsCredsReady(loading) };
rsSpecFetch('/api/report-specs', loading).then(function() { out.loadingSent = true; },
                                               function(e) { out.refused = e.message; })
  .then(function() {
    out.sentWhileLoading = sent.length;
    return rsSpecFetch('/api/report-specs', Object.assign({}, loading, { token: 'PETER-TOKEN', tokenTried: true }));
  })
  .then(function() { out.sent = sent; console.log(JSON.stringify(out)); });
""")
    assert got["ready"] is False and got["sentWhileLoading"] == 0 and "loadingSent" not in got
    assert got["refused"] == "signing in to Egeria has not finished"
    assert [s["token"] for s in got["sent"]] == ["PETER-TOKEN"]              # the first request carries it


def test_who_is_ready_and_who_gets_a_plain_fetch(tmp_path):
    got = _run_node(tmp_path, """
var cases = {
  anonymous:     { url: '', server: '', userId: '', password: '' },
  failedMint:    { userId: 'peterprofile', password: 'pw', tokenTried: true },   // not signed in to Egeria
  noPassword:    { userId: 'peterprofile', password: '' },                       // acquireToken never mints
  none:          null,
};
var ready = {};
Object.keys(cases).forEach(function(k) { ready[k] = rsCredsReady(cases[k]); });
Promise.all(Object.keys(cases).map(function(k) { return rsSpecFetch('/api/report-specs', cases[k]); }))
  .then(function() { console.log(JSON.stringify({ ready: ready, sent: sent })); });
""")
    assert all(got["ready"].values()), got["ready"]
    assert [s["token"] for s in got["sent"]] == [None] * 4
    assert all(s["url"] == "/api/report-specs" for s in got["sent"])        # plain fetch, no query string


def test_the_list_waits_and_the_token_attempt_marks_itself_settled():
    html = _explorer()
    assert "if (!rsCredsReady(creds)) return;          // re-runs when the token lands" in html
    assert "}, [attempt, creds && creds.token, rsCredsReady(creds)]);" in html
    # acquireToken marks a settled attempt, with or without a token, and the load effect keeps it.
    assert "{ token: t.token, tokenTried: true } : { tokenTried: true }" in html
    assert ".catch(function() { return Object.assign({}, c, { tokenTried: true }); });" in html
    assert "if (withTok.token || withTok.tokenTried) setCreds(withTok);" in html
    assert "if (creds.token || creds.tokenTried) return;" in html
