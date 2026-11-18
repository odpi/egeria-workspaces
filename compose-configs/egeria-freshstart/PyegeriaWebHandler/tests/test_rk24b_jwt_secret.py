"""
RK-24b: the freshstart Portal never signs or checks a session with an unset key or the published default.

gen-env.sh rewrote .env on every run without JWT_SECRET, so the compose default (published in the repo) signed every
freshstart's session cookies: anyone could forge one. Now gen-env.sh keeps or generates the key, compose has no
default, and the handlers refuse an unset key or the published value. These tests cover the handler side; gen-env's
carry-over is checked by running the script twice on a scratch copy.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import demo_config  # noqa: E402


@pytest.mark.parametrize("value", ["", demo_config.PUBLIC_JWT_DEFAULT])
def test_the_signing_key_is_refused_when_unset_or_published(monkeypatch, value):
    monkeypatch.setattr(demo_config, "JWT_SECRET", value)
    with pytest.raises(RuntimeError) as info:
        demo_config.jwt_signing_key()
    assert "could be forged" in str(info.value)


def test_a_real_key_is_returned(monkeypatch):
    monkeypatch.setattr(demo_config, "JWT_SECRET", "a-real-random-key-for-this-test-only-0123456789")
    assert demo_config.jwt_signing_key() == "a-real-random-key-for-this-test-only-0123456789"


def test_signing_a_session_answers_503_without_a_real_key(monkeypatch):
    from fastapi import HTTPException
    import demo_auth_handler
    monkeypatch.setattr(demo_config, "JWT_SECRET", demo_config.PUBLIC_JWT_DEFAULT)
    with pytest.raises(HTTPException) as info:
        demo_auth_handler._make_jwt("someone", "user", "Someone", "egeria-token")
    assert info.value.status_code == 503


def test_a_session_signed_with_a_real_key_round_trips(monkeypatch):
    import demo_auth_handler
    monkeypatch.setattr(demo_config, "JWT_SECRET", "a-real-random-key-for-this-test-only-0123456789")
    token = demo_auth_handler._make_jwt("someone", "user", "Someone", "egeria-token")
    assert demo_auth_handler._decode_jwt(token)["sub"] == "someone"


def test_a_session_forged_with_the_published_key_is_not_accepted(monkeypatch):
    from jose import jwt
    import demo_auth_handler
    forged = jwt.encode({"sub": "admin", "role": "admin"}, demo_config.PUBLIC_JWT_DEFAULT, algorithm="HS256")
    monkeypatch.setattr(demo_config, "JWT_SECRET", "a-real-random-key-for-this-test-only-0123456789")
    with pytest.raises(Exception):
        demo_auth_handler._decode_jwt(forged)


def test_the_compose_file_has_no_published_default():
    compose = Path(__file__).resolve().parents[2] / "egeria-freshstart.yaml"
    if not compose.exists():   # a gate that copies only PyegeriaWebHandler/ can't see it; CI checks out the repo
        pytest.skip("egeria-freshstart.yaml isn't in this checkout (only PyegeriaWebHandler/ was copied)")
    yaml_text = compose.read_text(encoding="utf-8")
    assert "JWT_SECRET:-" not in yaml_text
    assert demo_config.PUBLIC_JWT_DEFAULT not in yaml_text
