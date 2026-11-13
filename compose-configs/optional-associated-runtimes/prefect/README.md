# Optional Associated Runtime: Prefect

This directory contains the Docker Compose configurations to run Prefect (v3) as an optional associated runtime.

---

## 1. Prerequisites (Database Initialization)

Prefect uses the shared PostgreSQL database container (`egeria-shared-postgres`). If you are running against an **already active** database volume (where the automatic initialization scripts do not run again), execute this command to create the required database and user:

```bash
docker exec -i egeria-shared-postgres psql -U postgres -d postgres -p 5442 -c \
"CREATE USER prefect_user WITH SUPERUSER LOGIN PASSWORD 'user4prefect'; CREATE DATABASE prefect; GRANT ALL PRIVILEGES ON DATABASE prefect TO prefect_user;"
```

---

## 2. Managing the Services

You can manage the Prefect services from this directory:

* **Start Prefect:**
  ```bash
  docker compose up -d
  ```
* **Verify Status:**
  ```bash
  docker compose ps
  ```
* **Stop Prefect:**
  ```bash
  docker compose down
  ```

Once started, the Prefect UI is available at **[http://localhost:4200](http://localhost:4200)**.

---

## 3. Resource Explorer's worker (`re-prefect-worker`)

The worker has **its own compose file**, `docker-compose.re-worker.yaml` (project `egeria-optional-re-prefect-worker`),
so §2's commands start and stop the Prefect server alone, without the worker's service-account env file. Compose
checks every required `${VAR:?}` in a file before it looks at which services you asked for. The worker joins the
same `egeria_network` and reaches the server by name, so start the server first.

Prefect's only user here is Trellis's Resource Explorer (RE). This service is RE's worker for the
`resource-explorer-pool` work pool. It replaced the July example worker on 2026-11-13, when the owner deleted
that worker's pool and both its deployments.

* **Image:** trellis's own RE image, role `prefect-worker`. In the trellis repo, `make image-re` builds
  `trellis/resource-explorer:local` and `:<sha12>` and bakes in the build commit. Set `TRELLIS_RE_IMAGE` to
  pick another tag.
* **Version parity:** the worker advertises its commit (`re-worker-<sha12>-<host>`) and serves only its own
  deployment and queue (`re-survey-step-<sha12>`, `re-<sha12>`). RE dispatches a step to it only when RE runs
  the same commit. Otherwise RE warns and runs the step itself. Build RE's web image and this one from the
  same commit.
* **It refuses to start** without a build commit, or with a library survey step missing from the image. The
  first lines of `docker logs egeria-optional-re-prefect-worker` say which.
* **What it can reach:**
  * Postgres, Egeria and the Prefect API, by service name;
  * the trellis data volume, `trellis_trellis-re-data` (the trellis stack creates it, so bring that up first);
  * one read-only survey root, `RE_WORKER_SURVEY_ROOT` mounted at `/survey`.

  A database registered as `localhost`, or a host path outside the survey root, is not reachable from the
  container.
* **GPU (Linux + NVIDIA only):** add `-f docker-compose.re-worker-nvidia.yaml` after `-f docker-compose.re-worker.yaml`. Never use it on a Mac, where
  Docker has no GPU passthrough.
* **Before relying on it:** run the A/B proof in trellis
  `packages/resource-explorer/docs/design-notes/PREFECT-CONTAINER-WORKER-2026-11-13.md`.

* **Its service account (required):** RE reads its own Egeria service account from `EGERIA_USER_ID` and
  `EGERIA_USER_PASSWORD`. Without one, every path that needs it refuses (`NoServiceAccount`). The compose file has
  no default on purpose: a persona default once made RE act as a person. Put the account in `.env.re-worker` in
  this directory. Git ignores that file; never commit it, and never paste its values anywhere:

  ```bash
  # .env.re-worker (this directory; gitignored). Fill in RE's service account, not a person's login.
  RE_DAEMON_USER_ID=
  RE_DAEMON_USER_PASSWORD=
  ```

  Compose refuses to start the worker while either value is missing.

```bash
docker compose up -d prefect-server        # the server: this directory's docker-compose.yaml, no env file needed
docker compose -f docker-compose.re-worker.yaml --env-file .env.re-worker up -d
docker compose -f docker-compose.re-worker.yaml --env-file .env.re-worker logs re-prefect-worker | head -5
#   expect "library steps ... (none missing)", then "Worker ... started!"
```

On laz (macOS), RE's worker runs on the host under launchd instead (trellis
`packages/resource-explorer/scripts/launchd/`). It can reach `localhost` resources and host paths, and it runs
the same checkout as the RE app.

---

## 4. The retired example flows

`runtime-volumes/prefect/user_code/` still holds the two July example flows: `postgres_schema_flow.py` and
`egeria_glossary_flow.py`. No worker runs them now: the pool they were deployed to, and their deployments
(`postgres-inspector`, `glossary-inspector`), were deleted on 2026-11-13. They remain as examples only.
