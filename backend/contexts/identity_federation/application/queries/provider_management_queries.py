"""Identity Provider Management queries (P200-B7)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityProviderRepository,
    ISynchronizationJobRepository,
)
from contexts.identity_federation.domain.services.eiftp_identity_providers import (
    validate_identity_providers_foundation,
)
from contexts.identity_federation.domain.services.identity_provider_platform import (
    get_identity_provider_platform,
)
from contexts.identity_federation.domain.value_objects.provider_types import provider_trust_label
from contexts.identity_federation.infrastructure.plugins import protocol_plugin_sdk


@dataclass(frozen=True, slots=True)
class GetManagedProviderQuery:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class GetProviderHealthQuery:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class GetFederationConnectionsQuery:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class GetProviderTrustScoreQuery:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class GetSyncStatusQuery:
    tenant_id: str
    provider_ref: str | None = None
    limit: int = 20


async def _load(providers: IIdentityProviderRepository, tenant_id: str, provider_ref: str):
    for p in await providers.list_by_tenant(tenant_id):
        if p.provider_ref == provider_ref:
            return p
    return None


async def handle_get_managed_provider(
    query: GetManagedProviderQuery, *, providers: IIdentityProviderRepository
) -> dict:
    provider = await _load(providers, query.tenant_id, query.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    return provider.to_dict()


async def handle_get_provider_health(
    query: GetProviderHealthQuery, *, providers: IIdentityProviderRepository
) -> dict:
    provider = await _load(providers, query.tenant_id, query.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    conn = provider.connections[0] if provider.connections else None
    return {
        "provider_ref": provider.provider_ref,
        "lifecycle_status": provider.lifecycle_status,
        "enabled": provider.enabled,
        "health_status": conn.health_status if conn else "unknown",
        "connection": conn.to_dict() if conn else None,
    }


async def handle_get_federation_connections(
    query: GetFederationConnectionsQuery, *, providers: IIdentityProviderRepository
) -> dict:
    provider = await _load(providers, query.tenant_id, query.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    items = [c.to_dict() for c in provider.connections]
    return {"provider_ref": provider.provider_ref, "connections": items, "count": len(items)}


async def handle_get_provider_trust_score(
    query: GetProviderTrustScoreQuery, *, providers: IIdentityProviderRepository
) -> dict:
    provider = await _load(providers, query.tenant_id, query.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    return {
        "provider_ref": provider.provider_ref,
        "trust_level": provider.trust_level,
        "trust_label": provider_trust_label(provider.trust_level),
        "trust_score": (provider.security_profile or {}).get("trust_score"),
        "trust_ref": provider.trust_ref,
    }


def handle_get_mapping_rules_catalog() -> dict:
    return {"catalog": get_identity_provider_platform().surface()["mapping"]}


def handle_get_protocol_plugins(*, protocol: str | None = None) -> dict:
    return {
        "plugins": protocol_plugin_sdk.list_protocol_plugins(
            protocol=protocol, include_disabled=True
        )
    }


async def handle_get_sync_status(
    query: GetSyncStatusQuery, *, sync_jobs: ISynchronizationJobRepository
) -> dict:
    jobs = await sync_jobs.list_by_tenant(query.tenant_id, limit=min(query.limit, 100))
    items = [j.to_dict() for j in jobs]
    if query.provider_ref:
        items = [j for j in items if j.get("provider_id") == query.provider_ref]
    return {"jobs": items, "count": len(items)}


def handle_get_provider_surface() -> dict:
    surface = get_identity_provider_platform().surface()
    return {
        **surface,
        "validation": validate_identity_providers_foundation(),
    }
