# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Local Dashboards — FastAPI router.

Browses user-authored Dashboard Sheets: the local-JSON-store model
(pyegeria.view._output_dashboard_sheet_models.DashboardSheet) built by the
Dr.Egeria `Create Dashboard Sheet` / `Link Report to Dashboard Sheet`
commands (egeria-python md_processing/v2/dashboard_sheet.py). Each Dashboard
Sheet is an ordered list of Placements, each referencing a Report Spec
(FormatSet, from pyegeria.view.base_report_formats) or another Dashboard
Sheet (nesting).

This is deliberately separate from egeria-overview.html's own Container
model (overview_containers.py): that one is the Overview app's own static
P0 KPI layout, resolved against overview_specs.SPECS (Python-computed tiles,
not stored ReportSpecs). Dashboard Sheets are the user-authored model —
different leaf type, different registry, different app.

Routes:
  GET /local-dashboards             → serve the SPA
  GET /api/local-dashboards         → list all Dashboard Sheets (summary)
  GET /api/local-dashboards/{name}  → one sheet, placements resolved against
                                       the report-spec registry (+ nested
                                       sheets resolved against the sheet store)

Rendering a placement reuses the existing POST /api/report-specs/execute
endpoint (report_specs_handler.py) — no new execution path. Only placements
whose report spec needs no required parameters can be auto-rendered by the
SPA; others surface their required params so the SPA can point at the full
Report Spec Browser (Egeria Explorer) instead of guessing values (see
OVERVIEW_REPORTING_MODEL.md §10 "NEXT-10 P3" for why a generic
per-placement-params execution engine doesn't exist yet).
"""
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

router = APIRouter(tags=["local-dashboards"])

_HERE = Path(__file__).parent
_HTML = _HERE / "local-dashboards.html"


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


def _report_registry() -> dict:
    from pyegeria.view.base_report_formats import get_report_registry
    return get_report_registry()


def _serialize_placement(p, sheets, registry) -> dict:
    fs = registry.get(p.ref)
    if fs is not None:
        action = getattr(fs, "action", None)
        return {
            "ref":            p.ref,
            "span":           p.span,
            "emphasis":       p.emphasis,
            "kind":           "spec",
            "heading":        getattr(fs, "heading", None) or p.ref,
            "description":    getattr(fs, "description", None) or "",
            "family":         getattr(fs, "family", None),
            "outputTypes":    sorted({str(t) for fmt in (getattr(fs, "formats", []) or [])
                                       for t in (getattr(fmt, "types", []) or [])}),
            "requiredParams": list(getattr(action, "required_params", []) or []) if action else [],
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
        "description": "Unresolved reference — no matching Report Spec or Dashboard Sheet.",
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


@router.get("/api/local-dashboards/{name}", summary="One Dashboard Sheet, placements resolved")
def get_local_dashboard(name: str):
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

    return JSONResponse({
        "name":        sheet.name,
        "heading":     sheet.heading,
        "description": sheet.description,
        "family":      sheet.family,
        "placements":  [_serialize_placement(p, sheets, registry) for p in sheet.placements],
    })
