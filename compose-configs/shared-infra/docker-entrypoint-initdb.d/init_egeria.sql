create user egeria_admin with superuser login password 'admin4egeria';
create user egeria_user with login password 'user4egeria';
create user demo_user with login password 'demo4egeria';
create user airflow_user with superuser login password 'user4airflow';
create user marquez_user with superuser login password 'user4marquez';
create user example_user with login password 'user4example';
create user uc_user with superuser login password 'user4uc';
create user mlflow_user with superuser login password 'mlflow_password';
create user egeria_advisor with login password 'advisor';
create user surveyor with login password 'surveyor4egeria';
create user dagster_user with superuser login password 'user4dagster';
create user prefect_user with superuser login password 'user4prefect';

create database egeria;
create database egeria_freshstart;
create database superset;
create database coco_pharma;
create database airflow;
create database marquez;
create database examples;
create database ucdb;
create database hive_metastore;
create database mlflow_db;
create database egeria_advisor owner egeria_advisor;
create database dagster;
create database prefect;

grant all privileges on database egeria to egeria_admin, egeria_user;
grant all privileges on database egeria_freshstart to egeria_admin, egeria_user;
grant all privileges on database superset to egeria_admin, egeria_user;
grant all privileges on database coco_pharma to egeria_admin, egeria_user, airflow_user, demo_user, surveyor;
grant all privileges on database airflow to airflow_user;
grant all privileges on database marquez to marquez_user;
grant all privileges on database examples to example_user;
alter database hive_metastore owner to egeria_admin;
grant all privileges on database hive_metastore to egeria_admin;
grant all privileges on database mlflow_db to mlflow_user;
grant all privileges on database egeria_advisor to egeria_advisor;
grant pg_monitor to surveyor;
grant all privileges on database dagster to dagster_user;
grant all privileges on database prefect to prefect_user;

\c egeria_advisor
CREATE EXTENSION IF NOT EXISTS vector;
