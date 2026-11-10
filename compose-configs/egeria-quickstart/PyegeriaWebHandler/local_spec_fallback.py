"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The Portal's own report specs as fallbacks for their Egeria-held copies.

The Portal defines two report specs in code:

- "Analytic - Generic Metric Trend" (here), which runs the built-in analytic `metric_trend`;
- "Resource Explorer - Curation Coverage" (re_analytics.py), which runs
  `re_curation_coverage_tile`, an analytic the Portal registers.

Both are also held in Egeria, in the CollectionFolder `ReportSpecFolder::EgeriaPortal`, which
report_spec_sync.py syncs into pyegeria's EGERIA tier. pyegeria resolves a label local > egeria >
builtin, so a local copy registered in the RUNTIME tier would always shadow the Egeria copy.
`reconcile()` therefore registers a local copy only while the EGERIA tier does not hold that
label, and removes it once the tier does:

- Egeria holds the label: the Egeria copy is the source; no local copy is registered.
- Egeria does not hold it (cold cache, folder emptied, spec pruned, a spec the sync skipped):
  the local copy is registered, so the tiles never break.

An Egeria outage does not change this: a failed sync keeps the cache it had.

`reconcile()` runs when report_specs_handler.py and analytics_registry_handler.py load, and
after every sync (report_spec_sync.py). It never raises.

Order matters for the Curation Coverage spec: the EGERIA tier refuses a cached spec whose
analytic is not registered, and keeps that refusal until its cache changes. So `reconcile()`
registers `re_curation_coverage_tile` first and then reloads the tier (`force=True`).
"""

from __future__ import annotations

import threading
from typing import Callable, Dict, List, Tuple

from loguru import logger

METRIC_TREND_LABEL = "Analytic - Generic Metric Trend"
WORKSPACE_LOCAL_SOURCE = "workspace_local"
RE_ANALYTICS_SOURCE = "re_analytics"

_LOCK = threading.Lock()
_LAST: Dict[str, str] = {}   # label -> "egeria" | "local" | "error: ..." from the last reconcile


def metric_trend_specs():
    """The Generic Metric Trend spec, keyed by its label. The Egeria-held copy must match it
    (egeria-held-specs/PORTAL_REPORT_SPECS.dr-egeria.md; tests/test_local_spec_fallback.py checks it)."""
    from pyegeria.view._output_format_models import ActionParameter, Format, FormatSet, FormatSetDict
    return FormatSetDict({METRIC_TREND_LABEL: FormatSet(
        heading="Generic Metric Trend",
        description="Trend any analytic function over time. metric_path is the target function; "
                    "metric_params are its keyword arguments. Default trends count_elements(type_name=Asset).",
        family="Analytic",
        target_type=None,
        formats=[Format(types=["DICT", "JSON", "SERIES"], attributes=[])],
        action=ActionParameter(
            function="",
            analytic_function="metric_trend",
            analytic_spec_params={
                "metric_path": "count_elements",
                "metric_params": {"type_name": "Asset"},
                "window": "6mo",
            },
        ),
    )})


def _curation_coverage_specs():
    import re_analytics
    return re_analytics.report_specs()


def fallbacks() -> List[Tuple[str, str, Callable]]:
    """(label, RUNTIME source, builder) for every Portal spec that has an Egeria-held copy."""
    import re_analytics
    return [
        (METRIC_TREND_LABEL, WORKSPACE_LOCAL_SOURCE, metric_trend_specs),
        (re_analytics.TILE_LABEL, RE_ANALYTICS_SOURCE, _curation_coverage_specs),
    ]


def _register_analytics() -> None:
    """Register the analytic functions the specs name, before the EGERIA tier is (re)loaded."""
    try:
        import re_analytics
        re_analytics.register_tile_function()
    except Exception as exc:  # noqa: BLE001 -- never stop the app over an optional analytic
        logger.warning(f"report-spec fallback: could not register the Resource Explorer tile function: {exc}")


def _egeria_labels() -> set:
    from pyegeria.view.egeria_spec_cache import egeria_tier
    return set(egeria_tier(force=True).keys())


def _registered_by(label: str) -> str | None:
    from pyegeria.view import base_report_formats as brf
    return getattr(brf, "_RUNTIME_REPORT_SOURCES", {}).get(label)


def reconcile() -> Dict[str, str]:
    """Register or remove each local copy by whether the EGERIA tier holds its label.
    Returns label -> "egeria" | "local" | "error: <words>". Never raises."""
    from pyegeria.view.base_report_formats import (ReportFormatCollision, register_report_specs,
                                                   unregister_report_spec)
    out: Dict[str, str] = {}
    with _LOCK:
        _register_analytics()
        try:
            held = _egeria_labels()
        except Exception as exc:  # noqa: BLE001 -- no tier means no Egeria copy: use the local one
            logger.warning(f"report-spec fallback: EGERIA tier unavailable, using local copies: {exc}")
            held = set()
        try:
            entries = fallbacks()
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"report-spec fallback: could not list the local specs: {exc}")
            entries = []
        for label, source, build in entries:
            try:
                if label in held:
                    if _registered_by(label) == source:
                        unregister_report_spec(label)
                        logger.info(f"report spec '{label}': Egeria holds it; the local copy is withdrawn")
                    out[label] = "egeria"
                    continue
                if _registered_by(label) != source:
                    try:
                        register_report_specs(build(), source=source)
                    except ReportFormatCollision:
                        logger.debug(f"report spec '{label}': already registered")
                    if _LAST.get(label) == "egeria":
                        logger.info(f"report spec '{label}': Egeria no longer holds it; using the local copy")
                out[label] = "local"
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"report-spec fallback: '{label}': {exc}")
                out[label] = f"error: {exc}"[:300]
        _LAST.clear()
        _LAST.update(out)
    return dict(out)


def last() -> Dict[str, str]:
    """The result of the last reconcile (label -> where the spec is served from)."""
    with _LOCK:
        return dict(_LAST)
