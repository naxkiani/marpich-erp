"""P5.2 — University/Inventory Postgres wiring + row mappers (no live DB required)."""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest

from contexts.inventory.container import get_inventory_service, reset_inventory_service
from contexts.inventory.infrastructure.persistence.memory_store import InMemoryStockLevelRepository
from contexts.inventory.infrastructure.persistence.postgres_store import (
    PostgresStockLevelRepository,
    _stock_from_row,
)
from contexts.university.container import get_university_service, reset_university_service
from contexts.university.infrastructure.persistence.memory_store import (
    InMemoryCourseRepository,
    InMemoryGradeRepository,
    InMemoryStudentRepository,
)
from contexts.university.infrastructure.persistence.postgres_store import (
    PostgresCourseRepository,
    PostgresGradeRepository,
    PostgresStudentRepository,
    _course_from_row,
    _grade_from_row,
    _student_from_row,
)


@pytest.fixture(autouse=True)
def _reset_containers():
    reset_university_service()
    reset_inventory_service()
    yield
    reset_university_service()
    reset_inventory_service()


def test_university_container_defaults_to_memory():
    svc = get_university_service()
    assert isinstance(svc._students, InMemoryStudentRepository)
    assert isinstance(svc._courses, InMemoryCourseRepository)
    assert isinstance(svc._grades, InMemoryGradeRepository)


def test_university_container_wires_postgres(monkeypatch):
    monkeypatch.setattr(
        "contexts.university.container.use_postgres",
        lambda: True,
    )
    reset_university_service()
    svc = get_university_service()
    assert isinstance(svc._students, PostgresStudentRepository)
    assert isinstance(svc._courses, PostgresCourseRepository)
    assert isinstance(svc._grades, PostgresGradeRepository)


def test_inventory_container_defaults_to_memory():
    svc = get_inventory_service()
    assert isinstance(svc._stock, InMemoryStockLevelRepository)


def test_inventory_container_wires_postgres(monkeypatch):
    monkeypatch.setattr(
        "contexts.inventory.container.use_postgres",
        lambda: True,
    )
    reset_inventory_service()
    svc = get_inventory_service()
    assert isinstance(svc._stock, PostgresStockLevelRepository)


def test_university_student_row_mapper():
    sid = uuid4()
    row = SimpleNamespace(
        id=sid,
        tenant_id="uni-a",
        student_number="S001",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@uni.dev",
        program_code="CS",
        status="enrolled",
        identity_user_id=None,
        document_id="doc-1",
        lms_external_id="m-1",
        lms_provider="moodle",
        delivery_model="bootcamp",
        cohort_ref="COH-2026",
        enrolled_at=datetime.now(UTC),
    )
    student = _student_from_row(row)  # type: ignore[arg-type]
    assert str(student.id) == str(sid)
    assert student.tenant_id == "uni-a"
    assert student.delivery_model == "bootcamp"
    assert student.cohort_ref == "COH-2026"
    assert student.document_id == "doc-1"


def test_university_course_and_grade_row_mappers():
    cid = uuid4()
    sid = uuid4()
    gid = uuid4()
    course = _course_from_row(
        SimpleNamespace(  # type: ignore[arg-type]
            id=cid,
            tenant_id="uni-a",
            course_code="CS101",
            title="Intro",
            credits=3,
            term="FALL26",
            status="active",
            lms_external_id=None,
            lms_provider=None,
            created_at=datetime.now(UTC),
        )
    )
    assert course.course_code == "CS101"
    assert course.credits == 3

    grade = _grade_from_row(
        SimpleNamespace(  # type: ignore[arg-type]
            id=gid,
            tenant_id="uni-a",
            student_id=sid,
            course_id=cid,
            letter_grade="A",
            posted_by="prof@uni.dev",
            posted_at=datetime.now(UTC),
        )
    )
    assert grade.letter_grade == "A"
    assert str(grade.student_id) == str(sid)


def test_inventory_stock_row_mapper():
    rid = uuid4()
    stock = _stock_from_row(
        SimpleNamespace(  # type: ignore[arg-type]
            id=rid,
            tenant_id="retail-a",
            sku="SKU-1",
            quantity_on_hand="12.5000",
            updated_at=datetime.now(UTC),
        )
    )
    assert stock.sku == "SKU-1"
    assert stock.quantity_on_hand == Decimal("12.5000")
    assert stock.tenant_id == "retail-a"
