"""Enterprise Financial Workflow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_workflow_service, reset_financial_kernel_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_workflow_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wf@kernel.dev", "password": "SecurePass123!", "display_name": "WF Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "wf@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_all_workflow_types(client):
    slug = "wf-types"
    headers = await _auth_headers(client, slug)
    types_resp = await client.get("/api/v1/financial-kernel/workflows/types", headers=headers)
    assert types_resp.status_code == 200
    types = {t["type"] for t in types_resp.json()["data"]}
    assert types == {
        "approval",
        "payment",
        "purchase",
        "expense",
        "transfer",
        "budget",
        "invoice",
        "payroll",
        "tax",
        "treasury",
    }

    for wf_type in types:
        resp = await client.post(
            "/api/v1/financial-kernel/workflows",
            headers=headers,
            json={
                "workflow_type": wf_type,
                "source_context": "finance",
                "source_document_id": f"doc-{wf_type}",
                "assignee_id": "approver-1",
                "amount": 1000,
            },
        )
        assert resp.status_code == 201, wf_type
        data = resp.json()["data"]
        assert data["workflow_type"] == wf_type
        assert data["ai_recommendation"]["recommendation"] in ("approve", "review", "escalate")
        assert data["sla_hours"] > 0
        assert len(data["history"]) >= 1


@pytest.mark.asyncio
async def test_approval_sign_complete_flow(client):
    slug = "wf-approve"
    headers = await _auth_headers(client, slug)

    start = await client.post(
        "/api/v1/financial-kernel/workflows",
        headers=headers,
        json={
            "workflow_type": "payment",
            "source_context": "treasury",
            "source_document_id": "pay-100",
            "assignee_id": "cfo",
            "amount": 25000,
        },
    )
    wf_id = start.json()["data"]["id"]

    approve = await client.post(
        f"/api/v1/financial-kernel/workflows/{wf_id}/approve",
        headers=headers,
        json={"comment": "Approved for payment"},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"

    sign = await client.post(
        f"/api/v1/financial-kernel/workflows/{wf_id}/sign",
        headers=headers,
        json={},
    )
    assert sign.status_code == 200
    assert sign.json()["data"]["status"] == "signed"
    assert sign.json()["data"]["signature"]["algorithm"] == "RS256"

    complete = await client.post(
        f"/api/v1/financial-kernel/workflows/{wf_id}/complete",
        headers=headers,
    )
    assert complete.status_code == 200
    assert complete.json()["data"]["status"] == "completed"


@pytest.mark.asyncio
async def test_escalation_and_history(client):
    slug = "wf-escalate"
    headers = await _auth_headers(client, slug)

    start = await client.post(
        "/api/v1/financial-kernel/workflows",
        headers=headers,
        json={
            "workflow_type": "purchase",
            "source_context": "procurement",
            "source_document_id": "po-50",
            "assignee_id": "buyer",
            "amount": 15000,
        },
    )
    wf_id = start.json()["data"]["id"]

    escalate = await client.post(
        f"/api/v1/financial-kernel/workflows/{wf_id}/escalate",
        headers=headers,
        json={"escalated_to": "procurement_director"},
    )
    assert escalate.status_code == 200
    assert escalate.json()["data"]["status"] == "escalated"
    assert escalate.json()["data"]["escalated_to"] == "procurement_director"

    history = await client.get(
        f"/api/v1/financial-kernel/workflows/{wf_id}/history",
        headers=headers,
    )
    assert history.status_code == 200
    actions = [h["action"] for h in history.json()["data"]]
    assert "started" in actions
    assert "escalated" in actions


@pytest.mark.asyncio
async def test_ai_recommendation_and_reject(client):
    slug = "wf-ai"
    headers = await _auth_headers(client, slug)

    start = await client.post(
        "/api/v1/financial-kernel/workflows",
        headers=headers,
        json={
            "workflow_type": "expense",
            "source_context": "hr",
            "source_document_id": "exp-1",
            "assignee_id": "manager",
            "amount": 500,
        },
    )
    wf_id = start.json()["data"]["id"]

    ai = await client.get(
        f"/api/v1/financial-kernel/workflows/{wf_id}/ai-recommendation",
        headers=headers,
    )
    assert ai.status_code == 200
    assert "recommendation" in ai.json()["data"]
    assert "confidence" in ai.json()["data"]

    reject = await client.post(
        f"/api/v1/financial-kernel/workflows/{wf_id}/reject",
        headers=headers,
        json={"comment": "Missing receipts"},
    )
    assert reject.status_code == 200
    assert reject.json()["data"]["status"] == "rejected"


@pytest.mark.asyncio
async def test_sla_auto_escalate(client):
    slug = "wf-sla"
    headers = await _auth_headers(client, slug)
    svc = get_financial_workflow_service()

    from datetime import UTC, datetime, timedelta
    from contexts.financial_kernel.domain.aggregates.financial_workflow import FinancialWorkflow
    from contexts.financial_kernel.domain.services.financial_workflow_engine import compute_sla_deadline

    workflow = FinancialWorkflow.start(
        tenant_id=slug,
        workflow_type="transfer",
        source_context="treasury",
        source_document_id="xfer-1",
        idempotency_key="xfer-1:transfer",
        assignee_id="treasurer",
        sla_hours=1,
        sla_deadline=datetime.now(UTC) - timedelta(hours=1),
        started_by="system",
        amount=100000,
    )
    from contexts.financial_kernel.infrastructure.persistence.financial_workflow_memory_store import (
        InMemoryFinancialWorkflowRepository,
    )
    await InMemoryFinancialWorkflowRepository().save(workflow)

    result = await client.post(
        "/api/v1/financial-kernel/workflows/sla/auto-escalate",
        headers=headers,
    )
    assert result.status_code == 200
    escalated = result.json()["data"]
    assert len(escalated) >= 1
    assert escalated[0]["status"] == "escalated"
