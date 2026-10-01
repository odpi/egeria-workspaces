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
from contextvars import ContextVar
from typing import Optional
import logging

logger = logging.getLogger("pyegeria_web.egeria_auth")

_egeria_token: ContextVar[Optional[str]] = ContextVar("egeria_token", default=None)

# Set from the X-Egeria-For-Lineage request header (the portal's "Promise / Memento"
# toggle). When true, every request body a pyegeria client sends in this request
# carries forLineage=true, so elements classified Promise/Memento -- hidden by
# default -- are returned. Pages where that isn't meaningful (operations, audit)
# simply never send the header.
_for_lineage: ContextVar[bool] = ContextVar("egeria_for_lineage", default=False)


def for_lineage_requested() -> bool:
    return _for_lineage.get()


def lineage_key() -> str:
    """Cache-key suffix. Anything that caches element data across requests must
    include this: the same URL returns different elements with forLineage on."""
    return "|fl" if _for_lineage.get() else ""


def _inject_for_lineage(client) -> None:
    """Wrap this client's request method so JSON bodies carry forLineage=true.

    Per-instance (clients are built fresh per request). A stand-in for pyegeria's
    upcoming lineage_visible() context manager -- swap for it once released.
    Bodiless requests are left alone.
    """
    orig = client._async_make_request

    async def _wrapped(request_type, endpoint, payload=None, *args, **kwargs):
        if isinstance(payload, dict):
            payload = {**payload, "forLineage": True}
        elif isinstance(payload, str) and payload.lstrip().startswith("{"):
            import json
            try:
                payload = json.dumps({**json.loads(payload), "forLineage": True})
            except ValueError:
                pass
        return await orig(request_type, endpoint, payload, *args, **kwargs)

    client._async_make_request = _wrapped


def get_request_token() -> Optional[str]:
    """Return the X-Egeria-Token supplied with the current request, if any."""
    return _egeria_token.get()


def apply_token(client) -> None:
    """Apply the per-request bearer token to a freshly-built pyegeria client, or
    obtain a fresh token from the client's configured credentials when none was
    supplied. Drop-in replacement for ``client.create_egeria_bearer_token()``."""
    token = _egeria_token.get()
    if token:
        client.set_bearer_token(token)
    else:
        client.create_egeria_bearer_token()
    if _for_lineage.get():
        _inject_for_lineage(client)


async def async_apply_token(client) -> None:
    """Async counterpart of :func:`apply_token` for use inside async FastAPI routes.

    Calls the async token-creation method directly so that async routes don't
    need to run a sub-loop (which would raise RuntimeError on Python 3.10+)."""
    token = _egeria_token.get()
    if token:
        client.set_bearer_token(token)
    else:
        await client._async_create_egeria_bearer_token()
    if _for_lineage.get():
        _inject_for_lineage(client)


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
            await self.app(scope, receive, send)
        finally:
            _for_lineage.reset(reset_fl)
            _egeria_token.reset(reset)
