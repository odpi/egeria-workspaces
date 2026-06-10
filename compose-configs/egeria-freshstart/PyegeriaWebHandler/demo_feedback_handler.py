"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

User Feedback handler — captures per-page tool feedback in the shared
Postgres `demo.feedback` table (coco_pharma DB, port 5442).

FB-5  Storage: Postgres instead of SQLite; schema demo.feedback.
FB-6  User identity: JWT sub (demo/freshstart) or anonymous (local).
FB-7  Full capture schema per spec.
FB-8  Admin list + triage endpoints.

POST  /api/demo-feedback           — submit feedback (any visitor)
GET   /api/demo-feedback           — list records, newest first (admin only)
GET   /api/demo-feedback/stats     — summary counts (admin only)
PATCH /api/demo-feedback/{id}      — update triage_status (admin only)
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text,
    create_engine, event, text,
)
from sqlalchemy.orm import DeclarativeBase, Session

from demo_config import DEMO_DB_URL, SERVER_MANAGED_AUTH, DEMO_MODE

# ── Schema / table ─────────────────────────────────────────────────────────────

_SCHEMA = "demo"
_JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-before-going-public")


class _Base(DeclarativeBase):
    pass


class UserFeedback(_Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": _SCHEMA}

    id                  = Column(String(36),  primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id          = Column(String(36),  nullable=True)
    user_id             = Column(String(200), nullable=True)   # FB-6: env-specific
    env                 = Column(String(40),  nullable=True)   # quickstart-demo | quickstart-local | freshstart
    persona             = Column(String(100), nullable=True)   # active Coco persona display name
    page                = Column(String(200), nullable=True)   # tool section / route
    element_guid        = Column(String(36),  nullable=True)   # Egeria element in view, if any
    rating              = Column(Integer,     nullable=True)   # 1–5 stars
    category            = Column(String(40),  nullable=True)   # bug | confusing | suggestion | praise
    message             = Column(Text,        nullable=True)   # free-text
    email               = Column(String(200), nullable=True)   # for follow-up
    wants_response      = Column(Boolean,     nullable=True, default=False)
    consent_to_contact  = Column(Boolean,     nullable=True, default=False)
    build_version       = Column(String(80),  nullable=True)
    user_agent          = Column(String(500), nullable=True)
    viewport            = Column(String(20),  nullable=True)   # e.g. 1920x1080
    locale              = Column(String(20),  nullable=True)
    triage_status       = Column(String(20),  nullable=True, default="new")  # new | triaged | actioned
    created_at          = Column(DateTime,    default=lambda: datetime.now(timezone.utc))


# ── Engine (lazy, with schema creation) ───────────────────────────────────────

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DEMO_DB_URL, pool_pre_ping=True)
        with _engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {_SCHEMA}"))
            conn.commit()
        _Base.metadata.create_all(_engine)
    return _engine


# ── Auth helpers ───────────────────────────────────────────────────────────────

def _jwt_payload(request: Request) -> dict:
    try:
        from jose import jwt
        token = request.cookies.get("demo_token") or request.cookies.get("fs_token")
        if not token:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:]
        if token:
            return jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
    except Exception:
        pass
    return {}


def _resolve_user_id(request: Request, req_email: Optional[str]) -> Optional[str]:
    """FB-6: env-specific user identity."""
    payload = _jwt_payload(request)
    sub = payload.get("sub")
    if sub:
        return sub
    # Local quickstart — no JWT; use the email supplied in the form
    return req_email or None


def _resolve_env() -> str:
    if DEMO_MODE:
        return "quickstart-demo"
    if SERVER_MANAGED_AUTH:
        return "freshstart"
    return "quickstart-local"


def _is_admin(request: Request) -> bool:
    # Local quickstart has no auth at all — admin page is served without a gate
    if not DEMO_MODE and not SERVER_MANAGED_AUTH:
        return True
    payload = _jwt_payload(request)
    if payload.get("role") == "admin":
        return True
    # Freshstart: check EGERIA_ADMIN_USERS set
    try:
        from demo_config import EGERIA_ADMIN_USERS
        return payload.get("sub") in EGERIA_ADMIN_USERS
    except ImportError:
        return False


# ── Request / response models ─────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    session_id:         Optional[str] = None
    page:               Optional[str] = None
    element_guid:       Optional[str] = None
    rating:             Optional[int] = None
    category:           Optional[str] = None
    message:            Optional[str] = None
    email:              Optional[str] = None
    wants_response:     Optional[bool] = False
    consent_to_contact: Optional[bool] = False
    persona:            Optional[str] = None
    viewport:           Optional[str] = None
    locale:             Optional[str] = None


class TriageRequest(BaseModel):
    triage_status: str   # new | triaged | actioned


# ── Routes ────────────────────────────────────────────────────────────────────

router = APIRouter(tags=["demo-feedback"])


def _row_dict(r: UserFeedback) -> dict:
    return {
        "id":                 r.id,
        "session_id":         r.session_id,
        "user_id":            r.user_id,
        "env":                r.env,
        "persona":            r.persona,
        "page":               r.page,
        "element_guid":       r.element_guid,
        "rating":             r.rating,
        "category":           r.category,
        "message":            r.message,
        "email":              r.email,
        "wants_response":     r.wants_response,
        "consent_to_contact": r.consent_to_contact,
        "build_version":      r.build_version,
        "user_agent":         r.user_agent,
        "viewport":           r.viewport,
        "locale":             r.locale,
        "triage_status":      r.triage_status,
        "created_at":         r.created_at.isoformat() if r.created_at else None,
    }


@router.post("/api/demo-feedback", summary="Submit user feedback")
def submit_feedback(req: FeedbackRequest, request: Request):
    try:
        record = UserFeedback(
            id=str(uuid.uuid4()),
            session_id=req.session_id,
            user_id=_resolve_user_id(request, req.email),
            env=_resolve_env(),
            persona=req.persona,
            page=req.page,
            element_guid=req.element_guid,
            rating=req.rating,
            category=req.category,
            message=req.message,
            email=req.email,
            wants_response=req.wants_response or False,
            consent_to_contact=req.consent_to_contact or False,
            build_version=os.environ.get("BUILD_VERSION", "unknown"),
            user_agent=request.headers.get("User-Agent", "")[:500],
            viewport=req.viewport,
            locale=req.locale,
            triage_status="new",
            created_at=datetime.now(timezone.utc),
        )
        with Session(_get_engine()) as db:
            db.add(record)
            db.commit()
        return {"status": "ok"}
    except Exception as exc:
        logger.exception("submit_feedback failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/demo-feedback", summary="List feedback submissions (admin)")
def get_feedback(
    request: Request,
    triage_status: Optional[str] = None,
    env:           Optional[str] = None,
    limit:         int = 200,
):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        with Session(_get_engine()) as db:
            q = db.query(UserFeedback).order_by(UserFeedback.created_at.desc())
            if triage_status:
                q = q.filter(UserFeedback.triage_status == triage_status)
            if env:
                q = q.filter(UserFeedback.env == env)
            rows = q.limit(limit).all()
            return [_row_dict(r) for r in rows]
    except Exception as exc:
        logger.exception("get_feedback failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/api/demo-feedback/stats", summary="Feedback summary stats (admin)")
def get_feedback_stats(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        from sqlalchemy import func
        with Session(_get_engine()) as db:
            total      = db.query(UserFeedback).count()
            new_count  = db.query(UserFeedback).filter(UserFeedback.triage_status == "new").count()
            wants_resp = db.query(UserFeedback).filter(UserFeedback.wants_response == True).count()
            avg_raw    = db.query(func.avg(UserFeedback.rating)).filter(UserFeedback.rating != None).scalar()
            avg_rating = round(float(avg_raw), 1) if avg_raw is not None else None
            return {"total": total, "new": new_count, "wants_response": wants_resp, "avg_rating": avg_rating}
    except Exception as exc:
        logger.exception("get_feedback_stats failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.patch("/api/demo-feedback/{record_id}", summary="Update triage status (admin)")
def triage_feedback(record_id: str, body: TriageRequest, request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="Admin access required")
    if body.triage_status not in ("new", "triaged", "actioned"):
        raise HTTPException(status_code=400, detail="triage_status must be new | triaged | actioned")
    try:
        with Session(_get_engine()) as db:
            row = db.query(UserFeedback).filter(UserFeedback.id == record_id).first()
            if not row:
                raise HTTPException(status_code=404, detail="Record not found")
            row.triage_status = body.triage_status
            db.commit()
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("triage_feedback failed")
        raise HTTPException(status_code=500, detail=str(exc))
