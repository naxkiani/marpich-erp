"""Policy Engine — evaluation, lifecycle, and seeding tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.audit.container import get_audit_service, reset_audit_service
from contexts.audit.infrastructure.persistence.memory_store import AuditMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.policy.container import get_policy_evaluator, get_policy_service, reset_policy_service
from contexts.policy.domain.services.condition_matcher import match_conditions
from contexts.policy.domain.services.policy_evaluator import evaluate_version, run_test_cases
from contexts.policy.domain.aggregates.policy_version import PolicyVersion
from contexts.policy.infrastructure.persistence.memory_store import PolicyMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
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
    PolicyMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    reset_audit_service()
    reset_policy_service()
    get_audit_service()
    get_organization_service()
    get_settings_service()
    get_notification_service()
    get_policy_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@policy.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@policy.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def test_condition_matcher_operators():
    facts = {"customer": {"tier": "gold"}, "loan": {"amount": 500000}}
    matched, _ = match_conditions(
        [{"field": "customer.tier", "operator": "eq", "value": "gold"}], facts
    )
    assert matched
    matched, _ = match_conditions(
        [{"field": "loan.amount", "operator": "lte", "value": 600000}], facts
    )
    assert matched


def test_evaluator_applies_exception():
    from datetime import UTC, datetime

    version = PolicyVersion.create_draft(
        policy_id="p1",
        tenant_id="t1",
        version=1,
        effective_from=datetime.now(UTC),
        conditions=[{"field": "jurisdiction", "operator": "eq", "value": "IR"}],
        rules=[{"outcome": "apply_rate", "parameters": {"rate": 0.09}}],
        exceptions=[
            {
                "id": "medical",
                "conditions": [{"field": "product.category", "operator": "eq", "value": "medical"}],
                "rules": [{"outcome": "apply_rate", "parameters": {"rate": 0.0}}],
            }
        ],
        approval_required=False,
    )
    version.activate()
    result = evaluate_version(
        version,
        {"jurisdiction": "IR", "product": {"category": "medical"}},
        require_active=False,
    )
    assert result["matched"]
    assert result["outcome"] == "apply_rate"
    assert result["parameters"]["rate"] == 0.0
    assert result["applied_exception"] == "medical"


@pytest.mark.asyncio
async def test_hospital_tenant_seeds_admission_policy(client):
    slug = "policy-hospital"
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    headers = await _auth_headers(client, slug)

    policies = await client.get("/api/v1/policies", headers=headers)
    assert policies.status_code == 200
    items = policies.json()["data"]
    assert any(p["key"] == "admission.eligibility" for p in items)

    evaluate = await client.post(
        "/api/v1/policies/evaluate",
        headers=headers,
        json={
            "domain": "hospital",
            "policy_key": "admission.eligibility",
            "facts": {"encounter": {"type": "emergency"}, "patient": {"age": 10}},
        },
    )
    assert evaluate.status_code == 200
    data = evaluate.json()["data"]
    assert data["matched"] is True
    assert data["outcome"] == "allow_admission"
    assert "guardian_consent" in data["parameters"]["required_documents"]


@pytest.mark.asyncio
async def test_tax_policy_via_evaluator_port(client):
    slug = "policy-tax"
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "tax_consulting"}}
    )
    headers = await _auth_headers(client, slug)

    decision = await get_policy_evaluator().evaluate(
        tenant_id=slug,
        domain="tax",
        policy_key="vat.rate",
        facts={"jurisdiction": "IR", "product": {"category": "medical"}},
    )
    assert decision.matched
    assert decision.parameters["rate"] == 0.0


@pytest.mark.asyncio
async def test_create_version_submit_activate_and_rollback(client):
    slug = "policy-lifecycle"
    headers = await _auth_headers(client, slug)

    created = await client.post(
        "/api/v1/policies",
        headers=headers,
        json={
            "domain": "bank",
            "key": "lending.test_limit",
            "name": "Test Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_amount": 100000}}],
            "approval_required": True,
        },
    )
    assert created.status_code == 201
    policy_id = created.json()["data"]["id"]

    v2 = await client.post(
        f"/api/v1/policies/{policy_id}/versions",
        headers=headers,
        json={
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_amount": 200000}}],
            "approval_required": True,
            "change_reason": "Increase limit",
        },
    )
    assert v2.status_code == 201
    version = v2.json()["data"]["version"]

    submitted = await client.post(
        f"/api/v1/policies/{policy_id}/versions/{version}/submit-approval",
        headers=headers,
    )
    assert submitted.status_code == 200
    assert submitted.json()["data"]["status"] == "pending_approval"

    activated = await client.post(
        f"/api/v1/policies/{policy_id}/versions/{version}/activate",
        headers=headers,
    )
    assert activated.status_code == 200
    assert activated.json()["data"]["status"] == "active"

    evaluate = await client.post(
        "/api/v1/policies/evaluate",
        headers=headers,
        json={"domain": "bank", "policy_key": "lending.test_limit", "facts": {}},
    )
    assert evaluate.json()["data"]["parameters"]["max_amount"] == 200000

    rollback = await client.post(
        f"/api/v1/policies/{policy_id}/rollback",
        headers=headers,
        json={"target_version": 1, "reason": "Regulatory correction"},
    )
    assert rollback.status_code == 200
    assert rollback.json()["data"]["version"] == 1


@pytest.mark.asyncio
async def test_simulate_and_test_runner(client):
    slug = "policy-sim"
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    headers = await _auth_headers(client, slug)

    policies = await client.get("/api/v1/policies?domain=bank", headers=headers)
    policy_id = next(p["id"] for p in policies.json()["data"] if p["key"] == "lending.single_exposure_limit")

    sim = await client.post(
        "/api/v1/policies/simulate",
        headers=headers,
        json={
            "domain": "bank",
            "policy_key": "lending.single_exposure_limit",
            "facts": {"customer": {"tier": "gold"}, "loan": {"amount": 400000}},
            "candidate_versions": [1],
        },
    )
    assert sim.status_code == 200
    assert sim.json()["data"]["comparisons"][0]["matched"] is True

    tests = await client.post(
        f"/api/v1/policies/{policy_id}/test?version=1",
        headers=headers,
        json={
            "test_cases": [
                {
                    "name": "Gold tier",
                    "facts": {"customer": {"tier": "gold"}},
                    "expect": {"outcome": "within_limit", "parameters": {"max_amount": 750000}},
                }
            ]
        },
    )
    assert tests.status_code == 200
    assert tests.json()["data"]["passed"] is True


def test_run_test_cases_helper():
    from datetime import UTC, datetime

    version = PolicyVersion.create_draft(
        policy_id="p1",
        tenant_id="t1",
        version=1,
        effective_from=datetime.now(UTC),
        conditions=[],
        rules=[{"outcome": "ok", "parameters": {"x": 1}}],
    )
    results = run_test_cases(
        version,
        [{"name": "pass", "facts": {}, "expect": {"outcome": "ok", "parameters": {"x": 1}}}],
    )
    assert results[0]["passed"] is True
