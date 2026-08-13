"""Biotechnology P217-J Clinical Research foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/509-enterprise-biotechnology-clinical-research.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_CLINICAL_RESEARCH.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_CLINICAL_RESEARCH_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_CLINICAL_RESEARCH_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_CLINICAL_RESEARCH_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_CLINICAL_RESEARCH_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_CLINICAL_RESEARCH_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_clinical_research.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_clinical_research_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_clinical_research_acl.py",
    "backend/contexts/biotechnology/application/bio_clinical_research_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/clinical_research_platform",
    "backend/contexts/ai_clinical_trial_platform",
    "backend/contexts/scientific_discovery_platform",
)
def validate_clinical_research_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_clinical_research_aggregates import (
        ClinicalResearchPlatformRoot, AiClinicalTrialsRoot, ScientificDiscoveryRoot,
        ResearchAutomationRoot, ClinicalDigitalTwinRoot, ResearchKnowledgeGraphRoot,
        ResearchAgentsRoot, ClinicalResearchGovernanceRoot, ClinicalResearchSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_clinical_research as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-J" and cat["adr"] == 509 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_clinical_innovation_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["clinical_research_platform_present_required"] is True
        and cat["ai_clinical_trials_present_required"] is True
        and cat["scientific_discovery_intelligence_present_required"] is True
        and cat["research_automation_present_required"] is True
        and cat["clinical_digital_twin_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["ai_clinical_trials"]["component_count"] == 5
        and cat["scientific_discovery"]["capability_count"] == 4
        and cat["research_automation"]["domain_count"] == 4
        and cat["research_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_i_precision_medicine"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["trial_simulation_via_p217g_acl_only"] is True
        and cat["lab_automation_via_p216z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_autonomous_clinical_trial_without_ethics_approval"] is True
        and cat["never_skip_human_researcher_oversight"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_k"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ClinicalResearchPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        AiClinicalTrialsRoot.enable(tenant_id="t1", trials_ref="tr1").is_missing() is False,
        ScientificDiscoveryRoot.enable(tenant_id="t1", discovery_ref="d1").is_missing() is False,
        ResearchAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        ClinicalDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ResearchKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ResearchAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        ClinicalResearchGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        ClinicalResearchSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_clinical_research_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "trial_simulation_via_p217g_acl_only", "lab_automation_via_p216z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_autonomous_clinical_trial_without_ethics_approval",
        "never_skip_human_researcher_oversight", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_clinical_research_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/clinical-research")', "/clinical-research/vision",
        "/clinical-research/architecture", "/clinical-research/ai-clinical-trials",
        "/clinical-research/scientific-discovery", "/clinical-research/research-automation",
        "/clinical-research/clinical-digital-twin", "/clinical-research/knowledge-graph",
        "/clinical-research/agents", "/clinical-research/domain-model", "/clinical-research/governance",
        "/clinical-research/security", "/clinical-research/integration", "/clinical-research/roadmap",
        "/clinical-research/cqrs", "/clinical-research/events", "/clinical-research/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_CLINICAL_RESEARCH.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Clinical Research Platform is missing",
        "Never AI Clinical Trials is missing",
        "Never Scientific Discovery Intelligence is missing",
        "Never Research Automation is missing",
        "Never Clinical Digital Twin is missing",
        "Never Knowledge Graph is missing",
        "Never AI Agents are missing",
        "Never Governance is missing",
        "Never Security Architecture is missing",
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
        "Never Replace P217-I Precision Medicine",
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
        "Never Autonomous Clinical Trial Without Ethics Approval",
        "Never Skip Human Researcher Oversight",
        "Create an intelligent research ecosystem capable of accelerating biomedical discoveries",
        "P217", "P217-I", "P216-Z", "P215-Z", "P214-Z", "P217-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-J", "adr": 509, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
