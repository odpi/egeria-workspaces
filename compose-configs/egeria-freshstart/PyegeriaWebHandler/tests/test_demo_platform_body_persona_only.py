"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Request bodies that carry a platform `url` and optionally the caller's own `user_pwd` (egeria_auth.PlatformBody)
follow the demo rule of POST /api/egeria-token. On the demo Portal (DEMO_MODE), a password sent with a user
name that is not a demo persona's is refused (403) as the body is parsed, before the route body runs. A body
with no user_id is held to the rule as EGERIA_USER, the user it is served as.

Unchanged:
- requests that present a sign-in token: clients then authenticate with the token only, and the body's
  credentials are ignored (Dr.Egeria: the token's user, as before);
- the PO-41 rule for a named user with no password (400);
- local and server-managed Portals.

This file is identical in both trees. No test reaches Egeria.
"""
import sys
from pathlib import Path
from typing import Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))
_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import demo_config  # noqa: E402
import egeria_auth  # noqa: E402
# The Dr.Egeria fakes (client, dispatcher) and helpers, shared with the token-identity tests.
from test_dr_egeria_token_identity import PETER, _document, _execute, world  # noqa: E402,F401
import dr_egeria_commands_handler as dch  # noqa: E402

# freshstart has /api/dr-egeria/execute only; quickstart also has execute-document
DRE_CALLS = [_execute] + ([_document] if hasattr(dch, "execute_document") else [])
DRE_IDS = ["execute", "execute-document"][:len(DRE_CALLS)]

HOME = "https://egeria.home.test:9443"
SERVICE_USER = "portal-service-user"
SERVICE_PWD = "service-secret"
PERSONA = "peterprofile"
NOT_A_PERSONA = "someone-not-in-the-persona-list"


class _Body(egeria_auth.PlatformBody):
    url: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


RAN = []


def _app():
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)

    @app.post("/body")
    async def route(body: _Body):
        RAN.append(body.user_id)
        return {"ran_as": body.user_id}
    return app


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER", SERVICE_USER)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    RAN.clear()


@pytest.fixture
def demo(monkeypatch):
    monkeypatch.setattr(demo_config, "DEMO_MODE", True)
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", False)


@pytest.fixture
def local(monkeypatch):
    monkeypatch.setattr(demo_config, "DEMO_MODE", False)
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", False)


@pytest.fixture
def client():
    return TestClient(_app(), raise_server_exceptions=False)


def _post(client, token=None, **body):
    return client.post("/body", json=body, headers={"X-Egeria-Token": token} if token else {})


# ── demo: persona / non-persona × password / no password ─────────────────────────────────────────────

def test_demo_persona_with_password_runs(client, demo):
    r = _post(client, user_id=PERSONA, user_pwd="persona-password")
    assert r.status_code == 200, r.text
    assert RAN == [PERSONA]


def test_demo_non_persona_with_password_is_403_before_the_route_runs(client, demo):
    r = _post(client, user_id=NOT_A_PERSONA, user_pwd="some-password")
    assert r.status_code == 403, r.text
    assert r.json()["detail"] == egeria_auth.DEMO_PERSONA_ONLY_WORDS
    assert RAN == []


def test_demo_password_with_no_user_is_held_to_the_rule_as_egeria_user(client, demo, monkeypatch):
    r = _post(client, user_pwd="some-password")          # served as EGERIA_USER, not a persona here
    assert r.status_code == 403, r.text
    assert RAN == []
    monkeypatch.setenv("EGERIA_USER", PERSONA)
    r = _post(client, user_pwd="persona-password")
    assert r.status_code == 200, r.text


def test_demo_persona_without_password_is_po41_unchanged(client, demo):
    r = _post(client, user_id=PERSONA)
    assert r.status_code == 400, r.text
    assert r.json()["detail"] == egeria_auth.NAMED_USER_NEEDS_PASSWORD_WORDS
    assert RAN == []


def test_demo_non_persona_without_password_is_po41_unchanged(client, demo):
    r = _post(client, user_id=NOT_A_PERSONA)
    assert r.status_code == 400, r.text
    assert r.json()["detail"] == egeria_auth.NAMED_USER_NEEDS_PASSWORD_WORDS
    assert RAN == []


def test_demo_no_user_no_password_runs_unchanged(client, demo):
    r = _post(client)
    assert r.status_code == 200, r.text
    assert RAN == [None]


def test_demo_with_a_token_the_body_credentials_are_not_checked(client, demo):
    r = _post(client, token=PETER, user_id=NOT_A_PERSONA, user_pwd="some-password")
    assert r.status_code == 200, r.text


# ── local: unchanged ─────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("user_id", [PERSONA, NOT_A_PERSONA])
def test_local_any_user_with_password_runs(client, local, user_id):
    r = _post(client, user_id=user_id, user_pwd="own")
    assert r.status_code == 200, r.text
    assert RAN == [user_id]


# ── Dr.Egeria on the demo Portal: the body's credentials are still ignored with a token ──────────────

@pytest.mark.parametrize("call", DRE_CALLS, ids=DRE_IDS)
def test_dr_egeria_demo_token_runs_as_the_token_user_ignoring_body_credentials(world, demo, call):
    r = call(world, PETER, user_id=NOT_A_PERSONA, user_pwd="some-password")
    assert r.status_code == 200, r.text
    [c] = world["clients"]
    assert c.user_id == "peterprofile" and c.token == PETER
    assert world["signins"] == []
    assert world["dispatched"] == 1


@pytest.mark.parametrize("call", DRE_CALLS, ids=DRE_IDS)
def test_dr_egeria_demo_without_a_token_runs_nothing(world, demo, monkeypatch, call):
    monkeypatch.setattr(world["dfh"], "DEMO_MODE", True)
    for body in ({"user_id": NOT_A_PERSONA, "user_pwd": "some-password"},
                 {"user_id": PERSONA, "user_pwd": "persona-password"}):
        r = call(world, None, **body)
        assert r.status_code in (401, 403), (body, r.text)
    assert world["clients"] == [] and world["dispatched"] == 0
