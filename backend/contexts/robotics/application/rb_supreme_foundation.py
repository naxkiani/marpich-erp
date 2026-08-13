"""Robotics P216-Z supreme control plane / intelligence nexus foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/498-enterprise-robotics-supreme.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_SUPREME.md",
    "docs/architecture/robotics/ROBOTICS_SUPREME_HOME.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SUPREME_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SUPREME_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SUPREME_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SUPREME_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_supreme.py",
    "backend/contexts/robotics/domain/aggregates/rb_supreme_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_supreme_acl.py",
    "backend/contexts/robotics/application/rb_supreme_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/ultimate_robotics_intelligence_platform",
    "backend/contexts/robotics_supreme_control_plane_platform",
    "backend/contexts/autonomous_robotics_civilization_platform",
    "backend/contexts/universal_robotics_intelligence_network_platform",
)
def validate_rb_supreme_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_supreme_aggregates import (
        SupremeControlPlaneRoot, UniversalRoboticsNetworkRoot, RoboticsCivilizationRoot,
        CollectiveIntelligenceRoot, UniversalDigitalTwinRoot, KnowledgeGraphUniverseRoot,
        AutonomousGovernanceRoot, SupremeSecurityRoot, HumanAuthorityRoot,
    )
    from contexts.robotics.domain.services import rb_platform_supreme as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-Z" and cat["adr"] == 498 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_robotics_supreme_intelligence_nexus"
        and cat["foundation_gate"] == "P216" and cat["ultimate_gate"] == "P216-Y"
        and cat["entertainment_gate"] == "P216-X"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["ultimate_robotics_intelligence_architecture_present_required"] is True
        and cat["meos_robotics_supreme_control_plane_present_required"] is True
        and cat["autonomous_robotics_civilization_layer_present_required"] is True
        and cat["universal_robotics_network_present_required"] is True
        and cat["collective_intelligence_engine_present_required"] is True
        and cat["robotics_digital_twin_universe_present_required"] is True
        and cat["robotics_knowledge_graph_present_required"] is True
        and cat["autonomous_governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["human_authority_framework_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_y_ultimate"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_authority_framework_required"] is True
        and cat["safety_by_design_required"] is True
        and cat["human_override_authority_required"] is True
        and cat["explainable_autonomous_systems_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["completes_p216_master_series"] is True
        and cat["foundation_for_p217"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SupremeControlPlaneRoot.enable(tenant_id="t1", control_ref="c1").is_missing() is False,
        UniversalRoboticsNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        RoboticsCivilizationRoot.enable(tenant_id="t1", civilization_ref="civ1").is_missing() is False,
        CollectiveIntelligenceRoot.enable(tenant_id="t1", collective_ref="ci1").is_missing() is False,
        UniversalDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        KnowledgeGraphUniverseRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        AutonomousGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SupremeSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        HumanAuthorityRoot.enable(tenant_id="t1", authority_ref="ha1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_supreme_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t", "via_p216_u", "via_p216_v", "via_p216_w", "via_p216_x", "via_p216_y",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_meos_data_api", "via_meos_digital_twin_api", "via_meos_kg_api", "via_meos_agent_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_y_ultimate",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_identity_platform",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "human_authority_framework_required", "safety_by_design_required",
        "human_override_authority_required", "explainable_autonomous_systems_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_supreme_platform_forbidden", "completes_p216_master_series",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/supreme")', "/supreme/vision", "/supreme/domain",
        "/supreme/bounded-contexts", "/supreme/control-plane", "/supreme/universal-network",
        "/supreme/civilization", "/supreme/collective-intelligence",
        "/supreme/digital-twin", "/supreme/knowledge-graph", "/supreme/governance",
        "/supreme/observability", "/supreme/security", "/supreme/cqrs", "/supreme/events",
        "/supreme/microservices", "/supreme/integration",
        "/supreme/deployment", "/supreme/testing",
        "/supreme/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_SUPREME.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Ultimate Robotics Intelligence Architecture is missing",
        "Never MEOS Robotics Supreme Control Plane is missing",
        "Never Autonomous Robotics Civilization Layer is missing",
        "Never Universal Robotics Network is missing",
        "Never Collective Intelligence Engine is missing",
        "Never Robotics Digital Twin Universe is missing",
        "Never Robotics Knowledge Graph is missing",
        "Never Autonomous Governance is missing",
        "Never Security Architecture is missing",
        "Never Human Authority Framework is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Supreme Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-Y Ultimate",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Human Authority Framework",
        "Never Skip Safety-by-Design",
        "Never Skip Human Override Authority",
        "Never Skip Explainable Autonomous Systems",
        "MEOS Robotics Supreme Intelligence Nexus SHALL unify",
        "P216", "P216-Y", "P215-Z", "P214-Z", "P217",
        "Completes P216 Master Series",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-Z", "adr": 498, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
