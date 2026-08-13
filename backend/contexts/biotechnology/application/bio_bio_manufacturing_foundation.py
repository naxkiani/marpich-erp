"""Biotechnology P217-L Bio Manufacturing foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/511-enterprise-biotechnology-bio-manufacturing.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_MANUFACTURING.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_MANUFACTURING_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_MANUFACTURING_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_MANUFACTURING_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_MANUFACTURING_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_MANUFACTURING_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_manufacturing.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_manufacturing_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_manufacturing_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_manufacturing_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_manufacturing_platform",
    "backend/contexts/smart_bio_factory_platform",
    "backend/contexts/biopharmaceutical_mes_platform",
)
def validate_bio_manufacturing_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_manufacturing_aggregates import (
        BioManufacturingPlatformRoot, SmartBioFactoryRoot, BioProductionAutomationRoot,
        ManufacturingAiRoot, ManufacturingDigitalTwinRoot, QualityIntelligenceRoot,
        ManufacturingAgentsRoot, BioManufacturingGovernanceRoot, BioManufacturingSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_manufacturing as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-L" and cat["adr"] == 511 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_manufacturing_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["biomedical_manufacturing_platform_present_required"] is True
        and cat["smart_bio_factory_present_required"] is True
        and cat["bio_production_automation_present_required"] is True
        and cat["manufacturing_ai_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["robotics_integration_present_required"] is True
        and cat["quality_intelligence_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["bio_pos"]["component_count"] == 4
        and cat["biopharma"]["domain_count"] == 4
        and cat["automation"]["domain_count"] == 4
        and cat["manufacturing_ai"]["engine_count"] == 4
        and cat["manufacturing_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_k_drug_discovery"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["manufacturing_twins_via_p217g_acl_only"] is True
        and cat["product_intelligence_via_p217k_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_gmp_compliance"] is True
        and cat["never_skip_human_manufacturing_oversight"] is True
        and cat["never_autonomous_release_without_quality_approval"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_m"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioManufacturingPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        SmartBioFactoryRoot.enable(tenant_id="t1", factory_ref="f1").is_missing() is False,
        BioProductionAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        ManufacturingAiRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        ManufacturingDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        QualityIntelligenceRoot.enable(tenant_id="t1", quality_ref="q1").is_missing() is False,
        ManufacturingAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioManufacturingGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        BioManufacturingSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_manufacturing_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "manufacturing_twins_via_p217g_acl_only", "product_intelligence_via_p217k_acl_only",
        "robotics_via_p216z_acl_only", "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_gmp_compliance", "never_skip_human_manufacturing_oversight",
        "never_autonomous_release_without_quality_approval", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_manufacturing_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-manufacturing")', "/bio-manufacturing/vision",
        "/bio-manufacturing/architecture", "/bio-manufacturing/bio-pos",
        "/bio-manufacturing/biopharma", "/bio-manufacturing/automation",
        "/bio-manufacturing/manufacturing-digital-twin", "/bio-manufacturing/manufacturing-ai",
        "/bio-manufacturing/knowledge-graph", "/bio-manufacturing/agents",
        "/bio-manufacturing/domain-model", "/bio-manufacturing/robotics-integration",
        "/bio-manufacturing/quantum-readiness", "/bio-manufacturing/governance",
        "/bio-manufacturing/security", "/bio-manufacturing/integration",
        "/bio-manufacturing/roadmap", "/bio-manufacturing/cqrs", "/bio-manufacturing/events",
        "/bio-manufacturing/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_MANUFACTURING.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Biomedical Manufacturing Platform is missing",
        "Never Smart Bio Factory is missing",
        "Never Bio Production Automation is missing",
        "Never Manufacturing AI is missing",
        "Never Digital Twin is missing",
        "Never Robotics Integration is missing",
        "Never Quality Intelligence is missing",
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
        "Never Replace P217-K Drug Discovery",
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
        "Never Skip GMP Compliance",
        "Never Skip Human Manufacturing Oversight",
        "Never Autonomous Release Without Quality Approval",
        "Create an intelligent biological manufacturing ecosystem capable of designing",
        "P217", "P217-K", "P216-Z", "P215-Z", "P214-Z", "P217-M",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-L", "adr": 511, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
