# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Catalog's Data scope section asks before a Save with every field emptied, because
that clears a stored scope (Architect R1, 2026-11-17). Cancel sends nothing; OK sends the PUT.

DataScopeSection is pulled out of tech-catalog.html and run under node with stub hooks;
skipped when node is not installed (the Portal container has none)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_TC = (Path(__file__).resolve().parent.parent / "tech-catalog.html").read_text()

_HARNESS = r"""
var states = __STATES__, si = 0, editorProps = null, sent = [], asked = [];
function DataScopeEditor() {} function DataScopeView() {}
var React = {
  createElement: function(type, props) { if (type === DataScopeEditor) editorProps = props; return null; },
  useState: function() { var v = states[si++]; return [v, function() {}]; },
};
function useState(x) { return React.useState(x); }
function useEffect() {}
function dataScopeFetchDimensions() { return { then: function() { return { catch: function() {} }; } }; }
function egeriaFetch(url, creds, opts) {
  sent.push(opts && opts.method);
  return { then: function() { return this; }, catch: function() { return this; }, finally: function() { return this; } };
}
var window = { confirm: function(q) { asked.push(q); return window._answer; } };
__FN__
function run(values, answer) {
  si = 0; sent = []; asked = []; window._answer = answer;
  DataScopeSection({ guid: 'g1', creds: { token: 't' } });
  editorProps.onSave(values);
  return { asked: asked.length, sent: sent.slice() };
}
console.log(JSON.stringify([
  run({ minLatitude: '', maxLatitude: '', scopeElements: {} }, false),
  run({ minLatitude: '', maxLatitude: '', scopeElements: {} }, true),
  run({ minLatitude: '50', maxLatitude: '' }, false),
]));
"""


def _section_source() -> str:
    start = _TC.index("function DataScopeSection(")
    end = _TC.index("\n// ── Generic detail panel", start)
    return _TC[start:end]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_save_with_every_field_empty_asks_before_clearing():
    groups = [{"id": "Latitude", "shape": "bound", "fields": []}]
    data = {"scope": {"minLatitude": 50, "maxLatitude": 51}, "summary": {"usageOnly": False}}
    states = [groups, data, "", True, False, ""]   # groups, data, err, editing, busy, writeErr
    js = _HARNESS.replace("__STATES__", json.dumps(states)).replace("__FN__", _section_source())
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    cancelled, confirmed, partial = json.loads(out.stdout.strip().splitlines()[-1])
    assert cancelled == {"asked": 1, "sent": []}
    assert confirmed == {"asked": 1, "sent": ["PUT"]}
    assert partial == {"asked": 0, "sent": ["PUT"]}      # a value still set: an ordinary save, no question
