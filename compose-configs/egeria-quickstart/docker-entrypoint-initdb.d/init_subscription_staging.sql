-- Coco Pharmaceuticals subscription staging database.
--
-- subscription_staging receives the data that subscribing systems take from the
-- strategic digital products in coco_data_hub.  It has one schema per
-- subscription - one subscribing system and one digital product - holding the
-- product's tables plus delivery columns.  Each subscriber has its own copy of
-- the product data, so that it can take deliveries on its own schedule and
-- reprocess them after an error.  The subscriptions are listed in
-- coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv.
--
-- Run by bin/apply-postgres-init.sh on every start, after init_coco_data_hub.sql
-- (which creates the provisioner user granted below).  Safe to run again: it only
-- creates what is missing.

SELECT 'CREATE DATABASE subscription_staging'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'subscription_staging')\gexec

grant all privileges on database subscription_staging to egeria_admin, egeria_user, airflow_user;

\connect subscription_staging
\ir data/subscription_staging.sql

-- Database users, as for coco_data_hub:
--
--  * provisioner - used by the provisioning services that deliver the digital
--    products to their subscribers; it reads and writes the rows of every
--    subscription table.
--  * surveyor - used by the PostgreSQL cataloguer and surveys; it reads, but never
--    writes, every subscription table.
-- Both are guarded because an install may predate either user.
DO $$
DECLARE
  subscription_schema text;
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    GRANT CONNECT, TEMPORARY ON DATABASE subscription_staging TO provisioner;

    FOR subscription_schema IN SELECT schema_name FROM information_schema.schemata
                                WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
      EXECUTE format('GRANT USAGE ON SCHEMA %I TO provisioner', subscription_schema);
      EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO provisioner', subscription_schema);
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE egeria_admin IN SCHEMA %I GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO provisioner', subscription_schema);
    END LOOP;
  END IF;

  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') THEN
    GRANT ALL PRIVILEGES ON DATABASE subscription_staging TO surveyor;

    FOR subscription_schema IN SELECT schema_name FROM information_schema.schemata
                                WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
      EXECUTE format('GRANT USAGE ON SCHEMA %I TO surveyor', subscription_schema);
      EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO surveyor', subscription_schema);
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE egeria_admin IN SCHEMA %I GRANT SELECT ON TABLES TO surveyor', subscription_schema);
    END LOOP;
  END IF;
END
$$;
