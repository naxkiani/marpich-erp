"""Contract tests — runtime published events during API flows."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.analytics.container import get_analytics_service, reset_analytics_service
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.documents.container import get_documents_service, reset_documents_service
from contexts.integration.container import get_integration_service, reset_integration_service
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.workflow.container import get_workflow_service, reset_workflow_service
from core.presentation.api.main import app
from shared.contracts.event_validator import validate_envelope, validate_event
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    PlatformMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_audit_service()
    reset_documents_service()
    reset_workflow_service()
    reset_integration_service()
    reset_analytics_service()
    get_organization_service()
    get_settings_service()
    get_audit_service()
    get_documents_service()
    get_workflow_service()
    get_integration_service()
    get_analytics_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_tenant_provision_publishes_contract_valid_events(client):
    captured: list[dict] = []

    async def capture(envelope: dict) -> None:
        captured.append(envelope)

    InProcessEventBus.subscribe("platform.tenant.provisioned", capture)
    InProcessEventBus.subscribe("organization.org.created", capture)

    response = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Contract Hospital", "slug": "contract-hospital", "industry_pack": "hospital"},
    )
    assert response.status_code == 201

    assert captured, "Expected integration events during tenant provision"
    for envelope in captured:
        validate_envelope(envelope)
        if envelope["event_name"] in {"platform.tenant.provisioned", "organization.org.created"}:
            validate_event(envelope)
