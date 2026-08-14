"""Robotics P216-D EROS / runtime / fleet control foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/476-enterprise-robotics-operating-system.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_RUNTIME.md",
    "docs/architecture/robotics/ROBOTICS_RUNTIME_OS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RUNTIME_FLEET.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RUNTIME_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RUNTIME_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RUNTIME_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_runtime.py",
    "backend/contexts/robotics/domain/aggregates/rb_runtime_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_runtime_acl.py",
    "backend/contexts/robotics/application/rb_runtime_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/robotics_runtime_platform",
    "backend/contexts/robotics_os_platform",
    "backend/contexts/fleet_control_plane_platform",
)
def validate_rb_runtime_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_runtime_aggregates import (
        ErosOsRoot, RobotRuntimeRoot, FleetControlPlaneRoot, AutonomousInfraRoot,
        EdgePlatformRoot, MissionRuntimeRoot, DeviceManagementRoot,
        RuntimeSecurityRoot, SelfHealingRoot,
    )
    from contexts.robotics.domain.services import rb_platform_runtime as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-D" and cat["adr"] == 476 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_robotics_operating_fabric"
        and cat["foundation_gate"] == "P216" and cat["mission_gate"] == "P216-A"
        and cat["strategy_gate"] == "P216-B" and cat["domain_gate"] == "P216-C"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["robotics_os_architecture_present_required"] is True
        and cat["robot_runtime_platform_present_required"] is True
        and cat["fleet_control_plane_present_required"] is True
        and cat["autonomous_machine_infrastructure_present_required"] is True
        and cat["edge_robotics_platform_present_required"] is True
        and cat["device_management_present_required"] is True
        and cat["mission_execution_engine_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["observability_architecture_present_required"] is True
        and cat["self_healing_capability_present_required"] is True
        and cat["os_architecture"]["layer_count"] == 6
        and cat["runtime_platform"]["component_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_c_domain"] is True
        and cat["never_direct_hardware_bypass_of_hal"] is True
        and cat["module_local_observability_store_forbidden"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_e"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ErosOsRoot.enable(tenant_id="t1", os_ref="o1").is_missing() is False,
        RobotRuntimeRoot.enable(tenant_id="t1", runtime_ref="r1").is_missing() is False,
        FleetControlPlaneRoot.enable(tenant_id="t1", fleet_ref="f1").is_missing() is False,
        AutonomousInfraRoot.enable(tenant_id="t1", infra_ref="i1").is_missing() is False,
        EdgePlatformRoot.enable(tenant_id="t1", edge_ref="e1").is_missing() is False,
        MissionRuntimeRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        DeviceManagementRoot.enable(tenant_id="t1", device_ref="d1").is_missing() is False,
        RuntimeSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        SelfHealingRoot.enable(tenant_id="t1", recovery_ref="rec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_runtime_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p215_z", "via_p214_z", "via_p213",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_observability_platform",
        "via_core_platform", "never_replace_p216_foundation", "never_replace_p216_a_mission",
        "never_replace_p216_b_strategy", "never_replace_p216_c_domain", "never_replace_p215_z",
        "never_replace_ai_platform", "never_replace_core_platform",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_robotics_runtime_forbidden", "never_direct_hardware_bypass_of_hal",
        "module_local_observability_store_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/runtime")', "/runtime/os", "/runtime/stack",
        "/runtime/platform", "/runtime/fleet", "/runtime/infrastructure",
        "/runtime/communication", "/runtime/missions", "/runtime/devices",
        "/runtime/edge", "/runtime/observability", "/runtime/security",
        "/runtime/self-healing", "/runtime/cqrs", "/runtime/events",
        "/runtime/microservices", "/runtime/deployment", "/runtime/testing",
        "/runtime/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_RUNTIME.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Robotics OS Architecture is missing",
        "Never Robot Runtime Platform is missing",
        "Never Fleet Control Plane is missing",
        "Never Autonomous Machine Infrastructure is missing",
        "Never Edge Robotics Platform is missing",
        "Never Device Management is missing",
        "Never Mission Execution Engine is missing",
        "Never Communication Framework is missing",
        "Never Security Architecture is missing",
        "Never Observability Architecture is missing",
        "Never Self-Healing Capability is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment Model is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-A Mission",
        "Never Replace P216-B Strategy",
        "Never Replace P216-C Domain",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Module-Local Observability Store",
        "Never Direct Hardware Bypass of HAL",
        "EROS SHALL become the operating intelligence layer",
        "P216", "P216-A", "P216-B", "P216-C", "P215-Z", "P214-Z", "P216-E",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-D", "adr": 476, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
