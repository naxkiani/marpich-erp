"""Biotechnology P217-W Bio Civilization foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/524-enterprise-biotechnology-bio-civilization.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_CIVILIZATION.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_CIVILIZATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_CIVILIZATION_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_CIVILIZATION_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_CIVILIZATION_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_CIVILIZATION_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_civilization.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_bio_civilization_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_bio_civilization_acl.py",
    "backend/contexts/biotechnology/application/bio_bio_civilization_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/bio_civilization_platform",
    "backend/contexts/collective_bio_intelligence_platform",
    "backend/contexts/human_bio_ai_symbiosis_platform",
)
def validate_bio_civilization_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_bio_civilization_aggregates import (
        BioCivilizationIntelligenceRoot, CollectiveBiologicalNetworkRoot,
        GlobalBioCognitiveEcosystemRoot, HumanBioAiSymbiosisRoot,
        KnowledgeCivilizationRoot, MultiAgentBioSocietyRoot,
        CollectiveBioDecisionRoot, CivilizationKnowledgeGraphRoot,
        BioCivilizationDigitalTwinRoot, HumanCivilizationOversightRoot,
        BioCivilizationSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_civilization as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-W" and cat["adr"] == 524 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_civilization_intelligence_fabric"
        and cat["bio_gi_gate"] == "P217-V" and cat["bio_security_gate"] == "P217-S"
        and cat["bio_autonomous_gate"] == "P217-U" and cat["bio_future_gate"] == "P217-T"
        and cat["simulation_gate"] == "P217-G"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_civilization_intelligence_present_required"] is True
        and cat["collective_biological_intelligence_network_present_required"] is True
        and cat["global_bio_cognitive_ecosystem_present_required"] is True
        and cat["human_bio_ai_symbiosis_framework_present_required"] is True
        and cat["knowledge_civilization_platform_present_required"] is True
        and cat["multi_agent_bio_society_present_required"] is True
        and cat["collective_bio_decision_intelligence_present_required"] is True
        and cat["civilization_knowledge_graph_present_required"] is True
        and cat["architecture"]["layer_count"] == 6
        and cat["collective_biological_network"]["capability_count"] == 4
        and cat["global_bio_cognitive_ecosystem"]["pillar_count"] == 4
        and cat["human_bio_ai_symbiosis"]["component_count"] == 4
        and cat["civilization_agents"]["agent_count"] == 6
        and cat["domain_models"]["domain_count"] == 3
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_v_bio_gi"] is True
        and cat["never_replace_compliance_platform"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["bio_gi_cognition_via_p217v_acl_only"] is True
        and cat["civilization_intelligence_via_p217w_acl_only"] is True
        and cat["security_via_p217s_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungoverned_cross_tenant_intelligence_federation"] is True
        and cat["never_opaque_collective_decisions"] is True
        and cat["never_skip_human_civilization_oversight"] is True
        and cat["never_skip_collective_bio_ethics_controls"] is True
        and cat["never_skip_human_bio_ai_symbiosis_controls"] is True
        and cat["never_unvalidated_civilization_scenario_release"] is True
        and cat["foundation_for_p217_x"] is True
        and cat["foundation_for_p217_y"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioCivilizationIntelligenceRoot.enable(tenant_id="t1", civilization_ref="c1").is_missing() is False,
        CollectiveBiologicalNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        GlobalBioCognitiveEcosystemRoot.enable(tenant_id="t1", ecosystem_ref="e1").is_missing() is False,
        HumanBioAiSymbiosisRoot.enable(tenant_id="t1", symbiosis_ref="s1").is_missing() is False,
        KnowledgeCivilizationRoot.enable(tenant_id="t1", knowledge_ref="k1").is_missing() is False,
        MultiAgentBioSocietyRoot.enable(tenant_id="t1", society_ref="a1").is_missing() is False,
        CollectiveBioDecisionRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        CivilizationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        BioCivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        HumanCivilizationOversightRoot.enable(tenant_id="t1", oversight_ref="o1").is_missing() is False,
        BioCivilizationSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_bio_civilization_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_g", "via_p217_s", "via_p217_t", "via_p217_u", "via_p217_v",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_v_bio_gi",
        "never_replace_compliance_platform", "never_replace_core_platform",
        "bio_ai_via_p214z_acl_only", "bio_gi_cognition_via_p217v_acl_only",
        "civilization_intelligence_via_p217w_acl_only", "security_via_p217s_acl_only",
        "no_module_local_llm", "never_opaque_unexplainable_decisions",
        "never_ungoverned_cross_tenant_intelligence_federation",
        "never_opaque_collective_decisions",
        "never_skip_human_civilization_oversight",
        "never_skip_collective_bio_ethics_controls",
        "never_skip_human_bio_ai_symbiosis_controls",
        "never_unvalidated_civilization_scenario_release",
        "never_replace_hospital_emr", "module_local_biotechnology_bio_civilization_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-civilization")', "/bio-civilization/vision",
        "/bio-civilization/architecture", "/bio-civilization/collective-network",
        "/bio-civilization/ecosystem", "/bio-civilization/symbiosis",
        "/bio-civilization/knowledge", "/bio-civilization/decisions",
        "/bio-civilization/agents", "/bio-civilization/knowledge-graph",
        "/bio-civilization/digital-twin", "/bio-civilization/domain-model",
        "/bio-civilization/robotics-integration", "/bio-civilization/quantum-readiness",
        "/bio-civilization/governance", "/bio-civilization/security",
        "/bio-civilization/integration", "/bio-civilization/roadmap",
        "/bio-civilization/cqrs", "/bio-civilization/events", "/bio-civilization/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_CIVILIZATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Civilization Intelligence Layer is missing",
        "Never Collective Biological Intelligence Network is missing",
        "Never Global Bio Cognitive Ecosystem is missing",
        "Never Human-Bio-AI Symbiosis Framework is missing",
        "Never Knowledge Civilization Platform is missing",
        "Never Multi-Agent Bio Society is missing",
        "Never Collective Bio Decision Intelligence is missing",
        "Never Civilization Knowledge Graph is missing",
        "Never Replace P217-V Bio-GI",
        "Never Replace Core Platform",
        "Never Replace Compliance Platform",
        "Never Module-Local LLM",
        "Never Ungoverned Cross-Tenant Intelligence Federation",
        "Never Opaque Collective Decisions",
        "Never Skip Human Civilization Oversight",
        "Never Skip Collective Bio Ethics Controls",
        "Never Skip Human-Bio-AI Symbiosis Controls",
        "Never Unvalidated Civilization Scenario Release",
        "Create the bio civilization intelligence layer",
        "P217-V", "P217-X", "P214-Z",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-W", "adr": 524, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
