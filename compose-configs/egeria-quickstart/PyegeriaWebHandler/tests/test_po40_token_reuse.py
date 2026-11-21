"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-40: POST /api/egeria-token gives back the token it already minted for the same caller password,
platform, server and user while it has at least 15 min left, so a page load does not start every
per-token cache cold (DESIGN-PO-40-TOKEN-REUSE-2026-11-17 + Architect read-back R1-R4).

No test reaches Egeria: the token-minting client is replaced.
"""
import asyncio
import base64
import json
import re
import socket
import sys
import time
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import egeria_auth  # noqa: E402

HOME = "https://egeria.home.test:9443"
FOREIGN = "https://evil.example.com"
SERVICE_PWD = "service-secret"


def _jwt(exp, n):
    payload = base64.urlsafe_b64encode(json.dumps({"sub": "u", "exp": exp, "n": n}).encode()).decode().rstrip("=")
    return f"hdr.{payload}.sig"


class _Mint:
    calls = []
    life = 7200          # seconds; None = a token with no readable exp
    delay = 0.0

    def __init__(self, view_server=None, platform_url=None, user_id=None, user_pwd=None):
        self.args = (platform_url, view_server, user_id, user_pwd)

    async def _async_create_egeria_bearer_token(self):
        _Mint.calls.append(self.args)
        if _Mint.delay:
            await asyncio.sleep(_Mint.delay)
        n = len(_Mint.calls)
        return f"opaque-{n}" if _Mint.life is None else _jwt(time.time() + _Mint.life, n)


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    monkeypatch.setattr(egeria_auth, "_TOKEN_REUSE", {})
    monkeypatch.setattr(egeria_auth, "_TOKEN_REUSE_LOCKS", {})
    import pyegeria
    monkeypatch.setattr(pyegeria, "AssetMaker", _Mint)
    _Mint.calls, _Mint.life, _Mint.delay = [], 7200, 0.0
    # The no-password cases here are the local (no login gate) mode. PO-68: in the login-gated modes a
    # no-password request first needs a signed-in Portal user (test_po68_token_route_gate.py).
    import demo_config
    monkeypatch.setattr(demo_config, "DEMO_MODE", False)
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", False)
    real = socket.getaddrinfo

    def fake_getaddrinfo(host, *a, **k):
        if host == "evil.example.com":
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]
        return real(host, *a, **k)
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)


@pytest.fixture
def app_client():
    import pyegeria_handler as handler
    return TestClient(handler.app)


def _tok(client, **body):
    r = client.post("/api/egeria-token", json=body)
    assert r.status_code == 200, r.text
    return r.json()["token"]


PETER = {"user_id": "peterprofile", "password": "own"}


def test_same_caller_password_reuses_one_token(app_client):
    a, b = _tok(app_client, **PETER), _tok(app_client, **PETER)
    assert a == b and len(_Mint.calls) == 1


def test_a_different_password_user_server_or_url_mints_its_own(app_client, monkeypatch):
    base = _tok(app_client, **PETER)
    others = [_tok(app_client, user_id="peterprofile", password="other"),
              _tok(app_client, user_id="someone", password="own"),
              _tok(app_client, server="other-view-server", **PETER)]
    monkeypatch.setenv("PORTAL_ALLOW_CUSTOM_PLATFORMS", "true")
    others.append(_tok(app_client, url=FOREIGN, **PETER))
    assert len({base, *others}) == 5 and len(_Mint.calls) == 5


def test_renew_always_mints(app_client):
    a = _tok(app_client, **PETER)
    b = _tok(app_client, renew=True, **PETER)
    assert a != b and len(_Mint.calls) == 2
    assert _tok(app_client, **PETER) == b          # the renewed one is what is reused next


def test_no_password_sent_always_mints(app_client):
    """R1': the env-fallback path (no password sent: the Portal's own user) never reuses."""
    _tok(app_client)
    _tok(app_client)
    assert len(_Mint.calls) == 2
    assert egeria_auth._TOKEN_REUSE == {}


def test_a_sent_password_equal_to_the_service_password_is_reused(app_client):
    """R1' (Dan's case on laz): every demo persona's password equals the service password; a persona page
    load sends it with the persona's user_id, and the reload gets the same token back."""
    a = _tok(app_client, user_id="peterprofile", password=SERVICE_PWD)
    b = _tok(app_client, user_id="peterprofile", password=SERVICE_PWD)
    assert a == b and len(_Mint.calls) == 1


def test_a_no_password_request_never_gets_a_named_users_token(app_client):
    """The key is the RESOLVED (user, credential): {} resolves to the service user with nothing sent, so it
    can never be handed peterprofile's stored token (and {user_id: peterprofile} alone is refused, PO-41)."""
    p = _tok(app_client, user_id="peterprofile", password=SERVICE_PWD)
    assert _tok(app_client) != p
    r = app_client.post("/api/egeria-token", json={"user_id": "peterprofile"})
    assert r.status_code == 400
    assert len(_Mint.calls) == 2


def test_less_than_15_minutes_left_is_replaced(app_client):
    _Mint.life = 10 * 60
    a, b = _tok(app_client, **PETER), _tok(app_client, **PETER)
    assert a != b and len(_Mint.calls) == 2


def test_a_stored_token_near_expiry_is_not_returned(app_client, monkeypatch):
    a = _tok(app_client, **PETER)
    later = time.time() + 7200 - 5 * 60            # 5 min left
    monkeypatch.setattr(egeria_auth.time, "time", lambda: later)
    b = _tok(app_client, **PETER)
    assert a != b and len(_Mint.calls) == 2


def test_an_expired_token_is_never_returned(app_client, monkeypatch):
    a = _tok(app_client, **PETER)
    later = time.time() + 7300
    monkeypatch.setattr(egeria_auth.time, "time", lambda: later)
    assert _tok(app_client, **PETER) != a


def test_an_unreadable_exp_never_reuses(app_client):
    """R3: a token whose exp cannot be read is minted per call and never kept."""
    _Mint.life = None
    a, b = _tok(app_client, **PETER), _tok(app_client, **PETER)
    assert a != b and len(_Mint.calls) == 2 and egeria_auth._TOKEN_REUSE == {}


def test_a_failed_mint_caches_nothing(app_client, monkeypatch):
    async def boom(self):
        _Mint.calls.append("boom")
        raise RuntimeError("egeria down")
    monkeypatch.setattr(_Mint, "_async_create_egeria_bearer_token", boom)
    r = app_client.post("/api/egeria-token", json=PETER)
    assert r.status_code == 500
    assert egeria_auth._TOKEN_REUSE == {}


def test_refused_platform_is_400_with_no_mint_and_no_lookup(app_client, monkeypatch):
    """R4: the platform gate runs before any lookup."""
    looked = []
    monkeypatch.setattr(egeria_auth, "reusable_token", lambda k: looked.append(k))
    monkeypatch.setattr(egeria_auth, "token_reuse_key", lambda *a: looked.append(a) or "k")
    monkeypatch.setenv("PORTAL_ALLOW_CUSTOM_PLATFORMS", "false")
    r = app_client.post("/api/egeria-token", json={"url": FOREIGN, **PETER})
    assert r.status_code == 400
    assert _Mint.calls == [] and looked == []


def test_key_is_an_hmac_not_a_bare_hash_of_the_password():
    """R2: the key cannot be recomputed without the per-process secret."""
    import hashlib
    k = egeria_auth.token_reuse_key(HOME, "s", "u", "own")
    bare = hashlib.sha256("\0".join([egeria_auth.normalize_platform_url(HOME), "s", "u", "own"]).encode()).hexdigest()
    assert k != bare and "own" not in k
    assert egeria_auth.token_reuse_key(HOME + "/", "s", "u", "own") == k      # the resolved, normalized url


def test_two_concurrent_requests_make_one_mint(app_client):
    import pyegeria_handler as handler
    _Mint.delay = 0.05

    async def go():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=handler.app), base_url="http://t") as c:
            rs = await asyncio.gather(*[c.post("/api/egeria-token", json=PETER) for _ in range(2)])
        return [r.json()["token"] for r in rs]
    a, b = asyncio.run(go())
    assert a == b and len(_Mint.calls) == 1


def test_map_and_locks_stay_bounded(monkeypatch):
    monkeypatch.setattr(egeria_auth, "_TOKEN_REUSE_MAX", 5)
    for i in range(20):
        k = egeria_auth.token_reuse_key(HOME, "s", f"u{i}", "own")
        egeria_auth.token_reuse_lock(k)
        egeria_auth.remember_token(k, _jwt(time.time() + 7200, i))
    assert len(egeria_auth._TOKEN_REUSE) == 5
    egeria_auth.token_reuse_lock("one-more")
    assert len(egeria_auth._TOKEN_REUSE_LOCKS) <= 6
    # keys whose mint never stored a token do not pile up either
    for i in range(50):
        egeria_auth.token_reuse_lock(f"no-token-{i}")
    assert len(egeria_auth._TOKEN_REUSE_LOCKS) <= 7


# ── every page's 401 refresher asks for a new token ──────────────────────────────────────────────────

def test_every_refresher_sends_renew():
    pages = sorted(p for p in _MODULE_DIR.glob("*.html") if "_tokenRefresher.refresh =" in p.read_text())
    assert len(pages) >= 6, [p.name for p in pages]
    for p in pages:
        s = p.read_text()
        for m in re.finditer(r"_tokenRefresher\.refresh = function\((\w+)\)\s*\{", s):
            body = s[m.end():m.end() + 600]
            assert ("refreshPersonaToken(%s)" % m.group(1) in body
                    or "acquireToken(%s, true)" % m.group(1) in body), p.name
    te = (_MODULE_DIR / "type-explorer.html").read_text()
    assert "renew:    renew ? true : undefined" in te
    js = (_MODULE_DIR / "static" / "egeria-shared-ui.js").read_text()
    fn = js[js.index("function refreshPersonaToken("):]
    assert "renew: true" in fn[:fn.index("\n}\n")]


def test_reuse_key_uses_pbkdf2_not_a_fast_hash(monkeypatch):
    """CodeQL #895 alert 101: the password goes through a key-stretching function, never a fast hash."""
    import hashlib
    calls = []
    real = hashlib.pbkdf2_hmac

    def counting(*a, **k):
        calls.append(a[3] if len(a) > 3 else k.get("iterations"))
        return real(*a, **k)

    monkeypatch.setattr(hashlib, "pbkdf2_hmac", counting)
    egeria_auth.token_reuse_key(HOME, "s", "u", "pw")
    assert calls == [egeria_auth._TOKEN_REUSE_ITERATIONS] and egeria_auth._TOKEN_REUSE_ITERATIONS >= 100_000


def test_reuse_key_is_stable_and_password_sensitive():
    a = egeria_auth.token_reuse_key(HOME, "s", "u", "pw")
    assert a == egeria_auth.token_reuse_key(HOME, "s", "u", "pw")
    assert a != egeria_auth.token_reuse_key(HOME, "s", "u", "pw2")
