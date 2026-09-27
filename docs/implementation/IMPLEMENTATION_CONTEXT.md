# Implementation Context (compact working memory)

> Keep this file short. Update at every checkpoint. Details live in the linked docs, not here.

## Current phase
**Phase 0 — Audit: done** (`IMPLEMENTATION_AUDIT.md`). **Next: Phase 1 foundation + parallel pure engines + web foundation.**

## Architecture (as built — target per TRD/SD)
- `backend/` — Python 3.12, FastAPI, SQLAlchemy 2 (sync) + psycopg 3, Alembic, PostgreSQL 16 (RLS, `identity` schema), Postgres job queue. Package `khata`.
  - `khata/core/` config, db session + tenant context, errors (RFC 9457), security, logging, ids
  - `khata/modules/<name>/` one package per SD §2 module (`models.py`, `schemas.py`, `service.py`, `api.py`); cross-module calls only via `service.py`
  - `khata/engines/` **pure** deterministic code (no DB/IO imports): scoring, results, mathcheck, bangla (Bijoy, digits), omr
  - `khata/worker/` queue runner, lanes, scheduler
- `web/` — React + TypeScript (Vite), i18n BN/EN, design tokens from `05` §4.
- `infra/` — Dockerfile, docker-compose (Postgres + MinIO + api + worker); CI in `.github/workflows/`.
- Android capture app: **not started** (no SDK in environment). Server contract shared with web/PDF upload.

## Source-of-truth precedence for conflicts
08 §5.3 (RBAC) · 06 (AI metrics/gates/schemas) · 07 (HITL, extended per ADR-004) · 05 over 04 (UX detail) · TRD over SD for requirements; SD for entity/endpoint shape. Resolutions: `IMPLEMENTATION_AUDIT.md` §11–12.

## Key decisions
See `TECHNICAL_DECISIONS.md`. One-liners:
- Auth: framework libraries, no Keycloak in MVP (ADR-001)
- All AI cells seeded at L0/L1; Fake provider for dev/test; real adapters by config (ADR-006)
- Risk model `uncalibrated-v0`: hard triggers + conservative rules; never "low" until calibrated (ADR-011)

## Local environment
- Postgres 16 at `/tmp:5432`, superuser `mohiuddin`. DBs `khata_dev`, `khata_test`. App role `khata_app` (non-owner, RLS enforced); migrations run as owner role `khata_owner`.
- Backend tests: `cd backend && uv run pytest` · Web: `cd web && pnpm dev` · e2e: `pnpm e2e`

## Completed
- [x] Phase 0 audit, context, doc consistency check (2026-09-28)

## Next
1. Phase 1 foundation (backend core, identity/auth, org, RBAC, audit chain, queue, tenancy/RLS + isolation tests)
2. Pure engines (scoring, results + ≥200 fixtures, mathcheck, Bijoy/digits) — parallel, isolated
3. Web foundation (tokens, i18n, shell, primitives, login) — parallel, isolated
4. Vertical slice 1: exam from template → rubric → lock → upload script (web/PDF) → pipeline (Fake AI) → review → lock → results → publish

## Known issues / active risks
- No AI keys, no gold data → AI quality not measurable here (labelled synthetic)
- Docker daemon down → compose file unverified locally
- Android app out of reach in this environment

## Files being modified
(update per wave)
