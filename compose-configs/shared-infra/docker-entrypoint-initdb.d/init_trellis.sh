#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project
#
# The egeria_advisor database for Trellis (Resource Explorer, Egeria Advisor and
# Studio): a pgvector-enabled database owned by the egeria_advisor role.
#
# No password lives in this file. The role's password comes from
# PGVECTOR_PASSWORD in the postgres container's environment
# (shared-infra.yaml passes it in from shared-infra/.env; gen-env.sh generates a
# random one for a brand-new install). If PGVECTOR_PASSWORD is empty, the role is
# created WITHOUT a password: it cannot log in over TCP until one is set with
# ALTER ROLE, and Trellis refuses to start without PGVECTOR_PASSWORD anyway.
# There is no built-in default password.
#
# Like every file in this directory, it runs only when the shared Postgres volume
# is first initialised. For an existing volume, see "Creating egeria_advisor on
# an existing volume" in ../README.md. Writing to the shared Postgres affects
# other users, so tell them first.
#
# Idempotent: an existing role, database or extension is left as it is. An
# existing role's password is never changed here.
#
# Named init_trellis.sh so it sorts AFTER init_egeria*.sql: the image's entrypoint
# runs these files in locale order, which ignores punctuation, so a name like
# init_egeria_advisor.sh would run before init_egeria.sql and the surveyor grant
# would find no surveyor role.
set -euo pipefail

if [[ -z "${PGVECTOR_PASSWORD:-}" ]]; then
  echo "[init_trellis] WARNING: PGVECTOR_PASSWORD is not set; creating egeria_advisor WITHOUT a password." >&2
  echo "[init_trellis] Set one later with ALTER ROLE (see compose-configs/shared-infra/README.md)." >&2
fi

# \getenv reads the password from the environment inside psql, so it never
# appears on a command line.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<'EOSQL'
\getenv adv_password PGVECTOR_PASSWORD
SELECT NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'egeria_advisor') AS need_role \gset
SELECT coalesce(:'adv_password', '') <> '' AS have_password \gset
\if :need_role
    CREATE ROLE egeria_advisor WITH LOGIN;
    \if :have_password
        ALTER ROLE egeria_advisor WITH PASSWORD :'adv_password';
    \endif
\endif
SELECT 'CREATE DATABASE egeria_advisor OWNER egeria_advisor'
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'egeria_advisor') \gexec
GRANT ALL PRIVILEGES ON DATABASE egeria_advisor TO egeria_advisor;
SELECT 'GRANT ALL PRIVILEGES ON DATABASE egeria_advisor TO surveyor'
 WHERE EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') \gexec
\c egeria_advisor
CREATE EXTENSION IF NOT EXISTS vector;
EOSQL
