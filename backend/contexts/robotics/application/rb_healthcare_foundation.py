"""Robotics P216-I healthcare robotics / medical AI / surgical foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/481-enterprise-robotics-healthcare.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_HEALTHCARE.md",
    "docs/architecture/robotics/ROBOTICS_HEALTHCARE_CLINICAL.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HEALTHCARE_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HEALTHCARE_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HEALTHCARE_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HEALTHCARE_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_healthcare.py",
    "backend/contexts/robotics/domain/aggregates/rb_healthcare_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_healthcare_acl.py",
    "backend/contexts/robotics/application/rb_healthcare_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/healthcare_robotics_platform",
    "backend/contexts/medical_ai_platform",
    "backend/contexts/surgical_robotics_platform",
    "backend/contexts/digital_healthcare_automation_platform",
)
def validate_rb_healthcare_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_healthcare_aggregates import (
        HealthcareRoboticsRoot, MedicalAiRoot, SurgicalRoboticsRoot,
        DigitalHealthcareAutomationRoot, ClinicalDecisionRoot, HealthcareDigitalTwinRoot,
        MedicalKnowledgeGraphRoot, HealthcareSecurityRoot, HealthcareObservabilityRoot,
    )
    from contexts.robotics.domain.services import rb_platform_healthcare as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-I" and cat["adr"] == 481 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_healthcare_robotics_fabric"
        and cat["foundation_gate"] == "P216" and cat["mobility_gate"] == "P216-H"
        and cat["logistics_gate"] == "P216-G" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["healthcare_robotics_platform_present_required"] is True
        and cat["medical_ai_platform_present_required"] is True
        and cat["surgical_robotics_platform_present_required"] is True
        and cat["clinical_decision_intelligence_present_required"] is True
        and cat["digital_healthcare_automation_platform_present_required"] is True
        and cat["healthcare_digital_twin_present_required"] is True
        and cat["medical_knowledge_graph_present_required"] is True
        and cat["security_compliance_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 11
        and cat["events"]["core_event_count"] == 10
        and cat["domain_model"]["entity_count"] == 14
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_h_mobility"] is True
        and cat["never_direct_fhir_hl7_dicom_bypass"] is True
        and cat["never_duplicate_hospital_clinic_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_in_the_loop_required_for_clinical_autonomy"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_j"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        HealthcareRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        MedicalAiRoot.enable(tenant_id="t1", medical_ai_ref="m1").is_missing() is False,
        SurgicalRoboticsRoot.enable(tenant_id="t1", surgical_ref="s1").is_missing() is False,
        DigitalHealthcareAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        ClinicalDecisionRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        HealthcareDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MedicalKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        HealthcareSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        HealthcareObservabilityRoot.enable(tenant_id="t1", observability_ref="o1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_healthcare_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_hospital_api", "via_clinic_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_h_mobility",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_fhir_hl7_dicom_bypass", "fhir_hl7_dicom_via_integration_platform_only",
        "never_duplicate_hospital_clinic_core_logic",
        "no_module_local_llm", "medical_ai_via_p214z_acl_only", "physical_ai_via_p214z_acl_only",
        "human_in_the_loop_required_for_clinical_autonomy",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_healthcare_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/healthcare")', "/healthcare/vision", "/healthcare/domain",
        "/healthcare/bounded-contexts", "/healthcare/robotics", "/healthcare/medical-ai",
        "/healthcare/surgical", "/healthcare/automation", "/healthcare/clinical-decision",
        "/healthcare/digital-twin", "/healthcare/knowledge-graph", "/healthcare/observability",
        "/healthcare/security", "/healthcare/cqrs", "/healthcare/events", "/healthcare/microservices",
        "/healthcare/integration", "/healthcare/deployment", "/healthcare/testing",
        "/healthcare/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_HEALTHCARE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Healthcare Robotics Platform is missing",
        "Never Medical AI Platform is missing",
        "Never Surgical Robotics Platform is missing",
        "Never Clinical Decision Intelligence is missing",
        "Never Digital Healthcare Automation Platform is missing",
        "Never Healthcare Digital Twin is missing",
        "Never Medical Knowledge Graph is missing",
        "Never Clinical Decision Platform is missing",
        "Never Security & Compliance Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Healthcare Integration is missing",
        "Never Testing & Validation Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-H Mobility",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate Hospital/Clinic Core Logic",
        "Never Direct FHIR/HL7/DICOM Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Human-in-the-Loop for Clinical Autonomy",
        "MEOS Healthcare Robotics Platform SHALL unify",
        "P216", "P216-H", "P215-Z", "P214-Z", "P216-J",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-I", "adr": 481, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
