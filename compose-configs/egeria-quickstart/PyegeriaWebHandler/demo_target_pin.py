"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Pin the Egeria platform URL for public demo traffic (DEMO_MODE only).

Nearly every route accepts a caller-supplied `url` (query parameter or JSON
body field) naming the Egeria platform to call, and many pair it with the
shared default Egeria credentials. On the public demo that let any visitor
make the server log in to a host of their choosing — handing it the default
user id and password — and probe whatever the server can reach. The frontends
only ever send the configured platform URL, so for requests that came through
Apache (EDGE_HEADER, see demo_auth_gate.py) this middleware replaces any other
`url` value with EGERIA_PLATFORM_URL before the route sees it:

  * every `url` query parameter;
  * a top-level "url" key in a JSON object body.

One place instead of ~170 parameters across the handlers, and it covers routes
added later. Container-to-container calls (no EDGE_HEADER) are untouched.
`/dr-egeria/process` takes its URL from a nested "environment" object instead;
pyegeria_handler._apply_request_configuration ignores that in demo mode.
"""

import json
import os
from urllib.parse import parse_qsl, urlencode

from demo_auth_gate import EDGE_HEADER

# Read once at import: request handling must never be able to move it.
PINNED_URL = os.environ.get("EGERIA_PLATFORM_URL", "https://host.docker.internal:9443")

_BODY_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _pin_query(query_string: bytes) -> bytes:
    pairs = parse_qsl(query_string.decode("latin-1"), keep_blank_values=True)
    if not any(k == "url" and v != PINNED_URL for k, v in pairs):
        return query_string
    return urlencode([(k, PINNED_URL if k == "url" else v) for k, v in pairs]).encode("latin-1")


def _pin_body(body: bytes) -> bytes:
    try:
        data = json.loads(body)
    except ValueError:
        return body
    if not isinstance(data, dict) or "url" not in data or data["url"] in (None, "", PINNED_URL):
        return body
    data["url"] = PINNED_URL
    return json.dumps(data).encode("utf-8")


class DemoTargetPinMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope["headers"])
        if EDGE_HEADER not in headers:
            await self.app(scope, receive, send)
            return

        scope = dict(scope, query_string=_pin_query(scope.get("query_string", b"")))

        content_type = headers.get(b"content-type", b"").split(b";")[0].strip()
        if scope["method"] not in _BODY_METHODS or content_type != b"application/json":
            await self.app(scope, receive, send)
            return

        chunks = []
        while True:
            message = await receive()
            if message["type"] != "http.request":
                # Client went away before sending the whole body.
                await self.app(scope, receive, send)
                return
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        body = _pin_body(b"".join(chunks))

        scope["headers"] = [(k, v) for k, v in scope["headers"] if k != b"content-length"]
        scope["headers"].append((b"content-length", str(len(body)).encode("latin-1")))

        replayed = False

        async def replay():
            nonlocal replayed
            if not replayed:
                replayed = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        await self.app(scope, replay, send)
