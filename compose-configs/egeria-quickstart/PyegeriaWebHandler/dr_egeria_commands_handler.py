"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Dr. Egeria Commands — FastAPI router.

Reads markdown command templates from the templates directory and returns a
structured representation of all available Dr. Egeria commands, grouped by
level (basic/advanced) and family.

Endpoints:
  GET /api/dr-egeria/commands         → all commands grouped by level and family
  POST /api/dr-egeria/execute         → build and execute a command block
"""

import os
import re
import tempfile
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from loguru import logger

router = APIRouter(tags=["dr-egeria"])

TEMPLATES_ROOT = os.environ.get("TEMPLATES_PATH", "/app/templates")
EGERIA_ROOT_PATH  = os.environ.get("EGERIA_ROOT_PATH",  "/")
EGERIA_INBOX_PATH = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")
EGERIA_OUTBOX_PATH = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")


def _parse_template(filepath: str) -> dict:
    """Parse a Dr. Egeria markdown template, extracting title, description and parameters."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        logger.warning(f"Could not read template {filepath}: {exc}")
        return {}

    lines = content.splitlines()
    title = ""
    description = ""
    parameters = []

    i = 0
    n = len(lines)

    # Find the ## title and collect the description (> lines) that follow
    while i < n:
        stripped = lines[i].strip()
        if stripped.startswith("## ") and not title:
            title = stripped[3:].strip()
            i += 1
            desc_parts = []
            while i < n:
                l = lines[i].strip()
                if l.startswith("### "):
                    break
                if l.startswith("> ") and not re.match(r"^>\s+\*\*", l):
                    text = l[2:].strip()
                    if text and not text.startswith("**"):
                        desc_parts.append(text)
                i += 1
            description = " ".join(desc_parts)
            break
        i += 1

    # Parse ### parameter blocks
    i = 0
    while i < n:
        stripped = lines[i].strip()
        if stripped.startswith("### "):
            param_name = stripped[4:].strip()
            param: dict = {
                "name": param_name,
                "required": False,
                "attribute_type": "",
                "description": "",
                "default_value": "",
                "alternative_labels": "",
                "valid_values": "",
            }
            i += 1
            while i < n:
                l = lines[i].strip()
                if l.startswith("### ") or l.startswith("## ") or l == "___":
                    break
                if l.startswith(">"):
                    text = l.lstrip(">").strip()
                    if text.startswith("**Input Required**:"):
                        val = text.split(":", 1)[1].strip().lower()
                        param["required"] = val in ("true", "yes")
                    elif text.startswith("**Attribute Type**:"):
                        param["attribute_type"] = text.split(":", 1)[1].strip()
                    elif text.startswith("**Description**:"):
                        param["description"] = text.split(":", 1)[1].strip()
                    elif text.startswith("**Default Value**:"):
                        param["default_value"] = text.split(":", 1)[1].strip()
                    elif text.startswith("**Alternative Labels**:"):
                        param["alternative_labels"] = text.split(":", 1)[1].strip()
                    elif text.startswith("**Valid Values**:"):
                        param["valid_values"] = text.split(":", 1)[1].strip()
                i += 1
            parameters.append(param)
            continue
        i += 1

    return {
        "title": title,
        "description": description,
        "parameters": parameters,
        "required_count": sum(1 for p in parameters if p["required"]),
        "optional_count": sum(1 for p in parameters if not p["required"]),
    }


def _load_level(level_dir: str) -> dict:
    """Load all families and their commands from a level directory (basic or advanced)."""
    families: dict = {}
    if not os.path.isdir(level_dir):
        return families
    for family in sorted(os.listdir(level_dir)):
        family_dir = os.path.join(level_dir, family)
        if not os.path.isdir(family_dir):
            continue
        commands = []
        for filename in sorted(os.listdir(family_dir)):
            if not filename.endswith(".md"):
                continue
            cmd = _parse_template(os.path.join(family_dir, filename))
            if cmd.get("title"):
                cmd["filename"] = filename[:-3]
                commands.append(cmd)
        if commands:
            families[family] = commands
    return families


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/api/dr-egeria/commands", summary="List all Dr. Egeria command templates")
def get_commands():
    """Return all Dr. Egeria command templates grouped by level (basic/advanced) and family."""
    templates_root = TEMPLATES_ROOT
    if not os.path.isdir(templates_root):
        logger.warning(f"Templates directory not found: {templates_root}")
        return JSONResponse({"basic": {}, "advanced": {}, "error": f"Templates not found at {templates_root}"})

    result = {
        "basic":    _load_level(os.path.join(templates_root, "basic")),
        "advanced": _load_level(os.path.join(templates_root, "advanced")),
    }
    basic_count    = sum(len(cmds) for cmds in result["basic"].values())
    advanced_count = sum(len(cmds) for cmds in result["advanced"].values())
    logger.info(f"Dr. Egeria commands loaded: {basic_count} basic, {advanced_count} advanced")
    return JSONResponse(result)


class ExecuteRequest(BaseModel):
    title:     str
    params:    dict = {}
    directive: str  = "display"
    url:       Optional[str] = None
    server:    Optional[str] = None
    user_id:   Optional[str] = None
    user_pwd:  Optional[str] = None


def _build_markdown_block(title: str, params: dict) -> str:
    """Build a Dr. Egeria markdown block from a command title and parameter dict."""
    lines = [f"# Egeria Explorer\n", f"## {title}\n", "> \n"]
    for name, value in params.items():
        if value is not None and str(value).strip():
            lines.append(f"### {name}\n> {value}\n\n")
    lines.append("___\n")
    return "".join(lines)


def _write_and_execute(markdown_block: str, directive: str,
                       url: str, server: str, user_id: str, user_pwd: str) -> str:
    """Write block to temp inbox file, execute, return result markdown."""
    import dr_egeria_md

    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    inbox_dir = os.path.join(EGERIA_ROOT_PATH, EGERIA_INBOX_PATH)
    os.makedirs(inbox_dir, exist_ok=True)
    file_path = os.path.join(inbox_dir, f"explorer-{ts}.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_block)

    # Patch env so the processor resolves paths correctly
    os.environ["EGERIA_ROOT_PATH"]  = "/"
    os.environ["EGERIA_INBOX_PATH"] = "."

    cmd  = dr_egeria_md.process_markdown_file
    func = getattr(cmd, "callback", cmd)
    try:
        result = func(
            input_file=file_path,
            output_folder="",
            directive=directive,
            server=server,
            url=url,
            userid=user_id,
            user_pass=user_pwd,
            outbox_path=EGERIA_OUTBOX_PATH,
        )
        return result or "(no output generated)"
    finally:
        try:
            os.remove(file_path)
        except OSError:
            pass


@router.post("/api/dr-egeria/execute", summary="Execute a Dr. Egeria command block")
def execute_command(req: ExecuteRequest):
    """Build a markdown block from the given command title + params and execute it."""
    url     = req.url     or os.environ.get("EGERIA_PLATFORM_URL",  "https://egeria-main:9443")
    server  = req.server  or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id = req.user_id or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = req.user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")

    block = _build_markdown_block(req.title, req.params)
    logger.info(f"Dr. Egeria execute: title={req.title!r} directive={req.directive!r}")

    try:
        result_md = _write_and_execute(block, req.directive, url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Dr. Egeria execute failed")
        return JSONResponse(
            {"error": str(exc), "markdown": f"❌ Execution failed: {exc}"},
            status_code=500,
        )

    return JSONResponse({"markdown": result_md, "directive": req.directive})
