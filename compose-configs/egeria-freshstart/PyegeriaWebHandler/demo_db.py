"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo-mode database — SQLite via SQLAlchemy.
Tables live in the `demo_data` file (path from DEMO_DB_PATH env var).
The Egeria metadata store is separate and unaffected.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import Boolean, Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from demo_config import DEMO_DB_PATH

# ── Models ─────────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id            = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    display_name  = Column(String(200), nullable=False)
    org           = Column(String(200))
    email         = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    role          = Column(String(20), default="user")   # 'user' | 'admin'
    verified      = Column(Boolean, default=False)
    verify_token  = Column(String(200))
    reset_token   = Column(String(200))
    reset_expires = Column(DateTime)
    created_at    = Column(DateTime, default=datetime.utcnow)
    last_login    = Column(DateTime)


class Event(Base):
    __tablename__ = "events"

    id         = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = Column(String(36))
    event_type = Column(String(50), nullable=False)
    detail     = Column(Text)          # JSON-encoded dict
    created_at = Column(DateTime, default=datetime.utcnow)


class Config(Base):
    __tablename__ = "config"

    key   = Column(String(100), primary_key=True)
    value = Column(Text)


# ── Engine ─────────────────────────────────────────────────────────────────────

_engine = None

_CONFIG_DEFAULTS = {
    "reset_interval_hours":  "24",
    "directive_cap":         "validate",
    "session_lifetime_user": "7200",
    "session_lifetime_admin":"604800",
    "reset_notify_minutes":  "30",
    "last_reset_at":         "",
    "reset_state":           "ready",   # 'ready' | 'resetting'
}


def get_engine():
    global _engine
    if _engine is None:
        db_path = Path(DEMO_DB_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(_engine)
        _seed_config()
    return _engine


def _seed_config() -> None:
    with Session(get_engine()) as session:
        for key, value in _CONFIG_DEFAULTS.items():
            if not session.get(Config, key):
                session.add(Config(key=key, value=value))
        session.commit()


# ── Dependency ─────────────────────────────────────────────────────────────────

def get_db() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session


# ── Config helpers ─────────────────────────────────────────────────────────────

def get_config(key: str, default: str = "") -> str:
    with Session(get_engine()) as session:
        row = session.get(Config, key)
        return row.value if row else default


def set_config(key: str, value: str) -> None:
    with Session(get_engine()) as session:
        row = session.get(Config, key)
        if row:
            row.value = value
        else:
            session.add(Config(key=key, value=value))
        session.commit()


# ── Admin bootstrap ────────────────────────────────────────────────────────────

def bootstrap_admin() -> None:
    """Create an admin account from ADMIN_BOOTSTRAP_EMAIL/PASSWORD env vars if no admin exists."""
    email    = os.environ.get("ADMIN_BOOTSTRAP_EMAIL", "").strip()
    password = os.environ.get("ADMIN_BOOTSTRAP_PASSWORD", "").strip()
    if not email or not password:
        return
    import bcrypt as _bcrypt
    with Session(get_engine()) as db:
        if db.query(User).filter_by(role="admin").first():
            return  # at least one admin already exists
        user = User(
            id=str(uuid.uuid4()),
            display_name="Admin",
            email=email,
            password_hash=_bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8"),
            role="admin",
            verified=True,
            created_at=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        print(f"[demo] Bootstrap admin created: {email}", flush=True)


# ── Event helper ───────────────────────────────────────────────────────────────

def log_event(db: Session, user_id: Optional[str], event_type: str, detail: Optional[dict] = None) -> None:
    event = Event(
        user_id=user_id,
        event_type=event_type,
        detail=json.dumps(detail or {}),
    )
    db.add(event)
    db.commit()
