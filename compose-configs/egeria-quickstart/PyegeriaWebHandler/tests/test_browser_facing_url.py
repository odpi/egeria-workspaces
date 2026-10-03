# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""browser_facing_url() must survive a junk X-Forwarded-Host.

A misconfigured Apache once sent `X-Forwarded-Host: i=99, localhost:8843` (an invalid
`RequestHeader set X-Forwarded-Host "%{Host}i"` -- %{..}i is mod_log_config syntax),
so tile URLs came out as http://i=99:8002/.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import demo_config  # noqa: E402


class _Request:
    def __init__(self, headers):
        self.headers = headers
        self.url = type("U", (), {"hostname": "localhost"})()


def _url(forwarded, host="laz.local:8843", configured="http://localhost:8002/"):
    headers = {"host": host}
    if forwarded is not None:
        headers["x-forwarded-host"] = forwarded
    return demo_config.browser_facing_url(configured, _Request(headers), 8002)


@pytest.mark.parametrize("forwarded,expected", [
    ("i=99, localhost:8843",  "http://localhost:8002/"),   # the old Apache bug
    ("localhost:8843",        "http://localhost:8002/"),
    ("laz.local:8843",        "http://laz.local:8002/"),
    ("i=99, laz.local:8843",  "http://laz.local:8002/"),
    ("laz.local",             "http://laz.local:8002/"),
    ("[::1]:8843",            "http://[::1]:8002/"),
    ("[2001:db8::5]",         "http://[2001:db8::5]:8002/"),
])
def test_forwarded_host_variants(forwarded, expected):
    assert _url(forwarded) == expected


def test_all_junk_falls_back_to_host_header():
    assert _url("i=99") == "http://laz.local:8002/"


def test_no_forwarded_header_uses_host_header():
    assert _url(None) == "http://laz.local:8002/"


def test_non_loopback_configured_url_is_untouched():
    assert _url("i=99", configured="http://myhost.example:9000/x") == "http://myhost.example:9000/x"
