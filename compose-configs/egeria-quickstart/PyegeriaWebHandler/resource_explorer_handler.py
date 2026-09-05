"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Explorer portal handoff — same "trellis" family app as Egeria
Advisor (see advisor_lock_handler.py), same SSO handoff mechanism via
trellis_sso.py, but deliberately NO exclusive lock: Resource Explorer is
multi-user with no single-shared-instance constraint, so there is nothing
to serialize access to. Just a reachability check plus a token mint.

Auth
----
In DEMO_MODE the handoff endpoint requires a verified JWT user, mirroring
advisor_lock_handler.py's _require_verified_or_local. Outside DEMO_MODE it
is open.
"""

import time

import httpx
from fastapi import APIRouter, HTTPException, Request
from loguru import logger
from pydantic import BaseModel

from demo_config import (
    DEMO_MODE,
    EGERIA_ADVISOR_SSO_SECRET,
    EGERIA_RESOURCE_EXPLORER_URL,
    resource_explorer_check_urls,
)
from trellis_sso import make_portal_sso_token

router = APIRouter(prefix="/api/resource-explorer", tags=["resource-explorer"])

_PERSONAS_FILE = None  # set lazily below to avoid importing Path twice


def _load_personas() -> dict:
    from pathlib import Path
    import json
    global _PERSONAS_FILE
    if _PERSONAS_FILE is None:
        _PERSONAS_FILE = Path(__file__).parent / "personas.json"
    try:
        return json.loads(_PERSONAS_FILE.read_text())
    except Exception:
        return {}


def _require_verified_or_local(request: Request):
    if not DEMO_MODE:
        return None
    from demo_auth_handler import require_verified_user
    from demo_db import get_db
    db = next(get_db())
    return require_verified_user(request, db)


# Same TTL-cached reachability pattern as advisor_lock_handler.py's
# _advisor_reachable — avoids hitting the remote host on every status poll.
_reachable_cache = {"ok": False, "checked_at": 0.0}
_REACHABLE_TTL_SECONDS = 15


async def _resource_explorer_reachable() -> bool:
    now = time.time()
    if now - _reachable_cache["checked_at"] < _REACHABLE_TTL_SECONDS:
        return _reachable_cache["ok"]
    ok = False
    for check_url in resource_explorer_check_urls():
        try:
            async with httpx.AsyncClient(verify=False, timeout=1.5) as client:
                await client.head(check_url)
            ok = True
            break
        except Exception:
            continue
    _reachable_cache.update(ok=ok, checked_at=now)
    return ok


class HandoffRequest(BaseModel):
    persona: str = ""
    display_name: str = ""


@router.get("/status")
async def resource_explorer_status():
    """Public — reachability + whether SSO is configured. No lock state to report."""
    reachable = await _resource_explorer_reachable()
    return {
        "reachable":      reachable,
        "sso_configured": bool(EGERIA_ADVISOR_SSO_SECRET),
    }


@router.post("/handoff")
async def handoff(request: Request, body: HandoffRequest):
    """Mint an SSO handoff URL for the caller's persona. No lock to acquire."""
    if not EGERIA_ADVISOR_SSO_SECRET:
        raise HTTPException(status_code=503, detail="Resource Explorer SSO is not configured (EGERIA_ADVISOR_SSO_SECRET unset)")
    if not body.persona:
        return {"ok": False, "reason": "Select a Coco persona first"}

    personas = _load_personas()
    persona = personas.get(body.persona)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona {body.persona!r} not found")

    user = _require_verified_or_local(request)

    try:
        sso_token = await make_portal_sso_token(user, body.persona, persona)
    except Exception as exc:
        logger.error(f"resource explorer: SSO token minting failed: {exc}")
        raise HTTPException(status_code=502, detail=f"Could not prepare Resource Explorer session: {exc}")

    resource_explorer_sso_url = f"{EGERIA_RESOURCE_EXPLORER_URL.rstrip('/')}/#pt={sso_token}"
    return {"ok": True, "resource_explorer_sso_url": resource_explorer_sso_url}
