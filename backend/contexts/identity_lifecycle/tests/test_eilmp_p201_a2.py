"""P201-A2 — Provisioning ACL + Workflow approvals."""
from __future__ import annotations

import pytest

from contexts.identity_lifecycle.container import (
    get_registration_onboarding_service,
    reset_identity_lifecycle_service,
)
from contexts.workflow.container import get_workflow_service, reset_workflow_service


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_lifecycle_service()
    reset_workflow_service()
    yield
    reset_identity_lifecycle_service()
    reset_workflow_service()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_provisioning_acl_creates_identity_user():
    svc = get_registration_onboarding_service()
    registered = await svc.register_identity(
        "tenant-a",
        email="prov-acl@example.com",
        display_name="Prov ACL",
        zt_context={"risk_score": 10, "device_trusted": True, "identity_evidence": True},
        auto_advance=True,
    )
    assert registered.succeeded, registered.error
    ref = registered.unwrap()["registration_ref"]
    await svc.initialize_profile("tenant-a", ref)
    await svc.start_onboarding("tenant-a", ref)
    prov = await svc.request_provisioning("tenant-a", ref)
    assert prov.succeeded, prov.error
    data = prov.unwrap()
    assert data["status"] == "activation_requested"
    assert data["onboarding"]["provisioning"].get("user_id")
    assert data["onboarding"]["provisioning"]["status"] == "completed"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_manual_approval_via_workflow():
    svc = get_registration_onboarding_service()
    registered = await svc.register_identity(
        "tenant-a",
        email="manual-wf@example.com",
        display_name="Manual WF",
        approval_mode="manual",
        zt_context={"risk_score": 10, "device_trusted": True, "identity_evidence": True},
        auto_advance=True,
        actor_id="approver-1",
    )
    assert registered.succeeded, registered.error
    data = registered.unwrap()
    assert data["status"] == "pending_approval"
    assert data["metadata"].get("workflow_instance_id")

    wf = get_workflow_service()
    tasks = await wf.list_tasks("tenant-a", "approver-1")
    assert tasks.succeeded
    task_list = tasks.unwrap()
    assert task_list
    task_id = task_list[0]["id"]
    completed = await wf.complete_task(
        tenant_id="tenant-a",
        correlation_id="corr-wf",
        task_id=task_id,
        outcome="approved",
        comment="ok",
        completed_by="approver-1",
    )
    assert completed.succeeded, completed.error

    status = await svc.get_registration("tenant-a", data["registration_ref"])
    assert status.succeeded
    assert status.unwrap()["status"] == "approved"
    assert status.unwrap()["case_ref"]
