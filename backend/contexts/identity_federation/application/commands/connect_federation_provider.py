"""Connect / disconnect / probe federation provider (P200-B5)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityProviderRepository,
)
from contexts.identity_federation.domain.ports.provider_health import IProviderHealthProbe
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics


@dataclass(frozen=True, slots=True)
class ConnectFederationProviderCommand:
    tenant_id: str
    provider_ref: str
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class DisconnectFederationProviderCommand:
    tenant_id: str
    provider_ref: str
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class ProbeProviderHealthCommand:
    tenant_id: str
    provider_ref: str


async def handle_connect_federation_provider(
    command: ConnectFederationProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await providers.find_by_ref(command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    conn = provider.connect_federation(correlation_id=command.correlation_id)
    await providers.save(provider)
    federation_protocol_metrics.increment("federation_connected_total")
    events = [e.event_name for e in provider.clear_events()]
    return {**provider.to_dict(), "primary_connection": conn.to_dict(), "domain_events": events}


async def handle_disconnect_federation_provider(
    command: DisconnectFederationProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await providers.find_by_ref(command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    conn = provider.disconnect_federation(correlation_id=command.correlation_id)
    await providers.save(provider)
    federation_protocol_metrics.increment("federation_disconnected_total")
    events = [e.event_name for e in provider.clear_events()]
    return {**provider.to_dict(), "primary_connection": conn.to_dict(), "domain_events": events}


async def handle_probe_provider_health(
    command: ProbeProviderHealthCommand,
    *,
    providers: IIdentityProviderRepository,
    health: IProviderHealthProbe,
) -> dict:
    provider = await providers.find_by_ref(command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    conn = provider.connections[0] if provider.connections else None
    result = await health.probe(
        tenant_id=command.tenant_id,
        provider_ref=provider.provider_ref,
        protocol=provider.protocol,
        endpoints=conn.endpoints if conn else {},
    )
    provider.update_health(health_status=result["health_status"], metadata={"probe": result})
    await providers.save(provider)
    return {**provider.to_dict(), "probe": result}
