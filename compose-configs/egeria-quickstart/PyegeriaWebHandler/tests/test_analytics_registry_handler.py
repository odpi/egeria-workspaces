"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

analytics_registry_handler._serialize: a function's demo report spec is found
whether pyegeria's demo specs name it by registered name (6.2.18+) or by
dotted path (6.2.17 and earlier).
"""

from types import SimpleNamespace

import analytics_registry_handler as h

_SPEC = SimpleNamespace(function="pyegeria.view.overview_metrics.governed_coverage", params=[])


def test_demo_spec_found_by_registered_name():
    s = h._serialize("governed_coverage", _SPEC, {"governed_coverage": "Analytic Demo - Governed Coverage"})
    assert s["demoReportSpec"] == "Analytic Demo - Governed Coverage"


def test_demo_spec_found_by_dotted_path():
    s = h._serialize("governed_coverage", _SPEC, {_SPEC.function: "Analytic Demo - Governed Coverage"})
    assert s["demoReportSpec"] == "Analytic Demo - Governed Coverage"


def test_no_demo_spec_is_none():
    assert h._serialize("governed_coverage", _SPEC, {})["demoReportSpec"] is None
