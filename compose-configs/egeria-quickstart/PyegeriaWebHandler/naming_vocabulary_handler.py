"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Naming Vocabulary Explorer — FastAPI router.

Endpoints:
  GET /api/naming-vocabulary   → elements classified PrimeWord/ClassWord/Modifier, grouped

`PrimeWord`/`ClassWord`/`Modifier` are classifications on `Referenceable`
(typically applied to `ValidValueDefinition`s) describing the word vocabulary
used to compose standard names — see `NamingStandardRule`'s free-text
`nameConventions` property, which references this vocabulary but has no
relationship type connecting the two. Since these are marker classifications
with no properties of their own (confirmed against
PrimeWordProperties/ClassWordProperties/ModifierProperties in the Java
source — no fields beyond the type discriminator), there's nothing to
extract from the classification itself; the "word" being described is just
the underlying element's own displayName. No generic classification
extraction is needed here since each list is already scoped to one known
classification name via get_elements_by_classification.
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from egeria_auth import apply_token
from common_serialize import _authored_fields, _header_summary

router = APIRouter(tags=["naming-vocabulary"])

_CLASSIFICATIONS = ("PrimeWord", "ClassWord", "Modifier")


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _serialize_word(element: dict, classification: str) -> dict:
    props, header = _props(element), _header(element)
    return {
        "guid":            header.get("guid", ""),
        "typeName":        _type_name(element),
        "displayName":     props.get("displayName") or props.get("name") or props.get("qualifiedName") or "",
        "qualifiedName":   props.get("qualifiedName") or "",
        "description":     props.get("description") or "",
        "classification":  classification,
        "_header":         _header_summary(element),
        **_authored_fields(element),
    }


@router.get("/api/naming-vocabulary", summary="Elements classified PrimeWord/ClassWord/Modifier, grouped")
def get_naming_vocabulary(
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create ClassificationExplorer manager for naming vocabulary")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    groups: dict = {}
    for classification in _CLASSIFICATIONS:
        try:
            raw = mgr.get_elements_by_classification(classification, page_size=200, output_format="JSON", graph_query_depth=0)
        except Exception as exc:
            logger.exception(f"get_elements_by_classification failed for {classification}")
            raise HTTPException(status_code=500, detail=f"Naming vocabulary retrieval failed for {classification}: {exc}")
        items = [_serialize_word(e, classification) for e in (raw if isinstance(raw, list) else []) if isinstance(e, dict)]
        items.sort(key=lambda x: (x.get("displayName") or "").lower())
        groups[classification] = items

    total = sum(len(v) for v in groups.values())
    return JSONResponse({"groups": groups, "total": total})
