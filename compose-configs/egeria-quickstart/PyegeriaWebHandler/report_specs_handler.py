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

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["report-specs"])


def _get_registry() -> dict:
    from pyegeria.view.base_report_formats import get_report_registry
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

    result: list[dict] = []
    for name, fs in registry.items():
        s = _serialize(name, fs)

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
    })
