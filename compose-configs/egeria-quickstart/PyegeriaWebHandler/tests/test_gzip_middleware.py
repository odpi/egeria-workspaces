"""App-wide gzip (pyegeria_handler): large JSON is compressed, small bodies and event streams are not.
Uses the same Starlette middleware and settings the app installs; no Egeria needed."""
import gzip, json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.testclient import TestClient
from starlette.middleware.gzip import GZipMiddleware


def _app():
    app = FastAPI(); app.add_middleware(GZipMiddleware, minimum_size=1024)
    big = [{"guid": str(i), "typeName": "Folder", "displayName": "name %d" % i} for i in range(500)]
    app.get("/big")(lambda: JSONResponse(big))
    app.get("/small")(lambda: JSONResponse({"ok": True}))
    app.get("/sse")(lambda: StreamingResponse(iter([b"data: " + b"x" * 5000 + b"\n\n"]), media_type="text/event-stream"))
    return app, big


def test_big_json_is_gzipped_and_round_trips():
    app, big = _app(); c = TestClient(app)
    r = c.get("/big", headers={"Accept-Encoding": "gzip"})
    assert r.headers["content-encoding"] == "gzip" and r.json() == big
    assert int(r.headers["content-length"]) < len(json.dumps(big)) / 3


def test_no_gzip_unless_asked_small_or_event_stream():
    app, _ = _app(); c = TestClient(app)
    assert "content-encoding" not in c.get("/big", headers={"Accept-Encoding": "identity"}).headers
    assert "content-encoding" not in c.get("/small", headers={"Accept-Encoding": "gzip"}).headers
    assert "content-encoding" not in c.get("/sse", headers={"Accept-Encoding": "gzip"}).headers


def test_the_app_installs_it_with_an_off_switch():
    import pathlib
    src = (pathlib.Path(__file__).resolve().parent.parent / "pyegeria_handler.py").read_text()
    assert "GZipMiddleware, minimum_size=1024" in src and "PORTAL_GZIP" in src
