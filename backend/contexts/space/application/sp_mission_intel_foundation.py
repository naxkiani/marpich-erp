"""Space P218-J Mission Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/536-enterprise-space-intelligence-mission-intel.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MISSION_INTEL.md",
    "docs/architecture/space/MISSION_INTEL_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/MISSION_INTEL_LIFECYCLE.v1.yaml",
    "docs/architecture/space/MISSION_INTEL_DDD_CQRS.v1.yaml",
    "docs/architecture/space/MISSION_INTEL_SECURITY.v1.yaml",
    "docs/architecture/space/MISSION_INTEL_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_mission_intel.py",
    "backend/contexts/space/domain/aggregates/sp_mission_intel_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_mission_intel_acl.py",
    "backend/contexts/space/application/sp_mission_intel_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/mission_intelligence_platform",
    "backend/contexts/mission_planning_bc",
    "backend/contexts/mission_execution_bc",
)


def validate_sp_mission_intel_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_mission_intel_aggregates import (
        MissionAiRoot, MissionDigitalTwinRoot, MissionExecutionRoot,
        MissionGovernanceRoot, MissionIntelPlatformRoot, MissionLifecycleRoot,
        MissionPlanningRoot, MissionResourcesRoot, MissionSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_mission_intel as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-J" and cat["adr"] == 536 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_mission_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["mission_intelligence_platform_present_required"] is True
        and cat["mission_planning_platform_present_required"] is True
        and cat["mission_execution_platform_present_required"] is True
        and cat["mission_lifecycle_present_required"] is True
        and cat["mission_ai_present_required"] is True
        and cat["mission_resource_management_present_required"] is True
        and cat["mission_digital_twin_present_required"] is True
        and cat["mission_governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 15
        and cat["planning"]["domain_count"] == 10
        and cat["planning"]["service_count"] == 8
        and cat["execution"]["service_count"] == 8
        and cat["execution"]["mode_count"] == 6
        and cat["mission_ai"]["capability_count"] == 10
        and cat["mission_ai"]["model_count"] == 6
        and cat["resources"]["domain_count"] == 10
        and cat["resources"]["goal_count"] == 6
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 13
        and cat["never_replace_p218_a_mission"] is True
        and cat["never_replace_p218_i_navigation"] is True
        and cat["never_ungated_mission_launch_authorization"] is True
        and cat["never_skip_mission_readiness_review"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_k"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        MissionIntelPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        MissionPlanningRoot.enable(tenant_id="t1", planning_ref="p1").is_missing() is False,
        MissionExecutionRoot.enable(tenant_id="t1", execution_ref="e1").is_missing() is False,
        MissionLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        MissionAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        MissionResourcesRoot.enable(tenant_id="t1", resources_ref="r1").is_missing() is False,
        MissionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="d1").is_missing() is False,
        MissionGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        MissionSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_mission_intel_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_biotechnology", "to_robotics_supreme",
        "to_quantum_supreme", "to_master_ai", "to_integration", "to_policy_engine",
        "to_workflow", "to_audit", "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_a_mission", "never_replace_p218_i_navigation",
        "never_ungated_mission_launch_authorization", "never_skip_mission_readiness_review",
        "module_local_mission_intel_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/mission-intel")', "/mission-intel/vision",
        "/mission-intel/architecture", "/mission-intel/lifecycle", "/mission-intel/planning",
        "/mission-intel/execution", "/mission-intel/mission-ai", "/mission-intel/resources",
        "/mission-intel/digital-twin", "/mission-intel/observability", "/mission-intel/governance",
        "/mission-intel/security", "/mission-intel/integration", "/mission-intel/deployment",
        "/mission-intel/testing", "/mission-intel/cqrs", "/mission-intel/events",
        "/mission-intel/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MISSION_INTEL.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Mission Intelligence Platform is missing",
        "Never Mission Planning Platform is missing",
        "Never Mission Execution Platform is missing", "Never Mission Lifecycle is missing",
        "Never Mission AI is missing", "Never Mission Resource Management is missing",
        "Never Mission Digital Twin is missing", "Never DDD Model is missing",
        "Never Mission Governance is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-A Mission", "Never Replace P218-I Navigation",
        "Never Module-Local LLM", "Never Ungated Mission Launch Authorization",
        "Never Skip Mission Readiness Review",
        "unified enterprise platform capable of planning, executing, monitoring",
        "P218-J", "P218-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-J", "adr": 536, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
