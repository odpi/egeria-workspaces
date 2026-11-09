# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Shared Egeria credential seam (LE-4).

Token-capable auth without touching endpoint signatures. A pure-ASGI
middleware stashes any incoming ``X-Egeria-Token`` header into a contextvar;
each handler's client factory calls :func:`apply_token` instead of
``client.create_egeria_bearer_token()``. When a token was supplied the client
reuses it (``set_bearer_token``); otherwise it falls back to obtaining a fresh
token from the client's configured ``user_id``/``user_pwd`` (env var or, during
the migration, query param) — so this is fully backward-compatible.

A standard ASGI middleware (not ``BaseHTTPMiddleware``) is used so the contextvar
set here propagates into the endpoint coroutine — mirroring MCPTokenMiddleware
in pyegeria_handler.py.
"""
import base64
import json
import os
import time
from contextlib import contextmanager
from contextvars import ContextVar

from pyegeria import lineage_visible  # pyegeria >= 6.1.25
from typing import Optional
import logging

logger = logging.getLogger("pyegeria_web.egeria_auth")

_egeria_token: ContextVar[Optional[str]] = ContextVar("egeria_token", default=None)

# Set from the X-Egeria-For-Lineage request header (the portal's "Promise / Memento"
# toggle). When true the middleware runs the request inside pyegeria's
# lineage_visible() block (contextvar-based, so concurrent requests don't leak), which
# sends forLineage=true on every request body; elements classified Promise/Memento --
# hidden by default -- are then returned. Pages where that isn't meaningful
# (operations, audit) simply never send the header. This var only mirrors the flag
# so lineage_key() can keep cached element data apart.
_for_lineage: ContextVar[bool] = ContextVar("egeria_for_lineage", default=False)


def for_lineage_requested() -> bool:
    return _for_lineage.get()


def lineage_key() -> str:
    """Cache-key suffix. Anything that caches element data across requests must
    include this: the same URL returns different elements with forLineage on."""
    return "|fl" if _for_lineage.get() else ""


@contextmanager
def lineage_scope(on: bool):
    """Run a block as if it were a request with X-Egeria-For-Lineage set to `on`: the mirror flag that
    lineage_key() reads AND pyegeria's lineage_visible(), exactly what EgeriaTokenMiddleware does per
    request. For background work with no request (cache warm-ups). Always restored, even on error."""
    reset = _for_lineage.set(bool(on))
    try:
        with lineage_visible(bool(on)):
            yield
    finally:
        _for_lineage.reset(reset)


def get_request_token() -> Optional[str]:
    """Return the X-Egeria-Token supplied with the current request, if any."""
    return _egeria_token.get()


def token_user() -> Optional[str]:
    """The user id in the current request's Egeria bearer token, or None.

    Egeria tokens are JWTs whose ``sub`` is the user id. The payload is read
    without verifying the signature: Egeria verifies the token on every call, and
    this is only for labelling things as the caller's own (my like, my rating)."""
    return _token_sub(_egeria_token.get())


def _token_sub(token: Optional[str]) -> Optional[str]:
    parts = token.split(".") if token else []
    if len(parts) != 3:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
    except (ValueError, TypeError):
        return None
    sub = payload.get("sub") if isinstance(payload, dict) else None
    return sub if isinstance(sub, str) and sub else None


def use_token(client, token: str) -> None:
    """Make a pyegeria client act only as the user the bearer token belongs to.

    pyegeria answers a 401 (usually an expired token) by logging in again with
    the client's own user_id/user_pwd and retrying. The portal builds its
    clients with the service credentials (EGERIA_USER, erinoverview), so when a
    signed-in user's token expired, that retry silently ran the request as the
    service user: Peter's lineage query failed with "erinoverview is not
    authorized". The client keeps no password, so there is no retry; the 401
    reaches the browser, which mints a new token for its own user."""
    client.set_bearer_token(token)
    client.user_id = _token_sub(token) or client.user_id
    client.user_pwd = None


# The words a caller sees when their sign-in cannot be used. Same text the report-spec
# execute route has always returned with HTTP 401.
TOKEN_REFUSED_WORDS = ("Not authorized for this operation — the current user does not have "
                       "permission for this report")


def _token_expired(token: Optional[str]) -> bool:
    """True when the token's ``exp`` claim is in the past. Read without verifying the signature
    (Egeria verifies it on every call); a token with no readable ``exp`` is not called expired."""
    parts = token.split(".") if token else []
    if len(parts) != 3:
        return False
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
    except (ValueError, TypeError):
        return False
    exp = payload.get("exp") if isinstance(payload, dict) else None
    return isinstance(exp, (int, float)) and exp <= time.time()


class PortalSupply:
    """The Portal's pyegeria ``RoleSupply`` (RS-W2-3): what a report-spec routine's declared
    inputs are filled from. Built per request (``PortalSupply(request)``).

    - ``client(cls)``: a client of that class acting as the signed-in user. With a request token
      it goes through :func:`use_token`, so the client holds no password and a 401 can never
      re-authenticate as the service user. A token whose ``exp`` has passed is refused here,
      before any Egeria call, with ``CallerTokenExpired``. With no token at all the client signs
      in with the service credentials, exactly as ``exec_report_spec`` did before.
    - forLineage: ``EgeriaTokenMiddleware`` already wraps the whole request in
      ``lineage_visible(...)`` and pyegeria reads that default per request, so every client handed
      out sees the request's Promise/Memento toggle with no wrapping here.
    - ``viewer()``: read from the ``report_viewer`` contextvar that ``execute_spec`` sets (no
      second copy). No chosen persona refuses, saying why.
    """

    def __init__(self, request=None, *, view_server: Optional[str] = None, view_url: Optional[str] = None,
                 user_id: Optional[str] = None, user_pwd: Optional[str] = None):
        self.request = request
        self._server = view_server
        self._url = view_url
        self._user = user_id
        self._pwd = user_pwd
        self._clients: dict = {}

    def client(self, cls):
        from pyegeria.view.role_supply import CallerTokenExpired
        token = _egeria_token.get()
        if token and _token_expired(token):
            raise CallerTokenExpired(TOKEN_REFUSED_WORDS, role=f"egeria_client:{getattr(cls, '__name__', cls)}")
        if cls not in self._clients:
            c = cls(self._server or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
                    self._url or os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
                    user_id=self._user or os.environ.get("EGERIA_USER", "erinoverview"),
                    user_pwd=self._pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret"))
            if token:
                use_token(c, token)
            else:
                c.create_egeria_bearer_token()
            self._clients[cls] = c
        return self._clients[cls]

    def viewer(self):
        from pyegeria.view.role_supply import RoleRefused, Viewer
        from report_viewer import current_viewer
        v = current_viewer()
        if not v or not v.get("persona_id"):
            why = (v or {}).get("reason") or "the viewer is not known"
            raise RoleRefused(f"No persona was chosen ({why})", role="viewer")
        persona = v.get("persona") or {}
        return Viewer(user_id=v["persona_id"], is_admin=None, display_name=persona.get("display_name"))

    def reader(self, source: str):
        from pyegeria.view.role_supply import NoSuchReader
        raise NoSuchReader(f"The Portal has no reader named '{source}'", role=f"reader:{source}")

    def subject(self):
        return None

    def refusal_words(self, kind: str) -> str:
        if kind == "egeria_client":
            return TOKEN_REFUSED_WORDS
        return f"The Portal does not supply '{kind}' to report specs."


def apply_token(client) -> None:
    """Apply the per-request bearer token to a freshly-built pyegeria client, or
    obtain a fresh token from the client's configured credentials when none was
    supplied. Drop-in replacement for ``client.create_egeria_bearer_token()``."""
    token = _egeria_token.get()
    if token:
        use_token(client, token)
    else:
        client.create_egeria_bearer_token()


async def async_apply_token(client) -> None:
    """Async counterpart of :func:`apply_token` for use inside async FastAPI routes.

    Calls the async token-creation method directly so that async routes don't
    need to run a sub-loop (which would raise RuntimeError on Python 3.10+)."""
    token = _egeria_token.get()
    if token:
        use_token(client, token)
    else:
        await client._async_create_egeria_bearer_token()


class EgeriaTokenMiddleware:
    """Stash the X-Egeria-Token request header into a contextvar for the
    duration of the request so token-capable handlers can pick it up."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        token = None
        for_lineage = False
        for name, value in scope.get("headers") or ():
            if name == b"x-egeria-token":
                token = value.decode("latin-1").strip() or None
            elif name == b"x-egeria-for-lineage":
                for_lineage = value.decode("latin-1").strip().lower() == "true"
        reset = _egeria_token.set(token)
        reset_fl = _for_lineage.set(for_lineage)
        try:
            with lineage_visible(for_lineage):
                await self.app(scope, receive, send)
        finally:
            _for_lineage.reset(reset_fl)
            _egeria_token.reset(reset)
