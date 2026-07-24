"""Federation engine queries (P200-B5)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityLinkRepository,
    IIdentityProviderRepository,
    ISynchronizationJobRepository,
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services.eiftp_federation_engine import (
    validate_federation_engine_foundation,
)
from contexts.identity_federation.domain.services.identity_federation_engine import (
    get_identity_federation_engine,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics


@dataclass(frozen=True, slots=True)
class GetProviderQuery:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class GetTrustStatusQuery:
    tenant_id: str
    trust_ref: str


@dataclass(frozen=True, slots=True)
class GetIdentityMappingQuery:
    tenant_id: str
    user_id: str


@dataclass(frozen=True, slots=True)
class GetSynchronizationStatusQuery:
    tenant_id: str
    limit: int = 20


async def handle_get_provider(
    query: GetProviderQuery, *, providers: IIdentityProviderRepository
) -> dict:
    provider = await providers.find_by_ref(query.tenant_id, query.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    return provider.to_dict()


async def handle_get_trust_status(
    query: GetTrustStatusQuery, *, trusts: ITrustRelationshipRepository
) -> dict:
    for trust in await trusts.list_by_tenant(query.tenant_id):
        if trust.trust_ref == query.trust_ref:
            return {
                "trust_ref": trust.trust_ref,
                "status": trust.status,
                "trust_score": trust.trust_score,
                "trust_level": trust.trust_level,
            }
    raise ValueError("trust.not_found")


async def handle_get_identity_mapping(
    query: GetIdentityMappingQuery, *, links: IIdentityLinkRepository
) -> dict:
    items = await links.list_by_user(query.tenant_id, query.user_id)
    return {"user_id": query.user_id, "links": [i.to_dict() for i in items], "count": len(items)}


async def handle_get_synchronization_status(
    query: GetSynchronizationStatusQuery, *, sync_jobs: ISynchronizationJobRepository
) -> dict:
    jobs = await sync_jobs.list_by_tenant(query.tenant_id, limit=query.limit)
    return {"jobs": [j.to_dict() for j in jobs], "count": len(jobs)}


def handle_get_engine_surface() -> dict:
    engine = get_identity_federation_engine()
    validation = validate_federation_engine_foundation()
    return {
        "prompt": "P200-B5",
        "adr": 219,
        "protocols": engine.protocol_catalog(),
        "metrics": federation_protocol_metrics.snapshot(),
        "validation": validation,
    }
