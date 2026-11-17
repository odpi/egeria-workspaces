# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-42 (Dan, 2026-11-17): the Locator calls Egeria's WorkingSet a "working set", not a "work list".

Sentence case, like "Data lens" (Architect read-back Q1). The API routes (/lists/…) and JSON keys
(listGuid, lists) keep their names for compatibility; only what a person reads changes."""
import re
from pathlib import Path

_DIR = Path(__file__).resolve().parent.parent
_PAGE = (_DIR / "resource-browser.html").read_text()
_HANDLER = (_DIR / "resource_browser_handler.py").read_text()
_LENS = (_DIR / "resource_locator_lens_handler.py").read_text()
_DOCS = (_DIR.parent.parent.parent / "portal-docs" / "tools" / "resource-locator.md")


def test_no_work_list_left_in_the_locator_page_or_handlers():
    for name, text in (("resource-browser.html", _PAGE), ("resource_browser_handler.py", _HANDLER),
                       ("resource_locator_lens_handler.py", _LENS)):
        hits = [line.strip()[:120] for line in text.splitlines() if re.search(r"\bwork[ -]lists?\b", line, re.I)
                and "PO-42: called a work list" not in line]
        assert hits == [], (name, hits)


def test_the_docs_say_working_set_and_name_the_old_term_once():
    if not _DOCS.exists():
        return
    lines = [l for l in _DOCS.read_text().splitlines() if re.search(r"\bwork[ -]lists?\b", l, re.I)]
    assert len(lines) == 1 and "until November 2026" in lines[0]
    assert "## Working sets" in _DOCS.read_text()


def test_the_main_labels():
    for text in ("'My working sets'", "'＋ Add to working set'", "'Add to working set\\u2026'",
                 "'New working set\\u2026'", "' to working set\\u2026'", "'Working sets it governs'",
                 "label: 'Working set'", "'Your working sets'"):
        assert text in _PAGE, text


def test_api_routes_and_keys_keep_their_names():
    assert '"/api/resource-browser/lists"' in _HANDLER
    assert "API + '/lists/'" in _PAGE and "listGuid" in _PAGE
    assert "p.get('list')" in _PAGE                          # ?list= links keep working
