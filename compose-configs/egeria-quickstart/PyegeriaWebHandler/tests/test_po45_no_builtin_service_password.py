"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-45 (TR-12 shape): no built-in service password. A deployment that forgot EGERIA_USER_PASSWORD used
to sign in with the well-known demo password "secret". Now:
  - egeria_auth.service_password() returns the configured password, or raises ServicePasswordMissing
    (503, in words) before any Egeria call;
  - every handler gets the password from it;
  - the scan below keeps a "secret" default (or any literal password default) from coming back.
"""
import ast
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import egeria_auth  # noqa: E402

_HANDLER_FILES = sorted(p for p in _MODULE_DIR.glob("*.py") if not p.name.startswith("test_"))
WORDS = egeria_auth.SERVICE_PASSWORD_MISSING_WORDS


@pytest.fixture
def no_outbound(monkeypatch):
    calls = []

    async def send(self, request, *a, **k):
        calls.append(str(request.url))
        raise AssertionError(f"outbound call to {request.url}")
    monkeypatch.setattr(httpx.AsyncClient, "send", send)
    return calls


# ── the getter ───────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("value", [None, ""])
def test_unset_or_empty_refuses_in_words(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    else:
        monkeypatch.setenv("EGERIA_USER_PASSWORD", value)
    with pytest.raises(egeria_auth.ServicePasswordMissing) as exc:
        egeria_auth.service_password()
    assert exc.value.status_code == 503 and WORDS in exc.value.detail
    assert egeria_auth.configured_service_password() is None
    assert egeria_auth.is_caller_password("anything") is True        # never raises, nothing to compare to


def test_set_is_returned_unchanged(monkeypatch):
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "configured-pw")
    assert egeria_auth.service_password() == "configured-pw"
    assert egeria_auth.is_caller_password("configured-pw") is False


def test_the_startup_no_longer_sets_a_default(monkeypatch):
    src = (_MODULE_DIR / "pyegeria_handler.py").read_text()
    assert 'setdefault("EGERIA_USER_PASSWORD"' not in src


# ── a route with no token and no password configured ────────────────────────────────────────────────

def test_a_service_route_refuses_in_words_with_no_egeria_call(monkeypatch, no_outbound):
    """tech_catalog's client factories take the service password through _creds."""
    monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    import tech_catalog_handler as tc
    with pytest.raises(egeria_auth.ServicePasswordMissing):
        tc._creds(None, None, None, None)
    assert tc._creds(None, None, None, "callers-own")[3] == "callers-own"   # a sent password needs no default
    assert no_outbound == []


def test_the_token_endpoint_refuses_in_words(monkeypatch, no_outbound):
    monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    import pyegeria_handler as handler
    r = TestClient(handler.app, raise_server_exceptions=False).post("/api/egeria-token", json={})
    assert r.status_code == 503 and WORDS in r.json()["detail"], r.text
    assert no_outbound == []


# ── scan: nothing reintroduces a built-in password ──────────────────────────────────────────────────

def _env_default_literal(node):
    """For os.environ.get(KEY, "<literal>") / os.getenv(KEY, "<literal>") with a PASSWORD-ish KEY: the
    literal; else None."""
    if not (isinstance(node, ast.Call) and len(node.args) >= 2):
        return None
    f = node.func
    name = ast.unparse(f)
    if name not in ("os.environ.get", "os.getenv", "environ.get", "getenv"):
        return None
    key, default = node.args[0], node.args[1]
    if isinstance(key, ast.Constant) and isinstance(key.value, str) and isinstance(default, ast.Constant) \
            and isinstance(default.value, str) and default.value \
            and any(w in key.value.upper() for w in ("PASSWORD", "PWD", "PASS")):
        return key.value, default.value
    return None


# Reported, not changed in PO-45 (database credentials, not the Egeria service password; their defaults are
# used by the database set-up across the stack): listed here by name so a new one still fails.
_REPORTED = {("demo_config.py", "DEMO_DB_PASSWORD"), ("demo_config.py", "EGERIA_META_DB_PASSWORD")}


def test_no_handler_file_carries_a_built_in_password():
    bad = []
    for p in _HANDLER_FILES:
        tree = ast.parse(p.read_text())
        for node in ast.walk(tree):
            hit = _env_default_literal(node)
            if hit and (p.name, hit[0]) not in _REPORTED:
                bad.append(f"{p.name}:{node.lineno}: {hit[0]} defaults to a literal")
            if isinstance(node, ast.Constant) and node.value == "secret":
                bad.append(f"{p.name}:{node.lineno}: the literal 'secret'")
            # dict.get("password", "<literal>") — a persona/profile password fallback
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get" \
                    and len(node.args) >= 2 and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str) and "pass" in node.args[0].value.lower() \
                    and isinstance(node.args[1], ast.Constant) and node.args[1].value \
                    and (p.name, node.args[0].value) not in _REPORTED:
                bad.append(f"{p.name}:{node.lineno}: .get({node.args[0].value!r}, <literal>)")
    assert bad == [], bad


def test_every_handler_gets_the_service_password_from_the_getter():
    """No handler reads EGERIA_USER_PASSWORD itself (only egeria_auth does)."""
    bad = []
    for p in _HANDLER_FILES:
        if p.name == "egeria_auth.py":
            continue
        for node in ast.walk(ast.parse(p.read_text())):
            if isinstance(node, ast.Call) and ast.unparse(node.func) in ("os.environ.get", "os.getenv") \
                    and node.args and isinstance(node.args[0], ast.Constant) \
                    and node.args[0].value == "EGERIA_USER_PASSWORD":
                bad.append(f"{p.name}:{node.lineno}")
            if isinstance(node, ast.Subscript) and ast.unparse(node.value) == "os.environ" \
                    and isinstance(node.slice, ast.Constant) and node.slice.value == "EGERIA_USER_PASSWORD" \
                    and isinstance(node.ctx, ast.Load):
                bad.append(f"{p.name}:{node.lineno} (os.environ[...])")
    assert bad == [], bad
