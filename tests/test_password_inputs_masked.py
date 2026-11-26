"""Source guard: every password field on a served page is a masked input (type="password").

Covers the Portal (quickstart and freshstart PyegeriaWebHandler: pages and static JS), the Apache pages
under compose-configs/egeria-quickstart, the Portal Docs viewer and the exchange pages. An input counts as
a password field when it is bound to a password value (its React props or HTML attributes mention a
password, pwd or secret). The one allowed exception is demo-admin.html's show/hide toggle, which an
administrator presses to read back a temporary password they are typing.

The Connection Settings panels (type-explorer.html and tech-catalog.html, both trees) are pinned as well:
type 'password' and autoComplete 'current-password'.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SERVED = (
    "compose-configs/egeria-quickstart/PyegeriaWebHandler",
    "compose-configs/egeria-freshstart/PyegeriaWebHandler",
    "portal-docs",
    "exchange-quickstart",
    "exchange-freshstart",
)
SERVED_TOP = ("compose-configs/egeria-quickstart",)          # its own *.html only (markdown viewer etc.)
SKIP_PARTS = {"node_modules", "tests", ".venv", "__pycache__"}
PASSWORDISH = re.compile(r"(?i)passw|pwd|secret")
REACT_INPUT = re.compile(r"createElement\(\s*['\"]input['\"]\s*,\s*\{")
HTML_INPUT = re.compile(r"<input\b[^>]*>", re.I)
MASKED_PROP = re.compile(r"type:\s*['\"]password['\"]")
MASKED_ATTR = re.compile(r"type\s*=\s*['\"]?password['\"]?", re.I)

CONNECTION_FORMS = [f"compose-configs/{tree}/PyegeriaWebHandler/{page}"
                    for tree in ("egeria-quickstart", "egeria-freshstart")
                    for page in ("type-explorer.html", "tech-catalog.html")]


def _sources():
    for d in SERVED:
        for p in (ROOT / d).rglob("*"):
            if p.is_file() and p.suffix in (".html", ".js") and not SKIP_PARTS.intersection(p.relative_to(ROOT).parts):
                yield p
    for d in SERVED_TOP:
        yield from (p for p in (ROOT / d).glob("*.html") if p.is_file())


def _react_props(text: str, start: int) -> str:
    """The props object of a createElement('input', {...}) call, braces balanced."""
    depth, i = 1, start
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[start:i - 1]


def test_sources_found():
    files = list(_sources())
    assert len(files) > 20, f"only {len(files)} served files found; the guard would check too little"


def test_every_password_input_is_masked():
    unmasked = []
    for p in _sources():
        text = p.read_text(encoding="utf-8", errors="replace")
        rel = p.relative_to(ROOT).as_posix()
        for m in REACT_INPUT.finditer(text):
            props = _react_props(text, m.end())
            if PASSWORDISH.search(props) and not MASKED_PROP.search(props):
                unmasked.append(f"{rel}:{text[:m.start()].count(chr(10)) + 1}")
        for m in HTML_INPUT.finditer(text):
            tag = m.group(0)
            if PASSWORDISH.search(tag) and not MASKED_ATTR.search(tag):
                unmasked.append(f"{rel}:{text[:m.start()].count(chr(10)) + 1}")
    assert not unmasked, f"password inputs that are not type=password: {unmasked}"


@pytest.mark.parametrize("rel", CONNECTION_FORMS)
def test_connection_settings_password_is_masked(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    hits = [_react_props(text, m.end()) for m in REACT_INPUT.finditer(text)]
    pw = [h for h in hits if "form.password" in h]
    assert len(pw) == 1, f"{rel}: expected one Connection Settings password input, found {len(pw)}"
    assert MASKED_PROP.search(pw[0]), f"{rel}: the Connection Settings password input is not type 'password'"
    assert re.search(r"autoComplete:\s*['\"]current-password['\"]", pw[0]), \
        f"{rel}: the Connection Settings password input lacks autoComplete 'current-password'"


def test_only_known_type_toggle():
    """A script that switches an input between 'password' and 'text' exists only in demo-admin.html."""
    toggles = []
    for p in _sources():
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"['\"]password['\"]\s*\?\s*['\"]text['\"]\s*:\s*['\"]password['\"]", text):
            toggles.append(p.relative_to(ROOT).as_posix())
    assert set(toggles) <= {"compose-configs/egeria-freshstart/PyegeriaWebHandler/demo-admin.html"}, toggles
