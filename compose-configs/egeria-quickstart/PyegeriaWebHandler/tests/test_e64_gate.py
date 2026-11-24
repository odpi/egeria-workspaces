"""The Egeria 6.4 version gate as the Explorer cards use it (egeria_6_4_support).

pyegeria's gate (pyegeria/core/egeria_6_4_gate.py) is not in a released pyegeria yet, so the support
module imports it when it is there and otherwise uses its own copy. Both must give the same answers and
the same words. tests/fixtures/egeria_6_4_gate_answers.json holds the answers of the real module (egeria-
python release/next-6.4 5bf2a53e), and each case runs on whichever gate is installed AND on the copy.
"""
import asyncio
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402

import egeria_6_4_support as installed  # noqa: E402
from e64_fixtures import ABOUT_6_3, ABOUT_6_4, FakeExplorer, client_error  # noqa: E402

ANSWERS = json.loads((Path(__file__).resolve().parent / "fixtures" / "egeria_6_4_gate_answers.json").read_text())


@pytest.fixture(scope="module")
def vendored():
    """The support module loaded as if pyegeria had no egeria_6_4_gate (the released 6.3.x case)."""
    saved = sys.modules.get("pyegeria.core.egeria_6_4_gate", "absent")
    sys.modules["pyegeria.core.egeria_6_4_gate"] = None   # makes the import raise ImportError
    try:
        spec = importlib.util.spec_from_file_location("egeria_6_4_support_vendored", installed.__file__)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        if saved == "absent":
            del sys.modules["pyegeria.core.egeria_6_4_gate"]
        else:
            sys.modules["pyegeria.core.egeria_6_4_gate"] = saved
    assert mod.GATE_SOURCE == "vendored"
    return mod


@pytest.fixture(params=["installed", "vendored"])
def gate(request, vendored):
    mod = installed if request.param == "installed" else vendored
    mod.clear_cache()
    yield mod
    mod.clear_cache()


@pytest.mark.parametrize("case", ANSWERS["carries_6_4"], ids=lambda c: json.dumps(c["about"])[:60])
def test_version_answers_match_pyegeria(gate, case):
    assert list(gate.carries_6_4(case["about"])) == case["answer"]


@pytest.mark.parametrize("case", ANSWERS["needs_6_4_words"], ids=lambda c: c["args"][0])
def test_words_match_pyegeria(gate, case):
    assert gate.needs_6_4_words(*case["args"]) == case["words"]


def test_laz_build_carries_the_additions(gate):
    # laz's /api/about on 2026-11-21: 6.4-SNAPSHOT built 19:52:59Z, after the #9463 merge (19:51:36Z)
    assert gate.carries_6_4(ABOUT_6_4)[0] is True
    assert gate.carries_6_4(ABOUT_6_3)[0] is False


def test_bare_404_is_a_missing_endpoint_but_other_errors_are_not(gate):
    assert gate.is_missing_6_4_endpoint(client_error(404)) is True
    assert gate.is_missing_6_4_endpoint(client_error(400)) is False
    assert gate.is_missing_6_4_endpoint(RuntimeError("404")) is False


def test_status_reads_about_once_and_unreadable_is_unknown_not_no(gate):
    fake = FakeExplorer(about=ABOUT_6_3)
    assert asyncio.run(gate.async_egeria_6_4_status(fake)) == (False, "6.3", fake.platform_url)
    fake.about = ABOUT_6_4                           # cached: the platform is asked once per TTL
    assert asyncio.run(gate.async_egeria_6_4_status(fake))[0] is False
    gate.clear_cache()
    broken = FakeExplorer(about=RuntimeError("connection refused"), url="https://down.test:9443")
    assert asyncio.run(gate.async_egeria_6_4_status(broken)) == (None, "", "https://down.test:9443")


def test_the_gate_source_is_reported():
    assert installed.GATE_SOURCE in ("pyegeria", "vendored")
