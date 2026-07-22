"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo-mode configuration — reads all settings from environment variables.
Import this module anywhere that needs DEMO_MODE or auth config.
"""

import os

# ── Core flag ──────────────────────────────────────────────────────────────────

DEMO_MODE: bool = os.environ.get("DEMO_MODE", "false").lower() in ("true", "1", "yes")

# Auth model: Quickstart resolves Egeria credentials from the connection form
# (local) or the selected demo persona (demo) — NOT from a server-managed
# Egeria JWT.  Freshstart sets this True.  Used by shared handlers to decide
# whether to use the logged-in user's Egeria bearer token.
SERVER_MANAGED_AUTH: bool = os.environ.get("SERVER_MANAGED_AUTH", "false").lower() in ("true", "1", "yes")

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

SITE_URL: str = os.environ.get("SITE_URL", "http://localhost:8885").rstrip("/")
COOKIE_SECURE: bool = SITE_URL.startswith("https://")

# ── Portal tile config ─────────────────────────────────────────────────────────
# Obsidian vault URL (vault name or full obsidian:// URI) — set in .env or yaml.
# OBSIDIAN_GITHUB_URL defaults to the coco-workbooks repo so the GitHub button
# is always available without any configuration.

OBSIDIAN_VAULT_URL:   str = os.environ.get("OBSIDIAN_VAULT_URL",   "")
OBSIDIAN_GITHUB_URL:  str = os.environ.get("OBSIDIAN_GITHUB_URL",  "https://github.com/odpi/egeria-workspaces/tree/main/coco-workbooks")

# URL of the Egeria Advisor service. Set in .env or yaml (default: localhost:8880).
# Checked server-side at startup to set advisor_running in portal-config.
# This is ALSO the literal URL sent to browsers (advisor_url / advisor_sso_url in
# pyegeria_handler.py / advisor_lock_handler.py) — it must be an address real
# users can resolve (e.g. the public domain), not a Docker-internal one like
# host.docker.internal, or external users get sent to an address only this
# container can reach. See advisor_check_urls() below for the internal-only
# fallback used just for the server-side reachability check.
EGERIA_ADVISOR_URL:   str = os.environ.get("EGERIA_ADVISOR_URL",   "http://localhost:8880/")


def advisor_check_urls() -> list:
    """URLs to try, in order, when checking if Advisor is reachable from inside
    this container. Always includes EGERIA_ADVISOR_URL itself (the public/real
    value), plus a host.docker.internal variant as a fallback — Advisor runs
    directly on the host, not in this compose network, and a public hostname
    routing back to this same machine may hit hairpin-NAT issues or simply not
    be port-forwarded (during setup) even though it works for real external
    users. Swapping just the hostname keeps EGERIA_ADVISOR_URL itself unchanged
    for anything sent to a browser.
    """
    if not EGERIA_ADVISOR_URL:
        return []
    from urllib.parse import urlsplit, urlunsplit
    parts = urlsplit(EGERIA_ADVISOR_URL)
    if parts.hostname in (None, "host.docker.internal"):
        return [EGERIA_ADVISOR_URL]
    port = f":{parts.port}" if parts.port else ""
    userinfo = f"{parts.username}{':' + parts.password if parts.password else ''}@" if parts.username else ""
    fallback_netloc = f"{userinfo}host.docker.internal{port}"
    fallback = urlunsplit((parts.scheme, fallback_netloc, parts.path, parts.query, parts.fragment))
    return [EGERIA_ADVISOR_URL, fallback]

# Shared HS256 secret with Egeria Advisor's own ADVISOR_PORTAL_SECRET — used to
# mint the short-lived SSO handoff token in advisor_lock_handler.py. Must match
# exactly; do not confuse with JWT_SECRET above (that signs the Portal's own
# demo_token cookie and is unrelated). Left empty, the Advisor tile's acquire
# call returns 503 rather than minting with an insecure/mismatched key.
EGERIA_ADVISOR_SSO_SECRET: str = os.environ.get("EGERIA_ADVISOR_SSO_SECRET", "")
