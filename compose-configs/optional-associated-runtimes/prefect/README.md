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

## 3. Development and Code Reloading

* Flow code is located in the host directory [runtime-volumes/prefect/user_code/](file:///../../../runtime-volumes/prefect/user_code/).
* The primary flow entrypoint is `flow.py`.
* The worker is configured with a `process` work pool named `egeria-pool`. It executes flow runs as local subprocesses inside the worker container.
* To run your flows:
  1. Modify `flow.py` locally on your host.
  2. You can register/deploy your flow to the running Prefect Server using the Prefect CLI:
     ```bash
     # Enter the worker container to deploy
     docker exec -it egeria-optional-prefect-worker prefect deploy flow.py:egeria_survey_flow --name egeria-deployment --pool egeria-pool
     ```
  3. Go to the UI at [http://localhost:4200](http://localhost:4200), select the deployment, and trigger a run.
