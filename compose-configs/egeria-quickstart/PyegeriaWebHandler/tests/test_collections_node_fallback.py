"""GET /api/collections/{guid} for a non-collection member (an asset, a StatementOfApplicability, ...)
falls back to digital_products_handler.get_node. That call passed user_pwd positionally into a route
function that has no user_pwd, so it landed in as_of_time and raised
"get_node() got multiple values for argument 'as_of_time'" -> HTTP 500 (PO-24). Pinned two ways:
statically, so that each tree's call (quickstart AND freshstart) binds to its own get_node signature;
and behaviourally (quickstart), so that the fallback really runs and forwards the arguments it was given."""
import ast
import inspect
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent.parent
_TREES = [_HERE, _HERE.parent.parent / "egeria-freshstart" / "PyegeriaWebHandler"]


def _get_node_signature(tree_dir):
    mod = ast.parse((tree_dir / "digital_products_handler.py").read_text())
    fn = next(n for n in mod.body if isinstance(n, ast.FunctionDef) and n.name == "get_node")
    a = fn.args
    params = [inspect.Parameter(x.arg, inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                default=(inspect.Parameter.empty if i < len(a.args) - len(a.defaults) else None))
              for i, x in enumerate(a.args)]
    params += [inspect.Parameter(x.arg, inspect.Parameter.KEYWORD_ONLY, default=None) for x in a.kwonlyargs]
    return inspect.Signature(params)


def _dp_get_node_calls(tree_dir):
    mod = ast.parse((tree_dir / "collections_handler.py").read_text())
    return [n for n in ast.walk(mod)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "dp_get_node"]


@pytest.mark.parametrize("tree_dir", [t for t in _TREES if (t / "collections_handler.py").exists()],
                         ids=lambda p: p.parent.name)
def test_fallback_call_binds_to_get_node_signature(tree_dir):
    sig = _get_node_signature(tree_dir)
    calls = _dp_get_node_calls(tree_dir)
    assert calls, "collections_handler no longer calls dp_get_node"
    for call in calls:
        args = [object()] * len(call.args)
        kwargs = {k.arg: object() for k in call.keywords}
        sig.bind(*args, **kwargs)          # raises TypeError on the PO-24 shape
        assert "user_pwd" not in kwargs, "get_node takes no user_pwd (credentials never come from the URL)"


def test_non_collection_guid_falls_back_with_its_arguments(monkeypatch):
    sys.path.insert(0, str(_HERE))
    fastapi = pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    import collections_handler as ch
    import digital_products_handler as dp

    class _NoCollection:
        def get_collection_by_guid(self, *a, **k):
            return None

    seen = {}
    real_sig = inspect.signature(dp.get_node)

    def fake_get_node(*a, **k):
        bound = real_sig.bind(*a, **k)     # same TypeError the real function raised
        seen.update(bound.arguments)
        return {"guid": bound.arguments["node_guid"], "fallback": True}

    monkeypatch.setattr(ch, "_get_manager", lambda *a, **k: _NoCollection())
    monkeypatch.setattr(dp, "get_node", fake_get_node)
    app = fastapi.FastAPI(); app.include_router(ch.router)
    r = TestClient(app).get("/api/collections/soa-guid-1",
                            params={"server": "qs-view-server", "as_of_time": "2026-11-16T00:00:00Z"})
    assert r.status_code == 200, r.text
    assert r.json() == {"guid": "soa-guid-1", "fallback": True}
    assert seen["server"] == "qs-view-server"
    assert seen["as_of_time"] == "2026-11-16T00:00:00Z"
    assert "user_pwd" not in seen
