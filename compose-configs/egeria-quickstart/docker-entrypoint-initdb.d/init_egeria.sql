create user egeria_admin with superuser login password 'admin4egeria';
create user egeria_user with login password 'user4egeria';
create user airflow_user with superuser login password 'user4airflow';
create user marquez_user with superuser login password 'user4marquez';
create user example_user with login password 'user4example';


create database egeria;
create database superset;
create database coco_pharma;
create database airflow;
create database marquez;
create database examples;

grant all privileges on database egeria to egeria_admin, egeria_user;
grant all privileges on database superset to egeria_admin, egeria_user;
grant all privileges on database coco_pharma to egeria_admin, egeria_user;
grant all privileges on database airflow to airflow_user;
grant all privileges on database marquez to marquez_user;
grant all privileges on database examples to example_user;


