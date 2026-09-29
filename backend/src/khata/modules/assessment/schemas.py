"""Request and response shapes for the assessment endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from khata.engines.rubric import Rubric
from khata.engines.scoring import CriterionDecision, TotalOverride


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- authoring


class ExamCreate(StrictModel):
    school_id: uuid.UUID
    name: str = Field(min_length=1, max_length=200)
    subject_code: str = Field(min_length=1, max_length=32)
    class_level: int = Field(ge=6, le=12)


class ExamOut(BaseModel):
    id: uuid.UUID
    name: str
    subject_code: str
    class_level: int
    state: str
    total_marks: Decimal
    rubric_locked_at: datetime | None
    marks_locked_at: datetime | None


class ItemCreate(StrictModel):
    item_no: int = Field(ge=1)
    max_marks: Decimal = Field(gt=0, allow_inf_nan=False)
    prompt_bn: str = Field(default="", max_length=5000)
    prompt_en: str = Field(default="", max_length=5000)


class ItemOut(BaseModel):
    id: uuid.UUID
    item_no: int
    prompt_bn: str
    prompt_en: str
    max_marks: Decimal


class RubricPut(StrictModel):
    rubric: Rubric


class RubricOut(BaseModel):
    id: uuid.UUID
    item_id: uuid.UUID
    version: int
    ai_eligible: bool
    locked_at: datetime | None
    payload: dict[str, Any]


# --------------------------------------------------------------------------- capture


class CandidateCreate(StrictModel):
    roll: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=200)
    #: Links the candidate to the roll. Without it no consent decision applies and
    #: the script is marked at L0 (FR-ORG-06).
    student_id: uuid.UUID | None = None


class CandidateOut(BaseModel):
    id: uuid.UUID
    roll: str
    name: str
    student_id: uuid.UUID | None = None


class AnswerSubmit(StrictModel):
    candidate_id: uuid.UUID
    item_id: uuid.UUID
    answer_text: str = Field(max_length=20_000)


class ItemResultOut(BaseModel):
    id: uuid.UUID
    script_id: uuid.UUID
    item_id: uuid.UUID
    state: str
    total: Decimal | None
    ai_confidence: Decimal | None
    decided_at: datetime | None


class ScriptOut(BaseModel):
    id: uuid.UUID
    exam_id: uuid.UUID
    candidate_id: uuid.UUID
    total_marks: Decimal | None


# --------------------------------------------------------------------------- review


class ReviewCard(BaseModel):
    """Everything the teacher needs to decide one item, on one screen (spec 05 §23).

    Deliberately one payload: the reviewer should never have to navigate away to
    see the rubric, the model answer or why the AI proposed what it did.
    """

    result_id: uuid.UUID
    item_id: uuid.UUID
    item_no: int
    prompt_bn: str
    prompt_en: str
    max_marks: Decimal
    state: str

    student_answer: str
    model_answer: str | None
    rubric: dict[str, Any]
    rubric_version: int | None

    ai_model: str | None
    ai_confidence: Decimal | None
    ai_low_confidence: bool
    ai_rationale: str | None
    ai_evidence: list[str]
    ai_decisions: list[dict[str, Any]]
    suggested_score: dict[str, Any] | None

    teacher_score: dict[str, Any] | None
    total: Decimal | None
    decided_at: datetime | None


class ReviewQueue(BaseModel):
    script_id: uuid.UUID
    candidate: CandidateOut
    exam_state: str
    script_total: Decimal | None
    items: list[ReviewCard]


class ReviewDecision(StrictModel):
    """A teacher's decision for one item.

    ``accepted_ai`` records whether the teacher took the suggestion unchanged; it
    drives the confirmed/edited distinction and the override-rate metric (spec 06).
    """

    decisions: list[CriterionDecision]
    deductions_applied: list[str] = Field(default_factory=list)
    total_override: TotalOverride | None = None
    accepted_ai: bool = False


class CandidateResultOut(BaseModel):
    """One student's line on the ledger (FR-RES-01/02/03)."""

    candidate_id: uuid.UUID
    roll: str
    name: str
    script_id: uuid.UUID | None
    marks: Decimal
    max_marks: Decimal
    percent: Decimal
    letter: str
    grade_point: Decimal
    is_pass: bool
    #: Items captured or expected but not yet decided. Non-zero means the marks
    #: above are incomplete, not that the student scored nothing for them.
    pending_items: int


class ExamResultsOut(BaseModel):
    exam_id: uuid.UUID
    name: str
    subject_code: str
    state: str
    max_marks: Decimal
    #: True until marks are locked. A provisional total will still change.
    provisional: bool
    candidates: list[CandidateResultOut]
