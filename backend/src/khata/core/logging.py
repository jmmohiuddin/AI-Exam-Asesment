"""Structured JSON logging, correlation IDs and the PII scrubber (TR-OBS-01, TR-PRV-04).

The scrubber runs on every record: sensitive keys in ``extra`` are replaced, and
free text (message, exception text) is pattern-redacted for mobile numbers, emails,
bearer tokens and JWTs. It is a safety net; code must still avoid logging PII.
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
import uuid
from collections.abc import Mapping
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

CORRELATION_HEADER = "X-Correlation-ID"
REDACTED = "[REDACTED]"

_correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)
_VALID_CORRELATION = re.compile(r"^[A-Za-z0-9._-]{8,64}$")

SENSITIVE_KEY_FRAGMENTS = (
    "password",
    "passwd",
    "secret",
    "token",
    "otp",
    "mobile",
    "phone",
    "authorization",
    "cookie",
    "code_hmac",
    "dek",
)
SENSITIVE_KEYS = frozenset(
    {"name", "name_bn", "name_en", "full_name", "student_name", "device_name", "code"}
)

_TEXT_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"eyJ[\w-]+\.[\w-]+\.[\w-]+"), "[TOKEN]"),
    (re.compile(r"(?i)bearer\s+\S+"), "Bearer [TOKEN]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[EMAIL]"),
    (re.compile(r"(?<!\d)(?:\+?880|0)1[3-9]\d{8}(?!\d)"), "[MOBILE]"),
    (re.compile(r"(?<![\w-])\+[1-9]\d{9,14}(?!\d)"), "[MOBILE]"),
)

_STANDARD_ATTRS = frozenset(
    vars(logging.LogRecord("", 0, "", 0, "", None, None)).keys() | {"message", "asctime"}
)


def get_correlation_id() -> str | None:
    return _correlation_id.get()


def set_correlation_id(value: str | None) -> None:
    _correlation_id.set(value)


def new_correlation_id() -> str:
    return uuid.uuid4().hex


def scrub_text(text: str) -> str:
    for pattern, replacement in _TEXT_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _is_sensitive_key(key: str) -> bool:
    lowered = key.lower()
    return lowered in SENSITIVE_KEYS or any(frag in lowered for frag in SENSITIVE_KEY_FRAGMENTS)


def scrub_value(value: Any, key: str | None = None) -> Any:
    """Return a scrubbed copy of ``value`` (never mutates the input)."""
    if key is not None and _is_sensitive_key(key):
        return REDACTED
    if isinstance(value, str):
        return scrub_text(value)
    if isinstance(value, Mapping):
        return {str(k): scrub_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, list | tuple | set | frozenset):
        return [scrub_value(item) for item in value]
    return value


class PiiScrubbingFilter(logging.Filter):
    """Redacts PII from the message and extras before any handler sees the record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = scrub_text(record.getMessage())
        record.args = None
        for attr, value in list(vars(record).items()):
            if attr not in _STANDARD_ATTRS:
                setattr(record, attr, scrub_value(value, attr))
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
        }
        for attr, value in vars(record).items():
            if attr not in _STANDARD_ATTRS and attr not in payload:
                payload[attr] = value
        if record.exc_info:
            payload["exc"] = scrub_text(self.formatException(record.exc_info))
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(PiiScrubbingFilter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
    for noisy in ("uvicorn.access",):
        logging.getLogger(noisy).handlers = []
        logging.getLogger(noisy).propagate = False


class CorrelationIdMiddleware:
    """Accepts a well-formed ``X-Correlation-ID`` or generates one; echoes it and logs access."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.logger = logging.getLogger("khata.access")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        incoming = _header(scope, CORRELATION_HEADER.lower())
        correlation = (
            incoming if incoming and _VALID_CORRELATION.match(incoming) else new_correlation_id()
        )
        set_correlation_id(correlation)
        started = time.perf_counter()
        status: dict[str, int] = {"code": 500}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message)[CORRELATION_HEADER] = correlation
                status["code"] = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            self.logger.info(
                "request",
                extra={
                    "method": scope.get("method"),
                    "path": scope.get("path"),
                    "status": status["code"],
                    "duration_ms": round((time.perf_counter() - started) * 1000, 1),
                },
            )


class SecurityHeadersMiddleware:
    """Conservative headers for a JSON API; responses carry personal data, so never cache."""

    HEADERS = (
        ("x-content-type-options", "nosniff"),
        ("x-frame-options", "DENY"),
        ("referrer-policy", "no-referrer"),
        ("cache-control", "no-store"),
    )

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                for name, value in self.HEADERS:
                    headers.setdefault(name, value)
            await send(message)

        await self.app(scope, receive, send_wrapper)


def _header(scope: Scope, name: str) -> str | None:
    target = name.encode("latin-1")
    for key, value in scope.get("headers", []):
        if key == target:
            decoded: str = value.decode("latin-1")
            return decoded
    return None
