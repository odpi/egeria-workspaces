"""PY-30: a Dr.Egeria block that ran no command must not report success, and it carries the extractor's hints."""
import json

import mcp_server


def test_zero_commands_is_not_success_and_carries_hints():
    raw = {"output": "", "results": [{"is_command": False}],
           "hints": ["line 1: '# Delete Instance' is an H1 heading, so it is read as a title, not a command."]}
    out = json.loads(mcp_server._build_structured_response(raw, "validate"))
    assert out["success"] is False
    assert out["commands_total"] == 0
    assert out["hints"] == raw["hints"]


def test_zero_commands_without_hints_still_says_why():
    out = json.loads(mcp_server._build_structured_response({"output": "", "results": []}, "process"))
    assert out["success"] is False
    assert out["hints"] and "No Dr.Egeria command was found" in out["hints"][0]


def test_a_successful_command_has_no_hints_and_succeeds():
    raw = {"output": "ok", "results": [{"is_command": True, "status": "success", "verb": "Delete",
                                        "object_type": "Instance"}], "hints": []}
    out = json.loads(mcp_server._build_structured_response(raw, "process"))
    assert out["success"] is True and out["commands_total"] == 1 and out["hints"] == []


def test_error_path_carries_hints():
    raw = {"output": "Warning: No valid Egeria commands found", "results": [], "error": "no_commands",
           "hints": ["No Dr.Egeria command was found."]}
    out = json.loads(mcp_server._build_structured_response(raw, "process"))
    assert out["success"] is False and out["hints"] == ["No Dr.Egeria command was found."]
