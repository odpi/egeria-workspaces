"""Every pyegeria method the Portal's handlers call on a client exists in the installed pyegeria.

pyegeria renamed get_external_identifier_by_guid to get_external_identifiers_by_guid in 6.1.0 and kept no alias;
the Portal's External Identifiers detail pane failed for everyone until a user reported it. A rename like that
should fail here, not on the live page. An AST scan, so no Egeria is needed.

Covers every module in PyegeriaWebHandler (handlers and helpers), via tests/pyegeria_calls.py."""
import ast
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
# Names the handlers give a pyegeria client (mgr = _get_manager(...), expert = ..., classifier = ...).
RECEIVERS = {"mgr", "expert", "classifier", "manager", "mgr2"}   # not "client": that is httpx or docker in places


def _called_methods(path: Path):
    """[(receiver, method, line)] for every `<receiver>.method(...)` call on a client-looking variable."""
    tree = ast.parse(path.read_text())
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id in RECEIVERS):
            out.append((node.func.value.id, node.func.attr, node.lineno))
    return out


def test_external_links_handler_calls_exist_on_ExternalReferences():
    from pyegeria import ExternalReferences
    calls = _called_methods(HERE / "external_links_handler.py")
    assert calls, "scan found no client calls: the test would pass vacuously"
    missing = sorted({(m, line) for r, m, line in calls if not hasattr(ExternalReferences, m)})
    assert not missing, f"ExternalReferences has no such method(s): {missing}"


def test_the_renamed_identifier_method_is_the_one_called():
    src = (HERE / "external_links_handler.py").read_text()
    assert "get_external_identifiers_by_guid(" in src and "get_external_identifier_by_guid(" not in src


def test_the_identifier_list_is_read_at_depth_0():
    assert "graph_query_depth=0" in (HERE / "external_links_handler.py").read_text().split("def list_external_identifiers")[1].split("def get_external_identifier")[0]


# --------------------------------------------------------------------------- every module, typed receivers
# tests/pyegeria_calls.py works out which variables hold a pyegeria client (constructor, same-module
# factory, `with ... as`, annotation) and checks each call against that class; client-looking names it
# cannot type are checked against every pyegeria class. See its docstring for the rules.
import pyegeria_calls  # noqa: E402

MODULES = sorted(p.name for p in HERE.glob("*.py") if not p.name.startswith("test_"))


@pytest.fixture(scope="module")
def scan():
    siblings = pyegeria_calls._siblings_for([HERE / m for m in MODULES])   # cross-module factories
    return {m: pyegeria_calls.scan_paths([HERE / m], siblings=siblings) for m in MODULES}


@pytest.mark.parametrize("module", MODULES)
def test_every_pyegeria_call_and_import_exists(module, scan):
    """A method or import the installed pyegeria does not have is a rename or a removal: it fails here."""
    bad = [str(f) for f in scan[module].findings if f.kind in ("missing", "missing-loose", "import")]
    assert not bad, f"{module}: calls/imports the installed pyegeria does not have:\n" + "\n".join(bad)


@pytest.mark.parametrize("module", MODULES)
def test_no_call_uses_a_deprecated_pyegeria_method_or_keyword(module, scan):
    """Deprecated-but-working: a method that now issues a DeprecationWarning, or a deprecated keyword."""
    bad = [str(f) for f in scan[module].findings if f.kind in ("deprecated", "deprecated-kwarg")]
    assert not bad, f"{module}: deprecated pyegeria usage:\n" + "\n".join(bad)


def test_the_scan_is_not_vacuous(scan):
    """The scan must actually type the handlers' clients: a regression in the inference would otherwise
    pass every module above while checking nothing."""
    typed = sum(r.typed_calls for r in scan.values())
    assert typed >= 250, f"only {typed} calls were checked against a known pyegeria class"
    # every ExternalReferences call there (the old receiver-name scan found the same 4) is typed
    assert scan["external_links_handler.py"].typed_calls == len(_called_methods(HERE / "external_links_handler.py"))


@pytest.mark.parametrize("snippet, kind", [
    ("from pyegeria import ExternalReferences\n"
     "def f():\n    mgr = ExternalReferences('v', 'u', 'x', 'p')\n    mgr.get_external_identifier_by_guid('g')\n",
     "missing"),
    ("from pyegeria import ExternalReferences\n"
     "def _mk():\n    return ExternalReferences('v', 'u', 'x', 'p')\n"
     "async def f():\n    m = _mk()\n    await m._async_get_external_identifier_by_guid('g')\n",
     "missing"),
    ("from pyegeria import EgeriaTech\n"
     "def f():\n    t = EgeriaTech('v', 'u', 'x', 'p')\n    t.no_such_method_anywhere()\n", "missing"),
    ("def f(mgr):\n    mgr.get_external_identifier_by_guid('g')\n", "missing-loose"),
    ("from pyegeria import NoSuchClient\n", "import"),
    ("from pyegeria import ExternalReferences\n"
     "def _mk():\n    return ExternalReferences('v', 'u', 'x', 'p')\n"
     "def _read(m, g):\n    return m.get_external_identifier_by_guid(g)\n"
     "def f():\n    return _read(_mk(), 'g')\n", "missing"),
])
def test_the_scan_catches_a_reintroduced_bad_name(snippet, kind):
    findings = pyegeria_calls.scan_source(snippet, "<snippet>").findings
    assert [f.kind for f in findings] == [kind], [str(f) for f in findings]


def test_the_scan_accepts_delegated_and_real_names():
    snippet = ("from pyegeria import EgeriaTech, ExternalReferences\n"
               "def f():\n    t = EgeriaTech('v', 'u', 'x', 'p')\n    t.get_external_identifiers_by_guid('g')\n"
               "    m = ExternalReferences('v', 'u', 'x', 'p')\n    m.server_name\n"
               "    client = make_httpx()\n    client.get('/x')\n")
    assert pyegeria_calls.scan_source(snippet, "<snippet>").findings == []
