"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared fixtures for the freshstart PyegeriaWebHandler tests.
"""
import pytest


@pytest.fixture(autouse=True)
def _configured_service_password(monkeypatch):
    """PO-45: the Portal has no built-in service password any more (egeria_auth.service_password refuses
    when EGERIA_USER_PASSWORD is unset). A test session models a CONFIGURED deployment, so it
    is set here when the environment does not set it (the gate's "nouser" run unsets it). The value is the
    Coco demo persona password: the live tests below sign in to this container's Egeria as that persona,
    exactly as the handlers' old built-in default did. Tests of the unset case delete it themselves."""
    import os
    if not os.environ.get("EGERIA_USER_PASSWORD"):
        monkeypatch.setenv("EGERIA_USER_PASSWORD", "secret")


@pytest.fixture(autouse=True)
def _fresh_rate_limits():
    """PO-83: the auth routes are rate-limited per client IP, and every TestClient calls from the same address
    ("testclient"), so no test may inherit another test's count."""
    import sys
    from pathlib import Path
    here = str(Path(__file__).resolve().parents[1])
    if here not in sys.path:
        sys.path.insert(0, here)
    from rate_limiter import limiter
    limiter.reset()
    yield
