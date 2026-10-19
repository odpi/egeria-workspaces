"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Default-deny login gate for the public demo (DEMO_MODE only).

Most routes in this app have no auth check of their own and fall back to a
shared default Egeria user when the caller sends no credentials, so on the
public demo everything — catalog reads, Dr.Egeria writes, server logs,
/api/egeria-token — was open to anonymous callers (audit, 2026-10-17). This
middleware closes that in one place: a request that came in through Apache
must carry a valid session (demo_token JWT of an existing, verified user)
unless its path is on the short public list below.

"Came in through Apache" = carries EDGE_HEADER, which proxy-locations.conf sets
on both the HTTPS and HTTP vhosts with `RequestHeader set` (so a client can't
remove it). Requests without it come straight from containers on
egeria_network (e.g. the Obsidian Dr.Egeria plugin calling
http://pyegeria-web:8000/sse) or from the host's loopback 8800 port, and keep
working as before. Keep pyegeria-web's host port bound to 127.0.0.1, or
that becomes a way around the gate.

Pure ASGI rather than BaseHTTPMiddleware so SSE responses stream untouched
(same reason as MCPTokenMiddleware).
"""

import time
from typing import Optional

from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError
from starlette.concurrency import run_in_threadpool

EDGE_HEADER = b"x-egeria-edge"

# Reachable without logging in. Everything else needs a session.
PUBLIC_PATHS = {
    "/", "/login", "/register", "/privacy", "/reset-password", "/favicon.ico",
    "/api/demo/personas",              # persona list, passwords stripped
    "/api/demo-feedback",              # anonymous submit (POST); GET is admin-gated in the route
    "/api/platform/portal-config",
    "/api/bootstrap/status",
    "/api/jupyter/status", "/api/jupyter/reservations",
    "/api/obsidian/status", "/api/obsidian/reservations",
    "/api/advisor/status", "/api/resource-explorer/status",
}
PUBLIC_PREFIXES = ("/static/", "/api/auth/")   # login, register, verify, password reset, me

# Paths that answer 401 JSON when unauthenticated; anything else is a page and
# is redirected to /login.
_API_PREFIXES = ("/api/", "/dr-egeria/", "/sse", "/messages", "/openapi.json", "/docs", "/redoc")

# user id -> (is_valid, checked_at). The DB lookup is what makes a disabled
# account (verified=False) lose access before its JWT expires; caching it
# briefly keeps that to one query per user per minute instead of per request.
_USER_CACHE: dict = {}
_USER_CACHE_TTL = 60


def _is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES)


def _token(headers: dict) -> Optional[str]:
    auth = headers.get(b"authorization", b"").decode("latin-1")
    if auth.startswith("Bearer "):
        return auth[7:] or None
    for part in headers.get(b"cookie", b"").decode("latin-1").split(";"):
        name, _, value = part.strip().partition("=")
        if name == "demo_token" and value:
            return value
    return None


def _user_is_valid(user_id: str) -> bool:
    from sqlalchemy.orm import Session
    from demo_db import User, get_engine
    with Session(get_engine()) as session:
        user = session.get(User, user_id)
        return bool(user and user.verified)


async def _authenticated(headers: dict) -> bool:
    from demo_auth_handler import _decode_jwt
    token = _token(headers)
    if not token:
        return False
    try:
        user_id = _decode_jwt(token)["sub"]
    except (JWTError, KeyError):
        return False
    hit = _USER_CACHE.get(user_id)
    if hit and time.monotonic() - hit[1] < _USER_CACHE_TTL:
        return hit[0]
    ok = await run_in_threadpool(_user_is_valid, user_id)
    _USER_CACHE[user_id] = (ok, time.monotonic())
    return ok


class DemoAuthGateMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope["headers"])
        path = scope["path"]
        if (EDGE_HEADER not in headers or scope["method"] == "OPTIONS"
                or _is_public(path) or await _authenticated(headers)):
            await self.app(scope, receive, send)
            return

        if path.startswith(_API_PREFIXES):
            response = JSONResponse(status_code=401, content={"detail": "Authentication required"})
        else:
            response = RedirectResponse(url="/login", status_code=302)
            # A disabled account still holds a well-formed cookie, and /login
            # bounces anyone /api/auth/me calls authenticated back to /portal —
            # clear it so that can't loop.
            response.delete_cookie("demo_token")
        await response(scope, receive, send)
