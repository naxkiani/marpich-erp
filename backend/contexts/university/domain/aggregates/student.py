"""Student aggregate — CAP-EDU-001 enrollment lifecycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Student(AggregateRoot):
    tenant_id: str
    student_number: str
    first_name: str
    last_name: str
    email: str
    program_code: str
    status: str = "enrolled"
    identity_user_id: str | None = None
    document_id: str | None = None
    lms_external_id: str | None = None
    lms_provider: str | None = None
    delivery_model: str = "degree"
    cohort_ref: str | None = None
    enrolled_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enroll(
        cls,
        *,
        tenant_id: str,
        student_number: str,
        first_name: str,
        last_name: str,
        email: str,
        program_code: str,
        identity_user_id: str | None = None,
        document_id: str | None = None,
        lms_external_id: str | None = None,
        lms_provider: str | None = None,
        delivery_model: str = "degree",
        cohort_ref: str | None = None,
    ) -> Student:
        model = (delivery_model or "degree").strip().lower()
        if model not in {"degree", "bootcamp", "certificate"}:
            raise ValueError("university.errors.invalid_delivery_model")
        cohort = (cohort_ref or "").strip().upper() or None
        if model == "bootcamp" and not cohort:
            raise ValueError("university.errors.bootcamp_cohort_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            student_number=student_number.strip().upper(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip().lower(),
            program_code=program_code.strip().upper(),
            identity_user_id=identity_user_id,
            document_id=document_id,
            lms_external_id=lms_external_id,
            lms_provider=lms_provider,
            delivery_model=model,
            cohort_ref=cohort,
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "student_number": self.student_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "program_code": self.program_code,
            "status": self.status,
            "identity_user_id": self.identity_user_id,
            "document_id": self.document_id,
            "lms_external_id": self.lms_external_id,
            "lms_provider": self.lms_provider,
            "delivery_model": self.delivery_model,
            "cohort_ref": self.cohort_ref,
            "enrolled_at": self.enrolled_at.isoformat(),
        }
