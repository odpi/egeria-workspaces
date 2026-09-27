-- Coco Pharmaceuticals Data Sharing Hub database.
--
-- coco_data_hub holds the data sets behind the Strategic Digital Product Catalog
-- (coco-workbooks/1. coco-data-hub/strategic-digital-products/): one schema per
-- digital product, one table per data structure, one column per data field.
-- coco_pharma keeps the existing Coco systems (coco_sus, coco_ods).
--
-- Applied by bin/apply-postgres-init.sh as its own migration (after
-- init_egeria.sql, which creates the roles granted below), so installs that
-- already ran init_egeria.sql pick it up on their next start.  Idempotent.

SELECT 'CREATE DATABASE coco_data_hub'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coco_data_hub')\gexec

grant all privileges on database coco_data_hub to egeria_admin, egeria_user, airflow_user;

\connect coco_data_hub
\ir data/coco_data_hub.sql

-- Database users for the data hub, each with only what its job needs:
--
--  * provisioner - used by the provisioning services that fill and deliver the
--    digital products' data sets (secrets collection "PostgreSQL Provisioning
--    Secret" in secrets/integration.omsecrets).  It reads and writes the rows of
--    every product table, including tables added to a product schema later.
--  * surveyor - used by the PostgreSQL cataloguer and surveys (secrets collection
--    "PostgreSQL Server Secret").  It is created by shared-infra's first-boot
--    init_egeria.sql.  It reads, but never writes, every product table: the Data
--    Sharing Hub Manager (Liskov) runs the PostgreSQL database survey against the
--    hub, and the survey's column statistics (pg_stats) and column sizes are only
--    visible to a user that can select from the table.  Guarded because an install
--    whose Postgres predates that user has no surveyor role.
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    CREATE USER provisioner WITH LOGIN PASSWORD 'provisioner4egeria';
  END IF;
END
$$;

GRANT CONNECT, TEMPORARY ON DATABASE coco_data_hub TO provisioner;

DO $$
DECLARE
  product_schema text;
BEGIN
  FOR product_schema IN SELECT schema_name FROM information_schema.schemata
                         WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO provisioner', product_schema);
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO provisioner', product_schema);
    EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE egeria_admin IN SCHEMA %I GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO provisioner', product_schema);
  END LOOP;

  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') THEN
    GRANT ALL PRIVILEGES ON DATABASE coco_data_hub TO surveyor;

    FOR product_schema IN SELECT schema_name FROM information_schema.schemata
                           WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
      EXECUTE format('GRANT USAGE ON SCHEMA %I TO surveyor', product_schema);
      EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO surveyor', product_schema);
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE egeria_admin IN SCHEMA %I GRANT SELECT ON TABLES TO surveyor', product_schema);
    END LOOP;
  END IF;
END
$$;
