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
- ISSUE-35/PY-15 (Postgres connector ignoring matchCriteria on 2+
  classification conditions) is FIXED and CLOSED server-side (verified
  2026-07-17, egeria-python's PYEGERIA_ISSUES.md — the canonical tracker as
  of 2026-08-05; this repo's own copy is now a pointer) — multi-classification
  compound search is safe to use now. Kept as a historical note since
  `get_summary()`'s 5-classification ANY tally and this module predate the
  fix.
- ISSUE-34, egeria-python's PYEGERIA_ISSUES.md: `find_metadata_elements`'s
  `start_from`/`page_size` are NOT separate parameters anymore — set
  `"startFrom"`/`"pageSize"` directly in the FindRequestBody dict passed to
  it. Passing them as kwargs is silently a no-op (absorbed by `**kwargs`),
  not an error.

Relationship conditions (2026-08-04, NEXT-25): `matchClassifications` has no
equivalent for "has/lacks a relationship of type X" — Egeria's find API
filters on element properties/classifications only. Relationship presence is
therefore computed client-side, same pattern `overview_metrics.ai_ready_assets`
already uses: fetch each distinct relationship type's full GUID set once via
`ClassificationExplorer.get_relationships`, then filter the already-fetched
classification/type hits by set membership. IMPORTANT interaction: relationship
filtering runs AFTER classification/type paging, so with `full_count=false`
(the default) a relationship condition filters only the fetched page, not the
whole matching population — `relationshipFilterNote` in the response says so
explicitly rather than silently under-counting.
"""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _ce(url=None, server=None, user_id=None, user_pwd=None):
    """ClassificationExplorer factory — needed alongside MetadataExpert only for
    relationship queries (get_relationships), same split overview_handler.py uses."""
    from pyegeria import ClassificationExplorer
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    ce = ClassificationExplorer(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(ce)
    return ce


def _cm(url=None, server=None, user_id=None, user_pwd=None):
    """CollectionManager factory — used only by the saved-query endpoints below
    (Track A of EGERIA_INSIGHTS_QUERY_MODEL.md's phased plan). Saved queries are
    stored as `ResultsSet` collections (NOT "ResultSet" — that's the pyegeria
    FormatSet alias's spelling; the real Egeria entity type, confirmed live
    2026-08-05 against qs-view-server's /api/types entity catalog, is
    `ResultsSet`), with the query spec in `additionalProperties` — the doc's
    explicitly-short-term interim state (§2.3) ahead of a real `Query` element
    type + relationship to `ResultSet`."""
    from pyegeria import CollectionManager
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    cm = CollectionManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(cm)
    return cm


# ── search-condition body construction ──────────────────────────────────────

class Condition(BaseModel):
    classification: str
    property: Optional[str] = None      # omit to match "carries this classification, any value"
    operator: str = "EQ"                # EQ | NEQ | LT | LTE | GT | GTE | LIKE | IS_NULL | NOT_NULL ...
    value: Optional[Any] = None
    value_type: str = "string"          # string | int | boolean


class RelationshipCondition(BaseModel):
    relationship_type: str
    presence: str = "has"               # has | lacks — "lacks" is the enrichment-backlog case
                                         # (NEXT-25: "which assets DON'T have lineage yet")
    end: str = "any"                    # any | end1 | end2 — role/direction-aware (NEXT-25 follow-up).
                                         # "any" = either end (original behavior). end1/end2 match
                                         # Egeria's own relationship-definition ends, not a generic
                                         # "source/target" label — those don't universally apply
                                         # (e.g. SemanticAssignment's ends are "elements"/"meanings",
                                         # not a source->target flow). The frontend shows each type's
                                         # real role1/role2 names (from /api/types) as the two options.


class ValueCondition(BaseModel):
    property: str
    operator: str = "EQ"                # same vocabulary as Condition.operator
    value: Optional[Any] = None
    value_type: str = "string"          # string | int | boolean


class SearchBody(BaseModel):
    type_name: Optional[str] = None     # metadataElementTypeName; omit = search all types
    match_criteria: str = "ALL"         # ALL | ANY | NONE across the conditions
    conditions: List[Condition] = []
    value_conditions: List[ValueCondition] = []
    value_match_criteria: str = "ALL"   # ALL | ANY | NONE across value_conditions -- element-level
                                         # property search (FindRequestBody's top-level
                                         # searchProperties), distinct from `conditions`
                                         # above (classification-scoped property search,
                                         # matchClassifications[].searchProperties). Egeria
                                         # combines both in ONE server call -- see
                                         # Egeria-api-metadata-expert.http's worked example.
    relationship_conditions: List[RelationshipCondition] = []
    relationship_match_criteria: str = "ALL"   # ALL | ANY | NONE across relationship_conditions
    exclude_types: List[str] = []       # type/supertype names to drop from results, client-side, after
                                         # fetch. Egeria's find API has no "NOT type X" operator at all --
                                         # metadataElementTypeName is a single positive inclusion filter,
                                         # and metadataElementSubtypeNames (a documented allow-list field)
                                         # is confirmed live to have zero effect on results (PYEGERIA_ISSUES.md
                                         # ISSUE-45, Egeria-server-side). Even a working allow-list wouldn't
                                         # be true exclusion anyway -- see ISSUE-46. This is the interim
                                         # workaround that entry names: applied over the fetched page only
                                         # (same caveat class as relationship_conditions below), matched
                                         # against a result's own typeName OR any of its superTypeNames --
                                         # excluding "Action" drops every ToDo/Meeting/Review/Notification
                                         # at once, not just literal "Action" instances.
    sort_by: Optional[str] = None       # displayName | typeName | qualifiedName | matchCount | totalRelationshipCount
    sort_dir: str = "asc"               # asc | desc
    as_of_time: Optional[str] = None
    full_count: bool = False
    start_from: int = 0
    page_size: int = 200
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


class SavedQueryBody(BaseModel):
    """Track A save/load prototype (EGERIA_INSIGHTS_QUERY_MODEL.md §2.1/§2.3).
    `search` reuses SearchBody as-is — the persisted spec is whatever's
    reachable by POSTing this same shape to /api/insights/search, deliberately
    NOT a pyegeria-method-centric abstraction. See `_search_spec()` for the
    persist-able subset (connection fields and per-invocation paging state are
    stripped before storage)."""
    name: str
    description: Optional[str] = None
    search: SearchBody
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


class RefreshQueryBody(BaseModel):
    """`overrides` is shallow-merged onto the stored spec immediately before
    execution — the caller decides at the point of use (§2.2), same as any
    other saved-query invocation."""
    overrides: Optional[Dict[str, Any]] = None
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


def _value_condition(v: ValueCondition) -> dict:
    cond: dict = {"property": v.property, "operator": v.operator}
    if v.operator not in ("IS_NULL", "NOT_NULL"):
        cond["value"] = _prop_value(v.value, v.value_type)
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
    if search.value_conditions:
        # Element-level property search (FindRequestBody's top-level
        # searchProperties) -- distinct from matchClassifications above
        # (which only searches WITHIN a classification's own properties) and
        # combinable with it in the SAME server call, confirmed against
        # Egeria-api-metadata-expert.http's worked "nested condition" example
        # (both searchProperties and matchClassifications set at once).
        body["searchProperties"] = {
            "class": "SearchProperties",
            "matchCriteria": search.value_match_criteria or "ALL",
            "conditions": [_value_condition(v) for v in search.value_conditions],
        }
    if search.as_of_time:
        body["asOfTime"] = search.as_of_time
    # BUG FOUND 2026-08-05 (NEXT-25): a relationship-only search (no type_name,
    # no classification conditions) sends a near-empty FindRequestBody, and
    # Egeria's findMetadataElements rejects it server-side --
    # OMAG-COMMON-400-006 "the metadataElementTypeName parameter ... is null"
    # (confirmed live: reproduces with relationship_conditions=[DataFlow:has]
    # and nothing else). Tried "Referenceable" (the universal base type) as
    # the default first -- that's literally every element in the repository,
    # and timed out live (30s, TIMEOUT_ERROR_408) since find_metadata_elements
    # ignores page_size and returns everything at once. "Asset" is the
    # practical, bounded default instead -- most governance/relationship
    # questions are Asset-scoped anyway (same assumption overview_metrics.py's
    # composite functions already make) -- only applied when the caller gave
    # nothing else to filter on, never overriding an explicit
    # type_name/conditions choice. The frontend surfaces this default in a
    # hint so it isn't a silent surprise.
    if (not search.type_name and not search.conditions and not search.value_conditions
            and search.relationship_conditions):
        body["metadataElementTypeName"] = "Asset"
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


def _serialize_member(el: dict) -> dict:
    """Serialize one CollectionManager.get_collection_members() hit — a
    converter-normalized OpenMetadataRootElement ({elementHeader, properties}),
    a DIFFERENT shape from _serialize_hit's raw find_metadata_elements shape
    (see module docstring's shape note). No classifications available on this
    shape in the deployed server version — materialized-result rows render
    via the same SearchResults table, just with blank classification/
    relationship columns."""
    header = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    type_info = header.get("type") or {}
    guid = header.get("guid", "")
    return {
        "guid":            guid,
        "typeName":        type_info.get("typeName", ""),
        "superTypeNames":  type_info.get("superTypeNames") or [],
        "displayName":     props.get("displayName") or props.get("name") or props.get("qualifiedName") or guid,
        "qualifiedName":   props.get("qualifiedName") or "",
        "classifications": {},
    }


# ── relationship presence (client-side — see module docstring) ──────────────

def _json_list(raw) -> list:
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for k in ("elements", "items", "relationships", "list"):
            if isinstance(raw.get(k), list):
                return [r for r in raw[k] if isinstance(r, dict)]
    return []


def _relationship_guid_counts(ce, relationship_type: str, as_of: Optional[str] = None,
                               page_size: int = 5000, end: str = "any") -> Dict[str, int]:
    """{guid: occurrence count} for every element that participates in >=1
    relationship of this type — counts each occurrence separately (an element
    that's end1 twice and end2 once counts 3 when end="any"), same end1/end2
    extraction `overview_metrics.ai_ready_assets` already verified live (a
    relationship's own GUID key is plain "guid", NOT "elementGUID" like a
    find_metadata_elements hit — two different key names for the same concept
    depending on which API path returned the data). Presence (has/lacks) is
    just `guid in counts`; the count itself is what lets a caller distinguish
    "1 DataFlow" from "12 DataFlows" (a much stronger enrichment signal, and
    a legitimate sort key — see matchCount/totalRelationshipCount below).

    `end`: "any" (default, both ends — original behavior) | "end1" | "end2" —
    role/direction-aware search (NEXT-25 follow-up). Restricting to one end
    answers "which elements are the SOURCE of a DataFlow" vs "which are the
    TARGET", not just "which participate at all"."""
    out: Dict[str, int] = {}
    end_keys = ("end1", "end2") if end == "any" else (end,)
    try:
        body = {"class": "ResultsRequestBody", "asOfTime": as_of} if as_of else None
        rels = _json_list(ce.get_relationships(
            relationship_type=relationship_type, output_format="JSON",
            start_from=0, page_size=page_size, body=body))
        for r in rels:
            for end_key in end_keys:
                g = ((r.get(end_key) or {}) if isinstance(r, dict) else {}).get("guid")
                if g:
                    out[g] = out.get(g, 0) + 1
    except Exception as exc:  # noqa: BLE001 — best-effort, degrade don't fail the whole search
        logger.debug(f"insights: relationship query failed for {relationship_type!r} end={end!r}: {exc}")
    return out


def _cond_key(c: "RelationshipCondition") -> str:
    """Result/aggregate dict key for one relationship condition — plain type
    name when end="any" (backward compatible with the pre-direction-aware
    shape), "Type:end1"/"Type:end2" when a specific end was asked for, so an
    "as source" and "as target" condition on the SAME type can coexist as two
    distinct entries rather than colliding."""
    return c.relationship_type if c.end == "any" else f"{c.relationship_type}:{c.end}"


def _annotate_relationships(
    results: List[dict], ce, conds: List["RelationshipCondition"], as_of: Optional[str] = None,
) -> List[dict]:
    """Add a "relationships": {key: bool} + "relationshipCounts": {key: int}
    pair to every result (key = _cond_key(condition)) — always run over the
    FULL fetched population (before any relationship filtering shrinks it),
    so aggregates below reflect what was actually fetched, not just what
    survived the filter."""
    if not conds:
        return results
    by_key = {_cond_key(c): c for c in conds}  # de-dup by (type, end) composite
    guid_counts = {k: _relationship_guid_counts(ce, c.relationship_type, as_of, end=c.end)
                   for k, c in by_key.items()}
    out = []
    for r in results:
        r = dict(r)
        r["relationships"] = {k: (r["guid"] in guid_counts[k]) for k in by_key}
        r["relationshipCounts"] = {k: guid_counts[k].get(r["guid"], 0) for k in by_key}
        out.append(r)
    return out


def _filter_by_relationships(
    results: List[dict], conds: List["RelationshipCondition"], match_criteria: str,
) -> List[dict]:
    """Filter already-annotated results (see _annotate_relationships) by
    has/lacks per condition, combined via ALL/ANY/NONE — same semantics as
    classification match_criteria."""
    if not conds:
        return results
    mc = (match_criteria or "ALL").upper()

    def _satisfies(r: dict) -> bool:
        rels = r.get("relationships") or {}
        checks = [rels.get(_cond_key(c), False) if c.presence == "has"
                  else not rels.get(_cond_key(c), False) for c in conds]
        if mc == "ANY":
            return any(checks)
        if mc == "NONE":
            return not any(checks)
        return all(checks)

    return [r for r in results if _satisfies(r)]


_SORT_FIELDS = {
    "displayName":   lambda r: (r.get("displayName") or "").lower(),
    "typeName":      lambda r: (r.get("typeName") or "").lower(),
    "qualifiedName": lambda r: (r.get("qualifiedName") or "").lower(),
    # matchCount: how many of the queried relationship conditions this result
    # satisfies "has" on — surfaces the closest-to-ready assets first when
    # sorted desc (e.g. "governed + documented, only missing lineage").
    "matchCount":    lambda r: sum(1 for v in (r.get("relationships") or {}).values() if v),
    # totalRelationshipCount: sum of occurrence counts across all queried
    # relationship types — distinguishes "1 DataFlow" from "12 DataFlows"
    # where matchCount alone (both "has DataFlow") can't.
    "totalRelationshipCount": lambda r: sum((r.get("relationshipCounts") or {}).values()),
}


def _sort_results(results: List[dict], sort_by: Optional[str], sort_dir: str) -> List[dict]:
    """Always sorted client-side — Egeria's own sequencing_order/sequencing_property
    is unreliable (NEXT-20 in egeria-workspaces BACKLOG.md: silently ignored once
    a classification filter is also present), so this module never relies on it."""
    key = _SORT_FIELDS.get(sort_by)
    if not key:
        return results
    return sorted(results, key=key, reverse=(sort_dir == "desc"))


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
        # startFrom/pageSize/graphQueryDepth go in the body itself now, not
        # as separate kwargs -- pyegeria's find_metadata_elements stopped
        # accepting those as parameters (PYEGERIA_ISSUES.md ISSUE-34:
        # startFrom/pageSize used to be URL query params for this endpoint,
        # then silently stopped working once Egeria moved pagination for it
        # into the request body; passing them as kwargs here is now a
        # silent no-op, not an error).
        body = {**body, "graphQueryDepth": 0, "startFrom": 0, "pageSize": _DEFAULT_CAP}
        raw = mgr.find_metadata_elements(body)
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


# ── Classification browse (2026-08-05) ───────────────────────────────────────
# Generalizes the left-rail browse beyond ZoneMembership (which stays the
# default, cheaply enumerable via GovernanceZone definitions) to ANY
# classification the caller picks — one on-demand tally per selection, not
# a pre-computed count for the whole type system (same cost-shape reasoning
# as _INTERESTING_RELATIONSHIP_TYPES below: computing this for every
# classification up front would mean one full query per type).

@router.get("/api/insights/classification-count", summary="Capped tally of elements carrying one named classification")
def get_classification_count(
    name: str = Query(..., description="Classification type name, e.g. Confidentiality"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create MetadataExpert for classification-count")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    body = {
        "class": "FindRequestBody",
        "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ANY",
                                  "conditions": [{"name": name}]},
        "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
        "startFrom": 0, "pageSize": _DEFAULT_CAP,
    }
    try:
        raw = mgr.find_metadata_elements(body)
    except Exception as exc:
        logger.exception(f"insights: classification-count query failed for {name!r}")
        raise HTTPException(status_code=500, detail=str(exc))
    hits = [el for el in (raw if isinstance(raw, list) else []) if isinstance(el, dict)]
    return JSONResponse({"name": name, "count": len(hits), "capped": len(hits) >= _DEFAULT_CAP})


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
                 "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
                 "startFrom": 0, "pageSize": 500}  # ISSUE-34 -- body fields, not kwargs (see get_summary)
    try:
        raw_zones = mgr.find_metadata_elements(zone_body)
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
        "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0,
        "startFrom": 0, "pageSize": _DEFAULT_CAP,  # ISSUE-34 -- body fields, not kwargs
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
        logger.exception("insights: zone usage tally failed; returning definitions with zero counts")

    for z in zones:
        z["count"] = zone_counts.get(z["name"], 0)

    return JSONResponse({"zones": zones, "countsCapped": counts_capped, "total": len(zones)})


# ── Relationships (NEXT-25) ──────────────────────────────────────────────────
# A curated subset, not all ~734 Egeria relationship types — each type here
# costs one full get_relationships fetch, so this stays a "commonly
# interesting" browse list (lineage/meaning/governance/collaboration), same
# curation philosophy _GOVERNANCE_CLASSIFICATIONS already uses for
# classifications. The Governance Search condition-builder is NOT limited to
# this list (it offers the full /api/types catalog) — this is only for the
# browse/summary views (RelationshipTree, Dashboard's Relationship Coverage
# card), where fetching all ~734 types live on every page load would be
# impractical.
_INTERESTING_RELATIONSHIP_TYPES = (
    ("DataFlow",             "🔀", "Data movement between assets/processes — operational lineage"),
    ("ControlFlow",          "🔀", "Process control-flow sequencing — operational lineage"),
    ("DataMapping",          "🔀", "Field-to-field data mapping — operational lineage"),
    ("SemanticAssignment",   "🧠", "Element linked to a glossary term — the meaning layer"),
    ("CollectionMembership", "🗂️", "Element belongs to a Collection (DigitalProduct, DataDictionary, ...)"),
    ("Certification",        "📜", "Formal certification against a CertificationType"),
    ("License",               "📄", "Formal license against a LicenseType"),
    ("Exception",             "⚠️", "Open governance exception"),
    ("AttachedComment",       "💬", "Crowd-sourced comment"),
    ("AttachedRating",        "⭐", "Crowd-sourced rating"),
    ("AttachedLike",          "👍", "Crowd-sourced like"),
    ("AttachedTag",           "🏷️", "Informal tag"),
    ("AttachedNoteLog",       "📝", "Attached note log"),
)


def _relationship_type_stats(ce, rel_type: str) -> dict:
    """One relationship type's instance/participant tally — the per-type cost
    _INTERESTING_RELATIONSHIP_TYPES is curated to avoid paying for all ~734
    types at once. Factored out so the curated browse list (get_relationships)
    and the on-demand single-type lookup (get_relationship_count, for
    anything outside that curated list) share one implementation."""
    try:
        rels = _json_list(ce.get_relationships(
            relationship_type=rel_type, output_format="JSON",
            start_from=0, page_size=_DEFAULT_CAP, body=None))
    except Exception:
        logger.debug(f"insights: relationship usage query failed for {rel_type!r}")
        rels = []
    participants: set = set()
    for r in rels:
        for end_key in ("end1", "end2"):
            g = ((r.get(end_key) or {}) if isinstance(r, dict) else {}).get("guid")
            if g:
                participants.add(g)
    capped = len(rels) >= _DEFAULT_CAP
    return {"instanceCount": len(rels), "participantCount": len(participants), "capped": capped}


@router.get("/api/insights/relationships", summary="Relationship-type usage counts (curated set, capped tally)")
def get_relationships(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        ce = _ce(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.exception("insights: failed to create ClassificationExplorer for relationships")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    out = []
    any_capped = False
    for rel_type, icon, desc in _INTERESTING_RELATIONSHIP_TYPES:
        stats = _relationship_type_stats(ce, rel_type)
        any_capped = any_capped or stats["capped"]
        out.append({"type": rel_type, "icon": icon, "description": desc, **stats})
    out.sort(key=lambda r: -r["instanceCount"])
    return JSONResponse({"relationships": out, "anyCapped": any_capped})


@router.get("/api/insights/relationship-count", summary="On-demand instance/participant tally for ANY relationship type (not just the curated set)")
def get_relationship_count(
    rel_type: str = Query(..., alias="type", description="Relationship type name, e.g. DataFlow"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        ce = _ce(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.exception("insights: failed to create ClassificationExplorer for relationship-count")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    stats = _relationship_type_stats(ce, rel_type)
    return JSONResponse({"type": rel_type, **stats})


# ── Compound search ───────────────────────────────────────────────────────────

@router.post("/api/insights/search", summary="Compound classification/zone/property search")
def search_elements(body: SearchBody = Body(...)):
    try:
        mgr = _expert(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create MetadataExpert for search")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    find_body = _build_find_body(body)

    # BUG FOUND 2026-08-05 (live-reported: user typed a classification into
    # the Classifications browse picker, saw its count, but clicked Search
    # directly instead of "+ Add condition" first -- so the search itself
    # carried NO type/classification/relationship/value condition at all).
    # _build_find_body's Asset-default guard only covers the
    # relationship-conditions-only case; a genuinely empty SearchBody falls
    # through with no metadataElementTypeName AND no matchClassifications/
    # searchProperties, and Egeria correctly (but unhelpfully) 400s with a
    # raw exception trace ("metadataElementTypeName ... is null") -- this
    # guard catches it before ever calling Egeria, with an actionable
    # message instead of a stack trace surfacing in the UI.
    if not any(k in find_body for k in ("metadataElementTypeName", "matchClassifications", "searchProperties")):
        raise HTTPException(
            status_code=400,
            detail="Add an element type, classification, relationship, or property-value condition "
                   "before searching — an unscoped search would match the entire repository.",
        )

    defaulted_type_note = (
        f"No type, classification, or property-value condition given for this relationship search — "
        f"defaulted to metadataElementTypeName={find_body['metadataElementTypeName']!r} (a "
        f"relationship-only search against every element in the repository times out; add a type, "
        f"classification, or property condition to search a different scope)."
    ) if (not body.type_name and not body.conditions and not body.value_conditions
          and body.relationship_conditions and find_body.get("metadataElementTypeName")) else None
    page_size = max(1, min(body.page_size, 500))

    # BUG FOUND 2026-08-05 (live-reported: "DataFlow shows 8 in the tree,
    # but Search with no other clauses returns 0"). Root cause: a
    # relationship-only search defaults to metadataElementTypeName="Asset"
    # (see `defaulted_type_note` above) with nothing else narrowing scope,
    # but the default (non-exhaustive) fetch only pulls ONE capped page
    # (page_size, default 200) out of the FULL Asset population (~1,900+ in
    # this demo) in Egeria's own arbitrary server order. Confirmed live:
    # DataFlow's 10 real participants (SoftwareServer/Topic, genuine Asset
    # subtypes) simply weren't among the first 200 assets returned --
    # full_count=true correctly found all 10, a plain page found 0. The
    # `relationshipFilterNote` caveat already existed and was technically
    # honest, but for this specific combination (type defaulted AND nothing
    # else narrowing scope) a single page is essentially never
    # representative -- relationship matches are typically a small fraction
    # of a whole type population, so silently returning "0 results" from a
    # near-random sample is actively misleading, not just incomplete.
    # Fix: force the exhaustive (paginate-everything) path automatically in
    # exactly this situation, regardless of what the caller passed for
    # full_count -- reflected honestly in the response's own `fullCount`.
    effective_full_count = body.full_count or bool(defaulted_type_note)

    hits: List[dict] = []
    truncated = False
    capped = False

    if effective_full_count:
        # BUG FOUND 2026-08-04, ROOT-CAUSED 2026-08-05 (PYEGERIA_ISSUES.md
        # ISSUE-34, formerly egeria-workspaces-fs's own PY-23). CORRECTED
        # diagnosis, same day: this was never an Egeria-server-side bug --
        # find_metadata_elements' pagination moved from URL query params to
        # request-body fields months ago, and pyegeria was (until just now)
        # still sending startFrom/pageSize as URL params for this endpoint,
        # which the server silently ignores. Real pagination DOES work once
        # startFrom/pageSize are set as BODY fields (confirmed live: two
        # distinct, non-overlapping pages, not the same full set twice).
        # pyegeria's find_metadata_elements no longer accepts start_from/
        # page_size as parameters at all (ISSUE-34's fix) -- set them in
        # find_body directly below, every iteration.
        #
        # The GUID-dedup loop below predates this fix (written when pagination
        # genuinely didn't work, to avoid the same ~1.7k elements being
        # re-appended every iteration until the hard cap). Left in place even
        # though real pagination now works -- it's a no-op safety net once
        # pages are genuinely distinct (each page contributes only new GUIDs,
        # so `added` naturally reaches 0 right after the last real page), and
        # it stays correct if this endpoint's pagination ever regresses again.
        start = 0
        seen_guids: set = set()
        while True:
            try:
                page = mgr.find_metadata_elements({**find_body, "graphQueryDepth": 0,
                                                     "startFrom": start, "pageSize": page_size})
            except Exception as exc:
                logger.exception("insights: full-count search page failed")
                raise HTTPException(status_code=500, detail=str(exc))
            page = [el for el in (page if isinstance(page, list) else []) if isinstance(el, dict)]
            added = 0
            for el in page:
                g = el.get("elementGUID")
                if g and g in seen_guids:
                    continue
                seen_guids.add(g)
                hits.append(el)
                added += 1
            if added == 0 or len(page) < page_size or len(hits) >= _FULL_COUNT_HARD_CAP:
                truncated = added > 0 and len(hits) >= _FULL_COUNT_HARD_CAP
                break
            start += page_size
    else:
        try:
            page = mgr.find_metadata_elements({**find_body, "graphQueryDepth": 0,
                                                 "startFrom": body.start_from, "pageSize": page_size})
        except Exception as exc:
            logger.exception("insights: search failed")
            raise HTTPException(status_code=500, detail=str(exc))
        hits = [el for el in (page if isinstance(page, list) else []) if isinstance(el, dict)]
        capped = len(hits) >= page_size

    results = [_serialize_hit(el) for el in hits]

    # Type exclusion (2026-08-05) — client-side, applied before everything
    # else below (aggregates, relationship annotation/filtering, sorting)
    # so excluded elements are treated as if they'd never been fetched, not
    # just hidden at the last step. See SearchBody.exclude_types' docstring
    # for why this can't be pushed server-side.
    excluded_type_note = None
    if body.exclude_types:
        exclude_set = {t for t in body.exclude_types if t}
        if exclude_set:
            before_exclude = len(results)
            results = [
                r for r in results
                if r["typeName"] not in exclude_set
                and not (set(r.get("superTypeNames") or []) & exclude_set)
            ]
            removed = before_exclude - len(results)
            if removed:
                excluded_type_note = (
                    f"Excluded {removed} of {before_exclude} fetched element(s) matching type "
                    f"{', '.join(sorted(exclude_set))} (or a subtype) — applied to the fetched page "
                    "only, not server-wide (Egeria's find API has no server-side type-exclusion; see "
                    "PYEGERIA_ISSUES.md ISSUE-45/ISSUE-46)."
                )

    fetched_count = len(results)

    # Relationship presence (NEXT-25) — client-side, see module docstring.
    # Annotate over the FULL fetched population first so aggregates reflect
    # what was fetched, then filter.
    relationship_filter_note = None
    if body.relationship_conditions:
        try:
            ce = _ce(body.url, body.server, body.user_id, body.user_pwd)
        except Exception as exc:  # noqa: BLE001
            logger.exception("insights: failed to create ClassificationExplorer for relationship conditions")
            raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
        results = _annotate_relationships(results, ce, body.relationship_conditions, body.as_of_time)
        if not effective_full_count:
            relationship_filter_note = (
                f"Relationship condition(s) were applied to the {fetched_count} elements fetched by the "
                f"classification/type filter{' (a capped page, not the full matching population)' if capped else ''} "
                "— not to every matching element server-wide. Use \"Exact count\" (full_count) for a complete answer."
            )
        results = _filter_by_relationships(results, body.relationship_conditions, body.relationship_match_criteria)

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

    # Relationship presence tally — counted over the annotated set before this
    # response's own filter narrowed `results` down to just the matches, so it
    # still shows "12 have DataFlow, 41 don't" even for a "lacks" query.
    relationship_aggregates: dict = {}
    if body.relationship_conditions:
        for c in body.relationship_conditions:
            key = _cond_key(c)
            has = sum(1 for r in results if (r.get("relationships") or {}).get(key))
            counts = [(r.get("relationshipCounts") or {}).get(key, 0) for r in results]
            total = sum(counts)
            relationship_aggregates[key] = {
                "has": has, "lacks": len(results) - has,
                "totalInstances": total,
                "avgPerHaving": round(total / has, 1) if has else 0,
                "maxPerElement": max(counts) if counts else 0,
            }

    results = _sort_results(results, body.sort_by, body.sort_dir)

    return JSONResponse({
        "results":                results,
        "total":                  len(results),
        "capped":                 capped,
        "truncated":              truncated,
        "fullCount":              effective_full_count,
        "aggregates":             aggregates,
        "relationshipAggregates": relationship_aggregates,
        "relationshipFilterNote": relationship_filter_note,
        "defaultedTypeNote": defaulted_type_note,
        "excludedTypeNote": excluded_type_note,
    })


# ── Saved queries (Track A, EGERIA_INSIGHTS_QUERY_MODEL.md) ─────────────────
# Prototype of the doc's §2.3 interim state: a saved query is a `ResultsSet`
# collection (real Egeria Collection subtype — confirmed live 2026-08-05, see
# _cm()'s docstring for the "ResultSet" vs "ResultsSet" naming trap) whose
# `additionalProperties` holds the mechanism-agnostic spec (§2.1: a real,
# re-postable {url, httpMethod, body} — here specifically {"/api/insights/
# search", "POST", <SearchBody-shaped JSON>}, not a pyegeria-method-centric
# abstraction) and whose CollectionMembership holds the last-materialized
# results (§2.4's staleness model — "as of <lastRefreshedTime>", refresh is
# explicit, not automatic on every view).
#
# Marked with additionalProperties["pyegeriaInsightsQuery"] = "true" so this
# module's listing only surfaces Insights-authored ResultsSets, not any other
# ResultsSet that might exist in the repository for an unrelated purpose.
_QUERY_TYPE = "ResultsSet"
_QUERY_MARKER_KEY = "pyegeriaInsightsQuery"
_QUERY_MARKER_VALUE = "true"

# The subset of SearchBody that's actually filter logic — persisted as-is.
# Deliberately excludes: url/server/user_id/user_pwd (connection details, not
# part of the query) and full_count/start_from/page_size (execution
# parameters, override-able at the point of use per §2.2, not baked into the
# saved spec).
_SEARCH_SPEC_FIELDS = (
    "type_name", "match_criteria", "conditions", "value_conditions",
    "value_match_criteria", "relationship_conditions",
    "relationship_match_criteria", "exclude_types", "sort_by", "sort_dir", "as_of_time",
)


def _search_spec(search: SearchBody) -> dict:
    d = search.dict()
    return {k: d[k] for k in _SEARCH_SPEC_FIELDS if k in d}


def _saved_query_summary(el: dict) -> dict:
    header = el.get("elementHeader") or {}
    props = el.get("properties") or {}
    additional = props.get("additionalProperties") or {}
    try:
        spec = json.loads(additional.get("queryBody") or "{}")
    except Exception:  # noqa: BLE001 — a corrupted spec shouldn't break the whole list
        spec = {}
    result_count = additional.get("resultCount") or ""
    return {
        "guid":              header.get("guid", ""),
        "name":              props.get("displayName") or "",
        "description":       props.get("description") or "",
        "qualifiedName":     props.get("qualifiedName") or "",
        "spec":              spec,
        "lastRefreshedTime": additional.get("lastRefreshedTime") or None,
        "resultCount":       int(result_count) if result_count.isdigit() else None,
        "favorite":          additional.get("favorite") == "true",
    }


@router.post("/api/insights/queries", summary="Save a query (Track A prototype)")
def create_saved_query(body: SavedQueryBody = Body(...)):
    try:
        cm = _cm(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create CollectionManager for saved-query create")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    spec = _search_spec(body.search)
    qualified_name = f"ResultsSet::insights-query::{body.name}::{uuid.uuid4().hex[:8]}"
    create_body = {
        "class": "NewElementRequestBody",
        "isOwnAnchor": True,
        "properties": {
            "class": "CollectionProperties",
            "typeName": _QUERY_TYPE,
            "qualifiedName": qualified_name,
            "displayName": body.name,
            "description": body.description or "",
            "additionalProperties": {
                _QUERY_MARKER_KEY: _QUERY_MARKER_VALUE,
                "queryUrl": "/api/insights/search",
                "queryHttpMethod": "POST",
                "queryBody": json.dumps(spec),
                "lastRefreshedTime": "",
                "resultCount": "",
                "favorite": "false",
            },
        },
    }
    try:
        guid = cm.create_collection(body=create_body)
    except Exception as exc:
        logger.exception("insights: saved-query create failed")
        raise HTTPException(status_code=500, detail=str(exc))
    return JSONResponse({"guid": guid, "name": body.name})


@router.get("/api/insights/queries", summary="List saved queries (Track A prototype)")
def list_saved_queries(
    search_string: str = Query("*"),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        cm = _cm(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("insights: failed to create CollectionManager for saved-query list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        found = cm.find_collections(search_string=search_string or "*", starts_with=False,
                                     metadata_element_type_name=_QUERY_TYPE, output_format="JSON", page_size=200)
    except Exception as exc:
        logger.exception("insights: saved-query list failed")
        raise HTTPException(status_code=500, detail=str(exc))
    out = []
    for el in (found if isinstance(found, list) else []):
        if not isinstance(el, dict):
            continue
        additional = (el.get("properties") or {}).get("additionalProperties") or {}
        if additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
            continue  # a ResultsSet from elsewhere in the repo, not an Insights-authored saved query
        out.append(_saved_query_summary(el))
    out.sort(key=lambda q: (q["name"] or "").lower())
    return JSONResponse({"queries": out, "total": len(out)})


@router.get("/api/insights/queries/{guid}", summary="Load one saved query (spec + staleness)")
def get_saved_query(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        cm = _cm(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        el = cm.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Saved query not found: {exc}")
    additional = ((el or {}).get("properties") or {}).get("additionalProperties") or {}
    if additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
        raise HTTPException(status_code=404, detail="Not a saved Insights query")
    return JSONResponse(_saved_query_summary(el))


@router.put("/api/insights/queries/{guid}", summary="Update a saved query in place (rename/re-describe/edit conditions)")
def update_saved_query(guid: str, body: SavedQueryBody = Body(...)):
    try:
        cm = _cm(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        el = cm.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Saved query not found: {exc}")
    props = (el or {}).get("properties") or {}
    existing_additional = props.get("additionalProperties") or {}
    if existing_additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
        raise HTTPException(status_code=404, detail="Not a saved Insights query")

    spec = _search_spec(body.search)
    # Editing the filter logic doesn't itself materialize new results —
    # lastRefreshedTime/resultCount carry over untouched; use the refresh
    # action for that.
    additional = dict(existing_additional)
    additional["queryBody"] = json.dumps(spec)
    update_body = {
        "class": "UpdateElementRequestBody",
        "properties": {
            "class": "CollectionProperties",
            "qualifiedName": props.get("qualifiedName"),  # must be preserved — Egeria requires it on update
            "displayName": body.name,
            "description": body.description or "",
            "additionalProperties": additional,
        },
    }
    try:
        cm.update_collection(guid, update_body)
    except Exception as exc:
        logger.exception(f"insights: saved-query update failed for {guid}")
        raise HTTPException(status_code=500, detail=str(exc))
    return JSONResponse({"guid": guid, "name": body.name})


class FavoriteBody(BaseModel):
    favorite: bool
    url: Optional[str] = None
    server: Optional[str] = None
    user_id: Optional[str] = None
    user_pwd: Optional[str] = None


@router.post("/api/insights/queries/{guid}/favorite", summary="Star/unstar a saved query (shown on the Dashboard's Favorite Queries card)")
def set_saved_query_favorite(guid: str, body: FavoriteBody = Body(...)):
    try:
        cm = _cm(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        el = cm.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Saved query not found: {exc}")
    props = (el or {}).get("properties") or {}
    existing_additional = props.get("additionalProperties") or {}
    if existing_additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
        raise HTTPException(status_code=404, detail="Not a saved Insights query")

    additional = dict(existing_additional)
    additional["favorite"] = "true" if body.favorite else "false"
    update_body = {
        "class": "UpdateElementRequestBody",
        "properties": {
            "class": "CollectionProperties",
            "qualifiedName": props.get("qualifiedName"),
            "displayName": props.get("displayName"),
            "description": props.get("description") or "",
            "additionalProperties": additional,
        },
    }
    try:
        cm.update_collection(guid, update_body)
    except Exception as exc:
        logger.exception(f"insights: saved-query favorite toggle failed for {guid}")
        raise HTTPException(status_code=500, detail=str(exc))
    return JSONResponse({"guid": guid, "favorite": body.favorite})


@router.delete("/api/insights/queries/{guid}", summary="Delete a saved query")
def delete_saved_query(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        cm = _cm(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        el = cm.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Saved query not found: {exc}")
    additional = ((el or {}).get("properties") or {}).get("additionalProperties") or {}
    if additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
        raise HTTPException(status_code=404, detail="Not a saved Insights query")

    # BUG FOUND 2026-08-05 (live-verified while building this): Egeria's
    # cascade delete only removes elements the collection OWNS (isOwnAnchor);
    # CollectionMembership links to independently-anchored elements (every
    # real search result is one) block a plain delete with
    # OMAG-GENERIC-HANDLERS-403-005 ("still has a dependent ... element")
    # even with cascade=True. Unlink materialized members first, then delete
    # the now-empty ResultsSet.
    try:
        members = cm.get_collection_members(collection_guid=guid, output_format="JSON", page_size=500) or []
    except Exception:  # noqa: BLE001
        members = []
    for m in (members if isinstance(members, list) else []):
        g = ((m or {}).get("elementHeader") or {}).get("guid")
        if g:
            try:
                cm.remove_from_collection(guid, g)
            except Exception:  # noqa: BLE001
                logger.debug(f"insights: failed to unlink member {g} while deleting saved query {guid}")
    try:
        cm.delete_collection(guid)
    except Exception as exc:
        logger.exception(f"insights: saved-query delete failed for {guid}")
        raise HTTPException(status_code=500, detail=str(exc))
    return JSONResponse({"deleted": True, "guid": guid})


@router.get("/api/insights/queries/{guid}/results", summary="Cached materialized results for a saved query (no re-execution)")
def get_saved_query_results(
    guid: str,
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    try:
        cm = _cm(url, server, user_id, user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        members = cm.get_collection_members(collection_guid=guid, output_format="JSON", page_size=500)
    except Exception as exc:
        logger.exception(f"insights: failed to fetch cached members for saved query {guid}")
        raise HTTPException(status_code=500, detail=str(exc))
    results = [_serialize_member(m) for m in (members if isinstance(members, list) else []) if isinstance(m, dict)]
    return JSONResponse({"results": results, "total": len(results)})


@router.post("/api/insights/queries/{guid}/refresh", summary="Re-execute a saved query and materialize its ResultsSet membership")
def refresh_saved_query(guid: str, body: RefreshQueryBody = Body(...)):
    try:
        cm = _cm(body.url, body.server, body.user_id, body.user_pwd)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")
    try:
        el = cm.get_collection_by_guid(guid, output_format="JSON")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Saved query not found: {exc}")
    props = (el or {}).get("properties") or {}
    additional = props.get("additionalProperties") or {}
    if additional.get(_QUERY_MARKER_KEY) != _QUERY_MARKER_VALUE:
        raise HTTPException(status_code=404, detail="Not a saved Insights query")

    try:
        spec = json.loads(additional.get("queryBody") or "{}")
    except Exception:  # noqa: BLE001
        spec = {}
    if body.overrides:
        spec = {**spec, **body.overrides}  # §2.2 — the caller decides at point of use
    spec.setdefault("url", body.url)
    spec.setdefault("server", body.server)
    spec.setdefault("user_id", body.user_id)
    spec.setdefault("user_pwd", body.user_pwd)
    try:
        search = SearchBody(**spec)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Stored query spec is invalid: {exc}")

    # Re-run the query in-process — calls straight into search_elements()'s
    # own logic (classification+relationship+value filtering, defaulting,
    # etc.) rather than round-tripping this app's own HTTP layer.
    response = search_elements(search)
    payload = json.loads(response.body)
    hit_guids = {r["guid"] for r in payload.get("results", []) if r.get("guid")}

    # Diff against the ResultsSet's current CollectionMembership.
    try:
        current_members = cm.get_collection_members(collection_guid=guid, output_format="JSON", page_size=500) or []
    except Exception:  # noqa: BLE001
        current_members = []
    current_guids = {
        ((m or {}).get("elementHeader") or {}).get("guid")
        for m in (current_members if isinstance(current_members, list) else [])
        if isinstance(m, dict) and ((m or {}).get("elementHeader") or {}).get("guid")
    }

    added = hit_guids - current_guids
    removed = current_guids - hit_guids
    for g in added:
        try:
            cm.add_to_collection(guid, g, body={
                "class": "NewRelationshipRequestBody",
                "properties": {"class": "CollectionMembershipProperties",
                                "membershipRationale": "Insights saved-query result"},
            })
        except Exception:  # noqa: BLE001
            logger.debug(f"insights: failed to add member {g} to saved query {guid}")
    for g in removed:
        try:
            cm.remove_from_collection(guid, g)
        except Exception:  # noqa: BLE001
            logger.debug(f"insights: failed to remove stale member {g} from saved query {guid}")

    now = datetime.now(timezone.utc).isoformat()
    additional = dict(additional)
    additional["lastRefreshedTime"] = now
    additional["resultCount"] = str(len(hit_guids))
    update_body = {
        "class": "UpdateElementRequestBody",
        "properties": {
            "class": "CollectionProperties",
            "qualifiedName": props.get("qualifiedName"),
            "displayName": props.get("displayName"),
            "description": props.get("description") or "",
            "additionalProperties": additional,
        },
    }
    try:
        cm.update_collection(guid, update_body)
    except Exception:  # noqa: BLE001 — the refresh itself succeeded; failing to stamp the badge shouldn't fail the call
        logger.exception(f"insights: failed to stamp lastRefreshedTime on saved query {guid}")

    return JSONResponse({
        "guid": guid, "resultCount": len(hit_guids),
        "added": len(added), "removed": len(removed),
        "lastRefreshedTime": now,
    })
