# Portal test strategy

This is the master reference for how the Portal apps (the no-build React
SPAs served by `PyegeriaWebHandler`, e.g. Egeria Explorer / `type-explorer.html`)
get tested — why the strategy is shaped this way, how to run each tier, and
how to read the results. Built across three phases in response to manual
click-through testing across 15 apps / ~275 backend endpoints becoming
unsustainable.

Scope as of this writing: **`egeria-quickstart` only**. `egeria-freshstart`
has its own separate container and hasn't had this work applied to it yet —
same handlers, same bug classes are plausible there, just not yet checked.

---

## Why this shape, not another

Considered and deliberately set aside (see the design discussion this
strategy came from for the full reasoning):

- **Consumer-driven contract testing (Pact)** — solves a frontend/backend
  version-skew problem this repo doesn't have (both live in the same repo,
  deploy together).
- **Component-level unit tests / Storybook** — the frontend has no build
  step and no component boundaries (everything is one giant inline-`<script>`
  HTML file), so this isn't practical without a frontend refactor that
  wasn't in scope.
- **Mutation testing, full OpenAPI schema hardening across all ~275
  endpoints** — real, but premature relative to the ~0% coverage this
  started from; noted as follow-up, not done now.

What's actually built: three tiers plus an orchestrator, in increasing cost
order, each one solving a specific gap the tier below it can't:

| Tier | What | Why it exists |
|---|---|---|
| **1. Backend contract** (`tests/`) | pytest + Schemathesis against the live FastAPI app, in-process (`TestClient`) | Cheapest, fastest, catches handler regressions and schema/crash bugs. Can't catch frontend routing bugs — no browser involved. |
| **2. Browser/E2E** (`tests/browser/`) | Playwright, real Chromium, driven from the host against the already-running container | Catches exactly what Tier 1 can't: which tab/screen the UI actually lands on. Grown one golden-path regression test at a time (per real bug found), not as an upfront smoke matrix — higher signal per test written. |
| **3. Orchestrator/triage** (`tests/analyze.py`) | Runs Tiers 1+2, clusters failures, drafts a root-cause hypothesis (local LLM first, Claude Code escalation on low-confidence/hollow answers) | Even with 1+2 automated, someone still has to read failures and tell a real regression apart from data drift or flakiness. Zero-cost on green runs — only engages on actual failures. |

A parallel, ongoing thread: **`PYEGERIA_GAPS.md`** tracks bugs found in the
`pyegeria` library itself (not this app's code) along the way. Logging
only — nothing there gets acted on without explicit approval.

---

## How to invoke each tier

### Tier 1 — backend contract (`tests/`)

Runs **inside** the `quickstart-pyegeria-web` container (needs
`EGERIA_PLATFORM_URL`/`host.docker.internal` to resolve, and in-process
access to `pyegeria_handler.app`):

```bash
# once, to install schemathesis/pytest into the container:
docker exec quickstart-pyegeria-web pip install -r requirements-test.txt

# every run:
docker exec quickstart-pyegeria-web pytest tests/ --ignore=tests/browser -v
```

Individual files: `test_golden_anchors.py` (characterization tests against
stable Coco Pharmaceuticals seed data), `test_schema_fuzz.py` (Schemathesis
fuzzing, currently scoped to the `collections`/`projects` OpenAPI tags —
see its module docstring for how to widen it tag by tag).

### Tier 2 — browser/E2E (`tests/browser/`)

Runs from the **host**, not the container (see `tests/browser/README.md`
for why — installing a browser + system deps into a shared live demo
container isn't worth the footprint):

```bash
cd tests/browser
# once:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m playwright install chromium

# every run:
source .venv/bin/activate
pytest -v
```

Requires the quickstart stack already running and reachable at
`http://localhost:8800` (override via `PORTAL_BASE_URL`).

### Tier 3 — orchestrator/triage (`tests/analyze.py`)

Runs both tiers above and only triages if something fails:

```bash
cd tests
python3 analyze.py
```

Requires: quickstart container running (for Tier 1), `tests/browser/.venv`
already set up (for Tier 2, else it's skipped with a note), Ollama running
locally with a model pulled (`OLLAMA_MODEL` env var, default
`qwen2.5-coder:latest`) for the local-first triage pass, and the `claude`
CLI on PATH for escalation (optional — if absent, low-confidence/hollow
clusters are just flagged as such instead of escalated).

Writes `tests/TRIAGE_REPORT.md`. Both `pip install`/`playwright install`
setup steps above must have already happened at least once.

---

## How to read the results

**Tier 1/2 test output** is standard pytest — a failing test name plus a
traceback. `test_golden_anchors.py` failures need one extra judgment call:
before assuming a regression, check whether the seed data itself changed
(a content-pack update) — see that file's module docstring and
`golden_anchors.py` for the re-derivation procedure. Everything else
(schema fuzz, browser) failing means an actual bug, full stop.

**`TRIAGE_REPORT.md`** (Tier 3 output) has one section per failure cluster:

```
## Cluster: `<normalized first line of the failure message>`
- Affected tests (N): ...
- Triage source: local | claude (escalated) | claude (escalated, unstructured) | none
- Confidence: HIGH | MEDIUM | LOW | UNKNOWN
- Root cause: <hypothesis>
- Suggested fix location: <file/function, or "unknown">
```

Reading it:

- **`Triage source: local`, `Confidence: HIGH`, and an actual (non-"unknown")
  fix location** — the local model handled it end to end; still verify, but
  this is the cheap/fast path working as intended.
- **`Triage source: claude (escalated)`** — the local model either wasn't
  confident, or claimed confidence without actually pointing at a fix
  location (a real failure mode observed in practice — see `analyze.py`'s
  inline comment on the escalation trigger). Claude took a second, more
  careful pass. Same trust level as the line above once you've read it.
- **`Triage source: claude (escalated, unstructured)`** — Claude responded
  but not in the expected `CONFIDENCE:`/`ROOT_CAUSE:`/`SUGGESTED_FIX_LOCATION:`
  format; its raw response is dumped into `root_cause` verbatim. Still worth
  reading, just parse it yourself.
- **`Triage source: none`** — both the local model and Claude CLI were
  unreachable (Ollama not running, `claude` not on PATH, or both). Fall back
  to reading the raw failure detail in the collapsed `<details>` block
  yourself.
- **This is always a hypothesis, never a fix.** The script does not modify
  test assertions, source files, or mark anything as expected/resolved. A
  human reads the report and decides.

---

## Where things live

```
PyegeriaWebHandler/
├── TESTING.md                    ← this file
├── PYEGERIA_GAPS.md               tracking log for pyegeria-library issues
├── egeria_error_mapping.py        shared pyegeria-exception → HTTP status mapper
├── requirements-test.txt          Tier 1 deps (pytest, schemathesis)
└── tests/
    ├── README.md                  Tier 1 detail
    ├── conftest.py                 shared TestClient fixture
    ├── golden_anchors.py           stable seed-data fixtures (shared with Tier 2)
    ├── test_golden_anchors.py
    ├── test_schema_fuzz.py
    ├── analyze.py                  Tier 3 orchestrator
    ├── TRIAGE_REPORT.md             ← generated, gitignored
    └── browser/
        ├── README.md                Tier 2 detail, incl. locator-strategy notes
        ├── requirements.txt
        ├── conftest.py
        └── test_collections_routing.py
```

---

## Known gaps / deliberately deferred

- **Tier 1 scope** — Schemathesis only covers the `collections`/`projects`
  OpenAPI tags so far. Widen tag by tag as each area gets its own
  error-mapping pass (the same shape as `egeria_error_mapping.py`'s fix for
  these two).
- **Full `case.validate_response()` schema conformance** — turned off in
  `test_schema_fuzz.py` on purpose; surfaced a separate, legitimate finding
  (query params like `url` aren't typed with a `format`/`pattern` constraint,
  so Schemathesis considers arbitrary strings schema-valid) that's a bigger,
  separate project from "stop leaking 500s."
- **Tier 2 smoke matrix** — no per-app/per-section exhaustive smoke tier
  exists. Deliberately: growing Tier 2 one targeted regression test per real
  bug found has a better value-per-test-written ratio than an upfront
  matrix across all 15 apps.
- **Phase 0 frontend testability pass** (semantic roles/`data-testid`
  instead of `<div onClick>`, routing silently-swallowed `.catch(() => {})`
  fetch failures to `console.error`) — turned out not to block Tier 2;
  Playwright's `get_by_text()` + auto-wait/auto-scroll sidestepped the
  fragility that showed up when manually driving the app via
  screenshot-coordinates earlier. Still worth doing for its own sake
  (accessibility, plus any future test that needs to disambiguate
  structurally-identical elements) — just not gating on it.
- **`egeria-freshstart` parity** — none of Tiers 1–3 have been set up
  against the freshstart container. Same handler code, so the same bug
  classes are plausible there.
- **Tier 3 clustering** — v1 heuristic (normalized first line of the failure
  message). Good enough so far; revisit if it turns out too coarse (lumping
  unrelated bugs together) or too fine (splitting one root cause into
  several clusters) in practice.
