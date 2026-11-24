"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-78: the freshstart Portal (SERVER_MANAGED_AUTH) refuses a caller with no Portal session.

Before the gate, every read route that builds its client with apply_token answered an anonymous caller 200,
running as the Portal's service user (kind cluster proof, 2026-11-22: GET /api/operations/platforms gave
platform names and GUIDs to a request with no cookie, or a bogus one). Now:
  - no session, a bogus / forged / expired session, or an X-Egeria-Token alone -> 401 JSON on /api/*,
    302 to /login on a page, whatever headers (X-Egeria-Edge) the request carries;
  - a signed-in caller (a demo_token JWT as /api/auth/login sets it) reaches the route;
  - the public list (health, sign-in page and its calls, static assets, the credential exchange) needs none;
  - with SERVER_MANAGED_AUTH false (the local posture) nothing changes.

Runs in a clean checkout: the signing key is a test key set on demo_config (as
test_report_spec_sync_redaction.py does), and no test reaches Egeria (the platform URL refuses connections
at once; the credential exchange's client is replaced).

Both process modes: the gate reads demo_config.SERVER_MANAGED_AUTH per request, so its checks run whatever
the process's SERVER_MANAGED_AUTH is. The sign-in routes (/api/auth/*, /api/platform/org-name, the /login
and /register pages' freshstart behaviour) are mounted at import from that env, so the cases that need
them (`signin_routes`) are skipped, with the reason, in a process started with SERVER_MANAGED_AUTH=false.
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

SIGNING_KEY = "po78-test-only-signing-key-0123456789abcdef"
UNREACHABLE = "https://127.0.0.1:9"      # refuses at once, so an ungated route fails fast instead of hanging

# A sample of read routes that build their Egeria client with apply_token (the service user when anonymous).
READ_ROUTES = [
    "/api/operations/platforms",
    "/api/tech-catalog/infrastructure/types",
    "/api/tech-catalog/software-capabilities",
    "/api/digital-products/catalogs",
    "/api/valid-values/properties",
    "/api/audit/platforms",
]
PAGES = ["/egeria-explorer", "/tech-catalog", "/egeria-operations", "/egeria-audit"]


def _egeria_jwt(sub, life=3600):
    payload = base64.urlsafe_b64encode(json.dumps({"sub": sub, "exp": time.time() + life}).encode())
    return "hdr." + payload.decode().rstrip("=") + ".sig"


def _session(user_id="peterprofile", key=SIGNING_KEY, life=timedelta(hours=1)):
    from jose import jwt
    claims = {"sub": user_id, "role": "user", "display_name": user_id,
              "egeria_token": _egeria_jwt(user_id), "exp": datetime.utcnow() + life}
    return jwt.encode(claims, key, algorithm="HS256")


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
    monkeypatch.setenv("EGERIA_PLATFORM_URL", UNREACHABLE)
    monkeypatch.setenv("EGERIA_USER", "portal-service-user")
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "service-secret")
    monkeypatch.setattr(demo_config, "JWT_SECRET", SIGNING_KEY)
    monkeypatch.setattr(demo_config, "DEMO_MODE", False)
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", True)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    import pyegeria
    monkeypatch.setattr(pyegeria, "AssetMaker", _Mint)
    _Mint.calls = []


@pytest.fixture(scope="module")
def app():
    import pyegeria_handler as handler
    return handler.app


@pytest.fixture
def signin_routes(app):
    """Skip unless this process mounted freshstart's sign-in routes (SERVER_MANAGED_AUTH true at import)."""
    import pyegeria_handler as handler
    # The same import-time flag that decides the mounting (pyegeria_handler: DEMO_MODE or SERVER_MANAGED_AUTH).
    # Not app.routes: FastAPI >= 0.165 nests included routers there, so their paths are not listed.
    if not handler._LOGIN_REQUIRED:
        pytest.skip("sign-in routes are mounted at import only when SERVER_MANAGED_AUTH is true; "
                    "this process started with it false")


@pytest.fixture
def client(app):
    return TestClient(app, raise_server_exceptions=False, follow_redirects=False)   # no `with`: no lifespan


def _get(client, path, cookie=None, headers=None):
    client.cookies.clear()
    if cookie is not None:
        client.cookies.set("demo_token", cookie)
    return client.get(path, headers=headers or {})


def _refused_api(r):
    assert r.status_code == 401, (r.status_code, r.text[:300])
    assert r.json() == {"detail": "Authentication required"}


def _refused_page(r):
    assert r.status_code == 302, (r.status_code, r.text[:300])
    assert r.headers["location"] == "/login"


# ── no session, or not a real one ─────────────────────────────────────────────────────────────────────

NOT_A_SESSION = {
    "none": None,
    "bogus": "not-a-jwt",
    "forged": _session(key="not-the-portal-key-0123456789abcdef"),
    "expired": _session(life=timedelta(seconds=-60)),
}


@pytest.mark.parametrize("cookie", NOT_A_SESSION.values(), ids=NOT_A_SESSION.keys())
@pytest.mark.parametrize("path", READ_ROUTES)
def test_read_route_without_a_session_is_401(client, path, cookie):
    _refused_api(_get(client, path, cookie))
    assert _Mint.calls == []


@pytest.mark.parametrize("cookie", NOT_A_SESSION.values(), ids=NOT_A_SESSION.keys())
@pytest.mark.parametrize("path", PAGES)
def test_page_without_a_session_redirects_to_login(client, path, cookie):
    _refused_page(_get(client, path, cookie))


@pytest.mark.parametrize("path", ["/api/operations/platforms", "/api/audit/platforms"])
def test_bogus_bearer_header_is_401(client, path):
    _refused_api(_get(client, path, headers={"Authorization": "Bearer not-a-jwt"}))


@pytest.mark.parametrize("path", ["/api/operations/platforms", "/api/valid-values/properties"])
def test_an_egeria_token_alone_is_not_a_portal_session(client, path):
    _refused_api(_get(client, path, headers={"X-Egeria-Token": _egeria_jwt("peterprofile")}))


@pytest.mark.parametrize("edge", [{"X-Egeria-Edge": "1"}, {}], ids=["with-edge-header", "without-edge-header"])
def test_edge_header_makes_no_difference(client, edge):
    """Freshstart's Apache never sets X-Egeria-Edge and :8000 may be published, so no exemption either way."""
    _refused_api(_get(client, "/api/operations/platforms", headers=edge))
    _refused_page(_get(client, "/egeria-explorer", headers=edge))


def test_no_signing_key_fails_closed(client, monkeypatch):
    cookie = _session()
    monkeypatch.setattr(demo_config, "JWT_SECRET", "")
    _refused_api(_get(client, "/api/operations/platforms", cookie))
    _refused_page(_get(client, "/egeria-explorer", cookie))


@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_writes_without_a_session_are_401(client, method):
    client.cookies.clear()
    r = getattr(client, method)("/api/favorites")
    _refused_api(r)


def test_dr_egeria_and_openapi_without_a_session_are_401(client):
    client.cookies.clear()
    _refused_api(client.post("/dr-egeria/process", json={}))
    _refused_api(_get(client, "/openapi.json"))
    _refused_api(_get(client, "/docs"))


# ── signed in ─────────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("path", PAGES)
def test_signed_in_user_gets_the_page(client, path):
    r = _get(client, path, _session())
    assert r.status_code == 200, (r.status_code, r.text[:300])
    assert "text/html" in r.headers["content-type"]


@pytest.mark.parametrize("path", READ_ROUTES)
def test_signed_in_user_reaches_the_read_route(client, path):
    """The gate lets the request through; the route then fails on the unreachable test platform, which is
    the route's answer (not the gate's 401 or a redirect)."""
    r = _get(client, path, _session())
    assert r.status_code not in (401, 302), (r.status_code, r.text[:300])
    assert r.json() != {"detail": "Authentication required"}


def test_signed_in_bearer_header_counts_as_a_session(client):
    r = _get(client, "/egeria-explorer", headers={"Authorization": "Bearer " + _session()})
    assert r.status_code == 200


def test_signed_in_user_gets_auth_me(client, signin_routes):
    r = _get(client, "/api/auth/me", _session())
    assert r.status_code == 200
    assert r.json()["authenticated"] is True and r.json()["user_id"] == "peterprofile"


# ── the public list ───────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("path", ["/", "/privacy", "/static/egeria-logo.png"])
def test_public_paths_need_no_session(client, path):
    r = _get(client, path)
    assert r.status_code == 200, (r.status_code, r.text[:300])


@pytest.mark.parametrize("path", ["/login", "/api/platform/org-name"])
def test_sign_in_page_and_its_heading_need_no_session(client, signin_routes, path):
    r = _get(client, path)
    assert r.status_code == 200, (r.status_code, r.text[:300])


def test_register_still_sends_to_login(client, signin_routes):
    r = _get(client, "/register")
    assert r.status_code in (302, 307) and r.headers["location"] == "/login"


def test_auth_me_without_a_session_says_not_signed_in(client, signin_routes):
    r = _get(client, "/api/auth/me", "not-a-jwt")
    assert r.status_code == 200
    assert r.json()["authenticated"] is False


def test_login_route_is_reachable_without_a_session(client, signin_routes):
    """The sign-in itself: the gate does not answer it (a bad body is the route's 422, not the gate's 401)."""
    client.cookies.clear()
    r = client.post("/api/auth/login", json={})
    assert r.status_code == 422, (r.status_code, r.text[:300])


def test_credential_exchange_with_a_password_needs_no_session(client):
    """The helm canary's path: a non-personal account's own password, through the front door."""
    client.cookies.clear()
    r = client.post("/api/egeria-token", json={"user_id": "canary", "password": "canary-pw", "url": UNREACHABLE})
    assert r.status_code == 200, (r.status_code, r.text[:300])
    assert _Mint.calls == [(UNREACHABLE, "canary", "canary-pw")]


def test_credential_exchange_without_a_password_still_needs_a_session(client):
    """PO-68 still holds behind the gate: no password and no session mints nothing."""
    client.cookies.clear()
    r = client.post("/api/egeria-token", json={})
    assert r.status_code == 401
    assert "Sign in to the Portal first" in r.json()["detail"]
    assert _Mint.calls == []


def test_cors_preflight_is_not_refused(client):
    client.cookies.clear()
    r = client.options("/api/operations/platforms",
                       headers={"Origin": "app://obsidian.md", "Access-Control-Request-Method": "GET"})
    assert r.status_code == 200


# ── the local posture ─────────────────────────────────────────────────────────────────────────────────

def test_gate_is_off_when_server_managed_auth_is_false(client, monkeypatch):
    monkeypatch.setattr(demo_config, "SERVER_MANAGED_AUTH", False)
    r = _get(client, "/egeria-explorer")
    assert r.status_code == 200
    r = _get(client, "/api/operations/platforms")
    assert r.status_code != 401
