"""GET /api/report-specs/sync names no spec and no zone to a caller who is not an administrator (F1).

The sync reads Egeria as the Portal's service account, so its skip list can name a zoned spec, and
its zones, that the viewer cannot read (read-back 2026-11-15: peter saw an erin-only spec's name and
zones). A non-admin gets the counts and the skip categories; an administrator keeps the full detail.
Through the real route, EgeriaTokenMiddleware and the real admin check (a signed demo JWT).
"""
import base64
import json
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import report_spec_sync as rss  # noqa: E402

HIDDEN = "ZZ-RB-20261115 erin restricted"
ZONE = "erinoverview"
FOLDER = "ReportSpecFolder::Consumer::Portal"
REPORT = {
    "added": [], "updated": [], "unchanged": ["Shared One", "Shared Two"], "pruned": [],
    "skipped": [[HIDDEN, f"zoned: not synced into a shared cache (until B6's public-only read); zones {ZONE}"],
                ["ZZ other zoned", "zoned: not synced into a shared cache; zones financeteam"],
                ["Draft Thing", "contentStatus DRAFT is not synced"]],
}


def _unsigned(sub):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + 3600})}.sig"


@pytest.fixture
def get(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from jose import jwt
    import demo_feedback_handler as dfh
    import report_specs_handler as rsh
    from egeria_auth import EgeriaTokenMiddleware

    monkeypatch.setattr(dfh, "DEMO_MODE", True)          # auth on: _is_admin really checks
    monkeypatch.setattr(rss, "configured_folders", lambda: [FOLDER])
    monkeypatch.setitem(rss._STATE, "outcome", "synced")
    monkeypatch.setitem(rss._STATE, "running", False)
    monkeypatch.setitem(rss._STATE, "finished_at", "2026-11-15T16:30:59+00:00")
    monkeypatch.setitem(rss._STATE, "report", json.loads(json.dumps(REPORT)))
    monkeypatch.setitem(rss._STATE, "error", None)

    app = FastAPI()
    app.include_router(rsh.router)
    app.add_middleware(EgeriaTokenMiddleware)
    client = TestClient(app)

    def demo(sub, role="user"):
        return jwt.encode({"sub": sub, "role": role, "exp": int(time.time()) + 3600}, dfh._JWT_SECRET, algorithm="HS256")

    def _get(who):
        headers, cookies = {}, {}
        if who == "peter":            # a signed-in viewer: an Egeria token and a non-admin demo session
            headers["X-Egeria-Token"] = _unsigned("peterprofile")
            cookies["demo_token"] = demo("peterprofile")
        elif who == "admin":
            headers["X-Egeria-Token"] = _unsigned("garygeeke")
            cookies["demo_token"] = demo("garygeeke", role="admin")
        r = client.get("/api/report-specs/sync", headers=headers, cookies=cookies)
        assert r.status_code == 200, r.text
        return r.json()
    return _get


@pytest.mark.parametrize("who", ["peter", "anonymous"])
def test_a_non_admin_sees_no_skipped_name_or_zone(get, who):
    st = get(who)
    text = json.dumps(st)
    for secret in (HIDDEN, "ZZ other zoned", "Draft Thing", ZONE, "financeteam"):
        assert secret not in text, f"{secret!r} reached a non-admin ({who})"
    rep = st["report"]
    assert st["detail"] is False and "skipped" not in rep
    assert rep["skipped_count"] == 3                                   # still honest: three were skipped
    assert rep["skipped_categories"] == [["zoned", 2], ["not active", 1]]
    assert rep["unchanged"] == ["Shared One", "Shared Two"]            # shared specs stay named


def test_an_admin_keeps_the_full_detail(get):
    st = get("admin")
    assert st["detail"] is True
    names = [who for who, _why in st["report"]["skipped"]]
    assert HIDDEN in names and ZONE in json.dumps(st["report"]["skipped"])


def test_a_signed_in_non_admin_no_longer_gets_the_error_text(get, monkeypatch):
    monkeypatch.setitem(rss._STATE, "outcome", "failed")
    monkeypatch.setitem(rss._STATE, "error", f"RuntimeError: {HIDDEN} in zone {ZONE}")
    assert HIDDEN not in json.dumps(get("peter"))
    assert HIDDEN in get("admin")["error"]


def test_no_skips_reads_zero_not_absent(get, monkeypatch):
    rep = dict(REPORT, skipped=[])
    monkeypatch.setitem(rss._STATE, "report", rep)
    got = get("peter")["report"]
    assert got["skipped_count"] == 0 and got["skipped_categories"] == []


def test_an_unknown_reason_is_other_never_its_words():
    assert rss.skip_summary([["X", f"something new about {HIDDEN}"]]) == [["other", 1]]
    assert rss.skip_category(None) == "other"


def test_the_explorer_counts_and_shows_the_categories():
    html = (ROOT / "type-explorer.html").read_text(encoding="utf-8")
    assert "r.skipped_count != null ? r.skipped_count" in html          # "N skipped" uses the count
    assert "skipped_categories" in html and "shown to administrators only" in html
    assert "Whether a restricted report spec can run is not checked here" in html   # A1
