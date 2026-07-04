"""Workflow — approvals and task inbox tests."""
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
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from contexts.workflow.infrastructure.persistence.memory_store import WorkflowMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


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
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    get_workflow_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_audit_service()
    get_documents_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    registered = await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@wf.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    user_id = registered.json()["data"]["id"]
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@wf.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {token}",
        "user_id": user_id,
    }


@pytest.mark.asyncio
async def test_deploy_definition_and_list(client):
    slug = "wf-deploy"
    headers = await _auth_headers(client, slug)
    headers.pop("user_id")

    deployed = await client.post(
        "/api/v1/workflow/definitions",
        json={
            "key": "purchase_approval",
            "name": "Purchase Approval",
            "steps": [
                {"key": "manager", "name": "Manager Review"},
                {"key": "finance", "name": "Finance Approval"},
            ],
        },
        headers=headers,
    )
    assert deployed.status_code == 201

    listed = await client.get("/api/v1/workflow/definitions", headers=headers)
    assert listed.status_code == 200
    keys = [d["key"] for d in listed.json()["data"]]
    assert "purchase_approval" in keys


@pytest.mark.asyncio
async def test_start_and_complete_approval_flow(client):
    slug = "wf-flow"
    headers = await _auth_headers(client, slug)
    user_id = headers.pop("user_id")

    await client.post(
        "/api/v1/workflow/definitions",
        json={
            "key": "expense",
            "name": "Expense",
            "steps": [{"key": "review", "name": "Review expense"}],
        },
        headers=headers,
    )

    started = await client.post(
        "/api/v1/workflow/instances",
        json={
            "definition_key": "expense",
            "context": {"amount": 500, "currency": "USD"},
            "assignees": {"review": user_id},
        },
        headers=headers,
    )
    assert started.status_code == 201
    task_id = started.json()["data"]["task"]["id"]
    instance_id = started.json()["data"]["instance"]["id"]

    inbox = await client.get("/api/v1/workflow/tasks", headers=headers)
    assert inbox.status_code == 200
    assert any(t["id"] == task_id for t in inbox.json()["data"])

    completed = await client.post(
        f"/api/v1/workflow/tasks/{task_id}/complete",
        json={"outcome": "approved", "comment": "Looks good"},
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["data"]["instance"]["status"] == "completed"

    instance = await client.get(f"/api/v1/workflow/instances/{instance_id}", headers=headers)
    assert instance.status_code == 200
    assert instance.json()["data"]["instance"]["status"] == "completed"


@pytest.mark.asyncio
async def test_module_activation_deploys_default_approval(client):
    slug = "wf-module"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "WF Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    activate = await client.post(
        f"/api/v1/platform/tenants/{slug}/modules",
        json={"module_id": "healthcare.pharmacy"},
        headers=headers,
    )
    assert activate.status_code == 200

    listed = await client.get("/api/v1/workflow/definitions", headers=headers)
    keys = [d["key"] for d in listed.json()["data"]]
    assert "module.healthcare.pharmacy.approval" in keys


@pytest.mark.asyncio
async def test_task_assigned_creates_notification(client):
    slug = "wf-notify"
    headers = await _auth_headers(client, slug)
    user_id = headers.pop("user_id")

    await client.post(
        "/api/v1/workflow/definitions",
        json={
            "key": "leave",
            "name": "Leave Request",
            "steps": [{"key": "hr", "name": "HR approval"}],
        },
        headers=headers,
    )
    await client.post(
        "/api/v1/workflow/instances",
        json={"definition_key": "leave", "assignees": {"hr": user_id}},
        headers=headers,
    )

    inbox = await client.get("/api/v1/notifications/inbox", headers=headers)
    categories = [m["category"] for m in inbox.json()["data"]]
    assert "workflow" in categories


@pytest.mark.asyncio
async def test_reject_stops_process(client):
    slug = "wf-reject"
    headers = await _auth_headers(client, slug)
    user_id = headers.pop("user_id")

    await client.post(
        "/api/v1/workflow/definitions",
        json={
            "key": "contract",
            "name": "Contract",
            "steps": [{"key": "legal", "name": "Legal review"}],
        },
        headers=headers,
    )
    started = await client.post(
        "/api/v1/workflow/instances",
        json={"definition_key": "contract", "assignees": {"legal": user_id}},
        headers=headers,
    )
    task_id = started.json()["data"]["task"]["id"]

    rejected = await client.post(
        f"/api/v1/workflow/tasks/{task_id}/complete",
        json={"outcome": "rejected", "comment": "Terms unacceptable"},
        headers=headers,
    )
    assert rejected.status_code == 200
    assert rejected.json()["data"]["instance"]["status"] == "rejected"
