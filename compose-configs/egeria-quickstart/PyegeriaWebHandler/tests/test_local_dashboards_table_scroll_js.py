"""Local Dashboards: large result tables scroll inside their tile.

Owner, 2026-11-11: "In local dashboards, can we have scroll bars in large
tables?" Every table the page renders (markdown TABLE output and JSON/DICT
results, in tiles and in the drill-down drawer) is wrapped in .tbl-scroll,
which scrolls both ways, caps a tile's table height and keeps the header row
in view. Small tables lay out as before.

The renderers run under node (skipped when node is not installed; the Portal
container has none). The CSS is checked as text, and in a real browser by the
preview check in the hand-over."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LD = (ROOT / "local-dashboards.html").read_text()


def _grab(pat):
    m = re.search(pat, LD, re.S)
    assert m, pat
    return m.group(0)


def _node(expr):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = "\n".join([
        _grab(r"function esc\(s\) \{.*?\n\}"),
        _grab(r"var TABLE_WIDE_COLS = [^\n]*;"),
        _grab(r"function tableWrapOpen\(nCols\) \{.*?\n\}"),
        _grab(r"var TABLE_WRAP_CLOSE = [^\n]*;"),
        _grab(r"function renderMdToHtml\(rawText\) \{.*?\n\}\n"),
        _grab(r"var JSON_TABLE_MAX_ROWS = [^\n]*;"),
        _grab(r"function hiddenColumnsNote\(hidden\) \{.*?\n\}"),
        _grab(r"function renderJsonTableHtml\(data, unmeasured\) \{.*?\n\}\n"),
        f"console.log(JSON.stringify({expr}));",
    ])
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _md_table(cols, rows):
    head = "| " + " | ".join(f"c{j}" for j in range(cols)) + " |"
    sep = "|" + "---|" * cols
    body = ["| " + " | ".join(f"r{i}c{j}" for j in range(cols)) + " |" for i in range(rows)]
    return "\n".join([head, sep, *body])


def _wrapped_tables(html):
    """Each <table> with the element that opens just before it."""
    return re.findall(r'(<div class="tbl-scroll">)?<table([^>]*)>', html)


def test_markdown_table_is_wrapped():
    html = _node(f"renderMdToHtml({json.dumps('Intro\n\n' + _md_table(3, 60))})")
    tables = _wrapped_tables(html)
    assert len(tables) == 1 and tables[0][0], html[:200]
    assert html.count("<tr>") == 61                       # every row is rendered, none dropped
    assert html.rstrip().endswith("</table></div>")


def test_small_table_keeps_its_old_layout():
    html = _node(f"renderMdToHtml({json.dumps(_md_table(3, 2))})")
    (wrap, attrs), = _wrapped_tables(html)
    assert wrap and attrs == ""                           # no tbl-wide class, no min width


def test_wide_table_gets_minimum_column_widths():
    html = _node(f"renderMdToHtml({json.dumps(_md_table(8, 2))})")
    (wrap, attrs), = _wrapped_tables(html)
    assert 'class="tbl-wide"' in attrs and "--tbl-cols:8" in attrs


def test_json_table_is_wrapped_and_shows_far_more_than_before():
    rows = [{f"k{j}": f"v{i}-{j}" for j in range(12)} for i in range(150)]
    html = _node(f"renderJsonTableHtml({json.dumps(rows)}, false)")
    (wrap, attrs), = _wrapped_tables(html)
    assert wrap and "--tbl-cols:12" in attrs
    assert html.count("<tr>") == 151                      # was capped at 25 rows
    assert html.count("<th>") == 12                       # was capped at 8 columns
    assert "more rows" not in html and "more columns" not in html


def test_json_table_names_what_is_beyond_its_caps():
    rows = [{f"k{j}": j for j in range(25)} for _ in range(230)]
    html = _node(f"renderJsonTableHtml({json.dumps(rows)}, false)")
    assert html.count("<tr>") == 201 and html.count("<th>") == 20
    assert "+30 more rows" in html
    assert "+5 more columns: k20, k21, k22, k23, k24<" in html   # n1: names what isn't shown


def test_hidden_columns_note_names_and_truncates():
    notes = _node("[hiddenColumnsNote(['a']), hiddenColumnsNote(['a', 'b']), "
                  "hiddenColumnsNote(['c1','c2','c3','c4','c5','c6','c7','c8','c9'])]")
    assert notes == [
        "+1 more column: a",
        "+2 more columns: a, b",
        "+9 more columns: c1, c2, c3, c4, c5, c6, and 3 more",
    ]


def test_hidden_column_names_are_escaped():
    rows = [{**{f"k{j}": j for j in range(20)}, "<b>x</b>": 1}]
    html = _node(f"renderJsonTableHtml({json.dumps(rows)}, false)")
    assert "+1 more column: &lt;b&gt;x&lt;/b&gt;" in html and "<b>x</b>" not in html


def test_css_scrolls_caps_height_and_keeps_header():
    css = LD[:LD.index("</style>")]
    assert re.search(r"\.tbl-scroll \{[^}]*overflow:auto", css)
    assert re.search(r"\.placement \.tbl-scroll \{[^}]*max-height:\d+px", css)
    assert re.search(r"\.tbl-scroll thead th \{[^}]*position:sticky;[^}]*top:0", css)
    assert re.search(r"\.tbl-scroll thead th \{[^}]*background:var\(--card\)", css)   # opaque, rows don't show through
    assert re.search(r"\.tbl-scroll::-webkit-scrollbar \{[^}]*width:", css)           # always-visible bars
    assert re.search(r"\.tbl-scroll table\.tbl-wide \{[^}]*min-width:calc\(var\(--tbl-cols\)", css)
    # n3: separate borders, so scrolled rows can't show through above the sticky header.
    assert re.search(r"\.tbl-scroll table \{[^}]*border-collapse:separate;[^}]*border-spacing:0", css)
    # n2: the drawer caps its table too, so the header sticks while it scrolls.
    assert re.search(r"\.dd-body \.tbl-scroll \{[^}]*max-height:\d+vh", css)
    # n4: Firefox bars, scoped so Chrome 121+ keeps the ::-webkit-scrollbar styling.
    ff = re.search(r"@supports \(-moz-appearance:none\) \{(.*?)\n  \}", css, re.S)
    assert ff and "scrollbar-width:thin" in ff.group(1) and "scrollbar-color:" in ff.group(1)
    outside = css.replace(ff.group(0), "")
    assert "scrollbar-width:" not in outside and "scrollbar-color:" not in outside   # declarations, not the comment


def test_no_table_bypasses_the_wrapper():
    script = LD[LD.index("</style>"):]
    assert "'<table" not in script.replace("'<div class=\"tbl-scroll\"><table'", "")
