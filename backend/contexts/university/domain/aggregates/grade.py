"""Grade aggregate — posted academic result."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

_LETTER_GRADES = frozenset({"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F", "P", "NP", "I", "W"})


@dataclass(eq=False, kw_only=True)
class Grade(AggregateRoot):
    tenant_id: str
    student_id: UniqueId
    course_id: UniqueId
    letter_grade: str
    posted_by: str | None = None
    posted_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def post(
        cls,
        *,
        tenant_id: str,
        student_id: UniqueId,
        course_id: UniqueId,
        letter_grade: str,
        posted_by: str | None = None,
    ) -> Grade:
        normalized = letter_grade.strip().upper()
        if normalized not in _LETTER_GRADES:
            raise ValueError("university.errors.invalid_letter_grade")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            student_id=student_id,
            course_id=course_id,
            letter_grade=normalized,
            posted_by=posted_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "student_id": str(self.student_id),
            "course_id": str(self.course_id),
            "letter_grade": self.letter_grade,
            "posted_by": self.posted_by,
            "posted_at": self.posted_at.isoformat(),
        }
