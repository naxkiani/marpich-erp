"""Robotics P216-Y ultimate / future intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/497-enterprise-robotics-ultimate.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_ULTIMATE.md",
    "docs/architecture/robotics/ROBOTICS_ULTIMATE_HOME.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ULTIMATE_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ULTIMATE_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ULTIMATE_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ULTIMATE_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_ultimate.py",
    "backend/contexts/robotics/domain/aggregates/rb_ultimate_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_ultimate_acl.py",
    "backend/contexts/robotics/application/rb_ultimate_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/future_robotics_architecture_platform",
    "backend/contexts/human_robot_symbiosis_platform",
    "backend/contexts/robotic_evolution_engine_platform",
    "backend/contexts/cognitive_robotics_ecosystem_platform",
)
def validate_rb_ultimate_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_ultimate_aggregates import (
        FutureRoboticsRoot, HumanMachineSymbiosisRoot, CognitiveRoboticsRoot,
        RoboticsEvolutionRoot, RoboticsDigitalTwinUniverseRoot, RoboticsKnowledgeGraphRoot,
        AutonomousIntelligenceRoot, UltimateTrustRoot, HumanGovernanceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_ultimate as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-Y" and cat["adr"] == 497 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_ultimate_robotics_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["entertainment_gate"] == "P216-X"
        and cat["personal_gate"] == "P216-W"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["future_robotics_architecture_present_required"] is True
        and cat["human_machine_symbiosis_platform_present_required"] is True
        and cat["cognitive_robotics_platform_present_required"] is True
        and cat["robotics_evolution_engine_present_required"] is True
        and cat["robotics_digital_twin_universe_present_required"] is True
        and cat["robotics_knowledge_graph_present_required"] is True
        and cat["autonomous_intelligence_layer_present_required"] is True
        and cat["trust_architecture_present_required"] is True
        and cat["human_governance_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_x_entertainment"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_control_preservation_required"] is True
        and cat["safety_by_design_required"] is True
        and cat["human_override_authority_required"] is True
        and cat["explainable_intelligence_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_z"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        FutureRoboticsRoot.enable(tenant_id="t1", future_ref="f1").is_missing() is False,
        HumanMachineSymbiosisRoot.enable(tenant_id="t1", symbiosis_ref="s1").is_missing() is False,
        CognitiveRoboticsRoot.enable(tenant_id="t1", cognitive_ref="c1").is_missing() is False,
        RoboticsEvolutionRoot.enable(tenant_id="t1", evolution_ref="e1").is_missing() is False,
        RoboticsDigitalTwinUniverseRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        RoboticsKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        AutonomousIntelligenceRoot.enable(tenant_id="t1", autonomy_ref="a1").is_missing() is False,
        UltimateTrustRoot.enable(tenant_id="t1", trust_ref="tr1").is_missing() is False,
        HumanGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_ultimate_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t", "via_p216_u", "via_p216_v", "via_p216_w", "via_p216_x",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_human_interface_api", "via_ai_agent_api", "via_smart_infrastructure_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_x_entertainment",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_identity_platform",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "human_control_preservation_required", "safety_by_design_required",
        "human_override_authority_required", "explainable_intelligence_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_ultimate_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/ultimate")', "/ultimate/vision", "/ultimate/domain",
        "/ultimate/bounded-contexts", "/ultimate/future-robotics", "/ultimate/symbiosis",
        "/ultimate/evolution", "/ultimate/cognitive", "/ultimate/autonomous-intelligence",
        "/ultimate/digital-twin", "/ultimate/knowledge-graph", "/ultimate/observability",
        "/ultimate/security", "/ultimate/cqrs", "/ultimate/events",
        "/ultimate/microservices", "/ultimate/integration",
        "/ultimate/deployment", "/ultimate/testing",
        "/ultimate/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_ULTIMATE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Future Robotics Architecture is missing",
        "Never Human-Machine Symbiosis Platform is missing",
        "Never Cognitive Robotics Platform is missing",
        "Never Robotics Evolution Engine is missing",
        "Never Robotics Digital Twin Universe is missing",
        "Never Robotics Knowledge Graph is missing",
        "Never Autonomous Intelligence Layer is missing",
        "Never Trust Architecture is missing",
        "Never Human Governance is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Ultimate Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-X Entertainment",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Human Control Preservation",
        "Never Skip Safety-by-Design",
        "Never Skip Human Override Authority",
        "Never Skip Explainable Intelligence for Autonomous Decisions",
        "MEOS Ultimate Robotics Intelligence Platform SHALL unify",
        "P216", "P216-X", "P215-Z", "P214-Z", "P216-Z",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-Y", "adr": 497, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
