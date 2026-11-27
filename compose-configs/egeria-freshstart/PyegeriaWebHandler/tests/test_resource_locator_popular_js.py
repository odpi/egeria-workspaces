# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator usage chips and the Home "Popular" tile in the freshstart page (PO-27F; parity with
the quickstart's PO-27).

Pinned here (design-docs/popularity-and-usage-measures.md §5):
  - a chip shows reads/day; a measured 0 says "0 reads/day (measured)"; no readings says "not measured";
    a reading without reads/day shows the read count, never 0 reads/day;
  - a row whose classifications were not read says "usage not read" (PO-27 FIX-1);
  - the window in a chip's title shows only the parts recorded, never "undefined" (PO-27 FIX-2);
  - the tile's states are distinct: loading, the read failed, no usage readings on this platform, ranked;
    the as-of date and the reads in window, readers in window and last read (lastReadAt, else
    lastReadInWindow) of each ranked resource are shown; ten are shown and the rest are counted.
Runs the helpers from resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()
_NAMES = ("fmtRate", "lastReadOf", "usageChip", "rowUsageChip", "popularSummary")


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


def _run(body: str):
    js = "\n".join(_fn(n) for n in _NAMES) + "\n" + body
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


@needs_node
def test_fmt_rate_keeps_two_decimals_at_most():
    d = _run("console.log(JSON.stringify([86.36, 0.5, 4, 0.3333, 0, 1.005].map(fmtRate)));")
    assert d[:5] == ["86.36", "0.5", "4", "0.33", "0"]


@needs_node
def test_usage_chip_states():
    d = _run(r"""
console.log(JSON.stringify({
  rate: usageChip({ readsPerDay: 86.36, readCount: 258, readsInWindow: 266, readersInWindow: 3,
                    lastReadAt: '2026-11-27T00:29:17.154Z', analysisService: 'open-lineage-data-scope-governance-service' }),
  zero: usageChip({ readsPerDay: 0, readCount: 0 }),
  countOnly: usageChip({ readCount: 1, lastReadAt: '2026-11-23T23:33:29.889Z' }),
  none: usageChip(null), undef: usageChip(undefined) }));""")
    assert d["rate"]["text"] == "86.36 reads/day" and not d["rate"]["absent"]
    assert "266" in d["rate"]["title"] and "3" in d["rate"]["title"]
    assert "open-lineage-data-scope-governance-service" in d["rate"]["title"]
    assert d["zero"]["text"] == "0 reads/day (measured)"
    assert d["countOnly"]["text"] == "1 reads" and "reads/day" not in d["countOnly"]["text"]
    assert "no reads-per-day reading" in d["countOnly"]["title"]
    assert d["none"] == {"text": "not measured", "absent": True,
                         "title": "No usage readings are recorded on this resource’s data scope"}
    assert d["undef"]["text"] == "not measured"


@needs_node
def test_last_read_falls_back_to_last_read_in_window():
    d = _run("console.log(JSON.stringify([lastReadOf({ lastReadAt: 'a', lastReadInWindow: 'b' }), "
             "lastReadOf({ lastReadInWindow: 'b' }), lastReadOf({}), lastReadOf(null)]));")
    assert d == ["a", "b", None, None]


@needs_node
def test_popular_summary_states_are_distinct():
    d = _run(r"""
var none = { available: false, reason: 'Popularity not available yet: no usage readings on this platform', notMeasured: 126 };
var failed = { available: false, failed: true, reason: 'Popularity could not be read: the read failed.' };
console.log(JSON.stringify({
  loading: popularSummary(null, ''), homeErr: popularSummary(null, 'HTTP 500'),
  none: popularSummary(none, ''), failed: popularSummary(failed, ''),
  old: popularSummary(undefined, '') }));""")
    assert d["loading"]["state"] == "loading"
    assert d["homeErr"]["state"] == "failed" and "could not be read" in d["homeErr"]["message"]
    assert d["none"] == {"state": "none", "message": "Popularity not available yet: no usage readings on this platform",
                         "rows": [], "more": 0, "unranked": [], "asOf": None, "capped": False}
    assert d["failed"]["state"] == "failed" and d["failed"]["message"].startswith("Popularity could not be read")
    assert d["old"]["state"] == "loading"


@needs_node
def test_popular_summary_ranked_shows_ten_and_counts_the_rest():
    d = _run(r"""
var ranking = []; for (var i = 0; i < 14; i++) ranking.push({ guid: 'g' + i, displayName: 'R' + i, usage: { readsPerDay: 14 - i } });
var p = { available: true, ranking: ranking, unranked: [{ guid: 'u', usage: { readCount: 1 } }], shown: 10,
          asOf: '2026-11-27T01:36:26Z', window: { start: '2026-10-28T01:36:26Z', end: '2026-11-27T01:36:26Z' }, capped: true };
console.log(JSON.stringify(popularSummary(p, '')));""")
    assert d["state"] == "ranked"
    assert [r["guid"] for r in d["rows"]] == [f"g{i}" for i in range(10)]
    assert d["more"] == 4 and d["unranked"][0]["guid"] == "u"
    assert d["asOf"] == "2026-11-27T01:36:26Z" and d["capped"] is True


@needs_node
def test_popular_summary_measured_but_none_ranked():
    d = _run(r"""
console.log(JSON.stringify(popularSummary({ available: true, ranking: [], unranked: [{ guid: 'u', usage: { readCount: 1 } }],
  shown: 10, asOf: null }, '')));""")
    assert d["state"] == "ranked" and d["rows"] == [] and len(d["unranked"]) == 1 and d["asOf"] is None


def test_the_tile_no_longer_says_popularity_is_never_available():
    assert "Nothing is ranked by use until Egeria records it" not in _PAGE
    assert "Popularity is not available yet." not in _PAGE


def test_home_shows_the_popular_tile_with_the_as_of_and_the_shown_fields():
    assert "el(Boundary, { what: 'Popular tile' }, el(PopularTile, { home: home, err: err }))" in _PAGE
    tile = _fn("PopularTile")
    assert "'As of '" in tile and "(end of the latest analysis window)" in tile
    assert "reads in window" in tile and "readers in window" in tile and "last read" in tile
    assert "lastReadOf(u)" in tile
    assert "Resources without readings are not measured and not ranked." in tile


@needs_node
def test_a_row_whose_classifications_were_not_read_says_usage_not_read():
    """PO-27 FIX-1: muted "usage not read", neither silent nor "not measured"."""
    d = _run(r"""
console.log(JSON.stringify({
  notRead: rowUsageChip({ usage: null, scopeRead: false }),
  notReadEvenWithUsage: rowUsageChip({ usage: { readsPerDay: 2 }, scopeRead: false }),
  notMeasured: rowUsageChip({ usage: null, scopeRead: true }),
  measured: rowUsageChip({ usage: { readsPerDay: 2 } }),
  notFromRow: rowUsageChip({ guid: 'x' }) }));""")
    assert d["notRead"]["text"] == "usage not read" and d["notRead"]["absent"] is True
    assert d["notReadEvenWithUsage"]["text"] == "usage not read"
    assert d["notMeasured"]["text"] == "not measured"
    assert d["measured"]["text"] == "2 reads/day" and d["measured"]["absent"] is False
    assert d["notFromRow"] is None


@needs_node
def test_the_window_in_the_chip_title_shows_only_the_parts_present():
    """PO-27 FIX-2: no "undefined" in the window title."""
    d = _run(r"""
console.log(JSON.stringify([
  usageChip({ readsPerDay: 1, analysisWindowStart: '2026-10-28T01:36:26Z', analysisWindowEnd: '2026-11-27T01:36:26Z' }).title,
  usageChip({ readsPerDay: 1, analysisWindowEnd: '2026-11-27T01:36:26Z' }).title,
  usageChip({ readsPerDay: 1, analysisWindowStart: '2026-10-28T01:36:26Z' }).title,
  usageChip({ readsPerDay: 1 }).title]));""")
    assert "window: 2026-10-28T01:36:26Z to 2026-11-27T01:36:26Z" in d[0]
    assert "window ends 2026-11-27T01:36:26Z" in d[1]
    assert "window starts 2026-10-28T01:36:26Z" in d[2]
    assert "window" not in d[3]
    assert not any("undefined" in t for t in d)


def test_the_page_helpers_match_the_quickstart_copy():
    """Parity: the usage helpers are the quickstart's, unchanged (skipped without the quickstart page beside)."""
    qs_path = Path(__file__).resolve().parents[3] / "egeria-quickstart" / "PyegeriaWebHandler" / "resource-browser.html"
    if not qs_path.exists():
        pytest.skip(f"{qs_path} not present")
    qs = qs_path.read_text()
    for name in _NAMES + ("UsageChip",):
        start = qs.index(f"function {name}(")
        assert _fn(name) == qs[start:qs.index("\n}\n", start) + 3], name


# ── F3: chips on rows ─────────────────────────────────────────────────────────

def test_result_rows_show_the_usage_chip_fed_by_the_server():
    row = _fn("ResultRow")
    # Every row that went through the server's _row has `usage` (null when not measured).
    assert "rowUsageChip(row) && el(UsageChip, { chip: rowUsageChip(row) })" in row


def test_scope_chips_are_unchanged():
    """F3 must not change freshstart's scope chips: the row's scope chip and ScopeChips stay as they were."""
    assert "row.dataScope && el('span', { className: 'rb-chip', title: 'This resource records its data scope (time or place)' }, '◷ scope')" in _fn("ResultRow")
    assert "chip('extra', 'scope details'" in _fn("ScopeChips")


def test_the_page_no_longer_says_egeria_holds_no_usage_measure():
    assert "Egeria holds no usage measure" not in _PAGE
