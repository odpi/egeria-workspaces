"""<br> in markdown table cells (pyegeria 6.2.37+).

pyegeria writes <br> inside table cells for a newline in a value (fix-now F9)
and between LIST bullets (R3); GFM tables accept it. The Portal's renderers
escape every cell, so it used to show as literal "a<br>b" text (for example
Mandy's CDO register tiles). Each renderer now turns back ONLY the exact
escaped forms of <br>, <br/> and <br /> inside table cells; everything else
stays escaped.

Choice for text that spells the entity itself: a source cell containing the
literal characters "&lt;br&gt;" is escaped to "&amp;lt;br&amp;gt;", which
the fix does not match, so it is shown as the text "&lt;br&gt;" and is
never a line break. Only a raw <br> tag becomes a break.

Covers the three renderers: local-dashboards.html renderMdToHtml, and
_renderMdHtml in the quickstart and freshstart copies of
static/egeria-shared-ui.js. Run under node; skipped when node is not
installed (the Portal container has none)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
QS = HERE.parent
FS = QS.parent.parent / "egeria-freshstart" / "PyegeriaWebHandler"
LD = (QS / "local-dashboards.html").read_text()


def _grab(src, pat):
    m = re.search(pat, src, re.S)
    assert m, pat
    return m.group(0)


def _ld_js():
    return "\n".join([
        _grab(LD, r"function esc\(s\) \{.*?\n\}"),
        _grab(LD, r"var TABLE_WIDE_COLS = [^\n]*;"),
        _grab(LD, r"function tableWrapOpen\(nCols\) \{.*?\n\}"),
        _grab(LD, r"var TABLE_WRAP_CLOSE = [^\n]*;"),
        _grab(LD, r"function restoreCellBreaks\(s\) \{.*?\n\}"),
        _grab(LD, r"function renderMdToHtml\(rawText\) \{.*?\n\}\n"),
        "var RENDER = renderMdToHtml;",
    ])


def _shared_js(path):
    ui = path.read_text()
    return "\n".join([
        _grab(ui, r"function _mdCellBreaks\(s\) \{.*?\n\}"),
        _grab(ui, r"function _renderMdHtml\(rawText\) \{.*?\n\}\n"),
        "var RENDER = _renderMdHtml;",
    ])


RENDERERS = {
    "local-dashboards": _ld_js,
    "shared-ui quickstart": lambda: _shared_js(QS / "static" / "egeria-shared-ui.js"),
    "shared-ui freshstart": lambda: _shared_js(FS / "static" / "egeria-shared-ui.js"),
}


def _render(which, md):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = RENDERERS[which]() + f"\nconsole.log(JSON.stringify(RENDER({json.dumps(md)})));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _cells(html):
    return re.findall(r"<td[^>]*>(.*?)</td>", html, re.S)


def _table(*cells):
    return "| A | B |\n|---|---|\n" + "\n".join(f"| {a} | {b} |" for a, b in cells)


ALL = list(RENDERERS)


@pytest.mark.parametrize("which", ALL)
def test_br_in_a_cell_is_a_line_break_in_one_cell(which):
    html = _render(which, _table(("a<br>b", "x"), ("one<br/>two<br />three", "y")))
    cells = _cells(html)
    assert cells[0] == "a<br>b"                         # two lines, one td
    assert cells[2] == "one<br>two<br>three"
    assert len(cells) == 4
    assert "&lt;br" not in html


@pytest.mark.parametrize("which", ALL)
def test_list_bullets_from_pyegeria_render_as_lines(which):
    # R3's LIST shape: bullets joined by <br>, with a "(+N more)" tail.
    html = _render(which, _table(("Risk", "• Implication one<br>• Implication two (+3 more)")))
    assert _cells(html)[1] == "• Implication one<br>• Implication two (+3 more)"


@pytest.mark.parametrize("which", ALL)
def test_nothing_else_is_unescaped(which):
    html = _render(which, _table(
        ("<script>alert(1)</script>", "<img src=x onerror=alert(1)>"),
        ("<br onclick=alert(1)>", "<BR>"),
        ("<b>bold</b>", "<br><script>x</script>"),
    ))
    assert "<script" not in html and "<img" not in html and "<b>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "&lt;br onclick=alert(1)&gt;" in html          # only the exact forms come back
    assert "&lt;BR&gt;" in html                           # exact = lower-case, as pyegeria writes it
    assert "<br>&lt;script&gt;x&lt;/script&gt;" in html   # a real <br> next to escaped script


@pytest.mark.parametrize("which", ALL)
def test_spelled_out_entity_stays_text(which):
    html = _render(which, _table(("see &lt;br&gt; here", "z")))
    assert _cells(html)[0] == "see &amp;lt;br&amp;gt; here"   # shows as the text "&lt;br&gt;"


@pytest.mark.parametrize("which", ALL)
def test_br_outside_tables_is_unchanged(which):
    # Only table cells were changed; prose stays fully escaped as before.
    html = _render(which, "Some text a<br>b")
    assert "a&lt;br&gt;b" in html


def test_cache_busters_bumped_together():
    """Both copies changed, so every page that loads either copy must have the new ?v=."""
    pages = list(QS.glob("*.html")) + list(FS.glob("*.html"))
    versions = {}
    for p in pages:
        for v in re.findall(r"egeria-shared-ui\.js\?v=([\w-]+)", p.read_text()):
            versions.setdefault(p.parent.parent.name, set()).add(v)
    assert all(len(v) == 1 for v in versions.values()), versions   # one version per environment
