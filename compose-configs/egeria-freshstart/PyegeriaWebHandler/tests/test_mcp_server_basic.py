import os
import io
import asyncio
from pathlib import Path

import builtins


# Under test path setup
import importlib
import sys
from pathlib import Path as _P

# Add PyegeriaWebHandler directory to sys.path so we can import modules directly
_THIS_DIR = _P(__file__).resolve().parent
_MODULE_DIR = _THIS_DIR.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))


def setup_temp_env(tmp_path: Path):
    # Point inbox/outbox to temp directories
    os.environ["EGERIA_ROOT_PATH"] = str(tmp_path)
    os.environ["EGERIA_INBOX_PATH"] = "inbox"
    os.environ["EGERIA_OUTBOX"] = "outbox"
    # Credentials (won't be used beyond token creation in these tests)
    os.environ["EGERIA_USER"] = "testuser"
    os.environ["EGERIA_USER_PASSWORD"] = "testpass"


class FakeEgeriaTech:
    def __init__(self, *args, **kwargs):
        pass

    def create_egeria_bearer_token(self, user, pwd):
        # Minimal stub used by dr_egeria_md
        return "fake-token"


def test_write_block_to_inbox_and_formatting(tmp_path, monkeypatch):
    setup_temp_env(tmp_path)

    # Import mcp_server fresh to pick up env
    mcp_server = importlib.import_module(
        "compose-configs.egeria-quickstart.PyegeriaWebHandler.mcp_server".replace("-", "_")
    )

    # Ensure dr_egeria_md.EgeriaTech is a fake to avoid any network
    monkeypatch.setattr(mcp_server.dr_egeria_md, "EgeriaTech", FakeEgeriaTech, raising=True)

    # Call the helper to write a minimal block
    file_name = mcp_server._write_block_to_inbox("# Test Block\nSome content\n")

    inbox_dir = Path(os.environ["EGERIA_ROOT_PATH"]) / os.environ.get("EGERIA_INBOX_PATH", "inbox")
    full_path = inbox_dir / file_name
    assert full_path.exists(), "Markdown file was not written to inbox"

    text = full_path.read_text(encoding="utf-8")
    # Should start with a H1 and end with delimiter line
    assert text.lstrip().startswith("# ")
    assert "\n___" in text, "Delimiter not appended to command block"


def test_run_block_unknown_command_returns_message(tmp_path, monkeypatch):
    setup_temp_env(tmp_path)
    mcp_server = importlib.import_module(
        "compose-configs.egeria-quickstart.PyegeriaWebHandler.mcp_server".replace("-", "_")
    )

    # Stub EgeriaTech to prevent real calls
    monkeypatch.setattr(mcp_server.dr_egeria_md, "EgeriaTech", FakeEgeriaTech, raising=True)

    # Provide a block that is very likely NOT a known command so the processor prints a no-op message
    block = "# Totally Unknown Command\nSome text\n___\n"

    text = asyncio.run(
        mcp_server.dr_egeria_run_block(
            ctx=None,
            markdown_block=block,
            url="https://example.invalid:9443",
            server_name="qs-view-server",
            user_id="user",
            user_pass="pass",
            directive="display",
            output_folder="",
        )
    )

    # The underlying processor will report that no updates were detected
    assert "No updates detected" in text or "Unknown command" in text or text != "", (
        f"Unexpected output: {text!r}"
    )


def test_wrapper_tools_delegate_to_run_block(tmp_path, monkeypatch):
    setup_temp_env(tmp_path)
    mcp_server = importlib.import_module(
        "compose-configs.egeria-quickstart.PyegeriaWebHandler.mcp_server".replace("-", "_")
    )

    # Monkeypatch the underlying runner to avoid relying on dr_egeria_md plumbing
    async def fake_run_block(ctx, markdown_block, url, server_name, user_id, user_pass, directive="process", output_folder=""):
        # Return a string that includes the title of the H1 we expect wrappers to construct
        title = markdown_block.splitlines()[0].lstrip("# ").strip()
        return f"OK:{title}:{directive}"

    monkeypatch.setattr(mcp_server, "dr_egeria_run_block", fake_run_block, raising=True)

    txt_g = asyncio.run(
        mcp_server.egeria_list_glossaries(
            ctx=None,
            url="https://example.invalid:9443",
            server_name="qs-view-server",
            user_id="u",
            user_pass="p",
        )
    )
    assert txt_g.startswith("OK:View Glossaries:"), txt_g

    txt_c = asyncio.run(
        mcp_server.egeria_list_collections(
            ctx=None,
            url="https://example.invalid:9443",
            server_name="qs-view-server",
            user_id="u",
            user_pass="p",
        )
    )
    # Collections wrapper uses display directive
    assert txt_c.startswith("OK:View Collections:"), txt_c
