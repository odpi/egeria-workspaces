"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo-mode configuration — reads all settings from environment variables.
Import this module anywhere that needs DEMO_MODE or auth config.
"""

import os

# ── Core flag ──────────────────────────────────────────────────────────────────

DEMO_MODE: bool = os.environ.get("DEMO_MODE", "false").lower() in ("true", "1", "yes")

# ── Database (PostgreSQL on egeria-shared-postgres:5442, coco_pharma / demo_auth schema) ──

DEMO_DB_HOST:     str = os.environ.get("DEMO_DB_HOST",     "egeria-shared-postgres")
DEMO_DB_PORT:     int = int(os.environ.get("DEMO_DB_PORT", "5442"))
DEMO_DB_NAME:     str = os.environ.get("DEMO_DB_NAME",     "coco_pharma")
DEMO_DB_SCHEMA:   str = os.environ.get("DEMO_DB_SCHEMA",   "demo_auth")
DEMO_DB_USER:     str = os.environ.get("DEMO_DB_USER",     "demo_user")
DEMO_DB_PASSWORD: str = os.environ.get("DEMO_DB_PASSWORD", "demo4egeria")
DEMO_DB_URL:      str = (
    f"postgresql://{DEMO_DB_USER}:{DEMO_DB_PASSWORD}"
    f"@{DEMO_DB_HOST}:{DEMO_DB_PORT}/{DEMO_DB_NAME}"
)

# ── JWT ────────────────────────────────────────────────────────────────────────

JWT_SECRET: str       = os.environ.get("JWT_SECRET", "change-me-before-going-public")
JWT_ALGORITHM: str    = "HS256"
JWT_EXPIRY_USER_SEC: int  = int(os.environ.get("JWT_EXPIRY_USER_SECONDS",  "7200"))    # 2 h
JWT_EXPIRY_ADMIN_SEC: int = int(os.environ.get("JWT_EXPIRY_ADMIN_SECONDS", "604800"))  # 7 d

# ── SMTP ───────────────────────────────────────────────────────────────────────
# SMTP_USER/PASSWORD fall back to the bootstrap admin credentials so you only
# need to set one pair of email credentials in .env.

_bootstrap_email:    str = os.environ.get("ADMIN_BOOTSTRAP_EMAIL",    "")
_bootstrap_password: str = os.environ.get("ADMIN_BOOTSTRAP_PASSWORD", "")

SMTP_HOST:     str  = os.environ.get("SMTP_HOST",     "")
SMTP_PORT:     int  = int(os.environ.get("SMTP_PORT", "587"))
SMTP_SSL:      bool = os.environ.get("SMTP_SSL", "false").lower() in ("true", "1", "yes")
SMTP_USER:     str  = os.environ.get("SMTP_USER",     "") or _bootstrap_email
SMTP_PASSWORD: str  = os.environ.get("SMTP_PASSWORD", "") or _bootstrap_password
SMTP_FROM:     str  = os.environ.get("SMTP_FROM",     "") or SMTP_USER

# ── Resend ─────────────────────────────────────────────────────────────────────

RESEND_API_KEY: str = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM:    str = os.environ.get("RESEND_FROM",    "")

# ── URLs ───────────────────────────────────────────────────────────────────────

SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8085").rstrip("/")
COOKIE_SECURE: bool = SITE_URL.startswith("https://")
