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
-- "PostgreSQL Provisioning Secret" in secrets/integration.omsecrets).  The quickstart's init_coco_data_hub.sql
-- creates it in the same way for the Coco Pharmaceuticals data hub.
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    CREATE USER provisioner WITH LOGIN PASSWORD 'provisioner4egeria';
  END IF;
END
$$;

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
