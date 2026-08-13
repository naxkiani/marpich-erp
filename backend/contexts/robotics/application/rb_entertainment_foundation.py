"""Robotics P216-X entertainment / creative intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/496-enterprise-robotics-entertainment.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_ENTERTAINMENT.md",
    "docs/architecture/robotics/ROBOTICS_ENTERTAINMENT_HOME.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ENTERTAINMENT_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ENTERTAINMENT_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ENTERTAINMENT_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_ENTERTAINMENT_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_entertainment.py",
    "backend/contexts/robotics/domain/aggregates/rb_entertainment_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_entertainment_acl.py",
    "backend/contexts/robotics/application/rb_entertainment_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/entertainment_robotics_platform",
    "backend/contexts/creative_ai_intelligence_platform",
    "backend/contexts/autonomous_media_production_platform",
    "backend/contexts/immersive_reality_platform",
)
def validate_rb_entertainment_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_entertainment_aggregates import (
        EntertainmentRoboticsRoot, CreativeAiRoot, AutonomousMediaProductionRoot,
        DigitalExperienceRoot, ImmersiveRealityRoot, CreativeDigitalTwinRoot,
        EntertainmentKnowledgeGraphRoot, CreativeSecurityRoot, CreativeGovernanceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_entertainment as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-X" and cat["adr"] == 496 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_creative_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["personal_gate"] == "P216-W"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["entertainment_robotics_platform_present_required"] is True
        and cat["creative_ai_platform_present_required"] is True
        and cat["autonomous_media_production_platform_present_required"] is True
        and cat["digital_experience_intelligence_present_required"] is True
        and cat["immersive_reality_platform_present_required"] is True
        and cat["creative_digital_twin_present_required"] is True
        and cat["entertainment_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["creative_governance_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_w_personal"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["no_module_local_llm"] is True
        and cat["creative_rights_governance_required"] is True
        and cat["human_ai_creative_collaboration_required"] is True
        and cat["explainable_ai_required"] is True
        and cat["audience_privacy_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_y"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        EntertainmentRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        CreativeAiRoot.enable(tenant_id="t1", creative_ref="c1").is_missing() is False,
        AutonomousMediaProductionRoot.enable(tenant_id="t1", media_ref="m1").is_missing() is False,
        DigitalExperienceRoot.enable(tenant_id="t1", experience_ref="e1").is_missing() is False,
        ImmersiveRealityRoot.enable(tenant_id="t1", immersive_ref="i1").is_missing() is False,
        CreativeDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        EntertainmentKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        CreativeSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        CreativeGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_entertainment_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t", "via_p216_u", "via_p216_v", "via_p216_w",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_gaming_api", "via_streaming_api", "via_metaverse_api", "via_creative_software_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_w_personal",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_identity_platform",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "creative_rights_governance_required", "human_ai_creative_collaboration_required",
        "explainable_ai_required", "audience_privacy_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_entertainment_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/entertainment")', "/entertainment/vision", "/entertainment/domain",
        "/entertainment/bounded-contexts", "/entertainment/robotics", "/entertainment/creative-ai",
        "/entertainment/media-production", "/entertainment/digital-experience",
        "/entertainment/immersive-reality", "/entertainment/digital-twin",
        "/entertainment/knowledge-graph", "/entertainment/observability",
        "/entertainment/security", "/entertainment/cqrs", "/entertainment/events",
        "/entertainment/microservices", "/entertainment/integration",
        "/entertainment/deployment", "/entertainment/testing",
        "/entertainment/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_ENTERTAINMENT.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Entertainment Robotics Platform is missing",
        "Never Creative AI Platform is missing",
        "Never Autonomous Media Production Platform is missing",
        "Never Digital Experience Intelligence is missing",
        "Never Immersive Reality Platform is missing",
        "Never Creative Digital Twin is missing",
        "Never Entertainment Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never Creative Governance is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Entertainment Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-W Personal",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Creative Rights Governance",
        "Never Skip Human-AI Creative Collaboration Controls",
        "Never Skip Explainable AI for Creative Decisions",
        "Never Skip Audience Privacy Protections",
        "MEOS Creative Intelligence Platform SHALL unify",
        "P216", "P216-W", "P215-Z", "P214-Z", "P216-Y",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-X", "adr": 496, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
