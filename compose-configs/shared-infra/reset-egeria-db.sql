-- SPDX-License-Identifier: Apache-2.0
-- Copyright Contributors to the ODPi Egeria project.
--
-- Drop and recreate one Egeria metadata-store database, with the grants the platform needs
-- (as docker-entrypoint-initdb.d/init_egeria.sql gives a new data directory). Shared by
-- reset-egeria-db.sh and egeria-quickstart/bin/egeria-upgrade-reset: one copy of the SQL.
--
-- Run as the Postgres superuser with psql, reading this file, and the database name as a
-- psql variable (the callers check it is a plain lowercase identifier and not a maintenance
-- database first):
--   docker exec -i egeria-shared-postgres psql -h localhost -p 5442 -U postgres \
--       -v ON_ERROR_STOP=1 -v db=egeria -f - < reset-egeria-db.sql
-- Each statement runs on its own (DROP/CREATE DATABASE cannot run inside a transaction).
-- WITH (FORCE) disconnects anything still attached (pgAdmin, DBeaver, ...).
DROP DATABASE IF EXISTS :"db" WITH (FORCE);
CREATE DATABASE :"db";
GRANT ALL PRIVILEGES ON DATABASE :"db" TO egeria_admin, egeria_user;
