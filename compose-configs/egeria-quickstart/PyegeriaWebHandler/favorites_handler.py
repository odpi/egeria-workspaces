"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Favorites — FastAPI router.

Stores per-user, per-persona portal favorites (links to sections within SPAs).
In demo mode the favorites are persisted in Postgres (demo_auth.favorites).
Without authentication (local mode) the endpoint returns persona defaults.

Endpoints:
  GET    /api/favorites?persona=<id>            → list favorites (or defaults)
  POST   /api/favorites?persona=<id>            → add a favorite
  DELETE /api/favorites/<id>                    → remove a favorite
  POST   /api/favorites/reorder?persona=<id>    → update positions [{id, position}, …]
  POST   /api/favorites/reset?persona=<id>      → reset to persona defaults
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from demo_auth_handler import get_current_user
from demo_db import Favorite, get_db

router = APIRouter(tags=["favorites"])

# ── Per-persona default favorites ──────────────────────────────────────────────
# These are returned when a user has no saved favorites yet, and in local mode.
# Each entry: {app, section, label, icon, url}

_PERSONA_DEFAULTS: dict[str, list[dict]] = {
    "erinoverview": [
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "data-design",       "label": "Data Design",                 "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "solution-architect","label": "Solution Architect",           "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "notelogs",          "label": "Note Logs",                   "icon": "📝", "url": "/egeria-explorer#notelogs"},
        {"app": "type-explorer", "section": "projects",          "label": "Projects",                    "icon": "📋", "url": "/egeria-explorer#projects"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "collections",       "label": "Collections",                 "icon": "📁", "url": "/egeria-explorer#collections"},
        {"app": "tech-catalog",  "section": "assets",            "label": "Data Assets",                 "icon": "🗃️", "url": "/tech-catalog"},
    ],
    "peterprofile": [
        {"app": "type-explorer", "section": "data-design",       "label": "Data Design",                 "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "collections",       "label": "Collections",                 "icon": "📁", "url": "/egeria-explorer#collections"},
    ],
    "calliequartile": [
        {"app": "type-explorer", "section": "data-design",       "label": "Data Design",                 "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
    ],
    "garygeeke": [
        {"app": "type-explorer", "section": "type-system",       "label": "Type Explorer",               "icon": "🔬", "url": "/egeria-explorer#type-system"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "digital-products",  "label": "Digital Products",            "icon": "📦", "url": "/egeria-explorer#digital-products"},
        {"app": "egeria-operations", "section": "",              "label": "Operations",                  "icon": "⚙️", "url": "/egeria-operations"},
    ],
    "ivorpadlock": [
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "perspectives",      "label": "Perspectives",                "icon": "👁️", "url": "/egeria-explorer#perspectives"},
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
    ],
    "faithbroker": [
        {"app": "type-explorer", "section": "perspectives",      "label": "Perspectives",                "icon": "👁️", "url": "/egeria-explorer#perspectives"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "actors",            "label": "Actors",                      "icon": "👥", "url": "/egeria-explorer#actors"},
    ],
    "pollytasker": [
        {"app": "type-explorer", "section": "solution-architect","label": "Solution Architect",           "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "projects",          "label": "Projects",                    "icon": "📋", "url": "/egeria-explorer#projects"},
        {"app": "type-explorer", "section": "perspectives",      "label": "Perspectives",                "icon": "👁️", "url": "/egeria-explorer#perspectives"},
    ],
    "tomtally": [
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "glossary",          "label": "Glossary",                    "icon": "📖", "url": "/egeria-explorer#glossary"},
        {"app": "type-explorer", "section": "data-design",       "label": "Data Design",                 "icon": "🗄️", "url": "/egeria-explorer#data-design"},
    ],
    "lemmiestage": [
        {"app": "type-explorer", "section": "type-system",       "label": "Type Explorer",               "icon": "🔬", "url": "/egeria-explorer#type-system"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "egeria-operations", "section": "",              "label": "Operations",                  "icon": "⚙️", "url": "/egeria-operations"},
    ],
    "juleskeeper": [
        {"app": "type-explorer", "section": "solution-architect","label": "Solution Architect",           "icon": "🏗️", "url": "/egeria-explorer#solution-architect"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
        {"app": "type-explorer", "section": "perspectives",      "label": "Perspectives",                "icon": "👁️", "url": "/egeria-explorer#perspectives"},
    ],
    "stewfaster": [
        {"app": "type-explorer", "section": "isc",               "label": "Information Supply Chains",   "icon": "🔗", "url": "/egeria-explorer#isc"},
        {"app": "type-explorer", "section": "data-design",       "label": "Data Design",                 "icon": "🗄️", "url": "/egeria-explorer#data-design"},
        {"app": "type-explorer", "section": "governance",        "label": "Governance",                  "icon": "⚖️", "url": "/egeria-explorer#governance"},
    ],
}


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


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/favorites")
def list_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse(_defaults_with_ids(persona))

    rows = (
        db.query(Favorite)
        .filter_by(user_email=user.email, persona_id=persona)
        .order_by(Favorite.position)
        .all()
    )
    if rows:
        return JSONResponse([_row_to_dict(r) for r in rows])

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

    body = await request.json()
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

    max_pos = db.query(Favorite).filter_by(user_email=user.email, persona_id=persona).count()
    fav = Favorite(
        id=str(uuid.uuid4()),
        user_email=user.email,
        persona_id=persona,
        app=app,
        section=section,
        label=label,
        icon=icon,
        url=url,
        position=max_pos,
        created_at=datetime.utcnow(),
    )
    db.add(fav)
    db.commit()
    return JSONResponse({"status": "added", "id": fav.id})


@router.delete("/api/favorites/{fav_id}")
def remove_favorite(
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

    db.delete(fav)
    db.commit()
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
    return JSONResponse({"status": "reordered"})


@router.post("/api/favorites/reset")
def reset_favorites(
    persona: str = Query(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    db.query(Favorite).filter_by(user_email=user.email, persona_id=persona).delete()
    db.commit()
    return JSONResponse({"status": "reset"})


def reset_all_favorites_for_demo_reset(db: Session) -> None:
    """Called during demo reset — wipes all per-user favorites so everyone reverts to defaults."""
    db.query(Favorite).delete()
    db.commit()
