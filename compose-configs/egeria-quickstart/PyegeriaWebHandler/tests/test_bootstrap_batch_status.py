# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
"""Data Initialization status: per-file run ledger (successes AND failures),
the batch-level roll-up, and live progress -- bootstrap_batches.py."""
import asyncio
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bootstrap_batches as bb  # noqa: E402


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    path = tmp_path / "ledger.json"
    monkeypatch.setenv("PYEGERIA_BOOTSTRAP_LEDGER", str(path))
    bb._progress.clear()
    bb._queued.clear()
    bb._owners.clear()
    yield path
    bb._progress.clear()
    bb._queued.clear()
    bb._owners.clear()


def _doc(tmp_path, name="a.md", text="## Create Glossary\n"):
    p = tmp_path / name
    p.write_text(text)
    return p


def test_failure_is_recorded_without_faking_a_success(ledger, tmp_path):
    doc = _doc(tmp_path)
    bb.record_result(doc, "failed", "exit 1: boom\nline two")
    state = bb._ledger_state(doc, bb._load_ledger())
    assert state["lastStatus"] == "failed"
    assert state["lastMessage"] == "exit 1: boom line two"
    assert state["lastAttemptAt"]
    assert state["lastRunAt"] is None
    assert state["runState"] == "no_record"   # never succeeded -- not "current"


def test_failure_after_success_keeps_last_success(ledger, tmp_path):
    doc = _doc(tmp_path)
    bb.record_run(doc)
    first_ok = bb._load_ledger()[str(doc.resolve())]["lastRunAt"]
    bb.record_result(doc, "failed", "timed out", source="auto-heal")
    state = bb._ledger_state(doc, bb._load_ledger())
    assert state["lastStatus"] == "failed"
    assert state["lastSource"] == "auto-heal"
    assert state["lastRunAt"] == first_ok
    assert state["runState"] == "current"


def test_success_clears_failure_message(ledger, tmp_path):
    doc = _doc(tmp_path)
    bb.record_result(doc, "failed", "boom")
    bb.record_run(doc)
    state = bb._ledger_state(doc, bb._load_ledger())
    assert state["lastStatus"] == "ok" and state["lastMessage"] == ""


def test_legacy_entry_reads_as_ok(ledger, tmp_path):
    doc = _doc(tmp_path)
    ledger.write_text(json.dumps({str(doc.resolve()): {"sha256": bb._file_sha(doc),
                                                       "lastRunAt": "2026-11-01T00:00:00Z"}}))
    state = bb._ledger_state(doc, bb._load_ledger())
    assert state["lastStatus"] == "ok"
    assert state["lastAttemptAt"] == "2026-11-01T00:00:00Z"
    assert state["runState"] == "current"


def _f(name, **kw):
    base = {"name": name, "enabled": True, "runState": "no_record", "lastRunAt": None,
            "lastAttemptAt": None, "lastStatus": None}
    return {**base, **kw}


@pytest.mark.parametrize("files,expected", [
    ([_f("a"), _f("b")], "never_run"),
    ([_f("a", lastAttemptAt="2026-11-15T01:00:00Z", lastStatus="ok", runState="current"), _f("b")], "partial"),
    ([_f("a", lastAttemptAt="2026-11-15T01:00:00Z", lastStatus="ok", runState="changed")], "changed"),
    ([_f("a", lastAttemptAt="2026-11-15T01:00:00Z", lastStatus="failed")], "failed"),
    ([_f("a", lastAttemptAt="2026-11-15T01:00:00Z", lastStatus="ok", runState="current"),
      _f("b", enabled=False)], "ok"),   # disabled files don't count
])
def test_batch_summary_status(ledger, files, expected):
    assert bb._batch_run_summary("B", files)["status"] == expected


def test_batch_summary_last_run_is_latest_attempt(ledger):
    files = [_f("a", lastAttemptAt="2026-11-15T01:00:00Z", lastStatus="ok", runState="current"),
             _f("b", lastAttemptAt="2026-11-15T03:00:00Z", lastStatus="failed")]
    s = bb._batch_run_summary("B", files)
    assert s["lastRunAt"] == "2026-11-15T03:00:00Z" and s["failedFiles"] == ["b"]


def test_progress_and_queue(ledger):
    bb.set_queued(["A", "B"], source="auto-heal")
    assert bb._batch_run_summary("B", [_f("x")])["status"] == "queued"
    bb.set_progress("B", "x.md", 2, 5)
    s = bb._batch_run_summary("B", [_f("x")])
    assert s["status"] == "running" and s["progress"]["index"] == 2 and s["progress"]["file"] == "x.md"
    started = s["progress"]["startedAt"]
    bb.set_progress("B", "y.md", 3, 5)
    assert bb._progress["B"]["startedAt"] == started   # batch start, not file start
    bb.clear_progress("B")
    assert bb._batch_run_summary("B", [_f("x")])["status"] == "never_run"


def test_run_batch_records_failure_and_clears_progress(ledger, tmp_path, monkeypatch):
    good = _doc(tmp_path, "good.md")
    bad = _doc(tmp_path, "bad.md")
    seen_progress = []

    def fake_command(doc, userid):
        seen_progress.append(dict(bb._progress.get("T") or {}))
        code = 0 if doc.name == "good.md" else 3
        return [sys.executable, "-c", f"print('out-{doc.name}'); raise SystemExit({code})"], None, None

    monkeypatch.setattr(bb, "run_command", fake_command)
    batch = {"id": "T", "path": str(tmp_path), "files": ["good.md", "bad.md"], "userids": {}}
    results = asyncio.run(bb.run_batch(batch, timeout_seconds=30))

    assert [r["status"] for r in results] == ["ok", "failed"]
    assert [p["index"] for p in seen_progress] == [1, 2]
    assert "T" not in bb._progress
    ledger_now = bb._load_ledger()
    assert ledger_now[str(good.resolve())]["lastStatus"] == "ok"
    bad_entry = ledger_now[str(bad.resolve())]
    assert bad_entry["lastStatus"] == "failed" and "exit 3" in bad_entry["lastMessage"]
    assert "lastRunAt" not in bad_entry


# ── One run per batch: manual runs and auto-heal don't overlap ────────────
def test_manual_run_refuses_batch_auto_heal_owns(ledger, tmp_path, monkeypatch):
    _doc(tmp_path, "a.md")
    ran = []
    monkeypatch.setattr(bb, "run_command", lambda doc, userid: ran.append(doc) or ([sys.executable, "-c", "pass"], None, None))
    assert bb.claim_batch("T", "auto-heal") is None
    bb.set_progress("T", "a.md", 1, 1, source="auto-heal")
    batch = {"id": "T", "path": str(tmp_path), "files": ["a.md"], "userids": {}}
    results = asyncio.run(bb.run_batch(batch, timeout_seconds=30))
    assert [r["status"] for r in results] == ["busy"] and "auto-heal" in results[0]["message"]
    assert ran == []
    assert bb._progress["T"]["source"] == "auto-heal"   # the refused run didn't clear the live line
    assert bb.batch_owner("T") == "auto-heal"


def test_run_batch_releases_claim(ledger, tmp_path, monkeypatch):
    _doc(tmp_path, "a.md")
    monkeypatch.setattr(bb, "run_command", lambda doc, userid: ([sys.executable, "-c", "pass"], None, None))
    batch = {"id": "T", "path": str(tmp_path), "files": ["a.md"], "userids": {}}
    assert [r["status"] for r in asyncio.run(bb.run_batch(batch, timeout_seconds=30))] == ["ok"]
    assert bb.batch_owner("T") is None
    assert bb.claim_batch("T", "auto-heal") is None


def test_owned_batch_is_not_marked_queued(ledger):
    bb.claim_batch("A", "manual")
    bb.set_queued(["A", "B"], source="auto-heal")
    assert "A" not in bb._queued and bb._queued["B"] == "auto-heal"
    bb.clear_queued(["B"])
    assert "B" not in bb._queued


def test_auto_heal_skips_batch_a_manual_run_owns(ledger, tmp_path, monkeypatch):
    mon = pytest.importorskip("bootstrap_monitor_handler")
    doc = _doc(tmp_path, "a.md")
    monkeypatch.setattr(mon, "_run_command", lambda d, u: pytest.fail("auto-heal ran a doc a manual run owns"))
    bb.claim_batch("T", "manual")
    family = {"name": "T", "docs": [str(doc)], "batch_id": "T"}
    result = asyncio.run(mon._heal_family(family))
    assert result.startswith("skipped") and bb.batch_owner("T") == "manual"


# ── Notebook runner: check-only cells ───────────────────────────────────────
nbformat = pytest.importorskip("nbformat")
pytest.importorskip("nbclient")
pytest.importorskip("ipykernel")


def _run_notebook(tmp_path, cells, timeout=20, check_timeout=2):
    import subprocess
    nb = nbformat.v4.new_notebook()
    for src, tags in cells:
        c = nbformat.v4.new_code_cell(src)
        if tags:
            c.metadata["tags"] = tags
        nb.cells.append(c)
    src_path, out_path = tmp_path / "nb.ipynb", tmp_path / "out.ipynb"
    nbformat.write(nb, src_path)
    proc = subprocess.run([sys.executable, "-c", bb._NOTEBOOK_RUNNER, str(src_path), str(out_path),
                           str(timeout), str(check_timeout)],
                          cwd=tmp_path, capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr


def test_check_only_timeout_is_skipped_and_later_cells_run(tmp_path):
    code, summary = _run_notebook(tmp_path, [
        ("x = 1", None),
        ("import time; time.sleep(30)", ["check-only"]),
        ("open('after.txt', 'w').write(str(x))", None),
    ])
    assert code == 0, summary
    assert "check-only cell 2" in summary and "CellTimeoutError" in summary
    assert (tmp_path / "after.txt").read_text() == "1"


def test_check_only_exception_is_skipped(tmp_path):
    code, summary = _run_notebook(tmp_path, [("raise ValueError('nope')", ["check-only"]), ("y = 2", None)])
    assert code == 0 and "ValueError" in summary


def test_untagged_timeout_still_fails_with_cell_number(tmp_path):
    code, summary = _run_notebook(tmp_path, [("x = 1", None), ("import time; time.sleep(30)", None)],
                                  timeout=2)
    assert code == 1
    assert summary.startswith("cell 2 of 2:") and "CellTimeoutError" in summary


def test_untagged_error_still_fails(tmp_path):
    code, summary = _run_notebook(tmp_path, [("raise KeyError('k')", None), ("y = 2", None)])
    assert code == 1 and summary.startswith("cell 1 of 2:") and "KeyError" in summary
