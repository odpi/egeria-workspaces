"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared fixtures for the browser/E2E test tier. Runs from the HOST against
the already-running quickstart-pyegeria-web container (see requirements.txt
for why this doesn't run inside the container like tests/ does).
"""

import os
import sys
from pathlib import Path

import pytest

_THIS_DIR = Path(__file__).resolve().parent
_TESTS_DIR = _THIS_DIR.parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

# golden_anchors.py lives one level up (shared with the container-side suite;
# it's pure data, no pyegeria/handler imports, so it's safe to import from a
# completely different Python environment).
import golden_anchors  # noqa: E402  (re-exported for test modules to import)

BASE_URL = os.environ.get("PORTAL_BASE_URL", "http://localhost:8800")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Overrides pytest-playwright's default base_url fixture."""
    return BASE_URL
