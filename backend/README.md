# Khata backend

Python 3.12 · FastAPI · SQLAlchemy 2 (sync) + psycopg 3 · Alembic · PostgreSQL 16.
Package name `khata`. See the [root README](../README.md) for the product, and
[`docs/03-system-design.md`](../docs/03-system-design.md) for the architecture.

## Setup

```bash
cp .env.example .env     # replace every CHANGE_ME value
make install             # dependencies into .venv
make db-bootstrap        # roles khata_owner/khata_app, databases khata_dev/khata_test
make migrate             # apply the migration chain
make seed                # one worked exam; refuses outside dev/test
make run                 # API on :8000
```

`make help` lists every target. `make check` runs everything CI runs.

## Layout

| Path | Contents |
|---|---|
| `src/khata/core/` | Config, DB session and tenant context, RFC 9457 errors, security, crypto, ids |
| `src/khata/engines/` | **Pure** deterministic code: rubric, scoring, results, mathcheck, bangla, workflow. No DB or I/O imports — enforced by `make imports`. |
| `src/khata/modules/<name>/` | One package per bounded context (`models.py`, `schemas.py`, `service.py`, `api.py`). Cross-module calls go through `service.py`. |
| `migrations/` | Alembic. One linear chain; every tenant table is under **FORCE** row-level security. |
| `tests/` | Unit tests for the engines; integration tests against a real `khata_test` database. |

## Two rules worth knowing before you edit

1. **Engines are pure.** Anything that decides a mark lives there and is tested with
   no infrastructure. `make imports` fails the build if an engine imports a module or
   `khata.core`.
2. **A provider never writes a mark.** `MarkingProvider.suggest` returns criterion
   decisions and evidence; `engines.scoring.score_item` computes the mark from the
   teacher's decision. The Fake provider is dev/test only and the app refuses to start
   with it in staging or production.
