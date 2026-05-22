"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Dr. Egeria Commands — FastAPI router.

Reads markdown command templates from the templates directory and returns a
structured representation of all available Dr. Egeria commands, grouped by
level (basic/advanced) and family.

Endpoints:
  GET /api/dr-egeria/commands    → all commands grouped by level and family
"""

import os
import re

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["dr-egeria"])

TEMPLATES_ROOT = os.environ.get("TEMPLATES_PATH", "/app/templates")


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
