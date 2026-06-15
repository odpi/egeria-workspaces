DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'egeria_admin') THEN
    CREATE USER egeria_admin WITH SUPERUSER LOGIN PASSWORD 'admin4egeria';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'egeria_user') THEN
    CREATE USER egeria_user WITH LOGIN PASSWORD 'user4egeria';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'airflow_user') THEN
    CREATE USER airflow_user WITH SUPERUSER LOGIN PASSWORD 'user4airflow';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'marquez_user') THEN
    CREATE USER marquez_user WITH SUPERUSER LOGIN PASSWORD 'user4marquez';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'example_user') THEN
    CREATE USER example_user WITH LOGIN PASSWORD 'user4example';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'uc_user') THEN
    CREATE USER uc_user WITH SUPERUSER LOGIN PASSWORD 'user4uc';
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'mlflow_user') THEN
    CREATE USER mlflow_user WITH SUPERUSER LOGIN PASSWORD 'mlflow_password';
  END IF;
END
$$;

SELECT 'CREATE DATABASE egeria'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'egeria')\gexec

SELECT 'CREATE DATABASE superset'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'superset')\gexec

SELECT 'CREATE DATABASE coco_pharma'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coco_pharma')\gexec

SELECT 'CREATE DATABASE airflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')\gexec

SELECT 'CREATE DATABASE marquez'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'marquez')\gexec

SELECT 'CREATE DATABASE examples'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'examples')\gexec

SELECT 'CREATE DATABASE ucdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ucdb')\gexec

SELECT 'CREATE DATABASE hive_metastore'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hive_metastore')\gexec

SELECT 'CREATE DATABASE mlflow_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mlflow_db')\gexec

SELECT 'CREATE DATABASE coco_ods'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coco_ods')\gexec

grant all privileges on database egeria to egeria_admin, egeria_user;
grant all privileges on database superset to egeria_admin, egeria_user;
grant all privileges on database coco_pharma to egeria_admin, egeria_user, airflow_user;
grant all privileges on database airflow to airflow_user;
grant all privileges on database marquez to marquez_user;
grant all privileges on database examples to example_user;
ALTER DATABASE hive_metastore OWNER TO egeria_admin;
GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO egeria_admin;
grant all privileges on database mlflow_db to mlflow_user;

-- Demo mode user registry (schema within the egeria database)
\connect egeria
CREATE SCHEMA IF NOT EXISTS demo;
GRANT ALL ON SCHEMA demo TO egeria_admin, egeria_user;
\connect coco_pharma
CREATE SCHEMA IF NOT EXISTS coco_sus;
GRANT ALL ON SCHEMA coco_sus TO egeria_admin, egeria_user, airflow_user;
SET search_path TO coco_sus;
\ir data/coco_sus.sql

CREATE SCHEMA IF NOT EXISTS coco_ods;
GRANT ALL ON SCHEMA coco_ods TO egeria_admin, egeria_user, airflow_user;
SET search_path TO coco_ods;
\ir data/coco_ods.sql
