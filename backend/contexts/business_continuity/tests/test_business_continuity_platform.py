"""Enterprise Business Continuity Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.business_continuity.container import get_business_continuity_service, reset_business_continuity_service
from contexts.business_continuity.domain.aggregates.continuity_platform import (
    ContinuityCapability,
    FailoverStatus,
    PlanType,
)
from contexts.business_continuity.domain.services import continuity_engine
from contexts.business_continuity.infrastructure.persistence.continuity_memory_store import (
    InMemoryBackupStrategyRepository,
    InMemoryContinuityPlanRepository,
    InMemoryContinuityTenantProfileRepository,
    InMemoryFailoverRecordRepository,
    InMemoryRecoveryTestRepository,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    InMemoryContinuityTenantProfileRepository.reset()
    InMemoryContinuityPlanRepository.reset()
    InMemoryBackupStrategyRepository.reset()
    InMemoryFailoverRecordRepository.reset()
    InMemoryRecoveryTestRepository.reset()
    InProcessEventBus.reset()
    reset_policy_service()
    reset_business_continuity_service()
    get_policy_service()
    get_business_continuity_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bcp@enterprise.dev", "password": "SecurePass123!", "display_name": "BCP"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "bcp@enterprise.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_catalog_lists_continuity_capabilities(client):
    headers = await _auth_headers(client, "bcpcat")
    resp = await client.get("/api/v1/business-continuity/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    caps = {c["capability"] for c in data["capabilities"]}
    assert ContinuityCapability.DISASTER_RECOVERY.value in caps
    assert ContinuityCapability.RECOVERY_POINT_OBJECTIVE.value in caps
    assert ContinuityCapability.RECOVERY_TIME_OBJECTIVE.value in caps
    assert ContinuityCapability.CONTINUITY_DASHBOARD.value in caps
    assert len(caps) == 11
    assert data["delegation"]["local_continuity_duplication"] is False


@pytest.mark.asyncio
async def test_seed_failover_test_and_dashboard(client):
    slug = "bcpseed"
    headers = await _auth_headers(client, slug)

    seed = await client.post("/api/v1/business-continuity/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["plans_seeded"] == 4
    assert body["backups_seeded"] == 3

    rpo_rto = await client.get("/api/v1/business-continuity/rpo-rto", headers=headers)
    assert rpo_rto.status_code == 200
    assert "rpo" in rpo_rto.json()["data"]
    assert "rto" in rpo_rto.json()["data"]

    ha = await client.get("/api/v1/business-continuity/high-availability", headers=headers)
    assert ha.status_code == 200
    assert ha.json()["data"]["availability_status"] == "healthy"

    replication = await client.get("/api/v1/business-continuity/replication", headers=headers)
    assert replication.status_code == 200
    assert replication.json()["data"]["strategies_count"] == 3

    failover = await client.post(
        "/api/v1/business-continuity/failover",
        headers=headers,
        json={
            "source_system": "primary-db",
            "target_system": "dr-db",
            "trigger_reason": "Primary site unreachable",
        },
    )
    assert failover.status_code == 201
    assert failover.json()["data"]["status"] == FailoverStatus.COMPLETED.value

    emergency = await client.post(
        "/api/v1/business-continuity/emergency-ops",
        headers=headers,
        json={},
    )
    assert emergency.status_code == 200
    assert emergency.json()["data"]["activated"] is True

    plans = await client.get("/api/v1/business-continuity/plans", headers=headers)
    plan_ref = plans.json()["data"][0]["plan_ref"]

    schedule = await client.post(
        "/api/v1/business-continuity/tests",
        headers=headers,
        json={"plan_ref": plan_ref, "test_type": "full"},
    )
    assert schedule.status_code == 201
    test_ref = schedule.json()["data"]["test_ref"]

    run = await client.post(
        f"/api/v1/business-continuity/tests/{test_ref}/run",
        headers=headers,
    )
    assert run.status_code == 200
    assert run.json()["data"]["status"] in ("passed", "failed")

    dash = await client.get("/api/v1/business-continuity/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert d["summary"]["capabilities"] == 11
    assert d["summary"]["active_plans"] == 4
    assert d["summary"]["backup_strategies"] == 3
    assert d["delegation"]["local_continuity_duplication"] is False


@pytest.mark.asyncio
async def test_create_plan_and_backup(client):
    slug = "bcpnew"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/business-continuity/seed", headers=headers)

    plan = await client.post(
        "/api/v1/business-continuity/plans",
        headers=headers,
        json={
            "title": "HR Systems DR Plan",
            "plan_type": PlanType.DR.value,
            "criticality_tier": "tier_2",
            "rpo_hours": 2,
            "rto_hours": 6,
            "recovery_steps": ["Restore HR database", "Validate payroll"],
        },
    )
    assert plan.status_code == 201
    assert plan.json()["data"]["rpo_hours"] == 2

    backup = await client.post(
        "/api/v1/business-continuity/backups",
        headers=headers,
        json={
            "name": "HR Weekly Backup",
            "backup_type": "full",
            "frequency_hours": 168,
            "retention_days": 60,
            "rpo_hours": 168,
        },
    )
    assert backup.status_code == 201
    assert backup.json()["data"]["encrypted"] is True


def test_engine_rpo_rto_and_dashboard():
    plans = [
        {"plan_type": "dr", "criticality_tier": "tier_1", "rpo_hours": 1, "rto_hours": 4, "status": "active"},
        {"plan_type": "bcp", "criticality_tier": "tier_2", "rpo_hours": 4, "rto_hours": 8, "status": "active"},
    ]
    backups = [{"rpo_hours": 1, "encrypted": True}]
    summary = continuity_engine.build_rpo_rto_summary(plans=plans, backups=backups, profile=None)
    assert summary["rpo"]["min_plan_hours"] == 1
    assert summary["rto"]["max_plan_hours"] == 8

    dashboard = continuity_engine.build_dashboard(
        profile=None, plans=plans, backups=backups, failovers=[], tests=[],
    )
    assert dashboard["summary"]["active_plans"] == 2

    test_result = continuity_engine.simulate_recovery_test(plan=plans[0])
    assert "passed" in test_result

    dm = continuity_engine.dependency_map()
    assert dm["no_continuity_duplication"] is True
