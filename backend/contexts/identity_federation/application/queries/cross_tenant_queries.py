"""Cross-tenant trust & delegation queries (P200-B8)."""
from __future__ import annotations

from dataclasses import dataclass

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
from contexts.identity_federation.domain.services.eiftp_cross_tenant import (
    validate_cross_tenant_foundation,
)


@dataclass(frozen=True, slots=True)
class GetTenantTrustQuery:
    tenant_id: str
    federation_ref: str


@dataclass(frozen=True, slots=True)
class GetTrustHistoryQuery:
    tenant_id: str
    federation_ref: str


@dataclass(frozen=True, slots=True)
class GetDelegationsQuery:
    tenant_id: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetDelegationAuditQuery:
    tenant_id: str
    delegation_ref: str


@dataclass(frozen=True, slots=True)
class GetPartnerAccessQuery:
    tenant_id: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetExternalIdentitiesQuery:
    tenant_id: str
    limit: int = 50


async def handle_get_tenant_trust(
    query: GetTenantTrustQuery, *, tenant_feds: ITenantFederationRepository
) -> dict:
    for fed in await tenant_feds.list_by_tenant(query.tenant_id):
        if fed.federation_ref == query.federation_ref:
            gate = get_cross_tenant_trust_engine().access_gate(trust_status=fed.status)
            return {**fed.to_dict(), "access_gate": gate}
    raise ValueError("cross_tenant.not_found")


async def handle_get_trust_history(
    query: GetTrustHistoryQuery, *, tenant_feds: ITenantFederationRepository
) -> dict:
    for fed in await tenant_feds.list_by_tenant(query.tenant_id):
        if fed.federation_ref == query.federation_ref:
            return {
                "federation_ref": fed.federation_ref,
                "history": list(fed.history or []),
                "count": len(fed.history or []),
            }
    raise ValueError("cross_tenant.not_found")


async def handle_get_delegations(
    query: GetDelegationsQuery, *, delegations: IDelegationRepository
) -> dict:
    items = await delegations.list_by_tenant(query.tenant_id, limit=min(query.limit, 100))
    for item in items:
        item.ensure_not_expired()
    return {
        "delegations": [d.to_dict() for d in items],
        "count": len(items),
    }


async def handle_get_delegation_audit(
    query: GetDelegationAuditQuery, *, delegations: IDelegationRepository
) -> dict:
    for item in await delegations.list_by_tenant(query.tenant_id, limit=200):
        if item.delegation_ref == query.delegation_ref:
            return {
                "delegation_ref": item.delegation_ref,
                "audit": list(item.audit or []),
                "status": item.status,
            }
    raise ValueError("delegation.not_found")


async def handle_get_partner_access(
    query: GetPartnerAccessQuery, *, partners: IPartnerAccessRepository
) -> dict:
    items = await partners.list_by_tenant(query.tenant_id, limit=min(query.limit, 100))
    return {"partners": [p.to_dict() for p in items], "count": len(items)}


async def handle_get_external_identities(
    query: GetExternalIdentitiesQuery, *, externals: IExternalIdentityRepository
) -> dict:
    items = await externals.list_by_tenant(query.tenant_id, limit=min(query.limit, 100))
    return {"external_identities": [e.to_dict() for e in items], "count": len(items)}


def handle_get_cross_tenant_surface() -> dict:
    return {
        **get_cross_tenant_trust_engine().catalog(),
        "validation": validate_cross_tenant_foundation(),
    }
