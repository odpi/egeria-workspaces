"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Governance Metrics browser — FastAPI router.

Provides one endpoint:
  GET /api/governance-metrics  → every GovernanceMetric element, with its
    GovernanceResults link resolved to a Report (+ that Report's reportSpec
    name, so the frontend can offer a "run it live" button reusing
    /api/report-specs/execute) and its per-metric InformationSupplyChain
    "data flow" (Purposes/Scope text + member list) resolved by the naming
    convention gen_governance_metrics.py uses ("<metric name> Data Flow").

This is Tier 1 of the design discussed in OVERVIEW_NEXT_STEPS.md (2026-08-17
"Design landed" section): real GovernanceMetric→GovernanceResults→Report
lineage, rendered from Egeria metadata that already exists — it does NOT
attempt true DataFlow lineage into the analytic function/data source (those
aren't Egeria elements yet; see BACKLOG.md's "GovernanceMetric lineage"
items). The InformationSupplyChain is a *documented* flow (its Purposes
text names the stages), not a literal DataFlow graph.

Sync routes throughout (matching overview_handler.py/local_dashboards_
handler.py's own convention — see CLAUDE.md's async-invariants note: sync
pyegeria calls are only safe from sync routes, never from `async def` routes).
"""

import os
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

router = APIRouter(tags=["governance-metrics"])

_HERE = Path(__file__).parent
_HTML = _HERE / "governance-metrics.html"

_CACHE_TTL = 30  # seconds — matches overview_handler.py's own cache discipline
_cache: dict = {}


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


def _prop(el: dict, name: str) -> Optional[str]:
    pvm = (el.get("elementProperties") or {}).get("propertyValueMap") or {}
    v = pvm.get(name)
    return v.get("primitiveValue") if isinstance(v, dict) else None


def _add_prop(el: dict, name: str) -> Optional[str]:
    """additionalProperties is a MapTypePropertyValue -- unwrap mapValues.propertyValueMap
    (confirmed live 2026-08-18: NOT a plain nested propertyValueMap like other properties)."""
    pvm = (el.get("elementProperties") or {}).get("propertyValueMap") or {}
    ap = pvm.get("additionalProperties") or {}
    inner = (((ap.get("mapValues") or {}).get("propertyValueMap") or {}) if isinstance(ap, dict) else {})
    v = inner.get(name)
    return v.get("primitiveValue") if isinstance(v, dict) else None


@router.get("/api/governance-metrics", summary="List GovernanceMetric elements with their Report + data-flow lineage")
def get_governance_metrics(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    import time
    ckey = f"{url}|{server}|{user_id}"
    cached = _cache.get(ckey)
    if cached and (time.time() - cached[0]) < _CACHE_TTL:
        return JSONResponse(cached[1])

    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    body = {
        "class": "FindRequestBody", "metadataElementTypeName": "GovernanceMetric",
        "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0, "pageSize": 200,
    }
    try:
        els = mgr.find_metadata_elements(body)
        els = [e for e in els if isinstance(e, dict)] if isinstance(els, list) else []
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"governance-metrics: find failed: {exc}")
        els = []

    out = []
    for el in els:
        name = _prop(el, "displayName")
        guid = el.get("elementGUID")
        entry = {
            "name": name,
            "guid": guid,
            "summary": _prop(el, "summary"),
            "scope": _prop(el, "scope"),
            "usage": _prop(el, "usage"),
            "implementationDescription": _prop(el, "implementationDescription"),
            "measurement": _prop(el, "measurement"),
            "target": _prop(el, "target"),
            "report": None,
            "dataFlow": None,
        }
        # Resolve the GovernanceResults link -> Report (real Egeria edge).
        try:
            rel = mgr.get_all_related_elements(guid, output_format="JSON")
            for item in (rel.get("elementList") or []):
                if item.get("type", {}).get("typeName") != "GovernanceResults":
                    continue
                report_el = item.get("element") or {}
                entry["report"] = {
                    "name": _prop(report_el, "displayName"),
                    "guid": report_el.get("elementGUID"),
                    "reportSpec": _add_prop(report_el, "reportSpec"),
                    "outputFormat": _add_prop(report_el, "outputFormat"),
                }
                break
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"governance-metrics: GovernanceResults lookup failed for {name}: {exc}")

        # Resolve the per-metric InformationSupplyChain "data flow" by the
        # naming convention gen_governance_metrics.py uses -- a documented
        # (not literal DataFlow) chain; see this module's own docstring.
        try:
            flow_name = f"{name} Data Flow"
            flow_body = {
                "class": "FindRequestBody", "metadataElementTypeName": "InformationSupplyChain",
                "searchProperties": {
                    "class": "SearchProperties", "matchCriteria": "ALL",
                    "conditions": [{"property": "displayName", "operator": "EQ",
                                     "value": {"class": "PrimitiveTypePropertyValue", "typeName": "string",
                                               "primitiveValue": flow_name}}],
                },
                "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0, "pageSize": 1,
            }
            flow_els = mgr.find_metadata_elements(flow_body)
            flow_els = [e for e in flow_els if isinstance(e, dict)] if isinstance(flow_els, list) else []
            if flow_els:
                flow_el = flow_els[0]
                entry["dataFlow"] = {
                    "name": flow_name,
                    "purposes": _prop(flow_el, "description"),
                }
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"governance-metrics: InformationSupplyChain lookup failed for {name}: {exc}")

        out.append(entry)

    out.sort(key=lambda e: e["name"] or "")
    payload = {"metrics": out, "total": len(out), "source": "live:governance-metrics"}
    _cache[ckey] = (time.time(), payload)
    return JSONResponse(payload)


@router.get("/governance-metrics", include_in_schema=False)
def governance_metrics_page():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="governance-metrics.html not found")
    return FileResponse(_HTML)
