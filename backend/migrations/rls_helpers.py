"""Helpers shared by migrations: raw SQL execution, tenant RLS and app-role grants.

Every tenant-owned table MUST go through :func:`enable_tenant_rls`; the isolation
suite (tests/integration/test_tenant_isolation.py) fails for any table that does not.
"""

from __future__ import annotations

from alembic import op

APP_ROLE = "khata_app"


def run_sql(sql: str) -> None:
    """Execute raw SQL on the driver (no bind-parameter parsing; multi-statement OK).

    Goes straight to the psycopg cursor with no parameter sequence. ``exec_driver_sql``
    would hand psycopg an empty parameter tuple, which turns on placeholder parsing and
    rejects a bare ``%`` — and the vendored procrastinate schema legitimately contains
    ``%`` in PL/pgSQL ``RAISE`` format strings. That file is upstream's, so it is kept
    byte-for-byte and the escaping problem is solved here instead.
    """
    driver_connection = op.get_bind().connection.driver_connection
    with driver_connection.cursor() as cursor:
        cursor.execute(sql)


def enable_tenant_rls(table: str, column: str = "tenant_id", *, nullable: bool = False) -> None:
    """ENABLE + FORCE RLS with the standard tenant policy (USING and WITH CHECK)."""
    predicate = (
        f"{column} IS NOT DISTINCT FROM app_current_tenant()"
        if nullable
        else f"{column} = app_current_tenant()"
    )
    run_sql(
        f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"
        f" ALTER TABLE {table} FORCE ROW LEVEL SECURITY;"
        f" CREATE POLICY tenant_isolation ON {table}"
        f" USING ({predicate}) WITH CHECK ({predicate});"
    )


def grant_app(table: str, privileges: str) -> None:
    run_sql(f"GRANT {privileges} ON {table} TO {APP_ROLE};")
