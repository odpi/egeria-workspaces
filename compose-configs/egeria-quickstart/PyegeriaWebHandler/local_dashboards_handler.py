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
from pathlib import Path
from typing import Optional

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


def _store_path() -> str:
    return os.path.expanduser(
        os.getenv("PYEGERIA_DASHBOARD_SHEETS_STORE", "~/.pyegeria/dashboard_sheets.json")
    )


def _load_sheets():
    from pyegeria.view._output_dashboard_sheet_models import DashboardSheetDict
    path = _store_path()
    if os.path.exists(path):
        return DashboardSheetDict.load_from_json(path)
    return DashboardSheetDict()


def _save_sheets(sheets) -> None:
    from pyegeria.view._output_dashboard_sheet_models import save_dashboard_sheets_to_json
    save_dashboard_sheets_to_json(sheets, _store_path())


def _report_registry() -> dict:
    from pyegeria.view.base_report_formats import get_report_registry
    return get_report_registry()


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


def _find_report_by_name(name: str, mgr) -> Optional[dict]:
    """Look up a `Report` element by exact display name. Returns a dict with
    guid/heading/description/reportSpec/outputFormat/params, or None if not
    found (or on any lookup failure -- best-effort, never raises)."""
    try:
        results = mgr.find_metadata_elements_with_string(
            search_string=name, starts_with=False, ends_with=False, ignore_case=False,
            metadata_element_type="Report", page_size=5,
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


def _serialize_placement(p, sheets, registry, mgr) -> dict:
    # A text placement (Dr.Egeria "Add Text on Dashboard Sheet") carries its
    # content inline -- no Egeria lookup needed at all, so check it before
    # attempting a Report/Sheet resolution (which would otherwise treat a
    # text placement's own Placement Name as an unresolved "missing" ref).
    if getattr(p, "content", None):
        return {
            "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "text",
            "heading": p.ref, "content": p.content,
        }
    report = _find_report_by_name(p.ref, mgr) if mgr is not None else None
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
        }
    sub = sheets.get(p.ref)
    if sub is not None:
        return {
            "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "sheet",
            "heading": sub.heading, "description": sub.description or "",
        }
    return {
        "ref": p.ref, "span": p.span, "emphasis": p.emphasis, "kind": "missing",
        "heading": p.ref,
        "description": "Unresolved reference — no matching Report or Dashboard Sheet.",
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
    path = _DOCS_DIR / filename
    try:
        if path.resolve().parent != _DOCS_DIR.resolve() or not path.is_file():
            raise HTTPException(status_code=404, detail=f"Document {filename!r} not found")
        content = path.read_text(encoding="utf-8")
    except HTTPException:
        raise
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read {filename!r}: {exc}")
    return JSONResponse({"filename": filename, "content": content})


@router.get("/api/local-dashboards/{name}", summary="One Dashboard Sheet, placements resolved")
def get_local_dashboard(
    name: str,
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
        "placements":  [_serialize_placement(p, sheets, registry, mgr) for p in sheet.placements],
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
