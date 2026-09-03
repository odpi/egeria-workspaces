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
import json
import os
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

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

# Sentinel so a cached "no Report found" result is distinguishable from
# "nothing cached yet" -- _find_report_by_name legitimately returns None for
# unresolved placements, and that negative result is worth caching too
# (otherwise a "missing" placement retries its failed lookup every request).
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


def _find_report_by_name(name: str, mgr, url=None, server=None, user_id=None) -> Optional[dict]:
    """Look up a `Report` element by exact display name. Returns a dict with
    guid/heading/description/reportSpec/outputFormat/params, or None if not
    found (or on any lookup failure -- best-effort, never raises).

    Cached for _CACHE_TTL seconds per (name, url, server, user_id) -- this is
    otherwise a live Egeria find call per Report-typed placement, per page
    load (BACKLOG.md NEXT-22). url/server/user_id are for cache-key scoping
    only (mgr already carries the resolved connection); a stale hit within
    the TTL simply means a Report renamed/reconfigured via Dr.Egeria can take
    up to _CACHE_TTL seconds to show up here, same tradeoff overview_handler.py
    already accepts for its own cached endpoints."""
    ckey = f"report|{name}|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return None if cached is _MISS else cached
    result = _find_report_by_name_uncached(name, mgr)
    _cache_put(ckey, result if result is not None else _MISS)
    return result


def _find_report_by_name_uncached(name: str, mgr) -> Optional[dict]:
    try:
        results = mgr.find_metadata_elements_with_string(
            search_string=name, starts_with=False, ends_with=False, ignore_case=False,
            metadata_element_type="Report", page_size=5,
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


def _serialize_placement(p, sheets, registry, mgr, url=None, server=None, user_id=None) -> dict:
    # A text placement (Dr.Egeria "Add Text on Dashboard Sheet") carries its
    # content inline -- no Egeria lookup needed at all, so check it before
    # attempting a Report/Sheet resolution (which would otherwise treat a
    # text placement's own Placement Name as an unresolved "missing" ref).
    if getattr(p, "content", None):
        return {
            "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "text",
            "heading": p.ref, "content": p.content,
            "perspectives": list(getattr(p, "perspectives", None) or []),
        }
    report = _find_report_by_name(p.ref, mgr, url, server, user_id) if mgr is not None else None
    if report is not None:
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
        }
    sub = sheets.get(p.ref)
    if sub is not None:
        return {
            "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "sheet",
            "heading": sub.heading, "description": sub.description or "",
            "perspectives": list(getattr(p, "perspectives", None) or []),
        }
    return {
        "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "missing",
        "heading": p.ref,
        "description": "Unresolved reference — no matching Report or Dashboard Sheet.",
        "perspectives": list(getattr(p, "perspectives", None) or []),
    }


@router.get("/local-dashboards", include_in_schema=False)
def serve_local_dashboards():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Local Dashboards page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


@router.get("/api/local-dashboards", summary="List locally-authored Dashboard Sheets")
def list_local_dashboards():
    try:
        sheets = _load_sheets()
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to load store")
        raise HTTPException(status_code=500, detail=f"Dashboard Sheet store unavailable: {exc}")
    return JSONResponse({
        "sheets": [
            {"name": s.name, "heading": s.heading, "description": s.description,
             "family": s.family, "placementCount": len(s.placements)}
            for s in sheets.values()
        ],
        "storePath": _store_path(),
        "total": len(sheets),
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


@router.get("/api/local-dashboards/{name}", summary="One Dashboard Sheet, placements resolved")
def get_local_dashboard(
    name: str,
    perspective: Optional[str] = Query(None, description="Keep only placements tagged with this "
                                        "perspective, plus any untagged ones (fail-open)."),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        sheets = _load_sheets()
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: failed to load store")
        raise HTTPException(status_code=500, detail=f"Dashboard Sheet store unavailable: {exc}")

    sheet = sheets.get(name)
    if sheet is None:
        raise HTTPException(status_code=404, detail=f"Dashboard Sheet {name!r} not found")

    try:
        registry = _report_registry()
    except Exception as exc:  # noqa: BLE001
        logger.exception("local-dashboards: report spec registry unavailable")
        raise HTTPException(status_code=500, detail=f"Report spec registry unavailable: {exc}")

    # Best-effort: if Egeria's unreachable, placements just fall through to
    # "missing" rather than failing the whole sheet — same degrade-don't-fail
    # philosophy as overview_handler.py.
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"local-dashboards: Egeria connection unavailable: {exc}")
        mgr = None

    return JSONResponse({
        "name":        sheet.name,
        "heading":     sheet.heading,
        "description": sheet.description,
        "family":      sheet.family,
        "placements":  [_serialize_placement(p, sheets, registry, mgr, url, server, user_id)
                         for p in _view_for_perspective(sheet.placements, perspective)],
        "perspective": perspective,
    })


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
    """
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

    logger.info(f"local-dashboards: deleted Dashboard Sheet {sheet.name!r}")
    return JSONResponse({"deleted": sheet.name})
