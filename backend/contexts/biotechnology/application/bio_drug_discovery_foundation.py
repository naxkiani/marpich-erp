"""Biotechnology P217-K Drug Discovery foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/510-enterprise-biotechnology-drug-discovery.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_DRUG_DISCOVERY.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DRUG_DISCOVERY_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DRUG_DISCOVERY_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DRUG_DISCOVERY_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DRUG_DISCOVERY_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DRUG_DISCOVERY_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_drug_discovery.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_drug_discovery_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_drug_discovery_acl.py",
    "backend/contexts/biotechnology/application/bio_drug_discovery_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/drug_discovery_platform",
    "backend/contexts/ai_drug_design_platform",
    "backend/contexts/pharmaceutical_intelligence_platform",
)
def validate_drug_discovery_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_drug_discovery_aggregates import (
        DrugDiscoveryPlatformRoot, AiDrugDesignRoot, MolecularDiscoveryRoot,
        PharmaceuticalIntelligenceRoot, DrugDigitalTwinRoot, PharmaKnowledgeGraphRoot,
        DrugDiscoveryAgentsRoot, DrugDiscoveryGovernanceRoot, DrugDiscoverySecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_drug_discovery as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-K" and cat["adr"] == 510 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_drug_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["drug_discovery_platform_present_required"] is True
        and cat["ai_drug_design_present_required"] is True
        and cat["molecular_discovery_present_required"] is True
        and cat["pharmaceutical_intelligence_present_required"] is True
        and cat["drug_digital_twin_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["ai_drug_design"]["component_count"] == 4
        and cat["molecular_discovery"]["capability_count"] == 4
        and cat["computational_drug"]["engine_count"] == 4
        and cat["drug_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_j_clinical_research"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["drug_twins_via_p217g_acl_only"] is True
        and cat["quantum_molecular_via_p215z_acl_only"] is True
        and cat["lab_execution_via_p216z_acl_only"] is True
        and cat["clinical_translation_via_p217j_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_unvalidated_therapeutic_candidate_release"] is True
        and cat["never_skip_human_scientific_oversight"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_l"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        DrugDiscoveryPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        AiDrugDesignRoot.enable(tenant_id="t1", design_ref="d1").is_missing() is False,
        MolecularDiscoveryRoot.enable(tenant_id="t1", molecular_ref="m1").is_missing() is False,
        PharmaceuticalIntelligenceRoot.enable(tenant_id="t1", pharma_ref="ph1").is_missing() is False,
        DrugDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PharmaKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        DrugDiscoveryAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        DrugDiscoveryGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        DrugDiscoverySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_drug_discovery_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "drug_twins_via_p217g_acl_only", "quantum_molecular_via_p215z_acl_only",
        "lab_execution_via_p216z_acl_only", "clinical_translation_via_p217j_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_unvalidated_therapeutic_candidate_release",
        "never_skip_human_scientific_oversight", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_drug_discovery_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/drug-discovery")', "/drug-discovery/vision",
        "/drug-discovery/architecture", "/drug-discovery/ai-drug-design",
        "/drug-discovery/molecular-discovery", "/drug-discovery/computational-intelligence",
        "/drug-discovery/drug-digital-twin", "/drug-discovery/knowledge-graph",
        "/drug-discovery/agents", "/drug-discovery/domain-model", "/drug-discovery/quantum-readiness",
        "/drug-discovery/governance", "/drug-discovery/security", "/drug-discovery/integration",
        "/drug-discovery/roadmap", "/drug-discovery/cqrs", "/drug-discovery/events",
        "/drug-discovery/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_DRUG_DISCOVERY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Drug Discovery Platform is missing",
        "Never AI Drug Design is missing",
        "Never Molecular Discovery is missing",
        "Never Pharmaceutical Intelligence is missing",
        "Never Drug Digital Twin is missing",
        "Never Knowledge Graph is missing",
        "Never AI Agents are missing",
        "Never Quantum Readiness is missing",
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
        "Never Replace P217-J Clinical Research",
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
        "Never Skip Human Scientific Oversight",
        "Never Unvalidated Therapeutic Candidate Release",
        "Create an intelligent pharmaceutical discovery ecosystem capable of discovering",
        "P217", "P217-J", "P216-Z", "P215-Z", "P214-Z", "P217-L",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-K", "adr": 510, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
