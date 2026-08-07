"""Space P218-L Exploration Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/538-enterprise-space-intelligence-exploration.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_EXPLORATION.md",
    "docs/architecture/space/EXPLORATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/EXPLORATION_LIFECYCLE.v1.yaml",
    "docs/architecture/space/EXPLORATION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/EXPLORATION_SECURITY.v1.yaml",
    "docs/architecture/space/EXPLORATION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_exploration.py",
    "backend/contexts/space/domain/aggregates/sp_exploration_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_exploration_acl.py",
    "backend/contexts/space/application/sp_exploration_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_exploration_platform",
    "backend/contexts/lunar_operations_bc",
    "backend/contexts/mars_operations_bc",
)


def validate_sp_exploration_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_exploration_aggregates import (
        AutonomyRoot, DeepSpaceRoot, ExplorationAiRoot, ExplorationDigitalTwinRoot,
        ExplorationGovernanceRoot, ExplorationPlatformRoot, ExplorationSecurityRoot,
        LunarOperationsRoot, MarsOperationsRoot,
    )
    from contexts.space.domain.services import sp_platform_exploration as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-L" and cat["adr"] == 538 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_exploration_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_exploration_platform_present_required"] is True
        and cat["lunar_operations_platform_present_required"] is True
        and cat["mars_operations_platform_present_required"] is True
        and cat["deep_space_exploration_platform_present_required"] is True
        and cat["exploration_ai_present_required"] is True
        and cat["autonomous_exploration_present_required"] is True
        and cat["exploration_digital_twin_present_required"] is True
        and cat["governance_and_safety_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["lunar"]["capability_count"] == 10
        and cat["lunar"]["zone_count"] == 7
        and cat["mars"]["capability_count"] == 10
        and cat["mars"]["mission_type_count"] == 6
        and cat["deep_space"]["destination_count"] == 6
        and cat["deep_space"]["capability_count"] == 8
        and cat["exploration_ai"]["capability_count"] == 10
        and cat["exploration_ai"]["model_count"] == 6
        and cat["autonomy"]["function_count"] == 8
        and cat["autonomy"]["agent_count"] == 8
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_k_scientific"] is True
        and cat["never_ungated_planetary_landing_authorization"] is True
        and cat["never_skip_planetary_protection_compliance"] is True
        and cat["never_ungated_surface_hazard_response"] is True
        and cat["never_skip_crew_safety_validation"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_m"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ExplorationPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        LunarOperationsRoot.enable(tenant_id="t1", lunar_ref="l1").is_missing() is False,
        MarsOperationsRoot.enable(tenant_id="t1", mars_ref="m1").is_missing() is False,
        DeepSpaceRoot.enable(tenant_id="t1", deep_space_ref="d1").is_missing() is False,
        ExplorationAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        AutonomyRoot.enable(tenant_id="t1", autonomy_ref="au1").is_missing() is False,
        ExplorationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ExplorationGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        ExplorationSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_exploration_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_policy_engine", "to_workflow", "to_audit", "to_identity",
        "to_core_platform", "to_enterprise_space", "never_replace_p218_k_scientific",
        "never_ungated_planetary_landing_authorization", "never_skip_planetary_protection_compliance",
        "never_ungated_surface_hazard_response", "never_skip_crew_safety_validation",
        "module_local_exploration_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/exploration")', "/exploration/vision",
        "/exploration/architecture", "/exploration/lifecycle", "/exploration/lunar",
        "/exploration/mars", "/exploration/deep-space", "/exploration/exploration-ai",
        "/exploration/autonomy", "/exploration/digital-twin", "/exploration/observability",
        "/exploration/governance", "/exploration/security", "/exploration/integration",
        "/exploration/deployment", "/exploration/testing", "/exploration/cqrs",
        "/exploration/events", "/exploration/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_EXPLORATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Exploration Platform is missing",
        "Never Lunar Operations Platform is missing",
        "Never Mars Operations Platform is missing",
        "Never Deep Space Exploration Platform is missing",
        "Never Exploration AI Platform is missing",
        "Never Autonomous Exploration is missing",
        "Never Exploration Digital Twin is missing", "Never DDD Model is missing",
        "Never Governance & Safety is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-K Scientific",
        "Never Module-Local LLM", "Never Skip Planetary Protection Compliance",
        "Never Ungated Planetary Landing Authorization",
        "Never Ungated Surface Hazard Response", "Never Skip Crew Safety Validation",
        "autonomous, resilient and continuously learning",
        "P218-L", "P218-M",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-L", "adr": 538, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
