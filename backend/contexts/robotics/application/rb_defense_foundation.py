"""Robotics P216-U defense / strategic intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/493-enterprise-robotics-defense.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_DEFENSE.md",
    "docs/architecture/robotics/ROBOTICS_DEFENSE_STRATEGIC.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DEFENSE_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DEFENSE_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DEFENSE_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DEFENSE_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_defense.py",
    "backend/contexts/robotics/domain/aggregates/rb_defense_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_defense_acl.py",
    "backend/contexts/robotics/application/rb_defense_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/military_robotics_platform",
    "backend/contexts/autonomous_defense_intelligence_platform",
    "backend/contexts/strategic_security_intelligence_platform",
    "backend/contexts/defense_ai_operations_platform",
)
def validate_rb_defense_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_defense_aggregates import (
        DefenseRoboticsRoot, StrategicIntelligenceRoot, AutonomousSystemGovernanceRoot,
        DefenseAiRoot, DefenseDigitalTwinRoot, SecurityKnowledgeGraphRoot,
        DefenseSecurityRoot, HumanOversightRoot, MissionIntelligenceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_defense as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-U" and cat["adr"] == 493 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_defense_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["government_gate"] == "P216-T"
        and cat["public_safety_gate"] == "P216-L" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["military_robotics_platform_present_required"] is True
        and cat["strategic_intelligence_platform_present_required"] is True
        and cat["autonomous_system_governance_present_required"] is True
        and cat["defense_ai_platform_present_required"] is True
        and cat["defense_digital_twin_present_required"] is True
        and cat["security_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["human_oversight_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 6
        and cat["domain_model"]["entity_count"] == 11
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_t_government"] is True
        and cat["never_replace_p216_l_public_safety"] is True
        and cat["never_duplicate_public_safety_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_authorization_control_required"] is True
        and cat["responsible_ai_governance_required"] is True
        and cat["explainable_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_v"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        DefenseRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        StrategicIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        AutonomousSystemGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        DefenseAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        DefenseDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SecurityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        DefenseSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        HumanOversightRoot.enable(tenant_id="t1", oversight_ref="h1").is_missing() is False,
        MissionIntelligenceRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_defense_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_cyber_api", "via_emergency_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_t_government", "never_replace_p216_l_public_safety",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_duplicate_public_safety_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "human_authorization_control_required", "responsible_ai_governance_required", "explainable_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_defense_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/defense")', "/defense/vision", "/defense/domain",
        "/defense/bounded-contexts", "/defense/robotics", "/defense/strategic-intelligence",
        "/defense/autonomous-governance", "/defense/ai", "/defense/mission-intelligence",
        "/defense/resilience", "/defense/digital-twin", "/defense/knowledge-graph",
        "/defense/observability", "/defense/security", "/defense/cqrs", "/defense/events",
        "/defense/microservices", "/defense/integration", "/defense/deployment",
        "/defense/testing", "/defense/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_DEFENSE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Military Robotics Platform is missing",
        "Never Strategic Intelligence Platform is missing",
        "Never Autonomous System Governance is missing",
        "Never Defense AI Platform is missing",
        "Never Defense Digital Twin is missing",
        "Never Security Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Defense Integration is missing",
        "Never Testing Architecture is missing",
        "Never Human Oversight Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-T Government",
        "Never Replace P216-L Public Safety",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate Public Safety Core Logic",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Human Authorization Control",
        "Never Skip Responsible AI Governance",
        "Never Skip Explainable AI for Defense Decisions",
        "MEOS Defense Intelligence Platform SHALL unify",
        "P216", "P216-T", "P215-Z", "P214-Z", "P216-V",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-U", "adr": 493, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
