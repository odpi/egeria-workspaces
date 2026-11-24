"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-78: default-deny login gate for the freshstart Portal (SERVER_MANAGED_AUTH).

Twin: compose-configs/egeria-quickstart/PyegeriaWebHandler/demo_auth_gate.py (DemoAuthGateMiddleware,
DEMO_MODE only). Same shape: a short public list, 401 JSON on API paths, 302 to /login for pages. Kept as a
freshstart copy rather than shared code because the two differ on purpose in two places (below), and the
trees are dual copies with no shared module today (BACKLOG SHARE-1/SHARE-2).

Why: most read routes build their Egeria client with egeria_auth.apply_token, which, when the caller sends
no X-Egeria-Token, signs in as the Portal's service user (EGERIA_USER + service_password()). With no gate,
an anonymous caller (no cookie, or a bogus one) read the catalog, operations, audit, ... as the service user
(kind cluster proof, 2026-11-22). SERVER_MANAGED_AUTH changed who Dr.Egeria / feedback / admin act as; it
never refused a tokenless read. This middleware does, in one place.

When it acts: on every HTTP request while demo_config.SERVER_MANAGED_AUTH is true (read per request, so the
flag is the one switch; its default is true, so the gate is on unless SERVER_MANAGED_AUTH is set to a
false value, which is the ungated local posture).

"Signed in" is the rule freshstart already uses for /portal, /admin, /profile and PO-68's no-password
/api/egeria-token: demo_auth_handler.get_current_user, i.e. a demo_token JWT (cookie, or Authorization:
Bearer) signed with JWT_SECRET and not expired. Fails closed when no usable signing key is set (PO-46b /
RK-24b: then no session can be trusted). An X-Egeria-Token header alone is NOT a Portal session (as on
quickstart): it is what apply_token reuses after sign-in, not proof of one.

The two deliberate differences from the quickstart twin:
  1. No edge-header exemption. Quickstart lets requests without X-Egeria-Edge through, as in-network
     callers. Freshstart's Apache (compose fastapi-ssl.conf and the chart's freshstart vhost) never sets
     that header, so the exemption would exempt everything; and freshstart's :8000 is published on
     EGERIA_BIND_IP (multi-host may be 0.0.0.0) and reachable as a Service in a cluster. So every request is
     held to the rule, whatever headers it carries.
  2. The signed-in check is the JWT alone: freshstart accounts live in Egeria, not quickstart's SQLite
     demo DB, so there is no verified-user row to look up.
"""

from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request

import demo_config

# Reachable without signing in. Everything else needs a session. Each entry is needed by the sign-in itself,
# by a probe, or has its own gate:
PUBLIC_PATHS = {
    "/",                        # health: the k8s liveness/readiness/startup probes (deployment-portal.yaml)
    "/login",                   # the sign-in page
    "/register",                # freshstart only redirects it to /login (no self-registration)
    "/privacy",                 # static privacy notice, linked from the sign-in page
    "/favicon.ico",
    "/api/platform/org-name",   # the sign-in page's heading (organisation name only)
    "/api/egeria-token",        # credential exchange: a sent password is checked by Egeria; with no password
                                # the route itself needs a signed-in session (PO-68). The helm canary signs in
                                # here through the front door with the canary account's password.
}
PUBLIC_PREFIXES = (
    "/static/",                 # the sign-in page's logo and shared assets
    "/api/auth/",               # login, change-password (first-login forced change: checks the old password
                                # with Egeria), logout, me (answers authenticated:false without a session)
)
# The MCP transport: MCPTokenMiddleware gates it with the MCP access token, and its callers (the Obsidian
# Dr.Egeria plugin) are machine clients with no Portal session. Freshstart's Apache does not proxy it.
_MCP_SUFFIXES = ("/sse", "/messages")

# Paths that answer 401 JSON when unauthenticated; anything else is a page and is redirected to /login.
_API_PREFIXES = ("/api/", "/dr-egeria/", "/openapi.json", "/docs", "/redoc")


def _is_public(path: str) -> bool:
    if path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
        return True
    return path.endswith(_MCP_SUFFIXES) or "/sse/" in path or "/messages/" in path


def _signed_in(scope) -> bool:
    from demo_auth_handler import get_current_user
    try:
        return get_current_user(Request(scope)) is not None
    except HTTPException:       # PO-46b: no usable signing key, so no session can be trusted (fails closed)
        return False


class ServerAuthGateMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if (scope["type"] != "http" or not demo_config.SERVER_MANAGED_AUTH
                or scope["method"] == "OPTIONS" or _is_public(scope["path"]) or _signed_in(scope)):
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        response: Optional[object]
        if path.startswith(_API_PREFIXES):
            response = JSONResponse(status_code=401, content={"detail": "Authentication required"})
        else:
            response = RedirectResponse(url="/login", status_code=302)
            # A stale or forged cookie is no session: clear it so the sign-in page starts clean.
            response.delete_cookie("demo_token")
        await response(scope, receive, send)
