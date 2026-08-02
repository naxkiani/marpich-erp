"""Space P218-E Space AI foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/531-enterprise-space-intelligence-space-ai.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SPACE_AI.md",
    "docs/architecture/space/SPACE_AI_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/SPACE_AI_MODELS.v1.yaml",
    "docs/architecture/space/SPACE_AI_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SPACE_AI_SECURITY.v1.yaml",
    "docs/architecture/space/SPACE_AI_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_space_ai.py",
    "backend/contexts/space/domain/aggregates/sp_space_ai_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_space_ai_acl.py",
    "backend/contexts/space/application/sp_space_ai_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_ai_platform",
    "backend/contexts/space_foundation_model_platform",
    "backend/contexts/space_cognitive_platform_bc",
)
def validate_sp_space_ai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_space_ai_aggregates import (
        SpaceAiPlatformRoot, FoundationModelsRoot, SpaceAiEngineRoot, MissionIntelligenceRoot,
        AutonomousDecisionRoot, SpaceAgentsRoot, KnowledgeGraphRoot, ResponsibleSpaceAiRoot, SpaceAiSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_space_ai as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-E" and cat["adr"] == 531 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_ai_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_ai_platform_present_required"] is True
        and cat["foundation_models_present_required"] is True
        and cat["space_ai_engine_present_required"] is True
        and cat["mission_intelligence_platform_present_required"] is True
        and cat["autonomous_decision_platform_present_required"] is True
        and cat["space_cognitive_platform_present_required"] is True
        and cat["multi_agent_architecture_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["ai_governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["foundation_models"]["model_count"] == 5
        and cat["space_ai_engine"]["component_count"] == 4
        and cat["mission_intelligence"]["capability_count"] == 8
        and cat["scientific_agents"]["agent_count"] == 12
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_d_infrastructure"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungated_autonomous_mission_strategy"] is True
        and cat["foundation_for_p218_f"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SpaceAiPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        FoundationModelsRoot.enable(tenant_id="t1", models_ref="m1").is_missing() is False,
        SpaceAiEngineRoot.enable(tenant_id="t1", engine_ref="e1").is_missing() is False,
        MissionIntelligenceRoot.enable(tenant_id="t1", intel_ref="i1").is_missing() is False,
        AutonomousDecisionRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        SpaceAgentsRoot.enable(tenant_id="t1", agents_ref="a1").is_missing() is False,
        KnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ResponsibleSpaceAiRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SpaceAiSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_space_ai_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p218_d", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_a_mission", "never_replace_p218_b_strategy",
        "never_replace_p218_c_domain", "never_replace_p218_d_infrastructure",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "space_ai_via_p214z_acl_only", "no_module_local_llm",
        "never_opaque_unexplainable_decisions", "module_local_space_ai_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/space-ai")', "/space-ai/vision", "/space-ai/architecture",
        "/space-ai/foundation-models", "/space-ai/engine", "/space-ai/mission-intelligence",
        "/space-ai/decision", "/space-ai/agents", "/space-ai/knowledge-graph",
        "/space-ai/lifecycle", "/space-ai/governance", "/space-ai/security",
        "/space-ai/integration", "/space-ai/deployment", "/space-ai/testing",
        "/space-ai/cqrs", "/space-ai/events", "/space-ai/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SPACE_AI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space AI Platform is missing",
        "Never Foundation Models are missing",
        "Never Space AI Engine is missing",
        "Never Mission Intelligence Platform is missing",
        "Never Autonomous Decision Platform is missing",
        "Never Space Cognitive Platform is missing",
        "Never Multi-Agent Architecture is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never AI Governance is missing",
        "Never Security Architecture is missing",
        "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Space BC",
        "Never Replace P218 Foundation",
        "Never Replace P218-A Mission",
        "Never Replace P218-B Strategy",
        "Never Replace P218-C Domain",
        "Never Replace P218-D Infrastructure",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Build the enterprise cognitive engine",
        "P218", "P218-D", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-F",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-E", "adr": 531, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
