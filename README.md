# Khata — AI-assisted exam script marking for Bangladeshi schools

**Repository:** https://github.com/jmmohiuddin/AI-Exam-Asesment

A marking workspace for **school internal exams** (NCTB CQ/MCQ format, Grades 9–10,
General Mathematics and Physics). Teachers set the paper and rubric, scripts are
captured with a phone, and the platform suggests criterion-level marks **with visible
evidence** — but **a teacher decides every mark**. Totals, pass rules, GPA, tabulation
and report cards are computed by tested code, never by a model.

> *খাতা* = answer script. Working name; branding is a separate decision.

### Why it is built this way

Bangladesh's SSC 2026 re-evaluation changed 27,836 grades, and mis-marking a public
exam is now a criminal offence. The research is equally clear that fully autonomous
AI grading is neither accurate enough nor acceptable. So three rules are structural,
not configurable:

- **The AI only ever suggests.** A suggestion leaves the mark `NULL`. Only a teacher's
  decision produces a mark, and the mark is computed by the scoring engine, not by
  the provider.
- **Nothing is scored that cannot be shown.** Every suggestion carries the rubric
  criterion and the evidence it rests on. A blank answer is routed to a human, never
  silently given zero.
- **Arithmetic is deterministic.** Totals, choice rules, pass rules, grades and GPA
  are pure, tested code with fixture corpora — so the product is useful even with AI
  switched off entirely.

---

## Status

**Early. About 28% of the MVP's 85 "Must" requirements are delivered.**

`docs/implementation/PRD_COVERAGE_AUDIT.md` is a requirement-by-requirement audit
against the PRD, re-measured against the running code rather than against notes.

| | |
|---|---|
| FRs delivered in full | 17 of 106 |
| Partial | 15 |
| Not started | 74 |
| Endpoints | 29 of the ~100 in the system design |
| Tests | 1,439 backend (85% coverage) · 79 web |

### What works end to end today

Verified in a browser against a real PostgreSQL database, not only in tests:

1. **Sign in** — password, then an SMS-style OTP on a device the account has not used
   before. A known device skips the code.
2. **Roster and consent** — import students from a CSV (English or Bangla headers,
   Bangla numerals, group and version synonyms). The file is validated first and the
   report says exactly what a commit would do; nothing is written until it is
   confirmed. Guardian consent is recorded per student for each of CT-1 (digital
   marking), CT-2 (AI assistance) and CT-3 (contribution to evaluation), as history
   rather than a flag, so what was permitted when a script was marked stays
   answerable after a withdrawal.
3. **Author** — create an exam, add questions, write rubrics (criteria, model answer,
   alternatives, deductions, error-carried-forward, numeric answer specs), lock them.
4. **Capture** — submit an answer as text. *(Real capture — photos, OCR, QR cover
   sheets — is not built.)*
5. **Evaluate** — a vendor-neutral marking provider proposes criterion decisions with
   evidence and confidence. Only a deterministic Fake provider exists; it is refused
   outside dev and test. **A student whose guardian has not given CT-2 is never sent
   to a provider at all** — the answer goes straight to the teacher to mark by hand.
6. **Review** — one screen shows the answer, the model answer, the rubric, the AI's
   reasoning, its evidence and its confidence. The teacher confirms or overrides per
   criterion; the mark recomputes and records who decided it.
7. **Lock and read results** — a board-style ledger: marks, percentage, NCTB grade,
   grade point, pass/fail per student, in Bangla or English. Provisional totals are
   labelled as such and say how many answers are still unmarked.

### Not built yet

Capture (Android app, image pipeline, OCR, QR cover sheets), curriculum packs and
paper templates, the background worker, moderation, publishing, re-checks, exports,
dashboards, and the AI capability registry that gates which cells may use AI at all.
`infra/` is empty: no Dockerfile, compose or CI.

One thing is deliberately incomplete rather than simply absent: **Bijoy/ANSI to
Unicode conversion on roster import** (FR-ORG-03, TR-BN-01). The maintained
converters are GPL-3.0 or unlicensed, and a mapping table written from memory would
silently corrupt student names. Until a verified table is sourced under a usable
licence, a name that looks like legacy Bijoy text is flagged as an error and the file
is not committed — never converted into a guess.

---

## Repository layout

```
backend/     Python 3.12 · FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL 16
  src/khata/
    core/        config, DB session + tenant context, RFC 9457 errors, security, crypto
    engines/     PURE deterministic code — no DB, no I/O (enforced by import-linter)
      rubric.py    criteria, alternatives, deductions, ECF, answer specs, validation
      scoring.py   the one function that turns criterion decisions into a mark
      workflow.py  exam and item state machines
      marks.py     exact rounding on the mark grid
      results/     aggregation, choice rules, pass rules, NCTB grades, GPA
      mathcheck/   numeric verification: Bangla/Latin numerals, units, sig-figs
      bangla/      digit normalisation
    modules/     one package per bounded context: identity, org, assessment,
                 aigateway, authz (audit, events and jobs are empty placeholders)
  tests/       unit + integration against a real database, with fixture corpora
web/         React 19 · TypeScript · Vite · i18n (Bangla/English) · PWA
docs/        the product definition package, 00–11 (see below)
research/    source extracts and independent fact verification
```

**The `engines/` boundary is the important one.** Nothing in it may import the
database or a module; a lint contract fails the build if that changes. Every rule that
decides a student's grade is therefore testable with no infrastructure at all — which
is why the result and maths engines ship with oracle-generated corpora of 304 and 502
cases respectively.

---

## Getting started

### Prerequisites

- **Python 3.12** and [`uv`](https://docs.astral.sh/uv/)
- **PostgreSQL 16**, reachable over a Unix socket (the defaults assume `/tmp`)
- **Node 20+** and `pnpm`

### Backend

```bash
cd backend
cp .env.example .env          # then replace every CHANGE_ME value
make install                  # dependencies into .venv
make db-bootstrap             # roles khata_owner/khata_app, databases khata_dev/khata_test
make migrate                  # apply the migration chain
make seed                     # one worked exam; refuses outside dev/test
make run                      # API on :8000
```

`.env.example` documents every setting and how to generate each secret. The app
refuses to start in a deployed environment with a placeholder value, with the Fake
marking provider, or with the dev OTP sender — failing loudly beats marking with
keyword matching or silently never sending a second factor.

### Web

```bash
cd web
pnpm install
pnpm dev                      # :5173, proxies /v1 to the API
pnpm dev:mock                 # or run against MSW mocks, no backend needed
```

### Signing in locally

`make seed` creates a teacher on `+8801712345678` whose password is
`KHATA_SEED_DEV_PASSWORD` from your `.env`. Sign-in needs an OTP the first time from
each browser; in dev the code is written to `backend/var/dev-otp.log` — read the last
line.

---

## Quality gates

Both halves must be green. `cd backend && make check` runs the backend set.

| Backend | Web |
|---|---|
| `make test` — 1,356 tests, 84% coverage | `pnpm test` — 47 tests |
| `make lint` — ruff lint + format | `pnpm lint` — eslint, no warnings |
| `make typecheck` — mypy over the whole package | `pnpm typecheck` — tsc |
| `make imports` — module boundary contracts | `pnpm i18n:check` — bn/en in step |
| | `pnpm format:check` · `pnpm build` |

Integration tests run against a real `khata_test` database — the RLS policies,
constraints and migration chain are the things most worth testing, and none of them
exist in a mock.

---

## Documentation

The product was specified before it was built. `docs/` is the source of truth; code
disagreeing with it is a bug in the code.

| | |
|---|---|
| [`00-research-synthesis.md`](docs/00-research-synthesis.md) | Verified facts, with confidence levels and open questions |
| [`01-PRD.md`](docs/01-PRD.md) | Users, scope, 106 functional requirements, success metrics |
| [`02-TRD.md`](docs/02-TRD.md) | Technical requirements and their test criteria |
| [`03-system-design.md`](docs/03-system-design.md) | Modules, entities, endpoints, pipelines |
| [`04-wireframes.md`](docs/04-wireframes.md) · [`05-ui-ux-design.md`](docs/05-ui-ux-design.md) | Screens, flows, design tokens |
| [`06-ai-model-decision-and-evaluation.md`](docs/06-ai-model-decision-and-evaluation.md) | Capability levels L0–L3, gates, metrics |
| [`07-hitl-and-continuous-improvement.md`](docs/07-hitl-and-continuous-improvement.md) | Human-in-the-loop, correction taxonomy |
| [`08-data-curriculum-security-privacy.md`](docs/08-data-curriculum-security-privacy.md) | Consent, RBAC, retention, threat model |
| [`09-qa-test-strategy.md`](docs/09-qa-test-strategy.md) · [`11-traceability-and-final-review.md`](docs/11-traceability-and-final-review.md) | Test strategy, traceability |
| [`10-registers.md`](docs/10-registers.md) | Decisions, assumptions, risks, experiments |

`docs/implementation/` tracks build state: the coverage audit, working context and
technical decisions.

---

## Notes for contributors

- **The engines stay pure.** If a rule decides a mark, it belongs in `engines/` with
  tests that need no database.
- **The AI never writes a mark.** Providers return suggestions; `engines.scoring`
  computes marks. Please do not route around this.
- **Bangla is not an afterthought.** Every user-facing string exists in both languages
  (`pnpm i18n:check` enforces it) and numerals follow the UI language.
- **Tests first.** Every defect found during this build was caught by a test written
  before the fix — including an OTP attempt limit that silently never fired.
