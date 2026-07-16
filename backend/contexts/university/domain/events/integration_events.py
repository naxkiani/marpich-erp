"""University integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class StudentEnrolledIntegration(IntegrationEvent):
    student_id: UniqueId
    student_number: str
    program_code: str
    email: str

    @property
    def event_name(self) -> str:
        return "university.student.enrolled"

    @property
    def source_context(self) -> str:
        return "university"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "student_id": str(self.student_id),
            "student_number": self.student_number,
            "program_code": self.program_code,
            "email": self.email,
        }


@dataclass(frozen=True, kw_only=True)
class CourseOfferedIntegration(IntegrationEvent):
    course_id: UniqueId
    course_code: str
    term: str
    credits: int

    @property
    def event_name(self) -> str:
        return "university.course.offered"

    @property
    def source_context(self) -> str:
        return "university"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "course_id": str(self.course_id),
            "course_code": self.course_code,
            "term": self.term,
            "credits": self.credits,
        }


@dataclass(frozen=True, kw_only=True)
class GradePostedIntegration(IntegrationEvent):
    grade_id: UniqueId
    student_id: UniqueId
    course_id: UniqueId
    letter_grade: str

    @property
    def event_name(self) -> str:
        return "university.grade.posted"

    @property
    def source_context(self) -> str:
        return "university"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "grade_id": str(self.grade_id),
            "student_id": str(self.student_id),
            "course_id": str(self.course_id),
            "letter_grade": self.letter_grade,
        }
