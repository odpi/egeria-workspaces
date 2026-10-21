<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# TestGen — optional runtime for Resource Explorer comparisons

[DataKitchen DataOps TestGen](https://github.com/DataKitchen/dataops-testgen) (Apache-2.0)
profiles database columns, generates data-quality tests from the profile, and runs them.
Resource Explorer's quality slice 1 vendors seven of TestGen's test types as data and runs them
with RE's own code (trellis `DESIGN-VALUE-PROFILE-AND-QUALITY-CHECKS.md`). This runtime runs
the real TestGen against the same coco databases, so the two can be compared:

1. **Profile comparison:** TestGen's measured profile against RE's value profile, column by column.
2. **Proposed vs generated:** RE's proposed checks against the tests TestGen generates, for
   RE's slice-1 test types.
3. **Results into Egeria:** a mapping only ([EGERIA-MAPPING.md](EGERIA-MAPPING.md)); nothing
   here writes to Egeria.

**This is a comparison harness beside Resource Explorer, not part of it.** RE never calls this
TestGen: in RE's design TestGen does not run, and its test catalogue is vendored as data
(trellis `INTEGRATION-TESTGEN-RE-EGERIA.md`). This runtime exists to check that work against
the real thing.

| Piece | What it does |
|---|---|
| `docker-compose.yaml` | TestGen's engine (UI, scheduler, API) on `egeria_network`; UI `127.0.0.1:8501`, API `127.0.0.1:8531`; telemetry off |
| `examples.yaml` | One TestGen project per coco database |
| `scripts/seed_examples.py` | Creates those projects, then profiles, generates and tests (runs in the container) |
| `scripts/export_testgen.py` | Writes the latest profile, tests and results as neutral JSON (runs in the container) |
| `compare/compare_re_testgen.py` | Joins that JSON with RE's registry; writes a report and CSVs (runs on the host) |

## What the open-source TestGen allows

Found in the 5.134.0 code, and the reason `seed_examples.py` exists:

- **The UI cannot create a project.** `setup-system-db` creates one project from `PROJECT_KEY`.
  No screen, REST endpoint, MCP tool or CLI command creates another.
- **The UI shows only a project's first connection.** The Connections page renders
  `connections[0]`. The data model, the engine, the API and the project switcher all handle
  several projects and connections.
- So this runtime uses **one project per database, with one connection each**, created through
  TestGen's own models (the password is encrypted with your `TG_DECRYPT_*` secrets, as the UI
  would). Each schema becomes a table group with a Standard test suite.
- Every permission is granted to every user in the open-source build (`RBACProvider`).

## Ports

| Host | Container | |
|---|---|---|
| `127.0.0.1:8501` | 8501 | TestGen UI |
| `127.0.0.1:8531` | 8530 | TestGen REST API and MCP (`/mcp`) |

8530 on the host is left free for a separately run TestGen. Nothing binds beyond localhost.

## Setup

Shared-infra must be up (`egeria-shared-postgres` on 5442, `egeria_network`).

### 1. Metadata database

TestGen keeps its own metadata in a `testgen` database on the shared Postgres, owned by a
`testgen_admin` role. `compose-configs/shared-infra/docker-entrypoint-initdb.d/init_testgen.sh` creates both,
but only when the shared Postgres volume is first initialised, and without a password.

**On an existing shared Postgres**, run this once. **It is a write to the shared Postgres, so
tell the other sessions first** (a peer round):

```bash
docker exec -i egeria-shared-postgres psql -U postgres -p 5442 -v ON_ERROR_STOP=1 \
     -v tg_password="$(grep '^TESTGEN_DB_PASSWORD=' .env | cut -d= -f2-)" <<'EOSQL'
SELECT NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'testgen_admin') AS need_role \gset
\if :need_role
    CREATE ROLE testgen_admin WITH LOGIN;
\endif
ALTER ROLE testgen_admin WITH PASSWORD :'tg_password';
SELECT 'CREATE DATABASE testgen OWNER testgen_admin'
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testgen') \gexec
EOSQL
```

On a fresh volume, set the password the same way, with only the `ALTER ROLE` line.

### 2. Environment

```bash
cp .env.example .env
```

Fill in `TESTGEN_PASSWORD`, `TESTGEN_DB_PASSWORD`, and the three TestGen secrets
(`openssl rand -hex 32` each). Keep the `TG_DECRYPT_*` pair stable: changing it makes the
stored connection passwords unreadable.

### 3. Create TestGen's schema, start it, seed the examples

```bash
docker compose --env-file .env run --rm engine setup-system-db --yes
docker compose --env-file .env up -d
docker compose --env-file .env exec engine python /examples/scripts/seed_examples.py
```

The seeder:

- discovers each database's schemas (the ones the connection account can use, less
  `exclude_schemas`), and creates the project, connection, table groups and suites;
- adds the UI user to each project, so the projects appear in the project switcher;
- runs `run-profile`, `run-test-generation` and `run-tests` for each table group. These
  queue jobs for the scheduler in the container and wait for them.

It is re-runnable: run it again after new schemas appear. Options: `--project CODE`
(repeatable), `--setup-only`, `--skip-tests`. A database it cannot reach is reported and
counted as a failure, never seeded as empty.

**It is slow on the full coco set.** On 2026-10-21 `COCO_DATA_HUB` alone took about 40 minutes,
and the other four together about 2.5 hours. Start with `--project COCO_DATA_HUB`.

**Schema names over 50 characters are skipped.** TestGen 5.134.0 stores schema names in
`VARCHAR(50)` columns (`profiling_runs`, `test_results` and others), so it cannot profile such a
schema at all. `subscription_staging` has many of them, for example
`coco_winch_mfg_control__personalised_manufacturing_schedule` (59). The seeder names each schema
it skips. Table groups created for them by an earlier seeder version are left in place, and the
export marks them `schema_name_too_long`.

`setup-system-db` also creates the `DEFAULT` project, with no connection. Ignore it.

## Comparing with Resource Explorer

```bash
mkdir -p out
docker compose --env-file .env exec -T engine python /examples/scripts/export_testgen.py \
    > out/testgen-export.json

uv run --no-project --with sqlalchemy --with "psycopg[binary]" compare/compare_re_testgen.py \
    --export out/testgen-export.json \
    --re-registry "postgresql+psycopg://egeria_advisor:<password>@localhost:5442/egeria_advisor?options=-csearch_path%3Dresource_explorer" \
    --out out/compare
```

`--re-registry` takes any SQLAlchemy URL, including `sqlite:///…/data/registry.db` for a
native RE. Name the driver (`postgresql+psycopg://`): SQLAlchemy 2.1 maps a bare
`postgresql://` to psycopg 3, so it fails if only psycopg2 is installed. `--no-project` keeps
`uv` from resolving the repository's own `pyproject.toml`. The script only reads. It writes `out/compare/report.md`, plus:

- `profile.csv`: per column, both sides' `record_ct`, `value_ct`, `distinct_value_ct`, …, and
  which measures differ;
- `checks.csv`: per `check_key`, whether RE proposed it, TestGen generated it, or both, with
  each side's parameters;
- `results.csv`: per `check_key`, each side's status, measure and threshold, and whether they
  agree.

RE's side comes from its quality slice 1 tables (`database_value_profiles`,
`database_quality_proposals`, `database_quality_results`). **They are on the unmerged trellis
branch `re/value-profile-quality-checks`**, so their names can still change. When they are
absent the report says so, rather than showing zeros.

What to expect:

- **`Row_Ct_Pct` is always `re_only`.** TestGen never generates it (it is manual-only there).
  RE proposes it from its row-count baseline.
- **Recency is not compared.** RE moved it to slice 2.
- **TestGen generates many more test types.** Only RE's seven are compared; pass `--types`
  to widen the comparison.
- **Counts can differ legitimately** when the two ran at different times against changing
  data. Compare runs made close together.

`out/` is git-ignored.

## Notes

- **Image pin.** `datakitchen/dataops-testgen:v5.134.0` is the release RE's vendored
  catalogue was copied from (commit `3606859c`). Move both together.
- **The CLI run commands print a deprecation notice** in 5.134.0 ("use the TestGen API or MCP
  server instead"). They still work, and the seeder uses them. If a later release removes
  them, switch the seeder to the REST API's run endpoints.
- **Release check.** TestGen checks Docker Hub for a newer release, and that cannot be turned
  off (`TG_RELEASE_CHECK` only chooses PyPI or Docker Hub). Mixpanel telemetry
  (`TG_ANALYTICS`) and the feedback popup are off.
- **Licence and trademark.** TestGen is Apache-2.0 with DataKitchen's NOTICE. The licence
  grants no trademark, so present work built on it under its own name.

## Verified

**Live run, 2026-10-21**, with the `v5.134.0` image against the shared Postgres and the five coco
databases:

- `setup-system-db` succeeded; the UI (127.0.0.1:8501) and API (127.0.0.1:8531) were
  localhost-only;
- creating the role and database changed no existing role or database (a before/after diff of
  `pg_authid` and `pg_database` showed only the two additions);
- all five projects were seeded and tested. The only failures were the 24 `subscription_staging`
  schemas with names over 50 characters, which the seeder now skips;
- the export (20.5 MB) and the comparison ran; RE's side reported slice 1 as not deployed, as
  expected.

Earlier, on 2026-10-20, in a sandbox with **pip-installed TestGen 5.134.0 against
PostgreSQL 16**:

- `init_testgen.sh` creates the role and database, is idempotent, and handles a password with
  a quote;
- `setup-system-db` works with the pre-created database and a role without `CREATEDB`;
- the seeder creates the projects, memberships, connections, table groups and suites, skips a
  schema the account cannot use, reports missing databases as failures, and a second run
  changes nothing;
- profiling, generation and test runs complete through the scheduler;
- the export and the comparison run end to end (RE's side against a fixture built from the
  slice-1 DDL, since RE's slice 1 is not merged).
