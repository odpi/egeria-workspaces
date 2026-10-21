#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
#
# Metadata store for the optional TestGen runtime
# (compose-configs/optional-associated-runtimes/testgen/): a `testgen` database
# owned by a `testgen_admin` role. TestGen creates its own `testgen` schema and
# tables in it on `testgen setup-system-db`, and uses the one role as both its
# schema admin and its application user, so no further grants are needed.
#
# Like every file in this directory it runs only when the shared Postgres
# volume is first initialised. For an existing volume, run the equivalent
# one-off psql in the TestGen README instead. That is a write to the shared
# Postgres, so tell the other sessions first.
#
# No password lives in this file. If TESTGEN_DB_PASSWORD is in the postgres
# container's environment it is used; otherwise the role is created without a
# password, which cannot log in over TCP until one is set with ALTER ROLE.
# Idempotent: an existing role or database is left as it is.
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
     -v tg_password="${TESTGEN_DB_PASSWORD:-}" <<'EOSQL'
SELECT NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'testgen_admin') AS need_role \gset
SELECT :'tg_password' <> '' AS have_password \gset
\if :need_role
    CREATE ROLE testgen_admin WITH LOGIN;
    \if :have_password
        ALTER ROLE testgen_admin WITH PASSWORD :'tg_password';
    \endif
\endif
SELECT 'CREATE DATABASE testgen OWNER testgen_admin'
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testgen') \gexec
EOSQL
