"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

POST /api/egeria-token on the demo Portal (DEMO_MODE): a password may be sent only with a demo persona's
user name. The personas are the server's own list (personas.json, the file POST /api/demo/select-persona
reads). Any other user name with a password is refused with 403 and nothing is minted. Unchanged:
  - the no-password path (PO-41, PO-68): a signed-in user gets the Portal's own user's token; no session is 401;
  - the server-managed (freshstart) path;
  - a local Portal (neither flag): any user name with that user's password, as before.

This file is identical in both trees. No test reaches Egeria: the token-minting client is replaced.
"""
import json
import sys
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
SERVICE_USER = "portal-service-user"
SERVICE_PWD = "service-secret"
SIGNING_KEY = "persona-only-test-signing-key-0123456789abcdef"
HAS_DEMO_GATE = (_MODULE_DIR / "demo_auth_gate.py").exists()     # quickstart only
PERSONAS = sorted(json.loads((_MODULE_DIR / "personas.json").read_text()))
PERSONA = "peterprofile"
NOT_A_PERSONA = "someone-not-in-the-persona-list"

LOCAL, DEMO, SERVER_MANAGED = "local", "demo", "server-managed"
MODES = {LOCAL: (False, False), DEMO: (True, False), SERVER_MANAGED: (False, True)}
_VERIFIED = set()


class _Mint:
    calls = []

    def __init__(self, view_server=None, platform_url=None, user_id=None, user_pwd=None):
        self.args = (platform_url, user_id, user_pwd)

    async def _async_create_egeria_bearer_token(self):
        _Mint.calls.append(self.args)
        return f"token-for-{self.args[1]}"


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


def _session_cookie(user_id):
    from jose import jwt
    claims = {"sub": user_id, "role": "user", "display_name": user_id,
              "exp": datetime.utcnow() + timedelta(hours=1)}
    _VERIFIED.add(user_id)
    return {"demo_token": jwt.encode(claims, SIGNING_KEY, algorithm="HS256")}


def _post(client, body, cookies=None, headers=None):
    client.cookies.clear()
    for k, v in (cookies or {}).items():
        client.cookies.set(k, v)
    return client.post("/api/egeria-token", json=body, headers=headers or {})


def test_persona_list_is_the_servers_own():
    assert PERSONA in PERSONAS and NOT_A_PERSONA not in PERSONAS
    assert egeria_auth.demo_persona_ids() == frozenset(PERSONAS)


def test_unreadable_persona_list_accepts_no_name(monkeypatch, tmp_path):
    monkeypatch.setattr(egeria_auth, "PERSONAS_FILE", str(tmp_path / "missing.json"))
    monkeypatch.setattr(demo_config, "DEMO_MODE", True)
    assert egeria_auth.demo_persona_ids() == frozenset()
    refusal = egeria_auth.demo_persona_refusal(PERSONA, True)
    assert refusal is not None and refusal.status_code == 403


# ── demo (DEMO_MODE) ─────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode", [DEMO], indirect=True)
@pytest.mark.parametrize("persona", PERSONAS)
def test_demo_signed_in_persona_with_password_is_allowed(client, mode, persona):
    r = _post(client, {"user_id": persona, "password": "persona-password"},
              cookies=_session_cookie("someone@example.org"))
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == persona
    assert _Mint.calls == [(HOME, persona, "persona-password")]


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
@pytest.mark.parametrize("user_id", [NOT_A_PERSONA, SERVICE_USER, "PeterProfile", " peterprofile"])
def test_demo_signed_in_non_persona_with_password_is_403(client, mode, user_id):
    r = _post(client, {"user_id": user_id, "password": "some-password"},
              cookies=_session_cookie("someone@example.org"))
    assert r.status_code == 403, r.text
    assert r.json()["detail"] == egeria_auth.DEMO_PERSONA_ONLY_WORDS
    assert "token" not in r.json()
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_password_with_no_user_name_is_403_unless_the_portal_user_is_a_persona(client, mode, monkeypatch):
    cookies = _session_cookie("someone@example.org")
    r = _post(client, {"password": "some-password"}, cookies=cookies)      # resolves to EGERIA_USER
    assert r.status_code == 403, r.text
    assert _Mint.calls == []
    monkeypatch.setenv("EGERIA_USER", PERSONA)                              # the demo's own default
    r = _post(client, {"password": "persona-password"}, cookies=cookies)
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == PERSONA


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_no_session_no_password_is_401_unchanged(client, mode):
    r = _post(client, {})
    assert r.status_code == 401, r.text
    assert "Sign in to the Portal first" in r.json()["detail"]
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_no_session_through_the_gate_is_401_unchanged(app, mode):
    if not HAS_DEMO_GATE:
        pytest.skip("only quickstart has DemoAuthGateMiddleware")
    from demo_auth_gate import DemoAuthGateMiddleware
    gated = TestClient(DemoAuthGateMiddleware(app), raise_server_exceptions=False)
    for body in ({}, {"user_id": PERSONA, "password": "persona-password"},
                 {"user_id": NOT_A_PERSONA, "password": "some-password"}):
        r = gated.post("/api/egeria-token", json=body, headers={"X-Egeria-Edge": "1"})
        assert r.status_code == 401, (body, r.text)
    assert _Mint.calls == []


@pytest.mark.parametrize("mode", [DEMO], indirect=True)
def test_demo_signed_in_no_password_is_unchanged(client, mode):
    r = _post(client, {}, cookies=_session_cookie("someone@example.org"))
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == SERVICE_USER
    assert _Mint.calls == [(HOME, SERVICE_USER, SERVICE_PWD)]


# ── local and server-managed: unchanged ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode", [LOCAL], indirect=True)
@pytest.mark.parametrize("user_id", [PERSONA, NOT_A_PERSONA, SERVICE_USER])
def test_local_any_user_with_password_is_unchanged(client, mode, user_id):
    r = _post(client, {"user_id": user_id, "password": "own"})
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == user_id
    assert _Mint.calls == [(HOME, user_id, "own")]


@pytest.mark.parametrize("mode", [SERVER_MANAGED], indirect=True)
def test_server_managed_password_request_is_unchanged(client, mode):
    r = _post(client, {"user_id": NOT_A_PERSONA, "password": "own"})
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == NOT_A_PERSONA
    assert _Mint.calls == [(HOME, NOT_A_PERSONA, "own")]


@pytest.mark.parametrize("mode", [LOCAL, DEMO, SERVER_MANAGED], indirect=True)
def test_platform_gate_still_runs_first(client, mode):
    r = _post(client, {"url": "https://other.example.com", "user_id": NOT_A_PERSONA, "password": "x"})
    assert r.status_code == 400, r.text
    assert _Mint.calls == []
