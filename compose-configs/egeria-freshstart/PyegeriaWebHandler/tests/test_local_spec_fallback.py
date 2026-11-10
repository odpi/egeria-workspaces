"""The workspace-local "Analytic - Generic Metric Trend" spec is registered only while the EGERIA
tier does not hold that label (report_specs_handler.register_local_specs). No Egeria call is made."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import report_specs_handler as rsh  # noqa: E402
from pyegeria.view import base_report_formats as brf  # noqa: E402
from pyegeria.view import egeria_spec_cache as esc  # noqa: E402
from pyegeria.view._output_format_models import FormatSetDict  # noqa: E402

LABEL = "Analytic - Generic Metric Trend"


@pytest.fixture(autouse=True)
def _restore(monkeypatch):
    yield
    monkeypatch.undo()
    brf.unregister_report_spec(LABEL)
    rsh.register_local_specs()


def test_egeria_lacks_the_label_local_copy_registered(monkeypatch):
    monkeypatch.setattr(esc, "egeria_tier", lambda force=False: FormatSetDict())
    brf.unregister_report_spec(LABEL)
    assert rsh.register_local_specs() == [LABEL]
    assert LABEL in brf._RUNTIME_REPORT_FORMATS.keys()
    assert brf.lookup_report_spec(LABEL)[1] == "local"


def test_egeria_holds_the_label_no_local_copy(monkeypatch):
    tier = FormatSetDict({LABEL: rsh._local_specs()[LABEL]})
    monkeypatch.setattr(esc, "egeria_tier", lambda force=False: tier)
    monkeypatch.setattr(brf, "_egeria_tier", lambda: tier)
    brf.unregister_report_spec(LABEL)
    assert rsh.register_local_specs() == []
    assert LABEL not in brf._RUNTIME_REPORT_FORMATS.keys()
    assert brf.lookup_report_spec(LABEL)[1] == "egeria"


def test_tier_unavailable_registers_local_copy(monkeypatch):
    def boom(force=False):
        raise OSError("cache dir unreadable")
    monkeypatch.setattr(esc, "egeria_tier", boom)
    brf.unregister_report_spec(LABEL)
    assert rsh.register_local_specs() == [LABEL]
