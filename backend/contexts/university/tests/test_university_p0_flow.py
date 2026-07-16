"""P0 — University CAP-EDU-001 + tenant/RBAC smoke."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.documents.infrastructure.persistence.memory_store import DocumentsMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from contexts.university.container import reset_university_service
from contexts.university.infrastructure.persistence.memory_store import UniversityMemoryStore
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from contexts.workflow.infrastructure.persistence.memory_store import WorkflowMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    OrganizationMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    AuditMemoryStore.reset()
    DocumentsMemoryStore.reset()
    WorkflowMemoryStore.reset()
    UniversityMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_university_service()
    get_documents_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_workflow_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _register_login(
    client: AsyncClient, tenant: str, email: str, display_name: str = "User"
) -> dict[str, str]:
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": display_name},
        headers={"X-Tenant-ID": tenant},
    )
    assert reg.status_code in (200, 201), reg.text
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_gateway_requires_tenant_on_business_routes(client):
    missing = await client.get("/api/v1/university/students")
    assert missing.status_code == 400
    assert "X-Tenant-ID" in missing.json()["detail"]

    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Uni A", "slug": "uni-gateway", "industry_pack": "university"},
    )
    assert provision.status_code == 201


@pytest.mark.asyncio
async def test_p0_smoke_login_docs_workflow_audit_enroll(client):
    slug = "uni-smoke-p0"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Smoke University", "slug": slug, "industry_pack": "university"},
    )
    assert provision.status_code == 201

    headers = await _register_login(client, slug, "admin@uni-smoke.dev", "Admin")

    root = await client.get("/api/v1/documents/folders/root", headers=headers)
    assert root.status_code == 200
    assert root.json()["data"]["is_root"] is True

    defs = await client.get("/api/v1/workflow/definitions", headers=headers)
    assert defs.status_code == 200

    audit = await client.get("/api/v1/audit/entries", headers=headers)
    assert audit.status_code == 200

    student = await client.post(
        "/api/v1/university/students",
        json={
            "student_number": "S1001",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@uni-smoke.dev",
            "program_code": "CS",
        },
        headers=headers,
    )
    assert student.status_code == 201, student.text
    assert student.json()["data"]["student_number"] == "S1001"

    listed = await client.get("/api/v1/university/students", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 1


@pytest.mark.asyncio
async def test_staff_vs_student_rbac_personas(client):
    slug = "uni-rbac-p0"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "RBAC University", "slug": slug, "industry_pack": "university"},
    )
    admin = await _register_login(client, slug, "admin@uni-rbac.dev", "Admin")

    seed = await client.post("/api/v1/identity/personas/education/seed", headers=admin)
    assert seed.status_code == 200, seed.text

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "staff@uni-rbac.dev",
            "password": "SecurePass123!",
            "display_name": "Staff",
        },
        headers={"X-Tenant-ID": slug},
    )
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@uni-rbac.dev",
            "password": "SecurePass123!",
            "display_name": "Student",
        },
        headers={"X-Tenant-ID": slug},
    )

    staff_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "staff@uni-rbac.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": slug},
    )
    student_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "student@uni-rbac.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": slug},
    )
    assert staff_login.status_code == 200
    assert student_login.status_code == 200

    from contexts.identity.container import get_identity_service

    svc = get_identity_service()
    staff_user = await svc._users.find_by_email(slug, "staff@uni-rbac.dev")
    student_user = await svc._users.find_by_email(slug, "student@uni-rbac.dev")
    assert staff_user and student_user
    staff_id = str(staff_user.id)
    student_id = str(student_user.id)

    assign_staff = await client.post(
        f"/api/v1/identity/users/{staff_id}/roles",
        json={"role_codes": ["staff"]},
        headers=admin,
    )
    assign_student = await client.post(
        f"/api/v1/identity/users/{student_id}/roles",
        json={"role_codes": ["student"]},
        headers=admin,
    )
    assert assign_staff.status_code == 200, assign_staff.text
    assert assign_student.status_code == 200, assign_student.text

    staff_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "staff@uni-rbac.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": slug},
    )
    student_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "student@uni-rbac.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": slug},
    )
    staff_h = {
        "X-Tenant-ID": slug,
        "Authorization": f"Bearer {staff_login.json()['data']['access_token']}",
    }
    student_h = {
        "X-Tenant-ID": slug,
        "Authorization": f"Bearer {student_login.json()['data']['access_token']}",
    }

    course = await client.post(
        "/api/v1/university/courses",
        json={
            "course_code": "CS101",
            "title": "Intro Computing",
            "credits": 3,
            "term": "FALL26",
        },
        headers=staff_h,
    )
    assert course.status_code == 201, course.text
    course_id = course.json()["data"]["id"]

    enrolled = await client.post(
        "/api/v1/university/students",
        json={
            "student_number": "S2001",
            "first_name": "Grace",
            "last_name": "Hopper",
            "email": "grace@uni-rbac.dev",
            "program_code": "CS",
        },
        headers=staff_h,
    )
    assert enrolled.status_code == 201, enrolled.text
    sid = enrolled.json()["data"]["id"]

    denied = await client.post(
        "/api/v1/university/grades",
        json={"student_id": sid, "course_id": course_id, "letter_grade": "A"},
        headers=student_h,
    )
    assert denied.status_code == 403

    posted = await client.post(
        "/api/v1/university/grades",
        json={"student_id": sid, "course_id": course_id, "letter_grade": "A"},
        headers=staff_h,
    )
    assert posted.status_code == 201, posted.text

    readable = await client.get(
        f"/api/v1/university/students/{sid}/grades",
        headers=student_h,
    )
    assert readable.status_code == 200
    assert readable.json()["data"][0]["letter_grade"] == "A"
