"""University FastAPI router — CAP-EDU-001."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.university.container import get_university_service
from contexts.university.presentation.schemas import (
    EnrollStudentRequest,
    OfferCourseRequest,
    PostGradeRequest,
)

router = APIRouter(prefix="/university", tags=["University"])


@router.post("/students", status_code=status.HTTP_201_CREATED)
async def enroll_student(
    body: EnrollStudentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("university.students.write"))],
):
    result = await get_university_service().enroll_student(
        tenant_id=tenant_id,
        student_number=body.student_number,
        first_name=body.first_name,
        last_name=body.last_name,
        email=str(body.email),
        program_code=body.program_code,
        correlation_id=correlation_id,
        identity_user_id=body.identity_user_id,
        document_id=body.document_id,
        delivery_model=body.delivery_model,
        cohort_ref=body.cohort_ref,
        actor_user_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/students")
async def list_students(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("university.students.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_university_service().list_students(
        tenant_id, limit=limit, offset=offset
    )
    return {"data": result.unwrap()}


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def offer_course(
    body: OfferCourseRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("university.courses.write"))],
):
    result = await get_university_service().offer_course(
        tenant_id=tenant_id,
        course_code=body.course_code,
        title=body.title,
        credits=body.credits,
        term=body.term,
        correlation_id=correlation_id,
        actor_user_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/courses")
async def list_courses(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("university.courses.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_university_service().list_courses(
        tenant_id, limit=limit, offset=offset
    )
    return {"data": result.unwrap()}


@router.post("/grades", status_code=status.HTTP_201_CREATED)
async def post_grade(
    body: PostGradeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("university.grades.write"))],
):
    result = await get_university_service().post_grade(
        tenant_id=tenant_id,
        student_id=body.student_id,
        course_id=body.course_id,
        letter_grade=body.letter_grade,
        correlation_id=correlation_id,
        posted_by=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/students/{student_id}/grades")
async def list_student_grades(
    student_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("university.grades.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_university_service().list_grades_for_student(
        tenant_id, student_id, limit=limit, offset=offset
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
