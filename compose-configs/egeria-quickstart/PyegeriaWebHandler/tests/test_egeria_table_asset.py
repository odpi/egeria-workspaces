"""/static/egeria-table.js is served from pyegeria's package data, with the Portal's copy as fallback (PO-5).

Each case asserts on what a reader of the response sees: the body served and the X-Egeria-Table-Source
header that names where it came from."""
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import egeria_table_asset as eta  # noqa: E402


def _client():
    app = FastAPI()
    app.include_router(eta.router)
    return TestClient(app)


def test_serves_pyegerias_copy_when_the_package_has_one(tmp_path, monkeypatch):
    pkg = tmp_path / "egeria-table.js"
    pkg.write_text("/* from pyegeria */")
    monkeypatch.setattr(eta, "pyegeria_table_js", lambda: (pkg, "9.9.9"))
    r = _client().get("/static/egeria-table.js")
    assert r.status_code == 200
    assert r.text == "/* from pyegeria */"
    assert r.headers[eta.SOURCE_HEADER] == "pyegeria 9.9.9 package data"
    assert r.headers["cache-control"] == "no-cache"
    assert r.headers["content-type"].startswith("text/javascript")


def test_falls_back_to_the_portal_copy_and_says_why(tmp_path, monkeypatch):
    vendored = tmp_path / "egeria-table.js"
    vendored.write_text("/* the Portal's copy */")
    monkeypatch.setattr(eta, "pyegeria_table_js", lambda: (None, "6.2.41"))
    monkeypatch.setattr(eta, "VENDORED", vendored)
    r = _client().get("/static/egeria-table.js")
    assert r.status_code == 200
    assert r.text == "/* the Portal's copy */"
    assert r.headers[eta.SOURCE_HEADER] == "portal fallback (static/egeria-table.js; pyegeria 6.2.41 has no egeria-table.js)"


def test_no_copy_anywhere_is_a_404_that_says_so(tmp_path, monkeypatch):
    monkeypatch.setattr(eta, "pyegeria_table_js", lambda: (None, None))
    monkeypatch.setattr(eta, "VENDORED", tmp_path / "missing.js")
    r = _client().get("/static/egeria-table.js")
    assert r.status_code == 404
    assert "ships none" in r.json()["detail"]


def test_the_installed_pyegeria_is_found_when_it_ships_the_file():
    path, version = eta.pyegeria_table_js()
    if version is None:
        pytest.skip("pyegeria not importable")
    from packaging.version import Version
    if Version(version) < Version("6.2.42"):
        pytest.skip(f"pyegeria {version} predates the package-data copy")
    assert path is not None and path.name == "egeria-table.js" and "pyegeria" in path.parts


def test_route_is_registered_before_the_static_mount():
    src = (ROOT / "pyegeria_handler.py").read_text()
    inc = src.index("app.include_router(egeria_table_router)")
    mount = src.index('app.mount("/static"')
    assert inc < mount
