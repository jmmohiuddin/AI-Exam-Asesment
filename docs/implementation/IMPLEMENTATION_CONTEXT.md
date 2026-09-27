# Implementation Context (compact working memory)

> Keep this file short. Update at every checkpoint. Details live in the linked docs, not here.

## Current phase
**Phase 1 — Wave A: partially delivered, consolidated and committed (31f9109).** Wave A was cut short by a token-limit stop; each of the three agents left scaffolding it never filled. **Next: finish the Wave A gaps, then Vertical Slice 1.**

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

## Completed (verified on disk, commit 31f9109)
- [x] Phase 0 audit, context, doc consistency check (2026-09-28)
- [x] `khata/core/` — config, db session + tenant context, RFC 9457 errors, security, crypto, idempotency, ids, logging, models, pagination, ratelimit, roles (~1.6k LOC; imports clean)
- [x] Alembic chain bootstrapped: `0001_foundation` + `migrations/rls_helpers.py` + `scripts/db_bootstrap.sql`
- [x] `khata/engines/` — scoring, rubric, rubric_heuristics, workflow, marks, bangla/digits (pure, no DB/IO)
- [x] `web/` base — design tokens, BN/EN i18n (7 namespaces), API client + problem-details, auth/session plumbing
- [x] **288 backend tests pass** (`cd backend && uv run pytest`, 3.1s)

## Not delivered — empty scaffolding left by the interrupted Wave A
These directories exist but contain **no files**. Do not mistake them for done.
- Backend modules: `modules/{identity,org,authz,audit,events,jobs}/`
- Backend: `worker/`, `scripts/` (no seed), `tests/unit/`, `tests/integration/`
- Engines: `engines/mathcheck/`, `engines/results/`, `engines/data/templates/`
- Engine fixtures: `tests/engines/fixtures/{bangla,math,results}/` are all empty — the planned **≥200 results fixtures do not exist**
- Web app shell: `src/{app,shell,components,pages,mocks,preferences}/`, `e2e/`, `scripts/`, `public/icons/` — **no `index.html`, no `main.tsx`, no `App.tsx`, so the web app cannot start yet**
- No FastAPI app object / route wiring yet; no `infra/` (Dockerfile, compose, CI)

## Next (in order)
1. **Backend gap-fill (sequential, one writer):** identity/auth → org → authz/RBAC → audit chain → events/jobs + worker. Wire the FastAPI app and `/v1/auth/*`, `/v1/me`.
2. **Engines gap-fill (parallel, isolated):** `mathcheck`, `results` + the ≥200 results fixtures and bangla/math fixtures.
3. **Web gap-fill (parallel, isolated):** entry point (`index.html`, `main.tsx`, `App.tsx`), router, shell, primitives, login screen.
4. **Vertical slice 1:** exam from template → rubric → lock → upload script (web/PDF) → pipeline (Fake AI) → review → lock → results → publish.

## Known issues / active risks
- **Token-limit stops silently truncate agent work.** Wave A left three worktrees uncommitted; the work was only recovered by inspecting them directly. Commit at every checkpoint from now on.
- No AI keys, no gold data → AI quality not measurable here (labelled synthetic)
- Docker daemon down → compose file unverified locally
- Android app out of reach in this environment
- Web dependency manifest pins very new majors (React 19, Vite 8, TS 6, vitest 5) and `node_modules` was never installed — `pnpm install` is unverified

## Worktree status
Both Wave A worktrees have been merged into the main tree and are now redundant:
- `.claude/worktrees/agent-a05f4ea16108b9916` (engines) — merged
- `.claude/worktrees/agent-ac4b0780dca0e6b33` (web) — merged
Remove with `git worktree remove --force <path>` once you are satisfied nothing else is in them.

## Wave plan (dependency-driven)
- **Backend is sequential** (one writer per wave; migrations are a single linear chain): B1 curriculum + roster/consent + exams + rubrics → B2 capture/upload + pipeline + ai-gateway (Fake + adapters) → B3 review/knowledge/moderation → B4 results/reporting/publish.
- **Frontend runs in parallel** with each backend wave, against that wave's OpenAPI contract (screen agents own disjoint `web/src/features/<area>/**`).
- Integration owner (orchestrator) merges worktrees, owns `pyproject.toml`/lockfiles, commits.
