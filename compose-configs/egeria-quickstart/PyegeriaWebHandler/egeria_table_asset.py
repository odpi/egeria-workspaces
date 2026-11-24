# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""GET /static/egeria-table.js: pyegeria's copy of the structured-TABLE renderer, the Portal's as fallback (PO-5).

egeria-table.js is edited in pyegeria first (owner decision D3, 2026-11-14) and shipped as package data,
pyegeria/view/static/egeria-table.js, from 6.2.42. The Portal used to serve only its vendored copy, which
drifts from pyegeria's unless someone copies it across. This route serves pyegeria's file when the
installed pyegeria has one, else the vendored static/egeria-table.js (an older pyegeria), and says which in
the X-Egeria-Table-Source header, so a reader of the page or of a test can tell what was served rather than
assume it. It is registered before the /static mount, so it wins over the mount for this one path.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

logger = logging.getLogger("pyegeria_web.egeria_table_asset")

router = APIRouter()

VENDORED = Path(__file__).resolve().parent / "static" / "egeria-table.js"
SOURCE_HEADER = "X-Egeria-Table-Source"


def pyegeria_table_js() -> Tuple[Optional[Path], Optional[str]]:
    """(path, pyegeria version) of the installed pyegeria's egeria-table.js, or (None, version|None)."""
    try:
        import importlib.metadata as md
        import pyegeria
        version = md.version("pyegeria")
    except Exception:
        return None, None
    path = Path(pyegeria.__file__).resolve().parent / "view" / "static" / "egeria-table.js"
    return (path if path.is_file() else None), version


def resolve() -> Tuple[Optional[Path], str]:
    """The file to serve and the X-Egeria-Table-Source value that names where it came from."""
    path, version = pyegeria_table_js()
    if path is not None:
        return path, f"pyegeria {version} package data"
    if VENDORED.is_file():
        why = f"pyegeria {version} has no egeria-table.js" if version else "pyegeria not importable"
        return VENDORED, f"portal fallback (static/egeria-table.js; {why})"
    return None, "none"


@router.get("/static/egeria-table.js", include_in_schema=False)
def egeria_table_js():
    path, source = resolve()
    if path is None:
        raise HTTPException(status_code=404,
                            detail="egeria-table.js: the installed pyegeria ships none and this Portal has no copy")
    # no-cache as for the rest of /static (NoCacheStaticFiles): revalidate, so a pyegeria upgrade shows at once.
    return FileResponse(str(path), media_type="text/javascript",
                        headers={"Cache-Control": "no-cache", SOURCE_HEADER: source})
