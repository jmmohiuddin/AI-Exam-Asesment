"""Paper structure and the marks that come in against it (FR-RES-01, SD §10).

A paper is components (CQ, SA, MCQ, practical, other); a marked component is
questions; a question is sub-parts (ka/kha/ga/gha). Components that the platform
does not mark — practicals, other subjects, MCQ read from the cover sheet — carry
a single imported mark instead of questions.

The structure validates itself, so a mis-set paper is caught at setup rather than
at publication: a component's maximum must equal what its questions can actually
award, which with a choice rule means the ``answer`` highest-scoring questions.
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum

from pydantic import Field, model_validator

from khata.engines.base import FrozenModel, NonNegativeDecimal, Percent, PositiveDecimal
from khata.engines.errors import ResultInputError

ZERO = Decimal(0)
DEFAULT_PASS_PERCENT = Decimal(33)


class ComponentKind(StrEnum):
    CQ = "cq"
    SA = "sa"
    MCQ = "mcq"
    PRACTICAL = "practical"
    OTHER = "other"


class ChoicePolicy(StrEnum):
    """What to count when a student answers more questions than allowed."""

    FIRST_ATTEMPTED = "first_attempted"  # default (SD §10)
    BEST = "best"  # school setting


class SubPartSpec(FrozenModel):
    id: str = Field(min_length=1)
    max_marks: PositiveDecimal


class QuestionSpec(FrozenModel):
    id: str = Field(min_length=1)
    sub_parts: tuple[SubPartSpec, ...] = Field(min_length=1)

    @property
    def max_marks(self) -> Decimal:
        return sum((part.max_marks for part in self.sub_parts), ZERO)


class ChoiceRule(FrozenModel):
    answer: int = Field(gt=0)
    policy: ChoicePolicy = ChoicePolicy.FIRST_ATTEMPTED


class ComponentSpec(FrozenModel):
    code: str = Field(min_length=1)
    kind: ComponentKind
    max_marks: PositiveDecimal
    pass_percent: Percent = DEFAULT_PASS_PERCENT
    questions: tuple[QuestionSpec, ...] = ()
    choice: ChoiceRule | None = None

    @property
    def is_marked_in_platform(self) -> bool:
        return bool(self.questions)

    @property
    def pass_mark(self) -> Decimal:
        return self.max_marks * self.pass_percent / Decimal(100)

    @model_validator(mode="after")
    def _consistent(self) -> ComponentSpec:
        if not self.questions:
            if self.choice is not None:
                raise ResultInputError(
                    f"component {self.code!r} has a choice rule but no questions"
                )
            return self
        self._check_unique_ids()
        self._check_max_marks()
        return self

    def _check_unique_ids(self) -> None:
        question_ids = [q.id for q in self.questions]
        part_ids = [p.id for q in self.questions for p in q.sub_parts]
        for label, ids in (("question", question_ids), ("sub-part", part_ids)):
            duplicates = sorted({i for i in ids if ids.count(i) > 1})
            if duplicates:
                raise ResultInputError(
                    f"component {self.code!r} has duplicate {label} ids: {', '.join(duplicates)}"
                )

    def _check_max_marks(self) -> None:
        maxima = sorted((q.max_marks for q in self.questions), reverse=True)
        if self.choice is None:
            awardable = sum(maxima, ZERO)
            detail = "its questions"
        else:
            if self.choice.answer > len(self.questions):
                raise ResultInputError(
                    f"component {self.code!r} asks for {self.choice.answer} answers "
                    f"but has only {len(self.questions)} questions"
                )
            awardable = sum(maxima[: self.choice.answer], ZERO)
            detail = f"its best {self.choice.answer} questions"
        if awardable != self.max_marks:
            raise ResultInputError(
                f"component {self.code!r} declares max {self.max_marks} but {detail} "
                f"award {awardable}"
            )


class PaperStructure(FrozenModel):
    """One subject's paper: the components a student is marked on."""

    subject_id: str = Field(min_length=1)
    components: tuple[ComponentSpec, ...] = Field(min_length=1)

    @property
    def max_marks(self) -> Decimal:
        return sum((c.max_marks for c in self.components), ZERO)

    @model_validator(mode="after")
    def _unique_component_codes(self) -> PaperStructure:
        codes = [c.code for c in self.components]
        duplicates = sorted({c for c in codes if codes.count(c) > 1})
        if duplicates:
            raise ResultInputError(f"duplicate component codes: {', '.join(duplicates)}")
        return self


class SubPartMark(FrozenModel):
    """One sub-part's confirmed mark. ``attempted`` drives the choice rule."""

    sub_part_id: str = Field(min_length=1)
    marks: NonNegativeDecimal = ZERO
    attempted: bool = True

    @model_validator(mode="after")
    def _blank_scores_nothing(self) -> SubPartMark:
        if not self.attempted and self.marks != ZERO:
            raise ResultInputError(
                f"sub-part {self.sub_part_id!r} is not attempted but carries {self.marks}"
            )
        return self


class ComponentMarks(FrozenModel):
    """Marks for one component: sub-parts when marked here, a single mark when imported."""

    component_code: str = Field(min_length=1)
    sub_parts: tuple[SubPartMark, ...] = ()
    marks: NonNegativeDecimal | None = None
    absent: bool = False

    @model_validator(mode="after")
    def _absent_carries_no_marks(self) -> ComponentMarks:
        if self.absent and (self.marks is not None or self.sub_parts):
            raise ResultInputError(f"component {self.component_code!r} is absent but carries marks")
        return self
