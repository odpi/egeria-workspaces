-- SPDX-License-Identifier: Apache-2.0
-- Copyright Contributors to the Egeria project.
--
-- Security operational data store.
--
-- security_ods receives the open metadata digital products of Egeria's Security Observability product family -
-- one table per product - so that the security team can query them with SQL.  The security products are in the
-- security governance zone, so they are kept apart from egeria_ods, which every user of the catalogue may read.
-- The subscription is set up by coco-workbooks/1. coco-data-hub/security-operational-data-store.md in quickstart.
-- Egeria's provisioning services create the schema and the tables as they deliver the products, so this script
-- creates only the database and the access to it.
--
-- Run when the shared PostgreSQL server is first created (docker-entrypoint-initdb.d, after init_egeria_ods.sql,
-- which creates the provisioner role and sets its password) and again by ensure-shared-infra.sh on every start,
-- so that a server created before this database was added picks it up.  Safe to run again: it creates only what
-- is missing.

SELECT 'CREATE DATABASE security_ods'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'security_ods')\gexec

-- Unlike egeria_ods, nobody may connect unless granted below.
REVOKE CONNECT, TEMPORARY ON DATABASE security_ods FROM PUBLIC;

-- provisioner creates the schema that receives the products, and the tables in it.  The role is created by
-- init_egeria_ods.sql; the guard covers a hand-run of this script on a server that does not have it yet.
DO $$
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    GRANT CONNECT, TEMPORARY, CREATE ON DATABASE security_ods TO provisioner;
  END IF;
END
$$;

-- surveyor reads what is delivered: it is the user of the PostgreSQL cataloguer and surveys (secrets collection
-- "PostgreSQL Server Secret"), which describe the database in open metadata.  egeria_admin and egeria_user, who
-- read egeria_ods, are deliberately not given access to the security data.
DO $$
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') THEN
    GRANT CONNECT, TEMPORARY ON DATABASE security_ods TO surveyor;
  END IF;
END
$$;

\connect security_ods

-- Whatever provisioner creates from now on is readable by surveyor.  The loop covers schemas and tables that
-- provisioner created before surveyor was added.
DO $$
DECLARE
  product_schema text;
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor')
     AND EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    ALTER DEFAULT PRIVILEGES FOR ROLE provisioner GRANT USAGE ON SCHEMAS TO surveyor;
    ALTER DEFAULT PRIVILEGES FOR ROLE provisioner GRANT SELECT ON TABLES TO surveyor;

    FOR product_schema IN SELECT schema_name FROM information_schema.schemata
                           WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
      EXECUTE format('GRANT USAGE ON SCHEMA %I TO surveyor', product_schema);
      EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO surveyor', product_schema);
    END LOOP;
  END IF;
END
$$;
