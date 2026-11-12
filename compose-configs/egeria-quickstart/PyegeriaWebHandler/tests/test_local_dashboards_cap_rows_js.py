"""Local Dashboards: long results are capped at whole table rows, with an honest note.

Architect finding F-LD1 (2026-11-11): the CDO "Governance Metric Register"
tile (a LIST report, 46 rows, 84 KB) showed 12 of 46 rows. _capContent cut
the markdown at 20,000 characters, mid-row, and said "this placement has no
query scope", which was false: it is scoped by search_string.

Now tables are capped only at whole rows, far higher (they scroll inside the
tile since #833), with "Showing the first N of M rows (this tile's render
limit)". The 20,000-character cap applies to text outside tables, and its
note names the placement's real scope, or says it has none.

The fixture is that tile's real result, captured read-only from laz on
pyegeria 6.2.37. Run under node; skipped when node is not installed (the
Portal container has none)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LD = (HERE.parent / "local-dashboards.html").read_text()
GM = json.loads((HERE / "fixtures" / "governance_metric_register_list_laz_2026_11_11.json").read_text())


def _grab(pat):
    m = re.search(pat, LD, re.S)
    assert m, pat
    return m.group(0)


def _node(expr, **data):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = "\n".join([
        _grab(r"var _MAX_RENDER_CHARS = [^\n]*"),
        _grab(r"var _MAX_TABLE_ROWS = [^\n]*"),
        _grab(r"var _MAX_TABLE_CHARS = [^\n]*"),
        _grab(r"function _scopeWords\(params\) \{.*?\n\}"),
        _grab(r"function _truncationNote\(params\) \{.*?\n\}"),
        _grab(r"function _isTableStart\(lines, i\) \{.*?\n\}"),
        _grab(r"function _capContent\(text, params\) \{.*?\n\}"),
        _grab(r"function esc\(s\) \{.*?\n\}"),
        _grab(r"var TABLE_WIDE_COLS = [^\n]*;"),
        _grab(r"function tableWrapOpen\(nCols\) \{.*?\n\}"),
        _grab(r"var TABLE_WRAP_CLOSE = [^\n]*;"),
        _grab(r"function restoreCellBreaks\(s\) \{.*?\n\}"),
        _grab(r"function renderMdToHtml\(rawText\) \{.*?\n\}\n"),
        *[f"var {k} = {json.dumps(v)};" for k, v in data.items()],
        f"console.log(JSON.stringify({expr}));",
    ])
    # Script on stdin: some inputs are larger than the OS argument limit.
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _data_rows(md):
    lines = md.split("\n")
    start = next(i for i in range(len(lines) - 1)
                 if lines[i].startswith("|") and re.match(r"^\|[\s\-:|]+\|", lines[i + 1]))
    rows = []
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            break
        rows.append(l)
    return rows


def test_fixture_is_the_real_f_ld1_shape():
    assert len(GM["content"]) > 20000
    assert len(_data_rows(GM["content"])) == 46
    assert "<br>" in GM["content"]                      # 6.2.37 LIST bullets


def test_governance_metric_register_keeps_all_46_rows():
    capped = _node("_capContent(TEXT, PARAMS)", TEXT=GM["content"], PARAMS=GM["params"])
    assert capped == GM["content"]                      # nothing cut, nothing added
    html = _node("renderMdToHtml(_capContent(TEXT, PARAMS))", TEXT=GM["content"], PARAMS=GM["params"])
    assert len(re.findall(r"<tr>", html)) == 47         # header + 46 rows
    assert "truncated" not in html.lower()


def test_old_cap_would_have_cut_mid_row():
    """Pins the F-LD1 failure: 20,000 characters lands inside a row."""
    head = GM["content"][:20000]
    assert len(_data_rows(head)) < 46 and not head.endswith("|")


def test_table_over_the_row_limit_is_cut_at_whole_rows_and_counted():
    header = "| Name | Notes |\n|---|---|\n"
    rows = [f"| m{i} | a<br>b |" for i in range(1500)]
    text = "### Big\n\n" + header + "\n".join(rows) + "\n\nAfter the table."
    out = _node("_capContent(TEXT, {})", TEXT=text)
    kept = _data_rows(out)
    assert len(kept) == 1000 and kept[-1] == "| m999 | a<br>b |"   # whole rows only
    assert "*Showing the first 1000 of 1500 rows (this tile's render limit).*" in out
    assert out.rstrip().endswith("After the table.")               # text after the table survives


def test_table_over_the_char_limit_is_cut_at_whole_rows():
    big = "x" * 300000
    text = "| A |\n|---|\n" + "\n".join(f"| {i}{big} |" for i in range(5))
    out = _node("_capContent(TEXT, {})", TEXT=text)
    kept = _data_rows(out)
    assert len(kept) == 3 and all(r.endswith(" |") for r in kept)
    assert "Showing the first 3 of 5 rows" in out


def test_scoped_text_truncation_names_the_real_scope():
    text = "\n".join("prose line %d " % i + "y" * 200 for i in range(200))
    out = _node("_capContent(TEXT, PARAMS)", TEXT=text,
                PARAMS={"search_string": "CocoPharma::GovernanceMetric::", "page_size": 50, "empty": "", "none": None})
    assert "has no query scope" not in out
    assert "This placement is scoped by search_string=CocoPharma::GovernanceMetric::, page_size=50" in out
    assert "render limit of 20,000 characters" in out
    body = out.split("\n\n*(Text truncated")[0]
    assert len(body) <= 20000 and body.split("\n")[-1].startswith("prose line")   # cut at a line, not mid-line


@pytest.mark.parametrize("params", [{}, None, {"search_string": "  "}, {"filters": []}])
def test_unscoped_text_truncation_says_so(params):
    text = "z" * 100 + "\n" + ("w" * 30000)
    out = _node("_capContent(TEXT, PARAMS)", TEXT=text, PARAMS=params)
    assert "This placement has no query scope" in out


def test_cut_inside_a_mermaid_fence_drops_the_half_diagram():
    text = "Intro\n```mermaid\ngraph TD\n" + "\n".join(f"  n{i} --> n{i+1}" for i in range(3000)) + "\n```\nEnd"
    out = _node("_capContent(TEXT, {})", TEXT=text)
    assert "```" not in out and out.startswith("Intro\n\n*(Text truncated")


def test_short_text_is_untouched():
    assert _node("_capContent('a\\n| A |\\n|---|\\n| 1 |', {})") == "a\n| A |\n|---|\n| 1 |"


def test_every_caller_passes_the_placement_params():
    assert "renderExecResult(result, effParams)" in LD          # drill-down drawer
    assert "renderExecResult(result, analyticParams)" in LD     # analytic placement
    assert "renderExecResult(result, params)" in LD             # report placement
    assert len(re.findall(r"_capContent\([^)]*\)", LD)) == 3    # definition + text + string-JSON
    assert all(c.endswith(", params)") for c in re.findall(r"_capContent\(result\.[a-z]+, params\)", LD))
