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

# ── Egeria metadata store reset ────────────────────────────────────────────────
# Credentials for the egeria database (not coco_pharma) — used to drop and
# recreate the metadata store schema during a demo reset.
EGERIA_CONTAINER_NAME:    str = os.environ.get("EGERIA_CONTAINER_NAME",    "quickstart-egeria-main")
EGERIA_META_DB_NAME:      str = os.environ.get("EGERIA_META_DB_NAME",      "egeria")
EGERIA_META_DB_USER:      str = os.environ.get("EGERIA_META_DB_USER",      "egeria_admin")
EGERIA_META_DB_PASSWORD:  str = os.environ.get("EGERIA_META_DB_PASSWORD",  "admin4egeria")

# ── JWT ────────────────────────────────────────────────────────────────────────

JWT_SECRET: str       = os.environ.get("JWT_SECRET", "change-me-before-going-public")
JWT_ALGORITHM: str    = "HS256"
JWT_EXPIRY_USER_SEC: int  = int(os.environ.get("JWT_EXPIRY_USER_SECONDS",  "7200"))    # 2 h
JWT_EXPIRY_ADMIN_SEC: int = int(os.environ.get("JWT_EXPIRY_ADMIN_SECONDS", "604800"))  # 7 d

# ── Resend (email) ─────────────────────────────────────────────────────────────
# Set RESEND_API_KEY in .env (never in the yaml).
# RESEND_FROM must be an address on a domain you have verified in Resend.

RESEND_API_KEY: str = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM:    str = os.environ.get("RESEND_FROM",    "")

# ── URLs ───────────────────────────────────────────────────────────────────────

SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8085").rstrip("/")
COOKIE_SECURE: bool = SITE_URL.startswith("https://")

# ── Portal tile config ─────────────────────────────────────────────────────────
# Obsidian vault URL (vault name or full obsidian:// URI) — set in .env or yaml.
# OBSIDIAN_GITHUB_URL defaults to the coco-workbooks repo so the GitHub button
# is always available without any configuration.

OBSIDIAN_VAULT_URL:   str = os.environ.get("OBSIDIAN_VAULT_URL",   "")
OBSIDIAN_GITHUB_URL:  str = os.environ.get("OBSIDIAN_GITHUB_URL",  "https://github.com/odpi/egeria-workspaces/tree/main/coco-workbooks")

# URL of the Egeria Advisor service. Set in .env or yaml (default: localhost:8080).
# Checked server-side at startup to set advisor_running in portal-config.
EGERIA_ADVISOR_URL:   str = os.environ.get("EGERIA_ADVISOR_URL",   "http://localhost:8080/")
