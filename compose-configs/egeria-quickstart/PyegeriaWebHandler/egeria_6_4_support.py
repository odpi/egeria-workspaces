"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria 6.4 (odpi/egeria#9463, configuration values and decisions) support for the Egeria Explorer and Catalog cards:
the version gate, the 14 new relationship lists, and the rule that tells "needs Egeria 6.4", "not read"
and "none" apart. Used by e64_handler.py.

The version gate
----------------
pyegeria has the gate as ``pyegeria.core.egeria_6_4_gate`` from the release after 6.3.1 (egeria-python
branch release/next-6.4). The Portal image may run an older pyegeria, so the import is guarded: when the
module is missing, the copy below is used. It gives the same answers and the same words (tests/
test_e64_gate.py checks both against the same cases). ``GATE_SOURCE`` says which one is in use. Drop the
copy once the Portal's pyegeria floor carries the module.

On an Egeria before 6.4 the new requests 404 and the new lists are absent. A card then says "needs Egeria
6.4" in words: never an error, and never "none".

The absence rule
----------------
Egeria leaves an empty relationship list out of its answer. So an absent list means "none" only when it was
asked for (a graph read of an element on a platform that has the list). A list that was not asked for is
"not read". On a platform without 6.4 it is "needs Egeria 6.4", and when the platform's version could not
be read it is "not known", never "none".
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime
from typing import Any, Optional

from loguru import logger

# ── The gate: pyegeria's when it has it, else this copy ──────────────────────────────────────────────────

try:  # pragma: no cover - which branch runs depends on the installed pyegeria
    from pyegeria.core.egeria_6_4_gate import (  # type: ignore[import-not-found]
        async_egeria_6_4_status, carries_6_4, clear_cache, is_missing_6_4_endpoint, needs_6_4_words,
    )
    GATE_SOURCE = "pyegeria"
except ImportError:
    GATE_SOURCE = "vendored"

    # A copy of pyegeria/core/egeria_6_4_gate.py (egeria-python release/next-6.4, 5bf2a53e). Keep the
    # answers and the words identical: tests/test_e64_gate.py runs the same cases on both.
    EGERIA_6_4_SNAPSHOT_CUTOFF = "2026-11-21T19:51:36Z"
    GATE_TTL_SECONDS = 3600
    GATE_FAILED_TTL_SECONDS = 60
    GATE_ABOUT_TIMEOUT_SECONDS = 5
    _CACHE: dict = {}

    def carries_6_4(about: Any) -> tuple:
        try:
            if isinstance(about, (str, bytes)):
                about = json.loads(about)
            if not isinstance(about, dict):
                return None, ""
            version = str(about.get("version") or "").strip()
            m = re.fullmatch(r"(\d+)\.(\d+)(?:\.(\d+))?(-SNAPSHOT)?", version)
            if not m:
                return None, version
            numbers = tuple(int(g or 0) for g in m.groups()[:3])
            if not m.group(4):
                return numbers >= (6, 4, 0), version
            if numbers[:2] > (6, 4):
                return True, version
            if numbers[:2] < (6, 4):
                return False, version
            built = about.get("time")
            if not built:
                return None, version
            when = datetime.fromisoformat(str(built).replace("Z", "+00:00"))
            cutoff = datetime.fromisoformat(EGERIA_6_4_SNAPSHOT_CUTOFF.replace("Z", "+00:00"))
            if when.tzinfo is None:
                return None, version
            return when >= cutoff, f"{version} built {built}"
        except Exception:  # noqa: BLE001 -- an unreadable answer is unknown, never "no"
            return None, ""

    def needs_6_4_words(what: str, platform_url: str = "", version: str = "") -> str:
        where = f"the platform at {platform_url}" if platform_url else "this platform"
        lead = f"{what} needs Egeria 6.4 (odpi/egeria#9463, configuration values and decisions): {where}"
        if version:
            return f"{lead} runs Egeria {version}. Nothing was sent to Egeria."
        return f"{lead} does not serve this request (HTTP 404), so nothing was changed."

    def is_missing_6_4_endpoint(exc: BaseException) -> bool:
        from pyegeria.core._exceptions import PyegeriaClientException
        return isinstance(exc, PyegeriaClientException) and getattr(exc, "http_status_code", None) == 404

    def _about_reader(client: Any):
        reader = getattr(client, "async_get_platform_origin", None)
        if reader is None:
            for sub in ("classification_manager", "metadata_expert"):
                inner = getattr(client, sub, None)
                reader = getattr(inner, "async_get_platform_origin", None) if inner is not None else None
                if reader is not None:
                    break
        return reader

    async def async_egeria_6_4_status(client: Any) -> tuple:
        url = getattr(client, "platform_url", None)
        if not isinstance(url, str) or not url:
            return None, "", ""
        hit = _CACHE.get(url)
        if hit is not None and hit[0] > time.monotonic():
            return hit[1], hit[2], url
        about = None
        try:
            reader = _about_reader(client)
            if reader is not None:
                import asyncio
                about = await asyncio.wait_for(reader(), timeout=GATE_ABOUT_TIMEOUT_SECONDS)
        except Exception as e:  # noqa: BLE001 -- a failed about-read is "unknown"
            logger.debug(f"Egeria 6.4 gate: could not read {url}/api/about: {e}")
        carries, version = carries_6_4(about) if about else (None, "")
        ttl = GATE_TTL_SECONDS if about else GATE_FAILED_TTL_SECONDS
        _CACHE[url] = (time.monotonic() + ttl, carries, version)
        return carries, version, url

    def clear_cache() -> None:
        _CACHE.clear()


# ── The 14 lists #9463 adds to OpenMetadataRootElement, and the relationship each reads ──────────────────
# The same table as pyegeria.core.egeria_6_4_names.ROOT_ELEMENT_LISTS and the 6.4 rows of
# pyegeria.view.egeria_relationship_fields.RELATIONSHIP_FIELDS (egeria-python release/next-6.4, generated
# from Egeria 0dbf4687 = 90232870b2). tests/fixtures/egeria_6_4_relationship_fields.json is that generated
# table's 6.4 rows; tests/test_e64_absence_rule.py checks this copy against it, and against the installed
# pyegeria's table once that carries them.
E64_LISTS: dict = {
    "decisionOutcomes": "Outcome",
    "associatedDecisions": "Outcome",
    "inputsToDecision": "Assessment",
    "assessmentDecisions": "Assessment",
    "projectTargets": "ProjectTarget",
    "workedOnByProjects": "ProjectTarget",
    "processingVariables": "ProcessingVariable",
    "dataValueUses": "ProcessingVariable",
    "embeddedDataValues": "EmbeddedDataValue",
    "parentDataValues": "EmbeddedDataValue",
    "dataValueSources": "DataValueSource",
    "providesDataValues": "DataValueSource",
    "processVariableTypes": "SupportedVariableType",
    "processVariableTypeUses": "SupportedVariableType",
}

E64_TYPES = frozenset({"Decision", "DataValue", "LiteralDataValue"})


def relationship_fields() -> dict:
    """RELATIONSHIP_FIELDS: the installed pyegeria's generated table, with the 6.4 rows added when it is a
    release that predates them (6.3.x has 285 lists and none of the 14)."""
    try:
        from pyegeria.view.egeria_relationship_fields import RELATIONSHIP_FIELDS as installed
        fields = dict(installed)
    except ImportError:
        fields = {}
    for key, rel_type in E64_LISTS.items():
        fields.setdefault(key, (rel_type,))
    return fields


# List states. The UI words are in type-explorer.html (e64ListWords); the backend sends the state and,
# for needs-6.4, the gate's own sentence.
NEEDS_6_4 = "needs-6.4"
NOT_KNOWN = "not-known"    # the platform's version could not be read, and the list is absent
NOT_READ = "not-read"      # the list was not asked for
NONE = "none"              # asked for, and Egeria returned none
READ = "read"              # asked for, with entries


def list_state(element: dict, key: str, requested, carries: Optional[bool], words: str = "") -> dict:
    """{"state", "words"?} for one relationship list on a read element.

    `requested`: the list keys the read asked for. A graph read (graph_query_depth >= 1) of a whole element
    asks for every RELATIONSHIP_FIELDS list, so callers pass relationship_fields() then, and an empty set
    for a properties-only read.
    `carries`: the gate's answer for the platform (True, False or None = not known).
    `words`: the gate's sentence, shown with needs-6.4."""
    value = element.get(key) if isinstance(element, dict) else None
    present = bool(value) if isinstance(value, (list, dict)) else value is not None
    if key not in relationship_fields() or key not in requested:
        return {"state": NOT_READ}
    if present:
        return {"state": READ}
    if key in E64_LISTS:
        if carries is False:
            return {"state": NEEDS_6_4, "words": words}
        if carries is None:
            return {"state": NOT_KNOWN}
    return {"state": NONE}


# ── Serialization helpers shared by the 6.4 cards ────────────────────────────────────────────────────────

def hdr(el: dict) -> dict:
    return (el.get("elementHeader") or {}) if isinstance(el, dict) else {}


def props(el: dict) -> dict:
    return (el.get("properties") or {}) if isinstance(el, dict) else {}


def type_name(el: dict) -> str:
    return (hdr(el).get("type") or {}).get("typeName") or ""


def display_name(p: dict, guid: str = "") -> str:
    return p.get("displayName") or p.get("name") or p.get("qualifiedName") or guid


def _rel_props(entry: dict) -> dict:
    return {k: v for k, v in (entry.get("relationshipProperties") or {}).items()
            if k not in ("class", "typeName")}


def related_rows(element: dict, key: str, rel_fields: tuple) -> list:
    """One row per relationship in element[key]: the related element plus the named relationship
    properties, keyed by the relationship GUID.

    Rows are never merged by the related element's GUID: an Assessment list names one element once per
    assessment. Only a repeated relationship GUID (the same relationship twice) is dropped."""
    val = element.get(key) if isinstance(element, dict) else None
    entries = val if isinstance(val, list) else ([val] if isinstance(val, dict) else [])
    rows, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rel_guid = (entry.get("relationshipHeader") or {}).get("guid") or ""
        if rel_guid:
            if rel_guid in seen:
                continue
            seen.add(rel_guid)
        rel = entry.get("relatedElement") if isinstance(entry.get("relatedElement"), dict) else entry
        rh, rp = hdr(rel), props(rel)
        guid = rh.get("guid") or ""
        rprops = _rel_props(entry)
        row = {
            "relationshipGuid": rel_guid,
            "relationshipType": ((entry.get("relationshipHeader") or {}).get("type") or {}).get("typeName") or "",
            "guid": guid,
            "typeName": type_name(rel),
            "superTypeNames": (rh.get("type") or {}).get("superTypeNames") or [],
            "displayName": display_name(rp, guid),
            "qualifiedName": rp.get("qualifiedName") or "",
            "elementDescription": rp.get("description") or "",
        }
        for f in rel_fields:
            v = rprops.get(f)
            row[f] = v if v is not None else ("" if f not in ("position", "minCardinality", "maxCardinality",
                                                                "additionalProperties") else None)
        rows.append(row)
    return rows


def classification_names(element: dict) -> list:
    """Every classification name on the element, wherever the 6.x header keeps it (its own key, a family
    list, otherClassifications) or the older top-level `classifications` list."""
    names, found = [], []
    h = hdr(element)
    for val in h.values():
        for c in (val if isinstance(val, list) else [val]):
            if isinstance(c, dict) and c.get("classificationName"):
                found.append(c)
    for c in element.get("classifications") or [] if isinstance(element, dict) else []:
        if isinstance(c, dict):
            found.append(c)
    for c in found:
        n = c.get("classificationName") or (c.get("type") or {}).get("typeName") or ""
        if n and n not in names:
            names.append(n)
    return names


def branch_of(element: dict) -> Optional[dict]:
    """The Branch classification's properties (displayName, scope, purpose, url), or None."""
    h = hdr(element)
    cands = []
    for val in h.values():
        cands.extend(val if isinstance(val, list) else [val])
    cands.extend((element.get("classifications") or []) if isinstance(element, dict) else [])
    for c in cands:
        if not isinstance(c, dict):
            continue
        name = c.get("classificationName") or (c.get("type") or {}).get("typeName") or ""
        if name == "Branch":
            cp = c.get("classificationProperties") or c.get("properties") or {}
            return {k: cp.get(k) or "" for k in ("displayName", "scope", "purpose", "url")}
    return None
