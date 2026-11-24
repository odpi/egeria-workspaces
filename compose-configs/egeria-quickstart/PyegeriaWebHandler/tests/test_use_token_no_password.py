"""use_token opts a client out of pyegeria's configured default password (NO_PASSWORD opt-out).

A token-switched client acts only as the token's user. With a demo default password configured
(settings.User_Profile.user_pwd), a sub-client it built before or after the switch must not hold that password,
or pyegeria's one 401 auto-retry could sign in again as the configured (demo) user.
Skipped on a pyegeria without the opt-out (pyegeria.core._no_password).
"""
import base64
import json
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from egeria_auth import use_token  # noqa: E402


def _jwt(sub):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + 3600})}.sig"


@pytest.fixture
def tech(monkeypatch):
    try:
        import pyegeria.core._no_password  # noqa: F401
    except ImportError:
        pytest.skip("pyegeria without the NO_PASSWORD opt-out")
    from pyegeria.core.config import settings
    from pyegeria import EgeriaTech
    from pyegeria.core import _base_server_client as bsc
    monkeypatch.setattr(settings.User_Profile, "user_pwd", "demo-default-secret")
    # Some sub-clients check the platform when built; nothing here talks to Egeria.
    from pyegeria.core import _base_platform_client as bpc
    for cls in (bsc.BaseServerClient, getattr(bpc, "BasePlatformClient", None)):
        if cls is not None:
            monkeypatch.setattr(cls, "check_connection", lambda self, *a, **k: True, raising=False)
    client = EgeriaTech("qs-view-server", "https://localhost:9443", user_id="erinoverview")
    assert client.user_pwd == "demo-default-secret"           # the default filled it, as in the Portal
    return client


def test_no_sub_client_holds_a_password_after_use_token(tech):
    names = list(tech._subclient_map)
    before = tech._get_subclient(names[0])                     # built before the switch
    assert before.user_pwd == "demo-default-secret"
    use_token(tech, _jwt("peterprofile"))
    assert tech.user_id == "peterprofile" and not tech.user_pwd and tech.use_default_password is False
    for name in names:                                         # the rest are built lazily, after it
        sub = tech._get_subclient(name)
        assert not sub.user_pwd, f"sub-client {name} holds a password after use_token"
        assert getattr(sub, "use_default_password", False) is False, name


def test_use_token_works_on_a_client_without_the_attribute():
    class Bare:
        __slots__ = ("user_id", "user_pwd", "token")

        def set_bearer_token(self, token):
            self.token = token
    c = Bare()
    c.user_id, c.user_pwd = "erinoverview", "secret"
    use_token(c, _jwt("peterprofile"))
    assert c.user_id == "peterprofile" and c.user_pwd is None
