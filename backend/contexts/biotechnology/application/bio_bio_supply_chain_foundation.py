"""Biotechnology P217-M Bio Supply Chain foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/512-enterprise-biotechnology-bio-supply-chain.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_SUPPLY_CHAIN.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SUPPLY_CHAIN_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SUPPLY_CHAIN_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SUPPLY_CHAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SUPPLY_CHAIN_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_SUPPLY_CHAIN_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_supply_chain.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_supply_chain_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_supply_chain_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_supply_chain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_supply_chain_platform",
    "backend/contexts/cold_chain_intelligence_platform",
    "backend/contexts/bio_logistics_platform",
)
def validate_bio_supply_chain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_supply_chain_aggregates import (
        BioSupplyChainPlatformRoot, BioLogisticsRoot, ColdChainIntelligenceRoot,
        BioInventoryIntelligenceRoot, TraceabilityNetworkRoot, SupplyDigitalTwinRoot,
        SupplyAgentsRoot, BioSupplyGovernanceRoot, BioSupplySecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_supply_chain as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-M" and cat["adr"] == 512 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_supply_chain_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D" and cat["bio_ai_gate"] == "P217-E"
        and cat["synthetic_gate"] == "P217-F" and cat["simulation_gate"] == "P217-G"
        and cat["digital_health_gate"] == "P217-H" and cat["precision_medicine_gate"] == "P217-I"
        and cat["clinical_research_gate"] == "P217-J" and cat["drug_discovery_gate"] == "P217-K"
        and cat["bio_manufacturing_gate"] == "P217-L"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_supply_chain_platform_present_required"] is True
        and cat["bio_logistics_present_required"] is True
        and cat["cold_chain_intelligence_present_required"] is True
        and cat["inventory_intelligence_present_required"] is True
        and cat["traceability_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["ai_agents_present_required"] is True
        and cat["quantum_readiness_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["meos_integration_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["bio_logistics"]["capability_count"] == 4
        and cat["cold_chain"]["domain_count"] == 4
        and cat["bio_inventory"]["category_count"] == 4
        and cat["supply_ai"]["engine_count"] == 4
        and cat["supply_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_l_bio_manufacturing"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["never_replace_inventory"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["supply_twins_via_p217g_acl_only"] is True
        and cat["manufacturing_via_p217l_acl_only"] is True
        and cat["product_intelligence_via_p217k_acl_only"] is True
        and cat["robotics_via_p216z_acl_only"] is True
        and cat["quantum_optimization_via_p215z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_skip_cold_chain_integrity"] is True
        and cat["never_skip_human_logistics_oversight"] is True
        and cat["never_untraceable_biological_material_movement"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_n"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioSupplyChainPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        BioLogisticsRoot.enable(tenant_id="t1", logistics_ref="l1").is_missing() is False,
        ColdChainIntelligenceRoot.enable(tenant_id="t1", cold_chain_ref="c1").is_missing() is False,
        BioInventoryIntelligenceRoot.enable(tenant_id="t1", inventory_ref="i1").is_missing() is False,
        TraceabilityNetworkRoot.enable(tenant_id="t1", trace_ref="t1").is_missing() is False,
        SupplyDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SupplyAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        BioSupplyGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        BioSupplySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_supply_chain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p217_e", "via_p217_f",
        "via_p217_g", "via_p217_h", "via_p217_i", "via_p217_j", "via_p217_k", "via_p217_l",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p217_e_bio_ai", "never_replace_p217_f_synthetic",
        "never_replace_p217_g_simulation", "never_replace_p217_h_digital_health",
        "never_replace_p217_i_precision_medicine", "never_replace_p217_j_clinical_research",
        "never_replace_p217_k_drug_discovery", "never_replace_p217_l_bio_manufacturing",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only",
        "supply_twins_via_p217g_acl_only", "manufacturing_via_p217l_acl_only",
        "product_intelligence_via_p217k_acl_only", "robotics_via_p216z_acl_only",
        "quantum_optimization_via_p215z_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_skip_cold_chain_integrity", "never_skip_human_logistics_oversight",
        "never_untraceable_biological_material_movement", "opaque_bio_safety_strategy_forbidden",
        "never_replace_hospital_emr", "never_replace_inventory",
        "module_local_biotechnology_bio_supply_chain_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-supply-chain")', "/bio-supply-chain/vision",
        "/bio-supply-chain/architecture", "/bio-supply-chain/bio-logistics",
        "/bio-supply-chain/cold-chain", "/bio-supply-chain/bio-inventory",
        "/bio-supply-chain/traceability", "/bio-supply-chain/supply-digital-twin",
        "/bio-supply-chain/supply-ai", "/bio-supply-chain/knowledge-graph",
        "/bio-supply-chain/agents", "/bio-supply-chain/domain-model",
        "/bio-supply-chain/robotics-integration", "/bio-supply-chain/quantum-readiness",
        "/bio-supply-chain/governance", "/bio-supply-chain/security",
        "/bio-supply-chain/integration", "/bio-supply-chain/roadmap",
        "/bio-supply-chain/cqrs", "/bio-supply-chain/events", "/bio-supply-chain/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_SUPPLY_CHAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Supply Chain Platform is missing",
        "Never Bio Logistics is missing",
        "Never Cold Chain Intelligence is missing",
        "Never Inventory Intelligence is missing",
        "Never Traceability is missing",
        "Never Digital Twin is missing",
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
        "Never Replace P217-L Bio Manufacturing",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Replace Inventory SoR",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Never Skip Cold Chain Integrity",
        "Never Skip Human Logistics Oversight",
        "Never Untraceable Biological Material Movement",
        "Create a globally connected biotechnology supply network capable of monitoring",
        "P217", "P217-L", "P216-Z", "P215-Z", "P214-Z", "P217-N",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-M", "adr": 512, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
