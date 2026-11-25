"""PO-82 (quickstart's PO-79): the quickstart Portal never accepts a published MCP token.

On the public demo, users' Jupyter containers share egeria_network with pyegeria-web:8000, so the published token let any
notebook drive the MCP tools. The compose file hardcoded MCP_ACCESS_TOKEN "egeria-secret-mcp-token", which was also pyegeria_handler's default, and
MCPTokenMiddleware accepted it, so anyone who could reach the Portal's port could drive the MCP tools. Now the token comes from
.env (gen-env.sh generates one on the first run and keeps it), an unset token means MCP is off and says so, and the published
value is refused (at startup, and per request if it got that far), the way a published JWT_SECRET is (PO-46b).
Run with JWT_SECRET, MCP_ACCESS_TOKEN and EGERIA_* unset: nothing here reads them.
"""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import demo_config  # noqa: E402

PUBLISHED = "egeria-secret-mcp-token"
REAL = "a-real-random-mcp-token-for-this-test-only-0123456789abcdef"
QS = Path(__file__).resolve().parents[2]            # compose-configs/egeria-quickstart


def _app(monkeypatch, token):
    """The real MCPTokenMiddleware over a stub app that records whether the request got through."""
    from fastapi.testclient import TestClient
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    import pyegeria_handler

    monkeypatch.setattr(demo_config, "MCP_ACCESS_TOKEN", token)
    reached = []

    async def ok(request):
        reached.append(request.url.path)
        return JSONResponse({"reached": True})

    inner = Starlette(routes=[Route("/mcp/sse", ok), Route("/mcp/messages", ok, methods=["POST", "GET"]), Route("/other", ok)])
    return TestClient(pyegeria_handler.MCPTokenMiddleware(inner)), reached


# ── the published value is refused ─────────────────────────────────────────────────────────────────────────────────

def test_the_published_value_is_refused_by_the_config(monkeypatch):
    monkeypatch.setattr(demo_config, "MCP_ACCESS_TOKEN", PUBLISHED)
    with pytest.raises(RuntimeError) as info:
        demo_config.mcp_access_token()
    assert "published example value" in str(info.value) and "MCP tools" in str(info.value)


def test_a_request_with_the_published_value_never_gets_through_even_when_it_is_configured(monkeypatch):
    client, reached = _app(monkeypatch, PUBLISHED)
    for kw in ({"params": {"token": PUBLISHED}}, {"headers": {"X-API-Key": PUBLISHED}}):
        r = client.get("/mcp/sse", **kw)
        assert r.status_code == 503 and "published example value" in r.json()["detail"]
    assert reached == []


def test_the_published_value_is_not_accepted_when_a_real_token_is_configured(monkeypatch):
    client, reached = _app(monkeypatch, REAL)
    r = client.get("/mcp/sse", params={"token": PUBLISHED})
    assert r.status_code == 403 and reached == []


def test_startup_refuses_the_published_value_and_says_so():
    src = (Path(__file__).resolve().parents[1] / "pyegeria_handler.py").read_text(encoding="utf-8")
    life = src[src.index("async def _lifespan"):]
    life = life[:life.index("await obs_start()")]
    assert "demo_config.mcp_access_token()" in life            # raises RuntimeError for the published value, before anything starts


# ── an unset token gives no MCP access ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("token", ["", None])
def test_with_no_token_set_mcp_is_off_and_says_so(monkeypatch, token):
    client, reached = _app(monkeypatch, token or "")
    for path in ("/mcp/sse", "/mcp/messages"):
        r = client.get(path) if path.endswith("sse") else client.post(path)
        assert r.status_code == 503 and r.json()["detail"] == demo_config.MCP_OFF_WORDS
    assert "MCP_ACCESS_TOKEN is not set" in demo_config.MCP_OFF_WORDS
    assert reached == []


def test_an_empty_token_is_not_a_match_for_an_unset_one(monkeypatch):
    client, reached = _app(monkeypatch, "")
    r = client.get("/mcp/sse", params={"token": ""})
    assert r.status_code == 503 and reached == []                  # "" == "" must never open it


def test_the_module_has_no_published_default(monkeypatch):
    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    import importlib

    reloaded = importlib.reload(demo_config)
    assert reloaded.MCP_ACCESS_TOKEN == "" and reloaded.mcp_access_token() == ""


# ── a real token works ─────────────────────────────────────────────────────────────────────────────────────────────

def test_a_real_token_works_as_a_query_parameter_and_as_a_header(monkeypatch):
    client, reached = _app(monkeypatch, REAL)
    assert client.get("/mcp/sse", params={"token": REAL}).status_code == 200
    assert client.get("/mcp/sse", headers={"X-API-Key": REAL}).status_code == 200
    assert len(reached) == 2


def test_a_wrong_or_missing_token_is_403_and_a_non_mcp_path_is_not_gated_by_it(monkeypatch):
    client, reached = _app(monkeypatch, REAL)
    assert client.get("/mcp/sse", params={"token": REAL + "x"}).status_code == 403
    assert client.get("/mcp/sse").status_code == 403
    assert client.get("/other").status_code == 200


def test_a_session_message_post_needs_no_token_but_a_session_id(monkeypatch):
    client, reached = _app(monkeypatch, REAL)
    assert client.post("/mcp/messages", params={"session_id": "s1"}).status_code == 200
    assert client.post("/mcp/messages").status_code == 403


# ── the compose file, gen-env.sh, .env.example and the Obsidian plugin's data ──────────────────────────────────────

def test_no_quickstart_file_publishes_the_token_as_a_default():
    for f in sorted(QS.glob("*.yaml")) + [QS / "gen-env.sh", QS / ".env.example"]:
        text = f.read_text(encoding="utf-8")
        if f.name == "gen-env.sh":
            assert text.count(PUBLISHED) == 1, "gen-env.sh names the published value once, to refuse it"
            continue
        assert PUBLISHED not in text, f"{f.name} publishes the MCP token"
    assert 'MCP_ACCESS_TOKEN: "${MCP_ACCESS_TOKEN:-}"' in (QS / "egeria-quickstart.yaml").read_text(encoding="utf-8")


def test_the_handler_modules_have_no_published_default():
    for name in ("pyegeria_handler.py", "obsidian_lock_handler.py"):
        src = (Path(__file__).resolve().parents[1] / name).read_text(encoding="utf-8")
        assert 'os.environ.get("MCP_ACCESS_TOKEN", "' not in src, f"{name} still defaults the token"


def test_env_example_lists_the_variable_with_no_real_value():
    lines = [l for l in (QS / ".env.example").read_text(encoding="utf-8").splitlines() if "MCP_ACCESS_TOKEN" in l and "=" in l]
    assert lines and all(l.strip() in ("# MCP_ACCESS_TOKEN=", "MCP_ACCESS_TOKEN=") for l in lines)


def test_the_obsidian_plugin_is_never_given_the_published_value(monkeypatch):
    import obsidian_lock_handler as olh

    src = Path(olh.__file__).read_text(encoding="utf-8")
    line = next(l for l in src.splitlines() if '"mcpToken"' in l)
    assert "PUBLIC_MCP_TOKENS" in line


# ── gen-env.sh: keeps, generates, and refuses (the pattern JWT_SECRET uses) ─────────────────────────────────────────
# The real MCP block of gen-env.sh, run on its own in a scratch directory: the whole script needs the container engine, the
# shared-infra scripts and the exchange config, none of which this block reads.

def _gen_env(tmp_path, existing_env=None, exported=None, demo_env=None):
    """Run gen-env.sh's MCP_ACCESS_TOKEN block in tmp_path; return (returncode, stderr, the token it settled on)."""
    import os

    text = (QS / "gen-env.sh").read_text(encoding="utf-8")
    block = text[text.index("# MCP_ACCESS_TOKEN (PO-82"):text.index("# Write .env atomically")]
    tmp_path.mkdir(parents=True, exist_ok=True)
    if existing_env is not None:
        (tmp_path / ".env").write_text(existing_env)
    if demo_env is not None:
        (tmp_path / ".env.demo").write_text(demo_env)
    script = "set -euo pipefail\n" + block + 'printf \'MCP_ACCESS_TOKEN=%s\\n\' "$MCP_ACCESS_TOKEN_VAL"\n'
    env = {k: v for k, v in os.environ.items() if k != "MCP_ACCESS_TOKEN"}
    if exported is not None:
        env["MCP_ACCESS_TOKEN"] = exported
    r = subprocess.run(["bash", "-c", script], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=60)
    return r.returncode, r.stderr, _token(r.stdout)


def _token(env_text):
    return next((l.split("=", 1)[1] for l in env_text.splitlines() if l.startswith("MCP_ACCESS_TOKEN=")), None)


def test_gen_env_writes_the_token_into_env():
    text = (QS / "gen-env.sh").read_text(encoding="utf-8")
    assert "printf 'MCP_ACCESS_TOKEN=%s\\n' \"$MCP_ACCESS_TOKEN_VAL\" >> \"$TMP_ENV\"" in text
    assert text.index("# MCP_ACCESS_TOKEN (PO-82") < text.index("# Write .env atomically")


def test_gen_env_generates_a_random_token_once_and_keeps_it(tmp_path):
    code, err, first = _gen_env(tmp_path)
    assert code == 0, err
    assert first and first != PUBLISHED and len(first) >= 32
    assert first not in err                                              # never printed
    code2, err2, again = _gen_env(tmp_path / "again", existing_env=f"X=1\nMCP_ACCESS_TOKEN={first}\n")
    assert code2 == 0 and again == first                                 # kept on the next run


def test_gen_env_keeps_the_demo_value_first(tmp_path):
    code, err, tok = _gen_env(tmp_path, existing_env="MCP_ACCESS_TOKEN=from-env-file-0123456789abcdef0123\n",
                              demo_env=f"MCP_ACCESS_TOKEN={REAL}\n")
    assert code == 0, err
    assert tok == REAL


def test_gen_env_never_keeps_the_published_value_from_an_old_env(tmp_path):
    code, err, tok = _gen_env(tmp_path, existing_env=f"MCP_ACCESS_TOKEN={PUBLISHED}\n")
    assert code == 0, err
    assert tok not in (None, "", PUBLISHED)


def test_gen_env_stops_on_an_exported_published_value(tmp_path):
    code, err, _tok = _gen_env(tmp_path, exported=PUBLISHED)
    assert code != 0 and "published example value" in err and "MCP_ACCESS_TOKEN" in err


def test_an_exported_real_value_wins(tmp_path):
    code, err, tok = _gen_env(tmp_path, exported=REAL)
    assert code == 0, err
    assert tok == REAL


# ── the Call Dr. Egeria Obsidian plugin names no default token ─────────────────────────────────────────────────────

PLUGIN = QS.parents[1] / "obsidian-plugins" / "call-dr-egeria"


@pytest.mark.parametrize("name", ["src/main.ts", "main.js", "deploy.mjs", "README.md"])
def test_the_obsidian_plugin_source_has_no_published_default(name):
    assert PUBLISHED not in (PLUGIN / name).read_text(encoding="utf-8"), f"{name} names the published MCP token"
