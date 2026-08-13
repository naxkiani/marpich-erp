"""Biotechnology P217-I Precision Medicine foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/508-enterprise-biotechnology-precision-medicine.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_PRECISION_MEDICINE.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_PRECISION_MEDICINE_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_PRECISION_MEDICINE_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_PRECISION_MEDICINE_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_PRECISION_MEDICINE_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_PRECISION_MEDICINE_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_precision_medicine.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_precision_medicine_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_precision_medicine_acl.py",
    "backend/contexts/biotechnology/application/bio_precision_medicine_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/precision_medicine_platform",
    "backend/contexts/genomics_ai_platform",
    "backend/contexts/personalized_therapy_platform",
)
def validate_precision_medicine_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_precision_medicine_aggregates import (
        PrecisionMedicinePlatformRoot, GenomicsAiRoot, OmicsIntelligenceRoot,
        MolecularMedicineRoot, PersonalizedTherapyRoot, PatientMolecularProfileRoot,
        PrecisionDigitalTwinRoot, PrecisionMedicineGovernanceRoot, PrecisionMedicineSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_precision_medicine as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-I" and cat["adr"] == 508 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_precision_health_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["precision_medicine_platform_present_required"] is True
        and cat["genomics_ai_present_required"] is True
        and cat["omics_intelligence_present_required"] is True
        and cat["molecular_medicine_present_required"] is True
        and cat["personalized_therapy_present_required"] is True
        and cat["precision_digital_twin_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["genomics_ai"]["component_count"] == 4
        and cat["omics"]["domain_count"] == 5
        and cat["molecular_medicine"]["capability_count"] == 4
        and cat["personalized_therapy"]["capability_count"] == 5
        and cat["patient_molecular_profile"]["component_count"] == 4
        and cat["precision_agents"]["agent_count"] == 5
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_h_digital_health"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["precision_twins_via_p217g_p217h_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_autonomous_clinical_action_without_physician"] is True
        and cat["never_unconsented_genomic_processing"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_j"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PrecisionMedicinePlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        GenomicsAiRoot.enable(tenant_id="t1", genomics_ref="g1").is_missing() is False,
        OmicsIntelligenceRoot.enable(tenant_id="t1", omics_ref="o1").is_missing() is False,
        MolecularMedicineRoot.enable(tenant_id="t1", molecular_ref="m1").is_missing() is False,
        PersonalizedTherapyRoot.enable(tenant_id="t1", therapy_ref="th1").is_missing() is False,
        PatientMolecularProfileRoot.enable(tenant_id="t1", profile_ref="pr1").is_missing() is False,
        PrecisionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PrecisionMedicineGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        PrecisionMedicineSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_precision_medicine_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "precision_twins_via_p217g_p217h_acl_only", "no_module_local_llm",
        "never_opaque_unexplainable_decisions", "never_autonomous_clinical_action_without_physician",
        "never_unconsented_genomic_processing", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_precision_medicine_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/precision-medicine")', "/precision-medicine/vision",
        "/precision-medicine/architecture", "/precision-medicine/genomics-ai", "/precision-medicine/omics",
        "/precision-medicine/molecular-medicine", "/precision-medicine/personalized-therapy",
        "/precision-medicine/patient-molecular-profile", "/precision-medicine/precision-digital-twin",
        "/precision-medicine/agents", "/precision-medicine/domain-model", "/precision-medicine/security",
        "/precision-medicine/governance", "/precision-medicine/integration", "/precision-medicine/roadmap",
        "/precision-medicine/cqrs", "/precision-medicine/events", "/precision-medicine/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_PRECISION_MEDICINE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Precision Medicine Platform is missing",
        "Never Genomics AI is missing",
        "Never Omics Intelligence is missing",
        "Never Molecular Medicine is missing",
        "Never Personalized Therapy is missing",
        "Never Precision Digital Twin is missing",
        "Never AI Agents are missing",
        "Never Security Architecture is missing",
        "Never Governance is missing",
        "Never MEOS Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace P217-B Strategy",
        "Never Replace P217-C Domain",
        "Never Replace P217-D Infrastructure",
        "Never Replace P217-E Bio-AI",
        "Never Replace P217-F Synthetic",
        "Never Replace P217-G Simulation",
        "Never Replace P217-H Digital Health",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Never Autonomous Clinical Action Without Physician",
        "Never Unconsented Genomic Processing",
        "Create an intelligent healthcare ecosystem capable of analysing individual biological differences",
        "P217", "P217-H", "P216-Z", "P215-Z", "P214-Z", "P217-J",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-I", "adr": 508, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
