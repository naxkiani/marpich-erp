"""Space P218-O Logistics Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/541-enterprise-space-intelligence-logistics.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_LOGISTICS.md",
    "docs/architecture/space/LOGISTICS_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/LOGISTICS_LIFECYCLE.v1.yaml",
    "docs/architecture/space/LOGISTICS_DDD_CQRS.v1.yaml",
    "docs/architecture/space/LOGISTICS_SECURITY.v1.yaml",
    "docs/architecture/space/LOGISTICS_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_logistics.py",
    "backend/contexts/space/domain/aggregates/sp_logistics_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_logistics_acl.py",
    "backend/contexts/space/application/sp_logistics_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_logistics_platform",
    "backend/contexts/orbital_supply_chain_bc",
    "backend/contexts/autonomous_cargo_bc",
)


def validate_sp_logistics_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_logistics_aggregates import (
        AutonomousCargoRoot, InterplanetaryTransportRoot, LogisticsAiRoot,
        LogisticsDigitalTwinRoot, LogisticsKnowledgeGraphRoot, LogisticsPlatformRoot,
        LogisticsRoboticsRoot, LogisticsSecurityRoot, SupplyChainRoot,
    )
    from contexts.space.domain.services import sp_platform_logistics as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-O" and cat["adr"] == 541 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_logistics_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L" and cat["manufacturing_gate"] == "P218-M"
        and cat["resources_gate"] == "P218-N"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_logistics_platform_present_required"] is True
        and cat["autonomous_cargo_systems_present_required"] is True
        and cat["orbital_supply_chain_present_required"] is True
        and cat["interplanetary_transportation_present_required"] is True
        and cat["logistics_ai_present_required"] is True
        and cat["robotics_integration_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["cargo"]["capability_count"] == 8
        and cat["cargo"]["cargo_type_count"] == 9
        and cat["supply_chain"]["domain_count"] == 6
        and cat["supply_chain"]["capability_count"] == 12
        and cat["interplanetary"]["domain_count"] == 5
        and cat["interplanetary"]["capability_count"] == 12
        and cat["logistics_ai"]["capability_count"] == 8
        and cat["logistics_ai"]["model_count"] == 6
        and cat["robotics"]["system_count"] == 6
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 6
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_n_resources"] is True
        and cat["never_ungated_cargo_launch_authorization"] is True
        and cat["never_skip_cargo_authentication"] is True
        and cat["never_skip_supply_chain_security_controls"] is True
        and cat["never_ungated_emergency_route_activation"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_p"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        LogisticsPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        AutonomousCargoRoot.enable(tenant_id="t1", cargo_ref="c1").is_missing() is False,
        SupplyChainRoot.enable(tenant_id="t1", supply_chain_ref="s1").is_missing() is False,
        InterplanetaryTransportRoot.enable(tenant_id="t1", interplanetary_ref="i1").is_missing() is False,
        LogisticsAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        LogisticsRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        LogisticsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        LogisticsKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        LogisticsSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_logistics_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_biotechnology",
        "to_robotics_supreme", "to_quantum_supreme", "to_master_ai", "to_integration",
        "to_policy_engine", "to_workflow", "to_audit", "to_identity", "to_core_platform",
        "to_enterprise_space", "never_replace_p218_n_resources",
        "never_ungated_cargo_launch_authorization", "never_skip_cargo_authentication",
        "never_skip_supply_chain_security_controls", "never_ungated_emergency_route_activation",
        "module_local_logistics_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/logistics")', "/logistics/vision",
        "/logistics/architecture", "/logistics/lifecycle", "/logistics/cargo",
        "/logistics/supply-chain", "/logistics/interplanetary", "/logistics/logistics-ai",
        "/logistics/robotics", "/logistics/digital-twin", "/logistics/knowledge-graph",
        "/logistics/observability", "/logistics/governance", "/logistics/security",
        "/logistics/integration", "/logistics/deployment", "/logistics/testing",
        "/logistics/cqrs", "/logistics/events", "/logistics/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_LOGISTICS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Logistics Platform is missing",
        "Never Autonomous Cargo Systems is missing",
        "Never Orbital Supply Chain is missing",
        "Never Interplanetary Transportation is missing",
        "Never Logistics AI is missing",
        "Never Robotics Integration is missing",
        "Never Digital Twin is missing", "Never Knowledge Graph is missing",
        "Never Governance is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-N Resources",
        "Never Module-Local LLM", "Never Ungated Cargo Launch Authorization",
        "Never Skip Cargo Authentication", "Never Skip Supply Chain Security Controls",
        "Never Ungated Emergency Route Activation",
        "autonomous logistics intelligence ecosystem",
        "P218-O", "P218-P",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-O", "adr": 541, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
