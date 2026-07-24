"""RegisterIdentityProvider command (P200-B5)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.factories import IdentityProviderFactory
from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityProviderRepository,
)
from contexts.identity_federation.domain.services.identity_federation_engine import (
    get_identity_federation_engine,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics


@dataclass(frozen=True, slots=True)
class RegisterIdentityProviderCommand:
    tenant_id: str
    provider_ref: str | None = None
    protocol: str = "oidc"
    name: str = ""
    config: dict = field(default_factory=dict)
    plugin_id: str | None = None
    correlation_id: str = ""


async def handle_register_identity_provider(
    command: RegisterIdentityProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    negotiation = get_identity_federation_engine().negotiate_protocol(requested=command.protocol)
    if not negotiation.get("negotiated_protocol"):
        raise ValueError("federation.protocol.unsupported")
    ref = command.provider_ref or providers.next_provider_ref(command.tenant_id)
    provider = IdentityProviderFactory.create(
        tenant_id=command.tenant_id,
        provider_ref=ref,
        protocol=negotiation["negotiated_protocol"],
        name=command.name or ref,
        config=command.config,
    )
    if command.plugin_id:
        provider.plugin_id = command.plugin_id
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_registered_total")
    return provider.to_dict()
