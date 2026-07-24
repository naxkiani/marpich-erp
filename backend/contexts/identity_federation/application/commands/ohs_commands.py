"""OHS dispatch / saga / outbox commands (P200-B10)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.application.cqrs.federation_buses import (
    BusEnvelope,
    get_command_bus,
    get_query_bus,
)
from contexts.identity_federation.domain.events.federation_integration_events import (
    FederationSagaCompensatedIntegration,
    FederationSagaCompletedIntegration,
)
from contexts.identity_federation.domain.services.federation_ohs_platform import (
    get_federation_ohs_platform,
)
from contexts.identity_federation.domain.services.federation_saga_engine import (
    get_federation_saga_engine,
)
from contexts.identity_federation.infrastructure.messaging.outbox_inbox_store import (
    FederationOutboxInboxStore,
)
from contexts.identity_federation.infrastructure.messaging.outbox_publisher import (
    OutboxFederationEventPublisher,
)
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from shared.domain.value_objects.tenant_id import TenantId


@dataclass(frozen=True, slots=True)
class DispatchCommandBusCommand:
    tenant_id: str
    name: str
    payload: dict = field(default_factory=dict)
    correlation_id: str = ""
    idempotency_key: str = ""


@dataclass(frozen=True, slots=True)
class DispatchQueryBusCommand:
    tenant_id: str
    name: str
    payload: dict = field(default_factory=dict)
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class PublishOhsEventCommand:
    tenant_id: str
    event_name: str
    payload: dict = field(default_factory=dict)
    event_version: int = 1
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class StartFederationSagaCommand:
    tenant_id: str
    saga_type: str
    context: dict = field(default_factory=dict)
    timeout_minutes: int = 60


@dataclass(frozen=True, slots=True)
class AdvanceFederationSagaCommand:
    tenant_id: str
    saga_ref: str
    step_ok: bool = True


@dataclass(frozen=True, slots=True)
class IngestInboxCommand:
    tenant_id: str
    event_id: str
    event_name: str
    consumer_id: str
    payload: dict = field(default_factory=dict)


async def handle_dispatch_command(command: DispatchCommandBusCommand) -> dict:
    result = await get_command_bus().dispatch(
        BusEnvelope(
            tenant_id=command.tenant_id,
            name=command.name,
            payload=command.payload,
            correlation_id=command.correlation_id,
            idempotency_key=command.idempotency_key,
        )
    )
    federation_protocol_metrics.increment("ohs_command_dispatched_total")
    return result


async def handle_dispatch_query(command: DispatchQueryBusCommand) -> dict:
    result = await get_query_bus().dispatch(
        BusEnvelope(
            tenant_id=command.tenant_id,
            name=command.name,
            payload=command.payload,
            correlation_id=command.correlation_id,
        )
    )
    federation_protocol_metrics.increment("ohs_query_dispatched_total")
    return result


async def handle_publish_ohs_event(command: PublishOhsEventCommand) -> dict:
    entry = await get_federation_ohs_platform().publish_event(
        tenant_id=command.tenant_id,
        event_name=command.event_name,
        payload=command.payload,
        event_version=command.event_version,
        correlation_id=command.correlation_id,
    )
    federation_protocol_metrics.increment("ohs_event_published_total")
    return entry


async def handle_start_federation_saga(command: StartFederationSagaCommand) -> dict:
    saga = get_federation_saga_engine().start(
        tenant_id=command.tenant_id,
        saga_type=command.saga_type,
        context=command.context,
        timeout_minutes=command.timeout_minutes,
    )
    federation_protocol_metrics.increment("ohs_saga_started_total")
    return saga


async def handle_advance_federation_saga(command: AdvanceFederationSagaCommand) -> dict:
    engine = get_federation_saga_engine()
    saga = engine.advance(
        tenant_id=command.tenant_id,
        saga_ref=command.saga_ref,
        step_ok=command.step_ok,
    )
    publisher = OutboxFederationEventPublisher()
    if saga["status"] == "completed":
        await publisher.publish(
            FederationSagaCompletedIntegration(
                tenant_id=TenantId(command.tenant_id),
                correlation_id=command.saga_ref,
                saga_ref=command.saga_ref,
                saga_type=saga["saga_type"],
                status="completed",
            )
        )
        FederationOutboxInboxStore.enqueue_outbox(
            tenant_id=command.tenant_id,
            event_name="federation.saga.completed",
            payload=saga,
            correlation_id=command.saga_ref,
        )
    elif saga["status"] == "compensated":
        await publisher.publish(
            FederationSagaCompensatedIntegration(
                tenant_id=TenantId(command.tenant_id),
                correlation_id=command.saga_ref,
                saga_ref=command.saga_ref,
                saga_type=saga["saga_type"],
                reason=str((saga.get("context") or {}).get("compensation_reason") or "step_failed"),
            )
        )
        FederationOutboxInboxStore.enqueue_outbox(
            tenant_id=command.tenant_id,
            event_name="federation.saga.compensated",
            payload=saga,
            correlation_id=command.saga_ref,
        )
    federation_protocol_metrics.increment("ohs_saga_advanced_total")
    return saga


async def handle_ingest_inbox(command: IngestInboxCommand) -> dict:
    entry = FederationOutboxInboxStore.ingest_inbox(
        tenant_id=command.tenant_id,
        event_id=command.event_id,
        event_name=command.event_name,
        consumer_id=command.consumer_id,
        payload=command.payload,
    )
    federation_protocol_metrics.increment("ohs_inbox_ingested_total")
    return entry
