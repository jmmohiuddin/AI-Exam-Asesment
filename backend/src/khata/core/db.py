"""Database engines and tenant-bound sessions (ADR-003).

* The **app engine** connects as ``khata_app`` (not owner, NOBYPASSRLS). All runtime
  code uses it, so PostgreSQL RLS is always the second authorisation layer.
* The **owner engine** (``khata_owner``) exists only for migrations and test setup.

Every unit of work is one transaction that first runs
``set_config('app.tenant_id', :tid, true)`` — transaction-local, so pooled
connections never leak a tenant between requests.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from khata.core.config import Settings

_BIND_CONTEXT_SQL = text(
    "SELECT set_config('app.tenant_id', :tenant_id, true),"
    " set_config('app.user_id', :user_id, true),"
    " set_config('app.platform_scope', :platform, true)"
)


def bind_context(
    session: Session,
    *,
    tenant_id: uuid.UUID | None,
    user_id: uuid.UUID | None = None,
    platform: bool = False,
) -> None:
    """Set the RLS context for the current transaction ('' means unset)."""
    session.execute(
        _BIND_CONTEXT_SQL,
        {
            "tenant_id": str(tenant_id) if tenant_id else "",
            "user_id": str(user_id) if user_id else "",
            "platform": "on" if platform else "",
        },
    )


def libpq_conninfo(sqlalchemy_url: str) -> str:
    """Convert ``postgresql+psycopg://…`` into a libpq URI (for procrastinate/psycopg)."""
    url = make_url(sqlalchemy_url).set(drivername="postgresql")
    return url.render_as_string(hide_password=False)


class Database:
    def __init__(
        self,
        app_url: str,
        owner_url: str | None = None,
        *,
        pool_size: int = 10,
        statement_timeout_ms: int = 30_000,
    ) -> None:
        self.app_engine: Engine = create_engine(
            app_url,
            pool_pre_ping=True,
            pool_size=pool_size,
            max_overflow=pool_size,
            connect_args={"options": f"-c statement_timeout={statement_timeout_ms}"},
        )
        self._owner_url = owner_url
        self._owner_engine: Engine | None = None
        self._sessions = sessionmaker(self.app_engine, expire_on_commit=False)

    @classmethod
    def from_settings(cls, settings: Settings) -> Database:
        return cls(
            settings.database_url_app,
            settings.database_url_owner,
            pool_size=settings.db_pool_size,
            statement_timeout_ms=settings.db_statement_timeout_ms,
        )

    @property
    def owner_engine(self) -> Engine:
        if self._owner_url is None:
            raise RuntimeError("owner database URL is not configured")
        if self._owner_engine is None:
            self._owner_engine = create_engine(self._owner_url, pool_pre_ping=True)
        return self._owner_engine

    @contextmanager
    def session_scope(
        self,
        tenant_id: uuid.UUID | None = None,
        *,
        user_id: uuid.UUID | None = None,
        platform: bool = False,
    ) -> Iterator[Session]:
        """One transaction with RLS context; commits on success, rolls back on error.

        ``user_id`` enables the membership policies (a user reading their own role
        assignments across tenants) and only applies when ``tenant_id`` is unset.
        ``platform`` enables platform-scope policies (tenant listing for maintenance).
        """
        session = self._sessions()
        try:
            with session.begin():
                bind_context(session, tenant_id=tenant_id, user_id=user_id, platform=platform)
                yield session
        finally:
            session.close()

    def ping(self) -> bool:
        try:
            with self.app_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return False
        return True

    def dispose(self) -> None:
        self.app_engine.dispose()
        if self._owner_engine is not None:
            self._owner_engine.dispose()
