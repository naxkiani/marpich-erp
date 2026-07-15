"""EILMP P201-A Registration & Onboarding foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/227-enterprise-identity-lifecycle-management-platform.md",
    "docs/architecture/ENTERPRISE_IDENTITY_LIFECYCLE_MANAGEMENT_PLATFORM.md",
    "docs/architecture/identity/eilmp/README.md",
    "docs/architecture/identity/eilmp/P201_MASTER_SERIES_ROADMAP.v1.yaml",
    "docs/architecture/identity/eilmp/REGISTRATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eilmp/IDENTITY_TYPES.v1.yaml",
    "docs/architecture/identity/eilmp/ONBOARDING_WORKFLOW.v1.yaml",
    "docs/architecture/identity/eilmp/EVENT_CATALOG.v1.yaml",
    "docs/architecture/identity/eilmp/CQRS_SURFACE.v1.yaml",
    "docs/architecture/identity/eilmp/BOUNDARIES.v1.yaml",
    "docs/architecture/identity/eilmp/CAPABILITY_MAP.v1.yaml",
    "docs/architecture/identity/eilmp/DEFINITION_OF_DONE.v1.yaml",
    "backend/contexts/identity_lifecycle/domain/aggregates/registration_onboarding.py",
    "backend/contexts/identity_lifecycle/domain/services/registration_onboarding_engine.py",
    "backend/contexts/identity_lifecycle/application/registration_service.py",
    "backend/contexts/identity_lifecycle/presentation/registration_router.py",
    "backend/shared/application/ports/identity_lifecycle.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eilmp"


def validate_registration_onboarding_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()

    from contexts.identity_lifecycle.domain.aggregates.registration_onboarding import (
        SUPPORTED_IDENTITY_TYPES,
    )
    from contexts.identity_lifecycle.domain.services.registration_onboarding_engine import (
        catalog,
        evaluate_zero_trust,
    )

    types_ok = len(SUPPORTED_IDENTITY_TYPES) >= 15
    cat = catalog()
    zt = evaluate_zero_trust({"risk_score": 90, "device_trusted": True})
    zt_blocks = zt["passed"] is False
    registry_text = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = (
        'id="identity_lifecycle"' in registry_text
        and "IDENTITY_LIFECYCLE" in registry_text
    )
    router = (
        root / "backend/contexts/identity_lifecycle/presentation/registration_router.py"
    ).read_text(encoding="utf-8")
    router_ok = "/registration/register" in router and "/eilmp/surface" in router
    port = (
        root / "backend/shared/application/ports/identity_lifecycle.py"
    ).read_text(encoding="utf-8")
    port_ok = "IIdentityLifecycleStatus" in port

    passed = (
        not missing
        and not sibling
        and types_ok
        and zt_blocks
        and registry_ok
        and router_ok
        and port_ok
        and "employee" in cat["identity_types"]
    )
    return {
        "prompt": "P201-A",
        "adr": 227,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "identity_types": types_ok,
        "zero_trust_gate": zt_blocks,
        "registry": registry_ok,
        "registration_router": router_ok,
        "shared_port": port_ok,
        "sor": "identity_lifecycle",
        "foundation_for": "P201-A2",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
