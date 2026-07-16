"""P2 — Moodle/Classroom LMS sync via ECF → university ACL."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.enterprise_connector_framework.container import (
    get_enterprise_connector_framework_service,
    reset_enterprise_connector_framework_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.university.container import get_university_service, reset_university_service
from contexts.university.infrastructure.persistence.memory_store import UniversityMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.connectors.builtins import register_builtin_connectors
from shared.connectors.registry import reset_connector_registry
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    UniversityMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_connector_registry()
    register_builtin_connectors()
    reset_platform_service()
    reset_university_service()
    reset_enterprise_connector_framework_service()
    get_university_service()
    get_enterprise_connector_framework_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "lms@uni.dev", "password": "SecurePass123!", "display_name": "LMS Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "lms@uni.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_moodle_courses_and_enrollments_sync_into_university(client):
    slug = "uni-lms-p2"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "LMS Uni", "slug": slug, "industry_pack": "university"},
    )
    headers = await _admin(client, slug)

    registered = await client.post(
        "/api/v1/enterprise-connector-framework/connectors",
        json={
            "connector_type": "moodle",
            "display_name": "Campus Moodle",
            "config": {
                "base_url": "https://moodle.example.edu",
                "environment": "sandbox",
            },
        },
        headers=headers,
    )
    assert registered.status_code == 200, registered.text
    instance_ref = registered.json()["data"]["instance_ref"]

    courses_exec = await client.post(
        f"/api/v1/enterprise-connector-framework/connectors/{instance_ref}/execute",
        json={"operation": "courses_sync", "payload": {}},
        headers=headers,
    )
    assert courses_exec.status_code == 200, courses_exec.text

    enroll_exec = await client.post(
        f"/api/v1/enterprise-connector-framework/connectors/{instance_ref}/execute",
        json={"operation": "enrollments_sync", "payload": {}},
        headers=headers,
    )
    assert enroll_exec.status_code == 200, enroll_exec.text

    grades_exec = await client.post(
        f"/api/v1/enterprise-connector-framework/connectors/{instance_ref}/execute",
        json={"operation": "grades_push", "payload": {}},
        headers=headers,
    )
    assert grades_exec.status_code == 200, grades_exec.text

    courses = await client.get("/api/v1/university/courses", headers=headers)
    assert courses.status_code == 200
    assert len(courses.json()["data"]) >= 2
    assert any(c.get("lms_provider") == "moodle" for c in courses.json()["data"])

    students = await client.get("/api/v1/university/students", headers=headers)
    assert students.status_code == 200
    assert len(students.json()["data"]) >= 1
    student_id = students.json()["data"][0]["id"]

    grades = await client.get(f"/api/v1/university/students/{student_id}/grades", headers=headers)
    assert grades.status_code == 200
    assert len(grades.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_google_classroom_roster_sync(client):
    slug = "uni-gc-p2"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Classroom Uni", "slug": slug, "industry_pack": "university"},
    )
    headers = await _admin(client, slug)
    registered = await client.post(
        "/api/v1/enterprise-connector-framework/connectors",
        json={
            "connector_type": "google_classroom",
            "display_name": "Classroom",
            "config": {"environment": "sandbox", "customer_id": "demo"},
        },
        headers=headers,
    )
    assert registered.status_code == 200, registered.text
    ref = registered.json()["data"]["instance_ref"]
    await client.post(
        f"/api/v1/enterprise-connector-framework/connectors/{ref}/execute",
        json={"operation": "courses_sync", "payload": {}},
        headers=headers,
    )
    await client.post(
        f"/api/v1/enterprise-connector-framework/connectors/{ref}/execute",
        json={"operation": "rosters_sync", "payload": {}},
        headers=headers,
    )
    students = await client.get("/api/v1/university/students", headers=headers)
    assert students.status_code == 200
    assert any(s.get("lms_provider") == "google_classroom" for s in students.json()["data"])
