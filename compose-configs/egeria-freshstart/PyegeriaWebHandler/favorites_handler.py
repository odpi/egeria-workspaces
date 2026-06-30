"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Favorites — FastAPI router.

Architecture:
  - Egeria Person.additionalProperties["portal_favorites"] is the canonical store,
    read/written using ActorManager instantiated with the persona's own credentials.
  - Postgres demo_auth.favorites is the per-portal-user runtime cache (populated
    from Egeria on first access, persists until reset).
  - In local mode (no auth) the endpoint returns per-persona hardcoded defaults.

Endpoints:
  GET    /api/favorites?persona=<id>            → list favorites (or defaults)
  POST   /api/favorites?persona=<id>            → add a favorite
  DELETE /api/favorites/<id>                    → remove a favorite
  POST   /api/favorites/reorder?persona=<id>    → update positions [{id, position}, …]
  POST   /api/favorites/reset?persona=<id>      → reset to persona defaults
"""

import json
import os
import uuid
from datetime import datetime
from typing import Optional

import pyegeria
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.orm import Session

from demo_auth_handler import get_current_user
from demo_db import Favorite, get_db
from egeria_auth import async_apply_token

router = APIRouter(tags=["favorites"])

pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

# ── Per-persona hardcoded defaults ────────────────────────────────────────────
# Returned when neither Postgres nor Egeria has favorites saved yet.

_PERSONA_DEFAULTS: dict[str, list[dict]] = {
    "erinoverview": [
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "data-design",        "label": "Data Design",                "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "solution-architect", "label": "Solution Architect",          "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "notelogs",           "label": "Note Logs",                  "icon": "📝", "url": "/egeria-explorer#notelogs"},
        {"app": "type-explorer", "section": "projects",           "label": "Projects",                   "icon": "📋", "url": "/egeria-explorer#projects"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "collections",        "label": "Collections",                "icon": "📁", "url": "/egeria-explorer#collections"},
        {"app": "tech-catalog",  "section": "assets",             "label": "Data Assets",                "icon": "🗃️", "url": "/tech-catalog"},
    ],
    "peterprofile": [
        {"app": "type-explorer", "section": "data-design",        "label": "Data Design",                "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "collections",        "label": "Collections",                "icon": "📁", "url": "/egeria-explorer#collections"},
    ],
    "calliequartile": [
        {"app": "type-explorer", "section": "data-design",        "label": "Data Design",                "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
    ],
    "garygeeke": [
        {"app": "type-explorer", "section": "type-system",        "label": "Type Explorer",              "icon": "🔬", "url": "/egeria-explorer#type-system"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "digital-products",   "label": "Digital Products",           "icon": "📦", "url": "/egeria-explorer#digital-products"},
        {"app": "egeria-operations", "section": "",               "label": "Operations",                 "icon": "⚙️", "url": "/egeria-operations"},
    ],
    "ivorpadlock": [
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "perspectives",       "label": "Perspectives",               "icon": "👁️", "url": "/egeria-explorer#perspectives"},
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
    ],
    "faithbroker": [
        {"app": "type-explorer", "section": "perspectives",       "label": "Perspectives",               "icon": "👁️", "url": "/egeria-explorer#perspectives"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "actors",             "label": "Actors",                     "icon": "👥", "url": "/egeria-explorer#actors"},
    ],
    "pollytasker": [
        {"app": "type-explorer", "section": "solution-architect", "label": "Solution Architect",          "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "projects",           "label": "Projects",                   "icon": "📋", "url": "/egeria-explorer#projects"},
        {"app": "type-explorer", "section": "perspectives",       "label": "Perspectives",               "icon": "👁️", "url": "/egeria-explorer#perspectives"},
    ],
    "tomtally": [
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "glossary",           "label": "Glossary",                   "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "data-design",        "label": "Data Design",                "icon": "🗄️", "url": "/egeria-explorer#data-design"},
    ],
    "lemmiestage": [
        {"app": "type-explorer", "section": "type-system",        "label": "Type Explorer",              "icon": "🔬", "url": "/egeria-explorer#type-system"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "egeria-operations", "section": "",               "label": "Operations",                 "icon": "⚙️", "url": "/egeria-operations"},
    ],
    "juleskeeper": [
        {"app": "type-explorer", "section": "solution-architect", "label": "Solution Architect",          "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "perspectives",       "label": "Perspectives",               "icon": "👁️", "url": "/egeria-explorer#perspectives"},
    ],
    "stewfaster": [
        {"app": "type-explorer", "section": "isc",                "label": "Information Supply Chains",  "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "data-design",        "label": "Data Design",                "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "governance",         "label": "Governance",                 "icon": "⚖️", "url": "/egeria-explorer#governance"},
    ],
}

# ── Egeria helpers ────────────────────────────────────────────────────────────

# In-memory GUID cache: persona_id → Egeria element GUID.
# GUIDs are stable for the life of the Egeria instance.
_guid_cache: dict[str, str] = {}

_PERSONAS_PATH = os.path.join(os.path.dirname(__file__), "personas.json")
_personas_data: dict = {}


def _persona_pwd(persona_id: str) -> str:
    global _personas_data
    if not _personas_data:
        try:
            with open(_PERSONAS_PATH) as f:
                _personas_data = json.load(f)
        except Exception:
            pass
    return _personas_data.get(persona_id, {}).get("password", "secret")


async def _actor_manager(persona_id: str):
    from pyegeria.omvs.actor_manager import ActorManager
    url    = os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER",  "qs-view-server")
    mgr = ActorManager(
        view_server=server, platform_url=url,
        user_id=persona_id, user_pwd=_persona_pwd(persona_id),
    )
    await async_apply_token(mgr)
    return mgr


async def _find_profile(mgr, persona_id: str) -> tuple[str | None, dict]:
    """Return (guid, properties_dict) for the persona's Person element."""
    try:
        profiles = await mgr._async_find_actor_profiles(
            search_string=persona_id, ignore_case=True, output_format="JSON"
        )
        if not isinstance(profiles, list):
            return None, {}
        for p in profiles:
            hdr  = p.get("elementHeader") or {}
            guid = hdr.get("guid")
            props = p.get("properties") or {}
            if guid:
                _guid_cache[persona_id] = guid
                return guid, props
    except Exception as e:
        logger.warning(f"[favorites] Egeria profile lookup failed for {persona_id}: {e}")
    return None, {}


async def _egeria_read_favorites(persona_id: str) -> list[dict] | None:
    """Read portal_favorites from Egeria additionalProperties. Returns None on any failure."""
    try:
        mgr = await _actor_manager(persona_id)
        guid, props = await _find_profile(mgr, persona_id)
        if not guid:
            return None
        raw = (props.get("additionalProperties") or {}).get("portal_favorites")
        if raw:
            return json.loads(raw)
    except Exception as e:
        logger.warning(f"[favorites] Egeria read failed for {persona_id}: {e}")
    return None


async def _egeria_write_favorites(persona_id: str, favs: list[dict]) -> None:
    """Write portal_favorites to Egeria additionalProperties (fire-and-forget on error)."""
    try:
        mgr = await _actor_manager(persona_id)
        guid = _guid_cache.get(persona_id)
        if not guid:
            guid, _ = await _find_profile(mgr, persona_id)
            if not guid:
                logger.warning(f"[favorites] No GUID for {persona_id}, skip Egeria write")
                return
        # Strip internal DB fields before storing in Egeria
        clean = [
            {k: v for k, v in f.items() if k in ("app", "section", "label", "icon", "url", "position")}
            for f in favs
        ]
        body = {
            "class": "UpdateElementRequestBody",
            "mergeUpdate": True,
            "properties": {
                "class": "ActorProfileProperties",
                "additionalProperties": {
                    "portal_favorites": json.dumps(clean)
                },
            },
        }
        await mgr._async_update_actor_profile(guid, body)
    except Exception as e:
        logger.warning(f"[favorites] Egeria write failed for {persona_id}: {e}")


# ── DB helpers ────────────────────────────────────────────────────────────────

def _row_to_dict(row: Favorite) -> dict:
    return {
        "id":         row.id,
        "app":        row.app,
        "section":    row.section,
        "label":      row.label,
        "icon":       row.icon or "⭐",
        "url":        row.url,
        "position":   row.position or 0,
        "persona_id": row.persona_id,
    }


def _defaults_with_ids(persona_id: str) -> list[dict]:
    defaults = _PERSONA_DEFAULTS.get(persona_id, [])
    return [dict(d, id=f"default-{i}", persona_id=persona_id, position=i)
            for i, d in enumerate(defaults)]


def _write_to_db(db: Session, user_email: str, persona_id: str, favs: list[dict]) -> None:
    """Replace all DB favorites for (user_email, persona_id) with the given list."""
    db.query(Favorite).filter_by(user_email=user_email, persona_id=persona_id).delete()
    for i, f in enumerate(favs):
        db.add(Favorite(
            id=str(uuid.uuid4()),
            user_email=user_email,
            persona_id=persona_id,
            app=f.get("app", ""),
            section=f.get("section", ""),
            label=f.get("label", ""),
            icon=f.get("icon", "⭐"),
            url=f.get("url", ""),
            position=f.get("position", i),
            created_at=datetime.utcnow(),
        ))
    db.commit()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/favorites")
async def list_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        # Local mode — return hardcoded defaults (no persistence)
        return JSONResponse(_defaults_with_ids(persona))

    # 1. Postgres cache hit
    rows = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if rows:
        return JSONResponse([_row_to_dict(r) for r in rows])

    # 2. Read from Egeria (authed as the persona)
    egeria_favs = await _egeria_read_favorites(persona)
    if egeria_favs:
        _write_to_db(db, user.email, persona, egeria_favs)
        rows = (
            db.query(Favorite)
            .filter_by(user_email=user.email, persona_id=persona)
            .order_by(Favorite.position)
            .all()
        )
        return JSONResponse([_row_to_dict(r) for r in rows])

    # 3. Fall back to hardcoded defaults
    return JSONResponse(_defaults_with_ids(persona))


@router.post("/api/favorites")
async def add_favorite(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    body    = await request.json()
    app     = body.get("app", "")
    section = body.get("section", "")
    label   = body.get("label", section)
    icon    = body.get("icon", "⭐")
    url     = body.get("url", "")

    existing = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona, app=app, section=section)
        .first()
    )
    if existing:
        return JSONResponse({"status": "already_exists", "id": existing.id})

    pos = db.query(Favorite).filter_by(user_email=user.email, persona_id=persona).count()
    fav = Favorite(
        id=str(uuid.uuid4()),
        user_email=user.email,
        persona_id=persona,
        app=app, section=section, label=label, icon=icon, url=url,
        position=pos,
        created_at=datetime.utcnow(),
    )
    db.add(fav)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "added", "id": fav.id})


@router.delete("/api/favorites/{fav_id}")
async def remove_favorite(
    fav_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    fav = db.get(Favorite, fav_id)
    if not fav or fav.user_email != user.email:
        raise HTTPException(status_code=404, detail="Not found")

    persona = fav.persona_id
    db.delete(fav)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "deleted"})


@router.post("/api/favorites/reorder")
async def reorder_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    items = await request.json()  # [{id, position}, …]
    for item in items:
        fav = db.get(Favorite, item.get("id"))
        if fav and fav.user_email == user.email and fav.persona_id == persona:
            fav.position = item.get("position", 0)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "reordered"})


@router.post("/api/favorites/reset")
async def reset_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    db.query(Favorite).filter_by(user_email=user.email, persona_id=persona).delete()
    db.commit()
    # Clear Egeria storage so Egeria also reverts to having no custom favorites
    await _egeria_write_favorites(persona, [])
    return JSONResponse({"status": "reset"})


def reset_all_favorites_for_demo_reset(db: Session) -> None:
    """Called during demo reset — wipes all per-user Postgres favorites.
    Each user's next GET will re-read from Egeria (or fall back to hardcoded defaults).
    """
    db.query(Favorite).delete()
    db.commit()
