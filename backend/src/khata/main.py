"""FastAPI application factory.

Wiring only: configuration, database, marking provider, middleware, error handlers
and routers. Business rules live in the modules; deterministic rules in the engines.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from khata.core.config import Environment, Settings, get_settings
from khata.core.db import Database
from khata.core.errors import install_error_handlers
from khata.core.logging import (
    CorrelationIdMiddleware,
    SecurityHeadersMiddleware,
    configure_logging,
)
from khata.modules.aigateway.fake import FakeMarkingProvider
from khata.modules.aigateway.provider import MarkingProvider
from khata.modules.assessment.api import router as assessment_router
from khata.modules.identity.api import router as identity_router

API_PREFIX = "/v1"
TITLE = "Khata API"
VERSION = "0.1.0"


def build_marking_provider(settings: Settings) -> MarkingProvider:
    """Choose the marking provider for this environment.

    Only the Fake provider exists so far. It is dev/test only, so a deployed
    environment must fail loudly rather than silently mark with keyword matching.
    """
    if settings.env in (Environment.STAGING, Environment.PRODUCTION):
        raise RuntimeError(
            "No production marking provider is configured; refusing to start with the Fake provider"
        )
    return FakeMarkingProvider()


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    configure_logging(resolved.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = resolved
        app.state.db = Database.from_settings(resolved)
        app.state.marking_provider = build_marking_provider(resolved)
        try:
            yield
        finally:
            app.state.db.dispose()

    app = FastAPI(
        title=TITLE,
        version=VERSION,
        lifespan=lifespan,
        docs_url="/docs" if resolved.expose_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if resolved.expose_docs else None,
    )

    # Order matters: correlation id is outermost so every log line and error carries it.
    app.add_middleware(SecurityHeadersMiddleware)
    if resolved.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=resolved.cors_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type", "X-Client", "Idempotency-Key"],
        )
    app.add_middleware(CorrelationIdMiddleware)

    install_error_handlers(app)

    app.include_router(identity_router, prefix=API_PREFIX)
    app.include_router(assessment_router, prefix=API_PREFIX)

    @app.get("/health", tags=["ops"], include_in_schema=False)
    def health() -> dict[str, object]:
        return {"status": "ok" if app.state.db.ping() else "degraded", "version": VERSION}

    return app
