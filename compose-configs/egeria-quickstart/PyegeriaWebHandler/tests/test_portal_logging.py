"""portal_logging: the Portal's info/warning lines reach a sink; pyegeria's do not; nothing appears twice."""
import io, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from loguru import logger  # noqa: E402

import portal_logging as pl  # noqa: E402


@pytest.fixture
def sink(monkeypatch):
    pl.remove_portal_log_sink()
    buf = io.StringIO()
    pl.ensure_portal_log_sink(buf)
    yield buf
    pl.remove_portal_log_sink()


def _log(name, level, msg):
    logger.patch(lambda r: r.update(name=name)).log(level, msg)


def test_portal_info_and_warning_reach_the_sink_pyegeria_info_does_not(sink):
    _log("collections_handler", "INFO", "portal-info")
    _log("collections_handler", "WARNING", "portal-warning")
    _log("pyegeria.view.overview_metrics", "INFO", "library-info")
    out = sink.getvalue()
    assert "portal-info" in out and "portal-warning" in out and "library-info" not in out


def test_a_line_pyegeria_console_already_prints_is_not_printed_twice(sink, monkeypatch):
    monkeypatch.setattr(pl, "_on_pyegeria_console", lambda record: record["level"].name == "ERROR")
    _log("collections_handler", "ERROR", "already-on-console")
    _log("collections_handler", "WARNING", "only-here")
    out = sink.getvalue()
    assert "already-on-console" not in out and "only-here" in out


def test_with_pyegeria_real_predicate_each_line_appears_exactly_once(sink):
    # Whatever pyegeria's own console settings are here (its level and filter come from its settings, and
    # differ between environments), a Portal line shows on THIS sink exactly when pyegeria's console would
    # not print it: never on both, never on neither.
    seen = []
    probe = logger.add(lambda m: seen.append(m.record["message"]), level="TRACE",
                       filter=lambda r: r["message"].startswith("probe-"))
    try:
        for level in ("INFO", "WARNING", "ERROR"):
            _log("collections_handler", level, "probe-" + level)
    finally:
        logger.remove(probe)
    out = sink.getvalue()
    for level in ("INFO", "WARNING", "ERROR"):
        rec = {"name": "collections_handler", "module": "test_portal_logging", "level": logger.level(level)}
        assert ("probe-" + level in out) == (not pl._on_pyegeria_console(rec)), level
    assert "probe-INFO" in out            # below pyegeria's console level (ERROR by default): always visible here


def test_demo_reset_keeps_its_own_sink_only(sink):
    _log("demo_reset_handler", "INFO", "reset-line")
    assert sink.getvalue() == ""


def test_attached_once_and_by_the_app_lifespan():
    pl.remove_portal_log_sink()
    a = pl.ensure_portal_log_sink(io.StringIO()); b = pl.ensure_portal_log_sink(io.StringIO())
    pl.remove_portal_log_sink()
    assert a == b
    src = (Path(__file__).resolve().parent.parent / "pyegeria_handler.py").read_text()
    assert "ensure_portal_log_sink()" in src
