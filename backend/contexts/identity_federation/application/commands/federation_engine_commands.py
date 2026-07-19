"""ExchangeFederatedToken + MapIdentity + ResolveSyncConflict (P200-B5)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.factories import IdentityLinkFactory
from contexts.identity_federation.domain.ports.federation_repositories import (
    IIdentityLinkRepository,
    ISynchronizationJobRepository,
)
from contexts.identity_federation.domain.services.identity_federation_engine import (
    get_identity_federation_engine,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, slots=True)
class ExchangeFederatedTokenCommand:
    tenant_id: str
    source_type: str
    target_type: str
    subject: str
    audience: str
    scopes: list[str] = field(default_factory=list)
    claims: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MapIdentityCommand:
    tenant_id: str
    user_id: str
    provider_id: str
    external_subject: str
    raw_claims: dict = field(default_factory=dict)
    mappings: list[dict] = field(default_factory=list)
    link_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ResolveSyncConflictCommand:
    tenant_id: str
    primary: dict
    secondary: dict
    strategy: str = "prefer_verified"
    job_ref: str | None = None


async def handle_exchange_federated_token(command: ExchangeFederatedTokenCommand) -> dict:
    engine = get_identity_federation_engine()
    result = engine.exchange_token(
        source_type=command.source_type,
        target_type=command.target_type,
        subject=command.subject,
        audience=command.audience,
        scopes=command.scopes,
        claims=command.claims,
    )
    if result.get("exchanged"):
        federation_protocol_metrics.increment("token_exchange_total")
    else:
        federation_protocol_metrics.increment("token_exchange_error_total")
    return {"tenant_id": command.tenant_id, **result}


async def handle_map_identity(
    command: MapIdentityCommand,
    *,
    links: IIdentityLinkRepository,
) -> dict:
    engine = get_identity_federation_engine()
    mapped = engine.transform_claims(raw_claims=command.raw_claims, mappings=command.mappings)
    link = IdentityLinkFactory.create(
        tenant_id=command.tenant_id,
        link_ref=command.link_ref or links.next_link_ref(command.tenant_id),
        user_id=command.user_id,
        provider_id=command.provider_id,
        external_subject=command.external_subject,
    )
    link.activate()
    await links.save(link)
    federation_protocol_metrics.increment("identity_mapped_total")
    events = [e.event_name for e in link.clear_events()]
    return {
        "link": link.to_dict(),
        "mapped_claims": mapped,
        "domain_events": events,
    }


async def handle_resolve_sync_conflict(
    command: ResolveSyncConflictCommand,
    *,
    sync_jobs: ISynchronizationJobRepository | None = None,
) -> dict:
    engine = get_identity_federation_engine()
    resolution = engine.resolve_identity_conflict(
        primary=command.primary,
        secondary=command.secondary,
        strategy=command.strategy,
    )
    federation_protocol_metrics.increment("sync_conflict_resolved_total")
    job_payload = None
    if sync_jobs is not None and command.job_ref:
        # best-effort annotate job metadata when present
        jobs = await sync_jobs.list_by_tenant(command.tenant_id, limit=100)
        for job in jobs:
            if job.job_ref == command.job_ref:
                job.metadata = {**(job.metadata or {}), "last_conflict": resolution}
                await sync_jobs.save(job)
                job_payload = job.to_dict()
                break
    return {
        "tenant_id": command.tenant_id,
        "resolution": resolution,
        "job": job_payload,
        "correlation": str(UniqueId.generate()),
    }
