<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# DuckDB Federation Server

This optional runtime provides a DuckDB instance exposed via a PostgreSQL-compatible proxy ([Buenavista](https://github.com/jwills/buenavista)). 

It is designed to act as a **federation server**, allowing you to query multiple data sources (Postgres, S3, MySQL, Iceberg, Delta Lake, etc.) using standard SQL through a single entry point.

## Features
- **Postgres Compatibility**: Connect using any Postgres client (psql, DBeaver, Superset, etc.) on port `5433`.
- **Pre-installed Extensions**: Includes `postgres`, `mysql`, `sqlite`, `httpfs`, `iceberg`, `delta`, `spatial`, and `excel`.
- **Local File Access**: Automatically mounts `exchange-quickstart` and `runtime-volumes` for easy access to local Parquet, CSV, or JSON files.

## Getting Started

### 1. Start the server
From this directory:
```bash
docker compose up -d
```

### 2. Connect to the server
You can use `psql` or any other Postgres-compatible tool:
```bash
psql -h localhost -p 5433 -U duckdb
```
*(Note: Any username/password will work as Buenavista/DuckDB doesn't enforce them by default in this configuration.)*

## Federation Examples

Once connected, you can attach external data sources:

### Attach Egeria's Postgres Database
```sql
-- Attach the shared Postgres database as a schema named 'egeria_pg'
ATTACH 'dbname=egeria user=egeria_admin password=admin4egeria host=egeria-shared-postgres port=5442' AS egeria_pg (TYPE postgres);

-- Query a table from Postgres
SELECT * FROM egeria_pg.coco_pharma.patient LIMIT 10;
```

### Query Local Parquet Files
```sql
-- Query a file from the exchange area
SELECT * FROM '/mnt/exchange-quickstart/coco-data-lake/landing-area/patients.parquet' LIMIT 10;
```

### Query from S3 (HTTPFS)
```sql
-- Setup AWS credentials (if needed)
-- SET s3_region='us-east-1';
-- SET s3_access_key_id='...';
-- SET s3_secret_access_key='...';

-- Query directly from a public S3 bucket
SELECT * FROM 's3://duckdb-blobs/train.parquet' LIMIT 5;
```

### Query Iceberg Tables
```sql
-- Load iceberg extension (pre-installed)
LOAD iceberg;

-- Query an Iceberg table (example path)
SELECT * FROM iceberg_scan('/mnt/exchange-quickstart/iceberg-data/my_table');
```

### Query Delta Lake (Databricks)
```sql
-- Load delta extension (pre-installed)
LOAD delta;

-- Query a Delta table
SELECT * FROM delta_scan('/mnt/exchange-quickstart/delta-data/my_delta_table');
```

### Google BigQuery
```sql
-- Install/Load BigQuery extension (Community)
LOAD bigquery;

-- Attach BigQuery project
-- ATTACH 'project_id' AS bq (TYPE bigquery);
```

### Oracle (via JDBC)
The server is pre-installed with the `jdbc` extension and a Java runtime. To connect to Oracle, you will need to provide the Oracle JDBC driver (JAR file) in a volume mount.
```sql
-- Load JDBC extension
LOAD jdbc;

-- Example of connecting via JDBC (requires driver JAR)
-- CALL jdbc_attach('oracle', 'jdbc:oracle:thin:@host:port:sid', user='...', password='...', driver='/path/to/ojdbc8.jar');
```

## Surveying and Metadata
The goal of this deployment is to facilitate "Surveying" of external systems by providing a uniform SQL interface. Egeria can be configured to connect to this DuckDB instance to discover and catalog assets from all federated sources at once.

## License
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
