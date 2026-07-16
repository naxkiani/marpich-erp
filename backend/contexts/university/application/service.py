"""University application service — CAP-EDU-001 student lifecycle."""
from __future__ import annotations

from contexts.university.domain.aggregates.course import Course
from contexts.university.domain.aggregates.grade import Grade
from contexts.university.domain.aggregates.student import Student
from contexts.university.domain.events.integration_events import (
    CourseOfferedIntegration,
    GradePostedIntegration,
    StudentEnrolledIntegration,
)
from contexts.university.domain.ports.repositories import (
    ICourseRepository,
    IGradeRepository,
    IStudentRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class UniversityApplicationService:
    def __init__(
        self,
        students: IStudentRepository,
        courses: ICourseRepository,
        grades: IGradeRepository,
    ) -> None:
        self._students = students
        self._courses = courses
        self._grades = grades

    async def enroll_student(
        self,
        *,
        tenant_id: str,
        student_number: str,
        first_name: str,
        last_name: str,
        email: str,
        program_code: str,
        correlation_id: str,
        identity_user_id: str | None = None,
        document_id: str | None = None,
        actor_user_id: str | None = None,
        lms_external_id: str | None = None,
        lms_provider: str | None = None,
        delivery_model: str = "degree",
        cohort_ref: str | None = None,
    ) -> Result[dict]:
        if await self._students.find_by_number(tenant_id, student_number):
            return Result.fail("university.errors.student_number_exists")
        if lms_external_id and lms_provider:
            by_lms = await self._students.find_by_lms_id(
                tenant_id, lms_provider=lms_provider, lms_external_id=lms_external_id
            )
            if by_lms:
                return Result.fail("university.errors.student_lms_id_exists")

        try:
            student = Student.enroll(
                tenant_id=tenant_id,
                student_number=student_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                program_code=program_code,
                identity_user_id=identity_user_id,
                document_id=document_id,
                lms_external_id=lms_external_id,
                lms_provider=lms_provider,
                delivery_model=delivery_model,
                cohort_ref=cohort_ref,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._students.save(student)
        await publish_integration_event(
            StudentEnrolledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_user_id,
                student_id=student.id,
                student_number=student.student_number,
                program_code=student.program_code,
                email=student.email,
            )
        )
        return Result.ok(student.to_dict())

    async def list_students(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[list[dict]]:
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        rows = await self._students.list_students(tenant_id, limit=limit, offset=offset)
        return Result.ok([s.to_dict() for s in rows])

    async def offer_course(
        self,
        *,
        tenant_id: str,
        course_code: str,
        title: str,
        credits: int,
        term: str,
        correlation_id: str,
        actor_user_id: str | None = None,
        lms_external_id: str | None = None,
        lms_provider: str | None = None,
    ) -> Result[dict]:
        if await self._courses.find_by_code(tenant_id, course_code):
            return Result.fail("university.errors.course_code_exists")
        if lms_external_id and lms_provider:
            by_lms = await self._courses.find_by_lms_id(
                tenant_id, lms_provider=lms_provider, lms_external_id=lms_external_id
            )
            if by_lms:
                return Result.fail("university.errors.course_lms_id_exists")
        try:
            course = Course.offer(
                tenant_id=tenant_id,
                course_code=course_code,
                title=title,
                credits=credits,
                term=term,
                lms_external_id=lms_external_id,
                lms_provider=lms_provider,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._courses.save(course)
        await publish_integration_event(
            CourseOfferedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_user_id,
                course_id=course.id,
                course_code=course.course_code,
                term=course.term,
                credits=course.credits,
            )
        )
        return Result.ok(course.to_dict())

    async def list_courses(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[list[dict]]:
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        rows = await self._courses.list_courses(tenant_id, limit=limit, offset=offset)
        return Result.ok([c.to_dict() for c in rows])

    async def post_grade(
        self,
        *,
        tenant_id: str,
        student_id: str,
        course_id: str,
        letter_grade: str,
        correlation_id: str,
        posted_by: str | None = None,
    ) -> Result[dict]:
        sid = UniqueId.from_string(student_id)
        cid = UniqueId.from_string(course_id)
        if not await self._students.find_by_id(tenant_id, sid):
            return Result.fail("university.errors.student_not_found")
        if not await self._courses.find_by_id(tenant_id, cid):
            return Result.fail("university.errors.course_not_found")
        try:
            grade = Grade.post(
                tenant_id=tenant_id,
                student_id=sid,
                course_id=cid,
                letter_grade=letter_grade,
                posted_by=posted_by,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._grades.save(grade)
        await publish_integration_event(
            GradePostedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=posted_by,
                grade_id=grade.id,
                student_id=sid,
                course_id=cid,
                letter_grade=grade.letter_grade,
            )
        )
        return Result.ok(grade.to_dict())

    async def list_grades_for_student(
        self, tenant_id: str, student_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[list[dict]]:
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        sid = UniqueId.from_string(student_id)
        if not await self._students.find_by_id(tenant_id, sid):
            return Result.fail("university.errors.student_not_found")
        rows = await self._grades.list_by_student(tenant_id, sid, limit=limit, offset=offset)
        return Result.ok([g.to_dict() for g in rows])

    async def apply_lms_batch(
        self,
        *,
        tenant_id: str,
        provider: str,
        correlation_id: str,
        courses: list[dict] | None = None,
        enrollments: list[dict] | None = None,
        grades: list[dict] | None = None,
    ) -> Result[dict]:
        """Idempotent ACL entry — map LMS sync payload into local aggregates."""
        applied = {"courses": 0, "enrollments": 0, "grades": 0}
        course_by_lms: dict[str, dict] = {}

        for row in courses or []:
            lms_id = str(row.get("lms_course_id") or "")
            existing = None
            if lms_id:
                existing = await self._courses.find_by_lms_id(
                    tenant_id, lms_provider=provider, lms_external_id=lms_id
                )
            if not existing:
                existing = await self._courses.find_by_code(
                    tenant_id, str(row.get("course_code") or lms_id or "COURSE")
                )
            if existing:
                applied["courses"] += 1
                if lms_id:
                    course_by_lms[lms_id] = existing.to_dict()
                continue
            result = await self.offer_course(
                tenant_id=tenant_id,
                course_code=str(row.get("course_code") or lms_id or "COURSE"),
                title=str(row.get("title") or "LMS Course"),
                credits=int(row.get("credits") or 3),
                term=str(row.get("term") or "TERM"),
                correlation_id=correlation_id,
                lms_external_id=lms_id or None,
                lms_provider=provider,
            )
            if result.succeeded:
                applied["courses"] += 1
                if lms_id:
                    course_by_lms[lms_id] = result.unwrap()

        student_by_number: dict[str, dict] = {}
        for row in enrollments or []:
            number = str(row.get("student_number") or row.get("lms_user_id") or "")
            lms_user = str(row.get("lms_user_id") or "")
            existing_s = None
            if lms_user:
                existing_s = await self._students.find_by_lms_id(
                    tenant_id, lms_provider=provider, lms_external_id=lms_user
                )
            if not existing_s and number:
                existing_s = await self._students.find_by_number(tenant_id, number)
            if existing_s:
                applied["enrollments"] += 1
                student_by_number[existing_s.student_number] = existing_s.to_dict()
                continue
            result = await self.enroll_student(
                tenant_id=tenant_id,
                student_number=number or "S0000",
                first_name=str(row.get("first_name") or "LMS"),
                last_name=str(row.get("last_name") or "Student"),
                email=str(row.get("email") or f"{number or 'student'}@lms.local"),
                program_code=str(row.get("program_code") or "GEN"),
                correlation_id=correlation_id,
                lms_external_id=lms_user or None,
                lms_provider=provider,
            )
            if result.succeeded:
                applied["enrollments"] += 1
                student_by_number[result.unwrap()["student_number"]] = result.unwrap()

        for row in grades or []:
            student_number = str(row.get("student_number") or "").upper()
            lms_course_id = str(row.get("lms_course_id") or "")
            course_code = str(row.get("course_code") or "").upper()
            student = student_by_number.get(student_number)
            if not student and student_number:
                found = await self._students.find_by_number(tenant_id, student_number)
                student = found.to_dict() if found else None
            course = course_by_lms.get(lms_course_id)
            if not course and course_code:
                found_c = await self._courses.find_by_code(tenant_id, course_code)
                course = found_c.to_dict() if found_c else None
            if not course and lms_course_id:
                found_c = await self._courses.find_by_lms_id(
                    tenant_id, lms_provider=provider, lms_external_id=lms_course_id
                )
                course = found_c.to_dict() if found_c else None
            if not student or not course:
                continue
            grade_result = await self.post_grade(
                tenant_id=tenant_id,
                student_id=student["id"],
                course_id=course["id"],
                letter_grade=str(row.get("letter_grade") or "P"),
                correlation_id=correlation_id,
                posted_by=f"lms:{provider}",
            )
            if grade_result.succeeded:
                applied["grades"] += 1

        return Result.ok({"provider": provider, "applied": applied})
