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

from demo_auth_handler import get_current_user, require_admin
from demo_db import Favorite, User, get_db
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

def _effective_email(user, persona: str) -> str:
    """Return the DB key to use for this request.

    Authenticated users (demo portal login) use their real email so favourites
    are tied to a verified identity.  Unauthenticated requests (local mode, or
    SPA pages accessed before the portal session cookie is set) fall back to a
    per-persona synthetic key so changes still persist across page loads.
    """
    return user.email if user else f"local:{persona}"


def _old_url_format(url: str) -> bool:
    """Return True for the legacy '#section?param=value' URL format (hash before query)."""
    if not url or '#' not in url or '?' not in url:
        return False
    return url.index('#') < url.index('?')


@router.get("/api/favorites")
async def list_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user  = get_current_user(request, db)
    email = _effective_email(user, persona)

    # 1. Postgres cache hit
    rows = (
        db.query(Favorite)
        .filter_by(user_email=email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if rows:
        # Purge any rows stored in the old '#section?param=value' URL format.
        # These were created before the URL-format fix and can no longer be matched
        # by FavoriteButtons (which now generate '?param=value#section'), so they
        # only appear as unexpected duplicates in the portal chip strip.
        stale = [r for r in rows if _old_url_format(r.url)]
        if stale:
            for r in stale:
                db.delete(r)
            db.commit()
            rows = [r for r in rows if not _old_url_format(r.url)]

        # Deduplicate by URL (keep the highest-position row for each URL).
        seen: dict[str, Favorite] = {}
        for r in rows:
            if r.url not in seen or r.position > seen[r.url].position:
                seen[r.url] = r
        deduped = sorted(seen.values(), key=lambda r: r.position)
        if len(deduped) < len(rows):
            # Remove the extra rows so the DB stays clean.
            keep_ids = {r.id for r in deduped}
            for r in rows:
                if r.id not in keep_ids:
                    db.delete(r)
            db.commit()

        if deduped:
            return JSONResponse([_row_to_dict(r) for r in deduped])

    # 2. Authenticated users: try to seed from Egeria
    if user:
        egeria_favs = await _egeria_read_favorites(persona)
        if egeria_favs:
            _write_to_db(db, email, persona, egeria_favs)
            rows = (
                db.query(Favorite)
                .filter_by(user_email=email, persona_id=persona)
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
    user  = get_current_user(request, db)
    email = _effective_email(user, persona)

    body    = await request.json()
    app     = body.get("app", "")
    section = body.get("section", "")
    label   = body.get("label", section)
    icon    = body.get("icon", "⭐")
    url     = body.get("url", "")

    has_rows = db.query(Favorite).filter_by(user_email=email, persona_id=persona).first() is not None
    if not has_rows:
        # First customization — materialize the defaults that were being displayed.
        # Exclude any page-level default for the same section as the item being added
        # to avoid an unexpected "duplicate" (e.g. section chip + element chip for ISC).
        persona_defaults = _PERSONA_DEFAULTS.get(persona, [])
        defaults_to_write = [
            d for d in persona_defaults
            if not (d.get("app") == app and d.get("section") == section)
        ]
        _write_to_db(db, email, persona, defaults_to_write)

    existing = (
        db.query(Favorite)
        .filter_by(user_email=email, persona_id=persona, url=url)
        .first()
    )
    if existing:
        return JSONResponse({"status": "already_exists", "id": existing.id})

    pos = db.query(Favorite).filter_by(user_email=email, persona_id=persona).count()
    fav = Favorite(
        id=str(uuid.uuid4()),
        user_email=email,
        persona_id=persona,
        app=app, section=section, label=label, icon=icon, url=url,
        position=pos,
        created_at=datetime.utcnow(),
    )
    db.add(fav)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if user:
        await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "added", "id": fav.id})


@router.delete("/api/favorites/{fav_id}")
async def remove_favorite(
    fav_id: str,
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user  = get_current_user(request, db)
    email = _effective_email(user, persona)

    if fav_id.startswith("default-"):
        # Synthetic id for a not-yet-persisted default.
        # Materialize the remaining defaults (minus this one) while preserving any
        # element-level rows that were explicitly added (not part of the defaults).
        try:
            idx = int(fav_id.split("-", 1)[1])
        except ValueError:
            idx = -1
        defaults = _PERSONA_DEFAULTS.get(persona, [])
        default_urls = {d.get("url", "") for d in defaults}

        # Collect any real (element-level) rows that aren't part of the defaults.
        existing = db.query(Favorite).filter_by(user_email=email, persona_id=persona).all()
        extra_rows = [_row_to_dict(r) for r in existing if r.url not in default_urls]

        # Defaults minus the removed one, excluding any URLs already in extra_rows.
        extra_urls = {r["url"] for r in extra_rows}
        remaining_defaults = [
            d for i, d in enumerate(defaults)
            if i != idx and d.get("url", "") not in extra_urls
        ]

        combined = remaining_defaults + extra_rows
        _write_to_db(db, email, persona, combined)
        if user:
            await _egeria_write_favorites(persona, combined)
        return JSONResponse({"status": "deleted"})

    fav = db.get(Favorite, fav_id)
    if not fav or fav.user_email != email:
        raise HTTPException(status_code=404, detail="Not found")

    persona = fav.persona_id
    db.delete(fav)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if user:
        await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "deleted"})


@router.post("/api/favorites/reorder")
async def reorder_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user  = get_current_user(request, db)
    email = _effective_email(user, persona)

    items = await request.json()  # [{id, position}, …]
    for item in items:
        fav = db.get(Favorite, item.get("id"))
        if fav and fav.user_email == email and fav.persona_id == persona:
            fav.position = item.get("position", 0)
    db.commit()

    all_rows = (
        db.query(Favorite)
        .filter_by(user_email=email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if user:
        await _egeria_write_favorites(persona, [_row_to_dict(r) for r in all_rows])
    return JSONResponse({"status": "reordered"})


@router.post("/api/favorites/reset")
async def reset_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user  = get_current_user(request, db)
    email = _effective_email(user, persona)

    db.query(Favorite).filter_by(user_email=email, persona_id=persona).delete()
    db.commit()
    if user:
        await _egeria_write_favorites(persona, [])
    return JSONResponse({"status": "reset"})


def reset_all_favorites_for_demo_reset(db: Session) -> None:
    """Called during demo reset — wipes all per-user Postgres favorites.
    Each user's next GET will re-read from Egeria (or fall back to hardcoded defaults).
    """
    db.query(Favorite).delete()
    db.commit()


# ── Admin ─────────────────────────────────────────────────────────────────────

@router.post("/api/admin/favorites/sync-to-egeria",
             summary="Push current Postgres favorites back to Egeria (admin only)")
async def admin_sync_favorites_to_egeria(
    persona: Optional[str] = Query(None, description="Limit sync to a single persona id; omit for all personas"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Push the current Postgres favorites for one persona (or every persona that has
    saved favorites) back into Egeria Person.additionalProperties, making the
    currently-displayed set the new canonical default for that persona.

    If more than one portal user has saved favorites under the same persona, the
    most recently created set is used as the source of truth.
    """
    query = db.query(Favorite.persona_id).distinct()
    if persona:
        query = query.filter(Favorite.persona_id == persona)
    persona_ids = [row[0] for row in query.all()]

    if not persona_ids:
        raise HTTPException(status_code=404, detail="No favorites found to sync")

    results: dict[str, dict] = {}
    for pid in persona_ids:
        rows = db.query(Favorite).filter_by(persona_id=pid).order_by(Favorite.created_at).all()
        if not rows:
            continue
        latest_email = max(rows, key=lambda r: r.created_at).user_email
        favs = sorted(
            (r for r in rows if r.user_email == latest_email),
            key=lambda r: r.position,
        )
        fav_dicts = [_row_to_dict(r) for r in favs]
        await _egeria_write_favorites(pid, fav_dicts)
        results[pid] = {"synced_count": len(fav_dicts), "source_user": latest_email}

    return JSONResponse({"status": "synced", "personas": results})
