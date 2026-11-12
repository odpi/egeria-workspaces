<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Upgrading or resetting the quickstart Egeria

`compose-configs/egeria-quickstart/bin/egeria-upgrade-reset` moves the quickstart to a new Egeria
platform image, clears its metadata store if you ask it to, and checks the result. It runs on the
**host** only: it needs the Docker CLI and the shared Postgres superuser (through `docker exec`),
which no container has, and which the Portal must never have. It replaces the hand procedure used on
2026-11-11; that night's reseed notes are history now.

It works in two halves. **`plan`** reads the current state and changes nothing. **`apply`** runs the
plan's steps in order, records each one with its evidence, and stops at the first failure. Run it
again to resume at the first step that is not done.

```bash
cd compose-configs/egeria-quickstart/bin
./egeria-upgrade-reset plan --latest                 # newest odpi/egeria-platform:latest, and clear the store
./egeria-upgrade-reset plan --digest sha256:<digest> # a chosen platform build
./egeria-upgrade-reset plan --no-clear               # rebuild/upgrade only; keep the metadata store
./egeria-upgrade-reset apply --plan ../../../runtime-volumes/egeria-resets/<UTC> --dry-run   # list the steps; run nothing
./egeria-upgrade-reset apply --plan ../../../runtime-volumes/egeria-resets/<UTC>
./egeria-upgrade-reset apply --plan … --personas skip    # in the background: answer verify's persona check up front
./egeria-upgrade-reset status --plan …                # each step's state
./egeria-upgrade-reset record --plan …                # write the Portal's reset row now (after a failed run)
./egeria-upgrade-reset infra-check [--record] [--json] [--log FILE] # shared-infra health; read-only, restarts nothing
```

`plan` writes `runtime-volumes/egeria-resets/<UTC>/plan.json` and `state.json` (git-ignored, with the
backup). It works on the checkout the running platform container was started from, which it reads
from the container's compose labels, so the Dockerfile, the secrets and the logs are that checkout's.
It prints that folder and the CLI's own checkout, and **refuses if they differ** (run the CLI from the
deployment's checkout, or pass `--allow-other-checkout` to mix them on purpose). It also prints:

- the pinned and the target image digest, and the running image;
- the database's size;
- Docker's free disk;
- the Resource Explorer (8813) and Egeria Advisor (8880) processes it will stop, and the launcher
  script that will restart each (or that none is usable, so a person must);
- the number of classification types the platform reports now (the baseline verify compares with);
- the secrets accounts that will be added, removed or changed, **by name only**.

Anything that would stop the run is listed as a **BLOCKER**: less than 15 GB free, or an RE/EA process
it does not know. `apply` refuses a plan with blockers, and refuses when the running image, the
database's size class or the Dockerfile pin has changed since the plan. Make a new plan then.

## The steps

| Step | What it does | Why |
|---|---|---|
| `disk-check` | Needs at least 15 GB free on the Docker VM (read inside the running Postgres container) | 2026-11-04: an image build filled the disk and Postgres stopped writing |
| `repin` | Pins `Dockerfile-egeria-platform`'s `FROM` to the target digest and prints the diff | The image must be reproducible and reviewable |
| `build` | Tags the current image `egeria-quickstart-platform:rollback-<UTC>`, then builds | Rollback: `docker tag …:rollback-<UTC> egeria-quickstart-platform:local` and recreate |
| `freeze-writers` | Stops RE on 8813 and EA on 8880 (their launcher process; its command line and folder are kept as evidence), and refuses if any other RE/EA process runs | Nothing may write to Egeria while it is cleared. Owner: freeze EA with RE, "Yes, with RE (Recommended)". The Portal's heal needs no pause: while Egeria is down its canary check cannot reach it, and an unreachable check never heals |
| `stop-platform` | `docker stop quickstart-egeria-main` | |
| `backup` | `pg_dump egeria \| gzip`, then a full gzip read, the `-- PostgreSQL database dump complete` marker, the size and sha256 | A truncated backup is worse than none: nothing goes on unless every check passes |
| `clear` | **Checkpoint:** type the database name. Then `compose-configs/shared-infra/reset-egeria-db.sql`: `DROP DATABASE … WITH (FORCE)`, `CREATE`, `GRANT ALL … TO egeria_admin, egeria_user` | The same SQL `reset-egeria-db.sh` uses: one copy |
| `secrets-sync` | While the platform is stopped: copies `compose-configs/egeria-quickstart/secrets/*.omsecrets` into `runtime-volumes/quickstart-platform-data/secrets` in place. Prints accounts added, removed or changed **by name only**. Files that are not in the compose secrets (e.g. `resource-explorer.omsecrets`) are kept | New accounts (such as `olpgpubnpa`) reach the platform; a value never reaches a terminal or a log. Done **before** the recreate so the new container mounts the final files |
| `recreate` | `docker compose … up -d --no-deps --force-recreate egeria-main`, checks the running image is the one just built, then checks the container sees the same secrets files as the host and restarts it **once** if its bind mount is stale | **Never `docker start`**: on 2026-11-11, `reset-egeria-db.sh` restarted the old container, which kept the old image. The one restart happens while Egeria is still starting, before the Portal's heal can begin: a restart mid-heal could half-run a batch that is not safe to re-run |
| `heal-wait` | Polls `/api/bootstrap/status` until the heal has finished **and** a monitor pass started at least 600 s after the last heal ended. Then lists ERROR lines from the Portal's `pyegeria.log` and its rotated zips since the recreate | An early read of `present` is stale. Canaries still missing fail the step |
| `report-spec-sync` | `POST /api/report-specs/sync` on the Portal, then waits for the sync and requires the consumer index to come back "read". Not run-once: it writes only the Portal's own cache, never Egeria, so it is safe to repeat. A Portal that wants an administrator answers 401/403: the step is *needs a person*, with the remedy | The Portal syncs report specs at its own startup; a sync during the restart leaves **Used by** "not read" (2026-11-12) |
| `unfreeze` | Restarts RE and EA through their **launcher scripts** (default `~/.re-gate/start-8813.sh` and `~/.re-gate/start-ea-8880.sh`; `plan --launcher PORT=PATH` or `EGERIA_RESET_LAUNCHER_<port>` to change), run from the script's folder, and waits for their ports. A writer with no usable launcher is **not** restarted: the step is marked *needs a person* and prints the command it ran with; the rest of the run goes on, and `apply` exits 3. Prints the RE recovery command | The launchers set the environment RE and EA need; replaying a recorded command line would lose it. RE recovery (re-attaching RE's Egeria links) is Part 3; until it exists, follow trellis `docs/egeria-operations.md` §8.1 |
| `verify` | Read-only, each **PASS / FAIL / NOT MEASURED** with evidence (below) | |
| `record` | Writes a row to Postgres `coco_pharma.demo.egeria_resets` and prints a HANDOFF-ready summary | The Portal's "Last Egeria reset" panel |

**Run-once steps** (`backup`, `clear`, `secrets-sync`) never repeat once done. To repeat one, run
`apply --redo <step>` and type the step's name.

### Verify

- **Canaries:** every batch enabled on this Portal (from `/api/bootstrap/batches`), found by type and
  display name. Exactly one each: two means a duplicate.
- **Folder walks:** `DashboardFolder::Consumer::Portal` has 5 members, `DashboardFolder::Consumer::EgeriaAdvisor`
  has 5, `RootCollection::DashboardSheets` has its 2 folders, and `ReportSpecFolder::Consumer::Portal`'s
  members are listed. A member listed twice fails.
- **The saved-query tile:** the Useful Dashboards batch's manual step (the first refresh, which must
  run as a signed-in user), from `/api/bootstrap/status`: done, pending ("saved query not yet
  refreshed": FAIL until someone refreshes it), or not checked.
- **Classification purposes:** the count from `/api/types/classification-purposes`, compared with the
  count `plan` read: equal is PASS; more types **on a new image** is **CHANGED** (reported for review, not
  a failure); fewer types, a change on the same image, or purposes no longer reported is FAIL; not
  readable is NOT MEASURED.
- **Persona sign-ins (checkpoint):** the CLI never signs in as anyone. It asks you to sign in as each
  persona you use and open a sheet, then records what you answer: `ok`, `skip` (NOT MEASURED), or the
  failure. For a run in the background, answer up front with `apply --personas ok|skip` (or
  `EGERIA_RESET_PERSONAS`). With no terminal and no answer, or if the prompt hits end of input, the check
  is NOT MEASURED: the run goes on (2026-11-12: a background run crashed here).
- **Shared infrastructure:** one line per service of `compose-configs/shared-infra/shared-infra.yaml`
  (see *The shared-infrastructure check* below). A FAIL fails verify; WARN and EXPECTED STOPPED are
  reported and don't; the latest OpenLineage event is information only.
- **Report-spec consumer index:** read-only (`GET /api/report-specs/sync`, which starts nothing): the last sync's
  consumer index is "read" and the sync finished after `quickstart-egeria-main` started. Otherwise FAIL, with the
  remedy: re-sync report specs (Report Specs → Sync from Egeria as an administrator, or `POST /api/report-specs/sync`),
  or wait for the Portal's self-heal. NOT MEASURED when the status or the start time cannot be read.
- **10 minutes of watching:** connections to the `egeria` database, sampled every minute (the leak
  shows as `idle in transaction` climbing), and authentication failures in the platform log:
  `UNAUTHORIZED` / `NOT_AUTHORIZED`, an Egeria `-401-NNN` message code, or `401` as a number of its own.
  A `401` inside a GUID (`aee401cf-…`) or a timestamp's milliseconds is not one (2026-11-12: that read as
  a false FAIL). The evidence quotes the first three lines found.

**After any egeria-main restart: re-sync report specs** (Egeria Explorer → Report Specs → **Sync from Egeria**, as an administrator, or `POST /api/report-specs/sync`), or wait for the Portal's self-heal: while the consumer index is "not read" it syncs again at most every 2 minutes, on the next Report Specs or publish request. A sync that ran while Egeria was restarting leaves **Used by** "not read" (2026-11-12).

## The Portal's "Last Egeria reset" panel

**Admin → Data Initialization** shows the latest reset and the earlier ones, from `demo.egeria_resets`
(`GET /api/admin/egeria-resets`, administrators only):

- when, who and on which host;
- the image digests;
- whether the store was cleared, and the backup's path, size and sha256;
- the heal result;
- the verify counts.

With no row it says *No reset recorded by egeria-upgrade-reset.* If the table cannot be read it says
*Reset history not read:* and the reason. It has no buttons: a reset can only start on the host.

## The shared-infrastructure check

`egeria-upgrade-reset infra-check` reports on every service in `compose-configs/shared-infra/shared-infra.yaml`
(read when it runs, so a new service is covered without a code change), plus any `extraComposeFiles` in
`compose-configs/shared-infra/infra-health.json`. It compares with the checkout the running platform was
started from (or `--checkout PATH`). It only reads: `docker inspect`, `docker ps`, and inside
`egeria-shared-kafka` `kafka-get-offsets.sh` and `stat`. **It never starts, stops, restarts, recreates or
updates anything**: fixing a drift is a person's decision. It exits 1 when any service FAILs.

| Verdict | When |
|---|---|
| **PASS** | running (and `healthy`, where there is a healthcheck), restart policy as the yaml says, created from this checkout's compose file |
| **FAIL** | missing, not running, `unhealthy`, or **restart-policy drift** ("container restart=no, yaml says always": the 2026-11-10 proxy case, two days of lost lineage) |
| **WARN** | created from another compose file, or one that no longer exists ("a recreate from the repo may change it"); a digest-pinned yaml image the container doesn't run; running though listed as expected stopped |
| **EXPECTED STOPPED** | down, and listed in `infra-health.json`'s `expectedStopped` with a reason and who said so. An entry may also give `"exitCode"`: a container that exited with another code is a **FAIL** ("exited 1 (expected 0)"); the exit code is shown either way |
| **NOT MEASURED** | the container could not be inspected, or the compose file is missing |

The **OpenLineage** line ("latest event <time> (offset N)") is **information only**: a quiet topic can mean no
DAG ran, so there is no alert and no age threshold. The time is the last write to the topic's newest log segment.

On 2026-11-12 it reported five PASS and one WARN: `egeria-shared-kroki` was created from a temporary copy of
the compose file that no longer exists.

**Optional runtimes.** `infra-health.json` also lists
`compose-configs/optional-associated-runtimes/airflow-marquez/airflow-marquez.yaml` (owner, 2026-11-12:
"Start marquez", and cover it). Its services have no `container_name`, so each is found by its compose
project (`name: airflow-marquez`) **and** service labels; two containers for one service is NOT MEASURED,
never a guess. `airflow-init` is a one-shot setup container that exits by design: it is listed under
`expectedStopped` with `"exitCode": 0`, so a failed database migration (a non-zero exit) is a FAIL. `marquez` and `marquez-web` had no restart policy and stayed down after the 2026-11-10
reboot; the yaml now says `unless-stopped`, so a container created before that change reports
**FAIL drift** (restart=no) until it is recreated from the yaml.

### The Portal's "Shared infrastructure" line

`infra-check --record` writes one row to `coco_pharma.demo.infra_checks` (created by `init_egeria.sql` and by
the CLI; the newest 500 rows are kept). **Admin → Data Initialization** shows the latest row under
"Last Egeria reset" (`GET /api/admin/infra-health`, administrators only). The Portal has no Docker socket and
gets none: it only reads the row.

- A row older than **30 minutes** is greyed and says *last checked <time>: not current*. It never shows green.
- With no row: *not checked yet (run `egeria-upgrade-reset infra-check --record` on the host)*.
- Separately labelled, **reachable from the Portal now**: a TCP connection from the Portal's container to
  postgres 5442, kafka 9192, the OpenLineage proxy 6000 and kroki 8000. It is a different fact: it says
  nothing about restart policies.

### Recording it every 10 minutes (not installed)

`compose-configs/egeria-quickstart/bin/org.odpi.egeria.infra-check.plist` is a launchd agent that runs
`infra-check --record` every 10 minutes. **Nothing installs it**: it is a standing change to the host, so it
needs the owner's word. Until it is installed, the panel shows the last manual record as *not current*.

To install it (macOS, from the deployment's checkout), **choose the interpreter first, and check it**.
The plist names an absolute `python3` (`__PYTHON3__`), never `/usr/bin/env python3`: under launchd's
PATH that found `/usr/local/bin/python3` on laz, a framework Python 3.12 that exited silently, so the
agent ran and recorded nothing (2026-11-12).

1. Pick a `python3` (3.10 or later) by its absolute path, for example `PY=$(command -v python3)` in your
   own shell, or a Homebrew one such as `/opt/homebrew/bin/python3`.
2. Check that it runs the CLI the way launchd will (an empty environment and the plist's PATH). It is
   read-only and writes one line to a probe log:

```bash
PY=/opt/homebrew/bin/python3
```

```bash
env -i HOME="$HOME" PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin "$PY" compose-configs/egeria-quickstart/bin/egeria-upgrade-reset infra-check --log /tmp/infra-check-probe.log; tail -1 /tmp/infra-check-probe.log
```

   It must print one line starting with the time and a verdict (`PASS`, `WARN`, `FAIL` ...). No line
   means this `python3` does not work under launchd: choose another.
3. Install it with that interpreter:

```bash
mkdir -p runtime-volumes/egeria-resets
sed -e "s|__REPO__|$PWD|g" -e "s|__PYTHON3__|$PY|g" compose-configs/egeria-quickstart/bin/org.odpi.egeria.infra-check.plist > ~/Library/LaunchAgents/org.odpi.egeria.infra-check.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/org.odpi.egeria.infra-check.plist
```

4. After 10 minutes, `tail -1 runtime-volumes/egeria-resets/infra-check.log` shows the agent's first
   line, and the Portal's panel is current.

To uninstall it:

```bash
launchctl bootout gui/$(id -u)/org.odpi.egeria.infra-check
rm ~/Library/LaunchAgents/org.odpi.egeria.infra-check.plist
```

It runs `infra-check --record --log runtime-volumes/egeria-resets/infra-check.log`: one line per run (time, overall verdict, counts, the services that are not PASS, the OpenLineage offset, and whether the row was recorded; an error is a line too), and the file keeps only its newest 2000 lines, about two weeks. launchd's own output is discarded, so nothing grows without bound. The folder is git-ignored.

## Limits

- Quickstart only. Freshstart has its own database (`egeria_freshstart`) and platform container; use
  `reset-egeria-db.sh --database egeria_freshstart --container …` there.
- RE and EA are restarted only through their launcher scripts. Part 3 adds a maintenance mode to RE,
  which will replace stopping and restarting it.
- The `--latest` digest comes from `docker buildx imagetools inspect`; without registry access, give
  `--digest`.
