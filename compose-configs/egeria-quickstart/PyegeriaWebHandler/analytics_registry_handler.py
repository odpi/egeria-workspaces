"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Analytic Functions Browser — FastAPI router.

Provides one endpoint:
  GET /api/analytics   → returns all registered analytic functions as JSON

Analytic functions are the routines a Report Spec's `analytic_function`
(Dr.Egeria's `extra_find`) can point at — see pyegeria.view.analytic_registry.
They are plain Python functions (not stored in Egeria) and this endpoint
requires no Egeria connection, mirroring report_specs_handler.py's
/api/report-specs endpoint for the same reason.

Also makes pyegeria.view.analytic_demo_specs's 10 demo report specs (one per
analytic function, proving each is actually runnable) show up in Egeria
Explorer's existing Report Specs browser alongside every other spec — see
analytic_demo_specs.py's module docstring for why these are hand-written
rather than Tinderbox-authored. Loading itself is pyegeria's own job now
(pyegeria.view.base_report_formats.get_report_registry() auto-loads its
CONFIG tier from settings.Environment.pyegeria_report_spec_modules / the
PYEGERIA_REPORT_SPEC_MODULES env var on first call) — this module only sets
that env var as a default, since the container's pyegeria install has no
config.json of its own pointing at it.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["analytics"])

os.environ.setdefault(
    "PYEGERIA_REPORT_SPEC_MODULES",
    "pyegeria.view.analytic_demo_specs:get_analytic_demo_specs",
)


def _get_registry() -> dict:
    from pyegeria.view.analytic_registry import get_analytic_registry
    return get_analytic_registry()


def _demo_report_spec_names() -> dict:
    """dotted function path -> demo report spec name, from
    pyegeria.view.analytic_demo_specs (best-effort -- {} if unavailable)."""
    try:
        from pyegeria.view.analytic_demo_specs import get_analytic_demo_specs
    except ImportError:
        return {}
    out = {}
    for spec_name, fs in get_analytic_demo_specs().items():
        action = getattr(fs, "action", None)
        func_decl = getattr(action, "analytic_function", None) if action else None
        if func_decl:
            out[func_decl] = spec_name
    return out


def _serialize(name: str, spec, demo_specs: dict) -> dict:
    """Convert an AnalyticFunctionSpec to a JSON-serialisable dict."""
    return {
        "name":           name,
        "function":       getattr(spec, "function", "") or "",
        "description":    getattr(spec, "description", "") or "",
        "returns":        getattr(spec, "returns", "") or "",
        "generic":        bool(getattr(spec, "generic", False)),
        "bindingNote":    getattr(spec, "binding_note", "") or "",
        "demoReportSpec": demo_specs.get(getattr(spec, "function", ""), None),
        "params": [
            {
                "name":        getattr(p, "name", ""),
                "type":        getattr(p, "type", "str"),
                "required":    bool(getattr(p, "required", False)),
                "default":     getattr(p, "default", None),
                "description": getattr(p, "description", "") or "",
            }
            for p in (getattr(spec, "params", []) or [])
        ],
    }


@router.get("/api/analytics", summary="List all registered analytic functions")
def get_analytics(
    q: Optional[str] = Query(
        None,
        description="Filter by function name, description, or dotted path (case-insensitive substring).",
    ),
):
    """
    Return all registered analytic functions (pyegeria.view.analytic_registry)
    as JSON. These are plain Python routines usable as a Report Spec's
    `analytic_function` (Dr.Egeria's `extra_find`) — no Egeria connection is
    required to list them.

    The full list is returned; filtering is intentionally lightweight (the
    browser UI does interactive search client-side). The server-side `q`
    filter is provided for direct API use.
    """
    try:
        registry = _get_registry()
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"Failed to load analytic function registry: {exc}")
        raise HTTPException(status_code=500, detail=f"Analytic function registry unavailable: {exc}")

    q_lower = q.strip().lower() if q else None
    demo_specs = _demo_report_spec_names()

    result: list[dict] = []
    for name, spec in registry.items():
        s = _serialize(name, spec, demo_specs)
        if q_lower is not None:
            haystack = " ".join([s["name"], s["description"], s["function"]]).lower()
            if q_lower not in haystack:
                continue
        result.append(s)

    result.sort(key=lambda s: s["name"])
    return JSONResponse({"functions": result, "total": len(result)})
