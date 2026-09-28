"""RFC 9457 problem details with stable codes and Bangla/English messages (TR-API-03, TR-ERR-03).

Every error response is ``application/problem+json``::

    {type, title, status, detail, instance, code, message_bn, message_en,
     support_code, correlation_id, errors?, ...extra}

Internal details never leave the server: unexpected exceptions are logged with the
support code and the client receives only the code.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from khata.core.ids import support_code
from khata.core.logging import CORRELATION_HEADER, get_correlation_id

logger = logging.getLogger("khata.errors")

PROBLEM_CONTENT_TYPE = "application/problem+json"
PROBLEM_TYPE_PREFIX = "urn:khata:error:"


@dataclass(frozen=True, slots=True)
class ErrorSpec:
    status: int
    title: str
    message_en: str
    message_bn: str


CATALOGUE: Mapping[str, ErrorSpec] = {
    # Generic
    "BAD_REQUEST": ErrorSpec(
        400, "Bad request", "The request could not be processed.", "অনুরোধটি প্রক্রিয়া করা যায়নি।"
    ),
    "VALIDATION_FAILED": ErrorSpec(
        422,
        "Validation failed",
        "Some fields are missing or invalid.",
        "কিছু তথ্য অনুপস্থিত বা ভুল।",
    ),
    "UNAUTHENTICATED": ErrorSpec(
        401, "Not signed in", "Please sign in again.", "অনুগ্রহ করে আবার সাইন ইন করুন।"
    ),
    "TOKEN_EXPIRED": ErrorSpec(
        401, "Session expired", "Your session has expired.", "আপনার সেশনের মেয়াদ শেষ হয়েছে।"
    ),
    "SESSION_REVOKED": ErrorSpec(
        401, "Session ended", "This session has been signed out.", "এই সেশন থেকে সাইন আউট করা হয়েছে।"
    ),
    "PERMISSION_DENIED": ErrorSpec(
        403,
        "Permission denied",
        "You do not have permission to do this.",
        "এই কাজটি করার অনুমতি আপনার নেই।",
    ),
    "NOT_FOUND": ErrorSpec(404, "Not found", "The item was not found.", "খুঁজে পাওয়া যায়নি।"),
    "METHOD_NOT_ALLOWED": ErrorSpec(
        405, "Method not allowed", "This action is not supported.", "এই কাজটি সমর্থিত নয়।"
    ),
    "CONFLICT": ErrorSpec(
        409,
        "Conflict",
        "This change conflicts with the current state.",
        "এই পরিবর্তনটি বর্তমান অবস্থার সাথে সাংঘর্ষিক।",
    ),
    "ALREADY_EXISTS": ErrorSpec(
        409, "Already exists", "This already exists.", "এটি আগে থেকেই আছে।"
    ),
    "RATE_LIMITED": ErrorSpec(
        429,
        "Too many requests",
        "Too many attempts. Please wait and try again.",
        "অনেকবার চেষ্টা করা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।",
    ),
    "INTERNAL_ERROR": ErrorSpec(
        500,
        "Internal error",
        "Something went wrong. Please try again or contact support with the code.",
        "কিছু একটা সমস্যা হয়েছে। আবার চেষ্টা করুন অথবা কোডসহ সহায়তায় যোগাযোগ করুন।",
    ),
    "SERVICE_UNAVAILABLE": ErrorSpec(
        503,
        "Service unavailable",
        "The service is temporarily unavailable.",
        "সেবাটি সাময়িকভাবে বন্ধ আছে।",
    ),
    "INVALID_CURSOR": ErrorSpec(
        400, "Invalid cursor", "The page link is invalid.", "পৃষ্ঠার লিংকটি সঠিক নয়।"
    ),
    "IDEMPOTENCY_KEY_INVALID": ErrorSpec(
        400, "Invalid idempotency key", "The request key is invalid.", "অনুরোধের কী সঠিক নয়।"
    ),
    "IDEMPOTENCY_KEY_CONFLICT": ErrorSpec(
        409,
        "Idempotency key reused",
        "This request key was already used for a different request.",
        "এই অনুরোধের কী অন্য একটি অনুরোধে ব্যবহার করা হয়েছে।",
    ),
    # Authentication
    "INVALID_CREDENTIALS": ErrorSpec(
        401,
        "Invalid credentials",
        "Mobile number or password is incorrect.",
        "মোবাইল নম্বর বা পাসওয়ার্ড সঠিক নয়।",
    ),
    "ACCOUNT_LOCKED": ErrorSpec(
        423,
        "Account locked",
        "Too many failed attempts. The account is locked for a while.",
        "অনেকবার ভুল চেষ্টার কারণে অ্যাকাউন্টটি কিছুক্ষণের জন্য বন্ধ আছে।",
    ),
    "OTP_INVALID": ErrorSpec(400, "Invalid code", "The code is incorrect.", "কোডটি সঠিক নয়।"),
    "OTP_EXPIRED": ErrorSpec(
        400,
        "Code expired",
        "The code has expired. Request a new one.",
        "কোডের মেয়াদ শেষ। নতুন কোড নিন।",
    ),
    "OTP_ATTEMPTS_EXCEEDED": ErrorSpec(
        400,
        "Too many wrong codes",
        "Too many wrong codes. Please sign in again.",
        "অনেকবার ভুল কোড দেওয়া হয়েছে। আবার সাইন ইন করুন।",
    ),
    "OTP_RATE_LIMITED": ErrorSpec(
        429,
        "Too many codes requested",
        "Too many codes were sent. Please try again later.",
        "অনেকবার কোড পাঠানো হয়েছে। পরে আবার চেষ্টা করুন।",
    ),
    "REFRESH_INVALID": ErrorSpec(
        401, "Session expired", "Please sign in again.", "অনুগ্রহ করে আবার সাইন ইন করুন।"
    ),
    "REFRESH_REUSED": ErrorSpec(
        401,
        "Session ended for safety",
        "This session was ended for your safety. Please sign in again.",
        "নিরাপত্তার জন্য এই সেশনটি বন্ধ করা হয়েছে। আবার সাইন ইন করুন।",
    ),
    "CSRF_CHECK_FAILED": ErrorSpec(
        403, "Request blocked", "The request was blocked.", "অনুরোধটি আটকানো হয়েছে।"
    ),
    "NO_ACTIVE_TENANT": ErrorSpec(
        403,
        "No organisation selected",
        "Select an organisation to continue.",
        "চালিয়ে যেতে একটি প্রতিষ্ঠান নির্বাচন করুন।",
    ),
    "NOT_A_MEMBER": ErrorSpec(
        403,
        "Not a member",
        "You do not have a role in this organisation.",
        "এই প্রতিষ্ঠানে আপনার কোনো দায়িত্ব নেই।",
    ),
    "STEP_UP_REQUIRED": ErrorSpec(
        403,
        "Verification required",
        "Confirm with the code sent to your mobile.",
        "আপনার মোবাইলে পাঠানো কোড দিয়ে নিশ্চিত করুন।",
    ),
    "PASSWORD_TOO_WEAK": ErrorSpec(
        422,
        "Password too weak",
        "Use at least 10 characters and avoid common passwords.",
        "কমপক্ষে ১০ অক্ষর ব্যবহার করুন এবং সহজ পাসওয়ার্ড এড়িয়ে চলুন।",
    ),
    # Organisation / staff
    "ROLE_NOT_ASSIGNABLE": ErrorSpec(
        403,
        "Role not assignable",
        "You cannot assign this role.",
        "আপনি এই দায়িত্বটি দিতে পারবেন না।",
    ),
    "CANNOT_REMOVE_OWN_ADMIN": ErrorSpec(
        409,
        "Cannot remove own admin role",
        "You cannot remove your own administrator role.",
        "আপনি নিজের প্রশাসকের দায়িত্ব সরাতে পারবেন না।",
    ),
    # Results
    "EXAM_HAS_NO_ITEMS": ErrorSpec(
        409,
        "No questions yet",
        "Add the paper's questions before asking for results.",
        "ফলাফল দেখার আগে প্রশ্নগুলো যোগ করুন।",
    ),
}


class DomainError(Exception):
    """An expected failure with a stable code from :data:`CATALOGUE`."""

    def __init__(
        self,
        code: str,
        detail: str | None = None,
        *,
        extra: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        if code not in CATALOGUE:
            raise ValueError(f"Unknown error code {code!r}")
        super().__init__(detail or code)
        self.code = code
        self.spec = CATALOGUE[code]
        self.detail = detail
        self.extra: Mapping[str, Any] = dict(extra or {})
        self.headers: Mapping[str, str] = dict(headers or {})


def problem_body(
    code: str,
    *,
    detail: str | None = None,
    instance: str | None = None,
    extra: Mapping[str, Any] | None = None,
    errors: Sequence[Mapping[str, Any]] | None = None,
    support: str | None = None,
) -> dict[str, Any]:
    spec = CATALOGUE[code]
    body: dict[str, Any] = {
        "type": f"{PROBLEM_TYPE_PREFIX}{code}",
        "title": spec.title,
        "status": spec.status,
        "detail": detail or spec.message_en,
        "code": code,
        "message_bn": spec.message_bn,
        "message_en": spec.message_en,
        "support_code": support or support_code(),
        "correlation_id": get_correlation_id(),
    }
    if instance:
        body["instance"] = instance
    if errors is not None:
        body["errors"] = list(errors)
    for key, value in (extra or {}).items():
        body.setdefault(key, value)
    return body


def problem_response(
    code: str,
    *,
    request: Request | None = None,
    detail: str | None = None,
    extra: Mapping[str, Any] | None = None,
    errors: Sequence[Mapping[str, Any]] | None = None,
    headers: Mapping[str, str] | None = None,
    support: str | None = None,
) -> JSONResponse:
    body = problem_body(
        code,
        detail=detail,
        instance=request.url.path if request else None,
        extra=extra,
        errors=errors,
        support=support,
    )
    all_headers = {CORRELATION_HEADER: body["correlation_id"], **(headers or {})}
    return JSONResponse(
        body, status_code=body["status"], headers=all_headers, media_type=PROBLEM_CONTENT_TYPE
    )


_STATUS_CODES: Mapping[int, str] = {
    400: "BAD_REQUEST",
    401: "UNAUTHENTICATED",
    403: "PERMISSION_DENIED",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_FAILED",
    429: "RATE_LIMITED",
    503: "SERVICE_UNAVAILABLE",
}


def _validation_errors(exc: RequestValidationError) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for err in exc.errors():
        location = [str(part) for part in err.get("loc", ()) if part not in ("body",)]
        # Never echo the submitted value back: it may contain a password or OTP.
        items.append(
            {
                "field": ".".join(location),
                "code": str(err.get("type", "invalid")),
                "message": str(err.get("msg", "Invalid value")),
            }
        )
    return items


async def _domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, DomainError)
    return problem_response(
        exc.code, request=request, detail=exc.detail, extra=exc.extra, headers=exc.headers
    )


async def _validation_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    return problem_response("VALIDATION_FAILED", request=request, errors=_validation_errors(exc))


async def _http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    code = _STATUS_CODES.get(exc.status_code, "BAD_REQUEST")
    if exc.status_code >= 500:
        code = "INTERNAL_ERROR"
    return problem_response(code, request=request, headers=exc.headers)


async def _unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
    support = support_code()
    logger.error(
        "unhandled_exception",
        exc_info=exc,
        extra={"support_code": support, "path": request.url.path, "method": request.method},
    )
    return problem_response("INTERNAL_ERROR", request=request, support=support)


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, _domain_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(Exception, _unhandled_handler)
