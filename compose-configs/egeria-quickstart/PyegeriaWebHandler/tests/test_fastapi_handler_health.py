from fastapi.testclient import TestClient
import sys
from pathlib import Path as _P

# Add PyegeriaWebHandler directory to sys.path so we can import modules directly
_THIS_DIR = _P(__file__).resolve().parent
_MODULE_DIR = _THIS_DIR.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

# Now we can import the module by simple name
import pyegeria_handler as handler  # type: ignore


def test_health_endpoint_ok():
    client = TestClient(handler.app)
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert body.get("service") == "dr-egeria-md"
