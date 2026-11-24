"""
L10 read-back R1: Dr.Egeria execute with no sign-in token, and the Portal not requiring sign-in, uses the Portal's
configured service password, or refuses (503, in words). Never a built-in password.

dr_egeria_identity's no-token branch used to fall back to the well-known demo password when EGERIA_USER_PASSWORD was
unset (the last one left after PO-45). No live server: the token and the auth mode are replaced.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dr_egeria_commands_handler as h  # noqa: E402


def _req(user_pwd=None):
    return SimpleNamespace(url=None, server=None, user_id=None, user_pwd=user_pwd)


@pytest.fixture
def no_token_no_auth(monkeypatch):
    import egeria_auth
    monkeypatch.setattr(egeria_auth, "get_request_token", lambda: None)
    monkeypatch.setattr(h, "_auth_on", lambda: False)


def test_no_service_password_refuses_with_503(no_token_no_auth, monkeypatch):
    monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    with pytest.raises(Exception) as info:
        h.dr_egeria_identity(_req())
    assert getattr(info.value, "status_code", None) == 503
    assert "secret" not in str(getattr(info.value, "detail", info.value))


def test_the_configured_service_password_is_used(no_token_no_auth, monkeypatch):
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "the-configured-service-password")
    ident = h.dr_egeria_identity(_req())
    assert ident.user_pwd == "the-configured-service-password" and ident.token is None


def test_a_body_password_is_still_used_as_given(no_token_no_auth, monkeypatch):
    monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    assert h.dr_egeria_identity(_req(user_pwd="typed-by-the-caller")).user_pwd == "typed-by-the-caller"
