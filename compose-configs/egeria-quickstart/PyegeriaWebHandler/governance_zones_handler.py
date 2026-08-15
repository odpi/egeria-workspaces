"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Governance Zone Membership — FastAPI router.

Endpoints:
  POST   /api/zone-membership/{zone_identifier}/members  → add elements to a zone (bulk)
  DELETE /api/zone-membership/{zone_identifier}/members  → remove elements from a zone (bulk)

Structurally different from collections_handler.py's bulk membership endpoints,
despite the similar shape: Collection membership is a real relationship
between two elements (CollectionMembership) -- a pure blind add/remove, no
read needed first. Zone membership is a *classification on the element
itself* (ZoneMembership, with a `zoneMembership: [name, ...]` list property)
-- and ClassificationExplorer.add_zone_membership() REPLACES that whole list,
it isn't additive. So "add this element to zone X" means: read the element's
current zone list, union in X, write the whole list back; "remove" means read,
subtract X, and either write the reduced list back or fully declassify if
that empties it. Confirmed live 2026-08-14 against a real qs-metadata-store
element (add twice with different lists -> second call succeeds and replaces,
no "already classified" error -- add_zone_membership is upsert, not
create-only, despite the "add" name and there being no separate
"set_zone_membership" method the way the other governance classifications
have set_confidentiality_classification/set_criticality_classification/etc.).

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
from egeria_error_mapping import raise_egeria_http_error, EGERIA_ERROR_RESPONSES

router = APIRouter(tags=["governance-zones"])


def _classification_explorer(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import ClassificationExplorer
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    ce = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(ce)
    return ce


def _current_zone_membership(ce, guid: str) -> list[str]:
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


class BulkZoneMembershipBody(BaseModel):
    guids: list[str]
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/zone-membership/{zone_identifier}/members", summary="Add elements to a governance zone (bulk)", responses=EGERIA_ERROR_RESPONSES)
def add_zone_members(zone_identifier: str, body: BulkZoneMembershipBody = Body(...)):
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create ClassificationExplorer")

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


@router.delete("/api/zone-membership/{zone_identifier}/members", summary="Remove elements from a governance zone (bulk)", responses=EGERIA_ERROR_RESPONSES)
def remove_zone_members(zone_identifier: str, body: BulkZoneMembershipBody = Body(...)):
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise_egeria_http_error(exc, "Failed to create ClassificationExplorer")

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
