"""The Dashboard Sheet page's report-spec registry is cached per spec identity (PO-7).

pyegeria's get_report_registry() holds the EGERIA tier of the CURRENT spec identity: the request's token
user (EgeriaTokenMiddleware runs each request inside spec_identity(<token user>), 4a6a9fd1), no one without a
token. local_dashboards_handler cached it under one process-wide key for a minute, so the first caller's
registry was served to everyone: another user's private specs to a user, or a registry built for no one (no
private specs) to the user who owns them. These tests drive pyegeria's own spec_identity and assert which
registry each caller gets back."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

esc = pytest.importorskip("pyegeria.view.egeria_spec_cache")
if not hasattr(esc, "spec_identity") or not hasattr(esc, "current_spec_identity"):
    pytest.skip("this pyegeria has no spec identities", allow_module_level=True)

import local_dashboards_handler as ldh  # noqa: E402

ERIN = "erinoverview@https://egeria.test:9443/qs-view-server"
PETER = "peterprofile@https://egeria.test:9443/qs-view-server"


@pytest.fixture
def registry(monkeypatch):
    """get_report_registry() answers with the identity it was read for, as pyegeria's tiers do."""
    import pyegeria.view.base_report_formats as brf
    calls = []

    def fake():
        who = esc.current_spec_identity()
        calls.append(who)
        return {"Public Spec": "public", **({f"Private of {who}": "private"} if who else {})}

    monkeypatch.setattr(brf, "get_report_registry", fake)
    monkeypatch.setattr(ldh, "_cache", {})
    return calls


def test_each_identity_gets_its_own_registry(registry):
    with esc.spec_identity(ERIN):
        erin = ldh._report_registry()
    with esc.spec_identity(PETER):
        peter = ldh._report_registry()
    with esc.spec_identity(None):
        nobody = ldh._report_registry()
    assert f"Private of {ERIN}" in erin and f"Private of {ERIN}" not in peter
    assert f"Private of {PETER}" in peter
    assert set(nobody) == {"Public Spec"}
    assert registry == [ERIN, PETER, None]


def test_a_cached_registry_is_reused_only_by_its_own_identity(registry):
    with esc.spec_identity(ERIN):
        ldh._report_registry()
        ldh._report_registry()
    assert registry == [ERIN]           # cached for Erin
    with esc.spec_identity(PETER):
        assert f"Private of {ERIN}" not in ldh._report_registry()
    assert registry == [ERIN, PETER]    # Peter's own read, not Erin's cache


def test_the_key_names_the_identity():
    with esc.spec_identity(ERIN):
        k1 = ldh._registry_key()
    with esc.spec_identity(PETER):
        k2 = ldh._registry_key()
    with esc.spec_identity(None):
        k3 = ldh._registry_key()
    assert len({k1, k2, k3}) == 3 and all(k.startswith("registry|") for k in (k1, k2, k3))
