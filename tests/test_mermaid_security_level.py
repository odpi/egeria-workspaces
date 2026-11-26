"""Source guard: every served page initialises mermaid with securityLevel 'strict'.

Mermaid text comes from Egeria, including names that element authors set. With 'strict', mermaid does not bind
diagram callbacks. Rendering every real-shape diagram in the fixtures under 'loose' and 'strict' (mermaid 11.17.2,
the version `mermaid@11` resolves to) gave the same labels, line breaks and layout. So no page needs a weaker level.

The guard covers:
- the Portal (quickstart and freshstart PyegeriaWebHandler);
- the Apache markdown viewer (markdown-header.html);
- the Portal Docs viewer;
- the exchange index pages.

Every `mermaid.initialize(...)` call in those files must say `securityLevel: 'strict'`, and no other securityLevel
value may appear. EXPECTED pins each file's number of calls, so a new call site, or a page that gains mermaid, has
to be added here on purpose.

Out of scope: notebooks and the generated sample HTML under coco-workbooks/ and workbooks/. They are not served by
the Portal or Apache.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
Q = "compose-configs/egeria-quickstart/"
F = "compose-configs/egeria-freshstart/"

# file -> number of mermaid.initialize calls it makes
EXPECTED = {
    Q + "PyegeriaWebHandler/static/egeria-shared-ui.js": 1,
    F + "PyegeriaWebHandler/static/egeria-shared-ui.js": 1,
    Q + "PyegeriaWebHandler/lineage-explorer.html": 1,
    F + "PyegeriaWebHandler/lineage-explorer.html": 1,
    Q + "PyegeriaWebHandler/local-dashboards.html": 1,
    Q + "PyegeriaWebHandler/governance-metrics.html": 1,
    Q + "markdown-header.html": 2,
    "portal-docs/viewer.html": 1,
    "exchange-quickstart/distribution-hub/index.html": 1,
    "exchange-quickstart/loading-bay/index.html": 1,
    "exchange-quickstart/loading-bay/dr-egeria-inbox/index.html": 1,
    "exchange-freshstart/distribution-hub/index.html": 1,
    "exchange-freshstart/loading-bay/index.html": 1,
    "exchange-freshstart/loading-bay/dr-egeria-inbox/index.html": 1,
}

SERVED_DIRS = (
    Q + "PyegeriaWebHandler",
    F + "PyegeriaWebHandler",
    "portal-docs",
    "exchange-quickstart",
    "exchange-freshstart",
)
SERVED_FILES = (Q + "markdown-header.html",)
SKIP_PARTS = {"node_modules", "tests", ".venv", "__pycache__"}

INIT = re.compile(r"mermaid\s*\.\s*initialize\s*\(")
LEVEL = re.compile(r"securityLevel\s*:\s*['\"]([A-Za-z]+)['\"]")


def _served_sources():
    files = [ROOT / f for f in SERVED_FILES]
    for d in SERVED_DIRS:
        for p in (ROOT / d).rglob("*"):
            if p.suffix in (".html", ".js") and p.is_file() and not SKIP_PARTS.intersection(p.relative_to(ROOT).parts):
                files.append(p)
    return files


def _init_calls(text: str) -> list[str]:
    """The argument text of each mermaid.initialize( ... ) call, with parentheses balanced."""
    calls = []
    for m in INIT.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            i += 1
        calls.append(text[m.end():i - 1])
    return calls


def test_expected_files_exist():
    missing = [f for f in EXPECTED if not (ROOT / f).is_file()]
    assert not missing, f"call-site files not found: {missing}"


@pytest.mark.parametrize("rel", sorted(EXPECTED))
def test_every_initialize_is_strict(rel):
    calls = _init_calls((ROOT / rel).read_text(encoding="utf-8"))
    assert len(calls) == EXPECTED[rel], f"{rel}: {len(calls)} mermaid.initialize calls, expected {EXPECTED[rel]}"
    for args in calls:
        assert LEVEL.findall(args) == ["strict"], f"{rel}: mermaid.initialize without securityLevel 'strict': {args.strip()[:120]}"


def test_no_other_initialize_sites_and_no_weaker_level():
    unexpected, weaker = [], []
    for p in _served_sources():
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8", errors="replace")
        if _init_calls(text) and rel not in EXPECTED:
            unexpected.append(rel)
        weaker += [f"{rel}: {lvl}" for lvl in LEVEL.findall(text) if lvl != "strict"]
    assert not unexpected, f"mermaid.initialize in files not pinned in EXPECTED: {unexpected}"
    assert not weaker, f"securityLevel other than 'strict': {weaker}"


def test_shared_ui_copies_identical():
    # SHARE-3 keeps the two copies identical; this guard relies on both being strict.
    a = (ROOT / Q / "PyegeriaWebHandler/static/egeria-shared-ui.js").read_bytes()
    b = (ROOT / F / "PyegeriaWebHandler/static/egeria-shared-ui.js").read_bytes()
    assert a == b
