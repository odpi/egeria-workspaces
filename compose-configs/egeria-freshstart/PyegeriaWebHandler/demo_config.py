"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Freshstart demo-mode configuration.
Authentication is backed by Egeria — no SQLite, no email.
"""

import os

# ── Core flag ──────────────────────────────────────────────────────────────────

DEMO_MODE: bool = os.environ.get("DEMO_MODE", "false").lower() in ("true", "1", "yes")

# ── JWT ────────────────────────────────────────────────────────────────────────

JWT_SECRET: str       = os.environ.get("JWT_SECRET", "change-me-before-going-public")
JWT_ALGORITHM: str    = "HS256"
JWT_EXPIRY_USER_SEC: int  = int(os.environ.get("JWT_EXPIRY_USER_SECONDS",  "7200"))    # 2 h
JWT_EXPIRY_ADMIN_SEC: int = int(os.environ.get("JWT_EXPIRY_ADMIN_SECONDS", "604800"))  # 7 d

# ── Egeria ─────────────────────────────────────────────────────────────────────

EGERIA_PLATFORM_URL: str  = os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443").rstrip("/")
EGERIA_VIEW_SERVER: str   = os.environ.get("EGERIA_VIEW_SERVER", "fs-view-server")
# Name registered by the Egeria platform in the metadata store (platform.name in application.properties).
EGERIA_PLATFORM_NAME: str = os.environ.get("EGERIA_PLATFORM_NAME", "OMAG Server Platform")

# User IDs granted admin role in the portal (Egeria handles its own RBAC separately).
# Comma-separated; bootstrap always included.
EGERIA_ADMIN_USERS: set[str] = {
    u.strip()
    for u in os.environ.get("EGERIA_ADMIN_USERS", "bootstrap").split(",")
    if u.strip()
}

# ── URLs ───────────────────────────────────────────────────────────────────────

SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8086").rstrip("/")

# ── User directory ─────────────────────────────────────────────────────────────

EGERIA_USER_SECRETS_PATH: str = os.environ.get("EGERIA_USER_SECRETS_PATH", "/secrets/user-directory.omsecrets")

# ── Admin service account ───────────────────────────────────────────────────────
# Used to obtain a fresh Egeria bearer token for SecurityOfficer and admin API
# calls. The portal admin JWT lasts 7 days but the Egeria bearer token it carries
# expires sooner; this account's credentials are used to re-authenticate as needed.
# Set EGERIA_ADMIN_CALLER_PASSWORD in .env — never in yaml.

EGERIA_ADMIN_CALLER_ID: str       = os.environ.get("EGERIA_ADMIN_CALLER_ID", "bootstrap")
EGERIA_ADMIN_CALLER_PASSWORD: str = os.environ.get("EGERIA_ADMIN_CALLER_PASSWORD", "secret")
