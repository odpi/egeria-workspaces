# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Insights — FastAPI router.

New portal app for cross-cutting governance search: compound classification +
zone faceted search over Egeria's native find_metadata_elements API. A query
like "quarantine zone AND Confidential AND High criticality" maps onto one
FindRequestBody (matchClassifications / SearchClassifications /
ClassificationCondition, each with its own nested SearchProperties, combined
via matchCriteria ALL/ANY) — this is a single Egeria call, not client-side
set intersection. See:
  org.odpi.openmetadata.frameworks.openmetadata.search.{SearchClassifications,
  ClassificationCondition, SearchProperties, PropertyComparisonOperator}

Facet *discovery* is deliberately not duplicated here — the frontend reuses
the existing /api/types (classification catalog, live from ValidMetadataManager)
and /api/valid-values/lookup (ordinal level labels, e.g. confidentialityLevel
2 -> "Confidential") endpoints already built for the Type System and Valid
Values tabs. This module only adds the querying/aggregation Egeria has no
native endpoint for.

Routes:
  GET  /egeria-insights       → serve the SPA
  GET  /api/insights/summary  → dashboard card counts (capped tally)
  GET  /api/insights/zones    → GovernanceZone definitions + usage counts
  POST /api/insights/search   → compound classification/zone/property search

Aggregate counts (both here and in the SPA) default to a capped tally over
the same page_size ceiling the rest of the app uses (~500 — see README's
"load-all, held in state" pagination philosophy) rather than a true
aggregation query, because Egeria's search API returns paged element lists
with no total-count metadata (checked OpenMetadataRootElementsResponse and
siblings — no totalCount field). `full_count=true` opts into paging through
everything up to `_FULL_COUNT_HARD_CAP` as a safety valve.

Verified live against qs-view-server 2026-07-15. Two things worth knowing:

- MetadataExpert.find_metadata_elements() returns the *raw* element shape (no
  elementHeader/properties wrapper — see the parsing helpers below), not the
  converter-normalized shape other handlers get from calls like
  AssetMaker.get_asset_by_guid(output_format="JSON").
- KNOWN SERVER BUG (PY-15 in PYEGERIA_ISSUES.md): the Postgres repository
  connector ignores matchCriteria for matchClassifications entirely once
  there are 2+ classification conditions — ANY/ALL/NONE all behave as if
  every named classification must be present on the same entity
  simultaneously, so any query naming 2+ classifications returns zero
  results. `get_summary()`'s 5-classification ANY tally and any
  multi-classification compound search are affected; both are still correct
  with 0 or 1 classification condition. No client-side workaround is applied
  here — see PY-15 for the server-side fix.
"""
import os
from pathlib import Path
from typing import Any, List, Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import apply_token

router = APIRouter(tags=["egeria-insights"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-insights.html"

_DEFAULT_CAP = 500            # same ceiling used elsewhere in the app (see module docstring)
_FULL_COUNT_HARD_CAP = 10000  # safety valve for the opt-in exhaustive count

# Governed-data classifications a "governance search" cares about by default —
# see GovernedDataClassificationBase subclasses in the Egeria source.
_GOVERNANCE_CLASSIFICATIONS = ("ZoneMembership", "Confidentiality", "Criticality", "Impact", "Retention")


# ── client factory ───────────────────────────────────────────────────────────

def _expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


# ── search-condition body construction ──────────────────────────────────────

class Condition(BaseModel):
    classification: str
    property: Optional[str] = None      # omit to match "carries this classification, any value"
    operator: str = "EQ"                # EQ | NEQ | LT | LTE | GT | GTE | LIKE | IS_NULL | NOT_NULL ...
    value: Optional[Any] = None
    value_type: str = "string"          # string | int | boolean


class SearchBody(BaseModel):
    type_name: Optional[str] = None     # metadataElementTypeName; omit = search all types
    match_criteria: str = "ALL"         # ALL | ANY | NONE across the conditions
    conditions: List[Condition] = []
    as_of_time: Optional[str] = None
    full_count: bool = False
    start_from: int = 0
    page_size: int = 200
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


def _prop_value(value, value_type: str) -> dict:
    vt = (value_type or "string").lower()
    if vt in ("int", "integer"):
        try:
            value = int(value)
        except (TypeError, ValueError):
            value = 0
        return {"class": "PrimitiveTypePropertyValue", "typeName": "int", "primitiveValue": value}
    if vt in ("bool", "boolean"):
        return {"class": "PrimitiveTypePropertyValue", "typeName": "boolean", "primitiveValue": bool(value)}
    return {"class": "PrimitiveTypePropertyValue", "typeName": "string", "primitiveValue": str(value)}


def _classification_condition(c: Condition) -> dict:
    cond: dict = {"name": c.classification}
    if c.property:
        prop_cond: dict = {"property": c.property, "operator": c.operator}
        if c.operator not in ("IS_NULL", "NOT_NULL"):
            prop_cond["value"] = _prop_value(c.value, c.value_type)
        cond["searchProperties"] = {
            "class": "SearchProperties",
            "matchCriteria": "ALL",
            "conditions": [prop_cond],
        }
    return cond


def _build_find_body(search: SearchBody) -> dict:
    body: dict = {"class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"]}
    if search.type_name:
        body["metadataElementTypeName"] = search.type_name
    if search.conditions:
        body["matchClassifications"] = {
            "class": "SearchClassifications",
            "matchCriteria": search.match_criteria or "ALL",
            "conditions": [_classification_condition(c) for c in search.conditions],
        }
    if search.as_of_time:
        body["asOfTime"] = search.as_of_time
    return body


# ── element / classification serialisation ──────────────────────────────────
# MetadataExpert.find_metadata_elements() returns the *raw* OpenMetataElement shape
# (verified live against qs-view-server), not the elementHeader/properties-wrapped
# "OpenMetadataRootElement" shape other handlers get from converter-backed calls
# like AssetMaker.get_asset_by_guid(output_format="JSON"). Concretely:
#   - no "elementHeader" wrapper — type/status/classifications sit at the top level
#   - guid is element["elementGUID"], not header["guid"]
#   - element["classifications"] is a flat list of AttachedClassification dicts,
#     each with "classificationName" and "classificationProperties.propertyValueMap"
#     (NOT a distinctly-named sibling key on a header, as originally guessed)
#   - properties live under element["elementProperties"]["propertyValueMap"], with
#     each value wrapped in a PrimitiveTypePropertyValue/ArrayTypePropertyValue dict
#     rather than being a plain scalar/list.

def _classification_key(type_name: str) -> str:
    return (type_name[:1].lower() + type_name[1:]) if type_name else type_name


def _prop_scalar(pv):
    """Unwrap one PropertyValue payload into a plain Python value. Arrays arrive as
    ArrayTypePropertyValue with a nested propertyValueMap keyed "0", "1", ... rather
    than a plain list — reassemble those in order."""
    if not isinstance(pv, dict):
        return pv
    if pv.get("class") == "ArrayTypePropertyValue":
        arr = (pv.get("arrayValues") or {}).get("propertyValueMap") or {}
        return [_prop_scalar(arr[k]) for k in sorted(arr, key=lambda k: int(k)) if k.isdigit()]
    if "primitiveValue" in pv:
        return pv.get("primitiveValue")
    return pv.get("symbolicName", pv)


def _element_props(element: dict) -> dict:
    """Flat {propName: value} from element["elementProperties"]["propertyValueMap"]."""
    pvm = (element.get("elementProperties") or {}).get("propertyValueMap") or {}
    return {k: _prop_scalar(v) for k, v in pvm.items()}


def _extract_classifications(element: dict) -> dict:
    """Best-effort {camelCaseKey: {propName: value}} for the governance-relevant
    classifications actually attached to this element. Only used to build result
    badges — an empty/partial result here degrades the UI, it doesn't fail a query."""
    out = {}
    interesting = {_classification_key(n) for n in _GOVERNANCE_CLASSIFICATIONS} | {"securityTags", "ownership"}
    for c in element.get("classifications") or []:
        if not isinstance(c, dict):
            continue
        name = c.get("classificationName")
        if not name:
            continue
        key = _classification_key(name)
        if key not in interesting:
            continue
        pvm = (c.get("classificationProperties") or {}).get("propertyValueMap") or {}
        out[key] = {k: _prop_scalar(v) for k, v in pvm.items()}
    return out


def _serialize_hit(el: dict) -> dict:
    type_info = el.get("type") or {}
    props = _element_props(el)
    guid = el.get("elementGUID", "")
    return {
        "guid":            guid,
        "typeName":        type_info.get("typeName", ""),
        "superTypeNames":  type_info.get("superTypeNames") or [],
        "displayName":     props.get("displayName") or props.get("name") or props.get("qualifiedName") or guid,
        "qualifiedName":   props.get("qualifiedName") or "",
        "classifications": _extract_classifications(el),
    }


def _zone_names(el: dict) -> list:
    zm = _extract_classifications(el).get("zoneMembership", {}).get("zoneMembership") or []
    return zm if isinstance(zm, list) else []


# ── SPA ───────────────────────────────────────────────────────────────────────

@router.get("/egeria-insights", include_in_schema=False)
def serve_insights():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Insights page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


# ── Dashboard summary ────────────────────────────────────────────────────────

@router.get("/api/insights/summary", summary="Dashboard card counts (capped tally)")
def get_summary(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create MetadataExpert for summary")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    body = {
        "class": "FindRequestBody",
        "matchClassifications": {
            "class": "SearchClassifications",
            "matchCriteria": "ANY",
            "conditions": [{"name": n} for n in _GOVERNANCE_CLASSIFICATIONS],
        },
        "limitResultsByStatus": ["ACTIVE"],
    }
    try:
        raw = mgr.find_metadata_elements(body, start_from=0, page_size=_DEFAULT_CAP, graph_query_depth=0)
    except Exception as exc:
        logger.exception("insights: summary search failed")
        raise HTTPException(status_code=500, detail=str(exc))

    hits = [el for el in (raw if isinstance(raw, list) else []) if isinstance(el, dict)]

    by_classification: dict = {}
    zone_counts: dict = {}
    for el in hits:
        for key in _extract_classifications(el):
            by_classification[key] = by_classification.get(key, 0) + 1
        for z in _zone_names(el):
            zone_counts[z] = zone_counts.get(z, 0) + 1

    top_zones = sorted(zone_counts.items(), key=lambda kv: -kv[1])[:8]
    return JSONResponse({
        "classifiedCount":  len(hits),
        "capped":           len(hits) >= _DEFAULT_CAP,
        "byClassification": by_classification,
        "topZones":         [{"zone": z, "count": c} for z, c in top_zones],
    })


# ── Zones ─────────────────────────────────────────────────────────────────────

@router.get("/api/insights/zones", summary="Governance zone definitions with usage counts")
def get_zones(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create MetadataExpert for zones")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    zone_body = {"class": "FindRequestBody", "metadataElementTypeName": "GovernanceZone",
                 "limitResultsByStatus": ["ACTIVE"]}
    try:
        raw_zones = mgr.find_metadata_elements(zone_body, start_from=0, page_size=500, graph_query_depth=0)
    except Exception as exc:
        logger.exception("insights: zone definitions query failed")
        raise HTTPException(status_code=500, detail=str(exc))

    zones = []
    for el in (raw_zones if isinstance(raw_zones, list) else []):
        if not isinstance(el, dict):
            continue
        props = _element_props(el)
        # GovernanceZone's zone-name property is "identifier" (the value that shows up
        # in a ZoneMembership classification's zoneMembership list), not "zoneName".
        name = props.get("identifier") or props.get("qualifiedName") or props.get("displayName") or ""
        zones.append({
            "guid":          el.get("elementGUID", ""),
            "name":          name,
            "displayName":   props.get("displayName") or name,
            "description":   props.get("description") or "",
            "qualifiedName": props.get("qualifiedName") or "",
            "count":         0,
        })
    zones.sort(key=lambda z: (z["displayName"] or z["name"] or "").lower())

    usage_body = {
        "class": "FindRequestBody",
        "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ANY",
                                  "conditions": [{"name": "ZoneMembership"}]},
        "limitResultsByStatus": ["ACTIVE"],
    }
    zone_counts: dict = {}
    counts_capped = False
    try:
        raw_usage = mgr.find_metadata_elements(usage_body, start_from=0, page_size=_DEFAULT_CAP, graph_query_depth=0)
        hits = [el for el in (raw_usage if isinstance(raw_usage, list) else []) if isinstance(el, dict)]
        counts_capped = len(hits) >= _DEFAULT_CAP
        for el in hits:
            for z in _zone_names(el):
                zone_counts[z] = zone_counts.get(z, 0) + 1
    except Exception:
        # Non-fatal — zone *definitions* are still useful without usage counts.
        logger.exception("insights: zone usage tally failed; returning definitions with zero counts")

    for z in zones:
        z["count"] = zone_counts.get(z["name"], 0)

    return JSONResponse({"zones": zones, "countsCapped": counts_capped, "total": len(zones)})


# ── Compound search ───────────────────────────────────────────────────────────

@router.post("/api/insights/search", summary="Compound classification/zone/property search")
def search_elements(body: SearchBody = Body(...)):
    try:
        mgr = _expert(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create MetadataExpert for search")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    find_body = _build_find_body(body)
    page_size = max(1, min(body.page_size, 500))

    hits: List[dict] = []
    truncated = False
    capped = False

    if body.full_count:
        start = 0
        while True:
            try:
                page = mgr.find_metadata_elements(find_body, start_from=start, page_size=page_size, graph_query_depth=0)
            except Exception as exc:
                logger.exception("insights: full-count search page failed")
                raise HTTPException(status_code=500, detail=str(exc))
            page = [el for el in (page if isinstance(page, list) else []) if isinstance(el, dict)]
            hits.extend(page)
            if len(page) < page_size or len(hits) >= _FULL_COUNT_HARD_CAP:
                truncated = len(page) == page_size and len(hits) >= _FULL_COUNT_HARD_CAP
                break
            start += page_size
    else:
        try:
            page = mgr.find_metadata_elements(find_body, start_from=body.start_from, page_size=page_size, graph_query_depth=0)
        except Exception as exc:
            logger.exception("insights: search failed")
            raise HTTPException(status_code=500, detail=str(exc))
        hits = [el for el in (page if isinstance(page, list) else []) if isinstance(el, dict)]
        capped = len(hits) >= page_size

    results = [_serialize_hit(el) for el in hits]

    # Aggregate counts per queried classification/property, tallied from whatever
    # was actually fetched (see `capped` / `truncated` for how complete that is).
    aggregates: dict = {}
    for cond in body.conditions:
        ck = _classification_key(cond.classification)
        agg_key = cond.classification + (("." + cond.property) if cond.property else "")
        tally: dict = {}
        for r in results:
            entry = r["classifications"].get(ck) or {}
            val = entry.get(cond.property) if cond.property else None
            values = val if isinstance(val, list) else ([val] if val is not None else [])
            for v in values:
                tally[str(v)] = tally.get(str(v), 0) + 1
        if tally:
            aggregates[agg_key] = tally

    return JSONResponse({
        "results":    results,
        "total":      len(results),
        "capped":     capped,
        "truncated":  truncated,
        "fullCount":  body.full_count,
        "aggregates": aggregates,
    })
