create user egeria_admin with superuser login password 'admin4egeria';
create user egeria_user with login password 'user4egeria';
create user airflow_user with superuser login password 'user4airflow';
create user marquez_user with superuser login password 'user4marquez';
create user example_user with login password 'user4example';
create user uc_user with superuser login password 'user4uc';
create user mlflow_user with superuser login password 'mlflow_password';
create user egeria_advisor with login password 'advisor';

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

grant all privileges on database egeria to egeria_admin, egeria_user;
grant all privileges on database egeria_freshstart to egeria_admin, egeria_user;
grant all privileges on database superset to egeria_admin, egeria_user;
grant all privileges on database coco_pharma to egeria_admin, egeria_user, airflow_user;
grant all privileges on database airflow to airflow_user;
grant all privileges on database marquez to marquez_user;
grant all privileges on database examples to example_user;
alter database hive_metastore owner to egeria_admin;
grant all privileges on database hive_metastore to egeria_admin;
grant all privileges on database mlflow_db to mlflow_user;
grant all privileges on database egeria_advisor to egeria_advisor;

\c egeria_advisor
CREATE EXTENSION IF NOT EXISTS vector;
