"""EIFTP Federation Engine (P200-B5) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/219-enterprise-identity-federation-engine.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_ENGINE.md",
    "docs/architecture/identity/eiftp/ENGINE_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/ENGINE_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/domain/services/identity_federation_engine.py",
    "backend/contexts/identity_federation/domain/ports/provider_health.py",
    "backend/contexts/identity_federation/infrastructure/adapters/provider_health_adapter.py",
    "backend/contexts/identity_federation/application/commands/register_identity_provider.py",
    "backend/contexts/identity_federation/application/commands/connect_federation_provider.py",
    "backend/contexts/identity_federation/application/commands/federation_engine_commands.py",
    "backend/contexts/identity_federation/application/queries/federation_engine_queries.py",
    "backend/contexts/identity_federation/presentation/engine_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_federation_engine_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    from contexts.identity_federation.domain.aggregates.federation_platform import (
        FederationConnection,
        IdentityProvider,
    )
    from contexts.identity_federation.domain.services.identity_federation_engine import (
        IdentityFederationEngine,
    )

    connection_ok = hasattr(IdentityProvider, "connect_federation") and hasattr(
        FederationConnection, "to_dict"
    )
    facade_ok = all(
        hasattr(IdentityFederationEngine, m)
        for m in ("exchange_token", "transform_claims", "resolve_identity_conflict", "negotiate_protocol")
    )
    passed = not missing and not sibling and connection_ok and facade_ok
    return {
        "prompt": "P200-B5",
        "adr": 219,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "federation_connection": connection_ok,
        "engine_facade": facade_ok,
        "foundation_for": "P200-B6",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
