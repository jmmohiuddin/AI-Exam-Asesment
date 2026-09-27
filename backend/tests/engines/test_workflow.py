from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from khata.engines.errors import IllegalTransition
from khata.engines.workflow import (
    EXAM_TRANSITIONS,
    ITEM_TRANSITIONS,
    TEACHER_DECIDED,
    ExamState,
    ItemState,
    allowed_targets,
    is_legal,
    transition,
)

I = ItemState  # noqa: E741
E = ExamState

EXPECTED_ITEM_EDGES = {
    # 07 §4.1
    (I.PENDING, I.UNMAPPED),
    (I.UNMAPPED, I.PENDING),
    (I.PENDING, I.PROCESSING),
    (I.PENDING, I.MANUAL_READY),
    (I.PROCESSING, I.SUGGESTED),
    (I.PROCESSING, I.EVIDENCE_ONLY),
    (I.SUGGESTED, I.CONFIRMED),
    (I.SUGGESTED, I.EDITED),
    (I.EVIDENCE_ONLY, I.EDITED),
    (I.MANUAL_READY, I.EDITED),
    (I.SUGGESTED, I.FLAGGED),
    (I.EVIDENCE_ONLY, I.FLAGGED),
    (I.FLAGGED, I.EDITED),
    (I.CONFIRMED, I.MODERATED),
    (I.EDITED, I.MODERATED),
    (I.MODERATED, I.LOCKED),
    (I.CONFIRMED, I.LOCKED),
    (I.EDITED, I.LOCKED),
    (I.LOCKED, I.RECHECK),
    (I.RECHECK, I.LOCKED),
    # ADR-004 extensions
    (I.PROCESSING, I.UNMAPPED),
    (I.PROCESSING, I.FAILED),
    (I.FAILED, I.MANUAL_READY),
    (I.FAILED, I.EVIDENCE_ONLY),
    (I.FAILED, I.PROCESSING),
    (I.SUGGESTED, I.PROCESSING),
    (I.EVIDENCE_ONLY, I.PROCESSING),
    (I.FLAGGED, I.CONFIRMED),
    (I.MANUAL_READY, I.FLAGGED),
    (I.CONFIRMED, I.FLAGGED),
    (I.EDITED, I.FLAGGED),
    (I.MODERATED, I.EDITED),
    (I.LOCKED, I.CONFIRMED),
    (I.LOCKED, I.EDITED),
}

EXPECTED_EXAM_EDGES = {
    (E.DRAFT, E.RUBRIC_LOCKED),
    (E.RUBRIC_LOCKED, E.DRAFT),
    (E.RUBRIC_LOCKED, E.CAPTURING),
    (E.CAPTURING, E.PROCESSING),
    (E.PROCESSING, E.REVIEWING),
    (E.CAPTURING, E.REVIEWING),
    (E.REVIEWING, E.MODERATION),
    (E.MODERATION, E.MARKS_LOCKED),
    (E.MARKS_LOCKED, E.REVIEWING),
    (E.MARKS_LOCKED, E.PUBLISHED),
    (E.PUBLISHED, E.RECHECK),
    (E.RECHECK, E.PUBLISHED),
}

# Context that satisfies every guard; used to probe the raw edge set.
PERMISSIVE_CTX: dict[str, Any] = {
    "via_exam_unlock": True,
    "rubric_validation_passed": True,
    "scripts_captured": 0,
    "rolling_mode": True,
    "all_items_decided": True,
    "completeness_ok": True,
    "moderation_done": True,
    "otp_verified": True,
    "reason": "re-open for correction",
}


def test_item_states_are_exactly_the_adr_004_set() -> None:
    assert {s.value for s in ItemState} == {
        "pending",
        "unmapped",
        "processing",
        "failed",
        "manual_ready",
        "evidence_only",
        "suggested",
        "confirmed",
        "edited",
        "flagged",
        "moderated",
        "locked",
        "recheck",
    }
    assert "not_attempted" not in {s.value for s in ItemState}


def test_item_edge_set_matches_spec_exactly() -> None:
    actual = {(src, dst) for src, targets in ITEM_TRANSITIONS.items() for dst in targets}
    assert actual == EXPECTED_ITEM_EDGES


def test_exam_edge_set_matches_spec_exactly() -> None:
    actual = {(src, dst) for src, targets in EXAM_TRANSITIONS.items() for dst in targets}
    assert actual == EXPECTED_EXAM_EDGES


@pytest.mark.parametrize(("src", "dst"), sorted(EXPECTED_ITEM_EDGES))
def test_every_item_edge_is_legal_with_satisfied_guards(src: ItemState, dst: ItemState) -> None:
    assert transition(src, dst, **PERMISSIVE_CTX) is dst


@pytest.mark.parametrize(("src", "dst"), sorted(EXPECTED_EXAM_EDGES))
def test_every_exam_edge_is_legal_with_satisfied_guards(src: ExamState, dst: ExamState) -> None:
    assert transition(src, dst, **PERMISSIVE_CTX) is dst


@pytest.mark.parametrize("src", list(ItemState))
@pytest.mark.parametrize("dst", list(ItemState))
def test_non_edges_raise_illegal_transition(src: ItemState, dst: ItemState) -> None:
    if (src, dst) in EXPECTED_ITEM_EDGES:
        return
    with pytest.raises(IllegalTransition) as info:
        transition(src, dst, **PERMISSIVE_CTX)
    assert info.value.current is src
    assert info.value.target is dst


@pytest.mark.parametrize("dst", [I.CONFIRMED, I.EDITED])
def test_locked_items_reopen_only_via_exam_unlock(dst: ItemState) -> None:
    with pytest.raises(IllegalTransition, match="exam unlock"):
        transition(I.LOCKED, dst)
    with pytest.raises(IllegalTransition):
        transition(I.LOCKED, dst, via_exam_unlock=False)
    assert transition(I.LOCKED, dst, via_exam_unlock=True) is dst


def test_exam_guards_are_enforced() -> None:
    with pytest.raises(IllegalTransition, match="validation"):
        transition(E.DRAFT, E.RUBRIC_LOCKED)
    with pytest.raises(IllegalTransition, match="scripts"):
        transition(E.RUBRIC_LOCKED, E.DRAFT, scripts_captured=3)
    with pytest.raises(IllegalTransition, match="rolling"):
        transition(E.CAPTURING, E.REVIEWING)
    with pytest.raises(IllegalTransition, match="decided"):
        transition(E.REVIEWING, E.MODERATION, all_items_decided=False)
    with pytest.raises(IllegalTransition, match="moderation"):
        transition(E.MODERATION, E.MARKS_LOCKED, completeness_ok=True)
    with pytest.raises(IllegalTransition, match="reason"):
        transition(E.MARKS_LOCKED, E.REVIEWING, otp_verified=True, reason="  ")
    with pytest.raises(IllegalTransition, match="OTP"):
        transition(E.MARKS_LOCKED, E.PUBLISHED)
    with pytest.raises(IllegalTransition, match="OTP"):
        transition(E.RECHECK, E.PUBLISHED, otp_verified=False)
    assert transition(E.CAPTURING, E.PROCESSING) is E.PROCESSING
    assert transition(E.RUBRIC_LOCKED, E.DRAFT, scripts_captured=0) is E.DRAFT


def test_unknown_context_keys_are_rejected() -> None:
    with pytest.raises(TypeError, match="unknown transition context"):
        transition(I.PENDING, I.PROCESSING, via_exam_unlok=True)


def test_mixed_enum_types_are_rejected() -> None:
    with pytest.raises(TypeError):
        transition(I.PENDING, E.DRAFT)  # type: ignore[call-overload]


def test_self_transitions_are_illegal() -> None:
    for state in ItemState:
        assert not is_legal(state, state)
    for exam_state in ExamState:
        assert not is_legal(exam_state, exam_state)


def test_allowed_targets_and_teacher_decided() -> None:
    assert allowed_targets(I.PENDING) == frozenset({I.UNMAPPED, I.PROCESSING, I.MANUAL_READY})
    assert TEACHER_DECIDED == frozenset({I.CONFIRMED, I.EDITED})
    assert allowed_targets(E.PUBLISHED) == frozenset({E.RECHECK})


@settings(max_examples=300)
@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=60))
def test_random_item_walks_only_take_legal_edges(choices: list[int]) -> None:
    state = I.PENDING
    history = [state]
    for pick in choices:
        targets = sorted(allowed_targets(state))
        if not targets:
            break
        nxt = targets[pick % len(targets)]
        state = transition(state, nxt, **PERMISSIVE_CTX)
        history.append(state)
    for before, after in zip(history, history[1:], strict=False):
        assert (before, after) in EXPECTED_ITEM_EDGES
    # Locked is only ever entered from a decided (or re-check) state.
    for before, after in zip(history, history[1:], strict=False):
        if after is I.LOCKED:
            assert before in {I.CONFIRMED, I.EDITED, I.MODERATED, I.RECHECK}


@settings(max_examples=300)
@given(st.lists(st.sampled_from(list(ItemState)), min_size=1, max_size=40))
def test_random_attempts_never_leave_the_graph(targets: list[ItemState]) -> None:
    state = I.PENDING
    for target in targets:
        before = state
        try:
            state = transition(state, target)
        except IllegalTransition:
            assert state is before
            continue
        assert (before, state) in EXPECTED_ITEM_EDGES
        # Without the unlock flag a locked item can never be reopened.
        assert not (before is I.LOCKED and state in TEACHER_DECIDED)


def test_locked_reachable_only_through_teacher_decided_states() -> None:
    # Every predecessor of LOCKED is decided, moderated (from decided) or recheck (from locked).
    predecessors = {src for src, dsts in ITEM_TRANSITIONS.items() if I.LOCKED in dsts}
    assert predecessors == {I.CONFIRMED, I.EDITED, I.MODERATED, I.RECHECK}
    moderated_preds = {src for src, dsts in ITEM_TRANSITIONS.items() if I.MODERATED in dsts}
    assert moderated_preds <= TEACHER_DECIDED
    recheck_preds = {src for src, dsts in ITEM_TRANSITIONS.items() if I.RECHECK in dsts}
    assert recheck_preds == {I.LOCKED}


@settings(max_examples=200)
@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=40))
def test_random_exam_walks_only_take_legal_edges(choices: list[int]) -> None:
    state = E.DRAFT
    for pick in choices:
        targets = sorted(allowed_targets(state))
        nxt = targets[pick % len(targets)]
        before = state
        state = transition(state, nxt, **PERMISSIVE_CTX)
        assert (before, state) in EXPECTED_EXAM_EDGES
