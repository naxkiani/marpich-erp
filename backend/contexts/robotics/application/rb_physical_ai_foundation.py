"""Robotics P216-E Physical AI foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/477-enterprise-robotics-physical-ai.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_PHYSICAL_AI.md",
    "docs/architecture/robotics/ROBOTICS_PHYSICAL_AI_ENGINE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PHYSICAL_AI_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PHYSICAL_AI_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PHYSICAL_AI_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PHYSICAL_AI_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_physical_ai.py",
    "backend/contexts/robotics/domain/aggregates/rb_physical_ai_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_physical_ai_acl.py",
    "backend/contexts/robotics/application/rb_physical_ai_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/physical_ai_platform",
    "backend/contexts/robot_perception_platform",
    "backend/contexts/cognitive_robotics_platform",
)
def validate_rb_physical_ai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_physical_ai_aggregates import (
        PhysicalAIEngineRoot, PerceptionPlatformRoot, CognitiveRoboticsRoot,
        AutonomousDecisionRoot, WorldModelRoot, RobotMemoryRoot,
        LearningPlatformRoot, ResponsibleAIRoot, KnowledgeGraphRoot,
    )
    from contexts.robotics.domain.services import rb_platform_physical_ai as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-E" and cat["adr"] == 477 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_physical_ai_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["mission_gate"] == "P216-A"
        and cat["strategy_gate"] == "P216-B" and cat["domain_gate"] == "P216-C"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["physical_ai_engine_present_required"] is True
        and cat["robot_perception_platform_present_required"] is True
        and cat["cognitive_robotics_platform_present_required"] is True
        and cat["autonomous_decision_platform_present_required"] is True
        and cat["world_model_architecture_present_required"] is True
        and cat["robot_memory_architecture_present_required"] is True
        and cat["learning_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["safety_and_responsible_ai_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_d_runtime"] is True
        and cat["physical_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_f"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PhysicalAIEngineRoot.enable(tenant_id="t1", engine_ref="e1").is_missing() is False,
        PerceptionPlatformRoot.enable(tenant_id="t1", perception_ref="p1").is_missing() is False,
        CognitiveRoboticsRoot.enable(tenant_id="t1", cognitive_ref="c1").is_missing() is False,
        AutonomousDecisionRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        WorldModelRoot.enable(tenant_id="t1", world_ref="w1").is_missing() is False,
        RobotMemoryRoot.enable(tenant_id="t1", memory_ref="m1").is_missing() is False,
        LearningPlatformRoot.enable(tenant_id="t1", learning_ref="l1").is_missing() is False,
        ResponsibleAIRoot.enable(tenant_id="t1", responsible_ref="r1").is_missing() is False,
        KnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_physical_ai_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p215_z", "via_p214_z",
        "via_p213", "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_a_mission", "never_replace_p216_b_strategy",
        "never_replace_p216_c_domain", "never_replace_p216_d_runtime", "never_replace_p215_z",
        "never_replace_ai_platform", "never_replace_core_platform", "no_module_local_llm",
        "physical_ai_via_p214z_acl_only", "never_opaque_unexplainable_decisions",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_physical_ai_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/physical-ai")', "/physical-ai/vision", "/physical-ai/domain",
        "/physical-ai/bounded-contexts", "/physical-ai/perception", "/physical-ai/engine",
        "/physical-ai/cognitive", "/physical-ai/decisions", "/physical-ai/world-model",
        "/physical-ai/memory", "/physical-ai/knowledge-graph", "/physical-ai/digital-twin",
        "/physical-ai/responsible-ai", "/physical-ai/cqrs", "/physical-ai/events",
        "/physical-ai/microservices", "/physical-ai/integration", "/physical-ai/deployment",
        "/physical-ai/testing", "/physical-ai/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_PHYSICAL_AI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Physical AI Engine is missing",
        "Never Robot Perception Platform is missing",
        "Never Cognitive Robotics Platform is missing",
        "Never Autonomous Decision Platform is missing",
        "Never World Model Architecture is missing",
        "Never Robot Memory Architecture is missing",
        "Never Learning Platform is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never Safety and Responsible AI is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge AI Deployment is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-A Mission",
        "Never Replace P216-B Strategy",
        "Never Replace P216-C Domain",
        "Never Replace P216-D Runtime",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Opaque Unexplainable Decisions",
        "Physical AI enables robots to perceive",
        "P216", "P216-D", "P215-Z", "P214-Z", "P216-F",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-E", "adr": 477, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
