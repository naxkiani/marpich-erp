"""Biotechnology P217-N Bio Regulatory foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/513-enterprise-biotechnology-bio-regulatory.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_REGULATORY.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_REGULATORY_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_REGULATORY_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_REGULATORY_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_REGULATORY_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_REGULATORY_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_regulatory.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_regulatory_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_regulatory_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_regulatory_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_regulatory_platform",
    "backend/contexts/regulatory_ai_platform",
    "backend/contexts/life_science_governance_platform",
)
def validate_bio_regulatory_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_regulatory_aggregates import (
        BioRegulatoryPlatformRoot, RegulatoryAiRoot, BiomedicalComplianceRoot,
        LifeScienceGovernanceRoot, RegulatoryKnowledgeGraphRoot, RegulatoryDigitalTwinRoot,
        RegulatoryAgentsRoot, BioRegulatoryEthicsRoot, BioRegulatorySecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_regulatory as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-N" and cat["adr"] == 513 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_regulatory_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L" and cat["bio_supply_chain_gate"] == "P217-M"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_regulatory_platform_present_required"] is True
        and cat["regulatory_ai_present_required"] is True
        and cat["biomedical_compliance_present_required"] is True
        and cat["life_science_governance_present_required"] is True
        and cat["regulatory_knowledge_graph_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["ethics_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["regulatory_ai"]["component_count"] == 4
        and cat["biomedical_compliance"]["domain_count"] == 4
        and cat["compliance_ops"]["capability_count"] == 4
        and cat["regulatory_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_m_bio_supply_chain"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["never_replace_compliance_platform"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["regulatory_twins_via_p217g_acl_only"] is True
        and cat["manufacturing_compliance_via_p217l_acl_only"] is True
        and cat["distribution_compliance_via_p217m_acl_only"] is True
        and cat["drug_regulatory_via_p217k_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_human_regulatory_oversight"] is True
        and cat["never_autonomous_regulatory_submission_without_approval"] is True
        and cat["never_skip_explainable_regulatory_ai"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_o"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioRegulatoryPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        RegulatoryAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        BiomedicalComplianceRoot.enable(tenant_id="t1", compliance_ref="c1").is_missing() is False,
        LifeScienceGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        RegulatoryKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        RegulatoryDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        RegulatoryAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioRegulatoryEthicsRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        BioRegulatorySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_regulatory_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery", "never_replace_p217_l_bio_manufacturing",
        "never_replace_p217_m_bio_supply_chain",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "regulatory_twins_via_p217g_acl_only", "manufacturing_compliance_via_p217l_acl_only",
        "distribution_compliance_via_p217m_acl_only", "drug_regulatory_via_p217k_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_human_regulatory_oversight",
        "never_autonomous_regulatory_submission_without_approval",
        "never_skip_explainable_regulatory_ai", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "never_replace_compliance_platform",
        "module_local_biotechnology_bio_regulatory_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-regulatory")', "/bio-regulatory/vision",
        "/bio-regulatory/architecture", "/bio-regulatory/regulatory-ai",
        "/bio-regulatory/biomedical-compliance", "/bio-regulatory/knowledge-graph",
        "/bio-regulatory/regulatory-digital-twin", "/bio-regulatory/compliance-operations",
        "/bio-regulatory/agents", "/bio-regulatory/domain-model", "/bio-regulatory/global-network",
        "/bio-regulatory/ethics", "/bio-regulatory/robotics-integration",
        "/bio-regulatory/quantum-readiness", "/bio-regulatory/governance",
        "/bio-regulatory/security", "/bio-regulatory/integration", "/bio-regulatory/roadmap",
        "/bio-regulatory/cqrs", "/bio-regulatory/events", "/bio-regulatory/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_REGULATORY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Regulatory Platform is missing",
        "Never Regulatory AI is missing",
        "Never Biomedical Compliance is missing",
        "Never Life Science Governance is missing",
        "Never Regulatory Knowledge Graph is missing",
        "Never Digital Twin is missing",
        "Never AI Agents are missing",
        "Never Quantum Readiness is missing",
        "Never Security Architecture is missing",
        "Never Ethics is missing",
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
        "Never Replace P217-K Drug Discovery",
        "Never Replace P217-L Bio Manufacturing",
        "Never Replace P217-M Bio Supply Chain",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Replace Compliance Platform SoR",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Never Skip Human Regulatory Oversight",
        "Never Autonomous Regulatory Submission Without Approval",
        "Never Skip Explainable Regulatory AI",
        "Create an intelligent regulatory ecosystem capable of continuously monitoring",
        "P217", "P217-M", "P216-Z", "P215-Z", "P214-Z", "P217-O",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-N", "adr": 513, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
