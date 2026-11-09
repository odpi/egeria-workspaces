"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Report Spec Browser — FastAPI router.

Provides one endpoint:
  GET /api/report-specs   → returns all pyegeria report spec definitions as JSON

Report specs are client-side pyegeria formatting specifications stored in
pyegeria.view.base_report_formats.  They are not stored in Egeria and this
endpoint requires no Egeria connection.
"""

import contextvars
import hashlib
import json
import os
import threading
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response
from loguru import logger
from pydantic import BaseModel

import spec_resolution
from result_cache import FRESH, MISS, STALE, ResultCache

from pyegeria.view.base_report_formats import get_report_registry, register_report_specs
from pyegeria.view._output_format_models import FormatSet, Format, Column, ActionParameter

router = APIRouter(tags=["report-specs"])


def register_local_specs():
    """Register workspace-local report specs into the pyegeria registry.
    This allows us to provide professional, generally useful analytic specs
    directly in the workspace before they are formally released into the
    core pyegeria library.
    """
    register_report_specs({
        "Analytic - Element Count by Type": FormatSet(
            heading="Element Count by Type",
            description="Counts active elements of a given type. Use type_name in "
                        "analytic_spec_params to set the target type.",
            family="Analytic",
            target_type=None,
            formats=[Format(types=["DICT", "JSON"], attributes=[])],
            action=ActionParameter(
                function="",
                analytic_function="count_elements",
                analytic_spec_params={"type_name": "GlossaryTerm"}
            )
        ),
        "Analytic - Generic Metric Trend": FormatSet(
            heading="Generic Metric Trend",
            description="Trend any analytic function over time. metric_path is the target function; "
                        "metric_params are its keyword arguments. Default trends count_elements(type_name=Asset).",
            family="Analytic",
            target_type=None,
            formats=[Format(types=["DICT", "JSON", "SERIES"], attributes=[])],
            action=ActionParameter(
                function="",
                analytic_function="metric_trend",
                analytic_spec_params={
                    "metric_path": "count_elements",
                    "metric_params": {"type_name": "Asset"},
                    "window": "6mo"
                }
            )
        )
    }, source="workspace_local")


try:
    register_local_specs()
except Exception as e:
    logger.warning(f"Failed to register local report specs: {e}")


def _get_registry() -> dict:
    return get_report_registry()


def _serialize_format(fmt) -> dict:
    """Serialise a single Format object (one row in the FormatSet.formats list)."""
    types = [str(t) for t in (getattr(fmt, "types", []) or [])]
    attrs = []
    for a in (getattr(fmt, "attributes", []) or []):
        attrs.append({
            "key":        getattr(a, "key",         "") or "",
            "name":       getattr(a, "name",        "") or "",
            "format":     bool(getattr(a, "format", False)),
            "detailSpec": getattr(a, "detail_spec", None) or None,
        })
    return {"types": types, "attributes": attrs}


def _serialize(name: str, fs) -> dict:
    """Convert a FormatSet object to a JSON-serialisable dict."""
    output_types: set[str] = set()
    formats = []
    for fmt in (getattr(fs, "formats", []) or []):
        for t in (getattr(fmt, "types", []) or []):
            output_types.add(str(t))
        formats.append(_serialize_format(fmt))

    question_spec = [
        {
            "perspectives": list(getattr(qs, "perspectives", []) or []),
            "questions":    list(getattr(qs, "questions",    []) or []),
        }
        for qs in (getattr(fs, "question_spec", []) or [])
    ]

    action = getattr(fs, "action", None)
    action_dict = None
    if action is not None:
        action_dict = {
            "function":              getattr(action, "function", "") or "",
            "required_params":       list(getattr(action, "required_params", []) or []),
            "optional_params":       list(getattr(action, "optional_params", []) or []),
            "spec_params":           dict(getattr(action, "spec_params", {}) or {}),
            "analytic_function":     getattr(action, "analytic_function", None) or None,
            "analytic_spec_params":  dict(getattr(action, "analytic_spec_params", {}) or {}),
        }

    return {
        "name":          name,
        "family":        getattr(fs, "family",      None),
        "heading":       getattr(fs, "heading",     None) or "",
        "description":   getattr(fs, "description", None) or "",
        "target_type":   getattr(fs, "target_type", None),
        "aliases":       list(getattr(fs, "aliases", []) or []),
        "output_types":  sorted(output_types),
        "formats":       formats,
        "question_spec": question_spec,
        "action":        action_dict,
    }


@router.get("/api/report-specs", summary="List all pyegeria report spec definitions")
def get_report_specs(
    perspective: Optional[str] = Query(
        None,
        description="Filter to specs whose question_spec includes this perspective (case-insensitive).",
    ),
    q: Optional[str] = Query(
        None,
        description="Filter by spec name, description, or question text (case-insensitive substring).",
    ),
):
    """
    Return all pyegeria report spec definitions (FormatSets) as JSON.

    These are client-side formatting specifications defined in
    pyegeria.view.base_report_formats.  No Egeria connection is required.

    The full list is returned and filtering is intentionally lightweight —
    the browser UI does all interactive search client-side.  Server-side
    filters (``perspective``, ``q``) are provided for direct API use.
    """
    try:
        registry = _get_registry()
    except Exception as exc:
        logger.exception(f"Failed to load report spec registry: {exc}")
        raise HTTPException(status_code=500, detail=f"Report spec registry unavailable: {exc}")

    persp_lower = perspective.strip().lower() if perspective else None
    q_lower     = q.strip().lower()           if q         else None

    # Load-time resolution (pyegeria spec_resolver, cached): runnable, unrunnable with the
    # resolver's words, or format-only. Keyed on the existing spec name (RS-W2-4).
    resolutions = spec_resolution.resolve_all()

    result: list[dict] = []
    for name, fs in registry.items():
        s = _serialize(name, fs)
        s["resolution"] = spec_resolution.resolution(name, fs, resolutions.get(name))

        if persp_lower is not None:
            all_p = [p.lower() for qs in s["question_spec"] for p in qs["perspectives"]]
            if not any(persp_lower in p for p in all_p):
                continue

        if q_lower is not None:
            name_hit     = q_lower in s["name"].lower() or q_lower in s["description"].lower()
            question_hit = any(
                q_lower in question.lower()
                for qs in s["question_spec"]
                for question in qs["questions"]
            )
            if not (name_hit or question_hit):
                continue

        result.append(s)

    families = sorted({s["family"] or "General" for s in result})
    all_perspectives = sorted({
        p
        for s in result
        for qs in s["question_spec"]
        for p in qs["perspectives"]
    })

    return JSONResponse({
        "specs":        result,
        "families":     families,
        "perspectives": all_perspectives,
        "total":        len(result),
        # Three states, never two: format-only specs are not unrunnable. `unresolved` counts
        # specs pyegeria did not resolve (0 when the resolver is present).
        "counts":       spec_resolution.counts(resolutions, [s["name"] for s in result]),
        "portalSupply": spec_resolution.PORTAL_SUPPLY_NOTE,
        "bindersDeprecatedPrefix": spec_resolution.binders_prefix(),
    })


# ── Execute ───────────────────────────────────────────────────────────────────

class ExecuteRequest(BaseModel):
    spec_name:     str
    output_format: str = "REPORT"
    params:        dict = {}
    url:           Optional[str] = None
    server:        Optional[str] = None
    user_id:       Optional[str] = None
    user_pwd:      Optional[str] = None
    # The persona the browser picked, for analytic functions that must act as
    # the viewer elsewhere (report_viewer.py). Optional: other specs ignore it.
    persona:       Optional[str] = None
    # Local-dashboard placements opt in to the server-side result cache (see _RESULT_CACHE below). The
    # Report Specs browser's manual Run leaves this off and always runs live.
    cache:         bool = False
    # With cache=True: skip the cache read, run now, and store the fresh result (a viewer's refresh click).
    refresh:       bool = False


@router.post("/api/report-specs/execute", summary="Execute a report spec action")
def execute_spec(req: ExecuteRequest, request: Request):
    """Call exec_report_spec and return a normalised result structure.

    pyegeria 6.1.10 (ISSUE-86) added a `token` param to exec_report_spec --
    when a caller already holds a bearer token for the current user, passing
    it runs the report as that user via set_bearer_token() instead of
    re-authenticating with user/user_pass on every call. We check
    get_request_token() (the X-Egeria-Token contextvar egeria_auth.py's
    middleware populates, same mechanism other handlers already use) and
    pass it through when present; falls back to user_id/user_pwd exactly as
    before otherwise. NOTE: as of 2026-09-05 no frontend caller of this
    endpoint actually sends X-Egeria-Token yet (the browser only holds
    user_id/user_pwd client-side, not a bearer token), so this is currently
    inert plumbing, not a behavior change -- wiring up a real client-side
    token flow is a separate, larger piece of work.
    """
    from egeria_auth import _token_expired, get_request_token, lineage_key, token_user

    url      = req.url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = req.server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = req.user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = req.user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    token    = get_request_token()

    from report_viewer import reset_viewer, resolve_viewer, set_viewer
    viewer = resolve_viewer(request, req.persona)
    viewer_token = set_viewer(viewer)
    try:
        # An expired token is never served from cache: it must reach _run_spec and be refused (401).
        if not req.cache or (token and _token_expired(token)):
            return JSONResponse(_run_spec(req, request, token, url, server, user_id, user_pwd))
        key = _cache_key(req, url, server, token_user() or user_id, viewer, lineage_key())
        return _cached_execute(key, req, request, token, url, server, user_id, user_pwd)
    finally:
        reset_viewer(viewer_token)


# ── Result cache for local-dashboard placements ─────────────────────────────
# A placement run takes 20-35 s because each run hits Egeria; a revisit should not pay that again.
# Fresh (<5 min): served at once. Stale: served at once, marked stale, and refreshed once in the
# background. Only successful results are stored: an error, a refusal (400) or a token failure
# propagates and is never cached. A "not measured" result is a success and is cached verbatim, so
# it still renders as not measured. Bounded (LRU). See result_cache.py.
_RESULT_CACHE = ResultCache(
    ttl=float(os.environ.get("PORTAL_RESULT_CACHE_TTL", "300")),
    max_entries=int(os.environ.get("PORTAL_RESULT_CACHE_MAX", "256")))


def _cache_key(req, url, server, identity, viewer, lineage) -> tuple:
    """Everything that can change the answer: the spec, format, params, platform, the signed-in
    identity (zone visibility differs per viewer), the chosen persona, and the forLineage toggle."""
    params = json.dumps(req.params, sort_keys=True, default=str)
    return (req.spec_name, req.output_format, params, url, server, identity,
            (viewer or {}).get("persona_id"), lineage)


def _stamp(stored_at: float) -> dict:
    return {"X-Cache-At": datetime.fromtimestamp(stored_at, timezone.utc).isoformat(timespec="seconds"),
            "X-Cache-Age": str(max(0, int(time.time() - stored_at)))}


def _cache_response(body: bytes, state: str, stored_at: float) -> Response:
    return Response(content=body, media_type="application/json",
                    headers={"X-Cache": state, **_stamp(stored_at)})


def _cached_execute(key, req, request, token, url, server, user_id, user_pwd) -> Response:
    if not req.refresh:
        state, body, stored_at = _RESULT_CACHE.lookup(key)
        if state == FRESH:
            return _cache_response(body, "hit", stored_at)
        if state == STALE:
            # claim is atomic: exactly one background refresh per key
            if _RESULT_CACHE.claim_refresh(key):
                ctx = contextvars.copy_context()   # carries the token, forLineage and viewer to the thread
                threading.Thread(target=ctx.run, daemon=True, name="report-spec-refresh",
                                 args=(_background_refresh, key, req, request, token, url, server, user_id, user_pwd)).start()
            return _cache_response(body, "stale", stored_at)
    # cold miss, or a forced refresh: run now, as an uncached call would
    body = JSONResponse(_run_spec(req, request, token, url, server, user_id, user_pwd)).body
    stored_at = _RESULT_CACHE.put(key, body)
    return _cache_response(body, "refresh" if req.refresh else "miss", stored_at)


def _background_refresh(key, req, request, token, url, server, user_id, user_pwd) -> None:
    failed = False
    try:
        body = JSONResponse(_run_spec(req, request, token, url, server, user_id, user_pwd)).body
        _RESULT_CACHE.put(key, body)
    except Exception as exc:  # noqa: BLE001 -- the stale entry stays; nothing failed is cached
        failed = True
        logger.warning(f"report-spec cache: background refresh of {req.spec_name!r} failed: {exc}")
    finally:
        _RESULT_CACHE.release_refresh(key, failed=failed)


def _run_spec(req, request, token, url, server, user_id, user_pwd):
    """Run the spec; return the result, or raise the HTTPException the browser should see."""
    from pyegeria.view.format_set_executor import exec_report_spec
    from egeria_auth import TOKEN_REFUSED_WORDS, PortalSupply
    from pyegeria.view.role_supply import CallerTokenExpired

    try:
        result = exec_report_spec(
            req.spec_name,
            output_format=req.output_format,
            params=req.params,
            view_server=server,
            view_url=url,
            user=user_id,
            user_pass=user_pwd,
            token=token,
            supply=PortalSupply(request, view_server=server, view_url=url, user_id=user_id, user_pwd=user_pwd),
        )
        return result
    except CallerTokenExpired:
        # Refused before any Egeria call; same 401 words as an Egeria 401 below.
        raise HTTPException(status_code=401, detail=TOKEN_REFUSED_WORDS)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        # Propagate Egeria 401s as HTTP 401 so the client can show a meaningful message.
        exc_text = str(exc)
        if "HTTP Code: 401" in exc_text or getattr(exc, "http_error_code", None) == 401:
            raise HTTPException(status_code=401, detail="Not authorized for this operation — the current user does not have permission for this report")
        logger.exception("exec_report_spec failed")
        raise HTTPException(status_code=500, detail=f"Execution failed: {exc}")
