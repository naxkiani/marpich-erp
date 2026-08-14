"""Robotics P216 foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/472-enterprise-robotics-foundation.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_FOUNDATION.md",
    "docs/architecture/robotics/ROBOTICS_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_foundation.py",
    "backend/contexts/robotics/domain/aggregates/rb_foundation_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_foundation_acl.py",
    "backend/contexts/robotics/application/rb_foundation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/robotics_platform",
    "backend/contexts/physical_ai_platform",
    "backend/contexts/autonomous_machine_platform",
    "backend/contexts/robot_fleet_platform",
)
def validate_rb_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_foundation_aggregates import (
        RobotSystemRoot, AutonomousMachineRoot, PhysicalAIRoot, IndustrialIntelligenceRoot,
        RobotFleetRoot, HumanRobotCollaborationRoot, EdgeIntelligenceRoot,
        RoboticsDigitalTwinRoot, SafetyIntelligenceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_foundation as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216" and cat["adr"] == 472 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_cyber_physical_intelligence_fabric"
        and cat["enterprise_robotics_platform_present_required"] is True
        and cat["autonomous_machine_platform_present_required"] is True
        and cat["physical_ai_engine_present_required"] is True
        and cat["industrial_intelligence_platform_present_required"] is True
        and cat["robot_fleet_intelligence_present_required"] is True
        and cat["edge_intelligence_present_required"] is True
        and cat["human_robot_collaboration_present_required"] is True
        and cat["cyber_physical_security_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 10
        and cat["never_replace_core_platform"] is True
        and cat["never_replace_ai_platform"] is True
        and cat["never_replace_p215_z"] is True
        and cat["ungated_physical_autonomy_forbidden"] is True
        and cat["opaque_safety_decisions_forbidden"] is True
        and cat["autonomous_brain"]["module_local_llm_forbidden"] is True
        and cat["physical_ai"]["module_local_llm_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        RobotSystemRoot.enable(tenant_id="t1", robot_ref="r1").is_missing() is False,
        AutonomousMachineRoot.enable(tenant_id="t1", machine_ref="m1").is_missing() is False,
        PhysicalAIRoot.enable(tenant_id="t1", pai_ref="p1").is_missing() is False,
        IndustrialIntelligenceRoot.enable(tenant_id="t1", industrial_ref="i1").is_missing() is False,
        RobotFleetRoot.enable(tenant_id="t1", fleet_ref="f1").is_missing() is False,
        HumanRobotCollaborationRoot.enable(tenant_id="t1", hri_ref="h1").is_missing() is False,
        EdgeIntelligenceRoot.enable(tenant_id="t1", edge_ref="e1").is_missing() is False,
        RoboticsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SafetyIntelligenceRoot.enable(tenant_id="t1", safety_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_foundation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_z", "via_p214_z", "via_p213", "via_identity", "via_policy_engine", "via_workflow",
        "via_audit", "via_integration_platform", "via_search", "via_core_platform",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "module_local_llm_forbidden", "ungated_physical_autonomy_forbidden",
        "opaque_safety_decisions_forbidden", "iiot_via_integration_platform_only",
        "module_local_robotics_foundation_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/foundation")', "/foundation/autonomous", "/foundation/physical-ai",
        "/foundation/industrial", "/foundation/fleet", "/foundation/collaboration",
        "/foundation/edge", "/foundation/safety", "/foundation/knowledge-graph",
        "/foundation/digital-twin", "/foundation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_FOUNDATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Enterprise Robotics Platform is missing",
        "Never Autonomous Machine Platform is missing",
        "Never Physical AI Engine is missing",
        "Never Industrial Intelligence Platform is missing",
        "Never Robot Fleet Intelligence is missing",
        "Never Digital Twin Integration is missing",
        "Never Edge Intelligence is missing",
        "Never Human-Robot Collaboration is missing",
        "Never Cyber-Physical Security is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Robotics BC",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy",
        "Never Opaque Safety Decisions",
        "MEOS Cyber-Physical Intelligence Platform SHALL",
        "P215-Z", "P214-Z", "P213",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216", "adr": 472, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
