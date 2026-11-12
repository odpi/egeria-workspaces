"""The read-only "Last Egeria reset" panel: GET /api/admin/egeria-resets and static/egeria-resets-panel.js.

Offline: the database read is a fake. The JS part runs under node (skipped without node).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

ROW = {"id": 2, "started_at": "2026-11-12T10:00:00+00:00", "finished_at": "2026-11-12T11:30:00+00:00",
       "outcome": "completed", "operator": "dwolfson", "host": "laz", "database": "egeria",
       "old_digest": "sha256:" + "1" * 64, "new_digest": "sha256:" + "2" * 64,
       "old_image_id": "sha256:old", "new_image_id": "sha256:new",
       "backup_path": "/x/egeria-20261112T100000Z.sql.gz", "backup_bytes": 52_428_800, "backup_sha256": "c" * 64,
       "heal": json.dumps({"families": {"batch:Security": {}}, "missing": [], "logErrorCount": 0}),
       "verify": json.dumps({"checks": [{"check": "a", "verdict": "PASS"}, {"check": "b", "verdict": "NOT MEASURED"}],
                             "failed": []}),
       "steps": "{}", "state_dir": "/x"}


def _payload(reader):
    import egeria_resets_handler as h
    return h.resets_payload(20, reader=reader)


def test_rows_newest_first():
    p = _payload(lambda n: [ROW, {**ROW, "id": 1, "outcome": "failed"}])
    assert p["state"] == "read" and p["latest"]["id"] == 2 and len(p["rows"]) == 2


def test_no_rows_says_so():
    p = _payload(lambda n: [])
    assert p == {"state": "none", "message": "No reset recorded by egeria-upgrade-reset.", "rows": []}


def test_no_table_yet_is_none_not_an_error():
    def reader(n):
        raise RuntimeError('(psycopg2.errors.UndefinedTable) relation "demo.egeria_resets" does not exist')
    p = _payload(reader)
    assert p["state"] == "none" and "does not exist yet" in p["message"]


def test_unreadable_is_not_read_with_the_reason():
    def reader(n):
        raise ConnectionError("could not connect to server: Connection refused")
    p = _payload(reader)
    assert p["state"] == "not read" and "Connection refused" in p["reason"] and p["rows"] is None


def test_route_is_admin_only_and_read_only(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import egeria_resets_handler as h
    import report_specs_handler as rs
    app = FastAPI()
    app.include_router(h.router)
    monkeypatch.setattr(rs, "_is_admin_closed", lambda request: False)
    assert TestClient(app).get("/api/admin/egeria-resets").status_code == 403
    monkeypatch.setattr(rs, "_is_admin_closed", lambda request: True)
    monkeypatch.setattr(h, "_read", lambda n: [ROW])
    r = TestClient(app).get("/api/admin/egeria-resets")
    assert r.status_code == 200 and r.json()["latest"]["host"] == "laz"
    assert {m for route in h.router.routes for m in route.methods} == {"GET"}     # no action


def test_pages_load_the_panel():
    for page in ("local-admin.html", "demo-admin.html"):
        html = (ROOT / page).read_text()
        assert "/static/egeria-resets-panel.js" in html and 'id="egeriaResets"' in html
        assert "EgeriaResetsPanel.load('egeriaResets')" in html
        assert "a reset cannot be started from the Portal" in html


def _render(data):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var P = require(" + json.dumps(str(ROOT / "static" / "egeria-resets-panel.js")) + ");"
          "var el = {innerHTML: ''}; P.render(el, " + json.dumps(data) + "); console.log(JSON.stringify(el.innerHTML));")
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_js_empty_state_is_a_sentence():
    html = _render({"state": "none", "rows": [], "message": "No reset recorded by egeria-upgrade-reset."})
    assert "No reset recorded by egeria-upgrade-reset." in html


def test_js_not_read_names_the_reason():
    assert "Reset history not read: Connection refused" in _render({"state": "not read", "reason": "Connection refused"})


def test_js_latest_row_and_history():
    html = _render({"state": "read", "rows": [ROW, {**ROW, "id": 1, "outcome": "failed", "started_at": "2026-11-11T21:00:00+00:00"}]})
    assert "2026-11-12T10:00:00+00:00" in html and "completed" in html
    assert "111111111111" in html and "222222222222" in html          # short digests
    assert "50.0 MB" in html and "1 pass, 0 fail, 1 not measured" in html and "all present" in html
    assert "Earlier resets (1)" in html and "failed" in html


def test_js_escapes():
    html = _render({"state": "read", "rows": [{**ROW, "operator": "<script>x</script>"}]})
    assert "<script>" not in html and "&lt;script&gt;" in html
