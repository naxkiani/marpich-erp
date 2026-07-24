"""Identity Provider Management commands (P200-B7)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.aggregates.federation_platform import SynchronizationJob
from contexts.identity_federation.domain.factories import IdentityProviderFactory
from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityProviderRepository,
    ISynchronizationJobRepository,
)
from contexts.identity_federation.domain.services.identity_provider_platform import (
    get_identity_provider_platform,
)
from contexts.identity_federation.infrastructure.certificates.certificate_manager import (
    CertificateManager,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from contexts.identity_federation.infrastructure.plugins import protocol_plugin_sdk
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, slots=True)
class RegisterManagedProviderCommand:
    tenant_id: str
    provider_ref: str | None = None
    protocol: str = "oidc"
    name: str = ""
    provider_type: str = "external_enterprise"
    config: dict = field(default_factory=dict)
    plugin_id: str | None = None
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class ConfigureProviderCommand:
    tenant_id: str
    provider_ref: str
    config: dict = field(default_factory=dict)
    security_profile: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class VerifyProviderCommand:
    tenant_id: str
    provider_ref: str


@dataclass(frozen=True, slots=True)
class ActivateIdentityProviderCommand:
    tenant_id: str
    provider_ref: str
    correlation_id: str = ""
    min_trust_level: int = 1


@dataclass(frozen=True, slots=True)
class SuspendIdentityProviderCommand:
    tenant_id: str
    provider_ref: str
    reason: str = "suspended"
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class CreateFederationConnectionCommand:
    tenant_id: str
    provider_ref: str
    connection_ref: str | None = None
    protocol: str | None = None
    endpoints: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InstallProtocolPluginCommand:
    plugin_id: str
    protocol: str
    name: str
    version: str = "1.0.0"
    capabilities: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CreateMappingRuleCommand:
    tenant_id: str
    source_claims: dict = field(default_factory=dict)
    rules: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SynchronizeIdentityCommand:
    tenant_id: str
    provider_ref: str
    mode: str = "batch"
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class ValidateProviderTrustCommand:
    tenant_id: str
    provider_ref: str
    inputs: dict = field(default_factory=dict)
    zero_trust_ctx: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RotateProviderCertificateCommand:
    tenant_id: str
    provider_ref: str
    cert_ref: str | None = None
    pem: str = "-----BEGIN CERTIFICATE-----\nMEOS\n-----END CERTIFICATE-----"


async def _load(providers: IIdentityProviderRepository, tenant_id: str, provider_ref: str):
    for p in await providers.list_by_tenant(tenant_id):
        if p.provider_ref == provider_ref:
            return p
    return None


async def handle_register_managed_provider(
    command: RegisterManagedProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    platform = get_identity_provider_platform()
    negotiation = platform.negotiate_protocol(requested=command.protocol)
    if not negotiation.get("negotiated_protocol"):
        raise ValueError("federation.protocol.unsupported")
    protocol = negotiation["negotiated_protocol"]
    plugin = command.plugin_id or (platform.resolve_plugin_for_protocol(protocol) or {}).get("plugin_id")
    if plugin is None:
        raise ValueError("federation.protocol.plugin_missing")
    ref = command.provider_ref or providers.next_provider_ref(command.tenant_id)
    provider = IdentityProviderFactory.create(
        tenant_id=command.tenant_id,
        provider_ref=ref,
        protocol=protocol,
        name=command.name or ref,
        config=command.config,
    )
    provider.provider_type = platform.normalize_type(command.provider_type)
    provider.plugin_id = plugin
    provider.lifecycle_status = "registered"
    provider.enabled = False
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_registered_total")
    return provider.to_dict()


async def handle_configure_provider(
    command: ConfigureProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    provider.configure(config=command.config, security_profile=command.security_profile)
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_configured_total")
    return provider.to_dict()


async def handle_verify_provider(
    command: VerifyProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    provider.verify()
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_verified_total")
    return provider.to_dict()


async def handle_activate_identity_provider(
    command: ActivateIdentityProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    platform = get_identity_provider_platform()
    conn = provider.connections[0] if provider.connections else None
    gate = platform.activation_gate(
        lifecycle_status=provider.lifecycle_status,
        has_endpoints=bool((conn and conn.endpoints) or (provider.config or {}).get("endpoints")),
        has_plugin=bool(provider.plugin_id)
        and protocol_plugin_sdk.protocol_plugin_exists_for(provider.protocol),
        trust_level=provider.trust_level,
        min_trust_level=command.min_trust_level,
    )
    if not gate["allowed"]:
        raise ValueError(f"provider.activate_blocked:{','.join(gate['reasons'])}")
    provider.activate(correlation_id=command.correlation_id)
    events = [e.event_name for e in provider.clear_events()]
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_activated_total")
    return {**provider.to_dict(), "activation_gate": gate, "domain_events": events}


async def handle_suspend_identity_provider(
    command: SuspendIdentityProviderCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    provider.suspend_provider(reason=command.reason, correlation_id=command.correlation_id)
    events = [e.event_name for e in provider.clear_events()]
    await providers.save(provider)
    federation_protocol_metrics.increment("idp_suspended_total")
    return {**provider.to_dict(), "domain_events": events}


async def handle_create_federation_connection(
    command: CreateFederationConnectionCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    ref = command.connection_ref or f"{command.provider_ref}-conn-{len(provider.connections)+1}"
    conn = provider.add_connection(
        connection_ref=ref,
        protocol=command.protocol,
        endpoints=command.endpoints,
    )
    await providers.save(provider)
    federation_protocol_metrics.increment("federation_connection_created_total")
    return {"provider_ref": provider.provider_ref, "connection": conn.to_dict()}


async def handle_install_protocol_plugin(command: InstallProtocolPluginCommand) -> dict:
    installed = protocol_plugin_sdk.install_protocol_plugin(
        plugin_id=command.plugin_id,
        protocol=command.protocol,
        name=command.name,
        version=command.version,
        capabilities=command.capabilities,
    )
    federation_protocol_metrics.increment("protocol_plugin_installed_total")
    return installed


async def handle_create_mapping_rule(command: CreateMappingRuleCommand) -> dict:
    result = get_identity_provider_platform().map_identity(
        source_claims=command.source_claims, rules=command.rules
    )
    federation_protocol_metrics.increment("mapping_rule_applied_total")
    return {"tenant_id": command.tenant_id, **result}


async def handle_synchronize_identity(
    command: SynchronizeIdentityCommand,
    *,
    providers: IIdentityProviderRepository,
    sync_jobs: ISynchronizationJobRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    if provider.lifecycle_status != "active":
        raise ValueError("provider.sync_requires_active")
    job = SynchronizationJob(
        id=UniqueId.generate(),
        tenant_id=command.tenant_id,
        job_ref=sync_jobs.next_job_ref(command.tenant_id),
        provider_id=command.provider_ref,
        direction="inbound" if command.mode != "outbound" else "outbound",
        status="queued",
        metadata={"mode": command.mode, "correlation_id": command.correlation_id},
    )
    await sync_jobs.save(job)
    provider.security_profile = {
        **(provider.security_profile or {}),
        "last_sync_job": job.job_ref,
        "last_sync_mode": command.mode,
    }
    await providers.save(provider)
    federation_protocol_metrics.increment("identity_sync_queued_total")
    return {**job.to_dict(), "provider_ref": command.provider_ref}


async def handle_validate_provider_trust(
    command: ValidateProviderTrustCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    evaluation = get_identity_provider_platform().evaluate_provider_trust(
        inputs=command.inputs,
        prior_score=int((provider.security_profile or {}).get("trust_score") or 50),
        zero_trust_ctx=command.zero_trust_ctx,
    )
    provider.apply_trust(
        trust_level=evaluation["provider_trust_level"],
        score=evaluation["trust_score"],
    )
    await providers.save(provider)
    federation_protocol_metrics.increment("provider_trust_evaluated_total")
    return {
        "provider_ref": command.provider_ref,
        "evaluation": evaluation,
        "permit_deny": None,
    }


async def handle_rotate_provider_certificate(
    command: RotateProviderCertificateCommand,
    *,
    providers: IIdentityProviderRepository,
) -> dict:
    provider = await _load(providers, command.tenant_id, command.provider_ref)
    if provider is None:
        raise ValueError("provider.not_found")
    certs = CertificateManager()
    cert_ref = command.cert_ref or f"{command.provider_ref}-signing"
    registered = certs.register_certificate(
        tenant_id=command.tenant_id,
        cert_ref=cert_ref,
        pem=command.pem,
        purpose="signing",
    )
    rotated = certs.rotate_jwks(tenant_id=command.tenant_id)
    provider.security_profile = {
        **(provider.security_profile or {}),
        "certificate": {**registered, **rotated},
    }
    await providers.save(provider)
    federation_protocol_metrics.increment("provider_certificate_rotated_total")
    return {
        "provider_ref": command.provider_ref,
        "certificate": registered,
        "rotation": rotated,
    }
