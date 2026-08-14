"""Biotechnology P217-V Bio-GI foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/521-enterprise-biotechnology-bio-gi.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_GI.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_GI_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_GI_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_GI_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_GI_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_GI_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_gi.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_gi_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_gi_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_gi_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_gi_platform",
    "backend/contexts/bio_general_intelligence_platform",
    "backend/contexts/cognitive_bio_enterprise_platform",
)
def validate_bio_gi_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_gi_aggregates import (
        BioGiPlatformRoot, BiologicalReasoningRoot, FoundationModelsRoot,
        CognitiveEnterpriseRoot, BioGiKnowledgeGraphRoot, BioGiDigitalTwinRoot,
        CognitiveAgentsRoot, BioIntelligenceRoot, BioGiGovernanceRoot,
        BioGiExplainabilityRoot, BioGiSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_gi as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-V" and cat["adr"] == 521 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_general_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L" and cat["bio_supply_chain_gate"] == "P217-M"
        and cat["bio_regulatory_gate"] == "P217-N" and cat["bio_sustainability_gate"] == "P217-O"
        and cat["bio_marketplace_gate"] == "P217-P" and cat["bio_innovation_gate"] == "P217-Q"
        and cat["bio_investment_gate"] == "P217-R" and cat["bio_security_gate"] == "P217-S"
        and cat["bio_future_gate"] == "P217-T" and cat["bio_autonomous_gate"] == "P217-U"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_gi_architecture_present_required"] is True
        and cat["biological_reasoning_present_required"] is True
        and cat["foundation_models_present_required"] is True
        and cat["cognitive_enterprise_present_required"] is True
        and cat["bio_gi_knowledge_graph_present_required"] is True
        and cat["bio_gi_digital_twin_present_required"] is True
        and cat["cognitive_agents_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["biological_reasoning"]["capability_count"] == 4
        and cat["foundation_models"]["domain_count"] == 5
        and cat["cognitive_enterprise"]["capability_count"] == 4
        and cat["bio_gi_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_u_bio_autonomous"] is True
        and cat["never_replace_p217_t_bio_future"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["bio_gi_twins_via_p217g_acl_only"] is True
        and cat["autonomy_execution_via_p217u_acl_only"] is True
        and cat["future_evolution_via_p217t_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_explainable_bio_gi_reasoning"] is True
        and cat["never_skip_human_cognitive_oversight"] is True
        and cat["never_skip_responsible_bio_gi_governance"] is True
        and cat["never_unvalidated_cognitive_decision_release"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_w"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioGiPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        BiologicalReasoningRoot.enable(tenant_id="t1", reasoning_ref="r1").is_missing() is False,
        FoundationModelsRoot.enable(tenant_id="t1", models_ref="m1").is_missing() is False,
        CognitiveEnterpriseRoot.enable(tenant_id="t1", enterprise_ref="e1").is_missing() is False,
        BioGiKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        BioGiDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CognitiveAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        BioGiGovernanceRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        BioGiExplainabilityRoot.enable(tenant_id="t1", explainability_ref="ex1").is_missing() is False,
        BioGiSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_gi_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l", "via_p217_m", "via_p217_n", "via_p217_o", "via_p217_p", "via_p217_q", "via_p217_r", "via_p217_s", "via_p217_t", "via_p217_u",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery", "never_replace_p217_l_bio_manufacturing",
        "never_replace_p217_m_bio_supply_chain", "never_replace_p217_n_bio_regulatory",
        "never_replace_p217_o_bio_sustainability", "never_replace_p217_p_bio_marketplace",
        "never_replace_p217_q_bio_innovation", "never_replace_p217_r_bio_investment",
        "never_replace_p217_s_bio_security", "never_replace_p217_t_bio_future",
        "never_replace_p217_u_bio_autonomous",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "bio_gi_twins_via_p217g_acl_only", "autonomy_execution_via_p217u_acl_only",
        "future_evolution_via_p217t_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_explainable_bio_gi_reasoning",
        "never_skip_human_cognitive_oversight",
        "never_skip_responsible_bio_gi_governance",
        "never_unvalidated_cognitive_decision_release", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_gi_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-gi")', "/bio-gi/vision",
        "/bio-gi/architecture", "/bio-gi/biological-reasoning",
        "/bio-gi/foundation-models", "/bio-gi/cognitive-enterprise",
        "/bio-gi/digital-twin", "/bio-gi/knowledge-graph",
        "/bio-gi/agents", "/bio-gi/domain-model",
        "/bio-gi/robotics-integration", "/bio-gi/quantum-readiness",
        "/bio-gi/governance", "/bio-gi/security",
        "/bio-gi/integration", "/bio-gi/roadmap",
        "/bio-gi/cqrs", "/bio-gi/events", "/bio-gi/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_GI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio-GI Architecture is missing",
        "Never Biological Reasoning is missing",
        "Never Foundation Models are missing",
        "Never Cognitive Enterprise is missing",
        "Never Bio-GI Knowledge Graph is missing",
        "Never Bio-GI Digital Twin is missing",
        "Never Cognitive Agents are missing",
        "Never Governance is missing",
        "Never Quantum Readiness is missing",
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
        "Never Replace P217-K Drug Discovery",
        "Never Replace P217-L Bio Manufacturing",
        "Never Replace P217-M Bio Supply Chain",
        "Never Replace P217-N Bio Regulatory",
        "Never Replace P217-O Bio Sustainability",
        "Never Replace P217-P Bio Marketplace",
        "Never Replace P217-Q Bio Innovation",
        "Never Replace P217-R Bio Investment",
        "Never Replace P217-S Bio Security",
        "Never Replace P217-T Bio Future",
        "Never Replace P217-U Bio Autonomous",
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
        "Never Skip Explainable Bio-GI Reasoning",
        "Never Skip Human Cognitive Oversight",
        "Never Skip Responsible Bio-GI Governance",
        "Never Unvalidated Cognitive Decision Release",
        "Create a next-generation biological intelligence system capable of understanding",
        "P217", "P217-U", "P217-T", "P216-Z", "P215-Z", "P214-Z", "P217-W",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-V", "adr": 521, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
