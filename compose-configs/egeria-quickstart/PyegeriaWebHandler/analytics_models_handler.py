"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Analytics models and model runs for the Egeria Explorer ("Models and Runs", #analytics-models).

Endpoints:
  GET /api/analytics-models              -> the DeployedAnalyticsModel list
  GET /api/analytics-models/{guid}       -> one model: properties, runs, run metrics, projects and experiments,
                                            model sources
  GET /api/analytics-model-runs          -> the AnalyticsModelRun list
  GET /api/analytics-model-runs/{guid}   -> one run: dates, model, run metrics, projects and experiments, sources

The types (Egeria source 90232870b2; design note DESIGN-PORTAL-MODELS-2026-11-22.md):
  DeployedAnalyticsModel (DeployedSoftwareComponent) and AnalyticsModelRun (TransientEmbeddedProcess): Egeria 5.2.
  Experiment, a classification on Project (ProjectKind) with `hypothesis`: Egeria 5.0.
  ExternalModelSource (ExternalReference): Egeria 6.0.
  RunMetrics, a classification on Process (ElementHeader.runMetrics): Egeria 6.2.
  ProjectTarget (workedOnByProjects / projectTargets), the project link: Egeria 6.4.
None is 6.4-only, so no route is gated. What a run takes in and gives out is 6.4 (odpi/egeria#9463):
  ProcessingVariable (Referenceable -> DataValue; label, description, position; 0 = unset): the data values an
    element uses. Egeria gives it no direction, so parameters and results are one list in position order, and
    the label (when its author set one) is what tells them apart. The card says so.
  SupportedVariableType (Referenceable -> SchemaType; position, minCardinality, maxCardinality): the types of
    value an element accepts, i.e. a model's declared signature.
Those lists use C1's list_state (needs-6.4 words on a platform before 6.4). The 6.4 gate's cached answer is
also read for absent run metrics (RunMetrics is 6.2) and for the list routes' 404 rule: a bare 404 says
"the platform lacks the types" only when the version could not be read; on a platform whose version is
known (5.2 or later) a 404 is an error.

The other 6.4 lists (decisions, data values provided, Branch) come from e64_handler.serialize_related over the
card's own graph read, without the lists the card already shows; the general Relationships block repeats none of
the 6.4 lists (the S2 ruling).

No relationship type is reserved for model -> run (a run is a TransientEmbeddedProcess, so usually
ProcessHierarchy). So runs, models, projects and model sources are found by the related element's type across
every relationship list of the graph read, and each row carries its relationship type.

pyegeria (6.3.1 in the image, and release/next-6.4) has no wrappers for these types: the generic
ClassificationExplorer calls are used. Every route is async; token only (X-Egeria-Token).
"""
from __future__ import annotations

import re
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

import egeria_6_4_support as e64
from common_serialize import _authored_fields, _classifications, _generic_relationships, _header_summary
from e64_handler import (_by_position, _explorer_async, _gate, _is_template, _is_type, _list_of_type, _raise_http,
                         literal_value, serialize_related)
from egeria_error_mapping import EGERIA_ERROR_RESPONSES
from graph_keys import extract_graph_fields

router = APIRouter(tags=["analytics-models"])

MODEL_TYPE = "DeployedAnalyticsModel"
RUN_TYPE = "AnalyticsModelRun"
SOURCE_TYPE = "ExternalModelSource"
PROJECT_TYPE = "Project"

# RunMetrics properties in the order the card shows them (RunMetricsProperties, Egeria 6.2).
RUN_METRICS_FIELDS = ("runCount", "failedRunCount", "firstRunStartTime", "lastRunId", "lastRunStartTime",
                      "lastRunEndTime", "lastRunStatus", "lastRunDuration", "totalRunDuration", "lastRunRowsRead",
                      "lastRunRowsWritten", "lastRunBytesRead", "lastRunBytesWritten", "totalRowsRead",
                      "totalRowsWritten", "totalBytesRead", "totalBytesWritten")

_PROCESS_KEYS = ("expectedBehaviour", "formula", "formulaType", "implementationLanguage", "deployedImplementationType",
                 "versionIdentifier", "activityStatus", "userDefinedActivityStatus", "requestedTime",
                 "requestedStartTime", "startTime", "dueTime", "completionTime", "lastPauseTime", "lastResumeTime")
_NOT_IN_TABLE = {"class", "typeName", "extendedProperties", "additionalProperties", "description", "displayName",
                 *_PROCESS_KEYS}

# metrics states
METRICS_READ = "read"
METRICS_NONE = "none"            # the platform carries RunMetrics (6.2+) and this element has none
METRICS_NEEDS_6_2 = "needs-6.2"  # the platform is before 6.2: it can't record run metrics
METRICS_NOT_KNOWN = "not-known"  # none here, and the platform's version could not be read


def egeria_at_least(version: str, floor: tuple) -> Optional[bool]:
    """True/False when `version` ("6.3", "6.4-SNAPSHOT", "6.2.1 built ...") can be read, else None."""
    m = re.match(r"\s*(\d+)\.(\d+)(?:\.(\d+))?", version or "")
    if not m:
        return None
    nums = tuple(int(x) for x in m.groups(default="0"))
    return nums >= tuple(floor) + (0,) * (3 - len(floor))


def platform_has_run_metrics(carries: Optional[bool], version: str) -> Optional[bool]:
    if carries is True:
        return True                   # 6.4 or later
    return egeria_at_least(version, (6, 2))


def _clean(d: dict) -> dict:
    return {k: v for k, v in (d or {}).items() if k not in ("class", "typeName")}


def _classification(element: dict, name: str) -> Optional[dict]:
    """The named classification's properties wherever the 6.x header keeps it (its own key such as
    runMetrics, a family list, otherClassifications) or the older top-level list. {} when it carries no
    properties; None when the element doesn't have it."""
    h = e64.hdr(element)
    cands = []
    for val in h.values():
        cands.extend(val if isinstance(val, list) else [val])
    cands.extend((element.get("classifications") or []) if isinstance(element, dict) else [])
    for c in cands:
        if not isinstance(c, dict):
            continue
        cname = c.get("classificationName") or (c.get("type") or {}).get("typeName") or ""
        if cname == name:
            return _clean(c.get("classificationProperties") or c.get("properties") or {})
    return None


def run_metrics(element: dict, carries: Optional[bool], version: str, purl: str = "") -> dict:
    """{state, values?, words?}. Values keep only what Egeria recorded: an unrecorded value is absent, never 0."""
    cp = _classification(element, "RunMetrics")
    if cp is not None:
        values = {k: cp[k] for k in RUN_METRICS_FIELDS if cp.get(k) is not None and cp.get(k) != ""}
        extra = cp.get("additionalProperties") if isinstance(cp.get("additionalProperties"), dict) else {}
        return {"state": METRICS_READ, "values": values, "additionalProperties": extra}
    has = platform_has_run_metrics(carries, version)
    if has is False:
        where = f"the platform at {purl}" if purl else "this platform"
        return {"state": METRICS_NEEDS_6_2,
                "words": f"Run metrics need Egeria 6.2 (the RunMetrics classification): {where} runs Egeria {version}."}
    if has is None:
        return {"state": METRICS_NOT_KNOWN}
    return {"state": METRICS_NONE}


def _is_of(rel_el: dict, type_name: str) -> bool:
    t = e64.hdr(rel_el).get("type") or {}
    return t.get("typeName") == type_name or type_name in (t.get("superTypeNames") or [])


def related_of_type(element: dict, type_name: str) -> list:
    """One entry per relationship (any relationship list) whose related element is a `type_name`:
    (list key, entry, related element). A repeated relationship GUID is dropped (the same relationship can
    appear under two keys); a related element linked twice stays twice."""
    out, seen = [], set()
    fields = e64.relationship_fields()
    for key, val in (element.items() if isinstance(element, dict) else ()):
        if key not in fields and not (isinstance(val, list) and val and isinstance(val[0], dict)
                                      and "relatedElement" in val[0]):
            continue
        entries = val if isinstance(val, list) else ([val] if isinstance(val, dict) else [])
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("relatedElement"), dict):
                continue
            rel = entry["relatedElement"]
            if not _is_of(rel, type_name):
                continue
            rh = entry.get("relationshipHeader") or {}
            rg = rh.get("guid") or ""
            if rg:
                if rg in seen:
                    continue
                seen.add(rg)
            out.append((key, entry, rel))
    return out


def _row_base(key: str, entry: dict, rel: dict) -> dict:
    rh = entry.get("relationshipHeader") or {}
    p = e64.props(rel)
    guid = e64.hdr(rel).get("guid") or ""
    return {
        "relationshipGuid": rh.get("guid") or "",
        "relationshipType": (rh.get("type") or {}).get("typeName") or "",
        "listKey": key,
        "guid": guid,
        "typeName": e64.type_name(rel),
        "superTypeNames": (e64.hdr(rel).get("type") or {}).get("superTypeNames") or [],
        "displayName": e64.display_name(p, guid),
        "qualifiedName": p.get("qualifiedName") or "",
        "elementDescription": p.get("description") or "",
    }


def _run_row(key, entry, rel) -> dict:
    p = e64.props(rel)
    cp = _classification(rel, "RunMetrics")
    return {**_row_base(key, entry, rel),
            "activityStatus": p.get("activityStatus") or p.get("userDefinedActivityStatus") or "",
            "startTime": p.get("startTime") or "", "completionTime": p.get("completionTime") or "",
            "lastRunStatus": (cp or {}).get("lastRunStatus") or "", "hasRunMetrics": cp is not None}


def _sort_runs(rows: list) -> list:
    """Newest start first; runs with no start time after them, by name."""
    started = sorted([r for r in rows if r.get("startTime")], key=lambda r: str(r["startTime"]), reverse=True)
    rest = sorted([r for r in rows if not r.get("startTime")], key=lambda r: (r["displayName"] or "").lower())
    return started + rest


def run_rows(element: dict) -> list:
    return _sort_runs([_run_row(*t) for t in related_of_type(element, RUN_TYPE)])


def model_rows(element: dict) -> list:
    rows = []
    for key, entry, rel in related_of_type(element, MODEL_TYPE):
        p = e64.props(rel)
        rows.append({**_row_base(key, entry, rel), "implementationLanguage": p.get("implementationLanguage") or "",
                     "versionIdentifier": p.get("versionIdentifier") or ""})
    return sorted(rows, key=lambda r: (r["displayName"] or "").lower())


def project_rows(element: dict) -> list:
    rows = []
    for key, entry, rel in related_of_type(element, PROJECT_TYPE):
        exp = _classification(rel, "Experiment")
        rows.append({**_row_base(key, entry, rel), "isExperiment": exp is not None,
                     "hypothesis": (exp or {}).get("hypothesis") or "",
                     "label": _clean(entry.get("relationshipProperties") or {}).get("label") or ""})
    return sorted(rows, key=lambda r: (not r["isExperiment"], (r["displayName"] or "").lower()))


def source_rows(element: dict) -> list:
    rows = []
    for key, entry, rel in related_of_type(element, SOURCE_TYPE):
        p = e64.props(rel)
        rows.append({**_row_base(key, entry, rel), "url": p.get("url") or "",
                     "referenceVersion": p.get("referenceVersion") or "", "organization": p.get("organization") or ""})
    return sorted(rows, key=lambda r: (r["displayName"] or "").lower())


def _entries(element: dict, key: str) -> list:
    val = element.get(key) if isinstance(element, dict) else None
    entries = val if isinstance(val, list) else ([val] if isinstance(val, dict) else [])
    out, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("relatedElement"), dict):
            continue
        rg = (entry.get("relationshipHeader") or {}).get("guid") or ""
        if rg:
            if rg in seen:
                continue
            seen.add(rg)
        out.append(entry)
    return out


def processing_variable_rows(element: dict) -> list:
    """The data values the element uses (ProcessingVariable): one row per relationship, in position order, each
    with its value as the Data Value card shows it (literal_value)."""
    rows = []
    for entry in _entries(element, "processingVariables"):
        rel = entry["relatedElement"]
        p = e64.props(rel)
        rp = _clean(entry.get("relationshipProperties") or {})
        is_literal = _is_of(rel, "LiteralDataValue")
        rows.append({**_row_base("processingVariables", entry, rel),
                     "label": rp.get("label") or "", "description": rp.get("description") or "",
                     "position": rp.get("position"),
                     "dataType": p.get("dataType") or "", "dataFormat": p.get("dataFormat") or "",
                     "usage": p.get("usage") or "", "isLiteral": is_literal, "value": literal_value(p, is_literal)})
    return _by_position(rows)


def variable_type_rows(element: dict) -> list:
    """The types of value the element accepts (SupportedVariableType -> SchemaType), in position order."""
    rows = []
    for entry in _entries(element, "processVariableTypes"):
        rel = entry["relatedElement"]
        p = e64.props(rel)
        rp = _clean(entry.get("relationshipProperties") or {})
        rows.append({**_row_base("processVariableTypes", entry, rel),
                     "label": rp.get("label") or "", "description": rp.get("description") or "",
                     "position": rp.get("position"), "minCardinality": rp.get("minCardinality"),
                     "maxCardinality": rp.get("maxCardinality"), "dataType": p.get("dataType") or ""})
    return _by_position(rows)


# The 6.4 lists a Models and Runs card shows in its own sections; the related rows leave these out.
_SHOWN_E64 = ("processingVariables", "processVariableTypes", "workedOnByProjects", "projectTargets")


def related_rows_for_card(element: dict, carries: Optional[bool], words: str) -> dict:
    """e64_handler.serialize_related over this card's graph read (which asked for every list), without the lists
    the card already shows, and without sections left empty."""
    rel = serialize_related(element, carries, words, requested=e64.relationship_fields())
    sections = []
    for sec in rel["sections"]:
        lists = [lst for lst in sec["lists"] if lst["key"] not in _SHOWN_E64]
        if lists:
            sections.append({**sec, "lists": lists})
    return {**rel, "sections": sections, "carries": carries}


def _rows_state(rows: list) -> dict:
    """A graph read asks for every relationship list: rows = read, none = none."""
    return {"state": e64.READ if rows else e64.NONE}


def _projects_state(element: dict, rows: list, carries: Optional[bool], words: str) -> dict:
    """Rows found through any relationship = read. With none, the 6.4 ProjectTarget list decides the words, so
    a platform before 6.4 says "needs Egeria 6.4" rather than "none"."""
    if rows:
        return {"state": e64.READ}
    return e64.list_state(element, "workedOnByProjects", e64.relationship_fields(), carries, words)


def _serialize_common(element: dict, carries: Optional[bool], version: str, purl: str, what: str) -> dict:
    p = e64.props(element)
    h = e64.hdr(element)
    guid = h.get("guid", "")
    words = e64.needs_6_4_words(what, purl, version) if carries is False else ""
    projects = project_rows(element)
    variables = processing_variable_rows(element)
    requested = e64.relationship_fields()
    sources = source_rows(element)
    return {
        # flat, top-level keys: GenericPropertiesTable reads item[key]
        **{k: v for k, v in p.items() if k not in _NOT_IN_TABLE and v not in (None, "", [], {})},
        "guid": guid,
        "typeName": e64.type_name(element),
        "superTypeNames": (h.get("type") or {}).get("superTypeNames") or [],
        "displayName": e64.display_name(p, guid),
        "description": p.get("description") or "",
        "status": h.get("status") or "",
        **{k: (p.get(k) if p.get(k) is not None else "") for k in _PROCESS_KEYS},
        "additionalProperties": p.get("additionalProperties") or {},
        "mermaidGraph": element.get("mermaidGraph") or "",
        **{k: v for k, v in extract_graph_fields(element).items() if k != "mermaidGraph"},
        "_header": _header_summary(element),
        **_authored_fields(element),
        "classifications": _classifications(element),
        "runMetrics": run_metrics(element, carries, version, purl),
        "projects": projects,
        "sources": sources,
        "variables": variables,
        "lists": {"projects": _projects_state(element, projects, carries, words), "sources": _rows_state(sources),
                  "variables": e64.list_state(element, "processingVariables", requested, carries, words)},
        "related": related_rows_for_card(element, carries, words),
    }


def _shown_keys(element: dict, *types) -> set:
    """The relationship lists the card's own sections show, plus every 6.4 list (shown in the card's sections or
    its related rows): the general Relationships block repeats none of them."""
    return {k for t in types for k, _e, _r in related_of_type(element, t)} | set(e64.E64_LISTS)


def serialize_model(element: dict, carries: Optional[bool] = True, version: str = "", purl: str = "") -> dict:
    node = _serialize_common(element, carries, version, purl, "The model's 6.4 lists (projects, variables)")
    types = variable_type_rows(element)
    node["variableTypes"] = types
    node["lists"]["variableTypes"] = e64.list_state(element, "processVariableTypes", e64.relationship_fields(),
                                                    carries, e64.needs_6_4_words("The model's signature (SupportedVariableType)", purl, version) if carries is False else "")
    runs = run_rows(element)
    node["runs"] = runs
    node["lists"]["runs"] = _rows_state(runs)
    shown = _shown_keys(element, RUN_TYPE, PROJECT_TYPE, SOURCE_TYPE)
    node["relationships"] = _generic_relationships(element, skip=tuple(shown))
    return node


def serialize_run(element: dict, carries: Optional[bool] = True, version: str = "", purl: str = "") -> dict:
    node = _serialize_common(element, carries, version, purl, "The run's parameters and results (ProcessingVariable)")
    models = model_rows(element)
    node["models"] = models
    node["lists"]["models"] = _rows_state(models)
    shown = _shown_keys(element, MODEL_TYPE, PROJECT_TYPE, SOURCE_TYPE)
    node["relationships"] = _generic_relationships(element, skip=tuple(shown))
    return node


def serialize_model_list_item(el: dict) -> dict:
    p = e64.props(el)
    guid = e64.hdr(el).get("guid", "")
    return {"guid": guid, "typeName": e64.type_name(el), "displayName": e64.display_name(p, guid),
            "qualifiedName": p.get("qualifiedName") or "",
            "implementationLanguage": p.get("implementationLanguage") or "",
            "versionIdentifier": p.get("versionIdentifier") or "",
            "hasRunMetrics": _classification(el, "RunMetrics") is not None}


def serialize_run_list_item(el: dict) -> dict:
    p = e64.props(el)
    guid = e64.hdr(el).get("guid", "")
    return {"guid": guid, "typeName": e64.type_name(el), "displayName": e64.display_name(p, guid),
            "qualifiedName": p.get("qualifiedName") or "",
            "activityStatus": p.get("activityStatus") or p.get("userDefinedActivityStatus") or "",
            "startTime": p.get("startTime") or "", "completionTime": p.get("completionTime") or "",
            "hasRunMetrics": _classification(el, "RunMetrics") is not None}


def _needs_types(what: str, purl: str, version: str = "") -> JSONResponse:
    where = f"the platform at {purl}" if purl else "this platform"
    lead = f"{what} need Egeria 5.2 or later (DeployedAnalyticsModel, AnalyticsModelRun): {where}"
    tail = (f" runs Egeria {version}. Nothing was sent to Egeria." if version
            else " answered HTTP 404 for this type and its version could not be read, so none could be listed.")
    return JSONResponse({"needsVersion": True, "items": [], "total": 0, "words": lead + tail})


async def _list(type_name: str, what: str, serializer, include_templates: bool, url, server):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    if carries is False and egeria_at_least(version, (5, 2)) is False:
        return _needs_types(what, purl, version)          # known to predate the types: nothing is sent
    try:
        raw, capped = await _list_of_type(client, type_name)
    except Exception as exc:
        # A bare 404 means "the platform lacks the types" only when its version could not be read; on a
        # platform whose version is known (5.2 or later) it is a real error (the W1 rule).
        if carries is None and e64.is_missing_6_4_endpoint(exc):
            return _needs_types(what, purl or getattr(client, "platform_url", "") or "")
        _raise_http(exc, f"get_elements({type_name}) failed")
    if not include_templates:
        raw = [e for e in raw if not _is_template(e)]
    items = [serializer(e) for e in raw]
    items.sort(key=lambda x: (x["displayName"] or x["qualifiedName"]).lower())
    return JSONResponse({"items": items, "total": len(items), "capped": capped})


async def _card(guid: str, type_name: str, noun: str, serializer, url, server):
    try:
        client = await _explorer_async(url, server)
    except Exception as exc:
        _raise_http(exc, "ClassificationExplorer client failed")
    carries, version, purl = await _gate(client)
    try:
        raw = await client._async_get_element_by_guid(guid, element_type_name=type_name, graph_query_depth=1,
                                                      output_format="JSON")
    except Exception as exc:
        _raise_http(exc, f"get_element_by_guid({type_name}) failed")
    element = raw[0] if isinstance(raw, list) and raw else raw
    if not isinstance(element, dict) or not e64.hdr(element).get("guid"):
        raise HTTPException(status_code=404, detail=f"No element {guid!r} is visible to you. It may not exist, "
                                                    "or zone security may hide it.")
    if not _is_type(element, type_name):
        raise HTTPException(status_code=404, detail=f"{guid!r} is a {e64.type_name(element) or 'element'}, "
                                                    f"not {noun}.")
    return JSONResponse(serializer(element, carries, version, purl))


@router.get("/api/analytics-models", summary="List deployed analytics models", responses=EGERIA_ERROR_RESPONSES)
async def list_analytics_models(include_templates: bool = Query(False),
                                url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    return await _list(MODEL_TYPE, "Analytics models", serialize_model_list_item, include_templates, url, server)


@router.get("/api/analytics-models/{guid}", summary="Get a deployed analytics model with its runs and run metrics",
            responses=EGERIA_ERROR_RESPONSES)
async def get_analytics_model(guid: str, url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    return await _card(guid, MODEL_TYPE, "a DeployedAnalyticsModel", serialize_model, url, server)


@router.get("/api/analytics-model-runs", summary="List analytics model runs", responses=EGERIA_ERROR_RESPONSES)
async def list_analytics_model_runs(include_templates: bool = Query(False),
                                    url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    return await _list(RUN_TYPE, "Model runs", serialize_run_list_item, include_templates, url, server)


@router.get("/api/analytics-model-runs/{guid}", summary="Get an analytics model run with its model and run metrics",
            responses=EGERIA_ERROR_RESPONSES)
async def get_analytics_model_run(guid: str, url: Optional[str] = Query(None), server: Optional[str] = Query(None)):
    return await _card(guid, RUN_TYPE, "an AnalyticsModelRun", serializer=serialize_run, url=url, server=server)
