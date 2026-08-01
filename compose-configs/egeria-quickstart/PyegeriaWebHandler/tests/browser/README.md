# Browser/E2E tests (Phase 2 of the Portal test strategy)

For the overall strategy (why this tier exists, how it fits with `../` and
`../analyze.py`, how to interpret failures), see `../../TESTING.md`. This
file covers just the mechanics of this one tier.

Playwright tests driven from the HOST against the already-running
`quickstart-pyegeria-web` container — NOT run inside the container (see
`requirements.txt` for why: installing a full browser + system deps into a
shared, live demo container isn't worth the footprint just to run tests
that only need HTTP/browser access to it).

## Setup (once)

```bash
cd tests/browser
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m playwright install chromium
```

## Run

Requires the quickstart stack to already be running (`docker ps` should
show `quickstart-pyegeria-web` up) and reachable at `http://localhost:8800`
(override with the `PORTAL_BASE_URL` env var if different):

```bash
source .venv/bin/activate
pytest -v
```

## What's here

- `test_collections_routing.py` — golden-path regression test for the
  2026-07-31 Collections-vs-Digital-Products routing bug. Verified to
  actually catch the regression (temporarily reverted the fix, confirmed
  this test fails with a timeout waiting for the Collections section,
  restored the fix, confirmed it passes again).

## What's deliberately NOT here yet

A per-app/per-section smoke matrix (Tier B from the test strategy
discussion) — growing Tier C (targeted regression tests, one per real bug
found, like the one above) has more value per test written than an
upfront exhaustive matrix across all 15 Portal apps. Add smoke coverage
opportunistically alongside Tier C, not as a separate sweep.

Also not done: the Phase 0 frontend testability pass (semantic
roles/`data-testid` instead of `<div onClick>`, `console.error` routing for
silently-swallowed fetch failures). Turned out not to block this test —
Playwright's `get_by_text()` locators work fine against plain divs, and
auto-wait/auto-scroll sidesteps the coordinate-based fragility that showed
up when manually driving the app via a screenshot-coordinate tool earlier
in this investigation. Still worth doing for its own sake (accessibility,
plus future tests that need to distinguish structurally-similar elements),
just not gating on it.

## Debugging locator strategy

Rows/cards in this app are plain `<div>`s with no ARIA roles, so scoping a
locator to "the card/row containing X" means walking up a specific number
of `.locator("..")` ancestors to find the one with exactly one matching
button — that exact number is fragile to markup changes. If a test starts
failing with "strict mode violation: resolved to N elements" or a timeout
waiting for a button that should exist, re-derive the ancestor depth by
inspecting the live DOM (`element.evaluate(...)` walking `parentElement`
and checking `querySelectorAll('button')` at each level) rather than
guessing.
