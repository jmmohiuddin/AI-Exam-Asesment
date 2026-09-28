"""OTP challenges: create, resend, verify (TR-AUTH-02, 08 §5.2).

Six digits is a small space, so the stored value is an HMAC keyed with a pepper
that lives outside the database (``otp_pepper``) and bound to the challenge id, and
every challenge counts its attempts. Three separate limits apply, and they mean
different things:

* **attempts** — wrong codes against one challenge. Exceeding it kills the
  challenge (``dead_at``); the right code afterwards no longer works. The count is
  written in its own transaction, because the request that made the wrong guess
  ends in a rollback — book-keeping that shares that transaction is erased, and an
  attacker gets unlimited guesses at a six-digit code.
* **expiry** — five minutes, so a code read from an old SMS is useless.
* **sends per hour, per user** — what stops the endpoint from being used to send
  someone an SMS every second.

A resend replaces the code rather than adding a second valid one: two live codes
would double the guessing surface for no benefit.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from khata.core.config import Settings
from khata.core.db import Database
from khata.core.errors import DomainError
from khata.core.models import utcnow
from khata.core.security import constant_time_equals, generate_otp_code, otp_hmac
from khata.modules.identity.delivery import OtpSender
from khata.modules.identity.models import AppUser, OtpChallenge, OtpSend

PURPOSE_LOGIN = "login"
PURPOSE_RESET = "reset"
PURPOSE_STEP_UP = "step_up"


@dataclass(frozen=True)
class Challenge:
    id: uuid.UUID
    expires_at: datetime


def start_challenge(
    session: Session,
    settings: Settings,
    sender: OtpSender,
    *,
    user: AppUser,
    purpose: str = PURPOSE_LOGIN,
    client: str = "web",
    session_id: uuid.UUID | None = None,
    step_up_purpose: str | None = None,
    now: datetime | None = None,
) -> Challenge:
    moment = now or utcnow()
    _check_send_budget(session, settings, user_id=user.id, now=moment)

    challenge = OtpChallenge(
        user_id=user.id,
        purpose=purpose,
        step_up_purpose=step_up_purpose,
        session_id=session_id,
        client=client,
        code_hmac="",  # replaced below: the HMAC is bound to the row's own id
        expires_at=moment + timedelta(seconds=settings.otp_ttl_seconds),
        last_sent_at=moment,
    )
    session.add(challenge)
    session.flush()
    _issue_code(session, settings, sender, user=user, challenge=challenge, now=moment)
    return Challenge(id=challenge.id, expires_at=challenge.expires_at)


def resend(
    session: Session,
    settings: Settings,
    sender: OtpSender,
    *,
    challenge_id: uuid.UUID,
    now: datetime | None = None,
) -> Challenge:
    """Issue a fresh code for a live challenge, invalidating the previous one."""
    moment = now or utcnow()
    challenge = session.get(OtpChallenge, challenge_id)
    if challenge is None or not _is_live(challenge, moment):
        raise DomainError("OTP_INVALID")
    user = session.get(AppUser, challenge.user_id)
    if user is None or not user.is_active:  # pragma: no cover - FK guarantees the row
        raise DomainError("OTP_INVALID")

    _check_send_budget(session, settings, user_id=challenge.user_id, now=moment)
    challenge.expires_at = moment + timedelta(seconds=settings.otp_ttl_seconds)
    challenge.last_sent_at = moment
    challenge.send_count += 1
    challenge.attempts = 0
    _issue_code(session, settings, sender, user=user, challenge=challenge, now=moment)
    return Challenge(id=challenge.id, expires_at=challenge.expires_at)


def verify(
    session: Session,
    settings: Settings,
    database: Database,
    *,
    challenge_id: uuid.UUID,
    code: str,
    purpose: str = PURPOSE_LOGIN,
    now: datetime | None = None,
) -> OtpChallenge:
    """Consume a challenge, or raise. The caller decides what the proof unlocks."""
    moment = now or utcnow()
    challenge = session.get(OtpChallenge, challenge_id)
    # An unknown, consumed or wrong-purpose challenge is reported as a wrong code:
    # saying which it was would confirm that a challenge id exists.
    if challenge is None or challenge.purpose != purpose or challenge.consumed_at is not None:
        raise DomainError("OTP_INVALID")
    if challenge.dead_at is not None or challenge.attempts >= settings.otp_max_attempts:
        raise DomainError("OTP_ATTEMPTS_EXCEEDED")
    if challenge.expires_at <= moment:
        raise DomainError("OTP_EXPIRED")

    expected = otp_hmac(settings.otp_pepper.get_secret_value(), challenge.id, code)
    if not constant_time_equals(expected, challenge.code_hmac):
        _record_failed_attempt(database, settings, challenge_id=challenge.id, now=moment)
        raise DomainError("OTP_INVALID")

    challenge.consumed_at = moment
    session.flush()
    return challenge


def _record_failed_attempt(
    database: Database, settings: Settings, *, challenge_id: uuid.UUID, now: datetime
) -> None:
    """Count one wrong guess in a transaction of its own, so the rollback that
    follows the raised error cannot erase it."""
    with database.session_scope(None) as bookkeeping:
        challenge = bookkeeping.get(OtpChallenge, challenge_id)
        if challenge is None:  # pragma: no cover - read moments ago
            return
        challenge.attempts += 1
        if challenge.attempts >= settings.otp_max_attempts:
            challenge.dead_at = now


def _issue_code(
    session: Session,
    settings: Settings,
    sender: OtpSender,
    *,
    user: AppUser,
    challenge: OtpChallenge,
    now: datetime,
) -> None:
    code = generate_otp_code()
    challenge.code_hmac = otp_hmac(settings.otp_pepper.get_secret_value(), challenge.id, code)
    session.add(OtpSend(user_id=user.id, challenge_id=challenge.id, sent_at=now))
    session.flush()
    sender.send(user.mobile, code, challenge.purpose)


def _check_send_budget(
    session: Session, settings: Settings, *, user_id: uuid.UUID, now: datetime
) -> None:
    window_start = now - timedelta(hours=1)
    sent = session.scalar(
        select(func.count())
        .select_from(OtpSend)
        .where(OtpSend.user_id == user_id, OtpSend.sent_at >= window_start)
    )
    if (sent or 0) >= settings.otp_sends_per_hour:
        raise DomainError("OTP_RATE_LIMITED")


def _is_live(challenge: OtpChallenge, now: datetime) -> bool:
    return (
        challenge.consumed_at is None and challenge.dead_at is None and challenge.expires_at > now
    )
