"""Federation Open Host Service catalog & event registry (P200-B10)."""
from __future__ import annotations

from pathlib import Path

import yaml

from contexts.identity_federation.application.cqrs.federation_buses import (
    get_command_bus,
    get_query_bus,
)
from contexts.identity_federation.infrastructure.messaging.outbox_inbox_store import (
    FederationOutboxInboxStore,
)
from contexts.identity_federation.infrastructure.messaging.outbox_publisher import (
    OutboxFederationEventPublisher,
)


REPO_ROOT = Path(__file__).resolve().parents[5]


class FederationOhsPlatform:
    """OHS facade — discovery + standardized dispatch — not Integration Platform."""

    def event_catalog(self) -> list[dict]:
        path = (
            REPO_ROOT
            / "docs/architecture/identity/eiftp/OHS_EVENT_CATALOG.v1.yaml"
        )
        if not path.exists():
            return []
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return list(data.get("events") or [])

    def api_registry(self) -> dict:
        return {
            "rest": [
                "/api/v1/federation/engine",
                "/api/v1/federation/trust-fabric",
                "/api/v1/federation/providers",
                "/api/v1/federation/cross-tenant",
                "/api/v1/federation/security",
                "/api/v1/federation/ohs",
                "/api/v1/federation/ops",
                "/api/v1/federation/qa",
            ],
            "graphql": "/graphql/v1/federation",
            "graphql_contract": "backend/shared/contracts/graphql/federation.graphql",
            "grpc": "marpich.federation.v1.FederationService",
            "grpc_contract": "backend/shared/contracts/grpc/federation/v1/federation.proto",
            "api_contract_catalog": "backend/shared/contracts/api_contract_catalog.yaml",
        }

    def cqrs_registry(self) -> dict:
        return {
            "commands": get_command_bus().catalog(),
            "queries": get_query_bus().catalog(),
            "middleware": ["tenant", "idempotency", "correlation", "metrics"],
        }

    def catalog(self) -> dict:
        return {
            "prompt": "P200-B10",
            "adr": 224,
            "role": "open_host_service",
            "not": ["integration_platform", "authorization_pdp", "event_fabric_transport"],
            "apis": self.api_registry(),
            "cqrs": self.cqrs_registry(),
            "events": self.event_catalog(),
            "patterns": [
                "outbox",
                "inbox",
                "idempotency",
                "correlation_id",
                "saga_orchestration",
                "choreography_via_events",
            ],
            "principles": [
                "api_first",
                "event_driven",
                "no_direct_coupling",
                "tenant_isolation",
                "zero_trust_headers",
                "horizontal_scale",
            ],
        }

    async def publish_event(
        self,
        *,
        tenant_id: str,
        event_name: str,
        payload: dict,
        event_version: int = 1,
        correlation_id: str = "",
    ) -> dict:
        known = {e["name"] for e in self.event_catalog()}
        if known and event_name not in known:
            raise ValueError("ohs.event_not_in_catalog")
        entry = FederationOutboxInboxStore.enqueue_outbox(
            tenant_id=tenant_id,
            event_name=event_name,
            payload=payload,
            event_version=event_version,
            correlation_id=correlation_id,
        )
        from contexts.identity_federation.domain.events.federation_integration_events import (
            FederationCatalogEventIntegration,
        )
        from shared.domain.value_objects.tenant_id import TenantId

        publisher = OutboxFederationEventPublisher()
        try:
            await publisher.publish(
                FederationCatalogEventIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=entry["correlation_id"],
                    catalog_event_name=event_name,
                    catalog_event_version=event_version,
                    body=payload,
                )
            )
            FederationOutboxInboxStore.mark_published(entry["outbox_id"])
            entry["status"] = "published"
        except Exception:
            # Outbox remains pending for dispatcher retry (B11 ops)
            entry["status"] = "pending"
        return entry


_platform: FederationOhsPlatform | None = None


def get_federation_ohs_platform() -> FederationOhsPlatform:
    global _platform
    if _platform is None:
        _platform = FederationOhsPlatform()
    return _platform
