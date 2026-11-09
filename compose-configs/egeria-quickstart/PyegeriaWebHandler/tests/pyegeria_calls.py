"""Static scan for calls to pyegeria methods that do not exist (renamed or removed) or that now warn.

pyegeria renamed get_external_identifier_by_guid to get_external_identifiers_by_guid in 6.1.0 and kept no
alias; the Portal's External Identifiers detail 500'd for three months. A call like that is only an
AttributeError at request time, so nothing short of hitting the exact page finds it. This module finds it
without Egeria: it parses the source, works out which variables hold a pyegeria client, and checks every
method called on them against the installed pyegeria.

How a receiver gets a type (per function scope, enclosing scopes inherited):
  * ``x = SomeClient(...)`` where SomeClient was imported from pyegeria (or md_processing), or
    ``pyegeria.SomeClient(...)`` / ``pe.SomeClient(...)`` through a module alias;
  * ``x = factory(...)`` / ``x = await factory(...)`` where ``factory`` is a function in the same
    module that returns a client (worked out to a fixed point, so factories of factories resolve), or
    is annotated ``-> SomeClient``;
  * ``with SomeClient(...) as x`` and parameters annotated ``x: SomeClient``.

A variable that is also assigned something that is not a client in the same scope is left untyped.

Checks:
  * strict: a typed receiver's ``x.method(...)``, ``x.method`` passed as a callable, and
    ``getattr(x, "method")`` must exist on its class. EgeriaTech / EgeriaClient delegate through
    ``__getattr__`` to their sub-clients, so their method set includes every sub-client's.
  * loose: an untyped receiver whose name is client-like (``mgr``, ``client``, ...) calling a name
    shaped like a pyegeria verb (``get_``, ``find_``, ``_async_create_``, ...) must name a method of
    SOME pyegeria class. ``client`` is httpx or docker in places; the verb filter keeps those out.
  * imports: every name imported from pyegeria / md_processing exists.
  * deprecated: calls to pyegeria methods that issue a DeprecationWarning, and keyword arguments
    pyegeria now reports as deprecated (request_filters.DEPRECATED_NAMES).

Run as a script on .py or .ipynb paths (needs the pyegeria to check against on the path):
    python3 tests/pyegeria_calls.py path/to/file.py path/to/notebook.ipynb ...
"""
from __future__ import annotations

import ast
import functools
import importlib
import inspect
import json
import pkgutil
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

LIB_ROOTS = ("pyegeria", "md_processing")

# Names the code gives a pyegeria client when the scan cannot type it. Only consulted together with VERB.
CLIENTISH = {
    "mgr", "mgr2", "manager", "expert", "classifier", "client", "c", "cm", "rm", "vmm", "ce", "dd", "ac",
    "am", "gm", "go", "sa", "so", "pm", "egeria", "egeria_tech", "egeria_client", "tech", "ec", "et",
    "a_client", "g_client", "o_client", "r_client", "s_client", "p_client", "t_client", "m_client",
    "client_obj", "explorer", "designer", "curator", "officer", "architect", "maker", "registry",
}
VERB = re.compile(
    r"^(_async_)?(get|find|create|update|delete|link|detach|attach|add|remove|set|clear|publish|withdraw|"
    r"setup|unlink|classify|declassify|reclassify|archive|initiate|refresh|validate|deploy|load|purge|"
    r"activate|shutdown|restart|retrieve|reset|register|select|assign|unassign|start|stop|issue|"
    r"list|search|make|run)_")


# --------------------------------------------------------------------------- what pyegeria offers

@functools.lru_cache(maxsize=None)
def _lib_modules() -> tuple:
    mods = []
    for root in LIB_ROOTS:
        try:
            pkg = importlib.import_module(root)
        except Exception:  # noqa: BLE001 -- md_processing may be absent
            continue
        mods.append(pkg)
        for mi in pkgutil.walk_packages(getattr(pkg, "__path__", []), root + "."):
            if mi.name.endswith("__main__"):
                continue
            try:
                mods.append(importlib.import_module(mi.name))
            except BaseException:  # noqa: BLE001 -- optional extras; their classes are just not known
                continue
    return tuple(mods)


def _is_lib_class(obj) -> bool:
    return inspect.isclass(obj) and (getattr(obj, "__module__", "") or "").split(".")[0] in LIB_ROOTS


@functools.lru_cache(maxsize=None)
def all_lib_names() -> frozenset:
    """Every attribute of every pyegeria/md_processing class, and every module-level function name."""
    names = set()
    for mod in _lib_modules():
        for n, obj in vars(mod).items():
            if _is_lib_class(obj):
                names.update(class_methods(obj))
            elif inspect.isfunction(obj):
                names.add(n)
    return frozenset(names)


def _delegates(cls) -> set:
    """Classes an EgeriaTech-style ``__getattr__`` hands unknown names to."""
    out = set()
    try:
        mod = sys.modules[cls.__module__]
        tree = ast.parse(inspect.getsource(cls))
    except (OSError, TypeError, KeyError, SyntaxError):
        return out
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for v in node.values:
                if isinstance(v, ast.Name) and _is_lib_class(getattr(mod, v.id, None)):
                    out.add(getattr(mod, v.id))
    return out


@functools.lru_cache(maxsize=None)
def class_methods(cls) -> frozenset:
    names = set(dir(cls))
    has_getattr = any("__getattr__" in vars(k) for k in cls.__mro__ if k is not object)
    if has_getattr:
        for d in _delegates(cls):
            names.update(class_methods(d))
    return frozenset(names)


def _warns_deprecation(fn_node: ast.AST) -> bool:
    for n in ast.walk(fn_node):
        if isinstance(n, ast.Call):
            f = ast.unparse(n.func)
            if f in ("warnings.warn", "warn") and any("DeprecationWarning" in ast.unparse(a) for a in n.args[1:]):
                return True
            if re.match(r"^_?(warn_|_warn_)\w*$|^_subject_area_moved$", f.split(".")[-1]):
                return True
    return False


@functools.lru_cache(maxsize=None)
def deprecated_methods() -> dict:
    """{public method name: 'Class'} for pyegeria client methods whose body issues a DeprecationWarning.

    Only methods that warn unconditionally on being called count; a method that warns for one
    deprecated *parameter* is covered by deprecated_kwargs instead."""
    out = {}
    for mod in _lib_modules():
        if not mod.__name__.startswith("pyegeria.omvs"):
            continue
        try:
            tree = ast.parse(inspect.getsource(mod))
        except (OSError, TypeError, SyntaxError):
            continue
        for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
            for fn in [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
                if fn.name.startswith("__") or re.match(r"^_?_?warn|^_subject_area_moved$", fn.name):
                    continue   # the warning helpers themselves
                # unconditional: a warn call that is a direct statement of the body (not under an if)
                for stmt in fn.body:
                    if isinstance(stmt, ast.Expr) and _warns_deprecation(stmt):
                        # keyed on the public name: the sync wrapper calls the _async_ body that warns
                        out[fn.name[len("_async_"):] if fn.name.startswith("_async_") else fn.name] = cls.name
                        break
    return out


@functools.lru_cache(maxsize=None)
def deprecated_kwargs() -> dict:
    try:
        from pyegeria.core.request_filters import DEPRECATED_NAMES
        return dict(DEPRECATED_NAMES)
    except Exception:  # noqa: BLE001
        return {}


# --------------------------------------------------------------------------- the scan

@dataclass
class Finding:
    kind: str          # missing | missing-loose | import | deprecated | deprecated-kwarg
    file: str
    line: int
    receiver: str
    name: str
    detail: str = ""

    def __str__(self):
        return f"{self.file}:{self.line}\t{self.kind}\t{self.receiver}.{self.name}\t{self.detail}"


@dataclass
class Report:
    findings: list = field(default_factory=list)
    typed_calls: int = 0       # calls checked against a known class
    loose_calls: int = 0       # calls checked against the union of all classes
    files: int = 0


_UNTYPED = object()   # a name that is also bound to something that is not a client


def _resolve_import(module: str, name: str):
    try:
        mod = importlib.import_module(module)
    except Exception:  # noqa: BLE001
        return _UNTYPED
    if hasattr(mod, name):
        return getattr(mod, name)
    try:
        return importlib.import_module(f"{module}.{name}")
    except Exception:  # noqa: BLE001
        return _UNTYPED


class _ModuleScan:
    def __init__(self, tree: ast.Module, fname: str, report: Report, siblings: Optional[dict] = None):
        self.tree, self.fname, self.report = tree, fname, report
        self.classes: dict[str, type] = {}     # local name -> pyegeria class
        self.lib_modules: dict[str, object] = {}  # local alias -> pyegeria module
        self.factories: dict[str, frozenset] = {}
        self.param_types: dict[str, dict[str, frozenset]] = {}   # function -> {param: classes}
        self.siblings = siblings if siblings is not None else {}  # module stem -> _ModuleScan
        self._collect_imports()
        self._collect_factories()

    def _sibling_factories(self) -> dict:
        """Factories imported from another scanned module: ``from digital_products_handler import _get_manager``."""
        out = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom) and node.module in self.siblings and node.level == 0:
                sib = self.siblings[node.module]
                for a in node.names:
                    if a.name in sib.factories:
                        out[a.asname or a.name] = sib.factories[a.name]
        return out

    # ---- imports
    def _fallback_imports(self) -> set:
        """ImportFrom nodes in an ``except`` branch whose ``try`` already imports from the library
        successfully: version shims (``try: from pyegeria.view.x import A / except: from pyegeria.x import A``)
        whose old path is expected to be gone."""
        out = set()
        for t in ast.walk(self.tree):
            if not isinstance(t, ast.Try):
                continue
            ok = any(isinstance(n, ast.ImportFrom) and n.module and n.module.split(".")[0] in LIB_ROOTS
                     and all(_resolve_import(n.module, a.name) is not _UNTYPED for a in n.names if a.name != "*")
                     for s in t.body for n in ast.walk(s))
            if ok:
                for h in t.handlers:
                    out.update(id(n) for s in h.body for n in ast.walk(s) if isinstance(n, ast.ImportFrom))
        return out

    def _collect_imports(self):
        fallbacks = self._fallback_imports()
        for node in ast.walk(self.tree):
            if id(node) in fallbacks:
                continue
            if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in LIB_ROOTS \
                    and node.level == 0:
                for a in node.names:
                    if a.name == "*":
                        mod = _resolve_import(node.module.rsplit(".", 1)[0], node.module.rsplit(".", 1)[-1]) \
                            if "." in node.module else importlib.import_module(node.module)
                        for n, o in vars(mod).items() if mod is not _UNTYPED else ():
                            if _is_lib_class(o):
                                self.classes[n] = o
                        continue
                    obj = _resolve_import(node.module, a.name)
                    if obj is _UNTYPED:
                        self.report.findings.append(Finding("import", self.fname, node.lineno, node.module,
                                                            a.name, "no such name in the installed library"))
                    elif _is_lib_class(obj):
                        self.classes[a.asname or a.name] = obj
            elif isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.split(".")[0] in LIB_ROOTS:
                        try:
                            self.lib_modules[a.asname or a.name.split(".")[0]] = importlib.import_module(
                                a.name if a.asname else a.name.split(".")[0])
                        except Exception:  # noqa: BLE001
                            self.report.findings.append(Finding("import", self.fname, node.lineno, "import",
                                                                a.name, "module not importable"))

    # ---- typing an expression
    def _ctor_class(self, func: ast.AST):
        if isinstance(func, ast.Name) and func.id in self.classes:
            return frozenset({self.classes[func.id]})
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) \
                and func.value.id in self.lib_modules:
            obj = getattr(self.lib_modules[func.value.id], func.attr, None)
            if obj is None:
                self.report.findings.append(Finding("missing", self.fname, func.lineno, func.value.id,
                                                    func.attr, "no such name in the pyegeria module"))
            elif _is_lib_class(obj):
                return frozenset({obj})
        if isinstance(func, ast.Name) and func.id in self.factories:
            return self.factories[func.id]
        return None

    def _expr_type(self, expr, env):
        if isinstance(expr, ast.Await):
            expr = expr.value
        if isinstance(expr, ast.Call):
            return self._ctor_class(expr.func)
        if isinstance(expr, ast.Name):
            t = env.get(expr.id)
            return t if t is not _UNTYPED else None
        return None

    def _ann_type(self, ann):
        if ann is None:
            return None
        if isinstance(ann, ast.Constant) and isinstance(ann.value, str):
            try:
                ann = ast.parse(ann.value, mode="eval").body
            except SyntaxError:
                return None
        if isinstance(ann, ast.Subscript) and ast.unparse(ann.value) in ("Optional", "typing.Optional"):
            ann = ann.slice
        if isinstance(ann, ast.BinOp):   # X | None
            for side in (ann.left, ann.right):
                t = self._ann_type(side)
                if t:
                    return t
            return None
        if isinstance(ann, ast.Name) and ann.id in self.classes:
            return frozenset({self.classes[ann.id]})
        if isinstance(ann, ast.Attribute) and isinstance(ann.value, ast.Name) and ann.value.id in self.lib_modules:
            obj = getattr(self.lib_modules[ann.value.id], ann.attr, None)
            return frozenset({obj}) if _is_lib_class(obj) else None
        return None

    # ---- scopes
    @staticmethod
    def _own_nodes(body):
        """Nodes of a scope, not descending into nested function / class / lambda bodies."""
        stack = list(body)
        while stack:
            n = stack.pop()
            yield n
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue   # its own scope; decorators and defaults are rare enough to ignore
            stack.extend(ast.iter_child_nodes(n))

    def _scope_env(self, fn, parent_env):
        env = dict(parent_env)
        local = {}
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            inferred = self.param_types.get(fn.name, {})
            for a in fn.args.args + fn.args.kwonlyargs + fn.args.posonlyargs:
                t = self._ann_type(a.annotation) or inferred.get(a.arg)
                local[a.arg] = t if t else _UNTYPED
            body = fn.body
        else:
            body = fn.body
        # two passes so `x = factory(); y = x` resolves regardless of walk order
        for _ in range(2):
            seen = {}
            for n in self._own_nodes(body):
                targets, value = [], None
                if isinstance(n, ast.Assign):
                    targets, value = n.targets, n.value
                elif isinstance(n, ast.AnnAssign) and n.value is not None:
                    targets, value = [n.target], n.value
                    t = self._ann_type(n.annotation)
                    if t and isinstance(n.target, ast.Name):
                        seen.setdefault(n.target.id, set()).add(t)
                        continue
                elif isinstance(n, (ast.With, ast.AsyncWith)):
                    for item in n.items:
                        if isinstance(item.optional_vars, ast.Name):
                            t = self._expr_type(item.context_expr, {**env, **local})
                            seen.setdefault(item.optional_vars.id, set()).add(t or _UNTYPED)
                    continue
                elif isinstance(n, (ast.For, ast.AsyncFor, ast.comprehension)) and isinstance(n.target, ast.Name):
                    seen.setdefault(n.target.id, set()).add(_UNTYPED)
                    continue
                elif isinstance(n, ast.NamedExpr):
                    targets, value = [n.target], n.value
                for tgt in targets:
                    if isinstance(tgt, ast.Name):
                        t = self._expr_type(value, {**env, **local})
                        seen.setdefault(tgt.id, set()).add(t or _UNTYPED)
                    else:
                        for nm in ast.walk(tgt):
                            if isinstance(nm, ast.Name):
                                seen.setdefault(nm.id, set()).add(_UNTYPED)
            for name, ts in seen.items():
                if name in local and local[name] is not _UNTYPED and isinstance(local[name], frozenset):
                    ts = ts | {local[name]}
                if _UNTYPED in ts or len(ts) != 1:
                    # several client classes for one name: accept a method on any of them
                    if _UNTYPED not in ts and ts:
                        local[name] = frozenset().union(*ts)
                    else:
                        local[name] = _UNTYPED
                else:
                    local[name] = next(iter(ts))
        env.update(local)
        return env

    def _functions(self):
        return [n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    def _all_scopes(self):
        """[(scope node, env)] for the module and every function, nested functions inheriting their
        enclosing function's env."""
        module_env = self._scope_env(self.tree, {})
        scopes = [(self.tree, module_env)]

        def visit(owner, env):
            for n in self._own_nodes(owner.body):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    fenv = self._scope_env(n, env)
                    scopes.append((n, fenv))
                    visit(n, fenv)
                elif isinstance(n, ast.ClassDef):
                    visit(n, env)
        visit(self.tree, module_env)
        return scopes

    def _infer_params(self, scopes) -> bool:
        """A parameter of a same-module function is typed when EVERY call site passes it a typed client."""
        fns = {}
        for fn in self._functions():
            fns.setdefault(fn.name, []).append(fn)
        seen: dict[tuple, set] = {}
        for owner, env in scopes:
            for n in self._own_nodes(owner.body):
                if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in fns):
                    continue
                if len(fns[n.func.id]) != 1:
                    continue   # two functions of one name: cannot tell which is called
                fn = fns[n.func.id][0]
                params = [a.arg for a in fn.args.posonlyargs + fn.args.args]
                pairs = list(zip(params, n.args)) + [(k.arg, k.value) for k in n.keywords if k.arg]
                for pname, val in pairs:
                    if isinstance(val, ast.Starred):
                        continue
                    seen.setdefault((fn.name, pname), set()).add(self._expr_type(val, env) or _UNTYPED)
        changed = False
        for (fname, pname), ts in seen.items():
            if _UNTYPED in ts or not ts:
                continue
            t = frozenset().union(*ts)
            if self.param_types.setdefault(fname, {}).get(pname) != t:
                self.param_types[fname][pname] = t
                changed = True
        return changed

    def _collect_factories(self):
        self.factories.update(self._sibling_factories())
        # fixed point: a factory may return another factory's result, a helper may get a client passed in
        for _ in range(6):
            scopes = self._all_scopes()
            changed = self._infer_params(scopes)
            module_env = scopes[0][1]
            for fn in self._functions():
                t = self._ann_type(fn.returns)
                if not t:
                    env = self._scope_env(fn, module_env)   # enclosing-function closures: rare in factories
                    rets = [self._expr_type(r.value, env) for r in self._own_nodes(fn.body)
                            if isinstance(r, ast.Return) and r.value is not None
                            and not (isinstance(r.value, ast.Constant) and r.value.value is None)]
                    if rets and all(rets):
                        t = frozenset().union(*rets)
                if t and self.factories.get(fn.name) != t:
                    self.factories[fn.name] = t
                    changed = True
            if not changed:
                break

    # ---- checks
    def _check_attr(self, node: ast.Attribute, env, called: bool):
        recv = node.value
        if isinstance(recv, ast.Name) and recv.id in self.classes and recv.id not in env \
                and (called or VERB.match(node.attr)):
            # the class itself, e.g. help(EgeriaTech.get_asset_graph): no instance, so no __getattr__
            # delegation -- only what the class really defines counts
            cls = self.classes[recv.id]
            self.report.typed_calls += 1
            if node.attr not in dir(cls):
                self.report.findings.append(Finding("missing", self.fname, node.lineno, recv.id, node.attr,
                                                    f"not defined on the class {cls.__name__} itself"))
            return
        if isinstance(recv, ast.Name):
            t, label = env.get(recv.id), recv.id
        elif isinstance(recv, (ast.Call, ast.Await)):
            t, label = self._expr_type(recv, env), ast.unparse(recv)[:40]   # ExternalReferences(...).get_x()
        else:
            return
        name = node.attr
        if isinstance(t, frozenset) and t:
            if not called and not VERB.match(name):
                return   # an instance attribute like mgr.server_name, set in __init__
            self.report.typed_calls += 1
            if not any(name in class_methods(c) for c in t):
                self.report.findings.append(Finding(
                    "missing", self.fname, node.lineno, label, name,
                    "not on " + "/".join(sorted(c.__name__ for c in t))))
            self._check_deprecated(node, label, name)
        elif called and isinstance(recv, ast.Name) and recv.id in CLIENTISH and VERB.match(name):
            self.report.loose_calls += 1
            if name not in all_lib_names():
                self.report.findings.append(Finding("missing-loose", self.fname, node.lineno, label, name,
                                                    "on no pyegeria class"))
            self._check_deprecated(node, label, name)

    def _check_deprecated(self, node, recv, name):
        dep = deprecated_methods()
        base = name[len("_async_"):] if name.startswith("_async_") else name
        if base in dep:
            self.report.findings.append(Finding("deprecated", self.fname, node.lineno, recv, name,
                                                f"{dep[base]}.{base} warns DeprecationWarning"))

    def run(self):
        scopes = self._all_scopes()
        dkw = deprecated_kwargs()
        for owner, env in scopes:
            called_attrs = set()
            for n in self._own_nodes(owner.body):
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Attribute):
                        called_attrs.add(id(n.func))
                        self._check_attr(n.func, env, called=True)
                    if isinstance(n.func, ast.Name) and n.func.id == "getattr" and len(n.args) >= 2 \
                            and isinstance(n.args[0], ast.Name) and isinstance(n.args[1], ast.Constant) \
                            and isinstance(n.args[1].value, str) and len(n.args) == 2:
                        fake = ast.Attribute(value=n.args[0], attr=n.args[1].value, lineno=n.lineno)
                        self._check_attr(fake, env, called=True)
                    for kw in n.keywords:
                        if kw.arg in dkw and self._is_lib_call(n, env):
                            self.report.findings.append(Finding(
                                "deprecated-kwarg", self.fname, n.lineno, ast.unparse(n.func)[:40], kw.arg,
                                f"use {dkw[kw.arg]}="))
            for n in self._own_nodes(owner.body):
                if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load) and id(n) not in called_attrs:
                    self._check_attr(n, env, called=False)

    def _is_lib_call(self, call, env):
        f = call.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            t = env.get(f.value.id)
            return isinstance(t, frozenset) or (f.value.id in CLIENTISH and bool(VERB.match(f.attr)))
        return False


def scan_source(src: str, fname: str, report: Optional[Report] = None) -> Report:
    report = report or Report()
    tree = ast.parse(src)
    _ModuleScan(tree, fname, report).run()
    report.files += 1
    return report


def _run_target_imports(path: Path, line: str) -> list[str]:
    """``%run initialize-pyegeria.ipynb`` defines names (EgeriaTech, ...) for the notebook that runs it:
    bring in that notebook's top-level import statements so the scan knows them too."""
    target = (path.parent / line.split(None, 1)[1].strip().strip("'\"")).resolve()
    if target.suffix != ".ipynb" or not target.is_file():
        return []
    out = []
    for cell in json.loads(target.read_text()).get("cells", []):
        if cell.get("cell_type") == "code":
            src = cell.get("source", "")
            src = "".join(src) if isinstance(src, list) else src
            out += [l for l in src.splitlines() if l.startswith(("import ", "from "))]
    return out


def notebook_source(path: Path) -> tuple[str, list[int]]:
    """Code cells joined into one module (IPython magics and shell lines blanked); [cell index per line]."""
    nb = json.loads(path.read_text())
    lines, cell_of = [], []
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        src = "".join(src) if isinstance(src, list) else src
        for ln in src.splitlines():
            s = ln.lstrip()
            if s.startswith("%run ") and ln == s:
                for imp in _run_target_imports(path, s):
                    lines.append(imp)
                    cell_of.append(i)
                continue
            if s.startswith(("%", "!", "?")) or s.endswith("?"):
                ln = ""
            lines.append(ln)
            cell_of.append(i)
        lines.append("")
        cell_of.append(i)
    return "\n".join(lines), cell_of


def _siblings_for(paths) -> dict:
    """Pre-scan the .py modules so one module's factories are known where another imports them.
    Two rounds, so a factory built on an imported factory resolves too."""
    sib: dict = {}
    pys = [Path(p) for p in paths if Path(p).suffix == ".py"]
    for _ in range(2):
        nxt = {}
        for p in pys:
            try:
                nxt[p.stem] = _ModuleScan(ast.parse(p.read_text()), str(p), Report(), siblings=sib)
            except SyntaxError:
                continue
        sib = nxt
    return sib


def scan_paths(paths: Iterable[Path], siblings: Optional[dict] = None) -> Report:
    paths = [Path(p) for p in paths]
    if siblings is None:
        siblings = _siblings_for(paths)
    report = Report()
    for p in paths:
        if p.suffix == ".ipynb":
            src, cell_of = notebook_source(p)
            try:
                tree_ok = ast.parse(src)
            except SyntaxError as exc:
                # one bad cell must not hide the rest: scan cell by cell instead
                nb = json.loads(p.read_text())
                for i, cell in enumerate(nb.get("cells", [])):
                    if cell.get("cell_type") != "code":
                        continue
                    s = cell.get("source", "")
                    s = "".join(s) if isinstance(s, list) else s
                    s = "\n".join("" if l.lstrip().startswith(("%", "!")) else l for l in s.splitlines())
                    try:
                        scan_source(s, f"{p}[cell {i}]", report)
                    except SyntaxError:
                        continue
                continue
            sub = Report()
            _ModuleScan(tree_ok, str(p), sub).run()
            for f in sub.findings:
                idx = cell_of[f.line - 1] if 0 < f.line <= len(cell_of) else "?"
                f.file = f"{p}[cell {idx}]"
            report.findings += sub.findings
            report.typed_calls += sub.typed_calls
            report.loose_calls += sub.loose_calls
            report.files += 1
        else:
            _ModuleScan(ast.parse(p.read_text()), str(p), report, siblings=siblings).run()
            report.files += 1
    return report


if __name__ == "__main__":
    r = scan_paths(Path(a) for a in sys.argv[1:])
    for f in r.findings:
        print(f)
    print(f"# files={r.files} typed_calls={r.typed_calls} loose_calls={r.loose_calls} findings={len(r.findings)}",
          file=sys.stderr)
