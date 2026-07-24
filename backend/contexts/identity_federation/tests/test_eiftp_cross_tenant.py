"""P200-B8 Cross-Tenant Trust & Delegation foundation + CQRS tests."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.cross_tenant_commands import (
    ActivateExternalIdentityCommand,
    ActivateTenantTrustCommand,
    ApproveDelegationCommand,
    ApproveTenantTrustCommand,
    AssignPartnerAccessCommand,
    CreateDelegationCommand,
    InviteExternalIdentityCommand,
    RegisterPartnerCommand,
    RequestTenantTrustCommand,
    RevokeTenantTrustCommand,
    handle_activate_external_identity,
    handle_activate_tenant_trust,
    handle_approve_delegation,
    handle_approve_tenant_trust,
    handle_assign_partner_access,
    handle_create_delegation,
    handle_invite_external_identity,
    handle_register_partner,
    handle_request_tenant_trust,
    handle_revoke_tenant_trust,
)
from contexts.identity_federation.application.queries.cross_tenant_queries import (
    GetTrustHistoryQuery,
    handle_get_cross_tenant_surface,
    handle_get_trust_history,
)
from contexts.identity_federation.container import (
    get_delegation_repository,
    get_external_identity_repository,
    get_partner_access_repository,
    get_tenant_federation_repository,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.aggregates.cross_tenant_platform import DelegationAgreement
from contexts.identity_federation.domain.services.eiftp_cross_tenant import (
    validate_cross_tenant_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_cross_tenant_foundation_passes():
    result = validate_cross_tenant_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B9"
    assert result["unlimited_privileges_rejected"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_tenant_trust_lifecycle_never_implicit():
    feds = get_tenant_federation_repository()
    expires = (datetime.now(UTC) + timedelta(days=60)).isoformat()
    requested = await handle_request_tenant_trust(
        RequestTenantTrustCommand(
            tenant_id="tenant-a",
            partner_tenant_id="tenant-b",
            agreement={"purpose": "b2b_collaboration"},
            effective_until=expires,
            assess_inputs={"identity_assurance": 80, "risk_signals": 15},
        ),
        tenant_feds=feds,
    )
    assert requested["status"] == "pending_approval"
    assert requested["enabled"] is False
    assert requested["assessment"]["permit_deny"] is None
    ref = requested["federation_ref"]

    approved = await handle_approve_tenant_trust(
        ApproveTenantTrustCommand(tenant_id="tenant-a", federation_ref=ref, actor_id="approver-1"),
        tenant_feds=feds,
    )
    assert approved["agreement"]["approved"] is True

    activated = await handle_activate_tenant_trust(
        ActivateTenantTrustCommand(tenant_id="tenant-a", federation_ref=ref),
        tenant_feds=feds,
    )
    assert activated["status"] == "active"
    assert activated["enabled"] is True

    history = await handle_get_trust_history(
        GetTrustHistoryQuery(tenant_id="tenant-a", federation_ref=ref),
        tenant_feds=feds,
    )
    assert history["count"] >= 3

    revoked = await handle_revoke_tenant_trust(
        RevokeTenantTrustCommand(tenant_id="tenant-a", federation_ref=ref, reason="contract_end"),
        tenant_feds=feds,
    )
    assert revoked["status"] == "revoked"
    assert revoked["enabled"] is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delegation_partner_external_and_reject_star_perms():
    with pytest.raises(ValueError, match="unlimited"):
        DelegationAgreement.create(
            tenant_id="tenant-a",
            delegation_ref="bad",
            delegation_type="ai_agent",
            owner_id="org-1",
            delegate_id="agent-1",
            permissions=["*"],
        )

    created = await handle_create_delegation(
        CreateDelegationCommand(
            tenant_id="tenant-a",
            delegation_type="ai_agent",
            owner_id="org-1",
            delegate_id="agent-9",
            scope=["workflow.approve.limited"],
            permissions=["workflow.task.claim"],
            conditions={"max_amount": 1000},
        ),
        delegations=get_delegation_repository(),
    )
    assert created["status"] == "pending"
    approved = await handle_approve_delegation(
        ApproveDelegationCommand(
            tenant_id="tenant-a",
            delegation_ref=created["delegation_ref"],
            actor_id="owner-1",
        ),
        delegations=get_delegation_repository(),
    )
    assert approved["status"] == "active"

    partner = await handle_register_partner(
        RegisterPartnerCommand(
            tenant_id="tenant-a",
            partner_kind="supplier",
            organization_name="Acme Supply",
            partner_tenant_id="tenant-c",
        ),
        partners=get_partner_access_repository(),
    )
    assigned = await handle_assign_partner_access(
        AssignPartnerAccessCommand(
            tenant_id="tenant-a",
            partner_ref=partner["partner_ref"],
            scopes=["procurement.read"],
            policy_ref="pol-partner-1",
        ),
        partners=get_partner_access_repository(),
    )
    assert assigned["status"] == "access_assigned"

    invited = await handle_invite_external_identity(
        InviteExternalIdentityCommand(
            tenant_id="tenant-a",
            email="guest@example.com",
            identity_kind="guest",
            sponsor_id="user-1",
            access_scopes=["docs.read"],
        ),
        externals=get_external_identity_repository(),
    )
    activated = await handle_activate_external_identity(
        ActivateExternalIdentityCommand(
            tenant_id="tenant-a", external_ref=invited["external_ref"]
        ),
        externals=get_external_identity_repository(),
    )
    assert activated["status"] == "active"


@pytest.mark.unit
def test_surface_and_no_sibling_bc():
    surface = handle_get_cross_tenant_surface()
    assert surface["adr"] == 222
    assert surface["validation"]["passed"] is True
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
