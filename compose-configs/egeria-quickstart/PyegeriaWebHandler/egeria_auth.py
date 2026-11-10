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

from fastapi import HTTPException
from pydantic import BaseModel, model_validator
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
            check_client_platform(c)
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


# ── Platform allowlist (BRIEF-PORTAL-PLATFORM-URL-ALLOWLIST-2026-11-10) ─────────────────────────────
# The rule: the Portal's service credentials only ever go to an allow-listed platform, and a token only
# ever goes to the platform it was minted for. A user's OWN password may go to a platform the user chose
# (the Explorer Connection form) when PORTAL_ALLOW_CUSTOM_PLATFORMS is on (default: on, off in DEMO_MODE).
#
# Enforced in three places, all through resolve_platform():
#   - EgeriaTokenMiddleware, for every request carrying a `url` query param (a query string never carries
#     a password, so such a url must be allow-listed or match the presented token's platform);
#   - PlatformBody, for request bodies with a `url` field, as the body is parsed (before any client is built:
#     a pyegeria client's constructor already calls platform_url);
#   - apply_token / async_apply_token / PortalSupply.client / check_client_platform, before any client
#     signs in or attaches a token (the backstop for every other path);
#   - POST /api/egeria-token, before minting.

_DEFAULT_PLATFORM_URL = "https://localhost:9443"     # the factories' own fallback when the env is unset
_PLATFORM_ENV_VARS = ("EGERIA_PLATFORM_URL", "EGERIA_VIEW_SERVER_URL", "EGERIA_INTEGRATION_DAEMON_URL",
                      "EGERIA_ENGINE_HOST_URL", "EGERIA_METADATA_STORE_URL")
_DEFAULT_PORTS = {"http": 80, "https": 443}


class PlatformRefused(HTTPException):
    """A platform URL this Portal will not send credentials to. An HTTPException, so routes that re-raise
    HTTPException answer with its status: 400 for the URL itself, 401 for a token presented for another
    platform. Raised before any outbound call is made."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


def normalize_platform_url(url: Optional[str]) -> Optional[str]:
    """``scheme://host:port``, lower-case, default port filled in; None when unparsable.
    ``https://Host:443/`` and ``https://host`` normalize to the same string."""
    from urllib.parse import urlsplit
    if not url or not isinstance(url, str):
        return None
    try:
        parts = urlsplit(url.strip())
        scheme = (parts.scheme or "").lower()
        host = (parts.hostname or "").lower()
        port = parts.port
    except ValueError:
        return None
    if scheme not in _DEFAULT_PORTS or not host:
        return None
    if parts.username is not None or parts.password is not None:
        return None          # userinfo in a platform URL is never legitimate
    port = port or _DEFAULT_PORTS[scheme]
    if ":" in host:          # IPv6 literal
        host = f"[{host}]"
    return f"{scheme}://{host}:{port}"


def default_platform_url() -> str:
    return os.environ.get("EGERIA_PLATFORM_URL") or _DEFAULT_PLATFORM_URL


def allowed_platform_urls() -> set:
    """Normalized platform URLs the Portal's own credentials may go to: the configured platform URLs plus
    the comma-separated PORTAL_ALLOWED_PLATFORM_URLS. Read from the environment on every call."""
    raw = [os.environ.get(v) for v in _PLATFORM_ENV_VARS]
    if not os.environ.get("EGERIA_PLATFORM_URL"):
        raw.append(_DEFAULT_PLATFORM_URL)
    raw += (os.environ.get("PORTAL_ALLOWED_PLATFORM_URLS") or "").split(",")
    return {n for n in (normalize_platform_url(u) for u in raw) if n}


def _env_flag(name: str) -> Optional[bool]:
    v = os.environ.get(name)
    if v is None or not v.strip():
        return None
    return v.strip().lower() in ("true", "1", "yes", "on")


def custom_platforms_allowed() -> bool:
    """May a user's own password go to a platform that is not allow-listed? PORTAL_ALLOW_CUSTOM_PLATFORMS
    when set; otherwise on, except in DEMO_MODE."""
    flag = _env_flag("PORTAL_ALLOW_CUSTOM_PLATFORMS")
    if flag is not None:
        return flag
    return not bool(_env_flag("DEMO_MODE"))


def service_password() -> str:
    return os.environ.get("EGERIA_USER_PASSWORD", "secret")


def is_caller_password(pwd: Optional[str]) -> bool:
    """True when `pwd` is a password the caller supplied, not the Portal's own. The Portal holds exactly one
    password (EGERIA_USER_PASSWORD); any client carrying it is carrying the service credential, whoever
    typed it, so it is treated as the service password."""
    return bool(pwd) and pwd != service_password()


# sha256(token) -> (normalized platform URL, expires_at). Filled by POST /api/egeria-token; process memory.
_TOKEN_PLATFORMS: dict = {}
_TOKEN_BIND_DEFAULT_TTL = 3600.0


def _token_hash(token: str) -> str:
    import hashlib
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _token_exp(token: Optional[str]) -> Optional[float]:
    parts = token.split(".") if token else []
    if len(parts) != 3:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
    except (ValueError, TypeError):
        return None
    exp = payload.get("exp") if isinstance(payload, dict) else None
    return float(exp) if isinstance(exp, (int, float)) else None


def bind_token_platform(token: str, url: str) -> None:
    """Record that `token` was minted here for platform `url`, for the token's lifetime."""
    norm = normalize_platform_url(url)
    if not token or not norm:
        return
    now = time.time()
    for k in [k for k, (_, exp) in _TOKEN_PLATFORMS.items() if exp <= now]:
        _TOKEN_PLATFORMS.pop(k, None)
    exp = _token_exp(token)
    _TOKEN_PLATFORMS[_token_hash(token)] = (norm, exp if exp and exp > now else now + _TOKEN_BIND_DEFAULT_TTL)


def token_platform(token: Optional[str]) -> Optional[str]:
    """The normalized platform a token was minted for here, or None if this Portal never minted it."""
    if not token:
        return None
    hit = _TOKEN_PLATFORMS.get(_token_hash(token))
    if not hit:
        return None
    norm, exp = hit
    if exp <= time.time():
        _TOKEN_PLATFORMS.pop(_token_hash(token), None)
        return None
    return norm


def _refuse_internal_address(norm: str) -> None:
    """SSRF guard for caller-chosen (not allow-listed) platforms: refuse hosts that resolve to private,
    loopback, link-local, reserved, multicast or unspecified addresses (the check rest_api_handler's
    _validate_platform_url makes). An internal platform the owner wants reachable goes in
    PORTAL_ALLOWED_PLATFORM_URLS instead."""
    import ipaddress
    import socket
    from urllib.parse import urlsplit
    host = urlsplit(norm).hostname or ""
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError):
        raise PlatformRefused(400, f"Could not resolve platform host: {host}")
    for *_, sockaddr in infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified):
            raise PlatformRefused(400, f"Refusing to connect to a private/internal address: {host}. "
                                       "Add it to PORTAL_ALLOWED_PLATFORM_URLS if it is one of yours.")


SERVICE_ACCOUNT_REFUSAL = "This Portal does not sign in to other platforms with its own account"
# What the caller can do about a refusal. A saved Connection-form URL that is not allow-listed hits the
# 400s below on every call; a token bound to a custom platform is forgotten when the Portal restarts
# (_TOKEN_PLATFORMS is process memory), which surfaces as the 401s.
_RECONNECT_OR_CLEAR = ("Reconnect with your own user and password, or clear the platform URL in the "
                       "connection settings to use this Portal's own platform.")
_CLEAR_ONLY = "Clear the platform URL in the connection settings to use this Portal's own platform."
_CONNECT_AGAIN = ("Connect again: sign-ins to another platform are not kept when the Portal restarts. "
                  "Or clear the platform URL in the connection settings to use this Portal's own platform.")


def resolve_platform(url: Optional[str], *, has_caller_password: bool = False,
                     token: Optional[str] = None) -> str:
    """The one gate. Returns the platform URL to use, or raises PlatformRefused.

    - url empty -> the configured default;
    - a token minted here for another platform -> 401, whatever `url` is;
    - url allow-listed -> allowed;
    - url not allow-listed:
        token minted here for that platform -> allowed;
        any other token -> 401 (a token only goes to the platform it was minted for);
        no caller password (the service password would be used) -> 400;
        caller password -> only with PORTAL_ALLOW_CUSTOM_PLATFORMS on, and not to an internal address.
    """
    if not url or not str(url).strip():
        return default_platform_url()
    norm = normalize_platform_url(url)
    if not norm:
        raise PlatformRefused(400, "Invalid platform URL.")
    bound = token_platform(token)
    if token and bound and bound != norm:
        raise PlatformRefused(401, f"This sign-in was issued for a different platform. {_CONNECT_AGAIN if custom_platforms_allowed() else _CLEAR_ONLY}")
    if norm in allowed_platform_urls():
        return url
    if token:
        if bound == norm:
            return url
        raise PlatformRefused(401, f"This sign-in was not issued for that platform ({norm}). {_CONNECT_AGAIN if custom_platforms_allowed() else _CLEAR_ONLY}")
    if not has_caller_password:
        # With custom platforms off (DEMO_MODE) reconnecting with your own password would only hit the
        # "only connects to its own platform" refusal, so then the one way out is to clear the URL.
        advice = _RECONNECT_OR_CLEAR if custom_platforms_allowed() else _CLEAR_ONLY
        raise PlatformRefused(400, f"{SERVICE_ACCOUNT_REFUSAL} ({norm}). {advice}")
    if not custom_platforms_allowed():
        raise PlatformRefused(400, f"This Portal only connects to its own platform, not {norm}. "
                                   "Clear the platform URL in the connection settings.")
    _refuse_internal_address(norm)
    return url


def check_client_platform(client, token: Optional[str] = None) -> None:
    """Gate a freshly-built pyegeria client before it signs in or attaches the request token: raises
    PlatformRefused when its platform_url may not receive them."""
    token = token or _egeria_token.get()
    resolve_platform(getattr(client, "platform_url", None),
                     has_caller_password=is_caller_password(getattr(client, "user_pwd", None)),
                     token=token)


def apply_token(client) -> None:
    """Apply the per-request bearer token to a freshly-built pyegeria client, or
    obtain a fresh token from the client's configured credentials when none was
    supplied. Drop-in replacement for ``client.create_egeria_bearer_token()``.
    Refuses (PlatformRefused) a platform the credentials may not go to."""
    check_client_platform(client)
    token = _egeria_token.get()
    if token:
        use_token(client, token)
    else:
        client.create_egeria_bearer_token()


async def async_apply_token(client) -> None:
    """Async counterpart of :func:`apply_token` for use inside async FastAPI routes.

    Calls the async token-creation method directly so that async routes don't
    need to run a sub-loop (which would raise RuntimeError on Python 3.10+)."""
    check_client_platform(client)
    token = _egeria_token.get()
    if token:
        use_token(client, token)
    else:
        await client._async_create_egeria_bearer_token()


class PlatformBody(BaseModel):
    """Base for request bodies that carry a platform `url` (and optionally the caller's own `user_pwd`).
    The platform gate runs as the body is parsed -- before the route builds any pyegeria client, whose
    constructor already makes a request to platform_url -- and a refusal answers 400/401."""

    @model_validator(mode="after")
    def _gate_platform(self):
        resolve_platform(getattr(self, "url", None),
                         has_caller_password=is_caller_password(getattr(self, "user_pwd", None)),
                         token=_egeria_token.get())
        return self


_SAME_SITE_FETCH = ("same-origin", "none")


def _query_platform_refusal(query_string: bytes, token: Optional[str],
                            fetch_site: Optional[str]) -> Optional[PlatformRefused]:
    """The platform gate for a request's `url` query param(s), or None when there are none / all pass.

    A query string never carries a password (no route takes user_pwd from it), so a query `url` must be
    allow-listed or be the platform the presented token was minted for. Also refuses (403) a cross-site
    request with a `url` param and no X-Egeria-Token: browsers send Sec-Fetch-Site on every request, so a
    page on another site cannot drive the Portal with a simple GET."""
    from urllib.parse import parse_qsl
    if not query_string:
        return None
    # Parsed exactly as Starlette parses it (keys are percent-decoded too: `%75rl=` is `url`).
    urls = [v for k, v in parse_qsl(query_string.decode("latin-1"), keep_blank_values=True) if k == "url"]
    if not urls:
        return None
    if not token and fetch_site is not None and fetch_site not in _SAME_SITE_FETCH:
        return PlatformRefused(403, "Cross-site requests may not choose a platform.")
    try:
        for u in urls:
            resolve_platform(u, has_caller_password=False, token=token)
    except PlatformRefused as exc:
        return exc
    return None


async def _send_json(send, status: int, body: dict) -> None:
    payload = json.dumps(body).encode("utf-8")
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json"),
                            (b"content-length", str(len(payload)).encode("ascii"))]})
    await send({"type": "http.response.body", "body": payload})


class EgeriaTokenMiddleware:
    """Stash the X-Egeria-Token request header into a contextvar for the
    duration of the request so token-capable handlers can pick it up. Refuses,
    before the route runs, a request whose `url` query param names a platform
    the Portal may not send credentials to (see _query_platform_refusal)."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        token = None
        for_lineage = False
        fetch_site = None
        for name, value in scope.get("headers") or ():
            if name == b"x-egeria-token":
                token = value.decode("latin-1").strip() or None
            elif name == b"x-egeria-for-lineage":
                for_lineage = value.decode("latin-1").strip().lower() == "true"
            elif name == b"sec-fetch-site":
                fetch_site = value.decode("latin-1").strip().lower()
        refusal = _query_platform_refusal(scope.get("query_string") or b"", token, fetch_site)
        if refusal is not None:
            await _send_json(send, refusal.status_code, {"detail": refusal.detail})
            return
        reset = _egeria_token.set(token)
        reset_fl = _for_lineage.set(for_lineage)
        try:
            with lineage_visible(for_lineage):
                await self.app(scope, receive, send)
        finally:
            _for_lineage.reset(reset_fl)
            _egeria_token.reset(reset)
