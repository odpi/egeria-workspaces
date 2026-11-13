# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Local Dashboards — FastAPI router.

Browses user-authored Dashboard Sheets: the local-JSON-store model
(pyegeria.view._output_dashboard_sheet_models.DashboardSheet) built by the
Dr.Egeria `Create Dashboard Sheet` / `Link Report to Dashboard Sheet`
commands (egeria-python md_processing/v2/dashboard_sheet.py). Each Dashboard
Sheet is an ordered list of Placements, each referencing a real Egeria
`Report` asset (created via the Dr.Egeria `Create Report` command; see
egeria-python md_processing/v2/report.py) or another Dashboard Sheet
(nesting).

Hard cutover 2026-07-29: a Placement used to reference a bare Report Spec
(FormatSet) name directly — switched to referencing a `Report` element by
name instead, since a Report Spec has no way to carry fixed/scoped
parameters (BACKLOG.md NEXT-14). A `Report` is a real Egeria asset
(DataSet -> Asset -> Referenceable) whose `additionalProperties` dict holds
`reportSpec` (the FormatSet to run) plus its own default execution params
(`outputFormat`, `searchString`, etc. — the same vocabulary Dr.Egeria's
`View Report` command exposes ad-hoc). Resolving a placement now means one
live Egeria lookup per Report-typed placement, not a pure in-process
registry lookup like before — accepted tradeoff (if Egeria's unreachable
the report couldn't execute anyway).

This is deliberately separate from egeria-overview.html's own Container
model (overview_containers.py): that one is the Overview app's own static
P0 KPI layout, resolved against overview_specs.SPECS (Python-computed tiles,
not stored ReportSpecs). Dashboard Sheets are the user-authored model —
different leaf type, different registry, different app.

Routes:
  GET /local-dashboards                    → serve the SPA
  GET /api/local-dashboards                → list all Dashboard Sheets (summary)
  GET /api/local-dashboards/{name}         → one sheet, placements resolved against
                                              live Egeria Report elements (+ nested
                                              sheets resolved against the sheet store)
  GET /api/local-dashboards/documents      → list shared Dr.Egeria documents
  GET /api/local-dashboards/documents/{filename} → one document's raw content

Rendering a placement reuses the existing POST /api/report-specs/execute
endpoint (report_specs_handler.py) — no new execution path. A `kind: "report"`
placement carries the Report's own stored `outputFormat`/`params`, used as-is
(no more guessing/auto-fill); a Report whose underlying spec still needs
params it doesn't have surfaces `requiredParams` so the SPA can point at the
full Report Spec Browser (Egeria Explorer) instead of guessing values.

The `documents` endpoints browse a shared, read-only folder of Dr.Egeria
dashboard-definition documents — exchange-quickstart/loading-bay/dr-egeria-inbox/
Local Dashboards, already bind-mounted into this container (read-only) at
/deployments/loading-bay as part of the existing loading-bay mount, no new
volume needed. This is the canonical place to drop a `.dr-egeria.md` file
that defines/updates a Dashboard Sheet, so it can be browsed and run from
the Local Dashboards page's "Run Dr.Egeria Document" panel (POST
/api/dr-egeria/execute-document, dr_egeria_commands_handler.py) instead of
pasting it in by hand.
"""
import contextvars
import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, Response
from loguru import logger

import spec_resolution
from result_cache import FRESH, MISS, STALE, ResultCache, credential_identity, request_identity

router = APIRouter(tags=["local-dashboards"])

_HERE = Path(__file__).parent
_HTML = _HERE / "local-dashboards.html"

_DOCS_DIR = Path(os.getenv(
    "LOCAL_DASHBOARDS_DOCS_PATH",
    "/deployments/loading-bay/dr-egeria-inbox/Local Dashboards",
))

# ── caching (BACKLOG.md NEXT-22) ─────────────────────────────────────────────
# Before this, every route re-read/re-parsed the sheet store from disk, re-
# fetched the report spec registry, and did a live Egeria find per Report-
# typed placement -- on every single page load. overview_handler.py already
# solved the equivalent problem for Overview with a tiny TTL cache; mirrored
# here for the registry/report lookups. The sheet store gets a different
# (mtime-based, not TTL) strategy below since it's a local file this process
# doesn't exclusively own -- Dr.Egeria command processing
# (egeria-python md_processing/v2/dashboard_sheet.py) writes it directly,
# outside this handler, so a blind TTL could serve stale content after an
# external write; comparing mtime catches that immediately instead of after
# up to _CACHE_TTL seconds.

_CACHE_TTL = 60.0  # seconds; matches overview_handler.py's default general TTL
_cache: dict[str, tuple[float, Any]] = {}

# Sentinel so a cached "Egeria does not hold this sheet" (_egeria_one) is
# distinguishable from "nothing cached yet". A Report lookup's miss is not
# cached at all (see _find_report_by_name).
_MISS = object()


def _cache_get(key: str):
    hit = _cache.get(key)
    if hit and (time.time() - hit[0]) < _CACHE_TTL:
        return hit[1]
    return None


def _cache_put(key: str, value: Any):
    _cache[key] = (time.time(), value)
    return value


def _store_path() -> str:
    return os.path.expanduser(
        os.getenv("PYEGERIA_DASHBOARD_SHEETS_STORE", "~/.pyegeria/dashboard_sheets.json")
    )


# path -> (mtime, DashboardSheetDict)
_sheets_cache: dict[str, tuple[float, Any]] = {}


def _load_sheets():
    from pyegeria.view._output_dashboard_sheet_models import DashboardSheetDict
    path = _store_path()
    if not os.path.exists(path):
        return DashboardSheetDict()
    mtime = os.path.getmtime(path)
    cached = _sheets_cache.get(path)
    if cached and cached[0] == mtime:
        return cached[1]
    sheets = DashboardSheetDict.load_from_json(path)
    _sheets_cache[path] = (mtime, sheets)
    return sheets


def _invalidate_sheets_cache() -> None:
    """Force the next _load_sheets() to re-read from disk. Called after this
    handler's own writes (delete) so a same-second reload doesn't miss the
    change on filesystems with coarse (1s) mtime resolution -- the mtime
    check above already covers writes from anywhere else (e.g. Dr.Egeria
    command processing), this just removes the same-second race for our own."""
    _sheets_cache.pop(_store_path(), None)


def _save_sheets(sheets) -> None:
    from pyegeria.view._output_dashboard_sheet_models import save_dashboard_sheets_to_json
    save_dashboard_sheets_to_json(sheets, _store_path())
    _invalidate_sheets_cache()


def _report_registry() -> dict:
    from pyegeria.view.base_report_formats import get_report_registry
    hit = _cache_get("registry")
    if hit is not None:
        return hit
    return _cache_put("registry", get_report_registry())


# ── Live Egeria lookup for Report-typed placements ──────────────────────────
# Sync client, matching overview_handler.py's _expert()/_make() convention —
# these routes are sync `def`s (see CLAUDE.md's async-invariants note: sync
# pyegeria calls are only safe from sync routes / apply_token, never async
# routes / a bare create_egeria_bearer_token()).

def _expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    from egeria_auth import apply_token
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


# ── Sheets held in Egeria (RS-DASH PR-3) ─────────────────────────────────────
# A Dashboard Sheet can live as an element chain in Egeria (pyegeria 6.2.29+: PR-2's reader turns it into
# a DashboardSheet) or in the JSON store. Egeria is read FIRST; the JSON store supplies every sheet name
# Egeria does not hold. Egeria wins by name. If Egeria cannot be reached, or the read fails, the JSON
# store answers alone and the response says so (`egeria.available: false` + the reason), never an empty
# list passed off as "no dashboards". Read only: nothing here writes to Egeria.
SOURCE_EGERIA = "egeria"
SOURCE_LOCAL = "local file"


class _EgeriaUnavailable(Exception):
    """Egeria sheets could not be read; the message is shown to the person."""


def _egeria_client(url=None, server=None, user_id=None, user_pwd=None):
    """Sync EgeriaTech client for the PR-2 reader, signed in with the request's token (or the configured
    user). For sync routes only (apply_token runs the sync token call)."""
    from pyegeria import EgeriaTech
    import pyegeria
    from egeria_auth import apply_token
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = EgeriaTech(server, url, user_id, user_pwd)
    apply_token(mgr)
    return mgr


def _egeria_identity(url, server, user_id, user_pwd) -> Optional[str]:
    """Cache-key part for this request: result_cache.request_identity (the presented credential, hashed) +
    platform/server + the forLineage toggle. None when the token has expired: the caller must then neither
    read nor fill its cache, so the request reaches Egeria and is refused."""
    from egeria_auth import lineage_key
    ident = request_identity(user_id, user_pwd)
    return None if ident is None else f"{ident}|{url}|{server}{lineage_key()}"


def _keyed(prefix, url, server, user_id, user_pwd) -> Optional[str]:
    ident = _egeria_identity(url, server, user_id, user_pwd)
    return None if ident is None else f"{prefix}|{ident}"


_TOKEN_EXPIRED = "Egeria token expired; sign in again"


def _reject_expired_token() -> None:
    """401 for a presented token whose exp has passed, before any cache or Egeria call: the page mints a
    new token for its own user. No token at all is not refused here (the Portal's service user answers)."""
    from egeria_auth import _token_expired, get_request_token
    token = get_request_token()
    if token and _token_expired(token):
        raise HTTPException(status_code=401, detail=_TOKEN_EXPIRED)


def _raise_if_token_refused(exc: Exception) -> None:
    """Egeria refused the CALLER's token (401/403): say so, never degrade to the JSON store as if Egeria
    were merely down. The service user's own failures (no token) keep degrading."""
    from egeria_auth import get_request_token
    from egeria_error_mapping import raise_if_auth_error
    if get_request_token():
        raise_if_auth_error(exc)


def _require_token_user() -> str:
    """The signed-in user of a write: a real, unexpired X-Egeria-Token, never the Portal's service user."""
    from egeria_auth import _token_expired, get_request_token, token_user
    token = get_request_token()
    if not token:
        raise HTTPException(status_code=401, detail="Sign in to change Dashboard Sheets: a change is made "
                                                    "as your own Egeria user, never the Portal's service user.")
    if _token_expired(token):
        raise HTTPException(status_code=401, detail=_TOKEN_EXPIRED)
    user = token_user()
    if not user:
        raise HTTPException(status_code=401, detail="The sign-in token names no user; sign in again")
    _verify_token_with_egeria(token, user)
    return user


def _verify_token_with_egeria(token: str, user: str) -> None:
    """token_user() reads the JWT WITHOUT checking its signature, so a hand-made token with a future exp
    would pass. Before a write, let Egeria check it: one cheap read (my profile, ~0.6 s) as that token.
    A refused token is a 401. "No profile" proves Egeria accepted the token: pyegeria returns its
    NO_ELEMENTS_FOUND marker for it, or raises PyegeriaNotFoundException on an HTTP 404 -- matched by that
    class and its 404 status only, never by text in a message. Anything else (Egeria unreachable, an
    unexpected error) refuses the write with 503 -- fail closed, never "unverified but OK".
    Sync: this runs in sync routes only (see CLAUDE.md's async invariants)."""
    from egeria_auth import check_client_platform, use_token
    from egeria_error_mapping import _is_auth_error
    import pyegeria
    from pyegeria import MyProfile, PyegeriaNotFoundException
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    try:
        client = MyProfile(os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
                           os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
                           user_id=user, user_pwd=None)
        check_client_platform(client, token)
        use_token(client, token)          # no password on the client: a 401 can never re-login as anyone
        client.get_my_profile()           # returns NO_ELEMENTS_FOUND (no exception) for a user with no profile
    except PyegeriaNotFoundException as exc:
        if getattr(exc, "response_code", None) == 404:
            return                        # HTTP 404 from Egeria: it accepted the token; no profile for this user
        _refuse_unverified(user, exc)
    except Exception as exc:  # noqa: BLE001
        if _is_auth_error(exc):
            raise HTTPException(status_code=401, detail="Egeria refused the sign-in token; sign in again")
        _refuse_unverified(user, exc)


def _refuse_unverified(user: str, exc: Exception) -> None:
    logger.warning(f"local-dashboards: could not verify the token of {user!r}: {exc}")
    raise HTTPException(status_code=503, detail="Could not check your sign-in with Egeria, so nothing "
                                                "was changed; try again shortly")


class _Listing(dict):
    """{name: EgeriaDashboardSheet}, plus how pyegeria read them (LD-1's DashboardSheetListing): `notes`, and
    `folders`, one entry per configured dashboard folder (qualifiedName, status "read" / "partial" /
    "not found" / "not read", reason, sheets). An older reader's plain list has neither: empty here."""
    def __init__(self, sheets=(), notes=None, folders=None):
        super().__init__((s.name, s) for s in sheets)
        self.notes = list(notes or [])
        self.folders = [dict(f) for f in (folders or [])]


def _configured_folders() -> list:
    """The dashboard folders the Portal lists from: pyegeria's configured_dashboard_folders()
    (PYEGERIA_DASHBOARD_FOLDERS, else config.json "Pyegeria Dashboard Folders"); empty means unscoped."""
    try:
        from pyegeria.view.dashboards import configured_dashboard_folders
        return list(configured_dashboard_folders())
    except Exception:  # noqa: BLE001 -- an older pyegeria: read the same variable directly
        return [p.strip() for p in (os.getenv("PYEGERIA_DASHBOARD_FOLDERS") or "").split(",") if p.strip()]


def _egeria_sheets(url=None, server=None, user_id=None, user_pwd=None) -> "_Listing":
    """The sheets Egeria holds in the configured dashboard folders (all Dashboard:: sheets when none are
    configured), as a _Listing. Raises _EgeriaUnavailable (never caches a failure). Cached _CACHE_TTL s per
    presented credential + platform/server + forLineage toggle: listing is per viewer."""
    ckey = _keyed("egeria-sheets", url, server, user_id, user_pwd)
    hit = _cache_get(ckey) if ckey else None
    if hit is not None:
        return hit
    try:
        from pyegeria.view.dashboards import list_dashboard_sheets
        sheets = list_dashboard_sheets(_egeria_client(url, server, user_id, user_pwd))
    except Exception as exc:  # noqa: BLE001
        _raise_if_token_refused(exc)
        logger.warning(f"local-dashboards: Egeria sheets unavailable: {exc}")
        raise _EgeriaUnavailable(f"{type(exc).__name__}: {' '.join(str(exc).split())[:240]}") from exc
    found = _Listing(sheets, getattr(sheets, "notes", None), getattr(sheets, "folders", None))
    return _cache_put(ckey, found) if ckey else found


def _consumer_index(url=None, server=None, user_id=None, user_pwd=None) -> dict:
    """pyegeria's dashboard consumer index ({sheet: [consumer, ...]} over RootCollection::DashboardSheets),
    for the "Used by" chips. Never raises: a failure is status "not read" with the reason, never an empty
    index passed off as "used by none". Only a clean read ("read" / "partial") is cached."""
    ckey = _keyed("egeria-consumers", url, server, user_id, user_pwd)
    hit = _cache_get(ckey) if ckey else None
    if hit is not None:
        return hit
    try:
        from pyegeria.view.dashboards import read_dashboard_consumer_index
        idx = read_dashboard_consumer_index(_egeria_client(url, server, user_id, user_pwd))
    except Exception as exc:  # noqa: BLE001
        _raise_if_token_refused(exc)
        return {"status": "not read", "reason": f"could not be read: {' '.join(str(exc).split())[:240]}",
                "consumers": [], "index": {}}
    if not isinstance(idx, dict):
        return {"status": "not read", "reason": "pyegeria returned no index", "consumers": [], "index": {}}
    # Cache a clean answer: read, partial, or a root that is simply not there ("not found"); never a failure.
    clean = idx.get("status") in ("read", "partial") or "not found" in str(idx.get("reason") or "")
    if clean and ckey:
        _cache_put(ckey, idx)
    return idx


def _consumer_display(name: str, consumers: dict) -> str:
    """One consumer, one name. The consumer index names a consumer by its folder's display name ("Egeria
    Advisor"); pyegeria's folder-scoped listing tags a sheet found in a SUB-folder with the qualifiedName
    segment instead ("EgeriaAdvisor"). Map the segment to the index's display name, so a chip or a filter
    never shows one consumer twice. A name the index does not know is kept as it is."""
    for c in consumers.get("consumers") or []:
        if not isinstance(c, dict):
            continue
        qn = c.get("qualifiedName") or ""
        segment = qn.split("::")[2] if qn.count("::") >= 2 else None
        if name and name in (c.get("name"), segment) and c.get("name"):
            return c["name"]
    return name


def _used_by(sheet, source: str, consumers: dict) -> dict:
    """A list row's "Used by": the consumers whose dashboard folders hold the sheet. `usedBy` is a list only
    when it is known; `usedByState` says how it was read ("read" / "partial" / "not read" / "not tracked")."""
    if source != SOURCE_EGERIA:
        return {"usedBy": None, "usedByState": "not tracked",
                "usedByReason": "a sheet in the local file is in no Egeria folder"}
    st = consumers.get("status")
    if st in ("read", "partial"):
        names = list((consumers.get("index") or {}).get(sheet.name) or [])
        own = [_consumer_display(n, consumers) for n in (getattr(sheet, "used_by", None) or [])]
        return {"usedBy": sorted(set(names) | set(own)),
                "usedByState": st, "usedByReason": consumers.get("reason")}
    own = list(getattr(sheet, "used_by", None) or [])
    if own:     # the folder-scoped listing found it in a consumer folder: that much is known
        return {"usedBy": sorted(own), "usedByState": "partial",
                "usedByReason": "the consumer index was not read (" + str(consumers.get("reason") or "unknown")
                                + "); shown: the configured folders it was found in"}
    return {"usedBy": None, "usedByState": "not read", "usedByReason": consumers.get("reason")}


def _egeria_one(name, url=None, server=None, user_id=None, user_pwd=None):
    """The one Egeria-held sheet `name`, or None. Raises _EgeriaUnavailable (a failure is never cached; a
    clean "Egeria does not hold it" is, for _CACHE_TTL s). Walks one chain: ~0.1 s for a name Egeria does not
    hold, against ~3 s per held sheet for the full list, so the detail route uses this, not the list."""
    ckey = _keyed(f"egeria-sheet|{name}", url, server, user_id, user_pwd)
    hit = _cache_get(ckey) if ckey else None
    if hit is not None:
        return None if hit is _MISS else hit
    lkey = _keyed("egeria-sheets", url, server, user_id, user_pwd)
    listed = _cache_get(lkey) if lkey else None
    if listed is not None and name in listed:
        found = listed[name]       # a miss is not "Egeria does not hold it": the list may be folder-scoped
    else:
        try:
            from pyegeria.view.dashboards import load_dashboard_sheet
            found = load_dashboard_sheet(name, _egeria_client(url, server, user_id, user_pwd))
        except Exception as exc:  # noqa: BLE001
            _raise_if_token_refused(exc)
            logger.warning(f"local-dashboards: Egeria sheet {name!r} unavailable: {exc}")
            raise _EgeriaUnavailable(f"{type(exc).__name__}: {' '.join(str(exc).split())[:240]}") from exc
    if ckey:
        _cache_put(ckey, found if found is not None else _MISS)
    return found


class _MergedSheets:
    """Egeria-held sheets first, then the JSON store's sheets for names Egeria does not hold.
    `.get` takes a name or an alias, like DashboardSheetDict; `source_of` labels a sheet."""
    def __init__(self, egeria: dict, local, loader=None):
        self.egeria = dict(egeria or {})
        self.local = local
        self._loader = loader      # name -> Egeria sheet or None, for names (nested sheets) not loaded yet
        self._alias = {a: s for s in self.egeria.values() for a in (getattr(s, "aliases", None) or [])}

    def get(self, name):
        """Egeria wins by NAME. An Egeria sheet's alias is only a fallback, after a local sheet of that name:
        the list shows every local sheet whose name Egeria does not hold, so a local sheet named like an
        Egeria alias is listed AND opens as itself (list and open agree), never as the Egeria sheet."""
        s = self.egeria.get(name)
        if s is None and self._loader is not None:
            s = self._loader(name)
            if s is not None:
                self.egeria[s.name] = s
        if s is None:
            s = self.local.get(name) or self._alias.get(name)
        return s

    def source_of(self, sheet) -> str:
        return SOURCE_EGERIA if self.egeria.get(getattr(sheet, "name", None)) is sheet else SOURCE_LOCAL

    def values(self):
        yield from self.egeria.values()
        for s in self.local.values():
            if s.name not in self.egeria:
                yield s

    def __len__(self):
        return sum(1 for _ in self.values())


def _egeria_fingerprint(name, url=None, server=None, user_id=None, user_pwd=None) -> str:
    """A short digest of the Egeria-held sheet `name` as just read (cached _CACHE_TTL s by _egeria_one), "-" when
    Egeria does not hold it, "down" when it could not be read. Part of the built-sheet cache key, so an
    edit in Egeria changes the key within a minute instead of waiting out the built sheet's own TTL."""
    import hashlib
    try:
        sheet = _egeria_one(name, url, server, user_id, user_pwd)
    except _EgeriaUnavailable:
        return "down"
    if sheet is None:
        return "-"
    try:
        body = sheet.model_dump_json()
    except Exception:  # noqa: BLE001
        body = repr(sheet)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def _merged_sheet_for(name, url=None, server=None, user_id=None, user_pwd=None):
    """Like _merged_sheets, for ONE sheet: reads just `name` from Egeria (nested sheets load lazily)."""
    local = _load_sheets()
    status = {"available": True}

    def loader(n):
        try:
            return _egeria_one(n, url, server, user_id, user_pwd)
        except _EgeriaUnavailable as exc:
            status.update(available=False, error=str(exc))
            return None
    first = loader(name)
    merged = _MergedSheets({first.name: first} if first is not None else {}, local, loader)
    return merged, status


def _merged_sheets(url=None, server=None, user_id=None, user_pwd=None):
    """(_MergedSheets, egeria_status). egeria_status is {"available": True} or
    {"available": False, "error": ...}; the JSON store failing still raises."""
    local = _load_sheets()
    try:
        listing = _egeria_sheets(url, server, user_id, user_pwd)
    except _EgeriaUnavailable as exc:
        return _MergedSheets({}, local), {"available": False, "error": str(exc), "configuredFolders": _configured_folders()}
    return _MergedSheets(listing, local), {"available": True, "configuredFolders": _configured_folders(),
                                           "folders": listing.folders, "notes": listing.notes}


def _flatten_property_value_map(pvm: dict) -> dict:
    """Un-nest Egeria's typed propertyValueMap into plain {name: value} pairs
    -- primitives pass through as strings; a nested Map property (e.g.
    additionalProperties) recurses via propertiesAsStrings, which pyegeria
    already provides pre-flattened."""
    out = {}
    for name, v in (pvm or {}).items():
        if not isinstance(v, dict):
            out[name] = v
            continue
        cls = v.get("class")
        if cls == "MapTypePropertyValue":
            out[name] = dict((v.get("mapValues") or {}).get("propertiesAsStrings") or {})
        else:
            out[name] = v.get("primitiveValue")
    return out


def _report_ckey(name, url, server, user_id, user_pwd) -> Optional[str]:
    """Cache key of one Report lookup: the PRESENTED credential (hashed), platform/server and the
    forLineage toggle, never a bare user_id: what a user may see in Egeria differs per user."""
    return _keyed(f"report|{name}", url, server, user_id, user_pwd)


def _find_report_by_name(name: str, mgr, url=None, server=None, user_id=None, user_pwd=None) -> Optional[dict]:
    """Look up a `Report` element by exact display name. Returns a dict with
    guid/heading/description/reportSpec/outputFormat/params, or None if not
    found (or on any lookup failure -- best-effort, never raises).

    Cached for _CACHE_TTL seconds per (name, url, server, user_id) -- this is
    otherwise a live Egeria find call per Report-typed placement, per page
    load (BACKLOG.md NEXT-22). url/server/user_id are for cache-key scoping
    only (mgr already carries the resolved connection); a stale hit within
    the TTL simply means a Report renamed/reconfigured via Dr.Egeria can take
    up to _CACHE_TTL seconds to show up here, same tradeoff overview_handler.py
    already accepts for its own cached endpoints.

    A miss is NOT cached (B5): on Egeria 8840035f a search can miss a Report whose same-named twin was
    deleted, so a miss may be false, and pinning it would hide the Report for a minute. A sheet with a
    missing placement is already kept in the short-lived degraded sheet cache (_SHEET_DEGRADED), which
    bounds how often a real miss is searched again."""
    ckey = _report_ckey(name, url, server, user_id, user_pwd)
    if ckey is None:            # expired token: no read, no fill, so Egeria decides
        return _find_report_by_name_uncached(name, mgr)
    cached = _cache_get(ckey)
    if cached is not None:
        return cached
    result = _find_report_by_name_uncached(name, mgr)
    if result is not None:
        _cache_put(ckey, result)
    return result


#: Page size of the by-name Report search. Egeria 8840035f answers a small page wrongly (a page of 1 says
#: "No elements found" though a match exists; a page of 5 can miss a Report whose same-named twin was
#: deleted), so ask for 25 and filter on the exact name below.
_REPORT_SEARCH_PAGE = 25


def _find_report_by_name_uncached(name: str, mgr) -> Optional[dict]:
    try:
        results = mgr.find_metadata_elements_with_string(
            search_string=name, starts_with=False, ends_with=False, ignore_case=False,
            metadata_element_type="Report", page_size=_REPORT_SEARCH_PAGE,
            graph_query_depth=0,  # PY-6/PY-14 perf lesson — only flat propertyValueMap fields read below;
                                  # this method's default (5) is worse than the usual 3.
        )
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"local-dashboards: Report lookup failed for {name!r}: {exc}")
        return None
    if not isinstance(results, list):
        return None
    for el in results:
        if not isinstance(el, dict):
            continue
        pvm = (el.get("elementProperties") or {}).get("propertyValueMap") or {}
        props = _flatten_property_value_map(pvm)
        if props.get("displayName") != name:
            continue
        extra = props.get("additionalProperties") or {}
        analytic_params = {}
        raw_analytic_params = extra.get("analyticParams")
        if raw_analytic_params:
            try:
                decoded = json.loads(raw_analytic_params)
                if isinstance(decoded, dict):
                    analytic_params = decoded
            except (TypeError, ValueError):
                logger.debug(f"local-dashboards: unparseable analyticParams for {name!r}: {raw_analytic_params!r}")
        return {
            "guid":        el.get("elementGUID"),
            "heading":     props.get("displayName") or name,
            "description": props.get("description") or "",
            "reportSpec":  extra.get("reportSpec"),
            "outputFormat": extra.get("outputFormat"),
            "analyticParams": analytic_params,
            "params":      {k: v for k, v in extra.items()
                             if k not in ("reportSpec", "outputFormat", "analyticParams")},
        }
    return None


def _prime_report_lookups(placements, url, server, user_id, user_pwd, max_workers: int = 6) -> None:
    """Look up the sheet's Reports CONCURRENTLY, filling _find_report_by_name's cache before the (serial)
    serialisation below reads it. Each lookup is a live Egeria find of 3-5 s, and they ran one after
    another: a four-placement sheet took ~18 s on the cold path (RS-DASH PR-3 measurement), the Report
    lookups being nearly all of it. Each worker has its OWN client (a sync pyegeria client is not safe to
    share across threads) and runs in a copy of the request context, so the token and the forLineage
    toggle travel with it and the cache key is the same one the serial path uses. Best-effort: a worker
    that fails leaves the cache empty and the serial path retries that one."""
    if _report_ckey("", url, server, user_id, user_pwd) is None:
        return              # expired token: nothing is cached for it, priming would only repeat the work
    ckey_of = lambda n: _report_ckey(n, url, server, user_id, user_pwd)
    names = []
    for p in placements:
        if getattr(p, "content", None) or (getattr(p, "kind", None) == "missing" and getattr(p, "note", None)):
            continue
        if p.ref not in names and _cache_get(ckey_of(p.ref)) is None:
            names.append(p.ref)
    if len(names) < 2:
        return
    from concurrent.futures import ThreadPoolExecutor

    def _one(name):
        client = None
        try:
            client = _expert(url, server, user_id, user_pwd)
            _find_report_by_name(name, client, url, server, user_id, user_pwd)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"local-dashboards: concurrent Report lookup failed for {name!r}: {exc}")
        finally:
            if client is not None:      # this worker's own client: close its HTTP session, never leak it
                try:
                    client.close_session()
                except Exception as exc:  # noqa: BLE001
                    logger.debug(f"local-dashboards: closing a lookup client failed: {exc}")

    with ThreadPoolExecutor(max_workers=min(max_workers, len(names)), thread_name_prefix="report-lookup") as pool:
        for n in names:
            pool.submit(contextvars.copy_context().run, _one, n)


def _serialize_placement(p, sheets, registry, mgr, url=None, server=None, user_id=None,
                         resolutions=None, user_pwd=None) -> dict:
    # A text placement (Dr.Egeria "Add Text on Dashboard Sheet") carries its
    # content inline -- no Egeria lookup needed at all, so check it before
    # attempting a Report/Sheet resolution (which would otherwise treat a
    # text placement's own Placement Name as an unresolved "missing" ref).
    if getattr(p, "content", None):
        return _text_placement(p, p.content)
    if getattr(p, "kind", None) == "missing" and getattr(p, "note", None):
        # An Egeria-held placement whose report link is gone (resolver fallback only): the reader's own words.
        return _missing_placement(p, p.note)
    report = _find_report_by_name(p.ref, mgr, url, server, user_id, user_pwd) if mgr is not None else None
    if report is not None:
        return _report_placement(p, report, registry, resolutions)
    sub = sheets.get(p.ref)
    if sub is not None:
        return {
            "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "sheet",
            "heading": sub.heading, "description": sub.description or "",
            "perspectives": list(getattr(p, "perspectives", None) or []),
        }
    return _missing_placement(p, "Unresolved reference — no matching Report or Dashboard Sheet.")


def _text_placement(p, content) -> dict:
    return {
        "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "text",
        "heading": p.ref, "content": content,
        "perspectives": list(getattr(p, "perspectives", None) or []),
    }


def _missing_placement(p, description) -> dict:
    return {
        "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "missing",
        "heading": p.ref, "description": description,
        "perspectives": list(getattr(p, "perspectives", None) or []),
    }


def _report_placement(p, report: dict, registry, resolutions) -> dict:
    """A kind:"report" placement from its Report (the dict _find_report_by_name_uncached returns, or the same
    shape built from pyegeria's resolver), so both paths serialise a report identically."""
    fs = registry.get(report["reportSpec"]) if report["reportSpec"] else None
    action = getattr(fs, "action", None) if fs is not None else None
    return {
        "ref":            p.ref,
        "span":           p.span,
        "emphasis":       p.emphasis,
        "kind":           "report",
        "heading":        report["heading"],
        "description":    report["description"] or (getattr(fs, "description", None) if fs else "") or "",
        "reportSpec":     report["reportSpec"],
        "outputFormat":   report["outputFormat"],
        "params":         report["params"],
        "analyticParams": report["analyticParams"],
        "family":         getattr(fs, "family", None) if fs else None,
        "outputTypes":    sorted({str(t) for fmt in (getattr(fs, "formats", []) or [])
                                   for t in (getattr(fmt, "types", []) or [])}) if fs else [],
        "requiredParams": list(getattr(action, "required_params", []) or []) if action else [],
        # True iff the underlying FormatSet's action runs an analytic function
        # (extra_find) rather than a live find-method query -- the frontend uses
        # this, not outputFormat=='SERIES', to decide whether to send
        # analyticParams or the standard find-vocabulary params. SERIES is one
        # possible rendering of an analytic result (a chart), not the signal
        # for "this is analytic" -- an analytic function can render as DICT/JSON
        # too (see analytic_demo_specs.py's count_elements demos), and using
        # outputFormat as the proxy silently sent search_string/graphQueryDepth
        # etc. to functions that don't accept them (TypeError: unexpected
        # keyword argument 'search_string').
        "isAnalytic":     bool(getattr(action, "analytic_function", None)) if action else False,
        "perspectives":   list(getattr(p, "perspectives", None) or []),
        # BACKLOG.md NEXT-21 (egeria-workspaces-fs) -- drill-down target,
        # a Report Spec name for local-dashboards.html to run in the
        # detail drawer. getattr, not p.detail_spec, so this degrades to
        # None on the currently-deployed pyegeria (predates this field)
        # instead of raising AttributeError and taking the whole sheet down.
        "detailSpec":     getattr(p, "detail_spec", None),
        # RS-W2-4: runnable (True/False, None = not resolved) and refusal (the resolver's
        # words when not runnable). The page shows the refusal instead of executing.
        **spec_resolution.placement_status(report["reportSpec"], resolutions or {},
                                            report["analyticParams"], action),
    }


# ── pyegeria's shared dashboard data step (B4 / D4, Portal-2) ────────────────
# A sheet held in Egeria is resolved by pyegeria's resolver (pyegeria.view.dashboard_resolver, the same
# data step Egeria Advisor uses), and only by it: every placement's kind, Report and words come from the
# resolver. It reads each Report by the GUID its placement links to, as the viewer, concurrently, and says
# when a Report or an EGERIA-tier ReportSpec is in a zone the viewer cannot see (kind "restricted", "not
# visible to you"), which a lookup by name cannot: Egeria drops such an element from searches without a
# word. The Portal keeps the sheet read (cached, fingerprinted), the caches and the serialised shape.
#
# resolve_sheet, not resolve_dashboard_sheet: the same data step, given the sheet the Portal has ALREADY
# read as this viewer (_egeria_one, cached and part of the built-sheet key), so the chain is not walked twice.
#
# The by-name path above is for sheets in the local file (no GUIDs to read by), and for an Egeria-held sheet
# only when the resolver fails as a whole (a refused token is raised, never degraded).
RESTRICTED_REASON = "not visible to you"
EMPTY_TEXT = "text placement with no content"


def _resolve_sheet(client, sheet, **kw):
    """pyegeria's resolver (pyegeria>=6.2.40 is the floor, so it is always there)."""
    from pyegeria.view.dashboard_resolver import resolve_sheet
    return resolve_sheet(client, sheet, **kw)


def _spec_lookup(registry):
    """The resolver's spec lookup: the Portal's own registry (as the by-name path uses it), plus pyegeria's
    spec_source, whose GUID lets the resolver re-check an EGERIA-tier spec as the viewer."""
    try:
        from pyegeria.view.base_report_formats import report_spec_source
    except ImportError:
        report_spec_source = None

    def lookup(label):
        fs = registry.get(label) if label else None
        if fs is None:
            return None, None
        try:
            return fs, (report_spec_source(label) if report_spec_source else None)
        except Exception as exc:  # noqa: BLE001 -- the source tag is extra; the spec was found
            logger.debug(f"local-dashboards: no spec_source for {label!r}: {exc}")
            return fs, None
    return lookup


def _resolve_egeria_sheet(sheet, perspective, registry, resolutions, url, server, user_id, user_pwd):
    """The serialised placements of an Egeria-held sheet, all from pyegeria's resolver, in sheet order for
    `perspective`; or None when the resolver failed as a whole, or answered for other placements than the
    sheet's (the caller then resolves every placement by name). A refused token is raised, never swallowed."""
    try:
        resolved = _resolve_sheet(_egeria_client(url, server, user_id, user_pwd), sheet,
                                  perspective=perspective, spec_lookup=_spec_lookup(registry))
    except Exception as exc:  # noqa: BLE001
        _raise_if_token_refused(exc)
        logger.warning(f"local-dashboards: pyegeria's sheet resolver failed for {sheet.name!r}, "
                       f"resolving by name instead: {exc}")
        return None
    position = {id(p): i for i, p in enumerate(sheet.placements, start=1)}
    visible = _view_for_perspective(sheet.placements, perspective)
    by_position = {rp.position: rp for rp in resolved.placements}
    if len(by_position) != len(visible):
        logger.warning(f"local-dashboards: the resolver answered {len(by_position)} placements of "
                       f"{sheet.name!r} for {len(visible)} shown; resolving by name instead")
        return None
    out = []
    for p in visible:
        rp = by_position.get(position[id(p)])
        if rp is None or rp.ref != p.ref:
            logger.warning(f"local-dashboards: the resolver's placements of {sheet.name!r} do not match the "
                           f"sheet's (at {p.ref!r}); resolving by name instead")
            return None
        out.append(_from_resolved(p, rp, registry, resolutions))
    return out


def _from_resolved(p, rp, registry, resolutions) -> dict:
    """One placement, serialised from the resolver's answer: the same dicts the by-name path makes."""
    if rp.kind == "restricted":
        return _restricted_placement(p, rp)
    if rp.kind == "report" and rp.report is not None:
        return _report_placement(p, _report_from_resolved(rp, p), registry, resolutions)
    if rp.kind == "text" and rp.content:
        return _text_placement(p, rp.content)
    # "missing" in the resolver's words: the reader's own (a report link gone) or the Report no longer in
    # Egeria. A text placement with no content says so in words, never as an empty tile.
    reason = rp.reason or rp.note or (EMPTY_TEXT if rp.kind == "text" else None) or "not resolved"
    return _missing_placement(p, reason)


def _report_from_resolved(rp, p) -> dict:
    r = rp.report
    return {"guid": r.guid, "heading": r.name or p.ref, "description": r.description or "",
            "reportSpec": r.report_spec, "outputFormat": r.output_format,
            "analyticParams": dict(r.analytic_params or {}), "params": dict(r.params or {})}


def _restricted_placement(p, rp) -> dict:
    return {
        "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "restricted",
        "heading": p.ref, "restricted": True, "restrictedElement": rp.restricted_element,
        "reason": rp.reason or RESTRICTED_REASON,
        "description": f"{'Report spec' if rp.restricted_element == 'ReportSpec' else 'Report'} "
                       f"{rp.reason or RESTRICTED_REASON}.",
        "perspectives": list(getattr(p, "perspectives", None) or []),
    }


@router.get("/local-dashboards", include_in_schema=False)
def serve_local_dashboards():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Local Dashboards page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


@router.get("/api/local-dashboards", summary="List Dashboard Sheets (Egeria-held first, then the local store)")
def list_local_dashboards(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
):
    # Auth is the X-Egeria-Token header only (EgeriaTokenMiddleware); with none, the Portal's service user
    # from the environment. No user_id/user_pwd query params: a password in a URL lands in access logs,
    # and a bare user_id would sign in as that user with the service password.
    _reject_expired_token()
    try:
        sheets, egeria_status = _merged_sheets(url, server, None, None)
    except HTTPException:
        raise                   # a refused token is a 401/403, not "store unavailable"
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to load store")
        raise HTTPException(status_code=500, detail=f"Dashboard Sheet store unavailable: {exc}")
    consumers = (_consumer_index(url, server, None, None) if egeria_status.get("available")
                 else {"status": "not read", "reason": "Egeria could not be read", "consumers": [], "index": {}})
    rows = []
    for s in sheets.values():
        src = sheets.source_of(s)
        row = {"name": s.name, "heading": s.heading, "description": s.description,
               "family": s.family, "placementCount": len(s.placements),
               "source": src, "breaks": list(getattr(s, "breaks", None) or []),
               "folders": list(getattr(s, "folders", None) or []) if src == SOURCE_EGERIA else []}
        row.update(_used_by(s, src, consumers))
        rows.append(row)
    return JSONResponse({
        "sheets": rows,
        "storePath": _store_path(),
        "total": len(sheets),
        "egeria": egeria_status,
        # How the "Used by" index was read ("read" | "partial" | "not read" + reason) and its consumers.
        "consumers": {"status": consumers.get("status"), "reason": consumers.get("reason"),
                      "root": consumers.get("root"),
                      "consumers": [{"name": c.get("name"), "status": c.get("status"), "sheets": c.get("sheets")}
                                    for c in (consumers.get("consumers") or []) if isinstance(c, dict)]},
    })


# ── Shared Dr.Egeria document library ────────────────────────────────────────
# Registered BEFORE /api/local-dashboards/{name} — FastAPI/Starlette matches
# routes in registration order, and {name} would otherwise swallow the literal
# "documents" segment as a (nonexistent) sheet name.

@router.get("/api/local-dashboards/documents",
            summary="List shared Dr.Egeria dashboard-definition documents")
def list_documents():
    """Files in the read-only shared folder — a curated place to drop
    `.dr-egeria.md` files that define/update Dashboard Sheets, browsable from
    the Run Dr.Egeria Document panel instead of pasting content by hand."""
    if not _DOCS_DIR.is_dir():
        return JSONResponse({"documents": [], "docsPath": str(_DOCS_DIR),
                             "error": "Folder not found — is the loading-bay volume mounted?"})
    docs = []
    for p in sorted(_DOCS_DIR.glob("*.md")):
        try:
            stat = p.stat()
            docs.append({"filename": p.name, "size": stat.st_size, "modified": stat.st_mtime})
        except OSError:
            continue
    return JSONResponse({"documents": docs, "docsPath": str(_DOCS_DIR), "total": len(docs)})


@router.get("/api/local-dashboards/documents/{filename}",
            summary="Raw content of one shared Dr.Egeria document")
def get_document(filename: str):
    # Reject path separators / traversal — filename must be a plain basename
    # within _DOCS_DIR, nothing else in the read-only loading-bay tree.
    if "/" in filename or "\\" in filename or filename in (".", ".."):
        raise HTTPException(status_code=400, detail="Invalid filename")
    docs_root = _DOCS_DIR.resolve()
    path = (docs_root / filename).resolve()
    try:
        if not path.is_relative_to(docs_root) or path.parent != docs_root or not path.is_file():
            raise HTTPException(status_code=404, detail=f"Document {filename!r} not found")
        content = path.read_text(encoding="utf-8")
    except HTTPException:
        raise
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read {filename!r}: {exc}")
    return JSONResponse({"filename": filename, "content": content})


def _view_for_perspective(placements, perspective: Optional[str]):
    """Filter+keep-order a Dashboard Sheet's placements for `perspective`
    (BACKLOG.md NEXT-19, egeria-workspaces-fs) -- mirrors
    overview_containers.view_for_perspective()'s shape exactly: a placement
    with no perspectives declared is kept regardless (empty means "relevant
    to every perspective", fail-open, same as Overview's own sub-container
    handling), not hidden. No filtering at all when `perspective` is None/
    empty -- the default, unscoped view."""
    if not perspective:
        return placements
    return [p for p in placements
            if not (getattr(p, "perspectives", None) or [])
            or perspective in p.perspectives]


# ── Resolved-sheet cache ─────────────────────────────────────────────────────
# Resolving a sheet looks up every placement's Report by name in Egeria, uncached per sheet: about a
# minute on the CDO sheet even when every placement RESULT is already cached (result_cache). Cache the
# resolved sheet the same way: stale-while-revalidate, one refresh in flight, errors never cached.
# Key: sheet name, perspective, the store file's mtime (an edit, from anywhere, invalidates it), a digest of
# the Egeria-held sheet (an edit in Egeria invalidates it within _CACHE_TTL), the
# presented credential (hashed, see result_cache.credential_identity), platform/server, and the
# forLineage toggle. A degraded answer (no Egeria connection, or a placement that did not resolve) is
# kept in a SEPARATE cache with a short TTL (a permanently broken placement would otherwise cost the
# full resolve on every visit, a transient failure is not pinned for minutes), is never served stale,
# and a degraded refresh never replaces a good entry.
_SHEET_CACHE = ResultCache(
    ttl=float(os.environ.get("PORTAL_SHEET_CACHE_TTL", "300")),
    max_entries=int(os.environ.get("PORTAL_SHEET_CACHE_MAX", "64")))
_DEGRADED_TTL = float(os.environ.get("PORTAL_SHEET_DEGRADED_TTL", "60"))
_SHEET_DEGRADED = ResultCache(ttl=_DEGRADED_TTL, max_stale=_DEGRADED_TTL,
                              max_entries=int(os.environ.get("PORTAL_SHEET_CACHE_MAX", "64")))


def _sheet_lookup(key):
    """The good entry if there is one (fresh or stale), else a still-fresh degraded one."""
    state, body, at = _SHEET_CACHE.lookup(key)
    if state in (FRESH, STALE):
        return state, body, at
    state, body, at = _SHEET_DEGRADED.lookup(key)
    return (FRESH, body, at) if state == FRESH else (MISS, None, None)


def _store_mtime_ns() -> int:
    try:
        return os.stat(_store_path()).st_mtime_ns
    except OSError:
        return 0


def _build_sheet(name, perspective, url, server, user_id, user_pwd):
    """Resolve one sheet. Returns (payload, cacheable); raises the HTTPException the browser should see."""
    try:
        sheets, egeria_status = _merged_sheet_for(name, url, server, user_id, user_pwd)
    except HTTPException:
        raise                   # a refused token is a 401/403, not "store unavailable"
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to load store")
        raise HTTPException(status_code=500, detail=f"Dashboard Sheet store unavailable: {exc}")

    sheet = sheets.get(name)
    if sheet is None:
        if not egeria_status["available"]:
            raise HTTPException(status_code=503, detail=(
                f"Dashboard Sheet {name!r} is not in the local store, and Egeria could not be read, so it "
                f"may be held there: {egeria_status['error']}"))
        raise HTTPException(status_code=404, detail=f"Dashboard Sheet {name!r} not found")
    source = sheets.source_of(sheet)

    try:
        registry = _report_registry()
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: report spec registry unavailable")
        raise HTTPException(status_code=500, detail=f"Report spec registry unavailable: {exc}")

    # pyegeria's load-time resolution (cached); {} on a pyegeria without the resolver.
    resolutions = spec_resolution.resolve_all()

    placements = (_resolve_egeria_sheet(sheet, perspective, registry, resolutions, url, server, user_id, user_pwd)
                  if source == SOURCE_EGERIA else None)
    connected = True
    if placements is None:
        # By name: a sheet in the local file, or an Egeria-held one the resolver failed on. Best-effort: if
        # Egeria's unreachable, placements just fall through to "missing" rather than failing the whole
        # sheet — same degrade-don't-fail philosophy as overview_handler.py.
        try:
            mgr = _expert(url, server, user_id, user_pwd)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"local-dashboards: Egeria connection unavailable: {exc}")
            mgr = None
        connected = mgr is not None
        visible = _view_for_perspective(sheet.placements, perspective)
        if mgr is not None:
            _prime_report_lookups(visible, url, server, user_id, user_pwd)
        placements = [_serialize_placement(p, sheets, registry, mgr, url, server, user_id, resolutions, user_pwd)
                      for p in visible]
    for pl in placements:
        pl["source"] = source        # a placement is held where its sheet is
    payload = {
        "name":        sheet.name,
        "source":      source,
        "breaks":      list(getattr(sheet, "breaks", None) or []),
        "egeria":      egeria_status,
        "heading":     sheet.heading,
        "description": sheet.description,
        "family":      sheet.family,
        "placements":  placements,
        "perspective": perspective,
    }
    cacheable = connected and egeria_status["available"] and all(pl.get("kind") != "missing" for pl in placements)
    return payload, cacheable


def _sheet_response(body: bytes, state: str, stored_at: float) -> Response:
    from report_specs_handler import _stamp
    return Response(content=body, media_type="application/json",
                    headers={"X-Cache": state, **_stamp(stored_at)})


def _refresh_sheet(key, args) -> None:
    failed = False
    try:
        payload, cacheable = _build_sheet(*args)
        if cacheable:
            _SHEET_CACHE.put(key, JSONResponse(payload).body)
        else:
            failed = True       # never replace a good entry with a degraded one
    except Exception as exc:  # noqa: BLE001 -- the stale entry stays; nothing failed is cached
        failed = True
        logger.warning(f"local-dashboards: background refresh of {args[0]!r} failed: {exc}")
    finally:
        _SHEET_CACHE.release_refresh(key, failed=failed)


@router.get("/api/local-dashboards/{name}", summary="One Dashboard Sheet, placements resolved")
def get_local_dashboard(
    name: str,
    perspective: Optional[str] = Query(None, description="Keep only placements tagged with this "
                                        "perspective, plus any untagged ones (fail-open)."),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    refresh: bool = Query(False, description="Resolve now and store the result, ignoring the cache."),
):
    from egeria_auth import get_request_token, lineage_key
    user_id = user_pwd = None       # X-Egeria-Token header only (see list_local_dashboards); never from the URL
    _reject_expired_token()         # never served from (or stored in) the cache: refused before any read
    token = get_request_token()
    args = (name, perspective, url, server, user_id, user_pwd)
    identity = credential_identity(token, user_id, user_pwd, os.environ.get("EGERIA_USER", "erinoverview"))
    key = ("sheet", name, perspective, _store_mtime_ns(), _egeria_fingerprint(name, url, server, user_id, user_pwd),
           identity, url, server, lineage_key())

    if not refresh:
        state, body, stored_at = _sheet_lookup(key)
        if state == FRESH:
            return _sheet_response(body, "hit", stored_at)
        if state == STALE:
            if _SHEET_CACHE.claim_refresh(key):      # atomic: exactly one refresh in flight per key
                ctx = contextvars.copy_context()     # token and forLineage travel with it
                threading.Thread(target=ctx.run, args=(_refresh_sheet, key, args), daemon=True,
                                 name="sheet-refresh").start()
            return _sheet_response(body, "stale", stored_at)
        leader, flight = _SHEET_CACHE.begin_flight(key)
        if not leader:        # the same sheet is already being resolved: wait for it
            flight.event.wait(200.0)
            state, body, stored_at = _sheet_lookup(key)
            if state in (FRESH, STALE):
                return _sheet_response(body, "hit", stored_at)
            if flight.error is not None:
                raise flight.error
            leader, flight = False, None
    else:
        leader, flight = False, None
    error = None
    try:
        payload, cacheable = _build_sheet(*args)
        body = JSONResponse(payload).body
        # a good answer replaces anything; a degraded one is stored short-lived and only if no good entry exists
        if cacheable:
            stored_at = _SHEET_CACHE.put(key, body)
        elif _SHEET_CACHE.lookup(key)[0] == MISS:
            stored_at = _SHEET_DEGRADED.put(key, body)
        else:
            stored_at = time.time()
    except BaseException as exc:
        error = exc
        raise
    finally:
        if leader:
            _SHEET_CACHE.end_flight(key, flight, error)
    return _sheet_response(body, "refresh" if refresh else "miss", stored_at)


@router.delete("/api/local-dashboards/{name}", summary="Delete a Dashboard Sheet")
def delete_local_dashboard(name: str):
    """
    Delete a Dashboard Sheet from the local JSON store.

    Removes the Sheet and its own Placement list only -- never the
    underlying Egeria `Report` elements any placement referenced (a Report
    is an independent, reusable object that may be linked from other
    sheets too; deleting a sheet must not delete data other dashboards
    depend on). If some other sheet nests this one as a Placement
    (`kind: "sheet"`), that placement will render as "missing" on its next
    load -- the same graceful-degrade behavior every other unresolved
    reference already gets here, not a hard foreign-key constraint this
    endpoint enforces or blocks on.

    NOTE -- implementation will change when Dashboard Sheet becomes a real
    Egeria element: this store is local-JSON-only today (see this module's
    docstring / pyegeria's `_output_dashboard_sheet_models.py`), so "delete"
    here is just a dict pop + full-file rewrite, with no soft-delete,
    cascade, or audit trail. Once Dashboard Sheet migrates to an Egeria
    `Collection` subtype (planned, not yet started), this needs to become a
    real Egeria delete (e.g. `CollectionManager.delete_collection`) instead.
    Kept deliberately thin for that reason.

    Requires a signed-in user (a real, unexpired X-Egeria-Token): never the Portal's service user, so an
    anonymous request cannot delete anyone's sheet.
    """
    who = _require_token_user()
    try:
        sheets = _load_sheets()
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to load store")
        raise HTTPException(status_code=500, detail=f"Dashboard Sheet store unavailable: {exc}")

    sheet = sheets.get(name)
    if sheet is None:
        raise HTTPException(status_code=404, detail=f"Dashboard Sheet {name!r} not found")

    # sheets.get() resolves name-or-alias; delete by the sheet's own
    # canonical `.name` (the real dict key), not the possibly-aliased path
    # param, so deleting by an alias doesn't KeyError.
    del sheets[sheet.name]

    try:
        _save_sheets(sheets)
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to save store after delete")
        raise HTTPException(status_code=500, detail=f"Failed to persist deletion: {exc}")

    logger.info(f"local-dashboards: {who} deleted Dashboard Sheet {sheet.name!r}")
    return JSONResponse({"deleted": sheet.name})
