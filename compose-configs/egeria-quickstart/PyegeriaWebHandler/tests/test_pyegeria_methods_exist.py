"""Every pyegeria method the Portal's handlers call on a client exists in the installed pyegeria.

pyegeria renamed get_external_identifier_by_guid to get_external_identifiers_by_guid in 6.1.0 and kept no alias;
the Portal's External Identifiers detail pane failed for everyone until a user reported it. A rename like that
should fail here, not on the live page. An AST scan, so no Egeria is needed."""
import ast
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


def _all_client_methods():
    import pyegeria
    names = set()
    for obj in vars(pyegeria).values():
        if inspect.isclass(obj):
            names.update(n for n in dir(obj) if not n.startswith("__"))
    return names


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


@pytest.mark.parametrize("handler", sorted(p.name for p in HERE.glob("*_handler.py")))
def test_every_handler_method_call_exists_on_some_pyegeria_client(handler):
    """Looser, for every handler: a name found on NO pyegeria client class is a rename or a typo."""
    known = _all_client_methods()
    missing = sorted({(m, line) for r, m, line in _called_methods(HERE / handler) if m not in known})
    assert not missing, f"{handler}: no pyegeria client has method(s) {missing}"
