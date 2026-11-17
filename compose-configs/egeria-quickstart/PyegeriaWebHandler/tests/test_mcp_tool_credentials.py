"""PO-44: the MCP tools must not publish the service password as a parameter default, must refuse a caller-named
user without that user's password (the PO-41 rule), and must only send the service password to an allow-listed
platform. Credentials are resolved at call time."""
import asyncio
import inspect
import json

import pytest

import mcp_server

SECRET = "s3rvice-pw-for-test"
TOOLS = ("dr_egeria_run_block", "egeria_list_glossaries", "egeria_list_collections")


@pytest.fixture(autouse=True)
def service_env(monkeypatch):
    monkeypatch.setenv("EGERIA_USER", "svcuser")
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SECRET)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", "https://allowed.example:9443")
    monkeypatch.delenv("PORTAL_ALLOWED_PLATFORMS", raising=False)


def _fn(name):
    f = getattr(mcp_server, name)
    return getattr(f, "fn", f)   # FastMCP may wrap the function


@pytest.mark.parametrize("name", TOOLS)
def test_no_credential_or_url_in_parameter_defaults(name):
    sig = inspect.signature(_fn(name))
    for p in ("url", "server_name", "user_id", "user_pass"):
        assert sig.parameters[p].default is None, f"{name}.{p} has a default"
    assert SECRET not in str(sig)


def test_published_tool_schemas_carry_no_service_password():
    tools = getattr(mcp_server.server, "_tool_manager", None)
    listed = tools.list_tools() if tools and hasattr(tools, "list_tools") else []
    assert len(listed) >= len(TOOLS), "no tool schemas were listed, so this test would prove nothing"
    text = json.dumps([getattr(t, "parameters", {}) for t in listed], default=str)
    assert SECRET not in text and '"secret"' not in text


def test_named_user_without_password_is_refused_before_any_call(monkeypatch):
    called = []
    monkeypatch.setattr(mcp_server, "_write_block_to_inbox", lambda *a, **k: called.append(1) or "x.md")
    out = asyncio.run(_fn("dr_egeria_run_block")(None, "## View Glossaries\n", user_id="peterprofile"))
    assert out.startswith("❌") and not called


def test_service_password_never_goes_to_an_unlisted_platform(monkeypatch):
    called = []
    monkeypatch.setattr(mcp_server, "_write_block_to_inbox", lambda *a, **k: called.append(1) or "x.md")
    out = asyncio.run(_fn("dr_egeria_run_block")(None, "## View Glossaries\n", url="https://evil.example:9443"))
    assert out.startswith("❌") and not called


def test_service_path_resolves_at_call_time():
    url, server, user, pwd = mcp_server._mcp_credentials(None, None, None, None)
    assert (url, user, pwd) == ("https://allowed.example:9443", "svcuser", SECRET)


def test_named_user_with_own_password_is_allowed():
    url, server, user, pwd = mcp_server._mcp_credentials(None, None, "peterprofile", "his-own")
    assert (user, pwd) == ("peterprofile", "his-own")


def test_no_service_password_configured_is_refused_in_words(monkeypatch):
    monkeypatch.delenv("EGERIA_USER_PASSWORD", raising=False)
    called = []
    monkeypatch.setattr(mcp_server, "_write_block_to_inbox", lambda *a, **k: called.append(1) or "x.md")
    out = asyncio.run(_fn("dr_egeria_run_block")(None, "## View Glossaries\n"))
    assert out == "❌ the Portal's service password isn't configured (EGERIA_USER_PASSWORD)" and not called


def test_no_builtin_service_password_is_set_at_import():
    import inspect as _inspect
    assert 'setdefault("EGERIA_USER_PASSWORD"' not in _inspect.getsource(mcp_server._bootstrap_runtime_defaults)
