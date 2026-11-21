"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-68: POST /api/egeria-token with no password sent must not mint a token for the Portal's service user
for an anonymous caller. Freshstart (SERVER_MANAGED_AUTH) had no gate at all, so `{}` gave anyone a token
for bootstrap, the admin caller (reproduced through a Helm chart Ingress, 2026-11-21).

The three modes (compose-configs/ENVIRONMENT_DIVERGENCE.md), each tested here by setting the two
demo_config flags, which the route reads at call time:
  - freshstart (SERVER_MANAGED_AUTH): no password needs a signed-in Portal user, who gets back their OWN
    Egeria token (the one kept in their Portal session), never the service user's; anonymous is 401;
  - demo-quickstart (DEMO_MODE): no password needs a signed-in Portal user (DemoAuthGateMiddleware already
    401s an anonymous request through Apache; the route now holds a direct call to the same rule);
  - local-quickstart (neither flag): `{}` behaves exactly as before (the service user's token).
A request that sends a password is unchanged in every mode.

This file is identical in both trees; the few tree differences (quickstart's demo gate and its demo
account check) are found at run time. No test reaches Egeria: the token-minting client is replaced.
"""
import base64
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import demo_config  # noqa: E402
import egeria_auth  # noqa: E402

HOME = "https://egeria.home.test:9443"
FOREIGN = "https://evil.example.com"
SERVICE_USER = "portal-service-user"
SERVICE_PWD = "service-secret"
SIGNING_KEY = "po68-test-only-signing-key-0123456789abcdef"
HAS_DEMO_GATE = (_MODULE_DIR / "demo_auth_gate.py").exists()     # quickstart only

LOCAL, DEMO, SERVER_MANAGED = "local", "demo", "server-managed"
MODES = {LOCAL: (False, False), DEMO: (True, False), SERVER_MANAGED: (False, True)}


def _egeria_jwt(sub, life=3600):
    """An Egeria-style bearer token (only its exp is ever read here)."""
    payload = base64.urlsafe_b64encode(json.dumps({"sub": sub, "exp": time.time() + life}).encode())
    return "hdr." + payload.decode().rstrip("=") + ".sig"


class _Mint:
    calls = []

    def __init__(self, view_server=None, platform_url=None, user_id=None, user_pwd=None):
        self.args = (platform_url, user_id, user_pwd)

    async def _async_create_egeria_bearer_token(self):
        _Mint.calls.append(self.args)
        return _egeria_jwt(self.args[1])


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER", SERVICE_USER)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(demo_config, "JWT_SECRET", SIGNING_KEY)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    for name in ("_TOKEN_REUSE", "_TOKEN_REUSE_LOCKS"):      # PO-40 (quickstart)
        if hasattr(egeria_auth, name):
            monkeypatch.setattr(egeria_auth, name, {})
    import pyegeria
    monkeypatch.setattr(pyegeria, "AssetMaker", _Mint)
    _Mint.calls = []
    if HAS_DEMO_GATE:
        import demo_auth_gate
        monkeypatch.setattr(demo_auth_gate, "_USER_CACHE", {})
        monkeypatch.setattr(demo_auth_gate, "_user_is_valid", lambda user_id: user_id in _VERIFIED)
    _VERIFIED.clear()


_VERIFIED = set()      # quickstart demo accounts that exist and are verified


@pytest.fixture
def mode(monkeypatch, request):
    demo, managed = MODES[request.param]
    monkeypatch.setattr(demo_config, "DEMO_MODE", demo)
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", managed)
    return request.param


@pytest.fixture(scope="module")
def app():
    import pyegeria_handler as handler
    return handler.app


@pytest.fixture
def client(app):
    return TestClient(app, raise_server_exceptions=False)      # no `with`: the lifespan never runs


def _session_cookie(user_id, egeria_token=None, key=SIGNING_KEY):
    """A Portal session (demo_token) as /api/auth/login sets it; freshstart's carries the user's Egeria
    token. Signed with the test key, so it is valid unless `key` says otherwise."""
    from jose import jwt
    claims = {"sub": user_id, "role": "user", "display_name": user_id,
              "exp": datetime.utcnow() + timedelta(hours=1)}
    if egeria_token is not None:
        claims["egeria_token"] = egeria_token
    _VERIFIED.add(user_id)
    return {"demo_token": jwt.encode(claims, key, algorithm="HS256")}


def _post(client, body, cookies=None, headers=None):
    if cookies:
        client.cookies.clear()
        for k, v in cookies.items():
            client.cookies.set(k, v)
    else:
        client.cookies.clear()
    return client.post("/api/egeria-token", json=body, headers=headers or {})


# ── freshstart (SERVER_MANAGED_AUTH) ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
@pytest.mark.parametrize("body", [{}, {"user_id": SERVICE_USER}, {"renew": True}, {"url": HOME}])
def test_server_managed_anonymous_no_password_is_401_and_mints_nothing(client, mode, body):
    r = _post(client, body)
    assert r.status_code == 401, r.text
    assert "Sign in to the Portal first" in r.json()["detail"]
    assert "token" not in r.json()
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_forged_session_is_401(client, mode):
    r = _post(client, {}, cookies=_session_cookie("peterprofile", _egeria_jwt("peterprofile"),
                                                  key="not-the-portal-key-0123456789abcdef"))
    assert r.status_code == 401, r.text
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
@pytest.mark.parametrize("body", [{}, {"user_id": "peterprofile"}, {"renew": True}, {"url": HOME}])
def test_server_managed_signed_in_user_gets_their_own_token(client, mode, body):
    own = _egeria_jwt("peterprofile")
    r = _post(client, body, cookies=_session_cookie("peterprofile", own))
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["token"] == own
    assert d["user_id"] == "peterprofile" != SERVICE_USER
    assert d["platform_url"] == HOME
    assert _Mint.calls == []                 # never a service-user (or any) sign-in
    assert egeria_auth.token_platform(own) == egeria_auth.normalize_platform_url(HOME)


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_signed_in_user_cannot_name_another_user(client, mode):
    r = _post(client, {"user_id": SERVICE_USER}, cookies=_session_cookie("peterprofile", _egeria_jwt("peterprofile")))
    assert r.status_code == 400, r.text
    assert "different user" in r.json()["detail"]
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_expired_session_token_is_401_not_a_service_token(client, mode):
    r = _post(client, {}, cookies=_session_cookie("peterprofile", _egeria_jwt("peterprofile", life=-60)))
    assert r.status_code == 401, r.text
    assert "expired" in r.json()["detail"]
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_session_without_an_egeria_token_is_401(client, mode):
    r = _post(client, {}, cookies=_session_cookie("peterprofile"))
    assert r.status_code == 401, r.text
    assert "no Egeria sign-in" in r.json()["detail"]
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_session_token_never_goes_to_another_platform(client, mode):
    r = _post(client, {"url": FOREIGN}, cookies=_session_cookie("peterprofile", _egeria_jwt("peterprofile")))
    assert r.status_code == 400, r.text
    assert _Mint.calls == []


# ── demo-quickstart (DEMO_MODE) ──────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_anonymous_edge_request_is_401_via_the_gate(app, mode):
    if not HAS_DEMO_GATE:
        pytest.skip("only quickstart has DemoAuthGateMiddleware (freshstart's route rule is tested below)")
    from demo_auth_gate import DemoAuthGateMiddleware
    gated = TestClient(DemoAuthGateMiddleware(app), raise_server_exceptions=False)
    r = gated.post("/api/egeria-token", json={}, headers={"X-Egeria-Edge": "1"})
    assert r.status_code == 401, r.text
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_anonymous_direct_request_is_401_at_the_route(client, mode):
    r = _post(client, {})                    # no edge header: the gate lets it by; the route does not
    assert r.status_code == 401, r.text
    assert "Sign in to the Portal first" in r.json()["detail"]
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_signed_in_user_no_password_is_as_before(client, mode):
    r = _post(client, {}, cookies=_session_cookie("someone@example.org"))
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == SERVICE_USER
    assert _Mint.calls == [(HOME, SERVICE_USER, SERVICE_PWD)]


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_disabled_account_is_401(client, mode):
    if not HAS_DEMO_GATE:
        pytest.skip("freshstart has no demo account store")
    cookies = _session_cookie("someone@example.org")
    _VERIFIED.discard("someone@example.org")
    r = _post(client, {}, cookies=cookies)
    assert r.status_code == 401, r.text
    assert _Mint.calls == []


# ── local-quickstart (neither flag) ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode", [LOCAL], indirect=True)
@pytest.mark.parametrize("body", [{}, {"user_id": SERVICE_USER}, {"renew": True}])
def test_local_no_password_is_exactly_as_before(client, mode, body):
    r = _post(client, body)
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == SERVICE_USER
    assert r.json()["platform_url"] == HOME
    assert _Mint.calls == [(HOME, SERVICE_USER, SERVICE_PWD)]


@pytest.mark.parametrize("mode", [LOCAL], indirect=True)
def test_local_no_password_named_user_still_refused_po41(client, mode):
    r = _post(client, {"user_id": "peterprofile"})
    assert r.status_code == 400, r.text
    assert r.json()["detail"] == egeria_auth.NAMED_USER_NEEDS_PASSWORD_WORDS
    assert _Mint.calls == []


# ── a request that sends a password: unchanged in every mode ─────────────────────────────────────────

@pytest.mark.parametrize("mode", [LOCAL, DEMO, SERVER_MANAGED], indirect=True)
def test_password_request_is_unchanged(client, mode):
    r = _post(client, {"user_id": "peterprofile", "password": "own"})
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == "peterprofile"
    assert r.json()["platform_url"] == HOME
    assert _Mint.calls == [(HOME, "peterprofile", "own")]


@pytest.mark.parametrize("mode", [LOCAL, DEMO, SERVER_MANAGED], indirect=True)
def test_password_request_with_a_session_still_signs_in_as_sent(client, mode):
    r = _post(client, {"user_id": "peterprofile", "password": "own"},
              cookies=_session_cookie("erinoverview", _egeria_jwt("erinoverview")))
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == "peterprofile"
    assert _Mint.calls == [(HOME, "peterprofile", "own")]


@pytest.mark.parametrize("mode", [LOCAL, DEMO, SERVER_MANAGED], indirect=True)
def test_password_request_foreign_platform_gate_unchanged(client, mode):
    r = _post(client, {"url": FOREIGN, "user_id": "x", "password": SERVICE_PWD})
    assert r.status_code == 400, r.text
    assert _Mint.calls == []
