# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-35: the Data scope editor (The Catalog and the Locator's lens form) takes typed dates, not a
date-and-time picker that filled in the time of day; it shows a stored start or end as just its
day (UTC) when it is that day's first or last instant; a chip shows a whole year or month as
"2026" or "2026-03". Runs dataScopeDateText and dataScopePeriodText under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
_JS = (_DIR / "static" / "data-scope-editor.js").read_text()


def _fn(name: str) -> str:
    start = _JS.index(f"  function {name}(")
    return _JS[start:_JS.index("\n  }\n", start) + 5]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_stored_times_show_as_days_and_whole_periods_collapse():
    js = "\n".join(_fn(n) for n in ("_pad", "dataScopeDateText", "dataScopePeriodText")) + r"""
console.log(JSON.stringify({
  start: dataScopeDateText('2026-01-01T00:00:00.000+00:00', 'start'),
  end: dataScopeDateText('2026-12-31T23:59:59.999+00:00', 'end'),
  oldSave: dataScopeDateText('2026-01-01T09:04:00.000+00:00', 'start'),
  empty: dataScopeDateText(null, 'start'),
  year: dataScopePeriodText('2026-01-01T00:00:00Z', '2026-12-31T23:59:59.999Z'),
  month: dataScopePeriodText('2026-02-01T00:00:00Z', '2026-02-28T23:59:59.999Z'),
  span: dataScopePeriodText('2026-01-01T00:00:00Z', '2026-06-30T23:59:59.999Z'),
  open: dataScopePeriodText('2026-01-01T00:00:00Z', null),
  po35: dataScopePeriodText('2026-01-01T09:04:00.000+00:00', '2026-12-31T09:05:00.000+00:00'),
}));"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["start"] == "2026-01-01" and d["end"] == "2026-12-31"
    assert d["oldSave"] == "2026-01-01 09:04" and d["empty"] == ""
    assert d["year"] == "2026" and d["month"] == "2026-02"
    assert d["span"] == "2026-01-01 → 2026-06-30"
    assert d["open"] == "2026-01-01 → …"
    assert d["po35"] == "2026-01-01 09:04 → 2026-12-31 09:05 UTC"    # an old save says what it holds


def test_dates_are_typed_not_picked():
    assert "datetime-local" not in _JS
    assert "yyyy, yyyy-mm or yyyy-mm-dd" in _JS
    for page in ("resource-browser.html", "tech-catalog.html"):
        assert "data-scope-editor.js?v=2026-11-17b" in (_DIR / page).read_text(), page
