"""Role vocabulary shared by org (storage), authz (policy) and identity (tokens)."""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    """Tenant roles held through ``role_assignment`` (08 §5.3)."""

    ORG_OWNER = "org_owner"
    SCHOOL_ADMIN = "school_admin"
    EXAM_COORDINATOR = "exam_coordinator"
    HOD = "hod"
    TEACHER = "teacher"
    CAPTURE_OPERATOR = "capture_operator"
    PRINCIPAL = "principal"


class PlatformRole(StrEnum):
    """Platform staff roles (audit C6). Grant access to /internal only; no tenant data."""

    PLATFORM_ADMIN = "platform_admin"
    PLATFORM_AIQ = "platform_aiq"
    PLATFORM_ASSESSMENT = "platform_assessment"
    PLATFORM_SUPPORT = "platform_support"


SUBJECT_SCOPED_ROLES = frozenset({Role.HOD, Role.TEACHER})
ORG_LEVEL_ROLES = frozenset({Role.ORG_OWNER})
