create user egeria_admin with superuser login password 'admin4egeria';
create user egeria_user with login password 'user4egeria';
create user airflow_user with superuser login password 'user4airflow';
create user marquez_user with superuser login password 'user4marquez';
create user example_user with login password 'user4example';
create user uc_user with superuser login password 'user4uc';
create user mlflow_user with superuser login password 'mlflow_password';

create database egeria;
create database superset;
create database coco_pharma;
create database airflow;
create database marquez;
create database examples;
create database ucdb;
CREATE DATABASE hive_metastore;
create database mlflow_db;
create database coco_ods;

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
