<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Pyegeria Web Handler
The Pyegeria Web Handler is a python module that provides a web handler for the pyegeria command line interface. It is
used to execute Dr.Egeria commands from anything that can make a REST call - and that shares the same filesystem as
the Egeria runtime.

## Maintenance Notes
A version of dr_egeria_md.py has been copied to the root of the pyegeria-web-handler directory rather than 
just calling it from the md_processing module of pyegeria. This facilitated building. However, what this does mean is that after
significant change (generally additions) to the Dr.Egeria md_processing module, we need to copy the new version
of dr_egeria_md.py into the root of the pyegeria-web-handler directory and make a few checks and changes.

Check that the imports are correct. The name of the main routine is process_markdown_file. So if this changes in the
future, you will need to change either pyegeria_handler or dr_egeria_md.py to match. Other than that is should be a drop
in replacement.

## Command Catalog Notes
`md_processing/__init__.py` now re-exports command handlers and command lists from
`pyegeria.view.md_processing_utils` when available, and only falls back to local stubs when unavailable.
This prevents valid commands from being silently skipped because local constants were empty.

`dr_egeria_md.py` also attempts handler dispatch even when a command is missing from `command_list` and logs a warning.

## Troubleshooting
If FastAPI returns `No updates detected. New File not created.`:
- Verify the markdown block starts with a command H1 (`# <Command Name>`).
- Check `debug_log.log` for warnings like `not found in command_list` or `Unknown command`.
- Confirm your pyegeria version includes the command handler in `pyegeria.view.md_processing_utils`.

