"""Identity lifecycle — integration smoke tests."""
import pytest

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import LifecycleCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="lc-smoke",
        email="lc-smoke@enterprise.dev",
        display_name="Lifecycle Smoke",
    )
    resp = await integration_client.get("/api/v1/identity-lifecycle/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert LifecycleCapability.CONSENT_MANAGEMENT.value in caps
    assert len(caps) == 14


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_lifecycle_registration_to_activation(integration_client):
    tenant = "lc-flow"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="lc-flow-admin@enterprise.dev",
        display_name="Lifecycle Flow Admin",
    )
    await integration_client.post("/api/v1/identity-lifecycle/seed", headers=headers)

    register = await integration_client.post(
        "/api/v1/identity-lifecycle/cases",
        headers=headers,
        json={"email": "new-user@enterprise.dev", "display_name": "New User"},
    )
    assert register.status_code == 200
    case_ref = register.json()["data"]["case_ref"]

    consent = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/consent",
        headers=headers,
        json={"purpose": "terms_of_service", "granted": True},
    )
    assert consent.status_code == 200

    email_verify = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/verify",
        headers=headers,
        json={"verification_type": "email_verification", "payload": {"verified": True}},
    )
    assert email_verify.status_code == 200

    identity_verify = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/verify",
        headers=headers,
        json={"verification_type": "identity_verification", "payload": {"verified": True}},
    )
    assert identity_verify.status_code == 200

    activate = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/activate",
        headers=headers,
    )
    assert activate.status_code == 200
    assert activate.json()["data"]["state"] == "active"

    assistant = await integration_client.get(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/assistant",
        headers=headers,
    )
    assert assistant.status_code == 200
    assert assistant.json()["data"]["explainable"] is True

    audit = await integration_client.get(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/audit",
        headers=headers,
    )
    assert audit.status_code == 200
    assert len(audit.json()["data"]) >= 4


@pytest.mark.integration
@pytest.mark.asyncio
async def test_suspend_reactivate_archive_and_soft_delete(integration_client):
    tenant = "lc-states"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="lc-states-admin@enterprise.dev",
        display_name="Lifecycle States Admin",
    )
    await integration_client.post("/api/v1/identity-lifecycle/seed", headers=headers)

    register = await integration_client.post(
        "/api/v1/identity-lifecycle/cases",
        headers=headers,
        json={"email": "state-user@enterprise.dev", "display_name": "State User"},
    )
    case_ref = register.json()["data"]["case_ref"]

    await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/consent",
        headers=headers,
        json={"purpose": "privacy_policy", "granted": True},
    )
    for vtype in ("email_verification", "identity_verification"):
        await integration_client.post(
            f"/api/v1/identity-lifecycle/cases/{case_ref}/verify",
            headers=headers,
            json={"verification_type": vtype, "payload": {"verified": True}},
        )
    activate = await integration_client.post(f"/api/v1/identity-lifecycle/cases/{case_ref}/activate", headers=headers)
    assert activate.status_code == 200
    assert activate.json()["data"]["state"] == "active"

    suspend = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/suspend",
        headers=headers,
        json={"reason": "policy_violation"},
    )
    assert suspend.status_code == 200
    assert suspend.json()["data"]["state"] == "suspended"

    reactivate = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/reactivate",
        headers=headers,
    )
    assert reactivate.status_code == 200
    assert reactivate.json()["data"]["state"] == "active"

    archive = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/archive",
        headers=headers,
        json={"reason": "offboarding"},
    )
    assert archive.status_code == 200
    assert archive.json()["data"]["state"] == "archived"

    soft_delete = await integration_client.post(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/delete",
        headers=headers,
        json={"deletion_type": "soft", "reason": "gdpr_request"},
    )
    assert soft_delete.status_code == 200
    assert soft_delete.json()["data"]["state"] == "soft_deleted"

    workflow = await integration_client.get(
        f"/api/v1/identity-lifecycle/cases/{case_ref}/workflow",
        headers=headers,
    )
    assert workflow.status_code == 200
    assert "identity_recovery" in workflow.json()["data"]["available_actions"]

    dashboard = await integration_client.get("/api/v1/identity-lifecycle/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["total_cases"] >= 1
