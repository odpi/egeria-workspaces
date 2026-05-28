"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo feedback handler — captures user experience feedback in a local SQLite
database that persists in the /app/demo-data volume.

POST /api/demo-feedback        — submit feedback (any visitor)
GET  /api/demo-feedback        — retrieve all records (admin only)
"""

import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

# ── Config ─────────────────────────────────────────────────────────────────────

_DB_PATH    = os.environ.get("FEEDBACK_DB_PATH", "/app/demo-data/feedback.db")
_JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-before-going-public")

# ── Model ──────────────────────────────────────────────────────────────────────

class _Base(DeclarativeBase):
    pass


class DemoFeedback(_Base):
    __tablename__ = "demo_feedback"

    id            = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id    = Column(String(36))
    user_id       = Column(String(200))    # JWT sub if available, else null
    section       = Column(String(100))
    star_rating   = Column(Integer)        # 1-5 or null
    comment       = Column(Text)
    contact_email = Column(String(200))
    user_agent    = Column(String(500))
    created_at    = Column(DateTime, default=datetime.utcnow)


# ── Engine (lazy init) ─────────────────────────────────────────────────────────

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        import pathlib
        pathlib.Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{_DB_PATH}",
            connect_args={"check_same_thread": False},
        )
        _Base.metadata.create_all(_engine)
    return _engine


# ── JWT helpers ────────────────────────────────────────────────────────────────

def _jwt_payload(request: Request) -> dict:
    try:
        from jose import jwt, JWTError
        token = request.cookies.get("demo_token")
        if not token:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:]
        if token:
            return jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
    except Exception:
        pass
    return {}


def _extract_user_id(request: Request) -> Optional[str]:
    return _jwt_payload(request).get("sub")


def _is_admin(request: Request) -> bool:
    return _jwt_payload(request).get("role") == "admin"


# ── Request model ──────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    session_id:    str
    section:       str
    star_rating:   Optional[int] = None
    comment:       Optional[str] = None
    contact_email: Optional[str] = None


# ── Routes ─────────────────────────────────────────────────────────────────────

router = APIRouter(tags=["demo-feedback"])


@router.post("/api/demo-feedback", summary="Submit demo experience feedback")
def submit_feedback(req: FeedbackRequest, request: Request):
    record = DemoFeedback(
        id=str(uuid.uuid4()),
        session_id=req.session_id,
        user_id=_extract_user_id(request),
        section=req.section,
        star_rating=req.star_rating,
        comment=req.comment,
        contact_email=req.contact_email,
        user_agent=request.headers.get("User-Agent", "")[:500],
        created_at=datetime.utcnow(),
    )
    with Session(_get_engine()) as db:
        db.add(record)
        db.commit()
    return {"status": "ok"}


@router.get("/api/demo-feedback", summary="Retrieve all demo feedback (admin only)")
def get_feedback(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="Admin access required")
    with Session(_get_engine()) as db:
        rows = db.query(DemoFeedback).order_by(DemoFeedback.created_at.desc()).all()
        return [
            {
                "id":            r.id,
                "session_id":    r.session_id,
                "user_id":       r.user_id,
                "section":       r.section,
                "star_rating":   r.star_rating,
                "comment":       r.comment,
                "contact_email": r.contact_email,
                "user_agent":    r.user_agent,
                "created_at":    r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
