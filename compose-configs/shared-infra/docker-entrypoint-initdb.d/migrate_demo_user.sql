-- Migration: add demo_user for the quickstart demo auth database.
-- Run this once against the running egeria-shared-postgres instance if it was
-- already initialised before this user was added to init_egeria.sql.
--
--   docker exec -i egeria-shared-postgres psql -U postgres -p 5442 -f /dev/stdin < migrate_demo_user.sql
--
-- Safe to run multiple times (IF NOT EXISTS guards).

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'demo_user') THEN
    CREATE USER demo_user WITH LOGIN PASSWORD 'demo4egeria';
  END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE coco_pharma TO demo_user;
