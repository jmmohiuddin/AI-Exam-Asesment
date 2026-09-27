"""Item and exam state machines (07 §4.1 + ADR-004; 03 §14.1).

``transition(current, target, **ctx)`` returns ``target`` or raises
:class:`~khata.engines.errors.IllegalTransition` (the API maps it to 409).
Guards read only the explicit keyword context; unknown keys are a TypeError so
that a misspelt flag can never silently satisfy or skip a guard.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from enum import StrEnum
from types import MappingProxyType
from typing import Any, overload

from khata.engines.errors import IllegalTransition


class ItemState(StrEnum):
    PENDING = "pending"
    UNMAPPED = "unmapped"
    PROCESSING = "processing"
    FAILED = "failed"
    MANUAL_READY = "manual_ready"
    EVIDENCE_ONLY = "evidence_only"
    SUGGESTED = "suggested"
    CONFIRMED = "confirmed"
    EDITED = "edited"
    FLAGGED = "flagged"
    MODERATED = "moderated"
    LOCKED = "locked"
    RECHECK = "recheck"


class ExamState(StrEnum):
    DRAFT = "draft"
    RUBRIC_LOCKED = "rubric_locked"
    CAPTURING = "capturing"
    PROCESSING = "processing"
    REVIEWING = "reviewing"
    MODERATION = "moderation"
    MARKS_LOCKED = "marks_locked"
    PUBLISHED = "published"
    RECHECK = "recheck"


_I = ItemState
_E = ExamState

#: "Confirmed" and "Edited" both mean the mark is teacher-decided (07 §4.1).
TEACHER_DECIDED: frozenset[ItemState] = frozenset({_I.CONFIRMED, _I.EDITED})

ITEM_TRANSITIONS: Mapping[ItemState, frozenset[ItemState]] = MappingProxyType(
    {
        _I.PENDING: frozenset({_I.UNMAPPED, _I.PROCESSING, _I.MANUAL_READY}),
        _I.UNMAPPED: frozenset({_I.PENDING}),
        _I.PROCESSING: frozenset({_I.SUGGESTED, _I.EVIDENCE_ONLY, _I.UNMAPPED, _I.FAILED}),
        _I.FAILED: frozenset({_I.MANUAL_READY, _I.EVIDENCE_ONLY, _I.PROCESSING}),
        _I.MANUAL_READY: frozenset({_I.EDITED, _I.FLAGGED}),
        _I.EVIDENCE_ONLY: frozenset({_I.EDITED, _I.FLAGGED, _I.PROCESSING}),
        _I.SUGGESTED: frozenset({_I.CONFIRMED, _I.EDITED, _I.FLAGGED, _I.PROCESSING}),
        _I.CONFIRMED: frozenset({_I.MODERATED, _I.LOCKED, _I.FLAGGED}),
        _I.EDITED: frozenset({_I.MODERATED, _I.LOCKED, _I.FLAGGED}),
        _I.FLAGGED: frozenset({_I.EDITED, _I.CONFIRMED}),
        _I.MODERATED: frozenset({_I.LOCKED, _I.EDITED}),
        _I.LOCKED: frozenset({_I.RECHECK, _I.CONFIRMED, _I.EDITED}),
        _I.RECHECK: frozenset({_I.LOCKED}),
    }
)

EXAM_TRANSITIONS: Mapping[ExamState, frozenset[ExamState]] = MappingProxyType(
    {
        _E.DRAFT: frozenset({_E.RUBRIC_LOCKED}),
        _E.RUBRIC_LOCKED: frozenset({_E.DRAFT, _E.CAPTURING}),
        _E.CAPTURING: frozenset({_E.PROCESSING, _E.REVIEWING}),
        _E.PROCESSING: frozenset({_E.REVIEWING}),
        _E.REVIEWING: frozenset({_E.MODERATION}),
        _E.MODERATION: frozenset({_E.MARKS_LOCKED}),
        _E.MARKS_LOCKED: frozenset({_E.REVIEWING, _E.PUBLISHED}),
        _E.PUBLISHED: frozenset({_E.RECHECK}),
        _E.RECHECK: frozenset({_E.PUBLISHED}),
    }
)

KNOWN_CONTEXT_KEYS = frozenset(
    {
        "via_exam_unlock",
        "rubric_validation_passed",
        "scripts_captured",
        "rolling_mode",
        "all_items_decided",
        "completeness_ok",
        "moderation_done",
        "otp_verified",
        "reason",
    }
)

Guard = Callable[[Mapping[str, Any]], str | None]


def _require_flag(key: str, message: str) -> Guard:
    def guard(ctx: Mapping[str, Any]) -> str | None:
        return None if ctx.get(key) is True else message

    return guard


def _all_of(*guards: Guard) -> Guard:
    def guard(ctx: Mapping[str, Any]) -> str | None:
        for check in guards:
            failure = check(ctx)
            if failure is not None:
                return failure
        return None

    return guard


def _no_scripts(ctx: Mapping[str, Any]) -> str | None:
    count = ctx.get("scripts_captured")
    if isinstance(count, int) and not isinstance(count, bool) and count == 0:
        return None
    return "rubric unlock requires scripts_captured == 0"


def _has_reason(ctx: Mapping[str, Any]) -> str | None:
    reason = ctx.get("reason")
    return None if isinstance(reason, str) and reason.strip() else "unlock requires a reason"


_OTP = _require_flag("otp_verified", "requires OTP verification")
_EXAM_UNLOCK = _require_flag("via_exam_unlock", "locked items reopen only via exam unlock")

ITEM_GUARDS: Mapping[tuple[ItemState, ItemState], Guard] = MappingProxyType(
    {
        (_I.LOCKED, _I.CONFIRMED): _EXAM_UNLOCK,
        (_I.LOCKED, _I.EDITED): _EXAM_UNLOCK,
    }
)

EXAM_GUARDS: Mapping[tuple[ExamState, ExamState], Guard] = MappingProxyType(
    {
        (_E.DRAFT, _E.RUBRIC_LOCKED): _require_flag(
            "rubric_validation_passed", "rubric lock requires validation to pass"
        ),
        (_E.RUBRIC_LOCKED, _E.DRAFT): _no_scripts,
        (_E.CAPTURING, _E.REVIEWING): _require_flag(
            "rolling_mode", "capturing -> reviewing only in rolling mode"
        ),
        (_E.REVIEWING, _E.MODERATION): _require_flag(
            "all_items_decided", "moderation requires all items decided"
        ),
        (_E.MODERATION, _E.MARKS_LOCKED): _all_of(
            _require_flag("completeness_ok", "marks lock requires completeness"),
            _require_flag("moderation_done", "marks lock requires moderation done"),
        ),
        (_E.MARKS_LOCKED, _E.REVIEWING): _all_of(_has_reason, _OTP),
        (_E.MARKS_LOCKED, _E.PUBLISHED): _OTP,
        (_E.RECHECK, _E.PUBLISHED): _OTP,
    }
)


def allowed_targets(state: ItemState | ExamState) -> frozenset[Any]:
    """Raw edge targets of ``state`` (guards not evaluated)."""
    if isinstance(state, ItemState):
        return ITEM_TRANSITIONS[state]
    return EXAM_TRANSITIONS[state]


def is_legal(current: ItemState | ExamState, target: ItemState | ExamState) -> bool:
    """True when ``current -> target`` is an edge (guards not evaluated)."""
    if type(current) is not type(target):
        return False
    return target in allowed_targets(current)


@overload
def transition(current: ItemState, target: ItemState, **ctx: Any) -> ItemState: ...
@overload
def transition(current: ExamState, target: ExamState, **ctx: Any) -> ExamState: ...
def transition(current: ItemState | ExamState, target: ItemState | ExamState, **ctx: Any) -> Any:
    unknown = set(ctx) - KNOWN_CONTEXT_KEYS
    if unknown:
        raise TypeError(f"unknown transition context keys: {sorted(unknown)}")
    if type(current) is not type(target):
        raise TypeError("current and target must be the same state enum")
    if target not in allowed_targets(current):
        raise IllegalTransition(current, target, "not an edge of the state machine")
    guards: Mapping[Any, Guard] = ITEM_GUARDS if isinstance(current, ItemState) else EXAM_GUARDS
    guard = guards.get((current, target))
    failure = guard(ctx) if guard is not None else None
    if failure is not None:
        raise IllegalTransition(current, target, failure)
    return target
