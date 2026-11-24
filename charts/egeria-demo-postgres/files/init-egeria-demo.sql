-- Demo PostgreSQL set-up for the egeria-platform chart: only what the Egeria platform needs.
-- Idempotent: it creates what is missing and never drops, resets or alters existing data.
-- The role names, passwords and grants are those of compose-configs/shared-infra/docker-entrypoint-initdb.d/init_egeria.sql
-- (charts/tests/drift_test.py compares them). DEMO ONLY: the passwords are the public demo ones.
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'egeria_admin') THEN CREATE ROLE egeria_admin WITH SUPERUSER LOGIN PASSWORD 'admin4egeria'; END IF; END $$;
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'egeria_user') THEN CREATE ROLE egeria_user WITH LOGIN PASSWORD 'user4egeria'; END IF; END $$;
DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') THEN CREATE ROLE surveyor WITH LOGIN PASSWORD 'surveyor4egeria'; END IF; END $$;
SELECT 'CREATE DATABASE egeria' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'egeria')\gexec
SELECT 'CREATE DATABASE egeria_freshstart' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'egeria_freshstart')\gexec
GRANT pg_monitor TO surveyor;
GRANT ALL PRIVILEGES ON DATABASE egeria TO egeria_admin, egeria_user, surveyor;
GRANT ALL PRIVILEGES ON DATABASE egeria_freshstart TO egeria_admin, egeria_user;
\c egeria
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
