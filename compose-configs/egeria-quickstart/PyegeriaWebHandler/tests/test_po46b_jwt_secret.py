"""
PO-46b: the quickstart Portal never signs or checks a session with an unset key or a published default.

Outside --demo, gen-env.sh rewrote .env on every run without JWT_SECRET, so the compose default (published in the
repo) signed every quickstart's session cookies, and the handlers fell back to a second published value. Now
gen-env.sh keeps or generates the key, compose has no default, and the handlers refuse an unset key or either
published value. These tests cover the handler side; gen-env's carry-over is checked by running the script's
JWT block on a scratch copy.
"""
import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import demo_config  # noqa: E402

REAL_KEY = "a-real-random-key-for-this-test-only-0123456789"


@pytest.mark.parametrize("value", ["", *demo_config.PUBLIC_JWT_DEFAULTS])
def test_the_signing_key_is_refused_when_unset_or_published(monkeypatch, value):
    monkeypatch.setattr(demo_config, "JWT_SECRET", value)
    with pytest.raises(RuntimeError) as info:
        demo_config.jwt_signing_key()
    assert "could be forged" in str(info.value)
    assert value == "" or value not in str(info.value)   # the refusal never repeats the key


def test_both_published_values_are_refused():
    assert set(demo_config.PUBLIC_JWT_DEFAULTS) == {
        "change-me-before-going-public", "change-me-before-going-public-meow"}


def test_a_real_key_is_returned(monkeypatch):
    monkeypatch.setattr(demo_config, "JWT_SECRET", REAL_KEY)
    assert demo_config.jwt_signing_key() == REAL_KEY


@pytest.mark.parametrize("value", ["", *demo_config.PUBLIC_JWT_DEFAULTS])
def test_signing_a_session_answers_503_without_a_real_key(monkeypatch, value):
    from fastapi import HTTPException
    import demo_auth_handler
    monkeypatch.setattr(demo_config, "JWT_SECRET", value)
    with pytest.raises(HTTPException) as info:
        demo_auth_handler._make_jwt("someone", "user")
    assert info.value.status_code == 503


def test_a_session_signed_with_a_real_key_round_trips(monkeypatch):
    import demo_auth_handler
    monkeypatch.setattr(demo_config, "JWT_SECRET", REAL_KEY)
    token = demo_auth_handler._make_jwt("someone", "user")
    assert demo_auth_handler._decode_jwt(token)["sub"] == "someone"


@pytest.mark.parametrize("published", demo_config.PUBLIC_JWT_DEFAULTS)
def test_a_session_forged_with_a_published_key_is_not_accepted(monkeypatch, published):
    from jose import jwt
    import demo_auth_handler
    forged = jwt.encode({"sub": "admin", "role": "admin"}, published, algorithm="HS256")
    monkeypatch.setattr(demo_config, "JWT_SECRET", REAL_KEY)
    with pytest.raises(Exception):
        demo_auth_handler._decode_jwt(forged)


def test_the_auth_gate_fails_closed_without_a_real_key(monkeypatch):
    """No usable key: the gate says 'not authenticated' rather than raising (a 500) or trusting the token."""
    from jose import jwt
    import demo_auth_gate
    token = jwt.encode({"sub": "admin", "role": "admin"}, demo_config.PUBLIC_JWT_DEFAULT, algorithm="HS256")
    monkeypatch.setattr(demo_config, "JWT_SECRET", demo_config.PUBLIC_JWT_DEFAULT)
    monkeypatch.setattr(demo_auth_gate, "_token", lambda headers: token)
    assert asyncio.run(demo_auth_gate._authenticated({})) is False


def test_feedback_treats_the_caller_as_anonymous_without_a_real_key(monkeypatch):
    from jose import jwt
    import demo_feedback_handler

    class _Req:
        cookies = {"demo_token": jwt.encode({"sub": "admin"}, demo_config.PUBLIC_JWT_DEFAULT, algorithm="HS256")}
        headers = {}

    monkeypatch.setattr(demo_config, "JWT_SECRET", demo_config.PUBLIC_JWT_DEFAULT)
    assert demo_feedback_handler._jwt_payload(_Req()) == {}


def test_feedback_reads_a_session_signed_with_a_real_key(monkeypatch):
    from jose import jwt
    import demo_feedback_handler

    class _Req:
        cookies = {"demo_token": jwt.encode({"sub": "someone"}, REAL_KEY, algorithm="HS256")}
        headers = {}

    monkeypatch.setattr(demo_config, "JWT_SECRET", REAL_KEY)
    assert demo_feedback_handler._jwt_payload(_Req())["sub"] == "someone"


def test_the_compose_file_has_no_published_default():
    compose = Path(__file__).resolve().parents[2] / "egeria-quickstart.yaml"
    if not compose.exists():   # a gate that copies only PyegeriaWebHandler/ can't see it; CI checks out the repo
        pytest.skip("egeria-quickstart.yaml isn't in this checkout (only PyegeriaWebHandler/ was copied)")
    yaml_text = compose.read_text(encoding="utf-8")
    assert "JWT_SECRET:-" not in yaml_text
    for published in demo_config.PUBLIC_JWT_DEFAULTS:
        assert published not in yaml_text
