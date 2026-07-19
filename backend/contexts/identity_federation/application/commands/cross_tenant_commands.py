"""Cross-tenant trust & delegation commands (P200-B8)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from contexts.identity_federation.domain.aggregates.cross_tenant_platform import (
    DelegationAgreement,
    ExternalIdentity,
    PartnerAccess,
)
from contexts.identity_federation.domain.aggregates.federation_platform import TenantFederation
from contexts.identity_federation.domain.ports.cross_tenant_repositories import (
    IDelegationRepository,
    IExternalIdentityRepository,
    IPartnerAccessRepository,
)
from contexts.identity_federation.domain.ports.federation_repositories import (
    ITenantFederationRepository,
)
from contexts.identity_federation.domain.services.cross_tenant_trust_engine import (
    get_cross_tenant_trust_engine,
)
from contexts.identity_federation.infrastructure.observability import federation_trust_metrics


def _parse_expires(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


@dataclass(frozen=True, slots=True)
class RequestTenantTrustCommand:
    tenant_id: str
    partner_tenant_id: str
    federation_ref: str | None = None
    federation_mode: str = "partner"
    agreement: dict = field(default_factory=dict)
    effective_until: str | None = None
    assess_inputs: dict = field(default_factory=dict)
    cross_tenant_enabled: bool = True


@dataclass(frozen=True, slots=True)
class ApproveTenantTrustCommand:
    tenant_id: str
    federation_ref: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class ActivateTenantTrustCommand:
    tenant_id: str
    federation_ref: str


@dataclass(frozen=True, slots=True)
class SuspendTenantTrustCommand:
    tenant_id: str
    federation_ref: str
    reason: str = "suspended"


@dataclass(frozen=True, slots=True)
class RevokeTenantTrustCommand:
    tenant_id: str
    federation_ref: str
    reason: str = "revoked"


@dataclass(frozen=True, slots=True)
class CreateDelegationCommand:
    tenant_id: str
    delegation_type: str
    owner_id: str
    delegate_id: str
    scope: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    conditions: dict = field(default_factory=dict)
    expires_at: str | None = None
    delegation_ref: str | None = None
    auto_approve: bool = False


@dataclass(frozen=True, slots=True)
class ApproveDelegationCommand:
    tenant_id: str
    delegation_ref: str
    actor_id: str | None = None
    activate: bool = True


@dataclass(frozen=True, slots=True)
class RevokeDelegationCommand:
    tenant_id: str
    delegation_ref: str
    reason: str = "revoked"


@dataclass(frozen=True, slots=True)
class RegisterPartnerCommand:
    tenant_id: str
    partner_kind: str
    organization_name: str = ""
    partner_tenant_id: str | None = None
    partner_ref: str | None = None
    expires_at: str | None = None


@dataclass(frozen=True, slots=True)
class AssignPartnerAccessCommand:
    tenant_id: str
    partner_ref: str
    scopes: list[str] = field(default_factory=list)
    policy_ref: str | None = None


@dataclass(frozen=True, slots=True)
class InviteExternalIdentityCommand:
    tenant_id: str
    email: str
    identity_kind: str = "guest"
    sponsor_id: str | None = None
    access_scopes: list[str] = field(default_factory=list)
    expires_at: str | None = None
    external_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ActivateExternalIdentityCommand:
    tenant_id: str
    external_ref: str


@dataclass(frozen=True, slots=True)
class RemoveExternalIdentityCommand:
    tenant_id: str
    external_ref: str
    reason: str = "removed"


async def _load_fed(
    feds: ITenantFederationRepository, tenant_id: str, federation_ref: str
) -> TenantFederation | None:
    for item in await feds.list_by_tenant(tenant_id):
        if item.federation_ref == federation_ref:
            return item
    return None


async def handle_request_tenant_trust(
    command: RequestTenantTrustCommand,
    *,
    tenant_feds: ITenantFederationRepository,
) -> dict:
    engine = get_cross_tenant_trust_engine()
    assessment = engine.assess_trust_request(
        cross_tenant_enabled=command.cross_tenant_enabled,
        inputs=command.assess_inputs,
    )
    if not assessment["allowed_to_proceed"]:
        raise ValueError(f"cross_tenant.assessment_failed:{assessment.get('reason')}")
    ref = command.federation_ref or tenant_feds.next_federation_ref(command.tenant_id)
    fed = TenantFederation.request_trust(
        tenant_id=command.tenant_id,
        federation_ref=ref,
        partner_tenant_id=command.partner_tenant_id,
        federation_mode=command.federation_mode,
        agreement=command.agreement,
        effective_until=_parse_expires(command.effective_until),
    )
    fed.apply_assessment(
        trust_score=assessment["trust_score"],
        trust_level=assessment["trust_level"],
        factors=list(assessment["assessment"].get("factors") or []),
    )
    await tenant_feds.save(fed)
    federation_trust_metrics.increment("cross_tenant_trust_requested_total")
    return {**fed.to_dict(), "assessment": assessment}


async def handle_approve_tenant_trust(
    command: ApproveTenantTrustCommand,
    *,
    tenant_feds: ITenantFederationRepository,
) -> dict:
    fed = await _load_fed(tenant_feds, command.tenant_id, command.federation_ref)
    if fed is None:
        raise ValueError("cross_tenant.not_found")
    fed.approve(actor_id=command.actor_id)
    await tenant_feds.save(fed)
    federation_trust_metrics.increment("cross_tenant_trust_approved_total")
    return fed.to_dict()


async def handle_activate_tenant_trust(
    command: ActivateTenantTrustCommand,
    *,
    tenant_feds: ITenantFederationRepository,
) -> dict:
    fed = await _load_fed(tenant_feds, command.tenant_id, command.federation_ref)
    if fed is None:
        raise ValueError("cross_tenant.not_found")
    fed.activate()
    await tenant_feds.save(fed)
    federation_trust_metrics.increment("cross_tenant_trust_activated_total")
    return fed.to_dict()


async def handle_suspend_tenant_trust(
    command: SuspendTenantTrustCommand,
    *,
    tenant_feds: ITenantFederationRepository,
) -> dict:
    fed = await _load_fed(tenant_feds, command.tenant_id, command.federation_ref)
    if fed is None:
        raise ValueError("cross_tenant.not_found")
    fed.suspend(reason=command.reason)
    await tenant_feds.save(fed)
    federation_trust_metrics.increment("cross_tenant_trust_suspended_total")
    return fed.to_dict()


async def handle_revoke_tenant_trust(
    command: RevokeTenantTrustCommand,
    *,
    tenant_feds: ITenantFederationRepository,
) -> dict:
    fed = await _load_fed(tenant_feds, command.tenant_id, command.federation_ref)
    if fed is None:
        raise ValueError("cross_tenant.not_found")
    fed.revoke(reason=command.reason)
    await tenant_feds.save(fed)
    federation_trust_metrics.increment("cross_tenant_trust_revoked_total")
    return fed.to_dict()


async def handle_create_delegation(
    command: CreateDelegationCommand,
    *,
    delegations: IDelegationRepository,
) -> dict:
    ref = command.delegation_ref or delegations.next_ref(command.tenant_id)
    agreement = DelegationAgreement.create(
        tenant_id=command.tenant_id,
        delegation_ref=ref,
        delegation_type=command.delegation_type,
        owner_id=command.owner_id,
        delegate_id=command.delegate_id,
        scope=command.scope,
        permissions=command.permissions,
        conditions=command.conditions,
        expires_at=_parse_expires(command.expires_at),
    )
    if command.auto_approve:
        agreement.approve()
        agreement.activate()
    await delegations.save(agreement)
    federation_trust_metrics.increment("delegation_created_total")
    return agreement.to_dict()


async def _load_delegation(
    repos: IDelegationRepository, tenant_id: str, delegation_ref: str
) -> DelegationAgreement | None:
    for item in await repos.list_by_tenant(tenant_id, limit=200):
        if item.delegation_ref == delegation_ref:
            return item
    return None


async def handle_approve_delegation(
    command: ApproveDelegationCommand,
    *,
    delegations: IDelegationRepository,
) -> dict:
    agreement = await _load_delegation(delegations, command.tenant_id, command.delegation_ref)
    if agreement is None:
        raise ValueError("delegation.not_found")
    agreement.approve(actor_id=command.actor_id)
    if command.activate:
        agreement.activate()
    await delegations.save(agreement)
    federation_trust_metrics.increment("delegation_approved_total")
    return agreement.to_dict()


async def handle_revoke_delegation(
    command: RevokeDelegationCommand,
    *,
    delegations: IDelegationRepository,
) -> dict:
    agreement = await _load_delegation(delegations, command.tenant_id, command.delegation_ref)
    if agreement is None:
        raise ValueError("delegation.not_found")
    agreement.revoke(reason=command.reason)
    await delegations.save(agreement)
    federation_trust_metrics.increment("delegation_revoked_total")
    return agreement.to_dict()


async def handle_register_partner(
    command: RegisterPartnerCommand,
    *,
    partners: IPartnerAccessRepository,
) -> dict:
    ref = command.partner_ref or partners.next_ref(command.tenant_id)
    partner = PartnerAccess.register(
        tenant_id=command.tenant_id,
        partner_ref=ref,
        partner_kind=command.partner_kind,
        organization_name=command.organization_name,
        partner_tenant_id=command.partner_tenant_id,
        expires_at=_parse_expires(command.expires_at),
    )
    await partners.save(partner)
    federation_trust_metrics.increment("partner_registered_total")
    return partner.to_dict()


async def handle_assign_partner_access(
    command: AssignPartnerAccessCommand,
    *,
    partners: IPartnerAccessRepository,
) -> dict:
    for partner in await partners.list_by_tenant(command.tenant_id, limit=200):
        if partner.partner_ref == command.partner_ref:
            partner.assign_access(scopes=command.scopes, policy_ref=command.policy_ref)
            await partners.save(partner)
            federation_trust_metrics.increment("partner_access_assigned_total")
            return partner.to_dict()
    raise ValueError("partner.not_found")


async def handle_invite_external_identity(
    command: InviteExternalIdentityCommand,
    *,
    externals: IExternalIdentityRepository,
) -> dict:
    ref = command.external_ref or externals.next_ref(command.tenant_id)
    identity = ExternalIdentity.invite(
        tenant_id=command.tenant_id,
        external_ref=ref,
        identity_kind=command.identity_kind,
        email=command.email,
        sponsor_id=command.sponsor_id,
        access_scopes=command.access_scopes,
        expires_at=_parse_expires(command.expires_at),
    )
    await externals.save(identity)
    federation_trust_metrics.increment("external_identity_invited_total")
    return identity.to_dict()


async def handle_activate_external_identity(
    command: ActivateExternalIdentityCommand,
    *,
    externals: IExternalIdentityRepository,
) -> dict:
    for identity in await externals.list_by_tenant(command.tenant_id, limit=200):
        if identity.external_ref == command.external_ref:
            identity.activate()
            await externals.save(identity)
            federation_trust_metrics.increment("external_identity_activated_total")
            return identity.to_dict()
    raise ValueError("external.not_found")


async def handle_remove_external_identity(
    command: RemoveExternalIdentityCommand,
    *,
    externals: IExternalIdentityRepository,
) -> dict:
    for identity in await externals.list_by_tenant(command.tenant_id, limit=200):
        if identity.external_ref == command.external_ref:
            identity.remove(reason=command.reason)
            await externals.save(identity)
            federation_trust_metrics.increment("external_identity_removed_total")
            return identity.to_dict()
    raise ValueError("external.not_found")
