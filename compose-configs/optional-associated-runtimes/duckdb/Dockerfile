# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project

FROM python:3.14-slim@sha256:cad9a2c871761c413caa6fdd6441c783451e740a48aaeba60ae62a8b53525ef6

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libssl-dev \
    gcc \
    python3-dev \
    default-jre-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install DuckDB and Buenavista
# Buenavista provides a Postgres-compatible proxy for DuckDB
RUN pip install --no-cache-dir \
    duckdb==1.0.0 \
    buenavista[duckdb]==0.4.1 \
    boto3 \
    psycopg2-binary

# Pre-install common DuckDB extensions for federation
# - postgres: PostgreSQL federation (postgres_scanner)
# - mysql: MySQL federation (mysql_scanner)
# - sqlite: SQLite federation (sqlite_scanner)
# - httpfs: S3/HTTP/GCS access
# - iceberg: Apache Iceberg support
# - delta: Delta Lake (Databricks) support
# - spatial: Geospatial data support
# - excel: Excel file support
# - bigquery: Google BigQuery support (community extension)
RUN python3 -c "import duckdb; conn = duckdb.connect(':memory:'); \
    conn.execute('INSTALL postgres;'); \
    conn.execute('INSTALL mysql;'); \
    conn.execute('INSTALL sqlite;'); \
    conn.execute('INSTALL httpfs;'); \
    conn.execute('INSTALL iceberg;'); \
    conn.execute('INSTALL delta;'); \
    conn.execute('INSTALL spatial;'); \
    conn.execute('INSTALL excel;'); \
    conn.execute('INSTALL jdbc;');"

# Note: BigQuery extension might need specific installation steps or be version-dependent.
# It's often available via 'INSTALL bigquery FROM community;' in newer DuckDB versions.
RUN python3 -c "import duckdb; conn = duckdb.connect(':memory:'); \
    try: conn.execute('INSTALL bigquery FROM community;'); \
    except: print('BigQuery community extension not available in this build');"

EXPOSE 5433

# Start Buenavista Postgres Proxy for DuckDB
# By default it creates/uses an in-memory database or a file specified in the command
# We use a file-backed database to persist federation metadata if needed.
ENV DUCKDB_FILE=/data/federation.duckdb

CMD python3 -m buenavista.postgres.server --host 0.0.0.0 --port 5433 duckdb $DUCKDB_FILE
