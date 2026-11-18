# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""static/data-scope-editor.js: the editor resets its form only when the stored scope or
the dimensions really change, not on every re-render.

The Catalog and the Locator pass groups.filter(...), a new array on every render. When the
reset effect depended on that array, pressing Save (which re-renders the page) put the
stored values back into the form, so the owner could not empty the fields (2026-11-17).

Run under node with a stub React that records each effect's dependencies; skipped when node
is not installed (the Portal container has none)."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_JS = (Path(__file__).resolve().parent.parent / "static" / "data-scope-editor.js").read_text()

_HARNESS = r"""
var deps = [];
var React = {
  createElement: function() { return null; }, Fragment: 'F',
  useState: function(init) { return [typeof init === 'function' ? init() : init, function() {}]; },
  useEffect: function(fn, d) { deps.push(d); },
};
var window = {};
function egeriaFetch() { throw new Error('no fetch in this test'); }
__JS__
var groups = [{ id: 'Latitude', shape: 'bound', fields: [{ name: 'minLatitude', kind: 'number', role: 'min' }, { name: 'maxLatitude', kind: 'number', role: 'max' }] },
              { id: 'additionalProperties', shape: 'map', readOnly: true, fields: [{ name: 'additionalProperties', kind: 'map', role: 'value' }] }];
var scope = { minLatitude: 50, maxLatitude: 51 };
function render(s) { window.DataScopeEditor({ groups: groups.filter(function(g) { return !g.readOnly; }), scope: s, onSave: function() {} }); }
// React re-runs an effect when any dependency differs by Object.is from the last render.
function reruns(a, b) { return a.length !== b.length || a.some(function(x, i) { return !Object.is(x, b[i]); }); }
render(scope); render(scope);                       // a re-render with a fresh, equal groups array
render({ minLatitude: 1, maxLatitude: 2 });         // the stored scope changed
console.log(JSON.stringify([reruns(deps[0], deps[1]), reruns(deps[1], deps[2])]));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_editor_resets_only_when_scope_or_dimensions_change():
    out = subprocess.run(["node", "-e", _HARNESS.replace("__JS__", _JS)], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    rerender_resets, change_resets = json.loads(out.stdout.strip().splitlines()[-1])
    assert rerender_resets is False, "a re-render with an equal groups array must not reset the form"
    assert change_resets is True, "a changed stored scope must reset the form"
