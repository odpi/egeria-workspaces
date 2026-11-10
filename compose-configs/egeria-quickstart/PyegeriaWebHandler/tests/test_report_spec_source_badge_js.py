"""static/report-spec-source.js: the source badge pages show on a report-spec run (local-dashboards,
governance-metrics). Runs under node; skips when node is not installed (the container has none).
The wiring checks run everywhere."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

DIR = Path(__file__).resolve().parent.parent
JS = DIR / "static" / "report-spec-source.js"


def _badge(expr):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = f"var S = require({json.dumps(str(JS))}); console.log(JSON.stringify({expr}));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_each_source_renders_its_words_and_colour():
    for src, words, colour in (("builtin", "pyegeria built-in", "#94a3b8"), ("egeria", "held in Egeria", "#34d399"),
                               ("local", "Portal (local)", "#60a5fa"), ("user", "user spec file", "#c084fc")):
        html = _badge(f"S.badgeHtml({{source: {json.dumps(src)}, sourceLabel: {json.dumps(words)}}})")
        assert words in html and colour in html and 'class="eg-spec-source"' in html


def test_no_source_or_unknown_source_renders_nothing():
    assert _badge("S.badgeHtml(null)") == ""
    assert _badge("S.badgeHtml({source: 'mystery'})") == ""
    assert _badge("S.blockHtml({kind: 'json', data: 1})") == ""           # result without specSource
    assert _badge("S.blockHtml({kind: 'json', data: 1, specSource: null})") == ""


def test_shadow_is_said_and_text_is_escaped():
    html = _badge("S.badgeHtml({source: 'local', sourceLabel: 'Portal (local)', shadows: 'builtin'})")
    assert "shadows the builtin copy" in html
    html = _badge("S.badgeHtml({source: 'builtin', shadowedBy: 'egeria'})")
    assert "shadowed by the egeria copy" in html and "pyegeria built-in" in html
    html = _badge("S.badgeHtml({source: 'egeria', sourceLabel: '<b>x</b>'})")
    assert "<b>x</b>" not in html and "&lt;b&gt;x&lt;/b&gt;" in html


def test_block_wraps_the_badge_from_a_run_result():
    html = _badge("S.blockHtml({kind: 'json', data: 1, specSource: {source: 'egeria', sourceLabel: 'held in Egeria'}})")
    assert html.startswith('<div class="eg-spec-source-line"') and "held in Egeria" in html


def test_pages_load_and_use_the_helper():
    for page in ("local-dashboards.html", "governance-metrics.html"):
        text = (DIR / page).read_text()
        assert '<script src="/static/report-spec-source.js?v=' in text
        assert "window.EgeriaSpecSource.blockHtml(" in text
    # same words as Egeria Explorer's Report Specs view and the API
    te = (DIR / "type-explorer.html").read_text()
    for colour in ("#34d399", "#60a5fa", "#c084fc"):
        assert colour in te and colour in JS.read_text()
    rs = (DIR / "report_specs_handler.py").read_text()
    for words in ("pyegeria built-in", "held in Egeria", "Portal (local)", "user spec file"):
        assert words in rs and words in JS.read_text()
