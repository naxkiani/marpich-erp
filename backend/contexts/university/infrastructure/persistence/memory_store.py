"""University in-memory repositories."""
from __future__ import annotations

from contexts.university.domain.aggregates.course import Course
from contexts.university.domain.aggregates.grade import Grade
from contexts.university.domain.aggregates.student import Student
from contexts.university.domain.ports.repositories import (
    ICourseRepository,
    IGradeRepository,
    IStudentRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class UniversityMemoryStore:
    students: dict[str, Student] = {}
    courses: dict[str, Course] = {}
    grades: dict[str, Grade] = {}

    @classmethod
    def reset(cls) -> None:
        cls.students.clear()
        cls.courses.clear()
        cls.grades.clear()


class InMemoryStudentRepository(IStudentRepository):
    async def save(self, student: Student) -> None:
        UniversityMemoryStore.students[str(student.id)] = student

    async def find_by_id(self, tenant_id: str, student_id: UniqueId) -> Student | None:
        s = UniversityMemoryStore.students.get(str(student_id))
        return s if s and s.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, student_number: str) -> Student | None:
        key = student_number.strip().upper()
        for s in UniversityMemoryStore.students.values():
            if s.tenant_id == tenant_id and s.student_number == key:
                return s
        return None

    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Student | None:
        for s in UniversityMemoryStore.students.values():
            if (
                s.tenant_id == tenant_id
                and s.lms_provider == lms_provider
                and s.lms_external_id == lms_external_id
            ):
                return s
        return None

    async def list_students(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Student]:
        rows = [s for s in UniversityMemoryStore.students.values() if s.tenant_id == tenant_id]
        return rows[offset : offset + limit]


class InMemoryCourseRepository(ICourseRepository):
    async def save(self, course: Course) -> None:
        UniversityMemoryStore.courses[str(course.id)] = course

    async def find_by_id(self, tenant_id: str, course_id: UniqueId) -> Course | None:
        c = UniversityMemoryStore.courses.get(str(course_id))
        return c if c and c.tenant_id == tenant_id else None

    async def find_by_code(self, tenant_id: str, course_code: str) -> Course | None:
        key = course_code.strip().upper()
        for c in UniversityMemoryStore.courses.values():
            if c.tenant_id == tenant_id and c.course_code == key:
                return c
        return None

    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Course | None:
        for c in UniversityMemoryStore.courses.values():
            if (
                c.tenant_id == tenant_id
                and c.lms_provider == lms_provider
                and c.lms_external_id == lms_external_id
            ):
                return c
        return None

    async def list_courses(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Course]:
        rows = [c for c in UniversityMemoryStore.courses.values() if c.tenant_id == tenant_id]
        return rows[offset : offset + limit]


class InMemoryGradeRepository(IGradeRepository):
    async def save(self, grade: Grade) -> None:
        UniversityMemoryStore.grades[str(grade.id)] = grade

    async def list_by_student(
        self, tenant_id: str, student_id: UniqueId, *, limit: int = 50, offset: int = 0
    ) -> list[Grade]:
        rows = [
            g
            for g in UniversityMemoryStore.grades.values()
            if g.tenant_id == tenant_id and str(g.student_id) == str(student_id)
        ]
        return rows[offset : offset + limit]
