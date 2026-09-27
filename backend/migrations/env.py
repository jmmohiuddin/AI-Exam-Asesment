"""Alembic environment. Migrations are forward-only and run as ``khata_owner``."""

from __future__ import annotations

import os

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config


def _database_url() -> str:
    explicit = context.get_x_argument(as_dictionary=True).get("db_url")
    if explicit:
        return explicit
    configured = config.attributes.get("db_url") or os.environ.get("KHATA_DATABASE_URL_OWNER")
    if configured:
        return str(configured)
    from khata.core.config import get_settings

    owner_url = get_settings().database_url_owner
    if not owner_url:
        raise RuntimeError("KHATA_DATABASE_URL_OWNER is required to run migrations")
    return owner_url


def run_migrations_online() -> None:
    engine = create_engine(_database_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, transaction_per_migration=True)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    raise RuntimeError("Offline (SQL script) migrations are not supported")
run_migrations_online()
