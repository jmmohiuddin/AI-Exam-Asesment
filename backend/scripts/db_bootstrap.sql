-- Khata local database bootstrap (run as a PostgreSQL superuser).
--
--   psql -h /tmp -U <superuser> -d postgres \
--        -v owner_password=... -v app_password=... -f scripts/db_bootstrap.sql
--
-- Idempotent: safe to re-run; passwords are re-synchronised on every run.
-- Roles:
--   khata_owner  owns every schema object and runs migrations (NOT superuser).
--   khata_app    runtime role: not owner, NOBYPASSRLS, least-privilege grants
--                (table grants are applied by the Alembic migrations).
\set ON_ERROR_STOP on

SELECT format('CREATE ROLE khata_owner LOGIN PASSWORD %L NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS', :'owner_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'khata_owner') \gexec

SELECT format('CREATE ROLE khata_app LOGIN PASSWORD %L NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS NOINHERIT', :'app_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'khata_app') \gexec

SELECT format('ALTER ROLE khata_owner WITH LOGIN PASSWORD %L NOSUPERUSER NOBYPASSRLS', :'owner_password') \gexec
SELECT format('ALTER ROLE khata_app WITH LOGIN PASSWORD %L NOSUPERUSER NOBYPASSRLS NOINHERIT', :'app_password') \gexec

SELECT 'CREATE DATABASE khata_dev OWNER khata_owner ENCODING ''UTF8'' TEMPLATE template0'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'khata_dev') \gexec

SELECT 'CREATE DATABASE khata_test OWNER khata_owner ENCODING ''UTF8'' TEMPLATE template0'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'khata_test') \gexec

REVOKE ALL ON DATABASE khata_dev FROM PUBLIC;
REVOKE ALL ON DATABASE khata_test FROM PUBLIC;
GRANT CONNECT, TEMPORARY ON DATABASE khata_dev TO khata_app;
GRANT CONNECT, TEMPORARY ON DATABASE khata_test TO khata_app;
GRANT ALL ON DATABASE khata_dev TO khata_owner;
GRANT ALL ON DATABASE khata_test TO khata_owner;

\connect khata_dev
ALTER SCHEMA public OWNER TO khata_owner;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

\connect khata_test
ALTER SCHEMA public OWNER TO khata_owner;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
