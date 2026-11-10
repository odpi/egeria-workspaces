"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

What the Portal says about a report spec's declarations and resolution (RS-W2-4).

pyegeria resolves every report spec when it loads (`pyegeria.view.spec_resolver`, RS-W2-2 PR-B):
a spec is runnable, unrunnable (with the resolver's own words), or format-only (no action; it
formats elements another call fetched). This module turns that, and the routine declarations in
`pyegeria.view.analytic_registry`, into JSON for /api/report-specs, /api/analytics and
/api/local-dashboards/{name}. It reads pyegeria's results; it never re-implements a check.

Three states, never two: a format-only spec is not broken and is never counted as unrunnable.

Every key is keyed on the existing spec `name`: nothing is renamed (Dashboard Sheets reach specs by
name through Egeria `Report` elements).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from loguru import logger

#: The stable prefix pyegeria's resolver puts on the warning for a spec that carried the removed
#: `analytic_binders` key (owner decision O1-a, pyegeria PR-0). Read from pyegeria when it has it,
#: so the tag lights up when that release lands and shows nothing before then.
BINDERS_DEPRECATED_PREFIX = "deprecated: analytic_binders ignored"

#: What the Portal's role supply (egeria_auth.PortalSupply) provides for each role kind. Stated,
#: not computed: it describes PortalSupply's behaviour for a reader of the UI.
PORTAL_SUPPLY_NOTE = (
    "In the Portal: each egeria_client:<Class> input is a client of that class for the signed-in "
    "user; viewer is the persona chosen in this browser; reader:<name> and subject inputs are not "
    "supplied, so a routine that declares one is refused before it runs."
)


def binders_prefix() -> str:
    try:
        from pyegeria.view import spec_resolver
        return getattr(spec_resolver, "BINDERS_DEPRECATED_PREFIX", BINDERS_DEPRECATED_PREFIX)
    except Exception:  # noqa: BLE001
        return BINDERS_DEPRECATED_PREFIX


def has_binders_warning(warnings: Optional[List[str]]) -> bool:
    prefix = binders_prefix()
    return any(isinstance(w, str) and w.startswith(prefix) for w in (warnings or []))


def resolve_all() -> Dict[str, Any]:
    """pyegeria's cached resolution of every registered spec, or {} on a pyegeria without the
    resolver (the Portal then shows no resolution rather than a wrong one)."""
    try:
        from pyegeria.view.spec_resolver import resolve_all as _resolve_all
    except ImportError:
        return {}
    try:
        return _resolve_all()
    except Exception as exc:  # noqa: BLE001 -- the listing must not go down with the resolver
        logger.warning(f"spec resolution unavailable: {exc}")
        return {}


def status_of(res: Any) -> Optional[str]:
    """'runnable' | 'unrunnable' | 'format_only', or None when not resolved."""
    if res is None:
        return None
    if getattr(res, "runnable", False):
        return "runnable"
    return "format_only" if getattr(res, "kind", "") == "format_only" else "unrunnable"


# ── Routine declarations ──────────────────────────────────────────────────────

def _field_rows(fields: List[Any]) -> List[Dict[str, Any]]:
    return [{"name": getattr(f, "name", ""), "label": getattr(f, "label", "") or "",
             "type": getattr(f, "type", "") or "", "kind": getattr(f, "kind", "") or ""}
            for f in fields or []]


def routine_out(entry: Any) -> Dict[str, Any]:
    """{outFields, outShape} for a registry entry. A shape name only the library registers reads as
    no fields in pyegeria (finding A2): outShape keeps its name so the UI can say so, rather than
    reading it as "no output"."""
    decl = getattr(entry, "declaration", None)
    out = getattr(decl, "out", None) if decl is not None else None
    fields: List[Any] = []
    try:
        fields = entry.routine().out_fields()
    except Exception:  # noqa: BLE001 -- an invalid declaration still shows what it can
        try:
            fields = decl.out_fields() if decl is not None and hasattr(decl, "out_fields") else []
        except Exception:  # noqa: BLE001
            fields = []
    shape = None
    if isinstance(out, str):
        shape = out
    elif isinstance(out, dict):
        shape = out.get("extends") or "inline shape"
    return {"outFields": _field_rows(fields), "outShape": shape, "outDeclared": decl is not None and out not in (None, [])}


def routine_params(entry: Any) -> List[Dict[str, Any]]:
    return [{"name": getattr(p, "name", ""), "type": getattr(p, "type", "str"),
             "required": bool(getattr(p, "required", False)), "default": getattr(p, "default", None),
             "category": getattr(p, "category", None) or "content",
             "description": getattr(p, "description", "") or ""}
            for p in (getattr(entry, "params", None) or [])]


def routine_entry(func_decl: Any) -> Any:
    if not func_decl:
        return None
    try:
        from pyegeria.view.spec_resolver import routine_entry as _routine_entry
        return _routine_entry(func_decl)
    except ImportError:
        pass
    except Exception:  # noqa: BLE001
        return None
    try:
        from pyegeria.view.analytic_registry import get_analytic_registry
        return get_analytic_registry().get(func_decl)
    except Exception:  # noqa: BLE001
        return None


def routine_fields(entry: Any) -> Dict[str, Any]:
    """The routine-declaration keys /api/analytics adds to each function."""
    target = ""
    try:
        target = entry.python_target()
    except Exception:  # noqa: BLE001
        target = getattr(entry, "function", "") or ""
    bindings = [{"kind": getattr(b, "kind", ""), "target": getattr(b, "target", "")}
                for b in (getattr(entry, "bindings", None) or [])]
    tile_safe = getattr(entry, "tile_safe", None)
    return {
        "kind":     getattr(entry, "kind", "routine") or "routine",
        "binding":  target,
        "bindings": bindings,
        "inputs":   list(getattr(entry, "inputs", None) or []),
        "tileSafe": tile_safe.model_dump() if hasattr(tile_safe, "model_dump") else None,
        **routine_out(entry),
    }


# ── A spec's resolution ───────────────────────────────────────────────────────

def _declared_params(action: Any) -> List[Dict[str, Any]]:
    """Every parameter a spec's action declares, with required/optional and, for an analytic
    routine's own, its category. Read from the spec and the routine declaration, not the resolver
    (which stops at the first failing check)."""
    if action is None:
        return []
    func = getattr(action, "function", "") or ""
    analytic = getattr(action, "analytic_function", None)
    owner = func or analytic or "spec"
    declared: Dict[str, Dict[str, Any]] = {}
    fixed: Dict[str, Any] = {}
    if analytic:
        fixed = dict(getattr(action, "analytic_spec_params", None) or {})
        entry = routine_entry(analytic)
        declared = {p["name"]: p for p in (routine_params(entry) if entry is not None else [])}
    rows: List[Dict[str, Any]] = []
    seen = set()

    def add(name: str, required: bool, stage: str) -> None:
        if name in seen:
            return
        seen.add(name)
        d = declared.get(name) if stage == analytic else None
        rows.append({"name": name, "required": required,
                     "category": d["category"] if d else None,
                     "default": fixed.get(name, d["default"] if d else None),
                     "stage": stage})

    for name in list(getattr(action, "required_params", None) or []):
        add(name, True, owner)
    for name in list(getattr(action, "optional_params", None) or []):
        add(name, False, owner)
    for name, d in declared.items():
        add(name, d["required"], analytic)
    return rows


def resolution(name: str, fs: Any, res: Any) -> Optional[Dict[str, Any]]:
    """The `resolution` object /api/report-specs adds to a spec; None when pyegeria has no resolver."""
    if res is None:
        return None
    status = status_of(res)
    action = getattr(fs, "action", None)
    out = {"outFields": [], "outShape": None, "outDeclared": False}
    analytic = getattr(action, "analytic_function", None) if action is not None else None
    if analytic:
        entry = routine_entry(analytic)
        if entry is not None:
            out = routine_out(entry)
    warnings = list(getattr(res, "warnings", None) or [])
    unrunnable = status == "unrunnable"
    tile_safe = getattr(res, "tile_safe", None)
    return {
        "status":        status,
        "runnable":      status == "runnable",
        "kind":          getattr(res, "kind", None),
        "targetType":    getattr(res, "target_type_name", None),
        "stages":        [dict(s) for s in (getattr(res, "stages", None) or [])],
        "params":        _declared_params(action),
        "roleInputs":    list(getattr(res, "role_inputs", None) or []),
        "outputFormats": list(getattr(res, "output_formats", None) or []),
        "outFields":     out["outFields"],
        "outShape":      out["outShape"],
        "outDeclared":   out["outDeclared"],
        "tileSafe":      tile_safe if isinstance(tile_safe, dict) else None,
        "words":         list(getattr(res, "words", None) or []) if status != "runnable" else None,
        "checks":        list(getattr(res, "checks", None) or []) if unrunnable else None,
        "notes":         list(getattr(res, "notes", None) or []),
        "warnings":      warnings,
        "bindersDeprecated": has_binders_warning(warnings),
    }


def counts(resolutions: Dict[str, Any], names) -> Dict[str, int]:
    c = {"runnable": 0, "unrunnable": 0, "formatOnly": 0, "unresolved": 0}
    for n in names:
        s = status_of(resolutions.get(n))
        key = {"runnable": "runnable", "unrunnable": "unrunnable", "format_only": "formatOnly"}.get(s, "unresolved")
        c[key] += 1
    return c


def _function_valued_param_refusal(analytic_params: Optional[Dict[str, Any]],
                                   action: Any = None) -> Optional[str]:
    """pyegeria's words refusing a function-valued parameter (e.g. metric_trend's `metric_path`)
    that a placement's own analyticParams supply, or None. The resolver checks only the spec's fixed
    analytic_spec_params; a dashboard Report's analyticParams override them at run time, so a
    placement can name a routine the spec never did. The check is pyegeria's own
    (resolve_report_spec_function, the call the routine makes at run time), not a re-implementation.
    Only parameters the spec's routine declares are checked, as the resolver does."""
    if not analytic_params:
        return None
    try:
        from pyegeria.view.spec_resolver import FUNCTION_VALUED_PARAMS
        from pyegeria.view.format_set_executor import AnalyticFunctionRefused, resolve_report_spec_function
    except ImportError:
        return None
    declared = None
    analytic = getattr(action, "analytic_function", None) if action is not None else None
    if analytic:
        entry = routine_entry(analytic)
        if entry is not None:
            declared = {getattr(p, "name", "") for p in (getattr(entry, "params", None) or [])}
    for param in FUNCTION_VALUED_PARAMS:
        value = analytic_params.get(param)
        if value in (None, "") or (declared is not None and param not in declared):
            continue
        try:
            resolve_report_spec_function(value)
        except AnalyticFunctionRefused as exc:
            return f"This placement's {param} '{value}' is refused: {exc}"
        except Exception as exc:  # noqa: BLE001 -- a resolver failure is not a verdict either way
            logger.debug(f"placement {param} {value!r} not checked: {exc}")
    return None


def placement_status(spec_name: Optional[str], resolutions: Dict[str, Any],
                     analytic_params: Optional[Dict[str, Any]] = None,
                     action: Any = None) -> Dict[str, Any]:
    """{runnable, refusal, bindersDeprecated} for a dashboard placement's spec. runnable is None when
    the spec is not resolved (unknown, not "runnable"); refusal is the resolver's words when not.
    A runnable spec is still refused when the placement's own analyticParams name a routine pyegeria
    refuses (a function-valued parameter such as metric_path)."""
    res = resolutions.get(spec_name) if spec_name else None
    if res is None:
        return {"runnable": None, "refusal": None, "bindersDeprecated": False}
    runnable = bool(getattr(res, "runnable", False))
    words = list(getattr(res, "words", None) or [])
    if runnable:
        param_refusal = _function_valued_param_refusal(analytic_params, action)
        if param_refusal:
            runnable, words = False, [param_refusal]
    return {
        "runnable": runnable,
        "refusal": None if runnable else (" ".join(words) or f"Spec '{spec_name}' cannot run."),
        "bindersDeprecated": has_binders_warning(getattr(res, "warnings", None)),
    }
