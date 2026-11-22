"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Whose report specs a request reads: the signed-in user's, never the Portal's service user's.

pyegeria keys the EGERIA tier and every fetched spec by a **credential identity** ("<user>@<host_port>/<view
server>"). A read made outside any `spec_identity` uses the process's own identity, which in the Portal is the
service user (EGERIA_USER, erinoverview), who is also the Erin persona. So a signed-in user's identity-less
read would come back as Erin's specs, and their own private specs would be hidden from them.

- **Multi-user** (`declare_multi_user`, at startup): the Portal tells pyegeria it serves many users. Once
  declared, an identity-less read resolves to no identity, so no private specs, instead of the service user
  (pyegeria R-A: `declare_multi_user()` / PYEGERIA_MULTI_USER=1). A pyegeria without the function still gets
  the environment flag, and is otherwise unchanged.
- **Per request** (`request_spec_identity`, entered by EgeriaTokenMiddleware): a request with an
  X-Egeria-Token runs as that token's user, on the platform the token may be used on. This is the identity
  `report_spec_restricted._user_client(token)` fetches with, so a user reads back what they fetched. Threads
  the Portal starts with `contextvars.copy_context()` carry it.
- **Process-wide decisions** (`anonymous_spec_identity`): reads whose answer is shared by every caller (the
  public route's shared-tier check, local fallback registration) are made as no one, never as whoever's
  request happened to trigger them.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Optional

from loguru import logger

MULTI_USER_ENV = "PYEGERIA_MULTI_USER"
_FALSE = ("0", "false", "no", "off")


def declare_multi_user() -> str:
    """Tell pyegeria this process serves many users. Returns what was done, for the startup log:
    "declared", "flag only" (a pyegeria without declare_multi_user), or "off" (PYEGERIA_MULTI_USER=0 set
    explicitly by the operator, which is respected and logged)."""
    if (os.environ.get(MULTI_USER_ENV) or "").strip().lower() in _FALSE:
        logger.warning(f"{MULTI_USER_ENV} is set off: identity-less report-spec reads run as the Portal's "
                       f"service user")
        return "off"
    os.environ[MULTI_USER_ENV] = "1"
    fn = None
    for mod in ("pyegeria.view.egeria_spec_cache", "pyegeria"):
        try:
            module = __import__(mod, fromlist=["declare_multi_user"])
        except ImportError:
            continue
        fn = getattr(module, "declare_multi_user", None)
        if callable(fn):
            break
        fn = None
    if fn is None:
        logger.info(f"report specs: {MULTI_USER_ENV}=1 set (this pyegeria has no declare_multi_user)")
        return "flag only"
    fn()
    logger.info("report specs: declared multi-user to pyegeria (identity-less reads see no private specs)")
    return "declared"


def token_spec_identity(token: Optional[str]) -> Optional[str]:
    """The credential identity of the token's user on the platform the token may be used on, or None (no
    token, no user in it, a refused platform, or a pyegeria without credential identities)."""
    if not token:
        return None
    from egeria_auth import _token_sub, default_platform_url, resolve_platform, token_platform
    user = _token_sub(token)
    if not user:
        return None
    credential_identity = spec_cache_attr("credential_identity")
    if credential_identity is None:
        return None
    try:
        url = resolve_platform(token_platform(token) or default_platform_url(), token=token)
    except Exception:  # noqa: BLE001 -- a refused platform: the request gets no identity, so public specs only
        return None
    return credential_identity(user, url, os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"))


def spec_cache_attr(name: str):
    """pyegeria's egeria_spec_cache.<name>, or None on a pyegeria without it. Feature detection for names only
    a newer pyegeria has (credential identities arrived with the spec-cache identity change): looked up on the
    module rather than imported, so an older pyegeria keeps working and nothing calls a name it lacks."""
    try:
        import pyegeria.view.egeria_spec_cache as esc
    except ImportError:
        return None
    return getattr(esc, name, None)


def _spec_identity():
    return spec_cache_attr("spec_identity")


@contextmanager
def request_spec_identity(token: Optional[str]):
    """Run the block as the token's user for report-spec reads (as no one without a token)."""
    spec_identity = _spec_identity()
    if spec_identity is None:
        yield None
        return
    identity = token_spec_identity(token)
    with spec_identity(identity):
        yield identity


@contextmanager
def anonymous_spec_identity():
    """Run the block as no one: for a read whose answer every caller shares."""
    spec_identity = _spec_identity()
    if spec_identity is None:
        yield
        return
    with spec_identity(None):
        yield
