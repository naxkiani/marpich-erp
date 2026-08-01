"""Robotics P216-A mission / vision / strategy foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/473-enterprise-robotics-mission.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_MISSION.md",
    "docs/architecture/robotics/ROBOTICS_MISSION_CAPABILITIES.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MISSION_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MISSION_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MISSION_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_mission.py",
    "backend/contexts/robotics/domain/aggregates/rb_mission_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_mission_acl.py",
    "backend/contexts/robotics/application/rb_mission_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/robotics_mission_platform",
    "backend/contexts/robotics_vision_platform",
    "backend/contexts/cyber_physical_strategy_platform",
)
def validate_rb_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_mission_aggregates import (
        RoboticsMissionRoot, RoboticsVisionRoot, StrategicScopeRoot, CapabilityMapRoot,
        OperatingModelRoot, EvolutionRoadmapRoot, GovernanceStrategyRoot,
        SecurityStrategyRoot, BusinessValueRoot,
    )
    from contexts.robotics.domain.services import rb_platform_mission as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-A" and cat["adr"] == 473 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_cyber_physical_strategic_intelligence_framework"
        and cat["foundation_gate"] == "P216" and cat["supreme_gate"] == "P215-Z"
        and cat["ai_gate"] == "P214-Z"
        and cat["robotics_mission_framework_present_required"] is True
        and cat["robotics_vision_framework_present_required"] is True
        and cat["strategic_cyber_physical_scope_present_required"] is True
        and cat["capability_map_present_required"] is True
        and cat["operating_model_present_required"] is True
        and cat["business_value_framework_present_required"] is True
        and cat["evolution_roadmap_present_required"] is True
        and cat["governance_strategy_present_required"] is True
        and cat["security_strategy_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["objectives"]["objective_count"] >= 5
        and cat["never_replace_p216_foundation"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_b"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        RoboticsMissionRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        RoboticsVisionRoot.enable(tenant_id="t1", vision_ref="v1").is_missing() is False,
        StrategicScopeRoot.enable(tenant_id="t1", scope_ref="s1").is_missing() is False,
        CapabilityMapRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        OperatingModelRoot.enable(tenant_id="t1", model_ref="o1").is_missing() is False,
        EvolutionRoadmapRoot.enable(tenant_id="t1", roadmap_ref="r1").is_missing() is False,
        GovernanceStrategyRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SecurityStrategyRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        BusinessValueRoot.enable(tenant_id="t1", value_ref="bv1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_mission_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p215_z", "via_p214_z", "via_p213", "via_policy_engine", "via_workflow",
        "via_audit", "via_identity", "via_core_platform", "never_replace_p216_foundation",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_robotics_mission_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/mission")', "/mission/vision", "/mission/objectives",
        "/mission/scope", "/mission/capabilities", "/mission/operating-model",
        "/mission/value", "/mission/roadmap", "/mission/governance",
        "/mission/security", "/mission/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_MISSION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Robotics Mission Framework is missing",
        "Never Robotics Vision Framework is missing",
        "Never Strategic Cyber-Physical Scope is missing",
        "Never Capability Map is missing",
        "Never Operating Model is missing",
        "Never Business Value Framework is missing",
        "Never Evolution Roadmap is missing",
        "Never Governance Strategy is missing",
        "Never Security Strategy is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Enterprise Robotics Platform SHALL",
        "Cyber-Physical Intelligence is the bridge",
        "P216", "P215-Z", "P214-Z", "P216-B",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-A", "adr": 473, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
