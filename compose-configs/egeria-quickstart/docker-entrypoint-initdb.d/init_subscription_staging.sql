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

-- Egeria's provisioning services write only the product's columns: a delivery inserts new rows and, on the
-- primary key, updates existing ones.  This trigger keeps the delivery columns right for the subscriber:
--
--  * a new row is stamped with the delivery and waits as 'delivered';
--  * a row whose product data changes is stamped again and set back to 'delivered', so it is reprocessed;
--  * a row whose product data is unchanged keeps its delivery columns - so redelivering an unchanged row, or the
--    subscriber marking a row 'processed' or 'failed', does not count as a new delivery.
--
-- delivery_identifier is the delivering transaction, so the rows of one delivery share it.
CREATE OR REPLACE FUNCTION public.mark_delivery() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
  delivery_columns constant text[] := ARRAY['delivery_identifier', 'delivery_timestamp', 'processing_status',
                                            'processing_timestamp', 'processing_message'];
BEGIN
  IF TG_OP = 'UPDATE' THEN
    IF (to_jsonb(NEW) - delivery_columns) IS NOT DISTINCT FROM (to_jsonb(OLD) - delivery_columns) THEN
      RETURN NEW;
    END IF;
  ELSIF NEW.delivery_identifier IS NOT NULL THEN
    RETURN NEW;                              -- the writer stamped its own delivery
  END IF;
  NEW.delivery_identifier  := 'delivery-' || pg_current_xact_id();
  NEW.delivery_timestamp   := now();
  NEW.processing_status    := 'delivered';
  NEW.processing_timestamp := NULL;
  NEW.processing_message   := NULL;
  RETURN NEW;
END
$$;

DO $$
DECLARE
  subscription_table record;
BEGIN
  FOR subscription_table IN SELECT c.table_schema, c.table_name FROM information_schema.columns c
                             WHERE c.column_name = 'delivery_identifier'
                               AND c.table_schema NOT IN ('information_schema', 'public') LOOP
    EXECUTE format('CREATE OR REPLACE TRIGGER mark_delivery BEFORE INSERT OR UPDATE ON %I.%I '
                   'FOR EACH ROW EXECUTE FUNCTION public.mark_delivery()',
                   subscription_table.table_schema, subscription_table.table_name);
  END LOOP;
END
$$;

-- Database users, as for coco_data_hub:
--
--  * provisioner - used by the provisioning services that deliver the digital
--    products to their subscribers; it reads and writes the rows of every
--    subscription table, and owns the subscription schemas and tables.  It also has CREATE on the database and the schemas,
--    because the provisioning services issue CREATE SCHEMA / CREATE TABLE
--    IF NOT EXISTS before writing, and PostgreSQL checks that privilege even
--    when the schema or table already exists.
--  * surveyor - used by the PostgreSQL cataloguer and surveys; it reads, but never
--    writes, every subscription table.
-- Both are guarded because an install may predate either user.
DO $$
DECLARE
  subscription_schema text;
  subscription_table  text;
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'provisioner') THEN
    GRANT CONNECT, TEMPORARY, CREATE ON DATABASE subscription_staging TO provisioner;

    FOR subscription_schema IN SELECT schema_name FROM information_schema.schemata
                                WHERE schema_name NOT LIKE 'pg\_%' AND schema_name NOT IN ('information_schema', 'public') LOOP
      -- The provisioning services also COMMENT ON the schema, its tables and their columns with the product's
      -- descriptions at each delivery, which only the owner may do.
      EXECUTE format('ALTER SCHEMA %I OWNER TO provisioner', subscription_schema);
      FOR subscription_table IN SELECT tablename FROM pg_tables WHERE schemaname = subscription_schema LOOP
        EXECUTE format('ALTER TABLE %I.%I OWNER TO provisioner', subscription_schema, subscription_table);
      END LOOP;
      EXECUTE format('GRANT USAGE, CREATE ON SCHEMA %I TO provisioner', subscription_schema);
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
