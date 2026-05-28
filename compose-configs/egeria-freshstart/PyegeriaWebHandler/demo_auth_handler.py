"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Freshstart Auth — FastAPI router.

Authentication is backed entirely by Egeria — no SQLite, no registration flow.
The portal issues a JWT session cookie after successful Egeria authentication.

Routes:
  POST /api/auth/login            — authenticate against Egeria; set JWT cookie
  POST /api/auth/change-password  — forced first-login password change
  POST /api/auth/logout           — clear session cookie
  GET  /api/auth/me               — current user from JWT

  GET    /api/admin/roles                                   (admin)
  GET    /api/admin/groups                                  (admin)
  GET    /api/admin/egeria-users                            (admin — ActorManager find_user_identities)
  POST   /api/admin/egeria-users                            (admin — SecurityOfficer set_user_account)
  PUT    /api/admin/egeria-users/{user_id}                  (admin — SecurityOfficer set_user_account)
  POST   /api/admin/egeria-users/{user_id}/disable          (admin — SecurityOfficer set_user_account)
  POST   /api/admin/egeria-users/{user_id}/reset-password   (admin — SecurityOfficer set_user_account)
  DELETE /api/admin/egeria-users/{user_id}                  (admin — SecurityOfficer delete_user_account)

  GET  /api/platform/org-name     — organisation name from application.properties
  GET  /api/my-profile            — get logged-in user's Egeria profile
  POST /api/my-profile            — create/update logged-in user's Egeria profile
  GET  /api/demo/config           — runtime config key/value store (admin)
  POST /api/demo/config           — update runtime config (admin)
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import httpx
import yaml
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from loguru import logger
from pydantic import BaseModel

from demo_config import (
    DEMO_MODE,
    EGERIA_ADMIN_CALLER_ID,
    EGERIA_ADMIN_CALLER_PASSWORD,
    EGERIA_ADMIN_USERS,
    EGERIA_PLATFORM_NAME,
    EGERIA_PLATFORM_URL,
    EGERIA_USER_SECRETS_PATH,
    EGERIA_VIEW_SERVER,
    JWT_ALGORITHM,
    JWT_EXPIRY_ADMIN_SEC,
    JWT_EXPIRY_USER_SEC,
    JWT_SECRET,
)

router = APIRouter(tags=["demo"])

_CONFIG_PATH = Path(os.environ.get("DEMO_DB_PATH", "/app/demo-data/demo.db")).with_name("config.json")

# ── Platform GUID cache ────────────────────────────────────────────────────────
# SecurityOfficer user-account paths require the GUID of the Egeria platform
# element, looked up once via classification-explorer and then cached.

_platform_guid_cache: Optional[str] = None
_platform_guid_lock = asyncio.Lock()

_HUMAN_TYPES = frozenset({"EMPLOYEE", "EXTERNAL", "CONTRACTOR"})

# ── YAML user-directory helpers ────────────────────────────────────────────────
# The omsecrets file is mounted read-write into the container.  We mirror every
# SecurityOfficer mutation here so the admin list is immediately accurate.
# (Egeria's OMRS sync from SecurityOfficer runs hourly; YAML is always current.)

_SECRETS_PATH = Path(EGERIA_USER_SECRETS_PATH)
_SECRETS_FILE_LOCK = asyncio.Lock()

# ── Admin Egeria token ─────────────────────────────────────────────────────────
# SecurityOfficer and ClassificationExplorer calls need a valid Egeria bearer
# token. Rather than reusing the portal JWT's stored token (which can expire
# before the 7-day admin portal JWT does), we maintain a separately refreshed
# token using the configured admin service account credentials.

_admin_token_cache: Optional[tuple[str, datetime]] = None
_admin_token_lock = asyncio.Lock()


async def _get_admin_egeria_token() -> str:
    """Return a cached Egeria bearer token for admin/SecurityOfficer operations.

    Refreshes automatically every 20 minutes so it stays valid regardless of
    the portal JWT lifetime.
    """
    global _admin_token_cache
    now = datetime.utcnow()
    if _admin_token_cache:
        token, expires_at = _admin_token_cache
        if now < expires_at:
            return token
    async with _admin_token_lock:
        if _admin_token_cache:
            token, expires_at = _admin_token_cache
            if now < expires_at:
                return token
        status, text = await _egeria_token_call(EGERIA_ADMIN_CALLER_ID, EGERIA_ADMIN_CALLER_PASSWORD)
        if status != 200 or not text.strip() or text.strip().startswith("{"):
            logger.error(
                f"Failed to obtain admin Egeria token for '{EGERIA_ADMIN_CALLER_ID}': "
                f"HTTP {status} — check EGERIA_ADMIN_CALLER_ID/PASSWORD in .env"
            )
            raise HTTPException(
                status_code=502,
                detail="Egeria admin token unavailable — check EGERIA_ADMIN_CALLER_ID/PASSWORD in .env",
            )
        token = text.strip()
        _admin_token_cache = (token, now + timedelta(minutes=20))
        logger.debug(f"Refreshed Egeria admin token for '{EGERIA_ADMIN_CALLER_ID}'")
        return token


def _read_omsecrets() -> dict:
    return yaml.safe_load(_SECRETS_PATH.read_text())


def _write_omsecrets(data: dict) -> None:
    _SECRETS_PATH.write_text(
        yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    )


def _secrets_users(data: dict) -> dict:
    """Return the mutable users dict from secretsCollections.userDirectory."""
    return data["secretsCollections"]["userDirectory"]["users"]


def _secrets_named_lists(data: dict) -> dict:
    """Return the namedLists dict from secretsCollections.userDirectory."""
    return data.get("secretsCollections", {}).get("userDirectory", {}).get("namedLists", {})


async def _get_platform_guid() -> str:
    """Return (and cache) the GUID of the Egeria platform element."""
    global _platform_guid_cache
    if _platform_guid_cache:
        return _platform_guid_cache
    async with _platform_guid_lock:
        if _platform_guid_cache:
            return _platform_guid_cache
        egeria_token = await _get_admin_egeria_token()
        url = (
            f"{EGERIA_PLATFORM_URL}/servers/{EGERIA_VIEW_SERVER}"
            "/api/open-metadata/classification-explorer/elements/by-exact-property-value"
        )
        body = {
            "class": "FindPropertyNamesProperties",
            "propertyValue": EGERIA_PLATFORM_NAME,
            "propertyNames": ["displayName", "qualifiedName", "resourceName"],
        }
        async with httpx.AsyncClient(verify=False) as client:
            r = await client.post(url, json=body, headers=_egeria_headers(egeria_token), timeout=15)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Platform GUID lookup failed: HTTP {r.status_code}")
        elements = r.json().get("elements", [])
        if not elements:
            raise HTTPException(
                status_code=502,
                detail=f"Platform element '{EGERIA_PLATFORM_NAME}' not found in metadata store",
            )
        guid = elements[0]["elementHeader"]["guid"]
        _platform_guid_cache = guid
        logger.info(f"Cached platform GUID for '{EGERIA_PLATFORM_NAME}': {guid}")
        return guid


# application.properties is mounted at this path if the yaml volume is added.
_APP_PROPS_PATH = Path(os.environ.get("APPLICATION_PROPERTIES_PATH", "/app/application.properties"))


# ── Config store (JSON file) ───────────────────────────────────────────────────

def _read_config() -> dict:
    try:
        if _CONFIG_PATH.exists():
            return json.loads(_CONFIG_PATH.read_text())
    except Exception:
        pass
    return {}


def _write_config(cfg: dict) -> None:
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


# ── JWT helpers ────────────────────────────────────────────────────────────────

def _make_jwt(user_id: str, role: str, display_name: str, egeria_token: str) -> str:
    exp = JWT_EXPIRY_ADMIN_SEC if role == "admin" else JWT_EXPIRY_USER_SEC
    return jwt.encode(
        {
            "sub": user_id,
            "role": role,
            "display_name": display_name,
            "egeria_token": egeria_token,
            "exp": datetime.utcnow() + timedelta(seconds=exp),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def _portal_token_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get("demo_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    return token or None


class CurrentUser:
    def __init__(self, user_id: str, role: str, display_name: str, egeria_token: str):
        self.user_id = user_id
        self.role = role
        self.display_name = display_name
        self.egeria_token = egeria_token


def get_current_user(request: Request) -> Optional[CurrentUser]:
    token = _portal_token_from_request(request)
    if not token:
        return None
    try:
        payload = _decode_jwt(token)
        return CurrentUser(
            user_id=payload["sub"],
            role=payload.get("role", "user"),
            display_name=payload.get("display_name", payload["sub"]),
            egeria_token=payload.get("egeria_token", ""),
        )
    except JWTError:
        return None


def require_user(request: Request) -> CurrentUser:
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def require_admin(request: Request) -> CurrentUser:
    user = require_user(request)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ── Egeria REST helpers ────────────────────────────────────────────────────────

async def _egeria_token_call(
    user_id: str,
    password: str,
    new_password: Optional[str] = None,
) -> tuple[int, str]:
    """POST {EGERIA_PLATFORM_URL}/api/token and return (status_code, body_text)."""
    body: dict = {"userId": user_id, "password": password}
    if new_password:
        body["newPassword"] = new_password
    async with httpx.AsyncClient(verify=False) as client:
        try:
            r = await client.post(f"{EGERIA_PLATFORM_URL}/api/token", json=body, timeout=15)
            return r.status_code, r.text
        except httpx.HTTPError as exc:
            logger.error(f"Egeria /api/token unreachable: {exc}")
            return 503, str(exc)


def _egeria_headers(egeria_token: str) -> dict:
    return {
        "Authorization": f"Bearer {egeria_token}",
        "Content-Type": "application/json",
    }


async def _egeria_post(path: str, body: dict, egeria_token: str) -> httpx.Response:
    url = f"{EGERIA_PLATFORM_URL}/servers/{EGERIA_VIEW_SERVER}{path}"
    async with httpx.AsyncClient(verify=False) as client:
        return await client.post(url, json=body, headers=_egeria_headers(egeria_token), timeout=30)


async def _egeria_get(path: str, egeria_token: str) -> httpx.Response:
    url = f"{EGERIA_PLATFORM_URL}/servers/{EGERIA_VIEW_SERVER}{path}"
    async with httpx.AsyncClient(verify=False) as client:
        return await client.get(url, headers=_egeria_headers(egeria_token), timeout=30)


# ── Pydantic models ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    user_id: str
    password: str


class ChangePasswordRequest(BaseModel):
    user_id: str
    password: str
    new_password: str


class CreateUserRequest(BaseModel):
    userId: str
    userName: Optional[str] = None
    userAccountType: str = "EMPLOYEE"
    givenName: Optional[str] = None
    surname: Optional[str] = None
    securityRoles: list[str] = []
    securityGroups: list[str] = []
    defaultZones: list[str] = []
    publishZones: list[str] = []
    clearPassword: str


class UpdateUserRequest(BaseModel):
    userName: Optional[str] = None
    securityRoles: Optional[list[str]] = None
    securityGroups: Optional[list[str]] = None
    defaultZones: Optional[list[str]] = None
    publishZones: Optional[list[str]] = None


class ResetPasswordRequest(BaseModel):
    clearPassword: str


class ConfigUpdateRequest(BaseModel):
    key: str
    value: str


# ── Login / logout ─────────────────────────────────────────────────────────────

@router.post("/api/auth/login")
async def login(req: LoginRequest, response: Response):
    status, text = await _egeria_token_call(req.user_id, req.password)

    if "CREDENTIALS_EXPIRED" in text:
        return JSONResponse(
            status_code=403,
            content={"credentials_expired": True, "user_id": req.user_id},
        )

    if status != 200 or not text.strip() or text.strip().startswith("{"):
        logger.warning(f"Login failed for {req.user_id!r}: HTTP {status}")
        raise HTTPException(status_code=401, detail="Invalid user ID or password")

    egeria_token = text.strip()
    role = "admin" if req.user_id in EGERIA_ADMIN_USERS else "user"
    portal_token = _make_jwt(req.user_id, role, req.user_id, egeria_token)
    exp = JWT_EXPIRY_ADMIN_SEC if role == "admin" else JWT_EXPIRY_USER_SEC
    response.set_cookie("demo_token", portal_token, httponly=True, samesite="lax", max_age=exp)
    return {"message": "Login successful", "role": role, "display_name": req.user_id}


@router.post("/api/auth/change-password")
async def change_password(req: ChangePasswordRequest, response: Response):
    """First-login forced password change — validates old creds and sets new password."""
    status, text = await _egeria_token_call(req.user_id, req.password, req.new_password)

    if status != 200 or not text.strip() or text.strip().startswith("{"):
        logger.warning(f"Password change failed for {req.user_id!r}: HTTP {status}: {text[:200]}")
        raise HTTPException(status_code=401, detail="Invalid credentials or password change failed")

    egeria_token = text.strip()
    role = "admin" if req.user_id in EGERIA_ADMIN_USERS else "user"
    portal_token = _make_jwt(req.user_id, role, req.user_id, egeria_token)
    exp = JWT_EXPIRY_ADMIN_SEC if role == "admin" else JWT_EXPIRY_USER_SEC
    response.set_cookie("demo_token", portal_token, httponly=True, samesite="lax", max_age=exp)
    return {"message": "Password changed successfully", "role": role}


@router.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie("demo_token")
    return {"message": "Logged out"}


@router.get("/api/auth/me")
def get_me(request: Request):
    user = get_current_user(request)
    if not user:
        return JSONResponse({"authenticated": False, "demo_mode": DEMO_MODE})
    return {
        "authenticated": True,
        "demo_mode": DEMO_MODE,
        "user_id": user.user_id,
        "display_name": user.display_name,
        "role": user.role,
    }


# ── Platform info ──────────────────────────────────────────────────────────────

@router.get("/api/platform/org-name")
def get_org_name():
    """Return the organisation name from application.properties or EGERIA_ORG_NAME env var."""
    try:
        if _APP_PROPS_PATH.exists():
            for line in _APP_PROPS_PATH.read_text().splitlines():
                line = line.strip()
                if line.startswith("platform.organization.name"):
                    _, _, value = line.partition("=")
                    name = value.strip()
                    if name:
                        return {"name": name}
    except Exception as exc:
        logger.warning(f"Could not read application.properties: {exc}")
    return {"name": os.environ.get("EGERIA_ORG_NAME", "Egeria")}


# ── Admin — Egeria roles and groups ────────────────────────────────────────────

def _extract_collection_elements(data: dict) -> list[dict]:
    elements = data.get("elements", data.get("elementList", []))
    result = []
    for e in (elements or []):
        result.append({
            "guid": e.get("elementHeader", {}).get("guid", ""),
            "qualifiedName": e.get("properties", {}).get("qualifiedName", ""),
            "displayName": e.get("properties", {}).get("displayName", ""),
        })
    return result


async def _list_elements_by_type(type_name: str) -> list[dict]:
    """Search for all metadata elements of the given type via classification-explorer."""
    egeria_token = await _get_admin_egeria_token()
    body = {
        "class": "FindPropertyNamesProperties",
        "metadataElementTypeName": type_name,
        "propertyValue": "",
        "propertyNames": ["qualifiedName", "displayName"],
    }
    r = await _egeria_post(
        "/api/open-metadata/classification-explorer/elements/by-property-value-search"
        "?startsWith=false&endsWith=false&ignoreCase=true",
        body,
        egeria_token,
    )
    if r.status_code != 200:
        logger.warning(f"list {type_name}: HTTP {r.status_code}: {r.text[:200]}")
        return []
    return _extract_collection_elements(r.json())


@router.get("/api/admin/roles")
async def list_roles(admin: CurrentUser = Depends(require_admin)):
    """List SecurityRole entries from the omsecrets namedLists."""
    if not _SECRETS_PATH.exists():
        return []
    named = _secrets_named_lists(_read_omsecrets())
    return [
        {"qualifiedName": key, "displayName": (entry or {}).get("displayName", key)}
        for key, entry in named.items()
        if (entry or {}).get("listTypeName") == "SecurityRole"
    ]


@router.get("/api/admin/groups")
async def list_groups(admin: CurrentUser = Depends(require_admin)):
    """List SecurityGroup entries from the omsecrets namedLists."""
    if not _SECRETS_PATH.exists():
        return []
    named = _secrets_named_lists(_read_omsecrets())
    return [
        {"qualifiedName": key, "displayName": (entry or {}).get("displayName", key)}
        for key, entry in named.items()
        if (entry or {}).get("listTypeName") == "SecurityGroup"
    ]


# ── Admin — Egeria user accounts ───────────────────────────────────────────────
#
# Listing reads egeria-user-directory.omsecrets directly (always current).
# Mutations go through SecurityOfficer REST (immediate in-memory auth effect)
# AND mirror the change to the omsecrets YAML so the list is instantly accurate.
#
# Background: Egeria's OMRS sync of SecurityOfficer accounts runs hourly, so
# ActorManager find_user_identities won't reflect new users until then.
# TODO: switch listing to the new SecurityOfficer list API once available.

_SECURITY_OFFICER_BASE = (
    f"{EGERIA_PLATFORM_URL}/servers/{EGERIA_VIEW_SERVER}"
    "/api/open-metadata/security-officer"
)


def _build_user_account_body(req: CreateUserRequest) -> dict:
    other: dict = {}
    if req.defaultZones:
        other["defaultZones"] = ",".join(req.defaultZones)
    if req.publishZones:
        other["publishZones"] = ",".join(req.publishZones)
    return {
        "class": "UserAccountRequestBody",
        "userAccount": {
            "class": "OpenMetadataUserAccount",
            "userId": req.userId,
            "userName": req.userName or req.userId,
            "userAccountType": req.userAccountType,
            "givenName": req.givenName or "",
            "surname": req.surname or "",
            "securityRoles": req.securityRoles,
            "securityGroups": req.securityGroups,
            "otherProperties": other,
            "userAccountStatus": "CREDENTIALS_EXPIRED",
            "secrets": {"clearPassword": req.clearPassword},
        },
    }


@router.get("/api/admin/egeria-users")
async def list_egeria_users(admin: CurrentUser = Depends(require_admin)):
    """List human user accounts from omsecrets YAML (always current)."""
    if not _SECRETS_PATH.exists():
        logger.warning(f"omsecrets not found at {_SECRETS_PATH}")
        return []
    data = _read_omsecrets()
    users = _secrets_users(data)
    return [
        {
            "userId": uid,
            "userName": (entry or {}).get("userName", uid) or uid,
            "userAccountStatus": (entry or {}).get("userAccountStatus", "AVAILABLE"),
            "userAccountType": (entry or {}).get("userAccountType", "EMPLOYEE"),
        }
        for uid, entry in users.items()
        if (entry or {}).get("userAccountType", "DIGITAL") in _HUMAN_TYPES
    ]


@router.post("/api/admin/egeria-users")
async def create_egeria_user(req: CreateUserRequest, admin: CurrentUser = Depends(require_admin)):
    # SecurityOfficer: immediate in-memory effect (user can log in right away)
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts",
            json=_build_user_account_body(req),
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    # Mirror to YAML so the admin list shows the user immediately
    if _SECRETS_PATH.exists():
        async with _SECRETS_FILE_LOCK:
            data = _read_omsecrets()
            users = _secrets_users(data)
            users[req.userId] = {
                "userAccountStatus": "CREDENTIALS_EXPIRED",
                "userAccountType": req.userAccountType,
                "userName": req.userName or req.userId,
                "secrets": {"clearPassword": req.clearPassword},
            }
            _write_omsecrets(data)
    return {"userId": req.userId, "status": "created"}


@router.get("/api/admin/egeria-users/{target_id}")
async def get_egeria_user(target_id: str, admin: CurrentUser = Depends(require_admin)):
    """Return full account details for a single user (for populating the admin edit modal)."""
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.get(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts/{target_id}",
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail=f"User {target_id!r} not found in Egeria")
    user_account = r.json().get("userAccount") or {}
    other = user_account.get("otherProperties") or {}
    return {
        "userId":            target_id,
        "userName":          user_account.get("userName", target_id),
        "userAccountStatus": user_account.get("userAccountStatus", ""),
        "userAccountType":   user_account.get("userAccountType", "EMPLOYEE"),
        "securityRoles":     user_account.get("securityRoles") or [],
        "securityGroups":    user_account.get("securityGroups") or [],
        "otherProperties": {
            "defaultZones": other.get("defaultZones", ""),
            "publishZones":  other.get("publishZones",  ""),
        },
    }


@router.put("/api/admin/egeria-users/{target_id}")
async def update_egeria_user(
    target_id: str,
    req: UpdateUserRequest,
    admin: CurrentUser = Depends(require_admin),
):
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        get_r = await client.get(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts/{target_id}",
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if get_r.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found in Egeria")
    current = get_r.json().get("userAccount", {})
    if req.userName is not None:
        current["userName"] = req.userName
    if req.securityRoles is not None:
        current["securityRoles"] = req.securityRoles
    if req.securityGroups is not None:
        current["securityGroups"] = req.securityGroups
    other = current.get("otherProperties", {})
    if req.defaultZones is not None:
        other["defaultZones"] = ",".join(req.defaultZones)
    if req.publishZones is not None:
        other["publishZones"] = ",".join(req.publishZones)
    current["otherProperties"] = other
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts",
            json={"class": "UserAccountRequestBody", "userAccount": current},
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    # Mirror display-name change to YAML
    if req.userName is not None and _SECRETS_PATH.exists():
        async with _SECRETS_FILE_LOCK:
            data = _read_omsecrets()
            users = _secrets_users(data)
            if target_id in users:
                (users[target_id] or {})["userName"] = req.userName
                _write_omsecrets(data)
    return {"userId": target_id, "status": "updated"}


@router.post("/api/admin/egeria-users/{target_id}/disable")
async def disable_egeria_user(target_id: str, admin: CurrentUser = Depends(require_admin)):
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        get_r = await client.get(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts/{target_id}",
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if get_r.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found in Egeria")
    current = get_r.json().get("userAccount", {})
    current["userAccountStatus"] = "DISABLED"
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts",
            json={"class": "UserAccountRequestBody", "userAccount": current},
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    if _SECRETS_PATH.exists():
        async with _SECRETS_FILE_LOCK:
            data = _read_omsecrets()
            users = _secrets_users(data)
            if target_id in users and users[target_id]:
                users[target_id]["userAccountStatus"] = "DISABLED"
                _write_omsecrets(data)
    return {"userId": target_id, "status": "disabled"}


@router.post("/api/admin/egeria-users/{target_id}/reset-password")
async def reset_egeria_password(
    target_id: str,
    req: ResetPasswordRequest,
    admin: CurrentUser = Depends(require_admin),
):
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        get_r = await client.get(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts/{target_id}",
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if get_r.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found in Egeria")
    current = get_r.json().get("userAccount", {})
    current["userAccountStatus"] = "CREDENTIALS_EXPIRED"
    current["secrets"] = {"clearPassword": req.clearPassword}
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts",
            json={"class": "UserAccountRequestBody", "userAccount": current},
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    if _SECRETS_PATH.exists():
        async with _SECRETS_FILE_LOCK:
            data = _read_omsecrets()
            users = _secrets_users(data)
            if target_id in users and users[target_id]:
                users[target_id]["userAccountStatus"] = "CREDENTIALS_EXPIRED"
                users[target_id].setdefault("secrets", {})["clearPassword"] = req.clearPassword
                _write_omsecrets(data)
    return {"userId": target_id, "status": "password_reset"}


@router.delete("/api/admin/egeria-users/{target_id}")
async def delete_egeria_user(target_id: str, admin: CurrentUser = Depends(require_admin)):
    if target_id == admin.user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    guid = await _get_platform_guid()
    admin_token = await _get_admin_egeria_token()
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.delete(
            f"{_SECURITY_OFFICER_BASE}/platforms/{guid}/user-accounts/{target_id}",
            headers=_egeria_headers(admin_token),
            timeout=30,
        )
    if r.status_code not in (200, 201, 204):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    if _SECRETS_PATH.exists():
        async with _SECRETS_FILE_LOCK:
            data = _read_omsecrets()
            users = _secrets_users(data)
            users.pop(target_id, None)
            _write_omsecrets(data)
    return {"userId": target_id, "status": "deleted"}


# ── My Profile ────────────────────────────────────────────────────────────────

@router.get("/api/my-profile")
async def get_my_profile(user: CurrentUser = Depends(require_user)):
    """Get the logged-in user's Egeria profile via the my-profile OMVS."""
    r = await _egeria_get(
        "/api/open-metadata/my-profile",
        user.egeria_token,
    )
    if r.status_code == 200:
        data = r.json()
        return data.get("personalProfile", data)
    return {}


@router.post("/api/my-profile")
async def set_my_profile(body: dict, user: CurrentUser = Depends(require_user)):
    """Create or update the logged-in user's Egeria profile."""
    r = await _egeria_post(
        "/api/open-metadata/my-profile",
        body,
        user.egeria_token,
    )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=f"Egeria error: {r.text[:300]}")
    return {"status": "saved"}


# ── Admin — runtime config ─────────────────────────────────────────────────────

@router.get("/api/demo/config")
def admin_get_config(admin: CurrentUser = Depends(require_admin)):
    return _read_config()


@router.post("/api/demo/config")
def admin_set_config(req: ConfigUpdateRequest, admin: CurrentUser = Depends(require_admin)):
    cfg = _read_config()
    cfg[req.key] = req.value
    _write_config(cfg)
    return {"key": req.key, "value": req.value}
