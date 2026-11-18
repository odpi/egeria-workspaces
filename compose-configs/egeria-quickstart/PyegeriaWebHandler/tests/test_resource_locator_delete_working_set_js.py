# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-43: what the delete confirm card and its outcome say (resource-browser.html, under node).

  - the question names the set and says its N resources stay;
  - shares and the owner's lenses are named as going;
  - any blocker disables Delete and is listed;
  - a 207 says what was removed, what failed and what is left, and to delete again.
Skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    end = _PAGE.index("\n}\n", start) + 3 if "\n" in _PAGE[start:_PAGE.index("}", start) + 1] else _PAGE.index("}", start) + 1
    return _PAGE[start:end]


def _run(body: str):
    js = "\n".join(_fn(n) for n in ("plural", "deleteConfirmText", "deleteOutcomeText")) + "\n" + body
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


@needs_node
def test_confirm_names_the_set_the_shares_and_the_lenses():
    d = _run(r"""console.log(JSON.stringify(deleteConfirmText({ displayName: 'Q3 sources', members: 3,
      shares: [{ displayName: 'Team A' }, { displayName: 'Team B' }], lenses: [{ displayName: 'UK' }], blockers: [], canDelete: true })));""")
    assert d["question"] == "Delete working set ‘Q3 sources’? Its 3 resources stay; only the set and its links are removed."
    assert d["lines"] == ["It stops being shared with Team A, Team B.", "Data lens ‘UK’ stops governing it."]
    assert d["canDelete"] is True and d["blockers"] == []


@needs_node
def test_one_resource_and_blockers_disable_delete():
    d = _run(r"""console.log(JSON.stringify(deleteConfirmText({ displayName: 'X', members: 1, shares: [], lenses: [],
      blockers: [{ text: 'A AttachedTag link to ‘hot’' }], canDelete: false })));""")
    assert "Its 1 resource stays;" in d["question"]
    assert d["canDelete"] is False and d["blockers"] == ["A AttachedTag link to ‘hot’"]


@needs_node
def test_outcomes():
    d = _run(r"""console.log(JSON.stringify([
      deleteOutcomeText({ deleted: true, displayName: 'Q3', membersKept: 10 }),
      deleteOutcomeText({ deleted: false, displayName: 'Q3', removed: { members: 3, shares: [{ displayName: 'Team A' }], lenses: [] },
        left: { members: 7, shares: [], lenses: [] }, failed: { step: 'unlink', displayName: 'patient_id', message: 'not authorised' } }),
      deleteOutcomeText({ deleted: false, removed: { members: 10, shares: [], lenses: [] }, left: { members: 0, shares: [], lenses: [] },
        failed: { step: 'delete', message: 'Every link was removed, but Egeria refused to delete the working set (busy). It is empty now: delete again.' } })
    ]));""")
    assert d[0] == "Deleted ‘Q3’. Its 10 resources are unchanged."
    assert d[1] == ("The working set was not deleted: 3 resources taken out of it, no longer shared with Team A, then "
                    "taking ‘patient_id’ out of it failed (not authorised). It still holds 7 resources. "
                    "Delete again to carry on.")
    assert d[2].startswith("The working set was not deleted: 10 resources taken out of it.")
    assert "It is empty now: delete again." in d[2]
