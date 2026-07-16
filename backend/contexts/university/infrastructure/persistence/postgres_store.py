"""PostgreSQL repositories — University bounded context (CAP-EDU-001)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.university.domain.aggregates.course import Course
from contexts.university.domain.aggregates.grade import Grade
from contexts.university.domain.aggregates.student import Student
from contexts.university.domain.ports.repositories import (
    ICourseRepository,
    IGradeRepository,
    IStudentRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    UniversityCourseRow,
    UniversityGradeRow,
    UniversityStudentRow,
)


class PostgresStudentRepository(IStudentRepository):
    async def save(self, student: Student) -> None:
        async with session_scope() as session:
            row = await session.get(UniversityStudentRow, UUID(str(student.id)))
            if row is None:
                session.add(
                    UniversityStudentRow(
                        id=UUID(str(student.id)),
                        tenant_id=student.tenant_id,
                        student_number=student.student_number,
                        first_name=student.first_name,
                        last_name=student.last_name,
                        email=student.email,
                        program_code=student.program_code,
                        status=student.status,
                        identity_user_id=student.identity_user_id,
                        document_id=student.document_id,
                        lms_external_id=student.lms_external_id,
                        lms_provider=student.lms_provider,
                        delivery_model=student.delivery_model,
                        cohort_ref=student.cohort_ref,
                        enrolled_at=student.enrolled_at,
                    )
                )
            else:
                row.first_name = student.first_name
                row.last_name = student.last_name
                row.email = student.email
                row.program_code = student.program_code
                row.status = student.status
                row.identity_user_id = student.identity_user_id
                row.document_id = student.document_id
                row.lms_external_id = student.lms_external_id
                row.lms_provider = student.lms_provider
                row.delivery_model = student.delivery_model
                row.cohort_ref = student.cohort_ref

    async def find_by_id(self, tenant_id: str, student_id: UniqueId) -> Student | None:
        async with session_scope() as session:
            row = await session.get(UniversityStudentRow, UUID(str(student_id)))
            return _student_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, student_number: str) -> Student | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(UniversityStudentRow).where(
                    UniversityStudentRow.tenant_id == tenant_id,
                    UniversityStudentRow.student_number == student_number.strip().upper(),
                )
            )
            return _student_from_row(row) if row else None

    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Student | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(UniversityStudentRow).where(
                    UniversityStudentRow.tenant_id == tenant_id,
                    UniversityStudentRow.lms_provider == lms_provider,
                    UniversityStudentRow.lms_external_id == lms_external_id,
                )
            )
            return _student_from_row(row) if row else None

    async def list_students(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Student]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(UniversityStudentRow)
                    .where(UniversityStudentRow.tenant_id == tenant_id)
                    .order_by(UniversityStudentRow.enrolled_at.desc())
                    .offset(offset)
                    .limit(limit)
                )
            ).all()
        return [_student_from_row(r) for r in rows]


class PostgresCourseRepository(ICourseRepository):
    async def save(self, course: Course) -> None:
        async with session_scope() as session:
            row = await session.get(UniversityCourseRow, UUID(str(course.id)))
            if row is None:
                session.add(
                    UniversityCourseRow(
                        id=UUID(str(course.id)),
                        tenant_id=course.tenant_id,
                        course_code=course.course_code,
                        title=course.title,
                        credits=course.credits,
                        term=course.term,
                        status=course.status,
                        lms_external_id=course.lms_external_id,
                        lms_provider=course.lms_provider,
                        created_at=course.created_at,
                    )
                )
            else:
                row.title = course.title
                row.credits = course.credits
                row.term = course.term
                row.status = course.status
                row.lms_external_id = course.lms_external_id
                row.lms_provider = course.lms_provider

    async def find_by_id(self, tenant_id: str, course_id: UniqueId) -> Course | None:
        async with session_scope() as session:
            row = await session.get(UniversityCourseRow, UUID(str(course_id)))
            return _course_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_code(self, tenant_id: str, course_code: str) -> Course | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(UniversityCourseRow).where(
                    UniversityCourseRow.tenant_id == tenant_id,
                    UniversityCourseRow.course_code == course_code.strip().upper(),
                )
            )
            return _course_from_row(row) if row else None

    async def find_by_lms_id(
        self, tenant_id: str, *, lms_provider: str, lms_external_id: str
    ) -> Course | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(UniversityCourseRow).where(
                    UniversityCourseRow.tenant_id == tenant_id,
                    UniversityCourseRow.lms_provider == lms_provider,
                    UniversityCourseRow.lms_external_id == lms_external_id,
                )
            )
            return _course_from_row(row) if row else None

    async def list_courses(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[Course]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(UniversityCourseRow)
                    .where(UniversityCourseRow.tenant_id == tenant_id)
                    .order_by(UniversityCourseRow.course_code)
                    .offset(offset)
                    .limit(limit)
                )
            ).all()
        return [_course_from_row(r) for r in rows]


class PostgresGradeRepository(IGradeRepository):
    async def save(self, grade: Grade) -> None:
        async with session_scope() as session:
            row = await session.get(UniversityGradeRow, UUID(str(grade.id)))
            if row is None:
                session.add(
                    UniversityGradeRow(
                        id=UUID(str(grade.id)),
                        tenant_id=grade.tenant_id,
                        student_id=UUID(str(grade.student_id)),
                        course_id=UUID(str(grade.course_id)),
                        letter_grade=grade.letter_grade,
                        posted_by=grade.posted_by,
                        posted_at=grade.posted_at,
                    )
                )
            else:
                row.letter_grade = grade.letter_grade
                row.posted_by = grade.posted_by

    async def list_by_student(
        self, tenant_id: str, student_id: UniqueId, *, limit: int = 50, offset: int = 0
    ) -> list[Grade]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(UniversityGradeRow)
                    .where(
                        UniversityGradeRow.tenant_id == tenant_id,
                        UniversityGradeRow.student_id == UUID(str(student_id)),
                    )
                    .order_by(UniversityGradeRow.posted_at.desc())
                    .offset(offset)
                    .limit(limit)
                )
            ).all()
        return [_grade_from_row(r) for r in rows]


def _student_from_row(row: UniversityStudentRow) -> Student:
    return Student(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        student_number=row.student_number,
        first_name=row.first_name,
        last_name=row.last_name,
        email=row.email,
        program_code=row.program_code,
        status=row.status,
        identity_user_id=row.identity_user_id,
        document_id=row.document_id,
        lms_external_id=row.lms_external_id,
        lms_provider=row.lms_provider,
        delivery_model=row.delivery_model or "degree",
        cohort_ref=row.cohort_ref,
        enrolled_at=row.enrolled_at,
    )


def _course_from_row(row: UniversityCourseRow) -> Course:
    return Course(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        course_code=row.course_code,
        title=row.title,
        credits=row.credits,
        term=row.term,
        status=row.status,
        lms_external_id=row.lms_external_id,
        lms_provider=row.lms_provider,
        created_at=row.created_at,
    )


def _grade_from_row(row: UniversityGradeRow) -> Grade:
    return Grade(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        student_id=UniqueId.from_string(str(row.student_id)),
        course_id=UniqueId.from_string(str(row.course_id)),
        letter_grade=row.letter_grade,
        posted_by=row.posted_by,
        posted_at=row.posted_at,
    )
