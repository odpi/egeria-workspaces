"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

SolutionActorRole navigation: the type-nav-map entry and the in-app dispatcher. A SolutionActorRole is an ActorRole by
supertype, but it is the DESIGN-time role of a solution: the most specific type wins, so it never lands on the Actors card.
Standalone (no app imports); run with node, skipped when node is missing (the Portal container has none).
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_HANDLER_DIR = Path(__file__).resolve().parent.parent


def _resolve(type_name, supers):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var window = global; global.fetch = function() { return Promise.resolve({ ok: true, json: function() { return "
          + json.dumps(json.loads((_HANDLER_DIR / "static" / "type-nav-map.json").read_text())) + "; } }); };"
          + (_HANDLER_DIR / "static" / "type-nav-resolve.js").read_text()
          + "loadTypeNavMap().then(function() { console.log(JSON.stringify(resolveTypeNav("
          + json.dumps(type_name) + "," + json.dumps(supers) + "))); });")
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


_ROLE_SUPERS = ["ActorRole", "Actor", "Referenceable", "OpenMetadataRoot"]   # as returned for a SolutionActorRole


def test_a_solution_actor_role_lands_on_the_solution_architect_roles_tab_not_actors():
    nav = _resolve("SolutionActorRole", _ROLE_SUPERS)
    assert nav["explorerHash"] == "solution-architect" and nav["kind"] == "roles"


def test_an_actor_role_still_lands_on_actors():
    # the Actors card keeps ActorRole; PersonRole (an ActorRole too) resolves through its supertype
    assert _resolve("ActorRole", ["Actor"])["explorerHash"] == "actors"
    nav = _resolve("PersonRole", ["ActorRole", "Actor", "Referenceable"])
    assert nav["explorerHash"] == "actors" and nav["kind"] == "roles"


def test_in_app_dispatcher_routes_solution_actor_role_before_the_actor_fallback():
    # onNavigateToElement is one if-chain; the SolutionActorRole branch must come before `_actorKindForType`, which maps any
    # ActorRole supertype to the Actors card.
    html = (_HANDLER_DIR / "type-explorer.html").read_text()
    start = html.index("const onNavigateToElement = useCallback(function(item) {")
    chain = html[start:start + 12000]
    assert chain.index("typeName === 'SolutionActorRole'") < chain.index("_actorKindForType(typeName, superTypes)")
    assert "kind: 'roles'" in html[html.index("const onNavigateToSolutionRole"):][:300]
