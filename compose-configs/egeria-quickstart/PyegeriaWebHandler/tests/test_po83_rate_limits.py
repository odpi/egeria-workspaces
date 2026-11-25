"""PO-83: the Portal's auth routes are rate-limited again, per REAL client IP (quickstart).

c0039ccc put slowapi limits on the auth routes; 085f9446 rewrote demo_auth_handler and they were lost, while
SlowAPIMiddleware stayed wired with nothing to enforce. Now: sign-in and the credential exchange 10/minute,
register / password reset / verification mail 5/hour. The key is the real client: X-Forwarded-For is read
only from the trusted proxy (the stack's Apache), so one user can't exhaust everyone's budget through Apache,
and a caller on egeria_network can't dodge its own limit by writing the header.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from slowapi import _rate_limit_exceeded_handler  # noqa: E402
from slowapi.errors import RateLimitExceeded  # noqa: E402
from slowapi.middleware import SlowAPIMiddleware  # noqa: E402
from starlette.requests import Request  # noqa: E402

import rate_limiter  # noqa: E402
from rate_limiter import client_ip, limiter  # noqa: E402

APACHE = "172.18.0.5"           # stands in for the stack's Apache container
NOTEBOOK = "172.18.0.9"         # a user's Jupyter container on egeria_network
ALICE, BOB = "203.0.113.10", "198.51.100.20"


@pytest.fixture(autouse=True)
def _fresh_limits(monkeypatch):
    monkeypatch.setenv("PORTAL_TRUSTED_PROXIES", APACHE)
    rate_limiter._resolved.update(spec=None, at=0.0, nets=())
    limiter.reset()
    yield
    limiter.reset()


def _req(peer, xff=None):
    headers = [(b"x-forwarded-for", xff.encode())] if xff is not None else []
    return Request({"type": "http", "method": "GET", "path": "/", "headers": headers, "client": (peer, 5000),
                    "query_string": b""})


# ── the key is the real client ───────────────────────────────────────────────────────────────────────────

def test_a_direct_caller_is_keyed_on_its_own_address():
    assert client_ip(_req(ALICE)) == ALICE


def test_x_forwarded_for_from_anyone_but_the_trusted_proxy_is_ignored():
    assert client_ip(_req(NOTEBOOK, xff=ALICE)) == NOTEBOOK     # a notebook can't pose as someone else


def test_behind_the_trusted_proxy_the_client_is_the_entry_it_appended():
    assert client_ip(_req(APACHE, xff=ALICE)) == ALICE


def test_entries_a_caller_wrote_to_the_left_are_ignored():
    # The caller sent "X-Forwarded-For: 1.2.3.4"; Apache appended the address it saw.
    assert client_ip(_req(APACHE, xff=f"1.2.3.4, {ALICE}")) == ALICE


def test_trusted_hops_are_skipped_right_to_left(monkeypatch):
    monkeypatch.setenv("PORTAL_TRUSTED_PROXIES", f"{APACHE},10.9.0.0/16")
    rate_limiter._resolved.update(spec=None)
    assert client_ip(_req(APACHE, xff=f"6.6.6.6, {ALICE}, 10.9.1.2")) == ALICE


def test_a_malformed_entry_where_the_proxy_wrote_trusts_none_of_it():
    assert client_ip(_req(APACHE, xff="not-an-ip")) == APACHE


def test_an_ipv4_mapped_peer_matches_the_proxy():
    assert client_ip(_req("::ffff:" + APACHE, xff=ALICE)) == ALICE
    assert client_ip(_req("::ffff:" + ALICE)) == ALICE


def test_a_proxy_named_by_hostname_is_resolved(monkeypatch):
    monkeypatch.setenv("PORTAL_TRUSTED_PROXIES", "the-apache")
    rate_limiter._resolved.update(spec=None)
    monkeypatch.setattr(rate_limiter.socket, "getaddrinfo",
                        lambda host, port: [(2, 1, 6, "", (APACHE, 0))] if host == "the-apache" else (_ for _ in ()).throw(OSError()))
    assert client_ip(_req(APACHE, xff=ALICE)) == ALICE


def test_a_proxy_name_that_does_not_resolve_trusts_nothing(monkeypatch):
    monkeypatch.setenv("PORTAL_TRUSTED_PROXIES", "no-such-apache")
    rate_limiter._resolved.update(spec=None)

    def fail(*a):
        raise OSError("no such host")
    monkeypatch.setattr(rate_limiter.socket, "getaddrinfo", fail)
    assert client_ip(_req(APACHE, xff=ALICE)) == APACHE


def test_no_header_means_no_name_lookup(monkeypatch):
    monkeypatch.setenv("PORTAL_TRUSTED_PROXIES", "some-apache")
    rate_limiter._resolved.update(spec=None)

    def boom(*a):
        raise AssertionError("resolved a proxy name for a request with no X-Forwarded-For")
    monkeypatch.setattr(rate_limiter.socket, "getaddrinfo", boom)
    assert client_ip(_req(ALICE)) == ALICE


def test_the_default_trusts_the_stacks_apache_containers(monkeypatch):
    monkeypatch.delenv("PORTAL_TRUSTED_PROXIES")
    assert rate_limiter.DEFAULT_TRUSTED_PROXIES == "quickstart-web-server,freshstart-web-server"


# ── the limits, through the same wiring as pyegeria_handler ──────────────────────────────────────────────

def _app(*routers):
    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    for r in routers:
        app.include_router(r)
    return app


def _hammer(app, path, n, peer, json=None, xff=None):
    c = TestClient(app, client=(peer, 5000))
    headers = {"X-Forwarded-For": xff} if xff else {}
    return [c.post(path, json=json or {}, headers=headers).status_code for _ in range(n)]


def _limited(statuses, allowed):
    assert 429 not in statuses[:allowed], statuses
    assert statuses[allowed:] and all(s == 429 for s in statuses[allowed:]), statuses


class _NoUsers:
    """A demo-db session in which no account exists: every lookup finds nothing."""
    def __getattr__(self, name):
        return lambda *a, **k: self

    def first(self):
        return None


@pytest.fixture
def auth_app():
    import demo_auth_handler
    from demo_db import get_db
    app = _app(demo_auth_handler.router)
    app.dependency_overrides[get_db] = lambda: _NoUsers()
    return app


LOGIN = {"email": "someone@example.com", "password": "wrong-password"}


def test_the_eleventh_login_in_a_minute_is_refused(auth_app):
    statuses = _hammer(auth_app, "/api/auth/login", 11, ALICE, json=LOGIN)
    assert statuses[:10] == [401] * 10
    _limited(statuses, 10)


def test_another_address_is_not_affected(auth_app):
    _hammer(auth_app, "/api/auth/login", 11, ALICE, json=LOGIN)
    assert _hammer(auth_app, "/api/auth/login", 1, BOB, json=LOGIN) == [401]


def test_users_behind_apache_each_get_their_own_budget(auth_app):
    _limited(_hammer(auth_app, "/api/auth/login", 11, APACHE, json=LOGIN, xff=ALICE), 10)
    assert _hammer(auth_app, "/api/auth/login", 1, APACHE, json=LOGIN, xff=BOB) == [401]


def test_a_notebook_cannot_dodge_its_limit_by_writing_x_forwarded_for(auth_app):
    for i in range(10):
        _hammer(auth_app, "/api/auth/login", 1, NOTEBOOK, json=LOGIN, xff=f"192.0.2.{i}")
    assert _hammer(auth_app, "/api/auth/login", 1, NOTEBOOK, json=LOGIN, xff="192.0.2.99") == [429]


@pytest.mark.parametrize("path,body", [
    ("/api/auth/register", {"display_name": "x", "email": "a@example.com", "password": "short"}),
    ("/api/auth/forgot-password", {"email": "a@example.com"}),
    ("/api/auth/resend-verification", {"email": "a@example.com"}),
    ("/api/auth/reset-password", {"token": "nope", "password": "a-new-password-123"}),
])
def test_account_and_mail_routes_allow_five_an_hour(auth_app, path, body):
    statuses = _hammer(auth_app, path, 6, ALICE, json=body)
    _limited(statuses, 5)
    assert _hammer(auth_app, path, 1, BOB, json=body) != [429]


def test_the_credential_exchange_is_limited_in_the_real_app(monkeypatch):
    """Through pyegeria_handler.app itself: its SlowAPIMiddleware and the decorator count the request once."""
    monkeypatch.setenv("EGERIA_PLATFORM_URL", "https://127.0.0.1:9")
    import pyegeria_handler
    statuses = _hammer(pyegeria_handler.app, "/api/egeria-token", 11, ALICE, json={})
    _limited(statuses, 10)
    assert _hammer(pyegeria_handler.app, "/api/egeria-token", 1, BOB, json={}) != [429]


def test_every_limited_route_is_decorated():
    import demo_auth_handler
    import tech_catalog_handler
    src = Path(demo_auth_handler.__file__).read_text() + Path(tech_catalog_handler.__file__).read_text()
    for route, limit in [('"/api/auth/login"', "LOGIN_LIMIT"), ('"/api/egeria-token"', "LOGIN_LIMIT"),
                         ('"/api/auth/register"', "ACCOUNT_EMAIL_LIMIT"), ('"/api/auth/forgot-password"', "ACCOUNT_EMAIL_LIMIT"),
                         ('"/api/auth/reset-password"', "ACCOUNT_EMAIL_LIMIT"),
                         ('"/api/auth/resend-verification"', "ACCOUNT_EMAIL_LIMIT")]:
        at = src.index(route)
        assert f"@limiter.limit({limit})" in src[at:at + 300], route
    assert rate_limiter.LOGIN_LIMIT == "10/minute" and rate_limiter.ACCOUNT_EMAIL_LIMIT == "5/hour"
