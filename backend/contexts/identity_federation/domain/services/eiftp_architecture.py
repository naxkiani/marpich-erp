"""EIFTP Enterprise Architecture (P200-B2) — catalog + structure gates."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/216-enterprise-identity-federation-trust-architecture.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_ARCHITECTURE.md",
    "docs/architecture/identity/eiftp/ARCH_DELIVERABLES_INDEX.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_SOLUTION.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_C4.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_DEPLOYMENT.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_FEDERATION.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_TRUST_FABRIC.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_CROSS_TENANT.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_EXTERNAL_IDP.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_FLOWS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_LIFECYCLES.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_SUBJECTS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_PLATFORM_INTEGRATIONS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_EVENTS_CQRS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_EDGE.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_DATA_PLANE.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_SECURITY.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_OBSERVABILITY.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_DEVSECOPS.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_REPO_STRUCTURE.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_DEFINITION_OF_DONE.v1.yaml",
    "docs/architecture/identity/eiftp/ARCH_IMPLEMENTATION_ROADMAP.v1.yaml",
    "backend/shared/application/ports/identity_federation.py",
    "backend/contexts/identity_federation/application/commands/evaluate_trust.py",
    "backend/contexts/identity_federation/application/queries/get_trust_facts.py",
    "backend/contexts/identity_federation/infrastructure/caching/federation_cache.py",
    "backend/contexts/identity_federation/infrastructure/messaging/outbox_publisher.py",
    "backend/contexts/identity_federation/infrastructure/adapters/federation_trust_facts_client.py",
    "backend/contexts/identity_federation/presentation/architecture_router.py",
]

DELIVERABLE_COUNT = 50
FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_architecture_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    passed = not missing and not sibling
    return {
        "prompt": "P200-B2",
        "adr": 216,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "deliverable_count": DELIVERABLE_COUNT,
        "foundation_for": "P200-B3",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
