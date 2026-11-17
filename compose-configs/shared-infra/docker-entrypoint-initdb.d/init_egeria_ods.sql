-- SPDX-License-Identifier: Apache-2.0
-- Copyright Contributors to the Egeria project.
--
-- Egeria operational data store.
--
-- egeria_ods receives the open metadata digital products that Egeria publishes - one table per product - so that
-- the content of the open metadata ecosystem can be queried with SQL.  It is filled by a subscription to each of
-- Egeria's top-level product families, each delivering to its own schema.  The subscriptions are set up by
-- workbooks/subscribing-to-digital-products/build-egeria-ods.ipynb in freshstart and by
-- coco-workbooks/1. coco-data-hub/egeria-operational-data-store.md in quickstart.  Egeria's provisioning services
-- create the schemas and the tables as they deliver the products, so this script creates only the database and
-- the access to it.
--
-- The database is used by both the quickstart and the freshstart environments.
--
-- Run when the shared PostgreSQL server is first created (docker-entrypoint-initdb.d, after init_egeria.sql) and
-- again by ensure-shared-infra.sh on every start, so that a server created before this database was added picks
-- it up.  Safe to run again: it creates only what is missing.

-- provisioner is the user that Egeria's provisioning services deliver digital products with (secrets collection
-- "PostgreSQL Provisioning Secret" in secrets/integration.omsecrets), and that Airflow's coco_data_hub connection
-- signs in with.  The quickstart's init_coco_data_hub.sql relies on it.
--
-- No password lives in this file (TR-28).  It comes from PROVISIONER_PASSWORD, which gen-env.sh keeps in
-- shared-infra/.env and ensure-shared-infra.sh passes in on every start, so the role's password is set from .env
-- each time: a new value in .env rotates it on the next start.  The start scripts put the same value into the
-- Egeria secrets (install-secrets.py) and the Airflow connection.  When PROVISIONER_PASSWORD is not set (the
-- container's first initialisation, or a hand-run psql), the role is created without a password - it cannot sign in
-- over TCP - and an existing role's password is left as it is.
\getenv prov_password PROVISIONER_PASSWORD
-- Unset (not just empty) leaves the variable undefined, and :'prov_password' would stop the script.
\if :{?prov_password}
\else
    \set prov_password ''
\endif
SELECT NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') AS need_provisioner \gset
SELECT :'prov_password' <> '' AS have_provisioner_password \gset
\if :need_provisioner
    CREATE ROLE provisioner WITH LOGIN;
\endif
\if :have_provisioner_password
    -- psql puts the value into the statement text on the client side, so keep this statement out of
    -- pg_stat_statements (preloaded on some installs), whose query-text file would otherwise hold the password.
    -- A dotted name is accepted even when the extension is not loaded. Superuser only: this script runs as postgres.
    SET pg_stat_statements.track_utility = off;
    ALTER ROLE provisioner WITH PASSWORD :'prov_password';
    RESET pg_stat_statements.track_utility;
\endif
\unset prov_password

SELECT 'CREATE DATABASE egeria_ods'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'egeria_ods')\gexec

-- provisioner creates the schemas that receive the products, and the tables in them.
GRANT CONNECT, TEMPORARY, CREATE ON DATABASE egeria_ods TO provisioner;

-- The other users read what is delivered:
--  * egeria_admin and egeria_user - for queries, such as the ones in the workbook;
--  * surveyor - used by the PostgreSQL cataloguer and surveys (secrets collection "PostgreSQL Server Secret").
-- Each is guarded because a server that predates a user does not have its role.
DO $$
DECLARE
  reader text;
BEGIN
  FOREACH reader IN ARRAY ARRAY['egeria_admin', 'egeria_user', 'surveyor'] LOOP
    IF EXISTS (SELECT FROM pg_roles WHERE rolname = reader) THEN
      EXECUTE format('GRANT CONNECT, TEMPORARY ON DATABASE egeria_ods TO %I', reader);
    END IF;
  END LOOP;
END
$$;

\connect egeria_ods

-- Whatever provisioner creates from now on is readable by the other users.  The second loop covers schemas and
-- tables that provisioner created before a reader was added.
DO $$
DECLARE
  reader         text;
  product_schema text;
BEGIN
  FOREACH reader IN ARRAY ARRAY['egeria_admin', 'egeria_user', 'surveyor'] LOOP
    IF EXISTS (SELECT FROM pg_roles WHERE rolname = reader) THEN
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE provisioner GRANT USAGE ON SCHEMAS TO %I', reader);
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE provisioner GRANT SELECT ON TABLES TO %I', reader);

      FOR product_schema IN SELECT schema_name FROM information_schema.schemata
                             WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
        EXECUTE format('GRANT USAGE ON SCHEMA %I TO %I', product_schema, reader);
        EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I', product_schema, reader);
      END LOOP;
    END IF;
  END LOOP;
END
$$;
