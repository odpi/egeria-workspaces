# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-35 (Dan's owner test, 2026-11-17): a lens with "2026" was saved 2026-01-01 09:04 → 2026-12-31
09:05, the time of day of the save, so a resource whose data starts at 00:00 on 1 January was
counted outside. A year, month or day now means the whole of it: a start is its first instant,
an end its last (…23:59:59.999Z), because the lens overlap test compares ends inclusively.
Shared by The Catalog's Data scope editor and the Locator's lens form (one server path)."""
import pytest

import data_scope_handler as ds
import resource_locator_lens_handler as lens
from test_data_scope import _DATA_SCOPE_63

_GROUPS = ds._dimensions(_DATA_SCOPE_63)


@pytest.mark.parametrize("value,role,expected", [
    ("2026", "start", "2026-01-01T00:00:00Z"),
    ("2026", "end", "2026-12-31T23:59:59.999Z"),
    ("2026-02", "end", "2026-02-28T23:59:59.999Z"),
    ("2028-02", "end", "2028-02-29T23:59:59.999Z"),
    ("2026-12", "end", "2026-12-31T23:59:59.999Z"),
    ("2026-03", "start", "2026-03-01T00:00:00Z"),
    ("2026-03-14", "start", "2026-03-14T00:00:00Z"),
    ("2026-03-14", "end", "2026-03-14T23:59:59.999Z"),
    ("2026-3-4", "end", "2026-03-04T23:59:59.999Z"),
    ("2026-03-14 09:30", "end", "2026-03-14T09:30:00Z"),       # a typed time is kept as given
    ("2026-03-14T09:30:00+02:00", "start", "2026-03-14T07:30:00Z"),
])
def test_a_year_month_or_day_means_the_whole_of_it(value, role, expected):
    assert ds._to_iso(value, role) == expected


def test_a_day_that_does_not_exist_is_a_problem_not_a_write():
    props, problems = ds._clean_values({"dataCollectionStartTime": "2026-02-30"}, _GROUPS)
    assert problems and "dataCollectionStartTime" in problems[0] and props == {}


def test_the_form_roles_decide_start_and_end():
    props, problems = ds._clean_values({"dataCollectionStartTime": "2026", "dataCollectionEndTime": "2026"}, _GROUPS)
    assert problems == []
    assert props == {"dataCollectionStartTime": "2026-01-01T00:00:00Z", "dataCollectionEndTime": "2026-12-31T23:59:59.999Z"}


def test_po35_a_resource_starting_at_midnight_on_1_january_is_inside_a_2026_lens():
    lens_scope, _ = ds._clean_values({"dataCollectionStartTime": "2026", "dataCollectionEndTime": "2026"}, _GROUPS)
    def outcome(start, end):
        return lens._lens_match(lens_scope, {"dataCollectionStartTime": start, "dataCollectionEndTime": end})["outcome"]
    assert outcome("2026-01-01T00:00:00.000+00:00", "2026-01-01T00:00:00.000+00:00") == "inside"
    assert outcome("2026-12-31T23:59:59.000+00:00", "2027-03-01T00:00:00.000+00:00") == "inside"
    assert outcome("2025-01-01T00:00:00.000+00:00", "2025-12-31T23:59:59.000+00:00") == "outside"
    assert outcome("2027-01-01T00:00:00.000+00:00", "2027-06-30T00:00:00.000+00:00") == "outside"
