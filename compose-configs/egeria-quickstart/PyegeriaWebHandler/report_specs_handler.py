"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Report Spec Browser — FastAPI router.

Provides one endpoint:
  GET /api/report-specs   → returns all pyegeria report spec definitions as JSON

Report specs are pyegeria formatting specifications. Most are pyegeria built-ins or
Portal/user specs; some may be held in Egeria and synced into a local cache
(report_spec_sync.py). Listing them needs no Egeria connection: the Egeria-held ones are
read from the cache. Each spec says where it came from (`source`), and which tools it is
published to (`usedBy`, from pyegeria's consumer index; report_spec_consumers.py).
"""

import contextvars
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response
from loguru import logger
from pydantic import BaseModel
from egeria_auth import PlatformBody  # platform gate on the body's url (see egeria_auth)

import report_spec_consumers
import spec_resolution
from result_cache import FRESH, MISS, STALE, ResultCache, credential_identity

from pyegeria.view.base_report_formats import get_report_registry, register_report_specs
from pyegeria.view._output_format_models import FormatSet, Format, Column, ActionParameter

router = APIRouter(tags=["report-specs"])


def register_local_specs():
    """Register the Portal's own report specs as fallbacks for their Egeria-held copies: a local
    copy is registered only while the EGERIA tier does not hold its label (local_spec_fallback.py).
    """
    import local_spec_fallback
    return local_spec_fallback.reconcile()


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


# ── Where each spec came from ────────────────────────────────────────────────
# pyegeria's registry has three tiers: builtin (the packaged seed), egeria (synced from Egeria into
# a local cache) and local. The Portal splits local into "local" (registered at runtime by Portal
# code, e.g. register_local_specs above) and "user" (JSON spec files in the user report specs
# directory, pyegeria's CONFIG tier).
SOURCE_WORDS = {
    "builtin": "pyegeria built-in",
    "egeria":  "held in Egeria",
    "local":   "Portal (local)",
    "user":    "user spec file",
}


def _spec_statuses() -> dict:
    """name -> pyegeria's list_report_specs(with_status=True) row; {} on a pyegeria without it."""
    try:
        from pyegeria.view.base_report_formats import list_report_specs
        return {row["name"]: row for row in list_report_specs(with_status=True)
                if isinstance(row, dict) and row.get("name")}
    except Exception as exc:  # noqa: BLE001 -- the source column is extra; never fail the list on it
        logger.warning(f"report specs: list_report_specs(with_status=True) unavailable: {exc}")
        return {}


def _user_labels() -> set:
    try:
        from pyegeria.view import base_report_formats as brf
        return set(getattr(brf, "_CONFIG_REPORT_FORMATS", {}) or {})
    except Exception:  # noqa: BLE001
        return set()


def _source_fields(name: str, row: Optional[dict], user_labels: set) -> dict:
    """The source/shadow fields for one spec. `source` is None when pyegeria did not say."""
    if not row:
        return {"source": None, "sourceLabel": "not reported", "shadowedBy": None, "shadows": None,
                "cacheAgeS": None, "egeria": None}
    source = row.get("source")
    base = name
    if source == "local" and base in user_labels:
        source = "user"
    out = {"source": source, "sourceLabel": SOURCE_WORDS.get(source, source or "not reported"),
           "shadowedBy": row.get("shadowed_by"), "shadows": row.get("shadows"),
           "cacheAgeS": row.get("cache_age_s"), "egeria": None}
    if source == "egeria":
        try:
            from pyegeria.view.egeria_spec_cache import egeria_tier_info
            info = egeria_tier_info(base) or {}
            out["egeria"] = {k: info.get(k) for k in ("guid", "qualified_name", "version", "header_version",
                                                      "synced_at", "fetched_at", "folders", "draft")}
        except Exception:  # noqa: BLE001
            pass
    return out


def _is_admin_closed(request: Request) -> bool:
    """The Portal's admin check, failing CLOSED: if the check itself cannot be loaded, nobody is
    an administrator. (Local quickstart without auth: _is_admin says everyone is.)"""
    try:
        from demo_feedback_handler import _is_admin
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"report specs: admin check unavailable, refusing admin-only access: {exc}")
        return False
    try:
        return bool(_is_admin(request))
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"report specs: admin check failed, refusing admin-only access: {exc}")
        return False


def _sync_detail_allowed(request: Optional[Request]) -> bool:
    """Error text and skip reasons from the sync go to administrators and to signed-in callers
    (an unexpired X-Egeria-Token); anonymous callers get the outcome without the detail."""
    if request is None:
        return False
    try:
        from egeria_auth import _token_expired, get_request_token
        token = get_request_token()
        if token and not _token_expired(token):
            return True
    except Exception:  # noqa: BLE001
        pass
    return _is_admin_closed(request)


def _sync_status_for(request: Optional[Request]) -> dict:
    import report_spec_sync
    if _sync_detail_allowed(request):
        return dict(report_spec_sync.status(), detail=True)
    return report_spec_sync.public_status()


def spec_source_for(name: str, run_source: Optional[dict] = None) -> Optional[dict]:
    """Where the spec a run used came from, in the Report Specs view's words: {"source",
    "sourceLabel", "shadows", "shadowedBy"}. `run_source` is the run's own `spec_source` (pyegeria
    resolved it with the same lookup that ran it); without one, pyegeria's report_spec_source(name)
    is asked. None when neither can say: the page then shows no badge, never a guessed tier."""
    src = run_source if isinstance(run_source, dict) else None
    if src is None:
        try:
            from pyegeria.view.base_report_formats import report_spec_source
            src = report_spec_source(name)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"report specs: spec source for {name!r} unavailable: {exc}")
            src = None
    tier = (src or {}).get("tier")
    if tier not in ("builtin", "egeria", "local"):
        return None
    label = (src or {}).get("label") or name
    source = "user" if tier == "local" and label in _user_labels() else tier
    shadows = shadowed_by = None
    try:
        from pyegeria.view import base_report_formats as brf
        shadow = (getattr(brf, "_REGISTRY_SHADOWS", {}) or {}).get(label)
    except Exception:  # noqa: BLE001
        shadow = None
    if shadow:
        if shadow.get("winner") == tier:
            shadows = shadow.get("loser")
        elif shadow.get("loser") == tier:
            shadowed_by = shadow.get("winner")
    return {"source": source, "sourceLabel": SOURCE_WORDS.get(source, source), "label": label,
            "shadows": shadows, "shadowedBy": shadowed_by}


def _egeria_held_summary(source_counts: dict, request: Optional[Request] = None) -> dict:
    """What the Report Specs view says about specs held in Egeria. Never just an empty list: when
    there are none, `message` says so and why."""
    import report_spec_sync
    sync = _sync_status_for(request)
    count = source_counts.get("egeria", 0)
    folders = sync.get("folders") or []
    outcome = sync.get("outcome")
    doing = report_spec_sync.running_words(sync)
    if count:
        message = f"{count} report spec{'s' if count != 1 else ''} held in Egeria"
    elif not folders:
        message = ("None held in Egeria: no report spec folders are configured for this Portal "
                   "(PYEGERIA_REPORT_SPEC_FOLDERS)")
    elif doing and outcome in (None, "failed"):
        message = f"None held in Egeria yet: {doing}"
    elif outcome is None:
        message = "None held in Egeria yet: no sync from Egeria has run"
    elif outcome == "failed":
        message = "None held in Egeria: the last sync from Egeria failed, so nothing is cached"
    elif outcome == "folders_missing":
        message = "None held in Egeria: the configured folders were not found in Egeria (or are not visible to the Portal's user)"
    elif outcome == "not_configured":
        message = "None held in Egeria: no report spec folders were configured when the last sync ran"
    elif outcome == "already_running":
        message = "None held in Egeria yet: another process was syncing this cache; try again shortly"
    else:
        message = "None held in Egeria: the configured folders hold no active report specs"
        if sync.get("missing_folders"):
            message += " (not found or not visible: " + ", ".join(sync["missing_folders"]) + ")"
    return {"count": count, "message": message, "folders": folders, "running": doing, "sync": sync}


@router.get("/api/report-specs", summary="List all pyegeria report spec definitions")
def get_report_specs(
    request: Request,
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
    statuses = _spec_statuses()
    user_labels = _user_labels()
    consumers = report_spec_consumers.index()

    # The list stays the registry's names (RS-W2-4). A spec that shadows a lower-tier copy says so
    # on its own row (`shadows`), and that copy stays runnable as "builtin:<name>" / "egeria:<name>".
    result: list[dict] = []
    for name, fs in registry.items():
        s = _serialize(name, fs)
        s["resolution"] = spec_resolution.resolution(name, fs, resolutions.get(name))
        s.update(_source_fields(name, statuses.get(name), user_labels))
        s.update(report_spec_consumers.used_by(name, s.get("source"), s.get("egeria"), consumers))

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

    source_counts: dict = {}
    for s in result:
        key = s.get("source") or "unknown"
        source_counts[key] = source_counts.get(key, 0) + 1

    return JSONResponse({
        "specs":        result,
        "sources":      source_counts,
        "sourceWords":  SOURCE_WORDS,
        "egeriaHeld":   _egeria_held_summary(source_counts, request),
        # "Used by": how the consumer index was read ("read" | "partial" | "not read" + reason).
        "consumers":    report_spec_consumers.summary(consumers),
        "families":     families,
        "perspectives": all_perspectives,
        "total":        len(result),
        # Three states, never two: format-only specs are not unrunnable. `unresolved` counts
        # specs pyegeria did not resolve (0 when the resolver is present).
        "counts":       spec_resolution.counts(resolutions, [s["name"] for s in result]),
        "portalSupply": spec_resolution.PORTAL_SUPPLY_NOTE,
        "bindersDeprecatedPrefix": spec_resolution.binders_prefix(),
    })


# ── Sync from Egeria ─────────────────────────────────────────────────────────

def _admin_gate(request: Request):
    """The Portal's admin check (as bootstrap_admin_handler.py uses), but failing CLOSED: if the
    check cannot be loaded, the sync is refused."""
    if not _is_admin_closed(request):
        raise HTTPException(status_code=403, detail="Syncing report specs from Egeria requires an administrator.")


@router.post("/api/report-specs/sync", summary="Sync report specs held in Egeria into the Portal's cache (admin only)")
def sync_from_egeria(request: Request):
    """Start `sync_report_specs` for the configured folders in the background. Reads Egeria only.
    Poll GET /api/report-specs/sync for the outcome."""
    _admin_gate(request)
    import report_spec_sync
    started = report_spec_sync.start("admin")
    st = dict(report_spec_sync.status(), detail=True)
    return JSONResponse({"started": started, "already_running": not started,
                         "running_words": report_spec_sync.running_words(st), **st})


@router.get("/api/report-specs/sync", summary="The last sync of report specs from Egeria")
def sync_status(request: Request):
    """Outcome, counts and what a running sync is doing, for everyone. Error text and skip
    reasons only for administrators and signed-in callers (detail: true)."""
    import report_spec_sync
    st = _sync_status_for(request)
    return JSONResponse(dict(st, running_words=report_spec_sync.running_words(st)))


# ── Execute ───────────────────────────────────────────────────────────────────

class ExecuteRequest(PlatformBody):
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
    # "structured" asks pyegeria (>= 6.2.37) for the structured TABLE result (kind "table", native values,
    # rendered by static/egeria-table.js). Only for output_format TABLE; ignored for every other format.
    # The default (None / "rows") is today's kind "json" rows, so other callers are unchanged.
    table_shape:   Optional[str] = None


TABLE_SHAPES = ("rows", "structured")


def _table_shape(req) -> Optional[str]:
    """The table_shape to pass to exec_report_spec: None unless the format is TABLE and a shape was
    asked for. A value other than "rows" / "structured" is refused (400) whatever the format."""
    shape = req.table_shape
    if shape is not None and shape not in TABLE_SHAPES:
        raise HTTPException(status_code=400, detail=f'table_shape must be "rows" or "structured", not {shape!r}.')
    if shape is None or str(req.output_format or "").upper() != "TABLE":
        return None
    return shape


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
    from egeria_auth import _token_expired, get_request_token, lineage_key

    url      = req.url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = req.server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = req.user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = req.user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    token    = get_request_token()
    _table_shape(req)            # refuse a bad value before any cache read or Egeria call

    from report_viewer import reset_viewer, resolve_viewer, set_viewer
    viewer = resolve_viewer(request, req.persona)
    viewer_token = set_viewer(viewer)
    try:
        # An expired token is never served from cache: it must reach _run_spec and be refused (401).
        if not req.cache or (token and _token_expired(token)):
            return JSONResponse(_run_spec(req, request, token, url, server, user_id, user_pwd))
        key = _cache_key(req, url, server, _credential_identity(req, token, user_id), viewer, lineage_key())
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


def _credential_identity(req, token, user_id) -> str:
    """See result_cache.credential_identity."""
    return credential_identity(token, req.user_id, req.user_pwd, user_id)


def _cache_key(req, url, server, identity, viewer, lineage) -> tuple:
    """Everything that can change the answer: the spec, format, params, platform, the signed-in
    identity (zone visibility differs per viewer), the chosen persona, the forLineage toggle, and the
    table shape (a structured TABLE and TABLE rows are different results)."""
    params = json.dumps(req.params, sort_keys=True, default=str)
    return (req.spec_name, req.output_format, params, url, server, identity,
            (viewer or {}).get("persona_id"), lineage, _table_shape(req))


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
                                 args=(_background_refresh, key, req, None, token, url, server, user_id, user_pwd)).start()
            return _cache_response(body, "stale", stored_at)
    if not req.refresh:
        err = _RESULT_CACHE.recent_timeout(key)
        if err is not None:      # it timed out a moment ago; do not spend the full timeout again on every load
            raise err
        leader, flight = _RESULT_CACHE.begin_flight(key)
        if not leader:           # another request is already running this exact report: wait for it
            flight.event.wait(_FLIGHT_WAIT)
            state, body, stored_at = _RESULT_CACHE.lookup(key)
            if state in (FRESH, STALE):
                return _cache_response(body, "hit", stored_at)
            if flight.error is not None:
                raise flight.error
            # the leader's result was too large to store (or it vanished): run it ourselves
            leader, flight = False, None
    else:
        leader, flight = False, None
    error = None
    try:
        body = JSONResponse(_run_spec(req, request, token, url, server, user_id, user_pwd)).body
        stored_at = _RESULT_CACHE.put(key, body)    # stored BEFORE followers are woken
    except BaseException as exc:
        error = exc
        if _is_timeout(exc):
            _RESULT_CACHE.note_timeout(key, exc)
        raise
    finally:
        if leader:
            _RESULT_CACHE.end_flight(key, flight, error)
    return _cache_response(body, "refresh" if req.refresh else "miss", stored_at)


_FLIGHT_WAIT = 200.0   # a follower waits at most this long for the leader's run (pyegeria times out at 90 s)


def _is_timeout(exc) -> bool:
    """A run that hit a timeout (pyegeria TIMEOUT_ERROR_408, an asyncio/httpx timeout, or a gateway 504)."""
    if isinstance(exc, HTTPException):
        text = str(exc.detail)
        return exc.status_code in (408, 504) or "TIMEOUT_ERROR_408" in text or "timed out" in text.lower()
    return False


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


# A Report that pins one element (collection_guid, collection_qname, ...) fails in Egeria's words once that
# element is gone: a stale GUID comes back as CLIENT_ERROR_400 naming it, a name that matches nothing as a
# pyegeria not-found (404). Either way the honest sentence is that the element is gone (W1).
_PINNED_PARAM = re.compile(r"^([a-z][a-z0-9_]*?)_(guid|qname|qualified_name)$")


def _http_code(exc) -> Optional[int]:
    for attr in ("related_http_code", "http_error_code", "http_status_code", "response_code"):
        v = getattr(exc, attr, None)
        try:
            if v is not None and int(v) >= 400:   # an Egeria 200 wrapper carries the real code elsewhere
                return int(v)
        except (TypeError, ValueError):
            continue
    text = str(exc)
    for code in (404, 400):
        if f"CLIENT_ERROR_{code}" in text or f"HTTP Code: {code}" in text:
            return code
    return None


def missing_pinned_element(exc, params: Optional[dict]) -> Optional[str]:
    """The sentence for a Report whose pinned element no longer exists, or None if `exc` is something else.

    Only a 404, or a 400 whose text names the pinned value, counts: any other 400 is a real refusal and keeps
    its own words."""
    pins = []
    for key, value in (params or {}).items():
        m = _PINNED_PARAM.match(str(key))
        if m and isinstance(value, str) and value.strip():
            pins.append((m.group(1).replace("_", " "), value.strip()))
    if not pins:
        return None
    code = _http_code(exc)
    text = str(exc)
    for thing, value in pins:
        if code == 404 or (code == 400 and value in text):
            return f"The {thing} this report names no longer exists ({value})."
    return None


def _run_spec(req, request, token, url, server, user_id, user_pwd):
    """Run the spec; return the result, or raise the HTTPException the browser should see."""
    from pyegeria.view.format_set_executor import exec_report_spec
    from egeria_auth import TOKEN_REFUSED_WORDS, PortalSupply
    from pyegeria.view.role_supply import CallerTokenExpired

    shape = {"table_shape": _table_shape(req)} if _table_shape(req) else {}
    try:
        result = exec_report_spec(
            req.spec_name,
            **shape,
            output_format=req.output_format,
            params=req.params,
            view_server=server,
            view_url=url,
            user=user_id,
            user_pass=user_pwd,
            token=token,
            supply=PortalSupply(request, view_server=server, view_url=url, user_id=user_id, user_pwd=user_pwd),
        )
        if isinstance(result, dict):
            result["specSource"] = spec_source_for(req.spec_name, result.get("spec_source"))
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
        gone = missing_pinned_element(exc, req.params)
        if gone:
            logger.info(f"exec_report_spec {req.spec_name!r}: {gone}")
            raise HTTPException(status_code=404, detail=gone)
        logger.exception("exec_report_spec failed")
        raise HTTPException(status_code=500, detail=f"Execution failed: {exc}")
