"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Explorer analytics as Portal tiles: a thin HTTP client.

`curation_coverage_tile` is an analytic function (pyegeria's analytic
registry runs it through exec_report_spec) that asks Resource Explorer for the
Analytic Library's curation-coverage tile and returns RE's dict unchanged. The
reshaping lives in trellis (trellis_analytics.portal.curation_coverage_tile);
nothing here computes a number. That keeps the Portal image free of trellis
packages, RE's registry and a pyegeria bump.

RE runs the tile as the viewer, never anonymously. The viewer is the persona
report_viewer.py resolved for this request. For that persona the Portal signs
its usual trellis SSO JWT (trellis_sso.encode_portal_sso_token) and trades it
at RE's `POST /api/auth/portal` for an RE session token. That token is cached
here, server-side only, until shortly before it expires, and re-traded once
on a 401.

Every failure (no viewer, SSO not configured, RE unreachable, RE refusing,
any non-200) comes back as a `not_established` tile carrying the reason, with
no counts at the top level, so a chart can never draw zeros for "could not
look".

RESOURCE_EXPLORER_API_URL is the server-to-server address of RE. It is
separate from EGERIA_RESOURCE_EXPLORER_URL, which is sent to browsers. The
default, http://host.docker.internal:8813, is the RE instance that runs on the
host today. Where a deployed RE should live is still open, so set it per
environment.

`report_specs()` is the tile's FormatSet, loaded through
PYEGERIA_REPORT_SPEC_MODULES (see analytics_registry_handler.py). It also
registers `curation_coverage_tile` in pyegeria's analytic registry as
`re_curation_coverage_tile`, the name the spec uses: a report spec names its
function by registered name, and pyegeria refuses an unregistered dotted path
outside its allowed packages (ISSUE-169/173). The name differs from trellis's
own `curation_coverage_tile` routine so the two never collide if trellis
packages are ever installed here.
"""

import os
import threading
import time
from typing import Optional

import httpx
from loguru import logger

RESOURCE_EXPLORER_API_URL = os.environ.get(
    "RESOURCE_EXPLORER_API_URL", "http://host.docker.internal:8813").rstrip("/")

TILE_LABEL = "Resource Explorer - Curation Coverage"
TILE_FUNCTION = "re_curation_coverage_tile"          # registered name; report specs use this
_TILE_IMPORT_PATH = "re_analytics.curation_coverage_tile"
_ENTITY_TYPES = ("database", "file_system", "document_source")

_EXCHANGE_TIMEOUT_S = 10
_TILE_TIMEOUT_S = 60
_EXPIRY_MARGIN_S = 60
_FALLBACK_TTL_S = 30 * 60   # when RE's token carries no readable exp

_sessions: dict = {}        # (portal user id, persona id) -> (RE access token, expires at epoch s)
_sessions_lock = threading.Lock()


class _Refused(Exception):
    """RE (or the Portal's own setup) refused; the message is the reason shown on the tile."""


def _state_tile(state: str, entity_type: str, slug: str, reason: str) -> dict:
    return {
        "state": state,
        "state_reason": reason,
        "subtitle": state.replace("_", " ") + (f" · {reason}" if reason else ""),
        "provenance": f"from Resource Explorer at {RESOURCE_EXPLORER_API_URL} · curation coverage",
        "summary": "",
        "groups": [],
        "kpis": [],
        "manifest": {"function": TILE_FUNCTION, "scope": f"{entity_type}:{slug}"},
    }


def _egeria_bearer(persona_id: str, password: str) -> str:
    from rest_api_handler import _env_defaults
    url = _env_defaults()["url"].rstrip("/")
    try:
        r = httpx.post(f"{url}/api/token", json={"userId": persona_id, "password": password},
                       verify=False, timeout=_EXCHANGE_TIMEOUT_S)
    except httpx.HTTPError as exc:
        raise _Refused(f"Egeria could not be reached to sign in {persona_id}: {exc}") from exc
    if r.status_code != 200 or not r.text.strip():
        raise _Refused(f"Egeria refused to sign in {persona_id} (HTTP {r.status_code})")
    return r.text.strip()


def _expiry(access_token: str) -> float:
    try:
        from jose import jwt
        exp = jwt.get_unverified_claims(access_token).get("exp")
        if exp:
            return float(exp)
    except Exception:  # noqa: BLE001  an opaque token is fine; fall back to a short TTL
        pass
    return time.time() + _FALLBACK_TTL_S


def _exchange(viewer: dict) -> str:
    from demo_config import EGERIA_ADVISOR_SSO_SECRET
    from trellis_sso import encode_portal_sso_token
    if not EGERIA_ADVISOR_SSO_SECRET:
        raise _Refused("Portal SSO is not configured (EGERIA_ADVISOR_SSO_SECRET is unset)")
    persona_id, persona, user = viewer["persona_id"], viewer["persona"], viewer["user"]
    egeria_token = _egeria_bearer(persona_id, persona["password"])
    portal_token = encode_portal_sso_token(user, persona_id, persona, egeria_token)
    try:
        r = httpx.post(f"{RESOURCE_EXPLORER_API_URL}/api/auth/portal", json={"portal_token": portal_token},
                       timeout=_EXCHANGE_TIMEOUT_S)
    except httpx.HTTPError as exc:
        raise _Refused(f"Resource Explorer is not reachable at {RESOURCE_EXPLORER_API_URL}: {exc}") from exc
    reasons = {
        401: "Resource Explorer refused the Portal sign-in (invalid or expired)",
        403: f"Resource Explorer does not accept {persona_id} for this (it is RE's daemon account)",
        400: "Resource Explorer says the Portal sign-in is missing claims",
        503: "Portal sign-in is not configured on Resource Explorer",
    }
    if r.status_code != 200:
        raise _Refused(reasons.get(r.status_code, f"Resource Explorer sign-in answered HTTP {r.status_code}"))
    token = (r.json() or {}).get("access_token")
    if not token:
        raise _Refused("Resource Explorer's sign-in answer carried no access token")
    key = (getattr(user, "id", None), persona_id)
    with _sessions_lock:
        _sessions[key] = (token, _expiry(token))
    return token


def _session_token(viewer: dict, fresh: bool = False) -> str:
    key = (getattr(viewer["user"], "id", None), viewer["persona_id"])
    if not fresh:
        with _sessions_lock:
            hit = _sessions.get(key)
        if hit and hit[1] - _EXPIRY_MARGIN_S > time.time():
            return hit[0]
    return _exchange(viewer)


def _fetch_tile(entity_type: str, slug: str, token: str) -> httpx.Response:
    url = f"{RESOURCE_EXPLORER_API_URL}/api/analytics/curation-coverage-tile/{entity_type}/{slug}"
    return httpx.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=_TILE_TIMEOUT_S)


def curation_coverage_tile(slug: str, resource_type: str = "database") -> dict:
    """Resource Explorer's curation-coverage tile for one resource, fetched as the viewer."""
    from report_viewer import current_viewer
    entity_type = resource_type
    if entity_type not in _ENTITY_TYPES:
        return _state_tile("not_applicable", entity_type, slug,
                           f"curation coverage is not offered for {entity_type}; it covers {', '.join(_ENTITY_TYPES)}")
    viewer = current_viewer()
    if not viewer or not viewer.get("persona_id"):
        why = (viewer or {}).get("reason") or "the viewer is not known"
        return _state_tile("not_established", entity_type, slug,
                           f"choose a persona to see this ({why})")
    try:
        r = _fetch_tile(entity_type, slug, _session_token(viewer))
        if r.status_code == 401:
            r = _fetch_tile(entity_type, slug, _session_token(viewer, fresh=True))
    except _Refused as exc:
        return _state_tile("not_established", entity_type, slug, str(exc))
    except httpx.HTTPError as exc:
        return _state_tile("not_established", entity_type, slug,
                           f"Resource Explorer is not reachable at {RESOURCE_EXPLORER_API_URL}: {exc}")
    if r.status_code != 200:
        logger.warning(f"re_analytics: curation-coverage-tile {entity_type}/{slug} answered HTTP {r.status_code}")
        return _state_tile("not_established", entity_type, slug,
                           f"Resource Explorer answered HTTP {r.status_code}")
    try:
        return r.json()
    except ValueError:
        return _state_tile("not_established", entity_type, slug, "Resource Explorer's answer was not JSON")


def register_tile_function() -> None:
    """Register curation_coverage_tile as TILE_FUNCTION in pyegeria's analytic registry (idempotent)."""
    from pyegeria.view.analytic_registry import get_analytic_registry, register_analytic_functions
    if TILE_FUNCTION in get_analytic_registry():
        return
    register_analytic_functions({TILE_FUNCTION: {
        "name": TILE_FUNCTION,
        "function": _TILE_IMPORT_PATH,
        "description": "Resource Explorer's curation-coverage tile for one resource, fetched as the viewer.",
        "returns": "dict (tile with a state envelope)",
        "params": [
            {"name": "slug", "type": "str", "required": True,
             "description": "The resource's slug in Resource Explorer."},
            {"name": "resource_type", "type": "str", "default": "database",
             "description": "One of " + ", ".join(_ENTITY_TYPES) + "."},
        ],
        "family": "Curation",
        "resource_types": list(_ENTITY_TYPES),
    }}, source="re_analytics")


def report_specs():
    """The tile's FormatSet, keyed by its label: the loader PYEGERIA_REPORT_SPEC_MODULES names."""
    from pyegeria.view._output_format_models import ActionParameter, Format, FormatSet, FormatSetDict
    register_tile_function()
    return FormatSetDict({TILE_LABEL: FormatSet(
        heading="Curation Coverage",
        description="Published against not yet published, from Resource Explorer's curation record "
                    "(trellis-analytics curation_coverage, run by RE as the viewer). The subtitle is the "
                    "result's state; counts carry the ids they count.",
        family="Curation",
        target_type=None,
        formats=[Format(types=["DICT", "JSON", "BAR"], attributes=[])],
        # function="" until the Portal image carries pyegeria >= 6.2.2 (ISSUE-141).
        action=ActionParameter(function="", analytic_function=TILE_FUNCTION,
                               analytic_spec_params={"resource_type": "database"}),
    )})
