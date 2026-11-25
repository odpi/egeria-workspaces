"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The SolutionActorRole card in type-explorer.html (SolutionRoleCard, between solution-role-pure:begin and :end), run under node
with test_e64_cards_js's stub React. Standalone (no app imports); skipped when node is not installed (the Portal container
has none). Rows are shaped like solution_architect_handler._serialize_role_detail's output, which test_solution_roles.py pins
against the recorded real shape.

First draft of SolutionRoleCard: qwen3-coder-next via opencode (build-local); it missed the 'live' badge on "Who holds it",
which test_holders_list_is_marked_live now pins.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_e64_cards_js import _PRELUDE  # noqa: E402

_HTML = (Path(__file__).resolve().parent.parent / "type-explorer.html").read_text()


def _block():
    m = re.search(r"/\* solution-role-pure:begin \*/(.*?)/\* solution-role-pure:end \*/", _HTML, re.S)
    assert m, "the solution-role-pure block is missing from type-explorer.html"
    return m.group(1)


def _render(role, handlers=True):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    hs = ", onNavigateToBlueprint: function(){}, onNavigateToComponent: function(){}, onNavigateToElement: function(){}" if handlers else ""
    body = (f"var t = render(React.createElement(SolutionRoleCard, {{ role: {json.dumps(role)}{hs} }}));"
            "out({ text: text(t), "
            "fields: all(t, 'div').filter(function(n) { return n.p && n.p['data-field']; }).map(function(n) { return n.p['data-field']; }), "
            "sections: all(t, 'div').filter(function(n) { return n.p && n.p['data-test']; }).map(function(n) { return n.p['data-test']; }), "
            "buttons: all(t, 'button').length, "
            "badges: all(t, 'span').filter(function(n) { return n.p && n.p.className === 'badge'; }).map(text) });")
    r = subprocess.run([node, "-e", _PRELUDE + _block() + "\n" + body], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def _item(guid, name, type_name):
    return {"guid": guid, "displayName": name, "qualifiedName": "q::" + name, "typeName": type_name}


FULL = {
    "guid": "r-1", "displayName": "Product Subscriber", "qualifiedName": "Role::Product Subscriber", "description": "Subscribes to a product.",
    "identifier": "ProductSubscriber", "title": "", "scope": "Within Solution", "actorRoleGroups": ["community-member"], "status": "ACTIVE",
    "typeName": "SolutionActorRole",
    "blueprints": [_item("b1", "Blueprint One", "SolutionBlueprint"), _item("b2", "Blueprint Two", "SolutionBlueprint")],
    "components": [_item("c1", "Comp 1", "SolutionComponent"), _item("c2", "Comp 2", "SolutionComponent"), _item("c3", "Comp 3", "SolutionComponent")],
    "memberOf": [_item("f1", "A Folio", "Folio")],
    "holders": [_item("h1", "Erin Overview", "Person")],
}
EMPTY = {"guid": "r-2", "displayName": "Runtime Manager", "qualifiedName": "Role::Runtime Manager", "typeName": "SolutionActorRole",
         "blueprints": [], "components": [], "memberOf": [], "holders": []}


def test_only_the_fields_the_type_returns_are_shown():
    r = _render(FULL)
    assert r["fields"] == ["qualified-name", "identifier", "scope", "role-groups", "status"]     # no title: it is empty
    assert "Within Solution" in r["text"] and "community-member" in r["text"] and "Subscribes to a product." in r["text"]


def test_a_title_is_shown_only_when_the_platform_returned_one():
    r = _render(dict(FULL, title="Chief Architect"))
    assert "title" in r["fields"] and "Chief Architect" in r["text"]


def test_a_bare_role_shows_no_placeholder_for_missing_fields():
    r = _render(EMPTY)
    assert r["fields"] == ["qualified-name"]
    assert "undefined" not in r["text"] and "null" not in r["text"]
    assert "role-description" not in r["sections"]


def test_empty_states_say_what_is_missing_in_words():
    r = _render(EMPTY)
    for words in ("Not used in any blueprint", "No solution component uses this role",
                  "Not a member of any other collection", "Nobody is assigned to this role right now"):
        assert words in r["text"]
    for title in ("Used in blueprints (0)", "Used by components (0)", "Also a member of (0)", "Who holds it (0)"):
        assert title in r["text"]


def test_links_to_blueprints_components_and_other_collections_with_counts():
    r = _render(FULL)
    for words in ("Blueprint One", "Blueprint Two", "Comp 3", "A Folio", "Erin Overview",
                  "Used in blueprints (2)", "Used by components (3)", "Also a member of (1)", "Who holds it (1)"):
        assert words in r["text"]
    assert r["buttons"] == 7                       # one View per linked item: 2 + 3 + 1 + 1


def test_without_handlers_nothing_pretends_to_be_a_link():
    assert _render(FULL, handlers=False)["buttons"] == 0


def test_holders_list_is_marked_live():
    r = _render(FULL)
    assert "live" in r["badges"]
    assert r["badges"].count("live") == 1          # only the holders list, not the design-time ones


def test_section_order():
    assert _render(FULL)["sections"] == ["role-header", "role-fields", "role-description", "used-in-blueprints", "used-by-components",
                                         "also-a-member-of", "who-holds-it"]


def test_no_role_renders_nothing():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    r = subprocess.run([node, "-e", _PRELUDE + _block() + "\nout({ t: text(render(React.createElement(SolutionRoleCard, { role: null }))) });"],
                       capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["t"] == ""
