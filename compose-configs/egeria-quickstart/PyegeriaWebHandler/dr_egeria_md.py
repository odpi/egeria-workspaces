import os
import sys
import asyncio
from typing import Optional
from rich.console import Console
from pyegeria import EgeriaTech
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Use local md_processing
from md_processing.md_processing_utils.md_processing_constants import load_commands
from md_processing.v2 import UniversalExtractor

# setup_dispatcher itself comes straight from pyegeria's own md_processing.dr_egeria --
# this app used to carry a hand-duplicated copy here (same structure, same imports,
# no app-specific processors of its own) that silently drifted out of sync as pyegeria
# added new command families upstream: it was missing "Create Report"/"Update Report"
# (only had "View Report") and the entire Dashboard Sheet family (Create Dashboard
# Sheet / Link Report to Dashboard Sheet / Add Text on Dashboard Sheet) entirely,
# so those commands reported "No processor registered" (or, for Create Report, were
# silently preserved as unparsed raw text) even though pyegeria's real dispatcher has
# always had them. Importing the real one directly means this app can no longer drift
# from pyegeria's command coverage.
from md_processing.dr_egeria import setup_dispatcher

# Configuration from environment
EGERIA_WIDTH = os.environ.get("EGERIA_WIDTH", "100")
EGERIA_ROOT_PATH = os.environ.get("EGERIA_ROOT_PATH", "/")
EGERIA_INBOX_PATH = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")
EGERIA_OUTBOX_PATH = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")

# Initial load
load_commands()

async def process_md_file_async(input_file: str, output_folder: str, directive: str,
                                server: str, url: str, userid: str, user_pass: str,
                                outbox_path: Optional[str] = None) -> str:
    # Get latest configuration from environment dynamically
    width = int(os.environ.get("EGERIA_WIDTH", "100"))
    root_path = os.environ.get("EGERIA_ROOT_PATH", "/")
    inbox_path = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")
    outbox_env = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")

    console = Console(width=width, force_terminal=False)
    client = EgeriaTech(server, url, user_id=userid)
    client.create_egeria_bearer_token(userid, user_pass)
    
    dispatcher = setup_dispatcher(client)
    
    # Construct the full file path. 
    # Use os.path.normpath to avoid issues like /./filename
    if os.path.isabs(input_file):
        full_file_path = os.path.normpath(input_file)
    else:
        full_file_path = os.path.normpath(os.path.join(root_path, inbox_path, input_file))
    
    # Fallback search if not found at primary path
    if not os.path.exists(full_file_path):
        mount_points = ["/work", "/coco-workbooks", "/work/Work-Obsidian"]
        for mp in mount_points:
            fallback = os.path.normpath(os.path.join(mp, input_file.lstrip("/")))
            if os.path.exists(fallback):
                full_file_path = fallback
                break
                
    if not os.path.exists(full_file_path):
        console.print(f"[bold red]Error:[/bold red] File not found at {full_file_path}")
        return f"Error: File not found at {full_file_path}"

    try:
        with open(full_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to read {full_file_path}: {e}")
        return f"Error: Failed to read {full_file_path}: {e}"

    extractor = UniversalExtractor(content)
    commands = extractor.extract_commands()
    
    if not commands:
        console.print(f"[bold yellow]Warning:[/bold yellow] No valid Egeria commands found in {input_file}")
        return f"Warning: No valid Egeria commands found in {input_file}"

    results = await dispatcher.dispatch_batch(commands, context={"directive": directive})

    # Aggregate output
    final_output = ""
    for res in results:
        if res.get("output"):
            final_output += res["output"] + "\n\n"

    return final_output


async def process_md_file_structured_async(
    input_file: str, output_folder: str, directive: str,
    server: str, url: str, userid: str, user_pass: str,
    outbox_path: Optional[str] = None,
) -> dict:
    """Like process_md_file_async but returns the full per-command result list alongside aggregated output."""
    width = int(os.environ.get("EGERIA_WIDTH", "100"))
    root_path = os.environ.get("EGERIA_ROOT_PATH", "/")
    inbox_path = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")

    Console(width=width, force_terminal=False)
    client = EgeriaTech(server, url, user_id=userid)
    client.create_egeria_bearer_token(userid, user_pass)

    dispatcher = setup_dispatcher(client)

    if os.path.isabs(input_file):
        full_file_path = os.path.normpath(input_file)
    else:
        full_file_path = os.path.normpath(os.path.join(root_path, inbox_path, input_file))

    if not os.path.exists(full_file_path):
        for mp in ["/work", "/coco-workbooks", "/work/Work-Obsidian"]:
            fallback = os.path.normpath(os.path.join(mp, input_file.lstrip("/")))
            if os.path.exists(fallback):
                full_file_path = fallback
                break

    if not os.path.exists(full_file_path):
        return {"output": f"Error: File not found at {full_file_path}", "results": [], "error": "file_not_found"}

    try:
        with open(full_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return {"output": f"Error: Failed to read {full_file_path}: {e}", "results": [], "error": "read_error"}

    extractor = UniversalExtractor(content)
    commands = extractor.extract_commands()

    if not commands:
        return {"output": "Warning: No valid Egeria commands found", "results": [], "error": "no_commands"}

    # Capture stdout so we receive Rich console output written by V2 processors
    import sys
    from io import StringIO
    _capture = StringIO()
    _old_stdout = sys.stdout
    sys.stdout = _capture
    try:
        results = await dispatcher.dispatch_batch(commands, context={"directive": directive})
    finally:
        sys.stdout = _old_stdout
    captured_stdout = _capture.getvalue()

    # Primary: aggregate per-command output strings (populated by some processor types)
    final_output = ""
    for res in results:
        if res.get("output"):
            final_output += res["output"] + "\n\n"

    # Secondary: use captured stdout (Rich console output from processors)
    if not final_output.strip() and captured_stdout.strip():
        final_output = captured_stdout

    # Fallback: synthesize human-readable output from result messages
    if not final_output.strip():
        parts = []
        for res in results:
            if not res.get("is_command", True):
                continue
            msg = res.get("message", "")
            if not msg:
                continue
            status = res.get("status", "success")
            verb   = res.get("verb", "")
            obj    = res.get("object_type", "")
            icon   = "✅" if status == "success" else ("⚠️" if status == "warning" else "❌")
            cmd    = f"{verb} {obj}".strip()
            parts.append(f"{icon} **{cmd}**: {msg}" if cmd else f"{icon} {msg}")
        if parts:
            final_output = "\n\n".join(parts)

    return {"output": final_output, "results": results}


def process_markdown_file_structured(
    input_file: str, output_folder: str, directive: str,
    server: str, url: str, userid: str, user_pass: str,
    outbox_path: Optional[str] = None,
) -> dict:
    """Synchronous wrapper returning per-command result metadata alongside aggregated output."""
    try:
        return asyncio.run(process_md_file_structured_async(
            input_file, output_folder, directive, server, url, userid, user_pass, outbox_path
        ))
    except Exception as e:
        return {"output": f"Error: Async processing failed: {e}", "results": [], "error": str(e)}


def process_markdown_file(input_file: str, output_folder: str, directive: str,
                        server: str, url: str, userid: str, user_pass: str,
                        outbox_path: Optional[str] = None) -> str:
    """Synchronous wrapper for backward compatibility with existing pyegeria_handler.py and mcp_server.py"""
    try:
        return asyncio.run(process_md_file_async(input_file, output_folder, directive, server, url, userid, user_pass, outbox_path))
    except Exception as e:
        print(f"Async processing failed: {e}")
        return f"Error: Async processing failed: {e}"

# Alias for backward compatibility
process_md_file = process_markdown_file
