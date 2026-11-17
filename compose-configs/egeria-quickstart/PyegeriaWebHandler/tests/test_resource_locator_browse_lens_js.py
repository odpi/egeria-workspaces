# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Browse lens filter, page logic: the Lens choice offers your own lenses
and those governing a list you can see; the outcome toggles filter the rows shown, and
"cannot be compared" rows stay selectable (never silently dropped).
Runs lensChoices and lensRows from resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    end = _PAGE.index("\n}\n", start) + 2
    return _PAGE[start:end]


_HARNESS = r"""
__FNS__
var lenses = [
  { guid: 'mine', origin: 'mine', governs: [] },
  { guid: 'governsShared', origin: 'portal', governs: [{ guid: 'shared-list' }] },
  { guid: 'governsMine', origin: 'portal', governs: [{ guid: 'my-list' }] },
  { guid: 'someoneElses', origin: 'portal', governs: [{ guid: 'private-list' }] },
];
var lists = { mine: [{ guid: 'my-list' }], sharedWithMe: [{ guid: 'shared-list' }] };
var items = [{ guid: 'a', lensOutcome: { outcome: 'inside' } }, { guid: 'b', lensOutcome: { outcome: 'outside' } },
             { guid: 'c', lensOutcome: { outcome: 'notComparable' } }, { guid: 'd' }];
console.log(JSON.stringify({
  choices: lensChoices(lenses, lists).map(function(l) { return l.guid; }),
  noLists: lensChoices(lenses, null).map(function(l) { return l.guid; }),
  insideOnly: lensRows(items, { inside: true }).map(function(r) { return r.guid; }),
  withNotComparable: lensRows(items, { inside: true, notComparable: true }).map(function(r) { return r.guid; }),
}));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_lens_choices_and_outcome_filter():
    js = _HARNESS.replace("__FNS__", _fn("lensChoices") + "\n" + _fn("lensRows"))
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["choices"] == ["mine", "governsShared", "governsMine"]
    assert d["noLists"] == ["mine"]
    assert d["insideOnly"] == ["a", "d"]                 # a row with no outcome (no lens) is never hidden
    assert d["withNotComparable"] == ["a", "c", "d"]
