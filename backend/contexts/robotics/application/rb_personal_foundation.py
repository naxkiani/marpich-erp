"""Robotics P216-W personal / home intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/495-enterprise-robotics-personal.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_PERSONAL.md",
    "docs/architecture/robotics/ROBOTICS_PERSONAL_HOME.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PERSONAL_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PERSONAL_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PERSONAL_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PERSONAL_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_personal.py",
    "backend/contexts/robotics/domain/aggregates/rb_personal_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_personal_acl.py",
    "backend/contexts/robotics/application/rb_personal_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/personal_robotics_platform",
    "backend/contexts/consumer_ai_robotics_platform",
    "backend/contexts/home_intelligence_platform",
    "backend/contexts/personal_ai_assistant_platform",
)
def validate_rb_personal_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_personal_aggregates import (
        PersonalRoboticsRoot, AiCompanionRoot, SmartHomeIntelligenceRoot,
        HumanAugmentationRoot, LifeAutomationRoot, PersonalDigitalTwinRoot,
        PersonalKnowledgeGraphRoot, PersonalSecurityRoot, PrivacySovereigntyRoot,
    )
    from contexts.robotics.domain.services import rb_platform_personal as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-W" and cat["adr"] == 495 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_personal_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["science_gate"] == "P216-V"
        and cat["healthcare_gate"] == "P216-I" and cat["education_gate"] == "P216-Q"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["personal_robotics_platform_present_required"] is True
        and cat["ai_companion_platform_present_required"] is True
        and cat["smart_home_intelligence_present_required"] is True
        and cat["personal_digital_twin_present_required"] is True
        and cat["human_augmentation_platform_present_required"] is True
        and cat["personal_knowledge_graph_present_required"] is True
        and cat["life_automation_platform_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["privacy_sovereignty_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_v_science"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["no_module_local_llm"] is True
        and cat["privacy_by_design_required"] is True
        and cat["personal_data_sovereignty_required"] is True
        and cat["human_control_by_design_required"] is True
        and cat["consent_management_required"] is True
        and cat["explainable_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_x"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PersonalRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        AiCompanionRoot.enable(tenant_id="t1", companion_ref="c1").is_missing() is False,
        SmartHomeIntelligenceRoot.enable(tenant_id="t1", home_ref="h1").is_missing() is False,
        HumanAugmentationRoot.enable(tenant_id="t1", augmentation_ref="a1").is_missing() is False,
        LifeAutomationRoot.enable(tenant_id="t1", automation_ref="la1").is_missing() is False,
        PersonalDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PersonalKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        PersonalSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        PrivacySovereigntyRoot.enable(tenant_id="t1", privacy_ref="p1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_personal_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t", "via_p216_u", "via_p216_v",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_iot_api", "via_smart_home_api", "via_wearable_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_v_science",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_identity_platform",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "privacy_by_design_required", "personal_data_sovereignty_required",
        "human_control_by_design_required", "consent_management_required", "explainable_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_personal_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/personal")', "/personal/vision", "/personal/domain",
        "/personal/bounded-contexts", "/personal/robotics", "/personal/ai-companion",
        "/personal/smart-home", "/personal/human-augmentation", "/personal/life-automation",
        "/personal/digital-twin", "/personal/knowledge-graph", "/personal/observability",
        "/personal/security", "/personal/cqrs", "/personal/events", "/personal/microservices",
        "/personal/integration", "/personal/deployment", "/personal/testing",
        "/personal/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_PERSONAL.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Personal Robotics Platform is missing",
        "Never AI Companion Platform is missing",
        "Never Smart Home Intelligence is missing",
        "Never Personal Digital Twin is missing",
        "Never Human Augmentation Platform is missing",
        "Never Personal Knowledge Graph is missing",
        "Never Life Automation Platform is missing",
        "Never Security Architecture is missing",
        "Never Privacy Sovereignty is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Personal Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-V Science",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Privacy by Design for Personal Data",
        "Never Skip Human Control by Design",
        "Never Skip Consent Management",
        "Never Skip Explainable AI for Personal Decisions",
        "Never Skip Personal Data Sovereignty",
        "MEOS Personal Intelligence Platform SHALL unify",
        "P216", "P216-V", "P215-Z", "P214-Z", "P216-X",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-W", "adr": 495, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
