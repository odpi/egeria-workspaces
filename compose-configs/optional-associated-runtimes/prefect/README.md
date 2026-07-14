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

## 3. Development and Examples

Flow code is located in the host directory [runtime-volumes/prefect/user_code/](file:///../../../runtime-volumes/prefect/user_code/). The worker is configured with a `process` work pool named `egeria-pool` and executes flows inside the container environment.

We have included two Egeria-centric example flows in this directory:

### A. PostgreSQL Schema Inspector (`postgres_schema_flow.py`)
Queries the shared Postgres instance (`egeria-shared-postgres:5442`) inside the Docker network. It identifies all active databases and dynamically connects to each database to list user schemas, tables, and views in a formatted `rich` console summary.

* **Deploy to Server:**
  Run the command with `-w /` to bypass OCI mount namespace restrictions on macOS:
  ```bash
  docker exec -w / egeria-optional-prefect-worker prefect deploy /opt/prefect/flows/postgres_schema_flow.py:postgres_schema_flow --name postgres-inspector --pool egeria-pool
  ```

### B. Egeria Glossary Inspector (`egeria_glossary_flow.py`)
Utilizes the `pyegeria` library (`GlossaryManager`) to connect to the Egeria quickstart OMAG platform (`https://host.docker.internal:9443`) inside the network. It authenticates, fetches all configured business glossaries, and prints a formatted summary table of active glossaries.

* **Deploy to Server:**
  Run the command with `-w /` to bypass OCI mount namespace restrictions on macOS:
  ```bash
  docker exec -w / egeria-optional-prefect-worker prefect deploy /opt/prefect/flows/egeria_glossary_flow.py:egeria_glossary_flow --name glossary-inspector --pool egeria-pool
  ```

---

## 4. Running the Flows

1. Run the `prefect deploy` command for the flow you wish to run (shown above).
2. Open the Prefect UI at **[http://localhost:4200](http://localhost:4200)**.
3. Click on the **Deployments** tab on the left.
4. Select your deployment (e.g., `postgres-inspector` or `glossary-inspector`) and click **Run** -> **Quick Run** in the top right.
5. Navigate to the **Runs** tab to watch the execution logs and view the printed schema/glossary tables.

