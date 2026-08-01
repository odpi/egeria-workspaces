"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared fixtures for PyegeriaWebHandler tests.

These tests exercise real handler code against the LIVE Egeria platform this
container is wired to (EGERIA_PLATFORM_URL, default https://host.docker.internal:9443
inside the quickstart container — see compose-configs/egeria-quickstart/
egeria-quickstart.yaml). There is no mocking of the Egeria side: handlers call
`_get_manager()` with no explicit credentials, which falls back to the
erinoverview/secret demo persona baked into every handler's defaults. That
means these tests must run where that hostname resolves, i.e. inside the
`quickstart-pyegeria-web` container (or an environment with equivalent
EGERIA_* env vars) — not from a bare host shell.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_THIS_DIR = Path(__file__).resolve().parent
_MODULE_DIR = _THIS_DIR.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import pyegeria_handler as handler  # type: ignore  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(handler.app)
