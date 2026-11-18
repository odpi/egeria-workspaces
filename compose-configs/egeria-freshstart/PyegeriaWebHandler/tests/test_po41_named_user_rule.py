"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-41, the central rule: a request naming an Egeria user other than EGERIA_USER must bring a sign-in
token or that user's password. Every route is covered by construction:
  - query ?user_id= is checked by EgeriaTokenMiddleware before routing (a query never carries a password);
  - a body user_id is checked by PlatformBody's validator (user_pwd is the password sent);
  - /api/egeria-token uses the same rule and words.
The route sweep below collects every route from the app, so a new route is covered without a new test,
and the scans keep a new body model or a raw body read from going around the rule.

No test reaches Egeria: outbound pyegeria traffic is refused.
"""
import ast
import inspect
import re
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import egeria_auth  # noqa: E402

HOME = "https://egeria.home.test:9443"
SERVICE_USER = "portal-service-user"
SERVICE_PWD = "service-secret"
WORDS = egeria_auth.NAMED_USER_NEEDS_PASSWORD_WORDS


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER", SERVICE_USER)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})

    async def send(self, request, *a, **k):
        raise AssertionError(f"outbound call to {request.url}")
    monkeypatch.setattr(httpx.AsyncClient, "send", send)


@pytest.fixture(scope="module")
def app():
    import pyegeria_handler as handler
    return handler.app


@pytest.fixture
def client(app):
    return TestClient(app, raise_server_exceptions=False)


def _walk(routes, prefix=""):
    """Every APIRoute with its full path. Newer FastAPI keeps an included router as one entry that
    points at the original router (and its prefix) instead of copying its routes into app.routes."""
    for r in routes:
        if isinstance(r, APIRoute):
            yield prefix + r.path, r
        elif getattr(r, "original_router", None) is not None:
            ctx = getattr(r, "include_context", None)
            yield from _walk(r.original_router.routes, prefix + (getattr(ctx, "prefix", "") or ""))


def _routes(app):
    seen, out = set(), []
    for path, r in _walk(app.routes):
        if (path, tuple(sorted(r.methods))) not in seen:
            seen.add((path, tuple(sorted(r.methods))))
            r.full_path = path
            out.append(r)
    return out


def _path(route):
    return re.sub(r"\{[^}]+\}", "x", getattr(route, "full_path", route.path))


def _query_user_routes(app):
    return [r for r in _routes(app) if any(q.name == "user_id" for q in r.dependant.query_params)]


def _platform_body_routes(app):
    out = []
    for r in _routes(app):
        for b in r.dependant.body_params:
            t = getattr(b, "type_", None) or getattr(getattr(b, "field_info", None), "annotation", None)
            t = getattr(b, "annotation", None) or t
            if inspect.isclass(t) and issubclass(t, egeria_auth.PlatformBody) and "user_id" in t.model_fields:
                out.append((r, t))
    return out


def _sample(annotation):
    """A valid value for a required field of this type (enough for the body to reach the validator)."""
    import typing
    origin = typing.get_origin(annotation)
    if origin in (list, tuple, set) or annotation in (list, tuple, set):
        return []
    if origin is dict or annotation is dict:
        return {}
    if origin is typing.Union or str(origin) == "types.UnionType":
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        return _sample(args[0]) if args else None
    if origin is typing.Literal:
        return typing.get_args(annotation)[0]
    if inspect.isclass(annotation) and hasattr(annotation, "model_fields"):
        return _required_body(annotation, ())
    if annotation is bool:
        return False
    if annotation in (int, float):
        return 1
    return "x"


def _required_body(model, skip):
    return {k: _sample(f.annotation) for k, f in model.model_fields.items() if f.is_required() and k not in skip}


# ── the rule itself ──────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("user_id,pwd,token,refused", [
    ("peterprofile", False, None, True),
    ("peterprofile", True, None, False),
    ("peterprofile", False, "tok", False),
    (SERVICE_USER, False, None, False),
    (None, False, None, False),
    ("", False, None, False),
])
def test_named_user_refusal(user_id, pwd, token, refused):
    r = egeria_auth.named_user_refusal(user_id, pwd, token)
    assert (r is not None) == refused
    if refused:
        assert r.status_code == 400 and r.detail == WORDS


# ── every query-user route ───────────────────────────────────────────────────────────────────────────

def test_there_are_query_user_routes_to_sweep(app):
    assert len(_query_user_routes(app)) >= 20


def test_every_query_user_route_refuses_a_named_user_without_a_token(app, client):
    bad = []
    for r in _query_user_routes(app):
        method = sorted(r.methods)[0]
        resp = client.request(method, _path(r), params={"user_id": "peterprofile"})
        if resp.status_code != 400 or resp.json().get("detail") != WORDS:
            bad.append(f"{method} {r.path}: {resp.status_code}")
    assert bad == []


def test_a_percent_encoded_user_id_key_is_refused_too(client, app):
    r = _query_user_routes(app)[0]
    resp = client.request(sorted(r.methods)[0], _path(r) + "?%75ser_id=peterprofile")
    assert resp.status_code == 400 and resp.json()["detail"] == WORDS


def test_the_service_user_or_a_token_passes_the_rule(app, client):
    """Neither is refused with the PO-41 words (the route then runs; it may fail later without Egeria)."""
    for r in _query_user_routes(app)[:15]:
        method = sorted(r.methods)[0]
        for params, headers in (({"user_id": SERVICE_USER}, {}),
                                ({"user_id": "peterprofile"}, {"X-Egeria-Token": "some-token"}),
                                ({}, {})):
            resp = client.request(method, _path(r), params=params, headers=headers)
            detail = resp.json().get("detail") if resp.headers.get("content-type", "").startswith("application/json") else None
            assert detail != WORDS, f"{method} {r.path} {params} {headers}"


# ── every PlatformBody route with a user_id ─────────────────────────────────────────────────────────

def test_every_platform_body_route_refuses_a_named_user_without_a_password(app, client):
    routes = _platform_body_routes(app)
    assert len(routes) >= 5
    bad = []
    for r, model in routes:
        required = _required_body(model, ("user_id",))
        body = {**required, "user_id": "peterprofile"}
        resp = client.request(sorted(r.methods)[0], _path(r), json=body)
        detail = resp.json().get("detail") if resp.headers.get("content-type", "").startswith("application/json") else None
        if resp.status_code != 400 or detail != WORDS:
            bad.append(f"{r.path}: {resp.status_code} {str(detail)[:80]}")
    assert bad == []


def test_a_platform_body_with_its_password_passes_the_rule(app, client):
    for r, model in _platform_body_routes(app):
        if "user_pwd" not in model.model_fields:
            continue
        required = _required_body(model, ("user_id", "user_pwd"))
        resp = client.request(sorted(r.methods)[0], _path(r),
                              json={**required, "user_id": "peterprofile", "user_pwd": SERVICE_PWD})
        detail = resp.json().get("detail") if resp.headers.get("content-type", "").startswith("application/json") else None
        assert detail != WORDS, r.path


# ── scans: nothing goes around the rule ─────────────────────────────────────────────────────────────

_HANDLER_FILES = sorted(p for p in _MODULE_DIR.glob("*.py") if not p.name.startswith("test_"))

# Body models with a user_id that is not an Egeria sign-in, or that always require the password.
_BODY_USER_ID_ALLOWED = {
    "_UserStatusBody": "the user account being changed (admin only), not who signs in",
    "ProcessRequest": "user_pass is a required field: the password always comes with it",
    "LoginRequest": "a Portal account sign-in (freshstart), checked with its password against the Portal's users",
    "ChangePasswordRequest": "a Portal account (freshstart), checked with its current password",
}


def test_every_body_model_with_a_user_id_is_a_platform_body():
    bad = []
    for p in _HANDLER_FILES:
        for c in ast.walk(ast.parse(p.read_text())):
            if not isinstance(c, ast.ClassDef):
                continue
            fields = [n.target.id for n in c.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
            bases = [ast.unparse(b) for b in c.bases]
            if "user_id" in fields and "PlatformBody" not in bases and c.name not in _BODY_USER_ID_ALLOWED \
                    and any(b in ("BaseModel",) or b.endswith("Body") for b in bases):
                bad.append(f"{p.name}:{c.name}")
    assert bad == [], f"a request body with user_id must subclass PlatformBody (PO-41): {bad}"


def test_no_route_reads_user_id_from_a_raw_body():
    """A raw `await request.json()` with .get("user_id") skips PlatformBody; only the token endpoint may,
    and it applies named_user_refusal itself."""
    bad = []
    for p in _HANDLER_FILES:
        for fn in ast.walk(ast.parse(p.read_text())):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            src = ast.unparse(fn)
            if "request.json()" in src and re.search(r"\.get\(['\"]user_id['\"]\)", src):
                if not (p.name == "tech_catalog_handler.py" and fn.name == "get_egeria_bearer_token"
                        and "named_user_refusal(" in src):
                    bad.append(f"{p.name}:{fn.name}")
    assert bad == []
