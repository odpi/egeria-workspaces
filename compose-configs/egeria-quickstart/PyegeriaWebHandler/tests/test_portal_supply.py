"""PortalSupply (RS-W2-3): the Portal's RoleSupply. No Egeria needed: clients are fakes."""
import base64
import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import egeria_auth  # noqa: E402
import report_viewer  # noqa: E402
from pyegeria.view.role_supply import CallerTokenExpired, NoSuchReader, RoleRefused, supply_inputs  # noqa: E402


def _jwt(sub="peter", exp_in=3600):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in})}.sig"


class FakeClient:
    instances = []
    lineage_seen = []

    def __init__(self, view_server, url, user_id=None, user_pwd=None):
        self.user_id, self.user_pwd, self.bearer, self.minted = user_id, user_pwd, None, False
        FakeClient.instances.append(self)
        import pyegeria
        FakeClient.lineage_seen.append(egeria_auth.for_lineage_requested())

    def set_bearer_token(self, t):
        self.bearer = t

    def create_egeria_bearer_token(self):
        self.minted = True


@pytest.fixture(autouse=True)
def _reset():
    FakeClient.instances.clear()
    FakeClient.lineage_seen.clear()


def test_token_client_holds_no_password_and_acts_as_token_user():
    tok = egeria_auth._egeria_token.set(_jwt("peter"))
    try:
        c = egeria_auth.PortalSupply().client(FakeClient)
    finally:
        egeria_auth._egeria_token.reset(tok)
    assert c.bearer and c.user_pwd is None and c.user_id == "peter" and not c.minted


def test_expired_token_refused_before_any_client_is_built():
    tok = egeria_auth._egeria_token.set(_jwt(exp_in=-5))
    try:
        with pytest.raises(CallerTokenExpired) as e:
            supply_inputs("r", ["egeria_client:EgeriaTech"], egeria_auth.PortalSupply())
    finally:
        egeria_auth._egeria_token.reset(tok)
    assert FakeClient.instances == []
    assert egeria_auth.TOKEN_REFUSED_WORDS in str(e.value)


def test_no_token_keeps_todays_service_sign_in():
    c = egeria_auth.PortalSupply().client(FakeClient)
    assert c.minted and c.bearer is None


def test_client_is_cached_per_class():
    s = egeria_auth.PortalSupply()
    assert s.client(FakeClient) is s.client(FakeClient)
    assert len(FakeClient.instances) == 1


def test_lineage_flag_in_force_for_client():
    fl = egeria_auth._for_lineage.set(True)
    try:
        egeria_auth.PortalSupply().client(FakeClient)
    finally:
        egeria_auth._for_lineage.reset(fl)
    assert FakeClient.lineage_seen == [True]


def test_viewer_read_from_report_viewer_contextvar():
    t = report_viewer.set_viewer({"persona_id": "erinoverview", "persona": {"display_name": "Erin Overview"},
                                  "user": None, "reason": ""})
    try:
        v = egeria_auth.PortalSupply().viewer()
    finally:
        report_viewer.reset_viewer(t)
    assert (v.user_id, v.display_name, v.is_admin) == ("erinoverview", "Erin Overview", None)


def test_viewer_refused_with_reason_when_no_persona():
    t = report_viewer.set_viewer({"persona_id": None, "persona": None, "user": None, "reason": "no persona was chosen in this browser"})
    try:
        with pytest.raises(RoleRefused) as e:
            egeria_auth.PortalSupply().viewer()
    finally:
        report_viewer.reset_viewer(t)
    assert "no persona was chosen in this browser" in str(e.value)


def test_reader_and_subject():
    s = egeria_auth.PortalSupply()
    with pytest.raises(NoSuchReader):
        s.reader("x")
    assert s.subject() is None


def test_unreadable_exp_is_not_expired():
    assert egeria_auth._token_expired("not-a-jwt") is False
