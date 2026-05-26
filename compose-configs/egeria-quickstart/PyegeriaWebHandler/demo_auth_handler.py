"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo Auth — FastAPI router.

Handles user registration, email verification, login, JWT sessions,
password reset, and persona selection for the Egeria Explorer demo.

Routes:
  POST /api/auth/register
  GET  /api/auth/verify/{token}
  POST /api/auth/login
  POST /api/auth/logout
  POST /api/auth/forgot-password
  POST /api/auth/reset-password
  GET  /api/auth/me
  POST /api/demo/select-persona
  GET  /api/demo/personas
  GET  /api/demo/portal-config
  GET  /api/demo/config          (admin only)
  POST /api/demo/config          (admin only)
  GET  /api/demo/users           (admin only)
  POST /api/demo/users/{id}/role (admin only)
  GET  /api/demo/events          (admin only)
"""

import json
import os
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from rate_limiter import limiter
from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError, jwt
from loguru import logger
import httpx
import bcrypt as _bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from demo_config import (
    JWT_ALGORITHM, JWT_EXPIRY_ADMIN_SEC, JWT_EXPIRY_USER_SEC, JWT_SECRET,
    RESEND_API_KEY, RESEND_FROM,
    SITE_URL, SMTP_FROM, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_SSL, SMTP_USER,
    COOKIE_SECURE,
)
from demo_db import Config, Event, User, get_db, get_config, log_event, set_config

router = APIRouter(tags=["demo"])

PERSONAS_FILE = Path(__file__).parent / "personas.json"


# ── Auth helpers ───────────────────────────────────────────────────────────────

def _hash(pw: str) -> str:
    return _bcrypt.hashpw(pw.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def _verify(plain: str, hashed: str) -> bool:
    return _bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def _make_jwt(user_id: str, role: str) -> str:
    exp = JWT_EXPIRY_ADMIN_SEC if role == "admin" else JWT_EXPIRY_USER_SEC
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": datetime.utcnow() + timedelta(seconds=exp)},
        JWT_SECRET, algorithm=JWT_ALGORITHM,
    )


def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def _token_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get("demo_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    return token or None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = _token_from_request(request)
    if not token:
        return None
    try:
        payload = _decode_jwt(token)
        return db.get(User, payload["sub"])
    except JWTError:
        return None


def require_verified_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not user.verified:
        raise HTTPException(status_code=403, detail="Email verification required")
    return user


def require_admin(request: Request, db: Session = Depends(get_db)) -> User:
    user = require_verified_user(request, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ── SMTP ───────────────────────────────────────────────────────────────────────

def _send_email(to: str, subject: str, html: str, text: str = "") -> None:
    # ── Try Resend first ──────────────────────────────────────────────────────
    if RESEND_API_KEY:
        try:
            resp = httpx.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY.strip()}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": RESEND_FROM or SMTP_FROM,
                    "to": to,
                    "subject": subject,
                    "html": html,
                    "text": text or html,
                },
                timeout=10.0,
            )
            if resp.status_code != 200:
                logger.error(f"Resend returned {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            logger.info(f"Email sent via Resend to {to!r}: {subject}")
            return
        except Exception as exc:
            logger.error(f"Resend failed, falling back to SMTP if available: {exc}")

    # ── Fallback to SMTP ──────────────────────────────────────────────────────
    if not SMTP_HOST:
        logger.warning(f"Email skipped — neither Resend nor SMTP configured for {to!r}")
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    if text:
        msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    try:
        if SMTP_SSL:
            ctx = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            ctx = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            ctx.starttls()
        with ctx as smtp:
            if SMTP_USER and SMTP_PASSWORD:
                smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.sendmail(SMTP_FROM, to, msg.as_string())
        logger.info(f"Email sent to {to!r}: {subject}")
    except Exception as exc:
        logger.error(f"Failed to send email to {to!r}: {exc}")


# ── Persona helpers ────────────────────────────────────────────────────────────

def _load_personas() -> dict:
    if PERSONAS_FILE.exists():
        with open(PERSONAS_FILE) as f:
            return json.load(f)
    return {}


# ── Pydantic models ────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    display_name: str
    org: Optional[str] = None
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class PersonaSelectRequest(BaseModel):
    persona: str


class ConfigUpdateRequest(BaseModel):
    key: str
    value: str


class RoleUpdateRequest(BaseModel):
    role: str   # 'user' | 'admin'


# ── Registration & verification ────────────────────────────────────────────────

@router.post("/api/auth/register", summary="Register a new demo account")
@limiter.limit("5/minute")
def register(request: Request, req: RegisterRequest, db: Session = Depends(get_db)):
    if len(req.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if db.query(User).filter(User.email == req.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    token = secrets.token_urlsafe(32)
    user = User(
        display_name=req.display_name.strip(),
        org=req.org.strip() if req.org else None,
        email=req.email.lower(),
        password_hash=_hash(req.password),
        verify_token=token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    verify_url = f"{SITE_URL}/api/auth/verify/{token}"
    _send_email(
        to=user.email,
        subject="Verify your Egeria Demo account",
        html=f"""
        <p>Hi {user.display_name},</p>
        <p>Thanks for registering. Click to verify your email:</p>
        <p><a href="{verify_url}" style="padding:10px 20px;background:#6366f1;
           color:white;text-decoration:none;border-radius:4px;">Verify Email</a></p>
        <p>Link expires in 24 hours.</p>
        """,
        text=f"Verify your Egeria Demo account: {verify_url}",
    )
    log_event(db, user.id, "register", {"email": user.email, "org": user.org})
    return {"message": "Registration successful — check your email to verify your account"}


@router.post("/api/auth/resend-verification", summary="Resend email verification link")
def resend_verification(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or user.verified:
        # Return success regardless to avoid email enumeration
        return {"message": "If that address is registered and unverified, a new link has been sent"}
    token = secrets.token_urlsafe(32)
    user.verify_token = token
    db.commit()
    verify_url = f"{SITE_URL}/api/auth/verify/{token}"
    _send_email(
        to=user.email,
        subject="Verify your Egeria Demo account",
        html=f"""
        <p>Hi {user.display_name},</p>
        <p>Here is a new verification link for your Egeria Demo account:</p>
        <p><a href="{verify_url}" style="padding:10px 20px;background:#6366f1;
           color:white;text-decoration:none;border-radius:4px;">Verify Email</a></p>
        <p>If you did not request this, you can ignore this email.</p>
        """,
        text=f"Verify your Egeria Demo account: {verify_url}",
    )
    log_event(db, user.id, "resend_verification", {"email": user.email})
    return {"message": "If that address is registered and unverified, a new link has been sent"}


@router.get("/api/auth/verify/{token}", summary="Verify email address", include_in_schema=False)
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verify_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification link")
    user.verified = True
    user.verify_token = None
    db.commit()
    log_event(db, user.id, "verify", {})

    demo_token = _make_jwt(user.id, user.role)
    exp = JWT_EXPIRY_ADMIN_SEC if user.role == "admin" else JWT_EXPIRY_USER_SEC
    response = RedirectResponse(url="/egeria-explorer?demo_welcome=1", status_code=302)
    response.set_cookie("demo_token", demo_token, httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=exp)
    return response


# ── Login / logout ─────────────────────────────────────────────────────────────

@router.post("/api/auth/login", summary="Log in and receive a session cookie")
@limiter.limit("10/minute")
def login(request: Request, req: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or not _verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    user.last_login = datetime.utcnow()
    db.commit()
    log_event(db, user.id, "login", {})

    exp = JWT_EXPIRY_ADMIN_SEC if user.role == "admin" else JWT_EXPIRY_USER_SEC
    response.set_cookie("demo_token", _make_jwt(user.id, user.role),
                        httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=exp)
    return {"message": "Login successful", "role": user.role, "display_name": user.display_name}


@router.post("/api/auth/logout", summary="Clear the session cookie")
def logout(response: Response):
    response.delete_cookie("demo_token")
    return {"message": "Logged out"}


@router.get("/api/auth/me", summary="Current user info")
def get_me(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"authenticated": False})
    return {
        "authenticated": True,
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
        "role": user.role,
        "org": user.org,
    }


# ── Password reset ─────────────────────────────────────────────────────────────

@router.post("/api/auth/forgot-password", summary="Request a password-reset email")
@limiter.limit("3/minute")
def forgot_password(request: Request, req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if user and user.verified:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        reset_url = f"{SITE_URL}/reset-password?token={token}"
        _send_email(
            to=user.email,
            subject="Reset your Egeria Demo password",
            html=f'<p><a href="{reset_url}">Reset Password</a> (valid 1 hour)</p>',
            text=f"Reset your password: {reset_url}",
        )
    return {"message": "If that email is registered, you'll receive a reset link shortly"}


@router.post("/api/auth/reset-password", summary="Set a new password using a reset token")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == req.token).first()
    if not user or not user.reset_expires or user.reset_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")
    if len(req.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    user.password_hash = _hash(req.password)
    user.reset_token = None
    user.reset_expires = None
    db.commit()
    return {"message": "Password reset successful — you can now log in"}


# ── Portal config (authenticated) ─────────────────────────────────────────────

@router.get("/api/demo/portal-config", summary="Return portal tile config for authenticated users")
def portal_config(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.verified:
        raise HTTPException(status_code=401, detail="Authentication required")
    raw = get_config("obsidian_vault_url", "")
    if raw and not raw.startswith("obsidian://"):
        # Treat bare value as a vault name → construct the URI
        import urllib.parse
        obsidian_url = "obsidian://open?vault=" + urllib.parse.quote(raw)
    else:
        obsidian_url = raw
    return {"obsidian_vault_url": obsidian_url}


# ── Persona selection ──────────────────────────────────────────────────────────

@router.get("/api/demo/personas", summary="List available Coco personas (public info only)")
def list_personas():
    personas = _load_personas()
    return {pid: {k: v for k, v in p.items() if k != "password"} for pid, p in personas.items()}


@router.post("/api/demo/select-persona", summary="Select a Coco persona for this session")
def select_persona(
    req: PersonaSelectRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or not user.verified:
        raise HTTPException(status_code=401, detail="Authentication required")

    personas = _load_personas()
    persona = personas.get(req.persona)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona {req.persona!r} not found")

    log_event(db, user.id, "persona_select", {"persona": req.persona})

    # Return credentials so the browser CredContext can use them for Egeria API calls.
    # The password is the well-known Coco demo default ("secret") — not a security risk.
    return {
        "persona":      req.persona,
        "display_name": persona.get("display_name", req.persona),
        "coco_title":   persona.get("coco_title", ""),
        "egeria_user":  req.persona,
        "egeria_password": persona["password"],
    }


# ── Admin — config ─────────────────────────────────────────────────────────────

@router.get("/api/demo/config", summary="Get all runtime config (admin only)")
def admin_get_config(user: User = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(Config).all()
    return {row.key: row.value for row in rows}


@router.post("/api/demo/config", summary="Update a runtime config value (admin only)")
def admin_set_config(req: ConfigUpdateRequest, user: User = Depends(require_admin)):
    set_config(req.key, req.value)
    return {"key": req.key, "value": req.value}


# ── Admin — users ──────────────────────────────────────────────────────────────

@router.get("/api/demo/users", summary="List all registered users (admin only)")
def admin_list_users(user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            "id":           u.id,
            "display_name": u.display_name,
            "email":        u.email,
            "org":          u.org,
            "role":         u.role,
            "verified":     u.verified,
            "created_at":   u.created_at.isoformat() if u.created_at else None,
            "last_login":   u.last_login.isoformat() if u.last_login else None,
        }
        for u in users
    ]


@router.post("/api/demo/users/{user_id}/role", summary="Promote or demote a user (admin only)")
def admin_set_role(
    user_id: str,
    req: RoleUpdateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if req.role not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="role must be 'user' or 'admin'")
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.role = req.role
    db.commit()
    return {"id": user_id, "role": req.role}


@router.post("/api/demo/users/{user_id}/disable", summary="Disable a user account (admin only)")
def admin_disable_user(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.verified = False   # blocks login without deleting record
    db.commit()
    return {"id": user_id, "status": "disabled"}


@router.post("/api/demo/users/{user_id}/enable", summary="Re-enable a disabled user account (admin only)")
def admin_enable_user(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.verified = True
    db.commit()
    return {"id": user_id, "status": "enabled"}


@router.post("/api/demo/users/{user_id}/resend-verification", summary="Admin: resend verification email to a user")
def admin_resend_verification(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if target.verified:
        raise HTTPException(status_code=400, detail="User is already verified")
    token = secrets.token_urlsafe(32)
    target.verify_token = token
    db.commit()
    verify_url = f"{SITE_URL}/api/auth/verify/{token}"
    _send_email(
        to=target.email,
        subject="Verify your Egeria Demo account",
        html=f"""
        <p>Hi {target.display_name},</p>
        <p>An administrator has sent you a new verification link:</p>
        <p><a href="{verify_url}" style="padding:10px 20px;background:#6366f1;
           color:white;text-decoration:none;border-radius:4px;">Verify Email</a></p>
        <p>Or copy this link: {verify_url}</p>
        """,
        text=f"Verify your Egeria Demo account: {verify_url}",
    )
    log_event(db, target.id, "admin_resend_verification", {"by": admin.email})
    return {"id": user_id, "status": "verification_sent", "verify_url": verify_url}


@router.delete("/api/demo/users/{user_id}", summary="Permanently delete a user account (admin only)")
def admin_delete_user(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Event).filter(Event.user_id == user_id).delete()
    db.delete(target)
    db.commit()
    return {"id": user_id, "status": "deleted"}


# ── Admin — events ─────────────────────────────────────────────────────────────

@router.get("/api/demo/events", summary="Recent event log (admin only)")
def admin_list_events(
    limit: int = 200,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    events = db.query(Event).order_by(Event.created_at.desc()).limit(limit).all()
    return [
        {
            "id":         e.id,
            "user_id":    e.user_id,
            "event_type": e.event_type,
            "detail":     json.loads(e.detail) if e.detail else {},
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in events
    ]
