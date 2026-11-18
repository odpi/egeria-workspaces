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
