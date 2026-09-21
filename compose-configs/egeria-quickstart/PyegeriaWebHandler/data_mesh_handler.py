"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Data Mesh — page route only. Its data API (list all Digital Products +
DigitalProductDependency edges, product detail) lives in
digital_products_handler.py (/api/digital-products/mesh, /api/digital-products/{guid}),
reused as-is since Data Mesh is just another view over the same products.
"""

from pathlib import Path

from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["data-mesh"])

_HERE = Path(__file__).parent
_HTML = _HERE / "data-mesh.html"


@router.get("/data-mesh", include_in_schema=False)
def data_mesh_page():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="data-mesh.html not found")
    return FileResponse(_HTML, media_type="text/html")
