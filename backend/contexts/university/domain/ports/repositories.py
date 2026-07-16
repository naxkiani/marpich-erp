"""University repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.university.domain.aggregates.course import Course
from contexts.university.domain.aggregates.grade import Grade
from contexts.university.domain.aggregates.student import Student
from shared.domain.value_objects.unique_id import UniqueId


class IStudentRepository(ABC):
    @abstractmethod
    async def save(self, student: Student) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, student_id: UniqueId) -> Student | None: ...

    @abstractmethod
    async def find_by_number(self, tenant_id: str, student_number: str) -> Student | None: ...

    @abstractmethod
    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Student | None: ...

    @abstractmethod
    async def list_students(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Student]: ...


class ICourseRepository(ABC):
    @abstractmethod
    async def save(self, course: Course) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, course_id: UniqueId) -> Course | None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, course_code: str) -> Course | None: ...

    @abstractmethod
    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Course | None: ...

    @abstractmethod
    async def list_courses(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Course]: ...


class IGradeRepository(ABC):
    @abstractmethod
    async def save(self, grade: Grade) -> None: ...

    @abstractmethod
    async def list_by_student(
        self, tenant_id: str, student_id: UniqueId, *, limit: int = 50, offset: int = 0
    ) -> list[Grade]: ...
