"""EILMP P201-A1 Series Foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/227-enterprise-identity-lifecycle-management-platform.md",
    "docs/architecture/ENTERPRISE_IDENTITY_LIFECYCLE_MANAGEMENT_PLATFORM.md",
    "docs/architecture/identity/eilmp/README.md",
    "docs/architecture/identity/eilmp/P201_MASTER_SERIES_ROADMAP.v1.yaml",
    "docs/architecture/identity/eilmp/ARCH_EILMP.v1.yaml",
    "docs/architecture/identity/eilmp/IDENTITY_TYPES.v1.yaml",
    "docs/architecture/identity/eilmp/STATE_MACHINE.v1.yaml",
    "docs/architecture/identity/eilmp/JML_WORKFLOWS.v1.yaml",
    "docs/architecture/identity/eilmp/EVENT_CATALOG.v1.yaml",
    "docs/architecture/identity/eilmp/CQRS_SURFACE.v1.yaml",
    "docs/architecture/identity/eilmp/CAPABILITY_MAP.v1.yaml",
    "docs/architecture/identity/eilmp/BOUNDARIES.v1.yaml",
    "docs/architecture/identity/eilmp/DEFINITION_OF_DONE.v1.yaml",
    "backend/contexts/identity_lifecycle/domain/aggregates/identity_lifecycle_platform.py",
    "backend/contexts/identity_lifecycle/domain/services/lifecycle_workflow_engine.py",
    "backend/contexts/identity_lifecycle/domain/services/eilmp_foundation.py",
    "backend/shared/application/ports/identity_lifecycle.py",
    "backend/contexts/identity_lifecycle/presentation/router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eilmp"

JML_ACTIONS = {
    "joiner",
    "mover",
    "leaver",
    "transfer",
    "role_change",
    "rehire",
    "place_under_investigation",
}


def validate_eilmp_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()

    from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
        STATE_ALIASES,
        LifecycleAction,
        LifecycleState,
    )
    from contexts.identity_lifecycle.domain.services import lifecycle_workflow_engine as workflow

    jml_ok = JML_ACTIONS.issubset({a.value for a in LifecycleAction})
    under_inv = LifecycleState.UNDER_INVESTIGATION.value in {s.value for s in LifecycleState}
    aliases_ok = all(
        k in STATE_ALIASES
        for k in (
            "requested",
            "pending_validation",
            "approved",
            "provisioned",
            "operational",
        )
    )
    jml_list = {a["action"] for a in workflow.list_jml_actions()}
    jml_engine_ok = JML_ACTIONS.issubset(jml_list)
    can_joiner = workflow.can_transition("verified", "joiner")
    can_leaver = workflow.can_transition("active", "leaver")

    registry_text = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = (
        'id="identity_lifecycle"' in registry_text and "IDENTITY_LIFECYCLE" in registry_text
    )
    router = (
        root / "backend/contexts/identity_lifecycle/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        "/state-machine" in router
        and "/jml/" in router
        and "/eilmp/surface" in router
    )
    port = (
        root / "backend/shared/application/ports/identity_lifecycle.py"
    ).read_text(encoding="utf-8")
    port_ok = "IIdentityLifecycleStatus" in port
    metrics = (
        root / "docs/architecture/observability/METRICS_CATALOG.yaml"
    ).read_text(encoding="utf-8")
    metrics_ok = "identity_lifecycle_metrics" in metrics

    passed = (
        not missing
        and not sibling
        and jml_ok
        and under_inv
        and aliases_ok
        and jml_engine_ok
        and can_joiner
        and can_leaver
        and registry_ok
        and router_ok
        and port_ok
        and metrics_ok
    )
    return {
        "prompt": "P201-A1",
        "adr": 227,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "jml_actions": jml_ok and jml_engine_ok,
        "state_aliases": aliases_ok,
        "under_investigation_state": under_inv,
        "joiner_transition": can_joiner,
        "leaver_transition": can_leaver,
        "registry": registry_ok,
        "router_surface": router_ok,
        "shared_port": port_ok,
        "metrics_catalog": metrics_ok,
        "sor": "identity_lifecycle",
        "foundation_for": "P201-A2",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
