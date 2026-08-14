"""Space P218-M Manufacturing Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/539-enterprise-space-intelligence-manufacturing.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MANUFACTURING.md",
    "docs/architecture/space/MANUFACTURING_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/MANUFACTURING_LIFECYCLE.v1.yaml",
    "docs/architecture/space/MANUFACTURING_DDD_CQRS.v1.yaml",
    "docs/architecture/space/MANUFACTURING_SECURITY.v1.yaml",
    "docs/architecture/space/MANUFACTURING_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_manufacturing.py",
    "backend/contexts/space/domain/aggregates/sp_manufacturing_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_manufacturing_acl.py",
    "backend/contexts/space/application/sp_manufacturing_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_manufacturing_platform",
    "backend/contexts/orbital_factory_bc",
    "backend/contexts/in_orbit_manufacturing_bc",
)


def validate_sp_manufacturing_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_manufacturing_aggregates import (
        AutonomousProductionRoot, IndustrialSystemsRoot, InOrbitManufacturingRoot,
        ManufacturingAiRoot, ManufacturingDigitalTwinRoot, ManufacturingKnowledgeGraphRoot,
        ManufacturingPlatformRoot, ManufacturingRoboticsRoot, ManufacturingSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_manufacturing as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-M" and cat["adr"] == 539 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_manufacturing_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_manufacturing_platform_present_required"] is True
        and cat["in_orbit_manufacturing_present_required"] is True
        and cat["orbital_industrial_systems_present_required"] is True
        and cat["autonomous_production_present_required"] is True
        and cat["manufacturing_ai_present_required"] is True
        and cat["space_robotics_integration_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["industrial_knowledge_graph_present_required"] is True
        and cat["security_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["in_orbit"]["capability_count"] == 8
        and cat["in_orbit"]["category_count"] == 8
        and cat["industrial"]["infrastructure_count"] == 7
        and cat["industrial"]["capability_count"] == 7
        and cat["autonomy"]["function_count"] == 8
        and cat["autonomy"]["agent_count"] == 8
        and cat["manufacturing_ai"]["capability_count"] == 10
        and cat["manufacturing_ai"]["model_count"] == 6
        and cat["materials"]["domain_count"] == 7
        and cat["robotics"]["system_count"] == 7
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 6
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_l_exploration"] is True
        and cat["never_ungated_autonomous_factory_production"] is True
        and cat["never_skip_quality_validation"] is True
        and cat["never_skip_industrial_safety_certification"] is True
        and cat["never_violate_circular_space_economy_principles"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_n"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ManufacturingPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        InOrbitManufacturingRoot.enable(tenant_id="t1", in_orbit_ref="io1").is_missing() is False,
        IndustrialSystemsRoot.enable(tenant_id="t1", industrial_ref="i1").is_missing() is False,
        AutonomousProductionRoot.enable(tenant_id="t1", autonomy_ref="a1").is_missing() is False,
        ManufacturingAiRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        ManufacturingRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        ManufacturingDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ManufacturingKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        ManufacturingSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_manufacturing_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme",
        "to_master_ai", "to_integration", "to_policy_engine", "to_workflow", "to_audit",
        "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_l_exploration", "never_ungated_autonomous_factory_production",
        "never_skip_quality_validation", "never_skip_industrial_safety_certification",
        "never_violate_circular_space_economy_principles", "module_local_manufacturing_forbidden",
        "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/manufacturing")', "/manufacturing/vision",
        "/manufacturing/architecture", "/manufacturing/lifecycle", "/manufacturing/in-orbit",
        "/manufacturing/industrial", "/manufacturing/autonomy", "/manufacturing/manufacturing-ai",
        "/manufacturing/materials", "/manufacturing/robotics", "/manufacturing/digital-twin",
        "/manufacturing/knowledge-graph", "/manufacturing/observability", "/manufacturing/governance",
        "/manufacturing/security", "/manufacturing/integration", "/manufacturing/deployment",
        "/manufacturing/testing", "/manufacturing/cqrs", "/manufacturing/events",
        "/manufacturing/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MANUFACTURING.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Manufacturing Platform is missing",
        "Never In-Orbit Manufacturing is missing",
        "Never Orbital Industrial Systems is missing",
        "Never Autonomous Production is missing",
        "Never Manufacturing AI is missing",
        "Never Space Robotics Integration is missing",
        "Never Digital Twin is missing", "Never Industrial Knowledge Graph is missing",
        "Never Security is missing", "Never DDD Model is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-L Exploration",
        "Never Module-Local LLM", "Never Ungated Autonomous Factory Production",
        "Never Skip Quality Validation", "Never Skip Industrial Safety Certification",
        "Never Violate Circular Space Economy Principles",
        "autonomous space industrial ecosystem",
        "P218-M", "P218-N",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-M", "adr": 539, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
