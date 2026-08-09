"""Civilization P219-Q consciousness intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/570-enterprise-civilization-operating-system-consciousness.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_CONSCIOUSNESS.md",
    "docs/architecture/civilization/CIVILIZATION_CONSCIOUSNESS_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_CONSCIOUSNESS_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_CONSCIOUSNESS_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_CONSCIOUSNESS_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_CONSCIOUSNESS_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_consciousness.py",
    "backend/contexts/civilization/domain/aggregates/civ_consciousness_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_consciousness_acl.py",
    "backend/contexts/civilization/application/civ_consciousness_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_consciousness_intelligence_platform",
    "backend/contexts/collective_consciousness_network_bc",
    "backend/contexts/wisdom_intelligence_platform_bc",
)


def validate_civ_consciousness_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_consciousness_aggregates import (
        CivilizationAwarenessPlatformRoot,
        CivilizationConsciousnessIntelligencePlatformRoot,
        CivilizationDigitalTwinRoot,
        CivilizationKnowledgeGraphRoot,
        CollectiveConsciousnessNetworkRoot,
        CollectiveLearningPlatformRoot,
        ConsciousnessEventArchitectureRoot,
        MeosCivilizationConsciousnessIntelligenceCoreRoot,
        WisdomIntelligencePlatformRoot,
    )
    from contexts.civilization.domain.services import civ_platform_consciousness as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-Q" and cat["adr"] == 570 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_consciousness_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["collaboration_gate"] == "P219-P"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_consciousness_intelligence_platform_present_required"] is True
        and cat["collective_consciousness_network_present_required"] is True
        and cat["wisdom_intelligence_platform_present_required"] is True
        and cat["civilization_awareness_platform_present_required"] is True
        and cat["collective_learning_platform_present_required"] is True
        and cat["civilization_digital_twin_present_required"] is True
        and cat["meos_civilization_consciousness_intelligence_core_present_required"] is True
        and cat["civilization_knowledge_graph_present_required"] is True
        and cat["consciousness_event_architecture_present_required"] is True
        and cat["consciousness_cqrs_model_present_required"] is True
        and cat["meos_consciousness_integration_map_present_required"] is True
        and cat["architecture"]["evolution_stage_count"] == 7
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["awareness_domain_count"] == 10
        and cat["architecture"]["wisdom_domain_count"] == 8
        and cat["architecture"]["awareness_platform_domain_count"] == 9
        and cat["architecture"]["learning_lifecycle_step_count"] == 7
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 4
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_p_collaboration"] is True
        and cat["never_replace_p219_e_ai_os"] is True
        and cat["never_replace_p219_i_knowledge"] is True
        and cat["never_ungated_consciousness_recommendation_execution"] is True
        and cat["never_treat_wisdom_score_as_binding_policy"] is True
        and cat["never_bypass_constitutional_ai_safeguards"] is True
        and cat["never_opaque_unexplainable_consciousness_decisions"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_r"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationConsciousnessIntelligencePlatformRoot.enable(
            tenant_id="t1", consciousness_ref="c1"
        ).is_missing() is False,
        CollectiveConsciousnessNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        WisdomIntelligencePlatformRoot.enable(tenant_id="t1", wisdom_ref="w1").is_missing() is False,
        CivilizationAwarenessPlatformRoot.enable(
            tenant_id="t1", awareness_ref="a1"
        ).is_missing() is False,
        CollectiveLearningPlatformRoot.enable(tenant_id="t1", learning_ref="l1").is_missing() is False,
        CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationConsciousnessIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        CivilizationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ConsciousnessEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_consciousness_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d", "via_p219_e",
        "via_p219_f", "via_p219_g", "via_p219_h", "via_p219_i", "via_p219_j", "via_p219_k",
        "via_p219_l", "via_p219_m", "via_p219_n", "via_p219_o", "via_p219_p",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os", "never_replace_p219_i_knowledge",
        "never_replace_p219_k_governance", "never_replace_p219_p_collaboration",
        "never_opaque_unexplainable_consciousness_decisions",
        "never_ungated_consciousness_recommendation_execution",
        "never_treat_wisdom_score_as_binding_policy",
        "never_skip_ethical_consciousness_governance",
        "never_skip_human_authority_consciousness",
        "never_violate_human_sovereignty_consciousness",
        "never_bypass_trusted_consciousness_validation",
        "never_bypass_constitutional_ai_safeguards",
        "module_local_llm_forbidden",
        "module_local_civilization_consciousness_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/consciousness")',
        "/consciousness/architecture", "/consciousness/network", "/consciousness/wisdom",
        "/consciousness/awareness", "/consciousness/learning", "/consciousness/digital-twin",
        "/consciousness/knowledge-graph", "/consciousness/agents", "/consciousness/bounded-contexts",
        "/consciousness/aggregates", "/consciousness/events", "/consciousness/cqrs",
        "/consciousness/integration", "/consciousness/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_CONSCIOUSNESS.md").read_text(
        encoding="utf-8"
    )
    doc_ok = all(x in law for x in (
        "Never Civilization Consciousness Intelligence Platform is missing",
        "Never Collective Consciousness Network is missing",
        "Never Wisdom Intelligence Platform is missing",
        "Never Civilization Awareness Platform is missing",
        "Never Collective Learning Platform is missing",
        "Never Civilization Digital Twin is missing",
        "Never MEOS Civilization Consciousness Intelligence Core is missing",
        "Never Civilization Knowledge Graph is missing",
        "Never Consciousness Event Architecture is missing",
        "Never Consciousness CQRS Model is missing",
        "Never MEOS Consciousness Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-I Knowledge",
        "Never Replace P219-P Collaboration",
        "Never Opaque Unexplainable Consciousness Decisions",
        "Never Ungated Consciousness Recommendation Execution",
        "Never Treat Wisdom Score As Binding Policy",
        "Never Bypass Constitutional AI Safeguards",
        "transforming global knowledge, experience, evidence and intelligence into",
        "P219-R",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-Q", "adr": 570, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
