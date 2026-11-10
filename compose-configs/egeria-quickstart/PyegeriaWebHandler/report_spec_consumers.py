"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

"Used by": which tools each report spec is published to (report-spec consumer folders, phase 2).

A spec is published to a tool by being a member of that tool's consumer folder
(`ReportSpecFolder::Consumer::<Name>`, under the RootCollection `RootCollection::ReportSpecs`).
pyegeria's report-spec sync reads that tree and caches a consumer index, `{label: [consumer, ...]}`
(`pyegeria.view.egeria_spec_cache.read_consumer_index`, the release after 6.2.32). This module
turns it into the Report Specs view's "Used by" fields. It never reads Egeria itself.

Absence is never "none":
- the index was not read (no sync yet, the root not visible, or a pyegeria without the index)
  -> `usedByState` "not read" with the reason, for every spec;
- a spec held in Egeria that no consumer folder holds -> `usedBy` [] ("Used by: none");
- a built-in or local spec -> "not tracked": built-ins join the folders in phase 3 (references).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from loguru import logger

NOT_TRACKED = ("consumers are tracked for report specs held in Egeria; built-in and local specs "
               "are not consumer-folder members yet")
_TIER_PREFIXES = ("egeria:", "builtin:", "seed:")


def _pyegeria_version() -> str:
    try:
        from importlib.metadata import version
        return version("pyegeria")
    except Exception:  # noqa: BLE001
        return "(version unknown)"


def _not_read(reason: str, supported: bool = True) -> Dict[str, Any]:
    return {"status": "not read", "reason": reason, "root": None, "readAt": None, "readAs": None,
            "consumers": [], "index": {}, "supported": supported}


def index() -> Dict[str, Any]:
    """The consumer index as the last sync cached it, or "not read" with the reason. Never raises."""
    try:
        from pyegeria.view import egeria_spec_cache as esc
    except Exception as exc:  # noqa: BLE001
        return _not_read(f"pyegeria's report spec cache could not be loaded: {exc}", supported=False)
    reader = getattr(esc, "read_consumer_index", None)
    if reader is None:
        return _not_read(f"pyegeria {_pyegeria_version()} has no consumer index (it arrives in the release "
                         f"after 6.2.32)", supported=False)
    try:
        data = reader() or {}
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"report specs: the consumer index could not be read: {exc}")
        return _not_read(f"the consumer index could not be read: {type(exc).__name__}: {exc}")
    status = data.get("status") or "not read"
    return {"status": status, "reason": data.get("reason"), "root": data.get("root"),
            "readAt": data.get("read_at"), "readAs": data.get("read_as"),
            "consumers": [{k: c.get(k) for k in ("name", "qualifiedName", "status", "reason", "specs")}
                          for c in (data.get("consumers") or []) if isinstance(c, dict)],
            "index": dict(data.get("index") or {}) if status != "not read" else {},
            "supported": True}


def _label(name: str) -> str:
    for p in _TIER_PREFIXES:
        if name.startswith(p):
            return name[len(p):]
    return name


def used_by(name: str, source: Optional[str], egeria: Optional[dict], idx: Dict[str, Any]) -> Dict[str, Any]:
    """The "Used by" fields of one spec row: `usedBy` (list of consumer names, [] for none, or None
    when unknown), `usedByState` ("read" | "partial" | "not read" | "not tracked") and
    `usedByReason`."""
    status = idx.get("status") or "not read"
    if status == "not read":
        return {"usedBy": None, "usedByState": "not read", "usedByReason": idx.get("reason")}
    partial_reason = idx.get("reason") if status == "partial" else None
    names = (idx.get("index") or {}).get(_label(name))
    if names:
        return {"usedBy": list(names), "usedByState": status, "usedByReason": partial_reason}
    if source == "egeria" or egeria or name.startswith("egeria:"):
        return {"usedBy": [], "usedByState": status, "usedByReason": partial_reason}
    return {"usedBy": None, "usedByState": "not tracked", "usedByReason": NOT_TRACKED}


def summary(idx: Dict[str, Any]) -> Dict[str, Any]:
    """The response's top-level `consumers` block: how the index was read, without the index."""
    return {k: v for k, v in idx.items() if k != "index"}
