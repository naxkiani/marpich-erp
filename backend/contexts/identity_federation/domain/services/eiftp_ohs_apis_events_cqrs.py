"""EIFTP OHS APIs / Events / CQRS (P200-B10) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/224-enterprise-identity-federation-apis-events-cqrs.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_APIS_EVENTS_CQRS.md",
    "docs/architecture/identity/eiftp/OHS_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/OHS_EVENT_CATALOG.v1.yaml",
    "docs/architecture/identity/eiftp/OHS_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/application/cqrs/federation_buses.py",
    "backend/contexts/identity_federation/domain/services/federation_ohs_platform.py",
    "backend/contexts/identity_federation/domain/services/federation_saga_engine.py",
    "backend/contexts/identity_federation/infrastructure/messaging/outbox_inbox_store.py",
    "backend/contexts/identity_federation/application/commands/ohs_commands.py",
    "backend/contexts/identity_federation/application/queries/ohs_queries.py",
    "backend/contexts/identity_federation/presentation/ohs_router.py",
    "backend/shared/contracts/graphql/federation.graphql",
    "backend/shared/contracts/grpc/federation/v1/federation.proto",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_ohs_apis_events_cqrs_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    gql = (root / "backend/shared/contracts/graphql/federation.graphql").read_text(
        encoding="utf-8"
    )
    proto = (root / "backend/shared/contracts/grpc/federation/v1/federation.proto").read_text(
        encoding="utf-8"
    )
    gql_ok = "EvaluateZeroTrust" in gql and "GetSecurityPosture" in gql
    grpc_ok = "EvaluateZeroTrust" in proto and "GetSecurityPosture" in proto
    from contexts.identity_federation.application.cqrs.federation_buses import (
        FederationCommandBus,
        FederationQueryBus,
    )
    from contexts.identity_federation.domain.services.federation_saga_engine import (
        FederationSagaEngine,
    )
    from contexts.identity_federation.infrastructure.messaging.outbox_inbox_store import (
        FederationOutboxInboxStore,
    )

    bus_ok = hasattr(FederationCommandBus, "dispatch") and hasattr(
        FederationQueryBus, "dispatch"
    )
    saga_ok = "federation_trust_establishment" in FederationSagaEngine.SAGA_TYPES
    patterns_ok = hasattr(FederationOutboxInboxStore, "enqueue_outbox") and hasattr(
        FederationOutboxInboxStore, "ingest_inbox"
    )
    passed = (
        not missing
        and not sibling
        and gql_ok
        and grpc_ok
        and bus_ok
        and saga_ok
        and patterns_ok
    )
    return {
        "prompt": "P200-B10",
        "adr": 224,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "graphql_ohs_extended": gql_ok,
        "grpc_ohs_extended": grpc_ok,
        "cqrs_buses": bus_ok,
        "saga_engine": saga_ok,
        "outbox_inbox": patterns_ok,
        "foundation_for": "P200-B11",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
