"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Governance Zone Membership — FastAPI router.

Ported from quickstart's governance_zones_handler.py as part of the
bulk-select/bulk-action framework sync (2026-08-15). freshstart has no
egeria-insights.html / "Query" feature (quickstart-only, out of scope for
this port), so the GET /api/insights/zones endpoint quickstart's
ZoneMembershipModal picker depends on doesn't exist here yet either — rather
than pull in the whole insights_handler.py module (a much bigger, unrelated
surface), a minimal, self-contained version of just that one endpoint is
included below, built on MetadataExpert the same way action_center_handler.py
already does in this codebase (its own private _prop_scalar/_element_props
copies, not cross-imported, matching this codebase's per-handler-private-
helper convention).

Endpoints:
  GET    /api/insights/zones                              → GovernanceZone definitions + usage counts (picker data)
  POST   /api/zone-membership/{zone_identifier}/members    → add elements to a zone (bulk)
  DELETE /api/zone-membership/{zone_identifier}/members    → remove elements from a zone (bulk)

Structurally different from collections_handler.py's bulk membership endpoints,
despite the similar shape: Collection membership is a real relationship
between two elements (CollectionMembership) -- a pure blind add/remove, no
read needed first. Zone membership is a *classification on the element
itself* (ZoneMembership, with a `zoneMembership: [name, ...]` list property)
-- and ClassificationExplorer.add_zone_membership() REPLACES that whole list,
it isn't additive. So "add this element to zone X" means: read the element's
current zone list, union in X, write the whole list back; "remove" means read,
subtract X, and either write the reduced list back or fully declassify if
that empties it. (Confirmed live against quickstart's qs-metadata-store in the
original port: add twice with different lists -> second call succeeds and
replaces, no "already classified" error -- add_zone_membership is upsert, not
create-only, despite the "add" name and there being no separate
"set_zone_membership" method the way the other governance classifications
have set_confidentiality_classification/set_criticality_classification/etc.)

This read-then-write means bulk zone actions cost one extra GET per element
compared to collections' pure-write loop -- an N+1, not a single blind
write per guid. Selections here are typically tens of items (not thousands),
so accepted as-is; revisit with a bulk-read endpoint if that changes.
"""

import os
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_auth import apply_token

router = APIRouter(tags=["governance-zones"])

_DEFAULT_CAP = 500  # same ceiling used elsewhere in this codebase


def _classification_explorer(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    ce = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(ce)
    return ce


def _expert(url=None, server=None, user_id=None, user_pwd=None):
    """MetadataExpert factory — for the zones-list endpoint only (raw
    find_metadata_elements query), matching action_center_handler.py's
    factory pattern in this codebase."""
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


def _prop_scalar(pv):
    """Unwrap one PropertyValue payload into a plain Python value. Arrays arrive as
    ArrayTypePropertyValue with a nested propertyValueMap keyed "0", "1", ... rather
    than a plain list — reassemble those in order. (Private copy, matching this
    codebase's per-handler-private-helper convention — see action_center_handler.py.)"""
    if not isinstance(pv, dict):
        return pv
    if pv.get("class") == "ArrayTypePropertyValue":
        arr = (pv.get("arrayValues") or {}).get("propertyValueMap") or {}
        return [_prop_scalar(arr[k]) for k in sorted(arr, key=lambda k: int(k)) if k.isdigit()]
    if "primitiveValue" in pv:
        return pv.get("primitiveValue")
    return pv.get("symbolicName", pv)


def _element_props(element: dict) -> dict:
    """Flat {propName: value} from element["elementProperties"]["propertyValueMap"]
    (MetadataExpert's raw find_metadata_elements shape)."""
    pvm = (element.get("elementProperties") or {}).get("propertyValueMap") or {}
    return {k: _prop_scalar(v) for k, v in pvm.items()}


def _zone_names(el: dict) -> list:
    """The ZoneMembership classification's zoneMembership list for one raw
    MetadataExpert element hit, kept as a real list (not the joined-string
    shape common_serialize.py's shared classification helpers use, which
    would need re-splitting here)."""
    for c in el.get("classifications") or []:
        if not isinstance(c, dict) or c.get("classificationName") != "ZoneMembership":
            continue
        pvm = (c.get("classificationProperties") or {}).get("propertyValueMap") or {}
        zm = pvm.get("zoneMembership")
        val = _prop_scalar(zm) if zm else []
        return val if isinstance(val, list) else []
    return []


@router.get("/api/insights/zones", summary="Governance zone definitions with usage counts")
def get_zones(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Minimal picker-data endpoint for ZoneMembershipModal — see module
    docstring for why this lives here rather than in a full insights_handler.py."""
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("governance-zones: failed to create MetadataExpert for zones")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    zone_body = {"class": "FindRequestBody", "metadataElementTypeName": "GovernanceZone",
                 "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                 "startFrom": 0, "pageSize": 500}
    try:
        raw_zones = mgr.find_metadata_elements(zone_body)
    except Exception as exc:
        logger.exception("governance-zones: zone definitions query failed")
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
        "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
        "startFrom": 0, "pageSize": _DEFAULT_CAP,
    }
    zone_counts: dict = {}
    counts_capped = False
    try:
        raw_usage = mgr.find_metadata_elements(usage_body)
        hits = [el for el in (raw_usage if isinstance(raw_usage, list) else []) if isinstance(el, dict)]
        counts_capped = len(hits) >= _DEFAULT_CAP
        for el in hits:
            for z in _zone_names(el):
                zone_counts[z] = zone_counts.get(z, 0) + 1
    except Exception:
        # Non-fatal — zone *definitions* are still useful without usage counts.
        logger.exception("governance-zones: zone usage tally failed; returning definitions with zero counts")

    for z in zones:
        z["count"] = zone_counts.get(z["name"], 0)
    return JSONResponse({"zones": zones, "countsCapped": counts_capped})


class BulkZoneMembershipBody(BaseModel):
    guids: list[str]
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/zone-membership/{zone_identifier}/members", summary="Add elements to a governance zone (bulk)")
def add_zone_members(zone_identifier: str, body: BulkZoneMembershipBody = Body(...)):
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("governance-zones: failed to create ClassificationExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    added, failed = [], []
    for guid in body.guids:
        try:
            current = _current_zone_membership(ce, guid)
            if zone_identifier in current:
                added.append(guid)  # already a member -- idempotent, not an error
                continue
            ce.add_zone_membership(guid, {
                "class": "NewClassificationRequestBody",
                "properties": {
                    "class": "ZoneMembershipProperties",
                    "zoneMembership": current + [zone_identifier],
                },
            })
            added.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, matches collections_handler.py's bulk endpoints
            logger.debug(f"zone-membership: failed to add {guid} to zone {zone_identifier}: {exc}")
            failed.append({"guid": guid, "error": str(exc)})
    return JSONResponse({"added": added, "failed": failed})


@router.delete("/api/zone-membership/{zone_identifier}/members", summary="Remove elements from a governance zone (bulk)")
def remove_zone_members(zone_identifier: str, body: BulkZoneMembershipBody = Body(...)):
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("governance-zones: failed to create ClassificationExplorer")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    removed, failed = [], []
    for guid in body.guids:
        try:
            current = _current_zone_membership(ce, guid)
            if zone_identifier not in current:
                removed.append(guid)  # already not a member -- idempotent, not an error
                continue
            remaining = [z for z in current if z != zone_identifier]
            if remaining:
                ce.add_zone_membership(guid, {
                    "class": "NewClassificationRequestBody",
                    "properties": {"class": "ZoneMembershipProperties", "zoneMembership": remaining},
                })
            else:
                ce.clear_zone_membership(guid, {"class": "DeleteClassificationRequestBody"})
            removed.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, matches collections_handler.py's bulk endpoints
            logger.debug(f"zone-membership: failed to remove {guid} from zone {zone_identifier}: {exc}")
            failed.append({"guid": guid, "error": str(exc)})
    return JSONResponse({"removed": removed, "failed": failed})


def _current_zone_membership(ce, guid: str) -> list:
    """Current ZoneMembership.zoneMembership list for one element, or [] if
    the element carries no ZoneMembership classification at all. depth=0 --
    only elementHeader.zoneMembership is read, no relationship traversal."""
    raw = ce.get_element_by_guid(guid=guid, output_format="JSON", body={"class": "GetRequestBody", "graphQueryDepth": 0})
    if not raw:
        raise ValueError(f"Element {guid!r} not found")
    zm = (raw.get("elementHeader") or {}).get("zoneMembership")
    if not zm:
        return []
    return list((zm.get("classificationProperties") or {}).get("zoneMembership") or [])
