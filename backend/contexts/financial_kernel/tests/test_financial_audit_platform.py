"""Enterprise financial audit platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_audit_service,
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.financial_kernel.domain.services.financial_audit_engine import (
    assert_deletion_forbidden,
    build_immutable_audit_report,
    build_lifecycle_history,
    compute_audit_tamper_hash,
    verify_audit_chain,
)
from contexts.financial_kernel.infrastructure.persistence.financial_audit_memory_store import (
    InMemoryFinancialAuditRepository,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_kernel_service()
    get_financial_audit_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "audit@kernel.dev", "password": "SecurePass123!", "display_name": "Audit Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "audit@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision_hospital(slug: str) -> dict[str, str]:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    return {
        "ar": (await svc.resolve_account_code(slug, "patient_receivables")).unwrap(),
        "rev": (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap(),
        "cash": (await svc.resolve_account_code(slug, "cash")).unwrap(),
    }


def test_deletion_forbidden():
    with pytest.raises(PermissionError):
        assert_deletion_forbidden()


def test_tamper_hash_chain():
    h1 = compute_audit_tamper_hash(
        action="created", actor_id="u1", resource_id="j1", payload_checksum="abc"
    )
    h2 = compute_audit_tamper_hash(
        action="posted",
        actor_id="u2",
        resource_id="j1",
        payload_checksum="def",
        previous_hash=h1,
    )
    assert h1 != h2


def test_lifecycle_history_tracks_actors():
    entries = [
        {
            "action": "created",
            "actor_id": "creator",
            "occurred_at": "2025-01-01T10:00:00Z",
            "tenant_id": "t1",
            "organization_id": "org-1",
        },
        {
            "action": "approved",
            "actor_id": "approver",
            "occurred_at": "2025-01-01T11:00:00Z",
            "tenant_id": "t1",
            "organization_id": "org-1",
        },
        {
            "action": "posted",
            "actor_id": "poster",
            "occurred_at": "2025-01-01T12:00:00Z",
            "tenant_id": "t1",
            "organization_id": "org-1",
        },
    ]
    lifecycle = build_lifecycle_history(entries)
    assert lifecycle["who_created"] == "creator"
    assert lifecycle["who_approved"] == "approver"
    assert lifecycle["who_posted"] == "poster"
    assert lifecycle["tenant"] == "t1"
    assert lifecycle["organization"] == "org-1"


@pytest.mark.asyncio
async def test_audit_catalog(client):
    slug = "audit-cat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/financial-kernel/audit/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"][0]
    assert data["immutable"] is True
    assert data["deletion_allowed"] is False
    assert "who_created" in data["tracked_fields"]


@pytest.mark.asyncio
async def test_journal_post_creates_audit_trail(client):
    slug = "audit-post"
    ctx = await _provision_hospital(slug)
    headers = await _auth_headers(client, slug)

    post = await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "audit-j-001",
            "lines": [
                {"account_code": ctx["ar"], "debit": 100, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 100},
            ],
        },
    )
    assert post.status_code == 201
    journal_id = post.json()["data"]["id"]

    history = await client.get(
        "/api/v1/financial-kernel/audit/history",
        headers=headers,
        params={"resource_type": "journal", "resource_id": journal_id},
    )
    assert history.status_code == 200
    report = history.json()["data"]
    assert report["immutable"] is True
    assert report["deletion_allowed"] is False
    assert report["chain_valid"] is True
    assert report["tracked"]["who_posted"] is not None
    assert len(report["entries"]) >= 1


@pytest.mark.asyncio
async def test_delete_audit_entry_forbidden(client):
    slug = "audit-del"
    headers = await _auth_headers(client, slug)
    svc = get_financial_audit_service()
    recorded = (
        await svc.record(
            tenant_id=slug,
            resource_type="journal",
            resource_id="j-del",
            action="created",
            actor_id="system",
        )
    ).unwrap()

    resp = await client.delete(
        f"/api/v1/financial-kernel/audit/entries/{recorded['id']}",
        headers=headers,
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_verify_audit_chain(client):
    slug = "audit-chain"
    headers = await _auth_headers(client, slug)
    ctx = await _provision_hospital(slug)

    await client.post(
        "/api/v1/financial-kernel/journals",
        headers=headers,
        json={
            "source_context": "manual",
            "source_document_id": "audit-chain-1",
            "lines": [
                {"account_code": ctx["ar"], "debit": 50, "credit": 0},
                {"account_code": ctx["rev"], "debit": 0, "credit": 50},
            ],
        },
    )

    verify = await client.get(
        "/api/v1/financial-kernel/audit/verify-chain",
        headers=headers,
    )
    assert verify.status_code == 200
    assert verify.json()["data"]["valid"] is True


@pytest.mark.asyncio
async def test_repository_delete_raises():
    InMemoryFinancialAuditRepository.reset()
    repo = InMemoryFinancialAuditRepository()
    with pytest.raises(PermissionError):
        await repo.delete("any-id")
