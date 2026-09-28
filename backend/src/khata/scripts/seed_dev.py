"""Seed a development database with one worked exam.

Creates an organisation, a school, a teacher, one exam with a locked rubric, two
candidates with captured answers, and runs the Fake marking provider so the review
screen has something real to show.

Refuses to run outside dev/test: it writes a known password.

    uv run python -m khata.scripts.seed_dev
"""

from __future__ import annotations

import sys
import uuid
from decimal import Decimal

from sqlalchemy import select

from khata.core.config import Environment, Settings, get_settings
from khata.core.db import Database
from khata.core.roles import Role
from khata.engines.rubric import Rubric
from khata.modules.aigateway.fake import FakeMarkingProvider
from khata.modules.assessment import service
from khata.modules.assessment.models import Script
from khata.modules.identity.models import AppUser
from khata.modules.identity.service import create_user
from khata.modules.org.models import Organization, RoleAssignment, School

TEACHER_MOBILE = "+8801712345678"
ORG_NAME = "Shaheed Suhrawardy Model School"

MODEL_ANSWER = (
    "Photosynthesis is the process in which a plant uses chlorophyll to capture "
    "sunlight and converts carbon dioxide and water into glucose and oxygen."
)

RUBRIC = Rubric.model_validate(
    {
        "item_id": "q1",
        "version": 1,
        "model_answer": MODEL_ANSWER,
        "half_marks_allowed": False,
        "criteria": [
            {
                "id": "c1",
                "text_en": "Identifies chlorophyll as the pigment",
                "text_bn": "ক্লোরোফিলকে রঞ্জক হিসেবে চিহ্নিত করেছে",
                "marks": "2",
                "type": "concept",
                "evidence_expectation": "chlorophyll",
            },
            {
                "id": "c2",
                "text_en": "Identifies sunlight as the energy source",
                "text_bn": "সূর্যালোককে শক্তির উৎস হিসেবে চিহ্নিত করেছে",
                "marks": "2",
                "type": "concept",
                "evidence_expectation": "sunlight",
            },
            {
                "id": "c3",
                "text_en": "Names glucose as a product",
                "text_bn": "গ্লুকোজকে উৎপাদ হিসেবে উল্লেখ করেছে",
                "marks": "1",
                "type": "final_answer",
                "evidence_expectation": "glucose",
            },
        ],
    }
)

ANSWERS = (
    (
        "101",
        "Karim Rahman",
        "Plants use chlorophyll in their leaves to absorb sunlight. They turn "
        "carbon dioxide and water into glucose and release oxygen.",
    ),
    (
        "102",
        "Fatema Akter",
        "The plant makes food in the leaf. It needs light from the sun.",
    ),
)


def seed(database: Database, settings: Settings) -> dict[str, str]:
    password = settings.seed_dev_password
    tenant_id = uuid.uuid4()

    with database.session_scope(tenant_id) as session:
        existing = session.scalar(select(AppUser).where(AppUser.mobile == TEACHER_MOBILE))
        if existing is not None:
            raise SystemExit(f"{TEACHER_MOBILE} already exists — the database is already seeded.")

        session.add(Organization(id=tenant_id, name=ORG_NAME))
        session.flush()
        school = School(
            tenant_id=tenant_id,
            name_bn="শহীদ সোহরাওয়ার্দী মডেল স্কুল",
            name_en=ORG_NAME,
            board="dhaka",
        )
        session.add(school)
        teacher = create_user(session, mobile=TEACHER_MOBILE, name="Rahim Uddin", password=password)
        session.add(
            RoleAssignment(
                tenant_id=tenant_id,
                user_id=teacher.id,
                school_id=school.id,
                role=Role.EXAM_COORDINATOR.value,
            )
        )
        session.flush()

        exam = service.create_exam(
            session,
            tenant_id=tenant_id,
            school_id=school.id,
            name="Biology — First Term",
            subject_code="BIO",
            class_level=9,
            created_by=teacher.id,
        )
        item = service.add_item(
            session,
            exam=exam,
            item_no=1,
            max_marks=Decimal(5),
            prompt_en="What is photosynthesis?",
            prompt_bn="সালোকসংশ্লেষণ কাকে বলে?",
        )
        service.set_rubric(session, exam=exam, item=item, rubric=RUBRIC, created_by=teacher.id)
        service.lock_rubrics(session, exam)

        # Capture every script first, then evaluate. Evaluating moves the exam on to
        # reviewing, which closes capture — the same order a real exam follows.
        script_ids: list[uuid.UUID] = []
        for roll, name, answer in ANSWERS:
            candidate = service.add_candidate(session, exam=exam, roll=roll, name=name)
            result = service.submit_answer(
                session, exam=exam, candidate=candidate, item=item, answer_text=answer
            )
            script_ids.append(result.script_id)

        provider = FakeMarkingProvider()
        for script_id in script_ids:
            script = session.get(Script, script_id)
            assert script is not None
            service.evaluate_script(session, provider, script)

        return {
            "tenant_id": str(tenant_id),
            "mobile": TEACHER_MOBILE,
            "password": password,
            "exam_id": str(exam.id),
        }


def main() -> int:
    settings = get_settings()
    if settings.env not in (Environment.DEV, Environment.TEST):
        print(f"Refusing to seed in env={settings.env}.", file=sys.stderr)
        return 1

    database = Database.from_settings(settings)
    try:
        created = seed(database, settings)
    finally:
        database.dispose()

    print("Seeded a development exam.")
    for key, value in created.items():
        print(f"  {key:<10} {value}")
    print("\nSign in at http://localhost:5173/login")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
