<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Pyegeria Web Handler
The Pyegeria Web Handler is a python module that provides a web handler for the pyegeria command line interface. It is
used to execute Dr.Egeria commands from anything that can make a REST call - and that shares the same filesystem as
the Egeria runtime.

## Maintenance Notes
The Pyegeria Web Handler now uses the **Dr. Egeria v2** core, which features a dynamic registry-based dispatcher (`V2Dispatcher`).

### Dynamic Discovery
Unlike previous versions, you no longer need to manually update `dr_egeria_md.py` with `if-elif` blocks when new commands are added to `pyegeria`. The handler now:
1.  **Auto-Registers**: Scans command specifications (JSON) in `md_processing/data/compact_commands` and automatically maps them to their respective processors.
2.  **Supports Variants**: Handles "Link", "Attach", "Add", "Detach", "Remove", etc., automatically based on the command specs.
3.  **Hot Reload**: You can trigger a refresh of the command specifications (without restarting the container) via the `/dr-egeria/refresh` POST endpoint or the "Refresh" button in the Obsidian plugin.

### Diagnostics
The v2 engine provides rich feedback tables ("Command Analysis" and "Parsed Attributes"). If the Obsidian plugin detects a long response, it will display these diagnostics in a modal window to help troubleshoot markdown formatting or missing requirements.

### Generalized MCP
The included `mcp_server.py` now supports dynamic execution. You can use the `egeria_execute_command` tool to run any Dr. Egeria command by name, and `egeria_list_commands` to see what is currently available.

## Troubleshooting
If FastAPI returns `No updates detected. New File not created.`:
- Verify the markdown block starts with a command H1 (`# <Command Name>`).
- Check `debug_log.log` for warnings like `not found in command_list` or `Unknown command`.
- Confirm your pyegeria version includes the command handler in `pyegeria.view.md_processing_utils`.

