"""EIFTP Tactical Domain Model (P200-B4) — catalog + behavior gates."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/218-enterprise-identity-federation-trust-domain-model.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_DOMAIN_MODEL.md",
    "docs/architecture/identity/eiftp/MODEL_AGGREGATE_MAP.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_VALUE_OBJECTS.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_DOMAIN_EVENTS.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_COMMANDS.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_QUERIES.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_KG_TWIN.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_PERSISTENCE.v1.yaml",
    "docs/architecture/identity/eiftp/MODEL_ARCHITECTURE_VALIDATION.v1.yaml",
    "backend/contexts/identity_federation/domain/aggregates/ai_federated_agent.py",
    "backend/contexts/identity_federation/domain/events/federation_domain_events.py",
    "backend/contexts/identity_federation/domain/value_objects/federation_vos.py",
    "backend/contexts/identity_federation/domain/specifications/federation_specs.py",
    "backend/contexts/identity_federation/domain/factories/federation_factories.py",
    "backend/contexts/identity_federation/domain/policies/federation_policies.py",
    "backend/contexts/identity_federation/application/commands/establish_trust.py",
    "backend/contexts/identity_federation/application/commands/register_ai_identity.py",
    "backend/contexts/identity_federation/application/commands/terminate_session.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_domain_model_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    # Behavior smoke: TrustRelationship must expose grant/revoke
    from contexts.identity_federation.domain.aggregates.federation_platform import (
        FederationSession,
        TrustRelationship,
    )
    from contexts.identity_federation.domain.aggregates.ai_federated_agent import AiFederatedAgent

    behaviors_ok = all(
        hasattr(TrustRelationship, m) for m in ("grant", "revoke", "suspend", "reactivate", "rescore")
    ) and all(hasattr(FederationSession, m) for m in ("terminate", "elevate", "mark_expired"))
    ai_ok = hasattr(AiFederatedAgent, "register") and hasattr(AiFederatedAgent, "revoke")
    passed = not missing and not sibling and behaviors_ok and ai_ok
    return {
        "prompt": "P200-B4",
        "adr": 218,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "non_anemic_behaviors": behaviors_ok,
        "ai_identity_aggregate": ai_ok,
        "foundation_for": "P200-B5",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
