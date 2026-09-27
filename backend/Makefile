# Khata backend developer tasks. Requires uv and a local PostgreSQL 16.
SHELL := /bin/bash
PG_SUPERUSER ?= $(USER)
PG_HOST ?= /tmp
ENV_FILE ?= .env

# Read a single KEY=value from .env without exporting the whole file.
env_value = $(shell grep -E '^$(1)=' $(ENV_FILE) | head -1 | cut -d= -f2- | sed -e 's/[[:space:]]*\#.*$$//')

.PHONY: help install db-bootstrap migrate migrate-test seed run worker test test-unit test-integration lint format typecheck imports check

help:
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-18s %s\n", $$1, $$2}'

install: ## Install dependencies into .venv
	uv sync

db-bootstrap: ## Create roles khata_owner/khata_app and databases khata_dev/khata_test (superuser)
	psql -h $(PG_HOST) -U $(PG_SUPERUSER) -d postgres \
	  -v owner_password='$(call env_value,KHATA_DB_OWNER_PASSWORD)' \
	  -v app_password='$(call env_value,KHATA_DB_APP_PASSWORD)' \
	  -f scripts/db_bootstrap.sql

migrate: ## Apply migrations to khata_dev (as khata_owner)
	uv run alembic upgrade head

seed: ## Seed dev data (refuses unless KHATA_ENV is dev|test)
	uv run python -m khata.scripts.seed_dev

run: ## Run the API with autoreload
	uv run uvicorn khata.main:create_app --factory --reload --port 8000

worker: ## Run the job worker
	uv run python -m khata.worker

test: ## Full test suite with coverage
	uv run pytest --cov

test-unit:
	uv run pytest -m unit

test-integration:
	uv run pytest -m integration

lint: ## Ruff lint + format check
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck: ## mypy (strict on khata.core)
	uv run mypy src/khata/core

imports: ## Module boundary contracts
	uv run lint-imports

check: lint typecheck imports test ## Everything CI runs
