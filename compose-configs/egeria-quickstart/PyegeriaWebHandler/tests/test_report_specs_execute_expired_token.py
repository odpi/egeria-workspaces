"""/api/report-specs/execute with an expired token: 401 with the Portal's words, no Egeria call."""
import base64, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import report_specs_handler  # noqa: E402


def _jwt(exp_in):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': 'peter', 'exp': int(time.time()) + exp_in})}.sig"


def test_expired_token_is_401_before_any_egeria_call(monkeypatch):
    from pyegeria.view.analytic_demo_specs import register_analytic_demo_specs
    try:
        register_analytic_demo_specs()
    except Exception:
        pass  # already registered in this process
    built = []
    import pyegeria.view.format_set_executor as fse
    monkeypatch.setattr(fse, "_plain_client", lambda *a, **k: built.append(a) or None)
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(report_specs_handler.router)
    r = TestClient(app).post("/api/report-specs/execute", headers={"X-Egeria-Token": _jwt(-60)},
                             json={"spec_name": "Analytic Demo - Element Count by Type", "output_format": "DICT"})
    assert r.status_code == 401, r.text
    assert r.json()["detail"] == egeria_auth.TOKEN_REFUSED_WORDS
    assert built == []
