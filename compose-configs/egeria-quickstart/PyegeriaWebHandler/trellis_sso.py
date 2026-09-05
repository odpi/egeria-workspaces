"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared SSO handoff token minting for the "trellis" family of external apps
(Egeria Advisor, Resource Explorer) — one function so the claim shape only
exists in one place, used by both advisor_lock_handler.py and
resource_explorer_handler.py.

Contract (2026-09-05, per the trellis side): the minted HS256 JWT carries
{"sub", "role", "display_name", "egeria_token", "iat", "exp"}, signed with
EGERIA_ADVISOR_SSO_SECRET (shared with Advisor's ADVISOR_PORTAL_SECRET /
Resource Explorer's TRELLIS_PORTAL_SECRET — same value, different env-var
name on each side, confirmed against compose-configs/optional-associated-
runtimes/trellis/docker-compose.yaml). This replaced an earlier
{"egeria_user","egeria_password","iat","exp"} shape that Advisor's own auth
now rejects with a 400 once it went multi-user.

egeria_token is a REAL short-lived Egeria bearer token minted server-side
for the chosen persona, not the raw persona password — Advisor/Resource
Explorer never see a credential. This mirrors rest_api_handler.py's
_async_bearer_token_for_spec_fetch, but deliberately does NOT reuse that
function outright: that helper first tries get_request_token() (whatever
token the CALLER's own request already carries, e.g. an admin browsing the
portal), which is wrong here — the handoff must always mint a token for the
PERSONA the user selected, not whichever token happens to be in the current
request's context.
"""

import time
from typing import Optional

from jose import jwt
from loguru import logger

from demo_config import EGERIA_ADVISOR_SSO_SECRET

_PLATFORM_URL = None  # lazily read from rest_api_handler's _env_defaults()


def _platform_defaults() -> dict:
    # Reuse the one place platform_url/server env defaults are already
    # defined, rather than duplicating EGERIA_PLATFORM_URL/EGERIA_VIEW_SERVER
    # parsing here.
    from rest_api_handler import _env_defaults
    return _env_defaults()


async def _acquire_egeria_bearer_for_handoff(user_id: str, user_pwd: str) -> Optional[str]:
    """Mint a fresh Egeria bearer token for the given persona's credentials.

    Always mints fresh (unlike _async_bearer_token_for_spec_fetch) — the
    handoff needs a token scoped to the PERSONA being handed off, never the
    calling request's own already-forwarded token.
    """
    defaults = _platform_defaults()
    try:
        from pyegeria import ValidMetadataManager
        vmm = ValidMetadataManager(
            view_server=defaults["server"], platform_url=defaults["url"],
            user_id=user_id, user_pwd=user_pwd,
        )
        token = await vmm._async_create_egeria_bearer_token()
        vmm.close_session()
        return token
    except Exception as exc:
        logger.warning(f"trellis SSO: could not mint Egeria bearer token for {user_id!r}: {exc}")
        return None


async def make_portal_sso_token(user, persona_id: str, persona: dict) -> str:
    """Mint the shared trellis SSO handoff JWT.

    `user` is the Portal's own User DB model instance (or None outside
    DEMO_MODE / local mode) — supplies `sub`/`role`. `persona_id` is the
    personas.json key (also the Egeria user_id); `persona` is that entry's
    dict (supplies `display_name` and the password used only to mint the
    bearer token below, never placed in the JWT itself).

    Raises RuntimeError if no bearer token could be minted — better to fail
    loudly here than hand the caller a token Advisor/Resource Explorer will
    just reject with a 400 anyway.
    """
    egeria_token = await _acquire_egeria_bearer_for_handoff(persona_id, persona["password"])
    if not egeria_token:
        raise RuntimeError(f"Could not obtain an Egeria bearer token for persona {persona_id!r}")

    now = int(time.time())
    payload = {
        "sub":          user.id if user else persona_id,
        "role":         getattr(user, "role", "guest") if user else "guest",
        "display_name": persona.get("display_name", persona_id),
        "egeria_token": egeria_token,
        "iat":          now,
        "exp":          now + 120,  # short-lived -- immediately exchanged client-side
    }
    return jwt.encode(payload, EGERIA_ADVISOR_SSO_SECRET, algorithm="HS256")
