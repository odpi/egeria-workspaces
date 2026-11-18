# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""resource-browser.html defines each top-level function once. A scripted edit once spliced a
region of the page in twice (about 1,090 lines, 2026-11-17); the later copy silently wins in the
browser, so node --check passes while the page runs stale code. This catches that."""
import re
from pathlib import Path

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text(encoding="utf-8")


def test_no_top_level_function_is_defined_twice():
    names = re.findall(r"^function (\w+)\(", _PAGE, re.M)
    assert names, "no functions found"
    assert sorted({n for n in names if names.count(n) > 1}) == []


def test_no_top_level_var_is_declared_twice():
    names = re.findall(r"^var ([A-Z_][A-Z0-9_]*) = ", _PAGE, re.M)
    assert sorted({n for n in names if names.count(n) > 1}) == []
