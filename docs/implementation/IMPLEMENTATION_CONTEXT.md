# Implementation Context (compact working memory)

> Keep this file short. Update at every checkpoint. Details live in the linked docs, not here.

## Current phase
**Phase 1 — Vertical slice 1 works end to end** (commit 79f7c83). Sign in → create exam → rubric → lock → capture answer → AI evaluation → teacher review → lock marks, proven in a browser against the real database. **Next: broaden the slice (OTP sign-in, real capture/OCR, results & publish) and fill the remaining Wave A gaps.**

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

## Completed (verified, commit 79f7c83)
- [x] Phase 0 audit, context, doc consistency check
- [x] `khata/core/` — config, db session + tenant context, RFC 9457 errors, security, crypto, idempotency, ids, logging, models, pagination, ratelimit, roles
- [x] Migrations `0001_foundation` + `0002_assessment`; 30 tables; every tenant table under **FORCE** RLS
- [x] `khata/engines/` — scoring, rubric, rubric_heuristics, workflow, marks, bangla/digits (pure; enforced by import-linter)
- [x] `khata/modules/` — identity (password sign-in, sessions, refresh rotation, switch-tenant, `/me`), org, authz (bearer principal, role deps, tenant-bound session), assessment (authoring → capture → evaluation → review → lock), aigateway (vendor-neutral `MarkingProvider` + deterministic Fake)
- [x] FastAPI app (`khata.main:create_app`), 16 endpoints, health check
- [x] `khata.scripts.seed_dev` — one worked exam; refuses outside dev/test
- [x] `web/` runs: entry point, router, sign-in, exam list, **review screen** (question · answer · model answer · rubric · AI reasoning · evidence · confidence · teacher decision, one screen)
- [x] eslint/prettier/MSW mocks/i18n-check — the web scripts that were declared but missing
- [x] **Verified in a browser**: overrode the AI on one criterion; mark recomputed 5 → 4, persisted as `edited` with the deciding user, AI suggestion retained

### Gates (all passing)
| Half | Gates |
|---|---|
| backend | 312 tests · ruff · ruff format · mypy (core) · import-linter |
| web | 31 tests · eslint · prettier · tsc · i18n check · production build |

## The AI failsafe, as built
A provider only ever **suggests**. A suggestion moves an item to `suggested` and leaves `total` NULL. Only a teacher decision produces a mark, and the mark is computed by `engines.scoring.score_item`, never by the provider. A blank answer yields `cannot_determine` + `needs_teacher`, not a silent zero. `accepted_ai` distinguishes `confirmed` from `edited`, which is what the override-rate metric (spec 06) will read.

## Not delivered yet
- **OTP sign-in** — tables (`otp_challenge`, `otp_send`) and config exist; `web/src/auth/types.ts` already codes for it; login answers `status:"ok"` so the discriminator is ready
- **Capture** — answers are submitted as text. No upload, image processing, OCR or segmentation; `engines/mathcheck/` and `engines/results/` are still empty, and the ≥200 results fixtures do not exist
- Publish (needs step-up OTP), moderation, recheck; `modules/{audit,events,jobs}/`, `worker/`
- `infra/` — no Dockerfile, compose or CI; `web/e2e/` empty (no Playwright specs committed); `web/public/icons/` empty, so the PWA manifest points at missing icons
- Android capture app — out of reach in this environment

## Next (in order)
1. **OTP sign-in** — completes the auth contract the web already expects.
2. **Capture + pipeline** — upload, image handling, OCR, segmentation, background jobs via the Postgres queue.
3. **`mathcheck` / `results` engines** + their fixture corpora.
4. **Results, moderation, publish** (publish gated on step-up OTP).
5. **infra/** — Dockerfile, compose, CI running both gate suites; commit Playwright e2e for the slice.

## Known issues / active risks
- **Token-limit stops silently truncate agent work.** Wave A left three uncommitted worktrees. Commit at every checkpoint.
- **Parallel agents drift on contracts.** The web and backend halves of Wave A disagreed on the auth shapes; the backend was moved to the web's (spec-derived) contract. Fix the contract in one place before splitting work again.
- `_advance_to_reviewing` pushes the whole exam to `reviewing` as soon as one script is evaluated. Fine for one script; revisit with `rolling_mode` when capture is real.
- No AI keys and no gold data → AI quality is not measurable here. The Fake provider is keyword matching and is refused in staging/production by `build_marking_provider`.
- Docker daemon down → compose unverified locally.
- Web pins very new majors (React 19, Vite 8, TS 6, vitest 5). `pnpm install` and the full gate suite now pass, so this is watch-only.

## Local environment
- Postgres 16 on `/tmp:5432`, superuser `mohiuddin`. App role `khata_app` (non-owner, RLS enforced); migrations run as `khata_owner`.
- `khata_dev` is migrated **and seeded**; `khata_test` is migrated and wiped per test.
- Dev sign-in: `+8801712345678` / `Khata-dev-2027!` (from `KHATA_SEED_DEV_PASSWORD`).
- Run: `cd backend && make run` (:8000) · `cd web && pnpm dev` (:5173, proxies `/v1`). Vite binds `localhost`, not `127.0.0.1`.
- Re-seed: `cd backend && uv run python -m khata.scripts.seed_dev` (refuses if the teacher already exists).

## Worktree status
Both Wave A worktrees were merged and are redundant:
`.claude/worktrees/agent-a05f4ea16108b9916` (engines), `.claude/worktrees/agent-ac4b0780dca0e6b33` (web).
Remove with `git worktree remove --force <path>`.

## Wave plan (dependency-driven)
- **Backend is sequential** (one writer per wave; migrations are a single linear chain): B1 curriculum + roster/consent + exams + rubrics → B2 capture/upload + pipeline + ai-gateway (Fake + adapters) → B3 review/knowledge/moderation → B4 results/reporting/publish.
- **Frontend runs in parallel** with each backend wave, against that wave's OpenAPI contract (screen agents own disjoint `web/src/features/<area>/**`).
- Integration owner (orchestrator) merges worktrees, owns `pyproject.toml`/lockfiles, commits.
