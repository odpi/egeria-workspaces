# pyegeria gaps and issues

Running log of gaps/rough edges found *in the `pyegeria` library itself*
(not this app's handler code) while building out the Portal test strategy.
Entries here are candidates for upstream fixes — **do not act on any of
these against the pyegeria repo without explicit approval**; this file is
the tracking mechanism, not an authorization to patch.

Status values: `logged` (found, not yet reviewed) · `approved` (owner said
fix it) · `fixed-upstream` (patched in pyegeria) · `wont-fix` (owner decided
against it, reason noted).

---

## 1. `PyegeriaAPIException` is a catch-all; typed subclasses exist but aren't raised for it

**Status:** logged (2026-07-31)

**What:** `pyegeria.core._exceptions` defines `PyegeriaNotFoundException` and
`PyegeriaUnauthorizedException` as distinct exception classes, but
`_base_server_client.py`'s `_async_make_request` never actually raises them.
Every "Egeria wrapped an error in an HTTP 200 response" case (Egeria's own
`relatedHTTPCode` pattern — auth failures, not-found, etc.) raises the
generic `PyegeriaAPIException` instead, regardless of what `relatedHTTPCode`
says. Callers have to inspect `.related_http_code` at runtime to tell a 401
from a 404 from a 500-from-Egeria.

**Where seen:** `egeria_error_mapping.py` (this repo) — had to build the
whole mapper around `.related_http_code`/`.response_code` inspection instead
of a clean `except PyegeriaNotFoundException` / `except
PyegeriaUnauthorizedException`, specifically because those classes are
defined-but-dead.

**Candidate fix:** in `_async_make_request`, when constructing
`PyegeriaAPIException`, branch on `related_http_code` and raise
`PyegeriaNotFoundException`/`PyegeriaUnauthorizedException` (etc.) instead
of the generic class where a specific one already exists.

---

## 2. `httpx.InvalidURL` isn't wrapped

**Status:** logged (2026-07-31)

**What:** A non-printable character in a caller-supplied `server`/`user_id`
param (reaching pyegeria's client construction) causes a raw
`httpx.InvalidURL` to propagate — not one of pyegeria's own exception types.
Every other client-construction failure path in `_base_server_client.py`
wraps things into `PyegeriaConnectionException`/`PyegeriaInvalidParameterException`;
this one specific path doesn't.

**Where seen:** Schemathesis fuzzing `server`/`user_id` query params on
`/api/collections/*` and `/api/projects/*` (this repo's
`tests/test_schema_fuzz.py`) surfaced it directly.

**Candidate fix:** catch `httpx.InvalidURL` in the same place other
constructor validation errors get wrapped, and re-raise as
`PyegeriaInvalidParameterException`.

---

## 3. Malformed `as_of_time` reaches pydantic as a raw `ValidationError`

**Status:** logged (2026-07-31)

**What:** Passing a non-datetime string (e.g. the literal `"null"`) as
`as_of_time` propagates all the way to a `pydantic_core.ValidationError`
when pyegeria builds the internal `SearchStringRequestBody`/`GetRequestBody`
model — not caught or translated by pyegeria itself.

**Where seen:** same Schemathesis run as #2, fuzzing the `as_of_time` query
param on `/api/projects*`.

**Candidate fix:** validate/parse `as_of_time` at the pyegeria client-method
boundary (before building the request body) and raise
`PyegeriaInvalidParameterException` on failure, consistent with how other
malformed inputs are handled elsewhere in the same file.

---

## 4. `pyegeria.core.mcp_server` is pinned to a stale `mcp` package API, can't be imported, and this repo forked it instead of extending it

**Status:** logged (2026-07-31) — owner will handle from the egeria-python repo directly.

**What:** `pyegeria/core/mcp_server.py` does
`from mcp.server.fastmcp.exceptions import ValidationError` and
`from mcp.server.fastmcp import FastMCP`, both of which come from an older
`mcp` package API. This container runs `mcp>=2.0.0`, where `FastMCP` was
renamed/relocated to `mcp.server.mcpserver.MCPServer`. As a result,
`pyegeria.core.mcp_server` **cannot be imported at all** in this
environment:

```
ModuleNotFoundError: No module named 'mcp.server.fastmcp'
```

Consequence: this repo's own `PyegeriaWebHandler/mcp_server.py` had to be
written against the new `mcp` API from scratch (`from mcp.server.mcpserver
import MCPServer, Context`) rather than importing and extending pyegeria's
server object with its own Dr.Egeria-specific tools. Its four report-facing
tools (`list_reports`, `find_report_specs`, `describe_report`, `run_report`)
don't reimplement report logic — they call straight into
`pyegeria.core.mcp_adapter`, the same module pyegeria's own (broken) server
uses — but the `MCPServer` construction and `@server.tool()` registration
for those four tools is now duplicated across two files instead of living
in one. That's a standing drift risk: if `mcp_adapter`'s signatures or
pyegeria's own tool registration change, nothing enforces this repo's
hand-written wrappers staying in sync.

**Where seen:** direct inspection of
`/usr/local/lib/python3.12/site-packages/pyegeria/core/mcp_server.py`
inside `quickstart-pyegeria-web`, prompted by comparing it against this
repo's local `mcp_server.py` after fixing an unrelated bug in the latter
(module-level `EGERIA_ROOT_PATH`/`EGERIA_INBOX_PATH` constants captured at
import time — see `mcp_server.py`'s inline comment, 2026-07-31).

**Candidate fix:** update `pyegeria/core/mcp_server.py` to the current `mcp`
package API (`mcp.server.mcpserver.MCPServer` in place of
`mcp.server.fastmcp.FastMCP`, and whatever the corresponding
`ValidationError`/`Context` import paths are now). Once that's done, this
repo's `mcp_server.py` could import pyegeria's server object directly and
register only the Dr.Egeria-specific tools onto it, eliminating the
duplicated `MCPServer` construction and the four hand-wired report-tool
wrappers.

---

## 5. `get_collection_members` silently drops non-Collection members when `body` is omitted

**Status:** logged (2026-07-31) — owner will handle from the egeria-python repo directly.

**What:** `pyegeria/core/_server_client.py`'s `_async_get_results_body_request`
builds a default request body when the caller passes `body=None`, and that
default hardcodes `metadataElementTypeName=_type` (here `_type="Collection"`,
from `CollectionManager.get_collection_members`'s internal call). That field
filters the **returned members**, not the collection being queried — so any
collection whose members aren't themselves `Collection`-typed (e.g. a
`WorkItemList` whose members are `Project` entities) comes back with an
empty member list, even though the collection genuinely has members.

**Where seen:** user ran the "Collection Members" report (Reports screen,
Egeria Explorer) against guid `0affb580-fa81-4d00-9438-b26faf11845d` (the
same `WorkItemList` used as a golden anchor throughout this test-strategy
work, confirmed via `GET /api/collections/{guid}` to have exactly 5
`Project`-typed members) and got an empty list. Traced to
`pyegeria/view/base_report_formats.py:2058-2072`'s `"Collection Members"`
`FormatSet` — its `ActionParameter` doesn't list `body` in
`optional_params`, so `format_set_executor.py` never passes one, always
hitting the default-body branch. By contrast, this repo's own
`collections_handler.py:204-209` passes an explicit
`body={"class": "ResultsRequestBody", "graphQueryDepth": 0}` (no
`metadataElementTypeName` key) for the same underlying call, which is why
`/api/collections/{guid}` returns the correct 5 members for this exact
guid.

**Candidate fix:** either (a) stop hardcoding `metadataElementTypeName=_type`
in the default-body branch of `_async_get_results_body_request` — a
collection's *members* aren't guaranteed to share the collection's own
type — or (b) add `"body"` to the `"Collection Members"` FormatSet's
`optional_params`/`spec_params` in `base_report_formats.py` so callers (like
the Reports screen) can override the default and get unfiltered members,
matching what `collections_handler.py` already does correctly.

---

## 6. `Analytic Parameters`/`Report Parameters` stringify every value, breaking list-valued params (e.g. `type_map`)

**Status:** fixed-upstream (2026-08-01) — full write-up (repro, exact stack
trace, fix, live verification) is in egeria-python's `PYEGERIA_ISSUES.md`
(ISSUE-20), the canonical tracker; this entry is just a pointer so it's
discoverable from this app's own gaps file too. **Not yet in a published
pyegeria release** — this repo's `requirements.txt` is still pinned to
`6.0.17.8`, which predates the fix; needs a version bump once the next
pyegeria release goes out.

**What:** `md_processing/v2/report.py`'s `_report_additional_properties()`
does `str(v)` on every `Analytic Parameters`/`Report Parameters` value
before JSON-encoding the whole dict. A scalar value (`type_name: Project`)
survives that fine; a value that's meant to be a list (`counts_by_type`'s
`type_map: [["Projects", "Project"], ["Terms", "GlossaryTerm"]]`) gets
double-encoded — stored as a JSON string of the list's text, not a real
JSON array — so it comes back out as a Python `str`, and the analytic
function crashes trying to unpack it (`not enough values to unpack`).

**Where seen:** building the Local Dashboards sample's Projects/Terms
analytic-function demo — worked around by sticking to scalar params only
(`count_elements(type_name=...)`) instead of `counts_by_type`'s list param.

---

*(Add new entries above this line as they're found. Keep the format:
status, what, where seen, candidate fix — so entries are self-contained
enough to hand to whoever eventually reviews/fixes them upstream.)*
