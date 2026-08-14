"""Robotics P216-Q education / smart campus foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/489-enterprise-robotics-education.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_EDUCATION.md",
    "docs/architecture/robotics/ROBOTICS_EDUCATION_CAMPUS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_EDUCATION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_EDUCATION_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_EDUCATION_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_EDUCATION_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_education.py",
    "backend/contexts/robotics/domain/aggregates/rb_education_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_education_acl.py",
    "backend/contexts/robotics/application/rb_education_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/education_robotics_platform",
    "backend/contexts/ai_learning_intelligence_platform",
    "backend/contexts/autonomous_campus_operations_platform",
    "backend/contexts/smart_university_platform",
)
def validate_rb_education_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_education_aggregates import (
        EducationRoboticsRoot, AiLearningRoot, SmartCampusRoot,
        AutonomousEducationOperationsRoot, AcademicIntelligenceRoot,
        EducationDigitalTwinRoot, LearningKnowledgeGraphRoot,
        EducationSecurityRoot, SmartClassroomRoot,
    )
    from contexts.robotics.domain.services import rb_platform_education as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-Q" and cat["adr"] == 489 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_education_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["hospitality_gate"] == "P216-P"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["education_robotics_platform_present_required"] is True
        and cat["ai_learning_platform_present_required"] is True
        and cat["smart_campus_platform_present_required"] is True
        and cat["autonomous_education_operations_present_required"] is True
        and cat["academic_intelligence_platform_present_required"] is True
        and cat["education_digital_twin_present_required"] is True
        and cat["learning_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 14
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_p_hospitality"] is True
        and cat["never_duplicate_sis_lms_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["privacy_by_design_required"] is True
        and cat["accessibility_by_design_required"] is True
        and cat["human_centered_learning_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_r"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        EducationRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        AiLearningRoot.enable(tenant_id="t1", learning_ref="l1").is_missing() is False,
        SmartCampusRoot.enable(tenant_id="t1", campus_ref="c1").is_missing() is False,
        AutonomousEducationOperationsRoot.enable(tenant_id="t1", operations_ref="o1").is_missing() is False,
        AcademicIntelligenceRoot.enable(tenant_id="t1", academic_ref="a1").is_missing() is False,
        EducationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        LearningKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        EducationSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        SmartClassroomRoot.enable(tenant_id="t1", classroom_ref="cl1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_education_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_sis_api", "via_lms_api", "via_library_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_p_hospitality",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_duplicate_sis_lms_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "privacy_by_design_required", "accessibility_by_design_required", "human_centered_learning_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_education_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/education")', "/education/vision", "/education/domain",
        "/education/bounded-contexts", "/education/robotics", "/education/ai-learning",
        "/education/smart-campus", "/education/autonomous-operations", "/education/academic-intelligence",
        "/education/digital-twin", "/education/knowledge-graph", "/education/observability",
        "/education/security", "/education/cqrs", "/education/events", "/education/microservices",
        "/education/integration", "/education/deployment", "/education/testing",
        "/education/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_EDUCATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Education Robotics Platform is missing",
        "Never AI Learning Platform is missing",
        "Never Smart Campus Platform is missing",
        "Never Autonomous Education Operations is missing",
        "Never Academic Intelligence Platform is missing",
        "Never Education Digital Twin is missing",
        "Never Learning Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Education Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-P Hospitality",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate SIS/LMS Core Logic",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Privacy by Design for Student Data",
        "Never Skip Accessibility by Design",
        "MEOS Education Intelligence Platform SHALL unify",
        "P216", "P216-P", "P215-Z", "P214-Z", "P216-R",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-Q", "adr": 489, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
