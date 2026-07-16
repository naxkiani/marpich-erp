"""Course aggregate — academic offering."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Course(AggregateRoot):
    tenant_id: str
    course_code: str
    title: str
    credits: int
    term: str
    status: str = "active"
    lms_external_id: str | None = None
    lms_provider: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def offer(
        cls,
        *,
        tenant_id: str,
        course_code: str,
        title: str,
        credits: int,
        term: str,
        lms_external_id: str | None = None,
        lms_provider: str | None = None,
    ) -> Course:
        if credits < 1 or credits > 12:
            raise ValueError("university.errors.invalid_credits")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            course_code=course_code.strip().upper(),
            title=title.strip(),
            credits=credits,
            term=term.strip().upper(),
            lms_external_id=lms_external_id,
            lms_provider=lms_provider,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "course_code": self.course_code,
            "title": self.title,
            "credits": self.credits,
            "term": self.term,
            "status": self.status,
            "lms_external_id": self.lms_external_id,
            "lms_provider": self.lms_provider,
            "created_at": self.created_at.isoformat(),
        }
