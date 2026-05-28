"""
pyegeria_docs_handler.py

Introspects the installed pyegeria package and serves API documentation.

GET /api/pyegeria-docs → {
    version: str,
    classes: [{
        name, module, summary, doc,
        methods: [{ name, signature, summary, doc }]
    }]
}

No Egeria connection required. Result is cached in memory after first call.
"""

import functools
import importlib
import inspect
import pkgutil
from typing import Any

import pyegeria
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


# ── helpers ───────────────────────────────────────────────────────────────────

def _clean_sig(method) -> str:
    """Return method signature string with 'self'/'cls' removed."""
    try:
        sig = inspect.signature(method)
        params = [p for n, p in sig.parameters.items() if n not in ("self", "cls")]
        return str(inspect.Signature(params))
    except Exception:
        return "(...)"


def _first_sentence(text: str) -> str:
    """Return the first non-blank sentence (up to '. ') of a docstring."""
    if not text:
        return ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            idx = stripped.find(". ")
            return stripped[: idx + 1] if idx >= 0 else stripped
    return ""


def _is_useful(name: str, obj: Any) -> bool:
    if not inspect.isclass(obj):
        return False
    if not obj.__module__.startswith("pyegeria"):
        return False
    if issubclass(obj, Exception):
        return False
    public = [m for m, _ in inspect.getmembers(obj, predicate=inspect.isfunction)
              if not m.startswith("_")]
    return len(public) > 0


# ── introspection (cached after first call) ───────────────────────────────────

@functools.lru_cache(maxsize=1)
def _build_docs() -> dict:
    version = getattr(pyegeria, "__version__", "unknown")
    seen: set[str] = set()
    classes: list[dict] = []

    def _add(name, obj):
        if name in seen or not _is_useful(name, obj):
            return
        seen.add(name)

        cls_doc = inspect.getdoc(obj) or ""
        methods = []
        for mname, member in sorted(
            inspect.getmembers(obj, predicate=inspect.isfunction)
        ):
            if mname.startswith("_"):
                continue
            doc = inspect.getdoc(member) or ""
            methods.append({
                "name": mname,
                "signature": _clean_sig(member),
                "summary": _first_sentence(doc),
                "doc": doc,
            })

        if methods:
            classes.append({
                "name": name,
                "module": obj.__module__,
                "summary": _first_sentence(cls_doc),
                "doc": cls_doc,
                "methods": methods,
            })

    # Top-level pyegeria namespace first (most user-visible)
    for name, obj in inspect.getmembers(pyegeria, inspect.isclass):
        _add(name, obj)

    # Walk sub-modules for any remaining classes
    pkg_path = getattr(pyegeria, "__path__", [])
    for _finder, mod_name, _is_pkg in pkgutil.walk_packages(pkg_path, prefix="pyegeria."):
        try:
            mod = importlib.import_module(mod_name)
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                _add(name, obj)
        except Exception:
            pass

    classes.sort(key=lambda c: c["name"].lower())
    return {"version": version, "classes": classes}


# ── route ─────────────────────────────────────────────────────────────────────

@router.get("/api/pyegeria-docs", summary="pyegeria class and method documentation")
def get_pyegeria_docs():
    """Introspected pyegeria API docs; cached in memory after first call."""
    return JSONResponse(_build_docs())
