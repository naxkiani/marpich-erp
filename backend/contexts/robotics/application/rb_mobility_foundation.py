"""Robotics P216-H autonomous mobility / connected vehicles / drones foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/480-enterprise-robotics-mobility.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_MOBILITY.md",
    "docs/architecture/robotics/ROBOTICS_MOBILITY_VEHICLE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MOBILITY_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MOBILITY_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MOBILITY_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_MOBILITY_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_mobility.py",
    "backend/contexts/robotics/domain/aggregates/rb_mobility_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_mobility_acl.py",
    "backend/contexts/robotics/application/rb_mobility_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/autonomous_mobility_platform",
    "backend/contexts/connected_vehicle_platform",
    "backend/contexts/drone_intelligence_platform",
    "backend/contexts/smart_transportation_platform",
)
def validate_rb_mobility_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_mobility_aggregates import (
        ConnectedVehicleRoot, AutonomousNavigationRoot, DroneIntelligenceRoot,
        FleetMobilityRoot, SmartTransportationRoot, MobilityDigitalTwinRoot,
        TransportationKnowledgeGraphRoot, MobilitySecurityRoot, MobilityObservabilityRoot,
    )
    from contexts.robotics.domain.services import rb_platform_mobility as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-H" and cat["adr"] == 480 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_autonomous_mobility_fabric"
        and cat["foundation_gate"] == "P216" and cat["logistics_gate"] == "P216-G"
        and cat["industrial_gate"] == "P216-F" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["connected_vehicle_platform_present_required"] is True
        and cat["autonomous_navigation_platform_present_required"] is True
        and cat["drone_intelligence_platform_present_required"] is True
        and cat["fleet_mobility_platform_present_required"] is True
        and cat["smart_transportation_platform_present_required"] is True
        and cat["mobility_digital_twin_present_required"] is True
        and cat["transportation_knowledge_graph_present_required"] is True
        and cat["observability_platform_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["domain_model"]["entity_count"] == 13
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_g_logistics"] is True
        and cat["never_direct_v2x_bypass"] is True
        and cat["v2x_via_integration_platform_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_i"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ConnectedVehicleRoot.enable(tenant_id="t1", vehicle_ref="v1").is_missing() is False,
        AutonomousNavigationRoot.enable(tenant_id="t1", navigation_ref="n1").is_missing() is False,
        DroneIntelligenceRoot.enable(tenant_id="t1", drone_ref="d1").is_missing() is False,
        FleetMobilityRoot.enable(tenant_id="t1", fleet_ref="f1").is_missing() is False,
        SmartTransportationRoot.enable(tenant_id="t1", transportation_ref="tr1").is_missing() is False,
        MobilityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        TransportationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        MobilitySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        MobilityObservabilityRoot.enable(tenant_id="t1", observability_ref="o1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_mobility_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_g_logistics",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_v2x_bypass", "v2x_via_integration_platform_only",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_mobility_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/mobility")', "/mobility/vision", "/mobility/domain",
        "/mobility/bounded-contexts", "/mobility/connected-vehicle", "/mobility/navigation",
        "/mobility/drones", "/mobility/fleet", "/mobility/transportation",
        "/mobility/digital-twin", "/mobility/knowledge-graph", "/mobility/observability",
        "/mobility/security", "/mobility/cqrs", "/mobility/events", "/mobility/microservices",
        "/mobility/integration", "/mobility/deployment", "/mobility/testing",
        "/mobility/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_MOBILITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Connected Vehicle Platform is missing",
        "Never Autonomous Navigation Platform is missing",
        "Never Drone Intelligence Platform is missing",
        "Never Fleet Mobility Platform is missing",
        "Never Smart Transportation Platform is missing",
        "Never Mobility Digital Twin is missing",
        "Never Transportation Knowledge Graph is missing",
        "Never Observability Platform is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Mobility Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-G Logistics",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Direct V2X Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Autonomous Mobility Platform SHALL coordinate",
        "P216", "P216-G", "P215-Z", "P214-Z", "P216-I",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-H", "adr": 480, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
