# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""A console sink so the Portal's own info and warning log lines are visible.

pyegeria's config_logging() removes loguru's default sink and installs a console sink that prints only
what pyegeria's console_log_filter lets through at PYEGERIA_CONSOLE_LOG_LVL (ERROR by default), so every
Portal logger.info / logger.warning (failed cache refreshes, the warm-up, ...) reached only
/app/logs/pyegeria.log, never `docker logs`. This adds ONE stderr sink for the Portal's own modules:

- not pyegeria's records (its own logging stays as configured);
- not the lines pyegeria's console sink already prints, so nothing appears twice;
- not demo_reset_handler, which attaches its own narrating sink;
- at PORTAL_LOG_LEVEL (INFO by default).

Call ensure_portal_log_sink() from app startup, after pyegeria's logging is configured (its logger.remove()
would drop a sink added at import time). Idempotent.
"""
import os
import sys
from typing import Optional

from loguru import logger

_sink_id: Optional[int] = None


def _on_pyegeria_console(record) -> bool:
    """Would pyegeria's own console sink print this record? (Same level threshold and filter it uses.)"""
    try:
        from pyegeria.core.config import settings
        from pyegeria.core.logging_configuration import console_log_filter
        threshold = logger.level(settings.Logging.console_logging_level).no
        return record["level"].no >= threshold and bool(console_log_filter(record))
    except Exception:  # noqa: BLE001 -- unknown means "not printed there": show it rather than lose it
        return False


def portal_record_filter(record) -> bool:
    name = record["name"] or ""
    if name.startswith("pyegeria") or name == "demo_reset_handler":
        return False
    return not _on_pyegeria_console(record)


def ensure_portal_log_sink(sink=None) -> int:
    """Attach the Portal sink once (sink defaults to stderr; tests pass their own). Returns its id."""
    global _sink_id
    if _sink_id is not None:
        return _sink_id
    _sink_id = logger.add(
        sink or sys.stderr,
        level=os.environ.get("PORTAL_LOG_LEVEL", "INFO"),
        filter=portal_record_filter,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <7} | {name}:{line} - {message}",
    )
    return _sink_id


def remove_portal_log_sink() -> None:
    """Detach it (tests)."""
    global _sink_id
    if _sink_id is not None:
        logger.remove(_sink_id)
        _sink_id = None
