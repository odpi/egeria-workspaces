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
the frontend (egeria-shared-ui.js's useApplicableClassifications hook, which
replaced the old hardcoded-supertype _classificationApplicable guess with a
live call to GET /api/classification/applicable below) -- this router does
not re-check it server-side; a caller that bypasses the UI can still classify
anything Egeria itself would allow.

/api/classification/applicable (added 2026-08-17, Dan's call) intersects
ValidMetadataManager.get_valid_classification_types() -- Egeria's own
authoritative per-entity-type classification list -- across every distinct
type in a selection, then filters that down to whichever of CLASSIFICATIONS
below this router actually knows how to set/clear. That second filter matters:
get_valid_classification_types('GlossaryTerm') returns ~45 classification
types (Ownership, Retention, SecurityTags, a dozen Policy* governance points,
etc. -- most OpenMetadata classifications are validFor "Referenceable"), but
this router only has real set_X/clear_X support for a handful. Only the
handful are ever offered.

Endpoints:
  GET    /api/classification/applicable                             → which supported classifications are valid for a given (possibly mixed) set of entity types
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
from egeria_auth import apply_token
from governance_zones_handler import _classification_explorer

router = APIRouter(tags=["governance-classifications"])

# name (as used in URLs/frontend) -> pyegeria method stem, properties class,
# level property name, and the real Egeria classification type name (used to
# match against ValidMetadataManager.get_valid_classification_types() output
# in the /applicable endpoint below). "kind": "level" (default) needs a
# level int (+ optional notes) and comes from ClassificationExplorer; "kind":
# "marker" is a bare apply/clear with no properties at all and comes from
# GlossaryManager instead -- see _classification_client() below for how the
# right pyegeria client gets picked per entry.
CLASSIFICATIONS = {
    "confidentiality": {
        "kind": "level",
        "client": "classification_explorer",
        "set_method": "set_confidentiality_classification",
        "clear_method": "clear_confidentiality_classification",
        "properties_class": "ConfidentialityProperties",
        "type_name": "Confidentiality",
        "level_field": "confidentialityLevel",
    },
    "criticality": {
        "kind": "level",
        "client": "classification_explorer",
        "set_method": "set_criticality_classification",
        "clear_method": "clear_criticality_classification",
        "properties_class": "CriticalityProperties",
        "type_name": "Criticality",
        "level_field": "criticalityLevel",
    },
    "impact": {
        "kind": "level",
        "client": "classification_explorer",
        "set_method": "set_impact_classification",
        "clear_method": "clear_impact_classification",
        "properties_class": "ImpactProperties",
        "type_name": "Impact",
        "level_field": "severityLevel",
    },
    # Added 2026-08-17 alongside /api/classification/applicable -- same shape
    # as the three above (ClassificationExplorer.set_confidence_classification/
    # clear_confidence_classification, ConfidenceProperties.confidenceLevel),
    # confirmed via ClassificationExplorer's own docstring sample body.
    "confidence": {
        "kind": "level",
        "client": "classification_explorer",
        "set_method": "set_confidence_classification",
        "clear_method": "clear_confidence_classification",
        "properties_class": "ConfidenceProperties",
        "type_name": "Confidence",
        "level_field": "confidenceLevel",
    },
    # Added 2026-08-17 -- naming-standards markers (0438-Naming-Standards).
    # These are NOT on ClassificationExplorer at all; GlossaryManager exposes
    # them as set_is_X/clear_is_X(term_guid, body=None) -- confirmed via
    # pyegeria's own signatures, no properties class, no level. Egeria's own
    # typedef for e.g. PrimeWord carries zero attributeDefinitions, matching:
    # this is a bare apply/remove, not a level-style classification.
    "prime_word": {
        "kind": "marker",
        "client": "glossary_manager",
        "set_method": "set_is_prime_word",
        "clear_method": "clear_is_prime_word",
        "type_name": "PrimeWord",
    },
    "class_word": {
        "kind": "marker",
        "client": "glossary_manager",
        "set_method": "set_is_class_word",
        "clear_method": "clear_is_class_word",
        "type_name": "ClassWord",
    },
    "modifier": {
        "kind": "marker",
        "client": "glossary_manager",
        "set_method": "set_is_modifier",
        "clear_method": "clear_is_modifier",
        "type_name": "Modifier",
    },
}


def _classification_config(classification_name: str) -> dict:
    cfg = CLASSIFICATIONS.get(classification_name)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Unknown classification {classification_name!r}; v1 supports: {', '.join(CLASSIFICATIONS)}")
    return cfg


def _glossary_manager(url=None, server=None, user_id=None, user_pwd=None):
    """GlossaryManager client -- separate from _classification_explorer's
    ClassificationExplorer above. The naming-standards marker classifications
    (PrimeWord/ClassWord/Modifier/...) live here, not on ClassificationExplorer
    at all (Dan's correction, 2026-08-17 -- confirmed via GlossaryManager's own
    set_is_prime_word/set_is_class_word/set_is_modifier method names)."""
    from pyegeria import GlossaryManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    gm = GlossaryManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(gm)
    return gm


def _classification_client(cfg: dict, url=None, server=None, user_id=None, user_pwd=None):
    """Picks the right pyegeria client for a CLASSIFICATIONS entry based on
    its "client" key -- "glossary_manager" for marker classifications,
    "classification_explorer" (default, for backward compatibility with
    entries that predate this key) otherwise."""
    if cfg.get("client") == "glossary_manager":
        return _glossary_manager(url, server, user_id, user_pwd)
    return _classification_explorer(url, server, user_id, user_pwd)


def _valid_metadata_manager(url=None, server=None, user_id=None, user_pwd=None):
    """ValidMetadataManager client -- separate from _classification_explorer's
    ClassificationExplorer above; only ValidMetadataManager exposes
    get_valid_classification_types(). Same env-default/apply_token pattern."""
    from pyegeria import ValidMetadataManager
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    vmm = ValidMetadataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(vmm)
    return vmm


# entity type name -> set of classification type names valid for it, straight
# from get_valid_classification_types(). Cached process-wide, unbounded --
# entity/classification type defs don't change at runtime, and the key space
# is small (Egeria's own entity type catalog), same tradeoff as
# type_system_handler.py's _TYPE_NAMES_CACHE.
_VALID_CLASSIFICATIONS_CACHE: dict[str, set] = {}

def _valid_classification_names_for_type(vmm, entity_type: str) -> set:
    if entity_type in _VALID_CLASSIFICATIONS_CACHE:
        return _VALID_CLASSIFICATIONS_CACHE[entity_type]
    try:
        resp = vmm.get_valid_classification_types(entity_type)
        names = {td.get("name") for td in (resp or {}).get("typeDefs", []) if td.get("name")}
    except Exception as exc:
        logger.warning(f"get_valid_classification_types failed for {entity_type!r}: {exc}")
        names = set()
    _VALID_CLASSIFICATIONS_CACHE[entity_type] = names
    return names


@router.get("/api/classification/applicable", summary="Which of our supported bulk classifications are valid for the given entity type(s)")
def get_applicable_classifications(
    entity_types: str = Query(..., description="Comma-separated entity type names -- one per distinct type in the current selection"),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """A classification is offered only if it's valid for *every* distinct
    type in the selection -- that's what makes it safe to apply to the whole
    (possibly mixed-type) selection in one bulk action."""
    types = sorted({t.strip() for t in entity_types.split(",") if t.strip()})
    if not types:
        return JSONResponse({"classifications": []})
    try:
        vmm = _valid_metadata_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        common = None
        for t in types:
            names = _valid_classification_names_for_type(vmm, t)
            common = names if common is None else (common & names)
        vmm.close_session()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Egeria error: {exc}")
    common = common or set()
    applicable = [key for key, cfg in CLASSIFICATIONS.items() if cfg["type_name"] in common]
    return JSONResponse({"classifications": applicable})


# Egeria primitive category -> a small vocabulary the frontend renders a plain
# input for (int -> number input, string -> text input, boolean -> checkbox,
# anything else -> text input as a best-effort fallback). Extend as new
# classifications with richer property shapes get added.
_PRIMITIVE_KIND = {
    "OM_PRIMITIVE_TYPE_INT": "int", "OM_PRIMITIVE_TYPE_LONG": "int", "OM_PRIMITIVE_TYPE_SHORT": "int",
    "OM_PRIMITIVE_TYPE_FLOAT": "number", "OM_PRIMITIVE_TYPE_DOUBLE": "number",
    "OM_PRIMITIVE_TYPE_BOOLEAN": "boolean",
    "OM_PRIMITIVE_TYPE_DATE": "date",
    "OM_PRIMITIVE_TYPE_STRING": "string",
}

# classification type_name -> full attributeDefinitions list from Egeria's own
# ClassificationDef (get_all_classification_defs), cached process-wide -- same
# "type defs don't change at runtime" tradeoff as _VALID_CLASSIFICATIONS_CACHE.
# Keyed by type_name (not our short registry key) since that's what the raw
# typedef list is keyed by.
_CLASSIFICATION_SCHEMA_CACHE: dict[str, list] = {}

def _classification_schema(vmm, type_name: str) -> list:
    if type_name in _CLASSIFICATION_SCHEMA_CACHE:
        return _CLASSIFICATION_SCHEMA_CACHE[type_name]
    try:
        defs = vmm.get_all_classification_defs()
        td = next((t for t in (defs or []) if t.get("name") == type_name), None)
        attrs = (td or {}).get("attributeDefinitions") or []
    except Exception as exc:
        logger.warning(f"get_all_classification_defs failed while resolving {type_name!r} schema: {exc}")
        attrs = []
    _CLASSIFICATION_SCHEMA_CACHE[type_name] = attrs
    return attrs


@router.get("/api/classification/{classification_name}/schema", summary="Editable extra properties for a classification (beyond the level field and notes, which have dedicated UI)")
def get_classification_schema(
    classification_name: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    """Reads Egeria's own ClassificationDef.attributeDefinitions live (Dan's
    call, 2026-08-17) -- never hardcoded -- so any classification's full
    property set shows up automatically, not just the level+notes fields this
    UI already had dedicated controls for. Returns [] for "marker" kind
    classifications (they have none by design, e.g. PrimeWord) and for any
    classification whose level/notes fields exhaust its actual schema."""
    cfg = _classification_config(classification_name)
    if cfg.get("kind") != "level":
        return JSONResponse({"properties": []})
    try:
        vmm = _valid_metadata_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        attrs = _classification_schema(vmm, cfg["type_name"])
        vmm.close_session()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Egeria error: {exc}")

    skip = {cfg.get("level_field"), "notes"}
    props = []
    for a in attrs:
        name = a.get("attributeName")
        if not name or name in skip:
            continue
        attr_type = a.get("attributeType") or {}
        kind = _PRIMITIVE_KIND.get(attr_type.get("primitiveDefCategory"), "string")
        props.append({
            "name": name,
            "kind": kind,
            "description": a.get("attributeDescription") or "",
        })
    return JSONResponse({"properties": props})


@router.get("/api/classification/{classification_name}/level-property", summary="Which valid-values property name feeds this classification's level dropdown (or that it has none)")
def get_level_property(classification_name: str):
    cfg = _classification_config(classification_name)
    # "kind" lets the frontend skip the whole Level/Notes UI and valid-values
    # lookup for marker classifications (PrimeWord etc.) -- level_field is
    # None for those, there's nothing to look up.
    return JSONResponse({"level_field": cfg.get("level_field"), "kind": cfg.get("kind", "level")})


class BulkClassificationSetBody(BaseModel):
    guids: list[str]
    level: Optional[int] = None  # required for kind="level" classifications only; ignored for "marker"
    notes: Optional[str] = None
    # Free-form extra properties from GET .../schema (steward, stewardTypeName,
    # stewardPropertyName, source, confidence, statusIdentifier, or whatever
    # else a future classification's typedef carries) -- all optional, merged
    # straight into the write with statusIdentifier/confidence defaulted only
    # if the caller didn't supply them, so new property names never need a
    # backend code change, just a frontend form field.
    extra_properties: Optional[dict] = None
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/classification/{classification_name}/members", summary="Bulk-set a governance classification (level classifications: same level for every guid; marker classifications: no properties)")
def set_classification_members(classification_name: str, body: BulkClassificationSetBody = Body(...)):
    cfg = _classification_config(classification_name)
    kind = cfg.get("kind", "level")
    if kind == "level" and body.level is None:
        raise HTTPException(status_code=400, detail=f"{classification_name!r} requires a level")
    try:
        client = _classification_client(cfg, body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    if kind == "level":
        extra = dict(body.extra_properties or {})
        props = {
            "class": cfg["properties_class"],
            cfg["level_field"]: body.level,
            "statusIdentifier": extra.pop("statusIdentifier", 0),
            "confidence": extra.pop("confidence", 100),
        }
        props.update(extra)  # steward/stewardTypeName/stewardPropertyName/source/anything else the schema offered
        if body.notes:
            props["notes"] = body.notes
        req_body = {"class": "NewClassificationRequestBody", "properties": props}
    else:
        req_body = None  # marker classifications (GlossaryManager.set_is_X) take no properties at all

    set_method = getattr(client, cfg["set_method"])
    added, failed = [], []
    for guid in body.guids:
        try:
            if req_body is None:
                set_method(guid)
            else:
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
        client = _classification_client(cfg, body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    clear_method = getattr(client, cfg["clear_method"])
    removed, failed = [], []
    for guid in body.guids:
        try:
            clear_method(guid)
            removed.append(guid)
        except Exception as exc:  # noqa: BLE001 — partial-failure tolerant, matches collections_handler.py's bulk endpoints
            logger.debug(f"classification: failed to clear {classification_name} on {guid}: {exc}")
            failed.append({"guid": guid, "error": describe_bulk_item_error(exc)})
    return JSONResponse({"removed": removed, "failed": failed})
