"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The Portal must not send its credentials to a caller-chosen platform URL
(BRIEF-PORTAL-PLATFORM-URL-ALLOWLIST-2026-11-10).

Rule: the Portal's service credentials only ever go to an allow-listed platform, and a token only ever
goes to the platform it was minted for. A user's own password may go to a platform the user chose when
PORTAL_ALLOW_CUSTOM_PLATFORMS is on (default on; off in DEMO_MODE).

Freshstart copy of the quickstart test: the route tests use GET /api/operations/platforms (freshstart has no
local-dashboards), with operations_handler._runtime_manager stubbed. No test here reaches Egeria or any other host: outbound pyegeria traffic (httpx.AsyncClient.send) and the
token-minting client are replaced, and the app is driven with TestClient without its lifespan (no
bootstrap). DNS for the "public" custom platform is faked.
"""
import ast
import json
import socket
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import egeria_auth  # noqa: E402
from egeria_auth import (PlatformRefused, bind_token_platform, normalize_platform_url,  # noqa: E402
                         resolve_platform)

HOME = "https://egeria.home.test:9443"
FOREIGN = "https://evil.example.com"
SERVICE_PWD = "service-secret"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    """A known allowlist and service password; no custom-platform flag; a fresh token map."""
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    real = socket.getaddrinfo

    def fake_getaddrinfo(host, *a, **k):     # the foreign host is "public"; nothing is resolved for real
        if host == "evil.example.com" or host == "other.example.org":
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]
        return real(host, *a, **k)
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)


@pytest.fixture
def no_outbound(monkeypatch):
    """Record (and refuse) every pyegeria HTTP request; the list must stay empty."""
    calls = []

    async def send(self, request, *a, **k):
        calls.append(str(request.url))
        raise AssertionError(f"outbound call to {request.url}")
    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    return calls


# ── normalization ───────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("a,b", [
    ("https://Host:443/", "https://host"),
    ("http://host:80/x/y", "http://HOST"),
    ("https://egeria.home.test:9443/", "https://EGERIA.home.test:9443"),
])
def test_normalization_equal(a, b):
    assert normalize_platform_url(a) == normalize_platform_url(b) is not None


@pytest.mark.parametrize("bad", ["", None, "egeria:9443", "ftp://host", "https://user:pw@host", "https:///x"])
def test_normalization_rejects(bad):
    assert normalize_platform_url(bad) is None


# ── resolve_platform: one test per row of the brief's §3.2 table ────────────────────────────────────

def test_empty_url_is_the_default():
    assert resolve_platform(None) == HOME
    assert resolve_platform("  ") == HOME


def test_allow_listed_is_allowed():
    assert resolve_platform("https://EGERIA.home.test:9443/") == "https://EGERIA.home.test:9443/"


def test_extra_allowlist_env(monkeypatch):
    monkeypatch.setenv("PORTAL_ALLOWED_PLATFORM_URLS", " https://second.home.test:9444 , ")
    assert resolve_platform("https://second.home.test:9444")


def test_foreign_with_service_password_is_refused():
    with pytest.raises(PlatformRefused) as e:
        resolve_platform(FOREIGN, has_caller_password=False)
    assert e.value.status_code == 400 and "own account" in e.value.detail


def test_foreign_with_caller_password_needs_the_flag(monkeypatch):
    assert resolve_platform(FOREIGN, has_caller_password=True) == FOREIGN        # default: on locally
    monkeypatch.setenv("PORTAL_ALLOW_CUSTOM_PLATFORMS", "false")
    with pytest.raises(PlatformRefused) as e:
        resolve_platform(FOREIGN, has_caller_password=True)
    assert e.value.status_code == 400


def test_demo_mode_turns_custom_platforms_off(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "true")
    with pytest.raises(PlatformRefused):
        resolve_platform(FOREIGN, has_caller_password=True)
    monkeypatch.setenv("PORTAL_ALLOW_CUSTOM_PLATFORMS", "true")                  # an explicit flag wins
    assert resolve_platform(FOREIGN, has_caller_password=True) == FOREIGN


def test_caller_password_never_reaches_an_internal_address():
    for u in ("http://127.0.0.1:9999", "https://localhost:9443", "http://10.1.2.3"):
        with pytest.raises(PlatformRefused) as e:
            resolve_platform(u, has_caller_password=True)
        assert e.value.status_code == 400


def test_token_bound_to_a_used_for_b_is_401():
    bind_token_platform("tok-a", HOME)
    with pytest.raises(PlatformRefused) as e:
        resolve_platform(FOREIGN, token="tok-a")
    assert e.value.status_code == 401
    bind_token_platform("tok-b", FOREIGN)
    with pytest.raises(PlatformRefused) as e:          # B's token never goes to A either
        resolve_platform(HOME, token="tok-b")
    assert e.value.status_code == 401
    assert resolve_platform(FOREIGN, token="tok-b") == FOREIGN


def test_unbound_token_only_for_allow_listed():
    assert resolve_platform(HOME, token="minted-elsewhere") == HOME
    with pytest.raises(PlatformRefused) as e:
        resolve_platform(FOREIGN, token="minted-elsewhere")
    assert e.value.status_code == 401


def test_service_password_counts_as_service_even_if_typed():
    assert not egeria_auth.is_caller_password(SERVICE_PWD)
    assert not egeria_auth.is_caller_password(None)
    assert egeria_auth.is_caller_password("users-own")


def test_apply_token_refuses_before_signing_in(monkeypatch):
    class Fake:
        platform_url = FOREIGN
        user_pwd = SERVICE_PWD

        def create_egeria_bearer_token(self):
            raise AssertionError("signed in at a foreign platform")
    with pytest.raises(PlatformRefused):
        egeria_auth.apply_token(Fake())


# ── routes ───────────────────────────────────────────────────────────────────────────────────────────

class _FakeRM:
    def get_platforms_by_type(self, *a, **k):
        return []


@pytest.fixture(scope="module")
def app_client():
    import pyegeria_handler as handler  # noqa: E402
    return TestClient(handler.app)       # no `with`: the lifespan (bootstrap) never runs


def test_operations_platforms_foreign_url_is_400_with_no_outbound(app_client, monkeypatch, no_outbound):
    import operations_handler as oh
    monkeypatch.setattr(oh, "_runtime_manager", lambda *a, **k: (_ for _ in ()).throw(AssertionError("route ran")))
    r = app_client.get("/api/operations/platforms", params={"url": "https://example.invalid"})
    assert r.status_code == 400, r.text
    assert no_outbound == []


def test_query_url_with_password_param_is_still_refused(app_client, no_outbound):
    # user_pwd is no longer a query param on any route: it cannot turn a foreign url into "the caller's own".
    r = app_client.get("/api/operations/platforms", params={"url": FOREIGN, "user_id": "x", "user_pwd": "mine"})
    assert r.status_code == 400
    assert no_outbound == []


def test_cross_site_get_with_url_is_403(app_client, no_outbound):
    r = app_client.get("/api/operations/platforms", params={"url": HOME}, headers={"Sec-Fetch-Site": "cross-site"})
    assert r.status_code == 403
    assert no_outbound == []


def test_same_origin_get_with_allow_listed_url_passes_the_gate(app_client, monkeypatch):
    import operations_handler as oh
    seen = []
    monkeypatch.setattr(oh, "_runtime_manager", lambda url, *a, **k: (seen.append(url), _FakeRM())[1])
    r = app_client.get("/api/operations/platforms", params={"url": HOME}, headers={"Sec-Fetch-Site": "same-origin"})
    assert r.status_code == 200, r.text
    assert seen == [HOME]


def test_token_minted_for_a_refused_at_b(app_client, no_outbound):
    bind_token_platform("tok-home", HOME)
    r = app_client.get("/api/operations/platforms", params={"url": FOREIGN}, headers={"X-Egeria-Token": "tok-home"})
    assert r.status_code == 401
    assert no_outbound == []


def test_egeria_token_text_plain_is_415(app_client, no_outbound):
    r = app_client.post("/api/egeria-token", content=json.dumps({"url": FOREIGN}),
                        headers={"Content-Type": "text/plain"})
    assert r.status_code == 415
    assert no_outbound == []


class _FakeAssetMaker:
    minted = []

    def __init__(self, view_server=None, platform_url=None, user_id=None, user_pwd=None):
        self.platform_url, self.user_id, self.user_pwd = platform_url, user_id, user_pwd

    async def _async_create_egeria_bearer_token(self):
        _FakeAssetMaker.minted.append((self.platform_url, self.user_id, self.user_pwd))
        return f"tok-for-{self.platform_url}"


@pytest.fixture
def fake_mint(monkeypatch):
    import pyegeria
    _FakeAssetMaker.minted = []
    monkeypatch.setattr(pyegeria, "AssetMaker", _FakeAssetMaker)
    return _FakeAssetMaker.minted


def test_egeria_token_foreign_url_without_password_is_400(app_client, fake_mint):
    r = app_client.post("/api/egeria-token", json={"url": FOREIGN, "user_id": "erinoverview"})
    assert r.status_code == 400
    assert fake_mint == []


def test_egeria_token_foreign_url_with_service_password_is_400(app_client, fake_mint):
    r = app_client.post("/api/egeria-token", json={"url": FOREIGN, "user_id": "x", "password": SERVICE_PWD})
    assert r.status_code == 400
    assert fake_mint == []


def test_egeria_token_default_platform_still_works(app_client, fake_mint):
    r = app_client.post("/api/egeria-token", json={"user_id": "peterprofile", "password": "own"})
    assert r.status_code == 200, r.text
    assert r.json()["platform_url"] == HOME
    assert fake_mint == [(HOME, "peterprofile", "own")]
    assert egeria_auth.token_platform(r.json()["token"]) == normalize_platform_url(HOME)


def test_connection_form_second_platform_with_own_password(app_client, fake_mint, monkeypatch):
    """Explorer's Connection form: the user's own password goes to the user's chosen platform; the token
    is bound to it, and is then accepted there and only there."""
    r = app_client.post("/api/egeria-token", json={"url": FOREIGN, "user_id": "me", "password": "own"})
    assert r.status_code == 200, r.text
    tok = r.json()["token"]
    assert r.json()["platform_url"] == FOREIGN and fake_mint == [(FOREIGN, "me", "own")]

    import operations_handler as oh
    monkeypatch.setattr(oh, "_runtime_manager", lambda url, *a, **k: _FakeRM())
    ok = app_client.get("/api/operations/platforms", params={"url": FOREIGN}, headers={"X-Egeria-Token": tok})
    assert ok.status_code == 200, ok.text
    home = app_client.get("/api/operations/platforms", params={"url": HOME}, headers={"X-Egeria-Token": tok})
    assert home.status_code == 401

    monkeypatch.setenv("PORTAL_ALLOW_CUSTOM_PLATFORMS", "false")
    off = app_client.post("/api/egeria-token", json={"url": FOREIGN, "user_id": "me", "password": "own"})
    assert off.status_code == 400


def test_post_body_url_is_gated_before_any_client(app_client, no_outbound):
    r = app_client.post("/api/report-specs/execute", json={"spec_name": "x", "url": FOREIGN})
    assert r.status_code == 400, r.text
    assert "own account" in r.json()["detail"]
    assert no_outbound == []


# ── scans ────────────────────────────────────────────────────────────────────────────────────────────

_HANDLER_FILES = sorted(p for p in _MODULE_DIR.glob("*.py") if not p.name.startswith("test_"))


def _trees():
    for p in _HANDLER_FILES:
        yield p, ast.parse(p.read_text())


def _is_call_named(node, *names):
    return isinstance(node, ast.Call) and (
        (isinstance(node.func, ast.Name) and node.func.id in names)
        or (isinstance(node.func, ast.Attribute) and node.func.attr in names))


def _route_functions(tree):
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                ast.unparse(d).startswith(("router.", "app.")) for d in fn.decorator_list):
            yield fn


def _params_with_defaults(fn):
    a = fn.args
    pos = a.posonlyargs + a.args
    return list(zip(pos[len(pos) - len(a.defaults):], a.defaults)) + \
        [(k, d) for k, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None]


def test_scan_no_user_pwd_query_param():
    bad = []
    for p, tree in _trees():
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg, d in _params_with_defaults(fn):
                    if arg.arg in ("user_pwd", "password", "user_pass") and _is_call_named(d, "Query"):
                        bad.append(f"{p.name}:{fn.name}")
            if isinstance(fn, ast.Call) and _is_call_named(fn, "dict"):
                for kw in fn.keywords:
                    if kw.arg in ("user_pwd", "password") and _is_call_named(kw.value, "Query"):
                        bad.append(f"{p.name}:dict({kw.arg}=Query)")
    assert bad == [], f"password taken from a query string: {bad}"


def test_scan_platform_url_params_are_named_url_and_come_from_the_query():
    """The middleware gates the query param named `url`. A route must not take a platform URL any other way
    (another name, a path param, a Body/Form field) that would bypass it."""
    bad = []
    for p, tree in _trees():
        for fn in _route_functions(tree):
            for arg, d in _params_with_defaults(fn):
                name = arg.arg.lower()
                if "url" in name and name != "url":
                    bad.append(f"{p.name}:{fn.name}:{arg.arg}")
                if name == "url" and not _is_call_named(d, "Query"):
                    bad.append(f"{p.name}:{fn.name}:url not a Query")
            for arg in fn.args.args + fn.args.kwonlyargs:
                if arg.arg == "url" and arg not in [a for a, _ in _params_with_defaults(fn)]:
                    bad.append(f"{p.name}:{fn.name}:url without a Query default")
    assert bad == [], bad


def test_scan_every_body_model_with_a_url_is_a_platform_body():
    bad = []
    for p, tree in _trees():
        for cls in ast.walk(tree):
            if isinstance(cls, ast.ClassDef):
                fields = {s.target.id for s in cls.body if isinstance(s, ast.AnnAssign)
                          and isinstance(s.target, ast.Name)}
                bases = {ast.unparse(b) for b in cls.bases}
                if "url" in fields and "PlatformBody" not in bases:
                    bad.append(f"{p.name}:{cls.name}")
    assert bad == [], f"request bodies with an ungated url: {bad}"


def test_scan_every_token_attach_is_gated():
    """Every place outside egeria_auth that signs a pyegeria client in or attaches a token must, in the
    same function, pass the platform gate first (check_client_platform / resolve_platform / apply_token)."""
    attach = ("create_egeria_bearer_token", "_async_create_egeria_bearer_token", "set_bearer_token", "use_token")
    gates = ("check_client_platform", "resolve_platform", "apply_token", "async_apply_token")
    bad = []
    for p, tree in _trees():
        if p.name == "egeria_auth.py":
            continue
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)]
            attaches = [c for c in calls if _is_call_named(c, *attach)]
            if not attaches:
                continue
            first_attach = min(c.lineno for c in attaches)
            gated = [c for c in calls if _is_call_named(c, *gates) and c.lineno <= first_attach]
            if not gated:
                bad.append(f"{p.name}:{fn.name}:{first_attach}")
    assert bad == [], f"token attached with no platform gate before it: {bad}"


def test_scan_json_bodies_reading_url_are_gated():
    """A route that reads `url` out of `await request.json()` must resolve it through resolve_platform."""
    bad = []
    for p, tree in _trees():
        for fn in _route_functions(tree):
            src = ast.unparse(fn)
            if "request.json()" in src and ("get('url')" in src or 'get("url")' in src) \
                    and "resolve_platform(" not in src:
                bad.append(f"{p.name}:{fn.name}")
    assert bad == [], bad


def test_percent_encoded_url_key_is_still_gated(app_client, no_outbound):
    r = app_client.get(f"/api/operations/platforms?%75rl={FOREIGN}")
    assert r.status_code == 400
    assert no_outbound == []
