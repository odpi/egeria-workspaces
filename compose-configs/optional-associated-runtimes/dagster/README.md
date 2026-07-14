# Optional Associated Runtime: Dagster

This directory contains the Docker Compose configurations to run Dagster as an optional associated runtime.

---

## 1. Prerequisites (Database Initialization)

Dagster uses the shared PostgreSQL database container (`egeria-shared-postgres`). If you are running against an **already active** database volume (where the automatic initialization scripts do not run again), execute this command to create the required database and user:

```bash
docker exec -i egeria-shared-postgres psql -U postgres -d postgres -p 5442 -c \
"CREATE USER dagster_user WITH SUPERUSER LOGIN PASSWORD 'user4dagster'; CREATE DATABASE dagster; GRANT ALL PRIVILEGES ON DATABASE dagster TO dagster_user;"
```

---

## 2. Managing the Services

You can manage the Dagster services from this directory using standard Compose:

* **Start Dagster:**
  ```bash
  docker compose up -d
  ```
* **Verify Status:**
  ```bash
  docker compose ps
  ```
* **Stop Dagster:**
  ```bash
  docker compose down
  ```

Once started, the Dagster Webserver UI is available at **[http://localhost:8050](http://localhost:8050)**.

---

## 3. How to Develop & Reload Code

* Pipelines are configured to load dynamically from the host directory [runtime-volumes/dagster/user_code/](file:///../../../runtime-volumes/dagster/user_code/).
* The primary pipeline script is `repo.py`.
* To edit your pipelines:
  1. Modify `repo.py` locally on your host.
  2. Navigate to [http://localhost:8050](http://localhost:8050) in your browser.
  3. Click **Reload** in the top-right workspace panel to instantly update the definitions without restarting the containers.

---

## 4. Integration with Egeria

* **OpenLineage:** The `openlineage_sensor` defined in `repo.py` automatically captures asset and job execution metadata and posts it to Egeria's HTTP proxy on port `6000` (resolvable inside the Docker network at `http://egeria-shared-openlineage-proxy-backend:6000`).
* **Pyegeria:** You can write Python tasks using `pyegeria` directly in your Dagster code to catalog assets or read/update Egeria's metadata.
