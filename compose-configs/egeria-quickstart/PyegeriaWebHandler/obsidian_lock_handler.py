"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Obsidian session lock — manages exclusive access to the containerised Obsidian
(KasmVNC) instance so multiple demo users don't collide.

States
------
  FREE          Nobody holds the lock; anyone can acquire it.
  IN_USE        A user holds the lock; has an expiry and a keepalive timer.
  ADMIN_IN_USE  An admin holds the lock (e.g. live demo presentation).
  STUCK         The holder stopped sending keepalives; eligible for auto-release.

Persona injection
-----------------
On acquire, if a valid persona is supplied the handler merges that persona's
Egeria credentials into the Call Dr. Egeria plugin's data.json inside the
shared coco-workbooks vault volume.  The plugin's file-watcher detects the
change and reloads settings automatically.

On release / expiry, data.json is cleared back to defaults so the next user
doesn't inherit a previous persona.

Auth
----
In DEMO_MODE the acquire endpoint requires a verified JWT user; admin endpoints
require the admin role.  Outside DEMO_MODE all endpoints are open (single-user
local operation).
"""

import asyncio
import json
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
from pydantic import BaseModel

from demo_config import DEMO_MODE

router = APIRouter(prefix="/api/obsidian", tags=["obsidian-lock"])

# ── Configuration ──────────────────────────────────────────────────────────────

LOCK_ENABLED         = os.environ.get("OBSIDIAN_LOCK_ENABLED", "true").lower() not in ("false", "0", "no")

_SESSION_MINUTES     = int(os.environ.get("OBSIDIAN_SESSION_MINUTES",     "20"))
_IDLE_SOFT_MINUTES   = int(os.environ.get("OBSIDIAN_IDLE_SOFT_MINUTES",    "5"))
_IDLE_HARD_MINUTES   = int(os.environ.get("OBSIDIAN_IDLE_HARD_MINUTES",   "10"))
_BUFFER_MINUTES      = int(os.environ.get("OBSIDIAN_BUFFER_MINUTES",      "10"))
_EVICT_GRACE_SECONDS = int(os.environ.get("OBSIDIAN_EVICT_GRACE_SECONDS", "300"))
_CLEANUP_INTERVAL    = 60   # background task interval in seconds

_PLUGIN_DATA_JSON = Path(os.environ.get(
    "OBSIDIAN_PLUGIN_DATA_JSON",
    "/coco-workbooks/.obsidian/plugins/call-dr-egeria/data.json",
))
_LOCK_FILE = Path(os.environ.get(
    "OBSIDIAN_LOCK_STATE_FILE",
    "/app/demo-data/obsidian_lock.json",
))
_PERSONAS_FILE = Path(__file__).parent / "personas.json"

# ── In-memory state ────────────────────────────────────────────────────────────

_mu = asyncio.Lock()   # protects _state mutations

_state: dict = {
    "state":          "FREE",
    "holder_token":   None,   # opaque string; proves ownership for release/keepalive
    "holder_display": None,   # human-readable name shown in the portal
    "holder_persona": None,   # egeria user_id (e.g. "erinoverview")
    "acquired_at":    None,   # ISO datetime
    "expires_at":     None,   # ISO datetime
    "last_keepalive": None,   # ISO datetime
    "evicting":       False,  # True while grace period is running
    "evict_deadline": None,   # ISO datetime when eviction takes effect
}
_audit: list[dict] = []       # capped at 200 entries
_reservations: list[dict] = []
_res_seq = 0

_scheduler_task: Optional[asyncio.Task] = None


# ── Persistence helpers ────────────────────────────────────────────────────────

def _save_state() -> None:
    try:
        _LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        _LOCK_FILE.write_text(json.dumps(_state, default=str))
    except Exception as exc:
        logger.warning(f"obsidian lock: could not persist state: {exc}")


def _load_state() -> None:
    try:
        if _LOCK_FILE.exists():
            data = json.loads(_LOCK_FILE.read_text())
            _state.update(data)
            logger.info(f"obsidian lock: restored state '{_state['state']}' from disk")
    except Exception as exc:
        logger.warning(f"obsidian lock: could not load saved state: {exc}")


def _audit_entry(action: str, display: Optional[str] = None) -> None:
    global _audit
    _audit.append({
        "action":  action,
        "display": display or _state.get("holder_display"),
        "persona": _state.get("holder_persona"),
        "at":      datetime.utcnow().isoformat(),
    })
    if len(_audit) > 200:
        _audit = _audit[-200:]


# ── Persona injection ──────────────────────────────────────────────────────────

def _load_personas() -> dict:
    try:
        return json.loads(_PERSONAS_FILE.read_text())
    except Exception:
        return {}


def _inject_persona(persona_id: str) -> None:
    """Write persona credentials into the plugin's data.json."""
    if not _PLUGIN_DATA_JSON.exists():
        logger.warning(f"obsidian lock: plugin data.json not found at {_PLUGIN_DATA_JSON}")
        return
    personas = _load_personas()
    if persona_id not in personas:
        logger.warning(f"obsidian lock: unknown persona '{persona_id}' — skipping inject")
        return
    try:
        existing = json.loads(_PLUGIN_DATA_JSON.read_text())
    except Exception:
        existing = {}
    existing.update({
        "userId":   persona_id,
        "userPass": personas[persona_id].get("password", "secret"),
        "mcpToken": os.environ.get("MCP_ACCESS_TOKEN", "egeria-secret-mcp-token"),
    })
    _PLUGIN_DATA_JSON.write_text(json.dumps(existing, indent=2))
    logger.info(f"obsidian lock: injected persona '{persona_id}' into data.json")


def _clear_persona() -> None:
    """Reset persona-specific fields in the plugin's data.json."""
    if not _PLUGIN_DATA_JSON.exists():
        return
    try:
        existing = json.loads(_PLUGIN_DATA_JSON.read_text())
    except Exception:
        existing = {}
    existing.update({"userId": "", "userPass": "", "mcpToken": ""})
    _PLUGIN_DATA_JSON.write_text(json.dumps(existing, indent=2))
    logger.info("obsidian lock: cleared persona from data.json")


# ── State transitions ──────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _expiry_iso(minutes: int) -> str:
    return (datetime.utcnow() + timedelta(minutes=minutes)).isoformat()


def _parse_iso(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def _next_reservation_start() -> Optional[datetime]:
    now = datetime.utcnow()
    upcoming = [
        r for r in _reservations
        if _parse_iso(r["starts_at"]) and _parse_iso(r["starts_at"]) > now
    ]
    if not upcoming:
        return None
    return min(_parse_iso(r["starts_at"]) for r in upcoming)


def _buffer_clash() -> bool:
    """True if acquiring now would intrude on a reserved block's buffer window."""
    nrs = _next_reservation_start()
    if not nrs:
        return False
    buffer_end = datetime.utcnow() + timedelta(minutes=_SESSION_MINUTES + _BUFFER_MINUTES)
    return buffer_end > nrs


def _minutes_until_free() -> Optional[int]:
    exp = _parse_iso(_state.get("expires_at"))
    if not exp:
        return None
    delta = exp - datetime.utcnow()
    return max(0, int(delta.total_seconds() / 60))


def _do_release(reason: str = "released") -> None:
    _audit_entry(reason)
    if _state.get("holder_persona"):
        _clear_persona()
    _state.update({
        "state":          "FREE",
        "holder_token":   None,
        "holder_display": None,
        "holder_persona": None,
        "acquired_at":    None,
        "expires_at":     None,
        "last_keepalive": None,
        "evicting":       False,
        "evict_deadline": None,
    })
    _save_state()


# ── Background cleanup ─────────────────────────────────────────────────────────

async def start_scheduler() -> None:
    global _scheduler_task
    _load_state()
    _scheduler_task = asyncio.create_task(_cleanup_loop())
    logger.info("obsidian lock scheduler started")


async def stop_scheduler() -> None:
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass
    _scheduler_task = None


async def _cleanup_loop() -> None:
    while True:
        await asyncio.sleep(_CLEANUP_INTERVAL)
        try:
            await _run_cleanup()
        except Exception as exc:
            logger.error(f"obsidian lock cleanup error: {exc}")


async def _run_cleanup() -> None:
    async with _mu:
        now = datetime.utcnow()
        state = _state.get("state")

        if state in ("IN_USE", "ADMIN_IN_USE"):
            # Hard expiry
            exp = _parse_iso(_state.get("expires_at"))
            if exp and now > exp:
                logger.info("obsidian lock: session expired — releasing")
                _do_release("expired")
                return

            # Eviction deadline passed
            if _state.get("evicting"):
                deadline = _parse_iso(_state.get("evict_deadline"))
                if deadline and now > deadline:
                    logger.info("obsidian lock: eviction grace period over — releasing")
                    _do_release("evicted")
                    return

            # Idle hard timeout → STUCK
            ka = _parse_iso(_state.get("last_keepalive"))
            if ka:
                idle_seconds = (now - ka).total_seconds()
                if idle_seconds > _IDLE_HARD_MINUTES * 60:
                    logger.info(f"obsidian lock: idle {idle_seconds:.0f}s — marking STUCK")
                    _state["state"] = "STUCK"
                    _save_state()

        elif state == "STUCK":
            # Auto-release stuck sessions after double the hard idle timeout
            ka = _parse_iso(_state.get("last_keepalive"))
            if ka:
                idle_seconds = (now - ka).total_seconds()
                if idle_seconds > _IDLE_HARD_MINUTES * 2 * 60:
                    logger.info("obsidian lock: stuck session auto-released")
                    _do_release("auto_released_stuck")


# ── Auth helpers ───────────────────────────────────────────────────────────────

def _require_lock_enabled():
    if not LOCK_ENABLED:
        raise HTTPException(status_code=503, detail="Obsidian lock is disabled on this instance (OBSIDIAN_LOCK_ENABLED=false)")


def _opt_user(request: Request):
    """Returns the current user if in demo mode + authenticated, else None."""
    if not DEMO_MODE:
        return None
    try:
        from demo_auth_handler import get_current_user
        from demo_db import get_db
        db = next(get_db())
        return get_current_user(request, db)
    except Exception:
        return None


def _require_admin_or_local(request: Request):
    if not DEMO_MODE:
        return None   # local mode: admin operations always allowed
    from demo_auth_handler import require_admin
    from demo_db import get_db
    db = next(get_db())
    return require_admin(request, db)


def _require_verified_or_local(request: Request):
    if not DEMO_MODE:
        return None
    from demo_auth_handler import require_verified_user
    from demo_db import get_db
    db = next(get_db())
    return require_verified_user(request, db)


# ── Request / response models ──────────────────────────────────────────────────

class AcquireRequest(BaseModel):
    persona:      str = ""   # egeria user_id from personas.json
    display_name: str = ""   # human-readable name for the portal UI


class ReleaseRequest(BaseModel):
    token: str


class KeepaliveRequest(BaseModel):
    token: str


class ExtendRequest(BaseModel):
    token: str


class ReservationRequest(BaseModel):
    label:     str
    starts_at: str   # ISO datetime
    ends_at:   str   # ISO datetime


class EvictRequest(BaseModel):
    grace_seconds: int = _EVICT_GRACE_SECONDS
    message: str = ""


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/status")
async def obsidian_status(request: Request):
    """Public — current lock state, time remaining, next reservation."""
    if not LOCK_ENABLED:
        return {"state": "DISABLED"}
    async with _mu:
        now = datetime.utcnow()
        state = _state["state"]
        minutes_left = _minutes_until_free()

        # Soft-idle warning flag for the portal (no state change here)
        idle_warning = False
        ka = _parse_iso(_state.get("last_keepalive"))
        if ka and state in ("IN_USE", "ADMIN_IN_USE"):
            idle_warning = (now - ka).total_seconds() > _IDLE_SOFT_MINUTES * 60

        # Next reservation
        nrs = _next_reservation_start()

        return {
            "state":           state,
            "holder_display":  _state.get("holder_display"),
            "holder_persona":  _state.get("holder_persona"),
            "acquired_at":     _state.get("acquired_at"),
            "expires_at":      _state.get("expires_at"),
            "minutes_left":    minutes_left,
            "idle_warning":    idle_warning,
            "evicting":        _state.get("evicting", False),
            "evict_deadline":  _state.get("evict_deadline"),
            "next_reservation_at": nrs.isoformat() if nrs else None,
            "buffer_minutes":  _BUFFER_MINUTES,
            "session_minutes": _SESSION_MINUTES,
        }


@router.post("/acquire")
async def acquire(request: Request, body: AcquireRequest, _: None = Depends(_require_lock_enabled)):
    """Acquire the Obsidian lock. Returns a session token the caller must use for keepalive/release."""
    user = _require_verified_or_local(request)

    async with _mu:
        state = _state["state"]
        if state not in ("FREE",):
            minutes = _minutes_until_free()
            nrs = _next_reservation_start()
            return {
                "acquired": False,
                "reason": f"Obsidian is {state.lower().replace('_', ' ')}",
                "minutes_left": minutes,
                "next_reservation_at": nrs.isoformat() if nrs else None,
            }

        if _buffer_clash():
            nrs = _next_reservation_start()
            return {
                "acquired": False,
                "reason": "Too close to a reserved block — session would run into reserved time",
                "next_reservation_at": nrs.isoformat() if nrs else None,
            }

        # Determine identity
        if user:
            token = user.id
            display = body.display_name or getattr(user, "display_name", user.email)
            is_admin = getattr(user, "role", "") == "admin"
        else:
            token = secrets.token_urlsafe(24)
            display = body.display_name or "Local user"
            is_admin = False

        persona = body.persona or ""

        _state.update({
            "state":          "ADMIN_IN_USE" if is_admin else "IN_USE",
            "holder_token":   token,
            "holder_display": display,
            "holder_persona": persona or None,
            "acquired_at":    _now_iso(),
            "expires_at":     _expiry_iso(_SESSION_MINUTES),
            "last_keepalive": _now_iso(),
            "evicting":       False,
            "evict_deadline": None,
        })
        _audit_entry("acquired")
        _save_state()

        if persona:
            _inject_persona(persona)

        logger.info(f"obsidian lock acquired by '{display}' (persona={persona or 'none'})")

        return {
            "acquired":   True,
            "token":      token,
            "expires_at": _state["expires_at"],
            "session_minutes": _SESSION_MINUTES,
        }


@router.post("/release")
async def release(request: Request, body: ReleaseRequest, _: None = Depends(_require_lock_enabled)):
    """Release the lock. Must present the token returned at acquire time."""
    async with _mu:
        if _state["state"] == "FREE":
            return {"released": True, "note": "already free"}
        if _state.get("holder_token") != body.token:
            raise HTTPException(status_code=403, detail="Not the lock holder")
        _do_release("released")
        logger.info("obsidian lock released by holder")
        return {"released": True}


@router.post("/keepalive")
async def keepalive(request: Request, body: KeepaliveRequest, _: None = Depends(_require_lock_enabled)):
    """Heartbeat — resets the idle clock. Portal should call this every 60 s."""
    async with _mu:
        if _state["state"] == "FREE":
            raise HTTPException(status_code=409, detail="No active session")
        if _state.get("holder_token") != body.token:
            raise HTTPException(status_code=403, detail="Not the lock holder")
        _state["last_keepalive"] = _now_iso()
        # Recover from STUCK if the holder comes back
        if _state["state"] == "STUCK":
            _state["state"] = "IN_USE"
        _save_state()
        return {"ok": True, "expires_at": _state.get("expires_at")}


@router.post("/extend")
async def extend(request: Request, body: ExtendRequest, _: None = Depends(_require_lock_enabled)):
    """Extend the session by _SESSION_MINUTES, if no reservation is blocking."""
    async with _mu:
        if _state["state"] == "FREE":
            raise HTTPException(status_code=409, detail="No active session")
        if _state.get("holder_token") != body.token:
            raise HTTPException(status_code=403, detail="Not the lock holder")
        if _buffer_clash():
            nrs = _next_reservation_start()
            return {
                "extended": False,
                "reason": "Too close to a reserved block",
                "next_reservation_at": nrs.isoformat() if nrs else None,
            }
        _state["expires_at"] = _expiry_iso(_SESSION_MINUTES)
        _save_state()
        return {"extended": True, "expires_at": _state["expires_at"]}


# ── Reservation endpoints ──────────────────────────────────────────────────────

@router.get("/reservations")
async def list_reservations(request: Request):
    """Public — list upcoming reservations."""
    now = datetime.utcnow()
    upcoming = [r for r in _reservations if _parse_iso(r["ends_at"]) and _parse_iso(r["ends_at"]) > now]
    return {"reservations": sorted(upcoming, key=lambda r: r["starts_at"])}


@router.post("/reservations")
async def create_reservation(request: Request, body: ReservationRequest, _: None = Depends(_require_lock_enabled)):
    """Admin — reserve a future block."""
    global _res_seq
    _require_admin_or_local(request)

    starts = _parse_iso(body.starts_at)
    ends   = _parse_iso(body.ends_at)
    if not starts or not ends or ends <= starts:
        raise HTTPException(status_code=400, detail="Invalid starts_at / ends_at")

    # Conflict check
    for r in _reservations:
        rs = _parse_iso(r["starts_at"])
        re = _parse_iso(r["ends_at"])
        if rs and re and not (ends <= rs or starts >= re):
            raise HTTPException(status_code=409, detail=f"Conflicts with reservation {r['id']}: {r['label']}")

    _res_seq += 1
    entry = {
        "id":         _res_seq,
        "label":      body.label,
        "starts_at":  body.starts_at,
        "ends_at":    body.ends_at,
        "created_at": _now_iso(),
    }
    _reservations.append(entry)
    logger.info(f"obsidian reservation created: {body.label} ({body.starts_at} → {body.ends_at})")
    return entry


@router.delete("/reservations/{res_id}")
async def delete_reservation(request: Request, res_id: int, _: None = Depends(_require_lock_enabled)):
    """Admin — cancel a reservation."""
    global _reservations
    _require_admin_or_local(request)
    before = len(_reservations)
    _reservations = [r for r in _reservations if r["id"] != res_id]
    if len(_reservations) == before:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"deleted": True}


# ── Admin override endpoints ───────────────────────────────────────────────────

@router.post("/evict")
async def evict(request: Request, body: EvictRequest, _: None = Depends(_require_lock_enabled)):
    """Admin — begin grace-period eviction of the current holder."""
    _require_admin_or_local(request)
    async with _mu:
        if _state["state"] == "FREE":
            raise HTTPException(status_code=409, detail="Nothing to evict — lock is free")
        if _state.get("evicting"):
            return {"evicting": True, "evict_deadline": _state.get("evict_deadline"), "note": "already evicting"}
        grace = max(10, body.grace_seconds)
        deadline = (datetime.utcnow() + timedelta(seconds=grace)).isoformat()
        _state["evicting"]      = True
        _state["evict_deadline"] = deadline
        _save_state()
        logger.info(f"obsidian lock eviction started — grace {grace}s, deadline {deadline}")
        return {
            "evicting":       True,
            "evict_deadline": deadline,
            "grace_seconds":  grace,
            "message":        body.message or f"An admin needs Obsidian in {grace // 60} min. Please save and close.",
        }


@router.post("/unlock")
async def force_unlock(request: Request, _: None = Depends(_require_lock_enabled)):
    """Admin — force-release a stuck or frozen lock."""
    _require_admin_or_local(request)
    async with _mu:
        if _state["state"] == "FREE":
            return {"unlocked": False, "note": "already free"}
        _do_release("force_unlocked")
        logger.info("obsidian lock force-unlocked by admin")
        return {"unlocked": True}


@router.get("/audit")
async def get_audit(request: Request, _: None = Depends(_require_lock_enabled)):
    """Admin — recent lock audit log."""
    _require_admin_or_local(request)
    return {"audit": list(reversed(_audit[-50:]))}
