"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Zone-restricted report specs, per signed-in user (Portal-3; EA's B6, advisor/egeria_spec_restricted.py).

The Portal's shared EGERIA tier holds public specs only: pyegeria's shared-cache sync skips any spec that
carries a governance zone. A restricted spec is read here **as the signed-in user's token**, with pyegeria's
`list_visible_restricted_specs` (6.2.35+); Egeria's zone check decides what comes back, so each user sees
exactly the restricted specs their zones allow.

- **Listing** is cached per **credential identity** (a hash of the token, plus the platform and view
  server), never by bare user id: two sessions of one user can hold different zone grants. Nothing read
  here is written to the shared cache or registered in the shared registry. A sync of the shared tier, or
  a publish, drops these listings (`invalidate`).
- **Describing** one (its full definition, for the Report Specs detail) and **running** one fetch it from
  Egeria for that call, as the user (`refresh_spec`); never a shared copy. pyegeria keeps a fetched spec in
  this process under an internal name ("egeria:<label>@v<N>"). The public execute route denies every such
  name by default (`public_fetched_name_allowed`): only a shared-tier spec at exactly that version passes,
  and a label the restricted path fetches is recorded before its fetch starts.
- No token: "sign in". No function in pyegeria, folders not read, and "read, and nothing restricted is
  visible to you" are each their own answer, never one empty list.
"""
from __future__ import annotations

import hashlib
import os
import re
import threading
import time
from typing import Any, Dict, List, Optional

from loguru import logger

CACHE_TTL_S = float(os.environ.get("PORTAL_RESTRICTED_SPECS_TTL", "120"))
_CACHE_MAX = 256
_lock = threading.Lock()
_cache: Dict[str, Any] = {}
#: (label, header version) of every spec this process fetched through the restricted path.
_RESTRICTED_FETCHED: set = set()
#: Every label the restricted path has fetched or is fetching. Recorded BEFORE the fetch starts: pyegeria
#: holds the definition under its internal name while the run is still going (read-back, 2026-11-12).
_RESTRICTED_LABELS: set = set()
_FETCHED_NAME = re.compile(r"^(?:egeria:)?(?P<label>.+)@v(?P<version>\d+)$")

BADGE = "restricted (visible to you)"
SIGN_IN = "Sign in to see restricted report specs: they are read from Egeria as you."
NEEDS = ("Restricted report specs need pyegeria 6.2.35 or later (list_visible_restricted_specs); this "
         "Portal has an older pyegeria.")


class TokenRefused(Exception):
    """Egeria refused the caller's token: the route answers 401 ("sign in again")."""


# ── seams (replaced in tests) ─────────────────────────────────────────────────

def _reader():
    try:
        from pyegeria.view.egeria_spec_cache import list_visible_restricted_specs
        return list_visible_restricted_specs
    except ImportError:
        return None


def _folders() -> List[str]:
    import report_spec_sync
    return report_spec_sync.configured_folders()


def _platform(token: str) -> tuple[str, str]:
    from egeria_auth import default_platform_url, resolve_platform, token_platform
    url = resolve_platform(token_platform(token) or default_platform_url(), token=token)
    return url, os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")


def _user_client(token: str):
    """A client that acts only as the token's user (no password, so no silent re-login as the service
    account). The platform gate is called in this function, beside the token attach."""
    from pyegeria import EgeriaTech
    from egeria_auth import default_platform_url, resolve_platform, token_platform, use_token
    url = resolve_platform(token_platform(token) or default_platform_url(), token=token)
    client = EgeriaTech(os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"), url,
                        user_id=os.environ.get("EGERIA_USER", "erinoverview"))
    use_token(client, token)
    return client


def _token_user(token: str) -> Optional[str]:
    from egeria_auth import _token_sub
    return _token_sub(token)


def _is_token_refused(exc: BaseException) -> bool:
    """The same test the execute route uses for an Egeria 401."""
    return getattr(exc, "http_error_code", None) == 401 or "HTTP Code: 401" in str(exc)


# ── the cache ─────────────────────────────────────────────────────────────────

def credential_key(token: str) -> str:
    """The cache key of a credential: the token's hash, with the platform and view server it is used on.
    Never the bare user id."""
    url, server = _platform(token)
    return hashlib.sha256(f"{token}|{url}|{server}".encode()).hexdigest()[:32]


def _cache_get(key: str, refresh: bool) -> Any:
    if refresh:
        return None
    with _lock:
        hit = _cache.get(key)
        if hit and time.monotonic() - hit[0] < CACHE_TTL_S:
            return hit[1]
    return None


def _cache_put(key: str, value: Any) -> None:
    with _lock:
        if len(_cache) >= _CACHE_MAX:
            for k, _ in sorted(_cache.items(), key=lambda kv: kv[1][0])[: _CACHE_MAX // 4]:
                _cache.pop(k, None)
        _cache[key] = (time.monotonic(), value)


def invalidate() -> None:
    """Drop every user's cached listing (after a sync of the shared tier, or a publish/withdraw)."""
    with _lock:
        _cache.clear()


# ── listing ───────────────────────────────────────────────────────────────────

def _used_by(folders_qn: List[str], idx: Dict[str, Any]) -> List[str]:
    """The consumers a restricted spec is in, by display name: a folder's own consumer, or the consumer
    whose qualified name is its longest '::' prefix (sub-folders are walked). Unmatched folders keep their
    qualified name."""
    names = {c.get("qualifiedName"): c.get("name") for c in idx.get("consumers") or []
             if c.get("qualifiedName") and c.get("name")}
    out = set()
    for f in folders_qn or []:
        if f in names:
            out.add(names[f])
            continue
        best = max((q for q in names if f.startswith(q + "::")), key=len, default=None)
        out.add(names[best] if best else f)
    return sorted(out)


def restricted_specs(token: Optional[str], *, refresh: bool = False) -> Dict[str, Any]:
    """The restricted specs this user can see in the Portal's folders.

    {"state": ok | none_visible | not_signed_in | unsupported | read_failed | partial,
     "specs": [{"label", "zones", "folders", "qualified_name", "guid", "version", "usedBy"}],
     "message": str | None, "viewer": user id | None, "cached": bool, "badge": BADGE}
    Raises TokenRefused when Egeria refuses the token."""
    base = {"badge": BADGE}
    if not token:
        return {**base, "state": "not_signed_in", "specs": [], "message": SIGN_IN, "viewer": None, "cached": False}
    viewer = _token_user(token)
    reader = _reader()
    if reader is None:
        return {**base, "state": "unsupported", "specs": [], "message": NEEDS, "viewer": viewer, "cached": False}
    folders = _folders()
    key = f"restricted|{credential_key(token)}|{','.join(folders)}"
    cached = _cache_get(key, refresh)
    if cached is not None:
        return {**cached, "cached": True}
    try:
        got = reader(_user_client(token), folders=folders) or {}
    except Exception as exc:  # noqa: BLE001 -- said in words below; never cached
        if _is_token_refused(exc):
            raise TokenRefused("Egeria refused your sign-in token; sign in again.") from exc
        logger.warning(f"restricted specs: reading as {viewer!r} failed: {type(exc).__name__}: {exc}")
        return {**base, "state": "read_failed", "specs": [], "viewer": viewer, "cached": False,
                "message": f"Could not read restricted report specs from Egeria as {viewer}."}
    try:
        import report_spec_consumers
        idx = report_spec_consumers.index()
    except Exception:  # noqa: BLE001
        idx = {}
    status = got.get("status")
    specs = [{**s, "usedBy": _used_by(s.get("folders") or [], idx)} for s in (got.get("specs") or [])
             if isinstance(s, dict) and s.get("label")]
    if status == "not read":
        state, message = "read_failed", f"Restricted report specs were not read: {got.get('reason')}"
    elif status == "partial":
        state, message = "partial", f"Restricted report specs were partly read: {got.get('reason')}"
    elif not specs:
        state, message = "none_visible", got.get("reason") or f"No restricted report specs are visible to {viewer}."
    else:
        state, message = "ok", None
    out = {**base, "state": state, "specs": specs, "message": message, "viewer": viewer,
           "folders": got.get("folders") or folders, "notes": got.get("notes") or []}
    if state != "read_failed":
        _cache_put(key, out)
    return {**out, "cached": False}


def visible_label(token: str, label: str) -> Optional[Dict[str, Any]]:
    """The listed restricted spec named `label`, as this user sees it, or None."""
    for s in restricted_specs(token).get("specs") or []:
        if s.get("label") == label:
            return s
    return None


# ── describe and run (fetched as the user, for this call) ────────────────────

def _remember_fetch(label: str) -> None:
    try:
        from pyegeria.view import egeria_spec_cache as esc
        for (lab, ver) in list(getattr(esc, "_FETCHED", {}) or {}):
            if lab == label:
                _RESTRICTED_FETCHED.add((lab, ver))
    except Exception:  # noqa: BLE001
        pass


def is_restricted_fetch(name: str) -> bool:
    """True for an internal fetched name ("egeria:<label>@v<N>" or "<label>@v<N>") whose label the
    restricted path has fetched, or is fetching now (recorded before the fetch starts)."""
    m = _FETCHED_NAME.match((name or "").strip())
    return bool(m and (m.group("label") in _RESTRICTED_LABELS
                       or (m.group("label"), int(m.group("version"))) in _RESTRICTED_FETCHED))


def _shared_tier_version(label: str) -> Optional[int]:
    try:
        from pyegeria.view.egeria_spec_cache import egeria_tier_info
        info = egeria_tier_info(label) or {}
    except Exception:  # noqa: BLE001
        return None
    v = info.get("header_version")
    return v if isinstance(v, int) and not info.get("fetched") else None


def public_fetched_name_allowed(name: str) -> bool:
    """The public execute route's rule for an internal fetched name, deny by default: allowed only when it
    names a spec of the shared (public) tier at exactly that version, and the restricted path has never
    fetched that label. Any other name is not a fetched name and is not this rule's business (True)."""
    m = _FETCHED_NAME.match((name or "").strip())
    if not m:
        return True
    if is_restricted_fetch(name):
        return False
    return _shared_tier_version(m.group("label")) == int(m.group("version"))


def describe(token: str, label: str) -> Dict[str, Any]:
    """The full definition of a restricted spec this user can see, fetched from Egeria as them:
    {"spec": <the Report Specs row shape>, "zones", "usedBy"} or raises LookupError (not visible)."""
    listed = visible_label(token, label)
    if listed is None:
        raise LookupError(f"No restricted report spec named '{label}' is visible to you.")
    from pyegeria.view.egeria_spec_cache import fetch_spec_for_call, fetched_spec
    _RESTRICTED_LABELS.add(label)          # before the fetch: the public path refuses its name from now on
    try:
        internal = fetch_spec_for_call(_user_client(token), label)
    except Exception as exc:  # noqa: BLE001
        if _is_token_refused(exc):
            raise TokenRefused("Egeria refused your sign-in token; sign in again.") from exc
        raise
    _remember_fetch(label)
    fs = fetched_spec(internal.split(":", 1)[-1])
    if fs is None:
        raise LookupError(f"'{label}' was fetched but its definition could not be read.")
    from report_specs_handler import _serialize
    row = _serialize(label, fs)
    row.update(name=label, label=label, restricted=True, source="restricted", sourceLabel=BADGE,
               zones=listed.get("zones") or [], usedBy=listed.get("usedBy") or [], usedByState="read",
               egeria={"guid": listed.get("guid"), "qualified_name": listed.get("qualified_name"),
                       "version": listed.get("version"), "folders": listed.get("folders")})
    return row


def run(token: str, label: str, *, output_format: str, params: Optional[Dict[str, Any]] = None,
        table_shape: Optional[str] = None) -> Any:
    """Run a restricted spec as the user: fetched from Egeria for this call (refresh_spec=True), never from
    a shared copy, and only one this user's listing shows. Raises LookupError (not visible),
    TokenRefused, or the run's own error."""
    if visible_label(token, label) is None:
        raise LookupError(f"No restricted report spec named '{label}' is visible to you.")
    from pyegeria.view.format_set_executor import exec_report_spec
    url, server = _platform(token)
    kw = {"table_shape": table_shape} if table_shape else {}
    _RESTRICTED_LABELS.add(label)          # before the fetch: the public path refuses its name from now on
    try:
        result = exec_report_spec(label, output_format=output_format, params=params or {}, view_server=server,
                                  view_url=url, user=_token_user(token) or "", user_pass="", token=token,
                                  refresh_spec=True, **kw)
    except Exception as exc:  # noqa: BLE001
        if _is_token_refused(exc):
            raise TokenRefused("Egeria refused your sign-in token; sign in again.") from exc
        raise
    finally:
        _remember_fetch(label)
    return result


def _reset_for_tests() -> None:
    invalidate()
    _RESTRICTED_FETCHED.clear()
    _RESTRICTED_LABELS.clear()
