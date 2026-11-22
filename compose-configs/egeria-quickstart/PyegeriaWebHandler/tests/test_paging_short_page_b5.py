"""Paging honesty (Egeria's paging contract + bug B5).

* A SHORT page is not the last page: Egeria filters each page after reading it, so Insights'
  exhaustive searches page until an empty or null page, with a cap, and say "may be more" at the cap.
* A find with pageSize 1 can answer "No elements found" when a match exists (B5, 8840035f), so
  existence/oldest lookups ask for 25 -- in freshstart as quickstart already does.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import insights_handler as ih  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
FRESH = HERE.parent.parent / "egeria-freshstart" / "PyegeriaWebHandler"


def _els(*guids):
    return [{"elementGUID": g} for g in guids]


def _fetcher(pages):
    """pages: startFrom -> page (a list, None, or pyegeria's 'No elements found' string)."""
    calls = []

    def fetch(start):
        calls.append(start)
        return pages.get(start)
    return fetch, calls


def test_a_short_page_is_not_the_last_page():
    fetch, calls = _fetcher({0: _els("a", "b"), 3: _els("c"), 6: _els("d", "e", "f"), 9: None})
    out = []
    assert ih._page_all(fetch, 3, 100, set(), out) is False
    assert [e["elementGUID"] for e in out] == ["a", "b", "c", "d", "e", "f"]
    assert calls == [0, 3, 6, 9]


def test_an_empty_list_or_the_no_elements_string_ends_it():
    for end in ([], "No elements found", None):
        fetch, calls = _fetcher({0: _els("a"), 3: end})
        out = []
        assert ih._page_all(fetch, 3, 100, set(), out) is False and len(out) == 1 and calls == [0, 3]


def test_the_cap_stops_it_and_says_may_be_more():
    pages = {i * 2: _els(f"g{i}a", f"g{i}b") for i in range(50)}
    fetch, calls = _fetcher(pages)
    out = []
    assert ih._page_all(fetch, 2, 5, set(), out) is True
    assert len(out) == 5 and len(calls) == 3


def test_a_repeating_page_stops_and_says_may_be_more():
    fetch, calls = _fetcher({0: _els("a", "b"), 2: _els("a", "b"), 4: _els("c")})
    out = []
    assert ih._page_all(fetch, 2, 100, set(), out) is True and len(out) == 2 and calls == [0, 2]


def test_guids_already_seen_by_another_type_are_not_counted_twice():
    seen, out = set(), []
    f1, _ = _fetcher({0: _els("a", "b"), 2: None})
    f2, _ = _fetcher({0: _els("b", "c"), 2: None})
    assert ih._page_all(f1, 2, 100, seen, out) is False
    assert ih._page_all(f2, 2, 100, seen, out) is False
    assert [e["elementGUID"] for e in out] == ["a", "b", "c"]


def test_no_insights_loop_stops_on_a_short_page_any_more():
    src = (HERE / "insights_handler.py").read_text()
    assert not re.search(r"^\s*if .*len\(page\) < page_size", src, re.M)
    assert len(re.findall(r"_page_all\(_fetch, page_size, _FULL_COUNT_HARD_CAP", src)) == 2


def test_the_ui_says_may_be_more_when_truncated():
    html = (HERE / "egeria-insights.html").read_text()
    assert "truncated at 10,000" not in html and html.count("there may be more") == 2


def test_a_complete_run_is_not_called_exact():
    """Both loops use metadata-expert finds, where a filtered page can come back null (B5 capture) and
    pyegeria collapses [] with null, so a stop on an empty page is not proof of the end."""
    html = (HERE / "egeria-insights.html").read_text()
    assert "matching elements (exact" not in html
    assert "'matching elements (counted until Egeria reported no more)'" in html


def test_freshstart_lookups_ask_for_25_not_1():
    for name, const in (("bootstrap_monitor_handler.py", "_CANARY_PAGE_SIZE"),
                        ("catalog_search_handler.py", "_OLDEST_PAGE_SIZE")):
        src = (FRESH / name).read_text()
        assert re.search(rf"^{const} = 25$", src, re.M), name
        assert not re.search(r'"pageSize":\s*1\b', src), name
        assert f'"pageSize": {const}' in src, name


def test_a_canary_miss_reads_not_found_in_the_first_25():
    for root in (HERE, FRESH):
        src = (root / "bootstrap_monitor_handler.py").read_text()
        assert "(canary missing)" not in src
        assert "(canary not found in the first {_CANARY_PAGE_SIZE})" in src
