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
./egeria-upgrade-reset status --plan …                # each step's state
./egeria-upgrade-reset record --plan …                # write the Portal's reset row now (after a failed run)
```

`plan` writes `runtime-volumes/egeria-resets/<UTC>/plan.json` and `state.json` (git-ignored, with the
backup). It works on the checkout the running platform container was started from, which it reads
from the container's compose labels, so the Dockerfile, the secrets and the logs are that checkout's.
It prints:

- the pinned and the target image digest, and the running image;
- the database's size;
- Docker's free disk;
- the Resource Explorer (8813) and Egeria Advisor (8880) processes it will stop;
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
| `freeze-writers` | Stops RE on 8813 and EA on 8880 (their launcher process), and refuses if any other RE/EA process runs | Nothing may write to Egeria while it is cleared. Owner: freeze EA with RE, "Yes, with RE (Recommended)". The Portal's heal needs no pause: while Egeria is down its canary check cannot reach it, and an unreachable check never heals |
| `stop-platform` | `docker stop quickstart-egeria-main` | |
| `backup` | `pg_dump egeria \| gzip`, then a full gzip read, the `-- PostgreSQL database dump complete` marker, the size and sha256 | A truncated backup is worse than none: nothing goes on unless every check passes |
| `clear` | **Checkpoint:** type the database name. Then `compose-configs/shared-infra/reset-egeria-db.sql`: `DROP DATABASE … WITH (FORCE)`, `CREATE`, `GRANT ALL … TO egeria_admin, egeria_user` | The same SQL `reset-egeria-db.sh` uses: one copy |
| `recreate` | `docker compose … up -d --no-deps --force-recreate egeria-main`, then checks the running image is the one just built | **Never `docker start`**: on 2026-11-11, `reset-egeria-db.sh` restarted the old container, which kept the old image |
| `secrets-sync` | Copies `compose-configs/egeria-quickstart/secrets/*.omsecrets` into `runtime-volumes/quickstart-platform-data/secrets` in place. Prints accounts added, removed or changed **by name only**. Files that are not in the compose secrets (e.g. `resource-explorer.omsecrets`) are kept. Then checks the container sees the same files, and restarts it once if its bind mount is stale | New accounts (such as `olpgpubnpa`) reach the platform; a value never reaches a terminal or a log. A stale mount shows an empty `/deployments/secrets` |
| `heal-wait` | Polls `/api/bootstrap/status` until the heal has finished **and** a monitor pass started at least 600 s after the last heal ended. Then lists ERROR lines from the Portal's `pyegeria.log` and its rotated zips since the recreate | An early read of `present` is stale. Canaries still missing fail the step |
| `unfreeze` | Restarts RE and EA with the command line and folder they were started with, and waits for their ports. Prints the RE recovery command | RE recovery (re-attaching RE's Egeria links) is Part 3; until it exists, follow trellis `docs/egeria-operations.md` §8.1 |
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
- **Classification purposes:** `/api/types/classification-purposes` reports purposes for 94 types
  (`EGERIA_RESET_CLASSIFICATION_TYPES` to change).
- **Persona sign-ins (checkpoint):** the CLI never signs in as anyone. It asks you to sign in as each
  persona you use and open a sheet, then records what you answer: `ok`, `skip` (NOT MEASURED), or the
  failure.
- **10 minutes of watching:** connections to the `egeria` database, sampled every minute (the leak
  shows as `idle in transaction` climbing), and `401`/`UNAUTHORIZED` lines in the platform log.

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

## Limits

- Quickstart only. Freshstart has its own database (`egeria_freshstart`) and platform container; use
  `reset-egeria-db.sh --database egeria_freshstart --container …` there.
- RE and EA are restarted with the command line `ps` showed and the CLI's own environment. A process
  that relied on variables set only in the shell that started it may need restarting by hand: the
  `unfreeze` step's evidence has the command and log path.
- The `--latest` digest comes from `docker buildx imagetools inspect`; without registry access, give
  `--digest`.
