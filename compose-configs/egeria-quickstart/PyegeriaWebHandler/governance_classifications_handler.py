"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Governance Classifications (Confidentiality / Criticality / Impact) — bulk
classify/declassify FastAPI router.

v1 scope: Confidentiality, Criticality, Impact only (Dan's call, 2026-08-16).
Retention is deliberately out of scope for v1 — its properties are a
genuinely different shape (retentionBasis/status as strings, archiveAfter/
deleteAfter timestamps, no simple int level) rather than a level dropdown
like the other three, so it needs its own form design later, not a 4th row
in CLASSIFICATIONS below. Confidence (a distinct classification from
Confidentiality, easy to conflate) was never requested — also out of scope.

Unlike governance_zones_handler.py's ZoneMembership (a list-valued
classification where add_zone_membership() replaces the whole list, forcing
a read-then-write), these three are plain single-valued classifications with
real set_X/clear_X methods on ClassificationExplorer — pure blind set/clear,
no read needed first, same shape as collections_handler.py's bulk write loop.
Confirmed live 2026-08-16 against a real qs-metadata-store element (a
CSVFile): set as erinoverview, read back to confirm the write took
(confidentialityLevel round-tripped correctly), cleared, re-verified None.

Authorization: confirmed live once, 2026-08-16, that set_confidentiality_
classification succeeds for erinoverview and (at the time) garygeeke/
calliequartile/peterprofile/tanyatidie for this demo's persona set — no
elevated privilege beyond ordinary write access was required. That test
itself turned out to be the wrong way to answer the question, though: Egeria
records createdBy/updatedBy per classification version, so those test calls
are now permanently attributed to those personas in Egeria's own audit
trail, even though clearing the classification afterward removed the
*current* value. Don't repeat that pattern. The right way to handle
authorization here is what this router actually does: attempt the real
action the real user requested, and if Egeria denies it (401/403), surface
that as a clean "You don't have permission to do this." per-item message
(egeria_error_mapping.describe_bulk_item_error) rather than a raw exception
dump — never pre-test whether a persona *would* be allowed to.

Level values are NOT hardcoded here or in the frontend — valid_values_
handler.py's GET /api/valid-values/lookup?property_name=<levelField> reads
Egeria's own authoritative valid-metadata-values registry live. Confirmed
2026-08-16 for confidentialityLevel: 0=Unclassified, 1=Internal,
2=Confidential, 3=Sensitive, 4=Restricted, 99=Other. The frontend
ClassificationModal calls this endpoint itself; this router does not
duplicate the mapping.

Type applicability: Egeria's own type definition says Confidentiality/
Criticality/Impact are validFor "Referenceable" — i.e. technically
attachable to almost anything, including a Notification or ToDo, which
doesn't make sense in practice (the classification's own doc comment says
"typically a data field, schema attribute or glossary term" -- see
https://egeria-project.org/types/4/0422-Governed-Data-Classifications/).
Since Egeria's type model doesn't enforce this, the guard lives entirely in
the frontend (egeria-shared-ui.js's _classificationApplicable, checked
against typeName/superTypeNames) -- this router does not re-check it
server-side; a caller that bypasses the UI can still classify anything
Egeria itself would allow.

Endpoints:
  GET    /api/classification/{classification_name}/level-property  → which valid-values property name feeds this classification's level dropdown
  POST   /api/classification/{classification_name}/members          → bulk set (same level+notes for every guid)
  DELETE /api/classification/{classification_name}/members          → bulk clear
"""

import os
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from egeria_error_mapping import describe_bulk_item_error
from governance_zones_handler import _classification_explorer

router = APIRouter(tags=["governance-classifications"])

# name (as used in URLs/frontend) -> (pyegeria method stem, properties class, level property name)
CLASSIFICATIONS = {
    "confidentiality": {
        "set_method": "set_confidentiality_classification",
        "clear_method": "clear_confidentiality_classification",
        "properties_class": "ConfidentialityProperties",
        "level_field": "confidentialityLevel",
    },
    "criticality": {
        "set_method": "set_criticality_classification",
        "clear_method": "clear_criticality_classification",
        "properties_class": "CriticalityProperties",
        "level_field": "criticalityLevel",
    },
    "impact": {
        "set_method": "set_impact_classification",
        "clear_method": "clear_impact_classification",
        "properties_class": "ImpactProperties",
        "level_field": "severityLevel",
    },
}


def _classification_config(classification_name: str) -> dict:
    cfg = CLASSIFICATIONS.get(classification_name)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Unknown classification {classification_name!r}; v1 supports: {', '.join(CLASSIFICATIONS)}")
    return cfg


@router.get("/api/classification/{classification_name}/level-property", summary="Which valid-values property name feeds this classification's level dropdown")
def get_level_property(classification_name: str):
    cfg = _classification_config(classification_name)
    return JSONResponse({"level_field": cfg["level_field"]})


class BulkClassificationSetBody(BaseModel):
    guids: list[str]
    level: int
    notes: Optional[str] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/classification/{classification_name}/members", summary="Bulk-set a governance classification (same level for every guid)")
def set_classification_members(classification_name: str, body: BulkClassificationSetBody = Body(...)):
    cfg = _classification_config(classification_name)
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    props = {
        "class": cfg["properties_class"],
        cfg["level_field"]: body.level,
        "statusIdentifier": 0,
        "confidence": 100,
    }
    if body.notes:
        props["notes"] = body.notes
    req_body = {"class": "NewClassificationRequestBody", "properties": props}

    set_method = getattr(ce, cfg["set_method"])
    added, failed = [], []
    for guid in body.guids:
        try:
            set_method(guid, req_body)
            added.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, matches collections_handler.py's bulk endpoints
            logger.debug(f"classification: failed to set {classification_name} on {guid}: {exc}")
            failed.append({"guid": guid, "error": describe_bulk_item_error(exc)})
    return JSONResponse({"added": added, "failed": failed})


class BulkClassificationClearBody(BaseModel):
    guids: list[str]
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.delete("/api/classification/{classification_name}/members", summary="Bulk-clear a governance classification")
def clear_classification_members(classification_name: str, body: BulkClassificationClearBody = Body(...)):
    cfg = _classification_config(classification_name)
    try:
        ce = _classification_explorer(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    clear_method = getattr(ce, cfg["clear_method"])
    removed, failed = [], []
    for guid in body.guids:
        try:
            clear_method(guid)
            removed.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, matches collections_handler.py's bulk endpoints
            logger.debug(f"classification: failed to clear {classification_name} on {guid}: {exc}")
            failed.append({"guid": guid, "error": describe_bulk_item_error(exc)})
    return JSONResponse({"removed": removed, "failed": failed})
