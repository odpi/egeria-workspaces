# Model Context Protocol (MCP) server that exposes Dr. Egeria capabilities via tools
#
# This server focuses on glossaries and collections to start with, by leveraging the
# existing dr_egeria_md processor. We provide:
# - dr_egeria.run_block: execute a markdown command block using the existing processor
# - egeria.list_glossaries: convenience wrapper to list/view glossaries
# - egeria.list_collections: convenience wrapper to list/view collections
#
# Transport is stdio so this can be used from compatible MCP clients.

from __future__ import annotations

import asyncio
import io
import os
import tempfile
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from typing import Optional

from loguru import logger

# Ensure environment defaults similar to the FastAPI handler
os.environ.setdefault("EGERIA_USER", "erinoverview")
os.environ.setdefault("EGERIA_USER_PASSWORD", "secret")
# Important: ensure root path is empty so container joins to /dr-egeria-inbox/<file>
os.environ.setdefault("EGERIA_ROOT_PATH", "/")
os.environ.setdefault("EGERIA_INBOX_PATH", "dr-egeria-inbox")
os.environ.setdefault("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")

EGERIA_ROOT_PATH = os.environ.get("EGERIA_ROOT_PATH", "/")
EGERIA_INBOX_PATH = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")

# Local import of existing processor
import dr_egeria_md  # type: ignore

# MCP server primitives
from mcp.server.fastmcp import FastMCP, Context


server = FastMCP(
    "pyegeria-mcp",
    version="0.1.0",
    description="Model Context Protocol server exposing Egeria via Dr. Egeria markdown commands.",
)


def _run_and_capture(func, *args, **kwargs) -> str:
    """Run a callable capturing both stdout and stderr and return the combined text."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        try:
            func(*args, **kwargs)
        except SystemExit:
            # in case click tries to exit
            pass
        except Exception as e:
            # Let exceptions be reflected on stderr capture
            import traceback
            traceback.print_exc()
    out = stdout_buf.getvalue()
    err = stderr_buf.getvalue()
    return (out + ("\n" if out and err else "") + err).strip()


def _write_block_to_inbox(markdown_block: str) -> str:
    """Write the provided markdown block to the configured inbox and return the relative file name.
    We create a unique file name with timestamp to avoid clashes.
    """
    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    file_name = f"mcp-{ts}.md"
    inbox_dir = os.path.join(EGERIA_ROOT_PATH, EGERIA_INBOX_PATH)
    os.makedirs(inbox_dir, exist_ok=True)
    full_path = os.path.join(inbox_dir, file_name)
    with open(full_path, "w", encoding="utf-8") as f:
        # Ensure H1 wrapped block terminates with ___ delimiter if not present
        content = markdown_block.strip()
        if not content.startswith("# "):
            content = "# MCP Command\n\n" + content
        if "\n___" not in content:
            if not content.endswith("\n"):
                content += "\n"
            content += "___\n"
        f.write(content)
    return file_name


@server.tool()
async def dr_egeria_run_block(
    ctx: Context,
    markdown_block: str,
    url: str,
    server_name: str,
    user_id: str,
    user_pass: str,
    directive: str = "process",
    output_folder: str = "",
) -> str:
    """Execute a Dr. Egeria markdown command block using the existing processor and return the console output.
    Parameters:
    - markdown_block: Markdown content that contains one or more H1 command blocks understood by Dr. Egeria.
    - url: Egeria platform URL (e.g., https://host.docker.internal:9443)
    - server_name: Egeria view server name (e.g., qs-view-server)
    - user_id / user_pass: Egeria credentials
    - directive: display | validate | process (default process)
    - output_folder: optional subfolder under outbox
    """
    # Write to inbox and invoke the existing file-based processor
    file_name = _write_block_to_inbox(markdown_block)
    cmd = dr_egeria_md.process_markdown_file
    func = getattr(cmd, "callback", cmd)
    text = _run_and_capture(
        func,
        input_file=file_name,
        output_folder=output_folder or "",
        directive=directive,
        server=server_name,
        url=url,
        userid=user_id,
        user_pass=user_pass,
    )
    return text or "(no output)"


def _build_simple_block(title: str) -> str:
    return f"# {title}\n___\n"


@server.tool()
async def egeria_list_glossaries(
    ctx: Context,
    url: str,
    server_name: str,
    user_id: str,
    user_pass: str,
) -> str:
    """List or view glossaries in the connected Egeria environment."""
    block = _build_simple_block("View Glossaries")
    return await dr_egeria_run_block(ctx, block, url, server_name, user_id, user_pass, directive="display")


@server.tool()
async def egeria_list_collections(
    ctx: Context,
    url: str,
    server_name: str,
    user_id: str,
    user_pass: str,
) -> str:
    """List or view collections/folders in the connected Egeria environment."""
    # Many collection views are produced through the output command paths; use a generic View command
    block = _build_simple_block("View Collections")
    # Fallback: if not recognized, the processor will echo an unknown command message which is still useful feedback
    return await dr_egeria_run_block(ctx, block, url, server_name, user_id, user_pass, directive="display")


async def main() -> None:
    # Run stdio transport for MCP
    await server.run_stdio()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
