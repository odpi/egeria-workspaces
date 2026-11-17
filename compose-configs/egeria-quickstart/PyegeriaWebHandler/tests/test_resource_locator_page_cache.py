# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Resource Locator page is served with Cache-Control: no-store, like the Portal's
other pages, so a browser never keeps showing the page from before a deploy (2026-11-17:
after the Data lens deploy the owner's browser still showed Home without the tile)."""


def test_locator_page_is_not_cached(client):
    for path in ("/resource-locator", "/resource-browser"):
        r = client.get(path)
        assert r.status_code == 200
        assert "no-store" in r.headers.get("cache-control", ""), path
