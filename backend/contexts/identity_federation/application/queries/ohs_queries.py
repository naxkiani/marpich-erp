"""OHS discovery queries (P200-B10)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.services.eiftp_ohs_apis_events_cqrs import (
    validate_ohs_apis_events_cqrs_foundation,
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


@dataclass(frozen=True, slots=True)
class GetSagaQuery:
    tenant_id: str
    saga_ref: str


@dataclass(frozen=True, slots=True)
class GetOutboxQuery:
    tenant_id: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetInboxQuery:
    tenant_id: str
    limit: int = 50


def handle_get_ohs_surface() -> dict:
    return {
        **get_federation_ohs_platform().catalog(),
        "validation": validate_ohs_apis_events_cqrs_foundation(),
    }


def handle_get_ohs_apis() -> dict:
    return get_federation_ohs_platform().api_registry()


def handle_get_ohs_events() -> dict:
    events = get_federation_ohs_platform().event_catalog()
    return {"events": events, "count": len(events)}


def handle_get_ohs_cqrs() -> dict:
    return get_federation_ohs_platform().cqrs_registry()


def handle_get_saga(query: GetSagaQuery) -> dict:
    return get_federation_saga_engine().get(
        tenant_id=query.tenant_id, saga_ref=query.saga_ref
    )


def handle_get_outbox(query: GetOutboxQuery) -> dict:
    items = FederationOutboxInboxStore.list_outbox(
        tenant_id=query.tenant_id, limit=min(query.limit, 100)
    )
    return {"outbox": items, "count": len(items)}


def handle_get_inbox(query: GetInboxQuery) -> dict:
    items = FederationOutboxInboxStore.list_inbox(
        tenant_id=query.tenant_id, limit=min(query.limit, 100)
    )
    return {"inbox": items, "count": len(items)}
