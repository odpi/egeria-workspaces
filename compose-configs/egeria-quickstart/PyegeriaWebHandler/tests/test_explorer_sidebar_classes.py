"""Egeria Explorer: classes and CSS variables the views use must be defined in type-explorer.html's
stylesheet. .btn-sm (~35 Refresh/Sync buttons), .search-box and .sidebar-item (Context Events) and
--text-dim were used but never defined, so those controls rendered as unstyled native widgets."""
import re
from pathlib import Path

HTML = (Path(__file__).resolve().parent.parent / "type-explorer.html").read_text()
STYLE = HTML[HTML.index("<style>"):HTML.index("</style>")]


def _rule(selector):
    return re.search(r"(^|[\s,}])" + re.escape(selector) + r"\s*[,{:]", STYLE, re.M) is not None


def test_classes_used_by_views_are_defined():
    for cls in ("btn-sm", "search-box", "sidebar-item"):
        assert re.search(r"className:\s*['\"][^'\"]*\b" + cls + r"\b", HTML), cls + " is no longer used"
        assert _rule("." + cls), "." + cls + " is used but not defined in the stylesheet"
    assert _rule(".sidebar-item.selected")


def test_classes_have_light_theme_overrides():
    for sel in (":root.light .search-box", ":root.light .btn-sm", ":root.light .sidebar-item.selected"):
        assert sel in STYLE, sel


def test_text_dim_variable_is_defined():
    assert "var(--text-dim)" in HTML
    assert re.search(r"--text-dim\s*:", STYLE)
