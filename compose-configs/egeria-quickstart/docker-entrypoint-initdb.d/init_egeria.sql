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

-- Demo-mode user registry + feedback tables (coco_pharma) ──────────────────
-- Defensive: demo_user is normally created by shared-infra's native
-- docker-entrypoint-initdb.d/init_egeria.sql (first-boot only). Guard here so
-- this migration is self-sufficient even if that step hasn't run yet.
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'demo_user') THEN
    CREATE USER demo_user WITH LOGIN PASSWORD 'demo4egeria';
  END IF;
END
$$;
GRANT ALL PRIVILEGES ON DATABASE coco_pharma TO demo_user;

-- demo_auth (users/events/favorites/config) and demo (feedback) are normally
-- created lazily by the app itself (demo_db.py / demo_feedback_handler.py) on
-- first use, which makes demo_user the owner automatically. That only breaks
-- if something else creates the schema first — e.g. sync-demo-db.sh's
-- _merge_feedback() runs `CREATE SCHEMA IF NOT EXISTS demo` as the superuser
-- PGUSER during an import, and only grants USAGE (not CREATE) back to
-- demo_user afterwards. If that happens before the app has ever created
-- demo.feedback itself, every later feedback submission 500s with
-- "permission denied for schema demo" — hit for real on cray on 2026-08-07.
-- Create both schemas AUTHORIZATION demo_user up front, and re-assert
-- ownership on every run in case a schema already exists under a different
-- owner (idempotent — safe to rerun).
CREATE SCHEMA IF NOT EXISTS demo_auth AUTHORIZATION demo_user;
CREATE SCHEMA IF NOT EXISTS demo      AUTHORIZATION demo_user;
ALTER SCHEMA demo_auth OWNER TO demo_user;
ALTER SCHEMA demo      OWNER TO demo_user;

-- Pre-create the tables too (not just the schemas) so a fresh install has
-- them ready before the app ever starts, and so this migration is a complete
-- description of what demo_db.py / demo_feedback_handler.py expect to find.
-- Columns mirror those SQLAlchemy models; the app's own
-- `ADD COLUMN IF NOT EXISTS` migrations still run on top of this and remain
-- the source of truth for schema evolution going forward — this is just
-- idempotent bootstrap, not a replacement for them.
CREATE TABLE IF NOT EXISTS demo_auth.users (
  id            VARCHAR(36)  PRIMARY KEY,
  display_name  VARCHAR(200) NOT NULL,
  org           VARCHAR(200),
  email         VARCHAR(200) NOT NULL UNIQUE,
  password_hash VARCHAR(200) NOT NULL,
  role          VARCHAR(20)  DEFAULT 'user',
  verified      BOOLEAN      DEFAULT false,
  verify_token  VARCHAR(200),
  reset_token   VARCHAR(200),
  reset_expires TIMESTAMP,
  created_at    TIMESTAMP,
  last_login    TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_demo_auth_users_email ON demo_auth.users (email);

CREATE TABLE IF NOT EXISTS demo_auth.events (
  id                VARCHAR(36) PRIMARY KEY,
  user_id           VARCHAR(36),
  user_email        VARCHAR(200),
  user_display_name VARCHAR(200),
  persona_name      VARCHAR(200),
  tool              VARCHAR(100),
  event_type        VARCHAR(50) NOT NULL,
  detail            TEXT,
  created_at        TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demo_auth.favorites (
  id         VARCHAR(36)  PRIMARY KEY,
  user_email VARCHAR(200) NOT NULL,
  persona_id VARCHAR(100) NOT NULL,
  app        VARCHAR(100) NOT NULL,
  section    VARCHAR(100) NOT NULL,
  label      VARCHAR(200) NOT NULL,
  icon       VARCHAR(10),
  url        VARCHAR(500) NOT NULL,
  position   INTEGER DEFAULT 0,
  created_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_demo_auth_favorites_user_email ON demo_auth.favorites (user_email);

CREATE TABLE IF NOT EXISTS demo_auth.config (
  key   VARCHAR(100) PRIMARY KEY,
  value TEXT
);

CREATE TABLE IF NOT EXISTS demo.feedback (
  id                 VARCHAR(36) PRIMARY KEY,
  session_id         VARCHAR(36),
  user_id            VARCHAR(200),
  env                VARCHAR(40),
  persona            VARCHAR(100),
  page               VARCHAR(200),
  element_guid       VARCHAR(36),
  rating             INTEGER,
  category           VARCHAR(40),
  message            TEXT,
  email              VARCHAR(200),
  wants_response     BOOLEAN,
  consent_to_contact BOOLEAN,
  build_version      VARCHAR(80),
  user_agent         VARCHAR(500),
  viewport           VARCHAR(20),
  locale             VARCHAR(20),
  triage_status      VARCHAR(20),
  created_at         TIMESTAMP
);

-- Tables just created above are owned by whoever ran this script (PGUSER,
-- e.g. egeria_admin) — schema ownership doesn't propagate to table
-- ownership. Reassign every table in both schemas to demo_user so the app's
-- ALTER TABLE migrations (which require ownership, not just GRANTed DML)
-- keep working, and so this also self-heals any pre-existing tables left
-- mis-owned by a past sync-demo-db.sh import (mirrors _reown_schema() there).
DO $$
DECLARE r RECORD;
BEGIN
  FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'demo_auth' LOOP
    EXECUTE format('ALTER TABLE demo_auth.%I OWNER TO demo_user', r.tablename);
  END LOOP;
  FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'demo' LOOP
    EXECUTE format('ALTER TABLE demo.%I OWNER TO demo_user', r.tablename);
  END LOOP;
END
$$;
